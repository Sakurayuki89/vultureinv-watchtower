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

## Required Context

Before planning or implementation, read:

- `DOC/collaboration/ai_role_protocol.md`
- `DOC/collaboration/context_tool_profiles.md`
- `DOC/mission.md`
- `DOC/architecture.md`
- `DOC/vultureinv_integration_contract.md`

Before settings, API, or UI work, also read:

- `DOC/specs/settings_and_web_integration.md`
- `DOC/specs/vultureinv_support_plan.md`

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

## Collaboration Roles

- Claude: main implementation and local Mac mini verification.
- Codex/GPT: architecture, planning, review, repair prompts, high-risk corrections.
- Gemini: broad documentation consistency and memory/audit work if used.

Codex may also make small direct code changes when the owner explicitly asks or
when Watchtower/VultureInv/OpenClaw/Telegram boundaries are at risk. Follow
`DOC/codex_coding_guardrails.md`.

External AI reports are review-only unless the owner explicitly says to apply
them.

## Validation

After code changes, run the project validation commands from the active prompt.
At minimum:

```bash
./scripts/validate.sh
python3 -m py_compile $(find app -name '*.py')
```

Add lint/test commands once the scaffold defines them.
