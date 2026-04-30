# Watchtower Admin UI And Intelligence Pipeline Plan

## Purpose

The Mac mini dashboard is an operations monitor. It shows whether OpenClaw,
Watchtower, snapshots, and the news briefing job are alive.

The next UI is different: it controls what economic/news intelligence is
collected, filtered, reviewed, and passed to VultureInv.

## Product Boundary

Watchtower remains the automation sidecar.

It may:
- collect source data,
- store raw and derived snapshots,
- label freshness and warnings,
- schedule refresh jobs,
- send Telegram alerts,
- expose reviewed snapshots to VultureInv,
- ask OpenClaw to summarize already stored source bundles when explicitly
  enabled by owner policy.

It must not:
- become the VultureInv investment cockpit,
- make trade/risk/position sizing decisions,
- expose secrets,
- call OpenClaw for full-universe automatic analysis by default,
- expand beyond Korea stocks, US stocks, Korea ETFs, and US ETFs.

## UI Surfaces

### 1. Mac mini Dashboard

Status: implemented in `/Users/macmini/code/macmini-dashboard`.

Role:
- local operations monitor,
- OpenClaw/Watchtower/service state,
- latest news briefing log,
- snapshot freshness,
- quick links.

Not role:
- filter editing,
- routing policy,
- research approval workflow.

### 2. Watchtower Admin UI

Recommended path:

```text
http://127.0.0.1:8010/admin
```

Role:
- configure local automation safely,
- inspect source and job health,
- define filter/routing rules,
- run manual refreshes,
- review what will be sent downstream.

First tabs:
- Status
- Sources
- Filters
- Routing
- Review Queue
- Telegram
- AI Providers

### 3. VultureInv Intelligence Inbox

Recommended owner: main VultureInv project.

Role:
- receive Watchtower snapshots,
- show macro/news/disclosure context inside the PC cockpit,
- let the owner promote items into Signal Convergence or Research Desk,
- keep deterministic scoring/risk in VultureInv, not Watchtower/OpenClaw.

## Data Flow

```text
source adapters
-> raw source snapshots
-> deterministic filters
-> derived intelligence bundle
-> optional OpenClaw summary from stored bundle
-> Watchtower review queue
-> Telegram brief and/or VultureInv snapshot API
-> VultureInv Intelligence Inbox
```

## Filter Model

Initial filter fields:

```text
enabled
market_scope: KR | US | KR_ETF | US_ETF
symbols[]
sectors[]
keywords_include[]
keywords_exclude[]
source_types: news | disclosure | macro | flow
min_importance: low | medium | high
freshness_window_minutes
telegram_enabled
vultureinv_enabled
requires_owner_review
```

Rules:
- filters are deterministic,
- AI may summarize matched bundles only,
- every output keeps source timestamps and warnings.

## Routing Model

Initial routing destinations:

```text
none
telegram_brief
vultureinv_snapshot
review_queue
```

Routing decisions must be explainable:
- which filter matched,
- which source produced the item,
- why it was sent or held.

## Project Roles

### Claude

Use Claude for:
- implementing Watchtower Admin UI,
- adding settings/read-only API endpoints,
- local FastAPI/Next verification,
- UI screenshots,
- applying concrete Codex repair prompts.

### Codex

Use Codex for:
- architecture decisions,
- provider and AI boundary review,
- routing/filter schema review,
- high-risk fixes,
- checking Claude output against specs.

### OpenClaw

Use OpenClaw for:
- local assistant operation,
- owner-triggered summaries from stored source bundles,
- Telegram assistance.

Do not use OpenClaw as the source of product truth or numeric risk/scoring.

## MacBook / Mac mini Operating Model

Mac mini:
- runs OpenClaw gateway,
- runs Watchtower API and worker,
- runs macmini-dashboard,
- owns local secrets and source automation.

MacBook:
- can run Codex/Claude for code work,
- can access Mac mini over Tailscale,
- should not duplicate OpenClaw gateway unless explicitly testing a second
  node.

Recommended access:
- use Tailscale SSH for code/admin work,
- expose only the macmini-dashboard if needed,
- keep Watchtower admin and OpenClaw Control UI local or behind a deliberate
  tunnel.

## Next Implementation Step

Build Watchtower Admin UI v1 with:
- `GET /admin`
- `GET /settings/redacted`
- `GET /filters`
- `POST /filters`
- `GET /routing`
- `POST /routing`
- `GET /review-queue`

For v1, filters and routing can persist in SQLite or a local JSON config, but
must not expose tokens or `.env` contents.
