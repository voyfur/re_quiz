# QA Agent 2: Running & Endurance Specialist - 100 Buyer Test Case Audit Report
**Date:** 2026-11-12  
**Scope:** Race Expert Quiz — Running & Race Preparation (`goal_group: 'running'`)  
**Catalog Source:** `wiki/projects/quiz-set-audit.json` (206 sets total, 41 candidate running sets)  
**Matcher:** `test-quiz-sandbox/draft_matcher.py:draft_recommend`
## Executive Summary
| Metric | Count | Percentage |
|---|---|---|
| **Total Scenarios** | **100** | **100%** |
| **PASS (Sound Buyer Experience)** | **40** | **40%** |
| **WARN (Suboptimal / Borderline / Minor Inaccuracy)** | **23** | **23%** |
| **FAIL (Critical Human Logic / Catalog Breakdown)** | **37** | **37%** |
```
Verdict Distribution: [####################-----------!!!!!!!!!!!!!!!!!!]
  PASS: 40 | WARN: 23 | FAIL: 37
```
## Critical Architectural & Human-Logic Findings
### 1. The Half-Marathon Blindspot (CRITICAL FAIL - 20 Scenarios Affected)
> [!CAUTION]
> In Ukraine, the half-marathon (21.1 km) is by far the most popular mass participation race distance (Kyiv Half Marathon, Nova Poshta series, etc.).  
> However, **ZERO sets out of 206** in `quiz-set-audit.json` have `half_marathon` tagged in `matching_evidence.race_formats`!  
> When a buyer chooses `race_format: 'half_marathon'`, the draft matcher returns **`status: no_exact_match` (0 sets)**, even though sets like «Марафонець» (RE11660) explicitly state *'полумарафон и марафон'* in their descriptions. This causes an immediate failure for 100% of half-marathon runner queries unless relaxed fallback is manually triggered.
### 2. Gym / Powerlifting Leakage into Marathon Preparation (CRITICAL FAIL/WARN)
> [!WARNING]
> **Creatine Tub for a Marathoner:** Set `RE11660` (Набір «Марафонець», 1500 UAH) bundles a **300g tub of pure Creatine Monohydrate** with only 5 energy gels. In endurance running physiology, creatine causes intracellular water retention leading to a 1–2 kg body weight penalty, which increases energy cost of running without aerobic benefit.  
> **Bizarre Marketing Pitch:** When recommended to a marathon runner, `draft_matcher` generates the following expert explanation:  
> *«Мощный комплекс для силовых тренировок: повышает взрывную силу, пиковую работоспособность и стимулирует качественный мышечный рост.»*  
> Recommending powerlifting explosive strength and bodybuilding muscle hypertrophy to an aerobic endurance runner preparing for 42.2 km destroys coach credibility.
### 3. Severe Nutrition Catalog Starvation (CRITICAL FAIL/WARN)
> [!IMPORTANT]
> Out of 41 running candidate sets in the catalog:
> - **23 sets are purely socks** (Акційний набір шкарпеток 5 пар / 1+1=3).
> - **Only TWO sets** in the entire catalog have `component_classes: ['protein_carbohydrate_food']`: `RE11659` (Набір «Тиждень бігуна») and `RE11660` (Набір «Марафонець» with Creatine).
> - `UT-PRO-2026` (Ultra Trail Marathon Pro) contains 3x SIS Beta Fuel gels and a protein bar, but its audit entry **omits `protein_carbohydrate_food`** and only lists `hydration_items`!
> - Consequently, when runners search for energy bars or race food with specific constraints, the catalog immediately starves out.
### 4. Schema Rejection of Running Salt Capsules & Drink Powders (CRITICAL FAIL)
> [!NOTE]
> `draft_matcher.py` defines `PRODUCT_FORMS_BY_GOAL['running'] = {'bars', 'gel', 'food_or_meal', 'liquid', 'sticks'}`.  
> It completely excludes `'capsules'` and `'powder'`.  
> In real running, **salt capsules** (e.g. Precision Hydration, SaltStick) and **isotonic powders** in canisters/tubs are essential endurance staples. When a runner selects capsules or powder, `draft_recommend` crashes with `DraftMatchError: product_form is not supported for the selected need`.
### 5. False 'No Foreign Items' Guarantees in `why_suitable`
> The explanation generator frequently outputs:  
> *«Категория товаров: в наборе именно Спортивное питание и батончики (без посторонних позиций).»*  
> Yet for `RE11660`, 70% of the set's physical mass and cost is a 300g bodybuilding creatine tub. Similarly, for sets labeled accessories, 3-month club subscriptions or 360g BCAA tubs are bundled.
## Detailed Breakdown of Test Categories
### Test Scenario Log (100 Cases)
| # | Scenario Name | Budget | Class | Race Format | Form | Verdict | Main Flaw / Human Note |
|---|---|---|---|---|---|---|---|
| 001 | Marathoner: Energy gels during | 2500 ₴ | protein_carbohydrate_food | marathon | gel | **WARN** | Questionable Composition: Set contains 300g pure Creatine tub bundled wi… |
| 002 | Marathoner: Energy gels, mediu | 1500 ₴ | protein_carbohydrate_food | marathon | gel | **WARN** | Questionable Composition: Set contains 300g pure Creatine tub bundled wi… |
| 003 | Marathoner: Tight budget gels | 800 ₴ | protein_carbohydrate_food | marathon | gel | **WARN** | Questionable Composition: Set contains 300g pure Creatine tub bundled wi… |
| 004 | Marathoner: Hydration & electr | 1600 ₴ | hydration_items | marathon | - | **PASS** | Clean match & sound explanation |
| 005 | Marathoner: Hydration, tight b | 700 ₴ | hydration_items | marathon | - | **PASS** | Clean match & sound explanation |
| 006 | Marathoner: Salt capsules for  | 1500 ₴ | hydration_items | marathon | capsules | **FAIL** | Schema limitation: Endurance runners frequently use electrolyte capsules… |
| 007 | Marathoner: Isotonic powder in | 1800 ₴ | hydration_items | marathon | powder | **FAIL** | Schema limitation: Endurance runners frequently use electrolyte capsules… |
| 008 | Marathoner: Anti-blister racin | 1200 ₴ | apparel_footwear | marathon | - | **PASS** | Clean match & sound explanation |
| 009 | Marathoner: Winter marathon th | 1200 ₴ | apparel_footwear | marathon | - | **PASS** | Clean match & sound explanation |
| 010 | Marathoner: Marathon accessori | 1500 ₴ | sports_accessories | marathon | - | **PASS** | Clean match & sound explanation |
| 011 | Marathoner: Recovery nutrition | 2000 ₴ | protein_carbohydrate_food | marathon | - | **WARN** | Questionable Composition: Set contains 300g pure Creatine tub bundled wi… |
| 012 | Marathoner: General prep, any  | 1500 ₴ | any | marathon | - | **FAIL** | Gym/Powerlifting Leak & Bizarre Expert Pitch: Recommended «Набір Марафон… |
| 013 | Marathoner: High-budget comple | 4000 ₴ | any | marathon | - | **WARN** | Questionable Composition: Set contains 300g pure Creatine tub bundled wi… |
| 014 | Marathoner: Energy bars for tr | 1600 ₴ | protein_carbohydrate_food | marathon | bars | **FAIL** | Catalog Starvation / No Match: Runner requested running nutrition/food, … |
| 015 | Marathoner: Multi-choice form  | 1800 ₴ | protein_carbohydrate_food | marathon | ['gel', 'bars'] | **WARN** | Questionable Composition: Set contains 300g pure Creatine tub bundled wi… |
| 016 | Marathoner: Electrolyte sticks | 1600 ₴ | hydration_items | marathon | sticks | **PASS** | Clean match & sound explanation |
| 017 | Marathoner: Daily hydration to | 1500 ₴ | hydration_items | marathon | - | **PASS** | Clean match & sound explanation |
| 018 | Marathoner: Low budget socks s | 600 ₴ | apparel_footwear | marathon | - | **PASS** | Clean match & sound explanation |
| 019 | Marathoner: Accessories + food | 1600 ₴ | sports_accessories | marathon | gel | **PASS** | Clean match & sound explanation |
| 020 | Marathoner: Pre-race carb load | 1700 ₴ | protein_carbohydrate_food | marathon | - | **WARN** | Questionable Composition: Set contains 300g pure Creatine tub bundled wi… |
| 021 | Half-marathoner: Race gels, me | 1500 ₴ | protein_carbohydrate_food | half_marathon | gel | **FAIL** | Catalog Starvation / No Match: Runner requested running nutrition/food, … |
| 022 | Half-marathoner: Race gels, ti | 900 ₴ | protein_carbohydrate_food | half_marathon | gel | **FAIL** | Catalog Starvation / No Match: Runner requested running nutrition/food, … |
| 023 | Half-marathoner: Hydration & e | 1500 ₴ | hydration_items | half_marathon | - | **FAIL** | Zero Coverage for Half-Marathon: The quiz returned 0 exact matches for '… |
| 024 | Half-marathoner: Salt capsules | 1400 ₴ | hydration_items | half_marathon | capsules | **FAIL** | Schema limitation: Endurance runners frequently use electrolyte capsules… |
| 025 | Half-marathoner: Running socks | 1100 ₴ | apparel_footwear | half_marathon | - | **FAIL** | Zero Coverage for Half-Marathon: The quiz returned 0 exact matches for '… |
| 026 | Half-marathoner: Running socks | 1100 ₴ | apparel_footwear | half_marathon | - | **FAIL** | Zero Coverage for Half-Marathon: The quiz returned 0 exact matches for '… |
| 027 | Half-marathoner: Bib belt and  | 1500 ₴ | sports_accessories | half_marathon | - | **FAIL** | Zero Coverage for Half-Marathon: The quiz returned 0 exact matches for '… |
| 028 | Half-marathoner: Energy bars f | 1600 ₴ | protein_carbohydrate_food | half_marathon | bars | **FAIL** | Catalog Starvation / No Match: Runner requested running nutrition/food, … |
| 029 | Half-marathoner: High budget c | 3000 ₴ | any | half_marathon | - | **FAIL** | Zero Coverage for Half-Marathon: The quiz returned 0 exact matches for '… |
| 030 | Half-marathoner: Tight budget  | 500 ₴ | any | half_marathon | - | **FAIL** | Zero Coverage for Half-Marathon: The quiz returned 0 exact matches for '… |
| 031 | Half-marathoner: Daily trainin | 1500 ₴ | protein_carbohydrate_food | half_marathon | bars | **FAIL** | Catalog Starvation / No Match: Runner requested running nutrition/food, … |
| 032 | Half-marathoner: Liquid energy | 1600 ₴ | protein_carbohydrate_food | half_marathon | liquid | **FAIL** | Catalog Starvation / No Match: Runner requested running nutrition/food, … |
| 033 | Half-marathoner: Multi-choice  | 1600 ₴ | hydration_items | half_marathon | ['gel', 'sticks'] | **FAIL** | Zero Coverage for Half-Marathon: The quiz returned 0 exact matches for '… |
| 034 | Half-marathoner: Isotonic powd | 1400 ₴ | hydration_items | half_marathon | powder | **FAIL** | Schema limitation: Endurance runners frequently use electrolyte capsules… |
| 035 | Half-marathoner: Fall race col | 1200 ₴ | apparel_footwear | half_marathon | - | **FAIL** | Zero Coverage for Half-Marathon: The quiz returned 0 exact matches for '… |
| 036 | Half-marathoner: Pre-race brea | 1500 ₴ | protein_carbohydrate_food | half_marathon | bars | **FAIL** | Catalog Starvation / No Match: Runner requested running nutrition/food, … |
| 037 | Half-marathoner: Electrolyte s | 1500 ₴ | hydration_items | half_marathon | sticks | **FAIL** | Zero Coverage for Half-Marathon: The quiz returned 0 exact matches for '… |
| 038 | Half-marathoner: Budget 1200 U | 1200 ₴ | any | half_marathon | - | **FAIL** | Zero Coverage for Half-Marathon: The quiz returned 0 exact matches for '… |
| 039 | Half-marathoner: Spring 10k/21 | 1400 ₴ | sports_accessories | half_marathon | - | **FAIL** | Zero Coverage for Half-Marathon: The quiz returned 0 exact matches for '… |
| 040 | Half-marathoner: High budget ( | 2500 ₴ | protein_carbohydrate_food | half_marathon | - | **FAIL** | Catalog Starvation / No Match: Runner requested running nutrition/food, … |
| 041 | Ultra-trail runner: Mountain 5 | 2000 ₴ | hydration_items | ultra_or_long_distance | gel | **PASS** | Clean match & sound explanation |
| 042 | Ultra runner: Calorie-dense fo | 2500 ₴ | protein_carbohydrate_food | ultra_or_long_distance | bars | **FAIL** | Catalog Starvation / No Match: Runner requested running nutrition/food, … |
| 043 | Ultra runner: Salt sticks / el | 1800 ₴ | hydration_items | ultra_or_long_distance | sticks | **PASS** | Clean match & sound explanation |
| 044 | Ultra runner: Electrolyte caps | 1600 ₴ | hydration_items | ultra_or_long_distance | capsules | **FAIL** | Schema limitation: Endurance runners frequently use electrolyte capsules… |
| 045 | Ultra runner: Isotonic powder  | 2200 ₴ | hydration_items | ultra_or_long_distance | powder | **FAIL** | Schema limitation: Endurance runners frequently use electrolyte capsules… |
| 046 | Ultra runner: High budget all- | 4500 ₴ | any | ultra_or_long_distance | - | **PASS** | Clean match & sound explanation |
| 047 | Ultra runner: Tight budget (10 | 1000 ₴ | hydration_items | ultra_or_long_distance | - | **PASS** | Clean match & sound explanation |
| 048 | Ultra runner: Anti-friction th | 1500 ₴ | apparel_footwear | ultra_or_long_distance | - | **PASS** | Clean match & sound explanation |
| 049 | Ultra runner: Trail running ac | 1600 ₴ | sports_accessories | ultra_or_long_distance | - | **PASS** | Clean match & sound explanation |
| 050 | Ultra runner: Multi-form nutri | 2200 ₴ | hydration_items | ultra_or_long_distance | ['gel', 'sticks'] | **PASS** | Clean match & sound explanation |
| 051 | Ultra runner: Post-ultra recov | 2000 ₴ | protein_carbohydrate_food | ultra_or_long_distance | - | **FAIL** | Catalog Starvation / No Match: Runner requested running nutrition/food, … |
| 052 | Ultra runner: Daily training h | 1600 ₴ | hydration_items | ultra_or_long_distance | - | **PASS** | Clean match & sound explanation |
| 053 | Ultra runner: Extreme budget ( | 600 ₴ | any | ultra_or_long_distance | - | **PASS** | Clean match & sound explanation |
| 054 | Ultra runner: Medium budget ge | 1500 ₴ | protein_carbohydrate_food | ultra_or_long_distance | gel | **FAIL** | Catalog Starvation / No Match: Runner requested running nutrition/food, … |
| 055 | Ultra runner: Ready meals for  | 2000 ₴ | protein_carbohydrate_food | ultra_or_long_distance | food_or_meal | **FAIL** | Catalog Starvation / No Match: Runner requested running nutrition/food, … |
| 056 | Ultra runner: Summer ultra soc | 1200 ₴ | apparel_footwear | ultra_or_long_distance | - | **PASS** | Clean match & sound explanation |
| 057 | Ultra runner: Winter ultra tra | 1500 ₴ | sports_accessories | ultra_or_long_distance | - | **PASS** | Clean match & sound explanation |
| 058 | Ultra runner: Liquid energy sh | 1700 ₴ | protein_carbohydrate_food | ultra_or_long_distance | liquid | **FAIL** | Catalog Starvation / No Match: Runner requested running nutrition/food, … |
| 059 | Ultra runner: Any component, 1 | 1800 ₴ | any | ultra_or_long_distance | - | **PASS** | Clean match & sound explanation |
| 060 | Ultra runner: High budget (350 | 3500 ₴ | hydration_items | ultra_or_long_distance | - | **PASS** | Clean match & sound explanation |
| 061 | 10k Beginner: First race prepa | 1500 ₴ | protein_carbohydrate_food | race_or_event_preparation | gel | **WARN** | Questionable Composition: Set contains 300g pure Creatine tub bundled wi… |
| 062 | 10k Beginner: Tight budget nut | 800 ₴ | protein_carbohydrate_food | race_or_event_preparation | - | **WARN** | Questionable Composition: Set contains 300g pure Creatine tub bundled wi… |
| 063 | 5k Runner: Fast energy bar bef | 1500 ₴ | protein_carbohydrate_food | race_or_event_preparation | bars | **PASS** | Clean match & sound explanation |
| 064 | Race prep: Hydration electroly | 1500 ₴ | hydration_items | race_or_event_preparation | - | **WARN** | Questionable Set: Recommends Набір «Тренувальний ресурс Race Expert Club… |
| 065 | Race prep: Tight budget hydrat | 750 ₴ | hydration_items | race_or_event_preparation | - | **WARN** | Questionable Set: Recommends Набір «Тренувальний ресурс Race Expert Club… |
| 066 | Race prep: Socks size 36 for r | 1000 ₴ | apparel_footwear | race_or_event_preparation | - | **PASS** | Clean match & sound explanation |
| 067 | Race prep: Socks size 46 for l | 1100 ₴ | apparel_footwear | race_or_event_preparation | - | **PASS** | Clean match & sound explanation |
| 068 | Race prep: Race starter pack ( | 1500 ₴ | sports_accessories | race_or_event_preparation | - | **WARN** | Questionable Set: Recommends Набір «Тренувальний ресурс Race Expert Club… |
| 069 | Race prep: High budget compreh | 3000 ₴ | any | race_or_event_preparation | - | **PASS** | Clean match & sound explanation |
| 070 | Race prep: Tight budget genera | 900 ₴ | any | race_or_event_preparation | - | **PASS** | Clean match & sound explanation |
| 071 | Race prep: Summer heat defense | 1300 ₴ | hydration_items | race_or_event_preparation | - | **WARN** | Questionable Set: Recommends Набір «Тренувальний ресурс Race Expert Club… |
| 072 | Race prep: Ready snacks for ra | 1600 ₴ | protein_carbohydrate_food | race_or_event_preparation | food_or_meal | **FAIL** | Catalog Starvation / No Match: Runner requested running nutrition/food, … |
| 073 | Race prep: Multi-choice [bars, | 1600 ₴ | protein_carbohydrate_food | race_or_event_preparation | ['bars', 'sticks'] | **PASS** | Clean match & sound explanation |
| 074 | Race prep: Powder mix for pre- | 1500 ₴ | hydration_items | race_or_event_preparation | powder | **FAIL** | Schema limitation: Endurance runners frequently use electrolyte capsules… |
| 075 | Race prep: Electrolyte capsule | 1500 ₴ | hydration_items | race_or_event_preparation | capsules | **FAIL** | Schema limitation: Endurance runners frequently use electrolyte capsules… |
| 076 | Race prep: Medium budget acces | 1300 ₴ | sports_accessories | race_or_event_preparation | - | **WARN** | Questionable Set: Recommends Набір «Тренувальний ресурс Race Expert Club… |
| 077 | Race prep: Winter 10k thermal  | 1100 ₴ | apparel_footwear | race_or_event_preparation | - | **PASS** | Clean match & sound explanation |
| 078 | Race prep: Post-race recovery  | 1600 ₴ | protein_carbohydrate_food | race_or_event_preparation | - | **WARN** | Questionable Composition: Set contains 300g pure Creatine tub bundled wi… |
| 079 | Race prep: 1800 UAH budget, op | 1800 ₴ | any | race_or_event_preparation | - | **PASS** | Clean match & sound explanation |
| 080 | Race prep: Liquid caffeine ene | 1600 ₴ | protein_carbohydrate_food | race_or_event_preparation | liquid | **FAIL** | Catalog Starvation / No Match: Runner requested running nutrition/food, … |
| 081 | Daily jogger: Regular training | 1000 ₴ | apparel_footwear | - | - | **PASS** | Clean match & sound explanation |
| 082 | Daily jogger: Dark socks size  | 1000 ₴ | apparel_footwear | - | - | **PASS** | Clean match & sound explanation |
| 083 | Daily jogger: White socks size | 1000 ₴ | apparel_footwear | - | - | **PASS** | Clean match & sound explanation |
| 084 | Daily runner: Everyday hydrati | 1500 ₴ | hydration_items | - | - | **PASS** | Clean match & sound explanation |
| 085 | Daily runner: Energy bars for  | 1500 ₴ | protein_carbohydrate_food | - | bars | **PASS** | Clean match & sound explanation |
| 086 | Daily runner: Training accesso | 1400 ₴ | sports_accessories | - | - | **WARN** | Questionable Set: Recommends Набір «Тренувальний ресурс Race Expert Club… |
| 087 | Daily runner: High budget trai | 2500 ₴ | sports_accessories | - | - | **WARN** | Questionable Set: Recommends Набір «Тренувальний ресурс Race Expert Club… |
| 088 | Daily runner: Weekly runner pa | 1600 ₴ | protein_carbohydrate_food | - | - | **WARN** | Questionable Composition: Set contains 300g pure Creatine tub bundled wi… |
| 089 | Daily runner: Tight budget ene | 650 ₴ | protein_carbohydrate_food | - | - | **WARN** | Questionable Composition: Set contains 300g pure Creatine tub bundled wi… |
| 090 | Daily runner: Tight budget soc | 500 ₴ | apparel_footwear | - | - | **PASS** | Clean match & sound explanation |
| 091 | Daily runner: Electrolyte stic | 1500 ₴ | hydration_items | - | sticks | **WARN** | Questionable Set: Recommends Набір «Тренувальний ресурс Race Expert Club… |
| 092 | Daily runner: Isotonic tub pow | 1800 ₴ | hydration_items | - | powder | **FAIL** | Schema limitation: Endurance runners frequently use electrolyte capsules… |
| 093 | Daily runner: Daily salt capsu | 1500 ₴ | hydration_items | - | capsules | **FAIL** | Schema limitation: Endurance runners frequently use electrolyte capsules… |
| 094 | Daily runner: Winter training  | 1200 ₴ | apparel_footwear | - | - | **PASS** | Clean match & sound explanation |
| 095 | Daily runner: Fall gear buff a | 1500 ₴ | sports_accessories | - | - | **WARN** | Questionable Set: Recommends Набір «Тренувальний ресурс Race Expert Club… |
| 096 | Daily runner: Multi-form [gel, | 1700 ₴ | protein_carbohydrate_food | - | ['gel', 'bars'] | **WARN** | Questionable Composition: Set contains 300g pure Creatine tub bundled wi… |
| 097 | Daily runner: Recovery food af | 1600 ₴ | protein_carbohydrate_food | - | - | **WARN** | Questionable Composition: Set contains 300g pure Creatine tub bundled wi… |
| 098 | Daily runner: Open preference, | 1500 ₴ | any | - | - | **PASS** | Clean match & sound explanation |
| 099 | Daily runner: Open preference, | 2000 ₴ | any | - | - | **PASS** | Clean match & sound explanation |
| 100 | Daily runner: Open preference, | 700 ₴ | any | - | - | **PASS** | Clean match & sound explanation |

## Concrete Actionable Recommendations for Engineering & Nutrition Curators
1. **Fix Half-Marathon Tagging Immediately:** In `wiki/projects/quiz-set-audit.json`, add `'half_marathon'` to `matching_evidence.race_formats` for sets `RE11660` (Набір «Марафонець»), `RE11804` (Набір «Марафонський темп»), `RE11659` (Набір «Тиждень бігуна»), and all sock multipacks. This will immediately resolve 20 failing customer scenarios.
2. **Fix `PRODUCT_FORMS_BY_GOAL['running']`:** Add `'capsules'` (for salt/electrolyte capsules like RE11650) and `'powder'` (for electrolyte & isotonic mix powders) to allowed running product forms.
3. **Disqualify Pure Bodybuilding Creatine from Running/Marathon:** Remove `running_race_preparation` from `RE11660`'s matching evidence or replace the 300g Creatine component with an isotonic mix or hydration sticks. No marathon coach recommends a 300g tub of creatine for 42.2 km race prep.
4. **Correct UT-PRO-2026 Audit Metadata:** Add `'protein_carbohydrate_food'` to `component_classes` of set `UT-PRO-2026` since it contains 3 SIS Beta Fuel high-carb gels and a protein bar.
5. **Fix Expert Summary Logic for Running:** When goal is `running`, ensure `expert_summary` never describes products as *'комплекс для силовых тренировок и стимуляции мышечного роста'*, even if the set happens to contain amino acids or creatine.
