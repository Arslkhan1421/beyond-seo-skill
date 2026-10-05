# Technical Dev Brief

Use this module when the user asks for developer tasks, implementation tickets, technical SEO fixes, schema JSON-LD, redirect maps, sitemap fixes, robots fixes, tracking requirements, or handoff-ready SEO engineering instructions.

## Task Format

Each developer task must include:

```text
Title
Severity
Business impact
Affected URL(s)
Evidence
Required change
Acceptance criteria
Validation method
Owner suggestion
Priority
```

## Common Technical Tasks

Create tasks for:

- Sitemap coverage fixes.
- Robots.txt changes.
- Canonical normalization.
- HTTP/HTTPS and www/non-www redirects.
- 404 and legacy URL redirect maps.
- Missing or duplicate title/meta/H1 patterns.
- Schema JSON-LD implementation.
- Internal link additions.
- Image alt/compression/lazy loading.
- Core Web Vitals and Lighthouse issues when verified.
- Noindex/indexability problems.
- JavaScript rendering or empty HTML problems.
- GA4/GSC/CRM conversion tracking.

## Redirect Map Format

Use:

```text
old_url
new_url
status_code
reason
priority
validation
```

Only recommend 301 redirects when the new URL is a relevant replacement. If no relevant replacement exists, recommend improving the 404 page or creating a matching page.

## Schema Output Rules

- Only generate schema that matches visible page content.
- Include JSON-LD examples when useful.
- Mention required visible content for each schema property.
- Do not promise rich results.

## Acceptance Criteria Examples

- URL returns 200 and is indexable.
- Canonical points to the preferred absolute URL.
- Sitemap includes all indexable money pages and excludes noindex/404 URLs.
- Legacy URL returns one-hop 301 to the closest relevant live page.
- JSON-LD validates without critical errors and matches visible content.
- GA4 event fires once per valid form submit/call/booking action.

## Final Handoff

Group tickets by:

- Must fix now.
- High impact next.
- Strategic build.
- Monitor.
