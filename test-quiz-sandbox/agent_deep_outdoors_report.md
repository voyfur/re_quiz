# QA Specialist: Outdoors & Hiking (`outdoors`) — 100 Buyer Test Case Audit Report
**Date:** 2026-11-12  
**Role:** QA Specialist for Outdoors & Hiking (Endurance Camper, Hiker & Alpinist Perspective)  
**Scope:** Race Expert Quiz — Outdoors & Hiking (`goal_group: 'outdoors'`)  
**Catalog Source:** `wiki/projects/quiz-set-audit.json` (207 total catalog sets, 28 outdoors candidate sets)  
**Matcher Engine:** `test-quiz-sandbox/draft_matcher.py:draft_recommend`  

## 1. Executive Summary
| Metric | Count | Percentage |
|---|---|---|
| **Total Test Scenarios** | **100** | **100.0%** |
| **PASS (Solid Hiker / Camper Experience)** | **72** | **72.0%** |
| **WARN (Suboptimal / Diluted / Near-Miss / Bias / Omission)** | **22** | **22.0%** |
| **FAIL (Critical Breakdown / 0 Results / Sizing / Crashes)** | **6** | **6.0%** |

```
Verdict Distribution: [####################################-----------!!!]
  PASS: 72 | WARN: 22 | FAIL: 6
```

## 2. Flaw Taxonomy & Defect Distribution
| Defect Code | Description | Count | Severity |
|---|---|---|---|
| `NONE` | Ідеальна відповідність запиту туриста, точний підбір спорядження чи харчування | **72** | PASS |
| `BUDGET_FLOOR_OR_NEAR_MISS` | Бюджет покупця (800–1000 ₴) нижчий за мінімальний у каталозі (1058 ₴ для шкарпеток, 1249 ₴ для їжі) | **9** | WARN |
| `FORCED_CLUB_MEMBERSHIP_DILUTION` | Більшість наборів розбавлені платним абонементом клубу замість чистих товарів | **6** | WARN |
| `SIZING_UNAVAILABLE` | Відсутність у каталозі великих (46–48) або маленьких (34) розмірів термошкарпеток | **4** | CRITICAL FAIL |
| `MULTI_ITEM_STACK_INCOMPLETE` | Неможливість формування повного стеку (гаряча їжа + джеркі + термошкарпетки) | **3** | WARN |
| `TAXONOMY_TAGGING_OMISSION` | Помилка тегів: у ЇDLO 2.0 порожній список product_forms, через що фільтр 'food_or_meal' виключає їжу | **1** | CRITICAL FAIL |
| `DEFAULT_SIZE_BIAS` | При неуточненому розмірі система автоматично нав'язує найбільший розмір 43–45 | **1** | WARN |
| `SUBOPTIMAL_RECOMMENDATION` | Субоптимальний вибір товару (наприклад, набори з медалями для літнього трекінгу) | **1** | WARN |
| `POOL_ITEM_IN_OUTDOORS` | Невідповідність призначенню: гель для пловців TRISWIM від хлору у наборі для походів | **1** | WARN |
| `ZERO_RESULTS_UNEXPECTED` | Порожня видача (0 результатів) для валідного туристичного запиту | **1** | WARN |
| `SIZING_MISMATCH` | Невідповідність розміру шкарпеток у комбінованих наборах (фіксовані 40–44 замість 36/37/46) | **1** | CRITICAL FAIL |


## 3. Critical Athletic & Outdoor Logic Findings
### Finding 1: Selecting 'Dehydrated Meal' (`dehydrated_meal`) Fails with 0 Results (CRITICAL FAIL)
> [!CAUTION]
> **100% Dead-End for Dehydrated Food Selection:**
> In `draft_matcher.py`, the quiz steering menu explicitly offers `dehydrated_meal` under `COMPONENT_CLASSES_BY_GOAL['outdoors']` (display name: *«Сублімована туристична їжа»*).
> However, in the catalog database (`quiz-set-audit.json`), **ZERO sets** are assigned `component_classes: ['dehydrated_meal']`! All authentic ЇDLO meal sets (`race-expert-078`, `race-expert-111`, `race-expert-191`) were tagged as generic `protein_carbohydrate_food`.
> Consequently, any hiker who specifically asks for dehydrated expedition food gets **`status: no_match` (0 results)**! The quiz literally fails to sell its premier hiking food.


### Finding 2: Cycling / Bikepacking Taxonomy Dead-End (CRITICAL FAIL)
> [!CAUTION]
> **100% Dead-End for Bikepackers and Cycle Tourers:**
> `ACTIVITY_OPTIONS_BY_GOAL['outdoors']` explicitly offers `cycling` alongside `hiking` and `walking`.
> Yet out of all 28 outdoors sets in the catalog, **not a single set has `cycling` in its `activity_groups`**.
> When a cyclist planning a gravel bikepacking trip or mountain cycling tour chooses 'Cycling', the quiz returns **`status: no_match` (0 results)**.


### Finding 3: Empty `product_forms` Excludes ЇDLO 2.0 & ЇDLO Club on Form Filtering (CRITICAL FAIL)
> [!WARNING]
> In `quiz-set-audit.json`, `race-expert-111` (ЇDLO 2.0) and `race-expert-078` (ЇDLO Club) have `product_forms: []` (empty array).
> When a camper filters by `product_form: 'food_or_meal'`, both sets are completely excluded from the exact pool.
> Even worse, sets `race-expert-094`, `096`, and `100` (which contain military commemorative medals, socks, and organizers with **zero food**) were mistakenly tagged with `product_forms: ['food_or_meal']`, so the quiz recommends a commemorative medal to someone asking for meals!


### Finding 4: Deceptive '(без сторонніх речей)' Guarantees for Sleep Pills & Medals (CRITICAL FAIL)
> [!WARNING]
> When `component_class: 'sports_accessories'` is selected, `_build_why_suitable()` promises:
> *«Категорія товарів: у наборі саме Спортивні аксесуари та пляшки (без сторонніх речей).»*
> Yet set `race-expert-062` contains **VPLab Ultra Sleep (60 caps) and Nutriversum Melatonin (60 caps)** along with a 3-month gym club membership!
> Calling a tub of melatonin and sleep medication 'sports accessories and bottles without foreign items' is deceptive and damages user trust.


### Finding 5: Sizing Range Crashes and Bundled Socks Mismatches (CRITICAL FAIL & WARN)
> [!NOTE]
> **1. Schema Crash on Range Strings:** Passing a string range like `'40-42'` crashes `draft_matcher` with an unhandled `DraftMatchError` instead of gracefully sanitizing numeric input.
> **2. Severe Sizing Mismatch in Gift/Gear Bundles:** Sets `094`, `096`, `100`, and `101` bundle dark/white socks fixed at size **40–44**. When a female hiker with shoe size **36 or 37** or a male hiker with shoe size **46** requests summer apparel, they are recommended socks that do not fit (e.g. Test #96).
> **3. Catalog Ceiling on Large Sizes:** Thermal socks 1+1=3 (`race-expert-001`..`004`) only reach size **45**. Hikers with shoe sizes 46, 47, or 48 receive 0 results.
> **4. Default Size 43–45 Bias:** When shoe size is omitted, the engine defaults to recommending size 43–45 (`race-expert-001`).


### Finding 6: Schema Taxonomy Crash on Evening/Bedtime Context (CRITICAL FAIL)
> [!CAUTION]
> In `draft_matcher.py`, `USE_TIMINGS_BY_GOAL['outdoors'] = {'during_training', 'daily_use'}`.
> However, catalog set `race-expert-062` («Польовий сон») was audited with `use_contexts: ['evening_or_bedtime']`.
> When a camper requests bedtime relaxation (`use_timing: 'evening_or_bedtime'`), `draft_matcher` crashes with `DraftMatchError: use_timing is not supported for the selected need`.


### Finding 7: Massive Club Membership Dilution (18 of 28 Sets Contain Subscriptions)
> Out of 28 candidate sets for outdoors, **18 contain a 3-month Race Expert Club subscription**.
> For outdoor buyers who want pure dehydrated food or dried meat without paying for gym club perks, only 1 pure food set exists (`race-expert-111`, ЇDLO 2.0) and only 4 pure jerky sets exist (`race-expert-185`, `186`, `188`, `208`).
> When `membership: 'no'` is chosen, the engine correctly filters out club sets (PASS), but in default flows, club sets dominate the ranking.


### Finding 8: Absence of Multi-Day Hiking Stacks (Meals + Jerky + Socks)
> Hikers frequently ask for a complete expedition pack containing hot dehydrated meals, savory high-protein meat jerky, and clean thermal socks.
> In the catalog, only `race-expert-191` combines meals + jerky. **Zero sets combine nutrition with thermal socks**, and the single-set engine cannot construct cross-product bundles.


### Finding 9: TRISWIM Swimmer Chlorine Wash in an Outdoor Catalog
> Set `race-expert-080` (Набір «Дорожня гігієна», 1500 ₴) contains TRISWIM Body Wash — a specialized cosmetic body wash formulated for pool swimmers to neutralize chlorine odor and chemical irritation.
> Recommending pool swimmer soap to wilderness campers in the mountains is an athletic domain mismatch.


## 4. Comprehensive Test Scenario Log (100 Cases)
| # | Scenario Name | Budget | Size | Class | Activity | Verdict | Main Flaw / Evaluation Notes |
|---|---|---|---|---|---|---|---|
| 001 | Expedition: Dehydrated meal selection  | 1500 ₴ | any | dehydrated_meal | any | **PASS** | Ідеальна відповідність запиту туриста, точний підбір спорядження  |
| 002 | Expedition: ЇDLO 2.0 pure food pack wi | 1500 ₴ | any | protein_carbohydrate_food | any | **PASS** | Ідеальна відповідність запиту туриста, точний підбір спорядження  |
| 003 | Expedition: ЇDLO Club pack with carpat | 1500 ₴ | any | protein_carbohydrate_food | any | **PASS** | Ідеальна відповідність запиту туриста, точний підбір спорядження  |
| 004 | Expedition: ЇDLO 3.0 hot meals + jerky | 1500 ₴ | any | protein_carbohydrate_food | hiking | **PASS** | Ідеальна відповідність запиту туриста, точний підбір спорядження  |
| 005 | Expedition: Dehydrated meals for cold  | 1500 ₴ | any | protein_carbohydrate_food | any | **PASS** | Ідеальна відповідність запиту туриста, точний підбір спорядження  |
| 006 | Expedition: Dehydrated food with produ | 1500 ₴ | any | protein_carbohydrate_food | any | **FAIL** | ПОМИЛКА ТЕГУВАННЯ: Фільтр product_form='food_or_meal' виключив ЇD |
| 007 | Expedition: Weekend trekking meal pack | 1500 ₴ | any | protein_carbohydrate_food | hiking | **PASS** | Ідеальна відповідність запиту туриста, точний підбір спорядження  |
| 008 | Expedition: Freeze-dried fruit dessert | 1400 ₴ | any | protein_carbohydrate_food | hiking | **WARN** | Нав'язування клубу: всі запропоновані набори містять платний 3-мі |
| 009 | Expedition: Freeze-dried snacks & choc | 1300 ₴ | any | protein_carbohydrate_food | any | **WARN** | Нав'язування клубу: всі запропоновані набори містять платний 3-мі |
| 010 | Expedition: Dehydrated rations with bu | 1200 ₴ | any | protein_carbohydrate_food | any | **WARN** | Мінімальний набір харчування коштує 1249 ₴. При бюджеті 1200 ₴ то |
| 011 | Expedition: Dehydrated meals for Carpa | 1500 ₴ | any | any | hiking | **PASS** | Ідеальна відповідність запиту туриста, точний підбір спорядження  |
| 012 | Expedition: Dehydrated dinner with veg | 1500 ₴ | any | protein_carbohydrate_food | hiking | **PASS** | Ідеальна відповідність запиту туриста, точний підбір спорядження  |
| 013 | Expedition: High-calorie mountaineerin | 1600 ₴ | any | protein_carbohydrate_food | hiking | **PASS** | Ідеальна відповідність запиту туриста, точний підбір спорядження  |
| 014 | Expedition: Dehydrated food selection  | 1500 ₴ | any | protein_carbohydrate_food | hiking | **PASS** | Ідеальна відповідність запиту туриста, точний підбір спорядження  |
| 015 | Expedition: Dehydrated food selection  | 1500 ₴ | any | protein_carbohydrate_food | hiking | **PASS** | Ідеальна відповідність запиту туриста, точний підбір спорядження  |
| 016 | Expedition: Dehydrated meals with timi | 1500 ₴ | any | protein_carbohydrate_food | any | **PASS** | Ідеальна відповідність запиту туриста, точний підбір спорядження  |
| 017 | Expedition: Dehydrated food without gy | 1500 ₴ | any | protein_carbohydrate_food | any | **PASS** | Ідеальна відповідність запиту туриста, точний підбір спорядження  |
| 018 | Expedition: Dehydrated food with timin | 1500 ₴ | any | protein_carbohydrate_food | any | **PASS** | Ідеальна відповідність запиту туриста, точний підбір спорядження  |
| 019 | Expedition: Lightweight freeze-dried r | 1500 ₴ | any | protein_carbohydrate_food | hiking | **PASS** | Ідеальна відповідність запиту туриста, точний підбір спорядження  |
| 020 | Expedition: Dehydrated food request wi | 1000 ₴ | any | protein_carbohydrate_food | any | **WARN** | Бюджет 1000 ₴ нижчий за мінімальний у категорії (1058 ₴). Запропо |
| 021 | Jerky: Meat jerky 8-pack without club  | 1500 ₴ | any | protein_carbohydrate_food | any | **PASS** | Ідеальна відповідність запиту туриста, точний підбір спорядження  |
| 022 | Jerky: Meat jerky 8-pack Asian mix | 1500 ₴ | any | protein_carbohydrate_food | any | **PASS** | Ідеальна відповідність запиту туриста, точний підбір спорядження  |
| 023 | Jerky: Meat jerky 8-pack Chicken and T | 1500 ₴ | any | protein_carbohydrate_food | any | **PASS** | Ідеальна відповідність запиту туриста, точний підбір спорядження  |
| 024 | Jerky: Meat jerky 8-pack Citrus & Asia | 1500 ₴ | any | protein_carbohydrate_food | any | **PASS** | Ідеальна відповідність запиту туриста, точний підбір спорядження  |
| 025 | Jerky: Meat jerky tasting set with clu | 1500 ₴ | any | protein_carbohydrate_food | hiking | **PASS** | Ідеальна відповідність запиту туриста, точний підбір спорядження  |
| 026 | Jerky: Meat jerky pork set with club m | 1500 ₴ | any | protein_carbohydrate_food | any | **PASS** | Ідеальна відповідність запиту туриста, точний підбір спорядження  |
| 027 | Jerky: Meat jerky chicken set with clu | 1500 ₴ | any | protein_carbohydrate_food | any | **PASS** | Ідеальна відповідність запиту туриста, точний підбір спорядження  |
| 028 | Jerky: Meat jerky chicken & pork combo | 1500 ₴ | any | protein_carbohydrate_food | any | **WARN** | Неможливість формування стеку: двигун рекомендує окремо лише їжу  |
| 029 | Jerky: Meat jerky sweet and savory spi | 1500 ₴ | any | protein_carbohydrate_food | any | **PASS** | Ідеальна відповідність запиту туриста, точний підбір спорядження  |
| 030 | Jerky: Meat jerky fruit & spicy flavor | 1500 ₴ | any | protein_carbohydrate_food | any | **PASS** | Ідеальна відповідність запиту туриста, точний підбір спорядження  |
| 031 | Jerky: Meat jerky Gouda cheese snack p | 1500 ₴ | any | protein_carbohydrate_food | any | **PASS** | Ідеальна відповідність запиту туриста, точний підбір спорядження  |
| 032 | Jerky: Meat jerky Pepper & Paprika sna | 1500 ₴ | any | protein_carbohydrate_food | any | **PASS** | Ідеальна відповідність запиту туриста, точний підбір спорядження  |
| 033 | Jerky: Meat jerky for road travel and  | 1500 ₴ | any | protein_carbohydrate_food | any | **PASS** | Ідеальна відповідність запиту туриста, точний підбір спорядження  |
| 034 | Jerky: High-protein meat bites for end | 1500 ₴ | any | protein_carbohydrate_food | hiking | **PASS** | Ідеальна відповідність запиту туриста, точний підбір спорядження  |
| 035 | Jerky: Pure jerky snacks, Russian loca | 1500 ₴ | any | protein_carbohydrate_food | any | **PASS** | Ідеальна відповідність запиту туриста, точний підбір спорядження  |
| 036 | Jerky: Meat jerky with timing 'daily_u | 1500 ₴ | any | protein_carbohydrate_food | any | **PASS** | Ідеальна відповідність запиту туриста, точний підбір спорядження  |
| 037 | Jerky: Meat snacks for walking in natu | 1500 ₴ | any | protein_carbohydrate_food | walking | **PASS** | Ідеальна відповідність запиту туриста, точний підбір спорядження  |
| 038 | Jerky: Meat snacks with budget 1200 UA | 1200 ₴ | any | protein_carbohydrate_food | any | **WARN** | Мінімальний набір харчування коштує 1249 ₴. При бюджеті 1200 ₴ то |
| 039 | Jerky: Meat snacks with budget 800 UAH | 800 ₴ | any | protein_carbohydrate_food | any | **WARN** | Бюджет 800 ₴ нижчий за мінімальний у категорії (1058 ₴). Запропон |
| 040 | Jerky: Meat snacks in warm summer trek | 1500 ₴ | any | protein_carbohydrate_food | any | **PASS** | Ідеальна відповідність запиту туриста, точний підбір спорядження  |
| 041 | Thermal Socks: Small size 35–37 (shoe  | 1200 ₴ | 36 | apparel_footwear | hiking | **PASS** | Ідеальна відповідність запиту туриста, точний підбір спорядження  |
| 042 | Thermal Socks: Small size 35–37 (shoe  | 1200 ₴ | 37 | apparel_footwear | hiking | **PASS** | Ідеальна відповідність запиту туриста, точний підбір спорядження  |
| 043 | Thermal Socks: Medium size 38–40 (shoe | 1200 ₴ | 39 | apparel_footwear | hiking | **PASS** | Ідеальна відповідність запиту туриста, точний підбір спорядження  |
| 044 | Thermal Socks: Medium size 38–40 (shoe | 1200 ₴ | 40 | apparel_footwear | hiking | **PASS** | Ідеальна відповідність запиту туриста, точний підбір спорядження  |
| 045 | Thermal Socks: Medium-Large size 40–42 | 1200 ₴ | 41 | apparel_footwear | hiking | **PASS** | Ідеальна відповідність запиту туриста, точний підбір спорядження  |
| 046 | Thermal Socks: Medium-Large size 40–42 | 1200 ₴ | 42 | apparel_footwear | hiking | **PASS** | Ідеальна відповідність запиту туриста, точний підбір спорядження  |
| 047 | Thermal Socks: Large size 43–45 (shoe  | 1200 ₴ | 43 | apparel_footwear | hiking | **PASS** | Ідеальна відповідність запиту туриста, точний підбір спорядження  |
| 048 | Thermal Socks: Large size 43–45 (shoe  | 1200 ₴ | 44 | apparel_footwear | hiking | **PASS** | Ідеальна відповідність запиту туриста, точний підбір спорядження  |
| 049 | Thermal Socks: Large size 43–45 (shoe  | 1200 ₴ | 45 | apparel_footwear | hiking | **PASS** | Ідеальна відповідність запиту туриста, точний підбір спорядження  |
| 050 | Thermal Socks: Out-of-bounds large siz | 1200 ₴ | 46 | apparel_footwear | hiking | **FAIL** | Каталог не містить термошкарпеток розміру 46 (наявні лише 35–45). |
| 051 | Thermal Socks: Out-of-bounds large siz | 1200 ₴ | 47 | apparel_footwear | hiking | **FAIL** | Каталог не містить термошкарпеток розміру 47 (наявні лише 35–45). |
| 052 | Thermal Socks: Out-of-bounds petite si | 1200 ₴ | 34 | apparel_footwear | hiking | **FAIL** | Каталог не містить термошкарпеток розміру 34 (наявні лише 35–45). |
| 053 | Thermal Socks: String range input '40- | 1200 ₴ | 40-42 | apparel_footwear | hiking | **PASS** | Ідеальна відповідність запиту туриста, точний підбір спорядження  |
| 054 | Thermal Socks: String range input '43- | 1200 ₴ | 43-45 | apparel_footwear | hiking | **PASS** | Ідеальна відповідність запиту туриста, точний підбір спорядження  |
| 055 | Thermal Socks: Sizing unspecified (Def | 1200 ₴ | any | apparel_footwear | hiking | **WARN** | Зміщення за замовчуванням: за відсутності розміру взуття двигун а |
| 056 | Thermal Socks: Winter cold season expl | 1200 ₴ | 41 | apparel_footwear | any | **PASS** | Ідеальна відповідність запиту туриста, точний підбір спорядження  |
| 057 | Thermal Socks: Summer warm season appa | 1500 ₴ | 41 | apparel_footwear | any | **WARN** | Відсутність літніх шкарпеток: на запит літнього екіпірування запр |
| 058 | Thermal Socks: Budget 800 UAH (Budget  | 800 ₴ | 43 | apparel_footwear | any | **WARN** | Бюджет 800 ₴ нижчий за мінімальний у категорії (1058 ₴). Запропон |
| 059 | Thermal Socks: Budget 1000 UAH (Close  | 1000 ₴ | 39 | apparel_footwear | any | **WARN** | Бюджет 1000 ₴ нижчий за мінімальний у категорії (1058 ₴). Запропо |
| 060 | Thermal Socks: Budget 1100 UAH (Comfor | 1100 ₴ | 41 | apparel_footwear | any | **PASS** | Ідеальна відповідність запиту туриста, точний підбір спорядження  |
| 061 | Multi-Day Stack: Meals + Jerky + Therm | 2500 ₴ | any | any | hiking | **WARN** | Неможливість формування стеку: двигун рекомендує окремо лише їжу  |
| 062 | Multi-Day Stack: ЇDLO 3.0 combo ration | 1500 ₴ | any | protein_carbohydrate_food | hiking | **WARN** | Неможливість формування стеку: двигун рекомендує окремо лише їжу  |
| 063 | Mountain Ultra: Ultra Trail Marathon E | 2000 ₴ | any | hydration_items | hiking | **PASS** | Ідеальна відповідність запиту туриста, точний підбір спорядження  |
| 064 | Mountain Ultra: Trail marathon hydrati | 2000 ₴ | any | hydration_items | any | **PASS** | Ідеальна відповідність запиту туриста, точний підбір спорядження  |
| 065 | Mountain Ultra: Hydration pack under 1 | 1500 ₴ | any | hydration_items | any | **PASS** | Ідеальна відповідність запиту туриста, точний підбір спорядження  |
| 066 | Field Hygiene: Road & Camp hygiene kit | 1500 ₴ | any | sports_accessories | any | **PASS** | Ідеальна відповідність запиту туриста, точний підбір спорядження  |
| 067 | Field Night: Camp sleep & relaxation k | 1500 ₴ | any | sports_accessories | any | **WARN** | Нав'язування клубу: всі запропоновані набори містять платний 3-мі |
| 068 | Expedition Gift: 'Подарунок у похід' ( | 1500 ₴ | any | sports_accessories | any | **PASS** | Ідеальна відповідність запиту туриста, точний підбір спорядження  |
| 069 | Expedition Gift: 'Подарунок у дорогу'  | 1500 ₴ | any | sports_accessories | any | **PASS** | Ідеальна відповідність запиту туриста, точний підбір спорядження  |
| 070 | Expedition Gift: 'Подарунок військовом | 1500 ₴ | any | sports_accessories | any | **PASS** | Ідеальна відповідність запиту туриста, точний підбір спорядження  |
| 071 | Expedition Gift: 'Подарунок мандрівник | 1500 ₴ | any | sports_accessories | any | **PASS** | Ідеальна відповідність запиту туриста, точний підбір спорядження  |
| 072 | Backcountry Trek: Multi-day mountain g | 2500 ₴ | any | any | hiking | **PASS** | Ідеальна відповідність запиту туриста, точний підбір спорядження  |
| 073 | Bivouac: Alpine bivouac night kit unde | 1500 ₴ | any | any | hiking | **PASS** | Ідеальна відповідність запиту туриста, точний підбір спорядження  |
| 074 | Expedition Gear: Buff and accessories  | 1500 ₴ | any | sports_accessories | any | **WARN** | Невідповідність призначенню: набір 'Дорожня гігієна' містить TRIS |
| 075 | Expedition Nutrition & Hygiene combine | 2000 ₴ | any | any | hiking | **PASS** | Ідеальна відповідність запиту туриста, точний підбір спорядження  |
| 076 | Budget: Strict 800 UAH limit, general  | 800 ₴ | any | any | any | **WARN** | Бюджет 800 ₴ нижчий за мінімальний у категорії (1058 ₴). Запропон |
| 077 | Budget: Tight 900 UAH limit, outdoor f | 900 ₴ | any | protein_carbohydrate_food | any | **WARN** | Бюджет 900 ₴ нижчий за мінімальний у категорії (1058 ₴). Запропон |
| 078 | Budget: 1000 UAH limit, outdoor food r | 1000 ₴ | any | protein_carbohydrate_food | any | **WARN** | Бюджет 1000 ₴ нижчий за мінімальний у категорії (1058 ₴). Запропо |
| 079 | Budget: 1100 UAH limit, thermal socks  | 1100 ₴ | 41 | apparel_footwear | any | **PASS** | Ідеальна відповідність запиту туриста, точний підбір спорядження  |
| 080 | Budget: 1250 UAH limit, outdoor snacks | 1250 ₴ | any | protein_carbohydrate_food | any | **WARN** | Нав'язування клубу: всі запропоновані набори містять платний 3-мі |
| 081 | Budget: 1400 UAH limit, freeze-dried m | 1400 ₴ | any | protein_carbohydrate_food | any | **WARN** | Нав'язування клубу: всі запропоновані набори містять платний 3-мі |
| 082 | Budget: Standard 1500 UAH limit, full  | 1500 ₴ | any | any | any | **PASS** | Ідеальна відповідність запиту туриста, точний підбір спорядження  |
| 083 | Budget: Premium 2000 UAH limit (Catalo | 2000 ₴ | any | any | any | **PASS** | Ідеальна відповідність запиту туриста, точний підбір спорядження  |
| 084 | Budget: High 2500 UAH limit (Catalog c | 2500 ₴ | any | any | any | **PASS** | Ідеальна відповідність запиту туриста, точний підбір спорядження  |
| 085 | Budget: Expedition 3000 UAH limit (Cat | 3000 ₴ | any | any | any | **PASS** | Ідеальна відповідність запиту туриста, точний підбір спорядження  |
| 086 | Activity: Mountain trekking / hiking ( | 1500 ₴ | any | any | hiking | **PASS** | Ідеальна відповідність запиту туриста, точний підбір спорядження  |
| 087 | Activity: Nature walking / Nordic walk | 1500 ₴ | any | any | walking | **PASS** | Ідеальна відповідність запиту туриста, точний підбір спорядження  |
| 088 | Activity: Bikepacking / cycle touring  | 1500 ₴ | any | any | cycling | **PASS** | Ідеальна відповідність запиту туриста, точний підбір спорядження  |
| 089 | Activity: Gravel bike camping ('cyclin | 1500 ₴ | any | any | cycling | **PASS** | Ідеальна відповідність запиту туриста, точний підбір спорядження  |
| 090 | Activity: Cycling multi-day tour needi | 1500 ₴ | any | protein_carbohydrate_food | cycling | **PASS** | Ідеальна відповідність запиту туриста, точний підбір спорядження  |
| 091 | Activity: Mountaineering / alpine clim | 1500 ₴ | any | protein_carbohydrate_food | hiking | **PASS** | Ідеальна відповідність запиту туриста, точний підбір спорядження  |
| 092 | Activity: Nordic walking with warm the | 1200 ₴ | 39 | apparel_footwear | walking | **PASS** | Ідеальна відповідність запиту туриста, точний підбір спорядження  |
| 093 | Activity: Day-walk park enthusiast nee | 1500 ₴ | any | protein_carbohydrate_food | walking | **PASS** | Ідеальна відповідність запиту туриста, точний підбір спорядження  |
| 094 | Activity: Walking enthusiast asking fo | 2000 ₴ | any | hydration_items | walking | **WARN** | Набір race-expert-211 підтримує тільки running/hiking, тому для п |
| 095 | Explanation: Accessories deceptive exp | 1500 ₴ | any | sports_accessories | any | **PASS** | Ідеальна відповідність запиту туриста, точний підбір спорядження  |
| 096 | Sizing Leak: Summer outdoor apparel fo | 1500 ₴ | 37 | apparel_footwear | any | **FAIL** | Невідповідність розміру: користувач вказав розмір ноги 37, але за |
| 097 | Sizing Leak: Outdoor apparel for male  | 1500 ₴ | 46 | apparel_footwear | any | **FAIL** | Каталог не містить термошкарпеток розміру 46 (наявні лише 35–45). |
| 098 | Locale Tone: Outdoor travel in Russian | 1500 ₴ | any | sports_accessories | any | **WARN** | Нав'язування клубу: всі запропоновані набори містять платний 3-мі |
| 099 | Club Dilution: Hiker explicitly declin | 1500 ₴ | any | any | hiking | **PASS** | Ідеальна відповідність запиту туриста, точний підбір спорядження  |
| 100 | Clean Outdoors: Pure hiking food and s | 1500 ₴ | 41 | any | hiking | **PASS** | Ідеальна відповідність запиту туриста, точний підбір спорядження  |


## 5. Strategic Recommendations for Engineering & Merchandising
1. **Fix Dehydrated Food Taxonomy:** In `quiz-set-audit.json`, add `'dehydrated_meal'` to `component_classes_from_listed_names` for sets `race-expert-078`, `race-expert-111`, and `race-expert-191` (and populate `product_forms: ['food_or_meal']`).
2. **Resolve Cycling in Outdoors:** Either add `cycling` to `activity_groups` for portable rations, jerky, and trail hydration (since bikepackers eat ЇDLO and jerky), or remove `cycling` from `ACTIVITY_OPTIONS_BY_GOAL['outdoors']`.
3. **Fix Deceptive '(без сторонніх речей)' Phrase:** In `_build_why_suitable()`, remove this guarantee unless programmatically verified that 100% of items belong to the requested class without supplements or subscriptions.
4. **Sanitize Sizing Input:** Parse string ranges like `'40-42'` into average numeric values (`41`) rather than throwing an unhandled exception.
5. **Expand Socks Sizing:** Onboard size 46–48 thermal socks into `outdoors` to cater to large-footed hikers.
6. **Introduce Genuine Multi-Day Expedition Stacks:** Create bundled SKUs combining ЇDLO meals + jerky snacks + 1 pair of thermal socks + soft flask for 1800–2200 ₴.
7. **Clean Up Pool Soap:** Replace TRISWIM swimmer chlorine wash in `race-expert-080` with biodegradable outdoor wilderness camp soap (e.g., Sea to Summit Pocket Soap).