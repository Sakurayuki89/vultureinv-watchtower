# Watchtower Next Steps

## Current State

Watchtower can now run local web/API operations:

- status and snapshot APIs,
- Admin UI,
- filters,
- routing rules,
- review queue,
- mock intelligence run,
- queue deduplication.

Telegram operation is not complete yet. It should be connected after the review
queue workflow is safe.

## Recommended Order

### 1. Review Queue Operations

Status: in progress.

Goal:
- approve/reject/pending status changes,
- safe Admin UI rendering,
- no HTML injection from stored or external text.

Scope:
- `POST /review-queue/{item_id}/status`,
- Admin UI action buttons,
- HTML escaping for all DB/source text.

### 2. Telegram Basic Commands

Goal:
- let the owner inspect Watchtower from Telegram without opening the UI.

Commands:
- `/status` - API, scheduler, storage, snapshot freshness,
- `/brief` - deterministic macro/flow/catalyst summary,
- `/queue` - pending review queue summary,
- `/refresh_mock` - run mock refresh and mock intelligence.

Rules:
- allow only configured chat IDs,
- keep messages concise,
- no secrets,
- no AI output by default.

### 3. Telegram Queue Commands

Goal:
- let the owner approve or reject pending queue items from Telegram.

Commands:
- `/approve <id>`,
- `/reject <id>`,
- `/pending <id>`.

Rules:
- confirm item status after each command,
- reject unknown item IDs,
- rate-limit noisy output,
- do not send market advice language.

### 4. Real Provider Connection

Goal:
- replace mock snapshots gradually with official/public sources.

Suggested order:
- FRED for macro regime,
- SEC EDGAR for US filings,
- OpenDART for Korea disclosures,
- KRX for Korea market/flow data.

Rules:
- source adapters first,
- raw snapshot before derived snapshot,
- source timestamp and freshness required,
- no full-universe AI calls.

### 5. VultureInv Main Inbox

Goal:
- let VultureInv consume reviewed Watchtower intelligence.

Integration direction:

```text
Watchtower reviewed snapshot
-> VultureInv backend
-> VultureInv PC cockpit Intelligence Inbox
-> Signal Convergence / Research Desk promotion
```

Rules:
- VultureInv owns final score/risk/portfolio decisions,
- Watchtower supplies source/freshness/context,
- stale/mock warnings must remain visible.

### 6. OpenClaw Summary Layer

Goal:
- use OpenClaw only after deterministic pipeline and review queue are stable.

Allowed:
- owner-triggered summaries from stored source bundles,
- optional wording draft for Telegram brief,
- local/private explanation support.

Not allowed:
- AI numeric score,
- AI risk/position sizing,
- automatic full-universe analysis,
- hiding source timestamps or freshness warnings.

## Operating Boundary

Mac mini:
- runs OpenClaw,
- runs Watchtower API/worker,
- runs macmini-dashboard,
- owns local secrets and automation.

Claude:
- main implementation and local verification.

Codex:
- planning, review, high-risk fixes, and focused support coding.

Gemini:
- broad audit and documentation consolidation when needed.
