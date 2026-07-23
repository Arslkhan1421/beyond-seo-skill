# Visual Scorecards and Evidence Reporting

Use this file whenever the user asks for a report, client audit, SEO dashboard, keyword report, competitor report, or website improvement plan.

The goal is to make Beyond SEO reports easier to understand while keeping every score evidence-based.

For PDF output, also load:

```text
reporting/pdf-report-design-system.md
```

---

## 1. Required Visual Score Elements

Every serious report should include a simple visual scorecard.

Use text-safe visuals that work in Markdown, docs, PDFs, and chat:

```text
Overall SEO Health: 72/100
[##############------] 72%
Status: Good foundation, needs content + authority expansion
```

Use score bands:

```text
0-39   Critical
40-59  Weak
60-74  Developing
75-89  Strong
90-100 Excellent
```

Use traffic-light labels:

```text
Red: urgent blocker
Amber: important improvement
Green: working well
Gray: not verified from available data
```

---

## 2. SEO Health Visual Table

Default scorecard:

```text
| Area | Score | Visual | Status | Main Reason | Next Action |
|---|---:|---|---|---|---|
| Technical SEO | 16/20 | [################----] | Strong | Crawlable, but speed issues remain | Fix CWV on money pages |
| Content / E-E-A-T | 11/20 | [###########---------] | Weak | Service pages are thin | Expand money pages |
```

Scores must be supported by findings. Do not score categories with no data as if they were verified.

If data is missing:

```text
Score: Not verified
Visual: [????????????????????]
Reason: GSC/GA4/backlink/GBP data was not provided.
```

---

## 3. Priority Heatmap

Use a heatmap-style table for client decisions:

```text
| Action | Impact | Effort | Confidence | Priority | Why |
|---|---:|---:|---:|---|---|
| Fix indexable duplicate city pages | 5 | 2 | 5 | Must Fix Now | Reduces crawl waste and ranking confusion |
| Add 6 service pages | 5 | 4 | 4 | High Impact Next | Captures missing money intent |
```

Priority formula:

```text
Priority = Impact + Confidence - Effort - Risk
```

Labels:

```text
Must Fix Now
High Impact Next
Strategic Build
Monitor
Ignore for Now
```

---

## 4. Authentic Keyword Evidence Rules

Keyword data must be labeled by source.

Allowed keyword evidence sources:

```text
Google Search Console export/API
Google Ads Keyword Planner export
Google Trends
Apify SERP scrape
Ahrefs/Semrush/Moz/DataForSEO export
Manual live SERP sample
Competitor page/title/H1/content crawl
People Also Ask / related searches scrape
Bing Webmaster Tools export
```

Every keyword table must include:

```text
Keyword
Intent
Source
Verification status
Current URL if known
Current rank if verified
Search volume if verified
Competitor URL if verified
Action
Confidence
```

Do not invent search volume, ranking, CPC, difficulty, or competitor ownership. If unavailable, use:

```text
Not verified from available data
Recommended source: [exact source]
```

---

## 5. Competitor Keyword Evidence Rules

Competitor keywords are authentic only when supported by one of:

```text
SEO tool export showing competitor keyword rankings
SERP scrape showing competitor page ranking for the query
GSC is not valid for competitor data unless the competitor owns/provides it
Manual SERP check with location/device/date noted
Competitor page crawl showing clear targeting, labeled as "targeted by competitor", not "ranking"
```

Use two different labels:

```text
Competitor Ranking Keyword: verified competitor ranking from SERP/tool data.
Competitor Targeted Keyword: inferred from competitor title/H1/content, ranking not verified.
```

Never mix the two.

---

## 6. Keyword Opportunity Visual

Use this table for keyword opportunities:

```text
| Keyword | Intent | Evidence | Current Position | Best Competitor | Opportunity | Confidence | Action |
|---|---|---|---:|---|---|---|---|
| emergency dentist chicago | Local urgent | SERP sample + competitor crawl | Not verified | example.com/emergency-dentist | Missing money page | Medium | Create local service page |
```

Opportunity labels:

```text
Existing Winner
Fastest Win
Missing Money Page
Competitor-Owned
Topical Authority Builder
Brand Defense
AEO Opportunity
Local Map Intent
Ignore for Now
```

---

## 7. Website Improvement Text Blocks

Reports must include plain-English improvement sections, not only tables.

Use this format:

```text
### Improvement: [Page or issue]

Current problem:
[What is weak now, in simple words.]

Why it matters:
[Ranking, crawlability, trust, conversion, local, AI visibility, or revenue impact.]

Recommended change:
[Specific text, section, technical fix, schema, layout, CTA, internal link, or content action.]

Example improvement text:
[Optional draft copy, title tag, H1, meta description, FAQ, CTA, or section outline.]

Priority:
[Must Fix Now / High Impact Next / Strategic Build / Monitor]

Evidence:
[URL, crawl finding, SERP observation, GSC data, competitor example, or "not verified".]
```

This section is mandatory for the top 5 highest-priority fixes.

---

## 8. Report Visuals That Are Allowed

Use:

```text
Markdown score tables
Text progress bars
Traffic-light labels
Priority heatmaps
Keyword opportunity matrices
Competitor gap tables
Before/after text blocks
Roadmap timelines
KPI cards written as Markdown tables
```

Do not use:

```text
Fake charts with invented numbers
Decorative visuals without evidence
Traffic projections without assumptions
Keyword volumes without a source
Competitor keyword claims without source labels
```

---

## 9. Final Report Rule

A report is not complete unless it answers:

```text
What is the score?
Why is the score justified?
Which keywords are verified?
Which competitor keywords are verified vs inferred?
What exact website text/technical/content improvements should be made?
What Microsoft Clarity behavior signals are verified, over which 1–3 day window, and what should be investigated?
What data is missing?
What should be done first?
```
