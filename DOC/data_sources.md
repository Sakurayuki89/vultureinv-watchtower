# Data Sources

## Source Priority

1. Official/public APIs.
2. Stable open-source wrappers around official/public sources.
3. Scraping only behind isolated provider adapters and with conservative rate
   limits.

## Initial Sources

### KRX / Korea Market Flow

Purpose:
- Korea stock and ETF price/volume,
- investor-type flow where available,
- market/index context.

Candidate:
- `pykrx`

Notes:
- It is useful for Korean market data but includes scraping behavior.
- Keep calls scheduled and rate-limited.
- Store source and fetched timestamp.
- Do not treat it as guaranteed official truth without validation.

### OpenDART

Purpose:
- Korea filings,
- company information,
- major disclosures,
- financial statement metadata.

Approach:
- Prefer official OpenDART API.
- Keep API key in local `.env`.
- Store filing number, company, title, source URL, fetched timestamp.

### SEC EDGAR

Purpose:
- US 8-K, 10-Q, 10-K, 13F/13D/13G-style research inputs.

Approach:
- Use SEC APIs or a reviewed downloader wrapper.
- Always provide a compliant User-Agent with company name and email.
- Store accession number, form type, filing date, URL, fetched timestamp.

### FRED

Purpose:
- macro regime inputs such as rates, liquidity, inflation, unemployment,
  credit stress, and dollar/risk context.

Approach:
- Use official FRED API or `fredapi`.
- Store series id, observation date, value, realtime metadata where available.

## Not First

- Dark pool APIs.
- Paid data vendors.
- Full-universe AI summarization.
- Broker APIs.
- Trade execution APIs.
