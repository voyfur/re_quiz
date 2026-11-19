"""Multi-Sport Box Decision Engine.

Builds personalized 4-slot equipment and nutrition boxes for:
- Running & Trail (478 items)
- Cycling (30 items)
- Triathlon & Swimming (30 items)
- Gym & Fitness (30 items)
- Hiking & Outdoor / ЇDLO (30 items)
"""

import json
from pathlib import Path
from typing import Dict, List, Any
import runner_box_engine

BASE_DIR = Path(__file__).resolve().parent

# Catalog Cache
_CATALOGS: Dict[str, List[Dict[str, Any]]] = {}


def load_catalog(sport: str) -> List[Dict[str, Any]]:
    global _CATALOGS
    if sport in _CATALOGS:
        return _CATALOGS[sport]

    filename_map = {
        "running": "running_catalog.json",
        "cycling": "cycling_catalog.json",
        "triathlon": "triathlon_catalog.json",
        "gym": "gym_catalog.json",
        "outdoor": "outdoor_catalog.json"
    }

    file_path = BASE_DIR / filename_map.get(sport, "running_catalog.json")
    if file_path.exists():
        with open(file_path, "r", encoding="utf-8") as f:
            _CATALOGS[sport] = json.load(f)
    else:
        _CATALOGS[sport] = []

    return _CATALOGS[sport]


def score_item(p: dict, price_tier: str, priority_keywords: List[str] = None) -> float:
    score = 50.0
    if p.get("price_tier") == price_tier:
        score += 35.0
    elif (price_tier == "premium" and p.get("price_tier") == "standard") or (price_tier == "economy" and p.get("price_tier") == "standard"):
        score += 15.0

    # Brand bonus
    brand = p.get("brand", "")
    if brand in ["SiS", "Maurten", "Precision Fuel & Hydration", "GU Energy", "Sponser", "Race Expert", "Optimum Nutrition", "Scitec Nutrition", "ЇDLO", "Chamois Butt'r"]:
        score += 20.0

    # Stock availability bonus
    qty = p.get("quantity", 0)
    if qty > 20:
        score += 8.0

    # Priority keywords synergy
    if priority_keywords:
        name_lower = p.get("name", "").lower()
        if any(k in name_lower for k in priority_keywords):
            score += 20.0

    return score


def pick_with_alts(available: List[dict], slot: str, price_tier: str, sub_type: str = None, need_caffeine: bool = None, exclude_ids: set = None, priority_keywords: List[str] = None, allowed_sub_types: List[str] = None):
    candidates = [p for p in available if p.get("slot") == slot]
    if exclude_ids:
        unexcluded = [p for p in candidates if p.get("product_id") not in exclude_ids]
        if unexcluded:
            candidates = unexcluded

    if allowed_sub_types:
        sub_m = [p for p in candidates if p.get("sub_type") in allowed_sub_types]
        if sub_m:
            candidates = sub_m
    elif sub_type:
        sub_m = [p for p in candidates if p.get("sub_type") == sub_type]
        if sub_m:
            candidates = sub_m

    if need_caffeine is not None:
        caff_m = [p for p in candidates if p.get("caffeine") == need_caffeine]
        if caff_m:
            candidates = caff_m

    if not candidates:
        # Fallback to any in slot
        candidates = [p for p in available if p.get("slot") == slot]
        if need_caffeine is not None:
            caff_m = [p for p in candidates if p.get("caffeine") == need_caffeine]
            if caff_m:
                candidates = caff_m

    if not candidates:
        return None, []

    candidates.sort(key=lambda p: (-score_item(p, price_tier, priority_keywords), p.get("price", 0)))
    primary = candidates[0]
    alternatives = candidates[1:6]
    return primary, alternatives


def optimize_box_for_budget(slots: dict, custom_budget: float, current_total: float, catalog: list = None) -> float:
    if not custom_budget or current_total <= custom_budget:
        return current_total

    all_entries = []
    for slot_name, slot_items in slots.items():
        for it in slot_items:
            all_entries.append((slot_name, it))
    all_entries.sort(key=lambda x: x[1]["product"]["price"] * x[1]["quantity_recommended"], reverse=True)

    # Pass 1: Try alternatives already attached to the item
    for slot_name, it in all_entries:
        if current_total <= custom_budget:
            break
        curr_price = it["product"]["price"]
        qty = it["quantity_recommended"]
        alts = it.get("alternatives", [])
        cheaper_alts = [a for a in alts if a.get("price", 0) < curr_price and a.get("quantity", 0) > 0]
        cheaper_alts.sort(key=lambda a: a.get("price", 0))
        if cheaper_alts:
            best_alt = cheaper_alts[0]
            diff = (curr_price - best_alt["price"]) * qty
            it["product"] = best_alt
            current_total -= diff

    # Pass 2: Gently reduce quantities of multi-unit consumables (down to min 1)
    if current_total > custom_budget:
        for slot_name, it in all_entries:
            if current_total <= custom_budget:
                break
            qty = it["quantity_recommended"]
            sub = it["product"].get("sub_type")
            # For gym snacks/bars/shots, preserve pack size (min 4 units)
            # For outdoor hot meals, keep minimum 2 to guarantee complete pack (6+ meals for weekend, 8-12 for expedition)
            if sub in ["energy_shot", "protein_bar", "protein_snack"]:
                min_qty = 4
            elif sub in ["breakfast_meal", "gourmet_soup", "gourmet_meal", "jerky", "recovery_porridge"]:
                min_qty = 2
            else:
                min_qty = 1

            if qty > min_qty:
                price = it["product"]["price"]
                reduce_by = min(qty - min_qty, int((current_total - custom_budget) // price) + 1)
                if reduce_by > 0:
                    it["quantity_recommended"] -= reduce_by
                    current_total -= reduce_by * price

    # Pass 3: If still over budget and catalog provided, look for cheaper candidates in that slot
    # preserving caffeine status, unique items, and protected functional sub_types
    if current_total > custom_budget and catalog:
        existing_ids = {it["product"]["product_id"] for _, it in all_entries}
        protein_subtypes = {"whey_protein", "diet_whey", "whey_isolate", "vegan_protein"}
        protected_subtypes = {
            "anti_chlorine", "race_number_belt", "flasks", "anti_chafe_cream", "anti_chafe",
            "magnesium", "salt_caps", "protein_powder", "shaker",
            "trekking_socks", "soft_flask", "water_bottle", "gourmet_meal", "gourmet_soup",
            "breakfast_meal", "jerky", "electrolyte_tablets", "recovery_porridge",
            "creatine", "bcaa", "l_carnitine", "cla", "fat_burner"
        } | protein_subtypes
        for slot_name, it in all_entries:
            if current_total <= custom_budget:
                break
            curr_prod = it["product"]
            curr_price = curr_prod["price"]
            curr_st = curr_prod.get("sub_type")
            curr_caff = curr_prod.get("caffeine", False)
            qty = it["quantity_recommended"]

            candidates = [
                p for p in catalog
                if p.get("slot") == slot_name
                and p.get("price", 0) < curr_price
                and p.get("quantity", 0) > 0
                and p.get("product_id") not in existing_ids
                and p.get("caffeine", False) == curr_caff
            ]
            if curr_st in protein_subtypes:
                candidates = [p for p in candidates if p.get("sub_type") in protein_subtypes]
            elif curr_st in protected_subtypes:
                candidates = [p for p in candidates if p.get("sub_type") == curr_st]
            candidates.sort(key=lambda p: p.get("price", 0))
            if candidates:
                best_cand = candidates[0]
                existing_ids.discard(curr_prod["product_id"])
                existing_ids.add(best_cand["product_id"])
                diff = (curr_price - best_cand["price"]) * qty
                it["product"] = best_cand
                current_total -= diff

    return round(current_total, 2)


def generate_cycling_box(inputs: Dict[str, Any], catalog: List[Dict[str, Any]]) -> Dict[str, Any]:
    distance_fmt = inputs.get("distance_format", "medium")  # short, medium, long
    price_tier = inputs.get("price_tier", "standard")
    caffeine_pref = inputs.get("caffeine_preference", "boost")
    weather = inputs.get("weather", "moderate")
    saddle_comfort = inputs.get("saddle_comfort", True)

    custom_budget = None
    raw_b = inputs.get("custom_budget") or inputs.get("max_budget")
    if raw_b:
        try:
            custom_budget = float(raw_b)
        except (ValueError, TypeError):
            custom_budget = None

    if custom_budget and not inputs.get("price_tier_explicit"):
        price_tier = "economy" if custom_budget < 2400 else ("standard" if custom_budget <= 3200 else "premium")

    available = [p for p in catalog if p.get("quantity", 0) > 0]
    if caffeine_pref == "none":
        available = [p for p in available if not p.get("caffeine", False)]

    slots = {"energy": [], "hydration": [], "gear": [], "care_recovery": []}
    used_ids = set()

    # --- 1. ENERGY SLOT (Solid Fuel + Fast Gels) ---
    # Solid fuel: Bakes / Bars / Chews
    if distance_fmt == "short":
        solid_qty = 2  # ~60g carbs
    elif distance_fmt == "medium":
        solid_qty = 3  # ~90g carbs
    else:  # long / Gran Fondo
        solid_qty = 5  # ~150g carbs

    solid_item, solid_alts = pick_with_alts(
        available, "energy", price_tier,
        allowed_sub_types=["bake", "bar", "chew"],
        exclude_ids=used_ids,
        priority_keywords=["bake", "chew", "bar", "beta fuel", "sponser"]
    )
    if not solid_item:
        solid_item, solid_alts = pick_with_alts(available, "energy", price_tier, exclude_ids=used_ids, priority_keywords=["bake", "bar", "chew"])

    if solid_item:
        used_ids.add(solid_item["product_id"])
        solid_timing = {
            "short": "Вживати по 1 батончику/бейку кожні 45-60 хвилин для підтримки сили",
            "medium": "Вживати 1 батончик/бейк щогодини протягом перших 3 годин заїзду",
            "long": "Вживати тверде паливо кожні 45-60 хв на рівнинних ділянках (перші 4-5 годин)"
        }
        slots["energy"].append({
            "product": solid_item,
            "quantity_recommended": solid_qty,
            "timing_instruction": solid_timing.get(distance_fmt, "Кожні 45-60 хв у сідлі"),
            "checked_by_default": True,
            "reason_badge": "Тверда енергія (попереджує голод та падіння сил)",
            "alternatives": solid_alts
        })

    # Fast Gels (Non-caffeine Base Gel)
    if distance_fmt == "short":
        base_gel_qty = 1
    elif distance_fmt == "medium":
        base_gel_qty = 2 if caffeine_pref == "none" else 1
    else:  # long
        base_gel_qty = 3 if caffeine_pref == "none" else 2

    gel_item, gel_alts = pick_with_alts(
        available, "energy", price_tier,
        sub_type="gel",
        need_caffeine=False,
        exclude_ids=used_ids,
        priority_keywords=["pf 30", "sis", "carbosnack", "maurten"]
    )
    if not gel_item:
        gel_item, gel_alts = pick_with_alts(available, "energy", price_tier, sub_type="gel", exclude_ids=used_ids)

    if gel_item:
        used_ids.add(gel_item["product_id"])
        gel_timing = {
            "short": "За 15-20 хвилин до фінального підйому або швидкісного темпового відрізка",
            "medium": "По 1 гелю перед підйомами та на другій половині маршруту",
            "long": "Швидкі вуглеводи для затяжних підйомів та останніх 40 км"
        }
        slots["energy"].append({
            "product": gel_item,
            "quantity_recommended": base_gel_qty,
            "timing_instruction": gel_timing.get(distance_fmt, "Перед підйомами"),
            "checked_by_default": True,
            "reason_badge": "Швидкий ізотонічний гель (миттєвий викид глюкози)",
            "alternatives": gel_alts
        })

    # Caffeine Boost Gel (if boost)
    if caffeine_pref == "boost":
        caff_gel_qty = 1 if distance_fmt != "long" else 2
        caff_item, caff_alts = pick_with_alts(
            available, "energy", price_tier,
            sub_type="caff_gel",
            need_caffeine=True,
            exclude_ids=used_ids,
            priority_keywords=["caffeine", "226ers", "gu", "carbosnack"]
        )
        if not caff_item:
            caff_item, caff_alts = pick_with_alts(available, "energy", price_tier, need_caffeine=True, exclude_ids=used_ids)
        if caff_item:
            used_ids.add(caff_item["product_id"])
            slots["energy"].append({
                "product": caff_item,
                "quantity_recommended": caff_gel_qty,
                "timing_instruction": "За 20-30 хв до найкрутішого градієнту або фінішного спринту",
                "checked_by_default": True,
                "reason_badge": "Кофеїновий буст (активація ЦНС та потужності у ватах)",
                "alternatives": caff_alts
            })

    # --- 2. HYDRATION SLOT (Isotonic / Drink Mix / Salt Caps) ---
    iso_item, iso_alts = pick_with_alts(
        available, "hydration", price_tier,
        exclude_ids=used_ids,
        priority_keywords=["tube", "isotonic", "drinx", "olimp", "precision"]
    )
    if iso_item:
        used_ids.add(iso_item["product_id"])
        is_sachet = iso_item.get("sub_type") in ["isotonic_sachet", "sachet"] or iso_item.get("price", 0) < 100
        if is_sachet:
            iso_qty = 1 if distance_fmt == "short" else (2 if distance_fmt == "medium" else 3)
        else:
            iso_qty = 1  # 1 tube contains 10-18 tabs

        slots["hydration"].append({
            "product": iso_item,
            "quantity_recommended": iso_qty,
            "timing_instruction": "Розчинити у велофлязі 500-750 мл. Пити кожні 15-20 хвилин маленькими ковтками",
            "checked_by_default": True,
            "reason_badge": "Ізотонічна гідратація та захист від зневоднення",
            "alternatives": iso_alts
        })

    if weather == "hot" or distance_fmt == "long":
        salt_item, salt_alts = pick_with_alts(available, "hydration", price_tier, sub_type="salt_caps", exclude_ids=used_ids)
        if salt_item:
            used_ids.add(salt_item["product_id"])
            slots["hydration"].append({
                "product": salt_item,
                "quantity_recommended": 1,
                "timing_instruction": "1 капсула на годину при інтенсивному потовиділенні від судом у литках",
                "checked_by_default": True,
                "reason_badge": "Сольовий баланс та електроліти",
                "alternatives": salt_alts
            })

    # --- 3. GEAR SLOT (Cycling bidon / socks) ---
    gear_item, gear_alts = pick_with_alts(available, "gear", price_tier, exclude_ids=used_ids)
    if gear_item:
        used_ids.add(gear_item["product_id"])
        slots["gear"].append({
            "product": gear_item,
            "quantity_recommended": 1,
            "timing_instruction": "Установити у фляготримач або одягти перед виїздом",
            "checked_by_default": True,
            "reason_badge": "Велоаксесуар для комфорту на треку",
            "alternatives": gear_alts
        })

    # --- 4. CARE & RECOVERY SLOT (Chamois Butt'r / Magneslife / Recovery Drink) ---
    if saddle_comfort:
        chamois, chamois_alts = pick_with_alts(
            available, "care_recovery", price_tier,
            sub_type="anti_chafe_cream",
            exclude_ids=used_ids,
            priority_keywords=["chamois", "butt'r"]
        )
        if chamois:
            used_ids.add(chamois["product_id"])
            slots["care_recovery"].append({
                "product": chamois,
                "quantity_recommended": 1,
                "timing_instruction": "Нанести на велопамперс та внутрішню поверхню стегон перед виїздом",
                "checked_by_default": True,
                "reason_badge": "Захист від натирання сідлом (Chamois Butt'r)",
                "alternatives": chamois_alts
            })

    if distance_fmt == "long":
        mag_item, mag_alts = pick_with_alts(
            available, "care_recovery", price_tier,
            sub_type="magnesium",
            exclude_ids=used_ids,
            priority_keywords=["magneslife", "magnesium"]
        )
        if mag_item and mag_item["product_id"] not in used_ids:
            used_ids.add(mag_item["product_id"])
            slots["care_recovery"].append({
                "product": mag_item,
                "quantity_recommended": 1,
                "timing_instruction": "При перших ознаках посмикування м'язів або перед останнім важким підйомом",
                "checked_by_default": True,
                "reason_badge": "Швидкий рідкий магній від спазмів",
                "alternatives": mag_alts
            })

    rec_item, rec_alts = pick_with_alts(
        available, "care_recovery", price_tier,
        exclude_ids=used_ids,
        allowed_sub_types=["recovery_drink", "recovery_tub", "recovery_sachet", "protein", "recovery_snack"],
        priority_keywords=["rego", "regener", "recovery", "протеїн"]
    )
    if rec_item and not any(it["product"]["product_id"] == rec_item["product_id"] for it in slots["care_recovery"]):
        used_ids.add(rec_item["product_id"])
        is_rec_sachet = rec_item.get("sub_type") in ["recovery_sachet", "sachet"] or rec_item.get("price", 0) < 250
        rec_qty = 2 if (is_rec_sachet and distance_fmt == "long") else 1

        slots["care_recovery"].append({
            "product": rec_item,
            "quantity_recommended": rec_qty,
            "timing_instruction": "Випити протягом 30 хвилин після тренування для швидкого відновлення м'язів",
            "checked_by_default": True,
            "reason_badge": "Швидке відновлення м'язових волокон",
            "alternatives": rec_alts
        })

    total_price = sum(it["product"]["price"] * it["quantity_recommended"] for s in slots.values() for it in s)
    if custom_budget:
        total_price = optimize_box_for_budget(slots, custom_budget, total_price, available)

    dist_labels = {"short": "Короткий заїзд (до 50 км)", "medium": "Середня дистанція (60-100 км)", "long": "Гран Фондо / Бревет (100+ км)"}
    tier_labels = {"economy": "Економ (до 2 300 грн)", "standard": "Оптимальний (до 2 600–3 000 грн)", "premium": "PRO / Еліта (від 3 500+ грн)"}

    return {
        "sport": "cycling",
        "sport_label": "Велоспорт",
        "distance_label": dist_labels.get(distance_fmt, "Велозаїзд"),
        "box_title": f"Стартовий велобокс: {dist_labels.get(distance_fmt, 'Велозаїзд')}",
        "total_base_price": round(total_price, 2),
        "slots": slots,
        "budget_info": {
            "type": "custom" if custom_budget else "preset",
            "price_tier": price_tier,
            "tier_label": tier_labels.get(price_tier, price_tier),
            "custom_budget": custom_budget,
            "within_budget": total_price <= custom_budget if custom_budget else True,
            "savings": round(custom_budget - total_price, 2) if custom_budget and total_price <= custom_budget else 0.0
        }
    }


def generate_triathlon_box(inputs: Dict[str, Any], catalog: List[Dict[str, Any]]) -> Dict[str, Any]:
    fmt = inputs.get("format", "half")  # sprint, half, full, swim
    price_tier = inputs.get("price_tier", "standard")
    caffeine_pref = inputs.get("caffeine_preference", "boost")
    wetsuit_care = inputs.get("wetsuit_care", True)

    custom_budget = None
    raw_b = inputs.get("custom_budget") or inputs.get("max_budget")
    if raw_b:
        try:
            custom_budget = float(raw_b)
        except (ValueError, TypeError):
            custom_budget = None

    if custom_budget and not inputs.get("price_tier_explicit"):
        price_tier = "economy" if custom_budget < 3000 else ("standard" if custom_budget <= 6500 else "premium")

    available = [p for p in catalog if p.get("quantity", 0) > 0]
    if caffeine_pref == "none":
        available = [p for p in available if not p.get("caffeine", False)]

    slots = {"energy": [], "hydration": [], "gear": [], "care_recovery": []}
    used_ids = set()

    # --- 1. ENERGY SLOT ---
    # 1A. Primary Non-Caff Hydrogel
    reg_candidates = [p for p in available if p.get("slot") == "energy" and p.get("sub_type") in ["hydrogel", "gel"] and not p.get("caffeine", False)]
    if not reg_candidates:
        reg_candidates = [p for p in available if p.get("slot") == "energy" and p.get("sub_type") in ["hydrogel", "gel"]]
    reg_candidates.sort(key=lambda p: (-score_item(p, price_tier, ["pf 30", "pf 90", "maurten", "beta fuel"]), p.get("price", 0)))

    primary_gel = reg_candidates[0] if reg_candidates else None
    if primary_gel:
        used_ids.add(primary_gel["product_id"])
        if fmt in ["sprint", "swim"]:
            qty = 2 if caffeine_pref == "boost" else 3
        elif fmt == "half":
            qty = 5 if caffeine_pref == "boost" else 7
        elif fmt == "full":
            qty = 8 if caffeine_pref == "boost" else 11
        else:
            qty = 2

        if primary_gel["product_id"] == 2025:
            qty = max(1, qty // 3)

        timing_map = {
            "sprint": "1 гель у T1 на виході з води + 1 гель на велоетапі",
            "swim": "1 гель за 15 хв до старту запливу + 1 гель одразу після фінішу",
            "half": "1 гель у T1, далі по 1 гелю кожні 40 хв на 90 км велоетапі та першій половині бігу",
            "full": "Базове вуглеводне живлення: 1 гель кожні 35-40 хв на 180 км вело та марафоні"
        }
        slots["energy"].append({
            "product": primary_gel,
            "quantity_recommended": qty,
            "timing_instruction": timing_map.get(fmt, "Вживати на дистанції кожні 40 хвилин"),
            "checked_by_default": True,
            "reason_badge": "Базовий гідрогель високої плинності (не подразнює ШКТ)",
            "alternatives": reg_candidates[1:6]
        })

    # 1B. Caffeine Boost Gel
    if caffeine_pref == "boost":
        caff_candidates = [p for p in available if p.get("slot") == "energy" and p.get("sub_type") in ["hydrogel", "gel"] and p.get("caffeine", True) and p.get("product_id") not in used_ids]
        caff_candidates.sort(key=lambda p: (-score_item(p, price_tier, ["pf 30", "226ers", "gu"]), p.get("price", 0)))
        caff_gel = caff_candidates[0] if caff_candidates else None
        if caff_gel:
            used_ids.add(caff_gel["product_id"])
            c_qty = 1 if fmt in ["sprint", "swim"] else 2
            caff_timing_map = {
                "sprint": "У транзитній зоні T2 перед вибіганням на 5 км для темпового фінішу",
                "swim": "За 20 хв до старту для максимальної концентрації та реакції у воді",
                "half": "1 гель на 70-му км вело + 1 гель на 12-му км бігу для фінішного прискорення",
                "full": "2 гелі на марафонському етапі (на 21 км та 32 км) для подолання ментальної втоми"
            }
            slots["energy"].append({
                "product": caff_gel,
                "quantity_recommended": c_qty,
                "timing_instruction": caff_timing_map.get(fmt, "Перед фінішним сегментом"),
                "checked_by_default": True,
                "reason_badge": "Кофеїновий буст для ЦНС та фінішного ривка",
                "alternatives": caff_candidates[1:6]
            })

    # 1C. Transition Chews (for 70.3 and 140.6)
    if fmt in ["half", "full"]:
        chew_candidates = [p for p in available if p.get("slot") == "energy" and p.get("sub_type") in ["chew", "transition_chew"] and p.get("product_id") not in used_ids]
        chew_candidates.sort(key=lambda p: (-score_item(p, price_tier, ["pf 30", "chew"]), p.get("price", 0)))
        chew_item = chew_candidates[0] if chew_candidates else None
        if chew_item:
            used_ids.add(chew_item["product_id"])
            slots["energy"].append({
                "product": chew_item,
                "quantity_recommended": 2,
                "timing_instruction": "Вживати по 1 цукерці кожні 20 хв на рівнинних ділянках велоетапу для різноманітності текстури",
                "checked_by_default": True,
                "reason_badge": "Жувальні цукерки для велоетапу (зручно в аеробарі)",
                "alternatives": chew_candidates[1:6]
            })

    # 1D. High-Carb Drink Mix for 180km Bike Leg (Full Ironman 140.6 only)
    if fmt == "full":
        drink_candidates = [p for p in available if p.get("slot") == "energy" and p.get("sub_type") == "drink_mix" and p.get("product_id") not in used_ids]
        drink_candidates.sort(key=lambda p: (-score_item(p, price_tier, ["beta fuel", "maurten", "pf 60"]), p.get("price", 0)))
        drink_item = drink_candidates[0] if drink_candidates else None
        if drink_item:
            used_ids.add(drink_item["product_id"])
            d_qty = 1 if drink_item.get("price", 0) > 1000 else 2
            slots["energy"].append({
                "product": drink_item,
                "quantity_recommended": d_qty,
                "timing_instruction": "Розчинити в аерофлязі на велоетапі (забезпечує 80-90 г вуглеводів на годину)",
                "checked_by_default": True,
                "reason_badge": "Високовуглеводне рідке паливо для 180 км велоетапу",
                "alternatives": drink_candidates[1:6]
            })

    # --- 2. HYDRATION SLOT ---
    salt_item, salt_alts = pick_with_alts(available, "hydration", price_tier, sub_type="salt_caps", exclude_ids=used_ids, priority_keywords=["electrolyte", "capsule", "salt"])
    if salt_item:
        used_ids.add(salt_item["product_id"])
        salt_timing_map = {
            "sprint": "1 капсула за 15 хв до входу у воду для захисту від судом у холодній воді",
            "swim": "1-2 капсули перед стартом запливу",
            "half": "1 капсула перед запливом + 1 капсула кожні 45-60 хв на велоетапі та на бігу",
            "full": "1 капсула перед запливом + по 1 капсулі щогодини протягом усього дня (10-15 год)"
        }
        slots["hydration"].append({
            "product": salt_item,
            "quantity_recommended": 1,
            "timing_instruction": salt_timing_map.get(fmt, "1 капсула на годину"),
            "checked_by_default": True,
            "reason_badge": "Електроліти проти судом литок у воді та на вело",
            "alternatives": salt_alts
        })

    iso_item, iso_alts = pick_with_alts(available, "hydration", price_tier, exclude_ids=used_ids, priority_keywords=["ph 1000", "ph 1500", "tube", "isotonic", "zero drinx"])
    if iso_item and not any(it["product"]["product_id"] == iso_item["product_id"] for it in slots["hydration"]):
        used_ids.add(iso_item["product_id"])
        iso_qty = 2 if fmt == "full" else 1
        slots["hydration"].append({
            "product": iso_item,
            "quantity_recommended": iso_qty,
            "timing_instruction": "Розчиняти у флягах (1 таб на 500 мл) для регулярної гідратації на вело та в T2",
            "checked_by_default": True,
            "reason_badge": "Гіпотонік / ізотонік високої осмолярності",
            "alternatives": iso_alts
        })

    # --- 3. GEAR SLOT ---
    gear_item, gear_alts = pick_with_alts(available, "gear", price_tier, exclude_ids=used_ids)
    if gear_item:
        used_ids.add(gear_item["product_id"])
        slots["gear"].append({
            "product": gear_item,
            "quantity_recommended": 1,
            "timing_instruction": "Одягти у транзитці T1; повертати номер на спину на вело, на груди — на бігу",
            "checked_by_default": True,
            "reason_badge": "Стартовий пояс для номера та гелів (вимога правил триатлону)",
            "alternatives": gear_alts
        })

    if fmt == "full":
        flask_item, flask_alts = pick_with_alts(available, "gear", price_tier, sub_type="flasks", exclude_ids=used_ids)
        if flask_item:
            used_ids.add(flask_item["product_id"])
            slots["gear"].append({
                "product": flask_item,
                "quantity_recommended": 1,
                "timing_instruction": "Для заправки рідких гелів та розчинених електролітів на 42.2 км марафон",
                "checked_by_default": True,
                "reason_badge": "М'яка фляга на марафонський сегмент",
                "alternatives": flask_alts
            })

    # --- 4. CARE & RECOVERY SLOT ---
    if wetsuit_care:
        triswim, triswim_alts = pick_with_alts(available, "care_recovery", price_tier, sub_type="anti_chlorine", exclude_ids=used_ids, priority_keywords=["triswim"])
        if not triswim:
            triswim, triswim_alts = pick_with_alts(available, "care_recovery", price_tier, exclude_ids=used_ids, priority_keywords=["triswim"])
        if triswim:
            used_ids.add(triswim["product_id"])
            slots["care_recovery"].append({
                "product": triswim,
                "quantity_recommended": 1,
                "timing_instruction": "Змити сіль та хлор після плавального етапу (захищає шкіру та вимиває запах)",
                "checked_by_default": True,
                "reason_badge": "TRISWIM: дехлорація та захист шкіри після відкритої води",
                "alternatives": triswim_alts
            })

    if fmt in ["half", "full"]:
        chafe_item, chafe_alts = pick_with_alts(available, "care_recovery", price_tier, sub_type="anti_chafe_cream", exclude_ids=used_ids)
        if not chafe_item:
            chafe_item, chafe_alts = pick_with_alts(available, "care_recovery", price_tier, sub_type="anti_chafe", exclude_ids=used_ids)
        if chafe_item:
            used_ids.add(chafe_item["product_id"])
            slots["care_recovery"].append({
                "product": chafe_item,
                "quantity_recommended": 1,
                "timing_instruction": "Нанести на комір гідрокостюма від натирання шиї та на велопамперс перед виїздом на 90-180 км",
                "checked_by_default": True,
                "reason_badge": "Захист від натирання сідлом та коміром гідрокостюма",
                "alternatives": chafe_alts
            })

    rec_shake, rec_alts = pick_with_alts(available, "care_recovery", price_tier, exclude_ids=used_ids, priority_keywords=["recovery", "shake", "regener"])
    if rec_shake and not any(it["product"]["product_id"] == rec_shake["product_id"] for it in slots["care_recovery"]):
        used_ids.add(rec_shake["product_id"])
        slots["care_recovery"].append({
            "product": rec_shake,
            "quantity_recommended": 1,
            "timing_instruction": "Випити протягом 30 хвилин після фінішу для негайного запуску відновлення м'язів",
            "checked_by_default": True,
            "reason_badge": "Повне м'язове відновлення після мультинавантаження",
            "alternatives": rec_alts
        })

    total_price = sum(it["product"]["price"] * it["quantity_recommended"] for s in slots.values() for it in s)
    if custom_budget:
        total_price = optimize_box_for_budget(slots, custom_budget, total_price, available)

    fmt_labels = {"sprint": "Спринт / Олімпійка", "half": "Half-Ironman 70.3", "full": "Full Ironman 140.6", "swim": "Заплив на відкритій воді"}
    tier_labels = {"economy": "Економ (до 2 500–3 500 грн)", "standard": "Оптимальний (до 3 000–6 000 грн)", "premium": "PRO / Maurten (від 8 000+ грн)"}

    return {
        "sport": "triathlon",
        "sport_label": "Триатлон та плавання",
        "distance_label": fmt_labels.get(fmt, "Триатлон"),
        "box_title": f"Стартовий бокс триатлета: {fmt_labels.get(fmt, 'Триатлон')}",
        "total_base_price": round(total_price, 2),
        "slots": slots,
        "budget_info": {
            "type": "custom" if custom_budget else "preset",
            "price_tier": price_tier,
            "tier_label": tier_labels.get(price_tier, price_tier),
            "custom_budget": custom_budget,
            "within_budget": total_price <= custom_budget if custom_budget else True,
            "savings": round(custom_budget - total_price, 2) if custom_budget and total_price <= custom_budget else 0.0
        }
    }


def generate_gym_box(inputs: Dict[str, Any], catalog: List[Dict[str, Any]]) -> Dict[str, Any]:
    goal = inputs.get("goal", "mass")  # mass, lean, tone, strength
    price_tier = inputs.get("price_tier", "standard")
    pre_boost = inputs.get("pre_workout_boost", "caffeine")  # caffeine, beta_alanine, none

    custom_budget = None
    raw_b = inputs.get("custom_budget") or inputs.get("max_budget")
    if raw_b:
        try:
            custom_budget = float(raw_b)
        except (ValueError, TypeError):
            custom_budget = None

    if custom_budget and not inputs.get("price_tier_explicit"):
        price_tier = "economy" if custom_budget < 3800 else ("standard" if custom_budget <= 5500 else "premium")

    available = [p for p in catalog if p.get("quantity", 0) > 0]
    if pre_boost in ["none", "beta_alanine"]:
        available = [p for p in available if not p.get("caffeine", False)]

    slots = {"energy": [], "hydration": [], "gear": [], "care_recovery": []}
    used_ids = set()

    # Slot 1: Energy & Activation (Pre-workout powder, beta-alanine, shots x6, or protein snacks/bars x6)
    if pre_boost == "caffeine":
        pre_item, pre_alts = pick_with_alts(
            available, "energy", price_tier, exclude_ids=used_ids,
            need_caffeine=True,
            allowed_sub_types=["pre_workout", "energy_shot"],
            priority_keywords=["передтренув", "pre-workout", "scatterbrain", "shot"]
        )
        if not pre_item:
            pre_item, pre_alts = pick_with_alts(
                available, "energy", price_tier, exclude_ids=used_ids,
                allowed_sub_types=["pre_workout", "energy_shot", "protein_bar", "protein_snack"],
                priority_keywords=["передтренув", "pre-workout", "scatterbrain", "shot", "fitly", "bar", "cookie"]
            )
    elif pre_boost == "beta_alanine":
        pre_item, pre_alts = pick_with_alts(
            available, "energy", price_tier, exclude_ids=used_ids,
            allowed_sub_types=["beta_alanine", "pre_workout"],
            priority_keywords=["аланін", "alanine", "gold beta", "levrone"]
        )
        if not pre_item:
            snack_avail = [p for p in available if "пудинг" not in p.get("name", "").lower()]
            pre_item, pre_alts = pick_with_alts(
                snack_avail, "energy", price_tier, exclude_ids=used_ids,
                allowed_sub_types=["protein_bar", "protein_snack"],
                priority_keywords=["fitly", "cookie", "батончик", "мус", "mousse", "печиво"]
            )
    else:
        snack_avail = [p for p in available if "пудинг" not in p.get("name", "").lower()]
        pre_item, pre_alts = pick_with_alts(
            snack_avail, "energy", price_tier, exclude_ids=used_ids,
            allowed_sub_types=["protein_bar", "protein_snack"],
            priority_keywords=["fitly", "cookie", "батончик", "мус", "mousse", "печиво"]
        )

    if pre_item:
        used_ids.add(pre_item["product_id"])
        st = pre_item.get("sub_type", "")
        name_l = pre_item.get("name", "").lower()

        # Realistic pack quantities for 1-month gym course (12-16 workouts)
        if st == "beta_alanine" or "аланін" in name_l or "alanine" in name_l:
            qty = 1
            timing = "1 мірна порція (або капсули) за 20-30 хв до тренування для витривалості та буферизації молочної кислоти без стимуляції ЦНС"
            badge = "Бета-аланін без стимуляторів (передтренувальний комплекс)"
        elif st == "energy_shot" or "шот" in name_l:
            qty = 6
            timing = "1 шот за 20-30 хвилин до важких тренувань для фокусу та пампінгу (курс 6 шт на місяць)"
            badge = "Енергетичні шоти (набір 6 шт)"
        elif st == "protein_bar" or "батончик" in name_l:
            qty = 6
            timing = "Зручний білковий перекус після тренування або між прийомами їжі (набір 6 шт)"
            badge = "Протеїнові батончики (набір 6 шт)"
        elif "мус" in name_l or "mousse" in name_l:
            qty = 4
            timing = "Високобілковий десерт без цукру після залу (набір 4 шт)"
            badge = "Протеїновий десерт (набір 4 шт)"
        elif "cookie" in name_l or "печиво" in name_l:
            qty = 6
            timing = "Поживний білковий перекус (38 г білка) для закриття анаболічного вікна (набір 6 шт)"
            badge = "Протеїнове печиво (набір 6 шт)"
        else:
            qty = 1
            timing = "Прийняти за 25-30 хвилин до силового тренування для вибухової сили та пампінгу"
            badge = "Передтренувальний комплекс"

        slots["energy"].append({
            "product": pre_item,
            "quantity_recommended": qty,
            "timing_instruction": timing,
            "checked_by_default": True,
            "reason_badge": badge,
            "alternatives": pre_alts
        })

    # Slot 2: Hydration & Intra-Workout (BCAA strictly prioritized for gym muscle recovery)
    bcaa_item, bcaa_alts = pick_with_alts(
        available, "hydration", price_tier, exclude_ids=used_ids,
        allowed_sub_types=["bcaa"],
        priority_keywords=["bcaa", "recovery", "амінокислот"]
    )
    if not bcaa_item:
        bcaa_item, bcaa_alts = pick_with_alts(
            available, "hydration", price_tier, exclude_ids=used_ids,
            allowed_sub_types=["isotonic"],
            priority_keywords=["електроліт"]
        )
    if bcaa_item:
        used_ids.add(bcaa_item["product_id"])
        slots["hydration"].append({
            "product": bcaa_item,
            "quantity_recommended": 1,
            "timing_instruction": "Розчинити 1 мірну порцію у воді та пити під час тренування між підходами для захисту м'язів від катаболізму",
            "checked_by_default": True,
            "reason_badge": "Амінокислотна підтримка BCAA під час навантажень",
            "alternatives": bcaa_alts
        })

    # Slot 3: Gear (Fitness Shaker strictly prioritized over squeeze water bottles)
    shaker_item, shaker_alts = pick_with_alts(
        available, "gear", price_tier, exclude_ids=used_ids,
        allowed_sub_types=["shaker"],
        priority_keywords=["шейкер", "shaker"]
    )
    if shaker_item:
        used_ids.add(shaker_item["product_id"])
        slots["gear"].append({
            "product": shaker_item,
            "quantity_recommended": 1,
            "timing_instruction": "Зручний шейкер 600 мл з сіткою для швидкого змішування протеїнових шейків та BCAA без грудочок",
            "checked_by_default": True,
            "reason_badge": "Спортивний шейкер для залу",
            "alternatives": shaker_alts
        })

    # Slot 4: Care & Recovery (Differentiated by Goal: Mass vs Strength vs Lean/Cut/Tone)
    if goal == "mass":
        # Item 1: Core 100% Whey Protein (Hypertrophy & Recovery)
        whey_item, whey_alts = pick_with_alts(
            available, "care_recovery", price_tier, exclude_ids=used_ids,
            allowed_sub_types=["whey_protein", "vegan_protein"],
            priority_keywords=["gold standard", "whey protein", "compact whey", "scitec", "протеїн"]
        )
        if whey_item:
            used_ids.add(whey_item["product_id"])
            name_l = whey_item.get("name", "").lower()
            qty = 2 if ("500 г" in name_l or "500г" in name_l) and price_tier in ["standard", "premium"] else 1
            slots["care_recovery"].append({
                "product": whey_item,
                "quantity_recommended": qty,
                "timing_instruction": "1 мірна порція відразу після тренування для максимального синтезу м'язового білка",
                "checked_by_default": True,
                "reason_badge": "Преміальний сироватковий протеїн для росту м'язів",
                "alternatives": whey_alts
            })

        # Item 2: Creatine Monohydrate (Strength & ATP Regeneration)
        creatine_item, creat_alts = pick_with_alts(
            available, "care_recovery", price_tier, sub_type="creatine", exclude_ids=used_ids,
            allowed_sub_types=["creatine"],
            priority_keywords=["creatine", "креатин"]
        )
        if creatine_item and not any(it["product"]["product_id"] == creatine_item["product_id"] for it in slots["care_recovery"]):
            used_ids.add(creatine_item["product_id"])
            slots["care_recovery"].append({
                "product": creatine_item,
                "quantity_recommended": 1,
                "timing_instruction": "5 г щодня (вранці або після тренування з водою/соком) для росту силових показників та накопичення креатинфосфату",
                "checked_by_default": True,
                "reason_badge": "Креатин моногідрат для вибухової сили",
                "alternatives": creat_alts
            })

        # Item 3: Hormone Support & Night Anabolic Recovery (ZMA / Vitamin D3 / Tribulus)
        hormone_item, horm_alts = pick_with_alts(
            available, "care_recovery", price_tier, exclude_ids=used_ids,
            allowed_sub_types=["zma", "vitamins", "testosterone_booster"],
            priority_keywords=["zmd", "zma", "d-3", "d3", "tribulus", "трибулус"]
        )
        if hormone_item and not any(it["product"]["product_id"] == hormone_item["product_id"] for it in slots["care_recovery"]):
            used_ids.add(hormone_item["product_id"])
            slots["care_recovery"].append({
                "product": hormone_item,
                "quantity_recommended": 1,
                "timing_instruction": "Приймати за 30-40 хвилин до сну для глибокої регенерації ЦНС та нормалізації тестостерону",
                "checked_by_default": True,
                "reason_badge": "Нічне відновлення та гормональний баланс (ZMA / D3)",
                "alternatives": horm_alts
            })

    elif goal == "strength":
        # Strength: Whey Protein / Isolate + Creatine Monohydrate + Strength Support (Glutamine / ZMA / Vitamins)
        whey_item, whey_alts = pick_with_alts(
            available, "care_recovery", price_tier, exclude_ids=used_ids,
            allowed_sub_types=["whey_protein", "whey_isolate"],
            priority_keywords=["gold standard", "whey protein", "compact whey", "scitec", "isolate", "ізолят", "протеїн"]
        )
        if whey_item:
            used_ids.add(whey_item["product_id"])
            slots["care_recovery"].append({
                "product": whey_item,
                "quantity_recommended": 1,
                "timing_instruction": "1 мірна порція після силового тренування для швидкої регенерації мікророзривів м'язів",
                "checked_by_default": True,
                "reason_badge": "Сироватковий протеїн для сили та відновлення",
                "alternatives": whey_alts
            })

        creatine_item, creat_alts = pick_with_alts(
            available, "care_recovery", price_tier, sub_type="creatine", exclude_ids=used_ids,
            allowed_sub_types=["creatine"],
            priority_keywords=["creatine", "креатин"]
        )
        if creatine_item and not any(it["product"]["product_id"] == creatine_item["product_id"] for it in slots["care_recovery"]):
            used_ids.add(creatine_item["product_id"])
            slots["care_recovery"].append({
                "product": creatine_item,
                "quantity_recommended": 1,
                "timing_instruction": "5 г щодня для ресинтезу АТФ, вибухової сили та росту робочих ваг у базових вправах",
                "checked_by_default": True,
                "reason_badge": "Креатин моногідрат для максимальної сили",
                "alternatives": creat_alts
            })

        strength_supp, supp_alts = pick_with_alts(
            available, "care_recovery", price_tier, exclude_ids=used_ids,
            allowed_sub_types=["glutamine", "zma", "vitamins"],
            priority_keywords=["глютамін", "glutamine", "zma", "zmd", "d-3", "d3"]
        )
        if strength_supp and not any(it["product"]["product_id"] == strength_supp["product_id"] for it in slots["care_recovery"]):
            used_ids.add(strength_supp["product_id"])
            slots["care_recovery"].append({
                "product": strength_supp,
                "quantity_recommended": 1,
                "timing_instruction": "Приймати після навантажень або перед сном для підтримки зв'язок, імунітету та відновлення ЦНС",
                "checked_by_default": True,
                "reason_badge": "Підтримка витривалості та відновлення ЦНС (глютамін/ZMA)",
                "alternatives": supp_alts
            })

    else:
        # Domain 8: Lean, Tone & Fat Loss
        # Item 1: High Protein / Low-Carb (Diet Whey or Whey Isolate 94)
        diet_item, diet_alts = pick_with_alts(
            available, "care_recovery", price_tier, exclude_ids=used_ids,
            allowed_sub_types=["diet_whey", "whey_isolate", "whey_protein"],
            priority_keywords=["diet whey", "ізолят", "isolate", "compact whey", "протеїн"]
        )
        if diet_item:
            used_ids.add(diet_item["product_id"])
            slots["care_recovery"].append({
                "product": diet_item,
                "quantity_recommended": 1,
                "timing_instruction": "1 мірна ложка після тренування або замість перекусу для збереження сухих м'язів без зайвих калорій",
                "checked_by_default": True,
                "reason_badge": "Чистий ізолят / Diet Whey з мінімальною калорійністю",
                "alternatives": diet_alts
            })

        # Item 2: Fat Metabolism & Lipolysis (L-Carnitine / CLA / Fat Burner)
        fatburn_item, fatburn_alts = pick_with_alts(
            available, "care_recovery", price_tier, exclude_ids=used_ids,
            allowed_sub_types=["l_carnitine", "cla", "fat_burner"],
            priority_keywords=["carnitine", "карнітин", "cla", "thermo", "жироспалювач"]
        )
        if fatburn_item and not any(it["product"]["product_id"] == fatburn_item["product_id"] for it in slots["care_recovery"]):
            used_ids.add(fatburn_item["product_id"])
            slots["care_recovery"].append({
                "product": fatburn_item,
                "quantity_recommended": 1,
                "timing_instruction": "Приймати за 30 хвилин до кардіо або тренування для транспортування жирних кислот у мітохондрії",
                "checked_by_default": True,
                "reason_badge": "Активатор спалювання жиру (L-Carnitine / CLA)",
                "alternatives": fatburn_alts
            })

        # Item 3: Anti-catabolic muscle defense (Glutamine / Casein)
        rec_item, rec_alts = pick_with_alts(
            available, "care_recovery", price_tier, exclude_ids=used_ids,
            allowed_sub_types=["glutamine", "casein_protein", "vitamins"],
            priority_keywords=["глютамін", "glutamine", "casein", "казеїн"]
        )
        if rec_item and not any(it["product"]["product_id"] == rec_item["product_id"] for it in slots["care_recovery"]):
            used_ids.add(rec_item["product_id"])
            slots["care_recovery"].append({
                "product": rec_item,
                "quantity_recommended": 1,
                "timing_instruction": "Після тренування або перед сном для захисту м'язів від руйнування в умовах дефіциту калорій",
                "checked_by_default": True,
                "reason_badge": "Антикатаболічний захист м'язів при дефіциті калорій",
                "alternatives": rec_alts
            })

    total_price = sum(it["product"]["price"] * it["quantity_recommended"] for s in slots.values() for it in s)
    if custom_budget:
        total_price = optimize_box_for_budget(slots, custom_budget, total_price, available)

    goal_labels = {
        "mass": "Набір м'язової маси та сили (1-місячний курс)",
        "lean": "Рельєф, сушка та спалювання жиру (1-місячний курс)",
        "tone": "Тонус та функціональне здоров'я (1-місячний курс)",
        "strength": "Сила та витривалість (1-місячний курс)"
    }
    tier_labels = {"economy": "Економ (до 2 800 грн)", "standard": "Оптимальний (до 4 500 грн)", "premium": "PRO / Преміум (від 6 500+ грн)"}

    return {
        "sport": "gym",
        "sport_label": "Тренажерний зал та фітнес",
        "distance_label": goal_labels.get(goal, "Фітнес тренування"),
        "box_title": f"Фітнес-бокс: {goal_labels.get(goal, 'Фітнес тренування')}",
        "total_base_price": round(total_price, 2),
        "slots": slots,
        "budget_info": {
            "type": "custom" if custom_budget else "preset",
            "price_tier": price_tier,
            "tier_label": tier_labels.get(price_tier, price_tier),
            "custom_budget": custom_budget,
            "within_budget": total_price <= custom_budget if custom_budget else True,
            "savings": round(custom_budget - total_price, 2) if custom_budget and total_price <= custom_budget else 0.0
        }
    }


def generate_outdoor_box(inputs: Dict[str, Any], catalog: List[Dict[str, Any]]) -> Dict[str, Any]:
    duration = inputs.get("duration", "weekend")  # 1day, weekend, expedition
    price_tier = inputs.get("price_tier", "standard")
    dietary = inputs.get("dietary") or inputs.get("diet") or inputs.get("dietary_preference") or inputs.get("stomach_type") or "standard"
    is_vegan = str(dietary).lower() in ["vegan", "vegetarian", "plant_based"]

    weather = inputs.get("weather") or inputs.get("season") or "moderate"
    is_cold = str(weather).lower() in ["cold", "winter", "alpine"]
    is_warm = str(weather).lower() in ["warm", "summer", "hot"]

    custom_budget = None
    raw_b = inputs.get("custom_budget") or inputs.get("max_budget")
    if raw_b:
        try:
            custom_budget = float(raw_b)
        except (ValueError, TypeError):
            custom_budget = None

    if custom_budget and not inputs.get("price_tier_explicit"):
        price_tier = "economy" if custom_budget < 4200 else ("standard" if custom_budget <= 6500 else "premium")

    available = [p for p in catalog if p.get("quantity", 0) > 0]
    meat_keywords = ["індич", "ялович", "куряч", "джерки", "креветк", "по-флотськи"]
    if is_vegan:
        available = [p for p in available if not (p.get("sub_type") == "jerky" or any(k in p.get("name", "").lower() for k in meat_keywords))]

    slots = {"energy": [], "hydration": [], "gear": [], "care_recovery": []}
    used_ids = set()

    # --- SLOT 1: ENERGY (ЇDLO breakfasts, hot lunches, gourmet dinners, trail snacks) ---
    if duration == "1day":
        # Day hike: 1 hot meal + 1 trail snack
        meal, meal_alts = pick_with_alts(available, "energy", price_tier, sub_type="gourmet_meal", exclude_ids=used_ids)
        if meal:
            used_ids.add(meal["product_id"])
            slots["energy"].append({
                "product": meal,
                "quantity_recommended": 1,
                "timing_instruction": "Гарячий поживний обід на денному привалі (залити окропом у пакеті на 8-10 хв)",
                "checked_by_default": True,
                "reason_badge": "Гаряча основна страва ЇDLO" if not is_vegan else "Веганська гаряча страва ЇDLO",
                "alternatives": meal_alts
            })
        snack, snack_alts = pick_with_alts(available, "energy", price_tier, sub_type="energy_snack", exclude_ids=used_ids)
        if not snack:
            snack, snack_alts = pick_with_alts(available, "energy", price_tier, sub_type="energy_bar", exclude_ids=used_ids)
        if snack:
            used_ids.add(snack["product_id"])
            slots["energy"].append({
                "product": snack,
                "quantity_recommended": 1,
                "timing_instruction": "Швидкий енергетичний перекус на підйомі",
                "checked_by_default": True,
                "reason_badge": "Енергетичний перекус на маршруті",
                "alternatives": snack_alts
            })
    elif duration == "weekend":
        # Domain 9: Weekend Hike (2-3 Days, camping)
        # 2 breakfasts, 4-5 main hot meals (2 soups + 2-3 gourmet meals), 1-2 trail snacks
        bfast_kw = ["гранола", "вівсянка"] if not is_cold else ["гранола", "вівсянка", "гаряча"]
        bfast, bfast_alts = pick_with_alts(available, "energy", price_tier, sub_type="breakfast_meal", exclude_ids=used_ids, priority_keywords=bfast_kw)
        if bfast:
            used_ids.add(bfast["product_id"])
            slots["energy"].append({
                "product": bfast,
                "quantity_recommended": 2,
                "timing_instruction": "Калорійний сніданок у наметі (дні 2 та 3): залити окропом на 8-10 хв перед виходом на перевал",
                "checked_by_default": True,
                "reason_badge": "Сублімований сніданок ЇDLO (2 дні)" if not is_vegan else "Рослинний сніданок ЇDLO (2 дні)",
                "alternatives": bfast_alts
            })

        soup_kw = ["борщ", "суп"] if not is_cold else ["борщ", "суп", "грибами"]
        soup, soup_alts = pick_with_alts(available, "energy", price_tier, sub_type="gourmet_soup", exclude_ids=used_ids, priority_keywords=soup_kw)
        if soup:
            used_ids.add(soup["product_id"])
            slots["energy"].append({
                "product": soup,
                "quantity_recommended": 2,
                "timing_instruction": "Зігріваючий суп/борщ на обідні привали під час переходів (2 порції)",
                "checked_by_default": True,
                "reason_badge": "Гарячий обід ЇDLO (2 супи)" if not is_vegan else "Вегетаріанський крем-суп ЇDLO (2 супи)",
                "alternatives": soup_alts
            })

        meal_kw = ["картопля", "макспро", "макарони", "гречка"] if not is_vegan else ["гречка", "кус-кус", "бануш"]
        meal, meal_alts = pick_with_alts(available, "energy", price_tier, sub_type="gourmet_meal", exclude_ids=used_ids, priority_keywords=meal_kw)
        if meal:
            used_ids.add(meal["product_id"])
            m_qty = 3 if price_tier != "economy" else 2
            slots["energy"].append({
                "product": meal,
                "quantity_recommended": m_qty,
                "timing_instruction": "Ситні вечірні гарячі вечері в таборі для відновлення витрачених калорій",
                "checked_by_default": True,
                "reason_badge": f"Калорійна вечеря ЇDLO ({m_qty} порції)" if not is_vegan else f"Веганська ситна вечеря ЇDLO ({m_qty} порції)",
                "alternatives": meal_alts
            })

        snack, snack_alts = pick_with_alts(available, "energy", price_tier, sub_type="energy_snack", exclude_ids=used_ids)
        if not snack:
            snack, snack_alts = pick_with_alts(available, "energy", price_tier, sub_type="energy_bar", exclude_ids=used_ids)
        if snack:
            used_ids.add(snack["product_id"])
            slots["energy"].append({
                "product": snack,
                "quantity_recommended": 1,
                "timing_instruction": "Горіхово-фруктовий перекус між основними переходами",
                "checked_by_default": True,
                "reason_badge": "Натуральні горіхи та сухофрукти ЇDLO",
                "alternatives": snack_alts
            })
    else:
        # Domain 10: Multi-Day Mountain Expedition (4+ Days autonomous)
        # Minimum 8-12 hot meals: 4 breakfasts (2 types), 4 hot soups (lunches), 4 gourmet meals (dinners), 2 energy snacks
        bfast1, bfast1_alts = pick_with_alts(available, "energy", price_tier, sub_type="breakfast_meal", exclude_ids=used_ids, priority_keywords=["гранола"])
        if bfast1:
            used_ids.add(bfast1["product_id"])
            slots["energy"].append({
                "product": bfast1,
                "quantity_recommended": 2,
                "timing_instruction": "Експедиційний сніданок: поживна гранола/вівсянка (ранок 1-2)",
                "checked_by_default": True,
                "reason_badge": "Сніданок ЇDLO (2 порції)",
                "alternatives": bfast1_alts
            })

        bfast2, bfast2_alts = pick_with_alts(available, "energy", price_tier, sub_type="breakfast_meal", exclude_ids=used_ids, priority_keywords=["вівсянка", "кукурудзяна"])
        if not bfast2 and bfast1:
            bfast2, bfast2_alts = bfast1, bfast1_alts
        if bfast2:
            used_ids.add(bfast2["product_id"])
            slots["energy"].append({
                "product": bfast2,
                "quantity_recommended": 2,
                "timing_instruction": "Експедиційний сніданок: інший смак для різноманітності (ранок 3-4)",
                "checked_by_default": True,
                "reason_badge": "Сніданок ЇDLO — різноманітність (2 порції)",
                "alternatives": bfast2_alts
            })

        soup1, soup1_alts = pick_with_alts(available, "energy", price_tier, sub_type="gourmet_soup", exclude_ids=used_ids, priority_keywords=["борщ"] if not is_vegan else ["грибами"])
        if soup1:
            used_ids.add(soup1["product_id"])
            slots["energy"].append({
                "product": soup1,
                "quantity_recommended": 2,
                "timing_instruction": "Гарячий рідкий обід на перевалі: відновлення водно-сольового балансу (2 обіди)",
                "checked_by_default": True,
                "reason_badge": "Гарячий суп/борщ ЇDLO (2 обіди)",
                "alternatives": soup1_alts
            })

        soup2, soup2_alts = pick_with_alts(available, "energy", price_tier, sub_type="gourmet_soup", exclude_ids=used_ids, priority_keywords=["суп", "грибами"])
        if not soup2 and soup1:
            soup2, soup2_alts = soup1, soup1_alts
        if soup2:
            used_ids.add(soup2["product_id"])
            slots["energy"].append({
                "product": soup2,
                "quantity_recommended": 2,
                "timing_instruction": "Гарячий обідній суп на денному привалі (2 обіди)",
                "checked_by_default": True,
                "reason_badge": "Густий суп ЇDLO на обід (2 обіди)",
                "alternatives": soup2_alts
            })

        meal1_kw = ["картопля", "макспро"] if not is_vegan else ["гречка"]
        meal1, meal1_alts = pick_with_alts(available, "energy", price_tier, sub_type="gourmet_meal", exclude_ids=used_ids, priority_keywords=meal1_kw)
        if meal1:
            used_ids.add(meal1["product_id"])
            slots["energy"].append({
                "product": meal1,
                "quantity_recommended": 2,
                "timing_instruction": "Щільна висококалорійна гаряча вечеря в наметі після важкого ходового дня (вечори 1-2)",
                "checked_by_default": True,
                "reason_badge": "Основна гаряча вечеря ЇDLO (2 порції)",
                "alternatives": meal1_alts
            })

        meal2_kw = ["макарони", "гречка", "бануш", "кус-кус"] if not is_vegan else ["кус-кус", "бануш"]
        meal2, meal2_alts = pick_with_alts(available, "energy", price_tier, sub_type="gourmet_meal", exclude_ids=used_ids, priority_keywords=meal2_kw)
        if not meal2 and meal1:
            meal2, meal2_alts = meal1, meal1_alts
        if meal2:
            used_ids.add(meal2["product_id"])
            slots["energy"].append({
                "product": meal2,
                "quantity_recommended": 2,
                "timing_instruction": "Гаряча вечеря: альтернативна страва для повноцінного раціону (вечори 3-4)",
                "checked_by_default": True,
                "reason_badge": "Основна гаряча вечеря ЇDLO (2 порції)",
                "alternatives": meal2_alts
            })

        snack, snack_alts = pick_with_alts(available, "energy", price_tier, sub_type="energy_snack", exclude_ids=used_ids)
        if not snack:
            snack, snack_alts = pick_with_alts(available, "energy", price_tier, sub_type="energy_bar", exclude_ids=used_ids)
        if snack:
            used_ids.add(snack["product_id"])
            slots["energy"].append({
                "product": snack,
                "quantity_recommended": 2,
                "timing_instruction": "Висококалорійні горіхи з родзинками на крутих підйомах та перевалах",
                "checked_by_default": True,
                "reason_badge": "Енергетичний раціон ЇDLO (2 упаковки)",
                "alternatives": snack_alts
            })

    # --- SLOT 2: HYDRATION (Electrolyte tablets, Carpathian tea, camp drip coffee) ---
    if duration == "1day":
        drink_item, drink_alts = pick_with_alts(available, "hydration", price_tier, exclude_ids=used_ids)
        if drink_item:
            used_ids.add(drink_item["product_id"])
            slots["hydration"].append({
                "product": drink_item,
                "quantity_recommended": 1,
                "timing_instruction": "Розчиняти у воді на переході для підтримки водно-сольового балансу",
                "checked_by_default": True,
                "reason_badge": "Гідратація та мінералізація питної води",
                "alternatives": drink_alts
            })
    elif duration == "weekend":
        electro, electro_alts = pick_with_alts(available, "hydration", price_tier, sub_type="electrolyte_tablets", exclude_ids=used_ids)
        if electro:
            used_ids.add(electro["product_id"])
            slots["hydration"].append({
                "product": electro,
                "quantity_recommended": 1,
                "timing_instruction": "1 туба (10-20 таб): розчиняти по 1 таблетці на кожні 500-750 мл води на підйомах",
                "checked_by_default": True,
                "reason_badge": "Електроліти проти зневоднення на сонці та судом ніг" if is_warm else "Електроліти проти зневоднення та судом ніг",
                "alternatives": electro_alts
            })
        hot_drink, hot_alts = pick_with_alts(available, "hydration", price_tier, sub_type="hot_drink", exclude_ids=used_ids)
        if not hot_drink:
            hot_drink, hot_alts = pick_with_alts(available, "hydration", price_tier, sub_type="coffee", exclude_ids=used_ids)
        if hot_drink:
            used_ids.add(hot_drink["product_id"])
            slots["hydration"].append({
                "product": hot_drink,
                "quantity_recommended": 1 if hot_drink.get("sub_type") == "hot_drink" else 2,
                "timing_instruction": "Зігріваючий табірний напій біля вечірнього багаття чи вранці біля намету",
                "checked_by_default": True,
                "reason_badge": "Зігріваючий карпатський чай/кава ЇDLO" if is_cold else "Табірний гарячий чай/кава ЇDLO",
                "alternatives": hot_alts
            })
    else:  # expedition
        electro, electro_alts = pick_with_alts(available, "hydration", price_tier, sub_type="electrolyte_tablets", exclude_ids=used_ids)
        if electro:
            used_ids.add(electro["product_id"])
            slots["hydration"].append({
                "product": electro,
                "quantity_recommended": 1,
                "timing_instruction": "Туба електролітів на 4+ днів: обов'язкова щоденна мінералізація гірської струмкової води",
                "checked_by_default": True,
                "reason_badge": "Електролітна безпека на 4+ дні",
                "alternatives": electro_alts
            })
        tea, tea_alts = pick_with_alts(available, "hydration", price_tier, sub_type="hot_drink", exclude_ids=used_ids)
        if tea:
            used_ids.add(tea["product_id"])
            slots["hydration"].append({
                "product": tea,
                "quantity_recommended": 1,
                "timing_instruction": "Карпатський трав'яний чай (40 г): джерело вітамінів та релаксу на ночівлях",
                "checked_by_default": True,
                "reason_badge": "Карпатський чай «Чаїдло» (вечірній табір)",
                "alternatives": tea_alts
            })
        coffee, coff_alts = pick_with_alts(available, "hydration", price_tier, sub_type="coffee", exclude_ids=used_ids)
        if coffee:
            used_ids.add(coffee["product_id"])
            slots["hydration"].append({
                "product": coffee,
                "quantity_recommended": 4,
                "timing_instruction": "1 саше натуральної меленої кави на кожен ранок експедиції для бадьорого старту",
                "checked_by_default": True,
                "reason_badge": "Ранкова кава ЇDLO (4 дні експедиції)",
                "alternatives": coff_alts
            })

    # --- SLOT 3: GEAR (Trekking socks with proper sizing, soft flask, water bottle) ---
    if duration == "1day":
        socks, sock_alts = pick_with_alts(available, "gear", price_tier, sub_type="trekking_socks", exclude_ids=used_ids)
        if socks:
            used_ids.add(socks["product_id"])
            slots["gear"].append({
                "product": socks,
                "quantity_recommended": 1,
                "timing_instruction": "Одягти на маршрут для захисту стопи від натертостей та вологи",
                "checked_by_default": True,
                "reason_badge": "Трекінгові шкарпетки Race Expert",
                "alternatives": sock_alts,
                "available_sizes": [
                    {"size": "35-37", "product_id": 5597},
                    {"size": "38-40", "product_id": 5598},
                    {"size": "40-42", "product_id": 5599},
                    {"size": "43-45", "product_id": 5600}
                ]
            })
    elif duration == "weekend":
        socks, sock_alts = pick_with_alts(available, "gear", price_tier, sub_type="trekking_socks", exclude_ids=used_ids)
        if socks:
            used_ids.add(socks["product_id"])
            sock_qty = 2 if price_tier == "premium" else 1
            slots["gear"].append({
                "product": socks,
                "quantity_recommended": sock_qty,
                "timing_instruction": "Зональне ущільнення береже стопу. У поході 2-3 дні 2-га суха пара важлива для сну в наметі",
                "checked_by_default": True,
                "reason_badge": f"Термошкарпетки Race Expert ({sock_qty} пар)",
                "alternatives": sock_alts,
                "available_sizes": [
                    {"size": "35-37", "product_id": 5597},
                    {"size": "38-40", "product_id": 5598},
                    {"size": "40-42", "product_id": 5599},
                    {"size": "43-45", "product_id": 5600}
                ]
            })
        bottle, b_alts = pick_with_alts(available, "gear", price_tier, sub_type="water_bottle" if price_tier in ["economy", "standard"] else "soft_flask", exclude_ids=used_ids)
        if not bottle:
            bottle, b_alts = pick_with_alts(available, "gear", price_tier, sub_type="water_bottle", exclude_ids=used_ids)
        if bottle:
            used_ids.add(bottle["product_id"])
            slots["gear"].append({
                "product": bottle,
                "quantity_recommended": 1,
                "timing_instruction": "Зручна ємність для пиття та швидкого змішування електролітів на переходах",
                "checked_by_default": True,
                "reason_badge": "Гідратаційне спорядження",
                "alternatives": b_alts
            })
    else:  # expedition
        socks, sock_alts = pick_with_alts(available, "gear", price_tier, sub_type="trekking_socks", exclude_ids=used_ids)
        if socks:
            used_ids.add(socks["product_id"])
            slots["gear"].append({
                "product": socks,
                "quantity_recommended": 2,
                "timing_instruction": "Золоте правило гір: 1 ходова пара + 1 абсолютно суха пара в гермомішку виключно для спальника",
                "checked_by_default": True,
                "reason_badge": "2 пари термошкарпеток Race Expert (ходові + табір)",
                "alternatives": sock_alts,
                "available_sizes": [
                    {"size": "35-37", "product_id": 5597},
                    {"size": "38-40", "product_id": 5598},
                    {"size": "40-42", "product_id": 5599},
                    {"size": "43-45", "product_id": 5600}
                ]
            })
        flask, fl_alts = pick_with_alts(available, "gear", price_tier, sub_type="soft_flask", exclude_ids=used_ids)
        if not flask:
            flask, fl_alts = pick_with_alts(available, "gear", price_tier, sub_type="water_bottle", exclude_ids=used_ids)
        if flask:
            used_ids.add(flask["product_id"])
            slots["gear"].append({
                "product": flask,
                "quantity_recommended": 1,
                "timing_instruction": "Еластична фляга або пляшка: швидкий доступ до води з лямки рюкзака без зупинки",
                "checked_by_default": True,
                "reason_badge": "Гідратаційне спорядження для маршруту",
                "alternatives": fl_alts
            })

    # --- SLOT 4: CARE & RECOVERY (ЇDLO Jerkies/Vegan Porridge, Chamois Butt'r balm, Nutrend Magneslife) ---
    if duration == "1day":
        if is_vegan:
            veg_snack, v_alts = pick_with_alts(available, "care_recovery", price_tier, sub_type="recovery_porridge", exclude_ids=used_ids)
            if not veg_snack:
                veg_snack, v_alts = pick_with_alts(available, "energy", price_tier, sub_type="energy_snack", exclude_ids=used_ids)
            if veg_snack:
                used_ids.add(veg_snack["product_id"])
                slots["care_recovery"].append({
                    "product": veg_snack,
                    "quantity_recommended": 1,
                    "timing_instruction": "Легке рослинне відновлення після ходового дня",
                    "checked_by_default": True,
                    "reason_badge": "Рослинне відновлення ЇDLO",
                    "alternatives": v_alts
                })
        else:
            jerky, jerky_alts = pick_with_alts(available, "care_recovery", price_tier, sub_type="jerky", exclude_ids=used_ids)
            if jerky:
                used_ids.add(jerky["product_id"])
                slots["care_recovery"].append({
                    "product": jerky,
                    "quantity_recommended": 1,
                    "timing_instruction": "Високобілковий перекус на денному маршруті (25 г чистого білка)",
                    "checked_by_default": True,
                    "reason_badge": "Джерки ЇDLO (сушене м'ясо)",
                    "alternatives": jerky_alts
                })
        mag, mag_alts = pick_with_alts(available, "care_recovery", price_tier, sub_type="magnesium", exclude_ids=used_ids)
        if mag:
            used_ids.add(mag["product_id"])
            slots["care_recovery"].append({
                "product": mag,
                "quantity_recommended": 1,
                "timing_instruction": "Після фінішу для зняття напруги м'язів та профілактики судом",
                "checked_by_default": True,
                "reason_badge": "Швидкий рідкий магній від спазмів",
                "alternatives": mag_alts
            })
    elif duration == "weekend":
        if is_vegan:
            veg_snack, v_alts = pick_with_alts(available, "care_recovery", price_tier, sub_type="recovery_porridge", exclude_ids=used_ids)
            if not veg_snack:
                veg_snack, v_alts = pick_with_alts(available, "energy", price_tier, sub_type="energy_snack", exclude_ids=used_ids)
            if veg_snack:
                used_ids.add(veg_snack["product_id"])
                j_qty = 3 if price_tier != "economy" else 2
                slots["care_recovery"].append({
                    "product": veg_snack,
                    "quantity_recommended": j_qty,
                    "timing_instruction": f"Рослинне вуглеводно-білкове відновлення в таборі ({j_qty} порції)",
                    "checked_by_default": True,
                    "reason_badge": f"Відновлювальне харчування ЇDLO ({j_qty} порції)",
                    "alternatives": v_alts
                })
        else:
            jerky, jerky_alts = pick_with_alts(available, "care_recovery", price_tier, sub_type="jerky", exclude_ids=used_ids)
            if jerky:
                used_ids.add(jerky["product_id"])
                j_qty = 3 if price_tier != "economy" else 2
                slots["care_recovery"].append({
                    "product": jerky,
                    "quantity_recommended": j_qty,
                    "timing_instruction": f"Чистий тваринний білок на кожному денному перевалі ({j_qty} упаковки: щоденний перекус)",
                    "checked_by_default": True,
                    "reason_badge": f"Джерки ЇDLO ({j_qty} упаковки по 50 г)",
                    "alternatives": jerky_alts
                })

        if price_tier == "premium":
            balm, balm_alts = pick_with_alts(available, "care_recovery", price_tier, sub_type="anti_chafe_balm", exclude_ids=used_ids)
            if balm:
                used_ids.add(balm["product_id"])
                slots["care_recovery"].append({
                    "product": balm,
                    "quantity_recommended": 1,
                    "timing_instruction": "Змастити стопи та зону паху перед кожним виходом: надійний захист від мозолів під важким рюкзаком",
                    "checked_by_default": True,
                    "reason_badge": "Захисний бальзам Chamois Butt'r Ultra",
                    "alternatives": balm_alts
                })

        mag, mag_alts = pick_with_alts(available, "care_recovery", price_tier, sub_type="magnesium", exclude_ids=used_ids)
        if mag:
            used_ids.add(mag["product_id"])
            slots["care_recovery"].append({
                "product": mag,
                "quantity_recommended": 2,
                "timing_instruction": "По 1 ампулі щовечора перед сном у наметі для повного розслаблення литок",
                "checked_by_default": True,
                "reason_badge": "Антиспазм магній Nutrend Magneslife Strong (2 дні)",
                "alternatives": mag_alts
            })
    else:  # expedition
        if is_vegan:
            v1, v1_alts = pick_with_alts(available, "care_recovery", price_tier, sub_type="recovery_porridge", exclude_ids=used_ids)
            if v1:
                used_ids.add(v1["product_id"])
                slots["care_recovery"].append({
                    "product": v1,
                    "quantity_recommended": 3,
                    "timing_instruction": "Рослинна бананова відновлювальна каша після денних переходів (3 упаковки)",
                    "checked_by_default": True,
                    "reason_badge": "Відновлювальна каша ЇDLO (3 упаковки)",
                    "alternatives": v1_alts
                })
            v2, v2_alts = pick_with_alts(available, "energy", price_tier, sub_type="energy_bar", exclude_ids=used_ids)
            if not v2:
                v2, v2_alts = pick_with_alts(available, "energy", price_tier, sub_type="energy_snack", exclude_ids=used_ids)
            if v2:
                used_ids.add(v2["product_id"])
                slots["care_recovery"].append({
                    "product": v2,
                    "quantity_recommended": 2,
                    "timing_instruction": "Поживний натуральний батончик/снек для табірного відпочинку (2 упаковки)",
                    "checked_by_default": True,
                    "reason_badge": "Рослинний снек ЇDLO (2 упаковки)",
                    "alternatives": v2_alts
                })
        else:
            j1, j1_alts = pick_with_alts(available, "care_recovery", price_tier, sub_type="jerky", exclude_ids=used_ids)
            if j1:
                used_ids.add(j1["product_id"])
                slots["care_recovery"].append({
                    "product": j1,
                    "quantity_recommended": 3,
                    "timing_instruction": "Висококалорійний тваринний білок та сіль під час денних переходів (3 упаковки)",
                    "checked_by_default": True,
                    "reason_badge": "М'ясні джерки ЇDLO (3 упаковки)",
                    "alternatives": j1_alts
                })
            j2, j2_alts = pick_with_alts(available, "care_recovery", price_tier, sub_type="jerky", exclude_ids=used_ids)
            if j2:
                used_ids.add(j2["product_id"])
                slots["care_recovery"].append({
                    "product": j2,
                    "quantity_recommended": 2,
                    "timing_instruction": "М'ясний перекус іншого сорту для різноманітності автономного раціону (2 упаковки)",
                    "checked_by_default": True,
                    "reason_badge": "М'ясні джерки ЇDLO (2 упаковки)",
                    "alternatives": j2_alts
                })

        if price_tier == "premium":
            balm, balm_alts = pick_with_alts(available, "care_recovery", price_tier, sub_type="anti_chafe_balm", exclude_ids=used_ids)
            if balm:
                used_ids.add(balm["product_id"])
                slots["care_recovery"].append({
                    "product": balm,
                    "quantity_recommended": 1,
                    "timing_instruction": "Критично для захисту стоп у 4+ денному поході: наносити на точки тертя щоранку",
                    "checked_by_default": True,
                    "reason_badge": "Преміальний бальзам Chamois Butt'r Ultra від мозолів",
                    "alternatives": balm_alts
                })
        elif not is_vegan:
            porridge, p_alts = pick_with_alts(available, "care_recovery", price_tier, sub_type="recovery_porridge", exclude_ids=used_ids)
            if porridge:
                used_ids.add(porridge["product_id"])
                slots["care_recovery"].append({
                    "product": porridge,
                    "quantity_recommended": 1,
                    "timing_instruction": "Легке вуглеводне відновлення в таборі відразу після важкого переходу",
                    "checked_by_default": True,
                    "reason_badge": "Відновлювальна бананова каша ЇDLO",
                    "alternatives": p_alts
                })

        mag, mag_alts = pick_with_alts(available, "care_recovery", price_tier, sub_type="magnesium", exclude_ids=used_ids)
        if mag:
            used_ids.add(mag["product_id"])
            slots["care_recovery"].append({
                "product": mag,
                "quantity_recommended": 4,
                "timing_instruction": "Курс на 4 вечори: по 1 ампулі перед засинанням проти нічних судом у спальнику",
                "checked_by_default": True,
                "reason_badge": "Nutrend Magneslife Strong (4 ампули на експедицію)",
                "alternatives": mag_alts
            })

    total_price = sum(it["product"]["price"] * it["quantity_recommended"] for s in slots.values() for it in s)
    if custom_budget:
        total_price = optimize_box_for_budget(slots, custom_budget, total_price, available)

    dur_labels = {"1day": "Одноденний похід (Day Hike)", "weekend": "Похід на вихідні (2-3 дні)", "expedition": "Автономна експедиція (4+ днів)"}
    tier_labels = {"economy": "Економ (до 3 000–6 000 грн)", "standard": "Оптимальний (до 4 000–6 500 грн)", "premium": "PRO / Максимум (від 6 500–8 000+ грн)"}

    return {
        "sport": "outdoor",
        "sport_label": "Походи та туризм (ЇDLO)",
        "distance_label": dur_labels.get(duration, "Похід"),
        "box_title": f"Туристичний бокс: {dur_labels.get(duration, 'Похід')}",
        "total_base_price": round(total_price, 2),
        "slots": slots,
        "budget_info": {
            "type": "custom" if custom_budget else "preset",
            "price_tier": price_tier,
            "tier_label": tier_labels.get(price_tier, price_tier),
            "custom_budget": custom_budget,
            "within_budget": total_price <= custom_budget if custom_budget else True,
            "savings": round(custom_budget - total_price, 2) if custom_budget and total_price <= custom_budget else 0.0
        }
    }


def generate_custom_sport_box(sport: str, inputs: Dict[str, Any]) -> Dict[str, Any]:
    catalog = load_catalog(sport)

    if sport == "running":
        return runner_box_engine.generate_runner_box(inputs, catalog)
    elif sport == "cycling":
        return generate_cycling_box(inputs, catalog)
    elif sport == "triathlon":
        return generate_triathlon_box(inputs, catalog)
    elif sport == "gym":
        return generate_gym_box(inputs, catalog)
    elif sport == "outdoor":
        return generate_outdoor_box(inputs, catalog)
    else:
        # Fallback to running
        return runner_box_engine.generate_runner_box(inputs, load_catalog("running"))
