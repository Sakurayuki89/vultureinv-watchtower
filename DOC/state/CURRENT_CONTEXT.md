# Current Context

Last updated: 2026-05-01

## State

Phase 0 scaffold complete and smoke-tested on Mac mini.

Codex prepared implementation handoffs:
- `DOC/watchtower_admin_ui_plan.md`
- `prompts/claude_002_watchtower_admin_ui.md`
- `prompts/claude_003_mock_intelligence_queue.md`

Implemented:
- `app/` FastAPI scaffold with lifespan startup/shutdown.
- `app/core/config.py` — pydantic-settings from `.env`.
- `app/storage/sqlite_store.py` — SQLite WAL, snapshots/job_runs/watchlist tables.
- `app/providers/mock_provider.py` — regime, flow, catalysts mock data.
- `app/providers/{krx,fred,opendart,sec}_provider.py` — disabled stubs.
- `app/ai/{local,gemini,grok}_provider.py` — disabled stubs.
- `app/services/{snapshot,ingestion,alert,telegram}_service.py`.
- `app/scheduler/jobs.py` — AsyncIOScheduler mock job every 30 min.
- `app/api/routes/{health,status,snapshots,jobs}.py`.
- `scripts/run_api.sh`, `scripts/run_worker.sh`.
- `requirements.txt`.

All endpoints verified:
- `GET /health` ✅
- `GET /status` ✅
- `POST /jobs/refresh/mock` ✅
- `GET /snapshots/regime/latest` ✅
- `GET /snapshots/flow/latest` ✅
- `GET /snapshots/catalysts/latest` ✅

`./scripts/validate.sh` passes.

## Current Goal

Build the mock intelligence pipeline and Review Queue generation before adding
real providers.

Reason:
- Watchtower Admin UI v1 is now implemented.
- The next risk to remove is whether filters and routing rules actually create
  review queue items from stored snapshots.
- `macmini-dashboard` remains only the operations monitor; it is not the filter
  or transmission policy UI.

## Do Not Do Yet

- Real KRX/FRED/OpenDART/SEC calls.
- Grok/OpenClaw live calls.
- Gemini live calls.
- Automated trading.
- Docker-only deployment.
- Expanding `macmini-dashboard` into the admin/editor surface.
- Letting OpenClaw generate numeric score/risk/position-sizing fields.

## Next Prompt

Use:

```text
prompts/claude_003_mock_intelligence_queue.md
```

Claude should implement that prompt when available, then report:
- changed files,
- validation output,
- `POST /intelligence/run/mock` response,
- review queue count before/after,
- what remains mock/local-only,
- `git status --short --branch`.
