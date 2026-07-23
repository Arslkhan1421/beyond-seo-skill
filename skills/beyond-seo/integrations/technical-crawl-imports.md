# Technical Crawl Import Workflow

Use this file when the user provides Screaming Frog, Sitebulb, Lumar, JetOctopus, or other technical crawl exports, especially for large websites.

Load this together with:

```text
tools/source_classifier.py
templates/data-imports/screaming-frog-internal.csv
templates/data-imports/sitebulb-url-list.csv
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
