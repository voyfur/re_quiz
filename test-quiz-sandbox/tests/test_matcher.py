import unittest

from catalog_builder import parse_analysis
from matcher import MatchError, QUIZ_GOAL_GROUPS, goal_group_for_purpose, recommend
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
ANALYSIS_PATH = PROJECT_ROOT / "wiki" / "projects" / "race-expert-need-sets-206-analysis.md"


class MatcherTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.catalog = parse_analysis(ANALYSIS_PATH.read_text(encoding="utf-8"))

    def test_returns_requested_number_of_distinct_alternatives(self):
        for limit in (1, 2, 3):
            response = recommend(self.catalog, {"purpose": "cold_weather_comfort", "result_count": limit})
            self.assertEqual(len(response["results"]), limit)
            self.assertEqual(len({item["set_id"] for item in response["results"]}), limit)
            self.assertEqual(response["status"], "matched")

    def test_consumer_goal_group_maps_to_catalog_purpose_tags(self):
        response = recommend(self.catalog, {"goal_group": "running", "result_count": 3})
        self.assertTrue(response["results"])
        for item in response["results"]:
            record = next(row for row in self.catalog if row["set_id"] == item["set_id"])
            self.assertTrue(any(goal_group_for_purpose(tag) == "running" for tag in record["tags"].get("purpose", [])))

    def test_consumer_goal_groups_do_not_return_unqualified_audience_sets(self):
        restricted = {"children", "children_3_plus", "pregnant_women", "women_planning_pregnancy", "men", "men_50_plus", "women"}
        excluded_ids = {
            row["set_id"] for row in self.catalog
            if restricted.intersection(row.get("tags", {}).get("audience", []))
        }
        for group in QUIZ_GOAL_GROUPS:
            response = recommend(self.catalog, {"goal_group": group, "result_count": 3})
            self.assertTrue(excluded_ids.isdisjoint(item["set_id"] for item in response["results"]))

    def test_rejects_unknown_consumer_goal_group(self):
        with self.assertRaises(MatchError):
            recommend(self.catalog, {"goal_group": "choose_exact_set"})

    def test_applies_full_set_price_ceiling_inclusively(self):
        request = {"purpose": "gym_training_prep", "result_count": 3, "max_price_uah": 1499}
        under = recommend(self.catalog, request)
        self.assertEqual(under["results"], [])
        self.assertEqual(under["status"], "no_match")

        request["max_price_uah"] = 1500
        at_limit = recommend(self.catalog, request)
        self.assertEqual([item["catalog_row"] for item in at_limit["results"]], [206])

    def test_shoe_size_uses_recorded_inclusive_size_range(self):
        response = recommend(
            self.catalog,
            {"purpose": "cold_weather_comfort", "shoe_size": 42, "result_count": 3},
        )
        self.assertEqual([item["catalog_row"] for item in response["results"]], [2])
        self.assertEqual(response["requested_count"], 3)
        self.assertEqual(response["returned_count"], 1)

        next_size = recommend(
            self.catalog,
            {"purpose": "cold_weather_comfort", "shoe_size": 43, "result_count": 3},
        )
        self.assertEqual([item["catalog_row"] for item in next_size["results"]], [1])

    def test_missing_shoe_size_range_is_reported_as_unknown(self):
        catalog = [{
            "set_id": "untagged-size", "catalog_row": 10, "sku": "SIZE-UNKNOWN",
            "title": "No size tag", "source_url": "https://example.test/size",
            "price_uah": 500, "price_snapshot_date": "2026-11-06", "composition": "",
            "tags": {"purpose": ["running_gear"]},
        }]
        response = recommend(catalog, {"purpose": "running_gear", "shoe_size": 42})
        self.assertEqual(response["returned_count"], 1)
        self.assertEqual(response["results"][0]["shoe_size_status"], "unknown")

    def test_known_caffeine_amount_is_explained_per_set(self):
        response = recommend(
            self.catalog,
            {"purpose": "gym_training_prep", "result_count": 1},
        )
        item = response["results"][0]
        self.assertEqual(item["catalog_row"], 206)
        self.assertEqual(item["caffeine_per_set"], ["400_mg"])
        self.assertTrue(any("400_mg" in note for note in item["data_notes"]))

    def test_ukrainian_backend_explanations_are_localized(self):
        response = recommend(
            self.catalog,
            {"purpose": "cold_weather_comfort", "locale": "uk", "result_count": 1},
        )
        item = response["results"][0]
        self.assertIn("Знайдено тестових варіантів: 1", response["message"])
        self.assertIn("Тег призначення збігається", item["reasons"][0])
        self.assertTrue(any("Кофеїн не перевірений" in note for note in item["data_notes"]))

    def test_strict_caffeine_avoidance_fails_closed_on_unknown_or_present(self):
        response = recommend(
            self.catalog,
            {"purpose": "cold_weather_comfort", "caffeine_mode": "avoid", "result_count": 3},
        )
        self.assertEqual(response["results"], [])
        self.assertEqual(response["status"], "insufficient_data")
        self.assertIn("подтверждённым отсутствием кофеина", response["message"].lower())

    def test_results_never_describe_missing_caffeine_tag_as_absent(self):
        response = recommend(self.catalog, {"purpose": "cold_weather_comfort", "result_count": 1})
        states = [item["caffeine_status"] for item in response["results"]]
        self.assertIn("unknown", states)
        self.assertNotIn("confirmed_absent", states)
        self.assertEqual(response["results"][0]["matched_tags"], {"purpose": ["cold_weather_comfort"]})

    def test_general_sport_sets_rank_below_exact_matches(self):
        catalog = [
            {
                "set_id": "set-exact", "catalog_row": 2, "sku": "EXACT", "title": "Exact sport",
                "source_url": "https://example.test/exact", "price_uah": 200,
                "price_snapshot_date": "2026-11-06", "composition": "", "tags": {
                    "purpose": ["running_gear"], "sport": ["running"],
                },
            },
            {
                "set_id": "set-general", "catalog_row": 1, "sku": "GENERAL", "title": "General set",
                "source_url": "https://example.test/general", "price_uah": 100,
                "price_snapshot_date": "2026-11-06", "composition": "", "tags": {
                    "purpose": ["running_gear"], "sport": ["not_sport_specific"],
                },
            },
            {
                "set_id": "set-other", "catalog_row": 3, "sku": "OTHER", "title": "Other sport",
                "source_url": "https://example.test/other", "price_uah": 50,
                "price_snapshot_date": "2026-11-06", "composition": "", "tags": {
                    "purpose": ["running_gear"], "sport": ["cycling"],
                },
            },
        ]
        response = recommend(catalog, {"purpose": "running_gear", "sport": "running", "result_count": 3})
        self.assertEqual([item["set_id"] for item in response["results"]], ["set-exact", "set-general"])
        self.assertEqual(response["results"][0]["matched_tags"]["sport"], ["running"])
        self.assertNotIn("sport", response["results"][1]["matched_tags"])

    def test_form_and_race_format_are_catalog_backed_hard_filters(self):
        form_match = recommend(
            self.catalog,
            {"purpose": "portable_snack", "form": "bars", "result_count": 3},
        )
        self.assertEqual([item["catalog_row"] for item in form_match["results"]], [8])

        race_match = recommend(
            self.catalog,
            {"purpose": "running_preparation", "race_format": "marathon", "result_count": 3},
        )
        self.assertEqual([item["catalog_row"] for item in race_match["results"]], [55])

    def test_in_stock_only_uses_explicit_stock_tags(self):
        response = recommend(self.catalog, {"purpose": "cold_weather_comfort", "in_stock_only": True, "result_count": 3})
        self.assertTrue(response["results"])
        self.assertTrue(all(item["availability"] == "in_stock" for item in response["results"]))

    def test_returns_no_match_without_filling_with_unrelated_sets(self):
        response = recommend(
            self.catalog,
            {"purpose": "cold_weather_comfort", "max_price_uah": 1, "result_count": 3},
        )
        self.assertEqual(response["status"], "no_match")
        self.assertEqual(response["results"], [])

    def test_rejects_unsupported_safety_filters(self):
        for field in (
            "age", "allergy", "allergens", "buyer_weight", "distance_km", "interactions",
            "pregnancy", "medications", "duration", "period",
        ):
            with self.subTest(field=field):
                value = "3_months" if field == "duration" else "test"
                with self.assertRaises(MatchError):
                    recommend(self.catalog, {"purpose": "cold_weather_comfort", field: value, "result_count": 1})

    def test_rejects_invalid_result_count_and_negative_budget(self):
        with self.assertRaises(MatchError):
            recommend(self.catalog, {"purpose": "cold_weather_comfort", "result_count": 4})
        with self.assertRaises(MatchError):
            recommend(self.catalog, {"purpose": "cold_weather_comfort", "max_price_uah": -1})
        with self.assertRaises(MatchError):
            recommend(self.catalog, {"purpose": "cold_weather_comfort", "shoe_size": 0})

    def test_rejects_a_purpose_that_is_not_a_catalog_option(self):
        with self.assertRaises(MatchError):
            recommend(self.catalog, {"purpose": "made_up_purpose"})


if __name__ == "__main__":
    unittest.main()
