"""Test 20 Runner Personas against the Decision Engine.

Validates that every single runner persona receives a complete, non-empty,
expert-grade starter box strictly aligned with physiology, weather, distance,
safety constraints, and budget tiers.
"""

import json
from runner_box_engine import generate_runner_box

SCENARIOS = [
    {
        "id": 1, "name": "10k Beginner (First Race, Economy)",
        "inputs": {"distance": "10k", "pace_target": "finish", "weather": "moderate", "stomach_type": "normal", "caffeine_preference": "none", "body_concerns": [], "gear_needed": [], "price_tier": "economy"}
    },
    {
        "id": 2, "name": "10k PB Chaser (Cold, Caffeine Boost, Standard)",
        "inputs": {"distance": "10k", "pace_target": "record", "weather": "cold", "stomach_type": "normal", "caffeine_preference": "boost", "body_concerns": [], "gear_needed": [], "price_tier": "standard"}
    },
    {
        "id": 3, "name": "10k Hot Weather + Cramps (Economy)",
        "inputs": {"distance": "10k", "pace_target": "steady", "weather": "hot", "stomach_type": "normal", "caffeine_preference": "none", "body_concerns": ["cramps"], "gear_needed": ["belt"], "price_tier": "economy"}
    },
    {
        "id": 4, "name": "10k Sensitive Stomach (Premium Hydrogel)",
        "inputs": {"distance": "10k", "pace_target": "record", "weather": "moderate", "stomach_type": "sensitive", "caffeine_preference": "none", "body_concerns": [], "gear_needed": ["socks"], "price_tier": "premium"}
    },
    {
        "id": 5, "name": "10k Vegan Runner (Standard)",
        "inputs": {"distance": "10k", "pace_target": "steady", "weather": "moderate", "stomach_type": "vegan", "caffeine_preference": "boost", "body_concerns": ["chafing"], "gear_needed": [], "price_tier": "standard"}
    },
    {
        "id": 6, "name": "21k Steady Runner (Moderate, Standard)",
        "inputs": {"distance": "21k", "pace_target": "steady", "weather": "moderate", "stomach_type": "normal", "caffeine_preference": "boost", "body_concerns": [], "gear_needed": ["belt"], "price_tier": "standard"}
    },
    {
        "id": 7, "name": "21k Hot Summer Half (Cramps Risk, Standard)",
        "inputs": {"distance": "21k", "pace_target": "steady", "weather": "hot", "stomach_type": "normal", "caffeine_preference": "none", "body_concerns": ["cramps"], "gear_needed": ["flask"], "price_tier": "standard"}
    },
    {
        "id": 8, "name": "21k Record Racer (Cold, Premium Maurten/PF&H)",
        "inputs": {"distance": "21k", "pace_target": "record", "weather": "cold", "stomach_type": "sensitive", "caffeine_preference": "boost", "body_concerns": ["chafing"], "gear_needed": ["belt", "socks"], "price_tier": "premium"}
    },
    {
        "id": 9, "name": "21k Economy Budget Runner",
        "inputs": {"distance": "21k", "pace_target": "finish", "weather": "moderate", "stomach_type": "normal", "caffeine_preference": "none", "body_concerns": [], "gear_needed": [], "price_tier": "economy"}
    },
    {
        "id": 10, "name": "21k Knee/Joint Care Runner",
        "inputs": {"distance": "21k", "pace_target": "steady", "weather": "moderate", "stomach_type": "normal", "caffeine_preference": "none", "body_concerns": ["joints"], "gear_needed": ["socks"], "price_tier": "standard"}
    },
    {
        "id": 11, "name": "42k Marathon PB (Hot, Cramps, Premium)",
        "inputs": {"distance": "42k", "pace_target": "record", "weather": "hot", "stomach_type": "normal", "caffeine_preference": "boost", "body_concerns": ["cramps", "chafing"], "gear_needed": ["belt", "flask"], "price_tier": "premium"}
    },
    {
        "id": 12, "name": "42k First-time Marathoner (Sensitive, Standard)",
        "inputs": {"distance": "42k", "pace_target": "finish", "weather": "cold", "stomach_type": "sensitive", "caffeine_preference": "none", "body_concerns": ["cramps", "chafing", "joints"], "gear_needed": ["belt", "socks"], "price_tier": "standard"}
    },
    {
        "id": 13, "name": "42k Hot Marathon Wave (Electrolyte Priority)",
        "inputs": {"distance": "42k", "pace_target": "steady", "weather": "hot", "stomach_type": "normal", "caffeine_preference": "boost", "body_concerns": ["cramps"], "gear_needed": ["flask"], "price_tier": "standard"}
    },
    {
        "id": 14, "name": "42k Vegan Marathoner (Standard)",
        "inputs": {"distance": "42k", "pace_target": "steady", "weather": "moderate", "stomach_type": "vegan", "caffeine_preference": "none", "body_concerns": ["chafing"], "gear_needed": ["belt"], "price_tier": "standard"}
    },
    {
        "id": 15, "name": "42k Economy Marathon Budget",
        "inputs": {"distance": "42k", "pace_target": "finish", "weather": "moderate", "stomach_type": "normal", "caffeine_preference": "none", "body_concerns": [], "gear_needed": [], "price_tier": "economy"}
    },
    {
        "id": 16, "name": "Trail 30k Mountain Run (Standard)",
        "inputs": {"distance": "trail", "pace_target": "steady", "weather": "moderate", "stomach_type": "sensitive", "caffeine_preference": "boost", "body_concerns": ["chafing"], "gear_needed": ["flask", "socks"], "price_tier": "standard"}
    },
    {
        "id": 17, "name": "Ultra Trail 50k Pro (Hot, Premium)",
        "inputs": {"distance": "trail", "pace_target": "record", "weather": "hot", "stomach_type": "normal", "caffeine_preference": "boost", "body_concerns": ["cramps", "chafing", "joints"], "gear_needed": ["belt", "flask", "socks"], "price_tier": "premium"}
    },
    {
        "id": 18, "name": "Trail Cold Weather (Economy)",
        "inputs": {"distance": "trail", "pace_target": "finish", "weather": "cold", "stomach_type": "normal", "caffeine_preference": "none", "body_concerns": ["cramps"], "gear_needed": ["flask"], "price_tier": "economy"}
    },
    {
        "id": 19, "name": "Trail Vegan Ultra (Premium)",
        "inputs": {"distance": "trail", "pace_target": "steady", "weather": "moderate", "stomach_type": "vegan", "caffeine_preference": "none", "body_concerns": ["joints"], "gear_needed": ["belt"], "price_tier": "premium"}
    },
    {
        "id": 20, "name": "21k Severe Chafing Risk (Standard)",
        "inputs": {"distance": "21k", "pace_target": "steady", "weather": "hot", "stomach_type": "sensitive", "caffeine_preference": "boost", "body_concerns": ["chafing"], "gear_needed": ["belt"], "price_tier": "standard"}
    }
]

def run_stress_test():
    with open("running_catalog.json", "r", encoding="utf-8") as f:
        catalog = json.load(f)

    print(f"Loaded {len(catalog)} products. Running 20 Runner Personas audit...\n")
    
    passed = 0
    failed = 0

    for sc in SCENARIOS:
        box = generate_runner_box(sc["inputs"], catalog)
        slots = box["slots"]
        errors = []

        # Check 1: No empty slots
        for sname in ["energy", "hydration", "gear", "care_recovery"]:
            if len(slots.get(sname, [])) == 0:
                errors.append(f"Empty slot: '{sname}'")

        # Check 2: Caffeine safety
        all_items = [it for s in slots.values() for it in s]
        if sc["inputs"]["caffeine_preference"] == "none":
            for it in all_items:
                if it["product"].get("caffeine", False):
                    errors.append(f"Caffeine leak: {it['product']['name']}")

        # Check 2b: Single gel brand consistency (never mix different gel brands)
        energy_gels = [it for it in slots["energy"] if it["product"].get("sub_type") == "gel"]
        gel_brands = {it["product"].get("brand") for it in energy_gels}
        if len(gel_brands) > 1:
            errors.append(f"Mixed gel brands in energy slot: {gel_brands}")

        # Check 3: Caffeine boost present if requested
        if sc["inputs"]["caffeine_preference"] == "boost":
            caff_items = [it for it in slots["energy"] if it["product"].get("caffeine")]
            if not caff_items:
                errors.append("Requested caffeine boost but none in energy slot")

        # Check 4: Hot weather / cramps salt injection
        if sc["inputs"]["weather"] == "hot" or "cramps" in sc["inputs"]["body_concerns"]:
            subtypes = [it["product"].get("sub_type") for it in slots["hydration"]]
            if "salt_caps" not in subtypes:
                errors.append("Hot weather/cramps missing salt_caps in hydration")

        # Check 5: Stock quantities
        for it in all_items:
            if it["product"].get("quantity", 0) <= 0:
                errors.append(f"Zero quantity product: {it['product']['name']}")

        # Check 6: Sane total price > 0
        if box["total_base_price"] <= 0:
            errors.append("Total base price <= 0")

        if errors:
            print(f"[FAIL] Scenario #{sc['id']}: {sc['name']}")
            for err in errors:
                print(f"       -> {err}")
            failed += 1
        else:
            print(f"[PASS] Scenario #{sc['id']:02d}: {sc['name']:<45} | {len(all_items)} items | {box['total_base_price']:>7.1f} грн")
            passed += 1

    print(f"\n==========================================")
    print(f"Total: {passed + failed} | Passed: {passed} | Failed: {failed}")
    print(f"==========================================")
    assert failed == 0, f"{failed} scenarios failed"

def test_runner_20_scenarios():
    run_stress_test()

if __name__ == "__main__":
    run_stress_test()
