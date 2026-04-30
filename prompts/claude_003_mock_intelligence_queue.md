# Claude Prompt 003 - Mock Intelligence Pipeline And Review Queue

ROLE CHECK: Claude
WHY: This is implementation work for Watchtower services, storage, API, and admin UI behavior.
ACTION: proceed

## Goal

Build the first deterministic intelligence pipeline that turns existing mock
snapshots into review queue items through filters and routing rules.

Do not add real providers yet. This step proves the flow:

```text
mock snapshots
-> filter matching
-> routing rule evaluation
-> review_queue item creation
-> admin UI inspection
```

## Read First

- `AGENTS.md`
- `DOC/collaboration/ai_role_protocol.md`
- `DOC/collaboration/context_tool_profiles.md`
- `DOC/mission.md`
- `DOC/architecture.md`
- `DOC/specs/settings_and_web_integration.md`
- `DOC/vultureinv_integration_contract.md`
- `DOC/openclaw_news_report_plan.md`
- `DOC/watchtower_admin_ui_plan.md`
- `DOC/state/CURRENT_CONTEXT.md`

## Current Baseline

Implemented and pushed:
- FastAPI scaffold
- mock ingestion snapshots
- `/health`
- `/status`
- `/snapshots/{regime,flow,catalysts}/latest`
- `/jobs/refresh/mock`
- `/settings/redacted`
- `/filters`
- `/routing`
- `/review-queue`
- `/admin`

`macmini-dashboard` is only the operations monitor. Do not expand it.

## Scope

Implement a local-only deterministic pipeline using existing mock data and
existing SQLite persistence.

Recommended new/changed pieces:

```text
app/services/intelligence_service.py
app/api/routes/intelligence.py
app/storage/sqlite_store.py
app/api/routes/admin.py
app/main.py
```

Use existing project patterns if better names already exist.

## Required API

Add:

```text
POST /intelligence/run/mock
```

Behavior:
- reads latest mock snapshots for `regime`, `flow`, and `catalysts`,
- reads filters and routing rules,
- creates review queue items only for matched/routed content,
- returns:
  - `ok`
  - `created_count`
  - `skipped_count`
  - `matched_filters`
  - `warnings`

Optional but useful:

```text
GET /intelligence/status
```

Behavior:
- returns latest run summary if stored,
- returns review queue counts by status.

## Filter Matching v1

Use simple deterministic matching.

For each candidate item from snapshots:
- market scope must match if the item has a market.
- symbol must match if filter `symbols` is non-empty and the item has a symbol.
- source type must match:
  - `flow` snapshot -> `flow`
  - `catalysts` snapshot -> `disclosure` or `news`
  - `regime` snapshot -> `macro`
- include keywords match title/content/note when provided.
- exclude keywords block item when matched.

Do not use AI for matching.

## Routing v1

For matched filters:
- if matching routing rule has destination `review_queue`, create a review queue
  item.
- if no routing rule exists but filter `requires_owner_review` is true, create a
  review queue item.
- do not send Telegram yet.
- do not call VultureInv yet.
- do not call OpenClaw yet.

## Review Queue Items

Each generated review queue item should include enough data for audit:

```text
source_type
snapshot_id
title
content
matched_filter_id
routing_rule_id
status = pending
```

Avoid creating duplicates across repeated runs.

Acceptable duplicate key:

```text
snapshot_id + source_type + title + matched_filter_id
```

Implement this in the store if practical.

## Admin UI Updates

Update `/admin`:
- add a "Run Mock Intelligence" button in Review Queue or Sources.
- show created/skipped result.
- show queue counts by status if `/intelligence/status` is implemented.
- keep UI local/admin-only and dense.

Do not expose tokens, API keys, `.env`, or raw secret-bearing config.

## OpenClaw Policy

OpenClaw is not used in this step.

Do not add calls to:
- OpenClaw,
- Gemini,
- Grok,
- external news APIs,
- real KRX/FRED/OpenDART/SEC providers.

## Validation

Run:

```bash
./scripts/validate.sh
python3 -m py_compile $(find app -name '*.py' -not -path '*/__pycache__/*')
```

Manual checks:

```bash
./scripts/run_api.sh
curl http://127.0.0.1:8010/health
curl http://127.0.0.1:8010/status
curl http://127.0.0.1:8010/filters
curl http://127.0.0.1:8010/routing
curl http://127.0.0.1:8010/review-queue
curl -X POST http://127.0.0.1:8010/intelligence/run/mock
curl http://127.0.0.1:8010/review-queue
```

Open:

```text
http://127.0.0.1:8010/admin
```

## Completion Report

Include:
- changed files,
- run commands,
- validation output,
- `POST /intelligence/run/mock` response,
- review queue count before/after,
- what remains mock/local-only,
- `git status --short --branch`.
