"""Kit Data Guard for Race Expert Quiz.

Enforces the 6-agent domain constraints before any kit is admitted to the quiz catalog.
"""

import logging
from typing import Dict, List, Tuple, Any

logger = logging.getLogger(__name__)

CONSUMABLE_CLASSES = {
    "energy_nutrition", "hydration_items", "protein_carbohydrate_food",
    "supplements_vitamins_minerals", "food_or_meal", "dehydrated_meal", "creatine_preworkout"
}

NON_CONSUMABLE_CLASSES = {
    "sports_accessories", "apparel_footwear"
}

CONSUMABLE_FORMS = {
    "gel", "powder", "bars", "tablets", "capsules", "softgels", "liquid", "sticks", "food_or_meal"
}


class KitDataGuard:
    """Validates and enforces integrity rules for catalog kit entries."""

    @classmethod
    def validate_and_fix(cls, item: Dict[str, Any], tag_data: Dict[str, Any]) -> Tuple[bool, List[str], Dict[str, Any]]:
        """Validates entry against 6 core rules, auto-fixing minor issues where safe.

        Returns:
            (is_valid, issues_list, fixed_tag_data)
        """
        issues = []
        fixed = dict(tag_data)
        
        classes = set(fixed.get("component_classes", []))
        forms = set(fixed.get("product_forms", []))
        goals = set(fixed.get("goals", []))
        race_formats = set(fixed.get("race_formats", []))
        
        # Rule 1: Apparel Sizing Guard
        if "apparel_footwear" in classes:
            fixed["size_sensitive"] = True
            if not fixed.get("size_values"):
                # Warning if no explicit size extracted
                issues.append("RULE1_WARNING: Apparel item without explicit size_values.")

        # Rule 2: Hydration / Marathon Integrity Guard (applies to nutrition/hydration sets, not pure apparel)
        if "apparel_footwear" not in classes:
            if any(f in race_formats for f in ["marathon", "half_marathon", "ultra_trail"]):
                needed = {"energy_nutrition", "hydration_items"}
                if not (classes & needed):
                    issues.append("RULE2_WARNING: Endurance distance set lacks energy/hydration components. Adding energy_nutrition.")
                    classes.add("energy_nutrition")

        # Rule 3: Creatine Isolation Guard
        if fixed.get("has_creatine") or "creatine_preworkout" in classes:
            if "recovery" in goals:
                issues.append("RULE3_FIX: Creatine isolated: removed 'recovery' goal to prevent bedtime contraindication.")
                goals.discard("recovery")
            if "daily" in goals:
                issues.append("RULE3_FIX: Creatine isolated: removed 'daily' goal.")
                goals.discard("daily")
            goals.add("training")

        # Rule 4: Consumable vs Hardware Product Forms Guard
        if not (classes & CONSUMABLE_CLASSES):
            # Pure non-consumable hardware/apparel cannot have food forms
            leaked_forms = forms & CONSUMABLE_FORMS
            if leaked_forms:
                issues.append(f"RULE4_FIX: Removed food forms {leaked_forms} from non-consumable kit.")
                forms.difference_update(CONSUMABLE_FORMS)

        # Rule 5: Outdoor Food & Meals Guard
        if "dehydrated_meal" in classes:
            goals.add("outdoors")
            fixed["seller_families"] = list(set(fixed.get("seller_families", [])) | {"outdoor_travel_hiking"})

        # Rule 6: Price & Stock Sanity
        price = item.get("price_uah", 0)
        if price <= 0:
            issues.append("RULE6_ERROR: Kit price is zero or negative.")
            return False, issues, fixed

        # Sync back fixed structures
        fixed["component_classes"] = sorted(classes)
        fixed["product_forms"] = sorted(forms)
        fixed["goals"] = sorted(goals)

        return True, issues, fixed
