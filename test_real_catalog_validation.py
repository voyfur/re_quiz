import json
from pathlib import Path
import pytest
from runner_box_engine import generate_runner_box

@pytest.fixture
def real_catalog():
    path = Path("running_catalog.json")
    assert path.exists(), "running_catalog.json must exist"
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def test_real_catalog_has_all_slots(real_catalog):
    slots = {p["slot"] for p in real_catalog}
    expected_slots = {"energy", "hydration", "gear", "care_recovery"}
    assert expected_slots.issubset(slots), f"Missing slots in catalog: {expected_slots - slots}"

def test_real_catalog_all_quantities_positive(real_catalog):
    for p in real_catalog:
        assert p["quantity"] > 0, f"Product {p['name']} has zero quantity"
        assert p["price"] > 0, f"Product {p['name']} has invalid price"

def test_full_marathon_box_generation_on_real_catalog(real_catalog):
    inputs = {
        "distance": "42k",
        "pace_target": "record",
        "weather": "hot",
        "stomach_type": "sensitive",
        "caffeine_preference": "boost",
        "body_concerns": ["cramps", "chafing"],
        "gear_needed": ["belt", "flask"],
        "price_tier": "premium"
    }
    box = generate_runner_box(inputs, real_catalog)
    assert box["total_base_price"] > 0
    assert len(box["slots"]["energy"]) >= 1
    assert len(box["slots"]["hydration"]) >= 1
    assert len(box["slots"]["gear"]) >= 1
    assert len(box["slots"]["care_recovery"]) >= 1

def test_socks_sizing_and_gear_selection(real_catalog):
    inputs = {
        "distance": "21k",
        "pace_target": "steady",
        "weather": "moderate",
        "stomach_type": "normal",
        "caffeine_preference": "none",
        "body_concerns": ["joints"],
        "gear_needed": ["socks", "belt"],
        "price_tier": "standard"
    }
    box = generate_runner_box(inputs, real_catalog)
    gear_items = box["slots"]["gear"]
    sub_types = [it["product"]["sub_type"] for it in gear_items]
    assert "running_socks" in sub_types
    socks_item = next(it for it in gear_items if it["product"]["sub_type"] == "running_socks")
    assert "available_sizes" in socks_item
    sizes = [s["size"] for s in socks_item["available_sizes"]]
    assert "38-40" in sizes
    assert "40-42" in sizes

def test_vegan_guarantee_on_real_catalog(real_catalog):
    inputs = {
        "distance": "42k",
        "pace_target": "record",
        "weather": "moderate",
        "stomach_type": "vegan",
        "caffeine_preference": "none",
        "body_concerns": [],
        "gear_needed": [],
        "price_tier": "standard"
    }
    box = generate_runner_box(inputs, real_catalog)
    for slot_name, items in box["slots"].items():
        for it in items:
            assert it["product"].get("is_vegan", True) is True, f"Non-vegan item found: {it['product']['name']}"
