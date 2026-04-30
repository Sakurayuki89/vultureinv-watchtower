# VultureInv Support Plan

## Purpose

Watchtower exists to support the main VultureInv cockpit, not to become a
separate product. Its value is reliable background work: collect, normalize,
store, alert, and expose snapshots.

## Support Modules

### S1 - Regime Feed Support

Supports VultureInv M1.

Inputs:
- FRED macro series,
- US10Y / DXY / VIX provider snapshots,
- KOSPI/KOSDAQ/SPY/QQQ index snapshots.

Outputs:
- latest regime snapshot,
- stale/fresh source labels,
- simple risk environment tags.

### S2 - Flow Radar Support

Supports VultureInv M3.

Inputs:
- KRX investor-type flow,
- price/volume,
- ETF proxy data where available.

Outputs:
- flow candidate snapshot,
- accumulation/distribution counts,
- source timestamps.

### S3 - Catalyst Support

Supports VultureInv M2.

Inputs:
- OpenDART disclosures,
- SEC EDGAR filings,
- scheduled macro/earnings calendar later.

Outputs:
- catalyst/disclosure alerts,
- filing source metadata,
- watched-symbol event list.

### S4 - Risk Support

Supports VultureInv M4.

Inputs:
- latest prices,
- portfolio/watchlist from VultureInv,
- volatility/drawdown snapshots later.

Outputs:
- stale price warnings,
- risk event alerts,
- no automatic trade instructions.

## MVP Phases

### Phase 0 - Harness And Mock Loop

- FastAPI `/health` and `/status`.
- mock ingestion job.
- local snapshot store.
- Telegram `/status`, `/brief`, `/refresh_mock`.

### Phase 1 - Regime Provider

- Add FRED provider.
- Add basic regime snapshot endpoint.
- Telegram daily macro brief.

### Phase 2 - Disclosure Providers

- Add OpenDART provider.
- Add SEC EDGAR provider.
- Watchlist disclosure alerts.

### Phase 3 - KRX Flow Provider

- Add KRX/pykrx provider behind conservative scheduler.
- Daily KR flow brief after market close.

### Phase 4 - VultureInv Integration

- VultureInv backend pulls Watchtower snapshots.
- VultureInv displays freshness and source state.
- Manual refresh endpoints require token.

## Integration Principle

Watchtower produces evidence. VultureInv decides how to present and score it.

Watchtower must not produce final investment decisions, guaranteed returns, or
live trading instructions.
