/**
 * Race Expert - Custom Multi-Sport Box Builder
 * Supports: Running, Cycling, Triathlon, Gym & Fitness, Hiking & Outdoor (ЇDLO)
 * Authentic Light Theme for Race Expert Store
 * Reactive Frontend & OpenCart Multi-Add Integration
 */

(function () {
  'use strict';

  // Sport Metadata & Configurations
  const SPORT_SLOT_META = {
    running: [
      { key: 'energy', title: 'Енергія та вуглеводи', icon: '⚡', desc: 'Основне паливо для підтримки темпу' },
      { key: 'hydration', title: 'Гідратація та солі', icon: '💧', desc: 'Захист від судом і втрати мінералів' },
      { key: 'gear', title: 'Бігове спорядження', icon: '🎒', desc: 'Комфортне перенесення та захист' },
      { key: 'care_recovery', title: 'Догляд та відновлення', icon: '🛡️', desc: 'Захист шкіри, зв’язок та релаксація м’язів' }
    ],
    cycling: [
      { key: 'energy', title: 'Енергія та батончики', icon: '⚡', desc: 'Вуглеводи для стабільного каденсу в сідлі' },
      { key: 'hydration', title: 'Гідратація та електроліти', icon: '💧', desc: 'Ізотоніки у флягу та солі від судом' },
      { key: 'gear', title: 'Велоспорядження та фляги', icon: '🚴', desc: 'Пляшки та шкарпетки для тривалого педалювання' },
      { key: 'care_recovery', title: 'Догляд за сідлом (Chamois) та рекавері', icon: '🛡️', desc: 'Крем Chamois Butt’r та м’язове відновлення' }
    ],
    triathlon: [
      { key: 'energy', title: 'Гідрогелі та енергія', icon: '⚡', desc: 'Легке ковтання у транзитних зонах T1/T2' },
      { key: 'hydration', title: 'Електроліти проти судом', icon: '💧', desc: 'Захист литок у холодній воді та на вело' },
      { key: 'gear', title: 'Стартове спорядження', icon: '🏊🚴', desc: 'Пояс для номера та фляги для транзитки' },
      { key: 'care_recovery', title: 'TRISWIM та рекавері', icon: '🛡️', desc: 'Захист від хлору, натертостей гідрокостюма та регенерація' }
    ],
    gym: [
      { key: 'energy', title: 'Енергія та передтрени', icon: '⚡', desc: 'Фокус, витривалість та пампінг у залі' },
      { key: 'hydration', title: 'Гідратація та BCAA', icon: '💧', desc: 'Захист м’язів від катаболізму під час підходів' },
      { key: 'gear', title: 'Спортивний шейкер', icon: '🥤', desc: 'Змішування протеїнових коктейлів без грудочок' },
      { key: 'care_recovery', title: '100% Протеїн, креатин та рекавері', icon: '💪', desc: 'Анаболічне вікно, ріст силових та синтез білка' }
    ],
    outdoor: [
      { key: 'energy', title: 'Сублімати ЇDLO (гаряче)', icon: '🍲', desc: 'Калорійні супи, сніданки та обіди прямо в пакеті' },
      { key: 'hydration', title: 'Гідратація та чай / кава', icon: '☕', desc: 'Мінералізація води, електроліти та напій у таборі' },
      { key: 'gear', title: 'Трекінгове спорядження', icon: '🎒', desc: 'Шкарпетки RE із зональним ущільненням та фляги' },
      { key: 'care_recovery', title: 'Джерки ЇDLO (білок) та догляд', icon: '🥩', desc: 'Сушене м’ясо на привалах та магній для натруджених ніг' }
    ]
  };

  const SPORT_BADGES = {
    running: '🏃 Біг (478 товарів)',
    cycling: '🚴 Велоспорт (40 товарів)',
    triathlon: '🏊🚴 Триатлон (34 товари)',
    gym: '🏋️ Фітнес / Зал (40 товарів)',
    outdoor: '🏕️ Походи (ЇDLO) (32 товари)'
  };

  const RUNNING_TIER_PRICES = {
    '10k': {
      economy: 'до 900 ₴',
      standard: 'до 1 500 ₴',
      premium: 'від 2 200+ ₴'
    },
    '21k': {
      economy: 'до 1 200 ₴',
      standard: 'до 2 000 ₴',
      premium: 'від 2 800+ ₴'
    },
    '42k': {
      economy: 'до 2 800 ₴',
      standard: 'до 3 800 ₴',
      premium: 'від 4 500+ ₴'
    },
    'ultra': {
      economy: 'до 3 000 ₴',
      standard: 'до 4 500 ₴',
      premium: 'від 5 500+ ₴'
    }
  };

  function updateRunningPriceBadges(dist) {
    const prices = RUNNING_TIER_PRICES[dist] || RUNNING_TIER_PRICES['21k'];
    const bEco = el('running-price-badge-economy');
    const bStd = el('running-price-badge-standard');
    const bPre = el('running-price-badge-premium');
    if (bEco) bEco.textContent = prices.economy;
    if (bStd) bStd.textContent = prices.standard;
    if (bPre) bPre.textContent = prices.premium;
  }

  // State Management
  const state = {
    sport: 'running',
    currentStep: 1,
    totalSteps: 7,
    answers: {
      distance: '21k',
      pace_target: 'steady',
      weather: 'moderate',
      stomach_type: 'normal',
      caffeine_preference: 'boost',
      body_concerns: [],
      gear_needed: [],
      price_tier: 'standard'
    },
    sportAnswers: {
      cycling: {
        distance_format: 'medium',
        weather: 'moderate',
        caffeine_preference: 'boost',
        saddle_comfort: true,
        price_tier: 'standard'
      },
      triathlon: {
        format: 'half',
        wetsuit_care: true,
        caffeine_preference: 'boost',
        price_tier: 'standard'
      },
      gym: {
        goal: 'mass',
        pre_workout_boost: 'caffeine',
        price_tier: 'standard'
      },
      outdoor: {
        duration: 'weekend',
        price_tier: 'standard'
      }
    },
    boxData: null,
    selectedItems: {},
    variantSelections: {},
    swapIndex: {},
    customSelections: {},
    isCheckingOut: false
  };

  const el = (id) => document.getElementById(id);

  function init() {
    setupSportSelectorListeners();
    setupRunningStepListeners();
    updateStepperUI();
    updateRunningPriceBadges(state.answers.distance || '21k');
    attachGlobalActions();
    setupTabs();
  }

  // Setup Product Page Tabs
  function setupTabs() {
    const tabBtns = document.querySelectorAll('.product-tab-btn');
    tabBtns.forEach((btn) => {
      btn.addEventListener('click', () => {
        const targetTab = btn.dataset.tab;
        tabBtns.forEach((b) => {
          b.classList.remove('border-blue-600', 'text-blue-700', 'border-b-2', 'font-bold');
          b.classList.add('border-transparent', 'text-slate-500', 'hover:text-slate-800');
        });
        btn.classList.add('border-blue-600', 'text-blue-700', 'border-b-2', 'font-bold');
        btn.classList.remove('border-transparent', 'text-slate-500');

        document.querySelectorAll('.product-tab-content').forEach((panel) => {
          if (panel.id === `tab-pane-${targetTab}`) {
            panel.classList.remove('hidden');
          } else {
            panel.classList.add('hidden');
          }
        });
      });
    });
  }

  // Sport Selector Handling
  function setupSportSelectorListeners() {
    document.querySelectorAll('.sport-btn').forEach((btn) => {
      btn.addEventListener('click', () => {
        const selectedSport = btn.dataset.sport;
        const resultsVisible = !el('result-container')?.classList.contains('hidden');
        if (state.sport === selectedSport && !resultsVisible) return;
        setSport(selectedSport);
        const target = el('sport-selector') || el('stepper-container') || document.body;
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      });
    });
  }

  function setSport(newSport) {
    state.sport = newSport;
    
    // Always hide results and show quiz forms when switching or resetting sport
    el('result-container')?.classList.add('hidden');
    el('stepper-container')?.classList.remove('hidden');

    const s7 = el('step-7-submit');
    if (s7) {
      s7.disabled = false;
      s7.innerHTML = `<span>Сформувати мій Стартовий бокс</span><svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M14 5l7 7m0 0l-7 7m7-7H3"></path></svg>`;
    }
    
    // Update button states
    document.querySelectorAll('.sport-btn').forEach((btn) => {
      const isTarget = btn.dataset.sport === newSport;
      if (isTarget) {
        btn.className = 'sport-btn p-3 rounded-xl border-2 border-blue-600 bg-blue-50 text-blue-900 font-bold text-xs flex flex-col items-center gap-1 transition-all re-shadow-sm';
      } else {
        btn.className = 'sport-btn p-3 rounded-xl border border-slate-200 bg-white hover:border-blue-400 hover:bg-slate-50 text-slate-700 font-semibold text-xs flex flex-col items-center gap-1 transition-all';
      }
    });

    // Update active badge
    const badge = el('active-sport-badge');
    if (badge) {
      badge.textContent = SPORT_BADGES[newSport] || newSport;
    }

    const runningSteps = el('running-steps-container');
    const runningHeader = el('running-stepper-header');
    const otherContainer = el('other-sports-container');

    if (newSport === 'running') {
      if (runningSteps) runningSteps.classList.remove('hidden');
      if (runningHeader) runningHeader.classList.remove('hidden');
      if (otherContainer) otherContainer.classList.add('hidden');
      state.currentStep = 1;
      updateStepperUI();
      updateRunningPriceBadges(state.answers.distance || '21k');
    } else {
      if (runningSteps) runningSteps.classList.add('hidden');
      if (runningHeader) runningHeader.classList.add('hidden');
      if (otherContainer) {
        otherContainer.classList.remove('hidden');
        renderOtherSportForm(newSport);
      }
    }
  }

  // Render Form for Cycling, Triathlon, Gym, Outdoor
  function renderOtherSportForm(sport) {
    const container = el('other-sports-container');
    if (!container) return;

    if (sport === 'cycling') {
      container.innerHTML = `
        <div class="space-y-6">
          <div>
            <div class="inline-flex items-center gap-2 px-2.5 py-1 rounded-md bg-blue-50 text-blue-700 text-xs font-semibold border border-blue-200 mb-2">
              <span>🚴</span> <span>Конфігуратор велобоксу</span>
            </div>
            <h2 class="text-xl md:text-2xl font-bold font-display text-slate-900 tracking-tight">
              Специфіка вашого велозаїзду
            </h2>
            <p class="text-sm text-slate-500 mt-1">
              Двигун розрахує необхідні вуглеводи на годину, ізотоніки у флягу та крем від натертостей сідлом.
            </p>
          </div>

          <!-- Q1: Distance -->
          <div class="space-y-2.5">
            <label class="text-xs font-bold text-slate-700 uppercase tracking-wider block">Формат заїзду:</label>
            <div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
              <button type="button" data-field="distance_format" data-val="short" class="sport-opt-btn p-3.5 rounded-xl border border-slate-200 bg-white hover:border-blue-400 text-slate-800 text-left transition-all re-shadow-sm">
                <div class="font-bold text-sm text-slate-900">Короткий (до 50 км)</div>
                <div class="text-xs text-slate-500 mt-0.5">1.5–2 години в сідлі</div>
              </button>
              <button type="button" data-field="distance_format" data-val="medium" class="sport-opt-btn p-3.5 rounded-xl border-2 border-blue-600 bg-blue-50 text-blue-900 ring-2 ring-blue-500/20 text-left transition-all re-shadow-sm">
                <div class="font-bold text-sm text-blue-900">Середній (60–100 км)</div>
                <div class="text-xs text-slate-600 mt-0.5">Груповий виїзд або гравел</div>
              </button>
              <button type="button" data-field="distance_format" data-val="long" class="sport-opt-btn p-3.5 rounded-xl border border-slate-200 bg-white hover:border-blue-400 text-slate-800 text-left transition-all re-shadow-sm">
                <div class="font-bold text-sm text-slate-900">Гран Фондо (100+ км)</div>
                <div class="text-xs text-slate-500 mt-0.5">Бревет / довга витривалість</div>
              </button>
            </div>
          </div>

          <!-- Q2: Weather & Cramps -->
          <div class="space-y-2.5">
            <label class="text-xs font-bold text-slate-700 uppercase tracking-wider block">Погода під час заїзду:</label>
            <div class="grid grid-cols-2 gap-3">
              <button type="button" data-field="weather" data-val="moderate" class="sport-opt-btn p-3.5 rounded-xl border-2 border-blue-600 bg-blue-50 text-blue-900 ring-2 ring-blue-500/20 text-left transition-all re-shadow-sm">
                <div class="font-bold text-sm text-blue-900">🌤️ Помірна / комфортна</div>
                <div class="text-xs text-slate-600 mt-0.5">15–22°C</div>
              </button>
              <button type="button" data-field="weather" data-val="hot" class="sport-opt-btn p-3.5 rounded-xl border border-slate-200 bg-white hover:border-blue-400 text-slate-800 text-left transition-all re-shadow-sm">
                <div class="font-bold text-sm text-slate-900">☀️ Спека (+24°C і вище)</div>
                <div class="text-xs text-slate-500 mt-0.5">Потрібні додаткові солі</div>
              </button>
            </div>
          </div>

          <!-- Q3: Saddle Comfort -->
          <div class="space-y-2.5">
            <label class="text-xs font-bold text-slate-700 uppercase tracking-wider block">Захист від натирання сідлом (Chamois Butt'r):</label>
            <div class="grid grid-cols-2 gap-3">
              <button type="button" data-field="saddle_comfort" data-val="true" class="sport-opt-btn p-3.5 rounded-xl border-2 border-blue-600 bg-blue-50 text-blue-900 ring-2 ring-blue-500/20 text-left transition-all re-shadow-sm">
                <div class="font-bold text-sm text-blue-900">🛡️ Так, додати крем Chamois</div>
                <div class="text-xs text-slate-600 mt-0.5">На памперс перед виїздом</div>
              </button>
              <button type="button" data-field="saddle_comfort" data-val="false" class="sport-opt-btn p-3.5 rounded-xl border border-slate-200 bg-white hover:border-blue-400 text-slate-800 text-left transition-all re-shadow-sm">
                <div class="font-bold text-sm text-slate-900">❌ Не потрібно</div>
                <div class="text-xs text-slate-500 mt-0.5">Є свій перевірений крем</div>
              </button>
            </div>
          </div>

          <!-- Q4: Price Tier & Custom Budget -->
          <div class="space-y-3">
            <div class="flex items-center justify-between">
              <label class="text-xs font-bold text-slate-700 uppercase tracking-wider block">Ціновий сегмент або точний бюджет:</label>
              <span class="text-[11px] text-slate-500">Оберіть категорію або вкажіть суму</span>
            </div>
            <div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
              <button type="button" data-field="price_tier" data-val="economy" class="sport-opt-btn p-3.5 rounded-xl border border-slate-200 bg-white hover:border-blue-400 text-left transition-all re-shadow-sm cursor-pointer">
                <div class="flex items-center justify-between">
                  <span class="font-bold text-xs text-emerald-600 block">🟢 Економ</span>
                  <span class="text-[11px] font-extrabold text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded-md border border-emerald-200">до 2 300 ₴</span>
                </div>
                <div class="text-[11px] text-slate-500 mt-1">Базовий надійний набір</div>
              </button>
              <button type="button" data-field="price_tier" data-val="standard" class="sport-opt-btn p-3.5 rounded-xl border-2 border-blue-600 bg-blue-50 text-blue-900 ring-2 ring-blue-500/20 text-left transition-all re-shadow-sm cursor-pointer">
                <div class="flex items-center justify-between">
                  <span class="font-bold text-xs text-blue-900 block">🔵 Оптимальний</span>
                  <span class="text-[11px] font-extrabold text-blue-700 bg-blue-100/60 px-2 py-0.5 rounded-md border border-blue-200">до 3 000 ₴</span>
                </div>
                <div class="text-[11px] text-slate-600 mt-1">SiS, Sponser, Chamois</div>
              </button>
              <button type="button" data-field="price_tier" data-val="premium" class="sport-opt-btn p-3.5 rounded-xl border border-slate-200 bg-white hover:border-blue-400 text-left transition-all re-shadow-sm cursor-pointer">
                <div class="flex items-center justify-between">
                  <span class="font-bold text-xs text-purple-700 block">🟣 PRO / Еліта</span>
                  <span class="text-[11px] font-extrabold text-purple-700 bg-purple-50 px-2 py-0.5 rounded-md border border-purple-200">від 3 500+ ₴</span>
                </div>
                <div class="text-[11px] text-slate-500 mt-1">Maurten, Beta Fuel</div>
              </button>
            </div>

            <!-- Custom Budget Input -->
            <div class="p-4 rounded-xl border-2 border-dashed border-slate-300 bg-slate-50/70 hover:bg-slate-50 transition-all flex flex-col sm:flex-row sm:items-center justify-between gap-3.5 sport-custom-budget-container">
              <div class="flex-1">
                <label for="cycling-custom-budget-input" class="text-xs font-bold text-slate-800 flex items-center gap-2 cursor-pointer">
                  <span class="text-base">💰</span> <span>Вказати точний максимальний бюджет (грн):</span>
                </label>
                <span class="text-[11px] text-slate-500 block mt-0.5">
                  Введіть вашу бажану суму (наприклад: 2 500 грн) — алгоритм точно вкладеться у цей ліміт.
                </span>
              </div>
              <div class="relative w-full sm:w-44 flex-shrink-0">
                <input 
                  type="number" 
                  id="cycling-custom-budget-input" 
                  min="300" 
                  max="50000" 
                  step="50" 
                  placeholder="Напр. 2500" 
                  class="sport-custom-budget-input w-full pl-3.5 pr-10 py-2.5 rounded-xl border border-slate-300 focus:border-blue-600 focus:ring-2 focus:ring-blue-100 font-extrabold text-slate-900 text-sm outline-none bg-white transition-all"
                >
                <span class="absolute right-3.5 top-2.5 text-xs font-bold text-slate-400 pointer-events-none">грн</span>
              </div>
            </div>
          </div>

          <div class="pt-4">
            <button id="other-sport-submit" type="button" class="w-full py-4 px-6 rounded-xl bg-blue-600 hover:bg-blue-700 text-white font-extrabold text-base tracking-wide shadow-lg shadow-blue-600/25 transition-all flex items-center justify-center gap-2">
              <span>Зібрати мій Велобокс ➔</span>
            </button>
          </div>
        </div>
      `;
    } else if (sport === 'triathlon') {
      container.innerHTML = `
        <div class="space-y-6">
          <div>
            <div class="inline-flex items-center gap-2 px-2.5 py-1 rounded-md bg-blue-50 text-blue-700 text-xs font-semibold border border-blue-200 mb-2">
              <span>🏊🚴🏃</span> <span>Конфігуратор для триатлону</span>
            </div>
            <h2 class="text-xl md:text-2xl font-bold font-display text-slate-900 tracking-tight">
              Параметри вашої мультиспортивної гонки
            </h2>
            <p class="text-sm text-slate-500 mt-1">
              Підбір харчування в транзитні зони T1/T2, захист від судом у воді та догляд TRISWIM від хлору.
            </p>
          </div>

          <!-- Q1: Format -->
          <div class="space-y-2.5">
            <label class="text-xs font-bold text-slate-700 uppercase tracking-wider block">Формат змагань:</label>
            <div class="grid grid-cols-2 sm:grid-cols-4 gap-2.5">
              <button type="button" data-field="format" data-val="sprint" class="sport-opt-btn p-3 rounded-xl border border-slate-200 bg-white hover:border-blue-400 text-slate-800 text-left transition-all re-shadow-sm">
                <div class="font-bold text-xs text-slate-900">Спринт / Олімпійка</div>
              </button>
              <button type="button" data-field="format" data-val="half" class="sport-opt-btn p-3 rounded-xl border-2 border-blue-600 bg-blue-50 text-blue-900 ring-2 ring-blue-500/20 text-left transition-all re-shadow-sm">
                <div class="font-bold text-xs text-blue-900">Half-Ironman 70.3</div>
              </button>
              <button type="button" data-field="format" data-val="full" class="sport-opt-btn p-3 rounded-xl border border-slate-200 bg-white hover:border-blue-400 text-slate-800 text-left transition-all re-shadow-sm">
                <div class="font-bold text-xs text-slate-900">Full Ironman 140.6</div>
              </button>
              <button type="button" data-field="format" data-val="swim" class="sport-opt-btn p-3 rounded-xl border border-slate-200 bg-white hover:border-blue-400 text-slate-800 text-left transition-all re-shadow-sm">
                <div class="font-bold text-xs text-slate-900">Заплив Open Water</div>
              </button>
            </div>
          </div>

          <!-- Q2: Wetsuit & Chlorine -->
          <div class="space-y-2.5">
            <label class="text-xs font-bold text-slate-700 uppercase tracking-wider block">Захист від хлору та натертостей гідрокостюма:</label>
            <div class="grid grid-cols-2 gap-3">
              <button type="button" data-field="wetsuit_care" data-val="true" class="sport-opt-btn p-3.5 rounded-xl border-2 border-blue-600 bg-blue-50 text-blue-900 ring-2 ring-blue-500/20 text-left transition-all re-shadow-sm">
                <div class="font-bold text-sm text-blue-900">🏊 Додати TRISWIM</div>
                <div class="text-xs text-slate-600 mt-0.5">Нейтралізація хлору і солі</div>
              </button>
              <button type="button" data-field="wetsuit_care" data-val="false" class="sport-opt-btn p-3.5 rounded-xl border border-slate-200 bg-white hover:border-blue-400 text-slate-800 text-left transition-all re-shadow-sm">
                <div class="font-bold text-sm text-slate-900">❌ Не потрібно</div>
                <div class="text-xs text-slate-500 mt-0.5">Тільки харчування</div>
              </button>
            </div>
          </div>

          <!-- Q3: Price Tier & Custom Budget -->
          <div class="space-y-3">
            <div class="flex items-center justify-between">
              <label class="text-xs font-bold text-slate-700 uppercase tracking-wider block">Ціновий сегмент або точний бюджет:</label>
              <span class="text-[11px] text-slate-500">Оберіть категорію або вкажіть суму</span>
            </div>
            <div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
              <button type="button" data-field="price_tier" data-val="economy" class="sport-opt-btn p-3.5 rounded-xl border border-slate-200 bg-white hover:border-blue-400 text-left transition-all re-shadow-sm cursor-pointer">
                <div class="flex items-center justify-between">
                  <span class="font-bold text-xs text-emerald-600 block">🟢 Економ</span>
                  <span class="text-[11px] font-extrabold text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded-md border border-emerald-200">до 2 500–3 500 ₴</span>
                </div>
                <div class="text-[11px] text-slate-500 mt-1">Базовий стартовий набір</div>
              </button>
              <button type="button" data-field="price_tier" data-val="standard" class="sport-opt-btn p-3.5 rounded-xl border-2 border-blue-600 bg-blue-50 text-blue-900 ring-2 ring-blue-500/20 text-left transition-all re-shadow-sm cursor-pointer">
                <div class="flex items-center justify-between">
                  <span class="font-bold text-xs text-blue-900 block">🔵 Оптимальний</span>
                  <span class="text-[11px] font-extrabold text-blue-700 bg-blue-100/60 px-2 py-0.5 rounded-md border border-blue-200">до 4 200–6 000 ₴</span>
                </div>
                <div class="text-[11px] text-slate-600 mt-1">SiS, Precision, Sponser</div>
              </button>
              <button type="button" data-field="price_tier" data-val="premium" class="sport-opt-btn p-3.5 rounded-xl border border-slate-200 bg-white hover:border-blue-400 text-left transition-all re-shadow-sm cursor-pointer">
                <div class="flex items-center justify-between">
                  <span class="font-bold text-xs text-purple-700 block">🟣 PRO / Maurten</span>
                  <span class="text-[11px] font-extrabold text-purple-700 bg-purple-50 px-2 py-0.5 rounded-md border border-purple-200">від 8 000+ ₴</span>
                </div>
                <div class="text-[11px] text-slate-500 mt-1">Maurten Hydrogel повний курс</div>
              </button>
            </div>

            <!-- Custom Budget Input -->
            <div class="p-4 rounded-xl border-2 border-dashed border-slate-300 bg-slate-50/70 hover:bg-slate-50 transition-all flex flex-col sm:flex-row sm:items-center justify-between gap-3.5 sport-custom-budget-container">
              <div class="flex-1">
                <label for="triathlon-custom-budget-input" class="text-xs font-bold text-slate-800 flex items-center gap-2 cursor-pointer">
                  <span class="text-base">💰</span> <span>Вказати точний максимальний бюджет (грн):</span>
                </label>
                <span class="text-[11px] text-slate-500 block mt-0.5">
                  Введіть вашу бажану суму (наприклад: 4 500 грн) — алгоритм точно вкладеться у цей ліміт.
                </span>
              </div>
              <div class="relative w-full sm:w-44 flex-shrink-0">
                <input 
                  type="number" 
                  id="triathlon-custom-budget-input" 
                  min="300" 
                  max="50000" 
                  step="50" 
                  placeholder="Напр. 4500" 
                  class="sport-custom-budget-input w-full pl-3.5 pr-10 py-2.5 rounded-xl border border-slate-300 focus:border-blue-600 focus:ring-2 focus:ring-blue-100 font-extrabold text-slate-900 text-sm outline-none bg-white transition-all"
                >
                <span class="absolute right-3.5 top-2.5 text-xs font-bold text-slate-400 pointer-events-none">грн</span>
              </div>
            </div>
          </div>

          <div class="pt-4">
            <button id="other-sport-submit" type="button" class="w-full py-4 px-6 rounded-xl bg-blue-600 hover:bg-blue-700 text-white font-extrabold text-base tracking-wide shadow-lg shadow-blue-600/25 transition-all flex items-center justify-center gap-2">
              <span>Зібрати бокс для триатлону ➔</span>
            </button>
          </div>
        </div>
      `;
    } else if (sport === 'gym') {
      container.innerHTML = `
        <div class="space-y-6">
          <div>
            <div class="inline-flex items-center gap-2 px-2.5 py-1 rounded-md bg-blue-50 text-blue-700 text-xs font-semibold border border-blue-200 mb-2">
              <span>🏋️</span> <span>Конфігуратор силового боксу</span>
            </div>
            <h2 class="text-xl md:text-2xl font-bold font-display text-slate-900 tracking-tight">
              Ваші цілі в тренажерному залі
            </h2>
            <p class="text-sm text-slate-500 mt-1">
              Підбір передтренувального заряду, BCAA, 100% сироваткового протеїну та креатину.
            </p>
          </div>

          <!-- Q1: Goal -->
          <div class="space-y-2.5">
            <label class="text-xs font-bold text-slate-700 uppercase tracking-wider block">Головна ціль тренувань:</label>
            <div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
              <button type="button" data-field="goal" data-val="mass" class="sport-opt-btn p-3.5 rounded-xl border-2 border-blue-600 bg-blue-50 text-blue-900 ring-2 ring-blue-500/20 text-left transition-all re-shadow-sm">
                <div class="font-bold text-sm text-blue-900">💪 М'язова маса та сила</div>
                <div class="text-xs text-slate-600 mt-0.5">Курс на 1 місяць</div>
              </button>
              <button type="button" data-field="goal" data-val="lean" class="sport-opt-btn p-3.5 rounded-xl border border-slate-200 bg-white hover:border-blue-400 text-slate-800 text-left transition-all re-shadow-sm">
                <div class="font-bold text-sm text-slate-900">🔥 Рельєф та сушка</div>
                <div class="text-xs text-slate-500 mt-0.5">Ізолят, L-карнітин</div>
              </button>
              <button type="button" data-field="goal" data-val="tone" class="sport-opt-btn p-3.5 rounded-xl border border-slate-200 bg-white hover:border-blue-400 text-slate-800 text-left transition-all re-shadow-sm">
                <div class="font-bold text-sm text-slate-900">⚡ Тонус та здоров'я</div>
                <div class="text-xs text-slate-500 mt-0.5">Функціональний фітнес</div>
              </button>
            </div>
          </div>

          <!-- Q2: Pre-workout -->
          <div class="space-y-2.5">
            <label class="text-xs font-bold text-slate-700 uppercase tracking-wider block">Передтренувальний буст:</label>
            <div class="grid grid-cols-2 gap-3">
              <button type="button" data-field="pre_workout_boost" data-val="caffeine" class="sport-opt-btn p-3.5 rounded-xl border-2 border-blue-600 bg-blue-50 text-blue-900 ring-2 ring-blue-500/20 text-left transition-all re-shadow-sm">
                <div class="font-bold text-sm text-blue-900">⚡ З кофеїном</div>
                <div class="text-xs text-slate-600 mt-0.5">Вибухова концентрація та памп</div>
              </button>
              <button type="button" data-field="pre_workout_boost" data-val="none" class="sport-opt-btn p-3.5 rounded-xl border border-slate-200 bg-white hover:border-blue-400 text-slate-800 text-left transition-all re-shadow-sm">
                <div class="font-bold text-sm text-slate-900">🌿 Без кофеїну</div>
                <div class="text-xs text-slate-500 mt-0.5">Для вечірніх тренувань</div>
              </button>
            </div>
          </div>

          <!-- Q3: Price Tier & Custom Budget -->
          <div class="space-y-3">
            <div class="flex items-center justify-between">
              <label class="text-xs font-bold text-slate-700 uppercase tracking-wider block">Ціновий сегмент або точний бюджет:</label>
              <span class="text-[11px] text-slate-500">Оберіть категорію або вкажіть суму</span>
            </div>
            <div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
              <button type="button" data-field="price_tier" data-val="economy" class="sport-opt-btn p-3.5 rounded-xl border border-slate-200 bg-white hover:border-blue-400 text-left transition-all re-shadow-sm cursor-pointer">
                <div class="flex items-center justify-between">
                  <span class="font-bold text-xs text-emerald-600 block">🟢 Економ</span>
                  <span class="text-[11px] font-extrabold text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded-md border border-emerald-200">до 2 800 ₴</span>
                </div>
                <div class="text-[11px] text-slate-500 mt-1">BioTech / PureGold</div>
              </button>
              <button type="button" data-field="price_tier" data-val="standard" class="sport-opt-btn p-3.5 rounded-xl border-2 border-blue-600 bg-blue-50 text-blue-900 ring-2 ring-blue-500/20 text-left transition-all re-shadow-sm cursor-pointer">
                <div class="flex items-center justify-between">
                  <span class="font-bold text-xs text-blue-900 block">🔵 Оптимальний</span>
                  <span class="text-[11px] font-extrabold text-blue-700 bg-blue-100/60 px-2 py-0.5 rounded-md border border-blue-200">до 4 800 ₴</span>
                </div>
                <div class="text-[11px] text-slate-600 mt-1">Scitec / Olimp</div>
              </button>
              <button type="button" data-field="price_tier" data-val="premium" class="sport-opt-btn p-3.5 rounded-xl border border-slate-200 bg-white hover:border-blue-400 text-left transition-all re-shadow-sm cursor-pointer">
                <div class="flex items-center justify-between">
                  <span class="font-bold text-xs text-purple-700 block">🟣 PRO / Gold</span>
                  <span class="text-[11px] font-extrabold text-purple-700 bg-purple-50 px-2 py-0.5 rounded-md border border-purple-200">від 6 500+ ₴</span>
                </div>
                <div class="text-[11px] text-slate-500 mt-1">Optimum Nutrition Whey</div>
              </button>
            </div>

            <!-- Custom Budget Input -->
            <div class="p-4 rounded-xl border-2 border-dashed border-slate-300 bg-slate-50/70 hover:bg-slate-50 transition-all flex flex-col sm:flex-row sm:items-center justify-between gap-3.5 sport-custom-budget-container">
              <div class="flex-1">
                <label for="gym-custom-budget-input" class="text-xs font-bold text-slate-800 flex items-center gap-2 cursor-pointer">
                  <span class="text-base">💰</span> <span>Вказати точний максимальний бюджет (грн):</span>
                </label>
                <span class="text-[11px] text-slate-500 block mt-0.5">
                  Введіть вашу бажану суму (наприклад: 3 500 грн) — курс збереться точно за вашим бюджетом.
                </span>
              </div>
              <div class="relative w-full sm:w-44 flex-shrink-0">
                <input 
                  type="number" 
                  id="gym-custom-budget-input" 
                  min="300" 
                  max="50000" 
                  step="50" 
                  placeholder="Напр. 3500" 
                  class="sport-custom-budget-input w-full pl-3.5 pr-10 py-2.5 rounded-xl border border-slate-300 focus:border-blue-600 focus:ring-2 focus:ring-blue-100 font-extrabold text-slate-900 text-sm outline-none bg-white transition-all"
                >
                <span class="absolute right-3.5 top-2.5 text-xs font-bold text-slate-400 pointer-events-none">грн</span>
              </div>
            </div>
          </div>

          <div class="pt-4">
            <button id="other-sport-submit" type="button" class="w-full py-4 px-6 rounded-xl bg-blue-600 hover:bg-blue-700 text-white font-extrabold text-base tracking-wide shadow-lg shadow-blue-600/25 transition-all flex items-center justify-center gap-2">
              <span>Зібрати мій Фітнес-бокс ➔</span>
            </button>
          </div>
        </div>
      `;
    } else if (sport === 'outdoor') {
      container.innerHTML = `
        <div class="space-y-6">
          <div>
            <div class="inline-flex items-center gap-2 px-2.5 py-1 rounded-md bg-blue-50 text-blue-700 text-xs font-semibold border border-blue-200 mb-2">
              <span>🏕️</span> <span>Конфігуратор туристок-боксу (ЇDLO)</span>
            </div>
            <h2 class="text-xl md:text-2xl font-bold font-display text-slate-900 tracking-tight">
              Параметри вашого походу
            </h2>
            <p class="text-sm text-slate-500 mt-1">
              Підбір сублімованих гарячих страв ЇDLO, гідратації, трекінгових шкарпеток та високобілкових джерків.
            </p>
          </div>

          <!-- Q1: Duration -->
          <div class="space-y-2.5">
            <label class="text-xs font-bold text-slate-700 uppercase tracking-wider block">Тривалість походу:</label>
            <div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
              <button type="button" data-field="duration" data-val="1day" class="sport-opt-btn p-3.5 rounded-xl border border-slate-200 bg-white hover:border-blue-400 text-slate-800 text-left transition-all re-shadow-sm">
                <div class="font-bold text-sm text-slate-900">Одноденний хайкінг</div>
                <div class="text-xs text-slate-500 mt-0.5">Легкий вихід на 1 день</div>
              </button>
              <button type="button" data-field="duration" data-val="weekend" class="sport-opt-btn p-3.5 rounded-xl border-2 border-blue-600 bg-blue-50 text-blue-900 ring-2 ring-blue-500/20 text-left transition-all re-shadow-sm">
                <div class="font-bold text-sm text-blue-900">Вихідні (2–3 дні)</div>
                <div class="text-xs text-slate-600 mt-0.5">З ночівлею в наметі</div>
              </button>
              <button type="button" data-field="duration" data-val="expedition" class="sport-opt-btn p-3.5 rounded-xl border border-slate-200 bg-white hover:border-blue-400 text-slate-800 text-left transition-all re-shadow-sm">
                <div class="font-bold text-sm text-slate-900">Автономна експедиція</div>
                <div class="text-xs text-slate-500 mt-0.5">4+ днів у горах</div>
              </button>
            </div>
          </div>

          <!-- Q2: Price Tier & Custom Budget -->
          <div class="space-y-3">
            <div class="flex items-center justify-between">
              <label class="text-xs font-bold text-slate-700 uppercase tracking-wider block">Ціновий сегмент або точний бюджет:</label>
              <span class="text-[11px] text-slate-500">Оберіть категорію або вкажіть суму</span>
            </div>
            <div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
              <button type="button" data-field="price_tier" data-val="economy" class="sport-opt-btn p-3.5 rounded-xl border border-slate-200 bg-white hover:border-blue-400 text-left transition-all re-shadow-sm cursor-pointer">
                <div class="flex items-center justify-between">
                  <span class="font-bold text-xs text-emerald-600 block">🟢 Економ</span>
                  <span class="text-[11px] font-extrabold text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded-md border border-emerald-200">до 2 500–3 000 ₴</span>
                </div>
                <div class="text-[11px] text-slate-500 mt-1">Базовий раціон ЇDLO</div>
              </button>
              <button type="button" data-field="price_tier" data-val="standard" class="sport-opt-btn p-3.5 rounded-xl border-2 border-blue-600 bg-blue-50 text-blue-900 ring-2 ring-blue-500/20 text-left transition-all re-shadow-sm cursor-pointer">
                <div class="flex items-center justify-between">
                  <span class="font-bold text-xs text-blue-900 block">🔵 Оптимальний</span>
                  <span class="text-[11px] font-extrabold text-blue-700 bg-blue-100/60 px-2 py-0.5 rounded-md border border-blue-200">до 3 800–4 200 ₴</span>
                </div>
                <div class="text-[11px] text-slate-600 mt-1">Повне меню + джерки</div>
              </button>
              <button type="button" data-field="price_tier" data-val="premium" class="sport-opt-btn p-3.5 rounded-xl border border-slate-200 bg-white hover:border-blue-400 text-left transition-all re-shadow-sm cursor-pointer">
                <div class="flex items-center justify-between">
                  <span class="font-bold text-xs text-purple-700 block">🟣 PRO Експедиція</span>
                  <span class="text-[11px] font-extrabold text-purple-700 bg-purple-50 px-2 py-0.5 rounded-md border border-purple-200">від 6 500–8 000+ ₴</span>
                </div>
                <div class="text-[11px] text-slate-500 mt-1">Преміум набір + спорядження</div>
              </button>
            </div>

            <!-- Custom Budget Input -->
            <div class="p-4 rounded-xl border-2 border-dashed border-slate-300 bg-slate-50/70 hover:bg-slate-50 transition-all flex flex-col sm:flex-row sm:items-center justify-between gap-3.5 sport-custom-budget-container">
              <div class="flex-1">
                <label for="outdoor-custom-budget-input" class="text-xs font-bold text-slate-800 flex items-center gap-2 cursor-pointer">
                  <span class="text-base">💰</span> <span>Вказати точний максимальний бюджет (грн):</span>
                </label>
                <span class="text-[11px] text-slate-500 block mt-0.5">
                  Введіть вашу бажану суму (наприклад: 3 000 грн) — набір підбереться збалансовано.
                </span>
              </div>
              <div class="relative w-full sm:w-44 flex-shrink-0">
                <input 
                  type="number" 
                  id="outdoor-custom-budget-input" 
                  min="300" 
                  max="50000" 
                  step="50" 
                  placeholder="Напр. 3000" 
                  class="sport-custom-budget-input w-full pl-3.5 pr-10 py-2.5 rounded-xl border border-slate-300 focus:border-blue-600 focus:ring-2 focus:ring-blue-100 font-extrabold text-slate-900 text-sm outline-none bg-white transition-all"
                >
                <span class="absolute right-3.5 top-2.5 text-xs font-bold text-slate-400 pointer-events-none">грн</span>
              </div>
            </div>
          </div>

          <div class="pt-4">
            <button id="other-sport-submit" type="button" class="w-full py-4 px-6 rounded-xl bg-blue-600 hover:bg-blue-700 text-white font-extrabold text-base tracking-wide shadow-lg shadow-blue-600/25 transition-all flex items-center justify-center gap-2">
              <span>Зібрати мій Туристичний бокс ➔</span>
            </button>
          </div>
        </div>
      `;
    }

    // Attach click listeners for option buttons in dynamic form
    container.querySelectorAll('.sport-opt-btn').forEach((btn) => {
      btn.addEventListener('click', () => {
        const field = btn.dataset.field;
        const val = btn.dataset.val === 'true' ? true : (btn.dataset.val === 'false' ? false : btn.dataset.val);
        state.sportAnswers[sport][field] = val;

        // If clicking price_tier button, clear any custom budget input
        if (field === 'price_tier') {
          delete state.sportAnswers[sport].custom_budget;
          const customInp = container.querySelector('.sport-custom-budget-input');
          if (customInp) customInp.value = '';
          const budgetBox = container.querySelector('.sport-custom-budget-container');
          if (budgetBox) {
            budgetBox.classList.remove('border-blue-600', 'bg-blue-50/50');
            budgetBox.classList.add('border-slate-300', 'bg-slate-50/70');
          }
        }

        // Visual toggle in group
        const parent = btn.parentElement;
        parent.querySelectorAll('.sport-opt-btn').forEach((b) => {
          b.className = 'sport-opt-btn p-3.5 rounded-xl border border-slate-200 bg-white hover:border-blue-400 text-left transition-all re-shadow-sm cursor-pointer';
        });
        btn.className = 'sport-opt-btn p-3.5 rounded-xl border-2 border-blue-600 bg-blue-50 text-blue-900 ring-2 ring-blue-500/20 text-left transition-all re-shadow-sm cursor-pointer';
      });
    });

    // Custom budget listener
    const sportBudgetInput = container.querySelector('.sport-custom-budget-input');
    if (sportBudgetInput) {
      sportBudgetInput.addEventListener('input', () => {
        const val = parseFloat(sportBudgetInput.value);
        const budgetBox = container.querySelector('.sport-custom-budget-container');
        if (!isNaN(val) && val > 0) {
          state.sportAnswers[sport].custom_budget = val;
          // Unhighlight preset tier buttons in this sport
          container.querySelectorAll('[data-field="price_tier"]').forEach((b) => {
            b.className = 'sport-opt-btn p-3.5 rounded-xl border border-slate-200 bg-white hover:border-blue-400 text-left transition-all re-shadow-sm cursor-pointer';
          });
          if (budgetBox) {
            budgetBox.classList.add('border-blue-600', 'bg-blue-50/50');
            budgetBox.classList.remove('border-slate-300', 'bg-slate-50/70');
          }
        } else {
          delete state.sportAnswers[sport].custom_budget;
          if (budgetBox) {
            budgetBox.classList.remove('border-blue-600', 'bg-blue-50/50');
            budgetBox.classList.add('border-slate-300', 'bg-slate-50/70');
          }
        }
      });
    }

    // Attach submit listener
    const submitBtn = el('other-sport-submit');
    if (submitBtn) {
      submitBtn.addEventListener('click', () => {
        generateBoxForSport(sport);
      });
    }
  }

  // Stepper UI Update (for Running)
  function updateStepperUI() {
    if (state.sport !== 'running') return;
    const stepEl = el('stepper-container');
    if (!stepEl) return;

    const progressPercent = Math.round((state.currentStep / state.totalSteps) * 100);
    const progressBar = el('stepper-progress-bar');
    if (progressBar) {
      progressBar.style.width = `${progressPercent}%`;
    }

    const stepCounter = el('stepper-counter');
    if (stepCounter) {
      stepCounter.textContent = `Крок ${state.currentStep} з ${state.totalSteps}`;
    }

    for (let i = 1; i <= state.totalSteps; i++) {
      const qCard = el(`step-${i}`);
      if (qCard) {
        if (i === state.currentStep) {
          qCard.classList.remove('hidden');
          qCard.classList.add('flex');
        } else {
          qCard.classList.add('hidden');
          qCard.classList.remove('flex');
        }
      }
    }

    const backBtn = el('quiz-back-btn');
    if (backBtn) {
      if (state.currentStep > 1) {
        backBtn.classList.remove('invisible', 'opacity-0');
        backBtn.classList.add('visible', 'opacity-100');
      } else {
        backBtn.classList.add('invisible', 'opacity-0');
        backBtn.classList.remove('visible', 'opacity-100');
      }
    }
  }

  // Question Listeners (Running)
  function setupRunningStepListeners() {
    document.querySelectorAll('[data-q="distance"]').forEach((btn) => {
      btn.addEventListener('click', () => {
        const val = btn.dataset.val;
        state.answers.distance = val;
        updateRunningPriceBadges(val);
        highlightActiveRadio('distance', val);
        advanceStep();
      });
    });

    document.querySelectorAll('[data-q="pace_target"]').forEach((btn) => {
      btn.addEventListener('click', () => {
        const val = btn.dataset.val;
        state.answers.pace_target = val;
        highlightActiveRadio('pace_target', val);
        advanceStep();
      });
    });

    document.querySelectorAll('[data-q="weather"]').forEach((btn) => {
      btn.addEventListener('click', () => {
        const val = btn.dataset.val;
        state.answers.weather = val;
        highlightActiveRadio('weather', val);
        advanceStep();
      });
    });

    document.querySelectorAll('[data-q="stomach_type"]').forEach((btn) => {
      btn.addEventListener('click', () => {
        const val = btn.dataset.val;
        state.answers.stomach_type = val;
        highlightActiveRadio('stomach_type', val);
        advanceStep();
      });
    });

    document.querySelectorAll('[data-q="caffeine_preference"]').forEach((btn) => {
      btn.addEventListener('click', () => {
        const val = btn.dataset.val;
        state.answers.caffeine_preference = val;
        highlightActiveRadio('caffeine_preference', val);
        advanceStep();
      });
    });

    // Step 6 continue button
    const step6Btn = el('step-6-continue-btn');
    if (step6Btn) {
      step6Btn.addEventListener('click', () => {
        const selectedConcerns = [];
        document.querySelectorAll('input[name="body_concern"]:checked').forEach((ch) => {
          selectedConcerns.push(ch.value);
        });
        state.answers.body_concerns = selectedConcerns;
        advanceStep();
      });
    }

    document.querySelectorAll('[data-q="price_tier"]').forEach((btn) => {
      btn.addEventListener('click', () => {
        const val = btn.dataset.val;
        state.answers.price_tier = val;
        delete state.answers.custom_budget;
        const runningBudgetInput = el('running-custom-budget-input');
        if (runningBudgetInput) runningBudgetInput.value = '';
        const budgetBox = el('running-custom-budget-container');
        if (budgetBox) {
          budgetBox.classList.remove('border-blue-600', 'bg-blue-50/50');
          budgetBox.classList.add('border-slate-300', 'bg-slate-50/70');
        }
        highlightActiveRadio('price_tier', val);
      });
    });

    const runningBudgetInput = el('running-custom-budget-input');
    if (runningBudgetInput) {
      runningBudgetInput.addEventListener('input', () => {
        const val = parseFloat(runningBudgetInput.value);
        const budgetBox = el('running-custom-budget-container');
        if (!isNaN(val) && val > 0) {
          state.answers.custom_budget = val;
          // Unhighlight preset tier buttons in running
          document.querySelectorAll('[data-q="price_tier"]').forEach((b) => {
            b.className = 'p-3.5 rounded-xl border border-slate-200 bg-white hover:border-blue-400 text-left transition-all re-shadow-sm cursor-pointer';
          });
          if (budgetBox) {
            budgetBox.classList.add('border-blue-600', 'bg-blue-50/50');
            budgetBox.classList.remove('border-slate-300', 'bg-slate-50/70');
          }
        } else {
          delete state.answers.custom_budget;
          if (budgetBox) {
            budgetBox.classList.remove('border-blue-600', 'bg-blue-50/50');
            budgetBox.classList.add('border-slate-300', 'bg-slate-50/70');
          }
        }
      });
    }

    const backBtn = el('quiz-back-btn');
    if (backBtn) {
      backBtn.addEventListener('click', () => {
        if (state.currentStep > 1) {
          state.currentStep--;
          updateStepperUI();
        }
      });
    }

    const step7Submit = el('step-7-submit');
    if (step7Submit) {
      step7Submit.addEventListener('click', () => {
        const selectedGears = [];
        document.querySelectorAll('input[name="gear"]:checked').forEach((ch) => {
          selectedGears.push(ch.value);
        });
        state.answers.gear_needed = selectedGears;
        generateBoxForSport('running');
      });
    }
  }

  function highlightActiveRadio(field, activeVal) {
    document.querySelectorAll(`[data-q="${field}"]`).forEach((btn) => {
      if (btn.dataset.val === activeVal) {
        btn.classList.add('border-2', 'border-blue-600', 'bg-blue-50', 'text-blue-900', 'ring-2', 'ring-blue-500/20');
        btn.classList.remove('border', 'border-slate-200', 'bg-white', 'text-slate-800');
      } else {
        btn.classList.remove('border-2', 'border-blue-600', 'bg-blue-50', 'text-blue-900', 'ring-2', 'ring-blue-500/20');
        btn.classList.add('border', 'border-slate-200', 'bg-white', 'text-slate-800');
      }
    });
  }

  function advanceStep() {
    if (state.currentStep < state.totalSteps) {
      state.currentStep++;
      updateStepperUI();
    }
  }

  function attachGlobalActions() {
    const restartBtns = document.querySelectorAll('.restart-quiz-btn');
    restartBtns.forEach((btn) => {
      btn.addEventListener('click', () => {
        state.currentStep = 1;
        state.boxData = null;
        state.selectedItems = {};
        state.variantSelections = {};
        state.swapIndex = {};
        state.customSelections = {};
        el('result-container')?.classList.add('hidden');
        el('stepper-container')?.classList.remove('hidden');
        setSport(state.sport);
        window.scrollTo({ top: 0, behavior: 'smooth' });
      });
    });
  }

  // Backward-compatible alias for running box generator
  const generateRunnerBox = () => generateBoxForSport('running');

  // API Call to generate sport box
  async function generateBoxForSport(sport) {
    const activeBtn = (sport === 'running') ? el('step-7-submit') : el('other-sport-submit');
    const originalText = activeBtn ? activeBtn.innerHTML : '';
    if (activeBtn) {
      activeBtn.disabled = true;
      activeBtn.innerHTML = `
        <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white inline-block" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z"></path>
        </svg>
        Формуємо ваш бокс...
      `;
    }

    const payload = (sport === 'running') 
      ? { sport: 'running', ...state.answers }
      : { sport: sport, ...state.sportAnswers[sport] };

    try {
      const res = await fetch('/api/generate-sport-box', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });

      if (!res.ok) {
        throw new Error(`Помилка сервера: ${res.status}`);
      }

      const data = await res.json();
      state.boxData = data;
      renderResultScreen(data, sport);
    } catch (err) {
      console.error('Error generating sport box:', err);
      alert(`Не вдалося сформувати бокс: ${err.message}. Будь ласка, спробуйте ще раз.`);
    } finally {
      if (activeBtn) {
        activeBtn.disabled = false;
        activeBtn.innerHTML = originalText;
      }
    }
  }

  // Render Result Screen
  function renderResultScreen(box, sport) {
    el('stepper-container')?.classList.add('hidden');
    const resultContainer = el('result-container');
    if (!resultContainer) return;
    resultContainer.classList.remove('hidden');

    const titleEl = el('box-distance-title');
    if (titleEl) {
      titleEl.textContent = box.box_title || `Стартовий бокс: ${box.distance_label}`;
    }

    const budgetBadge = el('box-budget-badge');
    if (budgetBadge) {
      if (box.budget_info) {
        budgetBadge.classList.remove('hidden');
        if (box.budget_info.type === 'custom') {
          const customB = Math.round(box.budget_info.custom_budget);
          const totalP = Math.round(box.total_base_price);
          const savings = Math.round(box.budget_info.savings || 0);
          budgetBadge.innerHTML = `
            <span>🎯 Ваш бюджет: <strong class="text-blue-950 font-bold">${customB} грн</strong></span>
            <span class="text-slate-300">•</span>
            <span>Підібрано на суму: <strong class="text-blue-950 font-bold">${totalP} грн</strong></span>
            ${savings > 0 ? `<span class="bg-emerald-100 text-emerald-800 text-[11px] font-extrabold px-2 py-0.5 rounded border border-emerald-200">Економія: ${savings} грн</span>` : '<span class="bg-emerald-100 text-emerald-800 text-[11px] font-extrabold px-2 py-0.5 rounded border border-emerald-200">✓ В межах бюджету</span>'}
          `;
        } else {
          const tierLabel = box.budget_info.tier === 'economy' 
            ? '🟢 Економ' 
            : (box.budget_info.tier === 'premium' ? '🟣 PRO / Еліта' : '🔵 Оптимальний');
          budgetBadge.innerHTML = `
            <span>Цінова категорія: <strong class="text-blue-950 font-bold">${tierLabel}</strong></span>
            <span class="text-slate-300">•</span>
            <span>Базова сума: <strong class="text-blue-950 font-bold">${Math.round(box.total_base_price)} грн</strong></span>
          `;
        }
      } else {
        budgetBadge.classList.add('hidden');
      }
    }

    state.selectedItems = {};
    state.variantSelections = {};
    state.swapIndex = {};
    state.customSelections = {};

    const slotsGrid = el('slots-container');
    if (!slotsGrid) return;
    slotsGrid.innerHTML = '';

    // Order items management banner with Select All / Deselect All
    const helperCard = document.createElement('div');
    helperCard.className = 'bg-blue-50/80 border border-blue-200/90 rounded-2xl p-4 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 mb-5 re-shadow-sm';
    helperCard.innerHTML = `
      <div class="flex items-center gap-2.5">
        <span class="text-2xl">🛒</span>
        <div>
          <h4 class="text-xs font-bold text-slate-900 uppercase tracking-wider">Формування вашого замовлення</h4>
          <p class="text-xs text-slate-600">Зніміть галочку з будь-якого товару, якщо він у вас вже є або ви не бажаєте його замовляти.</p>
        </div>
      </div>
      <div class="flex items-center gap-2 w-full sm:w-auto flex-shrink-0">
        <button type="button" id="select-all-items-btn" class="text-xs font-bold px-3 py-1.5 rounded-lg bg-white border border-slate-200 text-blue-700 hover:bg-blue-50 hover:border-blue-400 transition-all shadow-sm cursor-pointer">
          ✓ Обрати всі
        </button>
        <button type="button" id="deselect-all-items-btn" class="text-xs font-bold px-3 py-1.5 rounded-lg bg-white border border-slate-200 text-slate-600 hover:text-rose-600 hover:bg-rose-50 hover:border-rose-300 transition-all shadow-sm cursor-pointer">
          ✕ Зняти всі
        </button>
      </div>
    `;
    slotsGrid.appendChild(helperCard);

    const slotMetaList = SPORT_SLOT_META[sport] || SPORT_SLOT_META['running'];

    slotMetaList.forEach((slotMeta) => {
      const items = box.slots[slotMeta.key] || [];
      if (items.length === 0) return;

      const slotSection = document.createElement('section');
      slotSection.className = 'bg-white border border-slate-200 rounded-2xl p-5 md:p-6 re-shadow-sm mb-5';
      
      let itemsHtml = '';
      items.forEach((item, index) => {
        const itemKey = `${slotMeta.key}_${index}`;
        state.selectedItems[itemKey] = item.checked_by_default;

        if (item.available_sizes && item.available_sizes.length > 0) {
          state.variantSelections[itemKey] = item.available_sizes[1]?.product_id || item.available_sizes[0].product_id;
        }

        const product = item.product;
        const itemTotal = (product.price * item.quantity_recommended).toFixed(0);

        let sizeSelectorHtml = '';
        if (item.available_sizes && item.available_sizes.length > 0) {
          const selectedId = state.variantSelections[itemKey];
          const pills = item.available_sizes.map((s) => {
            const isPillActive = s.product_id === selectedId;
            return `
              <button type="button" data-item-key="${itemKey}" data-product-id="${s.product_id}" class="size-pill text-xs font-semibold px-2.5 py-1 rounded-md border transition-all ${
                isPillActive 
                  ? 'border-blue-600 bg-blue-600 text-white font-bold shadow-sm' 
                  : 'border-slate-200 bg-white text-slate-700 hover:border-blue-400 hover:bg-slate-50'
              }">
                ${s.size}
              </button>
            `;
          }).join('');

          sizeSelectorHtml = `
            <div class="mt-2.5 pt-2.5 border-t border-slate-100 flex items-center gap-2">
              <span class="text-[11px] font-semibold text-slate-500 uppercase tracking-wider">Розмір:</span>
              <div class="flex items-center gap-1.5 flex-wrap">${pills}</div>
            </div>
          `;
        }

        const hasAlts = item.alternatives && item.alternatives.length > 0;
        const swapBtnHtml = hasAlts ? `
          <button type="button" data-item-key="${itemKey}" class="swap-item-btn text-[11px] font-semibold text-slate-600 hover:text-blue-600 hover:bg-blue-50 transition-colors flex items-center gap-1.5 px-2.5 py-1 rounded-md bg-white border border-slate-200 shadow-sm cursor-pointer">
            <span>🔀 Замінити смак / бренд</span>
          </button>
        ` : '';

        const isChecked = item.checked_by_default;
        itemsHtml += `
          <div class="item-card p-4 rounded-xl border border-slate-200 ${isChecked ? 'bg-slate-50/70 hover:bg-white' : 'opacity-50 bg-slate-100/60'} hover:border-blue-400 transition-all flex flex-col gap-3 re-shadow-sm">
            <div class="flex items-start justify-between gap-3">
              <div class="flex items-start gap-3.5 flex-1 min-w-0">
                <label class="item-checkbox-label cursor-pointer flex flex-col items-center gap-1.5 pt-1 select-none group" title="Натисніть, щоб додати або прибрати цей товар з кошика">
                  <input type="checkbox" data-item-key="${itemKey}" class="item-checkbox sr-only" ${isChecked ? 'checked' : ''}>
                  <div class="item-checkbox-box w-6 h-6 rounded-lg border flex items-center justify-center transition-all ${
                    isChecked
                      ? 'border-blue-600 bg-blue-600 text-white shadow-sm shadow-blue-600/20'
                      : 'border-slate-300 bg-white text-transparent group-hover:border-slate-400'
                  }">
                    <svg class="w-4 h-4 fill-current" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"></path></svg>
                  </div>
                  <span class="item-check-badge text-[10px] font-bold px-1.5 py-0.5 rounded border transition-all text-center whitespace-nowrap ${
                    isChecked
                      ? 'bg-blue-50 text-blue-700 border-blue-200'
                      : 'bg-slate-100 text-slate-400 border-slate-200'
                  }">
                    ${isChecked ? 'В кошик' : 'Не додавати'}
                  </span>
                </label>

                <div class="w-16 h-16 rounded-xl bg-white border border-slate-200 flex-shrink-0 overflow-hidden flex items-center justify-center p-1">
                  <img src="${product.image}" alt="${product.name}" class="max-w-full max-h-full object-contain" onerror="this.src='https://placehold.co/100x100/f8fafc/64748b?text=RE'">
                </div>

                <div class="flex-1 min-w-0">
                  <div class="flex items-center gap-2 flex-wrap mb-1">
                    <span class="text-xs text-slate-500 font-semibold uppercase tracking-wider">${product.brand || 'Race Expert'}</span>
                    <span class="text-[10px] font-semibold px-2 py-0.5 rounded-full bg-blue-50 text-blue-700 border border-blue-200">${item.reason_badge}</span>
                  </div>
                  <h4 class="text-sm font-bold text-slate-900 leading-snug line-clamp-2">
                    <a href="${product.url}" target="_blank" class="hover:text-blue-600 transition-colors">${product.name}</a>
                  </h4>
                  <p class="text-xs text-amber-700 mt-1 flex items-center gap-1.5 font-medium">
                    <span class="inline-block w-1.5 h-1.5 rounded-full bg-amber-500"></span>
                    <span>${item.timing_instruction}</span>
                  </p>
                </div>
              </div>

              <div class="text-right flex-shrink-0">
                <div class="item-price-display text-base font-bold font-display ${isChecked ? 'text-blue-700' : 'line-through text-slate-400'}">${itemTotal} грн</div>
                <div class="text-[11px] text-slate-500 font-medium">${item.quantity_recommended} шт × ${product.price} грн</div>
              </div>
            </div>

            <div class="flex items-center justify-between pt-1">
              ${sizeSelectorHtml}
              <div class="ml-auto">${swapBtnHtml}</div>
            </div>
          </div>
        `;
      });

      slotSection.innerHTML = `
        <div class="flex items-center justify-between pb-3 mb-4 border-b border-slate-100">
          <div class="flex items-center gap-2.5">
            <span class="text-2xl">${slotMeta.icon}</span>
            <div>
              <h3 class="text-base font-bold font-display text-slate-900">${slotMeta.title}</h3>
              <p class="text-xs text-slate-500">${slotMeta.desc}</p>
            </div>
          </div>
          <span class="text-xs font-semibold px-2.5 py-1 rounded-full bg-slate-100 text-slate-700 border border-slate-200">
            ${items.length} ${items.length === 1 ? 'позиція' : (items.length < 5 ? 'позиції' : 'позицій')}
          </span>
        </div>
        <div class="space-y-3">${itemsHtml}</div>
      `;

      slotsGrid.appendChild(slotSection);
    });

    updateLiveTotal();
    attachResultInteractions();

    const userInputs = (sport === 'running') ? state.answers : state.sportAnswers[sport];
    fetchLunaConsultation(userInputs, box);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  // Call Luna AI Consultant
  async function fetchLunaConsultation(inputs, boxData) {
    const loadingEl = el('luna-loading');
    const contentEl = el('luna-content');
    if (loadingEl) loadingEl.classList.remove('hidden');
    if (contentEl) contentEl.classList.add('hidden');

    try {
      const res = await fetch('/api/luna-consult-box', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          user_inputs: inputs,
          generated_box: boxData,
          locale: 'uk'
        })
      });

      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const payload = await res.json();
      if (!payload.ok || !payload.data) throw new Error('Invalid response');

      const data = payload.data;
      if (el('luna-safety-badge')) el('luna-safety-badge').textContent = data.safety_badge || '100% сумісність';
      if (el('luna-verdict')) el('luna-verdict').textContent = data.expert_verdict || '';
      if (el('luna-strategy')) el('luna-strategy').textContent = data.tactical_strategy || '';
      if (el('luna-pro-tip')) el('luna-pro-tip').textContent = data.pro_tip || '';

      const timelineList = el('luna-timeline-list');
      if (timelineList && data.timeline_steps) {
        timelineList.innerHTML = data.timeline_steps.map((st) => `
          <div class="p-2.5 rounded-lg bg-white border border-blue-100 flex items-start gap-2.5 re-shadow-sm">
            <span class="text-[11px] font-bold text-blue-700 bg-blue-50 border border-blue-200 px-2 py-0.5 rounded flex-shrink-0">${st.timing}</span>
            <div class="text-[11px] text-slate-700">
              <span class="font-semibold text-slate-900">${st.product_name ? st.product_name + ': ' : ''}</span>
              ${st.instruction}
            </div>
          </div>
        `).join('');
      }

      if (loadingEl) loadingEl.classList.add('hidden');
      if (contentEl) contentEl.classList.remove('hidden');
    } catch (err) {
      console.warn('Luna consultation fetch failed:', err);
      if (loadingEl) loadingEl.classList.add('hidden');
    }
  }

  // Handle Result Interactions (Checkboxes, Swaps, Sizes)
  function attachResultInteractions() {
    document.querySelectorAll('.item-checkbox').forEach((checkbox) => {
      checkbox.addEventListener('change', (e) => {
        const key = checkbox.dataset.itemKey;
        const isChecked = checkbox.checked;
        state.selectedItems[key] = isChecked;

        const label = checkbox.closest('label');
        if (label) {
          const box = label.querySelector('.item-checkbox-box');
          if (box) {
            if (isChecked) {
              box.className = 'item-checkbox-box w-6 h-6 rounded-lg border flex items-center justify-center transition-all border-blue-600 bg-blue-600 text-white shadow-sm shadow-blue-600/20';
            } else {
              box.className = 'item-checkbox-box w-6 h-6 rounded-lg border flex items-center justify-center transition-all border-slate-300 bg-white text-transparent group-hover:border-slate-400';
            }
          }
          const badge = label.querySelector('.item-check-badge');
          if (badge) {
            if (isChecked) {
              badge.className = 'item-check-badge text-[10px] font-bold px-1.5 py-0.5 rounded border transition-all text-center whitespace-nowrap bg-blue-50 text-blue-700 border-blue-200';
              badge.textContent = 'В кошик';
            } else {
              badge.className = 'item-check-badge text-[10px] font-bold px-1.5 py-0.5 rounded border transition-all text-center whitespace-nowrap bg-slate-100 text-slate-400 border-slate-200';
              badge.textContent = 'Не додавати';
            }
          }
        }

        const card = checkbox.closest('.item-card');
        if (card) {
          const priceDiv = card.querySelector('.item-price-display');
          if (isChecked) {
            card.classList.remove('opacity-50', 'bg-slate-100/60');
            card.classList.add('bg-slate-50/70', 'hover:bg-white');
            if (priceDiv) {
              priceDiv.classList.remove('line-through', 'text-slate-400');
              priceDiv.classList.add('text-blue-700');
            }
          } else {
            card.classList.remove('bg-slate-50/70', 'hover:bg-white');
            card.classList.add('opacity-50', 'bg-slate-100/60');
            if (priceDiv) {
              priceDiv.classList.remove('text-blue-700');
              priceDiv.classList.add('line-through', 'text-slate-400');
            }
          }
        }

        updateLiveTotal();
      });
    });

    // Select All / Deselect All Controls
    const selectAllBtn = el('select-all-items-btn');
    if (selectAllBtn) {
      selectAllBtn.onclick = () => {
        document.querySelectorAll('.item-checkbox').forEach((cb) => {
          if (!cb.checked) {
            cb.checked = true;
            cb.dispatchEvent(new Event('change'));
          }
        });
      };
    }

    const deselectAllBtn = el('deselect-all-items-btn');
    if (deselectAllBtn) {
      deselectAllBtn.onclick = () => {
        document.querySelectorAll('.item-checkbox').forEach((cb) => {
          if (cb.checked) {
            cb.checked = false;
            cb.dispatchEvent(new Event('change'));
          }
        });
      };
    }

    document.querySelectorAll('.size-pill').forEach((pill) => {
      pill.addEventListener('click', () => {
        const key = pill.dataset.itemKey;
        const productId = parseInt(pill.dataset.productId, 10);
        state.variantSelections[key] = productId;

        pill.parentElement.querySelectorAll('.size-pill').forEach((p) => {
          p.className = 'size-pill text-xs font-semibold px-2.5 py-1 rounded-md border transition-all border-slate-200 bg-white text-slate-700 hover:border-blue-400 hover:bg-slate-50';
        });
        pill.className = 'size-pill text-xs font-semibold px-2.5 py-1 rounded-md border transition-all border-blue-600 bg-blue-600 text-white font-bold shadow-sm';
      });
    });

    // Swap item button (cycle through alternative flavors/brands)
    document.querySelectorAll('.swap-item-btn').forEach((btn) => {
      btn.addEventListener('click', () => {
        const key = btn.dataset.itemKey;
        const [slot, idxStr] = key.split('_');
        const idx = parseInt(idxStr, 10);
        const item = state.boxData.slots[slot][idx];
        if (!item || !item.alternatives || item.alternatives.length === 0) return;

        state.swapIndex[key] = state.swapIndex[key] || 0;
        const currentAltIdx = state.swapIndex[key];
        const allOptions = [item.product, ...item.alternatives];
        const nextAltIdx = (currentAltIdx + 1) % allOptions.length;
        state.swapIndex[key] = nextAltIdx;

        const newProduct = allOptions[nextAltIdx];
        state.customSelections[key] = newProduct;

        const card = btn.closest('.item-card');
        if (card) {
          const img = card.querySelector('img');
          if (img) img.src = newProduct.image;
          const titleLink = card.querySelector('h4 a');
          if (titleLink) {
            titleLink.textContent = newProduct.name;
            titleLink.href = newProduct.url || '#';
          }
          const brandSpan = card.querySelector('span.text-xs');
          if (brandSpan) brandSpan.textContent = (newProduct.brand || 'Race Expert').toUpperCase();
          
          const priceDiv = card.querySelector('.item-price-display');
          if (priceDiv) {
            priceDiv.textContent = `${Math.round(newProduct.price * item.quantity_recommended)} грн`;
          }
          const priceDetail = card.querySelector('.text-\\[11px\\]');
          if (priceDetail) {
            priceDetail.textContent = `${item.quantity_recommended} шт × ${newProduct.price} грн`;
          }
        }

        updateLiveTotal();
      });
    });

    const buyBtn = el('buy-box-btn');
    if (buyBtn) {
      buyBtn.onclick = handleBuyBoxClick;
    }

    const heroBuyBtn = el('hero-buy-box-btn');
    if (heroBuyBtn) {
      heroBuyBtn.onclick = handleBuyBoxClick;
    }
  }

  // Recalculate Live Total
  function updateLiveTotal() {
    if (!state.boxData) return;

    let totalPrice = 0;
    let selectedCount = 0;
    let totalItemsCount = 0;

    const slotNames = ['energy', 'hydration', 'gear', 'care_recovery'];
    slotNames.forEach((slot) => {
      const items = state.boxData.slots[slot] || [];
      items.forEach((item, idx) => {
        totalItemsCount++;
        const key = `${slot}_${idx}`;
        if (state.selectedItems[key]) {
          const activeProduct = state.customSelections[key] || item.product;
          totalPrice += activeProduct.price * item.quantity_recommended;
          selectedCount++;
        }
      });
    });

    const totalDisplay = el('total-box-price');
    if (totalDisplay) {
      totalDisplay.textContent = `${Math.round(totalPrice)} грн`;
    }

    const heroPrice = el('hero-box-price');
    if (heroPrice) {
      heroPrice.textContent = `${Math.round(totalPrice)} грн`;
    }

    const countDisplay = el('selected-items-count');
    if (countDisplay) {
      countDisplay.textContent = `${selectedCount} з ${totalItemsCount} ${totalItemsCount === 1 ? 'позиції' : (totalItemsCount < 5 ? 'позицій' : 'позицій')}`;
    }

    const buyBtn = el('buy-box-btn');
    if (buyBtn && !state.isCheckingOut) {
      if (selectedCount === 0) {
        buyBtn.disabled = true;
        buyBtn.innerHTML = `<span>Оберіть хоча б 1 товар для покупки</span>`;
        buyBtn.className = 'py-3.5 px-6 sm:px-8 rounded-xl bg-slate-300 text-slate-500 font-extrabold text-sm sm:text-base tracking-wide cursor-not-allowed transition-all flex items-center justify-center gap-2';
      } else if (selectedCount === totalItemsCount) {
        buyBtn.disabled = false;
        buyBtn.innerHTML = `
          <svg class="w-5 h-5 fill-current" viewBox="0 0 20 20"><path d="M3 1a1 1 0 000 2h1.22l.305 1.222a.997.997 0 00.01.042l1.358 5.43-.893.892C3.74 11.846 4.632 14 6.414 14H15a1 1 0 000-2H6.414l1-1H14a1 1 0 00.894-.553l3-6A1 1 0 0017 3H6.28l-.31-1.243A1 1 0 005 1H3zM16 16.5a1.5 1.5 0 11-3 0 1.5 1.5 0 013 0zM6.5 18a1.5 1.5 0 100-3 1.5 1.5 0 000 3z"></path></svg>
          <span>Купити весь бокс (${selectedCount} шт • ${Math.round(totalPrice)} грн)</span>
        `;
        buyBtn.className = 'py-3.5 px-6 sm:px-8 rounded-xl bg-blue-600 hover:bg-blue-700 text-white font-extrabold text-sm sm:text-base tracking-wide shadow-lg shadow-blue-600/25 transition-all flex items-center justify-center gap-2 cursor-pointer';
      } else {
        buyBtn.disabled = false;
        buyBtn.innerHTML = `
          <svg class="w-5 h-5 fill-current" viewBox="0 0 20 20"><path d="M3 1a1 1 0 000 2h1.22l.305 1.222a.997.997 0 00.01.042l1.358 5.43-.893.892C3.74 11.846 4.632 14 6.414 14H15a1 1 0 000-2H6.414l1-1H14a1 1 0 00.894-.553l3-6A1 1 0 0017 3H6.28l-.31-1.243A1 1 0 005 1H3zM16 16.5a1.5 1.5 0 11-3 0 1.5 1.5 0 013 0zM6.5 18a1.5 1.5 0 100-3 1.5 1.5 0 000 3z"></path></svg>
          <span>Купити обрані (${selectedCount} з ${totalItemsCount} • ${Math.round(totalPrice)} грн)</span>
        `;
        buyBtn.className = 'py-3.5 px-6 sm:px-8 rounded-xl bg-blue-600 hover:bg-blue-700 text-white font-extrabold text-sm sm:text-base tracking-wide shadow-lg shadow-blue-600/25 transition-all flex items-center justify-center gap-2 cursor-pointer';
      }
    }

    const heroBuyBtn = el('hero-buy-box-btn');
    if (heroBuyBtn && !state.isCheckingOut) {
      if (selectedCount === 0) {
        heroBuyBtn.disabled = true;
        heroBuyBtn.innerHTML = `<span>Оберіть хоча б 1 товар</span>`;
        heroBuyBtn.className = 'py-3 px-5 rounded-xl bg-slate-300 text-slate-500 font-extrabold text-xs sm:text-sm tracking-wide cursor-not-allowed transition-all flex items-center justify-center gap-1.5';
      } else if (selectedCount === totalItemsCount) {
        heroBuyBtn.disabled = false;
        heroBuyBtn.innerHTML = `
          <svg class="w-4 h-4 fill-current" viewBox="0 0 20 20"><path d="M3 1a1 1 0 000 2h1.22l.305 1.222a.997.997 0 00.01.042l1.358 5.43-.893.892C3.74 11.846 4.632 14 6.414 14H15a1 1 0 000-2H6.414l1-1H14a1 1 0 00.894-.553l3-6A1 1 0 0017 3H6.28l-.31-1.243A1 1 0 005 1H3zM16 16.5a1.5 1.5 0 11-3 0 1.5 1.5 0 013 0zM6.5 18a1.5 1.5 0 100-3 1.5 1.5 0 000 3z"></path></svg>
          <span>Купити весь бокс</span>
        `;
        heroBuyBtn.className = 'py-3 px-5 rounded-xl bg-blue-600 hover:bg-blue-700 text-white font-extrabold text-xs sm:text-sm tracking-wide shadow-md shadow-blue-600/25 transition-all flex items-center justify-center gap-1.5 cursor-pointer';
      } else {
        heroBuyBtn.disabled = false;
        heroBuyBtn.innerHTML = `
          <svg class="w-4 h-4 fill-current" viewBox="0 0 20 20"><path d="M3 1a1 1 0 000 2h1.22l.305 1.222a.997.997 0 00.01.042l1.358 5.43-.893.892C3.74 11.846 4.632 14 6.414 14H15a1 1 0 000-2H6.414l1-1H14a1 1 0 00.894-.553l3-6A1 1 0 0017 3H6.28l-.31-1.243A1 1 0 005 1H3zM16 16.5a1.5 1.5 0 11-3 0 1.5 1.5 0 013 0zM6.5 18a1.5 1.5 0 100-3 1.5 1.5 0 000 3z"></path></svg>
          <span>Купити обрані (${selectedCount})</span>
        `;
        heroBuyBtn.className = 'py-3 px-5 rounded-xl bg-blue-600 hover:bg-blue-700 text-white font-extrabold text-xs sm:text-sm tracking-wide shadow-md shadow-blue-600/25 transition-all flex items-center justify-center gap-1.5 cursor-pointer';
      }
    }
  }

  // OpenCart Multi-Add Queue Engine
  async function handleBuyBoxClick() {
    if (state.isCheckingOut || !state.boxData) {
      // If box is not generated yet, scroll to generator
      if (!state.boxData) {
        const submitBtn = (state.sport === 'running') ? el('step-7-submit') : el('other-sport-submit');
        if (submitBtn) {
          submitBtn.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }
        return;
      }
      return;
    }

    const itemsToAdd = [];
    const slotNames = ['energy', 'hydration', 'gear', 'care_recovery'];
    slotNames.forEach((slot) => {
      const items = state.boxData.slots[slot] || [];
      items.forEach((item, idx) => {
        const key = `${slot}_${idx}`;
        if (state.selectedItems[key]) {
          const activeProduct = state.customSelections[key] || item.product;
          const finalProductId = state.variantSelections[key] || activeProduct.product_id;
          itemsToAdd.push({
            productId: finalProductId,
            quantity: item.quantity_recommended,
            name: activeProduct.name,
            price: activeProduct.price
          });
        }
      });
    });

    if (itemsToAdd.length === 0) {
      alert('Будь ласка, оберіть хоча б один товар для покупки.');
      return;
    }

    state.isCheckingOut = true;
    const buyBtn = el('buy-box-btn');
    const heroBuyBtn = el('hero-buy-box-btn');
    const checkoutStatusEl = el('checkout-status-message');
    if (checkoutStatusEl) {
      checkoutStatusEl.classList.remove('hidden', 'text-rose-600', 'text-emerald-600');
      checkoutStatusEl.classList.add('text-blue-700');
      checkoutStatusEl.textContent = 'Ініціалізація кошика магазину...';
    }

    try {
      if (buyBtn) {
        buyBtn.disabled = true;
        buyBtn.innerHTML = `
          <svg class="animate-spin -ml-1 mr-2 h-5 w-5 text-white inline-block" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z"></path>
          </svg>
          Додаємо бокс до кошика...
        `;
      }

      // Спроба пакетного додавання (1 атомарний HTTP POST-запит)
      const bulkResult = await addBulkProducts(itemsToAdd);

      if (!bulkResult.success) {
        // Плавний fallback на поштучне додавання якщо пакетний ендпоінт ще не підключено в OpenCart
        for (let i = 0; i < itemsToAdd.length; i++) {
          const it = itemsToAdd[i];
          if (buyBtn) {
            buyBtn.innerHTML = `
              <svg class="animate-spin -ml-1 mr-2 h-5 w-5 text-white inline-block" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z"></path>
              </svg>
              Додаємо товар ${i + 1} з ${itemsToAdd.length}...
            `;
          }

          if (checkoutStatusEl) {
            checkoutStatusEl.textContent = `Додаємо до кошика: "${it.name}" (${i + 1}/${itemsToAdd.length})`;
          }

          const addResult = await addProductWithRetry(it.productId, it.quantity);

          if (!addResult.success) {
            const errorMsg = addResult.error || 'Помилка з’єднання з магазином';
            throw new Error(`Не вдалося додати товар "${it.name}" (ID ${it.productId}): ${errorMsg}`);
          }
        }
      }

      if (buyBtn) {
        buyBtn.innerHTML = `
          <svg class="w-5 h-5 text-white inline-block" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"></path>
          </svg>
          Всі товари додано! Переходимо...
        `;
      }

      if (checkoutStatusEl) {
        checkoutStatusEl.classList.remove('text-blue-700');
        checkoutStatusEl.classList.add('text-emerald-700');
        checkoutStatusEl.textContent = `✅ Успішно додано ${itemsToAdd.length} позицій! Відкриваємо кошик магазину...`;
      }

      setTimeout(() => {
        const cartUrl = window.location.hostname.includes('raceexpert.com.ua')
          ? '/index.php?route=checkout/cart'
          : 'https://raceexpert.com.ua/index.php?route=checkout/cart';
        window.location.href = cartUrl;
      }, 1200);

    } catch (err) {
      console.error('Checkout error:', err);
      state.isCheckingOut = false;
      updateLiveTotal();

      if (checkoutStatusEl) {
        checkoutStatusEl.classList.remove('text-blue-700', 'text-emerald-700');
        checkoutStatusEl.classList.add('text-rose-600');
        checkoutStatusEl.innerHTML = `⚠️ ${err.message}. Будь ласка, спробуйте ще раз або відкрийте товари на сайті.`;
      }
    }
  }

  async function addBulkProducts(items) {
    const isLocalOrDemo = window.location.hostname === 'localhost' || 
                          window.location.hostname === '127.0.0.1' || 
                          window.location.hostname === '185.25.119.96';

    if (isLocalOrDemo && !window.FORCE_LIVE_OPENCART) {
      await new Promise((r) => setTimeout(r, 200));
      return { success: true, simulated: true };
    }

    const endpoint = window.location.hostname.includes('raceexpert.com.ua')
      ? '/index.php?route=checkout/quiz_cart/add_bulk'
      : 'https://raceexpert.com.ua/index.php?route=checkout/quiz_cart/add_bulk';

    try {
      const payload = {
        items: items.map(it => ({
          product_id: it.productId,
          quantity: it.quantity
        }))
      };

      const res = await fetch(endpoint, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-Requested-With': 'XMLHttpRequest'
        },
        body: JSON.stringify(payload),
        credentials: 'include'
      });

      if (!res.ok) {
        return { success: false, status: res.status, error: `HTTP ${res.status}` };
      }

      const json = await res.json();
      if (json && json.success) {
        return { success: true, data: json };
      }
      return { success: false, error: json.error || 'Не вдалося додати товари' };
    } catch (err) {
      return { success: false, error: err.message };
    }
  }

  async function addProductWithRetry(productId, quantity, maxRetries = 2) {
    const isLocalOrDemo = window.location.hostname === 'localhost' || 
                          window.location.hostname === '127.0.0.1' || 
                          window.location.hostname === '185.25.119.96';

    if (isLocalOrDemo && !window.FORCE_LIVE_OPENCART) {
      await new Promise((r) => setTimeout(r, 200));
      return { success: true, simulated: true };
    }

    const endpoint = window.location.hostname.includes('raceexpert.com.ua')
      ? '/index.php?route=checkout/cart/add'
      : 'https://raceexpert.com.ua/index.php?route=checkout/cart/add';

    for (let attempt = 0; attempt <= maxRetries; attempt++) {
      try {
        const formData = new URLSearchParams();
        formData.append('product_id', productId);
        formData.append('quantity', quantity);

        const res = await fetch(endpoint, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'X-Requested-With': 'XMLHttpRequest'
          },
          body: formData,
          credentials: 'include'
        });

        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const json = await res.json();
        if (json.success) return { success: true };
        if (json.error) {
          if (json.error.option) {
            return { success: false, error: 'Необхідно обрати опцію товару (смак/розмір)' };
          }
          return { success: false, error: json.error };
        }
        return { success: true };
      } catch (err) {
        if (attempt === maxRetries) return { success: false, error: err.message };
        await new Promise((r) => setTimeout(r, 300));
      }
    }
    return { success: false, error: 'Перевищено час очікування відповіді' };
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
