# Aeo Geo

Use the contents below to select the relevant workflow; load only the needed sections.


## aeo-content-writing-persona

# AEO Content Writing Persona

AEO means Answer Engine Optimization.

The job:

```text
Make the content become the answer.
```

This file tells the AI agent how to write or rewrite any page, blog, FAQ, service page, course page, or article in an answer-engine-friendly style.

---

## 1. When to Use

Use this file when the user asks:

```text
Write AI-friendly content
Make this AEO optimized
Make this answer engine optimized
Rewrite this for Google AI / ChatGPT / Perplexity
Create content that becomes the answer
```

---

## 2. Persona

Write like:

```text
A clear expert who answers first, explains second, proves third, and sells last.
```

Tone:

```text
Simple
Clear
Direct
Helpful
Evidence-aware
Balanced
Human
Easy for AI to extract
```

---

## 3. AEO Writing Formula

Use this order:

```text
1. Direct answer in 40-80 words
2. Context
3. Step-by-step explanation
4. Examples
5. Comparison
6. Proof
7. Risks / limitations
8. FAQs
9. Next step
```

---

## 4. Bad vs Good

Bad:

```text
In today's digital world, every business needs AI...
```

Good:

```text
A practical AI course is one that teaches you to build real workflows, agents, and business systems. Before choosing a course, check the instructor, projects, certificate verification, student reviews, support system, and whether the course teaches implementation instead of theory only.
```

---

## 5. Required AEO Blocks

For any important page, add:

```text
Short answer block
Definition block
Step-by-step block
Cost / effort block
Comparison block
Proof block
Limitations block
FAQ block
CTA block
```

---

## 6. AEO Content Brief Template

```text
Page:
Target question:
Short answer:
Required sections:
Proof needed:
FAQs:
Schema:
Internal links:
External proof links:
CTA:
```

---

## 7. Apify Inputs

Use Apify to collect:

```text
People Also Ask
Related queries
SERP snippets
Competitor FAQ sections
Reviews and review questions
Community questions
AI Overview / AI Mode checks where supported
```

---

## 8. Quality Gate

AEO content is ready when:

```text
The answer appears early.
The page answers related questions.
The proof is visible.
The structure is easy to extract.
The page has schema where valid.
The CTA is clear.
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


## ai-friendly-seo-master-workflow

# AI-Friendly SEO Master Workflow

This file activates when a user says:

```text
AI-friendly SEO
AEO
GEO
AI search optimization
Make my website ready for ChatGPT / Gemini / Perplexity / Google AI
Make my brand appear in AI answers
Answer engine optimization
Generative engine optimization
Entity SEO
Reputation SEO
Conversation SEO
```

The goal is to audit normal SEO plus AI-search readiness and produce a practical report.

---

## 1. Simple Meaning for Agents

When a user asks for AI-friendly SEO, do not treat it as only keywords.

Run this combined system:

```text
Traditional SEO
AEO: become the answer
GEO: become a source AI can mention or cite
Entity SEO: make the brand/person/company clear
Reputation SEO: prove trust with reviews, media, profiles, proof
Conversation SEO: answer the full human decision question
```

For Google Search, AEO and GEO are still SEO. The work is not to chase hacks; it is to make crawlable, indexed, useful, unique, expert-led content easier for search systems and AI features to understand, retrieve, summarize, trust, and cite.

Do not present AI-friendly SEO as a guaranteed way to appear in AI Overviews, AI Mode, ChatGPT, Gemini, Perplexity, or any other answer system.

---

## 2. Default Apify-First Flow

Use Apify first.

Required default check:

```text
APIFY_API_TOKEN
```

Do not ask for many APIs up front.

Apify should be used for:

```text
Website crawl
Competitor crawl
Google SERP checks
People Also Ask / related queries
Google Trends
Google Maps / Places
Google reviews
PageSpeed / Lighthouse actors
AI Overview / AI Mode checks where supported
Search Console Search Generative AI performance reports where available
Third-party mentions
Social profile checks
Backlink / authority checks
GSC/GA4 connector or export actors where available
```

If Apify cannot collect a metric, label it missing or ask for an export later.

If Search Console generative AI performance reports are available, use them as the strongest first-party evidence for Google AI visibility. Track AI feature impressions, surfaced pages, countries, devices, and dates. If they are not available, say so and do not invent AI visibility.

---

## 3. AI-Friendly SEO Audit Steps

### Step 1: Capability Check

```text
Is APIFY_API_TOKEN available?
Can Apify actors run?
What is the website URL?
What is the target country/city?
What is the business goal?
```

### Step 2: Normal SEO Baseline

Check:

```text
Crawlability
Indexability
Sitemap / robots
Metadata
H1/H2
Content depth
Schema
Internal links
Page speed
Conversion path
Keywords
Competitors
Backlinks / authority
Local SEO if relevant
```

### Step 3: AEO Audit

Check if pages:

```text
Answer direct questions early
Use clear headings
Include definitions
Include steps
Include cost/process/risk sections
Include comparison tables
Include FAQs based on real questions
Use proof and expert notes
```

### Step 4: GEO Audit

Check if pages are source-worthy:

```text
Clear claims
Clear entity
Original proof
Fresh information
Author/expert identity
External proof links
Structured data
Balanced comparison
No fake hype
```

Also check whether content is non-commodity:

```text
Original examples
First-hand experience
Expert explanation
Real data or proof
Specific process details
Clear limitations or risks
Useful images/video where relevant
```

### Step 5: Entity SEO Audit

Check if the website clearly explains:

```text
Who the person/brand/company is
What they do
Where they operate
Why they are trusted
Which profiles belong to them
Which reviews/media/certificates prove them
```

### Step 6: Reputation SEO Audit

Check:

```text
Google reviews
Trustpilot
LinkedIn
Facebook
YouTube
Clutch/G2/Capterra if relevant
Media mentions
Third-party articles
Student/customer proof
Case studies
Website review/proof pages
```

### Step 7: Conversation SEO Audit

For every money keyword, convert it into a full human question.

Example:

```text
Keyword: AI course
Conversation: Which AI course is trusted, practical, affordable, and can help me earn?
```

Then check if the website answers that complete question.

---

## 4. AI-Friendly SEO Report Structure

Use this report when the user asks for AI-friendly SEO:

```text
1. Audit Mode and Data Sources
2. Executive Summary
3. Traditional SEO Health
4. AEO Score: Can content become the answer?
5. GEO Score: Can AI cite or mention the brand?
6. Entity SEO Score: Does Google/AI understand who this is?
7. Reputation SEO Score: Is there enough proof?
8. Conversation SEO Score: Does content answer real human questions?
9. Apify Findings
10. Competitor / AI Visibility Gap
11. Pages to Create
12. Pages to Improve
13. Schema and Entity Fixes
14. Review / Reputation / Third-Party Authority Plan
15. 30-Day AI-Friendly SEO Plan
16. 60-Day Authority + Content Plan
17. 90-Day Growth Plan
18. Missing Data
```

---

## 5. Scoring Model

Score out of 100:

```text
Technical SEO: 15
Content / On-page: 15
AEO Readiness: 15
GEO / Source-worthiness: 15
Entity SEO: 15
Reputation Proof: 10
Conversation SEO: 10
Conversion / Tracking: 5
```

If local SEO is critical, include local SEO inside Entity + Reputation + Conversion.

---

## 6. Output Rule

Never say:

```text
This guarantees Google AI will show you.
This guarantees ChatGPT will mention you.
```

Say:

```text
This improves the probability that search engines and AI-answer systems can understand, trust, summarize, mention, or cite the brand.
```

Do not recommend these as Google AI visibility requirements:

```text
llms.txt
Special AI-only schema
Artificial chunking
Mass query-variant pages
Inauthentic third-party mentions
Bot-first rewrites
```

These may be discussed only when a non-Google platform specifically uses them, and the limitation must be stated.

---

## 7. Final Action Plan

Every AI-friendly SEO report must end with exact actions:

```text
Create these entity pages
Create these answer blocks
Create these reputation/proof pages
Create these third-party articles
Add these schema types
Fix these SEO blockers
Improve these conversion paths
Build these backlinks/profiles
Track these AI/search KPIs
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


## ai-overview-opportunity-audit

# AI Overview Opportunity Audit

Audits opportunities to appear in Google AI Overviews or AI search-style answers where supported.

---

## Checks

AI answer presence, cited sources, mentioned brands, source patterns, missing entity proof, missing answer blocks.

## Actions

Create direct answers, definitions, comparison tables, cost/process/risk sections, expert proof, citations, schema, and source-worthy pages.

## Caution

Do not guarantee AI Overview inclusion.


## ai-search-readiness

# AI Search Readiness

This file teaches Beyond SEO how to audit whether a website is ready for AI-powered search, AI Overviews, AI Mode, ChatGPT/Perplexity/Copilot/Gemini-style search, and answer engines.

## Purpose

AI Search Readiness answers:

```text
Can AI systems understand who this brand is, what it offers, where it operates, why it is trusted, and which pages should answer which questions?
```

AI search readiness is not a trick. It is built from crawlable SEO, entity clarity, answer clarity, trust proof, topical authority, citations, structured data, and external authority.

## Inputs

Use any available:

```text
Website crawl
Rendered/source HTML
SERP data
AI Overview / AI Mode data where available
Apify SERP/AI actors
Native AI-search checks
GSC long-tail queries
Competitor pages
Schema output
Author/expert pages
Backlink/mention data
Google Business Profile data
```

If no AI-search checking is available, label the audit as `Readiness Only`.

## Readiness Checklist

### Crawlability

```text
Important pages indexable
Important content present in HTML/rendered output
No money pages empty because of JavaScript
Unique title/meta/H1
Sitemap includes important pages
```

### Entity clarity

```text
Brand/business name clear
Organization details clear
Founder/expert/doctor/instructor visible
Services/products/courses clearly defined
Location/service area clear where local
sameAs profiles and schema used where useful
```

### Answer clarity

```text
Direct answers
Definitions
Process sections
Cost/pricing sections
Risk/limitation sections
Comparison sections
FAQs based on real questions
```

### Trust and source-worthiness

```text
Credentials
Reviews/testimonials
Case studies/examples
Citations/sources where needed
Policies/contact info
YMYL disclaimers where needed
External mentions/backlinks
```

### Structure

```text
Logical headings
Tables/lists/checklists
Schema
Internal links
Breadcrumbs
Freshness/update dates where useful
```

## AI Query Testing

If tools allow, test:

```text
Who is [brand/person]?
Best [service/course/product] in [location]
How much does [service] cost?
[service/course/product] vs [alternative]
How to choose [provider/course]?
What is [topic]?
[topic] for [profession]
```

Record:

```text
Query
AI answer present?
Brand mentioned?
Competitors mentioned?
Sources cited?
Which pages cited?
Narrative gap
Recommended action
```

## Visibility Labels

Use:

```text
Verified Mention
Verified Citation
Competitor Mention
Source Gap
Not verified
Readiness Only
```

## Scoring

Score out of 100:

```text
Crawlability: 20
Entity clarity: 20
Answer clarity: 20
Trust/source-worthiness: 20
Structure/schema/internal links: 10
Original value/freshness: 10
```

## Output Template

```text
## AI Search Readiness Audit
Audit Mode:
Score:
Main Gaps:
AI Query Test Results:
Pages to Improve:
Pages to Create:
Schema / Entity Fixes:
30-Day Plan:
Missing Data:
```

## Common Mistakes

Do not promise AI Overview inclusion. Do not claim ChatGPT/Perplexity/Gemini mentions without checking. Do not treat FAQs as the whole AEO strategy. Do not ignore crawlability, entity clarity, trust, or source-worthiness.


## answer-engine-optimization

# Answer Engine Optimization

AEO makes content answer direct user questions clearly enough for search engines, AI assistants, featured snippets, People Also Ask, voice assistants, and chat-style search systems.

## Purpose

AEO answers:

```text
Which questions should this website answer?
Where should those answers live?
How should the answer be structured?
Which page should become the source of truth?
```

## Inputs

Use:

```text
People Also Ask
Related searches
GSC long-tail queries
Sales/customer questions
Reviews
Competitor FAQs
AI-search prompts
Support tickets
WhatsApp/chat questions
Course enrollment objections
Clinic/service objections
```

## Question Types

```text
Definition: What is X?
Process: How does X work?
Cost: How much does X cost?
Comparison: X vs Y
Eligibility: Who is X for?
Risk: What are the risks?
Timeline: How long does X take?
Local: Where can I get X in city?
Best/provider: Who is the best X?
Trust: Is X certified/verified/reliable?
```

## Answer Placement

Map each question to the right asset:

```text
Money page FAQ
Dedicated support article
Comparison page
Cost/pricing page
Process section
Course page module section
Local page FAQ
Knowledge hub/glossary
```

## Answer Block Format

Use:

```text
Question as H2/H3
Direct answer in 40-80 words
Expanded explanation
Steps/details/examples
Risks/limitations where relevant
Internal link to money page
Source/expert proof if needed
CTA if commercial
```

## AEO Elements

```text
Short direct answers
Definitions
Numbered steps
Comparison tables
Cost factor lists
FAQ blocks
Pros/cons
Eligibility lists
Risk/limitation notes
Checklists
Examples
Expert notes
```

## AEO for Local Businesses

Answer:

```text
What services are offered in this city?
Who provides the service?
How can the user book?
What areas are served?
What does it cost?
Is emergency/same-day help available?
What proof/reviews exist?
```

Include NAP, service area, reviews, provider credentials, FAQ, local schema, and call/booking CTA.

## AEO for Courses

Answer:

```text
Who is this course for?
What will students learn?
Which tools are covered?
What projects are built?
Is there a certificate?
How long does it take?
Can beginners join?
What outcomes can it support?
```

## AEO for YMYL

Use expert-reviewed content, disclaimers, risks/limitations, sources where needed, and visible credentials.

## Output Template

```text
## AEO Plan
Questions to Answer:
Answer Blocks to Add:
Support Articles:
Schema:
Trust Requirements:
Internal Links:
Priority:
```

## Common Mistakes

Do not add fake FAQs, hidden FAQs, vague answers, unrelated question blocks, duplicate FAQs everywhere, or YMYL answers without expert proof.


## citations-and-source-worthiness

# Citations and Source-Worthiness

Source-worthiness evaluates whether a page is worthy of being cited, referenced, linked to, or trusted by search engines, AI systems, journalists, bloggers, and other websites.

It matters for AEO, GEO, backlinks, PR, and authority.

## Purpose

Source-worthiness answers:

```text
Would someone cite this page?
Would an AI answer use this page as support?
Would another website link to this page naturally?
```

## Source-Worthy Content Types

```text
Original research
Data studies
Case studies
Step-by-step guides
Comparison guides
Definitions with expert clarity
Cost/pricing explainers
Industry reports
Templates/checklists
Tool lists
Local guides
Expert commentary
Founder insights
Medical/legal/technical explainers with credentials
```

## Criteria

Check:

```text
Originality
Accuracy
Expertise
Specificity
Freshness
Clear authorship
Citations/sources where needed
Useful formatting
Data/examples
Visuals/tables
Clear URL/title
Internal and external context
```

## Weak Signals

```text
Generic AI-written content
No author/expert
No sources
No examples
No unique point of view
No data/proof
Outdated information
Overly promotional page
Thin content
Unclear entity
```

## Citation Strategy

For each important cluster, create at least one citation-worthy asset.

Examples:

```text
AI automation adoption checklist for Pakistani businesses
Prompt engineering framework for beginners
Dental implant cost factors guide
Local emergency dental care checklist
AI agents glossary with examples
Course certification verification guide
```

## External Citation Targets

```text
Industry blogs
Local media
University pages
Professional communities
Associations
Partner sites
Newsletters
Resource pages
Relevant directories
Free article platforms when used carefully
```

## Output Template

```text
## Source-Worthiness Audit
Page/Topic:
Current Status:
Missing Proof:
Source Asset Idea:
Outreach Fit:
Priority:
```

## Common Mistakes

Do not expect people to link to generic sales pages, create studies without data, use fake citations, over-promote inside source assets, or ignore author credentials.


## conversation-seo-framework

# Conversation SEO Framework

Conversation SEO means answering full human questions, not just keywords.

---

## 1. Simple Meaning

Keyword:

```text
AI course
```

Human question:

```text
Which AI course is trusted, practical, affordable, and can help me earn?
```

The page must answer the full human question.

---

## 2. Conversation Map

For each money keyword, create:

```text
Main question
Follow-up questions
Fear questions
Cost questions
Comparison questions
Trust questions
Proof questions
Action questions
```

---

## 3. Example: AI Course

```text
Main: Which AI course should I choose?
Trust: Who teaches it?
Proof: Are there real students?
Practical: Does it include projects?
Outcome: Can it help me earn?
Certificate: Is it verifiable?
Cost: Is it affordable?
Action: How do I enroll?
```

---

## 4. Example: Dental Implants

```text
Main: Are dental implants right for me?
Cost: How much do they cost?
Pain: Is the process painful?
Trust: Which dentist can I trust?
Proof: Are there patient reviews?
Risk: What can go wrong?
Action: How do I book consultation?
```

---

## 5. Content Types

```text
Decision guides
Comparison pages
Cost pages
FAQ hubs
Review/proof pages
Objection pages
Use-case pages
Is it worth it pages
How to choose pages
```

---

## 6. Apify Sources

Use Apify/native tools to collect:

```text
People Also Ask
Related searches
Competitor FAQs
Reviews
YouTube comments
Reddit/Quora/community questions
Google Maps reviews
AI-search prompts
```

---

## 7. Conversation Brief Template

```text
Money keyword:
Full human question:
User fear:
Proof needed:
Required answer:
Follow-up questions:
Recommended page/section:
Internal proof links:
CTA:
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


## entity-seo

# Entity SEO

Entity SEO makes the brand, people, organization, services, products, courses, locations, and topics clearly understandable to search engines and AI systems.

Without entity clarity, AEO and GEO stay weak.

## Purpose

Entity SEO answers:

```text
Who is this?
What do they do?
Where do they operate?
Who is behind it?
What are they known for?
Can this entity be trusted?
How is it connected to other entities?
```

## Entity Types

Audit:

```text
Organization
Founder/CEO/expert
Author/instructor/doctor
Brand
Service
Product
Course
Location
Certification
Event
Community
Topic/category
```

## Entity Assets

Check:

```text
About page
Team/founder page
Author pages
Service/course/product pages
Location pages
Contact page
Press/media page
Reviews/testimonials
Case studies
Certificate/verification page
Social profiles
External profiles
PR/knowledge mentions
Schema
```

## Entity Consistency

Ensure consistency in:

```text
Name spelling
Brand handle
Logo
Website URL
Address
Phone
Email
Founder/expert name
Social profile links
Business category
Services/courses/products
```

## Schema

Use:

```text
Organization
Person
LocalBusiness
Course
Service
Product
Article
BreadcrumbList
sameAs
```

Use stable `@id` references:

```text
https://example.com/#organization
https://example.com/#website
https://example.com/about/#founder
https://example.com/ai-automation-course/#course
```

## Entity Page Requirements

### Organization

```text
What company does
Who it serves
Location/service area
History/proof
Services/products/courses
Leadership
Contact
External profiles
Schema
```

### Person

```text
Name
Role
Bio
Credentials
Experience
Awards/certifications
Topics known for
Media/social profiles
Published content
Organization relationship
Person schema
```

### Service/Course/Product

```text
Definition
Who it is for
Details
Proof
FAQs
Related pages
Schema
CTA
```

## Output Template

```text
## Entity SEO Audit
Entity:
Current Status:
Gap:
Fix:
Priority:
Schema:
External Consistency Action:
```

## Common Mistakes

Do not use different names everywhere, hide founder/expert identity, skip sameAs links, publish course/service pages without provider proof, or use schema that conflicts with visible content.


## generative-engine-optimization

# Generative Engine Optimization

GEO helps a brand, entity, website, and content become more likely to be understood, mentioned, and cited by generative search systems.

GEO is built on SEO, AEO, entity clarity, trust, source-worthiness, topical authority, and external mentions.

## Purpose

GEO answers:

```text
Why would an AI system mention this brand?
Why would it cite this page?
What evidence makes this source trustworthy?
What content is missing for AI-generated answers?
```

## GEO Signals

Audit:

```text
Entity clarity
Topical authority
Crawlable pages
Expert/founder/author credibility
Original insight
Citations/sources
Structured data
Consistent brand mentions
Backlinks/references
Media/PR mentions
Reviews/testimonials
Clear service/course/product pages
Support content depth
```

## GEO Content Requirements

Strong GEO content includes:

```text
Specific answers
Unique examples
Original frameworks
Definitions
Comparison tables
Practical experience
Expert commentary
Citations where appropriate
Transparent authorship
Fresh updates
Internal links
```

Generic content is weak GEO content.

## Entity Building Actions

Strengthen:

```text
About page
Founder/expert pages
Author pages
Organization schema
Person schema
Service/course/product pages
Case studies
Press/media page
Reviews/testimonials page
Certification/verification pages
External profiles
sameAs links
```

## Source-Worthiness Questions

Ask:

```text
Would an AI answer cite this over competitors?
Does this page provide something original?
Is it specific?
Is the expert/source clear?
Are claims supported?
Is it easy to quote or summarize?
```

## GEO Query Testing

Test:

```text
Best [service/course/product] in [location]
Who offers [service/course/product]?
What is the best way to learn [topic]?
How does [service/process] work?
[Brand] vs [competitor]
[service/product] cost
[topic] for [profession]
```

## GEO Actions

```text
Create entity-rich about/founder pages
Add source-worthy guides
Add expert review boxes
Add schema
Build topical clusters
Earn relevant mentions/backlinks
Publish comparison/cost/process pages
Add case studies/project proof
Create external profile consistency
Update stale content
```

## Output Template

```text
## GEO Audit
Entity Status:
Mention/Citation Status:
Main GEO Gaps:
Pages to Create/Improve:
External Authority Actions:
30-Day GEO Plan:
Missing Data:
```

## Common Mistakes

Do not claim GEO success without testing, make generic pages, ignore external authority, ignore schema, hide expert proof, or exaggerate claims.


## geo-ai-citation-optimization

# GEO AI Citation Optimization

GEO means Generative Engine Optimization.

The goal:

```text
Make the brand, person, company, product, service, or course easier for AI systems to mention, summarize, or cite.
```

No AI mention is guaranteed.

---

## 1. When to Use

Use this when the user asks:

```text
Make my brand appear in AI answers
Optimize for ChatGPT / Gemini / Perplexity / Google AI
GEO optimization
AI citation optimization
AI-friendly brand visibility
```

---

## 2. GEO Audit Questions

Ask:

```text
Can AI understand who this brand/person is?
Can AI find proof?
Can AI safely mention this entity?
Can AI compare it fairly?
Can AI cite the page as a source?
Is the content balanced and specific?
```

---

## 3. GEO-Ready Page Requirements

```text
Clear entity name
Clear topic
Short summary
Original proof
Fresh date
Author/expert identity
Citations or external proof where needed
Internal proof links
Structured data
Consistent facts
No fake hype
```

---

## 4. Source-Worthy Pages to Build

```text
/about/
/founder-or-expert-profile/
/company-profile/
/reviews/
/student-results/ or /client-results/
/case-studies/
/certifications/
/media/
/methodology/
/comparison-pages/
/faq/
```

---

## 5. GEO Citation Block

Add this to authority pages:

```text
Claim:
Evidence:
Source / proof link:
Context:
Limitation:
Related internal page:
```

---

## 6. Apify Workflow

Use Apify to check:

```text
SERP sources
AI Overview / AI Mode sources where supported
Competitor cited pages
Review sites
Media mentions
Social profiles
Third-party articles
Authority/backlink data
```

---

## 7. GEO Output Template

```text
Entity:
AI visibility status:
Competitors mentioned:
Cited sources found:
Missing pages:
Missing proof:
Schema needed:
Third-party authority plan:
Priority actions:
```

---

## 8. Quality Gate

GEO is strong when:

```text
The entity is clear.
The website has proof pages.
External reputation supports the claim.
The content is balanced.
Schema connects the entity.
Third-party sources confirm the story.
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


## topical-authority

# Topical Authority

Topical authority is the website’s demonstrated depth around a topic, service, product, course, or niche.

Beyond SEO uses topical authority to decide what clusters are needed and how money pages should be supported.

## Purpose

Topical authority answers:

```text
Does this website cover the topic deeply enough to be trusted and ranked?
```

## Strong Cluster Components

```text
Hub page / money page
Subtopic pages
Support articles
FAQ/answer blocks
Comparison pages
Cost/process pages
Case studies/proof
Internal links
Schema
Relevant backlinks/mentions
```

## Cluster Audit

For each topic, check:

```text
Is there a hub page?
Are key subtopics covered?
Are support articles linked to money pages?
Are FAQs answered?
Are comparison/cost/process questions covered?
Are author/expert signals visible?
Are pages internally linked?
Are external links/mentions supporting the cluster?
```

## Examples

### Dental Implants

```text
Hub: /dental-implants/
Subpages: All-on-4, All-on-5, bone grafting
Support: cost, recovery, candidacy, implants vs dentures
Proof: doctor credentials, case stories, reviews
```

### AI Academy

```text
Hub: /ai-course-pakistan/
Money pages: AI automation, AI agents, prompt engineering
Support: what are AI agents, AI automation vs no-code, best AI courses Pakistan
Proof: instructor credentials, student projects, certifications
```

## Internal Linking Rules

```text
Support articles link to money pages
Money pages link to related pages
Hub pages link to subpages
Breadcrumbs connect structure
Navigation includes top money pages
Anchor text is natural
```

## Authority Score

Score 0-10:

```text
Hub page quality: 0-2
Subtopic coverage: 0-2
Support content: 0-2
Internal linking: 0-2
Trust/backlinks/proof: 0-2
```

## Output Template

```text
## Topical Authority Audit
Topic Cluster:
Score:
Missing Pages:
Weak Pages:
Support Articles:
Internal Links:
Backlink Targets:
90-Day Action:
```

## Common Mistakes

Do not publish isolated blogs, build support content without internal links, ignore money pages, create too many thin subpages, or ignore proof/authority.
