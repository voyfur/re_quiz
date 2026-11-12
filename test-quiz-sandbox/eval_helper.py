import sys
import json
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from server import _load_catalog, CATALOG_PATH, AUDIT_PATH
from draft_matcher import attach_audit_evidence, draft_recommend, draft_options

# Load catalog and audit
raw_catalog = _load_catalog(CATALOG_PATH)
audit_data = json.load(open(AUDIT_PATH, encoding="utf-8"))
catalog = attach_audit_evidence(raw_catalog, audit_data)
catalog_by_sku = {r["sku"]: r for r in catalog}

print(f"Loaded {len(catalog)} catalog records.")

# Known domain knowledge about sets in catalog
# Legitimate gym products: creatine, whey protein, pre-workout, BCAA, shaker, gym towel, mass gainer, gym vitamins/omega
# Disqualifications / Flaws:
# 1. RE11632 "Розум і Сила" - Mind Shi 4Mushroom + Cookies -> NO creatine, NO preworkout! False creatine tag!
# 2. RE11660 "Марафонець" - Marathon kit with PF 30 Gels -> Endurance running gear, NOT gym strength!
# 3. RE11651 "Нічний ZMA" - Sleep ZMA -> Bedtime recovery, not workout strength/creatine!
# 4. RE11663 "Йога та пілатес" - Yoga mat & expander -> False creatine tag!
# 5. RE11665 "Активний рух" - Jump rope & ab roller -> False creatine tag!
# 6. RE89489 "Основа регулярних тренувань" - Bath towel & shaker -> False creatine tag!
# 7. RE11557 "Розумна їжа" - Meal replacement Napiy -> False creatine tag!
# 8. Nabir_1118 "Міцна основа 2.0" - Whey protein & bars -> False creatine tag!
# 9. Nabir_1121 "Чоловіча сила" - Contains 4 pairs of socks in a strength/creatine kit!
# 10. RE11680 "Силовий старт" - Contains 300g pure creatine at 759 UAH, but MISSED creatine tag!

def evaluate_run(case, res):
    req = case["request"]
    results = res.get("results", [])
    near_miss = res.get("near_miss_results", [])
    floor_anchor = res.get("floor_anchor_results", [])
    status = res.get("status")
    
    act = req.get("activity")
    comp_class = req.get("component_class")
    budget = req.get("max_price_uah")
    timing = req.get("use_timing")
    
    c1_legit = True
    c1_notes = []
    
    c2_no_leak = True
    c2_notes = []
    
    c3_creatine = True
    c3_notes = []
    
    c4_truthful = True
    c4_notes = []
    
    verdict = "PASS"
    flaws = []
    
    # 0. Check core activity taxonomy defect
    if act in ("strength_training", "functional_training", "mind_body_mobility"):
        if not results and status in ("no_match", "no_exact_match"):
            verdict = "FAIL"
            flaw_msg = f"КРИТИЧНИЙ БАГ МАТЧЕРА: Відповідь на активність '{act}' повертає 0 результатів! Причина: у доказах каталогу збережено тільки 'fitness_gym', а таксономічний маппінг на '{act}' відсутній, тому двигун відхилив 100% силових наборів."
            flaws.append(flaw_msg)
            c1_legit = False
            c1_notes.append("Користувач не отримав жодного товару через таксономічний збій фільтра активності.")
            return {
                "verdict": verdict,
                "c1_legit": False,
                "c1_notes": c1_notes,
                "c2_no_leak": True,
                "c2_notes": ["Немає видачі — витік неможливий."],
                "c3_creatine": False if comp_class == "creatine_preworkout" else True,
                "c3_notes": ["Запит на креатин не задоволено (0 результатів)."] if comp_class == "creatine_preworkout" else [],
                "c4_truthful": False,
                "c4_notes": ["Двигун повідомив про відсутність наборів, хоча в каталозі є 46 наборів для залу."],
                "flaws": flaws
            }

    # Evaluate when results are returned or floor anchor
    items_to_eval = results if results else (near_miss if near_miss else floor_anchor)
    
    if not items_to_eval:
        if budget is not None and budget < 759:
            # Below absolute catalog minimum for training
            if status == "floor_anchor" and floor_anchor:
                c1_notes.append(f"Запропоновано мінімальний якірний набір ({floor_anchor[0]['price_uah']} грн) при бюджеті {budget} грн.")
            else:
                verdict = "WARN"
                flaws.append(f"Бюджет {budget} грн нижче мінімального (759 грн), але floor_anchor не спрацював належним чином.")
        else:
            verdict = "FAIL"
            flaws.append(f"Порожня видача при допустимому бюджеті ({budget} грн) та параметрах.")
        return {
            "verdict": verdict,
            "c1_legit": len(items_to_eval) > 0,
            "c1_notes": c1_notes,
            "c2_no_leak": True,
            "c2_notes": [],
            "c3_creatine": True,
            "c3_notes": [],
            "c4_truthful": True,
            "c4_notes": [],
            "flaws": flaws
        }

    for idx, item in enumerate(items_to_eval):
        sku = item.get("sku")
        title = item.get("title", "")
        price = item.get("price_uah", 0)
        reasons = item.get("why_suitable", []) or item.get("reasons", [])
        expert_sum = item.get("expert_summary", "")
        cat_rec = catalog_by_sku.get(sku, {})
        comp = (cat_rec.get("composition") or "").lower()
        title_lower = title.lower()
        
        # Criterion 1: Legitimate strength/gym products
        # A legitimate gym set must contain protein, creatine, bcaa, shaker, gym towel, or training vitamins
        has_gym_substance = any(w in comp or w in title_lower for w in [
            "креатин", "creatine", "протеїн", "whey", "bcaa", "eaa", "шейкер", "shaker", 
            "полотенце", "рушник", "маса", "mass", "передтрен", "pre-workout", "трибулус",
            "d3", "вітамін", "мульти", "мінерал", "магній", "глютамін", "батончик", "коврик"
        ])
        if not has_gym_substance:
            c1_legit = False
            c1_notes.append(f"#{idx+1} [{sku}] '{title}' не містить профільних продуктів для залу.")
            flaws.append(f"Товар #{idx+1} [{sku}] не має очевидної користі для силового атлета.")
            
        # Criterion 2: Leaks of non-gym items
        # Marathon gels
        if "pf 30 gel" in comp or "марафонець" in title_lower or "марафон" in title_lower:
            c2_no_leak = False
            msg = f"ВИТІК МАРАФОНСЬКОГО БІГУ: #{idx+1} [{sku}] '{title}' містить вуглеводні бігові гелі PF 30 Gel для тривалого забігу, що неприпустимо для чисто силового тренування!"
            c2_notes.append(msg)
            flaws.append(msg)
            verdict = "FAIL"
            
        # Night ZMA / Sleep items during daytime or strength request
        if ("zma" in comp or "нічний" in title_lower or "сон" in comp) and timing in ("before_or_after_training", "during_training"):
            c2_no_leak = False
            msg = f"ВИТІК ЗАСОБУ ДЛЯ СНУ: #{idx+1} [{sku}] '{title}' призначений для сну та нічного відновлення, але рекомендований для вживання під час/перед тренуванням!"
            c2_notes.append(msg)
            flaws.append(msg)
            if verdict != "FAIL":
                verdict = "WARN"
                
        # Socks in pure gym kit
        if "носки" in comp or "шкарпет" in comp:
            msg = f"ДИВНИЙ СКЛАД: #{idx+1} [{sku}] '{title}' містить 4 пари шкарпеток у силовому наборі спортивного харчування."
            c2_notes.append(msg)
            if verdict == "PASS":
                verdict = "WARN"
            flaws.append(msg)

        # Criterion 3: Creatine / Pre-workout precision
        if comp_class == "creatine_preworkout":
            has_actual_creatine = any(w in comp or w in title_lower for w in ["креатин", "creatine", "передтрен", "pre-workout", "pump"])
            if not has_actual_creatine:
                c3_creatine = False
                msg = f"ФАЛЬШИВИЙ КРЕАТИН: Користувач обрав клас 'creatine_preworkout', але #{idx+1} [{sku}] '{title}' взагалі не містить креатину чи передтренувального комплексу (лише гриби/печиво/снеки/інвентар)!"
                c3_notes.append(msg)
                flaws.append(msg)
                verdict = "FAIL"
            else:
                c3_notes.append(f"#{idx+1} [{sku}] містить дійсний креатин/передтрен.")

        # Criterion 4: Natural & Truthful explanation
        # Check if explanation claims "у наборі саме Креатин" when there is no creatine
        for r_text in reasons:
            if "саме Креатин" in r_text and not any(w in comp or w in title_lower for w in ["креатин", "creatine", "передтрен"]):
                c4_truthful = False
                msg = f"ОБМАН У ПОЯСНЕННІ: Двигун стверджує '{r_text}', але набір [{sku}] не має креатину!"
                c4_notes.append(msg)
                flaws.append(msg)
                verdict = "FAIL"
            if "без сторонніх речей" in r_text and ("носки" in comp or "полотенце" in comp or "коврик" in comp):
                c4_truthful = False
                msg = f"НЕПРАВДИВЕ ТВЕРДЖЕННЯ: Двигун заявляє 'без сторонніх речей', але набір [{sku}] містить побутові речі (шкарпетки/рушник)."
                c4_notes.append(msg)
                flaws.append(msg)
                if verdict == "PASS":
                    verdict = "WARN"

    return {
        "verdict": verdict,
        "c1_legit": c1_legit,
        "c1_notes": c1_notes,
        "c2_no_leak": c2_no_leak,
        "c2_notes": c2_notes,
        "c3_creatine": c3_creatine,
        "c3_notes": c3_notes,
        "c4_truthful": c4_truthful,
        "c4_notes": c4_notes,
        "flaws": flaws
    }

print("Evaluation engine ready.")
