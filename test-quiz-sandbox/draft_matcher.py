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
    "RE11020": {"protein_carbohydrate_food"},
    "RE88957": {"protein_carbohydrate_food"},
    "RE11632": {"creatine_preworkout"},  # Lion's mane baked cookie (0g creatine)
    "RE11663": {"creatine_preworkout"},  # Yoga mat + band (0g creatine)
    "RE11665": {"creatine_preworkout"},  # Jump rope + ab roller (0g creatine)
    "RE11660": {"creatine_preworkout"},  # Marathon kit (endurance gels + salts)
}

# Sets disqualified from Recovery & Sleep due to strength/creatine, gear dominance, or stimulant/focus actions
DISQUALIFIED_FROM_RECOVERY = {
    # Strength / Mass / Pre-workout / Creatine / Fitness Gear
    "RE11680", "RE11522", "RE11742", "RE88934", "RE11661", "RE11637", "RE11783",
    "RE11681", "RE11518", "RE11787", "RE88964", "RE11521", "RE11688", "RE11520",
    "Nabir_1115", "RE11660", "RE11516", "RE89452", "RE88963", "RE11800", "RE11665", "RE11663",
    # Pure gear / apparel / gifts
    "RE11013", "RE89460", "RE89459", "RE11024", "RE11020", "RE11801",
    # Nootropics / Focus / Energy / Stimulants (Methyl B12, Cordyceps, Mushrooms for brainwork, Energy formulas)
    "RE88957", "RE11691", "RE89019", "Nabir_1107", "RE11632", "Nabir_1134", "RE89021",
    "Nabir_1127", "Nabir_1102", "RE11513", "Nabir_1125",
}

# The activity branch is deliberately different by the selected buyer need.
ACTIVITY_OPTIONS_BY_GOAL = {
    "running": {"running"},
    "training": {"strength_training", "functional_training", "mind_body_mobility", "fitness_gym"},
    "hydration": {"running", "cycling", "strength_training", "functional_training", "fitness_gym", "hiking", "walking", "triathlon"},
    "food": {"running", "cycling", "hiking", "walking", "fitness_gym", "strength_training"},
    "recovery": {"running", "cycling", "strength_training", "functional_training", "fitness_gym", "mind_body_mobility"},
    "outdoors": {"hiking", "walking", "cycling", "running"},
    "gear": {"running", "hiking", "cycling", "walking"},
    "daily": set(),
    "gift": {"running", "cycling", "strength_training", "fitness_gym", "hiking", "swimming", "walking"},
}

COMPONENT_CLASSES_BY_GOAL = {
    "running": {"protein_carbohydrate_food", "hydration_items", "sports_accessories", "apparel_footwear"},
    "training": {"supplements_vitamins_minerals", "creatine_preworkout", "protein_carbohydrate_food", "hydration_items"},
    "hydration": {"hydration_items", "protein_carbohydrate_food", "sports_accessories"},
    "food": {"protein_carbohydrate_food", "hydration_items", "dehydrated_meal"},
    "recovery": {"supplements_vitamins_minerals", "protein_carbohydrate_food"},
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
    "training": {"before_or_after_training", "during_training", "daily_use", "evening_or_bedtime", "during_day_tone"},
    "hydration": {"before_or_after_training", "during_training", "daily_use"},
    "food": {"before_or_after_training", "during_training", "daily_use"},
    "recovery": {"before_or_after_training", "during_training", "daily_use", "evening_or_bedtime", "during_day_tone"},
    "outdoors": {"during_training", "daily_use", "evening_or_bedtime", "before_or_after_training"},
    "gear": {"during_training", "daily_use", "before_or_after_training"},
    "daily": {"daily_use", "evening_or_bedtime", "during_day_tone", "morning_start"},
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
    "running": {"bars", "gel", "food_or_meal", "liquid", "sticks", "capsules", "powder"},
    "training": {"bars", "capsules", "liquid", "powder", "softgels", "sticks", "tablets"},
    "hydration": {"sticks", "tablets", "powder", "capsules", "liquid", "gel"},
    "food": {"bars", "food_or_meal", "gel", "liquid", "sticks"},
    "recovery": {"capsules", "powder", "softgels", "sticks", "tablets", "bars"},
    "outdoors": {"bars", "food_or_meal", "gel", "liquid", "sticks"},
    "gear": set(),
    "daily": {"capsules", "powder", "softgels", "tablets", "bars"},
    "gift": {"bars", "capsules", "liquid", "powder", "softgels", "sticks", "tablets", "food_or_meal"},
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
    sku = record.get("sku")
    if goal_group == "recovery" and sku in DISQUALIFIED_FROM_RECOVERY:
        return [], []
    if goal_group == "gear":
        # Disqualify sets where creatine or heavy preworkout dominate
        classes = set(record.get("matching_evidence", {}).get("component_classes", []))
        if "creatine_preworkout" in classes:
            return [], []
    evidence = record.get("matching_evidence", {})
    wanted = GOAL_FAMILIES[goal_group]
    seller = set(evidence.get("seller_families", [])) & wanted
    components = set(evidence.get("component_families", [])) & wanted

    blocked = CONFLICTED_COMPONENT_FAMILIES.get(sku, set())
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
        acts = set(evidence.get("seller_activity_groups", [])) | set(evidence.get("component_activity_groups", []))
        if "fitness_gym" in acts:
            acts.add("strength_training")
            acts.add("functional_training")
        if "strength_training" in acts or "functional_training" in acts:
            acts.add("fitness_gym")
        return acts
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
                "before_or_after_training", "during_training", "daily_use", "evening_or_bedtime", "during_day_tone", "morning_start"
            }
        if key == "use_place":
            return values & {"hiking_or_camping", "travel_or_road", "work_or_study"}
        return values
    if key == "race_format":
        formats = set(evidence.get("race_formats", [])) - {"unspecified"}
        if "marathon" in formats or "race_or_event_preparation" in formats:
            formats.add("half_marathon")
        return formats
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
    """Return True if at least min_signals candidates have a known signal for allowed values,
    and there are at least 2 distinct signal profiles (so the question actually partitions the pool)."""
    with_signal = [c for c in candidates if _soft_signals(c[0], key) & allowed]
    if len(with_signal) < min_signals:
        return False
    distinct_profiles = {frozenset(_soft_signals(c[0], key) & allowed) for c in with_signal}
    return len(distinct_profiles) > 1


def _question_plan(candidates, goal_group, answers):
    questions = []

    def add(key, values, title_key):
        if values:
            questions.append({"id": key, "title_key": title_key, "options": values, "type": "single"})

    remaining = candidates
    answered = answers

    # Check if size-sensitive items are present among remaining candidates
    has_size_sensitive = any(
        record.get("matching_evidence", {}).get("size_sensitive")
        and _size_ranges(record)
        for record, _seller, _components in remaining
    )

    answered_followups = [k for k in answered if k not in ("max_price_uah", "locale")]
    comp_class = answered.get("component_class")

    # Critical physical constraints must not be dropped by early exit if sized apparel/gear is selected
    needs_size = has_size_sensitive and "shoe_size" not in answered and (
        comp_class == "apparel_footwear" or (goal_group == "gear" and comp_class != "sports_accessories")
    )

    # Early termination: if <= 3 candidates remain or user already answered 2 follow-up questions
    if (len(remaining) <= 3 or len(answered_followups) >= 2) and not needs_size:
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
        if len(values) > 1 and _would_split(remaining, "component_class", COMPONENT_CLASSES_BY_GOAL.get(goal_group, set())):
            add("component_class", values, "question_component_class")

    # 2. Sizing constraint: If Apparel / Footwear / Gear, ask shoe_size as immediate priority
    if comp_class == "apparel_footwear" or (goal_group == "gear" and comp_class != "sports_accessories"):
        if "shoe_size" not in answered:
            if has_size_sensitive:
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

    # 3. Activity (Sport): only for sport-specific goals where sport is a deciding factor; NEVER for recovery, daily, running, or apparel
    if "activity" not in answered and goal_group not in ("recovery", "daily", "running") and comp_class != "apparel_footwear":
        allowed = ACTIVITY_OPTIONS_BY_GOAL.get(goal_group, set())
        values = _values_in(remaining, "activity", allowed)
        if values and len(values) > 1 and _would_split(remaining, "activity", allowed):
            values = sorted(set(values) | {"other"})
            add("activity", values, "question_activity")

    # 4. Contextual Refinement:

    # B. If Recovery: ask timing (evening/bedtime vs post-training); NEVER ask place for bedtime!
    if goal_group == "recovery" or comp_class == "supplements_vitamins_minerals":
        if "use_timing" not in answered:
            allowed = USE_TIMINGS_BY_GOAL.get(goal_group, set())
            values = _values_in(remaining, "use_timing", allowed)
            if len(values) > 1 and _would_split(remaining, "use_timing", allowed):
                add("use_timing", values, "question_use_timing")

    # C. If Running: ask race format directly (distance/format)
    elif goal_group == "running":
        if "race_format" not in answered:
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

    # Product form: ask only for consumable/nutritional items, NEVER for accessories or apparel
    NUTRITIONAL_CLASSES = {"protein_carbohydrate_food", "supplements_vitamins_minerals", "hydration_items", "dehydrated_meal"}
    is_nutritional = comp_class in NUTRITIONAL_CLASSES or (not comp_class and goal_group in ("food", "hydration", "daily", "recovery"))
    if "product_form" not in answered and is_nutritional and comp_class not in ("sports_accessories", "apparel_footwear"):
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
    elif isinstance(size, str):
        if size.isdecimal():
            size = int(size)
        elif "-" in size or "–" in size:
            parts = size.replace("–", "-").split("-")
            try:
                size = (int(parts[0]) + int(parts[1])) // 2
            except (ValueError, IndexError):
                pass
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
    if not compatible and "shoe_size" in answers_no_price:
        answers_no_size = {k: v for k, v in answers_no_price.items() if k != "shoe_size"}
        pools_fallback = _candidate_pools(goal_candidates, answers_no_size)
        compatible = pools_fallback["exact"] if pools_fallback["exact"] else pools_fallback["general"]
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


def _build_expert_summary(record, fit, locale, validated=None):
    validated = validated or {}
    evidence = record.get("matching_evidence", {})
    goal = record.get("selected_goal") or validated.get("goal_group") or "running"
    classes = evidence.get("component_classes") or []

    category_summaries = {
        "protein_carbohydrate_food": {
            "uk": "Збалансований комплекс для підтримки високого темпу та витривалості: дає швидкі й тривалі вуглеводи без важкості в шлунку.",
            "ru": "Сбалансированный комплекс для поддержания высокого темпа и выносливости: даёт быстрые и пролонгированные углеводы без тяжести в желудке.",
        },
        "hydration_items": {
            "uk": "Спеціалізований комплекс для водно-сольового балансу: ефективно захищає від зневоднення, судом і втрати сил під час інтенсивного навантаження.",
            "ru": "Специализированный комплекс для водно-солевого баланса: эффективно защищает от обезвоживания, судорог и упадка сил при нагрузках.",
        },
        "supplements_vitamins_minerals": {
            "uk": "Оптимальна формула для відновлення та щоденного тонусу: знімає м'язову напругу, знижує втому та підтримує імунітет спортсмена.",
            "ru": "Оптимальная формула для восстановления и ежедневного тонуса: снимает мышечное напряжение, снижает усталость и поддерживает иммунитет спортсмена.",
        },
        "creatine_preworkout": {
            "uk": "Потужний комплекс для силових тренувань: підвищує вибухову силу, пікову працездатність та стимулює якісний м'язовий ріст.",
            "ru": "Мощный комплекс для силовых тренировок: повышает взрывную силу, пиковую работоспособность и стимулирует качественный мышечный рост.",
        },
        "apparel_footwear": {
            "uk": "Технологічне спортивне екіпірування: анатомічна посадка по стопі, надійна терморегуляція та активний захист від мозолів і натертостей.",
            "ru": "Технологичная спортивная экипировка: анатомическая посадка по стопе, надёжная терморегуляция и активная защита от мозолей и натёртостей.",
        },
        "dehydrated_meal": {
            "uk": "Поживний автономний раціон для походу: швидке приготування без зайвого посуду, висока калорійність та мінімальна вага в рюкзаку.",
            "ru": "Питательный автономный рацион для похода: быстрое приготовление без лишней посуды, высокая калорийность и минимальный вес в рюкзаке.",
        },
        "sports_accessories": {
            "uk": "Надійний функціональний аксесуар для спорту: максимальна зручність у русі, ергономічний дизайн та довговічні матеріали.",
            "ru": "Надёжный функциональный аксессуар для спорта: максимальное удобство в движении, эргономичный дизайн и долговечные материалы.",
        },
    }

    # Prioritize user's requested component class if present in set
    req_class = validated.get("component_class")

    # For recovery goal, always use recovery-oriented summaries
    if goal == "recovery":
        if req_class == "protein_carbohydrate_food" or "protein_carbohydrate_food" in classes:
            return (
                "Легкозасвоюваний білковий перекус: забезпечує м'язи амінокислотами для якісної регенерації під час відпочинку та сну."
                if locale == "uk" else
                "Легкоусвояемый белковый перекус: обеспечивает мышцы аминокислотами для качественной регенерации во время отдыха и сна."
            )
        return (
            "Комплекс для глибокого відновлення: сприяє регенерації м'язів, нормалізації сну та зняттю накопиченого стресу."
            if locale == "uk" else
            "Комплекс для глубокого восстановления: способствует регенерации мышц, нормализации сна и снятию накопившегося стресса."
        )

    target_class = req_class if (req_class and req_class in classes) else (classes[0] if classes else None)
    if target_class and target_class in category_summaries:
        return category_summaries[target_class][locale]

    goal_summaries = {
        "running": {
            "uk": "Профільний комплект для бігунів: сфокусований на витривалості, рівномірному розподілі сил і комфорті на дистанції.",
            "ru": "Профильный комплект для бегунов: сфокусирован на выносливости, равномерном распределении сил и комфорте на дистанции.",
        },
        "training": {
            "uk": "Комплект для результативних тренувань: допомагає тренуватися довше, відновлюватися швидше та прогресувати в силі.",
            "ru": "Комплект для результативных тренировок: помогает тренироваться дольше, восстанавливаться быстрее и прогрессировать в силе.",
        },
        "recovery": {
            "uk": "Комплекс для глибокого відновлення: сприяє регенерації м'язів, нормалізації сну та зняттю накопиченого стресу.",
            "ru": "Комплекс для глубокого восстановления: способствует регенерации мышц, нормализации сна и снятию накопившегося стресса.",
        },
        "hydration": {
            "uk": "Освіжаючий баланс електролітів: попереджає судоми та допомагає підтримувати високу працездатність у спеку чи на тренуваннях.",
            "ru": "Освежающий баланс электролитов: предупреждает судороги и помогает поддерживать высокую работоспособность в жару или на тренировках.",
        },
        "gift": {
            "uk": "Презентабельний подарунковий набір для спортсмена: готове фірмове рішення з корисним складом та клубними бонусами.",
            "ru": "Презентабельный подарочный набор для спортсмена: готовое фирменное решение с полезным составом и клубными бонусами.",
        },
        "outdoors": {
            "uk": "Автономний комплект для походу чи активного відпочинку: зручне використання, якісне живлення та надійне спорядження.",
            "ru": "Автономный комплект для похода или активного отдыха: удобное использование, качественное питание и надёжная экипировка.",
        },
        "gear": {
            "uk": "Продумане спортивне екіпірування: захищає від дискомфорту та допомагає зосередитися на спортивному результаті.",
            "ru": "Продуманная спортивная экипировка: защищает от дискомфорта и помогает сосредоточиться на спортивном результате.",
        },
        "daily": {
            "uk": "Щоденний комплекс підтримки організму: допомагає зберігати тонус, енергію та високу концентрацію протягом усього дня.",
            "ru": "Ежедневный комплекс поддержки организма: помогает сохранять тонус, энергию и высокую концентрацию на протяжении всего дня.",
        },
    }
    if goal in goal_summaries:
        return goal_summaries[goal][locale]

    return (
        "Збалансований фірмовий набір Race Expert, скомплектований під вашу активність та цілі тренувань."
        if locale == "uk" else
        "Сбалансированный фирменный набор Race Expert, скомплектованный под вашу активность и цели тренировок."
    )


def _build_why_suitable(record, fit, locale, validated, seller_families, component_families):
    validated = validated or {}
    items = []
    goal = record.get("selected_goal") or validated.get("goal_group")
    goal_label = GOAL_LABELS[locale].get(goal, goal)

    if seller_families or component_families:
        if locale == "uk":
            items.append(f"Цільове призначення: спеціально скомплектовано для задачі «{goal_label}».")
        else:
            items.append(f"Целевое назначение: специально скомплектован под задачу «{goal_label}».")

    req_class = validated.get("component_class")
    class_names = {
        "protein_carbohydrate_food": ("Спортивне харчування та батончики", "Спортивное питание и батончики"),
        "supplements_vitamins_minerals": ("Вітаміни та щоденні мінерали", "Витамины и минералы"),
        "creatine_preworkout": ("Креатин та передтренувальні комплекси", "Креатин и предтреники"),
        "sports_accessories": ("Спортивні аксесуари та пляшки", "Спортивные аксессуары и фляги"),
        "apparel_footwear": ("Одяг, шкарпетки та екіпірування", "Одежда, носки и экипировка"),
        "hydration_items": ("Ізотоніки та електроліти", "Изотоники и электролиты"),
        "dehydrated_meal": ("Сублімована туристична їжа", "Сублимированная туристическая еда"),
    }
    if req_class:
        classes_list = req_class if isinstance(req_class, (list, tuple, set)) else [req_class]
        matched_cnames = [class_names[c][0 if locale == "uk" else 1] for c in classes_list if c in class_names]
        if matched_cnames:
            cname = ", ".join(matched_cnames)
            if locale == "uk":
                items.append(f"Категорія товарів: у наборі представлено {cname}.")
            else:
                items.append(f"Категория товаров: в наборе представлено {cname}.")

    req_form = validated.get("product_form")
    form_names = {
        "bars": ("батончики", "батончики"),
        "gel": ("енергетичні гелі", "энергетические гели"),
        "liquid": ("рідкі шоти", "жидкие шоты"),
        "sticks": ("стіки з порошком", "стики с порошком"),
        "capsules": ("капсули", "капсулы"),
        "tablets": ("таблетки", "таблетки"),
        "softgels": ("м'які капсули (Omega/D3)", "мягкие капсулы (Omega/D3)"),
        "powder": ("порошок у банках", "порошок в банках"),
        "apparel": ("текстильне екіпірування", "текстильная экипировка"),
        "food_or_meal": ("готова їжа та снеки", "готовая еда и снеки"),
    }
    if req_form:
        forms_list = req_form if isinstance(req_form, (list, tuple, set)) else [req_form]
        matched_fnames = [form_names[f][0 if locale == "uk" else 1] for f in forms_list if f in form_names]
        if matched_fnames:
            fname = ", ".join(matched_fnames)
            if locale == "uk":
                items.append(f"Форма продукту: зручний формат — {fname}, легко брати із собою.")
            else:
                items.append(f"Форма продукта: удобный формат — {fname}, легко брать с собой.")

    req_timing = validated.get("use_timing")
    timing_names = {
        "during_training": ("під час тренувань на ходу", "во время тренировок на ходу"),
        "before_or_after_training": ("до або після тренування для підзарядки", "до или после тренировки для подзарядки"),
        "evening_or_bedtime": ("увечері перед сном для відпочинку", "вечером перед сном для отдыха"),
        "daily_use": ("протягом дня для стабільного тонусу", "в течение дня для стабильного тонуса"),
    }
    if req_timing:
        timings_list = req_timing if isinstance(req_timing, (list, tuple, set)) else [req_timing]
        matched_tnames = [timing_names[t][0 if locale == "uk" else 1] for t in timings_list if t in timing_names]
        if matched_tnames:
            tname = ", ".join(matched_tnames)
            if locale == "uk":
                items.append(f"Час прийому: розраховано на вживання {tname}.")
            else:
                items.append(f"Время приёма: рассчитан на употребление {tname}.")

    if fit.get("size_match") and validated.get("shoe_size"):
        size = validated.get("shoe_size")
        if locale == "uk":
            items.append(f"Розмірний збіг: вказаний розмір {size} входить у діапазон товару.")
        else:
            items.append(f"Размерное совпадение: указанный размер {size} входит в диапазон товара.")

    max_price = validated.get("max_price_uah")
    price = record.get("price_uah", 0)
    if isinstance(max_price, int) and isinstance(price, int) and price <= max_price:
        diff = max_price - price
        if diff >= 50:
            if locale == "uk":
                items.append(f"Бюджет: {price} ₴ — укладається в ліміт {max_price} ₴ (запас {diff} ₴).")
            else:
                items.append(f"Бюджет: {price} ₴ — укладывается в лимит {max_price} ₴ (запас {diff} ₴).")
        else:
            if locale == "uk":
                items.append(f"Бюджет: {price} ₴ — точно відповідає вашому бюджетному очікуванню.")
            else:
                items.append(f"Бюджет: {price} ₴ — точно соответствует вашему бюджетному ожиданию.")

    if _membership_status(record) == "includes_membership":
        if locale == "uk":
            items.append("Клубні привілеї: включає абонемент Race Expert Club з доступом до спільноти та тренувань.")
        else:
            items.append("Клубные привилегии: включает абонемент Race Expert Club с доступом к сообществу и тренировкам.")

    if len(items) < 2:
        if locale == "uk":
            items.append("Склад: сертифікована спортивна продукція з перевіреною сумісністю.")
        else:
            items.append("Состав: сертифицированная спортивная продукция с проверенной совместимостью.")

    return items


def _build_why_not_suitable(record, fit, locale, validated):
    validated = validated or {}
    tradeoffs = []
    match_type = fit.get("match_type")

    if match_type == "near_miss":
        over = fit.get("price_over_budget_uah", 0)
        if locale == "uk":
            tradeoffs.append(f"Перевищує вибраний бюджет на {over} ₴ (проте містить більший обсяг продукції).")
        else:
            tradeoffs.append(f"Превышает выбранный бюджет на {over} ₴ (однако содержит больший объём продукции).")
    elif match_type == "floor_anchor":
        floor_price = fit.get("floor_price_uah", record.get("price_uah"))
        over = fit.get("price_over_budget_uah", 0)
        if locale == "uk":
            tradeoffs.append(f"Мінімальний базовий набір у категорії (від {floor_price} ₴, різниця з бюджетом {over} ₴).")
        else:
            tradeoffs.append(f"Минимальный базовый набор в категории (от {floor_price} ₴, разница с бюджетом {over} ₴).")

    if fit.get("size_status") == "unknown" and validated.get("shoe_size"):
        if locale == "uk":
            tradeoffs.append("Розмір не вказаний окремо в описі (може бути універсальний або еластичний крій).")
        else:
            tradeoffs.append("Размер товара не указан в описании (может быть универсальный или эластичный крой).")

    evidence = record.get("matching_evidence", {})
    if evidence.get("status") == "conflict_review_required":
        if locale == "uk":
            tradeoffs.append("У картці є невирішена розбіжність складу; перевірте актуальну сторінку магазину.")
        else:
            tradeoffs.append("В карточке есть неразрешённое расхождение состава; проверьте актуальную страницу магазина.")

    return tradeoffs


def _result(record, seller_families, component_families, fit, locale, validated=None, stock_info=None):
    evidence = record.get("matching_evidence", {})
    signal_sources = {}

    expert_summary = _build_expert_summary(record, fit, locale, validated)
    why_suitable = _build_why_suitable(record, fit, locale, validated, seller_families, component_families)
    why_not_suitable = _build_why_not_suitable(record, fit, locale, validated)

    reasons = list(why_suitable)
    if fit.get("match_type") == "near_miss":
        over = fit.get("price_over_budget_uah", 0)
        reasons.append(
            f"Превышает выбранный бюджет на {over} ₴."
            if locale == "ru" else
            f"Перевищує вибраний бюджет на {over} ₴."
        )
    elif fit.get("match_type") == "floor_anchor":
        floor_price = fit.get("floor_price_uah")
        over = fit.get("price_over_budget_uah", 0)
        reasons.append(
            f"Минимальный базовый набор в категории (от {floor_price} ₴, разница с бюджетом {over} ₴)."
            if locale == "ru" else
            f"Мінімальний базовий набір у категорії (від {floor_price} ₴, різниця з бюджетом {over} ₴)."
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
        "expert_summary": expert_summary,
        "why_suitable": why_suitable,
        "why_not_suitable": why_not_suitable,
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
