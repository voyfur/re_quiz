# QA Agent 6: Gear & Apparel Specialist — 100 Buyer Test Case Audit Report
**Date:** 2026-11-12  
**Role:** QA Agent 6 — Gear & Apparel Specialist (Human Athlete & Equipment Perspective)  
**Scope:** Race Expert Quiz — Gear & Accessories (`goal_group: 'gear'`)  
**Catalog Source:** `wiki/projects/quiz-set-audit.json` (207 sets loaded, 68 candidate gear sets)  
**Matcher Engine:** `test-quiz-sandbox/draft_matcher.py:draft_recommend`  

## 1. Executive Summary
| Metric | Count | Percentage |
|---|---|---|
| **Total Scenarios** | **100** | **100.0%** |
| **PASS (Sound Gear Buyer Experience)** | **33** | **33.0%** |
| **WARN (Suboptimal / Diluted / Near-Miss / Bias)** | **22** | **22.0%** |
| **FAIL (Critical Breakdown / Creatine Leak / Sizing Mismatch)** | **45** | **45.0%** |

```
Verdict Distribution: [################-----------!!!!!!!!!!!!!!!!!!!!!!]
  PASS: 33 | WARN: 22 | FAIL: 45
```

## 2. Flaw Taxonomy & Defect Distribution
| Defect Code | Description | Count | Severity |
|---|---|---|---|
| `NONE` | Ідеальна відповідність спортивному призначенню, розміру та ціні | **33** | PASS |
| `SUPPLEMENT_CREATINE_LEAK` | Витік бодібілдерського креатину, банок або фармакологічних добавок у спорядження | **29** | CRITICAL FAIL |
| `MINOR_LEAKAGE_OR_MEMBERSHIP` | Набір містить спорядження, але розбавлений абонементом або їстівними батончиками | **10** | WARN |
| `BUDGET_FLOOR_OR_NEAR_MISS` | Бюджет покупця (400–800 ₴) нижчий за мінімальний у каталозі (950 ₴) | **6** | WARN |
| `DECEPTIVE_EXPLANATION` | Неправдиві маркетингові твердження (наприклад, 'без сторонніх речей' при наявності добавок) | **5** | CRITICAL FAIL |
| `ZERO_RESULTS_UNEXPECTED` | Порожня видача (0 результатів) для валідного спортивного запиту | **5** | CRITICAL FAIL |
| `SWIMMING_TAXONOMY_DEAD_END` | Глухий кут: плавання дозволено у вікторині, але в каталозі 0 товарів для плавання | **5** | CRITICAL FAIL |
| `DEFAULT_SIZE_BIAS` | При неуточненому розмірі система автоматично нав'язує гігантський розмір 46–48 | **4** | WARN |
| `SUBOPTIMAL_RECOMMENDATION` | Субоптимальний вибір товару за сезоном або призначенням | **2** | WARN |
| `SCHEMA_CRASH_UNSANITIZED_INPUT` | Падіння двигуна на рядковому діапазоні розміру (наприклад, '42-44') | **1** | CRITICAL FAIL |


## 3. Critical Architectural & Athletic Logic Findings
### Finding 1: Massive Bodybuilding Creatine & Supplement Leakage into Gear (CRITICAL FAIL)
> [!CAUTION]
> **500g Bodybuilder Creatine Monohydrate Sold as 'Running Gear & Accessories':**
> In `quiz-set-audit.json`, multiple gym strength sets (`race-expert-009`, `race-expert-029`, `race-expert-040`, `race-expert-068`, `race-expert-149`) were erroneously assigned `candidate_tiers.seller_positioned: ['foot_apparel_comfort']` and `component_based: ['foot_apparel_comfort']`.
> As a catastrophic consequence, when a runner or walker selects `goal_group: 'gear'`, `component_class: 'sports_accessories'`, the quiz recommends:
> - **Set `race-expert-068` (Набір «Чоловіча сила», 1005 ₴):** 500g Creatine Monohydrate tub + 4 pairs of socks + 3-month gym club membership!
> - **Set `race-expert-040` (Набір «Ріст м'язів», 1225 ₴):** Bodyperson Creatine Monohydrate 500g + 2x Lipobar protein bars + club membership!
> - **Set `race-expert-009` (Набір «Чиста сила», 1399 ₴):** 500g Myprotein Creatine Monohydrate + shaker + club membership!
> Selling a powerlifter mass-gain creatine tub to a runner asking for water bottles and race belts completely destroys the credibility of Race Expert as an endurance specialist.


### Finding 2: False 'No Foreign Items' Guarantees in Explanations (CRITICAL FAIL)
> [!WARNING]
> In `draft_matcher.py:_build_why_suitable()`, when `component_class: 'sports_accessories'` is selected, the engine prints:
> *«Категорія товарів: у наборі саме Спортивні аксесуари та пляшки (без сторонніх речей).»*
> Yet for `race-expert-068`, over 80% of the set's physical content is a **500g tub of bodybuilding creatine** and a **3-month gym club subscription**!
> Guaranteeing to the consumer that there are *'no foreign items'* while handing them a tub of muscle-building powder and an unrequested club membership is fraudulent marketing that violates consumer trust.


### Finding 3: Swimming Gear Taxonomy Dead-End (CRITICAL FAIL)
> [!IMPORTANT]
> `draft_matcher.py` explicitly lists `swimming` in `ACTIVITY_OPTIONS_BY_GOAL['gear'] = {'running', 'hiking', 'cycling', 'walking', 'swimming'}`.
> However, in the catalog, **ZERO sets out of 207** support swimming!
> When a swimmer clicks 'Swimming' looking for swim gear (swim cap, goggles, fast-drying towel), the draft matcher returns **`status: no_match` (0 sets)**.
> Offering a sport in the quiz UI that has a 100% dead-end guarantee is a major UX defect.


### Finding 4: Cyclist Hard-Block for Socks (CRITICAL FAIL)
> [!WARNING]
> In `quiz-set-audit.json`, **none of the 29 sock sets** include `cycling` in `activity_groups` (they only list `running, hiking, walking, general_lifestyle`).
> Because `activity` is a mandatory core filter, any cyclist requesting socks receives **`status: no_match` (0 sets)**, while cyclists requesting general gear receive gym subscriptions with BCAA powder (`race-expert-150`).


### Finding 5: Sizing Pitfalls & Default Size 46–48 Bias (CRITICAL FAIL & WARN)
> [!NOTE]
> **1. Mismatched Sizing on Accessory Bundles:** Sets like `race-expert-056`, `115`, and `210` bundle race accessories (cap, bib belt, bottle) with fixed size **40–42 white socks**. When a female athlete with shoe size **37** requests race accessories, the engine either fails or sends socks 3 sizes too large.
> **2. Default Size 46–48 Bias:** When a user does not specify a shoe size (`shoe_size: 'any'`), the engine defaults to recommending **«46–48» socks** (the lowest priced set at 950 ₴). For the average Ukrainian runner (shoe size 38–43), receiving EU 46–48 socks makes them completely unwearable.
> **3. Crash on String Range Input:** Passing a string range like `'42-44'` causes `draft_matcher` to crash with `DraftMatchError: shoe_size must be a numeric shoe size.` instead of cleanly parsing or sanitizing.


### Finding 6: Extreme Apparel Catalog Monoculture (Only Socks!)
> Out of 29 sets tagged as `apparel_footwear` in the catalog, **100% are socks** (either 5-pair cotton/polyester packs at 950 ₴ or 3-pair thermal packs at 1058 ₴).
> There are **zero** running t-shirts, shorts, windbreakers, tights, caps (standalone), gloves, or shoes in the catalog.
> Furthermore, for budget-conscious buyers (400–800 ₴), **zero sets exist under 950 ₴** in gear, forcing every budget runner into near-miss or floor-anchor states.


## 4. Comprehensive Test Scenario Log (100 Cases)
| # | Scenario Name | Budget | Size | Class | Activity | Verdict | Main Flaw / Human-Logic Evaluation |
|---|---|---|---|---|---|---|---|
| 001 | Runner: Small size socks (37), entr | 600 ₴ | 37 | apparel_footwear | running | **WARN** | NEAR-MISS ПЕРЕВИЩЕННЯ: Бюджет 600 ₴, товар 950 ₴ (перевищення на 350 ₴). |
| 002 | Runner: Small size socks (37), regu | 1000 ₴ | 37 | apparel_footwear | running | **PASS** | Ідеальний збіг за спорядженням, розміром, бюджетом та поясненнями. |
| 003 | Runner: Small size socks (36), dark | 1100 ₴ | 36 | apparel_footwear | running | **PASS** | Ідеальний збіг за спорядженням, розміром, бюджетом та поясненнями. |
| 004 | Runner: Small size winter thermal s | 1200 ₴ | 37 | apparel_footwear | running | **PASS** | Ідеальний збіг за спорядженням, розміром, бюджетом та поясненнями. |
| 005 | Runner: Medium size socks (39), ent | 700 ₴ | 39 | apparel_footwear | running | **WARN** | NEAR-MISS ПЕРЕВИЩЕННЯ: Бюджет 700 ₴, товар 950 ₴ (перевищення на 250 ₴). |
| 006 | Runner: Medium size socks (40), whi | 1000 ₴ | 40 | apparel_footwear | running | **PASS** | Ідеальний збіг за спорядженням, розміром, бюджетом та поясненнями. |
| 007 | Runner: Medium size socks (41), dar | 1000 ₴ | 41 | apparel_footwear | running | **PASS** | Ідеальний збіг за спорядженням, розміром, бюджетом та поясненнями. |
| 008 | Runner: Medium size winter thermal  | 1200 ₴ | 40 | apparel_footwear | running | **PASS** | Ідеальний збіг за спорядженням, розміром, бюджетом та поясненнями. |
| 009 | Runner: Medium size winter thermal  | 1200 ₴ | 39 | apparel_footwear | running | **PASS** | Ідеальний збіг за спорядженням, розміром, бюджетом та поясненнями. |
| 010 | Runner: Large size socks (43), entr | 800 ₴ | 43 | apparel_footwear | running | **WARN** | NEAR-MISS ПЕРЕВИЩЕННЯ: Бюджет 800 ₴, товар 950 ₴ (перевищення на 150 ₴). |
| 011 | Runner: Large size socks (43), whit | 1000 ₴ | 43 | apparel_footwear | running | **PASS** | Ідеальний збіг за спорядженням, розміром, бюджетом та поясненнями. |
| 012 | Runner: Large size socks (44), dark | 1000 ₴ | 44 | apparel_footwear | running | **PASS** | Ідеальний збіг за спорядженням, розміром, бюджетом та поясненнями. |
| 013 | Runner: Large size winter thermal s | 1200 ₴ | 43 | apparel_footwear | running | **PASS** | Ідеальний збіг за спорядженням, розміром, бюджетом та поясненнями. |
| 014 | Runner: Large size socks (42), warm | 1200 ₴ | 42 | apparel_footwear | running | **PASS** | Ідеальний збіг за спорядженням, розміром, бюджетом та поясненнями. |
| 015 | Runner: XL size socks (46), entry b | 750 ₴ | 46 | apparel_footwear | running | **WARN** | NEAR-MISS ПЕРЕВИЩЕННЯ: Бюджет 750 ₴, товар 950 ₴ (перевищення на 200 ₴). |
| 016 | Runner: XL size socks (46), dark, r | 1000 ₴ | 46 | apparel_footwear | running | **PASS** | Ідеальний збіг за спорядженням, розміром, бюджетом та поясненнями. |
| 017 | Runner: XL size socks (47), white,  | 1000 ₴ | 47 | apparel_footwear | running | **PASS** | Ідеальний збіг за спорядженням, розміром, бюджетом та поясненнями. |
| 018 | Runner: XL size winter thermal sock | 1200 ₴ | 46 | apparel_footwear | running | **PASS** | Ідеальний збіг за спорядженням, розміром, бюджетом та поясненнями. |
| 019 | Runner: Unspecified size socks, tra | 1000 ₴ | any | apparel_footwear | running | **WARN** | ЗСУВ ЗАМОВЧУВАННЯ: При неуточненому розмірі система нав'язує гігантський розмір «46–48» (бо він найдешевший за 950 грн). |
| 020 | Runner: Unspecified size socks, eve | 1100 ₴ | any | apparel_footwear | running | **WARN** | ЗСУВ ЗАМОВЧУВАННЯ: При неуточненому розмірі система нав'язує гігантський розмір «46–48» (бо він найдешевший за 950 грн). |
| 021 | Runner: Unspecified size socks, eve | 1000 ₴ | any | apparel_footwear | running | **WARN** | ЗСУВ ЗАМОВЧУВАННЯ: При неуточненому розмірі система нав'язує гігантський розмір «46–48» (бо він найдешевший за 950 грн). |
| 022 | Runner: Premium budget socks bundle | 1500 ₴ | 43 | apparel_footwear | running | **PASS** | Ідеальний збіг за спорядженням, розміром, бюджетом та поясненнями. |
| 023 | Runner: Premium budget socks bundle | 1500 ₴ | 40 | apparel_footwear | running | **PASS** | Ідеальний збіг за спорядженням, розміром, бюджетом та поясненнями. |
| 024 | Runner: High budget (2000 UAH), col | 2000 ₴ | 44 | apparel_footwear | running | **PASS** | Ідеальний збіг за спорядженням, розміром, бюджетом та поясненнями. |
| 025 | Runner: High budget (2500 UAH), war | 2500 ₴ | 41 | apparel_footwear | running | **WARN** | ВИТІК ЇЖІ/СНЕКІВ: Набір [race-expert-115] 'Набір «Підготовка до забігу»' містить їстівні батончики/печиво/сублімати у розділі спорядження. |
| 026 | Runner: Race accessories (bib belt, | 1500 ₴ | any | sports_accessories | running | **FAIL** | ВИТІК ЇЖІ/СНЕКІВ: Набір [race-expert-197] 'Набір «Бігова екіпіровка»' містить їстівні батончики/печиво/сублімати у розділі спорядження. |
| 027 | Runner: Race bib belt & cap, Russia | 1500 ₴ | any | sports_accessories | running | **WARN** | ВИТІК ЇЖІ/СНЕКІВ: Набір [race-expert-197] 'Набір «Бігова екіпіровка»' містить їстівні батончики/печиво/сублімати у розділі спорядження. |
| 028 | Runner: Running gear with bottle &  | 1300 ₴ | any | sports_accessories | running | **FAIL** | КРИТИЧНИЙ ВИТІК БОДІБІЛДИНГУ: Набір [race-expert-068] 'Набір «Чоловіча сила Race Expert Club» — абонемент на 3 місяці' містить банку чистого КРЕАТИНУ моногідрату у відповідь на запит спортивного екіпірування! |
| 029 | Runner: Accessories, tight budget 8 | 800 ₴ | any | sports_accessories | running | **FAIL** | КРИТИЧНИЙ ВИТІК БОДІБІЛДИНГУ: Набір [race-expert-068] 'Набір «Чоловіча сила Race Expert Club» — абонемент на 3 місяці' містить банку чистого КРЕАТИНУ моногідрату у відповідь на запит спортивного екіпірування! |
| 030 | Runner: Accessories, entry budget 6 | 600 ₴ | any | sports_accessories | running | **FAIL** | КРИТИЧНИЙ ВИТІК БОДІБІЛДИНГУ: Набір [race-expert-068] 'Набір «Чоловіча сила Race Expert Club» — абонемент на 3 місяці' містить банку чистого КРЕАТИНУ моногідрату у відповідь на запит спортивного екіпірування! |
| 031 | Runner: Accessories, 1000 UAH budge | 1000 ₴ | any | sports_accessories | running | **FAIL** | КРИТИЧНИЙ ВИТІК БОДІБІЛДИНГУ: Набір [race-expert-068] 'Набір «Чоловіча сила Race Expert Club» — абонемент на 3 місяці' містить банку чистого КРЕАТИНУ моногідрату у відповідь на запит спортивного екіпірування! |
| 032 | Runner: Accessories, 1200 UAH budge | 1200 ₴ | any | sports_accessories | running | **FAIL** | КРИТИЧНИЙ ВИТІК БОДІБІЛДИНГУ: Набір [race-expert-068] 'Набір «Чоловіча сила Race Expert Club» — абонемент на 3 місяці' містить банку чистого КРЕАТИНУ моногідрату у відповідь на запит спортивного екіпірування! |
| 033 | Runner: Warm season accessories (bo | 1500 ₴ | any | sports_accessories | running | **FAIL** | ДОМІНУВАННЯ АБОНЕМЕНТА: Набір [race-expert-025] є насамперед 3-місячною підпискою на клуб, а не реальним спортивним спорядженням. |
| 034 | Runner: Cold season accessories | 1500 ₴ | any | sports_accessories | running | **WARN** | ДОМІНУВАННЯ АБОНЕМЕНТА: Набір [race-expert-095] є насамперед 3-місячною підпискою на клуб, а не реальним спортивним спорядженням. |
| 035 | Runner: Everyday running accessorie | 1500 ₴ | any | sports_accessories | running | **FAIL** | КРИТИЧНИЙ ВИТІК БОДІБІЛДИНГУ: Набір [race-expert-068] 'Набір «Чоловіча сила Race Expert Club» — абонемент на 3 місяці' містить банку чистого КРЕАТИНУ моногідрату у відповідь на запит спортивного екіпірування! |
| 036 | Runner: Race prep accessories, prem | 2000 ₴ | any | sports_accessories | running | **FAIL** | ВИТІК ЇЖІ/СНЕКІВ: Набір [race-expert-197] 'Набір «Бігова екіпіровка»' містить їстівні батончики/печиво/сублімати у розділі спорядження. |
| 037 | Runner: Accessories with shoe size  | 1500 ₴ | 43 | sports_accessories | running | **FAIL** | КРИТИЧНИЙ ВИТІК БОДІБІЛДИНГУ: Набір [race-expert-068] 'Набір «Чоловіча сила Race Expert Club» — абонемент на 3 місяці' містить банку чистого КРЕАТИНУ моногідрату у відповідь на запит спортивного екіпірування! |
| 038 | Runner: Accessories with shoe size  | 1500 ₴ | 37 | sports_accessories | running | **WARN** | ВИТІК ДОБАВОК/ВІТАМІНІВ: Набір [race-expert-150] 'Набір «Тренувальний ресурс Race Expert Club» — абонемент на 3 місяці' містить фармакологічні добавки (BCAA/карнітин/вітаміни) у розділі одягу та екіпірування. |
| 039 | Runner: Accessories with shoe size  | 1500 ₴ | 46 | sports_accessories | running | **FAIL** | ВИТІК ДОБАВОК/ВІТАМІНІВ: Набір [race-expert-150] 'Набір «Тренувальний ресурс Race Expert Club» — абонемент на 3 місяці' містить фармакологічні добавки (BCAA/карнітин/вітаміни) у розділі одягу та екіпірування. |
| 040 | Runner: Accessories without club me | 1500 ₴ | any | sports_accessories | running | **FAIL** | ВИТІК ЇЖІ/СНЕКІВ: Набір [race-expert-197] 'Набір «Бігова екіпіровка»' містить їстівні батончики/печиво/сублімати у розділі спорядження. |
| 041 | Hiker: Trekking accessories (1500 U | 1500 ₴ | any | sports_accessories | hiking | **WARN** | ПОРУШЕННЯ КАТЕГОРІЇ: Користувач просив спортивні аксесуари, але отримав виключно шкарпетки [race-expert-034] 'Набір «Ритм твого руху»'. |
| 042 | Hiker: Outdoor accessories, cold se | 1500 ₴ | any | sports_accessories | hiking | **WARN** | ДОМІНУВАННЯ АБОНЕМЕНТА: Набір [race-expert-091] є насамперед 3-місячною підпискою на клуб, а не реальним спортивним спорядженням. |
| 043 | Hiker: Outdoor accessories, budget  | 1000 ₴ | any | sports_accessories | hiking | **FAIL** | ДОМІНУВАННЯ АБОНЕМЕНТА: Набір [race-expert-091] є насамперед 3-місячною підпискою на клуб, а не реальним спортивним спорядженням. |
| 044 | Hiker: Outdoor accessories, event p | 1600 ₴ | any | sports_accessories | hiking | **WARN** | ПОРУШЕННЯ КАТЕГОРІЇ: Користувач просив спортивні аксесуари, але отримав виключно шкарпетки [race-expert-034] 'Набір «Ритм твого руху»'. |
| 045 | Cyclist: Cycling accessories (1500  | 1500 ₴ | any | sports_accessories | cycling | **FAIL** | ВИТІК ДОБАВОК/ВІТАМІНІВ: Набір [race-expert-150] 'Набір «Тренувальний ресурс Race Expert Club» — абонемент на 3 місяці' містить фармакологічні добавки (BCAA/карнітин/вітаміни) у розділі одягу та екіпірування. |
| 046 | Cyclist: Cycling accessories, warm  | 1500 ₴ | any | sports_accessories | cycling | **WARN** | ДОМІНУВАННЯ АБОНЕМЕНТА: Набір [race-expert-025] є насамперед 3-місячною підпискою на клуб, а не реальним спортивним спорядженням. |
| 047 | Cyclist: Cycling accessories, entry | 700 ₴ | any | sports_accessories | cycling | **FAIL** | ВИТІК ДОБАВОК/ВІТАМІНІВ: Набір [race-expert-150] 'Набір «Тренувальний ресурс Race Expert Club» — абонемент на 3 місяці' містить фармакологічні добавки (BCAA/карнітин/вітаміни) у розділі одягу та екіпірування. |
| 048 | Walker: Walking accessories for dai | 1500 ₴ | any | sports_accessories | walking | **WARN** | ДОМІНУВАННЯ АБОНЕМЕНТА: Набір [race-expert-091] є насамперед 3-місячною підпискою на клуб, а не реальним спортивним спорядженням. |
| 049 | Walker: Walking accessories, budget | 1000 ₴ | any | sports_accessories | walking | **FAIL** | ДОМІНУВАННЯ АБОНЕМЕНТА: Набір [race-expert-091] є насамперед 3-місячною підпискою на клуб, а не реальним спортивним спорядженням. |
| 050 | Walker: Walking accessories, cold s | 1500 ₴ | any | sports_accessories | walking | **FAIL** | ДОМІНУВАННЯ АБОНЕМЕНТА: Набір [race-expert-091] є насамперед 3-місячною підпискою на клуб, а не реальним спортивним спорядженням. |
| 051 | Athlete: Foam roller & massage ball | 1500 ₴ | any | sports_accessories | running | **FAIL** | КРИТИЧНИЙ ВИТІК БОДІБІЛДИНГУ: Набір [race-expert-068] 'Набір «Чоловіча сила Race Expert Club» — абонемент на 3 місяці' містить банку чистого КРЕАТИНУ моногідрату у відповідь на запит спортивного екіпірування! |
| 052 | Fitness: Jump rope & ab roller for  | 1500 ₴ | any | sports_accessories | any | **FAIL** | КРИТИЧНИЙ ВИТІК БОДІБІЛДИНГУ: Набір [race-expert-068] 'Набір «Чоловіча сила Race Expert Club» — абонемент на 3 місяці' містить банку чистого КРЕАТИНУ моногідрату у відповідь на запит спортивного екіпірування! |
| 053 | Yogi: Yoga mat & resistance band | 1500 ₴ | any | sports_accessories | walking | **FAIL** | Неочікувана порожня видача для валідного запиту: no_exact_match |
| 054 | Fitness: Home fitness kit with grid | 1500 ₴ | any | sports_accessories | any | **FAIL** | КРИТИЧНИЙ ВИТІК БОДІБІЛДИНГУ: Набір [race-expert-068] 'Набір «Чоловіча сила Race Expert Club» — абонемент на 3 місяці' містить банку чистого КРЕАТИНУ моногідрату у відповідь на запит спортивного екіпірування! |
| 055 | Athlete: Kuznetsov acupressure mat  | 1500 ₴ | any | sports_accessories | any | **FAIL** | КРИТИЧНИЙ ВИТІК БОДІБІЛДИНГУ: Набір [race-expert-068] 'Набір «Чоловіча сила Race Expert Club» — абонемент на 3 місяці' містить банку чистого КРЕАТИНУ моногідрату у відповідь на запит спортивного екіпірування! |
| 056 | Fitness: Training gear, entry budge | 750 ₴ | any | sports_accessories | running | **FAIL** | КРИТИЧНИЙ ВИТІК БОДІБІЛДИНГУ: Набір [race-expert-068] 'Набір «Чоловіча сила Race Expert Club» — абонемент на 3 місяці' містить банку чистого КРЕАТИНУ моногідрату у відповідь на запит спортивного екіпірування! |
| 057 | Fitness: Bath towels for training / | 1500 ₴ | any | sports_accessories | any | **FAIL** | КРИТИЧНИЙ ВИТІК БОДІБІЛДИНГУ: Набір [race-expert-068] 'Набір «Чоловіча сила Race Expert Club» — абонемент на 3 місяці' містить банку чистого КРЕАТИНУ моногідрату у відповідь на запит спортивного екіпірування! |
| 058 | Fitness: Towel & shaker set without | 1500 ₴ | any | sports_accessories | running | **FAIL** | ВИТІК ЇЖІ/СНЕКІВ: Набір [race-expert-197] 'Набір «Бігова екіпіровка»' містить їстівні батончики/печиво/сублімати у розділі спорядження. |
| 059 | Runner: Post-run massage gear, Russ | 1500 ₴ | any | sports_accessories | running | **FAIL** | КРИТИЧНИЙ ВИТІК БОДІБІЛДИНГУ: Набір [race-expert-068] 'Набір «Чоловіча сила Race Expert Club» — абонемент на 3 місяці' містить банку чистого КРЕАТИНУ моногідрату у відповідь на запит спортивного екіпірування! |
| 060 | Fitness: Premium home gym gear (250 | 2500 ₴ | any | sports_accessories | any | **FAIL** | КРИТИЧНИЙ ВИТІК БОДІБІЛДИНГУ: Набір [race-expert-068] 'Набір «Чоловіча сила Race Expert Club» — абонемент на 3 місяці' містить банку чистого КРЕАТИНУ моногідрату у відповідь на запит спортивного екіпірування! |
| 061 | Fitness: Mobility equipment, cold s | 1500 ₴ | any | sports_accessories | walking | **FAIL** | Неочікувана порожня видача для валідного запиту: no_exact_match |
| 062 | Fitness: Speed jump rope and hand g | 1500 ₴ | any | sports_accessories | running | **FAIL** | КРИТИЧНИЙ ВИТІК БОДІБІЛДИНГУ: Набір [race-expert-068] 'Набір «Чоловіча сила Race Expert Club» — абонемент на 3 місяці' містить банку чистого КРЕАТИНУ моногідрату у відповідь на запит спортивного екіпірування! |
| 063 | Fitness: Yoga mat without membershi | 1500 ₴ | any | sports_accessories | any | **FAIL** | ВИТІК ЇЖІ/СНЕКІВ: Набір [race-expert-197] 'Набір «Бігова екіпіровка»' містить їстівні батончики/печиво/сублімати у розділі спорядження. |
| 064 | Runner: Acupressure & foam roller,  | 1600 ₴ | any | sports_accessories | running | **FAIL** | КРИТИЧНИЙ ВИТІК БОДІБІЛДИНГУ: Набір [race-expert-068] 'Набір «Чоловіча сила Race Expert Club» — абонемент на 3 місяці' містить банку чистого КРЕАТИНУ моногідрату у відповідь на запит спортивного екіпірування! |
| 065 | Fitness: Everyday fitness accessori | 1200 ₴ | any | sports_accessories | any | **FAIL** | КРИТИЧНИЙ ВИТІК БОДІБІЛДИНГУ: Набір [race-expert-068] 'Набір «Чоловіча сила Race Expert Club» — абонемент на 3 місяці' містить банку чистого КРЕАТИНУ моногідрату у відповідь на запит спортивного екіпірування! |
| 066 | Hiker: Winter trekking thermal sock | 1200 ₴ | 43 | apparel_footwear | hiking | **PASS** | Ідеальний збіг за спорядженням, розміром, бюджетом та поясненнями. |
| 067 | Hiker: Winter trekking thermal sock | 1200 ₴ | 40 | apparel_footwear | hiking | **PASS** | Ідеальний збіг за спорядженням, розміром, бюджетом та поясненнями. |
| 068 | Hiker: Winter trekking thermal sock | 1200 ₴ | 37 | apparel_footwear | hiking | **PASS** | Ідеальний збіг за спорядженням, розміром, бюджетом та поясненнями. |
| 069 | Hiker: Winter trekking thermal sock | 1200 ₴ | 46 | apparel_footwear | hiking | **FAIL** | ДОМІНУВАННЯ АБОНЕМЕНТА: Набір [race-expert-092] є насамперед 3-місячною підпискою на клуб, а не реальним спортивним спорядженням. |
| 070 | Hiker: Summer trekking socks size 4 | 1200 ₴ | 43 | apparel_footwear | hiking | **WARN** | ДОМІНУВАННЯ АБОНЕМЕНТА: Набір [race-expert-094] є насамперед 3-місячною підпискою на клуб, а не реальним спортивним спорядженням. |
| 071 | Hiker: Hiking socks, entry budget 6 | 600 ₴ | 40 | apparel_footwear | hiking | **WARN** | ЦІНОВИЙ ЯКІР: Бюджет 600 ₴ нижчий за мінімальний у каталозі (950 ₴). Запропоновано базовий набір за 1058 ₴. |
| 072 | Hiker: General hiking gear, any com | 1500 ₴ | 43 | any | hiking | **PASS** | Ідеальний збіг за спорядженням, розміром, бюджетом та поясненнями. |
| 073 | Hiker: Cold season outdoor gift kit | 1500 ₴ | any | any | hiking | **PASS** | Ідеальний збіг за спорядженням, розміром, бюджетом та поясненнями. |
| 074 | Hiker: Everyday hiking socks size 4 | 1000 ₴ | 41 | apparel_footwear | hiking | **WARN** | NEAR-MISS ПЕРЕВИЩЕННЯ: Бюджет 1000 ₴, товар 1058 ₴ (перевищення на 58 ₴). |
| 075 | Hiker: Premium hiking gear pack (20 | 2000 ₴ | 43 | any | hiking | **PASS** | Ідеальний збіг за спорядженням, розміром, бюджетом та поясненнями. |
| 076 | Cyclist: Cycling socks size 43, reg | 1000 ₴ | 43 | apparel_footwear | cycling | **FAIL** | Неочікувана порожня видача для валідного запиту: no_match |
| 077 | Cyclist: Cycling socks size 40, reg | 1000 ₴ | 40 | apparel_footwear | cycling | **FAIL** | Неочікувана порожня видача для валідного запиту: no_match |
| 078 | Cyclist: Winter cycling thermal soc | 1200 ₴ | 44 | apparel_footwear | cycling | **FAIL** | Неочікувана порожня видача для валідного запиту: no_match |
| 079 | Cyclist: General cycling gear, any  | 1500 ₴ | any | any | cycling | **FAIL** | ВИТІК ДОБАВОК/ВІТАМІНІВ: Набір [race-expert-150] 'Набір «Тренувальний ресурс Race Expert Club» — абонемент на 3 місяці' містить фармакологічні добавки (BCAA/карнітин/вітаміни) у розділі одягу та екіпірування. |
| 080 | Cyclist: Cycling gear, event prep ( | 1500 ₴ | any | any | cycling | **FAIL** | ВИТІК ДОБАВОК/ВІТАМІНІВ: Набір [race-expert-150] 'Набір «Тренувальний ресурс Race Expert Club» — абонемент на 3 місяці' містить фармакологічні добавки (BCAA/карнітин/вітаміни) у розділі одягу та екіпірування. |
| 081 | Walker: Walking socks size 37, ever | 1000 ₴ | 37 | apparel_footwear | walking | **PASS** | Ідеальний збіг за спорядженням, розміром, бюджетом та поясненнями. |
| 082 | Walker: Walking socks size 40, ever | 1000 ₴ | 40 | apparel_footwear | walking | **PASS** | Ідеальний збіг за спорядженням, розміром, бюджетом та поясненнями. |
| 083 | Walker: Walking socks size 43, ever | 1000 ₴ | 43 | apparel_footwear | walking | **PASS** | Ідеальний збіг за спорядженням, розміром, бюджетом та поясненнями. |
| 084 | Walker: Winter walking thermal sock | 1200 ₴ | 43 | apparel_footwear | walking | **PASS** | Ідеальний збіг за спорядженням, розміром, бюджетом та поясненнями. |
| 085 | Walker: Walking gear, any component | 1200 ₴ | any | any | walking | **PASS** | Ідеальний збіг за спорядженням, розміром, бюджетом та поясненнями. |
| 086 | Swimmer: Swimming gear, any compone | 1500 ₴ | any | any | swimming | **FAIL** | Таксономічний глухий кут: 'swimming' офіційно дозволений у вікторині для 'gear', але в каталозі 0 товарів для плавання! |
| 087 | Swimmer: Swimming accessories (towe | 1500 ₴ | any | sports_accessories | swimming | **FAIL** | Таксономічний глухий кут: 'swimming' офіційно дозволений у вікторині для 'gear', але в каталозі 0 товарів для плавання! |
| 088 | Swimmer: Swimming gear, training sc | 1500 ₴ | any | any | swimming | **FAIL** | Таксономічний глухий кут: 'swimming' офіційно дозволений у вікторині для 'gear', але в каталозі 0 товарів для плавання! |
| 089 | Swimmer: Swimming gear, event prepa | 2000 ₴ | any | any | swimming | **FAIL** | Таксономічний глухий кут: 'swimming' офіційно дозволений у вікторині для 'gear', але в каталозі 0 товарів для плавання! |
| 090 | Swimmer: Swimming gear, budget 1000 | 1000 ₴ | any | any | swimming | **FAIL** | Таксономічний глухий кут: 'swimming' офіційно дозволений у вікторині для 'gear', але в каталозі 0 товарів для плавання! |
| 091 | Athlete: General gear, running, siz | 1500 ₴ | 43 | any | running | **PASS** | Ідеальний збіг за спорядженням, розміром, бюджетом та поясненнями. |
| 092 | Athlete: General gear, running, siz | 1000 ₴ | 40 | any | running | **PASS** | Ідеальний збіг за спорядженням, розміром, бюджетом та поясненнями. |
| 093 | Athlete: General gear, cold season, | 1500 ₴ | 43 | any | any | **PASS** | Ідеальний збіг за спорядженням, розміром, бюджетом та поясненнями. |
| 094 | Athlete: General gear, warm season, | 1500 ₴ | 40 | any | any | **WARN** | ДОМІНУВАННЯ АБОНЕМЕНТА: Набір [race-expert-025] є насамперед 3-місячною підпискою на клуб, а не реальним спортивним спорядженням. |
| 095 | Athlete: General gear, event prepar | 1500 ₴ | any | any | any | **PASS** | Ідеальний збіг за спорядженням, розміром, бюджетом та поясненнями. |
| 096 | Edge Case: String shoe size '42-44' | 1200 ₴ | 42-44 | apparel_footwear | any | **FAIL** | Двигун впав з винятком DraftMatchError при передачі діапазону розміру рядком '42-44'. |
| 097 | Edge Case: Extremely low budget (40 | 400 ₴ | any | apparel_footwear | any | **WARN** | ЗСУВ ЗАМОВЧУВАННЯ: При неуточненому розмірі система нав'язує гігантський розмір «46–48» (бо він найдешевший за 950 грн). |
| 098 | Edge Case: Ultra-high budget (3000  | 3000 ₴ | any | any | any | **PASS** | Ідеальний збіг за спорядженням, розміром, бюджетом та поясненнями. |
| 099 | Edge Case: Extreme shoe size (50) | 1500 ₴ | 50 | apparel_footwear | any | **WARN** | ДОМІНУВАННЯ АБОНЕМЕНТА: Набір [race-expert-092] є насамперед 3-місячною підпискою на клуб, а не реальним спортивним спорядженням. |
| 100 | Edge Case: Contradictory request (s | 1500 ₴ | 43 | sports_accessories | any | **FAIL** | КРИТИЧНИЙ ВИТІК БОДІБІЛДИНГУ: Набір [race-expert-068] 'Набір «Чоловіча сила Race Expert Club» — абонемент на 3 місяці' містить банку чистого КРЕАТИНУ моногідрату у відповідь на запит спортивного екіпірування! |


## 5. Strategic Recommendations for Quiz & Catalog Engineering
1. **Purge Gym Sets from `foot_apparel_comfort` in `quiz-set-audit.json`:** Immediately strip `foot_apparel_comfort` from sets `race-expert-009, 028, 029, 040, 068, 075, 142, 147, 148, 149, 150, 151, 155, 162, 206`. They belong strictly to `training` and `strength_muscle_training`.
2. **Fix `why_suitable` Deceptive Claims:** Remove the hardcoded phrase `(без сторонніх речей)` unless verified that 100% of the set's items belong to the requested component class.
3. **Fix Swimming Option:** Either onboard genuine swimming gear (silicone caps, anti-fog goggles, microfiber swim towels) or remove `swimming` from `ACTIVITY_OPTIONS_BY_GOAL['gear']`.
4. **Add `cycling` to Socks Activity Scope:** Add `cycling` to `activity_groups` for sport sock bundles so cyclists can receive socks.
5. **Fix Sizing UX:** Parse range strings like `'42-44'` or `'39-41'` safely. For size-unspecified queries, prompt the user for their shoe size rather than silently defaulting to size 46–48.
6. **Expand Entry-Level Gear Catalog:** Introduce standalone gear items under 800 ₴: single pairs of technical running socks (250–350 ₴), standalone soft flasks (400–600 ₴), and elastic race number belts (350–500 ₴).