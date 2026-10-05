#!/usr/bin/env python3
"""Export and normalize Microsoft Clarity live insights without exposing tokens."""

from __future__ import annotations

import argparse
import csv
import ipaddress
import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import unquote, urlsplit, urlunsplit

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
SENSITIVE_KEY_PARTS = {
    "email", "userhint", "customid", "sessionid", "userid", "visitorid",
    "recordingid", "ipaddress", "clientid", "deviceid", "accountid",
}
SAVED_EXPORT_PROVENANCE = "owner_export"
ALLOWED_AGGREGATE_KEYS = {
    "activetime",
    "deadclickcount",
    "distinctusercount",
    "engagementtime",
    "errorclickcount",
    "excessivescrollcount",
    "observedvalue",
    "pagespersessionpercentage",
    "quickbackclickcount",
    "rageclickcount",
    "scripterrorcount",
    "scrolldepth",
    "sessionswithmetriccount",
    "sessionswithmetricpercentage",
    "totalbotsessioncount",
    "totalscreencount",
    "totalsessioncount",
}
EMAIL_PATTERN = re.compile(r"(?<![\w.+-])[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}(?![\w.-])")


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
    compact_key = normalized_key.replace(" ", "").replace("-", "")
    if any(part in compact_key for part in SENSITIVE_KEY_PARTS):
        return "[redacted]"
    text = str(value)
    parsed = urlsplit(text)
    if "url" in normalized_key or parsed.scheme or parsed.netloc:
        return _safe_url(text)
    if EMAIL_PATTERN.search(text):
        return "[redacted]"
    try:
        if ipaddress.ip_address(text.strip()).version in {4, 6}:
            return "[redacted]"
    except ValueError:
        pass
    return text


def _compact_key(key: Any) -> str:
    return re.sub(r"[^a-z0-9]+", "", str(key).lower())


def _is_sensitive_key(key: Any) -> bool:
    compact = _compact_key(key)
    return any(part in compact for part in SENSITIVE_KEY_PARTS)


def _sensitive_path_segment(segment: str) -> bool:
    decoded = unquote(segment).strip()
    if not decoded:
        return False
    if EMAIL_PATTERN.search(decoded):
        return True
    try:
        ipaddress.ip_address(decoded)
        return True
    except ValueError:
        pass
    compact = re.sub(r"[^A-Za-z0-9]+", "", decoded)
    return (compact.isdigit() and len(compact) >= 4) or len(compact) >= 20


def _safe_url(value: str) -> str:
    try:
        parsed = urlsplit(value)
        safe_segments = [
            "[redacted]" if _sensitive_path_segment(segment) else segment
            for segment in parsed.path.split("/")
        ]
        safe_path = "/".join(safe_segments)
        if not (parsed.scheme or parsed.netloc):
            return safe_path
        hostname = parsed.hostname or ""
        if ":" in hostname and not hostname.startswith("["):
            hostname = f"[{hostname}]"
        port = parsed.port
        netloc = f"{hostname}:{port}" if port else hostname
        return urlunsplit((parsed.scheme, netloc, safe_path, "", ""))
    except ValueError:
        return "[redacted-url]"


def _is_aggregate_value(key: Any, value: Any) -> bool:
    compact = _compact_key(key)
    if compact not in ALLOWED_AGGREGATE_KEYS:
        return False
    if isinstance(value, bool) or value is None:
        return False
    if isinstance(value, (int, float)):
        return True
    text = str(value).strip().replace(",", "").removesuffix("%")
    try:
        float(text)
        return True
    except ValueError:
        return False


def _sanitize_clarity_payload(payload: list[Any], dimensions: list[str]) -> list[dict[str, Any]]:
    sanitized: list[dict[str, Any]] = []
    dimension_set = set(dimensions)
    for group in payload:
        if not isinstance(group, dict):
            continue
        information = group.get("information") or []
        if isinstance(information, dict):
            information = [information]
        safe_rows = []
        for item in information:
            if not isinstance(item, dict):
                continue
            safe_item: dict[str, Any] = {}
            for raw_key, value in item.items():
                key = str(raw_key)
                if _is_sensitive_key(key):
                    continue
                if key in dimension_set:
                    safe_item[key] = _safe_value(key, value)
                elif _is_aggregate_value(key, value):
                    safe_item[key] = value
            safe_rows.append(safe_item)
        sanitized.append({
            "metricName": _safe_value("metricName", group.get("metricName") or "Unnamed metric"),
            "information": safe_rows,
        })
    return sanitized


def _validated_retrieved_at(value: Any) -> str:
    text = str(value or "").strip().replace("Z", "+00:00")
    if not text:
        raise ValueError("Saved Microsoft Clarity exports require retrieved_at in UTC.")
    try:
        parsed = datetime.fromisoformat(text)
    except ValueError as exc:
        raise ValueError("Saved Microsoft Clarity retrieved_at must be an ISO-8601 timestamp.") from exc
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise ValueError("Saved Microsoft Clarity retrieved_at must include a UTC offset.")
    return parsed.astimezone(timezone.utc).replace(microsecond=0).isoformat()


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


def normalize_export(
    payload: Any,
    num_days: int,
    dimensions: list[str],
    retrieved_at: str | None = None,
    provenance: str = "authenticated_api",
) -> dict[str, Any]:
    validate_request(num_days, dimensions)
    if not isinstance(payload, list):
        raise ValueError("Microsoft Clarity export data must be a list of metric groups.")
    if provenance not in {"authenticated_api", SAVED_EXPORT_PROVENANCE}:
        raise ValueError("Unsupported Microsoft Clarity export provenance.")
    if provenance == SAVED_EXPORT_PROVENANCE:
        retrieved_at = _validated_retrieved_at(retrieved_at)
    else:
        retrieved_at = retrieved_at or datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    export = {
        "source": "Microsoft Clarity Data Export API",
        "source_url": DOCS_URL,
        "evidence_label": "First-party verified",
        "retrieved_at": retrieved_at,
        "provenance": provenance,
        "num_days": num_days,
        "dimensions": dimensions,
        "api_limits": {
            "requests_per_project_per_day": 10,
            "maximum_rows": 1000,
            "pagination": False,
        },
        "data": _sanitize_clarity_payload(payload, dimensions),
    }
    export["report_section"] = build_report_section(export)
    return export


def load_saved_export(path: Path, default_num_days: int, default_dimensions: list[str]) -> dict[str, Any]:
    if path.suffix.lower() == ".csv":
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            rows = list(reader)
            headers = set(reader.fieldnames or [])
        required_headers = {"retrieved_at_utc", "window_days", "metric_name", "observed_value"}
        missing_headers = sorted(required_headers - headers)
        if missing_headers:
            raise ValueError(
                f"Saved Microsoft Clarity CSV is missing required columns: {', '.join(missing_headers)}"
            )
        if not rows:
            raise ValueError("Saved Microsoft Clarity CSV export is empty.")
        retrieved_values = {str(row.get("retrieved_at_utc") or "").strip() for row in rows}
        window_values = {str(row.get("window_days") or "").strip() for row in rows}
        if len(retrieved_values) != 1 or len(window_values) != 1:
            raise ValueError("Saved Microsoft Clarity CSV rows must share one retrieval time and window.")
        retrieved_at = _validated_retrieved_at(next(iter(retrieved_values)))
        try:
            num_days = int(next(iter(window_values)))
        except ValueError as exc:
            raise ValueError("Saved Microsoft Clarity CSV window_days must be 1, 2, or 3.") from exc
        data: list[dict[str, Any]] = []
        grouped: dict[str, list[dict[str, Any]]] = {}
        imported_dimensions: list[str] = []
        for row in rows:
            metric_name = str(row.get("metric_name") or "").strip()
            if not metric_name:
                raise ValueError("Every Microsoft Clarity CSV row requires metric_name.")
            dimension = str(row.get("dimension") or "").strip()
            item: dict[str, Any] = {"observedValue": row.get("observed_value", "")}
            if dimension:
                if dimension not in ALLOWED_DIMENSIONS:
                    raise ValueError(f"Unsupported Microsoft Clarity CSV dimension: {dimension}")
                if dimension not in imported_dimensions:
                    imported_dimensions.append(dimension)
                dimension_column = "url" if dimension == "URL" else dimension
                item[dimension] = row.get(dimension_column, row.get(dimension_column.lower(), ""))
            grouped.setdefault(metric_name, []).append(item)
        data = [{"metricName": name, "information": information} for name, information in grouped.items()]
        dimensions = imported_dimensions or [item for item in default_dimensions if item]
        return normalize_export(data, num_days, dimensions, retrieved_at, SAVED_EXPORT_PROVENANCE)

    saved = json.loads(path.read_text(encoding="utf-8"))
    required_fields = {"retrieved_at", "num_days", "dimensions", "data"}
    if not isinstance(saved, dict) or not required_fields.issubset(saved):
        raise ValueError(
            "Saved Microsoft Clarity JSON must include retrieved_at, num_days, dimensions, and data."
        )
    num_days = int(saved.get("num_days", default_num_days))
    dimensions = saved.get("dimensions") or default_dimensions
    if not isinstance(dimensions, list):
        raise ValueError("Saved Microsoft Clarity dimensions must be a list.")
    return normalize_export(
        saved.get("data"),
        num_days,
        [str(item) for item in dimensions],
        str(saved.get("retrieved_at") or ""),
        SAVED_EXPORT_PROVENANCE,
    )


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
    parser.add_argument("--input", help="Normalize an existing raw Clarity JSON or CSV export instead of calling the API.")
    parser.add_argument("--days", type=int, default=3, choices=[1, 2, 3])
    parser.add_argument("--dimension", action="append", default=[], help="Repeat up to three times.")
    parser.add_argument("--token-env", default="CLARITY_API_TOKEN")
    args = parser.parse_args()
    dimensions = args.dimension or ["URL"]
    if args.input:
        export = load_saved_export(Path(args.input), args.days, dimensions)
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
