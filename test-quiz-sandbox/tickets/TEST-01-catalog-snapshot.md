# TEST-01: Extract the 206-set snapshot into the sandbox

**What to build:** The local quiz can read a normalized, source-linked copy of the 206 analyzed ready sets and expose their supported tags without editing the maintained Wiki data.

**Blocked by:** None.

**Status:** test-only / implemented

- [x] Parse all 206 in-scope records across the three analysis formats and reject duplicates or missing records.
- [x] Preserve catalog row, SKU when present, title, source URL, price snapshot, composition/description, tags, and data-quality flags.
- [x] Treat absent fields as unknown and keep the 2026-11-06 price snapshot date visible.
- [x] Exclude the 19 distance-category records; never use the extra catalog rows as silent candidates.
