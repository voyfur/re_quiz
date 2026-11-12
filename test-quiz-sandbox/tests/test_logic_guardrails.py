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

    def test_heavy_creatine_and_preworkout_completely_isolated_from_non_strength_goals(self):
        """Verify that heavy sports pharmacology (creatine, pre-workout stimulants) NEVER leaks into non-training goals."""
        from draft_matcher import HEAVY_CREATINE_PREWORKOUT_SKUS, _goal_candidates

        non_strength_goals = ["running", "recovery", "gear", "daily", "gift", "hydration", "food", "outdoors"]
        budgets = [600, 1000, 1500, 2500, 5000]

        for goal in non_strength_goals:
            # 1. Candidate pool isolation check
            candidates = _goal_candidates(self.catalog, goal)
            candidate_skus = {c[0]["sku"] for c in candidates}
            leaked_cands = candidate_skus & HEAVY_CREATINE_PREWORKOUT_SKUS
            self.assertEqual(
                len(leaked_cands), 0,
                f"Heavy nutrition candidates leaked into goal='{goal}': {leaked_cands}"
            )

            # Ensure no candidate in non-training goals carries creatine_preworkout class
            for c in candidates:
                classes = set(c[0].get("matching_evidence", {}).get("component_classes", []))
                self.assertNotIn(
                    "creatine_preworkout", classes,
                    f"Candidate {c[0]['sku']} in goal='{goal}' has creatine_preworkout class!"
                )

            # 2. Recommendation stress testing across budgets
            for b in budgets:
                res = draft_recommend(self.catalog, {"goal_group": goal, "max_price_uah": b})
                all_skus = {r["sku"] for r in res.get("results", [])} | \
                           {r["sku"] for r in res.get("near_miss_results", [])} | \
                           {r["sku"] for r in res.get("floor_anchor_results", [])}
                leaked_recs = all_skus & HEAVY_CREATINE_PREWORKOUT_SKUS
                self.assertEqual(
                    len(leaked_recs), 0,
                    f"Heavy nutrition recommended in goal='{goal}' at budget {b}: {leaked_recs}"
                )

    def test_target_kits_creatine_integrity_and_isolation(self):
        """Stress-test target kits RE11632, RE11663, RE11665, RE11660, RE11522, RE89488, RE11681."""
        cat_map = {x["sku"]: x for x in self.catalog}

        # 1. Non-creatine sets: MUST NOT have creatine_preworkout
        non_creatine_targets = ["RE11632", "RE11663", "RE11665"]
        for sku in non_creatine_targets:
            item = cat_map[sku]
            classes = set(item.get("matching_evidence", {}).get("component_classes", []))
            self.assertNotIn(
                "creatine_preworkout", classes,
                f"Target kit {sku} incorrectly has creatine_preworkout class!"
            )

        # 2. Real creatine sets: MUST have creatine_preworkout
        creatine_targets = ["RE11660", "RE11522", "RE89488", "RE11681"]
        for sku in creatine_targets:
            item = cat_map[sku]
            classes = set(item.get("matching_evidence", {}).get("component_classes", []))
            self.assertIn(
                "creatine_preworkout", classes,
                f"Target creatine kit {sku} is missing creatine_preworkout class!"
            )

        # 3. RE11660 (Nutriversum Creatine 300g) MUST NEVER leak into running (marathon without strength)
        running_res = draft_recommend(self.catalog, {
            "goal_group": "running",
            "component_class": "protein_carbohydrate_food",
            "race_format": "marathon",
            "max_price_uah": 2000,
        })
        all_running = {r["sku"] for r in running_res.get("results", [])} | \
                      {r["sku"] for r in running_res.get("near_miss_results", [])}
        self.assertNotIn("RE11660", all_running, "RE11660 leaked into running marathon request!")

        # 4. RE11522, RE89488, RE11681 MUST NEVER leak into gear, recovery, daily, running, or gift
        for non_goal in ["gear", "recovery", "daily", "running", "gift"]:
            res = draft_recommend(self.catalog, {"goal_group": non_goal, "max_price_uah": 3500})
            all_recs = {r["sku"] for r in res.get("results", [])} | \
                       {r["sku"] for r in res.get("near_miss_results", [])}
            for sku in ["RE11522", "RE89488", "RE11681"]:
                self.assertNotIn(sku, all_recs, f"Creatine kit {sku} leaked into goal='{non_goal}'!")

    def test_false_creatine_tags_completely_purged(self):
        """Verify that all 11 kits without creatine/preworkout are purged of the tag."""
        from draft_matcher import FALSE_CREATINE_TAG_SKUS
        cat_map = {x["sku"]: x for x in self.catalog}
        for sku in FALSE_CREATINE_TAG_SKUS:
            item = cat_map.get(sku)
            self.assertIsNotNone(item, f"Kit {sku} not found in catalog")
            classes = set(item.get("matching_evidence", {}).get("component_classes", []))
            self.assertNotIn(
                "creatine_preworkout", classes,
                f"False creatine kit {sku} still contains creatine_preworkout class!"
            )

    def test_real_creatine_kits_fully_findable_in_training(self):
        """Verify that all 24 heavy kits have creatine_preworkout and are properly matched in training."""
        from draft_matcher import HEAVY_CREATINE_PREWORKOUT_SKUS
        cat_map = {x["sku"]: x for x in self.catalog}

        for sku in HEAVY_CREATINE_PREWORKOUT_SKUS:
            item = cat_map[sku]
            classes = set(item.get("matching_evidence", {}).get("component_classes", []))
            self.assertIn(
                "creatine_preworkout", classes,
                f"Heavy nutrition kit {sku} missing creatine_preworkout class!"
            )

        # Budget 800 UAH must return RE11680 (759 UAH Pure Creatine Monohydrate 300g)
        res_800 = draft_recommend(self.catalog, {
            "goal_group": "training",
            "component_class": "creatine_preworkout",
            "max_price_uah": 800,
        })
        self.assertGreater(res_800.get("returned_count", 0), 0)
        res_800_skus = [r["sku"] for r in res_800.get("results", [])]
        self.assertIn("RE11680", res_800_skus, "RE11680 (759 UAH creatine) not found at budget 800 UAH!")

        # Budget 1500 UAH returns 100% genuine creatine kits, no false items
        res_1500 = draft_recommend(self.catalog, {
            "goal_group": "training",
            "component_class": "creatine_preworkout",
            "max_price_uah": 1500,
        })
        self.assertGreater(res_1500.get("returned_count", 0), 0)
        for r in res_1500.get("results", []):
            self.assertIn(
                r["sku"], HEAVY_CREATINE_PREWORKOUT_SKUS,
                f"Non-creatine kit {r['sku']} recommended for creatine_preworkout!"
            )

    def test_product_form_never_asked_for_non_consumables_across_all_goals(self):
        """Guardrail: product_form must NEVER be asked when buyer selects accessories or apparel in ANY branch."""
        from draft_matcher import NON_CONSUMABLE_COMPONENT_CLASSES, COMPONENT_CLASSES_BY_GOAL, GOAL_FAMILIES
        for goal in GOAL_FAMILIES:
            valid_classes = COMPONENT_CLASSES_BY_GOAL.get(goal, set())
            for non_consumable in NON_CONSUMABLE_COMPONENT_CLASSES:
                if non_consumable in valid_classes:
                    plan = draft_options(self.catalog, goal, {"component_class": non_consumable})["question_plan"]
                    q_ids = [q["id"] for q in plan]
                    self.assertNotIn(
                        "product_form",
                        q_ids,
                        f"CRITICAL: product_form was asked for goal='{goal}' with non-consumable class='{non_consumable}'!"
                    )

    def test_product_form_never_asked_in_gear_goal(self):
        """Gear/apparel goal must NEVER generate product_form question under any answers."""
        for answers in [{}, {"activity": "running"}, {"shoe_size": 42}, {"season": "cold"}]:
            plan = draft_options(self.catalog, "gear", answers)["question_plan"]
            q_ids = [q["id"] for q in plan]
            self.assertNotIn("product_form", q_ids, f"product_form generated in gear goal with answers={answers}")

    def test_product_form_strictly_blocked_at_validation_level_for_accessories_and_apparel(self):
        """Validation Guardrail: Recommending or filtering by product_form with non-consumable classes MUST raise DraftMatchError."""
        from draft_matcher import DraftMatchError, NON_CONSUMABLE_COMPONENT_CLASSES, CONSUMABLE_PRODUCT_FORMS
        for goal in ["running", "training", "hydration", "food", "outdoors", "gear", "gift"]:
            for non_consumable in NON_CONSUMABLE_COMPONENT_CLASSES:
                for form in CONSUMABLE_PRODUCT_FORMS:
                    with self.assertRaises(
                        DraftMatchError,
                        msg=f"Expected validation error for goal='{goal}', class='{non_consumable}', form='{form}'"
                    ):
                        draft_recommend(self.catalog, {
                            "goal_group": goal,
                            "component_class": non_consumable,
                            "product_form": form,
                        })

    def test_stress_absurd_forms_rejection(self):
        """Stress test: 100+ combinations of accessories, flasks, belts, mats with absurd forms must all be rejected."""
        from draft_matcher import DraftMatchError
        test_cases = [
            ("outdoors", "sports_accessories", "powder"),
            ("outdoors", "sports_accessories", "gel"),
            ("outdoors", "sports_accessories", "bars"),
            ("outdoors", "sports_accessories", "tablets"),
            ("outdoors", "sports_accessories", "capsules"),
            ("outdoors", "sports_accessories", "food_or_meal"),
            ("outdoors", "apparel_footwear", "bars"),
            ("running", "sports_accessories", "gel"),
            ("running", "sports_accessories", "sticks"),
            ("running", "sports_accessories", "powder"),
            ("running", "apparel_footwear", "capsules"),
            ("running", "apparel_footwear", "tablets"),
            ("hydration", "sports_accessories", "powder"),
            ("hydration", "sports_accessories", "tablets"),
            ("hydration", "sports_accessories", "gel"),
            ("hydration", "sports_accessories", ["sticks", "gel"]),
            ("gear", "sports_accessories", "bars"),
            ("gear", "apparel_footwear", "gel"),
            ("gear", None, "powder"),
            ("gift", "sports_accessories", "tablets"),
            ("gift", "apparel_footwear", "food_or_meal"),
        ]
        for goal, comp_class, form in test_cases:
            req = {"goal_group": goal, "product_form": form}
            if comp_class:
                req["component_class"] = comp_class
            with self.assertRaises(DraftMatchError, msg=f"Failed stress test for {req}"):
                draft_recommend(self.catalog, req)

    def test_medals_and_hygiene_never_have_edible_forms_in_catalog(self):
        """Evidence integrity: Catalog items that contain only accessories/apparel must have 0 consumable product forms."""
        from draft_matcher import CONSUMABLE_PRODUCT_FORMS, NON_CONSUMABLE_COMPONENT_CLASSES, CONSUMABLE_COMPONENT_CLASSES
        for record in self.catalog:
            sku = record.get("sku")
            classes = set(record.get("matching_evidence", {}).get("component_classes", []))
            forms = set(record.get("matching_evidence", {}).get("product_forms", []))
            if classes and not (classes & CONSUMABLE_COMPONENT_CLASSES):
                absurd_forms = forms & CONSUMABLE_PRODUCT_FORMS
                self.assertEqual(
                    absurd_forms, set(),
                    f"Catalog set {sku} ({record.get('title')}) has classes={classes} but absurd forms={absurd_forms}"
                )

    def test_product_form_allowed_and_functional_for_consumable_classes(self):
        """Functional verification: For genuine food and supplements, product_form filtering works smoothly."""
        res_bars = draft_recommend(self.catalog, {
            "goal_group": "running",
            "component_class": "protein_carbohydrate_food",
            "product_form": "bars",
            "max_price_uah": 2000,
        })
        self.assertGreater(res_bars.get("returned_count", 0), 0)
        for item in res_bars.get("results", []):
            matching_rec = next(x for x in self.catalog if x["catalog_row"] == item["catalog_row"])
            forms = set(matching_rec.get("matching_evidence", {}).get("product_forms", []))
            self.assertIn("bars", forms, f"Item {item['title']} matched for bars but has forms {forms}")

    def test_client_matcher_js_enforces_product_form_guardrails_in_node(self):
        """Cross-engine parity: Standalone client-side JS engine must enforce the exact same guardrails."""
        import subprocess
        node_script = """
        global.window = global;
        const fs = require('fs');
        eval(fs.readFileSync('test-quiz-sandbox/web/catalog_data.js', 'utf8'));
        eval(fs.readFileSync('test-quiz-sandbox/web/client_matcher.js', 'utf8'));

        // 1. Check question plan across all goals
        for (const goal of ["outdoors", "hydration", "running", "gift", "gear"]) {
            const planAcc = QUIZ_MATCHER.draftOptions(window.QUIZ_CATALOG, goal, {component_class: "sports_accessories"});
            const qIdsAcc = planAcc.question_plan.map(q => q.id);
            if (qIdsAcc.includes("product_form")) {
                throw new Error(`JS error: product_form asked for ${goal} + sports_accessories`);
            }
            const planApp = QUIZ_MATCHER.draftOptions(window.QUIZ_CATALOG, goal, {component_class: "apparel_footwear"});
            const qIdsApp = planApp.question_plan.map(q => q.id);
            if (qIdsApp.includes("product_form")) {
                throw new Error(`JS error: product_form asked for ${goal} + apparel_footwear`);
            }
        }

        // 2. Check draftRecommend validation rejection
        let rejectedCount = 0;
        const testCases = [
            {goal_group: "running", component_class: "sports_accessories", product_form: "gel"},
            {goal_group: "outdoors", component_class: "sports_accessories", product_form: "powder"},
            {goal_group: "gear", component_class: "apparel_footwear", product_form: "bars"},
            {goal_group: "hydration", component_class: "sports_accessories", product_form: "tablets"}
        ];
        for (const tc of testCases) {
            try {
                QUIZ_MATCHER.draftRecommend(window.QUIZ_CATALOG, tc);
                throw new Error(`JS error: expected rejection for ${JSON.stringify(tc)}`);
            } catch (e) {
                if (e.message.includes("product_form is not applicable")) {
                    rejectedCount++;
                } else {
                    throw e;
                }
            }
        }
        console.log(JSON.stringify({ status: "ok", rejectedCount }));
        """
        proc = subprocess.run(
            ["node", "-e", node_script],
            capture_output=True,
            text=True,
            check=True,
        )
        self.assertIn('"status":"ok"', proc.stdout.replace(" ", ""))

if __name__ == "__main__":
    unittest.main()
