# Google Search Console Workflow

How Beyond SEO should use GSC exports or access.

Before analysis, load `integrations/first-party-data-quality.md`. Validate provenance, property, dates, timezone, filters, normalized units, anonymized-query/export limits and canonical URL attribution. GSC does not verify conversions. Average position is not a fixed live rank.

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
