# Mac Mini Runbook

## Goal

Run Watchtower continuously on the owner's Mac mini with minimal moving parts.

## First Setup

```bash
git clone https://github.com/Sakurayuki89/vultureinv-watchtower.git
cd vultureinv-watchtower
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Fill `.env` and then validate:

```bash
./scripts/validate.sh
```

Fill `.env` locally:

- `TELEGRAM_BOT_TOKEN`
- `TELEGRAM_ALLOWED_CHAT_IDS`
- optional source keys such as `FRED_API_KEY` and `OPENDART_API_KEY`
- optional AI keys/endpoints, kept disabled until the mock loop works

Initial recommended AI settings:

```text
ENABLE_LIVE_AI=false
OPENCLAW_ENDPOINT=
OPENCLAW_MODEL=
GEMINI_API_KEY=
GEMINI_MODEL=gemini-2.5-flash-lite
ENABLE_GEMINI_LIVE=false
GROK_API_KEY=
GROK_MODEL=grok-4.20
ENABLE_GROK_LIVE=false
```

Do not enable Gemini, Grok, or local AI before `/status`, `/refresh_mock`, and
`/brief` work with mock data.

## First Smoke Test

```bash
# Option A — script (recommended)
./scripts/run_api.sh

# Option B — direct uvicorn
uvicorn app.main:app --host 127.0.0.1 --port 8010

# Option C — module mode
python -m app.main
```

Then test:

```bash
curl http://127.0.0.1:8010/health
curl http://127.0.0.1:8010/status

# Generate mock snapshots
curl -X POST http://127.0.0.1:8010/jobs/refresh/mock

# Read snapshots
curl http://127.0.0.1:8010/snapshots/regime/latest
curl http://127.0.0.1:8010/snapshots/flow/latest
curl http://127.0.0.1:8010/snapshots/catalysts/latest
```

Telegram:

```text
/status
/refresh_mock
/brief
```

## Launch Agent Direction

After the scaffold works manually, add a macOS LaunchAgent that starts the
service on login.

Do not create the LaunchAgent until manual smoke tests pass.

## Logs

Use local `logs/` for MVP. Do not commit log files.

Important logs:

- API startup,
- job runs,
- provider failures,
- Telegram send failures,
- VultureInv integration failures.
