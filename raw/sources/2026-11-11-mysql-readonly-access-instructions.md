# Инструкция и параметры подключения к MySQL (read-only) — 2026-11-11

## Источник

Указания пользователя на основе результатов и ограничений проверки из проекта «ШІ-помічник у картці товару» (`wiki/sources/mysql-readonly-access-and-product-query-guide.md`).

## Параметры и ограничения

1. **Маршрут подключения:** Подключаться к MySQL исключительно с VPS-61125 (`185.25.119.96`) на порт `3306`. Доступ разрешён и проверен именно с этого VPS.
2. **База данных:** `raceexpertcomua`. Хост, логин и пароль берутся из MySQL-блока локального `.env`. В `.env` дублируются `HOST` и `PASSWORD` в блоках SSH и MySQL: не делать `source` всего файла и не загружать его целиком как dotenv. Использовать отдельные ключи: `MYSQL_HOST`, `MYSQL_PORT`, `MYSQL_DATABASE`, `MYSQL_USER`, `MYSQL_PASSWORD`. Значения паролей не выводить в чат, логи и shell history.
3. **Требования к TLS:** Требовать TLS без перехода на открытое соединение (plaintext). Ошибка `SSLCertVerificationError` ожидаема из-за самоподписанного сертификата сервера MySQL. Пользователь разрешил для разовой read-only проверки обязательный TLS с отключённой проверкой сертификата. Это не постоянное production-решение (для production нужен доверенный CA или SSH/VPN-туннель).
4. **Проверочные запросы:**
   - `SELECT DATABASE()`
   - `SELECT 1`
   - `SHOW GRANTS FOR CURRENT_USER`
   - `SHOW COLUMNS FROM ...` и `SELECT * FROM ... LIMIT 0` для пяти таблиц контекста товара:
     - `oc_product`
     - `oc_product_description`
     - `oc_product_attribute`
     - `oc_attribute_description`
     - `oc_stock_status`
5. **Ограничения прав и безопасности:**
   - Не запрашивать строки отзывов или заказов.
   - Не запрашивать `oc_review_article` (нет прав SELECT, грант отсутствует).
   - Не использовать старые `product_id` без нового поиска по `model` / `sku`.
