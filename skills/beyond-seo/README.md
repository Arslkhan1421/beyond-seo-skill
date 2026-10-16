# Beyond SEO 1.5.1

Portable evidence-led SEO workflows and deterministic analysis with client-ready PDFs. Read SKILL.md first for workflows and a complete package index.

```text
python -m pip install -r requirements.txt
python tools/audit_runner.py --config audit-config.json --output-dir output/site-date
python tools/audit_runner.py --config audit-config.json --crawl-snapshot pages.json --serp-snapshot serp.json --output-dir output/site-offline
python tools/validate_skill.py
python -m unittest discover -s tests -v
```

Copy templates/audit-config-template.json outside the package. Exact contracts and tools: core/v1.5-workflows.md. Offline crawl ingestion disables all network collectors; it never implies fresh observation, complete crawling or Google indexation.

Consolidated guides retain original module prose/headings. core/module-migration.json maps old paths; vendor headers now live in core/import-schemas.json. Schema, query-overlap, backlink and funnel outputs are review candidates, not automated SEO truth or authorization to change a site.

Keep credentials and private client artifacts outside the distributable. Preserve local-only configuration on upgrade and install dependencies in the execution environment. Every report distinguishes observations, inferred impact and unknown outcomes; no ranking, rich-result or ROI guarantees.

## License

MIT. See LICENSE included in this skill. Earlier release archives retain their original notices.
