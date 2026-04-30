# Watchtower Architecture

## System Shape

```text
watchtower-api
  FastAPI service for status, snapshots, and VultureInv integration

watchtower-worker
  APScheduler-backed background jobs

watchtower-telegram
  Telegram bot commands and outbound alerts

providers/
  source-specific adapters: mock, KRX, FRED, OpenDART, SEC

storage/
  raw snapshots, derived snapshots, job runs, alert events
```

## Data Flow

```text
provider adapter
-> raw snapshot table/file
-> normalizer
-> derived snapshot
-> alert evaluator
-> Telegram and API
```

## Process Boundaries

MVP can run API, scheduler, and Telegram bot in one Python process if that is
simpler on the Mac mini. Keep the code boundaries separate so they can later be
split into separate processes.

## Recommended Modules

```text
app/
  main.py
  core/config.py
  api/routes/health.py
  api/routes/status.py
  api/routes/snapshots.py
  api/routes/jobs.py
  providers/base.py
  providers/mock_provider.py
  providers/krx_provider.py
  providers/fred_provider.py
  providers/opendart_provider.py
  providers/sec_provider.py
  services/ingestion_service.py
  services/snapshot_service.py
  services/alert_service.py
  services/telegram_service.py
  scheduler/jobs.py
  storage/sqlite_store.py
```

## Persistence

Start with SQLite because the Mac mini setup should be easy.

Store:

- job runs,
- raw snapshots,
- derived snapshots,
- alert events,
- watchlist symbols,
- source freshness metadata.

Move to PostgreSQL only after the API contract and scheduled loop are stable.

## AI Policy

AI can summarize stored source documents or answer owner-triggered questions.
AI must not:

- fetch every symbol automatically,
- calculate score/risk/position size,
- overwrite deterministic snapshots,
- hide source timestamps.
