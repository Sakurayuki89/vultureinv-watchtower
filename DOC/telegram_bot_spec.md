# Telegram Bot Spec

## Purpose

Telegram is the owner's alert and command interface for Watchtower.

It should not become a noisy market chat stream. It should send concise,
actionable messages that tell the owner whether opening the VultureInv cockpit
is worth it.

## Commands

### `/status`

Returns:
- API status,
- worker status,
- latest successful job,
- stale sources,
- DB path,
- VultureInv API reachability.

### `/brief`

Returns the latest daily battlefield brief:
- regime state,
- KR flow highlights,
- US macro/index highlights,
- catalyst/disclosure alerts,
- blocked/stale data warnings.

### `/refresh_mock`

Runs a mock ingestion job immediately.

Purpose:
- end-to-end test without external source credentials.

### `/watchlist`

Shows current watched symbols.

### `/help`

Shows available commands and safety notes.

## Alert Types

Send alerts for:

- job failure,
- stale critical source,
- watched symbol disclosure,
- flow accumulation threshold hit,
- risk regime change,
- manual refresh completed.

Do not alert for every price move.

## Safety

- Only allow configured Telegram chat IDs.
- Never print secrets.
- Rate-limit repeated failures.
- Every alert should include snapshot timestamp and source/freshness label.
