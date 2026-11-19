# Running Custom Box Builder Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a deterministic 4-slot running nutrition and gear box builder that takes 7 user preferences and dynamically selects matching products from the live 458-item OpenCart running catalog (`running_catalog.json`) with interactive checkboxes and one-click cart checkout.

**Architecture:** A lightweight deterministic matching engine calculates physiological requirements (carbohydrates per hour, sodium/electrolytes for temperature, caffeine pacing, anti-chafe protection, and carrying logistics). It filters products by slot, price tier, and constraints, returning a structured box payload with pre-checked items. A reactive frontend renders the 7 steps and final box with live total calculation, dispatching an asynchronous multi-add queue to OpenCart's AJAX cart endpoint.

**Tech Stack:** Python 3 (Backend & Engine), Pytest (TDD Suite), OpenCart MySQL Readonly, Modern Vanilla JavaScript (Fetch/Async Queue), Tailwind CSS (Dark UI).

**Spec:** [spec_running_custom_box.md](../../spec_running_custom_box.md)

## Global Constraints

- Inventory constraint: Only products with `quantity > 0` and `status = 1` may be recommended.
- Caffeine safety: If `caffeine_preference == 'none'`, zero caffeine items are permitted in any slot under any circumstance.
- Price tier fidelity: Selected products must strictly respect the chosen tier (`economy`, `standard`, `premium`) unless an explicit upsell is triggered.
- OpenCart cart protocol: Multi-add must operate via sequential POST requests to `index.php?route=checkout/cart/add` with error detection for missing options.
- Performance: Box compilation execution time must be under 50ms from static memory cache.

## Review Focus

1. **Zero-caffeine leak:** User selects no caffeine, but a combo product with natural guarana/caffeine is included.
2. **Out-of-stock collision:** Product quantity drops to zero while user is in quiz; fallback must smoothly replace with next best item in same tier.
3. **Mandatory option failure:** Item requires flavor/size selection in OpenCart (`error_option_required`); frontend must link to product page instead of failing silently.
4. **Extreme weather dehydration:** Hot weather (+20°C) with long distance (42k) failing to provide salt capsules.
5. **Checkbox de-selection math:** Unchecking an item does not immediately update the subtotal and checkout payload.

---

### Task 1: Runner Box Decision Engine (`runner_box_engine.py`)

**Files:**
- Create: `runner_box_engine.py`
- Test: `test_runner_box_engine.py`

**Interfaces:**
- Consumes: `QuizUserInput` dict, `catalog` list of `RunningCatalogItem`.
- Produces: `generate_runner_box(inputs: dict, catalog: list) -> dict` returning `GeneratedRunnerBox`.

- [x] **Step 1: Write the failing tests for engine logic and safety constraints**
- [x] **Step 2: Run test to verify it fails**
- [x] **Step 3: Implement minimal engine code in `runner_box_engine.py`**
- [x] **Step 4: Run test to verify it passes**

---

### Task 2: Real Catalog TDD Verification (`test_real_catalog_validation.py`)

**Files:**
- Create: `test_real_catalog_validation.py`
- Uses: `running_catalog.json`

- [x] **Step 1: Write integration tests verifying all 458 real products against domain rules**
- [x] **Step 2: Run test and verify 100% pass rate on live catalog**

---

### Task 3: Interactive Frontend & Reactive Checkboxes UI

**Files:**
- Create: `public/runner_box.html`
- Create: `public/runner_box.js`

**Interfaces:**
- Consumes: `/api/generate-runner-box` (POST payload `QuizUserInput`)
- Produces: Visual box with reactive price calculation and checkout button dispatching OpenCart AJAX multi-add.

- [x] **Step 1: Build the 7-question stepper component in Tailwind CSS**
- [x] **Step 2: Build the 4-slot result card with checkbox toggle event listeners**
- [x] **Step 3: Implement the multi-add queue in `runner_box.js`**

---

### Task 4: Deployment & Daily Sync Daemon

**Files:**
- Modify: `server.py` (Add `/api/generate-runner-box` endpoint)
- Test: `curl -s http://localhost:8000/api/health`

- [x] **Step 1: Mount engine and catalog in `server.py`**
- [x] **Step 2: Verify local server on port 8000**
- [ ] **Step 3: Deploy to VPS `185.25.119.96`**
