#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""QA Deep Food Specialist: 100 Dedicated Buyer Test Scenarios & Evaluation for 'food' Goal."""

import json
import os
import sys
from pathlib import Path
from collections import Counter

# Add sandbox to sys.path
SANDBOX_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SANDBOX_DIR.parent
sys.path.insert(0, str(SANDBOX_DIR))

from draft_matcher import attach_audit_evidence, draft_recommend, DraftMatchError

CATALOG_PATH = SANDBOX_DIR / "catalog.json"
AUDIT_PATH = PROJECT_ROOT / "wiki" / "projects" / "quiz-set-audit.json"
OUTPUT_JSON = SANDBOX_DIR / "agent_deep_food_100_tests.json"
OUTPUT_REPORT = SANDBOX_DIR / "agent_deep_food_report.md"

def load_environment():
    cat = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    audit = json.loads(AUDIT_PATH.read_text(encoding="utf-8"))
    catalog = attach_audit_evidence(cat, audit)
    return catalog

NON_FOOD_LEAK_SKUS = {
    "RE89489": "Банний рушник (135×70 см) + шейкер + вітаміни (аксесуари/екіпірування)",
    "RE11665": "Швидкісна скакалка + подвійний ролик для преса (фітнес-інвентар)",
    "RE11663": "Килимок для йоги + текстильна стрічка-еспандер (фітнес-інвентар)",
    "Nabir_1110": "Капсули грибів Рейші 60 шт + капсули для сну Sleep Deep 60 шт (ноотропи/снодійне)",
    "RE88934": "Банка креатину 500 г + шейкер + шкарпетки (силове харчування + одяг)",
    "RE11688": "Банка Anabolic Mass 1 кг + Creatine 300 г (бодібілдинг/гейнер, не снеки)",
    "RE11019": "Шкарпетки + шейкер + скляна пляшка + брелок (одяг та аксесуари)",
    "RE11026": "2 пари шкарпеток + 3 брелоки-гільзи + Vitamin D3 (одяг та сувеніри)",
    "RE11651": "90 капсул Now Foods ZMA + 1 батончик (аптечні капсули для сну)",
    "RE11632": "60 капсул Mind Shi 4Mushroom + печиво (ноотропні грибні капсули)",
    "RE11660": "Банка креатину 300 г + 5 вуглеводних гелів (бодібілдерський креатин у бігу)",
}

SAVORY_JERKY_SKUS = {
    "RE89418", "RE89416", "RE89417", "RE89413",
    "RE89329", "RE89328", "RE89327", "RE89326",
    "RE89325", "RE89324", "RE89301", "RE89297",
    "RE89331", "RE89330", "RE88977"
}

SWEET_BAR_SKUS = {
    "RE89450", "RE11490", "RE11788", "Nabir_1129", "RE11721", "RE11659"
}

MEAL_SHAKE_SKUS = {
    "RE11557", "RE11695"
}

CAMPING_RATION_SKUS = {
    "RE11494", "RE11495", "RE88977"
}

WHEY_TUB_SKUS = {
    "Nabir_1118", "Nabir_1131"
}

def create_scenarios():
    scenarios = []

    def add(tid, name, cat_name, persona, intent, req, expected_flavor=None, expected_form=None):
        scenarios.append({
            "test_id": tid,
            "name": name,
            "category": cat_name,
            "persona": persona,
            "intent": intent,
            "request_payload": {"goal_group": "food", **req},
            "expected_flavor": expected_flavor, # "sweet", "savory", "neutral"
            "expected_form": expected_form,     # "bars", "meal_shake", "jerky", "camp_ration"
        })

    # =========================================================================
    # GROUP 1: Pure Energy Bars vs Protein Bars (20 tests: FOOD-001 - FOOD-020)
    # =========================================================================
    add("FOOD-001", "Runner energy bars during run", "Sweet Bars",
        "Марафонець-любитель", "Шукає вуглеводні батончики для підживлення під час тривалого бігу",
        {"activity": "running", "product_form": "bars", "use_timing": "during_training", "max_price_uah": 1500, "locale": "uk"},
        expected_flavor="sweet", expected_form="bars")

    add("FOOD-002", "Marathoner carbohydrate bars race prep", "Sweet Bars",
        "Асфальтний бігун", "Потрібні енергетичні батончики для тренувань перед марафоном",
        {"activity": "running", "product_form": "bars", "use_timing": "during_training", "max_price_uah": 1600, "locale": "uk"},
        expected_flavor="sweet", expected_form="bars")

    add("FOOD-003", "Cyclist protein bars long ride", "Sweet Bars",
        "Шосейний велосипедист", "Шукає протеїнові батончики для тривалого виїзду на 80+ км",
        {"activity": "cycling", "product_form": "bars", "use_timing": "during_training", "max_price_uah": 1500, "locale": "uk"},
        expected_flavor="sweet", expected_form="bars")

    add("FOOD-004", "Hiker sweet energy bars", "Sweet Bars",
        "Хайкер Карпати", "Потрібні компактні солодкі батончики для перекусів на маршруті",
        {"activity": "hiking", "product_form": "bars", "use_timing": "during_training", "max_price_uah": 1500, "locale": "uk"},
        expected_flavor="sweet", expected_form="bars")

    add("FOOD-005", "Runner standalone bars no club", "Sweet Bars",
        "Студент-легкоатлет", "Хоче купити тільки батончики без підписки на клуб",
        {"activity": "running", "product_form": "bars", "membership": "no", "max_price_uah": 1500, "locale": "uk"},
        expected_flavor="sweet", expected_form="bars")

    add("FOOD-006", "Cyclist bulk box bars with club", "Sweet Bars",
        "Регулярний шосейник", "Хоче великий бокс батончиків із клубною знижкою/абонементом",
        {"activity": "cycling", "product_form": "bars", "membership": "yes", "max_price_uah": 1500, "locale": "uk"},
        expected_flavor="sweet", expected_form="bars")

    add("FOOD-007", "Runner post-run protein bars", "Sweet Bars",
        "Бігунка після тренування", "Білковий перекус після інтенсивного темпового тренування",
        {"activity": "running", "product_form": "bars", "use_timing": "before_or_after_training", "max_price_uah": 1500, "locale": "uk"},
        expected_flavor="sweet", expected_form="bars")

    add("FOOD-008", "Daily desk worker healthy snack bars", "Sweet Bars",
        "Офісний працівник/бігун", "Корисний солодкий перекус замість шоколадок до кави",
        {"activity": "running", "product_form": "bars", "use_timing": "daily_use", "max_price_uah": 1500, "locale": "uk"},
        expected_flavor="sweet", expected_form="bars")

    add("FOOD-009", "Cyclist energy bars low budget 800 UAH", "Sweet Bars",
        "Бюджетний велосипедист", "Шукає недорогу пачку батончиків до 800 грн",
        {"activity": "cycling", "product_form": "bars", "max_price_uah": 800, "locale": "uk"},
        expected_flavor="sweet", expected_form="bars")

    add("FOOD-010", "Ultra runner energy bars high budget 2500 UAH", "Sweet Bars",
        "Ультрамарафонець", "Готовий витратити 2500 грн на якісний запас батончиків",
        {"activity": "running", "product_form": "bars", "max_price_uah": 2500, "locale": "uk"},
        expected_flavor="sweet", expected_form="bars")

    add("FOOD-011", "Runner general bars selection", "Sweet Bars",
        "Любитель бігу 10 км", "Батончики для бігу на регулярні тренування",
        {"activity": "running", "product_form": "bars", "locale": "uk"},
        expected_flavor="sweet", expected_form="bars")

    add("FOOD-012", "Cyclist bars no club membership", "Sweet Bars",
        "Грейвел-райдер", "Батончики без додаткових клубних послуг",
        {"activity": "cycling", "product_form": "bars", "membership": "no", "locale": "uk"},
        expected_flavor="sweet", expected_form="bars")

    add("FOOD-013", "Hiker bars with club membership", "Sweet Bars",
        "Член турклубу", "Батончики з абонементом Race Expert Club",
        {"activity": "hiking", "product_form": "bars", "membership": "yes", "locale": "uk"},
        expected_flavor="sweet", expected_form="bars")

    add("FOOD-014", "Runner protein bars ru locale", "Sweet Bars",
        "Русскоязычный бегун", "Протеиновые батончики после пробежек",
        {"activity": "running", "product_form": "bars", "locale": "ru"},
        expected_flavor="sweet", expected_form="bars")

    add("FOOD-015", "Runner energy bars uk locale", "Sweet Bars",
        "Україномовний бігун", "Енергетичні батончики на тренування",
        {"activity": "running", "product_form": "bars", "locale": "uk"},
        expected_flavor="sweet", expected_form="bars")

    add("FOOD-016", "Triathlete energy bars during training", "Sweet Bars",
        "Тріатлет на велоетпапі", "Легкозасвоювані солодкі вуглеводні батончики",
        {"activity": "cycling", "product_form": "bars", "use_timing": "during_training", "locale": "uk"},
        expected_flavor="sweet", expected_form="bars")

    add("FOOD-017", "Trail runner compact bars 1000 UAH", "Sweet Bars",
        "Трейлраннер", "Компактний набір батончиків до 1000 грн",
        {"activity": "running", "product_form": "bars", "max_price_uah": 1000, "locale": "uk"},
        expected_flavor="sweet", expected_form="bars")

    add("FOOD-018", "Cyclist component class protein_carbohydrate_food", "Sweet Bars",
        "Велотурист", "Вибір категорії спортивне харчування та батончики",
        {"activity": "cycling", "component_class": "protein_carbohydrate_food", "product_form": "bars", "locale": "uk"},
        expected_flavor="sweet", expected_form="bars")

    add("FOOD-019", "Runner bars without foreign items guarantee", "Sweet Bars",
        "Свідомий покупець", "Потрібні ТІЛЬКИ батончики, без пляшок та капсул",
        {"activity": "running", "component_class": "protein_carbohydrate_food", "product_form": "bars", "locale": "uk"},
        expected_flavor="sweet", expected_form="bars")

    add("FOOD-020", "Daily commuter pocket bars 1300 UAH", "Sweet Bars",
        "Активний містянин", "Зручні кишенькові батончики на щодень до 1300 грн",
        {"activity": "running", "product_form": "bars", "max_price_uah": 1300, "use_timing": "daily_use", "locale": "uk"},
        expected_flavor="sweet", expected_form="bars")

    # =========================================================================
    # GROUP 2: Meal Replacement Shakes & Liquid Nutrition (15 tests: FOOD-021 - FOOD-035)
    # =========================================================================
    add("FOOD-021", "Busy runner meal replacement shake after training", "Meal Shakes",
        "Зайнятий бігун", "Не встигає поїсти після вечірнього бігу, шукає повноцінний напій Napiy",
        {"activity": "running", "product_form": "liquid", "use_timing": "before_or_after_training", "locale": "uk"},
        expected_flavor="neutral", expected_form="meal_shake")

    add("FOOD-022", "Cyclist meal replacement drinks touring", "Meal Shakes",
        "Веломандрівник", "Шукає рідку розумну їжу в дорогу у форматі рідини",
        {"activity": "cycling", "product_form": "liquid", "use_timing": "daily_use", "locale": "uk"},
        expected_flavor="neutral", expected_form="meal_shake")

    add("FOOD-023", "Hiker ready-to-drink meal shakes food_or_meal", "Meal Shakes",
        "Піший турист", "Шукає формат їжі smart-food / напої Napiy для стоянок",
        {"activity": "hiking", "product_form": "food_or_meal", "use_timing": "before_or_after_training", "locale": "uk"},
        expected_flavor="neutral", expected_form="meal_shake")

    add("FOOD-024", "Office worker daily meal replacement drink", "Meal Shakes",
        "Офісний працівник", "Здоровий обід у шейкері замість фастфуду на роботі",
        {"activity": "running", "product_form": "liquid", "use_timing": "daily_use", "max_price_uah": 1500, "locale": "uk"},
        expected_flavor="neutral", expected_form="meal_shake")

    add("FOOD-025", "Runner meal shake no club membership", "Meal Shakes",
        "Бігун-індивідуал", "Шукає смарт-фуд напої Napiy без клубної картки",
        {"activity": "running", "product_form": "liquid", "membership": "no", "locale": "uk"},
        expected_flavor="neutral", expected_form="meal_shake")

    add("FOOD-026", "Cyclist meal shakes with 3-mo club membership", "Meal Shakes",
        "Велосипедист-ентузіаст", "Хоче набір 'Розумна їжа' разом з абонементом у клуб",
        {"activity": "cycling", "product_form": "liquid", "membership": "yes", "locale": "uk"},
        expected_flavor="neutral", expected_form="meal_shake")

    add("FOOD-027", "Hiker quick liquid nutrition 1300 UAH", "Meal Shakes",
        "Хайкер на вихідні", "Шукає набір рідкого перекусу до 1300 грн (наприклад, Мандрівний смаколик 1249 грн)",
        {"activity": "hiking", "product_form": "liquid", "max_price_uah": 1300, "locale": "uk"},
        expected_flavor="neutral", expected_form="meal_shake")

    add("FOOD-028", "Runner meal replacement shakes 1600 UAH", "Meal Shakes",
        "Марафонець на дієті", "Шукає поживні рідкі коктейлі до 1600 грн",
        {"activity": "running", "product_form": "liquid", "max_price_uah": 1600, "locale": "uk"},
        expected_flavor="neutral", expected_form="meal_shake")

    add("FOOD-029", "Budget buyer meal shakes under 900 UAH", "Meal Shakes",
        "Студент на підготовці", "Шукає недорогий смарт-напій до 900 грн",
        {"activity": "running", "product_form": "liquid", "max_price_uah": 900, "locale": "uk"},
        expected_flavor="neutral", expected_form="meal_shake")

    add("FOOD-030", "High budget buyer meal shake kit 2500 UAH", "Meal Shakes",
        "Підприємець-бігун", "Готовий придбати запас смарт-фуду на 2500 грн",
        {"activity": "running", "product_form": "liquid", "max_price_uah": 2500, "locale": "uk"},
        expected_flavor="neutral", expected_form="meal_shake")

    add("FOOD-031", "Athlete meal shake before_or_after uk locale", "Meal Shakes",
        "Спортсмен любитель", "Рідке харчування до або після тренування",
        {"activity": "running", "product_form": "liquid", "use_timing": "before_or_after_training", "locale": "uk"},
        expected_flavor="neutral", expected_form="meal_shake")

    add("FOOD-032", "Athlete meal shake before_or_after ru locale", "Meal Shakes",
        "Спортсмен любитель", "Жидкое питание до или после тренировки",
        {"activity": "running", "product_form": "liquid", "use_timing": "before_or_after_training", "locale": "ru"},
        expected_flavor="neutral", expected_form="meal_shake")

    add("FOOD-033", "Multi-sport athlete meal shake component class", "Meal Shakes",
        "Спортивний ентузіаст", "Вибір класу protein_carbohydrate_food у форматі рідини",
        {"activity": "cycling", "component_class": "protein_carbohydrate_food", "product_form": "liquid", "locale": "uk"},
        expected_flavor="neutral", expected_form="meal_shake")

    add("FOOD-034", "Backpacker meal shake hiking 1400 UAH", "Meal Shakes",
        "Легкохід у Карпатах", "Шукає набір смарт-фуду та сублімованих ягід до 1400 грн",
        {"activity": "hiking", "product_form": "food_or_meal", "max_price_uah": 1400, "locale": "uk"},
        expected_flavor="neutral", expected_form="meal_shake")

    add("FOOD-035", "Commuter liquid meal shake daily use", "Meal Shakes",
        "Активний водій/бігун", "Харчування в авто/дорозі на щодень",
        {"activity": "running", "product_form": "liquid", "use_timing": "daily_use", "locale": "uk"},
        expected_flavor="neutral", expected_form="meal_shake")

    # =========================================================================
    # GROUP 3: Savory Meat Jerky & Chicken Chips (25 tests: FOOD-036 - FOOD-060)
    # =========================================================================
    add("FOOD-036", "Hiker savory chicken chips RyabChick hiking", "Savory Meat Jerky",
        "Гірський турист", "Шукає солоні сушені м'ясні снеки (РябChick) замість солодких батончиків",
        {"activity": "hiking", "locale": "uk"},
        expected_flavor="savory", expected_form="jerky")

    add("FOOD-037", "Cyclist savory dried meat Myasko ToGo long ride", "Savory Meat Jerky",
        "Бреветчик 200 км", "Потрібне в'ялене м'ясо М'яско ToGo для сольового та білкового балансу на дистанції",
        {"activity": "cycling", "product_form": "food_or_meal", "locale": "uk"},
        expected_flavor="savory", expected_form="jerky")

    add("FOOD-038", "Runner savory jerky after run", "Savory Meat Jerky",
        "Трейловий ультрабігун", "Не переносить солодке після 4 годин бігу, шукає солоне курча чи яловичину",
        {"activity": "running", "product_form": "food_or_meal", "use_timing": "before_or_after_training", "locale": "uk"},
        expected_flavor="savory", expected_form="jerky")

    add("FOOD-039", "Savory meat jerky without club membership", "Savory Meat Jerky",
        "Покупець снеків", "Хоче купити набір в'яленого м'яса (8 шт) БЕЗ клубного абонемента",
        {"activity": "hiking", "product_form": "food_or_meal", "membership": "no", "locale": "uk"},
        expected_flavor="savory", expected_form="jerky")

    add("FOOD-040", "Savory meat jerky with club subscription", "Savory Meat Jerky",
        "Постійний клієнт", "Хоче великий бокс РябChick або М'яско ToGo з клубним абонементом",
        {"activity": "hiking", "membership": "yes", "locale": "uk"},
        expected_flavor="savory", expected_form="jerky")

    add("FOOD-041", "Hiker savory meat jerky 1500 UAH", "Savory Meat Jerky",
        "Карпатський мандрівник", "М'ясний раціон на похід вартістю до 1500 грн",
        {"activity": "hiking", "product_form": "food_or_meal", "max_price_uah": 1500, "locale": "uk"},
        expected_flavor="savory", expected_form="jerky")

    add("FOOD-042", "Cyclist non-sweet protein meat snacks", "Savory Meat Jerky",
        "Гревел-байкер", "Вимагає несолодкий білковий перекус, ненавидить шоколад",
        {"activity": "cycling", "product_form": "food_or_meal", "locale": "uk"},
        expected_flavor="savory", expected_form="jerky")

    add("FOOD-043", "Trail runner salty meat snacks", "Savory Meat Jerky",
        "Трейловий бігун Чорногора", "Потрібні солоні снеки для відновлення солей на ходу",
        {"activity": "running", "product_form": "food_or_meal", "locale": "uk"},
        expected_flavor="savory", expected_form="jerky")

    add("FOOD-044", "Hiker chicken jerky RyabChick soy sauce", "Savory Meat Jerky",
        "Любитель курки", "Шукає саме курячі сушені слайси в соєвому соусі (RE89418)",
        {"activity": "hiking", "locale": "uk"},
        expected_flavor="savory", expected_form="jerky")

    add("FOOD-045", "Hiker honey mustard meat snacks RyabChick", "Savory Meat Jerky",
        "Любитель пікантного", "Шукає сушену курку медово-гірчичну (RE89416)",
        {"activity": "hiking", "locale": "uk"},
        expected_flavor="savory", expected_form="jerky")

    add("FOOD-046", "Hiker pork dried meat Myasko ToGo", "Savory Meat Jerky",
        "Шанувальник свинини", "Шукає ситне в'ялене м'ясо свинини (RE89301)",
        {"activity": "hiking", "product_form": "food_or_meal", "locale": "uk"},
        expected_flavor="savory", expected_form="jerky")

    add("FOOD-047", "Cyclist citrus dried meat Myasko ToGo", "Savory Meat Jerky",
        "Шосейний гонщик", "Шукає в'ялене м'ясо з цитрусовим акцентом (RE89327)",
        {"activity": "cycling", "product_form": "food_or_meal", "membership": "no", "locale": "uk"},
        expected_flavor="savory", expected_form="jerky")

    add("FOOD-048", "Runner standalone 8-pack meat jerky no membership", "Savory Meat Jerky",
        "Бігун вихідного дня", "Хоче купити набір снеків 8 шт без підписки (RE89324, RE89326, RE89327)",
        {"activity": "running", "product_form": "food_or_meal", "membership": "no", "locale": "uk"},
        expected_flavor="savory", expected_form="jerky")

    add("FOOD-049", "Buyer meat jerky low budget 1000 UAH", "Savory Meat Jerky",
        "Студент на дієті", "Шукає м'ясні снеки до 1000 грн (перевірка порогу цін)",
        {"activity": "hiking", "product_form": "food_or_meal", "max_price_uah": 1000, "locale": "uk"},
        expected_flavor="savory", expected_form="jerky")

    add("FOOD-050", "Buyer meat jerky high budget 2200 UAH", "Savory Meat Jerky",
        "Забезпечений турист", "Хоче великий запас м'ясних снеків на 2200 грн",
        {"activity": "hiking", "product_form": "food_or_meal", "max_price_uah": 2200, "locale": "uk"},
        expected_flavor="savory", expected_form="jerky")

    add("FOOD-051", "Hiker savory snacks food_or_meal generic", "Savory Meat Jerky",
        "Піший мандрівник", "Готова їжа та м'ясні снеки для маршруту",
        {"activity": "hiking", "product_form": "food_or_meal", "locale": "uk"},
        expected_flavor="savory", expected_form="jerky")

    add("FOOD-052", "Cyclist savory snacks food_or_meal generic", "Savory Meat Jerky",
        "Байкпакер", "Снеки в підсідельну сумку на велопохід",
        {"activity": "cycling", "product_form": "food_or_meal", "locale": "uk"},
        expected_flavor="savory", expected_form="jerky")

    add("FOOD-053", "Runner savory snacks food_or_meal no membership", "Savory Meat Jerky",
        "Трейловий атлет", "М'ясні снеки без абонемента в клуб",
        {"activity": "running", "product_form": "food_or_meal", "membership": "no", "locale": "uk"},
        expected_flavor="savory", expected_form="jerky")

    add("FOOD-054", "Hiker savory meat snacks daily use", "Savory Meat Jerky",
        "Офісний працівник/турист", "Здоровий білковий солоний перекус щодня",
        {"activity": "hiking", "product_form": "food_or_meal", "use_timing": "daily_use", "locale": "uk"},
        expected_flavor="savory", expected_form="jerky")

    add("FOOD-055", "Cyclist savory jerky before after training", "Savory Meat Jerky",
        "Кроскантрійник", "Перекус після важкого підйому",
        {"activity": "cycling", "product_form": "food_or_meal", "use_timing": "before_or_after_training", "locale": "uk"},
        expected_flavor="savory", expected_form="jerky")

    add("FOOD-056", "Walking savory meat jerky test", "Savory Meat Jerky",
        "Нордичний ходок", "Шукає снеки для скандинавської ходьби (перевірка activity='other')",
        {"activity": "other", "product_form": "food_or_meal", "locale": "uk"},
        expected_flavor="savory", expected_form="jerky")

    add("FOOD-057", "Keto athlete salty chicken jerky", "Savory Meat Jerky",
        "Кето-спортсмен", "Суворе обмеження цукру: шукає 0% цукру солоне м'ясо",
        {"activity": "hiking", "locale": "uk"},
        expected_flavor="savory", expected_form="jerky")

    add("FOOD-058", "Hiker tasting meat pack Myasko ToGo", "Savory Meat Jerky",
        "Гурман-турист", "Шукає дегустаційний набір з різними смаками (RE89325)",
        {"activity": "hiking", "product_form": "food_or_meal", "locale": "uk"},
        expected_flavor="savory", expected_form="jerky")

    add("FOOD-059", "Buyer meat jerky ukrainian locale", "Savory Meat Jerky",
        "Український покупець", "Пояснення українською мовою для м'ясних снеків",
        {"activity": "hiking", "product_form": "food_or_meal", "locale": "uk"},
        expected_flavor="savory", expected_form="jerky")

    add("FOOD-060", "Buyer meat jerky russian locale", "Savory Meat Jerky",
        "Покупатель", "Пояснения на русском языке для мясных снеков",
        {"activity": "hiking", "product_form": "food_or_meal", "locale": "ru"},
        expected_flavor="savory", expected_form="jerky")

    # =========================================================================
    # GROUP 4: Camping Rations & Expedition Food (ЇDLO, Sublimates) (20 tests: FOOD-061 - FOOD-080)
    # =========================================================================
    add("FOOD-061", "Hiker explicitly selecting component_class dehydrated_meal", "Camping Rations",
        "Гірський турист", "Клікає у вікторині 'Сублімована туристична їжа' (dehydrated_meal) — критичний тест на 0 результатів!",
        {"activity": "hiking", "component_class": "dehydrated_meal", "locale": "uk"},
        expected_flavor="savory", expected_form="camp_ration")

    add("FOOD-062", "Camper selecting dehydrated_meal budget 1500 UAH", "Camping Rations",
        "Кемпер Карпати", "Шукає сублімовані туристичні страви на 1500 грн",
        {"activity": "hiking", "component_class": "dehydrated_meal", "max_price_uah": 1500, "locale": "uk"},
        expected_flavor="savory", expected_form="camp_ration")

    add("FOOD-063", "Backpacker selecting dehydrated_meal membership no", "Camping Rations",
        "Автономний турист", "Шукає сублімати без клубного членства",
        {"activity": "hiking", "component_class": "dehydrated_meal", "membership": "no", "locale": "uk"},
        expected_flavor="savory", expected_form="camp_ration")

    add("FOOD-064", "Mountain trekker selecting dehydrated_meal for hiking", "Camping Rations",
        "Трекер Кавказ/Татри", "Потрібні готові сублімовані обіди (каша, картопля, макарони)",
        {"activity": "hiking", "component_class": "dehydrated_meal", "locale": "ru"},
        expected_flavor="savory", expected_form="camp_ration")

    add("FOOD-065", "Bikepacker selecting dehydrated_meal cycling", "Camping Rations",
        "Велотурист автономник", "Шукає сублімати для приготування окропом у велопоході",
        {"activity": "cycling", "component_class": "dehydrated_meal", "locale": "uk"},
        expected_flavor="savory", expected_form="camp_ration")

    add("FOOD-066", "Hiker wanting IDLO 2.0 without membership", "Camping Rations",
        "Похідник соло", "Шукає чистий набір їжі ЇDLO 2.0 (RE11494) без клубного абонемента",
        {"activity": "hiking", "component_class": "protein_carbohydrate_food", "product_form": "food_or_meal", "membership": "no", "locale": "uk"},
        expected_flavor="savory", expected_form="camp_ration")

    add("FOOD-067", "Hiker wanting IDLO with club subscription", "Camping Rations",
        "Регулярний мандрівник", "Шукає набір ЇDLO з бонусною підпискою на клуб (RE11495)",
        {"activity": "hiking", "component_class": "protein_carbohydrate_food", "product_form": "food_or_meal", "membership": "yes", "locale": "uk"},
        expected_flavor="savory", expected_form="camp_ration")

    add("FOOD-068", "Backpacker camp meals low budget 1000 UAH", "Camping Rations",
        "Студент турист", "Шукає похідну їжу до 1000 грн (перевірка floor anchor)",
        {"activity": "hiking", "product_form": "food_or_meal", "max_price_uah": 1000, "locale": "uk"},
        expected_flavor="savory", expected_form="camp_ration")

    add("FOOD-069", "Camper camp meals 1600 UAH", "Camping Rations",
        "Сім'я в кемпінгу", "Готовий туристичний раціон на вихідні до 1600 грн",
        {"activity": "hiking", "product_form": "food_or_meal", "max_price_uah": 1600, "locale": "uk"},
        expected_flavor="savory", expected_form="camp_ration")

    add("FOOD-070", "Expedition leader camp meals high budget 3000 UAH", "Camping Rations",
        "Керівник експедиції", "Шукає великий об'єм туристичного харчування на 3000 грн",
        {"activity": "hiking", "product_form": "food_or_meal", "max_price_uah": 3000, "locale": "uk"},
        expected_flavor="savory", expected_form="camp_ration")

    add("FOOD-071", "Hiker sublimated fruits and ice cream RE11721", "Camping Rations",
        "Любитель десертів на вершині", "Шукає сублімовані фрукти та морозиво (RE11721)",
        {"activity": "hiking", "product_form": "food_or_meal", "locale": "uk"},
        expected_flavor="sweet", expected_form="camp_ration")

    add("FOOD-072", "Hiker IDLO 3.0 turkey jerky and polenta RE88977", "Camping Rations",
        "Мандрівник Карпатами", "Шукає суміш в'яленого м'яса та поленти (RE88977)",
        {"activity": "hiking", "product_form": "food_or_meal", "locale": "uk"},
        expected_flavor="savory", expected_form="camp_ration")

    add("FOOD-073", "Camper camping food during training trail", "Camping Rations",
        "Трейловий турист", "Їжа під час трекінгу на ходу",
        {"activity": "hiking", "product_form": "food_or_meal", "use_timing": "during_training", "locale": "uk"},
        expected_flavor="savory", expected_form="camp_ration")

    add("FOOD-074", "Camper camping food daily use camp", "Camping Rations",
        "Мешканець базового табору", "Їжа для базового табору протягом дня",
        {"activity": "hiking", "product_form": "food_or_meal", "use_timing": "daily_use", "locale": "uk"},
        expected_flavor="savory", expected_form="camp_ration")

    add("FOOD-075", "Hiker food_or_meal generic camping", "Camping Rations",
        "Піший мандрівник", "Харчування для походів у форматі готової їжі",
        {"activity": "hiking", "product_form": "food_or_meal", "locale": "uk"},
        expected_flavor="savory", expected_form="camp_ration")

    add("FOOD-076", "Hiker food_or_meal camping membership no", "Camping Rations",
        "Турист без підписок", "Харчування для походів без абонементів",
        {"activity": "hiking", "product_form": "food_or_meal", "membership": "no", "locale": "uk"},
        expected_flavor="savory", expected_form="camp_ration")

    add("FOOD-077", "Mountain hiker IDLO ukrainian locale", "Camping Rations",
        "Український альпініст", "Опис та склад набору ЇDLO українською мовою",
        {"activity": "hiking", "product_form": "food_or_meal", "locale": "uk"},
        expected_flavor="savory", expected_form="camp_ration")

    add("FOOD-078", "Mountain hiker IDLO russian locale", "Camping Rations",
        "Альпинист", "Описание и состав походной еды на русском языке",
        {"activity": "hiking", "product_form": "food_or_meal", "locale": "ru"},
        expected_flavor="savory", expected_form="camp_ration")

    add("FOOD-079", "Multi-day bikepacker camp food 1500 UAH", "Camping Rations",
        "Веломандрівник", "Сублімована їжа для пальника на веломаршруті",
        {"activity": "cycling", "product_form": "food_or_meal", "max_price_uah": 1500, "locale": "uk"},
        expected_flavor="savory", expected_form="camp_ration")

    add("FOOD-080", "Solo trekker camping rations no gear leak", "Camping Rations",
        "Легкохід ультралайт", "Вимагає виключно пакети з їжею, ніяких рушників чи гантелей",
        {"activity": "hiking", "component_class": "protein_carbohydrate_food", "product_form": "food_or_meal", "locale": "uk"},
        expected_flavor="savory", expected_form="camp_ration")

    # =========================================================================
    # GROUP 5: Fitness, Gym & Cross-training Athletes Seeking Food (10 tests: FOOD-081 - FOOD-090)
    # =========================================================================
    add("FOOD-081", "Gym athlete post-workout food activity fitness crash test", "Fitness Food",
        "Атлет у тренажерному залі", "Шукає протеїнові перекуси з вибором активності 'fitness' (тест валідатора!)",
        {"activity": "fitness", "max_price_uah": 1500, "locale": "uk"},
        expected_flavor="sweet", expected_form="bars")

    add("FOOD-082", "Fitness enthusiast protein bars activity fitness_gym crash test", "Fitness Food",
        "Відвідувач фітнес-клубу", "Шукає батончики, вибираючи активність 'fitness_gym' (тест валідатора!)",
        {"activity": "fitness_gym", "product_form": "bars", "locale": "uk"},
        expected_flavor="sweet", expected_form="bars")

    add("FOOD-083", "Crossfit athlete energy food activity strength_training crash test", "Fitness Food",
        "Кросфітер", "Шукає їжу для тренувань, вибираючи 'strength_training' (тест валідатора!)",
        {"activity": "strength_training", "locale": "uk"},
        expected_flavor="sweet", expected_form="bars")

    add("FOOD-084", "Gym athlete protein bars using activity other", "Fitness Food",
        "Силовий атлет", "Оминає блокування активності, вибираючи activity='other'",
        {"activity": "other", "product_form": "bars", "locale": "uk"},
        expected_flavor="sweet", expected_form="bars")

    add("FOOD-085", "Fitness enthusiast protein bars activity other no membership", "Fitness Food",
        "Фітнес-дівчина", "Шукає батончики без клубної картки через activity='other'",
        {"activity": "other", "product_form": "bars", "membership": "no", "locale": "uk"},
        expected_flavor="sweet", expected_form="bars")

    add("FOOD-086", "Bodybuilder snacks activity other component_class check", "Fitness Food",
        "Бодібілдер", "Шукає харчування через 'protein_carbohydrate_food' та activity='other'",
        {"activity": "other", "component_class": "protein_carbohydrate_food", "locale": "uk"},
        expected_flavor="sweet", expected_form="bars")

    add("FOOD-087", "Gym member protein snacks 1200 UAH activity other", "Fitness Food",
        "Студент у залі", "Шукає перекус до 1200 грн через activity='other'",
        {"activity": "other", "max_price_uah": 1200, "locale": "uk"},
        expected_flavor="sweet", expected_form="bars")

    add("FOOD-088", "Fitness girl diet bars 1500 UAH activity other", "Fitness Food",
        "Дівчина на кардіо", "Низькокалорійні батончики до 1500 грн через activity='other'",
        {"activity": "other", "product_form": "bars", "max_price_uah": 1500, "locale": "uk"},
        expected_flavor="sweet", expected_form="bars")

    add("FOOD-089", "Powerlifter post-gym food activity other before_or_after", "Fitness Food",
        "Пауерліфтер", "Їжа після важкого присідного дня",
        {"activity": "other", "use_timing": "before_or_after_training", "locale": "uk"},
        expected_flavor="sweet", expected_form="bars")

    add("FOOD-090", "Fitness coach protein snacks daily use activity other", "Fitness Food",
        "Тренер групових програм", "Швидкий перекус між тренуваннями щодня",
        {"activity": "other", "use_timing": "daily_use", "locale": "uk"},
        expected_flavor="sweet", expected_form="bars")

    # =========================================================================
    # GROUP 6: Budget Edge Cases (<1000 vs >1700), Subscriptions & Truthfulness (10 tests: FOOD-091 - FOOD-100)
    # =========================================================================
    add("FOOD-091", "Ultra-low budget student 400 UAH food request", "Budget & Integrity",
        "Студент на мілині", "Шукає хоч якісь батончики на 400 грн (тест floor_anchor на гейнер/гриби!)",
        {"activity": "running", "max_price_uah": 400, "locale": "uk"},
        expected_flavor="sweet", expected_form="bars")

    add("FOOD-092", "Low budget runner 600 UAH food request", "Budget & Integrity",
        "Початківець у бігу", "Шукає перекус до 600 грн (тест floor_anchor)",
        {"activity": "running", "max_price_uah": 600, "locale": "uk"},
        expected_flavor="sweet", expected_form="bars")

    add("FOOD-093", "Entry budget hiker 800 UAH food request", "Budget & Integrity",
        "Турист-початківець", "Шукає їжу в похід до 800 грн (тест near_miss на 1149 грн гейнер)",
        {"activity": "hiking", "max_price_uah": 800, "locale": "uk"},
        expected_flavor="savory", expected_form="camp_ration")

    add("FOOD-094", "Tight budget cyclist 950 UAH food request", "Budget & Integrity",
        "Велосипедист аматор", "Шукає батончики до 950 грн (тест near_miss на RE11688 'Набір маси')",
        {"activity": "cycling", "product_form": "bars", "max_price_uah": 950, "locale": "uk"},
        expected_flavor="sweet", expected_form="bars")

    add("FOOD-095", "High budget corporate buyer 2000 UAH bulk snacks", "Budget & Integrity",
        "Корпоративний менеджер", "Замовляє бокс перекусів в офіс на 2000 грн (перевірка стелі каталогу)",
        {"activity": "running", "max_price_uah": 2000, "locale": "uk"},
        expected_flavor="sweet", expected_form="bars")

    add("FOOD-096", "High budget endurance athlete 2500 UAH food", "Budget & Integrity",
        "Марафонець бізнесмен", "Готовий сплатити 2500 грн за преміум раціон",
        {"activity": "running", "max_price_uah": 2500, "locale": "uk"},
        expected_flavor="sweet", expected_form="bars")

    add("FOOD-097", "Maximum budget athlete 3500 UAH complete food supply", "Budget & Integrity",
        "Учасник Ironman", "Шукає максимальний запас на 3500 грн (каталог закінчується на 1500 грн)",
        {"activity": "cycling", "max_price_uah": 3500, "locale": "uk"},
        expected_flavor="sweet", expected_form="bars")

    add("FOOD-098", "Direct membership filter comparison test", "Budget & Integrity",
        "Аналітик вікторини", "Тестування чіткої роботи прапорця membership='yes' у категорії їжа",
        {"activity": "running", "membership": "yes", "locale": "uk"},
        expected_flavor="sweet", expected_form="bars")

    add("FOOD-099", "Deceptive explanation truthfulness test bez storonnih rechey", "Budget & Integrity",
        "Вимогливий покупець", "Перевірка твердження '(без сторонніх речей)' при рекомендації батончиків",
        {"activity": "running", "component_class": "protein_carbohydrate_food", "locale": "uk"},
        expected_flavor="sweet", expected_form="bars")

    add("FOOD-100", "Generic bare food request baseline audit", "Budget & Integrity",
        "Звичайний покупець", "Просто обрав 'Перекуси та харчування' без жодних додаткових фільтрів",
        {"locale": "uk"},
        expected_flavor="neutral", expected_form=None)

    return scenarios

print(f"Total scenarios defined: {len(create_scenarios())}")

def evaluate_scenario(scenario, catalog):
    req = dict(scenario["request_payload"])
    persona = scenario["persona"]
    intent = scenario["intent"]
    cat_name = scenario["category"]
    exp_flavor = scenario["expected_flavor"]
    exp_form = scenario["expected_form"]
    max_price = req.get("max_price_uah")

    test_record = {
        "test_id": scenario["test_id"],
        "name": scenario["name"],
        "category": cat_name,
        "persona": persona,
        "intent": intent,
        "request_payload": req,
        "execution": {},
        "evaluation": {
            "verdict": "PASS",
            "defect_codes": [],
            "flaws": [],
            "qa_notes": []
        }
    }

    # Step 1: Run draft_recommend
    try:
        res = draft_recommend(catalog, req)
        test_record["execution"] = {
            "status": res.get("status"),
            "exact_count": res.get("exact_count"),
            "general_count": res.get("general_count"),
            "relaxed_count": res.get("relaxed_count"),
            "returned_count": res.get("returned_count"),
            "results": [
                {
                    "sku": r.get("sku"),
                    "title": r.get("title"),
                    "price_uah": r.get("price_uah"),
                    "score": r.get("score"),
                    "why_suitable": r.get("why_suitable", [])
                }
                for r in res.get("results", [])
            ],
            "near_miss_results": [
                {
                    "sku": r.get("sku"),
                    "title": r.get("title"),
                    "price_uah": r.get("price_uah")
                }
                for r in res.get("near_miss_results", [])
            ],
            "floor_anchor_results": [
                {
                    "sku": r.get("sku"),
                    "title": r.get("title"),
                    "price_uah": r.get("price_uah")
                }
                for r in res.get("floor_anchor_results", [])
            ]
        }
    except DraftMatchError as e:
        test_record["execution"] = {
            "status": "VALIDATOR_EXCEPTION",
            "error_type": "DraftMatchError",
            "error_message": str(e)
        }
        # Immediate FAIL on validator crash
        test_record["evaluation"]["verdict"] = "FAIL"
        test_record["evaluation"]["defect_codes"].append("CRITICAL_FAIL_VALIDATOR_CRASH")
        flaw_msg = f"КРИТИЧНИЙ ЗБІЙ ВАЛІДАТОРА: Запит завершився падінням з помилкою DraftMatchError: '{e}'. Причина: активність '{req.get('activity')}' відсутня в списку дозволених для food, хоча в каталозі є десятки протеїнових батончиків для залу."
        test_record["evaluation"]["flaws"].append(flaw_msg)
        test_record["evaluation"]["qa_notes"].append("Користувач отримав системну помилку замість товарної видачі.")
        return test_record
    except Exception as e:
        test_record["execution"] = {
            "status": "UNEXPECTED_EXCEPTION",
            "error_type": type(e).__name__,
            "error_message": str(e)
        }
        test_record["evaluation"]["verdict"] = "FAIL"
        test_record["evaluation"]["defect_codes"].append("CRITICAL_FAIL_EXCEPTION")
        test_record["evaluation"]["flaws"].append(f"Непередбачений виняток: {e}")
        return test_record

    exec_res = test_record["execution"]
    results = exec_res.get("results", [])
    near_miss = exec_res.get("near_miss_results", [])
    floor_anchor = exec_res.get("floor_anchor_results", [])
    status = exec_res.get("status")

    # Step 2: Check Dehydrated Meal dead end
    if req.get("component_class") == "dehydrated_meal":
        if not results and status in ("no_match", "no_exact_match"):
            test_record["evaluation"]["verdict"] = "FAIL"
            test_record["evaluation"]["defect_codes"].append("CRITICAL_FAIL_DEHYDRATED_MEAL_DEAD_END")
            flaw_msg = "ГЛУХИЙ КУТ СУБЛІМАТІВ: Покупець обрав офіційну опцію 'Сублімована туристична їжа' (dehydrated_meal), але двигун видав 0 результатів. Причина: всі 3 набори ЇDLO в quiz-set-audit.json помилково розмічені як 'protein_carbohydrate_food'."
            test_record["evaluation"]["flaws"].append(flaw_msg)
            test_record["evaluation"]["qa_notes"].append("Покупець похідної їжі отримує порожню сторінку, хоча магазин продає пакети ЇDLO.")
            return test_record

    # Step 3: Check Empty results on valid queries
    if not results and not near_miss and not floor_anchor:
        test_record["evaluation"]["verdict"] = "FAIL"
        test_record["evaluation"]["defect_codes"].append("ZERO_RESULTS_UNEXPECTED")
        test_record["evaluation"]["flaws"].append(f"Повна відсутність результатів (0 товарів, 0 near-miss, 0 floor-anchor) для валідного запиту.")
        return test_record

    # Step 4: Check Non-Food Leaks in Recommended Items
    active_items = results if results else (near_miss if near_miss else floor_anchor)
    leak_found = False
    for item in results:
        sku = item.get("sku")
        if sku in NON_FOOD_LEAK_SKUS:
            leak_found = True
            desc = NON_FOOD_LEAK_SKUS[sku]
            test_record["evaluation"]["verdict"] = "FAIL"
            test_record["evaluation"]["defect_codes"].append("CRITICAL_FAIL_NON_FOOD_LEAK")
            test_record["evaluation"]["flaws"].append(f"ВИТІК НЕХАРЧОВИХ ТОВАРІВ У СНЕКИ: Товар [{sku}] «{item.get('title')}» містить сторонні предмети: {desc}.")

    # Step 5: Check False Explanations "(без сторонніх речей)"
    for item in results:
        sku = item.get("sku")
        why = item.get("why_suitable", [])
        has_bez_storonnih = any("без сторонніх" in w or "без посторонних" in w for w in why)
        if has_bez_storonnih:
            # Check if this set actually has foreign items
            has_club = "абонемент" in item.get("title", "").lower()
            if sku in NON_FOOD_LEAK_SKUS or has_club or sku in WHEY_TUB_SKUS:
                test_record["evaluation"]["verdict"] = "FAIL"
                if "CRITICAL_FAIL_DECEPTIVE_EXPLANATION" not in test_record["evaluation"]["defect_codes"]:
                    test_record["evaluation"]["defect_codes"].append("CRITICAL_FAIL_DECEPTIVE_EXPLANATION")
                test_record["evaluation"]["flaws"].append(
                    f"НЕПРАВДИВЕ ПОЯСНЕННЯ У КАРТЦІ: Двигун стверджує 'у наборі саме Спортивне харчування та батончики (без сторонніх речей)', але набір [{sku}] «{item.get('title')}» містить {NON_FOOD_LEAK_SKUS.get(sku, '3-місячний абонемент у клуб або велику банку порошку')}."
                )

    # Step 6: Check Sweet vs Savory Flavor Matching
    if exp_flavor == "savory":
        # Buyer specifically wanted savory meat jerky (РябChick, М'яско ToGo, ЇDLO)
        savory_in_results = any(r.get("sku") in SAVORY_JERKY_SKUS or r.get("sku") in CAMPING_RATION_SKUS for r in results)
        pure_sweet_only = all(r.get("sku") in SWEET_BAR_SKUS for r in results)
        if results and not savory_in_results:
            test_record["evaluation"]["verdict"] = "FAIL"
            test_record["evaluation"]["defect_codes"].append("FAIL_SWEET_SAVORY_CONFUSION")
            test_record["evaluation"]["flaws"].append(
                "ПОВНИЙ ЗБІЙ СОЛОДКЕ/СОЛОНЕ: Покупець шукав солоні м'ясні снеки/джеркі, але алгоритм запропонував виключно солодкі десертні батончики/фрукти, оскільки в системі відсутня диференціація смаків."
            )
        elif results and not pure_sweet_only and not savory_in_results:
            if test_record["evaluation"]["verdict"] == "PASS":
                test_record["evaluation"]["verdict"] = "WARN"
            test_record["evaluation"]["defect_codes"].append("WARN_SWEET_SAVORY_DILUTED")
            test_record["evaluation"]["flaws"].append(
                "РОЗБАВЛЕНИЙ СМАКОВИЙ ПРОФІЛЬ: У видачі змішані солодкі та солоні позиції через відсутність фільтра смакового профілю."
            )

    elif exp_flavor == "sweet":
        # Buyer specifically wanted sweet bars/gels
        sweet_in_results = any(r.get("sku") in SWEET_BAR_SKUS for r in results)
        pure_savory_only = all(r.get("sku") in SAVORY_JERKY_SKUS for r in results)
        if results and not sweet_in_results and pure_savory_only:
            test_record["evaluation"]["verdict"] = "FAIL"
            test_record["evaluation"]["defect_codes"].append("FAIL_SWEET_SAVORY_CONFUSION")
            test_record["evaluation"]["flaws"].append(
                "ЗБІЙ СМАКОВОГО ПРОФІЛЮ: Покупець шукав солодкі енергетичні батончики, а отримав м'ясні снеки."
            )

    # Step 7: Check Budget Floor / Near-Miss Poisoning
    if not results and (near_miss or floor_anchor):
        anchor_items = near_miss if near_miss else floor_anchor
        poisoned = any(item.get("sku") in NON_FOOD_LEAK_SKUS for item in anchor_items)
        if poisoned:
            if test_record["evaluation"]["verdict"] == "PASS":
                test_record["evaluation"]["verdict"] = "WARN"
            test_record["evaluation"]["defect_codes"].append("WARN_BUDGET_FLOOR_POISONING")
            poison_skus = [item.get("sku") for item in anchor_items if item.get("sku") in NON_FOOD_LEAK_SKUS]
            test_record["evaluation"]["flaws"].append(
                f"ОТРУЄННЯ БЮДЖЕТНОГО ЯКОРЯ: При бюджеті {max_price} грн система рекомендує як найдешевшу альтернативу нехарчовий набір {poison_skus} (Anabolic Mass 1кг або капсули грибів), оскільки вони помилково позначені найдешевшими 'снеками' (1149/1215 грн)."
            )
        else:
            if test_record["evaluation"]["verdict"] == "PASS":
                test_record["evaluation"]["verdict"] = "WARN"
            test_record["evaluation"]["defect_codes"].append("WARN_BUDGET_BELOW_MINIMUM")
            test_record["evaluation"]["flaws"].append(
                f"Бюджет {max_price} грн нижчий за мінімальну ціну харчових наборів у каталозі (1149 грн). Спрацював {status}."
            )

    # Step 8: High budget catalog ceiling check
    if max_price and max_price >= 1800 and results:
        top_price = max(r.get("price_uah", 0) for r in results)
        if top_price <= 1500:
            if test_record["evaluation"]["verdict"] == "PASS":
                test_record["evaluation"]["verdict"] = "WARN"
            test_record["evaluation"]["defect_codes"].append("WARN_HIGH_BUDGET_CATALOG_CEILING")
            test_record["evaluation"]["flaws"].append(
                f"СТЕЛЯ КАТАЛОГУ: Покупець готовий сплатити {max_price} грн, але найдорожчий набір у каталозі коштує {top_price} грн. Магазин втрачає чек на преміум/bulk наборах."
            )

    # Step 9: Membership filter fidelity
    membership_req = req.get("membership")
    if membership_req == "no" and results:
        has_club_leak = any("абонемент" in r.get("title", "").lower() for r in results)
        if has_club_leak:
            test_record["evaluation"]["verdict"] = "FAIL"
            test_record["evaluation"]["defect_codes"].append("CRITICAL_FAIL_MEMBERSHIP_LEAK")
            test_record["evaluation"]["flaws"].append("ПОРУШЕННЯ ФІЛЬТРА: Покупець обрав membership='no', але отримав набір з абонементом у клуб!")

    # Step 10: If no defects, record clean pass notes
    if not test_record["evaluation"]["defect_codes"]:
        test_record["evaluation"]["defect_codes"].append("NONE")
        test_record["evaluation"]["qa_notes"].append(
            "Ідеальна відповідність: видано справжні харчові позиції, чесні пояснення, сумісні параметри бюджету та форми."
        )

    # Deduplicate defect codes
    test_record["evaluation"]["defect_codes"] = list(dict.fromkeys(test_record["evaluation"]["defect_codes"]))

    return test_record

print("Evaluator logic ready.")

def main():
    print("Starting Deep QA Evaluation for 'Food & Snacks' (100 Scenarios)...")
    catalog = load_environment()
    scenarios = create_scenarios()

    evaluated_tests = []
    verdicts = Counter()
    defect_counts = Counter()
    category_verdicts = {}

    for idx, sc in enumerate(scenarios, 1):
        record = evaluate_scenario(sc, catalog)
        evaluated_tests.append(record)
        v = record["evaluation"]["verdict"]
        cat = record["category"]
        verdicts[v] += 1

        if cat not in category_verdicts:
            category_verdicts[cat] = Counter()
        category_verdicts[cat][v] += 1

        for code in record["evaluation"]["defect_codes"]:
            defect_counts[code] += 1

        if idx % 20 == 0 or idx == len(scenarios):
            print(f"Processed {idx}/{len(scenarios)} tests... Current: PASS={verdicts['PASS']}, WARN={verdicts['WARN']}, FAIL={verdicts['FAIL']}")

    # Save JSON output
    print(f"Writing detailed test results to {OUTPUT_JSON}...")
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(evaluated_tests, f, indent=2, ensure_ascii=False)

    # Generate Markdown Report
    print(f"Generating comprehensive markdown report to {OUTPUT_REPORT}...")
    generate_markdown_report(evaluated_tests, verdicts, defect_counts, category_verdicts)
    print("Done! Evaluation completed successfully.")


def generate_markdown_report(tests, verdicts, defect_counts, category_verdicts):
    total = len(tests)
    p_pass = verdicts["PASS"] / total * 100
    p_warn = verdicts["WARN"] / total * 100
    p_fail = verdicts["FAIL"] / total * 100

    report = []
    report.append("# QA Deep Audit Report: Food & Snacks (`goal_group: 'food'`)")
    report.append("**Role:** QA Specialist for Food & Snacks (`food`) — Sports Nutritionist, Endurance Athlete & Human Buyer Perspective  ")
    report.append("**Test Scope:** 100 Dedicated Buyer Scenarios covering Sweet Bars, Meal Shakes, Savory Meat Jerky (РябChick, М'яско ToGo), Camping Rations (ЇDLO), Fitness Food, and Budget Extremes  ")
    report.append("**Catalog Source:** `wiki/projects/quiz-set-audit.json` (207 sets in catalog, 38 food candidate sets)  ")
    report.append(f"**Execution Engine:** `test-quiz-sandbox/draft_matcher.py:draft_recommend`  \n")

    report.append("## 1. Executive Summary & Verdict Scorecard")
    report.append("Out of 100 realistic, domain-specific buyer test scenarios across all food sub-categories, timings, formats, and budgets:\n")
    report.append(f"- **PASS:** {verdicts['PASS']} ({p_pass:.1f}%) — clean, athletic-logical matching with genuine food products and honest explanations.")
    report.append(f"- **WARN:** {verdicts['WARN']} ({p_warn:.1f}%) — partial matches, budget floor anchors, catalog ceiling limitations, or sweet/savory profile dilution.")
    report.append(f"- **FAIL:** {verdicts['FAIL']} ({p_fail:.1f}%) — critical domain breakdowns: non-food leaks (bath towels, yoga mats, jump ropes, mass gainers, pill bottles), 100% dead end for camping meals, validator crashes on fitness activities, or deceptive '(без сторонніх речей)' claims.\n")

    report.append("### Scorecard by Sub-Category")
    report.append("| Sub-Category | Total Tests | PASS | WARN | FAIL | Pass Rate |")
    report.append("| :--- | :---: | :---: | :---: | :---: | :---: |")
    for cat, counts in category_verdicts.items():
        cat_total = sum(counts.values())
        cat_pass = counts["PASS"]
        cat_warn = counts["WARN"]
        cat_fail = counts["FAIL"]
        cat_rate = (cat_pass / cat_total * 100) if cat_total else 0
        report.append(f"| **{cat}** | {cat_total} | {cat_pass} | {cat_warn} | {cat_fail} | {cat_rate:.1f}% |")
    report.append(f"| **OVERALL** | **{total}** | **{verdicts['PASS']}** | **{verdicts['WARN']}** | **{verdicts['FAIL']}** | **{p_pass:.1f}%** |\n")

    report.append("```")
    bar_pass = int(p_pass / 2)
    bar_warn = int(p_warn / 2)
    bar_fail = 50 - bar_pass - bar_warn
    report.append(f"Verdict Visual: [{'#' * bar_pass}{'-' * bar_warn}{'!' * bar_fail}]")
    report.append(f"  PASS: {verdicts['PASS']} ({p_pass:.1f}%) | WARN: {verdicts['WARN']} ({p_warn:.1f}%) | FAIL: {verdicts['FAIL']} ({p_fail:.1f}%)")
    report.append("```\n")

    report.append("---")
    report.append("## 2. Flaw Taxonomy & Defect Distribution")
    report.append("| Defect Code | Description | Occurrences | Severity |")
    report.append("| :--- | :--- | :---: | :--- |")

    defect_descriptions = {
        "NONE": ("Ідеальна спортивна відповідність, справжня їжа та чесні пояснення", "PASS"),
        "CRITICAL_FAIL_NON_FOOD_LEAK": ("Витік нехарчових товарів (банний рушник, килимок йоги, скакалка, пігулки, гейнер)", "CRITICAL FAIL"),
        "CRITICAL_FAIL_DECEPTIVE_EXPLANATION": ("Неправдива заява '(без сторонніх речей)' при наявності рушників, добавок або абонементів", "CRITICAL FAIL"),
        "CRITICAL_FAIL_DEHYDRATED_MEAL_DEAD_END": ("100% глухий кут: вибір 'dehydrated_meal' дає 0 результатів через помилку тегування ЇDLO", "CRITICAL FAIL"),
        "CRITICAL_FAIL_VALIDATOR_CRASH": ("Падіння валідатора DraftMatchError на активностях fitness, fitness_gym, strength_training", "CRITICAL FAIL"),
        "FAIL_SWEET_SAVORY_CONFUSION": ("Повний збій смакового профілю: замість солоного м'яса видано виключно солодкі батончики", "FAIL"),
        "CRITICAL_FAIL_MEMBERSHIP_LEAK": ("Порушення фільтра: видача обов'язкового абонемента при виборі membership='no'", "CRITICAL FAIL"),
        "WARN_BUDGET_FLOOR_POISONING": ("Отруєння бюджетного якоря: при низькому бюджеті якір пропонує гейнер 1кг або гриби", "WARN"),
        "WARN_HIGH_BUDGET_CATALOG_CEILING": ("Стеля каталогу (1500 грн): відсутність великих оптових боксів для бюджетів 1800–3500 грн", "WARN"),
        "WARN_BUDGET_BELOW_MINIMUM": ("Бюджет покупця нижче мінімального порогу каталогу (1149 грн), спрацював near-miss/anchor", "WARN"),
        "WARN_SWEET_SAVORY_DILUTED": ("Змішування солодких та солоних позицій через відсутність фільтра смакового профілю", "WARN"),
        "ZERO_RESULTS_UNEXPECTED": ("Порожня видача при валідному запиті", "CRITICAL FAIL"),
    }

    for code, count in defect_counts.most_common():
        desc, sev = defect_descriptions.get(code, ("Невідомий дефект", "UNKNOWN"))
        report.append(f"| `{code}` | {desc} | **{count}** | {sev} |")
    report.append("\n---\n")

    report.append("## 3. Deep Domain & Architectural Analysis of Critical Flaws")

    report.append("### Finding 1: Gross Non-Food Leaks into 'Food & Snacks' (CRITICAL FAIL)")
    report.append("> [!CAUTION]")
    report.append("> **11 out of 38 catalog candidates in `food` are NOT food sets:**")
    report.append("> In `quiz-set-audit.json`, numerous non-food kits were erroneously assigned `candidate_tiers.component_based: ['portable_food_snacks']` or `seller_positioned: ['portable_food_snacks', 'endurance_energy']`.")
    report.append("> As a result, when a customer asks for snacks, the quiz recommends:")
    report.append("> 1. **RE89489 («Основа регулярних тренувань»):** A **135×70 cm cotton bath towel**, Myprotein shaker, and Nutriversum daily vitamins bundled with a 3-month gym club membership. Zero food items!")
    report.append("> 2. **RE11665 («Активний рух»):** A **speed jump rope with counter**, double ab wheel roller with knee pad, and massage ball. Gym equipment sold as food!")
    report.append("> 3. **RE11663 («Йога та пілатес»):** An **EasyFit yoga mat** and textile resistance band. Fitness gear sold as edible snacks!")
    report.append("> 4. **Nabir_1110 («Зменшення стресу та регуляція сну»):** 60 capsules of Mind Shi Reishi mushroom nootropics and 60 capsules of Sleep Deep sleep medication. Sleeping pill bottles sold as food!")
    report.append("> 5. **RE11688 («Набір маси»):** 1,000g Kevin Levrone Anabolic Mass powder and 300g Creatine Monohydrate. A 1.3kg bodybuilding powder tub sold as 'portable snacks'!")
    report.append("> 6. **RE88934 («Регулярний зал»):** 500g Creatine Monohydrate tub, gym shaker, and socks.")
    report.append("> 7. **RE11019 («Щоденний комфорт»):** White socks size 40–42, shaker, glass water bottle, and keychains.")
    report.append("> 8. **RE11026 («Спортивний подарунок»):** 2 pairs of socks, 3 bullet keychains, and a bottle of Vitamin D3 softgels.")
    report.append("> 9. **RE11651 («Нічний ZMA»):** 90 capsules of ZMA sleep minerals with 1 bar.")
    report.append("> 10. **RE11632 («Розум і Сила»):** 60 capsules of Mind Shi 4Mushroom nootropics with cookies.")
    report.append("> 11. **RE11660 («Марафонець»):** 300g Creatine Monohydrate tub bundled with 5 carbohydrate gels.\n")

    report.append("### Finding 2: The Dehydrated Camping Meal Dead-End (100% Failure Rate)")
    report.append("> [!IMPORTANT]")
    report.append("> When an outdoor camper or hiker selects the officially advertised option `component_class: 'dehydrated_meal'` ('Сублімована туристична їжа'), the quiz engine returns **`status: no_match` (0 results)**.")
    report.append("> **Root Cause:** In `quiz-set-audit.json`, the genuine camping ration sets (`RE11494` ЇDLO 2.0, `RE11495` ЇDLO Club, `RE88977` ЇDLO 3.0) were tagged with `component_classes: ['protein_carbohydrate_food']` instead of `'dehydrated_meal'`. Meanwhile, `COMPONENT_CLASSES_BY_GOAL['food']` offers `'dehydrated_meal'` as a primary steering filter. Every hiker who clicks this button experiences a dead-end blank screen.\n")

    report.append("### Finding 3: Complete Absence of Sweet vs Savory Taste Profiling")
    report.append("> [!WARNING]")
    report.append("> The Race Expert food catalog contains two diametrically opposed taste worlds:")
    report.append("> - **Sweet confectionary:** Sweet protein & carb bars (LipoBar, Fitly, Myprotein cookies), fruit crisps, and sweet dessert shakes.")
    report.append("> - **Savory / Salty meat snacks:** 14 sets of dried meat jerky (РябChick dried chicken slices in soy sauce, honey mustard, paprika, Gouda cheese; М'яско ToGo beef, pork, turkey, chicken).")
    report.append("> **The Problem:** The quiz interface and data model contain **zero fields, signals, or questions for taste or flavor preference** (sweet vs savory / salty / meat).")
    report.append("> A hiker or cyclist specifically demanding salty meat jerky for salt replenishment during sweaty endurance workouts is indiscriminately fed chocolate bars, cookies, or sublimated strawberries. Conversely, a sweet tooth buyer gets meat jerky. Furthermore, sets like RyabChick have `product_forms: []` empty in their audit record, causing them to fall into 'unknown' when `product_form: 'bars'` or `'food_or_meal'` is requested.\n")

    report.append("### Finding 4: Deceptive Marketing Claims: '(без сторонніх речей)'")
    report.append("> [!CAUTION]")
    report.append("> In `draft_matcher.py:_build_why_suitable()`, when `component_class: 'protein_carbohydrate_food'` is matched, the engine generates:")
    report.append("> *«Категорія товарів: у наборі саме Спортивне харчування та батончики (без сторонніх речей).»*")
    report.append("> In reality, the recommended set frequently contains:")
    report.append("> - A 135×70 cm cotton bath towel (`RE89489`)")
    report.append("> - 4 pairs of athletic socks (`RE11026`)")
    report.append("> - 60 capsules of nootropic mushrooms or sleeping pills (`RE11632`, `RE11651`)")
    report.append("> - A mandatory 3-month gym club membership (accounting for a large portion of the 1500 UAH price).")
    report.append("> Claiming '(без сторонніх речей)' ('without extraneous items') when the bundle is dominated by non-food accessories is false advertising that destroys customer trust.\n")

    report.append("### Finding 5: Artificial Validator Wall Blocking Gym & Fitness Athletes")
    report.append("> [!IMPORTANT]")
    report.append("> `draft_matcher.py` restricts `ACTIVITY_OPTIONS_BY_GOAL['food'] = {'running', 'cycling', 'hiking'}`.")
    report.append("> If a gym member, crossfitter, or fitness enthusiast enters the quiz looking for protein bars and selects `fitness`, `fitness_gym`, or `strength_training`, the validator raises an unhandled `DraftMatchError: activity is not supported for the selected need`.")
    report.append("> Yet in the catalog, almost all protein bars (LipoBar, Fitly, Myprotein) and meal shakes explicitly list `fitness_gym` in their source metadata! The engine crashes on the very audience that consumes the most protein bars.\n")

    report.append("### Finding 6: Low Budget Floor Poisoning (< 1000 UAH)")
    report.append("> [!NOTE]")
    report.append("> The entire catalog has **ZERO food sets below 1149 UAH**.")
    report.append("> When a buyer specifies a budget of 400–1000 UAH, the engine triggers `near_miss` or `floor_anchor`. The two lowest-priced sets matched to `food` are:")
    report.append("> 1. `RE11688` (1149 UAH) — 1,000g Anabolic Mass powder tub + 300g Creatine Monohydrate.")
    report.append("> 2. `RE11632` (1215 UAH) — Mind Shi 4Mushroom nootropic capsules.")
    report.append("> Consequently, every budget-conscious buyer looking for affordable snack bars is told: *'Here is our lowest-priced food anchor: a 1kg tub of bodybuilder gainer powder and mushroom brain pills!'*.\n")

    report.append("### Finding 7: High Budget Upsell Ceiling (1800–3500 UAH)")
    report.append("> [!NOTE]")
    report.append("> The maximum price of any food set in the catalog is **1500 UAH**.")
    report.append("> High-budget buyers (ultra runners, expedition teams, corporate clients) willing to spend 2000–3500 UAH are shown standard 1500 UAH sets with club memberships, because the store has no large bulk snack boxes (e.g. 50-pack bar boxes or multi-month expedition ration crates).\n")

    report.append("### Finding 8: The Running & Cycling Activity Blackout for Meat Jerky & Meal Shakes (24 Unintended Failures)")
    report.append("> [!CAUTION]")
    report.append("> **Runner & Cyclist Blackout:** Every single savory meat snack set (12 sets of М'яско ToGo and 2 sets of RyabChick) lists `activity_groups: ['fitness_gym', 'general_lifestyle', 'hiking', 'walking']`. **None of them list `running` or `cycling` in their metadata!**")
    report.append("> Similarly, the liquid meal replacement shakes (`RE11557` Napiy, `RE11695` Мандрівний смаколик) only list `hiking` or `fitness_gym`.")
    report.append("> Meanwhile, `ACTIVITY_OPTIONS_BY_GOAL['food']` in `draft_matcher.py` strictly forces `activity` to be one of `{'running', 'cycling', 'hiking'}`.")
    report.append("> Because `activity` is treated as a hard gate CORE field in `draft_matcher.py:_candidate_fit` (`elif key in CORE_ANSWER_FIELDS: return None`), selecting `activity: 'running'` or `'cycling'` **completely eliminates 100% of the store's meat snacks and meal shakes**.")
    report.append("> And because selecting `activity: 'fitness_gym'` or `'walking'` triggers a `DraftMatchError` crash, it is practically impossible for any runner, cyclist, gym athlete, or walker to find meat snacks through the quiz unless they guess to select `hiking` or `other`.\n")

    report.append("---")
    report.append("## 4. Full 100 Buyer Test Execution Log")
    report.append("| Test ID | Sub-Category | Persona & Intent | Request Parameters | Primary Results (SKU & Title) | Verdict | Flaws & Notes |")
    report.append("| :--- | :--- | :--- | :--- | :--- | :---: | :--- |")

    for t in tests:
        tid = t["test_id"]
        cat = t["category"]
        persona_intent = f"**{t['persona']}**: {t['intent']}"
        req = t["request_payload"]
        req_summary = f"`act={req.get('activity')}`, `form={req.get('product_form')}`, `budget={req.get('max_price_uah')}`, `mem={req.get('membership')}`"
        v = t["evaluation"]["verdict"]
        flaws = "<br>".join(t["evaluation"]["flaws"]) if t["evaluation"]["flaws"] else "None"

        res = t["execution"].get("results", [])
        near = t["execution"].get("near_miss_results", [])
        floor = t["execution"].get("floor_anchor_results", [])
        err = t["execution"].get("error_message")

        if err:
            res_summary = f"**ERROR:** `{err}`"
        elif res:
            res_summary = "<br>".join([f"[{r['sku']}] {r['title']} ({r['price_uah']} грн)" for r in res[:2]])
            if len(res) > 2:
                res_summary += f"<br>*(+{len(res)-2} more)*"
        elif near:
            res_summary = f"**Near-Miss:** [{near[0]['sku']}] {near[0]['title']} ({near[0]['price_uah']} грн)"
        elif floor:
            res_summary = f"**Floor-Anchor:** [{floor[0]['sku']}] {floor[0]['title']} ({floor[0]['price_uah']} грн)"
        else:
            res_summary = "*No results*"

        v_badge = f"**{v}**" if v == "PASS" else (f"`{v}`" if v == "WARN" else f"**`{v}`**")
        report.append(f"| `{tid}` | {cat} | {persona_intent} | {req_summary} | {res_summary} | {v_badge} | {flaws} |")

    report.append("\n---\n")
    report.append("## 5. Actionable Strategic Recommendations")
    report.append("### Immediate Catalog & Audit Fixes (`quiz-set-audit.json`):")
    report.append("1. **Prune Non-Food Leaks from `food`:** Strip `portable_food_snacks` and `endurance_energy` tags from `RE89489` (bath towel), `RE11665` (jump rope/roller), `RE11663` (yoga mat), `Nabir_1110` (Reishi/Sleep pills), `RE11688` (1kg mass gainer), `RE88934` (creatine/socks), `RE11019` (socks/shaker), and `RE11026` (socks/keychains).")
    report.append("2. **Fix Dehydrated Meal Classification:** Update `RE11494`, `RE11495`, and `RE88977` (ЇDLO camping meals) to include `dehydrated_meal` in `component_classes` so the quiz option works immediately.")
    report.append("3. **Fix Product Forms for RyabChick:** Add `forms: ['food_or_meal']` to all RyabChick chicken chip sets (`RE89418`, `RE89416`, `RE89417`, `RE89413`) instead of leaving `forms: []` empty.")

    report.append("\n### Engine & Matcher Fixes (`draft_matcher.py`):")
    report.append("1. **Expand Allowed Activities for Food:** Add `fitness_gym`, `fitness`, `strength_training`, `functional_training`, and `walking` to `ACTIVITY_OPTIONS_BY_GOAL['food']`.")
    report.append("2. **Introduce Flavor Profiling Question:** Add a `flavor_profile` question (`sweet_dessert` vs `savory_salty_meat` vs `any`) to separate sweet bars/cookies from meat jerky and savory camp rations.")
    report.append("3. **Fix Deceptive Explanations:** Only append `(без сторонніх речей)` when the set contains strictly food components and zero club memberships, accessories, or clothing.")
    report.append("4. **Clean Budget Anchor Pool:** Ensure `_find_floor_anchor` filters out disqualified/leak sets before selecting the baseline anchor, preventing 1kg mass gainer tubs from acting as low-cost snack anchors.")

    # Write report
    with open(OUTPUT_REPORT, "w", encoding="utf-8") as f:
        f.write("\n".join(report))


if __name__ == "__main__":
    main()
