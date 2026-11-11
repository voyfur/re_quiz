# Протокол проверки подключения к MySQL (read-only) — 2026-11-11

## Маршрут и безопасность

- **Маршрут:** Выполнен с VPS автоматизации `VPS-61125` (`185.25.119.96`) на порт `3306` MySQL endpoint (`173.242.63.36`).
- **Схема:** `raceexpertcomua`.
- **Пользователь:** `raceexpert_readonly`.
- **TLS:** Обязательный TLS 1.3 (`TLS_AES_256_GCM_SHA384`), сервер `8.0.45-36`. Ошибка `SSLCertVerificationError` обработана отключением валидации самоподписанного сертификата на основании разового разрешения пользователя. Plaintext fallback не использовался.
- **Секреты:** Не сохранялись на VPS, не передавались в аргументах командной строки и не выводились в логи.

## Результаты проверок

1. `SELECT DATABASE()`: возвращено `raceexpertcomua`.
2. `SELECT 1`: возвращено `1`.
3. `SHOW GRANTS FOR CURRENT_USER`: подтверждены `USAGE ON *.*` и `SELECT` на семи таблицах:
   - `oc_product`
   - `oc_product_description`
   - `oc_product_attribute`
   - `oc_attribute_description`
   - `oc_stock_status`
   - `oc_review` (не запрашивалась)
   - `oc_remarketing_orders` (не запрашивалась)
4. Проверка `SHOW COLUMNS` и `SELECT * FROM <table> LIMIT 0`:
   - `oc_product`: 34 столбца подтверждены, 0 строк возвращено.
   - `oc_product_description`: 10 столбцов подтверждены, 0 строк возвращено.
   - `oc_product_attribute`: 4 столбца подтверждены, 0 строк возвращено.
   - `oc_attribute_description`: 3 столбца подтверждены, 0 строк возвращено.
   - `oc_stock_status`: 3 столбца подтверждены, 0 строк возвращено.
5. Тестовый поиск по SKU набора `RE89450`:
   - `product_id`: `7149`
   - `model`: `RE89450`
   - `sku`: `RE89450`
   - `price`: `1525.0000`
   - `quantity`: `15`
   - `stock_status_id`: `5`
   - `status`: `1`
