# Operations and capability reference

## automation-runtime

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
- `crawl-observations.json` and `crawl-coverage.json`
- `first-party-quality.json` for configured normalized imports
- `audit-config.sanitized.json` and `reproducibility-manifest.json` with tool/source hashes and artifact checksums
- `evidence-ledger.json` and `.csv`
- `competitor-classification.json`
- `audit-comparison.json` when a previous audit is supplied
- `report-input.json`
- `beyond-seo-audit.pdf`
- `beyond-seo-audit.qa.json`

Historical findings also use `Not rechecked` and `Not comparable`. Resolution requires the same check on every previously affected URL. Legacy findings without recorded checks cannot be automatically resolved. A lower known severity requires comparable rechecks before claiming improvement; higher known severity is worsened. Review `core/finding-contract.md` and `core/scoring-methodology.md`.

The runner performs bounded HTTP extraction, not JavaScript rendering or every specialist audit. It preserves slash/scheme variants, records response/header noindex observations and stops crawling when robots availability is unknown. Sitemap XML traversal and frontier limits are disclosed. Page-purpose signals require contextual review. Owner-supplied priority/template mappings are not inferred business value.

Sanitized parsed observations support reproducing built-in checks; full HTML and private raw analytics exports are not bundled. Keep private originals separately when exact replay requires them. Never reuse a prior output directory. Optional SERP failure becomes a data gap; it must not fabricate an empty-site ranking conclusion.

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


## data-quality-rules

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

Read `core/finding-contract.md` for traceability, `core/scoring-methodology.md` before scoring, `integrations/integrations.md#first-party-data-quality` before using GSC/GA4 totals, and `audit/audit.md#traffic-drop-diagnosis` for decline diagnosis.

Use `core/current-guidance-register.json` for changing policies and capabilities. Verify applicable primary documentation and actual account fields in the current audit. Record conflicting sources rather than silently selecting one. A screenshot validates only the visible data and scope, not an entire export/account.

Keep private raw data and credentials out of public repositories, reports and reproducibility bundles. Preserve necessary private originals in owner-controlled storage.


## decision-tree

# Decision Tree

Decision logic for choosing the right workflow.

---

## Start

Identify user goal: audit, keyword research, competitor research, backlinks, local SEO, AEO/GEO, proposal, report, or implementation.

## Capability

Check available data: URL, Apify, browser/search, files, GSC, GA4, GBP, backlink exports.

## Mode

Choose Full Intelligence, Apify Intelligence, Native Scraping, File Analysis, or Advisory mode.

## Output

Return the most useful deliverable: audit, roadmap, page brief, backlink evaluation, content calendar, proposal, or monthly report.


## final-output-standards

# Final Output Standards

Defines what every Beyond SEO response must include.

---

## Audit Output

Include what was checked, what was found, why it matters, what to do next, priority, and missing data.

## Strategy Output

Include goal, current situation, blockers, execution plan, KPIs, risks, and next action.

## Backlink Output

Include relevance, risk, authority, traffic, anchor advice, target page, and verdict.


## no-fluff-rules

# No-Fluff Rules

Rules that stop Beyond SEO from producing generic agency filler.

---

## Banned Generic Advice

Avoid empty advice like 'optimize SEO', 'write quality content', 'build backlinks', or 'improve visibility' unless followed by exact actions.

## Required Format

Every recommendation should include: issue, evidence, impact, exact fix, priority, and measurement.

## Reality Check

Never guarantee rankings or invent data. Label estimates clearly.


## seo-aeo-definition

# SEO, AEO, and GEO Definitions

Defines traditional SEO, answer engine optimization, and generative engine optimization.

---

## SEO

SEO improves crawlability, relevance, authority, and conversion for search engines and users.

## AEO

AEO makes content easier for answer engines to extract and use: direct answers, definitions, steps, FAQs, comparisons, costs, and trust signals.

## GEO

GEO improves the chance of being mentioned or cited by generative search systems through entity clarity, source-worthiness, topical authority, and structured content.

## Important

AEO/GEO is not a trick. It is strong SEO plus clearer, more trustworthy, answer-ready content.


## seo-principles

# SEO Principles

Core principles Beyond SEO must follow in every task.

---

## Main Rule

SEO recommendations must connect to crawlability, indexability, topical authority, search intent, local visibility, backlinks, conversion, AEO/GEO visibility, or measurement.

## Modern SEO View

Do not rely on keyword stuffing, fixed keyword density, or outdated checklist thinking. Build helpful, crawlable, structured, trusted pages that satisfy real search intent.

## Business Outcome

Traffic is not the final goal. Qualified leads, calls, bookings, enrollments, sales, authority, and measurable growth are the real outcomes.


## audit-modes

# Apify-First Audit Mode Override

Beyond SEO should prefer Apify Intelligence Mode whenever Apify is available.

## New Default Mode Priority

```text
1. Apify Intelligence Mode
2. Apify + File Analysis Mode
3. Native Agent Scraping Mode
4. File Analysis Mode
5. Advisory Mode
```

Full Intelligence Mode now means:

```text
Apify Intelligence Mode + authenticated/export-based Apify data + optional uploaded files.
```

The skill should not ask for separate GSC/GA4/Ahrefs/Semrush/Moz/PageSpeed APIs at the start. It should search/use Apify actors first.


---

# Audit Modes

Beyond SEO works in five modes. The agent must choose the correct mode before starting an audit, strategy, competitor analysis, backlink plan, or AEO/GEO task.

The goal is to produce the best possible result without pretending that unavailable data was checked.

---

## Mode Summary

```text
Mode 1: Full Intelligence Mode
Mode 2: Apify Intelligence Mode
Mode 3: Native Agent Scraping Mode
Mode 4: File Analysis Mode
Mode 5: Advisory Mode
```

---

# Mode 1: Full Intelligence Mode

## When to Use

Use this mode when the agent has most of the following:

```text
Website URL
Target market/location
Competitor URLs
Apify token or advanced crawler
Native browser/search/scraping
GSC export/access
GA4 export/access
Microsoft Clarity token/export when behavior evidence is relevant
GBP export/access if local
Ahrefs/Semrush/Moz export or authority data
Ability to process CSV/PDF/JSON files
```

## What This Mode Can Produce

```text
Full technical SEO audit
Page inventory
Crawlability and indexability review
Keyword ranking and opportunity review
GSC query/page performance analysis
GA4 conversion/landing page analysis
Microsoft Clarity behavior/friction analysis
Competitor SERP and content gap analysis
Local SEO and map pack analysis
Backlink/authority gap analysis
AEO/GEO readiness audit
Conversion SEO audit
30/60/90-day execution roadmap
Client-ready report
Developer task brief
Content and page brief plan
```

## Required Output Sections

```text
1. Data Sources Used
2. Executive Summary
3. Current SEO Health
4. Confirmed Technical Issues
5. Keyword and Page Opportunity
6. Competitor Gap
7. Local SEO Gap if relevant
8. Backlink/Authority Gap
9. AEO/GEO Gap
10. Conversion Gap
11. 30-Day Plan
12. 60-Day Plan
13. 90-Day Plan
14. KPIs
15. Remaining Data Gaps
```

## Confidence Level

High, if data is fresh and complete.

Still avoid guarantees.

---

# Mode 2: Apify Intelligence Mode

## When to Use

Use this mode when:

```text
APIFY_API_TOKEN is available
OR Apify MCP/tool access is available
```

but GSC/GA4/GBP/official backlink exports may be missing.

## What Apify Can Help With

Depending on actor availability:

```text
Website crawling
Competitor crawling
Sitemap crawling
SERP scraping
Google Trends checks
Google Maps/local scraping
Google reviews scraping
Ahrefs-style metrics via community actors
Semrush-style checks via community actors
Moz-style checks via community actors
Similarweb-style traffic checks
Social/content competitor scraping
Scheduled monitoring
```

## Important Caution

Apify is a marketplace. Actor quality varies.

Use labels:

```text
Confirmed: when actor output is reliable and directly observed.
Directional: when community actor data approximates third-party SEO metrics.
Not verified: when the actor does not support a needed metric.
```

Do not say “official Ahrefs data” unless the data came from an official export or authenticated official source.

## Required Process

```text
1. Identify needed actor categories.
2. Check actor availability.
3. Run/plan website crawl.
4. Run/plan SERP checks for target keywords.
5. Run/plan competitor crawls.
6. Run/plan local/maps checks if local business.
7. Run/plan authority-style checks if useful.
8. Normalize outputs.
9. Build audit and roadmap.
10. Mark missing GSC/GA4/GBP data.
```

## What This Mode Cannot Fully Confirm Without Other Data

```text
Actual GSC queries
Actual organic clicks/impressions
Actual GA4 conversions
Microsoft Clarity behavior signals unless an authenticated or dated export is supplied
Actual GBP calls/directions
Official Ahrefs/Semrush/Moz backlink counts
CRM lead quality
Revenue data
```

## Best Use Cases

```text
First serious SEO audit
Competitor research
SERP and content gap analysis
Local SEO scan
AI-search/AEO checks if actors support SERP/AI result scraping
Backlink/authority directional review
```

## Confidence Level

Medium to high for crawl/SERP/content findings.
Medium or directional for third-party authority metrics unless verified.

---

# Mode 3: Native Agent Scraping Mode

## When to Use

Use this mode when no Apify token is available, but the agent has:

```text
Browser/search access
Page opening ability
Scraper/crawler tool
Screenshot or HTML inspection
Manual SERP research capability
```

## What This Mode Can Produce

```text
Visible website audit
Basic technical observations
Content and on-page audit
Competitor visible page comparison
Manual SERP observations
Schema presence checks if HTML/source can be viewed
Internal linking observations
Local SEO visible checks
AEO/GEO content readiness review
Strategic 90-day plan
```

## Limitations

Cannot reliably confirm without specific tools/files:

```text
Full site crawl for large sites
Complete backlink profile
Exact search volume
Exact ranking history
GSC clicks/impressions
GA4 conversions
GBP performance
Core Web Vitals field data
```

## Required Output Labels

Use:

```text
Observed from available pages
Inferred
Not verified
Recommended next check
```

## Best Use Cases

```text
Fast first-pass audit
Client discovery review
Proposal preparation
Competitor page comparison
Service page gap discovery
AEO/GEO content improvement
```

## Example Output Note

```text
This audit is based on visible pages and available search/scraping access. It is strong for content, page structure, and strategy. It is limited for confirmed rankings, backlinks, traffic, and conversions because GSC, GA4, GBP, and backlink exports were not provided.
```

## Confidence Level

Medium for visible page findings.
Low for exact rankings/backlinks unless directly checked.

---

# Mode 4: File Analysis Mode

## When to Use

Use this mode when live tools are unavailable, but the user provides:

```text
SEO PDF reports
GSC exports
GA4 exports
Microsoft Clarity JSON/CSV exports
Screaming Frog exports
Sitebulb exports
Ahrefs exports
Semrush exports
Moz exports
Backlink sheets
Keyword sheets
Competitor reports
Client documents
Screenshots
```

## What This Mode Can Produce

```text
Report analysis
Findings summary
Prioritized action plan
Keyword map from exports
Backlink prospect review
Competitor strategy based on reports
90-day roadmap
Client proposal
Developer brief
```

## Required Process

```text
1. Identify file types.
2. Extract confirmed facts.
3. Separate data from recommendations.
4. Check for outdated data.
5. Build issue/opportunity summary.
6. Create roadmap.
7. List missing live checks.
```

## Important Caution

Files may be outdated. Metadata is not enough. Use document content and dates if available.

If the report says “current” but has old dates, label it:

```text
Potentially outdated. Needs live verification.
```

## Best Use Cases

```text
Turning existing audits into better plans
Upgrading client proposals
Building skill examples
Summarizing SEO exports
Creating execution briefs
Analyzing backlink lists
```

## Confidence Level

Depends on source freshness and completeness.

Use:

```text
Confirmed from uploaded file
Not independently verified live
```

---

# Mode 5: Advisory Mode

## When to Use

Use this mode when:

```text
No API
No browser/search
No scraping
No uploaded files
No exports
Only a general question or goal
```

## What This Mode Can Produce

```text
Manual audit checklist
Data request list
SEO strategy framework
Client intake form
Technical checklist
Backlink evaluation framework
AEO/GEO framework
Content plan template
90-day planning skeleton
```

## What This Mode Must Not Do

Do not claim:

```text
The site has X backlinks.
The site ranks for X keywords.
The site traffic is X.
Competitor has X pages.
Core Web Vitals are poor.
GBP is weak.
```

unless the user provided data.

## Best Use Cases

```text
Planning
Training
Prompt writing
Skill design
Client intake
SEO SOP creation
Manual checklist creation
```

## Confidence Level

Strategic only. Not an audit.

---

# Hybrid Modes

Sometimes the correct mode is a combination.

## Native + File Mode

Use when:

```text
Uploaded files exist
Browser/search/scraping exists
No Apify
```

Output:

```text
Audit Mode: Native Agent Scraping Mode + File Analysis
```

## Apify + File Mode

Use when:

```text
Apify exists
Uploaded exports/reports exist
```

Output:

```text
Audit Mode: Apify Intelligence Mode + File Analysis
```

## Advisory + Templates

Use when:

```text
No data exists but user needs deliverables
```

Output:

```text
Audit Mode: Advisory Mode
Deliverable: checklist/template/brief
```

---

# Audit Mode Selection Tree

Use this decision tree:

```text
START

Do I have enough data/tools for live verification?

IF Apify + GSC/GA4/backlink/GBP exports + competitor data:
    Full Intelligence Mode

ELSE IF Apify is available:
    Apify Intelligence Mode

ELSE IF browser/search/scraping is available:
    Native Agent Scraping Mode

ELSE IF uploaded files are available:
    File Analysis Mode

ELSE:
    Advisory Mode
```

If two sources exist, combine modes.

---

# Mode Announcement Template

For serious audits, include a short mode note:

```text
Audit Mode: [mode name]
Available: [data/tools]
Missing: [data/tools]
Confidence: [short note]
```

Example:

```text
Audit Mode: Apify Intelligence Mode
Available: website URL, target city, Apify token, competitor URLs
Missing: GSC, GA4, GBP, official backlink export
Confidence: strong for crawl/SERP/competitor checks; limited for actual traffic, conversions, and GBP call data.
```

---

# Mode-Specific Deliverables

## Full Intelligence Mode Deliverables

```text
Technical audit
Keyword audit
GSC opportunity report
GA4 conversion report
Microsoft Clarity behavior report
Competitor gap
Backlink gap
Local SEO audit
AEO/GEO audit
30/60/90-day plan
KPI dashboard outline
```

## Apify Intelligence Mode Deliverables

```text
Crawl report
SERP/competitor findings
Local/maps findings where actor supports it
Authority-style directional analysis
Keyword-to-page map
AEO/GEO recommendations
90-day plan
Missing-data list
```

## Native Agent Scraping Mode Deliverables

```text
Visible site audit
Manual competitor comparison
Content/page gap plan
Technical observations
AEO/GEO recommendations
Backlink/local next-check list
90-day strategy
```

## File Analysis Mode Deliverables

```text
Findings from files
Issue consolidation
Opportunity summary
Execution roadmap
Report rewrite/proposal
Missing live verification list
```

## Advisory Mode Deliverables

```text
Manual checklist
Data request list
Process guide
Templates
Strategic plan skeleton
```

---

# What to Do If the User Disagrees With Mode

If user says:

```text
No, do full audit without tools.
```

Respond:

```text
I can create a strategic audit framework and first-pass checklist, but I cannot honestly confirm rankings, backlinks, traffic, or technical crawl issues without live access, scraping, or exports.
```

Then continue in Advisory or File mode.

If user says:

```text
Use only my files.
```

Use File Analysis Mode and do not browse.

If user says:

```text
Do not use APIs.
```

Use Native Agent Scraping Mode or File Analysis Mode.

---

# Quality Gate Before Final Output

Before giving final output, check:

```text
Did I announce or internally select the correct mode?
Did I avoid inventing unavailable data?
Did I label estimates?
Did I include missing data?
Did I prioritize issues?
Did I connect actions to business impact?
Did I avoid guarantees?
```

If yes, proceed.

---

# Short Mode Reference

```text
Full Intelligence = best possible, complete data stack.
Apify Intelligence = strong crawl/SERP/data layer, missing first-party performance unless exports exist.
Native Scraping = good visible audit, limited hard metrics.
File Analysis = strong if exports/reports are good, needs live verification.
Advisory = strategy only, not verified audit.
```


## capability-detection

# Apify-First Capability Detection Override

Before using any other data/API path, check Apify first.

## Default Detection Order

```text
1. APIFY_API_TOKEN or Apify MCP
2. Apify actor shortlist
3. Website URL
4. Target country/city
5. Main goal
6. Apify datasets/exports already available
7. Native browser/search only if Apify is missing or unsuitable
8. Uploaded files only if provided or needed
```

## API Asking Rule

Do not ask for many APIs. Ask for `APIFY_API_TOKEN` only.

If GSC, GA4, PageSpeed, Ahrefs, Semrush, Moz, or backlink data is needed, first search/use Apify actor categories or Apify-hosted export workflows.

## Mode Selection

```text
IF APIFY_API_TOKEN or Apify MCP exists:
    Use Apify Intelligence Mode

ELSE IF native browser/search/scraping exists:
    Use Native Agent Scraping Mode and ask once for APIFY_API_TOKEN to upgrade

ELSE IF uploaded files exist:
    Use File Analysis Mode and ask once for APIFY_API_TOKEN to upgrade

ELSE:
    Use Advisory Mode and ask once for APIFY_API_TOKEN
```


---

# Capability Detection

Before any SEO task, Beyond SEO must detect available capabilities and choose the correct audit mode.

This prevents fake audits and helps the agent work properly across Codex, Claude, OpenClaw, Cursor, custom agents, and no-tool environments.

---

## 1. Detection Goal

The agent must answer:

```text
What can I actually access right now?
What can I verify?
What must be estimated?
What must be requested from the user?
Which audit mode should I use?
```

---

## 2. Detection Order

Check in this order:

```text
1. User-provided website URL
2. User-provided competitors
3. User-provided target location/market
4. Uploaded files or exports
5. Native browser/search access
6. Native scraping/crawling access
7. Apify API token or Apify MCP access
8. PageSpeed API access
9. GSC/GA4/Microsoft Clarity exports or access
10. Ahrefs/Semrush/Moz exports or screenshots
11. Google Business Profile data
12. Ability to run scripts/tools
```

---

## 3. Environment Variable Checks

If the agent can inspect environment variables, check:

```text
APIFY_API_TOKEN
PAGESPEED_API_KEY
GSC_EXPORT_PATH
GA4_EXPORT_PATH
CLARITY_API_TOKEN
CLARITY_EXPORT_PATH
AHREFS_EXPORT_PATH
SEMRUSH_EXPORT_PATH
MOZ_EXPORT_PATH
SCREAMING_FROG_EXPORT_PATH
SITEBULB_EXPORT_PATH
CUSTOM_SCRAPER_API_KEY
CUSTOM_SCRAPER_BASE_URL
```

Do not reveal secret values. Only state whether they are present.

Correct:

```text
APIFY_API_TOKEN detected.
```

Wrong:

```text
Your API token is apify_api_xxxxx.
```

---

## 4. Tool Capability Checklist

### Browser/Search

Can the agent search the web or open URLs?

If yes, it can:

```text
Check live pages
Inspect visible content
Find competitors
Check SERP manually
Find backlink opportunities
Check public profiles/directories
```

### Scraper/Crawler

Can the agent scrape or crawl multiple pages?

If yes, it can:

```text
Create page inventory
Extract titles/meta/H1/H2
Find thin pages
Find internal links
Classify URLs
Check schema snippets
Compare competitor pages
```

### Apify

Is `APIFY_API_TOKEN` or Apify MCP/tool access available?

If yes, it can potentially:

```text
Run website crawlers
Run SERP scrapers
Run Google Maps/local actors
Run Google Trends actors
Run authority-style actors
Run social/content scrapers
Schedule monitoring actors
Export structured datasets
```

Actor availability and quality must still be verified.

### File Access

Can the agent read uploaded files?

If yes, it can analyze:

```text
PDF reports
CSV keyword exports
GSC exports
GA4 exports
Microsoft Clarity JSON/CSV exports
Ahrefs exports
Semrush exports
Moz exports
Crawl exports
Backlink sheets
Competitor documents
```

### Code Execution

Can the agent run Python/Node/shell?

If yes, it can:

```text
Normalize CSVs
Merge keyword data
Score issues
Classify URLs
Build reports
Validate JSON/schema syntax
Generate templates
```

### No Tools

If no tools are available, the agent can still:

```text
Ask for data
Provide manual audit process
Create strategy templates
Prepare client/developer briefs
Explain what to check
```

---

## 5. Input Data Quality Labels

Use these labels in reports.

### Confirmed

Use when data was directly verified from a reliable source or file.

Example:

```text
Confirmed: GSC export shows 1,240 clicks from the target country in the last 90 days.
```

### Inferred
Use when evidence strongly suggests something but full verification is missing.

Example:

```text
Inferred: short extracted content requires rendered page and intent review; word count alone does not establish thin content.
```

### Directional

Use for third-party/community actor data or approximate tools.

Example:

```text
Directional: Apify Ahrefs-style actor suggests low authority, but this should be confirmed with Ahrefs/Moz/Semrush export.
```

### Directional
Use for calculations based on assumptions.

Example:

```text
Directional: at 10% visitor-to-query conversion, 500 monthly queries require around 5,000 qualified visits/interactions.
```

### Not verified

Use when a key data source was unavailable.

Example:

```text
Not verified: Google Business Profile performance was not available in this audit.
```

---

## 6. Capability Detection Output

Before a full audit, briefly state:

```text
Audit Mode:
Available Data:
Available Tools:
Missing Data:
How this affects confidence:
```

Example:

```text
Audit Mode: Native Agent Scraping Mode
Available Data: website URL, target city, 3 competitors
Available Tools: browser/search, page scraping
Missing Data: GSC, GA4, GBP, backlink export, Apify token
Confidence: strong for visible on-page and competitor content; limited for exact rankings, backlinks, and traffic.
```

For client-facing reports, include this as “Data Sources Used” and “Data Not Available.”

---

## 7. Mode Selection Logic

Use this decision tree:

```text
IF Apify + native browser/scraping + GSC/GA4/backlink exports are available:
    Use Full Intelligence Mode

ELSE IF Apify is available:
    Use Apify Intelligence Mode

ELSE IF native browser/search/scraping is available:
    Use Native Agent Scraping Mode

ELSE IF uploaded files/exports are available:
    Use File Analysis Mode

ELSE:
    Use Advisory Mode
```

If both files and native browser are available but no Apify exists, use:

```text
Native Agent Scraping Mode + File Analysis
```

If Apify exists but no live browser exists, use:

```text
Apify Intelligence Mode + File Analysis if files exist
```

---

## 8. What Each Capability Enables

### Website URL Only

Possible:

```text
First-pass audit
Visible content review
Basic technical checks if browser/scraper exists
Manual competitor discovery if search exists
```

Not possible without tools:

```text
Confirmed keyword rankings
Confirmed traffic
Confirmed backlinks
Confirmed GSC queries
Confirmed GBP performance
```

### Website URL + Apify

Possible:

```text
Structured crawl
SERP checks
Competitor crawl
Google Trends
Local/maps checks depending on actors
Authority-style directional checks depending on actors
```

Still may need:

```text
GSC/GA4 for actual performance
GBP access for actual calls/directions
Official Ahrefs/Semrush/Moz for verified authority/backlink metrics
```

### Website URL + GSC

Possible:

```text
Actual queries
Actual clicks/impressions
CTR issues
Pages with opportunity
Keyword cannibalization signals
Pages near ranking improvement
```

Need other tools for:

```text
Competitor gaps
Backlinks
Technical crawl
Local/map performance
```

### Website URL + GA4

Possible:

```text
Landing page performance
Engagement
Conversions if configured
Traffic source behavior
```

Need GSC for:

```text
Query-level SEO performance
```

### Website URL + Microsoft Clarity

Possible:

```text
Short-window URL/device/source behavior analysis
Engagement and scroll observations
Rage/dead clicks, excessive scrolling, quick backs, and script-error investigation
Heatmap/recording review plan
Conversion-event instrumentation recommendations
```

Need GSC, GA4, and CRM for:

```text
Search queries, reliable longer-term trends, qualified leads, revenue, and attribution
```

### Website URL + GBP

Possible:

```text
Local calls
Direction requests
Profile views
Review strategy
Local conversion behavior
```

Need SERP/map scraping for:

```text
Competitor map pack comparison
```

### Ahrefs/Semrush/Moz Exports

Possible:

```text
Backlink audit
Authority gap
Competitor authority comparison
Top pages
Ranking footprint
Keyword gaps
```

Caution:

```text
Different tools have different databases. Do not treat one tool as absolute truth.
```

---

## 9. Missing Data Request Rules

Only request missing data when it materially changes the output.

High-value asks:

```text
GSC export
GA4 conversion report
Microsoft Clarity export when behavior/CRO evidence would materially change the recommendations
GBP performance data
Competitor URLs
Ahrefs/Semrush/Moz backlink export
Apify token
Target city/service list
```

Low-value asks:

```text
Brand colors
Logo
Full company history
Every social link
```

Unless the task is a proposal or brand audit.

---

## 10. Confidence Notes

Every audit should include a confidence note if data is incomplete.

Example:

```text
This audit is strong for on-page structure, content gaps, and strategic planning. It is limited for confirmed rankings, backlinks, and conversion data because GSC, GA4, GBP, and authority exports were not provided.
```

---

## 11. Capability Detection Examples

### Example A: User Gives URL Only

Input:

```text
Audit https://example.com
```

If browser/search/scraping exists:

```text
Mode: Native Agent Scraping Mode
Proceed with visible crawl/search checks.
```

If no tools:

```text
Mode: Advisory Mode
Provide manual audit framework and request exports.
```

### Example B: User Gives URL + Apify Token

Input:

```text
Audit https://example.com. APIFY_API_TOKEN is available.
```

Output:

```text
Mode: Apify Intelligence Mode
Use Apify for crawl, SERP, competitor, and local/authority-style checks where actors exist.
```

### Example C: User Gives PDF Reports

Input:

```text
Use these SEO PDFs and make a plan.
```

Output:

```text
Mode: File Analysis Mode
Extract confirmed facts from PDFs, create recommendations, and label what needs live verification.
```

### Example D: User Gives Everything

Input:

```text
Website, competitors, GSC, GA4, GBP, Ahrefs export, Apify token.
```

Output:

```text
Mode: Full Intelligence Mode
Run complete technical, performance, keyword, competitor, local, backlink, AEO/GEO, and conversion audit.
```

---

## 12. Common Mistakes to Avoid

Do not:

```text
Choose Full Intelligence Mode just because a website URL was provided.
Claim backlink analysis without backlink data.
Claim rankings without SERP/GSC/rank data.
Treat Apify community actors as official Ahrefs/Semrush truth.
Ignore uploaded files.
Ask for APIs again after user already said they do not have them.
Stop working because one tool is missing.
```

---

## 13. Completion Rule

Capability detection is complete when the agent can clearly say:

```text
I know what data is available.
I know what tools are available.
I know what cannot be verified.
I know which audit mode to use.
I know how to proceed.
```


## INSTALL_FOR_AGENTS

# Apify-First Agent Install Note

For Codex, Claude, OpenClaw, Cursor, and custom agents:

1. Install the `beyond-seo` folder.
2. Configure only `APIFY_API_TOKEN` as the main token.
3. Restart the agent/runtime so the environment variable is loaded.
4. The skill should use Apify actors first for crawling, SERP, maps, trends, PageSpeed/Lighthouse, GSC/GA4-style connector/export workflows, and backlink/authority checks.

Do not place the token inside any Markdown, JSON, CSV, or report file.


---

# Install Beyond SEO in Different AI Agents

## Codex

1. Keep the folder name as `beyond-seo`.
2. Ensure `SKILL.md` is at the root of the folder.
3. `SKILL.md` includes YAML frontmatter for Codex-style skill discovery.
4. Add the full folder to the project or skills directory.
5. Tell Codex: "Use the Beyond SEO skill. Read SKILL.md first."

## Claude Projects

1. Upload the full `beyond-seo` folder or ZIP.
2. Add this project instruction:
   "Use Beyond SEO as the operating system for SEO, AEO/GEO, backlinks, local SEO, competitor research, keyword mapping, and reporting. Read SKILL.md first."

## OpenClaw

1. Add the folder to your skills or agent knowledge directory.
2. Register/alias it as `beyond-seo`.
3. Allow the agent to access the Markdown files and optional Python tools.
4. If Apify is available, expose `APIFY_API_TOKEN`.

## Cursor / Local Agents

1. Place the folder inside your repo.
2. Open `SKILL.md`.
3. Use the supporting modules as task-specific SOPs.
4. Install optional Python requirements only if using `/tools`.

## Optional Environment Variables

```text
APIFY_API_TOKEN
PAGESPEED_API_KEY
GSC_EXPORT_PATH
GA4_EXPORT_PATH
AHREFS_EXPORT_PATH
SEMRUSH_EXPORT_PATH
MOZ_EXPORT_PATH
SCREAMING_FROG_EXPORT_PATH
CUSTOM_SCRAPER_API_KEY
CUSTOM_SCRAPER_BASE_URL
```

## Optional Python Setup

```bash
pip install -r requirements.txt
```


## onboarding

# Beyond SEO Onboarding — Apify-First

This file controls the first interaction when a user asks for SEO, AEO/GEO, backlinks, local SEO, competitor research, or reporting.

The goal is simple: do not ask for too many things.

---

## 1. Default First Question

Ask only for the essentials:

```text
Send the website URL, target country/city, main goal, and make sure APIFY_API_TOKEN is configured. If Apify is available, I can fetch the rest through Apify actors wherever possible.
```

If the website URL and goal are already given, do not ask again. Start capability detection.

---

## 2. API Rule

The only default API/access request is:

```text
APIFY_API_TOKEN
```

Do not ask up front for:

```text
Google Search Console API
GA4 API
PageSpeed API key
Ahrefs API
Semrush API
Moz API
Firecrawl
DataForSEO
```

Reason: Beyond SEO is Apify-first. It should look for Apify actors, Apify MCP tools, Apify datasets, or Apify-hosted exports first.

---

## 3. When to Ask for Extra Access

Ask for extra access only when:

```text
Apify cannot fetch the data.
An authenticated first-party source is required.
A user wants exact GSC/GA4/GBP performance.
A user wants first-party behavior/friction evidence from Microsoft Clarity.
A paid SEO database actor requires the user's own account/export.
The user asks for official verification rather than directional data.
```

Even then, phrase it as:

```text
Apify can handle this if there is an authenticated connector/export actor. If not, upload the export or connect the account.
```

---

## 4. Minimal Audit Start

For most audits:

```text
1. Check APIFY_API_TOKEN or Apify MCP.
2. If present, enter Apify Intelligence Mode.
3. Ask only missing business context: website URL, target location, goal.
4. Run credit-safe crawl/SERP sample.
5. Expand only after findings justify it.
```

---

## 5. Good Opening Message

```text
I’ll use Apify as the main data layer. I need the website URL, target location if local, and your main goal. If APIFY_API_TOKEN is configured, I’ll start with a credit-safe crawl and SERP sample, then use Apify actors for competitors, maps, trends, PageSpeed/Lighthouse, and authority/backlink checks where needed.
```

---

## 6. Bad Opening Message

Do not say:

```text
Please provide GSC, GA4, Ahrefs, Semrush, Moz, PageSpeed API, Screaming Frog, GBP, DataForSEO, Firecrawl, and Apify.
```

That overwhelms the user and defeats the Apify-first design.

---

## 7. Token Handling

Never ask the user to paste tokens into normal content files.

Preferred:

```text
Environment variable: APIFY_API_TOKEN
Environment variable: CLARITY_API_TOKEN when Clarity reporting is requested
Agent secret manager
Apify MCP configuration
Secure runtime secret
```

If a token appears in chat, do not repeat it and do not save it into the skill.


## setup

# Apify-First Setup Update

Beyond SEO 1.3.0 is evidence-led and Apify-first, with a reusable audit runtime, provenance ledger, realistic competitor qualification, historical comparison, performance fallback, and report QA.

## Required Setup

Only one token is expected by default:

```text
APIFY_API_TOKEN
```

## Recommended Agent Behavior

At install or first use, check for `APIFY_API_TOKEN`.

If found:

```text
Use Apify Intelligence Mode.
```

If missing:

```text
Ask once for APIFY_API_TOKEN or Apify MCP setup.
```

Do not ask for GSC, GA4, Ahrefs, Semrush, Moz, PageSpeed API, DataForSEO, or Firecrawl by default. Use Apify actors first for those workflows where available.

For first-party behavior analysis, optionally use:

```text
CLARITY_API_TOKEN
CLARITY_EXPORT_PATH
```

Only request Clarity access when behavior, UX, CRO, or verified page-friction evidence is in scope.

## Optional Python Requirements

```bash
pip install -r requirements.txt
```


---

# Beyond SEO Setup Guide

This file explains how to install and use the Beyond SEO skill in different AI-agent environments.

Beyond SEO is designed as a portable folder-based skill. The agent should read `SKILL.md` first, then use the supporting files when a task requires setup, onboarding, capability detection, or audit mode selection.

---

## 1. Folder Placement

Recommended folder:

```text
beyond-seo/
├── SKILL.md
├── _meta.json
├── README.md
├── core/operations.md#setup
├── core/operations.md#onboarding
├── core/operations.md#capability-detection
└── core/operations.md#audit-modes
```

In future phases, additional folders will be added:

```text
integrations/
audit/
keyword-research/
competitor-research/
aeo-geo/
local-seo/
backlink-system/
strategy/
industry-playbooks/
reporting/
templates/
examples/
tools/
```

---

## 2. Required File Read Order

When loading this skill into an AI-agent system, instruct the agent to read files in this order:

```text
1. SKILL.md
2. _meta.json
3. README.md
4. core/operations.md#setup
5. core/operations.md#onboarding
6. core/operations.md#capability-detection
7. core/operations.md#audit-modes
```

For actual SEO work, the agent should always follow the operating rules in `SKILL.md`.

---

## 3. Recommended Agent System Prompt

Use this short instruction when attaching the skill folder to an agent:

```text
You have access to the Beyond SEO skill folder. Read SKILL.md first. Follow its no-fluff SEO, AEO/GEO, backlink, local SEO, competitor research, and reporting rules. Before any audit, use core/operations.md#capability-detection and core/operations.md#audit-modes to choose the correct operating mode based on available tools, APIs, files, and exports. Never invent rankings, traffic, backlinks, or search volume. Label estimates clearly.
```

---

## 4. Optional Environment Variables

Beyond SEO does not require APIs to function, but it becomes much stronger when these are available.

### Primary

```text
APIFY_API_TOKEN
```

Use this for Apify actors, crawling, scraping, SERP checks, maps/local checks, trends, authority-style data, and competitor data.

### Technical Checks

```text
PAGESPEED_API_KEY
```

Use this for PageSpeed Insights and Core Web Vitals where supported.

### Export Paths

```text
GSC_EXPORT_PATH
GA4_EXPORT_PATH
CLARITY_API_TOKEN
CLARITY_EXPORT_PATH
AHREFS_EXPORT_PATH
SEMRUSH_EXPORT_PATH
MOZ_EXPORT_PATH
SCREAMING_FROG_EXPORT_PATH
SITEBULB_EXPORT_PATH
```

These point to uploaded or local files the agent can analyze.

### Custom Scraping

```text
CUSTOM_SCRAPER_API_KEY
CUSTOM_SCRAPER_BASE_URL
```

Use these if the environment has a private scraper, crawler, or MCP scraping server.

---

## 5. Codex Setup

For Codex-style agent environments:

1. Add the `beyond-seo/` folder to the project repository.
2. Add or expose `APIFY_API_TOKEN` in the environment if available.
3. Tell Codex:

```text
Use the Beyond SEO skill. Read beyond-seo/SKILL.md first. For every SEO task, detect available APIs, files, and scraping tools, then choose the proper audit mode before producing output.
```

4. If Codex can run Python or shell commands, future tool scripts inside `tools/` can be used for environment checks and output normalization.

---

## 6. Claude Projects Setup

For Claude Projects:

1. Upload the complete `beyond-seo/` folder or files.
2. Add the short agent instruction from section 3.
3. When starting a task, provide:
   - website URL;
   - target market;
   - business type;
   - competitors if known;
   - exports if available.

Claude may not have direct environment variable access depending on setup. If so, paste API availability or exported reports manually.

---

## 7. OpenClaw Setup

For OpenClaw or similar file-based agent systems:

1. Place `beyond-seo/` in the skills or knowledge directory used by the agent.
2. Add a skill alias such as:

```text
beyond-seo
```

3. Make sure the agent can access:
   - browser/search tool;
   - scraper tool;
   - Apify MCP/API if configured;
   - local files/exports.

4. Instruct the agent:

```text
When the user asks for SEO, AEO, backlinks, competitors, local SEO, or website growth plans, activate Beyond SEO and follow its audit-mode detection.
```

---

## 8. Cursor Setup

For Cursor:

1. Add `beyond-seo/` to the project repo.
2. Open the workspace.
3. Ask Cursor:

```text
Read beyond-seo/SKILL.md and follow it as the operating rule for this SEO project.
```

4. If building SEO fixes for a website, use Beyond SEO outputs as developer briefs:
   - metadata changes;
   - schema;
   - page routes;
   - SSR/pre-rendering;
   - internal linking;
   - content blocks;
   - technical SEO fixes.

---

## 9. Custom Agent Setup

For any custom agent:

1. Load all Markdown files as system or knowledge instructions.
2. Give highest priority to `SKILL.md`.
3. Use `_meta.json` for metadata and feature discovery.
4. Expose API keys through environment variables.
5. Give the agent access to:
   - browser/search;
   - page scraper;
   - file reader;
   - CSV parser;
   - optional Apify API;
   - optional PageSpeed API.

The agent must not fail if APIs are missing.

---

## 10. Minimal Usage Example

User prompt:

```text
Audit https://example.com for SEO and AEO. I want a 90-day plan to increase qualified leads.
```

Beyond SEO response flow:

```text
1. Check available data/tools.
2. Choose audit mode.
3. Crawl or inspect the site.
4. Identify technical, content, keyword, local, backlink, and AEO gaps.
5. Prioritize issues.
6. Produce 30/60/90-day plan.
7. List missing data.
```

---

## 11. Strong Usage Example

User prompt:

```text
Audit https://example.com. Target city: Karachi. Main services: AI automation, AI agents, no-code systems. Competitors: competitor1.com, competitor2.com. I have Apify token and GSC export.
```

Beyond SEO should:

```text
1. Use Full Intelligence or Apify Intelligence Mode.
2. Crawl own site.
3. Crawl competitors.
4. Pull SERP/keyword opportunities if possible.
5. Analyze GSC export.
6. Build keyword-to-page map.
7. Create service pages and support article plan.
8. Add AEO/GEO recommendations.
9. Add local SEO recommendations if service-area relevant.
10. Produce 90-day execution roadmap.
```

---

## 12. Output File Creation

When the agent creates outputs, prefer:

```text
Markdown for reports
CSV for keyword maps and backlink prospects
JSON for machine-readable audit summaries
PDF/DOCX only when user explicitly asks for shareable documents
```

---

## 13. Safety and Honesty Rules

The agent must not:

- claim it crawled a site if it did not;
- claim it checked Apify if no token/tool existed;
- claim traffic or ranking data without evidence;
- recommend risky backlink packages;
- promise ranking timelines;
- hide missing data.

Use:

```text
Confirmed
Inferred
Directional
Not verified
```

---

## 14. Phase 1 Completion Test

After installing Phase 1, ask the agent:

```text
What audit mode would you use if I only provide a website URL and no API?
```

Correct answer:

```text
Native Agent Scraping Mode if browser/search/scraping tools exist; otherwise Advisory Mode. The agent should still provide a useful workflow and not pretend live data exists.
```

Second test:

```text
What audit mode would you use if I provide APIFY_API_TOKEN but no GSC/GA4?
```

Correct answer:

```text
Apify Intelligence Mode.
```

Third test:

```text
Can you guarantee top 3 ranking in 90 days?
```

Correct answer:

```text
No. Beyond SEO can build a realistic plan, but it cannot guarantee rankings.
```
