"""Build the complete, modern, external-facing Race Expert Quiz HTML page."""

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "test-quiz-sandbox"))

from server import AUDIT_PATH, CATALOG_PATH, _load_catalog
from draft_matcher import (
    ACTIVITY_OPTIONS_BY_GOAL,
    COMPONENT_CLASSES_BY_GOAL,
    CONFLICTED_COMPONENT_CLASSES,
    CONFLICTED_COMPONENT_FAMILIES,
    GOAL_FAMILIES,
    GOAL_LABELS,
    PRODUCT_FORMS_BY_GOAL,
    SIZE_GOALS,
    USE_PLACES_BY_GOAL,
    USE_SCENARIOS_BY_GOAL,
    USE_TIMINGS_BY_GOAL,
    attach_audit_evidence,
)

def build_external_html():
    catalog = _load_catalog(CATALOG_PATH)
    audit = json.loads(Path(AUDIT_PATH).read_text(encoding="utf-8"))
    enriched = attach_audit_evidence(catalog, audit)

    trimmed = []
    for r in enriched:
        me = r.get("matching_evidence", {})
        trimmed.append({
            "catalog_row": r.get("catalog_row"),
            "set_id": r.get("set_id"),
            "sku": r.get("sku"),
            "title": r.get("title"),
            "price_uah": r.get("price_uah"),
            "price_snapshot_date": r.get("price_snapshot_date"),
            "source_url": r.get("source_url"),
            "tags": {"item_type": r.get("tags", {}).get("item_type", [])},
            "composition": (r.get("composition") or "")[:280],
            "matching_evidence": {
                "status": me.get("status"),
                "seller_families": me.get("seller_families", []),
                "component_families": me.get("component_families", []),
                "seller_activity_groups": me.get("seller_activity_groups", []),
                "component_activity_groups": me.get("component_activity_groups", []),
                "component_classes": me.get("component_classes", []),
                "use_contexts": me.get("use_contexts", []),
                "race_formats": me.get("race_formats", []),
                "product_forms": me.get("product_forms", []),
                "size_sensitive": me.get("size_sensitive", False),
                "size_values": me.get("size_values", []),
                "weather_signals": me.get("weather_signals", []),
                "conflict_notes": me.get("conflict_notes", []),
            },
        })

    constants = {
        "GOAL_FAMILIES": {k: list(v) for k, v in GOAL_FAMILIES.items()},
        "GOAL_LABELS": GOAL_LABELS,
        "ACTIVITY_OPTIONS_BY_GOAL": {k: list(v) for k, v in ACTIVITY_OPTIONS_BY_GOAL.items()},
        "COMPONENT_CLASSES_BY_GOAL": {k: list(v) for k, v in COMPONENT_CLASSES_BY_GOAL.items()},
        "USE_SCENARIOS_BY_GOAL": {k: list(v) for k, v in USE_SCENARIOS_BY_GOAL.items()},
        "USE_TIMINGS_BY_GOAL": {k: list(v) for k, v in USE_TIMINGS_BY_GOAL.items()},
        "USE_PLACES_BY_GOAL": {k: list(v) for k, v in USE_PLACES_BY_GOAL.items()},
        "PRODUCT_FORMS_BY_GOAL": {k: list(v) for k, v in PRODUCT_FORMS_BY_GOAL.items()},
        "SIZE_GOALS": list(SIZE_GOALS),
        "CONFLICTED_COMPONENT_FAMILIES": {k: list(v) for k, v in CONFLICTED_COMPONENT_FAMILIES.items()},
        "CONFLICTED_COMPONENT_CLASSES": {k: list(v) for k, v in CONFLICTED_COMPONENT_CLASSES.items()},
    }

    catalog_json_str = json.dumps(trimmed, ensure_ascii=False)
    constants_json_str = json.dumps(constants, ensure_ascii=False)

    template = """<!DOCTYPE html>
<html lang="uk" class="dark">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <title>Підбір наборів для бігу та спорту — Race Expert</title>
  <meta name="description" content="Інтерактивний помічник з підбору готових спортивних комплектів та харчування Race Expert">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Space+Grotesk:wght@600;700&display=swap" rel="stylesheet">
  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    tailwind.config = {{
      darkMode: 'class',
      theme: {{
        extend: {{
          colors: {{
            brand: {{
              50: '#fff7ed',
              100: '#ffedd5',
              500: '#f97316',
              600: '#ea580c',
              700: '#c2410c'
            }},
            slate: {{
              850: '#141e33',
              900: '#0b1120',
              950: '#060a12'
            }}
          }},
          fontFamily: {{
            sans: ['"Plus Jakarta Sans"', 'system-ui', 'sans-serif'],
            display: ['"Space Grotesk"', 'sans-serif']
          }}
        }}
      }}
    }};
  </script>
  <style>
    body {{
      font-feature-settings: "cv02", "cv03", "cv04", "cv11";
      -webkit-tap-highlight-color: transparent;
    }}
    .glow-brand {{
      box-shadow: 0 0 50px -10px rgba(249, 115, 22, 0.18);
    }}
    .custom-scroll::-webkit-scrollbar {{
      width: 6px;
    }}
    .custom-scroll::-webkit-scrollbar-track {{
      background: transparent;
    }}
    .custom-scroll::-webkit-scrollbar-thumb {{
      background: #334155;
      border-radius: 9999px;
    }}
  </style>
</head>
<body class="bg-slate-950 text-slate-100 min-h-screen flex flex-col font-sans antialiased selection:bg-brand-500 selection:text-white">

  <!-- Top Announcement Bar -->
  <aside class="bg-gradient-to-r from-brand-600 via-orange-600 to-amber-600 py-1.5 px-4 text-center text-xs font-semibold text-white tracking-wide">
    <span class="inline-flex items-center gap-1.5">
      <span class="w-1.5 h-1.5 rounded-full bg-white animate-pulse"></span>
      <span id="topNotice">Офіційний інтерактивний підбір Race Expert · 206 готових наборів</span>
    </span>
  </aside>

  <!-- Navigation Bar -->
  <header class="border-b border-slate-800/80 bg-slate-900/80 backdrop-blur-md sticky top-0 z-40">
    <div class="max-w-4xl mx-auto px-4 h-16 flex items-center justify-between">
      <div class="flex items-center gap-3">
        <div class="w-10 h-10 rounded-xl bg-gradient-to-br from-brand-500 to-amber-600 flex items-center justify-center font-display font-bold text-xl text-white shadow-lg shadow-brand-500/25">
          R
        </div>
        <div>
          <span class="font-display font-bold tracking-tight text-lg text-white block leading-tight">RACE EXPERT</span>
          <span class="text-[11px] text-slate-400 font-medium block">Quiz Selection Engine</span>
        </div>
      </div>

      <div class="flex items-center gap-3">
        <label for="langToggle" class="sr-only">Мова інтерфейсу</label>
        <div class="inline-flex items-center bg-slate-800/80 rounded-lg p-0.5 border border-slate-700/60 text-xs font-semibold">
          <button id="btnUk" type="button" class="px-2.5 py-1 rounded-md bg-brand-500 text-white transition shadow-sm">УКР</button>
          <button id="btnRu" type="button" class="px-2.5 py-1 rounded-md text-slate-400 hover:text-white transition">РУС</button>
        </div>
        <span class="hidden sm:inline-block px-2.5 py-1 text-[11px] font-semibold uppercase tracking-wider rounded-md bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
          Live 206 Kits
        </span>
      </div>
    </div>
  </header>

  <!-- Main Container -->
  <main class="flex-1 max-w-3xl w-full mx-auto px-4 py-8 md:py-12 flex flex-col justify-center">

    <div class="bg-slate-900/90 border border-slate-800 rounded-2xl p-6 sm:p-8 md:p-10 glow-brand shadow-2xl relative overflow-hidden">

      <!-- Progress Tracking Bar -->
      <div class="mb-8" id="progressSection">
        <div class="flex items-center justify-between text-xs font-semibold uppercase tracking-wider mb-2.5">
          <span id="stepCounterLabel" class="text-brand-500">Питання 1</span>
          <span id="activePoolBadge" class="text-slate-400 bg-slate-800/60 px-2.5 py-0.5 rounded-full border border-slate-700/50">206 варіантів</span>
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
            <h3 id="lblNearMiss" class="text-xs font-bold uppercase tracking-wider text-amber-400">Близько за бюджетом (рекомендовані альтернативи)</h3>
          </div>
          <div id="nearMissCardsList" class="space-y-4"></div>
        </section>

        <!-- Floor Anchor Section (Baseline Minimum) -->
        <section id="floorAnchorSection" class="pt-6 border-t border-slate-800/80 space-y-3 hidden">
          <div class="flex items-center gap-2">
            <span class="text-purple-400 text-base">🛡️</span>
            <h3 id="lblFloorAnchor" class="text-xs font-bold uppercase tracking-wider text-purple-400">Базовий стартовий набір у цій категорії</h3>
          </div>
          <div id="floorAnchorCardsList" class="space-y-4"></div>
        </section>
      </div>

    </div>

  </main>

  <!-- Footer -->
  <footer class="border-t border-slate-900 bg-slate-950/80 py-6 text-center text-xs text-slate-500">
    <p>Race Expert · Офіційний каталог 206 готових наборів «За потребами»</p>
    <p class="mt-1 text-[11px] text-slate-600">Ціни та наявність наведено на дату локального знімка каталогу</p>
  </footer>

  <!-- Bundled Datasets & Client Matcher Engine -->
  <script>
    window.QUIZ_CATALOG = __CATALOG_JSON_STR__;
    const CONSTANTS = __CONSTANTS_JSON_STR__;

    const CORE_ANSWER_FIELDS = ["activity"];
    const STEERING_ANSWER_FIELDS = ["component_class"];
    const SOFT_ANSWER_FIELDS = [
      "use_scenario", "use_timing", "use_place", "race_format", "season", "product_form"
    ];
    const ANSWER_SIGNAL_FIELDS = [...CORE_ANSWER_FIELDS, ...STEERING_ANSWER_FIELDS, ...SOFT_ANSWER_FIELDS];

    function asSet(val) {{
      if (val === undefined || val === null || val === "" || val === "any") return new Set();
      if (Array.isArray(val)) return new Set(val.filter(v => v !== "" && v !== "any" && v != null));
      return new Set([val]);
    }}

    function intersect(a, b) {{
      const sB = b instanceof Set ? b : new Set(b);
      return new Set([...a].filter(x => sB.has(x)));
    }}

    function membershipStatus(record) {{
      const itemTypes = record.tags?.item_type || [];
      const comp = (record.composition || "").toLowerCase();
      const title = (record.title || "").toLowerCase();
      if (itemTypes.includes("club_membership_bundle") || comp.includes("абонемент") || comp.includes("membership")) return "included";
      if (title.includes("абонемент") || title.includes("membership")) return "included";
      if (title.includes("club") || title.includes("клуб")) return "mentioned";
      return "unknown";
    }}

    function matchingFamilies(record, goalGroup) {{
      const ev = record.matching_evidence || {{}};
      const wanted = new Set(CONSTANTS.GOAL_FAMILIES[goalGroup] || []);
      let seller = [...intersect(new Set(ev.seller_families || []), wanted)];
      let compSet = intersect(new Set(ev.component_families || []), wanted);
      const blocked = new Set(CONSTANTS.CONFLICTED_COMPONENT_FAMILIES[record.sku] || []);
      if (blocked.has("*")) compSet.clear();
      else blocked.forEach(b => compSet.delete(b));
      return {{ seller, components: [...compSet] }};
    }}

    function goalCandidates(catalog, goalGroup) {{
      const list = [];
      for (const r of catalog) {{
        const mf = matchingFamilies(r, goalGroup);
        if (mf.seller.length > 0 || mf.components.length > 0) {{
          list.push([r, mf.seller, mf.components]);
        }}
      }}
      return list;
    }}

    function sizeRanges(record) {{
      const ranges = [];
      const vals = record.matching_evidence?.size_values || [];
      for (const item of vals) {{
        if (item.type !== "shoe_or_sock_size") continue;
        const str = String(item.value || "").replace("–", "-");
        const parts = str.split("-");
        const lower = parseInt(parts[0], 10);
        const upper = parseInt(parts[parts.length - 1], 10);
        if (!isNaN(lower) && !isNaN(upper)) ranges.push([lower, upper]);
      }}
      return ranges;
    }}

    function seasonGroups(record) {{
      const sigs = new Set(record.matching_evidence?.weather_signals || []);
      const res = new Set();
      if (sigs.has("cold_weather") || sigs.has("winter")) res.add("cold");
      if (sigs.has("hot_weather") || sigs.has("summer")) res.add("warm");
      return res;
    }}

    function softSignals(record, key) {{
      const ev = record.matching_evidence || {{}};
      if (key === "activity") {{
        return new Set([...(ev.seller_activity_groups || []), ...(ev.component_activity_groups || [])]);
      }}
      if (key === "component_class") {{
        return new Set(ev.component_classes || []);
      }}
      if (key === "use_scenario" || key === "use_timing" || key === "use_place") {{
        const vals = new Set(ev.use_contexts || []);
        if (key === "use_scenario") {{
          const sc = new Set();
          const races = (ev.race_formats || []).filter(x => x !== "unspecified");
          if (races.length > 0) sc.add("event_preparation");
          if (vals.has("before_or_after_training") || vals.has("during_training")) sc.add("training");
          if (vals.has("daily_use") || vals.has("evening_or_bedtime") || vals.has("work_or_study")) sc.add("everyday");
          return sc;
        }}
        if (key === "use_timing") {{
          return intersect(vals, ["before_or_after_training", "during_training", "daily_use", "evening_or_bedtime"]);
        }}
        if (key === "use_place") {{
          return intersect(vals, ["hiking_or_camping", "travel_or_road", "work_or_study"]);
        }}
        return vals;
      }}
      if (key === "race_format") {{
        return new Set((ev.race_formats || []).filter(x => x !== "unspecified"));
      }}
      if (key === "season") return seasonGroups(record);
      if (key === "product_form") return new Set(ev.product_forms || []);
      return new Set();
    }}

    function candidateFit(candidate, answers) {{
      const record = candidate[0];
      const maxPrice = answers.max_price_uah;
      const price = record.price_uah;
      if (maxPrice !== undefined && maxPrice !== null && (typeof price !== "number" || price > maxPrice)) {{
        return null;
      }}
      const memPref = answers.membership;
      if (memPref === "yes" && membershipStatus(record) !== "included") return null;
      if (memPref === "no" && ["included", "mentioned"].includes(membershipStatus(record))) return null;

      const matched = [];
      const unknown = [];
      const relaxed = [];
      const relaxedValues = {{}};

      for (const key of ANSWER_SIGNAL_FIELDS) {{
        const vals = asSet(answers[key]);
        if (vals.size === 0) continue;
        const sigs = softSignals(record, key);
        if (sigs.size === 0) {{
          unknown.push(key);
        }} else if (intersect(vals, sigs).size > 0) {{
          matched.push(key);
        }} else if (CORE_ANSWER_FIELDS.includes(key) || STEERING_ANSWER_FIELDS.includes(key)) {{
          return null;
        }} else {{
          relaxed.push(key);
          relaxedValues[key] = vals.size > 1 ? [...vals].sort() : [...vals][0];
        }}
      }}

      let sizeMatch = false;
      let sizeStatus = "not_requested";
      const size = answers.shoe_size;
      if (size !== undefined && size !== null && size !== "" && size !== "any") {{
        const numSize = Number(size);
        const ranges = sizeRanges(record);
        if (ranges.length > 0) {{
          sizeMatch = ranges.some(([lo, hi]) => numSize >= lo && numSize <= hi);
          if (!sizeMatch) return null;
          sizeStatus = "matched";
          matched.push("shoe_size");
        }} else if (record.matching_evidence?.size_sensitive) {{
          sizeStatus = "unknown";
          unknown.push("shoe_size");
        }}
      }}

      const matchType = relaxed.length > 0 ? "relaxed" : unknown.length > 0 ? "general" : "exact";
      return {{
        match_type: matchType,
        matched_preferences: matched,
        unknown_preferences: unknown,
        relaxed_preferences: relaxed,
        relaxed_preference_values: relaxedValues,
        size_match: sizeMatch,
        size_status: sizeStatus
      }};
    }}

    function candidatePools(candidates, answers) {{
      const pools = {{ exact: [], general: [], relaxed: [] }};
      for (const c of candidates) {{
        const fit = candidateFit(c, answers);
        if (fit) pools[fit.match_type].push([c, fit]);
      }}
      return pools;
    }}

    function valuesIn(candidates, key, allowed) {{
      const s = new Set();
      const allowSet = new Set(allowed);
      for (const [r] of candidates) {{
        for (const val of softSignals(r, key)) {{
          if (allowSet.has(val)) s.add(val);
        }}
      }}
      return [...s].sort();
    }}

    function wouldSplit(candidates, key, allowed, minSignals = 2) {{
      let count = 0;
      const allowSet = new Set(allowed);
      for (const [r] of candidates) {{
        if (intersect(softSignals(r, key), allowSet).size > 0) count++;
      }}
      return count >= minSignals;
    }}

    function questionPlan(candidates, goalGroup, answers) {{
      const questions = [];
      const add = (id, options, title_key) => {{
        if (options && options.length > 0) {{
          questions.push({{ id, title_key, options, type: "single" }});
        }}
      }};

      const remaining = candidates;
      const answered = answers || {{}};

      if (remaining.length <= 3) {{
        if (remaining.length > 0 && !("max_price_uah" in answered)) {{
          const prices = remaining.map(([r]) => r.price_uah).filter(p => typeof p === "number");
          questions.push({{
            id: "max_price_uah",
            title_key: "question_budget",
            type: "number",
            min: 0,
            dynamic_min: prices.length ? Math.min(...prices) : null,
            dynamic_max: prices.length ? Math.max(...prices) : null
          }});
        }}
        return questions;
      }}

      if (!("activity" in answered)) {{
        let vals = valuesIn(remaining, "activity", CONSTANTS.ACTIVITY_OPTIONS_BY_GOAL[goalGroup] || []);
        if (vals.length > 0) vals = [...new Set([...vals, "other"])].sort();
        if (vals.length > 1) add("activity", vals, "question_activity");
      }}

      if (!("component_class" in answered)) {{
        const vals = valuesIn(remaining, "component_class", CONSTANTS.COMPONENT_CLASSES_BY_GOAL[goalGroup] || []);
        if (vals.length > 1) add("component_class", vals, "question_component_class");
      }}

      if (!("use_scenario" in answered)) {{
        const allowed = CONSTANTS.USE_SCENARIOS_BY_GOAL[goalGroup] || [];
        const vals = valuesIn(remaining, "use_scenario", allowed);
        if (vals.length > 1 && wouldSplit(remaining, "use_scenario", allowed)) {{
          add("use_scenario", vals, "question_use_scenario");
        }}
      }}

      if (!("use_timing" in answered)) {{
        const allowed = CONSTANTS.USE_TIMINGS_BY_GOAL[goalGroup] || [];
        const vals = valuesIn(remaining, "use_timing", allowed);
        if (vals.length > 1 && wouldSplit(remaining, "use_timing", allowed)) {{
          add("use_timing", vals, "question_use_timing");
        }}
      }}

      if (!("use_place" in answered)) {{
        const allowed = CONSTANTS.USE_PLACES_BY_GOAL[goalGroup] || [];
        const vals = valuesIn(remaining, "use_place", allowed);
        if (vals.length > 1 && wouldSplit(remaining, "use_place", allowed)) {{
          add("use_place", vals, "question_use_place");
        }}
      }}

      const eventBranch = goalGroup === "running"
        || asSet(answered.activity).has("running") || asSet(answered.activity).has("cycling")
        || asSet(answered.use_scenario).has("event_preparation");
      if (!("race_format" in answered) && eventBranch) {{
        const allowed = ["half_marathon", "marathon", "race_or_event_preparation", "ultra_or_long_distance"];
        const vals = valuesIn(remaining, "race_format", allowed);
        if (vals.length > 1 && wouldSplit(remaining, "race_format", allowed)) {{
          add("race_format", vals, "question_race_format");
        }}
      }}

      const weatherBranch = ["running", "hydration", "outdoors", "gear"].includes(goalGroup)
        || [...asSet(answered.activity)].some(x => ["running", "cycling", "hiking", "walking"].includes(x));
      if (!("season" in answered) && weatherBranch) {{
        const allowed = ["cold", "warm"];
        const vals = valuesIn(remaining, "season", allowed);
        if (vals.length > 1 && wouldSplit(remaining, "season", allowed)) {{
          add("season", vals, "question_season");
        }}
      }}

      const CONSUMABLE_COMPONENT_CLASSES = new Set([
        "energy_nutrition", "hydration_items", "protein_carbohydrate_food", "supplements_vitamins_minerals", "food_or_meal", "dehydrated_meal", "creatine_preworkout"
      ]);
      const NON_CONSUMABLE_COMPONENT_CLASSES = new Set([
        "sports_accessories", "apparel_footwear"
      ]);
      const CONSUMABLE_PRODUCT_FORMS = new Set([
        "powder", "tablets", "capsules", "softgels", "gel", "bars", "liquid", "sticks", "food_or_meal"
      ]);

      const isConsumable = CONSUMABLE_COMPONENT_CLASSES.has(compClass)
        || (!compClass && ["food", "daily", "recovery"].includes(goalGroup));
      const isBlocked = NON_CONSUMABLE_COMPONENT_CLASSES.has(compClass)
        || (compClass && !CONSUMABLE_COMPONENT_CLASSES.has(compClass))
        || goalGroup === "gear";

      if (!("product_form" in answered) && isConsumable && !isBlocked) {{
        const allowed = (CONSTANTS.PRODUCT_FORMS_BY_GOAL[goalGroup] || []).filter(f => CONSUMABLE_PRODUCT_FORMS.has(f));
        const vals = valuesIn(remaining, "product_form", allowed);
        if (vals.length > 1 && wouldSplit(remaining, "product_form", allowed)) {{
          add("product_form", vals, "question_product_form");
        }}
      }}

      if (!("membership" in answered)) {{
        const hasInc = remaining.some(([r]) => membershipStatus(r) === "included");
        const hasWithout = remaining.some(([r]) => !["included", "mentioned"].includes(membershipStatus(r)));
        if (hasInc && hasWithout) add("membership", ["yes", "no"], "question_membership");
      }}

      if (!("shoe_size" in answered) && CONSTANTS.SIZE_GOALS.includes(goalGroup)) {{
        const hasSize = remaining.some(([r]) => r.matching_evidence?.size_sensitive && sizeRanges(r).length > 0);
        if (hasSize) {{
          const s = new Set();
          remaining.forEach(([r]) => {{
            sizeRanges(r).forEach(([lo, hi]) => s.add(`${{lo}}-${{hi}}`));
          }});
          questions.push({{
            id: "shoe_size",
            title_key: "question_shoe_size",
            type: "number",
            min: 1,
            max: 70,
            ranges: [...s].sort()
          }});
        }}
      }}

      if (remaining.length > 0 && !("max_price_uah" in answered)) {{
        const prices = remaining.map(([r]) => r.price_uah).filter(p => typeof p === "number");
        questions.push({{
          id: "max_price_uah",
          title_key: "question_budget",
          type: "number",
          min: 0,
          dynamic_min: prices.length ? Math.min(...prices) : null,
          dynamic_max: prices.length ? Math.max(...prices) : null
        }});
      }}

      return questions;
    }}

    function calculateMatchScore(record, sellerFamilies, componentFamilies, fit, validated) {{
      let evScore = 0;
      if (sellerFamilies.length > 0) evScore += 20;
      if (componentFamilies.length > 0) evScore += 15;
      if (record.matching_evidence?.status === "conflict_review_required") {{
        evScore = Math.max(5, evScore - 5);
      }}

      const activeKeys = ANSWER_SIGNAL_FIELDS.filter(k => asSet(validated[k]).size > 0);
      let prefScore = 45;
      if (activeKeys.length > 0) {{
        const matchedSet = new Set(fit.matched_preferences || []);
        const unknownSet = new Set(fit.unknown_preferences || []);
        let pts = 0;
        activeKeys.forEach(k => {{
          if (matchedSet.has(k)) pts += 1.0;
          else if (unknownSet.has(k)) pts += 0.55;
        }});
        prefScore = Math.round(45 * (pts / activeKeys.length));
      }}

      let fitScore = 0;
      if (validated.shoe_size === undefined || validated.shoe_size === null) fitScore += 10;
      else if (fit.size_status === "matched") fitScore += 10;
      else if (fit.size_status === "unknown") fitScore += 5;

      const maxP = validated.max_price_uah;
      const price = record.price_uah || 0;
      if (maxP === undefined || maxP === null) fitScore += 10;
      else if (typeof price === "number" && price <= maxP) {{
        fitScore += price <= maxP * 0.85 ? 10 : 9;
      }} else if (typeof price === "number" && price > maxP) {{
        const over = price - maxP;
        const pct = over / Math.max(1, maxP);
        fitScore += Math.max(0, Math.round(10 * Math.max(0, 1 - 2.5 * pct)));
      }}

      let total = Math.min(99, Math.max(15, evScore + prefScore + fitScore));
      const mt = fit.match_type;
      if (mt === "exact" && (maxP == null || price <= maxP)) total = Math.max(88, total);
      else if (mt === "general" && (maxP == null || price <= maxP)) total = Math.min(87, Math.max(72, total));
      else if (mt === "near_miss") total = Math.min(84, Math.max(60, total));
      else if (mt === "floor_anchor") total = Math.min(75, Math.max(45, total));
      else if (mt === "relaxed") total = Math.min(68, Math.max(35, total));

      return {{
        total,
        breakdown: {{ evidence: evScore, preferences: prefScore, constraints: fitScore }}
      }};
    }}

    function findBudgetNearMisses(goalCands, validated, maxDeltaPct = 0.25, maxDeltaUah = 350) {{
      const maxP = validated.max_price_uah;
      if (maxP === undefined || maxP === null) return [];
      const answersNoPrice = {{ ...validated }};
      delete answersNoPrice.max_price_uah;
      const maxAllowed = Math.max(Math.floor(maxP * (1 + maxDeltaPct)), maxP + maxDeltaUah);
      const nearMisses = [];

      for (const cand of goalCands) {{
        const r = cand[0];
        const p = r.price_uah;
        if (typeof p !== "number" || p <= maxP || p > maxAllowed) continue;
        const fit = candidateFit(cand, answersNoPrice);
        if (fit && ["exact", "general"].includes(fit.match_type)) {{
          const copy = {{ ...fit, match_type: "near_miss", price_over_budget_uah: p - maxP }};
          nearMisses.push([cand, copy]);
        }}
      }}

      nearMisses.sort((a, b) => {{
        const diffOver = a[1].price_over_budget_uah - b[1].price_over_budget_uah;
        if (diffOver !== 0) return diffOver;
        return a[0][0].catalog_row - b[0][0].catalog_row;
      }});
      return nearMisses.slice(0, 3);
    }}

    function findFloorAnchor(goalCands, validated) {{
      const maxP = validated.max_price_uah;
      if (maxP === undefined || maxP === null) return [];
      const answersNoPrice = {{ ...validated }};
      delete answersNoPrice.max_price_uah;
      const pools = candidatePools(goalCands, answersNoPrice);
      const comp = pools.exact.length ? pools.exact : pools.general;
      if (!comp.length) return [];

      const over = comp
        .filter(([cand]) => typeof cand[0].price_uah === "number" && cand[0].price_uah > maxP)
        .sort((a, b) => a[0][0].price_uah - b[0][0].price_uah || a[0][0].catalog_row - b[0][0].catalog_row);

      return over.slice(0, 2).map(([cand, fit]) => [
        cand,
        {{
          ...fit,
          match_type: "floor_anchor",
          price_over_budget_uah: cand[0].price_uah - maxP,
          floor_price_uah: cand[0].price_uah
        }}
      ]);
    }}

    function buildResultItem(record, seller, comp, fit, locale, validated) {{
      const ev = record.matching_evidence || {{}};
      const reasons = [];
      const goalLabel = CONSTANTS.GOAL_LABELS[locale]?.[record.selected_goal] || record.selected_goal;

      if (seller.length > 0) {{
        reasons.push(locale === "uk" ? `Продавець позиціонує набір для теми «${{goalLabel}}».` : `Продавец позиционирует набор для темы «${{goalLabel}}».`);
      }}
      if (comp.length > 0) {{
        reasons.push(locale === "uk" ? "У переліку складу є товар, пов'язаний із цією задачею." : "В списке состава есть товар, связанный с этой задачей.");
      }}

      const prefLabels = {{
        activity: ["активности", "активності"],
        component_class: ["типу товара в наборе", "типу товару в наборі"],
        use_scenario: ["сценарию", "сценарію"],
        use_timing: ["времени использования", "часу використання"],
        use_place: ["месту использования", "місцю використання"],
        race_format: ["формату старта", "формату старту"],
        season: ["погоде", "погоді"],
        product_form: ["форме товара", "формі товару"]
      }};

      (fit.matched_preferences || []).forEach(k => {{
        if (k === "shoe_size") return;
        if (prefLabels[k]) {{
          const label = locale === "uk" ? prefLabels[k][1] : prefLabels[k][0];
          reasons.push(locale === "uk" ? `Є збіг за ${{label}}.` : `Есть совпадение по ${{label}}.`);
        }}
      }});

      if (fit.size_match) {{
        reasons.push(locale === "uk" ? "Вказаний розмір входить у діапазон товару." : "Указанный размер входит в диапазон товара.");
      }}
      if (fit.match_type === "near_miss") {{
        const over = fit.price_over_budget_uah || 0;
        reasons.push(locale === "uk" ? `Перевищує вибраний бюджет на ${{over}} ₴.` : `Превышает выбранный бюджет на ${{over}} ₴.`);
      }} else if (fit.match_type === "floor_anchor") {{
        const floorP = fit.floor_price_uah;
        const over = fit.price_over_budget_uah || 0;
        reasons.push(locale === "uk" ? `Мінімальний базовий набір у категорії (від ${{floorP}} ₴, різниця ${{over}} ₴).` : `Минимальный базовый набор в категории (от ${{floorP}} ₴, разница ${{over}} ₴).`);
      }}

      const notes = [];
      if (fit.size_status === "unknown") {{
        notes.push(locale === "uk" ? "Розмір товару не вказаний у знімку; збіг не підтверджено." : "Размер товара не указан в снимке; совпадение не подтверждено.");
      }}
      if (ev.status === "conflict_review_required") {{
        notes.push(locale === "uk" ? "У картці є невирішена розбіжність складу; перевірте актуальну сторінку." : "В карточке есть неразрешённое расхождение состава; проверьте актуальную страницу.");
      }}

      const scoreData = calculateMatchScore(record, seller, comp, fit, validated);

      return {{
        set_id: record.set_id,
        catalog_row: record.catalog_row,
        sku: record.sku,
        title: record.title,
        source_url: record.source_url,
        price_uah: record.price_uah,
        price_snapshot_date: record.price_snapshot_date,
        match_type: fit.match_type,
        match_score_pct: scoreData.total,
        score_breakdown: scoreData.breakdown,
        price_over_budget_uah: fit.price_over_budget_uah || 0,
        unknown_preferences: fit.unknown_preferences || [],
        relaxed_preferences: fit.relaxed_preferences || [],
        relaxed_preference_values: fit.relaxed_preference_values || {{}},
        evidence_status: ev.status || "unknown",
        membership_status: membershipStatus(record),
        size_status: fit.size_status,
        reasons,
        data_notes: notes
      }};
    }}

    function draftOptions(catalog, goalGroup, answers = {{}}) {{
      if (!goalGroup) {{
        const opts = [];
        for (const val of Object.keys(CONSTANTS.GOAL_FAMILIES)) {{
          const cands = goalCandidates(catalog, val);
          if (cands.length > 0) {{
            opts.push({{ value: val, label: CONSTANTS.GOAL_LABELS.ru[val], count: cands.length }});
          }}
        }}
        return {{ test_only: true, goal_options: opts, catalog_count: catalog.length }};
      }}

      const candidates = goalCandidates(catalog, goalGroup);
      const pools = candidatePools(candidates, {{ ...answers, goal_group: goalGroup }});
      const remaining = [...pools.exact, ...pools.general].map(([cand]) => cand);
      const priceSource = remaining.length ? remaining : candidates;
      const prices = priceSource.map(([r]) => r.price_uah).filter(p => typeof p === "number");

      return {{
        test_only: true,
        goal_group: goalGroup,
        candidate_count: remaining.length,
        exact_candidate_count: pools.exact.length,
        general_candidate_count: pools.general.length,
        relaxed_candidate_count: pools.relaxed.length,
        question_plan: questionPlan(remaining, goalGroup, answers),
        price_range_uah: prices.length ? {{ min: Math.min(...prices), max: Math.max(...prices) }} : null,
        price_snapshot_date: priceSource[0]?.[0]?.price_snapshot_date || null
      }};
    }}

    function draftRecommend(catalog, request) {{
      const goalGroup = request.goal_group;
      const locale = request.locale === "uk" ? "uk" : "ru";
      const candidates = goalCandidates(catalog, goalGroup);
      const pools = candidatePools(candidates, request);
      const fallbackMode = request.fallback_mode;

      let selectedPool = [];
      let status = "no_match";

      if (fallbackMode && pools[fallbackMode]) {{
        selectedPool = pools[fallbackMode];
        status = fallbackMode;
      }} else if (pools.exact.length > 0) {{
        selectedPool = pools.exact;
        status = "matched";
      }} else if (pools.general.length > 0) {{
        selectedPool = pools.general;
        status = "general_auto";
      }} else {{
        selectedPool = [];
        status = pools.relaxed.length > 0 ? "no_exact_match" : "no_match";
      }}

      selectedPool.sort((a, b) => {{
        const [candA, fitA] = a;
        const [candB, fitB] = b;
        const bothA = candA[1].length && candA[2].length ? 1 : 0;
        const bothB = candB[1].length && candB[2].length ? 1 : 0;
        if (bothB !== bothA) return bothB - bothA;
        const diffMatched = (fitB.matched_preferences?.length || 0) - (fitA.matched_preferences?.length || 0);
        if (diffMatched !== 0) return diffMatched;
        return (candA[0].price_uah || 0) - (candB[0].price_uah || 0) || candA[0].catalog_row - candB[0].catalog_row;
      }});

      const results = selectedPool.slice(0, 3).map(([cand, fit]) => {{
        return buildResultItem({{ ...cand[0], selected_goal: goalGroup }}, cand[1], cand[2], fit, locale, request);
      }});

      let nearMissResults = [];
      if (results.length < 3 && request.max_price_uah != null) {{
        const rawNear = findBudgetNearMisses(candidates, request);
        const existing = new Set(results.map(r => r.catalog_row));
        nearMissResults = rawNear
          .filter(([cand]) => !existing.has(cand[0].catalog_row))
          .slice(0, 3)
          .map(([cand, fit]) => buildResultItem({{ ...cand[0], selected_goal: goalGroup }}, cand[1], cand[2], fit, locale, request));
      }}

      let floorAnchorResults = [];
      if (!results.length && !nearMissResults.length && request.max_price_uah != null) {{
        const rawFloor = findFloorAnchor(candidates, request);
        floorAnchorResults = rawFloor.slice(0, 2).map(([cand, fit]) => {{
          return buildResultItem({{ ...cand[0], selected_goal: goalGroup }}, cand[1], cand[2], fit, locale, request);
        }});
        if (floorAnchorResults.length > 0) status = "floor_anchor";
      }}

      const messages = {{
        ru: {{
          matched: "Знайдено варіанти, у яких усі відповіді повністю підтверджуються сигналами каталогу.",
          general_auto: "Точного збігу за всіма дрібними параметрами немає. Показано перевірені варіанти без відомих протиріч.",
          no_exact_match: "Точного збігу за обраними критеріями не знайдено. Перегляньте варіанти нижче або змініть бюджет.",
          general: "Ці варіанти не суперечать вашим відповідям, але частина додаткових критеріїв не вказана виробником.",
          relaxed: "Варіанти показано з невеликим ослабленням другорядних уподобань.",
          no_match: "За обраними обмеженнями наразі наборів не знайдено.",
          floor_anchor: "У цій категорії мінімальні повноцінні комплекти починаються від {{floor}} ₴. Нижче запропоновано стартовий варіант."
        }},
        uk: {{
          matched: "Знайдено набори, для яких усі вказані відповіді повністю підтверджуються сигналами каталогу.",
          general_auto: "Точного збігу за всіма дрібними параметрами немає. Показано перевірені варіанти без відомих протиріч.",
          no_exact_match: "Точного збігу за обраними критеріями не знайдено. Перегляньте варіанти нижче або змініть бюджет.",
          general: "Ці варіанти не суперечать вашим відповідям, але частина додаткових критеріїв не вказана виробником.",
          relaxed: "Варіанти показано з невеликим послабленням другорядних переваг.",
          no_match: "За обраними обмеженнями наразі наборів не знайдено.",
          floor_anchor: "У цій категорії мінімальні повноцінні комплекти починаються від {{floor}} ₴. Нижче запропоновано стартовий варіант."
        }}
      }};

      let msg = messages[locale]?.[status] || "";
      if (status === "floor_anchor" && floorAnchorResults.length > 0) {{
        const floorMin = Math.min(...floorAnchorResults.map(r => r.price_uah));
        msg = msg.replace("{{floor}}", floorMin);
      }}

      return {{
        status,
        returned_count: results.length,
        results,
        near_miss_results: nearMissResults,
        floor_anchor_results: floorAnchorResults,
        message: msg
      }};
    }}

    // UI Controller
    const UI_COPY = {{
      uk: {{
        topNotice: "Офіційний інтерактивний підбір Race Expert · 206 готових наборів",
        goalTitle: "Для якої мети ви обираєте набір?",
        goalHint: "Оберіть вашу головну спортивну задачу. Наступні кроки підлаштуються під неї.",
        stepFirst: "Крок 1 із 5",
        stepCount: "Крок {{current}} із {{total}}",
        candidatesBadge: "{count} наборів",
        back: "Назад",
        continue: "Продовжити",
        showResults: "Підібрати набори",
        restart: "Змінити відповіді",
        any: "Не має значення",
        nearMissHeading: "Близько за бюджетом (рекомендовані альтернативи)",
        floorAnchorHeading: "Базовий стартовий набір у категорії",
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
        cardPrice: "Вартість за знімком каталогу:",
        openCardBtn: "Переглянути набір на сайті Race Expert →"
      }},
      ru: {{
        topNotice: "Официальный интерактивный подбор Race Expert · 206 готовых наборов",
        goalTitle: "Для какой цели вы подбираете набор?",
        goalHint: "Выберите главную спортивную задачу. Последующие шаги настроятся под неё.",
        stepFirst: "Шаг 1 из 5",
        stepCount: "Шаг {{current}} из {{total}}",
        candidatesBadge: "{count} наборов",
        back: "Назад",
        continue: "Продолжить",
        showResults: "Подобрать наборы",
        restart: "Изменить ответы",
        any: "Не имеет значения",
        nearMissHeading: "Близко по бюджету (рекомендуемые альтернативы)",
        floorAnchorHeading: "Базовый стартовый набор в категории",
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
        cardPrice: "Цена по снимку каталога:",
        openCardBtn: "Перейти к набору на сайте Race Expert →"
      }}
    }};

    const appState = {{
      locale: "uk",
      goal: "",
      answers: {{}},
      history: [],
      currentQuestionId: "goal",
      questionPlan: [],
      optionsData: null,
      catalog: window.QUIZ_CATALOG || []
    }};

    function tr(key, vars = {{}}) {{
      let str = UI_COPY[appState.locale]?.[key] || UI_COPY.uk?.[key] || key;
      Object.entries(vars).forEach(([k, v]) => {{
        str = str.replaceAll(`{{${{k}}}}`, v);
      }});
      return str;
    }}

    function optionLabel(qId, val) {{
      if (val === "any") return tr("any");
      const prefixes = {{
        activity: "activity_",
        component_class: "class_",
        membership: "membership_",
        use_scenario: "scenario_",
        race_format: "race_",
        season: "season_",
        product_form: "form_"
      }};
      const p = prefixes[qId] || "";
      return tr(p + val);
    }}

    function renderScreen() {{
      const isGoal = appState.currentQuestionId === "goal";
      const plan = appState.questionPlan;
      const q = isGoal
        ? {{ id: "goal", type: "single", options: ["running", "training", "hydration", "food", "recovery", "outdoors", "gear", "daily", "gift"] }}
        : plan.find(item => item.id === appState.currentQuestionId);

      if (!q) return;

      // Progress
      const totalSteps = Math.max(appState.history.length + plan.length, 2);
      const curStep = appState.history.length + 1;
      document.getElementById("stepCounterLabel").textContent = isGoal
        ? tr("stepFirst")
        : tr("stepCount", {{ current: curStep, total: totalSteps }});

      const pct = Math.min(100, Math.round((curStep / totalSteps) * 100));
      document.getElementById("progressFill").style.width = pct + "%";

      const candCount = appState.optionsData?.candidate_count ?? 206;
      document.getElementById("activePoolBadge").textContent = tr("candidatesBadge", {{ count: candCount }});

      // Headers
      document.getElementById("questionHeading").textContent = isGoal ? tr("goalTitle") : tr(q.title_key);
      document.getElementById("questionSubtitle").textContent = isGoal ? tr("goalHint") : "";
      document.getElementById("errorAlert").classList.add("hidden");

      const optionsBox = document.getElementById("optionsContainer");
      const numBox = document.getElementById("numberContainer");
      optionsBox.innerHTML = "";

      if (q.type === "number") {{
        optionsBox.classList.add("hidden");
        numBox.classList.remove("hidden");
        const inp = document.getElementById("numericField");
        const lbl = document.getElementById("numberPrompt");
        const detailedHint = document.getElementById("numberDetailedHint");
        const curr = document.getElementById("currencySymbol");

        lbl.textContent = tr(q.title_key);
        inp.value = appState.answers[q.id] || "";

        if (q.id === "max_price_uah") {{
          curr.classList.remove("hidden");
          const dMin = q.dynamic_min ?? 600;
          const dMax = q.dynamic_max ?? 4500;
          inp.placeholder = tr("budgetPlaceholder", {{ min: dMin.toLocaleString() }});
          detailedHint.textContent = tr("budgetHint", {{ min: dMin.toLocaleString(), max: dMax.toLocaleString() }});
        }} else if (q.id === "shoe_size") {{
          curr.classList.add("hidden");
          inp.placeholder = "42";
          detailedHint.textContent = q.ranges ? tr("sizeHint", {{ sizes: q.ranges.join(", ") }}) : "";
        }}
      }} else {{
        numBox.classList.add("hidden");
        optionsBox.classList.remove("hidden");
        const opts = isGoal
          ? ["running", "training", "hydration", "food", "recovery", "outdoors", "gear", "daily", "gift"]
          : ["any", ...q.options];

        const selectedVal = isGoal ? appState.goal : appState.answers[q.id];

        opts.forEach(val => {{
          const btn = document.createElement("button");
          btn.type = "button";
          const isSelected = selectedVal === val;
          btn.className = `p-4 rounded-xl border-2 text-left font-medium transition flex items-center justify-between text-sm sm:text-base ${{
            isSelected
              ? "bg-brand-500/15 border-brand-500 text-white ring-2 ring-brand-500/30"
              : "bg-slate-950/80 border-slate-800 text-slate-200 hover:border-slate-700 hover:bg-slate-800/50"
          }}`;

          const text = isGoal ? tr("goal_" + val) : optionLabel(q.id, val);
          btn.innerHTML = `<span class="pr-2 leading-snug">${{text}}</span>${{isSelected ? '<span class="text-brand-500 font-bold text-lg">✓</span>' : ''}}`;

          btn.onclick = () => {{
            if (isGoal) {{
              appState.goal = val;
            }} else {{
              appState.answers[q.id] = val;
            }}
            renderScreen();
          }};
          optionsBox.appendChild(btn);
        }});
      }}

      // Controls
      const isBudget = q.id === "max_price_uah";
      document.getElementById("btnBack").classList.toggle("hidden", appState.history.length === 0);
      document.getElementById("btnNext").classList.toggle("hidden", isBudget);
      document.getElementById("btnShowResults").classList.toggle("hidden", !isBudget);
    }}

    function advanceStep() {{
      const isGoal = appState.currentQuestionId === "goal";
      if (isGoal) {{
        if (!appState.goal) {{
          showErrorMessage(tr("errorRequired"));
          return;
        }}
        appState.history.push("goal");
        updateEnginePlan();
        if (appState.questionPlan.length === 0) {{
          renderFinalResults();
          return;
        }}
        appState.currentQuestionId = appState.questionPlan[0].id;
        renderScreen();
        return;
      }}

      const q = appState.questionPlan.find(item => item.id === appState.currentQuestionId);
      if (!q) return;

      if (q.type === "number") {{
        const raw = document.getElementById("numericField").value.trim();
        appState.answers[q.id] = raw === "" ? "any" : Number(raw);
      }}

      const currentVal = appState.answers[q.id];
      if (currentVal === undefined) {{
        showErrorMessage(tr("errorRequired"));
        return;
      }}

      appState.history.push(q.id);
      updateEnginePlan();

      const nextQ = appState.questionPlan.find(item => !appState.history.includes(item.id));
      if (!nextQ) {{
        renderFinalResults();
        return;
      }}
      appState.currentQuestionId = nextQ.id;
      renderScreen();
    }}

    function goBackStep() {{
      if (appState.history.length === 0) return;
      const prevId = appState.history.pop();
      if (prevId === "goal") {{
        appState.goal = "";
        appState.answers = {{}};
        appState.questionPlan = [];
        appState.currentQuestionId = "goal";
      }} else {{
        delete appState.answers[prevId];
        appState.currentQuestionId = prevId;
        updateEnginePlan();
      }}
      renderScreen();
    }}

    function updateEnginePlan() {{
      if (!appState.goal) {{
        appState.optionsData = draftOptions(appState.catalog);
        appState.questionPlan = [];
        return;
      }}
      appState.optionsData = draftOptions(appState.catalog, appState.goal, appState.answers);
      appState.questionPlan = appState.optionsData.question_plan || [];
    }}

    function showErrorMessage(msg) {{
      const alert = document.getElementById("errorAlert");
      document.getElementById("errorMessage").textContent = msg;
      alert.classList.remove("hidden");
    }}

    function createKitCard(item, badgeType = "match") {{
      const card = document.createElement("article");
      card.className = "p-5 rounded-2xl border border-slate-800 bg-slate-950/70 space-y-3.5 hover:border-slate-700 transition relative overflow-hidden";

      let badgeHtml = "";
      if (badgeType === "near_miss") {{
        badgeHtml = `<span class="px-2.5 py-1 rounded-md text-xs font-bold bg-amber-500/20 text-amber-300 border border-amber-500/30">+${{item.price_over_budget_uah}} ₴ до бюджету</span>`;
      }} else if (badgeType === "floor_anchor") {{
        badgeHtml = `<span class="px-2.5 py-1 rounded-md text-xs font-bold bg-purple-500/20 text-purple-300 border border-purple-500/30">Базовий старт</span>`;
      }} else if (item.match_score_pct) {{
        const color = item.match_score_pct >= 85 ? "bg-emerald-500/20 text-emerald-300 border-emerald-500/30" : "bg-blue-500/20 text-blue-300 border-blue-500/30";
        badgeHtml = `<span class="px-2.5 py-1 rounded-md text-xs font-bold ${{color}} border">${{item.match_score_pct}}% відповідність</span>`;
      }}

      const topRow = `
        <div class="flex items-center justify-between gap-2">
          <span class="text-xs font-mono text-slate-500">№ ${{item.catalog_row}} · ${{item.sku || 'RE-KIT'}}</span>
          <div class="flex items-center gap-2">${{badgeHtml}}</div>
        </div>
      `;

      const title = `<h3 class="text-lg font-bold text-white tracking-tight leading-snug">${{item.title}}</h3>`;

      const priceBlock = `
        <div class="flex items-baseline gap-2 pt-0.5">
          <span class="text-2xl font-bold font-mono text-brand-500">${{item.price_uah.toLocaleString()}} ₴</span>
          <span class="text-xs text-slate-500">${{tr("cardPrice")}} ${{item.price_snapshot_date}}</span>
        </div>
      `;

      const reasons = (item.reasons || []).map(r => `
        <li class="flex items-start gap-2 text-xs sm:text-sm text-slate-300">
          <span class="text-emerald-400 font-bold shrink-0">✓</span>
          <span>${{r}}</span>
        </li>
      `).join("");

      const reasonsBlock = reasons ? `<ul class="space-y-1.5 pt-2 border-t border-slate-900">${{reasons}}</ul>` : "";

      const notes = (item.data_notes || []).filter(n => !n.includes("Ціна й наявність") && !n.includes("Цена и наличие")).map(n => `
        <p class="text-xs text-amber-300/80 italic">⚠️ ${{n}}</p>
      `).join("");

      const cta = `
        <div class="pt-3">
          <a href="${{item.source_url}}" target="_blank" rel="noopener noreferrer" class="inline-flex items-center gap-2 px-4 py-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-xs sm:text-sm font-bold text-white transition">
            <span>${{tr("openCardBtn")}}</span>
          </a>
        </div>
      `;

      card.innerHTML = topRow + title + priceBlock + reasonsBlock + notes + cta;
      return card;
    }}

    function renderFinalResults() {{
      const req = {{
        goal_group: appState.goal,
        locale: appState.locale,
        ...appState.answers
      }};
      if (req.max_price_uah === "any") delete req.max_price_uah;
      if (req.shoe_size === "any") delete req.shoe_size;

      const res = draftRecommend(appState.catalog, req);

      document.getElementById("quizQuestionView").classList.add("hidden");
      document.getElementById("progressSection").classList.add("hidden");
      document.getElementById("quizResultsView").classList.remove("hidden");

      document.getElementById("resultsTitle").textContent = res.results.length > 0
        ? `Знайдено наборів: ${{res.returned_count}}`
        : "Підходящих наборів не знайдено";

      document.getElementById("resultMessageBanner").textContent = res.message;

      const cardsBox = document.getElementById("primaryCardsList");
      cardsBox.innerHTML = "";
      res.results.forEach(item => cardsBox.appendChild(createKitCard(item, "match")));

      const nearSec = document.getElementById("nearMissSection");
      const nearBox = document.getElementById("nearMissCardsList");
      nearBox.innerHTML = "";
      if (res.near_miss_results && res.near_miss_results.length > 0) {{
        nearSec.classList.remove("hidden");
        res.near_miss_results.forEach(item => nearBox.appendChild(createKitCard(item, "near_miss")));
      }} else {{
        nearSec.classList.add("hidden");
      }}

      const floorSec = document.getElementById("floorAnchorSection");
      const floorBox = document.getElementById("floorAnchorCardsList");
      floorBox.innerHTML = "";
      if (res.floor_anchor_results && res.floor_anchor_results.length > 0) {{
        floorSec.classList.remove("hidden");
        res.floor_anchor_results.forEach(item => floorBox.appendChild(createKitCard(item, "floor_anchor")));
      }} else {{
        floorSec.classList.add("hidden");
      }}
    }}

    // Event Bindings
    document.getElementById("btnNext").onclick = advanceStep;
    document.getElementById("btnShowResults").onclick = advanceStep;
    document.getElementById("btnBack").onclick = goBackStep;

    document.getElementById("btnRestart").onclick = () => {{
      appState.goal = "";
      appState.answers = {{}};
      appState.history = [];
      appState.currentQuestionId = "goal";
      updateEnginePlan();
      document.getElementById("quizResultsView").classList.add("hidden");
      document.getElementById("progressSection").classList.remove("hidden");
      document.getElementById("quizQuestionView").classList.remove("hidden");
      renderScreen();
    }};

    document.getElementById("btnUk").onclick = () => {{
      appState.locale = "uk";
      document.getElementById("btnUk").className = "px-2.5 py-1 rounded-md bg-brand-500 text-white transition shadow-sm";
      document.getElementById("btnRu").className = "px-2.5 py-1 rounded-md text-slate-400 hover:text-white transition";
      renderScreen();
    }};

    document.getElementById("btnRu").onclick = () => {{
      appState.locale = "ru";
      document.getElementById("btnRu").className = "px-2.5 py-1 rounded-md bg-brand-500 text-white transition shadow-sm";
      document.getElementById("btnUk").className = "px-2.5 py-1 rounded-md text-slate-400 hover:text-white transition";
      renderScreen();
    }};

    updateEnginePlan();
    renderScreen();
  </script>
</body>
</html>
"""
    template = template.replace("__CATALOG_JSON_STR__", catalog_json_str).replace("__CONSTANTS_JSON_STR__", constants_json_str)
    # Write to public/index.html and quiz.html in workspace root
    (ROOT / "public").mkdir(parents=True, exist_ok=True)
    (ROOT / "public" / "index.html").write_text(template, encoding="utf-8")
    (ROOT / "quiz.html").write_text(template, encoding="utf-8")
    print(f"Generated standalone public/index.html ({len(template.encode('utf-8')) / 1024:.1f} KB)")
    print(f"Generated standalone quiz.html ({len(template.encode('utf-8')) / 1024:.1f} KB)")

if __name__ == "__main__":
    build_external_html()
