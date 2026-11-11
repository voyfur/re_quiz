#!/usr/bin/env python3
"""Normalize and validate a new product kit dictionary for the Race Expert quiz catalog."""

from pathlib import Path
import re
import sys
from typing import Any, Dict, List, Set

VALID_GOAL_FAMILIES: Set[str] = {
    "running_race_preparation",
    "strength_muscle_training",
    "hydration_electrolytes",
    "portable_food_snacks",
    "endurance_energy",
    "recovery_fatigue",
    "sleep_relaxation_stress",
    "outdoor_travel_hiking",
    "foot_apparel_comfort",
    "general_daily_nutrition",
    "gift_identity",
    "bone_joint_support_claim",
    "immune_support_claim",
    "focus_cognition",
    "skin_beauty_claim",
    "digestive_metabolic_claim",
    "women_men_audience",
}

VALID_ACTIVITY_GROUPS: Set[str] = {
    "running", "cycling", "hiking", "strength_training", "functional_training",
    "swimming", "mind_body_mobility", "walking", "general_fitness", "other",
}

VALID_COMPONENT_CLASSES: Set[str] = {
    "protein_carbohydrate_food",
    "supplements_vitamins_minerals",
    "creatine_preworkout",
    "sports_accessories",
    "apparel_footwear",
    "hydration_items",
    "dehydrated_meal",
    "club_membership",
}

VALID_USE_CONTEXTS: Set[str] = {
    "event_preparation", "training", "everyday",
    "before_or_after_training", "during_training", "daily_use", "evening_or_bedtime",
    "hiking_or_camping", "travel_or_road", "work_or_study", "gift",
}

VALID_RACE_FORMATS: Set[str] = {
    "half_marathon", "marathon", "race_or_event_preparation", "ultra_or_long_distance", "unspecified",
}

VALID_PRODUCT_FORMS: Set[str] = {
    "bars", "gel", "liquid", "sticks", "capsules", "powder", "softgels", "tablets", "apparel", "food_or_meal",
}

VALID_WEATHER_SIGNALS: Set[str] = {
    "cold_weather", "winter", "hot_weather", "summer",
}

VALID_EVIDENCE_STATUSES: Set[str] = {
    "candidate_direct_seller_positioning",
    "candidate_component_signal",
    "conflict_review_required",
    "candidate_low_evidence",
}


class ValidationError(ValueError):
    """Raised when incoming kit data violates taxonomy or constraints."""


def normalize_kit(raw: Dict[str, Any]) -> Dict[str, Any]:
    """Validate and normalize a kit record against controlled vocabularies."""
    if not isinstance(raw, dict):
        raise ValidationError("Kit record must be a JSON dictionary.")

    # 1. Title
    title = str(raw.get("title", "")).strip()
    if not title or len(title) < 3:
        raise ValidationError("Missing or invalid 'title'.")

    # 2. Price
    raw_price = raw.get("price_uah")
    try:
        price_uah = int(round(float(raw_price)))
        if price_uah <= 0 or price_uah > 100_000:
            raise ValueError
    except (TypeError, ValueError):
        raise ValidationError(f"Invalid 'price_uah': expected positive integer, got {raw_price!r}")

    # 3. Source URL
    source_url = str(raw.get("source_url", "")).strip()
    if not source_url.startswith("http"):
        raise ValidationError(f"Invalid 'source_url': expected HTTP(S) URL, got {source_url!r}")

    # 4. Composition & Description
    composition = str(raw.get("composition", "")).strip()
    description = str(raw.get("description", "")).strip() or composition

    # 5. SKU
    sku = raw.get("sku")
    sku = str(sku).strip() if sku else None

    # 6. Tags
    tags = raw.get("tags") or {}
    item_type = list(tags.get("item_type", []))
    comp_lower = composition.lower()
    title_lower = title.lower()

    if "абонемент" in comp_lower or "membership" in comp_lower or "club" in title_lower or "клуб" in title_lower:
        if "club_membership_bundle" not in item_type:
            item_type.append("club_membership_bundle")

    # 7. Matching Evidence Sub-dictionary
    evidence = raw.get("matching_evidence") or {}

    status = evidence.get("status", "candidate_direct_seller_positioning")
    if status not in VALID_EVIDENCE_STATUSES:
        raise ValidationError(f"Invalid evidence status: {status!r}. Allowed: {sorted(VALID_EVIDENCE_STATUSES)}")

    def filter_enum_list(field_name: str, allowed: Set[str]) -> List[str]:
        items = evidence.get(field_name) or []
        cleaned: List[str] = []
        for it in items:
            it_str = str(it).strip().lower()
            if it_str in allowed:
                if it_str not in cleaned:
                    cleaned.append(it_str)
            else:
                print(f"[WARN] Unknown term {it_str!r} dropped from {field_name}", file=sys.stderr)
        return cleaned

    seller_families = filter_enum_list("seller_families", VALID_GOAL_FAMILIES)
    component_families = filter_enum_list("component_families", VALID_GOAL_FAMILIES)
    seller_activity = filter_enum_list("seller_activity_groups", VALID_ACTIVITY_GROUPS)
    component_activity = filter_enum_list("component_activity_groups", VALID_ACTIVITY_GROUPS)
    component_classes = filter_enum_list("component_classes", VALID_COMPONENT_CLASSES)
    use_contexts = filter_enum_list("use_contexts", VALID_USE_CONTEXTS)
    race_formats = filter_enum_list("race_formats", VALID_RACE_FORMATS)
    product_forms = filter_enum_list("product_forms", VALID_PRODUCT_FORMS)
    weather_signals = filter_enum_list("weather_signals", VALID_WEATHER_SIGNALS)

    if not seller_families and not component_families:
        raise ValidationError("Kit must map to at least one valid goal family in seller_families or component_families.")

    # 8. Sizing
    size_sensitive = bool(evidence.get("size_sensitive", False))
    raw_sizes = evidence.get("size_values") or []
    size_values = []
    if size_sensitive:
        for s in raw_sizes:
            val = str(s.get("value", "")).replace("–", "-").strip()
            if re.match(r"^\d{2}-\d{2}$", val):
                size_values.append({"type": "shoe_or_sock_size", "value": val})

    conflict_notes = list(evidence.get("conflict_notes") or [])

    return {
        "title": title,
        "sku": sku,
        "price_uah": price_uah,
        "source_url": source_url,
        "composition": composition,
        "description": description,
        "tags": {
            "item_type": sorted(set(item_type)),
            "availability": tags.get("availability", ["in_stock"]),
        },
        "matching_evidence": {
            "status": status,
            "seller_families": seller_families,
            "component_families": component_families,
            "seller_activity_groups": seller_activity,
            "component_activity_groups": component_activity,
            "component_classes": component_classes,
            "use_contexts": use_contexts,
            "race_formats": race_formats,
            "product_forms": product_forms,
            "size_sensitive": size_sensitive and len(size_values) > 0,
            "size_values": size_values,
            "weather_signals": weather_signals,
            "conflict_notes": conflict_notes,
        },
    }


if __name__ == "__main__":
    import json
    if len(sys.argv) > 1:
        path = sys.argv[1]
        data = json.loads(Path(path).read_text(encoding="utf-8"))
        norm = normalize_kit(data)
        print(json.dumps(norm, ensure_ascii=False, indent=2))
        print("\n[OK] Kit normalized successfully.")
    else:
        print("Usage: python3 normalize_kit_data.py <path_to_kit.json>")
