import io
import json
import unittest
from email.message import Message

from server import CATALOG_PATH, _load_catalog, create_server, make_handler


class ApiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.handler_class = make_handler(_load_catalog(CATALOG_PATH))

    def dispatch(self, method, path, body=b"", headers=None):
        handler = object.__new__(self.handler_class)
        handler.path = path
        handler.headers = Message()
        for key, value in (headers or {}).items():
            handler.headers[key] = value
        handler.rfile = io.BytesIO(body)
        handler.wfile = io.BytesIO()
        handler.response_headers = {}
        handler.send_response = lambda status: setattr(handler, "status", status)
        handler.send_header = lambda key, value: handler.response_headers.__setitem__(key, value)
        handler.end_headers = lambda: None
        if method == "GET":
            handler.do_GET()
        else:
            handler.do_POST()
        return handler.status, handler.response_headers, handler.wfile.getvalue()

    def post_json(self, path, payload):
        body = json.dumps(payload).encode("utf-8")
        return self.dispatch(
            "POST", path, body,
            {"Content-Type": "application/json", "Content-Length": str(len(body))},
        )

    def test_home_page_is_served_with_test_only_banner(self):
        status, headers, body = self.dispatch("GET", "/")
        page = body.decode("utf-8")
        self.assertEqual(status, 200)
        self.assertIn("Content-Security-Policy", headers)
        self.assertIn("TEST ONLY", page)
        self.assertIn("206", page)

    def test_browser_client_uses_only_local_api_and_does_not_store_answers(self):
        project_root = CATALOG_PATH.parent
        script = (project_root / "web" / "app.js").read_text(encoding="utf-8")
        page = (project_root / "web" / "index.html").read_text(encoding="utf-8").lower()
        self.assertIn('fetch("/api/options")', script)
        self.assertIn('fetch("/api/recommend",', script)
        self.assertNotIn("localStorage", script)
        self.assertNotIn("sessionStorage", script)
        self.assertNotIn("add-to-cart", page)
        self.assertNotIn("cart", page)
        self.assertNotIn('id="purpose"', page)
        self.assertIn('input.name = "goal_group"', script)
        self.assertEqual(page.count('class="quiz-step"'), 4)

    def test_options_are_built_from_the_local_206_record_catalog(self):
        status, headers, body = self.dispatch("GET", "/api/options")
        payload = json.loads(body.decode("utf-8"))
        self.assertEqual(status, 200)
        self.assertIn("application/json", headers["Content-Type"])
        self.assertGreaterEqual(payload["catalog_count"], 206)
        self.assertTrue(payload["purpose_options"])
        self.assertTrue({"running", "training", "recovery", "food", "outdoors", "gear", "daily", "gift"}.issubset(
            {option["value"] for option in payload["goal_options"]}
        ))
        self.assertTrue(all("value" in option and "label" in option for option in payload["purpose_options"]))
        self.assertTrue(payload["form_options"])
        self.assertTrue(payload["race_format_options"])
        self.assertEqual(payload["price_range_uah"]["min"], 759)
        self.assertGreaterEqual(payload["price_range_uah"]["max"], 1500)

    def test_recommendation_returns_the_backend_contract(self):
        status, headers, body = self.post_json(
            "/api/recommend",
            {"purpose": "cold_weather_comfort", "result_count": 2, "locale": "uk"},
        )
        payload = json.loads(body.decode("utf-8"))
        self.assertEqual(status, 200)
        self.assertIn("no-store", headers["Cache-Control"])
        self.assertEqual(payload["status"], "matched")
        self.assertTrue(payload["test_only"])
        self.assertTrue(payload["alternatives"])
        self.assertIn("Знайдено тестових варіантів", payload["message"])
        self.assertEqual(payload["returned_count"], 2)
        self.assertTrue(payload["results"][0]["source_url"].startswith("https://"))
        self.assertTrue(all(item["is_alternative"] for item in payload["results"]))
        self.assertTrue(all(item["price_snapshot_date"] == "2026-11-06" for item in payload["results"]))

    def test_consumer_goal_request_returns_matching_alternatives(self):
        status, _, body = self.post_json(
            "/api/recommend",
            {"goal_group": "running", "result_count": 2, "locale": "uk"},
        )
        payload = json.loads(body.decode("utf-8"))
        self.assertEqual(status, 200)
        self.assertEqual(payload["returned_count"], 2)
        self.assertTrue(all(item["is_alternative"] for item in payload["results"]))

    def test_unsupported_filters_return_a_clear_client_error(self):
        status, _, body = self.post_json(
            "/api/recommend",
            {"purpose": "cold_weather_comfort", "age": 12},
        )
        payload = json.loads(body.decode("utf-8"))
        self.assertEqual(status, 400)
        self.assertTrue(payload["test_only"])
        self.assertIn("age", payload["error"])

    def test_bad_json_and_unknown_routes_do_not_return_recommendations(self):
        bad_json = b"{invalid"
        bad_status, _, bad_body = self.dispatch(
            "POST", "/api/recommend", bad_json,
            {"Content-Type": "application/json", "Content-Length": str(len(bad_json))},
        )
        self.assertEqual(bad_status, 400)
        self.assertTrue(json.loads(bad_body.decode("utf-8"))["error"])
        status, _, body = self.post_json("/api/not-a-route", {})
        payload = json.loads(body.decode("utf-8"))
        self.assertEqual(status, 404)
        self.assertEqual(payload["results"], [])

    def test_request_size_and_loopback_binding_are_guarded(self):
        status, _, body = self.dispatch(
            "POST", "/api/recommend", b"x" * 20,
            {"Content-Type": "application/json", "Content-Length": str(32769)},
        )
        self.assertEqual(status, 400)
        self.assertIn("32768", json.loads(body.decode("utf-8"))["error"])
        with self.assertRaises(ValueError):
            create_server(host="0.0.0.0", port=0, catalog_path=CATALOG_PATH)

    def test_check_stock_endpoint_returns_availability_data(self):
        status, headers, body = self.post_json(
            "/api/check-stock",
            {"skus": ["RE88955", "RE11819"]},
        )
        payload = json.loads(body.decode("utf-8"))
        self.assertEqual(status, 200)
        self.assertIn("stocks", payload)
        stocks = payload["stocks"]
        self.assertIn("RE88955", stocks)
        self.assertIn("RE11819", stocks)
        self.assertIn("in_stock", stocks["RE88955"])
        self.assertIn("in_stock", stocks["RE11819"])


if __name__ == "__main__":
    unittest.main()
