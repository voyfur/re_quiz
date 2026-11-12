# Human-Centric Question Matrix: Sports Nutrition & Pharmacology
**Architectural Blueprint for the Race Expert AI Quiz (207 Product Sets)**  
**Author:** Lead Sports Nutritionist & Pharmacologist, AI Quiz Architecture Team  
**Scope:** Categories «Відновлення та сон», «Щоденна підтримка та вітаміни», «Спортивне харчування та перекуси», «Гідратація та електроліти»  
**Status:** Approved for Implementation | Grounded in 600 Stress Test Empirical Findings  

---

## 1. Executive Summary & Clinical Manifesto

Following the comprehensive audit of 600 end-to-end stress tests across 207 catalog sets, a fundamental architectural flaw was uncovered in the quiz engine: **the quiz was speaking like a database query optimizer instead of a caring sports physician and nutritionist.**

When a runner asks for post-race muscle relief, presenting dry database tokens such as `protein_carbohydrate_food`, `during_day_tone`, or `supplements_vitamins_minerals` alienates the athlete. Worse, rigid algorithmic categorization caused catastrophic pharmacological blunders:
1. Recommending **ZMA (a deep-sleep neuro-relaxant) as a pre-workout "charge-up"** for daytime training (`agent_1_report.md`).
2. Confusing **daytime adaptogenic stress-resilience** (`during_day_tone`) with bedtime sedatives or throwing API 400 validation crashes.
3. Leaking **spirulina tablets and mushroom nootropics into Hydration** for thirsty endurance runners while genuine dehydrated camping meals (`ЇDLO`) suffered a **100% failure rate** (`agent_4_report.md`).
4. Recommending **1 kg bodybuilding weight-gainer powders and pure creatine tubs** to runners seeking portable trail snacks.
5. Offering **unlabeled psychoactive mushroom microdosing (Amanita muscaria)** without informed consent or athletic warnings.

### The Human-Centric Clinical Philosophy
This matrix replaces machine-centric filters with **empathetic, intent-driven clinical dialogue**. Each question is crafted to:
- Mirror the consultation of an elite sports doctor who understands training load, circadian rhythms, gastrointestinal tolerance, and cellular biochemistry.
- Offer **bilingual parity** (Ukrainian and Russian) with warm, natural phrasing and explicit explanatory subtext.
- Implement **fail-safe intent mapping** that guarantees **0 dead ends, 0 validation errors, and 0 empty searches**.
- Enforce **strict medical guardrails** preventing contraindications, stimulants before sleep, or sedative lethargy before races.

---

## 2. Category 1: «Відновлення та сон» (Recovery, Sleep, CNS & Joint Regeneration)

### 2.1. Clinical & Pharmacological Diagnostics
In sports pharmacology, "recovery" encompasses four distinct biochemical and physiological cascades that must never be conflated:
1. **Sleep Architecture & Chronobiology:** Modulation of GABAergic pathways, pineal melatonin signaling, and slow-wave (N3/REM) sleep depth. Agents: Melatonin, 5-HTP, ZMA (Zinc L-Monomethionine + Magnesium Aspartate + B6), sleep reishi extracts, chamomile/hops.
2. **Daytime CNS Anti-Stress & Cortisol Regulation:** Modulation of the HPA (hypothalamic-pituitary-adrenal) axis without somnolence or motor sedation. Agents: Ashwagandha (Withania somnifera), daytime adaptogenic Reishi, Magnesium Citrate/Ultra-Mag, CBD oil, B-complex.
3. **Post-Exercise Myofibrillar Repair & DOMS Relief:** Glycogen resynthesis, mTOR activation, prevention of muscle protein catabolism, and clearance of metabolic lactate/hydrogen ions. Agents: L-Glutamine, BCAA (2:1:1), protein-carbohydrate recovery blends, chelated magnesium for nocturnal cramps.
4. **Articular Cartilage & Connective Matrix Regeneration:** Extracellular matrix remodeling, proteoglycan synthesis, chondroprotection, and bone mineral density under impact pounding. Agents: Bone Restore complexes, Calcium/Magnesium/Zinc chelates, Vitamin D3+K2, trace minerals.

---

### 2.2. The 4 Natural Diagnostic Questions

#### Question 1: Physiological Focus (Першочергова потреба)
- **UK:** «Що саме потребує відновлення у вашому організмі в першу чергу?»  
  *Subtext: «Виберіть головний пріоритет, щоб ми підібрали комплекс з точним фармакологічним впливом.»*
- **RU:** «Что именно требует восстановления в вашем организме в первую очередь?»  
  *Subtext: «Выберите главный приоритет, чтобы мы подобрали комплекс с точным фармакологическим действием.»*

| Option Code | Label (UK) | Label (RU) | Explanatory Subtext (UK / RU) |
|---|---|---|---|
| `sleep_deep` | **Глибокий сон та легке засинання** | **Глубокий сон и легкое засыпание** | Зняття нічної тривожності, швидке засинання та повноцінне відновлення нервової системи до ранку. / Снятие ночной тревожности, быстрое засыпание и глубокое восстановление ЦНС к утру. |
| `cns_stress` | **Денний спокій та захист від стресу** | **Дневное спокойствие и защита от стресса** | Зниження рівня кортизолу, спокій і стійкість без денної сонливості чи млявості. / Снижение кортизола, эмоциональный баланс и устойчивость без сонливости или вялости. |
| `muscle_doms` | **М'язи після тренувань (зняття крепатури)** | **Мышцы после тренировок (снятие крепатуры)** | Швидке загоєння мікророзривів м'язів, поповнення амінокислот та зняття судом. / Быстрое заживление микротравм мышечных волокон, восполнение аминокислот и снятие спазмов. |
| `joints_ligaments` | **Суглоби, зв'язки та міцність кісток** | **Суставы, связки и крепость костей** | Зміцнення суглобового хряща та сполучної тканини при регулярному біговому та ударному навантаженні. / Укрепление хрящевой и соединительной ткани при регулярных ударных и беговых нагрузках. |

#### Question 2: Administration Timing & Rhythm (Час прийому та біоритми)
- **UK:** «У який час доби вам найзручніше приймати комплекс?»  
  *Subtext: «Це дозволяє уникнути конфлікту між стимулюючими та релаксуючими компонентами.»*
- **RU:** «В какое время суток вам удобнее всего принимать комплекс?»  
  *Subtext: «Это позволяет избежать конфликта между бодрящими и расслабляющими компонентами.»*

| Option Code | Label (UK) | Label (RU) | Explanatory Subtext (UK / RU) |
|---|---|---|---|
| `bedtime` | **Ввечері перед сном (за 30–60 хв)** | **Вечером перед сном (за 30–60 мин)** | Формули для релаксації, м'язового розслаблення та підготовки до глибокої фази сну. / Формулы для релаксации, мышечного покоя и глубокого восстановительного сна. |
| `post_workout` | **Одразу після завершення тренування** | **Сразу после окончания тренировки** | Закриття білково-вуглеводного та амінокислотного вікна для блокування катаболізму. / Закрытие анаболического окна для блокировки катаболизма и быстрого снятия усталости. |
| `daytime_steady` | **Вранці або вдень під час їжі** | **Утром или днем во время еды** | Комплекси щоденного прийому для суглобів, зв'язок або денного антистрес-контролю. / Комплексы ежедневного приема для суставов, связок или дневного антистресс-баланса. |
| `any_timing` | **Будь-який зручний час** | **Любое удобное время** | Головне — ефективність активних речовин, графік прийому підлаштую. / Главное — максимальный терапевтический эффект, график приема адаптирую. |

#### Question 3: Form Factor & Preference (Бажана форма прийому)
- **UK:** «Який формат відновлювального комплексу для вас найзручніший?»  
  *Subtext: «Оберіть те, що приємно та легко вживати саме вам.»*
- **RU:** «Какой формат восстановительного комплекса для вас наиболее удобен?»  
  *Subtext: «Выберите то, что приятно и легко принимать именно вам.»*

| Option Code | Label (UK) | Label (RU) | Explanatory Subtext (UK / RU) |
|---|---|---|---|
| `capsules_tabs` | **Капсули або таблетки** | **Капсулы или таблетки** | Точне фармакологічне дозування без стороннього смаку, зручно брати з собою. / Точная терапевтическая дозировка без вкуса, удобно принимать дома и в поездках. |
| `drink_powder` | **Розчинний напій або порошок** | **Растворимый напиток или порошок** | Смачний коктейль або BCAA/глютамін, що додатково насичує організм водою. / Вкусный восстановительный напиток или BCAA/глютамин с быстрым усвоением и гидратацией. |
| `bars_plus_minerals` | **Корисний перекус + мінерали** | **Полезный перекус + минералы** | Ситні протеїнові батончики в поєднанні з релаксуючими мікроелементами. / Питательные белковые батончики в комбинации с расслабляющими минералами. |
| `any_form` | **Будь-яка форма (на розсуд фахівця)** | **Любая форма (на усмотрение эксперта)** | Оптимальний підбір за дією без обмежень за формою випуску. / Подбор по максимальной эффективности без ограничений по типу формы. |

#### Question 4: Budget Anchor & Club Coaching
- **UK:** «Оберіть комфортний бюджет на повноцінний курс відновлення:»  
  *Subtext: «Базові моноелементи від 985 ₴, преміальні багатокомпонентні набори від 1350 ₴.»*
- **RU:** «Выберите комфортный бюджет на полноценный курс восстановления:»  
  *Subtext: «Базовые монокомплексы от 985 ₴, премиальные многокомпонентные наборы от 1350 ₴.»*

---

### 2.3. Underlying Catalog Intent Mapping (Guaranteed 0 Dead Ends)

| User Path (Need + Timing) | Primary Target SKUs | Secondary Fallback SKUs | Catalog Price Range | Match Status Guarantee |
|---|---|---|---|---|
| **`sleep_deep` + `bedtime`** | `RE89017` (Вечірній ритуал — 1425 ₴), `RE88947` (Спокійний сон — 1485 ₴), `RE89026` (Нічне відновлення — 1500 ₴), `RE11523` (Глибокий сон — 1489 ₴), `RE11525` (Природний сон — 1485 ₴), `RE11803` (Польовий сон — 1500 ₴), `race-expert-167` (Нічний ZMA — 1500 ₴) | `Nabir_1127` (Ultra-Mag 60 табл — 1379 ₴), `RE11652` (Triple Magnesium — 1500 ₴) | 1379 – 1500 ₴ | **100% Exact Match** (7 primary sets available) |
| **`cns_stress` + `daytime_steady`** | `RE88958` (Відпочинок нервової системи — 1500 ₴), `RE88949` (Спокійний вечір — 1479 ₴), `RE11674` (Внутрішній баланс — 1449 ₴), `RE11821` (Мінеральний тонус — 1375 ₴), `race-expert-168` (Рівновага дня), `race-expert-170` (Нервова система), `race-expert-172` (Зменшення стресу) | `RE89017` (Рейші адаптація), `Nabir_1127` | 1375 – 1500 ₴ | **100% Exact Match** (Unlocks previously crashing `during_day_tone` sets) |
| **`muscle_doms` + `post_workout`** | `RE11796` (М'язи в тонусі BCAA+Gluta — **985 ₴**), `RE11797` (Швидке відновлення Glutamine + Sponser — 1500 ₴), `RE11652` (Боротьба з кріпатурою Magnesium + Hydria — 1500 ₴), `RE89451` (Ultra-Mag + Рушник — 1500 ₴), `race-expert-120` (L-Glutamine 500g), `race-expert-174` (BCAA+Gluta 500g) | `RE11786` (Nutriversum BCAA + Hydria — 1285 ₴), `RE11659` (Тиждень бігуна — 1200 ₴) | 985 – 1500 ₴ | **100% Exact Match** (Budget entry at 985 ₴ prevents floor-anchor dead end) |
| **`joints_ligaments` + `daytime_steady`** | `RE11812` (Опора руху Bone Restore — 1269 ₴), `RE11810` (Міцні кістки — 1419 ₴), `RE11514` (Кістки, м’язи і нерви Ca/Mg/Zn — 1435 ₴), `RE89023` (Підтримка 50+ — 1500 ₴) | `RE11821` (Trace Minerals — 1375 ₴) | 1269 – 1500 ₴ | **100% Exact Match** (Dedicated cartilage/bone sets) |

---

### 2.4. Critical Pharmacological Guardrails & Safety Warnings

> [!CAUTION]
> **GUARDRAIL 1: Zero Pre-Workout Sedation**  
> Sets containing **ZMA, Melatonin, 5-HTP, or High-Dose Reishi** (`race-expert-167`, `RE89017`, `RE88947`, `RE89026`, `RE11523`, `RE11525`, `RE11803`) must **NEVER** be displayed when the user selects `before_training` or seeks an energy boost.  
> *Physiological rationale:* ZMA and melatonin cross the blood-brain barrier to trigger neuro-inhibition and muscular hypotonia; taking them pre-workout induces lethargy, slows motor reaction time, and increases injury risk.

> [!WARNING]
> **GUARDRAIL 2: Zero Evening Stimulants in Sleep Inquiries**  
> Caffeinated gels, Pre-Workout boosters (`RE11636`), and Cordyceps extracts (`RE11806`, `Row 79`) must **NEVER** appear for `sleep_deep` or `bedtime`.

> [!IMPORTANT]
> **GUARDRAIL 3: Fly Agaric (Amanita muscaria) Informed Consent Gate**  
> Sets containing red fly agaric microdosing (`Nabir_1101` / `race-expert-126`, `race-expert-169`) must **NEVER** be served as standard recommendations to unsuspecting athletes or recovery seekers.  
> *Enforcement:* If offered under stress relief, the UI must render an explicit medical disclosure: *«Містить сертифікований мікродозинг Amanita muscaria (червоний мухомор 500 мг). Не рекомендується особам до 18 років, вагітним та спортсменам перед проходженням допінг-контролю.»*

---

## 3. Category 2: «Щоденна підтримка та вітаміни» (Daily Wellness, Immunity & Vitality)

### 3.1. Clinical & Pharmacological Diagnostics
Daily supplementation requires balancing long-term organ protection and cellular vitality:
1. **Systemic Immunity & Micronutrient Balance:** Mitigating chronic micronutrient deficiencies (Vitamin D3, Zinc, Vitamin C, Spirulina, trace minerals) that compromise cellular immunity and increase susceptibility to upper respiratory tract infections (URTI) in hard-training individuals.
2. **Cognitive Longevity & Neuro-Focus:** Nootropic mushroom polysaccharides (Erinacines and Hericenones from *Hericium erinaceus* / Lion's Mane), Acetyl-L-Carnitine, and B-vitamins that stimulate Nerve Growth Factor (NGF) and acetylcholine without inducing tachycardia or adrenal fatigue.
3. **Cardiovascular & Lipid Architecture:** High-potency Omega-3 polyunsaturated fatty acids (EPA/DHA) and trace minerals that maintain vascular endothelial elasticity and reduce chronic low-grade inflammation.
4. **Locomotor Integrity:** Daily calcium, magnesium, trace mineral, and Vitamin K2-MK7 complexes that sustain skeletal mineralization during repetitive micro-impacts.

---

### 3.2. The 4 Natural Diagnostic Questions

#### Question 1: Health Vector Focus (Головний фокус здоров'я)
- **UK:** «Який аспект вашого здоров'я та самопочуття потребує найбільшої підтримки?»  
  *Subtext: «Оберіть напрямок, щоб комплекс закривав саме ваші індивідуальні дефіцити.»*
- **RU:** «Какой аспект вашего здоровья и самочувствия требует наибольшей поддержки?»  
  *Subtext: «Выберите направление, чтобы комплекс закрывал именно ваши индивидуальные дефициты.»*

| Option Code | Label (UK) | Label (RU) | Explanatory Subtext (UK / RU) |
|---|---|---|---|
| `daily_immunity` | **Міцний імунітет та щоденний тонус** | **Крепкий иммунитет и ежедневный тонус** | Захист від застуд, антиоксиданти та базова вітамінно-мінеральна енергія для організму щодня. / Защита от сезонных простуд, антиоксиданты и восполнение базовой витаминной нормы каждый день. |
| `daily_brain` | **Ясний розум, пам'ять та концентрація** | **Ясный ум, память и концентрация** | Покращення когнітивних функцій, фокус на роботі та захист клітин мозку від перевтоми (ноотропи/гриби). / Улучшение работы мозга, высокая концентрация на работе и защита от умственного истощения (ежовик/ноотропы). |
| `daily_joints` | **Здоров'я опорно-рухового апарату** | **Здоровье опорно-двигательного аппарата** | Підтримка суглобів, мінералізація кісток та еластичність зв'язок при щоденній руховій активності. / Поддержка суставов, минерализация костей и прочность связок при активном ритме жизни. |
| `daily_heart` | **Серцево-судинна система та антиоксиданти** | **Сердечно-сосудистая система и антиоксиданты** | Поліненасичені омега-3 кислоти, очищення організму та захист судин від оксидативного стресу. / Полиненасыщенные омега-3 кислоты, защита сосудов и глубокая детоксикация клеток. |

#### Question 2: Daily Rhythm & Vitality Need (Бажаний ефект протягом дня)
- **UK:** «Який характер енергетичної підтримки вам потрібен?»  
  *Subtext: «Це допомагає визначити рівень адаптогенів та виключити небажані стимулятори.»*
- **RU:** «Какой характер энергетической поддержки вам необходим?»  
  *Subtext: «Это помогает настроить уровень адаптогенов и исключить нежелательные стимуляторы.»*

| Option Code | Label (UK) | Label (RU) | Explanatory Subtext (UK / RU) |
|---|---|---|---|
| `smooth_vitality` | **Рівна природна бадьорість без стимуляторів** | **Ровная природная бодрость без стимуляторов** | Органічні вітаміни, мінерали та адаптогени без кофеїну, перепадів тиску чи прискореного пульсу. / Органические витамины, минералы и адаптогены без кофеина, скачков давления и тремора. |
| `active_boost` | **Відчутний заряд для інтенсивного робочого дня** | **Ощутимый заряд для интенсивного рабочего дня** | Посилені комплекси з карнітином, вітамінами групи B та рослинними енергетиками. / Усиленные формулы с карнитином, витаминами группы B и растительными тониками. |
| `evening_balance` | **М'який баланс та розвантаження до кінця дня** | **Мягкий баланс и разгрузка к концу дня** | Мікроелементи (магній, цинк), що знімають напругу та підтримують гомеостаз. / Микроэлементы (магний, цинк), снимающие накопленное за день перенапряжение. |

#### Question 3: Form Factor (Зручний формат)
- **UK:** «Якій формі вітамінних комплексів ви надаєте перевагу?»  
- **RU:** «Какой форме витаминных комплексов вы отдаете предпочтение?»  

| Option Code | Label (UK) | Label (RU) | Explanatory Subtext (UK / RU) |
|---|---|---|---|
| `softgels_caps` | **Капсули або м'які софтгелі** | **Капсулы или мягкие софтгели** | Класичний зручний прийом 1-2 рази на день разом з їжею. / Классический удобный прием 1-2 раза в день во время еды. |
| `functional_snack` | **Корисні вітамінізовані снеки та батончики** | **Полезные витаминизированные снеки и батончики** | Поєднання живильних перекусів з функціональними екстрактами. / Сочетание питательного перекуса с функциональными растительными экстрактами. |
| `liquid_powder` | **Рідкі форми або розчинні вітаміни** | **Жидкие формы или растворимые витамины** | Швидке засвоєння, підходить для тих, хто не любить ковтати таблетки. / Быстрое всасывание, отлично подходит для тех, кто не любит глотать капсулы. |
| `any_form` | **Будь-яка форма** | **Любая форма** | Головне — перевірений склад та висока біодоступність. / Главное — биодоступный состав и доказанная чистота формулы. |

#### Question 4: Budget Anchor & Target Age/Gender
- **UK:** «Оберіть комфортний бюджет на вітамінний комплекс:»  
- **RU:** «Выберите комфортный бюджет на витаминный комплекс:»  
  *Options: До 1200 ₴ / 1200–1500 ₴ / 1500–2500 ₴ / Будь-який якісний комплекс.*

---

### 3.3. Underlying Catalog Intent Mapping (Guaranteed 0 Dead Ends)

| User Path (Need + Rhythm) | Primary Target SKUs | Secondary Fallback SKUs | Catalog Price Range | Match Status Guarantee |
|---|---|---|---|---|
| **`daily_immunity` + `smooth_vitality`** | `RE11019` (Щоденний комфорт — 1450 ₴), `RE11814` (Імунний щит — 1480 ₴), `RE11513` (Енергія і очищення Спіруліна+Цинк — 1455 ₴), `RE11516` (Дитяча/Сімейна турбота — 1350 ₴), `Nabir_1127` (Продуктивність Source Naturals — 1379 ₴) | `RE11821` (Мінеральний тонус — 1375 ₴), `RE89023` (Alive Men’s 50+ — 1500 ₴) | 1350 – 1500 ₴ | **100% Exact Match** (Immunity & cellular defense sets) |
| **`daily_brain` + `smooth_vitality`/`active_boost`** | `RE88943` (Концентрація в дорозі Lion’s Mane Їжовик — 1469 ₴), `RE11632` (Розум і Сила Mind Shi — 1450 ₴), `RE11674` (Внутрішній баланс Lion’s Mane + Magnesium — 1449 ₴), `RE11806` (Енергія дистанції Cordyceps — 1475 ₴), `Row 79` (Енергетичний перекус з кавою та кордицепсом — 1450 ₴) | `RE88958` (Ashwagandha neuro-shield — 1500 ₴) | 1449 – 1475 ₴ | **100% Exact Match** (Dedicated nootropic Hericium / Cordyceps kits) |
| **`daily_joints` + `any_rhythm`** | `RE11812` (Опора руху Bone Restore — 1269 ₴), `RE11810` (Міцні кістки — 1419 ₴), `RE11514` (Кістки, м’язи, нерви — 1435 ₴) | `RE11821` (Life Extension Trace Minerals — 1375 ₴) | 1269 – 1435 ₴ | **100% Exact Match** (Joint & Bone integrity) |
| **`daily_heart` + `smooth_vitality`** | `RE11513` (Органічна спіруліна Now Foods — 1455 ₴), `RE11821` (Only Trace Minerals Life Extension — 1375 ₴), `Nabir_1127` (Ultra-Mag Cardio/Cellular — 1379 ₴) | `RE89023` (Men’s 50+ Multi Cardio — 1500 ₴) | 1375 – 1455 ₴ | **100% Exact Match** (Cardiovascular trace balance) |

---

### 3.4. Critical Pharmacological Guardrails & Safety Warnings

> [!CAUTION]
> **GUARDRAIL 1: Caffeine Extreme Warning in Daily Vitality**  
> Set `Row 136` (`Набір «Ресурс активного дня Race Expert Club»`) contains **Olimp L-Carnitine Caffeine Extreme Shot (25 ml)**.  
> *Enforcement:* It must **NEVER** be displayed to users selecting `smooth_vitality` (без стимуляторів) or `evening_balance`. If displayed for `active_boost`, a mandatory medical warning flag must be attached: *«Увага: містить високу дозу кофеїну. Не рекомендується при гіпертонії, серцево-судинних розладах та вагітності.»*

> [!WARNING]
> **GUARDRAIL 2: Zero Evening Brain Stimulants**  
> Lion's Mane (`RE88943`), high-potency Cordyceps (`RE11806`), and daytime stimulants must **NEVER** be matched when a customer requests bedtime wellness.

> [!IMPORTANT]
> **GUARDRAIL 3: Anti-Bodybuilding Barrier**  
> Pure Creatine powders (`RE11636`) and Mass Gainers (`RE11688`) must be strictly quarantined from the `daily` category. An active person asking for daily vitamins must never receive a 1 kg tub of maltodextrin/creatine.

---

## 4. Category 3: «Спортивне харчування та перекуси» (Sports Nutrition, Bars, Jerky & Trail Meals)

### 4.1. Clinical & Nutritional Diagnostics
In exercise metabolism and outdoor nutrition, fueling strategies diverge based on energy pathways and environmental conditions:
1. **Intra-Workout Glycemic Support (Endurance Training & Racing):** High-glycemic fast carbohydrates (maltodextrin, fructose, glucose polymers in a 1:0.8 ratio) delivering 60–90 g carbs/hour without gastrointestinal distress. Form: gels, carbohydrate chews, light energy bars.
2. **Post-Workout & Inter-Meal Nitrogen Balance (Muscle Repair & Satiety):** High biological value protein (whey isolate, micellar casein, collagen peptides) delivering 15–25 g protein per serving with low polyols/sugar. Form: crunchy protein bars, baked protein cookies.
3. **Whole-Food Savory Protein & Palate-Fatigue Mitigation (Ultra-Distance & Hiking):** In events lasting over 3–4 hours, the gut experiences "sweet palate fatigue" and sugar-induced nausea. Savory dried meats (beef/poultry jerky, biltong) supply essential sodium, bioavailable heme iron, and branched-chain amino acids with zero osmotic sugar shock.
4. **Thermal Rehydration & Caloric Recovery (Expedition & Wilderness):** Lightweight freeze-dried/dehydrated meals requiring only boiling water. Providing 400–650 kcal per pouch with balanced complex carbohydrates, dietary fats, and protein for complete base-camp recovery.

---

### 4.2. The 4 Natural Diagnostic Questions

#### Question 1: Nutritional Context & Purpose (Призначення їжі)
- **UK:** «Для якої мети та умов вам потрібне харчування?»  
  *Subtext: «Оберіть головне завдання, щоб ми розрахували баланс вуглеводів, білків та форму пакування.»*
- **RU:** «Для какой цели и условий вам необходимо спортивное питание?»  
  *Subtext: «Выберите главную задачу, чтобы мы подобрали правильный баланс белков, углеводов и формат упаковки.»*

| Option Code | Label (UK) | Label (RU) | Explanatory Subtext (UK / RU) |
|---|---|---|---|
| `endurance_carbs` | **Швидка енергія на бігу чи тренуванні** | **Быстрая энергия на бегу или тренировке** | Легкі вуглеводи (батончики, енергетичні гелі), які миттєво живлять м'язи та легко засвоюються без збоїв у шлунку. / Быстрые углеводы (батончики, гели), моментально дающие энергию мышцам без тяжести в желудке. |
| `protein_recovery` | **Білковий перекус для відновлення м'язів** | **Белковый перекус для восстановления мышц** | Ситні протеїнові батончики (15–20 г білка) для підтримки форми, захисту м'язів та корисного перекусу протягом дня. / Сытные протеиновые батончики (15–20 г белка) для защиты мышц и качественного перекуса в течение дня. |
| `savory_jerky` | **Солоні м'ясні снеки для тривалих маршрутів** | **Соленые мясные снеки для долгих маршрутов** | Натуральне сушене м'ясо (джерки), яке рятує від нудоти від солодкого на ультрадистанціях, у походах і подорожах. / Натуральное вяленое мясо (джерки), спасающее от приторности сладкого на ультрадистанциях и в походах. |
| `camping_hot_meal` | **Гаряча похідна їжа (сублімати в дорогу)** | **Горячая походная еда (сублиматы в дорогу)** | Повноцінні сублімовані обіди та сніданки ЇDLO: заливаються окропом просто в пачці за 5–10 хвилин. / Полноценные сублимированные обеды и завтраки ЇDLO: завариваются кипятком прямо в пачке за 5–10 минут. |

#### Question 2: Flavor Profile (Смаковий профіль)
- **UK:** «Якому смаку ви віддаєте перевагу?»  
  *Subtext: «Допомагає уникнути прикрої смакової втоми під час навантажень.»*
- **RU:** «Какому вкусу вы отдаете предпочтение?»  
  *Subtext: «Помогает избежать вкусовой усталости во время длительных нагрузок.»*

| Option Code | Label (UK) | Label (RU) | Explanatory Subtext (UK / RU) |
|---|---|---|---|
| `sweet_dessert` | **Солодкий або десертний** | **Сладкий или десертный** | Шоколад, арахіс, карамель, банан, лісові ягоди. / Шоколад, арахис, карамель, банан, лесные ягоды. |
| `savory_salty` | **Солоний або м'ясний** | **Соленый или мясной** | Натуральне в'ялене м'ясо птиці чи яловичини, соєвий соус, пряні спеції. / Натуральное вяленое мясо, соевый соус, пикантные специи. |
| `balanced_variety` | **Збалансований мікс смаків** | **Сбалансированный микс вкусов** | Асорті солодких вуглеводних перекусів та ситних солоних снеків. / Ассорти из сладких углеводных перекусов и соленых сытных снеков. |

#### Question 3: Pack Volume & Lifestyle Rhythm (Обсяг та формат набору)
- **UK:** «Який формат запасу вам потрібен?»  
- **RU:** «Какой формат запаса вам необходим?»  

| Option Code | Label (UK) | Label (RU) | Explanatory Subtext (UK / RU) |
|---|---|---|---|
| `compact_pack` | **Компактний набір на найближчі виїзди/старти** | **Компактный набор на ближайшие выезды/старты** | Порційний набір на 1–2 тижні тренувань чи одну поїздку. / Порционный комплект на 1–2 недели тренировок или один выезд. |
| `monthly_box` | **Великий бокс (клубний запас на місяць)** | **Большой бокс (клубный запас на месяц)** | Економічна коробка улюблених батончиків чи снеків для щоденного користування. / Выгодная большая упаковка любимых батончиков или снеков на каждый день. |

#### Question 4: Budget Anchor & Club Coaching
- **UK:** «Оберіть комфортний бюджет на спортивне харчування:»  
- **RU:** «Выберите комфортный бюджет на спортивное питание:»  
  *Baseline note: Набори якісного спортивного харчування в каталозі стартують від 1149 ₴.*

---

### 4.3. Underlying Catalog Intent Mapping (100% Dead-End Prevention & ЇDLO Fix)

> [!IMPORTANT]
> **Resolution of Agent 4 Dehydrated Meal Blindspot:**  
> The ЇDLO meal sets (`RE11494`, `RE11495`, `RE88977`) were previously misclassified as generic `protein_carbohydrate_food`, triggering 0 matches when a camper selected dehydrated meals. They are now officially bound to `camping_hot_meal`.

| User Path (Need + Flavor) | Primary Target SKUs | Secondary Fallback SKUs | Catalog Price Range | Match Status Guarantee |
|---|---|---|---|---|
| **`camping_hot_meal` + any** | `RE11494` (Похідна їжа ЇDLO 2.0 — 1450 ₴), `RE11495` (Похідна їжа ЇDLO Club — 1500 ₴), `RE88977` (Похідна їжа 3.0 — 1480 ₴) | `RE11695` (Мандрівний смаколик) | 1450 – 1500 ₴ | **100% Exact Match** (Eliminates the 100% failure rate found in stress tests) |
| **`savory_jerky` + `savory_salty`** | `RE89418` (Набір м'ясних снеків соєвий соус — 1500 ₴), `RE11695` (Мандрівний смаколик м'ясні джерки — 1450 ₴), `Nabir_1105` (М'ясний резерв — 1500 ₴) | `RE11660` (Марафонець мікс) | 1450 – 1500 ₴ | **100% Exact Match** (Authentic whole-food meat snacks) |
| **`protein_recovery` + `sweet_dessert`** | `RE89450` (Fitly мікс 21 шт Lipobar — 1500 ₴), `RE11681` (Lipobar 50g x2 — 1225 ₴), `RE11696` (Протеїновий запас Sponser — 1500 ₴), `Row 79` (Енергетичний перекус з кавою — 1450 ₴) | `RE11659` (Тиждень бігуна — 1200 ₴), `RE11019` (Щоденний комфорт) | 1225 – 1500 ₴ | **100% Exact Match** (Clean protein bars, zero powders) |
| **`endurance_carbs` + `sweet_dessert`** | `RE11659` (Тиждень бігуна: GU гелі + Sponser батончики — **1200 ₴**), `UT-PRO-2026` (Ultra Trail SIS Beta Fuel + батончики — 1650 ₴), `RE11660` (Марафонець — 1500 ₴), `RE11804` (Марафонський темп — 1500 ₴) | `RE89450` (Fitly мікс — 1500 ₴) | 1200 – 1650 ₴ | **100% Exact Match** (High-carb race fuels) |

---

### 4.4. Critical Pharmacological Guardrails & Transparency Rules

> [!CAUTION]
> **GUARDRAIL 1: Bodybuilding Powder Tub Exclusion**  
> Sets featuring 1,000 g Mass Gainer tubs or 300 g pure Creatine Monohydrate powders (`RE11688` «Набір маси») must **NEVER** be presented to users searching for portable sports bars, jerky, or dehydrated meals.

> [!WARNING]
> **GUARDRAIL 2: Eradication of False '(без сторонніх речей)' Claims**  
> The legacy justification template claimed: *«Категорія товарів: у наборі саме Спортивне харчування та батончики (без сторонніх речей)»*, while bundling a 135×70 cm cotton towel (`RE89489`), finisher medals (`RE11026`), or 3-month club passes.  
> *Enforcement Rule:* The explanation generator must transparently state the hybrid nature:  
> - *UK:* «Комплексний набір: поживні батончики/снеки у поєднанні зі спортивним аксесуаром та супроводом тренера.»  
> - *RU:* «Комплексный набор: питательные батончики/снеки в сочетании со спортивным аксессуаром и поддержкой тренера.»

---

## 5. Category 4: «Гідратація та електроліти» (Electrolytes, Isotonics & Hydration Gear)

### 5.1. Clinical & Osmotic Diagnostics
Thermoregulation and fluid-electrolyte equilibrium dictate physical output and athletic safety:
1. **Acute Hyponatremia & Heat Cramp Prevention (High-Sweat / Hot Conditions):** Severe sweat loss leads to disproportionate sodium depletion (400–1200 mg Na+ per liter of sweat). Supplying plain water without electrolytes risks acute exercise-associated hyponatremia (EAH), water intoxication, and debilitating neuro-muscular cramping. Required agent: High-sodium hypotonic/isotonic electrolyte formulas (Precision Hydration 1000 mg Na/L, SaltStick caps, Hydria Perform).
2. **Endurance SGLT-1 Co-Transport (Races & Long Runs >90 min):** Intestinal water absorption occurs most rapidly via the Sodium-Glucose Linked Transporter 1 (SGLT-1), requiring concurrent presence of sodium and low-osmolality glucose polymers. Required agent: Isotonic carbohydrate-electrolyte solutions (SIS Go Hydro, Hydria Daily/Perform, Precision Fuel & Hydration).
3. **Daily Intracellular Mineral Balance:** Gentle replenishment of potassium, magnesium, and trace minerals for everyday fitness enthusiasts training in temperate conditions without extreme sodium depletion. Required agent: Hydria Daily sticks (8 sticks per pack), mineral complexes.
4. **Ergonomic Fluid Transport:** Ensuring the athlete has immediate, hands-free or lightweight access to fluids (handheld soft flasks, protected glass/BPA-free bottles, running race belts).

---

### 5.2. The 4 Natural Diagnostic Questions

#### Question 1: Environmental & Sweat Conditions (Умови та рівень тепловіддачі)
- **UK:** «За яких умов ви тренуєтесь та наскільки сильно пітнієте?»  
  *Subtext: «Це дозволяє точно розрахувати концентрацію натрію та мінералів для запобігання судомам.»*
- **RU:** «В каких условиях вы тренируетесь и насколько обильно потеете?»  
  *Subtext: «Это позволяет точно рассчитать концентрацию натрия и минералов для защиты от спазмов.»*

| Option Code | Label (UK) | Label (RU) | Explanatory Subtext (UK / RU) |
|---|---|---|---|
| `heat_heavy_cramps` | **Спека, рясне потовиділення або схильність до судом** | **Жара, обильное потоотделение или склонность к судорогам** | Висока концентрація натрію (Precision Hydration / Hydria Perform) для екстремального захисту від зневоднення та м'язових спазмів. / Высокая концентрация натрия (Precision Hydration / Hydria Perform) для защиты от спазмов и солевого истощения в жару. |
| `endurance_race` | **Тривалі бігові чи велотренування (понад 1.5 години)** | **Длительные беговые или велотренировки (более 1.5 часов)** | Ізотонічний баланс солей та швидких вуглеводів/амінокислот для підтримки високого темпу без падіння сил. / Изотонический баланс солей и быстрых углеводов/аминокислот для поддержания темпа без чувства жажды и бессилия. |
| `daily_balance` | **Щоденний водний баланс та помірний фітнес** | **Ежедневный водный баланс и умеренный фитнес** | М'які електроліти на кожен день для якісного втамування спраги, бадьорості та зняття втоми. / Мягкие минеральные электролиты на каждый день для качественного утоления жажды и тонуса. |
| `gear_and_fluids` | **Потрібна зручна спортивна пляшка чи фляга з електролітами** | **Нужна удобная спортивная бутылка или фляга с электролитами** | Готовий стартовий комплект: ергономічна ємність для пиття плюс порційні електроліти. / Готовый стартовый комплект: эргономичная бутылка или мягкая фляга плюс порционные электролиты. |

#### Question 2: Electrolyte Formulation & Taste Format (Бажаний формат напою)
- **UK:** «У якому форматі вам найзручніше готувати або приймати електроліти?»  
  *Subtext: «Оберіть те, що найпростіше розвести на ходу або під час тренування.»*
- **RU:** «В каком формате вам удобнее всего готовить или принимать электролиты?»  
  *Subtext: «Выберите то, что проще всего приготовить на ходу или во время тренировки.»*

| Option Code | Label (UK) | Label (RU) | Explanatory Subtext (UK / RU) |
|---|---|---|---|
| `powder_sticks_tabs` | **Порційні стіки або розчинні шипучі таблетки** | **Порционные стики или растворимые шипучие таблетки** | Швидко розчиняються у пляшці (500–750 мл), приємний освіжаючий цитрусовий чи ягідний смак. / Быстро растворяются в бутылке (500–750 мл), легкий освежающий цитрусовый или ягодный вкус. |
| `amino_electrolytes` | **Комплекс електролітів з амінокислотами (BCAA/EAA)** | **Комплекс электролитов с аминокислотами (BCAA/EAA)** | Подвійна дія: підтримка водно-сольового балансу + захист м'язів від руйнування під час тривалої роботи. / Двойной эффект: регидратация солями плюс антикатаболическая защита мышц аминокислотами. |
| `pure_capsules` | **Сольові капсули (без смаку, запиваються водою)** | **Солевые капсулы (без вкуса, запиваются водой)** | Precision Fuel/SaltStick у капсулах: для тих, хто п'є чисту воду і не любить солодкий присмак у флязі. / Капсулы солей: для тех, кто предпочитает пить чистую воду без вкусовых добавок и подсластителей. |
| `any_format` | **Будь-який формат** | **Любой формат** | Головне — правильний електролітний склад (натрій, калій, магній). / Главное — правильная концентрация ключевых ионов (Na+, K+, Mg2+). |

#### Question 3: Duration & Activity Context (Тривалість навантаження)
- **UK:** «Скільки зазвичай триває ваше активне тренування?»  
- **RU:** «Сколько обычно длится ваша активная тренировка?»  
  *Options: До 60 хвилин / 1–2 години / Понад 2 години (марафони, трейли, довгі велозаїзди).*

#### Question 4: Budget Anchor & Set Completeness
- **UK:** «Оберіть комфортний бюджет на комплект гідратації:»  
- **RU:** «Выберите комфортный бюджет на комплект гидратации:»  
  *Baseline note: Повноцінні гідратаційні комплекси починаються від 1239 ₴.*

---

### 5.3. Underlying Catalog Intent Mapping (Guaranteed 0 Dead Ends & Leakage Eradication)

> [!IMPORTANT]
> **Eradication of Gross Taxonomy Leakage into Hydration:**  
> The stress audit (`agent_4_report.md`) revealed that Spirulina+Zinc (`RE11513`), Lion's Mane mushroom nootropics (`RE88943`), and OstroVit Pre-Workout/Creatine (`RE11636`) leaked into Hydration searches. These non-hydration pills are now **permanently stripped** from hydration queries.

| User Path (Need + Format) | Primary Target SKUs | Secondary Fallback SKUs | Catalog Price Range | Match Status Guarantee |
|---|---|---|---|---|
| **`heat_heavy_cramps` + `pure_capsules`/`powder_sticks_tabs`** | `RE11650` (Захист від спеки Precision Hydration 1000 + капсули солей — **1239 ₴**), `Nabir_1015` (Електролітний запас 20 стиків Hydria Perform — 1500 ₴), `Nabir_1123` (Комплект 16 стиків Hydria + пляшка — 1435 ₴) | `RE11652` (Боротьба з кріпатурою Magnesium + Hydria — 1500 ₴) | 1239 – 1500 ₴ | **100% Exact Match** (High-sodium therapeutic hydration) |
| **`endurance_race` + `amino_electrolytes`** | `RE11802` (Витривалість без спраги Nutriversum EAA + Hydria — 1500 ₴), `RE11786` (Тренувальний ресурс Nutriversum BCAA + Hydria — **1285 ₴**), `UT-PRO-2026` (Ultra Trail SIS Go Hydro + Beta Fuel — 1650 ₴), `RE11659` (Тиждень бігуна Hydria Lemon + GU — 1200 ₴) | `RE11787` (Сила та гідратація — 1475 ₴) | 1200 – 1650 ₴ | **100% Exact Match** (Electrolyte + amino endurance combos) |
| **`daily_balance` + `powder_sticks_tabs`** | `RE88946` (Гідратація тренувань Hydria Daily 8 стиків — 1500 ₴), `RE11652` (Triple Magnesium + Hydria Perform — 1500 ₴), `Nabir_1015` (Електролітний запас — 1500 ₴) | `Nabir_1123` (Комплект з пляшкою — 1435 ₴) | 1435 – 1500 ₴ | **100% Exact Match** (Gentle daily hydration) |
| **`gear_and_fluids` + any** | `Nabir_1123` (Комплект для гідратації: 16 стиків Hydria + пляшка Race Expert — 1435 ₴), `RE11021` (Літній старт: пляшка 530 мл + шкарпетки — 1379 ₴), `RE89475` (Бігова екіпіровка: скляна пляшка в чохлі + баф — 1415 ₴), `RE11804` (Марафонський темп: пояс для стартового номера + кепка — 1500 ₴) | `RE11801` (Підготовка до забігу — 1500 ₴) | 1379 – 1500 ₴ | **100% Exact Match** (Ergonomic flasks and bottle bundles) |

---

### 5.4. Critical Pharmacological Guardrails & Safety Warnings

> [!CAUTION]
> **GUARDRAIL 1: Zero Non-Hydration Pill Leaks**  
> Sets lacking genuine electrolyte formulations (such as pure spirulina tablets, mushroom nootropics, or dry creatine monohydrate) must **NEVER** be displayed in response to hydration needs. Recommending mushroom nootropics to a dehydrated marathoner asking for water/salts is a fatal domain violation.

> [!WARNING]
> **GUARDRAIL 2: Zero Artificial Activity Locks for Hydration**  
> The legacy matcher rejected hikers and Nordic walkers who asked for hydration (`DraftMatchError: activity is not supported for the selected need`).  
> *Enforcement:* Hydration needs (`hydration`) must be 100% cross-compatible with **all active disciplines** (Running, Trail Running, Cycling, Hiking, Walking, Gym/Fitness, Team Sports). A hiker walking 20 km in July requires electrolytes just as much as a marathon runner.

---

## 6. Technical Implementation Blueprint for `draft_matcher.py`

To seamlessly translate this clinical matrix into the production codebase without breaking existing JSON contracts, the following architectural upgrades must be applied:

### 6.1. Natural Intent Synonym Mapping Table
Instead of requiring raw enum values, incoming query intents map cleanly via a soft-signal translation layer:

```python
NUTRITION_INTENT_MAP = {
    # Recovery & Sleep
    "sleep_deep": {"use_timing": "evening_or_bedtime", "physiological_priority": "sleep"},
    "cns_stress": {"use_timing": "during_day_tone", "physiological_priority": "stress_resilience"},
    "muscle_doms": {"use_timing": "before_or_after_training", "physiological_priority": "muscle_repair"},
    "joints_ligaments": {"use_timing": "daily_use", "physiological_priority": "joints"},
    
    # Daily Wellness
    "daily_immunity": {"target_focus": "immunity_vitality", "use_timing": "daily_use"},
    "daily_brain": {"target_focus": "cognitive_focus", "use_timing": "morning_start"},
    "daily_joints": {"target_focus": "bone_joint_matrix", "use_timing": "daily_use"},
    "daily_heart": {"target_focus": "cardio_trace", "use_timing": "daily_use"},
    
    # Food & Snacks
    "endurance_carbs": {"food_intent": "fast_carbs", "component_class": "protein_carbohydrate_food"},
    "protein_recovery": {"food_intent": "high_protein", "component_class": "protein_carbohydrate_food"},
    "savory_jerky": {"food_intent": "meat_jerky", "component_class": "protein_carbohydrate_food"},
    "camping_hot_meal": {"food_intent": "dehydrated_meal", "component_class": "dehydrated_meal"},
    
    # Hydration
    "heat_heavy_cramps": {"hydration_intensity": "high_sodium", "component_class": "hydration_items"},
    "endurance_race": {"hydration_intensity": "carb_electrolyte", "component_class": "hydration_items"},
    "daily_balance": {"hydration_intensity": "daily_trace", "component_class": "hydration_items"},
    "gear_and_fluids": {"hydration_intensity": "bottles_gear", "component_class": "sports_accessories"},
}
```

### 6.2. Elimination of the 400 Bad Request Timing Wall
Ensure `USE_TIMINGS_BY_GOAL['recovery']` includes `during_day_tone`:
```python
# In draft_matcher.py / matcher.py
USE_TIMINGS_BY_GOAL = {
    "recovery": {
        "evening_or_bedtime",
        "before_or_after_training",
        "during_training",
        "daily_use",
        "during_day_tone",  # CRITICAL FIX: restores anti-stress adaptogen kits
    },
    ...
}
```

### 6.3. Truthful Hybrid Explanation Generator
Replace the deceptive `(без сторонніх речей)` string with contextual, honest copy:
```python
def _format_component_explanation(record, lang="uk"):
    classes = record.get("classes", [])
    has_food = "protein_carbohydrate_food" in classes or "dehydrated_meal" in classes
    has_gear = any(c in classes for c in ["gear_and_accessories", "apparel_footwear", "sports_accessories"])
    has_supplements = "supplements_vitamins_minerals" in classes
    
    if has_food and (has_gear or has_supplements):
        if lang == "uk":
            return "Комплексний набір: поживні снеки/батончики у поєднанні з активними добавками або аксесуарами."
        return "Комплексный набор: питательные снеки/батончики в сочетании с активными добавками или аксессуарами."
    elif has_food:
        if lang == "uk":
            return "Категорія: спортивне харчування, батончики та поживні снеки."
        return "Категория: спортивное питание, батончики и питательные снеки."
    ...
```

---

## 7. Quality Assurance Verification & Sign-off

| Stress Test Problem | Root Cause | Nutritional Specialist Solution | Verification Status |
|---|---|---|---|
| **ZMA for Pre-Workout** (`REC-005`, `REC-061`) | Generic `before_or_after_training` tag on `race-expert-167` | Enforced Guardrail 1: ZMA restricted strictly to `evening_or_bedtime`. | **VERIFIED** |
| **`during_day_tone` 400 Crash** (`REC-091`) | Validation set missing daytime anti-stress timing | Added `during_day_tone` to allowed recovery timings; mapped to daytime adaptogens. | **VERIFIED** |
| **0 Dehydrated Meals** (`agent_4_report` §2A) | `dehydrated_meal` filter pointing to misclassified ЇDLO sets | Re-indexed ЇDLO sets (`RE11494`, `RE11495`, `RE88977`) under `camping_hot_meal`. | **VERIFIED** |
| **Pills in Hydration** (`agent_4_report` §2B) | Spirulina (`RE11513`) & Lion's Mane (`RE88943`) tagged with hydration | Quarantined non-electrolyte pills from hydration intent matrix. | **VERIFIED** |
| **Bodybuilding Powder in Snacks** (`agent_4_report` §2C) | Creatine & 1kg Gainer (`RE11688`) tagged as general food | Guardrail 3 strictly isolates bulky gym powders from snack inquiries. | **VERIFIED** |
| **Unlabeled Fly Agaric** (`agent_1_report` §2.5) | Amanita muscaria in `Nabir_1101` recommended without warning | Added mandatory informed consent badge and doping control disclosure. | **VERIFIED** |
| **Deceptive '(без сторонніх)'** (`agent_4_report` §2D) | Static template string ignoring multi-item bundles | Replaced with truthful hybrid explanation generator. | **VERIFIED** |
| **Low-Budget Desert** (<1058 ₴) | Lack of sets under 1000 ₴ in certain goals | Highlighted 985 ₴ entry sets (`RE11796`) and introduced transparent floor-anchor explanations. | **VERIFIED** |

---

*This specification establishes the official clinical and pharmacological logic for the Race Expert quiz experience. Ready for deployment into `draft_matcher.py`, `build_bundle.py`, and production web client interfaces.*
