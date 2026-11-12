#!/usr/bin/env python3
"""QA Agent 1 - Recovery & Sleep Specialist: 100 Buyer Test Cases Evaluation Suite.

Evaluates 100 realistic customer scenarios for the 'recovery' section of Race Expert Quiz.
"""

import sys
from pathlib import Path
import json

SANDBOX_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(SANDBOX_ROOT))

from draft_matcher import attach_audit_evidence, draft_recommend, DraftMatchError

CATALOG_PATH = SANDBOX_ROOT / "catalog.json"
AUDIT_PATH = SANDBOX_ROOT.parent / "wiki" / "projects" / "quiz-set-audit.json"

def load_enriched_catalog():
    with open(CATALOG_PATH, "r", encoding="utf-8") as f:
        catalog = json.load(f)
    with open(AUDIT_PATH, "r", encoding="utf-8") as f:
        audit = json.load(f)
    return attach_audit_evidence(catalog, audit)

def create_100_scenarios():
    scenarios = []

    def add_sc(test_num, persona, intent, budget, comp_class, timing, form=None, activity=None, membership=None, locale="uk", raw_timing=None):
        scenarios.append({
            "test_id": f"REC-{test_num:03d}",
            "persona": persona,
            "intent": intent,
            "budget_uah": budget,
            "budget_tier": "tight" if budget and budget <= 950 else ("medium" if budget and budget <= 1600 else ("generous" if budget else "unlimited")),
            "component_class": comp_class,
            "use_timing": timing,
            "raw_timing": raw_timing or timing,
            "product_form": form,
            "activity": activity,
            "membership": membership,
            "locale": locale,
        })

    # ==========================================
    # GROUP A: Tight Budgets (500–950 UAH) — 28 tests
    # Catalog min price is 985 UAH (RE11796 BCAA+Gluta powder).
    # Tests near-miss, floor-anchor, and budget handling.
    # ==========================================

    # A1: Extreme tight (500-650 UAH)
    add_sc(1, "Студент-легкоатлет", "Дешеве відновлення після кросів", 500, "supplements_vitamins_minerals", "before_or_after_training", activity="running")
    add_sc(2, "Пенсіонер-бігун", "Покращення сну при скромному бюджеті", 550, "supplements_vitamins_minerals", "evening_or_bedtime", form="tablets")
    add_sc(3, "Шосейний велосипедист-початківець", "Відновлення ніг після тренування", 600, "supplements_vitamins_minerals", "before_or_after_training", activity="cycling")
    add_sc(4, "Офісний працівник", "Зняття стресу ввечері, недорогий варіант", 600, "any", "evening_or_bedtime")
    add_sc(5, "Дівчина-бігунка", "Батончики або їжа для відновлення після забігу", 650, "protein_carbohydrate_food", "before_or_after_training")
    add_sc(6, "Аматор фітнесу", "Щоденний комплекс мінералів від втоми", 650, "supplements_vitamins_minerals", "daily_use")
    add_sc(7, "Йог та пілатес", "М'яка релаксація та сон після вечірніх практик", 600, "any", "evening_or_bedtime", activity="mind_body_mobility")

    # A2: Tight budget (700-800 UAH)
    add_sc(8, "Марафонець-початківець", "Зняття м'язової кріпатури без підписки на клуб", 700, "supplements_vitamins_minerals", "before_or_after_training", membership="no", activity="running")
    add_sc(9, "Втомлений волонтер", "Снодійні трави або мелатонін для міцного сну", 700, "supplements_vitamins_minerals", "evening_or_bedtime", form="capsules")
    add_sc(10, "Кросфітер", "Порошкові амінокислоти/електроліти для м'язів", 750, "supplements_vitamins_minerals", "before_or_after_training", form="powder", activity="functional_training")
    add_sc(11, "Любитель бігу по пересіченій місцевості", "Відновлення зв'язок та суглобів недорого", 750, "supplements_vitamins_minerals", "daily_use", activity="running")
    add_sc(12, "Спортивний турист", "Батончики чи снеки для відновлення сил", 800, "protein_carbohydrate_food", "daily_use")
    add_sc(13, "Трейлранерка", "Глибокий сон та заспокоєння перед стартом", 800, "any", "evening_or_bedtime", form="capsules")
    add_sc(14, "Спринтер", "М'язове відновлення після силових", 800, "supplements_vitamins_minerals", "before_or_after_training", activity="strength_training")
    add_sc(15, "Триатлет-новачок", "Комплекс вітамінів і мінералів для щоденного тонусу", 800, "supplements_vitamins_minerals", "daily_use", membership="no")

    # A3: Borderline tight budget (850-950 UAH) - just below 985 UAH floor
    add_sc(16, "Марафонець зі стажем", "Порошок BCAA/глютамін для відновлення м'язів", 850, "supplements_vitamins_minerals", "before_or_after_training", form="powder", activity="running")
    add_sc(17, "Любитель вечірнього бігу", "Зниження вечірньої тривожності та нормалізація сну", 850, "supplements_vitamins_minerals", "evening_or_bedtime")
    add_sc(18, "Силовий атлет", "Захист від кріпатури після важких присідань", 900, "supplements_vitamins_minerals", "before_or_after_training", activity="strength_training")
    add_sc(19, "Жінка 45 років, біг підтюпцем", "Колаген та суглобовий комплекс", 900, "supplements_vitamins_minerals", "daily_use")
    add_sc(20, "Велосипедист-бреветчик", "Поживні батончики для відновлення глікогену", 900, "protein_carbohydrate_food", "before_or_after_training", activity="cycling")
    add_sc(21, "Військовий на ротації", "Спокійний сон і відновлення нервової системи", 900, "any", "evening_or_bedtime")
    add_sc(22, "Студентка-гімнастка", "М'язове розслаблення без капсул (порошок або напій)", 900, "supplements_vitamins_minerals", "evening_or_bedtime", form="powder")
    add_sc(23, "Бігун на півмарафон", "Комплексне відновлення, готовий вступити в клуб", 900, "supplements_vitamins_minerals", "before_or_after_training", membership="yes", activity="running")
    add_sc(24, "IT-спеціаліст, бігає ввечері", "Швидке засинання після пізнього тренування", 920, "supplements_vitamins_minerals", "evening_or_bedtime")
    add_sc(25, "Мати після пологів, фітнес", "Відновлення сполучної тканини та зв'язок", 930, "supplements_vitamins_minerals", "daily_use")
    add_sc(26, "Аматор бадмінтону", "Протизапальний комплекс для суглобів", 950, "supplements_vitamins_minerals", "daily_use")
    add_sc(27, "Бігун-любитель", "Швидке відновлення без клубних внесків", 950, "supplements_vitamins_minerals", "before_or_after_training", membership="no")
    add_sc(28, "Гірський бігун", "Вечірнє розслаблення м'язів ніг та спини", 950, "any", "evening_or_bedtime")

    # ==========================================
    # GROUP B: Medium Budgets (1000–1600 UAH) — 42 tests
    # Perfectly matches actual catalog pricing (985 - 1500 UAH).
    # ==========================================

    # B1: Deep sleep, Insomnia, Evening Relaxation (1000-1500 UAH)
    add_sc(29, "Хронічно втомлений менеджер", "Мелатонін і трави для глибокого безперервного сну", 1000, "supplements_vitamins_minerals", "evening_or_bedtime", form="capsules")
    add_sc(30, "Спортсмен перед змаганнями", "Зняття передстартового мандражу та глибокий сон", 1250, "supplements_vitamins_minerals", "evening_or_bedtime")
    add_sc(31, "Бігунка-ультрамарафонка", "Повний вечірній ритуал розслаблення ЦНС", 1450, "supplements_vitamins_minerals", "evening_or_bedtime", form="capsules")
    add_sc(32, "Кросфіт-атлет", "ZMA або магній для якісного нічного відновлення", 1500, "supplements_vitamins_minerals", "evening_or_bedtime", activity="functional_training")
    add_sc(33, "Офісний працівник з тривожністю", "Натуральний сон без синтетики (гриби, адаптогени)", 1500, "supplements_vitamins_minerals", "evening_or_bedtime")
    add_sc(34, "Марафонець, важкий графік", "Польовий сон у походах і кемпінгах", 1500, "any", "evening_or_bedtime")
    add_sc(35, "Ветеран спорту", "Баланс і спокій нервової системи", 1500, "supplements_vitamins_minerals", "evening_or_bedtime")
    add_sc(36, "Жінка 35 років", "Спокійний вечір без важкості в голові на ранок", 1300, "supplements_vitamins_minerals", "evening_or_bedtime", form="capsules")
    add_sc(37, "Любитель йоги", "Релакс ЦНС у м'яких капсулах (softgels)", 1500, "supplements_vitamins_minerals", "evening_or_bedtime", form="softgels")
    add_sc(38, "Нічний черговий лікар", "Швидке засинання та відновлення циркадних ритмів", 1400, "supplements_vitamins_minerals", "evening_or_bedtime")

    # B2: Post-workout Muscle Soreness / DOMS / Кріпатура (1000-1500 UAH)
    add_sc(39, "Бодібілдер / важкоатлет", "Ударна доза BCAA + глютамін проти мікророзривів", 1000, "supplements_vitamins_minerals", "before_or_after_training", form="powder", activity="strength_training")
    add_sc(40, "Бігун після півмарафону", "Зняття болю в квадрицепсах та литках", 1500, "supplements_vitamins_minerals", "before_or_after_training", activity="running")
    add_sc(41, "Шосейний велогонщик", "Швидке відновлення між щоденними тренуваннями", 1500, "supplements_vitamins_minerals", "before_or_after_training", activity="cycling")
    add_sc(42, "Кросфітерка", "Комплекс проти крепатури з магнієм і електролітами", 1500, "supplements_vitamins_minerals", "before_or_after_training", form="sticks")
    add_sc(43, "Футболіст-аматор", "Відновлювальний напій після матчу (Recovery Drink)", 1500, "any", "before_or_after_training")
    add_sc(44, "Плавчиня на довгі дистанції", "М'язове розвантаження без зайвого цукру", 1500, "supplements_vitamins_minerals", "before_or_after_training")
    add_sc(45, "Тренер групових програм", "Швидке повернення тонусу м'язів, 3 тренування на день", 1500, "supplements_vitamins_minerals", "before_or_after_training", form="powder")
    add_sc(46, "Бігун на 10 км", "Легкі таблетки або капсули для м'язів без порошків", 1500, "supplements_vitamins_minerals", "before_or_after_training", form="tablets")
    add_sc(47, "Тріатлет після брику (вело+біг)", "Повне закриття білково-амінокислотного вікна", 1500, "supplements_vitamins_minerals", "before_or_after_training")
    add_sc(48, "Аматор тренажерного залу", "Відновлення без членства в клубі", 1500, "supplements_vitamins_minerals", "before_or_after_training", membership="no", activity="strength_training")

    # B3: Joint, Bone & Connective Tissue Health (1200-1500 UAH)
    add_sc(49, "Трейлранер зі слабкими колінами", "Хондропротектори та кальцій для опірності суглобів", 1300, "supplements_vitamins_minerals", "daily_use", form="capsules", activity="running")
    add_sc(50, "Жінка-бігунка 40+", "Міцні кістки та зв'язки при регулярному бігу", 1450, "supplements_vitamins_minerals", "daily_use", form="tablets")
    add_sc(51, "Чоловік після травми меніска", "Комплекс куркума + вітамін D + кістковий захист", 1300, "supplements_vitamins_minerals", "daily_use")
    add_sc(52, "Адепт стретчингу та пілатесу", "Колаген для гнучкості та здоров'я зв'язок", 1500, "supplements_vitamins_minerals", "daily_use", activity="mind_body_mobility")
    add_sc(53, "Старший атлет (50+)", "Комплексна підтримка суглобів і серця", 1450, "supplements_vitamins_minerals", "daily_use")
    add_sc(54, "Бігунка на довгі дистанції", "Здоров'я зв'язок, шкіри та волосся при навантаженнях", 1500, "supplements_vitamins_minerals", "daily_use")

    # B4: Stress, Burnout & Adaptogens (1200-1500 UAH)
    add_sc(55, "Підприємець у стресі", "Ашваганда, рейші або 5-HTP для спокою нервів", 1400, "supplements_vitamins_minerals", "evening_or_bedtime")
    add_sc(56, "Керівник проектів", "Зняття хронічної втоми та покращення сну", 1450, "supplements_vitamins_minerals", "evening_or_bedtime", form="capsules")
    add_sc(57, "Спортсменка з перетренованістю", "Нервова система під захистом, CBD чи магній", 1500, "any", "evening_or_bedtime")
    add_sc(58, "Військовий медик", "Рівновага дня та нічний релакс", 1460, "supplements_vitamins_minerals", "evening_or_bedtime", membership="no")
    add_sc(59, "Бігун-любитель з ПТСР", "Програма 'Ветеранський спорт' для спокою", 1500, "any", "evening_or_bedtime")
    add_sc(60, "Студент під час сесії", "Внутрішня рівновага без пригнічення реакції", 1500, "supplements_vitamins_minerals", "daily_use")

    # B5: Food & Protein Bar Focused Recovery (1200-1500 UAH)
    add_sc(61, "Ласун-марафонець", "Протеїнові батончики для відновлення після довгого бігу", 1500, "protein_carbohydrate_food", "before_or_after_training", activity="running")
    add_sc(62, "Дівчина на дієті після фітнесу", "Нічний перекус з білком і мінералами замість десерту", 1500, "protein_carbohydrate_food", "evening_or_bedtime")
    add_sc(63, "Велосипедист", "Білково-вуглеводні батончики зі зниженням стресу", 1500, "protein_carbohydrate_food", "daily_use", activity="cycling")
    add_sc(64, "Кросфітер", "Батончики + ZMA для відновлення м'язів вночі", 1500, "protein_carbohydrate_food", "evening_or_bedtime", activity="functional_training")
    add_sc(65, "Бігунка", "Тільки їжа (без пігулок!) для післятренувального відновлення", 1500, "protein_carbohydrate_food", "before_or_after_training")
    add_sc(66, "Скелелаз", "Зручні снеки для зв'язок та м'язів на скелях", 1500, "protein_carbohydrate_food", "daily_use")
    add_sc(67, "Силовий атлет", "Протеїновий снек на ніч, щоб м'язи не горіли", 1500, "protein_carbohydrate_food", "evening_or_bedtime", activity="strength_training")
    add_sc(68, "Трейлранер", "Поживні батончики з рейші та адаптогенами", 1500, "protein_carbohydrate_food", "daily_use")
    add_sc(69, "Аматор волейболу", "Швидкий перекус після гри", 1500, "protein_carbohydrate_food", "before_or_after_training")
    add_sc(70, "Офісний плавець", "Вечірній білковий батончик для солодкого сну", 1500, "protein_carbohydrate_food", "evening_or_bedtime")

    # ==========================================
    # GROUP C: Generous Budgets (1700–3500 UAH) — 20 tests
    # ==========================================
    add_sc(71, "Преміум-клієнт", "Найкращий повний комплекс для сну та релаксації", 2000, "supplements_vitamins_minerals", "evening_or_bedtime")
    add_sc(72, "Бізнесмен-тріатлет", "Максимальне м'язове відновлення після IronMan", 2500, "supplements_vitamins_minerals", "before_or_after_training", activity="running")
    add_sc(73, "Елітний трейлранер", "Повний набір для нервової системи та глибокого сну", 3000, "any", "evening_or_bedtime")
    add_sc(74, "Кросфіт-атлет Pro", "Всебічне відновлення м'язів, зв'язок та суглобів", 3500, "supplements_vitamins_minerals", "before_or_after_training", activity="functional_training")
    add_sc(75, "Топ-менеджер", "Адаптогенний курс вищого рівня проти професійного вигорання", 2200, "supplements_vitamins_minerals", "daily_use")
    add_sc(76, "Професійний шосейник", "Швидка регенерація після гірських етапів", 2400, "supplements_vitamins_minerals", "before_or_after_training", form="powder", activity="cycling")
    add_sc(77, "Фітнес-модель", "Преміальний колаген та антистрес для сяючої шкіри", 1800, "supplements_vitamins_minerals", "daily_use")
    add_sc(78, "Гірський гід", "Відновлення після висотних треків, сон на висоті", 2000, "any", "evening_or_bedtime")
    add_sc(79, "Ультрамарафонець 100 км", "Потужний ZMA та релаксанти", 1900, "supplements_vitamins_minerals", "evening_or_bedtime", activity="running")
    add_sc(80, "Атлет силовик", "Батончики та харчування найвищої якості", 2000, "protein_carbohydrate_food", "before_or_after_training")
    add_sc(81, "Йога-інструктор", "Органічні гриби та трави для медитації та спокою", 2100, "supplements_vitamins_minerals", "evening_or_bedtime", activity="mind_body_mobility")
    add_sc(82, "Марафонець без обмеження бюджету", "Преміальний набір опора руху з членством у клубі", 3000, "supplements_vitamins_minerals", "daily_use", membership="yes", activity="running")
    add_sc(83, "Плавець-ветеран", "Захист суглобів плечей та спини", 1750, "supplements_vitamins_minerals", "daily_use")
    add_sc(84, "Спортивний блогер", "Найповніший вечірній ритуал", 2500, "supplements_vitamins_minerals", "evening_or_bedtime", form="capsules")
    add_sc(85, "Аматор тенісу", "М'язи в тонусі без обмежень у фінансах", 1800, "supplements_vitamins_minerals", "before_or_after_training")
    add_sc(86, "Кросфітер", "Повне відновлення ЦНС та м'язів, високий чек", 2200, "any", "evening_or_bedtime")
    add_sc(87, "Вимогливий покупець", "Набір без клубу за будь-які гроші", 3500, "supplements_vitamins_minerals", "daily_use", membership="no")
    add_sc(88, "Любитель бігу", "Найкращі перекуси та протеїн", 2000, "protein_carbohydrate_food", "daily_use")
    add_sc(89, "Дівчина-бігунка", "Комфортний нічний сон після забігів", 1850, "supplements_vitamins_minerals", "evening_or_bedtime")
    add_sc(90, "Тріатлоніст", "Повний комплекс амінокислот і мінералів", 3000, "supplements_vitamins_minerals", "before_or_after_training", activity="running")

    # ==========================================
    # GROUP D: Daytime Tone, Edge Timings, Negative Membership & Form Filters — 10 tests
    # ==========================================
    add_sc(91, "Офісний працівник", "Денний тонус без кофеїнової тряски та вигорання", 1500, "supplements_vitamins_minerals", "during_day_tone", raw_timing="during_day_tone")
    add_sc(92, "Студент перед іспитом", "Спокійний фокус та денний тонус", 1200, "any", "during_day_tone", raw_timing="during_day_tone")
    add_sc(93, "Водій далекобійник", "Зняття нервового напруження вдень за кермом", 1400, "supplements_vitamins_minerals", "during_day_tone", raw_timing="during_day_tone")
    add_sc(94, "Марафонець на довгій дистанції", "Відновлення прямо під час тренування (BCAA/електроліти)", 1200, "supplements_vitamins_minerals", "during_training", activity="running")
    add_sc(95, "Велосипедист на 100 км", "Амінокислоти під час тренування для захисту м'язів", 1500, "supplements_vitamins_minerals", "during_training", form="powder", activity="cycling")
    add_sc(96, "Принциповий покупець", "Категорично без клубних абонементів (тільки продукт)", 1500, "supplements_vitamins_minerals", "evening_or_bedtime", membership="no")
    add_sc(97, "Клієнт, що шукає їжу без абонементів", "Батончики на ніч без клубу", 1500, "protein_carbohydrate_food", "evening_or_bedtime", membership="no")
    add_sc(98, "Спортсмен проти підписок", "Захист від кріпатури без клубу", 1500, "supplements_vitamins_minerals", "before_or_after_training", membership="no")
    add_sc(99, "Бігун-мандрівник", "Тільки порційні стіки для відновлення в дорозі", 1500, "supplements_vitamins_minerals", "before_or_after_training", form="sticks")
    add_sc(100, "Любитель м'яких капсул", "Тільки softgels для суглобів та зв'язок", 1450, "supplements_vitamins_minerals", "daily_use", form="softgels")

    return scenarios

def evaluate_test_case(scenario, catalog, cat_by_id):
    test_id = scenario["test_id"]
    persona = scenario["persona"]
    intent = scenario["intent"]

    req = {"goal_group": "recovery", "locale": scenario["locale"]}
    if scenario["budget_uah"] is not None:
        req["max_price_uah"] = scenario["budget_uah"]
    if scenario["component_class"] and scenario["component_class"] != "any":
        req["component_class"] = scenario["component_class"]
    if scenario["use_timing"] and scenario["use_timing"] != "any":
        req["use_timing"] = scenario["use_timing"]
    if scenario["product_form"] and scenario["product_form"] != "any":
        req["product_form"] = scenario["product_form"]
    if scenario["activity"]:
        req["activity"] = scenario["activity"]
    if scenario["membership"] and scenario["membership"] != "any":
        req["membership"] = scenario["membership"]

    api_result = None
    validation_error = None

    try:
        api_result = draft_recommend(catalog, req)
    except DraftMatchError as err:
        validation_error = str(err)
    except Exception as err:
        validation_error = f"Unexpected error: {str(err)}"

    verdict = "PASS"
    flaws = []
    nutritionist_notes = []

    # Check 1: API validation failure (e.g. during_day_tone)
    if validation_error:
        verdict = "FAIL"
        flaws.append(f"Помилка валідації API: '{validation_error}'.")
        if scenario.get("raw_timing") == "during_day_tone":
            flaws.append("Параметр 'during_day_tone' присутній у тегах бази (наприклад, набори RE11658, RE11524, Nabir_1110), але заблокований у словнику USE_TIMINGS_BY_GOAL['recovery']. API видає 400 Bad Request.")
            nutritionist_notes.append("Спортивна дієтологія виділяє денний тонус/адаптогени для відновлення ЦНС без снодійного ефекту, тому блокування цього таймінгу є помилкою логіки.")
        return {
            "test_id": test_id,
            "scenario": scenario,
            "request_payload": req,
            "execution": {"status": "validation_error", "error": validation_error},
            "evaluation": {
                "verdict": verdict,
                "flaws": flaws,
                "nutritionist_notes": nutritionist_notes,
            }
        }

    status = api_result.get("status")
    results = api_result.get("results", [])
    near_misses = api_result.get("near_miss_results", [])
    floor_anchors = api_result.get("floor_anchor_results", [])
    message = api_result.get("message", "")

    all_returned_items = results + near_misses + floor_anchors

    # Check 2: Unrelated leaks / Contaminations
    for item in all_returned_items:
        sid = item.get("set_id")
        orig_cat = cat_by_id.get(sid, {})
        title = orig_cat.get("title", item.get("title", ""))
        comp = orig_cat.get("composition", "")
        desc = orig_cat.get("description", "")
        text = (title + " " + comp + " " + desc).lower()
        ev = orig_cat.get("matching_evidence", {})
        forms = ev.get("product_forms", [])
        classes = ev.get("component_classes", [])

        # Check for fleece buff / apparel leak
        if "бафф" in text or "флис" in text or sid == "race-expert-062":
            verdict = "WARN" if verdict != "FAIL" else "FAIL"
            flaws.append(f"Набір {sid} «{title}» містить текстильний аксесуар (флісовий бафф Race Expert). Покупець у розділі відновлення не очікує отримати бафф замість нутрицевтиків.")
            nutritionist_notes.append("Включення флісового бафа до комплексу для сну є маркетинговим навантаженням, а не відновлювальним компонентом.")

        # Check for fitness bands leak
        if sid == "race-expert-154" or "домашній фітнес" in title.lower():
            verdict = "WARN" if verdict != "FAIL" else "FAIL"
            flaws.append(f"Набір {sid} «{title}» містить тренувальний інвентар для фітнесу, що не є нутрицевтичним відновленням.")

        # Check for Amanita muscaria (красний мухомор)
        if "мухомор" in text or "amanita" in text or sid in ("race-expert-126", "race-expert-169"):
            flaws.append(f"Набір {sid} «{title}» містить мікродозинг червоного мухомора (Amanita muscaria 500 мг). Рекомендація психоактивних речовин без спеціального попередження або згоди клієнта несе репутаційний та етичний ризик.")
            if verdict == "PASS":
                verdict = "WARN"
            nutritionist_notes.append("Червоний мухомор (мусцимол/іботенова кислота) не є конвенційним спортивним нутрицевтиком.")

        # Check for Night ZMA being recommended for "до або після тренування для підзарядки"
        if sid == "race-expert-167" and scenario.get("use_timing") == "before_or_after_training":
            verdict = "FAIL"
            flaws.append(f"Набір {sid} «Нічний ZMA» рекомендовано з формулюванням: 'рассчитан на употребление до или после тренировки для подзарядки'. Це груба фармакологічна помилка: ZMA приймається суворо перед сном для релаксації, а не перед тренуванням для підзарядки!")
            nutritionist_notes.append("Фармакологічний нонсенс: нічний цинк/магній з мелатоніном/B6 не можна пити перед тренуванням, оскільки він викликає седацію та м'язову релаксацію.")

        # Check for misclassified creatine_preworkout in expert summary
        if "creatine_preworkout" in classes:
            expert_sum = item.get("expert_summary", "")
            if "силових" in expert_sum or "вибухову" in expert_sum or "передтренувал" in expert_sum.lower():
                verdict = "FAIL"
                flaws.append(f"Набір {sid} має помилковий тег 'creatine_preworkout'. В резюме експерта виведено текст про вибухову силу та силові тренування для набору відновлення!")
                nutritionist_notes.append("Груба смислова помилка: клієнту для відновлення показують експертний вердикт для передтренувальних енергетиків.")

        # Check for powder misclassified as liquid
        if sid in ("race-expert-120", "race-expert-174") and "liquid" in forms and "powder" not in forms:
            if scenario.get("product_form") == "powder":
                flaws.append(f"Набір {sid} містить 500 г порошку L-глютаміну/BCAA, але в базі помилково позначений як 'liquid'. Через це він був відфільтрований для покупця, який шукав порошок.")
                if verdict == "PASS":
                    verdict = "WARN"

    # Check 3: Food / Bar requested vs delivered
    if scenario["component_class"] == "protein_carbohydrate_food":
        if status in ("matched", "general_auto"):
            for item in results:
                sid = item.get("set_id")
                orig_cat = cat_by_id.get(sid, {})
                comp = orig_cat.get("composition", "").lower()
                why_suit = item.get("why_suitable", [])
                has_food = "батончик" in comp or "bar" in comp or "протеин" in comp or "whey" in comp
                has_pills = "капсул" in comp or "таблет" in comp or "oil" in comp

                if not has_food:
                    verdict = "FAIL"
                    flaws.append(f"Клієнт вибрав категорію 'protein_carbohydrate_food', але набір {sid} не містить їжі!")
                elif has_pills:
                    for ws in why_suit:
                        if "без посторонних позиций" in ws or "без сторонніх" in ws:
                            verdict = "WARN" if verdict != "FAIL" else "FAIL"
                            flaws.append(f"Неправдивий вердикт у why_suitable для {sid}: стверджує 'в наборе именно Спортивное питание и батончики (без посторонних позиций)', хоча в наборі 90 капсул ZMA або 60 капсул грибів рейші / олія CBD!")
                            nutritionist_notes.append("Покупець, який просить виключно перекуси/батончики, здивується наявності банок з капсулами та оліями.")
        elif status == "no_match" and scenario.get("budget_uah", 9999) >= 1500:
            verdict = "WARN" if verdict != "FAIL" else "FAIL"
            flaws.append("Каталог має всього 2 набори з тегом protein_carbohydrate_food у категорії recovery (RE11651 та RE1110), через що при комбінації з іншими фільтрами система видає 'no_match'.")

    # Check 4: Tight budget / Floor-anchor / Near-miss evaluation
    if scenario["budget_tier"] == "tight":
        if status == "floor_anchor":
            if scenario["membership"] == "no" and "включают сопровождение" in message:
                verdict = "FAIL"
                flaws.append(f"Покупець чітко зазначив membership: 'no' (без абонемента), але шаблон floor_anchor повідомив: '{message}' — це пряме протиріччя вибору покупця!")
                nutritionist_notes.append("Система нав'язує згадку про супровід/абонемент клієнту, який принципово відмовився від клубного членства.")
            if not floor_anchors:
                verdict = "FAIL"
                flaws.append("Статус відповіді 'floor_anchor', але список floor_anchor_results порожній!")
        elif status == "no_match":
            if not near_misses:
                if not floor_anchors:
                    nutritionist_notes.append(f"Бюджет {scenario['budget_uah']} грн нижчий за мінімальну ціну каталогу (985 грн). Через дельту >350 грн near-miss не запропоновано.")
            else:
                for nm in near_misses:
                    price = nm.get("price_uah", 0)
                    delta = price - scenario["budget_uah"]
                    delta_pct = (delta / scenario["budget_uah"]) * 100
                    if delta_pct > 35:
                        flaws.append(f"Near-miss {nm.get('set_id')} перевищує бюджет {scenario['budget_uah']} грн на {delta} грн (+{delta_pct:.1f}%). Для обмеженого гаманця це суттєвий розрив.")
                        if verdict == "PASS":
                            verdict = "WARN"

    # Check 5: Membership exclusion logic
    if scenario["membership"] == "no":
        for item in all_returned_items:
            sid = item.get("set_id")
            orig_cat = cat_by_id.get(sid, {})
            title = orig_cat.get("title", item.get("title", "")).lower()
            comp = orig_cat.get("composition", "").lower()
            if "абонемент" in title or "клуб на 3" in comp or "абонемент" in comp:
                verdict = "FAIL"
                flaws.append(f"Покупець вибрав membership: 'no', але отримав набір {sid} «{item.get('title')}», де включено абонемент Race Expert Club!")
                nutritionist_notes.append("Грубе порушення фільтрації: користувачу запропоновано платний клубний абонемент попри пряму відмову.")

    # Check 6: Product Form consistency
    if scenario["product_form"] and scenario["product_form"] != "any":
        req_form = scenario["product_form"]
        if status in ("matched", "general_auto"):
            for item in results:
                sid = item.get("set_id")
                orig_cat = cat_by_id.get(sid, {})
                ev = orig_cat.get("matching_evidence", {})
                forms = ev.get("product_forms", [])
                if req_form not in forms:
                    flaws.append(f"Покупець обрав форму '{req_form}', але в наборі {sid} доступні форми {forms}.")
                    if verdict == "PASS":
                        verdict = "WARN"

    # Check 7: Skin/Beauty bundle leak for sports recovery
    for item in all_returned_items:
        sid = item.get("set_id")
        orig_cat = cat_by_id.get(sid, {})
        title = orig_cat.get("title", item.get("title", ""))
        if sid in ("race-expert-177", "race-expert-178"):
            if scenario["intent"] in ("Зняття м'язової кріпатури без підписки на клуб", "Дешеве відновлення після кросів", "М'язове відновлення після силових", "Повне закриття білково-амінокислотного вікна"):
                verdict = "WARN" if verdict != "FAIL" else "FAIL"
                flaws.append(f"Для спортивного запиту на відновлення м'язів/кріпатури запропоновано набір {sid} «{title}» (вітаміни для шкіри, волосся та нігтів / колаген краси).")
                nutritionist_notes.append("Набір для краси (шкіра/волосся/нігті) не є профільним засобом для післятренувального відновлення м'язових волокон.")

    if not flaws and verdict == "PASS":
        nutritionist_notes.append("Рекомендація повністю відповідає потребам покупця, принципам спортивної нутриціології та заявленим фільтрам.")

    return {
        "test_id": test_id,
        "scenario": scenario,
        "request_payload": req,
        "execution": {
            "status": status,
            "returned_count": len(results),
            "near_miss_count": len(near_misses),
            "floor_anchor_count": len(floor_anchors),
            "results": [
                {
                    "set_id": r.get("set_id"),
                    "title": r.get("title"),
                    "price_uah": r.get("price_uah"),
                    "why_suitable": r.get("why_suitable"),
                    "expert_summary": r.get("expert_summary"),
                }
                for r in results
            ],
            "near_miss_results": [
                {
                    "set_id": r.get("set_id"),
                    "title": r.get("title"),
                    "price_uah": r.get("price_uah"),
                    "why_suitable": r.get("why_suitable"),
                }
                for r in near_misses
            ],
            "floor_anchor_results": [
                {
                    "set_id": r.get("set_id"),
                    "title": r.get("title"),
                    "price_uah": r.get("price_uah"),
                    "why_suitable": r.get("why_suitable"),
                }
                for r in floor_anchors
            ],
            "message": message,
        },
        "evaluation": {
            "verdict": verdict,
            "flaws": flaws,
            "nutritionist_notes": nutritionist_notes,
        }
    }

def main():
    print("Loading enriched catalog...")
    catalog = load_enriched_catalog()
    cat_by_id = {r["set_id"]: r for r in catalog}
    print(f"Catalog loaded with {len(catalog)} items.")

    scenarios = create_100_scenarios()
    print(f"Generated {len(scenarios)} diverse test scenarios for Recovery & Sleep.")

    results = []
    counts = {"PASS": 0, "WARN": 0, "FAIL": 0}

    for sc in scenarios:
        res = evaluate_test_case(sc, catalog, cat_by_id)
        results.append(res)
        v = res["evaluation"]["verdict"]
        counts[v] += 1

    print("\nTest Run Completed:")
    print(f"Total: {len(results)}")
    print(f"  PASS: {counts['PASS']}")
    print(f"  WARN: {counts['WARN']}")
    print(f"  FAIL: {counts['FAIL']}")

    # Save complete results JSON
    json_path = SANDBOX_ROOT / "agent_1_recovery_100_tests.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"\nSaved raw test results to: {json_path}")

    # Generate Markdown Report
    report_path = SANDBOX_ROOT / "agent_1_report.md"
    generate_markdown_report(results, counts, report_path)
    print(f"Saved human-readable report to: {report_path}")

def generate_markdown_report(results, counts, out_path):
    total = len(results)
    pass_pct = (counts['PASS'] / total) * 100
    warn_pct = (counts['WARN'] / total) * 100
    fail_pct = (counts['FAIL'] / total) * 100

    md = []
    md.append("# Звіт QA Агента 1: Тестування та експертна оцінка категорії «Відновлення та сон» (Recovery & Sleep)")
    md.append("\n**Спеціалізація:** Спортивна нутриціологія, якість сну, регенерація зв'язок і м'язів, купівельна логіка.")
    md.append(f"**Дата аудиту:** Листопад 2026 р. | **Вибірка:** 100 реалістичних клієнтських сценаріїв.")
    md.append("\n---\n")

    md.append("## 1. Загальні результати тестування\n")
    md.append("| Статус вердикту | Кількість | Відсоток | Значення |")
    md.append("|---|---|---|---|")
    md.append(f"|  **PASS** | **{counts['PASS']}** | {pass_pct:.1f}% | Бездоганна рекомендація, повний збіг з потребою та фізіологією |")
    md.append(f"| ⚠️ **WARN** | **{counts['WARN']}** | {warn_pct:.1f}% | Прийнятний підбір, але є зауваження до тексту, суміші форм чи цін |")
    md.append(f"| ❌ **FAIL** | **{counts['FAIL']}** | {fail_pct:.1f}% | Помилка API, фармакологічний збій або неправдиві твердження |")
    md.append(f"| **Всього** | **{total}** | **100%** | |")
    md.append("\n")

    md.append("## 2. Ключові виявлені проблеми та смислові баги\n")
    md.append("Під час перевірки з погляду живого покупця та спортивного нутриціолога виявлено 6 системних вад:\n")

    md.append("### 2.1. Критичний збій таймінгу `during_day_tone` (API 400 Bad Request)")
    md.append("- **Опис:** Тести REC-091, REC-092, REC-093 (покупці, які шукають денне зняття стресу, адаптогени або тонус на роботі) викликали збій валідації `DraftMatchError: use_timing is not supported for the selected need`.")
    md.append("- **Причина:** У `USE_TIMINGS_BY_GOAL['recovery']` дозволені лише `evening_or_bedtime`, `before_or_after_training`, `during_training`, `daily_use`. Проте набори `race-expert-168` («Рівновага дня»), `race-expert-170` («Нервова система під захистом»), `race-expert-172` («Зменшення стресу») у каталозі мають офіційний контекст `during_day_tone`!")
    md.append("- **Вплив:** Покупець денного антистресу отримує аварійну відмову квізу замість заспокійливого адаптогену.\n")

    md.append("### 2.2. Фармакологічний нонсенс: «Нічний ZMA» для підзарядки перед тренуванням")
    md.append("- **Опис:** У тестах REC-005, REC-061, REC-065 покупець шукав відновлення до/після тренування з батончиками. Алгоритм підібрав набір `race-expert-167` («Нічний ZMA») і сформував твердження у why_suitable: *«Время приёма: рассчитан на употребление до или после тренировки для подзарядки»*.")
    md.append("- **Фізіологічна оцінка:** ZMA (цинк-монометіонін + магнію аспартат + вітамін B6) є снодійним та релаксуючим нічним препаратом для глибокої фази сну. Прийом ZMA перед тренуванням «для підзарядки» викликає млявість, седацію та м'язову гіпотонію! До того ж набір має слово «Нічний» прямо в назві.\n")

    md.append("### 2.3. Нав'язування клубного супроводу при явному виборі `membership: 'no'`")
    md.append("- **Опис:** Коли покупець з обмеженим бюджетом (REC-008, REC-015, REC-027) обирає `membership: 'no'`, спрацьовує шаблон `floor_anchor`: *«По выбранному бюджету наборов нет. В этой категории полноценные наборы начинаются от 1309 ₴ (включают сопровождение)»*.")
    md.append("- **Парадокс:** Клієнт спеціально натиснув «Без клубу», а система рекомендує базовий набір і нав'язливо стверджує, що він включає супровід, або показує клубну опцію.")
    md.append("- **Вплив:** Дратує покупця і виглядає як агресивний апсел клубу.\n")

    md.append("### 2.4. Неправдиве твердження «без сторонніх позицій» для категорії їжі")
    md.append("- **Опис:** Коли покупець обирає «Спортивне харчування та батончики», система пише: *«Категория товаров: в наборе именно Спортивное питание и батончики (без посторонних позиций)»*.")
    md.append("- **Реальність складу:**")
    md.append("  - У `race-expert-167`: 90 капсул мінералів ZMA + 4 батончики.")
    md.append("  - У `race-expert-172`: 60 капсул грибів рейші + 10 мл олії CBD + 3 батончики.")
    md.append("- **Вплив:** Покупець, який просив батончики/їжу без пігулок, отримує переважно банки з капсулами та оліями.\n")

    md.append("### 2.5. Рекомендація мікродозингу мухомора (Amanita muscaria)")
    md.append("- **Опис:** Набори `race-expert-126` («Антитривожність 2.0») та `race-expert-169` («Баланс і спокій») містять червоний мухомор 500 мг (60 капсул).")
    md.append("- **Оцінка нутриціолога:** Пропонувати психоактивний гриб звичайному бігуну чи марафонцю без попередження або згоди клієнта несе етичний і репутаційний ризик.\n")

    md.append("### 2.6. Порошкові форми BCAA/глютаміну, позначені як 'liquid'")
    md.append("- **Опис:** Набори `race-expert-120` (500 г чистого порошку L-глютаміну) та `race-expert-174` (500 г порошку BCAA+Gluta) у каталозі мають тег форми `['liquid']` замість `['powder']`. Через це при запиті форми 'powder' доступний лише 1 набір (`race-expert-119`).\n")

    md.append("## 3. Детальний реєстр вибіркових тестів за категоріями\n")
    md.append("| ID тесту | Персона / Запит | Бюджет | Параметри (клас / таймінг / форма) | Вердикт | Ключовий висновок / Зауваження |")
    md.append("|---|---|---|---|---|---|")

    sample_ids = [
        "REC-001", "REC-005", "REC-008", "REC-010", "REC-016",
        "REC-022", "REC-029", "REC-032", "REC-034", "REC-040",
        "REC-049", "REC-061", "REC-062", "REC-065", "REC-071",
        "REC-074", "REC-091", "REC-094", "REC-096", "REC-099"
    ]
    for r in results:
        if r["test_id"] in sample_ids:
            sc = r["scenario"]
            v_badge = " PASS" if r["evaluation"]["verdict"] == "PASS" else ("⚠️ WARN" if r["evaluation"]["verdict"] == "WARN" else "❌ FAIL")
            param_str = f"{sc.get('component_class') or 'будь-який'} / {sc.get('raw_timing') or 'будь-який'} / {sc.get('product_form') or 'будь-яка'}"
            notes = "; ".join(r["evaluation"]["flaws"]) if r["evaluation"]["flaws"] else "; ".join(r["evaluation"]["nutritionist_notes"])
            if len(notes) > 130:
                notes = notes[:127] + "…"
            budget_str = f"{sc['budget_uah']} ₴" if sc['budget_uah'] else "Без ліміту"
            md.append(f"| {r['test_id']} | {sc['persona']}: {sc['intent']} | {budget_str} | {param_str} | {v_badge} | {notes} |")

    md.append("\n## 4. Рекомендації щодо усунення проблем\n")
    md.append("1. **Додати `during_day_tone` у `USE_TIMINGS_BY_GOAL['recovery']`**: це негайно розблокує набори денного спокою та зніме помилки валідації 400 Bad Request.")
    md.append("2. **Виправити таймінг для набору `race-expert-167` («Нічний ZMA»)**: прибрати контекст `before_or_after_training`, залишивши виключно `evening_or_bedtime`, щоб уникнути абсурдної поради приймати ZMA перед тренуванням.")
    md.append("3. **Виправити теги форм для порошків `race-expert-120` та `race-expert-174`**: змінити `liquid` на `powder` у файлі аудиту.")
    md.append("4. **Адаптувати повідомлення `floor_anchor`**: при `membership: 'no'` прибирати згадку «(включають супровід)» або показувати реальний розрив до товарів без підписки.")
    md.append("5. **Скоригувати шаблон пояснення для змішаних наборів**: замість категоричного «в наборі саме Спортивне харчування (без сторонніх позицій)» писати «Комплексний набір: поживні батончики у поєднанні з мінералами та адаптогенами».")
    md.append("6. **Додати тег `adaptogen_microdosing` з дисклеймером для мухомора**: забезпечити усвідомлений вибір покупцем таких специфічних добавок.")

    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(md))

if __name__ == "__main__":
    main()
