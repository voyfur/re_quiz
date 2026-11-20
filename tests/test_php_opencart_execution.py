"""Tests OpenCart PHP controller quiz_cart.php execution inside real PHP 8.2 runtime via Docker.

Ensures the controller executes without fatal errors, correctly invokes $this->cart->add(),
clears shipping/payment caches in $this->session, and returns expected JSON responses.
"""

import subprocess
from pathlib import Path
import pytest

ROOT = Path(__file__).resolve().parent.parent
CONTROLLER_PATH = ROOT / "integrations" / "opencart" / "catalog" / "controller" / "checkout" / "quiz_cart.php"
FIXTURE_PATH = ROOT / "tests" / "fixtures" / "run_cart_test.php"

def test_php_syntax_lint():
    res = subprocess.run([
        "docker", "run", "--rm",
        "-v", f"{ROOT}/integrations/opencart:/app",
        "php:8.2-alpine",
        "php", "-l", "/app/catalog/controller/checkout/quiz_cart.php"
    ], capture_output=True, text=True, check=False)
    assert res.returncode == 0, f"PHP Lint Failed: {res.stderr}\n{res.stdout}"
    assert "No syntax errors detected" in res.stdout

def test_php_add_bulk_valid_execution():
    cmd = [
        "docker", "run", "--rm",
        "-v", f"{ROOT}/integrations/opencart:/app",
        "-v", f"{FIXTURE_PATH}:/test/run_cart_test.php:ro",
        "php:8.2-alpine",
        "php", "/test/run_cart_test.php", "valid"
    ]
    res = subprocess.run(cmd, capture_output=True, text=True, check=False)
    assert res.returncode == 0, f"PHP execution failed: {res.stderr}\n{res.stdout}"
    assert "OK_VALID" in res.stdout

def test_php_add_bulk_invalid_ids_execution():
    cmd = [
        "docker", "run", "--rm",
        "-v", f"{ROOT}/integrations/opencart:/app",
        "-v", f"{FIXTURE_PATH}:/test/run_cart_test.php:ro",
        "php:8.2-alpine",
        "php", "/test/run_cart_test.php", "invalid_ids"
    ]
    res = subprocess.run(cmd, capture_output=True, text=True, check=False)
    assert res.returncode == 0, f"PHP execution failed: {res.stderr}\n{res.stdout}"
    assert "OK_INVALID_DETECTED" in res.stdout

def test_php_add_bulk_empty_payload_execution():
    cmd = [
        "docker", "run", "--rm",
        "-v", f"{ROOT}/integrations/opencart:/app",
        "-v", f"{FIXTURE_PATH}:/test/run_cart_test.php:ro",
        "php:8.2-alpine",
        "php", "/test/run_cart_test.php", "empty_payload"
    ]
    res = subprocess.run(cmd, capture_output=True, text=True, check=False)
    assert res.returncode == 0, f"PHP execution failed: {res.stderr}\n{res.stdout}"
    assert "OK_EMPTY_DETECTED" in res.stdout
