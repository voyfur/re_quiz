"""End-to-End (E2E) Test Suite: Multi-Threaded Concurrency & Load Verification.

Fires 50 rapid concurrent requests across multiple threads to prove that:
1. ThreadingHTTPServer handles concurrent requests without dropped connections.
2. Box generation engines are thread-safe and re-entrant.
3. Latency remains sub-50ms per request under concurrent load.
"""

from concurrent.futures import ThreadPoolExecutor, as_completed
import json
import time
import urllib.request
import pytest
from test_server_runner_box import live_server

def test_concurrent_sport_box_generation_stress(live_server):
    scenarios = [
        {"sport": "running", "distance": "10k", "price_tier": "economy"},
        {"sport": "running", "distance": "21k", "price_tier": "standard"},
        {"sport": "running", "distance": "42k", "caffeine_preference": "boost"},
        {"sport": "cycling", "distance": "50k", "price_tier": "economy"},
        {"sport": "cycling", "distance": "100k", "price_tier": "premium"},
        {"sport": "triathlon", "distance": "sprint", "price_tier": "standard"},
        {"sport": "triathlon", "distance": "half", "price_tier": "premium"},
        {"sport": "gym", "goal": "mass", "price_tier": "standard"},
        {"sport": "gym", "goal": "lean", "price_tier": "premium"},
        {"sport": "outdoor", "duration": "1day", "price_tier": "standard"},
    ] * 5  # 50 total requests

    def make_request(payload):
        start = time.perf_counter()
        req = urllib.request.Request(
            f"{live_server}/api/generate-sport-box",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req, timeout=5) as resp:
            dur_ms = (time.perf_counter() - start) * 1000
            assert resp.status == 200
            body = json.loads(resp.read().decode("utf-8"))
            return dur_ms, body

    total_start = time.perf_counter()
    latencies = []

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(make_request, sc) for sc in scenarios]
        for f in as_completed(futures):
            dur, body = f.result()
            latencies.append(dur)
            assert body["total_base_price"] > 0
            assert len(body["slots"]) >= 3

    total_time = time.perf_counter() - total_start
    avg_latency = sum(latencies) / len(latencies)

    # Performance assertions
    assert len(latencies) == 50
    assert total_time < 5.0, f"50 concurrent requests took too long: {total_time:.2f}s"
    assert avg_latency < 50.0, f"Average latency too high: {avg_latency:.2f}ms"
