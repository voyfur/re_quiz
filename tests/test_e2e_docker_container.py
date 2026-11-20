"""End-to-End (E2E) Test Suite: Production Docker Image Build and Live Container Execution.

Validates that:
1. Dockerfile builds cleanly into an image.
2. Container starts up, exposes port, and responds to /api/health.
3. Live requests against containerized application succeed.
4. Clean container shutdown.
"""

import json
import socket
import subprocess
import time
import urllib.request
import urllib.error
from pathlib import Path
import pytest

ROOT = Path(__file__).resolve().parent.parent
IMAGE_TAG = "raceexpert-quiz:e2e-test"
CONTAINER_NAME = "raceexpert-quiz-e2e-runner"
HOST_PORT = 8099

def get_free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("", 0))
        return s.getsockname()[1]

@pytest.fixture(scope="module")
def docker_live_container():
    port = get_free_port()

    # Clean any leftover test container
    subprocess.run(["docker", "rm", "-f", CONTAINER_NAME], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # 1. Build image
    build_cmd = ["docker", "build", "-t", IMAGE_TAG, str(ROOT)]
    build_res = subprocess.run(build_cmd, capture_output=True, text=True, check=False)
    assert build_res.returncode == 0, f"Docker build failed:\n{build_res.stderr}\n{build_res.stdout}"

    # 2. Run container
    run_cmd = [
        "docker", "run", "-d",
        "--name", CONTAINER_NAME,
        "-p", f"127.0.0.1:{port}:8000",
        "-e", "PORT=8000",
        IMAGE_TAG
    ]
    run_res = subprocess.run(run_cmd, capture_output=True, text=True, check=False)
    assert run_res.returncode == 0, f"Docker run failed:\n{run_res.stderr}"

    # 3. Wait for container to be ready
    base_url = f"http://127.0.0.1:{port}"
    ready = False
    for _ in range(20):
        try:
            req = urllib.request.Request(f"{base_url}/api/health")
            with urllib.request.urlopen(req, timeout=1) as resp:
                if resp.status == 200:
                    ready = True
                    break
        except Exception:
            time.sleep(0.5)

    if not ready:
        logs = subprocess.run(["docker", "logs", CONTAINER_NAME], capture_output=True, text=True).stdout
        subprocess.run(["docker", "rm", "-f", CONTAINER_NAME], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        pytest.fail(f"Container failed to respond within 10s. Logs:\n{logs}")

    yield base_url

    # Cleanup container
    subprocess.run(["docker", "rm", "-f", CONTAINER_NAME], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def test_docker_container_e2e_healthcheck(docker_live_container):
    req = urllib.request.Request(f"{docker_live_container}/api/health")
    with urllib.request.urlopen(req, timeout=5) as resp:
        assert resp.status == 200
        data = json.loads(resp.read().decode("utf-8"))
        assert data["status"] == "ok"
        assert data["running_catalog_count"] >= 400

def test_docker_container_e2e_serves_html_and_js(docker_live_container):
    # Fetch root
    with urllib.request.urlopen(f"{docker_live_container}/", timeout=5) as resp:
        assert resp.status == 200
        body = resp.read().decode("utf-8")
        assert "Race Expert" in body

    # Fetch JS
    with urllib.request.urlopen(f"{docker_live_container}/runner_box.js", timeout=5) as resp:
        assert resp.status == 200
        js = resp.read().decode("utf-8")
        assert "SPORT_SLOT_META" in js

def test_docker_container_e2e_generate_box(docker_live_container):
    payload = {
        "sport": "cycling",
        "distance": "100k",
        "weather": "moderate",
        "gear_needed": ["bottle"],
        "price_tier": "standard"
    }
    req = urllib.request.Request(
        f"{docker_live_container}/api/generate-sport-box",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=5) as resp:
        assert resp.status == 200
        box = json.loads(resp.read().decode("utf-8"))
        assert box.get("sport_label") == "Велоспорт" or box.get("sport") == "cycling"
        assert box["total_base_price"] > 0
        assert len(box["slots"]) >= 3
