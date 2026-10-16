# Integrations

Use the contents below to select the relevant workflow; load only the needed sections.


## ahrefs-semrush-moz-style-checks

# Ahrefs, Semrush, and Moz Style Checks

How to use authority and backlink data from SEO tools or Apify-style community actors.

---

## Use Cases

Check DR/DA/Authority Score, referring domains, backlink quality, organic keywords, traffic estimates, anchors, top pages, and competitor gaps.

## Data Confidence

Official exports are stronger. Scraped/community actor outputs are directional.

## Output

Always explain authority gap, link relevance, anchor risk, and next backlink actions.


## apify-actor-registry

# Apify Actor Registry for Beyond SEO

This file defines which categories of Apify actors Beyond SEO should look for and how to use them.

Actor availability, pricing, and quality can change. Therefore, this registry uses categories and preferred examples rather than treating any single actor as permanent truth.

---

## 1. Registry Philosophy

Do not hardcode one actor forever.

For each SEO job, the agent should:

```text
1. Identify needed data.
2. Choose the best actor category.
3. Prefer official/maintained actors when available.
4. Check actor rating, users, last modified date, pricing, and output examples.
5. Use community actors carefully.
6. Label low-confidence outputs as directional.
```

---

## 2. Actor Quality Checklist

Before using an actor, check:

```text
Actor name
Actor ID
Developer/maintainer
Rating
Number of users
Last modified date
Pricing model
Input schema clarity
Output schema clarity
Reviews/issues
Whether it supports API/MCP
Whether it exports JSON/CSV/Excel
Whether it has enough fields for SEO use
```

### Actor Confidence Levels

```text
High: maintained by Apify or reputable developer, strong usage, clear output, recent updates.
Medium: community actor with decent rating/usage and clear output.
Low: few users, unclear output, no recent updates, poor reviews, or unverifiable claims.
```

---

## 3. Primary Actor Categories

### 3.1 Website Crawling

Purpose:

```text
Own-site crawl
Competitor crawl
Content extraction
Page inventory
AEO/GEO content extraction
RAG/LLM-ready Markdown output
```

Preferred actor examples:

```text
apify/website-content-crawler
apify/web-scraper
custom Crawlee actor
```

Use for:

```text
URL discovery
Markdown/text extraction
HTML cleanup
JS-rendered page crawling
Sitemap crawling
File download if needed
Competitor page analysis
```

Standard output fields needed:

```text
url
title
description/meta
h1
h2_list
text/markdown
links
canonical
schema snippets if available
files
```

Caution:

```text
Website Content Crawler is excellent for content extraction, but may not provide every technical SEO field by default. For technical audits, combine with raw HTML extraction, custom Web Scraper logic, or native tools.
```

---

### 3.2 SERP Scraping

Purpose:

```text
Keyword ranking checks
Competitor discovery
SERP intent analysis
People Also Ask extraction
Related queries
AI Overview / AI Mode visibility where supported
Ads and SERP feature checks
```

Preferred actor examples:

```text
apify/google-search-scraper
other high-quality Google SERP scraper actors
Bing SERP actors where needed
```

Use for:

```text
Top 10/20/30 organic results
Local keyword checks
Country/language/device SERPs
PAA questions
Related searches
AI-search visibility checks where actor supports it
```

Standard output fields needed:

```text
query
country
language
location/city
device
rank
url
domain
title
snippet
serp_feature
paa_questions
related_queries
ai_overview_presence
ai_cited_sources
ads
```

Caution:

```text
SERP results vary by location, device, personalization, and time. Always record query, country, city/geolocation, language, device, and date.
```

---

### 3.3 Google Trends / Topic Demand

Purpose:

```text
Validate topic demand
Find rising queries
Compare keyword interest
Identify seasonality
Find regional interest
Support content calendar planning
```

Preferred actor examples:

```text
apify/google-trends-scraper
high-quality Google Trends community actors
```

Use for:

```text
Interest over time
Interest by country/city/subregion
Rising queries
Top related queries
Related topics
Topic comparison
```

Standard output fields needed:

```text
keyword/topic
time_range
region
interest_over_time
interest_by_region
rising_queries
top_queries
related_topics
```

Caution:

```text
Google Trends is relative interest, not exact search volume. Do not present it as keyword volume.
```

---

### 3.4 Google Maps / Local SEO

Purpose:

```text
Local competitor discovery
Map pack competitor analysis
Google Business Profile comparison
Review/rating analysis
Local category comparison
Service area discovery
```

Actor examples to look for:

```text
Google Maps Scraper actors
Google Places Scraper actors
Google Reviews Scraper actors
Competitive intelligence actors using Google Maps data
```

Use for:

```text
Business names
Categories
Ratings
Review counts
Address
Phone
Website
Hours
Services
Photos
Review text snippets
Map position where available
```

Standard output fields needed:

```text
query
city
business_name
category
rating
review_count
address
phone
website
hours
map_position
review_snippets
profile_url
```

Caution:

```text
Do not scrape or store unnecessary personal data. For SEO, business-level data and review themes are usually enough.
```

---

### 3.5 Authority / Backlink / SEO Metrics

Purpose:

```text
Directional domain authority checks
Backlink profile review
Competitor authority gap
Traffic estimate
Organic keyword footprint estimate
```

Actor categories to look for:

```text
Ahrefs-style scraper
Semrush-style scraper
Moz DA checker
Similarweb-style traffic checker
Ubersuggest-style scraper
Domain authority checker
Backlink checker
```

Use for:

```text
DR/DA/Authority Score
Referring domains
Backlinks
Dofollow/nofollow ratio
Top pages
Organic keywords
Organic traffic estimate
Anchors
Competitor comparison
```

Critical caution:

```text
Most Ahrefs/Semrush/Moz-style Apify actors are community-maintained or scrape public/limited data. Treat as directional unless the user provides an official export or authenticated official source.
```

Never write:

```text
Ahrefs confirms...
```

unless it truly came from Ahrefs export/access.

Write:

```text
Directional authority check suggests...
```

---

### 3.6 Social and Brand Authority

Purpose:

```text
Competitor content analysis
Brand demand signals
Social proof scan
Topic/format discovery
Content velocity comparison
```

Actor categories to look for:

```text
Instagram scraper
Facebook pages/posts scraper
Facebook reviews scraper
YouTube scraper
TikTok scraper
LinkedIn public data actors where allowed
Reddit scraper where relevant
```

Use for:

```text
Post topics
Engagement
Content frequency
Follower count
Video topics
Review themes
Competitor campaigns
Brand mentions
```

Caution:

```text
Social scraping must respect platform rules and privacy. Use public business/content data only.
```

---

### 3.7 Lead / Contact Enrichment

Purpose:

```text
SEO outreach prospecting
Local citation prospecting
Partnership link building
Digital PR prospecting
```

Actor categories to look for:

```text
Business leads enrichment
Google Maps lead extraction
Company website contact extraction
Social profile enrichment
```

Use for:

```text
Prospect name
Business URL
Email if legally and ethically appropriate
Phone
Category
Location
Website
Social profile
```

Caution:

```text
Follow email/privacy laws. Do not scrape personal data unnecessarily. Do not spam.
```

---

## 4. Preferred SEO Actor Stack

For most Beyond SEO audits, use this order:

```text
1. Website crawler
2. Google SERP scraper
3. Google Trends scraper
4. Google Maps/local actor if local business
5. Authority/backlink actor if needed
6. Social/content actor if brand/content strategy matters
```

---

## 5. Actor Selection by Task

### Website Technical + Content Audit

Use:

```text
Website Content Crawler
Web Scraper
Custom Crawlee actor
Native browser/source inspection
```

### Keyword Ranking Snapshot

Use:

```text
Google Search Results Scraper
GSC export if available
Rank tracking export if available
```

### Competitor Discovery

Use:

```text
Google SERP scraper
Google Maps scraper for local
Competitive Intelligence actors
Native search
```

### AEO/GEO Visibility

Use:

```text
Google Search scraper with AI Overview/AI Mode fields where supported
AI-search add-ons where available
Perplexity/ChatGPT/Copilot/Gemini search actors where available
Native AI-search testing if available
```

### Local SEO

Use:

```text
Google Maps scraper
Google Reviews scraper
Competitive intelligence actor using maps data
GBP export if available
```

### Backlink/Authority

Use:

```text
Ahrefs-style actor
Semrush-style actor
Moz DA actor
Similarweb-style actor
Official exports when available
```

### Content Calendar / Trends

Use:

```text
Google Trends scraper
SERP scraper
Social scrapers
Competitor blogs crawl
```

### Free/Paid Backlink Prospecting

Use:

```text
SERP scraper with queries like "write for us" + niche
Google Maps for local associations/business directories
Web scraper for prospect pages
Authority-style actor for prospect evaluation
```

---

## 6. Actor Discovery Queries

When the host agent can search Apify Store, use queries like:

```text
website crawler
website content crawler
google search scraper
serp scraper
google trends scraper
google maps scraper
google reviews scraper
ahrefs scraper
semrush scraper
moz domain authority
similarweb scraper
backlink checker
instagram scraper
facebook pages scraper
youtube scraper
tiktok scraper
competitive intelligence agent
```

---

## 7. Actor Approval Rules

Approve actor use if:

```text
The actor directly supports the task.
Output fields match the needed SEO fields.
Cost is reasonable for the task.
It has acceptable reliability.
The task is compliant and public-data based.
```

Reject or avoid actor if:

```text
It promises unrealistic data.
It has unclear output.
It is too expensive for the current question.
It has poor reviews/issues.
It collects unnecessary personal data.
It requires credentials the user does not have.
It violates task boundaries.
```

---

## 8. Actor Result Documentation

Every Apify-based report should include:

```text
Actor/category used
Purpose
Input scope
Date/time if available
Confidence label
Limitations
```

Example:

```text
Data Source: Google SERP scraper
Purpose: Local keyword SERP analysis
Input: 12 keywords, country US, location Arlington Heights, desktop
Confidence: Confirmed for sampled SERPs, not a full rank-tracking history
```

---

## 9. Actor Output to SEO Action Mapping

### If SERP shows competitors dominate with service pages

Action:

```text
Create or improve dedicated service landing pages.
```

### If PAA questions repeat cost/risk/process intent

Action:

```text
Add answer blocks, FAQs, cost sections, risk/process sections.
```

### If Trends shows rising query

Action:

```text
Prioritize content/page creation earlier in roadmap.
```

### If Maps shows competitors have more reviews

Action:

```text
Build review velocity and GBP content strategy.
```

### If authority actors show low referring domains

Action:

```text
Build niche/local/PR backlink plan, verify with official export if budget depends on it.
```

### If social scrapers show competitor content themes

Action:

```text
Create SEO-supporting content cluster and social proof loop.
```

---

## 10. Registry Maintenance

Because actors change, this registry should be reviewed regularly.

Update when:

```text
A better official actor appears.
Actor pricing changes significantly.
Actor output schema changes.
An actor becomes unreliable.
A new AI-search/AEO actor becomes available.
A better local SEO/maps actor appears.
```

---

## 11. Bottom Line

The registry exists to prevent tool chaos.

Beyond SEO should not ask, “Which random actor should I run?”

It should ask:

```text
What SEO question am I answering?
What data do I need?
Which actor category provides it?
How reliable is that actor?
How should I label the output?
What action does the data support?
```


## apify-actor-shortlist.local

# Apify Actor Shortlist

Generated from Apify Store checks on 2026-05-26. Actor availability, quality, and pricing can change, so re-check before large runs.

Do not store API tokens in this file.

## Recommended Starting Actors

| Workflow | Preferred Actor | Actor ID | Maintainer | Confidence | Notes |
|---|---|---|---|---|---|
| Website/content crawl | `apify/website-content-crawler` | `aYG0l9s7dbB7j3gbS` | Apify | High | Best first choice for page inventory and content extraction. |
| Custom crawl/scrape | `apify/web-scraper` | `moJRLRc85AitArpNN` | Apify | High | Use when custom extraction or JS rendering is needed. |
| Google SERP sample | `apify/google-search-scraper` | `nFJndFXA5zjCTuudP` | Apify | High | Use for keyword SERP snapshots, competitor discovery, PAA/related result checks where available. |
| Google Trends | `apify/google-trends-scraper` | `DyNQEYDj9awfGQf9A` | Apify | Medium | Useful for directional demand and seasonality; validate important decisions with other data. |
| Google Maps/local | `compass/crawler-google-places` | `nwua9Gu5YrADL7ZDj` | Compass | High | Strong local SEO starting point for map pack and local competitor discovery. |
| Google reviews | `compass/Google-Maps-Reviews-Scraper` | `Xb8osYTtOjlsgI6k9` | Compass | High | Use for review pattern analysis when local SEO requires it. |
| PageSpeed/Core Web Vitals via Apify | `alizarin_refrigerator-owner/pagespeed-insights` | `wEonoqiLlBBugf5Xk` | Community | Medium | Use through Apify first. Treat as confirmed when raw URL/device/timestamp metrics are returned; otherwise directional. |
| GSC via Apify | Search Apify Store per project | varies | varies | Medium-High | Prefer authenticated GSC connector/export actors when available. Confirm query/page/click/impression data only when actor uses owned-account auth or uploaded export. |
| GA4 via Apify | Search Apify Store per project | varies | varies | Medium-High | Prefer authenticated GA4 connector/export actors when available. Confirm traffic/conversion data only when actor uses owned-account auth or uploaded export. |
| Ahrefs/Semrush/Moz via Apify | Search Apify Store per project | varies | varies | Medium | Use Apify actors where available. Treat as confirmed only if the actor connects to an owned paid account/export; public/free-tool scrapes stay directional. |
| Backlink/authority style checks | Community SEO/backlink actors | varies | Community | Low-Medium | Use through Apify when no export/account actor exists, but label authority/backlink metrics as directional. |

## Credit-Safe Default Sequence

1. Crawl homepage and sitemap first.
2. Limit first crawl to 50 pages.
3. Run only 5-10 SERP queries for the initial keyword sample.
4. Crawl 3-5 competitors after SERP discovery.
5. Use GSC/GA4 actors or Apify-hosted exports when first-party performance data is needed.
6. Use Maps/reviews only for local SEO projects.
7. Use authority/backlink actors after checking whether Apify has authenticated Ahrefs/Semrush/Moz workflows for the project.


## apify-actor-shortlist

# Apify Actor Shortlist

Generated from Apify Store checks on 2026-05-26. Actor availability, quality, and pricing can change, so re-check before large runs.

Do not store API tokens in this file.

## Recommended Starting Actors

| Workflow | Preferred Actor | Actor ID | Maintainer | Confidence | Notes |
|---|---|---|---|---|---|
| Website/content crawl | `apify/website-content-crawler` | `aYG0l9s7dbB7j3gbS` | Apify | High | Best first choice for page inventory and content extraction. |
| Custom crawl/scrape | `apify/web-scraper` | `moJRLRc85AitArpNN` | Apify | High | Use when custom extraction or JS rendering is needed. |
| Google SERP sample | `apify/google-search-scraper` | `nFJndFXA5zjCTuudP` | Apify | High | Use for keyword SERP snapshots, competitor discovery, PAA/related result checks where available. |
| Google Trends | `apify/google-trends-scraper` | `DyNQEYDj9awfGQf9A` | Apify | Medium | Useful for directional demand and seasonality; validate important decisions with other data. |
| Google Maps/local | `compass/crawler-google-places` | `nwua9Gu5YrADL7ZDj` | Compass | High | Strong local SEO starting point for map pack and local competitor discovery. |
| Google reviews | `compass/Google-Maps-Reviews-Scraper` | `Xb8osYTtOjlsgI6k9` | Compass | High | Use for review pattern analysis when local SEO requires it. |
| PageSpeed/Core Web Vitals via Apify | `alizarin_refrigerator-owner/pagespeed-insights` | `wEonoqiLlBBugf5Xk` | Community | Medium | Use through Apify first. Treat as confirmed when raw URL/device/timestamp metrics are returned; otherwise directional. |
| GSC via Apify | Search Apify Store per project | varies | varies | Medium-High | Prefer authenticated GSC connector/export actors when available. Confirm query/page/click/impression data only when actor uses owned-account auth or uploaded export. |
| GA4 via Apify | Search Apify Store per project | varies | varies | Medium-High | Prefer authenticated GA4 connector/export actors when available. Confirm traffic/conversion data only when actor uses owned-account auth or uploaded export. |
| Ahrefs/Semrush/Moz via Apify | Search Apify Store per project | varies | varies | Medium | Use Apify actors where available. Treat as confirmed only if the actor connects to an owned paid account/export; public/free-tool scrapes stay directional. |
| Backlink/authority style checks | Community SEO/backlink actors | varies | Community | Low-Medium | Use through Apify when no export/account actor exists, but label authority/backlink metrics as directional. |

## Credit-Safe Default Sequence

1. Crawl homepage and sitemap first.
2. Limit first crawl to 50 pages.
3. Run only 5-10 SERP queries for the initial keyword sample.
4. Crawl 3-5 competitors after SERP discovery.
5. Use GSC/GA4 actors or Apify-hosted exports when first-party performance data is needed.
6. Use Maps/reviews only for local SEO projects.
7. Use authority/backlink actors after checking whether Apify has authenticated Ahrefs/Semrush/Moz workflows for the project.


## apify-ai-friendly-seo-workflows

# Apify AI-Friendly SEO Workflows

This file adds AI-friendly SEO workflows to the Apify-first Beyond SEO system.

Use this whenever a user asks for AI-friendly SEO, AEO, GEO, Entity SEO, Reputation SEO, or Conversation SEO.

---

## 1. Actor Categories to Use

Search Apify Store or use known actors for:

```text
Website content crawl
Custom web scrape
Google SERP
Google Trends
Google Maps / Places
Google reviews
PageSpeed / Lighthouse
Social profile scraping
YouTube scraping
News / article scraping
Backlink / authority checks
AI Overview / AI Mode checks where supported
Perplexity / answer engine checks where supported
GSC / GA4 connector or export actors where available
```

---

## 2. Credit-Safe AI-Friendly SEO Sequence

```text
1. Crawl own website: homepage + sitemap, max 50 pages.
2. Extract entity data from own site.
3. Run 5-10 SERP queries around money keywords.
4. Extract People Also Ask and related questions.
5. Crawl 3-5 competitors.
6. Check Google Maps/reviews if local.
7. Check social/reputation profiles.
8. Check PageSpeed/Lighthouse on homepage + money pages.
9. Check authority/backlink actors after page strategy is known.
10. Check AI Overview / answer engine visibility where supported.
```

---

## 3. Data to Extract

### AEO

```text
Questions
PAA
Related searches
FAQ sections
Answer snippets
Content gaps
```

### GEO

```text
Cited sources
Mentioned brands
Competitor cited pages
Authority pages
Media mentions
Balanced comparison content
```

### Entity SEO

```text
Brand name
Person name
Alternate names
Profiles
sameAs links
Reviews
Media
Certifications
Schema
```

### Reputation SEO

```text
Review platforms
Review count/rating
Review themes
Trustpilot/Google/LinkedIn proof
Media articles
Third-party authority pages
```

### Conversation SEO

```text
Human questions
Objections
Cost concerns
Trust concerns
Comparison questions
Action questions
```

---

## 4. Output

Apify findings should feed into:

```text
AI-friendly SEO report
Page creation plan
Answer block plan
Entity page plan
Reputation proof plan
Third-party authority article plan
Schema plan
90-day roadmap
```

---

## 5. Confidence Labels

```text
Confirmed: crawl/SERP/review data directly extracted.
Directional: community authority/backlink/AI visibility estimates.
Not verified: actor unavailable or data not collected.
```

## Research Anchors

Use these public guidance anchors when explaining or auditing AI-friendly SEO:

- Google Search Central: AI features and your website — https://developers.google.com/search/docs/appearance/ai-features
- Google Search Central: Google Search generative AI optimization guide — https://developers.google.com/search/docs/fundamentals/ai-optimization-guide
- Google Search Central: Creating helpful, reliable, people-first content — https://developers.google.com/search/docs/fundamentals/creating-helpful-content
- Google Search Central: Organization structured data — https://developers.google.com/search/docs/appearance/structured-data/organization
- Google Search Central: ProfilePage structured data — https://developers.google.com/search/docs/appearance/structured-data/profile-page
- Google Search Central: Review snippet structured data — https://developers.google.com/search/docs/appearance/structured-data/review-snippet
- Bing Webmaster Tools: AI Performance — https://www.bing.com/webmasters/help/ai-performance-9f8e7d6c
- Bing Webmaster Blog: AI Performance announcement — https://blogs.bing.com/webmaster/February-2026/Introducing-AI-Performance-in-Bing-Webmaster-Tools-Public-Preview
- Perplexity Hub — https://www.perplexity.ai/hub


## apify-first-operating-policy

# Apify-First Operating Policy

Beyond SEO is now Apify-first.

The skill should not ask the user for a long list of APIs during normal onboarding. The default required input is:

```text
APIFY_API_TOKEN
```

Everything else should be handled through Apify actors, Apify MCP, Apify datasets, uploaded exports, or the agent's native tools when required.

---

## 1. Install-Time / First-Run Behavior

When Beyond SEO starts inside an agent, it should check:

```text
APIFY_API_TOKEN
Apify MCP/tool availability
Existing Apify dataset/export files
```

If Apify is not configured, ask once:

```text
Please provide or configure APIFY_API_TOKEN. With Apify I can run crawl, SERP, competitor, maps/local, trends, PageSpeed/Lighthouse, backlink/authority, and connector/export workflows from one data layer.
```

Do not ask for GSC, GA4, PageSpeed API, Ahrefs, Semrush, Moz, Firecrawl, DataForSEO, or other APIs in the first message.

---

## 2. What Apify Should Cover First

Use Apify first for:

```text
Website crawl
Competitor crawl
Google SERP
People Also Ask / related queries
AI Overview / AI Mode checks where supported
Google Trends
Google Maps / Places
Google reviews
PageSpeed or Lighthouse actors
GSC connector/export actors where available
GA4 connector/export actors where available
Ahrefs/Semrush/Moz-style actors where available
Backlink/authority actors
Social/content scraping
Scheduled monitoring
```

If a task requires authenticated first-party data, the agent should look for an Apify actor or Apify-hosted export workflow first.

---

## 3. Data Confidence

Use:

```text
Confirmed
Directional
Directional
Not verified
```

Confirmed:

```text
Actor directly extracts public crawl/SERP data.
Actor returns raw URL/device/timestamp PageSpeed/Lighthouse metrics.
Actor connects to authenticated first-party account or user-provided export.
```

Directional:

```text
Community actor estimates DR/DA/traffic/backlinks.
Actor scrapes public/free-tool surfaces.
Actor method is unclear.
```

---

## 4. Minimal User Questions

The normal audit start should ask only:

```text
1. Website URL
2. Target country/city if local
3. Main goal
4. APIFY_API_TOKEN if not configured
```

Everything else is optional and should be asked later only if Apify cannot fetch it or if private authentication is required.

---

## 5. Cost-Safe Default Run

Default Apify run order:

```text
1. Website crawl: homepage + sitemap, max 50 URLs.
2. SERP sample: 5-10 priority queries.
3. Competitor discovery from SERP.
4. Competitor crawl: 3-5 competitors, limited pages.
5. Local Maps/reviews only if local project.
6. Trends only if topic prioritization is needed.
7. PageSpeed/Lighthouse for homepage + 3-5 money pages.
8. Authority/backlink actors after page/keyword strategy is known.
```

Do not burn credits by crawling huge sites or running hundreds of keywords without approval.

---

## 6. Secret Handling

Never write API tokens into:

```text
SKILL.md
README.md
_meta.json
MANIFEST.json
Actor shortlist files
Reports
Logs
Templates
```

Only read tokens from environment variables, secure agent secrets, or runtime secret stores.

---

## 7. Fallback

If Apify is not available, Beyond SEO can still work using native browsing, scraping, uploaded files, or advisory mode — but it should clearly say the audit is limited.

The preferred path remains Apify.


## apify-workflows

# Apify Workflows for Beyond SEO

This file defines practical Apify workflows for SEO, AEO/GEO, local SEO, competitor research, backlinks, and reporting.

The goal is not to run actors blindly. The goal is to collect exactly the data needed to make better SEO decisions.

---

## 1. Workflow Rules

Before running Apify:

```text
1. Define the business goal.
2. Define the SEO question.
3. Choose the smallest useful data pull.
4. Select actor/category.
5. Run test input first.
6. Inspect output quality.
7. Expand only if useful.
8. Normalize results.
9. Convert findings into actions.
```

Bad:

```text
Run every actor and see what happens.
```

Good:

```text
Run a 20-page crawl and 10-keyword SERP sample to identify page and competitor patterns.
```

---

## 2. Workflow A: First-Pass Website Crawl

### Use When

```text
User provides a website URL.
Need technical/content/on-page overview.
No crawl export exists.
Apify token is available.
```

### Actor Category

```text
Website crawler
Website content crawler
Web scraper
Custom Crawlee actor
```

### Input

```text
start_url: website homepage
include_sitemap: true if supported
max_pages: 50-200 for first pass
same_domain_only: true
exclude_patterns:
  - /wp-admin/
  - /cart/
  - /checkout/
  - /login/
  - /account/
  - ?replytocom=
  - tracking/query parameters
render_js: true only if needed
```

### Extract

```text
URL
status/final URL if available
title
meta description
H1
H2s
body text/Markdown
word count
links
canonical
schema snippets if available
page type
```

### Analyze

```text
Missing/duplicate titles
Missing/duplicate meta descriptions
Missing/multiple H1s
Thin pages
Empty JS-rendered pages
Orphan-like pages
Weak CTAs
Missing schema
Weak internal links
Service pages vs blog/support pages
```

### Output

```text
Page inventory
Issue summary
Priority technical/content fixes
Pages to improve first
Need for deeper crawl if required
```

---

## 3. Workflow B: JavaScript Rendering Check

### Use When

```text
Site appears modern React/Next/Lovable/SPA.
Crawl output has little body text.
Important pages show empty HTML or missing H1/H2.
```

### Actor Category

```text
Website crawler with headless browser
Web scraper with JS rendering
Native browser/source inspection
```

### Test

Compare:

```text
Raw HTML content
Rendered page content
Crawl-extracted Markdown/text
Visible browser content
```

### Red Flags

```text
No server-rendered H1/H2
Meta tags missing in source
Content only appears after JS
Course/product/service pages not crawlable
Canonical missing on dynamic routes
Duplicate title/meta across routes
```

### Output

```text
Rendering risk:
Critical / High / Medium / Low

Required fix:
SSR / pre-rendering / dynamic metadata / schema injection / static landing pages
```

---

## 4. Workflow C: SERP and Keyword Sample

### Use When

```text
Need keyword opportunities.
Need competitor discovery.
Need ranking snapshot.
Need SERP intent analysis.
```

### Actor Category

```text
Google SERP scraper
```

### Input

```text
queries:
  - 5 existing money keywords
  - 5 missing money keywords
  - 5 competitor-owned keywords
country
city/location/geocode if local
language
device: desktop/mobile if supported
max_pages_per_query: 1-3
```

### Extract

```text
Organic top 10/20/30
Titles
URLs
Domains
Snippets
PAA questions
Related queries
Ads
Local pack presence
AI Overview/AI Mode presence if available
```

### Analyze

```text
Who ranks repeatedly?
What page types rank?
Are directories dominating?
Are competitors using dedicated service pages?
Are pages local pages, category pages, blogs, homepages, or GBP-heavy results?
Are PAA questions cost/risk/process/comparison focused?
Are AI answers citing competitor or authority sources?
```

### Output

```text
Keyword-to-page map
Competitor list
SERP intent summary
PAA/AEO questions
Page creation/improvement priorities
```

---

## 5. Workflow D: Competitor Crawl

### Use When

```text
SERPs reveal top competitors.
User provides competitors.
Need content/service-page gap.
```

### Actor Category

```text
Website crawler
Website content crawler
Web scraper
```

### Input

```text
competitor_domains: 3-10
max_pages_per_domain: 50-150
include_sitemap: true
focus_patterns:
  - /services/
  - /service/
  - /treatments/
  - /courses/
  - /blog/
  - /resources/
  - location/city pages
```

### Extract

```text
Top service/product/course pages
Title/H1/H2
Content depth
FAQ sections
Schema
CTA patterns
Trust proof
Internal links
Blog/support clusters
Location pages
```

### Analyze

```text
Pages competitors have that client lacks
Service pages with stronger depth
Keyword clusters competitors cover
FAQ/PAA coverage
Schema usage
Conversion paths
Internal linking patterns
Local proof
Content freshness
```

### Output

```text
Competitor matrix
Missing page list
Service-page gap
Content gap
Internal linking recommendations
90-day build priority
```

---

## 6. Workflow E: Local SEO / Maps Scan

### Use When

```text
Business serves a local city/region.
User wants calls, appointments, map pack, or local queries.
```

### Actor Category

```text
Google Maps scraper
Google Places scraper
Google Reviews scraper
Competitive intelligence actor with Maps data
```

### Input

```text
queries:
  - main service + city
  - near me intent if useful
  - emergency/service-specific terms
location/city
radius if supported
max_results: 10-30 per query
```

### Extract

```text
Business name
Category
Rating
Review count
Address
Phone
Website
Hours
Services
Profile URL
Review snippets/themes if available
Map position if supported
```

### Analyze

```text
Who dominates map results?
What categories are competitors using?
How many reviews do winners have?
What review keywords appear?
Is client category/service coverage weak?
Does client need review velocity?
Does client need local landing pages?
Does client need citation cleanup?
```

### Output

```text
Map competitor summary
GBP optimization checklist
Review strategy
Local page plan
Citation/local backlink plan
```

---

## 7. Workflow F: Trends and Content Demand

### Use When

```text
Need content calendar.
Need topic prioritization.
Need seasonal/regional demand check.
Need to compare multiple service/course topics.
```

### Actor Category

```text
Google Trends scraper
```

### Input

```text
terms:
  - target service/course/product keywords
region
time_range: 12 months / 5 years / 90 days
category if relevant
```

### Extract

```text
Interest over time
Interest by region/city
Rising queries
Top queries
Related topics
```

### Analyze

```text
Which topic has rising demand?
Which city/region shows strongest demand?
Is this seasonal?
Which related queries should become support articles?
Which topics are low-volume but high-conversion?
```

### Output

```text
Topic priority
Content calendar input
Regional targeting
Support article ideas
Warnings where Trends is not enough
```

Important:

```text
Trends is relative interest, not exact keyword volume.
```

---

## 8. Workflow G: Authority / Backlink Directional Scan

### Use When

```text
Need backlink gap.
Need authority comparison.
User does not have official Ahrefs/Semrush/Moz export.
Apify community actor exists.
```

### Actor Category

```text
Ahrefs-style scraper
Semrush-style scraper
Moz DA checker
Similarweb-style checker
Backlink checker
```

### Input

```text
client_domain
competitor_domains: 3-10
```

### Extract

```text
Authority score/DR/DA if available
Referring domains
Backlinks
Organic keywords
Traffic estimate
Top pages
Anchor examples if available
```

### Analyze

```text
Authority gap
Competitor link advantage
Whether site needs local/niche links
Whether current authority is enough for target keywords
Whether paid backlink options need evaluation
```

### Output

```text
Directional authority comparison
Backlink priority
Need official export?
Safe link categories
Risk notes
```

Required disclaimer:

```text
This authority scan is directional unless verified with official Ahrefs/Semrush/Moz exports.
```

---

## 9. Workflow H: AEO/GEO Visibility Check

### Use When

```text
User wants AI search visibility.
SERP actor supports AI Overview/AI Mode or AI search add-ons.
Task involves AEO/GEO.
```

### Actor Category

```text
Google SERP scraper with AI Overview/AI Mode
AI-search actors/add-ons where available
Perplexity/ChatGPT/Copilot/Gemini search actors where available
Native AI-search testing if available
```

### Input

```text
Brand/entity questions
Service-intent questions
Comparison questions
Best/top provider questions
Cost/process questions
Problem-solution questions
```

Examples:

```text
best AI automation course in Pakistan
who offers AI agents course in Pakistan
best dental implants dentist in Arlington Heights
how much do dental implants cost in Arlington Heights
```

### Extract

```text
AI answer presence
Cited sources
Mentioned brands
Mentioned competitors
Narrative gaps
Questions generated/fan-out if available
```

### Analyze

```text
Does the brand appear?
Are competitors cited?
Which sources are cited?
What content format is being cited?
What entity information is missing?
What pages need answer blocks?
What proof/citations/schema are missing?
```

### Output

```text
AI-search visibility status
Mention/citation gap
Source-worthiness plan
AEO/GEO content blocks
Entity/schema recommendations
```

---

## 10. Workflow I: Free Backlink Prospecting

### Use When

```text
User wants free backlink posting ideas.
User has a backlink sheet/list.
Need entity-building support articles.
Need safe support backlinks.
```

### Actor Category

```text
SERP scraper
Website crawler
Manual/native scraping
Authority actor for prospect quality if needed
```

### Prospect Query Examples

```text
site:medium.com "write for us" niche
niche "guest post"
niche "submit article"
niche "contribute"
niche "community"
niche "forum"
niche "directory"
city business directory
industry association directory
```

### Analyze Prospects

```text
Indexability
Relevance
Traffic estimate if available
Outbound link behavior
Spam risk
Niche fit
Free/paid status
Anchor policy
Editorial quality
```

### Output

```text
Prospect URL
Type
Free/Paid
Relevance
Risk
Suggested article topic
Suggested anchor
Suggested target page
Priority
```

---

## 11. Workflow J: Paid Backlink Evaluation

### Use When

```text
User has a paid backlink offer.
Need decide buy/avoid/negotiate.
```

### Actor Category

```text
Website crawler
SERP scraper
Authority actor
Similarweb-style actor
Native browser inspection
```

### Input

```text
placement_domain
placement_page if known
price
target_page
proposed_anchor
niche
country
```

### Extract

```text
Indexation
Organic keywords estimate
Traffic estimate
Authority estimate
Outbound links
Recent posts
Niche relevance
Country relevance
Link selling pattern
Content quality
```

### Output Verdict

```text
Buy
Avoid
Negotiate
Use only branded anchor
Use nofollow/sponsored
Need more data
```

### Required Reasoning

```text
Relevance
Traffic
Authority
Spam risk
Anchor risk
Price fairness
Best target page
Best anchor
```

---

## 12. Workflow K: Scheduled Monitoring

### Use When

```text
Client has ongoing SEO campaign.
Need weekly/monthly tracking.
Apify schedules/webhooks are available.
```

### Monitoring Jobs

```text
Weekly SERP sample for priority keywords
Weekly competitor page change crawl
Monthly own-site crawl
Monthly backlink/authority directional scan
Weekly Google Trends/rising query scan
Monthly local/maps competitor review count scan
Monthly AEO/GEO visibility check
```

### Output

```text
Change summary
New issues
Ranking movement
Competitor movement
New content opportunities
Backlink opportunities
Local review movement
Next actions
```

---

## 13. Apify Workflow Output Standard

Every Apify workflow should produce:

```text
Workflow name
Actor/category used
Input scope
Date
Records collected
Confidence label
Key findings
Recommended actions
Missing data
Next run suggestion
```

Example:

```text
Workflow: SERP and Keyword Sample
Actor: Google SERP scraper
Input: 12 local service keywords, US, Arlington Heights, desktop
Records: 120 organic results + PAA data
Confidence: Confirmed for sampled SERPs
Finding: Competitors rank using dedicated service pages; client relies too heavily on homepage.
Action: Build service pages for family dentist, emergency dentist, Invisalign, cosmetic, veneers.
```

---

## 14. Mistakes to Avoid

Do not:

```text
Run large crawls without scope.
Treat scraped keyword appearances as rankings.
Treat Trends as search volume.
Treat community authority actors as official Ahrefs data.
Ignore failed or partial runs.
Give raw Apify output as the final report.
Forget to normalize fields.
Forget to label confidence.
```

---

## 15. Bottom Line

Apify workflows should help Beyond SEO move from opinion to evidence.

But the final deliverable must still be:

```text
What is wrong
Why it matters
What to fix first
What to build next
What to measure
What data is missing
```


## apify

# Apify Integration for Beyond SEO

Apify is the preferred external data layer for Beyond SEO.

The skill must remain useful without Apify, but when `APIFY_API_TOKEN` or Apify MCP access exists, Beyond SEO should use Apify as the primary collection layer for crawling, SERP checks, local SEO checks, trend research, competitor research, PageSpeed/Lighthouse-style checks, GSC/GA4-style connector or export workflows, social/content scans, and authority/backlink checks.

---

## 1. Purpose

Apify gives Beyond SEO a flexible marketplace-style data engine.

Use it for:

```text
Own-site crawling
Competitor crawling
Sitemap-based discovery
Google SERP scraping
People Also Ask / related queries extraction
AI Overview / AI Mode visibility checks where supported
Google Trends analysis
Google Maps/local competitor discovery
Review and ratings extraction where supported
Social profile/content scraping
Authority-style checks using Ahrefs/Semrush/Moz-like community actors
Google Search Console connector/export actors where available
GA4 connector/export actors where available
PageSpeed Insights or Lighthouse actors
Custom Crawlee actors
Scheduled SEO monitoring
Structured datasets for reporting
```

Apify should not replace human SEO judgment. It should provide raw data that Beyond SEO interprets. If Apify can collect the data, use Apify first. If an Apify actor is only scraping a third-party surface or estimating proprietary metrics, label the result as directional unless the actor is backed by authenticated first-party access or a user-provided export.

---

## 2. Required Access

Preferred environment variable:

```text
APIFY_API_TOKEN
```

Alternative access:

```text
Apify MCP server
Apify API client already configured by the host agent
Manual Apify dataset export uploaded by the user
CSV/JSON output from a previous Apify run
Authenticated Apify actor outputs for GSC, GA4, PageSpeed, Ahrefs, Semrush, Moz, or similar providers
```

If no Apify access exists, switch to Native Agent Scraping Mode or File Analysis Mode.

---

## 3. Apify Detection

Before using Apify, check:

```text
Is APIFY_API_TOKEN present?
Can the agent call Apify through MCP?
Can the agent run actors?
Can the agent read Apify datasets?
Can the agent export JSON/CSV?
```

Do not expose token values.

Correct:

```text
APIFY_API_TOKEN detected. I can use Apify Intelligence Mode.
```

Wrong:

```text
Your Apify token is apify_api_...
```

---

## 4. Apify Role in Beyond SEO

Apify should be used as a data collector, not as the strategist.

### Apify collects:

```text
URLs
HTML/text/Markdown
SERP results
AI-search answers where supported
People Also Ask
Related queries
Local business profiles
Reviews/ratings
Trends data
Social content
Public competitor data
Directional authority data
Authenticated first-party exports when an Apify actor connects to GSC, GA4, GBP, or another owned account
PageSpeed/Lighthouse measurements collected through Apify actors
```

### Beyond SEO decides:

```text
Which issues matter
Which pages need to be created
Which keywords are worth targeting
Which competitors are strongest
Which backlinks are safe or risky
Which actions should happen in 30/60/90 days
Which claims are confirmed vs directional
```

---

## 5. Data Quality Rules

Apify has official and community actors. Quality varies by actor.

Use these labels:

```text
Confirmed
Directional
Directional
Not verified
```

### Use Confirmed When

```text
The actor directly extracted visible public page data.
The crawl output contains the exact title/H1/meta/schema/page text.
The SERP output directly shows the result position for the query/region used.
The output includes raw URLs, snippets, dates, or visible text.
The Apify actor uses authenticated first-party access or an uploaded export for GSC, GA4, GBP, Ahrefs, Semrush, Moz, or similar data.
The Apify actor returns raw PageSpeed/Lighthouse measurements with URL, device, timestamp, and metric fields.
```

### Use Directional When

```text
A community actor estimates DR/DA/traffic/backlinks.
A third-party-style actor scrapes public Ahrefs/Semrush/Moz-like data.
A GSC/GA4/backlink actor does not clearly document whether data is authenticated/export-based or scraped/estimated.
An actor has low rating, few users, or unclear methodology.
The output conflicts with official exports.
```

### Use Not verified When

```text
No actor was run.
Actor failed.
Actor output is incomplete.
User did not provide official export/access.
The metric requires first-party data such as GSC, GA4, or GBP.
```

---

## 6. Apify Cost Awareness

Beyond SEO must not waste credits.

Use Apify intelligently:

```text
Start small.
Limit crawl depth for discovery.
Use sitemap where possible.
Test 5-10 URLs before full crawl.
Test 5-10 keywords before large SERP run.
Avoid crawling irrelevant assets.
Avoid duplicate competitor runs.
Use raw HTTP crawler when enough.
Use browser/headless mode only when JS rendering is needed.
Export only needed fields when possible.
```

Recommended credit-safe order:

```text
1. Crawl homepage + sitemap.
2. Crawl top money pages only.
3. Run SERP checks for 5-10 priority keywords.
4. Crawl 3-5 strongest competitors.
5. Add Trends/Maps/authority checks only when needed.
6. Expand only after findings justify it.
```

Never run a huge crawl without purpose.

---

## 7. Legal and Ethical Scraping Rules

Only scrape public data that is necessary for the SEO task.

Respect:

```text
robots.txt where applicable
site terms
privacy boundaries
personal data rules
rate limits
copyright boundaries
client confidentiality
```

Do not recommend scraping private user data, login-protected pages, or personal data unless the user has a legitimate right and the task is compliant.

Do not republish scraped content. Use it for analysis, summaries, and strategy.

---

## 8. Primary Apify Use Cases

### 8.1 Own-Site Crawl

Use to extract:

```text
URL
Title
Meta description
H1/H2
Text content
Markdown
Internal links
Canonical
Schema snippets if available
Status/code if actor supports it
Detected language
Content depth
```

Goal:

```text
Build page inventory and find SEO blockers.
```

### 8.2 Competitor Crawl

Use to extract:

```text
Competitor service pages
Page titles
H1/H2 structures
Content depth
FAQs
Schema
Internal links
CTA structure
Trust proof
Pricing/cost sections
Review/testimonial usage
```

Goal:

```text
Find what competitors rank with and what the client site lacks.
```

### 8.3 SERP Checks

Use to extract:

```text
Top organic results
Local pack/map results if supported
Ads
People Also Ask
Related queries
AI Overviews / AI Mode where supported
Result titles/snippets
Ranking URLs
Competitor domains
Search intent patterns
```

Goal:

```text
Understand what Google rewards for the target keyword and region.
```

### 8.4 Trends Research

Use to extract:

```text
Interest over time
Interest by region/city
Rising queries
Top related queries
Related topics
Seasonality
```

Goal:

```text
Prioritize topics by rising demand and regional relevance.
```

### 8.5 Local SEO / Maps

Use to extract:

```text
Competitor business names
Categories
Ratings
Review count
Address/service area
Opening hours
Website link
Phone
Photos if available
Review snippets if available
Map ranking patterns
```

Goal:

```text
Assess Google Business Profile and map-pack competition.
```

### 8.6 Backlink / Authority Directional Checks

Use only when actor exists and quality is acceptable.

Extract:

```text
DR/DA/Authority Score if available
Referring domains
Backlinks
Dofollow/nofollow if available
Organic traffic estimate
Top pages
Anchor data if available
```

Goal:

```text
Estimate authority gap and decide whether official exports are needed.
```

Always label as directional unless verified by official exports.

### 8.7 Social / Brand Authority Checks

Use when relevant.

Extract:

```text
YouTube posts/videos
Instagram content
Facebook pages/posts/reviews
TikTok content
Engagement patterns
Content topics
Brand mentions
Competitor content velocity
```

Goal:

```text
Understand brand demand, topical authority, and content ecosystem.
```

---

## 9. Standard Apify Workflow

When Apify is available:

```text
1. Define audit goal.
2. Select actor category.
3. Choose smallest useful input set.
4. Run actor or ask host agent to run it.
5. Retrieve dataset.
6. Normalize output.
7. Remove duplicates.
8. Label data confidence.
9. Convert data into SEO findings.
10. Prioritize actions.
11. Include missing data list.
```

---

## 10. Recommended Apify Data Normalization

Convert actor outputs into standard Beyond SEO fields.

### Crawl Output Standard

```text
source_actor
run_id
url
final_url
status_code
title
meta_description
h1
h2_list
word_count
text
markdown
canonical
robots_meta
schema_types
internal_links
external_links
images
page_type
seo_issue_flags
```

### SERP Output Standard

```text
source_actor
run_id
query
country
city_or_geo
language
device
date
organic_position
url
domain
title
snippet
serp_feature
paa_questions
related_queries
ai_answer_presence
ai_cited_sources
ads_presence
local_pack_presence
```

### Local Output Standard

```text
source_actor
run_id
query
city
business_name
category
rating
review_count
address
phone
website
hours
map_position
review_snippets
photos_count
profile_url
```

### Authority Output Standard

```text
source_actor
run_id
domain
metric_name
metric_value
referring_domains
backlinks
organic_keywords
organic_traffic_estimate
top_pages
anchor_examples
confidence_label
```

---

## 11. When Not to Use Apify

Do not use Apify when:

```text
User explicitly says not to use it.
Task can be answered from uploaded verified exports.
The crawl would be too expensive for a small request.
The target website prohibits the intended scraping.
The data requested is private or sensitive.
The actor is low quality and a manual/browser check is better.
```

---

## 12. Apify Failure Handling

If an actor fails:

```text
1. Do not apologize dramatically.
2. Note the failure.
3. Try a smaller input.
4. Try a simpler actor/category.
5. Switch to native scraping or file analysis.
6. Label unavailable data.
```

Example:

```text
The Apify crawl did not return enough body content. I will switch to a smaller crawl and also inspect the live pages manually. If the site is JS-heavy, we may need a headless-browser crawler or SSR check.
```

---

## 13. Best Practices for SEO Agents

Use Apify to build proof, not noise.

Bad:

```text
Crawl 10,000 pages and dump all issues.
```

Good:

```text
Crawl priority pages, classify issue patterns, then recommend fixes by impact.
```

Bad:

```text
Run 500 keywords randomly.
```

Good:

```text
Run 10 seed money keywords, identify SERP patterns, expand only into high-intent clusters.
```

Bad:

```text
Use community Ahrefs actor and present numbers as official.
```

Good:

```text
Use community Ahrefs-style actor as directional and ask for official Ahrefs/Semrush/Moz export for final authority confirmation.
```

---

## 14. Apify Output in Client Reports

In final reports, list Apify under data sources:

```text
Data Sources Used:
- Apify Website Content Crawler for page extraction
- Apify Google SERP scraper for keyword SERP checks
- Apify Google Trends scraper for topic trend validation
- Apify/third-party community actors for directional authority data
```

If community actors were used, add:

```text
Authority metrics from community actors are directional and should be verified with official Ahrefs, Semrush, or Moz exports before final budgeting.
```

---

## 15. Bottom Line

Apify gives Beyond SEO the hands and eyes.

The agent still needs the brain:

```text
Crawl
Compare
Classify
Prioritize
Explain
Plan
Measure
```

Never let raw data become the report. The report is the decision layer.


---

## AI-Friendly SEO Add-On Workflows

When a user asks for AI-friendly SEO, AEO, GEO, Entity SEO, Reputation SEO, or Conversation SEO, use Apify as the main collection layer.

Use Apify to collect:

```text
Website crawl data
Competitor crawl data
SERP/PAA/related-query data
Google Trends demand signals
Google Maps / Places data
Google reviews
Social profile and content data
Third-party mentions
Media/article sources
Backlink/authority signals
PageSpeed/Lighthouse data
AI Overview / AI Mode visibility where supported
GSC/GA4 connector or export actors where available
```

Then map collected data into:

```text
AEO answer block plan
GEO citation/source-worthiness plan
Entity SEO knowledge graph plan
Reputation SEO proof stack plan
Conversation SEO question map
AI-friendly SEO report
30/60/90-day roadmap
```

For detailed instructions, use:

```text
integrations/integrations.md#apify-ai-friendly-seo-workflows
aeo-geo/aeo-geo.md#ai-friendly-seo-master-workflow
```


## fallback-without-apis

# Fallback Without APIs

This file defines how Beyond SEO should work when Apify, DataForSEO, Ahrefs API, Semrush API, Moz API, Firecrawl, and other paid APIs are unavailable.

The skill must not become useless without APIs.

---

## 1. Core Principle

No API does not mean no SEO work.

It means:

```text
Use native browser/search/scraping if available.
Use uploaded files if available.
Use manual audit frameworks if no live tools exist.
Label anything unverified.
Ask for exports only when necessary.
```

---

## 2. Fallback Levels

### Level 1: Native Tools Available

Use:

```text
Browser
Search
Page scraping
HTML inspection
Sitemap/robots fetch
Screenshots
Manual competitor review
```

Mode:

```text
Native Agent Scraping Mode
```

### Level 2: Files Available

Use:

```text
GSC export
GA4 export
Crawl export
SEO PDF
Backlink sheet
Ahrefs/Semrush/Moz screenshots
Keyword CSV
Competitor report
```

Mode:

```text
File Analysis Mode
```

### Level 3: No Tools, No Files

Use:

```text
Advisory Mode
```

Output:

```text
Manual audit checklist
Data request list
Strategy template
Client intake questions
Implementation plan skeleton
```

---

## 3. What Can Still Be Done Without APIs

### With Website URL + Browser

```text
Homepage SEO review
Main service/page review
Navigation/internal linking review
Visible content depth check
Title/meta/H1 if accessible
Sitemap/robots check
Competitor discovery via search
Manual SERP intent review
Local visibility observations
AEO/GEO content readiness
Conversion path review
```

### With Uploaded GSC Export

```text
Actual queries
Clicks
Impressions
CTR
Average position
Pages with opportunity
Queries near top 3/top 10
CTR improvement opportunities
Content refresh priorities
Cannibalization hints
```

### With Uploaded GA4 Export

```text
Organic landing pages
Engagement
Conversion paths
Traffic channels
Assisted conversion hints
Pages with traffic but no conversion
```

### With Uploaded Crawl Export

```text
Technical SEO issues
Titles/meta
H1/H2
Status codes
Canonicals
Indexability
Word count
Internal links
Broken links
Redirects
Schema if included
```

### With Uploaded Backlink Export

```text
Referring domains
Anchor text
Dofollow/nofollow
Link relevance
Spam risk
Competitor link gap if included
Link cleanup priorities
```

---

## 4. What Cannot Be Confirmed Without APIs or Exports

Do not confirm:

```text
Exact search volume
Full keyword universe
Full ranking history
Full backlink profile
Complete technical crawl of large site
Actual GSC performance
Actual GA4 conversions
Actual GBP calls/directions
Complete local map rank tracking
AI Overview citation history
```

Use:

```text
Not verified from available data.
Recommended check:
```

---

## 5. Manual Research Methods

### Manual SERP Check

Use search queries:

```text
primary service + city
service + near me
best service + city
service cost + city
service provider + city
competitor service pages
```

Record:

```text
Top 10 domains
Ranking page type
SERP features
PAA questions
Local pack presence
Ads
Directories
Repeated competitors
```

### Manual Competitor Check

Open competitor pages and record:

```text
Title
H1
Sections
Content depth
FAQs
CTA
Reviews/trust proof
Location proof
Schema if visible
Internal links
```

### Manual Backlink Prospecting

Search:

```text
industry "write for us"
industry "guest post"
industry "submit article"
city "business directory"
city "chamber of commerce"
industry association directory
competitor brand mentions
```

Evaluate:

```text
Relevance
Indexability
Organic footprint if visible
Outbound link quality
Paid/free status
Risk
```

---

## 6. File-Based Audit Procedure

When uploaded files are available:

```text
1. Identify file type.
2. Extract metrics and findings.
3. Check date/freshness.
4. Separate facts from recommendations.
5. Consolidate issues.
6. Remove duplicate findings.
7. Prioritize by impact.
8. Build action plan.
9. List missing live checks.
```

Example:

```text
Confirmed from file: The report shows 36 ranking keywords.
Not verified live: Current rankings may have changed since report date.
Action: Use the keyword footprint as baseline, then verify with fresh SERP/GSC data.
```

---

## 7. Advisory Mode Output

When no data exists, output:

```text
1. What data is needed
2. How to collect it
3. What to check manually
4. What the SEO strategy should include
5. What templates to use
6. What not to claim yet
```

Advisory output is not an audit. Say that clearly.

---

## 8. Data Request List

If deeper audit is needed, ask for:

```text
Website URL
Target city/country
Main services/products/courses
Top competitors
GSC export last 3-6 months
GA4 landing page + conversion export
GBP insights export/screenshots
Ahrefs/Semrush/Moz export
Screaming Frog/Sitebulb crawl export
Backlink prospect sheet
Apify token if available
```

Do not ask for everything if the task is small.

---

## 9. Fallback Report Language

Use honest phrasing.

Good:

```text
Based on the visible pages and provided files, the main likely issue is shallow service-page depth. Exact rankings and backlinks were not verified because GSC and backlink exports were not provided.
```

Bad:

```text
Your rankings are low because backlinks are bad.
```

unless verified.

Good:

```text
The current report suggests authority is low. Verify with Ahrefs/Semrush/Moz before buying backlinks.
```

Bad:

```text
Buy 100 backlinks.
```

---

## 10. No-API SEO Plan Template

When user wants a plan without tools, structure it:

```text
Goal
Assumptions
Data needed
Manual checks
Technical SEO checklist
Keyword/page architecture
Competitor research method
Content plan
Local SEO plan
Backlink plan
AEO/GEO plan
Conversion plan
30/60/90-day roadmap
KPIs
Risks
```

---

## 11. Fallback for Backlinks

Without backlink APIs:

```text
Do not claim full profile.
Evaluate provided backlink URLs.
Use public search for brand mentions.
Use competitor visible links where discoverable.
Build safe prospect categories.
Ask for Ahrefs/Semrush/Moz export for full profile.
```

Safe categories:

```text
Local directories
Industry associations
Partner/vendor pages
Guest articles on relevant sites
Digital PR
Founder/expert interviews
Resource pages
Free publishing platforms used carefully
```

Unsafe categories:

```text
Bulk link packages
PBNs
Irrelevant high-DA sites
Exact-match anchor abuse
Sites with obvious paid-link farms
```

---

## 12. Fallback for AEO/GEO

Without AI-search scraping:

```text
Audit content structure.
Check entity clarity.
Check answer blocks.
Check schema.
Check expert proof.
Check direct question coverage.
Check citations/sources.
Recommend pages and sections likely to improve AI answer eligibility.
```

Do not claim:

```text
ChatGPT cites your site
Google AI Overview uses your page
```

unless checked.

---

## 13. Fallback for Local SEO

Without GBP access:

```text
Audit website NAP.
Check location/service pages.
Check visible reviews/testimonials.
Check public listings if available.
Recommend GBP audit.
Recommend review strategy.
Recommend citation cleanup.
```

Do not claim:

```text
GBP calls are low
Directions are down
Map rankings are X
```

unless provided.

---

## 14. Fallback for Technical SEO

Without a full crawl:

```text
Check sample pages.
Check sitemap.
Check robots.
Check source if available.
Check visible metadata.
Look for pattern issues.
Recommend full crawl for confirmation.
```

Use language:

```text
Sampled pages show...
Likely pattern...
Needs full crawl verification...
```

---

## 15. Bottom Line

Beyond SEO should never say:

```text
I cannot help because there is no API.
```

It should say:

```text
I can produce a first-pass or strategic audit with current access. For confirmed rankings, backlinks, traffic, and conversion data, we need GSC/GA4/GBP/backlink exports or an Apify/API data layer.
```

No excuses. No fake certainty. Just useful work.


## first-party-data-quality

# First-Party Data Quality

Normalize columns explicitly and run:

```text
python tools/first_party_quality.py --input normalized.csv --metadata export-metadata.json --output quality.json
```

Use `templates/first-party-metadata-template.json`. Audit config accepts `first_party_imports` entries with `input_path` and `metadata_path`. Imports validate and report aggregates; they do not automatically implement keyword strategy or authenticate owner declarations.

The runner validates property/site compatibility. GA4 metadata must include the owner's explicit `website_url` mapping because a numeric property ID does not identify a hostname. GSC properties must cover the target; domain properties covering multiple subdomains require explicit website mapping and appropriate filters for a subdomain audit. Standalone validation accepts `--website` for the same gate.

## GSC

Required metrics: `clicks`, `impressions`, `ctr` (0-1 ratio), `position`; dimensions must match metadata. Preserve property, search type, dates, timezone, device/country filters and export method. Duplicate keys and incompatible units are rejected. Zero impressions have no interpretable CTR/position; do not turn them into rank.

Query rows may omit anonymized queries and be truncated. Do not force their sums to match property totals. Calculate aggregate CTR from total clicks/impressions rather than averaging row CTR. Average position is not a fixed live rank. Reconcile Google-selected canonical URLs before joining performance and crawl datasets. Brand shares describe only the disclosed observed population.

Check the actual Search Console interface/API/export and current official docs before using AI-specific reports. Standard Web data alone cannot isolate an AI feature. Use feature fields only when explicitly present and documented. Manual AI samples require date, engine/model, prompt/query, location, sample size and repeatability limits.

## GA4 and CRM

Required GA4 metrics: `sessions`, `key_events`; include `key_event_definition`. A key event may occur multiple times per session. Identify channel filters, attribution model, consent mode, thresholding, sampling, event changes and timezone. A click is not automatically a qualified lead or revenue.

Reconcile forms, bookings, calls, spam, duplicates and qualification with CRM records where available. Explain differences between GSC clicks, analytics sessions and CRM leads.

## Comparisons

Match property, source, dimensions, filters, timezone, search type, event definition, attribution and equal-length non-overlapping windows. Note weekday composition, seasonality, tracking changes and low counts. `comparison_compatibility` identifies structural mismatches; compatible windows do not establish causation.

Sources: [GSC limits](https://developers.google.com/search/blog/2022/10/performance-data-deep-dive), [GSC API](https://developers.google.com/webmaster-tools/v1/how-tos/all-your-data), [Google AI features](https://developers.google.com/search/docs/appearance/ai-features). Refresh at use time.


## google-analytics

# Google Analytics Workflow

How Beyond SEO should use GA4 data.

---

## Key Data

Organic landing pages, sessions, engagement, conversions, events, source/medium, paths, and revenue where relevant.

## Use Cases

Find pages with traffic but low conversion, conversion tracking gaps, and landing page quality issues.

## Output

Tie SEO traffic to business outcomes, not vanity sessions.


## google-search-console

# Google Search Console Workflow

How Beyond SEO should use GSC exports or access.

Before analysis, load `integrations/integrations.md#first-party-data-quality`. Validate provenance, property, dates, timezone, filters, normalized units, anonymized-query/export limits and canonical URL attribution. GSC does not verify conversions. Average position is not a fixed live rank.

---

## Key Data

Queries, pages, clicks, impressions, CTR, average position, countries, devices, and dates.

When available, also inspect:

- branded vs non-branded query filters;
- Search Generative AI performance reports;
- AI feature impressions for AI Overviews, AI Mode, and Discover generative AI features;
- pages surfaced in generative AI features;
- countries, devices, and date trends for generative AI visibility.

These feature-specific checks are conditional: verify current official documentation and the property's actual UI/API/export fields. Do not assume dedicated reports exist or are required for eligibility. Standard Web metrics cannot isolate AI visibility by themselves. Check `core/current-guidance-register.json` for conflicting source wording and disclose unresolved capabilities.

## Use Cases

Find existing winners, fastest wins, low CTR pages, cannibalization hints, pages with impressions but weak clicks, and pages needing refresh.

Use branded/non-branded segmentation to separate brand demand from organic discovery. Treat non-branded growth as the cleaner signal for SEO expansion.

Use generative AI performance reports to identify pages already appearing in AI features, then improve those pages for clarity, proof, source-worthiness, internal links, and conversion. Do not treat AI impressions as a ranking position.

## Output

Create GSC opportunity table: query, page, impressions, clicks, CTR, position, issue, action.

If generative AI report data exists, add an AI visibility table:

```text
Page
AI feature type if available
Impressions
Country
Device
Date trend
Inferred reason surfaced with supporting evidence
Recommended improvement
Confidence
```

If the reports are not visible in Search Console, say:

```text
Search Generative AI performance reports were not available for this property, so AI visibility is not verified from first-party data.
```


## microsoft-clarity

# Microsoft Clarity Workflow

Use Microsoft Clarity as a first-party behavior and conversion-support source. It complements GSC and GA4; it does not replace query, ranking, revenue, or CRM evidence.

Official references:

- Data Export API: `https://learn.microsoft.com/en-us/clarity/setup-and-installation/clarity-data-export-api`
- Client API: `https://learn.microsoft.com/en-us/clarity/setup-and-installation/clarity-api`
- Semantic metrics: `https://learn.microsoft.com/en-us/clarity/insights/semantic-metrics`
- Privacy and consent: `https://learn.microsoft.com/en-us/clarity/faq`

## Access

Prefer either:

1. `CLARITY_API_TOKEN` generated by a Clarity project admin under **Settings → Data Export**; or
2. a dated JSON/CSV export supplied through `CLARITY_EXPORT_PATH`.

Saved JSON must contain `retrieved_at` (an ISO-8601 timestamp with UTC offset), `num_days`, `dimensions`, and raw `data`. Saved CSV must contain `retrieved_at_utc`, `window_days`, `metric_name`, `observed_value`, and optional `dimension` plus the matching dimension column (use `url` for `URL`). All rows must share one retrieval time and window. The importer ignores any supplied `report_section`, keeps only approved dimensions and numeric aggregate fields, discards identifier and unknown fields, and rebuilds report rows.

Never print, log, copy into configuration, or save the token. Send it only in the `Authorization: Bearer` header.

Run:

```text
python tools/clarity_export.py --days 3 --dimension URL --output output/clarity-live-insights.json
```

The export API permits:

- the previous 1, 2, or 3 days only;
- up to three dimensions: Browser, Device, Country/Region, OS, Source, Medium, Campaign, Channel, URL;
- 10 requests per project per day;
- 1,000 response rows with no pagination.

The API response is UTC. Record retrieval time, requested window, dimensions, row limit, and source with every import.

## Evidence Rules

Use `First-party verified` only for authenticated API output or an owner-supplied dated export with explicit provenance. Filename/header detection alone is not verification. Use `Screenshot verified` for dated dashboard screenshots. Use `Not verified` when neither exists.

Clarity can support observations about:

- traffic and page popularity within the exported window;
- engagement time and scroll depth;
- rage clicks, dead clicks, excessive scrolling, quick backs, script errors, and error clicks;
- device, browser, country/region, source, medium, campaign, channel, and URL breakdowns.

Do not use Clarity to claim:

- keyword rankings, impressions, CTR, search demand, backlinks, revenue, or qualified leads;
- a full monthly trend from the 1–3 day API window;
- causation from a frustration signal;
- a conversion unless the event and business outcome are correctly instrumented and independently validated.

Compare rates only when a valid denominator is present. Otherwise report exact counts and recommend investigation.

## Audit Workflow

1. Verify the tracking code is installed on the intended domain and templates.
2. Verify masking, privacy disclosure, consent mode, and regional consent behavior.
3. Verify custom events/tags for meaningful actions such as form start, form submit, booking, call click, checkout, or lead qualification.
4. Export a URL breakdown for the latest 1–3 days.
5. Segment by device or source only when a second request is justified and within quota.
6. Prioritize landing pages with material traffic plus friction or shallow engagement.
7. Review recordings and heatmaps manually for the highest-value signals; do not export personal or sensitive content into reports.
8. Connect behavioral findings to a page, hypothesis, recommended change, owner, and validation method.

## Privacy Gate

- Do not use Clarity on websites or apps targeting users under 18.
- Keep sensitive content masked and never include personal identifiers, recording links, or raw user-level data in client PDFs.
- Pass consent signals through Clarity Consent Mode or a supported consent platform where required.
- Treat fragmented sessions or reduced recording coverage as a measurement limitation when consent is absent.
- Ask the client or privacy owner to approve tracking and retention settings; do not provide legal certification.

## PDF Output

When verified Clarity data exists, add a **Microsoft Clarity Behavior Insights** section containing:

- source, evidence label, UTC retrieval time, requested window, dimensions, and API limitations;
- compact metric/segment rows;
- URL-level friction signals where available;
- recommended investigation or experiment;
- a clear note that behavior signals do not prove SEO causation.

When Clarity is unavailable, show:

```text
Microsoft Clarity: Not verified. Connect CLARITY_API_TOKEN or provide a dated export.
```

Do not add Clarity to the overall SEO score unless a separate, documented conversion/UX scoring model exists and all required inputs are verified.


## native-agent-scraping

# Native Agent Scraping Workflow

This file defines how Beyond SEO should work when Apify is not available but the AI-agent environment has browser, search, scraping, page-opening, screenshot, or HTML-reading tools.

Many agents already have scraping tools. Beyond SEO should use them before asking for a separate API.

---

## 1. When to Use

Use Native Agent Scraping Mode when:

```text
No APIFY_API_TOKEN is available
No Apify MCP access exists
The agent can still browse/search/open pages
The agent can inspect pages or scrape visible content
The user only gave a URL
The task needs first-pass SEO analysis
```

This mode is still useful. It is not a “weak mode” if used carefully.

---

## 2. Native Tool Examples

Depending on the host environment, native tools may include:

```text
Browser/open URL
Search engine access
HTML extraction
Screenshot analysis
Built-in crawler
Playwright/Puppeteer
Requests + BeautifulSoup
Sitemap fetcher
Robots.txt fetcher
File reader
CSV parser
Schema validator
PageSpeed tool
Custom scraper
MCP browser tools
```

Use whatever exists.

---

## 3. Native Scraping Priorities

Start with high-value checks:

```text
1. Homepage
2. Sitemap.xml
3. Robots.txt
4. Main service/product/course pages
5. Blog/resources page
6. Contact/conversion page
7. Competitor top pages
8. SERP top results for target keywords
9. Local/GBP public profiles where available
10. Backlink/prospect pages if relevant
```

Do not try to crawl the entire internet.

---

## 4. First-Pass Native Website Audit

### Step 1: Open Homepage

Extract:

```text
Title tag
Meta description
H1
Visible hero copy
Main navigation
Primary CTA
Internal links to service pages
Trust proof
Schema if visible/source accessible
```

Ask:

```text
Is the main business/entity clear?
Is the primary offer clear?
Is there a location if local?
Is the page crawlable?
Does the page target the right keyword?
```

### Step 2: Check Sitemap

Try:

```text
/domain.com/sitemap.xml
/domain.com/sitemap_index.xml
/domain.com/wp-sitemap.xml
robots.txt sitemap references
```

Extract:

```text
Total URLs
URL types
Priority routes
Old/irrelevant URLs
Missing service pages
Blog/article coverage
```

### Step 3: Check Robots

Try:

```text
/domain.com/robots.txt
```

Look for:

```text
Blocked important paths
Sitemap reference
Crawl traps
Staging paths
Admin/private paths properly blocked
```

### Step 4: Inspect Money Pages

For each main page:

```text
URL
Title
Meta
H1
H2
Content depth
Intent match
CTA
Trust proof
FAQ
Schema
Internal links
Conversion path
```

### Step 5: Check Blog/Support Content

Look for:

```text
Topical clusters
Internal links to money pages
Author/expert proof
Freshness
Long-tail intent coverage
```

---

## 5. Native SERP Research

When search tools exist, run small targeted SERP checks.

Use:

```text
Primary service + city
Service + near me
Best + service + city
Cost + service + city
Competitor brand terms
Course/product category terms
```

Extract manually:

```text
Top ranking domains
Ranking page type
Directory presence
Local pack presence
PAA questions
Featured snippets
AI answer/AI Overview presence if visible
Ads presence
Repeated competitors
```

Output:

```text
SERP intent
Competitor list
Page types Google rewards
Questions to answer
Content/page gaps
```

---

## 6. Native Competitor Research

Use SERP top results or user-provided competitors.

For each competitor, inspect:

```text
Homepage positioning
Main service pages
Location pages
Blog/resources
FAQ sections
Schema if visible
CTA style
Trust proof
Reviews/testimonials
Internal linking
Content depth
```

Create a competitor gap table:

```text
Competitor
Strong pages
Missing on client site
Content depth
Trust proof
Schema
CTA strength
Backlink/authority data if visible
Action for client
```

---

## 7. Native Backlink/Authority Research

Without Ahrefs/Semrush/Moz/API, do not pretend to know full backlink profile.

Possible checks:

```text
Search brand mentions
Search exact domain mentions
Search competitor "write for us" and directory opportunities
Check public profiles/directories
Check obvious citations
Inspect user-provided backlink URLs
Evaluate paid backlink placement pages
```

Use search queries:

```text
"brand name" -site:clientdomain.com
"clientdomain.com" -site:clientdomain.com
"competitor.com" -site:competitor.com
industry "write for us"
industry "guest post"
city "business directory"
industry association directory city
```

Output:

```text
Backlink opportunities
Brand mention opportunities
Citation gaps
Need official backlink export
```

Required label:

```text
Backlink profile not fully verified without official backlink data or a trusted backlink source.
```

---

## 8. Native Local SEO Checks

Use public information only.

Check:

```text
Business name consistency
Website NAP
Contact page
Footer NAP
Google map embed if present
Location/service pages
Review widgets/testimonials
Schema
Public GBP if search can show it
Competitor map/listing visibility if visible
```

Do not claim actual GBP performance unless data is provided.

Output:

```text
Local visibility gaps
GBP data needed
Review strategy
Local pages needed
Citation cleanup needs
```

---

## 9. Native AEO/GEO Checks

Inspect whether pages answer questions clearly.

Look for:

```text
Definitions
Direct answer blocks
Cost sections
Process/steps
Comparison tables
Risks/limitations
FAQs
Author/expert credentials
Sources/citations
Schema
Entity clarity
```

Search for:

```text
Who is [brand]?
Best [service] in [city]
How much does [service] cost in [city]?
[service] vs [alternative]
How to choose [provider type]
```

Output:

```text
Entity clarity gap
Answer block gaps
Source-worthiness gaps
Schema/entity recommendations
```

---

## 10. Native Technical Checks

Depending on available tools, check:

```text
HTTPS
www/non-www consistency
Redirects
404 pages
Canonical tags
Title/meta
H1/H2
Robots
Sitemap
Index/noindex
Mobile visible issues
Speed observations if PageSpeed available
Schema snippets
Broken navigation links
Thin/empty pages
```

If the tool cannot inspect HTML, say so.

---

## 11. Data Labels in Native Mode

Use:

```text
Confirmed
Inferred
Directional
Not verified
```

Examples:

```text
Confirmed: the homepage H1 is missing from visible content.
Inferred: the site may have JavaScript-rendering SEO issues because direct HTML shows very little body content.
Not verified: exact rankings and backlinks require GSC/rank/backlink data.
```

---

## 12. Native Mode Output Structure

For a first-pass audit:

```text
Audit Mode: Native Agent Scraping Mode

Available:
- Website URL
- Browser/search/scraping tools

Missing:
- GSC
- GA4
- GBP
- Backlink export
- Apify

Findings:
1. Technical
2. On-page
3. Content
4. Keyword/SERP
5. Competitor
6. Local if relevant
7. Backlinks if relevant
8. AEO/GEO
9. Conversion
10. Next actions
```

---

## 13. When Native Mode Is Enough

Native mode can be enough for:

```text
Proposal preparation
First-pass audit
Page structure review
Content strategy
AEO/GEO recommendations
Service-page planning
Competitor page comparison
Client discovery
```

---

## 14. When Native Mode Is Not Enough

Need stronger data for:

```text
Exact keyword ranking report
Traffic performance
Query-level GSC data
Conversion analysis
GBP calls/directions
Complete backlink audit
Large site technical crawl
Historical trend analysis
```

Ask for:

```text
GSC export
GA4 export
GBP export
Ahrefs/Semrush/Moz export
Apify token
Crawl export
```

---

## 15. Common Mistakes to Avoid

Do not:

```text
Say “I crawled the whole site” if only a few pages were opened.
Say “site has no backlinks” without backlink data.
Say “not ranking” without SERP/GSC/rank data.
Say “technical SEO is fine” without checking source/crawl.
Rely only on homepage.
Ignore sitemap.
Ignore competitors.
Ignore conversion.
```

---

## 16. Bottom Line

Native scraping mode is practical and powerful when used honestly.

It should produce:

```text
A strong first-pass diagnosis
A clear list of verified findings
A clear list of missing data
A practical roadmap
```

Not fake certainty.


## no-paid-seo-intelligence

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


## pagespeed-insights

# PageSpeed Insights Workflow

How Beyond SEO should use PageSpeed and Core Web Vitals data.

---

## Metrics

LCP, INP, CLS, TTFB, mobile/desktop performance, field data, lab data.

## Use Cases

Identify page speed issues that hurt UX, crawl efficiency, and conversion.

## Caution

Do not make speed the whole SEO strategy. Speed is important, but weak content and architecture still need fixing.


## seo-data-tools-evidence

# SEO Data Tools Evidence Workflow

Use this file when the user asks for authentic keywords, competitor keywords, backlink data, ranking data, trend data, or tool-backed SEO reporting.

Beyond SEO can use outputs from SEO platforms, but must not pretend access exists.

If the user asks to use Semrush, Ahrefs, DataForSEO, Moz, SERP tools, or "trending SEO tools" but no paid API/export/access is available, also load:

```text
integrations/integrations.md#no-paid-seo-intelligence
integrations/integrations.md#seo-tool-methodology
```

Use that workflow to produce legitimate no-paid evidence from live SERP samples, competitor pages, public snippets, user-provided screenshots, CSV exports, and first-party data. Never clone, scrape, or imply access to proprietary paid-tool databases without authorization.

If the user asks how these metrics work, how to imitate paid-tool workflows, or how to move from free checks to paid exports, load:

```text
integrations/integrations.md#seo-tool-methodology
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


## seo-tool-methodology

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


## technical-crawl-imports

# Technical Crawl Import Workflow

Use this file when the user provides Screaming Frog, Sitebulb, Lumar, JetOctopus, or other technical crawl exports, especially for large websites.

Load this together with:

```text
tools/source_classifier.py
core/import-schemas.json
core/import-schemas.json
```

---

## 1. Supported Export Types

Preferred exports:

```text
Screaming Frog Internal HTML export
Screaming Frog Response Codes export
Screaming Frog Page Titles export
Screaming Frog Meta Descriptions export
Screaming Frog H1/H2 export
Screaming Frog Canonicals export
Screaming Frog Directives export
Screaming Frog Inlinks export
Screaming Frog Structured Data export
Sitebulb URL List
Sitebulb Hints / Issues export
Sitebulb Internal Links export
Sitebulb Structured Data export
```

If only one export is available, use it and label missing technical areas as not verified.

---

## 2. Required Fields to Normalize

Normalize crawl exports into these fields when possible:

```text
URL
Status code
Indexability
Indexability reason
Canonical URL
Title
Title length
Meta description
Meta description length
H1
H2
Word count
Content type
Internal inlinks
Internal outlinks
Crawl depth
Robots directives
Response time
Structured data status
Issue count
```

---

## 3. Issue Classification

Classify crawl findings by business impact:

```text
Critical:
Indexable pages blocked by robots/noindex unexpectedly
Important pages returning 4xx/5xx
Canonical points to wrong URL
Redirect chains on money pages
Duplicate canonical clusters affecting key pages
Broken internal links to conversion or service pages

High:
Missing titles/H1s on important pages
Duplicate titles/meta across important templates
Thin money pages
Orphan or low-inlink money pages
Slow response time patterns
Missing structured data on key page types

Medium:
Long or short title/meta patterns
Minor duplicate headings
Image alt gaps
Pagination/faceted URL cleanup
Non-critical 3xx cleanup

Low:
Formatting polish
Legacy pages with no traffic or links
Small metadata improvements on low-value pages
```

Do not treat every crawler warning as equal. Prioritize by page type and revenue impact.

---

## 4. Large Site Workflow

For large sites:

```text
1. Classify URLs by page type: homepage, service, category, product, blog, location, legal, tag, parameter, asset.
2. Separate indexable from non-indexable pages.
3. Summarize issue counts by page type.
4. Identify patterns, not just individual URLs.
5. Inspect top revenue pages manually.
6. Build a technical fix backlog with acceptance criteria.
7. Add sample affected URLs for every pattern.
8. Mark whether the issue is confirmed from crawl export or needs live verification.
```

---

## 5. Required Report Tables

### Crawl Summary

```text
Metric
Count
Share
Evidence source
Notes
```

### Technical Issue Backlog

```text
Issue
Severity
Affected URL count
Example URLs
Page type affected
Business impact
Fix
Acceptance criteria
Confidence
```

### Page Type Health

```text
Page type
Indexable pages
Noindex/blocked pages
4xx/5xx pages
Missing title/H1
Thin pages
Canonical issues
Internal link issues
Priority
```

---

## 6. Acceptance Criteria Examples

Use concrete acceptance criteria:

```text
All indexable service pages return 200, self-canonicalize, have one H1, and appear in XML sitemap.
No internal links point to 404 URLs from primary navigation, footer, service hubs, or money pages.
All old URLs with backlinks or SERP visibility 301 redirect to the closest current page.
No money page has fewer than 500 crawlable words unless intentionally thin.
Canonical clusters are documented and each cluster points to the intended ranking URL.
```

---

## 7. Data Quality Rules

Use:

```text
Technical crawl verified
```

only for data present in the export.

Use:

```text
Needs live verification
```

for issues affected by rendering, personalization, bot handling, current server state, or stale crawl dates.

Always include crawl date/export date when available.
