"""Evidence-tiered matcher for the first buyer-facing quiz preview."""

try:
    from stock_checker import check_stock
except Exception:
    def check_stock(skus):
        return {}

GOAL_FAMILIES = {
    "running": {"running_race_preparation"},
    "training": {"strength_muscle_training"},
    "hydration": {"hydration_electrolytes"},
    "food": {"portable_food_snacks", "endurance_energy"},
    "recovery": {"recovery_fatigue", "sleep_relaxation_stress"},
    "outdoors": {"outdoor_travel_hiking"},
    "gear": {"foot_apparel_comfort"},
    "daily": {"general_daily_nutrition"},
    "gift": {"gift_identity"},
}

GOAL_LABELS = {
    "ru": {
        "running": "Бег и старты",
        "training": "Тренировки и сила",
        "hydration": "Гидратация",
        "food": "Перекусы и питание",
        "recovery": "Восстановление и отдых",
        "outdoors": "Походы и активный отдых",
        "gear": "Одежда и аксессуары",
        "daily": "Ежедневное использование",
        "gift": "Подарок",
    },
    "uk": {
        "running": "Біг і старти",
        "training": "Тренування та сила",
        "hydration": "Гідратація",
        "food": "Перекуси та харчування",
        "recovery": "Відновлення та відпочинок",
        "outdoors": "Походи й активний відпочинок",
        "gear": "Одяг та аксесуари",
        "daily": "Щоденне використання",
        "gift": "Подарунок",
    },
}

# These families depend on a disputed component in the current evidence map.
# Seller-positioned signals remain usable; affected component signals do not.
CONFLICTED_COMPONENT_FAMILIES = {
    "RE11518": {"hydration_electrolytes"},
    "RE11807": {"*"},
    "RE11013": {"portable_food_snacks"},
    "Nabir_1133": {"general_daily_nutrition"},
}
CONFLICTED_COMPONENT_CLASSES = {
    "RE11518": {"sports_accessories"},
    "RE11807": {"*"},
    "RE11013": {"protein_carbohydrate_food"},
    "Nabir_1133": {"sports_accessories", "supplements_vitamins_minerals"},
}

# The activity branch is deliberately different by the selected buyer need.
ACTIVITY_OPTIONS_BY_GOAL = {
    "running": set(),
    "training": {"strength_training", "functional_training", "mind_body_mobility"},
    "hydration": {"running", "cycling", "strength_training", "functional_training"},
    "food": {"running", "cycling", "hiking"},
    "recovery": {"running", "cycling", "strength_training", "functional_training", "mind_body_mobility"},
    "outdoors": {"hiking", "walking", "cycling"},
    "gear": {"running", "hiking", "cycling", "walking", "swimming"},
    "daily": set(),
    "gift": {"running", "cycling", "strength_training", "hiking", "swimming", "walking"},
}

COMPONENT_CLASSES_BY_GOAL = {
    "running": {"protein_carbohydrate_food", "hydration_items", "sports_accessories", "apparel_footwear"},
    "training": {"supplements_vitamins_minerals", "creatine_preworkout", "protein_carbohydrate_food", "hydration_items"},
    "hydration": {"hydration_items", "protein_carbohydrate_food", "sports_accessories"},
    "food": {"protein_carbohydrate_food", "hydration_items", "dehydrated_meal"},
    "recovery": {"supplements_vitamins_minerals", "creatine_preworkout", "protein_carbohydrate_food"},
    "outdoors": {"dehydrated_meal", "protein_carbohydrate_food", "hydration_items", "sports_accessories", "apparel_footwear"},
    "gear": {"apparel_footwear", "sports_accessories"},
    "daily": {"supplements_vitamins_minerals", "protein_carbohydrate_food"},
    "gift": {"protein_carbohydrate_food", "supplements_vitamins_minerals", "sports_accessories", "apparel_footwear", "hydration_items"},
}

USE_SCENARIOS_BY_GOAL = {
    "running": {"event_preparation", "training", "everyday"},
    "training": {"training", "everyday"},
    "hydration": {"event_preparation", "training", "everyday"},
    "food": {"event_preparation", "training", "everyday"},
    "recovery": {"training", "everyday"},
    "outdoors": {"training", "everyday"},
    "gear": {"event_preparation", "training", "everyday"},
    "daily": {"everyday"},
    "gift": {"event_preparation", "training", "everyday"},
}

USE_TIMINGS_BY_GOAL = {
    "running": {"before_or_after_training", "during_training", "daily_use"},
    "training": {"before_or_after_training", "during_training", "daily_use", "evening_or_bedtime"},
    "hydration": {"before_or_after_training", "during_training", "daily_use"},
    "food": {"before_or_after_training", "during_training", "daily_use"},
    "recovery": {"before_or_after_training", "during_training", "daily_use", "evening_or_bedtime"},
    "outdoors": {"during_training", "daily_use"},
    "gear": {"during_training", "daily_use"},
    "daily": {"daily_use", "evening_or_bedtime"},
    "gift": {"daily_use", "during_training", "evening_or_bedtime"},
}

USE_PLACES_BY_GOAL = {
    "running": {"travel_or_road", "hiking_or_camping"},
    "training": {"work_or_study", "travel_or_road"},
    "hydration": {"travel_or_road", "hiking_or_camping"},
    "food": {"travel_or_road", "hiking_or_camping"},
    "recovery": {"work_or_study", "travel_or_road"},
    "outdoors": {"hiking_or_camping", "travel_or_road"},
    "gear": {"hiking_or_camping", "travel_or_road"},
    "daily": {"work_or_study", "travel_or_road"},
    "gift": {"work_or_study", "travel_or_road", "hiking_or_camping"},
}

PRODUCT_FORMS_BY_GOAL = {
    "running": {"bars", "gel", "food_or_meal", "liquid", "sticks"},
    "training": {"bars", "capsules", "liquid", "powder", "softgels", "sticks", "tablets"},
    "hydration": {"bars", "gel", "liquid", "sticks"},
    "food": {"bars", "food_or_meal", "gel", "liquid", "sticks"},
    "recovery": {"capsules", "powder", "softgels", "sticks", "tablets"},
    "outdoors": {"bars", "food_or_meal", "gel", "liquid", "sticks"},
    "gear": set(),
    "daily": {"capsules", "powder", "softgels", "tablets"},
    "gift": {"apparel", "bars", "capsules", "food_or_meal", "gel", "liquid", "softgels", "sticks", "tablets"},
}

SIZE_GOALS = {"running", "outdoors", "gear", "gift"}
CORE_ANSWER_FIELDS = ("activity",)
STEERING_ANSWER_FIELDS = ("component_class",)
SOFT_ANSWER_FIELDS = (
    "use_scenario", "use_timing", "use_place", "race_format", "season", "product_form",
)
ANSWER_SIGNAL_FIELDS = CORE_ANSWER_FIELDS + STEERING_ANSWER_FIELDS + SOFT_ANSWER_FIELDS


class DraftMatchError(ValueError):
    """Raised when a preview request is invalid or unsupported."""


def attach_audit_evidence(catalog, audit):
    """Attach the audit's evidence tiers and conditional facets by catalog row."""
    audit_records = audit.get("records", [])
    if len(audit_records) < 206:
        raise ValueError("Matching audit must contain at least 206 records")

    by_row = {record.get("catalog_row"): record for record in audit_records}
    if len(by_row) != len(audit_records):
        raise ValueError("Matching audit must contain unique catalog rows")
    if {record.get("catalog_row") for record in catalog} != set(by_row):
        raise ValueError("Catalog and matching audit rows do not match")

    enriched = []
    for record in catalog:
        audited = by_row[record["catalog_row"]]
        pool = audited.get("full_audit", {}).get("evidence_pool", {})
        proposal = audited.get("full_audit", {}).get("matching_proposal", {})
        tiers = proposal.get("candidate_tiers", {})
        activity = pool.get("activity_scope", {})
        component_classes = set(pool.get("component_classes_from_listed_names", []))
        blocked_classes = CONFLICTED_COMPONENT_CLASSES.get(record.get("sku"), set())
        if "*" in blocked_classes:
            component_classes.clear()
        else:
            component_classes.difference_update(blocked_classes)
        activity_groups = sorted(
            set(activity.get("seller_positioned_activity_groups", []))
            | set(activity.get("component_name_activity_groups", []))
        )
        enriched_record = dict(record)
        enriched_record["matching_evidence"] = {
            "status": proposal.get("status", "unknown"),
            "seller_families": list(tiers.get("seller_positioned", [])),
            "component_families": list(tiers.get("component_based", [])),
            "supplemental_families": list(tiers.get("supplemental_page_copy_needs_manual_review", [])),
            "tag_only_families": list(tiers.get("catalog_tags_only_or_auxiliary", [])),
            "activity_groups": activity_groups,
            "seller_activity_groups": list(activity.get("seller_positioned_activity_groups", [])),
            "component_activity_groups": list(activity.get("component_name_activity_groups", [])),
            "component_classes": sorted(component_classes),
            "use_contexts": list(pool.get("use_contexts", [])),
            "race_formats": list(pool.get("race_formats", [])),
            "product_forms": list(pool.get("product_forms_visible_in_listed_names", [])),
            "size_sensitive": bool(pool.get("size_sensitive_item_present")),
            "size_values": [
                item for item in pool.get("recorded_size_values", [])
                if item.get("type") == "shoe_or_sock_size"
            ],
            "weather_signals": list(pool.get("season_weather_signals", [])),
            "seller_summary": pool.get("seller_summary_text"),
            "conflict_notes": list(pool.get("conflict_notes", [])),
        }
        enriched.append(enriched_record)
    return enriched


def _matching_families(record, goal_group):
    evidence = record.get("matching_evidence", {})
    wanted = GOAL_FAMILIES[goal_group]
    seller = set(evidence.get("seller_families", [])) & wanted
    components = set(evidence.get("component_families", [])) & wanted

    blocked = CONFLICTED_COMPONENT_FAMILIES.get(record.get("sku"), set())
    if "*" in blocked:
        components.clear()
    else:
        components.difference_update(blocked)
    return sorted(seller), sorted(components)


def _goal_candidates(catalog, goal_group):
    candidates = []
    for record in catalog:
        seller, components = _matching_families(record, goal_group)
        if seller or components:
            candidates.append((record, seller, components))
    return candidates


def _size_ranges(record):
    ranges = []
    for item in record.get("matching_evidence", {}).get("size_values", []):
        if item.get("type") != "shoe_or_sock_size":
            continue
        value = str(item.get("value", "")).replace("–", "-")
        parts = value.split("-", 1)
        try:
            lower = int(parts[0])
            upper = int(parts[-1])
        except ValueError:
            continue
        ranges.append((lower, upper))
    return ranges


def _season_groups(record):
    signals = set(record.get("matching_evidence", {}).get("weather_signals", []))
    groups = set()
    if signals & {"cold_weather", "winter"}:
        groups.add("cold")
    if signals & {"hot_weather", "summer"}:
        groups.add("warm")
    return groups


def _soft_signals(record, key):
    evidence = record.get("matching_evidence", {})
    if key == "activity":
        return set(evidence.get("seller_activity_groups", [])) | set(evidence.get("component_activity_groups", []))
    if key == "component_class":
        return set(evidence.get("component_classes", []))
    if key in ("use_scenario", "use_timing", "use_place"):
        values = set(evidence.get("use_contexts", []))
        if key == "use_scenario":
            scenarios = set()
            if set(evidence.get("race_formats", [])) - {"unspecified"}:
                scenarios.add("event_preparation")
            if values & {"before_or_after_training", "during_training"}:
                scenarios.add("training")
            if values & {"daily_use", "evening_or_bedtime", "work_or_study"}:
                scenarios.add("everyday")
            return scenarios
        if key == "use_timing":
            return values & {
                "before_or_after_training", "during_training", "daily_use", "evening_or_bedtime",
            }
        if key == "use_place":
            return values & {"hiking_or_camping", "travel_or_road", "work_or_study"}
        return values
    if key == "race_format":
        return set(evidence.get("race_formats", [])) - {"unspecified"}
    if key == "season":
        return _season_groups(record)
    if key == "product_form":
        return set(evidence.get("product_forms", []))
    return set()


def _as_set(value):
    """Normalize a string, iterable, or empty answer into a set of non-empty values."""
    if value in (None, "", "any"):
        return set()
    if isinstance(value, (list, tuple, set)):
        return {item for item in value if item not in (None, "", "any")}
    return {value}


def _candidate_fit(candidate, answers):
    """Classify one goal candidate against answers without guessing unknown data."""
    record = candidate[0]
    maximum = answers.get("max_price_uah")
    price = record.get("price_uah")
    if maximum is not None and (isinstance(price, bool) or not isinstance(price, int) or price > maximum):
        return None

    membership_pref = answers.get("membership")
    if membership_pref == "yes":
        if _membership_status(record) != "included":
            return None
    elif membership_pref == "no":
        if _membership_status(record) in ("included", "mentioned"):
            return None

    matched = []
    unknown = []
    relaxed = []
    relaxed_values = {}
    for key in ANSWER_SIGNAL_FIELDS:
        vals = _as_set(answers.get(key))
        if not vals:
            continue
        if key == "activity" and "other" in vals:
            matched.append(key)
            continue
        signals = _soft_signals(record, key)
        if not signals:
            if key in STEERING_ANSWER_FIELDS:
                return None
            unknown.append(key)
        elif vals & signals:
            matched.append(key)
        elif key in CORE_ANSWER_FIELDS or key in STEERING_ANSWER_FIELDS:
            return None
        else:
            relaxed.append(key)
            relaxed_values[key] = sorted(vals) if len(vals) > 1 else next(iter(vals))

    size_match = False
    size_status = "not_requested"
    size = answers.get("shoe_size")
    if size is not None:
        ranges = _size_ranges(record)
        if ranges:
            size_match = any(lower <= size <= upper for lower, upper in ranges)
            if not size_match:
                return None
            size_status = "matched"
            matched.append("shoe_size")
        elif record.get("matching_evidence", {}).get("size_sensitive"):
            size_status = "unknown"
            unknown.append("shoe_size")

    match_type = "relaxed" if relaxed else "general" if unknown else "exact"
    return {
        "match_type": match_type,
        "matched_preferences": matched,
        "unknown_preferences": unknown,
        "relaxed_preferences": relaxed,
        "relaxed_preference_values": relaxed_values,
        "size_match": size_match,
        "size_status": size_status,
    }


def _candidate_pools(candidates, answers):
    """Split candidates into exact, unknown-but-compatible, and relaxed pools."""
    pools = {"exact": [], "general": [], "relaxed": []}
    for candidate in candidates:
        fit = _candidate_fit(candidate, answers)
        if fit:
            pools[fit["match_type"]].append((candidate, fit))
    return pools


def _followup_candidates(candidates, goal_group, answers):
    """Return the same non-conflicting pool used by the final recommendation."""
    pools = _candidate_pools(candidates, answers)
    return [candidate for tier in ("exact", "general") for candidate, _fit in pools[tier]]


def _values_in(candidates, key, allowed):
    return sorted({
        value
        for record, _seller, _components in candidates
        for value in (_soft_signals(record, key) & allowed)
    })


def _would_split(candidates, key, allowed, min_signals=2):
    """Return True if at least min_signals candidates have a known signal for allowed values."""
    with_signal = sum(1 for record, _, _ in candidates if _soft_signals(record, key) & allowed)
    return with_signal >= min_signals


def _question_plan(candidates, goal_group, answers):
    questions = []

    def add(key, values, title_key):
        if values:
            questions.append({"id": key, "title_key": title_key, "options": values, "type": "single"})

    remaining = candidates
    answered = answers

    # Early termination: if <= 3 candidates remain or user already answered 2 follow-up questions, skip directly to budget
    answered_followups = [k for k in answered if k not in ("max_price_uah", "locale")]
    if len(remaining) <= 3 or len(answered_followups) >= 2:
        if remaining and "max_price_uah" not in answered:
            prices = [record["price_uah"] for record, _seller, _components in remaining if isinstance(record.get("price_uah"), int)]
            questions.append({
                "id": "max_price_uah",
                "title_key": "question_budget",
                "type": "number",
                "min": 0,
                "dynamic_min": min(prices) if prices else None,
                "dynamic_max": max(prices) if prices else None,
            })
        return questions

    # 1. Primary filter: Component Class (What type of product do you need in the kit?)
    if "component_class" not in answered:
        values = _values_in(remaining, "component_class", COMPONENT_CLASSES_BY_GOAL.get(goal_group, set()))
        if len(values) > 1:
            add("component_class", values, "question_component_class")

    # 2. Activity (Sport): only for sport-specific goals where sport is a deciding factor; NEVER for recovery or daily
    if "activity" not in answered and goal_group not in ("recovery", "daily"):
        allowed = ACTIVITY_OPTIONS_BY_GOAL.get(goal_group, set())
        values = _values_in(remaining, "activity", allowed)
        if values and len(values) > 1:
            values = sorted(set(values) | {"other"})
            add("activity", values, "question_activity")

    # 3. Contextual Refinement (Choose at most ONE high-signal question based on component_class):
    comp_class = answered.get("component_class")

    # A. If Apparel / Footwear: ask shoe_size and season
    if comp_class == "apparel_footwear" or (goal_group == "gear" and comp_class != "sports_accessories"):
        if "shoe_size" not in answered:
            has_size = any(
                record.get("matching_evidence", {}).get("size_sensitive")
                and _size_ranges(record)
                for record, _seller, _components in remaining
            )
            if has_size:
                ranges = sorted({
                    "{}-{}".format(lower, upper)
                    for record, _seller, _components in remaining
                    for lower, upper in _size_ranges(record)
                })
                questions.append({"id": "shoe_size", "title_key": "question_shoe_size", "type": "number", "min": 1, "max": 70, "ranges": ranges})

        if "season" not in answered:
            values = _values_in(remaining, "season", {"cold", "warm"})
            if len(values) > 1 and _would_split(remaining, "season", {"cold", "warm"}):
                add("season", values, "question_season")

    # B. If Recovery: ask timing (evening/bedtime vs post-training); NEVER ask place for bedtime!
    elif goal_group == "recovery" or comp_class == "supplements_vitamins_minerals":
        if "use_timing" not in answered:
            allowed = USE_TIMINGS_BY_GOAL.get(goal_group, set())
            values = _values_in(remaining, "use_timing", allowed)
            if len(values) > 1 and _would_split(remaining, "use_timing", allowed):
                add("use_timing", values, "question_use_timing")

    # C. If Running nutrition/hydration: check race format only if event preparation
    elif goal_group == "running":
        if "use_scenario" not in answered:
            allowed = USE_SCENARIOS_BY_GOAL.get(goal_group, set())
            values = _values_in(remaining, "use_scenario", allowed)
            if len(values) > 1 and _would_split(remaining, "use_scenario", allowed):
                add("use_scenario", values, "question_use_scenario")
        elif answered.get("use_scenario") == "event_preparation" and "race_format" not in answered:
            allowed = {"half_marathon", "marathon", "race_or_event_preparation", "ultra_or_long_distance"}
            values = _values_in(remaining, "race_format", allowed)
            if len(values) > 1 and _would_split(remaining, "race_format", allowed):
                add("race_format", values, "question_race_format")

    # D. If Outdoors: ask camping vs travel or dehydrated meal form
    elif goal_group == "outdoors":
        if "use_place" not in answered:
            allowed = USE_PLACES_BY_GOAL.get(goal_group, set())
            values = _values_in(remaining, "use_place", allowed)
            if len(values) > 1 and _would_split(remaining, "use_place", allowed):
                add("use_place", values, "question_use_place")

    # Product form: ask only if forms vary and not apparel
    if "product_form" not in answered and comp_class != "apparel_footwear":
        allowed = PRODUCT_FORMS_BY_GOAL.get(goal_group, set())
        values = _values_in(remaining, "product_form", allowed)
        if len(values) > 1 and _would_split(remaining, "product_form", allowed, min_signals=3):
            add("product_form", values, "question_product_form")

    # Budget question is always appended at the end
    if remaining and "max_price_uah" not in answered:
        prices = [record["price_uah"] for record, _seller, _components in remaining if isinstance(record.get("price_uah"), int)]
        questions.append({
            "id": "max_price_uah",
            "title_key": "question_budget",
            "type": "number",
            "min": 0,
            "dynamic_min": min(prices) if prices else None,
            "dynamic_max": max(prices) if prices else None,
        })
    return questions


def draft_options(catalog, goal_group=None, answers=None):
    """Return follow-ups from the same non-conflicting pool as recommendations."""
    if goal_group is None:
        options = []
        for value in GOAL_FAMILIES:
            candidates = _goal_candidates(catalog, value)
            if candidates:
                options.append({"value": value, "label": GOAL_LABELS["ru"][value], "count": len(candidates)})
        return {"test_only": True, "goal_options": options, "catalog_count": len(catalog)}

    if answers is not None and not isinstance(answers, dict):
        raise DraftMatchError("Answers must be an object.")
    answers = answers or {}
    validated = _validate_request(catalog, {**answers, "goal_group": goal_group})
    goal_group = validated["goal_group"]
    candidates = _goal_candidates(catalog, goal_group)
    pools = _candidate_pools(candidates, validated)
    remaining = [candidate for tier in ("exact", "general") for candidate, _fit in pools[tier]]
    price_source = remaining if remaining else candidates
    prices = [record["price_uah"] for record, _seller, _components in price_source if isinstance(record.get("price_uah"), int)]
    return {
        "test_only": True,
        "goal_group": goal_group,
        "candidate_count": len(remaining),
        "exact_candidate_count": len(pools["exact"]),
        "general_candidate_count": len(pools["general"]),
        "relaxed_candidate_count": len(pools["relaxed"]),
        "question_plan": _question_plan(remaining, goal_group, answers),
        "price_range_uah": {"min": min(prices), "max": max(prices)} if prices else None,
        "price_snapshot_date": price_source[0][0].get("price_snapshot_date") if price_source else None,
    }


def _validate_request(catalog, request):
    if not isinstance(request, dict):
        raise DraftMatchError("Request must be a JSON object.")

    allowed = {
        "goal_group", "activity", "component_class", "use_scenario", "use_timing", "use_place",
        "race_format", "season", "product_form", "max_price_uah", "shoe_size", "locale", "fallback_mode",
        "membership", "verify_stock",
    }
    unsupported = set(request) - allowed
    if unsupported:
        raise DraftMatchError("Unsupported preview field: {}.".format(", ".join(sorted(unsupported))))

    goal_group = request.get("goal_group")
    if not isinstance(goal_group, str) or goal_group not in GOAL_FAMILIES:
        raise DraftMatchError("Choose a supported buyer need.")

    locale = request.get("locale", "ru")
    if locale not in ("ru", "uk"):
        raise DraftMatchError("locale must be 'ru' or 'uk'.")

    maximum = request.get("max_price_uah")
    if maximum in ("", "any"):
        maximum = None
    elif isinstance(maximum, str) and maximum.isdecimal():
        maximum = int(maximum)
    if maximum is not None and (
        isinstance(maximum, bool) or not isinstance(maximum, int) or maximum < 0
    ):
        raise DraftMatchError("max_price_uah must be a nonnegative integer.")

    size = request.get("shoe_size")
    if size in ("", "any"):
        size = None
    elif isinstance(size, str) and size.isdecimal():
        size = int(size)
    if size is not None and (
        isinstance(size, bool) or not isinstance(size, int) or size < 1 or size > 70
    ):
        raise DraftMatchError("shoe_size must be a numeric shoe size.")

    fallback_mode = request.get("fallback_mode")
    if fallback_mode not in (None, "general", "relaxed"):
        raise DraftMatchError("fallback_mode must be 'general' or 'relaxed'.")

    membership = request.get("membership")
    if membership in ("", "any"):
        membership = None
    if membership is not None and membership not in ("yes", "no"):
        raise DraftMatchError("membership must be 'yes', 'no', or 'any'.")

    choice_options = {
        "activity": ACTIVITY_OPTIONS_BY_GOAL[goal_group] | {"other"},
        "component_class": COMPONENT_CLASSES_BY_GOAL[goal_group],
        "use_scenario": USE_SCENARIOS_BY_GOAL[goal_group],
        "use_timing": USE_TIMINGS_BY_GOAL[goal_group],
        "use_place": USE_PLACES_BY_GOAL[goal_group],
        "race_format": {"half_marathon", "marathon", "race_or_event_preparation", "ultra_or_long_distance"},
        "season": {"cold", "warm"},
        "product_form": PRODUCT_FORMS_BY_GOAL[goal_group],
    }
    normalized_choices = {}
    for key, values in choice_options.items():
        value = request.get(key)
        if value in (None, "", "any"):
            continue
        if isinstance(value, str):
            if value not in values:
                raise DraftMatchError("{} is not supported for the selected need.".format(key))
            normalized_choices[key] = value
        elif isinstance(value, (list, tuple, set)):
            val_list = [item for item in value if item not in (None, "", "any")]
            if not val_list:
                continue
            for item in val_list:
                if not isinstance(item, str) or item not in values:
                    raise DraftMatchError("{} value '{}' is not supported for the selected need.".format(key, item))
            normalized_choices[key] = val_list if len(val_list) > 1 else val_list[0]
        else:
            raise DraftMatchError("{} must be a string or list of strings.".format(key))

    return {
        **request,
        **normalized_choices,
        "goal_group": goal_group,
        "max_price_uah": maximum,
        "shoe_size": size,
        "locale": locale,
        "fallback_mode": fallback_mode,
        "membership": membership,
    }


def _membership_status(record):
    item_types = record.get("tags", {}).get("item_type", []) or []
    composition = str(record.get("composition", "")).casefold()
    title = str(record.get("title", "")).casefold()
    if "club_membership_bundle" in item_types or "абонемент" in composition or "membership" in composition:
        return "included"
    if "абонемент" in title or "membership" in title:
        return "included"
    if "club" in title or "клуб" in title:
        return "mentioned"
    return "unknown"


def _calculate_match_score(record, seller_families, component_families, fit, validated):
    """Calculate an explainable 0-100% confidence score for a recommendation."""
    if not validated:
        return 75, {"evidence": 20, "preferences": 35, "constraints": 20}

    # 1. Слой доказательной базы (до 35%)
    evidence_score = 0
    if seller_families:
        evidence_score += 20
    if component_families:
        evidence_score += 15
    if record.get("matching_evidence", {}).get("status") == "conflict_review_required":
        evidence_score = max(5, evidence_score - 5)

    # 2. Слой предпочтений покупателя (до 45%)
    active_keys = [
        k for k in ANSWER_SIGNAL_FIELDS
        if validated.get(k) not in (None, "", "any")
    ]
    if not active_keys:
        pref_score = 45
    else:
        matched_set = set(fit.get("matched_preferences", []))
        unknown_set = set(fit.get("unknown_preferences", []))
        points = 0.0
        for k in active_keys:
            if k in matched_set:
                points += 1.0
            elif k in unknown_set:
                points += 0.55
        pref_score = int(round(45 * (points / len(active_keys))))

    # 3. Слой ограничений бюджета и размера (до 20%)
    fit_score = 0
    # Оценка размера (до 10%)
    if validated.get("shoe_size") is None:
        fit_score += 10
    elif fit.get("size_status") == "matched":
        fit_score += 10
    elif fit.get("size_status") == "unknown":
        fit_score += 5

    # Оценка бюджета (до 10%)
    maximum = validated.get("max_price_uah")
    price = record.get("price_uah", 0)
    if maximum is None:
        fit_score += 10
    elif isinstance(price, int) and price <= maximum:
        if price <= maximum * 0.85:
            fit_score += 10
        else:
            fit_score += 9
    elif isinstance(price, int) and price > maximum:
        over = price - maximum
        pct = over / max(1, maximum)
        fit_score += max(0, int(round(10 * max(0.0, 1.0 - 2.5 * pct))))

    total = min(99, max(15, evidence_score + pref_score + fit_score))
    match_type = fit.get("match_type")
    if match_type == "exact" and (maximum is None or price <= maximum):
        total = max(88, total)
    elif match_type == "general" and (maximum is None or price <= maximum):
        total = min(87, max(72, total))
    elif match_type == "near_miss":
        total = min(84, max(60, total))
    elif match_type == "floor_anchor":
        total = min(75, max(45, total))
    elif match_type == "relaxed":
        total = min(68, max(35, total))

    return total, {
        "evidence": evidence_score,
        "preferences": pref_score,
        "constraints": fit_score,
    }


def _find_budget_near_misses(goal_candidates, validated, max_delta_pct=0.25, max_delta_uah=350):
    """Find compatible candidates that only slightly exceed the user's budget."""
    maximum = validated.get("max_price_uah")
    if maximum is None:
        return []

    answers_no_price = {k: v for k, v in validated.items() if k != "max_price_uah"}
    near_misses = []
    max_allowed = max(int(maximum * (1 + max_delta_pct)), maximum + max_delta_uah)

    for candidate in goal_candidates:
        record = candidate[0]
        price = record.get("price_uah")
        if not isinstance(price, int) or price <= maximum or price > max_allowed:
            continue

        fit = _candidate_fit(candidate, answers_no_price)
        if fit and fit["match_type"] in ("exact", "general"):
            fit_copy = dict(fit)
            fit_copy["match_type"] = "near_miss"
            fit_copy["price_over_budget_uah"] = price - maximum
            near_misses.append((candidate, fit_copy))

    near_misses.sort(
        key=lambda entry: (
            entry[1]["price_over_budget_uah"],
            -int(bool(entry[0][1]) and bool(entry[0][2])),
            -len(entry[1]["matched_preferences"]),
            len(entry[1]["unknown_preferences"]),
            entry[0][0]["catalog_row"],
        )
    )
    return near_misses[:3]


def _find_floor_anchor(goal_candidates, validated):
    """Find the lowest-priced compatible baseline sets when user budget is below all matches."""
    maximum = validated.get("max_price_uah")
    if maximum is None:
        return []

    answers_no_price = {k: v for k, v in validated.items() if k != "max_price_uah"}
    pools = _candidate_pools(goal_candidates, answers_no_price)

    # Consider exact pool first, then general pool
    compatible = pools["exact"] if pools["exact"] else pools["general"]
    if not compatible:
        return []

    over_budget = [
        (candidate, fit)
        for candidate, fit in compatible
        if isinstance(candidate[0].get("price_uah"), int) and candidate[0]["price_uah"] > maximum
    ]
    if not over_budget:
        return []

    # Sort strictly by lowest price first, then best fit
    over_budget.sort(
        key=lambda entry: (
            entry[0][0]["price_uah"],
            -int(bool(entry[0][1]) and bool(entry[0][2])),
            -len(entry[1]["matched_preferences"]),
            len(entry[1]["unknown_preferences"]),
            entry[0][0]["catalog_row"],
        )
    )

    floor_anchors = []
    for candidate, fit in over_budget[:2]:
        fit_copy = dict(fit)
        fit_copy["match_type"] = "floor_anchor"
        fit_copy["price_over_budget_uah"] = candidate[0]["price_uah"] - maximum
        fit_copy["floor_price_uah"] = candidate[0]["price_uah"]
        floor_anchors.append((candidate, fit_copy))

    return floor_anchors


def _result(record, seller_families, component_families, fit, locale, validated=None, stock_info=None):
    evidence = record.get("matching_evidence", {})
    reasons = []
    matched_preferences = fit["matched_preferences"]
    goal_label = GOAL_LABELS[locale][record["selected_goal"]]
    if seller_families:
        reasons.append(
            "Продавец позиционирует набор для темы «{}».".format(goal_label)
            if locale == "ru" else
            "Продавець позиціонує набір для теми «{}».".format(goal_label)
        )
    if component_families:
        reasons.append(
            "В списке состава есть товар, связанный с этой задачей."
            if locale == "ru" else
            "У переліку складу є товар, пов'язаний із цією задачею."
        )
    preference_labels = {
        "activity": ("активности", "активності"),
        "component_class": ("типу товара в наборе", "типу товару в наборі"),
        "use_scenario": ("сценарию", "сценарію"),
        "use_timing": ("времени использования", "часу використання"),
        "use_place": ("месту использования", "місцю використання"),
        "race_format": ("формату старта", "формату старту"),
        "season": ("погоде", "погоді"),
        "product_form": ("форме товара", "формі товару"),
    }
    signal_sources = {}
    for key in matched_preferences:
        if key == "shoe_size":
            continue
        if key == "use_scenario":
            contexts = set(evidence.get("use_contexts", []))
            has_race = bool(set(evidence.get("race_formats", [])) - {"unspecified"})
            if "event_preparation" in _soft_signals(record, "use_scenario") and not (contexts & {"event_preparation"}):
                if has_race:
                    signal_sources["use_scenario"] = "inferred_from_race_format"
                    reasons.append(
                        "Сценарий «подготовка к старту» определён по формату старта набора."
                        if locale == "ru" else
                        "Сценарій «підготовка до старту» визначений за форматом старту набору."
                    )
                    continue
        ru_label, uk_label = preference_labels[key]
        reasons.append(
            "Есть совпадение по {}.".format(ru_label)
            if locale == "ru" else
            "Є збіг за {}.".format(uk_label)
        )
    if fit["size_match"]:
        reasons.append(
            "Указанный размер входит в диапазон товара."
            if locale == "ru" else
            "Вказаний розмір входить у діапазон товару."
        )
    if fit.get("match_type") == "near_miss":
        over = fit.get("price_over_budget_uah", 0)
        reasons.append(
            "Превышает выбранный бюджет на {} ₴.".format(over)
            if locale == "ru" else
            "Перевищує вибраний бюджет на {} ₴.".format(over)
        )
    elif fit.get("match_type") == "floor_anchor":
        floor_price = fit.get("floor_price_uah")
        over = fit.get("price_over_budget_uah", 0)
        reasons.append(
            "Минимальный базовый набор в категории (от {} ₴, разница с бюджетом {} ₴).".format(floor_price, over)
            if locale == "ru" else
            "Мінімальний базовий набір у категорії (від {} ₴, різниця з бюджетом {} ₴).".format(floor_price, over)
        )

    notes = []
    if fit["size_status"] == "unknown":
        notes.append(
            "Размер товара не указан в снимке; совпадение не подтверждено."
            if locale == "ru" else
            "Розмір товару не вказаний у знімку; збіг не підтверджено."
        )
    if evidence.get("status") == "conflict_review_required":
        notes.append(
            "В карточке есть неразрешённое расхождение состава; проверьте актуальную страницу."
            if locale == "ru" else
            "У картці є невирішена розбіжність складу; перевірте актуальну сторінку."
        )

    if stock_info and stock_info.get("is_live_check"):
        if stock_info.get("in_stock"):
            notes.append(
                "Наличие подтверждено по базе магазина: в наличии."
                if locale == "ru" else
                "Наявність підтверджена за базою магазину: в наявності."
            )
        else:
            status_text = stock_info.get(f"stock_status_text_{locale}") or ("Нет в наличии" if locale == "ru" else "Немає в наявності")
            notes.append(
                f"Статус на складе магазина: {status_text}."
                if locale == "ru" else
                f"Статус на складі магазину: {status_text}."
            )
        live_price = stock_info.get("live_price_uah")
        if live_price is not None and abs(live_price - record["price_uah"]) >= 1:
            notes.append(
                f"Актуальная цена на сайте: {live_price:.0f} ₴ (в каталоге было {record['price_uah']} ₴)."
                if locale == "ru" else
                f"Актуальна ціна на сайті: {live_price:.0f} ₴ (у каталозі було {record['price_uah']} ₴)."
            )
    else:
        notes.append(
            "Цена и наличие не обновляются в реальном времени."
            if locale == "ru" else
            "Ціна й наявність не оновлюються в реальному часі."
        )

    match_score_pct, score_breakdown = _calculate_match_score(
        record, seller_families, component_families, fit, validated
    )

    current_price_uah = (
        stock_info["live_price_uah"]
        if stock_info and stock_info.get("live_price_uah") is not None
        else record["price_uah"]
    )

    return {
        "set_id": record["set_id"],
        "catalog_row": record["catalog_row"],
        "sku": record.get("sku"),
        "title": record["title"],
        "source_url": record["source_url"],
        "price_uah": current_price_uah,
        "catalog_price_uah": record["price_uah"],
        "stock_info": stock_info or {
            "sku": record.get("sku"),
            "in_stock": True,
            "quantity": None,
            "status": 1,
            "live_price_uah": record["price_uah"],
            "stock_status_text_uk": "В наявності",
            "stock_status_text_ru": "В наличии",
            "is_live_check": False,
        },
        "price_snapshot_date": record["price_snapshot_date"],
        "match_type": fit["match_type"],
        "match_score_pct": match_score_pct,
        "score_breakdown": score_breakdown,
        "price_over_budget_uah": fit.get("price_over_budget_uah", 0),
        "unknown_preferences": fit["unknown_preferences"],
        "relaxed_preferences": fit["relaxed_preferences"],
        "relaxed_preference_values": fit["relaxed_preference_values"],
        "evidence_status": evidence.get("status", "unknown"),
        "membership_status": _membership_status(record),
        "matched_tiers": {
            "seller_positioned": seller_families,
            "component_based": component_families,
        },
        "size_status": fit["size_status"],
        "signal_sources": signal_sources,
        "reasons": reasons,
        "data_notes": notes,
    }


def _rank_candidate_entries(entries, stock_map=None):
    def sort_key(entry):
        rec = entry[0][0]
        sku = rec.get("sku") or ""
        in_stock = True
        if stock_map and sku in stock_map:
            in_stock = bool(stock_map[sku].get("in_stock", True))
        return (
            -int(in_stock),  # In-stock items prioritized first
            -int(bool(entry[0][1]) and bool(entry[0][2])),
            -int(bool(entry[0][1]) or bool(entry[0][2])),
            -len(entry[1]["matched_preferences"]),
            len(entry[1]["unknown_preferences"]),
            len(entry[1]["relaxed_preferences"]),
            entry[0][0]["price_uah"],
            entry[0][0]["catalog_row"],
        )
    return sorted(entries, key=sort_key)


def draft_recommend(catalog, request, stock_map=None):
    """Return exact matches first; show general automatically; relaxed on request."""
    validated = _validate_request(catalog, request)
    goal_group = validated["goal_group"]
    goal_candidates = _goal_candidates(catalog, goal_group)
    pools = _candidate_pools(goal_candidates, validated)
    fallback_mode = validated["fallback_mode"]
    if fallback_mode:
        selected_pool = pools[fallback_mode]
        status = fallback_mode if selected_pool else "no_match"
    elif pools["exact"]:
        selected_pool = pools["exact"]
        status = "matched"
    elif pools["general"]:
        selected_pool = pools["general"]
        status = "general_auto"
    else:
        selected_pool = []
        status = "no_match" if not pools["relaxed"] else "no_exact_match"

    verify_stock = request.get("verify_stock", False) or (stock_map is not None)
    if stock_map is None and verify_stock:
        candidate_skus = set()
        for pool_name in ("exact", "general", "relaxed"):
            for ((rec, _, _), _) in pools.get(pool_name, []):
                if rec.get("sku"):
                    candidate_skus.add(rec["sku"])
        if candidate_skus:
            try:
                stock_map = check_stock(list(candidate_skus))
            except Exception:
                stock_map = {}
        else:
            stock_map = {}

    ranked = _rank_candidate_entries(selected_pool, stock_map=stock_map)
    results = [
        _result(
            {**record, "selected_goal": goal_group},
            seller,
            components,
            fit,
            validated["locale"],
            validated,
            stock_info=stock_map.get(record.get("sku")) if stock_map else None,
        )
        for (record, seller, components), fit in ranked[:3]
    ]

    near_miss_results = []
    if len(results) < 3 and validated.get("max_price_uah") is not None:
        raw_near_misses = _find_budget_near_misses(goal_candidates, validated)
        existing_rows = {item["catalog_row"] for item in results}
        ranked_near_misses = _rank_candidate_entries(raw_near_misses, stock_map=stock_map)
        near_miss_results = [
            _result(
                {**record, "selected_goal": goal_group},
                seller,
                components,
                fit,
                validated["locale"],
                validated,
                stock_info=stock_map.get(record.get("sku")) if stock_map else None,
            )
            for (record, seller, components), fit in ranked_near_misses
            if record["catalog_row"] not in existing_rows
        ][:3]

    floor_anchor_results = []
    if not results and not near_miss_results and validated.get("max_price_uah") is not None:
        raw_floor_anchors = _find_floor_anchor(goal_candidates, validated)
        ranked_floor_anchors = _rank_candidate_entries(raw_floor_anchors, stock_map=stock_map)
        floor_anchor_results = [
            _result(
                {**record, "selected_goal": goal_group},
                seller,
                components,
                fit,
                validated["locale"],
                validated,
                stock_info=stock_map.get(record.get("sku")) if stock_map else None,
            )
            for (record, seller, components), fit in ranked_floor_anchors
        ][:2]
        if floor_anchor_results:
            status = "floor_anchor"

    fallback_options = []
    if status == "general_auto":
        if pools["relaxed"]:
            fallback_options = [{"mode": "relaxed", "count": len(pools["relaxed"])}]
    elif status == "no_exact_match":
        if pools["relaxed"]:
            fallback_options = [{"mode": "relaxed", "count": len(pools["relaxed"])}]
    elif fallback_mode:
        other_mode = "relaxed" if fallback_mode == "general" else "general"
        if pools[other_mode]:
            fallback_options = [{"mode": other_mode, "count": len(pools[other_mode])}]

    messages = {
        "ru": {
            "matched": "Найдены варианты, у которых все указанные ответы подтверждаются сигналами снимка каталога. Это не оценка эффективности или безопасности.",
            "general_auto": "Точного совпадения по всем ответам нет. Показаны варианты без известных противоречий; часть данных не подтверждена.",
            "no_exact_match": "Точного совпадения по подтверждённым данным нет. Ниже можно отдельно посмотреть варианты, которые не совпадают с мягкими предпочтениями.",
            "general": "Эти варианты не имеют известных противоречий ответам, но некоторые выбранные предпочтения не подтверждены данными каталога.",
            "relaxed": "Эти варианты показаны по вашему запросу с ослаблением мягких предпочтений. Известные расхождения перечислены в карточках.",
            "no_match": "По ответам и жёстким ограничениям подходящих вариантов нет.",
            "floor_anchor": "По выбранному бюджету наборов нет. В этой категории полноценные наборы начинаются от {floor} ₴ (включают сопровождение). Ниже предложен базовый вариант.",
        },
        "uk": {
            "matched": "Знайдено варіанти, для яких усі вказані відповіді підтверджуються сигналами знімка каталогу. Це не оцінка ефективності чи безпеки.",
            "general_auto": "Точного збігу за всіма відповідями немає. Показано варіанти без відомих суперечностей; частина даних не підтверджена.",
            "no_exact_match": "Точного збігу за підтвердженими даними немає. Нижче можна окремо переглянути варіанти, що не відповідають м’яким перевагам.",
            "general": "Ці варіанти не мають відомих суперечностей із відповідями, але деякі вибрані переваги не підтверджені даними каталогу.",
            "relaxed": "Ці варіанти показано на ваш запит із послабленням м’яких переваг. Відомі розбіжності перелічено в картках.",
            "no_match": "За відповідями та жорсткими обмеженнями відповідних варіантів немає.",
            "floor_anchor": "За вибраним бюджетом наборів немає. У цій категорії повноцінні набори починаються від {floor} ₴ (включають супровід). Нижче запропоновано базовий варіант.",
        },
    }
    message_key = status
    template = messages[validated["locale"]][message_key]
    if status == "floor_anchor" and floor_anchor_results:
        floor_min = min(item["price_uah"] for item in floor_anchor_results)
        message = template.format(floor=floor_min)
    else:
        message = template

    if not results and near_miss_results:
        extra_note = (
            " Ниже предложены варианты, подходящие по параметрам, с небольшим превышением бюджета."
            if validated["locale"] == "ru" else
            " Нижче запропоновано варіанти, які підходять за параметрами, з невеликим перевищенням бюджету."
        )
        message += extra_note

    return {
        "status": status,
        "test_only": True,
        "alternatives": len(results) > 1,
        "returned_count": len(results),
        "exact_count": len(pools["exact"]),
        "general_count": len(pools["general"]),
        "relaxed_count": len(pools["relaxed"]),
        "near_miss_count": len(near_miss_results),
        "floor_anchor_count": len(floor_anchor_results),
        "floor_price_uah": min((item["price_uah"] for item in floor_anchor_results), default=None),
        "fallback_options": fallback_options,
        "message": message,
        "price_snapshot_date": catalog[0].get("price_snapshot_date") if catalog else None,
        "stock_verified": bool(stock_map),
        "results": results,
        "near_miss_results": near_miss_results,
        "floor_anchor_results": floor_anchor_results,
    }
