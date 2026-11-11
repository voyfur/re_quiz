---
type: "query"
date: "2026-11-10T06:45:17.657522+00:00"
question: "Какие правила нужны для production? Что сейчас не так? Что сейчас не хватает для того, чтобы этот квиз был просто production-версии?"
contributor: "graphify"
source_nodes: ["Quiz Matching Rules Technical Brief", "Owner Approval of Matching Rules", "Catalog Access and Matching Requirements", "Owner Answers on Quiz Logic", "Buyer-Selected Budget Input", "Product-Set Quiz Project"]
---

# Q: Какие правила нужны для production? Что сейчас не так? Что сейчас не хватает для того, чтобы этот квиз был просто production-версии?

## Answer

Expanded from original query via vocab: [quiz, matching, rule, catalog, data, price, availability, owner, integration, set, backend, source]. Verified against the current wiki/spec: v1 is ready-made sets only, but the 206 audited records are not an approved recommendation allowlist. The owner still needs to approve eligible SKUs, hard versus soft fields, ranking/ties/result count, no-match and fallback behavior, membership handling, budget boundaries and unavailable-item behavior. The proposed budget bands overlap at 1500 UAH. The current sandbox audit reduced known answer conflicts to 0/100, but exact results are empty in 47/100 cases; 11 source-conflict records remain unresolved, 9/108 shown cards carry a composition-conflict marker, and club-membership bundles appear often. These metrics check consistency with current evidence, not commercial correctness. Catalog evidence is incomplete (132 of 206 pages have archived text, 74 do not; 548 of 728 component rows have unknown/ambiguous quantity; only 7 independent component product records); caffeine/allergen/safety and exact distance are not adequately supported. The preview uses a local test-only JSON snapshot dated 2026-11-06 and a loopback-only server, with no live price/stock adapter or site integration. Minimal production can stay within ready-made sets, use an owner-approved structured catalog behind an adapter without choosing MySQL now, exclude unsupported safety claims, return a clear no-match state, disclose memberships, and link to set pages; cart support requires separate approval.

## Source Nodes

- Quiz Matching Rules Technical Brief
- Owner Approval of Matching Rules
- Catalog Access and Matching Requirements
- Owner Answers on Quiz Logic
- Buyer-Selected Budget Input
- Product-Set Quiz Project