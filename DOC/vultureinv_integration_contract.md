# VultureInv Integration Contract

## Responsibility Split

Watchtower owns:
- background ingestion,
- source freshness,
- local snapshot store,
- Telegram alerts,
- source/archive metadata.

VultureInv owns:
- PC command-center UI,
- owner decision workflow,
- score/risk display,
- research drafting/publishing,
- portfolio/risk cockpit.

## Integration Direction

MVP should prefer pull-based integration:

```text
VultureInv backend -> Watchtower snapshot API
```

Telegram can call Watchtower directly.

## Watchtower API Endpoints

### `GET /health`

Basic liveness.

### `GET /status`

Returns service, scheduler, source, and storage health.

### `GET /snapshots/regime/latest`

Returns latest regime-oriented snapshot.

### `GET /snapshots/flow/latest`

Returns latest Flow Radar candidate snapshot.

### `GET /snapshots/catalysts/latest`

Returns latest disclosure/event snapshot.

### `POST /jobs/refresh/mock`

Manual mock refresh for smoke testing.

### `POST /jobs/refresh/{source}`

Manual source refresh. Must require a local token once implemented.

## Snapshot Metadata

Every snapshot must include:

```text
snapshot_id
snapshot_type
generated_at
source
source_fetched_at
freshness_state: fresh | stale | failed | mock
items[]
warnings[]
```

## VultureInv Consumption Rules

- VultureInv should display freshness state.
- VultureInv should not hide stale source warnings.
- VultureInv should not treat Watchtower alerts as investment advice.
- Watchtower data can support Signal Convergence, but final UI labels and risk
  calculations must stay in the VultureInv deterministic layer.
