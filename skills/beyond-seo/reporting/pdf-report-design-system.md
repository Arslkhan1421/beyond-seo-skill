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
Verified: crawl, sitemap, robots, metadata
Sampled: live SERP checks
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
