# VultureInv Watchtower

VultureInv Watchtower is the Mac mini sidecar service for VultureInv.

It is not the main investment cockpit. Its job is to keep the battlefield data
warm, organized, and actionable:

- collect delayed/free market and disclosure data in the background,
- store raw source snapshots and derived summaries,
- send high-signal Telegram alerts,
- expose a small read-only API that VultureInv can consume,
- keep AI analysis opt-in and traceable.

## Product Boundary

Watchtower supports Korea stocks, US stocks, Korea ETFs, and US ETFs only.

It must not expand into crypto, futures, options, FX, automated live trading, or
unreviewed paid data integrations unless the owner explicitly changes scope.

## First MVP

The first useful version should run on the owner's Mac mini and provide:

1. `watchtower-api`
   - FastAPI service with `/health`, `/status`, and snapshot endpoints.
2. `watchtower-worker`
   - scheduled mock ingestion first,
   - provider adapter boundaries for KRX, FRED, OpenDART, and SEC EDGAR.
3. `watchtower-telegram`
   - Telegram commands for `/status`, `/brief`, `/refresh_mock`, and `/watchlist`.

## Harness

Watchtower uses a lightweight version of the VultureInv AI collaboration
harness.

Read before implementation:

- `AGENTS.md`
- `DOC/collaboration/ai_role_protocol.md`
- `DOC/collaboration/context_tool_profiles.md`
- `DOC/state/CURRENT_CONTEXT.md`

Concrete support and integration specs:

- `DOC/specs/vultureinv_support_plan.md`
- `DOC/specs/settings_and_web_integration.md`
- `DOC/vultureinv_integration_contract.md`

## Default Data Flow

```text
external sources
-> provider adapters
-> raw snapshots
-> derived snapshots
-> watchtower API
-> VultureInv dashboard and Telegram alerts
```

Frontend screens should not call external financial APIs directly. They should
read the latest stored snapshot through VultureInv or Watchtower API contracts.

## Recommended Stack

- Python 3.11+
- FastAPI
- APScheduler
- python-telegram-bot
- pandas/numpy
- SQLite for the first local MVP
- PostgreSQL later when the integration stabilizes

## Local Development Shape

The repo starts as a documented scaffold. Claude should implement from
`prompts/claude_001_scaffold.md`.

Do not put real secrets in this repo. Copy `.env.example` to `.env` on the Mac
mini and fill local values there.

Run the repository guard with:

```bash
./scripts/validate.sh
```
