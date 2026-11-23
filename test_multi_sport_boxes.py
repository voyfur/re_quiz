"""Test suite for Multi-Sport Box Decision Engine and API."""

import pytest
from multi_sport_engine import generate_custom_sport_box, load_catalog
from luna_box_consultant import consult_luna_for_box


@pytest.mark.parametrize("sport", ["running", "cycling", "triathlon", "gym", "outdoor"])
def test_all_catalogs_loaded_with_items(sport):
    cat = load_catalog(sport)
    assert len(cat) >= 30, f"Expected at least 30 items for {sport}, got {len(cat)}"
    for p in cat:
        assert p["quantity"] > 0, f"Product {p['name']} has quantity <= 0"
        assert p["price"] > 0, f"Product {p['name']} has price <= 0"
        assert p["slot"] in ["energy", "hydration", "gear", "care_recovery"], f"Invalid slot {p['slot']} for {p['name']}"


def test_cycling_box_generation():
    inputs = {
        "distance_format": "long",
        "weather": "hot",
        "caffeine_preference": "boost",
        "saddle_comfort": True,
        "price_tier": "standard"
    }
    box = generate_custom_sport_box("cycling", inputs)
    assert box["sport"] == "cycling"
    assert box["total_base_price"] > 0
    assert len(box["slots"]["energy"]) >= 2
    assert len(box["slots"]["hydration"]) >= 2  # Hot weather salt + isotonic
    assert len(box["slots"]["gear"]) >= 1
    assert len(box["slots"]["care_recovery"]) >= 2  # Chamois + recovery


def test_cycling_zero_caffeine_guarantee():
    inputs = {
        "distance_format": "medium",
        "weather": "moderate",
        "caffeine_preference": "none",
        "saddle_comfort": True,
        "price_tier": "standard"
    }
    box = generate_custom_sport_box("cycling", inputs)
    for s_items in box["slots"].values():
        for it in s_items:
            assert it["product"]["caffeine"] is False, f"Caffeine leak: {it['product']['name']}"


def test_triathlon_box_generation():
    inputs = {
        "format": "half",
        "wetsuit_care": True,
        "caffeine_preference": "boost",
        "price_tier": "premium"
    }
    box = generate_custom_sport_box("triathlon", inputs)
    assert box["sport"] == "triathlon"
    assert box["total_base_price"] > 0
    for slot in ["energy", "hydration", "gear", "care_recovery"]:
        assert len(box["slots"][slot]) >= 1, f"Empty slot {slot} in triathlon"


def test_gym_box_generation():
    inputs = {
        "goal": "mass",
        "pre_workout_boost": "caffeine",
        "price_tier": "standard"
    }
    box = generate_custom_sport_box("gym", inputs)
    assert box["sport"] == "gym"
    assert box["total_base_price"] > 0
    assert any("whey" in it["product"]["name"].lower() or "протеїн" in it["product"]["name"].lower() for it in box["slots"]["care_recovery"])


def test_outdoor_box_generation():
    inputs = {
        "duration": "weekend",
        "price_tier": "standard"
    }
    box = generate_custom_sport_box("outdoor", inputs)
    assert box["sport"] == "outdoor"
    assert box["total_base_price"] > 0
    # Must contain ЇDLO meals
    assert any("їdlo" in it["product"]["name"].lower() or "їдло" in it["product"]["name"].lower() for it in box["slots"]["energy"])


def test_outdoor_domain_9_weekend_full_pack():
    inputs = {
        "duration": "weekend",
        "price_tier": "standard"
    }
    box = generate_custom_sport_box("outdoor", inputs)
    # Energy meals: 2 breakfasts + 2 soups + 3 mains = 7 hot meals + 1 snack
    total_meals = sum(it["quantity_recommended"] for it in box["slots"]["energy"] if it["product"].get("sub_type") in ["breakfast_meal", "gourmet_soup", "gourmet_meal"])
    assert total_meals >= 6, f"Expected at least 6 hot meals for weekend hike, got {total_meals}"
    
    # Jerkies / snacks: at least 3 packs
    total_jerkies = sum(it["quantity_recommended"] for it in box["slots"]["care_recovery"] if it["product"].get("sub_type") == "jerky")
    total_snacks = total_jerkies + sum(it["quantity_recommended"] for it in box["slots"]["energy"] if it["product"].get("sub_type") in ["energy_snack", "energy_bar"])
    assert total_snacks >= 3, f"Expected at least 3 packs of jerkies/snacks for weekend, got {total_snacks}"
    
    # Hydration: electrolytes
    assert any(it["product"].get("sub_type") == "electrolyte_tablets" for it in box["slots"]["hydration"])
    
    # Gear: socks with sizes
    sock_item = next(it for it in box["slots"]["gear"] if it["product"].get("sub_type") == "trekking_socks")
    assert sock_item["quantity_recommended"] >= 1
    assert any(s["product_id"] == 5599 for s in sock_item["available_sizes"])


def test_outdoor_domain_10_expedition_full_pack():
    inputs = {
        "duration": "expedition",
        "price_tier": "standard"
    }
    box = generate_custom_sport_box("outdoor", inputs)
    # 4 breakfasts + 4 soups + 4 mains = 12 hot meals
    total_meals = sum(it["quantity_recommended"] for it in box["slots"]["energy"] if it["product"].get("sub_type") in ["breakfast_meal", "gourmet_soup", "gourmet_meal"])
    assert total_meals >= 8, f"Expected 8-12 hot meals for expedition, got {total_meals}"
    
    # Jerkies / snacks: 6-8 packs
    total_jerkies = sum(it["quantity_recommended"] for it in box["slots"]["care_recovery"] if it["product"].get("sub_type") == "jerky")
    total_snacks = total_jerkies + sum(it["quantity_recommended"] for it in box["slots"]["energy"] if it["product"].get("sub_type") in ["energy_snack", "energy_bar"])
    assert total_snacks >= 6, f"Expected 6-8 jerky/energy snack packs for expedition, got {total_snacks}"
    
    # 2 pairs of RE trekking socks
    sock_item = next(it for it in box["slots"]["gear"] if it["product"].get("sub_type") == "trekking_socks")
    assert sock_item["quantity_recommended"] == 2
    
    # Hydration gear: flask or bottle
    assert any(it["product"].get("sub_type") in ["soft_flask", "water_bottle"] for it in box["slots"]["gear"])
    
    # Recovery pack: magnesium 4 ampoules
    mag_item = next(it for it in box["slots"]["care_recovery"] if it["product"].get("sub_type") == "magnesium")
    assert mag_item["quantity_recommended"] == 4


def test_gym_domain_7_mass_starter_pack_1_month():
    for tier in ["economy", "standard", "premium"]:
        inputs = {
            "goal": "mass",
            "pre_workout_boost": "caffeine",
            "price_tier": tier
        }
        box = generate_custom_sport_box("gym", inputs)
        assert box["sport"] == "gym"
        assert box["total_base_price"] > 2000, f"Expected full 1-month course price > 2000 грн for {tier}, got {box['total_base_price']}"
        
        # 1. Whey protein check (at least 500g, or 1000g via qty=2)
        whey_items = [it for it in box["slots"]["care_recovery"] if it["product"].get("sub_type") in ["whey_protein", "vegan_protein"]]
        assert len(whey_items) >= 1, f"Missing whey protein in {tier} mass pack"
        
        # 2. Creatine Monohydrate check (essential for 1-month strength)
        creat_items = [it for it in box["slots"]["care_recovery"] if it["product"].get("sub_type") == "creatine"]
        assert len(creat_items) >= 1, f"Missing creatine in {tier} mass pack"
        assert creat_items[0]["quantity_recommended"] >= 1
        
        # 3. Hormone support (ZMA or Vitamin D3 or Tribulus)
        horm_items = [it for it in box["slots"]["care_recovery"] if it["product"].get("sub_type") in ["zma", "vitamins", "testosterone_booster"]]
        assert len(horm_items) >= 1, f"Missing hormone/recovery support in {tier} mass pack"
        
        # 4. Gear must be a shaker
        shaker_items = [it for it in box["slots"]["gear"] if it["product"].get("sub_type") == "shaker"]
        assert len(shaker_items) >= 1, f"Missing shaker in {tier} mass pack"
        
        # 5. Energy activation: pre-workout or multi-pack shots/bars
        energy_items = box["slots"]["energy"]
        assert len(energy_items) >= 1
        for en in energy_items:
            name_l = en["product"]["name"].lower()
            if en["product"].get("sub_type") in ["energy_shot", "protein_bar"] or ("батончик" in name_l or "шот" in name_l or "cookie" in name_l):
                assert en["quantity_recommended"] >= 4, f"Snack/shot bottleneck: qty={en['quantity_recommended']} for {en['product']['name']}"


def test_gym_domain_8_lean_cut_full_pack():
    for tier in ["economy", "standard", "premium"]:
        inputs = {
            "goal": "lean",
            "pre_workout_boost": "caffeine",
            "price_tier": tier
        }
        box = generate_custom_sport_box("gym", inputs)
        assert box["sport"] == "gym"
        assert box["total_base_price"] > 2000
        
        # 1. High-protein low-carb / Diet Whey / Isolate
        diet_items = [it for it in box["slots"]["care_recovery"] if it["product"].get("sub_type") in ["diet_whey", "whey_isolate", "whey_protein"]]
        assert len(diet_items) >= 1, f"Missing lean protein in {tier} lean cut pack"
        
        # 2. Fat burner / L-Carnitine / CLA
        fatburn_items = [it for it in box["slots"]["care_recovery"] if it["product"].get("sub_type") in ["l_carnitine", "cla", "fat_burner"]]
        assert len(fatburn_items) >= 1, f"Missing fat burner (L-Carnitine/CLA) in {tier} lean cut pack"
        
        # 3. Anti-catabolic recovery (BCAA + Glutamine/Casein)
        assert any(it["product"].get("sub_type") == "bcaa" for it in box["slots"]["hydration"]), f"Missing BCAA in hydration for {tier} lean cut pack"
        
        # 4. Gear must be a shaker
        assert any(it["product"].get("sub_type") == "shaker" for it in box["slots"]["gear"]), f"Missing shaker for {tier} lean cut pack"


def test_gym_zero_caffeine_protein_bars_pack():
    inputs = {
        "goal": "mass",
        "pre_workout_boost": "none",
        "price_tier": "standard"
    }
    box = generate_custom_sport_box("gym", inputs)
    # Zero caffeine check across all items
    for slot_items in box["slots"].values():
        for it in slot_items:
            assert it["product"]["caffeine"] is False, f"Caffeine leak in zero-caffeine gym box: {it['product']['name']}"
    
    # Must recommend multi-pack bars/cookies
    energy_item = box["slots"]["energy"][0]
    assert energy_item["quantity_recommended"] >= 4, f"Expected pack of bars, got {energy_item['quantity_recommended']}"


from unittest.mock import patch

@patch("luna_box_consultant.get_api_key", return_value=None)
def test_luna_consultation_all_sports(mock_key):
    for sport in ["cycling", "triathlon", "gym", "outdoor"]:
        inputs = {"sport": sport, "price_tier": "standard"}
        box = generate_custom_sport_box(sport, inputs)
        luna_res = consult_luna_for_box(inputs, box)
        assert luna_res["ok"] is True
        data = luna_res["data"]
        assert len(data["expert_verdict"]) > 10
        assert len(data["timeline_steps"]) >= 2
        assert len(data["pro_tip"]) > 10
