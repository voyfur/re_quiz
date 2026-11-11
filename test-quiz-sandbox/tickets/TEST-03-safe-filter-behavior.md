# TEST-03: Keep budget and restriction filters source-backed

**What to build:** The local result flow applies optional budget, shoe-size, caffeine, and stock constraints without turning unknown catalog values into confirmed claims.

**Blocked by:** TEST-02: Match answers to 1–3 alternative sets.

**Status:** test-only / implemented

- [x] Apply a numeric UAH ceiling to the full set price and show the source snapshot date.
- [x] Match a selected shoe size only against a recorded size range; do not infer a size for untagged sets.
- [x] For strict caffeine avoidance, accept only a confirmed set-level absence; with current data, explain that the evidence is insufficient and return no candidates.
- [x] In stock-only mode, return only explicit `availability:in_stock` records; label every untagged status unknown.
- [x] Reject unsupported age, allergy, buyer-weight, interaction, and numeric-distance filters rather than silently ignoring them.
