from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

def test_runner_box_js_supports_atomic_bulk_cart():
    js_path = ROOT / "public" / "runner_box.js"
    assert js_path.exists(), "public/runner_box.js must exist"
    code = js_path.read_text(encoding="utf-8")
    
    assert "checkout/quiz_cart/add_bulk" in code, "runner_box.js must support atomic bulk add route"
    assert "addBulkProducts" in code or "items" in code
