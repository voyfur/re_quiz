"""Comprehensive Test Suite for Running and Gym Starter Box Variations.

Validates:
1. Running: 100% Single Brand Gel Rule, Zero Caffeine Leaks, Distance Pacing, Custom Budgets.
2. Gym: Mass, Lean/Cut, and Strength packs, Shaker & Protein inclusion, Zero Caffeine.
3. Cart & Checkbox Simulation: Deselection updates total price, count, and cart payload.
"""

import pytest
import json
from pathlib import Path
from runner_box_engine import generate_runner_box
from multi_sport_engine import generate_custom_sport_box, load_catalog

@pytest.fixture(scope="module")
def running_cat():
    with open("running_catalog.json", "r", encoding="utf-8") as f:
        return json.load(f)

@pytest.fixture(scope="module")
def gym_cat():
    return load_catalog("gym")


# ==========================================
# 1. RUNNING VARIATIONS & SINGLE BRAND RULE
# ==========================================

@pytest.mark.parametrize("distance", ["10k", "21k", "42k", "trail"])
@pytest.mark.parametrize("tier", ["economy", "standard", "premium"])
@pytest.mark.parametrize("caffeine", ["none", "boost"])
def test_running_single_gel_brand_rule(distance, tier, caffeine, running_cat):
    inputs = {
        "distance": distance,
        "pace_target": "record" if tier == "premium" else "steady",
        "weather": "moderate",
        "stomach_type": "normal",
        "caffeine_preference": caffeine,
        "price_tier": tier
    }
    box = generate_runner_box(inputs, running_cat)
    assert box["total_base_price"] > 0
    
    energy_gels = [it for it in box["slots"]["energy"] if it["product"].get("sub_type") == "gel"]
    assert len(energy_gels) >= 2, f"Expected at least 2 gels for {distance}, got {len(energy_gels)}"
    
    gel_brands = {it["product"]["brand"] for it in energy_gels}
    assert len(gel_brands) == 1, f"Gel brand mixing detected for {distance}/{tier}/{caffeine}: {gel_brands}"
    
    primary_brand = list(gel_brands)[0]
    assert primary_brand in ["SiS", "Nutrend", "Precision Fuel & Hydration", "GU Energy", "226ERS", "Sponser"]
    
    # Check caffeine safety
    if caffeine == "none":
        for it in energy_gels:
            assert it["product"]["caffeine"] is False, f"Caffeine leak in gel: {it['product']['name']}"
    elif caffeine == "boost":
        caff_gels = [it for it in energy_gels if it["product"]["caffeine"]]
        assert len(caff_gels) >= 1, f"Expected caffeine gel for boost in {distance}"
        assert caff_gels[0]["product"]["brand"] == primary_brand, "Caffeine boost gel must match base gel brand"


@pytest.mark.parametrize("custom_budget", [1000.0, 1500.0, 2500.0, 3500.0])
def test_running_custom_budget_optimization(custom_budget, running_cat):
    inputs = {
        "distance": "21k",
        "pace_target": "steady",
        "weather": "moderate",
        "stomach_type": "normal",
        "caffeine_preference": "boost",
        "custom_budget": custom_budget
    }
    box = generate_runner_box(inputs, running_cat)
    assert box["total_base_price"] <= custom_budget, f"Box total {box['total_base_price']} exceeds custom budget {custom_budget}"
    assert box["budget_info"]["within_budget"] is True
    
    # Brand consistency must be preserved even after budget downswap
    energy_gels = [it for it in box["slots"]["energy"] if it["product"].get("sub_type") == "gel"]
    gel_brands = {it["product"]["brand"] for it in energy_gels}
    assert len(gel_brands) == 1, f"Brand mixing after budget downswap: {gel_brands}"


def test_running_hot_weather_salt_and_chafing(running_cat):
    inputs = {
        "distance": "42k",
        "pace_target": "steady",
        "weather": "hot",
        "stomach_type": "sensitive",
        "caffeine_preference": "none",
        "body_concerns": ["cramps", "chafing"],
        "gear_needed": ["socks", "flask"],
        "price_tier": "standard"
    }
    box = generate_runner_box(inputs, running_cat)
    # Hydration must have salt
    salt_items = [it for it in box["slots"]["hydration"] if it["product"].get("sub_type") == "salt_caps"]
    assert len(salt_items) >= 1, "Hot marathon with cramps must include salt caps"
    
    # Care must have anti chafe
    chafe_items = [it for it in box["slots"]["care_recovery"] if it["product"].get("sub_type") == "anti_chafe"]
    assert len(chafe_items) >= 1, "Chafing concern must include anti-chafe cream"
    
    # Socks must have size pills
    sock_items = [it for it in box["slots"]["gear"] if it["product"].get("sub_type") == "running_socks"]
    assert len(sock_items) >= 1
    assert "available_sizes" in sock_items[0]
    assert len(sock_items[0]["available_sizes"]) >= 4


# ==========================================
# 2. GYM & FITNESS VARIATIONS
# ==========================================

@pytest.mark.parametrize("goal", ["mass", "lean", "strength"])
@pytest.mark.parametrize("tier", ["economy", "standard", "premium"])
def test_gym_goals_and_tiers(goal, tier, gym_cat):
    inputs = {
        "goal": goal,
        "pre_workout_boost": "caffeine",
        "price_tier": tier
    }
    box = generate_custom_sport_box("gym", inputs)
    assert box["sport"] == "gym"
    assert box["total_base_price"] > 1500, f"Expected 1-month course price > 1500 грн for {goal}/{tier}"
    
    # Shaker is mandatory gear in gym boxes
    shakers = [it for it in box["slots"]["gear"] if it["product"].get("sub_type") == "shaker"]
    assert len(shakers) == 1, f"Gym {goal}/{tier} must include exactly 1 shaker"
    
    # Protein is mandatory
    proteins = [it for it in box["slots"]["care_recovery"] if "protein" in it["product"].get("sub_type", "").lower() or "whey" in it["product"].get("sub_type", "").lower()]
    assert len(proteins) >= 1, f"Gym {goal}/{tier} must include whey/protein"
    
    if goal == "mass":
        creatines = [it for it in box["slots"]["care_recovery"] if it["product"].get("sub_type") == "creatine"]
        assert len(creatines) >= 1, f"Mass pack must include creatine monohydrate"
    elif goal == "lean":
        fatburners = [it for it in box["slots"]["care_recovery"] if it["product"].get("sub_type") in ["l_carnitine", "fat_burner", "cla"]]
        assert len(fatburners) >= 1, f"Lean cut pack must include L-Carnitine/fat burner"


def test_gym_zero_caffeine_guarantee(gym_cat):
    inputs = {
        "goal": "mass",
        "pre_workout_boost": "none",
        "price_tier": "standard"
    }
    box = generate_custom_sport_box("gym", inputs)
    for s_items in box["slots"].values():
        for it in s_items:
            assert it["product"]["caffeine"] is False, f"Caffeine leak in gym: {it['product']['name']}"


@pytest.mark.parametrize("custom_budget", [2500.0, 3500.0, 5000.0])
def test_gym_custom_budget_optimization(custom_budget, gym_cat):
    inputs = {
        "goal": "mass",
        "pre_workout_boost": "caffeine",
        "custom_budget": custom_budget
    }
    box = generate_custom_sport_box("gym", inputs)
    assert box["total_base_price"] <= custom_budget, f"Gym box total {box['total_base_price']} exceeds custom budget {custom_budget}"


# ==========================================
# 3. CART & CHECKBOX DESELECTION SIMULATION
# ==========================================

def test_item_deselection_logic(running_cat):
    # Simulate user generating a 21k running box
    inputs = {
        "distance": "21k",
        "pace_target": "steady",
        "weather": "moderate",
        "stomach_type": "normal",
        "caffeine_preference": "boost",
        "body_concerns": ["chafing"],
        "gear_needed": ["belt"],
        "price_tier": "standard"
    }
    box = generate_runner_box(inputs, running_cat)
    all_items = []
    for slot_name in ["energy", "hydration", "gear", "care_recovery"]:
        for idx, it in enumerate(box["slots"].get(slot_name, [])):
            all_items.append((f"{slot_name}_{idx}", it))
    
    total_original_price = sum(it["product"]["price"] * it["quantity_recommended"] for _, it in all_items)
    assert round(total_original_price, 2) == round(box["total_base_price"], 2)
    
    # User deselects gear (belt) and care (cream) because they already have them at home
    selected_items_map = {}
    for key, it in all_items:
        if "gear" in key or "care_recovery" in key:
            selected_items_map[key] = False  # UNCHECKED
        else:
            selected_items_map[key] = True   # CHECKED
            
    # Calculate cart payload
    cart_items = []
    cart_total_price = 0.0
    for key, it in all_items:
        if selected_items_map[key]:
            cart_items.append({
                "productId": it["product"]["product_id"],
                "quantity": it["quantity_recommended"],
                "price": it["product"]["price"]
            })
            cart_total_price += it["product"]["price"] * it["quantity_recommended"]
            
    assert len(cart_items) < len(all_items)
    assert cart_total_price < total_original_price
    # Verify no gear or care items entered the cart
    for item in cart_items:
        prod_id = item["productId"]
        prod_slot = next(p["slot"] for p in running_cat if p["product_id"] == prod_id)
        assert prod_slot in ["energy", "hydration"], f"Deselected slot item entered cart: {prod_slot}"
