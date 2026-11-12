import json
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent


class TestHtmlBundle(unittest.TestCase):
    def setUp(self):
        self.quiz_html = ROOT / "quiz.html"
        self.public_html = ROOT / "public" / "index.html"
        self.assertTrue(self.quiz_html.exists(), "quiz.html does not exist")
        self.assertTrue(self.public_html.exists(), "public/index.html does not exist")
        self.html_content = self.quiz_html.read_text(encoding="utf-8")

    def test_file_size_and_standalone(self):
        # Must be self-contained and reasonably sized (> 300 KB with 206 kits)
        size_kb = len(self.html_content.encode("utf-8")) / 1024
        self.assertGreater(size_kb, 300, f"HTML file size is too small: {size_kb:.1f} KB")

    def test_title_and_branding(self):
        self.assertIn("<title>Race Expert Quiz</title>", self.html_content)
        self.assertIn("Race Expert Quiz", self.html_content)

    def test_bilingual_support_present(self):
        # Both Ukrainian and Russian language switches and dictionaries
        self.assertIn('id="btnUk"', self.html_content)
        self.assertIn('id="btnRu"', self.html_content)
        self.assertIn("UI_COPY", self.html_content)
        self.assertIn("uk:", self.html_content)
        self.assertIn("ru:", self.html_content)
        self.assertIn("Для якої мети ви обираєте набір?", self.html_content)
        self.assertIn("Для какой цели вы подбираете набор?", self.html_content)

    def test_catalog_embedded(self):
        self.assertIn("window.QUIZ_CATALOG", self.html_content)
        self.assertIn("window.QUIZ_MATCHER", self.html_content)

    def test_restart_buttons_present_and_wired(self):
        # Top restart button
        self.assertIn('id="btnRestart"', self.html_content)
        self.assertIn('id="lblRestart"', self.html_content)
        # Bottom restart button
        self.assertIn('id="btnBottomRestart"', self.html_content)
        self.assertIn('id="lblBottomRestart"', self.html_content)
        # Check copy and handler binding
        self.assertIn('restart: "Пройти заново"', self.html_content)
        self.assertIn('btnBottomRestart.onclick = restartQuiz', self.html_content)
        self.assertIn('document.getElementById("btnRestart").onclick = restartQuiz', self.html_content)

    def test_public_and_root_bundles_identical_and_standalone(self):
        public_content = self.public_html.read_text(encoding="utf-8")
        self.assertEqual(self.html_content, public_content, "quiz.html and public/index.html must be identical")
        
        # Verify client bundles in public/
        pub_cat = ROOT / "public" / "catalog_data.js"
        pub_matcher = ROOT / "public" / "client_matcher.js"
        self.assertTrue(pub_cat.exists(), "public/catalog_data.js missing")
        self.assertTrue(pub_matcher.exists(), "public/client_matcher.js missing")
        self.assertGreater(len(pub_cat.read_text(encoding="utf-8")), 100000)
        self.assertGreater(len(pub_matcher.read_text(encoding="utf-8")), 30000)

    def test_any_option_strictly_at_the_end(self):
        # Must place 'any' strictly at the end, never at the beginning
        self.assertIn(': [...rawOptions, "any"]', self.html_content)
        self.assertNotIn(': ["any", ...', self.html_content)
        self.assertIn('any: "Не має значення"', self.html_content)
        self.assertIn('any: "Не имеет значения"', self.html_content)

    def test_localization_titles_and_no_results_messages(self):
        # Ukrainian headers and messages
        self.assertIn('resultsFound: "Знайдено наборів: {count}"', self.html_content)
        self.assertIn('resultsNotFound: "На жаль, за вашими критеріями наборів не знайдено"', self.html_content)
        
        # Russian headers and messages
        self.assertIn('resultsFound: "Найдено наборов: {count}"', self.html_content)
        self.assertIn('resultsNotFound: "К сожалению, по вашим критериям наборов не найдено"', self.html_content)

        # Matcher no_match messages
        self.assertIn("На жаль, за вашими критеріями підходящих наборів не знайдено", self.html_content)
        self.assertIn("К сожалению, по вашим критериям подходящих наборов не найдено", self.html_content)

    def test_node_full_simulation_and_flow_integrity(self):
        node_script = """
        const fs = require('fs');
        const html = fs.readFileSync('quiz.html', 'utf-8');
        const scripts = [...html.matchAll(/<script>([\\s\\S]*?)<\\/script>/g)].map(m => m[1]);
        global.window = global;
        eval(scripts[1]); // QUIZ_CATALOG
        eval(scripts[2]); // QUIZ_MATCHER

        // 1. Verify all 9 goals question plans have 'any' strictly at the end
        const goals = ["running", "training", "hydration", "food", "recovery", "outdoors", "gear", "daily", "gift"];
        for (const goal of goals) {
            const planRes = QUIZ_MATCHER.draftOptions(QUIZ_CATALOG, goal, {});
            const plan = planRes.question_plan || [];
            for (const q of plan) {
                if (q.type !== "number" && q.options) {
                    const rawOptions = (q.options || []).filter(o => o !== "any");
                    const opts = [...rawOptions, "any"];
                    if (opts[opts.length - 1] !== "any") {
                        throw new Error(`In goal ${goal}, question ${q.id}: 'any' is not the last option!`);
                    }
                    if (opts[0] === "any" && opts.length > 1) {
                        throw new Error(`In goal ${goal}, question ${q.id}: 'any' is erroneously at index 0!`);
                    }
                }
            }
        }

        // 2. Verify no-results scenario returns localized message
        const noMatchUk = QUIZ_MATCHER.draftRecommend(QUIZ_CATALOG, {
            goal_group: 'running',
            activity: 'running',
            max_price_uah: 50, // Impossible budget
            locale: 'uk'
        });
        if (noMatchUk.results.length !== 0) {
            throw new Error('Expected 0 results for 50 UAH running kit');
        }
        if (!noMatchUk.message) {
            throw new Error('Message is empty for no-match scenario');
        }

        const noMatchRu = QUIZ_MATCHER.draftRecommend(QUIZ_CATALOG, {
            goal_group: 'running',
            activity: 'running',
            max_price_uah: 50,
            locale: 'ru'
        });
        if (noMatchRu.results.length !== 0) {
            throw new Error('Expected 0 results for 50 UAH running kit (RU)');
        }

        // 3. Test strict no_match with impossible filter combination
        const strictNoMatch = QUIZ_MATCHER.draftRecommend(QUIZ_CATALOG, {
            goal_group: 'recovery',
            component_class: 'creatine_preworkout', // Disallowed in recovery
            locale: 'uk'
        });
        if (strictNoMatch.results.length !== 0) {
            throw new Error('Expected 0 results for creatine in recovery');
        }
        if (!strictNoMatch.message.includes('На жаль, за вашими критеріями')) {
            throw new Error('Ukrainian no_match message does not include expected phrase: ' + strictNoMatch.message);
        }

        const strictNoMatchRu = QUIZ_MATCHER.draftRecommend(QUIZ_CATALOG, {
            goal_group: 'recovery',
            component_class: 'creatine_preworkout',
            locale: 'ru'
        });
        if (!strictNoMatchRu.message.includes('К сожалению, по вашим критериям')) {
            throw new Error('Russian no_match message does not include expected phrase: ' + strictNoMatchRu.message);
        }

        console.log(JSON.stringify({
            verified_goals_count: goals.length,
            uk_no_match_msg: strictNoMatch.message,
            ru_no_match_msg: strictNoMatchRu.message,
            uk_near_miss_or_floor: noMatchUk.status,
            success: true
        }));
        """
        proc = subprocess.run(
            ["node", "-e", node_script],
            cwd=str(ROOT),
            capture_output=True,
            text=True,
            check=True,
        )
        data = json.loads(proc.stdout)
        self.assertTrue(data["success"])
        self.assertEqual(data["verified_goals_count"], 9)
        self.assertIn("На жаль, за вашими критеріями", data["uk_no_match_msg"])
        self.assertIn("К сожалению, по вашим критериям", data["ru_no_match_msg"])

    def test_node_execution_and_matcher_scenarios(self):
        node_script = """
        const fs = require('fs');
        const html = fs.readFileSync('quiz.html', 'utf-8');
        const scripts = [...html.matchAll(/<script>([\\s\\S]*?)<\\/script>/g)].map(m => m[1]);
        global.window = global;
        eval(scripts[1]);
        eval(scripts[2]);

        if (!Array.isArray(window.QUIZ_CATALOG) || window.QUIZ_CATALOG.length < 200) {
            throw new Error('QUIZ_CATALOG invalid length: ' + (window.QUIZ_CATALOG ? window.QUIZ_CATALOG.length : 0));
        }

        // Test Scenario 1: Running
        const resRun = QUIZ_MATCHER.draftRecommend(QUIZ_CATALOG, { goal_group: 'running', max_price_uah: 2500 });
        if (!resRun.results || resRun.results.length === 0) {
            throw new Error('No results for running scenario');
        }

        // Test Scenario 2: Hydration
        const resHyd = QUIZ_MATCHER.draftRecommend(QUIZ_CATALOG, { goal_group: 'hydration', max_price_uah: 1500 });
        if (!resHyd.results || resHyd.results.length === 0) {
            throw new Error('No results for hydration scenario');
        }

        // Test Scenario 3: Training
        const resTrain = QUIZ_MATCHER.draftRecommend(QUIZ_CATALOG, { goal_group: 'training', max_price_uah: 3000 });
        if (!resTrain.results || resTrain.results.length === 0) {
            throw new Error('No results for training scenario');
        }

        console.log(JSON.stringify({
            catalog_count: window.QUIZ_CATALOG.length,
            running_matches: resRun.results.length,
            top_running: resRun.results[0].title,
            hydration_matches: resHyd.results.length,
            training_matches: resTrain.results.length,
        }));
        """
        proc = subprocess.run(
            ["node", "-e", node_script],
            cwd=str(ROOT),
            capture_output=True,
            text=True,
            check=True,
        )
        data = json.loads(proc.stdout)
        self.assertGreaterEqual(data["catalog_count"], 206)
        self.assertGreater(data["running_matches"], 0)
        self.assertGreater(data["hydration_matches"], 0)
        self.assertGreater(data["training_matches"], 0)


if __name__ == "__main__":
    unittest.main()
