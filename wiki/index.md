# LLM Wiki

## Active memory

- [Session handoff](session-handoff.md) — current context for the next chat.

## Project brief

- [Intent проекта](../intent.md) — сводное описание цели, границ, подтверждённых направлений и открытых решений.
- [Черновик спецификации v1](../spec.md) — объём квиза по готовым наборам, переносимая граница каталога, тестовая граница и решения, оставленные TBD.

## Knowledge

- [Проект № 5 — Генератор наборов товаров через квиз](projects/project-5-quiz-product-set-generator.md) — статус проекта, решения и открытые вопросы; черновик спецификации v1 уже подготовлен.
- [Исследование выбора спортивного питания и товаров спортсменами](projects/quiz-athlete-product-selection-research.md) — первичные исследования, украинский локальный сигнал, ограничения доказательств и рекомендации для динамических вопросов; теги — вспомогательный сигнал.
- [ТЗ на правила подбора квиза по 206 наборам](projects/quiz-matching-rules-technical-brief.md) — единая рабочая карта полного аудита и черновых динамических переходов; [реестр](projects/quiz-set-audit.json) содержит максимум найденных сигналов для 206/206 наборов. Текст архива доступен по 132 наборам, 74 остаются пробелом, 11 конфликтов сохранены для сверки; ни один набор пока не отсеян окончательно.
- [Аудит квиза на 150 покупательских сценариях](projects/quiz-buyer-scenario-audit-100.md) — расширенный проход на 150 сценариях с новыми механизмами (мультивыбор, Near-Miss, Dynamic Price Hint, Floor Price Anchor): 0 известных конфликтов, 0 нарушений цены/размера и 0 истинных тупиков (100% выдача).
- [Локальный тестовый квиз по 206 наборам](projects/quiz-test-sandbox.md) — локальная песочница и динамический двуязычный HTML-прототип покупательского квиза в стиле Windows 98 по адресу `/draft`; реализованы процент соответствия, мультивыбор, умные подсказки бюджета, Near-Miss и Floor Price Anchor.
- [Техническая документация Quiz Selection Engine](projects/quiz-engine-technical-documentation.md) — полная документация архитектуры, 4-слойной модели доказательств, формулы Match Confidence Score (0–99%), автономного JS-движка, 8-направленного ресайза виджета и скилла онбординга.
- [Каталог наборов Race Expert — снимок на 2026-11-06](projects/race-expert-set-catalog-2026-11-06.md) — 225 публичных наборов с названиями, артикулами и ценами на дату проверки.
- [206 наборов «За потребами»: состав, назначение и теги](projects/race-expert-need-sets-206-analysis.md) — полный разбор 206/206 наборов с источниками, составом, назначением, тегами и отмеченными расхождениями.
- [Актуальная анкета v3: наборы как исходный сценарий](projects/quiz-owner-discovery-questionnaire-v3.md) — анкета требований для владельца, опубликованная по IP; это не квиз для покупателей.
- [Предыдущая анкета v2: каталог и правила](projects/quiz-owner-discovery-questionnaire-v2.md) — прежний 13-вопросный список; после обратной связи выявлены избыточные вопросы о видимых данных каталога.
- [Предыдущий мастер-опросник](projects/quiz-owner-discovery-questionnaire.md) — прежний 21-вопросный вариант, заменённый опубликованной формой v3.
- [MySQL: read-only подключение и запрос контекста OpenCart](sources/mysql-readonly-access-and-product-query-guide.md) — проверенный маршрут через VPS-61125, ограничения TLS 1.3, схема пяти таблиц товара и SQL-шаблоны для проверки перед выдачей.
- `wiki/sources/` — source summaries.
- `wiki/concepts/` — durable concepts.
- `wiki/syntheses/` — integrated conclusions.

## Raw evidence

- [`raw/sources/2026-11-04-project-5-quiz.md`](../raw/sources/2026-11-04-project-5-quiz.md) — исходное описание проекта от пользователя.
- [`raw/sources/2026-11-04-quiz-owner-questionnaire-request.md`](../raw/sources/2026-11-04-quiz-owner-questionnaire-request.md) — требования к мастер-опроснику и уточнение числа квизов.
- [`raw/sources/2026-11-04-owner-questionnaire-feedback.md`](../raw/sources/2026-11-04-owner-questionnaire-feedback.md) — уточнение проблемы покупателя, бизнес-целей, рынка и валюты.
- [`raw/sources/2026-11-04-market-languages-scope.md`](../raw/sources/2026-11-04-market-languages-scope.md) — подтверждённые география, языки и валюта квиза.
- [`raw/sources/2026-11-04-backend-scope-no-advertising.md`](../raw/sources/2026-11-04-backend-scope-no-advertising.md) — backend-объём; реклама, платный трафик и рекламная аналитика исключены.
- [`raw/sources/2026-11-04-questionnaire-question-3-clarification.md`](../raw/sources/2026-11-04-questionnaire-question-3-clarification.md) — уточнение, что в вопросе 3 считается число обращений к консультантам.
- [`raw/sources/2026-11-04-quiz-recommendation-may-include-multiple-products.md`](../raw/sources/2026-11-04-quiz-recommendation-may-include-multiple-products.md) — квиз упрощает выбор и может предложить один или несколько товаров.
- [`raw/sources/2026-11-04-quiz-logic-question-audit.md`](../raw/sources/2026-11-04-quiz-logic-question-audit.md) — вопросы только о логике; рекомендовать можно товары, уже размещённые на сайте.
- [`raw/sources/2026-11-04-local-html-telegram-form-request.md`](../raw/sources/2026-11-04-local-html-telegram-form-request.md) — локальная HTML-форма, Telegram после завершения, серверные данные позже.
- [`raw/sources/2026-11-04-quiz-questionnaire-catalog-and-matching.md`](../raw/sources/2026-11-04-quiz-questionnaire-catalog-and-matching.md) — требование собирать источник каталога и конкретные правила соответствия ответов товарам.
- [`raw/sources/2026-11-04-questionnaire-buyer-inputs-not-full-quiz.md`](../raw/sources/2026-11-04-questionnaire-buyer-inputs-not-full-quiz.md) — уточнение, что владельцу не нужно писать весь клиентский квиз.

- [`raw/sources/2026-11-04-questionnaire-ukrainian-simple-list.md`](../raw/sources/2026-11-04-questionnaire-ukrainian-simple-list.md) — вимога до простої української мови, Markdown-формату та прикладів відповідей.
- [`raw/sources/2026-11-04-questionnaire-rule-basis-and-coverage.md`](../raw/sources/2026-11-04-questionnaire-rule-basis-and-coverage.md) — уточнення, що правила мають мати підставу, а приклади — охоплювати важливі випадки.
- [`raw/sources/2026-11-04-html-form-13-question-update.md`](../raw/sources/2026-11-04-html-form-13-question-update.md) — оновлення локальної HTML-форми за узгодженим списком із 13 питань.
- [`raw/sources/2026-11-04-quiz-deployed-by-ip.md`](../raw/sources/2026-11-04-quiz-deployed-by-ip.md) — публикация обновлённой формы по IP и удаление вводного абзаца.
- [`raw/sources/2026-11-04-telegram-connected-and-tested.md`](../raw/sources/2026-11-04-telegram-connected-and-tested.md) — подключение Telegram и успешная тестовая доставка.
- [`raw/sources/2026-11-04-questionnaire-feedback-result-type-gating.md`](../raw/sources/2026-11-04-questionnaire-feedback-result-type-gating.md) — требование убрать очевидные вопросы и строить условные ветки по типу результата квиза.
- [`raw/sources/2026-11-04-race-expert-public-catalog-review.md`](../raw/sources/2026-11-04-race-expert-public-catalog-review.md) — наблюдения по публичным категориям, наборам и полям карточек сайта.
- [`raw/sources/2026-11-04-questionnaire-addressed-to-single-client.md`](../raw/sources/2026-11-04-questionnaire-addressed-to-single-client.md) — требование адресовать анкету одному замовнику, а не команде сайта.
- [`raw/sources/2026-11-04-budget-is-buyer-input.md`](../raw/sources/2026-11-04-budget-is-buyer-input.md) — уточнение: бюджет выбирает покупатель и квиз использует его для подбора.
- [`raw/sources/2026-11-05-quiz-owner-questionnaire-answers.md`](../raw/sources/2026-11-05-quiz-owner-questionnaire-answers.md) — ответы владельца: один общий квиз, готовые и новые AI-наборы, параметры подбора, бюджетные диапазоны и неразрешённые правила.
- [`raw/sources/2026-11-06-scope-206-needs-sets.md`](../raw/sources/2026-11-06-scope-206-needs-sets.md) — решение разобрать в следующем чате состав и назначение всех 206 наборов «За потребами».
- [`raw/sources/2026-11-06-approved-tags-for-206-sets.md`](../raw/sources/2026-11-06-approved-tags-for-206-sets.md) — пользователь утвердил формат состава/назначения и теги по спорту, дистанции, цене, весу покупателя и источникам.
- [`raw/sources/2026-11-06-206-set-follow-up-verifications.md`](../raw/sources/2026-11-06-206-set-follow-up-verifications.md) — перепроверка количеств товара и кофеина для спорных карточек 206 наборов.
- [`raw/sources/2026-11-09-quiz-matching-rules-spec-request.md`](../raw/sources/2026-11-09-quiz-matching-rules-spec-request.md) — поручение подготовить ТЗ по параметрам подбора, с фиксацией того, что конкретные правила ещё не утверждены.
- [`raw/sources/2026-11-09-v1-ready-sets-only-scope-and-portable-catalog.md`](../raw/sources/2026-11-09-v1-ready-sets-only-scope-and-portable-catalog.md) — уточнение: v1 работает только с готовыми наборами, а источник каталога должен быть заменяемым.
- [`raw/sources/2026-11-09-athlete-product-selection-research-request.md`](../raw/sources/2026-11-09-athlete-product-selection-research-request.md) — поручение исследовать, как спортсмены выбирают спортивные товары и наборы; теги — вторичный сигнал, квиз — динамический, набор выбирает backend.
- [`raw/sources/2026-11-09-quiz-buyer-scenario-audit-request.md`](../raw/sources/2026-11-09-quiz-buyer-scenario-audit-request.md) — запрос на 100 логических сценариев квиза со спортивной перспективы.
- [`raw/sources/2026-11-09-quiz-audit-synthesis-implementation-plan-request.md`](../raw/sources/2026-11-09-quiz-audit-synthesis-implementation-plan-request.md) — запрос свести результаты 100 сценариев и составить план исправления; пользователь будет тестировать `/draft` в следующем чате.

## Session recall

- `wiki/session-index.jsonl` — derived local index for date, tag, file and status queries.
- `wiki/tag-taxonomy.yml` — controlled tag vocabulary.
