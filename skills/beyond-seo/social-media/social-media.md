# Social Media

Use the contents below to select the relevant workflow; load only the needed sections.


## instagram-content-builder

# Instagram Content Builder

Use this module when the user asks for Instagram captions, carousel outlines, Reels scripts, Stories, hashtags, visual briefs, or Instagram content based on Beyond SEO strategy.

## Platform Role

Use Instagram for:

- simplified education from SEO/service topics;
- carousel explainers and checklists;
- visual proof, process, team, portfolio, and behind-the-scenes content;
- short-form Reels that answer common questions;
- Stories for polls, FAQs, social proof, offers, and reminders.

## Content Formats

Choose the format based on topic:

```text
Carousel: best for frameworks, checklists, myths, comparisons, before/after process, FAQs.
Reel: best for quick answers, founder face-to-camera, process clips, teardown snippets.
Static Post: best for proof, quote, announcement, offer, or single strong idea.
Story Sequence: best for polls, questions, reminders, social proof, and soft CTAs.
```

## Required Output Fields

For each Instagram asset provide:

```text
post_id
platform
post_type
content_pillar
seo_source_url
target_keyword_or_topic
hook
caption
carousel_slides_or_reel_script
visual_brief
cta
target_url
utm_url
hashtags
evidence_label
approval_notes
```

## Carousel Structure

For carousel posts, use:

```text
Slide 1: strong hook or problem.
Slides 2-6: teaching points, proof, process, checklist, or example.
Final slide: CTA tied to a target page, call, booking, or guide.
```

Keep slides short enough to design. Do not write paragraphs for slide text.

## Reel Script Structure

For Reels, include:

```text
Opening hook
3-5 talking points or scene beats
On-screen text suggestions
Visual direction
CTA
```

## Hashtag Rules

Use a balanced set:

```text
Brand hashtag
Service hashtags
Niche/problem hashtags
Location hashtags when relevant
Audience/industry hashtags
```

Prefer 6-12 hashtags unless the user gives a platform-specific preference. Avoid unrelated viral hashtags.

## Safety

Do not invent images, testimonials, client names, results, screenshots, follower counts, or engagement metrics. Mark missing proof as `Not verified` and ask for assets when needed.

Do not auto-post to Instagram. Export content for review or scheduler import unless a future API publishing module is available, authenticated, and approved by the user.


## linkedin-post-builder

# LinkedIn Post Builder

Use this module when the user asks for LinkedIn posts, founder posts, company page posts, thought leadership, case-study posts, service education, or B2B lead-generation content from Beyond SEO findings.

## Platform Role

Use LinkedIn for:

- B2B authority and founder/expert POV;
- service education and problem framing;
- case studies, process proof, and lessons learned;
- lead-generation CTAs for audits, calls, demos, or consultations;
- distribution of website pages, reports, guides, and technical briefs.

## Post Formats

Choose the format based on intent:

```text
Founder POV: opinion, lesson, tradeoff, mistake, or market observation.
Company Page Education: clear service explanation tied to a landing page.
Case Study Mini Story: problem, approach, result, and lesson without fake numbers.
Problem / Solution: pain point, cause, fix, and CTA.
Technical Authority: checklist, framework, architecture note, audit finding, or teardown.
Comparison / Objection: "X vs Y", "when to choose", "why this fails".
Offer CTA: audit, consultation, demo, booking, download, or quote request.
```

## Required Output Fields

For each LinkedIn post provide:

```text
post_id
platform
post_type
content_pillar
seo_source_url
target_keyword_or_topic
hook
post_copy
cta
target_url
utm_url
hashtags
evidence_label
approval_notes
```

## Writing Rules

Write for a real B2B reader:

- start with a specific hook, not a generic slogan;
- use short paragraphs and plain language;
- explain one useful idea per post;
- connect the post to a service, pain point, page, or proof item;
- use one clear CTA;
- use 3-6 relevant hashtags;
- avoid engagement bait, fake urgency, fake results, fake clients, and fake statistics.

## Voice Guidance

Use personal/founder voice when the user wants POV, lessons, opinions, hiring, delivery, market, or founder-led authority.

Use company voice when the user wants service clarity, process, proof, offers, reports, technical education, or company-page publishing.

## CTA Patterns

Use CTAs matched to the funnel:

```text
Awareness: Read the full guide, see the checklist, compare the options.
Consideration: View the service page, review the process, ask for the audit.
Conversion: Book a call, request a quote, schedule a demo, send the project brief.
```

## Safety

Do not auto-post to LinkedIn. Export content for review or scheduler import unless a future API publishing module is available, authenticated, and approved by the user.


## social-calendar-builder

# Social Calendar Builder

Use this module when the user asks for a 30-day LinkedIn and Instagram calendar, content plan, posting schedule, approval workflow, or social content roadmap from Beyond SEO.

## Default Duration

Default to 30 days when the user does not specify another duration.

For this Beyond SEO skill, a "30-day social calendar" means a day-by-day plan with platform, format, pillar, topic, copy direction, CTA, target URL, and evidence label.

## Calendar Requirements

Every calendar row must include:

```text
day
date
platform
post_type
content_pillar
seo_source_url
target_keyword_or_topic
hook
post_copy_or_caption
carousel_slides_or_visual_brief
cta
target_url
utm_url
hashtags
evidence_label
status
approval_notes
```

## Recommended Cadence

Use a sustainable default unless the user gives a brand capacity:

```text
LinkedIn: 4 posts per week.
Instagram: 5 posts per week, mixed across carousel, Reel, static, and Story.
```

If the user asks for daily content, provide at least one planned post for each of the 30 days. It is acceptable to use LinkedIn on some days, Instagram on others, and both on high-value campaign days.

## Weekly Rhythm

Use this rhythm as a starting point:

```text
Monday: service education or problem framing.
Tuesday: proof, process, case study, or technical authority.
Wednesday: AEO/GEO answer, FAQ, or objection handling.
Thursday: competitor-gap, comparison, or founder POV.
Friday: offer, CTA, recap, checklist, or lead magnet.
Weekend: lighter Instagram Stories, reminders, behind-the-scenes, or evergreen tips.
```

## Content Balance

Keep the 30-day calendar balanced:

```text
40% service education
20% proof or case study
15% founder/expert POV
15% objections, comparisons, or competitor-gap topics
10% direct offer or CTA
```

## Quality Checks

Before finalizing:

- every post must map to a business goal or SEO source;
- no duplicate hooks across the same week;
- each platform must use platform-native wording;
- each post must have a CTA or intentional soft CTA;
- each link post must include a target URL and UTM suggestion;
- each metric or claim must have an evidence label;
- unverified claims must be removed or rewritten.

## Approval Workflow

Use these statuses:

```text
draft
needs_review
approved
scheduled
posted
```

Default new calendars to `draft` unless the user says content is already approved.


## social-posting-export

# Social Posting Export

Use this module when the user asks to export LinkedIn or Instagram content to CSV, spreadsheet, scheduler-ready format, or posting handoff files.

## Export Purpose

Create files that can be reviewed manually or imported into scheduling tools such as Buffer, Hootsuite, Later, Metricool, Sprout Social, SocialBee, HubSpot, or similar tools.

Do not claim direct posting is complete. This module prepares content for human approval and scheduler import.

## Default CSV Columns

Use `templates/social-posting-30-day-template.csv` when available.

Required columns:

```text
day
date
platform
post_type
content_pillar
seo_source_url
target_keyword_or_topic
hook
post_copy
caption
carousel_slides_or_visual_brief
cta
target_url
utm_url
hashtags
evidence_label
status
approval_notes
```

## UTM Pattern

Use a readable campaign slug:

```text
utm_source={platform}
utm_medium=social
utm_campaign={campaign_slug}
utm_content=day-{day}-{post_type}
```

If the target URL already has query parameters, append UTM parameters with `&`. Otherwise use `?`.

## Scheduler Compatibility

If the user names a scheduler, adapt column names to that scheduler's import format when known. If unsure, keep the default Beyond SEO format and mention that the file may need column mapping inside the scheduler.

## Export Quality Gate

Before delivering an export:

- check that every row has platform, post type, hook, copy/caption, CTA, status, and evidence label;
- check target URLs for link posts;
- check UTM URLs are present when target URLs are present;
- avoid duplicate post copy;
- keep LinkedIn copy and Instagram captions separate when a post appears on both platforms;
- keep hashtags platform-relevant;
- keep all unverified performance claims out of the copy.

## API Publishing Boundary

This module does not publish posts through LinkedIn, Instagram, Meta, or third-party scheduler APIs.

If the user asks for auto-posting later, require:

```text
platform or scheduler choice
developer app or scheduler API access
permissions/scopes
account/page IDs
media assets
human approval step
dry-run mode
posting log
rollback/edit plan
```


## social-seo-strategy

# Social SEO Strategy

Use this module when the user asks Beyond SEO to turn SEO audit findings, keyword maps, competitor gaps, service pages, or AEO/GEO opportunities into LinkedIn and Instagram content strategy.

## Goal

Build social content that supports:

- brand/entity recognition;
- service and money-page demand;
- referral traffic to SEO landing pages;
- expert trust and proof;
- content validation for future SEO topics;
- leads, calls, bookings, demos, or sales.

Do not claim that social posting directly guarantees Google rankings. Treat social SEO as demand creation, brand reinforcement, audience proof, traffic support, and content distribution unless first-party analytics proves more.

## Inputs To Collect

Use what is available:

- business type, audience, country/location, services, and conversion goal;
- website audit findings and priority pages;
- target keywords, page clusters, and content gaps;
- competitor pages and social positioning if sampled;
- case studies, offers, testimonials, team expertise, or proof;
- brand voice, posting frequency, and approval owner;
- allowed claims, restricted claims, and compliance notes.

If these inputs are missing, proceed with clearly labeled assumptions.

## Pillar Framework

Create 4-6 content pillars. Prefer:

```text
Service Education: explain problems, solutions, process, and outcomes tied to money pages.
Problem / Objection Handling: answer sales objections and comparison questions.
Proof / Case Study: show outcomes, process proof, before-after context, or lessons learned.
Founder / Expert POV: share opinions, lessons, tradeoffs, and market observations.
AEO / GEO Answer Content: concise answers to questions found in SERPs, PAA, FAQs, or audits.
Conversion / Offer: drive audits, calls, demos, bookings, downloads, or quote requests.
```

For each pillar include:

```text
Pillar
Audience pain
SEO source page or finding
Target keyword/topic
Recommended platforms
Best formats
Primary CTA
Evidence label
```

## Evidence Rules

Label every topic and claim:

```text
Confirmed: directly observed on the website, crawl, SERP, or provided source.
First-party verified: from GSC, GA4, CRM, GBP, or platform analytics export.
Paid-tool verified: from Semrush, Ahrefs, Moz, DataForSEO, Screaming Frog, Sitebulb, or similar export.
Live SERP sample: from current manual/native/Apify search samples.
Inferred: a strategic conclusion from available evidence.
Directional: useful but not statistically complete.
Not verified: missing supporting data.
```

Do not invent impressions, followers, engagement, traffic, conversions, keyword volume, difficulty, DR/DA, rankings, or competitor social performance.

## 30-Day Strategy Output

When building a 30-day strategy, include:

```text
Positioning summary
Audience and offer assumptions
Content pillars
Platform role: LinkedIn vs Instagram
Weekly rhythm
30-day calendar summary
Measurement plan
Data gaps and exports needed next
```

Recommended default mix:

```text
40% service education
20% proof or case study
15% founder/expert POV
15% objections, comparisons, or competitor-gap topics
10% direct offer or CTA
```

Keep every post connected to at least one SEO source: a page, keyword/topic, competitor gap, SERP question, service, audit issue, or conversion goal.
