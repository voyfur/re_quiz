import json
import re

with open("test-quiz-sandbox/scratch_207_raw.json", "r", encoding="utf-8") as f:
    records = json.load(f)

def audit_record(r):
    row = r["catalog_row"]
    sku = r["sku"]
    title = (r["title"] or "").strip()
    title_l = title.lower()
    comp = (r["composition"] or "").strip()
    comp_l = comp.lower()
    desc = (r["description"] or "").strip()
    desc_l = desc.lower()
    text = f"{title_l} {comp_l} {desc_l}"

    goals = set()
    classes = set()
    timings = set()
    activities = set()
    rationale_parts = []

    # Ingredient / Item Flags
    has_creatine = "креатин" in text or "creatine" in text
    has_preworkout = any(w in text for w in ["передтренув", "предтрен", "aakg", "citrulline", "цитрулін", "beta-alanine", "бета-аланін", "pump", "c4"])
    has_protein_powder = any(w in text for w in ["100% whey", "pure whey", "whey pro", "протеїн nutrend", "протеин nutrend", "протеин myprotein", "сироватковий"])
    has_gainer = "гейнер" in text or "gainer" in text or "набір маси" in text
    has_bcaa = "bcaa" in text or "eaa" in text

    has_melatonin = "мелатонин" in text or "мелатонін" in text or "ultra sleep" in text
    has_zma = "zma" in text or "нічний zma" in text or "ночной zma" in text
    has_night_relax = any(w in text for w in ["5-htp", "gaba", "вечірн", "вечерн", "нічне відновлення", "ночное восстановление", "спокійний сон", "спокойный сон", "глибокий сон", "глубокий сон", "польовий сон", "природний сон", "вечірнє розслаблення", "вечернее расслабление", "вечірній ритуал", "антитривожність", "відпочинок нервової системи", "внутрішня рівновага"])
    has_joints = any(w in text for w in ["bone restore", "суглоб", "сустав", "опора руху", "міцні кістки", "колаген", "коллаген", "куркума"])
    has_magnesium = any(w in text for w in ["ultra-mag", "triple magnesium", "magnesium bisglycinate", "magnesium glycinate", "magnesium citrate"])
    has_massage_roller = ("релакс та відновлення" in title_l) or ("kuznetsov" in comp_l)

    has_stimulants = any(w in text for w in [
        "mind shi 4mushroom", "4mushroom", "methyl b12", "b-12", "b-50", "кордицепс", "cordyceps", 
        "ежовик", "їжачник", "lion's mane", "чиста енергія", "концентрац", "продуктивність на максимум", 
        "розум і сила", "ресурс активного дня", "за кермом", "для офісу", "фокус"
    ])

    has_isotonics = any(w in text for w in ["hydria", "ізотонік", "изотоник", "електроліт", "электролит", "hydro"])
    has_energy_gels = any(w in text for w in ["енергетичний гель", "энергетический гель", "energy chews", "gu energy", "тиждень бігуна", "sis beta fuel", "sis go"])
    has_socks = any(w in comp_l for w in ["шкарпет", "носк", "термошкарпет", "термоноск"])
    has_running_gear = any(w in text for w in ["бігова екіпіровка", "шнурки з фіксатором", "пояс для номера", "підготовка до забігу", "марафонець", "все для марафону", "біговий старт"])
    has_fitness_gear = any(w in text for w in ["скакалка", "еспандер", "эспандер", "домашній фітнес", "йога та пілатес", "активний рух"])

    # Food check: Is it dominantly food?
    is_major_food = (any(w in text for w in [
        "14 протеиновых", "13 протеиновых", "14 протеїнових", "13 протеїнових", "fitly мікс", "fitly микс",
        "снеків", "снеков", "джерки", "енергетичний перекус", "21 lipobar", "lipobar мікс",
        "8 шт", "9 шт", "16 шт", "м'яско togo"
    ]) or has_energy_gels or has_protein_powder or has_gainer) and not has_creatine

    has_dehydrated = any(w in text for w in ["сублімат", "сублимат", "їдло", "james cook"])
    has_gift = any(w in title_l for w in ["подарунок", "подарок", "gift", "воля та незламність", "клубний бокс"])

    # --- CLASSIFY GOALS ---

    # 1. HYDRATION
    if has_isotonics:
        goals.add("hydration")
        classes.add("hydration_items")
        timings.add("during_training")
        activities.add("running")
        activities.add("cycling")
        rationale_parts.append("Ізотоніки/електроліти для гідратації")

    # 2. TRAINING (Strength, Muscle, Mass)
    if has_creatine or has_preworkout or has_protein_powder or has_gainer or has_bcaa or "сила" in title_l or "зал" in title_l or "силовий" in title_l:
        goals.add("training")
        if has_creatine or has_preworkout:
            classes.add("creatine_preworkout")
        if has_protein_powder or has_gainer:
            classes.add("protein_carbohydrate_food")
        if has_bcaa:
            classes.add("supplements_vitamins_minerals")
        timings.add("before_or_after_training")
        activities.add("strength_training")
        activities.add("functional_training")
        rationale_parts.append("Силові тренування (креатин/протеїн/предтрен)")

    # 3. RECOVERY & SLEEP (Strict!)
    # Permitted: Melatonin, ZMA, GABA, 5-HTP, sleep herbs, magnesium (without stimulants), joint repair, relax roller
    # Blocked: Creatine, Preworkout, Stimulants/Nootropics, pure socks
    if (has_melatonin or has_zma or has_night_relax or has_joints or has_massage_roller or (has_magnesium and not has_stimulants)) and not has_creatine and not has_preworkout and not has_stimulants:
        goals.add("recovery")
        timings.add("evening_or_bedtime")
        if has_joints or has_melatonin or has_zma or has_night_relax or has_magnesium:
            classes.add("supplements_vitamins_minerals")
        if has_massage_roller:
            classes.add("sports_accessories")
        if has_zma and "батончик" in comp_l:
            classes.add("protein_carbohydrate_food")
        rationale_parts.append("Відновлення та сон (магній/мелатонін/суглоби/ZMA)")

    # 4. RUNNING
    if has_energy_gels or "марафон" in title_l or "біг" in title_l or "бег" in title_l or has_running_gear or (has_socks and "термо" not in title_l):
        goals.add("running")
        activities.add("running")
        if has_energy_gels:
            classes.add("protein_carbohydrate_food")
            timings.add("during_training")
        if has_socks:
            classes.add("apparel_footwear")
        if has_running_gear or "пляшк" in comp_l or "бутылк" in comp_l:
            classes.add("sports_accessories")
        rationale_parts.append("Біг і старти (гелі/шкарпетки/аксесуари)")

    # 5. GEAR
    if has_socks or has_running_gear or has_fitness_gear or "екіпіровка" in title_l or "полотенце" in comp_l or "рушник" in comp_l:
        goals.add("gear")
        if has_socks:
            classes.add("apparel_footwear")
        if has_running_gear or has_fitness_gear or "пляшк" in comp_l or "бутылк" in comp_l or "шейкер" in comp_l:
            classes.add("sports_accessories")
        rationale_parts.append("Одяг та аксесуари")

    # 6. FOOD & SNACKS
    if is_major_food or "перекус" in title_l or has_dehydrated:
        goals.add("food")
        classes.add("protein_carbohydrate_food")
        timings.add("daily_use")
        rationale_parts.append("Спортивні перекуси (батончики/снеки)")

    # 7. OUTDOORS
    if "термошкарпет" in title_l or "термошкарпет" in comp_l or has_dehydrated or "похід" in text or "кемпінг" in text:
        goals.add("outdoors")
        activities.add("hiking")
        activities.add("walking")
        if "термошкарпет" in comp_l:
            classes.add("apparel_footwear")
        if has_dehydrated:
            classes.add("dehydrated_meal")
        rationale_parts.append("Походи та кемпінг (термошкарпетки/сублімати)")

    # 8. DAILY (Wellness, Vitamins, Daytime Focus/Tone)
    if (has_stimulants or "щоденн" in title_l or "ежедневн" in title_l or "тонус" in title_l or "офіс" in title_l or "за кермом" in title_l or "імунітет" in title_l or "активне довголіття" in title_l or "три опори" in title_l or "омега" in text or "d3" in text or "d-3" in text) and not has_creatine:
        goals.add("daily")
        classes.add("supplements_vitamins_minerals")
        timings.add("daily_use")
        rationale_parts.append("Щоденна підтримка (вітаміни/тонус/денний фокус)")

    # 9. GIFT
    if has_gift:
        goals.add("gift")
        rationale_parts.append("Подарунковий набір")

    # Safety fallbacks
    if not goals:
        if has_socks:
            goals.add("gear")
            classes.add("apparel_footwear")
        else:
            goals.add("daily")
            classes.add("supplements_vitamins_minerals")

    if not classes:
        classes.add("supplements_vitamins_minerals")

    if not timings:
        timings.add("daily_use")

    # Build matcher families
    families = set()
    if "running" in goals:
        families.add("running_race_preparation")
    if "training" in goals:
        families.add("strength_muscle_training")
    if "hydration" in goals:
        families.add("hydration_electrolytes")
    if "food" in goals:
        families.add("portable_food_snacks")
    if "recovery" in goals:
        families.add("sleep_relaxation_stress")
        families.add("recovery_fatigue")
    if "outdoors" in goals:
        families.add("outdoor_travel_hiking")
    if "gear" in goals:
        families.add("foot_apparel_comfort")
    if "daily" in goals:
        families.add("general_daily_nutrition")
    if "gift" in goals:
        families.add("gift_identity")

    return {
        "catalog_row": row,
        "sku": sku,
        "title": title,
        "price_uah": r["price_uah"],
        "composition": comp,
        "goals": sorted(goals),
        "families": sorted(families),
        "classes": sorted(classes),
        "timings": sorted(timings),
        "activities": sorted(activities),
        "rationale": "; ".join(rationale_parts)
    }

curated = [audit_record(r) for r in records]

with open("test-quiz-sandbox/curated_207_audit.json", "w", encoding="utf-8") as f:
    json.dump(curated, f, ensure_ascii=False, indent=2)

print(f"Audited all {len(curated)} records and wrote to test-quiz-sandbox/curated_207_audit.json")
