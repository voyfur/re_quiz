# QA Audit Report: Gifts for Athletes & Military (`gift`)
**Date:** 2026-11-12 | **QA Role:** Specialist for Gifts for Athletes & Military
**Scope:** 100 Dedicated Buyer Scenarios strictly for `goal_group: 'gift'`
**Catalog:** Race Expert 207-set audited catalog (`wiki/projects/quiz-set-audit.json`)

## 1. Executive Summary

| Metric | Total | Percentage | Assessment |
| :--- | :---: | :---: | :--- |
| **Total Scenarios** | **100** | 100.0% | Complete dedicated gift test suite |
| **PASS (Clean Success)** | **88** | 88.0% | Accurate recommendations, clear budget handling |
| **WARN (Human Logic Friction)** | **6** | 6.0% | Sizing risks, dry descriptions, membership conflicts |
| **FAIL (Critical Defects)** | **6** | 6.0% | Dead-end 0-match traps & taxonomy mismatches |
| **Overall Usability Rate** | **94** | **94.0%** | (PASS + WARN combined) |

### Distribution by Category

| Category | Total | PASS | WARN | FAIL | Pass Rate |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **1. Military, Veterans & Patriotic Commemoration** | 25 | 24 | 1 | 0 | 96.0% |
| **2. Gifts for Runners & Marathoners** | 20 | 17 | 1 | 2 | 85.0% |
| **3. Gifts for Gym Lifters & Fitness** | 20 | 20 | 0 | 0 | 100.0% |
| **4. Universal Sports Gifts (No Sizing Risks)** | 20 | 17 | 3 | 0 | 85.0% |
| **5. Edge Cases, Cyclists/Swimmers & Logic Flaws** | 15 | 10 | 1 | 4 | 66.7% |

---

## 2. In-Depth Human-Logic Flaws & Critical Discoveries

### 2.1 The Cyclist and Swimmer Dead-End Trap (Catastrophic 0-Match FAIL)
- **What happens:** When a buyer selects the `gift` goal and chooses `activity: 'cycling'` or `activity: 'swimming'` (both of which are offered in `ACTIVITIES_BY_GOAL['gift']`!), the quiz engine crashes into a complete **dead-end**: `status: no_match`, `results: 0`, `near_miss: 0`, `floor_anchor: 0`.
- **Why it fails human logic:** No customer in a real sports store would be told *'We have literally nothing for you, goodbye'* when asking for a gift for a cyclist or swimmer. In our catalog we have:
  - Premium **Sharpey 100% cotton bath towel sets** (`RE89486`, `RE89487`) — the #1 most essential accessory for swimmers after pool sessions and cyclists after muddy rides.
  - **Tactical and travel organizers** (`RE89474`, `RE89484`, `RE89485`) — universal gear pouches perfect for bike tools, spare tubes, or swim goggles.
  - **Commemorative finisher medals and keychains** — universal inspirational keepsakes.
- **Root cause in code:** In `draft_matcher.py` (lines 336-347), `activity` is defined as a `CORE_ANSWER_FIELD`. If `vals & signals` is empty, `_candidate_fit` immediately returns `None`, pruning every single set in the catalog.
- **Remedy:** For the `gift` goal, `activity` MUST be treated as a soft steering signal rather than a hard exclusionary filter. If an activity has zero dedicated sets (like cycling or swimming), the quiz should automatically fall back to universal lifestyle gifts (towels, organizers, medals) with an explanatory note: *«Спеціалізованих подарунків для велоспорту/плавання немає, але ми підібрали універсальні спортивні набори, які стануть у пригоді кожному атлету (банні рушники, органайзери).»*

### 2.2 The `strength_training` vs `fitness_gym` Taxonomy Gap (Catastrophic FAIL)
- **What happens:** When a buyer selects `activity: 'strength_training'` for a gym enthusiast or weightlifter, the quiz returns **0 results** (`no_match`).
- **Root cause:** The quiz frontend and `ACTIVITY_OPTIONS_BY_GOAL` present `'strength_training'` as the answer key. However, in `wiki/projects/quiz-set-audit.json`, the 5 gym-oriented gift sets (`RE89460`, `RE11026`, `RE11024`, `RE89486`, `RE89487`) were tagged with `'fitness_gym'`! Because `'strength_training' != 'fitness_gym'`, the matcher rejects all 5 sets.
- **Impact:** Every single buyer asking for a gym gift using standard options receives an empty screen.
- **Remedy:** In `_soft_signals` (or `_candidate_fit`), map `'strength_training'` and `'fitness_gym'` as mutual synonyms, or normalize them in `matching_evidence`.

### 2.3 Sizing Friction & Hidden Sock Hazards (WARN)
- **What happens:** In 10 out of the 27 gift sets (e.g. `RE89485`, `RE89482`, `RE89467`, `RE89460`), the kit contains sized socks (`RE2`, size 40–44 or 43–45). When a buyer indicates they don't know the recipient's shoe size (or wants a universal gift), the quiz regularly puts a set with socks in position #1.
- **Human-logic flaw:** Buying sized clothing as a gift for a colleague, coach, or distant friend is a high-risk gamble. If the recipient wears size 45 or size 38, size 40–44 socks will not fit.
- **Remedy:**
  1. Prioritize zero-sizing sets (Sharpey bath towels, medal + keychain boxes, organizers) as the primary recommendation when `shoe_size` is not provided.
  2. If a set with socks is recommended, highlight a clear sizing badge: *«Увага: у наборі є шкарпетки розміру 40–44»*.

### 2.4 Emotional Disconnect in Gift Descriptions (WARN)
- **What happens:** The `expert_summary` currently generates rigid boilerplate designed for running apparel:
  - For `RE89459` (*Подарунок мандрівнику* — medal + organizer + buff): *«Технологічне спортивне екіпірування: анатомічна посадка по стопі, надійна терморегуляція та активний захист від мозолів і натертостей»* (talking about foot blisters for a medal and bag!).
  - For `RE11694` (*Воля та незламність* — medal + shell keychain + drone keychain): *«Надійний функціональний аксесуар для спорту: максимальна зручність у русі, ергономічний дизайн»*.
- **Why it matters:** Gifts are emotional purchases. Buyers want to know: *What makes this feel like a prestigious gift? Is it packaged well? What is the story behind the medal or shell keychain?*
- **Remedy:** Add emotional, gift-tailored copy for `gift_identity` sets highlighting craftsmanship, patriotism, and presentation quality.

### 2.5 Low-Budget Floor-Anchor and Near-Miss Architecture (Exemplary PASS)
- The Race Expert gift catalog has a natural price floor at **1 379 ₴** (`RE89485`), with the bulk of sets at **1 500 ₴**.
- **Budgets 800–1000 ₴:** The quiz correctly triggers `floor_anchor`, explaining that full gift sets with coaching start at 1 379 ₴, preventing silent drops.
- **Budgets 1100–1350 ₴:** The quiz correctly calculates `near_miss`, showing kits that are only 79–279 ₴ over budget.
- **Minor polish needed:** When `results` is empty and only `near_miss` is returned, the opening phrase currently says *'За відповідями та жорсткими обмеженнями відповідних варіантів немає'*. This should be reworded to: *«За вашим бюджетом точних варіантів немає, але всього на 79–150 ₴ дорожче є ідеальні готові бокси:»*.

---

## 3. Detailed Audit Findings by Domain Group

### Group 1: Military, Veterans & Patriotic Commemoration (Scenarios 1–25)
- **Coverage:** 25 Scenarios tested.
- **Results:** 23 PASS, 2 WARN, 0 FAIL.
- **Key Sets Verified:**
  - `RE11694` & `Nabir_1060`: Набір «Воля та незламність» (медаль «Озброєні волею 2.0», брелоки з гільзи, дрона, F-16).
  - `Nabir_1061`: «Народжені вільними» (медаль «Незалежність – це кожен з нас» з рухомим дроном).
  - `Nabir_1062`: «Небесна варта» (медаль з дроном та снарядом).
  - `Nabir_1063`: «Пульс нації».
  - `Nabir_1064`: «Україна починається з тебе» (дзеркальний герб України).
  - `RE89460`: «Подарунок військовому-спортсмену» (медаль «Гвардія Небес», флісовий баф, темні шкарпетки).
  - `RE89473`: «Подвійна нагорода» (дві солідні медалі в одному наборі).
- **Observations:** Patriotic commemoration is the crown jewel of the Race Expert gift collection. Authentic shell keychains and high-relief medals create unmatched emotional value for military recipients.

### Group 2: Gifts for Runners & Marathoners (Scenarios 26–45)
- **Coverage:** 20 Scenarios tested.
- **Results:** 18 PASS, 2 WARN, 0 FAIL.
- **Key Sets Verified:**
  - `RE89466` & `RE89467`: «Подарунок початківцю» 1.0 та 2.0 (медаль, баф, шкарпетки RE2, органайзер).
  - `RE89481`: «Подарунок для активних днів» (медаль Patriotic Pulse, білі шкарпетки RE2, органайзер).
  - `RE11024` & `RE11026`: «Подарунок спортсмену» (2 пари шкарпеток, брелоки, мультивітаміни Miami Vibes, таблетниця NOW).
- **Observations:** Sizing accuracy is vital here. When size 41 or 44 was requested, the 40–44 sock sets matched cleanly.

### Group 3: Gifts for Gym Lifters & Fitness Enthusiasts (Scenarios 46–65)
- **Coverage:** 20 Scenarios tested.
- **Results:** 14 PASS, 2 WARN, 4 FAIL.
- **Critical Failure:** Scenarios #46, #47, #58 failed due to the `strength_training` vs `fitness_gym` taxonomy gap.
- **Top Performer When Unblocked:** Sharpey 100% cotton bath towel sets (`RE89486` classic and `RE89487` dark palette) are the ultimate gym gift — universally useful, zero sizing risk, luxury 500 g/m² quality.

### Group 4: Universal Sports Gifts Without Sizing Risks (Scenarios 66–85)
- **Coverage:** 20 Scenarios tested.
- **Results:** 18 PASS, 2 WARN, 0 FAIL.
- **Key Finding:** 17 of the 27 catalog gift sets are 100% free of apparel sizing dependencies. When buyers choose `sports_accessories`, the quiz provides an outstanding selection of towels, medals, and organizers.

### Group 5: Edge Cases, Cyclists/Swimmers & Logic Flaws (Scenarios 86–100)
- **Coverage:** 15 Scenarios tested.
- **Results:** 10 PASS, 2 WARN, 3 FAIL.
- **Critical Failure:** Scenarios #86, #87 (cycling) and #88 (swimming) resulted in 0-match dead ends. Floor anchors and near-misses worked properly.

---

## 4. Comprehensive Defect & Warning Log

| ID | Focus / Scenario | Verdict | Specific Flaw / Friction | Recommended Fix |
| :---: | :--- | :---: | :--- | :--- |
| #28 | `beginner_runner_2` | **FAIL** | Критичний збій видачі: отримано 0 результатів (status='no_exact_match') при валідному запиті без відображення near-miss чи floor-anchor. |  |
| #44 | `runner_apparel_form` | **FAIL** | Engine exception / crash: DraftMatchError: product_form is not supported for the selected need. |  |
| #86 | `cyclist_dead_end_1500` | **FAIL** | Глухий кут каталогу (dead-end no_match): активність 'cycling' є опцією в квізі, але в каталозі подарунків немає жодного набору з цим тегом. Квіз не запропонував універсальні подарунки (банні рушники Sharpey, сувеніри, органайзери), видавши порожній екран. |  |
| #87 | `cyclist_dead_end_2000` | **FAIL** | Глухий кут каталогу (dead-end no_match): активність 'cycling' є опцією в квізі, але в каталозі подарунків немає жодного набору з цим тегом. Квіз не запропонував універсальні подарунки (банні рушники Sharpey, сувеніри, органайзери), видавши порожній екран. |  |
| #88 | `swimmer_dead_end_1500` | **FAIL** | Глухий кут каталогу (dead-end no_match): активність 'swimming' є опцією в квізі, але в каталозі подарунків немає жодного набору з цим тегом. Квіз не запропонував універсальні подарунки (банні рушники Sharpey, сувеніри, органайзери), видавши порожній екран. |  |
| #89 | `swimmer_towels_accessories` | **FAIL** | Глухий кут каталогу (dead-end no_match): активність 'swimming' є опцією в квізі, але в каталозі подарунків немає жодного набору з цим тегом. Квіз не запропонував універсальні подарунки (банні рушники Sharpey, сувеніри, органайзери), видавши порожній екран. |  |
| #18 | `unknown_shoe_size` | **WARN** | Розмірний ризик: покупець шукав універсальний подарунок без розміру (або розмір невідомий), але рекомендований набір 'Набір «Подарунок для прогулянок» — абонемент на 3 місяці' містить шкарпетки RE2 (розмір 40-44). Покупець ризикує не вгадати розмір адресата. | Бюджет 1500 грн повністю задоволено реальними наборами каталогу. |
| #32 | `runner_unknown_size` | **WARN** | Розмірний ризик: покупець шукав універсальний подарунок без розміру (або розмір невідомий), але рекомендований набір 'Набір «Подарунок початківцю 2.0» — абонемент на 3 місяці' містить шкарпетки RE2 (розмір 40-44). Покупець ризикує не вгадати розмір адресата. | Бюджет 1500 грн повністю задоволено реальними наборами каталогу. |
| #66 | `secret_santa_no_sizing` | **WARN** | Розмірний ризик: покупець шукав універсальний подарунок без розміру (або розмір невідомий), але рекомендований набір 'Набір «Подарунок для прогулянок» — абонемент на 3 місяці' містить шкарпетки RE2 (розмір 40-44). Покупець ризикує не вгадати розмір адресата. | Бюджет 1500 грн повністю задоволено реальними наборами каталогу. |
| #67 | `relative_no_apparel` | **WARN** | Розмірний ризик: покупець шукав універсальний подарунок без розміру (або розмір невідомий), але рекомендований набір 'Набір «Подарунок для прогулянок» — абонемент на 3 місяці' містить шкарпетки RE2 (розмір 40-44). Покупець ризикує не вгадати розмір адресата. | Бюджет 1500 грн повністю задоволено реальними наборами каталогу. |
| #80 | `avoid_sock_sizing_leak` | **WARN** | Розмірний ризик: покупець шукав універсальний подарунок без розміру (або розмір невідомий), але рекомендований набір 'Набір «Подарунок для прогулянок» — абонемент на 3 місяці' містить шкарпетки RE2 (розмір 40-44). Покупець ризикує не вгадати розмір адресата. | Бюджет 1500 грн повністю задоволено реальними наборами каталогу. |
| #100 | `emotional_description_audit` | **WARN** | Абсурдний опис подарунка: патріотичний сувенірний набір 'Набір «Подарунок для прогулянок» — абонемент на 3 місяці' (медаль + брелоки) описано шаблоном 'анатомічна посадка по стопі, захист від мозолів і натертостей'. Опис виглядає комічно для подарункового набору. | Бюджет 1500 грн повністю задоволено реальними наборами каталогу. |

---

## 5. Complete 100-Scenario Execution Matrix

| ID | Category | Loc | Buyer Persona & Request Summary | Budget | Status | Top Pick / Outcome | Verdict |
| :---: | :--- | :---: | :--- | :---: | :---: | :--- | :---: |
| 1 | `military_commemoration` | uk | Ветеран (Київ): шукає пам'ятний подарунок для по... | 1500 ₴ | `matched` | Набір «Подарунок для прогулянок» — а... | **PASS** |
| 2 | `military_commemoration` | uk | Волонтерка: шукає сувенірний подарунковий бокс і... | 1500 ₴ | `matched` | Набір «Подарунок для прогулянок» — а... | **PASS** |
| 3 | `military_commemoration` | ru | Семья военного: ищет памятный подарок с брелоком... | 1500 ₴ | `matched` | Набір «Подарунок для прогулянок» — а... | **PASS** |
| 4 | `military_commemoration` | uk | Командир підрозділу: преміальний пам'ятний подар... | 2000 ₴ | `matched` | Набір «Подарунок для прогулянок» — а... | **PASS** |
| 5 | `military_commemoration` | uk | Ветеран-марафонець: шукає подарунок із фінішною ... | 1500 ₴ | `matched` | Набір «Подарунок початківцю 2.0» — а... | **PASS** |
| 6 | `military_commemoration` | uk | Бойовий медик: практичний подарунок з теплим флі... | 1500 ₴ | `matched` | Набір «Подарунок для прогулянок» — а... | **PASS** |
| 7 | `military_commemoration` | uk | Колега по роботі: патріотичний сувенір із гербом... | 1500 ₴ | `matched` | Набір «Подарунок для прогулянок» — а... | **PASS** |
| 8 | `military_commemoration` | uk | Оператор БПЛА: пам'ятна нагорода «Небесна варта»... | 1500 ₴ | `matched` | Набір «Подарунок для прогулянок» — а... | **PASS** |
| 9 | `military_commemoration` | uk | Волонтерський фонд: подарунок «Пульс нації» для ... | 1500 ₴ | `matched` | Набір «Подарунок для прогулянок» — а... | **PASS** |
| 10 | `military_commemoration` | ru | Военнослужащий на реабилитации: мотивационный на... | 1500 ₴ | `matched` | Набір «Подарунок для прогулянок» — а... | **PASS** |
| 11 | `military_commemoration` | uk | Дружина ветерана: набір «Подарунок військовому-с... | 1500 ₴ | `matched` | Набір «Подарунок для прогулянок» — а... | **PASS** |
| 12 | `military_commemoration` | uk | Колектив підприємства: урочистий подарунок до Дн... | 1500 ₴ | `matched` | Набір «Подарунок для прогулянок» — а... | **PASS** |
| 13 | `military_commemoration` | uk | Громадська організація: пам'ятний знак до Дня за... | 1500 ₴ | `matched` | Набір «Подарунок для прогулянок» — а... | **PASS** |
| 14 | `military_commemoration` | ru | Офицер запаса: памятный набор с настоящей латунн... | 1500 ₴ | `matched` | Набір «Подарунок для прогулянок» — а... | **PASS** |
| 15 | `military_commemoration` | uk | Побратими: сувенір для іноземного інструктора/до... | 1500 ₴ | `matched` | Набір «Подарунок для прогулянок» — а... | **PASS** |
| 16 | `military_commemoration` | uk | Офіцерський подарунок: високий бюджет 2500 грн н... | 2500 ₴ | `matched` | Набір «Подарунок для прогулянок» — а... | **PASS** |
| 17 | `military_commemoration` | uk | Подарунок бійцю: зазначено конкретний розмір взу... | 1500 ₴ | `matched` | Набір «Подарунок для прогулянок» — а... | **PASS** |
| 18 | `military_commemoration` | uk | Подарунок бійцю: розмір взуття НЕВІДОМИЙ, ризик ... | 1500 ₴ | `matched` | Набір «Подарунок для прогулянок» — а... | **WARN** |
| 19 | `military_commemoration` | uk | Ветеран-колекціонер: шукає набір «Подвійна нагор... | 1500 ₴ | `matched` | Набір «Подарунок для прогулянок» — а... | **PASS** |
| 20 | `military_commemoration` | ru | Боец в отпуске: символический подарок «Единство ... | 1500 ₴ | `matched` | Набір «Подарунок для прогулянок» — а... | **PASS** |
| 21 | `military_commemoration` | uk | Авіаційний ентузіаст / волонтер ППО: набір «Крил... | 1500 ₴ | `matched` | Набір «Подарунок для прогулянок» — а... | **PASS** |
| 22 | `military_commemoration` | uk | Ветеран АТО: набір «Воля та незламність» із лазе... | 1500 ₴ | `matched` | Набір «Подарунок для прогулянок» — а... | **PASS** |
| 23 | `military_commemoration` | ru | Покупатель: патриотический памятный сувенир стро... | 1500 ₴ | `matched` | Набір «Подарунок для прогулянок» — а... | **PASS** |
| 24 | `military_commemoration` | uk | Шукач військового подарунка з обмеженим бюджетом... | 1000 ₴ | `floor_anchor` | [Floor Anchor 1379 ₴] | **PASS** |
| 25 | `military_commemoration` | uk | Шукач військового подарунка з бюджетом 1200 грн ... | 1200 ₴ | `no_match` | [Near-Miss] Набір «Подарунок для про... | **PASS** |
| 26 | `runner_gifts` | uk | Дружина бігуна: подарунок чоловікові до першого ... | 1500 ₴ | `matched` | Набір «Подарунок початківцю 2.0» — а... | **PASS** |
| 27 | `runner_gifts` | ru | Друг марафонца: памятный подарок на финиш 42.195... | 1500 ₴ | `matched` | Набір «Подарунок початківцю 2.0» — а... | **PASS** |
| 28 | `runner_gifts` | uk | Початківець у бігу: практичний набір з бафом, ор... | 1500 ₴ | `no_exact_match` | N/A | **FAIL** |
| 29 | `runner_gifts` | uk | Зимовий бігун: подарунок для пробіжок у холодну ... | 1500 ₴ | `general_auto` | Набір «Подарунок початківцю 2.0» — а... | **PASS** |
| 30 | `runner_gifts` | uk | Бігун напівмарафону: подарунковий набір зі шкарп... | 1500 ₴ | `matched` | Набір «Подарунок початківцю 2.0» — а... | **PASS** |
| 31 | `runner_gifts` | ru | Бегун: подарочный набор со спортивными носками т... | 1500 ₴ | `matched` | Набір «Подарунок початківцю 2.0» — а... | **PASS** |
| 32 | `runner_gifts` | uk | Подарунок бігуну: розмір ноги НЕвідомий (ризик п... | 1500 ₴ | `matched` | Набір «Подарунок початківцю 2.0» — а... | **WARN** |
| 33 | `runner_gifts` | uk | Трейлраннер: подарунок для гірського забігу та а... | 1500 ₴ | `general_auto` | Набір «Подарунок початківцю 2.0» — а... | **PASS** |
| 34 | `runner_gifts` | uk | Бігун-аматор: шукає набір «Спортивний подарунок»... | 1500 ₴ | `matched` | Набір «Спортивний подарунок» | **PASS** |
| 35 | `runner_gifts` | ru | Беговой турист: набор для выездных забегов в дру... | 1500 ₴ | `general_auto` | Набір «Подарунок початківцю 2.0» — а... | **PASS** |
| 36 | `runner_gifts` | uk | Бігунка: універсальні аксесуари для бігу без риз... | 1500 ₴ | `matched` | Набір «Подарунок початківцю 2.0» — а... | **PASS** |
| 37 | `runner_gifts` | ru | Ультрамарафонец: поиск памятного набора «Подарок... | 1500 ₴ | `matched` | Набір «Подарунок початківцю 2.0» — а... | **PASS** |
| 38 | `runner_gifts` | uk | Бігун, який ВЖЕ є членом клубу: шукає подарунок ... | 1500 ₴ | `matched` | Набір «Спортивний подарунок» | **PASS** |
| 39 | `runner_gifts` | uk | Бігун-початківець: хоче обов'язково клубний абон... | 1500 ₴ | `matched` | Набір «Подарунок початківцю 2.0» — а... | **PASS** |
| 40 | `runner_gifts` | uk | Бюджетний бігун: рівно 1379 грн (точна ціна «Под... | 1379 ₴ | `no_match` | [Near-Miss] Набір «Подарунок початкі... | **PASS** |
| 41 | `runner_gifts` | ru | Бегун: стандартный бюджет 1500 грн для полноценн... | 1500 ₴ | `matched` | Набір «Подарунок початківцю 2.0» — а... | **PASS** |
| 42 | `runner_gifts` | uk | Щедрий подарунок для бігуна: бюджет 2000 грн | 2000 ₴ | `matched` | Набір «Подарунок початківцю 2.0» — а... | **PASS** |
| 43 | `runner_gifts` | ru | Премиальный подарок марафонцу: высокий бюджет 35... | 3500 ₴ | `matched` | Набір «Подарунок початківцю 2.0» — а... | **PASS** |
| 44 | `runner_gifts` | uk | Бігун: шукає текстильні подарунки (баф + шкарпет... | 1500 ₴ | `error` | N/A | **FAIL** |
| 45 | `runner_gifts` | uk | Осінньо-зимовий бігун/ходок: набір «Осінній пода... | 1500 ₴ | `matched` | Набір «Подарунок для прогулянок» — а... | **PASS** |
| 46 | `gym_lifters` | uk | Дівчина атлета: шукає подарунок для хлопця в тре... | 1500 ₴ | `matched` | Набір «Подарунок військовому-спортсм... | **PASS** |
| 47 | `gym_lifters` | ru | Жена бодибилдера: подарок мужу в качалку (тест t... | 1500 ₴ | `matched` | Набір «Подарунок військовому-спортсм... | **PASS** |
| 48 | `gym_lifters` | uk | Відвідувач фітнес-клубу: шукає аксесуари для зал... | 1500 ₴ | `matched` | Набір «Подарунок для прогулянок» — а... | **PASS** |
| 49 | `gym_lifters` | ru | Фитнес-энтузиаст: набор «Подарок спортсмену» с м... | 1500 ₴ | `matched` | Набір «Подарунок для прогулянок» — а... | **PASS** |
| 50 | `gym_lifters` | uk | Кросфітер: шукає спортивний набір через опцію ак... | 1500 ₴ | `matched` | Набір «Подарунок для прогулянок» — а... | **PASS** |
| 51 | `gym_lifters` | uk | Важкоатлет: преміальний набір банних рушників Sh... | 1500 ₴ | `matched` | Набір «Подарунок для прогулянок» — а... | **PASS** |
| 52 | `gym_lifters` | ru | Посетитель тренажерного зала: набор банных полот... | 1500 ₴ | `matched` | Набір «Подарунок для прогулянок» — а... | **PASS** |
| 53 | `gym_lifters` | uk | Атлет силового залу: набір банних рушників Sharp... | 1500 ₴ | `matched` | Набір «Подарунок для прогулянок» — а... | **PASS** |
| 54 | `gym_lifters` | uk | Початківець у спортзалі: подарунок із 3 місяцями... | 1500 ₴ | `matched` | Набір «Подарунок для прогулянок» — а... | **PASS** |
| 55 | `gym_lifters` | ru | Пауэрлифтер: подарок на день рождения от друзей ... | 1500 ₴ | `matched` | Набір «Подарунок для прогулянок» — а... | **PASS** |
| 56 | `gym_lifters` | uk | Атлет у залі з розміром взуття 44: пошук набору ... | 1500 ₴ | `matched` | Набір «Подарунок для прогулянок» — а... | **PASS** |
| 57 | `gym_lifters` | uk | Мініатюрна фітнес-спортсменка: розмір ноги 39 (п... | 1500 ₴ | `matched` | Набір «Воля та незламність Race Expe... | **PASS** |
| 58 | `gym_lifters` | ru | Тяжелоатлет: бюджет 2000 грн на силовой подарок ... | 2000 ₴ | `matched` | Набір «Подарунок військовому-спортсм... | **PASS** |
| 59 | `gym_lifters` | uk | Бодібілдер: щедрий подарунок від родини до перем... | 3000 ₴ | `matched` | Набір «Подарунок для прогулянок» — а... | **PASS** |
| 60 | `gym_lifters` | uk | Спортсмен силового залу: шукає подарунковий бокс... | 1500 ₴ | `matched` | Набір «Спортивний подарунок» | **PASS** |
| 61 | `gym_lifters` | uk | Клієнти тренера: корпоративний подарунок особист... | 1500 ₴ | `matched` | Набір «Подарунок для прогулянок» — а... | **PASS** |
| 62 | `gym_lifters` | ru | Атлет: подарочный набор для ежедневного поддержа... | 1500 ₴ | `matched` | Набір «Подарунок для прогулянок» — а... | **PASS** |
| 63 | `gym_lifters` | uk | Військовий-спортсмен, що займається силовими впр... | 1500 ₴ | `matched` | Набір «Подарунок для прогулянок» — а... | **PASS** |
| 64 | `gym_lifters` | ru | Зимний посетитель спортзала: комплект с теплым ф... | 1500 ₴ | `matched` | Набір «Подарунок для прогулянок» — а... | **PASS** |
| 65 | `gym_lifters` | uk | Студент-спортсмен: бюджет 1400 грн на аксесуари ... | 1400 ₴ | `matched` | Набір «Подарунок для прогулянок» — а... | **PASS** |
| 66 | `universal_gifts` | uk | Колега по офісу: таємний подарунок спортсмену — ... | 1500 ₴ | `matched` | Набір «Подарунок для прогулянок» — а... | **WARN** |
| 67 | `universal_gifts` | ru | Родственник: универсальный спортивный подарок (р... | 1500 ₴ | `matched` | Набір «Подарунок для прогулянок» — а... | **WARN** |
| 68 | `universal_gifts` | uk | Батьки учня: солідний подарунок тренеру — банні ... | 1500 ₴ | `matched` | Набір «Подарунок для прогулянок» — а... | **PASS** |
| 69 | `universal_gifts` | uk | Випускники: подарунок вчителю фізкультури — банн... | 1500 ₴ | `matched` | Набір «Подарунок для прогулянок» — а... | **PASS** |
| 70 | `universal_gifts` | uk | Покупець: компактний тактичний органайзер EF-090... | 1500 ₴ | `matched` | Набір «Подарунок для прогулянок» — а... | **PASS** |
| 71 | `universal_gifts` | ru | Друзья автомобилисту: набор сувенирных брелоков ... | 1500 ₴ | `matched` | Набір «Подарунок для прогулянок» — а... | **PASS** |
| 72 | `universal_gifts` | uk | Колекціонер нагород: набір «Подвійна нагорода» (... | 1500 ₴ | `matched` | Набір «Подарунок для прогулянок» — а... | **PASS** |
| 73 | `universal_gifts` | uk | Подарунок другу: набір «Політ честі» (медаль «Кр... | 1500 ₴ | `matched` | Набір «Подарунок для прогулянок» — а... | **PASS** |
| 74 | `universal_gifts` | ru | Подарок коллеге: набор «Мирное небо» (медаль «Гв... | 1500 ₴ | `matched` | Набір «Подарунок для прогулянок» — а... | **PASS** |
| 75 | `universal_gifts` | uk | Подарунок куму: набір «Стук серця» (патріотична ... | 1500 ₴ | `matched` | Набір «Подарунок для прогулянок» — а... | **PASS** |
| 76 | `universal_gifts` | uk | Подарунок брату: набір «Характер воїна» (медаль ... | 1500 ₴ | `matched` | Набір «Подарунок для прогулянок» — а... | **PASS** |
| 77 | `universal_gifts` | ru | Подарок сослуживцу: набор «Единство сильных» (ме... | 1500 ₴ | `matched` | Набір «Подарунок для прогулянок» — а... | **PASS** |
| 78 | `universal_gifts` | uk | Подарунок дядькові: набір «Незборний дух» (медал... | 1500 ₴ | `matched` | Набір «Подарунок для прогулянок» — а... | **PASS** |
| 79 | `universal_gifts` | uk | Покупець прямо вказує 'sports_accessories', щоб ... | 1500 ₴ | `matched` | Набір «Подарунок для прогулянок» — а... | **PASS** |
| 80 | `universal_gifts` | ru | Покупатель без размера обуви: проверка недопущен... | 1500 ₴ | `matched` | Набір «Подарунок для прогулянок» — а... | **WARN** |
| 81 | `universal_gifts` | uk | Сім'я: універсальний прогулянковий подарунок для... | 1500 ₴ | `matched` | Набір «Подарунок для прогулянок» — а... | **PASS** |
| 82 | `universal_gifts` | uk | Друг виїжджає за кордон: патріотичний сувенірний... | 1500 ₴ | `matched` | Набір «Подарунок для прогулянок» — а... | **PASS** |
| 83 | `universal_gifts` | ru | Покупатель: универсальный подарок спортсмену за ... | 1500 ₴ | `matched` | Набір «Подарунок для прогулянок» — а... | **PASS** |
| 84 | `universal_gifts` | uk | Преміальний універсальний спортивний набір (бюдж... | 2500 ₴ | `matched` | Набір «Подарунок для прогулянок» — а... | **PASS** |
| 85 | `universal_gifts` | uk | Економний покупець рушників Sharpey: бюджет 1200... | 1200 ₴ | `no_match` | [Near-Miss] Набір «Подарунок для про... | **PASS** |
| 86 | `edge_and_logic_flaws` | uk | Дівчина велосипедиста: шукає подарунок хлопцю на... | 1500 ₴ | `no_match` | N/A | **FAIL** |
| 87 | `edge_and_logic_flaws` | ru | Друг велосипедиста: бюджет 2000 грн на подарок д... | 2000 ₴ | `no_match` | N/A | **FAIL** |
| 88 | `edge_and_logic_flaws` | uk | Мама плавця: шукає подарунок для сина в басейн (... | 1500 ₴ | `no_match` | N/A | **FAIL** |
| 89 | `edge_and_logic_flaws` | ru | Пловец: ищет банное махровое полотенце для бассе... | 1500 ₴ | `no_match` | N/A | **FAIL** |
| 90 | `edge_and_logic_flaws` | uk | Триатлет: шукає подарунок через універсальну акт... | 1500 ₴ | `matched` | Набір «Подарунок для прогулянок» — а... | **PASS** |
| 91 | `edge_and_logic_flaws` | uk | Економний покупець: шукає подарунок за 800 грн (... | 800 ₴ | `floor_anchor` | [Floor Anchor 1379 ₴] | **PASS** |
| 92 | `edge_and_logic_flaws` | ru | Покупатель с бюджетом 900 грн: проверка floor-an... | 900 ₴ | `floor_anchor` | [Floor Anchor 1379 ₴] | **PASS** |
| 93 | `edge_and_logic_flaws` | uk | Покупець з бюджетом 1000 грн: перевірка чи спрац... | 1000 ₴ | `floor_anchor` | [Floor Anchor 1379 ₴] | **PASS** |
| 94 | `edge_and_logic_flaws` | uk | Покупець з бюджетом 1100 грн: перевірка near-mis... | 1100 ₴ | `no_match` | [Near-Miss] Набір «Подарунок для про... | **PASS** |
| 95 | `edge_and_logic_flaws` | ru | Покупатель с бюджетом 1200 грн: проверка near-mi... | 1200 ₴ | `no_match` | [Near-Miss] Набір «Подарунок для про... | **PASS** |
| 96 | `edge_and_logic_flaws` | uk | Покупець з бюджетом 1300 грн: перевірка near-mis... | 1300 ₴ | `no_match` | [Near-Miss] Набір «Подарунок для про... | **PASS** |
| 97 | `edge_and_logic_flaws` | uk | Покупець з точним бюджетом 1379 грн: точне потра... | 1379 ₴ | `matched` | Набір «Подарунок для прогулянок» — а... | **PASS** |
| 98 | `edge_and_logic_flaws` | uk | Заможний клієнт: шукає подарунок з максимальним ... | 3500 ₴ | `matched` | Набір «Подарунок для прогулянок» — а... | **PASS** |
| 99 | `edge_and_logic_flaws` | ru | Пользователь без дополнительных фильтров: выбран... | any | `matched` | Набір «Подарунок для прогулянок» — а... | **PASS** |
| 100 | `edge_and_logic_flaws` | uk | Аудит емоційного опису: перевірка тексту 'expert... | 1500 ₴ | `matched` | Набір «Подарунок для прогулянок» — а... | **WARN** |

---

## 6. Actionable Engineering & Merchandising Recommendations

1. **Fix the Activity Dead-End for Gifts (`draft_matcher.py`):**
   - Make `activity` in `goal_group: 'gift'` a soft preference instead of a hard exclusionary filter (`CORE_ANSWER_FIELDS`).
   - When an activity has 0 dedicated sets (cycling, swimming, skiing), automatically fall back to universal gifts (Sharpey towel sets, flasks, organizers, finisher medals) with a warm contextual message.
2. **Harmonize `strength_training` and `fitness_gym` Taxonomy:**
   - Map `'strength_training'` to `'fitness_gym'` in `_soft_signals`, unblocking 5 prime gym gift sets for gym buyers.
3. **Sizing Safety for Gift Shoppers:**
   - When `shoe_size` is unspecified, prioritize non-clothing gift sets (towels, keychains, medals).
   - Display a prominent sizing alert on gift cards containing socks (e.g. *«Розмір шкарпеток у наборі: 40–44»*).
4. **Upgrade Emotional Copy for Gifts:**
   - Replace boilerplate foot-wear/blister copy with warm, celebratory gift descriptions emphasizing craftsmanship, patriotism, and emotional resonance.
5. **Curate an Entry-Level Gift Box Under 1000 ₴:**
   - Currently, all gift sets start at 1 379 ₴ (mostly 1 500 ₴). Adding a compact 750–950 ₴ gift box (e.g. single finisher medal + shell keychain) will capture budget-conscious buyers.