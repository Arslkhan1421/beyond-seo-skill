#!/usr/bin/env python3
"""Export and normalize Microsoft Clarity live insights without exposing tokens."""

from __future__ import annotations

import argparse
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit, urlunsplit

import requests


ENDPOINT = "https://www.clarity.ms/export-data/api/v1/project-live-insights"
DOCS_URL = "https://learn.microsoft.com/en-us/clarity/setup-and-installation/clarity-data-export-api"
ALLOWED_DIMENSIONS = {
    "Browser", "Device", "Country/Region", "OS", "Source",
    "Medium", "Campaign", "Channel", "URL",
}
FRICTION_METRICS = {
    "Dead Click Count": "Inspect apparently interactive elements and delayed responses.",
    "Excessive Scroll": "Review content findability, hierarchy, and page length.",
    "Rage Click Count": "Inspect repeated clicks, latency, overlays, and misleading controls.",
    "Quickback Click": "Review destination relevance, navigation labels, and page expectations.",
    "Script Error Count": "Reproduce and fix client-side errors on the affected page or segment.",
    "Error Click Count": "Inspect clicks associated with an error state.",
}
SENSITIVE_KEY_PARTS = {"email", "userhint", "customid", "custom id", "sessionid", "session id"}


def validate_request(num_days: int, dimensions: list[str]) -> None:
    if num_days not in {1, 2, 3}:
        raise ValueError("Microsoft Clarity num_days must be 1, 2, or 3.")
    if len(dimensions) > 3:
        raise ValueError("Microsoft Clarity accepts at most three dimensions per request.")
    unsupported = [item for item in dimensions if item not in ALLOWED_DIMENSIONS]
    if unsupported:
        raise ValueError(f"Unsupported Microsoft Clarity dimensions: {', '.join(unsupported)}")


def _information_rows(payload: Any) -> list[tuple[str, dict[str, Any]]]:
    rows: list[tuple[str, dict[str, Any]]] = []
    if not isinstance(payload, list):
        return rows
    for metric_group in payload:
        if not isinstance(metric_group, dict):
            continue
        metric_name = str(metric_group.get("metricName") or "Unnamed metric")
        information = metric_group.get("information") or []
        if isinstance(information, dict):
            information = [information]
        for item in information:
            if isinstance(item, dict):
                rows.append((metric_name, item))
    return rows


def _has_positive_number(item: dict[str, Any]) -> bool:
    for value in item.values():
        try:
            if float(str(value).replace(",", "")) > 0:
                return True
        except (TypeError, ValueError):
            continue
    return False


def _safe_value(key: str, value: Any) -> str:
    normalized_key = " ".join(str(key).lower().replace("_", " ").split())
    if any(part in normalized_key for part in SENSITIVE_KEY_PARTS):
        return "[redacted]"
    text = str(value)
    if "url" in normalized_key:
        try:
            parsed = urlsplit(text)
            if parsed.scheme or parsed.netloc:
                return urlunsplit((parsed.scheme, parsed.netloc, parsed.path, "", ""))
            return text.split("?", 1)[0].split("#", 1)[0]
        except ValueError:
            return text.split("?", 1)[0].split("#", 1)[0]
    return text


def build_report_section(export: dict[str, Any], max_rows: int = 30) -> dict[str, Any]:
    dimensions = export.get("dimensions") or []
    metric_rows = []
    signals = []
    for metric_name, item in _information_rows(export.get("data")):
        segments = [
            f"{name}: {_safe_value(name, item[name])}"
            for name in dimensions if item.get(name) not in {None, ""}
        ]
        values = [
            f"{key}: {_safe_value(key, value)}"
            for key, value in item.items() if key not in dimensions
        ]
        row = {
            "metric": metric_name,
            "segment": "; ".join(segments) or "All returned traffic",
            "observed": "; ".join(values) or "No numeric fields returned",
            "evidence_label": "First-party verified",
        }
        if len(metric_rows) < max_rows:
            metric_rows.append(row)
        if metric_name in FRICTION_METRICS and _has_positive_number(item) and len(signals) < 15:
            signals.append({
                "signal": metric_name,
                "scope": row["segment"],
                "evidence": row["observed"],
                "action": FRICTION_METRICS[metric_name],
            })
    return {
        "source": "Microsoft Clarity Data Export API",
        "source_url": DOCS_URL,
        "evidence_label": "First-party verified",
        "retrieved_at": export.get("retrieved_at"),
        "window": f"Previous {export.get('num_days')} day(s), UTC",
        "dimensions": ", ".join(dimensions) or "None",
        "metrics": metric_rows,
        "signals": signals,
        "limitations": (
            "Short-window behavior snapshot: 1–3 days, up to three dimensions, "
            "1,000 rows without pagination, and 10 requests per project per day. "
            "Signals support investigation and do not prove SEO causation."
        ),
    }


def normalize_export(payload: Any, num_days: int, dimensions: list[str]) -> dict[str, Any]:
    validate_request(num_days, dimensions)
    export = {
        "source": "Microsoft Clarity Data Export API",
        "source_url": DOCS_URL,
        "evidence_label": "First-party verified",
        "retrieved_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "num_days": num_days,
        "dimensions": dimensions,
        "api_limits": {
            "requests_per_project_per_day": 10,
            "maximum_rows": 1000,
            "pagination": False,
        },
        "data": payload,
    }
    export["report_section"] = build_report_section(export)
    return export


def collect(
    token: str,
    num_days: int = 3,
    dimensions: list[str] | None = None,
    timeout: int = 30,
) -> dict[str, Any]:
    dimensions = dimensions or ["URL"]
    validate_request(num_days, dimensions)
    params: dict[str, Any] = {"numOfDays": num_days}
    for index, dimension in enumerate(dimensions, 1):
        params[f"dimension{index}"] = dimension
    response = requests.get(
        ENDPOINT,
        params=params,
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
        timeout=timeout,
    )
    if response.status_code == 429:
        raise RuntimeError("Microsoft Clarity daily export limit was reached; use a saved export or retry tomorrow.")
    if response.status_code in {401, 403}:
        raise RuntimeError("Microsoft Clarity authentication failed; verify the project-admin export token.")
    response.raise_for_status()
    return normalize_export(response.json(), num_days, dimensions)


def main() -> None:
    parser = argparse.ArgumentParser(description="Export Microsoft Clarity live insights safely.")
    parser.add_argument("--output", required=True, help="Output JSON path.")
    parser.add_argument("--input", help="Normalize an existing raw Clarity JSON export instead of calling the API.")
    parser.add_argument("--days", type=int, default=3, choices=[1, 2, 3])
    parser.add_argument("--dimension", action="append", default=[], help="Repeat up to three times.")
    parser.add_argument("--token-env", default="CLARITY_API_TOKEN")
    args = parser.parse_args()
    dimensions = args.dimension or ["URL"]
    if args.input:
        raw = json.loads(Path(args.input).read_text(encoding="utf-8"))
        export = normalize_export(raw, args.days, dimensions)
    else:
        token = os.getenv(args.token_env)
        if not token:
            raise SystemExit(f"{args.token_env} is not configured. Token value was not printed.")
        export = collect(token, args.days, dimensions)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(export, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(output.resolve())


if __name__ == "__main__":
    main()
