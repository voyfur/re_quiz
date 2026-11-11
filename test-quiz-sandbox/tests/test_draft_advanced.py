import json
import unittest
from pathlib import Path

from draft_matcher import (
    DraftMatchError,
    attach_audit_evidence,
    draft_options,
    draft_recommend,
)
from server import AUDIT_PATH, CATALOG_PATH, _load_catalog


class DraftAdvancedFeaturesTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        catalog = _load_catalog(CATALOG_PATH)
        audit = json.loads(Path(AUDIT_PATH).read_text(encoding="utf-8"))
        cls.catalog = attach_audit_evidence(catalog, audit)

    def test_multi_choice_preference_matches_any_valid_signal(self):
        # Multi-choice for forms: bars OR gel
        request = {
            "goal_group": "running",
            "component_class": "protein_carbohydrate_food",
            "product_form": ["bars", "gel"],
            "max_price_uah": 2000,
        }
        response = draft_recommend(self.catalog, request)
        self.assertIn(response["status"], ("matched", "general_auto"))
        self.assertGreater(response["returned_count"], 0)
        # Every matched item must contain either bars or gel or be unknown
        for item in response["results"]:
            forms = item.get("relaxed_preference_values", {}).get("product_form")
            # Should not be in relaxed
            self.assertIsNone(forms)

    def test_multi_choice_validation_rejects_unsupported_item(self):
        request = {
            "goal_group": "running",
            "product_form": ["bars", "invalid_space_food"],
        }
        with self.assertRaises(DraftMatchError) as ctx:
            draft_recommend(self.catalog, request)
        self.assertIn("invalid_space_food", str(ctx.exception))

    def test_match_score_pct_is_calculated_and_scaled(self):
        request = {
            "goal_group": "running",
            "max_price_uah": 1500,
        }
        response = draft_recommend(self.catalog, request)
        self.assertGreater(response["returned_count"], 0)
        for item in response["results"]:
            self.assertIn("match_score_pct", item)
            self.assertIn("score_breakdown", item)
            score = item["match_score_pct"]
            self.assertGreaterEqual(score, 60)
            self.assertLessEqual(score, 99)
            breakdown = item["score_breakdown"]
            self.assertIn("evidence", breakdown)
            self.assertIn("preferences", breakdown)
            self.assertIn("constraints", breakdown)

    def test_budget_near_miss_suggests_alternatives_when_budget_is_tight(self):
        # A budget of 1200 UAH where sets at 1345 and 1500 exist but none <= 1200
        request = {
            "goal_group": "running",
            "component_class": "protein_carbohydrate_food",
            "use_scenario": "event_preparation",
            "use_timing": "during_training",
            "max_price_uah": 1200,
        }
        response = draft_recommend(self.catalog, request)
        # Main results should be 0 due to 1200 UAH budget
        self.assertEqual(len(response["results"]), 0)
        # But near_miss_results should catch compatible sets slightly exceeding 1200 UAH (e.g. 1345 UAH)
        self.assertGreater(response["near_miss_count"], 0)
        near_miss = response["near_miss_results"][0]
        self.assertEqual(near_miss["match_type"], "near_miss")
        self.assertGreater(near_miss["price_uah"], 1200)
        self.assertGreater(near_miss["price_over_budget_uah"], 0)
        self.assertIn("Превышает выбранный бюджет", " ".join(near_miss["reasons"]))

    def test_dynamic_price_hint_reflects_remaining_candidates(self):
        options = draft_options(
            self.catalog,
            "running",
            {"component_class": "protein_carbohydrate_food", "use_scenario": "event_preparation"},
        )
        self.assertIsNotNone(options["price_range_uah"])
        # Running event prep nutrition sets start from >= 1209 UAH
        self.assertGreaterEqual(options["price_range_uah"]["min"], 1209)
        budget_q = next((q for q in options["question_plan"] if q["id"] == "max_price_uah"), None)
        self.assertIsNotNone(budget_q)
        self.assertEqual(budget_q["dynamic_min"], options["price_range_uah"]["min"])
        self.assertEqual(budget_q["dynamic_max"], options["price_range_uah"]["max"])

    def test_floor_price_anchor_prevents_empty_results_when_budget_too_low(self):
        # Extremely low budget (800 UAH) where no sets exist under 1200 UAH
        request = {
            "goal_group": "running",
            "component_class": "protein_carbohydrate_food",
            "max_price_uah": 800,
        }
        response = draft_recommend(self.catalog, request)
        self.assertEqual(len(response["results"]), 0)
        self.assertEqual(len(response["near_miss_results"]), 0)
        self.assertEqual(response["status"], "floor_anchor")
        self.assertGreater(response["floor_anchor_count"], 0)
        anchor = response["floor_anchor_results"][0]
        self.assertEqual(anchor["match_type"], "floor_anchor")
        self.assertGreaterEqual(anchor["price_uah"], 1209)
        self.assertEqual(anchor["price_over_budget_uah"], anchor["price_uah"] - 800)
        self.assertIn("Минимальный базовый набор", " ".join(anchor["reasons"]))
        self.assertIn(str(response["floor_price_uah"]), response["message"])

    def test_stock_awareness_prioritizes_in_stock_candidates_over_out_of_stock(self):
        request = {
            "goal_group": "running",
            "max_price_uah": 2000,
        }
        # First get default results without stock restriction
        default_res = draft_recommend(self.catalog, request)
        self.assertGreaterEqual(len(default_res["results"]), 2)
        top_sku = default_res["results"][0]["sku"]
        second_sku = default_res["results"][1]["sku"]

        # Now simulate that the top SKU is OUT OF STOCK, but the second SKU is IN STOCK
        mock_stock_map = {
            top_sku: {
                "sku": top_sku,
                "in_stock": False,
                "quantity": 0,
                "status": 1,
                "live_price_uah": default_res["results"][0]["price_uah"],
                "stock_status_text_uk": "Немає в наявності",
                "stock_status_text_ru": "Нет в наличии",
                "is_live_check": True,
            },
            second_sku: {
                "sku": second_sku,
                "in_stock": True,
                "quantity": 10,
                "status": 1,
                "live_price_uah": default_res["results"][1]["price_uah"],
                "stock_status_text_uk": "В наявності",
                "stock_status_text_ru": "В наличии",
                "is_live_check": True,
            },
        }

        # Run with stock_map
        stock_res = draft_recommend(self.catalog, request, stock_map=mock_stock_map)
        self.assertTrue(stock_res["stock_verified"])
        # The in-stock candidate must now be ranked #1
        self.assertEqual(stock_res["results"][0]["sku"], second_sku)
        self.assertTrue(stock_res["results"][0]["stock_info"]["in_stock"])
        self.assertIn("Наличие подтверждено", " ".join(stock_res["results"][0]["data_notes"]))

    def test_stock_live_price_updates_and_records_note(self):
        request = {
            "goal_group": "running",
            "max_price_uah": 2000,
        }
        default_res = draft_recommend(self.catalog, request)
        top_sku = default_res["results"][0]["sku"]
        old_price = default_res["results"][0]["price_uah"]
        new_price = old_price + 150.0

        mock_stock_map = {
            top_sku: {
                "sku": top_sku,
                "in_stock": True,
                "quantity": 25,
                "status": 1,
                "live_price_uah": new_price,
                "stock_status_text_uk": "В наявності",
                "stock_status_text_ru": "В наличии",
                "is_live_check": True,
            }
        }
        stock_res = draft_recommend(self.catalog, request, stock_map=mock_stock_map)
        top_item = stock_res["results"][0]
        self.assertEqual(top_item["price_uah"], new_price)
        self.assertEqual(top_item["catalog_price_uah"], old_price)
        self.assertIn("Актуальная цена на сайте", " ".join(top_item["data_notes"]))


if __name__ == "__main__":
    unittest.main()
