#!/usr/bin/env python3
"""Fetch a product page from a URL or raw file, parse candidate signals, and identify research gaps."""

import argparse
import json
import re
import sys
import urllib.request
from typing import Any, Dict, List

CUE_MAP = {
    "activity": {
        "running": ["біг", "бег", "марафон", "напівмарафон", "полумарафон", "трейл", "забіг", "забег"],
        "cycling": ["вело", "велосипед", "cycling", "bike"],
        "hiking": ["похід", "поход", "кемпінг", "трекінг", "гори", "горах"],
        "strength_training": ["зал", "силові", "силовые", "гантелі", "штанга", "жим", "м'язи", "мышцы", "маса", "масса"],
        "functional_training": ["кросфіт", "crossfit", "функціонал", "hiit"],
        "swimming": ["плаван", "басейн", "бассейн"],
    },
    "component_classes": {
        "hydration_items": ["ізотонік", "изотоник", "електроліт", "электролит", "гідратац", "гидратац", "пляшка", "бутылка", "hydria"],
        "creatine_preworkout": ["креатин", "creatine", "передтренув", "предтреник", "pre-workout", "бета-аланін", "bcaa"],
        "protein_carbohydrate_food": ["батончик", "печиво", "печенье", "вафл", "вуглевод", "углевод", "протеїн", "протеин", "снек"],
        "supplements_vitamins_minerals": ["вітамін", "витамин", "магній", "магний", "цинк", "d3", "omega", "омега", "кальцій", "селен"],
        "apparel_footwear": ["шкарпет", "носки", "кепка", "бандана", "термошкарпет"],
        "sports_accessories": ["шейкер", "пояс для номера", "тримач"],
        "dehydrated_meal": ["сублім", "сублим", "їжа в похід", "каша"],
    },
    "product_forms": {
        "gel": ["гель", "гелі", "гели", "gel", "hydrogel"],
        "bars": ["батончик", "батончики", "bar", "bars"],
        "liquid": ["рідк", "жидк", "шот", "shot", "ампул"],
        "powder": ["порошок", "порошковий", "порошковый"],
        "sticks": ["стик", "стік", "саше", "stick", "sticks"],
        "capsules": ["капсул", "caps"],
        "softgels": ["softgel", "м'які капсули", "мягкие капсулы"],
        "tablets": ["таблет", "табл"],
        "apparel": ["шкарпет", "носки", "одяг", "кепка"],
    },
    "race_formats": {
        "half_marathon": ["напівмарафон", "полумарафон", "21 км", "21.1"],
        "marathon": ["марафон", "42 км", "42.2"],
        "ultra_or_long_distance": ["ультра", "ultra", "50 км", "100 км", "ironman"],
        "race_or_event_preparation": ["5 км", "10 км", "змагання", "старт", "гонк"],
    },
    "weather": {
        "cold_weather": ["термо", "зимов", "зимн", "холод", "мороз", "осінь-зима"],
        "hot_weather": ["літн", "летн", "спека", "жара", "summer"],
    }
}


def fetch_url_content(url: str) -> str:
    """Fetch raw HTML text using a standard browser User-Agent."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
        "Accept-Language": "uk-UA,uk;q=0.9,ru;q=0.8,en;q=0.7",
    }
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=15) as resp:
        return resp.read().decode("utf-8", errors="replace")


def parse_html_signals(html: str, url: str) -> Dict[str, Any]:
    """Parse signals from raw page text."""
    # 1. Clean HTML tags
    title_match = re.search(r"<h1[^>]*>(.*?)</h1>", html, re.IGNORECASE | re.DOTALL)
    title = title_match.group(1).strip() if title_match else ""
    title = re.sub(r"<[^>]+>", "", title).strip()

    # Meta title fallback
    if not title:
        meta_m = re.search(r"<title[^>]*>(.*?)</title>", html, re.IGNORECASE | re.DOTALL)
        if meta_m:
            title = meta_m.group(1).split("—")[0].split("-")[0].strip()

    # 2. Price extraction
    price = None
    price_match = re.search(r'class="[^"]*price[^"]*"[^>]*>([\d\s]+)\s*(?:грн|₴)', html, re.IGNORECASE)
    if price_match:
        digits = re.sub(r"\D", "", price_match.group(1))
        if digits:
            price = int(digits)

    # 3. SKU extraction
    sku = None
    sku_m = re.search(r'(?:Артикул|SKU|Код товару)[:\s]*(?:<[^>]*>)*\s*([A-Za-z0-9_-]+)', html, re.IGNORECASE)
    if not sku_m:
        sku_m = re.search(r'(RE\d{4,6}|Nabir_\d{3,5})', html)
    if sku_m:
        sku = sku_m.group(1).strip()

    # 4. Text body
    text_content = re.sub(r"<script[^>]*>.*?</script>", " ", html, flags=re.IGNORECASE | re.DOTALL)
    text_content = re.sub(r"<style[^>]*>.*?</style>", " ", text_content, flags=re.IGNORECASE | re.DOTALL)
    text_content = re.sub(r"<[^>]+>", " ", text_content)
    text_content = " ".join(text_content.split())
    text_lower = text_content.lower()

    # 5. Composition detection
    comp_lines: List[str] = []
    bullet_matches = re.findall(r'<li[^>]*>(.*?)</li>', html, re.IGNORECASE | re.DOTALL)
    for b in bullet_matches:
        cleaned_b = re.sub(r"<[^>]+>", "", b).strip()
        if len(cleaned_b) > 4 and any(w in cleaned_b.lower() for w in ["х", "x", "шт", "г", "мл", "таб", "капс", "пар"]):
            comp_lines.append(cleaned_b)

    composition = "; ".join(comp_lines) if comp_lines else title

    # 6. Signal analysis via keywords
    detected_activities: List[str] = []
    for act, kws in CUE_MAP["activity"].items():
        if any(kw in text_lower for kw in kws):
            detected_activities.append(act)

    detected_classes: List[str] = []
    for cls, kws in CUE_MAP["component_classes"].items():
        if any(kw in text_lower for kw in kws):
            detected_classes.append(cls)

    detected_forms: List[str] = []
    for frm, kws in CUE_MAP["product_forms"].items():
        if any(kw in text_lower for kw in kws):
            detected_forms.append(frm)

    detected_races: List[str] = []
    for rce, kws in CUE_MAP["race_formats"].items():
        if any(kw in text_lower for kw in kws):
            detected_races.append(rce)

    detected_weather: List[str] = []
    for wth, kws in CUE_MAP["weather"].items():
        if any(kw in text_lower for kw in kws):
            detected_weather.append(wth)

    # Sizes
    size_matches = re.findall(r'\b(3[5-9]|4[0-8])[–-](\d{2})\b', text_content)
    size_values = [{"type": "shoe_or_sock_size", "value": f"{s[0]}-{s[1]}"} for s in size_matches]

    # Membership
    is_membership = any(w in text_lower for w in ["абонемент", "membership", "club", "клуб"])

    # 7. Goal Families Assignment
    seller_families: List[str] = []
    if "running" in detected_activities:
        seller_families.append("running_race_preparation")
    if "strength_training" in detected_activities:
        seller_families.append("strength_muscle_training")
    if "hydration_items" in detected_classes:
        seller_families.append("hydration_electrolytes")
    if "protein_carbohydrate_food" in detected_classes:
        seller_families.append("portable_food_snacks")
    if "hiking" in detected_activities:
        seller_families.append("outdoor_travel_hiking")
    if "apparel_footwear" in detected_classes:
        seller_families.append("foot_apparel_comfort")
    if not seller_families:
        seller_families.append("general_daily_nutrition")

    # 8. Research Gaps Identification
    research_tasks: List[str] = []
    if not price:
        research_tasks.append("Missing price_uah: check page or search price for this SKU.")
    if not sku:
        research_tasks.append("Missing SKU: search official site or catalog to locate item code.")
    if not comp_lines:
        research_tasks.append("Composition details missing: search manufacturer site or exact component breakdown.")
    if "apparel_footwear" in detected_classes and not size_values:
        research_tasks.append("Apparel present but no shoe/sock size range found: research available sizes.")
    if not detected_forms:
        research_tasks.append("Product forms unclear: research whether items are gels, powders, bars or tablets.")

    item_types = []
    if "apparel_footwear" in detected_classes:
        item_types.append("apparel_bundle")
    if "protein_carbohydrate_food" in detected_classes:
        item_types.append("snack_bundle")
    if "supplements_vitamins_minerals" in detected_classes:
        item_types.append("supplement_bundle")
    if is_membership:
        item_types.append("club_membership_bundle")

    draft_record = {
        "title": title or "Новий набір",
        "sku": sku,
        "price_uah": price or 1000,
        "source_url": url,
        "composition": composition,
        "description": text_content[:500],
        "tags": {
            "item_type": item_types or ["equipment_bundle"],
            "availability": ["in_stock"],
        },
        "matching_evidence": {
            "status": "candidate_direct_seller_positioning",
            "seller_families": seller_families,
            "component_families": seller_families,
            "seller_activity_groups": detected_activities or ["running"],
            "component_activity_groups": detected_activities or ["running"],
            "component_classes": detected_classes or ["protein_carbohydrate_food"],
            "use_contexts": ["event_preparation" if detected_races else "training"],
            "race_formats": detected_races or ["race_or_event_preparation"],
            "product_forms": detected_forms or ["bars"],
            "size_sensitive": bool(size_values),
            "size_values": size_values,
            "weather_signals": detected_weather,
            "conflict_notes": [],
        },
        "research_tasks": research_tasks,
    }

    return draft_record


def main():
    parser = argparse.ArgumentParser(description="Fetch and parse product kit from URL or file")
    parser.add_argument("source", help="URL or path to saved HTML file")
    parser.add_argument("--out", help="Output JSON path")
    args = parser.parse_args()

    if args.source.startswith("http"):
        print(f"Fetching {args.source}...")
        html = fetch_url_content(args.source)
        url = args.source
    else:
        from pathlib import Path
        html = Path(args.source).read_text(encoding="utf-8")
        url = "https://raceexpert.com.ua/product-kit"

    parsed = parse_html_signals(html, url)
    out_json = json.dumps(parsed, ensure_ascii=False, indent=2)

    if args.out:
        from pathlib import Path
        Path(args.out).write_text(out_json, encoding="utf-8")
        print(f"Saved to {args.out}")
    else:
        print(out_json)

    if parsed["research_tasks"]:
        print(f"\n[ATTENTION] Found {len(parsed['research_tasks'])} research tasks:")
        for t in parsed["research_tasks"]:
            print(f"  👉 {t}")
    else:
        print("\n[OK] Kit parsed completely with zero information gaps.")


if __name__ == "__main__":
    main()
