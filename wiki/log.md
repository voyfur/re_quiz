# Wiki Log

## [2026-11-09] project-audit | Complete the 206-set source snapshot audit

- Завершён проход по 206/206 наборам каталожного снимка 2026-11-06; в JSON учтено 728 компонентных строк, количество товара в наборе отделено от содержимого упаковки.
- 548 количеств оставлены неизвестными или неоднозначными; отдельные product-source ссылки есть у 7 компонентов, остальные свойства не подтверждены независимо и не используются как факты matching.
- 11 наборов удержаны из-за неразрешённых конфликтов состава/версии источника; 195 допусков — предложения владельцу на утверждение. Текущие цены и наличие не обновлялись для всех карточек.
- Динамические темы вопросов отложены по указанию пользователя. Код прототипа не менялся; обновлены аудит, ТЗ, handoff и Wiki index.
- Источниковые наблюдения по спорным карточкам сохранены в JSON-реестре с датой и ограничениями кэшированного доступа.

## [2026-11-09] research | Athlete product selection and adaptive quiz

- Подготовлено исследование о том, как спортсмены выбирают спортивное питание/добавки: первичные опросы, валидированный факторный опросник, рекомендации IOC/AIS и отдельная оценка ограничений.
- Найдено небольшое украинское исследование из двух фитнес-клубов Полтавы (90 потребителей спортпита и 10 экспертов); оно не репрезентативно для рынка. В просмотренных источниках не найдено прямых исследований выбора готовых многотоварных наборов.
- Зафиксировано уточнение пользователя: теги вспомогательны; backend подбирает набор автоматически; следующие вопросы/варианты динамически ограничиваются совместимыми кандидатами; форма необязательна, размер условен для одежды/обуви.
- Обновлены исследовательская карточка, ТЗ matching, карточка проекта, `wiki/index.md`, `wiki/source-manifest.md` и handoff. Код квиза не менялся.
- Raw-запрос: `raw/sources/2026-11-09-athlete-product-selection-research-request.md`; session: `raw/sessions/2026-11-09-athlete-product-selection-research.md`.
- Следующий этап: спроектировать динамическую карту вопросов и соответствие ответов кандидатам; текущие прототипные эвристики не являются финальными.

## [2026-11-09] session-log | Complete and verify the 206-set quiz sandbox

- Доведён до рабочего состояния локальный двуязычный квиз и backend-подбор по каталогу из 206 наборов. Реализация находится отдельно в `test-quiz-sandbox/`; production-сайт и анкета владельца не затронуты.
- Повторная проверка: 26 unit/handler-тестов прошли; JS проверен `node --check`. В локальном браузере проверены варианты 1/2/3, строгий отказ по кофеину при недостатке данных, граница бюджета 1 499/1 500 грн, размеры 42/43, украинский язык и мобильная ширина 390×844 без горизонтальной прокрутки.
- Обновлены `spec.md`, test plan, implementation plan, ticket TEST-04, карточка sandbox, карточка проекта и `session-handoff.md`. Старые записи ниже сохранены как история состояния на момент первоначальной реализации.
- Зафиксировано продолжение: интеграция сайта — следующий отдельный этап; актуальный каталог и production-правила требуют отдельного подключения/согласования.

## [2026-11-09] session-log | Build isolated quiz sandbox for 206 sets

- По прямому поручению пользователя создан локальный двуязычный квиз с backend-подбором по 206 наборам «За потребами». Код размещён отдельно в `test-quiz-sandbox/`; анкета владельца и исходные 206 карточек не менялись.
- Добавлены производный локальный `catalog.json`, валидатор запросов и matcher, loopback-only API, UI на русском/украинском, test plan и 4 локальных test-only tickets. Эвристики явно не утверждены для production; сайт, корзина, актуальный каталог и Telegram не подключены.
- На входе доступны назначение, спорт, тип набора, форма, текстовый тег формата старта, бюджет по полной цене снимка, размер, компонент, подтверждённое отсутствие кофеина и явно отмеченное наличие. Квиз возвращает 1–3 альтернативы; неизвестные ограничения не заполняет догадками.
- Обновлены `spec.md`, `intent.md`, карточка проекта, ТЗ, session handoff, индекс Wiki и source manifest; создана карточка `quiz-test-sandbox.md` и исходная запись запроса.
- Проверки: 21 unit/handler-тест пройден; JS `node --check` и HTML parser прошли. Визуальный браузерный запуск не выполнен: текущая execution-среда блокирует loopback TCP binding; ручную проверку нужно сделать локально.
- Следующий этап по плану пользователя — проверить локальную песочницу, затем отдельно интегрировать сайт после согласования production-правил и источника актуального каталога.

## [2026-11-09] session-log | Clarify proposal and approval roles

- Уточнено в `spec.md`, `intent.md`, handoff и проектных страницах: ассистент готовит предложения по квизу и matching-правилам; владелец проверяет, корректирует и утверждает их до реализации.
- Исходные записи и содержание каталога не менялись.

## [2026-11-09] session-log | Add v1 quiz specification

- Подготовлен корневой `spec.md` с объёмом v1, переносимой границей источника каталога, контрактом результата, тестовой границей и открытыми решениями.
- Обновлены `intent.md`, `wiki/index.md`, `wiki/session-handoff.md`, карточка проекта и ТЗ по подбору; пользователь подтвердил тестирование внешнего backend-контракта и пожелание позже переключить источник каталога на API к базе данных.
- Контентный индекс перестроен; `lint_content.py` прошёл успешно (7 карточек). Новых raw-источников нет, поэтому `source-manifest.md` и содержимое `raw/` не менялись.
- Правила matching и допущенный список наборов остаются на согласование с владельцем.

## [2026-11-09] session-log | Prepare quiz matching-rules technical brief

- На основании завершённого анализа 206 наборов и ответов владельца создано рабочее ТЗ: параметры квиза, покрытие данных, правила для подтверждённых/отсутствующих/неизвестных значений и матрица для согласования.
- Зафиксированы пробелы текущей разметки: вес покупателя неизвестен во всех 206 наборах, числовой дистанции нет, кофеин указан у 4 наборов (точные 400 мг только у №206), наличие размечено для 24 наборов; цены основаны на снимке 2026-11-06 с 49 отмеченными расхождениями.
- Изменены `wiki/projects/quiz-matching-rules-technical-brief.md`, карточка проекта, `wiki/index.md`, `wiki/session-handoff.md`, `wiki/source-manifest.md`. Запрос сохранён в `raw/sources/2026-11-09-quiz-matching-rules-spec-request.md`.
- Контентный индекс перестроен; `lint_content.py` прошёл успешно (7 карточек в индексе).
- Фильтры, диапазоны, безопасность, ранжирование и поведение без совпадений оставлены на согласование; этот этап их не утверждает.
- Следующее: в следующем чате пройти матрицу параметров и согласовать примеры правил, затем определить подходящие наборы.

## [2026-11-06] refine | Verify incomplete product descriptions

- По официальным карточкам уточнены количество, материал, назначение и спортивная применимость пяти наборов носков (строки 82–86); состав больше не отмечен как неполностью извлечённый.
- Для RE11742 добавлено зафиксированное расхождение цены карточки (1 500 грн) и каталожного снимка (1 295 грн); общее число помеченных расхождений — 49. Для набора «Дитяча турбота» добавлено назначение по формулировке продавца.
- Источники — официальные карточки Race Expert, ссылки сохранены в соответствующих записях анализа.

## [2026-11-06] complete | Analysis of 206 need-based sets

- Завершены все 206 source-linked записей по утверждённому формату: состав, назначение, спорт, дистанция/формат, цена из снимка каталога, вес покупателя и подтверждённые дополнительные метрики.
- Проверено покрытие снимка каталога: строки 1–107, 111–116 и 118–210 включены без пропусков и дублей; 19 наборов «По дистанціях» исключены. Теги цены совпадают со снимком; 48 расхождений с подробными карточками отмечены `data_quality:live_price_differs`. Для всех наборов стоит `buyer_weight:not_specified`.
- Обновлены карточка анализа, карточка проекта, index и handoff. Контентный индекс перестроен и проверен lint-скриптом.
- Следующий этап: черновая матрица «потребность/ответ покупателя → наборы-кандидаты» и согласование списка и правил с владельцем.

## [2026-11-06] design | Tag schema for 206 need-based sets

- Пользователь утвердил отдельный анализ всех 206 наборов «За потребами» с составом, назначением, спортом, дистанцией/форматом, ценой в UAH, весом покупателя только по подтверждённым данным и дополнительными метриками.
- Создан рабочий Wiki-файл со словарём тегов и тремя примерами; полный разбор продолжается.
- Зафиксированы правила источников, неизвестных значений, различия между весом покупателя и массой товара, а также между форматом марафона и числовой дистанцией.
- Обновлены карточка проекта, index, handoff, source manifest и content index.
- Источник решения: `raw/sources/2026-11-06-approved-tags-for-206-sets.md`.

## [2026-11-06] decision | Analyze all 206 need-based sets

- Пользователь зафиксировал следующий этап: разобрать состав и назначение всех 206 наборов раздела «За потребами».
- Девятнадцать наборов раздела «По дистанціях» не входят в этот этап. Включение всех 206 в анализ не утверждает правила их рекомендации квизом.
- Обновлены карточка проекта, индекс, handoff и source manifest; исходное решение сохранено в raw source.
- Источник: `raw/sources/2026-11-06-scope-206-needs-sets.md`.

## [2026-11-06] catalog | Snapshot all Race Expert sets

- Проверены 225 карточек из разделов «За потребами» и «По дистанціях»: у всех указана цена, у одной не указан артикул.
- В Wiki сохранены название, артикул и цена каждого набора; цены обозначены как снимок на дату проверки.
- Обновлены индекс Wiki, карточка проекта и handoff.
- Источник: [публичный каталог Race Expert](https://raceexpert.com.ua/nabori/).

## [2026-11-06] ingest | Owner answers to quiz logic questionnaire

- Сохранены ответы владельца анкеты от 2026-11-05 в неизменяемом raw source; непонятые ответы оставлены открытыми, без домысливания.
- Зафиксированы: один общий квиз; готовые наборы по потребностям и новые наборы из 2–5 товаров с подбором AI; параметры потребности, производителя, формы и срока; кнопка добавления состава набора в корзину.
- Отмечены вопросы к уточнению: первые потребности, примеры правильных/нулевых результатов, пересечение бюджета на 1500 грн, безопасность и инструкции приёма, база данных (MySQL не подтверждён), обновления каталога и отсутствие товаров.
- Обновлены карточка проекта, индекс и source manifest. HTML-форма и сервер не менялись.
- Источник: `raw/sources/2026-11-05-quiz-owner-questionnaire-answers.md`.

## [2026-11-05] deploy | Publish owner questionnaire v3

- HTML-форма обновлена с прежних 13 обязательных вопросов до 9 основных вопросов и условных веток, обращена к одному замовнику.
- Серверная проверка адаптирована под активные вопросы. Публичная страница по IP вернула HTTP 200; тестовая отправка 17 ответов прошла через Telegram.
- Предыдущие файлы сохранены в `/opt/race-expert-quiz/backups/quiz-v3-20261105T091007Z`; секретный env-файл не менялся.
- Обновлены карточка проекта, индекс и handoff.

## [2026-11-04] refine | Budget is selected by the quiz buyer

- Уточнено, что бюджет выбирает покупатель внутри квиза, и ответ влияет на подбор набора; точные диапазоны и правило применения полной цены набора остаются на согласование.
- Обновлены известный контекст и вопрос 5 в анкете v3, индекс и handoff. Опубликованная HTML-форма не менялась.
- Источник: `raw/sources/2026-11-04-budget-is-buyer-input.md`.

## [2026-11-04] refine | Clarify buyer-input question is not full quiz copy

- Уточнён пункт 2 локального черновика: владелец перечисляет только входные параметры покупателя и значения, которые влияют на подбор; финальные тексты клиентского квиза не требуются.
- Сохранён источник: `raw/sources/2026-11-04-questionnaire-buyer-inputs-not-full-quiz.md`.

## [2026-11-04] ingest | Questionnaire adds catalog source and recommendation mapping

- По уточнению пользователя создан локальный черновик анкеты требований: он отдельно собирает источник данных каталога, доступные поля, конкретные соответствия ответов ID товаров/наборов и ответственных за утверждение.
- Зафиксировано, что наличие базы каталога заявлено пользователем, но её платформа, API, схема и доступ пока не проверены; PostgreSQL стека автоматизации не считается базой сайта без подтверждения.
- Старый 21-вопросный документ и HTML-форма оставлены как прежний вариант; форма не обновлялась и ничего не загружалось на сервер.
- Источник: `raw/sources/2026-11-04-quiz-questionnaire-catalog-and-matching.md`.

## [2026-11-04] implement | Local questionnaire form with Telegram delivery

- Созданы `index.html` и `server.py`: форма по актуальному мастер-опроснику разделена на четыре шага с обязательным ядром и условными модулями.
- После полной проверки ответов сервер отправляет все заполненные ответы и статусы модулей одним текстовым файлом через Telegram Bot API.
- `.env` не перезаписывался; секреты остаются на серверной стороне и исключены через `.gitignore`. Тестовое сообщение в Telegram не отправлялось.
- Локальный сервер запущен на `http://127.0.0.1:8000`; публичное размещение ожидает серверные данные пользователя.
- Источник: `raw/sources/2026-11-04-local-html-telegram-form-request.md`.

## [2026-11-04] audit | Questionnaire limited to recommendation logic

- Перепроверен весь мастер-опросник: вместо 133 прежних вопросов оставлен 21 вопрос, относящийся к правилам подбора товаров сайта.
- Зафиксировано, что товары вне каталога сайта рекомендовать нельзя; подтверждённые рынок, языки, валюта, бизнес-цели и границы рекламы повторно не спрашиваются.
- Удалены вопросы о рекламе, метриках бизнеса, API и интерфейсе, юридическом хранении данных, сроках, запуске и операционном сопровождении.
- Остались обязательные вопросы о сценарии, ответах, полях товаров, правилах включения/ранжирования, бюджете, наличии и поведении без подходящего результата; добавлены только применимые модули ветвления, наборов/вариантов и товарных ограничений.
- Источник: `raw/sources/2026-11-04-quiz-logic-question-audit.md`.

## [2026-11-04] clarify | Quiz recommends what the buyer needs

- Уточнена основная цель: помочь покупателю выбрать нужные ему товары, включая случай, когда он сам не знает, что выбрать.
- Зафиксировано, что рекомендация может включать один товар или несколько; точный формат (отдельные позиции, подборка или готовый набор) остаётся открытым решением.
- Обновлены карточка проекта, мастер-опросник, handoff, индекс и source manifest.
- Источник: `raw/sources/2026-11-04-quiz-recommendation-may-include-multiple-products.md`.

## [2026-11-04] refine | Question 3 specifies the measured quantity

- Переписан вопрос 3: теперь он спрашивает о числе обращений к консультантам по выбору товара/набора за выбранный период и источнике этой цифры.
- Источник: `raw/sources/2026-11-04-questionnaire-question-3-clarification.md`.

## [2026-11-04] update | Quiz backend scope clarified

- Зафиксировано, что текущая работа — backend квиза; реклама, привлечение трафика и рекламная аналитика не входят в объём.
- Удалены рекламные вопросы; формулировки о входных данных, результате и интеграции уточнены под backend-контракт с сайтом.
- Обновлены карточка проекта, мастер-опросник, индекс и source manifest; опросник содержит 133 вопроса: 18 обязательных и 115 в 12 условных модулях.
- Источник: `raw/sources/2026-11-04-backend-scope-no-advertising.md`.

## [2026-11-04] ingest | Quiz market and languages

- Зафиксировано: рынок только Украина, языки — русский и украинский, валюта — гривна.
- Удалён 4-й обязательный вопрос как повторяющий уже заданные параметры; нумерация и ссылки на номера обновлены.

## [2026-11-04] ingest | Owner questionnaire feedback and known context

- Зафиксированы известные ответы: покупателю трудно выбрать; квиз подбирает набор под спортивную цель и релевантные личные параметры; бизнес-цели — повысить конверсию и сократить консультации; рынок — Украина, валюта — гривна.
- Обновлены карточка проекта и мастер-опросник: известные сведения вынесены отдельно, вопросы о неизвестных решениях переформулированы конкретнее и проще.
- Следующее: определить цели первого запуска, нужные параметры покупателя и измеримые цели конверсии/нагрузки.

## [2026-11-04] ingest | Quiz owner discovery questionnaire

- Сохранён запрос на мастер-опросник и уточнение: 60–70 — существующие наборы, число квизов неизвестно; один общий квиз с ветвлением возможен, но не решён.
- Создан полный банк вопросов с обязательным ядром и 13 условными модулями: `wiki/projects/quiz-owner-discovery-questionnaire.md`.
- Обновлена карточка проекта и индекс; вопросы о безопасности и правилах оставлены на утверждение назначенным экспертам.
- Следующее: провести интервью, заполнить ответы/источники/владельцев, затем согласовать MVP и повторно оценить объём.

## [2026-11-04] ingest | Project 5 quiz product-set generator

- Сохранены исходные заметки в `raw/sources/2026-11-04-project-5-quiz.md`.
- Создана проектная карточка с анализом готовности, границ, зависимостей и открытых решений: `wiki/projects/project-5-quiz-product-set-generator.md`.
- Примеры добавок и бюджетов отмечены как неподтверждённые; правила рекомендаций не выводились из примеров.
- Следующее: согласовать сценарий, модель набора, правила/отказы, данные каталога и точку интеграции.

## [2026-11-04] session | Сканирование и подготовка сервера для опросника квиза

- Raw: `raw/sessions/2026-11-04-session.md`
- Tags: `activity:configuration`, `status:needs-review`, `task:quiz-server-staging`, `component:telegram`, `file:/opt/race-expert-quiz/index.html`, `file:/opt/race-expert-quiz/server.py`
- Status: `needs-review`

## [2026-11-04] session | Тест доставки ответов опросника в Telegram и проверка хранилища ключей

- Raw: `raw/sessions/2026-11-04-telegram.md`
- Tags: `activity:testing`, `status:needs-review`, `task:telegram-delivery-check`, `component:telegram`, `project:quiz-product-set-generator`
- Status: `needs-review`

## [2026-11-04] session | Quiz questionnaire requirements: catalog source and rule mapping

- Raw: `raw/sessions/2026-11-04-quiz-questionnaire-requirements-catalog-source-a.md`
- Tags: `activity:documentation`, `status:completed`, `task:quiz-requirements-questionnaire`, `component:product-catalog`, `project:quiz-product-set-generator`, `file:wiki/projects/quiz-owner-discovery-questionnaire-v2.md`
- Status: `completed`

## [2026-11-04] refine | Simple Ukrainian question list

- Переписано локальний список простими українськими словами у форматі Markdown: заголовок «Питання», нумерований список і приклад відповіді для кожного пункту.
- Пункт про дані покупця уточнює, що не потрібно писати весь клієнтський квіз.
- Джерело: `raw/sources/2026-11-04-questionnaire-ukrainian-simple-list.md`.

## [2026-11-04] session | Quiz questionnaire wording: Ukrainian plain language

- Raw: `raw/sessions/2026-11-04-quiz-questionnaire-wording-ukrainian-plain-langu.md`
- Tags: `activity:documentation`, `status:completed`, `task:plain-ukrainian-question-list`, `component:product-catalog`, `project:quiz-product-set-generator`, `file:wiki/projects/quiz-owner-discovery-questionnaire-v2.md`
- Status: `completed`

## [2026-11-04] refine | Ask for rule basis and complete examples

- У питанні 3 тепер потрібно вказати підставу відповідності відповіді товару; у питанні 12 — приклади для кожного важливого правила, а не лише фіксовані 5–10 рядків.
- Джерело: `raw/sources/2026-11-04-questionnaire-rule-basis-and-coverage.md`.

## [2026-11-04] session | Update questionnaire form to 13 Ukrainian questions

- Raw: `raw/sessions/2026-11-04-update-questionnaire-form-to-13-ukrainian-questi.md`
- Tags: `activity:implementation`, `status:completed`, `task:ukrainian-questionnaire-form`, `component:telegram`, `project:quiz-product-set-generator`, `file:index.html`, `file:server.py`
- Status: `completed`

## [2026-11-04] session | Deploy quiz questionnaire by IP

- Raw: `raw/sessions/2026-11-04-deploy-quiz-questionnaire-by-ip.md`
- Tags: `activity:configuration`, `status:partial`, `task:ip-deployment`, `project:quiz-product-set-generator`, `component:form`, `component:telegram`, `file:index.html`, `file:server.py`, `file:wiki/session-handoff.md`
- Status: `partial`

## [2026-11-04] session | Connect Telegram and test questionnaire delivery

- Raw: `raw/sessions/2026-11-04-connect-telegram-and-test-questionnaire-delivery.md`
- Tags: `activity:testing`, `status:completed`, `task:telegram-integration-test`, `project:quiz-product-set-generator`, `component:telegram`, `component:form`, `file:/etc/race-expert-quiz/telegram.env`, `file:wiki/session-handoff.md`
- Status: `completed`

## [2026-11-04] session | Revise questionnaire around result type and site catalog

- Raw: `raw/sessions/2026-11-04-revise-questionnaire-around-result-type-and-site.md`
- Tags: `activity:documentation`, `status:needs-review`, `task:questionnaire-v3`, `project:quiz-product-set-generator`, `component:questionnaire`, `component:product-catalog`, `file:wiki/projects/quiz-owner-discovery-questionnaire-v3.md`, `file:wiki/session-handoff.md`
- Status: `needs-review`

## [2026-11-04] session | Reconcile questionnaire with set-first project summary

- Raw: `raw/sessions/2026-11-04-reconcile-questionnaire-with-set-first-project-s.md`
- Tags: `activity:documentation`, `status:needs-review`, `task:set-first-questionnaire`, `project:quiz-product-set-generator`, `component:questionnaire`, `source:project-brief`, `file:wiki/projects/quiz-owner-discovery-questionnaire-v3.md`, `file:wiki/session-handoff.md`
- Status: `needs-review`

## [2026-11-04] session | Address questionnaire to one client

- Raw: `raw/sessions/2026-11-04-address-questionnaire-to-one-client.md`
- Tags: `activity:documentation`, `status:needs-review`, `task:single-client-questionnaire`, `project:quiz-product-set-generator`, `component:questionnaire`, `file:wiki/projects/quiz-owner-discovery-questionnaire-v3.md`, `file:wiki/session-handoff.md`
- Status: `needs-review`

## [2026-11-06] session | Record owner answers to quiz logic questionnaire

- Raw: `raw/sessions/2026-11-06-record-owner-answers-to-quiz-logic-questionnaire.md`
- Tags: `activity:documentation`, `status:completed`, `task:owner-questionnaire-answers`, `project:quiz-product-set-generator`, `component:questionnaire`, `file:raw/sources/2026-11-05-quiz-owner-questionnaire-answers.md`, `file:wiki/projects/project-5-quiz-product-set-generator.md`, `file:wiki/index.md`, `file:wiki/source-manifest.md`, `file:wiki/log.md`
- Status: `completed`

## [2026-11-06] session | Complete quiz project status and next-chat handoff

- Raw: `raw/sessions/2026-11-06-complete-quiz-project-status-and-next-chat-hando.md`
- Tags: `activity:documentation`, `status:completed`, `task:project-status-handoff`, `project:quiz-product-set-generator`, `component:questionnaire`, `component:telegram`, `file:wiki/projects/project-5-quiz-product-set-generator.md`, `file:wiki/index.md`, `file:wiki/session-handoff.md`
- Status: `completed`

## [2026-11-06] documentation | Follow up source audit for the 206 need-based sets

- Raw: `raw/sources/2026-11-06-206-set-follow-up-verifications.md`
- Tags: `activity:documentation`, `status:completed`, `task:206-composition-audit`, `project:quiz-product-set-generator`, `component:product-catalog`, `file:wiki/projects/race-expert-need-sets-206-analysis.md`, `file:wiki/index.md`, `file:wiki/session-handoff.md`, `file:wiki/source-manifest.md`, `file:wiki/log.md`
- Status: `completed`
- Outcome: уточнены составы наборов 111, 169, 171, 172, 175 и 206; оставшиеся расхождения и отсутствующие множители явно сохранены как неопределённости.

## [2026-11-09] documentation | Clarify v1 ready-set scope and portable catalog

- Raw: `raw/sources/2026-11-09-v1-ready-sets-only-scope-and-portable-catalog.md`
- Tags: `activity:documentation`, `status:completed`, `task:quiz-v1-scope`, `project:quiz-product-set-generator`, `component:matching-rules`, `component:product-catalog`, `file:intent.md`, `file:wiki/projects/quiz-matching-rules-technical-brief.md`, `file:wiki/projects/project-5-quiz-product-set-generator.md`, `file:wiki/session-handoff.md`
- Status: `completed`
- Outcome: первая версия ограничена подбором одного или нескольких готовых наборов из 206 записей «За потребами»; отдельные товары и AI-наборы вынесены в будущие сценарии. Зафиксирована рекомендация начать с локального структурированного индекса и заменить источник через адаптер при интеграции с сайтом.

## [2026-11-09] session | Athlete product selection research

- Raw: `raw/sessions/2026-11-09-athlete-product-selection-research.md`
- Tags: `activity:research`, `status:completed`, `task:athlete-product-selection-research`, `project:quiz-product-set-generator`, `component:matching-rules`, `component:questionnaire`, `file:wiki/projects/quiz-athlete-product-selection-research.md`, `file:wiki/projects/quiz-matching-rules-technical-brief.md`, `file:wiki/session-handoff.md`
- Status: `completed`

## [2026-11-09] documentation | Complete maximum-evidence audit for 206 sets

- Raw: `raw/sources/2026-11-09-quiz-set-audit-scope.md`; user clarified that confirmed and unconfirmed signals all stay in the pool until later pruning.
- Tags: `activity:documentation`, `status:completed`, `task:quiz-matching-logic-audit`, `project:quiz-product-set-generator`, `component:matching-rules`, `component:product-catalog`, `file:wiki/projects/quiz-matching-rules-technical-brief.md`, `file:wiki/projects/quiz-set-audit.json`, `file:wiki/session-handoff.md`, `file:wiki/index.md`
- Status: `completed`
- Outcome: 206/206 row-level audits and 728 component rows now carry evidence layers, source coverage, seller claims, activity/season/race/size/form/membership signals, uncertainties, conflicts, and draft candidate/topic maps. Search-index page text was found for 132 records (184 versions); 74 are archive misses. Eleven source/composition conflicts remain flagged but all records remain in the pool. Seller effects are not independently verified; current price/stock require runtime refresh. No quiz code changed; exact buyer wording and final pruning remain future decisions.

## [2026-11-09] session | Capture 206-set evidence audit and hand off conflict review

- Raw: `raw/sessions/2026-11-09-capture-206-set-evidence-audit-and-hand-off-conf.md`
- Tags: `activity:documentation`, `status:completed`, `task:206-set-evidence-audit-handoff`, `project:quiz-product-set-generator`, `component:matching-rules`, `component:product-catalog`, `source:2026-11-09-quiz-set-audit-scope`, `file:wiki/projects/quiz-set-audit.json`, `file:wiki/projects/quiz-matching-rules-technical-brief.md`, `file:wiki/index.md`, `file:wiki/session-handoff.md`, `file:wiki/log.md`
- Status: `completed`

## [2026-11-09] session-log | Build first buyer-facing quiz draft

- Used the existing 206-set signal/conflict audit to add an isolated Windows 98-style HTML preview at `/draft`; the older test form at `/` remains separate.
- Draft matcher uses seller positioning first, undisputed listed components second, activity as a soft rank, and tag-only/supplemental text as non-candidate signals. It shows conditional activity, shoe-size, and snapshot-budget inputs; results remain test-only.
- Updated the sandbox, matching brief, project page, index, and session handoff. Raw evidence was not edited.
- Verification: Python and JavaScript syntax checks passed; goal-level audit lookup found candidates and up to three results for all nine displayed goals. Browser flow rendered three running results and flagged a conflicted record; an overbroad endurance-to-running mapping was narrowed. Owner feedback remains next; no production rules approved.

## [2026-11-09] session-log | Fix quiz preview launch confusion

- Root cause: the user opened `draft.html` as `file://`, while the preview's absolute asset paths and matching API require the local server.
- Switched assets to relative paths, added a direct-file launch explanation, and documented that the supported preview URL is `http://127.0.0.1:8765/draft`.
- Reopened the server URL in the browser and confirmed that a goal radio option can be selected. Python and JavaScript syntax checks passed; the content index was rebuilt and lint passed.

## [2026-11-09] session-log | Repair dynamic buyer quiz flow

- Owner feedback identified a shallow flow and identical activity options across goals. Made `/draft` one question per screen, with goal-specific activities (food → running/cycling; training → strength/functional/yoga-pilates) and conditional class, scenario, timing, place, event, weather, form, size, and price questions.
- Split the audited use-context signal into time and place questions; hide event-preparation scenarios for strength training. Soft answers rank candidates; hard size and demo snapshot-price limits remain separate. Unknown data remains unknown.
- Fixed the stale-server/API mismatch that left the first selected goal on screen, removed raw budget placeholders, and fixed “Изменить ответы” so it reopens the first question.
- Updated `quiz-test-sandbox.md`, the matching-rules brief, `wiki/index.md`, and session handoff. Raw evidence and the production site were not changed.
- Verification: Python parse and `node --check`; browser pass through an eight-screen strength-training route to three results, then back to the first question. Food activity options and the strength activity branch were visibly checked. Owner review of wording and recommendations remains open; rules are still experimental.

## [2026-11-09] session-log | Audit buyer quiz with 100 scenarios

- Added a reproducible 100-scenario audit spanning running, food, hydration, training, recovery, outdoors, gear, daily use, gifts, budget/size edges and unsupported constraints. Each case followed the dynamic `draft_options` question order and was sent through `draft_recommend`.
- Findings: zero hard price/known-size violations; known preference conflicts in 71/100 scenarios and in the first result in 43/100; 16/100 had an empty answer-compatible pool but still returned recommendations from the original goal pool. Backend rejected unsupported caffeine, allergen and exact-5-km filters in 3/3 checks.
- Recorded the matrix, top results, known conflicts, unknown signals and buyer-question draft in `wiki/projects/quiz-buyer-scenario-audit-100.md`. The latest task is owner decision on soft versus hard filters and no-result behavior, followed by matcher repair and a repeat run.
- This was a logic simulation through the matching functions, not a fresh browser interaction test. The catalog is a 2026-11-06 snapshot; live stock and current price were not checked.

## [2026-11-09] session | Synthesize the 100-scenario quiz audit and record an implementation plan

- Raw: `raw/sessions/2026-11-09-synthesize-the-100-scenario-quiz-audit-and-recor.md`
- Tags: `activity:documentation`, `status:completed`, `task:quiz-100-scenario-synthesis-plan`, `project:quiz-product-set-generator`, `component:matching-rules`, `component:product-catalog`, `topic:quiz-audit`, `file:wiki/projects/quiz-buyer-scenario-audit-100.md`, `file:test-quiz-sandbox/scenario_audit_100.py`, `file:wiki/session-handoff.md`
- Status: `completed`

## [2026-11-09] session-log | Rework /draft matching after the 100-scenario audit

- Shared candidate classification across dynamic question planning and final recommendations. Normal results now exclude known conflicts; unknown signals and secondary-preference conflicts require separate explicit actions.
- Kept price and known-size mismatches hard, added conditional gift sizing, hiking to the food activity branch, and an explicit other-activity option. Result cards disclose confirmed or uncertain club-membership status.
- Updated the sandbox card, audit baseline note and session handoff. The 71/100 audit metrics describe the previous matcher.
- Verification: Python syntax and `node --check` passed. The 100-scenario audit and browser pass remain outstanding.

## [2026-11-09] session | Verify revised quiz matching logic

- Raw: `raw/sessions/2026-11-09-verify-revised-quiz-matching-logic.md`
- Tags: `activity:testing`, `status:completed`, `task:quiz-matching-regression`, `project:quiz-product-set-generator`, `component:matching-rules`, `component:product-catalog`, `topic:quiz-audit`, `topic:prototype-ui`, `file:test-quiz-sandbox/scenario_audit_100.py`, `file:wiki/projects/quiz-buyer-scenario-audit-100.md`, `file:wiki/projects/quiz-test-sandbox.md`, `file:wiki/index.md`, `file:wiki/content-index.jsonl`, `file:wiki/session-handoff.md`, `file:wiki/log.md`, `file:wiki/session-index.jsonl`, `file:raw/sessions/2026-11-09-verify-revised-quiz-matching-logic.md`
- Status: `completed`

## [2026-11-10] session | Implement Near-Miss, Floor Price Anchor and Dynamic Price Hint with 150 buyer scenarios audit

- Raw: `raw/sessions/2026-11-10-implement-near-miss-floor-price-anchor-and-dynam.md`
- Tags: `activity:implementation`, `status:completed`, `task:quiz-matching-enhancement`, `project:quiz-product-set-generator`, `component:matching-rules`, `component:product-catalog`, `topic:quiz-audit`, `topic:prototype-ui`, `file:test-quiz-sandbox/draft_matcher.py`, `file:test-quiz-sandbox/web/draft.js`, `file:test-quiz-sandbox/web/draft.css`, `file:test-quiz-sandbox/tests/test_draft_advanced.py`, `file:test-quiz-sandbox/scenario_audit_100.py`, `file:wiki/projects/quiz-buyer-scenario-audit-100.md`, `file:wiki/projects/quiz-test-sandbox.md`, `file:wiki/index.md`
- Status: `completed`

## [2026-11-10] session | Fix draft HTML syntax error, bundle standalone client matcher and enable offline interactive quiz walkthrough

- Raw: `raw/sessions/2026-11-10-fix-draft-html-syntax-error-bundle-standalone-cl.md`
- Tags: `activity:implementation`, `status:completed`, `task:offline-quiz-interactive-walkthrough`, `project:quiz-product-set-generator`, `component:matching-rules`, `component:product-catalog`, `topic:prototype-ui`, `topic:quiz`, `file:test-quiz-sandbox/web/draft.js`, `file:test-quiz-sandbox/web/draft.html`, `file:test-quiz-sandbox/web/catalog_data.js`, `file:test-quiz-sandbox/web/client_matcher.js`, `file:wiki/projects/quiz-test-sandbox.md`
- Status: `completed`

## [2026-11-10] session | Build autonomous kit onboarding skill, resizable widget UI and full quiz technical documentation

- Raw: `raw/sessions/2026-11-10-build-autonomous-kit-onboarding-skill-resizable-.md`
- Tags: `activity:implementation`, `status:completed`, `task:build-autonomous-kit-onboarding-skill`, `project:quiz-product-set-generator`, `component:matching-rules`, `component:product-catalog`, `topic:architecture`, `topic:quiz`, `topic:prototype-ui`, `file:wiki/projects/quiz-engine-technical-documentation.md`, `file:public/index.html`
- Status: `completed`
