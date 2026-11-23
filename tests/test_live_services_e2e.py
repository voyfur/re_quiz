"""Live End-to-End Test Suite against REAL External Services (MySQL & OpenAI).

Verifies real-world connectivity, data integrity, and pipeline execution:
1. Real OpenCart MySQL Database queries via SSH tunnel to VPS-61125.
2. Real OpenAI GPT-4o-mini API calls for Luna sports nutrition consultation.
3. Complete HTTP Server journey combining live stock checks, box generation,
   and live AI consultation.
"""

import json
import urllib.request
from pathlib import Path
import pytest
from stock_checker import check_stock, get_stock_checker
from luna_box_consultant import get_api_key, consult_luna_for_box
from test_server_runner_box import live_server


def test_real_opencart_mysql_live_stock_verification():
    """Verify physical database connection to OpenCart MySQL (raceexpertcomua)."""
    skus = ["RE89450", "RE89445", "UNKNOWN_SKU_XYZ"]
    res = check_stock(skus)
    
    assert isinstance(res, dict)
    assert "RE89450" in res
    assert "RE89445" in res
    assert "UNKNOWN_SKU_XYZ" in res

    # Known live products in OpenCart
    p1 = res["RE89450"]
    assert p1["is_live_check"] is True, "Must be verified against real MySQL"
    assert p1["product_id"] == 7149
    assert p1["status"] == 1
    assert p1["quantity"] > 0
    assert p1["live_price_uah"] > 0
    assert p1["in_stock"] is True
    assert p1["stock_status_text_uk"] == "В наявності"

    p2 = res["RE89445"]
    assert p2["is_live_check"] is True
    assert p2["product_id"] == 7326
    assert p2["quantity"] > 0
    assert p2["live_price_uah"] > 0
    assert p2["in_stock"] is True

    # Unknown product
    p3 = res["UNKNOWN_SKU_XYZ"]
    assert p3["is_live_check"] is True
    assert p3["in_stock"] is False
    assert p3["quantity"] == 0
    assert p3["product_id"] is None
    assert p3["stock_status_text_uk"] == "Товар не знайдено"


def test_real_openai_gpt_luna_consultation():
    """Verify live OpenAI API call using the production key from .env."""
    key = get_api_key()
    assert key is not None and key.startswith("sk-"), "OpenAI API key must be present in .env"

    inputs = {
        "sport": "running",
        "distance": "42k",
        "pace_target": "sub330",
        "weather": "hot",
        "caffeine_preference": "boost"
    }
    box = {
        "sport": "running",
        "sport_label": "Біг",
        "distance_label": "Марафон (42.2 км)",
        "box_title": "Марафонський стартовий бокс",
        "total_base_price": 2850,
        "slots": {
            "energy": [
                {"product": {"name": "SiS GO Isotonic Energy Gel", "caffeine": False}, "quantity_recommended": 4, "reason_badge": "Базова енергія"},
                {"product": {"name": "SiS GO + Caffeine Gel", "caffeine": True}, "quantity_recommended": 2, "reason_badge": "Кофеїновий буст на 32 км"}
            ],
            "hydration": [
                {"product": {"name": "SaltStick Electrolyte Caps", "caffeine": False}, "quantity_recommended": 1, "reason_badge": "Сольовий баланс"}
            ]
        }
    }

    res = consult_luna_for_box(inputs, box, locale="uk")
    assert res["ok"] is True
    assert res["source"] == "openai_luna", f"Expected live OpenAI response, got {res.get('source')}"

    data = res["data"]
    assert "expert_verdict" in data and len(data["expert_verdict"]) > 20
    assert "tactical_strategy" in data and len(data["tactical_strategy"]) > 50
    assert "timeline_steps" in data and isinstance(data["timeline_steps"], list)
    assert len(data["timeline_steps"]) >= 2
    assert "safety_badge" in data and len(data["safety_badge"]) > 5
    assert "pro_tip" in data and len(data["pro_tip"]) > 10

    # Strict Ukrainian language verification: ensure NO Russian characters leak
    full_text = json.dumps(data, ensure_ascii=False)
    assert not any(c in full_text for c in "ыЫэЭъЪёЁ"), f"Russian characters found in Luna response: {full_text}"


def test_live_server_full_pipeline_with_real_services(live_server):
    """End-to-end integration journey on HTTP server using both live MySQL and live OpenAI."""
    # 1. Check live stock for real SKUs via HTTP POST /api/check-stock
    stock_payload = {"skus": ["RE89450", "RE89445"]}
    req_stock = urllib.request.Request(
        f"{live_server}/api/check-stock",
        data=json.dumps(stock_payload).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req_stock, timeout=10) as resp:
        assert resp.status == 200
        stock_data = json.loads(resp.read().decode("utf-8"))
        assert stock_data["ok"] is True
        assert stock_data["stocks"]["RE89450"]["in_stock"] is True
        assert stock_data["stocks"]["RE89450"]["live_price_uah"] > 0
        assert stock_data["stocks"]["RE89450"]["is_live_check"] is True

    # 2. Generate a custom triathlon box via HTTP POST /api/generate-sport-box
    tri_payload = {
        "sport": "triathlon",
        "format": "half",
        "caffeine_preference": "boost",
        "wetsuit_care": True,
        "price_tier": "standard"
    }
    req_box = urllib.request.Request(
        f"{live_server}/api/generate-sport-box",
        data=json.dumps(tri_payload).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req_box, timeout=8) as resp:
        assert resp.status == 200
        box = json.loads(resp.read().decode("utf-8"))
        assert box["sport"] == "triathlon"
        assert box["total_base_price"] > 0

    # 3. Call live Luna AI consultant via HTTP POST /api/luna-consult-box
    luna_payload = {
        "user_inputs": tri_payload,
        "generated_box": box,
        "locale": "uk"
    }
    req_luna = urllib.request.Request(
        f"{live_server}/api/luna-consult-box",
        data=json.dumps(luna_payload).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req_luna, timeout=15) as resp:
        assert resp.status == 200
        luna_res = json.loads(resp.read().decode("utf-8"))
        assert luna_res["ok"] is True
        assert luna_res["source"] == "openai_luna"
        assert len(luna_res["data"]["timeline_steps"]) >= 2
        content_lower = str(luna_res["data"]).lower()
        assert any(k in content_lower for k in ["триатл", "half-ironman", "змагань", "плаван", "вело", "гель"])
