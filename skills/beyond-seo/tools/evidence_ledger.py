#!/usr/bin/env python3
"""Create and validate a machine-readable SEO evidence ledger."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


EVIDENCE_SCHEMA = json.loads((Path(__file__).resolve().parents[1] / "core" / "evidence-schema.json").read_text(encoding="utf-8"))
ALLOWED_LABELS = set(EVIDENCE_SCHEMA["labels"])
RESTRICTED_METRICS = {
    "keyword_volume", "keyword_difficulty", "traffic", "dr", "da",
    "authority_score", "backlinks", "referring_domains", "conversions",
    "ai_visibility",
}
VERIFIED_LABELS = {
    "Confirmed", "First-party verified", "Paid-tool verified",
    "Screenshot verified", "Technical crawl verified",
}
ALLOWED_PROVENANCE = {label: set(values) for label, values in EVIDENCE_SCHEMA["labels"].items() if values}
METRIC_LABELS = {
    "keyword_volume": {"Paid-tool verified"},
    "keyword_difficulty": {"Paid-tool verified"},
    "dr": {"Paid-tool verified"},
    "da": {"Paid-tool verified"},
    "authority_score": {"Paid-tool verified"},
    "backlinks": {"Paid-tool verified"},
    "referring_domains": {"Paid-tool verified"},
    "traffic": {"First-party verified", "Paid-tool verified"},
    "conversions": {"First-party verified"},
    "ai_visibility": {"First-party verified", "Paid-tool verified"},
}
METRIC_ALIASES = {
    "volume": "keyword_volume",
    "search_volume": "keyword_volume",
    "keywordvolume": "keyword_volume",
    "difficulty": "keyword_difficulty",
    "kd": "keyword_difficulty",
    "domain_rating": "dr",
    "domain_authority": "da",
    "linking_domains": "referring_domains",
    "inbound_links": "backlinks",
    "key_events": "conversions",
    "goals": "conversions",
}
METRIC_SOURCE_TYPES = {
    "keyword_volume": {"paid_tool", "seo_tool", "rank_tracker"},
    "keyword_difficulty": {"paid_tool", "seo_tool", "rank_tracker"},
    "dr": {"paid_tool", "seo_tool", "backlink_tool"},
    "da": {"paid_tool", "seo_tool", "backlink_tool"},
    "authority_score": {"paid_tool", "seo_tool", "backlink_tool"},
    "backlinks": {"paid_tool", "seo_tool", "backlink_tool"},
    "referring_domains": {"paid_tool", "seo_tool", "backlink_tool"},
    "traffic": {
        "first_party", "first_party_analytics", "analytics", "search_console",
        "paid_tool", "seo_tool",
    },
    "conversions": {
        "first_party", "first_party_analytics", "analytics", "crm",
        "behavior_analytics",
    },
    "ai_visibility": {"first_party", "search_console", "paid_tool", "seo_tool"},
}


def canonical_metric(value: Any) -> str:
    metric = re.sub(r"[^a-z0-9]+", "_", str(value).strip().lower()).strip("_")
    metric = METRIC_ALIASES.get(metric, metric)
    tokens = set(metric.split("_"))
    if "volume" in tokens and ({"keyword", "search"} & tokens):
        return "keyword_volume"
    if "difficulty" in tokens and "keyword" in tokens:
        return "keyword_difficulty"
    if "da" in tokens or {"domain", "authority"}.issubset(tokens):
        return "da"
    if "dr" in tokens or {"domain", "rating"}.issubset(tokens):
        return "dr"
    if {"authority", "score"}.issubset(tokens):
        return "authority_score"
    if {"ai", "visibility"}.issubset(tokens):
        return "ai_visibility"
    if "traffic" in tokens:
        return "traffic"
    if "conversion" in tokens or "conversions" in tokens:
        return "conversions"
    if "backlink" in tokens or "backlinks" in tokens:
        return "backlinks"
    if "referring" in tokens and ({"domain", "domains"} & tokens):
        return "referring_domains"
    return metric


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def stable_id(record: dict[str, Any]) -> str:
    material = json.dumps([record.get(key, "") for key in (
        "source_name", "source_url", "provenance", "scope", "metric", "value", "collected_at"
    )], sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(material.encode("utf-8")).hexdigest()[:16]


def normalize_record(record: dict[str, Any]) -> dict[str, Any]:
    record = {**record, "collected_at": record.get("collected_at") or utc_now()}
    output = {
        "id": record.get("id") or stable_id(record),
        "collected_at": record.get("collected_at") or utc_now(),
        "source_type": record.get("source_type", "unknown"),
        "source_name": record.get("source_name", "Unknown source"),
        "source_url": record.get("source_url", ""),
        "actor_id": record.get("actor_id", ""),
        "method": record.get("method", ""),
        "provenance": record.get("provenance", "unknown"),
        "scope": record.get("scope", ""),
        "metric": record.get("metric", ""),
        "value": record.get("value"),
        "label": record.get("label", "Not verified"),
        "artifact_path": record.get("artifact_path", ""),
        "artifact_locator": record.get("artifact_locator", ""),
        "measurement_start": record.get("measurement_start", ""),
        "measurement_end": record.get("measurement_end", ""),
        "country": record.get("country", ""),
        "language": record.get("language", ""),
        "device": record.get("device", ""),
        "sample_depth": record.get("sample_depth"),
        "notes": record.get("notes", ""),
    }
    if output["label"] not in ALLOWED_LABELS:
        raise ValueError(f"Unsupported evidence label: {output['label']}")
    required_provenance = ALLOWED_PROVENANCE.get(output["label"])
    if required_provenance and output["provenance"] not in required_provenance:
        raise ValueError(
            f"Evidence label '{output['label']}' requires provenance in "
            f"{sorted(required_provenance)}; received {output['provenance']!r}."
        )
    metric = canonical_metric(output["metric"])
    if metric in RESTRICTED_METRICS and output["value"] not in (None, "", "Not verified"):
        try:
            number = float(output["value"])
            if not math.isfinite(number) or number < 0 or isinstance(output["value"], bool):
                raise ValueError
        except (TypeError, ValueError) as exc:
            raise ValueError(f"Metric '{metric}' requires a finite nonnegative numeric value.") from exc
        supported_labels = METRIC_LABELS.get(metric, VERIFIED_LABELS)
        if output["label"] not in supported_labels:
            raise ValueError(
                f"Metric '{metric}' requires one of {sorted(supported_labels)}; received {output['label']}."
            )
        source_type = re.sub(
            r"[^a-z0-9]+", "_", str(output["source_type"]).strip().lower()
        ).strip("_")
        supported_source_types = METRIC_SOURCE_TYPES.get(metric, set())
        if source_type not in supported_source_types:
            raise ValueError(
                f"Metric '{metric}' with label '{output['label']}' requires source_type in "
                f"{sorted(supported_source_types)}; received {source_type!r}."
            )
    return output


class EvidenceLedger:
    def __init__(self, records: list[dict[str, Any]] | None = None):
        self.records = [normalize_record(record) for record in (records or [])]

    def add(self, **record: Any) -> dict[str, Any]:
        normalized = normalize_record(record)
        self.records.append(normalized)
        return normalized

    def write(self, json_path: Path, csv_path: Path | None = None) -> None:
        json_path.parent.mkdir(parents=True, exist_ok=True)
        json_path.write_text(json.dumps(self.records, indent=2, ensure_ascii=False), encoding="utf-8")
        if csv_path:
            csv_path.parent.mkdir(parents=True, exist_ok=True)
            fields = list(normalize_record({}).keys())
            with csv_path.open("w", encoding="utf-8", newline="") as handle:
                writer = csv.DictWriter(handle, fieldnames=fields)
                writer.writeheader()
                writer.writerows(self.records)


def main() -> None:
    parser = argparse.ArgumentParser(description="Normalize an SEO evidence ledger.")
    parser.add_argument("--input", required=True, help="JSON array of evidence records.")
    parser.add_argument("--output", required=True, help="Output JSON path.")
    parser.add_argument("--csv", help="Optional CSV output path.")
    args = parser.parse_args()
    records = json.loads(Path(args.input).read_text(encoding="utf-8"))
    ledger = EvidenceLedger(records)
    ledger.write(Path(args.output), Path(args.csv) if args.csv else None)
    print(json.dumps({"records": len(ledger.records), "output": str(Path(args.output).resolve())}))


if __name__ == "__main__":
    main()
