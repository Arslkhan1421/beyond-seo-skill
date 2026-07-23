---
name: beyond-seo
description: Run evidence-led SEO audits, AEO/GEO and local strategy, technical crawls, live SERP and realistic competitor research, Microsoft Clarity behavior analysis, keyword/rank baselines, content optimization, developer briefs, professional PDF reports, historical comparisons, CSV imports, and optional LinkedIn/Instagram planning. Use for website SEO audits, ranking diagnosis, UX/friction evidence, competitor gaps, content plans, recurring reports, and client-ready deliverables.
metadata:
  short-description: Evidence-led SEO, AEO/GEO, competitor, content, reporting, and social workflows
  version: 1.3.0
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
9. Render-check PDFs before delivery when rendering tools are available.
10. Explain unavailable tools plainly; do not expose raw rate-limit codes as client-facing findings.

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

For machine-readable provenance, use `tools/evidence_ledger.py`. It rejects restricted numeric metrics when the evidence label cannot support them.

## Start sequence

1. Identify the website, target country/location, services/products, and business goal.
2. Check `APIFY_API_TOKEN` and optional `CLARITY_API_TOKEN` without printing them.
3. Detect uploaded exports, including Microsoft Clarity JSON/CSV, and available crawl/browser/PDF/spreadsheet tools.
4. Select the audit mode.
5. Create or reuse a dated output directory; never overwrite the prior audit used for comparison.
6. Run the reusable pipeline when code execution is available.
7. Add specialist analysis from the relevant modules.
8. Produce the requested report, workbook, social export, and developer brief.
9. Validate evidence labels, formulas, PDF layout, and data gaps before delivery.

## Audit modes

### Full intelligence

Use when crawl/SERP plus first-party and authority data are available. Combine live evidence with GSC, GA4/CRM, Microsoft Clarity, GBP, crawler, and paid-tool exports.

### Apify intelligence

Use when `APIFY_API_TOKEN` exists but first-party exports do not. Start with the official Website Content Crawler and Google Search Scraper. Expand only when needed and credit-safe.

Read:

- `integrations/apify-first-operating-policy.md`
- `integrations/apify-actor-registry.md`
- `integrations/apify-workflows.md`
- `integrations/apify-ai-friendly-seo-workflows.md`

### Native agent scraping

Use browser/search/crawl tools when Apify is missing or unsuitable. Follow `integrations/native-agent-scraping.md` and `integrations/no-paid-seo-intelligence.md`.

### File analysis

Use uploaded CSV, JSON, XLSX, PDF, or crawler exports. Run `tools/source_classifier.py`; for Screaming Frog, Sitebulb, Lumar, or JetOctopus also read `integrations/technical-crawl-imports.md`.

### Advisory

When no live access or files exist, provide a clearly labeled plan and exact data request. Do not present site-specific facts.

## Reusable v1.3 runtime

When code execution is available, prefer the deterministic runner over one-off audit scripts.

1. Copy and edit `templates/audit-config-template.json` outside the skill folder.
2. Run:

```text
python tools/audit_runner.py --config audit-config.json --output-dir output/site-date
```

3. For month-over-month comparison:

```text
python tools/audit_runner.py --config audit-config.json --output-dir output/current --previous output/previous/audit-data.json
```

The runner creates crawl data, a rank baseline, qualified/excluded competitors, performance results, findings, an evidence ledger, comparison data, report input, and a PDF. Read `core/automation-runtime.md` for artifacts and quality gates.

If a different runtime is required, preserve the same output schema and evidence rules.

## Required audit coverage

For a full-depth website audit, cover:

- robots.txt, XML sitemaps, status codes, redirects, preferred host, canonicals, indexability, and crawl depth;
- titles, meta descriptions, H1/H2 structure, schema, renderability, duplicate content, thin pages, pagination, and internal links;
- money pages, proof/case studies, service coverage, intent, cannibalization, content clusters, E-E-A-T, and conversion paths;
- live localized SERP samples, target-page mapping, realistic competitors, content gaps, and rank baseline;
- AEO/GEO answer quality, entity clarity, source-worthiness, snippet eligibility, and structured data that matches visible content;
- local landing-page uniqueness, GBP/Maps evidence, NAP/citation consistency, reviews, service areas, and location proof when applicable;
- backlink/authority findings only when legitimate data exists;
- PageSpeed/Lighthouse/CrUX findings only when a test succeeds;
- CTA clarity, forms, calls/bookings, trust, and analytics/CRM measurement gaps.
- Microsoft Clarity behavior evidence when available: engagement, scroll depth, rage/dead clicks, excessive scrolling, quick backs, script errors, consent/masking, and configured business events.

Current Google AI-search guidance does not justify special AI schema, mass doorway variants, tiny artificial content chunks, or `llms.txt` claims for Google Search. Prefer crawlable, indexed, useful, expert-led content.

## Specialist modules

Load only the modules needed for the request:

- Full audit: `audit/full-site-audit.md`, `audit/technical-seo-audit.md`, `audit/content-quality-audit.md`, `audit/conversion-seo-audit.md`
- Rank baseline/history: `keyword-research/rank-tracker.md`
- Keyword architecture: `keyword-research/keyword-discovery.md`, `keyword-research/search-intent-analysis.md`, `keyword-research/keyword-to-page-map.md`
- Competitors: `competitor-research/competitor-deep-dive.md`
- Content rewrites: `strategy/content-optimizer.md`
- Developer tickets: `audit/technical-dev-brief.md`
- AEO/GEO: `aeo-geo/ai-friendly-seo-master-workflow.md`, `aeo-geo/geo-ai-citation-optimization.md`
- Local SEO: `local-seo/local-landing-pages.md`, `local-seo/map-pack-audit.md`, `local-seo/google-business-profile.md`
- Backlinks: `backlink-system/backlink-audit.md`, `backlink-system/link-gap-analysis.md`, `backlink-system/toxic-link-risk.md`
- Reporting: `reporting/report-builder-pro.md`, `reporting/pdf-report-design-system.md`, `reporting/visual-scorecards-and-evidence.md`
- Microsoft Clarity: `integrations/microsoft-clarity.md`; use `tools/clarity_export.py` for authenticated or saved exports
- Social strategy: the five files under `social-media/`

## Competitor selection

Use `tools/competitor_classifier.py` on live SERP candidates. Keep two separate groups:

- `Comparable`: realistic businesses competing for the same buyer and service.
- `Content competitor`: useful ranking page, publisher, or adjacent business but not a commercial benchmark.

Show excluded domains and reasons internally. Do not silently treat Reddit, Facebook, LinkedIn, directories, aggregators, or global platforms as realistic agency competitors.

## Rank tracking

A one-time SERP sample is a baseline, not ranking history. Record keyword, country, language, device, date/time, observed depth, position, URL, SERP features, source, and label. Use `Not visible within sampled top N`; never translate that to a fabricated position.

For recurring audits, preserve each dated `audit-data.json` and run `tools/audit_compare.py`. Report findings as New, Improved, Changed, Unchanged, Resolved, or Reopened.

## Performance

Use `tools/lighthouse_runner.py`. It attempts PageSpeed Insights, then locally installed Lighthouse. If neither completes, report `Not verified`; do not retain stale scores or infer Core Web Vitals.

Field Lighthouse data and lab Lighthouse data are different. Keep CrUX field evidence separate from lab measurements.

## Microsoft Clarity

Treat Clarity as first-party behavior evidence, not ranking evidence. The Data Export API covers only the previous 1–3 days, up to three dimensions, 1,000 rows without pagination, and 10 requests per project per day. Record the UTC retrieval time and window.

Add verified Clarity metrics and page-level friction signals to the PDF under **Microsoft Clarity Behavior Insights**. Do not infer causation, monthly trends, conversions, or SEO scores from short-window signals. Keep recordings, identifiers, and personal data out of reports. Verify consent and masking before recommending broader collection.

## Content and developer output

For every priority page provide, when relevant:

- target intent and page decision: improve, consolidate, redirect, create, or leave unchanged;
- recommended title, H1, meta description, section outline, FAQs, schema notes, internal links, proof requirements, and CTA copy;
- claims that require client/subject-matter-expert verification;
- developer task, affected URLs, business impact, required change, acceptance criteria, validation method, owner, priority, and evidence label.

Do not recommend mass-generated location or query variants without unique demand, operations, and proof.

## Reports and PDFs

Use `tools/report_builder.py` for repeatable audit PDFs or adapt its normalized JSON schema for richer client reports. Run:

```text
python tools/report_builder.py --input report-input.json --output output/pdf/report.pdf --qa
```

Report requirements:

- answer-first executive summary;
- data sources and confidence before scores;
- observed scorecards that exclude unverified categories;
- prioritized findings, rank baseline, qualified competitor gaps, direct website text, developer brief, roadmap, and exact data gaps;
- a Microsoft Clarity behavior section when verified data exists, or an explicit Clarity data gap when it does not;
- no copied proprietary logos or exact UI replicas;
- no broken text score bars, unexplained rate-limit codes, clipped tables, or accidental blank pages.

Use `tools/pdf_qa.py` and visually inspect rendered pages before delivery.

## Social mode

Social output is optional. Only load it when requested.

Read:

- `social-media/social-seo-strategy.md`
- `social-media/linkedin-post-builder.md`
- `social-media/instagram-content-builder.md`
- `social-media/social-calendar-builder.md`
- `social-media/social-posting-export.md`

Create platform-specific drafts, visual briefs, CTA, target URL, UTM URL, evidence label, approval status, and proof note. Do not claim performance before analytics exist. Do not auto-post without authenticated publishing access and explicit approval.

## Data imports

Templates under `templates/data-imports/` cover GSC, GA4, Microsoft Clarity, Semrush, Ahrefs, Moz, DataForSEO, Screaming Frog, and Sitebulb. Preserve source dates, retrieval windows, dimensions, and database/location fields. Reject incompatible or ambiguous columns instead of guessing.

Use first-party and paid-tool metrics exactly as supplied. Explain that Semrush/Ahrefs/Moz authority, traffic, volume, and difficulty are vendor estimates, not Google measurements.

## Completion gate

Before final delivery confirm:

- requested modules were actually used;
- every metric has a source and evidence label;
- no unsupported proprietary metric appears;
- comparable competitors are realistic;
- current and previous findings are not mixed;
- numeric scores exclude unverified areas;
- technical tasks have acceptance criteria;
- Clarity findings include the export window, source, evidence label, privacy limits, and no user-level data;
- social drafts have approval status and no fabricated proof;
- spreadsheet formulas contain no errors;
- PDF QA passes and rendered pages were reviewed;
- final response links every requested artifact and lists exact data needed next.
