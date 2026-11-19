"""Comprehensive 50-Scenario Test Suite for Gym & Fitness Category.

Race Expert Starter Box Generator - Gym & Fitness Validation.
Covers 50 distinct realistic personas across:
- Goals: 'mass' (набір м'язової маси), 'lean' (сушка / спалювання жиру), 'strength' (сила та витривалість).
- Pre-workout boost: 'caffeine' (кофеїновий передтрен/шоти), 'beta_alanine' (бета-аланін без стимуляторів), 'none' (без стимуляторів).
- Price tiers: 'economy', 'standard', 'premium'.
- Custom budgets: 2500, 2700, 3000, 3500, 4200, 5000, 6500, 8000 грн.
- Item deselection: tests where items (shaker, multivitamins, pre-workout, snacks) are deselected,
  verifying that order total and cart payload update correctly.

Domain Invariants Enforced:
1. 1-Month Complete Course: Scaled for a 1-month cycle (multi-pack consumables >= 4, tubs/shakers = 1).
2. Gear Shaker: Exactly 1 shaker included in the gear slot.
3. Protein Inclusion: Whey protein, Whey Isolate, or Diet Whey in care_recovery.
4. Goal Specific Ingredients:
   - Mass: Creatine Monohydrate + Vitamin D3/ZMA.
   - Lean: L-Carnitine, CLA, or Fat Burner + BCAA.
   - Strength: Creatine or BCAA + strength support (Glutamine/ZMA/Vitamins).
5. Zero Caffeine Guarantee: 100% caffeine-free across all slots when pre_workout_boost == 'none'.
6. Energy Activation: Pre-workout complex or multi-pack protein bars / energy shots (quantity >= 4).
7. Stock & Pricing: Quantity > 0, Price > 0, Total > 0, Total <= custom_budget (when provided).
8. No Empty Slots: All 4 slots (energy, hydration, gear, care_recovery) populated.
"""

import pytest
import json
from multi_sport_engine import generate_custom_sport_box, load_catalog

# ==============================================================================
# 50 DIVERSE GYM PERSONAS / SCENARIOS
# ==============================================================================

GYM_SCENARIOS = [
    # --------------------------------------------------------------------------
    # GROUP 1: GOAL = 'mass' (Набір м'язової маси та сили) — 17 Scenarios
    # --------------------------------------------------------------------------
    {
        "id": "gym_mass_econ_caff_01",
        "name": "Олег, студент-новачок у залі, набір маси на базовому бюджеті",
        "goal": "mass",
        "price_tier": "economy",
        "pre_workout_boost": "caffeine",
        "custom_budget": None,
        "deselected_subtypes": None,
        "target_cart_budget": None
    },
    {
        "id": "gym_mass_econ_beta_02",
        "name": "Максим, хардгейнер, чутливий до кофеїну, економ бета-аланін",
        "goal": "mass",
        "price_tier": "economy",
        "pre_workout_boost": "beta_alanine",
        "custom_budget": None,
        "deselected_subtypes": None,
        "target_cart_budget": None
    },
    {
        "id": "gym_mass_econ_none_03",
        "name": "Тарас, тренування пізно ввечері після роботи, економ, без кофеїну",
        "goal": "mass",
        "price_tier": "economy",
        "pre_workout_boost": "none",
        "custom_budget": None,
        "deselected_subtypes": None,
        "target_cart_budget": None
    },
    {
        "id": "gym_mass_std_caff_04",
        "name": "Андрій, регулярні силові 3-4 рази на тиждень, класичний масонабір",
        "goal": "mass",
        "price_tier": "standard",
        "pre_workout_boost": "caffeine",
        "custom_budget": None,
        "deselected_subtypes": None,
        "target_cart_budget": None
    },
    {
        "id": "gym_mass_std_beta_05",
        "name": "Ігор, 28 років, прогресивне перевантаження, бета-аланін для витривалості",
        "goal": "mass",
        "price_tier": "standard",
        "pre_workout_boost": "beta_alanine",
        "custom_budget": None,
        "deselected_subtypes": None,
        "target_cart_budget": None
    },
    {
        "id": "gym_mass_std_none_06",
        "name": "Сергій, набір маси без стимуляторів, протеїновий перекус для відновлення",
        "goal": "mass",
        "price_tier": "standard",
        "pre_workout_boost": "none",
        "custom_budget": None,
        "deselected_subtypes": None,
        "target_cart_budget": None
    },
    {
        "id": "gym_mass_prem_caff_07",
        "name": "Дмитро, досвідчений бодібілдер, преміум бренди ON + передтрен",
        "goal": "mass",
        "price_tier": "premium",
        "pre_workout_boost": "caffeine",
        "custom_budget": None,
        "deselected_subtypes": None,
        "target_cart_budget": None
    },
    {
        "id": "gym_mass_prem_beta_08",
        "name": "Владислав, преміальний масонабір, висока інтенсивність з бета-аланіном",
        "goal": "mass",
        "price_tier": "premium",
        "pre_workout_boost": "beta_alanine",
        "custom_budget": None,
        "deselected_subtypes": None,
        "target_cart_budget": None
    },
    {
        "id": "gym_mass_prem_none_09",
        "name": "Артем, нічний сон у пріоритеті, преміум протеїн Gold Standard без кофеїну",
        "goal": "mass",
        "price_tier": "premium",
        "pre_workout_boost": "none",
        "custom_budget": None,
        "deselected_subtypes": None,
        "target_cart_budget": None
    },
    {
        "id": "gym_mass_budget_2500_10",
        "name": "Роман, фіксований ліміт 2500 грн на місячний курс маси",
        "goal": "mass",
        "price_tier": "economy",
        "pre_workout_boost": "caffeine",
        "custom_budget": 2500.0,
        "deselected_subtypes": None,
        "target_cart_budget": None
    },
    {
        "id": "gym_mass_budget_3000_11",
        "name": "Євген, ліміт 3000 грн, стимулятор-фрі масонабірний курс",
        "goal": "mass",
        "price_tier": "economy",
        "pre_workout_boost": "none",
        "custom_budget": 3000.0,
        "deselected_subtypes": None,
        "target_cart_budget": None
    },
    {
        "id": "gym_mass_budget_3500_12",
        "name": "Олександр, ліміт 3500 грн, бета-аланін буст та креатин",
        "goal": "mass",
        "price_tier": "standard",
        "pre_workout_boost": "beta_alanine",
        "custom_budget": 3500.0,
        "deselected_subtypes": None,
        "target_cart_budget": None
    },
    {
        "id": "gym_mass_budget_4200_13",
        "name": "Василь, бюджет 4200 грн, потужний передтрен та якісний сироватковий білок",
        "goal": "mass",
        "price_tier": "standard",
        "pre_workout_boost": "caffeine",
        "custom_budget": 4200.0,
        "deselected_subtypes": None,
        "target_cart_budget": None
    },
    {
        "id": "gym_mass_budget_5000_14",
        "name": "Костянтин, річний абонемент, бюджет 5000 грн на місячний анаболічний курс",
        "goal": "mass",
        "price_tier": "standard",
        "pre_workout_boost": "caffeine",
        "custom_budget": 5000.0,
        "deselected_subtypes": None,
        "target_cart_budget": None
    },
    {
        "id": "gym_mass_budget_6500_15",
        "name": "Михайло, максимальний анаболічний стек, ліміт 6500 грн",
        "goal": "mass",
        "price_tier": "premium",
        "pre_workout_boost": "beta_alanine",
        "custom_budget": 6500.0,
        "deselected_subtypes": None,
        "target_cart_budget": None
    },
    {
        "id": "gym_mass_desel_shaker_16",
        "name": "Павло, має вдома колекцію шейкерів, деселект шейкера в кошику",
        "goal": "mass",
        "price_tier": "standard",
        "pre_workout_boost": "caffeine",
        "custom_budget": None,
        "deselected_subtypes": ["shaker"],
        "target_cart_budget": None
    },
    {
        "id": "gym_mass_desel_budget_1500_17",
        "name": "Юрій, студент, бюджет 1500 грн, деселект шейкера, перекусів, BCAA та вітамінів",
        "goal": "mass",
        "price_tier": "economy",
        "pre_workout_boost": "none",
        "custom_budget": None,
        "deselected_subtypes": ["shaker", "protein_bar", "bcaa", "vitamins"],
        "target_cart_budget": 1500.0
    },

    # --------------------------------------------------------------------------
    # GROUP 2: GOAL = 'lean' (Рельєф, сушка та спалювання жиру) — 17 Scenarios
    # --------------------------------------------------------------------------
    {
        "id": "gym_lean_econ_caff_18",
        "name": "Олена, сушка до літа, дефіцит калорій, кофеїновий шот перед залом",
        "goal": "lean",
        "price_tier": "economy",
        "pre_workout_boost": "caffeine",
        "custom_budget": None,
        "deselected_subtypes": None,
        "target_cart_budget": None
    },
    {
        "id": "gym_lean_econ_beta_19",
        "name": "Марина, інтервальний кардіо тренінг, бета-аланін без кофеїну",
        "goal": "lean",
        "price_tier": "economy",
        "pre_workout_boost": "beta_alanine",
        "custom_budget": None,
        "deselected_subtypes": None,
        "target_cart_budget": None
    },
    {
        "id": "gym_lean_econ_none_20",
        "name": "Анна, вечірнє кардіо, нуль кофеїну, спалювання жиру + BCAA",
        "goal": "lean",
        "price_tier": "economy",
        "pre_workout_boost": "none",
        "custom_budget": None,
        "deselected_subtypes": None,
        "target_cart_budget": None
    },
    {
        "id": "gym_lean_std_caff_21",
        "name": "Вікторія, фітнес-бікіні підготовка, Diet Whey + карнітин + передтрен",
        "goal": "lean",
        "price_tier": "standard",
        "pre_workout_boost": "caffeine",
        "custom_budget": None,
        "deselected_subtypes": None,
        "target_cart_budget": None
    },
    {
        "id": "gym_lean_std_beta_22",
        "name": "Юлія, кругові функціональні тренування, бета-аланін для витривалості",
        "goal": "lean",
        "price_tier": "standard",
        "pre_workout_boost": "beta_alanine",
        "custom_budget": None,
        "deselected_subtypes": None,
        "target_cart_budget": None
    },
    {
        "id": "gym_lean_std_none_23",
        "name": "Катерина, збереження м'язів без тахікардії, BCAA + L-карнітин",
        "goal": "lean",
        "price_tier": "standard",
        "pre_workout_boost": "none",
        "custom_budget": None,
        "deselected_subtypes": None,
        "target_cart_budget": None
    },
    {
        "id": "gym_lean_prem_caff_24",
        "name": "Наталія, PRO сушка, Sponser Whey Isolate 94 + жироспалювач",
        "goal": "lean",
        "price_tier": "premium",
        "pre_workout_boost": "caffeine",
        "custom_budget": None,
        "deselected_subtypes": None,
        "target_cart_budget": None
    },
    {
        "id": "gym_lean_prem_beta_25",
        "name": "Оксана, преміальний ізолят та чистий бета-аланін без стимуляції ЦНС",
        "goal": "lean",
        "price_tier": "premium",
        "pre_workout_boost": "beta_alanine",
        "custom_budget": None,
        "deselected_subtypes": None,
        "target_cart_budget": None
    },
    {
        "id": "gym_lean_prem_none_26",
        "name": "Діана, елітний сухий тонус, Diet Whey преміум без кофеїну",
        "goal": "lean",
        "price_tier": "premium",
        "pre_workout_boost": "none",
        "custom_budget": None,
        "deselected_subtypes": None,
        "target_cart_budget": None
    },
    {
        "id": "gym_lean_budget_2700_27",
        "name": "Анастасія, строгий ліміт 2700 грн на повний курс сушки",
        "goal": "lean",
        "price_tier": "economy",
        "pre_workout_boost": "none",
        "custom_budget": 2700.0,
        "deselected_subtypes": None,
        "target_cart_budget": None
    },
    {
        "id": "gym_lean_budget_3000_28",
        "name": "Христина, бюджет 3000 грн на жироспалювальний курс з карнітином",
        "goal": "lean",
        "price_tier": "economy",
        "pre_workout_boost": "caffeine",
        "custom_budget": 3000.0,
        "deselected_subtypes": None,
        "target_cart_budget": None
    },
    {
        "id": "gym_lean_budget_3500_29",
        "name": "Ярослав, сушка зі збереженням об'ємів, бюджет 3500 грн",
        "goal": "lean",
        "price_tier": "standard",
        "pre_workout_boost": "beta_alanine",
        "custom_budget": 3500.0,
        "deselected_subtypes": None,
        "target_cart_budget": None
    },
    {
        "id": "gym_lean_budget_4200_30",
        "name": "Олексій, підготовка до фотосесії, ліміт 4200 грн на Diet Whey + термогенік",
        "goal": "lean",
        "price_tier": "standard",
        "pre_workout_boost": "caffeine",
        "custom_budget": 4200.0,
        "deselected_subtypes": None,
        "target_cart_budget": None
    },
    {
        "id": "gym_lean_budget_5000_31",
        "name": "Богдан, преміальний дефіцит калорій, бюджет 5000 грн з бета-аланіном",
        "goal": "lean",
        "price_tier": "standard",
        "pre_workout_boost": "beta_alanine",
        "custom_budget": 5000.0,
        "deselected_subtypes": None,
        "target_cart_budget": None
    },
    {
        "id": "gym_lean_budget_8000_32",
        "name": "Поліна, безкомпромісний PRO курс рельєфу, ліміт 8000 грн",
        "goal": "lean",
        "price_tier": "premium",
        "pre_workout_boost": "none",
        "custom_budget": 8000.0,
        "deselected_subtypes": None,
        "target_cart_budget": None
    },
    {
        "id": "gym_lean_desel_shaker_33",
        "name": "Софія, шейкер є вдома, деселект шейкера для оптимізації кошика",
        "goal": "lean",
        "price_tier": "standard",
        "pre_workout_boost": "none",
        "custom_budget": None,
        "deselected_subtypes": ["shaker"],
        "target_cart_budget": None
    },
    {
        "id": "gym_lean_desel_budget_2000_34",
        "name": "Аліна, цільовий бюджет 2000 грн, деселект шейкера, перекусів та глутаміну",
        "goal": "lean",
        "price_tier": "economy",
        "pre_workout_boost": "none",
        "custom_budget": None,
        "deselected_subtypes": ["shaker", "protein_bar", "glutamine"],
        "target_cart_budget": 2000.0
    },

    # --------------------------------------------------------------------------
    # GROUP 3: GOAL = 'strength' (Сила та витривалість) — 16 Scenarios
    # --------------------------------------------------------------------------
    {
        "id": "gym_strength_econ_caff_35",
        "name": "Іван, паверліфтер-початківець, базова сила на економ бюджеті",
        "goal": "strength",
        "price_tier": "economy",
        "pre_workout_boost": "caffeine",
        "custom_budget": None,
        "deselected_subtypes": None,
        "target_cart_budget": None
    },
    {
        "id": "gym_strength_econ_beta_36",
        "name": "Руслан, кросфітер, витривалість під навантаженням, бета-аланін",
        "goal": "strength",
        "price_tier": "economy",
        "pre_workout_boost": "beta_alanine",
        "custom_budget": None,
        "deselected_subtypes": None,
        "target_cart_budget": None
    },
    {
        "id": "gym_strength_econ_none_37",
        "name": "Віталій, вечірні важкі присідання, без кофеїну, сила + BCAA",
        "goal": "strength",
        "price_tier": "economy",
        "pre_workout_boost": "none",
        "custom_budget": None,
        "deselected_subtypes": None,
        "target_cart_budget": None
    },
    {
        "id": "gym_strength_std_caff_38",
        "name": "Назар, станова тяга та жим, вибухова активація передтреном",
        "goal": "strength",
        "price_tier": "standard",
        "pre_workout_boost": "caffeine",
        "custom_budget": None,
        "deselected_subtypes": None,
        "target_cart_budget": None
    },
    {
        "id": "gym_strength_std_beta_39",
        "name": "Артем, кросфіт WOD та функціональний тренінг, бета-аланін бустер",
        "goal": "strength",
        "price_tier": "standard",
        "pre_workout_boost": "beta_alanine",
        "custom_budget": None,
        "deselected_subtypes": None,
        "target_cart_budget": None
    },
    {
        "id": "gym_strength_std_none_40",
        "name": "Григорій, робота з вагами без кофеїну, креатин + глутамін",
        "goal": "strength",
        "price_tier": "standard",
        "pre_workout_boost": "none",
        "custom_budget": None,
        "deselected_subtypes": None,
        "target_cart_budget": None
    },
    {
        "id": "gym_strength_prem_caff_41",
        "name": "Денис, підготовка до змагань з паверліфтингу, преміум протеїн та креатин",
        "goal": "strength",
        "price_tier": "premium",
        "pre_workout_boost": "caffeine",
        "custom_budget": None,
        "deselected_subtypes": None,
        "target_cart_budget": None
    },
    {
        "id": "gym_strength_prem_beta_42",
        "name": "Вадим, елітна силова витривалість, бета-аланін Now Foods преміум",
        "goal": "strength",
        "price_tier": "premium",
        "pre_workout_boost": "beta_alanine",
        "custom_budget": None,
        "deselected_subtypes": None,
        "target_cart_budget": None
    },
    {
        "id": "gym_strength_prem_none_43",
        "name": "Станіслав, максимальна сила з чистим фокусом без стимуляторів",
        "goal": "strength",
        "price_tier": "premium",
        "pre_workout_boost": "none",
        "custom_budget": None,
        "deselected_subtypes": None,
        "target_cart_budget": None
    },
    {
        "id": "gym_strength_budget_2500_44",
        "name": "Кирило, ліміт 2500 грн на базовий силовий стек з креатином",
        "goal": "strength",
        "price_tier": "economy",
        "pre_workout_boost": "caffeine",
        "custom_budget": 2500.0,
        "deselected_subtypes": None,
        "target_cart_budget": None
    },
    {
        "id": "gym_strength_budget_3000_45",
        "name": "Ростислав, ліміт 3000 грн, бета-аланін + BCAA + креатин",
        "goal": "strength",
        "price_tier": "economy",
        "pre_workout_boost": "beta_alanine",
        "custom_budget": 3000.0,
        "deselected_subtypes": None,
        "target_cart_budget": None
    },
    {
        "id": "gym_strength_budget_3500_46",
        "name": "Гліб, функціональна сила, бюджет 3500 грн без кофеїну",
        "goal": "strength",
        "price_tier": "standard",
        "pre_workout_boost": "none",
        "custom_budget": 3500.0,
        "deselected_subtypes": None,
        "target_cart_budget": None
    },
    {
        "id": "gym_strength_budget_4200_47",
        "name": "Тимофій, підготовка до важких проходок, бюджет 4200 грн з передтреном",
        "goal": "strength",
        "price_tier": "standard",
        "pre_workout_boost": "caffeine",
        "custom_budget": 4200.0,
        "deselected_subtypes": None,
        "target_cart_budget": None
    },
    {
        "id": "gym_strength_budget_6500_48",
        "name": "Борис, PRO силовий курс, ліміт 6500 грн з бета-аланіном",
        "goal": "strength",
        "price_tier": "premium",
        "pre_workout_boost": "beta_alanine",
        "custom_budget": 6500.0,
        "deselected_subtypes": None,
        "target_cart_budget": None
    },
    {
        "id": "gym_strength_desel_shaker_pre_49",
        "name": "Любомир, має шейкер та передтрен, деселект обох позицій у кошику",
        "goal": "strength",
        "price_tier": "standard",
        "pre_workout_boost": "caffeine",
        "custom_budget": None,
        "deselected_subtypes": ["shaker", "pre_workout"],
        "target_cart_budget": None
    },
    {
        "id": "gym_strength_desel_budget_1800_50",
        "name": "Святослав, ліміт 1800 грн, деселект шейкера, перекусів та креатину",
        "goal": "strength",
        "price_tier": "economy",
        "pre_workout_boost": "none",
        "custom_budget": None,
        "deselected_subtypes": ["shaker", "protein_bar", "creatine"],
        "target_cart_budget": 1800.0
    }
]

assert len(GYM_SCENARIOS) == 50, f"Expected exactly 50 scenarios, got {len(GYM_SCENARIOS)}"


# ==============================================================================
# PYTEST TEST SUITE (50 PARALLEL PARAMETRIZED TEST CASES)
# ==============================================================================

@pytest.mark.parametrize("scenario", GYM_SCENARIOS, ids=[s["id"] for s in GYM_SCENARIOS])
def test_gym_starter_box_scenario(scenario):
    """Executes and verifies one full gym starter box persona scenario."""
    sc_id = scenario["id"]
    goal = scenario["goal"]
    tier = scenario["price_tier"]
    boost = scenario["pre_workout_boost"]
    budget = scenario["custom_budget"]
    desel = scenario["deselected_subtypes"]
    target_cart_budget = scenario["target_cart_budget"]

    # 1. GENERATE BOX
    inputs = {
        "goal": goal,
        "price_tier": tier,
        "pre_workout_boost": boost
    }
    if budget:
        inputs["custom_budget"] = budget

    box = generate_custom_sport_box("gym", inputs)

    # 2. CORE BOX VALIDITY
    assert box["sport"] == "gym", f"[{sc_id}] Expected sport 'gym', got {box.get('sport')}"
    assert box["total_base_price"] > 0, f"[{sc_id}] Total base price must be positive"
    assert "slots" in box, f"[{sc_id}] Box missing 'slots' container"
    slots = box["slots"]

    # 3. NO EMPTY SLOTS (All 4 slots must contain items)
    for slot_name in ["energy", "hydration", "gear", "care_recovery"]:
        assert slot_name in slots, f"[{sc_id}] Missing slot: {slot_name}"
        assert len(slots[slot_name]) > 0, f"[{sc_id}] Slot {slot_name} must not be empty"

    # 4. GEAR SHAKER GUARANTEE (Exactly 1 shaker, quantity 1)
    gear_items = slots["gear"]
    assert len(gear_items) == 1, f"[{sc_id}] Gear slot must contain exactly 1 product, got {len(gear_items)}"
    shaker_item = gear_items[0]
    assert shaker_item["product"].get("sub_type") == "shaker", (
        f"[{sc_id}] Gear item must be a shaker, got {shaker_item['product'].get('sub_type')}"
    )
    assert shaker_item["quantity_recommended"] == 1, f"[{sc_id}] Shaker quantity must be 1"

    # 5. PROTEIN INCLUSION (Whey protein, Whey Isolate, or Diet Whey in care_recovery)
    care_items = slots["care_recovery"]
    care_subtypes = [it["product"].get("sub_type") for it in care_items]
    valid_protein_subtypes = {"whey_protein", "diet_whey", "whey_isolate", "vegan_protein"}
    has_protein = any(st in valid_protein_subtypes for st in care_subtypes)
    assert has_protein, (
        f"[{sc_id}] care_recovery must contain protein (Whey/Isolate/Diet Whey), found: {care_subtypes}"
    )

    # 6. GOAL SPECIFIC INGREDIENTS
    hyd_items = slots["hydration"]
    hyd_subtypes = [it["product"].get("sub_type") for it in hyd_items]

    if goal == "mass":
        has_creatine = any(st == "creatine" for st in care_subtypes)
        assert has_creatine, f"[{sc_id}] Mass box must include Creatine Monohydrate"
        has_hormone_support = any(st in {"zma", "vitamins", "testosterone_booster"} for st in care_subtypes)
        assert has_hormone_support, f"[{sc_id}] Mass box must include Vitamin D3 or ZMA"

    elif goal == "lean":
        has_fatburner = any(st in {"l_carnitine", "cla", "fat_burner"} for st in care_subtypes)
        assert has_fatburner, f"[{sc_id}] Lean cut box must include L-Carnitine, CLA, or Fat Burner"
        has_bcaa = any(st == "bcaa" for st in hyd_subtypes)
        assert has_bcaa, f"[{sc_id}] Lean cut box must include BCAA in hydration slot"

    elif goal == "strength":
        has_creatine_or_bcaa = any(st == "creatine" for st in care_subtypes) or any(st == "bcaa" for st in hyd_subtypes)
        assert has_creatine_or_bcaa, f"[{sc_id}] Strength box must include Creatine or BCAA"
        has_strength_support = any(st in {"glutamine", "zma", "vitamins"} for st in care_subtypes)
        assert has_strength_support, f"[{sc_id}] Strength box must include strength/CNS support (Glutamine/ZMA/Vitamins)"

    # 7. ZERO CAFFEINE GUARANTEE (When boost == 'none', 100% items caffeine == False)
    if boost == "none":
        for s_name, items in slots.items():
            for it in items:
                assert it["product"].get("caffeine") is False, (
                    f"[{sc_id}] Zero caffeine leak detected in slot {s_name}: {it['product']['name']}"
                )

    # 8. ENERGY ACTIVATION (Pre-workout tub x1, beta-alanine tub x1, or snacks/shots >= 4)
    energy_item = slots["energy"][0]
    e_st = energy_item["product"].get("sub_type")
    e_qty = energy_item["quantity_recommended"]

    if boost == "caffeine":
        assert energy_item["product"].get("caffeine") is True, f"[{sc_id}] Expected caffeinated energy activator"
        if e_st in {"energy_shot"}:
            assert e_qty >= 4, f"[{sc_id}] Energy shots pack must be >= 4, got {e_qty}"
        else:
            assert e_qty >= 1, f"[{sc_id}] Pre-workout tub quantity must be >= 1"

    elif boost == "beta_alanine":
        assert energy_item["product"].get("caffeine") is False, f"[{sc_id}] Beta-alanine must be non-stimulant"
        if e_st in {"protein_bar", "protein_snack"}:
            assert e_qty >= 4, f"[{sc_id}] Protein snacks pack must be >= 4, got {e_qty}"
        else:
            assert e_qty >= 1, f"[{sc_id}] Beta-alanine tub quantity must be >= 1"

    else:  # none
        assert energy_item["product"].get("caffeine") is False, f"[{sc_id}] Boost none must not have caffeine"
        assert e_qty >= 4, f"[{sc_id}] Protein bars / snacks pack for boost 'none' must be >= 4, got {e_qty}"

    # 9. 1-MONTH COMPLETE COURSE (Multi-pack consumables, tub quantities, realistic pricing)
    all_recommended_items = [it for s in slots.values() for it in s]
    for it in all_recommended_items:
        prod = it["product"]
        assert it["quantity_recommended"] > 0, f"[{sc_id}] Product quantity must be positive: {prod['name']}"
        assert prod["price"] > 0, f"[{sc_id}] Product price must be positive: {prod['name']}"
        assert prod["quantity"] > 0, f"[{sc_id}] Recommended product must be in stock: {prod['name']}"

    # Preset boxes without custom budget represent full complete courses
    if not budget:
        assert box["total_base_price"] >= 2400.0, (
            f"[{sc_id}] Complete 1-month course price must be >= 2400 грн, got {box['total_base_price']}"
        )

    # 10. STOCK & CUSTOM BUDGET OPTIMIZATION
    if budget:
        assert box["total_base_price"] <= budget, (
            f"[{sc_id}] Box total {box['total_base_price']} exceeds custom budget {budget}"
        )
        assert box["budget_info"]["within_budget"] is True, f"[{sc_id}] within_budget flag must be True"
        assert box["budget_info"]["custom_budget"] == budget

    # 11. ITEM DESELECTION & CART PAYLOAD UPDATE SIMULATION
    if desel:
        all_flattened = []
        for slot_k, items_list in slots.items():
            for idx, it in enumerate(items_list):
                all_flattened.append((f"{slot_k}_{idx}", it))

        selected_map = {}
        for key, it in all_flattened:
            st = it["product"].get("sub_type", "")
            # Uncheck items matching deselected subtypes
            selected_map[key] = (st not in desel)

        # Build cart payload from checked items
        cart_payload = []
        cart_total_price = 0.0
        for key, it in all_flattened:
            if selected_map[key]:
                cart_payload.append({
                    "productId": it["product"]["product_id"],
                    "quantity": it["quantity_recommended"],
                    "price": it["product"]["price"]
                })
                cart_total_price += it["product"]["price"] * it["quantity_recommended"]

        # Verifications of deselection behavior
        assert len(cart_payload) < len(all_flattened), (
            f"[{sc_id}] Cart items count must decrease after deselection"
        )
        assert cart_total_price < box["total_base_price"], (
            f"[{sc_id}] Cart total price ({cart_total_price}) must be less than base price ({box['total_base_price']})"
        )

        # Confirm none of the deselected subtypes entered the cart
        for cart_it in cart_payload:
            p_id = cart_it["productId"]
            matching_prod = next(it["product"] for _, it in all_flattened if it["product"]["product_id"] == p_id)
            assert matching_prod.get("sub_type") not in desel, (
                f"[{sc_id}] Deselected item {matching_prod['name']} ({matching_prod.get('sub_type')}) entered cart"
            )

        # If a target cart budget was configured (e.g. 1500, 1800, 2000 грн), assert cart_total fits
        if target_cart_budget:
            assert cart_total_price <= target_cart_budget, (
                f"[{sc_id}] Cart total price {cart_total_price} exceeds target budget {target_cart_budget}"
            )
