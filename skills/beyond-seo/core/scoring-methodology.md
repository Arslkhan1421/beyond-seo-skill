# Scoring and Coverage

Do not use issue-count deductions or present a partial crawler as an overall SEO score. Scores are transparent, versioned diagnostic rubrics, not Google measurements or growth predictions. Explain scope and evidence before numbers.

## Runtime rubric 1.4.0

The runner reports an **Observed sample checks** score and leaves overall SEO score unavailable.

| Check | Diagnostic weight | Eligible observations |
|---|---:|---|
| HTTP availability | 4, High | Known terminal HTTP responses |
| HTML title presence | 2, Medium | Successful HTML pages |
| HTML H1 presence | 1, Low | Successful HTML pages |
| No unintended noindex on priority URLs | 5, High | Owner-designated intended search URLs with successful HTML responses |

Owner-designated `priority_urls` carry 3x business importance. Score = 100 x passed weighted observations / all tested weighted observations. Transport failures and unavailable content checks are excluded from this denominator and reduce coverage. A known HTTP error fails availability; it does not establish a ranking penalty. Short text, canonicals, duplicates and sitemaps are review signals, not numeric penalties.

Report earned/possible weights, per-check tested/passed/failed counts, tested/eligible checks and coverage. A 100 on one fetched page does not describe site SEO health. If nothing can be tested, score is null/Not verified. Different rubrics or populations are not directly comparable.

All numeric examples in older specialist/report modules are illustrative. This methodology takes precedence over legacy scoring suggestions and example overall-health numbers.

## Crawl coverage

`crawl-coverage.json` records discovered/attempted/successful URLs, failed/blocked/excluded/unattempted URLs, rendered count, limits and stopping reason. Sitemap traversal failures make coverage partial. Discovered URLs are a bounded inventory, not the total site size. Template mappings are owner supplied; report observed counts per mapped template and unclassified pages.

For specialist scores, define checks, weights, evidence requirements and missing-data handling before calculation. Do not assign arbitrary subjective E-E-A-T, backlink or AI visibility scores.
