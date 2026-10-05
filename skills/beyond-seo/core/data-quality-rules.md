# Data Quality Rules

Rules for judging and labeling data quality.

---

## Labels

`core/evidence-schema.json` is the authoritative label and finding contract. SKILL.md explains the same labels for agents without code execution. Use `Inferred` for reasoned interpretations, `Directional` for estimates and `Not verified` for unavailable evidence. Do not introduce alternative labels.

Every recommendation distinguishes observation, interpretation and unknowns. A verified source confirms where a metric came from; vendor estimates remain estimates, and provenance does not establish causation.

## Never Invent

Do not invent search volume, rankings, traffic, backlinks, DR/DA, GBP calls, conversions, AI Overview visibility, AI Mode visibility, Discover AI visibility, branded/non-branded query splits, or Search Console generative AI report data.

## Tool Data

Apify community actors and scraped authority metrics are directional unless verified through official exports.

## Current SEO Data Rules

Use official Google sources for confirmed ranking and policy updates:

- Google Search Status Dashboard for core, spam, Discover, and ranking incidents.
- Google Search Central blog/docs for policy, Search Console, crawling, structured data, and AI-search guidance.
- Search Console exports for site-specific performance.

Industry articles, social posts, rank volatility tools, and community observations are useful but directional unless confirmed by official sources or the user's own data.

When diagnosing traffic drops, align the affected date range with confirmed updates before attributing causality. If timing only overlaps, use `Inferred` or `Directional` and explain the unknowns.

## Measurement and audit boundaries

Record property, measurement window, retrieval timestamp, dimensions, filters, units, country and device where relevant. Missing values are null/Not verified; zero requires an actual zero observation. Source compatibility matters: GSC does not measure conversions. GA4 key events are not automatically qualified leads. CRM qualification and revenue require CRM evidence.

A successful crawl does not confirm Google indexation or rendering. Short HTML text, canonical absence, sitemap omission or identical text hashes require contextual review rather than automatic fixes or ranking-loss claims.

Read `core/finding-contract.md` for traceability, `core/scoring-methodology.md` before scoring, `integrations/first-party-data-quality.md` before using GSC/GA4 totals, and `audit/traffic-drop-diagnosis.md` for decline diagnosis.

Use `core/current-guidance-register.json` for changing policies and capabilities. Verify applicable primary documentation and actual account fields in the current audit. Record conflicting sources rather than silently selecting one. A screenshot validates only the visible data and scope, not an entire export/account.

Keep private raw data and credentials out of public repositories, reports and reproducibility bundles. Preserve necessary private originals in owner-controlled storage.
