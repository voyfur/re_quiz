---
schema_version: 2
id: "source.mysql-readonly-access-and-product-query-guide"
type: "source"
title: "MySQL: read-only подключение и запрос контекста OpenCart"
description: "Практический порядок подключения через VPS-61125, подтверждённые ограничения TLS и SELECT, структура пяти таблиц товара и подготовленный запрос контекста."
tags: ["project:quiz-product-set-generator", "domain:ecommerce", "topic:database-access", "topic:database-schema", "topic:product-data", "workflow:discovery"]
source: {"raw_path": "raw/sources/2026-11-11-mysql-readonly-access-instructions.md"}
dates: {"added_at": "2026-11-11T12:15:00+02:00", "updated_at": "2026-11-11T12:15:00+02:00"}
relations: [{"type": "supports", "target": "project.quiz-product-set-generator"}]
aliases: ["OpenCart read-only MySQL guide", "Подключение к MySQL Race Expert", "Запрос контекста товара OpenCart"]
status: "active"
---

# MySQL: read-only подключение и запрос контекста OpenCart

## 1. Назначение инструкции

Для проверки наличия и актуальной цены наборов перед выдачей рекомендаций квиза достаточно существующих OpenCart-таблиц и оператора `SELECT`. Создавать новые таблицы или менять данные не требуется. Эта инструкция фиксирует проверенный маршрут, параметры безопасности, схему пяти таблиц и тестовые запросы.

## 2. Маршрут подключения и требования TLS

1. **Маршрут:** Соединение к MySQL выполняется **исключительно с VPS автоматизаций VPS-61125 (`185.25.119.96`)** на порт `3306`. Проверка подтверждает доступ именно с этого IP; напрямую с других IP порт может быть закрыт firewall.
2. **Переменные окружения:** В `.env` используются отдельные переменные во избежание коллизий с SSH:
   ```env
   MYSQL_HOST=173.242.63.36
   MYSQL_PORT=3306
   MYSQL_DATABASE=raceexpertcomua
   MYSQL_USER=raceexpert_readonly
   MYSQL_PASSWORD=...
   ```
   Секреты никогда не выводятся в логи, сообщения чата или shell history.
3. **Требования к TLS:**
   - MySQL endpoint требует обязательный TLS 1.3 (`TLS_AES_256_GCM_SHA384`).
   - Сервер предъявляет самоподписанный сертификат с собственным внутренним CA, поэтому возникает ожидаемая ошибка `SSLCertVerificationError`.
   - Пользователь дал явное разрешение на разовую read-only проверку с обязательным TLS и отключённой проверкой валидности сертификата.
   - **Запрещён переход на открытый текст (plaintext)** при ошибке сертификата.
   - Это разовый режим проверки. Для постоянного production backend необходим доверенный CA или туннелирование (SSH / VPN).

## 3. Права пользователя (Grants) и схема

База данных: `raceexpertcomua`.
Текущий пользователь имеет `USAGE ON *.*` и `SELECT` только на 7 таблицах:
- `oc_product` (основные параметры товара, цена, остаток, статус)
- `oc_product_description` (локализованное название и описание)
- `oc_product_attribute` (значения атрибутов)
- `oc_attribute_description` (названия атрибутов)
- `oc_stock_status` (статусы наличия на складе)
- `oc_review` (отзывы — не запрашивать)
- `oc_remarketing_orders` (заказы — не запрашивать)

Таблица `oc_review_article` не имеет grant на `SELECT` и не должна запрашиваться.

## 4. Проверочные запросы подключения

```sql
SELECT DATABASE();
SELECT 1;
SHOW GRANTS FOR CURRENT_USER;

SHOW COLUMNS FROM oc_product;
SHOW COLUMNS FROM oc_product_description;
SHOW COLUMNS FROM oc_product_attribute;
SHOW COLUMNS FROM oc_attribute_description;
SHOW COLUMNS FROM oc_stock_status;

SELECT * FROM oc_product LIMIT 0;
SELECT * FROM oc_product_description LIMIT 0;
SELECT * FROM oc_product_attribute LIMIT 0;
SELECT * FROM oc_attribute_description LIMIT 0;
SELECT * FROM oc_stock_status LIMIT 0;
```

## 5. Запрос поиска товара и набора перед рекомендацией

Поиск товара выполняется свежим запросом по `model` или `sku`:

```sql
SELECT product_id, model, sku, price, quantity, stock_status_id, status, subtract
FROM oc_product
WHERE model = ? OR sku = ?
ORDER BY product_id
LIMIT 2;
```

Подтверждённые языковые коды в `raceexpertcomua`:
- `1` — русский (`ru`)
- `6` — украинский (`uk`)
