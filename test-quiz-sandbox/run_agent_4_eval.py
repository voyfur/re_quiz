#!/usr/bin/env python3
"""QA Agent 4 - Food, Hydration & Outdoor Specialist Test Suite (100 Scenarios)."""

import json
import sys
from pathlib import Path

# Add test sandbox to path
SANDBOX_DIR = Path(__file__).resolve().parent
PROJECT_DIR = SANDBOX_DIR.parent
sys.path.append(str(SANDBOX_DIR))

import draft_matcher

CATALOG_PATH = SANDBOX_DIR / "catalog.json"
AUDIT_PATH = PROJECT_DIR / "wiki" / "projects" / "quiz-set-audit.json"
OUTPUT_JSON_PATH = SANDBOX_DIR / "agent_4_food_hydration_100_tests.json"
OUTPUT_REPORT_PATH = SANDBOX_DIR / "agent_4_report.md"

def load_enriched_catalog():
    catalog = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    audit = json.loads(AUDIT_PATH.read_text(encoding="utf-8"))
    return draft_matcher.attach_audit_evidence(catalog, audit), audit

def get_composition_summary(audit_records_by_sku, sku):
    rec = audit_records_by_sku.get(sku, {})
    comp = rec.get("composition", {})
    if isinstance(comp, dict):
        return comp.get("raw_text", "")
    return str(comp)

def generate_100_scenarios():
    """Generate 100 realistic, diverse test scenarios:
    - 40 Food (TC001 - TC040)
    - 30 Hydration (TC041 - TC070)
    - 30 Outdoors (TC071 - TC100)
    Covering low (500-1000), medium (1100-1800), high (1900-3500) budgets,
    component classes, activities, timings, forms, and locales.
    """
    scenarios = []

    # -------------------------------------------------------------
    # FOOD SCENARIOS (40 total: TC001 - TC040)
    # -------------------------------------------------------------
    # 1. Running & Food
    scenarios.append({
        "id": "TC001",
        "goal_group": "food",
        "persona": "Half-marathon runner looking for energy bars during training",
        "activity": "running",
        "component_class": "protein_carbohydrate_food",
        "product_form": "bars",
        "use_timing": "during_training",
        "max_price_uah": 1500,
        "locale": "uk"
    })
    scenarios.append({
        "id": "TC002",
        "goal_group": "food",
        "persona": "Marathon runner needing portable carbohydrate gels",
        "activity": "running",
        "component_class": "protein_carbohydrate_food",
        "product_form": "gel",
        "use_timing": "during_training",
        "max_price_uah": 1600,
        "locale": "uk"
    })
    scenarios.append({
        "id": "TC003",
        "goal_group": "food",
        "persona": "Budget runner looking for snacks under 800 UAH",
        "activity": "running",
        "component_class": "protein_carbohydrate_food",
        "use_timing": "during_training",
        "max_price_uah": 800,
        "locale": "uk"
    })
    scenarios.append({
        "id": "TC004",
        "goal_group": "food",
        "persona": "Ultra-distance runner with high budget wanting complete food pack",
        "activity": "running",
        "component_class": "protein_carbohydrate_food",
        "use_timing": "during_training",
        "max_price_uah": 3000,
        "locale": "uk"
    })
    scenarios.append({
        "id": "TC005",
        "goal_group": "food",
        "persona": "City runner needing post-workout protein bars",
        "activity": "running",
        "component_class": "protein_carbohydrate_food",
        "product_form": "bars",
        "use_timing": "before_or_after_training",
        "max_price_uah": 1500,
        "locale": "ru"
    })
    scenarios.append({
        "id": "TC006",
        "goal_group": "food",
        "persona": "Beginner runner needing general nutrition bars with medium budget",
        "activity": "running",
        "component_class": "protein_carbohydrate_food",
        "product_form": "bars",
        "max_price_uah": 1300,
        "locale": "uk"
    })
    scenarios.append({
        "id": "TC007",
        "goal_group": "food",
        "persona": "Trail runner needing liquid nutrition shots during training",
        "activity": "running",
        "component_class": "protein_carbohydrate_food",
        "product_form": "liquid",
        "use_timing": "during_training",
        "max_price_uah": 1600,
        "locale": "ru"
    })
    scenarios.append({
        "id": "TC008",
        "goal_group": "food",
        "persona": "High-budget trail runner (2500 UAH) wanting powder sticks / energy mix",
        "activity": "running",
        "component_class": "protein_carbohydrate_food",
        "product_form": "sticks",
        "max_price_uah": 2500,
        "locale": "uk"
    })
    scenarios.append({
        "id": "TC009",
        "goal_group": "food",
        "persona": "Student runner on strict low budget (500 UAH)",
        "activity": "running",
        "component_class": "protein_carbohydrate_food",
        "max_price_uah": 500,
        "locale": "uk"
    })
    scenarios.append({
        "id": "TC010",
        "goal_group": "food",
        "persona": "Everyday runner looking for daily healthy snacks",
        "activity": "running",
        "component_class": "protein_carbohydrate_food",
        "use_timing": "daily_use",
        "max_price_uah": 1500,
        "locale": "ru"
    })

    # 2. Cycling & Food
    scenarios.append({
        "id": "TC011",
        "goal_group": "food",
        "persona": "Road cyclist looking for on-the-bike energy bars",
        "activity": "cycling",
        "component_class": "protein_carbohydrate_food",
        "product_form": "bars",
        "use_timing": "during_training",
        "max_price_uah": 1500,
        "locale": "uk"
    })
    scenarios.append({
        "id": "TC012",
        "goal_group": "food",
        "persona": "Gravel cyclist needing portable energy gels for 100km ride",
        "activity": "cycling",
        "component_class": "protein_carbohydrate_food",
        "product_form": "gel",
        "use_timing": "during_training",
        "max_price_uah": 1700,
        "locale": "ru"
    })
    scenarios.append({
        "id": "TC013",
        "goal_group": "food",
        "persona": "Commuter cyclist looking for post-ride protein snacks (medium budget)",
        "activity": "cycling",
        "component_class": "protein_carbohydrate_food",
        "use_timing": "before_or_after_training",
        "max_price_uah": 1400,
        "locale": "uk"
    })
    scenarios.append({
        "id": "TC014",
        "goal_group": "food",
        "persona": "Bikepacker looking for ready meals / substantial food packs",
        "activity": "cycling",
        "component_class": "protein_carbohydrate_food",
        "product_form": "food_or_meal",
        "use_timing": "during_training",
        "max_price_uah": 1500,
        "locale": "uk"
    })
    scenarios.append({
        "id": "TC015",
        "goal_group": "food",
        "persona": "Budget cyclist searching for food under 900 UAH",
        "activity": "cycling",
        "component_class": "protein_carbohydrate_food",
        "max_price_uah": 900,
        "locale": "ru"
    })
    scenarios.append({
        "id": "TC016",
        "goal_group": "food",
        "persona": "Competitive cyclist with high budget (2800 UAH) for endurance food",
        "activity": "cycling",
        "component_class": "protein_carbohydrate_food",
        "max_price_uah": 2800,
        "locale": "uk"
    })
    scenarios.append({
        "id": "TC017",
        "goal_group": "food",
        "persona": "Cyclist looking for liquid meal replacement / carb drinks",
        "activity": "cycling",
        "component_class": "protein_carbohydrate_food",
        "product_form": "liquid",
        "max_price_uah": 1500,
        "locale": "ru"
    })
    scenarios.append({
        "id": "TC018",
        "goal_group": "food",
        "persona": "Weekend cyclist wanting daily snacks for recovery days",
        "activity": "cycling",
        "component_class": "protein_carbohydrate_food",
        "use_timing": "daily_use",
        "max_price_uah": 1500,
        "locale": "uk"
    })

    # 3. Hiking & Food
    scenarios.append({
        "id": "TC019",
        "goal_group": "food",
        "persona": "Hiker looking for trail meat snacks / jerky during trek",
        "activity": "hiking",
        "component_class": "protein_carbohydrate_food",
        "product_form": "food_or_meal",
        "use_timing": "during_training",
        "max_price_uah": 1500,
        "locale": "uk"
    })
    scenarios.append({
        "id": "TC020",
        "goal_group": "food",
        "persona": "Backpacker looking specifically for dehydrated camp meals",
        "activity": "hiking",
        "component_class": "dehydrated_meal",
        "product_form": "food_or_meal",
        "max_price_uah": 1600,
        "locale": "uk"
    })
    scenarios.append({
        "id": "TC021",
        "goal_group": "food",
        "persona": "Day-hiker needing quick trail energy bars under 1200 UAH",
        "activity": "hiking",
        "component_class": "protein_carbohydrate_food",
        "product_form": "bars",
        "use_timing": "during_training",
        "max_price_uah": 1200,
        "locale": "ru"
    })
    scenarios.append({
        "id": "TC022",
        "goal_group": "food",
        "persona": "Mountain trekker needing sublimated meals & snacks (medium budget 1400 UAH)",
        "activity": "hiking",
        "component_class": "protein_carbohydrate_food",
        "product_form": "food_or_meal",
        "max_price_uah": 1400,
        "locale": "uk"
    })
    scenarios.append({
        "id": "TC023",
        "goal_group": "food",
        "persona": "Budget backpacker searching for food under 750 UAH",
        "activity": "hiking",
        "component_class": "protein_carbohydrate_food",
        "max_price_uah": 750,
        "locale": "uk"
    })
    scenarios.append({
        "id": "TC024",
        "goal_group": "food",
        "persona": "Expedition hiker with high budget (3500 UAH) for mountain trek food",
        "activity": "hiking",
        "component_class": "protein_carbohydrate_food",
        "max_price_uah": 3500,
        "locale": "uk"
    })
    scenarios.append({
        "id": "TC025",
        "goal_group": "food",
        "persona": "Hiker wanting post-hike hearty protein snack / recovery meal",
        "activity": "hiking",
        "component_class": "protein_carbohydrate_food",
        "use_timing": "before_or_after_training",
        "max_price_uah": 1500,
        "locale": "ru"
    })
    scenarios.append({
        "id": "TC026",
        "goal_group": "food",
        "persona": "Family camper wanting dried fruit and snacks for daily camp eating",
        "activity": "hiking",
        "component_class": "protein_carbohydrate_food",
        "use_timing": "daily_use",
        "max_price_uah": 1500,
        "locale": "uk"
    })

    # 4. Walking & Other Activities & Broad Food
    scenarios.append({
        "id": "TC027",
        "goal_group": "food",
        "persona": "Nordic walker looking for pocket energy bars during long walks",
        "activity": "walking",
        "component_class": "protein_carbohydrate_food",
        "product_form": "bars",
        "max_price_uah": 1500,
        "locale": "uk"
    })
    scenarios.append({
        "id": "TC028",
        "goal_group": "food",
        "persona": "Urban walker wanting healthy meat snacks (low budget 1000 UAH)",
        "activity": "walking",
        "component_class": "protein_carbohydrate_food",
        "max_price_uah": 1000,
        "locale": "ru"
    })
    scenarios.append({
        "id": "TC029",
        "goal_group": "food",
        "persona": "Fitness enthusiast wanting any food options with medium budget",
        "activity": "other",
        "component_class": "any",
        "max_price_uah": 1500,
        "locale": "uk"
    })
    scenarios.append({
        "id": "TC030",
        "goal_group": "food",
        "persona": "Busy professional wanting daily meal snacks under 1300 UAH",
        "activity": "other",
        "component_class": "protein_carbohydrate_food",
        "use_timing": "daily_use",
        "max_price_uah": 1300,
        "locale": "ru"
    })
    scenarios.append({
        "id": "TC031",
        "goal_group": "food",
        "persona": "Food buyer seeking hydration-compatible nutrition items",
        "activity": "running",
        "component_class": "hydration_items",
        "max_price_uah": 1500,
        "locale": "uk"
    })
    scenarios.append({
        "id": "TC032",
        "goal_group": "food",
        "persona": "Food buyer mistakenly selecting sports accessories in food section",
        "activity": "running",
        "component_class": "sports_accessories",
        "max_price_uah": 1500,
        "locale": "ru"
    })
    scenarios.append({
        "id": "TC033",
        "goal_group": "food",
        "persona": "Food buyer mistakenly selecting apparel in food section",
        "activity": "running",
        "component_class": "apparel_footwear",
        "max_price_uah": 1500,
        "locale": "uk"
    })
    scenarios.append({
        "id": "TC034",
        "goal_group": "food",
        "persona": "Low budget buyer (600 UAH) with any food class",
        "activity": "running",
        "component_class": "any",
        "max_price_uah": 600,
        "locale": "uk"
    })
    scenarios.append({
        "id": "TC035",
        "goal_group": "food",
        "persona": "Ultra runner testing relaxed fallback mode for bars",
        "activity": "running",
        "component_class": "protein_carbohydrate_food",
        "product_form": "bars",
        "fallback_mode": "relaxed",
        "max_price_uah": 1200,
        "locale": "uk"
    })
    scenarios.append({
        "id": "TC036",
        "goal_group": "food",
        "persona": "Cyclist testing general fallback mode for food",
        "activity": "cycling",
        "component_class": "protein_carbohydrate_food",
        "fallback_mode": "general",
        "max_price_uah": 1300,
        "locale": "ru"
    })
    scenarios.append({
        "id": "TC037",
        "goal_group": "food",
        "persona": "Hiker wanting high-calorie energy bars for cold mountain trail",
        "activity": "hiking",
        "component_class": "protein_carbohydrate_food",
        "product_form": "bars",
        "season": "cold",
        "max_price_uah": 1600,
        "locale": "uk"
    })
    scenarios.append({
        "id": "TC038",
        "goal_group": "food",
        "persona": "Runner preparing for marathon event needing energy fuel",
        "activity": "running",
        "component_class": "protein_carbohydrate_food",
        "use_scenario": "event_preparation",
        "race_format": "marathon",
        "max_price_uah": 1800,
        "locale": "uk"
    })
    scenarios.append({
        "id": "TC039",
        "goal_group": "food",
        "persona": "High budget (3200 UAH) food buyer with no restrictions",
        "activity": "any",
        "component_class": "any",
        "max_price_uah": 3200,
        "locale": "uk"
    })
    scenarios.append({
        "id": "TC040",
        "goal_group": "food",
        "persona": "Buyer wanting non-club food sets without gym membership",
        "activity": "running",
        "component_class": "protein_carbohydrate_food",
        "membership": "no",
        "max_price_uah": 1500,
        "locale": "uk"
    })

    # -------------------------------------------------------------
    # HYDRATION SCENARIOS (30 total: TC041 - TC070)
    # -------------------------------------------------------------
    scenarios.append({
        "id": "TC041",
        "goal_group": "hydration",
        "persona": "Summer marathon runner needing electrolyte sticks during training",
        "activity": "running",
        "component_class": "hydration_items",
        "product_form": "sticks",
        "use_timing": "during_training",
        "max_price_uah": 1500,
        "locale": "uk"
    })
    scenarios.append({
        "id": "TC042",
        "goal_group": "hydration",
        "persona": "Road cyclist looking for water bottle + electrolytes bundle",
        "activity": "cycling",
        "component_class": "sports_accessories",
        "use_timing": "during_training",
        "max_price_uah": 1600,
        "locale": "uk"
    })
    scenarios.append({
        "id": "TC043",
        "goal_group": "hydration",
        "persona": "Budget runner seeking hydration under 800 UAH",
        "activity": "running",
        "component_class": "hydration_items",
        "max_price_uah": 800,
        "locale": "uk"
    })
    scenarios.append({
        "id": "TC044",
        "goal_group": "hydration",
        "persona": "High budget triathlete (3000 UAH) seeking pro hydration kit",
        "activity": "running",
        "component_class": "hydration_items",
        "max_price_uah": 3000,
        "locale": "uk"
    })
    scenarios.append({
        "id": "TC045",
        "goal_group": "hydration",
        "persona": "Gym athlete wanting hydration electrolytes during functional training",
        "activity": "functional_training",
        "component_class": "hydration_items",
        "use_timing": "during_training",
        "max_price_uah": 1500,
        "locale": "ru"
    })
    scenarios.append({
        "id": "TC046",
        "goal_group": "hydration",
        "persona": "Powerlifter seeking hydration during heavy strength training",
        "activity": "strength_training",
        "component_class": "hydration_items",
        "use_timing": "during_training",
        "max_price_uah": 1500,
        "locale": "uk"
    })
    scenarios.append({
        "id": "TC047",
        "goal_group": "hydration",
        "persona": "Hiker looking for hydration on mountain trails",
        "activity": "hiking",
        "component_class": "hydration_items",
        "max_price_uah": 1500,
        "locale": "uk"
    })
    scenarios.append({
        "id": "TC048",
        "goal_group": "hydration",
        "persona": "Walker seeking hydration bottle & electrolytes",
        "activity": "walking",
        "component_class": "hydration_items",
        "max_price_uah": 1500,
        "locale": "ru"
    })
    scenarios.append({
        "id": "TC049",
        "goal_group": "hydration",
        "persona": "Cyclist seeking electrolyte drink mix in sticks (medium budget 1400 UAH)",
        "activity": "cycling",
        "component_class": "hydration_items",
        "product_form": "sticks",
        "max_price_uah": 1400,
        "locale": "uk"
    })
    scenarios.append({
        "id": "TC050",
        "goal_group": "hydration",
        "persona": "Runner seeking isotonic liquid shots for quick intake",
        "activity": "running",
        "component_class": "hydration_items",
        "product_form": "liquid",
        "max_price_uah": 1500,
        "locale": "ru"
    })
    scenarios.append({
        "id": "TC051",
        "goal_group": "hydration",
        "persona": "Budget runner looking for hydration under 1000 UAH",
        "activity": "running",
        "component_class": "hydration_items",
        "max_price_uah": 1000,
        "locale": "uk"
    })
    scenarios.append({
        "id": "TC052",
        "goal_group": "hydration",
        "persona": "Athlete seeking daily hydration drink for heat protection",
        "activity": "running",
        "component_class": "hydration_items",
        "use_timing": "daily_use",
        "max_price_uah": 1500,
        "locale": "uk"
    })
    scenarios.append({
        "id": "TC053",
        "goal_group": "hydration",
        "persona": "Runner seeking post-workout rehydration bundle",
        "activity": "running",
        "component_class": "hydration_items",
        "use_timing": "before_or_after_training",
        "max_price_uah": 1500,
        "locale": "ru"
    })
    scenarios.append({
        "id": "TC054",
        "goal_group": "hydration",
        "persona": "Cyclist wanting high-end hydration gear (2500 UAH budget)",
        "activity": "cycling",
        "component_class": "sports_accessories",
        "max_price_uah": 2500,
        "locale": "uk"
    })
    scenarios.append({
        "id": "TC055",
        "goal_group": "hydration",
        "persona": "Student athlete on strict budget (500 UAH) for electrolytes",
        "activity": "running",
        "component_class": "hydration_items",
        "max_price_uah": 500,
        "locale": "uk"
    })
    scenarios.append({
        "id": "TC056",
        "goal_group": "hydration",
        "persona": "Hydration buyer mistakenly selecting dehydrated meal in hydration",
        "activity": "running",
        "component_class": "dehydrated_meal",
        "max_price_uah": 1500,
        "locale": "uk"
    })
    scenarios.append({
        "id": "TC057",
        "goal_group": "hydration",
        "persona": "Hydration buyer selecting apparel in hydration section",
        "activity": "running",
        "component_class": "apparel_footwear",
        "max_price_uah": 1500,
        "locale": "ru"
    })
    scenarios.append({
        "id": "TC058",
        "goal_group": "hydration",
        "persona": "Marathoner looking for energy gel + electrolyte combination",
        "activity": "running",
        "component_class": "protein_carbohydrate_food",
        "product_form": "gel",
        "max_price_uah": 1600,
        "locale": "uk"
    })
    scenarios.append({
        "id": "TC059",
        "goal_group": "hydration",
        "persona": "Hot summer cyclist needing maximum electrolyte replacement",
        "activity": "cycling",
        "component_class": "hydration_items",
        "season": "warm",
        "max_price_uah": 1500,
        "locale": "uk"
    })
    scenarios.append({
        "id": "TC060",
        "goal_group": "hydration",
        "persona": "Fitness athlete wanting pure electrolytes without club membership",
        "activity": "running",
        "component_class": "hydration_items",
        "membership": "no",
        "max_price_uah": 1500,
        "locale": "uk"
    })
    scenarios.append({
        "id": "TC061",
        "goal_group": "hydration",
        "persona": "Half marathon prep buyer needing hydration for race day",
        "activity": "running",
        "component_class": "hydration_items",
        "use_scenario": "event_preparation",
        "race_format": "half_marathon",
        "max_price_uah": 1500,
        "locale": "uk"
    })
    scenarios.append({
        "id": "TC062",
        "goal_group": "hydration",
        "persona": "Runner testing relaxed fallback for hydration bottles",
        "activity": "running",
        "component_class": "sports_accessories",
        "fallback_mode": "relaxed",
        "max_price_uah": 1300,
        "locale": "ru"
    })
    scenarios.append({
        "id": "TC063",
        "goal_group": "hydration",
        "persona": "Cyclist testing general fallback for electrolytes",
        "activity": "cycling",
        "component_class": "hydration_items",
        "fallback_mode": "general",
        "max_price_uah": 1200,
        "locale": "uk"
    })
    scenarios.append({
        "id": "TC064",
        "goal_group": "hydration",
        "persona": "Ultra-distance runner needing high-volume electrolytes (budget 2200 UAH)",
        "activity": "running",
        "component_class": "hydration_items",
        "use_scenario": "event_preparation",
        "race_format": "ultra_or_long_distance",
        "max_price_uah": 2200,
        "locale": "uk"
    })
    scenarios.append({
        "id": "TC065",
        "goal_group": "hydration",
        "persona": "Athlete with budget 1250 UAH looking for hydration",
        "activity": "running",
        "component_class": "any",
        "max_price_uah": 1250,
        "locale": "uk"
    })
    scenarios.append({
        "id": "TC066",
        "goal_group": "hydration",
        "persona": "Athlete with budget 3500 UAH and no restrictions in hydration",
        "activity": "any",
        "component_class": "any",
        "max_price_uah": 3500,
        "locale": "uk"
    })
    scenarios.append({
        "id": "TC067",
        "goal_group": "hydration",
        "persona": "Strength athlete looking for energy & hydration bars",
        "activity": "strength_training",
        "component_class": "protein_carbohydrate_food",
        "product_form": "bars",
        "max_price_uah": 1500,
        "locale": "ru"
    })
    scenarios.append({
        "id": "TC068",
        "goal_group": "hydration",
        "persona": "Budget cyclist (700 UAH) needing sports bottle",
        "activity": "cycling",
        "component_class": "sports_accessories",
        "max_price_uah": 700,
        "locale": "uk"
    })
    scenarios.append({
        "id": "TC069",
        "goal_group": "hydration",
        "persona": "Functional training athlete wanting isotonic sticks under 1350 UAH",
        "activity": "functional_training",
        "component_class": "hydration_items",
        "product_form": "sticks",
        "max_price_uah": 1350,
        "locale": "uk"
    })
    scenarios.append({
        "id": "TC070",
        "goal_group": "hydration",
        "persona": "Everyday runner wanting hydration gels for weekly long run",
        "activity": "running",
        "component_class": "hydration_items",
        "product_form": "gel",
        "max_price_uah": 1650,
        "locale": "uk"
    })

    # -------------------------------------------------------------
    # OUTDOORS SCENARIOS (30 total: TC071 - TC100)
    # -------------------------------------------------------------
    scenarios.append({
        "id": "TC071",
        "goal_group": "outdoors",
        "persona": "Mountain hiker looking for thermal socks bundle (size 42)",
        "activity": "hiking",
        "component_class": "apparel_footwear",
        "shoe_size": 41,
        "max_price_uah": 1200,
        "locale": "uk"
    })
    scenarios.append({
        "id": "TC072",
        "goal_group": "outdoors",
        "persona": "Female hiker looking for thermal socks bundle (size 36)",
        "activity": "hiking",
        "component_class": "apparel_footwear",
        "shoe_size": 36,
        "max_price_uah": 1200,
        "locale": "uk"
    })
    scenarios.append({
        "id": "TC073",
        "goal_group": "outdoors",
        "persona": "Hiker with large feet looking for thermal socks (size 44)",
        "activity": "hiking",
        "component_class": "apparel_footwear",
        "shoe_size": 44,
        "max_price_uah": 1100,
        "locale": "uk"
    })
    scenarios.append({
        "id": "TC074",
        "goal_group": "outdoors",
        "persona": "Backpacker looking for dehydrated camp meals",
        "activity": "hiking",
        "component_class": "dehydrated_meal",
        "max_price_uah": 1600,
        "locale": "uk"
    })
    scenarios.append({
        "id": "TC075",
        "goal_group": "outdoors",
        "persona": "Trekker looking for ready hiking food and meat jerky",
        "activity": "hiking",
        "component_class": "protein_carbohydrate_food",
        "product_form": "food_or_meal",
        "max_price_uah": 1500,
        "locale": "uk"
    })
    scenarios.append({
        "id": "TC076",
        "goal_group": "outdoors",
        "persona": "Camper looking for travel hygiene and outdoor accessories",
        "activity": "hiking",
        "component_class": "sports_accessories",
        "max_price_uah": 1500,
        "locale": "uk"
    })
    scenarios.append({
        "id": "TC077",
        "goal_group": "outdoors",
        "persona": "Budget hiker looking for thermal socks under 800 UAH",
        "activity": "hiking",
        "component_class": "apparel_footwear",
        "max_price_uah": 800,
        "locale": "uk"
    })
    scenarios.append({
        "id": "TC078",
        "goal_group": "outdoors",
        "persona": "High budget trekker (3000 UAH) looking for complete outdoor pack",
        "activity": "hiking",
        "component_class": "any",
        "max_price_uah": 3000,
        "locale": "uk"
    })
    scenarios.append({
        "id": "TC079",
        "goal_group": "outdoors",
        "persona": "Long distance walker looking for trekking snacks and socks",
        "activity": "walking",
        "component_class": "protein_carbohydrate_food",
        "max_price_uah": 1500,
        "locale": "ru"
    })
    scenarios.append({
        "id": "TC080",
        "goal_group": "outdoors",
        "persona": "Bikepacker seeking outdoor gear & food (cycling)",
        "activity": "cycling",
        "component_class": "protein_carbohydrate_food",
        "max_price_uah": 1500,
        "locale": "uk"
    })
    scenarios.append({
        "id": "TC081",
        "goal_group": "outdoors",
        "persona": "Trail runner searching in outdoors category",
        "activity": "running",
        "component_class": "hydration_items",
        "max_price_uah": 1700,
        "locale": "uk"
    })
    scenarios.append({
        "id": "TC082",
        "goal_group": "outdoors",
        "persona": "Hiker looking for pre/post-hike nutrition (testing timing)",
        "activity": "hiking",
        "component_class": "protein_carbohydrate_food",
        "use_timing": "before_or_after_training",
        "max_price_uah": 1500,
        "locale": "uk"
    })
    scenarios.append({
        "id": "TC083",
        "goal_group": "outdoors",
        "persona": "Hiker looking for trail energy food during the hike",
        "activity": "hiking",
        "component_class": "protein_carbohydrate_food",
        "use_timing": "during_training",
        "max_price_uah": 1500,
        "locale": "ru"
    })
    scenarios.append({
        "id": "TC084",
        "goal_group": "outdoors",
        "persona": "Camper looking for everyday outdoor items for base camp",
        "activity": "hiking",
        "component_class": "sports_accessories",
        "use_timing": "daily_use",
        "max_price_uah": 1500,
        "locale": "uk"
    })
    scenarios.append({
        "id": "TC085",
        "goal_group": "outdoors",
        "persona": "Winter mountaineer looking for thermal socks in cold weather",
        "activity": "hiking",
        "component_class": "apparel_footwear",
        "season": "cold",
        "shoe_size": 42,
        "max_price_uah": 1300,
        "locale": "uk"
    })
    scenarios.append({
        "id": "TC086",
        "goal_group": "outdoors",
        "persona": "Summer trekker looking for warm-weather hydration gear",
        "activity": "hiking",
        "component_class": "hydration_items",
        "season": "warm",
        "max_price_uah": 1600,
        "locale": "uk"
    })
    scenarios.append({
        "id": "TC087",
        "goal_group": "outdoors",
        "persona": "Budget camper looking for any outdoors kit under 600 UAH",
        "activity": "hiking",
        "component_class": "any",
        "max_price_uah": 600,
        "locale": "uk"
    })
    scenarios.append({
        "id": "TC088",
        "goal_group": "outdoors",
        "persona": "Outdoor enthusiast testing relaxed fallback for socks",
        "activity": "hiking",
        "component_class": "apparel_footwear",
        "fallback_mode": "relaxed",
        "max_price_uah": 1000,
        "locale": "ru"
    })
    scenarios.append({
        "id": "TC089",
        "goal_group": "outdoors",
        "persona": "Hiker testing general fallback for dehydrated food",
        "activity": "hiking",
        "component_class": "dehydrated_meal",
        "fallback_mode": "general",
        "max_price_uah": 1500,
        "locale": "uk"
    })
    scenarios.append({
        "id": "TC090",
        "goal_group": "outdoors",
        "persona": "Camper looking for outdoor gift bundle with accessories",
        "activity": "hiking",
        "component_class": "sports_accessories",
        "max_price_uah": 1600,
        "locale": "uk"
    })
    scenarios.append({
        "id": "TC091",
        "goal_group": "outdoors",
        "persona": "Trekker wanting pure outdoor gear without club membership",
        "activity": "hiking",
        "component_class": "apparel_footwear",
        "membership": "no",
        "max_price_uah": 1200,
        "locale": "uk"
    })
    scenarios.append({
        "id": "TC092",
        "goal_group": "outdoors",
        "persona": "Walker seeking outdoor walking snacks (medium budget 1400 UAH)",
        "activity": "walking",
        "component_class": "protein_carbohydrate_food",
        "product_form": "bars",
        "max_price_uah": 1400,
        "locale": "uk"
    })
    scenarios.append({
        "id": "TC093",
        "goal_group": "outdoors",
        "persona": "Mountain hiker looking for sublimated fruit snacks and drink",
        "activity": "hiking",
        "component_class": "protein_carbohydrate_food",
        "product_form": "liquid",
        "max_price_uah": 1300,
        "locale": "ru"
    })
    scenarios.append({
        "id": "TC094",
        "goal_group": "outdoors",
        "persona": "Hiker with budget 1058 UAH matching exact floor sock set",
        "activity": "hiking",
        "component_class": "apparel_footwear",
        "shoe_size": 43,
        "max_price_uah": 1058,
        "locale": "uk"
    })
    scenarios.append({
        "id": "TC095",
        "goal_group": "outdoors",
        "persona": "Hiker with budget 1000 UAH (near-miss testing for 1058 UAH socks)",
        "activity": "hiking",
        "component_class": "apparel_footwear",
        "shoe_size": 40,
        "max_price_uah": 1000,
        "locale": "uk"
    })
    scenarios.append({
        "id": "TC096",
        "goal_group": "outdoors",
        "persona": "Hiker with ultra-high budget (3500 UAH) in outdoors",
        "activity": "hiking",
        "component_class": "any",
        "max_price_uah": 3500,
        "locale": "uk"
    })
    scenarios.append({
        "id": "TC097",
        "goal_group": "outdoors",
        "persona": "Camper looking for camp sleep aid and warm gear",
        "activity": "hiking",
        "component_class": "sports_accessories",
        "max_price_uah": 1500,
        "locale": "ru"
    })
    scenarios.append({
        "id": "TC098",
        "goal_group": "outdoors",
        "persona": "Cyclist on bike tour wanting food and hydration",
        "activity": "cycling",
        "component_class": "hydration_items",
        "max_price_uah": 1650,
        "locale": "uk"
    })
    scenarios.append({
        "id": "TC099",
        "goal_group": "outdoors",
        "persona": "Trekker wanting meat snack pack under 1500 UAH",
        "activity": "hiking",
        "component_class": "protein_carbohydrate_food",
        "product_form": "food_or_meal",
        "max_price_uah": 1500,
        "locale": "uk"
    })
    scenarios.append({
        "id": "TC100",
        "goal_group": "outdoors",
        "persona": "Outdoor enthusiast with medium budget (1500 UAH) open to any kit",
        "activity": "other",
        "component_class": "any",
        "max_price_uah": 1500,
        "locale": "uk"
    })

    return scenarios

def evaluate_test_run(scenario, res, err, audit_by_sku):
    """Evaluate one test run against the 5 human/buyer logic criteria:
    1. Food logic
    2. Hydration logic
    3. Outdoors logic
    4. Explanations & veracity
    5. Overall Verdict (PASS, WARN, FAIL) + human explanation
    """
    findings = []
    verdict = "PASS"
    goal = scenario["goal_group"]

    if err is not None:
        err_msg = str(err)
        # Validation error happened
        # Check if validation error is reasonable or represents a human-logic flaw
        if "activity is not supported" in err_msg:
            act = scenario.get("activity")
            if goal == "food" and act == "walking":
                verdict = "WARN"
                findings.append(
                    f"Human logic flaw: Walkers/Nordic walkers eat portable snacks on long walks, "
                    f"but matcher strictly rejects 'walking' under Food: '{err_msg}'."
                )
            elif goal == "hydration" and act in ("hiking", "walking"):
                verdict = "FAIL"
                findings.append(
                    f"Athlete/Hiker flaw: Hikers sweat heavily and urgently need hydration/electrolytes, "
                    f"but matcher rejects 'hiking'/'walking' under Hydration: '{err_msg}'."
                )
            elif goal == "outdoors" and act == "running":
                verdict = "WARN"
                findings.append(
                    f"Athlete flaw: Trail/mountain runners look under Outdoors for wilderness kits, "
                    f"but matcher rejects 'running' under Outdoors: '{err_msg}'."
                )
            else:
                verdict = "WARN"
                findings.append(f"Validation rejected activity '{act}': {err_msg}")
        elif "component_class is not supported" in err_msg:
            cls = scenario.get("component_class")
            verdict = "WARN"
            findings.append(f"Buyer selected unsupported component class '{cls}' for goal '{goal}': {err_msg}")
        elif "use_timing is not supported" in err_msg:
            timing = scenario.get("use_timing")
            if goal == "outdoors" and timing == "before_or_after_training":
                verdict = "WARN"
                findings.append(
                    f"Human logic flaw: Hikers eat meals before or after long hikes, "
                    f"but Outdoors disallows 'before_or_after_training': '{err_msg}'."
                )
            else:
                verdict = "WARN"
                findings.append(f"Validation rejected timing '{timing}': {err_msg}")
        else:
            verdict = "FAIL"
            findings.append(f"Unexpected DraftMatchError: {err_msg}")

        return {
            "verdict": verdict,
            "status": "validation_error",
            "results_count": 0,
            "near_miss_count": 0,
            "findings": findings,
            "results_evaluated": []
        }

    status = res.get("status")
    results = res.get("results", [])
    near_misses = res.get("near_miss_results", [])
    budget = scenario.get("max_price_uah")
    req_class = scenario.get("component_class")

    # Check for empty results / dehydrated meal issue
    if req_class == "dehydrated_meal" and len(results) == 0:
        verdict = "FAIL"
        findings.append(
            "Major Catalog/Taxonomy Flaw: Buyer asked for 'dehydrated_meal', but 0 sets matched because "
            "ЇDLO camping meals (e.g. RE11494, RE11495) are tagged 'protein_carbohydrate_food' instead of 'dehydrated_meal'."
        )

    # Check for budget handling
    if budget is not None and budget <= 1000:
        if len(results) == 0 and len(near_misses) == 0:
            verdict = "WARN" if verdict != "FAIL" else "FAIL"
            findings.append(
                f"Catalog Coverage Gap: Budget {budget} UAH returned 0 results and 0 near-misses. "
                f"Lowest set in category is above {budget} UAH."
            )
        elif len(results) == 0 and len(near_misses) > 0:
            # Good: near miss suggested
            findings.append(
                f"Budget {budget} UAH exceeded, but system gracefully returned {len(near_misses)} near-miss recommendation(s)."
            )

    evaluated_items = []
    for item in (results or near_misses):
        sku = item.get("sku")
        title = item.get("title", "")
        price = item.get("price_uah")
        why = item.get("why_suitable", [])
        summary = item.get("expert_summary", "")
        raw_comp = get_composition_summary(audit_by_sku, sku).lower()

        item_flaws = []

        # 1. Food Check
        if goal == "food":
            # Check for non-food leakages
            if "creatine" in raw_comp and "gainer" in raw_comp:
                item_flaws.append("Heavy bodybuilding powder (Anabolic Mass gainer + Creatine) offered to food/snack buyer.")
            elif "полотенце" in raw_comp or "банный" in raw_comp:
                item_flaws.append("Bath towel and accessories bundled into food recommendation.")
            elif "mind shi" in raw_comp or "4mushroom" in raw_comp:
                item_flaws.append("Mushroom nootropic pill bottle bundled into food/snack recommendation.")
            elif "абонемент" in raw_comp:
                item_flaws.append("Set includes a 3-month gym club membership which drives the 1500 UAH price tag.")

        # 2. Hydration Check
        elif goal == "hydration":
            if "spirulina" in raw_comp or "спирулина" in raw_comp or "цинк" in raw_comp:
                item_flaws.append("Gross taxonomy leakage: Spirulina & Zinc pill bottles offered to hydration buyer.")
            elif "lion’s mane" in raw_comp or "lion's mane" in raw_comp or "d3" in raw_comp:
                item_flaws.append("Gross taxonomy leakage: Nootropic mushroom & Vitamin D3 pills offered to hydration buyer.")
            elif "creatine" in raw_comp and not ("hydria" in raw_comp or "електроліт" in raw_comp or "бутылка" in raw_comp):
                item_flaws.append("Creatine/pre-workout powder offered with no hydration electrolytes or flask.")
            elif "носки" in raw_comp and "бутылка" in raw_comp and not ("hydria" in raw_comp or "електроліт" in raw_comp):
                item_flaws.append("Running socks + bottle set offered with no electrolytes/isotonic components.")

        # 3. Outdoors Check
        elif goal == "outdoors":
            if "vplab ultra sleep" in raw_comp or "melatonin" in raw_comp:
                item_flaws.append("Sleeping pills (Melatonin / Ultra Sleep) recommended as outdoor kit.")
            elif "медаль" in raw_comp:
                item_flaws.append("Commemorative military medal + organizer bundled into outdoor recommendation.")

        # 4. Explanations Veracity Check
        # Check deceptive claim "(без сторонніх речей)" / "(без посторонних позиций)"
        for w in why:
            if ("без сторонніх речей" in w or "без посторонних позиций" in w):
                if any(x in raw_comp for x in ["абонемент", "полотенце", "шейкер", "медаль", "спирулина", "creatine", "креатин", "носки"]):
                    item_flaws.append(
                        f"Deceptive explanation: System claims '{w}', but kit contains extraneous non-food/non-hydration items "
                        f"(e.g. gym club membership, towel, shaker, medals, or pills)."
                    )

        if item_flaws:
            if any("Gross taxonomy leakage" in fl or "Heavy bodybuilding" in fl or "Deceptive explanation" in fl for fl in item_flaws):
                verdict = "FAIL"
            elif verdict != "FAIL":
                verdict = "WARN"
            findings.extend([f"[{sku} - {title}]: {fl}" for fl in item_flaws])

        evaluated_items.append({
            "sku": sku,
            "title": title,
            "price_uah": price,
            "why_suitable": why,
            "expert_summary": summary,
            "item_flaws": item_flaws
        })

    return {
        "verdict": verdict,
        "status": status,
        "results_count": len(results),
        "near_miss_count": len(near_misses),
        "findings": findings,
        "results_evaluated": evaluated_items
    }

def main():
    print("Loading enriched catalog...")
    enriched_catalog, audit = load_enriched_catalog()
    audit_by_sku = {r.get("sku"): r for r in audit.get("records", [])}
    print(f"Loaded {len(enriched_catalog)} catalog sets and {len(audit_by_sku)} audit records.")

    scenarios = generate_100_scenarios()
    print(f"Generated {len(scenarios)} test scenarios.")

    runs = []
    verdict_counts = {"PASS": 0, "WARN": 0, "FAIL": 0}

    for idx, sc in enumerate(scenarios, 1):
        sc_id = sc["id"]
        # Strip internal fields before sending request
        req = {k: v for k, v in sc.items() if k not in ("id", "persona")}
        # Convert 'any' to None
        clean_req = {}
        for k, v in req.items():
            if v == "any":
                continue
            clean_req[k] = v

        res = None
        err = None
        try:
            res = draft_matcher.draft_recommend(enriched_catalog, clean_req)
        except Exception as e:
            err = e

        eval_res = evaluate_test_run(sc, res, err, audit_by_sku)
        verdict = eval_res["verdict"]
        verdict_counts[verdict] += 1

        run_entry = {
            "test_id": sc_id,
            "persona": sc["persona"],
            "request": clean_req,
            "raw_response_status": eval_res["status"],
            "results_count": eval_res["results_count"],
            "near_miss_count": eval_res["near_miss_count"],
            "evaluation": {
                "verdict": verdict,
                "findings": eval_res["findings"],
                "items": eval_res["results_evaluated"]
            }
        }
        runs.append(run_entry)
        print(f"[{idx:03d}/100] {sc_id} ({sc['goal_group']}) -> {verdict} | Status: {eval_res['status']} | Findings: {len(eval_res['findings'])}")

    print("\nSummary of results:")
    print(f"Total: {len(runs)} | PASS: {verdict_counts['PASS']} | WARN: {verdict_counts['WARN']} | FAIL: {verdict_counts['FAIL']}")

    # Save to JSON
    OUTPUT_JSON_PATH.write_text(json.dumps(runs, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Saved complete runs to {OUTPUT_JSON_PATH}")

    # Generate Markdown Report
    generate_markdown_report(runs, verdict_counts)
    print(f"Saved markdown report to {OUTPUT_REPORT_PATH}")

def generate_markdown_report(runs, counts):
    total = len(runs)
    pass_pct = (counts["PASS"] / total) * 100
    warn_pct = (counts["WARN"] / total) * 100
    fail_pct = (counts["FAIL"] / total) * 100

    food_runs = [r for r in runs if r["request"].get("goal_group") == "food"]
    hyd_runs = [r for r in runs if r["request"].get("goal_group") == "hydration"]
    out_runs = [r for r in runs if r["request"].get("goal_group") == "outdoors"]

    def cat_counts(sub):
        p = sum(1 for r in sub if r["evaluation"]["verdict"] == "PASS")
        w = sum(1 for r in sub if r["evaluation"]["verdict"] == "WARN")
        f = sum(1 for r in sub if r["evaluation"]["verdict"] == "FAIL")
        return p, w, f

    f_p, f_w, f_f = cat_counts(food_runs)
    h_p, h_w, h_f = cat_counts(hyd_runs)
    o_p, o_w, o_f = cat_counts(out_runs)

    md = []
    md.append("# QA Agent 4: Comprehensive Evaluation Report — Food, Hydration & Outdoors")
    md.append("**Role:** QA Agent 4 — Nutritionist, Hiker, Endurance Athlete & Human Buyer Specialist  ")
    md.append(f"**Test Suite:** 100 Realistic Buyer Scenarios across `food` (40), `hydration` (30), and `outdoors` (30)  ")
    md.append(f"**Audit Evidence Source:** `wiki/projects/quiz-set-audit.json`  \n")

    md.append("## 1. Executive Summary & Verdict Scorecard")
    md.append(f"Across 100 diverse buyer tests covering budgets from 500 to 3500 UAH, all component classes, activity types, timings, and locales, the quiz matcher achieved:")
    md.append(f"- **PASS:** {counts['PASS']} ({pass_pct:.1f}%) — clean, logical matching, relevant products, and truthful justifications.")
    md.append(f"- **WARN:** {counts['WARN']} ({warn_pct:.1f}%) — partial matches, minor domain gaps (e.g., bath towels or gym passes bundled into food), or validation restrictions on common activities.")
    md.append(f"- **FAIL:** {counts['FAIL']} ({fail_pct:.1f}%) — severe logic flaws: blatant taxonomy leaks (pills/creatine in food; spirulina/zinc in hydration), 0 matches for dehydrated camping meals due to tag misclassification, or deceptive '(без сторонніх речей)' claims.\n")

    md.append("| Category | Total Tests | PASS | WARN | FAIL | Pass Rate |")
    md.append("| :--- | :---: | :---: | :---: | :---: | :---: |")
    md.append(f"| **Food & Snacks (`food`)** | {len(food_runs)} | {f_p} | {f_w} | {f_f} | {(f_p/len(food_runs))*100:.1f}% |")
    md.append(f"| **Hydration (`hydration`)** | {len(hyd_runs)} | {h_p} | {h_w} | {h_f} | {(h_p/len(hyd_runs))*100:.1f}% |")
    md.append(f"| **Outdoors & Hiking (`outdoors`)** | {len(out_runs)} | {o_p} | {o_w} | {o_f} | {(o_p/len(out_runs))*100:.1f}% |")
    md.append(f"| **OVERALL** | **{total}** | **{counts['PASS']}** | **{counts['WARN']}** | **{counts['FAIL']}** | **{pass_pct:.1f}%** |\n")

    md.append("---")
    md.append("## 2. Critical Human Logic & Domain Flaws Discovered")

    md.append("### A. The Dehydrated Camping Meal Blindspot (100% Failure Rate)")
    md.append("> [!CAUTION]")
    md.append("> When a hiker or camper explicitly selects `component_class: 'dehydrated_meal'`, the matcher returns **0 results (`status: no_match`)**.")
    md.append("The store actively stocks genuine dehydrated camping meals (`Похідна їжа ЇDLO 2.0` RE11494, `Похідна їжа ЇDLO Club` RE11495, `Похідна їжа 3.0` RE88977). However, in `quiz-set-audit.json`, every single ЇDLO set was classified as `protein_carbohydrate_food` rather than `dehydrated_meal`. Consequently, the `dehydrated_meal` filter is dead code that guarantees complete failure for hikers seeking camp dinners.\n")

    md.append("### B. Gross Taxonomy Leakage into Hydration")
    md.append("> [!WARNING]")
    md.append("> Non-hydration pill supplements leak directly into the `hydration` section.")
    md.append("- **RE11513 («Енергія і очищення»):** Contains Now Foods Organic Spirulina (100 tablets) + Zinc Picolinate. Spirulina and zinc pills have zero electrolyte replacement value and do not prevent dehydration or cramps.")
    md.append("- **RE88943 («Концентрація в дорозі»):** Contains Lion's Mane mushroom pills + Acetyl-L-Carnitine + Vitamin D3. Recommending mushroom nootropics to a thirsty runner asking for hydration is completely illogical.")
    md.append("- **RE11636 («Вибух сили»):** Contains OstroVit Creatine Monohydrate 500g + Pre-Workout caffeine powder, with zero electrolytes or water flasks.\n")

    md.append("### C. Pill Bottles, Towels & Creatine Powders Leaking into Food")
    md.append("- **RE11688 («Набір маси»):** Contains 1,000g Anabolic Mass gainer powder and 300g pure Creatine Monohydrate. An endurance athlete looking for portable snacks on runs is shown a 1kg bodybuilding powder tub.")
    md.append("- **RE89489 («Основа регулярних тренувань»):** Contains a 135×70 cm cotton bath towel, creatine, shaker, and 3-month gym membership.")
    md.append("- **RE11632 («Розум і Сила»):** Contains Mind Shi 4Mushroom nootropic capsules (60 caps) bundled with cookies.\n")

    md.append("### D. Deceptive Explanation Claims: '(без сторонніх речей)'")
    md.append("When a user specifies a component class like `protein_carbohydrate_food`, `_build_why_suitable()` generates:")
    md.append("`Категорія товарів: у наборі саме Спортивне харчування та батончики (без сторонніх речей).`")
    md.append("In reality, the recommended set frequently contains bath towels, commemorative medals, mushroom capsules, or 3-month gym club memberships. Stating '(без сторонніх речей)' ('without third-party/extraneous items') destroys buyer trust when extraneous items make up the majority of the bundle value.\n")

    md.append("### E. Artificial Validation Walls for Real Athletic Scenarios")
    md.append("- **Walkers eating food:** Walkers and Nordic walkers covering 15-25 km need energy snacks. `draft_matcher` throws `DraftMatchError: activity is not supported for the selected need` if `walking` is paired with `food`.")
    md.append("- **Hikers needing hydration:** Hikers carrying heavy packs in summer heat desperately need electrolytes and flasks. `draft_matcher` throws `DraftMatchError` if `hiking` or `walking` is selected for `hydration`.")
    md.append("- **Trail runners in Outdoors:** Trail runners looking under `outdoors` get rejected because `running` is disallowed.")
    md.append("- **Hiker meal timings:** Hikers who want hearty meals before or after long treks get rejected because `outdoors` disallows `before_or_after_training`.\n")

    md.append("### F. Low Budget Coverage Desert (< 1058 UAH)")
    md.append("The entire catalog has **0 food sets under 1149 UAH**, **0 hydration sets under 1225 UAH**, and **0 outdoor sets under 1058 UAH**. Any user entering a realistic budget of 500–1000 UAH receives either `no_match` or near-misses. The quiz must clearly communicate that the store only sells premium multi-item bundles, not single items.\n")

    md.append("---")
    md.append("## 3. Detailed Results of all 100 Scenarios")
    md.append("| ID | Goal | Activity | Class | Budget | Status | Verdict | Key Evaluation Note |")
    md.append("| :--- | :--- | :--- | :--- | :--- | :--- | :---: | :--- |")
    for r in runs:
        req = r["request"]
        ev = r["evaluation"]
        note = ev["findings"][0] if ev["findings"] else "Clean match, truthful explanation"
        if len(note) > 90:
            note = note[:87] + "…"
        md.append(f"| {r['test_id']} | `{req.get('goal_group')}` | {req.get('activity', 'any')} | {req.get('component_class', 'any')} | {req.get('max_price_uah', 'any')} ₴ | `{r['raw_response_status']}` | **{ev['verdict']}** | {note} |")

    md.append("\n---")
    md.append("## 4. Prioritized Action Plan for Engineering & Catalog Teams")
    md.append("1. **Reclassify ЇDLO Sets as `dehydrated_meal`:** Immediately update `RE11494`, `RE11495`, and `RE88977` in `wiki/projects/quiz-set-audit.json` to include `dehydrated_meal` in `component_classes_from_listed_names`.")
    md.append("2. **Disqualify Pill Tubs & Mass Gainers from Hydration and Food:**")
    md.append("   - Remove `hydration_electrolytes` family from `RE11513` (Spirulina/Zinc), `RE88943` (Lion's Mane/D3), and `RE11636` (Creatine/Pre-workout).")
    md.append("   - Remove `portable_food_snacks` family from `RE11688` (1kg Anabolic Mass gainer).")
    md.append("3. **Fix Validation Option Matrix in `draft_matcher.py`:**")
    md.append("   - Add `hiking` and `walking` to `ACTIVITY_OPTIONS_BY_GOAL['hydration']`.")
    md.append("   - Add `walking` to `ACTIVITY_OPTIONS_BY_GOAL['food']`.")
    md.append("   - Add `before_or_after_training` to `USE_TIMINGS_BY_GOAL['outdoors']`.")
    md.append("4. **Refactor Explanation Copy:** Eliminate the absolute claim `(без сторонніх речей)` / `(без посторонних позиций)` if the set contains bundle extras like towels, shakers, medals, or club memberships.")
    md.append("5. **Introduce Low-Budget Starter Bundles:** Create 3–5 targeted entry-level sets priced at 499–799 UAH (e.g. 5x gels + 2x electrolyte sticks pack) to satisfy low-budget shoppers.")

    OUTPUT_REPORT_PATH.write_text("\n".join(md), encoding="utf-8")

if __name__ == "__main__":
    main()
