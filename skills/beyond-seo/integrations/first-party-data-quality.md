# First-Party Data Quality

Normalize columns explicitly and run:

```text
python tools/first_party_quality.py --input normalized.csv --metadata export-metadata.json --output quality.json
```

Use `templates/first-party-metadata-template.json`. Audit config accepts `first_party_imports` entries with `input_path` and `metadata_path`. Imports validate and report aggregates; they do not automatically implement keyword strategy or authenticate owner declarations.

The runner validates property/site compatibility. GA4 metadata must include the owner's explicit `website_url` mapping because a numeric property ID does not identify a hostname. GSC properties must cover the target; domain properties covering multiple subdomains require explicit website mapping and appropriate filters for a subdomain audit. Standalone validation accepts `--website` for the same gate.

## GSC

Required metrics: `clicks`, `impressions`, `ctr` (0-1 ratio), `position`; dimensions must match metadata. Preserve property, search type, dates, timezone, device/country filters and export method. Duplicate keys and incompatible units are rejected. Zero impressions have no interpretable CTR/position; do not turn them into rank.

Query rows may omit anonymized queries and be truncated. Do not force their sums to match property totals. Calculate aggregate CTR from total clicks/impressions rather than averaging row CTR. Average position is not a fixed live rank. Reconcile Google-selected canonical URLs before joining performance and crawl datasets. Brand shares describe only the disclosed observed population.

Check the actual Search Console interface/API/export and current official docs before using AI-specific reports. Standard Web data alone cannot isolate an AI feature. Use feature fields only when explicitly present and documented. Manual AI samples require date, engine/model, prompt/query, location, sample size and repeatability limits.

## GA4 and CRM

Required GA4 metrics: `sessions`, `key_events`; include `key_event_definition`. A key event may occur multiple times per session. Identify channel filters, attribution model, consent mode, thresholding, sampling, event changes and timezone. A click is not automatically a qualified lead or revenue.

Reconcile forms, bookings, calls, spam, duplicates and qualification with CRM records where available. Explain differences between GSC clicks, analytics sessions and CRM leads.

## Comparisons

Match property, source, dimensions, filters, timezone, search type, event definition, attribution and equal-length non-overlapping windows. Note weekday composition, seasonality, tracking changes and low counts. `comparison_compatibility` identifies structural mismatches; compatible windows do not establish causation.

Sources: [GSC limits](https://developers.google.com/search/blog/2022/10/performance-data-deep-dive), [GSC API](https://developers.google.com/webmaster-tools/v1/how-tos/all-your-data), [Google AI features](https://developers.google.com/search/docs/appearance/ai-features). Refresh at use time.
