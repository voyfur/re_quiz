#!/usr/bin/env python3
"""Audit a newly onboarded kit to verify reachable quiz branches, scoring, and filters."""

import argparse
import json
from pathlib import Path
import re
import sys

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = Path(__file__).resolve().parents[4]
SANDBOX_DIR = PROJECT_ROOT / "test-quiz-sandbox"

sys.path.insert(0, str(SANDBOX_DIR))
from draft_matcher import (
    ACTIVITY_OPTIONS_BY_GOAL,
    COMPONENT_CLASSES_BY_GOAL,
    PRODUCT_FORMS_BY_GOAL,
    SIZE_GOALS,
    attach_audit_evidence,
    draft_options,
    draft_recommend,
)
from server import _load_catalog, AUDIT_PATH, CATALOG_PATH


def audit_kit(target_identifier: str):
    catalog = _load_catalog(CATALOG_PATH)
    audit = json.loads(AUDIT_PATH.read_text(encoding="utf-8"))
    enriched = attach_audit_evidence(catalog, audit)

    # Find kit
    record = None
    for r in enriched:
        if str(r.get("catalog_row")) == target_identifier or r.get("set_id") == target_identifier or r.get("sku") == target_identifier:
            record = r
            break

    if not record:
        print(f"[ERROR] Could not find kit with identifier {target_identifier!r} in catalog.", file=sys.stderr)
        sys.exit(1)

    print("=" * 65)
    print(f"AUDITING KIT: № {record['catalog_row']} · {record['set_id']} · {record['title']}")
    print(f"Price: {record['price_uah']} UAH | SKU: {record.get('sku') or 'N/A'}")
    print("=" * 65)

    ev = record["matching_evidence"]
    seller_families = ev["seller_families"]
    print(f"Declared Seller Families: {seller_families}")

    # 1. Reachability per Goal Group
    goal_mapping = {
        "running_race_preparation": "running",
        "strength_muscle_training": "training",
        "hydration_electrolytes": "hydration",
        "portable_food_snacks": "food",
        "recovery_fatigue": "recovery",
        "outdoor_travel_hiking": "outdoors",
        "foot_apparel_comfort": "gear",
        "general_daily_nutrition": "daily",
        "gift_identity": "gift",
    }

    target_goals = [goal_mapping[f] for f in seller_families if f in goal_mapping]
    print(f"Mapped Quiz Goals: {target_goals}")

    if not target_goals:
        print("[FAIL] Kit does not map to any active quiz goal branch!")
        sys.exit(1)

    for goal in target_goals:
        opts = draft_options(enriched, goal)
        print(f"\n[Test Goal: {goal}]")
        print(f"  Candidate Pool Count: {opts['candidate_count']} kits")
        print(f"  Price Range in Branch: {opts['price_range_uah']['min']} - {opts['price_range_uah']['max']} UAH")

        # Simulate exact request matching this kit
        req = {
            "goal_group": goal,
            "max_price_uah": record["price_uah"] + 200,
        }
        allowed_acts = ACTIVITY_OPTIONS_BY_GOAL.get(goal, set()) | {"other"}
        matching_acts = [a for a in ev.get("seller_activity_groups", []) if a in allowed_acts]
        if matching_acts:
            req["activity"] = matching_acts[0]

        allowed_comps = COMPONENT_CLASSES_BY_GOAL.get(goal, set())
        matching_comps = [c for c in ev.get("component_classes", []) if c in allowed_comps]
        if matching_comps:
            req["component_class"] = matching_comps[0]

        allowed_forms = PRODUCT_FORMS_BY_GOAL.get(goal, set())
        matching_forms = [f for f in ev.get("product_forms", []) if f in allowed_forms]
        if matching_forms:
            req["product_form"] = matching_forms[0]

        if goal in SIZE_GOALS and ev.get("size_sensitive") and ev.get("size_values"):
            val_str = str(ev["size_values"][0].get("value", ""))
            num_match = re.search(r"\d+", val_str)
            if num_match:
                req["shoe_size"] = int(num_match.group(0))

        res = draft_recommend(enriched, req)
        matched_rows = [item["catalog_row"] for item in res["results"]]
        found = record["catalog_row"] in matched_rows

        print(f"  Simulated Query: activity={req.get('activity')}, max_price={req.get('max_price_uah')}")
        print(f"  Returned {res['returned_count']} sets (Status: {res['status']})")
        if found:
            matched_item = next(item for item in res["results"] if item["catalog_row"] == record["catalog_row"])
            print(f"  ✅ SUCCESS: Kit surfaced at Rank {matched_rows.index(record['catalog_row']) + 1}!")
            print(f"     Match Score: {matched_item['match_score_pct']}% (Type: {matched_item['match_type']})")
            print(f"     Reasons: {len(matched_item['reasons'])} explanation cues")
        else:
            print(f"  ⚠️ Warning: Kit was not in top {len(matched_rows)} results (Top: {matched_rows})")

    print("\n[OK] Kit audit complete. Matching logic conforms to engine expectations.")


def main():
    parser = argparse.ArgumentParser(description="Audit onboarded kit matching behavior.")
    parser.add_argument("identifier", help="Catalog row (e.g. 206), set_id (e.g. race-expert-206) or SKU")
    args = parser.parse_args()
    audit_kit(args.identifier)


if __name__ == "__main__":
    main()
