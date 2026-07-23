# SEO Tool Methodology Layer

Use this file when the user asks how Semrush, Ahrefs, DataForSEO, Moz, or similar SEO intelligence tools work, or asks Beyond SEO to imitate their research workflow without paid APIs.

This file teaches the workflow, not unauthorized data access.

---

## 1. Source Reality

Semrush, Ahrefs, DataForSEO, Moz, Sistrix, SE Ranking, Similarweb, and related tools are third-party market-intelligence systems.

They usually combine:

```text
Search volume sources
SERP crawling at scale
Keyword/ranking databases
Clickstream or behavior panels where available
Backlink crawlers and link indexes
CTR models by ranking position
Tool-specific authority models
Spam/risk models
Historical snapshots
Machine-learning or statistical estimation
```

They are useful for market comparison, competitor discovery, and prioritization. They are not Google Analytics, Google Search Console, or a direct view into Google's ranking system.

---

## 2. Metric Methodology

### Keyword Volume

What it means:

```text
Estimated monthly searches for a keyword in a chosen country, region, city, or search database.
```

How paid tools generally produce it:

```text
Google Ads / keyword planner style sources
Clickstream data
Historical keyword databases
SERP and keyword panel data
Seasonality and trend models
Tool-specific normalization
```

How Beyond SEO should use it:

```text
Use exact numbers only from exports/API/screenshots.
If unavailable, label as Not verified.
Use demand classes instead: High demand, Mid demand, Long-tail, Unknown.
Do not convert a demand class into a fake number.
```

Required fields:

```text
Keyword
Country/location
Source
Source date
Volume
Database/location
Confidence
```

### Keyword Difficulty

What it means:

```text
Estimated difficulty of ranking organically for a keyword, usually on a 0-100 or percentage scale.
```

Common inputs:

```text
Backlinks/referring domains to top ranking pages
Authority of ranking domains/pages
SERP strength and result type
Content relevance and intent fit in some tools
SERP features and ads in some tools
Tool-specific formulas
```

Ahrefs-style mental model:

```text
Primarily evaluate referring domains/backlinks to the top ranking pages.
KD does not fully judge content quality, intent fit, brand strength, or conversion value.
```

Semrush-style mental model:

```text
Evaluate backlink strength of top results plus broader SERP competition and keyword context.
KD is useful for triage, not a final go/no-go decision.
```

No-paid substitute:

```text
Inspect page 1 manually.
Record top domains, page types, authority signals visible from public tools, content depth, SERP features, directories/marketplaces, and brand strength.
Label difficulty as Directional: Easy / Moderate / Hard / Very hard.
```

### DR / DA / Authority Score

What they mean:

```text
Ahrefs DR: backlink profile strength on a 0-100 logarithmic scale.
Moz DA: predicted domain ranking ability, commonly 1-100, based heavily on link data and machine-learning models.
Semrush Authority Score: compound site/page quality score using link power, estimated organic traffic, and spam/natural-profile signals.
```

Rules:

```text
Do not compare DR, DA, and Authority Score as if they are the same metric.
Do not call any of them a Google ranking factor.
Use them as competitive proxy metrics.
Benchmark against direct SERP competitors, not arbitrary universal scores.
```

No-paid substitute:

```text
Use public authority checkers only if available and allowed.
Otherwise evaluate authority qualitatively:
- repeated page-1 visibility
- topical relevance
- brand/entity trust
- visible high-quality mentions
- quality of backlinks from provided data
- directories/associations/press/partners
Label exact authority as Not verified.
```

### Full Competitor Keyword Footprint

What it means:

```text
The set of keywords a competitor domain, subfolder, or URL is estimated to rank for, usually with positions, volumes, URLs, traffic estimates, and SERP features.
```

How tools generally build it:

```text
Crawl SERPs at scale across keyword databases and regions.
Store ranking domains/URLs and positions.
Join rankings to search volume and CTR models.
Estimate traffic and top pages.
Track changes over time.
```

No-paid substitute:

```text
Build a directional competitor footprint from:
- live SERP samples
- competitor sitemap and service taxonomy
- competitor page titles/H1/H2s
- URL slugs
- schema/FAQ topics
- repeated SERP appearances
- PAA/related searches
Separate confirmed ranking keywords from inferred target keywords.
```

### Traffic Estimates

What they mean:

```text
Estimated organic visits from keywords a domain/page ranks for.
```

Common formula:

```text
Estimated traffic = keyword search volume x modeled CTR at observed ranking position
```

Tool differences:

```text
Each tool has different keyword coverage, SERP refresh timing, CTR curves, search volume estimates, country databases, and feature handling. Numbers will not match across tools.
```

No-paid substitute:

```text
Do not estimate exact traffic without data.
Use opportunity sizing only:
- High opportunity: high-demand topic, strong commercial intent, weak/missing client page
- Medium opportunity: relevant topic, moderate SERP competition
- Low/long-tail opportunity: narrow query, support content, low direct revenue
```

---

## 3. Paid Tool Workflows to Imitate

### Semrush-style workflow

With export/API:

```text
Domain Overview
Organic Research positions
Organic competitors
Keyword Gap
Keyword Overview / Keyword Magic
Backlink Analytics
Backlink Gap
Site Audit
Position Tracking
```

Without export/API:

```text
Manual domain overview from crawl + SERP visibility
SERP sample keyword positions
Competitor taxonomy and page gap
Manual keyword gap
Backlink prospect categories, not confirmed backlink gap
Technical crawl from native tools
```

### Ahrefs-style workflow

With export/API:

```text
Site Explorer
Organic Keywords
Top Pages
Content Gap
Backlinks
Referring Domains
Anchors
Broken Backlinks
Rank Tracker
Site Audit
```

Without export/API:

```text
Competitor top-page inference from SERP samples
Topic/content gap from ranking pages
Public backlink/mention prospecting
Provided backlink sheet classification
Manual anchor strategy recommendations
```

### DataForSEO-style workflow

With API:

```text
SERP API by keyword/location/device
Keyword Data API
Labs API for keyword/competitor databases
Backlinks API
Google Maps / local business data
AI Mode / SERP feature fields where available
```

Without API:

```text
Manual SERP sample table
Location/device/date notes
SERP feature observations
Competitor page type analysis
PAA/related-search capture where visible
```

### Moz-style workflow

With export/API:

```text
Domain Authority
Page Authority
Spam Score
Linking domains
Inbound links
Keyword Difficulty
SERP analysis
```

Without export/API:

```text
Authority quality review from visible evidence
Spam-risk review from backlink sheets or visible patterns
Manual SERP strength review
```

---

## 4. Free to Paid Data Ladder

Use this ladder before asking for expensive access.

```text
Level 0: Website crawl, sitemap, robots, metadata, schema, internal links.
Level 1: Public SERP samples, competitor pages, PAA, related searches.
Level 2: Free public tools with limits, screenshots, browser extensions, one-off authority/keyword checks.
Level 3: User-provided CSV exports from Semrush/Ahrefs/Moz/DataForSEO/Screaming Frog/Sitebulb.
Level 4: API access or direct paid subscription exports.
Level 5: First-party analytics plus paid market intelligence: GSC, GA4, CRM, GBP, Semrush/Ahrefs/DataForSEO.
```

Always state which level was used.

---

## 5. Required Data Quality Labels

Use one label per row:

```text
First-party verified
Paid-tool verified
Screenshot verified
Live SERP sample
Public free-tool sample
Inferred from competitor page
Directional estimate
Not verified
```

If the row has a number, cite the number's source.

If the row has no source, use `Not verified`.

---

## 6. Export Request Templates

When the user or team has a paid subscription, request these exports.

### Semrush

```text
Organic Research: positions, URL, volume, KD, CPC, traffic %, SERP features, date, database.
Keyword Gap: missing, weak, strong, untapped, unique keywords.
Backlink Analytics: referring domains, backlinks, authority score, anchor, target URL, follow/nofollow, first seen, last seen.
Site Audit: issue, affected URL, severity, crawl date.
```

### Ahrefs

```text
Organic Keywords: keyword, position, previous position, volume, KD, traffic, URL, country, SERP features.
Top Pages: URL, traffic, value, keywords, top keyword, backlinks/referring domains.
Content Gap: competitor, keyword, position, volume, KD, URL.
Backlinks / Referring Domains / Anchors: source URL, target URL, DR, traffic, anchor, link type, first seen, last check.
```

### DataForSEO

```text
SERP: keyword, location, language, device, datetime, rank group, rank absolute, URL, domain, title, description, SERP features.
Labs/Keyword: keyword, location, volume, competition, CPC, trends, related keywords, ranked domains/pages.
Backlinks: referring domain, source URL, target URL, anchor, link attributes, rank/authority fields, first seen, last seen.
```

### Moz

```text
Link metrics: DA, PA, Spam Score, linking domains, inbound links, top pages, anchors.
Keyword metrics: keyword, volume/range if available, difficulty, priority/opportunity, SERP analysis.
```

---

## 7. Output Rule

Whenever this methodology is used, include:

```text
Tool workflow imitated or used
Data level used
Metrics verified
Metrics not verified
Confidence labels
Next export/API needed to upgrade the report
```

This prevents Beyond SEO from sounding like it has paid data when it only has public evidence.
