#!/usr/bin/env python3
"""Validate normalized GSC/GA4 CSVs without guessing provenance or missing values."""
from __future__ import annotations

import argparse
import csv
import json
import math
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError
from urllib.parse import urlparse


def validate_export(path: Path, metadata: dict, website_url: str | None = None) -> dict:
    errors, warnings = [], []
    if not isinstance(metadata, dict):
        return {"source": "Unknown", "passed": False, "evidence_label": "Not verified", "summary": {}, "errors": ["Metadata must be an object."], "warnings": [], "row_count": 0}
    source = metadata.get("source")
    if not isinstance(source, str) or source not in {"gsc", "ga4"}:
        errors.append("Supported normalized sources are gsc and ga4; normalize other exports explicitly.")
    required = ["source", "provenance", "property", "retrieved_at", "start_date", "end_date", "timezone", "dimensions", "filters"]
    errors.extend(f"Missing metadata: {key}" for key in required if key not in metadata or metadata[key] in (None, ""))
    if not isinstance(metadata.get("provenance"), str) or metadata.get("provenance") not in {"owner_export", "authenticated_api"}:
        errors.append("Verified source requires owner_export or authenticated_api provenance.")
    if not isinstance(metadata.get("dimensions"), list) or not metadata.get("dimensions") or any(not isinstance(dim, str) or not dim for dim in metadata.get("dimensions", [])):
        errors.append("dimensions must be an explicit nonempty list.")
    if not isinstance(metadata.get("filters"), dict):
        errors.append("filters must be an explicit object, including {} when no filters apply.")
    try:
        start, end = date.fromisoformat(metadata["start_date"]), date.fromisoformat(metadata["end_date"])
        if end < start:
            errors.append("Measurement window ends before it starts.")
        timestamp = datetime.fromisoformat(metadata["retrieved_at"].replace("Z", "+00:00"))
        if timestamp.tzinfo is None:
            errors.append("retrieved_at requires a timezone offset.")
        if timestamp.date() < end:
            errors.append("Retrieval predates the measurement end.")
    except (KeyError, TypeError, ValueError, AttributeError):
        errors.append("Dates or retrieval timestamp are invalid.")
    try:
        ZoneInfo(metadata.get("timezone", ""))
    except (ZoneInfoNotFoundError, ValueError, TypeError):
        errors.append("timezone must be a supported IANA timezone.")
    dimensions = metadata.get("dimensions") if isinstance(metadata.get("dimensions"), list) and all(isinstance(dim, str) for dim in metadata.get("dimensions", [])) else []
    metrics = ["clicks", "impressions", "ctr", "position"] if source == "gsc" else ["sessions", "key_events"]
    numeric_sums = {metric: 0.0 for metric in metrics if metric not in {"ctr", "position"}}
    rows = 0
    keys = set()
    try:
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            headers = reader.fieldnames or []
            if len(headers) != len(set(headers)):
                errors.append("Duplicate CSV headers are ambiguous.")
            missing = set(metrics + dimensions) - set(headers)
            if missing:
                errors.append(f"Missing normalized columns: {sorted(missing)}")
            for row in reader:
                rows += 1
                if None in row or any(row.get(key) in (None, "") for key in metrics + dimensions):
                    errors.append(f"Row {rows}: malformed row or missing required values.")
                    continue
                key = tuple(row.get(dim) for dim in dimensions)
                if key in keys:
                    errors.append(f"Row {rows}: duplicate dimension key; reconcile overlapping exports before summing.")
                keys.add(key)
                try:
                    values = {name: float(row[name]) for name in metrics}
                    if any(not math.isfinite(value) or value < 0 for value in values.values()):
                        raise ValueError
                    if source == "gsc":
                        if values["ctr"] > 1 or values["clicks"] > values["impressions"]:
                            raise ValueError
                        if values["impressions"] > 0 and values["position"] < 1:
                            raise ValueError
                        if values["impressions"] and abs(values["ctr"] - values["clicks"] / values["impressions"]) > 0.005:
                            errors.append(f"Row {rows}: CTR does not match clicks/impressions; use a 0-1 ratio, not a percent string.")
                    for metric in numeric_sums:
                        numeric_sums[metric] += values[metric]
                except (ValueError, TypeError):
                    errors.append(f"Row {rows}: metrics must be finite nonnegative numbers with compatible units.")
    except (OSError, csv.Error, UnicodeError):
        errors.append("CSV could not be read.")
    if not rows:
        errors.append("Export contains no data rows; missing data is not zero performance.")
    if source == "ga4" and not metadata.get("key_event_definition"):
        errors.append("GA4 key_events require an explicit configured event definition; they are not automatically qualified leads.")
    if website_url:
        target_host = (urlparse(website_url).hostname or "").lower().removeprefix("www.")
        declared = metadata.get("website_url") or (metadata.get("property", "") if source == "gsc" else "")
        declared = declared if isinstance(declared, str) else ""
        if declared.startswith("sc-domain:"):
            source_host = declared.removeprefix("sc-domain:").lower().removeprefix("www.")
        else:
            source_host = (urlparse(declared).hostname or "").lower().removeprefix("www.")
        if source_host != target_host:
            errors.append("Export property/site mapping does not match the audit target; provide explicit verified website_url metadata.")
        if source == "gsc":
            property_value = metadata.get("property", "")
            property_value = property_value if isinstance(property_value, str) else ""
            property_host = property_value.removeprefix("sc-domain:").lower().removeprefix("www.") if property_value.startswith("sc-domain:") else (urlparse(property_value).hostname or "").lower().removeprefix("www.")
            if property_host != target_host and not (property_value.startswith("sc-domain:") and target_host.endswith("." + property_host)):
                errors.append("GSC property does not cover the target website; website_url cannot override an unrelated property.")
    if source == "gsc":
        warnings += ["Anonymized queries and export limits can omit rows. Row totals may not match property totals.",
                     "Average position is an aggregated observation, not a fixed rank. Do not average exported averages without compatible weights.",
                     "Page performance is normally attributed to Google-selected canonicals; reconcile before joining crawl URLs."]
    else:
        warnings += ["Check consent, thresholding, attribution model and channel definitions before reconciling with GSC or CRM."]
    warnings.append("Verification describes source provenance and normalized data validity; supplied metadata is not independently authenticated by this validator.")
    summaries = {}
    if not errors:
        summaries.update(numeric_sums)
        if source == "gsc":
            summaries["ctr"] = numeric_sums["clicks"] / numeric_sums["impressions"] if numeric_sums["impressions"] else None
        total = metadata.get("property_total_clicks")
        if source == "gsc" and total is not None:
            try:
                total = float(total)
                if not math.isfinite(total) or total < numeric_sums["clicks"]:
                    raise ValueError
                summaries["exported_click_coverage_percent"] = 100 * numeric_sums["clicks"] / total if total else None
            except (TypeError, ValueError):
                errors.append("property_total_clicks must be a compatible finite total at least as large as exported clicks.")
    return {"source": source, "evidence_label": "First-party verified" if not errors else "Not verified",
            "passed": not errors, "metadata": metadata, "row_count": rows,
            "summary": summaries if not errors else {}, "errors": errors, "warnings": warnings}


def comparison_compatibility(previous: dict, current: dict) -> list[str]:
    """Prevent mixing properties, dimensions or unequal windows silently."""
    reasons = []
    for key in ("source", "property", "timezone", "dimensions", "filters", "search_type", "key_event_definition", "attribution_model"):
        if previous.get(key) != current.get(key):
            reasons.append(f"Different {key}")
    try:
        windows = [(date.fromisoformat(meta["start_date"]), date.fromisoformat(meta["end_date"])) for meta in (previous, current)]
        if (windows[0][1] - windows[0][0]) != (windows[1][1] - windows[1][0]):
            reasons.append("Unequal measurement window lengths")
        if max(w[0] for w in windows) <= min(w[1] for w in windows):
            reasons.append("Overlapping measurement windows")
    except (KeyError, TypeError, ValueError):
        reasons.append("Measurement dates not verified")
    return reasons


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True)
    parser.add_argument("--metadata", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--website", help="Optional audit target for property/site compatibility validation.")
    args = parser.parse_args()
    result = validate_export(Path(args.input), json.loads(Path(args.metadata).read_text(encoding="utf-8")), args.website)
    Path(args.output).write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"passed": result["passed"], "rows": result["row_count"]}))
    if not result["passed"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
