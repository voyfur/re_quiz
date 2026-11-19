from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

def test_opencart_controller_exists_and_contains_logic():
    controller_path = ROOT / "integrations" / "opencart" / "catalog" / "controller" / "api" / "quiz_cart.php"
    assert controller_path.exists(), "quiz_cart.php controller must exist"
    
    code = controller_path.read_text(encoding="utf-8")
    assert "ControllerApiQuizCart" in code
    assert "public function add_bulk()" in code
    assert "$this->cart->add(" in code
    assert "application/json" in code
    assert "shipping_methods" in code
    assert "payment_methods" in code
