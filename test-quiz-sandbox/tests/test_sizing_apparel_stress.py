import json
import subprocess
import unittest
from pathlib import Path

from draft_matcher import attach_audit_evidence, draft_options, draft_recommend, _size_ranges
from server import AUDIT_PATH, CATALOG_PATH, _load_catalog

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent


class TestSizingApparelStress(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        catalog = _load_catalog(CATALOG_PATH)
        audit = json.loads(Path(AUDIT_PATH).read_text(encoding="utf-8"))
        cls.catalog = attach_audit_evidence(catalog, audit)

    def test_catalog_sizing_and_sock_coverage(self):
        """Verify that all kits mentioning socks/footwear have valid sizing metadata."""
        size_sensitive_rows = []
        for item in self.catalog:
            ev = item.get("matching_evidence", {})
            title = item.get("title", "").lower()
            ranges = _size_ranges(item)
            is_sens = ev.get("size_sensitive", False)
            classes = ev.get("component_classes", [])

            has_socks = any(w in title for w in ["шкарпет", "носк", "socks"])
            if has_socks or is_sens or ranges:
                size_sensitive_rows.append(item["catalog_row"])
                # If socks are mentioned in title, it must have size ranges or be marked size sensitive
                if has_socks:
                    self.assertTrue(
                        is_sens or len(ranges) > 0,
                        f"Row {item['catalog_row']} mentions socks but lacks size metadata: {item['title']}"
                    )

        # There are 38+ size-sensitive and apparel kits in the 207-set catalog
        self.assertGreaterEqual(len(size_sensitive_rows), 38)

    def test_shoe_size_always_first_for_apparel_footwear(self):
        """Verify that shoe_size is ALWAYS asked first when apparel_footwear is selected."""
        for goal in ["running", "gear", "outdoors", "gift"]:
            plan = draft_options(self.catalog, goal, {"component_class": "apparel_footwear"})["question_plan"]
            q_ids = [q["id"] for q in plan]
            self.assertIn("shoe_size", q_ids, f"shoe_size missing for goal={goal}")
            self.assertEqual(
                q_ids[0],
                "shoe_size",
                f"shoe_size was NOT the first question for goal={goal}! Plan: {q_ids}"
            )

    def test_shoe_size_never_dropped_by_early_termination(self):
        """Verify that early termination NEVER bypasses shoe_size even if candidates <= 3."""
        # Even if a subset has few candidates, shoe_size must still be asked before budget
        for goal in ["running", "gear", "outdoors", "gift"]:
            opts = draft_options(self.catalog, goal, {"component_class": "apparel_footwear"})
            plan = opts["question_plan"]
            q_ids = [q["id"] for q in plan]
            # Sizing question must always precede budget
            if "max_price_uah" in q_ids:
                budget_idx = q_ids.index("max_price_uah")
                size_idx = q_ids.index("shoe_size")
                self.assertLess(size_idx, budget_idx, f"Budget asked before shoe_size for goal={goal}")

    def test_shoe_size_never_asked_for_non_sizing_categories(self):
        """Verify that shoe_size is strictly barred from food, hydration, vitamins, etc."""
        nutrition_classes = [
            "protein_carbohydrate_food",
            "supplements_vitamins_minerals",
            "hydration_items",
            "creatine_preworkout",
            "dehydrated_meal",
        ]
        from draft_matcher import COMPONENT_CLASSES_BY_GOAL
        for goal in ["food", "hydration", "recovery", "daily"]:
            plan = draft_options(self.catalog, goal, {})["question_plan"]
            q_ids = [q["id"] for q in plan]
            self.assertNotIn("shoe_size", q_ids, f"shoe_size asked for pure {goal} goal!")
            valid_classes = COMPONENT_CLASSES_BY_GOAL.get(goal, set()) & set(nutrition_classes)
            for n_class in valid_classes:
                plan_comp = draft_options(self.catalog, goal, {"component_class": n_class})["question_plan"]
                q_comp_ids = [q["id"] for q in plan_comp]
                self.assertNotIn(
                    "shoe_size",
                    q_comp_ids,
                    f"shoe_size asked for {goal} with {n_class}!"
                )

    def test_rare_and_non_existent_sizes_floor_anchor_and_no_empty_screen(self):
        """Stress-test edge sizes (30, 35, 48, 50, 99) across budgets and goals - zero empty screens."""
        test_sizes = [25, 30, 34, 35, 36, 42, 48, 49, 50, 60]
        test_budgets = [None, 200, 500, 1500, 5000, 20000]
        test_goals = ["running", "gear", "outdoors", "gift"]

        for goal in test_goals:
            for size in test_sizes:
                for budget in test_budgets:
                    req = {
                        "goal_group": goal,
                        "component_class": "apparel_footwear",
                        "shoe_size": size,
                    }
                    if budget is not None:
                        req["max_price_uah"] = budget

                    res = draft_recommend(self.catalog, req)
                    total_results = (
                        len(res.get("results", []))
                        + len(res.get("near_miss_results", []))
                        + len(res.get("floor_anchor_results", []))
                    )

                    self.assertGreater(
                        total_results,
                        0,
                        f"EMPTY SCREEN for goal={goal}, size={size}, budget={budget}! Status: {res.get('status')}"
                    )

                    # If no exact results, floor anchor must be active
                    if not res.get("results") and not res.get("near_miss_results"):
                        self.assertEqual(
                            res.get("status"),
                            "floor_anchor",
                            f"Expected floor_anchor status for size {size}, budget {budget}, got: {res.get('status')}"
                        )
                        self.assertGreater(
                            len(res.get("floor_anchor_results", [])),
                            0,
                            f"Floor anchor results empty for size {size}, budget {budget}"
                        )

    def test_question_depth_strictly_capped_at_five_steps(self):
        """Verify that question depth for any sizing scenario NEVER exceeds 5 steps:
        Goal (1) -> Component (2) -> Shoe Size (3) -> Season (4) -> Budget (5)."""
        for goal in ["running", "gear", "outdoors", "gift"]:
            # Step 1: User picks Goal
            # Step 2: Component class
            plan_step2 = draft_options(self.catalog, goal, {"component_class": "apparel_footwear"})["question_plan"]
            remaining_after_step2 = [q["id"] for q in plan_step2]

            # Path length: Goal (1) + Component (1) + remaining questions <= 5
            total_steps = 2 + len(remaining_after_step2)
            self.assertLessEqual(
                total_steps,
                5,
                f"Question depth too long ({total_steps}) for goal={goal}: {['goal', 'component_class'] + remaining_after_step2}"
            )

            # Step 3: User answers Shoe Size
            plan_step3 = draft_options(
                self.catalog,
                goal,
                {"component_class": "apparel_footwear", "shoe_size": 42}
            )["question_plan"]
            remaining_after_step3 = [q["id"] for q in plan_step3]
            total_steps_from_step3 = 3 + len(remaining_after_step3)
            self.assertLessEqual(
                total_steps_from_step3,
                5,
                f"Question depth exceeded after shoe_size for goal={goal}: {remaining_after_step3}"
            )

            # Step 4: If season was asked, answer it
            if "season" in remaining_after_step3:
                plan_step4 = draft_options(
                    self.catalog,
                    goal,
                    {"component_class": "apparel_footwear", "shoe_size": 42, "season": "cold"}
                )["question_plan"]
                remaining_after_step4 = [q["id"] for q in plan_step4]
                # After goal (1) + component (2) + size (3) + season (4), only budget (5) can remain!
                self.assertTrue(
                    remaining_after_step4 == ["max_price_uah"] or remaining_after_step4 == [],
                    f"Expected only budget after season for goal={goal}, got: {remaining_after_step4}"
                )

    def test_floor_anchor_messages_and_reasons_contain_size_fallback_info(self):
        """Verify that when floor anchor triggers for unavailable size, reasons explain it properly."""
        # Size 50 in outdoors has no matches
        res = draft_recommend(self.catalog, {
            "goal_group": "outdoors",
            "component_class": "apparel_footwear",
            "shoe_size": 50,
            "locale": "ru"
        })
        self.assertEqual(res["status"], "floor_anchor")
        self.assertGreater(len(res["floor_anchor_results"]), 0)

        item = res["floor_anchor_results"][0]
        self.assertEqual(item["size_status"], "size_fallback")
        all_text = " ".join(item.get("reasons", []) + item.get("data_notes", []))
        self.assertTrue(
            any(w in all_text for w in ["размер", "отсутствует", "базовый"]),
            f"Expected size fallback explanation in reasons/notes: {all_text}"
        )

    def test_node_standalone_html_bundle_sizing_and_floor_anchor(self):
        """Verify that compiled quiz.html executes sizing and floor anchor flawlessly in Node.js."""
        node_script = """
        const fs = require('fs');
        const html = fs.readFileSync('quiz.html', 'utf-8');
        const scripts = [...html.matchAll(/<script>([\\s\\S]*?)<\\/script>/g)].map(m => m[1]);
        global.window = global;
        eval(scripts[1]); // QUIZ_CATALOG
        eval(scripts[2]); // QUIZ_MATCHER

        // 1. Sizing question priority in JS bundle
        const plan = QUIZ_MATCHER.draftOptions(QUIZ_CATALOG, 'running', { component_class: 'apparel_footwear' }).question_plan;
        if (!plan || plan.length === 0 || plan[0].id !== 'shoe_size') {
            throw new Error('JS bundle did not place shoe_size first in running apparel plan!');
        }

        // 2. Rare size fallback (size 48 in outdoors)
        const resRare = QUIZ_MATCHER.draftRecommend(QUIZ_CATALOG, {
            goal_group: 'outdoors',
            component_class: 'apparel_footwear',
            shoe_size: 48,
            locale: 'ru'
        });
        const totalRare = (resRare.results?.length || 0) + (resRare.floor_anchor_results?.length || 0);
        if (totalRare === 0) {
            throw new Error('JS bundle returned 0 results (empty screen) for rare size 48 in outdoors!');
        }
        if (resRare.status !== 'floor_anchor') {
            throw new Error('Expected floor_anchor status in JS bundle for rare size, got: ' + resRare.status);
        }

        // 3. Question depth limit <= 5 in JS bundle
        const fullPlan = QUIZ_MATCHER.draftOptions(QUIZ_CATALOG, 'running', { component_class: 'apparel_footwear' }).question_plan;
        if (2 + fullPlan.length > 5) {
            throw new Error('JS bundle question depth exceeded 5: ' + (2 + fullPlan.length));
        }

        console.log(JSON.stringify({
            first_q: plan[0].id,
            rare_status: resRare.status,
            rare_count: totalRare,
            success: true
        }));
        """
        proc = subprocess.run(
            ["node", "-e", node_script],
            cwd=str(PROJECT_ROOT),
            capture_output=True,
            text=True,
            check=True,
        )
        data = json.loads(proc.stdout)
        self.assertEqual(data["first_q"], "shoe_size")
        self.assertEqual(data["rare_status"], "floor_anchor")
        self.assertGreater(data["rare_count"], 0)


if __name__ == "__main__":
    unittest.main()
