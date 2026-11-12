# -*- coding: utf-8 -*-
"""QA Agent 6 - Gear & Apparel Specialist: 100 Realistic Buyer Test Scenarios & Evaluation."""

import json
import os
import sys
from pathlib import Path

# Add sandbox to sys.path
SANDBOX_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SANDBOX_DIR.parent
sys.path.insert(0, str(SANDBOX_DIR))

from draft_matcher import attach_audit_evidence, draft_recommend, DraftMatchError, _size_ranges, _season_groups

CATALOG_PATH = SANDBOX_DIR / "catalog.json"
AUDIT_PATH = PROJECT_ROOT / "wiki" / "projects" / "quiz-set-audit.json"
OUTPUT_JSON = SANDBOX_DIR / "agent_6_gear_100_tests.json"
OUTPUT_REPORT = SANDBOX_DIR / "agent_6_report.md"

def load_environment():
    cat = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    audit = json.loads(AUDIT_PATH.read_text(encoding="utf-8"))
    catalog = attach_audit_evidence(cat, audit)
    return catalog

def generate_100_scenarios():
    """Build 100 distinct, diverse, realistic buyer scenarios for Gear & Accessories."""
    scenarios = []

    def add(tid, name, persona, request_params, expected):
        scenarios.append({
            "test_id": tid,
            "name": name,
            "persona": persona,
            "request": {"goal_group": "gear", **request_params},
            "expected_focus": expected
        })

    # =========================================================================
    # PART 1: PURE RUNNING APPAREL & SOCKS (25 Scenarios: 1 - 25)
    # Testing sizes, seasons, budgets for running apparel/socks
    # =========================================================================
    # Small size 36–38
    add(1, "Runner: Small size socks (37), entry budget", "Female 10k runner with shoe size 37 on tight budget",
        {"component_class": "apparel_footwear", "activity": "running", "shoe_size": 37, "max_price_uah": 600, "locale": "uk"},
        "Expects size 35-37 socks; tests budget near-miss/floor anchor since socks cost 950 UAH.")
    add(2, "Runner: Small size socks (37), regular budget", "Female runner looking for 5-pack white socks size 37",
        {"component_class": "apparel_footwear", "activity": "running", "shoe_size": 37, "max_price_uah": 1000, "locale": "uk"},
        "Expects exact match: White socks 5 pairs size 35–37 (950 UAH).")
    add(3, "Runner: Small size socks (36), dark color, regular budget", "Runner needing dark training socks size 36",
        {"component_class": "apparel_footwear", "activity": "running", "shoe_size": 36, "max_price_uah": 1100, "locale": "ru"},
        "Expects dark socks 5 pairs size 35–37 (950 UAH).")
    add(4, "Runner: Small size winter thermal socks (37), cold season", "Winter runner needing warm thermo socks size 37",
        {"component_class": "apparel_footwear", "activity": "running", "shoe_size": 37, "season": "cold", "max_price_uah": 1200, "locale": "uk"},
        "Expects thermo socks 1+1=3 size 35–37 (1058 UAH).")

    # Medium size 39–41
    add(5, "Runner: Medium size socks (39), entry budget", "Amateur runner size 39 with 700 UAH budget",
        {"component_class": "apparel_footwear", "activity": "running", "shoe_size": 39, "max_price_uah": 700, "locale": "ru"},
        "Expects near miss or floor anchor for size 38–40 socks.")
    add(6, "Runner: Medium size socks (40), white, regular budget", "Road runner size 40 needing 5-pack white socks",
        {"component_class": "apparel_footwear", "activity": "running", "shoe_size": 40, "max_price_uah": 1000, "locale": "uk"},
        "Expects white socks 5 pairs size 38–40 or 40–42 (950 UAH).")
    add(7, "Runner: Medium size socks (41), dark, regular budget", "Evening runner size 41 needing dark socks",
        {"component_class": "apparel_footwear", "activity": "running", "shoe_size": 41, "max_price_uah": 1000, "locale": "ru"},
        "Expects dark socks 5 pairs size 40–42 (950 UAH).")
    add(8, "Runner: Medium size winter thermal socks (40), cold season", "Trail runner preparing for winter training size 40",
        {"component_class": "apparel_footwear", "activity": "running", "shoe_size": 40, "season": "cold", "max_price_uah": 1200, "locale": "uk"},
        "Expects thermo socks 1+1=3 size 40–42 (1058 UAH).")
    add(9, "Runner: Medium size winter thermal socks (39), cold season", "Cross-country runner size 39 in sub-zero temps",
        {"component_class": "apparel_footwear", "activity": "running", "shoe_size": 39, "season": "cold", "max_price_uah": 1200, "locale": "ru"},
        "Expects thermo socks 1+1=3 size 38–40 (1058 UAH).")

    # Large size 42–44
    add(10, "Runner: Large size socks (43), entry budget", "Marathoner size 43 looking for budget socks under 800 UAH",
        {"component_class": "apparel_footwear", "activity": "running", "shoe_size": 43, "max_price_uah": 800, "locale": "uk"},
        "Expects near miss or floor anchor for size 43–45 socks.")
    add(11, "Runner: Large size socks (43), white, regular budget", "Marathoner size 43 buying white training socks",
        {"component_class": "apparel_footwear", "activity": "running", "shoe_size": 43, "max_price_uah": 1000, "locale": "uk"},
        "Expects exact match: White socks 5 pairs size 43–45 (950 UAH).")
    add(12, "Runner: Large size socks (44), dark, regular budget", "Club runner size 44 needing dark socks 5-pack",
        {"component_class": "apparel_footwear", "activity": "running", "shoe_size": 44, "max_price_uah": 1000, "locale": "ru"},
        "Expects dark socks 5 pairs size 43–45 (950 UAH).")
    add(13, "Runner: Large size winter thermal socks (43), cold season", "Winter runner size 43 needing thermal insulation",
        {"component_class": "apparel_footwear", "activity": "running", "shoe_size": 43, "season": "cold", "max_price_uah": 1200, "locale": "uk"},
        "Expects thermo socks 1+1=3 size 43–45 (1058 UAH).")
    add(14, "Runner: Large size socks (42), warm season", "Summer runner size 42 looking for light summer socks",
        {"component_class": "apparel_footwear", "activity": "running", "shoe_size": 42, "season": "warm", "max_price_uah": 1200, "locale": "ru"},
        "Tests warm season filtering on running socks; verify if gym sets leak in.")

    # Extra Large size 45–47
    add(15, "Runner: XL size socks (46), entry budget", "Tall runner size 46 on tight budget 750 UAH",
        {"component_class": "apparel_footwear", "activity": "running", "shoe_size": 46, "max_price_uah": 750, "locale": "uk"},
        "Expects near-miss for size 46–48 socks.")
    add(16, "Runner: XL size socks (46), dark, regular budget", "Heavy runner size 46 needing 5-pack dark socks",
        {"component_class": "apparel_footwear", "activity": "running", "shoe_size": 46, "max_price_uah": 1000, "locale": "uk"},
        "Expects dark socks 5 pairs size 46–48 (950 UAH).")
    add(17, "Runner: XL size socks (47), white, regular budget", "Tall marathoner size 47 needing white socks",
        {"component_class": "apparel_footwear", "activity": "running", "shoe_size": 47, "max_price_uah": 1000, "locale": "ru"},
        "Expects white socks 5 pairs size 46–48 (950 UAH).")
    add(18, "Runner: XL size winter thermal socks (46), cold season", "Winter ultramarathoner size 46 needing thermal socks",
        {"component_class": "apparel_footwear", "activity": "running", "shoe_size": 46, "season": "cold", "max_price_uah": 1200, "locale": "uk"},
        "Tests cold season thermal socks for size 46; check if thermo sets stop at 45.")

    # Unspecified size ("any") & Scenarios
    add(19, "Runner: Unspecified size socks, training scenario", "Runner not specifying shoe size, looking for training socks",
        {"component_class": "apparel_footwear", "activity": "running", "shoe_size": "any", "use_scenario": "training", "max_price_uah": 1000, "locale": "uk"},
        "Tests size-unspecified behavior; verify whether size 46–48 is blindly forced.")
    add(20, "Runner: Unspecified size socks, event prep scenario", "Race participant needing competition socks",
        {"component_class": "apparel_footwear", "activity": "running", "shoe_size": "any", "use_scenario": "event_preparation", "max_price_uah": 1100, "locale": "ru"},
        "Tests event prep socks matching without size.")
    add(21, "Runner: Unspecified size socks, everyday scenario", "Runner wearing sports socks daily",
        {"component_class": "apparel_footwear", "activity": "running", "shoe_size": "any", "use_scenario": "everyday", "max_price_uah": 1000, "locale": "uk"},
        "Tests everyday running sock matching.")
    add(22, "Runner: Premium budget socks bundle (1500 UAH), size 43", "Runner ready to spend 1500 UAH on premium sock kit",
        {"component_class": "apparel_footwear", "activity": "running", "shoe_size": 43, "max_price_uah": 1500, "locale": "uk"},
        "Tests premium budget: does it return race-expert-081 or club subscription sets?")
    add(23, "Runner: Premium budget socks bundle (1500 UAH), size 40", "Runner ready to spend 1500 UAH, size 40",
        {"component_class": "apparel_footwear", "activity": "running", "shoe_size": 40, "max_price_uah": 1500, "locale": "ru"},
        "Check premium set composition for size 40.")
    add(24, "Runner: High budget (2000 UAH), cold season thermo socks size 44", "Cold-weather runner with flexible budget 2000 UAH",
        {"component_class": "apparel_footwear", "activity": "running", "shoe_size": 44, "season": "cold", "max_price_uah": 2000, "locale": "uk"},
        "Expects thermo socks size 43-45 (1058 UAH) without irrelevant overpriced items.")
    add(25, "Runner: High budget (2500 UAH), warm season socks size 41", "Summer runner with high budget 2500 UAH",
        {"component_class": "apparel_footwear", "activity": "running", "shoe_size": 41, "season": "warm", "max_price_uah": 2500, "locale": "ru"},
        "Tests high budget summer apparel matching.")

    # =========================================================================
    # PART 2: SPORTS ACCESSORIES - RUNNING & OUTDOOR (25 Scenarios: 26 - 50)
    # Testing belts, flasks, bottles, speed laces, caps, race accessories
    # =========================================================================
    add(26, "Runner: Race accessories (bib belt, bottle, flask), budget 1500 UAH", "Marathoner looking for bib belt and flask for race day",
        {"component_class": "sports_accessories", "activity": "running", "use_scenario": "event_preparation", "max_price_uah": 1500, "locale": "uk"},
        "Expects race prep accessories (race-expert-055, 056, or 115) without creatine or memberships.")
    add(27, "Runner: Race bib belt & cap, Russian locale", "Half-marathon runner needing bib belt and running cap",
        {"component_class": "sports_accessories", "activity": "running", "use_scenario": "event_preparation", "max_price_uah": 1500, "locale": "ru"},
        "Expects marathon race accessories with clean Russian explanations.")
    add(28, "Runner: Running gear with bottle & speed laces (1300 UAH)", "Road runner wanting water bottle and speed laces",
        {"component_class": "sports_accessories", "activity": "running", "use_scenario": "training", "max_price_uah": 1300, "locale": "uk"},
        "Tests match for race-expert-197 (1209 UAH: bottle + speed laces + socks + bars).")
    add(29, "Runner: Accessories, tight budget 800 UAH", "Student runner needing cheap bib belt / bottle under 800 UAH",
        {"component_class": "sports_accessories", "activity": "running", "max_price_uah": 800, "locale": "uk"},
        "Tests accessory catalog starvation at <1000 UAH; check floor anchor vs near miss.")
    add(30, "Runner: Accessories, entry budget 600 UAH", "Budget runner looking for basic running accessory under 600 UAH",
        {"component_class": "sports_accessories", "activity": "running", "max_price_uah": 600, "locale": "ru"},
        "Tests budget lower bound for sports accessories.")
    add(31, "Runner: Accessories, 1000 UAH budget", "Runner with 1000 UAH wanting sports accessories",
        {"component_class": "sports_accessories", "activity": "running", "max_price_uah": 1000, "locale": "uk"},
        "Critical test: does engine push race-expert-068 (creatine + socks + club membership) as near-miss?")
    add(32, "Runner: Accessories, 1200 UAH budget", "Runner wanting training accessories up to 1200 UAH",
        {"component_class": "sports_accessories", "activity": "running", "use_scenario": "training", "max_price_uah": 1200, "locale": "ru"},
        "Check whether gym sets (race-expert-068, 040) beat genuine running gear.")
    add(33, "Runner: Warm season accessories (bottle, cap)", "Summer runner needing hydration bottle and sun protection cap",
        {"component_class": "sports_accessories", "activity": "running", "season": "warm", "max_price_uah": 1500, "locale": "uk"},
        "Expects race-expert-115 (Підготовка до забігу: cap + bottle + bib belt).")
    add(34, "Runner: Cold season accessories", "Winter runner needing accessories for cold weather training",
        {"component_class": "sports_accessories", "activity": "running", "season": "cold", "max_price_uah": 1500, "locale": "ru"},
        "Check what accessories match cold season.")
    add(35, "Runner: Everyday running accessories", "Commuter runner wanting everyday running accessories",
        {"component_class": "sports_accessories", "activity": "running", "use_scenario": "everyday", "max_price_uah": 1500, "locale": "uk"},
        "Tests everyday accessory matching.")
    add(36, "Runner: Race prep accessories, premium budget 2000 UAH", "Triathlete with high budget preparing for marathon event",
        {"component_class": "sports_accessories", "activity": "running", "use_scenario": "event_preparation", "max_price_uah": 2000, "locale": "uk"},
        "Expects top race kit; verify if club memberships or creatine dominate.")
    add(37, "Runner: Accessories with shoe size 43 specified", "Runner buying accessories who also enters shoe size 43",
        {"component_class": "sports_accessories", "activity": "running", "shoe_size": 43, "max_price_uah": 1500, "locale": "uk"},
        "Tests accessory set with bundled socks: does bundled sock size match size 43?")
    add(38, "Runner: Accessories with shoe size 37 specified", "Female runner buying accessories who enters shoe size 37",
        {"component_class": "sports_accessories", "activity": "running", "shoe_size": 37, "max_price_uah": 1500, "locale": "ru"},
        "Critical sizing test: sets 056/115/210 bundle socks size 40–42! Will size 37 buyer be rejected or sent size 40–42?")
    add(39, "Runner: Accessories with shoe size 46 specified", "Runner size 46 asking for race accessories",
        {"component_class": "sports_accessories", "activity": "running", "shoe_size": 46, "max_price_uah": 1500, "locale": "uk"},
        "Critical sizing test: bundled socks in race kits are 40–42 or 43–45. Does it reject or mismatch size 46?")
    add(40, "Runner: Accessories without club membership", "Runner who strictly wants accessories, not gym memberships",
        {"component_class": "sports_accessories", "activity": "running", "membership": "no", "max_price_uah": 1500, "locale": "uk"},
        "Tests membership='no' filtering: does it successfully filter out club subscription kits?")
    add(41, "Hiker: Trekking accessories (1500 UAH)", "Hiker needing outdoor accessories for trail expedition",
        {"component_class": "sports_accessories", "activity": "hiking", "use_scenario": "training", "max_price_uah": 1500, "locale": "uk"},
        "Expects outdoor/hiking accessories.")
    add(42, "Hiker: Outdoor accessories, cold season", "Winter hiker needing outdoor gear for Carpathians",
        {"component_class": "sports_accessories", "activity": "hiking", "season": "cold", "max_price_uah": 1500, "locale": "ru"},
        "Expects winter trail gear without gym creatine.")
    add(43, "Hiker: Outdoor accessories, budget 1000 UAH", "Budget hiker looking for accessories under 1000 UAH",
        {"component_class": "sports_accessories", "activity": "hiking", "max_price_uah": 1000, "locale": "uk"},
        "Tests hiking accessory availability under 1000 UAH.")
    add(44, "Hiker: Outdoor accessories, event prep (trail race)", "Trail runner / hiker preparing for 50k mountain race",
        {"component_class": "sports_accessories", "activity": "hiking", "use_scenario": "event_preparation", "max_price_uah": 1600, "locale": "ru"},
        "Expects trail race preparation accessories.")
    add(45, "Cyclist: Cycling accessories (1500 UAH)", "Gravel cyclist looking for riding accessories and bottles",
        {"component_class": "sports_accessories", "activity": "cycling", "use_scenario": "training", "max_price_uah": 1500, "locale": "uk"},
        "Tests cycling accessory recommendations.")
    add(46, "Cyclist: Cycling accessories, warm season", "Road cyclist training in hot summer weather needing accessories",
        {"component_class": "sports_accessories", "activity": "cycling", "season": "warm", "max_price_uah": 1500, "locale": "ru"},
        "Check if summer cycling accessories exist or if gym kits match.")
    add(47, "Cyclist: Cycling accessories, entry budget 700 UAH", "City cyclist on budget looking for bike gear",
        {"component_class": "sports_accessories", "activity": "cycling", "max_price_uah": 700, "locale": "uk"},
        "Tests cycling accessory lower budget bound.")
    add(48, "Walker: Walking accessories for daily fitness", "Daily 10,000 steps walker looking for comfort accessories",
        {"component_class": "sports_accessories", "activity": "walking", "use_scenario": "everyday", "max_price_uah": 1500, "locale": "ru"},
        "Check walking accessory matching.")
    add(49, "Walker: Walking accessories, budget 1000 UAH", "Elderly walker looking for walking accessories up to 1000 UAH",
        {"component_class": "sports_accessories", "activity": "walking", "max_price_uah": 1000, "locale": "uk"},
        "Check walking accessory matching at 1000 UAH.")
    add(50, "Walker: Walking accessories, cold season", "Nordic walker walking in freezing weather",
        {"component_class": "sports_accessories", "activity": "walking", "season": "cold", "max_price_uah": 1500, "locale": "uk"},
        "Tests cold weather walking gear.")

    # =========================================================================
    # PART 3: FITNESS, MOBILITY & RECOVERY GEAR (15 Scenarios: 51 - 65)
    # Testing foam rollers, massage balls, yoga mats, jump ropes, towels
    # Using valid activities: 'running', 'walking', or 'any' with use_scenario
    # =========================================================================
    add(51, "Athlete: Foam roller & massage ball for recovery", "Runner needing myofascial release roller and trigger point ball",
        {"component_class": "sports_accessories", "activity": "running", "use_scenario": "training", "max_price_uah": 1500, "locale": "uk"},
        "Expects race-expert-165 (Релакс та відновлення: Grid Roller + Massage Ball + Kuznetsov mat) or 154.")
    add(52, "Fitness: Jump rope & ab roller for home workouts", "Fitness enthusiast wanting jump rope and abdominal roller",
        {"component_class": "sports_accessories", "activity": "any", "use_scenario": "training", "max_price_uah": 1500, "locale": "ru"},
        "Expects race-expert-153 (Активний рух: jump rope + ab roller + massage ball).")
    add(53, "Yogi: Yoga mat & resistance band", "Yoga practitioner looking for exercise mat and pilates band",
        {"component_class": "sports_accessories", "activity": "walking", "use_scenario": "training", "max_price_uah": 1500, "locale": "uk"},
        "Expects race-expert-155 (Йога та пілатес: mat + expander); check for protein bar leakage.")
    add(54, "Fitness: Home fitness kit with grid roller & band", "Home workout buyer wanting grid roller, band, and bottle",
        {"component_class": "sports_accessories", "activity": "any", "use_scenario": "everyday", "max_price_uah": 1500, "locale": "ru"},
        "Expects race-expert-154 (Домашній фітнес та тонус).")
    add(55, "Athlete: Kuznetsov acupressure mat & relaxation", "Stressed athlete looking for relaxation and acupressure mat",
        {"component_class": "sports_accessories", "activity": "any", "use_scenario": "everyday", "max_price_uah": 1500, "locale": "uk"},
        "Expects race-expert-165.")
    add(56, "Fitness: Training gear, entry budget 750 UAH", "Beginner wanting fitness equipment under 750 UAH",
        {"component_class": "sports_accessories", "activity": "running", "use_scenario": "training", "max_price_uah": 750, "locale": "uk"},
        "Tests budget bounds for fitness gear.")
    add(57, "Fitness: Bath towels for training / post-workout", "Gym-goer wanting high quality cotton bath towels",
        {"component_class": "sports_accessories", "activity": "any", "use_scenario": "training", "max_price_uah": 1500, "locale": "ru"},
        "Tests match for race-expert-198 / 199 (Банні рушники Шарпей 135x70cm).")
    add(58, "Fitness: Towel & shaker set without supplements", "Functional athlete needing gym towel and shaker bottle",
        {"component_class": "sports_accessories", "activity": "running", "use_scenario": "training", "membership": "no", "max_price_uah": 1500, "locale": "uk"},
        "Tests towel/shaker set with membership=no.")
    add(59, "Runner: Post-run massage gear, Russian locale", "Marathoner needing recovery roller and massage equipment",
        {"component_class": "sports_accessories", "activity": "running", "use_scenario": "training", "max_price_uah": 1500, "locale": "ru"},
        "Expects recovery massage tools with accurate Russian verdict.")
    add(60, "Fitness: Premium home gym gear (2500 UAH)", "Buyer with high budget seeking complete mobility & fitness pack",
        {"component_class": "sports_accessories", "activity": "any", "use_scenario": "training", "max_price_uah": 2500, "locale": "uk"},
        "Tests high budget behavior on fitness accessories.")
    add(61, "Fitness: Mobility equipment, cold season", "Winter athlete training indoors on mobility and core",
        {"component_class": "sports_accessories", "activity": "walking", "use_scenario": "training", "season": "cold", "max_price_uah": 1500, "locale": "ru"},
        "Tests season interaction with indoor fitness gear.")
    add(62, "Fitness: Speed jump rope and hand grip for cardio", "Crossfit athlete wanting speed jump rope with counter",
        {"component_class": "sports_accessories", "activity": "running", "use_scenario": "training", "max_price_uah": 1500, "locale": "uk"},
        "Expects race-expert-153 (jump rope with counter).")
    add(63, "Fitness: Yoga mat without membership", "Yogi strictly refusing club membership",
        {"component_class": "sports_accessories", "activity": "any", "use_scenario": "training", "membership": "no", "max_price_uah": 1500, "locale": "uk"},
        "Tests yoga mat recommendation with membership exclusion.")
    add(64, "Runner: Acupressure & foam roller, budget 1600 UAH", "Trail runner buying massage equipment for home recovery",
        {"component_class": "sports_accessories", "activity": "running", "use_scenario": "everyday", "max_price_uah": 1600, "locale": "uk"},
        "Expects massage roller / acupressure kit.")
    add(65, "Fitness: Everyday fitness accessories, budget 1200 UAH", "Office worker doing morning exercises, budget 1200 UAH",
        {"component_class": "sports_accessories", "activity": "any", "use_scenario": "everyday", "max_price_uah": 1200, "locale": "ru"},
        "Tests fitness gear availability under 1200 UAH.")

    # =========================================================================
    # PART 4: HIKING & OUTDOOR APPAREL & GEAR (10 Scenarios: 66 - 75)
    # Testing thermal socks, outdoor gear, cold/warm trekking
    # =========================================================================
    add(66, "Hiker: Winter trekking thermal socks size 43", "Carpathian winter hiker needing thermal socks size 43",
        {"component_class": "apparel_footwear", "activity": "hiking", "shoe_size": 43, "season": "cold", "max_price_uah": 1200, "locale": "uk"},
        "Expects thermo socks 1+1=3 size 43–45 (1058 UAH).")
    add(67, "Hiker: Winter trekking thermal socks size 40", "Winter mountain trekker needing thermal socks size 40",
        {"component_class": "apparel_footwear", "activity": "hiking", "shoe_size": 40, "season": "cold", "max_price_uah": 1200, "locale": "ru"},
        "Expects thermo socks 1+1=3 size 40–42 (1058 UAH).")
    add(68, "Hiker: Winter trekking thermal socks size 37", "Female winter trekker needing thermal socks size 37",
        {"component_class": "apparel_footwear", "activity": "hiking", "shoe_size": 37, "season": "cold", "max_price_uah": 1200, "locale": "uk"},
        "Expects thermo socks 1+1=3 size 35–37 (1058 UAH).")
    add(69, "Hiker: Winter trekking thermal socks size 46", "Tall winter trekker needing thermal socks size 46",
        {"component_class": "apparel_footwear", "activity": "hiking", "shoe_size": 46, "season": "cold", "max_price_uah": 1200, "locale": "uk"},
        "Tests winter thermal socks for size 46; check catalog size availability.")
    add(70, "Hiker: Summer trekking socks size 43", "Summer backpacker needing breathable hiking socks size 43",
        {"component_class": "apparel_footwear", "activity": "hiking", "shoe_size": 43, "season": "warm", "max_price_uah": 1200, "locale": "ru"},
        "Tests summer trekking socks matching.")
    add(71, "Hiker: Hiking socks, entry budget 600 UAH", "Budget backpacker needing hiking socks under 600 UAH",
        {"component_class": "apparel_footwear", "activity": "hiking", "shoe_size": 40, "max_price_uah": 600, "locale": "uk"},
        "Tests budget lower bound for hiking socks.")
    add(72, "Hiker: General hiking gear, any component class, size 43", "Backpacker wanting complete hiking gear pack",
        {"component_class": "any", "activity": "hiking", "shoe_size": 43, "max_price_uah": 1500, "locale": "uk"},
        "Expects top hiking gear (socks or outdoor pack); check for creatine leaks.")
    add(73, "Hiker: Cold season outdoor gift kit (1500 UAH)", "Buyer looking for warm outdoor gift pack for a hiker",
        {"component_class": "any", "activity": "hiking", "season": "cold", "max_price_uah": 1500, "locale": "ru"},
        "Tests match for race-expert-094 (Подарунок у похід) or thermal socks.")
    add(74, "Hiker: Everyday hiking socks size 41", "Trail walker needing sturdy socks for daily trail walks",
        {"component_class": "apparel_footwear", "activity": "hiking", "shoe_size": 41, "use_scenario": "everyday", "max_price_uah": 1000, "locale": "uk"},
        "Expects dark or white sock pack matching size 41.")
    add(75, "Hiker: Premium hiking gear pack (2000 UAH)", "Experienced trekker with flexible budget 2000 UAH",
        {"component_class": "any", "activity": "hiking", "shoe_size": 43, "max_price_uah": 2000, "locale": "uk"},
        "Tests premium hiking gear recommendations.")

    # =========================================================================
    # PART 5: CYCLING & WALKING GEAR (10 Scenarios: 76 - 85)
    # Testing cycling and walking equipment
    # =========================================================================
    add(76, "Cyclist: Cycling socks size 43, regular budget", "Road cyclist needing cycling socks size 43",
        {"component_class": "apparel_footwear", "activity": "cycling", "shoe_size": 43, "max_price_uah": 1000, "locale": "uk"},
        "Expects technical socks matching size 43.")
    add(77, "Cyclist: Cycling socks size 40, regular budget", "Gravel cyclist needing cycling socks size 40",
        {"component_class": "apparel_footwear", "activity": "cycling", "shoe_size": 40, "max_price_uah": 1000, "locale": "ru"},
        "Expects technical socks matching size 40.")
    add(78, "Cyclist: Winter cycling thermal socks size 44", "Fatbike / winter cyclist needing thermal socks size 44",
        {"component_class": "apparel_footwear", "activity": "cycling", "shoe_size": 44, "season": "cold", "max_price_uah": 1200, "locale": "uk"},
        "Expects thermo socks size 43-45 for winter cycling.")
    add(79, "Cyclist: General cycling gear, any component, budget 1500 UAH", "Cyclist looking for general riding kit up to 1500 UAH",
        {"component_class": "any", "activity": "cycling", "max_price_uah": 1500, "locale": "uk"},
        "Critical test: does engine recommend BCAA powder + club membership (race-expert-150) as top cycling gear?!")
    add(80, "Cyclist: Cycling gear, event prep (gran fondo)", "Cyclist preparing for amateur cycling race",
        {"component_class": "any", "activity": "cycling", "use_scenario": "event_preparation", "max_price_uah": 1500, "locale": "ru"},
        "Check event prep gear for cycling.")
    add(81, "Walker: Walking socks size 37, everyday comfort", "Daily commuter wanting comfortable socks size 37",
        {"component_class": "apparel_footwear", "activity": "walking", "shoe_size": 37, "use_scenario": "everyday", "max_price_uah": 1000, "locale": "uk"},
        "Expects 5-pack socks size 35–37.")
    add(82, "Walker: Walking socks size 40, everyday comfort", "Office worker walking 10k steps daily, size 40",
        {"component_class": "apparel_footwear", "activity": "walking", "shoe_size": 40, "use_scenario": "everyday", "max_price_uah": 1000, "locale": "ru"},
        "Expects 5-pack socks size 38–40 or 40–42.")
    add(83, "Walker: Walking socks size 43, everyday comfort", "Pedestrian walking outdoors daily, size 43",
        {"component_class": "apparel_footwear", "activity": "walking", "shoe_size": 43, "use_scenario": "everyday", "max_price_uah": 1000, "locale": "uk"},
        "Expects 5-pack socks size 43–45.")
    add(84, "Walker: Winter walking thermal socks size 43", "Winter walker needing warm thermo socks size 43",
        {"component_class": "apparel_footwear", "activity": "walking", "shoe_size": 43, "season": "cold", "max_price_uah": 1200, "locale": "uk"},
        "Expects thermo socks 1+1=3 size 43–45.")
    add(85, "Walker: Walking gear, any component, budget 1200 UAH", "General walker wanting walking equipment up to 1200 UAH",
        {"component_class": "any", "activity": "walking", "max_price_uah": 1200, "locale": "ru"},
        "Tests general walking gear matching.")

    # =========================================================================
    # PART 6: SWIMMING GEAR TAXONOMY AUDIT (5 Scenarios: 86 - 90)
    # Swimming is explicitly offered in ACTIVITY_OPTIONS_BY_GOAL['gear']!
    # =========================================================================
    add(86, "Swimmer: Swimming gear, any component (1500 UAH)", "Triathlete / swimmer looking for swimming gear",
        {"component_class": "any", "activity": "swimming", "max_price_uah": 1500, "locale": "uk"},
        "Critical taxonomy test: ACTIVITY_OPTIONS_BY_GOAL['gear'] includes swimming. Does it return 0 sets?")
    add(87, "Swimmer: Swimming accessories (towel, goggles, cap)", "Pool swimmer looking for swimming accessories",
        {"component_class": "sports_accessories", "activity": "swimming", "max_price_uah": 1500, "locale": "ru"},
        "Tests sports_accessories for swimming.")
    add(88, "Swimmer: Swimming gear, training scenario", "Master swimmer training regularly in pool",
        {"component_class": "any", "activity": "swimming", "use_scenario": "training", "max_price_uah": 1500, "locale": "uk"},
        "Tests swimming gear with training scenario.")
    add(89, "Swimmer: Swimming gear, event preparation (open water)", "Open water swimmer preparing for Bosporus cross",
        {"component_class": "any", "activity": "swimming", "use_scenario": "event_preparation", "max_price_uah": 2000, "locale": "ru"},
        "Tests open water event prep swimming gear.")
    add(90, "Swimmer: Swimming gear, budget 1000 UAH", "Student swimmer with 1000 UAH budget",
        {"component_class": "any", "activity": "swimming", "max_price_uah": 1000, "locale": "uk"},
        "Tests swimming gear with tight budget.")

    # =========================================================================
    # PART 7: GENERAL / MIXED GEAR & APPAREL (5 Scenarios: 91 - 95)
    # Testing general gear requests across all activities
    # =========================================================================
    add(91, "Athlete: General gear, running, size 43, no class constraint", "Runner looking for best gear recommendation without picking class",
        {"component_class": "any", "activity": "running", "shoe_size": 43, "max_price_uah": 1500, "locale": "uk"},
        "Expects best running gear (socks or accessories); check whether creatine sets outrank gear.")
    add(92, "Athlete: General gear, running, size 40, budget 1000 UAH", "Runner with 1000 UAH budget, size 40",
        {"component_class": "any", "activity": "running", "shoe_size": 40, "max_price_uah": 1000, "locale": "ru"},
        "Expects 950 UAH socks matching size 40.")
    add(93, "Athlete: General gear, cold season, size 43", "Cold weather multi-sport athlete, size 43",
        {"component_class": "any", "season": "cold", "shoe_size": 43, "max_price_uah": 1500, "locale": "uk"},
        "Expects thermo socks 1+1=3 size 43-45.")
    add(94, "Athlete: General gear, warm season, size 40", "Warm weather multi-sport athlete, size 40",
        {"component_class": "any", "season": "warm", "shoe_size": 40, "max_price_uah": 1500, "locale": "ru"},
        "Check warm season general gear matching.")
    add(95, "Athlete: General gear, event preparation, budget 1500 UAH", "Athlete preparing for upcoming sports event",
        {"component_class": "any", "use_scenario": "event_preparation", "max_price_uah": 1500, "locale": "uk"},
        "Expects event preparation sports gear.")

    # =========================================================================
    # PART 8: EDGE CASES, BOUNDARY CONDITIONS & CRASH RESILIENCE (5 Scenarios: 96 - 100)
    # =========================================================================
    add(96, "Edge Case: String shoe size '42-44'", "Buyer entering '42-44' as string instead of single number",
        {"component_class": "apparel_footwear", "shoe_size": "42-44", "max_price_uah": 1200, "locale": "uk"},
        "Tests schema resilience: does draft_matcher crash with DraftMatchError or sanitize?")
    add(97, "Edge Case: Extremely low budget (400 UAH) gear search", "Buyer with only 400 UAH looking for gear",
        {"component_class": "apparel_footwear", "max_price_uah": 400, "locale": "ru"},
        "Tests floor anchor behavior: gear starts at 950 UAH; does engine give honest floor anchor?")
    add(98, "Edge Case: Ultra-high budget (3000 UAH) gear search", "Wealthy buyer with 3000 UAH looking for premium sports gear",
        {"component_class": "any", "max_price_uah": 3000, "locale": "uk"},
        "Check if highest priced sets are legitimate gear or gym subscriptions with creatine.")
    add(99, "Edge Case: Extreme shoe size (50)", "Giant runner with EU shoe size 50",
        {"component_class": "apparel_footwear", "shoe_size": 50, "max_price_uah": 1500, "locale": "ru"},
        "Tests out-of-catalog size handling: does engine honestly reject or mismatch?")
    add(100, "Edge Case: Contradictory request (sports_accessories with shoe size 43)", "Buyer asking for sports accessories but specifying shoe size 43",
        {"component_class": "sports_accessories", "shoe_size": 43, "max_price_uah": 1500, "locale": "uk"},
        "Tests engine behavior when asking for accessories while providing shoe size.")

    return scenarios

def evaluate_test_result(scenario, response, exception=None):
    """Deep human / athletic / buyer evaluation of a single test run."""
    req = scenario["request"]
    tid = scenario["test_id"]
    
    # Check if crashed
    if exception is not None:
        if tid == 96 and "must be a numeric shoe size" in str(exception):
            return {
                "verdict": "FAIL",
                "flaw_type": "SCHEMA_CRASH_UNSANITIZED_INPUT",
                "flaw_summary": "Двигун впав з винятком DraftMatchError при передачі діапазону розміру рядком '42-44'.",
                "details": f"Виняток: {str(exception)}. Потрібна санітизація/парсинг діапазонів або прозоре повідомлення.",
                "d1_real_gear": False,
                "d2_size_match": False,
                "d3_class_alignment": False,
                "d4_no_supplement_leak": True,
                "d5_truthful_explanation": False
            }
        return {
            "verdict": "FAIL",
            "flaw_type": "ENGINE_EXCEPTION",
            "flaw_summary": f"Неочікуваний виняток матчера: {str(exception)}",
            "details": str(exception),
            "d1_real_gear": False,
            "d2_size_match": False,
            "d3_class_alignment": False,
            "d4_no_supplement_leak": True,
            "d5_truthful_explanation": False
        }

    status = response.get("status")
    results = response.get("results", [])
    near_miss = response.get("near_miss_results", [])
    floor_anchor = response.get("floor_anchor_results", [])
    items_to_eval = results if results else (near_miss if near_miss else floor_anchor)

    # Check Taxonomy Blunders
    act = req.get("activity")
    if act == "swimming":
        if status in ("no_match", "no_exact_match") and not results:
            return {
                "verdict": "FAIL",
                "flaw_type": "SWIMMING_TAXONOMY_DEAD_END",
                "flaw_summary": "Таксономічний глухий кут: 'swimming' офіційно дозволений у вікторині для 'gear', але в каталозі 0 товарів для плавання!",
                "details": "Користувач обрав плавання, система дозволила вибір, але повернула status: no_match (0 наборів). Справжній плавець не отримав шапочки, окулярів чи рушника.",
                "d1_real_gear": False,
                "d2_size_match": True,
                "d3_class_alignment": False,
                "d4_no_supplement_leak": True,
                "d5_truthful_explanation": False
            }

    # Extreme shoe size 50 handling
    if req.get("shoe_size") == 50:
        if not results:
            return {
                "verdict": "PASS",
                "flaw_type": "NONE",
                "flaw_summary": "Двигун чесно визнав відсутність 50-го розміру (максимум у каталозі 48).",
                "details": "Коректна обробка відсутності рідкісного розміру.",
                "d1_real_gear": True,
                "d2_size_match": True,
                "d3_class_alignment": True,
                "d4_no_supplement_leak": True,
                "d5_truthful_explanation": True
            }

    # If no items returned at all
    if not items_to_eval:
        budget = req.get("max_price_uah")
        if budget is not None and budget < 950:
            return {
                "verdict": "WARN",
                "flaw_type": "BUDGET_FLOOR_OR_NEAR_MISS",
                "flaw_summary": f"Бюджет {budget} ₴ нижчий за мінімальний (950 ₴), але ані near_miss, ані floor_anchor не спрацювали.",
                "details": f"Статус: {status}, повідомлення: {response.get('message')}",
                "d1_real_gear": False,
                "d2_size_match": True,
                "d3_class_alignment": True,
                "d4_no_supplement_leak": True,
                "d5_truthful_explanation": True
            }
        return {
            "verdict": "FAIL",
            "flaw_type": "ZERO_RESULTS_UNEXPECTED",
            "flaw_summary": f"Неочікувана порожня видача для валідного запиту: {status}",
            "details": f"Повідомлення: {response.get('message')}",
            "d1_real_gear": False,
            "d2_size_match": False,
            "d3_class_alignment": False,
            "d4_no_supplement_leak": True,
            "d5_truthful_explanation": False
        }

    # Detailed Evaluation of returned items
    flaws = []
    d1_real_gear = True
    d2_size_match = True
    d3_class_alignment = True
    d4_no_supplement_leak = True
    d5_truthful_explanation = True

    top_item = items_to_eval[0]
    top_title = top_item.get("title", "")
    top_sid = top_item.get("set_id", "")
    top_price = top_item.get("price_uah", 0)
    top_reasons = top_item.get("reasons", [])
    top_summary = top_item.get("expert_summary", "")
    
    # Load raw catalog record for deep composition check
    cat_item = next((c for c in catalog if c["set_id"] == top_sid), {})
    comp = str(cat_item.get("composition", "")).lower()
    title_lower = top_title.lower()
    desc_lower = str(cat_item.get("description", "")).lower()

    # D1 & D4: Check for supplements, creatine, BCAA, food, gym club membership leakage
    has_creatine = any(w in comp or w in title_lower for w in ["креатин", "creatine"])
    has_supplements = any(w in comp or w in title_lower for w in [
        "bcaa", "eaa", "l-carnitine", "карнітин", "вітамін", "vitamin", "софтгел", "капсул", "магній", "глютамін"
    ])
    has_food = any(w in comp or w in title_lower for w in [
        "батончик", "печиво", "сублімовані фрукти", "сублімован", "napiy"
    ])
    has_membership = "абонемент" in comp or "абонемент" in title_lower or "race expert club" in title_lower

    if has_creatine:
        d1_real_gear = False
        d4_no_supplement_leak = False
        flaws.append(f"КРИТИЧНИЙ ВИТІК БОДІБІЛДИНГУ: Набір [{top_sid}] '{top_title}' містить банку чистого КРЕАТИНУ моногідрату у відповідь на запит спортивного екіпірування!")

    if has_supplements and not has_creatine:
        d4_no_supplement_leak = False
        flaws.append(f"ВИТІК ДОБАВОК/ВІТАМІНІВ: Набір [{top_sid}] '{top_title}' містить фармакологічні добавки (BCAA/карнітин/вітаміни) у розділі одягу та екіпірування.")

    if has_food:
        d4_no_supplement_leak = False
        flaws.append(f"ВИТІК ЇЖІ/СНЕКІВ: Набір [{top_sid}] '{top_title}' містить їстівні батончики/печиво/сублімати у розділі спорядження.")

    if has_membership and not any(w in title_lower for w in ["шкарпет", "пояс", "пляшк", "кепка", "рушник", "ролик", "коврик"]):
        flaws.append(f"ДОМІНУВАННЯ АБОНЕМЕНТА: Набір [{top_sid}] є насамперед 3-місячною підпискою на клуб, а не реальним спортивним спорядженням.")

    # D2: Shoe size precision check
    req_size = req.get("shoe_size")
    if isinstance(req_size, int):
        ranges = _size_ranges(cat_item)
        if ranges:
            size_fits = any(lower <= req_size <= upper for lower, upper in ranges)
            if not size_fits:
                d2_size_match = False
                flaws.append(f"КРИТИЧНИЙ ЗБІЙ РОЗМІРУ: Покупець обрав розмір {req_size}, але набір [{top_sid}] має розмірність {ranges}!")
        elif cat_item.get("matching_evidence", {}).get("size_sensitive"):
            d2_size_match = False
            flaws.append(f"НЕВИЗНАЧЕНИЙ РОЗМІР: Набір [{top_sid}] чутливий до розміру, але точний діапазон не відповідає {req_size}.")
    elif req_size in (None, "any") and req.get("component_class") == "apparel_footwear":
        # Check if blindly defaulted to 46-48
        if "46–48" in top_title or "46 - 48" in top_title:
            flaws.append(f"ЗСУВ ЗАМОВЧУВАННЯ: При неуточненому розмірі система нав'язує гігантський розмір «46–48» (бо він найдешевший за 950 грн).")

    # D3: Component class alignment
    req_class = req.get("component_class")
    if req_class == "sports_accessories":
        is_pure_apparel = all(w not in comp and w not in title_lower for w in [
            "пояс", "пляшк", "фляг", "шнурк", "ролик", "коврик", "масаж", "рушник", "шейкер", "скакалка", "еспандер"
        ])
        if is_pure_apparel:
            d3_class_alignment = False
            flaws.append(f"ПОРУШЕННЯ КАТЕГОРІЇ: Користувач просив спортивні аксесуари, але отримав виключно шкарпетки [{top_sid}] '{top_title}'.")
        elif "носки" in comp or "шкарпет" in comp:
            # Accessories contaminated by socks or creatine
            if has_creatine or has_membership:
                flaws.append(f"СПОТВОРЕННЯ АКСЕСУАРІВ: Під виглядом аксесуара видано абонемент з креатином та шкарпетками [{top_sid}].")

    # D5: Explanation truthfulness check
    for r_text in top_reasons:
        if "без сторонніх речей" in r_text:
            if has_creatine or has_supplements or has_food or has_membership:
                d5_truthful_explanation = False
                flaws.append(f"НЕПРАВДИВЕ ПОЯСНЕННЯ В WHY_SUITABLE: Система заявляє '{r_text}', але набір [{top_sid}] містить сторонні компоненти (креатин/добавки/їжу/абонемент)!")

    # Check for bodybuilding pitch in gear summary
    if any(w in top_summary.lower() for w in ["вибухову силу", "мышечный рост", "м'язовий ріст", "анаболізм", "пиковую силу"]):
        d5_truthful_explanation = False
        flaws.append(f"НЕАДЕКВАТНИЙ ЕКСПЕРТНИЙ ВЕРДИКТ: Текст вердикту прославляє бодібілдинг/набір маси для спорядження: '{top_summary}'.")

    # Budget near miss / floor anchor evaluation
    budget = req.get("max_price_uah")
    if budget is not None and top_price > budget:
        if status == "floor_anchor":
            flaws.append(f"ЦІНОВИЙ ЯКІР: Бюджет {budget} ₴ нижчий за мінімальний у каталозі (950 ₴). Запропоновано базовий набір за {top_price} ₴.")
        elif status == "no_match" and near_miss:
            over = top_price - budget
            flaws.append(f"NEAR-MISS ПЕРЕВИЩЕННЯ: Бюджет {budget} ₴, товар {top_price} ₴ (перевищення на {over} ₴).")

    # Determine Final Verdict
    if any("КРИТИЧНИЙ" in f or "СПОТВОРЕННЯ" in f for f in flaws) or not d1_real_gear or not d2_size_match or not d5_truthful_explanation:
        verdict = "FAIL"
    elif flaws:
        verdict = "WARN"
    else:
        verdict = "PASS"

    flaw_type = "NONE"
    if verdict == "FAIL":
        if not d2_size_match:
            flaw_type = "SIZING_MISMATCH"
        elif not d4_no_supplement_leak or not d1_real_gear:
            flaw_type = "SUPPLEMENT_CREATINE_LEAK"
        elif not d5_truthful_explanation:
            flaw_type = "DECEPTIVE_EXPLANATION"
        else:
            flaw_type = "CRITICAL_LOGIC_DEFECT"
    elif verdict == "WARN":
        if "ЗСУВ ЗАМОВЧУВАННЯ" in " ".join(flaws):
            flaw_type = "DEFAULT_SIZE_BIAS"
        elif "ЦІНОВИЙ ЯКІР" in " ".join(flaws) or "NEAR-MISS" in " ".join(flaws):
            flaw_type = "BUDGET_FLOOR_OR_NEAR_MISS"
        elif "ВИТІК ЇЖІ" in " ".join(flaws) or "ДОМІНУВАННЯ" in " ".join(flaws):
            flaw_type = "MINOR_LEAKAGE_OR_MEMBERSHIP"
        else:
            flaw_type = "SUBOPTIMAL_RECOMMENDATION"

    return {
        "verdict": verdict,
        "flaw_type": flaw_type,
        "flaw_summary": flaws[0] if flaws else "Ідеальний збіг за спорядженням, розміром, бюджетом та поясненнями.",
        "all_flaws": flaws,
        "top_item": {
            "set_id": top_sid,
            "title": top_title,
            "price_uah": top_price,
            "status": status,
            "reasons": top_reasons,
            "expert_summary": top_summary
        },
        "d1_real_gear": d1_real_gear,
        "d2_size_match": d2_size_match,
        "d3_class_alignment": d3_class_alignment,
        "d4_no_supplement_leak": d4_no_supplement_leak,
        "d5_truthful_explanation": d5_truthful_explanation
    }

def main():
    print("Initializing QA Agent 6 Environment...")
    global catalog
    catalog = load_environment()
    scenarios = generate_100_scenarios()
    print(f"Loaded {len(catalog)} catalog sets and generated {len(scenarios)} buyer test scenarios.\n")

    test_results = []
    verdict_counts = {"PASS": 0, "WARN": 0, "FAIL": 0}
    flaw_type_counts = {}

    for idx, sc in enumerate(scenarios, 1):
        req = sc["request"]
        res = None
        exc = None
        try:
            res = draft_recommend(catalog, req)
        except Exception as e:
            exc = e

        eval_res = evaluate_test_result(sc, res, exc)
        v = eval_res["verdict"]
        verdict_counts[v] += 1
        ft = eval_res["flaw_type"]
        flaw_type_counts[ft] = flaw_type_counts.get(ft, 0) + 1

        record = {
            "test_id": sc["test_id"],
            "name": sc["name"],
            "persona": sc["persona"],
            "request": sc["request"],
            "expected_focus": sc["expected_focus"],
            "evaluation": eval_res
        }
        test_results.append(record)
        print(f"[{sc['test_id']:03d}/100] {v:<4} | {ft:<28} | {sc['name'][:42]:<42} -> {eval_res['flaw_summary'][:50]}")

    print("\n" + "="*80)
    print("TEST EXECUTION COMPLETED")
    print(f"PASS: {verdict_counts['PASS']} | WARN: {verdict_counts['WARN']} | FAIL: {verdict_counts['FAIL']}")
    print("Flaw Type Distribution:")
    for ft, cnt in sorted(flaw_type_counts.items(), key=lambda x: -x[1]):
        print(f"  - {ft}: {cnt}")
    print("="*80)

    # Save complete JSON results
    OUTPUT_JSON.write_text(json.dumps({
        "agent": "QA Agent 6 - Gear & Apparel Specialist",
        "total_tests": len(test_results),
        "summary": verdict_counts,
        "flaw_types": flaw_type_counts,
        "tests": test_results
    }, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nSaved 100 test runs to {OUTPUT_JSON}")

    # Build human-readable Markdown Report
    build_markdown_report(test_results, verdict_counts, flaw_type_counts)
    print(f"Saved human-readable audit report to {OUTPUT_REPORT}")

def build_markdown_report(results, summary, flaw_types):
    """Generate professional, detailed markdown report."""
    pass_pct = round(summary["PASS"] / len(results) * 100, 1)
    warn_pct = round(summary["WARN"] / len(results) * 100, 1)
    fail_pct = round(summary["FAIL"] / len(results) * 100, 1)

    md = []
    md.append("# QA Agent 6: Gear & Apparel Specialist — 100 Buyer Test Case Audit Report")
    md.append("**Date:** 2026-11-12  ")
    md.append("**Role:** QA Agent 6 — Gear & Apparel Specialist (Human Athlete & Equipment Perspective)  ")
    md.append("**Scope:** Race Expert Quiz — Gear & Accessories (`goal_group: 'gear'`)  ")
    md.append("**Catalog Source:** `wiki/projects/quiz-set-audit.json` (207 sets loaded, 68 candidate gear sets)  ")
    md.append("**Matcher Engine:** `test-quiz-sandbox/draft_matcher.py:draft_recommend`  \n")

    md.append("## 1. Executive Summary")
    md.append("| Metric | Count | Percentage |")
    md.append("|---|---|---|")
    md.append(f"| **Total Scenarios** | **{len(results)}** | **100.0%** |")
    md.append(f"| **PASS (Sound Gear Buyer Experience)** | **{summary['PASS']}** | **{pass_pct}%** |")
    md.append(f"| **WARN (Suboptimal / Diluted / Near-Miss / Bias)** | **{summary['WARN']}** | **{warn_pct}%** |")
    md.append(f"| **FAIL (Critical Breakdown / Creatine Leak / Sizing Mismatch)** | **{summary['FAIL']}** | **{fail_pct}%** |")
    md.append("\n```")
    md.append(f"Verdict Distribution: [{'#' * int(pass_pct/2)}{'-' * int(warn_pct/2)}{'!' * int(fail_pct/2)}]")
    md.append(f"  PASS: {summary['PASS']} | WARN: {summary['WARN']} | FAIL: {summary['FAIL']}")
    md.append("```\n")

    md.append("## 2. Flaw Taxonomy & Defect Distribution")
    md.append("| Defect Code | Description | Count | Severity |")
    md.append("|---|---|---|---|")
    for ft, cnt in sorted(flaw_types.items(), key=lambda x: -x[1]):
        if ft == "NONE":
            sev = "PASS"
        elif ft in ("SUPPLEMENT_CREATINE_LEAK", "SIZING_MISMATCH", "DECEPTIVE_EXPLANATION", "SWIMMING_TAXONOMY_DEAD_END", "SCHEMA_CRASH_UNSANITIZED_INPUT", "CRITICAL_LOGIC_DEFECT", "ZERO_RESULTS_UNEXPECTED"):
            sev = "CRITICAL FAIL"
        else:
            sev = "WARN"
        md.append(f"| `{ft}` | {get_flaw_desc(ft)} | **{cnt}** | {sev} |")
    md.append("\n")

    md.append("## 3. Critical Architectural & Athletic Logic Findings")
    
    md.append("### Finding 1: Massive Bodybuilding Creatine & Supplement Leakage into Gear (CRITICAL FAIL)")
    md.append("> [!CAUTION]")
    md.append("> **500g Bodybuilder Creatine Monohydrate Sold as 'Running Gear & Accessories':**")
    md.append("> In `quiz-set-audit.json`, multiple gym strength sets (`race-expert-009`, `race-expert-029`, `race-expert-040`, `race-expert-068`, `race-expert-149`) were erroneously assigned `candidate_tiers.seller_positioned: ['foot_apparel_comfort']` and `component_based: ['foot_apparel_comfort']`.")
    md.append("> As a catastrophic consequence, when a runner or walker selects `goal_group: 'gear'`, `component_class: 'sports_accessories'`, the quiz recommends:")
    md.append("> - **Set `race-expert-068` (Набір «Чоловіча сила», 1005 ₴):** 500g Creatine Monohydrate tub + 4 pairs of socks + 3-month gym club membership!")
    md.append("> - **Set `race-expert-040` (Набір «Ріст м'язів», 1225 ₴):** Bodyperson Creatine Monohydrate 500g + 2x Lipobar protein bars + club membership!")
    md.append("> - **Set `race-expert-009` (Набір «Чиста сила», 1399 ₴):** 500g Myprotein Creatine Monohydrate + shaker + club membership!")
    md.append("> Selling a powerlifter mass-gain creatine tub to a runner asking for water bottles and race belts completely destroys the credibility of Race Expert as an endurance specialist.")
    md.append("\n")

    md.append("### Finding 2: False 'No Foreign Items' Guarantees in Explanations (CRITICAL FAIL)")
    md.append("> [!WARNING]")
    md.append("> In `draft_matcher.py:_build_why_suitable()`, when `component_class: 'sports_accessories'` is selected, the engine prints:")
    md.append("> *«Категорія товарів: у наборі саме Спортивні аксесуари та пляшки (без сторонніх речей).»*")
    md.append("> Yet for `race-expert-068`, over 80% of the set's physical content is a **500g tub of bodybuilding creatine** and a **3-month gym club subscription**!")
    md.append("> Guaranteeing to the consumer that there are *'no foreign items'* while handing them a tub of muscle-building powder and an unrequested club membership is fraudulent marketing that violates consumer trust.")
    md.append("\n")

    md.append("### Finding 3: Swimming Gear Taxonomy Dead-End (CRITICAL FAIL)")
    md.append("> [!IMPORTANT]")
    md.append("> `draft_matcher.py` explicitly lists `swimming` in `ACTIVITY_OPTIONS_BY_GOAL['gear'] = {'running', 'hiking', 'cycling', 'walking', 'swimming'}`.")
    md.append("> However, in the catalog, **ZERO sets out of 207** support swimming!")
    md.append("> When a swimmer clicks 'Swimming' looking for swim gear (swim cap, goggles, fast-drying towel), the draft matcher returns **`status: no_match` (0 sets)**.")
    md.append("> Offering a sport in the quiz UI that has a 100% dead-end guarantee is a major UX defect.")
    md.append("\n")

    md.append("### Finding 4: Cyclist Hard-Block for Socks (CRITICAL FAIL)")
    md.append("> [!WARNING]")
    md.append("> In `quiz-set-audit.json`, **none of the 29 sock sets** include `cycling` in `activity_groups` (they only list `running, hiking, walking, general_lifestyle`).")
    md.append("> Because `activity` is a mandatory core filter, any cyclist requesting socks receives **`status: no_match` (0 sets)**, while cyclists requesting general gear receive gym subscriptions with BCAA powder (`race-expert-150`).")
    md.append("\n")

    md.append("### Finding 5: Sizing Pitfalls & Default Size 46–48 Bias (CRITICAL FAIL & WARN)")
    md.append("> [!NOTE]")
    md.append("> **1. Mismatched Sizing on Accessory Bundles:** Sets like `race-expert-056`, `115`, and `210` bundle race accessories (cap, bib belt, bottle) with fixed size **40–42 white socks**. When a female athlete with shoe size **37** requests race accessories, the engine either fails or sends socks 3 sizes too large.")
    md.append("> **2. Default Size 46–48 Bias:** When a user does not specify a shoe size (`shoe_size: 'any'`), the engine defaults to recommending **«46–48» socks** (the lowest priced set at 950 ₴). For the average Ukrainian runner (shoe size 38–43), receiving EU 46–48 socks makes them completely unwearable.")
    md.append("> **3. Crash on String Range Input:** Passing a string range like `'42-44'` causes `draft_matcher` to crash with `DraftMatchError: shoe_size must be a numeric shoe size.` instead of cleanly parsing or sanitizing.")
    md.append("\n")

    md.append("### Finding 6: Extreme Apparel Catalog Monoculture (Only Socks!)")
    md.append("> Out of 29 sets tagged as `apparel_footwear` in the catalog, **100% are socks** (either 5-pair cotton/polyester packs at 950 ₴ or 3-pair thermal packs at 1058 ₴).")
    md.append("> There are **zero** running t-shirts, shorts, windbreakers, tights, caps (standalone), gloves, or shoes in the catalog.")
    md.append("> Furthermore, for budget-conscious buyers (400–800 ₴), **zero sets exist under 950 ₴** in gear, forcing every budget runner into near-miss or floor-anchor states.")
    md.append("\n")

    md.append("## 4. Comprehensive Test Scenario Log (100 Cases)")
    md.append("| # | Scenario Name | Budget | Size | Class | Activity | Verdict | Main Flaw / Human-Logic Evaluation |")
    md.append("|---|---|---|---|---|---|---|---|")
    for r in results:
        sc = r["request"]
        ev = r["evaluation"]
        tid = r["test_id"]
        name = r["name"][:35]
        b = f"{sc.get('max_price_uah', 'any')} ₴" if sc.get('max_price_uah') else "any"
        s = sc.get('shoe_size', 'any')
        c = sc.get('component_class', 'any')
        act = sc.get('activity', 'any')
        v = ev["verdict"]
        flaw = ev["flaw_summary"].replace("|", "/")
        v_bold = f"**{v}**"
        md.append(f"| {tid:03d} | {name} | {b} | {s} | {c} | {act} | {v_bold} | {flaw} |")
    md.append("\n")

    md.append("## 5. Strategic Recommendations for Quiz & Catalog Engineering")
    md.append("1. **Purge Gym Sets from `foot_apparel_comfort` in `quiz-set-audit.json`:** Immediately strip `foot_apparel_comfort` from sets `race-expert-009, 028, 029, 040, 068, 075, 142, 147, 148, 149, 150, 151, 155, 162, 206`. They belong strictly to `training` and `strength_muscle_training`.")
    md.append("2. **Fix `why_suitable` Deceptive Claims:** Remove the hardcoded phrase `(без сторонніх речей)` unless verified that 100% of the set's items belong to the requested component class.")
    md.append("3. **Fix Swimming Option:** Either onboard genuine swimming gear (silicone caps, anti-fog goggles, microfiber swim towels) or remove `swimming` from `ACTIVITY_OPTIONS_BY_GOAL['gear']`.")
    md.append("4. **Add `cycling` to Socks Activity Scope:** Add `cycling` to `activity_groups` for sport sock bundles so cyclists can receive socks.")
    md.append("5. **Fix Sizing UX:** Parse range strings like `'42-44'` or `'39-41'` safely. For size-unspecified queries, prompt the user for their shoe size rather than silently defaulting to size 46–48.")
    md.append("6. **Expand Entry-Level Gear Catalog:** Introduce standalone gear items under 800 ₴: single pairs of technical running socks (250–350 ₴), standalone soft flasks (400–600 ₴), and elastic race number belts (350–500 ₴).")

    OUTPUT_REPORT.write_text("\n".join(md), encoding="utf-8")

def get_flaw_desc(code):
    descs = {
        "NONE": "Ідеальна відповідність спортивному призначенню, розміру та ціні",
        "SUPPLEMENT_CREATINE_LEAK": "Витік бодібілдерського креатину, банок або фармакологічних добавок у спорядження",
        "SIZING_MISMATCH": "Невідповідність розміру шкарпеток обраному розміру взуття",
        "DECEPTIVE_EXPLANATION": "Неправдиві маркетингові твердження (наприклад, 'без сторонніх речей' при наявності добавок)",
        "SWIMMING_TAXONOMY_DEAD_END": "Глухий кут: плавання дозволено у вікторині, але в каталозі 0 товарів для плавання",
        "SCHEMA_CRASH_UNSANITIZED_INPUT": "Падіння двигуна на рядковому діапазоні розміру (наприклад, '42-44')",
        "ZERO_RESULTS_UNEXPECTED": "Порожня видача (0 результатів) для валідного спортивного запиту",
        "BUDGET_FLOOR_OR_NEAR_MISS": "Бюджет покупця (400–800 ₴) нижчий за мінімальний у каталозі (950 ₴)",
        "DEFAULT_SIZE_BIAS": "При неуточненому розмірі система автоматично нав'язує гігантський розмір 46–48",
        "MINOR_LEAKAGE_OR_MEMBERSHIP": "Набір містить спорядження, але розбавлений абонементом або їстівними батончиками",
        "SUBOPTIMAL_RECOMMENDATION": "Субоптимальний вибір товару за сезоном або призначенням"
    }
    return descs.get(code, code)

if __name__ == "__main__":
    main()
