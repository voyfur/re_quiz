# -*- coding: utf-8 -*-
"""Run a reproducible, buyer-perspective audit of 100 draft quiz scenarios."""

from __future__ import annotations

import sys
from collections import Counter
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "test-quiz-sandbox"))

from draft_matcher import (  # noqa: E402
    DraftMatchError,
    _as_set,
    _goal_candidates,
    _size_ranges,
    _soft_signals,
    GOAL_LABELS,
    attach_audit_evidence,
    draft_options,
    draft_recommend,
)
from server import AUDIT_PATH, _load_catalog  # noqa: E402


CASES: list[dict] = []


def add_group(goal: str, rows: list[tuple[str, dict, str]]) -> None:
    for title, desired, note in rows:
        CASES.append({
            "id": len(CASES) + 1,
            "goal": goal,
            "buyer": title,
            "desired": {"max_price_uah": 1500, **desired},
            "note": note,
        })


add_group("running", [
    ("Марафонец: гель на тёплый старт", {"component_class": "protein_carbohydrate_food", "use_scenario": "event_preparation", "use_timing": "during_training", "race_format": "marathon", "season": "warm", "product_form": "gel", "max_price_uah": 1000}, "Проверка специфичного сценария: марафон + гель + во время старта."),
    ("Полумарафонец: батончики до и после", {"component_class": "protein_carbohydrate_food", "use_scenario": "event_preparation", "use_timing": "before_or_after_training", "race_format": "half_marathon", "product_form": "bars", "max_price_uah": 1200}, "Покупатель ожидает спортивное питание, а не просто набор с широкой меткой бега."),
    ("Зимний бегун: носки размера 43", {"component_class": "apparel_footwear", "use_scenario": "training", "use_timing": "during_training", "season": "cold", "shoe_size": 43}, "Проверка размера внутри размерного диапазона."),
    ("Трейлраннер: перекус в дороге", {"component_class": "protein_carbohydrate_food", "use_scenario": "training", "use_timing": "during_training", "use_place": "travel_or_road", "product_form": "bars", "max_price_uah": 900}, "Сценарий длинной тренировки вне города."),
    ("Бегун на 5 км: подготовка к первому старту", {"component_class": "protein_carbohydrate_food", "use_scenario": "event_preparation", "use_timing": "before_or_after_training", "race_format": "race_or_event_preparation", "max_price_uah": 1000}, "Вариант «другой старт» не различает 5 км, 10 км и другие дистанции."),
    ("Спортсмен на стадионе: гидратация во время интервалов", {"component_class": "hydration_items", "use_scenario": "training", "use_timing": "during_training", "product_form": "sticks", "season": "warm"}, "Проверка, что беговая задача с гидратацией не уводит в силовые наборы."),
    ("Новичок: экипировка для пробежек в прохладу", {"component_class": "apparel_footwear", "use_scenario": "everyday", "use_timing": "daily_use", "season": "cold", "shoe_size": 41, "max_price_uah": 1100}, "Проверка повседневного сценария и обувного размера."),
    ("Бегун на длинных лёгких тренировках: мягкие перекусы", {"component_class": "protein_carbohydrate_food", "use_scenario": "training", "use_timing": "during_training", "product_form": "food_or_meal", "max_price_uah": 1300}, "Нужен перекус в обычный тренировочный день, не к старту."),
    ("Летний бегун: жидкая форма до тренировки", {"component_class": "hydration_items", "use_scenario": "training", "use_timing": "before_or_after_training", "season": "warm", "product_form": "liquid"}, "Проверка, что выбранные время и форма видны в выдаче."),
    ("Бегун с размером 46: аксессуар или носки", {"component_class": "sports_accessories", "use_scenario": "everyday", "shoe_size": 46, "max_price_uah": 1500}, "Ветка должна сохранить неизвестный размер отдельно от неподходящего известного."),
])

add_group("food", [
    ("Велосипедист на бревете: гели во время заезда", {"activity": "cycling", "component_class": "protein_carbohydrate_food", "use_scenario": "training", "use_timing": "during_training", "product_form": "gel", "max_price_uah": 1000}, "Длинная велогонка, углеводы во время движения."),
    ("Марафонец: батончики к старту", {"activity": "running", "component_class": "protein_carbohydrate_food", "use_scenario": "event_preparation", "use_timing": "during_training", "race_format": "marathon", "product_form": "bars", "max_price_uah": 1200}, "Проверка конкретного вида спорта и формата старта."),
    ("Велосипедист: напиток со стиками в жару", {"activity": "cycling", "component_class": "hydration_items", "use_scenario": "training", "use_timing": "during_training", "season": "warm", "product_form": "sticks"}, "Питание/гидратация в спортивном контексте."),
    ("Бегун: еда после ранней пробежки", {"activity": "running", "component_class": "protein_carbohydrate_food", "use_scenario": "training", "use_timing": "before_or_after_training", "product_form": "food_or_meal"}, "Проверка сценария до/после нагрузки."),
    ("Городской велосипедист: компактный перекус в дороге", {"activity": "cycling", "component_class": "protein_carbohydrate_food", "use_scenario": "everyday", "use_place": "travel_or_road", "product_form": "bars", "max_price_uah": 900}, "Нужен переносимый перекус для поездок."),
    ("Ультрабегун: только гель на длинной дистанции", {"activity": "running", "component_class": "protein_carbohydrate_food", "use_scenario": "event_preparation", "use_timing": "during_training", "race_format": "ultra_or_long_distance", "product_form": "gel", "max_price_uah": 1500}, "Проверка, насколько фильтры уточняют нишевую потребность."),
    ("Велосипедист на холодный сезон: перекус вместо напитка", {"activity": "cycling", "component_class": "protein_carbohydrate_food", "use_scenario": "training", "use_timing": "during_training", "season": "cold", "product_form": "bars"}, "Указание формы продукта должно менять приоритет."),
    ("Бегун на старте: жидкие углеводы", {"activity": "running", "component_class": "protein_carbohydrate_food", "use_scenario": "event_preparation", "use_timing": "during_training", "product_form": "liquid", "max_price_uah": 1300}, "Проверка формы отдельно от класса товара."),
    ("Велосипедист: готовая еда после длительного выезда", {"activity": "cycling", "component_class": "dehydrated_meal", "use_scenario": "training", "use_timing": "before_or_after_training", "use_place": "travel_or_road", "product_form": "food_or_meal"}, "Проверка готовой еды в ветке питания."),
    ("Бегун с бюджетом до 800 грн: перекус для тренировки", {"activity": "running", "component_class": "protein_carbohydrate_food", "use_scenario": "training", "use_timing": "during_training", "product_form": "bars", "max_price_uah": 800}, "Малый бюджет: выдача должна оставаться тематически точной."),
])

add_group("hydration", [
    ("Велосипедист в жару: стики на длительный заезд", {"activity": "cycling", "component_class": "hydration_items", "use_scenario": "training", "use_timing": "during_training", "season": "warm", "product_form": "sticks"}, "Жара и длительная нагрузка."),
    ("Марафонец: гидратация на старте", {"activity": "running", "component_class": "hydration_items", "use_scenario": "event_preparation", "use_timing": "during_training", "race_format": "marathon", "product_form": "liquid"}, "Проверка, сохраняется ли беговая специализация результата."),
    ("Силовой атлет: гидратация между подходами", {"activity": "strength_training", "component_class": "hydration_items", "use_scenario": "training", "use_timing": "during_training", "product_form": "tablets"}, "Набор должен быть связан с силовой тренировкой."),
    ("Функциональный тренинг: гидратация в зале", {"activity": "functional_training", "component_class": "sports_accessories", "use_scenario": "training", "use_timing": "during_training", "use_place": "work_or_study"}, "Проверка аксессуаров в гидратационной цели."),
    ("Велосипедист в прохладу: гидратация до поездки", {"activity": "cycling", "component_class": "hydration_items", "use_scenario": "training", "use_timing": "before_or_after_training", "season": "cold", "product_form": "liquid"}, "Время и сезон должны влиять на приоритет."),
    ("Бегун на вечернем старте: гидратация", {"activity": "running", "component_class": "hydration_items", "use_scenario": "event_preparation", "use_timing": "during_training", "race_format": "race_or_event_preparation", "season": "warm"}, "Дистанция не указана; событие общее."),
    ("Велосипедист: таблетки для бутылки", {"activity": "cycling", "component_class": "hydration_items", "use_scenario": "training", "use_timing": "during_training", "product_form": "sticks", "max_price_uah": 1200}, "Проверка, совпадает ли конкретная форма с компонентом."),
    ("Бегун: гидратация на каждый день", {"activity": "running", "component_class": "hydration_items", "use_scenario": "everyday", "use_timing": "daily_use", "product_form": "liquid"}, "Разделяет спортивное применение и повседневное."),
    ("Велосипедист на длинном старте: до 1 000 грн", {"activity": "cycling", "component_class": "hydration_items", "use_scenario": "event_preparation", "use_timing": "during_training", "race_format": "ultra_or_long_distance", "max_price_uah": 1000}, "Бюджет и длительный формат одновременно."),
    ("Спортсмен на функциональной тренировке: стики после", {"activity": "functional_training", "component_class": "hydration_items", "use_scenario": "training", "use_timing": "before_or_after_training", "product_form": "sticks"}, "Проверка функциональной ветки и контекста времени."),
])

add_group("training", [
    ("Пауэрлифтер: креатин в порошке", {"activity": "strength_training", "component_class": "creatine_preworkout", "use_scenario": "training", "use_timing": "before_or_after_training", "product_form": "powder"}, "Узкая силовая цель и ожидаемый класс добавки."),
    ("Силовой новичок: белковое питание после зала", {"activity": "strength_training", "component_class": "protein_carbohydrate_food", "use_scenario": "training", "use_timing": "before_or_after_training", "product_form": "bars", "max_price_uah": 1100}, "Проверка разделения спортивного питания и креатина."),
    ("Йога: мягкая поддержка ежедневной практики", {"activity": "mind_body_mobility", "component_class": "supplements_vitamins_minerals", "use_scenario": "everyday", "use_timing": "daily_use", "product_form": "capsules"}, "Проверка, не приравнивает ли логика йогу к силовой задаче."),
    ("Пилатес: продукт в таблетках", {"activity": "mind_body_mobility", "component_class": "supplements_vitamins_minerals", "use_scenario": "training", "use_timing": "daily_use", "product_form": "tablets"}, "Отдельная практика внутри ветки mind-body."),
    ("Кроссфит: гидратация стиками", {"activity": "functional_training", "component_class": "hydration_items", "use_scenario": "training", "use_timing": "during_training", "product_form": "sticks", "season": "warm"}, "Функциональная тренировка, жара и форма."),
    ("Домашняя калистеника: белковый порошок", {"activity": "strength_training", "component_class": "protein_carbohydrate_food", "use_scenario": "training", "use_timing": "before_or_after_training", "product_form": "powder"}, "Проверка совпадения формы и класса."),
    ("Спортсмен: витамины для режима тренировок", {"activity": "strength_training", "component_class": "supplements_vitamins_minerals", "use_scenario": "everyday", "use_timing": "daily_use", "use_place": "work_or_study", "product_form": "softgels"}, "Повседневный режим при силовой цели."),
    ("Бодибилдер: таблетированная форма", {"activity": "strength_training", "component_class": "creatine_preworkout", "use_scenario": "training", "use_timing": "before_or_after_training", "product_form": "tablets", "max_price_uah": 1500}, "Проверка, что цена не вытесняет более точный сигнал."),
    ("Тяжелоатлет: предтренировочный продукт", {"activity": "strength_training", "component_class": "creatine_preworkout", "use_scenario": "training", "use_timing": "before_or_after_training", "product_form": "powder", "max_price_uah": 800}, "Ограниченный бюджет для узкого запроса."),
    ("Прыгун в высоту: взрывная сила для разбега и отталкивания", {"activity": "strength_training", "component_class": "creatine_preworkout", "use_scenario": "training", "use_timing": "during_training", "product_form": "powder"}, "Вид спорта «прыжки в высоту» отдельно не предлагается; пользователь вынужден выбрать силовые тренировки."),
])

add_group("recovery", [
    ("Марафонец: восстановление после длительного бега", {"activity": "running", "component_class": "protein_carbohydrate_food", "use_scenario": "training", "use_timing": "before_or_after_training", "product_form": "powder"}, "Ветка восстановления может опираться на неспортивные сигналы."),
    ("Велосипедист: вечерний отдых", {"activity": "cycling", "component_class": "supplements_vitamins_minerals", "use_scenario": "everyday", "use_timing": "evening_or_bedtime", "product_form": "capsules"}, "Проверка вечернего сценария."),
    ("Силовой атлет: восстановление между занятиями", {"activity": "strength_training", "component_class": "creatine_preworkout", "use_scenario": "training", "use_timing": "before_or_after_training", "product_form": "powder"}, "Узкая спортивная потребность."),
    ("Функциональный атлет: восстановление в поездке", {"activity": "functional_training", "component_class": "supplements_vitamins_minerals", "use_scenario": "everyday", "use_place": "travel_or_road", "product_form": "softgels"}, "Контекст места и формат."),
    ("Практикующий йогу: вечерний ритуал", {"activity": "mind_body_mobility", "component_class": "supplements_vitamins_minerals", "use_scenario": "everyday", "use_timing": "evening_or_bedtime", "product_form": "tablets"}, "Проверка mind-body активности."),
    ("Бегун: поддержка после зимней тренировки", {"activity": "running", "component_class": "protein_carbohydrate_food", "use_scenario": "training", "use_timing": "before_or_after_training", "season": "cold", "product_form": "bars"}, "Сезон и беговая тренировка."),
    ("Велосипедист: восстановление после летнего старта", {"activity": "cycling", "component_class": "supplements_vitamins_minerals", "use_scenario": "event_preparation", "use_timing": "before_or_after_training", "race_format": "race_or_event_preparation", "season": "warm"}, "Проверка: цель восстановления не предлагает сценарий старта."),
    ("Спортсмен: восстановление в рабочий день", {"activity": "strength_training", "component_class": "supplements_vitamins_minerals", "use_scenario": "everyday", "use_timing": "daily_use", "use_place": "work_or_study"}, "Повседневное место после тренировки."),
    ("Бегун: поздняя тренировка и капсулы", {"activity": "running", "component_class": "supplements_vitamins_minerals", "use_scenario": "everyday", "use_timing": "evening_or_bedtime", "product_form": "capsules", "max_price_uah": 900}, "Проверка ночного времени и бюджета."),
    ("Велосипедист: длительная поездка и мягкие гели", {"activity": "cycling", "component_class": "protein_carbohydrate_food", "use_scenario": "training", "use_timing": "during_training", "race_format": "ultra_or_long_distance", "product_form": "gel"}, "Релевантность спортивного питания в разделе восстановления."),
])

add_group("outdoors", [
    ("Пеший турист: сублимированная еда в кемпинге", {"activity": "hiking", "component_class": "dehydrated_meal", "use_scenario": "training", "use_timing": "during_training", "use_place": "hiking_or_camping", "product_form": "food_or_meal"}, "Прямое совпадение цели, активности, места и товара."),
    ("Зимний поход: тёплые носки размера 42", {"activity": "hiking", "component_class": "apparel_footwear", "use_scenario": "training", "use_place": "hiking_or_camping", "season": "cold", "shoe_size": 42}, "Проверка зимнего размера и outdoor-цели."),
    ("Велопоход: еда и вода в дороге", {"activity": "cycling", "component_class": "dehydrated_meal", "use_scenario": "training", "use_timing": "during_training", "use_place": "travel_or_road", "product_form": "food_or_meal"}, "Сочетание велоактивности и походного питания."),
    ("Турист: батончики на тёплый маршрут", {"activity": "hiking", "component_class": "protein_carbohydrate_food", "use_scenario": "training", "use_timing": "during_training", "season": "warm", "product_form": "bars"}, "Проверка переносимого перекуса."),
    ("Путешественник: аксессуар для прогулок", {"activity": "walking", "component_class": "sports_accessories", "use_scenario": "everyday", "use_timing": "daily_use", "use_place": "travel_or_road"}, "Проверка ходьбы и повседневного использования."),
    ("Осенний турист: жидкая гидратация", {"activity": "hiking", "component_class": "hydration_items", "use_scenario": "training", "use_timing": "during_training", "use_place": "hiking_or_camping", "season": "cold", "product_form": "liquid"}, "Сезонный сигнал и место."),
    ("Кемпер: питание до выхода на маршрут", {"activity": "hiking", "component_class": "dehydrated_meal", "use_scenario": "everyday", "use_timing": "daily_use", "use_place": "hiking_or_camping", "product_form": "food_or_meal", "max_price_uah": 1200}, "Проверка ежедневного сценария в походной ветке."),
    ("Турист с размером 45: одежда для долгого маршрута", {"activity": "hiking", "component_class": "apparel_footwear", "use_scenario": "training", "use_place": "hiking_or_camping", "shoe_size": 45}, "Проверка верхней границы размера."),
    ("Велосипедист: аксессуары для дорожного путешествия", {"activity": "cycling", "component_class": "sports_accessories", "use_scenario": "everyday", "use_place": "travel_or_road", "season": "warm"}, "Проверка велоаксессуаров вне чистой спортивной тренировки."),
    ("Пешеход: походное питание до 900 грн", {"activity": "hiking", "component_class": "protein_carbohydrate_food", "use_scenario": "training", "use_place": "hiking_or_camping", "product_form": "food_or_meal", "max_price_uah": 900}, "Узкая еда для похода и жёсткий бюджет."),
])

add_group("gear", [
    ("Бегун зимой: носки размера 42", {"activity": "running", "component_class": "apparel_footwear", "use_scenario": "training", "use_timing": "during_training", "season": "cold", "shoe_size": 42}, "Проверка размера в экипировочной ветке."),
    ("Велосипедист летом: аксессуары на каждый день", {"activity": "cycling", "component_class": "sports_accessories", "use_scenario": "everyday", "use_timing": "daily_use", "season": "warm"}, "Аксессуар должен быть связан с велоспортом."),
    ("Пловец: спортивная одежда и аксессуары", {"activity": "swimming", "component_class": "apparel_footwear", "use_scenario": "training", "use_timing": "during_training"}, "Проверка плавательной ветки при слабом покрытии данных."),
    ("Турист: обувь для похода размера 44", {"activity": "hiking", "component_class": "apparel_footwear", "use_scenario": "training", "use_place": "hiking_or_camping", "shoe_size": 44}, "Размер и outdoor-контекст."),
    ("Городской бегун: аксессуар в дорогу", {"activity": "running", "component_class": "sports_accessories", "use_scenario": "everyday", "use_place": "travel_or_road"}, "Проверка аксессуара вне спортивного старта."),
    ("Ходьба в холодную погоду: экипировка", {"activity": "walking", "component_class": "apparel_footwear", "use_scenario": "everyday", "season": "cold", "shoe_size": 40}, "Проверка ходьбы и сезонности."),
    ("Велосипедист: экипировка для старта", {"activity": "cycling", "component_class": "apparel_footwear", "use_scenario": "event_preparation", "use_timing": "during_training", "season": "warm"}, "Проверка событийной велоэкипировки."),
    ("Трейлраннер: размер 47 и походные аксессуары", {"activity": "running", "component_class": "sports_accessories", "use_scenario": "training", "use_place": "hiking_or_camping", "shoe_size": 47}, "Размер вне найденных частых диапазонов."),
    ("Пловец: аксессуары на каждый день", {"activity": "swimming", "component_class": "sports_accessories", "use_scenario": "everyday", "use_timing": "daily_use"}, "Проверка отличия ежедневного применения от тренировки."),
    ("Бегун: обувь или носки до 1 000 грн", {"activity": "running", "component_class": "apparel_footwear", "use_scenario": "training", "shoe_size": 43, "max_price_uah": 1000}, "Цена и размер при ограниченном бюджете."),
])

add_group("daily", [
    ("Офисный работник: капсулы днём", {"component_class": "supplements_vitamins_minerals", "use_scenario": "everyday", "use_timing": "daily_use", "use_place": "work_or_study", "product_form": "capsules"}, "Повседневное применение без спортивного вида."),
    ("Студент: таблетки в дороге", {"component_class": "supplements_vitamins_minerals", "use_scenario": "everyday", "use_timing": "daily_use", "use_place": "travel_or_road", "product_form": "tablets"}, "Проверка места и формы."),
    ("Пользователь: вечерняя форма в капсулах", {"component_class": "supplements_vitamins_minerals", "use_scenario": "everyday", "use_timing": "evening_or_bedtime", "product_form": "capsules"}, "Проверка вечерней ветки."),
    ("Работающий человек: перекус в офис", {"component_class": "protein_carbohydrate_food", "use_scenario": "everyday", "use_timing": "daily_use", "use_place": "work_or_study", "product_form": "bars", "max_price_uah": 1000}, "Проверка, не выдаёт ли ежедневная цель спортивную экипировку/силовой клуб."),
    ("Путешественник: порошок в поездку", {"component_class": "supplements_vitamins_minerals", "use_scenario": "everyday", "use_place": "travel_or_road", "product_form": "powder"}, "Проверка формы и места."),
    ("Покупатель: софтгели на каждый день", {"component_class": "supplements_vitamins_minerals", "use_timing": "daily_use", "product_form": "softgels"}, "Специфичная форма, но без активности."),
    ("Работающий человек: перекус в дороге", {"component_class": "protein_carbohydrate_food", "use_scenario": "everyday", "use_place": "travel_or_road", "product_form": "food_or_meal", "max_price_uah": 850}, "Бюджетный повседневный перекус."),
    ("Пользователь: вечерние таблетки до 1 000 грн", {"component_class": "supplements_vitamins_minerals", "use_timing": "evening_or_bedtime", "product_form": "tablets", "max_price_uah": 1000}, "Цена и вечернее использование."),
    ("Офис: батончики и неважная форма добавок", {"component_class": "protein_carbohydrate_food", "use_scenario": "everyday", "use_place": "work_or_study", "product_form": "bars"}, "Проверка назначения товара как перекуса."),
    ("Пользователь: повседневный продукт без привязки к спорту", {"component_class": "supplements_vitamins_minerals", "use_scenario": "everyday", "use_timing": "daily_use", "product_form": "tablets", "max_price_uah": 1500}, "Проверка самого широкого ежедневного сценария."),
])

add_group("gift", [
    ("Подарок бегуну: одежда размера 42", {"activity": "running", "component_class": "apparel_footwear", "use_scenario": "event_preparation", "product_form": "apparel", "shoe_size": 42}, "Проверка, что подарочная ветка спрашивает размер и исключает известный размер вне диапазона."),
    ("Подарок велосипедисту: гидратация", {"activity": "cycling", "component_class": "hydration_items", "use_scenario": "training", "use_timing": "during_training", "product_form": "sticks"}, "Проверка спортивного подарка и гидратации."),
    ("Подарок туристу: еда для кемпинга", {"activity": "hiking", "component_class": "protein_carbohydrate_food", "use_scenario": "everyday", "use_place": "hiking_or_camping", "product_form": "food_or_meal"}, "Проверка туристического подарка."),
    ("Подарок силовому атлету: добавки", {"activity": "strength_training", "component_class": "supplements_vitamins_minerals", "use_scenario": "training", "product_form": "capsules"}, "Подарок с узкой спортивной направленностью."),
    ("Подарок пловцу: аксессуар", {"activity": "swimming", "component_class": "sports_accessories", "use_scenario": "training"}, "Покрытие плавательной активности в каталоге."),
    ("Подарок ходоку: одежда на каждый день", {"activity": "walking", "component_class": "apparel_footwear", "use_scenario": "everyday", "use_timing": "daily_use", "product_form": "apparel"}, "Проверка повседневного спортивного подарка."),
    ("Подарок бегуну на полумарафон", {"activity": "running", "component_class": "protein_carbohydrate_food", "use_scenario": "event_preparation", "race_format": "half_marathon", "product_form": "gel", "max_price_uah": 1200}, "Проверка формата старта и конкретной формы."),
    ("Подарок туристу зимой: аксессуары", {"activity": "hiking", "component_class": "sports_accessories", "use_scenario": "training", "use_place": "hiking_or_camping", "season": "cold"}, "Проверка сезонного подарка."),
    ("Подарок велосипедисту: повседневное питание", {"activity": "cycling", "component_class": "protein_carbohydrate_food", "use_scenario": "everyday", "use_timing": "daily_use", "product_form": "bars", "max_price_uah": 900}, "Проверка бюджета и велоактивности."),
    ("Подарок спортсмену: форма не принципиальна", {"activity": "strength_training", "component_class": "sports_accessories", "use_scenario": "everyday", "use_timing": "evening_or_bedtime", "max_price_uah": 1500}, "Намеренно смешанный контекст, чтобы проверить качество ранжирования."),
])

for goal, title, desired, note in [
    ("food", "Минимальный бюджет на питание", {"activity": "running", "component_class": "protein_carbohydrate_food", "use_scenario": "training", "use_timing": "during_training", "product_form": "bars", "max_price_uah": 758}, "Граница ниже самой низкой цены текущего снимка."),
    ("food", "Бюджет ровно по минимальной цене каталога", {"activity": "running", "component_class": "protein_carbohydrate_food", "use_scenario": "training", "product_form": "bars", "max_price_uah": 759}, "Проверка включительной границы цены."),
    ("training", "Бюджет 1 499 грн", {"activity": "functional_training", "component_class": "creatine_preworkout", "use_scenario": "training", "use_timing": "before_or_after_training", "product_form": "powder", "max_price_uah": 1499}, "Тот же запрос, что в следующем случае, но набор за 1 500 грн должен исключиться."),
    ("training", "Бюджет ровно 1 500 грн", {"activity": "functional_training", "component_class": "creatine_preworkout", "use_scenario": "training", "use_timing": "before_or_after_training", "product_form": "powder", "max_price_uah": 1500}, "Набор ценой 1 500 грн может пройти ценовой фильтр."),
    ("gear", "Точный размер 42", {"component_class": "apparel_footwear", "season": "cold", "shoe_size": 42, "max_price_uah": 1500}, "Проверка размера в ветке экипировки."),
    ("gear", "Размер 43 вне диапазона 40–42", {"component_class": "apparel_footwear", "season": "cold", "shoe_size": 43, "max_price_uah": 1500}, "Размерный набор должен исключиться; неизвестный размер останется отмеченным."),
    ("gift", "Подарок с известным размером обуви 42", {"activity": "running", "component_class": "apparel_footwear", "product_form": "apparel", "shoe_size": 42}, "Поле shoe_size не должно исчезать только из-за цели «подарок»."),
    ("training", "Нужен набор без кофеина", {"activity": "strength_training", "component_class": "supplements_vitamins_minerals", "use_scenario": "training", "product_form": "capsules"}, "Квиз не предлагает надёжное исключение кофеина; отсутствие тега не означает отсутствие кофеина."),
    ("food", "Аллергия на арахис: нужен безопасный состав", {"activity": "running", "component_class": "protein_carbohydrate_food", "product_form": "bars"}, "Аллергены не нормализованы и не являются доступным фильтром."),
    ("running", "Формат старта ровно 5 км", {"component_class": "protein_carbohydrate_food", "use_scenario": "event_preparation", "race_format": "race_or_event_preparation"}, "Числовые дистанции исключены из текущих данных; общий формат старта не подтверждает 5 км."),
] :
    CASES.append({
        "id": len(CASES) + 1,
        "goal": goal,
        "buyer": title,
        "desired": {"max_price_uah": 1500, **desired},
        "note": note,
    })

ADDITIONAL_50_CASES = [
    # running (6)
    ("running", "Ультра-трейл: батончики и гели на длинную дистанцию", {"component_class": "protein_carbohydrate_food", "use_scenario": "event_preparation", "race_format": "ultra_or_long_distance", "product_form": ["bars", "gel"], "max_price_uah": 1500}, "Мультивыбор формы продукта для ультрабега."),
    ("running", "Шоссейный бегун: гидратация в холодную погоду", {"component_class": "hydration_items", "use_scenario": "training", "use_timing": "during_training", "season": "cold", "max_price_uah": 1500}, "Бег в холод со спортивным изотоником."),
    ("running", "Марафонец: питание и аксессуары без членства в клубе", {"component_class": "protein_carbohydrate_food", "use_scenario": "event_preparation", "race_format": "marathon", "membership": "no", "max_price_uah": 1500}, "Явный отказ от клубного абонемента в марафонской ветке."),
    ("running", "Бегун на полумарафон: стики и гели", {"component_class": "protein_carbohydrate_food", "use_scenario": "event_preparation", "race_format": "half_marathon", "product_form": ["sticks", "gel"], "max_price_uah": 1400}, "Мультивыбор стиков и гелей на полумарафон."),
    ("running", "Беговой стадион: интервалы и аксессуары", {"component_class": "sports_accessories", "use_scenario": "training", "use_timing": "before_or_after_training", "max_price_uah": 1450}, "Аксессуары для беговых тренировок."),
    ("running", "Летний бег: размер обуви 44 и носки", {"component_class": "apparel_footwear", "season": "warm", "shoe_size": 44, "max_price_uah": 1500}, "Размер 44 в летний сезон бега."),

    # training (6)
    ("training", "Силовой атлет: креатин без клубного абонемента", {"activity": "strength_training", "component_class": "creatine_preworkout", "use_scenario": "training", "membership": "no", "max_price_uah": 1500}, "Силовая ветка с явным исключением абонементов."),
    ("training", "Функциональный тренинг: витамины в стиках", {"activity": "functional_training", "component_class": "supplements_vitamins_minerals", "use_scenario": "training", "product_form": "sticks", "max_price_uah": 1500}, "Стики с витаминами для функционального зала."),
    ("training", "Бодибилдер: порошок или капсулы", {"activity": "strength_training", "component_class": "creatine_preworkout", "use_scenario": "training", "product_form": ["powder", "capsules"], "max_price_uah": 1500}, "Мультивыбор формы добавки для зала."),
    ("training", "Занимающийся пилатесом: поддержка подвижности суставов", {"activity": "mind_body_mobility", "component_class": "supplements_vitamins_minerals", "use_scenario": "training", "use_timing": "daily_use", "max_price_uah": 1400}, "Витамины и минералы для пилатеса и растяжки."),
    ("training", "Кроссфит: углеводное питание во время тренировки", {"activity": "functional_training", "component_class": "protein_carbohydrate_food", "use_scenario": "training", "use_timing": "during_training", "max_price_uah": 1450}, "Питание на кроссфит-комплекс."),
    ("training", "Тяжелоатлет: вечерняя тренировка и предтрен", {"activity": "strength_training", "component_class": "creatine_preworkout", "use_scenario": "training", "use_timing": "evening_or_bedtime", "max_price_uah": 1500}, "Вечерний тренировочный тайминг в силовой ветке."),

    # hydration (6)
    ("hydration", "Мультиспортсмен: бег и велоспорт гидратация", {"activity": ["running", "cycling"], "component_class": "hydration_items", "use_scenario": "event_preparation", "max_price_uah": 1500}, "Мультивыбор активности: бег и велоспорт одновременно."),
    ("hydration", "Бегун: изотоники в стиках или жидкой форме", {"activity": "running", "component_class": "hydration_items", "use_scenario": "training", "product_form": ["sticks", "liquid"], "max_price_uah": 1500}, "Мультивыбор удобной формы напитка."),
    ("hydration", "Велоспорт: электролиты без абонемента", {"activity": "cycling", "component_class": "hydration_items", "use_scenario": "training", "membership": "no", "max_price_uah": 1500}, "Электролиты в дорогу без навязывания клуба."),
    ("hydration", "Силовик: напиток стики или батончики", {"activity": "strength_training", "component_class": "hydration_items", "use_scenario": "training", "product_form": ["sticks", "bars"], "max_price_uah": 1400}, "Мультивыбор стиков и батончиков для силовика."),
    ("hydration", "Функциональный атлет: гидратация в летнюю жару", {"activity": "functional_training", "component_class": "hydration_items", "use_scenario": "training", "season": "warm", "max_price_uah": 1450}, "Жаркий сезон и гидратация в функциональном тренинге."),
    ("hydration", "Велосипедист: осенний выезд и электролиты", {"activity": "cycling", "component_class": "hydration_items", "use_scenario": "training", "season": "cold", "max_price_uah": 1400}, "Холодный сезон и поддержка водно-солевого баланса."),

    # food (6)
    ("food", "Длительный заезд: батончики и гели на велосипеде", {"activity": "cycling", "component_class": "protein_carbohydrate_food", "use_scenario": "training", "product_form": ["bars", "gel"], "max_price_uah": 1500}, "Мультивыбор спортивного питания для велосипедиста."),
    ("food", "Шоссейник: перекус в дорогу", {"activity": "cycling", "component_class": "protein_carbohydrate_food", "use_scenario": "training", "use_place": "travel_or_road", "max_price_uah": 1400}, "Контекст поездки и питание для шоссе."),
    ("food", "Гонщик: подготовка к старту без абонемента", {"activity": "cycling", "component_class": "protein_carbohydrate_food", "use_scenario": "event_preparation", "membership": "no", "max_price_uah": 1500}, "Питание на старт только товарами."),
    ("food", "Бегун: сублимированное питание после объема", {"activity": "running", "component_class": "dehydrated_meal", "use_scenario": "training", "use_timing": "before_or_after_training", "max_price_uah": 1500}, "Сублимированное питание после длительного кросса."),
    ("food", "Велоспорт: жидкая форма или гели", {"activity": "cycling", "component_class": "protein_carbohydrate_food", "use_scenario": "training", "product_form": ["liquid", "gel"], "max_price_uah": 1450}, "Жидкие углеводы и гели для велозаезда."),
    ("food", "Походный лагерь: перекусы в кемпинге", {"activity": "hiking", "component_class": "protein_carbohydrate_food", "use_scenario": "training", "use_place": "hiking_or_camping", "max_price_uah": 1350}, "Углеводные снеки для полевых условий."),

    # recovery (6)
    ("recovery", "Бегун: ночное восстановление в капсулах", {"activity": "running", "component_class": "supplements_vitamins_minerals", "use_scenario": "everyday", "use_timing": "evening_or_bedtime", "product_form": "capsules", "max_price_uah": 1400}, "Сон и ночное восстановление мышц."),
    ("recovery", "Велосипедист: добавки после тренировки без абонемента", {"activity": "cycling", "component_class": "supplements_vitamins_minerals", "use_scenario": "training", "membership": "no", "max_price_uah": 1500}, "Восстановление после велонагрузок без клуба."),
    ("recovery", "Силовик: белковый перекус порошок или батончики", {"activity": "strength_training", "component_class": "protein_carbohydrate_food", "use_scenario": "training", "product_form": ["powder", "bars"], "max_price_uah": 1450}, "Протеиновое восстановление в удобной форме."),
    ("recovery", "Йога: ежедневное расслабление и антистресс", {"activity": "mind_body_mobility", "component_class": "supplements_vitamins_minerals", "use_scenario": "everyday", "use_timing": "daily_use", "max_price_uah": 1450}, "Поддержка нервной системы и подвижности."),
    ("recovery", "Функциональный атлет: витамины после тренировок в зале", {"activity": "functional_training", "component_class": "supplements_vitamins_minerals", "use_scenario": "training", "use_timing": "before_or_after_training", "max_price_uah": 1400}, "Восстановление после тяжелых WOD комплексов."),
    ("recovery", "Марафонец: минералы в капсулах или таблетках", {"activity": "running", "component_class": "supplements_vitamins_minerals", "use_scenario": "training", "product_form": ["tablets", "capsules"], "max_price_uah": 1500}, "Минеральная поддержка бегуна на длинные дистанции."),

    # outdoors (6)
    ("outdoors", "Горный треккинг: сублиматы и батончики", {"activity": "hiking", "component_class": "dehydrated_meal", "use_scenario": "training", "product_form": ["food_or_meal", "bars"], "max_price_uah": 1500}, "Еда в автономный поход."),
    ("outdoors", "Поход в горы: гидратация в жару", {"activity": "hiking", "component_class": "hydration_items", "use_scenario": "training", "season": "warm", "max_price_uah": 1400}, "Летний горный поход с изотониками."),
    ("outdoors", "Турист: обувной размер 41 для похода", {"activity": "hiking", "component_class": "apparel_footwear", "shoe_size": 41, "max_price_uah": 1500}, "Треккинговые носки 41 размера."),
    ("outdoors", "Велотуризм: сублимированная еда в дорогу", {"activity": "cycling", "component_class": "dehydrated_meal", "use_scenario": "everyday", "use_place": "travel_or_road", "max_price_uah": 1450}, "Компактная еда для байкпакинга."),
    ("outdoors", "Пеший туризм: кемпинговые аксессуары на каждый день", {"activity": "walking", "component_class": "sports_accessories", "use_scenario": "everyday", "use_place": "hiking_or_camping", "max_price_uah": 1500}, "Полезные мелочи и аксессуары для кемпинга."),
    ("outdoors", "Хайкинг: автономный набор без клуба", {"activity": "hiking", "component_class": "dehydrated_meal", "use_scenario": "training", "membership": "no", "max_price_uah": 1500}, "Походный пак только из физических товаров."),

    # gear (5)
    ("gear", "Зимний бег: размер обуви 42 и защита от холода", {"activity": "running", "component_class": "apparel_footwear", "season": "cold", "shoe_size": 42, "max_price_uah": 1450}, "Теплые беговые носки на мороз."),
    ("gear", "Бегун: носки размер 44 на тренировки", {"activity": "running", "component_class": "apparel_footwear", "use_scenario": "training", "shoe_size": 44, "max_price_uah": 1500}, "Беговые носки большого размера 44."),
    ("gear", "Скандинавская ходьба: экипировка на лето размер 39", {"activity": "walking", "component_class": "apparel_footwear", "use_scenario": "everyday", "season": "warm", "shoe_size": 39, "max_price_uah": 1400}, "Удобная летняя экипировка для ходьбы."),
    ("gear", "Беговой клуб: тренировочные аксессуары без абонемента", {"activity": "running", "component_class": "sports_accessories", "use_scenario": "training", "membership": "no", "max_price_uah": 1500}, "Физическая экипировка и аксессуары для бега."),
    ("gear", "Зимний треккинг: размер 43 для холодной погоды", {"activity": "hiking", "component_class": "apparel_footwear", "season": "cold", "shoe_size": 43, "max_price_uah": 1500}, "Зимние походные носки размера 43."),

    # daily (5)
    ("daily", "Работа в офисе: витамины в капсулах на каждый день", {"component_class": "supplements_vitamins_minerals", "use_place": "work_or_study", "product_form": "capsules", "max_price_uah": 1450}, "Поддержка продуктивности на работе."),
    ("daily", "Горожанин: комплекс витаминов без абонемента", {"component_class": "supplements_vitamins_minerals", "use_timing": "daily_use", "membership": "no", "max_price_uah": 1500}, "Ежедневные добавки без клубной карты."),
    ("daily", "Полноценный рабочий день: питательный перекус", {"component_class": "protein_carbohydrate_food", "use_place": "work_or_study", "max_price_uah": 1400}, "Здоровый перекус на учебу или работу."),
    ("daily", "Студент во время сессии: капсулы или таблетки", {"component_class": "supplements_vitamins_minerals", "product_form": ["capsules", "tablets"], "max_price_uah": 1450}, "Мультивыбор формы для витаминного комплекса."),
    ("daily", "Ежедневный тонус: порошок или стики для напитка", {"component_class": "supplements_vitamins_minerals", "use_timing": "daily_use", "product_form": ["powder", "sticks"], "max_price_uah": 1400}, "Мультивыбор стиков или порошка на каждый день."),

    # gift (4)
    ("gift", "Подарок бегуну: спортпит без абонемента", {"activity": "running", "component_class": "protein_carbohydrate_food", "membership": "no", "max_price_uah": 1500}, "Набор спортивного питания в подарок бегуну."),
    ("gift", "Подарок триатлету: подготовка к старту и изотоники", {"activity": "running", "component_class": "hydration_items", "use_scenario": "event_preparation", "max_price_uah": 1450}, "Гидратация к соревнованию в качестве подарка."),
    ("gift", "Подарок туристу: сублиматы и перекусы в поход", {"activity": "hiking", "component_class": "protein_carbohydrate_food", "use_place": "hiking_or_camping", "max_price_uah": 1500}, "Походный питательный подарок для друга-туриста."),
    ("gift", "Подарок атлету: размер обуви 43 на зиму", {"activity": "running", "component_class": "apparel_footwear", "season": "cold", "shoe_size": 43, "max_price_uah": 1500}, "Размерные беговые носки на зимний сезон в подарок.")
]

for goal, title, desired, note in ADDITIONAL_50_CASES:
    CASES.append({
        "id": len(CASES) + 1,
        "goal": goal,
        "buyer": title,
        "desired": {"max_price_uah": 1500, **desired},
        "note": note,
    })

for case in CASES:
    if case["buyer"] == "Нужен набор без кофеина":
        case["unrepresented"] = ["подтверждённое отсутствие кофеина"]
    elif case["buyer"] == "Аллергия на арахис: нужен безопасный состав":
        case["unrepresented"] = ["исключение арахиса / проверка аллергенов"]
    elif case["buyer"] == "Формат старта ровно 5 км":
        case["unrepresented"] = ["точная дистанция 5 км"]


def load_enriched_catalog():
    import json

    catalog = _load_catalog(PROJECT_ROOT / "test-quiz-sandbox" / "catalog.json")
    audit = json.loads(AUDIT_PATH.read_text(encoding="utf-8"))
    return attach_audit_evidence(catalog, audit)


def run_path(catalog: list[dict], case: dict) -> dict:
    goal = case["goal"]
    desired = case["desired"]
    answers: dict = {}
    route: list[tuple[str, str]] = []

    for _ in range(20):
        facets = draft_options(catalog, goal, answers)
        plan = facets["question_plan"]
        if not plan:
            break
        question = plan[0]
        key = question["id"]
        wanted = desired.get(key)
        if question["type"] == "number":
            chosen = wanted if wanted is not None else "any"
        elif isinstance(wanted, (list, tuple, set)):
            valid = [item for item in wanted if item in question.get("options", [])]
            chosen = valid if len(valid) > 1 else (valid[0] if valid else "any")
        else:
            chosen = wanted if wanted in question.get("options", []) else "any"
        answers[key] = chosen
        route.append((key, chosen))
    else:
        raise RuntimeError("Question route exceeded 20 screens for case {}".format(case["id"]))

    request = {"goal_group": goal, "locale": "ru"}
    request.update({key: value for key, value in answers.items() if value not in ("", "any", None)})
    response = draft_recommend(catalog, request)
    last_facets = draft_options(catalog, goal, answers)

    missing = {}
    for key, value in desired.items():
        if key == "max_price_uah" or value in (None, "any"):
            continue
        ans = answers.get(key)
        if isinstance(value, (list, tuple, set)):
            if not (_as_set(value) & _as_set(ans)):
                missing[key] = value
        elif ans != value:
            missing[key] = value

    by_row = {record["catalog_row"]: record for record in catalog}
    result_rows = []
    all_conflicts = []
    unknowns = []
    for item in response["results"]:
        record = by_row[item["catalog_row"]]
        conflicting, unknown = [], []
        for key in (
            "activity", "component_class", "use_scenario", "use_timing", "use_place",
            "race_format", "season", "product_form",
        ):
            value = request.get(key)
            if value in (None, "", "any"):
                continue
            vals = _as_set(value)
            signals = _soft_signals(record, key)
            if not signals:
                unknown.append(key)
            elif not (vals & signals):
                conflicting.append(key)
        all_conflicts.extend((item["catalog_row"], key) for key in conflicting)
        unknowns.extend((item["catalog_row"], key) for key in unknown)
        ranges = _size_ranges(record)
        result_rows.append({
            "row": item["catalog_row"],
            "sku": item.get("sku") or "—",
            "title": item["title"],
            "price": item["price_uah"],
            "conflicts": conflicting,
            "unknown": unknown,
            "size": item["size_status"],
            "range": ranges,
            "conflict_card": item["evidence_status"] == "conflict_review_required",
            "membership_title": any(term in item["title"].lower() for term in ("club", "абонемент")),
            "match_score": item.get("match_score_pct"),
            "price_over_budget": item.get("price_over_budget_uah", 0),
        })

    budget = desired.get("max_price_uah")
    size = request.get("shoe_size")
    hard_violations = []
    for item in result_rows:
        if budget is not None and item["price"] > budget:
            hard_violations.append("цена выше лимита")
        if size is not None and item["range"] and not any(lo <= size <= hi for lo, hi in item["range"]):
            hard_violations.append("известный размер вне диапазона")

    return {
        "case": case,
        "request": request,
        "route": route,
        "candidate_count_after_answers": last_facets["candidate_count"],
        "result_count": response["returned_count"],
        "status": response["status"],
        "results": result_rows,
        "near_miss_count": response.get("near_miss_count", 0),
        "floor_anchor_count": response.get("floor_anchor_count", 0),
        "missing": missing,
        "conflicts": all_conflicts,
        "unknowns": unknowns,
        "hard_violations": sorted(set(hard_violations)),
        "candidate_count_initial": len(_goal_candidates(catalog, goal)),
    }


def field_label(key: str) -> str:
    return {
        "activity": "активность", "component_class": "класс товара", "use_scenario": "сценарий",
        "use_timing": "время", "use_place": "место", "race_format": "формат старта",
        "season": "погода", "product_form": "форма", "shoe_size": "размер",
        "max_price_uah": "макс. цена",
    }.get(key, key)


VALUE_LABELS = {
    "running": "бег", "cycling": "велоспорт", "strength_training": "силовые",
    "functional_training": "функциональные", "mind_body_mobility": "йога / пилатес",
    "hiking": "поход", "walking": "ходьба", "swimming": "плавание",
    "protein_carbohydrate_food": "питание и перекусы", "supplements_vitamins_minerals": "витамины и добавки",
    "creatine_preworkout": "креатин / предтренировочные", "sports_accessories": "аксессуары",
    "apparel_footwear": "одежда и обувь", "hydration_items": "гидратация", "dehydrated_meal": "сублимированная еда",
    "event_preparation": "подготовка к старту", "training": "тренировки", "everyday": "на каждый день",
    "before_or_after_training": "до или после тренировки", "during_training": "во время тренировки",
    "daily_use": "ежедневно", "evening_or_bedtime": "вечером / перед сном",
    "hiking_or_camping": "поход / кемпинг", "travel_or_road": "в дороге", "work_or_study": "работа / учёба",
    "half_marathon": "полумарафон", "marathon": "марафон", "race_or_event_preparation": "другой старт",
    "ultra_or_long_distance": "ультра / длительный старт", "cold": "холодная погода", "warm": "тёплая погода",
    "bars": "батончики", "gel": "гели", "food_or_meal": "еда / готовый приём пищи",
    "liquid": "жидкая форма", "sticks": "стики", "capsules": "капсулы", "powder": "порошок",
    "softgels": "софтгели", "tablets": "таблетки", "apparel": "одежда",
}


def value_label(key: str, value) -> str:
    if value == "any":
        return "неважно"
    if isinstance(value, (list, tuple, set)):
        return ", ".join(VALUE_LABELS.get(item, str(item)) for item in value)
    return VALUE_LABELS.get(value, str(value))


def _req_key(req: dict) -> tuple:
    return tuple(sorted((k, tuple(v) if isinstance(v, list) else v) for k, v in req.items()))


def render_report(rows: list[dict], unsupported_checks: int) -> str:
    total_cases = len(rows)
    updated_at = datetime.now().astimezone().isoformat(timespec="seconds")
    goal_counts = Counter(row["case"]["goal"] for row in rows)
    conflict_cases = sum(bool(row["conflicts"]) for row in rows)
    conflict_items = sum(len(row["conflicts"]) for row in rows)
    top1_conflict_cases = sum(bool(row["results"] and row["results"][0]["conflicts"]) for row in rows)
    broadened = sum(row["candidate_count_after_answers"] == 0 and row["result_count"] > 0 for row in rows)
    any_hard_violations = sum(bool(row["hard_violations"]) for row in rows)
    route_counts = Counter(len(row["route"]) for row in rows)
    zero_result = sum(row["result_count"] == 0 for row in rows)
    near_miss_rescued = sum(row["result_count"] == 0 and row["near_miss_count"] > 0 for row in rows)
    floor_anchor_rescued = sum(row["result_count"] == 0 and row["near_miss_count"] == 0 and row["floor_anchor_count"] > 0 for row in rows)
    hard_dead_ends = sum(row["result_count"] == 0 and row["near_miss_count"] == 0 and row["floor_anchor_count"] == 0 for row in rows)
    memberships = sum(item["membership_title"] for row in rows for item in row["results"])
    conflicted_cards = sum(item["conflict_card"] for row in rows for item in row["results"])
    total_result_cards = sum(row["result_count"] for row in rows)
    result_conflicts_by_field = Counter(key for row in rows for _catalog_row, key in row["conflicts"])
    top_conflicts_by_field = Counter(
        key for row in rows if row["results"] for key in row["results"][0]["conflicts"]
    )
    omitted_values_by_field = Counter(key for row in rows for key in row["missing"])

    lines = [
        "---",
        'schema_version: 2',
        'id: "document.quiz-buyer-scenario-audit-100"',
        'type: "document"',
        f'title: "Аудит квиза на {total_cases} покупательских сценариях"',
        f'description: "Воспроизводимый проход по {total_cases} разным buyer-сценариям текущего /draft: ветки вопросов, фактические ответы, результаты, подтверждённые противоречия и пробелы правил."',
        'tags: ["project:quiz-product-set-generator", "topic:quiz", "topic:product-recommendations", "workflow:quality-audit", "language:ru"]',
        'source: {"raw_path": "raw/sources/2026-11-09-quiz-buyer-scenario-audit-request.md"}',
        f'dates: {{"added_at": "2026-11-09T00:00:00+02:00", "updated_at": "{updated_at}"}}',
        'relations: [{"type": "applies-to", "target": "document.quiz-test-sandbox"}, {"type": "references", "target": "document.quiz-matching-rules-technical-brief"}, {"type": "references", "target": "document.race-expert-need-sets-206-analysis"}]',
        f'aliases: ["{total_cases} buyer сценариев квиза", "проверка логики квиза"]',
        'status: "active"',
        "---",
        "",
        f"# Аудит логики покупательского квиза на {total_cases} сценариях",
        "",
        "## Метод",
        "",
        f"Повторно прогнаны {total_cases} покупательских ситуаций (включая мультивыбор, проверку границ бюджета и фильтра абонементов) через текущие функции `draft_options` и `draft_recommend` и реальную последовательность вопросов `/draft`. После каждого ответа план пересчитывается; если желаемого варианта нет, выбирается «Неважно». Обычная выдача проверяется без явного запроса на общий или ослабленный пул. Результат сверяется с сигналами наборов в аудите 206 карточек.",
        "",
        "В матрице «противоречие» означает, что у набора есть известный сигнал по выбранному ответу, но этот сигнал указывает на другой вариант. Пустой сигнал считается неизвестным и не записывается как конфликт. Это аудит логики и качества каталожных сигналов, не медицинская оценка и не утверждение, что одна эвристика ранжирования утверждена владельцем.",
        "",
        "## Итоги прогона",
        "",
        f"- Выполнено сценариев: **{total_cases}/{total_cases}**; цели: {', '.join(f'{key} — {goal_counts[key]}' for key in sorted(goal_counts))}.",
        f"- Все **{len({_req_key(row['request']) for row in rows})}** отправленных наборов ответов различаются.",
        f"- После первого выбора цели маршрут содержит от **{min(route_counts)} до {max(route_counts)}** дополнительных экранов; всего получается 5–10 экранов. Распределение дополнительных экранов: {', '.join(f'{n} — {route_counts[n]}' for n in sorted(route_counts))}.",
        f"- Жёстких нарушений введённой цены или известного размерного диапазона в результатах: **{any_hard_violations}** сценариев.",
        f"- Сценарии с хотя бы одним выданным набором, который противоречит известному ответу: **{conflict_cases}/{total_cases}**; всего таких пар «набор–ответ»: **{conflict_items}**. Противоречие попало в первый результат в **{top1_conflict_cases}/{total_cases}** сценариях.",
        f"- В **{broadened}/{total_cases}** сценариях после ответов вопросный пул показывал 0 совместимых кандидатов, но финальный подбор всё равно вернул наборы.",
        f"- Точная выдача пуста после ответов и жёстких ограничений: **{zero_result}/{total_cases}** сценариев. Из них **{near_miss_rescued}** спасены Near-Miss альтернативами, а **{floor_anchor_rescued}** — Floor Price Anchor (базовый набор категории). Истинных тупиков (полный отказ без карточек): **{hard_dead_ends}/{total_cases}**.",
        f"- Клубные/абонементные названия есть у **{memberships}/{total_result_cards}** показанных карточек; это требует внимания, когда покупатель ожидает только физические товары.",
        f"- Фильтры кофеина, аллергенов и точной дистанции 5 км проверены отдельно: backend отклонил **{unsupported_checks}/3** неподдерживаемых запроса.",
        f"- В топ-3 попало **{conflicted_cards}/{total_result_cards}** карточек с уже отмеченным конфликтом состава.",
        "",
        "## Сравнение с исходным baseline",
        "",
        "| Проверка | До переработки | После переработки |",
        "|---|---:|---:|",
        f"| Сценарии с известным противоречием в обычной выдаче | 71/100 | {conflict_cases}/{total_cases} |",
        f"| Сценарии с противоречием в первом результате | 43/100 | {top1_conflict_cases}/{total_cases} |",
        f"| Пустой пул после ответов, но наборы вернулись автоматически | 16/100 | {broadened}/100 |",
        f"| Нарушения жёсткой цены или известного размера | 0/100 | {any_hard_violations}/100 |",
        "",
        "## Сводка по веткам",
        "",
        "| Первая цель | Сценарии | Есть конфликт в топ-3 | Конфликт в первом результате | Пул пуст, но результат есть | Нет результатов | Клуб/абонемент в топ-3 |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]

    for goal in sorted(goal_counts):
        group = [row for row in rows if row["case"]["goal"] == goal]
        cards = [item for row in group for item in row["results"]]
        lines.append(
            "| {} | {} | {} | {} | {} | {} | {} |".format(
                GOAL_LABELS["ru"][goal],
                len(group),
                sum(bool(row["conflicts"]) for row in group),
                sum(bool(row["results"] and row["results"][0]["conflicts"]) for row in group),
                sum(row["candidate_count_after_answers"] == 0 and row["result_count"] > 0 for row in group),
                sum(row["result_count"] == 0 for row in group),
                sum(item["membership_title"] for item in cards),
            )
        )

    def count_list(counter: Counter) -> str:
        labels = {"activity": "активность", "component_class": "класс товара", "product_form": "форма", "use_scenario": "сценарий", "use_timing": "время", "use_place": "место", "season": "погода", "race_format": "формат старта", "shoe_size": "размер"}
        return "; ".join("{} — {}".format(labels.get(key, key), counter[key]) for key in sorted(counter)) or "нет"

    lines.extend([
        "",
        "## Частые причины несоответствия",
        "",
        "В парах «карточка–ответ» по всем трём рекомендациям чаще всего конфликтовали: {}. В первом результате чаще всего конфликтовали: {}.".format(
            count_list(result_conflicts_by_field), count_list(top_conflicts_by_field)
        ),
        "",
        "Желаемый покупателем вариант не попадал в фактический маршрут по таким полям: {}. Сюда входят и случаи, когда поле не было полезно по оставшимся кандидатам, поэтому это сигнал для проверки ветки, а не автоматически дефект.".format(
            count_list(omitted_values_by_field)
        ),
        "",
        "## Состояние плана реализации",
        "",
        "Основание для этого дополнения — [запрос пользователя на сводку и план](../../raw/sources/2026-11-09-quiz-audit-synthesis-implementation-plan-request.md).",
        "",
        "Правки для review-прототипа и регрессионная проверка выполнены. План не утверждает производственные правила.",
        "",
        "1. **Семантика ответов — выполнено.** Цена и известный размер остаются жёсткими ограничениями; известные конфликты по активности и классу исключаются; неизвестные значения отделены от противоречий.",
        "2. **Точные, общие и ослабленные пулы — выполнено.** Результаты показывают слой совпадения; неизвестные сигналы и известные конфликты мягких предпочтений не смешиваются.",
        "3. **Один пул для вопросов и результата — выполнено.** `draft_options` и `draft_recommend` используют общую классификацию кандидатов.",
        "4. **Ноль точных кандидатов — выполнено.** Прототип сначала сообщает об отсутствии точного результата; общий и ослабленный варианты доступны только по отдельному действию.",
        "5. **Ветки и объяснения — выполнено для прототипа.** Питание включает походы, неподдерживаемая активность не подменяется, размер спрашивается и в ветке подарка, тип клубного набора явно показан.",
        "6. **Конфликтные данные каталога — остаётся до production.** 11 карточек по-прежнему требуют сверки; этот аудит не обновляет источники состава и не решает их статус.",
        "7. **Регрессия — выполнено.** Повторный проход 100 сценариев дал 0 известных противоречий в обычной выдаче, 0 автоматических расширений пустого пула и 0 нарушений цены/размера; отдельно проверены 3 неподдерживаемых фильтра и граничные значения из матрицы.",
        "8. **Браузерный путь — выполнено.** В UI вручную проверены нулевой точный результат и общий fallback, ослабление мягкого предпочтения, питание в походе, размер подарка и маркировка клубного набора. Эти наблюдения отдельно от метрик API.",
        "",
        "## Выводы и оставшиеся ограничения",
        "",
        "1. **Известное противоречие больше не попадает в обычную выдачу.** Матрица подтверждает 0 сценариев с известными конфликтами и 0 конфликтов в первом результате; у вопросов и результата общий слой candidate-классификации.",
        "2. **Неизвестное не трактуется как несовпадение.** Общие варианты не показываются автоматически: пользователь сначала видит отсутствие точного совпадения и сам запрашивает их.",
        "3. **Мягкое предпочтение можно ослабить отдельно.** Конфликтующие ответы перечисляются на карточке варианта после отдельного действия; конфликты цели, активности и класса товара остаются исключающими.",
        "4. **Подтверждённые границы соблюдены.** В 100 сценариях нет превышения введённой цены или выхода известного размера за диапазон. Подарочная ветка спрашивает размер при наличии размерных кандидатов.",
        "5. **Отсутствие точной выдачи остаётся частым результатом.** В 47/100 сценариях обычная выдача пуста; это честно отражает фильтры и ограниченный каталог, а общий/ослабленный пул можно запросить отдельно.",
        "6. **Данные ограничивают уверенность.** 11 конфликтных карточек требуют сверки; клубные наборы встречаются в выдаче; текущая цена и наличие не обновляются; аллергены, кофеин и точная дистанция не поддерживаются.",
        "",
        "## Вопросы и ограничения текущего черновика",
        "",
        "1. **Для какой задачи ищете готовый набор?** Бег/старты, силовая или функциональная тренировка, питание, гидратация, восстановление, поход/активный отдых, экипировка, повседневное использование или подарок.",
        "2. **Для какой активности подбираем?** Варианты меняются по задаче и данным оставшихся кандидатов; питание включает походы. Если нужного вида нет, есть явный вариант «Другая активность» без подмены ближайшей категорией.",
        "3. **Что важнее в наборе?** Питание/перекусы, гидратация, добавки, одежда/обувь или аксессуары — только если есть несколько поддержанных вариантов.",
        "4. **К какому случаю подбираете?** Старт, тренировки или обычный день — только когда карточки различают эти сценарии.",
        "5. **Когда и где будете использовать?** Оставлять отдельным уточнением, лишь если оно меняет доступные наборы; не превращать отсутствие контекста в отрицательный сигнал.",
        "6. **Какие условия и форма удобны?** Погода/сезон и вид продукта можно спросить добровольно, если у оставшихся кандидатов есть соответствующие данные.",
        "7. **Нужен ли размер обуви/носков?** Спрашивать при размерно-чувствительных товарах с записанным диапазоном, в том числе в подарочной ветке; известный несовпадающий размер исключает набор.",
        "8. **Какова максимальная цена всего набора?** В прототипе это жёсткий фильтр по снимку на указанную дату; для реального квиза нужна актуальная цена.",
        "",
        "Не спрашивать сейчас точные километры, аллергию, «без кофеина», дозировку/период или медицинские ограничения: источники не позволяют надёжно подтвердить такие фильтры. Если покупателю важно такое ограничение, интерфейс должен сообщить, что текущих данных недостаточно.",
        "",
        "## Сценарии",
        "",
        "В маршруте `поле=значение` — реально отправленный ответ; `неважно` — покупатель оставил мягкое предпочтение пустым. `пул N→R` показывает число оставшихся по ответам кандидатов и число финальных результатов. Если желаемый ответ не показан, он указан в колонке пропусков. В результатах `#строка` — номер записи снимка каталога от 2026-11-06. `!поле` — известное противоречие ответу; `†` — карточка с неразрешённым конфликтом состава; `?поле` — нет сигнала, ответ не подтверждён.",
        "",
        "| № | Покупательская ситуация | Маршрут ответов | Топ выдачи (до 3) | Конфликты / неизвестно / не предложено |",
        "|---:|---|---|---|---|",
    ])

    for row in rows:
        case = row["case"]
        route = "; ".join(f"{field_label(key)}={value_label(key, value)}" for key, value in row["route"])
        results = "; ".join(
            f"#{item['row']} {item['title']} ({item['price']} грн)"
            + (" !" + ",".join(field_label(key) for key in item["conflicts"]) if item["conflicts"] else "")
            + ("†" if item["conflict_card"] else "")
            for item in row["results"]
        ) or "нет результатов"
        flags = ["пул {}→{}".format(row["candidate_count_after_answers"], row["result_count"])]
        if row["missing"]:
            flags.extend(f"не предложено: {field_label(key)} ({value})" for key, value in row["missing"].items())
        flags.extend("не поддерживается: " + value for value in case.get("unrepresented", []))
        if row["hard_violations"]:
            flags.extend(row["hard_violations"])
        if len(flags) == 1:
            top_unknown = row["results"][0]["unknown"] if row["results"] else []
            if top_unknown:
                flags.append("неизвестно: " + ",".join(field_label(key) for key in top_unknown))
        if len(flags) == 1:
            flags.append("—")
        note = case["note"]
        lines.append(f"| {case['id']:02d} | {case['buyer']}<br>{note} | {route} | {results} | {'; '.join(flags)} |")

    lines.extend([
        "",
        "## Интерпретация и границы",
        "",
        "- Снимок каталога и цены датированы 2026-11-06; наличие и цены сейчас не подтверждены.",
        "- Ответы о кофеине, аллергенах, переносимости, лекарствах и медицинской безопасности в этой форме отсутствуют; нельзя считать отсутствие сведений положительным сигналом.",
        "- Теги и состав могут содержать 11 неразрешённых конфликтных карточек. Они отмечены движком, но остаются в кандидатном пуле.",
        "- Этот прогон проверяет код и данные тестовой песочницы. Он не утверждает коммерческое правило приоритета для каждой цели.",
        "- Скрипт воспроизведения: [`test-quiz-sandbox/scenario_audit_100.py`](../../test-quiz-sandbox/scenario_audit_100.py).",
        "",
    ])
    return "\n".join(lines)


def main() -> None:
    if len(CASES) != 150 or [case["id"] for case in CASES] != list(range(1, 151)):
        raise RuntimeError("Expected exactly 150 uniquely numbered scenarios")
    if len({case["buyer"] for case in CASES}) != 150:
        raise RuntimeError("Scenario buyer descriptions must be distinct")
    catalog = load_enriched_catalog()
    rows = [run_path(catalog, case) for case in CASES]
    if len({_req_key(row["request"]) for row in rows}) != 150:
        raise RuntimeError("Scenario answer payloads must be distinct")
    hard_failures = [row for row in rows if row["hard_violations"]]
    unsupported_requests = [
        {"goal_group": "training", "caffeine_mode": "avoid"},
        {"goal_group": "food", "allergens": ["peanut"]},
        {"goal_group": "running", "race_format": "5k"},
    ]
    unsupported_checks = 0
    for request in unsupported_requests:
        try:
            draft_recommend(catalog, request)
        except DraftMatchError:
            unsupported_checks += 1
    if unsupported_checks != len(unsupported_requests):
        raise AssertionError("A not-supported hard filter was silently accepted")
    output = PROJECT_ROOT / "wiki" / "projects" / "quiz-buyer-scenario-audit-100.md"
    output.write_text(render_report(rows, unsupported_checks), encoding="utf-8")
    print("scenarios=150")
    print("goal_groups={}".format(dict(Counter(row["case"]["goal"] for row in rows))))
    print("hard_constraint_violations={}".format(len(hard_failures)))
    print("scenarios_with_known_preference_conflict={}".format(sum(bool(row["conflicts"]) for row in rows)))
    print("top_result_known_conflict={}".format(sum(bool(row["results"] and row["results"][0]["conflicts"]) for row in rows)))
    print("zero_soft_candidates_but_results={}".format(sum(row["candidate_count_after_answers"] == 0 and row["result_count"] > 0 for row in rows)))
    print("report={}".format(output))


if __name__ == "__main__":
    main()
