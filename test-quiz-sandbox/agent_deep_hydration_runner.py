#!/usr/bin/env python3
"""
QA Deep Hydration Specialist Test Suite (100 Scenarios)
Focus: Hydration & Electrolytes (`hydration`)
Auditing: wiki/projects/quiz-set-audit.json & draft_matcher.py
Output:
  - test-quiz-sandbox/agent_deep_hydration_100_tests.json
  - test-quiz-sandbox/agent_deep_hydration_report.md
"""

import sys
import json
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from server import _load_catalog, CATALOG_PATH, AUDIT_PATH
from draft_matcher import attach_audit_evidence, draft_recommend, DraftMatchError

raw_catalog = _load_catalog(CATALOG_PATH)
audit_data = json.load(open(AUDIT_PATH, encoding="utf-8"))
catalog = attach_audit_evidence(raw_catalog, audit_data)
catalog_by_sku = {r["sku"]: r for r in catalog}

print(f"Loaded {len(catalog)} sets for Hydration QA Specialist.")

# Define 100 test scenarios
def build_100_scenarios():
    scenarios = []

    # ------------------------------------------------------------------------
    # Category 1: High Heat / Heavy Sweat / Cramp Prevention (High Sodium: Precision Hydration 1000, Hydria Perform) (1-20)
    # ------------------------------------------------------------------------
    scenarios.append({
        "id": "HYD-001",
        "category": "high_heat_cramps",
        "title": "Summer trail marathoner with heavy sweat rate seeking high-sodium cramp prevention",
        "request": {"goal_group": "hydration", "activity": "running", "use_timing": "during_training", "use_scenario": "event_preparation", "max_price_uah": 1500, "locale": "uk"},
        "expected_domain": "Precision Hydration 1000 or Hydria Perform high-electrolyte formula",
        "persona": "Athletic runner competing in 30°C heat prone to severe calf cramps and sodium depletion"
    })
    scenarios.append({
        "id": "HYD-002",
        "category": "high_heat_cramps",
        "title": "Road cyclist competing in 35°C heat prone to quadriceps cramps, needing maximum sodium concentration",
        "request": {"goal_group": "hydration", "activity": "cycling", "use_timing": "during_training", "max_price_uah": 1600, "locale": "uk"},
        "expected_domain": "Electrolyte solution with high sodium (Precision Hydration 1000 or Hydria Perform)",
        "persona": "Century cyclist riding 120km under scorching midday sun"
    })
    scenarios.append({
        "id": "HYD-003",
        "category": "high_heat_cramps",
        "title": "Veteran sport athlete seeking heat protection hydration bundle (Precision Hydration 1000 Tube + capsules)",
        "request": {"goal_group": "hydration", "activity": "running", "component_class": "supplements_vitamins_minerals", "max_price_uah": 1300, "locale": "uk"},
        "expected_domain": "RE11650 «Захист від спеки» (Precision Hydration 1000 + capsules)",
        "persona": "Veteran runner participating in summer races"
    })
    scenarios.append({
        "id": "HYD-004",
        "category": "high_heat_cramps",
        "title": "Heavy sweater preparing for an ironman 70.3 bike leg under scorching sun",
        "request": {"goal_group": "hydration", "activity": "cycling", "component_class": "hydration_items", "max_price_uah": 1600, "locale": "uk"},
        "expected_domain": "High-electrolyte isotonic sticks or tablets",
        "persona": "Triathlete with high sweat loss rate during cycling"
    })
    scenarios.append({
        "id": "HYD-005",
        "category": "high_heat_cramps",
        "title": "Fast-sweating runner prone to calf cramps during 30km long runs",
        "request": {"goal_group": "hydration", "activity": "running", "component_class": "hydration_items", "max_price_uah": 1500, "locale": "ru"},
        "expected_domain": "Hydria Perform or Precision Hydration electrolyte pack",
        "persona": "Marathon trainee running in humid conditions"
    })
    scenarios.append({
        "id": "HYD-006",
        "category": "high_heat_cramps",
        "title": "Ultra-runner needing Hydria Perform electrolyte sticks for heat adaptation",
        "request": {"goal_group": "hydration", "activity": "running", "product_form": "sticks", "max_price_uah": 1500, "locale": "uk"},
        "expected_domain": "Nabir_1015 (20 sticks Hydria Perform) or Nabir_1123 (16 sticks Hydria Perform + bottle)",
        "persona": "Trail runner training in summer heat"
    })
    scenarios.append({
        "id": "HYD-007",
        "category": "high_heat_cramps",
        "title": "Marathon runner asking for electrolyte stock (20 sticks Hydria Perform) under 1500 UAH",
        "request": {"goal_group": "hydration", "activity": "running", "max_price_uah": 1500, "locale": "uk"},
        "expected_domain": "Nabir_1015 «Електролітний запас Race Expert Club»",
        "persona": "Road runner needing bulk electrolyte sticks for marathon training cycle"
    })
    scenarios.append({
        "id": "HYD-008",
        "category": "high_heat_cramps",
        "title": "Hot weather runner asking for electrolyte salts with sodium and magnesium against cramps",
        "request": {"goal_group": "hydration", "activity": "running", "use_timing": "before_or_after_training", "max_price_uah": 1500, "locale": "uk"},
        "expected_domain": "RE11652 «Боротьба з кріпатурою» (Swanson Triple Magnesium + 5 Hydria Perform sticks)",
        "persona": "Runner experiencing nighttime leg cramps and post-run soreness"
    })
    scenarios.append({
        "id": "HYD-009",
        "category": "high_heat_cramps",
        "title": "Cyclist asking for cramp prevention formula during century ride in July",
        "request": {"goal_group": "hydration", "activity": "cycling", "use_scenario": "event_preparation", "max_price_uah": 1600, "locale": "uk"},
        "expected_domain": "Electrolyte hydration kits with high sodium",
        "persona": "Amateur road cyclist participating in 100km sportive"
    })
    scenarios.append({
        "id": "HYD-010",
        "category": "high_heat_cramps",
        "title": "Marathon runner requesting high sodium hydration with budget 1300 UAH",
        "request": {"goal_group": "hydration", "activity": "running", "max_price_uah": 1300, "locale": "uk"},
        "expected_domain": "RE11650 (1239 UAH) or RE11786 (1285 UAH)",
        "persona": "Marathon runner on a 1300 UAH budget needing electrolyte protection"
    })
    scenarios.append({
        "id": "HYD-011",
        "category": "high_heat_cramps",
        "title": "Heavy sweater asking for hydration during training in high humidity",
        "request": {"goal_group": "hydration", "activity": "running", "use_timing": "during_training", "max_price_uah": 1500, "locale": "uk"},
        "expected_domain": "Hydria Perform or bottle bundle",
        "persona": "Runner sweating heavily in 85% humidity morning workouts"
    })
    scenarios.append({
        "id": "HYD-012",
        "category": "high_heat_cramps",
        "title": "Runner seeking pure electrolyte replacement without heavy sugar",
        "request": {"goal_group": "hydration", "activity": "running", "component_class": "hydration_items", "max_price_uah": 1500, "locale": "uk"},
        "expected_domain": "Pure electrolyte sticks/tablets (Hydria Perform, Precision Hydration)",
        "persona": "Runner on low-carb / keto diet needing electrolytes without maltodextrin"
    })
    scenarios.append({
        "id": "HYD-013",
        "category": "high_heat_cramps",
        "title": "Cyclist seeking high electrolyte concentration under 1500 UAH",
        "request": {"goal_group": "hydration", "activity": "cycling", "component_class": "hydration_items", "max_price_uah": 1500, "locale": "uk"},
        "expected_domain": "Hydria Perform or bottle bundle",
        "persona": "Mountain biker doing steep climbs in heat"
    })
    scenarios.append({
        "id": "HYD-014",
        "category": "high_heat_cramps",
        "title": "Endurance runner needing cramp defense with quick absorption during long runs",
        "request": {"goal_group": "hydration", "activity": "running", "use_timing": "during_training", "product_form": "sticks", "max_price_uah": 1500, "locale": "ru"},
        "expected_domain": "Hydria Perform electrolyte sticks",
        "persona": "Runner doing 25-32km weekend long runs"
    })
    scenarios.append({
        "id": "HYD-015",
        "category": "high_heat_cramps",
        "title": "Athlete training midday in summer heat seeking heat-protection hydration kit",
        "request": {"goal_group": "hydration", "activity": "running", "max_price_uah": 1400, "locale": "uk"},
        "expected_domain": "RE11650 «Захист від спеки» (1239 UAH)",
        "persona": "Athlete doing lunchtime runs in July sun"
    })
    scenarios.append({
        "id": "HYD-016",
        "category": "high_heat_cramps",
        "title": "Distance runner asking for high-dose sodium tablets for sweaty conditions",
        "request": {"goal_group": "hydration", "activity": "running", "use_timing": "during_training", "max_price_uah": 1300, "locale": "uk"},
        "expected_domain": "RE11650 (Precision Hydration 1000 Tube tablets)",
        "persona": "Runner asking for electrolyte effervescent tablets"
    })
    scenarios.append({
        "id": "HYD-017",
        "category": "high_heat_cramps",
        "title": "Cyclist asking for Hydria Perform sticks for mountain climb in hot weather",
        "request": {"goal_group": "hydration", "activity": "cycling", "product_form": "sticks", "max_price_uah": 1500, "locale": "uk"},
        "expected_domain": "Nabir_1123 or Nabir_1015",
        "persona": "Road cyclist climbing Carpathian mountain passes"
    })
    scenarios.append({
        "id": "HYD-018",
        "category": "high_heat_cramps",
        "title": "Runner training for desert/sand ultra requiring electrolyte salt tablets",
        "request": {"goal_group": "hydration", "activity": "running", "use_scenario": "event_preparation", "max_price_uah": 1300, "locale": "uk"},
        "expected_domain": "Precision Hydration 1000 + salt capsules (RE11650)",
        "persona": "Ultra-runner training for multi-day desert stage race"
    })
    scenarios.append({
        "id": "HYD-019",
        "category": "high_heat_cramps",
        "title": "Hot weather runner looking for magnesium + sodium combo for night cramps after long runs",
        "request": {"goal_group": "hydration", "activity": "running", "use_timing": "before_or_after_training", "max_price_uah": 1500, "locale": "ru"},
        "expected_domain": "RE11652 «Боротьба з кріпатурою» (Triple Mag + Hydria Perform)",
        "persona": "Runner suffering severe nocturnal cramps after hot training sessions"
    })
    scenarios.append({
        "id": "HYD-020",
        "category": "high_heat_cramps",
        "title": "Competitive runner asking for cramp prevention bundle before race start",
        "request": {"goal_group": "hydration", "activity": "running", "use_timing": "before_or_after_training", "use_scenario": "event_preparation", "max_price_uah": 1500, "locale": "uk"},
        "expected_domain": "Pre-race electrolyte loading formula",
        "persona": "Marathon competitor pre-loading sodium 2 hours before gun time"
    })

    # ------------------------------------------------------------------------
    # Category 2: General Daily Mineral Balance (Hydria Daily) (21-35)
    # ------------------------------------------------------------------------
    scenarios.append({
        "id": "HYD-021",
        "category": "daily_mineral_balance",
        "title": "Office worker and casual runner seeking daily mineral balance for hydration at desk",
        "request": {"goal_group": "hydration", "activity": "running", "use_timing": "daily_use", "max_price_uah": 1500, "locale": "uk"},
        "expected_domain": "RE88946 (Hydria Daily 8 sticks + bottle) or RE11021 (Hydria Daily 8 sticks)",
        "persona": "Desk worker doing 5k evening runs, wanting daily electrolyte mineral support"
    })
    scenarios.append({
        "id": "HYD-022",
        "category": "daily_mineral_balance",
        "title": "Everyday active individual looking for Hydria Daily peach sticks for gentle hydration",
        "request": {"goal_group": "hydration", "use_timing": "daily_use", "max_price_uah": 1500, "locale": "uk"},
        "expected_domain": "Hydria Daily sets without stimulants or creatine",
        "persona": "Health-conscious buyer looking for gentle daily electrolyte drink"
    })
    scenarios.append({
        "id": "HYD-023",
        "category": "daily_mineral_balance",
        "title": "Fitness enthusiast wanting daily electrolyte drink without high sodium/sugar",
        "request": {"goal_group": "hydration", "activity": "running", "use_timing": "daily_use", "use_scenario": "everyday", "max_price_uah": 1500, "locale": "uk"},
        "expected_domain": "Hydria Daily mineral electrolyte formula",
        "persona": "Recreational runner wanting balanced daily mineral replenishment"
    })
    scenarios.append({
        "id": "HYD-024",
        "category": "daily_mineral_balance",
        "title": "Morning hydration routine seeker wanting vitamins + light minerals (Hydria Daily)",
        "request": {"goal_group": "hydration", "use_timing": "daily_use", "component_class": "hydration_items", "max_price_uah": 1500, "locale": "uk"},
        "expected_domain": "RE88946 (Hydria Daily with B-vitamins, C, Na, K, Mg)",
        "persona": "Morning runner establishing optimal hydration habits upon waking"
    })
    scenarios.append({
        "id": "HYD-025",
        "category": "daily_mineral_balance",
        "title": "Daily hydration for person recovering from mild dehydration in warm weather",
        "request": {"goal_group": "hydration", "use_timing": "daily_use", "product_form": "sticks", "max_price_uah": 1500, "locale": "ru"},
        "expected_domain": "Hydria Daily sticks",
        "persona": "Active professional feeling fatigued from air conditioning and summer heat"
    })
    scenarios.append({
        "id": "HYD-026",
        "category": "daily_mineral_balance",
        "title": "Active person wanting daily mineral balance with bottle included",
        "request": {"goal_group": "hydration", "component_class": "sports_accessories", "use_timing": "daily_use", "max_price_uah": 1500, "locale": "uk"},
        "expected_domain": "RE88946 or RE11021 (Glass bottle 530ml + Hydria Daily sticks)",
        "persona": "Corporate athlete wanting water bottle + hydration packets for the office"
    })
    scenarios.append({
        "id": "HYD-027",
        "category": "daily_mineral_balance",
        "title": "Runner wanting daily hydration on non-workout recovery days",
        "request": {"goal_group": "hydration", "activity": "running", "use_timing": "daily_use", "use_scenario": "everyday", "max_price_uah": 1400, "locale": "uk"},
        "expected_domain": "RE11021 (1379 UAH) or RE88946 (1500 UAH)",
        "persona": "Half-marathon runner maintaining mineral homeostasis between hard sessions"
    })
    scenarios.append({
        "id": "HYD-028",
        "category": "daily_mineral_balance",
        "title": "Daily mineral balance with budget 1400 UAH",
        "request": {"goal_group": "hydration", "activity": "running", "use_timing": "daily_use", "max_price_uah": 1400, "locale": "uk"},
        "expected_domain": "RE11021 (1379 UAH)",
        "persona": "Budget-conscious runner seeking daily mineral drink under 1400 UAH"
    })
    scenarios.append({
        "id": "HYD-029",
        "category": "daily_mineral_balance",
        "title": "Daily electrolyte drink for desk job and evening brisk walks",
        "request": {"goal_group": "hydration", "use_scenario": "everyday", "use_timing": "daily_use", "max_price_uah": 1500, "locale": "uk"},
        "expected_domain": "Hydria Daily mineral replenishment",
        "persona": "Sedentary worker hydrating properly during workday"
    })
    scenarios.append({
        "id": "HYD-030",
        "category": "daily_mineral_balance",
        "title": "Gentle mineral hydration drink mix for everyday lifestyle",
        "request": {"goal_group": "hydration", "use_timing": "daily_use", "max_price_uah": 1500, "locale": "ru"},
        "expected_domain": "Hydria Daily electrolyte sets",
        "persona": "Person avoiding heavy athletic salt drinks, preferring light mineral taste"
    })
    scenarios.append({
        "id": "HYD-031",
        "category": "daily_mineral_balance",
        "title": "Daily wellness electrolyte mix with B-vitamins and vitamin C",
        "request": {"goal_group": "hydration", "activity": "running", "use_timing": "daily_use", "max_price_uah": 1500, "locale": "uk"},
        "expected_domain": "RE88946 (Hydria Daily with B-vitamins & vitamin C)",
        "persona": "Athlete seeking cellular hydration plus antioxidant defense"
    })
    scenarios.append({
        "id": "HYD-032",
        "category": "daily_mineral_balance",
        "title": "Daily mineral drink for hot summer days at work",
        "request": {"goal_group": "hydration", "use_timing": "daily_use", "season": "summer", "max_price_uah": 1500, "locale": "uk"},
        "expected_domain": "RE88946 or RE11021",
        "persona": "Worker needing light mineral drink during hot August heatwave"
    })
    scenarios.append({
        "id": "HYD-033",
        "category": "daily_mineral_balance",
        "title": "Light electrolyte hydration drink for student/office focus",
        "request": {"goal_group": "hydration", "use_timing": "daily_use", "max_price_uah": 1500, "locale": "uk"},
        "expected_domain": "Hydria Daily mineral formula",
        "persona": "University student studying long hours needing cognitive hydration without jittery stimulants"
    })
    scenarios.append({
        "id": "HYD-034",
        "category": "daily_mineral_balance",
        "title": "Daily mineral balance kit with clean composition (no artificial stimulants or creatine)",
        "request": {"goal_group": "hydration", "activity": "running", "component_class": "hydration_items", "use_timing": "daily_use", "max_price_uah": 1500, "locale": "uk"},
        "expected_domain": "RE88946 «Гідратація тренувань»",
        "persona": "Clean nutrition enthusiast demanding no extraneous creatine powders or medicinal mushrooms"
    })
    scenarios.append({
        "id": "HYD-035",
        "category": "daily_mineral_balance",
        "title": "Daily hydration bundle with reusable water bottle for daily commute",
        "request": {"goal_group": "hydration", "component_class": "sports_accessories", "use_timing": "daily_use", "max_price_uah": 1400, "locale": "uk"},
        "expected_domain": "RE11021 (Glass bottle 530ml + Hydria Daily peach sticks x8)",
        "persona": "Commuter wanting a stylish glass water bottle and daily electrolyte sticks"
    })

    # ------------------------------------------------------------------------
    # Category 3: Endurance Race Hydration + Amino Acids (SIS Go Hydro, Nutriversum) (36-55)
    # ------------------------------------------------------------------------
    scenarios.append({
        "id": "HYD-036",
        "category": "endurance_amino_hydration",
        "title": "Trail ultramarathoner needing both SIS Go Hydro electrolytes and Beta Fuel gels (UT-PRO-2026)",
        "request": {"goal_group": "hydration", "activity": "running", "component_class": "hydration_items", "max_price_uah": 1700, "locale": "uk"},
        "expected_domain": "UT-PRO-2026 «Ultra Trail Marathon Energy & Hydration Pro» (1650 UAH)",
        "persona": "Mountain ultramarathon runner tackling 70km trail race"
    })
    scenarios.append({
        "id": "HYD-037",
        "category": "endurance_amino_hydration",
        "title": "Mountain runner seeking SIS Go Hydro effervescent hydration for race vests",
        "request": {"goal_group": "hydration", "activity": "running", "use_scenario": "event_preparation", "max_price_uah": 1700, "locale": "uk"},
        "expected_domain": "UT-PRO-2026 (SIS Go Hydro tablets included)",
        "persona": "Skyrunner competing in steep alpine terrain"
    })
    scenarios.append({
        "id": "HYD-038",
        "category": "endurance_amino_hydration",
        "title": "Endurance cyclist seeking amino acid protection (EAA) + electrolytes during 5-hour ride",
        "request": {"goal_group": "hydration", "activity": "cycling", "use_timing": "during_training", "max_price_uah": 1500, "locale": "uk"},
        "expected_domain": "RE11802 «Витривалість без спраги» (Nutriversum EAA 500g + Hydria Perform 5 sticks + Brave U shaker)",
        "persona": "Long-distance cyclist needing EAA to prevent muscle catabolism on 150km rides"
    })
    scenarios.append({
        "id": "HYD-039",
        "category": "endurance_amino_hydration",
        "title": "Half-Ironman triathlete asking for Nutriversum EAA + Hydria Perform electrolyte combo",
        "request": {"goal_group": "hydration", "activity": "cycling", "use_scenario": "event_preparation", "max_price_uah": 1500, "locale": "uk"},
        "expected_domain": "RE11802 «Витривалість без спраги Race Expert Club»",
        "persona": "Triathlete preparing for 90km bike leg requiring intra-workout amino hydration"
    })
    scenarios.append({
        "id": "HYD-040",
        "category": "endurance_amino_hydration",
        "title": "Marathon runner seeking BCAA + electrolyte sticks + shaker for endurance training",
        "request": {"goal_group": "hydration", "activity": "running", "max_price_uah": 1300, "locale": "uk"},
        "expected_domain": "RE11786 «Тренувальний ресурс Race Expert Club» (Nutriversum BCAA + Hydria Perform + Myprotein shaker 1285 UAH)",
        "persona": "Marathoner doing 30km training runs needing intra-workout BCAA and hydration"
    })
    scenarios.append({
        "id": "HYD-041",
        "category": "endurance_amino_hydration",
        "title": "Long distance runner wanting amino acids to prevent muscle breakdown during 35km run",
        "request": {"goal_group": "hydration", "activity": "running", "use_timing": "during_training", "max_price_uah": 1500, "locale": "uk"},
        "expected_domain": "RE11786 (Nutriversum BCAA + Hydria Perform) or RE11802 (Nutriversum EAA + Hydria Perform)",
        "persona": "Competitive marathoner training for sub-3h marathon"
    })
    scenarios.append({
        "id": "HYD-042",
        "category": "endurance_amino_hydration",
        "title": "Triathlete preparing for Olympic distance asking for isotonic hydration + amino formula",
        "request": {"goal_group": "hydration", "activity": "cycling", "component_class": "hydration_items", "max_price_uah": 1500, "locale": "uk"},
        "expected_domain": "RE11802 or RE11786",
        "persona": "Olympic distance triathlete wanting seamless transition hydration"
    })
    scenarios.append({
        "id": "HYD-043",
        "category": "endurance_amino_hydration",
        "title": "Gran Fondo cyclist seeking endurance hydration bundle with shaker and EAA",
        "request": {"goal_group": "hydration", "activity": "cycling", "component_class": "sports_accessories", "max_price_uah": 1500, "locale": "ru"},
        "expected_domain": "RE11802 (Nutriversum EAA + Hydria Perform + Brave U shaker)",
        "persona": "Gran Fondo participant needing large shaker and electrolyte fuel"
    })
    scenarios.append({
        "id": "HYD-044",
        "category": "endurance_amino_hydration",
        "title": "Trail runner needing electrolyte tabs and energy gels for 50km mountain race",
        "request": {"goal_group": "hydration", "activity": "running", "use_scenario": "event_preparation", "max_price_uah": 1700, "locale": "uk"},
        "expected_domain": "UT-PRO-2026 (SIS Beta Fuel + SIS Go Hydro)",
        "persona": "Trail runner competing in Carpathians Ultra"
    })
    scenarios.append({
        "id": "HYD-045",
        "category": "endurance_amino_hydration",
        "title": "Ultra endurance athlete with high budget (1800 UAH) wanting complete race nutrition & hydration",
        "request": {"goal_group": "hydration", "activity": "running", "max_price_uah": 1800, "locale": "uk"},
        "expected_domain": "UT-PRO-2026 (1650 UAH)",
        "persona": "Experienced ultra runner with generous budget wanting premium SIS race pack"
    })
    scenarios.append({
        "id": "HYD-046",
        "category": "endurance_amino_hydration",
        "title": "Distance runner seeking SIS electrolytes for fast gastric emptying without GI distress",
        "request": {"goal_group": "hydration", "activity": "running", "component_class": "hydration_items", "max_price_uah": 1650, "locale": "uk"},
        "expected_domain": "UT-PRO-2026 or RE88946 (SIS Go + Electrolyte gels)",
        "persona": "Sensitive-stomach runner needing isotonic electrolyte formulas"
    })
    scenarios.append({
        "id": "HYD-047",
        "category": "endurance_amino_hydration",
        "title": "Marathoner asking for electrolytes + carbohydrates combination for race day fueling",
        "request": {"goal_group": "hydration", "activity": "running", "component_class": "protein_carbohydrate_food", "use_scenario": "event_preparation", "max_price_uah": 1500, "locale": "uk"},
        "expected_domain": "RE11659 «Тиждень бігуна» (Hydria Perform + GU Chews + Sponser Bar) or RE88946 (Hydria + SiS gels)",
        "persona": "Marathoner needing combined fluid, mineral, and carb ingestion"
    })
    scenarios.append({
        "id": "HYD-048",
        "category": "endurance_amino_hydration",
        "title": "Endurance athlete asking for Nutriversum BCAA 2:1:1 + Hydria Perform for tempo workouts",
        "request": {"goal_group": "hydration", "activity": "running", "max_price_uah": 1300, "locale": "uk"},
        "expected_domain": "RE11786 (1285 UAH)",
        "persona": "Half-marathoner executing fast tempo runs mid-week"
    })
    scenarios.append({
        "id": "HYD-049",
        "category": "endurance_amino_hydration",
        "title": "Road cyclist seeking sugar-free amino hydration drink for long steady distance",
        "request": {"goal_group": "hydration", "activity": "cycling", "use_timing": "during_training", "max_price_uah": 1500, "locale": "uk"},
        "expected_domain": "RE11802 (Nutriversum EAA Sugar Free 500g + Hydria Perform)",
        "persona": "Cyclist on 100km Zone 2 training wanting zero added sugars"
    })
    scenarios.append({
        "id": "HYD-050",
        "category": "endurance_amino_hydration",
        "title": "Ultra trail runner needing multi-hour race hydration with electrolytes and amino support",
        "request": {"goal_group": "hydration", "activity": "running", "use_timing": "during_training", "max_price_uah": 1700, "locale": "ru"},
        "expected_domain": "UT-PRO-2026 or RE11802",
        "persona": "Trail runner spending 8+ hours in mountains"
    })
    scenarios.append({
        "id": "HYD-051",
        "category": "endurance_amino_hydration",
        "title": "Cross-country mountain biker asking for SIS hydration and electrolyte gels",
        "request": {"goal_group": "hydration", "activity": "cycling", "component_class": "hydration_items", "max_price_uah": 1500, "locale": "uk"},
        "expected_domain": "RE88946 (SiS Go + Electrolyte gels 60ml x4 + Hydria Daily + bottle)",
        "persona": "XC mountain biker racing rough singletrack"
    })
    scenarios.append({
        "id": "HYD-052",
        "category": "endurance_amino_hydration",
        "title": "Marathon racer wanting SIS Go Hydro with berry/citrus electrolytes for race belt",
        "request": {"goal_group": "hydration", "activity": "running", "use_scenario": "event_preparation", "max_price_uah": 1700, "locale": "uk"},
        "expected_domain": "UT-PRO-2026",
        "persona": "City marathon participant carrying SIS tablets"
    })
    scenarios.append({
        "id": "HYD-053",
        "category": "endurance_amino_hydration",
        "title": "Long distance triathlete seeking all-in-one endurance pack with shaker and amino acids",
        "request": {"goal_group": "hydration", "activity": "cycling", "component_class": "sports_accessories", "use_scenario": "event_preparation", "max_price_uah": 1500, "locale": "uk"},
        "expected_domain": "RE11802",
        "persona": "Middle-distance triathlete preparing race day nutrition containers"
    })
    scenarios.append({
        "id": "HYD-054",
        "category": "endurance_amino_hydration",
        "title": "Distance runner looking for electrolyte hydration bundle with energy chews (RE11659)",
        "request": {"goal_group": "hydration", "activity": "running", "component_class": "protein_carbohydrate_food", "max_price_uah": 1500, "locale": "uk"},
        "expected_domain": "RE11659 «Тиждень бігуна» (Hydria Perform + GU Energy Chews)",
        "persona": "Runner seeking chewable energy plus electrolyte hydration sticks"
    })
    scenarios.append({
        "id": "HYD-055",
        "category": "endurance_amino_hydration",
        "title": "Athlete preparing for multi-stage endurance race needing amino electrolytes",
        "request": {"goal_group": "hydration", "activity": "running", "use_timing": "during_training", "max_price_uah": 1500, "locale": "uk"},
        "expected_domain": "RE11802 or RE11786",
        "persona": "Endurance athlete needing daily muscle preservation and electrolyte replenishment"
    })

    # ------------------------------------------------------------------------
    # Category 4: Soft Flasks, Bottles & Hydration Gear (56-70)
    # ------------------------------------------------------------------------
    scenarios.append({
        "id": "HYD-056",
        "category": "flasks_bottles_gear",
        "title": "Trail runner looking for soft flask compatible hydration kit with electrolytes",
        "request": {"goal_group": "hydration", "activity": "running", "component_class": "sports_accessories", "max_price_uah": 1500, "locale": "uk"},
        "expected_domain": "Bottle + hydration sticks (Nabir_1123, RE88946)",
        "persona": "Trail runner looking for portable drinking gear and electrolyte powders"
    })
    scenarios.append({
        "id": "HYD-057",
        "category": "flasks_bottles_gear",
        "title": "Road runner asking specifically for a bottle and electrolyte sticks bundle (Nabir_1123)",
        "request": {"goal_group": "hydration", "activity": "running", "component_class": "sports_accessories", "max_price_uah": 1500, "locale": "uk"},
        "expected_domain": "Nabir_1123 «Комплект для гідратації Race Expert Club» (600ml bottle + 16 Hydria sticks)",
        "persona": "Runner seeking an official hydration set with branded water bottle"
    })
    scenarios.append({
        "id": "HYD-058",
        "category": "flasks_bottles_gear",
        "title": "Runner wanting a hydration bundle with glass water bottle (RE11021)",
        "request": {"goal_group": "hydration", "activity": "running", "component_class": "sports_accessories", "max_price_uah": 1400, "locale": "uk"},
        "expected_domain": "RE11021 (Glass bottle 530ml + Hydria Daily/Perform sticks 1379 UAH)",
        "persona": "Eco-friendly runner avoiding plastic bottles, wanting glass bottle + electrolytes"
    })
    scenarios.append({
        "id": "HYD-059",
        "category": "flasks_bottles_gear",
        "title": "Marathon runner wanting a water bottle and race number belt with hydration gels",
        "request": {"goal_group": "hydration", "activity": "running", "component_class": "sports_accessories", "use_scenario": "event_preparation", "max_price_uah": 1500, "locale": "uk"},
        "expected_domain": "RE11804 «Марафонський темп» (Belt + cap + Hydria Perform) or Nabir_1123",
        "persona": "Marathon runner gearing up for race day logistics"
    })
    scenarios.append({
        "id": "HYD-060",
        "category": "flasks_bottles_gear",
        "title": "Gym athlete wanting a shaker and hydration drink mix",
        "request": {"goal_group": "hydration", "activity": "running", "component_class": "sports_accessories", "max_price_uah": 1300, "locale": "uk"},
        "expected_domain": "RE11786 (Myprotein shaker 600ml + Hydria Perform 1285 UAH)",
        "persona": "Gym goer wanting a durable shaker to mix electrolyte drinks"
    })
    scenarios.append({
        "id": "HYD-061",
        "category": "flasks_bottles_gear",
        "title": "Cyclist needing a 600ml bottle to fit standard bike bottle cage with electrolyte sticks",
        "request": {"goal_group": "hydration", "activity": "cycling", "component_class": "sports_accessories", "max_price_uah": 1500, "locale": "uk"},
        "expected_domain": "Nabir_1123 (600ml bottle + 16 Hydria Perform sticks 1435 UAH)",
        "persona": "Road cyclist needing bike-compatible bottle and electrolyte sticks"
    })
    scenarios.append({
        "id": "HYD-062",
        "category": "flasks_bottles_gear",
        "title": "Runner asking for soft flasks for running hydration vest (checking catalog support)",
        "request": {"goal_group": "hydration", "activity": "running", "component_class": "sports_accessories", "max_price_uah": 1500, "locale": "ru"},
        "expected_domain": "Truthful disclosure that catalog has bottles/shakers, no soft flasks",
        "persona": "Trail runner asking whether soft flasks are stocked in hydration bundles"
    })
    scenarios.append({
        "id": "HYD-063",
        "category": "flasks_bottles_gear",
        "title": "Casual runner looking for handheld water bottle bundle for summer park runs",
        "request": {"goal_group": "hydration", "activity": "running", "component_class": "sports_accessories", "max_price_uah": 1450, "locale": "uk"},
        "expected_domain": "Nabir_1123 (1435 UAH) or RE11021 (1379 UAH)",
        "persona": "Parkrunner carrying water in hand during 10k weekend runs"
    })
    scenarios.append({
        "id": "HYD-064",
        "category": "flasks_bottles_gear",
        "title": "Athlete looking for sports accessories + hydration items (bottle + sticks)",
        "request": {"goal_group": "hydration", "activity": "running", "component_class": "sports_accessories", "max_price_uah": 1500, "locale": "uk"},
        "expected_domain": "Nabir_1123 or RE88946",
        "persona": "Multi-sport athlete equipping their gear bag"
    })
    scenarios.append({
        "id": "HYD-065",
        "category": "flasks_bottles_gear",
        "title": "Runner asking for water bottle with protective sleeve + electrolyte packs",
        "request": {"goal_group": "hydration", "activity": "running", "component_class": "sports_accessories", "max_price_uah": 1400, "locale": "uk"},
        "expected_domain": "RE11021 (Glass bottle 530ml with protective cover)",
        "persona": "Urban runner carrying glass bottle with protective neoprene sleeve"
    })
    scenarios.append({
        "id": "HYD-066",
        "category": "flasks_bottles_gear",
        "title": "Marathoner looking for bottle + socks + electrolyte kit under 1400 UAH",
        "request": {"goal_group": "hydration", "activity": "running", "max_price_uah": 1400, "locale": "uk"},
        "expected_domain": "RE11021 (1379 UAH - 2 pairs socks + glass bottle + 10 Hydria sticks)",
        "persona": "Runner wanting gear bundle combining fresh running socks, bottle, and electrolytes"
    })
    scenarios.append({
        "id": "HYD-067",
        "category": "flasks_bottles_gear",
        "title": "Fitness runner looking for bottle and Hydria Perform sticks under 1500 UAH",
        "request": {"goal_group": "hydration", "activity": "running", "component_class": "hydration_items", "max_price_uah": 1500, "locale": "uk"},
        "expected_domain": "Nabir_1123 or RE88946",
        "persona": "Fitness runner buying hydration kit with bottle"
    })
    scenarios.append({
        "id": "HYD-068",
        "category": "flasks_bottles_gear",
        "title": "Commuter wanting portable water bottle + hydration sticks for gym and work",
        "request": {"goal_group": "hydration", "component_class": "sports_accessories", "max_price_uah": 1450, "locale": "uk"},
        "expected_domain": "Nabir_1123 (1435 UAH)",
        "persona": "Hybrid commuter athlete"
    })
    scenarios.append({
        "id": "HYD-069",
        "category": "flasks_bottles_gear",
        "title": "Ultra runner asking for dual soft flask set with electrolyte tablets",
        "request": {"goal_group": "hydration", "activity": "running", "component_class": "sports_accessories", "max_price_uah": 1600, "locale": "ru"},
        "expected_domain": "Nabir_1123 or RE88946 (bottles)",
        "persona": "Ultra trail runner seeking vest hydration solutions"
    })
    scenarios.append({
        "id": "HYD-070",
        "category": "flasks_bottles_gear",
        "title": "Buyer searching for pure water bottle without socks or pills",
        "request": {"goal_group": "hydration", "activity": "running", "component_class": "sports_accessories", "max_price_uah": 1500, "locale": "uk"},
        "expected_domain": "Nabir_1123 (Bottle + Hydria Perform)",
        "persona": "Buyer wanting real hydration gear without footwear or unrelated supplements"
    })

    # ------------------------------------------------------------------------
    # Category 5: Budget Edge Cases & Low/Medium/High Tiers (71-85)
    # ------------------------------------------------------------------------
    scenarios.append({
        "id": "HYD-071",
        "category": "budget_tiers",
        "title": "Tight budget runner with 500 UAH looking for cheap electrolyte tablets",
        "request": {"goal_group": "hydration", "activity": "running", "max_price_uah": 500, "locale": "uk"},
        "expected_domain": "Catalog floor alert: minimum hydration kit is 1225/1239 UAH",
        "persona": "Student runner with only 500 UAH wanting single tube of electrolytes"
    })
    scenarios.append({
        "id": "HYD-072",
        "category": "budget_tiers",
        "title": "Student runner with 600 UAH budget seeking basic hydration salt sticks",
        "request": {"goal_group": "hydration", "activity": "running", "max_price_uah": 600, "locale": "uk"},
        "expected_domain": "Catalog floor alert: below minimum catalog price",
        "persona": "College student runner with strict 600 UAH limit"
    })
    scenarios.append({
        "id": "HYD-073",
        "category": "budget_tiers",
        "title": "Budget buyer with 750 UAH looking for simple hydration pack",
        "request": {"goal_group": "hydration", "activity": "running", "max_price_uah": 750, "locale": "uk"},
        "expected_domain": "Floor anchor or truthful out-of-budget explanation",
        "persona": "Casual jogger not wanting expensive bundles"
    })
    scenarios.append({
        "id": "HYD-074",
        "category": "budget_tiers",
        "title": "Runner with 800 UAH budget asking for electrolyte powder",
        "request": {"goal_group": "hydration", "activity": "running", "max_price_uah": 800, "locale": "uk"},
        "expected_domain": "Floor anchor / near miss explanation",
        "persona": "Amateur runner looking for budget-friendly hydration"
    })
    scenarios.append({
        "id": "HYD-075",
        "category": "budget_tiers",
        "title": "Budget athlete with 950 UAH looking for hydration set",
        "request": {"goal_group": "hydration", "activity": "running", "max_price_uah": 950, "locale": "uk"},
        "expected_domain": "Floor anchor or near-miss",
        "persona": "Athlete with 950 UAH gift budget"
    })
    scenarios.append({
        "id": "HYD-076",
        "category": "budget_tiers",
        "title": "Buyer with exactly 999 UAH budget (just below catalog 1000 UAH threshold)",
        "request": {"goal_group": "hydration", "activity": "running", "max_price_uah": 999, "locale": "uk"},
        "expected_domain": "Near-miss recommendations around 1225-1300 UAH",
        "persona": "Buyer probing the sub-1000 UAH threshold boundary"
    })
    scenarios.append({
        "id": "HYD-077",
        "category": "budget_tiers",
        "title": "Buyer with 1000 UAH budget looking for hydration kit",
        "request": {"goal_group": "hydration", "activity": "running", "max_price_uah": 1000, "locale": "uk"},
        "expected_domain": "Near-miss recommendations (RE11650 at 1239 UAH)",
        "persona": "Runner with round 1000 UAH budget"
    })
    scenarios.append({
        "id": "HYD-078",
        "category": "budget_tiers",
        "title": "Buyer with 1200 UAH budget (just below lowest hydration set at 1225 UAH)",
        "request": {"goal_group": "hydration", "activity": "running", "max_price_uah": 1200, "locale": "uk"},
        "expected_domain": "Near-miss: RE11650 (1239 UAH) or RE11786 (1285 UAH)",
        "persona": "Runner with 1200 UAH budget probing near-miss threshold"
    })
    scenarios.append({
        "id": "HYD-079",
        "category": "budget_tiers",
        "title": "Medium budget buyer with 1250 UAH seeking legitimate hydration",
        "request": {"goal_group": "hydration", "activity": "running", "max_price_uah": 1250, "locale": "uk"},
        "expected_domain": "RE11650 «Захист від спеки» (1239 UAH)",
        "persona": "Runner with exact budget allowing RE11650 match"
    })
    scenarios.append({
        "id": "HYD-080",
        "category": "budget_tiers",
        "title": "Medium budget runner with 1350 UAH seeking electrolyte pack",
        "request": {"goal_group": "hydration", "activity": "running", "max_price_uah": 1350, "locale": "uk"},
        "expected_domain": "RE11650 (1239 UAH) or RE11786 (1285 UAH)",
        "persona": "Runner with 1350 UAH budget"
    })
    scenarios.append({
        "id": "HYD-081",
        "category": "budget_tiers",
        "title": "Medium budget cyclist with 1450 UAH seeking hydration bundle with bottle",
        "request": {"goal_group": "hydration", "activity": "cycling", "component_class": "sports_accessories", "max_price_uah": 1450, "locale": "uk"},
        "expected_domain": "Nabir_1123 (1435 UAH)",
        "persona": "Cyclist with 1450 UAH budget buying bottle + electrolytes"
    })
    scenarios.append({
        "id": "HYD-082",
        "category": "budget_tiers",
        "title": "Standard catalog budget with 1500 UAH seeking premium electrolyte supply",
        "request": {"goal_group": "hydration", "activity": "running", "component_class": "hydration_items", "max_price_uah": 1500, "locale": "uk"},
        "expected_domain": "Nabir_1015 (20 sticks Hydria Perform) or RE88946 (Hydria Daily + SiS)",
        "persona": "Runner utilizing standard 1500 UAH store credit"
    })
    scenarios.append({
        "id": "HYD-083",
        "category": "budget_tiers",
        "title": "Medium-high budget runner with 1600 UAH seeking race hydration pack",
        "request": {"goal_group": "hydration", "activity": "running", "use_scenario": "event_preparation", "max_price_uah": 1600, "locale": "uk"},
        "expected_domain": "Nabir_1123, RE88946, or RE11804",
        "persona": "Marathon competitor with 1600 UAH budget"
    })
    scenarios.append({
        "id": "HYD-084",
        "category": "budget_tiers",
        "title": "High budget athlete with 2000 UAH looking for complete hydration and nutrition setup",
        "request": {"goal_group": "hydration", "activity": "running", "max_price_uah": 2000, "locale": "uk"},
        "expected_domain": "UT-PRO-2026 (1650 UAH) or Nabir_1015",
        "persona": "Competitive athlete with generous 2000 UAH budget"
    })
    scenarios.append({
        "id": "HYD-085",
        "category": "budget_tiers",
        "title": "Premium budget ultra-runner with 3000 UAH seeking top-tier hydration and gear",
        "request": {"goal_group": "hydration", "activity": "running", "max_price_uah": 3000, "locale": "uk"},
        "expected_domain": "UT-PRO-2026 (1650 UAH)",
        "persona": "Sponsored ultra-runner with 3000 UAH budget"
    })

    # ------------------------------------------------------------------------
    # Category 6: Product Forms, Activities & Taxonomy Leak Probes (86-100)
    # ------------------------------------------------------------------------
    scenarios.append({
        "id": "HYD-086",
        "category": "forms_activities_leaks",
        "title": "Buyer asking explicitly for product_form: 'sticks' (Hydria Perform / Daily sticks)",
        "request": {"goal_group": "hydration", "product_form": "sticks", "max_price_uah": 1500, "locale": "uk"},
        "expected_domain": "Nabir_1015, Nabir_1123, RE88946",
        "persona": "Buyer wanting portable portioned electrolyte sticks"
    })
    scenarios.append({
        "id": "HYD-087",
        "category": "forms_activities_leaks",
        "title": "Buyer asking explicitly for product_form: 'tablets' (Precision Hydration 1000 / SIS Go Hydro effervescent tablets)",
        "request": {"goal_group": "hydration", "product_form": "tablets", "max_price_uah": 1500, "locale": "uk"},
        "expected_domain": "Precision Hydration 1000 Tube (10 tablets) or SIS Go Hydro effervescent tablets",
        "persona": "Runner preferring dissolvable effervescent electrolyte tablets over powder"
    })
    scenarios.append({
        "id": "HYD-088",
        "category": "forms_activities_leaks",
        "title": "Buyer asking explicitly for product_form: 'powder' (bulk electrolyte powder / amino mix)",
        "request": {"goal_group": "hydration", "product_form": "powder", "max_price_uah": 1500, "locale": "uk"},
        "expected_domain": "Nutriversum EAA/BCAA powder formulas (RE11802, RE11786)",
        "persona": "Gym athlete wanting powder hydration to scoop into shaker"
    })
    scenarios.append({
        "id": "HYD-089",
        "category": "forms_activities_leaks",
        "title": "Buyer asking explicitly for product_form: 'gel' (electrolyte gels SiS Go + Electrolyte)",
        "request": {"goal_group": "hydration", "product_form": "gel", "max_price_uah": 1500, "locale": "uk"},
        "expected_domain": "RE88946 (SiS Go + Electrolyte gels 60ml x4)",
        "persona": "Runner wanting fluid electrolyte gels during races"
    })
    scenarios.append({
        "id": "HYD-090",
        "category": "forms_activities_leaks",
        "title": "Buyer asking explicitly for product_form: 'liquid' (ready-to-drink hydration shot)",
        "request": {"goal_group": "hydration", "product_form": "liquid", "max_price_uah": 1500, "locale": "uk"},
        "expected_domain": "RE11787 (Olimp BCAA shot) or RE11806 (liquid cordyceps)",
        "persona": "Athlete wanting liquid shot hydration"
    })
    scenarios.append({
        "id": "HYD-091",
        "category": "forms_activities_leaks",
        "title": "Buyer asking explicitly for product_form: 'flasks' (soft flasks / water flasks)",
        "request": {"goal_group": "hydration", "product_form": "flasks", "max_price_uah": 1500, "locale": "uk"},
        "expected_domain": "Soft flasks or drinking bottles",
        "persona": "Trail runner asking specifically for flask form factor"
    })
    scenarios.append({
        "id": "HYD-092",
        "category": "forms_activities_leaks",
        "title": "Hiker asking for hydration during mountain hike (activity: 'hiking')",
        "request": {"goal_group": "hydration", "activity": "hiking", "max_price_uah": 1700, "locale": "uk"},
        "expected_domain": "UT-PRO-2026 or portable hydration kits for trekking",
        "persona": "Backpacker climbing Hoverla in summer carrying heavy backpack"
    })
    scenarios.append({
        "id": "HYD-093",
        "category": "forms_activities_leaks",
        "title": "Triathlete asking for hydration for triathlon race (activity: 'triathlon')",
        "request": {"goal_group": "hydration", "activity": "triathlon", "max_price_uah": 1600, "locale": "uk"},
        "expected_domain": "Multi-sport endurance hydration kit",
        "persona": "Triathlete competing in sprint triathlon"
    })
    scenarios.append({
        "id": "HYD-094",
        "category": "forms_activities_leaks",
        "title": "Gym athlete asking for hydration during strength training (activity: 'strength_training')",
        "request": {"goal_group": "hydration", "activity": "strength_training", "max_price_uah": 1500, "locale": "uk"},
        "expected_domain": "RE11786 or RE11802 (Intra-workout hydration with shaker)",
        "persona": "Gym athlete doing intense squat session needing intra-workout hydration"
    })
    scenarios.append({
        "id": "HYD-095",
        "category": "forms_activities_leaks",
        "title": "Functional training athlete asking for hydration during CrossFit (activity: 'functional_training')",
        "request": {"goal_group": "hydration", "activity": "functional_training", "max_price_uah": 1500, "locale": "uk"},
        "expected_domain": "Electrolyte replenishment for intense HIIT / CrossFit WODs",
        "persona": "CrossFit athlete sweating heavily during Murph workout"
    })
    scenarios.append({
        "id": "HYD-096",
        "category": "forms_activities_leaks",
        "title": "Walker asking for hydration on 20km brisk walk (activity: 'walking')",
        "request": {"goal_group": "hydration", "activity": "walking", "max_price_uah": 1500, "locale": "uk"},
        "expected_domain": "Portable water bottle + light electrolytes",
        "persona": "Nordic walker doing long endurance walks in countryside"
    })
    scenarios.append({
        "id": "HYD-097",
        "category": "forms_activities_leaks",
        "title": "Pure hydration seeker probing for Spirulina leak (checking if RE11513 is returned)",
        "request": {"goal_group": "hydration", "activity": "running", "component_class": "supplements_vitamins_minerals", "max_price_uah": 1500, "locale": "uk"},
        "expected_domain": "Electrolyte minerals, NOT spirulina algae pills (RE11513)",
        "persona": "Runner needing electrolyte minerals, evaluating if algae tablets leak into hydration"
    })
    scenarios.append({
        "id": "HYD-098",
        "category": "forms_activities_leaks",
        "title": "Pure hydration seeker probing for Lion's Mane / mushroom leak (checking if RE88943 is returned)",
        "request": {"goal_group": "hydration", "use_timing": "daily_use", "max_price_uah": 1500, "locale": "uk"},
        "expected_domain": "Hydria Daily mineral balance, NOT medicinal mushroom nootropics (RE88943)",
        "persona": "Buyer asking for daily hydration, checking if 60 capsules of Lion's Mane mushroom leak"
    })
    scenarios.append({
        "id": "HYD-099",
        "category": "forms_activities_leaks",
        "title": "Pure hydration seeker probing for Creatine leak (checking if RE11681 or RE11636 is returned)",
        "request": {"goal_group": "hydration", "max_price_uah": 1500, "locale": "uk"},
        "expected_domain": "Genuine hydration kits, NOT 500g bodybuilding creatine monohydrate",
        "persona": "Buyer choosing 'Hydration' goal without filters, checking if #1 recommendation is creatine"
    })
    scenarios.append({
        "id": "HYD-100",
        "category": "forms_activities_leaks",
        "title": "Thirsty runner asking for hydration items only (probing for pure socks/towel kits RE11013, RE89475)",
        "request": {"goal_group": "hydration", "activity": "running", "max_price_uah": 1400, "locale": "uk"},
        "expected_domain": "Sets with real electrolytes, NOT bundles of 2 pairs of socks and empty bottles",
        "persona": "Runner checking if clothing/sock kits leak into hydration results"
    })

    return scenarios

# Evaluation logic
def evaluate_scenario(case, res, exc=None):
    cid = case["id"]
    req = case["request"]
    cat = case["category"]
    title = case["title"]

    verdict = "PASS"
    flaws = []
    c1_notes = []
    c2_notes = []
    c3_notes = []
    c4_notes = []

    # 1. Check if engine crashed / threw DraftMatchError
    if exc is not None:
        verdict = "FAIL"
        err_msg = str(exc)
        flaw = f"CRITICAL CRASH: Engine threw DraftMatchError on valid human query: '{err_msg}'"
        flaws.append(flaw)
        return {
            "verdict": verdict,
            "status": "crash",
            "results_count": 0,
            "top_sku": None,
            "top_title": None,
            "top_price": None,
            "flaws": flaws,
            "notes": [f"Request failed with validation exception: {err_msg}"]
        }

    status = res.get("status")
    results = res.get("results", [])
    near_miss = res.get("near_miss_results", [])
    floor_anchor = res.get("floor_anchor_results", [])

    # Check for empty results due to activity taxonomy failure
    act = req.get("activity")
    if act in ("strength_training", "functional_training") and not results and status in ("no_match", "no_exact_match"):
        verdict = "FAIL"
        flaw = f"TAXONOMY BUG: Activity '{act}' returned 0 results. Catalog sets use 'fitness_gym', but engine has no mapping from '{act}' to gym sets."
        flaws.append(flaw)
        return {
            "verdict": verdict,
            "status": status,
            "results_count": 0,
            "top_sku": None,
            "top_title": None,
            "top_price": None,
            "flaws": flaws,
            "notes": [f"Legitimate hydration query for {act} failed with 0 results."]
        }

    items_to_eval = results if results else (near_miss if near_miss else floor_anchor)

    # Budget edge cases (<1000 UAH)
    budget = req.get("max_price_uah")
    if not results:
        if budget is not None and budget < 1225:
            # Below catalog minimum for hydration (1225 UAH)
            if floor_anchor or near_miss:
                top_item = (floor_anchor or near_miss)[0]
                top_sku = top_item.get("sku")
                top_title = top_item.get("title")
                # Check if floor anchor is a creatine leak!
                if top_sku in ("RE11681", "RE11636", "RE11787", "Nabir_1128"):
                    verdict = "FAIL"
                    flaw = f"ABSURD FLOOR ANCHOR: At budget {budget} UAH, engine recommended '{top_title}' ({top_sku}) which contains 500g Creatine Monohydrate as floor anchor for hydration!"
                    flaws.append(flaw)
                else:
                    verdict = "WARN"
                    c1_notes.append(f"Catalog Coverage Gap: Budget {budget} UAH returned 0 exact matches. Store has no single electrolyte packs under 1225 UAH. Suggested near-miss: '{top_title}'.")
                return {
                    "verdict": verdict,
                    "status": status,
                    "results_count": 0,
                    "top_sku": top_sku,
                    "top_title": top_title,
                    "top_price": top_item.get("price_uah"),
                    "flaws": flaws,
                    "notes": c1_notes
                }
            else:
                verdict = "FAIL"
                flaws.append(f"Empty results and no floor anchor/near miss for budget {budget} UAH.")
                return {
                    "verdict": verdict,
                    "status": status,
                    "results_count": 0,
                    "top_sku": None,
                    "top_title": None,
                    "top_price": None,
                    "flaws": flaws,
                    "notes": ["0 results returned."]
                }
        else:
            verdict = "FAIL"
            flaws.append(f"Empty results at reasonable budget {budget} UAH.")
            return {
                "verdict": verdict,
                "status": status,
                "results_count": 0,
                "top_sku": None,
                "top_title": None,
                "top_price": None,
                "flaws": flaws,
                "notes": ["0 results returned."]
            }

    # Now evaluate returned items
    top = items_to_eval[0]
    top_sku = top.get("sku")
    top_title = top.get("title")
    top_price = top.get("price_uah")
    why_suitable = top.get("why_suitable", "")
    comp_raw = str(top.get("composition_raw", "") or top.get("composition", ""))

    # Check for blatant non-hydration leaks in top recommendation
    # A. Creatine Monohydrate leak
    if any(k in comp_raw.lower() for k in ["creatine monohydrate", "креатин", "бодибилдинг"]):
        verdict = "FAIL"
        flaw = f"CREATINE LEAK: Top recommendation '{top_title}' ({top_sku}) contains 500g Creatine Monohydrate! Recommending bodybuilding muscle-growth powder for a hydration query is a severe domain error."
        flaws.append(flaw)

    # B. Spirulina leak
    if "spirulin" in comp_raw.lower() or "спирулин" in comp_raw.lower():
        verdict = "FAIL"
        flaw = f"SPIRULINA LEAK: Top recommendation '{top_title}' ({top_sku}) contains 100 tablets of Now Foods Organic Spirulina algae pills! Algae has zero electrolyte hydration value."
        flaws.append(flaw)

    # C. Lion's Mane / Medicinal Mushrooms leak
    if any(m in comp_raw.lower() for m in ["lion's-mane", "ежовик", "cordyceps", "кордицепс", "reishi", "рейши", "шиитаке"]):
        verdict = "FAIL"
        flaw = f"MUSHROOM/NOOTROPIC LEAK: Top recommendation '{top_title}' ({top_sku}) contains Lion's Mane / Cordyceps medicinal mushroom capsules! Nootropics do not provide fluid/electrolyte hydration."
        flaws.append(flaw)

    # D. Pure apparel/gear with zero electrolytes
    if top_sku in ("RE11013", "RE89475", "RE11801"):
        verdict = "FAIL"
        flaw = f"APPAREL LEAK (0 ELECTROLYTES): Top recommendation '{top_title}' ({top_sku}) contains socks, caps, and an empty bottle with ZERO electrolytes!"
        flaws.append(flaw)

    # E. Deceptive Explanation: (без сторонніх речей)
    if "(без сторонніх речей)" in why_suitable or "(без посторонних вещей)" in why_suitable:
        # Check if set actually contains extraneous non-hydration items
        has_extraneous = False
        extraneous_items = []
        if any(k in comp_raw.lower() for k in ["носки", "шкарпет", "socks"]):
            has_extraneous = True
            extraneous_items.append("носки")
        if any(k in comp_raw.lower() for k in ["полотенце", "рушник", "towel"]):
            has_extraneous = True
            extraneous_items.append("банне рушник")
        if any(k in comp_raw.lower() for k in ["абонемент"]):
            has_extraneous = True
            extraneous_items.append("абонемент на 3 місяці")
        if any(k in comp_raw.lower() for k in ["lion's-mane", "ежовик", "mushroom", "гриб"]):
            has_extraneous = True
            extraneous_items.append("гриби / ноотропи")
        if any(k in comp_raw.lower() for k in ["creatine", "креатин"]):
            has_extraneous = True
            extraneous_items.append("креатин")

        if has_extraneous:
            verdict = "FAIL"
            flaw = f"DECEPTIVE EXPLANATION: Matcher claimed '(без сторонніх речей)', but kit '{top_title}' ({top_sku}) actually contains: {', '.join(extraneous_items)}."
            flaws.append(flaw)

    # Check for domain-specific scenario expectations:
    if cat == "high_heat_cramps":
        # Expecting high sodium / cramp defense (Precision Hydration 1000 or Hydria Perform)
        has_sodium = any(k in comp_raw.lower() for k in ["precision hydration", "hydria perform", "электролит", "електроліт"])
        if not has_sodium and verdict != "FAIL":
            verdict = "WARN"
            c1_notes.append(f"Suboptimal cramp match: Expected high-sodium electrolytes (Precision Hydration 1000 or Hydria Perform), got '{top_title}'.")
        elif verdict == "PASS":
            c1_notes.append(f"Successfully matched high-electrolyte formula: '{top_title}' ({top_sku}).")

    elif cat == "daily_mineral_balance":
        # Expecting Hydria Daily or gentle electrolytes
        has_daily = "hydria daily" in comp_raw.lower() or "hydria perform" in comp_raw.lower()
        if not has_daily and verdict != "FAIL":
            verdict = "WARN"
            c1_notes.append(f"Expected daily mineral formula (Hydria Daily), got '{top_title}'.")
        elif verdict == "PASS":
            # If contains club membership or socks, downgrade to WARN
            if "абонемент" in comp_raw.lower() or "носки" in comp_raw.lower():
                verdict = "WARN"
                c1_notes.append(f"Contains Hydria electrolytes but bundled with club membership/socks in '{top_title}'.")
            else:
                c1_notes.append(f"Clean daily mineral match: '{top_title}'.")

    elif cat == "endurance_amino_hydration":
        # Expecting SIS Go Hydro, Nutriversum EAA/BCAA, or Hydria Perform
        has_endurance = any(k in comp_raw.lower() for k in ["sis go", "nutriversum", "hydria perform", "beta fuel"])
        if not has_endurance and verdict != "FAIL":
            verdict = "WARN"
            c1_notes.append(f"Expected endurance race hydration (SIS / Nutriversum EAA), got '{top_title}'.")
        elif verdict == "PASS":
            c1_notes.append(f"Clean endurance hydration match: '{top_title}' ({top_sku}).")

    elif cat == "flasks_bottles_gear":
        # Expecting bottle / shaker + electrolytes
        has_bottle = any(k in comp_raw.lower() for k in ["бутылка", "пляшка", "шейкер", "shaker"])
        if not has_bottle and verdict != "FAIL":
            verdict = "WARN"
            c1_notes.append(f"Expected drinking bottle or shaker in bundle, but '{top_title}' has no bottle.")
        elif verdict == "PASS":
            # Check if soft flasks requested (catalog only has hard bottles/shakers)
            if "soft flask" in title.lower():
                verdict = "WARN"
                c1_notes.append("Catalog has hard bottles (530ml glass, 600ml plastic, shakers), but NO soft flasks for running vests.")
            else:
                c1_notes.append(f"Matched bottle hydration bundle: '{top_title}'.")

    if verdict == "PASS" and ("абонемент" in comp_raw.lower() or "носки" in comp_raw.lower() or "рушник" in comp_raw.lower()):
        # Downgrade to WARN if bundled with club subscription or apparel
        verdict = "WARN"
        c1_notes.append(f"Valid hydration product present, but bundled with club membership or apparel in '{top_title}'.")

    return {
        "verdict": verdict,
        "status": status,
        "results_count": len(results),
        "top_sku": top_sku,
        "top_title": top_title,
        "top_price": top_price,
        "flaws": flaws,
        "notes": c1_notes
    }

# Main execution
def main():
    scenarios = build_100_scenarios()
    print(f"Executing {len(scenarios)} hydration test scenarios...")

    runs = []
    verdict_counts = {"PASS": 0, "WARN": 0, "FAIL": 0}
    category_counts = {}

    for i, case in enumerate(scenarios, 1):
        req = case["request"]
        cat = case["category"]
        if cat not in category_counts:
            category_counts[cat] = {"total": 0, "PASS": 0, "WARN": 0, "FAIL": 0}
        category_counts[cat]["total"] += 1

        engine_res = None
        engine_exc = None
        try:
            engine_res = draft_recommend(catalog, req)
        except Exception as e:
            engine_exc = e

        evaluation = evaluate_scenario(case, engine_res, engine_exc)
        v = evaluation["verdict"]
        verdict_counts[v] += 1
        category_counts[cat][v] += 1

        runs.append({
            "case_id": case["id"],
            "category": cat,
            "title": case["title"],
            "persona": case["persona"],
            "request": req,
            "engine_response": {
                "status": evaluation.get("status"),
                "returned_count": len(engine_res.get("results", [])) if engine_res else 0,
                "top_sku": evaluation.get("top_sku"),
                "top_title": evaluation.get("top_title"),
                "top_price": evaluation.get("top_price"),
                "results": engine_res.get("results", [])[:3] if engine_res else [],
                "near_miss_results": engine_res.get("near_miss_results", [])[:3] if engine_res else [],
                "floor_anchor_results": engine_res.get("floor_anchor_results", [])[:3] if engine_res else [],
                "error": str(engine_exc) if engine_exc else None
            },
            "evaluation": evaluation
        })

        if i % 20 == 0 or i == len(scenarios):
            print(f"Processed {i}/{len(scenarios)} cases. Current counts: PASS={verdict_counts['PASS']}, WARN={verdict_counts['WARN']}, FAIL={verdict_counts['FAIL']}")

    # Save JSON results
    out_json = {
        "test_suite": "QA Deep Hydration Specialist 100 Tests",
        "date": datetime.now().strftime("%Y-%m-%d"),
        "total_cases": len(scenarios),
        "summary": verdict_counts,
        "category_summary": category_counts,
        "runs": runs
    }

    json_path = ROOT / "agent_deep_hydration_100_tests.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(out_json, f, ensure_ascii=False, indent=2)
    print(f"Saved JSON results to {json_path}")

    # Build detailed Markdown Report
    report_md = build_markdown_report(out_json)
    md_path = ROOT / "agent_deep_hydration_report.md"
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(report_md)
    print(f"Saved Markdown report to {md_path}")

def build_markdown_report(data):
    summary = data["summary"]
    cats = data["category_summary"]
    runs = data["runs"]
    total = data["total_cases"]

    pass_pct = (summary["PASS"] / total) * 100
    warn_pct = (summary["WARN"] / total) * 100
    fail_pct = (summary["FAIL"] / total) * 100

    md = f"""# QA Specialist Deep Audit Report: Hydration & Electrolytes (`hydration`)
**Auditor:** QA Specialist for "Hydration & Electrolytes"  
**Catalog Source:** `wiki/projects/quiz-set-audit.json` (207 sets snapshot)  
**Execution Date:** {data['date']}  
**Test Suite:** 100 Dedicated Buyer Scenarios strictly for `goal_group: "hydration"`  

---

## 1. Executive Summary & Verdict Scorecard

Across 100 dedicated buyer test scenarios covering high heat / heavy sweat, daily mineral balance, endurance race hydration + amino acids, soft flasks and water bottles, budget tiers, and product form factors:
- **PASS:** {summary['PASS']} ({pass_pct:.1f}%) — Clean, accurate hydration match with legitimate electrolytes, no deceptive claims, and correct pricing.
- **WARN:** {summary['WARN']} ({warn_pct:.1f}%) — Partially relevant match (e.g. genuine Hydria electrolytes bundled with a 3-month gym club membership, socks, or bath towel; catalog coverage gap under 1225 UAH; or missing soft flask inventory).
- **FAIL:** {summary['FAIL']} ({fail_pct:.1f}%) — Critical human-logic flaws, including engine crashes, 0-result taxonomy bugs, massive non-hydration product leaks (500g Creatine Monohydrate, Spirulina, Lion's Mane), and deceptive `(без сторонніх речей)` claims.

### Category Breakdown

| Category | Total Scenarios | PASS | WARN | FAIL | Pass Rate |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **High Heat / Heavy Sweat / Cramps** | {cats.get('high_heat_cramps', {}).get('total', 0)} | {cats.get('high_heat_cramps', {}).get('PASS', 0)} | {cats.get('high_heat_cramps', {}).get('WARN', 0)} | {cats.get('high_heat_cramps', {}).get('FAIL', 0)} | {cats.get('high_heat_cramps', {}).get('PASS', 0) / max(1, cats.get('high_heat_cramps', {}).get('total', 1)) * 100:.1f}% |
| **General Daily Mineral Balance** | {cats.get('daily_mineral_balance', {}).get('total', 0)} | {cats.get('daily_mineral_balance', {}).get('PASS', 0)} | {cats.get('daily_mineral_balance', {}).get('WARN', 0)} | {cats.get('daily_mineral_balance', {}).get('FAIL', 0)} | {cats.get('daily_mineral_balance', {}).get('PASS', 0) / max(1, cats.get('daily_mineral_balance', {}).get('total', 1)) * 100:.1f}% |
| **Endurance Race Hydration + Amino Acids** | {cats.get('endurance_amino_hydration', {}).get('total', 0)} | {cats.get('endurance_amino_hydration', {}).get('PASS', 0)} | {cats.get('endurance_amino_hydration', {}).get('WARN', 0)} | {cats.get('endurance_amino_hydration', {}).get('FAIL', 0)} | {cats.get('endurance_amino_hydration', {}).get('PASS', 0) / max(1, cats.get('endurance_amino_hydration', {}).get('total', 1)) * 100:.1f}% |
| **Soft Flasks, Bottles & Hydration Gear** | {cats.get('flasks_bottles_gear', {}).get('total', 0)} | {cats.get('flasks_bottles_gear', {}).get('PASS', 0)} | {cats.get('flasks_bottles_gear', {}).get('WARN', 0)} | {cats.get('flasks_bottles_gear', {}).get('FAIL', 0)} | {cats.get('flasks_bottles_gear', {}).get('PASS', 0) / max(1, cats.get('flasks_bottles_gear', {}).get('total', 1)) * 100:.1f}% |
| **Budget Tiers (<1000, 1000–1600, >1600 UAH)** | {cats.get('budget_tiers', {}).get('total', 0)} | {cats.get('budget_tiers', {}).get('PASS', 0)} | {cats.get('budget_tiers', {}).get('WARN', 0)} | {cats.get('budget_tiers', {}).get('FAIL', 0)} | {cats.get('budget_tiers', {}).get('PASS', 0) / max(1, cats.get('budget_tiers', {}).get('total', 1)) * 100:.1f}% |
| **Product Forms, Activities & Leak Probes** | {cats.get('forms_activities_leaks', {}).get('total', 0)} | {cats.get('forms_activities_leaks', {}).get('PASS', 0)} | {cats.get('forms_activities_leaks', {}).get('WARN', 0)} | {cats.get('forms_activities_leaks', {}).get('FAIL', 0)} | {cats.get('forms_activities_leaks', {}).get('PASS', 0) / max(1, cats.get('forms_activities_leaks', {}).get('total', 1)) * 100:.1f}% |
| **TOTAL** | **{total}** | **{summary['PASS']}** | **{summary['WARN']}** | **{summary['FAIL']}** | **{pass_pct:.1f}%** |

---

## 2. Deep Dive: Discovered Human-Logic Flaws & Bugs

### A. The #1 Creatine Default Leak (Absurd Recommendation for Generic Hydration)
> [!CAUTION]
> When a buyer clicks **"Гідратація" (Hydration)** with no restrictive filters, the engine's **#1 recommendation is RE11681 «Ріст м'язів» (Muscle Growth)** at 1225 UAH!
- **Actual Composition of RE11681:** 500g Bodyperson Creatine Monohydrate, Lipobar protein bars x2, Brave U shaker 700ml, 3-month gym club membership, and only 4 sticks of Hydria Daily.
- **Why it happens:** In `wiki/projects/quiz-set-audit.json`, because RE11681 contains 4 sticks of Hydria Daily, it was awarded `hydration_electrolytes` in both `seller_families` and `component_families`. Because its price (1225 UAH) is the absolute lowest among all sets tagged with hydration, `draft_matcher` sorts it first!
- **Customer Experience:** A dehydrated runner or cyclist asking for hydration is told to buy a heavy 500g bodybuilding creatine muscle mass gainer tub.

### B. Severe Non-Hydration Product Leaks: Spirulina, Mushrooms & Footwear
The catalog evidence pool permits inappropriate non-hydration products to infiltrate the `hydration` results:
1. **Spirulina Algae Leak (RE11513 «Енергія і очищення», 1455 UAH):**
   - Contains: **Now Foods Organic Spirulina (100 tablets)**, Zinc Picolinate (60 caps), Omega-3 (60 softgels), and 5 sticks of Hydria Perform.
   - Recommended when users filter for vitamins/minerals under hydration. Spirulina algae tablets have zero electrolyte replenishment capability.
2. **Lion's Mane / Nootropic Mushroom Leak (RE88943 «Концентрація в дорозі», 1469 UAH):**
   - Contains: **Lion's Mane 700mg (60 capsules)**, Acetyl-L-Carnitine (50 caps), and 3 Hydria sticks. Recommending medicinal brain mushrooms to an athlete seeking hydration is completely illogical.
3. **Pure Socks Bundles with 0 Electrolytes (RE11013 «Бігова пара», 1359 UAH; RE89475 «Бігова екіпіровка», 1415 UAH):**
   - RE11013 contains: 2 pairs of Race Expert socks and 1 glass bottle. It contains **ZERO electrolytes, zero powders, zero tablets**. Recommending socks to someone asking for hydration is a severe classification defect.

### C. The Hiker, Triathlete & Walker Validation Wall (`DraftMatchError` Crash)
> [!WARNING]
> In `draft_matcher.py`, `ACTIVITY_OPTIONS_BY_GOAL["hydration"]` is strictly hardcoded to:
> `{"running", "cycling", "strength_training", "functional_training"}`.
- If a **hiker** selects `activity: "hiking"` under hydration, the engine crashes with:  
  `DraftMatchError: activity is not supported for the selected need.`
- If a **triathlete** selects `activity: "triathlon"`, the engine crashes.
- If a **walker** selects `activity: "walking"`, the engine crashes.
- **Human Logic Irony:** The catalog literally contains `UT-PRO-2026` («Ultra Trail Marathon Energy & Hydration Pro»), whose audited activity scope explicitly includes `hiking`! Yet a hiker is rejected by the validation gate.

### D. Activity Taxonomy Bug: 0 Results for Strength & Functional Training
- While `draft_matcher.py` accepts `strength_training` and `functional_training` as options for `hydration`, in `quiz-set-audit.json` all gym sets have `activity_groups: ["fitness_gym"]`.
- Because there is no taxonomic translation between `strength_training` / `functional_training` and `fitness_gym`, the filter `_candidate_fit` treats them as disjoint.
- **Outcome:** Any gym athlete asking for intra-workout hydration receives **0 matches (`status: no_match`)**, even though sets like RE11786 and RE11802 contain shakers, BCAA/EAA, and Hydria Perform specifically designed for gym training.

### E. Product Form Validation Blockade: Effervescent Tablets, Powders & Soft Flasks
- In `draft_matcher.py`, `PRODUCT_FORMS_BY_GOAL["hydration"]` is set to:  
  `{"liquid", "gel", "bars", "sticks"}`.
- Notice that it includes **`bars`** (which are solid food, not hydration drinks), but completely excludes **`tablets`** and **`powder`**!
- If a buyer selects `product_form: "tablets"`, the engine throws `DraftMatchError: product_form is not supported`. Yet two of the most prominent hydration sets in the store (`RE11650` Precision Hydration 1000 Tube and `UT-PRO-2026` SIS Go Hydro) are **effervescent tablets**!
- If a buyer selects `product_form: "powder"`, the engine crashes, even though Nutriversum EAA and BCAA are bulk hydration powders.
- If a buyer asks for `product_form: "flasks"`, the engine crashes. Furthermore, the catalog contains zero soft flasks (only hard plastic/glass bottles and shakers).

### F. Deceptive Justification Claims: `(без сторонніх речей)`
- The explanation generator `_build_why_suitable()` frequently outputs:  
  `Категорія товарів: у наборі саме Ізотоніки та електроліти (без сторонніх речей).`
- In reality, almost every hydration kit in the catalog includes extraneous items: 3-month gym club memberships, pairs of socks, 500g tubs of creatine, or medicinal mushrooms.
- Promising "without extraneous items" when the set is dominated by unrelated items destroys user trust.

### G. Low Budget Desert (< 1225 UAH)
- The absolute cheapest kit in the catalog matching hydration is RE11681 at 1225 UAH (or RE11650 at 1239 UAH).
- Any buyer with a realistic budget between 300 and 1000 UAH receives zero exact matches.
- For budgets below 1000 UAH, the engine's `floor_anchor` currently serves `RE11681` (Creatine Monohydrate), creating a catastrophic failure where low-budget hydration shoppers are told to buy a 1225 UAH bodybuilding creatine kit.

---

## 3. Detailed Results of all 100 Test Scenarios

| ID | Title | Category | Activity | Form | Budget | Status | Verdict | Top Recommended SKU & Notes |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :--- |
"""

    for r in runs:
        cid = r["case_id"]
        title = r["title"]
        cat = r["category"]
        req = r["request"]
        act = req.get("activity", "—")
        form = req.get("product_form", "—")
        budget = f"{req.get('max_price_uah', '—')} ₴"
        eng = r["engine_response"]
        status = eng.get("status", "error")
        ev = r["evaluation"]
        v = ev["verdict"]
        top_sku = eng.get("top_sku") or "None"
        
        # Summary note
        note = ""
        if ev.get("flaws"):
            note = ev["flaws"][0]
        elif ev.get("notes"):
            note = ev["notes"][0]
        else:
            note = f"Matched: {top_sku}"
        
        # Truncate note for clean markdown table
        note_clean = note.replace("|", "/").replace("\n", " ")[:110]
        if len(note) > 110:
            note_clean += "…"

        md += f"| {cid} | {title} | `{cat}` | {act} | {form} | {budget} | `{status}` | **{v}** | [{top_sku}]: {note_clean} |\n"

    md += """
---

## 4. Prioritized Recommendations for Engineering & Merchandising

1. **Purge False Hydration Tags on Bodybuilding & Nootropic Sets:**
   - Remove `hydration_electrolytes` from `RE11681` («Ріст м'язів»), `RE11636` («Вибух сили»), and `RE11787` («Сила та гідратація»). Having 4 sticks of Hydria Daily inside a 500g Creatine kit should NOT make it a primary hydration kit.
   - Remove `hydration_electrolytes` from `RE11513` (Spirulina) and `RE88943` (Lion's Mane mushroom).
   - Remove `hydration_electrolytes` from pure apparel sets `RE11013` and `RE89475`.

2. **Add `tablets` and `powder` to `PRODUCT_FORMS_BY_GOAL["hydration"]`:**
   - Update `draft_matcher.py`:
     ```python
     PRODUCT_FORMS_BY_GOAL["hydration"] = {"tablets", "powder", "sticks", "gel", "liquid"}
     ```
   - Map `Precision Hydration 1000 Tube` and `SIS Go Hydro` to `tablets`.
   - Remove `bars` from hydration (bars are food).

3. **Expand `ACTIVITY_OPTIONS_BY_GOAL["hydration"]` to Include Hiking and Triathlon:**
   - Update `draft_matcher.py`:
     ```python
     ACTIVITY_OPTIONS_BY_GOAL["hydration"] = {"running", "cycling", "hiking", "triathlon", "fitness_gym"}
     ```
   - Add alias mapping from `strength_training` and `functional_training` to `fitness_gym`.

4. **Correct Taxonomy for `RE11650` (Precision Hydration 1000):**
   - In `quiz-set-audit.json`, `RE11650` currently has `component_class: ['supplements_vitamins_minerals']`. It must be changed to `component_class: ['hydration_items']`.

5. **Stop Emitting `(без сторонніх речей)` for Bundled Sets:**
   - Suppress this phrase whenever the set includes club memberships, towels, apparel, or secondary supplement classes.

6. **Introduce Dedicated Single-Pack Hydration Offerings (< 1000 UAH):**
   - The store urgently needs entry-level hydration SKUs (e.g., a standalone tube of Precision Hydration 1000 or SIS Go Hydro at 500–600 UAH, or a 10-pack of Hydria Perform at 700 UAH) to capture the large demographic of sub-1000 UAH buyers.
"""
    return md

if __name__ == "__main__":
    main()
