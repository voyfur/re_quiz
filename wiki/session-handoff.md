# Session Handoff

## Active Context

- Last session: `raw/sessions/2026-11-11-implement-live-stock-availability-checking-via-o.md`
- Current objective: Deploy standalone bilingual Race Expert Quiz to production VPS (185.25.119.96) with live OpenCart MySQL stock verification

## Current Decisions

- Deployed Race Expert Quiz to VPS-61125 (http://185.25.119.96/) replacing the old owner discovery questionnaire (which was backed up to /opt/race-expert-quiz/backups/questionnaire-pre-quiz-v1-20261111).
- Connected live OpenCart MySQL stock verification directly over TLS 1.3 via /api/check-stock endpoint.
- OpenCart stock rule is verified: status == 1 and quantity > 0.
- Client UI asynchronously queries /api/check-stock for rendered recommendations and dynamically updates live price and stock status.
- UI fully bilingual (UK/RU) with instant toggle, responsive layout, and resizable preview widget.
- 44 automated tests in pytest passing.

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
