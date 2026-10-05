# Traffic-Drop Diagnosis

Identify the metric/property: clicks, impressions, sessions, key events, qualified leads or revenue. Record onset, magnitude, windows, affected pages, country, device, search type and provenance. An analytics-session decline can be a measurement change even when GSC clicks are stable.

1. Validate tracking, exports, filters, consent, attribution, timezone and events. Check incomplete dates and equal-length windows.
2. Check deployments, outages, migrations, redirects, robots/noindex, canonicals, sitemaps, security/manual-action notices and URL Inspection. Compare affected URLs/templates rather than homepage status alone.
3. Segment brand/non-brand with query coverage limits, page type, country, device and supported appearance fields. Separate demand, click-through and position changes.
4. Review seasonality, prior-year demand, business changes and dated SERP samples. Trends and competitor changes support hypotheses, not causal proof.
5. Check the official [Search Status Dashboard](https://status.search.google.com/) and [traffic-drop guidance](https://developers.google.com/search/docs/monitor-debug/debugging-search-traffic-drops). Update timing overlap is not proof of cause.

Output: hypothesis, supporting evidence IDs, contradicting evidence, unknowns, next discriminating check, confidence, owner and action. Prioritize verified access/indexing or measurement defects before speculative rewrites. Do not recommend mass deletion, disavowal or sitewide redirects based on correlation alone.

For multilingual/ecommerce/migrations, inspect hreflang/canonical interactions, product/category/faceted intent, URL mapping and redirect chains on representative templates. For server logs, verify bot identity and redact identifiers; a Googlebot user-agent alone is insufficient.
