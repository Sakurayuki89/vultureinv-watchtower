# Current Context

Last updated: 2026-04-30

## State

Watchtower is a new sidecar repository for the VultureInv project.

Current committed state:
- planning scaffold,
- AI role/context harness,
- mission and architecture docs,
- data source policy,
- Telegram bot spec,
- Mac mini runbook,
- VultureInv integration contract,
- first Claude scaffold prompt.

## Current Goal

Build a Mac mini runnable MVP:

```text
mock ingestion
-> local snapshot store
-> FastAPI status/snapshot endpoints
-> Telegram /status, /brief, /refresh_mock
```

## Do Not Do Yet

- Real KRX/FRED/OpenDART/SEC calls.
- Grok/OpenClaw live calls.
- Automated trading.
- Docker-only deployment.
- Complex web UI.

## Next Prompt

Use `prompts/claude_001_scaffold.md`.
