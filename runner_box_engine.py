"""Runner Box Decision Engine.

Pure deterministic engine that builds custom running nutrition and gear boxes
based on physiological rules, weather, distance, and user preferences.
"""

from typing import Dict, List, Any


def generate_runner_box(inputs: Dict[str, Any], catalog: List[Dict[str, Any]]) -> Dict[str, Any]:
    raw_dist = str(inputs.get("distance", "21k")).lower().strip()
    dist_map = {
        "marathon": "42k",
        "full_marathon": "42k",
        "full": "42k",
        "42": "42k",
        "42.2k": "42k",
        "half": "21k",
        "half_marathon": "21k",
        "half-marathon": "21k",
        "21": "21k",
        "21.1k": "21k",
        "10": "10k",
        "ultra": "trail",
        "ultramarathon": "trail",
        "trail_run": "trail"
    }
    distance = dist_map.get(raw_dist, raw_dist if raw_dist in {"10k", "21k", "42k", "trail"} else "21k")
    pace_target = inputs.get("pace_target", "steady")
    caffeine_pref = inputs.get("caffeine_preference", "none")
    weather = inputs.get("weather", "moderate")
    stomach_type = inputs.get("stomach_type", "normal")
    body_concerns = set(inputs.get("body_concerns", []))
    gear_needed = set(inputs.get("gear_needed", []))
    price_tier = inputs.get("price_tier", "standard")

    # Custom budget handling
    custom_budget = None
    raw_budget = inputs.get("custom_budget") or inputs.get("max_budget")
    if raw_budget:
        try:
            custom_budget = float(raw_budget)
        except (ValueError, TypeError):
            custom_budget = None

    if custom_budget and custom_budget > 0 and not inputs.get("price_tier_explicit"):
        if distance == "10k":
            price_tier = "economy" if custom_budget < 1000 else ("standard" if custom_budget <= 2000 else "premium")
        elif distance == "21k":
            price_tier = "economy" if custom_budget < 1400 else ("standard" if custom_budget <= 2500 else "premium")
        else:
            price_tier = "economy" if custom_budget < 2900 else ("standard" if custom_budget <= 4200 else "premium")

    # Filter catalog by in-stock and distance suitability
    available = [
        p for p in catalog 
        if p.get("quantity", 0) > 0 and (not p.get("distances") or distance in p["distances"])
    ]

    # Enforce strict zero caffeine rule if requested
    if caffeine_pref == "none":
        available = [p for p in available if not p.get("caffeine", False)]

    # Enforce vegan filter if requested
    if stomach_type == "vegan":
        available = [p for p in available if p.get("is_vegan", True)]

    slots: Dict[str, List[Dict[str, Any]]] = {
        "energy": [],
        "hydration": [],
        "gear": [],
        "care_recovery": []
    }

    used_product_ids = set()

    # Intelligent multi-factor scoring function
    def score_item(p: dict) -> float:
        score = 50.0
        # Tier match bonus
        if p.get("price_tier") == price_tier:
            score += 35.0
        elif (price_tier == "premium" and p.get("price_tier") == "standard") or (price_tier == "economy" and p.get("price_tier") == "standard"):
            score += 15.0
        
        # Brand quality bonus (top tier running brands)
        brand = p.get("brand", "")
        if brand in ["SiS", "Maurten", "Precision Fuel & Hydration", "GU Energy", "Sponser", "Race Expert"]:
            score += 20.0
        
        # Stomach sensitive bonus
        if stomach_type == "sensitive" and p.get("stomach_gentle"):
            score += 30.0
        
        # Pace synergy
        name_lower = p.get("name", "").lower()
        if pace_target == "record":
            if any(k in name_lower for k in ["roctane", "beta fuel", "hydrogel", "caffeine", "endurosnack"]):
                score += 15.0
        elif pace_target == "finish":
            if any(k in name_lower for k in ["isotonic", "chew", "мармелад", "желейні"]):
                score += 15.0
        
        # Weather synergy
        if weather == "hot":
            if any(k in name_lower for k in ["electrolyte", "електроліт", "salt", "лимон", "лайм", "апельсин"]):
                score += 12.0

        # Stock availability bonus (prefer items with high stock to avoid checkout collisions)
        qty = p.get("quantity", 0)
        if qty > 50:
            score += 8.0

        return score

    # Helper to find best item with alternative suggestions
    def pick_item_with_alts(slot: str, sub_type: str = None, need_caffeine: bool = None, stomach_gentle: bool = None, exclude_ids: set = None, brand: str = None):
        candidates = [p for p in available if p.get("slot") == slot]
        if brand:
            brand_candidates = [p for p in candidates if p.get("brand") == brand]
            if brand_candidates:
                candidates = brand_candidates

        if sub_type:
            sub_matches = [p for p in candidates if p.get("sub_type") == sub_type]
            if sub_matches:
                candidates = sub_matches
        if need_caffeine is not None:
            caff_matches = [p for p in candidates if p.get("caffeine") == need_caffeine]
            if caff_matches:
                candidates = caff_matches
        if stomach_gentle:
            gentle_matches = [p for p in candidates if p.get("stomach_gentle")]
            if gentle_matches:
                candidates = gentle_matches

        if exclude_ids:
            unexcluded = [p for p in candidates if p.get("product_id") not in exclude_ids]
            if unexcluded:
                candidates = unexcluded
            # If all flavors/SKUs of this brand are in exclude_ids (e.g. 42k requires 5 gels but brand has 4 flavors),
            # keep candidates to repeat the best SKU of the SAME brand and strictly avoid mixing gel brands!

        if not candidates:
            # Safe fallback if criteria too narrow
            candidates = [p for p in available if p.get("slot") == slot]
            if brand:
                brand_cands = [p for p in candidates if p.get("brand") == brand]
                if brand_cands:
                    candidates = brand_cands
            if sub_type:
                sub_cands = [p for p in candidates if p.get("sub_type") == sub_type]
                if sub_cands:
                    candidates = sub_cands
            if need_caffeine is not None:
                caff_matches = [p for p in candidates if p.get("caffeine") == need_caffeine]
                if caff_matches:
                    candidates = caff_matches

        if not candidates:
            return None, []

        # Sort by dynamic score descending, price ascending
        candidates.sort(key=lambda p: (-score_item(p), p.get("price", 0)))
        primary = candidates[0]
        
        # Alternatives: prioritize same brand when brand is specified
        if brand:
            same_brand_alts = [p for p in available if p.get("slot") == slot and p.get("brand") == brand and p.get("product_id") != primary.get("product_id")]
            other_alts = [p for p in available if p.get("slot") == slot and p.get("brand") != brand]
            other_alts.sort(key=lambda p: (-score_item(p), p.get("price", 0)))
            alternatives = (same_brand_alts + other_alts)[:5]
        else:
            alternatives = candidates[1:6]

        return primary, alternatives

    def pick_item(slot: str, sub_type: str = None, need_caffeine: bool = None, stomach_gentle: bool = None, exclude_ids: set = None, brand: str = None):
        prim, _ = pick_item_with_alts(slot, sub_type, need_caffeine, stomach_gentle, exclude_ids, brand)
        return prim

    # 1. SLOT: ENERGY (Single Brand & Gel Type Consistency + Flavor Diversity)
    gentle = (stomach_type == "sensitive")
    
    # Select primary base gel to anchor the brand for all energy gels in this box
    base_gel, base_alts = pick_item_with_alts("energy", sub_type="gel", need_caffeine=False, stomach_gentle=gentle, exclude_ids=used_product_ids)
    primary_gel_brand = base_gel.get("brand") if base_gel else None

    if distance == "10k":
        if base_gel:
            used_product_ids.add(base_gel["product_id"])
            slots["energy"].append({
                "product": base_gel,
                "quantity_recommended": 1,
                "timing_instruction": "За 15 хв до старту для заповнення глікогенового депо",
                "checked_by_default": True,
                "reason_badge": "Основна енергія (вуглеводи)",
                "alternatives": base_alts
            })

        if caffeine_pref == "boost":
            caff_gel, caff_alts = pick_item_with_alts("energy", sub_type="gel", need_caffeine=True, brand=primary_gel_brand, exclude_ids=used_product_ids)
            if caff_gel:
                used_product_ids.add(caff_gel["product_id"])
                slots["energy"].append({
                    "product": caff_gel,
                    "quantity_recommended": 1,
                    "timing_instruction": "За 3-4 км до фінішу для прискорення на фінішній прямій",
                    "checked_by_default": True,
                    "reason_badge": "Кофеїновий буст на фініш",
                    "alternatives": caff_alts
                })
        else:
            gel2, gel2_alts = pick_item_with_alts("energy", sub_type="gel", need_caffeine=False, stomach_gentle=gentle, brand=primary_gel_brand, exclude_ids=used_product_ids)
            if gel2:
                used_product_ids.add(gel2["product_id"])
                slots["energy"].append({
                    "product": gel2,
                    "quantity_recommended": 1,
                    "timing_instruction": "На 5-6 км дистанції для підтримки темпу",
                    "checked_by_default": True,
                    "reason_badge": "Дистанційне підживлення",
                    "alternatives": gel2_alts
                })

    elif distance == "21k":
        if base_gel:
            used_product_ids.add(base_gel["product_id"])
            slots["energy"].append({
                "product": base_gel,
                "quantity_recommended": 1,
                "timing_instruction": "На 7 км дистанції для стабільного темпу",
                "checked_by_default": True,
                "reason_badge": "Вуглеводний блок #1",
                "alternatives": base_alts
            })

        for i, km in enumerate([12, 15]):
            gel, gel_alts = pick_item_with_alts("energy", sub_type="gel", need_caffeine=False, stomach_gentle=gentle, brand=primary_gel_brand, exclude_ids=used_product_ids)
            if gel:
                used_product_ids.add(gel["product_id"])
                slots["energy"].append({
                    "product": gel,
                    "quantity_recommended": 1,
                    "timing_instruction": f"На {km} км дистанції для стабільного темпу",
                    "checked_by_default": True,
                    "reason_badge": f"Вуглеводний блок #{i+2}",
                    "alternatives": gel_alts
                })

        if caffeine_pref == "boost":
            caff_gel, caff_alts = pick_item_with_alts("energy", sub_type="gel", need_caffeine=True, brand=primary_gel_brand, exclude_ids=used_product_ids)
            if caff_gel:
                used_product_ids.add(caff_gel["product_id"])
                slots["energy"].append({
                    "product": caff_gel,
                    "quantity_recommended": 1,
                    "timing_instruction": "На 17-18 км для фінішного прискорення",
                    "checked_by_default": True,
                    "reason_badge": "Кофеїновий буст на фініш",
                    "alternatives": caff_alts
                })
        else:
            gel_fin, fin_alts = pick_item_with_alts("energy", sub_type="gel", need_caffeine=False, stomach_gentle=gentle, brand=primary_gel_brand, exclude_ids=used_product_ids)
            if gel_fin:
                used_product_ids.add(gel_fin["product_id"])
                slots["energy"].append({
                    "product": gel_fin,
                    "quantity_recommended": 1,
                    "timing_instruction": "На 18 км для легкого фінішу",
                    "checked_by_default": True,
                    "reason_badge": "Фінішний запас глікогену",
                    "alternatives": fin_alts
                })

        chew, chew_alts = pick_item_with_alts("energy", sub_type="chew", need_caffeine=False, brand=primary_gel_brand, exclude_ids=used_product_ids)
        if chew:
            used_product_ids.add(chew["product_id"])
            slots["energy"].append({
                "product": chew,
                "quantity_recommended": 1,
                "timing_instruction": "На 10-12 км між гелями для збереження жувального тонусу",
                "checked_by_default": True,
                "reason_badge": "Енергетичний мармелад",
                "alternatives": chew_alts
            })

    else:
        # 42k or Trail
        target_gel_count = 5 if distance == "42k" else 4
        if base_gel:
            used_product_ids.add(base_gel["product_id"])
            slots["energy"].append({
                "product": base_gel,
                "quantity_recommended": 1,
                "timing_instruction": "На 7 км дистанції для запуску енергообміну",
                "checked_by_default": True,
                "reason_badge": "Вуглеводний блок #1",
                "alternatives": base_alts
            })

        for i in range(1, target_gel_count):
            g, alts = pick_item_with_alts("energy", sub_type="gel", need_caffeine=False, stomach_gentle=gentle, brand=primary_gel_brand, exclude_ids=used_product_ids)
            if g:
                used_product_ids.add(g["product_id"])
                km_hint = f"На {7 * (i + 1)} км дистанції"
                slots["energy"].append({
                    "product": g,
                    "quantity_recommended": 1,
                    "timing_instruction": km_hint,
                    "checked_by_default": True,
                    "reason_badge": f"Вуглеводний блок #{i+1}",
                    "alternatives": alts
                })

        if caffeine_pref == "boost":
            for ci, km in enumerate([32, 37] if distance == "42k" else [30]):
                caff_gel, caff_alts = pick_item_with_alts("energy", sub_type="gel", need_caffeine=True, brand=primary_gel_brand, exclude_ids=used_product_ids)
                if caff_gel:
                    used_product_ids.add(caff_gel["product_id"])
                    slots["energy"].append({
                        "product": caff_gel,
                        "quantity_recommended": 1,
                        "timing_instruction": f"На {km} км для подолання марафонської стіни та фінішного ривка",
                        "checked_by_default": True,
                        "reason_badge": f"Кофеїновий буст #{ci+1}",
                        "alternatives": caff_alts
                    })
        else:
            for ci, km in enumerate([32, 37] if distance == "42k" else [30]):
                extra_gel, extra_alts = pick_item_with_alts("energy", sub_type="gel", need_caffeine=False, stomach_gentle=gentle, brand=primary_gel_brand, exclude_ids=used_product_ids)
                if extra_gel:
                    used_product_ids.add(extra_gel["product_id"])
                    slots["energy"].append({
                        "product": extra_gel,
                        "quantity_recommended": 1,
                        "timing_instruction": f"На {km} км для підтримки глікогену на фінішних кілометрах",
                        "checked_by_default": True,
                        "reason_badge": f"Фінішний вуглеводний блок #{ci+1}",
                        "alternatives": extra_alts
                    })

        chew, chew_alts = pick_item_with_alts("energy", sub_type="chew", need_caffeine=False, brand=primary_gel_brand, exclude_ids=used_product_ids)
        if chew:
            used_product_ids.add(chew["product_id"])
            slots["energy"].append({
                "product": chew,
                "quantity_recommended": 1,
                "timing_instruction": "На 25 км (екватор дистанції) для переходу на тверду текстуру",
                "checked_by_default": True,
                "reason_badge": "Енергетичний мармелад",
                "alternatives": chew_alts
            })

    # 2. SLOT: HYDRATION
    if weather == "hot" or "cramps" in body_concerns or distance in ["42k", "trail"]:
        salt, salt_alts = pick_item_with_alts("hydration", sub_type="salt_caps", exclude_ids=used_product_ids)
        if salt:
            used_product_ids.add(salt["product_id"])
            slots["hydration"].append({
                "product": salt,
                "quantity_recommended": 1,
                "timing_instruction": "1 капсула кожні 45-50 хв для захисту від судом",
                "checked_by_default": True,
                "reason_badge": "Сольовий баланс та електроліти",
                "alternatives": salt_alts
            })
        iso, iso_alts = pick_item_with_alts("hydration", sub_type="isotonic", exclude_ids=used_product_ids)
        if iso:
            used_product_ids.add(iso["product_id"])
            slots["hydration"].append({
                "product": iso,
                "quantity_recommended": 1,
                "timing_instruction": "Пити невеликими ковтками для відновлення вологи",
                "checked_by_default": True,
                "reason_badge": "Гідратація та мінерали",
                "alternatives": iso_alts
            })
    else:
        iso, iso_alts = pick_item_with_alts("hydration", sub_type="isotonic", exclude_ids=used_product_ids)
        if iso:
            used_product_ids.add(iso["product_id"])
            slots["hydration"].append({
                "product": iso,
                "quantity_recommended": 1,
                "timing_instruction": "Розчинити у воді, пити за день до старту та після фінішу",
                "checked_by_default": True,
                "reason_badge": "Гідратація та електроліти",
                "alternatives": iso_alts
            })

    # 3. SLOT: GEAR
    gear_candidates = set(gear_needed)
    if not gear_candidates:
        if price_tier == "premium" or distance in ["42k", "trail"]:
            gear_candidates.add("socks")
        else:
            gear_candidates.add("belt")

    if "belt" in gear_candidates:
        belt, belt_alts = pick_item_with_alts("gear", sub_type="running_belt", exclude_ids=used_product_ids)
        if belt:
            used_product_ids.add(belt["product_id"])
            slots["gear"].append({
                "product": belt,
                "quantity_recommended": 1,
                "timing_instruction": "Для зручного кріплення гелів, телефону та стартового номера",
                "checked_by_default": True,
                "reason_badge": "Зручність перенесення",
                "alternatives": belt_alts
            })
    if "flask" in gear_candidates:
        flask, flask_alts = pick_item_with_alts("gear", sub_type="soft_flask", exclude_ids=used_product_ids)
        if flask:
            used_product_ids.add(flask["product_id"])
            slots["gear"].append({
                "product": flask,
                "quantity_recommended": 1,
                "timing_instruction": "М'яка бігова фляга для води чи ізотоніка на ходу",
                "checked_by_default": True,
                "reason_badge": "Гідратація на ходу",
                "alternatives": flask_alts
            })
    if "socks" in gear_candidates:
        socks, socks_alts = pick_item_with_alts("gear", sub_type="running_socks", exclude_ids=used_product_ids)
        if socks:
            used_product_ids.add(socks["product_id"])
            slots["gear"].append({
                "product": socks,
                "quantity_recommended": 1,
                "timing_instruction": "Спеціальні бігові шкарпетки проти натертостей та мозолів",
                "checked_by_default": True,
                "reason_badge": "Комфорт та захист стопи",
                "available_sizes": [
                    {"size": "35-37", "product_id": 7451},
                    {"size": "38-40", "product_id": 7452},
                    {"size": "40-42", "product_id": 7453},
                    {"size": "43-45", "product_id": 7454}
                ],
                "alternatives": socks_alts
            })

    # 4. SLOT: CARE & RECOVERY
    care_candidates = set(body_concerns)
    if distance in ["42k", "trail"]:
        care_candidates.add("chafing")
        care_candidates.add("recovery_shake")
    elif not care_candidates:
        if price_tier == "premium":
            care_candidates.add("recovery_shake")
        else:
            care_candidates.add("magnesium")

    if "chafing" in care_candidates:
        cream, cream_alts = pick_item_with_alts("care_recovery", sub_type="anti_chafe", exclude_ids=used_product_ids)
        if cream:
            used_product_ids.add(cream["product_id"])
            slots["care_recovery"].append({
                "product": cream,
                "quantity_recommended": 1,
                "timing_instruction": "Нанести на проблемні ділянки за 20 хв до старту",
                "checked_by_default": True,
                "reason_badge": "Захист шкіри від натирання",
                "alternatives": cream_alts
            })
    if "cramps" in care_candidates or "magnesium" in care_candidates:
        mg, mg_alts = pick_item_with_alts("care_recovery", sub_type="magnesium", exclude_ids=used_product_ids)
        if mg:
            used_product_ids.add(mg["product_id"])
            slots["care_recovery"].append({
                "product": mg,
                "quantity_recommended": 1,
                "timing_instruction": "Прийняти відразу після фінішу для швидкого розслаблення м'язів",
                "checked_by_default": True,
                "reason_badge": "Магній для відновлення м'язів",
                "alternatives": mg_alts
            })
    if "joints" in care_candidates:
        joints, joints_alts = pick_item_with_alts("care_recovery", sub_type="joint_care", exclude_ids=used_product_ids)
        if joints:
            used_product_ids.add(joints["product_id"])
            slots["care_recovery"].append({
                "product": joints,
                "quantity_recommended": 1,
                "timing_instruction": "Для підтримки зв'язок та суглобів під час навантажень",
                "checked_by_default": True,
                "reason_badge": "Захист суглобів та зв'язок",
                "alternatives": joints_alts
            })
    if "recovery_shake" in care_candidates or distance in ["42k", "trail"]:
        recovery, rec_alts = pick_item_with_alts("care_recovery", sub_type="recovery_drink", exclude_ids=used_product_ids)
        if recovery and not any(it["product"]["product_id"] == recovery["product_id"] for it in slots["care_recovery"]):
            used_product_ids.add(recovery["product_id"])
            slots["care_recovery"].append({
                "product": recovery,
                "quantity_recommended": 1,
                "timing_instruction": "Випити протягом 30 хв після фінішу для швидкого відновлення глікогену",
                "checked_by_default": True,
                "reason_badge": "Швидке відновлення м'язів",
                "alternatives": rec_alts
            })

    # Calculate total base price
    total_price = 0.0
    for slot_items in slots.values():
        for it in slot_items:
            total_price += it["product"]["price"] * it["quantity_recommended"]

    # Budget optimizer: if custom_budget is set and total_price > custom_budget, optimize down
    if custom_budget and custom_budget > 0 and total_price > custom_budget:
        all_entries = []
        for slot_name, slot_items in slots.items():
            for it in slot_items:
                all_entries.append((slot_name, it))
        all_entries.sort(key=lambda x: x[1]["product"]["price"] * x[1]["quantity_recommended"], reverse=True)

        # Pass 1: Attached alternatives (respecting gel brand consistency)
        for slot_name, it in all_entries:
            if total_price <= custom_budget:
                break
            curr_price = it["product"]["price"]
            qty = it["quantity_recommended"]
            alts = it.get("alternatives", [])
            curr_caff = it["product"].get("caffeine", False)
            curr_sub = it["product"].get("sub_type")
            cheaper_alts = [a for a in alts if a.get("price", 0) < curr_price and a.get("quantity", 0) > 0]
            if curr_sub:
                cheaper_alts = [a for a in cheaper_alts if a.get("sub_type") == curr_sub]
            if caffeine_pref == "none":
                cheaper_alts = [a for a in cheaper_alts if not a.get("caffeine", False)]
            elif slot_name == "energy" and curr_sub == "gel":
                # Preserve caffeine property of the gel
                cheaper_alts = [a for a in cheaper_alts if a.get("caffeine", False) == curr_caff]

            if slot_name == "energy" and curr_sub == "gel" and primary_gel_brand:
                cheaper_alts = [a for a in cheaper_alts if a.get("brand") == primary_gel_brand]

            cheaper_alts.sort(key=lambda a: a.get("price", 0))
            if cheaper_alts:
                best_alt = cheaper_alts[0]
                diff = (curr_price - best_alt["price"]) * qty
                it["product"] = best_alt
                total_price -= diff

        # Pass 2: Catalog alternatives in that slot
        if total_price > custom_budget:
            for slot_name, it in all_entries:
                if total_price <= custom_budget:
                    break
                curr_price = it["product"]["price"]
                qty = it["quantity_recommended"]
                curr_caff = it["product"].get("caffeine", False)
                curr_sub = it["product"].get("sub_type")
                candidates = [p for p in catalog if p.get("slot") == slot_name and p.get("price", 0) < curr_price and p.get("quantity", 0) > 0]
                if curr_sub:
                    candidates = [p for p in candidates if p.get("sub_type") == curr_sub]
                if caffeine_pref == "none":
                    candidates = [p for p in candidates if not p.get("caffeine", False)]
                elif slot_name == "energy" and curr_sub == "gel":
                    candidates = [p for p in candidates if p.get("caffeine", False) == curr_caff]

                if slot_name == "energy" and curr_sub == "gel" and primary_gel_brand:
                    candidates = [p for p in candidates if p.get("brand") == primary_gel_brand and p.get("sub_type") == "gel"]
                candidates.sort(key=lambda p: p.get("price", 0))
                if candidates:
                    best_cand = candidates[0]
                    diff = (curr_price - best_cand["price"]) * qty
                    it["product"] = best_cand
                    total_price -= diff

        # Pass 3: Multi-unit consumables reduction (down to min 1)
        if total_price > custom_budget:
            for slot_name, it in all_entries:
                if total_price <= custom_budget:
                    break
                qty = it["quantity_recommended"]
                if qty > 1:
                    price = it["product"]["price"]
                    reduce_by = min(qty - 1, int((total_price - custom_budget) // price) + 1)
                    if reduce_by > 0:
                        it["quantity_recommended"] -= reduce_by
                        total_price -= reduce_by * price

    labels = {
        "10k": "10 км",
        "21k": "Півмарафон (21.1 км)",
        "42k": "Марафон (42.2 км)",
        "trail": "Трейл / Ультра"
    }

    tier_labels = {
        "economy": "Економ (до 900–1 200 грн)",
        "standard": "Оптимальний (до 1 500–2 000 грн)",
        "premium": "PRO / Еліта (від 2 500+ грн)"
    }

    return {
        "distance_label": labels.get(distance, distance),
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
