# TEST-04: Serve the sandbox through a bilingual local API and page

**What to build:** A reviewer can run the test-only quiz locally in Ukrainian or Russian, inspect its recommendation behavior, and verify it has no production side effects.

**Blocked by:** TEST-02: Match answers to 1–3 alternative sets; TEST-03: Keep budget and restriction filters source-backed.

**Status:** test-only / implemented and browser-checked

- [x] Serve quiz options and recommendation responses from local JSON routes on localhost only.
- [x] Provide Russian and Ukrainian labels, a persistent `TEST ONLY` notice, and source-backed result cards.
- [x] Disable purchase/cart actions; make no network or Telegram calls and persist no answers.
- [x] Pass handler and matcher tests for counts 1/2/3, budget boundaries, shoe-size ranges, caffeine unknowns, stock unknowns, no match, and unsupported filters.
- [x] Open the running page in a browser; verify request flow, 1/2/3 results, zero results for strict caffeine-free mode, 1,499/1,500 UAH budget boundary, shoe sizes 42/43, Russian/Ukrainian copy, and the 390×844 mobile layout with no horizontal overflow.
