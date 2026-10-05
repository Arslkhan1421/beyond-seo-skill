# Implementation and Outcomes

Use `templates/implementation-outcomes-template.csv` and:

```text
python tools/outcome_tracker.py --input implementation-outcomes.csv --output outcomes.json
```

Connect tasks to URLs, finding/evidence IDs, owner, implementation date, validation result/evidence, business metric/unit, baseline/follow-up values/windows, source/property, segment/filters, timezone, measurement evidence and confounders. Choose an observation window appropriate to traffic and metric; do not promise a fixed SEO response time.

- **Fix verified**: acceptance criteria passed with recorded evidence.
- **Observed change**: comparable dated measurements show a positive, negative or zero delta. This does not establish that the fix caused it.

Baseline precedes implementation; follow-up follows it. Missing, overlapping or unequal windows are Not comparable. Zero baseline permits an absolute delta but no growth percentage. The tracker validates supplied records; it does not authenticate declarations or screenshots. Causation requires a defensible experiment/design, controls, sufficient data and confounder analysis.

Keep CRM leads/revenue distinct from analytics key events. Record other deployments, campaigns, search updates, seasonality and tracking changes. Do not publish client measurement data in the public skill repository.
