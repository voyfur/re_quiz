// Standalone Client-side Matcher mirroring draft_matcher.py
(function() {
  const CONSTANTS = {"GOAL_FAMILIES": {"running": ["running_race_preparation"], "training": ["strength_muscle_training"], "hydration": ["hydration_electrolytes"], "food": ["portable_food_snacks", "endurance_energy"], "recovery": ["recovery_fatigue", "sleep_relaxation_stress"], "outdoors": ["outdoor_travel_hiking"], "gear": ["foot_apparel_comfort"], "daily": ["general_daily_nutrition"], "gift": ["gift_identity"]}, "GOAL_LABELS": {"ru": {"running": "Бег и старты", "training": "Тренировки и сила", "hydration": "Гидратация", "food": "Перекусы и питание", "recovery": "Восстановление и отдых", "outdoors": "Походы и активный отдых", "gear": "Одежда и аксессуары", "daily": "Ежедневное использование", "gift": "Подарок"}, "uk": {"running": "Біг і старти", "training": "Тренування та сила", "hydration": "Гідратація", "food": "Перекуси та харчування", "recovery": "Відновлення та відпочинок", "outdoors": "Походи й активний відпочинок", "gear": "Одяг та аксесуари", "daily": "Щоденне використання", "gift": "Подарунок"}}, "ACTIVITY_OPTIONS_BY_GOAL": {"running": [], "training": ["strength_training", "mind_body_mobility", "functional_training"], "hydration": ["cycling", "strength_training", "functional_training", "running"], "food": ["cycling", "hiking", "running"], "recovery": ["cycling", "strength_training", "mind_body_mobility", "functional_training", "running"], "outdoors": ["cycling", "walking", "hiking"], "gear": ["cycling", "swimming", "hiking", "walking", "running"], "daily": [], "gift": ["cycling", "swimming", "hiking", "walking", "strength_training", "running"]}, "COMPONENT_CLASSES_BY_GOAL": {"running": ["protein_carbohydrate_food", "apparel_footwear", "sports_accessories", "hydration_items"], "training": ["supplements_vitamins_minerals", "protein_carbohydrate_food", "creatine_preworkout", "hydration_items"], "hydration": ["protein_carbohydrate_food", "sports_accessories", "hydration_items"], "food": ["dehydrated_meal", "protein_carbohydrate_food", "hydration_items"], "recovery": ["protein_carbohydrate_food", "creatine_preworkout", "supplements_vitamins_minerals"], "outdoors": ["protein_carbohydrate_food", "dehydrated_meal", "apparel_footwear", "sports_accessories", "hydration_items"], "gear": ["apparel_footwear", "sports_accessories"], "daily": ["protein_carbohydrate_food", "supplements_vitamins_minerals"], "gift": ["supplements_vitamins_minerals", "protein_carbohydrate_food", "apparel_footwear", "sports_accessories", "hydration_items"]}, "USE_SCENARIOS_BY_GOAL": {"running": ["event_preparation", "training", "everyday"], "training": ["training", "everyday"], "hydration": ["event_preparation", "training", "everyday"], "food": ["event_preparation", "training", "everyday"], "recovery": ["training", "everyday"], "outdoors": ["training", "everyday"], "gear": ["event_preparation", "training", "everyday"], "daily": ["everyday"], "gift": ["event_preparation", "training", "everyday"]}, "USE_TIMINGS_BY_GOAL": {"running": ["daily_use", "during_training", "before_or_after_training"], "training": ["daily_use", "evening_or_bedtime", "during_training", "before_or_after_training"], "hydration": ["daily_use", "during_training", "before_or_after_training"], "food": ["daily_use", "during_training", "before_or_after_training"], "recovery": ["daily_use", "evening_or_bedtime", "during_training", "before_or_after_training"], "outdoors": ["daily_use", "during_training"], "gear": ["daily_use", "during_training"], "daily": ["daily_use", "evening_or_bedtime"], "gift": ["daily_use", "evening_or_bedtime", "during_training"]}, "USE_PLACES_BY_GOAL": {"running": ["hiking_or_camping", "travel_or_road"], "training": ["travel_or_road", "work_or_study"], "hydration": ["hiking_or_camping", "travel_or_road"], "food": ["hiking_or_camping", "travel_or_road"], "recovery": ["travel_or_road", "work_or_study"], "outdoors": ["hiking_or_camping", "travel_or_road"], "gear": ["hiking_or_camping", "travel_or_road"], "daily": ["travel_or_road", "work_or_study"], "gift": ["hiking_or_camping", "travel_or_road", "work_or_study"]}, "PRODUCT_FORMS_BY_GOAL": {"running": ["sticks", "liquid", "food_or_meal", "bars", "gel"], "training": ["sticks", "powder", "liquid", "capsules", "tablets", "softgels", "bars"], "hydration": ["liquid", "sticks", "gel", "bars"], "food": ["sticks", "liquid", "food_or_meal", "bars", "gel"], "recovery": ["sticks", "powder", "capsules", "tablets", "softgels"], "outdoors": ["sticks", "liquid", "food_or_meal", "bars", "gel"], "gear": [], "daily": ["tablets", "softgels", "powder", "capsules"], "gift": ["sticks", "capsules", "tablets", "softgels", "gel", "apparel", "liquid", "bars", "food_or_meal"]}, "SIZE_GOALS": ["gear", "outdoors", "gift", "running"], "CONFLICTED_COMPONENT_FAMILIES": {"RE11518": ["hydration_electrolytes"], "RE11807": ["*"], "RE11013": ["portable_food_snacks"], "Nabir_1133": ["general_daily_nutrition"]}, "CONFLICTED_COMPONENT_CLASSES": {"RE11518": ["sports_accessories"], "RE11807": ["*"], "RE11013": ["protein_carbohydrate_food"], "Nabir_1133": ["sports_accessories", "supplements_vitamins_minerals"]}};
  const CORE_ANSWER_FIELDS = ["activity"];
  const STEERING_ANSWER_FIELDS = ["component_class"];
  const SOFT_ANSWER_FIELDS = [
    "use_scenario", "use_timing", "use_place", "race_format", "season", "product_form"
  ];
  const ANSWER_SIGNAL_FIELDS = [...CORE_ANSWER_FIELDS, ...STEERING_ANSWER_FIELDS, ...SOFT_ANSWER_FIELDS];

  function asSet(val) {
    if (val === undefined || val === null || val === "" || val === "any") return new Set();
    if (Array.isArray(val)) return new Set(val.filter(v => v !== "" && v !== "any" && v != null));
    return new Set([val]);
  }

  function intersect(a, b) {
    const sB = b instanceof Set ? b : new Set(b);
    return new Set([...a].filter(x => sB.has(x)));
  }

  function membershipStatus(record) {
    const itemTypes = record.tags?.item_type || [];
    const comp = (record.composition || "").toLowerCase();
    const title = (record.title || "").toLowerCase();
    if (itemTypes.includes("club_membership_bundle") || comp.includes("абонемент") || comp.includes("membership")) return "included";
    if (title.includes("абонемент") || title.includes("membership")) return "included";
    if (title.includes("club") || title.includes("клуб")) return "mentioned";
    return "unknown";
  }

  function matchingFamilies(record, goalGroup) {
    const ev = record.matching_evidence || {};
    const wanted = new Set(CONSTANTS.GOAL_FAMILIES[goalGroup] || []);
    let seller = [...intersect(new Set(ev.seller_families || []), wanted)];
    let compSet = intersect(new Set(ev.component_families || []), wanted);
    const blocked = new Set(CONSTANTS.CONFLICTED_COMPONENT_FAMILIES[record.sku] || []);
    if (blocked.has("*")) compSet.clear();
    else blocked.forEach(b => compSet.delete(b));
    return { seller, components: [...compSet] };
  }

  function goalCandidates(catalog, goalGroup) {
    const list = [];
    for (const r of catalog) {
      const mf = matchingFamilies(r, goalGroup);
      if (mf.seller.length > 0 || mf.components.length > 0) {
        list.push([r, mf.seller, mf.components]);
      }
    }
    return list;
  }

  function sizeRanges(record) {
    const ranges = [];
    const vals = record.matching_evidence?.size_values || [];
    for (const item of vals) {
      if (item.type !== "shoe_or_sock_size") continue;
      const str = String(item.value || "").replace("–", "-");
      const parts = str.split("-");
      const lower = parseInt(parts[0], 10);
      const upper = parseInt(parts[parts.length - 1], 10);
      if (!isNaN(lower) && !isNaN(upper)) ranges.push([lower, upper]);
    }
    return ranges;
  }

  function seasonGroups(record) {
    const sigs = new Set(record.matching_evidence?.weather_signals || []);
    const res = new Set();
    if (sigs.has("cold_weather") || sigs.has("winter")) res.add("cold");
    if (sigs.has("hot_weather") || sigs.has("summer")) res.add("warm");
    return res;
  }

  function softSignals(record, key) {
    const ev = record.matching_evidence || {};
    if (key === "activity") {
      return new Set([...(ev.seller_activity_groups || []), ...(ev.component_activity_groups || [])]);
    }
    if (key === "component_class") {
      return new Set(ev.component_classes || []);
    }
    if (key === "use_scenario" || key === "use_timing" || key === "use_place") {
      const vals = new Set(ev.use_contexts || []);
      if (key === "use_scenario") {
        const sc = new Set();
        const races = (ev.race_formats || []).filter(x => x !== "unspecified");
        if (races.length > 0) sc.add("event_preparation");
        if (vals.has("before_or_after_training") || vals.has("during_training")) sc.add("training");
        if (vals.has("daily_use") || vals.has("evening_or_bedtime") || vals.has("work_or_study")) sc.add("everyday");
        return sc;
      }
      if (key === "use_timing") {
        return intersect(vals, ["before_or_after_training", "during_training", "daily_use", "evening_or_bedtime"]);
      }
      if (key === "use_place") {
        return intersect(vals, ["hiking_or_camping", "travel_or_road", "work_or_study"]);
      }
      return vals;
    }
    if (key === "race_format") {
      return new Set((ev.race_formats || []).filter(x => x !== "unspecified"));
    }
    if (key === "season") return seasonGroups(record);
    if (key === "product_form") return new Set(ev.product_forms || []);
    return new Set();
  }

  function candidateFit(candidate, answers) {
    const record = candidate[0];
    const maxPrice = answers.max_price_uah;
    const price = record.price_uah;
    if (maxPrice !== undefined && maxPrice !== null && (typeof price !== "number" || price > maxPrice)) {
      return null;
    }
    const memPref = answers.membership;
    if (memPref === "yes" && membershipStatus(record) !== "included") return null;
    if (memPref === "no" && ["included", "mentioned"].includes(membershipStatus(record))) return null;

    const matched = [];
    const unknown = [];
    const relaxed = [];
    const relaxedValues = {};

    for (const key of ANSWER_SIGNAL_FIELDS) {
      const vals = asSet(answers[key]);
      if (vals.size === 0) continue;
      if (key === "activity" && vals.has("other")) {
        matched.push(key);
        continue;
      }
      const sigs = softSignals(record, key);
      if (sigs.size === 0) {
        if (STEERING_ANSWER_FIELDS.includes(key)) return null;
        unknown.push(key);
      } else if (intersect(vals, sigs).size > 0) {
        matched.push(key);
      } else if (CORE_ANSWER_FIELDS.includes(key) || STEERING_ANSWER_FIELDS.includes(key)) {
        return null;
      } else {
        relaxed.push(key);
        relaxedValues[key] = vals.size > 1 ? [...vals].sort() : [...vals][0];
      }
    }

    let sizeMatch = false;
    let sizeStatus = "not_requested";
    const size = answers.shoe_size;
    if (size !== undefined && size !== null && size !== "" && size !== "any") {
      const numSize = Number(size);
      const ranges = sizeRanges(record);
      if (ranges.length > 0) {
        sizeMatch = ranges.some(([lo, hi]) => numSize >= lo && numSize <= hi);
        if (!sizeMatch) return null;
        sizeStatus = "matched";
        matched.push("shoe_size");
      } else if (record.matching_evidence?.size_sensitive) {
        sizeStatus = "unknown";
        unknown.push("shoe_size");
      }
    }

    const matchType = relaxed.length > 0 ? "relaxed" : unknown.length > 0 ? "general" : "exact";
    return {
      match_type: matchType,
      matched_preferences: matched,
      unknown_preferences: unknown,
      relaxed_preferences: relaxed,
      relaxed_preference_values: relaxedValues,
      size_match: sizeMatch,
      size_status: sizeStatus
    };
  }

  function candidatePools(candidates, answers) {
    const pools = { exact: [], general: [], relaxed: [] };
    for (const c of candidates) {
      const fit = candidateFit(c, answers);
      if (fit) pools[fit.match_type].push([c, fit]);
    }
    return pools;
  }

  function valuesIn(candidates, key, allowed) {
    const s = new Set();
    const allowSet = new Set(allowed);
    for (const [r] of candidates) {
      for (const val of softSignals(r, key)) {
        if (allowSet.has(val)) s.add(val);
      }
    }
    return [...s].sort();
  }

  function wouldSplit(candidates, key, allowed, minSignals = 2) {
    let count = 0;
    const allowSet = new Set(allowed);
    for (const [r] of candidates) {
      if (intersect(softSignals(r, key), allowSet).size > 0) count++;
    }
    return count >= minSignals;
  }

  function questionPlan(candidates, goalGroup, answers) {
    const questions = [];
    const add = (id, options, title_key) => {
      if (options && options.length > 0) {
        questions.push({ id, title_key, options, type: "single" });
      }
    };

    const remaining = candidates;
    const answered = answers || {};

    // Early termination: if <= 3 candidates remain or user already answered 2 follow-up questions, skip directly to budget
    const answeredFollowups = Object.keys(answered).filter(k => !["max_price_uah", "locale"].includes(k));
    if (remaining.length <= 3 || answeredFollowups.length >= 2) {
      if (remaining.length > 0 && !("max_price_uah" in answered)) {
        const prices = remaining.map(([r]) => r.price_uah).filter(p => typeof p === "number");
        questions.push({
          id: "max_price_uah",
          title_key: "question_budget",
          type: "number",
          min: 0,
          dynamic_min: prices.length ? Math.min(...prices) : null,
          dynamic_max: prices.length ? Math.max(...prices) : null
        });
      }
      return questions;
    }

    // 1. Primary filter: Component Class (What type of product do you need in the kit?)
    if (!("component_class" in answered)) {
      const vals = valuesIn(remaining, "component_class", CONSTANTS.COMPONENT_CLASSES_BY_GOAL[goalGroup] || []);
      if (vals.length > 1) add("component_class", vals, "question_component_class");
    }

    // 2. Activity (Sport): only for sport-specific goals where sport is a deciding factor; NEVER for recovery or daily
    if (!("activity" in answered) && !["recovery", "daily"].includes(goalGroup)) {
      let vals = valuesIn(remaining, "activity", CONSTANTS.ACTIVITY_OPTIONS_BY_GOAL[goalGroup] || []);
      if (vals.length > 1) {
        vals = [...new Set([...vals, "other"])].sort();
        add("activity", vals, "question_activity");
      }
    }

    // 3. Contextual Refinement (Choose at most ONE high-signal question based on component_class):
    const compClass = answered.component_class;

    // A. If Apparel / Footwear: ask shoe_size and season
    if (compClass === "apparel_footwear" || (goalGroup === "gear" && compClass !== "sports_accessories")) {
      if (!("shoe_size" in answered)) {
        const hasSize = remaining.some(([r]) => r.matching_evidence?.size_sensitive && sizeRanges(r).length > 0);
        if (hasSize) {
          const s = new Set();
          remaining.forEach(([r]) => {
            sizeRanges(r).forEach(([lo, hi]) => s.add(`${lo}-${hi}`));
          });
          questions.push({
            id: "shoe_size",
            title_key: "question_shoe_size",
            type: "number",
            min: 1,
            max: 70,
            ranges: [...s].sort()
          });
        }
      }
      if (!("season" in answered)) {
        const allowed = ["cold", "warm"];
        const vals = valuesIn(remaining, "season", allowed);
        if (vals.length > 1 && wouldSplit(remaining, "season", allowed)) {
          add("season", vals, "question_season");
        }
      }
    }
    // B. If Recovery: ask timing (evening/bedtime vs post-training); NEVER ask place for bedtime!
    else if (goalGroup === "recovery" || compClass === "supplements_vitamins_minerals") {
      if (!("use_timing" in answered)) {
        const allowed = CONSTANTS.USE_TIMINGS_BY_GOAL[goalGroup] || [];
        const vals = valuesIn(remaining, "use_timing", allowed);
        if (vals.length > 1 && wouldSplit(remaining, "use_timing", allowed)) {
          add("use_timing", vals, "question_use_timing");
        }
      }
    }
    // C. If Running nutrition/hydration: check race format only if event preparation
    else if (goalGroup === "running") {
      if (!("use_scenario" in answered)) {
        const allowed = CONSTANTS.USE_SCENARIOS_BY_GOAL[goalGroup] || [];
        const vals = valuesIn(remaining, "use_scenario", allowed);
        if (vals.length > 1 && wouldSplit(remaining, "use_scenario", allowed)) {
          add("use_scenario", vals, "question_use_scenario");
        }
      } else if (answered.use_scenario === "event_preparation" && !("race_format" in answered)) {
        const allowed = ["half_marathon", "marathon", "race_or_event_preparation", "ultra_or_long_distance"];
        const vals = valuesIn(remaining, "race_format", allowed);
        if (vals.length > 1 && wouldSplit(remaining, "race_format", allowed)) {
          add("race_format", vals, "question_race_format");
        }
      }
    }
    // D. If Outdoors: ask camping vs travel or dehydrated meal form
    else if (goalGroup === "outdoors") {
      if (!("use_place" in answered)) {
        const allowed = CONSTANTS.USE_PLACES_BY_GOAL[goalGroup] || [];
        const vals = valuesIn(remaining, "use_place", allowed);
        if (vals.length > 1 && wouldSplit(remaining, "use_place", allowed)) {
          add("use_place", vals, "question_use_place");
        }
      }
    }

    // Product form: ask only if forms vary and not apparel
    if (!("product_form" in answered) && compClass !== "apparel_footwear") {
      const allowed = CONSTANTS.PRODUCT_FORMS_BY_GOAL[goalGroup] || [];
      const vals = valuesIn(remaining, "product_form", allowed);
      if (vals.length > 1 && wouldSplit(remaining, "product_form", allowed, 3)) {
        add("product_form", vals, "question_product_form");
      }
    }

    if (remaining.length > 0 && !("max_price_uah" in answered)) {
      const prices = remaining.map(([r]) => r.price_uah).filter(p => typeof p === "number");
      questions.push({
        id: "max_price_uah",
        title_key: "question_budget",
        type: "number",
        min: 0,
        dynamic_min: prices.length ? Math.min(...prices) : null,
        dynamic_max: prices.length ? Math.max(...prices) : null
      });
    }

    return questions;
  }

  function calculateMatchScore(record, sellerFamilies, componentFamilies, fit, validated) {
    let evScore = 0;
    if (sellerFamilies.length > 0) evScore += 20;
    if (componentFamilies.length > 0) evScore += 15;
    if (record.matching_evidence?.status === "conflict_review_required") {
      evScore = Math.max(5, evScore - 5);
    }

    const activeKeys = ANSWER_SIGNAL_FIELDS.filter(k => asSet(validated[k]).size > 0);
    let prefScore = 45;
    if (activeKeys.length > 0) {
      const matchedSet = new Set(fit.matched_preferences || []);
      const unknownSet = new Set(fit.unknown_preferences || []);
      let pts = 0;
      activeKeys.forEach(k => {
        if (matchedSet.has(k)) pts += 1.0;
        else if (unknownSet.has(k)) pts += 0.55;
      });
      prefScore = Math.round(45 * (pts / activeKeys.length));
    }

    let fitScore = 0;
    if (validated.shoe_size === undefined || validated.shoe_size === null) fitScore += 10;
    else if (fit.size_status === "matched") fitScore += 10;
    else if (fit.size_status === "unknown") fitScore += 5;

    const maxP = validated.max_price_uah;
    const price = record.price_uah || 0;
    if (maxP === undefined || maxP === null) fitScore += 10;
    else if (typeof price === "number" && price <= maxP) {
      fitScore += price <= maxP * 0.85 ? 10 : 9;
    } else if (typeof price === "number" && price > maxP) {
      const over = price - maxP;
      const pct = over / Math.max(1, maxP);
      fitScore += Math.max(0, Math.round(10 * Math.max(0, 1 - 2.5 * pct)));
    }

    let total = Math.min(99, Math.max(15, evScore + prefScore + fitScore));
    const mt = fit.match_type;
    if (mt === "exact" && (maxP == null || price <= maxP)) total = Math.max(88, total);
    else if (mt === "general" && (maxP == null || price <= maxP)) total = Math.min(87, Math.max(72, total));
    else if (mt === "near_miss") total = Math.min(84, Math.max(60, total));
    else if (mt === "floor_anchor") total = Math.min(75, Math.max(45, total));
    else if (mt === "relaxed") total = Math.min(68, Math.max(35, total));

    return {
      total,
      breakdown: { evidence: evScore, preferences: prefScore, constraints: fitScore }
    };
  }

  function findBudgetNearMisses(goalCands, validated, maxDeltaPct = 0.25, maxDeltaUah = 350) {
    const maxP = validated.max_price_uah;
    if (maxP === undefined || maxP === null) return [];
    const answersNoPrice = { ...validated };
    delete answersNoPrice.max_price_uah;
    const maxAllowed = Math.max(Math.floor(maxP * (1 + maxDeltaPct)), maxP + maxDeltaUah);
    const nearMisses = [];

    for (const cand of goalCands) {
      const r = cand[0];
      const p = r.price_uah;
      if (typeof p !== "number" || p <= maxP || p > maxAllowed) continue;
      const fit = candidateFit(cand, answersNoPrice);
      if (fit && ["exact", "general"].includes(fit.match_type)) {
        const copy = { ...fit, match_type: "near_miss", price_over_budget_uah: p - maxP };
        nearMisses.push([cand, copy]);
      }
    }

    nearMisses.sort((a, b) => {
      const diffOver = a[1].price_over_budget_uah - b[1].price_over_budget_uah;
      if (diffOver !== 0) return diffOver;
      return a[0][0].catalog_row - b[0][0].catalog_row;
    });
    return nearMisses.slice(0, 3);
  }

  function findFloorAnchor(goalCands, validated) {
    const maxP = validated.max_price_uah;
    if (maxP === undefined || maxP === null) return [];
    const answersNoPrice = { ...validated };
    delete answersNoPrice.max_price_uah;
    const pools = candidatePools(goalCands, answersNoPrice);
    const comp = pools.exact.length ? pools.exact : pools.general;
    if (!comp.length) return [];

    const over = comp
      .filter(([cand]) => typeof cand[0].price_uah === "number" && cand[0].price_uah > maxP)
      .sort((a, b) => a[0][0].price_uah - b[0][0].price_uah || a[0][0].catalog_row - b[0][0].catalog_row);

    return over.slice(0, 2).map(([cand, fit]) => [
      cand,
      {
        ...fit,
        match_type: "floor_anchor",
        price_over_budget_uah: cand[0].price_uah - maxP,
        floor_price_uah: cand[0].price_uah
      }
    ]);
  }

  function buildResultItem(record, seller, comp, fit, locale, validated, stockInfo = null) {
    const ev = record.matching_evidence || {};
    const reasons = [];
    const goalLabel = CONSTANTS.GOAL_LABELS[locale]?.[record.selected_goal] || record.selected_goal;

    if (seller.length > 0) {
      reasons.push(locale === "uk" ? `Продавець позиціонує набір для теми «${goalLabel}».` : `Продавец позиционирует набор для темы «${goalLabel}».`);
    }
    if (comp.length > 0) {
      reasons.push(locale === "uk" ? "У переліку складу є товар, пов'язаний із цією задачею." : "В списке состава есть товар, связанный с этой задачей.");
    }

    const prefLabels = {
      activity: ["активности", "активності"],
      component_class: ["типу товара в наборе", "типу товару в наборі"],
      use_scenario: ["сценарию", "сценарію"],
      use_timing: ["времени использования", "часу використання"],
      use_place: ["месту использования", "місцю використання"],
      race_format: ["формату старта", "формату старту"],
      season: ["погоде", "погоді"],
      product_form: ["форме товара", "формі товару"]
    };

    (fit.matched_preferences || []).forEach(k => {
      if (k === "shoe_size") return;
      if (prefLabels[k]) {
        const label = locale === "uk" ? prefLabels[k][1] : prefLabels[k][0];
        reasons.push(locale === "uk" ? `Є збіг за ${label}.` : `Есть совпадение по ${label}.`);
      }
    });

    if (fit.size_match) {
      reasons.push(locale === "uk" ? "Вказаний розмір входить у діапазон товару." : "Указанный размер входит в диапазон товара.");
    }
    if (fit.match_type === "near_miss") {
      const over = fit.price_over_budget_uah || 0;
      reasons.push(locale === "uk" ? `Перевищує вибраний бюджет на ${over} ₴.` : `Превышает выбранный бюджет на ${over} ₴.`);
    } else if (fit.match_type === "floor_anchor") {
      const floorP = fit.floor_price_uah;
      const over = fit.price_over_budget_uah || 0;
      reasons.push(locale === "uk" ? `Мінімальний базовий набір у категорії (від ${floorP} ₴, різниця ${over} ₴).` : `Минимальный базовый набор в категории (от ${floorP} ₴, разница ${over} ₴).`);
    }

    const notes = [];
    if (fit.size_status === "unknown") {
      notes.push(locale === "uk" ? "Розмір товару не вказаний у знімку; збіг не підтверджено." : "Размер товара не указан в снимке; совпадение не подтверждено.");
    }
    if (ev.status === "conflict_review_required") {
      notes.push(locale === "uk" ? "У картці є невирішена розбіжність складу; перевірте актуальну сторінку." : "В карточке есть неразрешённое расхождение состава; проверьте актуальную страницу.");
    }

    if (stockInfo && stockInfo.is_live_check) {
      if (stockInfo.in_stock) {
        notes.push(locale === "uk" ? "Наявність підтверджена за базою магазину: в наявності." : "Наличие подтверждено по базе магазина: в наличии.");
      } else {
        const statusText = (locale === "uk" ? stockInfo.stock_status_text_uk : stockInfo.stock_status_text_ru) || (locale === "uk" ? "Немає в наявності" : "Нет в наличии");
        notes.push(locale === "uk" ? `Статус на складі магазину: ${statusText}.` : `Статус на складе магазина: ${statusText}.`);
      }
      if (stockInfo.live_price_uah != null && Math.abs(stockInfo.live_price_uah - record.price_uah) >= 1) {
        notes.push(locale === "uk" ? `Актуальна ціна на сайті: ${stockInfo.live_price_uah} ₴ (у каталозі було ${record.price_uah} ₴).` : `Актуальная цена на сайте: ${stockInfo.live_price_uah} ₴ (в каталоге было ${record.price_uah} ₴).`);
      }
    } else {
      notes.push(locale === "uk" ? "Ціна й наявність не оновлюються в реальному часі." : "Цена и наличие не обновляются в реальном времени.");
    }

    const scoreData = calculateMatchScore(record, seller, comp, fit, validated);
    const currentPriceUah = (stockInfo && stockInfo.live_price_uah != null) ? stockInfo.live_price_uah : record.price_uah;

    return {
      set_id: record.set_id,
      catalog_row: record.catalog_row,
      sku: record.sku,
      title: record.title,
      source_url: record.source_url,
      price_uah: currentPriceUah,
      catalog_price_uah: record.price_uah,
      stock_info: stockInfo || {
        sku: record.sku,
        in_stock: true,
        quantity: null,
        status: 1,
        live_price_uah: record.price_uah,
        stock_status_text_uk: "В наявності",
        stock_status_text_ru: "В наличии",
        is_live_check: false
      },
      price_snapshot_date: record.price_snapshot_date,
      match_type: fit.match_type,
      match_score_pct: scoreData.total,
      score_breakdown: scoreData.breakdown,
      price_over_budget_uah: fit.price_over_budget_uah || 0,
      unknown_preferences: fit.unknown_preferences || [],
      relaxed_preferences: fit.relaxed_preferences || [],
      relaxed_preference_values: fit.relaxed_preference_values || {},
      evidence_status: ev.status || "unknown",
      membership_status: membershipStatus(record),
      size_status: fit.size_status,
      reasons,
      data_notes: notes
    };
  }

  function draftOptions(catalog, goalGroup, answers = {}) {
    if (!goalGroup) {
      const opts = [];
      for (const val of Object.keys(CONSTANTS.GOAL_FAMILIES)) {
        const cands = goalCandidates(catalog, val);
        if (cands.length > 0) {
          opts.push({ value: val, label: CONSTANTS.GOAL_LABELS.ru[val], count: cands.length });
        }
      }
      return { test_only: true, goal_options: opts, catalog_count: catalog.length };
    }

    const candidates = goalCandidates(catalog, goalGroup);
    const pools = candidatePools(candidates, { ...answers, goal_group: goalGroup });
    const remaining = [...pools.exact, ...pools.general].map(([cand]) => cand);
    const priceSource = remaining.length ? remaining : candidates;
    const prices = priceSource.map(([r]) => r.price_uah).filter(p => typeof p === "number");

    return {
      test_only: true,
      goal_group: goalGroup,
      candidate_count: remaining.length,
      exact_candidate_count: pools.exact.length,
      general_candidate_count: pools.general.length,
      relaxed_candidate_count: pools.relaxed.length,
      question_plan: questionPlan(remaining, goalGroup, answers),
      price_range_uah: prices.length ? { min: Math.min(...prices), max: Math.max(...prices) } : null,
      price_snapshot_date: priceSource[0]?.[0]?.price_snapshot_date || null
    };
  }

  function draftRecommend(catalog, request) {
    const goalGroup = request.goal_group;
    const locale = request.locale === "uk" ? "uk" : "ru";
    const candidates = goalCandidates(catalog, goalGroup);
    const pools = candidatePools(candidates, request);
    const fallbackMode = request.fallback_mode;

    let selectedPool = [];
    let status = "no_match";

    if (fallbackMode && pools[fallbackMode]) {
      selectedPool = pools[fallbackMode];
      status = fallbackMode;
    } else if (pools.exact.length > 0) {
      selectedPool = pools.exact;
      status = "matched";
    } else if (pools.general.length > 0) {
      selectedPool = pools.general;
      status = "general_auto";
    } else {
      selectedPool = [];
      status = pools.relaxed.length > 0 ? "no_exact_match" : "no_match";
    }

    const stockMap = request.stock_map || {};
    selectedPool.sort((a, b) => {
      const [candA, fitA] = a;
      const [candB, fitB] = b;
      const skuA = candA[0].sku || "";
      const skuB = candB[0].sku || "";
      const inStockA = stockMap[skuA] ? (stockMap[skuA].in_stock ? 1 : 0) : 1;
      const inStockB = stockMap[skuB] ? (stockMap[skuB].in_stock ? 1 : 0) : 1;
      if (inStockB !== inStockA) return inStockB - inStockA;
      const bothA = candA[1].length && candA[2].length ? 1 : 0;
      const bothB = candB[1].length && candB[2].length ? 1 : 0;
      if (bothB !== bothA) return bothB - bothA;
      const diffMatched = (fitB.matched_preferences?.length || 0) - (fitA.matched_preferences?.length || 0);
      if (diffMatched !== 0) return diffMatched;
      return (candA[0].price_uah || 0) - (candB[0].price_uah || 0) || candA[0].catalog_row - candB[0].catalog_row;
    });

    const results = selectedPool.slice(0, 3).map(([cand, fit]) => {
      const sInfo = stockMap[cand[0].sku] || null;
      return buildResultItem({ ...cand[0], selected_goal: goalGroup }, cand[1], cand[2], fit, locale, request, sInfo);
    });

    let nearMissResults = [];
    if (results.length < 3 && request.max_price_uah != null) {
      const rawNear = findBudgetNearMisses(candidates, request);
      const existing = new Set(results.map(r => r.catalog_row));
      nearMissResults = rawNear
        .filter(([cand]) => !existing.has(cand[0].catalog_row))
        .slice(0, 3)
        .map(([cand, fit]) => {
          const sInfo = stockMap[cand[0].sku] || null;
          return buildResultItem({ ...cand[0], selected_goal: goalGroup }, cand[1], cand[2], fit, locale, request, sInfo);
        });
    }

    let floorAnchorResults = [];
    if (!results.length && !nearMissResults.length && request.max_price_uah != null) {
      const rawFloor = findFloorAnchor(candidates, request);
      floorAnchorResults = rawFloor.slice(0, 2).map(([cand, fit]) => {
        const sInfo = stockMap[cand[0].sku] || null;
        return buildResultItem({ ...cand[0], selected_goal: goalGroup }, cand[1], cand[2], fit, locale, request, sInfo);
      });
      if (floorAnchorResults.length > 0) status = "floor_anchor";
    }

    const fallbackOptions = [];
    if (status === "general_auto" || status === "no_exact_match") {
      if (pools.relaxed.length > 0) fallbackOptions.push({ mode: "relaxed", count: pools.relaxed.length });
    } else if (fallbackMode) {
      const other = fallbackMode === "general" ? "relaxed" : "general";
      if (pools[other].length > 0) fallbackOptions.push({ mode: other, count: pools[other].length });
    }

    const messages = {
      ru: {
        matched: "Найдены варианты, у которых все указанные ответы подтверждаются сигналами снимка каталога.",
        general_auto: "Точного совпадения по всем ответам нет. Показаны варианты без известных противоречий; часть данных не подтверждена.",
        no_exact_match: "Точного совпадения по подтверждённым данным нет. Ниже можно отдельно посмотреть варианты с ослаблением мягких предпочтений.",
        general: "Эти варианты не имеют известных противоречий ответам, но некоторые предпочтения не подтверждены данными каталога.",
        relaxed: "Эти варианты показаны по вашему запросу с ослаблением мягких предпочтений.",
        no_match: "По ответам и жёстким ограничениям подходящих вариантов нет.",
        floor_anchor: "По выбранному бюджету наборов нет. В этой категории базовые наборы начинаются от {floor} ₴. Ниже предложен стартовый вариант."
      },
      uk: {
        matched: "Знайдено варіанти, для яких усі вказані відповіді підтверджуються сигналами знімка каталогу.",
        general_auto: "Точного збігу за всіма відповідями немає. Показано варіанти без відомих суперечностей; частина даних не підтверджена.",
        no_exact_match: "Точного збігу за підтвердженими даними немає. Нижче можна окремо переглянути варіанти з послабленням переваг.",
        general: "Ці варіанти не мають відомих суперечностей із відповідями, але деякі переваги не підтверджені даними каталогу.",
        relaxed: "Ці варіанти показано на ваш запит із послабленням м’яких переваг.",
        no_match: "За відповідями та жорсткими обмеженнями відповідних варіантів немає.",
        floor_anchor: "За вибраним бюджетом наборів немає. У цій категорії базові набори починаються від {floor} ₴. Нижче запропоновано стартовий варіант."
      }
    };

    let msg = messages[locale]?.[status] || "";
    if (status === "floor_anchor" && floorAnchorResults.length > 0) {
      const floorMin = Math.min(...floorAnchorResults.map(r => r.price_uah));
      msg = msg.replace("{floor}", floorMin);
    }
    if (!results.length && nearMissResults.length > 0) {
      msg += locale === "uk" ? " Нижче запропоновано варіанти з невеликим перевищенням бюджету." : " Ниже предложены варианты с небольшим превышением бюджета.";
    }

    return {
      status,
      test_only: true,
      alternatives: results.length > 1,
      returned_count: results.length,
      exact_count: pools.exact.length,
      general_count: pools.general.length,
      relaxed_count: pools.relaxed.length,
      near_miss_count: nearMissResults.length,
      floor_anchor_count: floorAnchorResults.length,
      floor_price_uah: floorAnchorResults.length ? Math.min(...floorAnchorResults.map(r => r.price_uah)) : null,
      fallback_options: fallbackOptions,
      message: msg,
      price_snapshot_date: catalog[0]?.price_snapshot_date || null,
      results,
      near_miss_results: nearMissResults,
      floor_anchor_results: floorAnchorResults
    };
  }

  window.QUIZ_MATCHER = {
    draftOptions,
    draftRecommend,
    handleRequest: async function(url, opts = {}) {
      const catalog = window.QUIZ_CATALOG || [];
      const parsedUrl = new URL(url, window.location.href);
      const path = parsedUrl.pathname;
      if (path.endsWith("/options")) {
        const params = parsedUrl.searchParams;
        const goal = params.get("goal_group");
        const answers = {};
        params.forEach((v, k) => {
          if (k !== "goal_group" && v) answers[k] = v;
        });
        return draftOptions(catalog, goal, answers);
      }
      if (path.endsWith("/recommend")) {
        const body = typeof opts.body === "string" ? JSON.parse(opts.body) : (opts.body || {});
        return draftRecommend(catalog, body);
      }
      throw new Error("Unhandled local path: " + path);
    }
  };
})();
