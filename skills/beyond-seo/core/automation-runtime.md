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

## Quality gates

Before delivery:

1. Confirm the ledger contains no token or secret.
2. Confirm proprietary metrics are absent unless backed by first-party or paid-tool evidence.
3. Run `python tools/pdf_qa.py --input report.pdf --output report.qa.json`.
4. Review the rendered PDF visually when rendering tools exist.
5. Review excluded competitors and restore one only when it is a realistic business benchmark.
6. Keep the raw SERP sample date, country, language, device, and depth in the report.

## Performance fallback

`tools/lighthouse_runner.py` tries PageSpeed Insights first and then a locally installed Lighthouse command. If neither succeeds, it writes `Not verified` with plain-language context. It must never convert an unavailable performance test into a numeric score.

## Scheduling boundary

The runtime creates repeatable audit artifacts, but it does not schedule itself. Use the host system's approved scheduler and persist each dated output directory. Never overwrite the previous audit used for comparison.
