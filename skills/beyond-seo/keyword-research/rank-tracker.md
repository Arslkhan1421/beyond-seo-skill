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
5. Label movement as improved, declined, unchanged, new, lost, or not comparable.
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
