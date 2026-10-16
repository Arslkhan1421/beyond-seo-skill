#!/usr/bin/env python3
"""Build a polished Beyond SEO PDF report from a normalized JSON file.

Usage:
  python tools/report_builder.py --input audit.json --output output/pdf/site-seo-report.pdf
  python tools/report_builder.py --sample --output output/pdf/sample-seo-report.pdf

The input schema is intentionally simple so agents can assemble it from crawl,
SERP, paid-tool export, or manual evidence.
"""

from __future__ import annotations

import argparse
import html
import json
import re
from urllib.parse import urlsplit
from datetime import date
from pathlib import Path
from typing import Any

try:
    from reportlab.lib import colors
    from reportlab.lib.enums import TA_CENTER, TA_LEFT
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
    from reportlab.lib.units import inch
    from reportlab.platypus import (
        PageBreak,
        Paragraph,
        SimpleDocTemplate,
        Spacer,
        Table,
        TableStyle,
        Flowable,
        Image,
        KeepTogether,
    )
except Exception as exc:  # pragma: no cover - runtime dependency message
    raise SystemExit(
        "reportlab is required. Install it or use the bundled Codex PDF runtime."
    ) from exc


BRAND = colors.HexColor("#12343B")
INK = colors.HexColor("#17252A")
MUTED = colors.HexColor("#5B6870")
SOFT = colors.HexColor("#F4F8FA")
LINE = colors.HexColor("#DDE6EA")
GREEN = colors.HexColor("#1F8A70")
ACCENT = colors.HexColor("#26B8A5")
AMBER = colors.HexColor("#C77D0E")
RED = colors.HexColor("#B94040")
GRAY = colors.HexColor("#AAB5BA")


def sample_payload() -> dict[str, Any]:
    return {
        "title": "SEO, AEO and Website Improvement Audit - Demonstration",
        "demo": True,
        "client": "Sample Client",
        "site_url": "https://example.com/",
        "audit_date": str(date.today()),
        "audit_mode": "Native scrape + manual SERP sample",
        "overall_score": 66,
        "status": "Developing",
        "summary": (
            "The site has a crawlable foundation, but growth is limited by "
            "content depth, missing keyword pages, authority gaps, and "
            "unverified analytics data."
        ),
        "data_confidence": [
            {"label": "Confirmed", "value": "crawl, sitemap, robots, metadata (demonstration)"},
            {"label": "Live SERP sample", "value": "manual SERP checks (demonstration)"},
            {"label": "Inferred", "value": "competitor targeting from page content"},
            {"label": "Not verified", "value": "paid-tool metrics, GSC/GA4, backlinks"},
        ],
        "scores": [
            {"area": "Technical SEO", "score": 70, "display": "14 / 20", "note": "Good base; sitemap and redirects need work."},
            {"area": "On-page SEO", "score": 67, "display": "10 / 15", "note": "Metadata exists; several pages need stronger H1/content."},
            {"area": "Content / E-E-A-T", "score": 50, "display": "10 / 20", "note": "Needs more proof, examples, and expert depth."},
            {"area": "Authority / Backlinks", "score": None, "display": "Not verified", "note": "Requires Ahrefs/Semrush/Moz export."},
        ],
        "clarity": {
            "source": "Microsoft Clarity Data Export API",
            "source_url": "https://learn.microsoft.com/en-us/clarity/setup-and-installation/clarity-data-export-api",
            "evidence_label": "First-party verified",
            "retrieved_at": f"{date.today()}T00:00:00+00:00",
            "window": "Previous 3 days, UTC",
            "dimensions": "URL",
            "metrics": [
                {
                    "metric": "Traffic",
                    "segment": "URL: /services",
                    "observed": "totalSessionCount: 125; PagesPerSessionPercentage: 1.8",
                    "evidence_label": "First-party verified",
                },
                {
                    "metric": "Rage Click Count",
                    "segment": "URL: /contact",
                    "observed": "sessionsWithMetricPercentage: 2.4",
                    "evidence_label": "First-party verified",
                },
            ],
            "signals": [
                {
                    "signal": "Rage Click Count",
                    "scope": "URL: /contact",
                    "evidence": "sessionsWithMetricPercentage: 2.4",
                    "action": "Inspect repeated clicks, latency, overlays, and misleading controls.",
                }
            ],
            "limitations": (
                "Short-window behavior snapshot. Signals support investigation "
                "and do not prove SEO causation."
            ),
        },
        "findings": [
            {"issue": "Key pages missing from sitemap", "evidence": "Service URLs absent from XML sitemap", "priority": "High", "fix": "Add all indexable service pages and resubmit in GSC."},
            {"issue": "Legacy URLs return 404", "evidence": "Old URLs still visible in samples", "priority": "High", "fix": "Map legacy URLs to direct 301 redirects."},
        ],
        "keywords": [
            {"keyword": "custom software development", "intent": "Commercial", "source": "Manual SERP sample", "volume": "Not verified", "difficulty": "Not verified", "action": "Expand service page", "confidence": "Live sample"},
        ],
        "competitors": [
            {"competitor": "competitor.com", "evidence": "Ranking in sample SERP", "gap": "Deeper service page", "action": "Add proof, process, FAQs, and case links."},
        ],
        "roadmap": [
            {"timeframe": "0-30 days", "actions": "Fix sitemap, redirects, metadata gaps, and top service content.", "outcome": "Cleaner crawl signals and stronger money pages."},
            {"timeframe": "31-60 days", "actions": "Build content clusters and case studies.", "outcome": "More topical authority and conversion proof."},
        ],
        "data_gaps": [
            {"source": "GSC", "needed": "Queries, pages, CTR, positions"},
            {"source": "Ahrefs/Semrush", "needed": "Backlinks, keyword footprint, authority metrics"},
        ],
        "sources": [
            {"label": "Website", "url": "https://example.com/"},
        ],
    }


def load_payload(path: str | None, use_sample: bool) -> dict[str, Any]:
    if use_sample or not path:
        return sample_payload()
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def paragraph_styles():
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(
        name="CoverTitle",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=27,
        leading=32,
        textColor=BRAND,
        alignment=TA_LEFT,
        spaceAfter=14,
    ))
    styles.add(ParagraphStyle(
        name="CoverSub",
        parent=styles["Normal"],
        fontSize=11,
        leading=15,
        textColor=MUTED,
        alignment=TA_LEFT,
    ))
    styles.add(ParagraphStyle(
        name="H1x",
        keepWithNext=True,
        parent=styles["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=17,
        leading=21,
        textColor=BRAND,
        spaceBefore=4,
        spaceAfter=8,
    ))
    styles.add(ParagraphStyle(
        name="H2x",
        keepWithNext=True,
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=12,
        leading=15,
        textColor=BRAND,
        spaceBefore=8,
        spaceAfter=5,
    ))
    styles.add(ParagraphStyle(
        name="Bodyx",
        parent=styles["BodyText"],
        fontSize=10,
        leading=14,
        textColor=INK,
        spaceAfter=5,
    ))
    styles.add(ParagraphStyle(
        name="Smallx",
        parent=styles["BodyText"],
        fontSize=7.6,
        leading=10,
        textColor=MUTED,
    ))
    styles.add(ParagraphStyle(
        name="TableHead",
        parent=styles["BodyText"],
        fontName="Helvetica-Bold",
        fontSize=8,
        leading=10,
        textColor=colors.white,
    ))
    styles.add(ParagraphStyle(
        name="TableCell",
        parent=styles["BodyText"],
        fontSize=8.5,
        leading=12,
        textColor=INK,
    ))
    return styles


STYLES = paragraph_styles()


def p(text: Any, style: str = "Bodyx") -> Paragraph:
    raw = str(text if text is not None else "").translate({0x2010: '-', 0x2011: '-', 0x2013: '-', 0x2014: '-'})
    parts = re.split(r'(https?://[^\s<>"\']+)', raw)
    escaped = ''.join(f'<link href="{html.escape(part, quote=True)}" color="#16776C">{html.escape(part)}</link>' if part.startswith(('https://', 'http://')) else html.escape(part) for part in parts)
    return Paragraph(escaped, STYLES[style])


class ReportDocument(SimpleDocTemplate):
    def afterFlowable(self, flowable):
        if isinstance(flowable, Paragraph) and flowable.style.name == 'H1x':
            key = f'section-{self.page}-{getattr(self, "section_count", 0)}'
            self.section_count = getattr(self, 'section_count', 0) + 1
            self.canv.bookmarkPage(key)
            self.canv.addOutlineEntry(flowable.getPlainText(), key, 0)


def score_color(score: int | float | None):
    if score is None:
        return GRAY
    if score >= 75:
        return GREEN
    if score >= 55:
        return AMBER
    return RED


def score_bar(score: int | float | None, width: int = 78, height: int = 8) -> Table:
    if score is None:
        filled = 1
    else:
        filled = max(1, int(width * max(0, min(100, score)) / 100))
    remaining = max(1, width - filled)
    return Table(
        [["", ""]],
        colWidths=[filled, remaining],
        rowHeights=[height],
        style=TableStyle([
            ("BACKGROUND", (0, 0), (0, 0), score_color(score)),
            ("BACKGROUND", (1, 0), (1, 0), colors.HexColor("#E7EEF1")),
            ("BOX", (0, 0), (-1, -1), 0.25, LINE),
            ("LEFTPADDING", (0, 0), (-1, -1), 0),
            ("RIGHTPADDING", (0, 0), (-1, -1), 0),
            ("TOPPADDING", (0, 0), (-1, -1), 0),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
        ]),
    )


def table(rows: list[list[Any]], widths: list[float], header: bool = True) -> Table:
    data = []
    for idx, row in enumerate(rows):
        style = "TableHead" if idx == 0 and header else "TableCell"
        data.append([item if hasattr(item, "wrap") else p(item, style) for item in row])
    commands = [
        ("LINEBELOW", (0, 0), (-1, -1), 0.35, LINE),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 9),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
    ]
    if header:
        commands.extend([
            ("BACKGROUND", (0, 0), (-1, 0), BRAND),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ])
    for idx in range(1 if header else 0, len(data)):
        if idx % 2 == 0:
            commands.append(("BACKGROUND", (0, idx), (-1, idx), colors.HexColor("#FAFCFC")))
    # Keep every table inside the actual page frame, including nested score bars.
    available = A4[0] - 1.16 * inch
    widths = [value * available / sum(widths) for value in widths]
    return Table(data, colWidths=widths, repeatRows=1 if header else 0, style=TableStyle(commands), spaceAfter=14)


class CoverIdentity(Flowable):
    """Vector brand panel: crisp at any zoom, with no external assets."""
    def __init__(self):
        super().__init__()
        self.width = A4[0] - 1.16 * inch
        self.height = 112

    def draw(self):
        c = self.canv
        c.setFillColor(BRAND)
        c.roundRect(0, 0, self.width, self.height, 10, fill=1, stroke=0)
        c.setFillColor(ACCENT)
        c.rect(22, 76, 30, 4, fill=1, stroke=0)
        c.setFillColor(colors.white)
        c.setFont("Helvetica-Bold", 24)
        c.drawString(22, 40, "BEYOND SEO")
        c.setFont("Helvetica", 9)
        c.drawString(22, 22, "SEARCH VISIBILITY / WEBSITE EXPERIENCE / ACTION PLAN")


def priority_badge(value):
    text = str(value or "Not assigned")
    tone = RED if text.lower() in ("high", "critical") else AMBER if text.lower() == "medium" else BRAND
    return Paragraph(f'<font color="{tone.hexval()}"><b>{html.escape(text)}</b></font>', STYLES["TableCell"])


def footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(LINE)
    canvas.line(doc.leftMargin, 0.55 * inch, A4[0] - doc.rightMargin, 0.55 * inch)
    canvas.setFont("Helvetica", 7.5)
    canvas.setFillColor(MUTED)
    canvas.drawString(doc.leftMargin, 0.38 * inch, "BEYOND SEO  /  Evidence-led website audit")
    canvas.drawRightString(A4[0] - doc.rightMargin, 0.38 * inch, f"Page {doc.page}")
    canvas.setFillColor(BRAND)
    canvas.setFont("Helvetica-Bold", 8)
    canvas.drawString(doc.leftMargin, A4[1] - 25, "BEYOND SEO")
    canvas.setStrokeColor(ACCENT)
    canvas.line(doc.leftMargin, A4[1] - 33, doc.leftMargin + 34, A4[1] - 33)
    canvas.restoreState()


def cover_band(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(BRAND)
    canvas.rect(0, A4[1] - 0.32 * inch, A4[0], 0.32 * inch, stroke=0, fill=1)
    canvas.rect(0, 0, A4[0], 0.16 * inch, stroke=0, fill=1)
    canvas.restoreState()


def build_pdf(payload: dict[str, Any], output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    doc = ReportDocument(
        str(output),
        pagesize=A4,
        rightMargin=0.58 * inch,
        leftMargin=0.58 * inch,
        topMargin=0.65 * inch,
        bottomMargin=0.7 * inch,
        title=payload.get("title", "Beyond SEO Report"),
        author="Beyond SEO",
    )
    story: list[Any] = []
    branding = payload.get('branding') or {}
    logo = branding.get('logo_path')
    if logo:
        local_logo = Path(logo)
        if not local_logo.is_file() or local_logo.suffix.lower() not in {'.png', '.jpg', '.jpeg'}:
            raise ValueError('Brand logo must be an existing local PNG or JPEG.')
        image = Image(str(local_logo))
        factor = min(120 / image.imageWidth, 45 / image.imageHeight)
        image.drawWidth, image.drawHeight = image.imageWidth * factor, image.imageHeight * factor
        image.hAlign = 'LEFT'
        story.extend([image, Spacer(1, 8)])
    if branding.get('contact'):
        story.append(p(branding['contact'], 'Smallx'))
    if payload.get("demo"):
        story.append(p("DEMONSTRATION DATA - illustrative values, not a website audit", "CoverSub"))

    story.extend([
        Spacer(1, 0.25 * inch),
        CoverIdentity(),
        Spacer(1, 0.4 * inch),
        p(payload.get("client", "SEO Audit"), "CoverTitle"),
        p(payload.get("title", "SEO, AEO and Website Improvement Report"), "CoverSub"),
        Spacer(1, 0.16 * inch),
        p(f"Website: {payload.get('site_url', 'Not provided')}", "CoverSub"),
        p(f"Audit date: {payload.get('audit_date', str(date.today()))} | Mode: {payload.get('audit_mode', 'Not specified')}", "CoverSub"),
        Spacer(1, 0.38 * inch),
        p("THE AUDIT AT A GLANCE", "H2x"),
        p(payload.get("summary", "No executive summary provided.")),
        Spacer(1, 12),
        table([["Overall score", "Audit status", "Findings / review tasks"],
               [payload.get("overall_score") if payload.get("overall_score") is not None else "Not verified",
                payload.get("status", "Not verified"), len(payload.get("findings") or [])]],
              [1.7 * inch, 2.9 * inch, 1.75 * inch]),
        p("DECISION GUIDE", "H2x"),
        p("Read the coverage and evidence first, review the observed findings, then use the action roadmap to assign and validate improvements."),
        p("Scores describe the measured sample. Unavailable data remains Not verified; recommendations do not guarantee ranking or traffic gains.", "Smallx"),
        PageBreak(),
    ])

    story.append(p("Executive Summary", "H1x"))
    story.append(p(payload.get("summary", "No executive summary provided.")))
    ordered = sorted(payload.get('findings') or [], key=lambda f: {'critical': 0, 'high': 1, 'medium': 2, 'low': 3, 'review': 4}.get(str(f.get('priority', '')).lower(), 5))
    if ordered:
        story.append(p('What to Do First', 'H1x'))
        for index, finding in enumerate(ordered[:3], 1):
            story.append(p(f"{index}. {finding.get('issue', 'Review finding')}", 'H2x'))
            story.append(p(finding.get('fix', 'Review evidence before acting.')))
            story.append(p(f"Owner: {finding.get('owner', 'Unassigned')} | Effort: {finding.get('effort', 'Not verified')} | Dependencies: {finding.get('dependencies', 'Not verified')}", 'Smallx'))
            story.append(p(f"Validate: {finding.get('validation_method', 'Define acceptance criteria before implementation.')}", 'Smallx'))

    confidence = payload.get("data_confidence") or []
    if confidence:
        story.append(p("Data Confidence", "H2x"))
        story.append(table(
            [["Level", "Evidence"]] + [[x.get("label", ""), x.get("value", "")] for x in confidence],
            [1.45 * inch, 4.9 * inch],
        ))

    scores = payload.get("scores") or []
    coverage = payload.get("coverage") or {}
    if coverage:
        story.append(p("Audit Coverage and Limits", "H2x"))
        story.append(p(f"Discovered: {coverage.get('discovered_urls', 'Not verified')} | Attempted: {coverage.get('attempted_urls', 'Not verified')} | Successful: {coverage.get('successful_urls', 'Not verified')} | Rendered: {coverage.get('rendered_urls', 0)}"))
        story.append(p(f"Scope: {'Partial audit' if coverage.get('partial', True) else 'Observed crawl sample'} | Stop: {coverage.get('stopping_reason', 'Not recorded')}"))
        story.append(p(coverage.get("limitations", ""), "Smallx"))
    if scores:
        story.append(p("Observed Diagnostic Scorecard", "H1x"))
        rows = [["Area", "Score", "Visual", "Reason"]]
        for row in scores:
            rows.append([
                row.get("area", ""),
                row.get("display", row.get("score", "Not verified")),
                score_bar(row.get("score")),
                row.get("note", ""),
            ])
        story.append(table(rows, [1.45 * inch, 0.85 * inch, 1.3 * inch, 2.75 * inch]))
    methodology = payload.get("score_methodology") or {}
    if methodology:
        story.append(p(f"Rubric {methodology.get('rubric_version')}; tested {methodology.get('tested_checks')} of {methodology.get('eligible_checks')} eligible sample checks; check coverage {methodology.get('check_coverage_percent')}%. Priority URLs carry 3x business weight.", "Smallx"))
        story.append(table([["Check", "Weight", "Tested", "Passed", "Failed"]] + [[x['label'], x['weight'], x['tested_pages'], x['passed_pages'], x['failed_pages']] for x in methodology.get("checks", [])], [2.55 * inch, 0.7 * inch, 1.0 * inch, 1.05 * inch, 1.05 * inch]))

    clarity = payload.get("clarity") or {}
    if clarity:
        story.append(PageBreak())
        story.append(p("Microsoft Clarity Behavior Insights", "H1x"))
        story.append(p(
            "First-party behavior evidence complements GSC, GA4, and CRM data. "
            "It does not establish keyword rankings or prove that a behavior signal caused an SEO outcome."
        ))
        story.append(table(
            [
                ["Source", "Evidence", "Window", "Dimensions"],
                [
                    clarity.get("source", "Microsoft Clarity"),
                    clarity.get("evidence_label", "Not verified"),
                    clarity.get("window", "Not provided"),
                    clarity.get("dimensions", "Not provided"),
                ],
            ],
            [1.9 * inch, 1.45 * inch, 1.65 * inch, 1.35 * inch],
        ))
        if clarity.get("retrieved_at"):
            story.append(p(f"Retrieved: {clarity.get('retrieved_at')}", "Smallx"))
        if clarity.get("limitations"):
            story.append(p(clarity.get("limitations"), "Smallx"))
        clarity_metrics = clarity.get("metrics") or []
        if clarity_metrics:
            story.append(p("Observed Metrics and Segments", "H2x"))
            story.append(table(
                [["Metric", "Segment", "Observed Value", "Evidence"]]
                + [[
                    x.get("metric", ""),
                    x.get("segment", ""),
                    x.get("observed", ""),
                    x.get("evidence_label", clarity.get("evidence_label", "")),
                ] for x in clarity_metrics],
                [1.25 * inch, 1.6 * inch, 2.7 * inch, 0.8 * inch],
            ))
        clarity_signals = clarity.get("signals") or []
        if clarity_signals:
            story.append(p("Behavior Signals to Investigate", "H2x"))
            story.append(table(
                [["Signal", "Scope", "Evidence", "Recommended Investigation"]]
                + [[
                    x.get("signal", ""),
                    x.get("scope", ""),
                    x.get("evidence", ""),
                    x.get("action", ""),
                ] for x in clarity_signals],
                [1.15 * inch, 1.45 * inch, 1.65 * inch, 2.1 * inch],
            ))

    findings = payload.get("findings") or []
    if findings:
        story.append(PageBreak())
        story.append(p("Observed Findings and Review Tasks", "H1x"))
        story.append(table(
            [["Issue", "Evidence", "Priority", "Recommended Fix"]]
            + [[x.get("issue", ""), x.get("evidence", ""), priority_badge(x.get("priority", "")), x.get("fix", "")] for x in findings],
            [1.45 * inch, 2.0 * inch, 0.75 * inch, 2.15 * inch],
        ))
        for finding in findings:
            if finding.get("finding_id"):
                card_start = len(story)
                story.append(table([[finding.get('issue', finding['finding_id']), priority_badge(finding.get('priority'))]], [5.3 * inch, 1.05 * inch], header=False))
                story.append(p(f"{finding['finding_id']} - Evidence and Acceptance", "H2x"))
                story.append(p(f"Affected URLs: {', '.join(finding.get('affected_urls', []))}"))
                story.append(p(f"Action: {finding.get('fix', '')}"))
                story.append(p(f"Effort: {finding.get('effort', 'Not verified')} | Dependencies: {finding.get('dependencies', 'Not verified')}", 'Smallx'))
                story.append(p(f"Observation ({finding['observation_label']}): {finding['observation']}"))
                story.append(p(f"Interpretation ({finding['interpretation_label']}): {finding['interpretation']}"))
                story.append(p(f"Impact: {finding['business_impact']} | Owner: {finding['owner']}"))
                story.append(p(f"Acceptance: {finding['acceptance_criteria']}"))
                story.append(p(f"Validate: {finding['validation_method']}"))
                story.append(p(f"Collected: {finding['collected_at']} | Artifact: {finding['source_artifact']} | Evidence IDs: {', '.join(finding['evidence_ids'][:3])}" , "Smallx"))
                card = story[card_start:]
                del story[card_start:]
                story.append(KeepTogether(card))

    keywords = payload.get("keywords") or []
    if keywords:
        story.append(p("Keyword Opportunity Snapshot", "H1x"))
        story.append(table(
            [["Keyword", "Intent", "Source", "Volume", "Difficulty", "Action", "Confidence"]]
            + [[
                x.get("keyword", ""),
                x.get("intent", ""),
                x.get("source", ""),
                x.get("volume", "Not verified"),
                x.get("difficulty", "Not verified"),
                x.get("action", ""),
                x.get("confidence", ""),
            ] for x in keywords],
            [1.1 * inch, 0.72 * inch, 1.0 * inch, 0.72 * inch, 0.72 * inch, 1.15 * inch, 0.85 * inch],
        ))

    competitors = payload.get("competitors") or []
    if competitors:
        story.append(PageBreak())
        story.append(p("Competitor Gap Dashboard", "H1x"))
        story.append(table(
            [["Competitor", "Evidence", "Gap", "Action"]]
            + [[x.get("competitor", ""), x.get("evidence", ""), x.get("gap", ""), x.get("action", "")] for x in competitors],
            [1.25 * inch, 1.75 * inch, 1.55 * inch, 1.8 * inch],
        ))

    roadmap = payload.get("roadmap") or []
    if roadmap:
        story.append(p("30/60/90-Day Roadmap", "H1x"))
        story.append(table(
            [["Timeframe", "Actions", "Expected Outcome"]]
            + [[x.get("timeframe", ""), x.get("actions", ""), x.get("outcome", "")] for x in roadmap],
            [1.1 * inch, 3.5 * inch, 1.75 * inch],
        ))

    gaps = payload.get("data_gaps") or []
    specialist = payload.get('specialist_reviews') or {}
    international = specialist.get('international', {}).get('issues', [])
    schema_issues = [(row['url'], issue) for row in specialist.get('schema', []) for issue in row.get('issues', [])]
    if international or schema_issues:
        story.append(p('Structured Data and International Review', 'H1x'))
        story.append(p('Review candidates from observed HTML only. These checks do not establish rich-result eligibility, search indexation or ranking impact.'))
        for issue in international:
            story.append(p(f"{issue['url']} | {issue['check']} ({issue['label']}): {issue['detail']}", 'Smallx'))
        for url, issue in schema_issues:
            story.append(p(f"{url} | {issue['check']} ({issue['label']}): {issue['detail']}", 'Smallx'))
    if payload.get('outcomes'):
        from outcome_tracker import assess_outcome
        story.append(p('Implementation and Observed Outcomes', 'H1x'))
        for row in payload['outcomes']:
            outcome = assess_outcome(row)
            story.append(p(row.get('finding_id', 'Tracked change'), 'H2x'))
            story.append(p(f"Implementation: {outcome['implementation_status']} | Measurement: {outcome['measurement_status']} | Absolute change: {outcome['absolute_change']} | Causation: {outcome['causal_claim']}"))
            story.append(p(f"Source: {row.get('source', 'Not verified')} | Before: {row.get('baseline_start', '?')} to {row.get('baseline_end', '?')} | After: {row.get('followup_start', '?')} to {row.get('followup_end', '?')} | Confounders: {row.get('confounders', 'Not verified')}", 'Smallx'))
    for quality in payload.get("first_party_quality", []):
        story.append(p(f"First-Party Data Quality: {quality.get('source', 'Unknown')}", "H2x"))
        story.append(p(f"{quality.get('evidence_label')} | Rows: {quality.get('row_count', 0)} | Window: {quality.get('metadata', {}).get('start_date', 'Unknown')} to {quality.get('metadata', {}).get('end_date', 'Unknown')}"))
        summary = quality.get("summary", {})
        if summary:
            story.append(table([["Observed metric", "Value"]] + [[str(key).replace('_', ' ').capitalize(), value] for key, value in summary.items()], [3.2 * inch, 3.15 * inch]))
        for note in quality.get("errors", []) + quality.get("warnings", []):
            story.append(p(note, "Smallx"))
    if gaps:
        story.append(p("Data Needed Next", "H1x"))
        story.append(table(
            [["Source", "Needed Data"]]
            + [[x.get("source", ""), x.get("needed", "")] for x in gaps],
            [1.7 * inch, 4.65 * inch],
        ))

    sources = payload.get("sources") or []
    if sources:
        story.append(p("Source Links", "H1x"))
        story.append(table(
            [["Source", "URL"]]
            + [[x.get("label", ""), x.get("url", "")] for x in sources],
            [2.0 * inch, 4.35 * inch],
        ))

    doc.build(story, onFirstPage=cover_band, onLaterPages=footer)


def build_and_validate_pdf(
    payload: dict[str, Any],
    output: Path,
    qa_output: Path | None = None,
) -> dict[str, Any]:
    from pdf_qa import inspect_pdf
    if not payload.get("demo"):
        from audit_quality import validate_report
        from evidence_ledger import normalize_record
        records = [normalize_record(row) for row in payload.get("evidence_records", [])]
        validate_report(payload, records)

    build_pdf(payload, output)
    qa_path = qa_output or output.with_suffix(".qa.json")
    result = inspect_pdf(output, qa_path)
    if not result["passed"]:
        raise RuntimeError(f"PDF failed structural QA; see {qa_path}.")
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="Build a Beyond SEO PDF report.")
    parser.add_argument("--input", help="Normalized report JSON path.")
    parser.add_argument("--output", required=True, help="Output PDF path.")
    parser.add_argument("--sample", action="store_true", help="Generate a sample report.")
    parser.add_argument(
        "--qa",
        action="store_true",
        help="Compatibility flag; structural PDF QA is always enforced.",
    )
    args = parser.parse_args()
    payload = load_payload(args.input, args.sample)
    output = Path(args.output)
    try:
        build_and_validate_pdf(payload, output)
    except RuntimeError as exc:
        raise SystemExit(str(exc)) from exc
    print(output.resolve())


if __name__ == "__main__":
    main()
