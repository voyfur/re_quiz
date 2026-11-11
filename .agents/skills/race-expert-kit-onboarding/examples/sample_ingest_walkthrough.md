# End-to-End Walkthrough: Onboarding a New Product Kit

This example shows the exact procedure followed by the `race-expert-kit-onboarding` skill when a user provides a URL.

---

### Step 1: User Request
> "Добавь в квиз новый набор: https://raceexpert.com.ua/nabir-marafon-finish"

---

### Step 2: Fetch and Initial Parse
Run `fetch_and_parse_kit.py`:
```bash
python3 .agents/skills/race-expert-kit-onboarding/scripts/fetch_and_parse_kit.py \
  https://raceexpert.com.ua/nabir-marafon-finish \
  --out /tmp/parsed_kit.json
```

**Parsed Draft Output:**
```json
{
  "title": "Набір «Марафонський фініш»",
  "sku": "RE99101",
  "price_uah": 1850,
  "source_url": "https://raceexpert.com.ua/nabir-marafon-finish",
  "composition": "Ізотонік Hydria Perform 500г, 6 енергетичних гелів SiS, бігові шкарпетки",
  "research_tasks": [
    "Apparel present but no shoe/sock size range found: research available sizes.",
    "Verify product forms for Hydria Perform (powder vs sticks) and SiS gels (gel vs liquid)."
  ]
}
```

---

### Step 3: Autonomous Web Research on Identified Gaps
The agent performs web searches using `search_web`:
1. **Query**: `"SiS Go Isotonic Energy Gel" product form ingredients`
   - *Result*: 60 ml energy gel sachets (`product_forms: ["gel"]`, `component_classes: ["protein_carbohydrate_food"]`).
2. **Query**: `"Hydria Perform" 500г powder electrolytes`
   - *Result*: Isotonic electrolyte powder drink mix (`product_forms: ["powder"]`, `component_classes: ["hydration_items"]`).
3. **Query**: `site:raceexpert.com.ua "Набір «Марафонський фініш»" розмір шкарпеток`
   - *Result*: Running socks included in sizes 40–42 and 43–45 (`size_sensitive: true`, `size_values: [{"type": "shoe_or_sock_size", "value": "40-42"}, {"type": "shoe_or_sock_size", "value": "43-45"}]`).

---

### Step 4: Normalization
Save the enriched JSON:
```json
{
  "title": "Набір «Марафонський фініш»",
  "sku": "RE99101",
  "price_uah": 1850,
  "source_url": "https://raceexpert.com.ua/nabir-marafon-finish",
  "composition": "Ізотонік Hydria Perform 500г, 6 енергетичних гелів SiS, бігові шкарпетки Race Expert (40–42, 43–45)",
  "description": "Комплексний набір для подолання марафону та напівмарафону: вуглеводне паливо на дистанції та відновлення водно-сольового балансу.",
  "tags": {
    "item_type": ["snack_bundle", "apparel_bundle"]
  },
  "matching_evidence": {
    "status": "candidate_direct_seller_positioning",
    "seller_families": ["running_race_preparation", "endurance_energy", "hydration_electrolytes"],
    "component_families": ["hydration_electrolytes", "portable_food_snacks", "foot_apparel_comfort"],
    "seller_activity_groups": ["running"],
    "component_activity_groups": ["running"],
    "component_classes": ["hydration_items", "protein_carbohydrate_food", "apparel_footwear"],
    "use_contexts": ["event_preparation", "during_training"],
    "race_formats": ["marathon", "half_marathon"],
    "product_forms": ["gel", "powder", "apparel"],
    "size_sensitive": true,
    "size_values": [
      {"type": "shoe_or_sock_size", "value": "40-42"},
      {"type": "shoe_or_sock_size", "value": "43-45"}
    ],
    "weather_signals": ["hot_weather"],
    "conflict_notes": []
  }
}
```

---

### Step 5: Master Ingestion & Bundle Rebuild
Execute:
```bash
python3 .agents/skills/race-expert-kit-onboarding/scripts/ingest_kit.py /tmp/enriched_kit.json
```
* Output:
  - Added as Row 207 (`race-expert-207`)
  - Regenerated `catalog_data.js` and `client_matcher.js`
  - Rebuilt `public/index.html` and `quiz.html`
  - Total catalog kits updated to 207!

---

### Step 6: Matching Simulation Audit
Execute:
```bash
python3 .agents/skills/race-expert-kit-onboarding/scripts/audit_new_kit.py 207
```
* Output:
  - Test Goal: `running` -> Candidate Pool: 90 kits.
  - Query: `activity=running, max_price=2050, shoe_size=42`.
  - Result: Surfaced at Rank 1 with Match Confidence Score: **96% (Exact match)**!
