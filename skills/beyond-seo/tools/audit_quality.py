#!/usr/bin/env python3
"""Finding contracts, bounded sample scoring, and reproducibility manifests."""
from __future__ import annotations

import hashlib
import json
import platform
from datetime import datetime
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urlparse

from evidence_ledger import ALLOWED_LABELS, EVIDENCE_SCHEMA
from evidence_ledger import canonical_metric


def validate_findings(findings: list[dict], evidence: list[dict]) -> None:
    records = {row["id"]: row for row in evidence}
    seen = set()
    for row in findings:
        missing = [key for key in EVIDENCE_SCHEMA["finding_required_fields"] if key not in row]
        if missing:
            raise ValueError(f"Finding contract is incomplete: {missing}")
        if row["finding_id"] in seen:
            raise ValueError("Duplicate finding ID.")
        seen.add(row["finding_id"])
        if not row["affected_urls"] or not row["evidence_ids"]:
            raise ValueError("Findings require affected URLs and evidence references.")
        refs = [records.get(key) for key in row["evidence_ids"]]
        if any(ref is None for ref in refs):
            raise ValueError("Finding references missing evidence.")
        for field in ("observation_label", "interpretation_label"):
            if row[field] not in ALLOWED_LABELS:
                raise ValueError(f"Unsupported finding label: {row[field]}")
        if row["observation_label"] == "Confirmed" and any(ref["label"] != "Confirmed" for ref in refs):
            raise ValueError("Confirmed observation requires direct evidence.")
        if set(row["affected_urls"]) - {ref.get("scope") for ref in refs}:
            raise ValueError("Affected URLs are not covered by the referenced evidence scopes.")
        if any(ref.get("artifact_path") != row["source_artifact"] for ref in refs):
            raise ValueError("Finding artifact differs from its evidence references.")
        try:
            timestamp = datetime.fromisoformat(row["collected_at"].replace("Z", "+00:00"))
            if timestamp.tzinfo is None:
                raise ValueError
        except (TypeError, ValueError, AttributeError) as exc:
            raise ValueError("Finding collection time requires an ISO timestamp with timezone.") from exc
        if not row["acceptance_criteria"] or not row["validation_method"]:
            raise ValueError("Finding requires acceptance criteria and a validation method.")


def validate_report(payload: dict, records: list[dict]) -> None:
    validate_findings(payload.get("findings", []), records)
    for row in payload.get("data_confidence", []):
        if row.get("label") not in ALLOWED_LABELS:
            raise ValueError("Report contains an unsupported evidence label.")
    for row in payload.get("keywords", []):
        for field, metric in (("volume", "keyword_volume"), ("difficulty", "keyword_difficulty")):
            value = row.get(field)
            if value in (None, "", "Not verified"):
                continue
            try:
                numeric = float(value)
            except (TypeError, ValueError) as exc:
                raise ValueError("Keyword numeric metrics need exact sourced values, not ranges or estimates without provenance.") from exc
            matches = [record for record in records if canonical_metric(record.get("metric")) == metric and record.get("scope") == row.get("keyword") and record.get("value") is not None]
            if not any(float(record["value"]) == numeric for record in matches):
                raise ValueError(f"Keyword {field} lacks matching evidence for its keyword scope.")
    rubric = payload.get("score_methodology")
    if rubric:
        earned, possible = rubric.get("earned_weight", 0), rubric.get("possible_weight", 0)
        expected = round(100 * earned / possible, 1) if possible else None
        if earned < 0 or possible < earned or rubric.get("score") != expected:
            raise ValueError("Diagnostic score does not match the recorded weighted rubric.")
        if payload.get("overall_score") is not None:
            raise ValueError("Sample rubric cannot authorize an overall SEO score.")
        if any(row.get("score") != expected for row in payload.get("scores", [])):
            raise ValueError("Displayed sample score differs from its rubric.")


def sample_score(pages: list[dict], config: dict) -> dict:
    """Heuristic rubric; never claims to measure rankings or overall SEO health."""
    priorities = set(config.get("priority_urls", []))
    checks = []
    specs = [
        ("http-availability", "HTTP availability", 4, "High", lambda p: p.get("status") == 200),
        ("title-presence", "HTML title presence", 2, "Medium", lambda p: bool(p.get("title"))),
        ("h1-presence", "HTML H1 presence", 1, "Low", lambda p: bool(p.get("h1"))),
        ("priority-noindex", "Intended search pages without detected noindex", 5, "High", lambda p: not p.get("noindex")),
    ]
    earned = possible = 0
    tested = eligible = 0
    for check_id, label, weight, severity, predicate in specs:
        observed = passed = 0
        for page in pages:
            priority = page.get("url") in priorities
            if check_id == "priority-noindex" and not priority:
                continue
            eligible += 1
            known = page.get("status") is not None
            if check_id != "http-availability":
                known = known and page.get("status") == 200 and page.get("is_html", False)
            if not known:
                continue
            importance = 3 if priority else 1
            contribution = weight * importance
            possible += contribution
            observed += 1
            tested += 1
            if predicate(page):
                passed += 1
                earned += contribution
        checks.append({"check_id": check_id, "label": label, "severity": severity, "weight": weight,
                       "tested_pages": observed, "passed_pages": passed, "failed_pages": observed - passed})
    return {
        "rubric_version": "1.4.0", "scope": "Observed crawl sample only",
        "score": round(100 * earned / possible, 1) if possible else None,
        "earned_weight": earned, "possible_weight": possible,
        "tested_checks": tested, "eligible_checks": eligible,
        "check_coverage_percent": round(100 * tested / eligible, 1) if eligible else None,
        "checks": checks,
        "limitations": "Heuristic sample diagnostic, not a Google metric or overall SEO score. Canonical absence, word count, sitemap absence and duplicates require contextual review and are not automatic penalties. Unknown checks are excluded. Priority URLs are owner-designated and weighted 3x.",
    }


def safe_config(value, key: str = ""):
    """Persist reproducibility settings without credential values or URL identifiers."""
    import re
    if re.search(r"token|password|secret|api.?key|authorization|cookie", key, re.I):
        return "[redacted]"
    if isinstance(value, dict):
        return {k: safe_config(v, k) for k, v in value.items()}
    if isinstance(value, list):
        return [safe_config(v, key) for v in value]
    if isinstance(value, str) and value.startswith(("http://", "https://")):
        parsed = urlparse(value)
        return parsed._replace(netloc=parsed.netloc.split("@")[-1], query="", fragment="").geturl()
    return value


def sanitize_artifact(value, key: str = ""):
    """Redact credential fields/known credentials and sensitive URL parameters."""
    import os
    import re
    sensitive = re.compile(r"token|password|secret|api.?key|authorization|cookie|session.?id|email|phone", re.I)
    if sensitive.search(key) and not key.endswith("_env"):
        return "[redacted]"
    if isinstance(value, dict):
        return {k: sanitize_artifact(v, str(k)) for k, v in value.items()}
    if isinstance(value, list):
        return [sanitize_artifact(v, key) for v in value]
    if isinstance(value, str):
        for name in ("APIFY_API_TOKEN", "CLARITY_API_TOKEN", "PAGESPEED_API_KEY"):
            secret = os.getenv(name)
            if secret:
                value = value.replace(secret, "[redacted]")
        if value.startswith(("http://", "https://")):
            parsed = urlparse(value)
            pairs = parse_qsl(parsed.query, keep_blank_values=True)
            if any(sensitive.search(k) for k, _ in pairs) or "@" in parsed.netloc:
                query = urlencode([(k, "[redacted]" if sensitive.search(k) else v) for k, v in pairs])
                value = parsed._replace(netloc=parsed.netloc.split("@")[-1], query=query).geturl()
    return value


def write_reproducibility(output: Path, config: dict, collected_at: str) -> dict:
    config_path = output / "audit-config.sanitized.json"
    config_path.write_text(json.dumps(safe_config(config), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    packages = {}
    for name in ("requests", "beautifulsoup4", "reportlab", "pypdf"):
        try:
            packages[name] = version(name)
        except PackageNotFoundError:
            packages[name] = "Unavailable"
    # Explicit allowlist: never sweep unrelated files, user exports or old runs into a bundle.
    names = ["audit-data.json", "crawl-observations.json", "crawl-coverage.json", "evidence-ledger.json",
             "evidence-ledger.csv", "report-input.json", "competitor-classification.json", "audit-comparison.json",
             "first-party-quality.json", "audit-config.sanitized.json", "apify-serp-raw.json",
             "clarity-live-insights.json", "beyond-seo-audit.pdf", "beyond-seo-audit.qa.json"]
    artifacts = [{"path": name, "sha256": hashlib.sha256((output / name).read_bytes()).hexdigest(),
                  "bytes": (output / name).stat().st_size} for name in names if (output / name).is_file()]
    payload = {"schema_version": "1.4.0", "collected_at": collected_at, "python": platform.python_version(),
               "packages": packages, "artifacts": artifacts,
               "source_code_sha256": {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(Path(__file__).parent.glob("*.py"))},
               "limitations": "Contains parsed observations and sanitized exports; original private source exports and full HTML are not bundled. Query parameters are redacted from persisted config; preserve private originals locally if exact replay needs them."}
    (output / "reproducibility-manifest.json").write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return payload
