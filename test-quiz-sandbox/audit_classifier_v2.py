import json
import re

with open("test-quiz-sandbox/scratch_207_raw.json", "r", encoding="utf-8") as f:
    records = json.load(f)

def clean_classify(r):
    title = (r["title"] or "").strip()
    title_l = title.lower()
    comp = (r["composition"] or "").strip()
    comp_l = comp.lower()
    desc = (r["description"] or "").strip()
    desc_l = desc.lower()
    full_text = f"{title_l} {comp_l} {desc_l}"

    # Exact ingredient checks
    has_creatine = "креатин" in full_text or "creatine" in full_text
    has_preworkout = any(w in full_text for w in ["передтренув", "предтрен", "aakg", "citrulline", "цитрулін", "beta-alanine", "бета-аланін", "pump", "c4"])
    has_protein_powder = any(w in full_text for w in ["100% whey", "pure whey", "whey pro", "протеїн nutrend", "протеин nutrend", "протеин myprotein", "сироватковий"])
    has_gainer = "гейнер" in full_text or "gainer" in full_text or "набір маси" in full_text
    has_bcaa = "bcaa" in full_text or "eaa" in full_text

    has_melatonin = "мелатонин" in full_text or "мелатонін" in full_text or "ultra sleep" in full_text
    has_zma = "zma" in full_text or "нічний zma" in full_text or "ночной zma" in full_text
    has_sleep_herbs = any(w in full_text for w in ["5-htp", "gaba", "вечірн", "вечерн", "сон", "нічне відновлення", "ночное восстановление", "спокійний сон", "спокойный сон", "глибокий сон", "глубокий сон", "польовий сон", "природний сон", "вечірнє розслаблення", "вечернее расслабление", "вечірній ритуал", "антитривожність", "відпочинок нервової системи", "внутрішня рівновага"])
    has_joints = any(w in full_text for w in ["bone restore", "суглоб", "сустав", "опора руху", "міцні кістки", "колаген", "коллаген", "куркума"])
    has_magnesium = any(w in full_text for w in ["ultra-mag", "triple magnesium", "magnesium bisglycinate", "magnesium glycinate", "magnesium citrate"])
    
    # Pure massage recovery
    has_massage_recovery = ("релакс та відновлення" in title_l) or ("kuznetsov" in comp_l and "pillow" in comp_l)

    has_focus_stimulants = any(w in full_text for w in [
        "фокус", "mind shi 4mushroom", "4mushroom", "methyl b12", "b-12", "b-50", "кордицепс", "cordyceps", 
        "ежовик", "їжачник", "lion's mane", "чиста енергія", "концентрац", "продуктивність на максимум", 
        "розум і сила", "ресурс активного дня", "за кермом", "для офісу"
    ])

    has_daily_vitamins = any(w in full_text for w in ["d3", "d-3", "omega", "омега", "daily one", "multi pro", "вітамін c", "витамин c", "цинк", "zinc", "імунітет", "иммунитет", "активне довголіття", "щоденний захист", "три опори", "alive men", "alive women", "trace minerals", "омега + сонце"])
    has_isotonics = any(w in full_text for w in ["hydria", "ізотонік", "изотоник", "електроліт", "электролит", "hydro"])
    has_energy_gels = any(w in full_text for w in ["енергетичний гель", "энергетический гель", "energy chews", "gu energy", "тиждень бігуна", "підготовка до забігу", "марафонець", "все для марафону", "біговий старт"])
    
    has_socks = any(w in comp_l for w in ["шкарпет", "носк", "термошкарпет", "термоноск"])
    has_pure_socks_box = "1+1=3" in title_l or "5 пар" in title_l or "термошкарпеток" in title_l or "білих шкарпеток" in title_l or "темних шкарпеток" in title_l
    
    has_fitness_gear = any(w in full_text for w in ["скакалка", "еспандер", "эспандер", "домашній фітнес", "йога та пілатес", "активний рух"])
    has_running_gear = any(w in full_text for w in ["бігова екіпіровка", "шнурки з фіксатором", "пояс для номера"])

    is_pure_food = any(w in full_text for w in [
        "fitly", "14 протеиновых", "13 протеиновых", "14 протеїнових", "13 протеїнових", 
        "снеків", "снеков", "джерки", "енергетичний перекус", "протеїновий заряд"
    ])
    has_dehydrated = "сублімат" in full_text or "їдло" in full_text or "похід" in full_text or "кемпінг" in full_text

    has_gift = any(w in title_l for w in ["подарунок", "подарок", "gift", "воля та незламність", "клубний бокс"])

    # Determine Goals
    goals = set()

    # 1. Recovery & Sleep
    # Strictly for sleep, relax, ZMA, magnesium, melatonin, joint/bone repair, and relax massage
    # Disallow: Creatine, Preworkout, Focus/Nootropics, Isotonics, Running gear, Pure socks
    if (has_melatonin or has_zma or has_sleep_herbs or has_joints or has_massage_recovery) and not has_creatine and not has_preworkout and not has_focus_stimulants and not has_pure_socks_box:
        goals.add("recovery")
    # Also pure magnesium if not bundled with stimulants
    if has_magnesium and not has_focus_stimulants and not has_creatine:
        goals.add("recovery")

    # 2. Training (Strength & Muscle)
    if has_creatine or has_preworkout or has_protein_powder or has_gainer or has_bcaa:
        goals.add("training")
    if any(w in title_l for w in ["чиста сила", "силовий старт", "ріст м'язів", "база сили", "запорука сили", "чоловіча база залу", "регулярний зал", "потужний старт", "підготовка до тренувань у залі"]):
        goals.add("training")

    # 3. Running
    if has_energy_gels or "марафон" in title_l or "біг" in title_l or "бег" in title_l:
        goals.add("running")
    if (has_socks or has_running_gear) and not ("термошкарпет" in title_l or "похід" in title_l):
        goals.add("running")
    if has_isotonics:
        goals.add("running")

    # 4. Hydration
    if has_isotonics:
        goals.add("hydration")

    # 5. Food & Snacks
    if is_pure_food or "перекус" in title_l:
        goals.add("food")

    # 6. Daily (Wellness, Focus, Daytime Immunity, Vitamins)
    if has_daily_vitamins or has_focus_stimulants or "щоденн" in title_l or "ежедневн" in title_l or "тонус" in title_l or "за кермом" in title_l or "офіс" in title_l or "імунітет" in title_l:
        goals.add("daily")

    # 7. Outdoors
    if "термошкарпет" in title_l or "термошкарпет" in comp_l or has_dehydrated:
        goals.add("outdoors")

    # 8. Gear (Apparel & Accessories)
    if has_socks or has_running_gear or has_fitness_gear or "екіпіровка" in title_l or has_massage_recovery:
        goals.add("gear")

    # 9. Gift
    if has_gift:
        goals.add("gift")

    # Fallback safety
    if not goals:
        if has_socks:
            goals.add("gear")
        else:
            goals.add("daily")

    # Determine Component Classes
    classes = set()
    if has_creatine or has_preworkout:
        classes.add("creatine_preworkout")
    if has_isotonics:
        classes.add("hydration_items")
    if is_pure_food or has_energy_gels or has_protein_powder or has_gainer:
        classes.add("protein_carbohydrate_food")
    # Only sets where food is meaningful (>= 4 bars or primary)
    if "батончик" in comp_l:
        match = re.search(r'батончик[а-я]*\s*(?:по\s*\d+\s*г\s*)?[×x]\s*(\d+)', comp_l)
        if match and int(match.group(1)) >= 3:
            classes.add("protein_carbohydrate_food")
        elif "нічний zma" in title_l:
            classes.add("protein_carbohydrate_food")
    if has_daily_vitamins or has_magnesium or has_melatonin or has_sleep_herbs or has_joints or has_focus_stimulants or has_bcaa:
        classes.add("supplements_vitamins_minerals")
    if has_socks or "одяг" in title_l:
        classes.add("apparel_footwear")
    if has_running_gear or has_fitness_gear or has_massage_recovery or "пляшк" in comp_l or "бутылк" in comp_l or "шейкер" in comp_l:
        classes.add("sports_accessories")
    if has_dehydrated:
        classes.add("dehydrated_meal")

    if not classes:
        classes.add("supplements_vitamins_minerals")

    # Timings
    timings = set()
    if "recovery" in goals:
        timings.add("evening_or_bedtime")
    if "running" in goals or "training" in goals:
        timings.add("before_or_after_training")
        if has_isotonics or has_energy_gels:
            timings.add("during_training")
    if "daily" in goals or is_pure_food or "gear" in goals:
        timings.add("daily_use")

    # Activity groups
    activities = set()
    if "running" in goals:
        activities.add("running")
    if "training" in goals:
        activities.add("strength_training")
        activities.add("functional_training")
    if "hydration" in goals:
        activities.add("running")
        activities.add("cycling")
    if "outdoors" in goals:
        activities.add("hiking")
        activities.add("walking")
    if has_fitness_gear:
        activities.add("functional_training")
        activities.add("mind_body_mobility")

    # Map to matcher families
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
        "catalog_row": r["catalog_row"],
        "sku": r["sku"],
        "title": title,
        "price_uah": r["price_uah"],
        "composition": comp,
        "goals": sorted(goals),
        "families": sorted(families),
        "classes": sorted(classes),
        "timings": sorted(timings),
        "activities": sorted(activities)
    }

audited = [clean_classify(r) for r in records]

with open("test-quiz-sandbox/scratch_207_audited_clean.json", "w", encoding="utf-8") as f:
    json.dump(audited, f, ensure_ascii=False, indent=2)

print(f"Audited {len(audited)} records.")

goal_counts = {}
for a in audited:
    for g in a["goals"]:
        goal_counts[g] = goal_counts.get(g, 0) + 1

print("\n=== CLEAN AUDITED GOALS DISTRIBUTION ===")
for g, c in sorted(goal_counts.items(), key=lambda x: -x[1]):
    print(f"  {g:12}: {c:3} sets")

class_counts = {}
for a in audited:
    for c in a["classes"]:
        class_counts[c] = class_counts.get(c, 0) + 1

print("\n=== CLEAN AUDITED CLASSES DISTRIBUTION ===")
for c, count in sorted(class_counts.items(), key=lambda x: -x[1]):
    print(f"  {c:30}: {count:3} sets")
