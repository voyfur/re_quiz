import json
import unittest
from pathlib import Path

from draft_matcher import attach_audit_evidence, draft_options, draft_recommend
from server import AUDIT_PATH, CATALOG_PATH, _load_catalog

class TestLogicGuardrails(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        catalog = _load_catalog(CATALOG_PATH)
        audit = json.loads(Path(AUDIT_PATH).read_text(encoding="utf-8"))
        cls.catalog = attach_audit_evidence(catalog, audit)

    def test_shoe_size_never_asked_for_nutrition_or_vitamins(self):
        nutrition_classes = {
            "protein_carbohydrate_food",
            "supplements_vitamins_minerals",
            "hydration_items",
            "creatine_preworkout",
            "dehydrated_meal",
        }
        from draft_matcher import COMPONENT_CLASSES_BY_GOAL
        for goal in ["running", "training", "hydration", "food", "recovery", "outdoors", "daily", "gift"]:
            valid_classes = COMPONENT_CLASSES_BY_GOAL.get(goal, set()) & nutrition_classes
            for comp_class in valid_classes:
                plan = draft_options(self.catalog, goal, {"component_class": comp_class})["question_plan"]
                q_ids = [q["id"] for q in plan]
                self.assertNotIn(
                    "shoe_size",
                    q_ids,
                    f"Shoe size was inappropriately asked for goal='{goal}' and component_class='{comp_class}'!"
                )

    def test_place_never_asked_for_evening_or_bedtime(self):
        plan = draft_options(
            self.catalog,
            "recovery",
            {"component_class": "supplements_vitamins_minerals", "use_timing": "evening_or_bedtime"}
        )["question_plan"]
        q_ids = [q["id"] for q in plan]
        self.assertNotIn("use_place", q_ids, "Place was asked for evening_or_bedtime!")

    def test_activity_never_asked_for_recovery_or_daily(self):
        for goal in ["recovery", "daily"]:
            plan = draft_options(self.catalog, goal, {})["question_plan"]
            q_ids = [q["id"] for q in plan]
            self.assertNotIn("activity", q_ids, f"Sport activity asked for goal='{goal}'!")

    def test_nutrition_never_recommends_apparel(self):
        res = draft_recommend(self.catalog, {
            "goal_group": "running",
            "component_class": "protein_carbohydrate_food",
            "use_scenario": "training",
            "max_price_uah": 1500,
        })
        self.assertGreater(res["returned_count"], 0)
        for item in res["results"]:
            matching_rec = next((x for x in self.catalog if x["catalog_row"] == item["catalog_row"]), None)
            classes = matching_rec.get("matching_evidence", {}).get("component_classes", [])
            self.assertIn("protein_carbohydrate_food", classes, f"Non-food item recommended: {item['title']}")
            self.assertNotEqual(item["catalog_row"], 100, "Gift apparel kit 100 recommended for food request!")

    def test_maximum_question_depth_capped_at_four(self):
        for goal in ["running", "training", "hydration", "food", "recovery", "outdoors", "gear", "daily", "gift"]:
            plan = draft_options(self.catalog, goal, {})["question_plan"]
            # After answering goal + 2 followups, remaining should only be budget
            if plan:
                first_q = plan[0]
                if first_q["type"] != "number" and first_q.get("options"):
                    opt1 = first_q["options"][0]
                    sub_plan = draft_options(self.catalog, goal, {first_q["id"]: opt1})["question_plan"]
                    if sub_plan:
                        second_q = sub_plan[0]
                        if second_q["type"] != "number" and second_q.get("options"):
                            opt2 = second_q["options"][0]
                            final_plan = draft_options(self.catalog, goal, {first_q["id"]: opt1, second_q["id"]: opt2})["question_plan"]
                            # Must be only max_price_uah
                            final_ids = [q["id"] for q in final_plan]
                            self.assertTrue(
                                final_ids == ["max_price_uah"] or final_ids == [],
                                f"Question plan too long for goal='{goal}': {final_ids}"
                            )

    def test_recovery_never_recommends_creatine_or_gear(self):
        res = draft_recommend(self.catalog, {
            "goal_group": "recovery",
            "max_price_uah": 800,
        })
        all_skus = [r["sku"] for r in res.get("results", [])] + \
                   [r["sku"] for r in res.get("near_miss_results", [])] + \
                   [r["sku"] for r in res.get("floor_anchor_results", [])]
        self.assertNotIn("RE11680", all_skus, "Row 33 (Creatine) recommended for recovery!")
        self.assertNotIn("RE11020", all_skus, "Gear kit recommended for recovery!")

    def test_running_nutrition_never_recommends_gear_kit_197(self):
        res = draft_recommend(self.catalog, {
            "goal_group": "running",
            "component_class": "protein_carbohydrate_food",
            "use_scenario": "everyday",
            "max_price_uah": 1300,
        })
        all_skus = [r["sku"] for r in res.get("results", [])]
        self.assertNotIn("RE11020", all_skus, "Apparel kit RE11020 recommended for sports nutrition!")

    def test_hydration_excludes_empty_bottles_and_socks(self):
        res = draft_recommend(self.catalog, {"goal_group": "hydration", "max_price_uah": 2000})
        all_skus = [r["sku"] for r in res.get("results", [])]
        self.assertNotIn("RE89475", all_skus, "Empty bottle + socks kit RE89475 recommended for hydration!")
        self.assertNotIn("RE11801", all_skus, "Cap + belt + bottle kit RE11801 recommended for hydration!")

    def test_gear_never_recommends_creatine_monohydrate(self):
        res = draft_recommend(self.catalog, {"goal_group": "gear", "max_price_uah": 2500})
        all_skus = [r["sku"] for r in res.get("results", [])]
        self.assertNotIn("RE11522", all_skus, "Creatine kit RE11522 recommended for gear!")
        self.assertNotIn("RE89488", all_skus, "Creatine kit RE89488 recommended for gear!")
        self.assertNotIn("RE11681", all_skus, "Creatine kit RE11681 recommended for gear!")

    def test_nabir_1015_matches_hydration_items(self):
        from draft_matcher import _candidate_fit, _goal_candidates
        candidates = _goal_candidates(self.catalog, "hydration")
        nabir_1015 = next((c for c in candidates if c[0]["sku"] == "Nabir_1015"), None)
        self.assertIsNotNone(nabir_1015, "Nabir_1015 missing from hydration candidates")
        fit = _candidate_fit(nabir_1015, {"goal_group": "hydration", "component_class": "hydration_items"})
        self.assertEqual(fit["match_type"], "exact", "Nabir_1015 should be an exact match for hydration_items")

    def test_accessories_never_ask_product_form(self):
        plan = draft_options(self.catalog, "outdoors", {"component_class": "sports_accessories"})["question_plan"]
        question_ids = [q["id"] for q in plan]
        self.assertNotIn("product_form", question_ids, "product_form should never be asked for sports accessories!")

if __name__ == "__main__":
    unittest.main()
