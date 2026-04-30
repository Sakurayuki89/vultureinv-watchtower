# Watchtower Mission

## One-Line Mission

Watchtower keeps VultureInv's market, flow, macro, and disclosure inputs ready
before the owner opens the cockpit.

## Why It Exists

The VultureInv cockpit should not wait on slow external APIs or scrape websites
when the owner is trying to decide. Watchtower runs in the background on the Mac
mini, gathers delayed/free data, labels freshness, and alerts only when there is
something worth attention.

## Owner Value

Watchtower should help the owner answer:

- Did market regime change?
- Which Korea stocks/ETFs had meaningful foreign/institution flow?
- Did a watched company file a new disclosure?
- Did a US company publish a material filing?
- Which candidates deserve opening the PC cockpit?
- Are data jobs healthy or stale?

## Non-Goals

- No automated trading.
- No broad chat feed.
- No mobile-first product.
- No crypto/futures/options/FX expansion.
- No AI-generated numeric risk or position sizing.
- No claims of guaranteed return.

## First Useful Loop

```text
scheduled data refresh
-> snapshot update
-> signal threshold check
-> Telegram brief
-> owner opens VultureInv cockpit for deeper review
```
