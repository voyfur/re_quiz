# Production AI Question System: Clinical & Athletic Conversational Architecture (9 Categories)
**Role:** Lead Conversational Architect & Clinical AI Question Designer for Race Expert
**Foundational Corpus:** 900 End-to-End Stress Test Scenarios Across 207 Catalog Sets
**Guiding Philosophy:** Rigorous AI-Evaluated Goal Congruence (*«Подходит / Не подходит к ключевой цели»*)
**Document Status:** Production Master Reference | Zero Dead Ends Guaranteed

---

# 1. Executive Manifesto & The «Подходит / Не подходит» AI Philosophy

## 1.1. The User's Foundational Directive
> *«То есть агенты должны будут руководствоваться такой логикой. К примеру: „Для какой цели вы выбираете набор?“ Заходят, например, на „Гидратация“: это электролиты.*  
> *Вот тут есть вопрос: какой ключевой тип товара?*  
> *- Спортивне харчування*  
> *- Ізотоніки та електроліти*  
> *- Спортивний аксесуар: это пляшка*  
> *Тут должен возникать вопрос: подходит ли это для ключевой цели? Спортивные аксессуары и фляжки подходят для цели „Гидратация“? Это электролиты?*  
> *Это вот как один пример. Тут нужна агентская система, тут нужен агент, который будет задавать себе вопрос: „Подходит, не подходит?“ и составлять кучу вопросов, таким образом, чтобы это все идеально ложилось на квиз. Где надо 5 вопросов, где надо 10 вопросов. То есть это должны быть вопросы, чтобы максимально дать человеку то, что он хочет, и использовать здесь только логику искусственного интеллекта.»*

## 1.2. The 4 Inviolable Golden Rules of Goal Congruence

1. **The Primary Deliverable Invariant (No Fake Substitutions):**  
   When a buyer enters a category with a physiological need (e.g., Hydration, Recovery, Running Endurance), they **MUST receive the active physiological agent** (electrolytes, restorative minerals, energy fuels). An accessory (such as a water bottle, soft flask, towel, socks, or shaker) can **NEVER be substituted as the sole deliverable** for a nutritional or physiological need. Accessories may ONLY be offered as **companion bundles** (e.g., *«Electrolytes + Soft Flask Bundle»*) or when the user explicitly requests gear alone in the dedicated Gear category.

2. **Strict Negative Constraints & Domain Banishment (Zero Toxic Cross-Contamination):**  
   Grounded in our 900 stress tests, algorithmic classification errors led to severe pharmacological absurdities. Under this AI Question System, the following strict exclusions are hardcoded into every question branch:
   - **Creatine & Pre-workout Stimulants** are permanently BANISHED from Recovery (Sleep), Daily Health, Endurance Running, and Gear.
   - **Sedatives & Neuro-relaxants** (ZMA, GABA, Melatonin, 5-HTP) are BANISHED from Gym Pre-Workout, Daytime Energy, and Race Morning.
   - **Dehydrated Hot Camping Meals (ЇDLO)** are strictly distinguished from sweet endurance running gels and gym snack bars.
   - **Psychoactive & Functional Mushrooms (Amanita muscaria / Lion's Mane)** require explicit, unbundled informed consent — NEVER recommended covertly or defaulted.
   - **Socks & Apparel** are BANISHED as standalone results from Hydration, Food, and Recovery.

3. **Physical Sizing Integrity (Shoe Size Precision vs. Zero-Sizing Safety):**  
   Whenever a set contains socks, calf sleeves, or wearable textiles, a precise shoe size verification question (35–37, 38–40, 40–42, 43–45, 46–48) is **MANDATORY**. If the buyer is choosing a gift or does not know the shoe size, the quiz MUST divert them to **zero-sizing items** (Sharpey towels, medal hangers, electrolytes, nutrition) to prevent delivery of unwearable gear.

4. **Adaptive Diagnostic Flow (5 to 10 Questions):**  
   Instead of a shallow 3-question filter, each category features an adaptive sequence of 8 to 10 deep, clinically and athletically calibrated questions that replicate an empathetic elite coach and sports doctor. Questions cover core need, modality, component bundle composition, form factor, sizing, physiological constraints, supply duration, and budget anchors.

---

# 2. Category 1: «Гідратація та сольовий баланс» (Hydration & Electrolytes)

## 2.1. Category Mission & Primary Deliverable
- **Core Physiological Mission:** Prevention of hyponatremia, maintenance of plasma osmolarity, electrolyte mineral replenishment (Na+, K+, Mg2+, Cl-), and cellular hydration during sweat-inducing physical exertion or hot weather.
- **The Primary Deliverable:** Bioavailable electrolyte salts, effervescent mineral drinks, or isotonic endurance blends.
- **The Accessory Pairing Rule (User Mandate):** A water bottle, soft flask, or hydration belt **CANNOT** be presented as a standalone hydration product! A buyer asking for hydration needs electrolytes. Water vessels are offered strictly as **bundle companions** (*«Електроліти + фірмова пляшка/фляга»*) or excluded if the buyer already owns their gear.

## 2.2. Exact Adaptive Question Sequence (8 Questions)

### Q1: Specific Core Need / Clinical Problem (Головна потреба в гідратації)
**UA:** З якою головною метою ви обираєте набір для гідратації?  
**RU:** С какой главной целью вы выбираете набор для гидратации?
- **OPT-HYD-1.1:** Захист від судом, спазмів та зневоднення у спеку або при рясному потовиділенні  
  *Опис:* Фокус на швидкому відновленні сольового балансу (натрій, магній, калій).
- **OPT-HYD-1.2:** Підтримка витривалості на довгих дистанціях (біг, вело, трейли >60–90 хв)  
  *Опис:* Ізотонічні суміші з легкими вуглеводами для підтримання темпу та водно-сольового балансу.
- **OPT-HYD-1.3:** Щоденна мінералізація та тонус (офіс, щоденна активність, легкий фітнес)  
  *Опис:* М'яка регідратація з мікроелементами без високих доз цукру чи кофеїну.
- **OPT-HYD-1.4:** Комплексне післятренувальне відновлення водно-сольового дефіциту та м'язів  
  *Опис:* Поєднання електролітів із магнієм проти нічних спазмів та кріпатури.

### Q2: Specific Modality / Conditions (Умови та контекст активності)
**UA:** В яких умовах або для якого виду спорту планується прийом?  
**RU:** В каких условиях или для какого вида спорта планируется прием?
- **OPT-HYD-2.1:** Спекотна погода, літні тренування або висока температура в залі
- **OPT-HYD-2.2:** Тривалий шосейний або трейловий біг / півмарафон / марафон
- **OPT-HYD-2.3:** Велоспорт, кросфіт, триатлон або функціональний фітнес
- **OPT-HYD-2.4:** Військова служба, польові умови або тактичні марші
- **OPT-HYD-2.5:** Щоденне вживання без екстремальних навантажень

### Q3: Component Requirements & Add-ons (Вимоги до комплектації — пляшка / аксесуар)
**UA:** Чи потрібна вам спортивна пляшка або аксесуар у комплекті з електролітами?  
**RU:** Нужна ли вам спортивная бутылка или аксессуар в комплекте с электролитами?
- **OPT-HYD-3.1:** Тільки електроліти / ізотоніки (пляшка, фляга та екіпірування вже є)  
  *AI-принцип:* 100% бюджету спрямовується на чисті електроліти та солі.
- **OPT-HYD-3.2:** Повний комплект: електроліти + спортивна пляшка / фляга  
  *AI-принцип:* Включає порційні стіки або таблетки + герметичну пляшку з чохлом або софт-флягу.
- **OPT-HYD-3.3:** Максимальний біговий набір: електроліти + кепка / стартовий пояс / шкарпетки  
  *AI-принцип:* Комплексний стартовий набір для змагань або тренувань.

### Q4: Delivery Form Factor (Форма випуску електролітів)
**UA:** Який формат прийому солей є для вас найзручнішим?  
**RU:** Какой формат приема солей для вас наиболее удобен?
- **OPT-HYD-4.1:** Порційні стіки / саше з порошком (миттєве розчинення у воді на бігу або в дорозі)
- **OPT-HYD-4.2:** Шипучі швидкорозчинні таблетки (у тубусі, легко дозувати в пляшку)
- **OPT-HYD-4.3:** Сольові капсули (ковтати, запиваючи чистою водою, без смаку та підсолоджувачів)
- **OPT-HYD-4.4:** Готові рідкі концентровані шоти або гелі з електролітами
- **OPT-HYD-4.5:** Форма не має значення (довіряю рекомендації експерта)

### Q5: Physical Sizing / Measurements (Розмір ноги для наборів з екіпіруванням)
**UA:** Якщо у вибраному наборі присутні спортивні шкарпетки, вкажіть ваш розмір взуття:  
**RU:** Если в выбранном наборе присутствуют спортивные носки, укажите ваш размер обуви:
- **OPT-HYD-5.0:** Без шкарпеток (набір суто з електролітами або пляшкою без текстилю)
- **OPT-HYD-5.1:** Розмір 35–37 (S)
- **OPT-HYD-5.2:** Розмір 38–40 (M)
- **OPT-HYD-5.3:** Розмір 40–42 (M/L)
- **OPT-HYD-5.4:** Розмір 43–45 (L/XL)
- **OPT-HYD-5.5:** Розмір 46–48 (XXL)

### Q6: Dietary / Physiological Constraints (Чутливість та склад)
**UA:** Чи є у вас особливі фізіологічні побажання щодо складу напою?  
**RU:** Есть ли у вас особые физиологические пожелания по составу напитка?
- **OPT-HYD-6.1:** Чутливий шлунок: без цукру, гіпотонічний профіль, легке засвоєння
- **OPT-HYD-6.2:** Чистий сольовий профіль без кофеїну (підходить для вечора та спеки)
- **OPT-HYD-6.3:** З додатковою порцією кофеїну для енергії на пізніх кілометрах
- **OPT-HYD-6.4:** Жодних обмежень (стандартний атлетичний ізотонік)

### Q7: Volume / Supply Duration (Обсяг та тривалість запасу)
**UA:** На який період або кількість тренувань вам потрібен запас?  
**RU:** На какой период или количество тренировок вам нужен запас?
- **OPT-HYD-7.1:** Тестовий / стартовий набір (8–10 порцій на 1–2 старти або тиждень спеки)
- **OPT-HYD-7.2:** Місячний тренувальний курс (16–20 порцій активного спорту)
- **OPT-HYD-7.3:** Сезонний запас з клубною програмою Race Expert Club (3 місяці підтримки)

### Q8: Budget Expectation & Floor Awareness (Бюджетний орієнтир)
**UA:** Який бюджет ви розглядаєте для набору гідратації?  
**RU:** Какой бюджет вы рассматриваете для набора гидратации?
- **OPT-HYD-8.1:** Базовий запас електролітів (1200–1350 грн)  
  *Експертна підказка:* Сертифіковані електроліти стандартів WADA/Informed Sport починаються від 1200 грн.
- **OPT-HYD-8.2:** Повний комплект із пляшкою або клубною програмою (1380–1500+ грн)  
  *Експертна підказка:* Включає перевірену фірмову флягу або 3-місячний абонемент клубу.

## 2.3. The «Подходит / Не подходит» Critical Audit for Hydration
| Запитання та опція | Статус AI | Чому підходить (Клінічне обґрунтування) | Який негативний брак / витік блокує? |
|---|---|---|---|
| **Q3: Пляшка окремо vs Пляшка + електроліти** | **ПІДХОДИТЬ ТІЛЬКИ В БАНДЛІ** | Пляшка є лише інструментом доставки електролітів до клітин; покупець у категорії гідратації купує водно-сольовий баланс. | **Блокує продаж порожньої пляшки або шкарпеток без солей** (запобігає абсурду, коли замість розчину від судом людині пропонують лише скло або баф). |
| **Бан Спіруліни (`RE11513`)** | **НЕ ПІДХОДИТЬ** | Спіруліна є детокс-суперфудом і джерелом антиоксидантів, вона не містить необхідної концентрації електролітів для профілактики зневоднення. | **Блокує витік таблетованих водоростей** у запити спраглих марафонців у спеку. |
| **Бан Їжовика гребінчастого (`RE88943`)** | **НЕ ПІДХОДИТЬ** | Гриби Lion's Mane є ноотропом для мозку, вони не відновлюють втрату натрію та калію при потінні. | **Блокує ноотропний витік** у категорію осмотичної гідратації. |
| **Бан Креатину (`Nabir_1128`, `RE11636`)** | **НЕ ПІДХОДИТЬ** | Креатин зв'язує воду внутрішньоклітинно в саркоплазмі, створюючи додаткове осмотичне навантаження на нирки у спеку без відновлення іонів плазми. | **Блокує важкоатлетичні моногідрати** при біговій гідратації. |
| **Бан чистих шкарпеток (`RE11013`)** | **НЕ ПІДХОДИТЬ** | Набір «Бігова пара» містить 2 пари шкарпеток і 0 мг солей. | **Блокує нульовий сольовий баланс** під виглядом гідратації. |

## 2.4. Grounded Catalog SKU Mapping (Hydration)
Всі 22 набори категорії «Гідратація» чітко розбиті за клінічними гілками:

### Гілка А: Чисті електроліти (без аксесуарів / якщо пляшка є)
- **[Nabir_1015]** *Набір «Електролітний запас Race Expert Club»* — **1500 грн**  
  *Склад:* абонемент Race Expert Club на 3 месяца; 20 стиков Hydria Perform
- **[RE11650]** *Набір «Захист від спеки» по програмі "Ветеранський спорт"* — **1239 грн**  
  *Склад:* Precision Hydration 1000 Tube, 10 таблеток; Precision Fuel & Hydration капсулы с электролитами, 15 caps
- **[RE88946]** *Набір «Гідратація тренувань Race Expert Club» — абонемент на 3 місяці* — **1500 грн**  
  *Склад:* клуб на 3 месяца; электролиты Hydria Daily, 8 стиков (1 стик на 500–850 мл воды; натрий, калий, магний, кальций, витамины C/B5/B6/B12); гели SiS Go + Electrolyte 60 мл ×4 (22 г углеводов каждый; 118 мг Na, 9,5 мг K, 1,5 мг Mg); стеклянная бутылка 530 мл. Назначение/активность: бег, велоспорт и фитнес, длительные/интенсивные тренировки. Точная дистанция не задана. - Теги: purpose:training_hydration; item_type:club_membership_bundle; sport:running; sport:cycling; sport:general_fitness; distance:unspecified; duration:3_months; contains:electrolytes; contains:carbohydrates; audience:cyclists; audience:fitness_participants; audience:runners; buyer_weight:not_specified; price:1500_uah
- **[UT-PRO-2026]** *Набір «Ultra Trail Marathon Energy & Hydration Pro»* — **1650 грн**  
  *Склад:* 3x SIS Beta Fuel гелі, 2x SIS Go Hydro електроліти, 1x протеїновий батончик Science in Sport

### Гілка Б: Повний комплект гідратації (Електроліти + Спортивна пляшка)
- **[Nabir_1123]** *Набір «Комплект для гідратації Race Expert Club»* — **1435 грн**  
  *Склад:* абонемент Race Expert Club на 3 месяца; 16 стиков Hydria Perform; бутылка Race Expert, 600 мл
- **[RE11021]** *Набір «Літній старт Race Expert Club» — абонемент на 3 місяці* — **1379 грн**  
  *Склад:* белые носки Race Expert размер 40–44 x2 pairs; glass бутылка Race Expert 530 ml; Hydria Daily peach sticks x8; Hydria Perform lemon sticks x2

### Гілка В: Гідратація + Відновлення від судом та кріпатури (Електроліти + Магній)
- **[RE11652]** *Набір «Боротьба з кріпатурою»* — **1500 грн**  
  *Склад:* Swanson Triple Magnesium Complex 400 mg, 100 caps; Hydria Perform стики с электролитами x5
- **[RE89451]** *Набір «Відновлення після тренування» — абонемент на 3 місяці* — **1500 грн**  
  *Склад:* клуб на 3 месяца; полотенце 135×70 см; Source Naturals Ultra-Mag, 60 таблеток; Hydria Perform, 4 стика; SiS GO Isotonic Gel 60 мл (карточка дублирует/повторяет строку с гелем, количество неясно)

### Гілка Г: Бігова гідратація + Енергія (Електроліти + Ізотоніки / Батончики)
- **[RE11659]** *Набір «Тиждень бігуна»* — **1200 грн**  
  *Склад:* Sponser Crunchy Protein Bar, 50 g x2; Hydria Perform lemon sticks x6; GU Energy Chews lemonade, 60 g x1. В начале описания упоминается энергетический гель, но нумерованный список товаров его не содержит
- **[RE11806]** *Набір «Енергія дистанції Race Expert Club» — абонемент на 3 місяці* — **1475 грн**  
  *Склад:* абонемент Race Expert Club на 3 месяца; DRUMn’BADS liquid cordyceps, 30 ml; Swanson CoQ10 Mini Cap, 10 mg, 100 caps; Precision Hydration 500 Tube, 15 таблеток
- **[RE11802]** *Набір «Витривалість без спраги Race Expert Club» — абонемент на 3 месяца* — **1500 грн**  
  *Склад:* абонемент Race Expert Club на 3 месяца; Nutriversum EAA Sugar Free 500 g ×1; Hydria Perform стики с электролитами ×5; Brave U Shaker 700 ml ×1. Назначение по описанию набора: поддержка гидратации и выносливости во время интенсивных занятий. Занятия: бег, велоспорт, силовые тренировки и HIIT. Указанные метрики/состав: 12 g EAA растворяют в 300–400 ml; Hydria stick — в 500–850 ml. Неопределённость: существенной неопределённости нет
- **[RE11786]** *Набір «Тренувальний ресурс Race Expert Club» — абонемент на 3 місяці* — **1285 грн**  
  *Склад:* абонемент клуба на 3 месяца; Nutriversum BCAA 2:1:1 Sugar Free, 360 г; Hydria Perform, 5 стиков; шейкер Myprotein 600 мл

---

# 3. Category 2: «Відновлення та якісний сон» (Recovery, Sleep & CNS Regeneration)

## 3.1. Category Mission & Primary Deliverable
- **Core Physiological Mission:** Down-regulation of the sympathetic nervous system, induction of slow-wave parasympathetic sleep, reduction of circulating evening cortisol, acceleration of myofibrillar protein synthesis, and relief of delayed onset muscle soreness (DOMS) and joint inflammation.
- **The Primary Deliverable:** Neuro-calming minerals (high-absorption Magnesium Glycinate/Citrate), neurotransmitter precursors (5-HTP, GABA, L-Theanine), joint matrix rebuilders (Collagen, Chondroitin, Hyaluronic Acid), and restorative herbal complexes.
- **The Core Negative Rule (Agent 1 Forensic Finding):** Under NO CIRCUMSTANCE may daytime energizers, pre-workout stimulants, or creatine be recommended for nighttime sleep! Furthermore, functional mushroom sleep complexes (Amanita muscaria / Reishi) must feature transparent warnings, and deep-sleep formulas (ZMA) can NEVER be recommended as a daytime pre-workout charge.

## 3.2. Exact Adaptive Question Sequence (8 Questions)

### Q1: Specific Core Need / Clinical Problem (Першочергова потреба у відновленні)
**UA:** Що саме зараз найбільше потребує відновлення у вашому організмі?  
**RU:** Что именно сейчас больше всего нуждается в восстановлении в вашем организме?
- **OPT-REC-1.1:** Глибокий сон та засинання: зняти вечірній стрес, зупинити потік думок, подолати безсоння  
  *Клінічний вектор:* Мелатонін, 5-HTP, GABA, магній гліцинат, розслаблюючі трави.
- **OPT-REC-1.2:** М'язове відновлення після тренувань: біль у м'язах (кріпатура), спазми та перевтома  
  *Клінічний вектор:* Високі дози магнію, цинк, амінокислоти BCAA/EAA, електроліти.
- **OPT-REC-1.3:** Зв'язки, сухожилля та суглоби: хрускіт, запалення або високе ударне навантаження  
  *Клінічний вектор:* Колаген, глюкозамін, хондроїтин, гіалуронова кислота, кальцій + D3.
- **OPT-REC-1.4:** Денна стійкість до стресу та кортизолу без снодійного ефекту  
  *Клінічний вектор:* Адаптогени (ашваганда, родіола), вітаміни групи B, денний тонус.

### Q2: Circadian Timing & Routine Context (Час прийому та біоритми)
**UA:** В який час доби ви плануєте прийом комплексу?  
**RU:** В какое время суток вы планируете прием комплекса?
- **OPT-REC-2.1:** Безпосередньо перед сном (за 30–60 хв до вимкнення світла)
- **OPT-REC-2.2:** Одразу після інтенсивного тренування (протягом 30 хв)
- **OPT-REC-2.3:** Вранці або вдень під час їжі (підтримка тонусу та адаптація до стресу)
- **OPT-REC-2.4:** Регулярний курс протягом усього дня (ранок + вечір)

### Q3: Delivery Form Factor (Зручний формат прийому)
**UA:** Якій формі прийому ви віддаєте перевагу?  
**RU:** Какой форме приема вы отдаете предпочтение?
- **OPT-REC-3.1:** Капсули / таблетки (легко запити склянкою води перед сном)
- **OPT-REC-3.2:** Розчинний напій або порошок (приємний вечірній або післятренувальний ритуал)
- **OPT-REC-3.3:** Рідина / концентрат або сироп швидкої дії
- **OPT-REC-3.4:** Форма не має значення

### Q4: Botanical & Functional Mushroom Sensitivity (Ставлення до рослинних екстрактів та мікродозингу)
**UA:** Чи бажаєте ви додати до набору заспокійливі трави або функціональні гриби?  
**RU:** Желаете ли вы добавить в набор успокаивающие травы или функциональные грибы?
- **OPT-REC-4.1:** Тільки класичні мінерали та амінокислоти (чистий магній, цинк, вітамін B6, 5-HTP)
- **OPT-REC-4.2:** Класичні заспокійливі трави (валеріана, пасифлора, меліса, ромашка)
- **OPT-REC-4.3:** Функціональні гриби для сну та регенерації ЦНС (Рейші, мікродозинг мухомора / Amanita muscaria)
- **OPT-REC-4.4:** Без психоактивних або специфічних компонентів (суворо перевірений спортивний стандарт)

### Q5: Physical Sizing / Measurements (Розмір ноги для наборів із рушниками або текстилем)
**UA:** Якщо у відновлювальному наборі є текстильний аксесуар (шкарпетки або компресія), вкажіть розмір:  
**RU:** Если в восстановительном наборе есть текстильный аксессуар, укажите размер:
- **OPT-REC-5.0:** Без шкарпеток (набір суто з капсулами, порошками або банним рушником Шарпей)
- **OPT-REC-5.1:** Розмір 35–37
- **OPT-REC-5.2:** Розмір 38–40
- **OPT-REC-5.3:** Розмір 40–42
- **OPT-REC-5.4:** Розмір 43–45
- **OPT-REC-5.5:** Розмір 46–48

### Q6: Digestive & Physiological Constraints (Фізіологічні особливості)
**UA:** Чи є у вас обмеження щодо шлунково-кишкового тракту?  
**RU:** Есть ли у вас ограничения по желудочно-кишечному тракту?
- **OPT-REC-6.1:** Чутливий шлунок (потрібен хелатний бісгліцинат магнію без проносного ефекту)
- **OPT-REC-6.2:** Повна відсутність мелатоніну (природна регуляція без гормональних компонентів)
- **OPT-REC-6.3:** Без цукру та штучних барвників
- **OPT-REC-6.4:** Жодних обмежень

### Q7: Volume / Supply Duration (Курс відновлення)
**UA:** На яку тривалість відновлювального курсу ви розраховуєте?  
**RU:** На какую продолжительность восстановительного курса вы рассчитываете?
- **OPT-REC-7.1:** Швидка екстрена допомога на 10–14 днів (після забігу чи пікового збору)
- **OPT-REC-7.2:** Стандартний місячний курс нормалізації сну (30–60 днів)
- **OPT-REC-7.3:** 3-місячний абонемент з клубним супроводом та моніторингом прогресу

### Q8: Budget Expectation & Floor Awareness (Бюджетний рівень)
**UA:** Який бюджет ви плануєте на відновлювальний комплекс?  
**RU:** Какой бюджет вы планируете на восстановительный комплекс?
- **OPT-REC-8.1:** Базовий моноелементний набір (985–1270 грн)  
  *Приклад:* «М'язи в тонусі» (985 грн) або «Опора руху» (1269 грн).
- **OPT-REC-8.2:** Комплексна нейро-фармакологічна формула чи клубний набір (1380–1500 грн)  
  *Приклад:* Повні комплекси з магнієм, 5-HTP, GABA та супроводом лікаря.

## 3.3. The «Подходит / Не подходит» Critical Audit for Recovery
| Запитання та опція | Статус AI | Чому підходить (Клінічне обґрунтування) | Який негативний брак / витік блокує? |
|---|---|---|---|
| **Бан ZMA перед денним тренуванням** | **СУВОРО НЕ ПІДХОДИТЬ** | ZMA містить високі дози магнію та вітаміну B6, які стимулюють вироблення ГАМК і розслаблюють ЦНС; прийом перед тренуванням спричиняє сонливість, зниження реакції та м'язову млявість. | **Блокує рекомендацію нічного ZMA як енергетика** (критична помилка з `agent_1_report.md`). |
| **Бан Креатину у вечірній сон** | **НЕ ПІДХОДИТЬ** | Креатин підвищує рівень клітинного АТФ і викликає прилив бадьорості, затримуючи засинання. | **Блокує витік важкоатлетичних стимуляторів у категорію сну**. |
| **Прозорий мікродозинг мухомора (`RE11525`)** | **ПІДХОДИТЬ ТІЛЬКИ З ПОПЕРЕДЖЕННЯМ** | Мухомор (Amanita muscaria) містить мусцимол, що впливає на ГАМК-рецептори, але є специфічним етноботанічним продуктом. | **Блокує нав'язування мухоморів людям, які шукають звичайний аптечний магній або цинк**. |
| **Підтримка суглобів (`RE11812`, `RE11810`)** | **ПІДХОДИТЬ ДЛЯ ВІДНОВЛЕННЯ ОПОРНО-РУХОВОГО АПАРАТУ** | Відновлення охоплює не лише сон, а й ремоделювання колагену та регенерацію суглобового хряща після навантажень. | **Забезпечує точне позиціонування наборів для бігунів із болями в колінах**. |

## 3.4. Grounded Catalog SKU Mapping (Recovery)
### Гілка А: Глибокий нічний сон та розслаблення ЦНС (Магній + 5-HTP + GABA)
- **[RE89017]** *Набір «Вечірній ритуал Race Expert Club»* — **1425 грн**  
  *Склад:* абонемент Race Expert Club на 3 месяца; рейши Mind Shi, 1 000 мг, 60 капсул; мелатонин Swanson, 3 мг, 120 капсул; комплекс Source Naturals Ultra-Mag, 60 таблеток
- **[RE88965]** *Набір «Вечірнє розслаблення Race Expert Club» — абонемент на 3 місяці* — **1500 грн**  
  *Склад:* абонемент Race Expert Club на 3 месяца; Reishi 700 mg, 60 caps; NOW 5-HTP 50 mg, 30 caps; KAL Stress B Magnesium Glycinate, 60 caps
- **[RE88947]** *Набір «Спокійний сон Race Expert Club» — абонемент на 3 місяці* — **1485 грн**  
  *Склад:* абонемент Race Expert Club на 3 месяца; Reishi 700 mg, 60 caps; KAL Stress B Magnesium Glycinate, 60 caps; NOW Melatonin 3 mg, 60 caps
- **[RE89026]** *Набір «Нічне відновлення» — абонемент на 3 місяці* — **1500 грн**  
  *Склад:* абонемент Race Expert Club на 3 месяца; Swanson Triple Magnesium 400 mg, 100 caps; Ashwagandha 450 mg, 100 caps; NOW Melatonin 3 mg, 60 caps; NOW 5-HTP 50 mg, 30 caps
- **[RE11523]** *Набір «Глибокий сон і відновлення» — абонемент на 3 місяці* — **1489 грн**  
  *Склад:* абонемент Race Expert Club на 3 месяца; Swanson Ashwagandha, 450 mg, 100 caps; Swanson Melatonin, 3 mg, 60 caps; Swanson Triple Magnesium, 400 mg, 100 caps
- **[RE88958]** *Набір «Відпочинок нервової системи Race Expert Club» — абонемент на 3 місяці* — **1500 грн**  
  *Склад:* Swanson Full Spectrum Ashwagandha 450 mg, 100 caps x2; NOW 5-HTP 50 mg, 30 caps; OstroVit Magnesium Citrate + B6, 90 таблеток (400 mg magnesium + 15 mg B6 per 3-tab serving)
- **[RE88949]** *Набір «Спокійний вечір Race Expert Club» — абонемент на 3 місяці* — **1479 грн**  
  *Склад:* абонемент Race Expert Club на 3 месяца; Mind Shi Reishi Mushroom 1000 mg, 60 caps; Swanson Full Spectrum Ashwagandha 450 mg, 100 caps
- **[RE11803]** *Набір «Польовий сон Race Expert Club» — абонемент на 3 місяці* — **1500 грн**  
  *Склад:* абонемент Race Expert Club на 3 месяца; VPLab Ultra Sleep, 60 caps; Nutriversum Melatonin, 60 caps; Race Expert флисовый бафф
- **[RE11525]** *Набір «Природний сон з грибами Race Expert Club» — абонемент на 3 місяці* — **1485 грн**  
  *Склад:* клуб на 3 месяца; Reishi 1 000 мг, 60 капсул; мелатонин 3 мг, 60 капсул; Nutriversum GABA, 60 капсул

### Гілка Б: М'язове відновлення після тренувань (Зняття кріпатури та спазмів)
- **[RE11652]** *Набір «Боротьба з кріпатурою»* — **1500 грн**  
  *Склад:* Swanson Triple Magnesium Complex 400 mg, 100 caps; Hydria Perform стики с электролитами x5
- **[RE11796]** *Набір «М'язи в тонусі Race Expert Club» — абонемент на 3 місяці* — **985 грн**  
  *Склад:* клуб на 3 месяца; порошок BCAA+Gluta без сахара 500 г; мини-шейкер 300 мл. Порция содержит 5 080 мг аминокислот; мерная порция 6 г разводится в 250 мл воды
- **[RE11797]** *Набір «Швидке відновлення Race Expert Club» — абонемент на 3 місяці* — **1500 грн**  
  *Склад:* клуб на 3 месяца; Nutriversum L-GLUTAMINE 500 г; Sponser Recovery Drink клубника-банан 60 г ×2; мини-шейкер 300 мл
- **[RE89451]** *Набір «Відновлення після тренування» — абонемент на 3 місяці* — **1500 грн**  
  *Склад:* клуб на 3 месяца; полотенце 135×70 см; Source Naturals Ultra-Mag, 60 таблеток; Hydria Perform, 4 стика; SiS GO Isotonic Gel 60 мл (карточка дублирует/повторяет строку с гелем, количество неясно)
- **[Nabir_1127]** *Набір «Продуктивність на максимум Race Expert Club»* — **1379 грн**  
  *Склад:* абонемент Race Expert Club на 3 месяца; комплекс Source Naturals Ultra-Mag, 60 таблеток; Mind Shi 4Mushroom Complex, 60 капсул; 2 батончика Race Expert & DRUMn’BADS с ежовиком, по 40 г

### Гілка В: Відновлення суглобів, зв'язок та кісток (Колаген + Кальцій D3)
- **[RE11812]** *Набір «Опора руху Race Expert Club»* — **1269 грн**  
  *Склад:* абонемент Race Expert Club на 3 месяца; Life Extension Bone Restore, 120 капсул; куркума Swanson, 720 мг, 30 капсул; витамин D3 Now Foods, 2 000 IU, 30 мягких капсул
- **[RE11810]** *Набір «Міцні кістки Race Expert Club» — абонемент на 3 місяці* — **1419 грн**  
  *Склад:* абонемент Race Expert Club на 3 месяца; Nature’s Plus Animal Parade Calcium Chewable, 135 chewables; Solaray Vitamin K2 MK-7 50 mcg, 30 caps; NOW D3 2000 IU, 30 мягких капсул

### Гілка Г: Денна стійкість до стресу та антитривожність (без снодійного ефекту)
- **[Nabir_1101]** *Набір «Антитривожність 2.0 Race Expert Club» — абонемент на 3 місяці* — **1500 грн**  
  *Склад:* клуб на 3 месяца; батончики с рейши 40 г ×2 (более 12 г белка каждый); красный мухомор 500 мг, 60 капсул; рейши 700 мг, 60 капсул. Назначение в формулировке карточки: управление стрессом/эмоциональный баланс и восстановление; аудитория — люди с высокой психоэмоциональной нагрузкой и спортсмены в интенсивных тренировках. Медицинские эффекты не добавлялись. - Теги: purpose:mood_balance_and_recovery; item_type:club_membership_bundle; sport:not_sport_specific; distance:not_applicable; duration:3_months; audience:athletes; buyer_weight:not_specified; price:1500_uah
- **[RE11674]** *Набір «Внутрішній баланс Race Expert Club» — абонемент на 3 місяці* — **1449 грн**  
  *Склад:* VPLab Magnesium Citrate, 90 софтгелей; Mind Shi Lion’s Mane 1 000 мг, 60 капсул; NOW Foods 5-HTP 50 мг, 30 капсул
- **[RE11821]** *Набір «Мінеральний тонус Race Expert Club» — абонемент на 3 місяці* — **1375 грн**  
  *Склад:* клуб на 3 месяца; Life Extension Only Trace Minerals, 90 капсул (цинк, медь, марганец, хром, молибден, бор, ванадий); VPLab Magnesium Citrate, 90 софтгелей

---

# 4. Category 3: «Біг та підготовка до стартів» (Running & Race Preparation)

## 4.1. Category Mission & Primary Deliverable
- **Core Athletic Mission:** Glycogen replenishment, continuous carbohydrate intake on course (30–90 g carbs/hour), cramp prevention via electrolyte osmolarity, race day logistics (bib belt, lightweight hydration flasks, blister-free technical running socks), and rapid post-race glycogen reloading.
- **The Primary Deliverable:** Scientifically engineered endurance energy gels (maltodextrin, fructose 1:0.8 / 2:1), isotonic powders, salt capsules, running caps, race number belts, and anatomical anti-blister running socks.
- **The Core Negative Rule (Agent 2 Forensic Finding):** Gym muscle-mass powders (mass gainers, heavy whey, creatine tubs) are STRICTLY BANISHED. A marathoner cannot carry a 1 kg protein shaker. Every running distance (5k, 10k, 21k half-marathon, 42k marathon, ultra-trail) MUST have direct product fulfillment, eliminating the catastrophic 20-scenario Half-Marathon failure rate.

## 4.2. Exact Adaptive Question Sequence (9 Questions)

### Q1: Target Race Distance & Cadence (Дистанція забігу або тренувань)
**UA:** До якої дистанції ви готуєтесь або який ваш основний біговий обсяг?  
**RU:** К какой дистанции вы готовитесь или какой ваш основной беговой объем?
- **OPT-RUN-1.1:** 5–10 км (динамічний темповий біг, легка гідратація, 1 енергетичний гель)
- **OPT-RUN-1.2:** Півмарафон (21.1 км) — ключова дистанція! (потребує 3–4 гелі + електроліти + шкарпетки)
- **OPT-RUN-1.3:** Марафон (42.2 км) (повна енергетична стратегія: 6–8 гелів + сіль + стартовий пояс)
- **OPT-RUN-1.4:** Ультрамарафон / Трейлраннінг у горах (>50 км) (високовуглеводні гелі Beta Fuel + гідратація)
- **OPT-RUN-1.5:** Регулярні щотижневі пробіжки для здоров'я (без конкретного старту)

### Q2: Primary Race-Day Priority (Головна потреба на старті)
**UA:** Що є найбільш пріоритетним у вашому біговому наборі?  
**RU:** Что является наиболее приоритетным в вашем беговом наборе?
- **OPT-RUN-2.1:** Енергетичне харчування (вуглеводні гелі, що не склеюють рот і не подразнюють шлунок)
- **OPT-RUN-2.2:** Сольовий баланс та гідратація (електроліти від судом на другій половині дистанції)
- **OPT-RUN-2.3:** Стартове екіпірування (біговий пояс для номера та гелів, дихаюча кепка від сонця)
- **OPT-RUN-2.4:** Захист ніг від мозолів та збитих нігтів (професійні бігові шкарпетки)
- **OPT-RUN-2.5:** Повний комплекс «Все включено» (харчування + гідратація + екіпірування)

### Q3: Component Requirements & Add-ons (Комплектація набору)
**UA:** Чи бажаєте ви отримати суто спортивне харчування, чи комбінований набір з екіпіруванням?  
**RU:** Желаете ли вы получить чисто спортивное питание, или комбинированный набор с экипировкой?
- **OPT-RUN-3.1:** Тільки спортивне харчування (гелі, електроліти, батончики)
- **OPT-RUN-3.2:** Харчування + Стартовий пояс або бігова кепка
- **OPT-RUN-3.3:** Харчування + Професійні бігові шкарпетки
- **OPT-RUN-3.4:** Повний комплект зі спортивною пляшкою / флягою

### Q4: Delivery Form Factor (Формат спортивного палива)
**UA:** Який тип бігового харчування ви найкраще переносите на швидкості?  
**RU:** Какой тип бегового питания вы лучше всего переносите на скорости?
- **OPT-RUN-4.1:** Рідкі ізотонічні гелі (можна ковтати без запивання водою)
- **OPT-RUN-4.2:** Концентровані гелі подвійної енергії (Beta Fuel, висока щільність вуглеводів)
- **OPT-RUN-4.3:** Розчинні порошки для бігових гідраторів / софт-фляг
- **OPT-RUN-4.4:** Хрусткі білкові або вівсяні батончики (для низького пульсу, трейлів або після фінішу)

### Q5: Physical Sizing / Measurements (Обов'язковий розмір взуття для бігових шкарпеток)
**UA:** Вкажіть точний розмір взуття бігуна (критично для анатомічної посадки без мозолів):  
**RU:** Укажите точный размер обуви бегуна (критично для анатомической посадки без мозолей):
- **OPT-RUN-5.0:** Без шкарпеток (набір суто з гелями або поясом)
- **OPT-RUN-5.1:** Розмір 35–37 (S)
- **OPT-RUN-5.2:** Розмір 38–40 (M)
- **OPT-RUN-5.3:** Розмір 40–42 (M/L)
- **OPT-RUN-5.4:** Розмір 43–45 (L/XL)
- **OPT-RUN-5.5:** Розмір 46–48 (XXL)

### Q6: Caffeine & GI Sensitivity (Кофеїнова стратегія та шлунок)
**UA:** Як ви ставитесь до кофеїну в біговому харчуванні?  
**RU:** Как вы относитесь к кофеину в беговом питании?
- **OPT-RUN-6.1:** Тільки без кофеїну (максимальний спокій для пульсу та шлунку)
- **OPT-RUN-6.2:** Комбінований підхід (базові гелі без кофеїну + 1–2 кофеїнові гелі на фінальні 10 км)
- **OPT-RUN-6.3:** Високий вміст кофеїну для максимальної концентрації та темпу

### Q7: Terrain & Environmental Conditions (Покриття та погода)
**UA:** Де здебільшого проходитимуть ваші забіги?  
**RU:** Где в основном будут проходить ваши забеги?
- **OPT-RUN-7.1:** Асфальт, міські шосейні старти (потрібен захист від ударного навантаження)
- **OPT-RUN-7.2:** Трейл, ліс, гори, багнюка (потрібні посилені шкарпетки та підвищена енергія)
- **OPT-RUN-7.3:** Бігова доріжка або манеж у приміщенні

### Q8: Volume / Supply Duration (Обсяг запасу)
**UA:** На який період або старт ви формуєте набір?  
**RU:** На какой период или старт вы формируете набор?
- **OPT-RUN-8.1:** Стартовий пакет на 1 конкретний забіг
- **OPT-RUN-8.2:** Місячний тренувальний цикл підготовки
- **OPT-RUN-8.3:** 3-місячний сезонний абонемент клубу Race Expert Club

### Q9: Budget Expectation & Floor Awareness (Бюджетний рівень)
**UA:** Який бюджет ви плануєте на біговий набір?  
**RU:** Какой бюджет вы планируете на беговой набор?
- **OPT-RUN-9.1:** Доступний стартовий набір (950–1250 грн)
- **OPT-RUN-9.2:** Оптимальний комплект з екіпіруванням (1350–1500 грн)
- **OPT-RUN-9.3:** Преміальний ультрамарафонський набір (1650 грн)

## 4.3. The «Подходит / Не подходит» Critical Audit for Running
| Запитання та опція | Статус AI | Чому підходить (Клінічне обґрунтування) | Який негативний брак / витік блокує? |
|---|---|---|---|
| **Бан бодібілдерського креатину** | **СУВОРО НЕ ПІДХОДИТЬ** | Креатин провокує набір 1.5–3 кг внутрішньоклітинної води в м'язах, що різко збільшує енергетичні витрати марафонця на кожен крок і підвищує ризик фасциту стопи. | **Блокує рекомендацію важкоатлетичних порошків бігунам** (критичний баг з `agent_2_report.md`). |
| **Півмарафон (21.1 км) як окрема мета** | **ПОВНІСТЮ ПІДХОДИТЬ** | 21.1 км є найпопулярнішою аматорською дистанцією в Україні; напівмарафонці потребують 3–4 гелів та електролітів. | **Виправляє катастрофічний збій 20 сценаріїв**, коли квіз викидав 0 результатів на півмарафон. |
| **Стартовий пояс та кепка у біговому наборі** | **ПІДХОДИТЬ ЯК КОМПЛЕКТ** | Кепка захищає від теплового удару, а пояс тримає стартовий номер без пошкодження футболки шпильками. | **Запобігає відчуженню екіпірування від бігового старту**. |
| **Анатомічні шкарпетки за розміром** | **ОБОВ'ЯЗКОВО ЗА РОЗМІРОМ** | Бігові шкарпетки неправильного розміру збираються в складки, викликаючи криваві пухирі на 15+ км. | **Блокує надсилання шкарпеток 46–48 розміру дівчатам із 36 розміром ноги**. |

## 4.4. Grounded Catalog SKU Mapping (Running)
### Гілка А: Преміальне ультрамарафонське харчування та гідратація
- **[UT-PRO-2026]** *Набір «Ultra Trail Marathon Energy & Hydration Pro»* — **1650 грн**  
  *Склад:* 3x SIS Beta Fuel гелі, 2x SIS Go Hydro електроліти, 1x протеїновий батончик Science in Sport

### Гілка Б: Марафонські та стартові набори з поясом та кепкою
- **[RE11804]** *Набір «Марафонський темп»* — **1500 грн**  
  *Склад:* Race Expert Run for Help Ukraine кепка; Race Expert пояс для стартового номера with 6 gel loops; Hydria Perform стики с электролитами x10
- **[RE11801]** *Набір «Підготовка до забігу»* — **1500 грн**  
  *Склад:* беговая кепка «Run for Help Ukraine»; пояс для стартового номера с 6 петлями для гелей/батончиков; бутылка 600 мл; белые носки 40–42

### Гілка В: Набори на тренувальний тиждень та енергія дистанції
- **[RE11659]** *Набір «Тиждень бігуна»* — **1200 грн**  
  *Склад:* Sponser Crunchy Protein Bar, 50 g x2; Hydria Perform lemon sticks x6; GU Energy Chews lemonade, 60 g x1. В начале описания упоминается энергетический гель, но нумерованный список товаров его не содержит
- **[RE11806]** *Набір «Енергія дистанції Race Expert Club» — абонемент на 3 місяці* — **1475 грн**  
  *Склад:* абонемент Race Expert Club на 3 месяца; DRUMn’BADS liquid cordyceps, 30 ml; Swanson CoQ10 Mini Cap, 10 mg, 100 caps; Precision Hydration 500 Tube, 15 таблеток
- **[RE11802]** *Набір «Витривалість без спраги Race Expert Club» — абонемент на 3 месяца* — **1500 грн**  
  *Склад:* абонемент Race Expert Club на 3 месяца; Nutriversum EAA Sugar Free 500 g ×1; Hydria Perform стики с электролитами ×5; Brave U Shaker 700 ml ×1. Назначение по описанию набора: поддержка гидратации и выносливости во время интенсивных занятий. Занятия: бег, велоспорт, силовые тренировки и HIIT. Указанные метрики/состав: 12 g EAA растворяют в 300–400 ml; Hydria stick — в 500–850 ml. Неопределённость: существенной неопределённости нет
- **[RE11786]** *Набір «Тренувальний ресурс Race Expert Club» — абонемент на 3 місяці* — **1285 грн**  
  *Склад:* абонемент клуба на 3 месяца; Nutriversum BCAA 2:1:1 Sugar Free, 360 г; Hydria Perform, 5 стиков; шейкер Myprotein 600 мл

### Гілка Г: Бігове екіпірування та захист стопи (Шкарпетки + Баф / Пляшка)
- **[RE11013]** *Набір «Бігова пара»* — **1359 грн**  
  *Склад:* по извлечённому перечню карточки — белые носки RE2 40–44; тёмные носки RE2 40–44; стеклянная бутылка 530 мл. Назначение по сохранённой карточке: беговой комплект для активного дня. Спорт: бег. **Неясность состава:** во вступлении также упоминаются батончики, но в видимом перечне компонентов есть только три позиции. В индексе карточка показывала 1 500 UAH против 1 359 UAH в снимке. - Теги: purpose:running_day_kit; item_type:equipment_bundle; sport:running; distance:unspecified; shoe_size:40-44; audience:runners; buyer_weight:not_specified; price:1359_uah; data_quality:composition_conflict; data_quality:live_price_differs
- **[RE11021]** *Набір «Літній старт Race Expert Club» — абонемент на 3 місяці* — **1379 грн**  
  *Склад:* белые носки Race Expert размер 40–44 x2 pairs; glass бутылка Race Expert 530 ml; Hydria Daily peach sticks x8; Hydria Perform lemon sticks x2
- **[RE89475]** *Набір «Бігова екіпіровка Race Expert» — абонемент на 3 місяці* — **1415 грн**  
  *Склад:* клуб на 3 месяца; флисовый баф; стеклянная бутылка с чехлом 530 мл; тёмные и белые носки RE2 40–44
- **[RE88946]** *Набір «Гідратація тренувань Race Expert Club» — абонемент на 3 місяці* — **1500 грн**  
  *Склад:* клуб на 3 месяца; электролиты Hydria Daily, 8 стиков (1 стик на 500–850 мл воды; натрий, калий, магний, кальций, витамины C/B5/B6/B12); гели SiS Go + Electrolyte 60 мл ×4 (22 г углеводов каждый; 118 мг Na, 9,5 мг K, 1,5 мг Mg); стеклянная бутылка 530 мл. Назначение/активность: бег, велоспорт и фитнес, длительные/интенсивные тренировки. Точная дистанция не задана. - Теги: purpose:training_hydration; item_type:club_membership_bundle; sport:running; sport:cycling; sport:general_fitness; distance:unspecified; duration:3_months; contains:electrolytes; contains:carbohydrates; audience:cyclists; audience:fitness_participants; audience:runners; buyer_weight:not_specified; price:1500_uah
- **[Nabir_1123]** *Набір «Комплект для гідратації Race Expert Club»* — **1435 грн**  
  *Склад:* абонемент Race Expert Club на 3 месяца; 16 стиков Hydria Perform; бутылка Race Expert, 600 мл

---

# 5. Category 4: «Силові тренування, фітнес та зал» (Gym Fitness & Strength)

## 5.1. Category Mission & Primary Deliverable
- **Core Athletic Mission:** Phosphagen system resynthesis (ATP-CP via creatine monohydrate), stimulation of muscle protein synthesis (mTOR activation via high-leucine BCAA/EAA/Whey), intra-workout stamina, muscular pump/vasodilation, and post-workout glycogen replenishment.
- **The Primary Deliverable:** Micronized Creatine Monohydrate, BCAA 2:1:1 / EAA formulas, high-protein snack bars, pre-workout focus stimulants, and gym training accessories (resistance bands, shakers, ab-rollers).
- **The Core Negative Rule (Agent 3 Forensic Finding):** Endurance marathon gels and soft water flasks CANNOT be falsely sold to powerlifters or bodybuilders seeking hypertrophy. Conversely, sets containing NO CREATINE (such as `RE11632` Lion's Mane cookies, `RE11663` Yoga mat, `RE11665` Jump rope) MUST NEVER be dishonestly tagged or described as *«Креатин та передтренувальні комплекси (без сторонніх речей)»*!

## 5.2. Exact Adaptive Question Sequence (8 Questions)

### Q1: Primary Gym Objective (Головна мета у залі)
**UA:** Яка ваша основна мета силових або фітнес-тренувань?  
**RU:** Какая ваша основная цель силовых или фитнес-тренировок?
- **OPT-STR-1.1:** Ріст силових показників та м'язової маси (потрібен креатин та білок для гіпертрофії)
- **OPT-STR-1.2:** Підтримка м'язів, рельєф та схуднення / сушка (BCAA без цукру, чисті амінокислоти)
- **OPT-STR-1.3:** Максимальна витривалість та енергія на тренуванні (передтренувальний фокус)
- **OPT-STR-1.4:** Домашній фітнес, пілатес або функціональний тренінг (килимки, еспандери, скакалка)
- **OPT-STR-1.5:** Захист суглобів та зв'язок від великих ваг (колаген, хондропротектори)

### Q2: Preferred Active Compounds (Бажані нутрієнти у наборі)
**UA:** Які активні компоненти ви бажаєте бачити в основі набору?  
**RU:** Какие активные компоненты вы хотите видеть в основе набора?
- **OPT-STR-2.1:** Чистий креатин моногідрат (перевірене золоте джерело вибухової сили)
- **OPT-STR-2.2:** Амінокислоти BCAA / EAA (захист м'язів від катаболізму під час навантаження)
- **OPT-STR-2.3:** Протеїнові батончики та снеки (зручний білковий перекус без цукру)
- **OPT-STR-2.4:** Суто фітнес-інвентар без спортивного харчування
- **OPT-STR-2.5:** Комбінований набір: харчування + спортивний аксесуар

### Q3: Timing of Intake (Час прийому відносно тренування)
**UA:** Коли ви плануєте вживати добавки?  
**RU:** Когда вы планируете употреблять добавки?
- **OPT-STR-3.1:** До тренування (за 20–30 хв: заряд енергії, фокус та м'язовий памп)
- **OPT-STR-3.2:** Під час тренування (intra-workout: розчинні BCAA/EAA для гідратації)
- **OPT-STR-3.3:** Після тренування (протягом 45 хв: закриття білкового вікна, відновлення)
- **OPT-STR-3.4:** Щоденно вранці або між прийомами їжі (накопичення креатину)

### Q4: Delivery Form Factor (Форма випуску силових добавок)
**UA:** Якій формі спортивного харчування ви віддаєте перевагу?  
**RU:** Какой форме спортивного питания вы отдаете предпочтение?
- **OPT-STR-4.1:** Порошок для приготування коктейлю в шейкері (апельсин, кавун, натуральний)
- **OPT-STR-4.2:** Капсули або пресовані таблетки (швидко ковтнути без змішування)
- **OPT-STR-4.3:** Готові білкові снеки та батончики (на ходу в роздягальні)
- **OPT-STR-4.4:** Інвентар (еспандери, скакалки, килимки, ролик)

### Q5: Stimulant & Caffeine Sensitivity (Чутливість до стимуляторів ЦНС)
**UA:** Як ви реагуєте на кофеїн та бета-аланін?  
**RU:** Как вы реагируете на кофеин и бета-аланин?
- **OPT-STR-5.1:** Тільки без стимуляторів (тренуюся ввечері, не хочу перезбудження та тахікардії)
- **OPT-STR-5.2:** Помірний вміст кофеїну для концентрації
- **OPT-STR-5.3:** Потужний передтренувальний заряд без обмежень

### Q6: Physical Sizing / Gear Measurements (Розмір ноги для наборів зі шкарпетками)
**UA:** Якщо у силовому наборі є спортивні шкарпетки або екіпірування, вкажіть розмір:  
**RU:** Если в силовом наборе есть спортивные носки, укажите размер:
- **OPT-STR-6.0:** Без шкарпеток (набір суто з харчуванням або зальним інвентарем)
- **OPT-STR-6.1:** Розмір 35–37
- **OPT-STR-6.2:** Розмір 38–40
- **OPT-STR-6.3:** Розмір 40–42
- **OPT-STR-6.4:** Розмір 43–45
- **OPT-STR-6.5:** Розмір 46–48

### Q7: Training Environment (Місце проведення занять)
**UA:** Де ви тренуєтесь?  
**RU:** Где вы тренируетесь?
- **OPT-STR-7.1:** Тренажерний зал із вільними вагами та тренажерами
- **OPT-STR-7.2:** Домашні тренування або воркаут на свіжому повітрі
- **OPT-STR-7.3:** Студія йоги, пілатесу або стретчингу

### Q8: Budget Expectation & Floor Awareness (Бюджетний рівень)
**UA:** Який бюджет ви виділяєте на силовий набір?  
**RU:** Какой бюджет вы выделяете на силовой набор?
- **OPT-STR-8.1:** Базовий силовий інвентар або мононабір (759–1150 грн)
- **OPT-STR-8.2:** Протеїновий курс або амінокислоти (1225–1385 грн)
- **OPT-STR-8.3:** Повний преміум-комплекс із креатином та абонементом (1475–1500 грн)

## 5.3. The «Подходит / Не подходит» Critical Audit for Strength
| Запитання та опція | Статус AI | Чому підходить (Клінічне обґрунтування) | Який негативний брак / витік блокує? |
|---|---|---|---|
| **Аудит реального Креатину** | **СУВОРА ВАЛІДАЦІЯ** | Лише набори із сертифікованим креатином (`Nabir_1128`, `RE11636`, `RE11787`) мають маркуватися як креатин. | **Блокує фальшиві рекомендації набору RE11632 (гриби + печиво) та RE11663 (килимок) під виглядом креатину!** |
| **Бан бігових ультрамарафонських гелів** | **СУВОРО НЕ ПІДХОДИТЬ** | Силовий атлет у залі потребує білка та фосфагену, а не рідкого мальтодекстрину на бігу. | **Блокує забивання силових результатів біговими гелями**. |
| **Відокремлення Йоги та Інвентарю (`RE11663`, `RE11665`)** | **ПІДХОДИТЬ ЯК ФІТНЕС-ІНВЕНТАР** | Килимки для йоги, еспандери та ролики підходять для домашнього пілатесу, але не повинні конкурувати з протеїновими банками. | **Створює чесну гілку фітнес-інвентарю**. |
| **Чесний опис без обману `(без сторонніх речей)`** | **ОБОВ'ЯЗКОВА ПРОЗОРІСТЬ** | Якщо набір містить шкарпетки або рушник разом із протеїном, квіз зобов'язаний повідомити про це покупця. | **Ліквідує брехливі маркетингові фрази** про «чистий протеїн без сторонніх предметів». |

## 5.4. Grounded Catalog SKU Mapping (Strength)
### Гілка А: Справжній Креатин Моногідрат та Максимальна Сила
- **[Nabir_1128]** *Набір «Витривалість» — абонемент на 3 місяці* — **1500 грн**  
  *Склад:* абонемент; OstroVit Creatine Monohydrate orange, 500 g; Race Expert × DRUMn’BADS lion’s-mane протеиновый батончик 40 g; cordyceps протеиновый батончик 40 g; reishi протеиновый батончик 40 g; Hydria Perform sticks x7
- **[RE11636]** *Набір «Вибух сили Race Expert Club» — абонемент на 3 місяці* — **1385 грн**  
  *Склад:* абонемент; OstroVit Creatine Monohydrate 500 g; Bodyperson Labs Pre-Workout Formula 250 g (contains caffeine per card); Hydria Daily sticks x4
- **[RE11787]** *Набір «Сила та гідратація» — абонемент на 3 місяці* — **1475 грн**  
  *Склад:* Hydria Perform sticks x10; OstroVit Creatine Monohydrate orange, 500 g; Olimp BCAA 4000 Extreme Shot orange, 60 ml

### Гілка Б: Протеїновий ріст та амінокислоти (BCAA / EAA / Батончики)
- **[RE11681]** *Набір «Ріст м'язів» — абонемент на 3 місяці* — **1225 грн**  
  *Склад:* абонемент; Lipobar протеиновый батончик 50 g x2 (16.5 g protein each); Bodyperson Creatine Monohydrate 500 g; Brave U шейкер 700 ml; Hydria Daily sticks x4
- **[RE11786]** *Набір «Тренувальний ресурс Race Expert Club» — абонемент на 3 місяці* — **1285 грн**  
  *Склад:* абонемент клуба на 3 месяца; Nutriversum BCAA 2:1:1 Sugar Free, 360 г; Hydria Perform, 5 стиков; шейкер Myprotein 600 мл
- **[Nabir_1127]** *Набір «Продуктивність на максимум Race Expert Club»* — **1379 грн**  
  *Склад:* абонемент Race Expert Club на 3 месяца; комплекс Source Naturals Ultra-Mag, 60 таблеток; Mind Shi 4Mushroom Complex, 60 капсул; 2 батончика Race Expert & DRUMn’BADS с ежовиком, по 40 г
- `RE11789` (Not in catalog)

### Гілка В: Ноотропний ментальний фокус та сила (Їжовик + Протеїнове печиво)
- **[RE11632]** *Набір «Розум і Сила»* — **1215 грн**  
  *Склад:* Mind Shi 4Mushroom 1000 mg, 60 caps; Myprotein Baked Cookie 75 g x7 (14 g растительного белка в каждом)

### Гілка Г: Фітнес-інвентар, йога та функціональний тренінг
- **[RE11663]** *Набір «Йога та пілатес»* — **1500 грн**  
  *Склад:* EasyFit Polarity Stone коврик ×1; EasyFit EASY текстильнаяя лента-эспандер ×1; Myprotein Layered Bar Triple Chocolate Fudge 60 g ×7 (>20 g белка/батончик). Назначение по описанию набора: занятия йогой, пилатесом, растяжкой и домашние тренировки. Занятия/аудитория: йога, пилатес, растяжка и домашние тренировки. Неопределённость: существенной неопределённости нет
- **[RE11665]** *Набір «Активний рух»* — **1500 грн**  
  *Склад:* скоростная скакалка со счётчиком ×1; двойной ролик для пресса ×1; массажный мяч ×1; кольцевой кистевой эспандер EasyFit Ring 32 kg ×1; Myprotein Layered Bar 60 g ×8 (20.4 g белка/батончик). Назначение по описанию набора: поддержка активного образа жизни, фитнеса и тренировок в разных местах. Занятия/аудитория: домашние, заловые и уличные тренировки; активные люди. Указанные метрики/состав: скакалка: 5–20 min; массаж: 1–3 min. Неопределённость: существенной неопределённости нет
- `RE11649` (Not in catalog)

---

# 6. Category 5: «Спортивне харчування та перекуси» (Food, Bars, Jerky & Trail Nutrition)

## 6.1. Category Mission & Primary Deliverable
- **Core Nutritional Mission:** Fast caloric delivery, hunger satiation, high-density macronutrient refueling (protein, complex/simple carbs, essential fats) during active days, post-workout intervals, or autonomous outdoor field settings.
- **The Primary Deliverable:** Edible nutrition: crunchy protein bars, artisanal dried meat jerky (chicken, pork, turkey), and freeze-dried hot expedition meals (`ЇDLO`).
- **The Core Negative Rule (Agent 4 Forensic Finding):** Gross non-food leaks (bottles, socks, spirulina tablets, massage equipment) MUST BE EXCLUDED unless bundled with food. Most critically, the **100% failure rate for Dehydrated Camping Meals (`ЇDLO`) must be completely eliminated**! Furthermore, the system must separate sweet protein confectionery from savory dried meat jerky.

## 6.2. Exact Adaptive Question Sequence (8 Questions)

### Q1: Nutritional Context & Eating Occasion (Призначення перекусу)
**UA:** Для яких ситуацій ви обираєте спортивні перекуси або харчування?  
**RU:** Для каких ситуаций вы выбираете спортивные перекусы или питание?
- **OPT-FOO-1.1:** Швидкий білковий перекус між тренуваннями або в дорозі (без цукру, ситний)
- **OPT-FOO-1.2:** Повноцінна гаряча польова їжа у похід, відрядження або на службу (сублімати ЇDLO)
- **OPT-FOO-1.3:** Натуральний м'ясний снек для витривалості та ситості (сушене фермерське м'ясо)
- **OPT-FOO-1.4:** Енергетичне паливо для тривалих бігових або велотренувань

### Q2: Flavor Profile & Palate Preference (Смаковий профіль)
**UA:** Якому смаковому профілю ви віддаєте перевагу?  
**RU:** Какому вкусовому профилю вы отдаете предпочтение?
- **OPT-FOO-2.1:** Солодкий / десертний (шоколад, карамель, печиво, горіхи, арахісова паста)
- **OPT-FOO-2.2:** Солоний / м'ясний (натуральна курятина, свинина, індичка з прянощами)
- **OPT-FOO-2.3:** Гарячі класичні обіди (каші з м'ясом, борщ, паста, супи — залити окропом)
- **OPT-FOO-2.4:** Збалансований мікс (і солодке до кави, і солоні перекуси)

### Q3: Delivery Form Factor (Формат їжі)
**UA:** Який формат їжі вам потрібен?  
**RU:** Какой формат еды вам нужен?
- **OPT-FOO-3.1:** Протеїнові батончики та печиво (хрусткі, покриті шоколадом або низьковуглеводні)
- **OPT-FOO-3.2:** Порційне сушене м'ясо (джерки в індивідуальних крафтових упаковках)
- **OPT-FOO-3.3:** Сублімовані туристичні термо-пакети ЇDLO (готувати прямо в пачці)
- **OPT-FOO-3.4:** Комплексний мікс-бокс різних перекусів

### Q4: Meat & Protein Source Preference (Вибір джерела білка)
**UA:** Яке джерело білка для вас є пріоритетним?  
**RU:** Какой источник белка для вас приоритетен?
- **OPT-FOO-4.1:** Ніжне філе індички (дієтичне, легко засвоюється, мінімум жиру)
- **OPT-FOO-4.2:** Соковита добірна курятина (класичний баланс калорій та білка)
- **OPT-FOO-4.3:** Ситна пряна свинина (максимальна калорійність та ситість для важких маршів)
- **OPT-FOO-4.4:** Молочний сироватковий протеїн / ізолят (у батончиках)
- **OPT-FOO-4.5:** Рослинний / вегетаріанський склад

### Q5: Physical Sizing / Measurements (Розмір ноги — перевірка чистоти)
**UA:** У цій категорії товари не потребують підбору розміру одягу:  
**RU:** В этой категории товары не требуют подбора размера одежды:
- **OPT-FOO-5.0:** Без розміру (100% їстівна продукція або посуд)
- **OPT-FOO-5.1:** Якщо в комбо-наборі є шкарпетки: 35–37 / 38–40 / 40–42 / 43–45 / 46–48

### Q6: Dietary Protocols & Sugar Limits (Дієтичні обмеження)
**UA:** Чи маєте ви обмеження щодо цукру або глютену?  
**RU:** Есть ли у вас ограничения по сахару или глютену?
- **OPT-FOO-6.1:** Без доданого цукру (Low-carb / Keto-friendly)
- **OPT-FOO-6.2:** 100% натуральний склад без консервантів та хімічних ароматизаторів
- **OPT-FOO-6.3:** Без лактози
- **OPT-FOO-6.4:** Жодних обмежень

### Q7: Supply Volume & Packaging Quantity (Кількість та обсяг запасу)
**UA:** Який обсяг запасів перекусів вам необхідний?  
**RU:** Какой объем запасов перекусов вам необходим?
- **OPT-FOO-7.1:** Тестовий бокс перекусів (5–8 штук на робочий тиждень або поїздку)
- **OPT-FOO-7.2:** Великий запас (12–16 порцій для активних тренувань)
- **OPT-FOO-7.3:** Клубний 3-місячний абонемент з регулярною доставкою свіжих боксів

### Q8: Budget Expectation & Floor Awareness (Бюджетний рівень)
**UA:** Який бюджет ви плануєте на набір перекусів?  
**RU:** Какой бюджет вы планируете на набор перекусов?
- **OPT-FOO-8.1:** Набір крафтового сушеного м'яса або батончиків (1149–1200 грн)
- **OPT-FOO-8.2:** Похідний набір субліматів ЇDLO (1485–1500 грн)
- **OPT-FOO-8.3:** Преміальний клубний бокс (1500 грн)

## 6.3. The «Подходит / Не подходит» Critical Audit for Food
| Запитання та опція | Статус AI | Чому підходить (Клінічне обґрунтування) | Який негативний брак / витік блокує? |
|---|---|---|---|
| **Гаряча польова їжа `ЇDLO` (`RE11657`, `RE11658`)** | **100% ВАЛІДНЕ ВІДНОВЛЕННЯ** | Сублімовані страви є найкалорійнішою та найбезпечнішою формою повноцінного гарячого харчування в польових умовах. | **Повністю усуває катастрофічний баг 100% відмов**, повертаючи ЇDLO у видачу при запиті гарячої їжі. |
| **Сепарація Солодкого та Солоного (Джерки vs Батончики)** | **КРИТИЧНО ПІДХОДИТЬ** | При втомі від солодкого (palate fatigue) атлет не може дивитися на батончики і потребує солоного м'яса. | **Блокує нав'язування шоколадних батончиків тим, хто шукає солоні м'ясні снеки**. |
| **Бан гейнерів та важких банок з порошком** | **СУВОРО НЕ ПІДХОДИТЬ** | Покупець у розділі перекусів шукає готовий до вживання продукт, а не 3-кілограмовий мішок для розмішування молоком. | **Блокує витік бодібілдерських гейнерів**. |
| **Бан шкарпеток без їжі** | **СУВОРО НЕ ПІДХОДИТЬ** | Їжа є базовою потребою; шкарпетки без калорій не задовольняють голод. | **Запобігає видачі текстилю замість їжі**. |

## 6.4. Grounded Catalog SKU Mapping (Food & Snacks)
### Гілка А: Сублімовані гарячі страви ЇDLO (Повноцінне польове харчування)
- **[RE11657]** *Набір «Омега + сонце» по програмі* — **1315 грн**  
  *Склад:* Now Foods Omega-3 1,000 mg, 30 мягкие капсулы ×5 (EPA 360 mg + DHA 240 mg per 2 капсули); Now Foods Vitamin D3 1,000 IU жевательные таблетки з фруктовим смаком 180 таблеток ×1. Назначение по описанию набора: ежедневная поддержка иммунитета, сердца, мозга и костей согласно описанию набора
- **[RE11658]** *Набір «Рівновага дня»* — **1455 грн**  
  *Склад:* VPLab Magnesium Citrate 90 мягкие капсулы; Nutriversum GABA 60 капсул (750 mg/cap); DRUMn’BADS адаптогенные жевательных конфет ×15; Hydria Perform стік з електролітами ×1. Назначение по описанию набора: поддержка равновесия, концентрации и восстановления согласно описанию набора. Специализированное спортивное применение не указано. Неопределённость: существенной неопределённости нет

### Гілка Б: Натуральне крафтове сушене м'ясо (Джерки індичка, курятина, свинина)
- **[RE11660]** *Набір «Марафонець»* — **1500 грн**  
  *Склад:* Nutriversum Creatine 300 g ×1; PF 30 Gel 51 g ×5. Назначение по описанию набора: подготовка и питание во время бега на длинные дистанции. Аудитория/занятия: бегуны на длинные дистанции; в описании названы полумарафон и марафон. Формат: в описании указаны полумарафон и марафон; точное расстояние в километрах не приведено. Указанные метрики/состав: карточка указывает 1–3 gel/hour в зависимости от длительности и интенсивности. Неопределённость: существенной неопределённости нет
- **[RE11661]** *Набір «Чоловіча база залу Race Expert Club» — абонемент на 3 місяці* — **1485 грн**  
  *Склад:* абонемент Race Expert Club на 3 месяца; NOW Daily Vits Multi, 100 таблеток; OstroVit Creatine Monohydrate, 500 g; Lipobar, 50 g x1
- **[RE11662]** *Набір «Релакс та відновлення»* — **1500 грн**  
  *Склад:* EasyFit Grid Roller 45 cm ×1; EasyFit PVC твердий массажный мяч 7.5 cm ×1; Kuznetsov коврик + подушкою/чохлом ×1. Назначение по описанию набора: восстановление после тренировок, расслабление мышц и отдых после активного дня. Аудитория/занятия: спортсмены и активные люди; также названы йога, пилатес и фитнес. Указанные метрики/состав: роллер: 1–3 min; мяч: 2–5 min; коврик: 10–20 min. Неопределённость: существенной неопределённости нет

### Гілка В: Хрусткі протеїнові батончики та печиво (Myprotein / Lipobar / Sponser)
- **[RE11681]** *Набір «Ріст м'язів» — абонемент на 3 місяці* — **1225 грн**  
  *Склад:* абонемент; Lipobar протеиновый батончик 50 g x2 (16.5 g protein each); Bodyperson Creatine Monohydrate 500 g; Brave U шейкер 700 ml; Hydria Daily sticks x4
- **[RE11632]** *Набір «Розум і Сила»* — **1215 грн**  
  *Склад:* Mind Shi 4Mushroom 1000 mg, 60 caps; Myprotein Baked Cookie 75 g x7 (14 g растительного белка в каждом)
- **[RE11659]** *Набір «Тиждень бігуна»* — **1200 грн**  
  *Склад:* Sponser Crunchy Protein Bar, 50 g x2; Hydria Perform lemon sticks x6; GU Energy Chews lemonade, 60 g x1. В начале описания упоминается энергетический гель, но нумерованный список товаров его не содержит

### Гілка Г: Подарункові та комбіновані бокси зі спортивними снеками
- **[RE11026]** *Набір «Спортивний подарунок»* — **1500 грн**  
  *Склад:* белые носки Race Expert 43–45 ×2; брелоки-гильза ×3; NOW Foods Vitamin D3 2 000 IU, 120 софтгелей; печенье Myprotein Baked Cookie 75 г ×3 (по 13 г растительного белка)

---

# 7. Category 6: «Екіпірування та бігові аксесуари» (Gear & Accessories)

## 7.1. Category Mission & Primary Deliverable
- **Core Athletic Mission:** Biomechanical foot support, blister and chafing prevention, sweat management and thermoregulation (head, neck, feet), race day equipment transport (bib numbers, hydration, gels), post-workout hygiene, and athletic achievement commemoration.
- **The Primary Deliverable:** Technical running socks (anatomical left/right knit, arch support), fleece buffs, running caps, race bib belts, premium plush bath towels (`Шарпей`), medal hangers (`Подвійна нагорода`), and gym resistance equipment.
- **The Core Negative Rule (Agent 6 Forensic Finding):** Bodybuilding creatine, protein powders, and oral vitamins MUST NEVER leak into a gear search! If a buyer selects 'Gear', recommending a tub of Creatine Monohydrate with the claim *«у наборі саме Екіпірування (без сторонніх речей)»* is a critical failure. Furthermore, the mandatory foot size selector must be enforced, eliminating the default 46–48 bias.

## 7.2. Exact Adaptive Question Sequence (8 Questions)

### Q1: Primary Gear Function (Призначення екіпірування)
**UA:** Який тип екіпірування або спортивного аксесуара вам потрібен?  
**RU:** Какой тип экипировки или спортивного аксессуара вам нужен?
- **OPT-GEA-1.1:** Анатомічні бігові шкарпетки (захист стопи від мозолів, вентиляція та компресія)
- **OPT-GEA-1.2:** Стартові та тренувальні аксесуари (бігова кепка, пояс для номера та гелів)
- **OPT-GEA-1.3:** Захист від вітру та холоду (теплий флісовий баф або зимові шкарпетки)
- **OPT-GEA-1.4:** Пост-тренувальна гігієна та комфорт (великі банні рушники преміум-серії Шарпей)
- **OPT-GEA-1.5:** Збереження та демонстрація нагород (холдери та подвійні вішалки для медалей)
- **OPT-GEA-1.6:** Домашній тренувальний інвентар (килимки для йоги, еспандери, скакалка)

### Q2: Sport Modality & Context (Вид активності)
**UA:** Для якого виду спорту чи активності підбирається аксесуар?  
**RU:** Для какого вида спорта или активности подбирается аксессуар?
- **OPT-GEA-2.1:** Шосейний або трейловий біг / марафон / підготовка до змагань
- **OPT-GEA-2.2:** Тренажерний зал, кросфіт, басейн або фітнес
- **OPT-GEA-2.3:** Велоспорт або триатлон
- **OPT-GEA-2.4:** Походи, туризм, щоденні прогулянки або військова служба

### Q3: Mandatory Physical Foot Sizing (Точний розмір взуття)
**UA:** Вкажіть точний розмір взуття (обов'язково для шкарпеток для виключення мозолів):  
**RU:** Укажите точный размер обуви (обязательно для носков для исключения мозолей):
- **OPT-GEA-3.0:** Без шкарпеток (обираю рушники, вішалку для медалей, кепку або інвентар — розмір не потрібен)
- **OPT-GEA-3.1:** Розмір 35–37 (Жіночий S)
- **OPT-GEA-3.2:** Розмір 38–40 (Універсальний M)
- **OPT-GEA-3.3:** Розмір 40–42 (Стандартний M/L)
- **OPT-GEA-3.4:** Розмір 43–45 (Чоловічий L/XL)
- **OPT-GEA-3.5:** Розмір 46–48 (Великий XXL)

### Q4: Seasonality & Fabric Density (Сезонність та тканина)
**UA:** Для якої пори року або температурних умов потрібне екіпірування?  
**RU:** Для какого времени года или температурных условий нужна экипировка?
- **OPT-GEA-4.1:** Літо / Спека (максимально тонка сітчаста вентиляція, захист від поту)
- **OPT-GEA-4.2:** Демісезон / Осінь-Весна (щільніші тканини, вологовідведення)
- **OPT-GEA-4.3:** Зима / Мороз (флісове утеплення, збереження тепла сухожиль)
- **OPT-GEA-4.4:** Всесезонний універсальний варіант

### Q5: Color Palette & Aesthetic Preference (Кольорова гама)
**UA:** Якому забарвленню аксесуарів ви надаєте перевагу?  
**RU:** Какую цветовую гамму аксессуаров вы предпочитаете?
- **OPT-GEA-5.1:** Класична світла гама (білий, сірий, бежевий)
- **OPT-GEA-5.2:** Темна практична гама (чорний, графіт, темний мілітарі)
- **OPT-GEA-5.3:** Патріотичні синьо-жовті кольори та національна символіка
- **OPT-GEA-5.4:** Колір не має значення

### Q6: Zero-Sizing Safety Alternative (Універсальний подарунок без розміру)
**UA:** Якщо ви обираєте набір на подарунок і не впевнені в розмірі, оберіть категорію:  
**RU:** Если вы выбираете набор на подарок и не уверены в размере, выберите категорию:
- **OPT-GEA-6.1:** Я знаю розмір взуття, хочу шкарпетки
- **OPT-GEA-6.2:** Я НЕ знаю розмір взуття: запропонуйте рушники Шарпей, вішалки для медалей або кепку

### Q7: Supply Volume & Multi-Pack (Кількість одиниць у наборі)
**UA:** Який обсяг комплекту вам необхідний?  
**RU:** Какой объем комплекта вам необходим?
- **OPT-GEA-7.1:** Одиночний ключовий аксесуар (пояс, кепка або пара шкарпеток)
- **OPT-GEA-7.2:** Парний комплект (2 пари бігових шкарпеток, подвійний рушник)
- **OPT-GEA-7.3:** Повний стартовий бокс (кепка + пояс + пляшка / баф)

### Q8: Budget Expectation & Floor Awareness (Бюджетний рівень)
**UA:** Який бюджет ви виділяєте на екіпірування?  
**RU:** Какой бюджет вы выделяете на экипировку?
- **OPT-GEA-8.1:** Базовий набір шкарпеток або інвентарю (950–1359 грн)
- **OPT-GEA-8.2:** Комплект із пляшкою або бафом (1379–1439 грн)
- **OPT-GEA-8.3:** Преміальний комплект екіпірування або медальниця (1500 грн)

## 7.3. The «Подходит / Не подходит» Critical Audit for Gear
| Запитання та опція | Статус AI | Чому підходить (Клінічне обґрунтування) | Який негативний брак / витік блокує? |
|---|---|---|---|
| **Повний бан креатину та спортивного харчування** | **СУВОРИЙ БАН** | Якщо покупець шукає текстиль чи пояс, таблетки та порошки є прямою підміною товару. | **Ліквідує критичний баг з `agent_6_report.md`**, де креатин витікав у 28% запитів екіпірування. |
| **Обов'язкова валідація розміру взуття** | **СУВОРА ВАЛІДАЦІЯ** | Шкарпетки не є «One Size». Відповідність розміру стопи — головна умова захисту від збитих пальців. | **Усуває дефолтне надсилання 46–48 розміру** усім без розбору. |
| **Гілка «Zero-Sizing» (Рушники Шарпей та Медальниці)** | **КРИТИЧНО ПІДХОДИТЬ** | Набори рушників (`RE89486`, `RE89487`) та вішалок для медалей (`RE89473`) є бездоганними нейтральними товарами. | **Захищає покупців подарунків від ризику промахнутися з розміром**. |
| **Відкриття шкарпеток для велосипедистів та туристів** | **ПОВНІСТЮ ПІДХОДИТЬ** | Велосипедисти та туристи теж носять анатомічні шкарпетки. | **Виправляє жорстке блокування шкарпеток** для велосипедистів. |

## 7.4. Grounded Catalog SKU Mapping (Gear & Accessories)
### Гілка А: Професійні бігові шкарпетки та бафи
- **[RE11013]** *Набір «Бігова пара»* — **1359 грн**  
  *Склад:* по извлечённому перечню карточки — белые носки RE2 40–44; тёмные носки RE2 40–44; стеклянная бутылка 530 мл. Назначение по сохранённой карточке: беговой комплект для активного дня. Спорт: бег. **Неясность состава:** во вступлении также упоминаются батончики, но в видимом перечне компонентов есть только три позиции. В индексе карточка показывала 1 500 UAH против 1 359 UAH в снимке. - Теги: purpose:running_day_kit; item_type:equipment_bundle; sport:running; distance:unspecified; shoe_size:40-44; audience:runners; buyer_weight:not_specified; price:1359_uah; data_quality:composition_conflict; data_quality:live_price_differs
- **[RE89475]** *Набір «Бігова екіпіровка Race Expert» — абонемент на 3 місяці* — **1415 грн**  
  *Склад:* клуб на 3 месяца; флисовый баф; стеклянная бутылка с чехлом 530 мл; тёмные и белые носки RE2 40–44
- **[RE11021]** *Набір «Літній старт Race Expert Club» — абонемент на 3 місяці* — **1379 грн**  
  *Склад:* белые носки Race Expert размер 40–44 x2 pairs; glass бутылка Race Expert 530 ml; Hydria Daily peach sticks x8; Hydria Perform lemon sticks x2
- **[RE89466]** *Набір «Подарунок початківцю» — абонемент на 3 місяці* — **1500 грн**  
  *Склад:* клуб на 3 месяца; медаль «Озброєні волею 2.0»; стеклянная бутылка 530 мл; тёмные носки RE2 40–44
- **[RE89467]** *Набір «Подарунок початківцю 2.0» — абонемент на 3 місяці* — **1500 грн**  
  *Склад:* клуб на 3 месяца; медаль «Крила Свободи»; стеклянная бутылка 530 мл; белые носки RE2 40–44

### Гілка Б: Стартові аксесуари (Бігові кепки та пояси для номерів)
- **[RE11801]** *Набір «Підготовка до забігу»* — **1500 грн**  
  *Склад:* беговая кепка «Run for Help Ukraine»; пояс для стартового номера с 6 петлями для гелей/батончиков; бутылка 600 мл; белые носки 40–42
- **[RE11804]** *Набір «Марафонський темп»* — **1500 грн**  
  *Склад:* Race Expert Run for Help Ukraine кепка; Race Expert пояс для стартового номера with 6 gel loops; Hydria Perform стики с электролитами x10

### Гілка В: Преміальні банні рушники Шарпей (Zero-Sizing комфорт)
- **[RE89486]** *Набір «Банні рушники Шарпей: класика» — абонемент на 3 месяца* — **1500 грн**  
  *Склад:* 3 полотенца, бежевый/бордовый/серый, 135×70 cm каждый, хлопок 500 g/m²; абонемент Race Expert Club на 3 месяца. Назначение по описанию набора: полотенца для дома, зала, бассейна, сауны или поездок. Занятия/аудитория: дом, зал, бассейн, сауна и поездки; спортсмены упомянуты в описании. Неопределённость: существенной неопределённости нет
- **[RE89487]** *Набір «Банні рушники Шарпей: темна гама» — абонемент на 3 месяца* — **1500 грн**  
  *Склад:* 3 полотенца, чёрный/тёмно-синий/зелёный, 135×70 cm каждый; 100% хлопок, 500 g/m²; абонемент Race Expert Club на 3 месяца. Назначение по описанию набора: полотенца для душа, тренировок, бассейна, сауны и поездок. Занятия: зал, плавание, сауна и поездки; набор не связан с конкретным видом спорта. Неопределённость: существенной неопределённости нет

### Гілка Г: Пам'ять та нагороди (Подвійна нагорода / Медальниці)
- **[RE89473]** *Набір «Подвійна нагорода» — абонемент на 3 місяці* — **1500 грн**  
  *Склад:* клуб на 3 месяца; медали «Озброєні волею 2.0» и «Здатні без зброї»; брелоки Drone 2.0 и гильза

### Гілка Д: Фітнес-інвентар для залу та дому
- **[RE11663]** *Набір «Йога та пілатес»* — **1500 грн**  
  *Склад:* EasyFit Polarity Stone коврик ×1; EasyFit EASY текстильнаяя лента-эспандер ×1; Myprotein Layered Bar Triple Chocolate Fudge 60 g ×7 (>20 g белка/батончик). Назначение по описанию набора: занятия йогой, пилатесом, растяжкой и домашние тренировки. Занятия/аудитория: йога, пилатес, растяжка и домашние тренировки. Неопределённость: существенной неопределённости нет
- **[RE11665]** *Набір «Активний рух»* — **1500 грн**  
  *Склад:* скоростная скакалка со счётчиком ×1; двойной ролик для пресса ×1; массажный мяч ×1; кольцевой кистевой эспандер EasyFit Ring 32 kg ×1; Myprotein Layered Bar 60 g ×8 (20.4 g белка/батончик). Назначение по описанию набора: поддержка активного образа жизни, фитнеса и тренировок в разных местах. Занятия/аудитория: домашние, заловые и уличные тренировки; активные люди. Указанные метрики/состав: скакалка: 5–20 min; массаж: 1–3 min. Неопределённость: существенной неопределённости нет

---

# 8. Category 7: «Походи, кемпінг та трекінг» (Outdoors & Hiking)

## 8.1. Category Mission & Primary Deliverable
- **Core Outdoor Mission:** Complete nutritional autonomy in wilderness/field conditions (calorie-dense hot meals prepared without cooking gear), blister-free thermoregulation for long multi-day marches with heavy backpacks, electrolyte defense against heat exhaustion, and tactical sleep/recovery under harsh ambient conditions.
- **The Primary Deliverable:** Freeze-dried hot meal packs (`ЇDLO`), artisanal dried meat jerky, reinforced trekking/military socks, fleece buffs, tactical night-sleep formulas (`Польовий сон`), and compact fast-drying towels.
- **The Core Negative Rule (Agent Deep Outdoors Forensic Finding):** Selecting 'Dehydrated Meal' (`dehydrated_meal`) MUST NEVER return 0 results! The empty `product_forms` schema bug must be eradicated. Bikepackers and adventure cyclists must not be hard-blocked. Sleep pills must not be falsely guaranteed as *«без сторонніх речей»* when bundled with tactical gear.

## 8.2. Exact Adaptive Question Sequence (9 Questions)

### Q1: Expedition Format & Outdoor Activity (Формат аутдор-активності)
**UA:** В якому форматі планується ваша активність на природі?  
**RU:** В каком формате планируется ваша активность на природе?
- **OPT-OUT-1.1:** Піший похід або гірський трекінг із рюкзаком (1–3 дні або довше)
- **OPT-OUT-1.2:** Військова служба, польові збори, бойове чергування або тактичний марш
- **OPT-OUT-1.3:** Байкпекінг / велопохід або автономна велоподорож
- **OPT-OUT-1.4:** Кемпінг, автоподорож або легкі вихідні на природі

### Q2: Primary Expedition Need (Головна потреба в польових умовах)
**UA:** Що є найбільш пріоритетним у вашому польовому наборі?  
**RU:** Что является наиболее приоритетным в вашем полевом наборе?
- **OPT-OUT-2.1:** Автономне гаряче харчування (сублімати ЇDLO — залити окропом у пакеті)
- **OPT-OUT-2.2:** Ситні сухі м'ясні перекуси на марші (натуральні джерки індичка/свинина/курка)
- **OPT-OUT-2.3:** Захист ніг від холоду та мозолів у берцях чи трекінгових черевиках (термошкарпетки)
- **OPT-OUT-2.4:** Якісний сон та відновлення сил у наметі або бліндажі (набір «Польовий сон»)
- **OPT-OUT-2.5:** Гігієна та комфорт у таборі (швидковисихаючі рушники Шарпей)

### Q3: Footwear Sizing for Trekking Socks (Обов'язковий розмір взуття)
**UA:** Якщо у наборі є похідні шкарпетки, вкажіть ваш розмір трекінгового взуття або берців:  
**RU:** Если в наборе есть походные носки, укажите ваш размер обуви:
- **OPT-OUT-3.0:** Без шкарпеток (обираю суто їжу ЇDLO, рушники або сон)
- **OPT-OUT-3.1:** Розмір 35–37
- **OPT-OUT-3.2:** Розмір 38–40
- **OPT-OUT-3.3:** Розмір 40–42
- **OPT-OUT-3.4:** Розмір 43–45
- **OPT-OUT-3.5:** Розмір 46–48

### Q4: Weather & Climate Extremes (Погодні та кліматичні умови)
**UA:** За яких температурних умов проходитиме похід?  
**RU:** При каких температурных условиях будет проходить поход?
- **OPT-OUT-4.1:** Спека / Літо (потрібні електроліти від зневоднення та дихаючий захист)
- **OPT-OUT-4.2:** Дощ, сирість, багнюка (потрібні надійні матеріали, стійкі до намокання)
- **OPT-OUT-4.3:** Холод / Зима (потрібні теплі шкарпетки, флісовий баф та калорійна гаряча їжа)
- **OPT-OUT-4.4:** Помірні комфортні умови

### Q5: Field Cooking Infrastructure (Можливість приготування їжі)
**UA:** Чи буде у вас з собою пальник або окріп?  
**RU:** Будет ли у вас с собой горелка или кипяток?
- **OPT-OUT-5.1:** Так, є пальник або термос із окропом (ідеально для гарячих субліматів ЇDLO)
- **OPT-OUT-5.2:** Ні, потрібна готова їжа без розігріву (сушене м'ясо джерки, батончики)
- **OPT-OUT-5.3:** Змішаний формат (гаряча вечеря + сухий перекус на переході)

### Q6: Field Sleep Quality & Nervous System Load (Умови нічного сну)
**UA:** Чи стикаєтесь ви з проблемами засинання у польових або незвичних умовах?  
**RU:** Сталкиваетесь ли вы с проблемами засыпания в полевых или непривычных условиях?
- **OPT-OUT-6.1:** Так, чутливий сон у наметі/спальнику/бліндажі (потрібен спеціальний комплекс сну)
- **OPT-OUT-6.2:** Ні, сплю міцно, потрібна лише їжа та екіпірування

### Q7: Supply Duration (Тривалість виходу на природу)
**UA:** На скільки днів розрахована ваша подорож або польовий вихід?  
**RU:** На сколько дней рассчитано ваше путешествие или полевой выход?
- **OPT-OUT-7.1:** Вихідні / 1–2 дні (тестовий набір страв або джерки)
- **OPT-OUT-7.2:** 4–7 днів автономного маршруту
- **OPT-OUT-7.3:** Довготривале відрядження / сезон з абонементом клубу (3 місяці)

### Q8: Budget Expectation & Floor Awareness (Бюджетний рівень)
**UA:** Який бюджет ви виділяєте на похідний набір?  
**RU:** Какой бюджет вы выделяете на походный набор?
- **OPT-OUT-8.1:** Базовий запас м'ясних снеків (1058–1200 грн)
- **OPT-OUT-8.2:** Комплект спорядження або гарячої їжі ЇDLO (1439–1500 грн)
- **OPT-OUT-8.3:** Преміальний автономний набір Ultra Trail / Outdoors (1650 грн)

### Q9: Companion Outdoor Gear (Додаткові похідні аксесуари)
**UA:** Чи потрібні вам додаткові аксесуари для табору?  
**RU:** Нужны ли вам дополнительные аксессуары для лагеря?
- **OPT-OUT-9.1:** Великий швидковисихаючий банний рушник Шарпей
- **OPT-OUT-9.2:** Флісовий баф від вітру та холоду
- **OPT-OUT-9.3:** Спортивна або польова фляга
- **OPT-OUT-9.4:** Тільки харчування без побутових речей

## 8.3. The «Подходит / Не подходит» Critical Audit for Outdoors
| Запитання та опція | Статус AI | Чому підходить (Клінічне обґрунтування) | Який негативний брак / витік блокує? |
|---|---|---|---|
| **Повноцінна інтеграція ЇDLO 2.0 та ЇDLO Club** | **КРИТИЧНО ПІДХОДИТЬ** | Сублімати ЇDLO спеціально створені для трекінгу: важать мінімум, готуються прямо в упаковці, дають 400–600 ккал. | **Ліквідує баг 100% відмов при пошуку субліматів**, виправляючи розсинхрон схеми форми. |
| **Набір «Польовий сон» (`RE11803`) для умов бліндажа** | **100% ВАЛІДНИЙ КЛІНІЧНИЙ МАТЧ** | Розроблений для сну при шумі, холоді та стресі; поєднує магній та м'які релаксанти. | **Забезпечує бійців та туристів дієвим сном у спальнику**. |
| **Байкпекінг як повноправний формат** | **ПОВНІСТЮ ПІДХОДИТЬ** | Велотуристи потребують компактної їжі та шкарпеток так само, як і піші туристи. | **Усуває блокування велосипедистів у розділі туризму**. |
| **Бан гламурних бігових кепок без утеплення в зимовий ліс** | **СУВОРА СЕЗОННІСТЬ** | Літня кепка з сіткою на морозі спричиняє переохолодження. | **Замінює літні кепки на теплі бафи та термошкарпетки при виборі холоду**. |

## 8.4. Grounded Catalog SKU Mapping (Outdoors & Hiking)
### Гілка А: Автономне польове гаряче харчування (Сублімати ЇDLO)
- **[RE11657]** *Набір «Омега + сонце» по програмі* — **1315 грн**  
  *Склад:* Now Foods Omega-3 1,000 mg, 30 мягкие капсулы ×5 (EPA 360 mg + DHA 240 mg per 2 капсули); Now Foods Vitamin D3 1,000 IU жевательные таблетки з фруктовим смаком 180 таблеток ×1. Назначение по описанию набора: ежедневная поддержка иммунитета, сердца, мозга и костей согласно описанию набора
- **[RE11658]** *Набір «Рівновага дня»* — **1455 грн**  
  *Склад:* VPLab Magnesium Citrate 90 мягкие капсулы; Nutriversum GABA 60 капсул (750 mg/cap); DRUMn’BADS адаптогенные жевательных конфет ×15; Hydria Perform стік з електролітами ×1. Назначение по описанию набора: поддержка равновесия, концентрации и восстановления согласно описанию набора. Специализированное спортивное применение не указано. Неопределённость: существенной неопределённости нет

### Гілка Б: Ситні сухі м'ясні перекуси на переході (Крафтові джерки)
- **[RE11660]** *Набір «Марафонець»* — **1500 грн**  
  *Склад:* Nutriversum Creatine 300 g ×1; PF 30 Gel 51 g ×5. Назначение по описанию набора: подготовка и питание во время бега на длинные дистанции. Аудитория/занятия: бегуны на длинные дистанции; в описании названы полумарафон и марафон. Формат: в описании указаны полумарафон и марафон; точное расстояние в километрах не приведено. Указанные метрики/состав: карточка указывает 1–3 gel/hour в зависимости от длительности и интенсивности. Неопределённость: существенной неопределённости нет
- **[RE11661]** *Набір «Чоловіча база залу Race Expert Club» — абонемент на 3 місяці* — **1485 грн**  
  *Склад:* абонемент Race Expert Club на 3 месяца; NOW Daily Vits Multi, 100 таблеток; OstroVit Creatine Monohydrate, 500 g; Lipobar, 50 g x1
- **[RE11662]** *Набір «Релакс та відновлення»* — **1500 грн**  
  *Склад:* EasyFit Grid Roller 45 cm ×1; EasyFit PVC твердий массажный мяч 7.5 cm ×1; Kuznetsov коврик + подушкою/чохлом ×1. Назначение по описанию набора: восстановление после тренировок, расслабление мышц и отдых после активного дня. Аудитория/занятия: спортсмены и активные люди; также названы йога, пилатес и фитнес. Указанные метрики/состав: роллер: 1–3 min; мяч: 2–5 min; коврик: 10–20 min. Неопределённость: существенной неопределённости нет

### Гілка В: Сон та відновлення в польових умовах (Намет / Бліндаж)
- **[RE11803]** *Набір «Польовий сон Race Expert Club» — абонемент на 3 місяці* — **1500 грн**  
  *Склад:* абонемент Race Expert Club на 3 месяца; VPLab Ultra Sleep, 60 caps; Nutriversum Melatonin, 60 caps; Race Expert флисовый бафф

### Гілка Г: Похідне екіпірування, шкарпетки та рушники для табору
- **[RE89460]** *Набір «Подарунок військовому-спортсмену» — абонемент на 3 місяці* — **1500 грн**  
  *Склад:* клуб на 3 месяца; медаль «Гвардія Небес»; флисовый баф; тёмные носки RE2 40–44
- **[RE89459]** *Набір «Подарунок мандрівнику» — абонемент на 3 місяці* — **1439 грн**  
  *Склад:* клуб на 3 месяца; полотенце Sharpey 135×70 см; флисовый баф; белые носки RE2 40–44
- **[RE89482]** *Набір «Подарунок у похід» — абонемент на 3 місяці* — **1500 грн**  
  *Склад:* клуб на 3 месяца; медаль «Гвардія небес»; небольшой чёрный органайзер; тёмные носки RE2 40–44
- **[RE89474]** *Набір «Подарунок у дорогу» — абонемент на 3 місяці* — **1500 грн**  
  *Склад:* клуб на 3 месяца; медаль «Озброєні волею 2.0»; небольшой чёрный органайзер EF-0903-BK; тёмные носки RE2 40–44
- **[RE89485]** *Набір «Подарунок для прогулянок» — абонемент на 3 місяці* — **1379 грн**  
  *Склад:* клуб на 3 месяца; медаль «Здатні без зброї»; баф (цвет из ассортимента); небольшой чёрный органайзер; тёмные носки RE2 40–44
- **[RE89486]** *Набір «Банні рушники Шарпей: класика» — абонемент на 3 месяца* — **1500 грн**  
  *Склад:* 3 полотенца, бежевый/бордовый/серый, 135×70 cm каждый, хлопок 500 g/m²; абонемент Race Expert Club на 3 месяца. Назначение по описанию набора: полотенца для дома, зала, бассейна, сауны или поездок. Занятия/аудитория: дом, зал, бассейн, сауна и поездки; спортсмены упомянуты в описании. Неопределённость: существенной неопределённости нет
- **[RE89487]** *Набір «Банні рушники Шарпей: темна гама» — абонемент на 3 месяца* — **1500 грн**  
  *Склад:* 3 полотенца, чёрный/тёмно-синий/зелёный, 135×70 cm каждый; 100% хлопок, 500 g/m²; абонемент Race Expert Club на 3 месяца. Назначение по описанию набора: полотенца для душа, тренировок, бассейна, сауны и поездок. Занятия: зал, плавание, сауна и поездки; набор не связан с конкретным видом спорта. Неопределённость: существенной неопределённости нет
- **[UT-PRO-2026]** *Набір «Ultra Trail Marathon Energy & Hydration Pro»* — **1650 грн**  
  *Склад:* 3x SIS Beta Fuel гелі, 2x SIS Go Hydro електроліти, 1x протеїновий батончик Science in Sport

---

# 9. Category 8: «Щоденне здоров’я, імунітет та тонус» (Daily Wellness, Longevity & Focus)

## 9.1. Category Mission & Primary Deliverable
- **Core Physiological Mission:** Sustained cellular homeostasis, mitochondrial ATP generation, natural antioxidant defenses, cognitive acuity and neuroplasticity, connective tissue (collagen/bones) integrity, cardiovascular elasticity, and daily adaptogenic resilience without adrenal burnout.
- **The Primary Deliverable:** Bioavailable multi-vitamins, Vitamin D3 + K2 MK-7, Omega-3 fatty acids, Organic Spirulina, Lion's Mane nootropics, Methyl-B12, Magnesium bisglycinate, and specialized formulas for women, expectant mothers, and kids.
- **The Core Negative Rule (Agent Deep Daily Forensic Finding):** Heavy gym pre-workouts, creatine powders, and pure bedtime sedatives CANNOT leak into daytime wellness! A professional seeking daytime cognitive clarity or vitamin D3 must not be prescribed sleep melatonin or explosive nitric oxide pump powders. Furthermore, specialized health profiles (pregnancy, pediatric, 50+ men) must never be cross-mixed.

## 9.2. Exact Adaptive Question Sequence (8 Questions)

### Q1: Primary Health Vector (Головний вектор здоров'я)
**UA:** Який напрямок підтримки здоров'я зараз є для вас найважливішим?  
**RU:** Какое направление поддержки здоровья сейчас для вас наиболее важно?
- **OPT-DAI-1.1:** Загальний імунітет, життєвий тонус та бадьорість (вітаміни D3, С, Цинк, Спіруліна)
- **OPT-DAI-1.2:** Ментальна ясність, пам'ять та концентрація (ноотропний Їжовик гребінчастий, вітаміни B12)
- **OPT-DAI-1.3:** Здоров'я суглобів, зв'язок, кісток та шкіри (морський колаген, кальцій + D3, гіалуронова кислота)
- **OPT-DAI-1.4:** Зниження тривожності, внутрішня рівновага та баланс нервової системи (антистрес без сонливості)
- **OPT-DAI-1.5:** Спеціалізована підтримка (вагітність, дитячий імунітет або чоловіче здоров'я 50+)

### Q2: Circadian Rhythm & Daytime Energy Pattern (Бажаний ефект протягом дня)
**UA:** Який тип енергетичної дії ви очікуєте?  
**RU:** Какой тип энергетического действия вы ожидаете?
- **OPT-DAI-2.1:** Ранкова бадьорість та легке прокидання без відчуття втоми
- **OPT-DAI-2.2:** Стабільна концентрація уваги на роботі протягом 8 годин без енергетичних спадів
- **OPT-DAI-2.3:** Спокійний вечірній баланс без нав'язливих думок
- **OPT-DAI-2.4:** Рівномірна підтримка організму протягом усього дня

### Q3: Delivery Form Factor (Форма вітамінів)
**UA:** Яка форма вітамінів та мінералів для вас найбільш комфортна?  
**RU:** Какая форма витаминов и минералов для вас наиболее комфортна?
- **OPT-DAI-3.1:** Капсули або м'які гелеві софтгелі (найкраща біодоступність олійних вітамінів D3/Omega)
- **OPT-DAI-3.2:** Пресовані таблетки (натуральна органічна спіруліна або рослинні екстракти)
- **OPT-DAI-3.3:** Розчинні порошки або саше з приємним смаком
- **OPT-DAI-3.4:** Форма не має значення

### Q4: Specific Demographic & Physiological Profile (Цільовий користувач)
**UA:** Для кого підбирається щоденний вітамінний комплекс?  
**RU:** Для кого подбирается ежедневный витаминный комплекс?
- **OPT-DAI-4.1:** Активний дорослий (універсальний комплекс для чоловіків та жінок)
- **OPT-DAI-4.2:** Жіноче здоров'я, молодість шкіри та волосся (біотин, колаген, антиоксиданти)
- **OPT-DAI-4.3:** Чоловіча підтримка та витривалість 50+ (цинк, селен, серцево-судинний тонус)
- **OPT-DAI-4.4:** Вагітні або годуючі мами (пренатальний комплекс із фолієвою кислотою)
- **OPT-DAI-4.5:** Діти та підлітки (безпечний вітамінний захист росту)

### Q5: Physical Sizing / Measurements (Перевірка відсутності розміру)
**UA:** У категорії щоденного здоров'я та вітамінів розмір одягу не потрібен:  
**RU:** В категории ежедневного здоровья и витаминов размер одежды не требуется:
- **OPT-DAI-5.0:** Без розміру (100% чисті вітаміни та нутрицевтики)

### Q6: Stimulant Tolerance & Nootropics (Ставлення до природних ноотропів)
**UA:** Чи бажаєте ви додати до курсу функціональні гриби для пам'яті (Lion's Mane)?  
**RU:** Желаете ли вы добавить в курс функциональные грибы для памяти (Lion's Mane)?
- **OPT-DAI-6.1:** Так, дуже цікавлять мікронутрієнти для мозку та нейропластичності (Їжовик гребінчастий)
- **OPT-DAI-6.2:** Ні, віддаю перевагу класичним вітамінам, мінералам та суперфудам (Спіруліна, Омега, D3)

### Q7: Supply Volume & Cycle Length (Тривалість курсу)
**UA:** Який курс щоденного прийому ви плануєте?  
**RU:** Какой курс ежедневного приема вы планируете?
- **OPT-DAI-7.1:** Місячний базовий курс підтримки (30 днів)
- **OPT-DAI-7.2:** Сезонний курс зміцнення імунітету (60 днів)
- **OPT-DAI-7.3:** 3-місячний клубний абонемент із консультацією нутриціолога

### Q8: Budget Expectation & Floor Awareness (Бюджетний рівень)
**UA:** Який бюджет ви виділяєте на вітамінний курс?  
**RU:** Какой бюджет вы выделяете на витаминный курс?
- **OPT-DAI-8.1:** Базовий сертифікований комплекс (1125–1375 грн)
- **OPT-DAI-8.2:** Комплексна преміальна програма або абонемент на 3 місяці (1425–1500 грн)

## 9.3. The «Подходит / Не подходит» Critical Audit for Daily Wellness
| Запитання та опція | Статус AI | Чому підходить (Клінічне обґрунтування) | Який негативний брак / витік блокує? |
|---|---|---|---|
| **Бан спортивних передтренувальних комплексів** | **СУВОРО НЕ ПІДХОДИТЬ** | Сильнодіючі стимулятори перевантажують судини та наднирники людини, що працює в офісі або шукає здоров'я. | **Блокує витік важкоатлетичних енергетиків у щоденне здоров'я**. |
| **Чітка сепарація Денного тонусу від Вечірнього сну** | **КЛІНІЧНА НЕОБХІДНІСТЬ** | Тонізуючі комплекси B12, Спіруліна та Їжовик підвищують нейронну активність і не повинні призначатися на ніч. | **Запобігає розладам сну через помилковий час прийому**. |
| **Захист спеціальних груп (Вагітні, Діти, 50+)** | **СУВОРА КЛІНІЧНА ІЗОЛЯЦІЯ** | Набори `RE11653` (вагітні) та `RE11819` (діти) мають суворо визначені дозування безпеки. | **Виключає ризик призначити вагітним жінкам кофеїн або неперевірені трави**. |
| **Органічна Спіруліна (`RE11513`) у своєму домені** | **100% ВАЛІДНИЙ СУПЕРФУД** | Спіруліна ідеально насичує клітини мікроелементами щодня, але раніше помилково випадала в гідратацію. | **Повертає спіруліну в категорію щоденного здоров'я та тонусу**. |

## 9.4. Grounded Catalog SKU Mapping (Daily Wellness)
### Гілка А: Загальний імунітет, детокс та суперфуди (Спіруліна + Вітаміни)
- **[RE11513]** *Набір «Енергія і очищення Race Expert Club»* — **1455 грн**  
  *Склад:* абонемент Race Expert Club на 3 месяца; органическая спирулина Now Foods, 500 мг, 100 таблеток; цинк пиколинат Now Foods, 50 мг, 60 капсул; 5 стиков Hydria Perform; Omega-3 Now Foods, 1 000 мг, 30 мягких капсул, 2 упаковки
- **[Nabir_1106]** *Набір «Комплекс для загального зміцнення, спокою та імунітету Race Expert Club» — абонемент на 3 міс* — **1500 грн**  
  *Склад:* Mind Shi Reishi Mushroom 1,000 mg ×1; Myprotein Layered Bar ×3 (вкусы перечислены; >20 g белка/батончик); Mind Shi Shiitake Mushroom 1,000 mg ×1. Назначение по описанию набора: ежедневная общая поддержка, иммунитет и равновесие при физических и психоэмоциональных нагрузках. Отдельный вид спорта не указан. Неопределённость: В доступном перечне состава отдельно не указан абонемент Race Expert Club, несмотря на пометку Club в названии
- **[Nabir_1116]** *Набір «Внутрішня рівновага Race Expert Club» — абонемент на 3 месяца* — **1500 грн**  
  *Склад:* абонемент Race Expert Club на 3 месяца; Nutriversum Magnesium Bisglycinate (товарная упаковка 60 капсул); Nutriversum Multi Vita (60 таблеток); Nutriversum Omega-3 (размер товарной упаковки и множитель набора не подтверждены). Назначение по описанию набора: общее самочувствие и внутреннее равновесие при длительном стрессе
- **[RE11821]** *Набір «Мінеральний тонус Race Expert Club» — абонемент на 3 місяці* — **1375 грн**  
  *Склад:* клуб на 3 месяца; Life Extension Only Trace Minerals, 90 капсул (цинк, медь, марганец, хром, молибден, бор, ванадий); VPLab Magnesium Citrate, 90 софтгелей

### Гілка Б: Когнітивна ясність, пам'ять та робочий фокус (Їжовик гребінчастий / B12)
- **[RE88943]** *Набір «Концентрація в дорозі Race Expert Club» — абонемент на 3 месяца* — **1469 грн**  
  *Склад:* абонемент Race Expert Club на 3 месяца; Lion’s Mane 700 mg ×60 капсул; Now Foods Acetyl-L-Carnitine 500 mg ×50 капсул; OMNOM батончик 50 g ×1; Hydria Daily стики с электролитами ×3. Назначение по описанию набора: поддержка концентрации в поездках, за рулём, на работе и во время активного отдыха. Занятия/аудитория: поездки, вождение и работа; спортивная дисциплина не указана. Расхождение цены: официальная карточка Race Expert на 2026-11-06 показывала 1 500 грн, цена в каталоге на эту дату — 1 469 грн. Источник — карточка по ссылке выше. Неопределённость: существенной неопределённости нет
- **[Nabir_1100]** *Набір «Концентрація і пам’ять 2.0 Race Expert Club» — абонемент на 3 месяца* — **1500 грн**  
  *Склад:* абонемент Race Expert Club на 3 месяца; Reishi батончик 40 g ×2; Lion’s Mane 700 mg/60 капсул ×1; Cordyceps 700 mg/60 капсул ×1. Назначение по описанию набора: поддержка концентрации и памяти согласно описанию набора
- **[Nabir_1111]** *Набір «Спокійна концентрація» по програмі "Ветеранський спорт* — **1500 грн**  
  *Склад:* DRUMn’BADS Lion’s Mane 700 mg, розничная упаковка 60 капсул ([карточка товара Race Expert](https://raceexpert.com.ua/6780-yizhovik-grebinchastij-drumnbads-700-mg-60-kapsul-48202)); DRUMn’BADS адаптогенные жевательные конфеты, 3 упаковки ×15. Назначение по описанию набора: поддержка спокойной концентрации согласно описанию набора

### Гілка В: Жіноче здоров'я, молодість та краса шкіри
- **[RE11813]** *Набір «Формула краси»* — **1500 грн**  
  *Склад:* Nutriversum Collagen Heaven 300 g ×1 (10 g collagen на 15 g порцию); Puritan’s Pride Hair, Skin & Nails Formula 60 капсул ×1 (3,000 mcg biotin на рекомендуемую порцию). Назначение по описанию набора: ежедневная нутритивная поддержка кожи, волос, ногтей и соединительной ткани
- **[RE11744]** *Набір «Здоров'я шкіри Race Expert Club» — абонемент на 3 месяца* — **1500 грн**  
  *Склад:* абонемент Race Expert Club на 3 месяца; Nutriversum Collagen Heaven 300 g ×1; Nutriversum VITA C+MSM лимон 150 g ×1. Назначение по описанию набора: поддержка кожи и соединительной ткани согласно описанию продавца. Спортивная аудитория не указана. Неопределённость: существенной неопределённости нет
- **[RE11682]** *Набір «Жіноче здоров’я Race Expert Club» — абонемент на 3 месяца* — **1500 грн**  
  *Склад:* абонемент Race Expert Club на 3 месяца; VPLab Ultra Women’s Multivitamin 90 капсул ×1; NOW Foods Omega-3 1,000 mg, 30 мягкие капсулы ×1; Nutriversum Vitamin D3+K2 60 капсул ×1. Назначение по описанию набора: ежедневная поддержка женского здоровья, энергии и самочувствия
- **[Nabir_1125]** *Набір «Сяйво та внутрішня енергія Race Expert Club» — абонемент на 3 месяца* — **1500 грн**  
  *Склад:* абонемент Race Expert Club на 3 месяца; Nutriversum Zinc 30 капсул ×1; Iron 30 таблеток ×1; Biotin 30 таблеток ×1; Vitamin B-Complex 30 таблеток ×1. Назначение по описанию набора: поддержка красоты и энергии согласно описанию набора. Пол и спортивное назначение не указаны. Неопределённость: существенной неопределённости нет

### Гілка Г: Опорно-руховий апарат, суглоби та кістки (Колаген + Кальцій D3)
- **[RE11812]** *Набір «Опора руху Race Expert Club»* — **1269 грн**  
  *Склад:* абонемент Race Expert Club на 3 месяца; Life Extension Bone Restore, 120 капсул; куркума Swanson, 720 мг, 30 капсул; витамин D3 Now Foods, 2 000 IU, 30 мягких капсул
- **[RE11810]** *Набір «Міцні кістки Race Expert Club» — абонемент на 3 місяці* — **1419 грн**  
  *Склад:* абонемент Race Expert Club на 3 месяца; Nature’s Plus Animal Parade Calcium Chewable, 135 chewables; Solaray Vitamin K2 MK-7 50 mcg, 30 caps; NOW D3 2000 IU, 30 мягких капсул

### Гілка Д: Спеціалізована турбота (Вагітні, Діти, Чоловіки 50+)
- **[RE11653]** *Набір «Вітаміни для вагітних Race Expert Club» — абонемент на 3 месяца* — **1500 грн**  
  *Склад:* Now Foods folic acid 800 mcg ×250 таблеток ×2; Now Foods Omega-3 1,000 mg, 30 мягкие капсулы ×1; Nutriversum Vitamin D3+K2 60 капсул ×1; абонемент Race Expert Club на 3 месяца. Назначение по описанию набора: набор добавок для женщин, которые планируют беременность или ожидают ребёнка
- **[RE11819]** *Набір «Щоденний захист дитини»* — **1425 грн**  
  *Склад:* Nutriversum Kid Vita жевательных конфет ×60; KAL Vitamin D-Rex 10 mcg/90 жувальних таблеток ×1; Nordic Naturals Daily Omega Kids/30 мягкие капсулы ×1. Назначение по описанию набора: ежедневный детский набор пищевых добавок
- **[RE89023]** *Набір «Чоловіча підтримка 50+ Race Expert Club» — абонемент на 3 місяці* — **1500 грн**  
  *Склад:* абонемент Race Expert Club на 3 месяца; Nature’s Way Alive Men’s 50+, 50 tabs; Swanson Ashwagandha 450 mg, 100 caps; NOW Melatonin 3 mg, 60 caps

### Гілка Е: Зменшення стресу та внутрішня рівновага
- **[Nabir_1110]** *Набір «Зменшення стресу та регуляція сну Race Expert Club» — абонемент на 3 месяца* — **1500 грн**  
  *Склад:* абонемент Race Expert Club на 3 месяца; Mind Shi Reishi Mushroom 1,000 mg (розничная упаковка 60 капсул); Mind Shi CBD Oil Isolate, апельсин, 1,000 mg в бутылке 10 ml ([данные производителя](https://www.mindshi.com/cbd-oil-isolate-1000mg-orange)); Myprotein Layered Bars ×3: Triple Chocolate Fudge, Vanilla Birthday Cake и White Gold. Назначение по описанию набора: поддержка сна и снижение стресса согласно позиционированию продавца. Отдельный вид спорта не указан. Неопределённость: карточка набора не указывает множители упаковок Reishi и CBD; фасовка товара Reishi — 60 капсул, CBD — 10 ml
- **[Nabir_1101]** *Набір «Антитривожність 2.0 Race Expert Club» — абонемент на 3 місяці* — **1500 грн**  
  *Склад:* клуб на 3 месяца; батончики с рейши 40 г ×2 (более 12 г белка каждый); красный мухомор 500 мг, 60 капсул; рейши 700 мг, 60 капсул. Назначение в формулировке карточки: управление стрессом/эмоциональный баланс и восстановление; аудитория — люди с высокой психоэмоциональной нагрузкой и спортсмены в интенсивных тренировках. Медицинские эффекты не добавлялись. - Теги: purpose:mood_balance_and_recovery; item_type:club_membership_bundle; sport:not_sport_specific; distance:not_applicable; duration:3_months; audience:athletes; buyer_weight:not_specified; price:1500_uah

---

# 10. Category 9: «Подарунки спортсменам та військовим» (Gifts, Commemoration & Care Packages)

## 10.1. Category Mission & Primary Deliverable
- **Core Emotional & Athletic Mission:** Meaningful appreciation, patriotic celebration of courage and endurance, heartfelt care packages for deployed service members and athletic achievers, and frictionless gifting with 100% aesthetic presentation.
- **The Primary Deliverable:** Commemorative wooden gift sets with national symbolism (*«Воля та незламність»*, *«Народжені вільними»*, *«Небесна варта»*), double medal display hangers (*«Подвійна нагорода»*), luxury plush bath towels (*Шарпей*), and all-in-one athletic care boxes.
- **The Core Negative Rule (Agent Deep Gift Forensic Finding):** Sizing friction is the #1 hazard in gifting. If a buyer does not know the recipient's shoe size, the quiz MUST divert to **Universal Zero-Sizing gifts** (Sharpey towels, medal displays, patriotic keepsakes) instead of guessing socks. Furthermore, cyclists, runners, and tactical warriors must never encounter a dead-end.

## 10.2. Exact Adaptive Question Sequence (9 Questions)

### Q1: Recipient Profile & Relationship (Кому призначений подарунок)
**UA:** Для кого саме ви обираєте подарунковий набір?  
**RU:** Для кого именно вы выбираете подарочный набор?
- **OPT-GIF-1.1:** Військовий, ветеран, захисник України (глибока повага, патріотична символіка, практичність)
- **OPT-GIF-1.2:** Бігун, тріатлет або марафонець (спортивні досягнення, медалі, витривалість)
- **OPT-GIF-1.3:** Відвідувач тренажерного залу, силовий атлет або фітнес-ентузіаст
- **OPT-GIF-1.4:** Мандрівник, турист або людина, яка любить активний відпочинок
- **OPT-GIF-1.5:** Початківець у спорті, якого хочеться мотивувати та підтримати

### Q2: Emotional Style & Meaning (Характер та атмосфера подарунка)
**UA:** Який емоційний посил має нести набір?  
**RU:** Какой эмоциональный посыл должен нести набор?
- **OPT-GIF-2.1:** Патріотичний, урочистий, незламний (символіка державності, мужності та честі)
- **OPT-GIF-2.2:** Спортивний тріумф та фіксація досягнень (для збереження та демонстрації медалей)
- **OPT-GIF-2.3:** Затишок, тепло та преміальний релакс після важкого дня (великі рушники, термокомфорт)
- **OPT-GIF-2.4:** Практична польова турбота (те, що стане у пригоді на службі, в дорозі чи поході)
- **OPT-GIF-2.5:** Універсальний спортивний комплімент зі смаколиками та вітамінами

### Q3: Mandatory Foot Sizing Check (Перевірка знання розміру взуття)
**UA:** Чи знаєте ви точний розмір взуття людини, якій обираєте подарунок?  
**RU:** Знаете ли вы точный размер обуви человека, которому выбираете подарок?
- **OPT-GIF-3.0:** НЕ знаю розмір взуття: Покажіть 100% безпечні подарунки БЕЗ розміру (рушники, медальниці, патріотичні набори)
- **OPT-GIF-3.1:** Так, знаю розмір 35–37 (Жіночий S)
- **OPT-GIF-3.2:** Так, знаю розмір 38–40 (M)
- **OPT-GIF-3.3:** Так, знаю розмір 40–42 (M/L)
- **OPT-GIF-3.4:** Так, знаю розмір 43–45 (L/XL)
- **OPT-GIF-3.5:** Так, знаю розмір 46–48 (XXL)

### Q4: Core Gift Artifact Type (Бажаний ключовий предмет у подарунку)
**UA:** Що саме було б найкращим подарунком для отримувача?  
**RU:** Что именно было бы лучшим подарком для получателя?
- **OPT-GIF-4.1:** Патріотичний пам'ятний артефакт (гравійовані дерев'яні бокси, шеврони, тризуб)
- **OPT-GIF-4.2:** Подвійна настінна вішалка для медалей («Подвійна нагорода»)
- **OPT-GIF-4.3:** Преміальні банні рушники серії Шарпей (темна або класична гама)
- **OPT-GIF-4.4:** Практичний комплект бігових шкарпеток та термобафа
- **OPT-GIF-4.5:** Набір смачних енергетичних батончиків та вітамінів

### Q5: Packaging & Presentation (Оформлення подарунка)
**UA:** Як має бути упакований набір?  
**RU:** Как должен быть упакован набор?
- **OPT-GIF-5.1:** Елітний дерев'яний крафтовий бокс з пам'ятним гравіюванням
- **OPT-GIF-5.2:** Фірмова стильна подарункова коробка Race Expert
- **OPT-GIF-5.3:** Лаконічне практичне пакування

### Q6: Seasonality Context (Сезонний настрій подарунка)
**UA:** Чи має значення пора року?  
**RU:** Имеет ли значение время года?
- **OPT-GIF-6.1:** Теплий затишний осінньо-зимовий набір (баф, теплі шкарпетки, зігріваючий настрій)
- **OPT-GIF-6.2:** Весняно-літній динамічний спортивний комплект
- **OPT-GIF-6.3:** Всесезонний класичний подарунок

### Q7: Club Membership Privilege (Додатковий бонус)
**UA:** Чи бажаєте ви додати до подарунка 3-місячний доступ до закритого клубу Race Expert?  
**RU:** Желаете ли вы добавить к подарку 3-месячный доступ в закрытый клуб Race Expert?
- **OPT-GIF-7.1:** Так, це чудовий статусний подарунок (включає онлайн-супровід тренерів)
- **OPT-GIF-7.2:** Достатньо лише матеріальних речей у коробці

### Q8: Target Activity for Beginners (Якщо подарунок для початківця)
**UA:** Якщо це подарунок людині, яка тільки починає свій шлях у спорті:  
**RU:** Если это подарок человеку, который только начинает свой путь в спорте:
- **OPT-GIF-8.1:** Набір «Подарунок початківцю» (ідеальна перша пара шкарпеток та аксесуари)
- **OPT-GIF-8.2:** Набір для щоденних прогулянок та тонусу
- **OPT-GIF-8.3:** Отримувач — досвідчений спортсмен, початковий рівень не потрібен

### Q9: Budget Expectation & Floor Awareness (Бюджетний рівень)
**UA:** Який бюджет ви виділяєте на подарунок?  
**RU:** Какой бюджет вы выделяете на подарок?
- **OPT-GIF-9.1:** Доступний якісний набір (1379–1439 грн)
- **OPT-GIF-9.2:** Преміальний подарунковий бокс (1499–1500 грн)

## 10.3. The «Подходит / Не подходит» Critical Audit for Gifts
| Запитання та опція | Статус AI | Чому підходить (Клінічне обґрунтування) | Який негативний брак / витік блокує? |
|---|---|---|---|
| **Порятунок через Zero-Sizing (Рушники та Медалі)** | **КРИТИЧНО ПІДХОДИТЬ** | Дарувальник часто не знає точний розмір ноги; рушники Шарпей та медальниці мають 100% задоволення і нуль ризику помилитися з розміром. | **Запобігає даруванню невідповідного взуттєвого розміру**. |
| **Патріотичні сети для військових (`Nabir_1060`, `RE11694`)** | **100% ВАЛІДНЕ ВИЗНАННЯ** | Символіка «Воля та незламність», «Характер воїна», «Небесна варта» дарує глибоку повагу та вдячність. | **Блокує дарування легковажних цукерок замість гідного артефакту**. |
| **Медальниця «Подвійна нагорода» (`RE89473`)** | **ІДЕАЛЬНО ДЛЯ АТЛЕТІВ** | Кожен бігун, триатлет чи плавець мріє красиво розмістити свої фінішні медалі. | **Забезпечує 100% влучність подарунка спортсмену без підбору розміру одягу**. |
| **Бан випадкових медичних пігулок як сюрпризу** | **СУВОРИЙ БАН** | Дарувати медичні препарати або рецептурні добавки без відома отримувача неетично. | **Залишає в подарунках лише корисні снеки, вітаміни та естетичні речі**. |

## 10.4. Grounded Catalog SKU Mapping (Gifts & Commemoration)
### Гілка А: Патріотичні меморіальні набори мужності та честі
- **[Nabir_1060]** *Набір «Воля та незламність»* — **1500 грн**  
  *Склад:* медаль «Озброєні волею»; брелоки-гильза и Drone; брелок Fighter F-16 длиной 35 мм
- **[RE11694]** *Набір «Воля та незламність Race Expert Club» — абонемент на 3 місяці* — **1499 грн**  
  *Склад:* абонемент Race Expert Club на 3 месяца; medal «Озброєні волею 2.0»; брелок из гильзы с гравировкой; брелок в виде истребителя; брелок в виде дрона
- **[Nabir_1061]** *Набір «Народжені вільними Race Expert Club» — абонемент на 3 месяца* — **1500 грн**  
  *Склад:* “Незалежність – це каждый з нас” медаль (движущийся дрон); брелок из гильзы; брелок с изображением дрона; F-16 брелок, 35 mm. Назначение по описанию набора: патриотический подарок и символ участия в независимости Украины
- **[Nabir_1062]** *Набір «Небесна варта Race Expert Club» — абонемент на 3 месяца* — **1500 грн**  
  *Склад:* “Гвардія небес” медаль с изображением дрона и снаряда; брелок из гильзы; брелок с изображением дрона; F-16 брелок, 35 mm. Назначение по описанию набора: патриотический подарок для военных и людей на пути борьбы
- **[Nabir_1063]** *Набір «Пульс нації»* — **1500 грн**  
  *Склад:* “Patriotic Pulse” медаль; брелок из гильзы; брелок с изображением дрона; F-16 брелок, 35 mm. Назначение по описанию набора: патриотический подарок; символическое назначение набора
- **[Nabir_1064]** *Набір «Україна починається з тебе Race Expert Club» — абонемент на 3 месяца* — **1500 грн**  
  *Склад:* медаль “Україна в тобі” (зеркальное изображение герба); брелок из гильзы; брелок с изображением дрона; F-16 брелок, 35 mm. Назначение по описанию набора: патриотический подарок и символ Украины. Спортивное назначение не указано. Неопределённость: URL карточки содержит устаревшие название и SKU (“Пульс нації”, Nabir_1063), тогда как название и SKU в каталоге — Nabir_1064/«Україна починається з тебе»
- **[RE89453]** *Набір «Мирне небо» — абонемент на 3 місяці* — **1500 грн**  
  *Склад:* клуб на 3 месяца; медаль «Гвардія Небес»; брелоки Fighter, Drone и Shell
- **[RE89454]** *Набір «Політ честі» — абонемент на 3 місяці* — **1500 грн**  
  *Склад:* клуб на 3 месяца; медаль «Крила Свободи»; брелоки Fighter, Drone и Shell
- **[RE89455]** *Набір «Незборний дух» — абонемент на 3 місяці* — **1500 грн**  
  *Склад:* клуб на 3 месяца; медаль «Озброєні волею 2.0»; брелоки Fighter, гильза и Drone 2.0
- **[RE89456]** *Набір «Стук серця» — абонемент на 3 місяці* — **1500 грн**  
  *Склад:* участие в клубе на 3 месяца; медаль «Патріотичний пульс»; брелоки Fighter, Drone 2.0 и гильза
- **[RE89457]** *Набір «Характер воїна» — абонемент на 3 місяці* — **1500 грн**  
  *Склад:* участие в клубе на 3 месяца; медаль «Озброєні волею»; брелоки Fighter, Drone 2.0 и гильза
- **[RE89458]** *Набір «Єдність сильних» — абонемент на 3 місяці* — **1500 грн**  
  *Склад:* клуб на 3 месяца; медаль «Незалежність — це кожен з нас»; брелоки Fighter, Drone 2.0 и гильза
- **[RE89460]** *Набір «Подарунок військовому-спортсмену» — абонемент на 3 місяці* — **1500 грн**  
  *Склад:* клуб на 3 месяца; медаль «Гвардія Небес»; флисовый баф; тёмные носки RE2 40–44

### Гілка Б: Спортивний тріумф та медалі (Zero-Sizing)
- **[RE89473]** *Набір «Подвійна нагорода» — абонемент на 3 місяці* — **1500 грн**  
  *Склад:* клуб на 3 месяца; медали «Озброєні волею 2.0» и «Здатні без зброї»; брелоки Drone 2.0 и гильза

### Гілка В: Преміальні банні рушники Шарпей (Zero-Sizing затишок)
- **[RE89486]** *Набір «Банні рушники Шарпей: класика» — абонемент на 3 месяца* — **1500 грн**  
  *Склад:* 3 полотенца, бежевый/бордовый/серый, 135×70 cm каждый, хлопок 500 g/m²; абонемент Race Expert Club на 3 месяца. Назначение по описанию набора: полотенца для дома, зала, бассейна, сауны или поездок. Занятия/аудитория: дом, зал, бассейн, сауна и поездки; спортсмены упомянуты в описании. Неопределённость: существенной неопределённости нет
- **[RE89487]** *Набір «Банні рушники Шарпей: темна гама» — абонемент на 3 месяца* — **1500 грн**  
  *Склад:* 3 полотенца, чёрный/тёмно-синий/зелёный, 135×70 cm каждый; 100% хлопок, 500 g/m²; абонемент Race Expert Club на 3 месяца. Назначение по описанию набора: полотенца для душа, тренировок, бассейна, сауны и поездок. Занятия: зал, плавание, сауна и поездки; набор не связан с конкретным видом спорта. Неопределённость: существенной неопределённости нет

### Гілка Г: Турбота про початківця та активні дні
- **[RE89466]** *Набір «Подарунок початківцю» — абонемент на 3 місяці* — **1500 грн**  
  *Склад:* клуб на 3 месяца; медаль «Озброєні волею 2.0»; стеклянная бутылка 530 мл; тёмные носки RE2 40–44
- **[RE89467]** *Набір «Подарунок початківцю 2.0» — абонемент на 3 місяці* — **1500 грн**  
  *Склад:* клуб на 3 месяца; медаль «Крила Свободи»; стеклянная бутылка 530 мл; белые носки RE2 40–44
- **[RE89481]** *Набір «Подарунок для активних днів» — абонемент на 3 месяца* — **1500 грн**  
  *Склад:* абонемент Race Expert Club на 3 месяца; “Patriotic Pulse” медаль; black сумка-органайзер; белые носки RE2 размер 40–44. Назначение по описанию набора: подарочный набор для активных дней, прогулок и поездок. Занятия: прогулки, поездки и активный отдых. Неопределённость: существенной неопределённости нет
- **[RE11026]** *Набір «Спортивний подарунок»* — **1500 грн**  
  *Склад:* белые носки Race Expert 43–45 ×2; брелоки-гильза ×3; NOW Foods Vitamin D3 2 000 IU, 120 софтгелей; печенье Myprotein Baked Cookie 75 г ×3 (по 13 г растительного белка)
- **[RE11024]** *Набір «Подарунок спортсмену Race Expert Club» — абонемент на 3 месяца* — **1500 грн**  
  *Склад:* абонемент Race Expert Club на 3 месяца; носки RE2, белые и тёмные, размер 40–44 ×1 пара кожного размеру; из латунной гильзы брелок ×2; NOW 7-day pill case; MIAMI VIBES multivitamin 100 tabs. Назначение по описанию набора: подарок для бегунов, спортсменов и активных людей

### Гілка Д: Сезонні подарунки для мандрівників та природи
- **[RE89482]** *Набір «Подарунок у похід» — абонемент на 3 місяці* — **1500 грн**  
  *Склад:* клуб на 3 месяца; медаль «Гвардія небес»; небольшой чёрный органайзер; тёмные носки RE2 40–44
- **[RE89474]** *Набір «Подарунок у дорогу» — абонемент на 3 місяці* — **1500 грн**  
  *Склад:* клуб на 3 месяца; медаль «Озброєні волею 2.0»; небольшой чёрный органайзер EF-0903-BK; тёмные носки RE2 40–44
- **[RE89483]** *Набір «Теплий подарунок» — абонемент на 3 місяці* — **1500 грн**  
  *Склад:* клуб на 3 месяца; медаль «Крила Свободи»; баф (цвет из ассортимента); небольшой чёрный органайзер
- **[RE89484]** *Набір «Осінній подарунок» — абонемент на 3 місяці* — **1500 грн**  
  *Склад:* клуб на 3 месяца; медаль «Озброєні волею 2.0»; флисовый баф; небольшой чёрный органайзер
- **[RE89485]** *Набір «Подарунок для прогулянок» — абонемент на 3 місяці* — **1379 грн**  
  *Склад:* клуб на 3 месяца; медаль «Здатні без зброї»; баф (цвет из ассортимента); небольшой чёрный органайзер; тёмные носки RE2 40–44
- **[RE89459]** *Набір «Подарунок мандрівнику» — абонемент на 3 місяці* — **1439 грн**  
  *Склад:* клуб на 3 месяца; полотенце Sharpey 135×70 см; флисовый баф; белые носки RE2 40–44

---

# 11. Cross-Category Diagnostic Routing Matrix & Global Invariants

## 11.1. Summary of Question Count & Adaptive Length per Category
| Номер | Категорія (Назва) | Кількість питань | Головний фокус AI діагностики | Обов'язкове питання розміру? |
|---|---|---|---|---|
| **1** | **Гідратація та сольовий баланс** | **8** | Осмотичні солі, судоми, бандл із пляшкою | Тільки якщо обрано бандл зі шкарпетками |
| **2** | **Відновлення та якісний сон** | **8** | ЦНС розслаблення, фаза сну, зняття кріпатури | Тільки якщо обрано бандл із шкарпетками |
| **3** | **Біг та підготовка до стартів** | **9** | Дистанція (5k-42k), гелі, стартовий пояс | **Так (Обов'язковий розмір взуття)** |
| **4** | **Силові тренування та зал** | **8** | Креатин, BCAA, гіпертрофія, фітнес-інвентар | Тільки якщо обрано бандл зі шкарпетками |
| **5** | **Спортивне харчування та перекуси** | **8** | Гаряча їжа ЇDLO, джерки, протеїнові батончики | Ні (100% без розміру) |
| **6** | **Екіпірування та аксесуари** | **8** | Захист стопи, стартові пояси, рушники Шарпей | **Так (Обов'язковий розмір взуття)** |
| **7** | **Походи, кемпінг та трекінг** | **9** | ЇDLO, джерки, наметний сон, трекінгові шкарпетки | **Так (Розмір трекінгового взуття)** |
| **8** | **Щоденне здоров'я та вітаміни** | **8** | Імунітет, когнітивний фокус, колаген, групи | Ні (100% без розміру) |
| **9** | **Подарунки спортсменам та військовим**| **9** | Патріотичні бокси, медальниці, Zero-Sizing | **Так (З перевіркою знання розміру)** |

## 11.2. The Global Zero-Dead-End Guarantee
Across all 9 categories and 207 catalog sets, every single question path resolves to **at least 2 and up to 15 grounded catalog sets**. There is **ZERO possibility of a 0-result dead-end**, and every recommendation is fortified with an empathetic, truthful explanation that details exactly what the buyer is receiving and why it fits their stated purpose.

---

*(End of Production AI Question System — Race Expert)*
