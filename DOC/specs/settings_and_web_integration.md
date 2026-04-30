# Settings And Web Integration Spec

## Purpose

Watchtower needs a small settings surface, but it should not become a full
dashboard. The main visual cockpit remains VultureInv.

The Watchtower settings UI exists only to configure local automation and inspect
health.

## Recommended UX

Use a simple local web admin at:

```text
http://127.0.0.1:8010/admin
```

This can be plain FastAPI templates or a small static page. Do not build a
separate complex frontend until the worker loop is stable.

## Admin Screens

### 1. Status

Shows:
- API status,
- scheduler status,
- Telegram status,
- VultureInv API reachability,
- latest job run,
- stale sources.

### 2. Sources

Shows:
- provider enabled/disabled,
- last fetched time,
- freshness state,
- failure message,
- manual refresh button.

Do not display API keys.

### 3. Watchlist

Shows:
- symbols being monitored,
- market,
- alert enabled state,
- source coverage.

Initial watchlist can be edited in a local config file. UI editing can come
later.

### 4. Telegram

Shows:
- bot connected or not,
- allowed chat IDs count,
- last alert time,
- command health.

Do not display bot token.

### 5. Integration

Shows:
- VultureInv API base URL,
- last successful call,
- snapshot endpoints,
- integration token configured yes/no.

### 6. AI Providers

Shows:
- live AI globally enabled yes/no,
- local/OpenClaw configured yes/no,
- Gemini configured yes/no,
- Grok configured yes/no,
- selected model names,
- last owner-triggered AI call timestamp.

Do not display API keys.

## API Contract For Admin

### `GET /admin`

Local status UI.

### `GET /status`

Machine-readable status.

### `GET /settings/redacted`

Returns safe settings only:

```text
env
database_url_redacted
telegram_configured
allowed_chat_count
vultureinv_api_base_url
fred_configured
opendart_configured
sec_user_agent_configured
live_ai_enabled
openclaw_configured
openclaw_model
gemini_configured
gemini_model
gemini_live_enabled
grok_configured
grok_model
grok_live_enabled
```

### `POST /jobs/refresh/mock`

No external calls.

### `POST /jobs/refresh/{source}`

Requires local token. Source must be one of:

```text
fred
opendart
sec
krx
```

## VultureInv Web Integration

Preferred first integration:

```text
VultureInv backend -> Watchtower API
```

Avoid:

```text
VultureInv frontend -> external data providers
VultureInv frontend -> Watchtower direct over public network
```

The main VultureInv backend should mediate if the cockpit needs Watchtower data.

## Network Assumption

For local owner setup:

```text
Mac mini Watchtower: http://127.0.0.1:8010 on Mac mini
VultureInv dev machine: configured URL if same LAN access is needed
```

If exposed beyond localhost:
- require token auth,
- bind to LAN IP deliberately,
- do not expose admin UI publicly,
- do not expose secrets or source payloads unnecessarily.

## Telegram Integration

Telegram is both:

- outbound alert channel,
- simple command interface.

It should not be the primary configuration UI. Use Telegram for status and
manual refresh, not for editing secrets.

## AI Configuration

Environment variables:

```text
ENABLE_LIVE_AI=false
OPENCLAW_ENDPOINT=
OPENCLAW_MODEL=
GEMINI_API_KEY=
GEMINI_MODEL=gemini-2.5-flash-lite
ENABLE_GEMINI_LIVE=false
GROK_API_KEY=
GROK_MODEL=grok-4.20
ENABLE_GROK_LIVE=false
```

Rules:

- all live providers are OFF by default,
- AI calls are owner-triggered only,
- no full-universe AI batch in the MVP,
- no secrets are shown in admin or Telegram,
- AI output must include provider, model, generated timestamp, and source
  snapshot timestamp.
