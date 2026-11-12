"""Stress tests for Outdoor, Food & Dehydrated Meals (Problem #5).

Verifies:
1. Taxonomy and metadata for ЇDLO camping meals (RE11494, RE11495, RE88977)
   and meat jerky snacks (RE89418, RE89416, RE89417, RE89413, RE89326).
2. Elimination of non-food leaks (medals, organizers, socks) from food_or_meal forms.
3. Realistic buyer journeys for camping, hiking, and endurance food without empty lists.
4. Robustness against activity variations (hiking, walking, cycling, running, fitness).
"""

import json
import unittest
from pathlib import Path

from draft_matcher import (
    attach_audit_evidence,
    draft_options,
    draft_recommend,
)
from server import AUDIT_PATH, CATALOG_PATH, _load_catalog


class OutdoorFoodStressTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        catalog = _load_catalog(CATALOG_PATH)
        audit = json.loads(Path(AUDIT_PATH).read_text(encoding="utf-8"))
        cls.catalog = attach_audit_evidence(catalog, audit)
        cls.by_sku = {r.get("sku"): r for r in cls.catalog}

    def test_yidlo_sets_classification_and_forms(self):
        yidlo_skus = ["RE11494", "RE11495", "RE88977"]
        for sku in yidlo_skus:
            rec = self.by_sku.get(sku)
            self.assertIsNotNone(rec, f"Missing SKU {sku} in catalog")
            evidence = rec.get("matching_evidence", {})

            # Must have dehydrated_meal in component_classes
            classes = evidence.get("component_classes", [])
            self.assertIn("dehydrated_meal", classes, f"{sku} must have dehydrated_meal class")
            self.assertIn("protein_carbohydrate_food", classes, f"{sku} must have protein_carbohydrate_food class")

            # Must have food_or_meal in product_forms
            forms = evidence.get("product_forms", [])
            self.assertIn("food_or_meal", forms, f"{sku} must have food_or_meal form")

            # Must be available under outdoors and food families
            sellers = set(evidence.get("seller_families", []))
            comps = set(evidence.get("component_families", []))
            self.assertIn("outdoor_travel_hiking", sellers | comps, f"{sku} must be in outdoor_travel_hiking")
            self.assertTrue(
                {"portable_food_snacks", "endurance_energy"} & (sellers | comps),
                f"{sku} must be in food families",
            )

            # Must support outdoor activities
            acts = set(evidence.get("seller_activity_groups", [])) | set(evidence.get("component_activity_groups", []))
            self.assertIn("hiking", acts, f"{sku} must support hiking")

    def test_meat_jerky_sets_classification_and_forms(self):
        jerky_skus = ["RE89418", "RE89416", "RE89417", "RE89413", "RE89326"]
        for sku in jerky_skus:
            rec = self.by_sku.get(sku)
            self.assertIsNotNone(rec, f"Missing SKU {sku} in catalog")
            evidence = rec.get("matching_evidence", {})

            # Must have protein_carbohydrate_food in component_classes
            classes = evidence.get("component_classes", [])
            self.assertIn("protein_carbohydrate_food", classes, f"{sku} must have protein_carbohydrate_food class")

            # Must have food_or_meal in product_forms
            forms = evidence.get("product_forms", [])
            self.assertIn("food_or_meal", forms, f"{sku} must have food_or_meal form")

            # Must be available under both food and outdoors
            sellers = set(evidence.get("seller_families", []))
            comps = set(evidence.get("component_families", []))
            self.assertIn("outdoor_travel_hiking", sellers | comps, f"{sku} must be in outdoor_travel_hiking")
            self.assertTrue(
                {"portable_food_snacks", "endurance_energy"} & (sellers | comps),
                f"{sku} must be in food families",
            )

    def test_non_food_items_never_have_food_or_meal_form(self):
        non_food_skus = [
            "RE89482",  # medal + organizer + socks
            "RE89474",  # medal + organizer + socks
            "RE89460",  # medal + buff + socks
            "RE89485",  # socks + bottle
            "Nabir_1060",  # commemorative medal set
            "Nabir_1061",  # commemorative medal set
            "Nabir_1062",  # commemorative medal set
        ]
        for sku in non_food_skus:
            rec = self.by_sku.get(sku)
            if rec:
                forms = rec.get("matching_evidence", {}).get("product_forms", [])
                self.assertNotIn(
                    "food_or_meal",
                    forms,
                    f"Non-food set {sku} ({rec.get('title')}) must NOT have food_or_meal form",
                )

    def test_outdoors_dehydrated_meal_returns_yidlo_sets(self):
        request = {
            "goal_group": "outdoors",
            "component_class": "dehydrated_meal",
            "locale": "uk",
        }
        resp = draft_recommend(self.catalog, request)
        self.assertIn(resp["status"], ("matched", "general_auto"))
        self.assertGreater(resp["returned_count"], 0)
        returned_skus = {r["sku"] for r in resp["results"]}
        self.assertTrue(
            returned_skus & {"RE11494", "RE11495", "RE88977"},
            f"Expected ЇDLO sets, got {returned_skus}",
        )

    def test_outdoors_food_or_meal_returns_authentic_rations_and_jerky(self):
        request = {
            "goal_group": "outdoors",
            "product_form": "food_or_meal",
            "locale": "uk",
        }
        resp = draft_recommend(self.catalog, request)
        self.assertIn(resp["status"], ("matched", "general_auto"))
        self.assertGreater(resp["returned_count"], 0)
        for r in resp["results"]:
            sku = r["sku"]
            cat_rec = self.by_sku[sku]
            classes = set(cat_rec.get("matching_evidence", {}).get("component_classes", []))
            self.assertTrue(
                classes & {"dehydrated_meal", "protein_carbohydrate_food"},
                f"Result {sku} must be food or dehydrated meal, but had classes {classes}",
            )
            # Ensure no military medal or non-food leaks
            self.assertNotIn("Гвардія", r["title"])
            self.assertNotIn("Озброєні", r["title"])
            self.assertNotIn("медаль", (r.get("composition") or "").lower())

    def test_food_dehydrated_meal_returns_yidlo_sets(self):
        request = {
            "goal_group": "food",
            "component_class": "dehydrated_meal",
            "locale": "uk",
        }
        resp = draft_recommend(self.catalog, request)
        self.assertIn(resp["status"], ("matched", "general_auto"))
        self.assertGreater(resp["returned_count"], 0)
        returned_skus = {r["sku"] for r in resp["results"]}
        self.assertTrue(
            returned_skus & {"RE11494", "RE11495", "RE88977"},
            f"Expected ЇDLO sets in food, got {returned_skus}",
        )

    def test_food_hiking_activity_recommends_camping_meals_and_snacks(self):
        request = {
            "goal_group": "food",
            "activity": "hiking",
            "locale": "uk",
        }
        resp = draft_recommend(self.catalog, request)
        self.assertIn(resp["status"], ("matched", "general_auto"))
        self.assertGreater(resp["returned_count"], 0)
        # Should include nutritious outdoor snacks or meals
        for r in resp["results"]:
            sku = r["sku"]
            cat_rec = self.by_sku[sku]
            classes = set(cat_rec.get("matching_evidence", {}).get("component_classes", []))
            self.assertTrue(
                classes & {"protein_carbohydrate_food", "dehydrated_meal"},
                f"Food recommendation {sku} must contain food items, got {classes}",
            )

    def test_food_bikepacking_cycling_dehydrated_meal(self):
        # Bikepackers often prepare dehydrated rations with boiling water on tours
        request = {
            "goal_group": "food",
            "activity": "cycling",
            "component_class": "dehydrated_meal",
            "locale": "uk",
        }
        resp = draft_recommend(self.catalog, request)
        self.assertIn(resp["status"], ("matched", "general_auto"))
        self.assertGreater(resp["returned_count"], 0)
        returned_skus = {r["sku"] for r in resp["results"]}
        self.assertTrue(returned_skus & {"RE11494", "RE11495", "RE88977"})

    def test_food_fitness_activity_does_not_crash(self):
        # Stress test: activity 'fitness' must be supported and cleanly handled
        request = {
            "goal_group": "food",
            "activity": "fitness",
            "max_price_uah": 1500,
            "locale": "uk",
        }
        resp = draft_recommend(self.catalog, request)
        self.assertIn(resp["status"], ("matched", "general_auto"))
        self.assertGreater(resp["returned_count"], 0)

    def test_multichoice_food_forms_including_bars_and_meals(self):
        request = {
            "goal_group": "food",
            "product_form": ["food_or_meal", "bars"],
            "max_price_uah": 1500,
            "locale": "uk",
        }
        resp = draft_recommend(self.catalog, request)
        self.assertIn(resp["status"], ("matched", "general_auto"))
        self.assertGreater(resp["returned_count"], 0)

    def test_trail_during_training_nutrition(self):
        request = {
            "goal_group": "food",
            "activity": "hiking",
            "product_form": "food_or_meal",
            "use_timing": "during_training",
            "locale": "uk",
        }
        resp = draft_recommend(self.catalog, request)
        self.assertIn(resp["status"], ("matched", "general_auto"))
        self.assertGreater(resp["returned_count"], 0)


if __name__ == "__main__":
    unittest.main()
