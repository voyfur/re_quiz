const copy = {
  ru: {
    windowTitle: "Квиз Race Expert — просмотр черновика",
    menuFile: "Файл",
    menuHelp: "Справка",
    languageLabel: "Язык",
    testLabel: "ТЕСТОВАЯ ВЕРСИЯ",
    testNotice: "Это первый просмотр покупательского квиза. Цена взята из локального снимка; состав и наличие на сайте не обновляются.",
    goalTitle: "Для какой ситуации вы ищете набор?",
    goalHint: "Сначала выберите задачу. Следующие вопросы будут зависеть от неё и от ответов.",
    chooseOne: "Выберите один вариант",
    any: "Не имеет значения",
    stepFirst: "Вопрос 1",
    stepCount: "Вопрос {current} из {total}",
    hintActivity: "Если нужного вида нет в списке, выберите «Другая активность»: квиз не подменит её ближайшей категорией.",
    hintComponentClass: "Известное расхождение по типу товара исключает набор. Если тип не принципиален, выберите «Неважно».",
    hintMembership: "Абонемент даёт доступ к сообществу и тренировочным программам клуба.",
    hintSoft: "Известное расхождение не попадёт в обычную выдачу. Варианты с неизвестными данными можно запросить отдельно.",
    hintContext: "Если сложно выбрать, отметьте «Неважно». Известное расхождение не попадёт в обычную выдачу; неизвестные данные можно посмотреть отдельно.",
    hintRace: "Показываем только форматы, которые явно встречаются в этой ветке. Километраж не предполагаем; известные расхождения не попадут в обычную выдачу.",
    hintSeason: "Сезонные сигналы есть не у всех наборов. Неизвестная погода не считается несовпадением, но такие варианты показываются отдельно.",
    hintSize: "Размер спрашиваем, когда в оставшихся наборах есть товар с подтверждённым диапазоном, в том числе в подарочной ветке. Неизвестный размер можно посмотреть отдельно.",
    hintBudget: "Подходящие наборы по вашим критериям: от {min} до {max} ₴ (на {date}). Пустое поле — без ограничения.",
    sizeValues: "В этой ветке встречаются размеры: {sizes}.",
    back: "Назад",
    continue: "Продолжить",
    showResults: "Показать варианты",
    resultsLabel: "Результат тестового подбора",
    editAnswers: "Изменить ответы",
    statusReady: "Готово",
    catalogStatus: "Локальный каталог · 206 наборов",
    goalRequired: "Выберите ситуацию, чтобы продолжить.",
    answerRequired: "Выберите вариант или оставьте поле пустым.",
    loading: "Подбираем следующий вопрос…",
    requestFailed: "Не удалось выполнить локальный подбор. Убедитесь, что запущен сервер.",
    fileModeHelp: "Этот HTML открыт напрямую и не может загрузить варианты. Запустите python3 server.py из папки test-quiz-sandbox, затем откройте http://127.0.0.1:8765/draft.",
    matches: "Точных совпадений: {count}",
    generalResults: "Вариантов без противоречий: {count}",
    relaxedResults: "Вариантов с ослаблением предпочтений: {count}",
    noExactResults: "Точных совпадений не найдено",
    noResults: "Подходящих вариантов не найдено",
    price: "Цена по снимку",
    snapshot: "на",
    openSource: "Открыть карточку набора",
    noResultsMessage: "По ответам и ограничениям совпадений в локальном снимке нет.",
    match_exact: "Совпадает с указанными ответами",
    match_general: "Нет известных противоречий; часть данных неизвестна",
    match_relaxed: "Показано с ослаблением мягких предпочтений",
    match_near_miss: "Близко по бюджету",
    match_floor_anchor: "Базовый старт",
    stockInStock: "В наличии",
    stockOutOfStock: "Нет в наличии",
    stockVerifiedLive: "Склад проверен онлайн",
    checkingStock: "Сверяем остатки на складе...",
    floorAnchorResults: "Базовый вариант в выбранной категории",
    floorAnchorHeading: "Минимальный стартовый набор в категории",
    budgetPlaceholder: "От {min} ₴ (или пусто)",
    nearMissHeading: "Альтернативы с небольшим превышением бюджета",
    overBudgetTag: "+{amount} ₴ к бюджету",
    unknownPreferences: "Нет данных для подтверждения: {fields}.",
    relaxedPreferences: "Не совпадает с выбранными значениями: {fields}.",
    showGeneral: "Показать варианты с неизвестными данными ({count})",
    showRelaxed: "Показать варианты с ослаблением предпочтений ({count})",
    membershipIncluded: "В набор включён абонемент Race Expert Club.",
    membershipMentioned: "Название упоминает Club; наличие абонемента не подтверждено.",
    goal_running: "Бег и старты",
    goal_training: "Тренировки и сила",
    goal_hydration: "Гидратация",
    goal_food: "Перекусы и питание",
    goal_recovery: "Восстановление и отдых",
    goal_outdoors: "Походы и активный отдых",
    goal_gear: "Одежда и аксессуары",
    goal_daily: "Ежедневное использование",
    goal_gift: "Подарок",
    question_activity: "Какой вид активности подходит к вашей задаче?",
    question_component_class: "Какой тип товара вам нужен в наборе?",
    question_membership: "Вам нужен набор с абонементом Race Expert Club?",
    question_use_scenario: "Что ближе к вашей ситуации?",
    question_use_timing: "Когда будете использовать набор?",
    question_use_place: "Где будете использовать товары?",
    question_race_format: "К какому формату старта подбираете набор?",
    question_season: "Для каких погодных условий подбираете?",
    question_product_form: "Какая форма продукта вам удобнее?",
    question_shoe_size: "Какой размер обуви или носков нужен?",
    question_budget: "Какова максимальная цена всего набора?",
    membership_yes: "Да, с абонементом",
    membership_no: "Нет, только товары без абонемента",
    activity_running: "Бег",
    activity_strength_training: "Силовые тренировки",
    activity_functional_training: "Функциональные тренировки",
    activity_cycling: "Велоспорт",
    activity_hiking: "Походы",
    activity_swimming: "Плавание",
    activity_mind_body_mobility: "Йога, пилатес и мобильность",
    activity_walking: "Ходьба",
    activity_general_fitness: "Общая физическая активность",
    activity_other: "Другая активность, не указана в списке",
    class_protein_carbohydrate_food: "Питание и перекусы",
    class_supplements_vitamins_minerals: "Витамины и добавки",
    class_creatine_preworkout: "Креатин и предтренировочные продукты",
    class_sports_accessories: "Спортивные аксессуары",
    class_apparel_footwear: "Одежда и обувь",
    class_hydration_items: "Гидратация",
    class_dehydrated_meal: "Сублимированная еда",
    scenario_event_preparation: "Подготовка к старту",
    scenario_training: "Тренировки",
    scenario_everyday: "На каждый день",
    context_before_or_after_training: "До или после тренировки",
    context_during_training: "Во время тренировки",
    context_daily_use: "Ежедневное использование",
    context_evening_or_bedtime: "Вечером или перед сном",
    context_hiking_or_camping: "В походе или кемпинге",
    context_travel_or_road: "В дороге",
    context_work_or_study: "На работе или учёбе",
    context_gift: "В подарок",
    race_half_marathon: "Полумарафон",
    race_marathon: "Марафон",
    race_race_or_event_preparation: "Другой старт или событие",
    race_ultra_or_long_distance: "Ультра или длительный старт",
    season_cold: "Холодная погода",
    season_warm: "Тёплая погода или лето",
    form_bars: "Батончики",
    form_food_or_meal: "Еда или готовый приём пищи",
    form_gel: "Гели",
    form_liquid: "Жидкая форма",
    form_sticks: "Стики",
    form_capsules: "Капсулы",
    form_powder: "Порошок",
    form_softgels: "Софтгели",
    form_tablets: "Таблетки",
    form_apparel: "Одежда",
    dataUnknownSize: "Размер товара не указан в снимке; совпадение не подтверждено.",
    reasonSeller: "Продавец позиционирует набор для выбранной задачи.",
    reasonComponent: "В списке состава есть товар, связанный с этой задачей.",
    noteConflict: "В карточке есть неразрешённое расхождение состава; проверьте актуальную страницу.",
    noteSnapshot: "Цена и наличие не обновляются в реальном времени."
  },
  uk: {
    windowTitle: "Квіз Race Expert — перегляд чернетки",
    menuFile: "Файл",
    menuHelp: "Довідка",
    languageLabel: "Мова",
    testLabel: "ТЕСТОВА ВЕРСІЯ",
    testNotice: "Це перший перегляд квізу для покупців. Ціну взято з локального знімка; склад і наявність на сайті не оновлюються.",
    goalTitle: "Для якої ситуації ви шукаєте набір?",
    goalHint: "Спочатку виберіть задачу. Наступні питання залежатимуть від неї та ваших відповідей.",
    chooseOne: "Виберіть один варіант",
    any: "Не має значення",
    stepFirst: "Питання 1",
    stepCount: "Питання {current} з {total}",
    hintActivity: "Якщо потрібного виду немає у списку, виберіть «Інша активність»: квіз не замінить її найближчою категорією.",
    hintComponentClass: "Відома розбіжність за типом товару виключає набір. Якщо тип не критичний, виберіть «Неважливо».",
    hintMembership: "Абонемент відкриває доступ до спільноти та тренувальних планів клубу.",
    hintSoft: "Відома розбіжність не потрапить до звичайної видачі. Варіанти з невідомими даними можна запросити окремо.",
    hintContext: "Якщо складно вибрати, позначте «Неважливо». Відома розбіжність не потрапить до звичайної видачі; невідомі дані можна переглянути окремо.",
    hintRace: "Показуємо лише формати, які явно є в цій гілці. Кілометраж не припускаємо; відомі розбіжності не потраплять до звичайної видачі.",
    hintSeason: "Сезонні сигнали є не в усіх наборах. Невідома погода не вважається невідповідністю, але такі варіанти показуємо окремо.",
    hintSize: "Розмір запитуємо, коли серед наборів є товар із підтвердженим діапазоном, зокрема у гілці подарунків. Невідомий розмір можна переглянути окремо.",
    hintBudget: "Відповідні набори за вашими критеріями: від {min} до {max} ₴ (на {date}). Порожнє поле — без обмеження.",
    sizeValues: "У цій гілці є розміри: {sizes}.",
    back: "Назад",
    continue: "Продовжити",
    showResults: "Показати варіанти",
    resultsLabel: "Результат тестового підбору",
    editAnswers: "Змінити відповіді",
    statusReady: "Готово",
    catalogStatus: "Локальний каталог · 206 наборів",
    goalRequired: "Виберіть ситуацію, щоб продовжити.",
    answerRequired: "Виберіть варіант або залиште поле порожнім.",
    loading: "Добираємо наступне питання…",
    requestFailed: "Не вдалося виконати локальний підбір. Перевірте, чи запущений сервер.",
    fileModeHelp: "Цей HTML відкрито напряму, тому він не може завантажити варіанти. Запустіть python3 server.py з теки test-quiz-sandbox, а потім відкрийте http://127.0.0.1:8765/draft.",
    matches: "Точних збігів: {count}",
    generalResults: "Варіантів без суперечностей: {count}",
    relaxedResults: "Варіантів із послабленням переваг: {count}",
    noExactResults: "Точних збігів не знайдено",
    noResults: "Відповідних варіантів не знайдено",
    price: "Ціна за знімком",
    snapshot: "на",
    openSource: "Відкрити картку набору",
    noResultsMessage: "За відповідями та обмеженнями збігів у локальному знімку немає.",
    match_exact: "Відповідає вказаним відповідям",
    match_general: "Немає відомих суперечностей; частина даних невідома",
    match_relaxed: "Показано з послабленням м’яких переваг",
    match_near_miss: "Близько за бюджетом",
    match_floor_anchor: "Базовий старт",
    stockInStock: "В наявності",
    stockOutOfStock: "Немає в наявності",
    stockVerifiedLive: "Склад перевірено онлайн",
    checkingStock: "Звіряємо залишки на складі...",
    floorAnchorResults: "Базовий варіант у вибраній категорії",
    floorAnchorHeading: "Мінімальний стартовий набір у категорії",
    budgetPlaceholder: "Від {min} ₴ (або порожньо)",
    nearMissHeading: "Альтернативи з невеликим перевищенням бюджету",
    overBudgetTag: "+{amount} ₴ до бюджету",
    unknownPreferences: "Немає даних для підтвердження: {fields}.",
    relaxedPreferences: "Не відповідає вибраним значенням: {fields}.",
    showGeneral: "Показати варіанти з невідомими даними ({count})",
    showRelaxed: "Показати варіанти з послабленням переваг ({count})",
    membershipIncluded: "До набору входить абонемент Race Expert Club.",
    membershipMentioned: "У назві згадано Club; наявність абонемента не підтверджена.",
    goal_running: "Біг і старти",
    goal_training: "Тренування та сила",
    goal_hydration: "Гідратація",
    goal_food: "Перекуси та харчування",
    goal_recovery: "Відновлення та відпочинок",
    goal_outdoors: "Походи й активний відпочинок",
    goal_gear: "Одяг та аксесуари",
    goal_daily: "Щоденне використання",
    goal_gift: "Подарунок",
    question_activity: "Який вид активності відповідає вашій задачі?",
    question_component_class: "Який тип товару вам потрібен у наборі?",
    question_membership: "Вам потрібен набір з абонементом Race Expert Club?",
    question_use_scenario: "Що найбільше відповідає вашій ситуації?",
    question_use_timing: "Коли використовуватимете набір?",
    question_use_place: "Де використовуватимете товари?",
    question_race_format: "Для якого формату старту шукаєте набір?",
    question_season: "Для яких погодних умов шукаєте?",
    question_product_form: "Яка форма продукту вам зручніша?",
    question_shoe_size: "Який розмір взуття чи шкарпеток потрібен?",
    question_budget: "Яка максимальна ціна всього набору?",
    membership_yes: "Так, з абонементом",
    membership_no: "Ні, лише товари без абонемента",
    activity_running: "Біг",
    activity_strength_training: "Силові тренування",
    activity_functional_training: "Функціональні тренування",
    activity_cycling: "Велоспорт",
    activity_hiking: "Походи",
    activity_swimming: "Плавання",
    activity_mind_body_mobility: "Йога, пілатес і мобільність",
    activity_walking: "Ходьба",
    activity_general_fitness: "Загальна фізична активність",
    activity_other: "Інша активність, якої немає у списку",
    class_protein_carbohydrate_food: "Харчування та перекуси",
    class_supplements_vitamins_minerals: "Вітаміни та добавки",
    class_creatine_preworkout: "Креатин і передтренувальні продукти",
    class_sports_accessories: "Спортивні аксесуари",
    class_apparel_footwear: "Одяг і взуття",
    class_hydration_items: "Гідратація",
    class_dehydrated_meal: "Сублімована їжа",
    scenario_event_preparation: "Підготовка до старту",
    scenario_training: "Тренування",
    scenario_everyday: "На щодень",
    context_before_or_after_training: "До або після тренування",
    context_during_training: "Під час тренування",
    context_daily_use: "Щоденне використання",
    context_evening_or_bedtime: "Увечері або перед сном",
    context_hiking_or_camping: "У поході або кемпінгу",
    context_travel_or_road: "У дорозі",
    context_work_or_study: "На роботі або навчанні",
    context_gift: "У подарунок",
    race_half_marathon: "Напівмарафон",
    race_marathon: "Марафон",
    race_race_or_event_preparation: "Інший старт або подія",
    race_ultra_or_long_distance: "Ультра або тривалий старт",
    season_cold: "Холодна погода",
    season_warm: "Тепла погода або літо",
    form_bars: "Батончики",
    form_food_or_meal: "Їжа або готовий прийом їжі",
    form_gel: "Гелі",
    form_liquid: "Рідка форма",
    form_sticks: "Стики",
    form_capsules: "Капсули",
    form_powder: "Порошок",
    form_softgels: "Софтгелі",
    form_tablets: "Таблетки",
    form_apparel: "Одяг",
    dataUnknownSize: "Розмір товару не вказаний у знімку; збіг не підтверджено.",
    reasonSeller: "Продавець позиціонує набір для вибраної задачі.",
    reasonComponent: "У переліку складу є товар, пов'язаний із цією задачею.",
    noteConflict: "У картці є невирішена розбіжність складу; перевірте актуальну сторінку.",
    noteSnapshot: "Ціна й наявність не оновлюються в реальному часі."
  }
};

const state = {
  locale: "ru",
  goals: [],
  selectedGoal: "",
  answers: {},
  questionPlan: [],
  currentId: "goal",
  history: [],
  lastRequest: null,
  lastResponse: null,
  facets: null,
  loading: false
};

const byId = (id) => document.getElementById(id);

function tr(key) {
  return copy[state.locale][key] || copy.ru[key] || key;
}

function format(key, values) {
  return Object.entries(values).reduce(
    (value, [name, replacement]) => value.replaceAll("{" + name + "}", replacement),
    tr(key)
  );
}

function element(tag, className, text) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text !== undefined && text !== null) node.textContent = text;
  return node;
}

function applyCopy() {
  document.documentElement.lang = state.locale;
  document.querySelectorAll("[data-i18n]").forEach((node) => {
    node.textContent = tr(node.dataset.i18n);
  });
  document.title = tr("windowTitle");
  renderQuestion();
  if (state.lastResponse) renderResponse(state.lastResponse);
}

function valueLabel(questionId, value) {
  const prefixes = {
    activity: "activity_",
    component_class: "class_",
    membership: "membership_",
    use_scenario: "scenario_",
    use_timing: "context_",
    use_place: "context_",
    race_format: "race_",
    season: "season_",
    product_form: "form_"
  };
  const key = (prefixes[questionId] || "") + value;
  return tr(key);
}

function currentQuestion() {
  if (state.currentId === "goal") {
    return { id: "goal", type: "single", options: state.goals.map((goal) => goal.value) };
  }
  return state.questionPlan.find((question) => question.id === state.currentId) || null;
}

function setStepMeta(question) {
  if (!question || question.id === "goal") {
    byId("step-counter").textContent = tr("stepFirst");
    byId("step-fill").style.width = "12.5%";
    return;
  }
  const total = Math.max(state.history.length + state.questionPlan.length, 2);
  const current = state.history.length + 1;
  byId("step-counter").textContent = format("stepCount", { current, total });
  byId("step-fill").style.width = (100 * current / total) + "%";
}

function renderSingleOptions(question, options, selectedValue, legend) {
  const container = byId("question-options");
  container.replaceChildren();
  byId("question-legend").textContent = legend;
  byId("question-fieldset").hidden = false;
  byId("question-number-wrap").hidden = true;
  const values = question.id === "goal" ? options : [...options.filter(o => o !== "any"), "any"];
  values.forEach((value) => {
    const label = element("label", "goal-option");
    const input = document.createElement("input");
    input.type = "radio";
    input.name = "answer";
    input.value = value;
    input.checked = value === selectedValue;
    const text = question.id === "goal" ? tr("goal_" + value) : value === "any" ? tr("any") : valueLabel(question.id, value);
    label.append(input, element("span", null, text));
    container.append(label);
  });
}

function questionHint(question) {
  if (!question || question.id === "goal") return tr("goalHint");
  if (question.id === "activity") return tr("hintActivity");
  if (question.id === "component_class") return tr("hintComponentClass");
  if (question.id === "membership") return tr("hintMembership");
  if (question.id === "product_form") return tr("hintSoft");
  if (question.id === "use_scenario" || question.id === "use_timing" || question.id === "use_place") return tr("hintContext");
  if (question.id === "race_format") return tr("hintRace");
  if (question.id === "season") return tr("hintSeason");
  if (question.id === "shoe_size") return tr("hintSize");
  return "";
}

function renderQuestion() {
  const question = currentQuestion();
  if (!question) return;
  byId("question-step").hidden = false;
  const titleKey = question.id === "goal" ? "goalTitle" : question.title_key;
  byId("question-title").textContent = tr(titleKey);
  const hint = questionHint(question);
  byId("question-hint").textContent = hint;
  byId("question-hint").hidden = !hint;
  setStepMeta(question);

  if (question.type === "number") {
    byId("question-options").replaceChildren();
    byId("question-legend").textContent = "";
    byId("question-fieldset").hidden = false;
    byId("question-number-wrap").hidden = false;
    const input = byId("question-number");
    input.min = String(question.min ?? 0);
    input.max = question.max === undefined ? "" : String(question.max);
    const savedValue = state.answers[question.id];
    input.value = savedValue === "any" || savedValue === undefined ? "" : String(savedValue);
    byId("question-number-label").textContent = tr(titleKey);
    if (question.id === "shoe_size") {
      input.placeholder = "";
      const ranges = question.ranges || [];
      byId("question-number-hint").textContent = ranges.length ? format("sizeValues", { sizes: ranges.join(", ") }) : tr("hintSize");
    } else if (question.id === "max_price_uah") {
      const minVal = question.dynamic_min ?? state.facets?.price_range_uah?.min;
      const maxVal = question.dynamic_max ?? state.facets?.price_range_uah?.max;
      if (minVal !== undefined && maxVal !== undefined) {
        input.placeholder = format("budgetPlaceholder", {
          min: minVal.toLocaleString(state.locale === "ru" ? "ru-RU" : "uk-UA")
        });
        byId("question-number-hint").textContent = format("hintBudget", {
          date: state.facets?.price_snapshot_date || "—",
          min: minVal.toLocaleString(state.locale === "ru" ? "ru-RU" : "uk-UA"),
          max: maxVal.toLocaleString(state.locale === "ru" ? "ru-RU" : "uk-UA")
        });
      } else {
        input.placeholder = "";
        byId("question-number-hint").textContent = "";
      }
    } else {
      input.placeholder = "";
      byId("question-number-hint").textContent = "";
    }
  } else {
    const selected = question.id === "goal" ? state.selectedGoal : state.answers[question.id];
    renderSingleOptions(question, question.options || [], selected, tr("chooseOne"));
  }

  byId("next-button").hidden = question.id === "max_price_uah";
  byId("submit-button").hidden = question.id !== "max_price_uah";
  byId("back-button").hidden = state.history.length === 0;
  byId("status-text").textContent = state.loading ? tr("loading") : tr("statusReady");
}

function showError(message) {
  byId("form-error").textContent = message;
  byId("form-error").hidden = !message;
}

async function fetchJson(url, options) {
  if (window.QUIZ_MATCHER && (window.location.protocol === "file:" || state.useLocalFallback)) {
    return window.QUIZ_MATCHER.handleRequest(url, options);
  }
  try {
    const response = await fetch(url, options);
    const payload = await response.json();
    if (!response.ok) throw new Error(payload.error || tr("requestFailed"));
    return payload;
  } catch (error) {
    if (window.QUIZ_MATCHER) {
      state.useLocalFallback = true;
      return window.QUIZ_MATCHER.handleRequest(url, options);
    }
    throw error;
  }
}

async function loadPlan(answers = state.answers) {
  const params = new URLSearchParams({ goal_group: state.selectedGoal });
  Object.entries(answers).forEach(([key, value]) => {
    if (value !== undefined && value !== null && value !== "") params.set(key, String(value));
  });
  state.loading = true;
  renderQuestion();
  try {
    state.facets = await fetchJson("/api/draft/options?" + params.toString());
    state.questionPlan = state.facets.question_plan || [];
    showError("");
  } catch (error) {
    showError(error.message || tr("requestFailed"));
    throw error;
  } finally {
    state.loading = false;
    renderQuestion();
  }
}

function readCurrentAnswer(question) {
  if (question.type === "number") {
    const value = byId("question-number").value;
    return value === "" ? "any" : Number(value);
  }
  return document.querySelector('input[name="answer"]:checked')?.value || "";
}

function buildRequest() {
  const request = { goal_group: state.selectedGoal, locale: state.locale };
  Object.entries(state.answers).forEach(([key, value]) => {
    if (value === "any" || value === "" || value === undefined) return;
    request[key] = value;
  });
  return request;
}

function renderCard(item) {
  const card = element("article", "result-card");
  const top = element("div", "result-top");
  top.append(element("span", null, "№ " + item.catalog_row));
  if (item.sku) top.append(element("span", null, item.sku));
  if (item.match_score_pct) {
    top.append(element("span", "match-score", item.match_score_pct + "%"));
  }
  if (item.price_over_budget_uah > 0) {
    top.append(element("span", "near-miss-tag", format("overBudgetTag", { amount: item.price_over_budget_uah })));
  }
  top.append(element("span", "match-badge", tr("match_" + item.match_type)));
  if (item.stock_info && item.stock_info.is_live_check) {
    if (item.stock_info.in_stock) {
      top.append(element("span", "stock-badge in-stock", tr("stockInStock")));
    } else {
      const outLabel = state.locale === "ru" ? (item.stock_info.stock_status_text_ru || tr("stockOutOfStock")) : (item.stock_info.stock_status_text_uk || tr("stockOutOfStock"));
      top.append(element("span", "stock-badge out-of-stock", outLabel));
    }
  }
  card.append(top, element("h3", null, item.title));
  if (item.membership_status === "included") {
    card.append(element("p", "result-note", tr("membershipIncluded")));
  } else if (item.membership_status === "mentioned") {
    card.append(element("p", "result-note", tr("membershipMentioned")));
  }
  const priceMeta = item.stock_info?.is_live_check ? tr("stockVerifiedLive") : (tr("snapshot") + " " + item.price_snapshot_date);
  card.append(element("p", "result-price",
    tr("price") + ": " + item.price_uah.toLocaleString(state.locale === "ru" ? "ru-RU" : "uk-UA") +
    " ₴ · " + priceMeta
  ));
  if (item.reasons?.length) {
    const reasons = element("ul");
    item.reasons.forEach((reason) => reasons.append(element("li", null, reason)));
    card.append(reasons);
  }
  if (item.unknown_preferences?.length) {
    const fields = item.unknown_preferences.map((key) => tr("question_" + key)).join(", ");
    card.append(element("p", "result-note", format("unknownPreferences", { fields })));
  } else if (item.size_status === "unknown") {
    card.append(element("p", "result-note", tr("dataUnknownSize")));
  }
  if (item.relaxed_preferences?.length) {
    const fields = item.relaxed_preferences.map((key) => {
      const selected = item.relaxed_preference_values?.[key];
      const label = tr("question_" + key);
      return selected ? label + " (" + valueLabel(key, selected) + ")" : label;
    }).join(", ");
    card.append(element("p", "result-note", format("relaxedPreferences", { fields })));
  }
  if (item.evidence_status === "conflict_review_required") {
    card.append(element("p", "result-note", tr("noteConflict")));
  }
  card.append(element("p", "result-note", tr("noteSnapshot")));
  const source = document.createElement("a");
  source.href = item.source_url;
  source.target = "_blank";
  source.rel = "noopener noreferrer";
  source.textContent = tr("openSource");
  card.append(source);
  return card;
}

function renderResponse(response) {
  const titleKey = {
    matched: "matches",
    general_auto: "generalResults",
    general: "generalResults",
    relaxed: "relaxedResults",
    no_exact_match: "noExactResults",
    floor_anchor: "floorAnchorResults"
  }[response.status] || "noResults";
  byId("results-title").textContent = ["matched", "general_auto", "general", "relaxed"].includes(response.status)
    ? format(titleKey, { count: response.returned_count })
    : tr(titleKey);
  byId("results-message").textContent = response.message || tr("noResultsMessage");
  const actions = byId("fallback-actions");
  actions.replaceChildren();
  (response.fallback_options || []).forEach((option) => {
    const key = option.mode === "general" ? "showGeneral" : "showRelaxed";
    const button = element("button", null, format(key, { count: option.count }));
    button.type = "button";
    button.addEventListener("click", () => {
      if (state.lastRequest) {
        requestRecommendations({ ...state.lastRequest, fallback_mode: option.mode });
      }
    });
    actions.append(button);
  });
  actions.hidden = actions.childElementCount === 0;
  const list = byId("results-list");
  list.replaceChildren();
  (response.results || []).forEach((item) => list.append(renderCard(item)));

  if (response.near_miss_results && response.near_miss_results.length > 0) {
    const nearMissSec = element("section", "near-miss-section");
    nearMissSec.append(element("h3", null, tr("nearMissHeading")));
    const nearMissList = element("div", "results-list");
    response.near_miss_results.forEach((item) => nearMissList.append(renderCard(item)));
    nearMissSec.append(nearMissList);
    list.append(nearMissSec);
  }

  if (response.floor_anchor_results && response.floor_anchor_results.length > 0) {
    const floorSec = element("section", "floor-anchor-section");
    floorSec.append(element("h3", null, tr("floorAnchorHeading")));
    const floorList = element("div", "results-list");
    response.floor_anchor_results.forEach((item) => floorList.append(renderCard(item)));
    floorSec.append(floorList);
    list.append(floorSec);
  }

  byId("question-step").hidden = true;
  byId("results-section").hidden = false;
  byId("quiz-form").hidden = true;
  byId("step-counter").textContent = tr("resultsLabel");
  byId("step-fill").style.width = "100%";
}

async function requestRecommendations(request) {
  byId("submit-button").disabled = true;
  showError("");
  try {
    const payload = { ...request, verify_stock: true };
    const response = await fetchJson("/api/draft/recommend", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });
    state.lastRequest = request;
    state.lastResponse = response;
    renderResponse(response);
  } catch (error) {
    showError(error.message || tr("requestFailed"));
  } finally {
    byId("submit-button").disabled = false;
  }
}

async function continueQuiz() {
  const question = currentQuestion();
  if (!question) return;
  if (question.id === "goal") {
    if (!state.selectedGoal) {
      showError(tr("goalRequired"));
      return;
    }
    state.answers = {};
    state.history = ["goal"];
    try {
      await loadPlan();
      if (!state.questionPlan.length) {
        await requestRecommendations(buildRequest());
        return;
      }
      state.currentId = state.questionPlan[0].id;
      renderQuestion();
      byId("question-title").focus();
    } catch (_) {
      return;
    }
    return;
  }

  const value = readCurrentAnswer(question);
  if (value === "") {
    showError(tr("answerRequired"));
    return;
  }
  showError("");
  state.answers[question.id] = value;
  state.history.push(question.id);
  try {
    await loadPlan();
    if (!state.questionPlan.length) {
      await requestRecommendations(buildRequest());
      return;
    }
    state.currentId = state.questionPlan[0].id;
    renderQuestion();
    byId("question-title").focus();
  } catch (_) {
    return;
  }
}

async function goBack() {
  if (!state.history.length) return;
  const previous = state.history.pop();
  if (previous === "goal") {
    state.selectedGoal = "";
    state.answers = {};
    state.questionPlan = [];
    state.facets = null;
    state.currentId = "goal";
    renderQuestion();
    byId("question-title").focus();
    return;
  }
  delete state.answers[previous];
  state.currentId = previous;
  try {
    await loadPlan();
    renderQuestion();
    byId("question-title").focus();
  } catch (_) {
    return;
  }
}

async function init() {
  if (window.location.protocol === "file:" && !window.QUIZ_MATCHER) {
    byId("launch-error").textContent = tr("fileModeHelp");
    byId("launch-error").hidden = false;
    byId("quiz-form").hidden = true;
    return;
  }

  try {
    const payload = await fetchJson("/api/draft/options");
    state.goals = payload.goal_options || [];
    byId("catalog-status").textContent = tr("catalogStatus");
  } catch (error) {
    showError(error.message || tr("requestFailed"));
  }

  byId("question-options").addEventListener("change", (event) => {
    if (state.currentId === "goal") state.selectedGoal = event.target.value;
  });
  byId("next-button").addEventListener("click", continueQuiz);
  byId("back-button").addEventListener("click", goBack);
  byId("quiz-form").addEventListener("submit", (event) => {
    event.preventDefault();
    const question = currentQuestion();
    if (!question || question.id !== "max_price_uah") return;
    const value = readCurrentAnswer(question);
    if (value !== "any") state.answers.max_price_uah = value;
    requestRecommendations(buildRequest());
  });
  byId("edit-button").addEventListener("click", () => {
    state.selectedGoal = "";
    state.answers = {};
    state.questionPlan = [];
    state.history = [];
    state.facets = null;
    state.currentId = "goal";
    state.lastRequest = null;
    state.lastResponse = null;
    byId("results-section").hidden = true;
    byId("quiz-form").hidden = false;
    renderQuestion();
  });
  byId("locale").addEventListener("change", async (event) => {
    state.locale = event.target.value;
    applyCopy();
    if (state.selectedGoal && state.currentId !== "goal" && !state.lastResponse) {
      try {
        await loadPlan();
      } catch (_) {
        return;
      }
    }
    if (state.lastRequest) {
      await requestRecommendations({ ...state.lastRequest, locale: state.locale });
    }
  });
  renderQuestion();
}

applyCopy();
init();
