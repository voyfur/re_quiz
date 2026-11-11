#!/usr/bin/env python3
"""Master CLI script to ingest a validated product kit into the Race Expert catalog and rebuild bundles."""

import argparse
from datetime import datetime
import json
from pathlib import Path
import subprocess
import sys
from zoneinfo import ZoneInfo

# Locate paths
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = Path(__file__).resolve().parents[4]
SANDBOX_DIR = PROJECT_ROOT / "test-quiz-sandbox"

CATALOG_PATH = SANDBOX_DIR / "catalog.json"
AUDIT_PATH = PROJECT_ROOT / "wiki" / "projects" / "quiz-set-audit.json"

sys.path.insert(0, str(SCRIPT_DIR))
from normalize_kit_data import ValidationError, normalize_kit


def get_next_identifiers(catalog: list):
    max_row = max(record.get("catalog_row", 0) for record in catalog)
    next_row = max_row + 1
    next_set_id = f"race-expert-{next_row:03d}"
    return next_row, next_set_id


def ingest_kit_record(kit_data: dict, dry_run: bool = False):
    # 1. Normalize and validate
    validated = normalize_kit(kit_data)

    # 2. Load existing catalog and audit
    catalog = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    audit = json.loads(AUDIT_PATH.read_text(encoding="utf-8"))

    # 3. Check for duplicates
    existing_urls = {r.get("source_url") for r in catalog if r.get("source_url")}
    if validated["source_url"] in existing_urls:
        print(f"[WARN] Kit with URL {validated['source_url']!r} already exists in catalog. Proceeding with update.", file=sys.stderr)

    next_row, next_set_id = get_next_identifiers(catalog)
    now_date = datetime.now(ZoneInfo("Europe/Kyiv")).strftime("%Y-%m-%d")

    evidence = validated["matching_evidence"]

    # 4. Construct catalog.json record
    catalog_record = {
        "set_id": next_set_id,
        "catalog_row": next_row,
        "sku": validated.get("sku"),
        "title": validated["title"],
        "source_url": validated["source_url"],
        "price_uah": validated["price_uah"],
        "price_snapshot_date": now_date,
        "composition": validated["composition"],
        "description": validated["description"],
        "tags": validated["tags"],
    }

    # 5. Construct quiz-set-audit.json record
    audit_record = {
        "set_id": next_set_id,
        "catalog_row": next_row,
        "sku": validated.get("sku"),
        "title": validated["title"],
        "source": validated["source_url"],
        "purpose": validated["tags"].get("purpose", []),
        "sport": validated["tags"].get("sport", []),
        "composition": validated["composition"],
        "record_audit_status": "verified_candidate",
        "record_audit_source_date": now_date,
        "audit_cycle": "onboarded_via_skill",
        "full_audit": {
            "evidence_pool": {
                "activity_scope": {
                    "seller_positioned_activity_groups": evidence["seller_activity_groups"],
                    "component_name_activity_groups": evidence["component_activity_groups"],
                },
                "component_classes_from_listed_names": evidence["component_classes"],
                "use_contexts": evidence["use_contexts"],
                "race_formats": evidence["race_formats"],
                "product_forms_visible_in_listed_names": evidence["product_forms"],
                "size_sensitive_item_present": evidence["size_sensitive"],
                "recorded_size_values": evidence["size_values"],
                "season_weather_signals": evidence["weather_signals"],
                "seller_summary_text": validated["description"],
                "conflict_notes": evidence["conflict_notes"],
            },
            "matching_proposal": {
                "status": evidence["status"],
                "why": "Onboarded via race-expert-kit-onboarding skill with validated evidence.",
                "candidate_tiers": {
                    "seller_positioned": evidence["seller_families"],
                    "component_based": evidence["component_families"],
                    "supplemental_page_copy_needs_manual_review": [],
                    "catalog_tags_only_or_auxiliary": [],
                },
            },
        },
    }

    print(f"\n[ONBOARDING PLAN]")
    print(f"  Row: {next_row}")
    print(f"  Set ID: {next_set_id}")
    print(f"  Title: {validated['title']}")
    print(f"  SKU: {validated['sku'] or 'N/A'}")
    print(f"  Price: {validated['price_uah']} UAH")
    print(f"  Goals: {evidence['seller_families']}")
    print(f"  Forms: {evidence['product_forms']}")
    print(f"  Activities: {evidence['seller_activity_groups']}")

    if dry_run:
        print("\n[DRY RUN] No files were modified.")
        return catalog_record, audit_record

    # 6. Append records
    catalog.append(catalog_record)
    audit["records"].append(audit_record)

    CATALOG_PATH.write_text(json.dumps(catalog, ensure_ascii=False, indent=2), encoding="utf-8")
    AUDIT_PATH.write_text(json.dumps(audit, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[OK] Appended to catalog.json and quiz-set-audit.json (Total kits: {len(catalog)})")

    # 7. Rebuild bundles
    print("[1/2] Rebuilding web bundles (catalog_data.js and client_matcher.js)...")
    res_b = subprocess.run([sys.executable, str(SANDBOX_DIR / "build_bundle.py")], capture_output=True, text=True)
    if res_b.returncode != 0:
        print(f"[ERROR] build_bundle.py failed:\n{res_b.stderr}", file=sys.stderr)
        sys.exit(1)

    print("[2/2] Rebuilding external HTML pages (public/index.html and quiz.html)...")
    res_h = subprocess.run([sys.executable, str(PROJECT_ROOT / "build_external_quiz_v2.py")], capture_output=True, text=True)
    if res_h.returncode != 0:
        print(f"[ERROR] build_external_quiz_v2.py failed:\n{res_h.stderr}", file=sys.stderr)
        sys.exit(1)

    # 8. Copy to chat artifact
    chat_artifact = Path("/Users/anatoly/.gemini/antigravity/brain/4168c8d8-570e-488d-9192-d410885bdf9c/quiz_interactive.html")
    if chat_artifact.parent.exists():
        chat_artifact.write_text((PROJECT_ROOT / "public" / "index.html").read_text(encoding="utf-8"), encoding="utf-8")

    print("\n🎉 [SUCCESS] New kit successfully ingested into quiz catalog and all frontend bundles!")
    return catalog_record, audit_record


def main():
    parser = argparse.ArgumentParser(description="Ingest a new product kit into the Race Expert quiz catalog.")
    parser.add_argument("input_json", help="Path to normalized kit JSON file")
    parser.add_argument("--dry-run", action="store_true", help="Perform validation without writing")
    args = parser.parse_args()

    data = json.loads(Path(args.input_json).read_text(encoding="utf-8"))
    ingest_kit_record(data, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
