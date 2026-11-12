import json
import re

with open("test-quiz-sandbox/scratch_207_raw.json", "r", encoding="utf-8") as f:
    records = json.load(f)

# Strict classification rules based on sports nutrition & gear domain
def classify_set(r):
    title = (r["title"] or "").lower()
    comp = (r["composition"] or "").lower()
    desc = (r["description"] or "").lower()
    full_text = f"{title} {comp} {desc}"

    # Flag detections
    has_creatine = "креатин" in full_text or "creatine" in full_text
    has_preworkout = any(w in full_text for w in ["передтренув", "предтрен", "aakg", "citrulline", "цитрулін", "beta-alanine", "бета-аланін", "pump", "c4"])
    has_protein_powder = any(w in full_text for w in ["whey", "100% whey", "сироватковий", "протеїн nutrend", "протеин nutrend", "протеин myprotein", "pure whey"])
    has_gainer = "гейнер" in full_text or "gainer" in full_text or "набір маси" in full_text or "рост мышц" in full_text or "ріст м'язів" in full_text
    has_bcaa = "bcaa" in full_text or "eaa" in full_text or "амінокисл" in full_text or "аминокисл" in full_text

    has_magnesium = any(w in full_text for w in ["ultra-mag", "triple magnesium", "магній", "магний", "magnesium", "stress b mag"])
    has_melatonin = "мелатонин" in full_text or "мелатонін" in full_text or "ultra sleep" in full_text or "sleep" in full_text
    has_sleep_herbs = any(w in full_text for w in ["5-htp", "zma", "ashwagandha", "ашваганд", "нічний zma", "спокійний вечір", "вечірнє розслаблення", "вечірній ритуал", "вечерний ритуал", "нічне відновлення", "глибокий сон", "природний сон", "польовий сон"])
    has_joint_support = any(w in full_text for w in ["bone restore", "суглоб", "сустав", "кістк", "кост", "куркума", "колаген", "коллаген", "flex", "опора руху", "зв'язк", "связок"])
    has_massage = any(w in full_text for w in ["grid roller", "массажный мяч", "масажний м'яч", "kuznetsov", "кузнецов", "валик", "роллер", "релакс та відновлення"])

    has_focus_stimulants = any(w in full_text for w in [
        "mind shi 4mushroom", "фокус і продуктивність", "фокус-формула", "свіжий фокус", "methyl b12", "b-12", "b-50", 
        "кордицепс", "cordyceps", "ежовик", "їжачник", "lion's mane", "чиста енергія", "енергія, витривалість та концентрація", 
        "розум і сила", "ресурс активного дня", "за кермом"
    ])
    
    has_daily_vitamins = any(w in full_text for w in ["d3", "d-3", "omega", "омега", "daily one", "multi pro", "вітамін c", "витамин c", "цинк", "zinc", "імунітет", "иммунитет", "активне довголіття", "щоденний захист", "три опори"])
    has_antioxidants = any(w in full_text for w in ["антиоксидант", "resveratrol", "ресвератрол", "coq10", "коензим", "вітамін e"])

    has_isotonics = any(w in full_text for w in ["hydria", "ізотонік", "изотоник", "електроліт", "электролит", "hydro", "гідратація", "гидратация", "захист від спеки"])
    has_energy_gels = any(w in full_text for w in ["гель", "gel", "марафон", "напівмарафон", "полумарафон", "підготовка до забігу", "біговий старт"])
    
    # Socks and apparel
    has_socks = any(w in full_text for w in ["шкарпет", "носк", "термошкарпет"])
    has_running_gear = any(w in full_text for w in ["бігова екіпіровка", "шнурки", "пляшка 530", "фляга", "номер", "пояс для номера"])
    has_fitness_gear = any(w in full_text for w in ["скакалка", "скакалк", "еспандер", "эспандер", "коврик", "килимок", "домашній фітнес", "йога та пілатес"])

    # Food quantities
    # Check if set is dominantly food (e.g. 10+ bars, pack of jerky, fitly mix)
    is_pure_food = False
    if any(w in full_text for w in ["14 протеиновых батончиков", "13 протеиновых батончиков", "14 протеїнових", "13 протеїнових", "fitly мікс", "fitly микс", "снеків", "снеков", "джерки", "енергетичний перекус"]):
        is_pure_food = True
    elif "батончик" in comp:
        # Check if there are only 1-2 bars as an accessory
        match = re.search(r'батончик[а-я]*\s*(?:по\s*\d+\s*г\s*)?[×x]\s*(\d+)', comp)
        if match and int(match.group(1)) >= 6:
            is_pure_food = True

    # 1. GOALS CLASSIFICATION
    goals = set()
    
    # HYDRATION
    if has_isotonics:
        goals.add("hydration")

    # STRENGTH / TRAINING
    if has_creatine or has_preworkout or has_protein_powder or has_gainer or has_bcaa or "силовий" in title or "сила" in title or "зал" in title:
        goals.add("training")

    # RECOVERY & SLEEP (Strict domain rules!)
    # Allowed: Melatonin, Sleep herbs (ZMA, 5-HTP, Reishi for sleep), Magnesium, Joint/Bone repair, Massage recovery
    # Strictly DISALLOWED: Creatine, Preworkout, Focus Nootropics/B12, Energy stimulants
    if (has_melatonin or has_sleep_herbs or has_magnesium or has_joint_support or has_massage) and not has_creatine and not has_preworkout and not has_focus_stimulants:
        goals.add("recovery")
    # Also pure night ZMA / anti-stress
    if "нічний zma" in title or "антитривожність" in title or "вечірн" in title or "вечерн" in title or "сон" in title:
        if not has_creatine:
            goals.add("recovery")

    # RUNNING
    if has_energy_gels or "марафон" in title or "біг" in title or "бег" in title or "бігова" in title or "біговий" in title:
        goals.add("running")
    if has_socks and ("біг" in full_text or "бег" in full_text or "спорт" in full_text):
        goals.add("running")

    # GEAR
    if has_socks or has_running_gear or has_fitness_gear or "екіпіровка" in title or "экипировка" in title:
        goals.add("gear")

    # FOOD
    if is_pure_food or "перекус" in title or "сніданок" in title or "харчування" in title:
        goals.add("food")

    # DAILY (Wellness, daily vitamins, mental focus/work, immunity, omega, general tone)
    if has_daily_vitamins or has_antioxidants or has_focus_stimulants or "щоденн" in title or "ежедневн" in title or "тонус" in title or "офіс" in title or "водій" in title or "за кермом" in title:
        goals.add("daily")

    # OUTDOORS
    if "термошкарпет" in comp or "термоноск" in comp or "сублімат" in full_text or "похід" in full_text or "поход" in full_text or "кемпінг" in full_text or "outdoor" in full_text:
        goals.add("outdoors")

    # GIFT
    if "подарунок" in title or "подарок" in title or "gift" in title or "презент" in title:
        goals.add("gift")

    # Ensure at least one goal
    if not goals:
        if has_socks:
            goals.add("gear")
        elif has_daily_vitamins:
            goals.add("daily")
        else:
            goals.add("training")

    # 2. COMPONENT CLASSES
    classes = set()
    if has_creatine or has_preworkout:
        classes.add("creatine_preworkout")
    if has_isotonics:
        classes.add("hydration_items")
    if is_pure_food or has_energy_gels:
        classes.add("protein_carbohydrate_food")
    if has_protein_powder or has_gainer:
        classes.add("protein_carbohydrate_food")
    # Only add food for sets with a few bars IF it's not a pure gear or pure nootropic set
    if "батончик" in comp and not is_pure_food:
        if "нічний zma" in title or "антитривожність" in title or "захист від спеки" in title:
            classes.add("protein_carbohydrate_food")
    if has_daily_vitamins or has_magnesium or has_melatonin or has_sleep_herbs or has_joint_support or has_focus_stimulants or has_antioxidants or has_bcaa:
        classes.add("supplements_vitamins_minerals")
    if has_socks or "одяг" in title:
        classes.add("apparel_footwear")
    if has_running_gear or has_fitness_gear or "пляшк" in comp or "бутылк" in comp or "шейкер" in comp:
        classes.add("sports_accessories")
    if "сублімат" in full_text:
        classes.add("dehydrated_meal")

    if not classes:
        classes.add("supplements_vitamins_minerals")

    # 3. USE TIMINGS
    timings = set()
    if "recovery" in goals:
        timings.add("evening_or_bedtime")
    if "running" in goals or "training" in goals:
        timings.add("before_or_after_training")
        if has_isotonics or has_energy_gels:
            timings.add("during_training")
    if "daily" in goals or is_pure_food:
        timings.add("daily_use")

    # 4. MAPPING FAMILIES FOR MATCHER
    # Map back to GOAL_FAMILIES
    # "running": {"running_race_preparation"}
    # "training": {"strength_muscle_training"}
    # "hydration": {"hydration_electrolytes"}
    # "food": {"portable_food_snacks", "endurance_energy"}
    # "recovery": {"recovery_fatigue", "sleep_relaxation_stress"}
    # "outdoors": {"outdoor_travel_hiking"}
    # "gear": {"foot_apparel_comfort"}
    # "daily": {"general_daily_nutrition"}
    # "gift": {"gift_identity"}
    new_families = set()
    if "running" in goals:
        new_families.add("running_race_preparation")
    if "training" in goals:
        new_families.add("strength_muscle_training")
    if "hydration" in goals:
        new_families.add("hydration_electrolytes")
    if "food" in goals:
        new_families.add("portable_food_snacks")
    if "recovery" in goals:
        new_families.add("sleep_relaxation_stress")
        new_families.add("recovery_fatigue")
    if "outdoors" in goals:
        new_families.add("outdoor_travel_hiking")
    if "gear" in goals:
        new_families.add("foot_apparel_comfort")
    if "daily" in goals:
        new_families.add("general_daily_nutrition")
    if "gift" in goals:
        new_families.add("gift_identity")

    return {
        "catalog_row": r["catalog_row"],
        "sku": r["sku"],
        "title": r["title"],
        "price_uah": r["price_uah"],
        "composition": r["composition"],
        "goals": sorted(goals),
        "families": sorted(new_families),
        "classes": sorted(classes),
        "timings": sorted(timings)
    }

proposals = [classify_set(r) for r in records]

with open("test-quiz-sandbox/scratch_207_proposals.json", "w", encoding="utf-8") as f:
    json.dump(proposals, f, ensure_ascii=False, indent=2)

print(f"Generated proposals for {len(proposals)} records.")

# Print statistics of new classification
goal_counts = {}
for p in proposals:
    for g in p["goals"]:
        goal_counts[g] = goal_counts.get(g, 0) + 1

print("\n=== PROPOSED GOALS DISTRIBUTION ===")
for g, c in sorted(goal_counts.items(), key=lambda x: -x[1]):
    print(f"  {g:12}: {c} sets")
