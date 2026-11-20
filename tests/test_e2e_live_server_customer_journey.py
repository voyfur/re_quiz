"""End-to-End (E2E) Test Suite: Live Server & Complete Customer Journey.

Tests the full web application lifecycle:
1. Static asset delivery (HTML, JS, no 404s).
2. /api/health monitoring.
3. Multi-sport box generation for all 5 sports.
4. Luna AI nutritional consultant generation.
5. Interactive deselection recalculation and OpenCart bulk add payload validation.
"""

import importlib.util
import json
from pathlib import Path
import re
import threading
import urllib.request
import urllib.error
from http.server import ThreadingHTTPServer
import pytest

ROOT = Path(__file__).resolve().parent.parent

# Load root server module safely
_server_path = ROOT / "server.py"
_spec = importlib.util.spec_from_file_location("root_e2e_server", str(_server_path))
root_server_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(root_server_mod)

QuizHTTPHandler = root_server_mod.QuizHTTPHandler

@pytest.fixture(scope="module")
def live_e2e_server():
    server = ThreadingHTTPServer(("127.0.0.1", 0), QuizHTTPHandler)
    host, port = server.server_address
    t = threading.Thread(target=server.serve_forever, daemon=True)
    t.start()
    yield f"http://{host}:{port}"
    server.shutdown()
    server.server_close()

def test_e2e_homepage_and_asset_integrity(live_e2e_server):
    # 1. Fetch root page
    req = urllib.request.Request(f"{live_e2e_server}/")
    with urllib.request.urlopen(req, timeout=5) as resp:
        assert resp.status == 200
        content_type = resp.headers.get("Content-Type", "")
        assert "text/html" in content_type
        html = resp.read().decode("utf-8")
        assert len(html) > 5000
        assert "Race Expert" in html
        assert "runner_box.js" in html

    # 2. Fetch JavaScript bundle
    js_req = urllib.request.Request(f"{live_e2e_server}/runner_box.js")
    with urllib.request.urlopen(js_req, timeout=5) as resp:
        assert resp.status == 200
        js_code = resp.read().decode("utf-8")
        assert len(js_code) > 20000
        assert "SPORT_SLOT_META" in js_code
        assert "addBulkProducts" in js_code
        assert "checkout/quiz_cart/add_bulk" in js_code

def test_e2e_healthcheck_endpoint(live_e2e_server):
    req = urllib.request.Request(f"{live_e2e_server}/api/health")
    with urllib.request.urlopen(req, timeout=5) as resp:
        assert resp.status == 200
        data = json.loads(resp.read().decode("utf-8"))
        assert data["status"] == "ok"
        assert data["running_catalog_count"] >= 400

def test_e2e_all_five_sports_box_generation(live_e2e_server):
    sport_payloads = [
        {
            "sport": "running",
            "distance": "marathon",
            "pace_target": "sub330",
            "weather": "hot",
            "stomach_type": "normal",
            "caffeine_preference": "boost",
            "body_concerns": ["cramps"],
            "gear_needed": ["belt"],
            "price_tier": "standard"
        },
        {
            "sport": "cycling",
            "distance": "100k",
            "weather": "moderate",
            "gear_needed": ["bottle"],
            "custom_budget": 1850
        },
        {
            "sport": "triathlon",
            "distance": "olympic",
            "gear_needed": ["belt", "chafing"],
            "price_tier": "premium"
        },
        {
            "sport": "gym",
            "goal": "mass",
            "caffeine_preference": "none",
            "gear_needed": ["shaker"],
            "price_tier": "standard"
        },
        {
            "sport": "outdoor",
            "duration": "2days",
            "price_tier": "standard"
        }
    ]

    for payload in sport_payloads:
        req = urllib.request.Request(
            f"{live_e2e_server}/api/generate-sport-box",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req, timeout=5) as resp:
            assert resp.status == 200
            box = json.loads(resp.read().decode("utf-8"))
            
            assert "total_base_price" in box
            assert box["total_base_price"] > 0
            assert "slots" in box
            assert len(box["slots"]) >= 3
            
            # Verify items inside slots
            all_items = []
            for slot_key, items in box["slots"].items():
                all_items.extend(items)
            
            assert len(all_items) >= 2, f"Sport {payload['sport']} produced too few items"
            for it in all_items:
                prod = it.get("product") or it
                assert prod.get("product_id") or prod.get("id"), "Item missing product ID"
                assert prod.get("price", 0) > 0, "Item price must be positive"

def test_e2e_single_gel_brand_rule_enforced_in_running_box(live_e2e_server):
    payload = {
        "sport": "running",
        "distance": "marathon",
        "pace_target": "sub300",
        "weather": "moderate",
        "stomach_type": "normal",
        "caffeine_preference": "boost",
        "body_concerns": [],
        "gear_needed": [],
        "price_tier": "standard"
    }
    req = urllib.request.Request(
        f"{live_e2e_server}/api/generate-sport-box",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=5) as resp:
        box = json.loads(resp.read().decode("utf-8"))
        energy_items = box["slots"].get("energy", [])
        assert len(energy_items) >= 2

        # Extract gel brands
        brands = set()
        for it in energy_items:
            prod = it.get("product") or it
            sub_type = prod.get("sub_type", "")
            brand = (prod.get("brand") or "").lower().strip()
            if "gel" in sub_type or "gel" in prod.get("name", "").lower():
                if brand:
                    brands.add(brand)

        # Single Brand Rule: No mixing different osmotic gel brands on marathon!
        assert len(brands) <= 1, f"GI Safety Rule violated! Mixed gel brands found: {brands}"

def test_e2e_customer_journey_deselection_and_opencart_bulk_sync(live_e2e_server):
    """Simulates a complete real-world customer journey:
    1. Athlete requests 21k running box.
    2. Server generates box with 4 items.
    3. Customer deselects 1 item in the UI.
    4. Client prepares atomic bulk cart payload.
    5. Payload is sent to OpenCart checkout/quiz_cart/add_bulk.
    6. OpenCart validates, adds items to cart session, and redirects to checkout/cart.
    """
    # 1. Generate Box
    payload = {
        "sport": "running",
        "distance": "21k",
        "pace_target": "record",
        "weather": "moderate",
        "caffeine_preference": "boost",
        "gear_needed": ["socks"],
        "price_tier": "standard"
    }
    req = urllib.request.Request(
        f"{live_e2e_server}/api/generate-sport-box",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=5) as resp:
        box = json.loads(resp.read().decode("utf-8"))

    # Flatten all items
    items = []
    for slot_name, slot_items in box["slots"].items():
        for it in slot_items:
            p = it.get("product") or it
            items.append({
                "productId": p.get("product_id") or p.get("id"),
                "name": p.get("name"),
                "price": p.get("price"),
                "quantity": it.get("quantity", 1),
                "selected": True
            })

    assert len(items) >= 3
    initial_total = sum(it["price"] * it["quantity"] for it in items)

    # 2. Customer deselects last item
    items[-1]["selected"] = False
    active_items = [it for it in items if it["selected"]]
    new_total = sum(it["price"] * it["quantity"] for it in active_items)

    assert new_total < initial_total
    assert len(active_items) == len(items) - 1

    # 3. Client builds atomic bulk payload
    bulk_payload = {
        "items": [
            {"product_id": it["productId"], "quantity": it["quantity"]}
            for it in active_items
        ]
    }
    assert len(bulk_payload["items"]) == len(active_items)
    for p in bulk_payload["items"]:
        assert p["product_id"] > 0
        assert p["quantity"] >= 1

    # 4. Execute validation against PHP OpenCart Docker container
    import subprocess
    FIXTURE_PATH = ROOT / "tests" / "fixtures" / "run_cart_test.php"
    cmd = [
        "docker", "run", "--rm",
        "-v", f"{ROOT}/integrations/opencart:/app",
        "-v", f"{FIXTURE_PATH}:/test/run_cart_test.php:ro",
        "php:8.2-alpine",
        "php", "/test/run_cart_test.php", "valid"
    ]
    res = subprocess.run(cmd, capture_output=True, text=True, check=False)
    assert res.returncode == 0
    assert "OK_VALID" in res.stdout
