"""Test Suite: 50 Comprehensive Scenarios for Cycling Category Starter Boxes.

This test file verifies the Cycling Starter Box Decision Engine against 50 distinct,
realistic, and diverse cyclist personas. It exercises the full matrix of:
- Distances / Formats: Short (40-60 km), Medium (80-100 km), Long Gran Fondo (120-200 km)
- Weather Conditions: Cold, Moderate, Hot
- Saddle Comfort Concerns: True (Chamois Butt'r) vs False
- Caffeine Preferences: 'none' (Strict Zero-Caffeine Guarantee) vs 'boost'
- Price Tiers: Economy, Standard, Premium
- Custom Budgets: Varied numeric caps (900, 1200, 1500, 1800, 2200, 2800, 3000, 3500, 4500, 5500 грн)
- Item Deselection: Verifies cart total and item removal calculations
"""

import pytest
from multi_sport_engine import generate_custom_sport_box, generate_cycling_box, load_catalog


# ==============================================================================
# 50 DIVERSE CYCLING SCENARIOS / PERSONAS
# ==============================================================================

SCENARIOS = [
    # --- Group 1: Short Distance (40-60 km) ---
    {
        "id": 1,
        "name": "01_Short_Beginner_Sprint_Economy_NoCaff_NoSaddle",
        "inputs": {"distance_format": "short", "weather": "moderate", "caffeine_preference": "none", "saddle_comfort": False, "price_tier": "economy"},
        "deselect": "gear",
        "description": "Beginner 40km fitness spin, economy budget, zero caffeine, already has bidon"
    },
    {
        "id": 2,
        "name": "02_Short_Commuter_Fitness_Standard_Cold_CaffBoost_SaddleComfort",
        "inputs": {"distance_format": "short", "weather": "cold", "caffeine_preference": "boost", "saddle_comfort": True, "price_tier": "standard"},
        "deselect": None,
        "description": "Cold morning fitness ride, caffeine kick for hills, saddle comfort cream"
    },
    {
        "id": 3,
        "name": "03_Short_Summer_Criterium_Premium_Hot_CaffBoost_SaddleComfort",
        "inputs": {"distance_format": "short", "weather": "hot", "caffeine_preference": "boost", "saddle_comfort": True, "price_tier": "premium"},
        "deselect": "care_recovery",
        "description": "Hot evening criterium race, maximum wattage boost, electrolytes, opts out of post-race care"
    },
    {
        "id": 4,
        "name": "04_Short_Recovery_Ride_Economy_Cold_NoCaff_NoSaddle",
        "inputs": {"distance_format": "short", "weather": "cold", "caffeine_preference": "none", "saddle_comfort": False, "price_tier": "economy"},
        "deselect": "energy_solid",
        "description": "Gentle winter recovery roll, low heart rate, no stimulants, deselects energy bakes"
    },
    {
        "id": 5,
        "name": "05_Short_Interval_Punch_Standard_Moderate_CaffBoost_NoSaddle",
        "inputs": {"distance_format": "short", "weather": "moderate", "caffeine_preference": "boost", "saddle_comfort": False, "price_tier": "standard"},
        "deselect": None,
        "description": "High-intensity VO2 max hill repeats, caffeine sprint fuel, short ride without chamois"
    },
    {
        "id": 6,
        "name": "06_Short_Hot_Noon_Blast_Standard_Hot_NoCaff_SaddleComfort",
        "inputs": {"distance_format": "short", "weather": "hot", "caffeine_preference": "none", "saddle_comfort": True, "price_tier": "standard"},
        "deselect": "gear",
        "description": "Intense midday heat, clean hydration with salt caps, saddle protection, deselects bottle"
    },
    {
        "id": 7,
        "name": "07_Short_Budget_Minimalist_Custom900_Moderate_NoCaff_NoSaddle",
        "inputs": {"distance_format": "short", "weather": "moderate", "caffeine_preference": "none", "saddle_comfort": False, "custom_budget": 900},
        "deselect": None,
        "description": "Strict 900 грн budget cap, zero stimulants, essential nutrition only"
    },
    {
        "id": 8,
        "name": "08_Short_Budget_Boost_Custom1200_Cold_CaffBoost_NoSaddle",
        "inputs": {"distance_format": "short", "weather": "cold", "caffeine_preference": "boost", "saddle_comfort": False, "custom_budget": 1200},
        "deselect": "care_recovery",
        "description": "Fast chilly tempo, 1200 грн limit, caffeine punch, deselects care items"
    },
    {
        "id": 9,
        "name": "09_Short_Comfort_Starter_Custom1500_Moderate_NoCaff_SaddleComfort",
        "inputs": {"distance_format": "short", "weather": "moderate", "caffeine_preference": "none", "saddle_comfort": True, "custom_budget": 1500},
        "deselect": "chamois",
        "description": "Entry road cyclist with saddle sensitivity, 1500 грн budget, tests unchecking chamois cream"
    },
    {
        "id": 10,
        "name": "10_Short_Cold_Tempo_Custom1800_Cold_CaffBoost_SaddleComfort",
        "inputs": {"distance_format": "short", "weather": "cold", "caffeine_preference": "boost", "saddle_comfort": True, "custom_budget": 1800},
        "deselect": None,
        "description": "Brisk autumn ride, solid carbs + caffeine gel, Chamois Butt'r defense"
    },
    {
        "id": 11,
        "name": "11_Short_Pro_Crit_Custom2200_Hot_CaffBoost_SaddleComfort",
        "inputs": {"distance_format": "short", "weather": "hot", "caffeine_preference": "boost", "saddle_comfort": True, "custom_budget": 2200},
        "deselect": "gear",
        "description": "Hot summer criterium racer, 2200 грн custom budget, precision hydration and electrolytes"
    },
    {
        "id": 12,
        "name": "12_Short_Elite_Track_Sprinter_Premium_Cold_CaffBoost_NoSaddle",
        "inputs": {"distance_format": "short", "weather": "cold", "caffeine_preference": "boost", "saddle_comfort": False, "price_tier": "premium"},
        "deselect": None,
        "description": "High-end power sprinter, premium Maurten/PF fuels, caffeine blast, no chamois needed"
    },
    {
        "id": 13,
        "name": "13_Short_Sensitive_Stomach_Standard_Moderate_NoCaff_SaddleComfort",
        "inputs": {"distance_format": "short", "weather": "moderate", "caffeine_preference": "none", "saddle_comfort": True, "price_tier": "standard"},
        "deselect": "recovery_drink",
        "description": "Gentle fuel on digestion, zero caffeine, Chamois Butt'r comfort, deselects recovery shake"
    },
    {
        "id": 14,
        "name": "14_Short_Midsummer_Scorcher_Economy_Hot_NoCaff_NoSaddle",
        "inputs": {"distance_format": "short", "weather": "hot", "caffeine_preference": "none", "saddle_comfort": False, "price_tier": "economy"},
        "deselect": None,
        "description": "Budget summer ride, heat salt protection, zero caffeine, clean isotonic"
    },
    {
        "id": 15,
        "name": "15_Short_Autumn_Spin_Standard_Cold_NoCaff_SaddleComfort",
        "inputs": {"distance_format": "short", "weather": "cold", "caffeine_preference": "none", "saddle_comfort": True, "price_tier": "standard"},
        "deselect": "chamois",
        "description": "Chilly fall 50km ride, clean energy, testing chamois deselection"
    },
    {
        "id": 16,
        "name": "16_Short_VIP_Club_Ride_Custom3500_Moderate_CaffBoost_SaddleComfort",
        "inputs": {"distance_format": "short", "weather": "moderate", "caffeine_preference": "boost", "saddle_comfort": True, "custom_budget": 3500},
        "deselect": None,
        "description": "Generous 3500 грн custom budget, premium bakes, caffeine gel, recovery tub"
    },

    # --- Group 2: Medium Distance (80-100 km) ---
    {
        "id": 17,
        "name": "17_Medium_Weekend_Club_Standard_Moderate_CaffBoost_SaddleComfort",
        "inputs": {"distance_format": "medium", "weather": "moderate", "caffeine_preference": "boost", "saddle_comfort": True, "price_tier": "standard"},
        "deselect": "gear",
        "description": "Classic 80-100km group ride, 3 solid bakes + gels, saddle comfort, deselects bottle"
    },
    {
        "id": 18,
        "name": "18_Medium_Rolling_Hills_Standard_Cold_NoCaff_SaddleComfort",
        "inputs": {"distance_format": "medium", "weather": "cold", "caffeine_preference": "none", "saddle_comfort": True, "price_tier": "standard"},
        "deselect": None,
        "description": "Cold autumn hilly ride, zero-caffeine guarantee, solid fuels for sustained energy"
    },
    {
        "id": 19,
        "name": "19_Medium_Summer_Fondo_Training_Standard_Hot_CaffBoost_SaddleComfort",
        "inputs": {"distance_format": "medium", "weather": "hot", "caffeine_preference": "boost", "saddle_comfort": True, "price_tier": "standard"},
        "deselect": "chamois",
        "description": "Hot 90km Gran Fondo prep, salt caps + isotonic, caffeine surge, deselects cream"
    },
    {
        "id": 20,
        "name": "20_Medium_Budget_Century_Prep_Economy_Moderate_NoCaff_NoSaddle",
        "inputs": {"distance_format": "medium", "weather": "moderate", "caffeine_preference": "none", "saddle_comfort": False, "price_tier": "economy"},
        "deselect": None,
        "description": "Economy 80km ride, affordable Fizi bars, zero caffeine, isotonic replenishment"
    },
    {
        "id": 21,
        "name": "21_Medium_Chilly_Autumn_Economy_Cold_CaffBoost_NoSaddle",
        "inputs": {"distance_format": "medium", "weather": "cold", "caffeine_preference": "boost", "saddle_comfort": False, "price_tier": "economy"},
        "deselect": "care_recovery",
        "description": "Cold 80km solo roll, economical solid fuel with caffeine kick, deselects recovery"
    },
    {
        "id": 22,
        "name": "22_Medium_Scorching_90k_Economy_Hot_CaffBoost_NoSaddle",
        "inputs": {"distance_format": "medium", "weather": "hot", "caffeine_preference": "boost", "saddle_comfort": False, "price_tier": "economy"},
        "deselect": None,
        "description": "Hot summer tempo ride, budget electrolyte salts, caffeine for tough headwind"
    },
    {
        "id": 23,
        "name": "23_Medium_Premium_Climbing_Camp_Premium_Moderate_CaffBoost_SaddleComfort",
        "inputs": {"distance_format": "medium", "weather": "moderate", "caffeine_preference": "boost", "saddle_comfort": True, "price_tier": "premium"},
        "deselect": "recovery_drink",
        "description": "Mountain climbing camp, SiS Beta Fuel chew + 226ERS caff gel, Chamois Butt'r"
    },
    {
        "id": 24,
        "name": "24_Medium_Alpine_Cold_Pass_Premium_Cold_CaffBoost_SaddleComfort",
        "inputs": {"distance_format": "medium", "weather": "cold", "caffeine_preference": "boost", "saddle_comfort": True, "price_tier": "premium"},
        "deselect": None,
        "description": "Cold mountain passes, high carbohydrate density, recovery shake, chamois barrier"
    },
    {
        "id": 25,
        "name": "25_Medium_Summer_Heatwave_Premium_Hot_NoCaff_SaddleComfort",
        "inputs": {"distance_format": "medium", "weather": "hot", "caffeine_preference": "none", "saddle_comfort": True, "price_tier": "premium"},
        "deselect": "gear",
        "description": "Intense 35°C heat, strict zero caffeine, high sodium isotonic, Chamois Butt'r"
    },
    {
        "id": 26,
        "name": "26_Medium_Strict_ZeroCaff_Racer_Standard_Moderate_NoCaff_SaddleComfort",
        "inputs": {"distance_format": "medium", "weather": "moderate", "caffeine_preference": "none", "saddle_comfort": True, "price_tier": "standard"},
        "deselect": None,
        "description": "Zero caffeine tolerance, clean isotonic, solid fuel bars, post-ride recovery"
    },
    {
        "id": 27,
        "name": "27_Medium_Budget_Cap_1500_Custom1500_Moderate_CaffBoost_SaddleComfort",
        "inputs": {"distance_format": "medium", "weather": "moderate", "caffeine_preference": "boost", "saddle_comfort": True, "custom_budget": 1500},
        "deselect": "chamois",
        "description": "1500 грн budget for medium ride, optimized fuel, test deselecting chamois"
    },
    {
        "id": 28,
        "name": "28_Medium_Budget_Cap_1800_Cold_Custom1800_Cold_NoCaff_SaddleComfort",
        "inputs": {"distance_format": "medium", "weather": "cold", "caffeine_preference": "none", "saddle_comfort": True, "custom_budget": 1800},
        "deselect": None,
        "description": "1800 грн budget in chilly weather, zero-caffeine guarantee, chamois protection"
    },
    {
        "id": 29,
        "name": "29_Medium_Budget_Cap_2200_Hot_Custom2200_Hot_CaffBoost_SaddleComfort",
        "inputs": {"distance_format": "medium", "weather": "hot", "caffeine_preference": "boost", "saddle_comfort": True, "custom_budget": 2200},
        "deselect": "care_recovery",
        "description": "Hot 80km ride with 2200 грн budget, salt caps, caffeine gel, deselects recovery"
    },
    {
        "id": 30,
        "name": "30_Medium_Budget_Cap_2800_Custom2800_Moderate_CaffBoost_SaddleComfort",
        "inputs": {"distance_format": "medium", "weather": "moderate", "caffeine_preference": "boost", "saddle_comfort": True, "custom_budget": 2800},
        "deselect": None,
        "description": "2800 грн budget, optimal mix of solid fuels, PF hydration tube, Chamois Butt'r"
    },
    {
        "id": 31,
        "name": "31_Medium_Budget_Cap_3500_Custom3500_Hot_CaffBoost_SaddleComfort",
        "inputs": {"distance_format": "medium", "weather": "hot", "caffeine_preference": "boost", "saddle_comfort": True, "custom_budget": 3500},
        "deselect": "gear",
        "description": "3500 грн custom budget, premium Beta Fuel chew, salts, Chamois Butt'r, deselects bidon"
    },
    {
        "id": 32,
        "name": "32_Medium_Budget_Cap_4500_Custom4500_Cold_NoCaff_SaddleComfort",
        "inputs": {"distance_format": "medium", "weather": "cold", "caffeine_preference": "none", "saddle_comfort": True, "custom_budget": 4500},
        "deselect": None,
        "description": "4500 грн high budget, zero caffeine, premium recovery tub, socks, solid energy"
    },
    {
        "id": 33,
        "name": "33_Medium_Fast_Paceline_Standard_Moderate_CaffBoost_NoSaddle",
        "inputs": {"distance_format": "medium", "weather": "moderate", "caffeine_preference": "boost", "saddle_comfort": False, "price_tier": "standard"},
        "deselect": "energy_caff",
        "description": "Fast paceline group ride, tests user deselecting caffeine gel from energy slot"
    },

    # --- Group 3: Long Distance / Gran Fondo / Brevet (120-200 km) ---
    {
        "id": 34,
        "name": "34_Long_Gran_Fondo_Challenger_Standard_Moderate_CaffBoost_SaddleComfort",
        "inputs": {"distance_format": "long", "weather": "moderate", "caffeine_preference": "boost", "saddle_comfort": True, "price_tier": "standard"},
        "deselect": "chamois",
        "description": "150km Gran Fondo, 5 solid bakes, salt caps, Magneslife, tests chamois uncheck"
    },
    {
        "id": 35,
        "name": "35_Long_Summer_Brevet_200k_Standard_Hot_CaffBoost_SaddleComfort",
        "inputs": {"distance_format": "long", "weather": "hot", "caffeine_preference": "boost", "saddle_comfort": True, "price_tier": "standard"},
        "deselect": None,
        "description": "200km hot summer brevet, essential salt caps, Magneslife anti-cramp, Chamois Butt'r"
    },
    {
        "id": 36,
        "name": "36_Long_Mountain_Century_Standard_Cold_NoCaff_SaddleComfort",
        "inputs": {"distance_format": "long", "weather": "cold", "caffeine_preference": "none", "saddle_comfort": True, "price_tier": "standard"},
        "deselect": "gear",
        "description": "Cold 160km century ride, zero caffeine guarantee, Magneslife, deselects bottle"
    },
    {
        "id": 37,
        "name": "37_Long_Budget_Brevet_150k_Economy_Moderate_NoCaff_NoSaddle",
        "inputs": {"distance_format": "long", "weather": "moderate", "caffeine_preference": "none", "saddle_comfort": False, "price_tier": "economy"},
        "deselect": None,
        "description": "Budget 150km brevet, economical solid energy, salt caps, zero stimulants"
    },
    {
        "id": 38,
        "name": "38_Long_Hot_Century_Economy_Hot_CaffBoost_NoSaddle",
        "inputs": {"distance_format": "long", "weather": "hot", "caffeine_preference": "boost", "saddle_comfort": False, "price_tier": "economy"},
        "deselect": "care_recovery",
        "description": "Hot 100-mile ride, salt caps + caffeine boost, deselects recovery products"
    },
    {
        "id": 39,
        "name": "39_Long_Cold_Endurance_Economy_Cold_NoCaff_NoSaddle",
        "inputs": {"distance_format": "long", "weather": "cold", "caffeine_preference": "none", "saddle_comfort": False, "price_tier": "economy"},
        "deselect": None,
        "description": "Cold 120km endurance ride, solid carbs, Magneslife, zero caffeine"
    },
    {
        "id": 40,
        "name": "40_Long_Pro_Gran_Fondo_Premium_Moderate_CaffBoost_SaddleComfort",
        "inputs": {"distance_format": "long", "weather": "moderate", "caffeine_preference": "boost", "saddle_comfort": True, "price_tier": "premium"},
        "deselect": "recovery_drink",
        "description": "Pro-tier 160km race, Maurten/Beta Fuel nutrition, Chamois Butt'r, deselects recovery"
    },
    {
        "id": 41,
        "name": "41_Long_Alpine_Epic_Premium_Cold_CaffBoost_SaddleComfort",
        "inputs": {"distance_format": "long", "weather": "cold", "caffeine_preference": "boost", "saddle_comfort": True, "price_tier": "premium"},
        "deselect": None,
        "description": "Alpine pass crossing, 5 solid bakes, caffeine punch, Magneslife, Chamois Butt'r"
    },
    {
        "id": 42,
        "name": "42_Long_Desert_Heat_Ultra_Premium_Hot_CaffBoost_SaddleComfort",
        "inputs": {"distance_format": "long", "weather": "hot", "caffeine_preference": "boost", "saddle_comfort": True, "price_tier": "premium"},
        "deselect": "gear",
        "description": "Extreme heat ultra ride, double salts, caffeine surge, Chamois Butt'r, deselects bottle"
    },
    {
        "id": 43,
        "name": "43_Long_Maurten_ZeroCaff_Fondo_Premium_Moderate_NoCaff_SaddleComfort",
        "inputs": {"distance_format": "long", "weather": "moderate", "caffeine_preference": "none", "saddle_comfort": True, "price_tier": "premium"},
        "deselect": None,
        "description": "Elite Gran Fondo, 100% zero-caffeine guarantee across all slots, Chamois Butt'r"
    },
    {
        "id": 44,
        "name": "44_Long_Custom_Budget_2800_Custom2800_Moderate_CaffBoost_SaddleComfort",
        "inputs": {"distance_format": "long", "weather": "moderate", "caffeine_preference": "boost", "saddle_comfort": True, "custom_budget": 2800},
        "deselect": "chamois",
        "description": "2800 грн budget for Gran Fondo, solid energy + salts, tests unchecking chamois"
    },
    {
        "id": 45,
        "name": "45_Long_Custom_Budget_3000_Hot_Custom3000_Hot_CaffBoost_SaddleComfort",
        "inputs": {"distance_format": "long", "weather": "hot", "caffeine_preference": "boost", "saddle_comfort": True, "custom_budget": 3000},
        "deselect": None,
        "description": "3000 грн budget hot century, full salt caps + Magneslife protection, Chamois Butt'r"
    },
    {
        "id": 46,
        "name": "46_Long_Custom_Budget_3500_Cold_Custom3500_Cold_CaffBoost_SaddleComfort",
        "inputs": {"distance_format": "long", "weather": "cold", "caffeine_preference": "boost", "saddle_comfort": True, "custom_budget": 3500},
        "deselect": "care_recovery",
        "description": "3500 грн budget cold mountain challenge, heavy solid fuels, deselects care slot"
    },
    {
        "id": 47,
        "name": "47_Long_Custom_Budget_4500_ZeroCaff_Custom4500_Moderate_NoCaff_SaddleComfort",
        "inputs": {"distance_format": "long", "weather": "moderate", "caffeine_preference": "none", "saddle_comfort": True, "custom_budget": 4500},
        "deselect": None,
        "description": "4500 грн budget Gran Fondo, strict zero-caffeine guarantee, REGO recovery tub"
    },
    {
        "id": 48,
        "name": "48_Long_Custom_Budget_5500_Ultimate_Custom5500_Hot_CaffBoost_SaddleComfort",
        "inputs": {"distance_format": "long", "weather": "hot", "caffeine_preference": "boost", "saddle_comfort": True, "custom_budget": 5500},
        "deselect": "gear",
        "description": "5500 грн ultimate setup, full course hydration + electrolytes, deselects gear"
    },
    {
        "id": 49,
        "name": "49_Long_Ultra_Audax_Standard_Moderate_NoCaff_SaddleComfort",
        "inputs": {"distance_format": "long", "weather": "moderate", "caffeine_preference": "none", "saddle_comfort": True, "price_tier": "standard"},
        "deselect": "chamois",
        "description": "Ultra-distance audax cyclist, zero stimulants, endurance energy, tests chamois toggle"
    },
    {
        "id": 50,
        "name": "50_Long_Solo_Mountain_Century_Standard_Cold_CaffBoost_SaddleComfort",
        "inputs": {"distance_format": "long", "weather": "cold", "caffeine_preference": "boost", "saddle_comfort": True, "price_tier": "standard"},
        "deselect": None,
        "description": "Solo 160km mountain ride, solid fuel bakes + caffeine climbs, Chamois Butt'r cream"
    }
]


# ==============================================================================
# TEST FIXTURE: CYCLING CATALOG
# ==============================================================================

@pytest.fixture(scope="module")
def cycling_catalog():
    return load_catalog("cycling")


# ==============================================================================
# PARAMETRIZED TEST SUITE: 50 TESTS
# ==============================================================================

@pytest.mark.parametrize("scenario", SCENARIOS, ids=[s["name"] for s in SCENARIOS])
def test_cycling_scenario(scenario, cycling_catalog):
    """Verify that every cycling persona receives a valid, complete, physiologically

    sound starter box complying with all domain guardrails and budget constraints.
    """
    sid = scenario["id"]
    inputs = scenario["inputs"]
    deselect_target = scenario.get("deselect")

    # 1. Generate box via multi_sport_engine
    box = generate_custom_sport_box("cycling", inputs)
    assert box["sport"] == "cycling"
    assert box["total_base_price"] > 0, f"Scenario #{sid}: total_base_price must be > 0"

    slots = box["slots"]

    # 2. Guardrail: No empty slots
    for slot_name in ["energy", "hydration", "gear", "care_recovery"]:
        assert slot_name in slots, f"Scenario #{sid}: Missing slot '{slot_name}' in box"
        assert len(slots[slot_name]) >= 1, f"Scenario #{sid}: Slot '{slot_name}' must not be empty"

    # 3. Guardrail: Solid fuels vs Fast fuels in energy slot
    # Cycling physiology requires solid energy (bakes, bars, chews) for early hours + fast gels for climbs/sprints
    has_solid = any(
        it["product"].get("sub_type") in ["bake", "energy_bake", "bar", "chew"] or
        any(k in it["product"]["name"].lower() for k in ["bake", "bar", "chew", "батончик", "печиво"])
        for it in slots["energy"]
    )
    assert has_solid, f"Scenario #{sid}: Energy slot must include solid fuels (bake/bar/chew)"

    has_fast_gel = any(
        it["product"].get("sub_type") == "gel" or "гель" in it["product"]["name"].lower()
        for it in slots["energy"]
    )
    assert has_fast_gel, f"Scenario #{sid}: Energy slot must include fast gels"

    # 4. Guardrail: Caffeine Preference & Zero-Caffeine Guarantee
    caff_pref = inputs.get("caffeine_preference")
    if caff_pref == "none":
        for s_name, items in slots.items():
            for it in items:
                assert it["product"].get("caffeine") is not True, (
                    f"Scenario #{sid}: Zero-caffeine leak! Product '{it['product']['name']}' "
                    f"in slot '{s_name}' contains caffeine."
                )
    elif caff_pref == "boost":
        has_caff = any(it["product"].get("caffeine", False) for it in slots["energy"])
        assert has_caff, f"Scenario #{sid}: Caffeine boost requested, but energy slot has no caffeine item"

    # 5. Guardrail: Saddle Comfort (Chamois Butt'r)
    saddle_comfort = inputs.get("saddle_comfort", True)
    has_chamois = any(
        "chamois" in it["product"]["name"].lower() or
        it["product"].get("sub_type") in ["chamois_cream", "anti_chafe_cream"]
        for it in slots["care_recovery"]
    )
    if saddle_comfort:
        assert has_chamois, (
            f"Scenario #{sid}: Saddle comfort concern requested, but Chamois Butt'r cream is missing "
            f"from care_recovery slot"
        )
    else:
        assert not has_chamois, (
            f"Scenario #{sid}: Saddle comfort was False, but Chamois Butt'r cream was included"
        )

    # 6. Guardrail: Hydration & Salts for Long Distance or Hot Weather
    dist = inputs.get("distance_format")
    weather = inputs.get("weather")
    if dist == "long" or weather == "hot":
        # Must have isotonic hydration
        has_isotonic = any(
            it["product"].get("sub_type") in ["isotonic", "isotonic_tube", "isotonic_sachet", "electrolyte_drink", "drink_mix"] or
            "ізотонік" in it["product"]["name"].lower() or "electrolyte" in it["product"]["name"].lower()
            for it in slots["hydration"]
        )
        assert has_isotonic, f"Scenario #{sid}: Long/hot cycling box must have isotonic drink/tabs"

        # Must have salt caps / electrolyte capsules or Magneslife anti-cramp shots
        has_salts = any(
            it["product"].get("sub_type") in ["salt_caps", "magnesium"] or
            any(k in it["product"]["name"].lower() for k in ["сольові", "magneslife", "магній"])
            for s in [slots["hydration"], slots["care_recovery"]]
            for it in s
        )
        assert has_salts, f"Scenario #{sid}: Long/hot cycling box must have salt caps or Magneslife anti-cramp shots"

    # 7. Guardrail: Recovery products in care_recovery
    has_recovery = any(
        it["product"].get("sub_type") in ["recovery_drink", "recovery_sachet", "recovery_tub", "protein", "recovery_snack", "magnesium"] or
        any(k in it["product"]["name"].lower() for k in ["rego", "regener", "recovery", "віднов", "протеїн", "magneslife"])
        for it in slots["care_recovery"]
    )
    assert has_recovery, f"Scenario #{sid}: care_recovery slot must contain muscle recovery product"

    # 8. Guardrail: Stock, Pricing & Custom Budget Compliance
    custom_budget = inputs.get("custom_budget")
    if custom_budget:
        assert box["total_base_price"] <= custom_budget, (
            f"Scenario #{sid}: Box total {box['total_base_price']} exceeds custom budget {custom_budget}"
        )
        assert box["budget_info"]["within_budget"] is True

    for s_name, items in slots.items():
        for it in items:
            p = it["product"]
            qty = it["quantity_recommended"]
            assert qty > 0, f"Scenario #{sid}: Product {p['name']} recommended quantity must be > 0"
            assert p.get("quantity", 0) > 0, f"Scenario #{sid}: Product {p['name']} is out of stock in catalog"
            assert p.get("price", 0) > 0, f"Scenario #{sid}: Product {p['name']} has invalid price {p.get('price')}"

    # 9. Guardrail: Item Deselection and Cart Total Update Simulation
    # Flatten all box items with their slot and index
    all_items = []
    for s_name in ["energy", "hydration", "gear", "care_recovery"]:
        for idx, it in enumerate(slots.get(s_name, [])):
            all_items.append((s_name, idx, it))

    calculated_base_price = sum(it["product"]["price"] * it["quantity_recommended"] for _, _, it in all_items)
    assert round(calculated_base_price, 2) == round(box["total_base_price"], 2)

    # Determine which items are deselected by user
    deselected_keys = set()
    if deselect_target == "gear":
        for s_name, idx, it in all_items:
            if s_name == "gear":
                deselected_keys.add((s_name, idx))
    elif deselect_target == "care_recovery":
        for s_name, idx, it in all_items:
            if s_name == "care_recovery":
                deselected_keys.add((s_name, idx))
    elif deselect_target == "chamois":
        for s_name, idx, it in all_items:
            if "chamois" in it["product"]["name"].lower() or it["product"].get("sub_type") in ["chamois_cream", "anti_chafe_cream"]:
                deselected_keys.add((s_name, idx))
    elif deselect_target == "recovery_drink":
        for s_name, idx, it in all_items:
            if it["product"].get("sub_type") in ["recovery_drink", "recovery_sachet", "recovery_tub", "protein"]:
                deselected_keys.add((s_name, idx))
    elif deselect_target == "energy_solid":
        for s_name, idx, it in all_items:
            if it["product"].get("sub_type") in ["bake", "energy_bake", "bar", "chew"] or any(k in it["product"]["name"].lower() for k in ["bake", "bar", "chew", "батончик", "печиво"]):
                deselected_keys.add((s_name, idx))
    elif deselect_target == "energy_caff":
        for s_name, idx, it in all_items:
            if it["product"].get("caffeine", False):
                deselected_keys.add((s_name, idx))

    # Calculate final cart state after deselection
    cart_items = []
    cart_total = 0.0
    expected_reduction = 0.0
    for s_name, idx, it in all_items:
        if (s_name, idx) in deselected_keys:
            expected_reduction += it["product"]["price"] * it["quantity_recommended"]
        else:
            cart_items.append(it)
            cart_total += it["product"]["price"] * it["quantity_recommended"]

    if deselect_target and len(deselected_keys) > 0:
        assert round(cart_total, 2) == round(box["total_base_price"] - expected_reduction, 2), (
            f"Scenario #{sid}: Cart total {cart_total} did not match expected {box['total_base_price'] - expected_reduction}"
        )
        assert len(cart_items) < len(all_items), f"Scenario #{sid}: Cart items count should be reduced"
        assert cart_total < box["total_base_price"], f"Scenario #{sid}: Cart total should be less than original"
        # Confirm no deselected item slipped into cart
        for it in cart_items:
            for s_name, idx in deselected_keys:
                target_it = next(item for sn, i, item in all_items if sn == s_name and i == idx)
                assert it["product"]["product_id"] != target_it["product"]["product_id"] or it is not target_it
    else:
        assert round(cart_total, 2) == round(box["total_base_price"], 2)
        assert len(cart_items) == len(all_items)
