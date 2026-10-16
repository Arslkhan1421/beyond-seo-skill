---
name: beyond-seo
description: Run evidence-led SEO audits, AEO/GEO and local strategy, technical crawls, live SERP and realistic competitor research, Microsoft Clarity behavior analysis, keyword/rank baselines, content optimization, developer briefs, professional PDF reports, historical comparisons, CSV imports, and optional LinkedIn/Instagram planning. Use for website SEO audits, ranking diagnosis, UX/friction evidence, competitor gaps, content plans, recurring reports, and client-ready deliverables.
metadata:
  short-description: Evidence-led SEO, AEO/GEO, competitor, content, reporting, and social workflows
  version: 1.5.1
  compatibility: Codex, Claude Projects, OpenClaw, Cursor, MCP-enabled agents, custom file-based agents
---

# Beyond SEO

Beyond SEO is an evidence-led SEO operating system. Connect every recommendation to qualified visibility, authority, conversion, local discovery, or AI-search eligibility. Never invent proprietary or first-party metrics.

## Non-negotiable rules

1. Inspect available evidence before recommending work.
2. Use the strongest legitimate source available; never bypass paywalls or scrape authenticated paid dashboards.
3. Do not invent keyword volume, difficulty, DR, DA, Authority Score, traffic, backlinks, rankings, conversions, revenue, or AI visibility.
4. Keep `Not verified` categories out of numeric overall scores. Show them separately.
5. Record the date, country, language, device, sample depth, source, and evidence label for every live SERP observation.
6. Treat Apify community actors as Directional unless independently verified.
7. Exclude directories, social platforms, marketplaces, and giant ecosystems from the comparable business competitor set unless the user explicitly requests them.
8. Never store or repeat API tokens in skill files, logs, reports, templates, or final responses.
9. Run structural PDF QA before delivery and visually inspect rendered pages when rendering tools are available.
10. Explain unavailable tools plainly; do not expose raw rate-limit codes as client-facing findings.
11. Distinguish confirmed observations, inferred impact and unknown outcomes. Source verification does not make vendor estimates exact or establish causation.
12. Report crawl/check coverage and limits before scores. Crawling does not confirm Google rendering or indexation.

## Evidence labels

Use only these labels:

- `Confirmed`: directly observed crawl, HTML, HTTP, sitemap, robots, rendered page, or deterministic calculation.
- `First-party verified`: authenticated/exported GSC, GA4, Microsoft Clarity, GBP, CRM, Bing, or equivalent owner data.
- `Paid-tool verified`: legitimate Semrush, Ahrefs, Moz, DataForSEO, Sistrix, Majestic, or similar export/API data.
- `Screenshot verified`: dated screenshot with visible source and context.
- `Technical crawl verified`: recognized crawler export with relevant fields.
- `Live SERP sample`: dated, localized, device-specific search sample.
- `Live search sample`: native search observation without a repeatable ranking dataset.
- `Inferred`: reasoned conclusion from confirmed observations.
- `Directional`: useful estimate or third-party/community actor signal requiring confirmation.
- `Not verified`: unavailable or unsupported.

`core/evidence-schema.json` is the authoritative label and finding contract. For machine-readable provenance, use `tools/evidence_ledger.py`. Restricted numeric metrics require a compatible evidence label, explicit provenance, and a matching source type. Modules must use these same labels; validate with `tools/validate_skill.py` after maintenance.

Every finding needs affected URLs, observation and interpretation with separate labels, evidence IDs/artifact locators, collection time, confidence, business impact, action, acceptance criteria, validation method and owner. Read `core/finding-contract.md`. Missing titles/H1s are source observations; short text, missing canonicals, duplicate text hashes and sitemap omissions require page-purpose/rendered/context review before fixes. Do not infer ranking loss from them.

For changing policies or capabilities, read `core/current-guidance-register.json`, verify relevant official sources and actual account/export fields during the audit, and record conflicts. Do not assume an AI-specific Search Console report exists or that standard Web totals isolate AI visibility.

## Start sequence

1. Identify website, audience/location, services and business goal. Inspect saved exports and tool capabilities; never print credentials.
2. Choose Full Intelligence, Apify Intelligence, Native Agent Scraping, File Analysis or Advisory from actual evidence. Capability detection is not authentication.
3. Read the relevant guide below and use a fresh dated output directory.
4. Run the deterministic pipeline and add supported specialist review.
5. Validate findings, source limitations, coverage, formulas and PDF layout.

## Runtime and offline execution

Install requirements.txt; copy templates/audit-config-template.json outside the skill. Set scope, limits and owner-priority URLs.
```text
python tools/audit_runner.py --config audit-config.json --output-dir output/site-date
python tools/audit_runner.py --config audit-config.json --crawl-snapshot pages.json --serp-snapshot serp.json --output-dir output/site-offline
```
The crawl-snapshot mode disables every network collector; aliases are --pages-json and --serp-json. Saved HTML/serialized DOM needs real source timestamps and collection methods. Unknown HTTP status stays unknown. Read `core/v1.5-workflows.md` for exact input contracts and individual CLI examples.

## Workflow routing

Load only needed sections. Consolidated guides retain source-module headings.
- Audits, traffic drops, rendered checks, WordPress/WooCommerce and migrations: `audit/audit.md`.
- International: `audit/international-seo-audit.md`; `tools/international_checks.py` checks observed HTML codes, self/return links and canonical conflicts.
- Schema parity: `tools/schema_validator.py`; local shape/text checks cannot establish Google eligibility.
- First-party quality, Clarity, Apify and native collection: `integrations/integrations.md`.
- Funnel review: `tools/funnel_joiner.py`; mismatched dates/segments return no diagnosis.
- Keyword architecture and ranks: `keyword-research/keyword-research.md`; `tools/cannibalization_check.py` emits query-overlap and link-graph review candidates, never automatic redirects.
- Competitor qualification: `competitor-research/competitor-research.md`; `tools/competitor_classifier.py`. Separate comparable businesses, content competitors and excluded ecosystems.
- Backlinks/outreach: `backlink-system/backlink-system.md`; `tools/backlink_classifier.py`. Patterns cannot establish penalties or justify automatic disavow.
- AEO/GEO/entities/reputation: `aeo-geo/aeo-geo.md`, `entity-seo/entity-seo.md`, `reputation-seo/reputation-seo.md`. No fabricated AI visibility or special-schema guarantees.
- Local/GBP: `local-seo/local-seo.md`; real eligible presence only.
- Vertical requirements: `industry-playbooks/industry-playbooks.md`; YMYL claims need qualified review and original proof.
- Content/growth: `strategy/strategy.md`; prioritize business evidence, dependencies and effort, not invented traffic forecasts.
- Social planning: `social-media/social-media.md`; no publishing without explicit authorization.
- PDF design, finding cards, branding and outcomes: `reporting/reporting.md`; `tools/report_builder.py`; `tools/outcome_tracker.py`.
- Templates: `templates/report-templates.md`; shared vendor/normalized column schemas: `core/import-schemas.json`.
- Setup, operations and prior paths: `core/operations.md`, `core/module-migration.json`.

## Completion gate

Distinguish observed facts, interpretations and unavailable data. Report coverage before sample scores. Retain evidence IDs, artifact locators and collection times. Match recommendations to page intent with owners, acceptance criteria and validation. Avoid arbitrary word targets, blanket canonical/noindex changes, automatic consolidation or causal growth claims.

After maintenance run tools/validate_skill.py and unittest discovery; refresh the inventory with tools/build_manifest.py. Preserve local-only configuration during install. Exclude credentials, caches and client artifacts from ZIPs. File limits apply to the distributable, not private output directories.

## Complete package index

Use this index for exact file discovery; it is not an instruction to load every file.

- Package: `LICENSE`, `MANIFEST.json`, `PLAYBOOK_DEPTH.md`, `README.md`, `RELEASE_NOTES.md`, `SKILL.md`, `_meta.json`, `requirements.txt`, `skill.json`.
- aeo-geo: `aeo-geo/aeo-geo.md`.
- agents: `agents/openai.yaml`.
- audit: `audit/audit.md`, `audit/international-seo-audit.md`.
- backlink-system: `backlink-system/backlink-source-database.csv`, `backlink-system/backlink-system.md`.
- competitor-research: `competitor-research/competitor-research.md`.
- core: `core/current-guidance-register.json`, `core/evidence-schema.json`, `core/finding-contract.md`, `core/import-schemas.json`, `core/module-migration.json`, `core/operations.md`, `core/scoring-methodology.md`, `core/v1.5-workflows.md`.
- entity-seo: `entity-seo/entity-seo.md`.
- examples: `examples/examples.md`.
- industry-playbooks: `industry-playbooks/industry-playbooks.md`.
- integrations: `integrations/integrations.md`.
- keyword-research: `keyword-research/keyword-research.md`.
- local-seo: `local-seo/local-seo.md`.
- reporting: `reporting/reporting.md`.
- reputation-seo: `reputation-seo/reputation-seo.md`.
- social-media: `social-media/social-media.md`.
- strategy: `strategy/strategy.md`.
- templates: `templates/audit-config-template.json`, `templates/backlink-prospect-template.csv`, `templates/competitor-matrix-template.csv`, `templates/content-calendar-template.csv`, `templates/first-party-metadata-template.json`, `templates/implementation-outcomes-template.csv`, `templates/issue-log-template.csv`, `templates/keyword-map-template.csv`, `templates/report-templates.md`, `templates/social-posting-30-day-template.csv`.
- tests: `tests/fixtures/current-audit.json`, `tests/fixtures/previous-audit.json`, `tests/test_reliability.py`, `tests/test_site_checks.py`, `tests/test_tooling.py`, `tests/test_v15.py`.
- tools: `tools/audit_compare.py`, `tools/audit_quality.py`, `tools/audit_runner.py`, `tools/backlink_classifier.py`, `tools/build_manifest.py`, `tools/cannibalization_check.py`, `tools/check_environment.py`, `tools/clarity_export.py`, `tools/competitor_classifier.py`, `tools/data_io.py`, `tools/evidence_ledger.py`, `tools/first_party_quality.py`, `tools/funnel_joiner.py`, `tools/international_checks.py`, `tools/lighthouse_runner.py`, `tools/normalize_apify_results.py`, `tools/outcome_tracker.py`, `tools/pdf_qa.py`, `tools/report_builder.py`, `tools/schema_validator.py`, `tools/site_checks.py`, `tools/sitemap_extractor.py`, `tools/snapshot_io.py`, `tools/source_classifier.py`, `tools/url_classifier.py`, `tools/validate_skill.py`.
