# Claude Prompt 001 - Watchtower Scaffold

ROLE CHECK: Claude
PROFILE CHECK: P4 Backend/API
MISSION SLICE: Build the first runnable Watchtower scaffold for Mac mini local testing.

## Read First

- `AGENTS.md`
- `README.md`
- `DOC/collaboration/ai_role_protocol.md`
- `DOC/collaboration/context_tool_profiles.md`
- `DOC/state/CURRENT_CONTEXT.md`
- `DOC/mission.md`
- `DOC/architecture.md`
- `DOC/data_sources.md`
- `DOC/telegram_bot_spec.md`
- `DOC/mac_mini_runbook.md`
- `DOC/vultureinv_integration_contract.md`
- `DOC/specs/vultureinv_support_plan.md`
- `DOC/specs/settings_and_web_integration.md`
- `.env.example`

## Do

1. Create a Python FastAPI scaffold.
2. Add `requirements.txt` with:
   - fastapi
   - uvicorn
   - pydantic-settings
   - apscheduler
   - python-telegram-bot
   - pandas
   - numpy
   - httpx
3. Create the module structure from `DOC/architecture.md`.
4. Implement config loading from `.env`.
5. Implement endpoints:
   - `GET /health`
   - `GET /status`
   - `GET /snapshots/regime/latest`
   - `GET /snapshots/flow/latest`
   - `GET /snapshots/catalysts/latest`
   - `POST /jobs/refresh/mock`
6. Implement mock provider and mock ingestion only.
7. Store mock snapshots in SQLite or a simple local JSON store if SQLite slows
   the first pass. Prefer SQLite if straightforward.
8. Implement Telegram bot commands:
   - `/status`
   - `/brief`
   - `/refresh_mock`
   - `/watchlist`
   - `/help`
9. Restrict Telegram access to `TELEGRAM_ALLOWED_CHAT_IDS`.
10. Add `scripts/run_api.sh` and `scripts/run_worker.sh` if useful.
11. Update `DOC/mac_mini_runbook.md` if implementation commands differ.
12. Keep `scripts/validate.sh` passing.

## Do Not

- Do not call real KRX, FRED, OpenDART, SEC, Grok, or OpenClaw yet.
- Do not add automated trading.
- Do not add crypto/futures/options/FX.
- Do not commit secrets or `.env`.
- Do not make Telegram noisy.
- Do not require Docker for the first version.

## Validation

```bash
./scripts/validate.sh
python3 -m py_compile $(find app -name '*.py')
uvicorn app.main:app --host 127.0.0.1 --port 8010
curl http://127.0.0.1:8010/health
curl http://127.0.0.1:8010/status
```

If test tooling is added:

```bash
pytest
```

## Expected Owner-Visible Result

- Mac mini can run Watchtower locally.
- `/health` and `/status` return useful JSON.
- `/jobs/refresh/mock` creates fresh mock snapshots.
- `/brief` in Telegram returns a concise mock battlefield brief.
- No external source credentials are required for the first smoke test.
