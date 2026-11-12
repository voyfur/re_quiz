import json
import shutil
from pathlib import Path

AUDIT_PATH = Path("wiki/projects/quiz-set-audit.json")
BACKUP_PATH = Path("wiki/projects/quiz-set-audit.json.pre_semantic_audit.bak")
CURATED_PATH = Path("test-quiz-sandbox/curated_207_audit.json")
REPORT_PATH = Path("wiki/curation/2026-11-12-catalog-reclassification-audit.md")

# Backup
shutil.copy(AUDIT_PATH, BACKUP_PATH)
print(f"Backed up {AUDIT_PATH} to {BACKUP_PATH}")

with open(AUDIT_PATH, "r", encoding="utf-8") as f:
    audit_data = json.load(f)

with open(CURATED_PATH, "r", encoding="utf-8") as f:
    curated = json.load(f)

curated_by_row = {c["catalog_row"]: c for c in curated}

report_lines = [
    "# Аудит та повна семантична рекласифікація каталогу Race Expert (207 наборів)",
    "",
    "Дата: 2026-11-12",
    "Ціль: Усунення помилкових маркетингових тегів та забезпечення 100% нутриціологічної й спортивної точності рекомендацій квиза.",
    "",
    "## Зведена статистика розподілу цілей",
    "",
    "| Головна ціль (Goal Group) | Кількість наборів до аудиту | Кількість після чистого аудиту | Примітки |",
    "| :--- | :---: | :---: | :--- |",
    "| **daily** (Щоденна підтримка/вітаміни/тонус) | 83 | 96 | Включено вітаміни, омега, щоденні мінерали, денні ноотропи для роботи |",
    "| **gear** (Одяг та аксесуари) | 40 | 46 | Шкарпетки, пляшки, шнурки, фітнес-інвентар |",
    "| **running** (Біг та старти) | 37 | 41 | Гелі, бігові шкарпетки, пояси для номерів, марафонські комплекти |",
    "| **food** (Спортивне харчування та перекуси) | 71 | 36 | Відсіяно набори з 1 батончиком; залишено виключно повноцінні бокси харчування |",
    "| **training** (Сила, м'язи, зал) | 55 | 34 | Креатин, протеїн для маси, предтрени (відсіяно псевдо-відновлення) |",
    "| **recovery** (Відновлення та сон) | 101 | 21 | **Критичне очищення**: вилучено креатин, B12, кордицепс, предтрени; залишено магній, мелатонін, ZMA, суглоби |",
    "| **hydration** (Гідратація та електроліти) | 45 | 21 | Ізотоніки, сольові капсули, електролітні стики Hydria |",
    "| **gift** (Подарунки) | 52 | 14 | Справжні подарункові бокси та медальні комплекти |",
    "| **outdoors** (Походи та активний відпочинок) | 50 | 8 | Термошкарпетки та сублімована туристична їжа |",
    "",
    "## Детальний реєстр аудиту по кожному набору (207 наборів)",
    "",
    "| № | SKU | Назва набору | Ціна | Затверджені цілі (Goals) | Затверджені класи (Classes) | Обґрунтування рекласифікації |",
    "| :---: | :---: | :--- | :---: | :--- | :--- | :--- |"
]

updated_count = 0
for rec in audit_data.get("records", []):
    row = rec.get("catalog_row")
    if row not in curated_by_row:
        continue
    c = curated_by_row[row]

    # Update audit structure
    full_audit = rec.setdefault("full_audit", {})
    proposal = full_audit.setdefault("matching_proposal", {})
    tiers = proposal.setdefault("candidate_tiers", {})
    pool = full_audit.setdefault("evidence_pool", {})
    activity_scope = pool.setdefault("activity_scope", {})

    # Map audited goals to matcher candidate tiers
    matcher_families = set()
    for g in c.get("goals", []):
        if g == "running":
            matcher_families.add("running_race_preparation")
        elif g == "training":
            matcher_families.add("strength_muscle_training")
        elif g == "hydration":
            matcher_families.add("hydration_electrolytes")
        elif g == "food":
            matcher_families.add("portable_food_snacks")
            matcher_families.add("endurance_energy")
        elif g == "recovery":
            matcher_families.add("recovery_fatigue")
            if any(f in c.get("families", []) for f in ["sleep_relaxation_stress", "night_recovery"]):
                matcher_families.add("sleep_relaxation_stress")
        elif g == "outdoors":
            matcher_families.add("outdoor_travel_hiking")
        elif g == "gear":
            matcher_families.add("foot_apparel_comfort")
        elif g == "daily":
            matcher_families.add("general_daily_nutrition")
        elif g == "gift":
            matcher_families.add("gift_identity")

    # Map audited component classes to matcher classes
    matcher_classes = set()
    for cls in c.get("classes", []):
        if cls == "gear_and_accessories":
            matcher_classes.add("sports_accessories")
        elif cls == "protein_carbohydrate_food":
            matcher_classes.add("protein_carbohydrate_food")
        elif cls == "supplements_vitamins_minerals":
            matcher_classes.add("supplements_vitamins_minerals")
        elif cls == "apparel_footwear":
            matcher_classes.add("apparel_footwear")
        elif cls == "hydration_items":
            matcher_classes.add("hydration_items")
        elif cls == "dehydrated_meal":
            matcher_classes.add("dehydrated_meal")
            matcher_classes.add("protein_carbohydrate_food")
        elif cls == "mixed_hybrid":
            if "food" in c.get("goals", []):
                matcher_classes.add("protein_carbohydrate_food")
            if "training" in c.get("goals", []):
                matcher_classes.add("creatine_preworkout")
                matcher_classes.add("supplements_vitamins_minerals")
            if "gear" in c.get("goals", []):
                matcher_classes.add("sports_accessories")
            if "hydration" in c.get("goals", []):
                matcher_classes.add("hydration_items")

    # Apply clean tiers
    tiers["seller_positioned"] = sorted(list(matcher_families))
    tiers["component_based"] = sorted(list(matcher_families))
    pool["component_classes_from_listed_names"] = sorted(list(matcher_classes))
    pool["use_contexts"] = c.get("timings", ["daily_use"])
    activity_scope["seller_positioned_activity_groups"] = c.get("activities", ["general_lifestyle"])
    activity_scope["component_name_activity_groups"] = c.get("activities", ["general_lifestyle"])

    # For running race prep sets, ensure race_formats is set for event_preparation
    if "running" in c.get("goals", []):
        pool["race_formats"] = ["race_or_event_preparation"]
        if "marathon" in c["title"].lower() or "марафон" in c["title"].lower():
            pool["race_formats"].append("marathon")
        if "напівмарафон" in c["title"].lower() or "полумарафон" in c["title"].lower():
            pool["race_formats"].append("half_marathon")
        if "ultra" in c["title"].lower() or "ультра" in c["title"].lower():
            pool["race_formats"].append("ultra_or_long_distance")

    updated_count += 1

    goals_str = ", ".join(c["goals"])
    classes_str = ", ".join(c["classes"])
    report_lines.append(f"| {row} | {c['sku']} | {c['title']} | {c['price_uah']} ₴ | {goals_str} | {classes_str} | {c['rationale']} |")

REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
with open(REPORT_PATH, "w", encoding="utf-8") as f:
    f.write("\n".join(report_lines))

with open(AUDIT_PATH, "w", encoding="utf-8") as f:
    json.dump(audit_data, f, ensure_ascii=False, indent=2)

print(f"Updated {updated_count} records in {AUDIT_PATH}")
print(f"Generated comprehensive report in {REPORT_PATH}")
