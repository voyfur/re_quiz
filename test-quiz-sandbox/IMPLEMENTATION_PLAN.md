# Test-only quiz sandbox Implementation Plan

> **For agentic workers:** Implement this plan task by task. Keep the test-only sandbox isolated from the existing owner questionnaire.

**Goal:** Run a local bilingual quiz demo that deterministically returns up to three alternative sets from the 206-set source snapshot, with transparent reasons and conservative unknown-data handling.

**Architecture:** A standard-library Python HTTP server serves a small responsive browser UI and JSON endpoints. A build script converts the maintained 206-set analysis into a local catalog snapshot; the matcher operates only on that normalized snapshot and is independently testable.

**Tech Stack:** Python standard library, `unittest`, semantic HTML, vanilla JavaScript, and CSS. No network or third-party runtime dependencies.

---

## Files

- `catalog_builder.py` parses the current maintained analysis and writes `catalog.json` with 206 unique rows, tags, descriptions, prices, and source URLs.
- `matcher.py` validates test inputs, applies exact tag filters, conservative unknown-state policies, deterministic ranking, and result explanations.
- `server.py` provides localhost-only static and JSON routes; it does not import or modify the existing app server.
- `web/index.html`, `web/app.js`, `web/styles.css` provide a bilingual local test interface with a prominent test-only notice.
- `tests/test_catalog.py`, `tests/test_matcher.py`, `tests/test_api.py` verify extracted data, selection behavior, safety states, and the HTTP contract.
- `README.md`, `TEST_PLAN.md`, and `tickets/` define isolation, scope, checks, and test-only work items.

## Tasks

**Implementation status:** catalog extraction, matcher, localhost API, bilingual page, and automated tests are implemented. All 26 unit/handler tests pass. The running page was checked in a browser for 1/2/3 results, strict caffeine filtering, budget boundaries, shoe-size matching, Ukrainian copy, and a 390×844 mobile viewport with no horizontal overflow.

### Task 1: Lock the behavior with catalog and matcher tests

1. Add failing tests for 206 unique records, all required tag namespaces, snapshot price parsing, top-N limits, purpose/sport ranking, budget boundary, shoe-size ranges, caffeine unknown behavior, in-stock-only behavior, no-match behavior, and rejection of unsupported safety filters.
2. Run `python3 -m unittest discover -s tests -v` from this directory and confirm the failures identify missing catalog/matcher behavior.

### Task 2: Parse the maintained 206-set analysis into the local catalog

1. Implement record-boundary parsing for the three formats used in the analysis: headings 1–24, numbered records 25–75, and bullet records 76–210.
2. Parse each record's source index, SKU/title, tags, price, composition/description, and first official set-card URL without inferring absent values.
3. Fail catalog generation unless it produces 206 unique in-scope records with no duplicate source indices. Preserve the exact evidence text needed for the result explanation.
4. Generate the sandbox `catalog.json` and run the catalog tests.

### Task 3: Implement deterministic, fail-closed matching

1. Validate request values (`result_count` 1–3, nonnegative integer UAH budget, catalog-backed tag values, supported shoe sizes, and allowed caffeine modes).
2. Apply exact selected purpose, budget, typed attributes, shoe-size-range, strict caffeine, and confirmed-stock rules.
3. Apply selected tag filters exactly, then rank exact sport matches above general-sport sets, recorded size-range matches above untagged size data, lower snapshot price, and source row; return no fallback candidates.
4. Include match reasons, source fields, price date, caffeine state, and availability state in each result; label multiple matches as alternatives.
5. Run matcher tests and retain no-result behavior for hard constraints whose data is unknown.

### Task 4: Expose the local JSON API and bilingual quiz page

1. Add the local server routes for quiz options and recommendation requests; bind to `127.0.0.1` and load only the generated local catalog.
2. Add the Russian/Ukrainian interface, test-only notice, filters represented by catalog data, result-count selector, result cards, explanations, unknown-state badges, and source reference.
3. Keep external purchase actions disabled and do not store submitted answers.
4. Run API tests, then manually open the local page and verify 1/2/3 results, zero-result safety cases, language switching, and mobile layout.

### Task 5: Verify the isolation and review deliverables

1. Run `python3 -m unittest discover -s tests -v` and confirm all tests pass.
2. Start the server, verify the test-only banner, API response structure, source links, and catalog count in the browser.
3. Confirm the root `index.html`, root `server.py`, Wiki analysis, and production `spec.md` were not modified by implementation.
