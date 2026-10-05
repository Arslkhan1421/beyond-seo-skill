#!/usr/bin/env python3
"""Qualify realistic SEO competitors and exclude platforms/directories."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from urllib.parse import urlparse


BLOCKED_DOMAINS = {
    "amazon.com", "apple.com", "facebook.com", "github.com", "google.com",
    "ibm.com", "linkedin.com", "microsoft.com", "oracle.com", "reddit.com",
    "salesforce.com", "wikipedia.org", "youtube.com", "upwork.com", "fiverr.com",
}
DIRECTORY_MARKERS = {
    "clutch", "designrush", "goodfirms", "g2", "capterra", "sortlist",
    "topdevelopers", "businessofapps", "agencyspotter",
}


def domain_of(row: dict) -> str:
    raw = row.get("domain") or row.get("url") or row.get("ranking_url") or ""
    if "://" in raw:
        raw = urlparse(raw).netloc
    return raw.lower().removeprefix("www.").split(":")[0]


def qualify(row: dict, context: dict) -> dict:
    domain = domain_of(row)
    reasons: list[str] = []
    excluded = False
    if not domain:
        excluded, reasons = True, ["missing domain"]
    if domain in BLOCKED_DOMAINS or any(domain.endswith(f".{item}") for item in BLOCKED_DOMAINS):
        excluded, reasons = True, ["giant platform or non-comparable ecosystem"]
    if any(marker in domain for marker in DIRECTORY_MARKERS):
        excluded, reasons = True, ["directory or marketplace"]

    services = {str(x).lower() for x in context.get("services", [])}
    text = " ".join(str(row.get(key, "")).lower() for key in (
        "title", "description", "service_focus", "keyword", "ranking_keyword"
    ))
    overlap = sum(1 for service in services if service and service in text)
    appearances = int(row.get("serp_appearances") or 1)
    position = int(row.get("observed_position") or row.get("position") or 100)
    score = min(30, overlap * 15) + min(25, appearances * 5) + (25 if position <= 3 else 15 if position <= 10 else 0)
    business_model_match = row.get("business_model_match")
    if business_model_match is True:
        score += 20
    if excluded:
        score = 0
    classification = "Comparable" if score >= 45 and not excluded else "Content competitor" if score >= 25 and not excluded else "Excluded"
    if not reasons:
        reasons.append(f"service overlap={overlap}; sampled position={position}")
        if business_model_match is not True:
            reasons.append("business model match not verified")
    return {**row, "domain": domain, "qualification_score": score, "classification": classification, "qualification_reason": "; ".join(reasons)}


def classify(rows: list[dict], context: dict) -> dict:
    results = [qualify(row, context) for row in rows]
    results.sort(key=lambda row: (-row["qualification_score"], row["domain"]))
    return {
        "comparable": [row for row in results if row["classification"] == "Comparable"],
        "content_competitors": [row for row in results if row["classification"] == "Content competitor"],
        "excluded": [row for row in results if row["classification"] == "Excluded"],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Qualify realistic SEO competitors.")
    parser.add_argument("--input", required=True)
    parser.add_argument("--context", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    result = classify(
        json.loads(Path(args.input).read_text(encoding="utf-8")),
        json.loads(Path(args.context).read_text(encoding="utf-8")),
    )
    Path(args.output).write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({key: len(value) for key, value in result.items()}))


if __name__ == "__main__":
    main()
