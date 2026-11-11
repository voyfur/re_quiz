import unittest
from pathlib import Path

from catalog_builder import parse_analysis


PROJECT_ROOT = Path(__file__).resolve().parents[2]
ANALYSIS_PATH = PROJECT_ROOT / "wiki" / "projects" / "race-expert-need-sets-206-analysis.md"


class CatalogBuilderTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.records = parse_analysis(ANALYSIS_PATH.read_text(encoding="utf-8"))
        cls.by_row = {record["catalog_row"]: record for record in cls.records}

    def test_extracts_exactly_206_unique_need_based_sets(self):
        self.assertEqual(len(self.records), 206)
        self.assertEqual(len(self.by_row), 206)
        self.assertTrue(all(record["source_url"].startswith("https://") for record in self.records))

    def test_preserves_required_catalog_fields_and_tag_values(self):
        for record in self.records:
            self.assertTrue(record["set_id"])
            self.assertTrue(record["title"])
            self.assertGreater(record["price_uah"], 0)
            self.assertTrue(record["tags"].get("purpose"))

    def test_preserves_caffeine_evidence_without_inventing_absence(self):
        for row in (38, 136, 148, 206):
            self.assertIn("caffeine", self.by_row[row]["tags"].get("contains", []))
        self.assertEqual(self.by_row[206]["tags"].get("caffeine_per_set"), ["400_mg"])
        self.assertNotIn("caffeine_free_verified", self.by_row[1]["tags"])

    def test_retains_composition_and_source_for_a_result_card(self):
        record = self.by_row[206]
        self.assertIn("PWO Shot", record["composition"])
        self.assertIn("product_id=7151", record["source_url"])


if __name__ == "__main__":
    unittest.main()
