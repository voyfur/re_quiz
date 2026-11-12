# QA Agent 4: Comprehensive Evaluation Report — Food, Hydration & Outdoors
**Role:** QA Agent 4 — Nutritionist, Hiker, Endurance Athlete & Human Buyer Specialist  
**Test Suite:** 100 Realistic Buyer Scenarios across `food` (40), `hydration` (30), and `outdoors` (30)  
**Audit Evidence Source:** `wiki/projects/quiz-set-audit.json`  

## 1. Executive Summary & Verdict Scorecard
Across 100 diverse buyer tests covering budgets from 500 to 3500 UAH, all component classes, activity types, timings, and locales, the quiz matcher achieved:
- **PASS:** 37 (37.0%) — clean, logical matching, relevant products, and truthful justifications.
- **WARN:** 19 (19.0%) — partial matches, minor domain gaps (e.g., bath towels or gym passes bundled into food), or validation restrictions on common activities.
- **FAIL:** 44 (44.0%) — severe logic flaws: blatant taxonomy leaks (pills/creatine in food; spirulina/zinc in hydration), 0 matches for dehydrated camping meals due to tag misclassification, or deceptive '(без сторонніх речей)' claims.

| Category | Total Tests | PASS | WARN | FAIL | Pass Rate |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Food & Snacks (`food`)** | 40 | 10 | 11 | 19 | 25.0% |
| **Hydration (`hydration`)** | 30 | 11 | 5 | 14 | 36.7% |
| **Outdoors & Hiking (`outdoors`)** | 30 | 16 | 3 | 11 | 53.3% |
| **OVERALL** | **100** | **37** | **19** | **44** | **37.0%** |

---
## 2. Critical Human Logic & Domain Flaws Discovered
### A. The Dehydrated Camping Meal Blindspot (100% Failure Rate)
> [!CAUTION]
> When a hiker or camper explicitly selects `component_class: 'dehydrated_meal'`, the matcher returns **0 results (`status: no_match`)**.
The store actively stocks genuine dehydrated camping meals (`Похідна їжа ЇDLO 2.0` RE11494, `Похідна їжа ЇDLO Club` RE11495, `Похідна їжа 3.0` RE88977). However, in `quiz-set-audit.json`, every single ЇDLO set was classified as `protein_carbohydrate_food` rather than `dehydrated_meal`. Consequently, the `dehydrated_meal` filter is dead code that guarantees complete failure for hikers seeking camp dinners.

### B. Gross Taxonomy Leakage into Hydration
> [!WARNING]
> Non-hydration pill supplements leak directly into the `hydration` section.
- **RE11513 («Енергія і очищення»):** Contains Now Foods Organic Spirulina (100 tablets) + Zinc Picolinate. Spirulina and zinc pills have zero electrolyte replacement value and do not prevent dehydration or cramps.
- **RE88943 («Концентрація в дорозі»):** Contains Lion's Mane mushroom pills + Acetyl-L-Carnitine + Vitamin D3. Recommending mushroom nootropics to a thirsty runner asking for hydration is completely illogical.
- **RE11636 («Вибух сили»):** Contains OstroVit Creatine Monohydrate 500g + Pre-Workout caffeine powder, with zero electrolytes or water flasks.

### C. Pill Bottles, Towels & Creatine Powders Leaking into Food
- **RE11688 («Набір маси»):** Contains 1,000g Anabolic Mass gainer powder and 300g pure Creatine Monohydrate. An endurance athlete looking for portable snacks on runs is shown a 1kg bodybuilding powder tub.
- **RE89489 («Основа регулярних тренувань»):** Contains a 135×70 cm cotton bath towel, creatine, shaker, and 3-month gym membership.
- **RE11632 («Розум і Сила»):** Contains Mind Shi 4Mushroom nootropic capsules (60 caps) bundled with cookies.

### D. Deceptive Explanation Claims: '(без сторонніх речей)'
When a user specifies a component class like `protein_carbohydrate_food`, `_build_why_suitable()` generates:
`Категорія товарів: у наборі саме Спортивне харчування та батончики (без сторонніх речей).`
In reality, the recommended set frequently contains bath towels, commemorative medals, mushroom capsules, or 3-month gym club memberships. Stating '(без сторонніх речей)' ('without third-party/extraneous items') destroys buyer trust when extraneous items make up the majority of the bundle value.

### E. Artificial Validation Walls for Real Athletic Scenarios
- **Walkers eating food:** Walkers and Nordic walkers covering 15-25 km need energy snacks. `draft_matcher` throws `DraftMatchError: activity is not supported for the selected need` if `walking` is paired with `food`.
- **Hikers needing hydration:** Hikers carrying heavy packs in summer heat desperately need electrolytes and flasks. `draft_matcher` throws `DraftMatchError` if `hiking` or `walking` is selected for `hydration`.
- **Trail runners in Outdoors:** Trail runners looking under `outdoors` get rejected because `running` is disallowed.
- **Hiker meal timings:** Hikers who want hearty meals before or after long treks get rejected because `outdoors` disallows `before_or_after_training`.

### F. Low Budget Coverage Desert (< 1058 UAH)
The entire catalog has **0 food sets under 1149 UAH**, **0 hydration sets under 1225 UAH**, and **0 outdoor sets under 1058 UAH**. Any user entering a realistic budget of 500–1000 UAH receives either `no_match` or near-misses. The quiz must clearly communicate that the store only sells premium multi-item bundles, not single items.

---
## 3. Detailed Results of all 100 Scenarios
| ID | Goal | Activity | Class | Budget | Status | Verdict | Key Evaluation Note |
| :--- | :--- | :--- | :--- | :--- | :--- | :---: | :--- |
| TC001 | `food` | running | protein_carbohydrate_food | 1500 ₴ | `matched` | **PASS** | Clean match, truthful explanation |
| TC002 | `food` | running | protein_carbohydrate_food | 1600 ₴ | `matched` | **FAIL** | [RE11660 - Набір «Марафонець»]: Deceptive explanation: System claims 'Категорія товарів… |
| TC003 | `food` | running | protein_carbohydrate_food | 800 ₴ | `floor_anchor` | **WARN** | Catalog Coverage Gap: Budget 800 UAH returned 0 results and 0 near-misses. Lowest set i… |
| TC004 | `food` | running | protein_carbohydrate_food | 3000 ₴ | `matched` | **FAIL** | [RE11660 - Набір «Марафонець»]: Deceptive explanation: System claims 'Категорія товарів… |
| TC005 | `food` | running | protein_carbohydrate_food | 1500 ₴ | `matched` | **FAIL** | [RE89450 - Набір «Fitly мікс» — абонемент на 3 місяці]: Set includes a 3-month gym club… |
| TC006 | `food` | running | protein_carbohydrate_food | 1300 ₴ | `no_match` | **FAIL** | [RE89450 - Набір «Fitly мікс» — абонемент на 3 місяці]: Set includes a 3-month gym club… |
| TC007 | `food` | running | protein_carbohydrate_food | 1600 ₴ | `no_exact_match` | **PASS** | Clean match, truthful explanation |
| TC008 | `food` | running | protein_carbohydrate_food | 2500 ₴ | `matched` | **PASS** | Clean match, truthful explanation |
| TC009 | `food` | running | protein_carbohydrate_food | 500 ₴ | `floor_anchor` | **WARN** | Catalog Coverage Gap: Budget 500 UAH returned 0 results and 0 near-misses. Lowest set i… |
| TC010 | `food` | running | protein_carbohydrate_food | 1500 ₴ | `matched` | **FAIL** | [RE11019 - Набір «Щоденний комфорт Race Expert Club» — абонемент на 3 місяці]: Deceptiv… |
| TC011 | `food` | cycling | protein_carbohydrate_food | 1500 ₴ | `matched` | **PASS** | Clean match, truthful explanation |
| TC012 | `food` | cycling | protein_carbohydrate_food | 1700 ₴ | `matched` | **FAIL** | [RE11660 - Набір «Марафонець»]: Deceptive explanation: System claims 'Категория товаров… |
| TC013 | `food` | cycling | protein_carbohydrate_food | 1400 ₴ | `no_match` | **FAIL** | [RE89450 - Набір «Fitly мікс» — абонемент на 3 місяці]: Set includes a 3-month gym club… |
| TC014 | `food` | cycling | protein_carbohydrate_food | 1500 ₴ | `no_exact_match` | **PASS** | Clean match, truthful explanation |
| TC015 | `food` | cycling | protein_carbohydrate_food | 900 ₴ | `floor_anchor` | **WARN** | Catalog Coverage Gap: Budget 900 UAH returned 0 results and 0 near-misses. Lowest set i… |
| TC016 | `food` | cycling | protein_carbohydrate_food | 2800 ₴ | `matched` | **FAIL** | [RE89450 - Набір «Fitly мікс» — абонемент на 3 місяці]: Set includes a 3-month gym club… |
| TC017 | `food` | cycling | protein_carbohydrate_food | 1500 ₴ | `no_exact_match` | **PASS** | Clean match, truthful explanation |
| TC018 | `food` | cycling | protein_carbohydrate_food | 1500 ₴ | `no_exact_match` | **PASS** | Clean match, truthful explanation |
| TC019 | `food` | hiking | protein_carbohydrate_food | 1500 ₴ | `no_exact_match` | **PASS** | Clean match, truthful explanation |
| TC020 | `food` | hiking | dehydrated_meal | 1600 ₴ | `no_match` | **FAIL** | Major Catalog/Taxonomy Flaw: Buyer asked for 'dehydrated_meal', but 0 sets matched beca… |
| TC021 | `food` | hiking | protein_carbohydrate_food | 1200 ₴ | `no_match` | **PASS** | Clean match, truthful explanation |
| TC022 | `food` | hiking | protein_carbohydrate_food | 1400 ₴ | `matched` | **FAIL** | [RE11695 - Набір «Мандрівний смаколик Race Expert Club» — абонемент на 3 місяці]: Set i… |
| TC023 | `food` | hiking | protein_carbohydrate_food | 750 ₴ | `floor_anchor` | **WARN** | Catalog Coverage Gap: Budget 750 UAH returned 0 results and 0 near-misses. Lowest set i… |
| TC024 | `food` | hiking | protein_carbohydrate_food | 3500 ₴ | `matched` | **FAIL** | [RE11695 - Набір «Мандрівний смаколик Race Expert Club» — абонемент на 3 місяці]: Set i… |
| TC025 | `food` | hiking | protein_carbohydrate_food | 1500 ₴ | `matched` | **FAIL** | [RE11695 - Набір «Мандрівний смаколик Race Expert Club» — абонемент на 3 місяці]: Set i… |
| TC026 | `food` | hiking | protein_carbohydrate_food | 1500 ₴ | `matched` | **FAIL** | [RE11695 - Набір «Мандрівний смаколик Race Expert Club» — абонемент на 3 місяці]: Set i… |
| TC027 | `food` | walking | protein_carbohydrate_food | 1500 ₴ | `validation_error` | **WARN** | Human logic flaw: Walkers/Nordic walkers eat portable snacks on long walks, but matcher… |
| TC028 | `food` | walking | protein_carbohydrate_food | 1000 ₴ | `validation_error` | **WARN** | Human logic flaw: Walkers/Nordic walkers eat portable snacks on long walks, but matcher… |
| TC029 | `food` | other | any | 1500 ₴ | `matched` | **WARN** | [RE11632 - Набір «Розум і Сила»]: Mushroom nootropic pill bottle bundled into food/snac… |
| TC030 | `food` | other | protein_carbohydrate_food | 1300 ₴ | `matched` | **FAIL** | [RE11695 - Набір «Мандрівний смаколик Race Expert Club» — абонемент на 3 місяці]: Set i… |
| TC031 | `food` | running | hydration_items | 1500 ₴ | `matched` | **PASS** | Clean match, truthful explanation |
| TC032 | `food` | running | sports_accessories | 1500 ₴ | `validation_error` | **WARN** | Buyer selected unsupported component class 'sports_accessories' for goal 'food': compon… |
| TC033 | `food` | running | apparel_footwear | 1500 ₴ | `validation_error` | **WARN** | Buyer selected unsupported component class 'apparel_footwear' for goal 'food': componen… |
| TC034 | `food` | running | any | 600 ₴ | `floor_anchor` | **WARN** | Catalog Coverage Gap: Budget 600 UAH returned 0 results and 0 near-misses. Lowest set i… |
| TC035 | `food` | running | protein_carbohydrate_food | 1200 ₴ | `no_match` | **FAIL** | [RE89450 - Набір «Fitly мікс» — абонемент на 3 місяці]: Set includes a 3-month gym club… |
| TC036 | `food` | cycling | protein_carbohydrate_food | 1300 ₴ | `no_match` | **FAIL** | [RE89450 - Набір «Fitly мікс» — абонемент на 3 місяці]: Set includes a 3-month gym club… |
| TC037 | `food` | hiking | protein_carbohydrate_food | 1600 ₴ | `general_auto` | **FAIL** | [RE89418 - Набір м'ясних снеків (соєвий соус) Race Expert Club — абонемент на 3 місяці]… |
| TC038 | `food` | running | protein_carbohydrate_food | 1800 ₴ | `matched` | **FAIL** | [RE11660 - Набір «Марафонець»]: Deceptive explanation: System claims 'Категорія товарів… |
| TC039 | `food` | any | any | 3200 ₴ | `matched` | **WARN** | [RE11632 - Набір «Розум і Сила»]: Mushroom nootropic pill bottle bundled into food/snac… |
| TC040 | `food` | running | protein_carbohydrate_food | 1500 ₴ | `matched` | **FAIL** | [RE11026 - Набір «Спортивний подарунок»]: Deceptive explanation: System claims 'Категор… |
| TC041 | `hydration` | running | hydration_items | 1500 ₴ | `matched` | **FAIL** | [RE11786 - Набір «Тренувальний ресурс Race Expert Club» — абонемент на 3 місяці]: Decep… |
| TC042 | `hydration` | cycling | sports_accessories | 1600 ₴ | `matched` | **FAIL** | [RE11786 - Набір «Тренувальний ресурс Race Expert Club» — абонемент на 3 місяці]: Decep… |
| TC043 | `hydration` | running | hydration_items | 800 ₴ | `floor_anchor` | **WARN** | Catalog Coverage Gap: Budget 800 UAH returned 0 results and 0 near-misses. Lowest set i… |
| TC044 | `hydration` | running | hydration_items | 3000 ₴ | `matched` | **FAIL** | [RE11786 - Набір «Тренувальний ресурс Race Expert Club» — абонемент на 3 місяці]: Decep… |
| TC045 | `hydration` | functional_training | hydration_items | 1500 ₴ | `no_match` | **PASS** | Clean match, truthful explanation |
| TC046 | `hydration` | strength_training | hydration_items | 1500 ₴ | `no_match` | **PASS** | Clean match, truthful explanation |
| TC047 | `hydration` | hiking | hydration_items | 1500 ₴ | `validation_error` | **FAIL** | Athlete/Hiker flaw: Hikers sweat heavily and urgently need hydration/electrolytes, but … |
| TC048 | `hydration` | walking | hydration_items | 1500 ₴ | `validation_error` | **FAIL** | Athlete/Hiker flaw: Hikers sweat heavily and urgently need hydration/electrolytes, but … |
| TC049 | `hydration` | cycling | hydration_items | 1400 ₴ | `matched` | **FAIL** | [RE11786 - Набір «Тренувальний ресурс Race Expert Club» — абонемент на 3 місяці]: Decep… |
| TC050 | `hydration` | running | hydration_items | 1500 ₴ | `no_exact_match` | **PASS** | Clean match, truthful explanation |
| TC051 | `hydration` | running | hydration_items | 1000 ₴ | `no_match` | **FAIL** | Budget 1000 UAH exceeded, but system gracefully returned 1 near-miss recommendation(s). |
| TC052 | `hydration` | running | hydration_items | 1500 ₴ | `matched` | **FAIL** | [RE11021 - Набір «Літній старт Race Expert Club» — абонемент на 3 місяці]: Deceptive ex… |
| TC053 | `hydration` | running | hydration_items | 1500 ₴ | `matched` | **FAIL** | [RE11786 - Набір «Тренувальний ресурс Race Expert Club» — абонемент на 3 місяці]: Decep… |
| TC054 | `hydration` | cycling | sports_accessories | 2500 ₴ | `matched` | **FAIL** | [RE11786 - Набір «Тренувальний ресурс Race Expert Club» — абонемент на 3 місяці]: Decep… |
| TC055 | `hydration` | running | hydration_items | 500 ₴ | `floor_anchor` | **WARN** | Catalog Coverage Gap: Budget 500 UAH returned 0 results and 0 near-misses. Lowest set i… |
| TC056 | `hydration` | running | dehydrated_meal | 1500 ₴ | `validation_error` | **WARN** | Buyer selected unsupported component class 'dehydrated_meal' for goal 'hydration': comp… |
| TC057 | `hydration` | running | apparel_footwear | 1500 ₴ | `validation_error` | **WARN** | Buyer selected unsupported component class 'apparel_footwear' for goal 'hydration': com… |
| TC058 | `hydration` | running | protein_carbohydrate_food | 1600 ₴ | `matched` | **PASS** | Clean match, truthful explanation |
| TC059 | `hydration` | cycling | hydration_items | 1500 ₴ | `matched` | **FAIL** | [RE11021 - Набір «Літній старт Race Expert Club» — абонемент на 3 місяці]: Deceptive ex… |
| TC060 | `hydration` | running | hydration_items | 1500 ₴ | `matched` | **PASS** | Clean match, truthful explanation |
| TC061 | `hydration` | running | hydration_items | 1500 ₴ | `no_exact_match` | **PASS** | Clean match, truthful explanation |
| TC062 | `hydration` | running | sports_accessories | 1300 ₴ | `no_match` | **FAIL** | [RE11013 - Набір «Бігова пара»]: Running socks + bottle set offered with no electrolyte… |
| TC063 | `hydration` | cycling | hydration_items | 1200 ₴ | `no_match` | **FAIL** | [RE11786 - Набір «Тренувальний ресурс Race Expert Club» — абонемент на 3 місяці]: Decep… |
| TC064 | `hydration` | running | hydration_items | 2200 ₴ | `matched` | **PASS** | Clean match, truthful explanation |
| TC065 | `hydration` | running | any | 1250 ₴ | `matched` | **PASS** | Clean match, truthful explanation |
| TC066 | `hydration` | any | any | 3500 ₴ | `matched` | **PASS** | Clean match, truthful explanation |
| TC067 | `hydration` | strength_training | protein_carbohydrate_food | 1500 ₴ | `no_match` | **PASS** | Clean match, truthful explanation |
| TC068 | `hydration` | cycling | sports_accessories | 700 ₴ | `floor_anchor` | **WARN** | Catalog Coverage Gap: Budget 700 UAH returned 0 results and 0 near-misses. Lowest set i… |
| TC069 | `hydration` | functional_training | hydration_items | 1350 ₴ | `no_match` | **PASS** | Clean match, truthful explanation |
| TC070 | `hydration` | running | hydration_items | 1650 ₴ | `matched` | **FAIL** | [RE89451 - Набір «Відновлення після тренування» — абонемент на 3 місяці]: Deceptive exp… |
| TC071 | `outdoors` | hiking | apparel_footwear | 1200 ₴ | `matched` | **PASS** | Clean match, truthful explanation |
| TC072 | `outdoors` | hiking | apparel_footwear | 1200 ₴ | `matched` | **PASS** | Clean match, truthful explanation |
| TC073 | `outdoors` | hiking | apparel_footwear | 1100 ₴ | `matched` | **PASS** | Clean match, truthful explanation |
| TC074 | `outdoors` | hiking | dehydrated_meal | 1600 ₴ | `no_match` | **FAIL** | Major Catalog/Taxonomy Flaw: Buyer asked for 'dehydrated_meal', but 0 sets matched beca… |
| TC075 | `outdoors` | hiking | protein_carbohydrate_food | 1500 ₴ | `matched` | **FAIL** | [RE11695 - Набір «Мандрівний смаколик Race Expert Club» — абонемент на 3 місяці]: Decep… |
| TC076 | `outdoors` | hiking | sports_accessories | 1500 ₴ | `matched` | **FAIL** | [RE11721 - Набір «Сублімований мікс Race Expert Club» — абонемент на 3 місяці]: Decepti… |
| TC077 | `outdoors` | hiking | apparel_footwear | 800 ₴ | `no_match` | **PASS** | Budget 800 UAH exceeded, but system gracefully returned 3 near-miss recommendation(s). |
| TC078 | `outdoors` | hiking | any | 3000 ₴ | `matched` | **PASS** | Clean match, truthful explanation |
| TC079 | `outdoors` | walking | protein_carbohydrate_food | 1500 ₴ | `matched` | **FAIL** | [RE11495 - Набір «Похідна їжа ЇDLO Race Expert Club» — абонемент на 3 місяці]: Deceptiv… |
| TC080 | `outdoors` | cycling | protein_carbohydrate_food | 1500 ₴ | `no_match` | **PASS** | Clean match, truthful explanation |
| TC081 | `outdoors` | running | hydration_items | 1700 ₴ | `validation_error` | **WARN** | Athlete flaw: Trail/mountain runners look under Outdoors for wilderness kits, but match… |
| TC082 | `outdoors` | hiking | protein_carbohydrate_food | 1500 ₴ | `validation_error` | **WARN** | Human logic flaw: Hikers eat meals before or after long hikes, but Outdoors disallows '… |
| TC083 | `outdoors` | hiking | protein_carbohydrate_food | 1500 ₴ | `no_exact_match` | **PASS** | Clean match, truthful explanation |
| TC084 | `outdoors` | hiking | sports_accessories | 1500 ₴ | `matched` | **FAIL** | [RE11721 - Набір «Сублімований мікс Race Expert Club» — абонемент на 3 місяці]: Decepti… |
| TC085 | `outdoors` | hiking | apparel_footwear | 1300 ₴ | `matched` | **PASS** | Clean match, truthful explanation |
| TC086 | `outdoors` | hiking | hydration_items | 1600 ₴ | `no_match` | **PASS** | Clean match, truthful explanation |
| TC087 | `outdoors` | hiking | any | 600 ₴ | `floor_anchor` | **WARN** | Catalog Coverage Gap: Budget 600 UAH returned 0 results and 0 near-misses. Lowest set i… |
| TC088 | `outdoors` | hiking | apparel_footwear | 1000 ₴ | `no_match` | **PASS** | Budget 1000 UAH exceeded, but system gracefully returned 3 near-miss recommendation(s). |
| TC089 | `outdoors` | hiking | dehydrated_meal | 1500 ₴ | `no_match` | **FAIL** | Major Catalog/Taxonomy Flaw: Buyer asked for 'dehydrated_meal', but 0 sets matched beca… |
| TC090 | `outdoors` | hiking | sports_accessories | 1600 ₴ | `matched` | **FAIL** | [RE11721 - Набір «Сублімований мікс Race Expert Club» — абонемент на 3 місяці]: Decepti… |
| TC091 | `outdoors` | hiking | apparel_footwear | 1200 ₴ | `matched` | **PASS** | Clean match, truthful explanation |
| TC092 | `outdoors` | walking | protein_carbohydrate_food | 1400 ₴ | `no_match` | **FAIL** | [RE11495 - Набір «Похідна їжа ЇDLO Race Expert Club» — абонемент на 3 місяці]: Deceptiv… |
| TC093 | `outdoors` | hiking | protein_carbohydrate_food | 1300 ₴ | `matched` | **FAIL** | [RE11695 - Набір «Мандрівний смаколик Race Expert Club» — абонемент на 3 місяці]: Decep… |
| TC094 | `outdoors` | hiking | apparel_footwear | 1058 ₴ | `matched` | **PASS** | Clean match, truthful explanation |
| TC095 | `outdoors` | hiking | apparel_footwear | 1000 ₴ | `no_match` | **PASS** | Budget 1000 UAH exceeded, but system gracefully returned 2 near-miss recommendation(s). |
| TC096 | `outdoors` | hiking | any | 3500 ₴ | `matched` | **PASS** | Clean match, truthful explanation |
| TC097 | `outdoors` | hiking | sports_accessories | 1500 ₴ | `matched` | **FAIL** | [RE11721 - Набір «Сублімований мікс Race Expert Club» — абонемент на 3 місяці]: Decepti… |
| TC098 | `outdoors` | cycling | hydration_items | 1650 ₴ | `no_match` | **PASS** | Clean match, truthful explanation |
| TC099 | `outdoors` | hiking | protein_carbohydrate_food | 1500 ₴ | `matched` | **FAIL** | [RE11695 - Набір «Мандрівний смаколик Race Expert Club» — абонемент на 3 місяці]: Decep… |
| TC100 | `outdoors` | other | any | 1500 ₴ | `matched` | **PASS** | Clean match, truthful explanation |

---
## 4. Prioritized Action Plan for Engineering & Catalog Teams
1. **Reclassify ЇDLO Sets as `dehydrated_meal`:** Immediately update `RE11494`, `RE11495`, and `RE88977` in `wiki/projects/quiz-set-audit.json` to include `dehydrated_meal` in `component_classes_from_listed_names`.
2. **Disqualify Pill Tubs & Mass Gainers from Hydration and Food:**
   - Remove `hydration_electrolytes` family from `RE11513` (Spirulina/Zinc), `RE88943` (Lion's Mane/D3), and `RE11636` (Creatine/Pre-workout).
   - Remove `portable_food_snacks` family from `RE11688` (1kg Anabolic Mass gainer).
3. **Fix Validation Option Matrix in `draft_matcher.py`:**
   - Add `hiking` and `walking` to `ACTIVITY_OPTIONS_BY_GOAL['hydration']`.
   - Add `walking` to `ACTIVITY_OPTIONS_BY_GOAL['food']`.
   - Add `before_or_after_training` to `USE_TIMINGS_BY_GOAL['outdoors']`.
4. **Refactor Explanation Copy:** Eliminate the absolute claim `(без сторонніх речей)` / `(без посторонних позиций)` if the set contains bundle extras like towels, shakers, medals, or club memberships.
5. **Introduce Low-Budget Starter Bundles:** Create 3–5 targeted entry-level sets priced at 499–799 UAH (e.g. 5x gels + 2x electrolyte sticks pack) to satisfy low-budget shoppers.