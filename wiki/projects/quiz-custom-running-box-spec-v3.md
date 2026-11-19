---
schema_version: 2
id: "document.quiz-custom-running-box-spec-v3"
type: "document"
title: "Специфікація та архітектура Custom Running Box Builder (SDD & TDD, v3.0)"
description: "Технічна специфікація та архітектура динамічного конфігуратора стартового боксу бігуна за стандартом Superpowers Spec-Driven Development: 4 слоти, 458 активних SKU з бази OpenCart, 7 запитань, TDD-тести та протокол інтеграції з кошиком."
tags: ["project:quiz-product-set-generator", "topic:quiz", "topic:architecture", "topic:running", "topic:spec-driven-development", "workflow:specification", "language:uk"]
source: {"raw_path": "docs/superpowers/specs/2026-11-16-running-custom-box-design.md"}
dates: {"added_at": "2026-11-16T14:50:00+02:00", "updated_at": "2026-11-16T14:50:00+02:00"}
relations: [{"type": "applies-to", "target": "project.quiz-product-set-generator"}, {"type": "references", "target": "document.quiz-engine-technical-documentation"}]
aliases: ["Custom Running Box Spec", "Конфігуратор боксу бігуна ТЗ", "Running Box SDD Spec"]
status: "active"
---

# Специфікація: Конфігуратор стартового боксу бігуна (Race Expert Custom Runner Box)

## 1. Контекст та еволюція архітектури
Попередня версія рекомендаційного рушія базувалася на статичних готових наборах з категорії «За потребами». 
Для підвищення конверсії, середнього чека та розпродажу високомаржинальних залишків власного бренду (понад 5 000 поясних сумок *Race Expert Slim Belt/Waist Pack* та тисячі пар шкарпеток *RE Ultra*) розроблено концепцію **«Динамічного стартового боксу з чекбоксами»**.

## 2. Інвентаризація, підключення бази та 3-рівнева фільтрація каталогу
* **Підключення до MySQL:** TLS 1.3 сокет до бази `raceexpertcomua`, доступ тільки для читання (`raceexpert_readonly`). База — єдине джерело залишків (`quantity > 0`) та цін.
* **Кешування:** Швидка генерація боксу (15мс) за рахунок щоденного оновлення локального `running_catalog.json` без навантаження на MySQL під час проходження квізу.
* **3-рівнева фільтрація спортивних товарів:**
  1. *Профільні категорії:* Гелі, електроліти, пояси для бігу, мармелад, шкарпетки, спортивна косметика.
  2. *Семантичні маркери:* Пошук ключів «для бігу», «марафон», «soft flask», «salt caps», «від натирань».
  3. *Anti-keywords (чорний список):* Блокування гейнерів для набору маси, трибулусу/бустерів тестостерону, банок понад 4 500 грн / від 3 кг.
* **Паспорт метаданих (15 полів):** `product_id`, `sku`, `name`, `brand`, `price`, `quantity`, `image`, `url`, `slot`, `sub_type`, `price_tier`, `caffeine`, `stomach_gentle`, `distances`, `is_vegan`.

Із загальної бази OpenCart (5 029 товарів) скриптом `scripts/build_running_catalog.py` відфільтровано **458 активних товарів у наявності (`quantity > 0`)**, збережених у `running_catalog.json`:
* **`SLOT_ENERGY` (140 SKU):** Вуглеводні гелі (SiS, Maurten, GU, Nutrend, Sponser), жувальний мармелад (PF 30 Chew), енергетичні вафлі, порошкові мікси, сублімати *ЇДЛО*.
* **`SLOT_HYDRATION` (74 SKU):** Ізотоніки, шипучі розчинні електроліти, сольові капсули (*SaltStick, Sponser Salt Caps*).
* **`SLOT_GEAR` (64 SKU):** Поясні сумки для бігу, пояси для номера та гелів, м'які фляги *PF&H Soft Flask 500 мл*, шкарпетки *RE Ultra*.
* **`SLOT_CARE_RECOVERY` (180 SKU):** Креми від натирання *Chamois Butt'r*, рідкий магній, хондропротектори *Nutrend Flexit*, рекавери-шейки *SiS REGO*, бета-аланін.

### Розподіл за ціновими рівнями:
* **Економ:** 45 товарів (Nutrend, Sporter, Bodyperson Labs)
* **Оптимальний:** 144 товари (SiS, Sponser, PowerBar, Race Expert)
* **PRO / Еліта:** 269 товарів (Maurten, Precision Fuel & Hydration, SaltStick, Chamois Butt'r)

## 3. Сценарій опитування (7 запитань)
1. **Дистанція:** 10 км | 21.1 км | 42.2 км | Трейл (гори).
2. **Темп / Мета:** На рекорд | У стабільному темпі | Головне — фініш.
3. **Погода:** Спека (+20°C+) ➔ *тригер солей*; Помірно (+10..+19°C); Прохолода (до +10°C).
4. **Шлунок (ЖКТ):** Чутливий/нудить від солодкого ➔ *пріоритет гідрогелям Maurten та твердому мармеладу*; Звичайний; Веган.
5. **Кофеїн:** Потрібен буст на фініш ➔ *1 гель із кофеїном 75-150 мг на кінець дистанції*; Суворо без кофеїну.
6. **Слабкі місця (мультиселект):** Судоми (*солі + магній*) | Натирання шкіри (*крем Chamois Butt'r*) | Суглоби/коліна (*Flexit*).
7. **Екіп та Бюджет:** Вибір речей (пояс, фляга, шкарпетки) + бажана цінова категорія (Економ / Оптимум / PRO).

## 4. Superpowers SDD & TDD Верифікація
Модуль підбору реалізовано у файлі `runner_box_engine.py` та верифіковано 100% зеленими TDD-тестами:
* `test_runner_box_engine.py`:
  * `test_zero_caffeine_guarantee()` — 100% виключення кофеїну за вимогою клієнта.
  * `test_caffeine_boost_included_on_half_marathon()` — гарантія бусту на фініш.
  * `test_hot_weather_salt_injection()` — обов'язкове додавання солей у спеку.
* `test_real_catalog_validation.py`:
  * Перевірка цілісності всіх 458 реальних SKU, валідності цін та позитивних залишків.

## 5. Рішення за результатами Builder Check
1. **Інтеграція з кошиком:** 
   * У production квіз розташовується на самому домені (`raceexpert.com.ua/quiz/`) — запити до `checkout/cart/add` є *same-origin* і зберігають сесію без CORS-блокувань.
   * Для зовнішнього демо на VPS застосовується демонстраційна симуляція та прямі лінки.
2. **Розміри шкарпеток:** Інлайн-селектор розміру `[ 35-37 | 38-40 | 40-42 | 43-45 ]` прямо в картці фінального боксу (мапиться на product_id 7451–7454).
3. **Failure Policy:** При відмові одного товару процес зупиняється з підсвічуванням і пропозицією заміни (без мовчазного оформлення напівпорожнього замовлення).
4. **Веган-фільтр:** Блокує тваринний колаген (*Flexit*) та желатин, залишаючи рослинні мальтодекстринові гелі (*SiS, Maurten*).

## 6. Ключові файли артефактів
* Повна дизайн-специфікація: `docs/superpowers/specs/2026-11-16-running-custom-box-design.md`
* Технічне завдання: `spec_running_custom_box.md`
* План впровадження: `docs/superpowers/plans/2026-11-16-running-custom-box-builder.md`
* База каталогу: `running_catalog.json`
* Рушій: `runner_box_engine.py`
