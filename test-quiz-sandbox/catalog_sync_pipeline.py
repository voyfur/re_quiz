#!/usr/bin/env python3
"""Autonomous Catalog Synchronization Pipeline for Race Expert Quiz.

Ingests products from OpenCart, enriches new kits with AI, validates with DataGuard,
and updates the production catalog bundle.
"""

import os
import sys
import json
import logging
import argparse
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple

ROOT = Path(__file__).resolve().parent
PROJECT_ROOT = ROOT.parent
sys.path.insert(0, str(ROOT))

from kit_extractor import OpenCartKitExtractor, MockKitExtractor
from kit_ai_tagger import LLMKitTagger, HeuristicKitTagger
from kit_data_guard import KitDataGuard
from build_bundle import build as build_bundle

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger("sync_pipeline")

CATALOG_PATH = ROOT / "catalog.json"
AUDIT_PATH = (
    PROJECT_ROOT / "wiki" / "projects" / "quiz-set-audit.json"
    if (PROJECT_ROOT / "wiki" / "projects" / "quiz-set-audit.json").exists()
    else ROOT / "quiz-set-audit.json"
)
REPORT_PATH = ROOT / "sync_report.json"


def load_current_catalog() -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
    catalog = []
    if CATALOG_PATH.exists():
        catalog = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    
    audit = {"records": []}
    if AUDIT_PATH.exists():
        audit = json.loads(AUDIT_PATH.read_text(encoding="utf-8"))
        
    return catalog, audit


def run_sync(
    mock: bool = False,
    dry_run: bool = False,
    use_llm: bool = True,
    limit: Optional[int] = None
) -> Dict[str, Any]:
    start_time = datetime.now()
    logger.info(f"Starting Race Expert Quiz Catalog Sync (mock={mock}, dry_run={dry_run}, use_llm={use_llm})")

    # 1. Initialize extractor
    if mock:
        extractor = MockKitExtractor()
    else:
        try:
            extractor = OpenCartKitExtractor()
        except Exception as e:
            logger.error(f"Failed to connect to OpenCart MySQL: {e}. Falling back to Mock.")
            extractor = MockKitExtractor()

    # 2. Extract kits from OpenCart
    try:
        candidate_kits = extractor.fetch_all_candidate_kits(limit=limit)
        logger.info(f"Extracted {len(candidate_kits)} candidate kit records from OpenCart.")
    finally:
        extractor.close()

    # 3. Load local catalog & audit
    catalog, audit = load_current_catalog()
    existing_skus = {item.get("sku") for item in catalog if item.get("sku")}
    existing_by_sku = {item.get("sku"): item for item in catalog if item.get("sku")}
    existing_by_row = {item.get("catalog_row"): item for item in catalog}
    
    audit_records = audit.get("records", [])
    audit_by_row = {r.get("catalog_row"): r for r in audit_records}

    # 4. Initialize taggers
    tagger = LLMKitTagger() if use_llm else HeuristicKitTagger()

    new_kits_added = 0
    prices_updated = 0
    stock_updated = 0
    skipped_count = 0
    audit_warnings = []

    max_row = max(existing_by_row.keys()) if existing_by_row else 0
    next_set_num = len(catalog) + 1

    for kit in candidate_kits:
        sku = kit.get("sku") or kit.get("model")
        price = kit.get("price_uah", 0)
        in_stock = kit.get("in_stock", True)

        if sku in existing_by_sku:
            # Existing kit: update price and stock
            existing_item = existing_by_sku[sku]
            if existing_item.get("price_uah") != price:
                old_p = existing_item.get("price_uah")
                existing_item["price_uah"] = price
                existing_item["price_snapshot_date"] = datetime.now().strftime("%Y-%m-%d")
                prices_updated += 1
                logger.info(f"Updated price for {sku}: {old_p} -> {price} UAH")

            # Update availability tag
            avail = "in_stock" if in_stock else "out_of_stock"
            tags = existing_item.setdefault("tags", {})
            tags["availability"] = [avail]
            stock_updated += 1
        else:
            # Brand new kit! Tag with AI & validate with DataGuard
            logger.info(f"New kit found: {kit.get('title')} ({sku}). Tagging...")
            raw_tags = tagger.tag(kit)
            is_valid, issues, fixed_tags = KitDataGuard.validate_and_fix(kit, raw_tags)
            
            if not is_valid:
                logger.warning(f"Kit {sku} rejected by DataGuard: {issues}")
                audit_warnings.extend(issues)
                skipped_count += 1
                continue

            if issues:
                audit_warnings.extend(issues)

            max_row += 1
            new_set_id = f"race-expert-{next_set_num:03d}"
            next_set_num += 1

            new_catalog_item = {
                "set_id": new_set_id,
                "catalog_row": max_row,
                "sku": sku,
                "title": kit.get("title"),
                "source_url": kit.get("source_url"),
                "price_uah": price,
                "price_snapshot_date": datetime.now().strftime("%Y-%m-%d"),
                "composition": fixed_tags.get("composition", ""),
                "description": fixed_tags.get("seller_summary", ""),
                "tags": {
                    "item_type": ["bundle_set"],
                    "availability": ["in_stock" if in_stock else "out_of_stock"],
                    "price": [f"{price}_uah"],
                    "sport": fixed_tags.get("seller_activity_groups", ["running"]),
                    "shoe_size": fixed_tags.get("size_values", [])
                }
            }
            catalog.append(new_catalog_item)
            existing_by_sku[sku] = new_catalog_item

            # Add corresponding audit record
            new_audit_record = {
                "catalog_row": max_row,
                "sku": sku,
                "full_audit": {
                    "evidence_pool": {
                        "activity_scope": {
                            "seller_positioned_activity_groups": fixed_tags.get("seller_activity_groups", []),
                            "component_name_activity_groups": fixed_tags.get("component_activity_groups", [])
                        },
                        "component_classes_from_listed_names": fixed_tags.get("component_classes", []),
                        "product_forms_visible_in_listed_names": fixed_tags.get("product_forms", [])
                    },
                    "matching_proposal": {
                        "candidate_tiers": {}
                    }
                }
            }
            audit_records.append(new_audit_record)
            new_kits_added += 1

    # 5. Save changes if not dry_run
    if not dry_run and (new_kits_added > 0 or prices_updated > 0):
        logger.info(f"Writing {len(catalog)} catalog entries and {len(audit_records)} audit records...")
        CATALOG_PATH.write_text(json.dumps(catalog, ensure_ascii=False, indent=2), encoding="utf-8")
        audit["records"] = audit_records
        AUDIT_PATH.write_text(json.dumps(audit, ensure_ascii=False, indent=2), encoding="utf-8")
        
        logger.info("Rebuilding JS bundle...")
        build_bundle()

    duration_sec = (datetime.now() - start_time).total_seconds()
    report = {
        "timestamp": datetime.now().isoformat(),
        "duration_sec": round(duration_sec, 2),
        "total_catalog_size": len(catalog),
        "new_kits_added": new_kits_added,
        "prices_updated": prices_updated,
        "stock_updated": stock_updated,
        "skipped_count": skipped_count,
        "warnings_count": len(audit_warnings),
        "warnings": audit_warnings[:20],
        "status": "SUCCESS"
    }

    if not dry_run:
        REPORT_PATH.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    logger.info(
        f"Sync completed in {duration_sec:.2f}s: "
        f"{new_kits_added} new kits, {prices_updated} prices updated, {len(catalog)} total."
    )
    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sync Race Expert kits with OpenCart")
    parser.add_argument("--mock", action="store_true", help="Use mock extractor instead of real DB")
    parser.add_argument("--dry-run", action="store_true", help="Perform checks without saving to disk")
    parser.add_argument("--no-llm", action="store_true", help="Use heuristic tagger instead of OpenAI LLM")
    parser.add_argument("--limit", type=int, default=None, help="Limit number of candidate kits")
    args = parser.parse_args()

    res = run_sync(mock=args.mock, dry_run=args.dry_run, use_llm=not args.no_llm, limit=args.limit)
    print(json.dumps(res, indent=2, ensure_ascii=False))
