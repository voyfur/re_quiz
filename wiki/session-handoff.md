# Session Handoff

## Active Context

- Last session: `raw/sessions/2026-11-11-implement-live-stock-availability-checking-via-o.md`
- Current objective: Implement live stock availability checking via OpenCart MySQL over TLS and publish quiz to GitHub

## Current Decisions

- OpenCart stock rule is verified as: status == 1 and quantity > 0.
- Stock checking subsystem operates via standard library TLS socket to MySQL on VPS-61125, supporting auto SSH tunnel when local direct access is blocked.
- Matching engine prioritizes in-stock items with -int(in_stock) and promotes Next Best Match if top kit is out of stock.
- Entire codebase and knowledge base published to GitHub at https://github.com/voyfur/re_quiz on main branch with .env excluded.

## Open Tasks

- Store owner review of wording and live feedback on the external IP deployment (http://172.20.10.6:8080/).
- Test onboarding skill with live product URLs provided by the store owner.

## Blockers

- No blockers recorded.

## Next Action

- Continue with store owner review, live link onboarding tests, or OpenCart production storefront integration.

## Relevant Pages

- wiki/projects/quiz-engine-technical-documentation.md
- wiki/projects/quiz-test-sandbox.md
- wiki/sources/mysql-readonly-access-and-product-query-guide.md
- wiki/index.md
