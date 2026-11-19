import pytest
from runner_box_engine import generate_runner_box

SAMPLE_CATALOG = [
    {
        "product_id": 101, "name": "SiS GO Gel Orange", "brand": "SiS",
        "price": 95.0, "quantity": 10, "slot": "energy", "sub_type": "gel",
        "price_tier": "standard", "caffeine": False, "stomach_gentle": True,
        "distances": ["10k", "21k", "42k"]
    },
    {
        "product_id": 102, "name": "SiS GO + Caffeine Espresso", "brand": "SiS",
        "price": 95.0, "quantity": 5, "slot": "energy", "sub_type": "gel",
        "price_tier": "standard", "caffeine": True, "stomach_gentle": True,
        "distances": ["21k", "42k"]
    },
    {
        "product_id": 201, "name": "Sponser Salt Caps", "brand": "Sponser",
        "price": 120.0, "quantity": 15, "slot": "hydration", "sub_type": "salt_caps",
        "price_tier": "standard", "caffeine": False, "stomach_gentle": True,
        "distances": ["21k", "42k", "trail"]
    },
    {
        "product_id": 301, "name": "Race Expert Slim Belt", "brand": "Race Expert",
        "price": 250.0, "quantity": 100, "slot": "gear", "sub_type": "running_belt",
        "price_tier": "economy", "caffeine": False, "stomach_gentle": True,
        "distances": ["10k", "21k", "42k", "trail"]
    },
    {
        "product_id": 401, "name": "Chamois Butt'r Cream", "brand": "Chamois Butt'r",
        "price": 95.0, "quantity": 8, "slot": "care_recovery", "sub_type": "anti_chafe",
        "price_tier": "standard", "caffeine": False, "stomach_gentle": True,
        "distances": ["21k", "42k", "trail"]
    }
]

def test_zero_caffeine_guarantee():
    inputs = {
        "distance": "21k", "pace_target": "record", "weather": "moderate",
        "stomach_type": "normal", "caffeine_preference": "none",
        "body_concerns": [], "gear_needed": [], "price_tier": "standard"
    }
    box = generate_runner_box(inputs, SAMPLE_CATALOG)
    for slot_name, items in box["slots"].items():
        for it in items:
            assert it["product"]["caffeine"] is False, f"Caffeine leak in {it['product']['name']}"

def test_caffeine_boost_included_on_half_marathon():
    inputs = {
        "distance": "21k", "pace_target": "record", "weather": "moderate",
        "stomach_type": "normal", "caffeine_preference": "boost",
        "body_concerns": [], "gear_needed": [], "price_tier": "standard"
    }
    box = generate_runner_box(inputs, SAMPLE_CATALOG)
    caffeine_items = [it for it in box["slots"]["energy"] if it["product"]["caffeine"]]
    assert len(caffeine_items) >= 1, "Expected caffeine boost item for half marathon finish"

def test_hot_weather_salt_injection():
    inputs = {
        "distance": "21k", "pace_target": "steady", "weather": "hot",
        "stomach_type": "normal", "caffeine_preference": "none",
        "body_concerns": [], "gear_needed": [], "price_tier": "standard"
    }
    box = generate_runner_box(inputs, SAMPLE_CATALOG)
    sub_types = [it["product"]["sub_type"] for it in box["slots"]["hydration"]]
    assert "salt_caps" in sub_types, "Hot weather must inject salt caps"

def test_single_gel_brand_consistency():
    inputs = {
        "distance": "21k", "pace_target": "record", "weather": "moderate",
        "stomach_type": "normal", "caffeine_preference": "boost",
        "body_concerns": [], "gear_needed": [], "price_tier": "standard"
    }
    box = generate_runner_box(inputs, SAMPLE_CATALOG)
    energy_gels = [it for it in box["slots"]["energy"] if it["product"].get("sub_type") == "gel"]
    gel_brands = {it["product"].get("brand") for it in energy_gels}
    assert len(gel_brands) == 1, f"Expected single gel brand, got: {gel_brands}"
    assert list(gel_brands)[0] == "SiS"
