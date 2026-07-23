# Report Builder Pro

Use this module when the user asks for a client-ready PDF, monthly report, proposal-style report, executive report, or visual SEO dashboard.

## Required Inputs

- Website URL, brand name, target market, services, and business goal.
- Crawl findings, SERP samples, keyword tables, competitor rows, issue log, and roadmap.
- Verified exports when available: GSC, GA4, Semrush, Ahrefs, Moz, DataForSEO, Screaming Frog, Sitebulb.
- Evidence labels for every metric.

## Report Modes

Choose one mode before writing:

- Full audit report: diagnosis, findings, scorecards, fixes, roadmap.
- Monthly progress report: movement, completed work, KPI changes, next-month plan.
- Competitor gap report: SERP competitors, content gaps, authority gaps, page comparisons.
- Proposal report: opportunity, pain points, scope, timeline, expected movement, data gaps.
- Developer handoff report: technical tasks, acceptance criteria, owners, priority.

## Client-Ready Structure

Include these sections for full reports:

1. Cover and audit scope.
2. Executive summary.
3. Data confidence and source labels.
4. SEO health dashboard.
5. Technical findings.
6. Page inventory and indexability.
7. Keyword and SERP opportunity.
8. Competitor gap.
9. Content, E-E-A-T, AEO/GEO, local, and conversion gaps.
10. Website improvement text.
11. Prioritized action plan.
12. 30/60/90-day roadmap.
13. Data not available and recommended exports.

## Visual Rules

- Use scorecards only for areas supported by evidence.
- Mark unverified metrics as `Not verified`; never force them into numeric charts.
- Use traffic-light severity, score bars, issue tables, keyword tables, and roadmap panels.
- Do not copy Semrush, Ahrefs, Moz, DataForSEO, GSC, or GA4 branding or proprietary UI.
- Keep tables readable in PDF: short columns, wrapped text, and repeated headers.

## PDF Completion Contract

- Write PDFs to `output/pdf/`.
- Write source Markdown/JSON to `output/reports/` when useful.
- Render the PDF to PNG and inspect representative pages before delivery.
- If rendering fails, still provide the PDF but clearly say render verification failed.

## Final Delivery

Return:

- PDF path.
- Supporting report path when created.
- Tools and sources used.
- Render-check status.
- Data gaps that affect confidence.
