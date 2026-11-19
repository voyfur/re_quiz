from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

def test_opencart_controller_exists_and_uses_customer_session_route():
    # Must be in checkout/ controller so OpenCart binds customer's OCSESSID cookie
    # (routes with 'api/' ignore buyer cookie sessions in OpenCart 2.x/3.x)
    controller_path = ROOT / "integrations" / "opencart" / "catalog" / "controller" / "checkout" / "quiz_cart.php"
    assert controller_path.exists(), "checkout/quiz_cart.php controller must exist"
    
    code = controller_path.read_text(encoding="utf-8")
    assert "ControllerCheckoutQuizCart" in code
    assert "public function add_bulk()" in code
    assert "$this->cart->add(" in code
    assert "application/json" in code
    assert "shipping_methods" in code
    assert "payment_methods" in code
