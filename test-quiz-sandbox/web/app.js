const copy = {
  ru: {
    languageLabel: "Язык", eyebrow: "Локальная тестовая версия", title: "Подбор наборов Race Expert",
    intro: "Ответьте на несколько вопросов. Квиз сопоставит ответы с тегами и составом 206 наборов из локального снимка каталога.",
    notice: "Экспериментальная логика ещё не утверждена. Результаты — альтернативы для проверки тегов каталога, не оценка безопасности, эффективности или совместимости. Ответы не сохраняются.",
    stepCounter: "Шаг {current} из {total}", stepName1: "Цель", stepName2: "Предпочтения", stepName3: "Ограничения", stepName4: "Результат",
    step1Title: "Для чего вы ищете набор?", step1Subtitle: "Выберите близкую тему. Это не выбор готового набора — квиз сам найдёт варианты.",
    goalLegend: "Что вам ближе?", goalRequired: "Выберите тему подбора, чтобы продолжить.",
    goal_running: "Бег и подготовка к стартам", goalHint_running: "Бег, соревнования и выносливость",
    goal_training: "Тренировки и силовые занятия", goalHint_training: "Зал, сила и регулярные тренировки",
    goal_recovery: "Восстановление и отдых", goalHint_recovery: "Темы восстановления, отдыха и сна в каталоге",
    goal_food: "Перекусы и питание", goalHint_food: "Перекусы, батончики и готовая еда",
    goal_outdoors: "Походы и поездки", goalHint_outdoors: "Питание и наборы для дороги и природы",
    goal_gear: "Одежда и экипировка", goalHint_gear: "Одежда, аксессуары и спортивный комфорт",
    goal_daily: "Повседневная активность", goalHint_daily: "Общие темы ежедневной активности и рутины",
    goal_gift: "Ищу подарок", goalHint_gift: "Готовые наборы, отмеченные в каталоге как подарочные",
    step2Title: "Что ещё учесть?", step2Subtitle: "Уточните активность или формат набора. Этот шаг можно пропустить.",
    step3Title: "Есть ли важные ограничения?", step3Subtitle: "Укажите только то, что нужно учесть. Необязательные поля можно оставить пустыми.",
    step4Title: "Сколько вариантов показать?", step4Subtitle: "Подбор вернёт только подходящие наборы; если их меньше, лишние не добавит.",
    reviewTitle: "Ваши ответы", summaryGoal: "Тема", summarySport: "Активность", summaryType: "Тип набора",
    summaryForm: "Форма", summaryRace: "Формат старта", summaryComponent: "Компонент", summaryBudget: "Бюджет до",
    summaryShoe: "Размер обуви", summaryCaffeine: "Без кофеина", summaryStock: "Только отмеченные в наличии",
    summaryCount: "Количество вариантов", anySelected: "Не выбрано",
    back: "Назад", continue: "Продолжить", showMatches: "Показать варианты", anySport: "Любой / не учитывать", anyType: "Любой тип",
    sportLabel: "Вид спорта", typeLabel: "Тип набора", formLabel: "Форма товара", anyForm: "Любая форма", raceFormatLabel: "Формат старта", anyRaceFormat: "Не учитывать", budgetLabel: "Максимальная цена, грн", budgetPlaceholder: "Без ограничения",
    shoeLabel: "Размер обуви", shoePlaceholder: "Не учитывать", shoeHelp: "Применяется только к наборам с подтверждённым диапазоном размера.",
    componentLabel: "Компонент в составе", anyComponent: "Не фильтровать по компоненту", caffeineLabel: "Кофеин", caffeineAny: "Не учитывать",
    caffeineAvoid: "Только если отсутствие подтверждено", stockOnly: "Только наборы с явно отмеченным наличием", resultCountLabel: "Количество вариантов",
    dataEyebrow: "Снимок данных", dataTitle: "Что учитывает прототип",
    dataPrice: "Цена полного набора в гривнах — из снимка на 2026-11-06; наличие также не обновляется в реальном времени.",
    dataUnknown: "Неизвестное значение остаётся неизвестным; квиз не заполняет пробелы догадками.",
    dataCaffeine: "В каталоге нет подтверждения отсутствия кофеина — строгий фильтр остановит подбор.",
    dataDistance: "Числовой дистанции в карточках нет. Формат старта показывается только как текстовый тег каталога.",
    dataDuration: "Тег «3 месяца» может относиться к абонементу клуба, поэтому срок не используется как длительность приёма.",
    dataLimits: "Возраст, вес покупателя и аллергены не предлагаются: подтверждённых структурированных данных недостаточно.",
    catalogCountLabel: "наборов в локальном снимке", priceSnapshotLabel: "Цены на дату", resultsEyebrow: "Результат тестового подбора",
    alternativeLabel: "Варианты-альтернативы", footer: "Тестовый каталог и правила не подключены к сайту и не сохраняют ответы.",
    requestFailed: "Не удалось выполнить локальный подбор. Проверьте, что сервер запущен.",
    matches: "Вариантов по вашим ответам: {count}", noResults: "По вашим ответам подходящих вариантов нет", price: "Цена", snapshot: "Снимок",
    openSource: "Открыть исходную карточку", composition: "Состав по карточке", description: "Назначение по карточке",
    caffeineStatus: "Кофеин", stockStatus: "Наличие", caffeine_present: "Отмечен в составе", caffeine_unknown: "Не проверен",
    caffeine_confirmed_absent: "Отсутствие подтверждено", availability_in_stock: "Отмечено в наличии в снимке", availability_out_of_stock: "Отмечено как нет в наличии в снимке",
    availability_unknown: "Не проверено", sizeNotRecorded: "Размер в этой карточке не указан.", sourceRow: "Строка снимка",
    noComposition: "Состав не указан в извлечённой карточке.", noDescription: "Дополнительное описание не указано.",
    tag_purpose: "назначение", tag_sport: "спорт", tag_item_type: "тип", tag_contains: "компонент", tag_shoe_size: "размер",
    tag_form: "форма", tag_race_format: "формат", tag_distance: "дистанция",
    tag_running: "бег", tag_hiking: "походы", tag_cycling: "велоспорт", tag_general_fitness: "фитнес",
    tag_strength_training: "силовые тренировки", tag_gym_training: "тренировки в зале", tag_yoga: "йога", tag_pilates: "пилатес",
    tag_active_recreation: "активный отдых", tag_crossfit: "кроссфит", tag_functional_training: "функциональные тренировки",
    tag_hiit: "интервальные тренировки", tag_intense_training: "интенсивные тренировки", tag_physical_activity_general: "общая физическая активность",
    tag_stretching: "растяжка", tag_swimming: "плавание", tag_training_general: "общие тренировки", tag_walking: "ходьба",
    tag_not_sport_specific: "без конкретного спорта", tag_supplement_bundle: "набор добавок", tag_snack_bundle: "набор перекусов",
    tag_equipment_bundle: "набор снаряжения", tag_apparel_bundle: "набор одежды", tag_apparel: "одежда", tag_food_bundle: "набор продуктов",
    tag_gift_bundle: "подарочный набор", tag_club_membership_bundle: "набор с клубным участием", tag_caffeine: "кофеин",
    tag_protein: "белок", tag_electrolytes: "электролиты", tag_magnesium: "магний", tag_creatine: "креатин",
    tag_5_htp: "5-HTP", tag_acetyl_l_carnitine: "ацетил-L-карнитин", tag_amanita: "мухомор", tag_amino_acids: "аминокислоты",
    tag_apple_cider_vinegar: "яблочный уксус", tag_arginine: "аргинин", tag_artichoke: "артишок", tag_ashwagandha: "ашваганда",
    tag_astaxanthin: "астаксантин", tag_bcaa: "BCAA", tag_beta_carotene: "бета-каротин", tag_biotin: "биотин",
    tag_boswellia: "босвеллия", tag_calcium: "кальций", tag_carbohydrate: "углевод", tag_carbohydrates: "углеводы",
    tag_cbd: "CBD", tag_choline: "холин", tag_chromium: "хром", tag_coenzyme_q10: "коэнзим Q10", tag_coq10: "CoQ10",
    tag_collagen: "коллаген", tag_copper: "медь", tag_cordyceps: "кордицепс", tag_curcumin: "куркумин", tag_dha: "DHA",
    tag_digestive_enzymes: "пищеварительные ферменты", tag_eaa: "EAA", tag_fiber: "клетчатка", tag_folic_acid: "фолиевая кислота",
    tag_gaba: "GABA", tag_ginger: "имбирь", tag_ginseng: "женьшень", tag_glutamine: "глутамин", tag_green_tea_extract: "экстракт зелёного чая",
    tag_inositol: "инозитол", tag_iron: "железо", tag_l_carnitine: "L-карнитин", tag_lion_s_mane: "ежовик гребенчатый",
    tag_lions_mane: "ежовик гребенчатый", tag_maca: "мака", tag_melatonin: "мелатонин", tag_milk_thistle: "расторопша",
    tag_minerals: "минералы", tag_msm: "MSM", tag_multivitamin: "мультивитаминный комплекс", tag_mushroom_complex: "комплекс грибов",
    tag_omega_3: "омега-3", tag_reishi: "рейши", tag_selenium: "селен", tag_shiitake: "шиитаке", tag_spirulina: "спирулина",
    tag_tribulus: "трибулус", tag_triphala: "трифала", tag_turmeric: "куркума", tag_vitamin_b: "витамин B",
    tag_vitamin_b12: "витамин B12", tag_vitamin_b_complex: "комплекс витаминов B", tag_vitamin_c: "витамин C",
    tag_vitamin_d: "витамин D", tag_vitamin_d3: "витамин D3", tag_vitamin_k2: "витамин K2", tag_whey_protein: "сывороточный белок",
    tag_zinc: "цинк",
    tag_capsules: "капсулы", tag_tablets: "таблетки", tag_bars: "батончики", tag_marathon: "марафон", tag_half_marathon: "полумарафон", tag_unspecified: "не указан",
    testOnly: "ТЕСТОВАЯ ВЕРСИЯ · ЛОГИКА НЕ УТВЕРЖДЕНА", noSources: "Источник не указан"
  },
  uk: {
    languageLabel: "Мова", eyebrow: "Локальна тестова версія", title: "Підбір наборів Race Expert",
    intro: "Дайте відповіді на кілька запитань. Квіз зіставить відповіді з тегами та складом 206 наборів із локального знімка каталогу.",
    notice: "Експериментальну логіку ще не затверджено. Результати — альтернативи для перевірки тегів каталогу, не оцінка безпеки, ефективності чи сумісності. Відповіді не зберігаються.",
    stepCounter: "Крок {current} із {total}", stepName1: "Мета", stepName2: "Побажання", stepName3: "Обмеження", stepName4: "Результат",
    step1Title: "Для чого ви шукаєте набір?", step1Subtitle: "Оберіть близьку тему. Це не вибір готового набору — квіз сам знайде варіанти.",
    goalLegend: "Що вам ближче?", goalRequired: "Оберіть тему підбору, щоб продовжити.",
    goal_running: "Біг і підготовка до стартів", goalHint_running: "Біг, змагання та витривалість",
    goal_training: "Тренування та силові заняття", goalHint_training: "Зал, сила та регулярні тренування",
    goal_recovery: "Відновлення та відпочинок", goalHint_recovery: "Теми відновлення, відпочинку та сну в каталозі",
    goal_food: "Перекуси та харчування", goalHint_food: "Перекуси, батончики й готова їжа",
    goal_outdoors: "Походи та подорожі", goalHint_outdoors: "Харчування й набори для дороги та природи",
    goal_gear: "Одяг і спорядження", goalHint_gear: "Одяг, аксесуари та спортивний комфорт",
    goal_daily: "Щоденна активність", goalHint_daily: "Загальні теми щоденної активності та рутини",
    goal_gift: "Шукаю подарунок", goalHint_gift: "Готові набори, позначені в каталозі як подарункові",
    step2Title: "Що ще врахувати?", step2Subtitle: "Уточніть активність або формат набору. Цей крок можна пропустити.",
    step3Title: "Чи є важливі обмеження?", step3Subtitle: "Вкажіть лише те, що потрібно врахувати. Необов’язкові поля можна лишити порожніми.",
    step4Title: "Скільки варіантів показати?", step4Subtitle: "Підбір поверне лише відповідні набори; якщо їх менше, зайвих не додасть.",
    reviewTitle: "Ваші відповіді", summaryGoal: "Тема", summarySport: "Активність", summaryType: "Тип набору",
    summaryForm: "Форма", summaryRace: "Формат старту", summaryComponent: "Компонент", summaryBudget: "Бюджет до",
    summaryShoe: "Розмір взуття", summaryCaffeine: "Без кофеїну", summaryStock: "Лише позначені в наявності",
    summaryCount: "Кількість варіантів", anySelected: "Не обрано",
    back: "Назад", continue: "Продовжити", showMatches: "Показати варіанти", anySport: "Будь-який / не враховувати", anyType: "Будь-який тип",
    sportLabel: "Вид спорту", typeLabel: "Тип набору", formLabel: "Форма товару", anyForm: "Будь-яка форма", raceFormatLabel: "Формат старту", anyRaceFormat: "Не враховувати", budgetLabel: "Максимальна ціна, грн", budgetPlaceholder: "Без обмеження",
    shoeLabel: "Розмір взуття", shoePlaceholder: "Не враховувати", shoeHelp: "Застосовується лише до наборів із підтвердженим діапазоном розміру.",
    componentLabel: "Компонент у складі", anyComponent: "Не фільтрувати за компонентом", caffeineLabel: "Кофеїн", caffeineAny: "Не враховувати",
    caffeineAvoid: "Лише якщо відсутність підтверджена", stockOnly: "Лише набори з явно позначеною наявністю", resultCountLabel: "Кількість варіантів",
    dataEyebrow: "Знімок даних", dataTitle: "Що враховує прототип",
    dataPrice: "Ціна повного набору у гривнях — зі знімка на 2026-11-06; наявність також не оновлюється в реальному часі.",
    dataUnknown: "Невідоме значення залишається невідомим; квіз не заповнює прогалини припущеннями.",
    dataCaffeine: "У каталозі немає підтвердження відсутності кофеїну — суворий фільтр зупинить підбір.",
    dataDistance: "У картках немає числової дистанції. Формат старту показано лише як текстовий тег каталогу.",
    dataDuration: "Тег «3 місяці» може стосуватися абонемента клубу, тому строк не використовується як тривалість приймання.",
    dataLimits: "Вік, вага покупця й алергени не пропонуються: підтверджених структурованих даних недостатньо.",
    catalogCountLabel: "наборів у локальному знімку", priceSnapshotLabel: "Ціни станом на", resultsEyebrow: "Результат тестового підбору",
    alternativeLabel: "Варіанти-альтернативи", footer: "Тестовий каталог і правила не підключені до сайту та не зберігають відповіді.",
    requestFailed: "Не вдалося виконати локальний підбір. Перевірте, чи запущено сервер.",
    matches: "Варіантів за вашими відповідями: {count}", noResults: "За вашими відповідями відповідних варіантів немає", price: "Ціна", snapshot: "Знімок",
    openSource: "Відкрити вихідну картку", composition: "Склад за карткою", description: "Призначення за карткою",
    caffeineStatus: "Кофеїн", stockStatus: "Наявність", caffeine_present: "Позначений у складі", caffeine_unknown: "Не перевірено",
    caffeine_confirmed_absent: "Відсутність підтверджено", availability_in_stock: "Позначено в наявності у знімку", availability_out_of_stock: "Позначено як немає в наявності у знімку",
    availability_unknown: "Не перевірено", sizeNotRecorded: "Розмір у цій картці не вказаний.", sourceRow: "Рядок знімка",
    noComposition: "Склад не вказаний у витягнутій картці.", noDescription: "Додатковий опис не вказаний.",
    tag_purpose: "призначення", tag_sport: "спорт", tag_item_type: "тип", tag_contains: "компонент", tag_shoe_size: "розмір",
    tag_form: "форма", tag_race_format: "формат", tag_distance: "дистанція",
    tag_running: "біг", tag_hiking: "походи", tag_cycling: "велоспорт", tag_general_fitness: "фітнес",
    tag_strength_training: "силові тренування", tag_gym_training: "тренування в залі", tag_yoga: "йога", tag_pilates: "пілатес",
    tag_active_recreation: "активний відпочинок", tag_crossfit: "кросфіт", tag_functional_training: "функціональні тренування",
    tag_hiit: "інтервальні тренування", tag_intense_training: "інтенсивні тренування", tag_physical_activity_general: "загальна фізична активність",
    tag_stretching: "розтягування", tag_swimming: "плавання", tag_training_general: "загальні тренування", tag_walking: "ходьба",
    tag_not_sport_specific: "без конкретного виду спорту", tag_supplement_bundle: "набір добавок", tag_snack_bundle: "набір перекусів",
    tag_equipment_bundle: "набір спорядження", tag_apparel_bundle: "набір одягу", tag_apparel: "одяг", tag_food_bundle: "набір продуктів",
    tag_gift_bundle: "подарунковий набір", tag_club_membership_bundle: "набір з участю у клубі", tag_caffeine: "кофеїн",
    tag_protein: "білок", tag_electrolytes: "електроліти", tag_magnesium: "магній", tag_creatine: "креатин",
    tag_5_htp: "5-HTP", tag_acetyl_l_carnitine: "ацетил-L-карнітин", tag_amanita: "мухомор", tag_amino_acids: "амінокислоти",
    tag_apple_cider_vinegar: "яблучний оцет", tag_arginine: "аргінін", tag_artichoke: "артишок", tag_ashwagandha: "ашваганда",
    tag_astaxanthin: "астаксантин", tag_bcaa: "BCAA", tag_beta_carotene: "бета-каротин", tag_biotin: "біотин",
    tag_boswellia: "босвелія", tag_calcium: "кальцій", tag_carbohydrate: "вуглевод", tag_carbohydrates: "вуглеводи",
    tag_cbd: "CBD", tag_choline: "холін", tag_chromium: "хром", tag_coenzyme_q10: "коензим Q10", tag_coq10: "CoQ10",
    tag_collagen: "колаген", tag_copper: "мідь", tag_cordyceps: "кордицепс", tag_curcumin: "куркумін", tag_dha: "DHA",
    tag_digestive_enzymes: "травні ферменти", tag_eaa: "EAA", tag_fiber: "клітковина", tag_folic_acid: "фолієва кислота",
    tag_gaba: "GABA", tag_ginger: "імбир", tag_ginseng: "женьшень", tag_glutamine: "глутамін", tag_green_tea_extract: "екстракт зеленого чаю",
    tag_inositol: "інозитол", tag_iron: "залізо", tag_l_carnitine: "L-карнітин", tag_lion_s_mane: "їжовик гребінчастий",
    tag_lions_mane: "їжовик гребінчастий", tag_maca: "мака", tag_melatonin: "мелатонін", tag_milk_thistle: "розторопша",
    tag_minerals: "мінерали", tag_msm: "MSM", tag_multivitamin: "мультивітамінний комплекс", tag_mushroom_complex: "комплекс грибів",
    tag_omega_3: "омега-3", tag_reishi: "рейші", tag_selenium: "селен", tag_shiitake: "шиїтаке", tag_spirulina: "спіруліна",
    tag_tribulus: "трибулус", tag_triphala: "трифала", tag_turmeric: "куркума", tag_vitamin_b: "вітамін B",
    tag_vitamin_b12: "вітамін B12", tag_vitamin_b_complex: "комплекс вітамінів B", tag_vitamin_c: "вітамін C",
    tag_vitamin_d: "вітамін D", tag_vitamin_d3: "вітамін D3", tag_vitamin_k2: "вітамін K2", tag_whey_protein: "сироватковий білок",
    tag_zinc: "цинк",
    tag_capsules: "капсули", tag_tablets: "таблетки", tag_bars: "батончики", tag_marathon: "марафон", tag_half_marathon: "напівмарафон", tag_unspecified: "не вказано",
    testOnly: "ТЕСТОВА ВЕРСІЯ · ЛОГІКУ НЕ ЗАТВЕРДЖЕНО", noSources: "Джерело не вказане"
  }
};

const state = { locale: "ru", options: null, lastRequest: null, lastResponse: null, currentStep: 0 };
const byId = (id) => document.getElementById(id);

function tr(key) {
  return copy[state.locale][key] || copy.ru[key] || key;
}

function setText(node, value) {
  node.textContent = value;
}

function applyCopy() {
  document.documentElement.lang = state.locale;
  document.querySelectorAll("[data-i18n]").forEach((node) => setText(node, tr(node.dataset.i18n)));
  document.querySelectorAll("[data-i18n-placeholder]").forEach((node) => {
    node.placeholder = tr(node.dataset.i18nPlaceholder);
  });
  byId("locale").setAttribute("aria-label", tr("languageLabel"));
  document.title = tr("title") + " · Race Expert Quiz Lab";
  if (state.options) {
    renderOptions();
    updateStep();
  }
  if (state.lastResponse) renderResponse(state.lastResponse, state.lastRequest);
}

function humanTag(value) {
  const key = "tag_" + value;
  return tr(key) === key ? value.replace(/_/g, " ") : tr(key);
}

function appendOption(select, value, label, count, keepEmpty) {
  const option = document.createElement("option");
  option.value = value;
  option.textContent = label + (count ? " · " + count : "");
  if (keepEmpty && !value) option.disabled = true;
  select.appendChild(option);
}

function renderOptions() {
  const options = state.options;
  renderGoalOptions();
  fillSelect("sport", options.sport_options, tr("anySport"), true);
  fillSelect("item-type", options.item_type_options, tr("anyType"), true);
  fillSelect("form", options.form_options, tr("anyForm"), true);
  fillSelect("race-format", options.race_format_options, tr("anyRaceFormat"), true);
  fillSelect("component", options.contains_options, tr("anyComponent"), false);
  byId("catalog-count").textContent = options.catalog_count;
  byId("snapshot-date").textContent = options.price_snapshot_date;
  const priceInput = byId("max-price");
  priceInput.placeholder = tr("budgetPlaceholder") + " · " + options.price_range_uah.min + "–" + options.price_range_uah.max;
  byId("shoe-size").placeholder = tr("shoePlaceholder") + " · " + options.shoe_size_options.join(", ");
}

function renderGoalOptions() {
  const container = byId("goal-options");
  const selected = container.querySelector('input[name="goal_group"]:checked')?.value;
  container.replaceChildren();
  state.options.goal_options.forEach(({ value }) => {
    const label = element("label", "goal-option");
    const input = document.createElement("input");
    input.type = "radio";
    input.name = "goal_group";
    input.value = value;
    input.checked = value === selected;
    const content = element("span", "goal-option-copy");
    content.append(element("strong", null, tr("goal_" + value)));
    content.append(element("small", null, tr("goalHint_" + value)));
    label.append(input, content);
    container.append(label);
  });
}

function fillSelect(id, values, placeholder, localizedTags) {
  const select = byId(id);
  const current = select.value;
  select.replaceChildren();
  appendOption(select, "", placeholder, 0, false);
  values.forEach((item) => appendOption(select, item.value, localizedTags ? humanTag(item.value) : humanTag(item.value), item.count, false));
  select.value = current;
}

function buildRequest() {
  const request = {
    goal_group: document.querySelector('input[name="goal_group"]:checked')?.value,
    result_count: Number(document.querySelector('input[name="result_count"]:checked')?.value || 3),
    locale: state.locale,
    caffeine_mode: byId("caffeine").value,
    in_stock_only: byId("in-stock").checked
  };
  if (byId("sport").value) request.sport = byId("sport").value;
  if (byId("item-type").value) request.item_type = byId("item-type").value;
  if (byId("form").value) request.form = byId("form").value;
  if (byId("race-format").value) request.race_format = byId("race-format").value;
  if (byId("component").value) request.contains = [byId("component").value];
  if (byId("max-price").value !== "") request.max_price_uah = Number(byId("max-price").value);
  if (byId("shoe-size").value !== "") request.shoe_size = Number(byId("shoe-size").value);
  return request;
}

function element(tag, className, text) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text !== undefined && text !== null) node.textContent = text;
  return node;
}

function stateValue(prefix, value) {
  const key = prefix + "_" + value;
  return tr(key) === key ? value.replace(/_/g, " ") : tr(key);
}

function renderCard(item, request) {
  const card = element("article", "result-card");
  const top = element("div", "result-card-top");
  top.append(element("span", "row-id", "№ " + item.catalog_row));
  if (item.sku) top.append(element("span", "sku", item.sku));
  card.append(top);

  card.append(element("h3", "result-title", item.title));
  const price = element("p", "price-line");
  price.append(element("strong", "price", item.price_uah.toLocaleString(state.locale === "ru" ? "ru-RU" : "uk-UA") + " ₴"));
  price.append(element("span", "price-date", tr("snapshot") + ": " + item.price_snapshot_date));
  card.append(price);

  const statusList = element("div", "status-list");
  statusList.append(element("span", "status-pill", tr("caffeineStatus") + ": " + stateValue("caffeine", item.caffeine_status)));
  statusList.append(element("span", "status-pill", tr("stockStatus") + ": " + stateValue("availability", item.availability)));
  card.append(statusList);

  const matched = Object.entries(item.matched_tags || {})
    .filter(([namespace]) => !(request.goal_group && namespace === "purpose"))
    .flatMap(([namespace, values]) => values.map((value) => humanTag(namespace) + ": " + humanTag(value)));
  if (matched.length) {
    const tags = element("div", "tag-list");
    matched.forEach((value) => tags.append(element("span", "tag", value)));
    card.append(tags);
  }

  if (item.description) {
    card.append(element("h4", null, tr("description")));
    card.append(element("p", "result-copy", item.description));
  }
  card.append(element("h4", null, tr("composition")));
  card.append(element("p", "result-copy", item.composition || tr("noComposition")));

  if (request.shoe_size && item.shoe_size_status === "unknown") {
    card.append(element("p", "data-warning", tr("sizeNotRecorded")));
  }

  if (item.reasons && item.reasons.length) {
    const reasons = element("ul", "reason-list");
    item.reasons.forEach((reason) => reasons.append(element("li", null, reason)));
    card.append(reasons);
  }
  if (item.data_notes && item.data_notes.length) {
    const notes = element("ul", "data-notes");
    item.data_notes.forEach((note) => notes.append(element("li", null, note)));
    card.append(notes);
  }

  const source = document.createElement("a");
  source.className = "source-link";
  source.href = item.source_url;
  source.target = "_blank";
  source.rel = "noopener noreferrer";
  source.textContent = tr("openSource") + " ↗";
  card.append(source);
  const cardNotice = element("p", "card-test-note", tr("testOnly"));
  card.append(cardNotice);
  return card;
}

function renderResponse(response, request) {
  const heading = byId("results-heading");
  const list = byId("results-list");
  const message = byId("results-message");
  heading.hidden = false;
  list.replaceChildren();
  const count = response.returned_count || 0;
  byId("results-title").textContent = count ? tr("matches").replace("{count}", count) : tr("noResults");
  setText(message, response.message || "");
  response.results.forEach((item) => list.append(renderCard(item, request)));
  byId("results-section").scrollIntoView({ behavior: "smooth", block: "start" });
}

async function requestRecommendations(request) {
  const error = byId("form-error");
  const button = byId("submit-button");
  const section = byId("results-section");
  error.hidden = true;
  button.disabled = true;
  section.setAttribute("aria-busy", "true");
  try {
    const response = await fetch("/api/recommend", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(request)
    });
    const payload = await response.json();
    if (!response.ok) throw new Error(payload.error || tr("requestFailed"));
    state.lastRequest = request;
    state.lastResponse = payload;
    renderResponse(payload, request);
  } catch (failure) {
    error.textContent = failure.message || tr("requestFailed");
    error.hidden = false;
  } finally {
    button.disabled = false;
    section.setAttribute("aria-busy", "false");
  }
}

function renderAnswerSummary() {
  const summary = byId("answer-summary");
  summary.replaceChildren();
  const choices = [];
  const goal = document.querySelector('input[name="goal_group"]:checked')?.value;
  if (goal) choices.push([tr("summaryGoal"), tr("goal_" + goal)]);

  for (const [id, key] of [["sport", "summarySport"], ["item-type", "summaryType"], ["form", "summaryForm"], ["race-format", "summaryRace"], ["component", "summaryComponent"]]) {
    const value = byId(id).value;
    if (value) choices.push([tr(key), humanTag(value)]);
  }
  if (byId("max-price").value !== "") choices.push([tr("summaryBudget"), Number(byId("max-price").value).toLocaleString(state.locale === "ru" ? "ru-RU" : "uk-UA") + " ₴"]);
  if (byId("shoe-size").value !== "") choices.push([tr("summaryShoe"), byId("shoe-size").value]);
  if (byId("caffeine").value === "avoid") choices.push([tr("summaryCaffeine"), tr("caffeineAvoid")]);
  if (byId("in-stock").checked) choices.push([tr("summaryStock"), "✓"]);
  const count = document.querySelector('input[name="result_count"]:checked')?.value || "3";
  choices.push([tr("summaryCount"), count]);

  choices.forEach(([label, value]) => {
    const row = element("li");
    row.append(element("strong", null, label + ": "), document.createTextNode(value));
    summary.append(row);
  });
}

function updateStep() {
  const step = state.currentStep;
  document.querySelectorAll(".quiz-step").forEach((section) => {
    section.hidden = Number(section.dataset.step) !== step;
  });
  byId("step-counter").textContent = tr("stepCounter").replace("{current}", step + 1).replace("{total}", 4);
  byId("step-name").textContent = tr("stepName" + (step + 1));
  byId("progress-track").setAttribute("aria-valuenow", String(step + 1));
  byId("progress-fill").style.width = ((step + 1) / 4 * 100) + "%";
  byId("back-button").hidden = step === 0;
  byId("next-button").hidden = step === 3;
  byId("submit-button").hidden = step !== 3;
  if (step === 3) renderAnswerSummary();
}

function goToStep(step) {
  state.currentStep = Math.max(0, Math.min(3, step));
  byId("form-error").hidden = true;
  updateStep();
  const heading = document.querySelector('.quiz-step[data-step="' + state.currentStep + '"] h2');
  heading.focus({ preventScroll: true });
  heading.scrollIntoView({ behavior: "smooth", block: "start" });
}

function validateGoal() {
  const selected = document.querySelector('input[name="goal_group"]:checked');
  if (selected) return true;
  byId("form-error").textContent = tr("goalRequired");
  byId("form-error").hidden = false;
  byId("goal-options").querySelector("input")?.focus();
  return false;
}

async function init() {
  applyCopy();
  try {
    const response = await fetch("/api/options");
    if (!response.ok) throw new Error("Options request failed");
    state.options = await response.json();
    renderOptions();
    updateStep();
  } catch (error) {
    byId("form-error").textContent = tr("requestFailed");
    byId("form-error").hidden = false;
  }

  byId("goal-options").addEventListener("change", () => {
    byId("form-error").hidden = true;
  });
  byId("next-button").addEventListener("click", () => {
    if (state.currentStep === 0 && !validateGoal()) return;
    goToStep(state.currentStep + 1);
  });
  byId("back-button").addEventListener("click", () => goToStep(state.currentStep - 1));
  byId("locale").addEventListener("change", async (event) => {
    state.locale = event.target.value;
    applyCopy();
    if (state.lastRequest) await requestRecommendations({ ...state.lastRequest, locale: state.locale });
  });
  byId("quiz-form").addEventListener("submit", (event) => {
    event.preventDefault();
    if (state.currentStep < 3) {
      if (state.currentStep === 0 && !validateGoal()) return;
      goToStep(state.currentStep + 1);
      return;
    }
    if (!validateGoal()) return;
    requestRecommendations(buildRequest());
  });
}

init();
