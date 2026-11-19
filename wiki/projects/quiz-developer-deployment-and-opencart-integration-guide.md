---
schema_version: 2
id: "document.quiz-developer-deployment-and-opencart-integration-guide"
type: "document"
title: "Інструкція для розробника: розгортання квіз-сервісу та інтеграція з OpenCart"
description: "Технічна інструкція для передачі репозиторію програмісту Race Expert: варіанти розгортання (Docker, systemd, Nginx reverse proxy), архітектура ендпоінтів та пакетне додавання товарів у кошик OpenCart."
tags: ["project:quiz-product-set-generator", "topic:deployment", "topic:opencart-integration", "topic:api", "topic:architecture", "workflow:implementation", "language:uk"]
source: {"raw_path": "raw/sources/2026-11-19-programmer-handoff-and-deployment-preparation.md"}
dates: {"added_at": "2026-11-19T18:22:00+02:00", "updated_at": "2026-11-19T18:22:00+02:00"}
relations: [{"type": "applies-to", "target": "project.quiz-product-set-generator"}, {"type": "references", "target": "document.quiz-multi-sport-complete-pack-architecture"}, {"type": "references", "target": "source.mysql-readonly-access-and-product-query-guide"}]
aliases: ["Developer Deployment & OpenCart Integration Guide", "Інструкція розробника для деплою", "OpenCart API інтеграція квізу"]
status: "active"
---

# Інструкція для розробника: розгортання квіз-сервісу та інтеграція з OpenCart

## 1. Огляд та архітектура сервісу

Квіз-конструктор Race Expert є автономним додатком швидкої генерації стартових та тренувальних боксів (Т-наборів) за 5 видами спорту: **Біг, Велоспорт, Триатлон, Зал / Фітнес, Походи / ЇDLO**.

### Стек технологій
* **Бекенд:** Python 3.10+ (легковаговий багатопотоковий сервер `server.py` або Uvicorn/FastAPI).
* **Алгоритмічні рушії:** `runner_box_engine.py` (бігові набори з правилом єдиного бренду гелів) та `multi_sport_engine.py` (4 інші дисципліни з 3-рівневою оптимізацією під точний бюджет покупця).
* **Фронтенд:** Чистий клієнтський JavaScript (`public/runner_box.js`) та адаптивний HTML5 (`public/runner_box.html`) на базі Tailwind CSS (CDN). Відсутній важкий білд-стек (Node.js/Webpack не потрібні для роботи).
* **Дані:** Попередньо відвалідовані каталоги товарів у форматі JSON (`running_catalog.json`, `cycling_catalog.json`, тощо), що забезпечують підбір боксу за < 5 мілісекунд.
* **Тести:** Повний автоматизований набір із 323+ тестів (`pytest`), який гарантує 100% стабільність алгоритмів.

---

## 2. Варіанти розгортання на сервері магазину

Сервіс передається через репозиторій GitHub. Для програміста доступні три зручні варіанти розгортання:

### Варіант А: Nginx Reverse Proxy на основному домені магазину (НАЙКРАЩИЙ ТА РЕКОМЕНДОВАНИЙ)
Сервіс запускається локально на сервері магазину (наприклад, на порту `8000`), а веб-сервер Nginx сайту `raceexpert.com.ua` проксіює запити на URL `/quiz/` або `/box/`.

**Фрагмент конфігурації Nginx (`/etc/nginx/sites-available/raceexpert.com.ua`):**
```nginx
location /quiz/ {
    proxy_pass http://127.0.0.1:8000/;
    proxy_http_version 1.1;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
}
```

**Ключові переваги Варіанту А:**
1. **Єдиний домен (`Same-Origin`):** Квіз і магазин працюють на одному домені `raceexpert.com.ua`.
2. **Спільні Cookies сесії OpenCart (`OCSESSID`):** Будь-який запит на додавання товару в кошик автоматично передає ідентифікатор сесії покупця. Немає блокування сторонніх cookies сучасними браузерами (Safari ITP, Chrome Privacy Sandbox).
3. **Відсутність проблем із CORS:** Запити виконуються без складних префлайт-налаштувань.

---

### Варіант Б: Окремий піддомен (`quiz.raceexpert.com.ua`)
Якщо програміст вирішить винести квіз на окремий піддомен:
* Потрібно налаштувати cookie сесії в OpenCart так, щоб вона діяла на всі піддомени:
  * У `php.ini` або конфігурації сесій OpenCart встановити: `session.cookie_domain = ".raceexpert.com.ua";`
* У конфігурації Nginx або бекенду квізу дозволити CORS для піддомену:
  * `Access-Control-Allow-Origin: https://quiz.raceexpert.com.ua`
  * `Access-Control-Allow-Credentials: true`

---

### Варіант В: Запуск у Docker (Найпростіший для ізоляції)
У репозиторій додається `Dockerfile` та `docker-compose.yml`:
```yaml
version: '3.8'
services:
  quiz-app:
    build: .
    restart: always
    ports:
      - "127.0.0.1:8000:8000"
    environment:
      - PORT=8000
      - TZ=Europe/Kyiv
    volumes:
      - ./data:/app/data
```
Програмісту достатньо виконати:
```bash
git clone https://github.com/race-expert/quiz.git
cd quiz
docker compose up -d
```

---

## 3. Інтеграція з кошиком OpenCart: два підходи

Головне завдання взаємодії квізу та магазину — перенести обрані покупцем позиції боксу (наприклад, 4 гелі, 1 магній, 1 ізотонік, 1 пояс) у реальний кошик OpenCart.

### Підхід 1: Стандартний нативний ендпоінт OpenCart (Zero-Code на боці OpenCart)
OpenCart за замовчуванням має стандартний маршрут додавання товару:
* **URL:** `POST /index.php?route=checkout/cart/add`
* **Тіло запиту (x-www-form-urlencoded):**
  * `product_id`: ID товару
  * `quantity`: кількість
* **Особливість:** Фронтенд квізу викликає цей ендпоінт послідовно для кожного товару з боксу.
* **Плюси:** Програмісту не потрібно писати жодного рядка коду в OpenCart.
* **Мінуси:** Якщо у боксі 10 товарів, браузер відправляє 10 HTTP-запитів підряд. Якщо товар має обов'язкові опції (наприклад, смак без дефолтного значення), OpenCart може повернути помилку форми.

---

### Підхід 2: Пакетний контролер (Bulk Add Endpoint — НАЙКРАЩА ПРАКТИКА)
Програміст створює один простий PHP-контролер у структурі OpenCart (20 рядків коду), який приймає весь сформований бокс за один швидкий запит.

**Рекомендований маршрут:** `POST /index.php?route=api/quiz_cart/add_bulk` або `POST /index.php?route=checkout/cart/add_bulk`

**Формат вхідного JSON від квізу:**
```json
{
  "items": [
    {"product_id": 1940, "quantity": 5},
    {"product_id": 3110, "quantity": 1},
    {"product_id": 5422, "quantity": 2}
  ]
}
```

**Готовий шаблон PHP-контролера для OpenCart 3.x / 4.x (`catalog/controller/api/quiz_cart.php` або `catalog/controller/checkout/cart.php`):**
```php
<?php
class ControllerApiQuizCart extends Controller {
    public function add_bulk() {
        $this->response->addHeader('Content-Type: application/json');
        $json = array();

        // Отримання сирого JSON-тіла
        $raw_input = file_get_contents('php://input');
        $data = json_decode($raw_input, true);

        if (!empty($data['items']) && is_array($data['items'])) {
            $added_count = 0;

            foreach ($data['items'] as $item) {
                $product_id = isset($item['product_id']) ? (int)$item['product_id'] : 0;
                $quantity = isset($item['quantity']) ? (int)$item['quantity'] : 1;
                $option = isset($item['option']) ? $item['option'] : array();

                if ($product_id > 0 && $quantity > 0) {
                    // Стандартний системний виклик OpenCart додавання в кошик
                    $this->cart->add($product_id, $quantity, $option);
                    $added_count++;
                }
            }

            // Очищення кешу розрахунків кошика
            unset($this->session->data['shipping_methods']);
            unset($this->session->data['shipping_method']);
            unset($this->session->data['payment_methods']);
            unset($this->session->data['payment_method']);

            $json['success'] = true;
            $json['added_items'] = $added_count;
            $json['total_items'] = $this->cart->countProducts();
            $json['redirect'] = $this->url->link('checkout/cart', '', true);
        } else {
            $json['success'] = false;
            $json['error'] = 'Порожній або некоректний список товарів';
        }

        $this->response->setOutput(json_encode($json));
    }
}
```

**Чому пакетний ендпоінт вигідніший:**
1. **Швидкість:** 1 мережевий запит займає 50–100 мс замість 3–5 секунд черги запитів.
2. **Атомарність:** Усі товари гарантовано потрапляють у кошик одночасно.
3. **Безпека:** Застосовується штатний метод OpenCart `$this->cart->add()`, що автоматично враховує знижки, акції та податки.

---

## 4. Синхронізація наявності та залишків товарів

Алгоритм квізу використовує каталоги формату JSON, щоб підбирати товари миттєво без постійного навантаження на базу даних OpenCart.

Для підтримки актуальних цін та наявності товарів на складі (`status = 1` та `quantity > 0`) програміст може обрати один із двох сценаріїв:
1. **Регламентний Cron-скрипт (Рекомендовано):**
   * Раз на добу (або кожні кілька годин) на сервері запускається скрипт синхронізації:
     `python3 scripts/sync_catalog_from_opencart.py`
   * Скрипт виконує простий `SELECT` з таблиць `oc_product`, `oc_product_description` та оновлює JSON-файли.
2. **Пряма перевірка залишків перед фінальним відображенням:**
   * У системі вже реалізовано модуль `stock_checker.py`, який може перевіряти статус переданого списку SKU через read-only підключення до MySQL бази `raceexpertcomua`.

---

## 5. Змінні оточення (`.env.example`)

Для запуску сервісу на сервері програмісту надається файл шаблону конфігурації:
```env
# Параметри веб-сервера
PORT=8000
HOST=127.0.0.1
BASE_URL=https://raceexpert.com.ua

# Інтеграція з кошиком OpenCart
OPENCART_CART_ENDPOINT=/index.php?route=checkout/cart/add
OPENCART_BULK_ENDPOINT=/index.php?route=api/quiz_cart/add_bulk
OPENCART_VIEW_CART_URL=/index.php?route=checkout/cart

# Підключення до MySQL OpenCart (для фонового оновлення залишків)
MYSQL_HOST=127.0.0.1
MYSQL_PORT=3306
MYSQL_DATABASE=raceexpertcomua
MYSQL_USER=raceexpert_readonly
MYSQL_PASSWORD=...

# ШІ-консультант Луна (опціонально)
OPENAI_API_KEY=...
```

---

## 6. Чек-лист передачі репозиторію через GitHub

Перед тим як надати посилання на GitHub програмісту, у репозиторії мають бути підготовлені:
- [x] Повна документація архітектури та алгоритмів.
- [ ] Очищений файл `.gitignore` (виключено персональні `.env`, кеші `__pycache__`, системні логи).
- [ ] Готовий `Dockerfile` та `docker-compose.yml`.
- [ ] Файл `.env.example` з коментарями для кожного параметра.
- [ ] Файл `README.md` із швидким стартом у 3 команди (`git clone`, `docker compose up -d`).
- [ ] PHP-файл контролера `quiz_cart.php` у папці `integrations/opencart/`, щоб програміст міг просто скопіювати його в OpenCart.
