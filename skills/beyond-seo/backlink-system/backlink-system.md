# Backlink System

Use the contents below to select the relevant workflow; load only the needed sections.


## anchor-text-strategy

# Anchor Text Strategy

This file defines safe anchor text planning for Beyond SEO backlink campaigns.

---

## 1. Anchor Types

```text
Brand anchor: BeyondTahir Academy
Naked URL: https://academy.beyondtahir.com
Partial-match: AI automation course by BeyondTahir
Topical: learn AI automation
Generic/contextual: this guide, here, full breakdown
Exact-match: AI automation course Pakistan
```

---

## 2. Recommended Mix

```text
Brand: 35-45%
Naked URL: 20-30%
Partial-match: 15-25%
Topical/generic: 10-20%
Exact-match: 0-5%
```

Adjust by niche risk and current anchor profile.

---

## 3. Rules

```text
Never repeat exact-match anchors across many posts.
Use exact match only on strong relevant pages.
Use branded anchors for free post/library links.
Use partial-match anchors for support articles.
Use natural sentence anchors for guest posts.
```

---

## 4. Output Template

```text
Target page:
Anchor type:
Suggested anchor:
Reason:
Risk:
```


## backlink-audit

# Backlink Audit

This file defines how Beyond SEO audits backlinks and authority.

Backlinks are not counted equally. One relevant local/niche link can be more valuable than dozens of generic low-quality links.

---

## 1. Purpose

Backlink audit answers:

```text
How strong is the site authority?
Are links relevant and safe?
What link gap exists against competitors?
Which links should be built next?
Which links should be avoided?
```

---

## 2. Inputs

Use any available:

```text
Ahrefs export/screenshot
Semrush export
Moz export
Apify Ahrefs/Semrush/Moz-style actors
GSC links export
Backlink sheet
Competitor backlink exports
Manual public checks
Paid backlink offers
```

If only community actor data is available, label it directional.

---

## 3. Metrics to Review

```text
Domain authority/DR/DA/AS
Referring domains
Backlinks
Dofollow/nofollow ratio
Anchor distribution
Top linked pages
Lost links
New links
Country relevance
Niche relevance
Spam/toxic risk
Organic traffic estimate of linking sites
Outbound link pattern
Competitor gap
```

---

## 4. Quality Signals

Good link:

```text
relevant niche or local source
indexed page
real organic footprint
editorial context
natural anchor
real audience
low outbound spam
```

Weak/risky link:

```text
irrelevant high-DA site
obvious link farm
expired-domain network
same anchor repeated
thin spun content
site sells every niche
no organic footprint
hidden/footer/sidebar spam
```

---

## 5. Anchor Distribution

Recommended safe mix:

```text
brand anchors
naked URLs
partial-match anchors
topical natural anchors
a few exact-match anchors only where natural
```

Red flag:

```text
too many exact-match commercial anchors
```

---

## 6. Link Gap Analysis

Compare client with competitors:

```text
referring domains
authority quality
local/niche links
directory/citation coverage
PR/editorial links
top linked pages
anchor pattern
```

Output:

```text
How many quality links are needed
Which types matter most
Which pages need links
Which competitor links can be replicated
```

---

## 7. Output Template

```text
## Backlink Audit

### Authority Summary
[summary]

### Link Quality Findings
| Finding | Evidence | Impact | Action |

### Competitor Link Gap
| Competitor | Strength | Replicable Opportunities |

### Priority Link Plan
1.
2.
3.

### Risk Notes
[spam/anchor/paid link risk]
```


## backlink-outreach-prompts

# Backlink Outreach Prompts

This file gives Beyond SEO safe outreach templates for link building.

---

## 1. Local Sponsorship Outreach

```text
Subject: Sponsorship / local resource opportunity

Hi [Name],

We are interested in supporting [event/community/resource]. If there is a sponsor or partner page, please share the details and requirements.

Our website: [URL]
Relevant page: [target page]

Thank you,
[Name]
```

---

## 2. Guest Article Outreach

```text
Subject: Article idea for [Site]

Hi [Name],

I wanted to suggest a practical article for your readers: [topic]. It would cover [brief value] and be written specifically for [audience].

If you accept guest contributions, I can send an outline first.

Best,
[Name]
```

---

## 3. Resource Page Outreach

```text
Subject: Useful resource for your [topic] page

Hi [Name],

I found your resource page on [topic]. We recently published [resource], which may help readers looking for [specific benefit].

Here is the link: [URL]

If useful, feel free to include it.

Thanks,
[Name]
```

---

## 4. Rules

```text
Personalize outreach.
Do not spam.
Do not promise payment unless approved.
Do not use misleading claims.
Track status.
Follow up once or twice max.
```


## backlink-quality-scoring

# Backlink Quality Scoring

This file defines a scoring system for backlink opportunities.

Beyond SEO must never recommend a link only because DA/DR is high.

---

## 1. Scorecard

Score each opportunity out of 100.

```text
Niche relevance: 20
Local/country relevance: 15
Organic traffic/visibility: 15
Page quality/context: 15
Authority metric: 10
Outbound link cleanliness: 10
Indexability: 5
Anchor safety: 5
Price fairness: 5
```

---

## 2. Verdicts

```text
80-100: Strong opportunity
65-79: Good if price/anchor is safe
50-64: Use cautiously / branded anchor only
30-49: Low value / avoid unless citation needed
0-29: Avoid
```

---

## 3. Required Fields

```text
Prospect URL
Domain
Type
Free/Paid
Niche relevance
Local relevance
Authority metric
Traffic estimate
Outbound link risk
Indexability
Anchor suggestion
Target page
Price
Score
Verdict
Notes
```

---

## 4. Anchor Safety

Lower score if:

```text
exact-match anchor required
site already has many paid anchors
target page is unrelated
same anchor used repeatedly in campaign
```

---

## 5. Price Fairness

Paid link is not worth buying if:

```text
no relevance
no organic footprint
obvious link farm
price is high only because of fake DA
placement is in weak article with many outgoing links
```

---

## 6. Output Template

```text
Backlink Score:
Verdict:
Why:
Best target page:
Best anchor:
Risk:
Negotiation note:
```


## digital-pr-system

# Digital PR System

Digital PR workflow for earning authority links and mentions.

---

## Angles

Founder story, research data, local impact, industry commentary, case studies, awards, reports.

## Targets

News sites, industry blogs, local press, podcasts, interviews, association publications.

## Output

PR angle, target list, pitch, link target, success metric.


## free-backlink-posting

# Free Backlink Posting System

This file defines how Beyond SEO should use free article-posting and community platforms safely.

It builds on `free-paid-backlink-source-library.md` and `backlink-source-database.csv`.

---

## 1. Purpose

Free posting is useful for:

```text
entity building
support article distribution
topical relevance
brand mentions
indexable support content
referral traffic
internal campaign footprint
```

It is not a replacement for real authority links.

---

## 2. Supported Source Types

From the uploaded backlink library:

```text
Medium
Dev.to
Forem communities
Substack
Blogspot
WebYourself / similar web publishing platforms
```

---

## 3. Category Matching

Choose sources by topical category.

```text
AI assistants/agents → agent/tool pages
Writing/content → prompt/content pages
Design/art → design tool pages
Video/animation → video AI pages
Voice/music → voice/audio AI pages
Coding/development → no-code/vibe coding/dev pages
Business/productivity → automation/business pages
Lifestyle → general AI adoption pages
Experimental → future tools/research pages
```

---

## 4. Posting Rules

```text
Every post must be unique.
Every post must be useful standalone content.
Use 1 contextual money-page link maximum.
Use 1 brand or homepage link if natural.
Do not post same article across platforms.
Do not repeat exact-match anchors.
Do not link only to homepage.
Track every post in a sheet.
```

---

## 5. Article Structure

```text
Title
Intro with real problem
Tool/topic explanation
5-7 useful points
Example/use case
Soft CTA
Contextual link
Author/brand mention
```

---

## 6. Anchor Examples

Safe:

```text
BeyondTahir Academy
AI automation course by BeyondTahir Academy
learn AI automation
this AI agents guide
academy.beyondtahir.com
```

Risky if repeated:

```text
best AI automation course Pakistan
best AI agents course Pakistan
cheap SEO backlinks
```

---

## 7. Output Template

```text
Source:
Platform:
Category:
Suggested article title:
Target page:
Anchor:
Secondary link:
Risk level:
Status:
```


## free-paid-backlink-source-library

# Free + Paid Backlink Source Library

This file converts the uploaded backlink document into a structured Beyond SEO source library.

The uploaded sheet contains **free article-post backlink assets** grouped into topical categories such as AI Assistants & Agents Tools, Writing & Content Creation, Design/Art/Creativity, Video & Animation, Voice/Sound/Music, Coding & Development, Business & Productivity, Everyday & Lifestyle, and Other/Experimental.

Beyond SEO must use these sources as **seed assets and posting-pattern examples**, not as a spam list.

---

## 1. How to Use This Library

Use this library when the user asks for:

```text
free backlinks
free posting sites
article backlinks
Medium backlinks
Dev.to backlinks
Forem backlinks
Substack backlinks
Blogspot backlinks
AI tool backlink plan
support article backlinks
entity-building links
```

The skill should suggest sources from this database only after checking:

```text
niche relevance
indexability
content uniqueness
anchor-text safety
target page relevance
whether the post is already published or needs a fresh post
```

---

## 2. Source Database

| Category | Platform | Type | URL | Best Use |
|---|---|---|---|---|
| AI Assistants & Agents Tools | Medium | Free article post | https://medium.com/@sahilchandio2004/top-5-super-simple-ai-assistants-agents-tools-anyone-can-use-8731b0244336 | AI assistants/agents support article |
| AI Assistants & Agents Tools | Medium | Free article post | https://medium.com/@sahilchandio860/top-5-next-level-ai-agents-tools-kids-love-too-50f4e7529b69?postPublishedType=initial | AI agents/tools support article |
| AI Assistants & Agents Tools | Forem | Free article post | https://open.forem.com/skye_wright_1443d44f7b6d1/top-5-more-easy-ai-agents-tools-for-fun-work-4f7a | AI agents/tools support article |
| Writing & Content Creation | Dev.to | Free article post | https://dev.to/skye_wright_1443d44f7b6d1/top-5-best-ai-tools-for-writing-content-creation-1bl2 | Writing/content support article |
| Writing & Content Creation | Forem | Free article post | https://future.forem.com/skye_wright_1443d44f7b6d1/5-best-ai-copywriting-tools-that-dont-suck-in-2026-1a8c | Copywriting/content support article |
| Writing & Content Creation | Dev.to | Free article post | https://dev.to/sahil_vvvchandio_3b863/top-5-ai-blog-writing-tools-to-crush-deadlines-2026-4ck2 | AI blog writing support article |
| Design, Art & Creativity | Forem | Free article post | https://open.forem.com/sahil_vvvchandio_3b863/top-5-best-ai-tools-for-design-2cgo | AI design support article |
| Design, Art & Creativity | Forem | Free article post | https://future.forem.com/sahil_vvvchandio_3b863/5-best-ai-tools-design-art-creativity-flux-canva-2026-em1 | AI design/art support article |
| Design, Art & Creativity | Forem | Free article post | https://vibe.forem.com/sahil_vvvchandio_3b863/best-5-ai-for-easy-designs-no-skills-needed-59i0 | AI design support article |
| Video & Animation | Forem | Free article post | https://vibe.forem.com/skye_wright_1443d44f7b6d1/best-ai-for-easy-video-editing-animation-2026-fe6 | AI video support article |
| Video & Animation | Forem | Free article post | https://zeroday.forem.com/skye_wright_1443d44f7b6d1/top-5-free-ai-video-makers-from-idea-to-viral-clip-1pfn | AI video maker support article |
| Video & Animation | Forem | Free article post | https://zeroday.forem.com/sahil_vvvchandio_3b863/5-ai-tools-to-animate-videos-like-a-pro-in-seconds-12la | AI animation support article |
| Voice, Sound & Music | Forem | Free article post | https://design.forem.com/skye_wright_1443d44f7b6d1/5-ai-tools-that-make-pro-music-from-text-in-seconds-57op | AI music support article |
| Voice, Sound & Music | Forem | Free article post | https://design.forem.com/sahil_vvvchandio_3b863/top-5-free-ai-sound-tools-create-hits-without-skills-4agj | AI sound/music support article |
| Voice, Sound & Music | WebYourself | Free article post | https://webyourself.eu/posts/1725930 | Voice/sound support post |
| Coding & Development | Substack | Free article post | https://open.substack.com/pub/sahilchandio/p/5-ai-tools-that-code-10x-faster-for?r=6d2z96&utm_campaign=post&utm_medium=web&showWelcomeOnShare=true | AI coding support article |
| Coding & Development | Substack | Free article post | https://open.substack.com/pub/sahilchandio1/p/top-5-free-ai-dev-tools-from-noob?r=6x2iys&utm_campaign=post&utm_medium=web&showWelcomeOnShare=true | AI dev tools support article |
| Coding & Development | Blogspot | Free article post | https://beyondtool.blogspot.com/2026/01/best-ai-coding-assistants-write-bug.html | AI coding assistant support article |
| Business & Productivity | Medium | Free article post | https://medium.com/@sahilchandio2004/top-5-free-ai-productivity-hacks-every-team-needs-e72037ac2097 | AI productivity support article |
| Business & Productivity | Medium | Free article post | https://medium.com/@sahilchandio860/5-ai-tools-that-slash-work-hours-by-50-2026-tested-52b2bcf86bda | AI productivity support article |
| Business & Productivity | Substack | Free article post | https://open.substack.com/pub/sahilchandio/p/best-ai-for-business-save-hours-on?r=6d2z96&utm_campaign=post&utm_medium=web&showWelcomeOnShare=true | AI business support article |
| Everyday & Lifestyle | Medium | Free article post | https://medium.com/@sahilchandio2004/5-ai-tools-to-crush-your-daily-chaos-in-minutes-4c420a39a02d | AI lifestyle support article |
| Everyday & Lifestyle | Medium | Free article post | https://medium.com/@sahilchandio860/lazy-hack-5-ai-tricks-for-effortless-days-db15a416315d?postPublishedType=repub | AI lifestyle support article |
| Everyday & Lifestyle | Forem | Free article post | https://open.forem.com/skye_wright_1443d44f7b6d1/transform-mornings-top-5-ai-hacks-for-busy-lives-h45 | AI lifestyle support article |
| Other / Experimental | Forem | Free article post | https://open.forem.com/sahil_vvvchandio_3b863/unlock-5-bold-ai-tools-for-next-level-experiments-1lmf | AI experimental support article |
| Other / Experimental | Dev.to | Free article post | https://dev.to/skye_wright_1443d44f7b6d1/5-experimental-ai-tools-that-redefine-your-work-in-2026-2n48 | AI experimental support article |
| Other / Experimental | Forem | Free article post | https://vibe.forem.com/skye_wright_1443d44f7b6d1/5-pro-ai-tools-pushing-boundaries-tested-for-2026-3fmo | AI experimental support article |

---

## 3. Platform Rules

### Medium

Best for:

```text
brand/entity support
thought leadership
course/tool summaries
support articles that link to money pages
```

Rules:

```text
Use unique content.
Use 1 contextual money-page link maximum.
Add 1 brand/homepage or author link if natural.
Avoid repeated exact-match anchors.
Do not repost identical content across accounts.
```

### Dev.to

Best for:

```text
technical AI, coding, automation, development, SaaS, tools
```

Rules:

```text
Keep content practical and technical.
Use examples/code/workflow where possible.
Avoid thin listicles.
Link naturally to relevant tool/course/resource pages.
```

### Forem Communities

Best for:

```text
AI tools
creative tools
video tools
design tools
experimental tech
community discovery
```

Rules:

```text
Match the community topic.
Do not post the same article everywhere.
Use varied titles, intros, examples, and links.
Check whether the community allows external links.
```

### Substack

Best for:

```text
newsletter-style authority
founder thought leadership
AI education
business/productivity articles
```

Rules:

```text
Use it like a publication, not a link dump.
Build topical sequence.
Link to landing pages only where context is strong.
```

### Blogspot / Other Web 2.0

Best for:

```text
supporting entity footprint
older long-form support content
low-risk branded support links
```

Rules:

```text
Use cautiously.
Keep branded or natural anchors.
Do not overuse.
Never depend on these as the only authority strategy.
```

---

## 4. Anchor Text Rules for This Library

Preferred anchor mix:

```text
40% brand anchors
25% URL/naked anchors
20% partial-match anchors
10% topical/generic anchors
5% exact-match anchors maximum, only where natural
```

Examples:

```text
BeyondTahir Academy
academy.beyondtahir.com
AI automation course by BeyondTahir Academy
learn AI automation
this AI automation guide
```

Avoid:

```text
best AI automation course Pakistan
best prompt engineering course Pakistan
best AI tools directory
```

if repeated across many posts.

---

## 5. Source Selection Logic

When suggesting free backlink posts, Beyond SEO must choose by category.

```text
AI agents page → AI Assistants & Agents Tools sources
Prompt/course page → Writing, Coding, Business sources
Design tools page → Design/Art/Creativity sources
Video tools page → Video & Animation sources
AI coding page → Coding & Development sources
Business automation page → Business & Productivity sources
General brand/entity → Medium/Substack/Blogspot sources
```

---

## 6. Free vs Paid Handling

This file mainly contains free/article-post seed assets. For paid backlinks, Beyond SEO must use `paid-backlink-evaluation.md` before recommending purchase.

Never mix:

```text
free support post
paid guest post
sponsored link
niche edit
PBN
citation
PR article
```

Each has different risk.

---

## 7. Output When User Asks for Free Backlinks

Use this template:

```text
Recommended source:
Platform:
Category fit:
Suggested article topic:
Target page:
Anchor suggestion:
Risk level:
Notes:
```

---

## 8. Non-Negotiables

Do not:

```text
create duplicate articles
blast same anchor everywhere
link only to homepage
use exact-match anchors repeatedly
claim these links alone will rank a site
call every free post a high-authority backlink
ignore relevance
```

Use this library as a controlled support layer, not the full authority strategy.


## guest-posting-system

# Guest Posting System

Safe guest posting workflow for backlinks and authority.

---

## Prospecting

Find relevant niche, local, industry, and editorial sites.

## Quality Checks

Relevance, traffic, indexability, outbound link pattern, editorial quality, price, anchor risk.

## Output

Prospect, topic, anchor, target page, risk, verdict.


## link-gap-analysis

# Link Gap Analysis

This file defines how Beyond SEO compares backlink authority against competitors.

---

## 1. Purpose

Link gap analysis answers:

```text
What links do competitors have that we do not?
Which are replicable?
Which link categories matter most?
How many quality links are needed?
```

---

## 2. Competitor Link Categories

```text
local citations
directories
associations
PR/media
sponsorships
partner/vendor links
guests posts
resource pages
profiles
reviews/platforms
industry tools/listings
```

---

## 3. Replication Priority

Prioritize:

```text
1. Same local/niche associations
2. Real directory/citation profiles
3. Partner/vendor listings
4. Community sponsorships
5. PR/editorial links
6. Guest articles on relevant sites
7. Free post support layer
```

---

## 4. Output Template

```text
Competitor:
Link type:
Source URL:
Replicable? Yes/No
Client target page:
Suggested anchor:
Priority:
Risk:
```


## niche-edit-evaluation

# Niche Edit Evaluation

Evaluates paid or negotiated niche edit placements.

---

## Checks

Existing page relevance, indexability, organic traffic, outbound links, anchor fit, editorial quality, history, price.

## Verdicts

Buy, Avoid, Negotiate, Branded anchor only, Nofollow/sponsored, Need more data.

## Rule

Avoid irrelevant high-DA link farms.


## paid-backlink-evaluation

# Paid Backlink Evaluation

This file defines how Beyond SEO evaluates paid backlink opportunities.

Paid links carry risk. The skill must not blindly recommend buying links.

---

## 1. When to Use

Use when user asks:

```text
Should I buy this backlink?
Is this guest post worth it?
Is this paid link safe?
What price should I pay?
Which anchor should I use?
```

---

## 2. Required Inputs

```text
Placement domain
Placement page if available
Price
Niche
Target page
Proposed anchor
Country/market
Metrics if provided
```

If missing, still evaluate what is visible and mark unknowns.

---

## 3. Checks

```text
Niche relevance
Country/local relevance
Organic traffic estimate
Indexed pages
Authority metric
Outbound link pattern
Recent posts quality
Sponsored/link-selling footprint
Anchor risk
Target page fit
Price fairness
```

---

## 4. Verdicts

```text
Buy
Avoid
Negotiate
Use branded anchor only
Use nofollow/sponsored
Need more data
```

---

## 5. Anchor Rules

Use exact-match only rarely.

Prefer:

```text
brand
naked URL
partial-match
natural sentence anchor
```

---

## 6. Output Template

```text
Verdict:
Score:
Reason:
Risk level:
Best anchor:
Best target page:
Price note:
Safer alternative:
```

---

## 7. Avoid If

```text
irrelevant niche
no organic traffic
obvious link farm
same site sells casino/crypto/adult/health/everything
hundreds of outbound paid links
exact-match anchor required
price based only on fake DA
```


## toxic-link-risk

# Toxic Link Risk

This file defines how Beyond SEO identifies risky backlinks.

---

## 1. Risk Signals

```text
irrelevant niche
spammy outbound links
casino/adult/pills mixed with unrelated niches
thin AI-spun articles
expired-domain network footprints
same IP/CMS/template patterns
exact-match anchors at scale
foreign-language irrelevant pages
no organic visibility
indexed but no real audience
```

---

## 2. Risk Levels

```text
Low: relevant and natural
Medium: weak but not dangerous
High: spammy or unnatural
Critical: manual-action style risk pattern
```

---

## 3. Actions

```text
Ignore low-value harmless links.
Avoid building more similar links.
Request removal only for serious risk.
Use disavow only with strong evidence and expert review.
```

Do not overuse disavow.

---

## 4. Output Template

```text
Risk:
Evidence:
Recommended action:
Do we need disavow? Yes/No/Expert review needed
```
