# Keyword Research

Use the contents below to select the relevant workflow; load only the needed sections.


## keyword-clustering

# Keyword Clustering

Keyword clustering groups search terms by intent so the agent builds the right pages instead of creating duplicate, cannibalized, or useless content.

## Purpose

Answer:

```text
Which keywords belong together?
Which keywords need separate pages?
Which keywords are support topics?
Which questions should become AEO blocks?
Which should be ignored?
```

## Inputs

```text
Keyword list
SERP top results
GSC queries
Competitor pages
Existing sitemap
Page inventory
People Also Ask
Related searches
Business services/products/courses
```

## Cluster Types

### Money Page Cluster

High-intent searches that deserve a commercial landing page.

Example:

```text
dental implants arlington heights
implant dentist arlington heights
dental implant dentist near me
```

Target:

```text
/dental-implants-arlington-heights/
```

### Service Subpage Cluster

Specific treatment/service needs its own page.

```text
all on 4 dental implants arlington heights
full arch dental implants arlington heights
```

Target:

```text
/all-on-4-dental-implants-arlington-heights/
```

### Support Article Cluster

Informational phrases that support a money page.

```text
dental implant cost
dental implants vs dentures
how long do dental implants last
```

Target:

```text
/dental-implant-cost/
```

Link to:

```text
/dental-implants/
```

### Course Cluster

```text
AI automation course
AI automation course Pakistan
no-code automation course
```

Target:

```text
/ai-automation-course/
```

### AEO Question Cluster

```text
what are AI agents
how do dental implants work
how to learn prompt engineering
```

Target:

```text
FAQ section, answer block, or support article
```

## SERP Similarity Rule

If keywords show the same ranking URLs and same page type, they usually belong on one page.

If SERPs show different page types or different intent, create separate pages.

Example:

```text
"dental implants arlington heights" and "implant dentist arlington heights" can usually share one page.
"all on 4 dental implants arlington heights" likely needs a dedicated subpage.
"how much do dental implants cost" usually needs a cost/support page.
```

## One Page vs Multiple Pages

Use one page when:

```text
Intent is the same.
SERP overlap is high.
One page can answer the topic naturally.
```

Use separate pages when:

```text
Intent is different.
Service/product/course is different.
SERP page types differ.
Topic needs deep standalone treatment.
Location/service combination is important.
```

Use support articles when:

```text
Question is informational.
SERP shows guides/PAA.
Topic supports a money page.
```

## Hierarchy

```text
Homepage / main category
↓
Hub money pages
↓
Sub-service pages
↓
Support articles
↓
FAQ/answer blocks
```

Dental example:

```text
/dentist-arlington-heights/
↓
/family-dentist-arlington-heights/
/emergency-dentist-arlington-heights/
/dental-implants/
↓
/dental-implant-cost/
/all-on-4-vs-dentures/
```

Academy example:

```text
/ai-course-pakistan/
↓
/ai-automation-course/
/ai-agents-course/
/prompt-engineering-course-pakistan/
↓
/what-is-ai-automation/
/ai-agents-explained-urdu-hindi/
```

## Cluster Fields

```text
Cluster name
Primary intent
Primary keyword
Secondary keywords
AEO questions
Target page type
Recommended URL
Existing page?
Current rank if available
Competitor page example
Business value
Priority
Internal link targets
Required support articles
```

## Output Template

```text
## Keyword Clusters

| Cluster | Intent | Primary Keyword | Target URL | Existing/New | Priority |

### Cluster Details
Cluster:
Target URL:
Intent:
Primary keyword:
Secondary keywords:
Questions:
Required sections:
Supporting articles:
Internal links:
Competitor example:
Priority:
```

## Mistakes to Avoid

```text
One page per keyword variation
Merging different intents
Using blogs for commercial intent
Creating thin local doorway pages
Ignoring existing pages
Ignoring SERP similarity
Ignoring internal linking
```

## Final Gate

A cluster is ready when:

```text
Intent is clear.
Target page is clear.
Support content is mapped.
Internal links are planned.
Cannibalization risk is reduced.
Priority is assigned.
```


## keyword-discovery

# Keyword Discovery

Keyword discovery in Beyond SEO is a business-intent mapping process, not a volume dump.

## Purpose

Discover the searches that can create ranking opportunity, qualified traffic, local visibility, leads, enrollments, bookings, or authority.

Every keyword must become one of these:

```text
Existing winner to defend
Fastest win to improve
Missing money page to build
Support article to publish
Local/GBP action to execute
AEO/GEO answer opportunity
Backlink/authority action
Ignore / no action
```

## Inputs

Use whatever is available:

```text
Website URL
Sitemap and crawl
Target services/products/courses
Target city/country
GSC queries
GA4 landing pages
GBP search terms
Apify SERP data
Apify Google Trends data
Native search
Competitor pages
Ahrefs/Semrush/Moz exports
Client PDFs/reports
Sales/support questions
Customer reviews
```

If ranking, volume, or traffic data is unavailable, label it as `Not verified`.

## Discovery Sources

### First-party

Highest trust:

```text
Google Search Console
Google Analytics
GBP insights
CRM leads
Sales questions
Support questions
Internal site search
```

### SERP

Use:

```text
Google SERP scraping
People Also Ask
Related searches
Autocomplete
AI Overview / AI Mode sources if available
Local pack
Directories and review platforms
```

### Competitor

Use:

```text
Competitor service pages
Competitor course/product pages
Competitor blog/support clusters
Competitor title/H1 patterns
Competitor local pages
Competitor FAQs
```

### Trend and topic demand

Use:

```text
Google Trends
Social/content scraping
YouTube topics
Community questions
News/trend pages
```

Google Trends is relative interest, not exact search volume.

## Keyword Classes

Classify every keyword:

```text
Brand
Core money keyword
Local service keyword
Emergency/urgent keyword
Course/enrollment keyword
Product/category keyword
Comparison keyword
Cost/pricing keyword
Problem/pain keyword
How-to keyword
Review/trust keyword
Near-me/map intent
AEO/question keyword
Topical authority keyword
Low-value/no-action keyword
```

## Business Value

Score business value:

```text
5 = direct revenue/query intent
4 = strong commercial/local intent
3 = supports money page or mid-funnel research
2 = awareness only
1 = mostly irrelevant
0 = ignore
```

High-value examples:

```text
dental implants arlington heights
emergency dentist arlington heights
AI automation course Pakistan
AI agents course
SEO audit service Karachi
```

## Intent Rules

Classify intent before page planning:

```text
Informational
Commercial investigation
Transactional
Local
Emergency
Navigational
AEO/question
```

Then choose page type:

```text
Service page
Course page
Product page
Location page
Comparison page
Cost page
FAQ/support article
Blog article
GBP/service action
No page needed
```

## Expansion Patterns

### Local service

```text
[service] + city
[service] near me
best [service] + city
emergency [service] + city
[service] cost + city
[provider type] + city
```

### Course / academy

```text
[topic] course
[topic] course + country
[topic] certification
learn [topic]
[topic] training
[topic] course Urdu/Hindi
[topic] for [profession]
```

### AEO/GEO questions

```text
what is [topic]
how does [service] work
how much does [service] cost
[service] vs [alternative]
how to choose [provider/course/product]
is [service/course/product] worth it
```

## Existing Winners

If the site already ranks:

```text
Top 1-3: defend, improve CTR/conversion, add internal links.
Top 4-10: push into top 3 with content depth, links, schema, CTA.
Top 11-20: fastest-win optimization if value is high.
```

Existing winners often produce faster revenue than brand-new pages.

## Missing Money Pages

A keyword cluster becomes a missing money page when:

```text
It has commercial/local intent.
Competitors have dedicated pages.
The client has no proper page.
The current page cannot satisfy intent.
Business value is high.
```

Output:

```text
Recommended URL
Primary keyword
Secondary keywords
Required sections
Internal links
Schema
CTA
Priority
```

## Priority Formula

```text
Priority = Business Value + Intent Strength + Current Opportunity + Ranking Feasibility + Content Gap Urgency - Authority Requirement
```

Labels:

```text
Very High
High
Medium
Low
Ignore
```

## Output Template

```text
## Keyword Discovery

### Data Sources Used
### Existing Winners
| Keyword | Rank | URL | Action |

### Fastest Wins
| Keyword | Rank | URL | Fix |

### Missing Money Pages
| Cluster | Required URL | Why | Priority |

### Support Content
| Topic | Supports Page | Intent | Priority |

### AEO/GEO Questions
| Question | Target Page/Section | Priority |

### Ignored Keywords
| Keyword | Why Ignored |
```

## Common Mistakes

Do not:

```text
Choose keywords only by volume.
Map everything to homepage.
Use blog posts for commercial service intent.
Ignore local intent.
Ignore existing ranking momentum.
Create pages for useless variations.
Invent volume or rankings.
```

## Final Gate

Keyword discovery is complete when every valuable keyword has:

```text
Intent
Business value
Current status
Required page/action
Priority
Measurement plan
```


## keyword-to-page-map

# Keyword-to-Page Map

Every valuable keyword must map to a page, action, or ignore decision.

This is where SEO becomes execution.

## Purpose

Answer:

```text
Which page should rank for which keyword?
Which existing page needs improvement?
Which new page must be created?
Which keywords support money pages?
Which keywords are GBP/backlink/AEO actions?
Which keywords should be ignored?
```

## Required Columns

```text
Keyword
Cluster
Intent
Volume
Current Rank
Current URL
Best Competitor URL
Required Page Type
Recommended URL
Existing/New
Business Value
Priority
Main Action
Supporting Content Needed
Internal Links Needed
Schema Needed
CTA
Confidence
Notes
```

If rank/volume is unavailable:

```text
Not verified
```

## Page Type Options

```text
Homepage
Service page
Sub-service page
Product page
Course page
Category page
Location page
Comparison page
Cost/pricing page
FAQ/support article
Blog article
Author/expert page
Case study
GBP/service action
Backlink/authority action
No action
```

## Mapping Logic

### Existing Page Improvement

Use when:

```text
Relevant page exists.
It has ranking momentum.
It can satisfy intent after improvement.
```

Actions:

```text
Expand content
Fix title/H1/meta
Add FAQs
Add schema
Add internal links
Add trust proof
Improve CTA
Build links if authority gap exists
```

### New Page Creation

Use when:

```text
No suitable page exists.
SERP rewards dedicated pages.
Intent is distinct.
Business value is high.
```

Actions:

```text
Create URL
Write page brief
Add internal links
Add schema
Add CTA
Add support content
```

### Support Article

Use when:

```text
Intent is informational.
Question supports a money page.
SERP shows guides/articles/PAA.
```

Actions:

```text
Write answer-focused article
Link to money page
Add expert proof
Add FAQ where useful
```

### GBP Action

Use when:

```text
Near-me/map/local pack intent is strong.
```

Actions:

```text
Optimize GBP categories, services, posts, photos, reviews, Q&A, UTM links.
```

### Backlink Action

Use when:

```text
Page is good but competitors are stronger in authority.
```

Actions:

```text
Build niche/local/PR links to page or cluster.
```

## Existing Winner Handling

```text
Top 1-3: defend + conversion + CTR.
Top 4-10: optimize to push top 3.
Top 11-20: fastest-win sprint.
```

## Missing Money Page Handling

For high-intent missing pages:

```text
Create dedicated page.
Map support articles.
Add homepage/service hub links.
Add schema.
Add page-specific CTA.
Add local proof if relevant.
```

## Examples

### Local Dental

```text
Cluster: Family Dentist Arlington Heights
Intent: Local service
Recommended URL: /family-dentist-arlington-heights/
Action: Create local service page
Schema: Dentist, Service, LocalBusiness, FAQPage
CTA: Book family appointment
```

### Academy

```text
Cluster: AI Automation Course
Intent: Course/enrollment
Recommended URL: /ai-automation-course/
Action: Create 1,500+ word course landing page
Schema: Course, Organization, Person, FAQPage
CTA: Join AI Automation Class
```

## Internal Link Mapping

Each money page should have:

```text
Homepage link
Navigation/service/category hub link
2-5 support article links pointing in
Related page links
Breadcrumbs
```

Use natural anchors.

Good:

```text
AI automation course
dental implants in Arlington Heights
emergency dental care
```

Bad:

```text
best dentist arlington heights best dentist arlington heights
```

## Schema Mapping

```text
Service page → Service + Organization/LocalBusiness + FAQPage + Breadcrumb
Local service page → LocalBusiness/Dentist/Service + FAQPage + Breadcrumb
Course page → Course + Organization + Person + FAQPage + Breadcrumb
Article → Article + Person + Organization + Breadcrumb
Product → Product + Breadcrumb
```

## Output Template

```text
## Keyword-to-Page Map

| Keyword | Cluster | Intent | Current Rank | Current URL | Recommended URL | Existing/New | Priority | Main Action |

### New Pages Required
| Page | Keywords | Why | Priority |

### Existing Pages to Improve
| Page | Keywords | Fix | Priority |

### Support Articles Required
| Article | Supports | Intent | Priority |

### GBP Actions
| Keyword | GBP Action | Priority |

### Backlink/Authority Actions
| Page/Cluster | Link Need | Priority |
```

## CSV Template

```csv
Keyword,Cluster,Intent,Volume,Current Rank,Current URL,Best Competitor URL,Required Page Type,Recommended URL,Existing/New,Business Value,Priority,Main Action,Supporting Content Needed,Internal Links Needed,Schema Needed,CTA,Confidence,Notes
```

## Final Gate

The map is complete when every valuable keyword has:

```text
Intent
Target page
Action
Priority
CTA
Internal link plan
Schema plan
Measurement plan
```


## local-keyword-research

# Local Keyword Research

Finds and maps local service keywords.

---

## Patterns

[service] + city, [service] near me, best [service] + city, emergency [service] + city, [provider] + city, [service] cost + city.

## Map Intent

If map pack dominates, combine website pages with GBP/reviews/citations.

## Output

Keyword, city, intent, page/GBP action, priority.


## long-tail-keyword-plan

# Long-Tail Keyword Plan

Uses long-tail queries to support money pages and AEO/GEO.

---

## Sources

GSC, PAA, related searches, reviews, sales questions, competitor FAQs, AI-search prompts.

## Use Cases

FAQ sections, support articles, cost/process/risk pages, comparison pages.

## Output

Long-tail query, target page/section, internal link target, priority.


## money-keyword-selection

# Money Keyword Selection

Selects keywords with the highest business impact.

---

## Formula

Business value × intent strength × feasibility × current opportunity.

## High Value

Service, product, course, local, emergency, cost, comparison, and booking/enrollment intent.

## Output

Keyword, value, intent, target page, priority.


## rank-tracker

# Rank Tracker

Use this module when the user asks to track rankings, monitor keyword movement, compare current vs previous SERPs, or build a recurring SEO progress report.

## Data Rules

- Prefer GSC average position, paid rank-tracker exports, DataForSEO SERP exports, or Apify/manual SERP samples.
- Treat one-time SERP samples as `Live SERP sample`, not stable rank truth.
- Store date, country, language, device, location, query, observed URL, observed position, and source.
- Do not invent current rank or movement when no prior snapshot exists.

## Tracking Table

Use this schema:

```text
date
keyword
country
location
device
source
observed_position
observed_url
previous_position
position_change
serp_features
top_competitors
confidence
notes
```

## Workflow

1. Normalize the target keywords and target URLs.
2. Load prior tracking CSV/JSON if provided.
3. Collect fresh rank evidence from available sources.
4. Compare only like-for-like location/device/source where possible.
5. Label keyword movement as improved, declined, unchanged, new, lost, or not comparable. For audit findings, use `Improved` only when known severity decreases and `Worsened` when it increases.
6. Flag cannibalization when multiple target URLs appear for the same query.
7. Recommend actions for keywords in positions 4-20 before chasing brand-new terms.

## Output

For every tracked keyword include:

- Current observed position.
- Ranking URL.
- Previous position when available.
- Movement.
- Source and confidence.
- Recommended page action.

## Report Notes

- Use sparklines or movement arrows only when historical data exists.
- For first runs, call the table a baseline, not a trend.
- Keep paid-tool and live-SERP rank evidence separate.


## search-intent-analysis

# Search Intent Analysis

Classifies keyword intent and matches it to the correct page type.

---

## Intent Types

Informational, commercial, transactional, local, emergency, navigational, brand, review/trust, AEO/question.

## SERP Reading

Use top results to decide whether the keyword needs a service page, course page, blog, comparison page, cost page, GBP action, or no action.

## Output

Keyword, intent, SERP pattern, required page type, action.


## top-5-keyword-defense

# Top 5 Keyword Defense

Protects keywords where the site already ranks well.

---

## Actions

Improve CTR, strengthen page content, add internal links, improve conversion, monitor competitors, refresh schema, protect brand trust.

## Do Not

Do not unnecessarily rebuild pages already winning unless evidence supports it.

## Output

Keyword, rank, page, risk, defense action.
