# No-Paid SEO Intelligence Workflow

Use this file when the user wants Semrush, Ahrefs, DataForSEO, SERP, keyword, competitor, backlink, or rank-style insight but paid APIs, subscriptions, or exports are not available.

The goal is to reproduce the thinking workflow of professional SEO tools using legitimate available evidence, not to fake proprietary metrics.

---

## 1. Hard Boundary

Do not:

```text
Bypass paywalls or login walls
Scrape paid dashboards without explicit user access
Invent Semrush/Ahrefs/DataForSEO/Moz metrics
Claim exact volume, KD, DR, DA, AS, backlinks, traffic, or rank history without a source
Present manual samples as full market coverage
```

Do:

```text
Use public SERPs, website crawls, competitor pages, public snippets, user-provided screenshots, CSV exports, and available first-party data.
Label data quality on every keyword and competitor table.
Separate confirmed ranking evidence from inferred targeting evidence.
Recommend the exact paid-tool export needed when a metric cannot be verified.
```

---

## 2. What Can Be Done Without Paid APIs

### DataForSEO-style SERP sampling

Use live search/browser tools where available.

Collect:

```text
Keyword
Search engine
Country/city if known
Device assumption
Date
Top ranking URLs/domains from the sample
SERP features visible in the sample
People Also Ask / related searches when visible
Page type ranking: service, blog, directory, marketplace, local pack, video, review site
Mative/client URL present: yes/no
Confidence: Live sample
```

Output warning:

```text
This is a live/manual SERP sample, not a full rank-tracking dataset.
```

### Semrush-style keyword gap without Semrush

Build a directional keyword gap from:

```text
Competitor title tags
Competitor H1/H2s
Competitor URL slugs
Competitor schema
Navigation and service taxonomy
Repeated SERP competitors
PAA questions
Related searches
Client sitemap and missing page types
```

Classify each keyword as:

```text
Confirmed competitor ranking keyword: seen in live SERP sample or provided export.
Inferred competitor target keyword: visible in competitor page title/H1/URL/content, but rank not verified.
Missing money page: relevant high-intent topic with no strong client page.
Support cluster opportunity: informational topic that supports a money page.
```

### Ahrefs-style backlink thinking without Ahrefs

Without backlink exports, do not claim full backlink profile.

Use:

```text
Public brand mention searches
Competitor "brand" -site:competitor.com searches
Visible partner/vendor/client links
Industry directories and association pages
Local citation opportunities
Press/news mentions
User-provided backlink sheets
```

Score prospects by:

```text
Topical relevance
Local/country relevance
Editorial quality
Indexability
Outbound link risk
Anchor safety
Business relationship fit
```

Label as:

```text
Backlink prospect, not verified backlink gap
```

### Keyword volume approximation

Do not invent exact numbers.

Allowed labels:

```text
Likely high demand: repeated competitors, commercial SERP, ads/directories visible, broad service category
Likely mid demand: niche commercial term, several relevant competitors, some SERP depth
Likely long-tail: specific service/question/location phrase
Not verified: exact volume requires Google Keyword Planner, Semrush, Ahrefs, DataForSEO, or another export
```

---

## 3. No-Paid Evidence Collection Sequence

When doing keyword or competitor research without paid APIs:

```text
1. Crawl the client sitemap and key pages.
2. Build the current page/topic inventory.
3. Search 5-15 money keywords manually or with native search tools.
4. Record repeated ranking competitors and ranking page types.
5. Open the strongest competitor pages.
6. Extract competitor title, meta description, H1, H2 themes, FAQ topics, schema, content sections, trust proof, CTA, and internal links.
7. Build keyword groups from SERP evidence and competitor page evidence.
8. Mark every row as Confirmed, Live sample, Inferred, Directional, or Not verified.
9. Recommend pages, content upgrades, internal links, schema, backlinks, and tracking.
```

For local SEO, add:

```text
city/service queries
near me queries
map pack visibility if visible
public GBP listing observations
review count/rating only if visible
local directories and citations
```

---

## 4. Required Tables

### Manual SERP Sample Table

```text
Keyword
Location
Date
Top visible competitors
SERP page types
SERP features
Client visible?
Opportunity
Confidence
```

### No-Paid Keyword Gap Table

```text
Keyword theme
Evidence source
Confirmed or inferred
Best competitor example
Client current page
Recommended page/action
Volume/KD status
Priority
```

### No-Paid Competitor Page Gap Table

```text
Competitor URL
Target topic
Why it ranks/targets
Content depth signals
Trust/proof signals
Schema/FAQ signals
Client gap
Recommended improvement
```

### Backlink Prospect Table

```text
Prospect/source
Type
Why relevant
Target page
Suggested anchor type
Risk
Status: prospect only / confirmed if provided
```

---

## 5. Report Language

Use this phrasing:

```text
No paid API/export was available, so this section uses live SERP samples and competitor page evidence. Exact volume, keyword difficulty, rank history, traffic, backlinks, DR/DA/AS, and full competitor keyword footprints are not verified.
```

When a user asks to "take help from Semrush and Ahrefs" without paid access, say:

```text
I can use the Semrush/Ahrefs-style research method without paid APIs: competitor keyword gap, top page review, backlink prospecting, and SERP analysis. I cannot claim their proprietary metrics unless you provide exports, screenshots, or access.
```

---

## 6. Upgrade Path When Exports Arrive

If the user later provides Semrush/Ahrefs/DataForSEO/GSC/GA4 files:

```text
1. Replace directional keyword rows with verified rows.
2. Add exact source, export date, database/location, volume, difficulty, current rank, ranking URL, and competitor URL.
3. Re-score priorities using verified data.
4. Keep manual SERP insights only as qualitative context.
5. Update the report's data quality section.
```

Do not mix unverified manual assumptions into verified tool columns.
