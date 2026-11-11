# TEST-02: Match answers to 1–3 alternative sets

**What to build:** A local test quiz accepts catalog-backed answers and returns one, two, or three distinct set alternatives with a concise explanation tied to exact tags and source text.

**Blocked by:** TEST-01: Extract the 206-set snapshot into the sandbox.

**Status:** test-only / implemented

- [x] Support purpose and sport selection using only values present in the local catalog.
- [x] Rank exact sport matches ahead of `not_sport_specific` sets and use stable tie-breaking.
- [x] Return no more than the requested 1–3 results; return fewer or none instead of padding with unrelated sets.
- [x] Show each set's composition, source reference, snapshot price date, and why it matched.
- [x] Label returned sets as alternatives, not a combined regimen or compatibility recommendation.
