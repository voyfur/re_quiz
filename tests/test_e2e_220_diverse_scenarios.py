"""220 Radically Diverse End-to-End (E2E) Customer Journey Scenarios.

Covers the full matrix of athlete personas, constraints, physiological profiles,
and commercial conditions across all 5 sports on a live HTTP server:
- Running & Trail (44 diverse scenarios: RUN_001 to RUN_044)
- Cycling (44 diverse scenarios: CYC_001 to CYC_044)
- Triathlon & Swimming (44 diverse scenarios: TRI_001 to TRI_044)
- Gym & Fitness (44 diverse scenarios: GYM_001 to GYM_044)
- Hiking & Outdoor / ЇDLO (44 diverse scenarios: OUT_001 to OUT_044)
- OpenCart cart payload integrity and price recalculation invariants.
"""

import json
import urllib.request
import pytest
from test_server_runner_box import live_server


def post_generate_box(server_url: str, sport: str, inputs: dict) -> dict:
    payload = {"sport": sport, **inputs}
    data_bytes = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        f"{server_url}/api/generate-sport-box",
        data=data_bytes,
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=8) as resp:
        assert resp.status == 200
        return json.loads(resp.read().decode("utf-8"))


def assert_box_structure(box: dict, expected_sport: str, inputs: dict):
    assert "slots" in box, "Box must contain 'slots'"
    slots = box["slots"]
    for s_name in ["energy", "hydration", "gear", "care_recovery"]:
        assert s_name in slots, f"Slot {s_name} missing from box"
        assert isinstance(slots[s_name], list), f"Slot {s_name} must be a list"
        assert len(slots[s_name]) >= 1, f"Slot {s_name} must not be empty"

    # Price integrity
    calc_total = 0.0
    for s_items in slots.values():
        for it in s_items:
            prod = it["product"]
            assert prod["price"] > 0, f"Product {prod.get('name')} price must be > 0"
            assert it["quantity_recommended"] >= 1, f"Quantity must be >= 1"
            calc_total += prod["price"] * it["quantity_recommended"]

    assert abs(box["total_base_price"] - round(calc_total, 2)) < 0.05, \
        f"total_base_price {box['total_base_price']} does not match sum {calc_total}"

    # Zero caffeine invariant
    if inputs.get("caffeine_preference") == "none" or inputs.get("pre_workout_boost") in ["none", "beta_alanine"]:
        for s_name, s_items in slots.items():
            for it in s_items:
                p = it["product"]
                assert p.get("caffeine", False) is False, \
                    f"Caffeine leak in zero-caffeine scenario ({s_name}): {p.get('name')}"

    # Custom budget check
    cb = inputs.get("custom_budget")
    if cb and float(cb) > 0:
        b_info = box.get("budget_info", {})
        assert b_info.get("type") == "custom"
        assert b_info.get("custom_budget") == float(cb)


# ==============================================================================
# 1. RUNNING SCENARIOS (RUN_001 to RUN_044)
# ==============================================================================
RUNNING_SCENARIOS = [
    ("RUN_001_5k_sprint_zero_caff_hot", {"distance": "10k", "pace_target": "record", "weather": "hot", "caffeine_preference": "none", "body_concerns": ["cramps"], "gear_needed": ["belt"], "price_tier": "economy"}),
    ("RUN_002_5k_cold_boost_flasks", {"distance": "10k", "pace_target": "steady", "weather": "cold", "caffeine_preference": "boost", "gear_needed": ["flask"], "price_tier": "standard"}),
    ("RUN_003_10k_beginner_vegan", {"distance": "10k", "pace_target": "finish", "weather": "moderate", "caffeine_preference": "none", "stomach_type": "vegan", "gear_needed": ["socks"], "price_tier": "economy"}),
    ("RUN_004_10k_sub40_cramps_chafing", {"distance": "10k", "pace_target": "record", "weather": "hot", "caffeine_preference": "boost", "body_concerns": ["cramps", "chafing"], "price_tier": "standard"}),
    ("RUN_005_10k_rainy_tempo_joints", {"distance": "10k", "pace_target": "steady", "weather": "cold", "caffeine_preference": "boost", "body_concerns": ["joints"], "price_tier": "premium"}),
    ("RUN_006_10k_night_sensitive_850uah", {"distance": "10k", "pace_target": "steady", "weather": "moderate", "caffeine_preference": "none", "stomach_type": "sensitive", "custom_budget": 850}),
    ("RUN_007_21k_debut_none_caff", {"distance": "21k", "pace_target": "finish", "weather": "moderate", "caffeine_preference": "none", "body_concerns": ["cramps"], "price_tier": "economy"}),
    ("RUN_008_21k_sub90_boost_socks_belt", {"distance": "21k", "pace_target": "record", "weather": "moderate", "caffeine_preference": "boost", "body_concerns": ["chafing"], "gear_needed": ["socks", "belt"], "price_tier": "standard"}),
    ("RUN_009_21k_summer_heat_1950uah", {"distance": "21k", "pace_target": "finish", "weather": "hot", "caffeine_preference": "boost", "body_concerns": ["cramps", "chafing"], "gear_needed": ["flask"], "custom_budget": 1950}),
    ("RUN_010_21k_vegan_cold_premium", {"distance": "21k", "pace_target": "steady", "weather": "cold", "caffeine_preference": "none", "stomach_type": "vegan", "price_tier": "premium"}),
    ("RUN_011_21k_trail_hill_joints_magnesium", {"distance": "21k", "pace_target": "steady", "weather": "hot", "caffeine_preference": "none", "body_concerns": ["joints", "cramps"], "price_tier": "standard"}),
    ("RUN_012_21k_masters50_recovery_shake", {"distance": "21k", "pace_target": "finish", "weather": "moderate", "caffeine_preference": "boost", "body_concerns": ["joints", "recovery_shake"], "custom_budget": 2400}),
    ("RUN_013_42k_first_marathon_economy", {"distance": "42k", "pace_target": "finish", "weather": "moderate", "caffeine_preference": "none", "stomach_type": "sensitive", "body_concerns": ["chafing", "cramps"], "price_tier": "economy"}),
    ("RUN_014_42k_sub3_boost_all_gear", {"distance": "42k", "pace_target": "record", "weather": "moderate", "caffeine_preference": "boost", "gear_needed": ["socks", "flask", "belt"], "price_tier": "premium"}),
    ("RUN_015_42k_hot_berlin_salt_double_iso", {"distance": "42k", "pace_target": "steady", "weather": "hot", "caffeine_preference": "boost", "body_concerns": ["cramps"], "price_tier": "standard"}),
    ("RUN_016_42k_winter_cold_recovery_3100uah", {"distance": "42k", "pace_target": "finish", "weather": "cold", "caffeine_preference": "none", "body_concerns": ["joints", "recovery_shake"], "custom_budget": 3100}),
    ("RUN_017_42k_vegan_marathon_premium", {"distance": "42k", "pace_target": "steady", "weather": "moderate", "caffeine_preference": "none", "stomach_type": "vegan", "body_concerns": ["chafing"], "price_tier": "premium"}),
    ("RUN_018_42k_boston_qualifier_4800uah", {"distance": "42k", "pace_target": "record", "weather": "moderate", "caffeine_preference": "boost", "body_concerns": ["joints", "chafing"], "gear_needed": ["socks"], "custom_budget": 4800}),
    ("RUN_019_50k_trail_mountain_boost", {"distance": "trail", "pace_target": "steady", "weather": "hot", "caffeine_preference": "boost", "gear_needed": ["flask"], "body_concerns": ["chafing", "cramps"], "price_tier": "standard"}),
    ("RUN_020_50k_autumn_mud_sensitive_economy", {"distance": "trail", "pace_target": "finish", "weather": "cold", "caffeine_preference": "none", "stomach_type": "sensitive", "price_tier": "economy"}),
    ("RUN_021_80k_carpathians_ultra_premium", {"distance": "trail", "pace_target": "steady", "weather": "moderate", "caffeine_preference": "boost", "gear_needed": ["flask", "belt"], "body_concerns": ["recovery_shake"], "price_tier": "premium"}),
    ("RUN_022_100k_chornohora_sky_5500uah", {"distance": "trail", "pace_target": "steady", "weather": "cold", "caffeine_preference": "boost", "body_concerns": ["chafing", "cramps", "joints"], "custom_budget": 5500}),
    ("RUN_023_100k_road_ultra_vegan_6200uah", {"distance": "trail", "pace_target": "steady", "weather": "hot", "caffeine_preference": "none", "stomach_type": "vegan", "gear_needed": ["socks"], "custom_budget": 6200}),
    ("RUN_024_10k_recovery_jogger_economy", {"distance": "10k", "pace_target": "finish", "weather": "cold", "caffeine_preference": "none", "body_concerns": ["joints"], "price_tier": "economy"}),
    ("RUN_025_21k_rain_storm_1200uah", {"distance": "21k", "pace_target": "steady", "weather": "hot", "caffeine_preference": "none", "body_concerns": ["chafing"], "gear_needed": ["belt"], "custom_budget": 1200}),
    ("RUN_026_42k_elite_international_10000uah", {"distance": "42k", "pace_target": "record", "weather": "moderate", "caffeine_preference": "boost", "gear_needed": ["socks", "flask"], "custom_budget": 10000}),
    ("RUN_027_10k_junior_athlete_none_caff", {"distance": "10k", "pace_target": "finish", "weather": "moderate", "caffeine_preference": "none", "price_tier": "economy"}),
    ("RUN_028_21k_corporate_charity_boost", {"distance": "21k", "pace_target": "finish", "weather": "moderate", "caffeine_preference": "boost", "gear_needed": ["socks"], "price_tier": "standard"}),
    ("RUN_029_42k_second_marathon_3500uah", {"distance": "42k", "pace_target": "steady", "weather": "hot", "caffeine_preference": "boost", "body_concerns": ["cramps", "chafing"], "custom_budget": 3500}),
    ("RUN_030_50k_desert_simulation_4200uah", {"distance": "trail", "pace_target": "steady", "weather": "hot", "caffeine_preference": "boost", "body_concerns": ["cramps"], "gear_needed": ["flask"], "custom_budget": 4200}),
    ("RUN_031_21k_coastal_humid_economy", {"distance": "21k", "pace_target": "finish", "weather": "hot", "caffeine_preference": "none", "stomach_type": "sensitive", "price_tier": "economy"}),
    ("RUN_032_10k_treadmill_intervals_record", {"distance": "10k", "pace_target": "record", "weather": "moderate", "caffeine_preference": "boost", "price_tier": "standard"}),
    ("RUN_033_42k_night_marathon_cold", {"distance": "42k", "pace_target": "finish", "weather": "cold", "caffeine_preference": "none", "body_concerns": ["cramps"], "price_tier": "standard"}),
    ("RUN_034_21k_barefoot_transition_premium", {"distance": "21k", "pace_target": "steady", "weather": "moderate", "caffeine_preference": "none", "body_concerns": ["joints", "chafing"], "price_tier": "premium"}),
    ("RUN_035_50k_canyon_trail_3900uah", {"distance": "trail", "pace_target": "steady", "weather": "hot", "caffeine_preference": "boost", "gear_needed": ["belt", "flask"], "custom_budget": 3900}),
    ("RUN_036_10k_corporate_sprint_standard", {"distance": "10k", "pace_target": "record", "weather": "moderate", "caffeine_preference": "boost", "gear_needed": ["flask"], "price_tier": "standard"}),
    ("RUN_037_21k_spring_blossom_vegan", {"distance": "21k", "pace_target": "steady", "weather": "moderate", "caffeine_preference": "none", "stomach_type": "vegan", "price_tier": "economy"}),
    ("RUN_038_42k_autumn_foliage_cold", {"distance": "42k", "pace_target": "finish", "weather": "cold", "caffeine_preference": "none", "body_concerns": ["chafing", "recovery_shake"], "price_tier": "standard"}),
    ("RUN_039_100k_desert_trail_7500uah", {"distance": "trail", "pace_target": "steady", "weather": "hot", "caffeine_preference": "boost", "body_concerns": ["cramps", "chafing"], "gear_needed": ["flask"], "custom_budget": 7500}),
    ("RUN_040_21k_windy_bridge_1800uah", {"distance": "21k", "pace_target": "finish", "weather": "cold", "caffeine_preference": "boost", "gear_needed": ["socks"], "body_concerns": ["chafing"], "custom_budget": 1800}),
    ("RUN_041_10k_mud_obstacle_economy", {"distance": "10k", "pace_target": "finish", "weather": "cold", "caffeine_preference": "none", "body_concerns": ["recovery_shake"], "price_tier": "economy"}),
    ("RUN_042_42k_altitude_mountain_premium", {"distance": "42k", "pace_target": "steady", "weather": "cold", "caffeine_preference": "boost", "body_concerns": ["joints", "cramps"], "price_tier": "premium"}),
    ("RUN_043_50k_forest_solo_2800uah", {"distance": "trail", "pace_target": "finish", "weather": "moderate", "caffeine_preference": "none", "stomach_type": "sensitive", "gear_needed": ["flask"], "custom_budget": 2800}),
    ("RUN_044_21k_fast_track_2100uah", {"distance": "21k", "pace_target": "record", "weather": "moderate", "caffeine_preference": "boost", "gear_needed": ["socks"], "custom_budget": 2100})
]

@pytest.mark.parametrize("scenario_id,inputs", RUNNING_SCENARIOS)
def test_e2e_running_scenario(live_server, scenario_id, inputs):
    box = post_generate_box(live_server, "running", inputs)
    assert_box_structure(box, "running", inputs)
    assert "Марафон" in box["distance_label"] or "км" in box["distance_label"] or "Трейл" in box["distance_label"]


# ==============================================================================
# 2. CYCLING SCENARIOS (CYC_001 to CYC_044)
# ==============================================================================
CYCLING_SCENARIOS = [
    ("CYC_001_criterium_short_boost_hot", {"distance_format": "short", "weather": "hot", "caffeine_preference": "boost", "saddle_comfort": True, "price_tier": "standard"}),
    ("CYC_002_evening_spin_short_none_caff", {"distance_format": "short", "weather": "moderate", "caffeine_preference": "none", "saddle_comfort": False, "price_tier": "economy"}),
    ("CYC_003_climb_hill_short_premium", {"distance_format": "short", "weather": "cold", "caffeine_preference": "boost", "saddle_comfort": True, "price_tier": "premium"}),
    ("CYC_004_gravel_sprint_short_2200uah", {"distance_format": "short", "weather": "hot", "caffeine_preference": "boost", "saddle_comfort": True, "custom_budget": 2200}),
    ("CYC_005_coffee_ride_short_none_caff", {"distance_format": "short", "weather": "moderate", "caffeine_preference": "none", "saddle_comfort": True, "price_tier": "economy"}),
    ("CYC_006_medium_club_ride_standard", {"distance_format": "medium", "weather": "moderate", "caffeine_preference": "boost", "saddle_comfort": True, "price_tier": "standard"}),
    ("CYC_007_medium_hot_sweat_salt", {"distance_format": "medium", "weather": "hot", "caffeine_preference": "boost", "saddle_comfort": True, "price_tier": "standard"}),
    ("CYC_008_medium_cold_headwind_none_caff", {"distance_format": "medium", "weather": "cold", "caffeine_preference": "none", "saddle_comfort": True, "price_tier": "economy"}),
    ("CYC_009_medium_gravel_adventure_premium", {"distance_format": "medium", "weather": "moderate", "caffeine_preference": "boost", "saddle_comfort": True, "price_tier": "premium"}),
    ("CYC_010_medium_custom_budget_2600uah", {"distance_format": "medium", "weather": "hot", "caffeine_preference": "boost", "saddle_comfort": True, "custom_budget": 2600}),
    ("CYC_011_medium_custom_budget_3100uah", {"distance_format": "medium", "weather": "cold", "caffeine_preference": "none", "saddle_comfort": True, "custom_budget": 3100}),
    ("CYC_012_gran_fondo_120k_standard", {"distance_format": "long", "weather": "moderate", "caffeine_preference": "boost", "saddle_comfort": True, "price_tier": "standard"}),
    ("CYC_013_gran_fondo_hot_140k_salt_mag", {"distance_format": "long", "weather": "hot", "caffeine_preference": "boost", "saddle_comfort": True, "price_tier": "standard"}),
    ("CYC_014_century_160k_premium_maurten", {"distance_format": "long", "weather": "moderate", "caffeine_preference": "boost", "saddle_comfort": True, "price_tier": "premium"}),
    ("CYC_015_brevet_200k_none_caff_economy", {"distance_format": "long", "weather": "cold", "caffeine_preference": "none", "saddle_comfort": True, "price_tier": "economy"}),
    ("CYC_016_brevet_200k_boost_chamois_4500uah", {"distance_format": "long", "weather": "hot", "caffeine_preference": "boost", "saddle_comfort": True, "custom_budget": 4500}),
    ("CYC_017_bikepacking_day1_long_3800uah", {"distance_format": "long", "weather": "moderate", "caffeine_preference": "none", "saddle_comfort": True, "custom_budget": 3800}),
    ("CYC_018_mountain_pass_tour_long_premium", {"distance_format": "long", "weather": "cold", "caffeine_preference": "boost", "saddle_comfort": True, "price_tier": "premium"}),
    ("CYC_019_short_fitness_loop_economy", {"distance_format": "short", "weather": "moderate", "caffeine_preference": "none", "saddle_comfort": False, "price_tier": "economy"}),
    ("CYC_020_medium_paceline_boost_standard", {"distance_format": "medium", "weather": "moderate", "caffeine_preference": "boost", "saddle_comfort": True, "price_tier": "standard"}),
    ("CYC_021_long_alpine_granfondo_5200uah", {"distance_format": "long", "weather": "cold", "caffeine_preference": "boost", "saddle_comfort": True, "custom_budget": 5200}),
    ("CYC_022_short_evening_intervals_standard", {"distance_format": "short", "weather": "moderate", "caffeine_preference": "boost", "saddle_comfort": True, "price_tier": "standard"}),
    ("CYC_023_medium_windy_flat_none_caff", {"distance_format": "medium", "weather": "cold", "caffeine_preference": "none", "saddle_comfort": True, "price_tier": "standard"}),
    ("CYC_024_long_endurance_brevet_5800uah", {"distance_format": "long", "weather": "hot", "caffeine_preference": "boost", "saddle_comfort": True, "custom_budget": 5800}),
    ("CYC_025_short_commuter_speed_economy", {"distance_format": "short", "weather": "cold", "caffeine_preference": "none", "saddle_comfort": False, "price_tier": "economy"}),
    ("CYC_026_medium_spring_classic_standard", {"distance_format": "medium", "weather": "moderate", "caffeine_preference": "boost", "saddle_comfort": True, "price_tier": "standard"}),
    ("CYC_027_long_summer_solstice_none_caff", {"distance_format": "long", "weather": "hot", "caffeine_preference": "none", "saddle_comfort": True, "price_tier": "standard"}),
    ("CYC_028_short_track_warmup_premium", {"distance_format": "short", "weather": "moderate", "caffeine_preference": "boost", "saddle_comfort": True, "price_tier": "premium"}),
    ("CYC_029_medium_coastal_loop_2700uah", {"distance_format": "medium", "weather": "hot", "caffeine_preference": "boost", "saddle_comfort": True, "custom_budget": 2700}),
    ("CYC_030_long_gravel_century_4800uah", {"distance_format": "long", "weather": "moderate", "caffeine_preference": "boost", "saddle_comfort": True, "custom_budget": 4800}),
    ("CYC_031_short_climbing_intervals_none_caff", {"distance_format": "short", "weather": "cold", "caffeine_preference": "none", "saddle_comfort": True, "price_tier": "economy"}),
    ("CYC_032_medium_autumn_gravel_standard", {"distance_format": "medium", "weather": "cold", "caffeine_preference": "boost", "saddle_comfort": True, "price_tier": "standard"}),
    ("CYC_033_long_desert_granfondo_6500uah", {"distance_format": "long", "weather": "hot", "caffeine_preference": "boost", "saddle_comfort": True, "custom_budget": 6500}),
    ("CYC_034_short_rainy_spin_economy", {"distance_format": "short", "weather": "cold", "caffeine_preference": "none", "saddle_comfort": True, "price_tier": "economy"}),
    ("CYC_035_medium_hilly_challenge_premium", {"distance_format": "medium", "weather": "moderate", "caffeine_preference": "boost", "saddle_comfort": True, "price_tier": "premium"}),
    ("CYC_036_long_night_brevet_none_caff", {"distance_format": "long", "weather": "cold", "caffeine_preference": "none", "saddle_comfort": True, "price_tier": "economy"}),
    ("CYC_037_short_fast_peloton_standard", {"distance_format": "short", "weather": "moderate", "caffeine_preference": "boost", "saddle_comfort": True, "price_tier": "standard"}),
    ("CYC_038_medium_rolling_hills_3300uah", {"distance_format": "medium", "weather": "hot", "caffeine_preference": "boost", "saddle_comfort": True, "custom_budget": 3300}),
    ("CYC_039_long_iron_legs_220k_7200uah", {"distance_format": "long", "weather": "moderate", "caffeine_preference": "boost", "saddle_comfort": True, "custom_budget": 7200}),
    ("CYC_040_short_city_sprint_economy", {"distance_format": "short", "weather": "hot", "caffeine_preference": "none", "saddle_comfort": False, "price_tier": "economy"}),
    ("CYC_041_medium_gravel_grinder_boost", {"distance_format": "medium", "weather": "cold", "caffeine_preference": "boost", "saddle_comfort": True, "price_tier": "standard"}),
    ("CYC_042_long_altitude_pass_premium", {"distance_format": "long", "weather": "cold", "caffeine_preference": "boost", "saddle_comfort": True, "price_tier": "premium"}),
    ("CYC_043_medium_scenic_tour_2900uah", {"distance_format": "medium", "weather": "moderate", "caffeine_preference": "none", "saddle_comfort": True, "custom_budget": 2900}),
    ("CYC_044_long_trans_carpathian_8000uah", {"distance_format": "long", "weather": "hot", "caffeine_preference": "boost", "saddle_comfort": True, "custom_budget": 8000})
]

@pytest.mark.parametrize("scenario_id,inputs", CYCLING_SCENARIOS)
def test_e2e_cycling_scenario(live_server, scenario_id, inputs):
    box = post_generate_box(live_server, "cycling", inputs)
    assert_box_structure(box, "cycling", inputs)
    assert "Вело" in box["sport_label"] or "Вело" in box["distance_label"]


# ==============================================================================
# 3. TRIATHLON SCENARIOS (TRI_001 to TRI_044)
# ==============================================================================
TRIATHLON_SCENARIOS = [
    ("TRI_001_sprint_debut_boost_standard", {"format": "sprint", "caffeine_preference": "boost", "wetsuit_care": True, "price_tier": "standard"}),
    ("TRI_002_sprint_flat_none_caff_economy", {"format": "sprint", "caffeine_preference": "none", "wetsuit_care": True, "price_tier": "economy"}),
    ("TRI_003_sprint_cold_lake_triswim", {"format": "sprint", "caffeine_preference": "boost", "wetsuit_care": True, "price_tier": "premium"}),
    ("TRI_004_sprint_custom_budget_2800uah", {"format": "sprint", "caffeine_preference": "boost", "wetsuit_care": True, "custom_budget": 2800}),
    ("TRI_005_sprint_no_wetsuit_pool", {"format": "sprint", "caffeine_preference": "none", "wetsuit_care": False, "price_tier": "economy"}),
    ("TRI_006_olympic_standard_boost", {"format": "half", "caffeine_preference": "boost", "wetsuit_care": True, "price_tier": "standard"}),
    ("TRI_007_olympic_sea_swim_triswim", {"format": "half", "caffeine_preference": "boost", "wetsuit_care": True, "price_tier": "standard"}),
    ("TRI_008_olympic_none_caff_economy", {"format": "half", "caffeine_preference": "none", "wetsuit_care": True, "price_tier": "economy"}),
    ("TRI_009_olympic_custom_budget_3600uah", {"format": "half", "caffeine_preference": "boost", "wetsuit_care": True, "custom_budget": 3600}),
    ("TRI_010_half_ironman_703_debut", {"format": "half", "caffeine_preference": "boost", "wetsuit_care": True, "price_tier": "standard"}),
    ("TRI_011_half_ironman_sub5hr_premium", {"format": "half", "caffeine_preference": "boost", "wetsuit_care": True, "price_tier": "premium"}),
    ("TRI_012_half_ironman_hot_bahrain_salt", {"format": "half", "caffeine_preference": "boost", "wetsuit_care": True, "price_tier": "standard"}),
    ("TRI_013_half_ironman_none_caff_economy", {"format": "half", "caffeine_preference": "none", "wetsuit_care": True, "price_tier": "economy"}),
    ("TRI_014_half_ironman_custom_4900uah", {"format": "half", "caffeine_preference": "boost", "wetsuit_care": True, "custom_budget": 4900}),
    ("TRI_015_half_ironman_custom_5800uah", {"format": "half", "caffeine_preference": "none", "wetsuit_care": True, "custom_budget": 5800}),
    ("TRI_016_full_ironman_1406_kona_qual", {"format": "full", "caffeine_preference": "boost", "wetsuit_care": True, "price_tier": "premium"}),
    ("TRI_017_full_ironman_standard_drinkmix", {"format": "full", "caffeine_preference": "boost", "wetsuit_care": True, "price_tier": "standard"}),
    ("TRI_018_full_ironman_none_caff_chews", {"format": "full", "caffeine_preference": "none", "wetsuit_care": True, "price_tier": "standard"}),
    ("TRI_019_full_ironman_extreme_heat_salt", {"format": "full", "caffeine_preference": "boost", "wetsuit_care": True, "price_tier": "premium"}),
    ("TRI_020_full_ironman_custom_7800uah", {"format": "full", "caffeine_preference": "boost", "wetsuit_care": True, "custom_budget": 7800}),
    ("TRI_021_full_ironman_custom_9500uah", {"format": "full", "caffeine_preference": "boost", "wetsuit_care": True, "custom_budget": 9500}),
    ("TRI_022_open_water_1500m_lake", {"format": "swim", "caffeine_preference": "none", "wetsuit_care": True, "price_tier": "economy"}),
    ("TRI_023_open_water_3000m_river_boost", {"format": "swim", "caffeine_preference": "boost", "wetsuit_care": True, "price_tier": "standard"}),
    ("TRI_024_open_water_5000m_sea_marathon", {"format": "swim", "caffeine_preference": "boost", "wetsuit_care": True, "price_tier": "premium"}),
    ("TRI_025_open_water_bosphorus_cross", {"format": "swim", "caffeine_preference": "boost", "wetsuit_care": True, "custom_budget": 2900}),
    ("TRI_026_sprint_junior_national_cup", {"format": "sprint", "caffeine_preference": "none", "wetsuit_care": True, "price_tier": "standard"}),
    ("TRI_027_703_rainy_luxembourg_chafe", {"format": "half", "caffeine_preference": "boost", "wetsuit_care": True, "price_tier": "standard"}),
    ("TRI_028_1406_windy_lanzarote_flasks", {"format": "full", "caffeine_preference": "boost", "wetsuit_care": True, "price_tier": "premium"}),
    ("TRI_029_open_water_cold_wetsuit_care", {"format": "swim", "caffeine_preference": "none", "wetsuit_care": True, "price_tier": "economy"}),
    ("TRI_030_sprint_corporate_relay_fast", {"format": "sprint", "caffeine_preference": "boost", "wetsuit_care": True, "price_tier": "economy"}),
    ("TRI_031_703_sub430_elite_maurten", {"format": "half", "caffeine_preference": "boost", "wetsuit_care": True, "price_tier": "premium"}),
    ("TRI_032_1406_first_timer_economy", {"format": "full", "caffeine_preference": "none", "wetsuit_care": True, "price_tier": "economy"}),
    ("TRI_033_open_water_ocean_swim_salt", {"format": "swim", "caffeine_preference": "none", "wetsuit_care": True, "price_tier": "standard"}),
    ("TRI_034_sprint_autumn_cross_triathlon", {"format": "sprint", "caffeine_preference": "boost", "wetsuit_care": True, "custom_budget": 2400}),
    ("TRI_035_703_coastal_nice_challenge", {"format": "half", "caffeine_preference": "boost", "wetsuit_care": True, "custom_budget": 5200}),
    ("TRI_036_1406_roth_record_pace_11000uah", {"format": "full", "caffeine_preference": "boost", "wetsuit_care": True, "custom_budget": 11000}),
    ("TRI_037_open_water_night_swim_none_caff", {"format": "swim", "caffeine_preference": "none", "wetsuit_care": True, "price_tier": "economy"}),
    ("TRI_038_sprint_fast_transitions_belt", {"format": "sprint", "caffeine_preference": "boost", "wetsuit_care": True, "price_tier": "standard"}),
    ("TRI_039_703_mountain_climb_austria", {"format": "half", "caffeine_preference": "boost", "wetsuit_care": True, "price_tier": "premium"}),
    ("TRI_040_1406_desert_texas_heat_salt", {"format": "full", "caffeine_preference": "boost", "wetsuit_care": True, "custom_budget": 8500}),
    ("TRI_041_open_water_danube_island_swim", {"format": "swim", "caffeine_preference": "boost", "wetsuit_care": True, "price_tier": "standard"}),
    ("TRI_042_sprint_indoor_winter_tri", {"format": "sprint", "caffeine_preference": "none", "wetsuit_care": False, "price_tier": "economy"}),
    ("TRI_043_703_first_time_finish_4200uah", {"format": "half", "caffeine_preference": "none", "wetsuit_care": True, "custom_budget": 4200}),
    ("TRI_044_1406_world_championship_pro", {"format": "full", "caffeine_preference": "boost", "wetsuit_care": True, "price_tier": "premium"})
]

@pytest.mark.parametrize("scenario_id,inputs", TRIATHLON_SCENARIOS)
def test_e2e_triathlon_scenario(live_server, scenario_id, inputs):
    box = post_generate_box(live_server, "triathlon", inputs)
    assert_box_structure(box, "triathlon", inputs)
    assert "Триатлон" in box["sport_label"] or "плавання" in box["sport_label"]


# ==============================================================================
# 4. GYM & FITNESS SCENARIOS (GYM_001 to GYM_044)
# ==============================================================================
GYM_SCENARIOS = [
    ("GYM_001_hypertrophy_mass_caffeine_pre", {"goal": "mass", "pre_workout_boost": "caffeine", "price_tier": "standard"}),
    ("GYM_002_mass_hardgainer_premium", {"goal": "mass", "pre_workout_boost": "caffeine", "price_tier": "premium"}),
    ("GYM_003_mass_zero_stim_beta_alanine", {"goal": "mass", "pre_workout_boost": "beta_alanine", "price_tier": "standard"}),
    ("GYM_004_mass_night_workout_none_caff", {"goal": "mass", "pre_workout_boost": "none", "price_tier": "economy"}),
    ("GYM_005_mass_custom_budget_3500uah", {"goal": "mass", "pre_workout_boost": "caffeine", "custom_budget": 3500}),
    ("GYM_006_mass_custom_budget_4400uah", {"goal": "mass", "pre_workout_boost": "beta_alanine", "custom_budget": 4400}),
    ("GYM_007_lean_cut_shred_caffeine", {"goal": "lean", "pre_workout_boost": "caffeine", "price_tier": "standard"}),
    ("GYM_008_lean_cut_summer_body_premium", {"goal": "lean", "pre_workout_boost": "caffeine", "price_tier": "premium"}),
    ("GYM_009_lean_cut_zero_stim_l_carnitine", {"goal": "lean", "pre_workout_boost": "none", "price_tier": "standard"}),
    ("GYM_010_lean_cut_beta_alanine_economy", {"goal": "lean", "pre_workout_boost": "beta_alanine", "price_tier": "economy"}),
    ("GYM_011_lean_cut_custom_budget_3900uah", {"goal": "lean", "pre_workout_boost": "caffeine", "custom_budget": 3900}),
    ("GYM_012_lean_cut_custom_budget_4900uah", {"goal": "lean", "pre_workout_boost": "none", "custom_budget": 4900}),
    ("GYM_013_powerlifting_max_strength_caff", {"goal": "strength", "pre_workout_boost": "caffeine", "price_tier": "premium"}),
    ("GYM_014_strength_creatine_heavy_standard", {"goal": "strength", "pre_workout_boost": "caffeine", "price_tier": "standard"}),
    ("GYM_015_strength_zero_caff_beta_alanine", {"goal": "strength", "pre_workout_boost": "beta_alanine", "price_tier": "standard"}),
    ("GYM_016_strength_evening_economy", {"goal": "strength", "pre_workout_boost": "none", "price_tier": "economy"}),
    ("GYM_017_strength_custom_budget_4100uah", {"goal": "strength", "pre_workout_boost": "caffeine", "custom_budget": 4100}),
    ("GYM_018_crossfit_functional_tone_boost", {"goal": "tone", "pre_workout_boost": "caffeine", "price_tier": "standard"}),
    ("GYM_019_crossfit_hiit_stamina_beta_alanine", {"goal": "tone", "pre_workout_boost": "beta_alanine", "price_tier": "standard"}),
    ("GYM_020_tone_vegan_plant_protein_none_caff", {"goal": "tone", "pre_workout_boost": "none", "price_tier": "economy"}),
    ("GYM_021_tone_custom_budget_3300uah", {"goal": "tone", "pre_workout_boost": "caffeine", "custom_budget": 3300}),
    ("GYM_022_mass_winter_bulking_season", {"goal": "mass", "pre_workout_boost": "caffeine", "price_tier": "standard"}),
    ("GYM_023_lean_contest_prep_cla_isolate", {"goal": "lean", "pre_workout_boost": "caffeine", "price_tier": "premium"}),
    ("GYM_024_strength_deadlift_focus_creatine", {"goal": "strength", "pre_workout_boost": "caffeine", "price_tier": "standard"}),
    ("GYM_025_tone_pilates_hybrid_none_caff", {"goal": "tone", "pre_workout_boost": "none", "price_tier": "economy"}),
    ("GYM_026_mass_college_student_economy", {"goal": "mass", "pre_workout_boost": "none", "price_tier": "economy"}),
    ("GYM_027_lean_fat_loss_metabolism_boost", {"goal": "lean", "pre_workout_boost": "caffeine", "price_tier": "standard"}),
    ("GYM_028_strength_power_builder_5500uah", {"goal": "strength", "pre_workout_boost": "caffeine", "custom_budget": 5500}),
    ("GYM_029_tone_calisthenics_bcaa_recovery", {"goal": "tone", "pre_workout_boost": "beta_alanine", "price_tier": "standard"}),
    ("GYM_030_mass_bcaa_intra_workout_protect", {"goal": "mass", "pre_workout_boost": "beta_alanine", "price_tier": "standard"}),
    ("GYM_031_lean_ketogenic_cut_zero_sugar", {"goal": "lean", "pre_workout_boost": "none", "price_tier": "premium"}),
    ("GYM_032_strength_bench_press_max_session", {"goal": "strength", "pre_workout_boost": "caffeine", "price_tier": "standard"}),
    ("GYM_033_tone_morning_bootcamp_boost", {"goal": "tone", "pre_workout_boost": "caffeine", "price_tier": "economy"}),
    ("GYM_034_mass_6day_push_pull_legs", {"goal": "mass", "pre_workout_boost": "caffeine", "custom_budget": 4800}),
    ("GYM_035_lean_intermittent_fasting_bcaa", {"goal": "lean", "pre_workout_boost": "beta_alanine", "price_tier": "standard"}),
    ("GYM_036_strength_strongman_heavy_duty", {"goal": "strength", "pre_workout_boost": "caffeine", "price_tier": "premium"}),
    ("GYM_037_tone_crossfit_open_prep", {"goal": "tone", "pre_workout_boost": "caffeine", "custom_budget": 3700}),
    ("GYM_038_mass_post_workout_protein_bars", {"goal": "mass", "pre_workout_boost": "none", "price_tier": "standard"}),
    ("GYM_039_lean_summer_abs_quick_cut", {"goal": "lean", "pre_workout_boost": "caffeine", "custom_budget": 3400}),
    ("GYM_040_strength_squat_master_joints", {"goal": "strength", "pre_workout_boost": "beta_alanine", "price_tier": "standard"}),
    ("GYM_041_tone_kettlebell_flow_recovery", {"goal": "tone", "pre_workout_boost": "none", "price_tier": "economy"}),
    ("GYM_042_mass_optimum_gold_standard", {"goal": "mass", "pre_workout_boost": "caffeine", "price_tier": "premium"}),
    ("GYM_043_lean_women_fitness_tone_up", {"goal": "lean", "pre_workout_boost": "none", "price_tier": "standard"}),
    ("GYM_044_strength_olympic_weightlifting", {"goal": "strength", "pre_workout_boost": "caffeine", "custom_budget": 5000})
]

@pytest.mark.parametrize("scenario_id,inputs", GYM_SCENARIOS)
def test_e2e_gym_scenario(live_server, scenario_id, inputs):
    box = post_generate_box(live_server, "gym", inputs)
    assert_box_structure(box, "gym", inputs)
    label_lower = box["sport_label"].lower()
    assert "фітнес" in label_lower or "зал" in label_lower
    # Check that shaker is recommended in gear slot
    assert any(it["product"].get("sub_type") == "shaker" for it in box["slots"]["gear"]), "Gym box must include shaker"


# ==============================================================================
# 5. HIKING & OUTDOOR SCENARIOS (OUT_001 to OUT_044)
# ==============================================================================
OUTDOOR_SCENARIOS = [
    ("OUT_001_day_hike_hoverla_ascent", {"duration": "1day", "diet": "standard", "price_tier": "economy"}),
    ("OUT_002_day_hike_forest_canyon_premium", {"duration": "1day", "diet": "standard", "price_tier": "premium"}),
    ("OUT_003_day_hike_vegan_energy_bars", {"duration": "1day", "diet": "vegan", "price_tier": "standard"}),
    ("OUT_004_day_hike_winter_hot_soup", {"duration": "1day", "diet": "meat", "price_tier": "standard"}),
    ("OUT_005_day_hike_custom_budget_2100uah", {"duration": "1day", "diet": "standard", "custom_budget": 2100}),
    ("OUT_006_weekend_borzhava_ridge_trek", {"duration": "weekend", "diet": "standard", "price_tier": "standard"}),
    ("OUT_007_weekend_gorgany_rocky_crossing", {"duration": "weekend", "diet": "meat", "price_tier": "premium"}),
    ("OUT_008_weekend_vegan_dehydrated_porridge", {"duration": "weekend", "diet": "vegan", "price_tier": "standard"}),
    ("OUT_009_weekend_rainy_camping_magnesium", {"duration": "weekend", "diet": "standard", "price_tier": "standard"}),
    ("OUT_010_weekend_custom_budget_3600uah", {"duration": "weekend", "diet": "meat", "custom_budget": 3600}),
    ("OUT_011_weekend_custom_budget_4400uah", {"duration": "weekend", "diet": "vegan", "custom_budget": 4400}),
    ("OUT_012_expedition_chornohora_traverse_6days", {"duration": "expedition", "diet": "meat", "price_tier": "premium"}),
    ("OUT_013_expedition_svaneti_alpine_crossing", {"duration": "expedition", "diet": "standard", "price_tier": "premium"}),
    ("OUT_014_expedition_winter_survival_jerky", {"duration": "expedition", "diet": "meat", "price_tier": "standard"}),
    ("OUT_015_expedition_vegan_autonomous_pack", {"duration": "expedition", "diet": "vegan", "price_tier": "standard"}),
    ("OUT_016_expedition_custom_budget_6500uah", {"duration": "expedition", "diet": "meat", "custom_budget": 6500}),
    ("OUT_017_expedition_custom_budget_7900uah", {"duration": "expedition", "diet": "standard", "custom_budget": 7900}),
    ("OUT_018_day_hike_fastpack_ultralight", {"duration": "1day", "diet": "standard", "price_tier": "standard"}),
    ("OUT_019_weekend_scout_troop_economy", {"duration": "weekend", "diet": "meat", "price_tier": "economy"}),
    ("OUT_020_expedition_polar_gear_socks_balm", {"duration": "expedition", "diet": "meat", "price_tier": "premium"}),
    ("OUT_021_day_hike_family_picnic_snack", {"duration": "1day", "diet": "standard", "price_tier": "economy"}),
    ("OUT_022_weekend_mountain_bike_packing", {"duration": "weekend", "diet": "standard", "price_tier": "standard"}),
    ("OUT_023_expedition_tatras_ridge_trail", {"duration": "expedition", "diet": "standard", "custom_budget": 7200}),
    ("OUT_024_day_hike_autumn_mushrooms_trail", {"duration": "1day", "diet": "vegan", "price_tier": "economy"}),
    ("OUT_025_weekend_climbing_crag_camp", {"duration": "weekend", "diet": "meat", "price_tier": "standard"}),
    ("OUT_026_expedition_norway_fjords_trek", {"duration": "expedition", "diet": "meat", "price_tier": "premium"}),
    ("OUT_027_day_hike_summer_lake_swim", {"duration": "1day", "diet": "standard", "price_tier": "standard"}),
    ("OUT_028_weekend_bushcraft_survival", {"duration": "weekend", "diet": "meat", "price_tier": "economy"}),
    ("OUT_029_expedition_lycian_way_coastal", {"duration": "expedition", "diet": "standard", "custom_budget": 6800}),
    ("OUT_030_day_hike_sunrise_peak_climb", {"duration": "1day", "diet": "meat", "price_tier": "standard"}),
    ("OUT_031_weekend_canyon_backpacking", {"duration": "weekend", "diet": "vegan", "price_tier": "premium"}),
    ("OUT_032_expedition_alps_tour_du_mont_blanc", {"duration": "expedition", "diet": "standard", "custom_budget": 8500}),
    ("OUT_033_day_hike_birdwatching_trail", {"duration": "1day", "diet": "vegan", "price_tier": "economy"}),
    ("OUT_034_weekend_river_kayak_tour", {"duration": "weekend", "diet": "standard", "price_tier": "standard"}),
    ("OUT_035_expedition_iceland_highlands", {"duration": "expedition", "diet": "meat", "price_tier": "premium"}),
    ("OUT_036_day_hike_geocaching_adventure", {"duration": "1day", "diet": "standard", "price_tier": "economy"}),
    ("OUT_037_weekend_stargazing_camp", {"duration": "weekend", "diet": "standard", "price_tier": "standard"}),
    ("OUT_038_expedition_patagonia_trek", {"duration": "expedition", "diet": "meat", "custom_budget": 9200}),
    ("OUT_039_day_hike_spring_waterfall_walk", {"duration": "1day", "diet": "vegan", "price_tier": "standard"}),
    ("OUT_040_weekend_foraging_wild_trail", {"duration": "weekend", "diet": "vegan", "price_tier": "economy"}),
    ("OUT_041_expedition_himalayan_basecamp", {"duration": "expedition", "diet": "standard", "price_tier": "premium"}),
    ("OUT_042_day_hike_coastal_cliff_path", {"duration": "1day", "diet": "meat", "price_tier": "standard"}),
    ("OUT_043_weekend_cave_exploration_camp", {"duration": "weekend", "diet": "meat", "custom_budget": 4100}),
    ("OUT_044_expedition_alta_via_dolomites", {"duration": "expedition", "diet": "meat", "custom_budget": 7700})
]

@pytest.mark.parametrize("scenario_id,inputs", OUTDOOR_SCENARIOS)
def test_e2e_outdoor_scenario(live_server, scenario_id, inputs):
    box = post_generate_box(live_server, "outdoor", inputs)
    assert_box_structure(box, "outdoor", inputs)
    assert "Походи" in box["sport_label"] or "ЇDLO" in box["sport_label"]


# ==============================================================================
# 6. CART PAYLOAD & INTERACTIVE INVARIANTS (INT_001 to INT_005)
# ==============================================================================
def test_e2e_opencart_atomic_bulk_cart_payload(live_server):
    """Test generating a multi-sport box and transforming it into OpenCart bulk payload."""
    box = post_generate_box(live_server, "running", {"distance": "21k", "caffeine_preference": "boost"})
    items_to_add = []
    for s_name, s_items in box["slots"].items():
        for it in s_items:
            items_to_add.append({
                "product_id": it["product"]["product_id"],
                "quantity": it["quantity_recommended"]
            })
    assert len(items_to_add) >= 4, "Must generate at least 4 items for bulk cart"
    payload = {"items": items_to_add}
    assert all(it["product_id"] > 0 for it in payload["items"])
    assert all(it["quantity"] > 0 for it in payload["items"])


def test_e2e_interactive_deselection_price_drop(live_server):
    """Simulate deselecting an item and verify resulting price matches math."""
    box = post_generate_box(live_server, "cycling", {"distance_format": "long", "caffeine_preference": "boost"})
    initial_price = box["total_base_price"]
    first_item = box["slots"]["energy"][0]
    drop_amount = first_item["product"]["price"] * first_item["quantity_recommended"]
    new_price = round(initial_price - drop_amount, 2)
    assert new_price < initial_price
    assert new_price > 0


def test_e2e_path_traversal_forbidden(live_server):
    """Ensure server blocks path traversal and forbidden file accesses."""
    for forbidden_path in [
        "/../server.py",
        "/../../etc/passwd",
        "/server.py",
        "/.env",
        "/Dockerfile",
        "/docker-compose.yml"
    ]:
        req = urllib.request.Request(f"{live_server}{forbidden_path}")
        try:
            with urllib.request.urlopen(req, timeout=3) as resp:
                assert resp.status in (403, 404), f"Path {forbidden_path} should be blocked"
        except urllib.error.HTTPError as e:
            assert e.code in (403, 404), f"Expected 403 or 404 for {forbidden_path}, got {e.code}"


def test_e2e_post_bad_length_and_type(live_server):
    """Ensure POST endpoint rejects empty or non-dict bodies with 400."""
    # Empty body
    req_empty = urllib.request.Request(
        f"{live_server}/api/generate-sport-box",
        data=b"",
        headers={"Content-Type": "application/json"}
    )
    try:
        urllib.request.urlopen(req_empty, timeout=3)
        pytest.fail("Empty body should be rejected")
    except urllib.error.HTTPError as e:
        assert e.code == 400

    # Non-dict JSON (array)
    req_array = urllib.request.Request(
        f"{live_server}/api/generate-sport-box",
        data=b"[1, 2, 3]",
        headers={"Content-Type": "application/json"}
    )
    try:
        urllib.request.urlopen(req_array, timeout=3)
        pytest.fail("Array JSON should be rejected")
    except urllib.error.HTTPError as e:
        assert e.code == 400


def test_e2e_live_stock_check_sanitization(live_server):
    """Ensure /api/check-stock handles messy SKU inputs with backslashes and nulls safely."""
    payload = {"skus": ["RE89450", "RE123\\", "INVALID'", None, 12345]}
    req = urllib.request.Request(
        f"{live_server}/api/check-stock",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=5) as resp:
        assert resp.status == 200
        data = json.loads(resp.read().decode("utf-8"))
        assert data["ok"] is True
        assert "stocks" in data
