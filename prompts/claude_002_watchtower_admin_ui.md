# Claude Prompt 002 - Watchtower Admin UI v1

ROLE CHECK: Claude
WHY: This is implementation work for Watchtower UI/API files.
ACTION: proceed

## Goal

Implement Watchtower Admin UI v1 for local configuration and intelligence
routing control.

This is not the VultureInv investment cockpit and not the macmini-dashboard
operations monitor. It is the local admin surface for filters, routing, source
health, and review queue.

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

## Current Related Systems

- macmini-dashboard: `/Users/macmini/code/macmini-dashboard`
  - operations monitor at `http://localhost:3000`
  - do not expand it into the admin/editor surface.
- Watchtower API:
  - repo: `/Users/macmini/code/vultureinv-watchtower/vultureinv-watchtower`
  - run: `./scripts/run_api.sh`
  - base URL: `http://127.0.0.1:8010`
- OpenClaw:
  - gateway/control layer on Mac mini
  - use only for owner-triggered summaries from stored source bundles.

## Scope

Implement v1 using the existing FastAPI app.

Required UI route:

```text
GET /admin
```

Required safe API routes:

```text
GET /filters
POST /filters
GET /routing
POST /routing
GET /review-queue
GET /settings/redacted
```

If existing route structure suggests `/admin/*` APIs are cleaner, use that, but
do not break existing `/health`, `/status`, `/settings/redacted`, `/snapshots/*`,
or `/jobs/refresh/mock`.

## UI Requirements

Desktop-first local admin. Keep it dense and operational.

Tabs or sections:
- Status
- Sources
- Filters
- Routing
- Review Queue
- Telegram
- AI Providers

Show:
- API/scheduler/storage health,
- provider configured/enabled state,
- latest job run,
- snapshot freshness,
- Telegram configured/allowed chat count,
- AI providers configured/live-enabled state,
- filter list,
- routing rules,
- pending review queue items.

Do not show:
- API keys,
- Telegram bot token,
- OpenClaw gateway token,
- `.env` contents,
- raw secret-bearing config.

## Filter Schema v1

Use this shape unless repository patterns suggest a better name:

```json
{
  "id": "string",
  "enabled": true,
  "name": "string",
  "market_scope": ["KR", "US", "KR_ETF", "US_ETF"],
  "symbols": [],
  "sectors": [],
  "keywords_include": [],
  "keywords_exclude": [],
  "source_types": ["news", "disclosure", "macro", "flow"],
  "min_importance": "medium",
  "freshness_window_minutes": 1440,
  "telegram_enabled": false,
  "vultureinv_enabled": true,
  "requires_owner_review": true
}
```

## Routing Schema v1

```json
{
  "id": "string",
  "enabled": true,
  "filter_id": "string",
  "destinations": ["review_queue"],
  "explain": true
}
```

Destinations:
- `review_queue`
- `telegram_brief`
- `vultureinv_snapshot`

## Persistence

Prefer existing SQLite store if it is straightforward.

If faster and safer for v1, use a local JSON file under `data/`, but:
- include it in `.gitignore` if it may contain local owner preferences,
- provide a `.example.json` only if needed,
- keep defaults safe.

## Validation

Run:

```bash
./scripts/validate.sh
python3 -m py_compile $(find app -name '*.py' -not -path '*/__pycache__/*')
```

Also manually verify:

```bash
./scripts/run_api.sh
curl http://127.0.0.1:8010/health
curl http://127.0.0.1:8010/status
curl http://127.0.0.1:8010/settings/redacted
curl http://127.0.0.1:8010/filters
curl http://127.0.0.1:8010/routing
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
- admin URL,
- screenshots or brief visual notes,
- what is mock/local-only,
- `git status --short --branch`.
