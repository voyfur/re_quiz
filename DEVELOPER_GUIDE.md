# 📘 Посібник розробника: розгортання квіз-сервісу Race Expert та інтеграція з OpenCart

Цей документ містить повну технічну інструкцію для програміста інтернет-магазину [Race Expert](https://raceexpert.com.ua) щодо розгортання сервісу підбору боксів, налаштування Nginx reverse proxy, конфігурації оточення та підключення пакетного додавання товарів у кошик OpenCart.

---

## 📌 Зміст
1. [Архітектура сервісу](#1-архітектура-сервісу)
2. [Швидкий старт (Docker Compose / systemd)](#2-швидкий-старт)
3. [Налаштування Nginx Reverse Proxy](#3-налаштування-nginx-reverse-proxy)
4. [Інтеграція з кошиком OpenCart (Контролер `quiz_cart.php`)](#4-інтеграція-з-кошиком-opencart)
5. [Реєстр API Endpoints та приклади curl](#5-реєстр-api-endpoints-та-приклади-curl)
6. [Змінні оточення та ключі доступу (`.env`)](#6-змінні-оточення-та-ключі-доступу-env)
7. [Каталоги товарів та оновлення залишків](#7-каталоги-товарів-та-оновлення-залишків)
8. [Чек-лист перевірки запуску (Smoke Test)](#8-чек-лист-перевірки-запуску-smoke-test)

---

## 1. Архітектура сервісу

Квіз-конструктор є автономним додатком на базі **Python 3.12** без важких сторонніх рантайм-бібліотек (використовує стандартний високопродуктивний багатопотоковий `ThreadingHTTPServer`).

### Ключові принципи:
* **Миттєвий розрахунок (< 5 мс):** Алгоритми підбору працюють із попередньо валідованими локальними JSON-каталогами 5 дисциплін (*Біг, Велоспорт, Триатлон, Зал / Фітнес, Походи / ЇDLO*). Сервіс не робить «важких» блокуючих SQL-запитів до бази OpenCart під час кліків покупця у браузері.
* **Single Gel Brand Rule:** Для бігунів алгоритм фіксує єдиний базовий бренд гелів на всю дистанцію (SiS, Nutrend, Maurten, Precision Fuel або PowerBar), унеможливлюючи шлунковий дискомфорт через різноосмолярні вуглеводи.
* **Same-Origin & Cookies:** Сервіс призначений для проксіювання через Nginx на підпапку основного сайту `https://raceexpert.com.ua/quiz/`. Це гарантує спільні сесійні cookies `OCSESSID` і виключає блокування кошика браузерами (Safari ITP / Chrome Privacy Sandbox).

---

## 2. Швидкий старт

### Варіант А: Запуск через Docker Compose (Рекомендовано)

1. **Клонуйте репозиторій на сервер магазину:**
   ```bash
   git clone https://github.com/voyfur/re_quiz.git /var/www/raceexpert-quiz
   cd /var/www/raceexpert-quiz
   ```

2. **Створіть конфігураційний файл оточення:**
   ```bash
   cp .env.example .env
   ```
   *(Заповніть змінні у `.env` — детальний опис у Розділі 6).*

3. **Запустіть контейнер у фоновому режимі:**
   ```bash
   docker compose up -d --build
   ```

4. **Перевірте стан контейнера:**
   ```bash
   docker compose ps
   curl -f http://127.0.0.1:8000/api/health
   ```

---

### Варіант Б: Запуск як системна служба Linux (systemd)

Якщо на сервері не використовується Docker:

1. **Створіть службовий юніт `/etc/systemd/system/quiz.service`:**
   ```ini
   [Unit]
   Description=Race Expert Quiz & Starter Box Builder
   After=network.target

   [Service]
   Type=simple
   User=www-data
   Group=www-data
   WorkingDirectory=/var/www/raceexpert-quiz
   EnvironmentFile=/var/www/raceexpert-quiz/.env
   ExecStart=/usr/bin/python3 /var/www/raceexpert-quiz/server.py
   Restart=always
   RestartSec=5
   StandardOutput=append:/var/www/raceexpert-quiz/logs/server.log
   StandardError=append:/var/www/raceexpert-quiz/logs/error.log

   [Install]
   WantedBy=multi-user.target
   ```

2. **Створіть папку для логів та запустіть службу:**
   ```bash
   mkdir -p /var/www/raceexpert-quiz/logs
   sudo chown -R www-data:www-data /var/www/raceexpert-quiz
   sudo systemctl daemon-reload
   sudo systemctl enable --now quiz.service
   sudo systemctl status quiz.service
   ```

---

## 3. Налаштування Nginx Reverse Proxy

Щоб квіз відкривався за адресою `https://raceexpert.com.ua/quiz/` і мав безперешкодний доступ до сесії OpenCart, додайте наступний блок у конфігураційний файл віртуального хосту сайту (наприклад, `/etc/nginx/sites-available/raceexpert.com.ua`):

```nginx
# ------------------------------------------------------------------------------
# Race Expert Quiz & Starter Box Builder
# ------------------------------------------------------------------------------
location /quiz/ {
    proxy_pass http://127.0.0.1:8000/;
    proxy_http_version 1.1;
    
    # Передача оригінальних заголовків клієнта
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
    
    # Безперешкодна передача cookies сесії OpenCart (OCSESSID)
    proxy_pass_header Set-Cookie;
    proxy_cookie_path / /;

    # Тайм-аути
    proxy_connect_timeout 10s;
    proxy_read_timeout 60s;
    proxy_send_timeout 60s;
}
```

Перевірте коректність конфігурації Nginx та застосуйте зміни:
```bash
sudo nginx -t && sudo systemctl reload nginx
```

---

## 4. Інтеграція з кошиком OpenCart

Покупець формує бокс і натискає кнопку «Купити бокс». Клієнтський скрипт передає всі обрані позиції в один клік у кошик магазину.

### ⚠️ Важливе зауваження щодо сесій OpenCart
В OpenCart (гілки 2.x та 3.x) стандартний обробник сесій `catalog/controller/startup/session.php` перевіряє маршрут: якщо маршрут починається з `api/`, OpenCart **ігнорує сесійну куку браузера `OCSESSID`** і очікує передачу `api_token`.
Саме тому контролер розміщено за маршрутом `checkout/quiz_cart/add_bulk`, що гарантує надійну прив'язку товарів до реального кошика покупця.

### Інструкція зі встановлення:
1. Скопіюйте файл контролера з репозиторію в каталог сайту OpenCart:
   ```bash
   cp /var/www/raceexpert-quiz/integrations/opencart/catalog/controller/checkout/quiz_cart.php \
      /var/www/raceexpert.com.ua/catalog/controller/checkout/quiz_cart.php
   ```

2. **Права на файл:**
   ```bash
   chmod 644 /var/www/raceexpert.com.ua/catalog/controller/checkout/quiz_cart.php
   chown www-data:www-data /var/www/raceexpert.com.ua/catalog/controller/checkout/quiz_cart.php
   ```

3. **Маршрут додавання:** `POST https://raceexpert.com.ua/index.php?route=checkout/quiz_cart/add_bulk`

4. **Формат вхідного тіла запиту (JSON):**
   ```json
   {
     "items": [
       {"product_id": 1940, "quantity": 4},
       {"product_id": 3110, "quantity": 1},
       {"product_id": 5422, "quantity": 2}
     ]
   }
   ```

5. **Формат відповіді (JSON):**
   ```json
   {
     "success": true,
     "added_items": 7,
     "total_items": 7,
     "redirect": "https://raceexpert.com.ua/index.php?route=checkout/cart"
   }
   ```

---

## 5. Реєстр API Endpoints та приклади curl

### 1. Перевірка працездатності (Healthcheck)
* **URL:** `GET http://127.0.0.1:8000/api/health`
* **Призначення:** Моніторинг статусу сервісу, кількості активних товарів та доступності модулів.
* **Приклад curl:**
  ```bash
  curl -s http://127.0.0.1:8000/api/health | jq .
  ```
* **Приклад відповіді:**
  ```json
  {
    "status": "ok",
    "timestamp": "2026-11-20T11:22:00",
    "running_catalog_count": 478,
    "engines": {
      "multi_sport_engine": true,
      "runner_box_engine": true,
      "luna_box_consultant": true
    }
  }
  ```

---

### 2. Генерація боксу під дисципліну та параметри атлета
* **URL:** `POST http://127.0.0.1:8000/api/generate-sport-box`
* **Headers:** `Content-Type: application/json`
* **Підтримувані види спорту (`sport`):** `running`, `cycling`, `triathlon`, `gym`, `outdoor`.
* **Приклад curl (Марафон з кофеїном та захистом від судом):**
  ```bash
  curl -X POST http://127.0.0.1:8000/api/generate-sport-box \
    -H "Content-Type: application/json" \
    -d '{
      "sport": "running",
      "distance": "marathon",
      "pace_target": "sub330",
      "weather": "hot",
      "stomach_type": "normal",
      "caffeine_preference": "boost",
      "body_concerns": ["cramps"],
      "gear_needed": ["belt"],
      "price_tier": "standard"
    }' | jq .
  ```
* **Приклад curl (Велоспорт 100 км із точним кастомним бюджетом):**
  ```bash
  curl -X POST http://127.0.0.1:8000/api/generate-sport-box \
    -H "Content-Type: application/json" \
    -d '{
      "sport": "cycling",
      "distance": "100k",
      "custom_budget": 1850,
      "weather": "moderate",
      "gear_needed": ["bottle"]
    }' | jq .
  ```

---

### 3. ШІ-консультація спортивного нутриціолога (Луна)
* **URL:** `POST http://127.0.0.1:8000/api/luna-consult-box`
* **Headers:** `Content-Type: application/json`
* **Призначення:** Отримання персоналізованого аналізу та таймінгу прийому гелів і солей на дистанції від GPT-4o-mini.
* **Приклад curl:**
  ```bash
  curl -X POST http://127.0.0.1:8000/api/luna-consult-box \
    -H "Content-Type: application/json" \
    -d '{
      "locale": "uk",
      "user_inputs": {
        "sport": "running",
        "distance": "marathon",
        "pace_target": "sub330"
      },
      "generated_box": {
        "sport_name": "Біг",
        "total_base_price": 1420
      }
    }' | jq .
  ```

---

### 4. Перевірка залишків та цін у реальному часі (Stock Check)
* **URL:** `POST http://127.0.0.1:8000/api/check-stock`
* **Headers:** `Content-Type: application/json`
* **Призначення:** Верифікація актуальних залишків та цін за списком артикулів (SKU/Model) напряму в таблиці `oc_product` OpenCart MySQL.
* **Приклад curl:**
  ```bash
  curl -X POST http://127.0.0.1:8000/api/check-stock \
    -H "Content-Type: application/json" \
    -d '{
      "skus": ["RE89450", "RE12345", "SIS-GEL-01"]
    }' | jq .
  ```
* **Приклад відповіді:**
  ```json
  {
    "ok": true,
    "stocks": {
      "RE89450": {
        "sku": "RE89450",
        "product_id": 7149,
        "in_stock": true,
        "quantity": 15,
        "live_price_uah": 1525.0,
        "stock_status_text_uk": "В наявності",
        "is_live_check": true
      }
    }
  }
  ```

---

### 5. Тест пакетного додавання в кошик OpenCart
* **URL:** `POST https://raceexpert.com.ua/index.php?route=checkout/quiz_cart/add_bulk`
* **Headers:** `Content-Type: application/json`, `Cookie: OCSESSID=<сесія>`
* **Приклад curl:**
  ```bash
  curl -X POST https://raceexpert.com.ua/index.php?route=checkout/quiz_cart/add_bulk \
    -H "Content-Type: application/json" \
    -H "Cookie: OCSESSID=7b38d49a8f2348c90b621e2894" \
    -d '{
      "items": [
        {"product_id": 1940, "quantity": 3},
        {"product_id": 3110, "quantity": 1}
      ]
    }' | jq .
  ```

---

## 6. Змінні оточення та ключі доступу (`.env`)

Скопіюйте приклад файлу конфігурації перед запуском:
```bash
cp .env.example .env
```

| Змінна | Призначення | Значення за замовчуванням | Обов'язкова? |
|---|---|---|:---:|
| `PORT` | Внутрішній TCP-порт HTTP-сервера | `8000` | Так |
| `BIND_HOST` | Інтерфейс прив'язки сокета (`0.0.0.0` для Docker) | `0.0.0.0` | Так |
| `BASE_URL` | Головний домен магазину | `https://raceexpert.com.ua` | Так |
| `OPENCART_BULK_ENDPOINT` | Маршрут пакетного додавання в кошик | `/index.php?route=checkout/quiz_cart/add_bulk` | Так |
| `OPENCART_CART_ENDPOINT` | Резервний нативний поштучний маршрут кошика | `/index.php?route=checkout/cart/add` | Так |
| `OPENCART_VIEW_CART_URL` | Сторінка кошика магазину для редиректу | `/index.php?route=checkout/cart` | Так |
| `OPENAI_API_KEY` | API-ключ OpenAI для консультанта Луни | `sk-proj-...` | Опціонально |
| `LUNA_MODEL` | Модель генерації порад нутриціолога | `gpt-4o-mini` | Опціонально |
| `MYSQL_HOST` | IP/хост бази OpenCart для перевірки залишків | `127.0.0.1` | Опціонально |
| `MYSQL_PORT` | Порт MySQL сервера магазину | `3306` | Опціонально |
| `MYSQL_DATABASE` | Назва бази даних OpenCart | `raceexpertcomua` | Опціонально |
| `MYSQL_USER` | Користувач MySQL із правом `SELECT` | `raceexpert_readonly` | Опціонально |
| `MYSQL_PASSWORD` | Пароль користувача MySQL | - | Опціонально |
| `TELEGRAM_BOT_TOKEN` | Токен бота для отримання логів замовлень | - | Опціонально |
| `TELEGRAM_CHAT_ID` | Telegram Chat ID адміністратора | - | Опціонально |

---

## 7. Каталоги товарів та оновлення залишків

Усі товари згруповані у валідованих JSON-каталогах:
* `running_catalog.json` — товари для бігунів (гелі, електроліти, солі, шкарпетки, пояси);
* `cycling_catalog.json` — харчування та спорядження для велосипедистів (фляги, ізотоніки, батончики);
* `triathlon_catalog.json` — триатлон (гідрокостюми, шапочки, швидкі вуглеводи);
* `gym_catalog.json` — протеїни, креатин, BCAA, шейкери;
* `outdoor_catalog.json` — сублімоване повноцінне харчування ЇDLO для походів та кемпінгу.

### Регламентне оновлення цін та залишків:
За замовчуванням сервіс підбирає товари миттєво з каталогів. Для періодичної синхронізації змін цін та наявності з бази OpenCart можна налаштувати простий нічний Cron:
```bash
# Синхронізація каталогів щоночі о 03:00
0 3 * * * cd /var/www/raceexpert-quiz && python3 scripts/sync_catalog_from_opencart.py >> logs/sync.log 2>&1
```

---

## 8. Чек-лист перевірки запуску (Smoke Test)

Виконайте ці 4 кроки після розміщення на сервері:

1. **Крок 1: Запуск та healthcheck бекенду**
   ```bash
   curl -f http://127.0.0.1:8000/api/health
   # Очікується HTTP 200 та {"status": "ok"}
   ```

2. **Крок 2: Перевірка проксіювання через домен магазину**
   Відкрийте в браузері: `https://raceexpert.com.ua/quiz/`
   * Має відкритися фірмова світла сторінка конструктора стартового боксу Race Expert.
   * Усі 5 вкладок видів спорту мають перемикатися без затримок.

3. **Крок 3: Тест кнопки «Купити бокс»**
   * Оберіть спорт (наприклад, Біг -> 21 км).
   * Натисніть «Скласти бокс».
   * На екрані результатів спробуйте зняти/додати галочку з окремого товару (сума має перерахуватися на льоту).
   * Натисніть синю кнопку **«Купити бокс»**.
   * Браузер має показати повідомлення про успішне додавання та автоматично перенаправити вас на сторінку `https://raceexpert.com.ua/index.php?route=checkout/cart`.
   * **Усі обрані товари мають знаходитися у вашому реальному кошику OpenCart!**

4. **Крок 4: Запуск регресійних тестів**
   ```bash
   pytest -v
   # Усі 690 тестів мають пройти з результатом 100% PASS (включаючи 225 E2E-сценаріїв та Chrome Headless)
   ```
