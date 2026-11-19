"""Comprehensive 50-Scenario Test Suite for Outdoor & Hiking (ЇDLO) Starter Box Generator.

Validates 50 distinct, realistic, highly diverse outdoor personas across:
- Duration / Format: 'weekend' (2-3 days) vs 'expedition' (4+ days autonomous)
- Season / Weather: 'warm' / 'summer' vs 'cold' / 'alpine' / 'winter'
- Dietary preferences: standard vs vegetarian/vegan
- Price tiers: 'economy', 'standard', 'premium'
- Custom budgets: 1200, 1800, 2500, 3200, 3500, 4000, 5000, 6500, 8000 грн
- Item deselection: verifying order total and cart payload update correctly

Domain Validations Enforced:
1. ЇDLO Hot Meals Complete Pack:
   - Weekend: at least 6 hot meals (breakfasts, gourmet soups, main dishes) + meat jerkies / energy snacks.
   - Expedition: at least 8-12 hot meals + 6-8 packs of jerkies/snacks.
2. Gear Slot:
   - Trekking socks with available_sizes (1 pair for weekend, 2 pairs for expedition).
   - Soft flask or outdoor water bottle included.
3. Hydration Slot:
   - Electrolyte drink tablets / hydration mix present.
4. Care & Recovery Slot:
   - Magnesium ampoules / recovery pack for muscle relaxation after long ascents.
5. Stock & Pricing:
   - All recommended products have quantity > 0, price > 0, total_base_price > 0.
   - total_base_price <= custom_budget when custom_budget is provided.
6. No Empty Slots:
   - Every slot (energy, hydration, gear, care_recovery) must contain items.
"""

import pytest
from multi_sport_engine import generate_custom_sport_box

MEAT_KEYWORDS = ["індич", "ялович", "куряч", "джерки", "креветк", "по-флотськи"]

SCENARIOS = [
    # =========================================================================
    # GROUP 1: Weekend Hikes — Standard Nutrition (Scenarios 1 - 10)
    # =========================================================================
    {
        "id": 1,
        "name": "Borzhava Autumn Ridge (Standard, Cold)",
        "persona": "Андрій, вихідні на Боржаві пізньої осені, холодний вітер, стандартний бюджет, зігріваючий раціон",
        "inputs": {"duration": "weekend", "weather": "cold", "dietary": "standard", "price_tier": "standard"},
    },
    {
        "id": 2,
        "name": "Pip Ivan Summer Sunrise (Standard, Warm)",
        "persona": "Оксана, літній світанок на Піп Івані Чорногірському, тепла погода, електроліти та супи",
        "inputs": {"duration": "weekend", "weather": "warm", "dietary": "standard", "price_tier": "standard"},
    },
    {
        "id": 3,
        "name": "Gorgany Boulder Ridge (Economy, Moderate)",
        "persona": "Тарас, кам'яні розсипи (греготи) Горган, економ-бюджет, міцні трекінгові шкарпетки",
        "inputs": {"duration": "weekend", "weather": "moderate", "dietary": "standard", "price_tier": "economy"},
    },
    {
        "id": 4,
        "name": "Marmarosy Alps Scramble (Premium, Cold)",
        "persona": "Ярослав, технічний трек Мармароськими Альпами, преміум-бокс, бальзам від мозолів",
        "inputs": {"duration": "weekend", "weather": "cold", "dietary": "standard", "price_tier": "premium"},
    },
    {
        "id": 5,
        "name": "Skole Beskids Valley Camping (Economy, Warm)",
        "persona": "Ірина, сімейний кемпінг у Сколівських Бескидах, тепла весна, базовий економ-набір",
        "inputs": {"duration": "weekend", "weather": "warm", "dietary": "standard", "price_tier": "economy"},
    },
    {
        "id": 6,
        "name": "Dzharylhach Coastal Sand Trek (Premium, Warm)",
        "persona": "Дмитро, піщаний автономний перехід островом Джарилгач, спека, PRO гідратація",
        "inputs": {"duration": "weekend", "weather": "warm", "dietary": "standard", "price_tier": "premium"},
    },
    {
        "id": 7,
        "name": "Hoverla & Petros Ridge Climb (Standard, Cold)",
        "persona": "Михайло, сходження на Говерлу та Петрос, мінлива холодна погода, борщ та джерки",
        "inputs": {"duration": "weekend", "weather": "cold", "dietary": "standard", "price_tier": "standard"},
    },
    {
        "id": 8,
        "name": "Kamyanka Waterfalls Fastpack (Standard, Warm)",
        "persona": "Катерина, фастпакінг уздовж річки Кам'янка, теплий вікенд, легка фляга CASNO",
        "inputs": {"duration": "weekend", "weather": "warm", "dietary": "standard", "price_tier": "standard"},
    },
    {
        "id": 9,
        "name": "Bukovel Wild Off-Grid Weekend (Economy, Cold)",
        "persona": "Богдан, дикі стежки навколо Буковелю, перші приморозки, економне гаряче харчування",
        "inputs": {"duration": "weekend", "weather": "cold", "dietary": "standard", "price_tier": "economy"},
    },
    {
        "id": 10,
        "name": "Synevyr Glade Comfort Camp (Premium, Moderate)",
        "persona": "Сергій, кемпінг на галявинах Синевиру, комфортний преміум вікенд із карпатським чаєм",
        "inputs": {"duration": "weekend", "weather": "moderate", "dietary": "standard", "price_tier": "premium"},
    },

    # =========================================================================
    # GROUP 2: Weekend Hikes — Vegetarian / Vegan Personas (Scenarios 11 - 20)
    # =========================================================================
    {
        "id": 11,
        "name": "Borzhava Vegan Blueberry Ridge (Standard, Warm)",
        "persona": "Марина, веган-чорничний хайкінг Боржавою, тепле літо, гречка з веганськими мітболами",
        "inputs": {"duration": "weekend", "weather": "warm", "dietary": "vegan", "price_tier": "standard"},
    },
    {
        "id": 12,
        "name": "Winter Gorgany Vegetarian Snowshoe (Standard, Cold)",
        "persona": "Олексій, зимовий похід на снігоступах Горганами, вегетаріанець, крем-суп з грибами",
        "inputs": {"duration": "weekend", "weather": "cold", "dietary": "vegetarian", "price_tier": "standard"},
    },
    {
        "id": 13,
        "name": "Beskids Plant-Based Weekend (Economy, Moderate)",
        "persona": "Юлія, легкий рослинний вікенд у Бескидах, помірна погода, економний кус-кус",
        "inputs": {"duration": "weekend", "weather": "moderate", "dietary": "vegan", "price_tier": "economy"},
    },
    {
        "id": 14,
        "name": "Pip Ivan Alpine Vegan Camp (Premium, Cold)",
        "persona": "Василь, високогірний табір біля Піп Івана, преміум веган-раціон, бананова каша й горіхи",
        "inputs": {"duration": "weekend", "weather": "cold", "dietary": "vegan", "price_tier": "premium"},
    },
    {
        "id": 15,
        "name": "Chornohora Lakes Vegetarian Trail (Standard, Warm)",
        "persona": "Олена, похід озерами Чорногори, вегетаріанка, літня спека, мінералізація води",
        "inputs": {"duration": "weekend", "weather": "warm", "dietary": "vegetarian", "price_tier": "standard"},
    },
    {
        "id": 16,
        "name": "Marmarosy Flora Exploration Vegan (Economy, Warm)",
        "persona": "Назар, ботанічна експедиція Мармаросами, рослинний раціон, базовий економ-бокс",
        "inputs": {"duration": "weekend", "weather": "warm", "dietary": "vegan", "price_tier": "economy"},
    },
    {
        "id": 17,
        "name": "Carpathian Ridge Vegan Solo (Premium, Warm)",
        "persona": "Ігор, сольний веган-траверс хребта, преміальний захисний крем і рослинне відновлення",
        "inputs": {"duration": "weekend", "weather": "warm", "dietary": "vegan", "price_tier": "premium"},
    },
    {
        "id": 18,
        "name": "Yavirnyk Autumn Vegetarian Camp (Economy, Cold)",
        "persona": "Христина, осінній вегетаріанський табір на Явірнику, холодні ночі, гарячий карпатський чай",
        "inputs": {"duration": "weekend", "weather": "cold", "dietary": "vegetarian", "price_tier": "economy"},
    },
    {
        "id": 19,
        "name": "Svydivsky Lakes Vegan Fastpack (Standard, Cold)",
        "persona": "Роман, швидкісний веган-фастпакінг Свидовецькими озерами, прохолодна погода",
        "inputs": {"duration": "weekend", "weather": "cold", "dietary": "vegan", "price_tier": "standard"},
    },
    {
        "id": 20,
        "name": "Dostupni Karpaty Zero-Meat Weekend (Premium, Moderate)",
        "persona": "Анна, інклюзивний проект 'Доступні Карпати', преміум безм'ясний поживний раціон",
        "inputs": {"duration": "weekend", "weather": "moderate", "dietary": "vegan", "price_tier": "premium"},
    },

    # =========================================================================
    # GROUP 3: Multi-Day Mountain Expeditions — Standard (Scenarios 21 - 30)
    # =========================================================================
    {
        "id": 21,
        "name": "Trans-Carpathian 5-Day Grand Traverse (Standard, Warm)",
        "persona": "Віктор, 5-денний Гранд-траверс Закарпаття, автономний перехід, 12 гарячих страв ЇDLO",
        "inputs": {"duration": "expedition", "weather": "warm", "dietary": "standard", "price_tier": "standard"},
    },
    {
        "id": 22,
        "name": "Chornohora-Gorgany 6-Day Extreme Traverse (Premium, Cold)",
        "persona": "Максим, екстремальний 6-денний перехід Чорногора-Горгани, морозний вітер, PRO екіпірування",
        "inputs": {"duration": "expedition", "weather": "cold", "dietary": "standard", "price_tier": "premium"},
    },
    {
        "id": 23,
        "name": "Marmarosy 4-Day Alpine Autonomous Trek (Economy, Cold)",
        "persona": "Артем, 4-денний автономний альпійський трек Мармаросами, економний експедиційний раціон",
        "inputs": {"duration": "expedition", "weather": "cold", "dietary": "standard", "price_tier": "economy"},
    },
    {
        "id": 24,
        "name": "Svydovets Ridge 5-Day Autonomous (Standard, Warm)",
        "persona": "Павло, 5 днів на хребті Свидовець, спекотне літо, подвійна гідратація та 7 упаковок перекусів",
        "inputs": {"duration": "expedition", "weather": "warm", "dietary": "standard", "price_tier": "standard"},
    },
    {
        "id": 25,
        "name": "Carpathian Wild Bear Trails 7-Day PRO (Premium, Warm)",
        "persona": "Денис, 7-денна експедиція дикими ведмежими куточками Карпат, преміум-набір ЇDLO",
        "inputs": {"duration": "expedition", "weather": "warm", "dietary": "standard", "price_tier": "premium"},
    },
    {
        "id": 26,
        "name": "Autumn Beskids 4-Day Ridge Backpacking (Economy, Moderate)",
        "persona": "Надія, 4-денний осінній бекпекінг Бескидами, волога погода, сухе табірне спорядження",
        "inputs": {"duration": "expedition", "weather": "moderate", "dietary": "standard", "price_tier": "economy"},
    },
    {
        "id": 27,
        "name": "Deep Gorgany Cedar Forest 5-Day Traverse (Standard, Cold)",
        "persona": "Степан, 5 днів крізь кедрові праліси Горган, кам'яні осипи, подвійні шкарпетки",
        "inputs": {"duration": "expedition", "weather": "cold", "dietary": "standard", "price_tier": "standard"},
    },
    {
        "id": 28,
        "name": "Winter High Ridge Sub-Zero Alpine Expedition (Premium, Cold)",
        "persona": "Юрій, зимова високогірна автономна експедиція, мінусова температура, 4 ампули магнію",
        "inputs": {"duration": "expedition", "weather": "cold", "dietary": "standard", "price_tier": "premium"},
    },
    {
        "id": 29,
        "name": "Ukrainian Boundary Trail 6-Day Thru-Hike (Standard, Warm)",
        "persona": "Олександр, 6 днів Українським Карпатським Шляхом, літо, енергетичний запас",
        "inputs": {"duration": "expedition", "weather": "warm", "dietary": "standard", "price_tier": "standard"},
    },
    {
        "id": 30,
        "name": "Late Fall Sub-Zero Autonomous Expedition (Economy, Cold)",
        "persona": "Григорій, пізньоосіння експедиція з мінусовими ночівлями, економне автономне харчування",
        "inputs": {"duration": "expedition", "weather": "cold", "dietary": "standard", "price_tier": "economy"},
    },

    # =========================================================================
    # GROUP 4: Multi-Day Mountain Expeditions — Vegetarian / Vegan (Scenarios 31 - 38)
    # =========================================================================
    {
        "id": 31,
        "name": "5-Day Chornohora Vegan High Traverse (Standard, Warm)",
        "persona": "Дарина, 5-денний веганський траверс Чорногори, 12 гарячих рослинних страв, горіхи",
        "inputs": {"duration": "expedition", "weather": "warm", "dietary": "vegan", "price_tier": "standard"},
    },
    {
        "id": 32,
        "name": "Gorgany 4-Day Plant-Powered Boulder Trek (Economy, Cold)",
        "persona": "Лев, 4 дні кам'яними горганами на рослинному паливі, економ-бюджет, грибні крем-супи",
        "inputs": {"duration": "expedition", "weather": "cold", "dietary": "vegan", "price_tier": "economy"},
    },
    {
        "id": 33,
        "name": "Marmarosy 6-Day Alpine Vegetarian Expedition (Premium, Cold)",
        "persona": "Світлана, 6-денна альпійська вегетаріанська експедиція Мармаросами, преміум-захист стоп",
        "inputs": {"duration": "expedition", "weather": "cold", "dietary": "vegetarian", "price_tier": "premium"},
    },
    {
        "id": 34,
        "name": "Svydovets 5-Day Solar Vegan Thru-Hike (Standard, Warm)",
        "persona": "Євген, 5 днів сонячного Свидовця, веган-раціон, ізотонічні таблетки проти зневоднення",
        "inputs": {"duration": "expedition", "weather": "warm", "dietary": "vegan", "price_tier": "standard"},
    },
    {
        "id": 35,
        "name": "Borzhava to Gorgany Vegan Traverse (Premium, Warm)",
        "persona": "Аліна, зв'язка Боржава-Горгани 5 днів, рослинний раціон, преміальне відновлення",
        "inputs": {"duration": "expedition", "weather": "warm", "dietary": "vegan", "price_tier": "premium"},
    },
    {
        "id": 36,
        "name": "Autonomous Carpathian Vegan Solitude 4-Day (Economy, Warm)",
        "persona": "Володимир, 4 дні наодинці з дикою природою, рослинний економ-бокс, кус-кус та вівсянка",
        "inputs": {"duration": "expedition", "weather": "warm", "dietary": "vegan", "price_tier": "economy"},
    },
    {
        "id": 37,
        "name": "Winter Chornohora Vegetarian Snow Camp 4-Day (Standard, Cold)",
        "persona": "Анастасія, зимовий сніговий табір на Чорногорі 4 дні, вегетаріанське зігріваюче меню",
        "inputs": {"duration": "expedition", "weather": "cold", "dietary": "vegetarian", "price_tier": "standard"},
    },
    {
        "id": 38,
        "name": "Ultra-Autonomous Plant-Based Expedition (Premium, Moderate)",
        "persona": "Костянтин, автономна транс-карпатська експедиція на суворо рослинній дієті, преміум",
        "inputs": {"duration": "expedition", "weather": "moderate", "dietary": "vegan", "price_tier": "premium"},
    },

    # =========================================================================
    # GROUP 5: Custom Budget Engine Optimizations (Scenarios 39 - 44)
    # =========================================================================
    {
        "id": 39,
        "name": "Weekend Budget Cap 3200 грн (Strict Economy Weekend)",
        "persona": "Петро, суворий бюджет 3200 грн на вікенд у Карпатах, оптимізація базового набору",
        "inputs": {"duration": "weekend", "weather": "moderate", "dietary": "standard", "custom_budget": 3200.0},
    },
    {
        "id": 40,
        "name": "Weekend Budget Cap 3500 грн (Carpathian Fast Weekend)",
        "persona": "Марко, швидкий вікенд із лімітом 3500 грн, літня спека, повний комплект ЇDLO",
        "inputs": {"duration": "weekend", "weather": "warm", "dietary": "standard", "custom_budget": 3500.0},
    },
    {
        "id": 41,
        "name": "Weekend Budget Cap 4000 грн (Optimal Hiking Budget)",
        "persona": "Тетяна, вегетаріанський вікенд із бюджетом 4000 грн, холодні осінні ночі, грибний суп",
        "inputs": {"duration": "weekend", "weather": "cold", "dietary": "vegetarian", "custom_budget": 4000.0},
    },
    {
        "id": 42,
        "name": "Weekend Budget Cap 5000 грн (Generous Comfort Weekend)",
        "persona": "Валентин, веган-вікенд із бюджетом 5000 грн, максимальний комфорт і відновлення",
        "inputs": {"duration": "weekend", "weather": "warm", "dietary": "vegan", "custom_budget": 5000.0},
    },
    {
        "id": 43,
        "name": "Expedition Budget Cap 6500 грн (Standard 4-Day Thru-Hike)",
        "persona": "Руслан, автономна експедиція на 4 дні з лімітом 6500 грн, повноцінні 12 гарячих обідів",
        "inputs": {"duration": "expedition", "weather": "moderate", "dietary": "standard", "custom_budget": 6500.0},
    },
    {
        "id": 44,
        "name": "Expedition Budget Cap 8000 грн (High-End Autonomous PRO Pack)",
        "persona": "Антон, автономний PRO-пак на експедицію з бюджетом 8000 грн, преміум-екіпірування",
        "inputs": {"duration": "expedition", "weather": "cold", "dietary": "vegan", "custom_budget": 8000.0},
    },

    # =========================================================================
    # GROUP 6: Item Deselection & Dynamic Cart Customization (Scenarios 45 - 50)
    # =========================================================================
    {
        "id": 45,
        "name": "Weekend Hiker with Own Socks (Gear Deselection, Target 3300 грн)",
        "persona": "Захар, досвідчений хайкер із власними термошкарпетками (деселекція шкарпеток, таргет 3300 грн)",
        "inputs": {"duration": "weekend", "weather": "moderate", "dietary": "standard", "price_tier": "standard"},
        "deselection": {"deselect_subtypes": ["trekking_socks"], "target_budget": 3300.0},
    },
    {
        "id": 46,
        "name": "Weekend Hiker with Own Flask & Bottle (Hydration Gear Deselection, Target 3400 грн)",
        "persona": "Зоя, веганка з власною м'якою флягою та пляшкою (деселекція фляги/пляшки, таргет 3400 грн)",
        "inputs": {"duration": "weekend", "weather": "warm", "dietary": "vegan", "price_tier": "standard"},
        "deselection": {"deselect_subtypes": ["water_bottle", "soft_flask"], "target_budget": 3400.0},
    },
    {
        "id": 47,
        "name": "Expedition Veteran with Complete Gear & Balm (Target Budget 5000 грн)",
        "persona": "Вадим, ветеран гір із повним спорядженням та мазями (деселекція спорядження, таргет 5000 грн)",
        "inputs": {"duration": "expedition", "weather": "cold", "dietary": "standard", "price_tier": "standard"},
        "deselection": {"deselect_subtypes": ["trekking_socks", "soft_flask", "anti_chafe_balm"], "target_budget": 5000.0},
    },
    {
        "id": 48,
        "name": "Food-Only Trail Restock (Target Budget 2500 грн, Gear & Recovery Deselected)",
        "persona": "Юліан, поповнення суто провізії на трейлі (деселекція спорядження та догляду, таргет 2500 грн)",
        "inputs": {"duration": "weekend", "weather": "warm", "dietary": "standard", "price_tier": "economy"},
        "deselection": {"deselect_slots": ["gear", "care_recovery"], "target_budget": 2500.0},
    },
    {
        "id": 49,
        "name": "Ultra-Light Summit Push (Target Budget 1800 грн, Deselect Gear & Hydration)",
        "persona": "Семен, ультралегкий штурмовий вихід (деселекція спорядження та гідратації, таргет 1800 грн)",
        "inputs": {"duration": "weekend", "weather": "moderate", "dietary": "vegan", "price_tier": "economy"},
        "deselection": {"deselect_slots": ["gear", "hydration"], "target_budget": 1800.0},
    },
    {
        "id": 50,
        "name": "Minimalist Trail Lunch Pack (Target Budget 1200 грн, Food-Only Deselection)",
        "persona": "Данило, мінімалістичний денний табірний пак їжі (деселекція усього крім їжі, таргет 1200 грн)",
        "inputs": {"duration": "weekend", "weather": "cold", "dietary": "standard", "price_tier": "economy"},
        "deselection": {"keep_only_subtypes": ["gourmet_meal", "gourmet_soup", "breakfast_meal"], "target_budget": 1200.0},
    },
]


@pytest.mark.parametrize("scenario", SCENARIOS, ids=[f"Scenario_{s['id']:02d}_{s['name'].replace(' ', '_').replace('/', '_')}" for s in SCENARIOS])
def test_outdoor_scenario(scenario):
    """Validate each of the 50 outdoor personas against crucial domain rules."""
    inputs = scenario["inputs"]
    duration = inputs.get("duration", "weekend")
    dietary = inputs.get("dietary", "standard")
    is_vegan = dietary in ["vegan", "vegetarian", "plant_based"]

    box = generate_custom_sport_box("outdoor", inputs)

    # 1. Basic Structure
    assert box["sport"] == "outdoor", f"Expected sport 'outdoor', got {box.get('sport')}"
    assert box["total_base_price"] > 0, "Total base price must be > 0"

    slots = box["slots"]

    # 2. No Empty Slots
    for slot_name in ["energy", "hydration", "gear", "care_recovery"]:
        assert len(slots.get(slot_name, [])) > 0, f"Slot '{slot_name}' cannot be empty"

    # 3. Stock, Pricing & Quantities
    all_slot_items = [it for s_items in slots.values() for it in s_items]
    for it in all_slot_items:
        prod = it["product"]
        assert prod["quantity"] > 0, f"Product {prod['name']} has stock <= 0"
        assert prod["price"] > 0, f"Product {prod['name']} has price <= 0"
        assert it["quantity_recommended"] > 0, f"Recommended quantity <= 0 for {prod['name']}"

    # 4. Custom Budget Cap Verification (when provided in inputs)
    if inputs.get("custom_budget"):
        budget = inputs["custom_budget"]
        assert box["total_base_price"] <= budget, (
            f"Box price {box['total_base_price']} exceeds custom budget {budget}"
        )
        assert box["budget_info"]["within_budget"] is True

    # 5. ЇDLO Hot Meals Complete Pack
    hot_meal_subtypes = ["breakfast_meal", "gourmet_soup", "gourmet_meal"]
    hot_meals = [it for it in slots["energy"] if it["product"].get("sub_type") in hot_meal_subtypes]
    total_hot_meals_count = sum(it["quantity_recommended"] for it in hot_meals)

    # Jerkies and snacks
    jerkies_care = sum(it["quantity_recommended"] for it in slots["care_recovery"] if it["product"].get("sub_type") in ["jerky", "recovery_porridge"])
    energy_snacks = sum(it["quantity_recommended"] for it in slots["energy"] if it["product"].get("sub_type") in ["energy_snack", "energy_bar"])
    care_snacks = sum(it["quantity_recommended"] for it in slots["care_recovery"] if it["product"].get("sub_type") in ["energy_snack", "energy_bar"])
    total_snacks_count = jerkies_care + energy_snacks + care_snacks

    if duration == "weekend":
        assert total_hot_meals_count >= 6, (
            f"Weekend hike requires at least 6 hot meals (breakfasts, soups, mains), got {total_hot_meals_count}"
        )
        assert total_snacks_count >= 3, (
            f"Weekend hike requires at least 3 packs of jerkies/energy snacks, got {total_snacks_count}"
        )
    elif duration == "expedition":
        assert total_hot_meals_count >= 8, (
            f"Expedition requires at least 8-12 hot meals, got {total_hot_meals_count}"
        )
        assert total_snacks_count >= 6, (
            f"Expedition requires 6-8 packs of jerkies/energy snacks, got {total_snacks_count}"
        )

    # 6. GEAR SLOT Validations
    gear_items = slots["gear"]
    gear_subtypes = [it["product"].get("sub_type") for it in gear_items]

    # Trekking socks with available_sizes
    assert "trekking_socks" in gear_subtypes, "Gear slot must include trekking socks"
    sock_item = next(it for it in gear_items if it["product"].get("sub_type") == "trekking_socks")
    expected_sock_qty = 2 if (duration == "expedition" or inputs.get("price_tier") == "premium") else 1
    assert sock_item["quantity_recommended"] >= expected_sock_qty, (
        f"Expected at least {expected_sock_qty} pairs of socks for {duration}, got {sock_item['quantity_recommended']}"
    )
    sizes = sock_item.get("available_sizes", [])
    assert len(sizes) >= 3, f"Trekking socks must offer size selection, got {sizes}"
    assert any(s["size"] == "40-42" for s in sizes), "Sizes must include standard 40-42"

    # Soft flask or water bottle
    assert any(st in ["soft_flask", "water_bottle"] for st in gear_subtypes), (
        "Gear slot must include soft flask or outdoor water bottle"
    )

    # 7. HYDRATION Validations
    hydration_subtypes = [it["product"].get("sub_type") for it in slots["hydration"]]
    assert "electrolyte_tablets" in hydration_subtypes, (
        "Hydration slot must contain electrolyte drink tablets for mineral balance"
    )

    # 8. CARE & RECOVERY Validations
    care_subtypes = [it["product"].get("sub_type") for it in slots["care_recovery"]]
    assert "magnesium" in care_subtypes, (
        "Care & recovery slot must include magnesium ampoules for anti-cramp muscle relaxation"
    )

    # 9. Dietary Safety Guarantee (Vegan / Vegetarian)
    if is_vegan:
        for it in all_slot_items:
            prod_name = it["product"]["name"].lower()
            prod_sub = it["product"].get("sub_type")
            assert prod_sub != "jerky", f"Meat jerky leak in vegan/vegetarian box: {it['product']['name']}"
            for kw in MEAT_KEYWORDS:
                assert kw not in prod_name, f"Meat ingredient '{kw}' detected in vegan box product '{it['product']['name']}'"

    # 10. Item Deselection & Dynamic Cart Simulation (for scenarios with deselection)
    if "deselection" in scenario:
        desel = scenario["deselection"]
        all_indexed_items = []
        for sname in ["energy", "hydration", "gear", "care_recovery"]:
            for i, it in enumerate(slots.get(sname, [])):
                all_indexed_items.append((sname, f"{sname}_{i}", it))

        original_total = sum(it["product"]["price"] * it["quantity_recommended"] for _, _, it in all_indexed_items)
        assert round(original_total, 2) == round(box["total_base_price"], 2)

        cart_items = []
        cart_total = 0.0

        for sname, _, it in all_indexed_items:
            st = it["product"].get("sub_type")
            keep = True
            if "deselect_subtypes" in desel and st in desel["deselect_subtypes"]:
                keep = False
            if "deselect_slots" in desel and sname in desel["deselect_slots"]:
                keep = False
            if "keep_only_subtypes" in desel and st not in desel["keep_only_subtypes"]:
                keep = False

            if keep:
                cart_items.append({
                    "productId": it["product"]["product_id"],
                    "quantity": it["quantity_recommended"],
                    "price": it["product"]["price"],
                    "sub_type": st,
                })
                cart_total += it["product"]["price"] * it["quantity_recommended"]

        cart_total = round(cart_total, 2)

        # Confirm deselection effects
        assert len(cart_items) < len(all_indexed_items), "Cart should contain fewer items after deselection"
        assert cart_total < original_total, f"Cart total {cart_total} must be lower than original {original_total}"

        # Verify deselected items are completely omitted from cart payload
        if "deselect_subtypes" in desel:
            for desel_st in desel["deselect_subtypes"]:
                assert not any(it["sub_type"] == desel_st for it in cart_items), (
                    f"Deselected subtype '{desel_st}' must not appear in cart payload"
                )

        # Verify target budget constraints if set
        if "target_budget" in desel:
            assert cart_total <= desel["target_budget"], (
                f"Cart total {cart_total} exceeds target budget {desel['target_budget']}"
            )
