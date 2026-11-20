"""End-to-End (E2E) Browser Test using Headless Google Chrome & Puppeteer.

Drives real Chrome browser through the complete customer journey:
- Page rendering, fonts, styling
- Sport tab switching
- Custom box generation
- Interactive item checkbox deselection & DOM total price recalculation
- Bulk cart addition network request verification
"""

import subprocess
from pathlib import Path
import pytest
from test_server_runner_box import live_server

ROOT = Path(__file__).resolve().parent.parent
SCRIPT_PATH = ROOT / "tests" / "browser_e2e_test.cjs"

def test_headless_chrome_full_customer_journey(live_server):
    cmd = ["node", str(SCRIPT_PATH), live_server]
    res = subprocess.run(cmd, capture_output=True, text=True, check=False)
    
    # Print browser stdout/stderr for full audit visibility
    print("\n--- BROWSER E2E LOGS ---")
    print(res.stdout)
    if res.stderr:
        print(res.stderr)
    print("-------------------------\n")
    
    assert res.returncode == 0, f"Browser E2E failed:\n{res.stderr}\n{res.stdout}"
    assert "ALL DOM & INTERACTION CHECKS PASSED IN REAL GOOGLE CHROME!" in res.stdout
