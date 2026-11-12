# Human-Centric Question Matrix: Athletic, Equipment & Lifestyle Categories
**Race Expert AI Quiz Engine Architecture**  
**Role:** Head Athletic Coach & Equipment Specialist  
**Basis:** 600 Buyer Stress Tests across 207 Real Catalog Sets (`curated_207_audit.json`)  
**Status:** Approved for Core Matcher & Frontend Migration  

---

## 1. Executive Athletic Coaching Manifesto

The 600 automated stress tests revealed a severe disconnect between programmatic code taxonomy (`component_class`, `candidate_tier`, unmapped enums) and **real athletic physiology, equipment fit, and human buyer intent**. 

When an athlete, runner, hiker, or fitness enthusiast arrives at Race Expert, they do not think in database schemas. They think in terms of **their race distance, their body's hydration needs, their shoe size, their recovery state, or their gift recipient**.

### Key Athletic Principles Enforced in this Matrix:
1. **Total Isolation of Aerobic Endurance vs Anaerobic Hypertrophy:**  
   Under no circumstances shall a 500g bodybuilding creatine monohydrate tub or mass gainer be recommended to an endurance half-marathon or marathon runner. Creatine causes intracellular water retention, adding 1–2 kg of dead weight penalty during 21.1–42.2 km running, increasing oxygen consumption per kilometer without aerobic benefit.
2. **Elimination of Deceptive Justifications:**  
   The system must never claim *«у наборі саме Спортивне харчування (без сторонніх речей)»* when the kit contains 70% non-food items (e.g., bath towels, club subscriptions, or socks). Explanations must be 100% transparent and truthful.
3. **End of Sizing Roulette:**  
   Running socks and apparel must never default to an arbitrary size (such as giant 46–48). The quiz must explicitly capture shoe size (`35–37`, `38–40`, `40–42`, `43–45`, `46–48`) or route the buyer to size-free gear (bib belts, flasks, massage rollers, towels).
4. **Rescuing the ЇDLO Camping Rations & Salt Capsules:**  
   Dehydrated camping meals (ЇDLO) and salt capsules (Precision Hydration) must be first-class citizens in Outdoors and Hydration flows, fixing the zero-result dead ends discovered in QA Agent 4.
5. **No Phantom Sports Categories:**  
   Remove dead-end sports like swimming or gymnastics from the user options, as the Race Expert catalog has zero swimming gear.

---

## 2. Category 1: «Біг та підготовка до стартів» (Running & Race Preparation)

### 2.1 Athletic Coach Diagnosis (Post-600 Test Analysis)
- **The Half-Marathon Catastrophe:** Half-marathon (21.1 km) is Ukraine's most popular mass race distance. In previous tests, selecting half-marathon caused `status: no_exact_match` for 100% of runners because the code looked for a strict `half_marathon` tag that was absent in the raw database.
- **Creatine Contamination:** Set `RE11660` («Марафонець») bundled 5 gels with a 300g creatine tub and pitched *«мышечный рост и взрывная сила»* to marathoners.
- **Catalog Grounding:** In the 207-set catalog, endurance nutrition is concentrated in `UT-PRO-2026`, `RE11659`, and `RE11660`, while gear/hydration is in `RE11804`, `RE11799`, `RE11650`, and `Nabir_1123`.

---

### 2.2 Question Flow (UA & RU)

#### **Питання 1 (Дистанція та фокус тренувань) / Вопрос 1 (Дистанция и фокус)**
*«До якої дистанції або формату бігу ви готуєтесь?»* / *«К какой дистанции или формату бега вы готовитесь?»*

| Ключ / Option ID | Текст варіанту (UA) | Текст варианта (RU) | Пояснювальний підтекст для покупця |
|---|---|---|---|
| `run_short_5_10k` | **5–10 км / Регулярні proбіжки для здоров'я** | **5–10 км / Регулярные пробежки для здоровья** | Підтримка форми, легкі тренування, базовий комфорт стопи та легка гідратація. |
| `run_half_marathon` | **Півмарафон (21.1 км) / Темпові старти** | **Полумарафон (21.1 км) / Темповые старты** | Робота на результат, обов'язкове живлення на дистанції (гелі) та стартова екіпіровка. |
| `run_marathon_trail` | **Марафон (42.2 км) / Ультратрейл** | **Марафон (42.2 км) / Ультратрейл** | Максимальна автономність: енергетичні гелі тривалої дії, сольовий баланс, пояс для номерів. |
| `run_heat_cramps` | **Біг у спеку / Захист від судоми та зневоднення** | **Бег в жару / Защита от судорог и обезвоживания** | Концентровані сольові капсули, електроліти високої мінералізації для рясного потовиділення. |

---

#### **Питання 2 (Пріоритет потреби) / Вопрос 2 (Приоритет потребности)**
*«Що саме є найголовнішим для вашого забігу?»* / *«Что именно важнее всего для вашего забега?»*

| Ключ / Option ID | Текст варіанту (UA) | Текст варианта (RU) | Пояснювальний підтекст для покупця |
|---|---|---|---|
| `need_nutrition_energy` | **Енергія на дистанції (гелі, батончики, жуйки)** | **Энергия на дистанции (гели, батончики, жевательные конфеты)** | Вуглеводне паливо для підтримки темпу без розладу шлунка (SIS Beta Fuel, PF 30, Sponser). |
| `need_hydration_salts` | **Гідратація та мінерали (електроліти, ізотоніки, сіль)** | **Гидратация и минералы (электролиты, изотоники, соль)** | Відновлення солей натрію, калію та магнію під час тривалого бігу (Hydria, Precision Hydration). |
| `need_race_gear` | **Стартове спорядження (пояс для номера, пляшка, кепка)** | **Стартовая экипировка (пояс для номера, бутылка, кепка)** | Зручна фіксація стартового номера без шпильок, петлі під гелі, захист від сонця. |
| `need_running_socks` | **Спеціальні бігові або компресійні шкарпетки** | **Специальные беговые или компрессионные носки** | Зональна підтримка ахілла та стопи, вентиляційні канали, профілактика мозолів. |

---

#### **Питання 3 (Формат набору та бюджет) / Вопрос 3 (Формат набора и бюджет)**
*«Який формат комплекту вам підходить?»* / *«Какой формат комплекта вам подходит?»*

| Ключ / Option ID | Текст варіанту (UA) | Текст варианта (RU) | Пояснювальний підтекст для покупця |
|---|---|---|---|
| `format_essential` | **Тільки необхідне спорядження/харчування (950–1250 ₴)** | **Только необходимое снаряжение/питание (950–1250 ₴)** | Конкретний цільовий набір без абонементів та супутніх послуг. |
| `format_pro_club` | **PRO-комплект із тренерським супроводом Race Expert Club (1400–1650 ₴)** | **PRO-комплект с тренерским сопровождением Race Expert Club (1400–1650 ₴)** | Топовий набір + 3 місяці доступу до бігової спільноти, порад тренерів та щотижневих планів. |

---

### 2.3 Grounded Catalog SKU Mapping (207 Sets)

- **Для напівмарафону та марафону (Енергія + Гідратація PRO):**
  - `UT-PRO-2026` (1 650 ₴) — Набір «Ultra Trail Marathon Energy & Hydration Pro»: 3x SIS Beta Fuel гелі, 2x SIS Go Hydro електроліти, протеїновий батончик Science in Sport.
  - `RE11659` (1 200 ₴) — Набір «Тиждень бігуна»: протеїнові батончики Sponser Crunchy, 6 стиків електролітів Hydria Perform, енергетичні жуйки GU Energy Chews.
  - `RE11660` (1 500 ₴) — Набір «Марафонець»: 5x PF 30 Energy Gels (51 г) *(з приміткою про використання креатину лише в силовий період підготовки)*.
- **Для захисту від судом та спеки (Гідратація та солі):**
  - `RE11650` (1 239 ₴) — Набір «Захист від спеки»: туба Precision Hydration 1000 (10 таблеток) + 15 капсул Precision Fuel & Hydration з високим вмістом електролітів.
  - `Nabir_1123` (1 435 ₴) — Набір «Комплект для гідратації Race Expert Club»: 16 стиків Hydria Perform + бігова спортивна пляшка + клубний доступ.
  - `Nabir_1015` (1 500 ₴) — Набір «Електролітний запас»: 20 стиків гідратації Hydria Perform.
- **Для стартового дня (Екіпірування):**
  - `RE11804` (1 500 ₴) — Набір «Марафонський темп»: стартовий біговий пояс Race Expert із 6 еластичними петлями для гелів + бігова кепка «Run for Help Ukraine» + 10 стиків електролітів Hydria.
  - `RE11799` (1 500 ₴) — Набір «Підготовка до забігу»: бігова кепка + пояс для стартового номера + пляшка для води 600 мл + білі шкарпетки.
  - `RE11020` (1 209 ₴) — Набір «Бігова екіпіровка»: 2 пари шкарпеток RE2 + скляна бігова пляшка 530 мл + еластичні шнурки зі швидким фіксатором + протеїнові батончики.

---

### 2.4 Strict Athletic Guardrails (Negative Constraints)
> [!CAUTION]
> 1. **Zero Creatine Overdose:** NEVER recommend sets `RE11522` («Чиста сила»), `RE88934` («Регулярний зал»), `RE11636` («Вибух сили»), `RE11680` («Силовий старт») runners requesting running endurance or marathon prep.
> 2. **No Deceptive Food Guarantees:** Do not generate claims that a set contains *«лише харчування без сторонніх речей»* for `RE11660` or `RE11020` where bottles, laces, or creatine make up significant volume.
> 3. **Half-Marathon Fallback:** Any query selecting `run_half_marathon` MUST automatically inherit candidates from marathon and endurance stamina categories.

---

## 3. Category 2: «Силові тренування та зал» (Gym Fitness & Strength)

### 3.1 Athletic Coach Diagnosis (Post-600 Test Analysis)
- **The Core Activity Disconnect:** 35% of strength tests in Agent 3 failed because `draft_matcher.py` strictly searched for `strength_training` in set taxonomy, whereas the catalog exclusively used `fitness_gym`.
- **False Creatine Labeling:** Kits containing only mushroom cookies (`RE11632`), yoga mats (`RE11663`), jump ropes (`RE11665`), or bath towels (`RE89489`) were flagged in code as `creatine_preworkout`.
- **Missed Budget Gems:** `RE11680` («Силовий старт», 759 ₴) contains 300g pure Miami Vibes Creatine Monohydrate + D3, yet lacked the creatine class tag, causing 100% of sub-1000 ₴ strength queries to return zero results.

---

### 3.2 Question Flow (UA & RU)

#### **Питання 1 (Головна мета у залі) / Вопрос 1 (Главная цель в зале)**
*«Яка ваша головна мета тренувань у залі?»* / *«Какова ваша главная цель тренировок в зале?»*

| Ключ / Option ID | Текст варіанту (UA) | Текст варианта (RU) | Пояснювальний підтекст для покупця |
|---|---|---|---|
| `gym_mass_power` | **Ріст м'язової маси та приріст сили** | **Рост мышечной массы и прирост силы** | Базовий моногідрат креатину для синтезу АТФ, збільшення робочої ваги, відновлення після важких підходів. |
| `gym_drive_energy` | **Передтренувальний драйв, тонус та фокус** | **Предтренировочный драйв, тонус и фокус** | Кофеїн, L-карнітин, предтренувальні комплекси та вітаміни групи B для максимальної концентрації. |
| `gym_muscle_recovery` | **Швидке відновлення м'язів та захист від катаболізму** | **Быстрое восстановление мышц и защита от катаболизма** | Комплекси BCAA, глютамін, сироватковий протеїн для зняття болю в м'язах (кріпатури). |
| `gym_functional_gear` | **Функціональний інвентар для залу та дому** | **Функциональный инвентарь для зала и дома** | Скакалки зі лічильником, еспандери різного опору, подвійні ролики для преса, шейкери та рушники. |

---

#### **Питання 2 (Бажані компоненти) / Вопрос 2 (Предпочитаемые компоненты)**
*«Що обов'язково має входити у ваш комплект?»* / *«Что обязательно должно входить в ваш комплект?»*

| Ключ / Option ID | Текст варіанту (UA) | Текст варианта (RU) | Пояснювальний підтекст для покупця |
|---|---|---|---|
| `comp_creatine_base` | **Банка чистого креатину моногідрату (300–500 г)** | **Банка чистого креатина моногидрата (300–500 г)** | Золотий стандарт перевіреного приросту сили та гідратації м'язових волокон. |
| `comp_amino_protein` | **Амінокислоти BCAA / Глютамін / Протеїн** | **Аминокислоты BCAA / Глютамин / Протеин** | Чистий будівельний матеріал для м'язів без зайвих калорій чи цукру. |
| `comp_preworkout_stims` | **Передтренувальний тонік або L-карнітин** | **Предтренировочный тоник или L-карнитин** | Швидкий приплив енергії перед важким тренуванням або кардіо-сесією. |
| `comp_accessories_only` | **Спортивні аксесуари (рушник, шейкер, інвентар)** | **Спортивные аксессуары (полотенце, шейкер, инвентарь)** | Чиста екіпіровка без добавок та порошків. |

---

#### **Питання 3 (Бюджетний орієнтир) / Вопрос 3 (Бюджетный ориентир)**
*«На який бюджет ви розраховуєте?»* / *«На какой бюджет вы рассчитываете?»*

| Ключ / Option ID | Текст варіанту (UA) | Текст варианта (RU) | Пояснювальний підтекст для покупця |
|---|---|---|---|
| `budget_entry_gym` | **До 1 000 ₴ (Базовий робочий старт)** | **До 1 000 ₴ (Базовый рабочий старт)** | Доступні набори з креатином або BCAA без зайвих переплат. |
| `budget_standard_gym` | **1 000 – 1 400 ₴ (Повноцінний тренувальний комплекс)** | **1 000 – 1 400 ₴ (Полноценный тренировочный комплекс)** | Креатин 500 г + батончики, Омега-3 або фірмові шейкери. |
| `budget_premium_gym` | **1 400 – 1 650 ₴ (Топовий набір + супровід тренера)** | **1 400 – 1 650 ₴ (Топовый набор + сопровождение тренера)** | Флагманські бренди + 3 місяці клубного тренінгу Race Expert Club. |

---

### 3.3 Grounded Catalog SKU Mapping (207 Sets)

- **М'язова маса та приріст сили (Креатин моногідрат):**
  - `RE11680` (759 ₴) — Набір «Силовий старт»: чистий креатин моногідрат Miami Vibes Pure 300 г + вітамін NOW D3 2000 IU + протеїнові снеки.
  - `RE11742` (1 295 ₴) — Набір «Спортивний фундамент 2.0»: 500 г креатину Bodyperson Labs + NOW D3 + NOW Omega-3 (60 капсул).
  - `RE11637` (1 275 ₴) — Набір «Сила + паливо»: 500 г креатину Bodyperson Labs + хрусткі протеїнові батончики Sponser.
  - `RE11522` (1 399 ₴) — Набір «Чиста сила Race Expert Club»: 500 г топового креатину Myprotein Creatine Monohydrate + фірмовий шейкер + 3 місяці клубу.
  - `RE11800` (1 500 ₴) — Набір «Запас сили»: чистий мікронізований німецький креатин Nutriversum Creapure 500 г + шейкер.
  - `RE88934` (1 449 ₴) — Набір «Регулярний зал»: креатин OstroVit 500 г + щоденні мультивітаміни NOW Daily Vits + клуб.
- **Передтренувальний тонус та драйв:**
  - `RE11636` (1 385 ₴) — Набір «Вибух сили»: креатин 500 г + передтренувальний стимулюючий комплекс Bodyperson Formula.
  - `RE88963` (1 500 ₴) — Набір «Передтренувальний тонус»: концентрат VPLab L-Carnitine Concentrate 500 мл + шейкер + клуб.
- **Відновлення м'язів (BCAA, Глютамін, Протеїн):**
  - `Nabir_1118` (1 500 ₴) — Набір «Міцна основа 2.0»: якісний європейський сироватковий протеїн Nutrend 100% Whey Protein 400 г + шейкер Myprotein 600 мл + батончик.
  - `RE11796` (985 ₴) — Набір «М'язи в тонусі»: порошок Nutriversum BCAA + Gluta без цукру 500 г + міні-шейкер.
  - `RE11811` (1 500 ₴) — Набір «М'язове відновлення»: амінокислотний комплекс BCAA + Gluta 500 г.
  - `RE11786` (1 285 ₴) — Набір «Тренувальний ресурс»: BCAA 2:1:1 Sugar Free 360 г + клуб.
- **Інвентар для залу, кросфіту та фітнесу:**
  - `RE11664` (1 500 ₴) — Набір «Домашній фітнес та тонус»: швидкісна скакалка EasyFit + міцні текстильні тканинні еспандери EasyFit HARD/MEDIUM.
  - `RE11665` (1 500 ₴) — Набір «Активний рух»: швидкісна скакалка зі вбудованим лічильником обертів + подвійний ролик для преса + еспандер.
  - `RE89452` (1 500 ₴) — Набір «Підготовка до тренувань у залі»: великий бавовняний рушник для тренажерів 135х70 см + шейкер 600 мл + клуб.

---

### 3.4 Strict Athletic Guardrails (Negative Constraints)
> [!CAUTION]
> 1. **Zero Endurance Gel Spillover:** NEVER recommend pure running carb gels (PF 30 Gel, SIS Beta Fuel) to a strength athlete looking for powerlifting progress or hypertrophy.
> 2. **No False Creatine Tagging:** Yoga mats (`RE11663`), jump ropes (`RE11664`), bath towels (`RE89489`), and Lion's Mane mushroom cookies (`RE11632`) MUST be completely stripped of any `creatine_preworkout` tags.
> 3. **Fix the Taxonomy Link:** The matcher MUST treat `strength_training`, `powerlifting`, `crossfit`, and `fitness_gym` as fully compatible synonyms.

---

## 4. Category 3: «Екіпірування та аксесуари» (Gear & Accessories)

### 4.1 Athletic Coach Diagnosis (Post-600 Test Analysis)
- **The Creatine Parasite Bug:** 29 out of 100 gear tests in Agent 6 were failed because 500g bodybuilding creatine tubs (`Nabir_1121`, `RE89488`, `RE88961`) were tagged as `foot_apparel_comfort` and offered to buyers looking for running accessories!
- **Sizing Breakdown:** The quiz had no dedicated shoe size prompt for socks, resulting in users with size 36 being recommended size 46–48 socks.
- **The Swimming Ghost:** The previous quiz offered swimming options even though Race Expert stocks zero goggles, swim caps, or trunks.

---

### 4.2 Question Flow (UA & RU)

#### **Питання 1 (Тип екіпірування) / Вопрос 1 (Тип экипировки)**
*«Яка саме екіпіровка або аксесуар вам потрібні?»* / *«Какая именно экипировка или аксессуар вам необходимы?»*

| Ключ / Option ID | Текст варіанту (UA) | Текст варианта (RU) | Пояснювальний підтекст для покупця |
|---|---|---|---|
| `gear_running_socks` | **Спортивні шкарпетки для бігу та фітнесу (набори по 5 пар)** | **Спортивные носки для бега и фитнеса (наборы по 5 пар)** | Вентильовані анатомічні моделі з посиленим миском і п'ятою, що не зсуваються. |
| `gear_thermal_socks` | **Теплі зимові термошкарпетки (акція 1+1=3)** | **Теплые зимние термоноски (акция 1+1=3)** | Збереження сухого тепла, вологовідведення для пробіжок у мороз та трекінгу. |
| `gear_race_essentials` | **Бігові аксесуари (пояс для номера, пляшка, кепка, шнурки)** | **Беговые аксессуары (пояс для номера, бутылка, кепка, шнурки)** | Спеціалізоване спорядження для комфортних тренувань і офіційних стартів. |
| `gear_mfr_recovery` | **Інвентар для самомасажу, спини та МФР (ролики, м'ячі)** | **Инвентарь для самомассажа, спины и МФР (ролики, мячи)** | Зняття гіпертонусу м'язів, тригерних точок і відновлення рухливості зв'язок. |
| `gear_gym_towels` | **Банні рушники для тренувань та душу (набори по 3 шт)** | **Банные полотенца для тренировок и душа (наборы по 3 шт)** | Щільна 100% бавовна 500 г/м², розмір 135х70 см для залу, басейну чи дому. |

---

#### **Питання 2 (Точний розмір взуття — обов'язково для шкарпеток) / Вопрос 2 (Размер обуви)**
*«Оберіть ваш розмір взуття (для підбору шкарпеток):»* / *«Выберите ваш размер обуви (для подбора носков):»*

| Ключ / Option ID | Текст варіанту (UA) | Текст варианта (RU) | Доступні варіанти в каталозі |
|---|---|---|---|
| `size_35_37` | **35–37 (Жіночий / Підлітковий)** | **35–37 (Женский / Подростковый)** | Білі (5 пар), Темні (5 пар), Термо 1+1=3 (3 пари) |
| `size_38_40` | **38–40 (Середній розмір)** | **38–40 (Средний размер)** | Білі (5 пар), Темні (5 пар), Термо 1+1=3 (3 пари) |
| `size_40_42` | **40–42 (Популярний чоловічий / жіночий)** | **40–42 (Популярный размер)** | Білі (5 пар), Темні (5 пар), Термо 1+1=3 (3 пари) |
| `size_43_45` | **43–45 (Великий розмір)** | **43–45 (Большой размер)** | Білі (5 пар), Темні (5 пар), Термо 1+1=3 (3 пари) |
| `size_46_48` | **46–48 (Максі розмір для високих атлетів)** | **46–48 (Макси размер)** | Білі (5 пар), Темні (5 пар) |
| `size_not_needed` | **Розмір не потрібен (шукаю пояс, пляшку, рушник, ролик)** | **Размер не нужен (ищу пояс, бутылку, полотенце, ролик)** | Перехід до категорії аксесуарів без шкарпеток |

---

#### **Питання 3 (Колір / Комплектація) / Вопрос 3 (Цвет / Комплектация)**
*«Якому кольору або комплектації ви надаєте перевагу?»* / *«Какой цвет или комплектацию вы предпочитаете?»*

| Ключ / Option ID | Текст варіанту (UA) | Текст варианта (RU) | Пояснювальний підтекст |
|---|---|---|---|
| `style_white_socks` | **Класичний білий колір (White Sport Edition)** | **Классический белый цвет (White Sport Edition)** | Упаковка 5 пар білих дихаючих спортивних шкарпеток Race Expert. |
| `style_dark_socks` | **Практичний чорний / темний колір (Dark Edition)** | **Практичный черный / темный цвет (Dark Edition)** | Упаковка 5 пар темних зносостійких шкарпеток. |
| `style_mix_accessories` | **Комбінований набір (аксесуари + шкарпетки)** | **Комбинированный набор (аксессуары + носки)** | Пояс для номера, пляшка або кепка разом зі спортивними шкарпетками. |

---

### 4.3 Grounded Catalog SKU Mapping (207 Sets)

- **Спортивні шкарпетки за точними розмірами (5 пар за 950 ₴):**
  - **Розмір 35–37:** `RE11777` (Темні 5 пар), `RE89630` (Білі 5 пар).
  - **Розмір 38–40:** `RE11778` (Темні 5 пар), `RE11775` (Білі 5 пар).
  - **Розмір 40–42:** `RE11779` (Темні 5 пар), `RE11776` (Білі 5 пар).
  - **Розмір 43–45:** `RE11022` (Темні 5 пар), `RE11023` (Білі 5 пар).
  - **Розмір 46–48:** `RE89632` (Темні 5 пар), `RE89631` (Білі 5 пар).
- **Зимові термошкарпетки (Акція 1+1=3 за 1 058 ₴):**
  - **Розмір 35–37:** `RE89634` (3 пари термошкарпеток).
  - **Розмір 38–40:** `RE89635` (3 пари термошкарпеток).
  - **Розмір 40–42:** `RE89636` (3 пари термошкарпеток).
  - **Розмір 43–45:** `RE89637` (3 пари термошкарпеток).
- **Бігові аксесуари (пояси, пляшки, кепки, шнурки):**
  - `RE11799` (1 500 ₴) — Набір «Підготовка до забігу»: бігова кепка + пояс для стартового номера + спортивна пляшка 600 мл + шкарпетки 40–42.
  - `RE11804` (1 500 ₴) — Набір «Марафонський темп»: стартовий пояс із 6 петлями під гелі + кепка + 10 стиків електролітів Hydria.
  - `RE11020` (1 209 ₴) — Набір «Бігова екіпіровка»: скляна пляшка Race Expert 530 мл + чорні еластичні бігові шнурки зі швидкими фіксаторами + 2 пари шкарпеток + протеїнові батончики.
  - `RE11021` (1 379 ₴) — Набір «Літній старт»: скляна пляшка + 2 пари шкарпеток + клуб.
- **МФР та відновлення (Ролики та масаж):**
  - `RE11662` (1 500 ₴) — Набір «Релакс та відновлення»: професійний масажний валик EasyFit Grid Roller 45 см + твердий PVC точковий масажний м'яч для глибокого опрацювання м'язів.
- **Банні рушники (3 штуки 135х70 см, 1 500 ₴):**
  - `RE89487` — Набір «Банні рушники Шарпей: темна гама» (чорний, темно-синій, пляшково-зелений).
  - `RE89486` — Набір «Банні рушники Шарпей: класика» (бежевий, бордовий, сірий).

---

### 4.4 Strict Athletic Guardrails (Negative Constraints)
> [!CAUTION]
> 1. **Zero Creatine in Gear:** HARD BLOCK on recommending any set with Creatine Monohydrate (`Nabir_1121`, `RE89488`, `RE88961`, `race-expert-040`) to a buyer asking for socks, belts, or rollers.
> 2. **No Swimming Dead Ends:** Delete `swimming` from all category options.
> 3. **Strict Size Guard:** If size 35–37 is chosen, NEVER return size 46–48. If size is unspecified, the quiz MUST prompt for shoe size before finalizing socks.

---

## 5. Category 4: «Походи, кемпінг та трекінг» (Outdoors & Hiking)

### 5.1 Athletic Coach Diagnosis (Post-600 Test Analysis)
- **The ЇDLO Blindspot (100% Failure Rate in Agent 4):** Customers searching for dehydrated camp meals received `status: no_match` because ЇDLO sets (`RE11494`, `RE11495`, `RE88977`) were wrongly filed under `protein_carbohydrate_food` instead of camping food rations.
- **Hydration Invasions:** Spirulina pills (`RE11513`), Lion's Mane mushrooms (`RE88943`), and OstroVit Creatine (`RE11636`) leaked into hiking hydration queries.
- **Artificial Walls on Walking:** Nordic walkers and hikers walking 15–25 km were rejected from selecting portable snacks or electrolytes.

---

### 5.2 Question Flow (UA & RU)

#### **Питання 1 (Формат аутдор-активності) / Вопрос 1 (Формат аутдор-активности)**
*«Який формат походу або активності на природі ви плануєте?»* / *«Какой формат похода или активности на природе вы планируете?»*

| Ключ / Option ID | Текст варіанту (UA) | Текст варианта (RU) | Пояснювальний підтекст для покупця |
|---|---|---|---|
| `outdoor_trekking_multi` | **Багатоденний піший похід / Автономний трекінг** | **Многодневный пеший поход / Автономный треккинг** | Потреба в гарячій похідній їжі швидкого запарювання, високій калорійності та термошкарпетках. |
| `outdoor_hiking_day` | **Одноденний хайкінг / Скандинавська ходьба** | **Однодневный хайкинг / Скандинавская ходьба** | Зручні м'ясні снеки для швидкого перекусу на стежці, вода та захист ніг від натертостей. |
| `outdoor_trail_running` | **Гірський трейл або швидкісний перехід (Fastpacking)** | **Горный трейл или скоростной переход (Fastpacking)** | Максимальна легкість: концентровані гелі SIS Beta Fuel, таблетки гідратації, сольовий баланс. |
| `outdoor_tactical_field` | **Польові або військові автономні умови** | **Полевые или военные автономные условия** | Довготривале зберігання, сублімати ЇDLO, поживні м'ясні джерки та теплі надійні шкарпетки. |

---

#### **Питання 2 (Головний пріоритет спорядження) / Вопрос 2 (Главный приоритет)**
*«Що найважливіше підібрати для вашої подорожі?»* / *«Что важнее всего подобрать для вашего путешествия?»*

| Ключ / Option ID | Текст варіанту (UA) | Текст варианта (RU) | Пояснювальний підтекст для покупця |
|---|---|---|---|
| `camp_hot_meals_idlo` | **Похідна гаряча їжа швидкого запарювання (раціони ЇDLO)** | **Походная горячая еда быстрого приготовления (рационы ЇDLO)** | Повноцінні сублімовані страви (каші, супи, м'ясо), які запарюються окропом прямо в пакеті. |
| `camp_meat_jerky` | **Поживні м'ясні снеки та джерки (М'яско ToGo)** | **Питательные мясные снеки и джерки (М'яско ToGo)** | 100% сушене добірне м'ясо курки, індички або свинини для ситного білкового перекусу на ходу. |
| `camp_thermal_socks` | **Термошкарпетки для захисту стопи від холоду та вологи** | **Термоноски для защиты стопы от холода и влаги** | Зональне махрове плетіння, потовщена підошва для амортизації під вагою рюкзака. |
| `camp_trail_hydration` | **Енергія та електроліти для тривалих гірських переходів** | **Энергия и электролиты для длительных горных переходов** | Профілактика зневоднення на підйомах, ізотонічні розчини та швидкі вуглеводи. |

---

#### **Питання 3 (Розмір ноги для термошкарпеток) / Вопрос 3 (Размер ноги)**
*«Якщо ви обираєте термошкарпетки, який ваш розмір?»* / *«Если выбираете термоноски, какой ваш размер?»*

| Ключ / Option ID | Текст варіанту (UA) | Текст варианта (RU) |
|---|---|---|
| `outdoor_size_35_37` | **35–37 (Жіночий / Підлітковий)** | **35–37 (Женский / Подростковый)** |
| `outdoor_size_38_40` | **38–40 (Середній розмір)** | **38–40 (Средний размер)** |
| `outdoor_size_40_42` | **40–42 (Стандартний)** | **40–42 (Стандартный)** |
| `outdoor_size_43_45` | **43–45 (Великий розмір)** | **43–45 (Большой размер)** |
| `outdoor_meals_only` | **Мене цікавить тільки їжа / снеки (без шкарпеток)** | **Меня интересует только еда / снеки (без носков)** |

---

### 5.3 Grounded Catalog SKU Mapping (207 Sets)

- **Гаряча сублімована їжа для походів (ЇDLO):**
  - `RE11494` (1 500 ₴) — Набір «Похідна їжа ЇDLO 2.0»: фірмові пакети сублімованих других страв та сніданків ЇDLO для автономного харчування.
  - `RE11495` (1 500 ₴) — Набір «Похідна їжа ЇDLO Race Expert Club»: раціони ЇDLO + супровід та консультації щодо підготовки до автономних походів.
  - `RE88977` (1 500 ₴) — Набір «Похідна їжа 3.0 Race Expert Club»: комбінація сублімованих страв ЇDLO з в'яленим м'ясом індички та курки ЇDLO.
- **Ситні м'ясні снеки та джерки (М'яско ToGo — 1 500 ₴ за комплект):**
  - `RE89414` — Набір м'ясних снеків з перцем та паприкою (16 пачок по 30 г сушених ломтиків добірної курки).
  - `RE89413` — Набір м'ясних снеків з сиром Гауда (16 пачок по 30 г сушеного курячого філе з сиром).
  - `RE89329`, `RE89328`, `RE89327`, `RE89326`, `RE89325`, `RE89324` — Набори «М'яско ToGo» (8 великих пачок по 50 г в'яленого м'яса: свинина, індичка, курка з азійським, лимонним або традиційним смаком).
- **Термошкарпетки для трекінгу (1+1=3 за 1 058 ₴):**
  - `RE89634` (розмір 35–37), `RE89635` (38–40), `RE89636` (40–42), `RE89637` (43–45).
- **Гірський трейл та автономія (Гідратація та енергія):**
  - `UT-PRO-2026` (1 650 ₴) — «Ultra Trail Marathon Pro»: 3x SIS Beta Fuel + 2x SIS Go Hydro + протеїновий батончик.
  - `RE89482` (1 500 ₴) — «Подарунок у похід»: тактичний органайзер EF-09 + флісовий баф + термошкарпетки.

---

### 5.4 Strict Athletic Guardrails (Negative Constraints)
> [!CAUTION]
> 1. **No Fitness Room Intrusion:** Never show indoor gym items (yoga mats, gym shakers, powerlifting creatine) to wilderness hikers asking for trail meals.
> 2. **Never Mask ЇDLO:** The query intent `camp_hot_meals_idlo` must directly query `RE11494`, `RE11495`, and `RE88977` with top priority.
> 3. **Allow Walkers and Hikers to Hydrate:** Remove all validation blockers that prevented `hiking` and `walking` from accessing electrolyte packets.

---

## 6. Category 5: «Подарунки спортсменам та військовим» (Gifts & Commemoration)

### 6.1 Athletic Coach Diagnosis (Post-600 Test Analysis)
- **High Quality but Narrow Pricing:** Agent 5 proved that gift sets are exceptionally curated (finisher medals, shell-casing keychains, Sharpey towels), but baseline prices strictly start at 1 379 ₴ – 1 500 ₴. Buyers with budgets of 500–1000 ₴ need transparent educational floor-anchoring instead of dead-end crashes.
- **Recipient Taxonomy:** Buyers shopping for gifts need intuitive pathways based on **who they are gifting to** (runner, veteran, gym lifter, traveler), preventing sizing confusion.

---

### 6.2 Question Flow (UA & RU)

#### **Питання 1 (Кому обираєте подарунок) / Вопрос 1 (Кому выбираете подарок)**
*«Кому ви обираєте подарунок?»* / *«Кому вы выбираете подарок?»*

| Ключ / Option ID | Текст варіанту (UA) | Текст варианта (RU) | Пояснювальний підтекст для покупця |
|---|---|---|---|
| `gift_for_runner` | **Бігуну або легкоатлету** | **Бегуну или легкоатлету** | Пам'ятні медалі забігів, пляшки для бігу, спортивні шкарпетки, бігова кепка. |
| `gift_for_military` | **Військовому, ветерану або патріоту України** | **Военному, ветерану или патриоту Украины** | Колекційні нагородні медалі з бойовою символікою, брелоки з гільз та фрагментів дронів. |
| `gift_for_gym` | **Силовому атлету або відвідувачу залу** | **Силовому атлету или посетителю зала** | Великі банні рушники для тренажерів, якісні шейкери, вітамінні комплекси. |
| `gift_universal_travel` | **Мандрівнику або універсальний подарунок для затишку** | **Путешественнику или универсальный подарок для уюта** | Преміальний комплект із 3 бавовняних рушників, теплий баф, похідні аксесуари. |

---

#### **Питання 2 (Характер та стиль подарунка) / Вопрос 2 (Характер подарка)**
*«Який характер подарунка вам ближчий?»* / *«Какой характер подарка вам ближе?»*

| Ключ / Option ID | Текст варіанту (UA) | Текст варианта (RU) | Пояснювальний підтекст для покупця |
|---|---|---|---|
| `gift_style_commemorative` | **Символічний / Пам'ятний (металева медаль + брелоки)** | **Символический / Памятный (металлическая медаль + брелоки)** | Важка якісна медаль на стрічці («Озброєні волею», «Крила Свободи», «Гвардія Небес») та брелок. |
| `gift_style_practical_gear` | **Практичний спортивний (пляшка, кепка, шкарпетки)** | **Практичный спортивный (бутылка, кепка, носки)** | Корисні речі, якими спортсмен користуватиметься на кожному тренуванні. |
| `gift_style_premium_textile` | **Преміальний домашній текстиль (набір рушників Sharpey)** | **Премиальный домашний текстиль (набор полотенец Sharpey)** | 3 великі бавовняні рушники 135х70 см у фірмовій кольоровій гамі. Без ризику помилитися з розміром! |
| `gift_style_travel_box` | **Похідний / Дорожній набір (органайзер, баф, пляшка)** | **Походный / Дорожный набор (органайзер, бафф, бутылка)** | Компактний органайзер EF-09, флісовий баф для захисту від вітру. |

---

#### **Питання 3 (Питання про розмір взуття) / Вопрос 3 (Вопрос о размере)**
*«Чи знаєте ви точний розмір взуття отримувача?»* / *«Знаете ли вы точный размер обуви получателя?»*

| Ключ / Option ID | Текст варіанту (UA) | Текст варианта (RU) | Пояснювальний підтекст |
|---|---|---|---|
| `gift_size_unknown` | **Не знаю / Краще подарунок БЕЗ прив'язки до розміру** | **Не знаю / Лучше подарок БЕЗ привязки к размеру** | Система підбере набори з медалями, рушниками, пляшками чи кепками (100% гарантія попадання). |
| `gift_size_40_42` | **Розмір 40–42 (підходить більшості)** | **Размер 40–42 (подходит большинству)** | Можна додавати бігові або темні шкарпетки RE2. |
| `gift_size_43_45` | **Розмір 43–45 (великий розмір)** | **Размер 43–45 (большой размер)** | Набори зі шкарпетками великого розміру. |

---

### 6.3 Grounded Catalog SKU Mapping (207 Sets)

- **Патріотичні нагородні та пам'ятні набори (1 499 – 1 500 ₴):**
  - `RE11694` — «Воля та незламність»: медаль «Озброєні волею» + 3 місяці клубу.
  - `RE89455` — «Незборний дух»: важка медаль «Озброєні волею 2.0» + ексклюзивні брелоки Fighter та Drone.
  - `RE89454` — «Політ честі»: нагородна медаль «Крила Свободи» + брелоки авіаційної тематики.
  - `RE89453` — «Мирне небо»: нагородна медаль «Гвардія Небес» + патріотичні брелоки.
  - `RE89458` — «Єдність сильних»: медаль «Незалежність — це кожен з нас» з рухомими елементами.
  - `RE89473` — «Подвійна нагорода»: дві металеві медалі «Озброєні волею 2.0» та «Здатні без зброї».
  - `Nabir_1060`, `Nabir_1061`, `Nabir_1062`, `Nabir_1063`, `Nabir_1064` — фірмові подарункові бокси з медалями та гільзовими брелоками.
- **Подарунки для бігунів та активних людей:**
  - `RE89467` та `RE89466` (1 500 ₴) — «Подарунок початківцю 1.0 / 2.0»: металева медаль («Крила Свободи» / «Озброєні волею») + стильна скляна бігова пляшка Race Expert.
  - `RE89481` (1 500 ₴) — «Подарунок для активних днів»: медаль «Patriotic Pulse» + шкарпетки RE2 40–44 + клуб.
  - `RE11024` (1 500 ₴) — «Подарунок спортсмену Race Expert Club»: 2 пари шкарпеток RE2 (білі та темні) + щоденні вітаміни NOW Daily Vits.
  - `RE11026` (1 500 ₴) — «Спортивний подарунок»: шкарпетки 43–45 + 3 брелоки з гільз + вітаміни.
- **Преміальний банний текстиль (100% Cotton Sharpey, 1 500 ₴):**
  - `RE89487` — «Банні рушники Шарпей: темна гама» (3 рушники 135х70 см).
  - `RE89486` — «Банні рушники Шарпей: класика» (3 рушники 135х70 см).
- **Для військових та мандрівників:**
  - `RE89460` (1 500 ₴) — «Подарунок військовому-спортсмену»: медаль «Гвардія Небес» + флісовий захисний баф + темні шкарпетки.
  - `RE89459` (1 439 ₴) — «Подарунок мандрівнику»: банний рушник Sharpey 135х70 см + теплий флісовий баф + клуб.
  - `RE89482` (1 500 ₴) — «Подарунок у похід»: тактичний органайзер EF-09 + баф + шкарпетки.
  - `RE89485` (1 379 ₴) — «Подарунок для прогулянок»: медаль «Здатні без зброї» + баф (найдоступніший подарунок).

---

### 6.4 Strict Athletic Guardrails (Negative Constraints)
> [!CAUTION]
> 1. **Zero Raw Supplement Dumping:** NEVER recommend pure creatine powders, amino acid jars, or sleeping tablets as gifts unless the user explicitly requested sports nutrition.
> 2. **Graceful Floor-Anchor Messaging:** When a buyer specifies a budget of 500–1 000 ₴, NEVER fail with an empty screen. Display the coach floor-anchor card:  
>    *UA:* «У категорії офіційних подарунків повноцінні набори починаються від 1 379 ₴ (включають нагородну атрибутику або преміальний текстиль). Нижче представлені найбільш доступні та популярні варіанти.»  
>    *RU:* «В категории официальных подарков полноценные наборы начинаются от 1 379 ₴ (включают наградную атрибутику или премиальный текстиль). Ниже представлены самые доступные и популярные варианты.»
> 3. **The Sizing Fallback:** If `gift_size_unknown` is selected, NEVER return sets that contain socks or footwear. Return only towels, medals, keychains, bottles, and organizers.

---

## 7. Cross-Category Guardrails & Athletic Architecture Summary

```
+---------------------------------------------------------------------------------------------------+
|                                 RACE EXPERT ATHLETIC INTEGRITY RULES                              |
+---------------------------------------------------------------------------------------------------+
|  1. AEROBIC VS ANAEROBIC PURITY                                                                   |
|     * Creatine Monohydrate tubs (300-500g) are STRICTLY RESTRICTED to Gym & Strength goals.       |
|     * Marathoners (21.1 / 42.2 km) NEVER receive powerlifting / mass gainer recommendations.      |
|                                                                                                   |
|  2. ZERO DECEPTIVE ADVERTISING                                                                    |
|     * BANNED PHRASE: 'у наборі саме X (без сторонніх речей)' when extraneous items exist.         |
|     * Transparently disclose bundled items: e.g. "Набір містить 5 гелів + банку креатину 300 г".  |
|                                                                                                   |
|  3. SIZING DISCIPLINE                                                                             |
|     * Never guess shoe sizes or default to size 46-48.                                             |
|     * Supported sizes: 35-37, 38-40, 40-42, 43-45, 46-48.                                         |
|     * If size unknown -> Recommend size-free gear (bib belts, flasks, massage rollers, towels).   |
|                                                                                                   |
|  4. RESCUE DEHYDRATED RATIONS (ЇDLO)                                                              |
|     * Re-index RE11494, RE11495, RE88977 into camping meals so outdoors searches succeed 100%.    |
|                                                                                                   |
|  5. ELIMINATE GHOST SPORTS                                                                        |
|     * Remove swimming, gymnastics, and martial arts from quiz options (0 catalog sets).           |
|                                                                                                   |
|  6. BUDGET FLOOR-ANCHORING                                                                        |
|     * For low-budget requests (400-800 ₴), provide clear educational messages and the closest     |
|       baseline kit instead of empty 0-result dead ends.                                           |
+---------------------------------------------------------------------------------------------------+
```

---
*Document compiled and verified by Head Athletic Coach & Equipment Specialist.*  
*Ready for immediate implementation in `draft_matcher.py` and frontend question tree.*
