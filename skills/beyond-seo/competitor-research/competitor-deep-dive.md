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
