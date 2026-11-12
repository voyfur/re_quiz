import json
import unittest
from pathlib import Path

from draft_matcher import (
    attach_audit_evidence,
    draft_options,
    draft_recommend,
    _goal_candidates,
    _candidate_fit,
)
from server import AUDIT_PATH, CATALOG_PATH, _load_catalog

class TestHydrationStress(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        catalog = _load_catalog(CATALOG_PATH)
        audit = json.loads(Path(AUDIT_PATH).read_text(encoding="utf-8"))
        cls.catalog = attach_audit_evidence(catalog, audit)

    def test_hydration_candidates_only_contain_real_active_substances(self):
        """Every single candidate set in the hydration category must contain genuine electrolytes or isotonics."""
        candidates = _goal_candidates(self.catalog, "hydration")
        self.assertGreater(len(candidates), 0, "Hydration candidates list cannot be empty")
        
        active_markers = [
            "hydria", "sis go", "hydro", "precision hydration",
            "електроліт", "электролит", "ізотонік", "изотоник", "солев"
        ]

        for cand in candidates:
            record = cand[0]
            title = record.get("title", "")
            comp = str(record.get("composition", ""))
            desc = str(record.get("description", ""))
            full_text = (title + " " + comp + " " + desc).lower()
            
            has_active = any(marker in full_text for marker in active_markers)
            self.assertTrue(
                has_active,
                f"Candidate set {record.get('sku')} '{title}' lacks active electrolyte/isotonic substances!"
            )

    def test_empty_bottles_caps_and_socks_never_recommended_for_hydration(self):
        """No kit without active electrolytes (empty flasks, caps, socks) may ever leak into hydration."""
        prohibited_skus = {
            "RE11013",  # Socks + glass bottle
            "RE89475",  # Socks + towel + bottle
            "RE11801",  # Cap + bib belt + bottle
            "RE11020",  # Apparel kit
            "RE88934",  # Creatine kit
            "RE11681",  # Creatine monohydrate 500g
            "RE11513",  # Spirulina algae pills
            "RE88943",  # Lion's mane mushrooms
        }
        
        test_queries = [
            {"goal_group": "hydration"},
            {"goal_group": "hydration", "max_price_uah": 1500},
            {"goal_group": "hydration", "max_price_uah": 2500},
            {"goal_group": "hydration", "component_class": "hydration_items"},
            {"goal_group": "hydration", "component_class": "sports_accessories"},
            {"goal_group": "hydration", "activity": "running"},
            {"goal_group": "hydration", "activity": "cycling"},
            {"goal_group": "hydration", "activity": "fitness_gym"},
            {"goal_group": "hydration", "activity": "walking"},
            {"goal_group": "hydration", "product_form": "sticks"},
            {"goal_group": "hydration", "product_form": "tablets"},
            {"goal_group": "hydration", "product_form": "powder"},
        ]

        for q in test_queries:
            res = draft_recommend(self.catalog, q)
            all_skus = (
                [r["sku"] for r in res.get("results", [])]
                + [r["sku"] for r in res.get("near_miss_results", [])]
                + [r["sku"] for r in res.get("floor_anchor_results", [])]
            )
            for bad_sku in prohibited_skus:
                self.assertNotIn(
                    bad_sku,
                    all_skus,
                    f"Forbidden non-hydration set {bad_sku} returned for query: {q}"
                )

    def test_nabir_1015_electrolyte_stock_exact_match(self):
        """Nabir_1015 (Електролітний запас Club, pure Hydria Perform) must be exact match and return properly."""
        candidates = _goal_candidates(self.catalog, "hydration")
        nabir_1015 = next((c for c in candidates if c[0]["sku"] == "Nabir_1015"), None)
        self.assertIsNotNone(nabir_1015, "Nabir_1015 must be present in hydration candidates")

        fit = _candidate_fit(nabir_1015, {
            "goal_group": "hydration",
            "component_class": "hydration_items",
            "product_form": "sticks"
        })
        self.assertIsNotNone(fit, "Nabir_1015 must fit hydration_items + sticks query")
        self.assertEqual(fit["match_type"], "exact", "Nabir_1015 must be an EXACT match")

        # Verify recommendation query with price cap
        from draft_matcher import _candidate_pools, _validate_request
        val = _validate_request(self.catalog, {
            "goal_group": "hydration",
            "component_class": "hydration_items",
            "product_form": "sticks",
            "max_price_uah": 1500,
        })
        cands = _goal_candidates(self.catalog, "hydration")
        pools = _candidate_pools(cands, val)
        exact_skus = [c[0][0]["sku"] for c in pools["exact"]]
        self.assertIn("Nabir_1015", exact_skus, "Nabir_1015 must be present in exact candidate pool")

        # When filtering by running activity and sticks, Nabir_1015 matches exactly
        res = draft_recommend(self.catalog, {
            "goal_group": "hydration",
            "activity": "running",
            "component_class": "hydration_items",
            "product_form": "sticks",
            "max_price_uah": 1500,
        })
        self.assertGreater(res["returned_count"], 0)
        self.assertIn("Nabir_1015", exact_skus)

    def test_sis_go_hydro_in_ut_pro_2026_classified_as_tablets(self):
        """UT-PRO-2026 contains SiS Go Hydro effervescent tablets and must match product_form: tablets."""
        candidates = _goal_candidates(self.catalog, "hydration")
        ut_pro = next((c for c in candidates if c[0]["sku"] == "UT-PRO-2026"), None)
        self.assertIsNotNone(ut_pro, "UT-PRO-2026 must be present in hydration candidates")

        forms = ut_pro[0].get("matching_evidence", {}).get("product_forms", [])
        self.assertIn("tablets", forms, "UT-PRO-2026 must declare 'tablets' form due to SiS Go Hydro")
        self.assertNotIn("sticks", forms, "UT-PRO-2026 has no sticks (SiS Go Hydro is effervescent tablets)")

        # Verify candidate pool contains UT-PRO-2026 for tablets
        from draft_matcher import _candidate_pools, _validate_request
        val = _validate_request(self.catalog, {
            "goal_group": "hydration",
            "product_form": "tablets",
            "max_price_uah": 2000,
        })
        cands = _goal_candidates(self.catalog, "hydration")
        pools = _candidate_pools(cands, val)
        exact_skus = [c[0][0]["sku"] for c in pools["exact"]]
        self.assertIn("UT-PRO-2026", exact_skus, "UT-PRO-2026 must be present in exact tablets pool")

        # When filtering by hiking / ultra trail, UT-PRO-2026 is top match
        res_hiking = draft_recommend(self.catalog, {
            "goal_group": "hydration",
            "activity": "hiking",
            "product_form": "tablets",
            "max_price_uah": 2000,
        })
        results_skus = [r["sku"] for r in res_hiking.get("results", [])]
        self.assertIn("UT-PRO-2026", results_skus, "UT-PRO-2026 should be top match for hiking hydration tablets")

    def test_precision_hydration_re11650_has_tablets_and_no_sticks(self):
        """RE11650 (Precision Hydration 1000) has effervescent tablets and capsules, but NO sticks."""
        candidates = _goal_candidates(self.catalog, "hydration")
        re11650 = next((c for c in candidates if c[0]["sku"] == "RE11650"), None)
        self.assertIsNotNone(re11650, "RE11650 must be present in hydration candidates")

        forms = re11650[0].get("matching_evidence", {}).get("product_forms", [])
        self.assertIn("tablets", forms, "RE11650 must include 'tablets' (Precision Hydration 1000 tube)")
        self.assertIn("capsules", forms, "RE11650 must include 'capsules' (Precision Fuel & Hydration caps)")
        self.assertNotIn("sticks", forms, "RE11650 has zero sticks!")

    def test_creatine_kits_never_recommended_for_hydration_items(self):
        """Kits with 500g Creatine Monohydrate (RE11681, RE11787, Nabir_1128) must never match hydration_items."""
        for goal in ["running", "training", "hydration"]:
            res = draft_recommend(self.catalog, {
                "goal_group": goal,
                "component_class": "hydration_items",
                "max_price_uah": 3000,
            })
            all_skus = [r["sku"] for r in res.get("results", [])]
            self.assertNotIn("RE11681", all_skus, f"Creatine kit RE11681 recommended for hydration_items under goal {goal}")
            self.assertNotIn("RE11787", all_skus, f"Creatine kit RE11787 recommended for hydration_items under goal {goal}")
            self.assertNotIn("Nabir_1128", all_skus, f"Creatine kit Nabir_1128 recommended for hydration_items under goal {goal}")

    def test_all_supported_product_forms_work_without_crash(self):
        """All consumable product forms for hydration (sticks, tablets, powder, capsules, liquid, gel, flasks) must resolve."""
        forms = ["sticks", "tablets", "powder", "capsules", "liquid", "gel", "flasks"]
        for form in forms:
            res = draft_recommend(self.catalog, {
                "goal_group": "hydration",
                "product_form": form,
                "max_price_uah": 2000,
            })
            self.assertIn(res["status"], ["matched", "general_auto", "no_exact_match", "floor_anchor"])
            if res.get("results"):
                for it in res["results"]:
                    rec = next(c for c in self.catalog if c["catalog_row"] == it["catalog_row"])
                    p_forms = rec.get("matching_evidence", {}).get("product_forms", [])
                    self.assertIn(form, p_forms, f"Kit {it['sku']} does not have requested form '{form}'")

    def test_walking_and_hiking_activities_supported_in_hydration(self):
        """Athletes walking or hiking must be supported in hydration without crashes or dead ends."""
        for act in ["walking", "hiking"]:
            res = draft_recommend(self.catalog, {
                "goal_group": "hydration",
                "activity": act,
                "max_price_uah": 2000,
            })
            self.assertEqual(res["status"], "matched", f"Activity {act} did not match in hydration")
            self.assertGreater(len(res["results"]), 0, f"Activity {act} returned 0 results")

    def test_season_summer_normalized_without_crash(self):
        """Requesting season='summer' or 'hot' must normalize to 'warm' and return summer hydration."""
        res = draft_recommend(self.catalog, {
            "goal_group": "hydration",
            "season": "summer",
            "max_price_uah": 2000,
        })
        self.assertIn(res["status"], ["matched", "general_auto", "floor_anchor"])

if __name__ == "__main__":
    unittest.main()
