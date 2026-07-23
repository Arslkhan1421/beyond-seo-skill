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
AMBER = colors.HexColor("#C77D0E")
RED = colors.HexColor("#B94040")
GRAY = colors.HexColor("#AAB5BA")


def sample_payload() -> dict[str, Any]:
    return {
        "title": "SEO, AEO and Website Improvement Audit",
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
            {"label": "Verified", "value": "crawl, sitemap, robots, metadata"},
            {"label": "Sampled", "value": "manual SERP checks"},
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
        alignment=TA_CENTER,
        spaceAfter=14,
    ))
    styles.add(ParagraphStyle(
        name="CoverSub",
        parent=styles["Normal"],
        fontSize=11,
        leading=15,
        textColor=MUTED,
        alignment=TA_CENTER,
    ))
    styles.add(ParagraphStyle(
        name="H1x",
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
        fontSize=9.2,
        leading=12.6,
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
        fontSize=7.7,
        leading=9.8,
        textColor=INK,
    ))
    return styles


STYLES = paragraph_styles()


def p(text: Any, style: str = "Bodyx") -> Paragraph:
    return Paragraph(html.escape(str(text or "")), STYLES[style])


def score_color(score: int | float | None):
    if score is None:
        return GRAY
    if score >= 75:
        return GREEN
    if score >= 55:
        return AMBER
    return RED


def score_bar(score: int | float | None, width: int = 118, height: int = 8) -> Table:
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
        ("GRID", (0, 0), (-1, -1), 0.35, LINE),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]
    if header:
        commands.extend([
            ("BACKGROUND", (0, 0), (-1, 0), BRAND),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ])
    for idx in range(1 if header else 0, len(data)):
        if idx % 2 == 0:
            commands.append(("BACKGROUND", (0, idx), (-1, idx), colors.HexColor("#FAFCFC")))
    return Table(data, colWidths=widths, repeatRows=1 if header else 0, style=TableStyle(commands))


def footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(LINE)
    canvas.line(doc.leftMargin, 0.55 * inch, A4[0] - doc.rightMargin, 0.55 * inch)
    canvas.setFont("Helvetica", 7.5)
    canvas.setFillColor(MUTED)
    canvas.drawString(doc.leftMargin, 0.38 * inch, "Beyond SEO report | evidence-based SEO, AEO, competitor, and conversion audit")
    canvas.drawRightString(A4[0] - doc.rightMargin, 0.38 * inch, f"Page {doc.page}")
    canvas.restoreState()


def cover_band(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(BRAND)
    canvas.rect(0, A4[1] - 0.32 * inch, A4[0], 0.32 * inch, stroke=0, fill=1)
    canvas.rect(0, 0, A4[0], 0.16 * inch, stroke=0, fill=1)
    canvas.restoreState()


def build_pdf(payload: dict[str, Any], output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(
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

    story.extend([
        Spacer(1, 1.25 * inch),
        p(payload.get("client", "SEO Audit"), "CoverTitle"),
        p(payload.get("title", "SEO, AEO and Website Improvement Report"), "CoverSub"),
        Spacer(1, 0.16 * inch),
        p(f"Website: {payload.get('site_url', 'Not provided')}", "CoverSub"),
        p(f"Audit date: {payload.get('audit_date', str(date.today()))} | Mode: {payload.get('audit_mode', 'Not specified')}", "CoverSub"),
        Spacer(1, 0.38 * inch),
        table(
            [
                ["Overall Score", "Status", "Executive Readout"],
                [
                    str(payload.get("overall_score", "Not verified")),
                    payload.get("status", "Not verified"),
                    payload.get("summary", "No executive summary provided."),
                ],
            ],
            [1.15 * inch, 1.2 * inch, 4.0 * inch],
        ),
        PageBreak(),
    ])

    story.append(p("Executive Summary", "H1x"))
    story.append(p(payload.get("summary", "No executive summary provided.")))

    confidence = payload.get("data_confidence") or []
    if confidence:
        story.append(p("Data Confidence", "H2x"))
        story.append(table(
            [["Level", "Evidence"]] + [[x.get("label", ""), x.get("value", "")] for x in confidence],
            [1.45 * inch, 4.9 * inch],
        ))

    scores = payload.get("scores") or []
    if scores:
        story.append(p("SEO Health Dashboard", "H1x"))
        rows = [["Area", "Score", "Visual", "Reason"]]
        for row in scores:
            rows.append([
                row.get("area", ""),
                row.get("display", row.get("score", "Not verified")),
                score_bar(row.get("score")),
                row.get("note", ""),
            ])
        story.append(table(rows, [1.45 * inch, 0.85 * inch, 1.3 * inch, 2.75 * inch]))

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
        story.append(p("Confirmed Findings", "H1x"))
        story.append(table(
            [["Issue", "Evidence", "Priority", "Recommended Fix"]]
            + [[x.get("issue", ""), x.get("evidence", ""), x.get("priority", ""), x.get("fix", "")] for x in findings],
            [1.45 * inch, 2.0 * inch, 0.75 * inch, 2.15 * inch],
        ))

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
            [1.2 * inch, 0.8 * inch, 1.05 * inch, 0.75 * inch, 0.75 * inch, 1.25 * inch, 0.55 * inch],
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
    if gaps:
        story.append(p("Data Needed Next", "H1x"))
        story.append(table(
            [["Source", "Needed Data"]]
            + [[x.get("source", ""), x.get("needed", "")] for x in gaps],
            [1.7 * inch, 4.65 * inch],
        ))

    sources = payload.get("sources") or []
    if sources:
        story.append(PageBreak())
        story.append(p("Source Links", "H1x"))
        story.append(table(
            [["Source", "URL"]]
            + [[x.get("label", ""), x.get("url", "")] for x in sources],
            [2.0 * inch, 4.35 * inch],
        ))

    doc.build(story, onFirstPage=cover_band, onLaterPages=footer)


def main() -> None:
    parser = argparse.ArgumentParser(description="Build a Beyond SEO PDF report.")
    parser.add_argument("--input", help="Normalized report JSON path.")
    parser.add_argument("--output", required=True, help="Output PDF path.")
    parser.add_argument("--sample", action="store_true", help="Generate a sample report.")
    parser.add_argument("--qa", action="store_true", help="Run structural PDF quality checks after generation.")
    args = parser.parse_args()
    payload = load_payload(args.input, args.sample)
    build_pdf(payload, Path(args.output))
    if args.qa:
        from pdf_qa import inspect_pdf
        result = inspect_pdf(Path(args.output), Path(args.output).with_suffix(".qa.json"))
        if not result["passed"]:
            raise SystemExit("PDF generated but failed quality checks. See the .qa.json artifact.")
    print(Path(args.output).resolve())


if __name__ == "__main__":
    main()
