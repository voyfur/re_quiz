import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CATALOG_JS_PATH = ROOT / "web" / "catalog_data.js"
MATCHER_JS_PATH = ROOT / "web" / "client_matcher.js"
ARTIFACT_PATH = Path("/Users/anatoly/.gemini/antigravity/brain/4168c8d8-570e-488d-9192-d410885bdf9c/quiz_interactive.html")

catalog_js = CATALOG_JS_PATH.read_text(encoding="utf-8")
matcher_js = MATCHER_JS_PATH.read_text(encoding="utf-8")

template = """<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Race Expert Quiz — Интерактивный черновик</title>
  <script src="https://www.gstatic.com/antigravity/web/dev/tailwindcss.min.js"></script>
  <script>
__CATALOG_DATA__
  </script>
  <script>
__MATCHER_DATA__
  </script>
  <style>
    :root {
      --bg: var(--background, #0f172a);
      --card-bg: var(--card, #1e293b);
      --fg: var(--foreground, #f8fafc);
      --muted: var(--muted-foreground, #94a3b8);
      --brd: var(--border, #334155);
      --pri: var(--primary, #3b82f6);
    }
  </style>
</head>
<body class="bg-[var(--bg)] text-[var(--fg)] antialiased p-3 md:p-5 min-h-screen">
  <div class="max-w-2xl mx-auto space-y-4">
    <!-- Header -->
    <header class="flex items-center justify-between border-b border-[var(--brd)] pb-3">
      <div>
        <span class="text-xs font-semibold tracking-wider uppercase text-blue-400">Race Expert · Черновик подбора</span>
        <h1 class="text-lg font-bold text-[var(--fg)]">Интерактивный квиз покупателя</h1>
      </div>
      <div class="flex items-center gap-2">
        <select id="langSelect" class="bg-[var(--card-bg)] text-[var(--fg)] text-xs border border-[var(--brd)] rounded px-2 py-1">
          <option value="ru" selected>RU</option>
          <option value="uk">UK</option>
        </select>
        <span class="text-xs text-[var(--muted)] px-2 py-1 rounded bg-[var(--card-bg)] border border-[var(--brd)]">206 наборов</span>
      </div>
    </header>

    <!-- Quiz Main Card -->
    <main class="bg-[var(--card-bg)] border border-[var(--brd)] rounded-xl p-5 shadow-lg">
      <!-- Progress Bar -->
      <div class="mb-5">
        <div class="flex justify-between text-xs text-[var(--muted)] mb-1 font-medium">
          <span id="progressStepText">Вопрос 1</span>
          <span id="candidateCountBadge" class="text-blue-400">206 вариантов</span>
        </div>
        <div class="w-full bg-[var(--brd)] h-2 rounded-full overflow-hidden">
          <div id="progressBar" class="bg-blue-500 h-full transition-all duration-300 w-1/8"></div>
        </div>
      </div>

      <!-- Question Screen -->
      <div id="questionScreen">
        <h2 id="qTitle" class="text-base md:text-lg font-semibold text-[var(--fg)] mb-1"></h2>
        <p id="qHint" class="text-xs text-[var(--muted)] mb-4"></p>

        <!-- Single Choice Options -->
        <div id="optionsGrid" class="grid grid-cols-1 sm:grid-cols-2 gap-2 mb-6"></div>

        <!-- Number / Budget Input -->
        <div id="numberInputWrap" class="mb-6 hidden space-y-2">
          <label id="numberLabel" class="block text-xs font-medium text-[var(--muted)]"></label>
          <div class="relative">
            <input id="numberInput" type="number" class="w-full bg-[var(--bg)] border border-[var(--brd)] rounded-lg px-4 py-2.5 text-sm text-[var(--fg)] focus:outline-none focus:ring-2 focus:ring-blue-500 font-mono">
            <span id="inputCurrency" class="absolute right-3 top-2.5 text-xs text-[var(--muted)] hidden">₴</span>
          </div>
          <p id="numberHint" class="text-xs text-blue-400"></p>
        </div>

        <p id="errorMsg" class="text-xs text-red-400 mb-3 hidden"></p>

        <!-- Navigation Buttons -->
        <div class="flex items-center justify-between pt-3 border-t border-[var(--brd)]">
          <button id="backBtn" type="button" class="px-3 py-1.5 rounded-lg border border-[var(--brd)] text-xs font-medium text-[var(--muted)] hover:text-[var(--fg)] hover:bg-[var(--bg)] transition hidden">
            ← Назад
          </button>
          <div class="ml-auto flex gap-2">
            <button id="nextBtn" type="button" class="px-4 py-2 rounded-lg bg-blue-600 hover:bg-blue-500 text-xs font-semibold text-white transition shadow">
              Продолжить →
            </button>
            <button id="submitBtn" type="button" class="px-4 py-2 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-xs font-semibold text-white transition shadow hidden">
              Показать варианты
            </button>
          </div>
        </div>
      </div>

      <!-- Results Screen -->
      <div id="resultsScreen" class="hidden space-y-4">
        <div class="flex items-start justify-between border-b border-[var(--brd)] pb-3">
          <div>
            <span class="text-xs font-medium text-emerald-400 uppercase tracking-wider" id="resultsCategoryLabel">Результат подбора</span>
            <h2 id="resultsHeadline" class="text-base md:text-lg font-bold text-[var(--fg)]"></h2>
          </div>
          <button id="restartBtn" type="button" class="text-xs px-3 py-1.5 rounded border border-[var(--brd)] text-[var(--muted)] hover:text-[var(--fg)] hover:bg-[var(--bg)]">
            Изменить ответы
          </button>
        </div>

        <p id="resultsNote" class="text-xs text-[var(--muted)] bg-[var(--bg)] p-3 rounded-lg border border-[var(--brd)]"></p>

        <!-- Cards List -->
        <div id="cardsList" class="space-y-3"></div>

        <!-- Near-Miss Section -->
        <div id="nearMissSection" class="space-y-3 pt-3 border-t border-[var(--brd)] hidden">
          <h3 class="text-xs font-bold uppercase tracking-wider text-amber-400">Близко по бюджету (альтернативы)</h3>
          <div id="nearMissList" class="space-y-3"></div>
        </div>

        <!-- Floor Anchor Section -->
        <div id="floorAnchorSection" class="space-y-3 pt-3 border-t border-[var(--brd)] hidden">
          <h3 class="text-xs font-bold uppercase tracking-wider text-purple-400">Базовый стартовый комплект категории</h3>
          <div id="floorAnchorList" class="space-y-3"></div>
        </div>
      </div>
    </main>
  </div>

  <script>
    const COPY = {
      ru: {
        goalTitle: "Для какой ситуации вы ищете набор?",
        goalHint: "Выберите главную задачу. Последующие вопросы подстроятся под неё.",
        chooseOne: "Выберите один вариант",
        any: "Неважно",
        stepFirst: "Вопрос 1",
        stepCount: "Вопрос {current} из {total}",
        candidatesBadge: "{count} вариантов",
        back: "← Назад",
        continue: "Продолжить →",
        showResults: "Показать варианты",
        editAnswers: "Изменить ответы",
        price: "Цена по снимку",
        nearMissTitle: "Близко по бюджету (альтернативы)",
        floorTitle: "Базовый стартовый набор в категории",
        budgetPlaceholder: "Например: {min}",
        budgetHint: "Подходящие наборы: от {min} до {max} ₴. Оставьте пустым, если без ограничения.",
        sizeHint: "Размеры в этой ветке: {sizes}.",
        errorSelect: "Пожалуйста, выберите вариант для продолжения.",
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
        question_budget: "Какова максимальная цена всего набора (₴)?",
        activity_running: "Бег",
        activity_strength_training: "Силовые тренировки",
        activity_functional_training: "Функциональные тренировки",
        activity_cycling: "Велоспорт",
        activity_hiking: "Походы",
        activity_swimming: "Плавание",
        activity_mind_body_mobility: "Йога, пилатес и мобильность",
        activity_walking: "Ходьба",
        activity_general_fitness: "Общая физ. активность",
        activity_other: "Другая активность",
        class_protein_carbohydrate_food: "Питание и перекусы",
        class_supplements_vitamins_minerals: "Витамины и добавки",
        class_creatine_preworkout: "Креатин и предтреники",
        class_sports_accessories: "Спортивные аксессуары",
        class_apparel_footwear: "Одежда и обувь",
        class_hydration_items: "Гидратация",
        class_dehydrated_meal: "Сублимированная еда",
        scenario_event_preparation: "Подготовка к старту",
        scenario_training: "Тренировки",
        scenario_everyday: "На каждый день",
        membership_yes: "Да, с абонементом клуба",
        membership_no: "Нет, только товары",
        race_half_marathon: "Полумарафон",
        race_marathon: "Марафон",
        race_race_or_event_preparation: "Другой старт",
        race_ultra_or_long_distance: "Ультрамарафон",
        season_cold: "Холодная погода / зима",
        season_warm: "Тёплая погода / лето",
        form_bars: "Батончики",
        form_food_or_meal: "Готовая еда",
        form_gel: "Гели",
        form_liquid: "Жидкая форма",
        form_sticks: "Стики",
        form_capsules: "Капсулы",
        form_powder: "Порошок",
        form_softgels: "Софтгели",
        form_tablets: "Таблетки",
        form_apparel: "Одежда"
      },
      uk: {
        goalTitle: "Для якої ситуації ви шукаєте набір?",
        goalHint: "Виберіть головну задачу. Наступні питання підлаштуються під неї.",
        chooseOne: "Виберіть один варіант",
        any: "Неважливо",
        stepFirst: "Питання 1",
        stepCount: "Питання {current} з {total}",
        candidatesBadge: "{count} варіантів",
        back: "← Назад",
        continue: "Продовжити →",
        showResults: "Показати варіанти",
        editAnswers: "Змінити відповіді",
        price: "Ціна за знімком",
        nearMissTitle: "Близько за бюджетом (альтернативи)",
        floorTitle: "Базовий стартовий набір у категорії",
        budgetPlaceholder: "Наприклад: {min}",
        budgetHint: "Відповідні набори: від {min} до {max} ₴. Залиште порожнім, якщо без обмеження.",
        sizeHint: "Розміри у цій гілці: {sizes}.",
        errorSelect: "Будь ласка, оберіть варіант для продовження.",
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
        question_use_scenario: "Що найближче до вашої ситуації?",
        question_use_timing: "Коли використовуватимете набір?",
        question_use_place: "Де використовуватимете товари?",
        question_race_format: "До якого формату старту шукаєте набір?",
        question_season: "Для яких погодних умов шукаєте?",
        question_product_form: "Яка форма продукту вам зручніша?",
        question_shoe_size: "Який розмір взуття чи шкарпеток потрібен?",
        question_budget: "Яка максимальна ціна всього набору (₴)?",
        activity_running: "Біг",
        activity_strength_training: "Силові тренування",
        activity_functional_training: "Функціональні тренування",
        activity_cycling: "Велоспорт",
        activity_hiking: "Походи",
        activity_swimming: "Плавання",
        activity_mind_body_mobility: "Йога, пілатес і мобільність",
        activity_walking: "Ходьба",
        activity_general_fitness: "Загальна фіз. активність",
        activity_other: "Інша активність",
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
        membership_yes: "Так, з абонементом клубу",
        membership_no: "Ні, лише товари",
        race_half_marathon: "Напівмарафон",
        race_marathon: "Марафон",
        race_race_or_event_preparation: "Інший старт",
        race_ultra_or_long_distance: "Ультрамарафон",
        season_cold: "Холодна погода / зима",
        season_warm: "Тепла погода / літо",
        form_bars: "Батончики",
        form_food_or_meal: "Готова їжа",
        form_gel: "Гелі",
        form_liquid: "Рідка форма",
        form_sticks: "Стики",
        form_capsules: "Капсули",
        form_powder: "Порошок",
        form_softgels: "Софтгелі",
        form_tablets: "Таблетки",
        form_apparel: "Одяг"
      }
    };

    const state = {
      locale: "ru",
      goal: "",
      answers: {},
      history: [],
      currentQuestionId: "goal",
      questionPlan: [],
      optionsData: null,
      catalog: window.QUIZ_CATALOG || []
    };

    function t(key, vars = {}) {
      let str = COPY[state.locale]?.[key] || COPY.ru?.[key] || key;
      Object.entries(vars).forEach(([k, v]) => { str = str.replaceAll(`{${k}}`, v); });
      return str;
    }

    function labelForValue(qId, val) {
      if (val === "any") return t("any");
      const map = {
        activity: "activity_",
        component_class: "class_",
        membership: "membership_",
        use_scenario: "scenario_",
        race_format: "race_",
        season: "season_",
        product_form: "form_"
      };
      const prefix = map[qId] || "";
      return t(prefix + val);
    }

    function renderCurrentStep() {
      const isGoal = state.currentQuestionId === "goal";
      const plan = state.questionPlan;
      const q = isGoal
        ? { id: "goal", type: "single", options: ["running", "training", "hydration", "food", "recovery", "outdoors", "gear", "daily", "gift"] }
        : plan.find(item => item.id === state.currentQuestionId);

      if (!q) return;

      const totalSteps = Math.max(state.history.length + plan.length, 2);
      const curStep = state.history.length + 1;
      document.getElementById("progressStepText").textContent = isGoal
        ? t("stepFirst")
        : t("stepCount", { current: curStep, total: totalSteps });

      const pct = Math.min(100, Math.round((curStep / totalSteps) * 100));
      document.getElementById("progressBar").style.width = pct + "%";

      const candCount = state.optionsData?.candidate_count ?? 206;
      document.getElementById("candidateCountBadge").textContent = t("candidatesBadge", { count: candCount });

      document.getElementById("qTitle").textContent = isGoal ? t("goalTitle") : t(q.title_key);
      document.getElementById("qHint").textContent = isGoal ? t("goalHint") : (q.id === "activity" ? "Если вашего спорта нет в списке, выберите «Другая активность»." : "");
      document.getElementById("errorMsg").classList.add("hidden");

      const grid = document.getElementById("optionsGrid");
      const numWrap = document.getElementById("numberInputWrap");
      grid.innerHTML = "";

      if (q.type === "number") {
        grid.classList.add("hidden");
        numWrap.classList.remove("hidden");
        const inp = document.getElementById("numberInput");
        const lbl = document.getElementById("numberLabel");
        const hint = document.getElementById("numberHint");
        const curr = document.getElementById("inputCurrency");

        lbl.textContent = t(q.title_key);
        inp.value = state.answers[q.id] || "";

        if (q.id === "max_price_uah") {
          curr.classList.remove("hidden");
          const dMin = q.dynamic_min ?? 600;
          const dMax = q.dynamic_max ?? 4500;
          inp.placeholder = t("budgetPlaceholder", { min: dMin.toLocaleString() });
          hint.textContent = t("budgetHint", { min: dMin.toLocaleString(), max: dMax.toLocaleString() });
        } else if (q.id === "shoe_size") {
          curr.classList.add("hidden");
          inp.placeholder = "42";
          hint.textContent = q.ranges ? t("sizeHint", { sizes: q.ranges.join(", ") }) : "";
        }
      } else {
        numWrap.classList.add("hidden");
        grid.classList.remove("hidden");
        const opts = isGoal
          ? ["running", "training", "hydration", "food", "recovery", "outdoors", "gear", "daily", "gift"]
          : ["any", ...q.options];

        const selectedVal = isGoal ? state.goal : state.answers[q.id];

        opts.forEach(val => {
          const btn = document.createElement("button");
          btn.type = "button";
          const isSelected = selectedVal === val;
          btn.className = `p-3 rounded-lg border text-left text-xs md:text-sm font-medium transition flex items-center justify-between ${
            isSelected
              ? "bg-blue-600/20 border-blue-500 text-blue-300 ring-1 ring-blue-500"
              : "bg-[var(--bg)] border-[var(--brd)] text-[var(--fg)] hover:border-slate-500"
          }`;

          const text = isGoal ? t("goal_" + val) : labelForValue(q.id, val);
          btn.innerHTML = `<span>${text}</span>${isSelected ? '<span class="text-blue-400 font-bold">✓</span>' : ''}`;

          btn.onclick = () => {
            if (isGoal) {
              state.goal = val;
            } else {
              state.answers[q.id] = val;
            }
            renderCurrentStep();
          };
          grid.appendChild(btn);
        });
      }

      const isBudget = q.id === "max_price_uah";
      document.getElementById("backBtn").classList.toggle("hidden", state.history.length === 0);
      document.getElementById("nextBtn").classList.toggle("hidden", isBudget);
      document.getElementById("submitBtn").classList.toggle("hidden", !isBudget);
    }

    async function advance() {
      const isGoal = state.currentQuestionId === "goal";
      if (isGoal) {
        if (!state.goal) {
          showError(t("errorSelect"));
          return;
        }
        state.history.push("goal");
        updatePlan();
        if (state.questionPlan.length === 0) {
          showRecommendations();
          return;
        }
        state.currentQuestionId = state.questionPlan[0].id;
        renderCurrentStep();
        return;
      }

      const q = state.questionPlan.find(item => item.id === state.currentQuestionId);
      if (!q) return;

      if (q.type === "number") {
        const val = document.getElementById("numberInput").value.trim();
        state.answers[q.id] = val === "" ? "any" : Number(val);
      }

      const currentVal = state.answers[q.id];
      if (currentVal === undefined) {
        showError(t("errorSelect"));
        return;
      }

      state.history.push(q.id);
      updatePlan();

      const nextQ = state.questionPlan.find(item => !state.history.includes(item.id));
      if (!nextQ) {
        showRecommendations();
        return;
      }
      state.currentQuestionId = nextQ.id;
      renderCurrentStep();
    }

    function goBack() {
      if (state.history.length === 0) return;
      const prevId = state.history.pop();
      if (prevId === "goal") {
        state.goal = "";
        state.answers = {};
        state.questionPlan = [];
        state.currentQuestionId = "goal";
      } else {
        delete state.answers[prevId];
        state.currentQuestionId = prevId;
        updatePlan();
      }
      renderCurrentStep();
    }

    function updatePlan() {
      if (!state.goal) {
        state.optionsData = window.QUIZ_MATCHER.draftOptions(state.catalog);
        state.questionPlan = [];
        return;
      }
      state.optionsData = window.QUIZ_MATCHER.draftOptions(state.catalog, state.goal, state.answers);
      state.questionPlan = state.optionsData.question_plan || [];
    }

    function showError(msg) {
      const err = document.getElementById("errorMsg");
      err.textContent = msg;
      err.classList.remove("hidden");
    }

    function renderCard(item, isNearMiss = false, isFloor = false) {
      const card = document.createElement("div");
      card.className = "p-4 rounded-xl border border-[var(--brd)] bg-[var(--bg)] space-y-2 relative";

      const topRow = document.createElement("div");
      topRow.className = "flex items-center justify-between gap-2 text-xs text-[var(--muted)]";
      topRow.innerHTML = `
        <span class="font-mono">№ ${item.catalog_row} · ${item.sku || 'Без SKU'}</span>
        <div class="flex items-center gap-1.5">
          ${item.match_score_pct ? `<span class="px-2 py-0.5 rounded-full font-bold text-xs bg-blue-500/20 text-blue-400 border border-blue-500/30">${item.match_score_pct}%</span>` : ''}
          ${isNearMiss ? `<span class="px-2 py-0.5 rounded-full font-bold text-xs bg-amber-500/20 text-amber-300 border border-amber-500/30">+${item.price_over_budget_uah} ₴</span>` : ''}
          ${isFloor ? `<span class="px-2 py-0.5 rounded-full font-bold text-xs bg-purple-500/20 text-purple-300 border border-purple-500/30">Базовый старт</span>` : ''}
        </div>
      `;

      const title = document.createElement("h4");
      title.className = "text-sm font-semibold text-[var(--fg)] leading-snug";
      title.textContent = item.title;

      const price = document.createElement("div");
      price.className = "text-sm font-bold text-emerald-400";
      price.textContent = `${item.price_uah.toLocaleString()} ₴`;

      const reasonsList = document.createElement("ul");
      reasonsList.className = "text-xs text-[var(--muted)] space-y-1 list-disc list-inside pt-1";
      (item.reasons || []).forEach(r => {
        const li = document.createElement("li");
        li.textContent = r;
        reasonsList.appendChild(li);
      });

      const link = document.createElement("a");
      link.href = item.source_url;
      link.target = "_blank";
      link.rel = "noopener noreferrer";
      link.className = "inline-block text-xs text-blue-400 hover:underline pt-2 font-medium";
      link.textContent = "Открыть страницу набора →";

      card.append(topRow, title, price, reasonsList, link);
      return card;
    }

    function showRecommendations() {
      const req = {
        goal_group: state.goal,
        locale: state.locale,
        ...state.answers
      };
      if (req.max_price_uah === "any") delete req.max_price_uah;
      if (req.shoe_size === "any") delete req.shoe_size;

      const res = window.QUIZ_MATCHER.draftRecommend(state.catalog, req);

      document.getElementById("questionScreen").classList.add("hidden");
      document.getElementById("resultsScreen").classList.remove("hidden");

      document.getElementById("resultsHeadline").textContent = res.results.length > 0
        ? `Найдено наборов: ${res.returned_count}`
        : "Подходящих вариантов не найдено";

      document.getElementById("resultsNote").textContent = res.message;

      const cardsList = document.getElementById("cardsList");
      cardsList.innerHTML = "";
      res.results.forEach(item => cardsList.appendChild(renderCard(item)));

      const nearSec = document.getElementById("nearMissSection");
      const nearList = document.getElementById("nearMissList");
      nearList.innerHTML = "";
      if (res.near_miss_results && res.near_miss_results.length > 0) {
        nearSec.classList.remove("hidden");
        res.near_miss_results.forEach(item => nearList.appendChild(renderCard(item, true)));
      } else {
        nearSec.classList.add("hidden");
      }

      const floorSec = document.getElementById("floorAnchorSection");
      const floorList = document.getElementById("floorAnchorList");
      floorList.innerHTML = "";
      if (res.floor_anchor_results && res.floor_anchor_results.length > 0) {
        floorSec.classList.remove("hidden");
        res.floor_anchor_results.forEach(item => floorList.appendChild(renderCard(item, false, true)));
      } else {
        floorSec.classList.add("hidden");
      }
    }

    document.getElementById("nextBtn").onclick = advance;
    document.getElementById("submitBtn").onclick = advance;
    document.getElementById("backBtn").onclick = goBack;

    document.getElementById("restartBtn").onclick = () => {
      state.goal = "";
      state.answers = {};
      state.history = [];
      state.currentQuestionId = "goal";
      updatePlan();
      document.getElementById("resultsScreen").classList.add("hidden");
      document.getElementById("questionScreen").classList.remove("hidden");
      renderCurrentStep();
    };

    document.getElementById("langSelect").onchange = (e) => {
      state.locale = e.target.value;
      renderCurrentStep();
    };

    updatePlan();
    renderCurrentStep();
  </script>
</body>
</html>
"""

final_html = template.replace("__CATALOG_DATA__", catalog_js).replace("__MATCHER_DATA__", matcher_js)
ARTIFACT_PATH.write_text(final_html, encoding="utf-8")
print(f"Artifact created at {ARTIFACT_PATH} ({len(final_html.encode('utf-8')) / 1024:.1f} KB)")
