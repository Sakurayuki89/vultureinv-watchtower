# Current Context

Last updated: 2026-05-01

## State

Phase 0 scaffold complete and smoke-tested on Mac mini.

Codex prepared the next implementation handoff for Watchtower Admin UI v1:
- `DOC/watchtower_admin_ui_plan.md`
- `prompts/claude_002_watchtower_admin_ui.md`

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

Build Watchtower Admin UI v1 before adding real providers.

Reason:
- the owner wants the Mac mini sidecar to control news/economic intelligence
  filters, routing, review queue, and downstream delivery policy before
  expanding provider integrations.
- `macmini-dashboard` is only the operations monitor; it is not the filter or
  transmission policy UI.

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
prompts/claude_002_watchtower_admin_ui.md
```

Claude should implement that prompt when available, then report:
- changed files,
- validation output,
- admin URL,
- what remains mock/local-only,
- `git status --short --branch`.
