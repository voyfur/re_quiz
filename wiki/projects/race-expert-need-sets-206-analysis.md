---
schema_version: 2
id: "document.race-expert-need-sets-206-analysis"
type: "document"
title: "206 наборов «За потребами»: состав, назначение и теги"
description: "Завершённый разбор состава и назначения 206 наборов раздела «За потребами» с источниками, тегами и отмеченными расхождениями."
tags: ["project:quiz-product-set-generator", "topic:product-catalog", "topic:product-recommendations", "workflow:catalog-inventory", "language:uk"]
source: {"raw_path": "raw/sources/2026-11-06-approved-tags-for-206-sets.md", "url": "https://raceexpert.com.ua/nabori/po-potrebam/"}
dates: {"added_at": "2026-11-06T16:58:56+02:00", "updated_at": "2026-11-06T18:55:12+02:00"}
relations: [{"type": "applies-to", "target": "project.quiz-product-set-generator"}, {"type": "references", "target": "document.race-expert-set-catalog-2026-11-06"}]
aliases: ["Анализ наборов за потребностями", "Теги 206 наборов Race Expert"]
status: "active"
---

# 206 наборов «За потребами»: состав, назначение и теги

## Объём и статус

В работу входят все **206 наборов** раздела [«За потребами»](https://raceexpert.com.ua/nabori/po-potrebam/) из снимка [каталога от 2026-11-06](race-expert-set-catalog-2026-11-06.md). Девятнадцать наборов раздела «По дистанціях» в этот разбор не входят.

Формат карточек и система тегов утверждены пользователем 2026-11-06. Разбор завершён: заполнены все **206 из 206** наборов «За потребами», каждому указана официальная карточка, состав/назначение и основные теги. Проверено соответствие наборов снимку каталога: пропусков и дублей нет. Строки 108–110 и 117 относятся к разделу «По дистанціях» и исключены; строки 211–225 также входят в этот раздел.

Цена в теге — цена набора из снимка каталога от 2026-11-06, в гривнах. Когда цена открытой карточки отличалась от снимка, наблюдение указано отдельно; все **49 зафиксированных расхождений** отмечены `data_quality:live_price_differs`. Цены и наличие меняются, поэтому снимок не заменяет проверку перед выдачей результата. Цена сама по себе не означает, что набор подходит к ещё не утверждённому диапазону бюджета квиза.

Во всех 206 карточках тег веса покупателя — `buyer_weight:not_specified`: диапазонов веса покупателя в проверенных источниках не найдено. Вес упаковки и размер обуви записываются отдельно. Неоднозначности состава и другие проблемы исходных карточек отмечены тегами `data_quality:*`; анализ описывает каталог и не утверждает, какие наборы должен рекомендовать квиз.

## Схема карточки

Для каждого набора фиксируются:

- **Набор:** название сайта, SKU и ссылка на карточку.
- **Состав:** входящие товары, количество, размер и масса упаковки, если указаны. Абонемент клуба и подарки отмечаются отдельно.
- **Назначение:** кратко, для чего сайт позиционирует набор; заявления о здоровье остаются заявлениями сайта, а не медицинским выводом.
- **Спорт и формат:** только виды активности, прямо связанные с назначением набора или его составом. Общие фразы из описания абонемента не переносятся автоматически на весь набор.
- **Дистанция:** числовые километры и формат соревнования записываются отдельно. «Марафон» не превращается автоматически в «42 км».
- **Вес покупателя:** диапазон добавляется только если источник прямо его указывает. Размер обуви и масса товара — отдельные характеристики. Если сведений нет, ставится `buyer_weight:not_specified`.
- **Цена и наличие:** цена UAH и тег точной цены на дату снимка; наличие — отдельное изменяемое поле с датой наблюдения.
- **Дополнительные признаки:** форма, длительность, целевая аудитория, тип набора и важные ингредиенты, только если они помогают идентификации и подтверждены источником.
- **Основание:** ссылка на официальную карточку; при недостатке данных — ссылка на официальный источник производителя. Спорные или выводные признаки помечаются.

## Словарь тегов

Каждый набор получает значения по базовым осям; дополнительные оси добавляются только при наличии подтверждённых данных.

| Ось | Формат | Примеры | Правило |
|---|---|---|---|
| Назначение | `purpose:<код>` | `purpose:hydration`, `purpose:strength_training`, `purpose:cold_weather_comfort` | По описанию конкретного набора и его составу. |
| Спорт/активность | `sport:<код>` | `sport:running`, `sport:strength_training`, `sport:hiking`, `sport:general_fitness`, `sport:not_sport_specific` | Не считать общую подписку на клуб доказательством назначения всего набора для бега. |
| Формат забега | `race_format:<код>` | `race_format:half_marathon`, `race_format:marathon` | Только если формат назван в описании. |
| Дистанция | `distance_km:<число>` или статус | `distance_km:10`, `distance:unspecified`, `distance:not_applicable` | Точные километры — только из источника; для бегового набора без числа — `unspecified`. |
| Цена | `price:<число>_uah` | `price:1058_uah` | Точная цена из каталожного снимка; ценовые диапазоны квиза отдельно не утверждены. |
| Вес покупателя | `buyer_weight:<диапазон>_kg` или статус | `buyer_weight:60-79_kg`, `buyer_weight:not_specified` | Только прямое ограничение или диапазон в источнике; не выводить из дозировки или комплекции. |
| Размер/масса товара | по типу товара | `shoe_size:43-45`, `package_weight:500_g` | Никогда не использовать вместо веса покупателя. |
| Тип/форма/срок | `item_type:`, `form:`, `duration:` | `item_type:supplement_bundle`, `form:capsules`, `duration:3_months` | По составу и названию карточки. |
| Аудитория | `audience:<код>` | `audience:children`, `audience:men_50_plus` | Только если аудитория названа в карточке; это не независимое подтверждение пригодности. |
| Состав | `contains:<код>` | `contains:caffeine`, `contains:creatine`, `contains:electrolytes` | Отмечать фактическое наличие компонента в составе. |
| Кофеин в полном наборе | `caffeine_per_set:<число>_mg` | `caffeine_per_set:400_mg` | Суммировать только подтверждённое содержание и количество кофеиносодержащих компонентов; указывать расчёт и источники. |
| Наличие | `availability:<код>` | `availability:in_stock`, `availability:out_of_stock`, `availability:unknown` | С датой снимка; статус может измениться. |
| Условия и качество данных | `weather:<код>`, `data_quality:<код>` | `weather:cold`, `data_quality:composition_conflict` | Фиксировать только явно значимые условия и реальные расхождения источников. |

Коды тегов пишутся строчными латинскими символами и `_`, чтобы их можно было стабильно искать и фильтровать. В пояснениях рядом сохраняются понятные русские/украинские названия.

## Правила источников и неизвестных данных

1. Для состава, назначения, цены, размера и наличия использовать официальную карточку набора. Для дополнительной информации искать официальный сайт производителя; сохранять ссылку.
2. Не добавлять вес покупателя, километры или пригодность для спорта по догадке. Если источник этого не говорит, оставлять значение неизвестным или неприменимым.
3. Если набор содержит добавки, записывать компоненты и наличие стимулирующих ингредиентов как факты состава. Не превращать рекламные формулировки в медицинские обещания и не придумывать инструкции по приёму.
4. Если страницы противоречат друг другу, сохранять оба факта с датой и источниками, а не выбирать молча.

## Карточки наборов

Номера ниже соответствуют строкам каталожного снимка; строки «По дистанціях» исключены. Цена и наличие — снимок на 2026-11-06.

### 1. RE89637 — Акційний набір термошкарпеток 1+1=3 «43–45»

- **Состав:** 3 пары термошкарпеток Race Expert, размер 43–45 (3 пары по цене 2).
- **Назначение:** тепло и комфорт при беге, походах и активности на улице в холодную погоду — как описано на карточке.
- **Спорт/дистанция:** бег, походы; конкретная дистанция не указана.
- **Цена/наличие:** 1 058 грн; «Є в наявності».
- **Вес покупателя:** не указан; размер обуви 43–45 — отдельный параметр.
- **Теги:** `item_type:apparel`, `purpose:cold_weather_comfort`, `sport:running`, `sport:hiking`, `distance:unspecified`, `weather:cold`, `shoe_size:43-45`, `buyer_weight:not_specified`, `price:1058_uah`, `availability:in_stock`.
- **Источник:** [карточка Race Expert](https://raceexpert.com.ua/index.php?route=product/product&product_id=7433).

### 2. RE89636 — Акційний набір термошкарпеток 1+1=3 «40–42»

- **Состав:** 3 пары термошкарпеток Race Expert, размер 40–42 (3 пары по цене 2).
- **Назначение:** тепло и комфорт при беге, походах и активности на улице в холодную погоду.
- **Спорт/дистанция:** бег, походы; конкретная дистанция не указана.
- **Цена/наличие:** 1 058 грн; «Є в наявності».
- **Вес покупателя:** не указан; размер обуви 40–42 — отдельный параметр.
- **Теги:** `item_type:apparel`, `purpose:cold_weather_comfort`, `sport:running`, `sport:hiking`, `distance:unspecified`, `weather:cold`, `shoe_size:40-42`, `buyer_weight:not_specified`, `price:1058_uah`, `availability:in_stock`.
- **Источник:** [карточка Race Expert](https://raceexpert.com.ua/index.php?route=product/product&product_id=7432).

### 3. RE89635 — Акційний набір термошкарпеток 1+1=3 «38–40»

- **Состав:** 3 пары термошкарпеток Race Expert, размер 38–40 (3 пары по цене 2).
- **Назначение:** тепло и комфорт при беге, походах и активности на улице в холодную погоду.
- **Спорт/дистанция:** бег, походы; конкретная дистанция не указана.
- **Цена/наличие:** 1 058 грн; «Є в наявності».
- **Вес покупателя:** не указан; размер обуви 38–40 — отдельный параметр.
- **Теги:** `item_type:apparel`, `purpose:cold_weather_comfort`, `sport:running`, `sport:hiking`, `distance:unspecified`, `weather:cold`, `shoe_size:38-40`, `buyer_weight:not_specified`, `price:1058_uah`, `availability:in_stock`.
- **Источник:** [карточка Race Expert](https://raceexpert.com.ua/index.php?route=product/product&product_id=7431).

### 4. RE89634 — Акційний набір термошкарпеток 1+1=3 «35–37»

- **Состав:** 3 пары термошкарпеток Race Expert, размер 35–37 (3 пары по цене 2).
- **Назначение:** тепло и комфорт при беге, походах и активности на улице в холодную погоду.
- **Спорт/дистанция:** бег, походы; конкретная дистанция не указана.
- **Цена/наличие:** 1 058 грн; «Є в наявності».
- **Вес покупателя:** не указан; размер обуви 35–37 — отдельный параметр.
- **Теги:** `item_type:apparel`, `purpose:cold_weather_comfort`, `sport:running`, `sport:hiking`, `distance:unspecified`, `weather:cold`, `shoe_size:35-37`, `buyer_weight:not_specified`, `price:1058_uah`, `availability:in_stock`.
- **Источник:** [карточка Race Expert](https://raceexpert.com.ua/index.php?route=product/product&product_id=7430).

### 5. RE89632 — Акційний набір темних шкарпеток, 5 пар «46–48»

- **Состав:** 5 пар тёмных носков Race Expert, размер 46–48.
- **Назначение:** комфорт при беге, занятиях спортом и активной повседневной жизни.
- **Спорт/дистанция:** бег и общая физическая активность; дистанция не указана.
- **Цена/наличие:** 950 грн; «Є в наявності».
- **Вес покупателя:** не указан; размер обуви 46–48 — отдельный параметр.
- **Теги:** `item_type:apparel`, `purpose:foot_comfort`, `sport:running`, `sport:general_fitness`, `distance:unspecified`, `shoe_size:46-48`, `buyer_weight:not_specified`, `price:950_uah`, `availability:in_stock`.
- **Источник:** [карточка Race Expert](https://raceexpert.com.ua/index.php?route=product/product&product_id=7429).

### 6. RE89631 — Акційний набір білих шкарпеток, 5 пар «46–48»

- **Состав:** 5 пар белых носков Race Expert, размер 46–48.
- **Назначение:** комфорт во время тренировок и активной повседневной жизни.
- **Спорт/дистанция:** бег и общая физическая активность; дистанция не указана.
- **Цена/наличие:** 950 грн; «Є в наявності».
- **Вес покупателя:** не указан; размер обуви 46–48 — отдельный параметр.
- **Теги:** `item_type:apparel`, `purpose:foot_comfort`, `sport:running`, `sport:general_fitness`, `distance:unspecified`, `shoe_size:46-48`, `buyer_weight:not_specified`, `price:950_uah`, `availability:in_stock`.
- **Источник:** [карточка Race Expert](https://raceexpert.com.ua/index.php?route=product/product&product_id=7428).

### 7. RE89630 — Акційний набір білих шкарпеток, 5 пар «35–37»

- **Состав:** 5 пар белых носков Race Expert, размер 35–37.
- **Назначение:** комфорт во время тренировок и активной повседневной жизни.
- **Спорт/дистанция:** бег и общая физическая активность; дистанция не указана.
- **Цена/наличие:** 950 грн; «Є в наявності».
- **Вес покупателя:** не указан; размер обуви 35–37 — отдельный параметр.
- **Теги:** `item_type:apparel`, `purpose:foot_comfort`, `sport:running`, `sport:general_fitness`, `distance:unspecified`, `shoe_size:35-37`, `buyer_weight:not_specified`, `price:950_uah`, `availability:in_stock`.
- **Источник:** [карточка Race Expert](https://raceexpert.com.ua/index.php?route=product/product&product_id=7427).

### 8. RE89450 — Набір «Fitly мікс» — абонемент на 3 місяці

- **Состав:** абонемент Race Expert Club на 3 месяца; 14 протеиновых батончиков Fitly по 45 г разных вкусов и 11 углеводных батончиков Fitly по 45 г.
- **Назначение:** иметь под рукой разнообразные перекусы в течение активного дня.
- **Спорт/дистанция:** конкретный вид спорта и дистанция не указаны.
- **Цена/наличие:** 1 500 грн; «Є в наявності».
- **Вес покупателя:** не указан; граммовка относится к батончикам.
- **Дополнительно:** клубная подписка 3 месяца; состав содержит белковые и углеводные батончики.
- **Теги:** `item_type:club_membership_bundle`, `purpose:portable_snack`, `sport:not_sport_specific`, `distance:not_applicable`, `duration:3_months`, `form:bars`, `contains:protein`, `contains:carbohydrate`, `buyer_weight:not_specified`, `price:1500_uah`, `availability:in_stock`.
- **Источник:** [карточка Race Expert](https://raceexpert.com.ua/7149-nabir-fitly-miks-abonement-na-3-misyaci-re89450-1-525-g).

### 9. RE11522 — Набір «Чиста сила Race Expert Club»

- **Состав:** абонемент Race Expert Club на 3 месяца; креатин Myprotein Creatine Monohydrate 500 г; шейкер Myprotein объёмом 600 мл.
- **Назначение и спорт:** силовые показатели и рост мышечной массы; силовые тренировки.
- **Дистанция:** не применима.
- **Цена/наличие:** 1 399 грн; «Є в наявності».
- **Вес покупателя:** не указан; 500 г — масса упаковки креатина.
- **Теги:** `item_type:club_membership_bundle`, `purpose:strength_training_support`, `sport:strength_training`, `distance:not_applicable`, `duration:3_months`, `contains:creatine`, `package_weight:500_g`, `package_volume:600_ml`, `buyer_weight:not_specified`, `price:1399_uah`, `availability:in_stock`.
- **Источник:** [карточка Race Expert](https://raceexpert.com.ua/6771-nabir-chista-sila-re11522-1-745-grn-re11522-sila-i-masa).

### 10. RE88951 — Набір «Захисний комплекс Race Expert Club»

- **Состав:** абонемент Race Expert Club на 3 месяца; экстракт шиитаке Mind Shi, 1 000 мг, 60 капсул; цинк пиколинат Now Foods, 50 мг, 30 капсул; селен Now Foods, 200 мкг, 90 капсул.
- **Назначение:** поддержка иммунитета, антиоксидантная поддержка и общее самочувствие — формулировки карточки сайта.
- **Спорт/дистанция:** конкретный вид спорта и дистанция не указаны.
- **Цена/наличие:** 1 275 грн; «Є в наявності».
- **Вес покупателя:** не указан.
- **Теги:** `item_type:club_membership_bundle`, `purpose:general_wellness`, `purpose:immune_support_claim`, `sport:not_sport_specific`, `distance:not_applicable`, `duration:3_months`, `contains:shiitake`, `contains:zinc`, `contains:selenium`, `buyer_weight:not_specified`, `price:1275_uah`, `availability:in_stock`.
- **Источник:** [карточка Race Expert](https://raceexpert.com.ua/7011-nabir-zahisnij-kompleks-re88951-1-519-grn-re88951-shode).

### 11. RE11023 — Акційний набір білих шкарпеток, 5 пар «43–45»

- **Состав:** 5 пар белых носков Race Expert, размер 43–45.
- **Назначение:** комфорт во время тренировок и активной повседневной жизни.
- **Спорт/дистанция:** бег и общая физическая активность; дистанция не указана.
- **Цена/наличие:** 950 грн; «Є в наявності».
- **Вес покупателя:** не указан; размер обуви 43–45 — отдельный параметр.
- **Теги:** `item_type:apparel`, `purpose:foot_comfort`, `sport:running`, `sport:general_fitness`, `distance:unspecified`, `shoe_size:43-45`, `buyer_weight:not_specified`, `price:950_uah`, `availability:in_stock`.
- **Источник:** [карточка Race Expert](https://raceexpert.com.ua/6700-nabir-bili-shkarpetki-re11023-1-825-grn-re11023-aksesua).

### 12. Nabir_1127 — Набір «Продуктивність на максимум Race Expert Club»

- **Состав:** абонемент Race Expert Club на 3 месяца; комплекс Source Naturals Ultra-Mag, 60 таблеток; Mind Shi 4Mushroom Complex, 60 капсул; 2 батончика Race Expert & DRUMn’BADS с ежовиком, по 40 г.
- **Назначение:** концентрация, выносливость и поддержка нервной системы при высоких нагрузках — по описанию набора.
- **Спорт/дистанция:** физические и умственные нагрузки; конкретный вид спорта и дистанция не указаны.
- **Цена/наличие:** 1 379 грн; «Є в наявності».
- **Вес покупателя:** не указан; 40 г — масса одного батончика.
- **Теги:** `item_type:club_membership_bundle`, `purpose:focus`, `purpose:endurance_support`, `sport:general_fitness`, `distance:not_applicable`, `duration:3_months`, `form:tablets`, `form:capsules`, `form:bars`, `buyer_weight:not_specified`, `price:1379_uah`, `availability:in_stock`.
- **Источник:** [карточка Race Expert](https://raceexpert.com.ua/6601-nabir-produktivnist-na-maksimum-1-835-grn-nabir-1127-vi).

### 13. RE11025 — Набір «Турбота і стиль Race Expert Club»

- **Состав:** абонемент Race Expert Club на 3 месяца; 2 пары тёмных и 2 пары белых носков Race Expert размера 43–45; бутылка 600 мл; брелок Race Expert; витамин D3 Now Foods, 2 000 IU, 120 мягких капсул.
- **Назначение:** сочетание повседневной заботы о здоровье и функциональных аксессуаров для активного образа жизни.
- **Спорт/дистанция:** конкретный вид спорта и дистанция не указаны.
- **Цена/наличие:** 1 500 грн; «Є в наявності».
- **Вес покупателя:** не указан; размер обуви и объём бутылки — отдельные характеристики.
- **Теги:** `item_type:club_membership_bundle`, `purpose:active_daily_lifestyle`, `sport:not_sport_specific`, `distance:not_applicable`, `duration:3_months`, `contains:vitamin_d3`, `shoe_size:43-45`, `package_volume:600_ml`, `buyer_weight:not_specified`, `price:1500_uah`, `availability:in_stock`.
- **Источник:** [карточка Race Expert](https://raceexpert.com.ua/6838-nabir-turbota-i-stil-re11025-2-029-grn-re11025-podarunk).

### 14. RE11812 — Набір «Опора руху Race Expert Club»

- **Состав:** абонемент Race Expert Club на 3 месяца; Life Extension Bone Restore, 120 капсул; куркума Swanson, 720 мг, 30 капсул; витамин D3 Now Foods, 2 000 IU, 30 мягких капсул.
- **Назначение:** поддержка костей, суставов и мышц — по описанию сайта.
- **Спорт/дистанция:** конкретный вид спорта и дистанция не указаны.
- **Цена/наличие:** 1 269 грн; «Є в наявності».
- **Вес покупателя:** не указан.
- **Теги:** `item_type:club_membership_bundle`, `purpose:bone_joint_support_claim`, `sport:not_sport_specific`, `distance:not_applicable`, `duration:3_months`, `form:capsules`, `contains:turmeric`, `contains:vitamin_d3`, `buyer_weight:not_specified`, `price:1269_uah`, `availability:in_stock`.
- **Источник:** [карточка Race Expert](https://raceexpert.com.ua/6970-nabir-opora-ruhu-re11812-1-619-grn-re11812-sila-i-masa).

### 15. Nabir_1123 — Набір «Комплект для гідратації Race Expert Club»

- **Состав:** абонемент Race Expert Club на 3 месяца; 16 стиков Hydria Perform; бутылка Race Expert, 600 мл.
- **Назначение и активность:** поддержка гидратации во время тренировок и в повседневной активности, по описанию набора.
- **Дистанция:** не указана.
- **Цена/наличие:** 1 435 грн; «Є в наявності».
- **Вес покупателя:** не указан; бутылка 600 мл — объём товара.
- **Теги:** `item_type:club_membership_bundle`, `purpose:hydration`, `sport:general_fitness`, `distance:not_applicable`, `duration:3_months`, `contains:electrolytes`, `package_volume:600_ml`, `buyer_weight:not_specified`, `price:1435_uah`, `availability:in_stock`.
- **Источник:** [карточка Race Expert](https://raceexpert.com.ua/6552-nabir-komplekt-dlya-gidrataciyi-1-558-grn-nabir-1123-na).

### 16. RE88955 — Набір «Активне довголіття Race Expert Club»

- **Состав:** абонемент Race Expert Club на 3 месяца; Mind Shi 4Mushroom Complex, 60 капсул; Swanson Balance B-50 Complex, 100 капсул.
- **Назначение:** ежедневная поддержка обмена веществ, нервной системы и концентрации — по описанию карточки.
- **Спорт/дистанция:** конкретный вид спорта и дистанция не указаны.
- **Цена/наличие:** 1 425 грн; «Є в наявності».
- **Вес покупателя:** не указан.
- **Теги:** `item_type:club_membership_bundle`, `purpose:general_wellness`, `purpose:focus`, `sport:not_sport_specific`, `distance:not_applicable`, `duration:3_months`, `form:capsules`, `buyer_weight:not_specified`, `price:1425_uah`, `availability:in_stock`.
- **Источник:** [карточка Race Expert](https://raceexpert.com.ua/7013-nabir-aktivne-dovgolittya-re88955-1-565-grn-re88955-sho).

### 17. RE11808 — Набір «Щоденний захист Race Expert Club»

- **Состав:** абонемент Race Expert Club на 3 месяца; экстракт шиитаке Mind Shi, 60 капсул; витамин C с биофлавоноидами Solaray, 100 капсул; витамин D3 Now Foods, 2 000 IU, 30 мягких капсул.
- **Назначение:** поддержка иммунитета и общего самочувствия — по описанию сайта.
- **Спорт/дистанция:** конкретный вид спорта и дистанция не указаны.
- **Цена/наличие:** 1 500 грн; «Є в наявності».
- **Вес покупателя:** не указан.
- **Теги:** `item_type:club_membership_bundle`, `purpose:immune_support_claim`, `purpose:general_wellness`, `sport:not_sport_specific`, `distance:not_applicable`, `duration:3_months`, `form:capsules`, `contains:shiitake`, `contains:vitamin_c`, `contains:vitamin_d3`, `buyer_weight:not_specified`, `price:1500_uah`, `availability:in_stock`.
- **Источник:** [карточка Race Expert](https://raceexpert.com.ua/6955-nabir-shodennij-zahist-re11808-1-609-grn-re11808-shoden).

### 18. RE89017 — Набір «Вечірній ритуал Race Expert Club»

- **Состав:** абонемент Race Expert Club на 3 месяца; рейши Mind Shi, 1 000 мг, 60 капсул; мелатонин Swanson, 3 мг, 120 капсул; комплекс Source Naturals Ultra-Mag, 60 таблеток.
- **Назначение:** вечернее расслабление и переход к отдыху — по описанию набора.
- **Спорт/дистанция:** конкретный вид спорта и дистанция не указаны.
- **Цена/наличие:** 1 425 грн; «Є в наявності».
- **Вес покупателя:** не указан.
- **Теги:** `item_type:club_membership_bundle`, `purpose:relaxation`, `purpose:sleep_support_claim`, `sport:not_sport_specific`, `distance:not_applicable`, `duration:3_months`, `form:capsules`, `form:tablets`, `contains:melatonin`, `contains:magnesium`, `buyer_weight:not_specified`, `price:1425_uah`, `availability:in_stock`.
- **Источник:** [карточка Race Expert](https://raceexpert.com.ua/7028-nabir-vechirnij-ritual-re89017-1-615-grn-re89017-shoden).

### 19. Nabir_1015 — Набір «Електролітний запас Race Expert Club»

- **Состав:** абонемент Race Expert Club на 3 месяца; 20 стиков Hydria Perform.
- **Назначение и активность:** гидратация и поддержка водно-солевого баланса при интенсивных физических нагрузках, жаре и потоотделении; описание адресовано спортсменам и военным.
- **Дистанция:** не указана.
- **Цена/наличие:** 1 500 грн; «Є в наявності».
- **Вес покупателя:** не указан.
- **Дополнительно:** каждый стик разводится в 500–850 мл воды по инструкции на карточке; это приводится как текст источника, не как персональная рекомендация.
- **Теги:** `item_type:club_membership_bundle`, `purpose:hydration`, `purpose:endurance_support`, `sport:general_fitness`, `distance:not_applicable`, `duration:3_months`, `contains:electrolytes`, `contains:amino_acids`, `buyer_weight:not_specified`, `price:1500_uah`, `availability:in_stock`.
- **Источник:** [карточка Race Expert](https://raceexpert.com.ua/5502-nabir-elektrolitnij-zapas-1-660-grn-nabir-1015-son-i-vi).

### 20. RE88938 — Набір «За кермом Race Expert Club»

- **Состав:** абонемент Race Expert Club на 3 месяца; Mind Shi 4Mushroom Complex, 60 капсул; Swanson Balance B-50 Complex, 100 капсул.
- **Назначение и аудитория:** поддержка концентрации, ясности мышления и спокойствия во время длительных поездок; набор адресован водителям.
- **Спорт/дистанция:** не спортивный набор; дистанция бега не применима.
- **Цена/наличие:** 1 425 грн; «Є в наявності».
- **Вес покупателя:** не указан.
- **Теги:** `item_type:club_membership_bundle`, `purpose:focus`, `audience:drivers`, `sport:not_sport_specific`, `distance:not_applicable`, `duration:3_months`, `form:capsules`, `buyer_weight:not_specified`, `price:1425_uah`, `availability:in_stock`.
- **Источник:** [карточка Race Expert](https://raceexpert.com.ua/7003-nabir-za-kermom-re88938-1-585-grn-re88938-fokus-i-produ).

### 21. RE89366 — Набір «Три опори здоров’я»

- **Состав:** абонемент Race Expert Club на 3 месяца; витамин D3 Now Foods, 2 000 IU, 120 мягких капсул, 2 упаковки; Omega-3 Now Foods, 1 000 мг, 30 мягких капсул; цинк пиколинат Swanson, 22 мг, 60 капсул; небольшой чёрный органайзер.
- **Назначение:** ежедневное дополнение рациона и удобное хранение добавок — по описанию набора.
- **Спорт/дистанция:** конкретный вид спорта и дистанция не указаны.
- **Цена/наличие:** 1 435 грн; «Є в наявності».
- **Вес покупателя:** не указан.
- **Теги:** `item_type:club_membership_bundle`, `purpose:general_wellness`, `sport:not_sport_specific`, `distance:not_applicable`, `duration:3_months`, `contains:vitamin_d3`, `contains:omega_3`, `contains:zinc`, `buyer_weight:not_specified`, `price:1435_uah`, `availability:in_stock`.
- **Источник:** [карточка Race Expert](https://raceexpert.com.ua/7138-nabir-tri-opori-zdorovya-abonement-na-3-misyaci-re89366).

### 22. RE88973 — Набір «Щоденна база для офісу Race Expert Club»

- **Состав:** абонемент Race Expert Club на 3 месяца; мультивитамины Now Foods Daily Vits Multi, 30 капсул; витамин D3 Now Foods, 2 000 IU, 120 мягких капсул; Mind Shi 4Mushroom Complex, 60 капсул.
- **Назначение и аудитория:** ежедневное дополнение рациона в течение насыщенного рабочего дня; название адресует набор офисным работникам.
- **Спорт/дистанция:** конкретный вид спорта и дистанция не указаны.
- **Цена/наличие:** 1 349 грн; «Є в наявності».
- **Вес покупателя:** не указан.
- **Теги:** `item_type:club_membership_bundle`, `purpose:daily_nutrition_support`, `audience:office_workers`, `sport:not_sport_specific`, `distance:not_applicable`, `duration:3_months`, `form:capsules`, `buyer_weight:not_specified`, `price:1349_uah`, `availability:in_stock`.
- **Источник:** [карточка Race Expert](https://raceexpert.com.ua/7024-nabir-shodenna-baza-dlya-ofisu-re88973-1-549-grn-re8897).

### 23. RE11742 — Набір «Спортивний фундамент» 2.0

- **Состав:** по перечню товаров — абонемент Race Expert Club на 3 месяца; креатин Bodyperson Labs Creatine Monohydrate, 500 г; витамин D3 Now Foods, 2 000 IU, 120 мягких капсул; Omega-3 Now Foods, 1 000 мг, 30 мягких капсул, 2 упаковки.
- **Назначение и спорт:** силовые/функциональные тренировки, сила и восстановление — карточка также описывает набор как основу для спортивного прогресса.
- **Дистанция:** не применима.
- **Цена каталога:** 1 295 грн; официальная карточка при перепроверке 2026-11-06 показывает 1 500 грн. Наличие на странице отмечено «Є в наявності».
- **Вес покупателя:** не указан; 500 г — масса упаковки креатина.
- **Расхождение источника:** вводный текст упоминает магний и комплекс D3+K2, но подробный перечень показывает D3 и Omega-3, без магния и K2. Состав требует повторной сверки перед использованием в правилах подбора.
- **Теги:** `item_type:club_membership_bundle`, `purpose:strength_training_support`, `purpose:recovery_support_claim`, `sport:strength_training`, `sport:functional_training`, `distance:not_applicable`, `duration:3_months`, `contains:creatine`, `contains:vitamin_d3`, `contains:omega_3`, `package_weight:500_g`, `buyer_weight:not_specified`, `price:1295_uah`, `availability:in_stock`, `data_quality:composition_conflict`, `data_quality:live_price_differs`.
- **Источник:** [карточка Race Expert](https://raceexpert.com.ua/6888-nabir-sportivnij-fundament-20-re11742-1-615-grn-re11742).

### 24. RE11513 — Набір «Енергія і очищення Race Expert Club»

- **Состав:** абонемент Race Expert Club на 3 месяца; органическая спирулина Now Foods, 500 мг, 100 таблеток; цинк пиколинат Now Foods, 50 мг, 60 капсул; 5 стиков Hydria Perform; Omega-3 Now Foods, 1 000 мг, 30 мягких капсул, 2 упаковки.
- **Назначение:** ежедневная поддержка организма и энергии в активном ритме; описание также упоминает иммунитет, гидратацию и общее самочувствие.
- **Спорт/дистанция:** регулярные тренировки упомянуты в описании абонемента; конкретный вид спорта и дистанция для набора не заданы.
- **Цена/наличие:** 1 455 грн; «Є в наявності».
- **Вес покупателя:** не указан.
- **Теги:** `item_type:club_membership_bundle`, `purpose:daily_nutrition_support`, `purpose:hydration`, `sport:not_sport_specific`, `distance:not_applicable`, `duration:3_months`, `form:tablets`, `form:capsules`, `contains:spirulina`, `contains:zinc`, `contains:electrolytes`, `contains:omega_3`, `buyer_weight:not_specified`, `price:1455_uah`, `availability:in_stock`.
- **Источник:** [карточка Race Expert](https://raceexpert.com.ua/6761-nabir-energiya-i-ochishennya-re11513-1-805-grn-re11513).

### Записи 25–75

25. **RE11021** — Набір «Літній старт Race Expert Club» — абонемент на 3 місяці. Цена каталога (06.11.2026): **1379 грн**. [Официальная карточка](https://raceexpert.com.ua/6698-nabir-litnij-start-re11021-1-975-grn-re11021-aksesuari). Текущая цена (наблюдение 06.11.2026): **1500 грн** (указана предыдущая цена 1975 грн). Состав: белые носки Race Expert размер 40–44 x2 pairs; glass бутылка Race Expert 530 ml; Hydria Daily peach sticks x8; Hydria Perform lemon sticks x2. Назначение: Гидратация и комфорт во время тренировок и активности в жаркую погоду. Спорт/активность: Общие тренировки; дисциплина не названа. Формат забега/дистанция: Не относится к конкретному забегу; дистанция не применима. Диапазон веса покупателя: не указан. Теги: purpose:hydration_in_heat; sport:training_general; distance:not_applicable; price:1379_uah; buyer_weight:not_specified; item_type:apparel_bundle; item_type:supplement_bundle; item_type:equipment_bundle; item_type:club_membership_bundle; contains:electrolytes; duration:3_months; shoe_size:40-44; data_quality:live_price_differs

26. **RE89019** — Набір «Свіжий фокус і щоденна підтримка Race Expert Club» — абонемент на 3 місяці. Цена каталога (06.11.2026): **1305 грн**. [Официальная карточка](https://raceexpert.com.ua/7030-nabir-svizhij-fokus-i-shodenna-pidtrimka-re89019-1-669). Текущая цена (наблюдение 06.11.2026): **1500 грн** (указана предыдущая цена 1669 грн). Состав: абонемент; Mind Shi 4Mushroom Complex 1000 mg, 60 caps; Swanson B12 500 mcg, 100 caps; NOW Omega-3 1000 mg, 30 мягких капсул; NOW D3 2000 IU, 30 мягких капсул. Назначение: Ежедневная нутритивная поддержка при высокой умственной нагрузке и офисной работе. Спорт/активность: Конкретный вид спорта не указан. Формат забега/дистанция: Не относится к конкретному забегу; дистанция не применима. Диапазон веса покупателя: не указан. Теги: purpose:focus_and_daily_support; sport:not_sport_specific; distance:not_applicable; price:1305_uah; buyer_weight:not_specified; item_type:supplement_bundle; item_type:club_membership_bundle; audience:office_workers; audience:high_mental_load; contains:mushroom_complex; contains:vitamin_b12; contains:omega_3; contains:vitamin_d3; duration:3_months; data_quality:live_price_differs

27. **RE88976** — Набір «Заряд для активного дня». Цена каталога (06.11.2026): **1399 грн**. [Официальная карточка](https://raceexpert.com.ua/7026-nabir-zaryad-dlya-aktivnogo-dnya-re88976-1-505-grn-re88). Текущая цена (наблюдение 06.11.2026): **1500 грн** (указана предыдущая цена 1505 грн). Состав: NOW Methyl B12 1000 mcg, 100 lozenges; Swanson Ashwagandha 450 mg, 100 caps; NOW Zinc Picolinate 50 mg, 60 caps; Olimp L-Carnitine 3000 Extreme Shot, 25 ml. Назначение: Для высокой физической и умственной активности; в карточке названы спортсмены. Спорт/активность: Физическая активность; дисциплина не названа. Формат забега/дистанция: Не относится к конкретному забегу; дистанция не применима. Диапазон веса покупателя: не указан. Теги: purpose:active_day_energy; sport:physical_activity_general; distance:not_applicable; price:1399_uah; buyer_weight:not_specified; item_type:supplement_bundle; audience:athletes; audience:high_activity; contains:vitamin_b12; contains:ashwagandha; contains:zinc; contains:l_carnitine; data_quality:live_price_differs

28. **RE89489** — Набір «Основа регулярних тренувань» — абонемент на 3 місяці. Цена каталога (06.11.2026): **1500 грн**. [Официальная карточка](https://raceexpert.com.ua/7173-nabir-osnova-regulyarnih-trenuvan-abonement-na-3-misyac). Текущая цена (наблюдение 06.11.2026): **1500 грн** (указана предыдущая цена 1629 грн). Состав: абонемент Race Expert Club на 3 месяца; Race Expert банное полотенце 135 × 70 cm, 100% cotton, 500 g/m²; Nutriversum мини-шейкер 300 ml; Lipobar протеиновые батончики 50 g x6 chocolate and x6 pistachio. Назначение: Для регулярных тренировок в зале или дома, активного отдыха и белкового перекуса после нагрузки. Спорт/активность: Тренировки в зале и дома. Формат забега/дистанция: Не относится к конкретному забегу; дистанция не применима. Диапазон веса покупателя: не указан. Теги: purpose:regular_training; sport:training_general; distance:not_applicable; price:1500_uah; buyer_weight:not_specified; item_type:snack_bundle; item_type:equipment_bundle; item_type:club_membership_bundle; audience:gym; audience:home_training; audience:active_recreation; contains:protein; duration:3_months

29. **RE89488** — Набір «Силовий прогрес» — абонемент на 3 місяці. Цена каталога (06.11.2026): **1500 грн**. [Официальная карточка](https://raceexpert.com.ua/7172-nabir-silovij-progres-abonement-na-3-misyaci-re89488-1). Текущая цена (наблюдение 06.11.2026): **1500 грн** (указана предыдущая цена 1549 грн). Состав: абонемент Race Expert Club на 3 месяца; Myprotein Creatine Monohydrate 500 g; Fitly шейкер with органайзер для таблеток, 600 ml/7 compartments. Назначение: Для силового прогресса и работы над мышечной массой; названы спортсмены и посетители зала. Спорт/активность: Силовые тренировки. Формат забега/дистанция: Не относится к конкретному забегу; дистанция не применима. Диапазон веса покупателя: не указан. Теги: purpose:strength_progress; sport:strength_training; distance:not_applicable; price:1500_uah; buyer_weight:not_specified; item_type:supplement_bundle; item_type:equipment_bundle; item_type:club_membership_bundle; audience:athletes; audience:gym_users; contains:creatine; duration:3_months

30. **RE88961** — Набір «Креатин і відновлення Race Expert Club» — абонемент на 3 місяці. Цена каталога (06.11.2026): **1415 грн**. [Официальная карточка](https://raceexpert.com.ua/7019-nabir-kreatin-i-vidnovlennya-re88961-1-519-grn-re88961). Текущая цена (наблюдение 06.11.2026): **1500 грн** (указана предыдущая цена 1519 грн). Состав: абонемент Race Expert Club на 3 месяца; OstroVit Creatine Monohydrate, 500 g; Swanson Triple Magnesium, 400 mg, 100 caps; Nutriversum мини-шейкер, 300 ml; Lipobar, 50 g x2; Hydria Daily stick x1. Назначение: Поддержка восстановления и силы после нагрузки; в карточке названы спортсмены. Спорт/активность: Дисциплина не указана. Формат забега/дистанция: Не относится к конкретному забегу; дистанция не применима. Диапазон веса покупателя: не указан. Теги: purpose:creatine_and_recovery; sport:not_sport_specific; distance:not_applicable; price:1415_uah; buyer_weight:not_specified; item_type:snack_bundle; item_type:supplement_bundle; item_type:equipment_bundle; item_type:club_membership_bundle; contains:creatine; contains:magnesium; contains:protein; contains:electrolytes; duration:3_months; data_quality:live_price_differs

31. **RE88934** — Набір «Регулярний зал Race Expert Club» — абонемент на 3 місяці. Цена каталога (06.11.2026): **1449 грн**. [Официальная карточка](https://raceexpert.com.ua/7002-nabir-regulyarnij-zal-re88934-1-500-grn-re88934-sila-i). Текущая цена (наблюдение 06.11.2026): **1500 грн** (указана предыдущая цена 1545 грн). Состав: абонемент Race Expert Club на 3 месяца; OstroVit Creatine Monohydrate, 500 g; Lipobar протеиновые батончики, 50 g: гранат x8 (16.5 g protein and 6.7 g fiber each), апельсин x7 (16.5 g protein and 7.4 g fiber each). Назначение: Для людей, регулярно посещающих зал и тренирующихся. Спорт/активность: Тренировки в зале/силовые тренировки. Формат забега/дистанция: Не относится к конкретному забегу; дистанция не применима. Диапазон веса покупателя: не указан. Теги: purpose:regular_gym_training; sport:gym_training; distance:not_applicable; price:1449_uah; buyer_weight:not_specified; item_type:snack_bundle; item_type:supplement_bundle; item_type:club_membership_bundle; contains:creatine; contains:protein; duration:3_months; data_quality:live_price_differs

32. **RE11810** — Набір «Міцні кістки Race Expert Club» — абонемент на 3 місяці. Цена каталога (06.11.2026): **1419 грн**. [Официальная карточка](https://raceexpert.com.ua/6957-nabir-micni-kistki-re11810-1-585-grn-re11810-sila-i-mas). Текущая цена (наблюдение 06.11.2026): **1500 грн** (указана предыдущая цена 1585 грн). Состав: абонемент Race Expert Club на 3 месяца; Nature’s Plus Animal Parade Calcium Chewable, 135 chewables; Solaray Vitamin K2 MK-7 50 mcg, 30 caps; NOW D3 2000 IU, 30 мягких капсул. Назначение: Поддержка костей; названы дети, взрослые, спортсмены и люди с физическими нагрузками. Спорт/активность: Упоминаются физические нагрузки; дисциплина не названа. Формат забега/дистанция: Не относится к конкретному забегу; дистанция не применима. Диапазон веса покупателя: не указан. Теги: purpose:bone_support; sport:physical_activity_general; distance:not_applicable; price:1419_uah; buyer_weight:not_specified; item_type:supplement_bundle; item_type:club_membership_bundle; audience:children; audience:adults; audience:athletes; contains:calcium; contains:vitamin_k2; contains:vitamin_d3; duration:3_months; data_quality:live_price_differs

33. **RE11680** — Набір «Силовий старт». Цена каталога (06.11.2026): **759 грн**. [Официальная карточка](https://raceexpert.com.ua/6874-nabir-silovij-start-re11680-1-949-grn-re11680-sila-i-ma). Текущая цена (наблюдение 06.11.2026): **1500 грн** (указана предыдущая цена 1585 грн). Состав: MIAMI VIBES PURE Creatine Monohydrate 300 g; NOW D3 2000 IU, 120 мягких капсул; Lipobar протеиновые батончики 50 g x2. Назначение: Для начала силовых тренировок, развития силы и мышечной массы и восстановления. Спорт/активность: Силовые тренировки. Формат забега/дистанция: Не относится к конкретному забегу; дистанция не применима. Диапазон веса покупателя: не указан. Теги: purpose:strength_training_start; sport:strength_training; distance:not_applicable; price:759_uah; buyer_weight:not_specified; item_type:snack_bundle; item_type:supplement_bundle; contains:creatine; contains:vitamin_d3; contains:protein; data_quality:live_price_differs

34. **Nabir_1119** — Набір «Ритм твого руху». Цена каталога (06.11.2026): **1500 грн**. [Официальная карточка](https://raceexpert.com.ua/6839-nabir-ritm-tvogo-ruhu-nabir-1119-1-875-grn-nabir-1119-g). Текущая цена (наблюдение 06.11.2026): **1500 грн** (указана предыдущая цена 1875 грн). Состав: white and тёмные носки Race Expert размер 40–42; Race Expert Run for Help Ukraine кепка; бутылка 600 ml; Myprotein Baked Cookie 75 g x3 (13 g protein each). Назначение: Комфорт, гидратация и защита от солнца; названы военнослужащие, спортсмены и активные люди. Спорт/активность: Спорт и физическая активность в целом; дисциплина не названа. Формат забега/дистанция: Не относится к конкретному забегу; дистанция не применима. Диапазон веса покупателя: не указан. Теги: purpose:movement_and_training_comfort; sport:physical_activity_general; distance:not_applicable; price:1500_uah; buyer_weight:not_specified; item_type:apparel_bundle; item_type:snack_bundle; item_type:equipment_bundle; audience:military; audience:athletes; contains:protein; shoe_size:40-42

35. **RE11661** — Набір «Чоловіча база залу Race Expert Club» — абонемент на 3 місяці. Цена каталога (06.11.2026): **1485 грн**. [Официальная карточка](https://raceexpert.com.ua/6832-nabir-cholovicha-baza-zalu-re11661-1-789-grn-re11661-fo). Текущая цена (наблюдение 06.11.2026): **1500 грн** (указана предыдущая цена 1789 грн). Состав: абонемент Race Expert Club на 3 месяца; NOW Daily Vits Multi, 100 таблеток; OstroVit Creatine Monohydrate, 500 g; Lipobar, 50 g x1. Назначение: Базовый набор для мужчин, регулярно тренирующихся в зале. Спорт/активность: Тренировки в зале. Формат забега/дистанция: Не относится к конкретному забегу; дистанция не применима. Диапазон веса покупателя: не указан. Теги: purpose:men_gym_base; sport:gym_training; distance:not_applicable; price:1485_uah; buyer_weight:not_specified; item_type:snack_bundle; item_type:supplement_bundle; item_type:club_membership_bundle; audience:men; contains:creatine; contains:protein; duration:3_months; data_quality:live_price_differs

36. **RE11652** — Набір «Боротьба з кріпатурою». Цена каталога (06.11.2026): **1500 грн**. [Официальная карточка](https://raceexpert.com.ua/6824-nabir-borotbi-z-kripaturoyu-re11652-1-519-grn-re11652-s). Текущая цена (наблюдение 06.11.2026): **1500 грн** (указана предыдущая цена 1559 грн). Состав: Swanson Triple Magnesium Complex 400 mg, 100 caps; Hydria Perform стики с электролитами x5. Назначение: Для восстановления после тренировок и физической нагрузки. Спорт/активность: Тренировки в целом; дисциплина не названа. Формат забега/дистанция: Не относится к конкретному забегу; дистанция не применима. Диапазон веса покупателя: не указан. Теги: purpose:post_exercise_recovery; sport:not_sport_specific; distance:not_applicable; price:1500_uah; buyer_weight:not_specified; item_type:supplement_bundle; contains:magnesium; contains:electrolytes

37. **RE11637** — Набір «Сила + паливо» — абонемент на 3 місяці. Цена каталога (06.11.2026): **1275 грн**. [Официальная карточка](https://raceexpert.com.ua/6820-nabir-sila-palivo-re11637-1-569-grn-re11637-sila-i-masa). Текущая цена (наблюдение 06.11.2026): **1500 грн** (указана предыдущая цена 1569 грн). Состав: абонемент; Bodyperson Creatine Monohydrate 500 g; Sponser Crunchy Protein Bar 50 g x2. Назначение: Поддержка силовых тренировок и питания. Спорт/активность: Силовые тренировки. Формат забега/дистанция: Не относится к конкретному забегу; дистанция не применима. Диапазон веса покупателя: не указан. Теги: purpose:strength_and_fueling; sport:strength_training; distance:not_applicable; price:1275_uah; buyer_weight:not_specified; item_type:snack_bundle; item_type:supplement_bundle; item_type:club_membership_bundle; contains:creatine; contains:protein; duration:3_months; data_quality:live_price_differs

38. **RE11636** — Набір «Вибух сили Race Expert Club» — абонемент на 3 місяці. Цена каталога (06.11.2026): **1385 грн**. [Официальная карточка](https://raceexpert.com.ua/6819-nabir-vibuh-sili-re11636-1-609-grn-re11636-sila-i-masa). Текущая цена (наблюдение 06.11.2026): **1500 грн** (указана предыдущая цена 1609 грн). Состав: абонемент; OstroVit Creatine Monohydrate 500 g; Bodyperson Labs Pre-Workout Formula 250 g (contains caffeine per card); Hydria Daily sticks x4. Назначение: Для интенсивных тренировок, силы и спортивной работоспособности. Спорт/активность: Интенсивные тренировки; дисциплина не названа. Формат забега/дистанция: Не относится к конкретному забегу; дистанция не применима. Диапазон веса покупателя: не указан. Теги: purpose:training_strength_and_performance; sport:intense_training; distance:not_applicable; price:1385_uah; buyer_weight:not_specified; item_type:supplement_bundle; item_type:club_membership_bundle; contains:creatine; contains:caffeine; contains:electrolytes; duration:3_months; data_quality:live_price_differs

39. **RE11783** — Набір "Запорука сили" — абонемент на 3 місяці. Цена каталога (06.11.2026): **1500 грн**. [Официальная карточка](https://raceexpert.com.ua/6915-nabir-re11783-1-525-grn-re11783-sila-i-masa). Текущая цена (наблюдение 06.11.2026): **1500 грн** (указана предыдущая цена 1525 грн). Состав: абонемент Race Expert Club на 3 месяца; OstroVit Creatine Monohydrate orange, 500 g; Nutriversum BCAA 2:1:1 Sugar Free, 500 g. Назначение: Для поддержки силовых тренировок. Спорт/активность: Силовые тренировки. Формат забега/дистанция: Не относится к конкретному забегу; дистанция не применима. Диапазон веса покупателя: не указан. Теги: purpose:strength_support; sport:strength_training; distance:not_applicable; price:1500_uah; buyer_weight:not_specified; item_type:supplement_bundle; item_type:club_membership_bundle; audience:athletes; contains:creatine; contains:bcaa; duration:3_months

40. **RE11681** — Набір «Ріст м'язів» — абонемент на 3 місяці. Цена каталога (06.11.2026): **1225 грн**. [Официальная карточка](https://raceexpert.com.ua/6875-nabir-rist-myaziv-re11681-1-995-grn-re11681-sila-i-masa). Текущая цена (наблюдение 06.11.2026): **1500 грн** (указана предыдущая цена 1995 грн). Состав: абонемент; Lipobar протеиновый батончик 50 g x2 (16.5 g protein each); Bodyperson Creatine Monohydrate 500 g; Brave U шейкер 700 ml; Hydria Daily sticks x4. Назначение: Для работы над ростом мышц. Спорт/активность: Силовые тренировки. Формат забега/дистанция: Не относится к конкретному забегу; дистанция не применима. Диапазон веса покупателя: не указан. Теги: purpose:muscle_growth_support; sport:strength_training; distance:not_applicable; price:1225_uah; buyer_weight:not_specified; item_type:snack_bundle; item_type:supplement_bundle; item_type:equipment_bundle; item_type:club_membership_bundle; contains:creatine; contains:protein; contains:electrolytes; duration:3_months; data_quality:live_price_differs

41. **RE11518** — Набір «Більше сили на тренуванні» по програмі "Ветеранський спорт" — абонемент на 3 місяці. Цена каталога (06.11.2026): **1335 грн**. [Официальная карточка](https://raceexpert.com.ua/6784-nabir-bilshe-sili-na-trenuvanni-0-grn-re11518). Текущая цена (наблюдение 06.11.2026): **1500 грн** (указана предыдущая цена 2139 грн). Состав: MIAMI VIBES PURE Creatine Monohydrate, 300 g; Nutriversum 2:1:1 BCAA Sugar Free, 360 g. Во вступлении упоминается шейкер, которого нет в нумерованном списке товаров. Назначение: Поддержка силовых тренировок; названы спортсмены и бодибилдеры. Спорт/активность: Силовые тренировки. Формат забега/дистанция: Не относится к конкретному забегу; дистанция не применима. Диапазон веса покупателя: не указан. Теги: data_quality:intro_list_mismatch; purpose:strength_training_support; sport:strength_training; distance:not_applicable; price:1335_uah; buyer_weight:not_specified; item_type:supplement_bundle; item_type:club_membership_bundle; audience:athletes; audience:bodybuilders; contains:creatine; contains:bcaa; duration:3_months; data_quality:live_price_differs

42. **RE88952** — Набір «Антиоксидантний ресурс Race Expert Club» — абонемент на 3 місяці. Цена каталога (06.11.2026): **1385 грн**. [Официальная карточка](https://raceexpert.com.ua/7018-nabir-antioksidantnij-resurs-re88952-1-619-grn-re88952). Состав: абонемент Race Expert Club на 3 месяца; Mind Shi 4Mushroom 1000 mg, 60 caps; NOW Selenium 100 mcg, 100 tabs; NOW Organic Spirulina 500 mg, 100 tabs. Назначение: Антиоксидантная поддержка для спортсменов и активных людей при физических и умственных нагрузках. Спорт/активность: Конкретный вид спорта не указан. Формат забега/дистанция: Не относится к конкретному забегу; дистанция не применима. Диапазон веса покупателя: не указан. Теги: purpose:antioxidant_support; sport:not_sport_specific; distance:not_applicable; price:1385_uah; buyer_weight:not_specified; item_type:supplement_bundle; item_type:club_membership_bundle; audience:athletes; audience:active_people; contains:mushroom_complex; contains:selenium; contains:spirulina; duration:3_months

43. **RE88950** — Набір «Щоденна імунна база». Цена каталога (06.11.2026): **1459 грн**. [Официальная карточка](https://raceexpert.com.ua/7010-nabir-shodenna-imunna-baza-re88950-1-529-grn-re88950-sh). Состав: Mind Shi 4Mushroom 1000 mg, 60 caps; UltraVit C 1000 mg, 60 caps; NOW D3 2000 IU, 30 softgels. Назначение: Ежедневная иммунная поддержка активных людей. Спорт/активность: Конкретный вид спорта не указан. Формат забега/дистанция: Не относится к конкретному забегу; дистанция не применима. Диапазон веса покупателя: не указан. Теги: purpose:daily_immune_support; sport:not_sport_specific; distance:not_applicable; price:1459_uah; buyer_weight:not_specified; item_type:supplement_bundle; audience:active_people; contains:mushroom_complex; contains:vitamin_c; contains:vitamin_d3

44. **RE11650** — Набір «Захист від спеки» по програмі "Ветеранський спорт". Цена каталога (06.11.2026): **1239 грн**. [Официальная карточка](https://raceexpert.com.ua/6822-nabir-zahist-vid-speki-re11650-1-559-grn-re11650-shoden). Текущая цена (наблюдение 06.11.2026): **1500 грн** (указана предыдущая цена 1559 грн). Состав: Precision Hydration 1000 Tube, 10 таблеток; Precision Fuel & Hydration капсулы с электролитами, 15 caps. Назначение: Гидратация при тренировках в жару и обильном потоотделении; названы спортсмены, бегуны, велосипедисты и люди, тренирующиеся в таких условиях. Спорт/активность: Бег и велоспорт. Формат забега/дистанция: Гоночный формат не указан; набор предназначен для тренировок в жару. Диапазон веса покупателя: не указан. Показатель применения: карточка приводит дозировку капсул для активности дольше 90 минут; это длительность активности, не гоночная дистанция. Теги: purpose:heat_protection_and_hydration; sport:running; sport:cycling; distance:not_applicable; price:1239_uah; buyer_weight:not_specified; item_type:supplement_bundle; audience:athletes; audience:runners; audience:cyclists; contains:electrolytes; data_quality:live_price_differs

45. **Nabir_1122** — Набір «Для імунітету Race Expert Club» — абонемент на 3 місяці. Цена каталога (06.11.2026): **1465 грн**. [Официальная карточка](https://raceexpert.com.ua/6418-nabir-dlya-imunitetu-2-137-grn-nabir-1122-nabori). Текущая цена (наблюдение 06.11.2026): **1500 грн** (указана предыдущая цена 2137 грн). Состав: абонемент Race Expert Club на 3 месяца; Mind Shi Chaga Mushroom, 1000 mg; Mind Shi 4Mushroom Complex, 1000 mg. Назначение: Иммунная и адаптогенная поддержка, восстановление. Спорт/активность: Конкретный вид спорта не указан. Формат забега/дистанция: Не относится к конкретному забегу; дистанция не применима. Диапазон веса покупателя: не указан. Теги: purpose:immune_support; sport:not_sport_specific; distance:not_applicable; price:1465_uah; buyer_weight:not_specified; item_type:supplement_bundle; item_type:club_membership_bundle; audience:active_people; contains:mushroom_complex; duration:3_months; data_quality:live_price_differs

46. **RE89031** — Набір «Імунітет і тонус». Цена каталога (06.11.2026): **1500 грн**. [Официальная карточка](https://raceexpert.com.ua/7035-nabir-imunitet-i-tonus-re89031-1-515-grn-re89031-shoden). Текущая цена (наблюдение 06.11.2026): **1500 грн** (указана предыдущая цена 1515 грн). Состав: Life Extension D3 25 mcg/1000 IU, 90 мягких капсул; Swanson C-500 with rose hips, 500 mg, 100 caps; NOW Zinc Picolinate, 50 mg, 60 caps. В начале описания упоминается B12, но в нумерованном списке товаров указаны только эти три позиции. Назначение: Поддержка иммунитета и тонуса. Спорт/активность: Конкретный вид спорта не указан. Формат забега/дистанция: Не относится к конкретному забегу; дистанция не применима. Диапазон веса покупателя: не указан. Теги: purpose:immune_and_tone_support; sport:not_sport_specific; distance:not_applicable; price:1500_uah; buyer_weight:not_specified; item_type:supplement_bundle; contains:vitamin_d3; contains:vitamin_c; contains:zinc; data_quality:intro_list_mismatch

47. **RE11820** — Набір «Клітинний захист». Цена каталога (06.11.2026): **1269 грн**. [Официальная карточка](https://raceexpert.com.ua/6972-nabir-klitinnij-zahist-re11820-1-775-grn-re11820-shoden). Состав: NOW Natural Beta Carotene 25,000 IU, 90 softgels; NOW Green Tea Extract 400 mg, 100 caps. Назначение: Антиоксидантная поддержка для спортсменов и людей с активным образом жизни. Спорт/активность: Конкретный вид спорта не указан. Формат забега/дистанция: Не относится к конкретному забегу; дистанция не применима. Диапазон веса покупателя: не указан. Теги: purpose:antioxidant_support; sport:not_sport_specific; distance:not_applicable; price:1269_uah; buyer_weight:not_specified; item_type:supplement_bundle; audience:athletes; audience:active_people; contains:beta_carotene; contains:green_tea_extract

48. **RE11809** — Набір «Антиоксидантний захист» — абонемент на 3 місяці. Цена каталога (06.11.2026): **1375 грн**. [Официальная карточка](https://raceexpert.com.ua/6959-nabir-antioksidantnij-zahist-re11809-1-625-grn-re11809). Состав: абонемент Race Expert Club на 3 месяца; NOW Astaxanthin 4 mg, 60 softgels; Swanson Turmeric 720 mg, 30 caps; NOW D3 2000 IU, 30 softgels; стеклянная бутылка 530 мл. Назначение: Антиоксидантная поддержка для спортсменов и активных людей. Спорт/активность: Конкретный вид спорта не указан. Формат забега/дистанция: Не относится к конкретному забегу; дистанция не применима. Диапазон веса покупателя: не указан. Теги: purpose:antioxidant_support; sport:not_sport_specific; distance:not_applicable; price:1375_uah; buyer_weight:not_specified; item_type:supplement_bundle; item_type:equipment_bundle; item_type:club_membership_bundle; audience:athletes; audience:active_people; contains:astaxanthin; contains:turmeric; contains:vitamin_d3; duration:3_months

49. **RE11807** — Набір «Антиоксидантна формула» — абонемент на 3 місяці. Цена каталога (06.11.2026): **1369 грн**. [Официальная карточка](https://raceexpert.com.ua/6954-nabir-antioksidantna-formula-re11807-1-629-grn-re11807). Текущая цена (наблюдение 06.11.2026): **1500 грн** (указана предыдущая цена 1629 грн). Состав: абонемент Race Expert Club на 3 месяца; NOW Foods C-1000 Zinc & D-3, 100 caps; Swanson Turmeric, 720 mg, 30 caps; OstroVit Spiruline, 90 таблеток; Race Expert стеклянная бутылка с чехлом, 530 ml. Назначение: Антиоксидантная защита; состав уточнён по официальной карточке. Спорт/активность: Конкретный вид спорта не указан. Формат забега/дистанция: Не относится к конкретному забегу; дистанция не применима. Диапазон веса покупателя: не указан. Примечание: состав вручную разобран по захвату официальной карточки. Теги: data_quality:manual_card_parse; purpose:antioxidant_support; sport:not_sport_specific; distance:not_applicable; price:1369_uah; buyer_weight:not_specified; item_type:supplement_bundle; item_type:equipment_bundle; item_type:club_membership_bundle; contains:vitamin_c; contains:zinc; contains:vitamin_d3; contains:turmeric; contains:spirulina; duration:3_months; data_quality:live_price_differs

50. **RE11817** — Набір «Ясний фокус Race Expert Club» — абонемент на 3 місяці. Цена каталога (06.11.2026): **1255 грн**. [Официальная карточка](https://raceexpert.com.ua/6968-nabir-yasnij-fokus-re11817-1-595-grn-re11817-fokus-i-pr). Состав: абонемент Race Expert Club на 3 месяца; Mind Shi 4Mushroom 1000 mg, 60 caps; NOW Choline & Inositol 250 mg, 100 caps. Назначение: Поддержка фокуса и умственной работы; карточка называет спортсменов и активных людей. Спорт/активность: Конкретный вид спорта не указан. Формат забега/дистанция: Не относится к конкретному забегу; дистанция не применима. Диапазон веса покупателя: не указан. Теги: purpose:focus_and_mental_work_support; sport:not_sport_specific; distance:not_applicable; price:1255_uah; buyer_weight:not_specified; item_type:supplement_bundle; item_type:club_membership_bundle; audience:athletes; audience:active_people; contains:mushroom_complex; contains:choline; duration:3_months

51. **RE11656** — Набір «Фокус - формула Race Expert Club» — абонемент на 3 місяці. Цена каталога (06.11.2026): **1500 грн**. [Официальная карточка](https://raceexpert.com.ua/6827-nabir-fokus-formula-re11656-1-555-grn-re11656-fokus-i-p). Текущая цена (наблюдение 06.11.2026): **1500 грн** (в категории указана предыдущая цена 1545 грн). Состав: абонемент Race Expert Club на 3 месяца; Mind Shi Lion’s Mane, 1000 mg, 60 caps; Swanson Balance B-50 Complex, 100 caps; NOW Omega-3, 1000 mg, 30 softgels. Назначение: поддержка фокуса и концентрации. Спорт/активность: конкретная дисциплина не указана. Формат забега/дистанция: Не относится к конкретному забегу; дистанция не применима. Диапазон веса покупателя: не указан. Теги: purpose:focus_support; sport:not_sport_specific; distance:not_applicable; price:1500_uah; buyer_weight:not_specified; item_type:supplement_bundle; item_type:club_membership_bundle; contains:mushroom_complex; contains:vitamin_b_complex; contains:omega_3; duration:3_months

52. **RE11632** — Набір «Розум і Сила». Цена каталога (06.11.2026): **1215 грн**. [Официальная карточка](https://raceexpert.com.ua/6816-nabir-rozum-i-sila-re11632-1-929-grn-re11632-sila-i-mas). Состав: Mind Shi 4Mushroom 1000 mg, 60 caps; Myprotein Baked Cookie 75 g x7 (14 g растительного белка в каждом). Назначение: Поддержка фокуса и когнитивной работы, а также восстановление мышц после тренировок; названы спортсмены, работники, студенты и путешественники. Спорт/активность: Упоминается восстановление после тренировок; дисциплина не названа. Формат забега/дистанция: Не относится к конкретному забегу; дистанция не применима. Диапазон веса покупателя: не указан. Теги: purpose:focus_and_post_training_recovery; sport:training_general; distance:not_applicable; price:1215_uah; buyer_weight:not_specified; item_type:snack_bundle; audience:athletes; audience:workers; audience:students; audience:travelers; contains:mushroom_complex; contains:protein

53. **Nabir_1107** — Набір «Енергія, витривалість та концентрація Race Expert Club» — абонемент на 3 місяці. Цена каталога (06.11.2026): **1500 грн**. [Официальная карточка](https://raceexpert.com.ua/6094-nabir-energiya-vitrivalist-ta-koncentraciya-2-137-grn-n). Текущая цена (наблюдение 06.11.2026): **1500 грн** (указана предыдущая цена 2137 грн). Состав: абонемент Race Expert Club на 3 месяца; Mind Shi Cordyceps, 1000 mg, 60 caps; Mind Shi Lion’s Mane, 1000 mg, 60 caps. Назначение: Поддержка физической выносливости, энергии и концентрации; названы спортсмены, активные люди и участники программы «Ветеранський спорт» в текущем листинге. Спорт/активность: Выносливость и физическая активность в целом; дисциплина не названа. Формат забега/дистанция: Не относится к конкретному забегу; дистанция не применима. Диапазон веса покупателя: не указан. Теги: purpose:energy_endurance_concentration; sport:physical_activity_general; distance:not_applicable; price:1500_uah; buyer_weight:not_specified; item_type:supplement_bundle; item_type:club_membership_bundle; audience:athletes; audience:active_people; contains:cordyceps; contains:mushroom_complex; duration:3_months

54. **RE11806** — Набір «Енергія дистанції Race Expert Club» — абонемент на 3 місяці. Цена каталога (06.11.2026): **1500 грн**. [Официальная карточка](https://raceexpert.com.ua/6962-nabir-energiya-distanciyi-re11806-1-665-grn-re11806-sil). Текущая цена (наблюдение 06.11.2026): **1500 грн** (указана предыдущая цена 1665 грн). Состав: абонемент Race Expert Club на 3 месяца; DRUMn’BADS liquid cordyceps, 30 ml; Swanson CoQ10 Mini Cap, 10 mg, 100 caps; Precision Hydration 500 Tube, 15 таблеток. Назначение: Энергия и выносливость во время тренировок, бега и велоспорта; поддержка гидратации. Спорт/активность: Бег и велоспорт; тренировки на выносливость. Формат забега/дистанция: Формат забега и точная дистанция не указаны.  Диапазон веса покупателя: не указан. Теги: purpose:energy_for_endurance; sport:running; sport:cycling; distance:unspecified; price:1500_uah; buyer_weight:not_specified; item_type:supplement_bundle; item_type:club_membership_bundle; audience:athletes; audience:active_people; contains:cordyceps; contains:coenzyme_q10; contains:electrolytes; duration:3_months

55. **RE11804** — Набір «Марафонський темп». Цена каталога (06.11.2026): **1500 грн**. [Официальная карточка](https://raceexpert.com.ua/6961-nabir-marafonskij-temp-re11804-2-145-grn-re11804-sila-i). Текущая цена (наблюдение 06.11.2026): **1500 грн** (указана предыдущая цена 2145 грн). Состав: Race Expert Run for Help Ukraine кепка; Race Expert пояс для стартового номера with 6 gel loops; Hydria Perform стики с электролитами x10. Назначение: Подготовка бегунов к марафонам, полумарафонам, длительным пробежкам и тренировкам на выносливость. Спорт/активность: Бег. Формат забега/дистанция: Форматы: марафон и полумарафон; точная дистанция в километрах не указана.  Диапазон веса покупателя: не указан. Теги: purpose:running_preparation; sport:running; race_format:marathon; race_format:half_marathon; distance:unspecified; price:1500_uah; buyer_weight:not_specified; item_type:supplement_bundle; item_type:equipment_bundle; audience:runners; contains:electrolytes

56. **RE11799** — Набір «Підготовка до забігу». Цена каталога (06.11.2026): **1500 грн**. [Официальная карточка](https://raceexpert.com.ua/6949-nabir-pidgotovka-do-zabigu-re11799-1-679-grn-re11799-si). Состав: Race Expert кепка; пояс для стартового номера; бутылка для воды Race Expert, 600 мл; белые носки, размер 40–42. Назначение: Подготовка к забегу и комфорт для начинающих и опытных бегунов. Спорт/активность: Бег. Формат забега/дистанция: Подготовка к забегу указана; формат и дистанция не уточнены.  Диапазон веса покупателя: не указан. Неопределённость: Предыдущая загрузка карточки завершилась cache miss; использован сохранённый захват официальной карточки. Теги: purpose:running_race_preparation; sport:running; distance:unspecified; price:1500_uah; buyer_weight:not_specified; item_type:apparel_bundle; item_type:equipment_bundle; audience:beginner_runners; audience:experienced_runners; shoe_size:40-42; data_quality:live_fetch_unavailable

57. **RE11787** — Набір «Сила та гідратація» — абонемент на 3 місяці. Цена каталога (06.11.2026): **1335 грн**. [Официальная карточка](https://raceexpert.com.ua/6947-nabir-sila-ta-gidrataciya-re11787-1-515-grn-re11787-sil). Текущая цена (наблюдение 06.11.2026): **1500 грн** (указана предыдущая цена 1515 грн). Состав: Hydria Perform sticks x10; OstroVit Creatine Monohydrate orange, 500 g; Olimp BCAA 4000 Extreme Shot orange, 60 ml. Назначение: Для интенсивных тренировок, силы, мышц, гидратации и восстановления. Спорт/активность: Тренировки; дисциплина не названа. Формат забега/дистанция: Не относится к конкретному забегу; дистанция не применима. Диапазон веса покупателя: не указан. Теги: purpose:strength_and_hydration; sport:strength_training; distance:not_applicable; price:1335_uah; buyer_weight:not_specified; item_type:supplement_bundle; item_type:club_membership_bundle; contains:creatine; contains:bcaa; contains:electrolytes; duration:3_months; data_quality:live_price_differs

58. **Nabir_1128** — Набір «Витривалість» — абонемент на 3 місяці. Цена каталога (06.11.2026): **1345 грн**. [Официальная карточка](https://raceexpert.com.ua/6602-nabir-vitrivalist-ta-sila-nabir-1128-1-559-grn-nabir-11). Текущая цена (наблюдение 06.11.2026): **1500 грн** (указана предыдущая цена 1515 грн). Состав: абонемент; OstroVit Creatine Monohydrate orange, 500 g; Race Expert × DRUMn’BADS lion’s-mane протеиновый батончик 40 g; cordyceps протеиновый батончик 40 g; reishi протеиновый батончик 40 g; Hydria Perform sticks x7. Назначение: Поддержка физической и умственной выносливости; названы спортсмены, бегуны и военнослужащие. Спорт/активность: Бег упомянут в описании; формат соревнований не назван. Формат забега/дистанция: Упоминается бег; формат и дистанция не указаны.  Диапазон веса покупателя: не указан. Теги: purpose:endurance_support; sport:running; distance:unspecified; price:1345_uah; buyer_weight:not_specified; item_type:snack_bundle; item_type:supplement_bundle; item_type:club_membership_bundle; audience:athletes; audience:runners; audience:military; contains:creatine; contains:protein; contains:electrolytes; duration:3_months; data_quality:live_price_differs

59. **RE11659** — Набір «Тиждень бігуна». Цена каталога (06.11.2026): **1500 грн**. [Официальная карточка](https://raceexpert.com.ua/ru/nabor-nedelya-beguna). Состав: Sponser Crunchy Protein Bar, 50 g x2; Hydria Perform lemon sticks x6; GU Energy Chews lemonade, 60 g x1. В начале описания упоминается энергетический гель, но нумерованный список товаров его не содержит. Назначение: Для бегунов: энергия на тренировках, восстановление и восполнение жидкости и питательных веществ. Спорт/активность: Бег. Формат забега/дистанция: Упоминаются тренировки и старты; формат и дистанция не указаны.  Диапазон веса покупателя: не указан. Теги: purpose:running_week_snacks_and_hydration; sport:running; distance:unspecified; price:1500_uah; buyer_weight:not_specified; item_type:snack_bundle; audience:runners; contains:protein; contains:electrolytes; data_quality:intro_list_mismatch

60. **RE88965** — Набір «Вечірнє розслаблення Race Expert Club» — абонемент на 3 місяці. Цена каталога (06.11.2026): **1395 грн**. [Официальная карточка](https://raceexpert.com.ua/7023-nabir-vechirnye-rozslablennya-re88965-1-549-grn-re88965). Состав: абонемент Race Expert Club на 3 месяца; Reishi 700 mg, 60 caps; NOW 5-HTP 50 mg, 30 caps; KAL Stress B Magnesium Glycinate, 60 caps. Назначение: Вечернее расслабление и отдых. Спорт/активность: Конкретный вид спорта не указан. Формат забега/дистанция: Не относится к конкретному забегу; дистанция не применима. Диапазон веса покупателя: не указан. Теги: purpose:evening_relaxation; sport:not_sport_specific; distance:not_applicable; price:1395_uah; buyer_weight:not_specified; item_type:supplement_bundle; item_type:club_membership_bundle; contains:reishi; contains:5_htp; contains:magnesium; duration:3_months

61. **RE88947** — Набір «Спокійний сон Race Expert Club» — абонемент на 3 місяці. Цена каталога (06.11.2026): **1385 грн**. [Официальная карточка](https://raceexpert.com.ua/7008-nabir-spokijnij-son-re88947-1-519-grn-re88947-son-i-vid). Состав: абонемент Race Expert Club на 3 месяца; Reishi 700 mg, 60 caps; KAL Stress B Magnesium Glycinate, 60 caps; NOW Melatonin 3 mg, 60 caps. Назначение: Поддержка сна и отдыха. Спорт/активность: Конкретный вид спорта не указан. Формат забега/дистанция: Не относится к конкретному забегу; дистанция не применима. Диапазон веса покупателя: не указан. Теги: purpose:sleep_and_rest_support; sport:not_sport_specific; distance:not_applicable; price:1385_uah; buyer_weight:not_specified; item_type:supplement_bundle; item_type:club_membership_bundle; contains:reishi; contains:magnesium; contains:melatonin; duration:3_months

62. **RE11803** — Набір «Польовий сон Race Expert Club» — абонемент на 3 місяці. Цена каталога (06.11.2026): **1500 грн**. [Официальная карточка](https://raceexpert.com.ua/6953-nabir-polovij-son-re11803-1-749-grn-re11803-son-i-vidno). Текущая цена (наблюдение 06.11.2026): **1500 грн** (указана предыдущая цена 1749 грн). Состав: абонемент Race Expert Club на 3 месяца; VPLab Ultra Sleep, 60 caps; Nutriversum Melatonin, 60 caps; Race Expert флисовый бафф. Назначение: Сон и отдых в полевых условиях. Спорт/активность: Спортивное применение не указано. Формат забега/дистанция: Не относится к конкретному забегу; дистанция не применима. Диапазон веса покупателя: не указан. Теги: purpose:field_sleep_support; sport:not_sport_specific; distance:not_applicable; price:1500_uah; buyer_weight:not_specified; item_type:apparel_bundle; item_type:supplement_bundle; item_type:equipment_bundle; item_type:club_membership_bundle; audience:field_use; contains:melatonin; duration:3_months

63. **RE89026** — Набір «Нічне відновлення» — абонемент на 3 місяці. Цена каталога (06.11.2026): **1500 грн**. [Официальная карточка](https://raceexpert.com.ua/7034-nabir-nichne-vidnovlennya-re89026-1-579-grn-re89026-son). Состав: абонемент Race Expert Club на 3 месяца; Swanson Triple Magnesium 400 mg, 100 caps; Ashwagandha 450 mg, 100 caps; NOW Melatonin 3 mg, 60 caps; NOW 5-HTP 50 mg, 30 caps. Назначение: Вечерняя поддержка отдыха и восстановления. Спорт/активность: Конкретный вид спорта не указан. Формат забега/дистанция: Не относится к конкретному забегу; дистанция не применима. Диапазон веса покупателя: не указан. Теги: purpose:night_recovery; sport:not_sport_specific; distance:not_applicable; price:1500_uah; buyer_weight:not_specified; item_type:supplement_bundle; item_type:club_membership_bundle; contains:magnesium; contains:ashwagandha; contains:melatonin; contains:5_htp; duration:3_months

64. **RE11523** — Набір «Глибокий сон і відновлення» — абонемент на 3 місяці. Цена каталога (06.11.2026): **1500 грн**. [Официальная карточка](https://raceexpert.com.ua/ru/nabor-4). Текущая цена (наблюдение 06.11.2026): **1500 грн** (указана предыдущая цена 1945 грн). Состав: абонемент Race Expert Club на 3 месяца; Swanson Ashwagandha, 450 mg, 100 caps; Swanson Melatonin, 3 mg, 60 caps; Swanson Triple Magnesium, 400 mg, 100 caps. Назначение: По названию набора — поддержка сна и восстановления; подробная формулировка назначения не подтверждена после исправления состава. Спорт/активность: Вид спорта не указан; назначение связано со сном и восстановлением. Формат забега/дистанция: Не относится к конкретному забегу; дистанция не применима. Диапазон веса покупателя: не указан. Теги: purpose:deep_sleep_and_recovery; sport:not_sport_specific; distance:not_applicable; price:1500_uah; buyer_weight:not_specified; item_type:supplement_bundle; item_type:club_membership_bundle; contains:ashwagandha; contains:melatonin; contains:magnesium; duration:3_months

65. **RE11694** — Набір «Воля та незламність Race Expert Club» — абонемент на 3 місяці. Цена каталога (06.11.2026): **1500 грн**. [Официальная карточка](https://raceexpert.com.ua/6885-nabir-volya-ta-nezlamnist-re11694-1-825-grn-re11694-aks). Текущая цена (наблюдение 06.11.2026): **1500 грн** (указана предыдущая цена 1825 грн). Состав: абонемент Race Expert Club на 3 месяца; medal «Озброєні волею 2.0»; брелок из гильзы с гравировкой; брелок в виде истребителя; брелок в виде дрона. Назначение: Патриотический подарок и символическая поддержка стойкости. Спорт/активность: Спортивное применение не указано. Формат забега/дистанция: Не относится к конкретному забегу; дистанция не применима. Диапазон веса покупателя: не указан. Теги: purpose:patriotic_gift; sport:not_sport_specific; distance:not_applicable; price:1500_uah; buyer_weight:not_specified; item_type:equipment_bundle; item_type:gift_bundle; item_type:club_membership_bundle; audience:gift; duration:3_months

66. **RE88958** — Набір «Відпочинок нервової системи Race Expert Club» — абонемент на 3 місяці. Цена каталога (06.11.2026): **1435 грн**. [Официальная карточка](https://raceexpert.com.ua/7015-nabir-vidpochinok-nervovoyi-sistemi-re88958-1-675-grn-r). Текущая цена (наблюдение 06.11.2026): **1500 грн** (указана предыдущая цена 1675 грн). Состав: Swanson Full Spectrum Ashwagandha 450 mg, 100 caps x2; NOW 5-HTP 50 mg, 30 caps; OstroVit Magnesium Citrate + B6, 90 таблеток (400 mg magnesium + 15 mg B6 per 3-tab serving). Назначение: Отдых и восстановление при стрессе, эмоциональном напряжении и высоких нагрузках; названы активные люди. Спорт/активность: Упоминаются физические нагрузки; дисциплина не названа. Формат забега/дистанция: Не относится к конкретному забегу; дистанция не применима. Диапазон веса покупателя: не указан. Теги: purpose:nervous_system_rest; sport:physical_activity_general; distance:not_applicable; price:1435_uah; buyer_weight:not_specified; item_type:supplement_bundle; item_type:club_membership_bundle; audience:active_people; audience:high_stress; contains:ashwagandha; contains:5_htp; contains:magnesium; duration:3_months; data_quality:live_price_differs

67. **RE88949** — Набір «Спокійний вечір Race Expert Club» — абонемент на 3 місяці. Цена каталога (06.11.2026): **1245 грн**. [Официальная карточка](https://raceexpert.com.ua/7009-nabir-spokijnij-vechir-re88949-1-525-grn-re88949-son-i). Текущая цена (наблюдение 06.11.2026): **1500 грн** (указана предыдущая цена 1525 грн). Состав: абонемент Race Expert Club на 3 месяца; Mind Shi Reishi Mushroom 1000 mg, 60 caps; Swanson Full Spectrum Ashwagandha 450 mg, 100 caps. Назначение: Эмоциональное равновесие и вечерний отдых при повседневных эмоциональных и физических нагрузках. Спорт/активность: Конкретный вид спорта не указан. Формат забега/дистанция: Не относится к конкретному забегу; дистанция не применима. Диапазон веса покупателя: не указан. Теги: purpose:calm_evening; sport:not_sport_specific; distance:not_applicable; price:1245_uah; buyer_weight:not_specified; item_type:supplement_bundle; item_type:club_membership_bundle; contains:reishi; contains:ashwagandha; duration:3_months; data_quality:live_price_differs

68. **Nabir_1121** — Набір «Чоловіча сила Race Expert Club» — абонемент на 3 місяці. Цена каталога (06.11.2026): **1005 грн**. [Официальная карточка](https://raceexpert.com.ua/6392-nabir-sila-i-komfort-nabir-1121-1-589-grn-nabir-1121-sh). Состав: абонемент Race Expert Club на 3 месяца; тёмные носки RE2 x2 пары и белые носки RE2 x2 пары, размер 40–44; OstroVit Creatine, 500 g; Myprotein Baked Cookie, 75 g. Назначение: Поддержка мужских силовых тренировок. Спорт/активность: Силовые тренировки; дисциплина не названа. Формат забега/дистанция: Не относится к конкретному забегу; дистанция не применима. Диапазон веса покупателя: не указан. Теги: purpose:men_strength_and_training_support; sport:strength_training; distance:not_applicable; price:1005_uah; buyer_weight:not_specified; item_type:apparel_bundle; item_type:snack_bundle; item_type:supplement_bundle; item_type:equipment_bundle; item_type:club_membership_bundle; audience:men; contains:creatine; contains:protein; duration:3_months; shoe_size:40-44

69. **RE89023** — Набір «Чоловіча підтримка 50+ Race Expert Club» — абонемент на 3 місяці. Цена каталога (06.11.2026): **1429 грн**. [Официальная карточка](https://raceexpert.com.ua/7033-nabir-cholovicha-pidtrimka-50-re89023-1-565-grn-re89023). Состав: абонемент Race Expert Club на 3 месяца; Nature’s Way Alive Men’s 50+, 50 tabs; Swanson Ashwagandha 450 mg, 100 caps; NOW Melatonin 3 mg, 60 caps. Назначение: Поддержка для мужчин 50+. Спорт/активность: Конкретный вид спорта не указан. Формат забега/дистанция: Не относится к конкретному забегу; дистанция не применима. Диапазон веса покупателя: не указан. Теги: purpose:men_support; sport:not_sport_specific; distance:not_applicable; price:1429_uah; buyer_weight:not_specified; item_type:supplement_bundle; item_type:club_membership_bundle; audience:men_50_plus; contains:ashwagandha; contains:melatonin; duration:3_months

70. **RE89020** — Набір «Жіноча енергія та баланс Race Expert Club» — абонемент на 3 місяці. Цена каталога (06.11.2026): **1500 грн**. [Официальная карточка](https://raceexpert.com.ua/7031-nabir-zhinocha-energiya-ta-balans-re89020-1-615-grn-re8). Состав: абонемент Race Expert Club на 3 месяца; Nature’s Way Alive Women’s Energy; Swanson Ashwagandha 450 mg, 100 caps; Swanson B12 500 mcg, 100 caps. Назначение: Энергия и баланс для женщин при активном образе жизни. Спорт/активность: Конкретный вид спорта не указан. Формат забега/дистанция: Не относится к конкретному забегу; дистанция не применима. Диапазон веса покупателя: не указан. Теги: purpose:womens_energy_and_balance; sport:not_sport_specific; distance:not_applicable; price:1500_uah; buyer_weight:not_specified; item_type:supplement_bundle; item_type:club_membership_bundle; audience:women; audience:active_lifestyle; contains:ashwagandha; contains:vitamin_b12; duration:3_months

71. **RE88962** — Набір «Чоловічий тонус 50+ Race Expert Club» — абонемент на 3 місяці. Цена каталога (06.11.2026): **1379 грн**. [Официальная карточка](https://raceexpert.com.ua/7020-nabir-cholovichij-tonus-50-re88962-1-549-grn-re88962-sh). Состав: абонемент Race Expert Club на 3 месяца; Alive Men’s 50+, 50 tabs; Ashwagandha 450 mg, 100 caps; NOW Zinc Picolinate 50 mg, 30 caps. Назначение: Поддержка тонуса для мужчин 50+. Спорт/активность: Конкретный вид спорта не указан. Формат забега/дистанция: Не относится к конкретному забегу; дистанция не применима. Диапазон веса покупателя: не указан. Теги: purpose:men_tone_support; sport:not_sport_specific; distance:not_applicable; price:1379_uah; buyer_weight:not_specified; item_type:supplement_bundle; item_type:club_membership_bundle; audience:men_50_plus; contains:ashwagandha; contains:zinc; duration:3_months

72. **RE88944** — Набір «Чоловічий тонус Race Expert Club» — абонемент на 3 місяці. Цена каталога (06.11.2026): **1500 грн**. [Официальная карточка](https://raceexpert.com.ua/7006-nabir-cholovichij-tonus-re88944-1-575-grn-re88944-shode). Состав: абонемент Race Expert Club на 3 месяца; Swanson Maca 500 mg, 60 caps; Ashwagandha 450 mg, 100 caps; NOW D3 5000 IU, 30 softgels; Hydria Daily sticks x5. Назначение: Поддержка мужского тонуса и активного образа жизни. Спорт/активность: Конкретный вид спорта не указан. Формат забега/дистанция: Не относится к конкретному забегу; дистанция не применима. Диапазон веса покупателя: не указан. Теги: purpose:men_tone_support; sport:not_sport_specific; distance:not_applicable; price:1500_uah; buyer_weight:not_specified; item_type:supplement_bundle; item_type:club_membership_bundle; audience:men; audience:active_lifestyle; contains:maca; contains:ashwagandha; contains:vitamin_d3; contains:electrolytes; duration:3_months

73. **RE89418** — Набір м'ясних снеків (соєвий соус) Race Expert Club — абонемент на 3 місяці. Цена каталога (06.11.2026): **1500 грн**. [Официальная карточка](https://raceexpert.com.ua/index.php?product_id=7148&route=product%2Fproduct). Текущая цена (наблюдение 06.11.2026): **1500 грн** (указана предыдущая цена 1555 грн). Состав: абонемент на 3 месяца; RyabChick сушёные ломтики курицы, soy sauce, 30 g x16. Назначение: Белковые снеки для спортсменов, людей, контролирующих вес или придерживающихся низкоуглеводного рациона, а также для поездок, работы и тренировок. Спорт/активность: Тренировки упомянуты в общем виде; дисциплина не названа. Формат забега/дистанция: Не относится к конкретному забегу; дистанция не применима. Диапазон веса покупателя: не указан. Пищевая ценность: 81 г белка на 100 г, 0,5 г углеводов, 95% курицы. Теги: purpose:protein_snacking; sport:training_general; distance:not_applicable; price:1500_uah; buyer_weight:not_specified; item_type:snack_bundle; item_type:club_membership_bundle; audience:athletes; audience:weight_control; audience:low_carb; contains:protein; duration:3_months; package_weight:30g

74. **RE89416** — Набір м'ясних снеків (мед, гірчиця) Race Expert Club — абонемент на 3 місяці. Цена каталога (06.11.2026): **1500 грн**. [Официальная карточка](https://raceexpert.com.ua/index.php?product_id=7146&route=product%2Fproduct). Текущая цена (наблюдение 06.11.2026): **1500 грн** (указана предыдущая цена 1555 грн). Состав: RyabChick сушёные ломтики курицы, медово-горчичный вкус, 30 g x16; карточка указывает, что в набор входит абонемент Race Expert Club на 3 месяца. Назначение: Белковые снеки для спортсменов, активных людей и тех, кто контролирует вес или потребление углеводов. Спорт/активность: Тренировки упомянуты в общем виде; дисциплина не названа. Формат забега/дистанция: Не относится к конкретному забегу; дистанция не применима. Диапазон веса покупателя: не указан. Пищевая ценность: заявлено высокое содержание белка и низкое содержание углеводов; точные значения на карточке набора не указаны. Теги: purpose:protein_snacking; sport:training_general; distance:not_applicable; price:1500_uah; buyer_weight:not_specified; item_type:snack_bundle; item_type:club_membership_bundle; audience:athletes; audience:active_people; audience:weight_control; audience:low_carb; contains:protein; duration:3_months; package_weight:30g

75. **RE11721** — Набір «Сублімований мікс Race Expert Club» — абонемент на 3 місяці. Цена каталога (06.11.2026): **1389 грн**. [Официальная карточка](https://raceexpert.com.ua/6887-nabir-sublimovanij-miks-re11721-1-519-grn-re11721-yizha). Состав: абонемент Race Expert Club на 3 месяца; ассорти сублимированных фруктов x6; ассорти сублимированного мороженого x6; бутылка Race Expert (объём не указан). Назначение: Снеки или подарок; спортивное назначение не указано. Спорт/активность: Конкретный вид спорта не указан. Формат забега/дистанция: Не относится к конкретному забегу; дистанция не применима. Диапазон веса покупателя: не указан. Теги: purpose:snacking_or_gift; sport:not_sport_specific; distance:not_applicable; price:1389_uah; buyer_weight:not_specified; item_type:snack_bundle; item_type:equipment_bundle; item_type:gift_bundle; item_type:club_membership_bundle; duration:3_months

### Записи 76–150

- **76 · RE11695 · Набір «Мандрівний смаколик Race Expert Club» — абонемент на 3 місяці · снимок: 1 249 UAH.** [Официальная карточка](https://raceexpert.com.ua/6886-nabir-re11695-1-499-grn-re11695-yizha-sneki-ta-napoyi). Состав: абонемент клуба на 3 месяца; 2 упаковки сублимированных фруктов по 6 штук; напиток Napiy ваниль-корица 90 г ×1 и шоколад 90 г ×1. Назначение: перекус в поездках, походах, на выездах, на работе или учёбе, до/после тренировки; конкретный вид спорта не указан. Каждый напиток: 25 г белка и 9 г клетчатки; смешивать с 300 мл воды или растительного молока. Карточка показывает 1 500 UAH против 1 249 UAH в снимке.
  - Теги: purpose:travel_snack; item_type:club_membership_bundle; sport:not_sport_specific; distance:not_applicable; duration:3_months; contains:protein; contains:fiber; audience:athletes; audience:students; audience:tourists; audience:travelers; buyer_weight:not_specified; price:1249_uah; data_quality:live_price_differs

- **77 · RE11557 · Набір «Розумна їжа Race Expert Club» — абонемент на 3 місяці · снимок: 1 500 UAH.** [Официальная карточка](https://raceexpert.com.ua/6778-nabir-rozumna-yizha-re11557-1-559-grn-re11557-yizha-sne). Состав: абонемент клуба на 3 месяца; напитки Napiy 90 г ×9 (ваниль-корица ×3, шоколад ×3, клубника ×3); шейкер 700 мл. Назначение: удобная полноценная еда/перекус для спортсменов, офисных работников, студентов и путешественников при нехватке времени; также после тренировки. В напитке 25 г белка; клубничный вкус содержит 9 г клетчатки; смешивать с 300 мл. Точная дистанция не указана.
  - Теги: purpose:quick_meal; item_type:club_membership_bundle; sport:not_sport_specific; distance:not_applicable; duration:3_months; contains:protein; contains:fiber; audience:athletes; audience:office_workers; audience:students; audience:travelers; buyer_weight:not_specified; price:1500_uah

- **78 · RE11495 · Набір «Похідна їжа ЇDLO Race Expert Club» — абонемент на 3 місяці · снимок: 1 500 UAH.** [Официальная карточка](https://raceexpert.com.ua/ru/nabor-pohodnaya-pisha-yidlo). Состав: абонемент клуба на 3 месяца; картофель с курицей 90 г ×2; полента с овощами 90 г ×2; гречка с веганскими тефтелями 100 г ×2; бануш 100 г ×1; карпатский чай 40 г (5 фильтр-пакетов, каждый на 1 л). Назначение: походы, поездки, кемпинг, рыбалка, охота и длительные выезды. Приготовление блюд — 10 минут. На порцию указано: картофель 344 ккал/17,1 г белка/50,7 г углеводов; полента 298,5/6,3/61,9; гречка 354/9,2/76,4; бануш 392 ккал.
  - Теги: purpose:hiking_food; item_type:club_membership_bundle; sport:hiking; distance:not_applicable; duration:3_months; audience:anglers; audience:campers; audience:hunters; audience:tourists; buyer_weight:not_specified; price:1500_uah

- **79 · Nabir_1129 · Набір «Енергетичний перекус Race Expert Club» — абонемент на 3 місяці · снимок: 1 500 UAH.** [Официальная карточка](https://raceexpert.com.ua/ru/nabor-energeticheskij-perekus). Состав: абонемент клуба на 3 месяца; протеиновые батончики 40 г ×13: клюква/рейши ×4, кофе/кордицепс ×5, кокос/ежовик ×4. Назначение: функциональный перекус для спортсменов, активных людей и людей с постоянной нагрузкой; конкретный спорт не указан. Кофейный вкус указан, количество кофеина — нет.
  - Теги: purpose:energy_snack; item_type:club_membership_bundle; sport:not_sport_specific; distance:not_applicable; duration:3_months; contains:protein; audience:active_people; audience:athletes; buyer_weight:not_specified; price:1500_uah

- **80 · RE11822 · Набір «Дорожня гігієна» · снимок: 1 500 UAH.** [Официальная карточка](https://raceexpert.com.ua/6974-nabir-dorozhnya-gigiyena-re11822-1-599-grn-re11822-shod). Состав: гель для душа TRISWIM Body Wash 251 мл; зубная паста NOW Foods Xyli White 181 г; баф Race Expert. Назначение: гигиена в поездках, на тренировках и при плавании; аудитория — пловцы, путешественники и спортсмены. Ранее карточка дала 404, но сохранённый официальный снимок от 2026-11-06 содержит состав и описание. Текущая цена отдельно не зафиксирована.
  - Теги: purpose:travel_hygiene; item_type:equipment_bundle; sport:swimming; distance:not_applicable; audience:athletes; audience:swimmers; audience:travelers; buyer_weight:not_specified; price:1500_uah

- **81 · RE11780 · Набір «Темні шкарпетки» (40-44) · снимок: 1 500 UAH.** [Официальная карточка](https://raceexpert.com.ua/6914-nabir-temni-shkarpetki-40-44-re11780-1-825-grn-re11780). Состав: 5 пар тёмных носков RE2, размер 40–44. Назначение: бег, спортивные тренировки, зал и повседневная носка; карточка прямо упоминает бегунов и спортсменов. Состав материала: 80% полиэстер, 17% эластан, 3% полиамид; указаны вентиляция, отведение влаги и антибактериальная обработка. Карточка показывает 1 500 UAH.
  - Теги: purpose:running_comfort; item_type:apparel_bundle; sport:running; distance:unspecified; shoe_size:40-44; audience:athletes; audience:runners; buyer_weight:not_specified; price:1500_uah

- **82 · RE11779 · Акційний набір темних шкарпеток 5 пар "40 - 42" · снимок: 950 UAH.** [Официальная карточка](https://raceexpert.com.ua/6913-nabir-temni-shkarpetki-40-42-re11779-1-575-grn-re11779). Состав: 5 пар тёмных носков Race Expert, размер 40–42 (в подробной карточке позиция указана в количестве 5 шт.); материал — 95% полиамид и 5% эластан. Назначение: комфорт при беге, тренировках в спортивном зале и повседневном использовании; карточка указывает на анатомическую посадку, влагоотведение и вентиляцию, антибактериальную обработку и защиту от натирания. Спорт/активность: бег и общие тренировки. Дистанция: конкретная не задана; описание говорит о комфорте независимо от дистанции. Цена карточки при перепроверке: 1 500 грн против 950 грн в снимке каталога.
  - Теги: purpose:running_comfort; item_type:apparel_bundle; sport:running; sport:general_fitness; distance:unspecified; shoe_size:40-42; audience:athletes; audience:runners; buyer_weight:not_specified; price:950_uah; data_quality:live_price_differs

- **83 · RE11778 · Акційний набір темних шкарпеток 5 пар "38 - 40" · снимок: 950 UAH.** [Официальная карточка](https://raceexpert.com.ua/6912-nabir-temni-shkarpetki-38-40-re11778-1-575-grn-re11778). Состав: 5 пар тёмных носков Race Expert, размер 38–40 (в подробной карточке позиция указана в количестве 5 шт.); материал — 95% полиамид и 5% эластан. Назначение: комфорт при беге, тренировках в спортивном зале и повседневном использовании; карточка указывает на анатомическую посадку, влагоотведение и вентиляцию, антибактериальную обработку и защиту от натирания. Спорт/активность: бег и общие тренировки. Дистанция: конкретная не задана; описание говорит о комфорте независимо от дистанции. Цена карточки при перепроверке: 1 500 грн против 950 грн в снимке каталога.
  - Теги: purpose:running_comfort; item_type:apparel_bundle; sport:running; sport:general_fitness; distance:unspecified; shoe_size:38-40; audience:athletes; audience:runners; buyer_weight:not_specified; price:950_uah; data_quality:live_price_differs

- **84 · RE11777 · Акційний набір темних шкарпеток 5 пар "35 - 37" · снимок: 950 UAH.** [Официальная карточка](https://raceexpert.com.ua/6911-nabir-temni-shkarpetki-35-37-re11777-1-575-grn-re11777). Состав: 5 пар тёмных носков Race Expert, размер 35–37 (в подробной карточке позиция указана в количестве 5 шт.); материал — 95% полиамид и 5% эластан. Назначение: комфорт при беге, тренировках в спортивном зале и повседневном использовании; карточка указывает на анатомическую посадку, влагоотведение и вентиляцию, антибактериальную обработку и защиту от натирания. Спорт/активность: бег и общие тренировки. Дистанция: конкретная не задана; описание говорит о комфорте независимо от дистанции. Цена карточки при перепроверке: 1 500 грн против 950 грн в снимке каталога.
  - Теги: purpose:running_comfort; item_type:apparel_bundle; sport:running; sport:general_fitness; distance:unspecified; shoe_size:35-37; audience:athletes; audience:runners; buyer_weight:not_specified; price:950_uah; data_quality:live_price_differs

- **85 · RE11776 · Акційний набір білих шкарпеток 5 пар "40 - 42" · снимок: 950 UAH.** [Официальная карточка](https://raceexpert.com.ua/6910-nabir-bili-shkarpetki-40-42-re11776-1-575-grn-re11776-a). Состав: 5 пар белых носков Race Expert, размер 40–42 (в подробной карточке позиция указана в количестве 5 шт.); материал — 95% полиамид и 5% эластан. Назначение: комфорт при беге, тренировках в спортивном зале и повседневном использовании; карточка указывает на анатомическую посадку, влагоотведение и вентиляцию, антибактериальную обработку и защиту от натирания. Спорт/активность: бег и общие тренировки. Дистанция: конкретная не задана; описание говорит о комфорте независимо от дистанции. Цена карточки при перепроверке: 1 500 грн против 950 грн в снимке каталога.
  - Теги: purpose:running_comfort; item_type:apparel_bundle; sport:running; sport:general_fitness; distance:unspecified; shoe_size:40-42; audience:athletes; audience:runners; buyer_weight:not_specified; price:950_uah; data_quality:live_price_differs

- **86 · RE11775 · Акційний набір білих шкарпеток 5 пар "38 - 40" · снимок: 950 UAH.** [Официальная карточка](https://raceexpert.com.ua/6909-nabir-bili-shkarpetki-38-40-re11775-1-575-grn-re11775-a). Состав: 5 пар белых носков Race Expert, размер 38–40 (в подробной карточке позиция указана в количестве 5 шт.); материал — 95% полиамид и 5% эластан. Назначение: комфорт при беге, тренировках в спортивном зале и повседневном использовании; карточка указывает на анатомическую посадку, влагоотведение и вентиляцию, антибактериальную обработку и защиту от натирания. Спорт/активность: бег и общие тренировки. Дистанция: конкретная не задана; описание говорит о комфорте независимо от дистанции. Цена карточки при перепроверке: 1 500 грн против 950 грн в снимке каталога.
  - Теги: purpose:running_comfort; item_type:apparel_bundle; sport:running; sport:general_fitness; distance:unspecified; shoe_size:38-40; audience:athletes; audience:runners; buyer_weight:not_specified; price:950_uah; data_quality:live_price_differs

- **87 · RE11022 · Акційний набір темних шкарпеток 5 пар "43 - 45" · снимок: 950 UAH.** [Официальная карточка](https://raceexpert.com.ua/6699-nabir-temni-shkarpetki-re11022-1-825-grn-re11022-aksesu). Состав: 5 пар тёмных носков Race Expert, размер 43–45. Назначение: комфорт при беге, тренировках в зале и повседневной носке. Карточка прямо называет бегунов и спортсменов. Сохранённый официальный снимок от 2026-11-06; текущая цена отдельно не зафиксирована.
  - Теги: purpose:running_comfort; item_type:apparel_bundle; sport:running; distance:unspecified; shoe_size:43-45; audience:athletes; audience:runners; buyer_weight:not_specified; price:950_uah

- **88 · RE11019 · Набір «Щоденний комфорт Race Expert Club» — абонемент на 3 місяці · снимок: 1 500 UAH.** [Официальная карточка](https://raceexpert.com.ua/6695-nabir-shodennij-komfort-re11019-1-849-grn-re11019-akses). Состав: клуб на 3 месяца; белые носки Race Expert 40–42; шейкер; стеклянная бутылка; печенье Fitly 45 г ×5, по 13 г белка. Назначение: комфорт в активный день на работе, тренировке, прогулке или в поездке; отдельный вид спорта не указан.
  - Теги: purpose:everyday_comfort; item_type:club_membership_bundle; sport:not_sport_specific; distance:not_applicable; duration:3_months; audience:active_people; buyer_weight:not_specified; price:1500_uah

- **89 · RE11018 · Набір «Бігова класика» · снимок: 1 500 UAH.** [Официальная карточка](https://raceexpert.com.ua/6694-nabir-bigova-klasika-re11018-2-085-grn-re11018-aksesuar). Состав: белые носки RE2 40–44; тёмные RE2 40–44; белые носки Race Expert 40–42; чёрный баф; брелок-гильза. Назначение: бег; баф также предлагается для велоспорта, хайкинга и повседневной носки. Формат забега/дистанция не указаны.
  - Теги: purpose:running_accessories; item_type:equipment_bundle; sport:running; distance:unspecified; shoe_size:40-42; shoe_size:40-44; audience:runners; buyer_weight:not_specified; price:1500_uah

- **90 · RE11013 · Набір «Бігова пара» · снимок: 1 359 UAH.** [Официальная карточка](https://raceexpert.com.ua/ru/nabor-begovaya-para). Состав: по извлечённому перечню карточки — белые носки RE2 40–44; тёмные носки RE2 40–44; стеклянная бутылка 530 мл. Назначение по сохранённой карточке: беговой комплект для активного дня. Спорт: бег. **Неясность состава:** во вступлении также упоминаются батончики, но в видимом перечне компонентов есть только три позиции. В индексе карточка показывала 1 500 UAH против 1 359 UAH в снимке.
  - Теги: purpose:running_day_kit; item_type:equipment_bundle; sport:running; distance:unspecified; shoe_size:40-44; audience:runners; buyer_weight:not_specified; price:1359_uah; data_quality:composition_conflict; data_quality:live_price_differs

- **91 · RE89485 · Набір «Подарунок для прогулянок» — абонемент на 3 місяці · снимок: 1 379 UAH.** [Официальная карточка](https://raceexpert.com.ua/7169-nabir-podarunok-dlya-progulyanok-abonement-na-3-misyaci). Состав: клуб на 3 месяца; медаль «Здатні без зброї»; баф (цвет из ассортимента); небольшой чёрный органайзер; тёмные носки RE2 40–44. Назначение: прогулки, поездки и активный отдых; подарочная аудитория — активные люди, друзья, семья и коллеги. Карточка показывает 1 500 UAH против 1 379 UAH в снимке.
  - Теги: purpose:walking_gift; item_type:club_membership_bundle; sport:not_sport_specific; distance:not_applicable; duration:3_months; shoe_size:40-44; audience:active_people; audience:colleagues; audience:family; audience:friends; buyer_weight:not_specified; price:1379_uah; data_quality:live_price_differs

- **92 · RE89484 · Набір «Осінній подарунок» — абонемент на 3 місяці · снимок: 1 500 UAH.** [Официальная карточка](https://raceexpert.com.ua/7168-nabir-osinnij-podarunok-abonement-na-3-misyaci-re89484). Состав: клуб на 3 месяца; медаль «Озброєні волею 2.0»; флисовый баф; небольшой чёрный органайзер. Назначение: подарок для прогулок, поездок и использования на улице в прохладную погоду.
  - Теги: purpose:cold_weather_gift; item_type:club_membership_bundle; sport:not_sport_specific; distance:not_applicable; duration:3_months; audience:gift_recipients; weather:cold; buyer_weight:not_specified; price:1500_uah

- **93 · RE89483 · Набір «Теплий подарунок» — абонемент на 3 місяці · снимок: 1 500 UAH.** [Официальная карточка](https://raceexpert.com.ua/7167-nabir-teplij-podarunok-abonement-na-3-misyaci-re89483-2). Состав: клуб на 3 месяца; медаль «Крила Свободи»; баф (цвет из ассортимента); небольшой чёрный органайзер. Назначение: подарок для прогулок, поездок и использования на улице в прохладную погоду.
  - Теги: purpose:walking_gift; item_type:club_membership_bundle; sport:not_sport_specific; distance:not_applicable; duration:3_months; audience:gift_recipients; weather:cold; buyer_weight:not_specified; price:1500_uah

- **94 · RE89482 · Набір «Подарунок у похід» — абонемент на 3 місяці · снимок: 1 500 UAH.** [Официальная карточка](https://raceexpert.com.ua/7166-nabir-podarunok-u-pohid-abonement-na-3-misyaci-re89482). Состав: клуб на 3 месяца; медаль «Гвардія небес»; небольшой чёрный органайзер; тёмные носки RE2 40–44. Назначение: походы, путешествия, длительные прогулки и отдых на природе; карточка ориентирует подарок на военных, ветеранов и путешественников.
  - Теги: purpose:hiking_gift; item_type:club_membership_bundle; sport:hiking; distance:not_applicable; duration:3_months; shoe_size:40-44; audience:military_personnel; audience:travelers; audience:veterans; buyer_weight:not_specified; price:1500_uah

- **95 · RE89475 · Набір «Бігова екіпіровка Race Expert» — абонемент на 3 місяці · снимок: 1 415 UAH.** [Официальная карточка](https://raceexpert.com.ua/index.php?product_id=7164&route=product%2Fproduct). Состав: клуб на 3 месяца; флисовый баф; стеклянная бутылка с чехлом 530 мл; тёмные и белые носки RE2 40–44. Назначение: бег и тренировки; конкретный старт или километраж не указан. В индексированной карточке цена 1 500 UAH против 1 415 UAH в снимке.
  - Теги: purpose:running_gear; item_type:equipment_bundle; sport:running; distance:unspecified; duration:3_months; shoe_size:40-44; audience:runners; buyer_weight:not_specified; price:1415_uah; data_quality:live_price_differs

- **96 · RE89474 · Набір «Подарунок у дорогу» — абонемент на 3 місяці · снимок: 1 500 UAH.** [Официальная карточка](https://raceexpert.com.ua/7163-nabir-podarunok-u-dorogu-abonement-na-3-misyaci-re89474). Состав: клуб на 3 месяца; медаль «Озброєні волею 2.0»; небольшой чёрный органайзер EF-0903-BK; тёмные носки RE2 40–44. Назначение: дорога, поездки, служба, тренировки и использование на улице; подарочная аудитория — военные, ветераны и путешественники.
  - Теги: purpose:travel_gift; item_type:club_membership_bundle; sport:not_sport_specific; distance:not_applicable; duration:3_months; shoe_size:40-44; audience:military_personnel; audience:travelers; audience:veterans; buyer_weight:not_specified; price:1500_uah

- **97 · RE89473 · Набір «Подвійна нагорода» — абонемент на 3 місяці · снимок: 1 500 UAH.** [Официальная карточка](https://raceexpert.com.ua/7162-nabir-podvijna-nagoroda-abonement-na-3-misyaci-re89473). Состав: клуб на 3 месяца; медали «Озброєні волею 2.0» и «Здатні без зброї»; брелоки Drone 2.0 и гильза. Назначение/аудитория: тематический подарок военным, ветеранам, волонтёрам, коллекционерам и людям, которым близка украинская символика; спорт не указан.
  - Теги: purpose:patriotic_gift; item_type:club_membership_bundle; sport:not_sport_specific; distance:not_applicable; duration:3_months; audience:collectors; audience:military_personnel; audience:veterans; audience:volunteers; buyer_weight:not_specified; price:1500_uah

- **98 · RE89467 · Набір «Подарунок початківцю 2.0» — абонемент на 3 місяці · снимок: 1 500 UAH.** [Официальная карточка](https://raceexpert.com.ua/7161-nabir-podarunok-pochatkivcyu-20-abonement-na-3-misyaci). Состав: клуб на 3 месяца; медаль «Крила Свободи»; стеклянная бутылка 530 мл; белые носки RE2 40–44. Назначение/аудитория: первый шаг к активному образу жизни, начало спорта или возвращение к занятиям; дистанция не указана.
  - Теги: purpose:beginner_sports_gift; item_type:club_membership_bundle; sport:not_sport_specific; distance:not_applicable; duration:3_months; shoe_size:40-44; audience:beginners; buyer_weight:not_specified; price:1500_uah

- **99 · RE89466 · Набір «Подарунок початківцю» — абонемент на 3 місяці · снимок: 1 500 UAH.** [Официальная карточка](https://raceexpert.com.ua/7160-nabir-podarunok-pochatkivcyu-abonement-na-3-misyaci-re8). Состав: клуб на 3 месяца; медаль «Озброєні волею 2.0»; стеклянная бутылка 530 мл; тёмные носки RE2 40–44. Назначение/аудитория: начало тренировок и активного образа жизни; конкретный вид спорта не указан.
  - Теги: purpose:beginner_sports_gift; item_type:club_membership_bundle; sport:not_sport_specific; distance:not_applicable; duration:3_months; shoe_size:40-44; audience:beginners; buyer_weight:not_specified; price:1500_uah

- **100 · RE89460 · Набір «Подарунок військовому-спортсмену» — абонемент на 3 місяці · снимок: 1 500 UAH.** [Официальная карточка](https://raceexpert.com.ua/7159-nabir-podarunok-vijskovomu-sportsmenu-abonement-na-3-mi). Состав: клуб на 3 месяца; медаль «Гвардія Небес»; флисовый баф; тёмные носки RE2 40–44. Назначение/аудитория: активный образ жизни, тренировки и использование в прохладную погоду; военные, ветераны и спортсмены.
  - Теги: purpose:military_sports_gift; item_type:club_membership_bundle; sport:not_sport_specific; distance:not_applicable; duration:3_months; shoe_size:40-44; audience:athletes; audience:military_personnel; audience:veterans; weather:cold; buyer_weight:not_specified; price:1500_uah

- **101 · RE89459 · Набір «Подарунок мандрівнику» — абонемент на 3 місяці · снимок: 1 439 UAH.** [Официальная карточка](https://raceexpert.com.ua/7158-nabir-podarunok-mandrivniku-abonement-na-3-misyaci-re89). Состав: клуб на 3 месяца; полотенце Sharpey 135×70 см; флисовый баф; белые носки RE2 40–44. Назначение: путешествия, походы, активный отдых и спортивные поездки; аудитория — путешественники и спортсмены. Карточка показывает 1 500 UAH против 1 439 UAH в снимке.
  - Теги: purpose:traveler_gift; item_type:club_membership_bundle; sport:not_sport_specific; distance:not_applicable; duration:3_months; shoe_size:40-44; audience:athletes; audience:travelers; buyer_weight:not_specified; price:1439_uah; data_quality:live_price_differs

- **102 · RE89458 · Набір «Єдність сильних» — абонемент на 3 місяці · снимок: 1 500 UAH.** [Официальная карточка](https://raceexpert.com.ua/7157-nabir-yednist-silnih-abonement-na-3-misyaci-re89458-1-8). Состав: клуб на 3 месяца; медаль «Незалежність — це кожен з нас»; брелоки Fighter, Drone 2.0 и гильза. Назначение/аудитория: тематический подарок военным, ветеранам, коллекционерам и поклонникам украинской символики; спорт не указан.
  - Теги: purpose:patriotic_gift; item_type:club_membership_bundle; sport:not_sport_specific; distance:not_applicable; duration:3_months; audience:collectors; audience:military_personnel; audience:veterans; buyer_weight:not_specified; price:1500_uah

- **103 · RE89455 · Набір «Незборний дух» — абонемент на 3 місяці · снимок: 1 500 UAH.** [Официальная карточка](https://raceexpert.com.ua/7154-nabir-nezbornij-duh-abonement-na-3-misyaci-re89455-1-83). Состав: клуб на 3 месяца; медаль «Озброєні волею 2.0»; брелоки Fighter, гильза и Drone 2.0. Назначение/аудитория: подарок военным, ветеранам и коллекционерам; конкретный спорт не указан.
  - Теги: purpose:patriotic_gift; item_type:club_membership_bundle; sport:not_sport_specific; distance:not_applicable; duration:3_months; audience:collectors; audience:military_personnel; audience:veterans; buyer_weight:not_specified; price:1500_uah

- **104 · RE89454 · Набір «Політ честі» — абонемент на 3 місяці · снимок: 1 500 UAH.** [Официальная карточка](https://raceexpert.com.ua/7153-nabir-polit-chesti-abonement-na-3-misyaci-re89454-1-855). Состав: клуб на 3 месяца; медаль «Крила Свободи»; брелоки Fighter, Drone и Shell. Назначение/аудитория: подарок военным, ветеранам и коллекционерам с авиационной символикой; спорт не указан.
  - Теги: purpose:patriotic_gift; item_type:club_membership_bundle; sport:not_sport_specific; distance:not_applicable; duration:3_months; audience:collectors; audience:military_personnel; audience:veterans; buyer_weight:not_specified; price:1500_uah

- **105 · RE89453 · Набір «Мирне небо» — абонемент на 3 місяці · снимок: 1 500 UAH.** [Официальная карточка](https://raceexpert.com.ua/7152-nabir-mirne-nebo-abonement-na-3-misyaci-re89453-1-855-g). Состав: клуб на 3 месяца; медаль «Гвардія Небес»; брелоки Fighter, Drone и Shell. Назначение/аудитория: подарок военным, ветеранам и коллекционерам с украинской/военной символикой; спорт не указан.
  - Теги: purpose:patriotic_gift; item_type:club_membership_bundle; sport:not_sport_specific; distance:not_applicable; duration:3_months; audience:collectors; audience:military_personnel; audience:veterans; buyer_weight:not_specified; price:1500_uah

- **106 · RE11026 · Набір «Спортивний подарунок» · снимок: 1 500 UAH.** [Официальная карточка](https://raceexpert.com.ua/6703-nabir-sportivnij-podarunok-re11026-2-229-grn-re11026-po). Состав: белые носки Race Expert 43–45 ×2; брелоки-гильза ×3; NOW Foods Vitamin D3 2 000 IU, 120 софтгелей; печенье Myprotein Baked Cookie 75 г ×3 (по 13 г растительного белка). Назначение: подарок любителям спорта и активного образа жизни; карточка прямо называет бегунов и спортсменов. Дистанция не указана.
  - Теги: purpose:sports_gift; item_type:gift_bundle; sport:not_sport_specific; distance:not_applicable; shoe_size:43-45; audience:athletes; audience:runners; buyer_weight:not_specified; price:1500_uah

- **107 · Nabir_1060 · Набір «Воля та незламність» · снимок: 1 500 UAH.** [Официальная карточка](https://raceexpert.com.ua/ru/nabor-vremya-vosstanovitsya). Состав: медаль «Озброєні волею»; брелоки-гильза и Drone; брелок Fighter F-16 длиной 35 мм. Назначение/аудитория: тематический подарок с украинской символикой, в том числе военным и людям, проходящим свой путь; спорт не указан.
  - Теги: purpose:patriotic_gift; item_type:gift_bundle; sport:not_sport_specific; distance:not_applicable; audience:collectors; audience:military_personnel; audience:supporters_of_ukrainian_symbolism; buyer_weight:not_specified; price:1500_uah

- **111 · RE11494 · Набір «Похідна їжа ЇDLO 2.0» · снимок: 1 500 UAH.** [Официальная карточка](https://raceexpert.com.ua/ru/nabor-pohodnaya-eda-yidlo-20). Состав: картофель с веганскими сосисками 90 г ×2; макароны по-флотски ЇDLO 90 г ×2 (масса продукта — 180 г; готовая порция — 350 г на упаковку, [данные производителя](https://idlo.com/ru/makarony-po-flotsky-yidlo/)); гаспачо с индейкой 60 г ×2; гороховое пюре с кунжутом 90 г ×2. Назначение: походы, поездки и выезды на природу; залить кипятком, готовить 10 минут. На порцию указано: картофель 377,7 ккал/13 г белка/53,4 г углеводов; макароны 286,7/14,5/41,9; гаспачо 214,3/18/29,3; гороховое пюре 291,2/18,7/43,6.
  - Теги: purpose:hiking_food; item_type:food_bundle; sport:hiking; distance:not_applicable; audience:outdoor_recreationists; audience:tourists; package_weight:90_g; buyer_weight:not_specified; price:1500_uah

- **112 · RE89457 · Набір «Характер воїна» — абонемент на 3 місяці · снимок: 1 500 UAH.** [Официальная карточка](https://raceexpert.com.ua/index.php?route=product/product&product_id=7156). Состав: участие в клубе на 3 месяца; медаль «Озброєні волею»; брелоки Fighter, Drone 2.0 и гильза. Назначение/аудитория: патриотический подарок военным, ветеранам и коллекционерам; спорт не указан. Состав взят из сохранённой официальной карточки от 2026-11-06.
  - Теги: purpose:patriotic_gift; item_type:club_membership_bundle; sport:not_sport_specific; distance:not_applicable; duration:3_months; audience:collectors; audience:military_personnel; audience:veterans; buyer_weight:not_specified; price:1500_uah

- **113 · RE89456 · Набір «Стук серця» — абонемент на 3 місяці · снимок: 1 500 UAH.** [Официальная карточка](https://raceexpert.com.ua/index.php?route=product/product&product_id=7155). Состав: участие в клубе на 3 месяца; медаль «Патріотичний пульс»; брелоки Fighter, Drone 2.0 и гильза. Назначение/аудитория: патриотический подарок с военной тематикой; спорт не указан. Состав взят из сохранённой официальной карточки от 2026-11-06.
  - Теги: purpose:patriotic_gift; item_type:club_membership_bundle; sport:not_sport_specific; distance:not_applicable; duration:3_months; audience:collectors; audience:military_personnel; audience:veterans; buyer_weight:not_specified; price:1500_uah

- **114 · RE89451 · Набір «Відновлення після тренування» — абонемент на 3 місяці · снимок: 1 500 UAH.** [Официальная карточка](https://raceexpert.com.ua/index.php?route=product/product&product_id=7150). Состав: клуб на 3 месяца; полотенце 135×70 см; Source Naturals Ultra-Mag, 60 таблеток; Hydria Perform, 4 стика; SiS GO Isotonic Gel 60 мл (карточка дублирует/повторяет строку с гелем, количество неясно). Назначение: гидратация и углеводное восстановление активных людей и бегунов; дистанция не указана. Неясность количества гелей сохранена по официальной карточке.
  - Теги: purpose:post_workout_recovery; item_type:club_membership_bundle; sport:not_sport_specific; distance:not_applicable; duration:3_months; contains:magnesium; contains:electrolytes; contains:carbohydrates; audience:active_people; audience:runners; buyer_weight:not_specified; price:1500_uah; data_quality:component_quantity_ambiguous

- **115 · RE11801 · Набір «Підготовка до забігу» · снимок: 1 500 UAH.** [Официальная карточка](https://raceexpert.com.ua/ru/nabor-podgotovka-k-zabegu-2). Состав: беговая кепка «Run for Help Ukraine»; пояс для стартового номера с 6 петлями для гелей/батончиков; бутылка 600 мл; белые носки 40–42. Назначение/аудитория: подготовка к беговому старту для новичков и опытных участников марафонов. Число километров и точный формат забега не указаны.
  - Теги: purpose:race_preparation; item_type:equipment_bundle; sport:running; race_format:marathon; distance:unspecified; shoe_size:40-42; audience:marathon_runners; buyer_weight:not_specified; price:1500_uah

- **116 · RE88957 · Набір «Фокус і продуктивність» · снимок: 1 305 UAH.** [Официальная карточка](https://raceexpert.com.ua/7014-nabir-fokus-i-produktivnist-re88957-1-669-grn-re88957-f). Состав: Mind Shi 4Mushroom 1 000 мг, 60 капсул; NOW Foods Methyl B12 1 000 мкг, 100 пастилок; батончик с кордицепсом 40 г (12,29 г белка, 139 ккал). Назначение/аудитория: концентрация, продуктивность и энергия для спортсменов, студентов и людей с интенсивной умственной работой. Карточка показывает 1 500 UAH против 1 305 UAH в снимке.
  - Теги: purpose:focus_and_productivity; item_type:supplement_bundle; sport:not_sport_specific; distance:not_applicable; contains:vitamin_b12; contains:protein; audience:athletes; audience:students; buyer_weight:not_specified; price:1305_uah; data_quality:live_price_differs

- **118 · RE11525 · Набір «Природний сон з грибами Race Expert Club» — абонемент на 3 місяці · снимок: 1 485 UAH.** [Официальная карточка](https://raceexpert.com.ua/ru/nabor-5). Состав: клуб на 3 месяца; Reishi 1 000 мг, 60 капсул; мелатонин 3 мг, 60 капсул; Nutriversum GABA, 60 капсул. Назначение: сон и восстановление; отдельный вид спорта не указан. Карточка показывает 1 500 UAH против 1 485 UAH в снимке.
  - Теги: purpose:sleep_and_recovery; item_type:club_membership_bundle; sport:not_sport_specific; distance:not_applicable; duration:3_months; contains:reishi; contains:melatonin; contains:gaba; buyer_weight:not_specified; price:1485_uah; data_quality:live_price_differs

- **119 · RE11796 · Набір «М'язи в тонусі Race Expert Club» — абонемент на 3 місяці · снимок: 985 UAH.** [Официальная карточка](https://raceexpert.com.ua/ru/nabor-myshcy-v-tonuse). Состав: клуб на 3 месяца; порошок BCAA+Gluta без сахара 500 г; мини-шейкер 300 мл. Порция содержит 5 080 мг аминокислот; мерная порция 6 г разводится в 250 мл воды. Назначение: регулярные тренировки для спортсменов и активных людей; конкретный спорт не указан. Карточка показывает 1 500 UAH против 985 UAH в снимке.
  - Теги: purpose:muscle_support; item_type:club_membership_bundle; sport:not_sport_specific; distance:not_applicable; duration:3_months; package_weight:500_g; contains:amino_acids; audience:active_people; audience:athletes; buyer_weight:not_specified; price:985_uah; data_quality:live_price_differs

- **120 · RE11797 · Набір «Швидке відновлення Race Expert Club» — абонемент на 3 місяці · снимок: 1 500 UAH.** [Официальная карточка](https://raceexpert.com.ua/6956-nabir-shvidke-vidnovlennya-re11797-1-819-grn-re11797-si). Состав: клуб на 3 месяца; Nutriversum L-GLUTAMINE 500 г; Sponser Recovery Drink клубника-банан 60 г ×2; мини-шейкер 300 мл. Назначение: восстановление после тренировок для спортсменов и регулярно тренирующихся. Инструкция: глютамин 5 г на 200 мл; напиток 40 г на 300 мл после нагрузки.
  - Теги: purpose:post_workout_recovery; item_type:club_membership_bundle; sport:not_sport_specific; distance:not_applicable; duration:3_months; package_weight:500_g; contains:glutamine; contains:amino_acids; audience:athletes; audience:regular_trainees; audience:trainees; buyer_weight:not_specified; price:1500_uah

- **121 · RE88964 · Набір «Розум і сила 2.0 Race Expert Club» — абонемент на 3 місяці · снимок: 1 379 UAH.** [Официальная карточка](https://raceexpert.com.ua/7022-nabir-rozum-i-sila-20-re88964-1-559-grn-re88964-sila-i). Состав: клуб на 3 месяца; креатин OstroVit 500 г (125 порций; мерная ложка 4 г даёт 3,4 г моногидрата креатина/3 г креатина); кордицепс 700 мг, 60 капсул; мини-шейкер 300 мл; печенье Crava 74 г, 14 г белка. Назначение: поддержка физической работоспособности при регулярной физической нагрузке. Карточка показывает 1 500 UAH против 1 379 UAH в снимке.
  - Теги: purpose:physical_performance; item_type:club_membership_bundle; sport:not_sport_specific; distance:not_applicable; duration:3_months; package_weight:500_g; contains:creatine; contains:cordyceps; contains:protein; audience:athletes; buyer_weight:not_specified; price:1379_uah; data_quality:live_price_differs

- **122 · RE88946 · Набір «Гідратація тренувань Race Expert Club» — абонемент на 3 місяці · снимок: 1 500 UAH.** [Официальная карточка](https://raceexpert.com.ua/7007-nabir-gidrataciya-trenuvan-re88946-1-575-grn-re88946-si). Состав: клуб на 3 месяца; электролиты Hydria Daily, 8 стиков (1 стик на 500–850 мл воды; натрий, калий, магний, кальций, витамины C/B5/B6/B12); гели SiS Go + Electrolyte 60 мл ×4 (22 г углеводов каждый; 118 мг Na, 9,5 мг K, 1,5 мг Mg); стеклянная бутылка 530 мл. Назначение/активность: бег, велоспорт и фитнес, длительные/интенсивные тренировки. Точная дистанция не задана.
  - Теги: purpose:training_hydration; item_type:club_membership_bundle; sport:running; sport:cycling; sport:general_fitness; distance:unspecified; duration:3_months; contains:electrolytes; contains:carbohydrates; audience:cyclists; audience:fitness_participants; audience:runners; buyer_weight:not_specified; price:1500_uah

- **123 · RE11685 · Набір «Комплекс для активного життя Race Expert Club» — абонемент на 3 місяці · снимок: 1 500 UAH.** [Официальная карточка](https://raceexpert.com.ua/6878-nabir-kompleks-dlya-aktivnogo-zhittya-re11685-1-535-grn). Состав: клуб на 3 месяца; Swanson Triple Magnesium 400 мг, 100 капсул; Cordyceps DRUMn’BADS 700 мг, 60 капсул; NOW Omega-3 1 000 мг, 30 софтгелей ×2. Назначение: активный образ жизни, упражнения и физическая/умственная нагрузка; аудитория — спортсмены и активные люди. Вид спорта не указан.
  - Теги: purpose:daily_activity_support; item_type:club_membership_bundle; sport:not_sport_specific; distance:not_applicable; duration:3_months; contains:magnesium; contains:cordyceps; contains:omega_3; audience:active_people; audience:athletes; buyer_weight:not_specified; price:1500_uah

- **124 · RE11674 · Набір «Внутрішній баланс Race Expert Club» — абонемент на 3 місяці · снимок: 1 449 UAH.** [Официальная карточка](https://raceexpert.com.ua/ru/nabor-vnutrennij-balans). Состав: VPLab Magnesium Citrate, 90 софтгелей; Mind Shi Lion’s Mane 1 000 мг, 60 капсул; NOW Foods 5-HTP 50 мг, 30 капсул. Назначение: эмоциональный баланс, ясность, сон и восстановление при стрессе и высокой физической/умственной нагрузке; отдельный вид спорта не указан. Карточка показывает 1 500 UAH против 1 449 UAH в снимке.
  - Теги: purpose:mood_balance_and_sleep; item_type:club_membership_bundle; sport:not_sport_specific; distance:not_applicable; duration:3_months; contains:magnesium; contains:lion_s_mane; contains:5_htp; buyer_weight:not_specified; price:1449_uah; data_quality:live_price_differs

- **125 · RE11743 · Набір «Максимальна продуктивність Race Expert Club» — абонемент на 3 місяці · снимок: 1 500 UAH.** [Официальная карточка](https://raceexpert.com.ua/6889-nabir-maksimalna-produktivnist-re11743-1-665-grn-re1174). Состав: клуб на 3 месяца; Swanson B-50, 100 капсул; Lion’s Mane DRUMn’BADS 700 мг, 60 капсул; Lipobar 50 г ×4 (каждый: 16,5 г белка, 7,8 г клетчатки, 1,6 г углеводов). Назначение/аудитория: продуктивность в спорте и повседневной жизни; спортсмены, студенты и люди с высокой умственной нагрузкой.
  - Теги: purpose:productivity; item_type:club_membership_bundle; sport:not_sport_specific; distance:not_applicable; duration:3_months; contains:vitamin_b; contains:lion_s_mane; contains:protein; audience:athletes; audience:students; buyer_weight:not_specified; price:1500_uah

- **126 · Nabir_1101 · Набір «Антитривожність 2.0 Race Expert Club» — абонемент на 3 місяці · снимок: 1 500 UAH.** [Официальная карточка](https://raceexpert.com.ua/6088-nabir-antitrivozhnist-20-1-633-grn-nabir-1101-nabori). Состав: клуб на 3 месяца; батончики с рейши 40 г ×2 (более 12 г белка каждый); красный мухомор 500 мг, 60 капсул; рейши 700 мг, 60 капсул. Назначение в формулировке карточки: управление стрессом/эмоциональный баланс и восстановление; аудитория — люди с высокой психоэмоциональной нагрузкой и спортсмены в интенсивных тренировках. Медицинские эффекты не добавлялись.
  - Теги: purpose:mood_balance_and_recovery; item_type:club_membership_bundle; sport:not_sport_specific; distance:not_applicable; duration:3_months; audience:athletes; buyer_weight:not_specified; price:1500_uah

- **127 · Nabir_1124 · Набір «Дитяча турбота Race Expert Club» — абонемент на 3 місяці · снимок: 1 149 UAH.** [Официальная карточка](https://raceexpert.com.ua/ru/nabor-detskaya-zabota). Состав: клуб на 3 месяца; Nutriversum Kid Vita Gummies клубника, 60 жевательных таблеток (карточка указывает 2 в день с 3 лет); NOW DHA Chewables 100 мг, 60 штук (2 в день); карманный футляр для витаминов. Назначение по формулировке продавца: ежедневная поддержка роста детей; состав рассчитан на детскую аудиторию. Это позиционирование карточки, а не медицинский вывод. Спорт не указан. Карточка показывает 1 500 UAH против 1 149 UAH в снимке.
  - Теги: purpose:daily_child_support; item_type:supplement_bundle; sport:not_sport_specific; distance:not_applicable; duration:3_months; contains:dha; audience:children_3_plus; buyer_weight:not_specified; price:1149_uah; data_quality:live_price_differs

- **128 · Nabir_1134 · Набір «Чиста енергія та рух Race Expert Club» — абонемент на 3 місяці · снимок: 1 500 UAH.** [Официальная карточка](https://raceexpert.com.ua/ru/nabor-chistaya-energiya-i-dvizhenie). Состав: клуб на 3 месяца; Mind Shi Chaga 1 000 мг, 60 капсул; белые носки Race Expert 43–45 ×2; бутылка 600 мл; Myprotein Baked Cookie 75 г ×2. Назначение: энергия/восстановление при ежедневной активности и тренировках; отдельный вид спорта не указан.
  - Теги: purpose:energy_and_activity; item_type:club_membership_bundle; sport:not_sport_specific; distance:not_applicable; duration:3_months; shoe_size:43-45; audience:active_people; buyer_weight:not_specified; price:1500_uah

- **129 · RE11821 · Набір «Мінеральний тонус Race Expert Club» — абонемент на 3 місяці · снимок: 1 375 UAH.** [Официальная карточка](https://raceexpert.com.ua/6973-nabir-mineralnij-tonus-re11821-1-525-grn-re11821-shoden). Состав: клуб на 3 месяца; Life Extension Only Trace Minerals, 90 капсул (цинк, медь, марганец, хром, молибден, бор, ванадий); VPLab Magnesium Citrate, 90 софтгелей. Назначение: активный образ жизни, физическая и психоэмоциональная нагрузка. Карточка показывает 1 500 UAH против 1 375 UAH в снимке.
  - Теги: purpose:mineral_support; item_type:club_membership_bundle; sport:not_sport_specific; distance:not_applicable; duration:3_months; contains:minerals; contains:magnesium; audience:active_people; audience:athletes; buyer_weight:not_specified; price:1375_uah; data_quality:live_price_differs

- **130 · RE11816 · Набір «Легкість після їжі Race Expert Club» — абонемент на 3 місяці · снимок: 1 319 UAH.** [Официальная карточка](https://raceexpert.com.ua/6967-nabir-legkist-pislya-yizhi-re11816-1-555-grn-re11816-sh). Состав: абонемент клуба на 3 месяца; NOW Foods Super Enzymes, 90 капсул; Nutriversum Artichoke, 30 капсул. Назначение: пищеварительный комфорт после еды, в том числе при плотном/нерегулярном рационе; спорт не указан. Карточка показывает 1 500 UAH против 1 319 UAH в снимке.
  - Теги: purpose:digestive_comfort_after_meals; item_type:club_membership_bundle; sport:not_sport_specific; distance:not_applicable; duration:3_months; contains:digestive_enzymes; contains:artichoke; buyer_weight:not_specified; price:1319_uah; data_quality:live_price_differs

- **131 · RE11814 · Набір «Комфорт травлення Race Expert Club» — абонемент на 3 місяці · снимок: 1 189 UAH.** [Официальная карточка](https://raceexpert.com.ua/6964-nabir-komfort-travlennya-re11814-1-595-grn-re11814-shod). Состав: шелуха подорожника NOW Foods Psyllium Husks Whole 454 г; Nutriversum Artichoke, 30 капсул. Назначение: увеличение клетчатки, регулярная работа кишечника и комфорт пищеварения; аудитория — люди, желающие добавить клетчатку или имеющие нерегулярный/плотный рацион. Карточка показывает 1 500 UAH против 1 189 UAH в снимке.
  - Теги: purpose:digestive_comfort; item_type:club_membership_bundle; sport:not_sport_specific; distance:not_applicable; duration:3_months; contains:fiber; contains:artichoke; audience:people_seeking_fiber; buyer_weight:not_specified; price:1189_uah; data_quality:live_price_differs

- **132 · RE11515 · Набір «Старт із добавками Race Expert Club» — абонемент на 3 місяці · снимок: 1 125 UAH.** [Официальная карточка](https://raceexpert.com.ua/6763-nabir-start-iz-dobavkami-re11515-1-645-grn-re11515-shod). Состав: абонемент клуба на 3 месяца; MIAMI VIBES Multi Vitamin, 100 таблеток; NOW D3 2 000 IU, 120 софтгелей; NOW Zinc Gluconate 50 мг, 100 таблеток. Назначение: простая база добавок при повышенной физической/умственной нагрузке; конкретный вид спорта не указан. Карточка показывает 1 500 UAH против 1 125 UAH в снимке.
  - Теги: purpose:basic_supplement_support; item_type:club_membership_bundle; sport:not_sport_specific; distance:not_applicable; duration:3_months; contains:vitamin_d3; contains:zinc; contains:multivitamin; buyer_weight:not_specified; price:1125_uah; data_quality:live_price_differs

- **133 · RE11514 · Набір «Кістки, м’язи і нерви Race Expert Club» — абонемент на 3 місяці · снимок: 1 435 UAH.** [Официальная карточка](https://raceexpert.com.ua/6762-nabir-kistki-myazi-i-nervi-re11514-1-805-grn-re11514-sh). Состав: по текущему перечню карточки — Puritan’s Pride Chelated Ca/Mg/Zn, 100 капсул; Nutriversum D3+K2, 60 капсул; NOW Omega-3 1 000 мг, 30 софтгелей ×2. Назначение: кости, мышцы, физическая активность и восстановление; вид спорта не указан. **Конфликт состава:** более ранний официальный поисковый фрагмент показывал другой бренд Ca/Mg/Zn и одну упаковку Omega-3; в карточке указаны состав выше. Цена карточки — 1 500 UAH против 1 435 UAH в снимке.
  - Теги: purpose:bone_muscle_nervous_support; item_type:club_membership_bundle; sport:not_sport_specific; distance:not_applicable; duration:3_months; contains:calcium; contains:magnesium; contains:zinc; contains:vitamin_d3; contains:omega_3; audience:active_people; audience:trainees; buyer_weight:not_specified; price:1435_uah; data_quality:composition_conflict; data_quality:live_price_differs

- **134 · Nabir_1103 · Набір «Відновлення ресурсів 2.0 Race Expert Club» — абонемент на 3 місяці · снимок: 1 500 UAH.** [Официальная карточка](https://raceexpert.com.ua/6090-nabir-vidnovlennya-resursiv-20-1-633-grn-nabir-1103). Состав: клуб на 3 месяца; батончики с рейши 40 г ×2 (более 12 г белка каждый); ежовик 700 мг, 60 капсул; рейши 700 мг, 60 капсул. Назначение/аудитория по карточке: восстановление и повседневная работоспособность при физической/умственной нагрузке или стрессе; спортсмены и занятые люди. Конкретный спорт не указан.
  - Теги: purpose:recovery_support; item_type:club_membership_bundle; sport:not_sport_specific; distance:not_applicable; duration:3_months; contains:lion_s_mane; contains:reishi; audience:athletes; audience:busy_people; buyer_weight:not_specified; price:1500_uah

- **135 · Nabir_1102 · Набір «Здоров’я та енергія 2.0 Race Expert Club» — абонемент на 3 місяці · снимок: 1 500 UAH.** [Официальная карточка](https://raceexpert.com.ua/ru/nabor-energiya-i-tonus). Состав: абонемент клуба на 3 месяца; батончики Reishi по 40 г ×2; DRUMn’BADS Cordyceps 700 мг, 60 капсул; Reishi 700 мг, 60 капсул. Назначение: поддержка энергии, иммунитета и восстановления в повседневной активности; конкретный спорт не указан.
  - Теги: purpose:daily_energy_support; item_type:club_membership_bundle; sport:not_sport_specific; distance:not_applicable; duration:3_months; contains:cordyceps; contains:reishi; buyer_weight:not_specified; price:1500_uah

- **136 · RE89021 · Набір «Ресурс активного дня Race Expert Club» — абонемент на 3 місяці · снимок: 1 500 UAH.** [Официальная карточка](https://raceexpert.com.ua/7032-nabir-resurs-aktivnogo-dnya-re89021-1-535-grn-re89021-s). Состав: клуб на 3 месяца; D3+K2 2 000 IU + 75 мкг, 60 капсул; Olimp Chela-Mag B6 Ashwagandha+Ginseng, 30 капсул; Olimp Mag B6 shot 25 мл; Olimp L-Carnitine Caffeine Extreme Shot 25 мл (доза кофеина не указана). Назначение: ресурс в активный день и при тренировках; отдельная дисциплина не названа.
  - Теги: purpose:active_day_support; item_type:club_membership_bundle; sport:not_sport_specific; distance:not_applicable; duration:3_months; contains:vitamin_d3; contains:magnesium; contains:caffeine; contains:l_carnitine; contains:ashwagandha; contains:ginseng; audience:active_people; audience:athletes; buyer_weight:not_specified; price:1500_uah

- **137 · RE89018 · Набір «Баланс вуглеводного обміну» · снимок: 1 500 UAH.** [Официальная карточка](https://raceexpert.com.ua/7029-nabir-balans-vuglevodnogo-obminu-re89018-1-599-grn-re89). Состав: NOW Foods Inositol 500 мг ×100; Swanson Chromium Picolinate 200 мкг ×200; Nutriversum Apple Cider Caps ×90. Назначение по карточке: поддержка углеводного обмена/рациона; спорт не указан. Официальный сохранённый снимок карточки — 2026-11-06; текущая цена отдельно не зафиксирована.
  - Теги: purpose:carbohydrate_metabolism_support; item_type:supplement_bundle; sport:not_sport_specific; distance:not_applicable; contains:inositol; contains:chromium; contains:apple_cider_vinegar; buyer_weight:not_specified; price:1500_uah

- **138 · RE88960 · Набір «Харчовий баланс» · снимок: 1 315 UAH.** [Официальная карточка](https://raceexpert.com.ua/7017-nabir-harchovij-balans-re88960-1-535-grn-re88960-shoden). Состав: по нумерованному списку — Nutriversum Apple Cider Caps ×90; Olimp Artichoke Premium ×30; Swanson Milk Thistle 500 мг ×100; Swanson Triphala 500 мг ×100. Назначение: поддержка пищевого баланса/пищеварения; конкретный спорт не указан. **Конфликт карточки:** во вступлении также упоминается мультивитаминный комплекс для женщин, которого нет в нумерованном составе. В официальном листинге наблюдалась цена 1 500 UAH против 1 315 UAH в снимке; сама карточка ранее возвращала cache miss.
  - Теги: purpose:nutrition_digestive_support; item_type:supplement_bundle; sport:not_sport_specific; distance:not_applicable; contains:apple_cider_vinegar; contains:artichoke; contains:milk_thistle; contains:triphala; buyer_weight:not_specified; price:1315_uah; data_quality:composition_conflict; data_quality:live_price_differs

- **139 · RE88959 · Набір «Підтримка травлення та печінки» · снимок: 1 455 UAH.** [Официальная карточка](https://raceexpert.com.ua/7016-nabir-pidtrimka-travlennya-ta-pechinki-re88959-1-679-gr). Состав: Nutriversum Apple Cider Caps ×90; Swanson Artichoke Extract 250 мг ×60; Milk Thistle 500 мг ×100; Triphala 500 мг ×100. Назначение: поддержка пищеварения и печени; спорт не указан. Состав получен из сохранённой официальной карточки от 2026-11-06; текущая цена отдельно не зафиксирована.
  - Теги: purpose:digestive_liver_support; item_type:supplement_bundle; sport:not_sport_specific; distance:not_applicable; contains:apple_cider_vinegar; contains:artichoke; contains:milk_thistle; contains:triphala; buyer_weight:not_specified; price:1455_uah

- **140 · RE11818 · Набір «Серце й антиоксидантний захист» · снимок: 1 319 UAH.** [Официальная карточка](https://raceexpert.com.ua/6969-nabir-serce-j-antioksidantnij-zahist-re11818-1-599-grn). Состав: NOW Omega-3 1 000 мг ×30; NOW CoQ10 100 мг ×30; Nutriversum Curcuma Ginger ×60; NOW D3 2 000 IU ×30. Назначение: поддержка сердечно-сосудистой системы и антиоксидантная поддержка; карточка упоминает спортсменов и активных людей. Состав из сохранённой официальной карточки от 2026-11-06; текущая цена отдельно не зафиксирована.
  - Теги: purpose:cardiovascular_antioxidant_support; item_type:supplement_bundle; sport:not_sport_specific; distance:not_applicable; contains:omega_3; contains:coq10; contains:curcumin; contains:ginger; contains:vitamin_d3; audience:active_people; audience:athletes; buyer_weight:not_specified; price:1319_uah

- **141 · RE11815 · Набір «Підтримка печінки» · снимок: 1 305 UAH.** [Официальная карточка](https://raceexpert.com.ua/6965-nabir-pidtrimka-pechinki-re11815-1-549-grn-re11815-shod). Состав: NOW Foods Liver Refresh, 90 капсул; Nutriversum Curcuma Ginger, 60 капсул. Назначение/аудитория: поддержка печени, пищеварения и антиоксидантной защиты для спортсменов и активных людей при физической нагрузке, стрессе или несбалансированном питании; отдельный спорт не указан. Карточка показывает 1 500 UAH против 1 305 UAH в снимке.
  - Теги: purpose:liver_support; item_type:supplement_bundle; sport:not_sport_specific; distance:not_applicable; contains:curcumin; contains:ginger; audience:active_people; audience:athletes; buyer_weight:not_specified; price:1305_uah; data_quality:live_price_differs

- **142 · RE11521 · Набір «Старт у спорті» · снимок: 1 500 UAH.** [Официальная карточка](https://raceexpert.com.ua/6770-nabir-start-u-sporti-re11521-1-605-grn-re11521-sila-i-m). Состав: Nutriversum Creatine, 300 г; BCAA Shot 60 мл ×3; шейкер Myprotein 600 мл; Pocket Pack Vitamin Case Small. Назначение/аудитория: базовое питание и аксессуары для новичков или тех, кто начинает тренироваться; спортивная дисциплина не названа.
  - Теги: purpose:beginning_training; item_type:supplement_bundle; sport:not_sport_specific; distance:not_applicable; package_weight:300_g; contains:creatine; contains:amino_acids; audience:beginners; buyer_weight:not_specified; price:1500_uah

- **143 · RE11511 · Набір «Мінімум для зайнятої людини» · снимок: 1 500 UAH.** [Официальная карточка](https://raceexpert.com.ua/6759-nabir-minimum-dlya-zajnyatoyi-lyudini-re11511-1-605-grn). Состав: по нумерованному списку — NOW Omega-3 1 000 мг, 30 софтгелей ×2; органайзер NOW 7 Day Pill Case. Во вступлении карточки мультивитамин назван третьим элементом, но его нет в нумерованном/извлечённом списке — состав конфликтует. Назначение/аудитория: простой базовый режим для занятых людей с быстрым темпом жизни; конкретный спорт не указан.
  - Теги: purpose:daily_basics_for_busy_people; item_type:supplement_bundle; sport:not_sport_specific; distance:not_applicable; contains:omega_3; audience:busy_people; buyer_weight:not_specified; price:1500_uah; data_quality:composition_conflict

- **144 · Nabir_1133 · Набір «Базова підтримка організму Race Expert Club» — абонемент на 3 місяці · снимок: 1 500 UAH.** [Официальная карточка](https://raceexpert.com.ua/ru/nabor-bazovaya-podderzhka-organizma). Состав: по нумерованному перечню — абонемент клуба на 3 месяца; белые носки Race Expert, размер 43–45, 2 пары; шейкер Brave U 700 мл. Во вступлении карточки упомянут мультивитаминный комплекс, отсутствующий в перечне компонентов — состав конфликтует. Назначение: ежедневная базовая поддержка; спорт не указан.
  - Теги: purpose:daily_basic_support; item_type:club_membership_bundle; sport:not_sport_specific; distance:not_applicable; duration:3_months; shoe_size:43-45; buyer_weight:not_specified; price:1500_uah; data_quality:composition_conflict

- **145 · Nabir_1132 · Набір «Підтримка та відновлення» · снимок: 1 309 UAH.** [Официальная карточка](https://raceexpert.com.ua/6619-nabir-pidtrimka-ta-vidnovlennya-1-793-grn-nabir-1132-na). Состав: MIAMI VIBES Multi Vitamin, 100 таблеток; Nutriversum Vitamin B-Complex, 30 таблеток; Swanson Boswellia Double Strength 800 мг, 60 капсул. Назначение: поддержка при активном распорядке, восстановлении и стрессе; карточка называет спортсменов, активных людей и бегунов. Карточка показывает 1 500 UAH против 1 309 UAH в снимке.
  - Теги: purpose:support_and_recovery; item_type:supplement_bundle; sport:not_sport_specific; distance:not_applicable; contains:multivitamin; contains:vitamin_b; contains:boswellia; audience:active_people; audience:athletes; audience:runners; buyer_weight:not_specified; price:1309_uah; data_quality:live_price_differs

- **146 · Nabir_1126 · Набір «Основа Енергії та Відновлення» · снимок: 1 500 UAH.** [Официальная карточка](https://raceexpert.com.ua/6600-nabir-osnova-energiyi-ta-vidnovlennya-1-659-grn-nabir-1). Состав: Nutriversum Iron, 30 таблеток; Nutriversum Vitamin D3+K2, 60 капсул; Nutriversum Magnesium Bisglycinate, 60 капсул. Назначение: ежедневная поддержка энергии, костей/мышц, нервной системы и восстановления; карточка упоминает активных людей и спортсменов при нагрузках. Текущая цена карточки — 1 500 UAH.
  - Теги: purpose:energy_and_recovery; item_type:supplement_bundle; sport:not_sport_specific; distance:not_applicable; contains:iron; contains:vitamin_d3; contains:vitamin_k2; contains:magnesium; audience:active_people; audience:athletes; buyer_weight:not_specified; price:1500_uah

- **147 · Nabir_1118 · Набір «Міцна основа 2.0» · снимок: 1 500 UAH.** [Официальная карточка](https://raceexpert.com.ua/6164-nabir-mentalnij-relaks-1-500-grn-nabir-1117-nabori). Состав: Nutrend 100% Whey Protein 400 г; шейкер Myprotein 600 мл; батончик Myprotein Impact Protein Bar ×3 (по 20 г белка; карточка также указывает 236 ккал и 8,6 г клетчатки); Myprotein Protein Brownie ×3 (по 23 г белка, 286 ккал и 4 г сахара). Назначение: регулярные тренировки, восстановление и поддержка мышц; конкретная дисциплина не указана. URL содержит «1117», но поле артикула официальной карточки — Nabir_1118, как в снимке.
  - Теги: purpose:regular_training_nutrition; item_type:supplement_bundle; sport:not_sport_specific; distance:not_applicable; package_weight:400_g; contains:protein; audience:regular_trainees; audience:trainees; buyer_weight:not_specified; price:1500_uah; data_quality:sku_url_mismatch

- **148 · RE88963 · Набір «Передтренувальний тонус Race Expert Club» — абонемент на 3 місяці · снимок: 1 500 UAH.** [Официальная карточка](https://raceexpert.com.ua/7021-nabir-peredtrenuvalnij-tonus-re88963-1-525-grn-re88963). Состав: клуб на 3 месяца; VPLab L-Carnitine Concentrate 500 мл (1 200 мг L-карнитина на 10 мл); Nutriversum AAKG Shot 60 мл ×2 (в каждом 6 000 мг AAKG + 1 000 мг бета-аланина); Nutriversum PWO Shot 60 мл (содержит кофеин, доза не указана); шейкер Brave U 700 мл. Назначение/аудитория: подготовка к интенсивной тренировке для спортсменов и активных людей; дисциплина не названа.
  - Теги: purpose:pre_workout_preparation; item_type:club_membership_bundle; sport:not_sport_specific; distance:not_applicable; duration:3_months; contains:l_carnitine; contains:amino_acids; contains:caffeine; audience:active_people; audience:athletes; buyer_weight:not_specified; price:1500_uah

- **149 · RE11800 · Набір «Запас сили» · снимок: 1 500 UAH.** [Официальная карточка](https://raceexpert.com.ua/6951-nabir-zapas-sili-re11800-2-905-grn-re11800-sila-i-masa). Состав: Nutriversum Creatine Monohydrate Creapure 500 г; мини-шейкер 300 мл. Назначение/аудитория: силовые показатели и физическая работоспособность спортсменов при интенсивных нагрузках. Карточка указывает 3 г креатина на порцию; 3,4 г порошка разводить в 200 мл, принимать до тренировки или в дни отдыха.
  - Теги: purpose:strength_and_performance; item_type:supplement_bundle; sport:strength_training; distance:not_applicable; package_weight:500_g; contains:creatine; audience:athletes; buyer_weight:not_specified; price:1500_uah

- **150 · RE11786 · Набір «Тренувальний ресурс Race Expert Club» — абонемент на 3 місяці · снимок: 1 285 UAH.** [Официальная карточка](https://raceexpert.com.ua/6946-nabir-trenuvalnij-resurs-re11786-1-639-grn-re11786-sila). Состав: абонемент клуба на 3 месяца; Nutriversum BCAA 2:1:1 Sugar Free, 360 г; Hydria Perform, 5 стиков; шейкер Myprotein 600 мл. Назначение: тренировки, гидратация и восстановление при физической нагрузке; конкретная дисциплина не указана. Карточка показывает 1 500 UAH против 1 285 UAH в снимке.
  - Теги: purpose:training_support; item_type:club_membership_bundle; sport:not_sport_specific; distance:not_applicable; duration:3_months; package_weight:360_g; contains:amino_acids; contains:electrolytes; audience:trainees; buyer_weight:not_specified; price:1285_uah; data_quality:live_price_differs

### Записи 151–210

- **151 · RE11811 · “Набір «М'язове відновлення»” · 1 500 грн по срезу.** [Официальная карточка](https://raceexpert.com.ua/6975-nabir-myazove-vidnovlennya-re11811-2-145-grn-re11811-si).
  Состав: Nutriversum BCAA + GLUTA без сахара чёрная смородина 500 g ×1 (10 g порция); SPONSER Recovery Drink клубника/банан 60 g ×1; Nutriversum Mini Shaker 300 ml ×1.
  Назначение по описанию набора: поддержка мышц, восстановление и восполнение энергии после интенсивной нагрузки.
  Аудитория/занятия: спортсмены и активные люди; силовые тренировки, бег, фитнес, CrossFit и высокоинтенсивные занятия.
  Указанные метрики/состав: порция — 10 g.
  Неопределённость: существенной неопределённости нет.
  Теги: purpose:muscle_recovery; sport:strength_training; sport:running; sport:general_fitness; sport:crossfit; distance:not_applicable; price:1500_uah; buyer_weight:not_specified; item_type:supplement_bundle; audience:athletes; audience:active_people; contains:bcaa; contains:glutamine.

- **152 · RE11688 · “Набір «Набір маси»” · 1 149 грн по срезу.** [Официальная карточка](https://raceexpert.com.ua/6882-nabir-nabir-masi-re11688-1-985-grn-re11688-za-potrebami).
  Состав: Kevin Levrone Anabolic Mass 1,000 g ×1; MIAMI VIBES Pure Creatine Monohydrate 300 g ×1.
  Назначение по описанию набора: набор мышечной массы и силы, а также восстановление во время интенсивных силовых тренировок.
  Занятия/аудитория: силовые тренировки; люди, стремящиеся набрать мышечную массу.
  Указанные метрики/состав: порция Anabolic Mass: 42 g белка и 54 g углеводов; в гейнере также указан креатин.
  Расхождение цены: официальная карточка Race Expert на 2026-11-06 показывала 1 500 грн, цена в каталоге на эту дату — 1 149 грн. Источник — карточка по ссылке выше.
  Неопределённость: существенной неопределённости нет.
  Теги: purpose:muscle_gain; sport:strength_training; distance:not_applicable; price:1149_uah; buyer_weight:not_specified; item_type:supplement_bundle; audience:muscle_gain_trainers; contains:creatine; data_quality:live_price_differs.

- **153 · RE11665 · “Набір «Активний рух»” · 1 500 грн по срезу.** [Официальная карточка](https://raceexpert.com.ua/6836-nabir-aktivnij-ruh-re11665-1-555-grn-re11665-aksesuari).
  Состав: скоростная скакалка со счётчиком ×1; двойной ролик для пресса ×1; массажный мяч ×1; кольцевой кистевой эспандер EasyFit Ring 32 kg ×1; Myprotein Layered Bar 60 g ×8 (20.4 g белка/батончик).
  Назначение по описанию набора: поддержка активного образа жизни, фитнеса и тренировок в разных местах.
  Занятия/аудитория: домашние, заловые и уличные тренировки; активные люди.
  Указанные метрики/состав: скакалка: 5–20 min; массаж: 1–3 min.
  Неопределённость: существенной неопределённости нет.
  Теги: purpose:active_fitness; sport:general_fitness; distance:not_applicable; price:1500_uah; buyer_weight:not_specified; item_type:equipment_bundle; item_type:snack_bundle.

- **154 · RE11664 · “Набір «Домашній фітнес та тонус»” · 1 500 грн по срезу.** [Официальная карточка](https://raceexpert.com.ua/ru/nabor-domashnij-fitnes-i-tonus).
  Состав: EasyFit скоростная скакалка 280 cm ×1; EasyFit HARD текстильнаяя лента-эспандер ×1; EasyFit Grid Roller 45 cm ×1; бутылка Race Expert ×1.
  Назначение по описанию набора: домашние фитнес-тренировки и поддержание тонуса.
  Занятия: домашние тренировки.
  Указанные метрики/состав: использование скакалки: 5–20 min.
  Неопределённость: существенной неопределённости нет.
  Теги: purpose:home_fitness; sport:general_fitness; distance:not_applicable; price:1500_uah; buyer_weight:not_specified; item_type:equipment_bundle.

- **155 · RE11663 · “Набір «Йога та пілатес»” · 1 500 грн по срезу.** [Официальная карточка](https://raceexpert.com.ua/ru/nabor-joga-i-pilates).
  Состав: EasyFit Polarity Stone коврик ×1; EasyFit EASY текстильнаяя лента-эспандер ×1; Myprotein Layered Bar Triple Chocolate Fudge 60 g ×7 (>20 g белка/батончик).
  Назначение по описанию набора: занятия йогой, пилатесом, растяжкой и домашние тренировки.
  Занятия/аудитория: йога, пилатес, растяжка и домашние тренировки.
  Неопределённость: существенной неопределённости нет.
  Теги: purpose:yoga_pilates; sport:yoga; sport:pilates; sport:stretching; distance:not_applicable; price:1500_uah; buyer_weight:not_specified; item_type:equipment_bundle; item_type:snack_bundle.

- **156 · RE11520 · “Набір «Тестостерон і витривалість»” · 1 500 грн по срезу.** [Официальная карточка](https://raceexpert.com.ua/ru/nabor-2).
  Состав: Nutrend Test Bomb 90 капсул ×1; Nutriversum Creatine 300 g ×1; Nutriversum BCAA Shot лимон-лайм 60 ml ×2.
  Назначение по описанию набора: поддержка спортивных результатов, силы и восстановления (позиционирование карточки).
  Аудитория/занятия: мужчины и активно тренирующиеся люди (согласно описанию набора).
  Указанные метрики/состав: креатин: 3.4 g на порцию; в Test Bomb перечислены tribulus, maca, ashwagandha, ginseng, arginine, magnesium и zinc.
  Неопределённость: существенной неопределённости нет.
  Теги: purpose:strength_endurance; sport:strength_training; distance:not_applicable; price:1500_uah; buyer_weight:not_specified; item_type:supplement_bundle; audience:men; audience:active_trainers; contains:creatine; contains:tribulus; contains:maca; contains:ashwagandha; contains:ginseng; contains:arginine; contains:magnesium; contains:zinc.

- **157 · Nabir_1115 · “Набір “Спортивний фундамент”” · 1 500 грн по срезу.** [Официальная карточка](https://raceexpert.com.ua/ru/nabor-sportivnyj-fundament).
  Состав: Nutriversum creatine (3.4 g/порция; количество в упаковке не указано); Nutriversum Magnesium Bisglycinate; Nutriversum Multi Vitamin Caps Pro (13 витаминов).
  Назначение по описанию набора: базовая поддержка регулярных тренировок и высоких нагрузок.
  Аудитория/занятия: в описании прямо названы военные, спортсмены и начинающие заниматься фитнесом.
  Неопределённость: Количество креатина в упаковке и количество других продуктов в доступном тексте карточки не указаны.
  Теги: purpose:training_foundation; sport:strength_training; sport:general_fitness; distance:not_applicable; price:1500_uah; buyer_weight:not_specified; item_type:supplement_bundle; audience:military; audience:athletes; audience:beginner_fitness; contains:creatine; contains:magnesium; contains:multivitamin; data_quality:composition_quantity_unspecified.

- **158 · RE11654 · “Набір «Імунний щит»” · 1 500 грн по срезу.** [Официальная карточка](https://raceexpert.com.ua/6826-nabir-imunnij-shit-re11654-1-519-grn-re11654-shodenna-b).
  Состав: NOW C-1000 100 капсул ×1; NOW Zinc Picolinate 50 mg/60 капсул ×1; Nutriversum D3+K2 60 капсул ×1.
  Назначение по описанию набора: поддержка иммунитета согласно позиционированию набора.
  Спорт: специализация не указана.
  Неопределённость: существенной неопределённости нет.
  Теги: purpose:immune_support; sport:not_sport_specific; distance:not_applicable; price:1500_uah; buyer_weight:not_specified; item_type:supplement_bundle; contains:vitamin_c; contains:zinc; contains:vitamin_d3; contains:vitamin_k2.

- **159 · RE11512 · “Набір «Захист і тонус» по програмі "Ветеранський спорт"” · 1 500 грн по срезу.** [Официальная карточка](https://raceexpert.com.ua/ru/nabor-zashita-i-tonus).
  Состав: Solaray Zinc + Copper 100 капсул; Solaray Vitamin C з Bioflavonoids 100 капсул; Nutriversum Vitamin D3+K2 60 капсул.
  Назначение по описанию набора: ежедневная поддержка иммунитета, энергии и общего тонуса согласно описанию продавца.
  Аудитория: указана программа «Ветеранський спорт»; спортивная дисциплина не названа.
  Неопределённость: В карточке не указано, для какого вида спорта предназначен набор.
  Теги: purpose:immune_energy_support; sport:not_sport_specific; distance:not_applicable; price:1500_uah; buyer_weight:not_specified; item_type:supplement_bundle; audience:veteran_sport_program; contains:zinc; contains:copper; contains:vitamin_c; contains:vitamin_d3; contains:vitamin_k2.

- **160 · RE88943 · “Набір «Концентрація в дорозі Race Expert Club» — абонемент на 3 месяца” · 1 469 грн по срезу.** [Официальная карточка](https://raceexpert.com.ua/7005-nabir-koncentraciya-v-dorozi-re88943-1-779-grn-re88943).
  Состав: абонемент Race Expert Club на 3 месяца; Lion’s Mane 700 mg ×60 капсул; Now Foods Acetyl-L-Carnitine 500 mg ×50 капсул; OMNOM батончик 50 g ×1; Hydria Daily стики с электролитами ×3.
  Назначение по описанию набора: поддержка концентрации в поездках, за рулём, на работе и во время активного отдыха.
  Занятия/аудитория: поездки, вождение и работа; спортивная дисциплина не указана.
  Расхождение цены: официальная карточка Race Expert на 2026-11-06 показывала 1 500 грн, цена в каталоге на эту дату — 1 469 грн. Источник — карточка по ссылке выше.
  Неопределённость: существенной неопределённости нет.
  Теги: purpose:travel_concentration; sport:not_sport_specific; distance:not_applicable; price:1469_uah; buyer_weight:not_specified; item_type:supplement_bundle; item_type:snack_bundle; audience:drivers; audience:travelers; duration:3_months; contains:acetyl_l_carnitine; contains:electrolytes; data_quality:live_price_differs.

- **161 · RE11691 · “Набір «Фокус-формула 2.0 Race Expert Club» — абонемент на 3 месяца” · 1 500 грн по срезу.** [Официальная карточка](https://raceexpert.com.ua/ru/nabor-fokus-formula-20).
  Состав: абонемент Race Expert Club на 3 месяца; DRUMn’BADS Lion’s Mane 700 mg ×60 капсул; Swanson Balance B-50 ×100 капсул; Now Foods Omega-3 1,000 mg ×30 мягкие капсулы.
  Назначение по описанию набора: поддержка концентрации, продуктивности и памяти согласно описанию набора.
  Спортивное назначение не указано.
  Неопределённость: существенной неопределённости нет.
  Теги: purpose:focus_productivity; sport:not_sport_specific; distance:not_applicable; price:1500_uah; buyer_weight:not_specified; item_type:supplement_bundle; duration:3_months; contains:lions_mane; contains:vitamin_b; contains:omega_3.

- **162 · RE11802 · “Набір «Витривалість без спраги Race Expert Club» — абонемент на 3 месяца” · 1 500 грн по срезу.** [Официальная карточка](https://raceexpert.com.ua/6952-nabir-vitrivalist-bez-spragi-re11802-3-309-grn-re11802).
  Состав: абонемент Race Expert Club на 3 месяца; Nutriversum EAA Sugar Free 500 g ×1; Hydria Perform стики с электролитами ×5; Brave U Shaker 700 ml ×1.
  Назначение по описанию набора: поддержка гидратации и выносливости во время интенсивных занятий.
  Занятия: бег, велоспорт, силовые тренировки и HIIT.
  Указанные метрики/состав: 12 g EAA растворяют в 300–400 ml; Hydria stick — в 500–850 ml.
  Неопределённость: существенной неопределённости нет.
  Теги: purpose:hydration_endurance; sport:running; sport:cycling; sport:strength_training; sport:hiit; distance:not_applicable; price:1500_uah; buyer_weight:not_specified; item_type:supplement_bundle; item_type:equipment_bundle; duration:3_months; contains:eaa; contains:electrolytes.

- **163 · Nabir_1131 · “Набір «Протеїновий заряд»” · 1 500 грн по срезу.** [Официальная карточка](https://raceexpert.com.ua/ru/nabor-proteinovyj-zaryad).
  Состав: Nutriversum PURE Whey Pro 500 g ×1 (23 g белка/порция; 30 g растворяют в 250 ml воде/молоке); Race Expert & DRUMn’BADS Reishi клюква батончик 40 g ×1; Cordyceps coffee батончик 40 g ×1; Lion’s Mane кокос батончик 40 g ×2.
  Назначение по описанию набора: протеиновые перекусы и восстановление для регулярно тренирующихся.
  Занятия/аудитория: регулярные тренировки и активный день; конкретный вид спорта не указан.
  Неопределённость: существенной неопределённости нет.
  Теги: purpose:protein_recovery_snacks; sport:general_fitness; distance:not_applicable; price:1500_uah; buyer_weight:not_specified; item_type:supplement_bundle; item_type:snack_bundle; contains:whey_protein; contains:reishi; contains:cordyceps; contains:lions_mane.

- **164 · RE11660 · “Набір «Марафонець»” · 1 500 грн по срезу.** [Официальная карточка](https://raceexpert.com.ua/ru/nabor-marafonec).
  Состав: Nutriversum Creatine 300 g ×1; PF 30 Gel 51 g ×5.
  Назначение по описанию набора: подготовка и питание во время бега на длинные дистанции.
  Аудитория/занятия: бегуны на длинные дистанции; в описании названы полумарафон и марафон.
  Формат: в описании указаны полумарафон и марафон; точное расстояние в километрах не приведено.
  Указанные метрики/состав: карточка указывает 1–3 gel/hour в зависимости от длительности и интенсивности.
  Неопределённость: существенной неопределённости нет.
  Теги: purpose:long_distance_running; sport:running; race_format:half_marathon; race_format:marathon; distance:unspecified; price:1500_uah; buyer_weight:not_specified; item_type:supplement_bundle; item_type:snack_bundle; audience:long_distance_runners; contains:creatine.

- **165 · RE11662 · “Набір «Релакс та відновлення»” · 1 500 грн по срезу.** [Официальная карточка](https://raceexpert.com.ua/ru/nabor-relaks-i-vosstanovlenie).
  Состав: EasyFit Grid Roller 45 cm ×1; EasyFit PVC твердий массажный мяч 7.5 cm ×1; Kuznetsov коврик + подушкою/чохлом ×1.
  Назначение по описанию набора: восстановление после тренировок, расслабление мышц и отдых после активного дня.
  Аудитория/занятия: спортсмены и активные люди; также названы йога, пилатес и фитнес.
  Указанные метрики/состав: роллер: 1–3 min; мяч: 2–5 min; коврик: 10–20 min.
  Неопределённость: существенной неопределённости нет.
  Теги: purpose:recovery_mobility; sport:general_fitness; sport:yoga; sport:pilates; distance:not_applicable; price:1500_uah; buyer_weight:not_specified; item_type:equipment_bundle; audience:athletes; audience:active_people.

- **166 · RE11657 · “Набір «Омега + сонце» по програмі” · 1 315 грн по срезу.** [Официальная карточка](https://raceexpert.com.ua/6828-nabir-omega-sonce-re11657-1-555-grn-re11657-shodenna-ba).
  Состав: Now Foods Omega-3 1,000 mg, 30 мягкие капсулы ×5 (EPA 360 mg + DHA 240 mg per 2 капсули); Now Foods Vitamin D3 1,000 IU жевательные таблетки з фруктовим смаком 180 таблеток ×1.
  Назначение по описанию набора: ежедневная поддержка иммунитета, сердца, мозга и костей согласно описанию набора.
  Аудитория: указана программа «Ветеранський спорт»; отдельный вид спорта не назван.
  Расхождение цены: официальная карточка Race Expert на 2026-11-06 показывала 1 500 грн, цена в каталоге на эту дату — 1 315 грн. Источник — карточка по ссылке выше.
  Неопределённость: В тексте карточки упомянута таблетница, но её нет в нумерованном перечне состава.
  Теги: purpose:daily_wellbeing; sport:not_sport_specific; distance:not_applicable; price:1315_uah; buyer_weight:not_specified; item_type:supplement_bundle; audience:veteran_sport_program; contains:omega_3; contains:vitamin_d3; data_quality:live_price_differs; data_quality:composition_ambiguity.

- **167 · RE11651 · “Набір «Нічний ZMA»” · 1 500 грн по срезу.** [Официальная карточка](https://raceexpert.com.ua/ru/nabor-nochnoj-zma).
  Состав: Now Foods ZMA 800 mg ×90 капсул; Myprotein Layered Bar 60 g ×4 (20.4 g белка/батончик).
  Назначение по описанию набора: поддержка сна и восстановления при высоких физических нагрузках.
  Аудитория/занятия: спортсмены и активные люди с высокой физической нагрузкой.
  Неопределённость: существенной неопределённости нет.
  Теги: purpose:sleep_recovery; sport:general_fitness; distance:not_applicable; price:1500_uah; buyer_weight:not_specified; item_type:supplement_bundle; item_type:snack_bundle; audience:athletes; audience:active_people; contains:zinc; contains:magnesium.

- **168 · RE11658 · “Набір «Рівновага дня»” · 1 455 грн по срезу.** [Официальная карточка](https://raceexpert.com.ua/ru/nabor-ravnovesie-dnya).
  Состав: VPLab Magnesium Citrate 90 мягкие капсулы; Nutriversum GABA 60 капсул (750 mg/cap); DRUMn’BADS адаптогенные жевательных конфет ×15; Hydria Perform стік з електролітами ×1.
  Назначение по описанию набора: поддержка равновесия, концентрации и восстановления согласно описанию набора.
  Специализированное спортивное применение не указано.
  Неопределённость: существенной неопределённости нет.
  Теги: purpose:stress_balance; sport:not_sport_specific; distance:not_applicable; price:1455_uah; buyer_weight:not_specified; item_type:supplement_bundle; contains:magnesium; contains:gaba; contains:electrolytes.

- **169 · Nabir_1112 · “Набір «Баланс і спокій» по програмі "Ветеранський спорт"” · 1 500 грн по срезу.** [Официальная карточка](https://raceexpert.com.ua/6099-nabir-formula-spokoyu-1-554-grn-nabir-1112-gribi-ta-ada).
  Состав: DRUMn’BADS Amanita червоного мухомора 500 mg, розничная упаковка 60 капсул ([карточка товара Race Expert](https://raceexpert.com.ua/6335-muhomor-chervonij-drumnbads-500-mg-60-kapsul-0-grn-re53)); DRUMn’BADS адаптогенные жевательные конфеты, 3 упаковки ×15.
  Назначение по описанию набора: поддержка спокойствия, баланса и сна согласно позиционированию продавца.
  Аудитория: указана программа «Ветеранський спорт»; дисциплина не названа.
  Неопределённость: карточка набора не указывает множитель упаковок Amanita; 60 капсул — размер одной розничной упаковки товара.
  Теги: purpose:stress_balance_sleep; sport:not_sport_specific; distance:not_applicable; price:1500_uah; buyer_weight:not_specified; item_type:supplement_bundle; audience:veteran_sport_program; contains:amanita; data_quality:composition_quantity_unspecified.

- **170 · RE11524 · “Набір «Нервова система під захистом Race Expert Club» — абонемент на 3 месяца” · 1 500 грн по срезу.** [Официальная карточка](https://raceexpert.com.ua/6776-nabir-nervova-sistema-pid-zahistom-re11524-1-589-grn-re).
  Состав: Mind Shi CBD Oil Isolate клубника 1,000 mg/10 ml; Nutriversum GABA ×60 капсул; Now Foods Pocket Pack Vitamin Case Small.
  Назначение по описанию набора: поддержка спокойствия и эмоционального равновесия в условиях стресса согласно описанию набора.
  Спортивное применение не указано.
  Неопределённость: существенной неопределённости нет.
  Теги: purpose:stress_calm; sport:not_sport_specific; distance:not_applicable; price:1500_uah; buyer_weight:not_specified; item_type:supplement_bundle; item_type:equipment_bundle; duration:3_months; contains:cbd; contains:gaba.

- **171 · Nabir_1116 · “Набір «Внутрішня рівновага Race Expert Club» — абонемент на 3 месяца” · 1 500 грн по срезу.** [Официальная карточка](https://raceexpert.com.ua/6163-nabir-vnutrishnya-rivnovaga-2-046-grn-nabir-1116).
  Состав: абонемент Race Expert Club на 3 месяца; Nutriversum Magnesium Bisglycinate (товарная упаковка 60 капсул); Nutriversum Multi Vita (60 таблеток); Nutriversum Omega-3 (размер товарной упаковки и множитель набора не подтверждены).
  Назначение по описанию набора: общее самочувствие и внутреннее равновесие при длительном стрессе.
  Аудитория: военные в условиях длительного стресса и спортсмены в интенсивных циклах. В клубе есть материалы о беге и тренировках, но набор имеет общее назначение.
  Неопределённость: карточка набора перечисляет каждый из трёх продуктов одной строкой без множителей; для Omega-3 не удалось подтвердить фасовку.
  Теги: purpose:wellbeing_balance; sport:not_sport_specific; distance:not_applicable; price:1500_uah; buyer_weight:not_specified; item_type:supplement_bundle; item_type:club_membership_bundle; audience:military; audience:athletes; duration:3_months; contains:magnesium; contains:omega_3; contains:multivitamin; data_quality:composition_quantity_unspecified.

- **172 · Nabir_1110 · “Набір «Зменшення стресу та регуляція сну Race Expert Club» — абонемент на 3 месяца” · 1 500 грн по срезу.** [Официальная карточка](https://raceexpert.com.ua/6097-zmenshennya-stresu-ta-regulyaciya-snu-2-632-grn-nabir-1).
  Состав: абонемент Race Expert Club на 3 месяца; Mind Shi Reishi Mushroom 1,000 mg (розничная упаковка 60 капсул); Mind Shi CBD Oil Isolate, апельсин, 1,000 mg в бутылке 10 ml ([данные производителя](https://www.mindshi.com/cbd-oil-isolate-1000mg-orange)); Myprotein Layered Bars ×3: Triple Chocolate Fudge, Vanilla Birthday Cake и White Gold.
  Назначение по описанию набора: поддержка сна и снижение стресса согласно позиционированию продавца.
  Отдельный вид спорта не указан.
  Неопределённость: карточка набора не указывает множители упаковок Reishi и CBD; фасовка товара Reishi — 60 капсул, CBD — 10 ml.
  Теги: purpose:stress_sleep_support; sport:not_sport_specific; distance:not_applicable; price:1500_uah; buyer_weight:not_specified; item_type:supplement_bundle; item_type:snack_bundle; item_type:club_membership_bundle; duration:3_months; contains:reishi; contains:cbd; data_quality:composition_quantity_unspecified.

- **173 · Nabir_1106 · “Набір «Комплекс для загального зміцнення, спокою та імунітету Race Expert Club» — абонемент на 3 міс” · 1 500 грн по срезу.** [Официальная карточка](https://raceexpert.com.ua/6093-kompleks-dlya-zagalnogo-zmicnennya-spokoyu-ta-imunitetu).
  Состав: Mind Shi Reishi Mushroom 1,000 mg ×1; Myprotein Layered Bar ×3 (вкусы перечислены; >20 g белка/батончик); Mind Shi Shiitake Mushroom 1,000 mg ×1.
  Назначение по описанию набора: ежедневная общая поддержка, иммунитет и равновесие при физических и психоэмоциональных нагрузках.
  Отдельный вид спорта не указан.
  Неопределённость: В доступном перечне состава отдельно не указан абонемент Race Expert Club, несмотря на пометку Club в названии.
  Теги: purpose:immune_balance; sport:not_sport_specific; distance:not_applicable; price:1500_uah; buyer_weight:not_specified; item_type:supplement_bundle; item_type:snack_bundle; item_type:club_membership_bundle; contains:reishi; contains:shiitake; duration:3_months.

- **174 · RE11805 · “Набір «М'язове відновлення»” · 1 500 грн по срезу.** [Официальная карточка](https://raceexpert.com.ua/6966-nabir-myazove-vidnovlennya-re11805-2-145-grn-re11805-si).
  Состав: Nutriversum BCAA+GLUTA без сахара 500 g ×1; SPONSER Recovery Drink клубника/банан 60 g ×1; Nutriversum Mini Shaker 300 ml ×1.
  Назначение по описанию набора: восстановление мышц после интенсивной нагрузки.
  Занятия/аудитория: силовые тренировки, бег, фитнес, CrossFit и другие высокоинтенсивные занятия; спортсмены.
  Неопределённость: существенной неопределённости нет.
  Теги: purpose:muscle_recovery; sport:strength_training; sport:running; sport:general_fitness; sport:crossfit; distance:not_applicable; price:1500_uah; buyer_weight:not_specified; item_type:supplement_bundle; audience:athletes; audience:active_people; contains:bcaa; contains:glutamine.

- **175 · Nabir_1111 · “Набір «Спокійна концентрація» по програмі "Ветеранський спорт"” · 1 500 грн по срезу.** [Официальная карточка](https://raceexpert.com.ua/6098-nabir-koncentraciya-ta-yasnist-1-554-grn-nabir-1111-gri).
  Состав: DRUMn’BADS Lion’s Mane 700 mg, розничная упаковка 60 капсул ([карточка товара Race Expert](https://raceexpert.com.ua/6780-yizhovik-grebinchastij-drumnbads-700-mg-60-kapsul-48202)); DRUMn’BADS адаптогенные жевательные конфеты, 3 упаковки ×15.
  Назначение по описанию набора: поддержка спокойной концентрации согласно описанию набора.
  Аудитория: указана программа «Ветеранський спорт»; конкретный вид спорта не назван.
  Неопределённость: карточка набора не указывает множитель упаковок Lion’s Mane; 60 капсул — размер одной розничной упаковки товара.
  Теги: purpose:calm_focus; sport:not_sport_specific; distance:not_applicable; price:1500_uah; buyer_weight:not_specified; item_type:supplement_bundle; audience:veteran_sport_program; contains:lions_mane; data_quality:composition_quantity_unspecified.

- **176 · RE11516 · “Набір «Набір маси»” · 1 500 грн по срезу.** [Официальная карточка](https://raceexpert.com.ua/6764-nabir-nabir-masi-re11516-1-749-grn-re11516-sila-i-masa).
  Состав: Nutriversum PURE Whey Pro 500 g ×1; Myprotein shaker 600 ml ×1; Nutriversum BCAA Shot 60 ml ×3.
  Назначение по описанию набора: набор мышечной массы и восстановление.
  Аудитория/занятия: спортсмены и тренирующиеся; отдельная дисциплина не выделена.
  Неопределённость: существенной неопределённости нет.
  Теги: purpose:muscle_gain_recovery; sport:general_fitness; distance:not_applicable; price:1500_uah; buyer_weight:not_specified; item_type:supplement_bundle; item_type:equipment_bundle; audience:athletes; audience:trainers; contains:whey_protein; contains:bcaa.

- **177 · RE11813 · “Набір «Формула краси»” · 1 500 грн по срезу.** [Официальная карточка](https://raceexpert.com.ua/6963-nabir-formula-krasi-re11813-2-169-grn-re11813-shodenna).
  Состав: Nutriversum Collagen Heaven 300 g ×1 (10 g collagen на 15 g порцию); Puritan’s Pride Hair, Skin & Nails Formula 60 капсул ×1 (3,000 mcg biotin на рекомендуемую порцию).
  Назначение по описанию набора: ежедневная нутритивная поддержка кожи, волос, ногтей и соединительной ткани.
  Аудитория: общая; спортивное назначение не указано.
  Проверенная официальная карточка на 2026-11-06 показывала 1 500 грн — совпадает со срезом.
  Неопределённость: существенной неопределённости нет.
  Теги: purpose:beauty_skin_hair_nails; sport:not_sport_specific; distance:not_applicable; price:1500_uah; buyer_weight:not_specified; item_type:supplement_bundle; contains:collagen; contains:biotin.

- **178 · RE11744 · “Набір «Здоров'я шкіри Race Expert Club» — абонемент на 3 месяца” · 1 500 грн по срезу.** [Официальная карточка](https://raceexpert.com.ua/6890-nabir-zdorovya-shkiri-re11744-2-105-grn-re11744-shodenn).
  Состав: абонемент Race Expert Club на 3 месяца; Nutriversum Collagen Heaven 300 g ×1; Nutriversum VITA C+MSM лимон 150 g ×1.
  Назначение по описанию набора: поддержка кожи и соединительной ткани согласно описанию продавца.
  Спортивная аудитория не указана.
  Неопределённость: существенной неопределённости нет.
  Теги: purpose:skin_support; sport:not_sport_specific; distance:not_applicable; price:1500_uah; buyer_weight:not_specified; item_type:supplement_bundle; item_type:club_membership_bundle; duration:3_months; contains:collagen; contains:vitamin_c; contains:msm.

- **179 · RE11682 · “Набір «Жіноче здоров’я Race Expert Club» — абонемент на 3 месяца” · 1 500 грн по срезу.** [Официальная карточка](https://raceexpert.com.ua/6876-nabir-zhinoche-zdorovya-re11682-1-749-grn-re11682-shode).
  Состав: абонемент Race Expert Club на 3 месяца; VPLab Ultra Women’s Multivitamin 90 капсул ×1; NOW Foods Omega-3 1,000 mg, 30 мягкие капсулы ×1; Nutriversum Vitamin D3+K2 60 капсул ×1.
  Назначение по описанию набора: ежедневная поддержка женского здоровья, энергии и самочувствия.
  Аудитория: женщины; упомянут активный образ жизни, но дисциплина не названа.
  Проверенная официальная карточка на 2026-11-06 показывала 1 500 грн — совпадает со срезом.
  Неопределённость: существенной неопределённости нет.
  Теги: purpose:womens_health; sport:not_sport_specific; distance:not_applicable; price:1500_uah; buyer_weight:not_specified; item_type:supplement_bundle; item_type:club_membership_bundle; audience:women; duration:3_months; contains:omega_3; contains:vitamin_d3; contains:vitamin_k2.

- **180 · Nabir_1125 · “Набір «Сяйво та внутрішня енергія Race Expert Club» — абонемент на 3 месяца” · 1 500 грн по срезу.** [Официальная карточка](https://raceexpert.com.ua/6599-nabir-syajvo-ta-vnutrishnya-energiya-1-554-grn-nabir-11).
  Состав: абонемент Race Expert Club на 3 месяца; Nutriversum Zinc 30 капсул ×1; Iron 30 таблеток ×1; Biotin 30 таблеток ×1; Vitamin B-Complex 30 таблеток ×1.
  Назначение по описанию набора: поддержка красоты и энергии согласно описанию набора.
  Пол и спортивное назначение не указаны.
  Неопределённость: существенной неопределённости нет.
  Теги: purpose:beauty_energy; sport:not_sport_specific; distance:not_applicable; price:1500_uah; buyer_weight:not_specified; item_type:supplement_bundle; item_type:club_membership_bundle; duration:3_months; contains:zinc; contains:iron; contains:biotin; contains:vitamin_b.

- **181 · RE89417 · “Набір м'ясних снеків (перець, паприка) Race Expert Club — абонемент на 3 месяца” · 1 500 грн по срезу.** [Официальная карточка](https://raceexpert.com.ua/index.php?product_id=7147&route=product%2Fproduct).
  Состав: сушеные ломтики курицы с перцем и паприкой, 30 g ×16.
  Назначение по описанию набора: портативный белковый перекус после тренировки, на работе или в дороге.
  Аудитория/занятия: спортсмены и активные люди; названы работа, поездки и пешие прогулки.
  Неопределённость: существенной неопределённости нет.
  Теги: purpose:protein_snack; sport:not_sport_specific; distance:not_applicable; price:1500_uah; buyer_weight:not_specified; item_type:snack_bundle; item_type:club_membership_bundle; audience:athletes; audience:active_people; duration:3_months.

- **182 · RE89413 · “Набір м'ясних снеків (сир Гауда) Race Expert Club — абонемент на 3 месяца” · 1 500 грн по срезу.** [Официальная карточка](https://raceexpert.com.ua/index.php?product_id=7145&route=product%2Fproduct).
  Состав: сушеные ломтики курицы с сыром Gouda, 30 g ×16.
  Назначение по описанию набора: портативный белковый перекус.
  Аудитория: спортсмены и активные люди; конкретная дисциплина не названа.
  Неопределённость: существенной неопределённости нет.
  Теги: purpose:protein_snack; sport:not_sport_specific; distance:not_applicable; price:1500_uah; buyer_weight:not_specified; item_type:snack_bundle; item_type:club_membership_bundle; audience:athletes; audience:active_people; duration:3_months.

- **183 · RE89329 · “Набір «Набір м'ясних снеків М'яско ToGo Фруктово-гострий Race Expert Club» — абонемент на 3 месяца” · 1 500 грн по срезу.** [Официальная карточка](https://raceexpert.com.ua/7065-nabir-myasnih-snekiv-myasko-togo-fruktovo-gostrij-8-sht).
  Состав: 8 ×50 g упаковок вяленого мяса (свинина/курица/индейка; медово-острый вкус, традиционный вкус, вишня и апельсин вкусы).
  Назначение по описанию набора: перекус в дороге, после тренировки или работы и во время активного отдыха.
  Упомянуты обычные тренировки без указания дисциплины, а также работа, поездки и активный отдых.
  Неопределённость: Точное количество каждого вкуса/вида мяса в доступном описании не установлено.
  Теги: purpose:snack_assortment; sport:not_sport_specific; distance:not_applicable; price:1500_uah; buyer_weight:not_specified; item_type:snack_bundle; item_type:club_membership_bundle; duration:3_months.

- **184 · RE89328 · “Набір «Набір м'ясних снеків М'яско ToGo Солодко-пікантний Race Expert Club» — абонемент на 3 месяца” · 1 500 грн по срезу.** [Официальная карточка](https://raceexpert.com.ua/7064-nabir-myasnih-snekiv-myasko-togo-solodko-pikantnij-8-sh).
  Состав: 8 ×50 g упаковок вяленого мяса (курица/индейка/свинина; азиатский вкус, медово-горчичный вкус, вишня и терияки вкусы).
  Назначение по описанию набора: перекус на работе, в дороге, после тренировки или во время активного отдыха.
  Конкретная дисциплина не указана; названы работа, поездки, тренировки и активный отдых.
  Неопределённость: Точное количество каждого вкуса/вида мяса в доступном описании не установлено.
  Теги: purpose:snack_assortment; sport:not_sport_specific; distance:not_applicable; price:1500_uah; buyer_weight:not_specified; item_type:snack_bundle; item_type:club_membership_bundle; duration:3_months.

- **185 · RE89327 · “«Набір м'ясних снеків М'яско ToGo «Класика з цитрусом», 8 шт»” · 1 500 грн по срезу.** [Официальная карточка](https://raceexpert.com.ua/7063-nabir-myasnih-snekiv-myasko-togo-klasika-z-citrusom-8-s).
  Состав: 8 ×50 g: курица, традиционный вкус ×3, курица, лимон ×2, свинина, медово-горчичный вкус ×2, индейка, апельсин ×1.
  Назначение по описанию набора: ассорти снеков для перекуса; конкретная активность не указана.
  Конкретная активность не указана.
  Неопределённость: существенной неопределённости нет.
  Теги: purpose:snack_assortment; sport:not_sport_specific; distance:not_applicable; price:1500_uah; buyer_weight:not_specified; item_type:snack_bundle.

- **186 · RE89326 · “«Набір м'ясних снеків М'яско ToGo «Азійський мікс», 8 шт»” · 1 500 грн по срезу.** [Официальная карточка](https://raceexpert.com.ua/7062-nabir-myasnih-snekiv-myasko-togo-azijskij-miks-8-sht-re).
  Состав: 8 ×50 g: курица, азиатский вкус ×2, курица, лимон ×2, свинина, медово-острый вкус ×3, индейка, терияки ×1.
  Назначение по описанию набора: ассорти снеков для перекуса; конкретная активность не указана.
  Конкретная активность не указана.
  Неопределённость: существенной неопределённости нет.
  Теги: purpose:snack_assortment; sport:not_sport_specific; distance:not_applicable; price:1500_uah; buyer_weight:not_specified; item_type:snack_bundle.

- **187 · RE89325 · “Набір «Набір м'ясних снеків М'яско ToGo Дегустаційний Race Expert Club» — абонемент на 3 месяца” · 1 500 грн по срезу.** [Официальная карточка](https://raceexpert.com.ua/7061-nabir-myasnih-snekiv-myasko-togo-degustacijnij-vsi-8-sm).
  Состав: 8 different Myasko ToGo вкусы across курица, индейка и свинина.
  Назначение по описанию набора: дегустационный набор снеков.
  Конкретная активность не указана.
  Неопределённость: Количество каждого отдельного вкуса не подтверждено доступным описанием.
  Теги: purpose:snack_tasting; sport:not_sport_specific; distance:not_applicable; price:1500_uah; buyer_weight:not_specified; item_type:snack_bundle; item_type:club_membership_bundle; duration:3_months.

- **188 · RE89324 · “«Набір м'ясних снеків М'яско ToGo «Курка та индейка», 8 шт»” · 1 500 грн по срезу.** [Официальная карточка](https://raceexpert.com.ua/7060-nabir-myasnih-snekiv-myasko-togo-kurka-ta-indichka-8-sh).
  Состав: 8 ×50 g: курица, традиционный вкус ×2, азиатский вкус ×2, лимон ×2; индейка, апельсин ×1, индейка, терияки ×1.
  Назначение по описанию набора: ассорти снеков для перекуса; конкретная активность не указана.
  Конкретная активность не указана.
  Неопределённость: существенной неопределённости нет.
  Теги: purpose:snack_assortment; sport:not_sport_specific; distance:not_applicable; price:1500_uah; buyer_weight:not_specified; item_type:snack_bundle.

- **189 · RE89301 · “Набір «Набір м'ясних снеків М'яско ToGo Свинячий Race Expert Club» — абонемент на 3 месяца” · 1 500 грн по срезу.** [Официальная карточка](https://raceexpert.com.ua/7059-nabir-myasnih-snekiv-myasko-togo-svinyachij-8-sht-re893).
  Состав: абонемент Race Expert Club на 3 месяца; вяленое мясо зі свинины 50 g ×8 (медово-острый вкус ×3, медово-горчичный вкус ×2, вишня ×3).
  Назначение по описанию набора: перекус в дороге и в течение активного дня.
  Занятия/аудитория: поездки, работа и активный отдых; конкретный вид спорта не указан.
  Неопределённость: существенной неопределённости нет.
  Теги: purpose:snack_assortment; sport:not_sport_specific; distance:not_applicable; price:1500_uah; buyer_weight:not_specified; item_type:snack_bundle; item_type:club_membership_bundle; duration:3_months.

- **190 · RE89297 · “Набір «Набір м'ясних снеків М'яско ToGo Курячий Race Expert Club» — абонемент на 3 месяца” · 1 500 грн по срезу.** [Официальная карточка](https://raceexpert.com.ua/7058-nabir-myasnih-snekiv-myasko-togo-kuryachij-9-sht-re8929).
  Состав: абонемент Race Expert Club на 3 месяца; вяленое мясо з курицы 50 g ×9 (традиционный вкус ×3, азиатский вкус ×3, лимон ×3).
  Назначение по описанию набора: удобный перекус для активного дня или после тренировки.
  Занятия/аудитория: активные люди, поездки и перекус после тренировки; дисциплина не названа.
  Неопределённость: существенной неопределённости нет.
  Теги: purpose:convenient_snack; sport:not_sport_specific; distance:not_applicable; price:1500_uah; buyer_weight:not_specified; item_type:snack_bundle; item_type:club_membership_bundle; duration:3_months.

- **191 · RE88977 · “Набір «Похідна їжа 3.0 Race Expert Club» — абонемент на 3 месяца” · 1 500 грн по срезу.** [Официальная карточка](https://raceexpert.com.ua/7027-nabir-pohidna-yizha-30-re88977-1-499-grn-re88977-yizha).
  Состав: вяленое мясо индейки ЇDLO 50 g ×2; вяленое мясо курицы ЇDLO 50 g ×1; перекус из Gouda, кукурузы и орехов 90 g ×1; полента с индейкой 100 g ×1; гороховый суп с индейкой 60 g ×1; кус-кус с клюквой и орехами 100 g ×1; Crava protein cookie 74 g ×1; Myprotein Baked Cookie 75 g ×1 (13 g белка).
  Назначение по описанию набора: еда для походов, поездок, кемпинга, тренировок или пребывания вне дома.
  Аудитория: в описании прямо названы туристы, путешественники, военные и спортсмены.
  Неопределённость: существенной неопределённости нет.
  Теги: purpose:hiking_travel_meals; sport:hiking; distance:not_applicable; price:1500_uah; buyer_weight:not_specified; item_type:snack_bundle; item_type:club_membership_bundle; audience:tourists; audience:travelers; audience:military; audience:athletes; duration:3_months; contains:protein.

- **192 · RE11490 · “Набір «LipoBar Мікс»” · 1 500 грн по срезу.** [Официальная карточка](https://raceexpert.com.ua/index.php?product_id=7057&route=product%2Fproduct).
  Состав: 21 LipoBar 50 g батончиків (гранат ×5, апельсин ×4, марципан ×4, манго ×4, клубника ×4); 16.5 g белка/батончик.
  Назначение по описанию набора: удобные протеиновые перекусы после тренировки или между приёмами пищи.
  Занятия/аудитория: обычные тренировки и перекус для активных людей; конкретная дисциплина не указана.
  Неопределённость: существенной неопределённости нет.
  Теги: purpose:protein_snacks; sport:not_sport_specific; distance:not_applicable; price:1500_uah; buyer_weight:not_specified; item_type:snack_bundle; contains:protein.

- **193 · RE11519 · “Набір «Швидке відновлення після тренування Race Expert Club» — абонемент на 3 місяці” · 1 500 грн по срезу.** [Официальная карточка](https://raceexpert.com.ua/6768-nabir-shvidke-vidnovlennya-pislya-trenuvannya-re11519-1).
  Состав: абонемент Race Expert Club на 3 месяца; Nutriversum Whey Pro 500 g ×1; Nutriversum BCAA Shot 60 ml ×2; Reishi батончик 40 g ×2.
  Назначение по описанию набора: восстановление после тренировки и восполнение питательных веществ после интенсивной нагрузки.
  Аудитория/занятия: спортсмены и активные люди; конкретный вид спорта не указан.
  Неопределённость: существенной неопределённости нет.
  Теги: purpose:post_training_recovery; sport:general_fitness; distance:not_applicable; price:1500_uah; buyer_weight:not_specified; item_type:supplement_bundle; item_type:snack_bundle; item_type:club_membership_bundle; audience:athletes; audience:active_people; duration:3_months; contains:whey_protein; contains:bcaa; contains:reishi.

- **194 · Nabir_1100 · “Набір «Концентрація і пам’ять 2.0 Race Expert Club» — абонемент на 3 месяца” · 1 500 грн по срезу.** [Официальная карточка](https://raceexpert.com.ua/6087-nabir-koncentraciya-i-pamyat-20-1-633-grn-nabir-1100-na).
  Состав: абонемент Race Expert Club на 3 месяца; Reishi батончик 40 g ×2; Lion’s Mane 700 mg/60 капсул ×1; Cordyceps 700 mg/60 капсул ×1.
  Назначение по описанию набора: поддержка концентрации и памяти согласно описанию набора.
  Аудитория: спортсмены, студенты и офисные работники.
  Неопределённость: существенной неопределённости нет.
  Теги: purpose:focus_memory; sport:not_sport_specific; distance:not_applicable; price:1500_uah; buyer_weight:not_specified; item_type:supplement_bundle; item_type:snack_bundle; item_type:club_membership_bundle; audience:athletes; audience:students; audience:office_workers; duration:3_months; contains:lions_mane; contains:cordyceps; contains:reishi.

- **195 · RE11819 · “Набір «Щоденний захист дитини»” · 1 425 грн по срезу.** [Официальная карточка](https://raceexpert.com.ua/6971-nabir-shodennij-zahist-ditini-re11819-1-809-grn-re11819).
  Состав: Nutriversum Kid Vita жевательных конфет ×60; KAL Vitamin D-Rex 10 mcg/90 жувальних таблеток ×1; Nordic Naturals Daily Omega Kids/30 мягкие капсулы ×1.
  Назначение по описанию набора: ежедневный детский набор пищевых добавок.
  Аудитория: дети; спортивное назначение не указано.
  Неопределённость: существенной неопределённости нет.
  Теги: purpose:child_daily_nutrition; sport:not_sport_specific; distance:not_applicable; price:1425_uah; buyer_weight:not_specified; item_type:supplement_bundle; audience:children; contains:vitamin_d; contains:omega_3.

- **196 · RE11653 · “Набір «Вітаміни для вагітних Race Expert Club» — абонемент на 3 месяца” · 1 500 грн по срезу.** [Официальная карточка](https://raceexpert.com.ua/ru/nabor-vitaminy-dlya-beremennyh).
  Состав: Now Foods folic acid 800 mcg ×250 таблеток ×2; Now Foods Omega-3 1,000 mg, 30 мягкие капсулы ×1; Nutriversum Vitamin D3+K2 60 капсул ×1; абонемент Race Expert Club на 3 месяца.
  Назначение по описанию набора: набор добавок для женщин, которые планируют беременность или ожидают ребёнка.
  Аудитория: женщины, которые планируют беременность или ожидают ребёнка; спорт не указан.
  Неопределённость: существенной неопределённости нет.
  Теги: purpose:pregnancy_nutrition; sport:not_sport_specific; distance:not_applicable; price:1500_uah; buyer_weight:not_specified; item_type:supplement_bundle; item_type:club_membership_bundle; audience:women_planning_pregnancy; audience:pregnant_women; duration:3_months; contains:folic_acid; contains:omega_3; contains:vitamin_d3; contains:vitamin_k2.

- **197 · RE11020 · “Набір «Бігова екіпіровка»” · 1 209 грн по срезу.** [Официальная карточка](https://raceexpert.com.ua/ru/nabor-begovaya-ekipirovka).
  Состав: белые носки RE2 размер 40–44 ×2; стеклянная бутылка Race Expert 530 ml ×1; черные эластичные шнурки для бега ×1 комплект (2 отрезки шнурка + 2 фиксаторы); cordyceps coffee батончик 40 g ×2 (>12 g белка/батончик); reishi клюква батончик 40 g ×2 (~10 g белка/батончик).
  Назначение по описанию набора: аксессуары и перекусы для более комфортного бега.
  Занятия: бег; вид забега и дистанция не указаны.
  Формат/дистанция: не указаны.
  Расхождение цены: официальная карточка Race Expert на 2026-11-06 показывала 1 500 грн, цена в каталоге на эту дату — 1 209 грн. Источник — карточка по ссылке выше.
  Неопределённость: существенной неопределённости нет.
  Теги: purpose:running_gear; sport:running; race_format:unspecified; distance:unspecified; price:1209_uah; buyer_weight:not_specified; item_type:apparel_bundle; item_type:equipment_bundle; item_type:snack_bundle; audience:runners; shoe_size:40-44; data_quality:live_price_differs.

- **198 · RE89487 · “Набір «Банні рушники Шарпей: темна гама» — абонемент на 3 месяца” · 1 500 грн по срезу.** [Официальная карточка](https://raceexpert.com.ua/7171-nabir-banni-rushniki-sharpej-temna-gama-abonement-na-3).
  Состав: 3 полотенца, чёрный/тёмно-синий/зелёный, 135×70 cm каждый; 100% хлопок, 500 g/m²; абонемент Race Expert Club на 3 месяца.
  Назначение по описанию набора: полотенца для душа, тренировок, бассейна, сауны и поездок.
  Занятия: зал, плавание, сауна и поездки; набор не связан с конкретным видом спорта.
  Неопределённость: существенной неопределённости нет.
  Теги: purpose:towel_set; sport:not_sport_specific; distance:not_applicable; price:1500_uah; buyer_weight:not_specified; item_type:apparel_bundle; item_type:club_membership_bundle; duration:3_months.

- **199 · RE89486 · “Набір «Банні рушники Шарпей: класика» — абонемент на 3 месяца” · 1 500 грн по срезу.** [Официальная карточка](https://raceexpert.com.ua/7170-nabir-banni-rushniki-sharpej-klasika-abonement-na-3-mis).
  Состав: 3 полотенца, бежевый/бордовый/серый, 135×70 cm каждый, хлопок 500 g/m²; абонемент Race Expert Club на 3 месяца.
  Назначение по описанию набора: полотенца для дома, зала, бассейна, сауны или поездок.
  Занятия/аудитория: дом, зал, бассейн, сауна и поездки; спортсмены упомянуты в описании.
  Неопределённость: существенной неопределённости нет.
  Теги: purpose:towel_set; sport:not_sport_specific; distance:not_applicable; price:1500_uah; buyer_weight:not_specified; item_type:apparel_bundle; item_type:club_membership_bundle; duration:3_months.

- **200 · RE89481 · “Набір «Подарунок для активних днів» — абонемент на 3 месяца” · 1 500 грн по срезу.** [Официальная карточка](https://raceexpert.com.ua/7165-nabir-podarunok-dlya-aktivnih-dniv-abonement-na-3-misya).
  Состав: абонемент Race Expert Club на 3 месяца; “Patriotic Pulse” медаль; black сумка-органайзер; белые носки RE2 размер 40–44.
  Назначение по описанию набора: подарочный набор для активных дней, прогулок и поездок.
  Занятия: прогулки, поездки и активный отдых.
  Неопределённость: существенной неопределённости нет.
  Теги: purpose:active_day_gift; sport:walking; sport:active_recreation; distance:not_applicable; price:1500_uah; buyer_weight:not_specified; item_type:gift_bundle; item_type:apparel_bundle; item_type:club_membership_bundle; duration:3_months; shoe_size:40-44.

- **201 · RE11024 · “Набір «Подарунок спортсмену Race Expert Club» — абонемент на 3 месяца” · 1 500 грн по срезу.** [Официальная карточка](https://raceexpert.com.ua/ru/nabor-podarok-sportsmenu).
  Состав: абонемент Race Expert Club на 3 месяца; носки RE2, белые и тёмные, размер 40–44 ×1 пара кожного размеру; из латунной гильзы брелок ×2; NOW 7-day pill case; MIAMI VIBES multivitamin 100 tabs.
  Назначение по описанию набора: подарок для бегунов, спортсменов и активных людей.
  Аудитория: в описании прямо названы бегуны, спортсмены и активные люди.
  Неопределённость: существенной неопределённости нет.
  Теги: purpose:athlete_gift; sport:not_sport_specific; distance:not_applicable; price:1500_uah; buyer_weight:not_specified; item_type:gift_bundle; item_type:apparel_bundle; item_type:supplement_bundle; item_type:club_membership_bundle; audience:athletes; audience:runners; duration:3_months; shoe_size:40-44.

- **202 · Nabir_1063 · “Набір «Пульс нації»” · 1 500 грн по срезу.** [Официальная карточка](https://raceexpert.com.ua/6085-nabir-puls-naciyi-1-803-grn-nabir-1063-vijskovim).
  Состав: “Patriotic Pulse” медаль; брелок из гильзы; брелок с изображением дрона; F-16 брелок, 35 mm.
  Назначение по описанию набора: патриотический подарок; символическое назначение набора.
  Аудитория: военные и люди на пути борьбы; спортивное назначение не указано.
  Неопределённость: существенной неопределённости нет.
  Теги: purpose:patriotic_gift; sport:not_sport_specific; distance:not_applicable; price:1500_uah; buyer_weight:not_specified; item_type:gift_bundle; audience:military; audience:supporters.

- **203 · Nabir_1064 · “Набір «Україна починається з тебе Race Expert Club» — абонемент на 3 месяца” · 1 500 грн по срезу.** [Официальная карточка](https://raceexpert.com.ua/6084-nabir-puls-naciyi-1-853-grn-nabir-1063-nabori).
  Состав: медаль “Україна в тобі” (зеркальное изображение герба); брелок из гильзы; брелок с изображением дрона; F-16 брелок, 35 mm.
  Назначение по описанию набора: патриотический подарок и символ Украины.
  Спортивное назначение не указано.
  Неопределённость: URL карточки содержит устаревшие название и SKU (“Пульс нації”, Nabir_1063), тогда как название и SKU в каталоге — Nabir_1064/«Україна починається з тебе».
  Теги: purpose:patriotic_gift; sport:not_sport_specific; distance:not_applicable; price:1500_uah; buyer_weight:not_specified; item_type:gift_bundle; item_type:club_membership_bundle; duration:3_months; data_quality:card_title_sku_mismatch.

- **204 · Nabir_1062 · “Набір «Небесна варта Race Expert Club» — абонемент на 3 месяца” · 1 500 грн по срезу.** [Официальная карточка](https://raceexpert.com.ua/6083-nabir-nebesna-varta-1-853-grn-nabir-1062-nabori).
  Состав: “Гвардія небес” медаль с изображением дрона и снаряда; брелок из гильзы; брелок с изображением дрона; F-16 брелок, 35 mm.
  Назначение по описанию набора: патриотический подарок для военных и людей на пути борьбы.
  Аудитория: военные и люди на пути борьбы; спортивное назначение не указано.
  Неопределённость: существенной неопределённости нет.
  Теги: purpose:patriotic_gift; sport:not_sport_specific; distance:not_applicable; price:1500_uah; buyer_weight:not_specified; item_type:gift_bundle; item_type:club_membership_bundle; audience:military; audience:supporters; duration:3_months.

- **205 · Nabir_1061 · “Набір «Народжені вільними Race Expert Club» — абонемент на 3 месяца” · 1 500 грн по срезу.** [Официальная карточка](https://raceexpert.com.ua/6082-nabir-narodzheni-vilnimi-1-853-grn-nabir-1061-nabori).
  Состав: “Незалежність – це каждый з нас” медаль (движущийся дрон); брелок из гильзы; брелок с изображением дрона; F-16 брелок, 35 mm.
  Назначение по описанию набора: патриотический подарок и символ участия в независимости Украины.
  Аудитория: военные и люди на пути борьбы; спортивное назначение не указано.
  Неопределённость: существенной неопределённости нет.
  Теги: purpose:patriotic_gift; sport:not_sport_specific; distance:not_applicable; price:1500_uah; buyer_weight:not_specified; item_type:gift_bundle; item_type:club_membership_bundle; audience:military; audience:supporters; duration:3_months.

- **206 · RE89452 · “Набір «Підготовка до тренувань у залі» — абонемент на 3 месяца” · 1 500 грн по срезу.** [Официальная карточка](https://raceexpert.com.ua/index.php?product_id=7151&route=product%2Fproduct).
  Состав: абонемент Race Expert Club на 3 месяца; полотенце 135×70 cm; OstroVit Creatine Monohydrate (масса упаковки не указана); Nutriversum FLOW PWO Shot 60 ml, кофеин 200 mg на шот ([карточка Race Expert](https://raceexpert.com.ua/6583-peredtrenuvalnij-napij-nutriversum-flow-pwo-shot-grejpf)); Nutriversum PWO Shot 60 ml, кофеин 200 mg на шот ([данные производителя](https://nutriversum.com/pwo-shot-bubblegum)); Nutriversum AAKG Shot 60 ml, без кофеина ([данные производителя](https://nutriversum.org/pre-Workout-formulas/DARK_-_AAKG_SHOT/)). В карточке набора указано по одной позиции каждого шота; всего два кофеиносодержащих шота, 400 mg кофеина по составу набора.
  Назначение по описанию набора: подготовка к тренировкам в зале и силовым занятиям.
  Занятия: тренировки в зале и силовые занятия.
  Неопределённость: масса упаковки креатина не указана; кофеин рассчитан по двум шотам по 200 mg каждый.
  Теги: purpose:gym_training_prep; sport:general_fitness; sport:strength_training; distance:not_applicable; price:1500_uah; buyer_weight:not_specified; item_type:equipment_bundle; item_type:supplement_bundle; item_type:club_membership_bundle; duration:3_months; contains:creatine; contains:caffeine; contains:amino_acids; caffeine_per_set:400_mg; data_quality:composition_quantity_unspecified.

- **207 · RE89331 · “Набір м'ясних снеків М'яско ToGo Курка та свинка Race Expert Club — абонемент на 3 месяца” · 1 500 грн по срезу.** [Официальная карточка](https://raceexpert.com.ua/nabir-myasnih-snekiv-myasko-togo-kurka-ta-svinka-8-sht-1).
  Состав: абонемент Race Expert Club на 3 месяца; вяленое мясо 50 g ×8: курица, лимон ×2, свинина, медово-острый вкус ×2, свинина, медово-горчичный вкус ×2, свинина, вишня ×2.
  Назначение по описанию набора: удобный перекус в дороге, на работе или после тренировки.
  Занятия/аудитория: поездки, работа и активный отдых; конкретный вид спорта не указан.
  Неопределённость: существенной неопределённости нет.
  Теги: purpose:convenient_snack; sport:not_sport_specific; distance:not_applicable; price:1500_uah; buyer_weight:not_specified; item_type:snack_bundle; item_type:club_membership_bundle; duration:3_months.

- **208 · RE89330 · “«Набір м'ясних снеків М'яско ToGo «Цитрус та Азія», 8 шт»” · 1 500 грн по срезу.** [Официальная карточка](https://raceexpert.com.ua/nabir-myasnih-snekiv-myasko-togo-citrus-ta-aziya-8-sht).
  Состав: 8 ×50 g вяленое мясо: курица, азиатский вкус ×3, курица, лимон ×2, свинина, медово-острый вкус ×1, индейка, апельсин ×1, индейка, терияки ×1.
  Назначение по описанию набора: портативное ассорти снеков для поездок, работы, активного отдыха или после тренировки.
  Конкретная дисциплина не указана; в карточке названы поездки, работа, перекус после тренировки и активный отдых.
  Неопределённость: существенной неопределённости нет.
  Теги: purpose:snack_assortment; sport:not_sport_specific; distance:not_applicable; price:1500_uah; buyer_weight:not_specified; item_type:snack_bundle.

- **209 · RE11788 · “Набір «LipoBar Мікс Race Expert Club» — абонемент на 3 месяца” · 1 500 грн по срезу.** [Официальная карточка](https://raceexpert.com.ua/nabir-lipobar-miks-race-expert-club-abonement-na-3-misyaci).
  Состав: абонемент Race Expert Club на 3 месяца; LipoBar 50 g ×21 (гранат ×5, апельсин ×4, марципан ×4, манго ×4, клубника ×4); 16.5 g белка/батончик.
  Назначение по описанию набора: ассорти протеиновых перекусов для активного дня, после тренировки или между приёмами пищи.
  Обычный перекус; отдельная дисциплина не указана.
  Неопределённость: существенной неопределённости нет.
  Теги: purpose:protein_snack; sport:not_sport_specific; distance:not_applicable; price:1500_uah; buyer_weight:not_specified; item_type:snack_bundle; item_type:club_membership_bundle; duration:3_months; contains:protein.

- **210 · SKU не указан · “Набір «Підготовка до забігу»” · 1 500 грн по срезу.** [Официальная карточка](https://raceexpert.com.ua/nabir-pidgotovka-do-zabigu).
  Состав: Race Expert кепка ×1; пояс для номера с 6 петлями ×1; 600 ml бутылка ×1; белые носки размер 40–42 ×1 пара.
  Назначение по описанию набора: аксессуары для подготовки к забегу.
  Аудитория/занятия: начинающие и опытные бегуны.
  Формат/дистанция: подготовка к забегу; точный формат и дистанция не указаны.
  Неопределённость: SKU в каталоге не указан; дистанция забега в километрах не приведена.
  Теги: purpose:race_preparation; sport:running; race_format:unspecified; distance:unspecified; price:1500_uah; buyer_weight:not_specified; item_type:apparel_bundle; item_type:equipment_bundle; audience:beginner_runners; audience:experienced_runners; shoe_size:40-42; data_quality:sku_not_listed.
