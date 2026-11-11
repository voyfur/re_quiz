---
name: race-expert-kit-onboarding
description: Use when the user provides a URL to a new product set or kit to add to the Race Expert quiz catalog. Automatically fetches the product page, extracts titles, prices, compositions, and attributes, conducts web research for missing facts, normalizes into the quiz evidence schema, updates the catalog and audit files, and rebuilds the interactive quiz bundles and HTML pages.
---

# Race Expert Product Kit Onboarding Skill

This skill teaches the agent how to autonomously take a URL for a new product kit, analyze its composition, research missing information across external sources, map it to the 4-layer quiz matching evidence taxonomy, and seamlessly ingest it into the live quiz without breaking existing logic or test baselines.

---

## Trigger Conditions

Activate this skill when:
* The user provides a link (URL) to a product or kit (e.g. `https://raceexpert.com.ua/...` or manufacturer page) and asks to add it to the quiz.
* The user says *"добавь новый набор по ссылке"*, *"подготовь новый набор"*, *"проанализируй товар и добавь в квиз"*, or similar.
* A batch of new sets or products needs to be ingested into the quiz catalog and verified against matching rules.

---

## Architecture & Data Flow

```
[ New Kit URL ]
       │
       ▼
1. Fetch & Parse (scripts/fetch_and_parse_kit.py)
   ├── Raw Source Preservation (`raw/sources/YYYY-MM-DD-kit-<slug>.md`)
   └── Extract: Title, SKU, Price, Composition, Initial Signals
       │
       ▼
2. Gap Analysis & Autonomous Research (search_web)
   ├── Identify: missing forms, unverified sizes, unknown ingredient classes
   └── Resolve: search brand/supplier data to fill all informational blanks
       │
       ▼
3. Normalization (scripts/normalize_kit_data.py)
   └── Enforce strict enum taxonomies (goals, activities, forms, contexts)
       │
       ▼
4. Master Ingestion (scripts/ingest_kit.py)
   ├── Append to `test-quiz-sandbox/catalog.json` & `wiki/projects/quiz-set-audit.json`
   ├── Rebuild client bundles (`catalog_data.js` & `client_matcher.js`)
   └── Rebuild HTML standalone pages (`public/index.html` & `quiz.html`)
       │
       ▼
5. Audit & Matching Verification (scripts/audit_new_kit.py)
   └── Simulate queries, verify score (88–99%), ensure 0 dead-ends
```

---

## Step-by-Step Execution Runbook

### Phase 1: Intake & Raw Evidence Preservation
1. When the user provides a URL (e.g., `https://raceexpert.com.ua/product-name`):
2. Fetch the page HTML content and save a copy to `raw/sources/<YYYY-MM-DD>-kit-<slug>.md` per the project's LLM Wiki immutability rules.
3. Run the parser script:
   ```bash
   python3 .agents/skills/race-expert-kit-onboarding/scripts/fetch_and_parse_kit.py <URL> --out /tmp/parsed_kit.json
   ```
4. Inspect the generated `/tmp/parsed_kit.json`. Review the `research_tasks` array to see what information is missing or ambiguous.

---

### Phase 2: Autonomous Web Research on Information Gaps
If `research_tasks` contains items (e.g., component forms, ingredient categories, sizing ranges, or specific benefits):
1. **Never guess or invent data.**
2. Use `search_web` to search manufacturer and sports nutrition resources for the specific component:
   * **Component form/composition query**: `"<Brand> <Component Name>" ingredients nutrition facts form` (e.g. `"SiS Go Isotonic Gel" packaging form`).
   * **Size query**: `site:raceexpert.com.ua "<Kit Title>" розмір шкарпеток` or check shoe/sock sizes.
   * **Usage context query**: `"<Product Name>" how to take during marathon running`.
3. Enrich the JSON draft with confirmed findings. If a component remains ambiguous after research, document it in `conflict_notes` rather than fabricating values.

---

### Phase 3: Taxonomy Normalization
1. Ensure all terms map strictly to the controlled vocabularies defined in:
   [controlled_vocabularies.md](references/controlled_vocabularies.md)
   * **Primary Goals (`seller_families`)**: must belong to `GOAL_FAMILIES` (e.g. `running_race_preparation`, `hydration_electrolytes`, `strength_muscle_training`).
   * **Activity Groups (`activity_groups`)**: `running`, `cycling`, `hiking`, `strength_training`, `functional_training`, `swimming`, `mind_body_mobility`, `walking`, `general_fitness`, `other`.
   * **Component Classes (`component_classes`)**: `protein_carbohydrate_food`, `supplements_vitamins_minerals`, `creatine_preworkout`, `hydration_items`, `sports_accessories`, `apparel_footwear`, `dehydrated_meal`, `club_membership`.
   * **Product Forms (`product_forms`)**: `gel`, `bars`, `liquid`, `powder`, `sticks`, `capsules`, `softgels`, `tablets`, `apparel`, `food_or_meal`.
   * **Use Contexts (`use_contexts`)**: `event_preparation`, `training`, `everyday`, `before_or_after_training`, `during_training`, `daily_use`, `evening_or_bedtime`, `hiking_or_camping`, `travel_or_road`, `work_or_study`, `gift`.
2. Validate the file:
   ```bash
   python3 .agents/skills/race-expert-kit-onboarding/scripts/normalize_kit_data.py /tmp/parsed_kit.json
   ```

---

### Phase 4: Master Ingestion & Bundle Rebuild
1. Run `ingest_kit.py`:
   ```bash
   python3 .agents/skills/race-expert-kit-onboarding/scripts/ingest_kit.py /tmp/parsed_kit.json
   ```
2. The script will:
   * Assign the next sequential `catalog_row` and `set_id` (e.g. Row 207, `race-expert-207`).
   * Append the structured record to `test-quiz-sandbox/catalog.json`.
   * Append the audit evidence entry to `wiki/projects/quiz-set-audit.json`.
   * Execute `build_bundle.py` to regenerate client-side `catalog_data.js` and `client_matcher.js`.
   * Execute `build_external_quiz_v2.py` to rebuild `public/index.html` and `quiz.html`.
   * Synchronize the in-chat interactive widget artifact.

---

### Phase 5: Verification & Audit
1. Run the targeted kit audit:
   ```bash
   python3 .agents/skills/race-expert-kit-onboarding/scripts/audit_new_kit.py <ROW_NUMBER_OR_SET_ID>
   ```
   * Confirm that the kit is reachable in each of its target goal branches.
   * Verify that an exact-match test query surfaces the kit in the top 3 results with a Match Confidence Score ≥ 88%.
2. Run regression tests to verify zero breaks across the catalog:
   ```bash
   cd test-quiz-sandbox && PYTHONPATH=. pytest tests
   ```
3. Report the result to the user with:
   * Allocated Row and Set ID
   * Ingested title, SKU, price, and composition
   * Matched goal branches and simulated match score %
   * Live preview URL on `http://172.20.10.6:8080/`
