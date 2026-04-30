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

Fill `.env` locally:

- `TELEGRAM_BOT_TOKEN`
- `TELEGRAM_ALLOWED_CHAT_IDS`
- optional source keys such as `FRED_API_KEY` and `OPENDART_API_KEY`

## First Smoke Test

```bash
python -m app.main
```

Then test:

```bash
curl http://127.0.0.1:8010/health
curl http://127.0.0.1:8010/status
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
