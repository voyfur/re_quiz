"""Deterministic test-only matching against the normalized local catalog."""

class MatchError(ValueError):
    """Raised when a quiz request is invalid or asks for unsupported data."""


ALLOWED_FILTERS = {
    "goal_group",
    "purpose",
    "sport",
    "max_price_uah",
    "shoe_size",
    "caffeine_mode",
    "in_stock_only",
    "item_type",
    "contains",
    "form",
    "race_format",
    "search_text",
    "result_count",
    "locale",
}
QUIZ_GOAL_GROUPS = (
    "running",
    "training",
    "recovery",
    "food",
    "outdoors",
    "gear",
    "daily",
    "gift",
)
_GOAL_GROUP_KEYWORDS = (
    ("gift", ("gift", "patriotic")),
    ("running", ("run", "race", "marathon", "half_marathon")),
    ("outdoors", ("hiking", "travel", "field_")),
    ("food", ("snack", "meal", "food", "nutrition", "protein")),
    ("gear", ("gear", "comfort", "apparel", "towel", "foot", "cold_weather", "accessories")),
    ("training", ("training", "strength", "gym", "fitness", "muscle", "workout", "performance", "sport", "pilates", "yoga")),
    ("recovery", ("recovery", "sleep", "relax", "rest", "stress", "calm", "balance", "nervous", "mobility")),
)
_UNVERIFIED_AUDIENCES = {
    "children",
    "children_3_plus",
    "pregnant_women",
    "women_planning_pregnancy",
    "men",
    "men_50_plus",
    "women",
}
UNSUPPORTED_FIELDS = {
    "age",
    "allergy",
    "allergens",
    "buyer_weight",
    "weight",
    "distance_km",
    "duration",
    "period",
    "pregnancy",
    "medications",
    "interactions",
}


def goal_group_for_purpose(purpose):
    """Map a source purpose tag to a broad, test-only consumer-facing theme."""
    value = purpose.casefold()
    if value.startswith("digestive_"):
        return "daily"
    for group, keywords in _GOAL_GROUP_KEYWORDS:
        if any(keyword in value for keyword in keywords):
            return group
    return "daily"


def _has_unverified_audience(record):
    return bool(_UNVERIFIED_AUDIENCES.intersection(_tags(record).get("audience", [])))


def goal_group_options(catalog):
    counts = {group: 0 for group in QUIZ_GOAL_GROUPS}
    for record in catalog:
        if _has_unverified_audience(record):
            continue
        groups = {goal_group_for_purpose(purpose) for purpose in _tags(record).get("purpose", [])}
        for group in groups:
            counts[group] += 1
    return [{"value": group, "count": counts[group]} for group in QUIZ_GOAL_GROUPS if counts[group]]


def _tags(record):
    return record.get("tags", {})


def _tag_options(catalog, namespace):
    return {
        value
        for record in catalog
        for value in _tags(record).get(namespace, [])
    }


def _validate_request(catalog, request):
    if not isinstance(request, dict):
        raise MatchError("Request must be a JSON object.")

    unsupported = (set(request) & UNSUPPORTED_FIELDS) | (set(request) - ALLOWED_FILTERS)
    if unsupported:
        names = ", ".join(sorted(unsupported))
        raise MatchError("Unsupported or unverified filter: {}.".format(names))

    result_count = request.get("result_count", 3)
    if isinstance(result_count, bool) or not isinstance(result_count, int) or result_count not in (1, 2, 3):
        raise MatchError("result_count must be 1, 2, or 3.")

    maximum = request.get("max_price_uah")
    if maximum is not None and (
        isinstance(maximum, bool) or not isinstance(maximum, int) or maximum < 0
    ):
        raise MatchError("max_price_uah must be a nonnegative integer.")

    size = request.get("shoe_size")
    if size is not None and (
        isinstance(size, bool) or not isinstance(size, int) or size < 1 or size > 70
    ):
        raise MatchError("shoe_size must be a numeric shoe size.")

    caffeine_mode = request.get("caffeine_mode", "any")
    if caffeine_mode not in ("any", "avoid"):
        raise MatchError("caffeine_mode must be 'any' or 'avoid'.")

    in_stock_only = request.get("in_stock_only", False)
    if not isinstance(in_stock_only, bool):
        raise MatchError("in_stock_only must be a boolean.")

    locale = request.get("locale", "ru")
    if locale not in ("ru", "uk"):
        raise MatchError("locale must be 'ru' or 'uk'.")

    selected = {}
    if "goal_group" in request and "purpose" in request:
        raise MatchError("Choose a broad quiz goal or a specific purpose tag, not both.")
    goal_group = request.get("goal_group")
    if goal_group is not None:
        if not isinstance(goal_group, str) or goal_group not in QUIZ_GOAL_GROUPS:
            raise MatchError("goal_group must be a supported quiz goal.")
        selected["goal_group"] = goal_group
    for field, namespace in (
        ("purpose", "purpose"),
        ("sport", "sport"),
        ("item_type", "item_type"),
        ("form", "form"),
        ("race_format", "race_format"),
    ):
        value = request.get(field)
        if value is not None:
            if not isinstance(value, str) or value not in _tag_options(catalog, namespace):
                raise MatchError("{} must be a value present in the local catalog.".format(field))
            selected[field] = value

    contains = request.get("contains", [])
    if isinstance(contains, str):
        contains = [contains]
    if not isinstance(contains, list) or any(not isinstance(value, str) for value in contains):
        raise MatchError("contains must be a list of catalog component tags.")
    unknown_components = set(contains) - _tag_options(catalog, "contains")
    if unknown_components:
        raise MatchError("Unknown component tag: {}.".format(", ".join(sorted(unknown_components))))

    search_text = request.get("search_text", "")
    if not isinstance(search_text, str) or len(search_text) > 80:
        raise MatchError("search_text must be a string of at most 80 characters.")
    search_text = search_text.strip()

    has_filter = bool(
        selected
        or contains
        or search_text
        or maximum is not None
        or size is not None
        or caffeine_mode == "avoid"
        or in_stock_only
    )
    if not has_filter:
        raise MatchError("Choose at least one catalog-backed filter.")

    return {
        "selected": selected,
        "contains": contains,
        "search_text": search_text.casefold(),
        "max_price_uah": maximum,
        "shoe_size": size,
        "caffeine_mode": caffeine_mode,
        "in_stock_only": in_stock_only,
        "result_count": result_count,
        "locale": locale,
    }


def _caffeine_status(record):
    tags = _tags(record)
    explicit = tags.get("caffeine_status", [])
    if "confirmed_absent" in explicit:
        return "confirmed_absent"
    if "present" in explicit or "caffeine" in tags.get("contains", []):
        return "present"
    return "unknown"


def _availability(record):
    if "in_stock" in _tags(record).get("availability", []):
        return "in_stock"
    if "out_of_stock" in _tags(record).get("availability", []):
        return "out_of_stock"
    return "unknown"


def _size_ranges(record):
    ranges = []
    for value in _tags(record).get("shoe_size", []):
        parts = value.replace("–", "-").split("-", 1)
        try:
            lower = int(parts[0])
            upper = int(parts[-1])
        except ValueError:
            continue
        ranges.append((lower, upper))
    return ranges


def _record_search_text(record):
    values = [record.get("title", ""), record.get("composition", ""), record.get("description", "")]
    for namespace, tags in _tags(record).items():
        values.append(namespace)
        values.extend(tags)
    return " ".join(values).casefold()


def _candidate_reasons(record, selected, contains, locale, sport_match, size_match):
    reasons = []
    tags = _tags(record)
    if "goal_group" in selected:
        group_label = {
            "ru": {
                "running": "бег и старты", "training": "тренировки", "recovery": "восстановление и отдых",
                "food": "перекусы и питание", "outdoors": "походы и поездки", "gear": "одежда и экипировка",
                "daily": "повседневная активность", "gift": "подарок",
            },
            "uk": {
                "running": "біг і старти", "training": "тренування", "recovery": "відновлення та відпочинок",
                "food": "перекуси та харчування", "outdoors": "походи й подорожі", "gear": "одяг та спорядження",
                "daily": "щоденна активність", "gift": "подарунок",
            },
        }[locale][selected["goal_group"]]
        reasons.append("Набор отнесён к теме «{}» по описанию каталога.".format(group_label) if locale == "ru" else "Набір віднесено до теми «{}» за описом каталогу.".format(group_label))
    elif "purpose" in selected:
        reasons.append("Тег назначения совпадает с выбранным." if locale == "ru" else "Тег призначення збігається з вибраним.")
    if "sport" in selected:
        if sport_match == 2:
            reasons.append("Тег вида спорта совпадает с выбранным." if locale == "ru" else "Тег виду спорту збігається з вибраним.")
        else:
            reasons.append("В каталоге указан общий тег спорта; точный вид не подтверждён." if locale == "ru" else "У каталозі вказано загальний тег спорту; точний вид не підтверджено.")
    field_labels = {
        "ru": {"item_type": "типа набора", "form": "формы товара", "race_format": "формата старта"},
        "uk": {"item_type": "типу набору", "form": "форми товару", "race_format": "формату старту"},
    }
    for field in ("item_type", "form", "race_format"):
        if field in selected:
            label = field_labels[locale][field]
            reasons.append("Совпадает тег {}.".format(label) if locale == "ru" else "Збігається тег {}.".format(label))
    for component in contains:
        reasons.append("В составе есть выбранный компонент." if locale == "ru" else "У складі є вибраний компонент.")
    if size_match:
        ranges = ", ".join(tags.get("shoe_size", []))
        reasons.append("Размер попадает в записанный диапазон {}.".format(ranges) if locale == "ru" else "Розмір входить у зазначений діапазон {}.".format(ranges))
    if not reasons:
        reasons.append("Совпадает с выбранными тегами каталога." if locale == "ru" else "Збігається з вибраними тегами каталогу.")
    return reasons


def _data_notes(record, locale):
    notes = []
    caffeine_status = _caffeine_status(record)
    if caffeine_status == "present":
        dose = _tags(record).get("caffeine_per_set", [])
        if dose:
            notes.append("В составе указан кофеин: {} на набор.".format(dose[0]) if locale == "ru" else "У складі зазначено кофеїн: {} на набір.".format(dose[0]))
        else:
            notes.append("Кофеин отмечен; количество на набор не подтверждено." if locale == "ru" else "Кофеїн позначений; кількість на набір не підтверджена.")
    elif caffeine_status == "unknown":
        notes.append("Кофеин не проверен; отсутствие тега не подтверждает его отсутствие." if locale == "ru" else "Кофеїн не перевірений; відсутність тегу не підтверджує його відсутність.")

    availability = _availability(record)
    if availability == "unknown":
        notes.append("Наличие не подтверждено в этом снимке." if locale == "ru" else "Наявність не підтверджена в цьому знімку.")

    if _tags(record).get("data_quality"):
        notes.append("В карточке отмечены ограничения качества данных." if locale == "ru" else "У картці позначено обмеження якості даних.")
    return notes


def _result(record, request, sport_match, size_match):
    locale = request["locale"]
    tags = _tags(record)
    if request["shoe_size"] is None:
        shoe_size_status = "not_requested"
    elif size_match:
        shoe_size_status = "matched"
    else:
        shoe_size_status = "unknown"
    matched_tags = {}
    for field in ("purpose", "sport", "item_type", "form", "race_format"):
        if field in request["selected"]:
            selected_value = request["selected"][field]
            if field != "sport" or sport_match == 2:
                matched_tags[field] = [selected_value]
    if "goal_group" in request["selected"]:
        matched_tags["purpose"] = [
            purpose for purpose in tags.get("purpose", [])
            if goal_group_for_purpose(purpose) == request["selected"]["goal_group"]
        ]
    if request["contains"]:
        matched_tags["contains"] = request["contains"]
    if size_match:
        matched_tags["shoe_size"] = tags.get("shoe_size", [])
    return {
        "set_id": record["set_id"],
        "catalog_row": record["catalog_row"],
        "sku": record.get("sku"),
        "title": record["title"],
        "source_url": record["source_url"],
        "price_uah": record["price_uah"],
        "price_snapshot_date": record["price_snapshot_date"],
        "composition": record.get("composition", ""),
        "matched_tags": matched_tags,
        "caffeine_status": _caffeine_status(record),
        "caffeine_per_set": tags.get("caffeine_per_set", []),
        "availability": _availability(record),
        "shoe_size_status": shoe_size_status,
        "reasons": _candidate_reasons(record, request["selected"], request["contains"], locale, sport_match, size_match),
        "data_notes": _data_notes(record, locale),
        "is_alternative": True,
    }


def recommend(catalog, request):
    """Return up to three deterministic alternative set matches for a test request."""
    validated = _validate_request(catalog, request)
    selected = validated["selected"]
    candidates = []
    before_caffeine = []

    for record in catalog:
        tags = _tags(record)
        # Sport is handled below so a general-purpose set can remain eligible
        # after exact sport matches, while a differently tagged sport is excluded.
        exact_filters = {key: value for key, value in selected.items() if key not in ("sport", "goal_group")}
        if any(value not in tags.get(field, []) for field, value in exact_filters.items()):
            continue
        if "goal_group" in selected:
            if not any(goal_group_for_purpose(purpose) == selected["goal_group"] for purpose in tags.get("purpose", [])):
                continue
            if _has_unverified_audience(record):
                continue
        if any(value not in tags.get("contains", []) for value in validated["contains"]):
            continue
        if validated["max_price_uah"] is not None and record["price_uah"] > validated["max_price_uah"]:
            continue
        if validated["in_stock_only"] and _availability(record) != "in_stock":
            continue
        if validated["search_text"] and validated["search_text"] not in _record_search_text(record):
            continue

        ranges = _size_ranges(record)
        size_match = False
        if validated["shoe_size"] is not None and ranges:
            size_match = any(lower <= validated["shoe_size"] <= upper for lower, upper in ranges)
            if not size_match:
                continue

        sport_match = 0
        if "sport" in selected:
            sports = tags.get("sport", [])
            if selected["sport"] in sports:
                sport_match = 2
            elif "not_sport_specific" in sports:
                sport_match = 1
            else:
                continue

        candidate = (record, sport_match, 1 if size_match else 0)
        before_caffeine.append(candidate)
        if validated["caffeine_mode"] == "avoid" and _caffeine_status(record) != "confirmed_absent":
            continue
        candidates.append(candidate)

    candidates.sort(
        key=lambda item: (
            -item[1],
            -item[2],
            item[0]["price_uah"],
            item[0]["catalog_row"],
        )
    )
    selected_results = [
        _result(record, validated, sport_match, size_match)
        for record, sport_match, size_match in candidates[:validated["result_count"]]
    ]

    if selected_results:
        status = "matched"
        message = "Найдено тестовых вариантов: {}. Тематическое соответствие основано на описаниях каталога и не подтверждает безопасность или пригодность.".format(len(selected_results)) if validated["locale"] == "ru" else "Знайдено тестових варіантів: {}. Тематична відповідність ґрунтується на описах каталогу й не підтверджує безпеку або придатність.".format(len(selected_results))
    elif validated["caffeine_mode"] == "avoid" and before_caffeine:
        status = "insufficient_data"
        message = "В каталоге нет наборов с подтверждённым отсутствием кофеина; по неизвестным данным подбор остановлен." if validated["locale"] == "ru" else "У каталозі немає наборів із підтвердженою відсутністю кофеїну; за невідомих даних підбір зупинено."
    else:
        status = "no_match"
        message = "По выбранным фильтрам подтверждённых совпадений нет." if validated["locale"] == "ru" else "За вибраними фільтрами підтверджених збігів немає."

    return {
        "status": status,
        "test_only": True,
        "alternatives": True,
        "requested_count": validated["result_count"],
        "returned_count": len(selected_results),
        "message": message,
        "results": selected_results,
    }
