# SEO Data Tools Evidence Workflow

Use this file when the user asks for authentic keywords, competitor keywords, backlink data, ranking data, trend data, or tool-backed SEO reporting.

Beyond SEO can use outputs from SEO platforms, but must not pretend access exists.

If the user asks to use Semrush, Ahrefs, DataForSEO, Moz, SERP tools, or "trending SEO tools" but no paid API/export/access is available, also load:

```text
integrations/no-paid-seo-intelligence.md
integrations/seo-tool-methodology.md
```

Use that workflow to produce legitimate no-paid evidence from live SERP samples, competitor pages, public snippets, user-provided screenshots, CSV exports, and first-party data. Never clone, scrape, or imply access to proprietary paid-tool databases without authorization.

If the user asks how these metrics work, how to imitate paid-tool workflows, or how to move from free checks to paid exports, load:

```text
integrations/seo-tool-methodology.md
```

For CSV export analysis, use:

```text
tools/source_classifier.py
templates/data-imports/
```

The classifier adds evidence level, verified metrics, missing metrics, and confidence notes. Use the CSV templates when asking a client or team member for structured exports.

---

## 1. Preferred Evidence Stack

Use the strongest available source for each data type.

```text
Own performance and behavior:
Google Search Console, Bing Webmaster Tools, GA4, Microsoft Clarity, server logs, CRM/call tracking

Keyword data:
Google Search Console, Google Ads Keyword Planner, Semrush, Ahrefs, Moz, DataForSEO, SE Ranking, Sistrix, Google Trends, AlsoAsked, AnswerThePublic, Keywords Everywhere

Competitor keywords:
Semrush Organic Research / Keyword Gap
Ahrefs Site Explorer / Organic Keywords / Content Gap
DataForSEO SERP + Labs APIs
SE Ranking competitor research
Sistrix visibility and keyword data
Manual SERP samples

Backlinks and authority:
Ahrefs, Semrush Backlink Analytics, Moz Link Explorer, Majestic, DataForSEO Backlinks API, SE Ranking backlinks

Technical crawl:
Screaming Frog, Sitebulb, Lumar, JetOctopus, Ahrefs Site Audit, Semrush Site Audit, PageSpeed Insights, Lighthouse, Chrome UX Report

Local SEO:
Google Business Profile, Google Maps/Places, BrightLocal, Whitespark, Local Falcon, Semrush Listing Management, Moz Local

AI visibility:
Google Search Console Search Generative AI reports, Bing Webmaster Tools AI Performance, Ahrefs Brand Radar where available, manual AI answer testing with date/query/location noted
```

---

## 2. Tool-Specific Use

### Semrush

Use for:

```text
Domain Overview
Organic Research
Keyword Gap
Keyword Overview
Keyword Magic Tool
Backlink Analytics
Backlink Gap
Position Tracking
Site Audit
```

Best report outputs:

```text
Competitor organic keywords
Keyword gap
Top pages
Ranking distribution
Search volume / KD / CPC where exported
Backlink gap
Site audit issues
```

### Ahrefs

Use for:

```text
Site Explorer
Organic Keywords
Top Pages
Content Gap
Keywords Explorer
Backlinks
Referring Domains
Anchors
Broken Backlinks
Rank Tracker
Site Audit
Brand visibility / AI visibility tools where available
```

Best report outputs:

```text
Competitor ranking keywords
Top pages by estimated traffic
Link gap
Anchor text risk
New/lost backlinks
Content gap opportunities
Keyword difficulty and parent topic where exported
```

### DataForSEO

Use for:

```text
SERP API
Keyword Data API
DataForSEO Labs
Backlinks API
Business Data / Google Maps data
AI Mode or AI-generated SERP fields where available
```

Best report outputs:

```text
Location-specific SERPs
SERP features
Rank tracking samples
Keyword and competitor data
Backlink/referring domain data
Local business data
```

### Moz / Majestic / SE Ranking / Sistrix

Use as supporting sources for:

```text
Authority metrics
Backlink profile checks
Keyword tracking
Visibility index
SERP/competitor gap
Local listings where supported
```

Do not treat DA, DR, AS, TF, CF, or visibility scores as Google metrics. They are third-party directional metrics.

---

## 3. Authentic Keyword Table

Every authentic keyword table must include:

```text
Keyword
Intent
Country/location
Source tool
Source date
Volume
Difficulty / competition if available
Current rank
Ranking URL
Best competitor URL
SERP feature / AI feature if visible
Action
Confidence
```

If a field is missing:

```text
Not verified
```

Never fill missing values from memory.

### No-paid fallback

When the only available evidence is public SERP and competitor page data, output:

```text
Source tool: Manual SERP sample / public competitor page review
Volume: Not verified
Difficulty: Not verified
Current rank: Verified only if seen in the live sample
Ranking URL: Verified only if seen in the live sample
Confidence: Live sample or Inferred
```

Do not place manual estimates inside Semrush, Ahrefs, Moz, or DataForSEO columns.

---

## 4. Competitor Keyword Table

Use this distinction:

```text
Verified competitor keyword:
The competitor is confirmed ranking from Semrush, Ahrefs, DataForSEO, SE Ranking, Sistrix, or a live SERP sample.

Inferred competitor target keyword:
The competitor appears to target the keyword based on title, H1, URL, headings, content, schema, or internal links, but ranking is not verified.
```

Report both, but keep them separate.

---

## 5. Data Trust Levels

Use trust labels:

```text
First-party verified:
GSC, GA4, Microsoft Clarity, GBP, Bing Webmaster Tools, CRM, server logs

Third-party verified:
Semrush/Ahrefs/Moz/DataForSEO/etc. export or API result

Live sample:
Manual SERP check or live scrape with date/location/device

Directional:
Tool metric, community actor, trend estimate, limited sample

Not verified:
No source available
```

---

## 6. Reporting Rule

If the user asks for authentic keywords or competitor keywords, the report must include:

```text
Data source used
Date collected
Country/location database
Whether volume/rank/difficulty are verified
Which terms are confirmed vs inferred
Recommended next data source if missing
```

Do not output a keyword strategy that hides the data quality.
