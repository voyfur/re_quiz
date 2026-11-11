# Test plan: Race Expert quiz sandbox

**Status:** local test only; matching rules are experimental and not approved for production.  
**Source:** [`spec.md`](../spec.md), [the 206-set analysis](../wiki/projects/race-expert-need-sets-206-analysis.md), and the user's request on 2026-11-09.  
**Implementation boundary:** separate folder; no website, cart, live catalog, Telegram, or production questionnaire connection.

## Goal

Demonstrate how a quiz can use the analyzed set tags and composition to return up to **1, 2, or 3 alternative ready sets** with a visible reason for each match. A result is a catalog match for review, not a health claim, safety certification, or instruction to combine or consume the returned sets.

## Data and limits

- Use the 206 analyzed «За потребами» records and preserve each source URL and catalog row/SKU when present. The source prices are a snapshot from 2026-11-06, not live prices.
- Availability tags are also part of this fixed snapshot; they do not indicate current stock.
- Current coverage includes 154 `purpose` values, 19 `sport` values, 69 `contains` values, 47 prices, 39 shoe-size assignments, and 24 explicit `availability:in_stock` tags.
- All 206 records have `buyer_weight:not_specified`; no numeric distance is recorded.
- `contains:caffeine` is present for rows 38, 136, 148, and 206. Only row 206 has `caffeine_per_set:400_mg`. A missing caffeine tag is unknown, not confirmed absence; the current data contains no set-level confirmed caffeine-free state.
- Audience labels are seller positioning, not age eligibility. Allergens and dietary exclusions are not normalized across the set components.

## Test-only matching behavior

The sandbox uses deterministic, readable heuristics so the same answers always produce the same results. Every rule below is marked as a prototype choice, not an owner-approved business rule.

1. If a `purpose` is selected, require an exact `purpose` tag match.
2. If a sport is selected, rank an exact sport tag above `sport:not_sport_specific`; never infer sport fit from a supplement claim or club subscription.
3. If a maximum budget is entered, exclude sets whose full snapshot price exceeds it. Show the snapshot date beside every price.
4. If shoe size is entered, a size-tagged set is eligible only when the selected size falls within its tagged range. A set without a size tag receives no size-match credit and is labelled “size not recorded.”
5. If the buyer requires a verified caffeine-free set, include only a set with an explicit set-level `confirmed_absent` state. Since the current analysis has no such state, the expected result is no candidates with an explanation that the catalog data is insufficient. Never infer “caffeine-free” from a missing tag.
6. If “in stock only” is selected, include only records explicitly tagged in stock. The other 182 analyzed sets remain unknown, not out of stock.
7. Apply selected purpose/type/form/race-format/component filters as exact matches. Then rank by exact sport over general sport, a recorded size-range match over an untagged size, lower snapshot price, and source catalog row. Return no duplicates and at most the requested 1–3 results. If fewer sets qualify, return fewer; if none qualify, return an empty result with a plain explanation.
8. Treat multiple results as alternatives. Do not claim the sets are compatible with each other or intended to be used together.

Filters for buyer weight, age eligibility, allergens, medication interactions, pregnancy, dosing, exact kilometer distance, and intake duration/period are not offered as working quiz inputs in this sandbox. The API rejects these filters rather than silently ignoring them. The `3_months` tag can identify a club membership period, so it is not treated as a product intake duration.

## Safety and isolation checks

- Every page and result carries a visible `TEST ONLY` notice that the matching logic is unapproved and the result is not medical advice.
- Result explanations cite only matching tags and catalog text, using wording such as “matches the catalog tags,” never “safe,” “treats,” or “will improve.”
- Show known caffeine presence, unknown caffeine status, stock state, price date, composition, and source distinctly.
- A hard restriction fails closed when the required attribute is unknown. It must not substitute an unverified set just to fill the requested number of results.
- Do not display dosing schedules, contraindication judgments, efficacy statements, or compatibility advice.
- Bind the test service to localhost, make no automatic outbound requests, do not persist visitor answers, and do not change the existing owner questionnaire. Product-source links open only when the user clicks them.
- No purchase/cart action is enabled. The source product URL is reference information only.

## Test scenarios and expected outcomes

| Case | Input or fixture | Expected behavior |
|---|---|---|
| Catalog completeness | Build the local catalog from the maintained 206-set analysis | Exactly 206 unique analyzed records; required source, row ID, price, title, and tags are preserved where present; excluded distance-category rows are absent. |
| Result count | A broad purpose with enough candidates; requested count 1, 2, then 3 | Return exactly 1/2/3 distinct alternatives, deterministically ordered. |
| Fewer matches | A purpose/size combination with fewer than requested results | Return only qualifying candidates; show that fewer matched. Never pad with unrelated sets. |
| No match | A valid catalog purpose plus a budget/other filter that excludes all candidates | Return zero results and an explanation; no random fallback. A tag value absent from the catalog is a validation error. |
| Purpose and sport | Select a purpose tag and sport | Every result matches the selected purpose; exact sport tags rank ahead of general sport. Explanations name the matching tags. |
| Budget boundary | Row 206 at 1,500 UAH; max 1,499 then 1,500 | Excluded at 1,499, eligible at 1,500; display UAH and snapshot date. |
| Shoe-size range | Size 42 against a `40-42` set, then size 43 | 42 matches inclusively; 43 does not. Other sets show size unknown, not matching. |
| Caffeine unknown | Require confirmed caffeine-free | Return no candidate because the set-level absence state is not recorded. Rows 38/136/148/206 are identified as containing caffeine; row 206 displays 400 mg per set. |
| Stock unknown | Enable in-stock-only | Return only explicitly tagged `in_stock` sets; never label untagged entries out of stock. |
| Unsupported safety filter | Submit age, allergy, or buyer-weight hard filter | Reject as unsupported/insufficient data; return no recommendation based on guessed suitability. |
| Input validation | Result count outside 1–3, invalid size, or negative budget | Return a clear validation error and no candidates. |
| Local-only behavior | Inspect requests and run the sandbox | Only local routes are used; no answers are saved, and the existing questionnaire/server behavior is unchanged. |

## Acceptance

The implementation has a 206-record source-linked catalog, deterministic matcher, bilingual local page and API, and 26 passing unit/handler tests. The live browser check verified 1/2/3 results, strict caffeine filtering, budget boundaries (1,499/1,500 UAH), shoe sizes 42/43, Ukrainian result copy, and a 390×844 mobile viewport with no horizontal overflow.

This plan does not approve the test heuristics for the production quiz. The later website connection and production rule approval remain separate work.
