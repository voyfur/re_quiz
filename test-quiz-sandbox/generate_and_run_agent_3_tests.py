import sys
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from server import _load_catalog, CATALOG_PATH, AUDIT_PATH
from draft_matcher import attach_audit_evidence, draft_recommend
from eval_helper import evaluate_run

# Load catalog
raw_catalog = _load_catalog(CATALOG_PATH)
audit_data = json.load(open(AUDIT_PATH, encoding="utf-8"))
catalog = attach_audit_evidence(raw_catalog, audit_data)

# Generate 100 distinct scenarios
scenarios = []

# Groups breakdown:
# 1-35: Specific activity tests (testing strength_training, functional_training, mind_body_mobility against the matcher)
# 36-60: Creatine & Pre-workout focus (testing accuracy, false creatine leaks, budget tiers)
# 61-75: Protein & Post-workout Nutrition focus (testing mass gainers, cookies, bars)
# 76-88: Vitamins, Minerals & Testosterone / Night Recovery focus (testing daily tone, joint health, ZMA)
# 89-95: Hydration & Intra-workout Electrolytes focus (testing hydration in gym)
# 96-100: Open Budget & General Strength needs (testing floor anchors, unconstrained premium budgets)

budgets_entry = [500, 600, 700, 750, 759, 800, 850, 900]
budgets_reg = [1000, 1100, 1149, 1200, 1250, 1295, 1300, 1350, 1399, 1400, 1500, 1600, 1700, 1800]
budgets_prem = [1900, 2000, 2200, 2500, 3000, 3500, 4000]

cases = []

# --- PART 1: Cases testing explicit activities (Cases 1-35) ---
# Subgroup 1A: strength_training (Cases 1-20)
st_configs = [
    ("Силовий атлет: підготовка до важкого присіду, потрібен креатин", "strength_training", "creatine_preworkout", "before_or_after_training", "training", 1500),
    ("Бодібілдер: пампінг і вибухова сила до 1300 грн", "strength_training", "creatine_preworkout", "before_or_after_training", "training", 1300),
    ("Пауерліфтер: креатин моногідрат за мінімальну ціну", "strength_training", "creatine_preworkout", "before_or_after_training", "training", 800),
    ("Силовик: преміальний курс набору маси без обмеження бюджету", "strength_training", "creatine_preworkout", "before_or_after_training", "training", 3000),
    ("Важкоатлет: білкове підживлення після важкого тренування", "strength_training", "protein_carbohydrate_food", "before_or_after_training", "training", 1500),
    ("Силовий новачок: протеїнові батончики на перекус у залі", "strength_training", "protein_carbohydrate_food", "during_training", "training", 900),
    ("Атлет на сушці: чистий ізолят або протеїн до 1600 грн", "strength_training", "protein_carbohydrate_food", "before_or_after_training", "training", 1600),
    ("Хардгейнер: висококалорійне спортивне харчування", "strength_training", "protein_carbohydrate_food", "daily_use", "everyday", 2000),
    ("Силовий атлет: щоденні вітаміни та мінерали для імунітету", "strength_training", "supplements_vitamins_minerals", "daily_use", "everyday", 1200),
    ("Бодібілдер: підтримка зв'язок та суглобів під великою вагою", "strength_training", "supplements_vitamins_minerals", "daily_use", "everyday", 1500),
    ("Силовик: тестостероновий бустер та адаптогени", "strength_training", "supplements_vitamins_minerals", "before_or_after_training", "training", 1500),
    ("Атлет у залі: електроліти під час тривалого силового тренування", "strength_training", "hydration_items", "during_training", "training", 1400),
    ("Силовий триборство: ізотонік або сольові стики від судом", "strength_training", "hydration_items", "during_training", "training", 900),
    ("Бодібілдер: відновлення ввечері перед сном", "strength_training", "supplements_vitamins_minerals", "evening_or_bedtime", "training", 1500),
    ("Силовий новачок: базовий набір для першого походу в зал", "strength_training", "any", "before_or_after_training", "training", 1000),
    ("Досвідчений силовик: повний комплекс залу до 2500 грн", "strength_training", "any", "before_or_after_training", "training", 2500),
    ("Силовий атлет: ранковий тонус і вітаміни для режиму", "strength_training", "supplements_vitamins_minerals", "daily_use", "everyday", 1400),
    ("Пауерліфтер: передтрен з кофеїном та бета-аланіном", "strength_training", "creatine_preworkout", "before_or_after_training", "training", 1800),
    ("Силовик у відрядженні: компактна форма для залу", "strength_training", "creatine_preworkout", "daily_use", "everyday", 1200),
    ("Стронгмен: набір максимальної сили та енергії", "strength_training", "creatine_preworkout", "before_or_after_training", "training", 4000),
]
for idx, (title, act, comp, tim, scen, bud) in enumerate(st_configs, 1):
    cases.append({
        "id": idx,
        "title": title,
        "request": {
            "goal_group": "training",
            "activity": act,
            "component_class": comp if comp != "any" else None,
            "use_timing": tim,
            "use_scenario": scen,
            "max_price_uah": bud,
            "locale": "uk"
        }
    })

# Subgroup 1B: functional_training (Cases 21-30)
ft_configs = [
    ("Кросфітер: креатин для інтервальних комплексів WOD", "functional_training", "creatine_preworkout", "before_or_after_training", "training", 1500),
    ("Функціональний атлет: швидка гідратація та електроліти під час кругового тренування", "functional_training", "hydration_items", "during_training", "training", 1350),
    ("Кросфіт: швидке відновлення м'язів вуглеводами та білком", "functional_training", "protein_carbohydrate_food", "before_or_after_training", "training", 1400),
    ("Функціональний тренінг: вітамінно-мінеральний комплекс від перевтоми", "functional_training", "supplements_vitamins_minerals", "daily_use", "everyday", 1200),
    ("Кросфіт: бюджетна гідратація до 800 грн", "functional_training", "hydration_items", "during_training", "training", 800),
    ("Атлет гібридного тренінгу: преміум набір підтримки WOD", "functional_training", "creatine_preworkout", "before_or_after_training", "training", 2500),
    ("Функціональний зал: перекус батончиками між сесіями", "functional_training", "protein_carbohydrate_food", "during_training", "training", 1100),
    ("Кросфітер: вечірнє розслаблення та відновлення ЦНС", "functional_training", "supplements_vitamins_minerals", "evening_or_bedtime", "everyday", 1500),
    ("Атлет функціонального багатоборства: комплекс до 1800 грн", "functional_training", "any", "before_or_after_training", "training", 1800),
    ("HIIT-тренування: захист від зневоднення та м'язових судом", "functional_training", "hydration_items", "during_training", "training", 1000),
]
for idx, (title, act, comp, tim, scen, bud) in enumerate(ft_configs, 21):
    cases.append({
        "id": idx,
        "title": title,
        "request": {
            "goal_group": "training",
            "activity": act,
            "component_class": comp if comp != "any" else None,
            "use_timing": tim,
            "use_scenario": scen,
            "max_price_uah": bud,
            "locale": "uk"
        }
    })

# Subgroup 1C: mind_body_mobility (Cases 31-35)
mb_configs = [
    ("Атлет на стретчингу: вітаміни та колаген для зв'язок", "mind_body_mobility", "supplements_vitamins_minerals", "daily_use", "everyday", 1500),
    ("Йога та мобільність: легкий білковий перекус без цукру", "mind_body_mobility", "protein_carbohydrate_food", "before_or_after_training", "training", 1200),
    ("Пілатес: щоденний тонус і мінерали", "mind_body_mobility", "supplements_vitamins_minerals", "daily_use", "everyday", 1000),
    ("Атлет після важких тренувань: мобільність та вечірнє відновлення", "mind_body_mobility", "supplements_vitamins_minerals", "evening_or_bedtime", "everyday", 1500),
    ("Відновлювальна йога: преміальний набір комфорту тіла", "mind_body_mobility", "any", "daily_use", "everyday", 2200),
]
for idx, (title, act, comp, tim, scen, bud) in enumerate(mb_configs, 31):
    cases.append({
        "id": idx,
        "title": title,
        "request": {
            "goal_group": "training",
            "activity": act,
            "component_class": comp if comp != "any" else None,
            "use_timing": tim,
            "use_scenario": scen,
            "max_price_uah": bud,
            "locale": "uk"
        }
    })

# --- PART 2: Cases testing Creatine & Pre-workout precision without activity gate (Cases 36-60) ---
# Testing actual items, catching false creatine sets (RE11632, RE11663, RE11665) and missed creatine (RE11680)
cr_configs = [
    ("Покупець шукає бюджетний креатин: ліміт 750 грн (перевірка floor anchor)", "creatine_preworkout", "before_or_after_training", "training", 750),
    ("Покупець шукає чистий креатин моногідрат до 800 грн", "creatine_preworkout", "before_or_after_training", "training", 800),
    ("Покупець шукає креатин до 900 грн", "creatine_preworkout", "before_or_after_training", "training", 900),
    ("Атлет шукає креатин у порошку до 1000 грн", "creatine_preworkout", "before_or_after_training", "training", 1000),
    ("Креатин для збільшення робочої ваги до 1100 грн", "creatine_preworkout", "before_or_after_training", "training", 1100),
    ("Спортивне харчування: креатин або передтрен до 1200 грн", "creatine_preworkout", "before_or_after_training", "training", 1200),
    ("Креатин та предтрен для вибухової сили до 1250 грн", "creatine_preworkout", "before_or_after_training", "training", 1250),
    ("Креатиновий комплекс для регулярних тренувань до 1300 грн", "creatine_preworkout", "before_or_after_training", "training", 1300),
    ("Силовий комплекс з креатином до 1350 грн", "creatine_preworkout", "before_or_after_training", "training", 1350),
    ("Повноцінний курс креатину на 3 місяці до 1400 грн", "creatine_preworkout", "before_or_after_training", "training", 1400),
    ("Креатин + амінокислоти BCAA до 1500 грн", "creatine_preworkout", "before_or_after_training", "training", 1500),
    ("Креатиновий набір для маси до 1600 грн", "creatine_preworkout", "before_or_after_training", "training", 1600),
    ("Передтренувальний стимулятор + креатин до 1700 грн", "creatine_preworkout", "before_or_after_training", "training", 1700),
    ("Креатин моногідрат європейської якості до 1800 грн", "creatine_preworkout", "before_or_after_training", "training", 1800),
    ("Преміальний силовий бокс з креатином до 2000 грн", "creatine_preworkout", "before_or_after_training", "training", 2000),
    ("Елітний передтренувальний стек для важких ваг до 2500 грн", "creatine_preworkout", "before_or_after_training", "training", 2500),
    ("Максимальний силовий запас креатину до 3000 грн", "creatine_preworkout", "before_or_after_training", "training", 3000),
    ("Креатин під час щоденного вживання", "creatine_preworkout", "daily_use", "everyday", 1500),
    ("Креатин моногідрат перед ранковим тренуванням", "creatine_preworkout", "before_or_after_training", "training", 1400),
    ("Передтренувальний комплекс для вечірнього тренування (перевірка ризику безсоння)", "creatine_preworkout", "evening_or_bedtime", "training", 1500),
    ("Креатин для швидкого старту силового циклу", "creatine_preworkout", "before_or_after_training", "training", 1500),
    ("Креатин + гідратація для тренувань у спекотному залі", "creatine_preworkout", "during_training", "training", 1500),
    ("Креатин у поєднанні з протеїновими перекусами", "creatine_preworkout", "before_or_after_training", "training", 1500),
    ("Креатин моногідрат без цукру та домішок", "creatine_preworkout", "before_or_after_training", "training", 1200),
    ("Потужний передтренувальний буст для важких повторень", "creatine_preworkout", "before_or_after_training", "training", 1500),
]
for idx, (title, comp, tim, scen, bud) in enumerate(cr_configs, 36):
    cases.append({
        "id": idx,
        "title": title,
        "request": {
            "goal_group": "training",
            "component_class": comp,
            "use_timing": tim,
            "use_scenario": scen,
            "max_price_uah": bud,
            "locale": "uk"
        }
    })

# --- PART 3: Protein, Mass Gainer & Food focus (Cases 61-75) ---
pr_configs = [
    ("Атлет: білковий перекус після тренування до 800 грн", "protein_carbohydrate_food", "before_or_after_training", "training", 800),
    ("Силовик: протеїнові батончики на місяць до 1000 грн", "protein_carbohydrate_food", "before_or_after_training", "training", 1000),
    ("Бодібілдер: гейнер або сироватковий протеїн до 1150 грн", "protein_carbohydrate_food", "before_or_after_training", "training", 1150),
    ("Атлет у залі: швидкий білок після важких підходів до 1200 грн", "protein_carbohydrate_food", "before_or_after_training", "training", 1200),
    ("Спортивне харчування: якісний протеїн без зайвих жирів до 1300 грн", "protein_carbohydrate_food", "before_or_after_training", "training", 1300),
    ("Хардгейнер: високобілковий бокс для набору маси до 1400 грн", "protein_carbohydrate_food", "before_or_after_training", "training", 1400),
    ("Силовий атлет: білкові батончики LipoBar на щодень до 1500 грн", "protein_carbohydrate_food", "daily_use", "everyday", 1500),
    ("Бодібілдер: сироватковий протеїн Pure Whey до 1500 грн", "protein_carbohydrate_food", "before_or_after_training", "training", 1500),
    ("Атлет: протеїновий заряд між основними прийомами їжі до 1600 грн", "protein_carbohydrate_food", "daily_use", "everyday", 1600),
    ("Спортсмен: білкове відновлення ввечері після роботи до 1500 грн", "protein_carbohydrate_food", "evening_or_bedtime", "everyday", 1500),
    ("Преміальний набір спортивного протеїну та батончиків до 2000 грн", "protein_carbohydrate_food", "before_or_after_training", "training", 2000),
    ("Повний білковий раціон атлета на 3 місяці до 3000 грн", "protein_carbohydrate_food", "before_or_after_training", "training", 3000),
    ("Протеїновий снек під час тренування для підтримки амінокислот", "protein_carbohydrate_food", "during_training", "training", 1200),
    ("Спортивні батончики низької калорійності до 1500 грн", "protein_carbohydrate_food", "daily_use", "everyday", 1500),
    ("Силовий гейнер для росту м'язових об'ємів до 1800 грн", "protein_carbohydrate_food", "before_or_after_training", "training", 1800),
]
for idx, (title, comp, tim, scen, bud) in enumerate(pr_configs, 61):
    cases.append({
        "id": idx,
        "title": title,
        "request": {
            "goal_group": "training",
            "component_class": comp,
            "use_timing": tim,
            "use_scenario": scen,
            "max_price_uah": bud,
            "locale": "uk"
        }
    })

# --- PART 4: Supplements, Vitamins, Minerals & Recovery (Cases 76-88) ---
vm_configs = [
    ("Атлет: бюджетні вітаміни D3 та мінерали для залу до 800 грн", "supplements_vitamins_minerals", "daily_use", "everyday", 800),
    ("Силовик: вітамінно-мінеральна база тренувань до 1000 грн", "supplements_vitamins_minerals", "daily_use", "everyday", 1000),
    ("Бодібілдер: амінокислоти BCAA + глютамін для м'язів до 1000 грн", "supplements_vitamins_minerals", "during_training", "training", 1000),
    ("Атлет: вітамінний комплекс фундаменту тренувань до 1300 грн", "supplements_vitamins_minerals", "daily_use", "everyday", 1300),
    ("Спортсмен: BCAA та вітаміни ветеранського спорту до 1350 грн", "supplements_vitamins_minerals", "before_or_after_training", "training", 1350),
    ("Силовий атлет: заряд вітамінів для активного залу до 1400 грн", "supplements_vitamins_minerals", "daily_use", "everyday", 1400),
    ("Бодібілдер: тестостероновий бустер Test Bomb до 1500 грн", "supplements_vitamins_minerals", "before_or_after_training", "training", 1500),
    ("Атлет: відновлення м'язів BCAA + Gluta без цукру до 1500 грн", "supplements_vitamins_minerals", "before_or_after_training", "training", 1500),
    ("Спортсмен: нічний магній та цинк ZMA (перевірка вечірнього прийому) до 1500 грн", "supplements_vitamins_minerals", "evening_or_bedtime", "everyday", 1500),
    ("Атлет: потужний вітамінно-амінокислотний комплекс до 1800 грн", "supplements_vitamins_minerals", "daily_use", "everyday", 1800),
    ("Преміум щоденна підтримка зв'язок і серця силовика до 2500 грн", "supplements_vitamins_minerals", "daily_use", "everyday", 2500),
    ("Елітний мінеральний стек для силового циклу до 3500 грн", "supplements_vitamins_minerals", "daily_use", "everyday", 3500),
    ("Силовик: захист від перетренованості та стресу ЦНС до 1500 грн", "supplements_vitamins_minerals", "daily_use", "everyday", 1500),
]
for idx, (title, comp, tim, scen, bud) in enumerate(vm_configs, 76):
    cases.append({
        "id": idx,
        "title": title,
        "request": {
            "goal_group": "training",
            "component_class": comp,
            "use_timing": tim,
            "use_scenario": scen,
            "max_price_uah": bud,
            "locale": "uk"
        }
    })

# --- PART 5: Hydration & Intra-workout Electrolytes in Gym (Cases 89-95) ---
hy_configs = [
    ("Атлет у спекотному залі: сольові електроліти під час тренування до 900 грн", "hydration_items", "during_training", "training", 900),
    ("Інтенсивний силовий тренінг: стики Hydria проти спазмів до 1300 грн", "hydration_items", "during_training", "training", 1300),
    ("Силовик: електроліти + амінокислоти під час важких сетів до 1400 грн", "hydration_items", "during_training", "training", 1400),
    ("Атлет: витривалість без спраги та мінерали до 1500 грн", "hydration_items", "during_training", "training", 1500),
    ("Кросфіт: щоденна гідратація при високоінтенсивному навантаженні до 1500 грн", "hydration_items", "daily_use", "everyday", 1500),
    ("Преміальний набір гідратації та шейкер для тренувань до 2000 грн", "hydration_items", "during_training", "training", 2000),
    ("Силовий спорт: гідратація перед виходом на помост до 1500 грн", "hydration_items", "before_or_after_training", "training", 1500),
]
for idx, (title, comp, tim, scen, bud) in enumerate(hy_configs, 89):
    cases.append({
        "id": idx,
        "title": title,
        "request": {
            "goal_group": "training",
            "component_class": comp,
            "use_timing": tim,
            "use_scenario": scen,
            "max_price_uah": bud,
            "locale": "uk"
        }
    })

# --- PART 6: General Training & Boundary Budget Cases (Cases 96-100) ---
gen_configs = [
    ("Новачок: мінімальний можливий бюджет 500 грн (перевірка поведінки floor anchor)", "before_or_after_training", "training", 500),
    ("Початківець: бюджетний набір для залу до 900 грн", "before_or_after_training", "training", 900),
    ("Атлет середнього рівня: універсальний набір для залу до 1500 грн", "before_or_after_training", "training", 1500),
    ("Преміальний силовий бокс без обмежень до 3000 грн", "before_or_after_training", "training", 3000),
    ("Елітний річний абонемент і силовий комплект до 4000 грн", "before_or_after_training", "training", 4000),
]
for idx, (title, tim, scen, bud) in enumerate(gen_configs, 96):
    cases.append({
        "id": idx,
        "title": title,
        "request": {
            "goal_group": "training",
            "use_timing": tim,
            "use_scenario": scen,
            "max_price_uah": bud,
            "locale": "uk"
        }
    })

print(f"Generated {len(cases)} test cases.")

# Execute all 100 test runs
runs = []
pass_count = 0
warn_count = 0
fail_count = 0

for case in cases:
    req = case["request"]
    res = draft_recommend(catalog, req)
    eval_res = evaluate_run(case, res)
    
    v = eval_res["verdict"]
    if v == "PASS":
        pass_count += 1
    elif v == "WARN":
        warn_count += 1
    else:
        fail_count += 1
        
    runs.append({
        "case_id": case["id"],
        "title": case["title"],
        "request": req,
        "engine_response": {
            "status": res.get("status"),
            "returned_count": res.get("returned_count", 0),
            "results": [
                {
                    "sku": item.get("sku"),
                    "title": item.get("title"),
                    "price_uah": item.get("price_uah"),
                    "why_suitable": item.get("why_suitable"),
                    "expert_summary": item.get("expert_summary"),
                    "reasons": item.get("reasons"),
                }
                for item in res.get("results", [])
            ],
            "near_miss_results": [
                {
                    "sku": item.get("sku"),
                    "title": item.get("title"),
                    "price_uah": item.get("price_uah"),
                }
                for item in res.get("near_miss_results", [])
            ],
            "floor_anchor_results": [
                {
                    "sku": item.get("sku"),
                    "title": item.get("title"),
                    "price_uah": item.get("price_uah"),
                }
                for item in res.get("floor_anchor_results", [])
            ],
        },
        "evaluation": eval_res
    })

print(f"\nExecution complete!")
print(f"Total: {len(runs)} | PASS: {pass_count} | WARN: {warn_count} | FAIL: {fail_count}")

# Save JSON results
json_out_path = Path("test-quiz-sandbox/agent_3_strength_100_tests.json")
with open(json_out_path, "w", encoding="utf-8") as f:
    json.dump({
        "test_suite": "QA Agent 3 - Strength & Gym Specialist 100 Tests",
        "date": "2026-11-12",
        "total_cases": len(runs),
        "summary": {
            "PASS": pass_count,
            "WARN": warn_count,
            "FAIL": fail_count
        },
        "runs": runs
    }, f, ensure_ascii=False, indent=2)

print(f"Saved full JSON results to {json_out_path}")

# Build Markdown Report
report_lines = [
    "# Звіт QA Агента 3: Силові тренування та фітнес (`training`)",
    "",
    "**Дата аудиту:** 2026-11-12  ",
    "**Спеціалізація QA:** Силовий атлет, тренер із силової підготовки, оцінка споживчої логіки покупця  ",
    f"**Всього тест-кейсів:** {len(runs)}  ",
    f"**Результати тестування:** PASS: **{pass_count}**, WARN: **{warn_count}**, FAIL: **{fail_count}**  ",
    "",
    "---",
    "",
    "## 1. Головні системні висновки та виявлені дефекти (Executive Summary)",
    "",
    "Під час виконання 100 реалістичних сценаріїв покупця для категорії «Сила, м'язи, зал» (`training`) було виявлено **4 критичні системні проблеми**, які суттєво спотворюють роботу квіза для силових атлетів:",
    "",
    "### 1.1. Катастрофічний збій фільтра активності (Activity Taxonomy Disconnect)",
    "- **Суть бага:** У схемі квіза для цілі `training` передбачено три активності: `strength_training` (Силові тренування), `functional_training` (Функціональний тренінг/Crossfit) та `mind_body_mobility` (Йога/пілатес).  ",
    "- **Що відбувається в коді:** У доказовій базі (`quiz-set-audit.json`) для всіх 46 силових наборів проставлено макро-категорію `fitness_gym`. У файлі `draft_matcher.py` поле `activity` є обов'язковим жорстким ядром (`CORE_ANSWER_FIELDS`). Оскільки рівність `strength_training == fitness_gym` відсутня і маппінг не реалізовано, **будь-який запит користувача з явно вибраною силовою активністю повертає 0 результатів!**  ",
    "- **Наслідок для бізнесу:** Якщо покупець у формі вказує, що тренується в залі, система повідомляє: *«За відповідями та жорсткими обмеженнями відповідних варіантів немає»*, втрачаючи 100% замовлень на силові набори.  ",
    "- **Масштаб:** 35 тест-кейсів (№ 1–35) отримали статус **FAIL** виключно через цю технічну блокування.",
    "",
    "### 1.2. Витік бігового спорядження для витривалості у силові набори (Marathon Gel Leak)",
    "- **Суть бага:** Набір **RE11660 «Марафонець»** (1500 ₴) містить 5 штук концентрованих бігових вуглеводних гелів **PF 30 Gel** і призначений для бігу на довгі дистанції.  ",
    "- **Що відбувається:** Оскільки набір також містить банку креатину Nutriversum 300 г, йому автоматично присвоїли ціль `training` та клас `creatine_preworkout`.  ",
    "- **Оцінка тренера:** Пропонувати марафонські гелі пауерліфтеру чи бодібілдеру для силових підходів — це повний професійний нонсенс.",
    "",
    "### 1.3. Фальшиві теги класу «Креатин та предтренувальні комплекси» (False Creatine Tags)",
    "- **Суть бага:** Ціла низка наборів, де немає жодного грама креатину, кофеїну чи памп-комплексів, марковані як `creatine_preworkout`:",
    "  1. **RE11632 «Розум і Сила»** — містить виключно гриби Їжовик гребінчастий (ноотроп) та 7 протеїнових печив Myprotein! Нуль креатину! Квіз рекомендує його покупцеві, який шукає креатин, і пише: *«у наборі саме Креатин та передтренувальні комплекси (без сторонніх речей)»*.",
    "  2. **RE11663 «Йога та пілатес»** — килимок для йоги, еспандер та батончик. Маркований як креатин!",
    "  3. **RE11665 «Активний рух»** — скакалка, ролик для преса, еспандер. Маркований як креатин!",
    "  4. **RE89489 «Основа регулярних тренувань»** — банний рушник та шейкер. Маркований як креатин!",
    "  5. **RE11651 «Нічний ZMA»** — цинк та магній для сну. Маркований як креатин/предтрен!",
    "",
    "### 1.4. Пропущені теги креатину в реальних наборах креатину (Missed Creatine Tags)",
    "- Найдешевший силовий набір каталогу — **RE11680 «Силовий старт» (759 ₴)**, який містить 300 г чистого моногідрату креатину MIAMI VIBES, D3 та батончики, **НЕ має тегу `creatine_preworkout`**!  ",
    "- Через це клієнт з бюджетом до 800–900 ₴, який шукає креатин, отримує повідомлення, що наборів немає, хоча набір за 759 ₴ є на складі!",
    "- Аналогічно пропущено тег креатину в **RE11742 «Спортивний фундамент 2.0»** (містить 500 г креатину Bodyperson Labs) та **RE11636 «Вибух сили»** (містить 500 г креатину та передтрен Bodyperson Formula).",
    "",
    "### 1.5. Шкарпетки та рушники в силових наборах спортивного харчування",
    "- Набір **Nabir_1121 «Чоловіча сила»** (1005 ₴) містить 4 пари шкарпеток (дві чорні, дві білі) разом з банкою креатину. При цьому квіз генерує пояснення: *«без сторонніх речей»*, що викликає здивування та недовіру покупця.",
    "",
    "---",
    "",
    "## 2. Зведена таблиця результатів 100 тест-кейсів",
    "",
    "| № | Назва сценарію покупця | Бюджет | Активність | Клас | Результат двигуна | Вердикт QA | Головна причина / логічний дефект |",
    "|---|------------------------|:------:|:----------:|:----:|:-----------------:|:----------:|-----------------------------------|",
]

for r in runs:
    cid = r["case_id"]
    t = r["title"]
    bud = r["request"].get("max_price_uah", "any")
    act = r["request"].get("activity", "—")
    comp = r["request"].get("component_class", "any")
    status = r["engine_response"]["status"]
    cnt = r["engine_response"]["returned_count"]
    v = r["evaluation"]["verdict"]
    flaws = "; ".join(r["evaluation"]["flaws"]) if r["evaluation"]["flaws"] else "Відповідає логіці тренера"
    if len(flaws) > 100:
        flaws = flaws[:97] + "…"
    report_lines.append(f"| {cid} | {t} | {bud} ₴ | {act} | {comp} | {status} ({cnt}) | **{v}** | {flaws} |")

report_lines.extend([
    "",
    "---",
    "",
    "## 3. Рекомендації для негайного виправлення (Actionable Fixes)",
    "",
    "1. **Виправити маппінг активності в `draft_matcher.py`:**",
    "   У функції `_soft_signals(record, 'activity')` додати розпізнавання `fitness_gym` як відповідності для `strength_training` та `functional_training`, а також зчитувати `all_relevance_signal_groups` з аудиту.",
    "2. **Очистити помилковий клас `creatine_preworkout`:**",
    "   Видалити тег креатину з наборів RE11632 (гриби), RE11663 (йога-килимок), RE11665 (скакалка), RE89489 (рушник), RE11651 (нічний ZMA).",
    "3. **Додати клас `creatine_preworkout` до реальних креатинів:**",
    "   Додати тег до RE11680 (759 ₴), RE11742 (1295 ₴), RE11636, RE11637, RE11783, RE11518, RE11787.",
    "4. **Виключити марафонський набір RE11660 з категорії `training`:**",
    "   Набір з біговими гелями PF 30 Gel має належати виключно до категорії `running`.",
    "5. **Відкоригувати шаблон пояснення `why_suitable`:**",
    "   Прибрати категоричну фразу *«(без сторонніх речей)»*, якщо набір містить шкарпетки, рушники чи сувенірну продукцію клубу."
])

report_path = Path("test-quiz-sandbox/agent_3_report.md")
with open(report_path, "w", encoding="utf-8") as f:
    f.write("\n".join(report_lines))

print(f"Saved human-readable Markdown report to {report_path}")
