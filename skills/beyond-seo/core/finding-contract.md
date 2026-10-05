# Traceable Findings

Use the required fields in `core/evidence-schema.json`; validate with `tools/audit_quality.py::validate_findings` when running the pipeline.

A finding contains a stable finding/check ID, affected URLs, exact observation, evidence IDs, source artifact and locator, collection time, interpretation and separate labels, confidence, business impact, severity, recommended action, acceptance criteria, validation method and owner. The ledger holds URL-level parsed values; the report carries references and a readable summary.

`H1 absent in fetched HTML` is Confirmed when HTML was collected successfully. `Heading clarity may need improvement` is Inferred. Ranking loss remains Not verified without supporting measurement. Render the page before concluding that a JavaScript site lacks an H1.

Determine intended search pages from the owner, architecture and first-party evidence. Review URL mappings, traffic and intent before consolidating pages, changing canonicals, removing content or redirects. Execute live-site changes only within the user's authorized scope. Do not manufacture monetary impact.

Record `checks_performed` per URL, including successful no-finding checks. Failed/excluded URLs are not successful rechecks. A disappearing finding is Resolved only when the same check ran on every previously affected URL; otherwise use Not rechecked. Different site/localization/device scope is Not comparable. Legacy audits without check records cannot prove resolution automatically.

If evidence conflicts, preserve both observations, dates, methods and scopes. Re-fetch specific URLs where useful and leave interpretation unverified until differences are explained.
