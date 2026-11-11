import sys
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from server import _load_catalog, CATALOG_PATH, AUDIT_PATH
from draft_matcher import (
    attach_audit_evidence,
    draft_options,
    draft_recommend,
    GOAL_FAMILIES,
    COMPONENT_CLASSES_BY_GOAL,
    ACTIVITY_OPTIONS_BY_GOAL,
    USE_TIMINGS_BY_GOAL,
    USE_PLACES_BY_GOAL,
    USE_SCENARIOS_BY_GOAL,
    PRODUCT_FORMS_BY_GOAL
)

def run_deep_audit():
    catalog = attach_audit_evidence(_load_catalog(CATALOG_PATH), json.load(open(AUDIT_PATH)))
    print(f"Loaded {len(catalog)} catalog records.")

    flaws = []

    # 1. Audit Catalog Misclassifications
    print("\n--- 1. AUDITING CATALOG DATA MISCLASSIFICATIONS ---")
    FOOD_CLASSES = {"protein_carbohydrate_food", "dehydrated_meal"}
    APPAREL_CLASSES = {"apparel_footwear"}

    for r in catalog:
        comp_str = (r.get("composition") or "").lower()
        title = (r.get("title") or "").lower()
        classes = r.get("matching_evidence", {}).get("component_classes", [])
        
        # Check if set has food class but zero food in composition
        has_food_class = any(c in FOOD_CLASSES for c in classes)
        has_actual_food = any(w in comp_str or w in title for w in [
            "гель", "батончик", "суп", "каша", "пюре", "їжа", "батон", "снек", "вафл",
            "протеїн", "вуглевод", "sis go", "powerbar", "flapjack", "чипс", "арахіс", "мармелад"
        ])
        
        # Check if set is purely clothing/souvenirs/club but tagged with food
        if has_food_class and not has_actual_food:
            flaws.append({
                "type": "CATALOG_FALSE_FOOD_TAG",
                "row": r["catalog_row"],
                "sku": r.get("sku"),
                "title": r.get("title"),
                "composition": r.get("composition"),
                "classes": classes
            })
            print(f"⚠️ [Catalog Bug] Row {r['catalog_row']} ({r.get('sku')}) '{r.get('title')}' has FOOD class but composition is: '{r.get('composition')}'")

    # 2. Simulate User Flows across all Goals
    print("\n--- 2. SIMULATING INTERACTIVE QUESTION FLOWS ---")
    
    # We will simulate depth-first traversals
    def explore_flow(goal, answers, depth=0):
        if depth > 10:
            flaws.append({"type": "EXCESSIVE_DEPTH", "goal": goal, "answers": answers, "depth": depth})
            return

        opts = draft_options(catalog, goal, answers)
        plan = opts.get("question_plan", [])
        
        if not plan:
            # Reached end of questions, test recommendation
            res = draft_recommend(catalog, {"goal_group": goal, **answers})
            
            # Check for Semantic Mismatches in returned results
            user_class = answers.get("component_class")
            if user_class and res.get("results"):
                for rec in res["results"]:
                    # If user wanted food, did rec have clothes/no food?
                    rec_classes = rec.get("component_classes") or []
                    # Let's check matching evidence of the record
                    matching_rec = next((x for x in catalog if x["catalog_row"] == rec["catalog_row"]), None)
                    me_classes = matching_rec.get("matching_evidence", {}).get("component_classes", []) if matching_rec else []
                    
                    if user_class == "protein_carbohydrate_food":
                        if "protein_carbohydrate_food" not in me_classes:
                            flaws.append({
                                "type": "RECOMMENDATION_MISMATCH",
                                "goal": goal,
                                "answers": answers,
                                "returned_title": rec["title"],
                                "returned_row": rec["catalog_row"],
                                "reason": "User wanted protein/food, but recommended set does not contain food!"
                            })
                    elif user_class == "apparel_footwear":
                        if "apparel_footwear" not in me_classes:
                            flaws.append({
                                "type": "RECOMMENDATION_MISMATCH",
                                "goal": goal,
                                "answers": answers,
                                "returned_title": rec["title"],
                                "returned_row": rec["catalog_row"],
                                "reason": "User wanted apparel, but recommended set does not contain apparel!"
                            })
            return

        # Check the current questions in plan
        q_ids = [q["id"] for q in plan]

        # Check Flaw: Asking shoe_size when user chose food/vitamins/hydration
        if "shoe_size" in q_ids:
            u_class = answers.get("component_class")
            if u_class in {"protein_carbohydrate_food", "supplements_vitamins_minerals", "hydration_items", "creatine_preworkout", "dehydrated_meal"}:
                flaws.append({
                    "type": "STUPID_QUESTION_SHOE_SIZE_FOR_NUTRITION",
                    "goal": goal,
                    "answers": answers,
                    "detail": f"Asked shoe_size when component_class is {u_class}"
                })

        # Check Flaw: Asking activity for sleep/recovery or daily
        if "activity" in q_ids and goal in {"recovery", "daily"}:
            flaws.append({
                "type": "AWKWARD_QUESTION_ACTIVITY_FOR_SLEEP_OR_DAILY",
                "goal": goal,
                "answers": answers,
                "detail": f"Asked sport activity for goal '{goal}'"
            })

        # Check Flaw: Asking use_place when use_timing is evening_or_bedtime
        if "use_place" in q_ids and answers.get("use_timing") == "evening_or_bedtime":
            flaws.append({
                "type": "CONTRADICTORY_QUESTION_PLACE_FOR_BEDTIME",
                "goal": goal,
                "answers": answers,
                "detail": "Asked where (work/travel) when user already said evening/bedtime"
            })

        # Check Flaw: Excessive total plan length
        if len(answers) + len(plan) > 5:
            flaws.append({
                "type": "EXCESSIVE_QUESTION_COUNT",
                "goal": goal,
                "answers": answers,
                "total_questions": len(answers) + len(plan),
                "plan": [q["id"] for q in plan]
            })

        # To avoid combinatorial explosion in test, sample key paths
        first_q = plan[0]
        q_id = first_q["id"]
        if first_q["type"] == "number":
            # Test with typical number
            val = 42 if q_id == "shoe_size" else 1500
            explore_flow(goal, {**answers, q_id: val}, depth + 1)
        else:
            options_to_test = first_q.get("options", [])[:3] # Sample first 3 options
            for opt in options_to_test:
                explore_flow(goal, {**answers, q_id: opt}, depth + 1)

    print("Traversing question graphs across all 9 goal categories...")
    for goal in GOAL_FAMILIES.keys():
        explore_flow(goal, {})

    print(f"\n==========================================")
    print(f"AUDIT COMPLETE: Found {len(flaws)} logic flaw occurrences.")
    print(f"==========================================")

    # Group by type
    by_type = {}
    for f in flaws:
        by_type.setdefault(f["type"], []).append(f)

    for f_type, items in by_type.items():
        print(f"\n[{f_type}]: {len(items)} instances")
        # Print sample
        sample = items[0]
        print(f"  Sample: {sample}")

    return flaws

if __name__ == "__main__":
    run_deep_audit()
