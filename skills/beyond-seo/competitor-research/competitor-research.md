# Competitor Research

Use the contents below to select the relevant workflow; load only the needed sections.


## authority-gap-analysis

# Authority Gap Analysis

Compares backlink and domain authority signals between client and competitors.

---

## Metrics

Referring domains, DR/DA/AS, organic keyword footprint, traffic estimate, link relevance, anchors, link quality.

## Caution

Treat community-scraped SEO metrics as directional unless verified.

## Output

Competitor, authority advantage, link gap, required link strategy.


## competitor-crawl

# Competitor Crawl

Defines how to crawl and analyze competitor websites.

---

## Extract

Pages, titles, H1/H2, content depth, FAQs, schema, CTAs, trust proof, internal links, location pages, support articles.

## Compare

Find pages and sections competitors have that the client lacks.

## Output

Competitor, winning page, strength, client gap, action.


## competitor-deep-dive

# Competitor Deep Dive

Use this module when the user asks to find competitors, compare competitors, explain why competitors outrank a site, or build a competitor gap report.

## Competitor Types

Classify competitors as:

- SERP competitor: ranks in sampled search results.
- Business competitor: sells the same service/product.
- Local competitor: competes in maps or local packs.
- Content competitor: wins informational queries.
- Authority competitor: has stronger links, brand mentions, or third-party proof.
- Tool-verified competitor: confirmed by Semrush, Ahrefs, Moz, DataForSEO, GSC, or similar export.

## Evidence To Collect

For each important competitor page capture:

```text
competitor_domain
ranking_keyword
source
observed_position
ranking_url
title
h1
meta_description
word_count
schema_types
content_sections
proof_trust_signals
cta_type
internal_links_seen
backlink_authority_metrics_if_verified
gap_vs_target
confidence
```

## Deep-Dive Workflow

1. Discover competitors from SERP samples, user input, and exports.
2. Group them by service, location, and intent.
3. Crawl or inspect top ranking pages.
4. Compare page depth, title/H1 targeting, topical sections, trust proof, schema, CTAs, and internal links.
5. Separate verified ranking keywords from inferred targeted keywords.
6. Identify what Google appears to reward for each intent.
7. Recommend how to build a better page without copying competitor text.

## Gap Categories

- Missing money page.
- Weak service-page depth.
- Missing comparison/cost/process/FAQ sections.
- Weak proof, case studies, reviews, or credentials.
- Weak internal links to the target page.
- Missing schema or unclear entity signals.
- Authority/backlink gap, if verified.
- Conversion gap.

## Output

Return a competitor matrix plus action plan:

- Competitor.
- Query/intent.
- What they have.
- What target lacks.
- Recommended target page.
- Priority.
- Evidence label.


## competitor-discovery

# Competitor Discovery

Competitor discovery identifies who is actually taking the visibility the client wants.

Business competitors and SEO competitors are not always the same.

## Purpose

Answer:

```text
Who ranks for the target searches?
Who appears repeatedly?
Who dominates local/map visibility?
Who is cited by answer engines?
Which competitors should we crawl deeply?
```

## Competitor Types

```text
Direct business competitor
Local competitor
Directory/marketplace
Publisher/blog/media site
Government/association source
Review platform
YouTube/video competitor
AI-answer cited source
Course/academy competitor
SaaS/tool competitor
Ecommerce marketplace
```

## Sources

```text
User-provided competitors
Google SERP scraping
Native search
Apify SERP data
Google Maps/local pack
GSC data if available
Ahrefs/Semrush/Moz exports
AI Overview/AI Mode cited sources if available
Client reports/PDFs
```

## SERP-Based Discovery

Search:

```text
Primary money keyword
Secondary money keyword
Local service keyword
Best + service + city
Cost + service + city
Emergency + service + city
Course/category keyword
Comparison keyword
```

Record:

```text
Domain
URL
Position
Page type
Keyword appeared for
SERP feature
Local pack presence
Notes
```

## Repeat Appearance Score

```text
+3 top 3 organic position
+2 top 10 organic position
+2 local pack presence
+2 AI answer/source mention
+1 People Also Ask/source reference
+1 repeated directory dominance
```

The highest-score competitors are the deep-crawl candidates.

## Local SEO Competitors

For local businesses, separate:

```text
Map pack competitors
Organic local page competitors
Directories/review platforms
Nearby service-area competitors
```

Record:

```text
Business name
Domain
GBP category
Rating
Review count
Map visibility
Organic visibility
Strong pages
```

## Content/AEO Competitors

For informational and AI-answer visibility, identify:

```text
Blogs
Publisher sites
Forums
YouTube videos
FAQs
Knowledge bases
AI-cited sources
```

These may not sell the same thing, but they capture attention and citations.

## Qualification Rules

Deeply analyze competitors if:

```text
They rank repeatedly for target keywords.
They own high-intent pages.
They have pages the client lacks.
They dominate local map visibility.
They are cited in AI/answer results.
They have stronger content clusters.
They have stronger authority/backlinks.
```

Do not waste time deeply crawling random one-off results.

## Output Template

```text
## SEO Competitor Discovery

### Top SEO Competitors
| Competitor | Type | Appears For | Strength | Why It Matters |

### Local Competitors
| Competitor | Map/Organic Strength | Review/Category Notes |

### Content/AEO Competitors
| Source | Topic | Why It Matters |

### Deep-Crawl Candidates
1.
2.
3.

### Monitor Only
1.
2.
```

## Common Mistakes

```text
Using only client-named competitors
Ignoring directories
Ignoring map pack competitors
Ignoring repeated SERP competitors
Ignoring AI-cited sources
Analyzing too many competitors deeply
Copying competitors blindly
```

## Final Gate

Competitor discovery is complete when:

```text
Top search competitors are identified.
Types are labeled.
Strongest 3-5 are selected for deep analysis.
Local/map competitors are separated.
Content/AEO competitors are separated.
```


## competitor-matrix

# Competitor Matrix

Standard format for comparing competitors.

---

## Columns

Competitor, type, ranking strength, top pages, content depth, local strength, backlinks, schema, CTA, client gap, action.

## Use

Include in client reports and strategy plans.

## Rule

Compare what matters; do not create vanity matrices.


## content-gap-analysis

# Content Gap Analysis

Content gap analysis compares client content against search intent and competitors to find missing pages, weak pages, missing sections, trust gaps, and AEO opportunities.

It is not “competitors wrote 50 blogs, so write 50 blogs.”

## Purpose

Answer:

```text
What pages are missing?
Which existing pages are too weak?
Which sections are missing?
Which support articles should feed money pages?
Which trust proof is missing?
Which AEO/GEO answer blocks are missing?
```

## Inputs

```text
Client crawl
Competitor crawl
SERP analysis
Keyword clusters
GSC queries
People Also Ask
Related searches
Reviews/customer questions
Sales objections
Existing reports/PDFs
```

## Gap Categories

### Missing Money Page

Client lacks a high-intent landing page.

Examples:

```text
/family-dentist-arlington-heights/
/emergency-dentist-arlington-heights/
/ai-automation-course/
/ai-agents-course/
```

### Thin Money Page

Page exists but lacks:

```text
cost
process
risks/limitations
FAQs
reviews
expert credentials
local proof
schema
CTA
```

### Missing Support Article

Examples:

```text
dental implant cost
All-on-4 vs dentures
AI automation vs no-code automation
what are AI agents
best AI courses in Pakistan
```

### Missing Trust Content

```text
doctor credentials
instructor profile
case studies
student/patient testimonials
certifications
media mentions
reviews
before/after proof where compliant
```

### Missing Local Content

```text
city/service pages
NAP/location proof
review snippets
map/directions
local FAQs
nearby areas
```

### Missing AEO/GEO Content

```text
direct answers
definitions
comparison tables
cost/process/risk sections
citations/sources
entity summaries
```

## Competitor Page Comparison

For each competitor page, compare:

```text
URL
Page type
Title/H1
Content depth
Sections
FAQs
Schema
Trust proof
CTA
Internal links
Local proof
Media
Unique angle
```

Ask:

```text
What does competitor cover that client does not?
What does client cover better?
What is missing from both that we can own?
```

## Section-Level Checks

### Service Page

```text
What the service is
Who it is for
Problems/symptoms
Benefits
Process
Cost/financing
Risks/limitations
Recovery/timeline
Why choose us
Reviews
FAQs
Related services
CTA
```

### Course Page

```text
Who it is for
What you will learn
Tools covered
Projects
Curriculum
Instructor proof
Certificate value
Pricing/enrollment
Student proof
FAQs
CTA
```

### Local Page

```text
Service + city intro
NAP/location proof
Service details
Local reviews
Payment/insurance if relevant
Map/directions
Nearby areas
FAQs
CTA
```

## Support Content Mapping

Each support article must feed a money page.

Output:

```text
Article title
Target query
Supports page
Internal link anchor
Priority
```

## AEO/GEO Gap Mapping

Question sources:

```text
PAA
GSC long-tail queries
Sales questions
Customer reviews
AI-search prompts
Competitor FAQs
```

For each question:

```text
Question
Answer location
Recommended section/page
Schema if relevant
Priority
```

## Prioritization

Prioritize gaps by:

```text
Business value
Search intent
Current ranking opportunity
Competitor dominance
Conversion value
Content effort
Authority requirement
AEO/GEO potential
```

Labels:

```text
Build Now
Improve Now
Build Next
Support Later
Monitor
Ignore
```

## Output Template

```text
## Content Gap Analysis

### Missing Money Pages
| Page | Target Cluster | Why Needed | Priority |

### Existing Pages to Expand
| URL | Missing Sections | Why It Matters | Priority |

### Support Articles
| Article | Supports Page | Intent | Priority |

### Trust/E-E-A-T Gaps
| Gap | Affected Pages | Fix |

### AEO/GEO Gaps
| Question/Section | Target Page | Fix |

### Internal Linking Actions
| From Page | To Page | Anchor |
```

## Page Brief From Gap

```text
Recommended URL:
Primary keyword:
Secondary keywords:
Intent:
Title:
Meta:
H1:
Required sections:
FAQs:
Trust proof:
Internal links:
Schema:
CTA:
Word count range:
Notes:
```

## Common Mistakes

```text
Random blogs
Copying competitor pages
Thin city doorway pages
No support-to-money links
No trust proof
No conversion
No AEO questions
Ignoring SERP page type
```

## Final Gate

Content gap analysis is complete when:

```text
Missing money pages are listed.
Weak pages have exact section fixes.
Support articles are mapped to money pages.
Trust gaps are identified.
AEO/GEO answer gaps are identified.
Internal links are planned.
Priorities are clear.
```


## serp-gap-analysis

# SERP Gap Analysis

SERP gap analysis shows what search engines currently reward for target keywords.

## Purpose

Answer:

```text
What page type is ranking?
Which competitors are winning?
What content/format does the SERP expect?
Are there local/map features?
Are there PAA or AI answer opportunities?
What should the client build or improve?
```

## Inputs

```text
Target keyword list
Apify Google SERP scraper
Native search
GSC queries
Rank tracking exports
Competitor URLs
Location/country/device
PAA/related search data
AI Overview/AI Mode data if available
```

## SERP Fields

```text
Query
Country
City/location
Language
Device
Date
Top organic URLs
Domains
Titles
Snippets
Page type
Local pack presence
Ads presence
People Also Ask
Related searches
Featured snippet
Video results
Directory results
AI Overview/AI Mode presence
AI cited sources
```

## Page Type Classification

```text
Homepage
Service page
Location page
Category page
Product page
Course page
Blog/article
Comparison page
Cost page
Directory/listing
Review platform
Video
Forum/community
Government/association
Tool/calculator
AI answer/source
```

## Intent Reading

If SERP shows service pages:

```text
Create/improve service page.
```

If SERP shows local pack:

```text
Local landing page + GBP optimization.
```

If SERP shows blogs/guides:

```text
Support article or guide.
```

If SERP shows directories:

```text
Website SEO + directory/citation strategy.
```

If SERP shows comparison pages:

```text
Create comparison content.
```

If SERP shows videos:

```text
Create video + transcript + VideoObject schema.
```

## SERP Features and Actions

```text
PAA → answer blocks, FAQ, support content.
Local pack → GBP, reviews, local landing pages.
AI Overview/AI Mode → entity clarity, source-worthy content, schema.
Ads → commercial intent confirmation.
Directories → claim/optimize profiles and build stronger trust pages.
Reviews → review strategy and trust proof.
```

## Competitor SERP Spread

Track for each competitor:

```text
Top 3 appearances
Top 10 appearances
Top 20 appearances
Local pack appearances
AI source appearances
```

Output:

```text
Competitor
Queries appeared
Best rank
Winning page types
Strength
Weakness
Action
```

## SERP Gap Types

```text
Page gap: client lacks winning page type.
Content depth gap: page exists but is weaker.
Local trust gap: GBP/reviews/citations are weak.
Authority gap: competitors have stronger links.
SERP feature gap: PAA/video/AI feature exists.
Conversion gap: competitors convert better.
```

## Output Template

```text
## SERP Gap Analysis

| Query | Intent | SERP Pattern | Winning Page Type | Client Gap | Required Action |

### Repeated Competitors
| Competitor | Appears For | Winning Pages | What To Learn |

### PAA / AEO Questions
| Question | Target Page/Section | Priority |

### Required New Pages
| Page | Keywords | Why | Priority |

### Existing Pages to Improve
| Page | SERP Gap | Fix | Priority |
```

## Local SERP Handling

For local keywords, always record:

```text
Organic top 10
Map/local pack
Directories
Review platforms
City modifiers
Near-me intent
GBP competitors
```

Website pages alone may not reach query targets when local pack dominates.

## AEO/GEO Handling

If AI Overview/AI Mode data exists, record:

```text
Is AI answer present?
Which brands are mentioned?
Which sources are cited?
What format is cited?
What information is missing from client site?
```

Action:

```text
Create citation-worthy answer sections, entity pages, and supporting content.
```

## Common Mistakes

```text
Analyzing volume without SERP
Assuming one page type for all queries
Ignoring local pack
Ignoring directories
Ignoring PAA
Ignoring AI answers
Ignoring ads as commercial-intent signal
Copying competitor content
```

## Final Gate

SERP analysis is complete when each target query has:

```text
Intent
SERP pattern
Winning page type
Competitor examples
Client gap
Recommended action
Priority
```


## service-page-gap-analysis

# Service Page Gap Analysis

Finds service, product, course, and location pages competitors have but the client lacks.

---

## Checks

Dedicated service pages, sub-service pages, cost pages, comparison pages, location pages, FAQs, schema, CTAs.

## Action

Build or improve missing high-intent pages.

## Output

Missing page, target keyword, competitor proof, priority.
