# Reporting

Use the contents below to select the relevant workflow; load only the needed sections.


## action-report-contract

# Action-focused reports

Start with up to three evidence-backed findings, ordered by observed priority and affected business scope. Show action, owner, effort, dependencies and validation. Unknown effort stays Not verified. Detailed finding cards preserve observations, interpretations, affected URLs, business impact, evidence IDs/artifacts, dates and acceptance criteria.

Optional payload fields: `branding.logo_path` (trusted local image), `branding.contact`, and per-finding `effort`, `dependencies`. Never accept arbitrary remote image URLs. PDF bookmarks follow section headings; HTTP(S) links are clickable. Preserve evidence even when abbreviating executive actions.

For before/after tracking supply `outcomes` as raw rows accepted by `tools/outcome_tracker.py`. The PDF recomputes comparison status; implementation validation and measured change remain separate. Report source, comparable windows and confounders; no causal attribution.

Use plain language. Keep technical artifacts in the evidence details. Client colors should be applied consistently through the report builder palette and contrast-checked; automatic custom palette configuration is not available.


## aeo-geo-report

# AEO/GEO Report

Framework for writing the aeo/geo report.

---

## Required Sections

Data sources, key findings, business impact, priority actions, KPIs, and missing data.

## Tone

Clear, direct, client-friendly, no fake guarantees.

## Output

Use tables for findings and short strategy paragraphs for decisions.


## backlink-report

# Backlink Report

Framework for writing the backlink report.

---

## Required Sections

Data sources, key findings, business impact, priority actions, KPIs, and missing data.

## Tone

Clear, direct, client-friendly, no fake guarantees.

## Output

Use tables for findings and short strategy paragraphs for decisions.


## client-audit-report

# Client Audit Report Framework

This file defines how Beyond SEO creates client-ready SEO reports.

The report must be clear enough for business owners and strong enough for technical teams.

When the user asks for a PDF, polished file, dashboard-style report, or presentation-ready report, also load:

```text
reporting/reporting.md#pdf-report-design-system
```

---

## 1. Report Purpose

A client audit report should answer:

```text
Where are we now?
What is blocking growth?
What is the biggest opportunity?
What exactly will we do?
What results can be measured?
What data is missing?
```

---

## 2. Required Report Sections

```text
1. Cover / Report Title
2. Data Sources Used
3. Executive Summary
4. Current SEO Health Snapshot
5. Visual SEO Scorecard
6. Biggest Opportunity
7. Biggest Blockers
8. Authentic Keyword Snapshot
9. Competitor Keyword Gap
10. Website Improvement Recommendations
11. Technical SEO Findings
12. On-Page SEO Findings
13. Content / E-E-A-T Findings
14. Local SEO Gap if relevant
15. Backlink / Authority Gap
16. AEO / GEO Gap
17. Conversion SEO Gap
18. 30-Day Fix Plan
19. 60-Day Growth Plan
20. 90-Day Ranking / Query Plan
21. KPIs
22. Missing Data / Next Checks
```

---

## 3. Client Language Rules

Use plain language.

Bad:

```text
Canonicalization inconsistencies may produce suboptimal crawl budget allocation.
```

Better:

```text
Some pages may be confusing Google about which URL should rank. This can weaken rankings unless canonical tags are fixed.
```

---

## 4. Evidence Table

Every major claim should include evidence:

```text
Finding
Evidence
Business Impact
Fix
Priority
```

---

## 4.1 Visual Scorecard Requirement

Every client report should include a visual scorecard using text-safe visuals:

```text
Overall SEO Health: 72/100
[##############------] 72%
Status: Developing
```

Then include category scores:

```text
Technical SEO
On-page SEO
Content / E-E-A-T
Keyword Architecture
Authority / Backlinks
Local SEO if relevant
AEO / GEO
Conversion / Tracking
```

If a category is not verified, show it as `Not verified` instead of guessing a score.

---

## 4.2 Authentic Keyword and Competitor Data

Keyword and competitor keyword claims must include source labels.

Use:

```text
GSC
Google Ads Keyword Planner
Google Trends
Apify SERP scrape
Ahrefs/Semrush/Moz/DataForSEO export
Manual SERP sample
Competitor crawl
Bing Webmaster Tools
```

Separate:

```text
Competitor Ranking Keyword: verified from SERP/tool data.
Competitor Targeted Keyword: inferred from competitor page title/H1/content, ranking not verified.
```

Never present inferred competitor targeting as confirmed ranking data.

---

## 4.3 Website Improvement Text

For the top 5 recommendations, include a plain-English improvement block:

```text
Current problem
Why it matters
Recommended change
Example improvement text
Priority
Evidence
```

These blocks should explain exactly what to change on the website, including title tags, H1s, page sections, FAQs, schema, CTAs, internal links, speed fixes, local proof, or conversion improvements where relevant.

---

## 5. Report Tone

The tone should be:

```text
Confident
Specific
Honest
Commercially focused
No fake guarantees
No fear-mongering
No generic SEO fluff
```

---

## 6. Executive Summary Pattern

```text
The website has [main strength], but growth is limited by [main blockers]. The fastest path to growth is [strategy]. The 90-day plan focuses on [foundation], [expansion], and [authority/conversion].
```

---

## 7. Client Report Output

Use tables for:

```text
Visual scores
Issues
Keywords
Competitors
Page recommendations
Backlinks
Roadmap
KPIs
```

Use paragraphs for:

```text
Executive summary
Strategic explanation
Risk notes
Next step
```


## competitor-report

# Competitor Report

Framework for writing the competitor report.

---

## Required Sections

Data sources, visual competitor scorecard, verified competitor keyword table, inferred competitor targeting table, key findings, business impact, priority actions, KPIs, and missing data.

---

## Competitor Scorecard

Include a visual comparison:

```text
| Domain | Organic Visibility | Content Depth | Authority | Local Strength | AEO/GEO Readiness | Overall |
|---|---:|---:|---:|---:|---:|---:|
| Client | 58 [############--------] | 52 | 41 | 70 | 45 | 53 |
| Competitor A | 78 [################----] | 82 | 75 | 72 | 67 | 75 |
```

Only score areas with evidence. Mark unknown areas as `Not verified`.

---

## Competitor Keyword Evidence

Separate competitor keyword types:

```text
Competitor Ranking Keyword:
Verified from Semrush, Ahrefs, DataForSEO, SE Ranking, Sistrix, Moz, or live SERP sample.

Competitor Targeted Keyword:
Inferred from title, H1, URL, headings, schema, or content. Ranking is not verified.
```

Use this table:

```text
| Competitor | Keyword | Evidence Type | Source | Source Date | Competitor URL | Position | Client URL | Gap | Action | Confidence |
|---|---|---|---|---|---|---:|---|---|---|---|
```

Never report competitor keywords as authentic ranking data without a source.

## Tone

Clear, direct, client-friendly, no fake guarantees.

## Output

Use tables for findings and short strategy paragraphs for decisions.

Include plain-English website improvement recommendations for the client's top competitor gaps.


## executive-summary

# Executive Summary Report

Framework for writing the executive summary report.

---

## Required Sections

Data sources, key findings, business impact, priority actions, KPIs, and missing data.

## Tone

Clear, direct, client-friendly, no fake guarantees.

## Output

Use tables for findings and short strategy paragraphs for decisions.


## implementation-outcomes

# Implementation and Outcomes

Use `templates/implementation-outcomes-template.csv` and:

```text
python tools/outcome_tracker.py --input implementation-outcomes.csv --output outcomes.json
```

Connect tasks to URLs, finding/evidence IDs, owner, implementation date, validation result/evidence, business metric/unit, baseline/follow-up values/windows, source/property, segment/filters, timezone, measurement evidence and confounders. Choose an observation window appropriate to traffic and metric; do not promise a fixed SEO response time.

- **Fix verified**: acceptance criteria passed with recorded evidence.
- **Observed change**: comparable dated measurements show a positive, negative or zero delta. This does not establish that the fix caused it.

Baseline precedes implementation; follow-up follows it. Missing, overlapping or unequal windows are Not comparable. Zero baseline permits an absolute delta but no growth percentage. The tracker validates supplied records; it does not authenticate declarations or screenshots. Causation requires a defensible experiment/design, controls, sufficient data and confounder analysis.

Keep CRM leads/revenue distinct from analytics key events. Record other deployments, campaigns, search updates, seasonality and tracking changes. Do not publish client measurement data in the public skill repository.


## keyword-report

# Keyword Report

Framework for writing the keyword report.

---

## Required Sections

Data sources, visual keyword opportunity score, key findings, authentic keyword table, business impact, priority actions, KPIs, and missing data.

---

## Authentic Keyword Requirement

Every keyword must show its source.

Accepted sources:

```text
Google Search Console
Google Ads Keyword Planner
Google Trends
Semrush
Ahrefs
Moz
DataForSEO
SE Ranking
Sistrix
Bing Webmaster Tools
Apify SERP scrape
Manual SERP sample
People Also Ask / related searches scrape
```

Use this table:

```text
| Keyword | Intent | Location | Source | Source Date | Volume | Difficulty | Current Rank | Current URL | Opportunity | Action | Confidence |
|---|---|---|---|---|---:|---:|---:|---|---|---|---|
```

If volume, rank, or difficulty is missing, write `Not verified`.

---

## Keyword Opportunity Visual

Include a score or visual for each major cluster:

```text
Service keywords: 82/100 [################----]
Local keywords: 74/100 [###############-----]
Informational support: 58/100 [############--------]
```

Explain the score using business value, intent strength, ranking feasibility, current gap, and conversion potential.

## Tone

Clear, direct, client-friendly, no fake guarantees.

## Output

Use tables for findings and short strategy paragraphs for decisions.

Never output a keyword list that looks precise but has no source.


## monthly-progress-report

# Monthly SEO Progress Report

This file defines monthly reporting for ongoing SEO campaigns.

---

## 1. Purpose

Monthly reporting should show:

```text
What changed?
What improved?
What was completed?
What still blocks growth?
What happens next?
```

---

## 2. Required Sections

```text
1. Month Summary
2. Work Completed
3. Keyword Movement
4. GSC Performance
5. GA4 / Conversion Performance
6. GBP Performance if local
7. Content Published
8. Technical Fixes
9. Backlinks / Authority Work
10. AEO/GEO Progress
11. Issues / Risks
12. Next Month Plan
```

---

## 3. KPI Table

```text
Metric
Previous Month
Current Month
Change
Notes
```

Use for:

```text
GSC clicks
GSC impressions
Average CTR
Average position
Organic sessions
Conversions
Phone/WhatsApp clicks
GBP calls/directions
Top 10 keywords
Referring domains
Indexed pages
```

---

## 4. Reporting Rule

Do not hide bad news.

If rankings did not move, explain why:

```text
Implementation delay
Indexing delay
Authority gap
Competitive SERP
Content not published
Tracking issue
Algorithm volatility
```

Then give next action.


## pdf-report-design-system

# PDF Report Design System

Use this file when the user asks Beyond SEO to create a PDF, client-ready audit, agency-style SEO report, dashboard-style report, or final report file.

The goal is to produce a polished SEO PDF that feels familiar to users of Semrush, Ahrefs, DataForSEO, Moz, Google Search Console, and GA4 without copying any proprietary interface, branding, logos, screenshots, or protected UI exactly.

For repeatable PDF generation, prefer:

```text
tools/report_builder.py
```

Build or normalize audit data into the script's JSON schema, generate the PDF, then render-check the output before delivery.

---

## 1. PDF Creation Workflow

When creating a PDF report:

```text
1. Finish the audit analysis first.
2. Identify which metrics are verified, sampled, inferred, or not verified.
3. Choose the report structure and visuals from this file.
4. Generate the PDF under output/pdf/.
5. Render representative pages to PNG using Poppler/pdftoppm or an equivalent renderer.
6. Inspect the cover, scorecard page, and densest table page.
7. Fix clipped text, cramped tables, weak contrast, or bad page breaks.
8. Return the final PDF path/link.
```

Use a PDF generation tool such as ReportLab when available. If the runtime has a dedicated PDF skill or PDF rendering workflow, follow it.

---

## 2. Visual Direction

Use a professional dashboard/report style:

```text
Clean white or very light background
Dark navy/charcoal headings
Muted gray body text
One primary accent color
Traffic-light colors for status only
Small KPI cards
Horizontal score bars
Compact data tables
Clear section headers
Footer with report name, source mode, and page number
```

Do not use:

```text
Exact Semrush/Ahrefs/DataForSEO/Moz/GSC/GA4 logos without permission
Exact copied UI screenshots unless provided by the user
Fake dashboard charts with invented numbers
Decorative gradients that reduce readability
Oversized marketing hero layouts
```

Allowed inspiration:

```text
Semrush-style: authority/keyword/competitor widgets, issue severity cards, keyword gap tables.
Ahrefs-style: backlink/organic keyword/top pages tables, DR-style authority panels, traffic estimate notes.
DataForSEO-style: SERP result tables, API/source evidence blocks, rank absolute/rank group fields.
Moz-style: DA/PA/spam-score style authority cards, SERP difficulty review panels.
GSC-style: clicks, impressions, CTR, average position cards and query/page tables.
GA4-style: traffic channel, landing page, conversion, engagement, and event summary cards.
```

Always label the source and confidence of each visual.

---

## 3. Recommended PDF Structure

Use this order for full audits:

```text
1. Cover page
2. Executive summary
3. SEO health dashboard
4. Data sources and confidence
5. Technical SEO findings
6. Page inventory snapshot
7. Keyword opportunity dashboard
8. Competitor gap dashboard
9. Backlink and authority section
10. Local SEO / AEO-GEO section when relevant
11. Website improvement text blocks
12. 30/60/90-day roadmap
13. Data needed next
14. Source links / appendix
```

For shorter audits, keep:

```text
Cover
Executive summary
Scorecard
Top findings
Keyword/competitor table
Roadmap
Data gaps
```

---

## 4. Required Dashboard Components

### Cover

Include:

```text
Client/site name
Report type
Website URL
Audit date
Audit mode
Prepared by Beyond SEO
One-line summary
```

### Executive KPI cards

Use 3 to 6 compact cards:

```text
Overall SEO Health
Technical Status
Keyword Opportunity
Authority Status
Content Gap
Tracking Confidence
```

Each card must include:

```text
Metric or label
Value
Status color
One short reason
Source/confidence
```

### Score bars

Use horizontal score bars for:

```text
Technical SEO
On-page SEO
Content / E-E-A-T
Keyword Architecture
Authority / Backlinks
Local SEO
AEO / GEO
Conversion / Tracking
```

If unverified:

```text
Show Not verified
Use gray bar
Explain required data source
```

### Tables

Use wrapped, readable tables for:

```text
Findings
Keywords
Competitors
Pages
Backlinks
Roadmap
Data gaps
```

Avoid tables wider than the page. Split long tables across pages intentionally.

---

## 5. Tool-Style Report Modules

### Semrush-inspired module

Use for:

```text
Organic keyword gap
Authority Score if verified
Competitor overlap
Site audit issues
Keyword intent and difficulty
```

Visuals:

```text
Keyword gap matrix
Issue severity cards
Competitor overlap table
Organic positions snapshot
```

Required warning if no Semrush export:

```text
Semrush metrics were not verified. This section uses manual SERP and competitor-page evidence.
```

### Ahrefs-inspired module

Use for:

```text
DR if verified
Referring domains
Top pages
Organic keywords
Content gap
Anchor risk
```

Visuals:

```text
Authority card
Top pages table
Backlink prospect/risk table
Content gap matrix
```

Required warning if no Ahrefs export:

```text
Ahrefs DR, backlinks, referring domains, traffic, and keyword footprint were not verified.
```

### DataForSEO-inspired module

Use for:

```text
SERP samples
Rank tracking snapshots
Location/device result differences
SERP features
Local/map results
```

Visuals:

```text
SERP sample table
Rank absolute/rank group table
SERP feature badges
Location/device/date evidence block
```

Required fields:

```text
Keyword
Location
Language
Device
Date collected
Rank/visibility if verified
URL/domain
SERP features
Confidence
```

### Moz-inspired module

Use for:

```text
DA/PA if verified
Spam Score if verified
Link risk
SERP difficulty review
```

Visuals:

```text
Authority comparison cards
Spam-risk badge
SERP difficulty panel
Link quality table
```

### GSC-inspired module

Use only when GSC data is provided.

Visuals:

```text
Clicks
Impressions
CTR
Average position
Top queries
Top pages
Branded vs non-branded split
Generative AI/Search appearance fields when available
```

If GSC is unavailable:

```text
Do not create fake GSC charts. Show Data needed next.
```

### GA4-inspired module

Use only when GA4 data is provided.

Visuals:

```text
Organic sessions/users
Landing pages
Engagement rate
Key events/conversions
Traffic channels
Device split
Conversion path notes
```

If GA4 is unavailable:

```text
Do not create fake GA4 charts. Show tracking data gap.
```

---

### Microsoft Clarity behavior module

Use only when authenticated Clarity Data Export API data, an owner-supplied dated export, or a dated dashboard screenshot exists.

Show:

```text
Evidence label
UTC retrieval time
Previous 1–3 day window
Dimensions used
Traffic/engagement/scroll observations
Rage clicks, dead clicks, excessive scrolling, quick backs, and script/error-click signals
Affected URL or segment
Recommended investigation or experiment
API limits and privacy/consent note
```

Use exact values returned by the source. Do not convert behavior signals into an SEO ranking score, claim causation, or extrapolate the API window into a monthly trend. Keep recordings, identifiers, and personal data out of the PDF.

If Clarity is unavailable:

```text
Microsoft Clarity: Not verified. Connect CLARITY_API_TOKEN or provide a dated export.
```

---

## 6. Chart Rules

Allowed charts:

```text
Horizontal score bars
Stacked status bars
Small trend lines only with time-series data
Donut/ring only for real proportions
Heatmap table for issue priority
Roadmap timeline
SERP feature badges
```

Do not use:

```text
Line charts without dates
Pie charts for guessed splits
Traffic forecasts without assumptions
Authority charts without verified tool data
Keyword volume charts without verified volume source
```

For unverified data, use:

```text
Gray cards
Not verified label
Recommended source
Confidence note
```

---

## 7. Data Confidence Strip

Every PDF should include a visible data confidence strip near the front:

```text
Confirmed: crawl, sitemap, robots, metadata
Live SERP sample: live SERP checks
Inferred: competitor targeting from page content
Not verified: Semrush/Ahrefs/Moz/DataForSEO metrics, GSC/GA4, backlinks, traffic, conversions
```

Adjust the strip based on actual inputs.

---

## 8. PDF Copy Rules

Use client-friendly language.

Prefer:

```text
This metric is not verified because no Ahrefs/Semrush export was provided.
Manual SERP samples show competitors targeting this keyword.
The page is crawlable, but it is missing from the XML sitemap.
```

Avoid:

```text
Your DR is low
Traffic is down
This keyword has 2,000 searches
Competitor ranks for 5,000 keywords
```

unless verified by a cited source.

---

## 9. File Naming

Use stable, descriptive filenames:

```text
output/pdf/{client-slug}-seo-audit-report.pdf
output/pdf/{client-slug}-keyword-gap-report.pdf
output/pdf/{client-slug}-technical-seo-report.pdf
```

If the user asks for a new version:

```text
output/pdf/{client-slug}-seo-audit-report-v2.pdf
```

---

## 10. Final Delivery

Final response should include:

```text
PDF path/link
Short note on what the PDF includes
Verification status: rendered/inspected or unable to render
Any data gaps that remain
```

Do not make the final answer longer than the report itself. The PDF is the deliverable.


## proposal-style-report

# Proposal-Style SEO Report

This file defines how Beyond SEO turns audit findings into a sales/client proposal.

A proposal should sell the strategy without exaggerating.

---

## 1. Purpose

A proposal-style report answers:

```text
Why does the client need SEO?
What is the opportunity?
What will we do?
Why is this approach different?
What can the client expect?
```

---

## 2. Proposal Structure

```text
1. Current Situation
2. Opportunity
3. Main Problems Found
4. Our Strategy
5. Deliverables
6. 90-Day Execution Plan
7. Expected Movement
8. KPIs
9. Why This Will Work
10. What We Need From Client
11. Next Step
```

---

## 3. Recommended Wording

Use:

```text
increase probability
build ranking foundation
expand keyword footprint
improve qualified visibility
turn traffic into queries
```

Avoid:

```text
guaranteed ranking
instant results
secret Google trick
AI will rank you automatically
```

---

## 4. Deliverables Template

```text
Technical SEO fixes
Service/course/product page optimization
New landing pages
Support article cluster
Internal linking
Schema
Local SEO/GBP optimization
Backlink/source building
AEO/GEO improvements
Conversion tracking
Monthly reporting
```

---

## 5. Expected Movement Section

```text
In 90 days, the goal is to build a stronger ranking foundation, expand keyword coverage, improve crawlability, publish high-intent pages, improve local signals, and start authority growth. Ranking movement depends on implementation speed, competition, authority gap, and indexation.
```

---

## 6. Proposal Rule

The proposal must feel valuable before pricing is discussed.

Specificity sells. Fluff doesn’t.


## report-builder-pro

# Report Builder Pro

Use this module when the user asks for a client-ready PDF, monthly report, proposal-style report, executive report, or visual SEO dashboard.

## Required Inputs

Non-demonstration reports require finding contracts and matching `evidence_records`; the builder validates them before PDF generation. Read `core/finding-contract.md` and `core/scoring-methodology.md`. Keyword volume/difficulty must match ledger values for the keyword scope. Legacy payloads must be normalized to the current contract rather than disabling verification. `--sample` visibly labels its synthetic demonstration data.

- Website URL, brand name, target market, services, and business goal.
- Crawl findings, SERP samples, keyword tables, competitor rows, issue log, and roadmap.
- Verified exports when available: GSC, GA4, Microsoft Clarity, Semrush, Ahrefs, Moz, DataForSEO, Screaming Frog, Sitebulb.
- Evidence labels for every metric.

## Report Modes

Choose one mode before writing:

- Full audit report: diagnosis, findings, scorecards, fixes, roadmap.
- Monthly progress report: movement, completed work, KPI changes, next-month plan.
- Competitor gap report: SERP competitors, content gaps, authority gaps, page comparisons.
- Proposal report: opportunity, pain points, scope, timeline, expected movement, data gaps.
- Developer handoff report: technical tasks, acceptance criteria, owners, priority.

## Client-Ready Structure

Include these sections for full reports:

1. Cover and audit scope.
2. Executive summary.
3. Data confidence and source labels.
4. SEO health dashboard.
5. Technical findings.
6. Page inventory and indexability.
7. Keyword and SERP opportunity.
8. Competitor gap.
9. Microsoft Clarity behavior insights when verified.
10. Content, E-E-A-T, AEO/GEO, local, and conversion gaps.
11. Website improvement text.
12. Prioritized action plan.
13. 30/60/90-day roadmap.
14. Data not available and recommended exports.

## Visual Rules

- Use scorecards only for areas supported by evidence.
- Mark unverified metrics as `Not verified`; never force them into numeric charts.
- Use traffic-light severity, score bars, issue tables, keyword tables, and roadmap panels.
- Do not copy Semrush, Ahrefs, Moz, DataForSEO, GSC, or GA4 branding or proprietary UI.
- For Clarity, show the UTC retrieval time, 1–3 day window, dimensions, exact observed values, evidence label, and investigation action. Do not include recording links, identifiers, personal data, or causal claims.
- Keep tables readable in PDF: short columns, wrapped text, and repeated headers.

## PDF Completion Contract

- Write PDFs to `output/pdf/`.
- Write source Markdown/JSON to `output/reports/` when useful.
- Render the PDF to PNG and inspect representative pages before delivery.
- If rendering fails, still provide the PDF but clearly say render verification failed.

## Final Delivery

Return:

- PDF path.
- Supporting report path when created.
- Tools and sources used.
- Render-check status.
- Data gaps that affect confidence.


## technical-report

# Technical SEO Report

Framework for writing the technical seo report.

---

## Required Sections

Data sources, key findings, business impact, priority actions, KPIs, and missing data.

## Tone

Clear, direct, client-friendly, no fake guarantees.

## Output

Use tables for findings and short strategy paragraphs for decisions.


## visual-scorecards-and-evidence

# Visual Scorecards and Evidence Reporting

Use this file whenever the user asks for a report, client audit, SEO dashboard, keyword report, competitor report, or website improvement plan.

The goal is to make Beyond SEO reports easier to understand while keeping every score evidence-based.

Read `core/scoring-methodology.md` first. Numeric examples below illustrate visual formatting, not validated site measurements or a required rubric. A partial crawl gets a scoped sample diagnostic with coverage, not an overall SEO score. Unmeasured categories stay Not verified; never use issue-count deductions.

For PDF output, also load:

```text
reporting/reporting.md#pdf-report-design-system
```

---

## 1. Required Visual Score Elements

Every serious report should include a simple visual scorecard.

Use text-safe visuals that work in Markdown, docs, PDFs, and chat:

```text
Overall SEO Health: 72/100
[##############------] 72%
Status: Good foundation, needs content + authority expansion
```

Use score bands:

```text
0-39   Critical
40-59  Weak
60-74  Developing
75-89  Strong
90-100 Excellent
```

Use traffic-light labels:

```text
Red: urgent blocker
Amber: important improvement
Green: working well
Gray: not verified from available data
```

---

## 2. SEO Health Visual Table

Default scorecard:

```text
| Area | Score | Visual | Status | Main Reason | Next Action |
|---|---:|---|---|---|---|
| Technical SEO | 16/20 | [################----] | Strong | Crawlable, but speed issues remain | Fix CWV on money pages |
| Content / E-E-A-T | 11/20 | [###########---------] | Weak | Service pages are thin | Expand money pages |
```

Scores must be supported by findings. Do not score categories with no data as if they were verified.

If data is missing:

```text
Score: Not verified
Visual: [????????????????????]
Reason: GSC/GA4/backlink/GBP data was not provided.
```

---

## 3. Priority Heatmap

Use a heatmap-style table for client decisions:

```text
| Action | Impact | Effort | Confidence | Priority | Why |
|---|---:|---:|---:|---|---|
| Fix indexable duplicate city pages | 5 | 2 | 5 | Must Fix Now | Reduces crawl waste and ranking confusion |
| Add 6 service pages | 5 | 4 | 4 | High Impact Next | Captures missing money intent |
```

Priority formula:

```text
Priority = Impact + Confidence - Effort - Risk
```

Labels:

```text
Must Fix Now
High Impact Next
Strategic Build
Monitor
Ignore for Now
```

---

## 4. Authentic Keyword Evidence Rules

Keyword data must be labeled by source.

Allowed keyword evidence sources:

```text
Google Search Console export/API
Google Ads Keyword Planner export
Google Trends
Apify SERP scrape
Ahrefs/Semrush/Moz/DataForSEO export
Manual live SERP sample
Competitor page/title/H1/content crawl
People Also Ask / related searches scrape
Bing Webmaster Tools export
```

Every keyword table must include:

```text
Keyword
Intent
Source
Verification status
Current URL if known
Current rank if verified
Search volume if verified
Competitor URL if verified
Action
Confidence
```

Do not invent search volume, ranking, CPC, difficulty, or competitor ownership. If unavailable, use:

```text
Not verified from available data
Recommended source: [exact source]
```

---

## 5. Competitor Keyword Evidence Rules

Competitor keywords are authentic only when supported by one of:

```text
SEO tool export showing competitor keyword rankings
SERP scrape showing competitor page ranking for the query
GSC is not valid for competitor data unless the competitor owns/provides it
Manual SERP check with location/device/date noted
Competitor page crawl showing clear targeting, labeled as "targeted by competitor", not "ranking"
```

Use two different labels:

```text
Competitor Ranking Keyword: verified competitor ranking from SERP/tool data.
Competitor Targeted Keyword: inferred from competitor title/H1/content, ranking not verified.
```

Never mix the two.

---

## 6. Keyword Opportunity Visual

Use this table for keyword opportunities:

```text
| Keyword | Intent | Evidence | Current Position | Best Competitor | Opportunity | Confidence | Action |
|---|---|---|---:|---|---|---|---|
| emergency dentist chicago | Local urgent | SERP sample + competitor crawl | Not verified | example.com/emergency-dentist | Missing money page | Medium | Create local service page |
```

Opportunity labels:

```text
Existing Winner
Fastest Win
Missing Money Page
Competitor-Owned
Topical Authority Builder
Brand Defense
AEO Opportunity
Local Map Intent
Ignore for Now
```

---

## 7. Website Improvement Text Blocks

Reports must include plain-English improvement sections, not only tables.

Use this format:

```text
### Improvement: [Page or issue]

Current problem:
[What is weak now, in simple words.]

Why it matters:
[Ranking, crawlability, trust, conversion, local, AI visibility, or revenue impact.]

Recommended change:
[Specific text, section, technical fix, schema, layout, CTA, internal link, or content action.]

Example improvement text:
[Optional draft copy, title tag, H1, meta description, FAQ, CTA, or section outline.]

Priority:
[Must Fix Now / High Impact Next / Strategic Build / Monitor]

Evidence:
[URL, crawl finding, SERP observation, GSC data, competitor example, or "not verified".]
```

This section is mandatory for the top 5 highest-priority fixes.

---

## 8. Report Visuals That Are Allowed

Use:

```text
Markdown score tables
Text progress bars
Traffic-light labels
Priority heatmaps
Keyword opportunity matrices
Competitor gap tables
Before/after text blocks
Roadmap timelines
KPI cards written as Markdown tables
```

Do not use:

```text
Fake charts with invented numbers
Decorative visuals without evidence
Traffic projections without assumptions
Keyword volumes without a source
Competitor keyword claims without source labels
```

---

## 9. Final Report Rule

A report is not complete unless it answers:

```text
What is the score?
Why is the score justified?
Which keywords are verified?
Which competitor keywords are verified vs inferred?
What exact website text/technical/content improvements should be made?
What Microsoft Clarity behavior signals are verified, over which 1–3 day window, and what should be investigated?
What data is missing?
What should be done first?
```
