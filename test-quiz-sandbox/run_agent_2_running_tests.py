#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""QA Agent 2: 100 Running & Endurance Buyer Test Scenarios & Evaluation."""

import json
import os
import sys
from pathlib import Path

# Add test-quiz-sandbox to path
SANDBOX_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SANDBOX_DIR.parent
sys.path.insert(0, str(SANDBOX_DIR))

from draft_matcher import attach_audit_evidence, draft_recommend, DraftMatchError

CATALOG_PATH = SANDBOX_DIR / "catalog.json"
AUDIT_PATH = PROJECT_ROOT / "wiki" / "projects" / "quiz-set-audit.json"
OUTPUT_JSON = SANDBOX_DIR / "agent_2_running_100_tests.json"
OUTPUT_REPORT = SANDBOX_DIR / "agent_2_report.md"

def load_environment():
    cat = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    audit = json.loads(AUDIT_PATH.read_text(encoding="utf-8"))
    catalog = attach_audit_evidence(cat, audit)
    return catalog

def generate_100_scenarios():
    """Generate 100 distinct, diverse, realistic buyer scenarios for running."""
    scenarios = []

    # Helper to add scenario
    def add(scenario_id, name, persona, request_params, expected_focus):
        scenarios.append({
            "test_id": scenario_id,
            "name": name,
            "persona": persona,
            "request": {"goal_group": "running", **request_params},
            "expected_focus": expected_focus
        })

    # Group 1: Marathon Runners (20 scenarios)
    # Different budgets, components, timings, forms
    scenarios_marathon = [
        (1, "Marathoner: Energy gels during race, high budget", "Experienced runner aiming for sub-3h marathon",
         {"component_class": "protein_carbohydrate_food", "use_scenario": "event_preparation", "use_timing": "during_training", "race_format": "marathon", "product_form": "gel", "max_price_uah": 2500, "locale": "ru"},
         "Expects high-carb energy gels for marathon race day without heavy creatine or gym mass gainers."),
        (2, "Marathoner: Energy gels, medium budget", "First-time marathon runner needing race nutrition",
         {"component_class": "protein_carbohydrate_food", "use_scenario": "event_preparation", "use_timing": "during_training", "race_format": "marathon", "product_form": "gel", "max_price_uah": 1500, "locale": "uk"},
         "Expects sufficient gels/energy pack for 42.2 km within 1500 UAH."),
        (3, "Marathoner: Tight budget gels", "Student preparing for Kyiv Marathon on tight budget",
         {"component_class": "protein_carbohydrate_food", "use_scenario": "event_preparation", "use_timing": "during_training", "race_format": "marathon", "product_form": "gel", "max_price_uah": 800, "locale": "uk"},
         "Tests tight budget handling for marathon gels; expects near-miss or floor anchor rather than socks."),
        (4, "Marathoner: Hydration & electrolytes during race", "Marathoner prone to muscle cramps and dehydration in warm weather",
         {"component_class": "hydration_items", "use_scenario": "event_preparation", "use_timing": "during_training", "race_format": "marathon", "max_price_uah": 1600, "locale": "ru"},
         "Expects isotonic sticks or electrolyte hydration packs for marathon distances."),
        (5, "Marathoner: Hydration, tight budget (700 UAH)", "Budget-conscious runner needing electrolyte replenishment",
         {"component_class": "hydration_items", "use_scenario": "event_preparation", "use_timing": "during_training", "race_format": "marathon", "max_price_uah": 700, "locale": "uk"},
         "Expects reasonable hydration floor anchor or honest budget warning without irrelevant gear."),
        (6, "Marathoner: Salt capsules for cramp prevention", "Hot marathon runner wanting sodium/electrolyte capsules",
         {"component_class": "hydration_items", "use_scenario": "event_preparation", "use_timing": "during_training", "race_format": "marathon", "product_form": "capsules", "max_price_uah": 1500, "locale": "ru"},
         "Tests product_form='capsules' for marathon electrolytes. (Known schema constraint: running restricts product_form)."),
        (7, "Marathoner: Isotonic powder in tubs", "Runner training weekly 30km long runs wanting tub powder",
         {"component_class": "hydration_items", "use_scenario": "training", "use_timing": "during_training", "race_format": "marathon", "product_form": "powder", "max_price_uah": 1800, "locale": "uk"},
         "Tests product_form='powder' for endurance runner. Check schema validation vs buyer need."),
        (8, "Marathoner: Anti-blister racing socks size 42", "Runner looking for specialized marathon socks to prevent blisters",
         {"component_class": "apparel_footwear", "use_scenario": "event_preparation", "use_timing": "during_training", "race_format": "marathon", "shoe_size": 42, "max_price_uah": 1200, "locale": "ru"},
         "Expects technical running socks matching size 42."),
        (9, "Marathoner: Winter marathon thermal socks size 45", "Winter marathon runner needing warm thermal socks",
         {"component_class": "apparel_footwear", "use_scenario": "event_preparation", "use_timing": "during_training", "race_format": "marathon", "season": "cold", "shoe_size": 45, "max_price_uah": 1200, "locale": "uk"},
         "Expects thermal running socks matching size 45."),
        (10, "Marathoner: Marathon accessories (bib belt, flask)", "Marathoner needing race bib belt with gel loops",
         {"component_class": "sports_accessories", "use_scenario": "event_preparation", "use_timing": "during_training", "race_format": "marathon", "max_price_uah": 1500, "locale": "ru"},
         "Expects running accessories like bib belt, soft flasks, or race belt."),
        (11, "Marathoner: Recovery nutrition after 42k", "Marathoner looking for post-race muscle recovery carbohydrates and protein",
         {"component_class": "protein_carbohydrate_food", "use_scenario": "event_preparation", "use_timing": "before_or_after_training", "race_format": "marathon", "max_price_uah": 2000, "locale": "uk"},
         "Expects recovery bars/protein snacks suitable for endurance runner recovery."),
        (12, "Marathoner: General prep, any component, medium budget", "Amateur marathon runner preparing for first marathon, budget 1500 UAH",
         {"component_class": "any", "use_scenario": "event_preparation", "use_timing": "during_training", "race_format": "marathon", "max_price_uah": 1500, "locale": "ru"},
         "Expects top marathon kit; verify whether Creatine 300g or explosive power pitch leaks in."),
        (13, "Marathoner: High-budget complete preparation (4000 UAH)", "Wealthy executive running Berlin Marathon wanting best package",
         {"component_class": "any", "use_scenario": "event_preparation", "use_timing": "during_training", "race_format": "marathon", "max_price_uah": 4000, "locale": "uk"},
         "Expects premium marathon endurance kit; check price ceiling and set appropriateness."),
        (14, "Marathoner: Energy bars for training long runs", "Marathoner wanting chewable solid energy bars for 3-hour long runs",
         {"component_class": "protein_carbohydrate_food", "use_scenario": "training", "use_timing": "during_training", "race_format": "marathon", "product_form": "bars", "max_price_uah": 1600, "locale": "ru"},
         "Expects energy bars; verify whether socks or gear masquerade as bars."),
        (15, "Marathoner: Multi-choice form (gels + bars)", "Marathoner wanting combined fueling: gels during + bars before/after",
         {"component_class": "protein_carbohydrate_food", "use_scenario": "event_preparation", "use_timing": "during_training", "race_format": "marathon", "product_form": ["gel", "bars"], "max_price_uah": 1800, "locale": "uk"},
         "Expects nutrition set combining both gels and bars."),
        (16, "Marathoner: Electrolyte sticks for portable flask mixing", "Marathoner carrying 500ml soft flasks wanting single-serve sticks",
         {"component_class": "hydration_items", "use_scenario": "event_preparation", "use_timing": "during_training", "race_format": "marathon", "product_form": "sticks", "max_price_uah": 1600, "locale": "ru"},
         "Expects electrolyte sticks for on-the-go hydration."),
        (17, "Marathoner: Daily hydration tonus during 16-week build", "Marathoner needing daily mineral hydration during high-mileage blocks",
         {"component_class": "hydration_items", "use_scenario": "everyday", "use_timing": "daily_use", "race_format": "marathon", "max_price_uah": 1500, "locale": "uk"},
         "Expects daily hydration/electrolyte support."),
        (18, "Marathoner: Low budget socks size 41 (600 UAH)", "Marathoner on budget looking for cheap socks",
         {"component_class": "apparel_footwear", "use_scenario": "training", "use_timing": "during_training", "race_format": "marathon", "shoe_size": 41, "max_price_uah": 600, "locale": "ru"},
         "Expects near miss/floor anchor to 950 UAH sock multipack."),
        (19, "Marathoner: Accessories + food combination check", "Runner wanting race belt + gels",
         {"component_class": "sports_accessories", "use_scenario": "event_preparation", "use_timing": "during_training", "race_format": "marathon", "product_form": "gel", "max_price_uah": 1600, "locale": "uk"},
         "Checks interaction between sports_accessories and product_form=gel (e.g. Набір «Марафонський темп»)."),
        (20, "Marathoner: Pre-race carb loading / breakfast", "Marathoner wanting pre-race carbs before starting 42k",
         {"component_class": "protein_carbohydrate_food", "use_scenario": "event_preparation", "use_timing": "before_or_after_training", "race_format": "marathon", "max_price_uah": 1700, "locale": "ru"},
         "Expects easily digestible pre-race carbs/bars.")
    ]
    for sc in scenarios_marathon:
        add(*sc)

    # Group 2: Half-Marathon Runners (20 scenarios)
    # The 21.1 km distance is Ukraine's most popular mass race format
    scenarios_half = [
        (21, "Half-marathoner: Race gels, medium budget (1500 UAH)", "Runner training for Nova Poshta Half Marathon needing 3-4 gels",
         {"component_class": "protein_carbohydrate_food", "use_scenario": "event_preparation", "use_timing": "during_training", "race_format": "half_marathon", "product_form": "gel", "max_price_uah": 1500, "locale": "uk"},
         "Expects race energy gels suitable for 21.1 km. CRITICAL: Test catalog half_marathon tagging."),
        (22, "Half-marathoner: Race gels, tight budget (900 UAH)", "First-time 21k runner on tight budget",
         {"component_class": "protein_carbohydrate_food", "use_scenario": "event_preparation", "use_timing": "during_training", "race_format": "half_marathon", "product_form": "gel", "max_price_uah": 900, "locale": "ru"},
         "Check budget response and catalog half_marathon coverage."),
        (23, "Half-marathoner: Hydration & electrolytes during training", "Runner needing electrolytes during 15-18km weekend runs",
         {"component_class": "hydration_items", "use_scenario": "training", "use_timing": "during_training", "race_format": "half_marathon", "max_price_uah": 1500, "locale": "uk"},
         "Expects hydration sticks or electrolytes for 21k training."),
        (24, "Half-marathoner: Salt capsules for hot weather half", "Runner in summer 21k race prone to severe sweating",
         {"component_class": "hydration_items", "use_scenario": "event_preparation", "use_timing": "during_training", "race_format": "half_marathon", "product_form": "capsules", "max_price_uah": 1400, "locale": "ru"},
         "Check if salt capsules are allowed/supported for half-marathon runner."),
        (25, "Half-marathoner: Running socks size 37", "Female half-marathoner needing anti-chafing socks",
         {"component_class": "apparel_footwear", "use_scenario": "event_preparation", "use_timing": "during_training", "race_format": "half_marathon", "shoe_size": 37, "max_price_uah": 1100, "locale": "uk"},
         "Expects running socks matching size 35-37."),
        (26, "Half-marathoner: Running socks size 43", "Male runner looking for 5-pack socks for half-marathon block",
         {"component_class": "apparel_footwear", "use_scenario": "training", "use_timing": "during_training", "race_format": "half_marathon", "shoe_size": 43, "max_price_uah": 1100, "locale": "ru"},
         "Expects running socks matching size 43-45."),
        (27, "Half-marathoner: Bib belt and bottle accessory", "Runner needing bottle and bib clip for 21k race",
         {"component_class": "sports_accessories", "use_scenario": "event_preparation", "use_timing": "during_training", "race_format": "half_marathon", "max_price_uah": 1500, "locale": "uk"},
         "Expects running accessories."),
        (28, "Half-marathoner: Energy bars for recovery", "Runner wanting post-run carb-protein bars after half-marathon",
         {"component_class": "protein_carbohydrate_food", "use_scenario": "event_preparation", "use_timing": "before_or_after_training", "race_format": "half_marathon", "product_form": "bars", "max_price_uah": 1600, "locale": "ru"},
         "Expects protein/energy bars without gym hypertrophy pitch."),
        (29, "Half-marathoner: High budget comprehensive prep (3000 UAH)", "Runner with ample budget wanting full half-marathon kit",
         {"component_class": "any", "use_scenario": "event_preparation", "use_timing": "during_training", "race_format": "half_marathon", "max_price_uah": 3000, "locale": "uk"},
         "Tests high-budget matching for half-marathon."),
        (30, "Half-marathoner: Tight budget (500 UAH)", "Student looking for minimal entry set for half-marathon",
         {"component_class": "any", "use_scenario": "event_preparation", "use_timing": "during_training", "race_format": "half_marathon", "max_price_uah": 500, "locale": "ru"},
         "Tests floor anchor / near miss at extreme low budget."),
        (31, "Half-marathoner: Daily training snacks", "Half-marathoner needing healthy everyday fuel for afternoon sessions",
         {"component_class": "protein_carbohydrate_food", "use_scenario": "everyday", "use_timing": "daily_use", "race_format": "half_marathon", "product_form": "bars", "max_price_uah": 1500, "locale": "uk"},
         "Expects daily endurance bars/snacks."),
        (32, "Half-marathoner: Liquid energy shots", "Runner wanting liquid fast-acting caffeine or energy shots for 18th km boost",
         {"component_class": "protein_carbohydrate_food", "use_scenario": "event_preparation", "use_timing": "during_training", "race_format": "half_marathon", "product_form": "liquid", "max_price_uah": 1600, "locale": "ru"},
         "Checks liquid form matching for half-marathon."),
        (33, "Half-marathoner: Multi-choice forms [gel, sticks]", "Runner wanting gels for energy + electrolyte sticks for water",
         {"component_class": "hydration_items", "use_scenario": "event_preparation", "use_timing": "during_training", "race_format": "half_marathon", "product_form": ["gel", "sticks"], "max_price_uah": 1600, "locale": "uk"},
         "Expects balanced hydration and fuel kit."),
        (34, "Half-marathoner: Isotonic powder for water bottle", "Half-marathoner wanting powder mix for bottle before training",
         {"component_class": "hydration_items", "use_scenario": "training", "use_timing": "before_or_after_training", "race_format": "half_marathon", "product_form": "powder", "max_price_uah": 1400, "locale": "ru"},
         "Tests product_form='powder' behavior for half-marathon."),
        (35, "Half-marathoner: Fall race cold weather socks size 40", "Autumn half-marathon runner facing rain and 5°C",
         {"component_class": "apparel_footwear", "use_scenario": "event_preparation", "use_timing": "during_training", "race_format": "half_marathon", "season": "cold", "shoe_size": 40, "max_price_uah": 1200, "locale": "uk"},
         "Expects technical running socks for cold weather."),
        (36, "Half-marathoner: Pre-race breakfast bars", "Runner needing solid light breakfast before 9:00 AM half start",
         {"component_class": "protein_carbohydrate_food", "use_scenario": "event_preparation", "use_timing": "before_or_after_training", "race_format": "half_marathon", "product_form": "bars", "max_price_uah": 1500, "locale": "ru"},
         "Expects pre-run energy bars."),
        (37, "Half-marathoner: Electrolyte sticks for daily hydration", "Half-marathoner battling summer dehydration",
         {"component_class": "hydration_items", "use_scenario": "everyday", "use_timing": "daily_use", "race_format": "half_marathon", "product_form": "sticks", "max_price_uah": 1500, "locale": "uk"},
         "Expects daily hydration sticks."),
        (38, "Half-marathoner: Budget 1200 UAH, any component", "Runner with 1200 UAH budget, open to suggestions",
         {"component_class": "any", "use_scenario": "training", "use_timing": "during_training", "race_format": "half_marathon", "max_price_uah": 1200, "locale": "ru"},
         "Tests general half-marathon matching under 1200 UAH."),
        (39, "Half-marathoner: Spring 10k/21k build with gear", "Runner updating gear for spring 21k",
         {"component_class": "sports_accessories", "use_scenario": "training", "use_timing": "during_training", "race_format": "half_marathon", "max_price_uah": 1400, "locale": "uk"},
         "Expects running accessories."),
        (40, "Half-marathoner: High budget (2500 UAH) food & energy", "Experienced runner wanting premium fuel for half-marathon PB",
         {"component_class": "protein_carbohydrate_food", "use_scenario": "event_preparation", "use_timing": "during_training", "race_format": "half_marathon", "max_price_uah": 2500, "locale": "ru"},
         "Tests high-budget food matching for 21.1 km.")
    ]
    for sc in scenarios_half:
        add(*sc)

    # Group 3: Ultra & Long Distance / Trail Runners (20 scenarios)
    # Ultra-distance: 50k, 100k, mountain trail, demanding serious calorie & mineral replacement
    scenarios_ultra = [
        (41, "Ultra-trail runner: Mountain 50k energy & hydration", "Carpathian trail 50k runner needing high carbs and electrolytes",
         {"component_class": "hydration_items", "use_scenario": "event_preparation", "use_timing": "during_training", "race_format": "ultra_or_long_distance", "product_form": "gel", "max_price_uah": 2000, "locale": "uk"},
         "Expects high-end ultra endurance kit (e.g. UT-PRO-2026)."),
        (42, "Ultra runner: Calorie-dense food for 8-hour race", "100k ultramarathoner needing bars, chews, and slow carbs",
         {"component_class": "protein_carbohydrate_food", "use_scenario": "event_preparation", "use_timing": "during_training", "race_format": "ultra_or_long_distance", "product_form": "bars", "max_price_uah": 2500, "locale": "ru"},
         "Expects high-calorie portable endurance food."),
        (43, "Ultra runner: Salt sticks / electrolyte sticks", "Desert/summer trail runner consuming 1g sodium per hour",
         {"component_class": "hydration_items", "use_scenario": "event_preparation", "use_timing": "during_training", "race_format": "ultra_or_long_distance", "product_form": "sticks", "max_price_uah": 1800, "locale": "uk"},
         "Expects electrolyte sticks for intense ultra sweat rates."),
        (44, "Ultra runner: Electrolyte capsules for multi-hour trail", "Trail runner carrying salt capsules in zip bag",
         {"component_class": "hydration_items", "use_scenario": "event_preparation", "use_timing": "during_training", "race_format": "ultra_or_long_distance", "product_form": "capsules", "max_price_uah": 1600, "locale": "ru"},
         "Tests capsules form for ultra running."),
        (45, "Ultra runner: Isotonic powder tub for training camps", "Runner on mountain training camp needing large quantity powder",
         {"component_class": "hydration_items", "use_scenario": "training", "use_timing": "during_training", "race_format": "ultra_or_long_distance", "product_form": "powder", "max_price_uah": 2200, "locale": "uk"},
         "Tests powder form for ultra runner."),
        (46, "Ultra runner: High budget all-inclusive pack (4500 UAH)", "Ultra runner investing in top gear and nutrition",
         {"component_class": "any", "use_scenario": "event_preparation", "use_timing": "during_training", "race_format": "ultra_or_long_distance", "max_price_uah": 4500, "locale": "ru"},
         "Expects best ultra/endurance sets in catalog."),
        (47, "Ultra runner: Tight budget (1000 UAH)", "Budget trail runner looking for basic ultra fuel",
         {"component_class": "hydration_items", "use_scenario": "event_preparation", "use_timing": "during_training", "race_format": "ultra_or_long_distance", "max_price_uah": 1000, "locale": "uk"},
         "Check budget handling: UT-PRO-2026 is 1650 UAH; expects truthful near miss/floor anchor."),
        (48, "Ultra runner: Anti-friction thermal socks size 44", "Mountain ultra runner facing wet trails, blisters, and freezing ridges",
         {"component_class": "apparel_footwear", "use_scenario": "event_preparation", "use_timing": "during_training", "race_format": "ultra_or_long_distance", "season": "cold", "shoe_size": 44, "max_price_uah": 1500, "locale": "ru"},
         "Expects heavy-duty running socks size 43-45."),
        (49, "Ultra runner: Trail running accessories (belt, soft flask)", "Ultra runner needing bottle and gear storage",
         {"component_class": "sports_accessories", "use_scenario": "event_preparation", "use_timing": "during_training", "race_format": "ultra_or_long_distance", "max_price_uah": 1600, "locale": "uk"},
         "Expects endurance accessories."),
        (50, "Ultra runner: Multi-form nutrition [gel, bars, sticks]", "Ultra runner needing diverse fuel to avoid taste fatigue",
         {"component_class": "hydration_items", "use_scenario": "event_preparation", "use_timing": "during_training", "race_format": "ultra_or_long_distance", "product_form": ["gel", "sticks"], "max_price_uah": 2200, "locale": "ru"},
         "Expects UT-PRO-2026 or similar multi-fuel set."),
        (51, "Ultra runner: Post-ultra recovery nutrition", "Runner recovering from 60km trail, needing muscle repair food",
         {"component_class": "protein_carbohydrate_food", "use_scenario": "event_preparation", "use_timing": "before_or_after_training", "race_format": "ultra_or_long_distance", "max_price_uah": 2000, "locale": "uk"},
         "Expects post-race endurance recovery nutrition."),
        (52, "Ultra runner: Daily training hydration during 100k weeks", "High-volume ultra runner needing daily electrolyte maintenance",
         {"component_class": "hydration_items", "use_scenario": "everyday", "use_timing": "daily_use", "race_format": "ultra_or_long_distance", "max_price_uah": 1600, "locale": "ru"},
         "Expects daily electrolyte sticks/hydration."),
        (53, "Ultra runner: Extreme budget (600 UAH)", "Ultra runner with very low budget",
         {"component_class": "any", "use_scenario": "event_preparation", "use_timing": "during_training", "race_format": "ultra_or_long_distance", "max_price_uah": 600, "locale": "uk"},
         "Tests floor anchor messaging when budget is far below 1650 UAH."),
        (54, "Ultra runner: Medium budget gels (1500 UAH)", "Ultra runner needing gels under 1500 UAH",
         {"component_class": "protein_carbohydrate_food", "use_scenario": "training", "use_timing": "during_training", "race_format": "ultra_or_long_distance", "product_form": "gel", "max_price_uah": 1500, "locale": "ru"},
         "Checks whether food matches ultra format at 1500 UAH."),
        (55, "Ultra runner: Ready meals for multi-day stage race", "Stage racer needing lightweight ready dehydrated meal",
         {"component_class": "protein_carbohydrate_food", "use_scenario": "event_preparation", "use_timing": "before_or_after_training", "race_format": "ultra_or_long_distance", "product_form": "food_or_meal", "max_price_uah": 2000, "locale": "uk"},
         "Tests food_or_meal form under running goal."),
        (56, "Ultra runner: Summer ultra socks size 41", "Ultra runner needing thin, breathable socks for 80k in 30°C heat",
         {"component_class": "apparel_footwear", "use_scenario": "training", "use_timing": "during_training", "race_format": "ultra_or_long_distance", "season": "warm", "shoe_size": 41, "max_price_uah": 1200, "locale": "ru"},
         "Expects breathable running socks size 40-42."),
        (57, "Ultra runner: Winter ultra trail accessories", "Winter trail runner needing buff and thermal gear",
         {"component_class": "sports_accessories", "use_scenario": "training", "use_timing": "during_training", "race_format": "ultra_or_long_distance", "season": "cold", "max_price_uah": 1500, "locale": "uk"},
         "Expects winter running accessories like buff/gloves."),
        (58, "Ultra runner: Liquid energy shots for night stages", "Ultra runner needing caffeine liquid shots for midnight miles",
         {"component_class": "protein_carbohydrate_food", "use_scenario": "event_preparation", "use_timing": "during_training", "race_format": "ultra_or_long_distance", "product_form": "liquid", "max_price_uah": 1700, "locale": "ru"},
         "Tests liquid form for ultra race."),
        (59, "Ultra runner: Any component, 1800 UAH budget", "Ultra runner with standard budget looking for best endurance kit",
         {"component_class": "any", "use_scenario": "event_preparation", "use_timing": "during_training", "race_format": "ultra_or_long_distance", "max_price_uah": 1800, "locale": "uk"},
         "Expects UT-PRO-2026 (1650 UAH) to be top match."),
        (60, "Ultra runner: High budget (3500 UAH) hydration focus", "Ultra runner wanting best hydration support available",
         {"component_class": "hydration_items", "use_scenario": "event_preparation", "use_timing": "during_training", "race_format": "ultra_or_long_distance", "max_price_uah": 3500, "locale": "ru"},
         "Expects top hydration kit.")
    ]
    for sc in scenarios_ultra:
        add(*sc)

    # Group 4: 5k/10k & General Race Preparation (20 scenarios)
    # race_format: "race_or_event_preparation"
    scenarios_race_prep = [
        (61, "10k Beginner: First race preparation energy gel", "Beginner running first 10k race needing 1 test gel",
         {"component_class": "protein_carbohydrate_food", "use_scenario": "event_preparation", "use_timing": "during_training", "race_format": "race_or_event_preparation", "product_form": "gel", "max_price_uah": 1500, "locale": "uk"},
         "Expects beginner-friendly race energy nutrition."),
        (62, "10k Beginner: Tight budget nutrition (800 UAH)", "Beginner runner on 800 UAH budget for 10k prep",
         {"component_class": "protein_carbohydrate_food", "use_scenario": "event_preparation", "use_timing": "during_training", "race_format": "race_or_event_preparation", "max_price_uah": 800, "locale": "ru"},
         "Tests budget floor/near-miss for race food."),
        (63, "5k Runner: Fast energy bar before evening 5k race", "Runner doing local 5k time trial wanting pre-race snack",
         {"component_class": "protein_carbohydrate_food", "use_scenario": "event_preparation", "use_timing": "before_or_after_training", "race_format": "race_or_event_preparation", "product_form": "bars", "max_price_uah": 1500, "locale": "uk"},
         "Expects light energy bars before short race."),
        (64, "Race prep: Hydration electrolytes for 10k race", "Runner needing electrolytes in warm weather 10k",
         {"component_class": "hydration_items", "use_scenario": "event_preparation", "use_timing": "during_training", "race_format": "race_or_event_preparation", "max_price_uah": 1500, "locale": "ru"},
         "Expects hydration sticks/electrolytes."),
        (65, "Race prep: Tight budget hydration (750 UAH)", "Runner wanting cheap electrolytes for upcoming 10k",
         {"component_class": "hydration_items", "use_scenario": "event_preparation", "use_timing": "during_training", "race_format": "race_or_event_preparation", "max_price_uah": 750, "locale": "uk"},
         "Tests hydration floor anchor at 750 UAH."),
        (66, "Race prep: Socks size 36 for race day", "Runner looking for competition socks size 36",
         {"component_class": "apparel_footwear", "use_scenario": "event_preparation", "use_timing": "during_training", "race_format": "race_or_event_preparation", "shoe_size": 36, "max_price_uah": 1000, "locale": "ru"},
         "Expects race socks matching size 35-37 under 1000 UAH."),
        (67, "Race prep: Socks size 46 for large feet", "Tall runner needing size 46 running socks for race",
         {"component_class": "apparel_footwear", "use_scenario": "event_preparation", "use_timing": "during_training", "race_format": "race_or_event_preparation", "shoe_size": 46, "max_price_uah": 1100, "locale": "uk"},
         "Expects running socks matching size 46-48 (e.g. RE89632 / RE89631)."),
        (68, "Race prep: Race starter pack (belt, cap, bottle)", "New runner needing starter accessories for first charity run",
         {"component_class": "sports_accessories", "use_scenario": "event_preparation", "use_timing": "during_training", "race_format": "race_or_event_preparation", "max_price_uah": 1500, "locale": "ru"},
         "Expects starter accessory kit (e.g. Набір «Підготовка до забігу»)."),
        (69, "Race prep: High budget comprehensive race kit (3000 UAH)", "Enthusiastic beginner buying complete race prep set",
         {"component_class": "any", "use_scenario": "event_preparation", "use_timing": "during_training", "race_format": "race_or_event_preparation", "max_price_uah": 3000, "locale": "uk"},
         "Expects complete race kit."),
        (70, "Race prep: Tight budget general (900 UAH)", "Runner with 900 UAH wanting anything useful for race",
         {"component_class": "any", "use_scenario": "event_preparation", "use_timing": "during_training", "race_format": "race_or_event_preparation", "max_price_uah": 900, "locale": "ru"},
         "Tests floor anchor / near miss to 950 UAH socks."),
        (71, "Race prep: Summer heat defense electrolytes", "Veteran athlete running summer event in extreme heat",
         {"component_class": "hydration_items", "use_scenario": "event_preparation", "use_timing": "during_training", "race_format": "race_or_event_preparation", "season": "warm", "max_price_uah": 1300, "locale": "uk"},
         "Expects heat protection electrolytes (e.g. RE11650 «Захист від спеки»)."),
        (72, "Race prep: Ready snacks for race morning", "Runner wanting easy-to-eat breakfast on race bus",
         {"component_class": "protein_carbohydrate_food", "use_scenario": "event_preparation", "use_timing": "before_or_after_training", "race_format": "race_or_event_preparation", "product_form": "food_or_meal", "max_price_uah": 1600, "locale": "ru"},
         "Expects pre-race meal/bars."),
        (73, "Race prep: Multi-choice [bars, sticks]", "Runner wanting bars before + electrolyte sticks during",
         {"component_class": "protein_carbohydrate_food", "use_scenario": "event_preparation", "use_timing": "during_training", "race_format": "race_or_event_preparation", "product_form": ["bars", "sticks"], "max_price_uah": 1600, "locale": "uk"},
         "Expects combination nutrition set."),
        (74, "Race prep: Powder mix for pre-race hydration", "Runner mixing carb-electrolyte drink before start",
         {"component_class": "hydration_items", "use_scenario": "event_preparation", "use_timing": "before_or_after_training", "race_format": "race_or_event_preparation", "product_form": "powder", "max_price_uah": 1500, "locale": "ru"},
         "Tests product_form='powder' under race_prep."),
        (75, "Race prep: Electrolyte capsules for pre-race dosing", "Runner wanting electrolyte capsules before 10k",
         {"component_class": "hydration_items", "use_scenario": "event_preparation", "use_timing": "before_or_after_training", "race_format": "race_or_event_preparation", "product_form": "capsules", "max_price_uah": 1500, "locale": "uk"},
         "Tests capsules under race_prep."),
        (76, "Race prep: Medium budget accessories (1300 UAH)", "Runner wanting race gear under 1300 UAH",
         {"component_class": "sports_accessories", "use_scenario": "event_preparation", "use_timing": "during_training", "race_format": "race_or_event_preparation", "max_price_uah": 1300, "locale": "ru"},
         "Expects accessories within 1300 UAH."),
        (77, "Race prep: Winter 10k thermal socks size 42", "Runner doing winter Saint Nicholas 10k run in snow",
         {"component_class": "apparel_footwear", "use_scenario": "event_preparation", "use_timing": "during_training", "race_format": "race_or_event_preparation", "season": "cold", "shoe_size": 42, "max_price_uah": 1100, "locale": "uk"},
         "Expects thermal socks matching size 40-42."),
        (78, "Race prep: Post-race recovery drink/nutrition", "Runner wanting immediate post-finish line protein/carb boost",
         {"component_class": "protein_carbohydrate_food", "use_scenario": "event_preparation", "use_timing": "before_or_after_training", "race_format": "race_or_event_preparation", "max_price_uah": 1600, "locale": "ru"},
         "Expects post-race recovery food."),
        (79, "Race prep: 1800 UAH budget, open need", "Amateur runner with 1800 UAH looking for best race prep bundle",
         {"component_class": "any", "use_scenario": "event_preparation", "use_timing": "during_training", "race_format": "race_or_event_preparation", "max_price_uah": 1800, "locale": "uk"},
         "Tests open need ranking for race prep at 1800 UAH."),
        (80, "Race prep: Liquid caffeine energy shots", "Runner wanting fast caffeine kick for final 2km sprint",
         {"component_class": "protein_carbohydrate_food", "use_scenario": "event_preparation", "use_timing": "during_training", "race_format": "race_or_event_preparation", "product_form": "liquid", "max_price_uah": 1600, "locale": "ru"},
         "Tests liquid fast energy form.")
    ]
    for sc in scenarios_race_prep:
        add(*sc)

    # Group 5: Everyday Running, Regular Training & Boundary Cases (20 scenarios)
    # Covering daily running routines, seasonal training, budget boundaries, multi-choice
    scenarios_daily = [
        (81, "Daily jogger: Regular training socks size 41", "Morning jogger (5km 3x/week) needing fresh socks pack",
         {"component_class": "apparel_footwear", "use_scenario": "training", "use_timing": "during_training", "shoe_size": 41, "max_price_uah": 1000, "locale": "uk"},
         "Expects 5-pack running socks matching size 40-42."),
        (82, "Daily jogger: Dark socks size 44 for muddy autumn runs", "Jogger running in local park on dirt trails",
         {"component_class": "apparel_footwear", "use_scenario": "training", "use_timing": "during_training", "shoe_size": 44, "max_price_uah": 1000, "locale": "ru"},
         "Expects dark socks matching size 43-45."),
        (83, "Daily jogger: White socks size 36 for summer mornings", "Jogger wanting fresh white socks for summer",
         {"component_class": "apparel_footwear", "use_scenario": "training", "use_timing": "during_training", "season": "warm", "shoe_size": 36, "max_price_uah": 1000, "locale": "uk"},
         "Expects white socks size 35-37."),
        (84, "Daily runner: Everyday hydration tonus", "Active runner drinking electrolytes daily to maintain hydration",
         {"component_class": "hydration_items", "use_scenario": "everyday", "use_timing": "daily_use", "max_price_uah": 1500, "locale": "ru"},
         "Expects daily hydration sticks (e.g. Hydria Daily / Perform)."),
        (85, "Daily runner: Energy bars for pre-workout snack at office", "Office worker heading to running track at 6 PM, needing 4 PM snack",
         {"component_class": "protein_carbohydrate_food", "use_scenario": "training", "use_timing": "before_or_after_training", "product_form": "bars", "max_price_uah": 1500, "locale": "uk"},
         "Expects protein or energy bars."),
        (86, "Daily runner: Training accessories (running water bottle)", "Jogger needing handheld bottle for 10km tempo runs",
         {"component_class": "sports_accessories", "use_scenario": "training", "use_timing": "during_training", "max_price_uah": 1400, "locale": "ru"},
         "Expects accessories containing bottle or flask."),
        (87, "Daily runner: High budget training gear (2500 UAH)", "Dedicated amateur runner buying top gear for track season",
         {"component_class": "sports_accessories", "use_scenario": "training", "use_timing": "during_training", "max_price_uah": 2500, "locale": "uk"},
         "Expects premium running accessories."),
        (88, "Daily runner: Weekly runner pack (gels + bars + electrolytes)", "Runner looking for complete weekly running fuel pack",
         {"component_class": "protein_carbohydrate_food", "use_scenario": "training", "use_timing": "during_training", "max_price_uah": 1600, "locale": "ru"},
         "Expects Набір «Тиждень бігуна» (RE11659)."),
        (89, "Daily runner: Tight budget energy snack (650 UAH)", "Student jogger looking for cheap energy snack",
         {"component_class": "protein_carbohydrate_food", "use_scenario": "training", "use_timing": "during_training", "max_price_uah": 650, "locale": "uk"},
         "Tests floor anchor / near miss when budget is 650 UAH."),
        (90, "Daily runner: Tight budget socks (500 UAH)", "Jogger wanting socks under 500 UAH",
         {"component_class": "apparel_footwear", "use_scenario": "training", "use_timing": "during_training", "shoe_size": 42, "max_price_uah": 500, "locale": "ru"},
         "Tests floor anchor to 950 UAH socks when budget is 500 UAH."),
        (91, "Daily runner: Electrolyte sticks for daily workout", "Runner needing hydration sticks for daily 8km run",
         {"component_class": "hydration_items", "use_scenario": "training", "use_timing": "during_training", "product_form": "sticks", "max_price_uah": 1500, "locale": "uk"},
         "Expects electrolyte sticks for training."),
        (92, "Daily runner: Isotonic tub powder for home dispenser", "Runner mixing drinks in large pitcher for whole family",
         {"component_class": "hydration_items", "use_scenario": "everyday", "use_timing": "daily_use", "product_form": "powder", "max_price_uah": 1800, "locale": "ru"},
         "Tests product_form='powder' daily hydration."),
        (93, "Daily runner: Daily salt capsules", "Heavy sweater needing salt capsule daily supplement",
         {"component_class": "hydration_items", "use_scenario": "everyday", "use_timing": "daily_use", "product_form": "capsules", "max_price_uah": 1500, "locale": "uk"},
         "Tests product_form='capsules' daily hydration."),
        (94, "Daily runner: Winter training socks size 48 (hard-to-find)", "Runner with size 48 shoe wanting winter thermal socks",
         {"component_class": "apparel_footwear", "use_scenario": "training", "use_timing": "during_training", "season": "cold", "shoe_size": 48, "max_price_uah": 1200, "locale": "ru"},
         "Checks size 46-48 matching for size 48 runner."),
        (95, "Daily runner: Fall gear buff and accessories", "Autumn jogger needing buff and headwear",
         {"component_class": "sports_accessories", "use_scenario": "training", "use_timing": "during_training", "season": "cold", "max_price_uah": 1500, "locale": "uk"},
         "Expects cold weather accessories (buff)."),
        (96, "Daily runner: Multi-form [gel, bars] for Sunday long run", "Weekend warrior doing 22km every Sunday",
         {"component_class": "protein_carbohydrate_food", "use_scenario": "training", "use_timing": "during_training", "product_form": ["gel", "bars"], "max_price_uah": 1700, "locale": "ru"},
         "Expects combo nutrition set for long runs."),
        (97, "Daily runner: Recovery food after heavy tempo run", "Runner needing fast protein-carb recovery",
         {"component_class": "protein_carbohydrate_food", "use_scenario": "training", "use_timing": "before_or_after_training", "max_price_uah": 1600, "locale": "uk"},
         "Expects post-run recovery bars/food."),
        (98, "Daily runner: Open preference, 1500 UAH, training during", "Runner with 1500 UAH open to any running product for workouts",
         {"component_class": "any", "use_scenario": "training", "use_timing": "during_training", "max_price_uah": 1500, "locale": "ru"},
         "Evaluates ranking across diverse running sets at 1500 UAH."),
        (99, "Daily runner: Open preference, 2000 UAH, everyday use", "Runner wanting general everyday running support",
         {"component_class": "any", "use_scenario": "everyday", "use_timing": "daily_use", "max_price_uah": 2000, "locale": "uk"},
         "Evaluates everyday running recommendations."),
        (100, "Daily runner: Open preference, tight budget (700 UAH)", "Runner wanting any budget running product",
         {"component_class": "any", "use_scenario": "training", "use_timing": "during_training", "max_price_uah": 700, "locale": "ru"},
         "Tests general floor anchor behavior for open need at 700 UAH.")
    ]
    for sc in scenarios_daily:
        add(*sc)

    return scenarios

def evaluate_test_run(scenario, rec_response, catalog_lookup, exception_msg=None):
    """Evaluate single test execution against human/buyer logic criteria."""
    req = scenario["request"]
    expected = scenario["expected_focus"]

    eval_result = {
        "verdict": "PASS",
        "human_flaws": [],
        "criteria_checks": {
            "unrelated_gym_powerlifting_leak": "OK",
            "food_vs_gear_confusion": "OK",
            "gear_vs_food_confusion": "OK",
            "endurance_race_format_fit": "OK",
            "truthful_relevant_explanations": "OK",
            "budget_floor_nearmiss_clarity": "OK"
        },
        "notes": []
    }

    if exception_msg:
        # Schema or validation error
        if "product_form is not supported" in exception_msg:
            eval_result["verdict"] = "FAIL"
            flaw = f"Schema limitation: Endurance runners frequently use electrolyte capsules (e.g. SaltStick) and drink powders for mixing into soft flasks, but the quiz rejects product_form='{req.get('product_form')}' with DraftMatchError."
            eval_result["human_flaws"].append(flaw)
            eval_result["criteria_checks"]["endurance_race_format_fit"] = "FAIL: unsupported runner form"
            eval_result["notes"].append(flaw)
            return eval_result
        else:
            eval_result["verdict"] = "FAIL"
            eval_result["human_flaws"].append(f"Unexpected exception: {exception_msg}")
            return eval_result

    status = rec_response.get("status")
    results = rec_response.get("results", [])
    near_miss = rec_response.get("near_miss_results", [])
    floor_anchors = rec_response.get("floor_anchor_results", [])

    all_returned_candidates = results + near_miss + floor_anchors

    # Criterion 1: Unrelated gym / powerlifting / mass gainer / pure creatine leakage
    for c in all_returned_candidates:
        row = c.get("catalog_row")
        cat_rec = catalog_lookup.get(row, {})
        sku = c.get("sku") or cat_rec.get("sku")
        title = c.get("title", "")
        summary = c.get("expert_summary", "") or ""

        # Check pure creatine in marathon/running
        if sku == "RE11660":
            if req.get("race_format") in ["marathon", "ultra_or_long_distance"] or req.get("component_class") == "protein_carbohydrate_food" or req.get("component_class") == "any":
                # RE11660 contains 300g Creatine Monohydrate + 5 gels.
                # In distance running, creatine causes intracellular water retention (1-2kg body weight gain), which impairs running economy.
                # Even worse, draft_matcher expert_summary says: "Повышает взрывную силу и стимулирует качественный мышечный рост!"
                if "качественный мышечный рост" in summary or "силовых тренировок" in summary or "взрывную силу" in summary:
                    eval_result["criteria_checks"]["unrelated_gym_powerlifting_leak"] = "FAIL"
                    eval_result["criteria_checks"]["truthful_relevant_explanations"] = "FAIL"
                    flaw = "Gym/Powerlifting Leak & Bizarre Expert Pitch: Recommended «Набір Марафонець» (RE11660) which contains 300g Creatine Monohydrate (causes unwanted water weight gain for runners), and pitches it to a distance runner as 'комплекс для силовых тренировок: повышает взрывную силу и стимулирует качественный мышечный рост'!"
                    eval_result["human_flaws"].append(flaw)
                    eval_result["verdict"] = "FAIL"
                else:
                    eval_result["criteria_checks"]["unrelated_gym_powerlifting_leak"] = "WARN"
                    flaw = "Questionable Composition: Set contains 300g pure Creatine tub bundled with only 5 gels. Creatine water-weight gain is counterproductive for distance endurance."
                    eval_result["human_flaws"].append(flaw)
                    if eval_result["verdict"] == "PASS":
                        eval_result["verdict"] = "WARN"

        # Check heavy bodybuilding BCAA/EAA sets with shakers (RE11786, RE11811, RE11802)
        if sku in ["RE11786", "RE11811", "RE11802"]:
            if req.get("component_class") in ["hydration_items", "sports_accessories"]:
                eval_result["criteria_checks"]["unrelated_gym_powerlifting_leak"] = "WARN"
                flaw = f"Questionable Set: Recommends {title} ({sku}) which is dominated by a 360g–500g bodybuilding BCAA/EAA tub + shaker, masquerading as running hydration or running accessories because of a few sample sticks."
                eval_result["human_flaws"].append(flaw)
                if eval_result["verdict"] == "PASS":
                    eval_result["verdict"] = "WARN"

    # Criterion 2: Food / Gels / Bars requested vs returned
    req_class = req.get("component_class")
    req_forms = req.get("product_form")
    if req_class == "protein_carbohydrate_food" or req_forms in ["gel", "bars", ["gel", "bars"]]:
        if status in ["no_match", "no_exact_match"]:
            if not results and not floor_anchors and not near_miss:
                eval_result["criteria_checks"]["food_vs_gear_confusion"] = "FAIL"
                flaw = "Catalog Starvation / No Match: Runner requested running nutrition/food, but received 0 matches and 0 options because only 2 sets in catalog are tagged with protein_carbohydrate_food."
                eval_result["human_flaws"].append(flaw)
                eval_result["verdict"] = "FAIL"
        else:
            for c in results:
                row = c.get("catalog_row")
                cat_rec = catalog_lookup.get(row, {})
                c_title = c.get("title", "")
                c_classes = cat_rec.get("matching_evidence", {}).get("component_classes", []) or []

                # If runner asked for food/bars and got pure socks or bottle
                if "шкарпеток" in c_title.lower() or "носки" in c_title.lower():
                    eval_result["criteria_checks"]["food_vs_gear_confusion"] = "FAIL"
                    flaw = f"Category Confusion: Runner specifically requested sports nutrition/food, but received socks ({c_title})!"
                    eval_result["human_flaws"].append(flaw)
                    eval_result["verdict"] = "FAIL"
                elif c.get("sku") in ["RE11013", "RE11020"] and req_forms == "bars":
                    # RE11013 has NO bars in reality (card says 'в перечне только 3 позиции: носки x2, бутылка')
                    if c.get("sku") == "RE11013":
                        eval_result["criteria_checks"]["food_vs_gear_confusion"] = "WARN"
                        flaw = f"False Product Form Match: Recommends «Бігова пара» (RE11013) for bars, but the actual set only contains socks and a glass bottle; bars were merely mentioned in introductory marketing text."
                        eval_result["human_flaws"].append(flaw)
                        if eval_result["verdict"] == "PASS":
                            eval_result["verdict"] = "WARN"

    # Criterion 3: Apparel / Socks requested vs returned
    if req_class == "apparel_footwear":
        for c in results:
            row = c.get("catalog_row")
            cat_rec = catalog_lookup.get(row, {})
            c_classes = cat_rec.get("matching_evidence", {}).get("component_classes", []) or []
            if "apparel_footwear" not in c_classes:
                eval_result["criteria_checks"]["gear_vs_food_confusion"] = "FAIL"
                flaw = f"Category Confusion: Runner asked for apparel/footwear, but received non-apparel set {c.get('title')}."
                eval_result["human_flaws"].append(flaw)
                eval_result["verdict"] = "FAIL"

    # Criterion 4: Race format alignment (Marathon, Half-Marathon, Ultra)
    req_format = req.get("race_format")
    if req_format == "half_marathon":
        # Check if quiz returned no_exact_match due to catalog zero-tagging
        if status in ["no_exact_match", "no_match"] and len(results) == 0:
            eval_result["criteria_checks"]["endurance_race_format_fit"] = "FAIL"
            flaw = "Zero Coverage for Half-Marathon: The quiz returned 0 exact matches for 'half_marathon' because NOT A SINGLE SET in the entire 206-record catalog has 'half_marathon' in its matching_evidence.race_formats, despite half-marathon being the #1 most popular race distance in Ukraine and explicitly mentioned in product titles/descriptions (e.g. Набір «Марафонець»)."
            eval_result["human_flaws"].append(flaw)
            eval_result["verdict"] = "FAIL"

    if req_format == "marathon":
        if status == "matched":
            has_marathon_set = any(
                ("marathon" in (catalog_lookup.get(c.get("catalog_row"), {}).get("matching_evidence", {}).get("race_formats", []) or []) or "марафон" in c.get("title", "").lower())
                for c in results
            )
            if not has_marathon_set:
                eval_result["criteria_checks"]["endurance_race_format_fit"] = "WARN"
                flaw = "Weak Marathon Fit: None of the recommended sets have explicit marathon endurance positioning."
                eval_result["human_flaws"].append(flaw)
                if eval_result["verdict"] == "PASS":
                    eval_result["verdict"] = "WARN"

    # Criterion 5: Truthful & Relevant Explanations ("why_suitable", "expert_summary")
    for c in all_returned_candidates:
        why = c.get("why_suitable", []) or []
        for line in why:
            # Check false "без посторонних позиций" claim
            if "без посторонних позиций" in line or "без сторонніх речей" in line:
                if c.get("sku") == "RE11660" and req_class == "protein_carbohydrate_food":
                    eval_result["criteria_checks"]["truthful_relevant_explanations"] = "WARN"
                    flaw = "False Claim in Explanation: «why_suitable» states 'в наборе именно Спортивное питание и батончики (без посторонних позиций)', but the set prominently includes a 300g Creatine Monohydrate powerlifting tub."
                    eval_result["human_flaws"].append(flaw)
                    if eval_result["verdict"] == "PASS":
                        eval_result["verdict"] = "WARN"
                elif c.get("sku") == "RE11786" and req_class == "sports_accessories":
                    eval_result["criteria_checks"]["truthful_relevant_explanations"] = "WARN"
                    flaw = f"False Claim in Explanation: «why_suitable» states 'в наборе именно Спортивные аксессуары (без посторонних позиций)', but set RE11786 actually bundles a 3-month gym club membership, 360g BCAA, and hydration sticks."
                    eval_result["human_flaws"].append(flaw)
                    if eval_result["verdict"] == "PASS":
                        eval_result["verdict"] = "WARN"
                elif c.get("sku") == "RE11020" and req_class == "sports_accessories":
                    eval_result["criteria_checks"]["truthful_relevant_explanations"] = "WARN"
                    flaw = f"False Claim in Explanation: «why_suitable» states 'в наборе именно Спортивные аксессуары (без посторонних позиций)', but set RE11020 also contains 2 pairs of socks and 4 protein bars."
                    eval_result["human_flaws"].append(flaw)
                    if eval_result["verdict"] == "PASS":
                        eval_result["verdict"] = "WARN"

    # Criterion 6: Budget logic & Near-Miss / Floor-Anchor helpfulness
    max_price = req.get("max_price_uah")
    if max_price is not None and max_price < 950:
        if status == "floor_anchor":
            eval_result["criteria_checks"]["budget_floor_nearmiss_clarity"] = "OK"
            fa_prices = [fa.get("price_uah") for fa in floor_anchors]
            if not fa_prices:
                eval_result["criteria_checks"]["budget_floor_nearmiss_clarity"] = "WARN"
                eval_result["human_flaws"].append(f"Floor anchor status indicated but 0 floor anchor sets returned for budget {max_price} UAH.")
                if eval_result["verdict"] == "PASS":
                    eval_result["verdict"] = "WARN"
        elif status == "matched":
            for c in results:
                if c.get("price_uah", 0) > max_price:
                    eval_result["criteria_checks"]["budget_floor_nearmiss_clarity"] = "FAIL"
                    flaw = f"Budget Breach: Returned set {c.get('title')} priced at {c.get('price_uah')} UAH which strictly exceeds max budget {max_price} UAH in matched status."
                    eval_result["human_flaws"].append(flaw)
                    eval_result["verdict"] = "FAIL"

    return eval_result

def main():
    print("Loading catalog and attaching audit evidence...")
    catalog = load_environment()
    catalog_lookup = {r["catalog_row"]: r for r in catalog}
    scenarios = generate_100_scenarios()
    print(f"Generated {len(scenarios)} running test scenarios.")

    results_data = []
    summary_counts = {"PASS": 0, "WARN": 0, "FAIL": 0}

    for sc in scenarios:
        t_id = sc["test_id"]
        req = sc["request"]
        print(f"Executing Test #{t_id:03d}: {sc['name']}...", end=" ")

        exc_str = None
        resp = None
        try:
            resp = draft_recommend(catalog, req)
        except DraftMatchError as e:
            exc_str = str(e)
        except Exception as e:
            exc_str = f"Unexpected {type(e).__name__}: {str(e)}"

        evaluation = evaluate_test_run(sc, resp or {}, catalog_lookup, exc_str)
        verdict = evaluation["verdict"]
        summary_counts[verdict] += 1
        print(f"[{verdict}] ({len(evaluation['human_flaws'])} flaws)")

        # Save test detail
        test_entry = {
            "test_id": t_id,
            "name": sc["name"],
            "persona": sc["persona"],
            "request": req,
            "expected_focus": sc["expected_focus"],
            "execution": {
                "status": resp.get("status") if resp else "EXCEPTION",
                "message": resp.get("message") if resp else None,
                "exception": exc_str,
                "results_count": len(resp.get("results", [])) if resp else 0,
                "near_miss_count": len(resp.get("near_miss_results", [])) if resp else 0,
                "floor_anchor_count": len(resp.get("floor_anchor_results", [])) if resp else 0,
                "results": [
                    {
                        "set_id": r.get("set_id"),
                        "sku": r.get("sku"),
                        "title": r.get("title"),
                        "price_uah": r.get("price_uah"),
                        "expert_summary": r.get("expert_summary"),
                        "why_suitable": r.get("why_suitable"),
                        "why_not_suitable": r.get("why_not_suitable")
                    } for r in (resp.get("results", []) if resp else [])
                ],
                "floor_anchor_results": [
                    {
                        "set_id": r.get("set_id"),
                        "sku": r.get("sku"),
                        "title": r.get("title"),
                        "price_uah": r.get("price_uah"),
                        "expert_summary": r.get("expert_summary")
                    } for r in (resp.get("floor_anchor_results", []) if resp else [])
                ],
                "near_miss_results": [
                    {
                        "set_id": r.get("set_id"),
                        "sku": r.get("sku"),
                        "title": r.get("title"),
                        "price_uah": r.get("price_uah")
                    } for r in (resp.get("near_miss_results", []) if resp else [])
                ]
            },
            "evaluation": evaluation
        }
        results_data.append(test_entry)

    # Save full JSON
    OUTPUT_JSON.write_text(json.dumps(results_data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nFull test data saved to {OUTPUT_JSON}")

    # Build and save Markdown Report
    build_markdown_report(results_data, summary_counts)
    print(f"Markdown report saved to {OUTPUT_REPORT}")
    print(f"\nFinal Summary: PASS={summary_counts['PASS']} | WARN={summary_counts['WARN']} | FAIL={summary_counts['FAIL']}")

def build_markdown_report(results_data, summary_counts):
    total = len(results_data)
    fails = [r for r in results_data if r["evaluation"]["verdict"] == "FAIL"]
    warns = [r for r in results_data if r["evaluation"]["verdict"] == "WARN"]
    passes = [r for r in results_data if r["evaluation"]["verdict"] == "PASS"]

    # Categorize flaws
    flaw_categories = {
        "half_marathon_zero_coverage": [],
        "creatine_gym_leakage": [],
        "unsupported_forms_capsules_powder": [],
        "food_starvation_or_sock_confusion": [],
        "misleading_explanations": []
    }

    for r in results_data:
        for f in r["evaluation"]["human_flaws"]:
            if "half_marathon" in f.lower() or "half-marathon" in f.lower():
                flaw_categories["half_marathon_zero_coverage"].append((r["test_id"], r["name"], f))
            elif "creatine" in f.lower() or "powerlifting" in f.lower() or "мышечный рост" in f.lower():
                flaw_categories["creatine_gym_leakage"].append((r["test_id"], r["name"], f))
            elif "capsules" in f.lower() or "powder" in f.lower() or "product_form is not supported" in f.lower():
                flaw_categories["unsupported_forms_capsules_powder"].append((r["test_id"], r["name"], f))
            elif "starvation" in f.lower() or "socks" in f.lower() or "category confusion" in f.lower():
                flaw_categories["food_starvation_or_sock_confusion"].append((r["test_id"], r["name"], f))
            elif "false claim" in f.lower() or "why_suitable" in f.lower():
                flaw_categories["misleading_explanations"].append((r["test_id"], r["name"], f))

    md = []
    md.append("# QA Agent 2: Running & Endurance Specialist - 100 Buyer Test Case Audit Report\n")
    md.append(f"**Date:** 2026-11-12  \n**Scope:** Race Expert Quiz — Running & Race Preparation (`goal_group: 'running'`)  \n**Catalog Source:** `wiki/projects/quiz-set-audit.json` (206 sets total, 41 candidate running sets)  \n**Matcher:** `test-quiz-sandbox/draft_matcher.py:draft_recommend`\n")

    md.append("## Executive Summary\n")
    md.append(f"| Metric | Count | Percentage |\n|---|---|---|\n| **Total Scenarios** | **{total}** | **100%** |\n| **PASS (Sound Buyer Experience)** | **{summary_counts['PASS']}** | **{summary_counts['PASS']*100//total}%** |\n| **WARN (Suboptimal / Borderline / Minor Inaccuracy)** | **{summary_counts['WARN']}** | **{summary_counts['WARN']*100//total}%** |\n| **FAIL (Critical Human Logic / Catalog Breakdown)** | **{summary_counts['FAIL']}** | **{summary_counts['FAIL']*100//total}%** |\n")

    md.append("```\n")
    md.append(f"Verdict Distribution: [{'#' * (summary_counts['PASS']//2)}{'-' * (summary_counts['WARN']//2)}{'!' * (summary_counts['FAIL']//2)}]\n")
    md.append(f"  PASS: {summary_counts['PASS']} | WARN: {summary_counts['WARN']} | FAIL: {summary_counts['FAIL']}\n")
    md.append("```\n")

    md.append("## Critical Architectural & Human-Logic Findings\n")

    md.append("### 1. The Half-Marathon Blindspot (CRITICAL FAIL - 20 Scenarios Affected)\n")
    md.append("> [!CAUTION]\n> In Ukraine, the half-marathon (21.1 km) is by far the most popular mass participation race distance (Kyiv Half Marathon, Nova Poshta series, etc.).  \n> However, **ZERO sets out of 206** in `quiz-set-audit.json` have `half_marathon` tagged in `matching_evidence.race_formats`!  \n> When a buyer chooses `race_format: 'half_marathon'`, the draft matcher returns **`status: no_exact_match` (0 sets)**, even though sets like «Марафонець» (RE11660) explicitly state *'полумарафон и марафон'* in their descriptions. This causes an immediate failure for 100% of half-marathon runner queries unless relaxed fallback is manually triggered.\n")

    md.append("### 2. Gym / Powerlifting Leakage into Marathon Preparation (CRITICAL FAIL/WARN)\n")
    md.append("> [!WARNING]\n> **Creatine Tub for a Marathoner:** Set `RE11660` (Набір «Марафонець», 1500 UAH) bundles a **300g tub of pure Creatine Monohydrate** with only 5 energy gels. In endurance running physiology, creatine causes intracellular water retention leading to a 1–2 kg body weight penalty, which increases energy cost of running without aerobic benefit.  \n> **Bizarre Marketing Pitch:** When recommended to a marathon runner, `draft_matcher` generates the following expert explanation:  \n> *«Мощный комплекс для силовых тренировок: повышает взрывную силу, пиковую работоспособность и стимулирует качественный мышечный рост.»*  \n> Recommending powerlifting explosive strength and bodybuilding muscle hypertrophy to an aerobic endurance runner preparing for 42.2 km destroys coach credibility.\n")

    md.append("### 3. Severe Nutrition Catalog Starvation (CRITICAL FAIL/WARN)\n")
    md.append("> [!IMPORTANT]\n> Out of 41 running candidate sets in the catalog:\n> - **23 sets are purely socks** (Акційний набір шкарпеток 5 пар / 1+1=3).\n> - **Only TWO sets** in the entire catalog have `component_classes: ['protein_carbohydrate_food']`: `RE11659` (Набір «Тиждень бігуна») and `RE11660` (Набір «Марафонець» with Creatine).\n> - `UT-PRO-2026` (Ultra Trail Marathon Pro) contains 3x SIS Beta Fuel gels and a protein bar, but its audit entry **omits `protein_carbohydrate_food`** and only lists `hydration_items`!\n> - Consequently, when runners search for energy bars or race food with specific constraints, the catalog immediately starves out.\n")

    md.append("### 4. Schema Rejection of Running Salt Capsules & Drink Powders (CRITICAL FAIL)\n")
    md.append("> [!NOTE]\n> `draft_matcher.py` defines `PRODUCT_FORMS_BY_GOAL['running'] = {'bars', 'gel', 'food_or_meal', 'liquid', 'sticks'}`.  \n> It completely excludes `'capsules'` and `'powder'`.  \n> In real running, **salt capsules** (e.g. Precision Hydration, SaltStick) and **isotonic powders** in canisters/tubs are essential endurance staples. When a runner selects capsules or powder, `draft_recommend` crashes with `DraftMatchError: product_form is not supported for the selected need`.\n")

    md.append("### 5. False 'No Foreign Items' Guarantees in `why_suitable`\n")
    md.append("> The explanation generator frequently outputs:  \n> *«Категория товаров: в наборе именно Спортивное питание и батончики (без посторонних позиций).»*  \n> Yet for `RE11660`, 70% of the set's physical mass and cost is a 300g bodybuilding creatine tub. Similarly, for sets labeled accessories, 3-month club subscriptions or 360g BCAA tubs are bundled.\n")

    md.append("## Detailed Breakdown of Test Categories\n")

    # Table of Scenarios
    md.append("### Test Scenario Log (100 Cases)\n")
    md.append("| # | Scenario Name | Budget | Class | Race Format | Form | Verdict | Main Flaw / Human Note |\n|---|---|---|---|---|---|---|---|\n")

    for r in results_data:
        req = r["request"]
        flaw_short = r["evaluation"]["human_flaws"][0] if r["evaluation"]["human_flaws"] else "Clean match & sound explanation"
        if len(flaw_short) > 75:
            flaw_short = flaw_short[:72] + "…"
        md.append(f"| {r['test_id']:03d} | {r['name'][:30]} | {req.get('max_price_uah', 'any')} ₴ | {req.get('component_class', 'any')} | {req.get('race_format', '-')} | {str(req.get('product_form', '-'))} | **{r['evaluation']['verdict']}** | {flaw_short} |\n")

    md.append("\n## Concrete Actionable Recommendations for Engineering & Nutrition Curators\n")
    md.append("1. **Fix Half-Marathon Tagging Immediately:** In `wiki/projects/quiz-set-audit.json`, add `'half_marathon'` to `matching_evidence.race_formats` for sets `RE11660` (Набір «Марафонець»), `RE11804` (Набір «Марафонський темп»), `RE11659` (Набір «Тиждень бігуна»), and all sock multipacks. This will immediately resolve 20 failing customer scenarios.\n")
    md.append("2. **Fix `PRODUCT_FORMS_BY_GOAL['running']`:** Add `'capsules'` (for salt/electrolyte capsules like RE11650) and `'powder'` (for electrolyte & isotonic mix powders) to allowed running product forms.\n")
    md.append("3. **Disqualify Pure Bodybuilding Creatine from Running/Marathon:** Remove `running_race_preparation` from `RE11660`'s matching evidence or replace the 300g Creatine component with an isotonic mix or hydration sticks. No marathon coach recommends a 300g tub of creatine for 42.2 km race prep.\n")
    md.append("4. **Correct UT-PRO-2026 Audit Metadata:** Add `'protein_carbohydrate_food'` to `component_classes` of set `UT-PRO-2026` since it contains 3 SIS Beta Fuel high-carb gels and a protein bar.\n")
    md.append("5. **Fix Expert Summary Logic for Running:** When goal is `running`, ensure `expert_summary` never describes products as *'комплекс для силовых тренировок и стимуляции мышечного роста'*, even if the set happens to contain amino acids or creatine.\n")

    OUTPUT_REPORT.write_text("".join(md), encoding="utf-8")

if __name__ == "__main__":
    main()
