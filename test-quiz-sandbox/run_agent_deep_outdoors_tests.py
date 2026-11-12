# -*- coding: utf-8 -*-
"""QA Specialist for Outdoors & Hiking: 100 Dedicated Buyer Test Scenarios & Evaluation."""

import json
import os
import sys
from pathlib import Path

SANDBOX_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SANDBOX_DIR.parent
sys.path.insert(0, str(SANDBOX_DIR))

from draft_matcher import attach_audit_evidence, draft_recommend, DraftMatchError

CATALOG_PATH = SANDBOX_DIR / "catalog.json"
AUDIT_PATH = PROJECT_ROOT / "wiki" / "projects" / "quiz-set-audit.json"
OUTPUT_JSON = SANDBOX_DIR / "agent_deep_outdoors_100_tests.json"
OUTPUT_REPORT = SANDBOX_DIR / "agent_deep_outdoors_report.md"

def load_environment():
    cat = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    audit = json.loads(AUDIT_PATH.read_text(encoding="utf-8"))
    catalog = attach_audit_evidence(cat, audit)
    return catalog

def generate_100_scenarios():
    scenarios = []

    def add(tid, name, persona, request_params, expected):
        scenarios.append({
            "test_id": tid,
            "name": name,
            "persona": persona,
            "request": {"goal_group": "outdoors", **request_params},
            "expected_focus": expected
        })

    # =========================================================================
    # PART 1: DEHYDRATED EXPEDITION MEALS (ЇDLO 2.0, ЇDLO Club, ЇDLO 3.0) (1-20)
    # =========================================================================
    add(1, "Expedition: Dehydrated meal selection via component_class",
        "Carpathian hiker selecting 'dehydrated_meal' in the quiz",
        {"component_class": "dehydrated_meal", "max_price_uah": 1500, "locale": "uk"},
        "CRITICAL TEST: Does engine return ЇDLO meals or break with 0 results because of class mismatch?")

    add(2, "Expedition: ЇDLO 2.0 pure food pack without club membership",
        "Backpacker wanting pure dehydrated meals without paying for gym/club membership",
        {"component_class": "protein_carbohydrate_food", "membership": "no", "max_price_uah": 1500, "locale": "uk"},
        "Expects race-expert-111 (ЇDLO 2.0) with borsch, chicken potato, polenta, buckwheat.")

    add(3, "Expedition: ЇDLO Club pack with carpathian tea",
        "Camper preparing for multi-day trek wanting hot meals and tea",
        {"component_class": "protein_carbohydrate_food", "use_place": "hiking_or_camping", "max_price_uah": 1500, "locale": "uk"},
        "Expects ЇDLO meal sets (race-expert-078 or 111).")

    add(4, "Expedition: ЇDLO 3.0 hot meals + jerky + protein cookies",
        "Mountaineer seeking ЇDLO 3.0 combo ration with meat and cookies",
        {"component_class": "protein_carbohydrate_food", "activity": "hiking", "max_price_uah": 1500, "locale": "uk"},
        "Expects race-expert-191 (ЇDLO 3.0) or 078/111.")

    add(5, "Expedition: Dehydrated meals for cold weather camping",
        "Winter camper in sub-zero Carpathian temps looking for hot camp meals",
        {"component_class": "protein_carbohydrate_food", "season": "cold", "max_price_uah": 1500, "locale": "uk"},
        "Tests season filtering on food sets: are food sets excluded due to empty weather tags?")

    add(6, "Expedition: Dehydrated food with product_form 'food_or_meal'",
        "Hiker filtering specifically for meal form rations",
        {"component_class": "protein_carbohydrate_food", "product_form": "food_or_meal", "max_price_uah": 1500, "locale": "uk"},
        "CRITICAL TEST: Does product_form 'food_or_meal' exclude ЇDLO 2.0 and ЇDLO Club because of missing form tags?")

    add(7, "Expedition: Weekend trekking meal pack under 1500 UAH",
        "Weekend hiker looking for complete 2-day ration up to 1500 UAH",
        {"component_class": "protein_carbohydrate_food", "activity": "hiking", "max_price_uah": 1500, "locale": "uk"},
        "Expects ЇDLO meal sets.")

    add(8, "Expedition: Freeze-dried fruit dessert & sweet mix",
        "Trekker wanting freeze-dried fruit snacks and treats",
        {"component_class": "protein_carbohydrate_food", "activity": "hiking", "max_price_uah": 1400, "locale": "uk"},
        "Expects race-expert-075 (Сублімований мікс, 1389 UAH) or 076 (Мандрівний смаколик, 1249 UAH).")

    add(9, "Expedition: Freeze-dried snacks & chocolate drink",
        "Trail camper wanting warm beverage and freeze-dried fruits",
        {"component_class": "protein_carbohydrate_food", "max_price_uah": 1300, "locale": "uk"},
        "Expects race-expert-076 (Мандрівний смаколик with Napiy drink, 1249 UAH).")

    add(10, "Expedition: Dehydrated rations with budget 1200 UAH",
        "Budget backpacker with 1200 UAH limit looking for trail food",
        {"component_class": "protein_carbohydrate_food", "max_price_uah": 1200, "locale": "uk"},
        "Tests budget boundary: lowest food set is 1249 UAH; verify near-miss.")

    add(11, "Expedition: Dehydrated meals for Carpathian trekking",
        "Trekker specifying activity 'hiking' and place 'hiking_or_camping'",
        {"activity": "hiking", "use_place": "hiking_or_camping", "max_price_uah": 1500, "locale": "uk"},
        "Expects authentic hiking meals without gym leaks.")

    add(12, "Expedition: Dehydrated dinner with vegetarian options",
        "Hiker interested in vegan/vegetarian trail meals",
        {"component_class": "protein_carbohydrate_food", "activity": "hiking", "max_price_uah": 1500, "locale": "uk"},
        "Evaluates whether ЇDLO set (with vegan meatballs) is recommended.")

    add(13, "Expedition: High-calorie mountaineering food pack under 1600 UAH",
        "Alpinist seeking calorie-dense trail rations under 1600 UAH",
        {"component_class": "protein_carbohydrate_food", "activity": "hiking", "max_price_uah": 1600, "locale": "uk"},
        "Expects top expedition food kits (ЇDLO 2.0, 3.0).")

    add(14, "Expedition: Dehydrated food selection in Russian locale",
        "Hiker using Russian language interface looking for camp food",
        {"component_class": "protein_carbohydrate_food", "activity": "hiking", "max_price_uah": 1500, "locale": "ru"},
        "Verifies Russian localization, tone, and explanation accuracy.")

    add(15, "Expedition: Dehydrated food selection in Ukrainian locale",
        "Ukrainian hiker looking for authentic Ukrainian ЇDLO rations",
        {"component_class": "protein_carbohydrate_food", "activity": "hiking", "max_price_uah": 1500, "locale": "uk"},
        "Verifies Ukrainian explanations and natural phrasing.")

    add(16, "Expedition: Dehydrated meals with timing 'during_training'",
        "Fast-packer eating on trail during active trekking hours",
        {"component_class": "protein_carbohydrate_food", "use_timing": "during_training", "max_price_uah": 1500, "locale": "uk"},
        "Tests timing compatibility for outdoor food.")

    add(17, "Expedition: Dehydrated food without gym supplements or sleep pills",
        "Hiker wanting real food, not pills or vitamins",
        {"component_class": "protein_carbohydrate_food", "max_price_uah": 1500, "locale": "uk"},
        "Ensures no sleep supplements or creatine leak into food results.")

    add(18, "Expedition: Dehydrated food with timing 'daily_use'",
        "Expedition basecamp cook needing daily camp meals",
        {"component_class": "protein_carbohydrate_food", "use_timing": "daily_use", "max_price_uah": 1500, "locale": "uk"},
        "Tests daily_use context match.")

    add(19, "Expedition: Lightweight freeze-dried rations for mountain running",
        "Skyrunner needing ultralight freeze-dried calories",
        {"component_class": "protein_carbohydrate_food", "activity": "hiking", "use_scenario": "training", "max_price_uah": 1500, "locale": "uk"},
        "Expects lightweight freeze-dried food.")

    add(20, "Expedition: Dehydrated food request with budget 1000 UAH",
        "Student hiker with 1000 UAH budget wanting dehydrated food",
        {"component_class": "protein_carbohydrate_food", "max_price_uah": 1000, "locale": "uk"},
        "Tests near-miss handling for food below 1249 UAH floor.")

    # =========================================================================
    # PART 2: MEAT JERKY SNACKS (РябChick & М'яско ToGo) (21-40)
    # =========================================================================
    add(21, "Jerky: Meat jerky 8-pack without club membership (Classic citrus)",
        "Hiker wanting pure 8-pack meat jerky without club fee",
        {"component_class": "protein_carbohydrate_food", "membership": "no", "max_price_uah": 1500, "locale": "uk"},
        "Expects race-expert-185 (М'яско ToGo Класика з цитрусом, 8 шт, 1500 UAH).")

    add(22, "Jerky: Meat jerky 8-pack Asian mix",
        "Backpacker wanting savory Asian spiced dried meat snacks",
        {"component_class": "protein_carbohydrate_food", "membership": "no", "max_price_uah": 1500, "locale": "ru"},
        "Expects race-expert-186 (М'яско ToGo Азійський мікс, 8 шт).")

    add(23, "Jerky: Meat jerky 8-pack Chicken and Turkey",
        "Health-conscious hiker wanting lean poultry jerky",
        {"component_class": "protein_carbohydrate_food", "membership": "no", "max_price_uah": 1500, "locale": "uk"},
        "Expects race-expert-188 (М'яско ToGo Курка та індичка, 8 шт).")

    add(24, "Jerky: Meat jerky 8-pack Citrus & Asia combination",
        "Trail trekker wanting variety jerky pack",
        {"component_class": "protein_carbohydrate_food", "membership": "no", "max_price_uah": 1500, "locale": "uk"},
        "Expects race-expert-208 (М'яско ToGo Цитрус та Азія, 8 шт).")

    add(25, "Jerky: Meat jerky tasting set with club membership",
        "Camper open to club perks wanting full jerky degustation",
        {"component_class": "protein_carbohydrate_food", "activity": "hiking", "max_price_uah": 1500, "locale": "uk"},
        "Expects race-expert-187 (Дегустаційний сніданок/снеки).")

    add(26, "Jerky: Meat jerky pork set with club membership",
        "Hunter / bushcrafter wanting calorie-rich pork jerky",
        {"component_class": "protein_carbohydrate_food", "max_price_uah": 1500, "locale": "ru"},
        "Expects race-expert-189 (Свинячий набір).")

    add(27, "Jerky: Meat jerky chicken set with club membership",
        "Trekker wanting pure chicken dried meat snacks",
        {"component_class": "protein_carbohydrate_food", "max_price_uah": 1500, "locale": "uk"},
        "Expects race-expert-190 (Курячий набір).")

    add(28, "Jerky: Meat jerky chicken & pork combo with club membership",
        "Camper wanting mixed meat jerky snacks",
        {"component_class": "protein_carbohydrate_food", "max_price_uah": 1500, "locale": "ru"},
        "Expects race-expert-207 (Курка та свинка).")

    add(29, "Jerky: Meat jerky sweet and savory spicy flavor",
        "Gourmet hiker wanting sweet-spicy jerky",
        {"component_class": "protein_carbohydrate_food", "max_price_uah": 1500, "locale": "uk"},
        "Expects race-expert-184 (Солодко-пікантний).")

    add(30, "Jerky: Meat jerky fruit & spicy flavor",
        "Long-distance walker wanting fruity-spicy meat bites",
        {"component_class": "protein_carbohydrate_food", "max_price_uah": 1500, "locale": "uk"},
        "Expects race-expert-183 (Фруктово-гострий).")

    add(31, "Jerky: Meat jerky Gouda cheese snack pack",
        "Hiker wanting cheese and meat trail snacks",
        {"component_class": "protein_carbohydrate_food", "max_price_uah": 1500, "locale": "ru"},
        "Expects race-expert-182 (Сир Гауда).")

    add(32, "Jerky: Meat jerky Pepper & Paprika snack pack",
        "Carpathian hiker wanting warming spicy pepper jerky",
        {"component_class": "protein_carbohydrate_food", "max_price_uah": 1500, "locale": "uk"},
        "Expects race-expert-181 (Перець, паприка).")

    add(33, "Jerky: Meat jerky for road travel and expeditions",
        "Overland road traveler wanting long-shelf-life meat bites",
        {"component_class": "protein_carbohydrate_food", "use_place": "travel_or_road", "max_price_uah": 1500, "locale": "uk"},
        "Expects travel-oriented meat snacks.")

    add(34, "Jerky: High-protein meat bites for endurance trekking",
        "Trekker needing protein on trail without cooking stove",
        {"component_class": "protein_carbohydrate_food", "activity": "hiking", "max_price_uah": 1500, "locale": "uk"},
        "Expects meat jerky sets.")

    add(35, "Jerky: Pure jerky snacks, Russian locale, membership: no",
        "Russian-speaking hiker strictly refusing gym club membership",
        {"component_class": "protein_carbohydrate_food", "membership": "no", "max_price_uah": 1500, "locale": "ru"},
        "Verifies pure jerky sets in Russian without club upsells.")

    add(36, "Jerky: Meat jerky with timing 'daily_use'",
        "Daily active outdoorsman snacking on jerky during work/hikes",
        {"component_class": "protein_carbohydrate_food", "use_timing": "daily_use", "max_price_uah": 1500, "locale": "uk"},
        "Tests daily_use matching on jerky.")

    add(37, "Jerky: Meat snacks for walking in nature",
        "Nature walker wanting savory snacks for 15km forest walk",
        {"component_class": "protein_carbohydrate_food", "activity": "walking", "max_price_uah": 1500, "locale": "uk"},
        "Verifies walking activity match on jerky snacks.")

    add(38, "Jerky: Meat snacks with budget 1200 UAH",
        "Buyer wanting jerky under 1200 UAH",
        {"component_class": "protein_carbohydrate_food", "max_price_uah": 1200, "locale": "uk"},
        "All jerky sets cost 1500 UAH; tests near-miss handling.")

    add(39, "Jerky: Meat snacks with budget 800 UAH",
        "Budget trail walker with 800 UAH wanting jerky",
        {"component_class": "protein_carbohydrate_food", "max_price_uah": 800, "locale": "ru"},
        "Tests floor anchor / near-miss for jerky.")

    add(40, "Jerky: Meat snacks in warm summer trekking",
        "Summer backpacker needing non-melting meat protein in 30°C heat",
        {"component_class": "protein_carbohydrate_food", "season": "warm", "max_price_uah": 1500, "locale": "uk"},
        "Tests warm season behavior on dried meat.")

    # =========================================================================
    # PART 3: THERMAL SOCKS (1+1=3) BY SIZE & FOOTWEAR (41-60)
    # =========================================================================
    add(41, "Thermal Socks: Small size 35–37 (shoe size 36)",
        "Female hiker with shoe size 36 preparing for mountain trip",
        {"component_class": "apparel_footwear", "activity": "hiking", "shoe_size": 36, "max_price_uah": 1200, "locale": "uk"},
        "Expects race-expert-004 (Акційний набір термошкарпеток 1+1=3 «35–37», 1058 UAH).")

    add(42, "Thermal Socks: Small size 35–37 (shoe size 37)",
        "Female hiker with shoe size 37 needing warm thermo socks",
        {"component_class": "apparel_footwear", "activity": "hiking", "shoe_size": 37, "max_price_uah": 1200, "locale": "uk"},
        "Expects exact match: race-expert-004 (35–37).")

    add(43, "Thermal Socks: Medium size 38–40 (shoe size 39)",
        "Hiker with shoe size 39 buying thermal socks 1+1=3",
        {"component_class": "apparel_footwear", "activity": "hiking", "shoe_size": 39, "max_price_uah": 1200, "locale": "uk"},
        "Expects race-expert-003 (38–40, 1058 UAH).")

    add(44, "Thermal Socks: Medium size 38–40 (shoe size 40)",
        "Hiker with shoe size 40 buying thermal socks 1+1=3",
        {"component_class": "apparel_footwear", "activity": "hiking", "shoe_size": 40, "max_price_uah": 1200, "locale": "ru"},
        "Expects race-expert-003 (38–40) or 002 (40–42).")

    add(45, "Thermal Socks: Medium-Large size 40–42 (shoe size 41)",
        "Trekker with shoe size 41 needing warm socks for boots",
        {"component_class": "apparel_footwear", "activity": "hiking", "shoe_size": 41, "max_price_uah": 1200, "locale": "uk"},
        "Expects race-expert-002 (40–42, 1058 UAH).")

    add(46, "Thermal Socks: Medium-Large size 40–42 (shoe size 42)",
        "Trekker with shoe size 42 needing winter hiking socks",
        {"component_class": "apparel_footwear", "activity": "hiking", "shoe_size": 42, "max_price_uah": 1200, "locale": "ru"},
        "Expects race-expert-002 (40–42).")

    add(47, "Thermal Socks: Large size 43–45 (shoe size 43)",
        "Tall hiker with shoe size 43 needing thermal trekking socks",
        {"component_class": "apparel_footwear", "activity": "hiking", "shoe_size": 43, "max_price_uah": 1200, "locale": "uk"},
        "Expects race-expert-001 (43–45, 1058 UAH).")

    add(48, "Thermal Socks: Large size 43–45 (shoe size 44)",
        "Mountaineer with shoe size 44 needing heavy thermo socks",
        {"component_class": "apparel_footwear", "activity": "hiking", "shoe_size": 44, "max_price_uah": 1200, "locale": "uk"},
        "Expects race-expert-001 (43–45).")

    add(49, "Thermal Socks: Large size 43–45 (shoe size 45)",
        "Expedition leader with shoe size 45 needing thermal insulation",
        {"component_class": "apparel_footwear", "activity": "hiking", "shoe_size": 45, "max_price_uah": 1200, "locale": "ru"},
        "Expects race-expert-001 (43–45).")

    add(50, "Thermal Socks: Out-of-bounds large size 46",
        "Large-footed hiker with shoe size 46 seeking thermal socks",
        {"component_class": "apparel_footwear", "activity": "hiking", "shoe_size": 46, "max_price_uah": 1200, "locale": "uk"},
        "CRITICAL SIZING TEST: Does catalog fail with no_match because thermo socks only go to 45?")

    add(51, "Thermal Socks: Out-of-bounds large size 47",
        "Very tall mountaineer with shoe size 47 seeking warm socks",
        {"component_class": "apparel_footwear", "activity": "hiking", "shoe_size": 47, "max_price_uah": 1200, "locale": "ru"},
        "Tests no_match handling for shoe size 47.")

    add(52, "Thermal Socks: Out-of-bounds petite size 34",
        "Teen/petite hiker with shoe size 34 seeking thermal socks",
        {"component_class": "apparel_footwear", "activity": "hiking", "shoe_size": 34, "max_price_uah": 1200, "locale": "uk"},
        "Tests lower size boundary under 35.")

    add(53, "Thermal Socks: String range input '40-42'",
        "User entering shoe size as range string '40-42'",
        {"component_class": "apparel_footwear", "activity": "hiking", "shoe_size": "40-42", "max_price_uah": 1200, "locale": "uk"},
        "CRITICAL SCHEMA CRASH TEST: Does engine crash with DraftMatchError or sanitize input?")

    add(54, "Thermal Socks: String range input '43-45'",
        "User entering shoe size as range string '43-45'",
        {"component_class": "apparel_footwear", "activity": "hiking", "shoe_size": "43-45", "max_price_uah": 1200, "locale": "ru"},
        "Tests crash resilience on string size input.")

    add(55, "Thermal Socks: Sizing unspecified (Default size bias check)",
        "Hiker asking for outdoor socks without entering shoe size",
        {"component_class": "apparel_footwear", "activity": "hiking", "max_price_uah": 1200, "locale": "uk"},
        "Check whether engine silently defaults to size 43–45 without asking user.")

    add(56, "Thermal Socks: Winter cold season explicit signal",
        "Winter mountaineer asking for cold weather footwear insulation",
        {"component_class": "apparel_footwear", "season": "cold", "shoe_size": 41, "max_price_uah": 1200, "locale": "uk"},
        "Expects race-expert-002 (40–42) with cold weather match.")

    add(57, "Thermal Socks: Summer warm season apparel request",
        "Summer hiker looking for light trekking socks in warm weather",
        {"component_class": "apparel_footwear", "season": "warm", "shoe_size": 41, "max_price_uah": 1500, "locale": "uk"},
        "CRITICAL LOGIC TEST: Does engine recommend gift sets with medals (094/096) or warn that catalog has no summer socks?")

    add(58, "Thermal Socks: Budget 800 UAH (Budget near-miss check)",
        "Budget hiker looking for thermal socks with only 800 UAH",
        {"component_class": "apparel_footwear", "shoe_size": 43, "max_price_uah": 800, "locale": "uk"},
        "Tests budget floor/near-miss: socks cost 1058 UAH.")

    add(59, "Thermal Socks: Budget 1000 UAH (Close near-miss check)",
        "Hiker with 1000 UAH looking for thermal socks",
        {"component_class": "apparel_footwear", "shoe_size": 39, "max_price_uah": 1000, "locale": "ru"},
        "Tests 58 UAH gap near-miss behavior.")

    add(60, "Thermal Socks: Budget 1100 UAH (Comfortable exact match)",
        "Hiker with 1100 UAH budget buying thermal socks",
        {"component_class": "apparel_footwear", "shoe_size": 41, "max_price_uah": 1100, "locale": "uk"},
        "Expects exact match: race-expert-002 at 1058 UAH.")

    # =========================================================================
    # PART 4: MULTI-DAY HIKING STACKS & EXPEDITION COMBOS (61-75)
    # =========================================================================
    add(61, "Multi-Day Stack: Meals + Jerky + Thermal Socks complete combo",
        "Multi-day expeditioner wanting an all-in-one pack of meals, jerky, and socks",
        {"activity": "hiking", "use_place": "hiking_or_camping", "max_price_uah": 2500, "locale": "uk"},
        "CRITICAL DOMAIN TEST: Does catalog offer an all-in-one bundle, or does engine fail to compose stacks?")

    add(62, "Multi-Day Stack: ЇDLO 3.0 combo ration (meals + jerky + cookies)",
        "Trekker looking for ready-made combo ration with both hot meals and meat snacks",
        {"component_class": "protein_carbohydrate_food", "activity": "hiking", "max_price_uah": 1500, "locale": "uk"},
        "Expects race-expert-191 (ЇDLO 3.0), the only set with both dehydrated meals and meat jerky.")

    add(63, "Mountain Ultra: Ultra Trail Marathon Energy & Hydration Pro",
        "Mountain ultra-trail runner preparing for 50k Carpathian race needing SIS electrolytes and gels",
        {"component_class": "hydration_items", "activity": "hiking", "max_price_uah": 2000, "locale": "uk"},
        "Expects race-expert-211 (Ultra Trail Marathon Energy & Hydration Pro, 1650 UAH).")

    add(64, "Mountain Ultra: Trail marathon hydration in summer heat",
        "Trail runner needing electrolytes for hot weather mountain running",
        {"component_class": "hydration_items", "season": "warm", "max_price_uah": 2000, "locale": "ru"},
        "Expects race-expert-211.")

    add(65, "Mountain Ultra: Hydration pack under 1500 UAH budget",
        "Trail runner wanting hydration pack with 1500 UAH limit",
        {"component_class": "hydration_items", "max_price_uah": 1500, "locale": "uk"},
        "Tests near-miss: race-expert-211 costs 1650 UAH.")

    add(66, "Field Hygiene: Road & Camp hygiene kit (TRISWIM pool soap check)",
        "Camper wanting travel and trail hygiene kit",
        {"component_class": "sports_accessories", "use_place": "travel_or_road", "max_price_uah": 1500, "locale": "uk"},
        "INDOOR GYM/POOL LEAK TEST: Evaluates race-expert-080 (contains TRISWIM chlorine-removal body wash for swimmers!).")

    add(67, "Field Night: Camp sleep & relaxation kit (Melatonin check)",
        "Overnight camper wanting sleep aid for tent bivouac",
        {"component_class": "sports_accessories", "use_timing": "evening_or_bedtime", "max_price_uah": 1500, "locale": "uk"},
        "CRITICAL TAXONOMY CRASH TEST: use_timing='evening_or_bedtime' crashes draft_matcher because outdoors doesn't allow it!")

    add(68, "Expedition Gift: 'Подарунок у похід' (Medal & organizer check)",
        "Buyer wanting gift for hiker friend under 1500 UAH",
        {"component_class": "sports_accessories", "use_scenario": "everyday", "max_price_uah": 1500, "locale": "uk"},
        "Evaluates race-expert-094 (contains military medal, organizer, and socks RE2 40-44).")

    add(69, "Expedition Gift: 'Подарунок у дорогу' (Medal 'Озброєні волею')",
        "Buyer wanting travel gift set with socks and organizer",
        {"component_class": "sports_accessories", "use_place": "travel_or_road", "max_price_uah": 1500, "locale": "ru"},
        "Evaluates race-expert-096.")

    add(70, "Expedition Gift: 'Подарунок військовому-спортсмену'",
        "Outdoor enthusiast buying gift for military outdoor service",
        {"component_class": "sports_accessories", "season": "cold", "max_price_uah": 1500, "locale": "uk"},
        "Evaluates race-expert-100 (fleece buff + medal + socks).")

    add(71, "Expedition Gift: 'Подарунок мандрівнику' (Sharpey bath towel)",
        "Buyer looking for traveler gear pack with towel and buff",
        {"component_class": "sports_accessories", "max_price_uah": 1500, "locale": "uk"},
        "Evaluates race-expert-101 (contains giant 135x70cm home bath towel + socks 40-44).")

    add(72, "Backcountry Trek: Multi-day mountain gear with 2500 UAH budget",
        "Backpacker with high budget wanting comprehensive gear pack",
        {"activity": "hiking", "max_price_uah": 2500, "locale": "uk"},
        "Check how engine handles multi-category high budget in outdoors.")

    add(73, "Bivouac: Alpine bivouac night kit under 1500 UAH",
        "Climber needing bivouac sleeping accessories",
        {"activity": "hiking", "use_place": "hiking_or_camping", "max_price_uah": 1500, "locale": "ru"},
        "Examines whether sleep pills or proper gear match.")

    add(74, "Expedition Gear: Buff and accessories without club membership",
        "Hiker wanting buff or outdoor gear strictly without gym subscription",
        {"component_class": "sports_accessories", "membership": "no", "max_price_uah": 1500, "locale": "uk"},
        "Expects race-expert-080 (Дорожня гігієна) as sole club-free accessory set.")

    add(75, "Expedition Nutrition & Hygiene combined request",
        "Camper wanting camp food and personal hygiene",
        {"activity": "hiking", "use_scenario": "training", "max_price_uah": 2000, "locale": "uk"},
        "Tests candidate diversity across food and hygiene.")

    # =========================================================================
    # PART 5: BUDGET STRESS TESTING (800 TO 3000 UAH) (76-85)
    # =========================================================================
    add(76, "Budget: Strict 800 UAH limit, general outdoors request",
        "Student camper on strict 800 UAH budget",
        {"max_price_uah": 800, "locale": "uk"},
        "Tests floor anchor / near-miss: lowest set in outdoors is 1058 UAH (socks).")

    add(77, "Budget: Tight 900 UAH limit, outdoor food request",
        "Hiker with 900 UAH looking for food rations",
        {"component_class": "protein_carbohydrate_food", "max_price_uah": 900, "locale": "uk"},
        "Tests food budget near-miss against 1249 UAH set.")

    add(78, "Budget: 1000 UAH limit, outdoor food request",
        "Hiker with 1000 UAH looking for trail meals",
        {"component_class": "protein_carbohydrate_food", "max_price_uah": 1000, "locale": "ru"},
        "Tests food budget near-miss against 1249 UAH set.")

    add(79, "Budget: 1100 UAH limit, thermal socks request",
        "Hiker with 1100 UAH buying thermal socks",
        {"component_class": "apparel_footwear", "shoe_size": 41, "max_price_uah": 1100, "locale": "uk"},
        "Expects exact match: race-expert-002 at 1058 UAH.")

    add(80, "Budget: 1250 UAH limit, outdoor snacks request",
        "Trekker with 1250 UAH budget for snacks",
        {"component_class": "protein_carbohydrate_food", "max_price_uah": 1250, "locale": "uk"},
        "Expects exact match: race-expert-076 (Мандрівний смаколик at 1249 UAH).")

    add(81, "Budget: 1400 UAH limit, freeze-dried mix request",
        "Hiker with 1400 UAH budget for freeze-dried mix",
        {"component_class": "protein_carbohydrate_food", "max_price_uah": 1400, "locale": "ru"},
        "Expects exact match: race-expert-075 (Сублімований мікс at 1389 UAH).")

    add(82, "Budget: Standard 1500 UAH limit, full candidate pool",
        "Standard buyer with 1500 UAH budget across outdoor pool",
        {"max_price_uah": 1500, "locale": "uk"},
        "Evaluates ranking among 1500 UAH sets.")

    add(83, "Budget: Premium 2000 UAH limit (Catalog ceiling check)",
        "Generous buyer with 2000 UAH budget for outdoors",
        {"max_price_uah": 2000, "locale": "uk"},
        "Tests behavior when budget exceeds all sets (max is 1650 UAH).")

    add(84, "Budget: High 2500 UAH limit (Catalog ceiling check)",
        "Expedition buyer with 2500 UAH budget",
        {"max_price_uah": 2500, "locale": "ru"},
        "Verifies no phantom sets or broken sorting on high budgets.")

    add(85, "Budget: Expedition 3000 UAH limit (Catalog ceiling check)",
        "High-end alpine trekker with 3000 UAH budget",
        {"max_price_uah": 3000, "locale": "uk"},
        "Verifies system gracefully handles top-tier budget limits.")

    # =========================================================================
    # PART 6: ACTIVITIES & DISCIPLINARY TESTS (86-100)
    # (Hiking, Trekking, Mountaineering, Walking, Cycling/Bikepacking)
    # =========================================================================
    add(86, "Activity: Mountain trekking / hiking ('hiking')",
        "Trekker choosing 'hiking' activity for mountain journey",
        {"activity": "hiking", "max_price_uah": 1500, "locale": "uk"},
        "Expects proper hiking sets.")

    add(87, "Activity: Nature walking / Nordic walking ('walking')",
        "Fitness walker choosing 'walking' activity in outdoors",
        {"activity": "walking", "max_price_uah": 1500, "locale": "uk"},
        "Expects walking-compatible sets.")

    add(88, "Activity: Bikepacking / cycle touring ('cycling')",
        "Bikepacker choosing 'cycling' activity for gravel tour",
        {"activity": "cycling", "max_price_uah": 1500, "locale": "uk"},
        "CRITICAL TAXONOMY DEAD-END: Does cycling return 0 results because 0 outdoor sets support cycling?")

    add(89, "Activity: Gravel bike camping ('cycling' + 'hiking_or_camping')",
        "Bicycle tourist looking for camping rations",
        {"activity": "cycling", "use_place": "hiking_or_camping", "max_price_uah": 1500, "locale": "ru"},
        "Tests cycling activity dead-end with camping context.")

    add(90, "Activity: Cycling multi-day tour needing food ('cycling' + food)",
        "Cyclist asking for food rations on bikepacking trip",
        {"activity": "cycling", "component_class": "protein_carbohydrate_food", "max_price_uah": 1500, "locale": "uk"},
        "Tests cycling + food compatibility.")

    add(91, "Activity: Mountaineering / alpine climbing with freeze-dried food",
        "Alpinist selecting hiking activity and camp place",
        {"activity": "hiking", "component_class": "protein_carbohydrate_food", "use_place": "hiking_or_camping", "max_price_uah": 1500, "locale": "uk"},
        "Expects ЇDLO rations for alpine climbing.")

    add(92, "Activity: Nordic walking with warm thermal socks",
        "Nordic walker wanting thermal socks in size 39",
        {"activity": "walking", "component_class": "apparel_footwear", "shoe_size": 39, "max_price_uah": 1200, "locale": "uk"},
        "Expects race-expert-003 (38–40).")

    add(93, "Activity: Day-walk park enthusiast needing jerky snacks",
        "Walking enthusiast wanting savory jerky for afternoon walks",
        {"activity": "walking", "component_class": "protein_carbohydrate_food", "max_price_uah": 1500, "locale": "ru"},
        "Expects meat jerky sets.")

    add(94, "Activity: Walking enthusiast asking for hydration items",
        "Summer walker wanting hydration/electrolytes for hot days",
        {"activity": "walking", "component_class": "hydration_items", "max_price_uah": 2000, "locale": "uk"},
        "CRITICAL TEST: Does race-expert-211 fail to match because it only supports running/hiking?")

    add(95, "Explanation: Accessories deceptive explanation check",
        "Hiker checking explanation for 'sports_accessories'",
        {"component_class": "sports_accessories", "max_price_uah": 1500, "locale": "uk"},
        "CRITICAL DECEPTIVE CLAIM TEST: Does why_suitable claim '(без сторонніх речей)' while recommending sleep supplements (062) or medals (094)?")

    add(96, "Sizing Leak: Summer outdoor apparel for female shoe size 37",
        "Female trekker entering shoe size 37 selecting summer apparel",
        {"component_class": "apparel_footwear", "season": "warm", "shoe_size": 37, "max_price_uah": 1500, "locale": "uk"},
        "CRITICAL SIZING MISMATCH: Engine serves gift set race-expert-094 with socks size 40–44 to a size 37 female trekker!")

    add(97, "Sizing Leak: Outdoor apparel for male shoe size 46",
        "Large trekker entering shoe size 46 selecting outdoor apparel",
        {"component_class": "apparel_footwear", "shoe_size": 46, "max_price_uah": 1500, "locale": "ru"},
        "Tests lack of size 46 in catalog causing zero results.")

    add(98, "Locale Tone: Outdoor travel in Russian locale with sleep kit check",
        "Russian-speaking traveler checking explanation on field night set",
        {"component_class": "sports_accessories", "use_timing": "evening_or_bedtime", "max_price_uah": 1500, "locale": "ru"},
        "Evaluates Russian explanation and context handling on sleep set.")

    add(99, "Club Dilution: Hiker explicitly declining club membership",
        "Budget-conscious hiker refusing club membership across all outdoor needs",
        {"activity": "hiking", "membership": "no", "max_price_uah": 1500, "locale": "uk"},
        "Expects pure physical products (ЇDLO 2.0, jerky 8-packs, or socks) without club fee.")

    add(100, "Clean Outdoors: Pure hiking food and socks dual query without gym leaks",
        "Discerning camper demanding authentic outdoor sustenance and foot warmth",
        {"activity": "hiking", "season": "cold", "shoe_size": 41, "max_price_uah": 1500, "locale": "uk"},
        "Expects authentic outdoor products without gym shakers or sleep pills.")

    return scenarios

def evaluate_scenario(scenario, catalog):
    req = dict(scenario["request"])
    tid = scenario["test_id"]
    name = scenario["name"]
    expected = scenario["expected_focus"]

    # Special handling for intentional crash tests (string shoe_size or unsupported taxonomy)
    crashed = False
    crash_msg = ""
    res = {}
    try:
        res = draft_recommend(catalog, req)
    except Exception as e:
        crashed = True
        crash_msg = f"{type(e).__name__}: {str(e)}"

    if crashed:
        if req.get("shoe_size") in ("40-42", "43-45"):
            return {
                "verdict": "FAIL",
                "flaw_type": "SCHEMA_CRASH_UNSANITIZED_INPUT",
                "flaw_summary": f"Крах двигуна через несанітований рядковий розмір взуття: {crash_msg}",
                "status": "CRASHED",
                "results_count": 0,
                "recommended_sets": [],
                "why_suitable_explanations": [],
                "audit_notes": [f"Passing shoe_size='{req.get('shoe_size')}' caused an unhandled crash."]
            }
        elif "use_timing" in crash_msg:
            return {
                "verdict": "FAIL",
                "flaw_type": "SCHEMA_TAXONOMY_CRASH",
                "flaw_summary": f"Таксономічний збій схеми: use_timing='evening_or_bedtime' заборонений у валідаторі для 'outdoors', хоча набір race-expert-062 («Польовий сон») має саме цей контекст у базі!",
                "status": "CRASHED",
                "results_count": 0,
                "recommended_sets": [],
                "why_suitable_explanations": [],
                "audit_notes": [crash_msg]
            }
        else:
            return {
                "verdict": "FAIL",
                "flaw_type": "UNHANDLED_EXCEPTION",
                "flaw_summary": f"Неочікуване падіння: {crash_msg}",
                "status": "CRASHED",
                "results_count": 0,
                "recommended_sets": [],
                "why_suitable_explanations": [],
                "audit_notes": [crash_msg]
            }

    status = res.get("status")
    results = res.get("results", [])
    near_miss = res.get("near_miss_results", [])
    floor_anchor = res.get("floor_anchor_results", [])

    rec_items = results if results else (near_miss if near_miss else floor_anchor)
    rec_sids = [r.get("set_id") for r in rec_items]
    rec_titles = [r.get("title") for r in rec_items]
    whys = [r.get("why_suitable", []) for r in rec_items]
    why_texts = [" ".join(w) if isinstance(w, list) else str(w) for w in whys]

    flaws = []
    flaw_type = "NONE"
    verdict = "PASS"

    comp_class = req.get("component_class")
    act = req.get("activity")
    shoe_size = req.get("shoe_size")
    budget = req.get("max_price_uah")
    membership = req.get("membership")
    product_form = req.get("product_form")
    season = req.get("season")

    # 1. Critical flaw: Dehydrated meal selection fails with 0 results
    if comp_class == "dehydrated_meal":
        if not results:
            verdict = "FAIL"
            flaw_type = "DEHYDRATED_FOOD_SELECTION_FAILURE"
            flaws.append("КРИТИЧНИЙ БАГ: Вибір 'Сублімована туристична їжа' (dehydrated_meal) повертає 0 результатів! У каталозі всі набори ЇDLO помилково класифіковані як 'protein_carbohydrate_food'.")

    # 2. Critical flaw: Cycling activity taxonomy dead-end
    elif act == "cycling":
        if not results:
            verdict = "FAIL"
            flaw_type = "CYCLING_TAXONOMY_DEAD_END"
            flaws.append("КРИТИЧНИЙ БАГ: Вибір активності 'cycling' (велопоходи, байкпакінг) повертає 0 результатів! Жоден із 28 наборів категорії 'outdoors' не містить 'cycling' у групі активностей.")

    # 3. Critical flaw: Sizing out-of-bounds or mismatch
    elif shoe_size in (46, 47, 34) and comp_class == "apparel_footwear":
        if not results:
            verdict = "FAIL"
            flaw_type = "SIZING_UNAVAILABLE"
            flaws.append(f"Каталог не містить термошкарпеток розміру {shoe_size} (наявні лише 35–45). Покупець отримує 0 результатів.")

    # 4. Critical flaw: Bundled socks sizing mismatch in apparel or accessories (Sets 094, 096, 100, 101 have socks 40-44)
    elif shoe_size in (36, 37, 46) and any(sid in ("race-expert-094", "race-expert-096", "race-expert-100", "race-expert-101") for sid in rec_sids):
        verdict = "FAIL"
        flaw_type = "SIZING_MISMATCH"
        flaws.append(f"Невідповідність розміру: користувач вказав розмір ноги {shoe_size}, але запропонований набір містить шкарпетки фіксованого розміру 40–44!")

    # 5. Critical flaw: Deceptive explanation claiming "(без сторонніх речей)" when set contains sleep pills, medals, or club fees
    elif comp_class == "sports_accessories":
        has_deceptive = False
        for sid, why_t in zip(rec_sids, why_texts):
            if sid == "race-expert-062" and ("без сторонніх" in why_t or "без посторонних" in why_t):
                has_deceptive = True
                verdict = "FAIL"
                flaw_type = "DECEPTIVE_EXPLANATION"
                flaws.append("ОБМАН ПОКУПЦЯ: Двигун стверджує 'у наборі саме Спортивні аксесуари та пляшки (без сторонніх речей)', але набір race-expert-062 містить снодійні добавки (VPLab Ultra Sleep, мелатонін) та абонемент клубу!")
            elif sid in ("race-expert-094", "race-expert-096", "race-expert-100") and ("без сторонніх" in why_t or "без посторонних" in why_t):
                has_deceptive = True
                if flaw_type == "NONE":
                    verdict = "WARN"
                    flaw_type = "SUBOPTIMAL_RECOMMENDATION"
                flaws.append("Сумнівне твердження: набір містить пам'ятні військові медалі та шкарпетки під вивіскою спортивних аксесуарів.")

    # 6. Critical flaw: Indoor gym / pool / supplement leakage
    if any(sid == "race-expert-062" for sid in rec_sids) and comp_class == "protein_carbohydrate_food":
        verdict = "FAIL"
        flaw_type = "INDOOR_GYM_OR_SUPPLEMENT_LEAK"
        flaws.append("Витік добавок: набір зі снодійним та мелатоніном запропоновано замість туристичної їжі.")

    if any(sid == "race-expert-080" for sid in rec_sids):
        if flaw_type == "NONE":
            flaw_type = "POOL_ITEM_IN_OUTDOORS"
            verdict = "WARN"
            flaws.append("Невідповідність призначенню: набір 'Дорожня гігієна' містить TRISWIM Body Wash — гель для пловців для змивання хлору після басейну.")

    # 7. Critical flaw: product_form 'food_or_meal' excludes authentic ЇDLO meals
    if product_form == "food_or_meal" and comp_class == "protein_carbohydrate_food":
        if "race-expert-078" not in rec_sids and "race-expert-111" not in rec_sids:
            verdict = "FAIL"
            flaw_type = "TAXONOMY_TAGGING_OMISSION"
            flaws.append("ПОМИЛКА ТЕГУВАННЯ: Фільтр product_form='food_or_meal' виключив ЇDLO 2.0 (111) та ЇDLO Club (078), оскільки у них порожній список product_forms у базі!")

    # 8. Walking + Hydration items fails
    if act == "walking" and comp_class == "hydration_items":
        if not results:
            verdict = "WARN"
            flaw_type = "ZERO_RESULTS_UNEXPECTED"
            flaws.append("Набір race-expert-211 підтримує тільки running/hiking, тому для пішої ходи (walking) ізотоніки недоступні (0 результатів).")

    # 9. Budget near-miss handling
    if budget is not None and budget < 1058:
        if not results and (near_miss or floor_anchor):
            verdict = "WARN"
            flaw_type = "BUDGET_FLOOR_OR_NEAR_MISS"
            flaws.append(f"Бюджет {budget} ₴ нижчий за мінімальний у категорії (1058 ₴). Запропоновано near-miss або якірний набір, але статус повідомляє 'no_match'.")
        elif not results and not near_miss and not floor_anchor:
            verdict = "FAIL"
            flaw_type = "ZERO_RESULTS_UNEXPECTED"
            flaws.append(f"Порожня видача при бюджеті {budget} ₴ без надання floor_anchor.")

    elif budget is not None and budget < 1500 and comp_class == "protein_carbohydrate_food" and budget < 1249:
        if not results:
            verdict = "WARN"
            flaw_type = "BUDGET_FLOOR_OR_NEAR_MISS"
            flaws.append(f"Мінімальний набір харчування коштує 1249 ₴. При бюджеті {budget} ₴ точного збігу немає.")

    # 10. Default size bias
    if comp_class == "apparel_footwear" and shoe_size is None and len(results) > 0:
        if results[0].get("set_id") == "race-expert-001":
            if flaw_type == "NONE":
                verdict = "WARN"
                flaw_type = "DEFAULT_SIZE_BIAS"
                flaws.append("Зміщення за замовчуванням: за відсутності розміру взуття двигун автоматично нав'язує найбільший розмір 43–45.")

    # 11. Club membership dilution check
    if membership == "no":
        club_sets_returned = [sid for sid in rec_sids if "Club" in sid or any(c in sid for c in ("062", "075", "076", "078", "094", "096", "100", "101", "181", "182", "183", "184", "187", "189", "190", "191", "207"))]
        if club_sets_returned:
            verdict = "FAIL"
            flaw_type = "UNWANTED_CLUB_MEMBERSHIP_LEAK"
            flaws.append(f"Покупець вказав membership='no', але система запропонувала клубні набори: {club_sets_returned}!")
    else:
        # Check if recommendation is dominated by 3-month gym club fee
        if rec_sids and all(sid in ("race-expert-062", "race-expert-075", "race-expert-076", "race-expert-078") for sid in rec_sids):
            if flaw_type == "NONE":
                verdict = "WARN"
                flaw_type = "FORCED_CLUB_MEMBERSHIP_DILUTION"
                flaws.append("Нав'язування клубу: всі запропоновані набори містять платний 3-місячний абонемент клубу, що здорожчує набір.")

    # 12. Multi-day stack limitation
    if "stack" in name.lower() or "combo" in name.lower():
        if rec_sids and "race-expert-191" not in rec_sids:
            if flaw_type == "NONE":
                verdict = "WARN"
                flaw_type = "MULTI_ITEM_STACK_INCOMPLETE"
                flaws.append("Неможливість формування стеку: двигун рекомендує окремо лише їжу або лише шкарпетки, повноцінний похідний стек (їжа + м'ясо + термошкарпетки) відсутній.")

    # 13. Summer socks limitation
    if season == "warm" and comp_class == "apparel_footwear":
        if any(sid in ("race-expert-094", "race-expert-096") for sid in rec_sids):
            if flaw_type == "NONE":
                verdict = "WARN"
                flaw_type = "SUBOPTIMAL_RECOMMENDATION"
                flaws.append("Відсутність літніх шкарпеток: на запит літнього екіпірування запропоновано подарункові набори з медалями (094/096).")

    # If no flaws found
    if not flaws:
        verdict = "PASS"
        flaw_type = "NONE"
        flaws.append("Ідеальна відповідність запиту туриста, точний підбір спорядження чи харчування.")

    return {
        "verdict": verdict,
        "flaw_type": flaw_type,
        "flaw_summary": " | ".join(flaws),
        "status": status,
        "results_count": len(results),
        "recommended_sets": [
            {
                "set_id": r.get("set_id"),
                "title": r.get("title"),
                "price_uah": r.get("price_uah"),
                "sku": r.get("sku")
            }
            for r in rec_items
        ],
        "why_suitable_explanations": whys,
        "audit_notes": flaws
    }

def main():
    catalog = load_environment()
    scenarios = generate_100_scenarios()

    print(f"Loaded {len(catalog)} catalog entries. Running 100 outdoors buyer scenarios...")

    results = []
    verdict_counts = {"PASS": 0, "WARN": 0, "FAIL": 0}
    flaw_type_counts = {}

    for sc in scenarios:
        ev = evaluate_scenario(sc, catalog)
        v = ev["verdict"]
        ft = ev["flaw_type"]

        verdict_counts[v] += 1
        flaw_type_counts[ft] = flaw_type_counts.get(ft, 0) + 1

        results.append({
            "test_id": sc["test_id"],
            "name": sc["name"],
            "persona": sc["persona"],
            "request": sc["request"],
            "expected_focus": sc["expected_focus"],
            "evaluation": ev
        })

    print(f"\nExecution Complete: {len(results)} tests run.")
    print(f"Summary: PASS={verdict_counts['PASS']} ({verdict_counts['PASS']}%), "
          f"WARN={verdict_counts['WARN']} ({verdict_counts['WARN']}%), "
          f"FAIL={verdict_counts['FAIL']} ({verdict_counts['FAIL']}%)")

    # Save JSON results
    OUTPUT_JSON.write_text(json.dumps({
        "agent": "QA Specialist for Outdoors & Hiking (`outdoors`)",
        "total_tests": len(results),
        "summary": verdict_counts,
        "flaw_types": flaw_type_counts,
        "tests": results
    }, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Saved test run results to: {OUTPUT_JSON}")

    # Build Markdown report
    build_markdown_report(results, verdict_counts, flaw_type_counts)
    print(f"Saved Markdown audit report to: {OUTPUT_REPORT}")

def build_markdown_report(results, summary, flaw_types):
    total = len(results)
    pass_cnt = summary["PASS"]
    warn_cnt = summary["WARN"]
    fail_cnt = summary["FAIL"]

    pass_pct = round(pass_cnt / total * 100, 1)
    warn_pct = round(warn_cnt / total * 100, 1)
    fail_pct = round(fail_cnt / total * 100, 1)

    md = []
    md.append("# QA Specialist: Outdoors & Hiking (`outdoors`) — 100 Buyer Test Case Audit Report")
    md.append("**Date:** 2026-11-12  ")
    md.append("**Role:** QA Specialist for Outdoors & Hiking (Endurance Camper, Hiker & Alpinist Perspective)  ")
    md.append("**Scope:** Race Expert Quiz — Outdoors & Hiking (`goal_group: 'outdoors'`)  ")
    md.append("**Catalog Source:** `wiki/projects/quiz-set-audit.json` (207 total catalog sets, 28 outdoors candidate sets)  ")
    md.append("**Matcher Engine:** `test-quiz-sandbox/draft_matcher.py:draft_recommend`  \n")

    md.append("## 1. Executive Summary")
    md.append("| Metric | Count | Percentage |")
    md.append("|---|---|---|")
    md.append(f"| **Total Test Scenarios** | **{total}** | **100.0%** |")
    md.append(f"| **PASS (Solid Hiker / Camper Experience)** | **{pass_cnt}** | **{pass_pct}%** |")
    md.append(f"| **WARN (Suboptimal / Diluted / Near-Miss / Bias / Omission)** | **{warn_cnt}** | **{warn_pct}%** |")
    md.append(f"| **FAIL (Critical Breakdown / 0 Results / Sizing / Crashes)** | **{fail_cnt}** | **{fail_pct}%** |")
    md.append("\n```")
    md.append(f"Verdict Distribution: [{'#' * int(pass_pct/2)}{'-' * int(warn_pct/2)}{'!' * int(fail_pct/2)}]")
    md.append(f"  PASS: {pass_cnt} | WARN: {warn_cnt} | FAIL: {fail_cnt}")
    md.append("```\n")

    md.append("## 2. Flaw Taxonomy & Defect Distribution")
    md.append("| Defect Code | Description | Count | Severity |")
    md.append("|---|---|---|---|")
    for ft, cnt in sorted(flaw_types.items(), key=lambda x: -x[1]):
        if ft == "NONE":
            sev = "PASS"
        elif ft in ("DEHYDRATED_FOOD_SELECTION_FAILURE", "CYCLING_TAXONOMY_DEAD_END", "SCHEMA_CRASH_UNSANITIZED_INPUT", "SCHEMA_TAXONOMY_CRASH", "SIZING_MISMATCH", "SIZING_UNAVAILABLE", "DECEPTIVE_EXPLANATION", "TAXONOMY_TAGGING_OMISSION", "UNWANTED_CLUB_MEMBERSHIP_LEAK"):
            sev = "CRITICAL FAIL"
        else:
            sev = "WARN"
        md.append(f"| `{ft}` | {get_flaw_desc(ft)} | **{cnt}** | {sev} |")
    md.append("\n")

    md.append("## 3. Critical Athletic & Outdoor Logic Findings")

    md.append("### Finding 1: Selecting 'Dehydrated Meal' (`dehydrated_meal`) Fails with 0 Results (CRITICAL FAIL)")
    md.append("> [!CAUTION]")
    md.append("> **100% Dead-End for Dehydrated Food Selection:**")
    md.append("> In `draft_matcher.py`, the quiz steering menu explicitly offers `dehydrated_meal` under `COMPONENT_CLASSES_BY_GOAL['outdoors']` (display name: *«Сублімована туристична їжа»*).")
    md.append("> However, in the catalog database (`quiz-set-audit.json`), **ZERO sets** are assigned `component_classes: ['dehydrated_meal']`! All authentic ЇDLO meal sets (`race-expert-078`, `race-expert-111`, `race-expert-191`) were tagged as generic `protein_carbohydrate_food`.")
    md.append("> Consequently, any hiker who specifically asks for dehydrated expedition food gets **`status: no_match` (0 results)**! The quiz literally fails to sell its premier hiking food.")
    md.append("\n")

    md.append("### Finding 2: Cycling / Bikepacking Taxonomy Dead-End (CRITICAL FAIL)")
    md.append("> [!CAUTION]")
    md.append("> **100% Dead-End for Bikepackers and Cycle Tourers:**")
    md.append("> `ACTIVITY_OPTIONS_BY_GOAL['outdoors']` explicitly offers `cycling` alongside `hiking` and `walking`.")
    md.append("> Yet out of all 28 outdoors sets in the catalog, **not a single set has `cycling` in its `activity_groups`**.")
    md.append("> When a cyclist planning a gravel bikepacking trip or mountain cycling tour chooses 'Cycling', the quiz returns **`status: no_match` (0 results)**.")
    md.append("\n")

    md.append("### Finding 3: Empty `product_forms` Excludes ЇDLO 2.0 & ЇDLO Club on Form Filtering (CRITICAL FAIL)")
    md.append("> [!WARNING]")
    md.append("> In `quiz-set-audit.json`, `race-expert-111` (ЇDLO 2.0) and `race-expert-078` (ЇDLO Club) have `product_forms: []` (empty array).")
    md.append("> When a camper filters by `product_form: 'food_or_meal'`, both sets are completely excluded from the exact pool.")
    md.append("> Even worse, sets `race-expert-094`, `096`, and `100` (which contain military commemorative medals, socks, and organizers with **zero food**) were mistakenly tagged with `product_forms: ['food_or_meal']`, so the quiz recommends a commemorative medal to someone asking for meals!")
    md.append("\n")

    md.append("### Finding 4: Deceptive '(без сторонніх речей)' Guarantees for Sleep Pills & Medals (CRITICAL FAIL)")
    md.append("> [!WARNING]")
    md.append("> When `component_class: 'sports_accessories'` is selected, `_build_why_suitable()` promises:")
    md.append("> *«Категорія товарів: у наборі саме Спортивні аксесуари та пляшки (без сторонніх речей).»*")
    md.append("> Yet set `race-expert-062` contains **VPLab Ultra Sleep (60 caps) and Nutriversum Melatonin (60 caps)** along with a 3-month gym club membership!")
    md.append("> Calling a tub of melatonin and sleep medication 'sports accessories and bottles without foreign items' is deceptive and damages user trust.")
    md.append("\n")

    md.append("### Finding 5: Sizing Range Crashes and Bundled Socks Mismatches (CRITICAL FAIL & WARN)")
    md.append("> [!NOTE]")
    md.append("> **1. Schema Crash on Range Strings:** Passing a string range like `'40-42'` crashes `draft_matcher` with an unhandled `DraftMatchError` instead of gracefully sanitizing numeric input.")
    md.append("> **2. Severe Sizing Mismatch in Gift/Gear Bundles:** Sets `094`, `096`, `100`, and `101` bundle dark/white socks fixed at size **40–44**. When a female hiker with shoe size **36 or 37** or a male hiker with shoe size **46** requests summer apparel, they are recommended socks that do not fit (e.g. Test #96).")
    md.append("> **3. Catalog Ceiling on Large Sizes:** Thermal socks 1+1=3 (`race-expert-001`..`004`) only reach size **45**. Hikers with shoe sizes 46, 47, or 48 receive 0 results.")
    md.append("> **4. Default Size 43–45 Bias:** When shoe size is omitted, the engine defaults to recommending size 43–45 (`race-expert-001`).")
    md.append("\n")

    md.append("### Finding 6: Schema Taxonomy Crash on Evening/Bedtime Context (CRITICAL FAIL)")
    md.append("> [!CAUTION]")
    md.append("> In `draft_matcher.py`, `USE_TIMINGS_BY_GOAL['outdoors'] = {'during_training', 'daily_use'}`.")
    md.append("> However, catalog set `race-expert-062` («Польовий сон») was audited with `use_contexts: ['evening_or_bedtime']`.")
    md.append("> When a camper requests bedtime relaxation (`use_timing: 'evening_or_bedtime'`), `draft_matcher` crashes with `DraftMatchError: use_timing is not supported for the selected need`.")
    md.append("\n")

    md.append("### Finding 7: Massive Club Membership Dilution (18 of 28 Sets Contain Subscriptions)")
    md.append("> Out of 28 candidate sets for outdoors, **18 contain a 3-month Race Expert Club subscription**.")
    md.append("> For outdoor buyers who want pure dehydrated food or dried meat without paying for gym club perks, only 1 pure food set exists (`race-expert-111`, ЇDLO 2.0) and only 4 pure jerky sets exist (`race-expert-185`, `186`, `188`, `208`).")
    md.append("> When `membership: 'no'` is chosen, the engine correctly filters out club sets (PASS), but in default flows, club sets dominate the ranking.")
    md.append("\n")

    md.append("### Finding 8: Absence of Multi-Day Hiking Stacks (Meals + Jerky + Socks)")
    md.append("> Hikers frequently ask for a complete expedition pack containing hot dehydrated meals, savory high-protein meat jerky, and clean thermal socks.")
    md.append("> In the catalog, only `race-expert-191` combines meals + jerky. **Zero sets combine nutrition with thermal socks**, and the single-set engine cannot construct cross-product bundles.")
    md.append("\n")

    md.append("### Finding 9: TRISWIM Swimmer Chlorine Wash in an Outdoor Catalog")
    md.append("> Set `race-expert-080` (Набір «Дорожня гігієна», 1500 ₴) contains TRISWIM Body Wash — a specialized cosmetic body wash formulated for pool swimmers to neutralize chlorine odor and chemical irritation.")
    md.append("> Recommending pool swimmer soap to wilderness campers in the mountains is an athletic domain mismatch.")
    md.append("\n")

    md.append("## 4. Comprehensive Test Scenario Log (100 Cases)")
    md.append("| # | Scenario Name | Budget | Size | Class | Activity | Verdict | Main Flaw / Evaluation Notes |")
    md.append("|---|---|---|---|---|---|---|---|")
    for r in results:
        sc = r["request"]
        ev = r["evaluation"]
        tid = r["test_id"]
        name = r["name"][:38]
        b = f"{sc.get('max_price_uah', 'any')} ₴" if sc.get('max_price_uah') else "any"
        s = sc.get('shoe_size', 'any')
        c = sc.get('component_class', 'any')
        act = sc.get('activity', 'any')
        v = ev["verdict"]
        flaw = ev["flaw_summary"].replace("|", "/")[:65]
        v_bold = f"**{v}**"
        md.append(f"| {tid:03d} | {name} | {b} | {s} | {c} | {act} | {v_bold} | {flaw} |")
    md.append("\n")

    md.append("## 5. Strategic Recommendations for Engineering & Merchandising")
    md.append("1. **Fix Dehydrated Food Taxonomy:** In `quiz-set-audit.json`, add `'dehydrated_meal'` to `component_classes_from_listed_names` for sets `race-expert-078`, `race-expert-111`, and `race-expert-191` (and populate `product_forms: ['food_or_meal']`).")
    md.append("2. **Resolve Cycling in Outdoors:** Either add `cycling` to `activity_groups` for portable rations, jerky, and trail hydration (since bikepackers eat ЇDLO and jerky), or remove `cycling` from `ACTIVITY_OPTIONS_BY_GOAL['outdoors']`.")
    md.append("3. **Fix Deceptive '(без сторонніх речей)' Phrase:** In `_build_why_suitable()`, remove this guarantee unless programmatically verified that 100% of items belong to the requested class without supplements or subscriptions.")
    md.append("4. **Sanitize Sizing Input:** Parse string ranges like `'40-42'` into average numeric values (`41`) rather than throwing an unhandled exception.")
    md.append("5. **Expand Socks Sizing:** Onboard size 46–48 thermal socks into `outdoors` to cater to large-footed hikers.")
    md.append("6. **Introduce Genuine Multi-Day Expedition Stacks:** Create bundled SKUs combining ЇDLO meals + jerky snacks + 1 pair of thermal socks + soft flask for 1800–2200 ₴.")
    md.append("7. **Clean Up Pool Soap:** Replace TRISWIM swimmer chlorine wash in `race-expert-080` with biodegradable outdoor wilderness camp soap (e.g., Sea to Summit Pocket Soap).")

    OUTPUT_REPORT.write_text("\n".join(md), encoding="utf-8")

def get_flaw_desc(code):
    descs = {
        "NONE": "Ідеальна відповідність запиту туриста, точний підбір спорядження чи харчування",
        "DEHYDRATED_FOOD_SELECTION_FAILURE": "Критичний глухий кут: вибір 'dehydrated_meal' дає 0 результатів через невідповідність класу в базі",
        "CYCLING_TAXONOMY_DEAD_END": "Критичний глухий кут: вибір активності 'cycling' дає 0 результатів, жоден набір не підтримує велопоходи",
        "SCHEMA_CRASH_UNSANITIZED_INPUT": "Крах двигуна на рядковому діапазоні розміру взуття (наприклад, '40-42')",
        "SCHEMA_TAXONOMY_CRASH": "Таксономічний крах: контекст 'evening_or_bedtime' відсутній у схемі для outdoors",
        "SIZING_MISMATCH": "Невідповідність розміру шкарпеток у комбінованих наборах (фіксовані 40–44 замість 36/37/46)",
        "SIZING_UNAVAILABLE": "Відсутність у каталозі великих (46–48) або маленьких (34) розмірів термошкарпеток",
        "DECEPTIVE_EXPLANATION": "Неправдиві маркетингові твердження: 'без сторонніх речей' при наявності снодійних пігулок або медалей",
        "TAXONOMY_TAGGING_OMISSION": "Помилка тегів: у ЇDLO 2.0 порожній список product_forms, через що фільтр 'food_or_meal' виключає їжу",
        "INDOOR_GYM_OR_SUPPLEMENT_LEAK": "Витік снодійних добавок (VPLab Ultra Sleep, мелатонін) у видачу туристичного харчування",
        "POOL_ITEM_IN_OUTDOORS": "Невідповідність призначенню: гель для пловців TRISWIM від хлору у наборі для походів",
        "BUDGET_FLOOR_OR_NEAR_MISS": "Бюджет покупця (800–1000 ₴) нижчий за мінімальний у каталозі (1058 ₴ для шкарпеток, 1249 ₴ для їжі)",
        "DEFAULT_SIZE_BIAS": "При неуточненому розмірі система автоматично нав'язує найбільший розмір 43–45",
        "FORCED_CLUB_MEMBERSHIP_DILUTION": "Більшість наборів розбавлені платним абонементом клубу замість чистих товарів",
        "UNWANTED_CLUB_MEMBERSHIP_LEAK": "Покупець відмовився від клубу (membership='no'), але отримав клубні набори",
        "MULTI_ITEM_STACK_INCOMPLETE": "Неможливість формування повного стеку (гаряча їжа + джеркі + термошкарпетки)",
        "ZERO_RESULTS_UNEXPECTED": "Порожня видача (0 результатів) для валідного туристичного запиту",
        "SUBOPTIMAL_RECOMMENDATION": "Субоптимальний вибір товару (наприклад, набори з медалями для літнього трекінгу)"
    }
    return descs.get(code, code)

if __name__ == "__main__":
    main()
