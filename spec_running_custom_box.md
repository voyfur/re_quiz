# Технічна специфікація та план впровадження: Конфігуратор стартового боксу бігуна (Race Expert Custom Runner Box)

**Стандарт проектування:** Superpowers Engineering Architecture (TDD, Formal Schemas, Defensive Failure Modes, Step-by-Step Verification)  
**Версія:** 3.0-PROD  
**Статус:** Затверджено до реалізації  
**Каталог:** 458 верифікованих активних SKU з живої бази OpenCart (`running_catalog.json`)

---

## 1. Архітектурне бачення та межі системи (System Boundaries)

### 1.1. Проблема та рішення
* **Проблема:** Покупець ускладнюється вибором серед сотень розрізнених товарів спортивного харчування та екіпірування. Статичні набори не враховують індивідуальні проблеми (судоми, чутливий шлунок, наявність власного екіпірування).
* **Рішення:** Детермінований алгоритмічний конфігуратор, що формує персоналізований **«Стартовий бокс» із 4 слотів** на основі відповідей на 7 запитань, з можливістю для клієнта динамічно вимикати/вмикати позиції чекбоксами перед покупкою в один клік.

### 1.2. Інваріанти системи (System Invariants)
1. **Нульова толерантність до відсутності:** До рекомендацій допускаються **тільки** товари зі статусом `status = 1` та залишком `quantity > 0`.
2. **Caffeine Safety Guardrail:** Якщо користувач обирає «Суворо без кофеїну», система за жодних умов не включає до боксу стимулятори (кофеїн, гуарана).
3. **Price Floor & Tier Sanity:** Товари підбираються строго у рамках обраного цінового рівня (`economy`, `standard`, `premium`) або з явним маркуванням доцільності апсейлу.
4. **Idempotent Multi-Add:** Додавання пачки товарів до кошика OpenCart виконується послідовною чергою з верифікацією кожної відповіді сервера перед перенаправленням на чек-аут.

---

## 2. Підключення до бази OpenCart та 3-рівнева ідентифікація бігових товарів

### 2.1. Архітектура бази даних та протокол синхронізації
* **Підключення:** Скрипт синхронізації підключається до бази даних магазину OpenCart (`raceexpertcomua`) через захищений TLS 1.3 сокет під користувачем з правами **виключно на читання** (`raceexpert_readonly`). Змінити або видалити дані магазину неможливо.
* **Роль бази даних:** База виступає єдиним джерелом правди (Single Source of Truth) для двох речей:
  1. *Актуальні залишки:* квіз рекомендує лише товари з `quantity > 0` та `status = 1`. Якщо товар розкупили, він миттєво зникає з підбору.
  2. *Живі ціни:* при зміні цін на сайті ціни в квізі оновлюються автоматично.
* **Кешування (15ms затримка замість навантаження на MySQL):** Квіз не виконує важких SQL-запитів на кожен клік клієнта. Замість цього скрипт `scripts/build_running_catalog.py` регулярно перезбирає плоский JSON-каталог `running_catalog.json`. Завдяки цьому рекомендації генеруються за 15 мілісекунд, не навантажуючи сервер магазину.

### 2.2. Як система ідентифікує, що товар відноситься до спорту та бігу (3 рівні)
В OpenCart немає окремої папки «Все для бігу». Скрипт класифікує каталог через 3 фільтри:
1. **Рівень 1 (Профільні категорії циклічного спорту):** Товари вивантажуються виключно з категорій бігового та витривалого профілю: *«Гелі енергетичні»*, *«Електроліти (гідратація)»*, *«Пояси, сумки та чохли для бігу»*, *«Мармеладні батончики»*, *«Шкарпетки та компресія»*, *«Спортивна косметика»*. Гелі, сольові капсули та м'які фляги — це 100% циклічний спорт, бодібілдери та фітнес-відвідувачі їх не використовують.
2. **Рівень 2 (Семантичні маркери бігу в назвах):** Скрипт шукає маркери: *«для бігу»*, *«для марафону»*, *«soft flask»*, *«salt caps»*, *«re ultra»*, *«chamois butt'r»*, *«від натирань»*.
3. **Рівень 3 (Anti-keywords — чорний список не-бігових товарів):** Алгоритм жорстко блокує силовий спорт та фітнес:
   * Гейнери для набору маси (`gainer`, `big mass`).
   * Бустери тестостерону та трибулус (`tribulus`, `t-100`, `zmb`).
   * Оптові банки спортивного харчування понад 4 500 грн або вагою від 3 кг.
   * Господарські дрібниці, шеврони та нецільовий інвентар.

### 2.3. Повний паспорт метаданих товару (Схема полів)
Кожен із 458 допущених товарів зберігає повний набір із 15 атрибутів:
* **Базові поля OpenCart:** `product_id` (ID товару), `sku` (артикул), `name` (назва), `brand` (бренд), `price` (актуальна ціна), `quantity` (залишок > 0), `image` (URL фото), `url` (посилання на сайт).
* **Спеціальні спортивні метадані квізу:**
  * `slot`: `energy` | `hydration` | `gear` | `care_recovery` (до якого з 4 блоків боксу належить)
  * `sub_type`: `gel`, `chew`, `waffle`, `salt_caps`, `isotonic`, `running_belt`, `soft_flask`, `running_socks`, `anti_chafe`, `magnesium`, `joint_care`
  * `price_tier`: `economy` | `standard` | `premium` (цінова категорія)
  * `caffeine`: `true` | `false` (захист від кофеїну за бажанням користувача)
  * `stomach_gentle`: `true` | `false` (для чутливого шлунку — гідрогелі, желейки без кислоти)
  * `distances`: `["10k", "21k", "42k", "trail"]` (сумісність із забігами)
  * `is_vegan`: `true` | `false` (рослинний склад без тваринного колагену та желатину)

---

## 3. Формальні контракти даних (JSON Schemas)

### 2.1. Схема вхідних відповідей користувача (`QuizUserInput`)
```typescript
interface QuizUserInput {
  distance: "10k" | "21k" | "42k" | "trail";
  pace_target: "record" | "steady" | "finish";
  weather: "hot" | "moderate" | "cold";
  stomach_type: "sensitive" | "normal" | "vegan";
  caffeine_preference: "boost" | "none";
  body_concerns: Array<"cramps" | "chafing" | "joints">;
  gear_needed: Array<"belt" | "flask" | "socks">;
  price_tier: "economy" | "standard" | "premium";
}
```

### 2.2. Схема товару каталогу (`RunningCatalogItem`)
```typescript
interface RunningCatalogItem {
  product_id: number;
  sku: string;
  name: string;
  brand: string;
  price: number;
  quantity: number;
  image: string;
  url: string;
  slot: "energy" | "hydration" | "gear" | "care_recovery";
  sub_type: 
    | "gel" | "chew" | "waffle" | "trail_food"
    | "isotonic" | "salt_caps"
    | "running_belt" | "soft_flask" | "running_socks" | "headwear"
    | "anti_chafe" | "magnesium" | "joint_care" | "recovery_drink" | "endurance_booster";
  price_tier: "economy" | "standard" | "premium";
  caffeine: boolean;
  stomach_gentle: boolean;
  distances: Array<"10k" | "21k" | "42k" | "trail">;
}
```

### 2.3. Схема вихідного боксу (`GeneratedRunnerBox`)
```typescript
interface BoxSlotItem {
  product: RunningCatalogItem;
  quantity_recommended: number;
  timing_instruction: string; // Наприклад: "На 14-му км" або "За 15 хв до старту"
  checked_by_default: boolean;
  reason_badge: string;       // Наприклад: "Захист від судом" або "Фінішний ривок"
}

interface GeneratedRunnerBox {
  distance_label: string;
  total_base_price: number;
  slots: {
    energy: BoxSlotItem[];
    hydration: BoxSlotItem[];
    gear: BoxSlotItem[];
    care_recovery: BoxSlotItem[];
  };
}
```

---

## 3. Матриця рішень та алгоритм збірки боксу (Decision Engine)

### 3.1. Слот 1: Енергія (`SLOT_ENERGY`)
* **Розрахунок кількості порцій:**
  * `10k`: 1 порція (при темпі `record` або `steady` — прийом за 15 хв до старту або на 6 км).
  * `21k`: 3 порції гелів (прийом на 7 км, 14 км, 18 км). Якщо `stomach_type === 'sensitive'`, 1 гель замінюється на пачку желейок `chew` або `waffle`.
  * `42k`: 6 порцій вуглеводів (кожні 35-40 хв) = 4-5 гелів + 1-2 жувальні мармелади.
  * `trail`: 4 гелі + 2 вафлі + 1 порція сублімованої їжі (*ЇДЛО*).
* **Правило кофеїну:**
  * Якщо `caffeine_preference === 'boost'`: останній гель на дистанції (18 км для півмарафону, 28 та 35 км для марафону) підбирається з прапорцем `caffeine: true` (75–150 мг).
  * Якщо `caffeine_preference === 'none'`: суворий фільтр `caffeine: false`.
* **Правило шлунку:**
  * Якщо `stomach_type === 'sensitive'`: пріоритет віддається `stomach_gentle: true` (Maurten Hydrogel або желейні цукерки без лимонної кислоти).

### 3.2. Слот 2: Гідратація та солі (`SLOT_HYDRATION`)
* Якщо `weather === 'hot'` АБО `body_concerns.includes('cramps')`:
  * **Обов'язкове включення:** `sub_type: 'salt_caps'` (*Sponser Salt Caps* або *SaltStick*).
* Загальний випадок:
  * 1 упаковка розчинного ізотоніка/електролітів у шипучих таблетках відповідного `price_tier`.

### 3.3. Слот 3: Екіпірування (`SLOT_GEAR`)
Підбір керується масивом `gear_needed`:
* Якщо `'belt'` увімкнено: додається `running_belt` (*Race Expert Slim Belt* за 250 грн або *RE пояс для номера та гелів* за 375 грн).
* Якщо `'flask'` увімкнено: додається `soft_flask` (*PF&H Soft Flask 500 мл*).
* Якщо `'socks'` увімкнено: додаються компресійні шкарпетки *RE Ultra Socks* (405 грн).

### 3.4. Слот 4: Захист та відновлення (`SLOT_CARE_RECOVERY`)
Керується масивом проблемних зон `body_concerns`:
* Якщо `body_concerns.includes('chafing')`:
  * Додається `sub_type: 'anti_chafe'` (*Chamois Butt'r* порційний/тюбик).
* Якщо `body_concerns.includes('cramps')`:
  * Додається ампула рідкого магнію `sub_type: 'magnesium'` (*Sponser Magnesium 375* або *PureGold*).
* Якщо `body_concerns.includes('joints')`:
  * Додається `sub_type: 'joint_care'` (*Nutrend Flexit* колаген/хондропротектор).
* Якщо `distance === '42k' || distance === 'trail'`:
  * Рекомендується відновлювальний білково-вуглеводний шейк `recovery_drink` (*SiS REGO Rapid Recovery*).

---

## 4. TDD-стратегія верифікації (Test-Driven Verification Suite)

Для гарантії бездоганної роботи двигуна розробляється набір модульних тестів (на базі `pytest`), які повинні виконуватися перед будь-яким релізом:

```python
# test_running_box_engine.py

def test_zero_caffeine_guarantee():
    """Перевірка: якщо клієнт обрав 'none', у жодному слоті немає кофеїну."""
    inputs = {
        "distance": "42k",
        "caffeine_preference": "none",
        "price_tier": "standard",
        "stomach_type": "normal",
        "weather": "moderate",
        "body_concerns": [],
        "gear_needed": []
    }
    box = generate_runner_box(inputs)
    for slot_name, items in box["slots"].items():
        for item in items:
            assert item["product"]["caffeine"] is False, f"Виявлено кофеїн у {item['product']['name']}"

def test_hot_weather_salt_injection():
    """Перевірка: спека обов'язково викликає сольові капсули."""
    inputs = {
        "distance": "21k",
        "weather": "hot",
        "body_concerns": [],
        "caffeine_preference": "boost",
        "price_tier": "economy",
        "gear_needed": []
    }
    box = generate_runner_box(inputs)
    sub_types = [item["product"]["sub_type"] for item in box["slots"]["hydration"]]
    assert "salt_caps" in sub_types, "Спека не викликала сольові капсули у слоті гідратації"

def test_stock_quantity_positive():
    """Перевірка: усі запропоновані товари мають залишок більше нуля."""
    inputs = {"distance": "42k", "weather": "hot", "body_concerns": ["cramps", "chafing"], "gear_needed": ["belt", "flask"]}
    box = generate_runner_box(inputs)
    for slot_name, items in box["slots"].items():
        for item in items:
            assert item["product"]["quantity"] > 0, f"Товар {item['product']['name']} має нульовий залишок"

def test_price_tier_adherence():
    """Перевірка: економ-запит не підтягує товари з преміум-сегменту без явної причини."""
    inputs = {"distance": "10k", "price_tier": "economy", "caffeine_preference": "none"}
    box = generate_runner_box(inputs)
    for item in box["slots"]["energy"]:
        assert item["product"]["price_tier"] in ["economy", "standard"]
```

---

## 5. Протокол інтеграції з кошиком OpenCart (Resilient Checkout Integration)

### 5.1. Послідовна черга запитів із повторними спробами (Retry Logic)
Додавання декількох товарів здійснюється послідовно через вбудований у браузер черговий механізм:

```javascript
async function addProductWithRetry(productId, quantity, maxRetries = 2) {
    for (let attempt = 0; attempt <= maxRetries; attempt++) {
        try {
            const formData = new URLSearchParams();
            formData.append('product_id', productId);
            formData.append('quantity', quantity);

            const res = await fetch('https://raceexpert.com.ua/index.php?route=checkout/cart/add', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                    'X-Requested-With': 'XMLHttpRequest'
                },
                body: formData
            });

            const json = await res.json();
            if (json.success) return true;
            if (json.error && json.error.option) {
                console.warn(`Товар ID ${productId} вимагає вибору опції (смак/розмір):`, json.error.option);
                return false;
            }
        } catch (e) {
            if (attempt === maxRetries) throw e;
            await new Promise(r => setTimeout(r, 400)); // Затримка перед повтором
        }
    }
    return false;
}
```

### 5.2. Fallback для опціональних товарів (Розміри / Смаки)
Якщо у товару є обов'язкова опція вибору смаку/розміру, квіз підставляє пряме посилання «Оберіть смак на сторінці товару» або дефолтний `product_option_value_id`, щоб уникнути помилки `error_option_required`.

---

## 6. Поетапний план реалізації (Superpowers Work Breakdown Structure)

```
[ Фаза 1: Модуль підбору (Engine Core) ] 
        ↓  (Верифікація через unit-тести)
[ Фаза 2: Інтерактивний UI 7 кроків + Екран боксу ] 
        ↓  (UI перевірка + реактивний перерахунок чекбоксів)
[ Фаза 3: Інтеграція з кошиком OpenCart ] 
        ↓  (E2E тест оформлення замовлення)
[ Фаза 4: Фінальний реліз та деплой на VPS ]
```

### Фаза 1. Ядро алгоритму підбору (`runner_box_engine.py` / `engine.js`)
* **Задача 1.1:** Реалізувати функцію `generateRunnerBox(inputs, catalog)` із точною реалізацією правил розділу 3.
* **Задача 1.2:** Написати та прогнати повний набір TDD-тестів (`test_runner_box_engine.py`), досягти 100% проходження перевірок безпеки.

### Фаза 2. Інтерфейс користувача (7 кроків та сторінка боксу)
* **Задача 2.1:** Створити адаптивний компонент опитування (Dark Theme, Tailwind CSS, плавні переходи без перезавантаження сторінки).
* **Задача 2.2:** Реалізувати екран готового боксу:
  * Групування по 4 слотах.
  * Інтерактивні чекбокси з миттєвим перерахунком суми в реальному часі.
  * Інструкція прийому (таймлайн по кілометрах під кожним товаром).

### Фаза 3. Зв'язок із кошиком магазину
* **Задача 3.1:** Реалізувати чергу `addCustomBoxToCart` із відображенням стану завантаження на кнопці.
* **Задача 3.2:** Перевірити поведінку кошика у мобільних браузерах (iOS Safari, Android Chrome).

### Фаза 4. Деплой та синхронізація
* **Задача 4.1:** Розгорнути оновлений квіз на бойовому сервері `185.25.119.96`.
* **Задача 4.2:** Налаштувати нічний запуск `build_running_catalog.py` для підтримки актуальності цін та залишків без участі людини.
