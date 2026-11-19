"""Suite of 50 Comprehensive Runner Personas & Scenarios for Race Expert Starter Box.

Validates that all 50 distinct runner personas receive a deterministic, physiological,
expert-grade starter box strictly aligned with:
1. Single Gel Brand Rule (Zero brand mixing in energy slot)
2. Zero Caffeine Leaks when caffeine_preference == 'none'
3. Guaranteed Caffeine Boost gel matching primary brand when caffeine_preference == 'boost'
4. Hot Weather / Cramps salt capsule injection
5. Sizing selector pills on running socks
6. In-stock guarantee and price validity (quantity > 0, price > 0, within custom budget)
7. Non-empty slots (all 4 slots: energy, hydration, gear, care_recovery)
8. Item deselection and cart payload calculations
"""

import json
from pathlib import Path
import pytest
from runner_box_engine import generate_runner_box

# Load catalog once for test session
CATALOG_PATH = Path(__file__).resolve().parent / "running_catalog.json"
with open(CATALOG_PATH, "r", encoding="utf-8") as f:
    CATALOG = json.load(f)


@pytest.fixture(scope="module")
def running_catalog():
    return CATALOG


SCENARIOS = [
    # =========================================================================
    # GROUP 1: 10K DISTANCE RUNNERS (Scenarios 1-12)
    # =========================================================================
    {
        "id": 1,
        "name": "10k Beginner Debutant (Cold, Finish, Economy, Zero Caffeine)",
        "inputs": {
            "distance": "10k",
            "pace_target": "finish",
            "weather": "cold",
            "stomach_type": "normal",
            "caffeine_preference": "none",
            "body_concerns": [],
            "gear_needed": [],
            "price_tier": "economy"
        },
        "deselect": {"sub_types": ["running_belt"]}
    },
    {
        "id": 2,
        "name": "10k PB Chaser Sub-40min (Moderate, Record, Standard, Caffeine Boost)",
        "inputs": {
            "distance": "10k",
            "pace_target": "record",
            "weather": "moderate",
            "stomach_type": "normal",
            "caffeine_preference": "boost",
            "body_concerns": [],
            "gear_needed": ["socks"],
            "price_tier": "standard"
        },
        "deselect": {"sub_types": ["running_socks"]}
    },
    {
        "id": 3,
        "name": "10k Hot Summer Night Run (Hot, Cramps, Standard, Budget 1200)",
        "inputs": {
            "distance": "10k",
            "pace_target": "steady",
            "weather": "hot",
            "stomach_type": "normal",
            "caffeine_preference": "none",
            "body_concerns": ["cramps"],
            "gear_needed": ["belt"],
            "custom_budget": 1200.0
        },
        "deselect": {"slots": ["gear"]}
    },
    {
        "id": 4,
        "name": "10k Sensitive Stomach Hydrogel (Moderate, Steady, Sensitive, Premium)",
        "inputs": {
            "distance": "10k",
            "pace_target": "steady",
            "weather": "moderate",
            "stomach_type": "sensitive",
            "caffeine_preference": "none",
            "body_concerns": [],
            "gear_needed": ["socks"],
            "price_tier": "premium"
        },
        "deselect": {"sub_types": ["running_socks"]}
    },
    {
        "id": 5,
        "name": "10k Vegan Sprint Master (Moderate, Record, Vegan, Boost, Standard)",
        "inputs": {
            "distance": "10k",
            "pace_target": "record",
            "weather": "moderate",
            "stomach_type": "vegan",
            "caffeine_preference": "boost",
            "body_concerns": ["chafing"],
            "gear_needed": [],
            "price_tier": "standard"
        },
        "deselect": {"sub_types": ["anti_chafe"]}
    },
    {
        "id": 6,
        "name": "10k Budget Student Runner (Cold, Finish, Normal, None, Budget 800)",
        "inputs": {
            "distance": "10k",
            "pace_target": "finish",
            "weather": "cold",
            "stomach_type": "normal",
            "caffeine_preference": "none",
            "body_concerns": [],
            "gear_needed": ["belt"],
            "custom_budget": 800.0
        },
        "deselect": {"slots": ["care_recovery"]}
    },
    {
        "id": 7,
        "name": "10k Masters Joint Care (Cold, Steady, Normal, None, Joints, Standard)",
        "inputs": {
            "distance": "10k",
            "pace_target": "steady",
            "weather": "cold",
            "stomach_type": "normal",
            "caffeine_preference": "none",
            "body_concerns": ["joints"],
            "gear_needed": ["socks"],
            "price_tier": "standard"
        },
        "deselect": {"sub_types": ["joint_care"]}
    },
    {
        "id": 8,
        "name": "10k Hot Noon with Chafing (Hot, Steady, Normal, Boost, Cramps+Chafing)",
        "inputs": {
            "distance": "10k",
            "pace_target": "steady",
            "weather": "hot",
            "stomach_type": "normal",
            "caffeine_preference": "boost",
            "body_concerns": ["cramps", "chafing"],
            "gear_needed": ["flask"],
            "price_tier": "standard"
        },
        "deselect": {"slots": ["gear"]}
    },
    {
        "id": 9,
        "name": "10k Elite Pro Maurten/PF&H (Moderate, Record, Normal, Boost, Budget 2000)",
        "inputs": {
            "distance": "10k",
            "pace_target": "record",
            "weather": "moderate",
            "stomach_type": "normal",
            "caffeine_preference": "boost",
            "body_concerns": [],
            "gear_needed": ["belt", "socks"],
            "custom_budget": 2000.0
        },
        "deselect": {"sub_types": ["running_belt"]}
    },
    {
        "id": 10,
        "name": "10k Corporate Team Debut (Moderate, Finish, Normal, None, Budget 1000)",
        "inputs": {
            "distance": "10k",
            "pace_target": "finish",
            "weather": "moderate",
            "stomach_type": "normal",
            "caffeine_preference": "none",
            "body_concerns": [],
            "gear_needed": ["belt"],
            "custom_budget": 1000.0
        },
        "deselect": {"sub_types": ["running_belt"]}
    },
    {
        "id": 11,
        "name": "10k Vegan Hot Summer Jogger (Hot, Steady, Vegan, None, Cramps, Standard)",
        "inputs": {
            "distance": "10k",
            "pace_target": "steady",
            "weather": "hot",
            "stomach_type": "vegan",
            "caffeine_preference": "none",
            "body_concerns": ["cramps"],
            "gear_needed": ["flask"],
            "price_tier": "standard"
        },
        "deselect": {"sub_types": ["soft_flask"]}
    },
    {
        "id": 12,
        "name": "10k Sensitive GI PB Seeker (Cold, Record, Sensitive, Boost, Budget 1500)",
        "inputs": {
            "distance": "10k",
            "pace_target": "record",
            "weather": "cold",
            "stomach_type": "sensitive",
            "caffeine_preference": "boost",
            "body_concerns": ["chafing"],
            "gear_needed": ["socks"],
            "custom_budget": 1500.0
        },
        "deselect": {"slots": ["care_recovery"]}
    },

    # =========================================================================
    # GROUP 2: 21K HALF MARATHON RUNNERS (Scenarios 13-28)
    # =========================================================================
    {
        "id": 13,
        "name": "21k First Half Marathon Finisher (Moderate, Finish, Normal, None, Economy)",
        "inputs": {
            "distance": "21k",
            "pace_target": "finish",
            "weather": "moderate",
            "stomach_type": "normal",
            "caffeine_preference": "none",
            "body_concerns": [],
            "gear_needed": ["belt"],
            "price_tier": "economy"
        },
        "deselect": {"sub_types": ["running_belt"]}
    },
    {
        "id": 14,
        "name": "21k Steady Half Pacer Sub-1:45 (Moderate, Steady, Normal, Boost, Standard)",
        "inputs": {
            "distance": "21k",
            "pace_target": "steady",
            "weather": "moderate",
            "stomach_type": "normal",
            "caffeine_preference": "boost",
            "body_concerns": [],
            "gear_needed": ["belt", "socks"],
            "price_tier": "standard"
        },
        "deselect": {"sub_types": ["running_socks"]}
    },
    {
        "id": 15,
        "name": "21k Sub-1:20 Record Racer (Cold, Record, Normal, Boost, Premium)",
        "inputs": {
            "distance": "21k",
            "pace_target": "record",
            "weather": "cold",
            "stomach_type": "normal",
            "caffeine_preference": "boost",
            "body_concerns": [],
            "gear_needed": ["belt", "flask", "socks"],
            "price_tier": "premium"
        },
        "deselect": {"sub_types": ["soft_flask"]}
    },
    {
        "id": 16,
        "name": "21k Hot Summer Half with Cramps (Hot, Steady, Normal, None, Cramps, Standard)",
        "inputs": {
            "distance": "21k",
            "pace_target": "steady",
            "weather": "hot",
            "stomach_type": "normal",
            "caffeine_preference": "none",
            "body_concerns": ["cramps"],
            "gear_needed": ["flask"],
            "price_tier": "standard"
        },
        "deselect": {"slots": ["gear"]}
    },
    {
        "id": 17,
        "name": "21k Sensitive Stomach Runner (Moderate, Steady, Sensitive, None, Standard)",
        "inputs": {
            "distance": "21k",
            "pace_target": "steady",
            "weather": "moderate",
            "stomach_type": "sensitive",
            "caffeine_preference": "none",
            "body_concerns": ["chafing"],
            "gear_needed": ["socks"],
            "price_tier": "standard"
        },
        "deselect": {"sub_types": ["anti_chafe"]}
    },
    {
        "id": 18,
        "name": "21k Sensitive Gut + Boost (Cold, Record, Sensitive, Boost, Budget 2500)",
        "inputs": {
            "distance": "21k",
            "pace_target": "record",
            "weather": "cold",
            "stomach_type": "sensitive",
            "caffeine_preference": "boost",
            "body_concerns": ["chafing"],
            "gear_needed": ["belt", "socks"],
            "custom_budget": 2500.0
        },
        "deselect": {"sub_types": ["running_belt"]}
    },
    {
        "id": 19,
        "name": "21k Vegan Endurance Athlete (Moderate, Steady, Vegan, Boost, Standard)",
        "inputs": {
            "distance": "21k",
            "pace_target": "steady",
            "weather": "moderate",
            "stomach_type": "vegan",
            "caffeine_preference": "boost",
            "body_concerns": [],
            "gear_needed": ["belt"],
            "price_tier": "standard"
        },
        "deselect": {"slots": ["care_recovery"]}
    },
    {
        "id": 20,
        "name": "21k Vegan Zero-Caffeine Pure Energy (Cold, Finish, Vegan, None, Budget 1200)",
        "inputs": {
            "distance": "21k",
            "pace_target": "finish",
            "weather": "cold",
            "stomach_type": "vegan",
            "caffeine_preference": "none",
            "body_concerns": [],
            "gear_needed": [],
            "custom_budget": 1200.0
        },
        "deselect": {"sub_types": ["running_belt"]}
    },
    {
        "id": 21,
        "name": "21k Knee & Hip Joint Protection (Moderate, Steady, Normal, None, Joints, Standard)",
        "inputs": {
            "distance": "21k",
            "pace_target": "steady",
            "weather": "moderate",
            "stomach_type": "normal",
            "caffeine_preference": "none",
            "body_concerns": ["joints"],
            "gear_needed": ["socks"],
            "price_tier": "standard"
        },
        "deselect": {"sub_types": ["joint_care"]}
    },
    {
        "id": 22,
        "name": "21k Severe Chafing Risk (Hot, Steady, Normal, Boost, Chafing, Standard)",
        "inputs": {
            "distance": "21k",
            "pace_target": "steady",
            "weather": "hot",
            "stomach_type": "normal",
            "caffeine_preference": "boost",
            "body_concerns": ["chafing", "cramps"],
            "gear_needed": ["flask", "socks"],
            "price_tier": "standard"
        },
        "deselect": {"slots": ["gear"]}
    },
    {
        "id": 23,
        "name": "21k High Budget PRO Athlete (Moderate, Record, Normal, Boost, Budget 3000)",
        "inputs": {
            "distance": "21k",
            "pace_target": "record",
            "weather": "moderate",
            "stomach_type": "normal",
            "caffeine_preference": "boost",
            "body_concerns": ["chafing", "joints"],
            "gear_needed": ["belt", "flask", "socks"],
            "custom_budget": 3000.0
        },
        "deselect": {"sub_types": ["soft_flask"]}
    },
    {
        "id": 24,
        "name": "21k Tight Budget Half Marathoner (Moderate, Finish, Normal, None, Budget 1400)",
        "inputs": {
            "distance": "21k",
            "pace_target": "finish",
            "weather": "moderate",
            "stomach_type": "normal",
            "caffeine_preference": "none",
            "body_concerns": [],
            "gear_needed": ["socks"],
            "custom_budget": 1400.0
        },
        "deselect": {"sub_types": ["running_socks"]}
    },
    {
        "id": 25,
        "name": "21k Hot Midday Scorcher (Hot, Record, Normal, Boost, Cramps+Chafing, Premium)",
        "inputs": {
            "distance": "21k",
            "pace_target": "record",
            "weather": "hot",
            "stomach_type": "normal",
            "caffeine_preference": "boost",
            "body_concerns": ["cramps", "chafing"],
            "gear_needed": ["belt", "flask"],
            "price_tier": "premium"
        },
        "deselect": {"sub_types": ["running_belt"]}
    },
    {
        "id": 26,
        "name": "21k Cold Rainy Half (Cold, Steady, Normal, None, Chafing+Joints, Budget 2600)",
        "inputs": {
            "distance": "21k",
            "pace_target": "steady",
            "weather": "cold",
            "stomach_type": "normal",
            "caffeine_preference": "none",
            "body_concerns": ["chafing", "joints"],
            "gear_needed": ["belt", "socks"],
            "custom_budget": 2600.0
        },
        "deselect": {"slots": ["care_recovery"]}
    },
    {
        "id": 27,
        "name": "21k Triple Concern Heavy Runner (Moderate, Finish, Sensitive, None, Cramps+Chafing+Joints)",
        "inputs": {
            "distance": "21k",
            "pace_target": "finish",
            "weather": "moderate",
            "stomach_type": "sensitive",
            "caffeine_preference": "none",
            "body_concerns": ["cramps", "chafing", "joints"],
            "gear_needed": ["socks"],
            "price_tier": "standard"
        },
        "deselect": {"sub_types": ["anti_chafe"]}
    },
    {
        "id": 28,
        "name": "21k Hydrogel Performance (Moderate, Record, Sensitive, Boost, Budget 2200)",
        "inputs": {
            "distance": "21k",
            "pace_target": "record",
            "weather": "moderate",
            "stomach_type": "sensitive",
            "caffeine_preference": "boost",
            "body_concerns": [],
            "gear_needed": ["belt"],
            "custom_budget": 2200.0
        },
        "deselect": {"slots": ["gear"]}
    },

    # =========================================================================
    # GROUP 3: 42K FULL MARATHON RUNNERS (Scenarios 29-42)
    # =========================================================================
    {
        "id": 29,
        "name": "42k Marathon Debutant (Moderate, Finish, Normal, None, Budget 2700)",
        "inputs": {
            "distance": "42k",
            "pace_target": "finish",
            "weather": "moderate",
            "stomach_type": "normal",
            "caffeine_preference": "none",
            "body_concerns": ["cramps"],
            "gear_needed": ["belt"],
            "custom_budget": 2700.0
        },
        "deselect": {"sub_types": ["running_belt"]}
    },
    {
        "id": 30,
        "name": "42k Sub-3:00 Boston Qualifier (Moderate, Record, Normal, Boost, Premium)",
        "inputs": {
            "distance": "42k",
            "pace_target": "record",
            "weather": "moderate",
            "stomach_type": "normal",
            "caffeine_preference": "boost",
            "body_concerns": ["chafing"],
            "gear_needed": ["belt", "socks"],
            "price_tier": "premium"
        },
        "deselect": {"sub_types": ["running_socks"]}
    },
    {
        "id": 31,
        "name": "42k Hot Marathon Wave (Hot, Steady, Normal, Boost, Cramps+Chafing, Standard)",
        "inputs": {
            "distance": "42k",
            "pace_target": "steady",
            "weather": "hot",
            "stomach_type": "normal",
            "caffeine_preference": "boost",
            "body_concerns": ["cramps", "chafing"],
            "gear_needed": ["flask", "socks"],
            "price_tier": "standard"
        },
        "deselect": {"sub_types": ["soft_flask"]}
    },
    {
        "id": 32,
        "name": "42k Cold Autumn Marathon (Cold, Steady, Sensitive, None, Chafing, Standard)",
        "inputs": {
            "distance": "42k",
            "pace_target": "steady",
            "weather": "cold",
            "stomach_type": "sensitive",
            "caffeine_preference": "none",
            "body_concerns": ["chafing"],
            "gear_needed": ["socks"],
            "price_tier": "standard"
        },
        "deselect": {"slots": ["care_recovery"]}
    },
    {
        "id": 33,
        "name": "42k Vegan Marathoner (Moderate, Steady, Vegan, Boost, Chafing, Standard)",
        "inputs": {
            "distance": "42k",
            "pace_target": "steady",
            "weather": "moderate",
            "stomach_type": "vegan",
            "caffeine_preference": "boost",
            "body_concerns": ["chafing"],
            "gear_needed": ["belt", "flask"],
            "price_tier": "standard"
        },
        "deselect": {"sub_types": ["anti_chafe"]}
    },
    {
        "id": 34,
        "name": "42k Vegan Zero Caffeine (Cold, Finish, Vegan, None, Cramps, Budget 2800)",
        "inputs": {
            "distance": "42k",
            "pace_target": "finish",
            "weather": "cold",
            "stomach_type": "vegan",
            "caffeine_preference": "none",
            "body_concerns": ["cramps"],
            "gear_needed": ["socks"],
            "custom_budget": 2800.0
        },
        "deselect": {"slots": ["gear"]}
    },
    {
        "id": 35,
        "name": "42k Multi-Issue Veteran (Moderate, Finish, Sensitive, None, Cramps+Chafing+Joints)",
        "inputs": {
            "distance": "42k",
            "pace_target": "finish",
            "weather": "moderate",
            "stomach_type": "sensitive",
            "caffeine_preference": "none",
            "body_concerns": ["cramps", "chafing", "joints"],
            "gear_needed": ["belt", "socks"],
            "price_tier": "standard"
        },
        "deselect": {"sub_types": ["joint_care"]}
    },
    {
        "id": 36,
        "name": "42k High Electrolyte Heavy Sweater (Hot, Record, Normal, Boost, Budget 3500)",
        "inputs": {
            "distance": "42k",
            "pace_target": "record",
            "weather": "hot",
            "stomach_type": "normal",
            "caffeine_preference": "boost",
            "body_concerns": ["cramps", "chafing"],
            "gear_needed": ["belt", "flask", "socks"],
            "custom_budget": 3500.0
        },
        "deselect": {"sub_types": ["soft_flask"]}
    },
    {
        "id": 37,
        "name": "42k Sub-2:45 Elite Marathoner (Cold, Record, Sensitive, Boost, Budget 4500)",
        "inputs": {
            "distance": "42k",
            "pace_target": "record",
            "weather": "cold",
            "stomach_type": "sensitive",
            "caffeine_preference": "boost",
            "body_concerns": ["chafing"],
            "gear_needed": ["belt", "socks"],
            "custom_budget": 4500.0
        },
        "deselect": {"sub_types": ["running_belt"]}
    },
    {
        "id": 38,
        "name": "42k Low Cost Marathoner (Moderate, Finish, Normal, None, Budget 2700)",
        "inputs": {
            "distance": "42k",
            "pace_target": "finish",
            "weather": "moderate",
            "stomach_type": "normal",
            "caffeine_preference": "none",
            "body_concerns": [],
            "gear_needed": ["belt"],
            "custom_budget": 2700.0
        },
        "deselect": {"slots": ["gear"]}
    },
    {
        "id": 39,
        "name": "42k Masters Marathoner Joints Focus (Moderate, Steady, Normal, None, Budget 2800)",
        "inputs": {
            "distance": "42k",
            "pace_target": "steady",
            "weather": "moderate",
            "stomach_type": "normal",
            "caffeine_preference": "none",
            "body_concerns": ["joints"],
            "gear_needed": ["socks"],
            "custom_budget": 2800.0
        },
        "deselect": {"sub_types": ["running_socks"]}
    },
    {
        "id": 40,
        "name": "42k Extreme Heat Summer Marathon (Hot, Finish, Normal, None, Cramps+Chafing)",
        "inputs": {
            "distance": "42k",
            "pace_target": "finish",
            "weather": "hot",
            "stomach_type": "normal",
            "caffeine_preference": "none",
            "body_concerns": ["cramps", "chafing"],
            "gear_needed": ["flask", "belt"],
            "price_tier": "standard"
        },
        "deselect": {"sub_types": ["anti_chafe"]}
    },
    {
        "id": 41,
        "name": "42k Ultra Energy 90g/hr High Carb (Moderate, Record, Normal, Boost, Budget 4000)",
        "inputs": {
            "distance": "42k",
            "pace_target": "record",
            "weather": "moderate",
            "stomach_type": "normal",
            "caffeine_preference": "boost",
            "body_concerns": ["chafing", "joints"],
            "gear_needed": ["belt", "socks"],
            "custom_budget": 4000.0
        },
        "deselect": {"slots": ["care_recovery"]}
    },
    {
        "id": 42,
        "name": "42k Sensitive GI Wall-Breaker (Cold, Steady, Sensitive, Boost, Budget 2800)",
        "inputs": {
            "distance": "42k",
            "pace_target": "steady",
            "weather": "cold",
            "stomach_type": "sensitive",
            "caffeine_preference": "boost",
            "body_concerns": ["cramps"],
            "gear_needed": ["flask"],
            "custom_budget": 2800.0
        },
        "deselect": {"sub_types": ["soft_flask"]}
    },

    # =========================================================================
    # GROUP 4: TRAIL & ULTRA RUNNERS (Scenarios 43-50)
    # =========================================================================
    {
        "id": 43,
        "name": "Trail 25k Mountain Sprint (Moderate, Record, Normal, Boost, Standard)",
        "inputs": {
            "distance": "trail",
            "pace_target": "record",
            "weather": "moderate",
            "stomach_type": "normal",
            "caffeine_preference": "boost",
            "body_concerns": ["chafing"],
            "gear_needed": ["flask", "socks"],
            "price_tier": "standard"
        },
        "deselect": {"sub_types": ["running_socks"]}
    },
    {
        "id": 44,
        "name": "Trail 35k Alpine Ascent (Cold, Steady, Sensitive, Boost, Budget 3200)",
        "inputs": {
            "distance": "trail",
            "pace_target": "steady",
            "weather": "cold",
            "stomach_type": "sensitive",
            "caffeine_preference": "boost",
            "body_concerns": ["joints", "cramps"],
            "gear_needed": ["belt", "flask"],
            "custom_budget": 3200.0
        },
        "deselect": {"sub_types": ["running_belt"]}
    },
    {
        "id": 45,
        "name": "Trail 50k Ultra Pro (Hot, Record, Normal, Boost, Cramps+Chafing+Joints, Budget 5000)",
        "inputs": {
            "distance": "trail",
            "pace_target": "record",
            "weather": "hot",
            "stomach_type": "normal",
            "caffeine_preference": "boost",
            "body_concerns": ["cramps", "chafing", "joints"],
            "gear_needed": ["belt", "flask", "socks"],
            "custom_budget": 5000.0
        },
        "deselect": {"sub_types": ["soft_flask"]}
    },
    {
        "id": 46,
        "name": "Trail Ultra Cold Weather (Cold, Finish, Normal, None, Cramps, Budget 2400)",
        "inputs": {
            "distance": "trail",
            "pace_target": "finish",
            "weather": "cold",
            "stomach_type": "normal",
            "caffeine_preference": "none",
            "body_concerns": ["cramps"],
            "gear_needed": ["flask"],
            "custom_budget": 2400.0
        },
        "deselect": {"slots": ["gear"]}
    },
    {
        "id": 47,
        "name": "Trail 60k Vegan Mountain Ultra (Moderate, Steady, Vegan, None, Budget 3500)",
        "inputs": {
            "distance": "trail",
            "pace_target": "steady",
            "weather": "moderate",
            "stomach_type": "vegan",
            "caffeine_preference": "none",
            "body_concerns": ["joints", "chafing"],
            "gear_needed": ["belt", "socks"],
            "custom_budget": 3500.0
        },
        "deselect": {"sub_types": ["joint_care"]}
    },
    {
        "id": 48,
        "name": "Trail Desert Heat Ultra (Hot, Steady, Normal, None, Cramps+Chafing, Budget 2800)",
        "inputs": {
            "distance": "trail",
            "pace_target": "steady",
            "weather": "hot",
            "stomach_type": "normal",
            "caffeine_preference": "none",
            "body_concerns": ["cramps", "chafing"],
            "gear_needed": ["flask", "socks"],
            "custom_budget": 2800.0
        },
        "deselect": {"slots": ["care_recovery"]}
    },
    {
        "id": 49,
        "name": "Trail 40k Sensitive Gut Mountain Finisher (Moderate, Finish, Sensitive, None)",
        "inputs": {
            "distance": "trail",
            "pace_target": "finish",
            "weather": "moderate",
            "stomach_type": "sensitive",
            "caffeine_preference": "none",
            "body_concerns": ["cramps"],
            "gear_needed": ["belt", "flask"],
            "price_tier": "standard"
        },
        "deselect": {"sub_types": ["running_belt"]}
    },
    {
        "id": 50,
        "name": "Trail 100k Carpathian Ultra Heavy Duty (Cold, Finish, Normal, Boost, Premium)",
        "inputs": {
            "distance": "trail",
            "pace_target": "finish",
            "weather": "cold",
            "stomach_type": "normal",
            "caffeine_preference": "boost",
            "body_concerns": ["cramps", "chafing", "joints"],
            "gear_needed": ["belt", "flask", "socks"],
            "price_tier": "premium"
        },
        "deselect": {"sub_types": ["anti_chafe"]}
    }
]


# Ensure exactly 50 scenarios are configured
assert len(SCENARIOS) == 50, f"Expected exactly 50 scenarios, found {len(SCENARIOS)}"


@pytest.mark.parametrize(
    "scenario",
    SCENARIOS,
    ids=[f"Scenario_{s['id']:02d}_{s['name'][:35].replace(' ', '_')}" for s in SCENARIOS]
)
def test_running_scenario(scenario, running_catalog):
    inputs = scenario["inputs"]
    box = generate_runner_box(inputs, running_catalog)

    # 1. Basic Structure
    assert isinstance(box, dict), "Box must be a dictionary"
    assert "slots" in box, "Box must contain 'slots'"
    assert "total_base_price" in box, "Box must contain 'total_base_price'"
    assert "budget_info" in box, "Box must contain 'budget_info'"
    slots = box["slots"]

    # 2. No Empty Slots: all 4 slots must contain items
    for slot_name in ["energy", "hydration", "gear", "care_recovery"]:
        assert slot_name in slots, f"Missing slot '{slot_name}' in box"
        assert len(slots[slot_name]) > 0, f"Slot '{slot_name}' is empty for {scenario['name']}"

    # Flatten all items in box
    all_items = []
    for slot_name in ["energy", "hydration", "gear", "care_recovery"]:
        for idx, item in enumerate(slots.get(slot_name, [])):
            all_items.append((slot_name, idx, item))

    # 3. Stock, Quantity & Price Sanity
    for slot_name, idx, item in all_items:
        prod = item["product"]
        assert prod.get("quantity", 0) > 0, f"Out of stock product recommended: {prod.get('name')}"
        assert prod.get("price", 0) > 0, f"Zero or negative price for product: {prod.get('name')}"
        assert item.get("quantity_recommended", 0) > 0, f"Invalid recommended quantity for {prod.get('name')}"

    assert box["total_base_price"] > 0, f"Total base price must be positive, got {box['total_base_price']}"

    # 4. Custom Budget Verification
    custom_budget = inputs.get("custom_budget")
    if custom_budget:
        assert box["total_base_price"] <= custom_budget, (
            f"Box total price {box['total_base_price']} exceeds custom budget {custom_budget} for {scenario['name']}"
        )
        assert box["budget_info"]["within_budget"] is True
        assert box["budget_info"]["custom_budget"] == custom_budget

    # 5. SINGLE GEL BRAND RULE: 100% of energy gels must be from the exact same brand
    energy_gels = [it for it in slots["energy"] if it["product"].get("sub_type") == "gel"]
    assert len(energy_gels) >= 1, f"Expected at least one gel in energy slot for {scenario['name']}"
    gel_brands = {it["product"].get("brand") for it in energy_gels}
    assert len(gel_brands) == 1, f"Gel brand mixing detected in {scenario['name']}: {gel_brands}"
    primary_brand = list(gel_brands)[0]
    assert primary_brand is not None and len(primary_brand) > 0

    # 6. ZERO CAFFEINE LEAKS
    if inputs.get("caffeine_preference") == "none":
        for slot_name, idx, item in all_items:
            assert item["product"].get("caffeine", False) is False, (
                f"Caffeine leak in zero-caffeine scenario '{scenario['name']}': "
                f"product '{item['product'].get('name')}' in slot '{slot_name}' has caffeine"
            )

    # 7. CAFFEINE BOOST INCLUSION & BRAND CONSISTENCY
    if inputs.get("caffeine_preference") == "boost":
        caff_gels = [it for it in energy_gels if it["product"].get("caffeine")]
        assert len(caff_gels) >= 1, (
            f"Requested caffeine boost but no caffeinated gel in energy slot for '{scenario['name']}'"
        )
        for cg in caff_gels:
            assert cg["product"].get("brand") == primary_brand, (
                f"Caffeine boost gel brand '{cg['product'].get('brand')}' does not match "
                f"base gel brand '{primary_brand}' in '{scenario['name']}'"
            )

    # 8. HOT WEATHER / CRAMPS SALT CAPSULES INCLUSION
    if inputs.get("weather") == "hot" or "cramps" in inputs.get("body_concerns", []):
        hydration_subtypes = [it["product"].get("sub_type") for it in slots["hydration"]]
        assert "salt_caps" in hydration_subtypes, (
            f"Hot weather/cramps scenario '{scenario['name']}' missing salt_caps in hydration slot"
        )

    # 9. SOCKS SIZING SELECTOR
    gear_socks = [it for it in slots["gear"] if it["product"].get("sub_type") == "running_socks"]
    for sock_item in gear_socks:
        assert "available_sizes" in sock_item, f"Running socks missing available_sizes in '{scenario['name']}'"
        assert len(sock_item["available_sizes"]) >= 2, (
            f"Running socks must have available size options in '{scenario['name']}'"
        )
        for size_opt in sock_item["available_sizes"]:
            assert "size" in size_opt and "product_id" in size_opt, f"Malformed size option {size_opt}"

    # 10. ITEM DESELECTION & CART PAYLOAD VERIFICATION
    # Checkbox simulation: calculate baseline price
    baseline_price = sum(it["product"]["price"] * it["quantity_recommended"] for _, _, it in all_items)
    assert round(baseline_price, 2) == round(box["total_base_price"], 2), (
        f"Sum of item prices ({baseline_price}) does not match total_base_price ({box['total_base_price']})"
    )

    deselect_rule = scenario.get("deselect", {})
    deselected_slots = set(deselect_rule.get("slots", []))
    deselected_subtypes = set(deselect_rule.get("sub_types", []))

    selected_items = []
    deselected_items = []

    for slot_name, idx, item in all_items:
        prod = item["product"]
        is_deselected = (slot_name in deselected_slots) or (prod.get("sub_type") in deselected_subtypes)
        if is_deselected:
            deselected_items.append(item)
        else:
            selected_items.append(item)

    # Verify that deselect target was found and unchecked
    assert len(deselected_items) > 0, f"Scenario '{scenario['name']}' specified deselection but no items matched"
    assert len(selected_items) > 0, f"Deselection removed all items in '{scenario['name']}'"

    # Simulate cart payload creation from checked items only
    cart_payload = []
    cart_total_price = 0.0
    for it in selected_items:
        item_qty = it["quantity_recommended"]
        item_price = it["product"]["price"]
        cart_payload.append({
            "productId": it["product"]["product_id"],
            "name": it["product"]["name"],
            "quantity": item_qty,
            "price": item_price,
            "slot": it["product"].get("slot")
        })
        cart_total_price += item_price * item_qty

    cart_total_price = round(cart_total_price, 2)

    # Assertions on Cart Payload
    assert len(cart_payload) == len(selected_items)
    assert cart_total_price < box["total_base_price"], "Deselected cart total should be strictly less than full box"

    # Ensure none of the deselected product IDs entered the cart
    deselected_ids = {it["product"]["product_id"] for it in deselected_items}
    for cart_entry in cart_payload:
        assert cart_entry["productId"] not in deselected_ids or any(
            it["product"]["product_id"] == cart_entry["productId"] for it in selected_items
        ), f"Deselected product {cart_entry['name']} found in cart payload"

    # Verify all selected items are accurately represented in cart
    for it in selected_items:
        matching = [c for c in cart_payload if c["productId"] == it["product"]["product_id"]]
        assert len(matching) >= 1, f"Selected product {it['product']['name']} missing from cart payload"
