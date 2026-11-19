"""Build Running Products Catalog from OpenCart MySQL DB.

Extracts all active, in-stock products for running nutrition, hydration,
gear, comfort, and recovery. Tags each product with slot, price tier,
distance suitability, caffeine content, and gastrointestinal friendliness.
"""

import os
import sys
import json
import re
from pathlib import Path

# Add test-quiz-sandbox to sys.path to reuse MySQL connection logic
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
sys.path.append(str(PROJECT_ROOT / "test-quiz-sandbox"))

from stock_checker import StockChecker, _mysql_query


def determine_brand(name: str) -> str:
    name_upper = name.upper()
    # Check specific patterns with word boundaries
    if re.search(r'\bGU\b|GU ENERGY', name_upper):
        return "GU Energy"
    if "MAURTEN" in name_upper:
        return "Maurten"
    if "SIS" in name_upper or "SCIENCE IN SPORT" in name_upper:
        return "SiS"
    if any(k in name_upper for k in ["PF&H", "PFH", "PRECISION FUEL", "PRECISION HYDRATION", "PF 30", "PF 90"]):
        return "Precision Fuel & Hydration"
    if "NUTREND" in name_upper:
        return "Nutrend"
    if "SPONSER" in name_upper:
        return "Sponser"
    if "SALTSTICK" in name_upper:
        return "SaltStick"
    if "CHAMOIS" in name_upper or "BUTT'R" in name_upper:
        return "Chamois Butt'r"
    if "RACE EXPERT" in name_upper or "RE ULTRA" in name_upper:
        return "Race Expert"
    if "NOW FOODS" in name_upper:
        return "NOW Foods"
    if "PUREGOLD" in name_upper:
        return "PureGold"
    if "BODYPERSON" in name_upper:
        return "Bodyperson Labs"
    if "OLIMP" in name_upper:
        return "Olimp"
    if "226ERS" in name_upper:
        return "226ERS"
    if "POWERBAR" in name_upper or "POWER BAR" in name_upper:
        return "PowerBar"
    if "TRISWIM" in name_upper:
        return "TRISWIM"
    if "ЇДЛО" in name_upper:
        return "ЇДЛО"
    if "SPORTER" in name_upper:
        return "Sporter"
    if "KEVIN LEVRONE" in name_upper:
        return "Kevin Levrone"
    if "SCITEC" in name_upper:
        return "Scitec Nutrition"
    if "BIOTECH" in name_upper:
        return "BioTechUSA"
    return "Інший бренд"


def determine_price_tier(price: float, slot: str) -> str:
    # Price tier based on unit price and product category
    if slot == "energy":
        if price <= 85.0:
            return "economy"
        elif price <= 135.0:
            return "standard"
        else:
            return "premium"
    elif slot == "hydration":
        if price <= 150.0:
            return "economy"
        elif price <= 450.0:
            return "standard"
        else:
            return "premium"
    elif slot == "gear":
        if price <= 300.0:
            return "economy"
        elif price <= 650.0:
            return "standard"
        else:
            return "premium"
    else:  # care_recovery
        if price <= 150.0:
            return "economy"
        elif price <= 600.0:
            return "standard"
        else:
            return "premium"


def main():
    print("Connecting to OpenCart database...")
    checker = StockChecker()
    sock = checker._ensure_connection()

    print("Fetching active in-stock products with attributes...")
    sql = """
        SELECT 
            p.product_id,
            p.model,
            p.sku,
            p.price,
            p.quantity,
            p.image,
            pd.name,
            pd.meta_title,
            pd.tag
        FROM oc_product p
        JOIN oc_product_description pd ON p.product_id = pd.product_id
        WHERE pd.language_id = 6 
          AND p.status = 1 
          AND p.quantity > 0
    """
    rows = _mysql_query(sock, sql)
    print(f"Fetched {len(rows)} active in-stock products. Filtering running inventory...")

    catalog = []
    
    for r in rows:
        pid = int(r["product_id"])
        name = r["name"] or ""
        name_lower = name.lower()
        tag = (r["tag"] or "").lower()
        price = float(r["price"] or 0)
        qty = int(r["quantity"] or 0)
        image = r["image"] or ""
        
        # Exclude wholesale bulk packs > 4500 грн or obvious non-running items
        if price > 4500.0:
            continue
        if any(bad in name_lower for bad in ["гейнер", "подарунковий сертифікат", "чоловіче здоров"]):
            continue

        slot = None
        sub_type = None
        caffeine = False
        stomach_gentle = False
        distances = ["10k", "21k", "42k", "trail"]

        # 1. SLOT: ENERGY
        if any(k in name_lower for k in ["гель", "gel", "pf 30", "pf 90", "drink mix", "енергетичний напій"]) and not any(k in name_lower for k in ["душу", "крем-гель", "для вмивання"]):
            slot = "energy"
            sub_type = "gel"
            if any(k in name_lower for k in ["кофеїн", "кофеин", "caffeine", "espresso", "cola", "кола", "подвійний кофеїн"]):
                caffeine = True
            if any(k in name_lower for k in ["maurten", "гідрогель", "hydrogel", "pf 30", "pf&h", "pf 90", "ізотонічний", "isotonic"]):
                stomach_gentle = True

        elif any(k in name_lower for k in ["мармелад", "желейні цукерки", "желейки", "chew", "gummy", "maurten solid"]):
            slot = "energy"
            sub_type = "chew"
            stomach_gentle = True
            if "кофеїн" in name_lower or "caffeine" in name_lower:
                caffeine = True

        elif any(k in name_lower for k in ["вафл", "waffle"]):
            slot = "energy"
            sub_type = "waffle"
            stomach_gentle = True

        # 2. SLOT: HYDRATION & SALTS
        elif any(k in name_lower for k in ["сольові", "солевые", "salt caps", "saltstick", "електроліт", "электролит", "ізотонік", "изотоник", "isodrinx", "hydro"]):
            slot = "hydration"
            if any(k in name_lower for k in ["сольов", "солев", "salt"]):
                sub_type = "salt_caps"
            else:
                sub_type = "isotonic"
            distances = ["10k", "21k", "42k", "trail"]

        # 3. SLOT: GEAR & CARRYING
        elif any(k in name_lower for k in ["пояс", "сумка для бігу", "waist pack", "slim belt", "тримач для номера"]):
            slot = "gear"
            sub_type = "running_belt"
            distances = ["10k", "21k", "42k", "trail"]

        elif any(k in name_lower for k in ["фляга", "soft flask", "пляшка"]):
            if not any(k in name_lower for k in ["шеврон"]):
                slot = "gear"
                sub_type = "soft_flask"
                distances = ["10k", "21k", "42k", "trail"]

        elif any(k in name_lower for k in ["шкарпетки", "носки"]) and any(k in name_lower for k in ["re ultra", "race expert", "компрес", "біг", "ultra"]):
            slot = "gear"
            sub_type = "running_socks"
            distances = ["10k", "21k", "42k", "trail"]

        elif any(k in name_lower for k in ["кепка", "баф", "buff"]) and "race expert" in name_lower:
            slot = "gear"
            sub_type = "headwear"
            distances = ["10k", "21k", "42k", "trail"]

        # 4. SLOT: CARE & RECOVERY
        elif any(k in name_lower for k in ["butt'r", "натиран", "натираний", "glide", "anti-friction"]):
            slot = "care_recovery"
            sub_type = "anti_chafe"
            distances = ["10k", "21k", "42k", "trail"]

        elif any(k in name_lower for k in ["магній", "магний", "magnesium"]):
            slot = "care_recovery"
            sub_type = "magnesium"
            distances = ["10k", "21k", "42k", "trail"]

        elif any(k in name_lower for k in ["flexit", "колаген", "коллаген"]):
            slot = "care_recovery"
            sub_type = "joint_care"
            distances = ["10k", "21k", "42k", "trail"]

        elif any(k in name_lower for k in ["rego", "pro recovery", "recovery drink", "відновлювальний напій"]):
            slot = "care_recovery"
            sub_type = "recovery_drink"
            distances = ["10k", "21k", "42k", "trail"]

        elif any(k in name_lower for k in ["beta alanine", "бета аланін", "цитрулін", "citrulline", "beet it"]):
            slot = "care_recovery"
            sub_type = "endurance_booster"
            distances = ["10k", "21k", "42k"]

        elif any(k in name_lower for k in ["їдло", "сублім"]):
            slot = "energy"
            sub_type = "trail_food"
            distances = ["trail"]

        if not slot:
            continue

        brand = determine_brand(name)
        price_tier = determine_price_tier(price, slot)

        # Force Maurten / Precision Fuel to premium
        if brand in ["Maurten", "Precision Fuel & Hydration"]:
            price_tier = "premium"
            stomach_gentle = True

        catalog.append({
            "product_id": pid,
            "sku": r["sku"] or "",
            "name": name,
            "brand": brand,
            "price": round(price, 2),
            "quantity": qty,
            "image": f"https://raceexpert.com.ua/image/{image}" if image else "",
            "url": f"https://raceexpert.com.ua/index.php?route=product/product&product_id={pid}",
            "slot": slot,
            "sub_type": sub_type,
            "price_tier": price_tier,
            "caffeine": caffeine,
            "stomach_gentle": stomach_gentle,
            "distances": distances
        })

    # Save to JSON
    output_path = PROJECT_ROOT / "running_catalog.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(catalog, f, ensure_ascii=False, indent=2)

    print(f"\nSuccessfully extracted and categorized {len(catalog)} running products!")
    
    # Statistics
    stats_slot = {}
    stats_tier = {}
    for item in catalog:
        s = item["slot"]
        t = item["price_tier"]
        stats_slot[s] = stats_slot.get(s, 0) + 1
        stats_tier[t] = stats_tier.get(t, 0) + 1

    print("\n--- By Slot ---")
    for s, c in sorted(stats_slot.items()):
        print(f"  {s:15}: {c} products")

    print("\n--- By Price Tier ---")
    for t, c in sorted(stats_tier.items()):
        print(f"  {t:15}: {c} products")


if __name__ == "__main__":
    main()
