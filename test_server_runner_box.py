import json
import threading
import urllib.request
from http.server import ThreadingHTTPServer
import pytest
import importlib.util
from pathlib import Path

_server_path = Path(__file__).resolve().parent / "server.py"
_spec = importlib.util.spec_from_file_location("quiz_server", str(_server_path))
_server_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_server_mod)
QuizHTTPHandler = _server_mod.QuizHTTPHandler
RUNNING_CATALOG = _server_mod.RUNNING_CATALOG

@pytest.fixture(scope="module")
def live_server():
    server = ThreadingHTTPServer(("127.0.0.1", 0), QuizHTTPHandler)
    host, port = server.server_address
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    yield f"http://{host}:{port}"
    server.shutdown()
    server.server_close()

def test_server_health(live_server):
    req = urllib.request.Request(f"{live_server}/api/health")
    with urllib.request.urlopen(req, timeout=5) as resp:
        assert resp.status == 200
        data = json.loads(resp.read().decode("utf-8"))
        assert data["status"] == "ok"
        assert data["running_catalog_count"] == len(RUNNING_CATALOG)
        assert data["running_catalog_count"] >= 400

def test_server_generate_runner_box(live_server):
    payload = {
        "distance": "21k",
        "pace_target": "record",
        "weather": "hot",
        "stomach_type": "normal",
        "caffeine_preference": "boost",
        "body_concerns": ["cramps", "chafing"],
        "gear_needed": ["belt", "flask"],
        "price_tier": "standard"
    }
    data_bytes = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        f"{live_server}/api/generate-runner-box",
        data=data_bytes,
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=5) as resp:
        assert resp.status == 200
        box = json.loads(resp.read().decode("utf-8"))
        assert "slots" in box
        assert "energy" in box["slots"]
        assert "hydration" in box["slots"]
        assert "gear" in box["slots"]
        assert "care_recovery" in box["slots"]
        assert box["total_base_price"] > 0

def test_server_runner_box_html(live_server):
    for route in ["/runner-box", "/box", "/runner_box.html"]:
        req = urllib.request.Request(f"{live_server}{route}")
        with urllib.request.urlopen(req, timeout=5) as resp:
            assert resp.status == 200
            assert "text/html" in resp.headers.get("Content-Type", "")
            body = resp.read().decode("utf-8")
            assert "Стартовий бокс бігуна" in body
            assert "runner_box.js" in body

def test_server_runner_box_js(live_server):
    req = urllib.request.Request(f"{live_server}/runner_box.js")
    with urllib.request.urlopen(req, timeout=5) as resp:
        assert resp.status == 200
        body = resp.read().decode("utf-8")
        assert "generateRunnerBox" in body
        assert "addProductWithRetry" in body

def test_server_luna_consult_box(live_server):
    payload = {
        "user_inputs": {"distance": "10k", "pace_target": "steady", "weather": "cold", "caffeine_preference": "boost"},
        "generated_box": {
            "distance_label": "10 км",
            "slots": {
                "energy": [{"product": {"name": "SiS Gel", "caffeine": False}, "quantity_recommended": 1, "reason_badge": "Основна енергія"}]
            }
        }
    }
    data_bytes = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        f"{live_server}/api/luna-consult-box",
        data=data_bytes,
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=12) as resp:
        assert resp.status == 200
        data = json.loads(resp.read().decode("utf-8"))
        assert data["ok"] is True
        assert "data" in data
        assert "expert_verdict" in data["data"]
        assert "timeline_steps" in data["data"]


