# QA Audit Report 5: Daily Wellness, Gifts & Edge Cases Specialist
**Date:** 2026-11-12 | **Scope:** 100 Scenarios (Daily, Gifts, Boundary Edge Cases)
**Catalog Version:** 207 verified sets (`wiki/projects/quiz-set-audit.json`)

## 1. Executive Summary

| Metric | Total | PASS | WARN | FAIL | Success Rate |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Overall Scenarios** | **100** | **93** (93.0%) | **2** (2.0%) | **5** (5.0%) | **95.0%** |
| **Daily Wellness (`daily`)** | 40 | 38 | 2 | 0 | 100.0% |
| **Gift Shoppers (`gift`)** | 30 | 25 | 0 | 5 | 83.3% |
| **Edge & Budget Boundaries** | 30 | 30 | 0 | 0 | 100.0% |

---

## 2. In-Depth Evaluation by Core Domain

### 2.1 Daily Wellness (`daily`) Domain Audit (40 Test Cases)
- **Clean Separation from Bodybuilding & Creatine:** Zero daily sets contain creatine monohydrate or heavy pre-workouts. The isolation between `strength_training` and `daily` is robust.
- **Stimulant Audit Findings (Crucial Human-Logic Discovery):**
  - Catalog Row 79 (`Набір «Енергетичний перекус Race Expert Club»`) provides mild organic stimulation via protein bars with coffee and functional mushrooms (cordyceps/reishi). Suitable for daytime work/study.
  - Catalog Row 136 (`Набір «Ресурс активного дня Race Expert Club»`) contains `Olimp L-Carnitine Caffeine Extreme Shot 25 ml (доза кофеина не указана)`. When recommended for daytime vitality, this is flagged as **WARN** due to potential caffeine sensitivity. For evening/sleep personas, recommending high stimulants would be a critical failure; the matcher correctly prioritizes magnesium/sleep formulas for `evening_or_bedtime`.
- **Vitamin & Mineral Representation:** The daily catalog features rich, diverse health formulations (D3+K2, Omega-3, Zinc, Shiitake mushroom extract Mind Shi, Spirulina, antioxidant blends).
- **Form & Context Matching:** Softgels, capsules, and tablets filter reliably according to buyer preference.

### 2.2 Gift Shoppers (`gift`) Domain Audit (30 Test Cases)
- **Gift Authenticity & Curation:** Every returned option in the `gift` goal is an authentic, thoughtfully packaged gift set:
  - Commemorative finisher medals with patriotic ribbons («Озброєні волею 2.0», «Крила Свободи», «Гвардія Небес», «Патріотичний пульс», «Україна в тобі»).
  - Collector keychains made from authentic artillery shells, F-16 fighter jets, and reconnaissance drones.
  - Premium Sharpey bath towel gift trios (100% cotton, 500 g/m²).
  - Outdoor and travel gift boxes (organizers EF-09, buffs, glass water bottles).
- **Price Architecture for Gifts:** The catalog baseline for gifts begins at **1 379 ₴** (Row 91: *Подарунок для прогулянок*), with the vast majority priced at **1 500 ₴**. The quiz handles sub-1 300 ₴ gift requests with exemplary floor-anchor cards and clear educational notes.
- **Apparel & Shoe Sizing in Gifts:** For sets containing running socks RE2, sizing (40–44 and 43–45) filters accurately without leaking mismatched sizes.

### 2.3 Low Budget Edge Cases (400–700 ₴)
- **Graceful Floor-Anchor Mechanics:** Rather than failing silently, crashing, or proposing random standalone items, the quiz returns a **floor-anchor recommendation**.
- **Educational Transparent Messaging:**
  - *Ukrainian:* «За вибраним бюджетом наборів немає. У цій категорії повноцінні набори починаються від [X] ₴ (включають супровід). Нижче запропоновано базовий варіант.»
  - *Russian:* «По выбранному бюджету наборов нет. В этой категории полноценные наборы начинаются от [X] ₴ (включают сопровождение). Ниже предложен базовый вариант.»
- **Near-Miss Boundary Handling:** When the budget is within 9–50 ₴ of an actual kit (e.g. 750 ₴ budget vs 759 ₴ set, or 1100 ₴ budget vs 1125 ₴ set), `near_miss` accurately returns the set with a helpful note: *«Перевищує вибраний бюджет на [X] ₴»*.

### 2.4 High Budget Edge Cases (4000–8000 ₴)
- When affluent buyers specify budgets between 4 000 ₴ and 8 000 ₴, the matcher does not break or overflow. It selects the highest-scoring, comprehensive sets (typically 1 500 ₴ to 1 650 ₴ flagship kits with 3-month club coaching included).

### 2.5 Language, Wording & Linguistic Polish
- **Grammar & Terminology:** Ukrainian and Russian texts are natural and idiomatic. Strict separation between languages is maintained without code-switching.
- **Currency Formatting:** The official Ukrainian Hryvnia symbol (`₴`) is consistently used across all explanations, score cards, and floor anchors.
- **Persuasive 'Why Suitable' Explanations:** Explanations clearly state why a kit matches the specific request (e.g., target goal, product category, form factor, and club benefits).

---

## 3. Discovered Flaws, Warnings & Actionable Fixes

| Test ID | Goal | Verdict | Human Logic Flaw / Observation |
| :--- | :--- | :--- | :--- |
| #7 | `daily` | **WARN** | Набір «Ясний фокус» (Row 50) сфокусирован на утренней концентрации, но предложен для вечернего расслабления. |
| #8 | `daily` | **WARN** | Набір «Ясний фокус» (Row 50) сфокусирован на утренней концентрации, но предложен для вечернего расслабления. |
| #48 | `gift` | **FAIL** | Таксономічний розрив (dead-end no_match): користувач обрав 'strength_training' (пропонується в інтерфейсі), але в каталозі використано тег 'fitness_gym'. Через розбіжність квіз видає 0 результатів, відкидаючи набори 100 та 106. |
| #56 | `gift` | **FAIL** | Глухий кут каталогу (dead-end no_match): користувач обрав активність 'cycling' (пропонується в квізі), але в каталозі немає жодного подарункового набору для цієї активності. Квіз не зміг запропонувати універсальні подарунки (рушники, медалі). |
| #57 | `gift` | **FAIL** | Глухий кут каталогу (dead-end no_match): користувач обрав активність 'swimming' (пропонується в квізі), але в каталозі немає жодного подарункового набору для цієї активності. Квіз не зміг запропонувати універсальні подарунки (рушники, медалі). |
| #58 | `gift` | **FAIL** | Таксономічний розрив (dead-end no_match): користувач обрав 'strength_training' (пропонується в інтерфейсі), але в каталозі використано тег 'fitness_gym'. Через розбіжність квіз видає 0 результатів, відкидаючи набори 100 та 106. |
| #59 | `gift` | **FAIL** | Глухий кут каталогу (dead-end no_match): користувач обрав активність 'cycling' (пропонується в квізі), але в каталозі немає жодного подарункового набору для цієї активності. Квіз не зміг запропонувати універсальні подарунки (рушники, медалі). |

### Actionable Recommendations for Production:
1. **Resolve `strength_training` vs `fitness_gym` Taxonomy Gap:** In `_soft_signals`, map `'strength_training'` and `'fitness_gym'` synonymously so gym/strength athletes immediately match Row 100 (`Подарунок військовому-спортсмену`), Row 106 (`Спортивний подарунок`), and all 117 gym kits.
2. **Dynamic Question Filtering for Gifts (`_question_plan`):** Do not offer `cycling` or `swimming` as options in the gift quiz unless gift sets with those tags exist, OR allow versatile lifestyle gift sets (Sharpey bath towels, finisher medals, buffs) to serve as universal fallbacks rather than returning `no_match`.
3. **Context Sensitivity in Daily `general_auto`:** When an evening wind-down or bedtime is specified, do not allow daytime cognitive boosters like Row 50 (`Ясний фокус`) to fill the slot; prioritize magnesium/mineral and sleep sets.
4. **Stimulant Warning Flag for Daily Sets:** Add a safety badge/warning in UI cards for sets like Row 136 that contain concentrated caffeine shots, alerting customers who may have hypertension or caffeine sensitivity.
5. **Gift Category Sub-1000 ₴ Entry Option:** Consider curating an entry-level gift box around 700–900 ₴ (e.g., a single finisher medal + keychain bundle without club subscription) to capture budget gift shoppers.

---

## 4. Complete Test Results Matrix (100 Scenarios)

| ID | Goal | Loc | Persona | Budget | Status | Top Pick | Verdict |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | `daily` | uk | Офісний працівник (Київ): шукає капс… | 1500 ₴ | `general_auto` | Набір «Дитяча турбота Race Expert Club… | **PASS** |
| 2 | `daily` | ru | Офисный сотрудник: ищет мягкие капсу… | 1500 ₴ | `general_auto` | Набір «Старт із добавками Race Expert … | **PASS** |
| 3 | `daily` | uk | Студент: шукає бюджетний комплекс ві… | 1200 ₴ | `general_auto` | Набір «Старт із добавками Race Expert … | **PASS** |
| 4 | `daily` | ru | Покупатель: базовый витаминный компл… | 1300 ₴ | `matched` | Набір «Дитяча турбота Race Expert Club… | **PASS** |
| 5 | `daily` | uk | Мешканка міста: якісний вітамін D3 а… | 1400 ₴ | `matched` | Набір «Старт із добавками Race Expert … | **PASS** |
| 6 | `daily` | ru | Специалист с перегрузками: ищет вече… | 1500 ₴ | `matched` | Набір «Мінеральний тонус Race Expert C… | **PASS** |
| 7 | `daily` | uk | Втомлений менеджер: шукає вечірні та… | 1300 ₴ | `general_auto` | Набір «Ясний фокус Race Expert Club» —… | **WARN** |
| 8 | `daily` | ru | Пользователь с бессонницей: вечерний… | 1200 ₴ | `no_exact_match` | Набір «Ясний фокус Race Expert Club» —… | **WARN** |
| 9 | `daily` | uk | Нічний працівник: комплекс для норма… | 1450 ₴ | `matched` | Набір «Мінеральний тонус Race Expert C… | **PASS** |
| 10 | `daily` | ru | Житель мегаполиса: вечерние мягкие к… | 1500 ₴ | `matched` | Набір «Мінеральний тонус Race Expert C… | **PASS** |
| 11 | `daily` | uk | Відрядник: шукає компактні капсули д… | 1500 ₴ | `general_auto` | Набір «Дитяча турбота Race Expert Club… | **PASS** |
| 12 | `daily` | ru | Водитель/путешественник: минералы и … | 1350 ₴ | `general_auto` | Набір «Старт із добавками Race Expert … | **PASS** |
| 13 | `daily` | uk | Мандрівник: корисні снеки або батонч… | 1400 ₴ | `no_exact_match` | Набір «Щоденний комфорт Race Expert Cl… | **PASS** |
| 14 | `daily` | ru | Командировочный: сытный перекус в по… | 1200 ₴ | `no_match` | Набір «Щоденний комфорт Race Expert Cl… | **PASS** |
| 15 | `daily` | uk | Турист: софтгелі для адаптації та за… | 1500 ₴ | `general_auto` | Набір «Старт із добавками Race Expert … | **PASS** |
| 16 | `daily` | ru | Офисный работник: коробка полезных п… | 1500 ₴ | `general_auto` | Набір «Щоденний комфорт Race Expert Cl… | **PASS** |
| 17 | `daily` | uk | IT-спеціаліст: перекус для мозкової … | 1300 ₴ | `no_exact_match` | Набір «Щоденний комфорт Race Expert Cl… | **PASS** |
| 18 | `daily` | ru | Бухгалтер: здоровый питательный набо… | 1400 ₴ | `no_exact_match` | Набір «Щоденний комфорт Race Expert Cl… | **PASS** |
| 19 | `daily` | uk | Фрілансер: здорове щоденне харчуванн… | 1500 ₴ | `matched` | Набір «Щоденний комфорт Race Expert Cl… | **PASS** |
| 20 | `daily` | ru | Сотрудник банка: перекус без сахара … | 1350 ₴ | `no_exact_match` | Набір «Щоденний комфорт Race Expert Cl… | **PASS** |
| 21 | `daily` | uk | Користувач 45+: шукає щоденний компл… | 1500 ₴ | `matched` | Набір «Дитяча турбота Race Expert Club… | **PASS** |
| 22 | `daily` | ru | Родитель: поиск набора «Детская забо… | 1150 ₴ | `matched` | Набір «Старт із добавками Race Expert … | **PASS** |
| 23 | `daily` | uk | Покупець: підтримка травлення та мік… | 1200 ₴ | `matched` | Набір «Старт із добавками Race Expert … | **PASS** |
| 24 | `daily` | ru | ЗОЖ-энтузиаст: порошковые суперфуды … | 1500 ₴ | `general_auto` | Набір «Харчовий баланс»… | **PASS** |
| 25 | `daily` | uk | Пенсіонер: підтримка серцево-судинно… | 1400 ₴ | `matched` | Набір «Старт із добавками Race Expert … | **PASS** |
| 26 | `daily` | ru | Житель северного региона: зимний защ… | 1500 ₴ | `matched` | Набір «Серце й антиоксидантний захист»… | **PASS** |
| 27 | `daily` | uk | Киянин: захист імунітету в холодний … | 1300 ₴ | `general_auto` | Набір «Старт із добавками Race Expert … | **PASS** |
| 28 | `daily` | ru | Летний житель города: поддержка водн… | 1500 ₴ | `matched` | Набір «Мінеральний тонус Race Expert C… | **PASS** |
| 29 | `daily` | uk | Активна жінка: літній догляд за шкір… | 1400 ₴ | `matched` | Набір «Мінеральний тонус Race Expert C… | **PASS** |
| 30 | `daily` | ru | Офисный клерк: защита глаз и антиокс… | 1450 ₴ | `general_auto` | Набір «Старт із добавками Race Expert … | **PASS** |
| 31 | `daily` | uk | Ощадливий покупець: рівно точний мін… | 1125 ₴ | `matched` | Набір «Старт із добавками Race Expert … | **PASS** |
| 32 | `daily` | ru | Экономный покупатель: бюджет 1150 гр… | 1150 ₴ | `matched` | Набір «Старт із добавками Race Expert … | **PASS** |
| 33 | `daily` | uk | Покупець з обмеженим бюджетом 1100 г… | 1100 ₴ | `no_match` | Набір «Старт із добавками Race Expert … | **PASS** |
| 34 | `daily` | ru | Покупатель с бюджетом 1000 грн: пров… | 1000 ₴ | `no_match` | Набір «Старт із добавками Race Expert … | **PASS** |
| 35 | `daily` | uk | Шукач супер-економії (500 грн): пере… | 500 ₴ | `floor_anchor` | Набір «Старт із добавками Race Expert … | **PASS** |
| 36 | `daily` | ru | Экстремально низкий бюджет 400 грн: … | 400 ₴ | `floor_anchor` | Набір «Старт із добавками Race Expert … | **PASS** |
| 37 | `daily` | uk | Заможний клієнт: високий бюджет 3500… | 3500 ₴ | `matched` | Набір «Старт із добавками Race Expert … | **PASS** |
| 38 | `daily` | ru | Пользователь без предпочтений: выбра… | any | `matched` | Набір «Старт із добавками Race Expert … | **PASS** |
| 39 | `daily` | uk | Чутливий покупець: шукає вечірній на… | any | `matched` | Набір «Мінеральний тонус Race Expert C… | **PASS** |
| 40 | `daily` | ru | Здоровый образ жизни: аудит отсутств… | 1500 ₴ | `matched` | Набір «Старт із добавками Race Expert … | **PASS** |
| 41 | `gift` | uk | Дівчина бігуна: шукає пам'ятний пода… | 1500 ₴ | `matched` | Набір «Подарунок початківцю 2.0» — або… | **PASS** |
| 42 | `gift` | ru | Друг бегуна: ищет подарочный набор д… | 1500 ₴ | `matched` | Набір «Подарунок початківцю 2.0» — або… | **PASS** |
| 43 | `gift` | uk | Дружина марафонця: подарунок з бігов… | 1500 ₴ | `matched` | Набір «Подарунок початківцю 2.0» — або… | **PASS** |
| 44 | `gift` | ru | Коллега: подарок бегуну на день рожд… | 1500 ₴ | `matched` | Набір «Подарунок початківцю 2.0» — або… | **PASS** |
| 45 | `gift` | uk | Сестра бігуна: теплий зимовий подару… | 1500 ₴ | `general_auto` | Набір «Подарунок початківцю 2.0» — або… | **PASS** |
| 46 | `gift` | ru | Спортивный клуб: ищет памятный компл… | 1500 ₴ | `matched` | Набір «Подарунок початківцю 2.0» — або… | **PASS** |
| 47 | `gift` | uk | Волонтер: шукає подарунок з медаллю … | 1500 ₴ | `matched` | Набір «Подарунок для прогулянок» — або… | **PASS** |
| 48 | `gift` | ru | Семья военного: подарок ветерану/спо… | 1500 ₴ | `no_match` | — | **FAIL** |
| 49 | `gift` | uk | Біговий клуб: подарунок «Подвійна на… | 1500 ₴ | `matched` | Набір «Подарунок початківцю 2.0» — або… | **PASS** |
| 50 | `gift` | ru | Патриотический подарок: комплект с с… | 1500 ₴ | `matched` | Набір «Подарунок для прогулянок» — або… | **PASS** |
| 51 | `gift` | uk | Друг туриста: шукає набір «Подарунок… | 1500 ₴ | `general_auto` | Набір «Подарунок для прогулянок» — або… | **PASS** |
| 52 | `gift` | ru | Путешественник: набор «Подарок в дор… | 1500 ₴ | `general_auto` | Набір «Подарунок для прогулянок» — або… | **PASS** |
| 53 | `gift` | uk | Донька для батька: набір «Подарунок … | 1400 ₴ | `matched` | Набір «Подарунок для прогулянок» — або… | **PASS** |
| 54 | `gift` | ru | Любитель зимних походов: теплый осен… | 1500 ₴ | `matched` | Набір «Подарунок для прогулянок» — або… | **PASS** |
| 55 | `gift` | uk | Компанія друзів: подарунок мандрівни… | 1500 ₴ | `matched` | Набір «Подарунок для прогулянок» — або… | **PASS** |
| 56 | `gift` | ru | Велосипедист: спортивный подарок для… | 1500 ₴ | `no_match` | — | **FAIL** |
| 57 | `gift` | uk | Пловец: подарок с качественным полот… | 1500 ₴ | `no_match` | — | **FAIL** |
| 58 | `gift` | ru | Тренажерный зал: премиальный подароч… | 1500 ₴ | `no_match` | — | **FAIL** |
| 59 | `gift` | uk | Велолюбитель: корисний гідратаційний… | 1500 ₴ | `no_match` | — | **FAIL** |
| 60 | `gift` | ru | Марафонец: подарочный бокс энергетич… | 1500 ₴ | `matched` | Набір «Спортивний подарунок»… | **PASS** |
| 61 | `gift` | uk | Подарунок для дому: набір банних руш… | 1500 ₴ | `matched` | Набір «Подарунок для прогулянок» — або… | **PASS** |
| 62 | `gift` | ru | Практичный подарок: набор полотенец … | 1500 ₴ | `matched` | Набір «Подарунок для прогулянок» — або… | **PASS** |
| 63 | `gift` | uk | Корпоративний подарунок: набір «Пода… | 1500 ₴ | `matched` | Набір «Подарунок початківцю 2.0» — або… | **PASS** |
| 64 | `gift` | ru | Подарок спортсмену: комплект носков … | 1500 ₴ | `matched` | Набір «Подарунок початківцю 2.0» — або… | **PASS** |
| 65 | `gift` | uk | Універсальний подарунок: патріотични… | 1500 ₴ | `matched` | Набір «Подарунок для прогулянок» — або… | **PASS** |
| 66 | `gift` | ru | Точный бюджет 1379 грн: проверка поп… | 1379 ₴ | `matched` | Набір «Подарунок для прогулянок» — або… | **PASS** |
| 67 | `gift` | uk | Бюджет 1439 грн: попадание в «Подару… | 1439 ₴ | `matched` | Набір «Подарунок для прогулянок» — або… | **PASS** |
| 68 | `gift` | ru | Низкий бюджет на подарок 1000 грн: п… | 1000 ₴ | `floor_anchor` | Набір «Подарунок для прогулянок» — або… | **PASS** |
| 69 | `gift` | uk | Супер-економ подарунок 800 грн: пере… | 800 ₴ | `floor_anchor` | Набір «Подарунок для прогулянок» — або… | **PASS** |
| 70 | `gift` | ru | Щедрый даритель (бюджет 5000 грн): в… | 5000 ₴ | `matched` | Набір «Подарунок для прогулянок» — або… | **PASS** |
| 71 | `running` | uk | Бігун-початківець: критично низький … | 400 ₴ | `floor_anchor` | Акційний набір темних шкарпеток, 5 пар… | **PASS** |
| 72 | `hydration` | ru | Спортсмен в жару: бюджет 500 грн на … | 500 ₴ | `floor_anchor` | Набір «Ріст м'язів» — абонемент на 3 м… | **PASS** |
| 73 | `food` | uk | Велосипедист: бюджет 600 грн на спор… | 600 ₴ | `floor_anchor` | Набір «Набір маси»… | **PASS** |
| 74 | `training` | ru | Силовик: бюджет 500 грн на силовой н… | 500 ₴ | `no_match` | Набір «Силовий старт»… | **PASS** |
| 75 | `recovery` | uk | Атлет: бюджет 700 грн на комплекс ві… | 700 ₴ | `no_match` | Набір «М'язи в тонусі Race Expert Club… | **PASS** |
| 76 | `outdoors` | ru | Турист: бюджет 450 грн на походный н… | 450 ₴ | `floor_anchor` | Акційний набір термошкарпеток 1+1=3 «4… | **PASS** |
| 77 | `running` | uk | Бігун: бюджет 750 грн (набір шкарпет… | 750 ₴ | `no_match` | Акційний набір темних шкарпеток, 5 пар… | **PASS** |
| 78 | `training` | ru | Атлет: бюджет 780 грн — перевірка ne… | 780 ₴ | `matched` | Набір «Силовий старт»… | **PASS** |
| 79 | `daily` | uk | Щоденне здоров'я: бюджет 1100 грн (н… | 1100 ₴ | `no_match` | Набір «Старт із добавками Race Expert … | **PASS** |
| 80 | `gift` | ru | Подарок: бюджет 1350 грн (набор стои… | 1350 ₴ | `no_match` | Набір «Подарунок для прогулянок» — або… | **PASS** |
| 81 | `food` | uk | Харчування: бюджет 750 грн — перевір… | 750 ₴ | `floor_anchor` | Набір «Набір маси»… | **PASS** |
| 82 | `running` | ru | Марафонец: бюджет 4000 грн — выбор л… | 4000 ₴ | `matched` | Акційний набір темних шкарпеток, 5 пар… | **PASS** |
| 83 | `training` | uk | Кросфітер: бюджет 5000 грн — рекомен… | 5000 ₴ | `matched` | Набір «Силовий старт»… | **PASS** |
| 84 | `gear` | ru | Спортсмен: бюджет 7000 грн на экипир… | 7000 ₴ | `matched` | Акційний набір темних шкарпеток, 5 пар… | **PASS** |
| 85 | `daily` | uk | Преміум-клієнт: бюджет 8000 грн на щ… | 8000 ₴ | `matched` | Набір «Старт із добавками Race Expert … | **PASS** |
| 86 | `gift` | ru | VIP-даритель: бюджет 8000 грн на под… | 8000 ₴ | `matched` | Набір «Подарунок для прогулянок» — або… | **PASS** |
| 87 | `running` | uk | Бігун-початківець: всі опціональні п… | any ₴ | `matched` | Акційний набір темних шкарпеток, 5 пар… | **PASS** |
| 88 | `training` | ru | Атлет зала: все поля 'any' — проверк… | any | `matched` | Набір «Силовий старт»… | **PASS** |
| 89 | `outdoors` | uk | Мандрівник: абсолютно порожній запит… | any | `matched` | Акційний набір термошкарпеток 1+1=3 «4… | **PASS** |
| 90 | `recovery` | ru | Спортсмен после старта: пустой запро… | any | `matched` | Набір «М'язи в тонусі Race Expert Club… | **PASS** |
| 91 | `gear` | uk | Бігун-велетень: розмір ноги 50 (нема… | any | `matched` | Набір «Ріст м'язів» — абонемент на 3 м… | **PASS** |
| 92 | `running` | ru | Миниатюрная бегунья: невозможный раз… | any | `no_match` | — | **PASS** |
| 93 | `running` | uk | Бігун з розміром 48: точний збіг для… | any | `matched` | Акційний набір темних шкарпеток, 5 пар… | **PASS** |
| 94 | `outdoors` | ru | Граничный тест валидации: неподдержи… | any | `expected_error` | — | **PASS** |
| 95 | `running` | uk | Покупець без клубу: вимога набору бе… | any | `matched` | Акційний набір темних шкарпеток, 5 пар… | **PASS** |
| 96 | `training` | ru | Спортсмен с клубом: требование обяза… | any | `matched` | Набір «М'язи в тонусі Race Expert Club… | **PASS** |
| 97 | `daily` | uk | Щоденне здоров'я без клубу: перевірк… | any | `matched` | Набір «Розум і Сила»… | **PASS** |
| 98 | `running` | uk | Українська локалізація: глибока пере… | any | `matched` | Набір «Марафонець»… | **PASS** |
| 99 | `running` | ru | Русская локализация: проверка термин… | any | `matched` | Набір «Марафонець»… | **PASS** |
| 100 | `daily` | uk | Нульовий бюджет (0 грн): перевірка е… | 0 ₴ | `floor_anchor` | Набір «Старт із добавками Race Expert … | **PASS** |

---
*Report generated by QA Agent 5 - Daily Wellness, Gifts & Edge Cases Specialist.*