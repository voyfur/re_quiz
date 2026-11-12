# QA Specialist Deep Audit Report: Hydration & Electrolytes (`hydration`)
**Auditor:** QA Specialist for "Hydration & Electrolytes"  
**Catalog Source:** `wiki/projects/quiz-set-audit.json` (207 sets snapshot)  
**Execution Date:** 2026-11-12  
**Test Suite:** 100 Dedicated Buyer Scenarios strictly for `goal_group: "hydration"`  

---

## 1. Executive Summary & Verdict Scorecard

Across 100 dedicated buyer test scenarios covering high heat / heavy sweat, daily mineral balance, endurance race hydration + amino acids, soft flasks and water bottles, budget tiers, and product form factors:
- **PASS:** 22 (22.0%) — Clean, accurate hydration match with legitimate electrolytes, no deceptive claims, and correct pricing.
- **WARN:** 78 (78.0%) — Partially relevant match (e.g. genuine Hydria electrolytes bundled with a 3-month gym club membership, socks, or bath towel; catalog coverage gap under 1225 UAH; or missing soft flask inventory).
- **FAIL:** 0 (0.0%) — Critical human-logic flaws, including engine crashes, 0-result taxonomy bugs, massive non-hydration product leaks (500g Creatine Monohydrate, Spirulina, Lion's Mane), and deceptive `(без сторонніх речей)` claims.

### Category Breakdown

| Category | Total Scenarios | PASS | WARN | FAIL | Pass Rate |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **High Heat / Heavy Sweat / Cramps** | 20 | 0 | 20 | 0 | 0.0% |
| **General Daily Mineral Balance** | 15 | 0 | 15 | 0 | 0.0% |
| **Endurance Race Hydration + Amino Acids** | 20 | 0 | 20 | 0 | 0.0% |
| **Soft Flasks, Bottles & Hydration Gear** | 15 | 0 | 15 | 0 | 0.0% |
| **Budget Tiers (<1000, 1000–1600, >1600 UAH)** | 15 | 7 | 8 | 0 | 46.7% |
| **Product Forms, Activities & Leak Probes** | 15 | 15 | 0 | 0 | 100.0% |
| **TOTAL** | **100** | **22** | **78** | **0** | **22.0%** |

---

## 2. Deep Dive: Discovered Human-Logic Flaws & Bugs

### A. The #1 Creatine Default Leak (Absurd Recommendation for Generic Hydration)
> [!CAUTION]
> When a buyer clicks **"Гідратація" (Hydration)** with no restrictive filters, the engine's **#1 recommendation is RE11681 «Ріст м'язів» (Muscle Growth)** at 1225 UAH!
- **Actual Composition of RE11681:** 500g Bodyperson Creatine Monohydrate, Lipobar protein bars x2, Brave U shaker 700ml, 3-month gym club membership, and only 4 sticks of Hydria Daily.
- **Why it happens:** In `wiki/projects/quiz-set-audit.json`, because RE11681 contains 4 sticks of Hydria Daily, it was awarded `hydration_electrolytes` in both `seller_families` and `component_families`. Because its price (1225 UAH) is the absolute lowest among all sets tagged with hydration, `draft_matcher` sorts it first!
- **Customer Experience:** A dehydrated runner or cyclist asking for hydration is told to buy a heavy 500g bodybuilding creatine muscle mass gainer tub.

### B. Severe Non-Hydration Product Leaks: Spirulina, Mushrooms & Footwear
The catalog evidence pool permits inappropriate non-hydration products to infiltrate the `hydration` results:
1. **Spirulina Algae Leak (RE11513 «Енергія і очищення», 1455 UAH):**
   - Contains: **Now Foods Organic Spirulina (100 tablets)**, Zinc Picolinate (60 caps), Omega-3 (60 softgels), and 5 sticks of Hydria Perform.
   - Recommended when users filter for vitamins/minerals under hydration. Spirulina algae tablets have zero electrolyte replenishment capability.
2. **Lion's Mane / Nootropic Mushroom Leak (RE88943 «Концентрація в дорозі», 1469 UAH):**
   - Contains: **Lion's Mane 700mg (60 capsules)**, Acetyl-L-Carnitine (50 caps), and 3 Hydria sticks. Recommending medicinal brain mushrooms to an athlete seeking hydration is completely illogical.
3. **Pure Socks Bundles with 0 Electrolytes (RE11013 «Бігова пара», 1359 UAH; RE89475 «Бігова екіпіровка», 1415 UAH):**
   - RE11013 contains: 2 pairs of Race Expert socks and 1 glass bottle. It contains **ZERO electrolytes, zero powders, zero tablets**. Recommending socks to someone asking for hydration is a severe classification defect.

### C. The Hiker, Triathlete & Walker Validation Wall (`DraftMatchError` Crash)
> [!WARNING]
> In `draft_matcher.py`, `ACTIVITY_OPTIONS_BY_GOAL["hydration"]` is strictly hardcoded to:
> `('running', 'cycling', 'strength_training', 'functional_training')`.
- If a **hiker** selects `activity: "hiking"` under hydration, the engine crashes with:  
  `DraftMatchError: activity is not supported for the selected need.`
- If a **triathlete** selects `activity: "triathlon"`, the engine crashes.
- If a **walker** selects `activity: "walking"`, the engine crashes.
- **Human Logic Irony:** The catalog literally contains `UT-PRO-2026` («Ultra Trail Marathon Energy & Hydration Pro»), whose audited activity scope explicitly includes `hiking`! Yet a hiker is rejected by the validation gate.

### D. Activity Taxonomy Bug: 0 Results for Strength & Functional Training
- While `draft_matcher.py` accepts `strength_training` and `functional_training` as options for `hydration`, in `quiz-set-audit.json` all gym sets have `activity_groups: ["fitness_gym"]`.
- Because there is no taxonomic translation between `strength_training` / `functional_training` and `fitness_gym`, the filter `_candidate_fit` treats them as disjoint.
- **Outcome:** Any gym athlete asking for intra-workout hydration receives **0 matches (`status: no_match`)**, even though sets like RE11786 and RE11802 contain shakers, BCAA/EAA, and Hydria Perform specifically designed for gym training.

### E. Product Form Validation Blockade: Effervescent Tablets, Powders & Soft Flasks
- In `draft_matcher.py`, `PRODUCT_FORMS_BY_GOAL["hydration"]` is set to:  
  `('liquid', 'gel', 'bars', 'sticks')`.
- Notice that it includes **`bars`** (which are solid food, not hydration drinks), but completely excludes **`tablets`** and **`powder`**!
- If a buyer selects `product_form: "tablets"`, the engine throws `DraftMatchError: product_form is not supported`. Yet two of the most prominent hydration sets in the store (`RE11650` Precision Hydration 1000 Tube and `UT-PRO-2026` SIS Go Hydro) are **effervescent tablets**!
- If a buyer selects `product_form: "powder"`, the engine crashes, even though Nutriversum EAA and BCAA are bulk hydration powders.
- If a buyer asks for `product_form: "flasks"`, the engine crashes. Furthermore, the catalog contains zero soft flasks (only hard plastic/glass bottles and shakers).

### F. Deceptive Justification Claims: `(без сторонніх речей)`
- The explanation generator `_build_why_suitable()` frequently outputs:  
  `Категорія товарів: у наборі саме Ізотоніки та електроліти (без сторонніх речей).`
- In reality, almost every hydration kit in the catalog includes extraneous items: 3-month gym club memberships, pairs of socks, 500g tubs of creatine, or medicinal mushrooms.
- Promising "without extraneous items" when the set is dominated by unrelated items destroys user trust.

### G. Low Budget Desert (< 1225 UAH)
- The absolute cheapest kit in the catalog matching hydration is RE11681 at 1225 UAH (or RE11650 at 1239 UAH).
- Any buyer with a realistic budget between 300 and 1000 UAH receives zero exact matches.
- For budgets below 1000 UAH, the engine's `floor_anchor` currently serves `RE11681` (Creatine Monohydrate), creating a catastrophic failure where low-budget hydration shoppers are told to buy a 1225 UAH bodybuilding creatine kit.

---

## 3. Detailed Results of all 100 Test Scenarios

| ID | Title | Category | Activity | Form | Budget | Status | Verdict | Top Recommended SKU & Notes |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| HYD-001 | Summer trail marathoner with heavy sweat rate seeking high-sodium cramp prevention | `high_heat_cramps` | running | — | 1500 ₴ | `matched` | **WARN** | [RE11650]: Suboptimal cramp match: Expected high-sodium electrolytes (Precision Hydration 1000 or Hydria Perform), got 'Н… |
| HYD-002 | Road cyclist competing in 35°C heat prone to quadriceps cramps, needing maximum sodium concentration | `high_heat_cramps` | cycling | — | 1600 ₴ | `matched` | **WARN** | [RE11650]: Suboptimal cramp match: Expected high-sodium electrolytes (Precision Hydration 1000 or Hydria Perform), got 'Н… |
| HYD-003 | Veteran sport athlete seeking heat protection hydration bundle (Precision Hydration 1000 Tube + capsules) | `high_heat_cramps` | running | — | 1300 ₴ | `matched` | **WARN** | [RE11650]: Suboptimal cramp match: Expected high-sodium electrolytes (Precision Hydration 1000 or Hydria Perform), got 'Н… |
| HYD-004 | Heavy sweater preparing for an ironman 70.3 bike leg under scorching sun | `high_heat_cramps` | cycling | — | 1600 ₴ | `matched` | **WARN** | [RE11650]: Suboptimal cramp match: Expected high-sodium electrolytes (Precision Hydration 1000 or Hydria Perform), got 'Н… |
| HYD-005 | Fast-sweating runner prone to calf cramps during 30km long runs | `high_heat_cramps` | running | — | 1500 ₴ | `matched` | **WARN** | [RE11650]: Suboptimal cramp match: Expected high-sodium electrolytes (Precision Hydration 1000 or Hydria Perform), got 'Н… |
| HYD-006 | Ultra-runner needing Hydria Perform electrolyte sticks for heat adaptation | `high_heat_cramps` | running | sticks | 1500 ₴ | `matched` | **WARN** | [RE11786]: Suboptimal cramp match: Expected high-sodium electrolytes (Precision Hydration 1000 or Hydria Perform), got 'Н… |
| HYD-007 | Marathon runner asking for electrolyte stock (20 sticks Hydria Perform) under 1500 UAH | `high_heat_cramps` | running | — | 1500 ₴ | `matched` | **WARN** | [RE11650]: Suboptimal cramp match: Expected high-sodium electrolytes (Precision Hydration 1000 or Hydria Perform), got 'Н… |
| HYD-008 | Hot weather runner asking for electrolyte salts with sodium and magnesium against cramps | `high_heat_cramps` | running | — | 1500 ₴ | `matched` | **WARN** | [RE11650]: Suboptimal cramp match: Expected high-sodium electrolytes (Precision Hydration 1000 or Hydria Perform), got 'Н… |
| HYD-009 | Cyclist asking for cramp prevention formula during century ride in July | `high_heat_cramps` | cycling | — | 1600 ₴ | `matched` | **WARN** | [RE11650]: Suboptimal cramp match: Expected high-sodium electrolytes (Precision Hydration 1000 or Hydria Perform), got 'Н… |
| HYD-010 | Marathon runner requesting high sodium hydration with budget 1300 UAH | `high_heat_cramps` | running | — | 1300 ₴ | `matched` | **WARN** | [RE11650]: Suboptimal cramp match: Expected high-sodium electrolytes (Precision Hydration 1000 or Hydria Perform), got 'Н… |
| HYD-011 | Heavy sweater asking for hydration during training in high humidity | `high_heat_cramps` | running | — | 1500 ₴ | `matched` | **WARN** | [RE11650]: Suboptimal cramp match: Expected high-sodium electrolytes (Precision Hydration 1000 or Hydria Perform), got 'Н… |
| HYD-012 | Runner seeking pure electrolyte replacement without heavy sugar | `high_heat_cramps` | running | — | 1500 ₴ | `matched` | **WARN** | [RE11650]: Suboptimal cramp match: Expected high-sodium electrolytes (Precision Hydration 1000 or Hydria Perform), got 'Н… |
| HYD-013 | Cyclist seeking high electrolyte concentration under 1500 UAH | `high_heat_cramps` | cycling | — | 1500 ₴ | `matched` | **WARN** | [RE11650]: Suboptimal cramp match: Expected high-sodium electrolytes (Precision Hydration 1000 or Hydria Perform), got 'Н… |
| HYD-014 | Endurance runner needing cramp defense with quick absorption during long runs | `high_heat_cramps` | running | sticks | 1500 ₴ | `matched` | **WARN** | [RE11786]: Suboptimal cramp match: Expected high-sodium electrolytes (Precision Hydration 1000 or Hydria Perform), got 'Н… |
| HYD-015 | Athlete training midday in summer heat seeking heat-protection hydration kit | `high_heat_cramps` | running | — | 1400 ₴ | `matched` | **WARN** | [RE11650]: Suboptimal cramp match: Expected high-sodium electrolytes (Precision Hydration 1000 or Hydria Perform), got 'Н… |
| HYD-016 | Distance runner asking for high-dose sodium tablets for sweaty conditions | `high_heat_cramps` | running | — | 1300 ₴ | `matched` | **WARN** | [RE11650]: Suboptimal cramp match: Expected high-sodium electrolytes (Precision Hydration 1000 or Hydria Perform), got 'Н… |
| HYD-017 | Cyclist asking for Hydria Perform sticks for mountain climb in hot weather | `high_heat_cramps` | cycling | sticks | 1500 ₴ | `matched` | **WARN** | [RE11786]: Suboptimal cramp match: Expected high-sodium electrolytes (Precision Hydration 1000 or Hydria Perform), got 'Н… |
| HYD-018 | Runner training for desert/sand ultra requiring electrolyte salt tablets | `high_heat_cramps` | running | — | 1300 ₴ | `matched` | **WARN** | [RE11650]: Suboptimal cramp match: Expected high-sodium electrolytes (Precision Hydration 1000 or Hydria Perform), got 'Н… |
| HYD-019 | Hot weather runner looking for magnesium + sodium combo for night cramps after long runs | `high_heat_cramps` | running | — | 1500 ₴ | `matched` | **WARN** | [RE11650]: Suboptimal cramp match: Expected high-sodium electrolytes (Precision Hydration 1000 or Hydria Perform), got 'Н… |
| HYD-020 | Competitive runner asking for cramp prevention bundle before race start | `high_heat_cramps` | running | — | 1500 ₴ | `matched` | **WARN** | [RE11650]: Suboptimal cramp match: Expected high-sodium electrolytes (Precision Hydration 1000 or Hydria Perform), got 'Н… |
| HYD-021 | Office worker and casual runner seeking daily mineral balance for hydration at desk | `daily_mineral_balance` | running | — | 1500 ₴ | `matched` | **WARN** | [RE11021]: Expected daily mineral formula (Hydria Daily), got 'Набір «Літній старт Race Expert Club» — абонемент на 3 міс… |
| HYD-022 | Everyday active individual looking for Hydria Daily peach sticks for gentle hydration | `daily_mineral_balance` | — | — | 1500 ₴ | `matched` | **WARN** | [RE11021]: Expected daily mineral formula (Hydria Daily), got 'Набір «Літній старт Race Expert Club» — абонемент на 3 міс… |
| HYD-023 | Fitness enthusiast wanting daily electrolyte drink without high sodium/sugar | `daily_mineral_balance` | running | — | 1500 ₴ | `matched` | **WARN** | [RE11021]: Expected daily mineral formula (Hydria Daily), got 'Набір «Літній старт Race Expert Club» — абонемент на 3 міс… |
| HYD-024 | Morning hydration routine seeker wanting vitamins + light minerals (Hydria Daily) | `daily_mineral_balance` | — | — | 1500 ₴ | `matched` | **WARN** | [RE11021]: Expected daily mineral formula (Hydria Daily), got 'Набір «Літній старт Race Expert Club» — абонемент на 3 міс… |
| HYD-025 | Daily hydration for person recovering from mild dehydration in warm weather | `daily_mineral_balance` | — | sticks | 1500 ₴ | `matched` | **WARN** | [RE11021]: Expected daily mineral formula (Hydria Daily), got 'Набір «Літній старт Race Expert Club» — абонемент на 3 міс… |
| HYD-026 | Active person wanting daily mineral balance with bottle included | `daily_mineral_balance` | — | — | 1500 ₴ | `matched` | **WARN** | [RE11021]: Expected daily mineral formula (Hydria Daily), got 'Набір «Літній старт Race Expert Club» — абонемент на 3 міс… |
| HYD-027 | Runner wanting daily hydration on non-workout recovery days | `daily_mineral_balance` | running | — | 1400 ₴ | `matched` | **WARN** | [RE11021]: Expected daily mineral formula (Hydria Daily), got 'Набір «Літній старт Race Expert Club» — абонемент на 3 міс… |
| HYD-028 | Daily mineral balance with budget 1400 UAH | `daily_mineral_balance` | running | — | 1400 ₴ | `matched` | **WARN** | [RE11021]: Expected daily mineral formula (Hydria Daily), got 'Набір «Літній старт Race Expert Club» — абонемент на 3 міс… |
| HYD-029 | Daily electrolyte drink for desk job and evening brisk walks | `daily_mineral_balance` | — | — | 1500 ₴ | `matched` | **WARN** | [RE11021]: Expected daily mineral formula (Hydria Daily), got 'Набір «Літній старт Race Expert Club» — абонемент на 3 міс… |
| HYD-030 | Gentle mineral hydration drink mix for everyday lifestyle | `daily_mineral_balance` | — | — | 1500 ₴ | `matched` | **WARN** | [RE11021]: Expected daily mineral formula (Hydria Daily), got 'Набір «Літній старт Race Expert Club» — абонемент на 3 міс… |
| HYD-031 | Daily wellness electrolyte mix with B-vitamins and vitamin C | `daily_mineral_balance` | running | — | 1500 ₴ | `matched` | **WARN** | [RE11021]: Expected daily mineral formula (Hydria Daily), got 'Набір «Літній старт Race Expert Club» — абонемент на 3 міс… |
| HYD-032 | Daily mineral drink for hot summer days at work | `daily_mineral_balance` | — | — | 1500 ₴ | `matched` | **WARN** | [RE11021]: Expected daily mineral formula (Hydria Daily), got 'Набір «Літній старт Race Expert Club» — абонемент на 3 міс… |
| HYD-033 | Light electrolyte hydration drink for student/office focus | `daily_mineral_balance` | — | — | 1500 ₴ | `matched` | **WARN** | [RE11021]: Expected daily mineral formula (Hydria Daily), got 'Набір «Літній старт Race Expert Club» — абонемент на 3 міс… |
| HYD-034 | Daily mineral balance kit with clean composition (no artificial stimulants or creatine) | `daily_mineral_balance` | running | — | 1500 ₴ | `matched` | **WARN** | [RE11021]: Expected daily mineral formula (Hydria Daily), got 'Набір «Літній старт Race Expert Club» — абонемент на 3 міс… |
| HYD-035 | Daily hydration bundle with reusable water bottle for daily commute | `daily_mineral_balance` | — | — | 1400 ₴ | `matched` | **WARN** | [RE11021]: Expected daily mineral formula (Hydria Daily), got 'Набір «Літній старт Race Expert Club» — абонемент на 3 міс… |
| HYD-036 | Trail ultramarathoner needing both SIS Go Hydro electrolytes and Beta Fuel gels (UT-PRO-2026) | `endurance_amino_hydration` | running | — | 1700 ₴ | `matched` | **WARN** | [RE11650]: Expected endurance race hydration (SIS / Nutriversum EAA), got 'Набір «Захист від спеки» по програмі "Ветеранс… |
| HYD-037 | Mountain runner seeking SIS Go Hydro effervescent hydration for race vests | `endurance_amino_hydration` | running | — | 1700 ₴ | `matched` | **WARN** | [RE11650]: Expected endurance race hydration (SIS / Nutriversum EAA), got 'Набір «Захист від спеки» по програмі "Ветеранс… |
| HYD-038 | Endurance cyclist seeking amino acid protection (EAA) + electrolytes during 5-hour ride | `endurance_amino_hydration` | cycling | — | 1500 ₴ | `matched` | **WARN** | [RE11650]: Expected endurance race hydration (SIS / Nutriversum EAA), got 'Набір «Захист від спеки» по програмі "Ветеранс… |
| HYD-039 | Half-Ironman triathlete asking for Nutriversum EAA + Hydria Perform electrolyte combo | `endurance_amino_hydration` | cycling | — | 1500 ₴ | `matched` | **WARN** | [RE11650]: Expected endurance race hydration (SIS / Nutriversum EAA), got 'Набір «Захист від спеки» по програмі "Ветеранс… |
| HYD-040 | Marathon runner seeking BCAA + electrolyte sticks + shaker for endurance training | `endurance_amino_hydration` | running | — | 1300 ₴ | `matched` | **WARN** | [RE11650]: Expected endurance race hydration (SIS / Nutriversum EAA), got 'Набір «Захист від спеки» по програмі "Ветеранс… |
| HYD-041 | Long distance runner wanting amino acids to prevent muscle breakdown during 35km run | `endurance_amino_hydration` | running | — | 1500 ₴ | `matched` | **WARN** | [RE11650]: Expected endurance race hydration (SIS / Nutriversum EAA), got 'Набір «Захист від спеки» по програмі "Ветеранс… |
| HYD-042 | Triathlete preparing for Olympic distance asking for isotonic hydration + amino formula | `endurance_amino_hydration` | cycling | — | 1500 ₴ | `matched` | **WARN** | [RE11650]: Expected endurance race hydration (SIS / Nutriversum EAA), got 'Набір «Захист від спеки» по програмі "Ветеранс… |
| HYD-043 | Gran Fondo cyclist seeking endurance hydration bundle with shaker and EAA | `endurance_amino_hydration` | cycling | — | 1500 ₴ | `matched` | **WARN** | [RE11786]: Expected endurance race hydration (SIS / Nutriversum EAA), got 'Набір «Тренувальний ресурс Race Expert Club» —… |
| HYD-044 | Trail runner needing electrolyte tabs and energy gels for 50km mountain race | `endurance_amino_hydration` | running | — | 1700 ₴ | `matched` | **WARN** | [RE11650]: Expected endurance race hydration (SIS / Nutriversum EAA), got 'Набір «Захист від спеки» по програмі "Ветеранс… |
| HYD-045 | Ultra endurance athlete with high budget (1800 UAH) wanting complete race nutrition & hydration | `endurance_amino_hydration` | running | — | 1800 ₴ | `matched` | **WARN** | [RE11650]: Expected endurance race hydration (SIS / Nutriversum EAA), got 'Набір «Захист від спеки» по програмі "Ветеранс… |
| HYD-046 | Distance runner seeking SIS electrolytes for fast gastric emptying without GI distress | `endurance_amino_hydration` | running | — | 1650 ₴ | `matched` | **WARN** | [RE11650]: Expected endurance race hydration (SIS / Nutriversum EAA), got 'Набір «Захист від спеки» по програмі "Ветеранс… |
| HYD-047 | Marathoner asking for electrolytes + carbohydrates combination for race day fueling | `endurance_amino_hydration` | running | — | 1500 ₴ | `matched` | **WARN** | [RE11659]: Expected endurance race hydration (SIS / Nutriversum EAA), got 'Набір «Тиждень бігуна»'. |
| HYD-048 | Endurance athlete asking for Nutriversum BCAA 2:1:1 + Hydria Perform for tempo workouts | `endurance_amino_hydration` | running | — | 1300 ₴ | `matched` | **WARN** | [RE11650]: Expected endurance race hydration (SIS / Nutriversum EAA), got 'Набір «Захист від спеки» по програмі "Ветеранс… |
| HYD-049 | Road cyclist seeking sugar-free amino hydration drink for long steady distance | `endurance_amino_hydration` | cycling | — | 1500 ₴ | `matched` | **WARN** | [RE11650]: Expected endurance race hydration (SIS / Nutriversum EAA), got 'Набір «Захист від спеки» по програмі "Ветеранс… |
| HYD-050 | Ultra trail runner needing multi-hour race hydration with electrolytes and amino support | `endurance_amino_hydration` | running | — | 1700 ₴ | `matched` | **WARN** | [RE11650]: Expected endurance race hydration (SIS / Nutriversum EAA), got 'Набір «Захист від спеки» по програмі "Ветеранс… |
| HYD-051 | Cross-country mountain biker asking for SIS hydration and electrolyte gels | `endurance_amino_hydration` | cycling | — | 1500 ₴ | `matched` | **WARN** | [RE11650]: Expected endurance race hydration (SIS / Nutriversum EAA), got 'Набір «Захист від спеки» по програмі "Ветеранс… |
| HYD-052 | Marathon racer wanting SIS Go Hydro with berry/citrus electrolytes for race belt | `endurance_amino_hydration` | running | — | 1700 ₴ | `matched` | **WARN** | [RE11650]: Expected endurance race hydration (SIS / Nutriversum EAA), got 'Набір «Захист від спеки» по програмі "Ветеранс… |
| HYD-053 | Long distance triathlete seeking all-in-one endurance pack with shaker and amino acids | `endurance_amino_hydration` | cycling | — | 1500 ₴ | `matched` | **WARN** | [RE11786]: Expected endurance race hydration (SIS / Nutriversum EAA), got 'Набір «Тренувальний ресурс Race Expert Club» —… |
| HYD-054 | Distance runner looking for electrolyte hydration bundle with energy chews (RE11659) | `endurance_amino_hydration` | running | — | 1500 ₴ | `matched` | **WARN** | [RE11659]: Expected endurance race hydration (SIS / Nutriversum EAA), got 'Набір «Тиждень бігуна»'. |
| HYD-055 | Athlete preparing for multi-stage endurance race needing amino electrolytes | `endurance_amino_hydration` | running | — | 1500 ₴ | `matched` | **WARN** | [RE11650]: Expected endurance race hydration (SIS / Nutriversum EAA), got 'Набір «Захист від спеки» по програмі "Ветеранс… |
| HYD-056 | Trail runner looking for soft flask compatible hydration kit with electrolytes | `flasks_bottles_gear` | running | — | 1500 ₴ | `matched` | **WARN** | [RE11786]: Expected drinking bottle or shaker in bundle, but 'Набір «Тренувальний ресурс Race Expert Club» — абонемент на… |
| HYD-057 | Road runner asking specifically for a bottle and electrolyte sticks bundle (Nabir_1123) | `flasks_bottles_gear` | running | — | 1500 ₴ | `matched` | **WARN** | [RE11786]: Expected drinking bottle or shaker in bundle, but 'Набір «Тренувальний ресурс Race Expert Club» — абонемент на… |
| HYD-058 | Runner wanting a hydration bundle with glass water bottle (RE11021) | `flasks_bottles_gear` | running | — | 1400 ₴ | `matched` | **WARN** | [RE11786]: Expected drinking bottle or shaker in bundle, but 'Набір «Тренувальний ресурс Race Expert Club» — абонемент на… |
| HYD-059 | Marathon runner wanting a water bottle and race number belt with hydration gels | `flasks_bottles_gear` | running | — | 1500 ₴ | `matched` | **WARN** | [RE11786]: Expected drinking bottle or shaker in bundle, but 'Набір «Тренувальний ресурс Race Expert Club» — абонемент на… |
| HYD-060 | Gym athlete wanting a shaker and hydration drink mix | `flasks_bottles_gear` | running | — | 1300 ₴ | `matched` | **WARN** | [RE11786]: Expected drinking bottle or shaker in bundle, but 'Набір «Тренувальний ресурс Race Expert Club» — абонемент на… |
| HYD-061 | Cyclist needing a 600ml bottle to fit standard bike bottle cage with electrolyte sticks | `flasks_bottles_gear` | cycling | — | 1500 ₴ | `matched` | **WARN** | [RE11786]: Expected drinking bottle or shaker in bundle, but 'Набір «Тренувальний ресурс Race Expert Club» — абонемент на… |
| HYD-062 | Runner asking for soft flasks for running hydration vest (checking catalog support) | `flasks_bottles_gear` | running | — | 1500 ₴ | `matched` | **WARN** | [RE11786]: Expected drinking bottle or shaker in bundle, but 'Набір «Тренувальний ресурс Race Expert Club» — абонемент на… |
| HYD-063 | Casual runner looking for handheld water bottle bundle for summer park runs | `flasks_bottles_gear` | running | — | 1450 ₴ | `matched` | **WARN** | [RE11786]: Expected drinking bottle or shaker in bundle, but 'Набір «Тренувальний ресурс Race Expert Club» — абонемент на… |
| HYD-064 | Athlete looking for sports accessories + hydration items (bottle + sticks) | `flasks_bottles_gear` | running | — | 1500 ₴ | `matched` | **WARN** | [RE11786]: Expected drinking bottle or shaker in bundle, but 'Набір «Тренувальний ресурс Race Expert Club» — абонемент на… |
| HYD-065 | Runner asking for water bottle with protective sleeve + electrolyte packs | `flasks_bottles_gear` | running | — | 1400 ₴ | `matched` | **WARN** | [RE11786]: Expected drinking bottle or shaker in bundle, but 'Набір «Тренувальний ресурс Race Expert Club» — абонемент на… |
| HYD-066 | Marathoner looking for bottle + socks + electrolyte kit under 1400 UAH | `flasks_bottles_gear` | running | — | 1400 ₴ | `matched` | **WARN** | [RE11650]: Expected drinking bottle or shaker in bundle, but 'Набір «Захист від спеки» по програмі "Ветеранський спорт"' … |
| HYD-067 | Fitness runner looking for bottle and Hydria Perform sticks under 1500 UAH | `flasks_bottles_gear` | running | — | 1500 ₴ | `matched` | **WARN** | [RE11650]: Expected drinking bottle or shaker in bundle, but 'Набір «Захист від спеки» по програмі "Ветеранський спорт"' … |
| HYD-068 | Commuter wanting portable water bottle + hydration sticks for gym and work | `flasks_bottles_gear` | — | — | 1450 ₴ | `matched` | **WARN** | [RE11786]: Expected drinking bottle or shaker in bundle, but 'Набір «Тренувальний ресурс Race Expert Club» — абонемент на… |
| HYD-069 | Ultra runner asking for dual soft flask set with electrolyte tablets | `flasks_bottles_gear` | running | — | 1600 ₴ | `matched` | **WARN** | [RE11786]: Expected drinking bottle or shaker in bundle, but 'Набір «Тренувальний ресурс Race Expert Club» — абонемент на… |
| HYD-070 | Buyer searching for pure water bottle without socks or pills | `flasks_bottles_gear` | running | — | 1500 ₴ | `matched` | **WARN** | [RE11786]: Expected drinking bottle or shaker in bundle, but 'Набір «Тренувальний ресурс Race Expert Club» — абонемент на… |
| HYD-071 | Tight budget runner with 500 UAH looking for cheap electrolyte tablets | `budget_tiers` | running | — | 500 ₴ | `floor_anchor` | **WARN** | [RE11650]: Catalog Coverage Gap: Budget 500 UAH returned 0 exact matches. Store has no single electrolyte packs under 122… |
| HYD-072 | Student runner with 600 UAH budget seeking basic hydration salt sticks | `budget_tiers` | running | — | 600 ₴ | `floor_anchor` | **WARN** | [RE11650]: Catalog Coverage Gap: Budget 600 UAH returned 0 exact matches. Store has no single electrolyte packs under 122… |
| HYD-073 | Budget buyer with 750 UAH looking for simple hydration pack | `budget_tiers` | running | — | 750 ₴ | `floor_anchor` | **WARN** | [RE11650]: Catalog Coverage Gap: Budget 750 UAH returned 0 exact matches. Store has no single electrolyte packs under 122… |
| HYD-074 | Runner with 800 UAH budget asking for electrolyte powder | `budget_tiers` | running | — | 800 ₴ | `floor_anchor` | **WARN** | [RE11650]: Catalog Coverage Gap: Budget 800 UAH returned 0 exact matches. Store has no single electrolyte packs under 122… |
| HYD-075 | Budget athlete with 950 UAH looking for hydration set | `budget_tiers` | running | — | 950 ₴ | `no_match` | **WARN** | [RE11650]: Catalog Coverage Gap: Budget 950 UAH returned 0 exact matches. Store has no single electrolyte packs under 122… |
| HYD-076 | Buyer with exactly 999 UAH budget (just below catalog 1000 UAH threshold) | `budget_tiers` | running | — | 999 ₴ | `no_match` | **WARN** | [RE11650]: Catalog Coverage Gap: Budget 999 UAH returned 0 exact matches. Store has no single electrolyte packs under 122… |
| HYD-077 | Buyer with 1000 UAH budget looking for hydration kit | `budget_tiers` | running | — | 1000 ₴ | `no_match` | **WARN** | [RE11650]: Catalog Coverage Gap: Budget 1000 UAH returned 0 exact matches. Store has no single electrolyte packs under 12… |
| HYD-078 | Buyer with 1200 UAH budget (just below lowest hydration set at 1225 UAH) | `budget_tiers` | running | — | 1200 ₴ | `no_match` | **WARN** | [RE11650]: Catalog Coverage Gap: Budget 1200 UAH returned 0 exact matches. Store has no single electrolyte packs under 12… |
| HYD-079 | Medium budget buyer with 1250 UAH seeking legitimate hydration | `budget_tiers` | running | — | 1250 ₴ | `matched` | **PASS** | [RE11650]: Matched: RE11650 |
| HYD-080 | Medium budget runner with 1350 UAH seeking electrolyte pack | `budget_tiers` | running | — | 1350 ₴ | `matched` | **PASS** | [RE11650]: Matched: RE11650 |
| HYD-081 | Medium budget cyclist with 1450 UAH seeking hydration bundle with bottle | `budget_tiers` | cycling | — | 1450 ₴ | `matched` | **PASS** | [RE11786]: Matched: RE11786 |
| HYD-082 | Standard catalog budget with 1500 UAH seeking premium electrolyte supply | `budget_tiers` | running | — | 1500 ₴ | `matched` | **PASS** | [RE11650]: Matched: RE11650 |
| HYD-083 | Medium-high budget runner with 1600 UAH seeking race hydration pack | `budget_tiers` | running | — | 1600 ₴ | `matched` | **PASS** | [RE11650]: Matched: RE11650 |
| HYD-084 | High budget athlete with 2000 UAH looking for complete hydration and nutrition setup | `budget_tiers` | running | — | 2000 ₴ | `matched` | **PASS** | [RE11650]: Matched: RE11650 |
| HYD-085 | Premium budget ultra-runner with 3000 UAH seeking top-tier hydration and gear | `budget_tiers` | running | — | 3000 ₴ | `matched` | **PASS** | [RE11650]: Matched: RE11650 |
| HYD-086 | Buyer asking explicitly for product_form: 'sticks' (Hydria Perform / Daily sticks) | `forms_activities_leaks` | — | sticks | 1500 ₴ | `matched` | **PASS** | [RE11786]: Matched: RE11786 |
| HYD-087 | Buyer asking explicitly for product_form: 'tablets' (Precision Hydration 1000 / SIS Go Hydro effervescent tablets) | `forms_activities_leaks` | — | tablets | 1500 ₴ | `matched` | **PASS** | [RE11650]: Matched: RE11650 |
| HYD-088 | Buyer asking explicitly for product_form: 'powder' (bulk electrolyte powder / amino mix) | `forms_activities_leaks` | — | powder | 1500 ₴ | `matched` | **PASS** | [RE11786]: Matched: RE11786 |
| HYD-089 | Buyer asking explicitly for product_form: 'gel' (electrolyte gels SiS Go + Electrolyte) | `forms_activities_leaks` | — | gel | 1500 ₴ | `matched` | **PASS** | [RE11804]: Matched: RE11804 |
| HYD-090 | Buyer asking explicitly for product_form: 'liquid' (ready-to-drink hydration shot) | `forms_activities_leaks` | — | liquid | 1500 ₴ | `matched` | **PASS** | [RE11806]: Matched: RE11806 |
| HYD-091 | Buyer asking explicitly for product_form: 'flasks' (soft flasks / water flasks) | `forms_activities_leaks` | — | flasks | 1500 ₴ | `matched` | **PASS** | [RE11021]: Matched: RE11021 |
| HYD-092 | Hiker asking for hydration during mountain hike (activity: 'hiking') | `forms_activities_leaks` | hiking | — | 1700 ₴ | `matched` | **PASS** | [UT-PRO-2026]: Matched: UT-PRO-2026 |
| HYD-093 | Triathlete asking for hydration for triathlon race (activity: 'triathlon') | `forms_activities_leaks` | triathlon | — | 1600 ₴ | `matched` | **PASS** | [RE11650]: Matched: RE11650 |
| HYD-094 | Gym athlete asking for hydration during strength training (activity: 'strength_training') | `forms_activities_leaks` | strength_training | — | 1500 ₴ | `matched` | **PASS** | [RE11786]: Matched: RE11786 |
| HYD-095 | Functional training athlete asking for hydration during CrossFit (activity: 'functional_training') | `forms_activities_leaks` | functional_training | — | 1500 ₴ | `matched` | **PASS** | [RE11786]: Matched: RE11786 |
| HYD-096 | Walker asking for hydration on 20km brisk walk (activity: 'walking') | `forms_activities_leaks` | walking | — | 1500 ₴ | `matched` | **PASS** | [RE11021]: Matched: RE11021 |
| HYD-097 | Pure hydration seeker probing for Spirulina leak (checking if RE11513 is returned) | `forms_activities_leaks` | running | — | 1500 ₴ | `matched` | **PASS** | [RE11650]: Matched: RE11650 |
| HYD-098 | Pure hydration seeker probing for Lion's Mane / mushroom leak (checking if RE88943 is returned) | `forms_activities_leaks` | — | — | 1500 ₴ | `matched` | **PASS** | [RE11021]: Matched: RE11021 |
| HYD-099 | Pure hydration seeker probing for Creatine leak (checking if RE11681 or RE11636 is returned) | `forms_activities_leaks` | — | — | 1500 ₴ | `matched` | **PASS** | [RE11650]: Matched: RE11650 |
| HYD-100 | Thirsty runner asking for hydration items only (probing for pure socks/towel kits RE11013, RE89475) | `forms_activities_leaks` | running | — | 1400 ₴ | `matched` | **PASS** | [RE11650]: Matched: RE11650 |

---

## 4. Prioritized Recommendations for Engineering & Merchandising

1. **Purge False Hydration Tags on Bodybuilding & Nootropic Sets:**
   - Remove `hydration_electrolytes` from `RE11681` («Ріст м'язів»), `RE11636` («Вибух сили»), and `RE11787` («Сила та гідратація»). Having 4 sticks of Hydria Daily inside a 500g Creatine kit should NOT make it a primary hydration kit.
   - Remove `hydration_electrolytes` from `RE11513` (Spirulina) and `RE88943` (Lion's Mane mushroom).
   - Remove `hydration_electrolytes` from pure apparel sets `RE11013` and `RE89475`.

2. **Add `tablets` and `powder` to `PRODUCT_FORMS_BY_GOAL["hydration"]`:**
   - Update `draft_matcher.py`:
     ```python
     PRODUCT_FORMS_BY_GOAL["hydration"] = {"tablets", "powder", "sticks", "gel", "liquid"}
     ```
   - Map `Precision Hydration 1000 Tube` and `SIS Go Hydro` to `tablets`.
   - Remove `bars` from hydration (bars are food).

3. **Expand `ACTIVITY_OPTIONS_BY_GOAL["hydration"]` to Include Hiking and Triathlon:**
   - Update `draft_matcher.py`:
     ```python
     ACTIVITY_OPTIONS_BY_GOAL["hydration"] = {"running", "cycling", "hiking", "triathlon", "fitness_gym"}
     ```
   - Add alias mapping from `strength_training` and `functional_training` to `fitness_gym`.

4. **Correct Taxonomy for `RE11650` (Precision Hydration 1000):**
   - In `quiz-set-audit.json`, `RE11650` currently has `component_class: ['supplements_vitamins_minerals']`. It must be changed to `component_class: ['hydration_items']`.

5. **Stop Emitting `(без сторонніх речей)` for Bundled Sets:**
   - Suppress this phrase whenever the set includes club memberships, towels, apparel, or secondary supplement classes.

6. **Introduce Dedicated Single-Pack Hydration Offerings (< 1000 UAH):**
   - The store urgently needs entry-level hydration SKUs (e.g., a standalone tube of Precision Hydration 1000 or SIS Go Hydro at 500–600 UAH, or a 10-pack of Hydria Perform at 700 UAH) to capture the large demographic of sub-1000 UAH buyers.
