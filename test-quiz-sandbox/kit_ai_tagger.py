"""AI Kit Tagger & Enricher for Race Expert Quiz.

Converts raw OpenCart product titles and descriptions into structured matching evidence
adhering to the 6-agent catalog taxonomy.
"""

import os
import re
import json
import logging
import urllib.request
import urllib.error
from typing import Dict, List, Optional, Any
from pathlib import Path

logger = logging.getLogger(__name__)

CANONICAL_GOALS = [
    "running", "training", "hydration", "food", "recovery", "outdoors", "gear", "daily", "gift"
]

CANONICAL_FAMILIES = {
    "running": ["running_race_preparation"],
    "training": ["strength_muscle_training"],
    "hydration": ["hydration_electrolytes"],
    "food": ["endurance_energy", "portable_food_snacks"],
    "recovery": ["sleep_relaxation_stress", "recovery_fatigue"],
    "outdoors": ["outdoor_travel_hiking"],
    "gear": ["foot_apparel_comfort"],
    "daily": ["general_daily_nutrition"],
    "gift": ["gift_identity"]
}

CANONICAL_CLASSES = [
    "energy_nutrition", "hydration_items", "protein_carbohydrate_food",
    "supplements_vitamins_minerals", "food_or_meal", "dehydrated_meal",
    "creatine_preworkout", "sports_accessories", "apparel_footwear"
]

CANONICAL_PRODUCT_FORMS = [
    "gel", "powder", "bars", "tablets", "capsules", "softgels", "liquid", "sticks", "food_or_meal"
]

PROMPT_SYSTEM = """Ти — головний класифікатор спортивного харчування та спорядження Race Expert.
Твоє завдання — проаналізувати товар (назву, опис, ціну) та згенерувати сувору JSON-розмітку для алгоритму підбору квиза.

Правила класифікації:
1. goals: список з [running, training, hydration, food, recovery, outdoors, gear, daily, gift].
2. component_classes: список з [energy_nutrition, hydration_items, protein_carbohydrate_food, supplements_vitamins_minerals, food_or_meal, dehydrated_meal, creatine_preworkout, sports_accessories, apparel_footwear].
3. product_forms: список з [gel, powder, bars, tablets, capsules, softgels, liquid, sticks, food_or_meal]. Якщо це ТІЛЬКИ шкарпетки, пляшки чи аксесуари — product_forms ПОВИНЕН бути порожнім!
4. activities: список з [running, cycling, triathlon, hiking, walking, fitness_gym, strength_training, functional_training, general_lifestyle].
5. race_formats: список з [10km, half_marathon, marathon, ultra_trail, ironman] (якщо застосовно).
6. composition: короткий структурований опис що входить у набір (1-2 речення).
7. size_sensitive: true, якщо це одяг/шкарпетки з конкретним розміром, інакше false.
8. size_values: знайдений розмір (наприклад ["M"], ["40-42"], ["43-45"]).
9. has_creatine: true, якщо містить креатин або передтренувальний стимулятор, інакше false.
10. summary: короткий експертний висновок (чому і для кого цей набір).

Повертай ТІЛЬКИ валідний JSON без додаткового тексту."""


class HeuristicKitTagger:
    """Fast, deterministic regex-based tagger for offline or fallback operation."""

    def tag(self, product: Dict[str, Any]) -> Dict[str, Any]:
        text = f"{product.get('title', '')} {product.get('description', '')}".lower()
        title = product.get("title", "").lower()

        goals = set()
        classes = set()
        forms = set()
        activities = set()
        race_formats = []
        size_values = []
        has_creatine = False

        # Detect creatine / heavy preworkout
        if "креатин" in text or "creatine" in text or "предтрен" in text or "pre-workout" in text:
            has_creatine = True
            classes.add("creatine_preworkout")
            goals.add("training")

        # Detect energy / gels
        if "гель" in text or "gel" in text or "енергетич" in text or "energy" in text:
            classes.add("energy_nutrition")
            forms.add("gel")
            goals.add("running")
            goals.add("food")
            activities.add("running")

        # Detect hydration / isotonic / electrolytes
        if "ізотонік" in text or "изотоник" in text or "електроліт" in text or "электролит" in text or "гідратац" in text or "сольові" in text:
            classes.add("hydration_items")
            goals.add("hydration")
            activities.update(["running", "cycling"])
            if "порошок" in text:
                forms.add("powder")
            elif "таблет" in text:
                forms.add("tablets")
            elif "капсул" in text:
                forms.add("capsules")

        # Detect apparel / socks / sizing
        if "шкарпет" in text or "носк" in text or "термо" in text or "одяг" in text or "одежд" in text:
            classes.add("apparel_footwear")
            goals.add("gear")
            activities.update(["running", "hiking", "walking"])
            
            # Sizing match
            size_match = re.search(r"(\b[smlx]{1,3}\b|\b\d{2}[–-]\d{2}\b)", title)
            if size_match:
                size_values.append(size_match.group(1).upper())

        # Detect outdoor / hiking / meals
        if "похід" in text or "поход" in text or "туризм" in text or "сублим" in text or "сублім" in text or "сухпай" in text or "сніданок" in text:
            goals.add("outdoors")
            activities.update(["hiking", "walking"])
            if "сублим" in text or "сублім" in text or "страва" in text:
                classes.add("dehydrated_meal")
                forms.add("food_or_meal")

        # Detect recovery / sleep / protein
        if "відновлен" in text or "восстановлен" in text or "сон" in text or "релакс" in text or "мелатонін" in text or "магній" in text:
            if not has_creatine:
                goals.add("recovery")
            classes.add("supplements_vitamins_minerals")
            if "протеїн" in text or "protein" in text:
                classes.add("protein_carbohydrate_food")

        # Detect distance / race format
        if "марафон" in text or "42" in text:
            race_formats.append("marathon")
            goals.add("running")
            activities.add("running")
        elif "півмарафон" in text or "полумарафон" in text or "21" in text:
            race_formats.append("half_marathon")
            goals.add("running")
            activities.add("running")
        elif "10 км" in text or "10km" in text:
            race_formats.append("10km")
            goals.add("running")
            activities.add("running")

        # Default fallbacks
        if not goals:
            goals.add("running")
        if not classes:
            classes.add("energy_nutrition")
        if not activities:
            activities.add("running")

        size_sensitive = bool(size_values or "apparel_footwear" in classes)

        seller_families = []
        for g in sorted(goals):
            seller_families.extend(CANONICAL_FAMILIES.get(g, []))

        return {
            "goals": sorted(goals),
            "seller_families": seller_families,
            "component_families": seller_families,
            "component_classes": sorted(classes),
            "seller_activity_groups": sorted(activities),
            "component_activity_groups": sorted(activities),
            "product_forms": sorted(forms),
            "race_formats": race_formats,
            "size_sensitive": size_sensitive,
            "size_values": size_values,
            "has_creatine": has_creatine,
            "composition": product.get("description", "")[:250] or product.get("title", ""),
            "seller_summary": f"Підібраний експертний комплект «{product.get('title')}» для активних цілей."
        }


class LLMKitTagger:
    """Calls OpenAI API to perform high-fidelity structured catalog extraction."""

    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-6-luna"):
        from ai_consultant import _get_api_key
        self.api_key = api_key or _get_api_key()
        self.model = model
        self.fallback = HeuristicKitTagger()

    def tag(self, product: Dict[str, Any]) -> Dict[str, Any]:
        if not self.api_key:
            logger.info("No OpenAI API key found; using heuristic tagger.")
            return self.fallback.tag(product)

        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

        user_content = (
            f"Товар: {product.get('title')}\n"
            f"Артикул: {product.get('sku') or product.get('model')}\n"
            f"Ціна: {product.get('price_uah')} грн\n"
            f"Опис:\n{product.get('description', '')[:1200]}\n"
        )

        payload = {
            "model": self.model,
            "reasoning_effort": "none",
            "messages": [
                {"role": "system", "content": PROMPT_SYSTEM},
                {"role": "user", "content": user_content}
            ],
            "response_format": {"type": "json_object"},
        }

        try:
            req = urllib.request.Request(
                url,
                data=json.dumps(payload).encode("utf-8"),
                headers=headers,
                method="POST"
            )
            with urllib.request.urlopen(req, timeout=12.0) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                content = data["choices"][0]["message"]["content"]
                parsed = json.loads(content)
                return self._normalize_llm_response(parsed, product)
        except Exception as e:
            logger.warning(f"LLM tagging failed for {product.get('sku')}: {e}. Falling back to heuristic.")
            return self.fallback.tag(product)

    def _normalize_llm_response(self, raw: Dict[str, Any], product: Dict[str, Any]) -> Dict[str, Any]:
        """Validate and normalize LLM response into quiz evidence structure."""
        goals = [g for g in raw.get("goals", []) if g in CANONICAL_GOALS]
        if not goals:
            goals = ["running"]

        classes = [c for c in raw.get("component_classes", []) if c in CANONICAL_CLASSES]
        if not classes:
            classes = ["energy_nutrition"]

        forms = [f for f in raw.get("product_forms", []) if f in CANONICAL_PRODUCT_FORMS]
        # Consumable guard: if non-consumable, strip forms
        non_consumables = {"sports_accessories", "apparel_footwear"}
        if set(classes).issubset(non_consumables):
            forms = []

        activities = raw.get("activities", ["running"])
        seller_families = []
        for g in goals:
            seller_families.extend(CANONICAL_FAMILIES.get(g, []))

        size_values = raw.get("size_values", [])
        size_sensitive = bool(raw.get("size_sensitive", False) or size_values or "apparel_footwear" in classes)

        return {
            "goals": sorted(set(goals)),
            "seller_families": sorted(set(seller_families)),
            "component_families": sorted(set(seller_families)),
            "component_classes": sorted(set(classes)),
            "seller_activity_groups": sorted(set(activities)),
            "component_activity_groups": sorted(set(activities)),
            "product_forms": sorted(set(forms)),
            "race_formats": raw.get("race_formats", []),
            "size_sensitive": size_sensitive,
            "size_values": size_values,
            "has_creatine": bool(raw.get("has_creatine", False) or "creatine_preworkout" in classes),
            "composition": raw.get("composition") or product.get("description", "")[:250] or product.get("title", ""),
            "seller_summary": raw.get("summary") or f"Експертний набір «{product.get('title')}»."
        }
