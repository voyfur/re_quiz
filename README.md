# Race Expert Quiz & Starter Box Builder

Інтелектуальний сервіс генерації персональних стартових та тренувальних боксів (Т-наборів) для інтернет-магазину [Race Expert](https://raceexpert.com.ua).

Сервіс покриває 5 ключових дисциплін: **Біг, Велоспорт, Триатлон, Зал / Фітнес, Походи / ЇDLO**.

---

## 🚀 Ключові можливості системи

1. **Миттєвий алгоритмічний підбір (< 5 мс):**
   - Усі каталоги товарів та матриці сумісності попередньо валідовані та зберігаються в оптимізованому JSON-форматі.
   - Відсутнє блокуюче навантаження на базу даних OpenCart під час кожного кліку покупця.

2. **Захист від шлункового дискомфорту (Single Gel Brand Rule):**
   - Алгоритм бігових та мультиспортивних наборів закріплює єдиний базовий бренд гелів (Nutrend, SiS, Maurten, Precision Fuel або PowerBar) на всю дистанцію.
   - Запобігає небезпечному змішуванню різноосмолярних вуглеводних формул (наприклад, мальтодекстрин SiS проти ізомальтулози Nutrend).

3. **3-рівнева оптимізація під точний бюджет покупця:**
   - Пресети вартості: **Базовий / Економ, Оптимальний, Максимальний / Pro** та підтримка довільного бюджету покупця (Custom Number).
   - Розумний алгоритм балансування кількості та вартості: пріоритет віддається життєво необхідним позиціям харчування та гідратації, а спеціалізовані аксесуари захищені від випадкової заміни.

4. **Інтерактивний вибір товарів покупцем:**
   - На фінальному екрані покупець може гнучко знімати або повертати окремі товари за допомогою інтерактивних галочок `[✓ В кошик]`.
   - Загальна сума боксу перераховується на льоту на клієнті.

5. **Пакетне додавання в кошик OpenCart за 1 клік:**
   - Весь сформований бокс передається в кошик покупця одним атомарним POST-запитом без черги запитів та затримок.

---

## 📁 Структура репозиторію

```text
├── server.py                   # Легковаговий виробничий HTTP-сервер (Python 3.10+)
├── runner_box_engine.py        # Алгоритмічний рушій підбору бігових боксів
├── multi_sport_engine.py       # Алгоритмічний рушій для велоспорту, триатлону, залу та походів
├── stock_checker.py            # Модуль перевірки залишків товарів у MySQL OpenCart
├── luna_box_consultant.py      # ШІ-консультант Луна (GPT-аналіз боксу під завдання атлета)
│
├── running_catalog.json        # Очищений каталог товарів для бігу
├── cycling_catalog.json        # Каталог товарів для велоспорту
├── triathlon_catalog.json      # Каталог товарів для триатлону
├── gym_catalog.json            # Каталог товарів для фітнесу та залу
├── outdoor_catalog.json        # Каталог сублімованого харчування та походів (ЇDLO)
│
├── public/                     # Клієнтський інтерфейс
│   ├── runner_box.html         # Адаптивний UI (Tailwind CSS CDN, мобільна оптимізація)
│   └── runner_box.js           # Логіка форми, фільтрів, розрахунку та зв'язку з кошиком
│
├── integrations/               # Готові модулі інтеграції
│   └── opencart/               # PHP-контролер пакетного додавання в кошик OpenCart
│       └── catalog/controller/api/quiz_cart.php
│
├── Dockerfile                  # Production-образ (Python 3.12-slim)
├── docker-compose.yml          # Маніфест швидкого запуску контейнера
├── .env.example                # Шаблон змінних оточення з коментарями
├── requirements.txt            # Залежності середовища та тестів
└── tests/                      # Автоматизовані тести перевірки конфігурації та логіки
```

---

## 🛠️ Швидкий старт та розгортання

### Варіант 1: Запуск через Docker Compose (Рекомендовано)

1. Клонуйте репозиторій на сервер:
   ```bash
   git clone https://github.com/race-expert/quiz.git /var/www/raceexpert-quiz
   cd /var/www/raceexpert-quiz
   ```

2. Створіть файл оточення:
   ```bash
   cp .env.example .env
   ```

3. Запустіть сервіс у фоновому режимі:
   ```bash
   docker compose up -d
   ```

Сервіс автоматично запуститься на порту `8000` із перезапуском у разі збоїв (`restart: always`) та перевіркою працездатності (healthcheck).

---

### Варіант 2: Запуск через systemd (Native Linux Service)

Якщо на сервері не використовується Docker, сервіс можна запустити як штатну службу Linux:

1. Створіть юніт-файл `/etc/systemd/system/quiz.service`:
   ```ini
   [Unit]
   Description=Race Expert Quiz & Starter Box Builder
   After=network.target

   [Service]
   Type=simple
   User=www-data
   WorkingDirectory=/var/www/raceexpert-quiz
   EnvironmentFile=/var/www/raceexpert-quiz/.env
   ExecStart=/usr/bin/python3 /var/www/raceexpert-quiz/server.py
   Restart=always
   RestartSec=5

   [Install]
   WantedBy=multi-user.target
   ```

2. Активуйте та запустіть службу:
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable --now quiz.service
   sudo systemctl status quiz.service
   ```

---

## 🌐 Налаштування Nginx Reverse Proxy (Основний домен магазину)

**Рекомендований маршрут:** `https://raceexpert.com.ua/quiz/`

Проксіювання запитів через Nginx основного домену забезпечує три критичні переваги:
1. **Єдиний домен (`Same-Origin`):** Квіз і OpenCart знаходяться в одному джерелі.
2. **Спільні Cookies сесії OpenCart (`OCSESSID`):** Коли покупець додає бокс у кошик, браузер автоматично передає активну сесійну куку OpenCart. Немає блокування сторонніх cookies сучасними браузерами (Safari ITP, Chrome Privacy Sandbox).
3. **Відсутність проблем із CORS:** Запити виконуються без додаткових заголовків і preflight-затримок OPTIONS.

### Конфігурація Nginx

Додайте цей блок усередину `server { ... }` основного сайту `/etc/nginx/sites-available/raceexpert.com.ua`:

```nginx
# Race Expert Quiz & Box Builder
location /quiz/ {
    proxy_pass http://127.0.0.1:8000/;
    proxy_http_version 1.1;
    
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
    
    # Підтримка передачі cookies сесії OpenCart (OCSESSID)
    proxy_pass_header Set-Cookie;
    proxy_cookie_path / /;

    proxy_connect_timeout 10s;
    proxy_read_timeout 60s;
}
```

Після збереження перевірте конфігурацію та перезавантажте Nginx:
```bash
sudo nginx -t && sudo systemctl reload nginx
```

---

## 🛒 Інтеграція з кошиком OpenCart

У репозиторії підготовлено готовий PHP-контролер для OpenCart 3.x / 4.x:
`integrations/opencart/catalog/controller/api/quiz_cart.php`

### Встановлення контролера:
1. Скопіюйте файл у структуру каталогу магазину:
   ```bash
   cp /var/www/raceexpert-quiz/integrations/opencart/catalog/controller/api/quiz_cart.php \
      /var/www/raceexpert.com.ua/catalog/controller/api/quiz_cart.php
   ```

2. Контролер реєструє ендпоінт:
   `POST /index.php?route=api/quiz_cart/add_bulk`

3. **Як це працює:**
   - Приймає JSON-масив товарів:
     ```json
     {
       "items": [
         {"product_id": 1940, "quantity": 4},
         {"product_id": 3110, "quantity": 1},
         {"product_id": 5422, "quantity": 2}
       ]
     }
     ```
   - Викликає нативний метод OpenCart `$this->cart->add($product_id, $quantity)` для кожної позиції.
   - Очищує закешовані методи доставки та оплати в сесії (`shipping_methods`, `payment_methods`), гарантуючи актуальний перерахунок кошика.
   - Повертає статус успіху, загальну кількість товарів та URL для переходу в кошик:
     ```json
     {
       "success": true,
       "added_items": 7,
       "total_items": 7,
       "redirect": "https://raceexpert.com.ua/index.php?route=checkout/cart"
     }
     ```

---

## 🔍 Перевірка роботи API через curl

### 1. Генерація боксу за видом спорту
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
  }'
```

### 2. Запит консультації ШІ Луни
```bash
curl -X POST http://127.0.0.1:8000/api/luna-consult-box \
  -H "Content-Type: application/json" \
  -d '{
    "locale": "uk",
    "user_inputs": {"sport": "cycling", "distance": "century"},
    "generated_box": {"sport_name": "Велоспорт", "total_base_price": 1450}
  }'
```

### 3. Тест пакетного додавання в кошик OpenCart
```bash
curl -X POST https://raceexpert.com.ua/index.php?route=api/quiz_cart/add_bulk \
  -H "Content-Type: application/json" \
  -H "Cookie: OCSESSID=your_opencart_session_id" \
  -d '{
    "items": [
      {"product_id": 1940, "quantity": 2}
    ]
  }'
```

---

## 🧪 Автоматизоване тестування

Репозиторій покритий повним набором автоматичних тестів (`pytest`):
- 250 стрес-сценаріїв для всіх 5 видів спорту (по 50 на кожну дисципліну);
- 20 комплексних персон бігунів;
- тести цілісності каталогів та перевірки наявності;
- тести Docker-середовища, змінних оточення та контролера OpenCart.

Запуск усіх тестів:
```bash
pytest -v
```
