# Codex Coding Guardrails

## Purpose

Claude remains the default implementation and local verification agent for
Watchtower. Codex may code directly when the owner asks for it or when a small
boundary fix prevents the Watchtower/VultureInv/OpenClaw/Telegram flow from
becoming harder to repair later.

This is an exception path, not a replacement for Claude.

## When Codex May Code

Codex may edit files directly for:

- OpenClaw provider guards,
- Telegram safety and rate-limit guards,
- Watchtower API contract fixes,
- VultureInv integration contract fixes,
- `.env` and secret safety,
- validation script repairs,
- small unblockers after Claude limit or partial edits,
- high-risk corrections where a written prompt would be slower or ambiguous.

Codex should keep changes small, scoped, and validated.

## When Codex Should Not Code

Codex should not be the default owner for:

- broad provider implementations,
- full real-data ingestion,
- speculative refactors,
- large Telegram bot feature sets,
- full-universe AI analysis.

Use Claude for those unless the owner explicitly asks Codex to implement.

## OpenClaw Defaults

OpenClaw/local AI must stay disabled by default:

```text
ENABLE_LIVE_AI=false
OPENCLAW_ENDPOINT=
OPENCLAW_MODEL=
```

First allowed implementation:

- config/status reporting,
- health check,
- deterministic fallback when unavailable,
- provider/model/generated timestamp metadata.

Forbidden first implementation:

- automatic full-universe AI runs,
- OpenClaw calculating scores, risk, stop loss, position size, or conviction,
- Telegram sending AI alerts without deterministic trigger rules,
- VultureInv frontend calling OpenClaw directly,
- committing real prompts containing private portfolio details.

## Non-Negotiable Boundaries

- Watchtower owns Telegram and background source collection.
- VultureInv owns cockpit UI, scoring, risk gates, and owner decision workflow.
- OpenClaw may draft text only from stored source/snapshot context.
- Raw source snapshots must be stored before AI summaries.
- AI output must be stored separately from source snapshots.
- Every AI output must carry provider, model, generated timestamp, source
  snapshot ids, and stub/live flag.

## Required Validation

After Codex code changes in this repo:

```bash
./scripts/validate.sh
python3 -m py_compile $(find app -name '*.py' -not -path '*/__pycache__/*')
```

If a command is not applicable yet, Codex must say so in the final report.
