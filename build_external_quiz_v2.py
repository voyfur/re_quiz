import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent

CATALOG_FILE = ROOT / "test-quiz-sandbox" / "catalog.json"
CATALOG_LEN = len(json.loads(CATALOG_FILE.read_text(encoding="utf-8"))) if CATALOG_FILE.exists() else 206

CATALOG_JS = (ROOT / "test-quiz-sandbox" / "web" / "catalog_data.js").read_text(encoding="utf-8")
MATCHER_JS = (ROOT / "test-quiz-sandbox" / "web" / "client_matcher.js").read_text(encoding="utf-8")

UI_SCRIPT = """
const UI_COPY = {
  uk: {
    topNotice: "Офіційний інтерактивний підбір Race Expert · __COUNT__ готових наборів",
    goalTitle: "Для якої мети ви обираєте набір?",
    goalHint: "Оберіть вашу головну спортивну задачу. Наступні кроки підлаштуються під неї.",
    stepFirst: "Крок 1 із 5",
    stepCount: "Крок {current} із {total}",
    candidatesBadge: "{count} наборів",
    back: "Назад",
    continue: "Продовжити",
    showResults: "Підібрати набори",
    restart: "Змінити відповіді",
    any: "Не має значення",
    budgetPrompt: "Яка максимальна вартість усього набору?",
    budgetHint: "Підходящі набори за вашими критеріями: від {min} до {max} ₴. Залиште порожнім, якщо без обмежень.",
    budgetPlaceholder: "Наприклад: {min}",
    sizeHint: "У цій категорії зустрічаються розміри: {sizes}.",
    errorRequired: "Будь ласка, оберіть варіант для продовження.",
    goal_running: "Біг і підготовка до стартів",
    goal_training: "Силові тренування та м'язи",
    goal_hydration: "Гідратація та електроліти",
    goal_food: "Спортивні перекуси та енергія",
    goal_recovery: "Відновлення та сон",
    goal_outdoors: "Походи та кемпінг",
    goal_gear: "Одяг та аксесуари",
    goal_daily: "Щоденна підтримка та вітаміни",
    goal_gift: "Подарунковий набір",
    question_activity: "Який саме вид активності планується?",
    question_component_class: "Який ключовий тип товару має бути в наборі?",
    question_membership: "Потрібен набір з клубним абонементом Race Expert Club?",
    question_use_scenario: "Який сценарій використання ближчий до вашого?",
    question_use_timing: "Коли плануєте вживати або використовувати продукцію?",
    question_use_place: "Де найчастіше будете використовувати набір?",
    question_race_format: "До якого формату старту готуєтесь?",
    question_season: "Для яких погодних умов підбираєте спорядження?",
    question_product_form: "Яка форма продукту найбільш зручна?",
    question_shoe_size: "Який розмір взуття чи шкарпеток потрібен?",
    question_budget: "Яка максимальна вартість усього набору?",
    activity_running: "Біг (шосе, трейл)",
    activity_strength_training: "Силові тренування у залі",
    activity_functional_training: "Функціональний тренінг / Crossfit",
    activity_cycling: "Велоспорт",
    activity_hiking: "Походи та трекінг",
    activity_swimming: "Плавання",
    activity_mind_body_mobility: "Йога, пілатес і розтяжка",
    activity_walking: "Ходьба / активні прогулянки",
    activity_general_fitness: "Загальний фітнес",
    activity_other: "Інший вид активності",
    class_protein_carbohydrate_food: "Спортивне харчування та батончики",
    class_supplements_vitamins_minerals: "Вітаміни та щоденні мінерали",
    class_creatine_preworkout: "Креатин та передтренувальні комплекси",
    class_sports_accessories: "Спортивні аксесуари та пляшки",
    class_apparel_footwear: "Одяг, шкарпетки та кепки",
    class_hydration_items: "Ізотоніки та електроліти",
    class_dehydrated_meal: "Сублімована їжа для походів",
    scenario_event_preparation: "Підготовка до забігу чи змагань",
    scenario_training: "Регулярні тренувальні тижні",
    scenario_everyday: "На кожен день для тонусу",
    membership_yes: "Так, обов'язково з абонементом клубу",
    membership_no: "Ні, лише товари без абонемента",
    race_half_marathon: "Напівмарафон (21.1 км)",
    race_marathon: "Марафон (42.2 км)",
    race_race_or_event_preparation: "Короткі або клубні забіги (5–10 км)",
    race_ultra_or_long_distance: "Ультрамарафон або тривалий трейл",
    season_cold: "Холодна погода / осінь-зима",
    season_warm: "Тепла погода / спека-літо",
    form_bars: "Батончики",
    form_food_or_meal: "Готова їжа / снеки",
    form_gel: "Енергетичні гелі",
    form_liquid: "Рідкі форми / шоти",
    form_sticks: "Стики з порошком",
    form_capsules: "Капсули",
    form_powder: "Порошок у банках чи пакетах",
    form_softgels: "М'які капсули (Omega, D3)",
    form_tablets: "Таблетки",
    form_apparel: "Текстиль / шкарпетки / одяг",
    cardPrice: "Вартість за знімком:",
    openCardBtn: "Переглянути набір на сайті Race Expert →"
  },
  ru: {
    topNotice: "Официальный интерактивный подбор Race Expert · __COUNT__ готовых наборов",
    goalTitle: "Для какой цели вы подбираете набор?",
    goalHint: "Выберите главную спортивную задачу. Последующие шаги настроятся под неё.",
    stepFirst: "Шаг 1 из 5",
    stepCount: "Шаг {current} из {total}",
    candidatesBadge: "{count} наборов",
    back: "Назад",
    continue: "Продолжить",
    showResults: "Подобрать наборы",
    restart: "Изменить ответы",
    any: "Не имеет значения",
    budgetPrompt: "Какова максимальная стоимость всего набора?",
    budgetHint: "Подходящие наборы по вашим критериям: от {min} до {max} ₴. Оставьте пустым, если без ограничений.",
    budgetPlaceholder: "Например: {min}",
    sizeHint: "В этой категории встречаются размеры: {sizes}.",
    errorRequired: "Пожалуйста, выберите вариант для продолжения.",
    goal_running: "Бег и подготовка к стартам",
    goal_training: "Силовые тренировки и масса",
    goal_hydration: "Гидратация и электролиты",
    goal_food: "Спортивные перекусы и энергия",
    goal_recovery: "Восстановление и сон",
    goal_outdoors: "Походы и кемпинг",
    goal_gear: "Одежда и аксессуары",
    goal_daily: "Ежедневная поддержка и витамины",
    goal_gift: "Подарочный набор",
    question_activity: "Какой именно вид активности планируется?",
    question_component_class: "Какой ключевой тип товара должен быть в наборе?",
    question_membership: "Нужен набор с клубным абонементом Race Expert Club?",
    question_use_scenario: "Какой сценарий использования ближе к вашей ситуации?",
    question_use_timing: "Когда планируете употреблять или использовать продукцию?",
    question_use_place: "Где чаще всего будете использовать набор?",
    question_race_format: "К какому формату старта готовитесь?",
    question_season: "Для каких погодных условий подбираете экипировку?",
    question_product_form: "Какая форма продукта наиболее удобна?",
    question_shoe_size: "Какой размер обуви или носков нужен?",
    question_budget: "Какова максимальная цена всего набора?",
    activity_running: "Бег (шоссе, трейл)",
    activity_strength_training: "Силовые тренировки в зале",
    activity_functional_training: "Функциональный тренинг / Crossfit",
    activity_cycling: "Велоспорт",
    activity_hiking: "Походы и треккинг",
    activity_swimming: "Плавание",
    activity_mind_body_mobility: "Йога, пилатес и растяжка",
    activity_walking: "Ходьба / активные прогулки",
    activity_general_fitness: "Общий фитнес",
    activity_other: "Другой вид активности",
    class_protein_carbohydrate_food: "Спортивное питание и батончики",
    class_supplements_vitamins_minerals: "Витамины и минералы",
    class_creatine_preworkout: "Креатин и предтренировочные комплексы",
    class_sports_accessories: "Спортивные аксессуары и бутылки",
    class_apparel_footwear: "Одежда, носки и кепки",
    class_hydration_items: "Изотоники и электролиты",
    class_dehydrated_meal: "Сублимированная еда для походов",
    scenario_event_preparation: "Подготовка к забегу или стартам",
    scenario_training: "Регулярные тренировочные недели",
    scenario_everyday: "На каждый день для тонуса",
    membership_yes: "Да, обязательно с абонементом клуба",
    membership_no: "Нет, только товары без абонемента",
    race_half_marathon: "Полумарафон (21.1 км)",
    race_marathon: "Марафон (42.2 км)",
    race_race_or_event_preparation: "Короткие или клубные старты (5–10 км)",
    race_ultra_or_long_distance: "Ультрамарафон или длительный трейл",
    season_cold: "Холодная погода / осень-зима",
    season_warm: "Тёплая погода / жара-лето",
    form_bars: "Батончики",
    form_food_or_meal: "Готовая еда / снеки",
    form_gel: "Энергетические гели",
    form_liquid: "Жидкие формы / шоты",
    form_sticks: "Стики с порошком",
    form_capsules: "Капсулы",
    form_powder: "Порошок в банках или пакетах",
    form_softgels: "Мягкие капсулы (Omega, D3)",
    form_tablets: "Таблетки",
    form_apparel: "Текстиль / носки / одежда",
    cardPrice: "Цена по снимку:",
    openCardBtn: "Перейти к набору на сайте Race Expert →"
  }
};

const appState = {
  locale: "uk",
  goal: "",
  answers: {},
  history: [],
  currentQuestionId: "goal",
  questionPlan: [],
  optionsData: null,
  catalog: window.QUIZ_CATALOG || []
};

function tr(key, vars = {}) {
  let str = UI_COPY[appState.locale]?.[key] || UI_COPY.uk?.[key] || key;
  Object.entries(vars).forEach(([k, v]) => {
    str = str.replaceAll("{" + k + "}", v);
  });
  return str;
}

function optionLabel(qId, val) {
  if (val === "any") return tr("any");
  const prefixes = {
    activity: "activity_",
    component_class: "class_",
    membership: "membership_",
    use_scenario: "scenario_",
    race_format: "race_",
    season: "season_",
    product_form: "form_"
  };
  const p = prefixes[qId] || "";
  return tr(p + val);
}

function renderScreen() {
  const isGoal = appState.currentQuestionId === "goal";
  const plan = appState.questionPlan;
  const q = isGoal
    ? { id: "goal", type: "single", options: ["running", "training", "hydration", "food", "recovery", "outdoors", "gear", "daily", "gift"] }
    : plan.find(item => item.id === appState.currentQuestionId);

  if (!q) return;

  const totalSteps = Math.max(appState.history.length + plan.length, 2);
  const curStep = appState.history.length + 1;
  document.getElementById("stepCounterLabel").textContent = isGoal
    ? tr("stepFirst")
    : tr("stepCount", { current: curStep, total: totalSteps });

  const pct = Math.min(100, Math.round((curStep / totalSteps) * 100));
  document.getElementById("progressFill").style.width = pct + "%";

  const candCount = appState.optionsData?.candidate_count ?? __COUNT__;
  document.getElementById("activePoolBadge").textContent = tr("candidatesBadge", { count: candCount });

  document.getElementById("questionHeading").textContent = isGoal ? tr("goalTitle") : tr(q.title_key);
  document.getElementById("questionSubtitle").textContent = isGoal ? tr("goalHint") : "";
  document.getElementById("errorAlert").classList.add("hidden");

  const optionsBox = document.getElementById("optionsContainer");
  const numBox = document.getElementById("numberContainer");
  optionsBox.innerHTML = "";

  if (q.type === "number") {
    optionsBox.classList.add("hidden");
    numBox.classList.remove("hidden");
    const inp = document.getElementById("numericField");
    const lbl = document.getElementById("numberPrompt");
    const detailedHint = document.getElementById("numberDetailedHint");
    const curr = document.getElementById("currencySymbol");

    lbl.textContent = tr(q.title_key);
    inp.value = appState.answers[q.id] || "";

    if (q.id === "max_price_uah") {
      curr.classList.remove("hidden");
      const dMin = q.dynamic_min ?? 600;
      const dMax = q.dynamic_max ?? 4500;
      inp.placeholder = tr("budgetPlaceholder", { min: dMin.toLocaleString() });
      detailedHint.textContent = tr("budgetHint", { min: dMin.toLocaleString(), max: dMax.toLocaleString() });
    } else if (q.id === "shoe_size") {
      curr.classList.add("hidden");
      inp.placeholder = "42";
      detailedHint.textContent = q.ranges ? tr("sizeHint", { sizes: q.ranges.join(", ") }) : "";
    }
  } else {
    numBox.classList.add("hidden");
    optionsBox.classList.remove("hidden");
    const opts = isGoal
      ? ["running", "training", "hydration", "food", "recovery", "outdoors", "gear", "daily", "gift"]
      : ["any", ...q.options];

    const selectedVal = isGoal ? appState.goal : appState.answers[q.id];

    opts.forEach(val => {
      const btn = document.createElement("button");
      btn.type = "button";
      const isSelected = selectedVal === val;
      btn.className = "p-4 rounded-xl border-2 text-left font-medium transition flex items-center justify-between text-sm sm:text-base " + (
        isSelected
          ? "bg-brand-500/15 border-brand-500 text-white ring-2 ring-brand-500/30"
          : "bg-slate-950/80 border-slate-800 text-slate-200 hover:border-slate-700 hover:bg-slate-800/50"
      );

      const text = isGoal ? tr("goal_" + val) : optionLabel(q.id, val);
      btn.innerHTML = '<span class="pr-2 leading-snug">' + text + '</span>' + (isSelected ? '<span class="text-brand-500 font-bold text-lg">✓</span>' : '');

      btn.onclick = () => {
        if (isGoal) {
          appState.goal = val;
        } else {
          appState.answers[q.id] = val;
        }
        renderScreen();
      };
      optionsBox.appendChild(btn);
    });
  }

  const isBudget = q.id === "max_price_uah";
  document.getElementById("btnBack").classList.toggle("hidden", appState.history.length === 0);
  document.getElementById("btnNext").classList.toggle("hidden", isBudget);
  document.getElementById("btnShowResults").classList.toggle("hidden", !isBudget);
}

function advanceStep() {
  const isGoal = appState.currentQuestionId === "goal";
  if (isGoal) {
    if (!appState.goal) {
      showErrorMessage(tr("errorRequired"));
      return;
    }
    appState.history.push("goal");
    updateEnginePlan();
    if (appState.questionPlan.length === 0) {
      renderFinalResults();
      return;
    }
    appState.currentQuestionId = appState.questionPlan[0].id;
    renderScreen();
    return;
  }

  const q = appState.questionPlan.find(item => item.id === appState.currentQuestionId);
  if (!q) return;

  if (q.type === "number") {
    const raw = document.getElementById("numericField").value.trim();
    appState.answers[q.id] = raw === "" ? "any" : Number(raw);
  }

  const currentVal = appState.answers[q.id];
  if (currentVal === undefined) {
    showErrorMessage(tr("errorRequired"));
    return;
  }

  appState.history.push(q.id);
  updateEnginePlan();

  const nextQ = appState.questionPlan.find(item => !appState.history.includes(item.id));
  if (!nextQ) {
    renderFinalResults();
    return;
  }
  appState.currentQuestionId = nextQ.id;
  renderScreen();
}

function goBackStep() {
  if (appState.history.length === 0) return;
  const prevId = appState.history.pop();
  if (prevId === "goal") {
    appState.goal = "";
    appState.answers = {};
    appState.questionPlan = [];
    appState.currentQuestionId = "goal";
  } else {
    delete appState.answers[prevId];
    appState.currentQuestionId = prevId;
    updateEnginePlan();
  }
  renderScreen();
}

function updateEnginePlan() {
  if (!appState.goal) {
    appState.optionsData = window.QUIZ_MATCHER.draftOptions(appState.catalog);
    appState.questionPlan = [];
    return;
  }
  appState.optionsData = window.QUIZ_MATCHER.draftOptions(appState.catalog, appState.goal, appState.answers);
  appState.questionPlan = appState.optionsData.question_plan || [];
}

function showErrorMessage(msg) {
  const alert = document.getElementById("errorAlert");
  document.getElementById("errorMessage").textContent = msg;
  alert.classList.remove("hidden");
}

function createKitCard(item, badgeType = "match") {
  const card = document.createElement("article");
  card.className = "p-5 rounded-2xl border border-slate-800 bg-slate-950/70 space-y-3.5 hover:border-slate-700 transition relative overflow-hidden";

  let badgeHtml = "";
  if (badgeType === "near_miss") {
    badgeHtml = '<span class="px-2.5 py-1 rounded-md text-xs font-bold bg-amber-500/20 text-amber-300 border border-amber-500/30">+' + item.price_over_budget_uah + ' ₴ до бюджету</span>';
  } else if (badgeType === "floor_anchor") {
    badgeHtml = '<span class="px-2.5 py-1 rounded-md text-xs font-bold bg-purple-500/20 text-purple-300 border border-purple-500/30">Базовий старт</span>';
  } else if (item.match_score_pct) {
    const color = item.match_score_pct >= 85 ? "bg-emerald-500/20 text-emerald-300 border-emerald-500/30" : "bg-blue-500/20 text-blue-300 border-blue-500/30";
    badgeHtml = '<span class="px-2.5 py-1 rounded-md text-xs font-bold ' + color + ' border">' + item.match_score_pct + '% відповідність</span>';
  }

  const topRow = '<div class="flex items-center justify-between gap-2">' +
    '<span class="text-xs font-mono text-slate-500">№ ' + item.catalog_row + ' · ' + (item.sku || 'RE-KIT') + '</span>' +
    '<div class="flex items-center gap-2">' + badgeHtml + '</div>' +
    '</div>';

  const title = '<h3 class="text-lg font-bold text-white tracking-tight leading-snug">' + item.title + '</h3>';

  const priceBlock = '<div class="flex items-baseline gap-2 pt-0.5">' +
    '<span class="text-2xl font-bold font-mono text-brand-500">' + item.price_uah.toLocaleString() + ' ₴</span>' +
    '<span class="text-xs text-slate-500">' + tr("cardPrice") + ' ' + item.price_snapshot_date + '</span>' +
    '</div>';

  const reasons = (item.reasons || []).map(r => '<li class="flex items-start gap-2 text-xs sm:text-sm text-slate-300"><span class="text-emerald-400 font-bold shrink-0">✓</span><span>' + r + '</span></li>').join("");
  const reasonsBlock = reasons ? '<ul class="space-y-1.5 pt-2 border-t border-slate-900">' + reasons + '</ul>' : "";

  const notes = (item.data_notes || []).filter(n => !n.includes("Ціна й наявність") && !n.includes("Цена и наличие")).map(n => '<p class="text-xs text-amber-300/80 italic">⚠️ ' + n + '</p>').join("");

  const cta = '<div class="pt-3">' +
    '<a href="' + item.source_url + '" target="_blank" rel="noopener noreferrer" class="inline-flex items-center gap-2 px-4 py-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-xs sm:text-sm font-bold text-white transition">' +
    '<span>' + tr("openCardBtn") + '</span>' +
    '</a></div>';

  card.innerHTML = topRow + title + priceBlock + reasonsBlock + notes + cta;
  return card;
}

function renderFinalResults() {
  const req = {
    goal_group: appState.goal,
    locale: appState.locale,
    ...appState.answers
  };
  if (req.max_price_uah === "any") delete req.max_price_uah;
  if (req.shoe_size === "any") delete req.shoe_size;

  const res = window.QUIZ_MATCHER.draftRecommend(appState.catalog, req);

  document.getElementById("quizQuestionView").classList.add("hidden");
  document.getElementById("progressSection").classList.add("hidden");
  document.getElementById("quizResultsView").classList.remove("hidden");

  document.getElementById("resultsTitle").textContent = res.results.length > 0
    ? ("Знайдено наборів: " + res.returned_count)
    : "Підходящих наборів не знайдено";

  document.getElementById("resultMessageBanner").textContent = res.message;

  const cardsBox = document.getElementById("primaryCardsList");
  cardsBox.innerHTML = "";
  res.results.forEach(item => cardsBox.appendChild(createKitCard(item, "match")));

  const nearSec = document.getElementById("nearMissSection");
  const nearBox = document.getElementById("nearMissCardsList");
  nearBox.innerHTML = "";
  if (res.near_miss_results && res.near_miss_results.length > 0) {
    nearSec.classList.remove("hidden");
    res.near_miss_results.forEach(item => nearBox.appendChild(createKitCard(item, "near_miss")));
  } else {
    nearSec.classList.add("hidden");
  }

  const floorSec = document.getElementById("floorAnchorSection");
  const floorBox = document.getElementById("floorAnchorCardsList");
  floorBox.innerHTML = "";
  if (res.floor_anchor_results && res.floor_anchor_results.length > 0) {
    floorSec.classList.remove("hidden");
    res.floor_anchor_results.forEach(item => floorBox.appendChild(createKitCard(item, "floor_anchor")));
  } else {
    floorSec.classList.add("hidden");
  }
}

// 8-Directional Resizing Controller
function initResize() {
  const widget = document.getElementById("resizableWidget");
  if (!widget) return;

  const handles = widget.querySelectorAll(".resize-handle");
  let isResizing = false;
  let currentDirection = "";
  let startX = 0, startY = 0;
  let startWidth = 0, startHeight = 0;
  let startLeft = 0, startTop = 0;

  handles.forEach(handle => {
    handle.addEventListener("pointerdown", (e) => {
      e.preventDefault();
      e.stopPropagation();
      isResizing = true;
      currentDirection = handle.dataset.direction;
      startX = e.clientX;
      startY = e.clientY;

      const rect = widget.getBoundingClientRect();
      startWidth = rect.width;
      startHeight = rect.height;

      widget.classList.add("select-none");
      document.body.classList.add("select-none");
      handle.setPointerCapture(e.pointerId);

      const onPointerMove = (ev) => {
        if (!isResizing) return;
        const dx = ev.clientX - startX;
        const dy = ev.clientY - startY;

        let newWidth = startWidth;
        let newHeight = startHeight;

        // Horizontal dragging
        if (currentDirection.includes("e")) { // right
          newWidth = startWidth + dx;
        } else if (currentDirection.includes("w")) { // left
          newWidth = startWidth - dx;
        }

        // Vertical dragging
        if (currentDirection.includes("s")) { // bottom
          newHeight = startHeight + dy;
        } else if (currentDirection.includes("n")) { // top
          newHeight = startHeight - dy;
        }

        // Apply boundaries
        const minW = 340;
        const maxW = Math.min(window.innerWidth - 32, 1600);
        const minH = 400;

        if (newWidth >= minW && newWidth <= maxW) {
          widget.style.width = newWidth + "px";
          widget.style.maxWidth = "none";
        }
        if (newHeight >= minH) {
          widget.style.minHeight = newHeight + "px";
        }
      };

      const onPointerUp = (ev) => {
        isResizing = false;
        widget.classList.remove("select-none");
        document.body.classList.remove("select-none");
        handle.releasePointerCapture(ev.pointerId);
        window.removeEventListener("pointermove", onPointerMove);
        window.removeEventListener("pointerup", onPointerUp);
      };

      window.addEventListener("pointermove", onPointerMove);
      window.addEventListener("pointerup", onPointerUp);
    });
  });

  // Size Presets
  const btnPresetSm = document.getElementById("btnPresetSm");
  const btnPresetMd = document.getElementById("btnPresetMd");
  const btnPresetLg = document.getElementById("btnPresetLg");

  if (btnPresetSm) btnPresetSm.onclick = () => {
    widget.style.width = "480px";
    widget.style.minHeight = "auto";
  };
  if (btnPresetMd) btnPresetMd.onclick = () => {
    widget.style.width = "768px";
    widget.style.minHeight = "auto";
  };
  if (btnPresetLg) btnPresetLg.onclick = () => {
    widget.style.width = "1080px";
    widget.style.minHeight = "auto";
  };
}

// Bindings
document.getElementById("btnNext").onclick = advanceStep;
document.getElementById("btnShowResults").onclick = advanceStep;
document.getElementById("btnBack").onclick = goBackStep;

document.getElementById("btnRestart").onclick = () => {
  appState.goal = "";
  appState.answers = {};
  appState.history = [];
  appState.currentQuestionId = "goal";
  updateEnginePlan();
  document.getElementById("quizResultsView").classList.add("hidden");
  document.getElementById("progressSection").classList.remove("hidden");
  document.getElementById("quizQuestionView").classList.remove("hidden");
  renderScreen();
};

document.getElementById("btnUk").onclick = () => {
  appState.locale = "uk";
  document.getElementById("btnUk").className = "px-2.5 py-1 rounded-md bg-brand-500 text-white transition shadow-sm";
  document.getElementById("btnRu").className = "px-2.5 py-1 rounded-md text-slate-400 hover:text-white transition";
  renderScreen();
};

document.getElementById("btnRu").onclick = () => {
  appState.locale = "ru";
  document.getElementById("btnRu").className = "px-2.5 py-1 rounded-md bg-brand-500 text-white transition shadow-sm";
  document.getElementById("btnUk").className = "px-2.5 py-1 rounded-md text-slate-400 hover:text-white transition";
  renderScreen();
};

updateEnginePlan();
renderScreen();
initResize();
"""

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="uk" class="dark">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <title>Race Expert Quiz</title>
  <meta name="description" content="Race Expert Quiz — інтерактивний помічник з підбору готових спортивних комплектів та харчування">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Space+Grotesk:wght@600;700&display=swap" rel="stylesheet">
  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    tailwind.config = {
      darkMode: 'class',
      theme: {
        extend: {
          colors: {
            brand: {
              50: '#fff7ed',
              100: '#ffedd5',
              500: '#f97316',
              600: '#ea580c',
              700: '#c2410c'
            },
            slate: {
              850: '#141e33',
              900: '#0b1120',
              950: '#060a12'
            }
          },
          fontFamily: {
            sans: ['"Plus Jakarta Sans"', 'system-ui', 'sans-serif'],
            display: ['"Space Grotesk"', 'sans-serif']
          }
        }
      }
    };
  </script>
  <style>
    body {
      font-feature-settings: "cv02", "cv03", "cv04", "cv11";
      -webkit-tap-highlight-color: transparent;
    }
    .glow-brand {
      box-shadow: 0 0 50px -10px rgba(249, 115, 22, 0.18);
    }
    .resize-handle {
      position: absolute;
      touch-action: none;
      z-index: 30;
    }
    .handle-e { right: 0; top: 12px; bottom: 12px; width: 10px; cursor: ew-resize; }
    .handle-w { left: 0; top: 12px; bottom: 12px; width: 10px; cursor: ew-resize; }
    .handle-s { bottom: 0; left: 12px; right: 12px; height: 10px; cursor: ns-resize; }
    .handle-n { top: 0; left: 12px; right: 12px; height: 10px; cursor: ns-resize; }
    
    .handle-se { right: 0; bottom: 0; width: 22px; height: 22px; cursor: nwse-resize; }
    .handle-sw { left: 0; bottom: 0; width: 22px; height: 22px; cursor: nesw-resize; }
    .handle-ne { right: 0; top: 0; width: 22px; height: 22px; cursor: nesw-resize; }
    .handle-nw { left: 0; top: 0; width: 22px; height: 22px; cursor: nwse-resize; }

    .corner-grip {
      position: absolute;
      right: 4px;
      bottom: 4px;
      width: 14px;
      height: 14px;
      pointer-events: none;
      background-image: radial-gradient(circle, #f97316 1.5px, transparent 1.5px);
      background-size: 5px 5px;
      opacity: 0.8;
    }
  </style>
</head>
<body class="bg-slate-950 text-slate-100 min-h-screen flex flex-col font-sans antialiased selection:bg-brand-500 selection:text-white">

  <!-- Top Announcement Bar -->
  <aside class="bg-gradient-to-r from-brand-600 via-orange-600 to-amber-600 py-1.5 px-4 text-center text-xs font-semibold text-white tracking-wide">
    <span class="inline-flex items-center gap-1.5">
      <span class="w-1.5 h-1.5 rounded-full bg-white animate-pulse"></span>
      <span id="topNotice">Офіційний інтерактивний підбір Race Expert · __COUNT__ готових наборів</span>
    </span>
  </aside>

  <!-- Navigation Bar -->
  <header class="border-b border-slate-800/80 bg-slate-900/80 backdrop-blur-md sticky top-0 z-40">
    <div class="max-w-6xl mx-auto px-4 h-16 flex items-center justify-between">
      <div class="flex items-center gap-3">
        <div class="w-10 h-10 rounded-xl bg-gradient-to-br from-brand-500 to-amber-600 flex items-center justify-center font-display font-bold text-xl text-white shadow-lg shadow-brand-500/25">
          R
        </div>
        <div>
          <span class="font-display font-bold tracking-tight text-lg text-white block leading-tight">Race Expert Quiz</span>
          <span class="text-[11px] text-slate-400 font-medium block">Інтерактивний підбір наборів</span>
        </div>
      </div>

      <!-- Quick Size Adjuster & Language Toggle -->
      <div class="flex items-center gap-3">
        <div class="hidden sm:inline-flex items-center bg-slate-800/80 rounded-lg p-0.5 border border-slate-700/60 text-xs text-slate-400">
          <span class="px-2 text-[10px] uppercase font-bold tracking-wider text-slate-500">Розмір:</span>
          <button id="btnPresetSm" type="button" class="px-2 py-0.5 rounded hover:text-white hover:bg-slate-700 transition">S</button>
          <button id="btnPresetMd" type="button" class="px-2 py-0.5 rounded hover:text-white hover:bg-slate-700 transition">M</button>
          <button id="btnPresetLg" type="button" class="px-2 py-0.5 rounded hover:text-white hover:bg-slate-700 transition">L</button>
        </div>

        <div class="inline-flex items-center bg-slate-800/80 rounded-lg p-0.5 border border-slate-700/60 text-xs font-semibold">
          <button id="btnUk" type="button" class="px-2.5 py-1 rounded-md bg-brand-500 text-white transition shadow-sm">УКР</button>
          <button id="btnRu" type="button" class="px-2.5 py-1 rounded-md text-slate-400 hover:text-white transition">РУС</button>
        </div>
        <span class="hidden md:inline-block px-2.5 py-1 text-[11px] font-semibold uppercase tracking-wider rounded-md bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
          Live __COUNT__ Kits
        </span>
      </div>
    </div>
  </header>

  <!-- Main Container -->
  <main class="flex-1 w-full px-4 py-6 md:py-10 flex flex-col items-center justify-center">

    <!-- Resizable Widget Wrapper -->
    <div id="resizableWidget" style="width: min(780px, 100%);" class="bg-slate-900/90 border-2 border-slate-800 rounded-3xl p-6 sm:p-8 md:p-10 glow-brand shadow-2xl relative transition-shadow">

      <!-- 8-Directional Drag Handles (Resize Everywhere) -->
      <div class="resize-handle handle-e" data-direction="e" title="Тягнути вправо"></div>
      <div class="resize-handle handle-w" data-direction="w" title="Тягнути вліво"></div>
      <div class="resize-handle handle-s" data-direction="s" title="Тягнути вниз"></div>
      <div class="resize-handle handle-n" data-direction="n" title="Тягнути вгору"></div>
      <div class="resize-handle handle-se" data-direction="se" title="Тягнути по діагоналі"><div class="corner-grip"></div></div>
      <div class="resize-handle handle-sw" data-direction="sw" title="Тягнути по діагоналі"></div>
      <div class="resize-handle handle-ne" data-direction="ne" title="Тягнути по діагоналі"></div>
      <div class="resize-handle handle-nw" data-direction="nw" title="Тягнути по діагоналі"></div>

      <!-- Resizing Hint Badge -->
      <div class="absolute -top-3 right-6 bg-slate-800 text-[10px] font-semibold text-slate-400 px-2 py-0.5 rounded-full border border-slate-700/80 shadow pointer-events-none flex items-center gap-1">
        <span>↔</span> <span>Тягніть за будь-який край або кут для зміни розміру</span>
      </div>

      <!-- Progress Tracking Bar -->
      <div class="mb-8" id="progressSection">
        <div class="flex items-center justify-between text-xs font-semibold uppercase tracking-wider mb-2.5">
          <span id="stepCounterLabel" class="text-brand-500">Питання 1</span>
          <span id="activePoolBadge" class="text-slate-400 bg-slate-800/60 px-2.5 py-0.5 rounded-full border border-slate-700/50">__COUNT__ варіантів</span>
        </div>
        <div class="w-full h-2 bg-slate-800 rounded-full overflow-hidden p-0.5">
          <div id="progressFill" class="h-full bg-gradient-to-r from-brand-600 to-amber-500 rounded-full transition-all duration-300 w-1/8"></div>
        </div>
      </div>

      <!-- Question Step View -->
      <div id="quizQuestionView">
        <h1 id="questionHeading" class="text-2xl sm:text-3xl font-display font-bold text-white tracking-tight mb-2"></h1>
        <p id="questionSubtitle" class="text-sm text-slate-400 mb-6 leading-relaxed"></p>

        <!-- Dynamic Options Grid -->
        <div id="optionsContainer" class="grid grid-cols-1 sm:grid-cols-2 gap-3 mb-8"></div>

        <!-- Numeric / Budget Input View -->
        <div id="numberContainer" class="mb-8 hidden space-y-3">
          <label id="numberPrompt" class="block text-sm font-medium text-slate-300"></label>
          <div class="relative max-w-md">
            <input id="numericField" type="number" step="1" inputmode="numeric" class="w-full bg-slate-950 border-2 border-slate-700 focus:border-brand-500 rounded-xl px-4 py-3.5 text-lg text-white font-mono focus:outline-none focus:ring-4 focus:ring-brand-500/20 transition">
            <span id="currencySymbol" class="absolute right-4 top-3.5 text-base font-bold text-slate-400">₴</span>
          </div>
          <div id="budgetHintCard" class="p-3.5 rounded-xl bg-brand-500/10 border border-brand-500/20 text-xs text-orange-200 flex items-start gap-2.5">
            <span class="text-brand-500 font-bold text-sm">💡</span>
            <span id="numberDetailedHint" class="leading-relaxed"></span>
          </div>
        </div>

        <!-- Error Banner -->
        <div id="errorAlert" class="p-3.5 rounded-xl bg-red-500/10 border border-red-500/30 text-xs text-red-300 mb-6 hidden flex items-center gap-2">
          <span>⚠️</span>
          <span id="errorMessage"></span>
        </div>

        <!-- Navigation Buttons -->
        <div class="pt-6 border-t border-slate-800/80 flex items-center justify-between gap-4">
          <button id="btnBack" type="button" class="px-4 py-2.5 rounded-xl border border-slate-700 hover:border-slate-600 text-sm font-semibold text-slate-300 hover:text-white transition hidden flex items-center gap-1.5">
            <span>←</span> <span id="lblBack">Назад</span>
          </button>
          <div class="ml-auto flex items-center gap-3">
            <button id="btnNext" type="button" class="px-6 py-3 rounded-xl bg-brand-500 hover:bg-brand-600 text-sm font-bold text-white transition shadow-lg shadow-brand-500/25 flex items-center gap-2">
              <span id="lblNext">Продовжити</span> <span>→</span>
            </button>
            <button id="btnShowResults" type="button" class="px-7 py-3 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-sm font-bold text-white transition shadow-lg shadow-emerald-600/25 hidden flex items-center gap-2">
              <span id="lblShowResults">Підібрати набори</span> <span>✨</span>
            </button>
          </div>
        </div>
      </div>

      <!-- Results View -->
      <div id="quizResultsView" class="hidden space-y-6">
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-5 border-b border-slate-800">
          <div>
            <span class="text-xs font-bold uppercase tracking-wider text-emerald-400 block mb-1">Підбір завершено</span>
            <h2 id="resultsTitle" class="text-2xl font-display font-bold text-white tracking-tight"></h2>
          </div>
          <button id="btnRestart" type="button" class="self-start sm:self-auto px-4 py-2 rounded-xl border border-slate-700 hover:border-slate-600 text-xs font-semibold text-slate-300 hover:text-white transition flex items-center gap-1.5">
            <span>🔄</span> <span id="lblRestart">Змінити відповіді</span>
          </button>
        </div>

        <!-- Result Explanation Banner -->
        <div id="resultMessageBanner" class="p-4 rounded-xl bg-slate-950/80 border border-slate-800 text-xs sm:text-sm text-slate-300 leading-relaxed"></div>

        <!-- Primary Cards Grid -->
        <div id="primaryCardsList" class="space-y-4"></div>

        <!-- Near-Miss Section (Budget Alternatives) -->
        <section id="nearMissSection" class="pt-6 border-t border-slate-800/80 space-y-3 hidden">
          <div class="flex items-center gap-2">
            <span class="text-amber-400 text-base">⚡</span>
            <h3 class="text-xs font-bold uppercase tracking-wider text-amber-400">Близько за бюджетом (рекомендовані альтернативи)</h3>
          </div>
          <div id="nearMissCardsList" class="space-y-4"></div>
        </section>

        <!-- Floor Anchor Section (Baseline Minimum) -->
        <section id="floorAnchorSection" class="pt-6 border-t border-slate-800/80 space-y-3 hidden">
          <div class="flex items-center gap-2">
            <span class="text-purple-400 text-base">🛡️</span>
            <h3 class="text-xs font-bold uppercase tracking-wider text-purple-400">Базовий стартовий набір у цій категорії</h3>
          </div>
          <div id="floorAnchorCardsList" class="space-y-4"></div>
        </section>
      </div>

    </div>

  </main>

  <!-- Footer -->
  <footer class="border-t border-slate-900 bg-slate-950/80 py-6 text-center text-xs text-slate-500">
    <p>Race Expert · Офіційний каталог __COUNT__ готових наборів «За потребами»</p>
    <p class="mt-1 text-[11px] text-slate-600">Ціни та наявність наведено на дату локального знімка каталогу</p>
  </footer>

  <!-- Scripts -->
  <script>
__CATALOG_DATA__
  </script>
  <script>
__MATCHER_DATA__
  </script>
  <script>
__UI_SCRIPT__
  </script>
</body>
</html>
"""

final_html = (
    HTML_TEMPLATE
    .replace("__CATALOG_DATA__", CATALOG_JS)
    .replace("__MATCHER_DATA__", MATCHER_JS)
    .replace("__UI_SCRIPT__", UI_SCRIPT)
    .replace("__COUNT__", str(CATALOG_LEN))
)

(ROOT / "public" / "index.html").write_text(final_html, encoding="utf-8")
(ROOT / "quiz.html").write_text(final_html, encoding="utf-8")
print(f"Generated standalone public/index.html ({len(final_html.encode('utf-8')) / 1024:.1f} KB)")
print(f"Generated standalone quiz.html ({len(final_html.encode('utf-8')) / 1024:.1f} KB)")
