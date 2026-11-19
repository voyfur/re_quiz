"""Comprehensive 50-Scenario Test Suite for Triathlon Category in Race Expert Starter Box Generator.

Validates 50 diverse triathlon personas across:
- Formats: 'sprint', 'half', 'full'
- Wetsuit care / Open water concern: True vs False
- Caffeine preferences: 'none' (strict zero-caffeine guarantee) vs 'boost'
- Price tiers: 'economy', 'standard', 'premium'
- Custom budgets: 1200 to 10000 грн
- Item deselection & Cart simulation: verifies deselected items, updated cart total, and payload.
- Domain validations: Multi-stage nutrition, non-empty slots, stock & pricing, gear & recovery rules.
"""

import pytest
from multi_sport_engine import generate_triathlon_box, generate_custom_sport_box, load_catalog

CATALOG = load_catalog("triathlon")

TRIATHLON_SCENARIOS = [
    # =========================================================================
    # SPRINT & OLYMPIC DISTANCE SCENARIOS (IDs 1 - 17)
    # =========================================================================
    {
        "id": 1,
        "name": "Sprint Debutant (First Triathlon, Economy Tier, Caffeine Boost)",
        "inputs": {"format": "sprint", "wetsuit_care": True, "caffeine_preference": "boost", "price_tier": "economy"}
    },
    {
        "id": 2,
        "name": "Sprint Zero Caffeine Standard (Strict GI Safety, Standard Tier)",
        "inputs": {"format": "sprint", "wetsuit_care": True, "caffeine_preference": "none", "price_tier": "standard"}
    },
    {
        "id": 3,
        "name": "Olympic Distance PB Chaser (Premium Maurten / PF Hydrogels, Boost)",
        "inputs": {"format": "sprint", "wetsuit_care": True, "caffeine_preference": "boost", "price_tier": "premium"}
    },
    {
        "id": 4,
        "name": "Sprint Pool-based Triathlon (No Wetsuit Care, Economy Tier)",
        "inputs": {"format": "sprint", "wetsuit_care": False, "caffeine_preference": "none", "price_tier": "economy"}
    },
    {
        "id": 5,
        "name": "Sprint Deselect Race Belt (Owns Race Belt, Standard Tier)",
        "inputs": {"format": "sprint", "wetsuit_care": True, "caffeine_preference": "boost", "price_tier": "standard"},
        "deselect": ["race_number_belt"]
    },
    {
        "id": 6,
        "name": "Olympic Sensitive Stomach (No Caffeine, Standard Tier)",
        "inputs": {"format": "sprint", "wetsuit_care": True, "caffeine_preference": "none", "price_tier": "standard"}
    },
    {
        "id": 7,
        "name": "Sprint Fast & Light (Caffeine Boost, No Wetsuit Care)",
        "inputs": {"format": "sprint", "wetsuit_care": False, "caffeine_preference": "boost", "price_tier": "standard"}
    },
    {
        "id": 8,
        "name": "Olympic Elite Age-Grouper (Premium Tier, Zero Caffeine)",
        "inputs": {"format": "sprint", "wetsuit_care": True, "caffeine_preference": "none", "price_tier": "premium"}
    },
    {
        "id": 9,
        "name": "Sprint Custom Budget 1800 грн (Wetsuit Care, Boost)",
        "inputs": {"format": "sprint", "wetsuit_care": True, "caffeine_preference": "boost", "custom_budget": 1800}
    },
    {
        "id": 10,
        "name": "Sprint Custom Budget 2000 грн (Zero Caffeine)",
        "inputs": {"format": "sprint", "wetsuit_care": True, "caffeine_preference": "none", "custom_budget": 2000}
    },
    {
        "id": 11,
        "name": "Sprint Custom Budget 2500 грн (Standard Tier, Boost)",
        "inputs": {"format": "sprint", "wetsuit_care": True, "caffeine_preference": "boost", "custom_budget": 2500}
    },
    {
        "id": 12,
        "name": "Sprint Deselect TRISWIM (Already Stocked, Target Budget 1500 грн)",
        "inputs": {"format": "sprint", "wetsuit_care": True, "caffeine_preference": "boost", "price_tier": "economy"},
        "deselect": ["anti_chlorine"],
        "custom_budget_target": 1500
    },
    {
        "id": 13,
        "name": "Sprint High Budget 3000 грн (Premium Nutrition & Gear)",
        "inputs": {"format": "sprint", "wetsuit_care": True, "caffeine_preference": "boost", "custom_budget": 3000}
    },
    {
        "id": 14,
        "name": "Olympic Distance Warm Lake (No Wetsuit Care, Custom Budget 1500 грн)",
        "inputs": {"format": "sprint", "wetsuit_care": False, "caffeine_preference": "boost", "custom_budget": 1500}
    },
    {
        "id": 15,
        "name": "Olympic Distance Deselect Recovery (Has Powder at Home)",
        "inputs": {"format": "sprint", "wetsuit_care": True, "caffeine_preference": "boost", "price_tier": "standard"},
        "deselect": ["recovery_drink"]
    },
    {
        "id": 16,
        "name": "Sprint Zero Caffeine + No Wetsuit Care (Strict Budget 1200 грн)",
        "inputs": {"format": "sprint", "wetsuit_care": False, "caffeine_preference": "none", "custom_budget": 1200}
    },
    {
        "id": 17,
        "name": "Olympic Distance Master AG (Premium Tier, Wetsuit Care, Boost)",
        "inputs": {"format": "sprint", "wetsuit_care": True, "caffeine_preference": "boost", "price_tier": "premium"}
    },

    # =========================================================================
    # HALF IRONMAN 70.3 SCENARIOS (IDs 18 - 34)
    # =========================================================================
    {
        "id": 18,
        "name": "70.3 First Timer (Standard Tier, Wetsuit Care, Caffeine Boost)",
        "inputs": {"format": "half", "wetsuit_care": True, "caffeine_preference": "boost", "price_tier": "standard"}
    },
    {
        "id": 19,
        "name": "70.3 Zero Caffeine Racer (Strict Stomach Safety, Standard Tier)",
        "inputs": {"format": "half", "wetsuit_care": True, "caffeine_preference": "none", "price_tier": "standard"}
    },
    {
        "id": 20,
        "name": "70.3 World Championship Qualifier (Premium Maurten / PF, Boost)",
        "inputs": {"format": "half", "wetsuit_care": True, "caffeine_preference": "boost", "price_tier": "premium"}
    },
    {
        "id": 21,
        "name": "70.3 Economy Budget (No Wetsuit Care, Finish Focus)",
        "inputs": {"format": "half", "wetsuit_care": False, "caffeine_preference": "none", "price_tier": "economy"}
    },
    {
        "id": 22,
        "name": "70.3 Hot Weather Half (Electrolyte & Salt Priority, Boost)",
        "inputs": {"format": "half", "wetsuit_care": True, "caffeine_preference": "boost", "price_tier": "standard"}
    },
    {
        "id": 23,
        "name": "70.3 Deselect Race Belt (Owns Custom Belt, Standard Tier)",
        "inputs": {"format": "half", "wetsuit_care": True, "caffeine_preference": "boost", "price_tier": "standard"},
        "deselect": ["race_number_belt"]
    },
    {
        "id": 24,
        "name": "70.3 Deselect TRISWIM & Chamois Cream (Stocked at Home, Standard)",
        "inputs": {"format": "half", "wetsuit_care": True, "caffeine_preference": "none", "price_tier": "standard"},
        "deselect": ["anti_chlorine", "anti_chafe"]
    },
    {
        "id": 25,
        "name": "70.3 Custom Budget 2000 грн (Economy Transition Fuel, Zero Caffeine)",
        "inputs": {"format": "half", "wetsuit_care": True, "caffeine_preference": "none", "custom_budget": 2000}
    },
    {
        "id": 26,
        "name": "70.3 Custom Budget 2200 грн (Standard Fuel, Caffeine Boost)",
        "inputs": {"format": "half", "wetsuit_care": True, "caffeine_preference": "boost", "custom_budget": 2200}
    },
    {
        "id": 27,
        "name": "70.3 Custom Budget 2500 грн (Balanced Multi-Stage Fuel)",
        "inputs": {"format": "half", "wetsuit_care": True, "caffeine_preference": "boost", "custom_budget": 2500}
    },
    {
        "id": 28,
        "name": "70.3 Custom Budget 3000 грн (Standard Tier, Zero Caffeine)",
        "inputs": {"format": "half", "wetsuit_care": True, "caffeine_preference": "none", "custom_budget": 3000}
    },
    {
        "id": 29,
        "name": "70.3 Custom Budget 3500 грн (Standard Multi-Stage, Boost)",
        "inputs": {"format": "half", "wetsuit_care": True, "caffeine_preference": "boost", "custom_budget": 3500}
    },
    {
        "id": 30,
        "name": "70.3 Custom Budget 4000 грн (Premium Transition Nutrition)",
        "inputs": {"format": "half", "wetsuit_care": True, "caffeine_preference": "boost", "custom_budget": 4000}
    },
    {
        "id": 31,
        "name": "70.3 Custom Budget 5000 грн (Elite Setup, Boost)",
        "inputs": {"format": "half", "wetsuit_care": True, "caffeine_preference": "boost", "custom_budget": 5000}
    },
    {
        "id": 32,
        "name": "70.3 Mediterranean Salt Water Race (Heavy Wetsuit Care, Premium)",
        "inputs": {"format": "half", "wetsuit_care": True, "caffeine_preference": "boost", "price_tier": "premium"}
    },
    {
        "id": 33,
        "name": "70.3 Rolling Hills Bike Leg (High Chew Demand, Zero Caffeine)",
        "inputs": {"format": "half", "wetsuit_care": True, "caffeine_preference": "none", "price_tier": "standard"}
    },
    {
        "id": 34,
        "name": "70.3 Deselect Belt & Recovery Drink (Nutrition-Only Reorder)",
        "inputs": {"format": "half", "wetsuit_care": True, "caffeine_preference": "boost", "price_tier": "standard"},
        "deselect": ["race_number_belt", "recovery_drink"]
    },

    # =========================================================================
    # FULL IRONMAN 140.6 SCENARIOS (IDs 35 - 50)
    # =========================================================================
    {
        "id": 35,
        "name": "140.6 Ironman Debut (Standard Tier, Wetsuit Care, Boost)",
        "inputs": {"format": "full", "wetsuit_care": True, "caffeine_preference": "boost", "price_tier": "standard"}
    },
    {
        "id": 36,
        "name": "140.6 Pure Endurance (Strict Zero Caffeine, Standard Tier)",
        "inputs": {"format": "full", "wetsuit_care": True, "caffeine_preference": "none", "price_tier": "standard"}
    },
    {
        "id": 37,
        "name": "140.6 Sub-10h Chaser (Premium Beta Fuel + Maurten, Boost)",
        "inputs": {"format": "full", "wetsuit_care": True, "caffeine_preference": "boost", "price_tier": "premium"}
    },
    {
        "id": 38,
        "name": "140.6 Economy Budget Warrior (Zero Caffeine, Economy Tier)",
        "inputs": {"format": "full", "wetsuit_care": True, "caffeine_preference": "none", "price_tier": "economy"}
    },
    {
        "id": 39,
        "name": "140.6 Non-Wetsuit Ocean Race (Cozumel / Kona, Wetsuit Care False)",
        "inputs": {"format": "full", "wetsuit_care": False, "caffeine_preference": "boost", "price_tier": "standard"}
    },
    {
        "id": 40,
        "name": "140.6 High-Carb Bike Fuel (80-90g/hr, Custom Budget 3000 грн)",
        "inputs": {"format": "full", "wetsuit_care": True, "caffeine_preference": "boost", "custom_budget": 3000}
    },
    {
        "id": 41,
        "name": "140.6 Custom Budget 2500 грн (Budget-Optimized Ironman)",
        "inputs": {"format": "full", "wetsuit_care": True, "caffeine_preference": "none", "custom_budget": 2500}
    },
    {
        "id": 42,
        "name": "140.6 Custom Budget 3500 грн (Standard Multi-Stage, Boost)",
        "inputs": {"format": "full", "wetsuit_care": True, "caffeine_preference": "boost", "custom_budget": 3500}
    },
    {
        "id": 43,
        "name": "140.6 Custom Budget 4000 грн (High-Carb Drink Mix + Gels)",
        "inputs": {"format": "full", "wetsuit_care": True, "caffeine_preference": "boost", "custom_budget": 4000}
    },
    {
        "id": 44,
        "name": "140.6 Custom Budget 5000 грн (Zero Caffeine Ultra Endurance)",
        "inputs": {"format": "full", "wetsuit_care": True, "caffeine_preference": "none", "custom_budget": 5000}
    },
    {
        "id": 45,
        "name": "140.6 Custom Budget 6500 грн (Premium Pro Ironman Package)",
        "inputs": {"format": "full", "wetsuit_care": True, "caffeine_preference": "boost", "custom_budget": 6500}
    },
    {
        "id": 46,
        "name": "140.6 Deselect Flask (Owns Hydration Flasks, Standard Tier)",
        "inputs": {"format": "full", "wetsuit_care": True, "caffeine_preference": "boost", "price_tier": "standard"},
        "deselect": ["flasks"]
    },
    {
        "id": 47,
        "name": "140.6 Deselect Belt & Flask (Owns All Race Gear, Premium Tier)",
        "inputs": {"format": "full", "wetsuit_care": True, "caffeine_preference": "boost", "price_tier": "premium"},
        "deselect": ["race_number_belt", "flasks"]
    },
    {
        "id": 48,
        "name": "140.6 Severe Chafing Risk (Wetsuit Care + Anti-Chafe, Boost)",
        "inputs": {"format": "full", "wetsuit_care": True, "caffeine_preference": "boost", "price_tier": "standard"}
    },
    {
        "id": 49,
        "name": "140.6 Deselect TRISWIM & Recovery Shake (Care Stocked at Home)",
        "inputs": {"format": "full", "wetsuit_care": True, "caffeine_preference": "none", "price_tier": "standard"},
        "deselect": ["anti_chlorine", "recovery_drink", "recovery_shake"]
    },
    {
        "id": 50,
        "name": "140.6 Ultimate PRO Ironman Package (Custom Budget 8000 грн, Boost)",
        "inputs": {"format": "full", "wetsuit_care": True, "caffeine_preference": "boost", "custom_budget": 8000}
    }
]


@pytest.mark.parametrize("scenario", TRIATHLON_SCENARIOS, ids=lambda s: f"Scenario_{s['id']:02d}_{s['name'][:35]}")
def test_triathlon_persona_scenario(scenario):
    """Verifies that each triathlon scenario produces a valid, compliant starter box."""
    inputs = scenario["inputs"]
    fmt = inputs.get("format", "half")
    caff_pref = inputs.get("caffeine_preference", "boost")
    wetsuit_care = inputs.get("wetsuit_care", True)
    custom_budget = inputs.get("custom_budget")
    deselect = scenario.get("deselect", [])

    # Generate starter box using multi_sport_engine
    box = generate_custom_sport_box("triathlon", inputs)

    # 1. Sport & Title checks
    assert box["sport"] == "triathlon"
    assert "триатлон" in box["sport_label"].lower() or "плавання" in box["sport_label"].lower()
    assert box["total_base_price"] > 0

    # 2. No empty slots
    required_slots = ["energy", "hydration", "gear", "care_recovery"]
    for slot in required_slots:
        assert slot in box["slots"], f"Slot {slot} missing in output"
        assert len(box["slots"][slot]) >= 1, f"Empty slot {slot} in scenario {scenario['id']}"

    # 3. Stock & Pricing validation across all recommended items
    all_recommended_items = []
    for slot_name, items in box["slots"].items():
        for it in items:
            p = it["product"]
            qty = it["quantity_recommended"]
            assert p["quantity"] > 0, f"Out of stock product: {p['name']}"
            assert p["price"] > 0, f"Invalid price for: {p['name']}"
            assert qty > 0, f"Invalid recommended quantity for: {p['name']}"
            all_recommended_items.append(it)

    # 4. Total base price accuracy
    computed_total = sum(it["product"]["price"] * it["quantity_recommended"] for it in all_recommended_items)
    assert round(computed_total, 2) == round(box["total_base_price"], 2)

    # 5. Budget Constraints
    if custom_budget:
        assert box["total_base_price"] <= custom_budget, (
            f"Box total ({box['total_base_price']}) exceeds custom budget ({custom_budget})"
        )
        assert box["budget_info"]["within_budget"] is True

    # 6. Zero Caffeine Guarantee
    if caff_pref == "none":
        for it in all_recommended_items:
            assert it["product"].get("caffeine") is False, (
                f"Caffeine leak found for zero-caffeine persona: {it['product']['name']}"
            )

    # 7. Caffeine Boost Requirement
    if caff_pref == "boost":
        caff_items = [it for it in box["slots"]["energy"] if it["product"].get("caffeine") is True]
        assert len(caff_items) >= 1, (
            f"Scenario {scenario['id']}: Expected caffeine boost item in energy slot"
        )

    # 8. Wetsuit / Open Water Care
    if wetsuit_care:
        triswim_items = [
            it for it in box["slots"]["care_recovery"]
            if "triswim" in it["product"]["name"].lower() or it["product"].get("sub_type") == "anti_chlorine"
        ]
        assert len(triswim_items) >= 1, (
            f"Scenario {scenario['id']}: Expected TRISWIM care product in care_recovery"
        )

    # 9. Gear Slot Validation
    gear_items = box["slots"]["gear"]
    assert any(
        it["product"].get("sub_type") in ["race_number_belt", "flasks", "belt", "flask"]
        or "пояс" in it["product"]["name"].lower()
        or "фляга" in it["product"]["name"].lower()
        for it in gear_items
    ), f"Scenario {scenario['id']}: Missing essential gear item (race belt or soft flask)"

    if fmt == "full" and not custom_budget:
        # Full Ironman standard/premium boxes should include soft flask for marathon leg
        assert any(
            it["product"].get("sub_type") == "flasks" or "фляга" in it["product"]["name"].lower()
            for it in gear_items
        ), f"Scenario {scenario['id']}: Full Ironman should provide soft flask for the marathon leg"

    # 10. Recovery Slot Validation
    care_items = box["slots"]["care_recovery"]
    assert any(
        it["product"].get("sub_type") in ["recovery_drink", "recovery_shake", "anti_chlorine", "anti_chafe_cream", "anti_chafe", "magnesium"]
        or "відновлювальний" in it["product"]["name"].lower()
        or "regener" in it["product"]["name"].lower()
        or "recovery" in it["product"]["name"].lower()
        for it in care_items
    ), f"Scenario {scenario['id']}: Missing recovery or care product in care_recovery"

    # 11. Multi-Stage Nutrition Scaling
    energy_items = box["slots"]["energy"]
    total_energy_units = sum(it["quantity_recommended"] for it in energy_items)
    # Note: PF 90 (product_id 2025) is a triple-serving 153g / 90g carb pouch
    effective_energy_servings = sum(
        it["quantity_recommended"] * (3 if it["product"]["product_id"] == 2025 else 1)
        for it in energy_items
    )

    if fmt == "sprint":
        assert effective_energy_servings >= 2, f"Sprint should have at least 2 energy servings, got {effective_energy_servings}"
    elif fmt == "half":
        assert total_energy_units >= 3, f"Half Ironman should have at least 3 energy units, got {total_energy_units}"
        assert any(
            it["product"].get("sub_type") in ["chew", "transition_chew"] or "chew" in it["product"]["name"].lower()
            for it in energy_items
        ), f"Scenario {scenario['id']}: Half Ironman should include transition chews for the bike leg"
    elif fmt == "full":
        min_units = 3 if custom_budget else 4
        assert total_energy_units >= min_units, f"Full Ironman should have at least {min_units} energy units, got {total_energy_units}"
        assert any(
            it["product"].get("sub_type") in ["chew", "transition_chew"] or "chew" in it["product"]["name"].lower()
            for it in energy_items
        ), f"Scenario {scenario['id']}: Full Ironman should include transition chews for bike leg"
        assert any(
            it["product"].get("sub_type") == "drink_mix" or "напій" in it["product"]["name"].lower()
            for it in energy_items
        ), f"Scenario {scenario['id']}: Full Ironman must include high-carb drink mix for 180km bike leg"

    # 12. Deselection & Cart Payload Simulation (for deselection scenarios)
    if deselect:
        cart_payload = []
        cart_total = 0.0
        deselected_count = 0

        for slot_name, items in box["slots"].items():
            for it in items:
                p = it["product"]
                st = p.get("sub_type", "")
                name_l = p.get("name", "").lower()
                is_deselected = (st in deselect) or any(d in st or d in name_l for d in deselect)

                if is_deselected:
                    deselected_count += 1
                else:
                    cart_payload.append({
                        "productId": p["product_id"],
                        "name": p["name"],
                        "quantity": it["quantity_recommended"],
                        "price": p["price"]
                    })
                    cart_total += p["price"] * it["quantity_recommended"]

        assert deselected_count > 0, f"Scenario {scenario['id']}: Target deselection item not found in box"
        assert len(cart_payload) < len(all_recommended_items), "Cart should contain fewer items after deselection"
        assert cart_total < box["total_base_price"], "Cart total should be less than original total after deselection"
        assert round(cart_total, 2) == round(sum(i["price"] * i["quantity"] for i in cart_payload), 2)

        # Verify deselected items are completely omitted from cart payload
        for item in cart_payload:
            matching_cat_prod = next(p for p in CATALOG if p["product_id"] == item["productId"])
            cat_st = matching_cat_prod.get("sub_type", "")
            cat_name_l = matching_cat_prod.get("name", "").lower()
            assert not ((cat_st in deselect) or any(d in cat_st or d in cat_name_l for d in deselect)), (
                f"Deselected item found in cart payload: {item['name']}"
            )

        if "custom_budget_target" in scenario:
            assert cart_total <= scenario["custom_budget_target"], (
                f"Cart total ({cart_total}) exceeds deselection budget target ({scenario['custom_budget_target']})"
            )
