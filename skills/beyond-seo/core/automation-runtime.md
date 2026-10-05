# Beyond SEO Automation Runtime

Use this reference when running a repeatable audit or maintaining historical audit data.

## Standard command

```text
python tools/audit_runner.py --config audit-config.json --output-dir output/site-date
```

Copy `templates/audit-config-template.json`, then set the website, country, services, goals, and query set. Keep crawl and SERP limits conservative until the first run succeeds.

## Historical comparison

```text
python tools/audit_runner.py --config audit-config.json --output-dir output/current --previous output/previous/audit-data.json
```

The runner creates:

- `audit-data.json`
- `evidence-ledger.json` and `.csv`
- `competitor-classification.json`
- `audit-comparison.json` when a previous audit is supplied
- `report-input.json`
- `beyond-seo-audit.pdf`
- `beyond-seo-audit.qa.json`

Historical findings use `New`, `Improved`, `Worsened`, `Changed`, `Unchanged`, `Resolved`, and `Reopened`. A lower known severity is improved; a higher known severity is worsened; unrecognized severity changes are changed rather than guessed.

## Quality gates

Before delivery:

1. Confirm the ledger contains no token or secret.
2. Confirm proprietary metrics are absent unless backed by first-party or paid-tool evidence.
3. Confirm `beyond-seo-audit.qa.json` reports a passing structural check. The runner creates it automatically and stops when QA fails.
4. Review the rendered PDF visually when rendering tools exist; structural QA does not replace visual review.
5. Review excluded competitors and restore one only when it is a realistic business benchmark.
6. Keep the raw SERP sample date, country, language, device, and depth in the report.

## Crawl boundary

The crawler respects `robots.txt` by default, rejects credentialed and non-HTTP URLs, pins each request to the validated DNS address, limits redirects and response size, and blocks private/non-public addresses. Same-site crawling is the default. Add external sitemap hosts explicitly with `allowed_sitemap_hosts`; set `allow_private_network` to `true` only for an intentional, trusted internal audit target.

## Performance fallback

`tools/lighthouse_runner.py` tries PageSpeed Insights first. A locally installed Lighthouse command is available only when `performance.allow_local_lighthouse` is explicitly `true` for a trusted target; the local browser is disabled by default because it can reach network locations from the runner host. If no allowed method succeeds, the tool writes `Not verified` with plain-language context. It must never convert an unavailable performance test into a numeric score.

## Scheduling boundary

The runtime creates repeatable audit artifacts, but it does not schedule itself. Use the host system's approved scheduler and persist each dated output directory. Never overwrite the previous audit used for comparison.
