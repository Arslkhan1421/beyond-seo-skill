#!/usr/bin/env python3
"""Classify SEO CSV rows by evidence source and metric confidence.

Usage:
  python tools/source_classifier.py --input semrush.csv --output classified.csv
  python tools/source_classifier.py --input gsc_queries.csv --json
"""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path
from typing import Iterable


FIRST_PARTY = {
    "gsc", "google search console", "ga4", "google analytics", "gbp",
    "google business profile", "bing webmaster tools", "microsoft clarity", "clarity",
}
PAID_TOOLS = {"semrush", "ahrefs", "moz", "dataforseo", "sistrix", "se ranking", "majestic"}
CRAWL_TOOLS = {"screaming frog", "sitebulb", "lumar", "jetoctopus", "crawl"}


def norm(value: str) -> str:
    return " ".join((value or "").strip().lower().replace("_", " ").replace("-", " ").split())


def detect_source(path: Path, headers: Iterable[str], explicit: str | None) -> str:
    if explicit:
        return norm(explicit)
    haystack = " ".join([norm(path.stem), *(norm(h) for h in headers)])
    candidates = [
        "google search console", "gsc", "google analytics", "ga4", "semrush",
        "ahrefs", "dataforseo", "moz", "screaming frog", "sitebulb",
        "microsoft clarity", "clarity", "manual serp", "screenshot",
    ]
    for candidate in candidates:
        if candidate in haystack:
            return candidate
    if {"clicks", "impressions", "ctr", "position"}.issubset(set(norm(h) for h in headers)):
        return "google search console"
    if {"sessions", "users"}.intersection(set(norm(h) for h in headers)) and "conversions" in haystack:
        return "google analytics"
    if {"metric name", "observed value"}.issubset(set(norm(h) for h in headers)):
        return "microsoft clarity"
    return "unknown"


def evidence_level(source: str) -> str:
    source = norm(source)
    if source in FIRST_PARTY:
        return "First-party verified"
    if source in PAID_TOOLS:
        return "Paid-tool verified"
    if source in CRAWL_TOOLS:
        return "Technical crawl verified"
    if "screenshot" in source:
        return "Screenshot verified"
    if "manual serp" in source or "serp sample" in source:
        return "Live SERP sample"
    if "competitor" in source or "page review" in source:
        return "Inferred from competitor page"
    return "Not verified"


def metric_confidence(row: dict[str, str], level: str) -> tuple[str, str]:
    headers = {norm(k): v for k, v in row.items()}
    verified = []
    missing = []
    metric_map = {
        "volume": ["volume", "search volume", "nq"],
        "difficulty": ["keyword difficulty", "difficulty", "kd"],
        "rank": ["position", "rank", "rank absolute", "po"],
        "url": ["url", "ranking url", "address"],
        "traffic": ["traffic", "sessions", "clicks", "users"],
        "authority": ["domain rating", "dr", "domain authority", "da", "authority score", "as"],
        "backlinks": ["backlinks", "referring domains", "linking domains", "inbound links"],
        "conversions": ["conversions", "key events", "goals"],
    }
    for metric, names in metric_map.items():
        value = ""
        for name in names:
            if name in headers:
                value = str(headers.get(name) or "").strip()
                break
        if value and value.lower() not in {"not verified", "n/a", "na", "-"}:
            verified.append(metric)
        else:
            missing.append(metric)
    if level == "First-party verified":
        metric_name = str(headers.get("metric name") or "").strip()
        observed_value = str(headers.get("observed value") or "").strip()
        if metric_name and observed_value:
            verified.append("behavior")
    if level in {"Not verified", "Inferred from competitor page", "Live SERP sample"}:
        restricted = {"volume", "difficulty", "traffic", "authority", "backlinks", "conversions"}
        verified = [m for m in verified if m not in restricted]
        missing = sorted(set(missing).union(restricted))
    return ", ".join(sorted(set(verified))) or "none", ", ".join(sorted(set(missing))) or "none"


def classify(input_path: Path, source: str | None) -> tuple[list[dict[str, str]], dict[str, object]]:
    with input_path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)
        headers = reader.fieldnames or []
    detected = detect_source(input_path, headers, source)
    level = evidence_level(detected)
    output_rows = []
    counts = Counter()
    for row in rows:
        verified, missing = metric_confidence(row, level)
        enriched = dict(row)
        enriched["detected_source"] = detected
        enriched["evidence_level"] = level
        enriched["verified_metrics"] = verified
        enriched["missing_metrics"] = missing
        enriched["confidence_note"] = (
            "Use exact numeric metrics only when present in this source. "
            "Do not fill missing paid-tool or first-party fields from memory."
        )
        output_rows.append(enriched)
        counts[level] += 1
    summary = {
        "input": str(input_path),
        "detected_source": detected,
        "evidence_level": level,
        "rows": len(rows),
        "levels": dict(counts),
    }
    return output_rows, summary


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys()) if rows else [
        "detected_source", "evidence_level", "verified_metrics", "missing_metrics", "confidence_note"
    ]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description="Classify SEO evidence rows by source confidence.")
    parser.add_argument("--input", required=True, help="Input CSV path.")
    parser.add_argument("--output", help="Output classified CSV path.")
    parser.add_argument("--source", help="Explicit source name, e.g. Semrush, Ahrefs, GSC.")
    parser.add_argument("--json", action="store_true", help="Print JSON summary.")
    args = parser.parse_args()
    rows, summary = classify(Path(args.input), args.source)
    if args.output:
        write_csv(Path(args.output), rows)
    if args.json or not args.output:
        print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
