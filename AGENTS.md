# VultureInv Watchtower Agent Instructions

## Identity

Watchtower is a Mac mini automation sidecar for VultureInv.

It collects data, stores snapshots, sends Telegram alerts, and exposes a small
API for the main VultureInv cockpit. It does not replace the cockpit.

## Relationship To VultureInv

VultureInv:
- PC-first command center,
- owner decision support,
- Flow Radar / Catalyst / Regime / Portfolio UI,
- final analysis and research workflow.

Watchtower:
- background ingestion,
- local automation,
- Telegram alerts and commands,
- snapshot API,
- source archive.

Do not let Watchtower redefine VultureInv product truth. If there is conflict,
follow the main VultureInv repo's `AGENTS.md`, `DOC/owner_mission.md`, and specs.

## Scope

Allowed asset scope:
- Korea stocks,
- US stocks,
- Korea ETFs,
- US ETFs.

Not allowed by default:
- crypto,
- futures,
- options,
- FX trading,
- fully automated live trading,
- guaranteed return language.

## Engineering Rules

- Keep external source calls inside provider adapters.
- Keep route handlers thin.
- Keep scheduling logic separate from provider parsing.
- Store raw source snapshots before deriving signals.
- Every snapshot must carry source, fetched timestamp, and freshness state.
- Telegram alerts must be high-signal and rate-limited.
- Grok/OpenClaw/LLM calls must be owner-triggered or explicitly scheduled by a
  reviewed policy. No full-universe automatic AI calls by default.
- Never commit `.env`, tokens, API keys, Telegram bot tokens, or local data.

## First Implementation Priority

1. FastAPI health/status endpoints.
2. Mock ingestion job that proves the scheduler and snapshot API work.
3. Telegram `/status`, `/brief`, `/refresh_mock`.
4. VultureInv integration contract endpoints.
5. Real providers only after the mock loop is stable.

## Validation

After code changes, run the project validation commands from the active prompt.
At minimum:

```bash
python3 -m py_compile $(find app -name '*.py')
```

Add lint/test commands once the scaffold defines them.
