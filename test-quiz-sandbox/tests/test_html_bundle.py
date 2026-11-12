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
