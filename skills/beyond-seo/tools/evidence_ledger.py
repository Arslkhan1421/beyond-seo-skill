#!/usr/bin/env python3
"""Create and validate a machine-readable SEO evidence ledger."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ALLOWED_LABELS = {
    "Confirmed",
    "First-party verified",
    "Paid-tool verified",
    "Screenshot verified",
    "Technical crawl verified",
    "Live SERP sample",
    "Live search sample",
    "Inferred",
    "Directional",
    "Not verified",
}
RESTRICTED_METRICS = {
    "keyword_volume", "keyword_difficulty", "traffic", "dr", "da",
    "authority_score", "backlinks", "referring_domains", "conversions",
    "ai_visibility",
}
VERIFIED_LABELS = {
    "Confirmed", "First-party verified", "Paid-tool verified",
    "Screenshot verified", "Technical crawl verified",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def stable_id(record: dict[str, Any]) -> str:
    material = "|".join(str(record.get(key, "")) for key in (
        "source_name", "source_url", "scope", "metric", "value"
    ))
    return hashlib.sha256(material.encode("utf-8")).hexdigest()[:16]


def normalize_record(record: dict[str, Any]) -> dict[str, Any]:
    output = {
        "id": record.get("id") or stable_id(record),
        "collected_at": record.get("collected_at") or utc_now(),
        "source_type": record.get("source_type", "unknown"),
        "source_name": record.get("source_name", "Unknown source"),
        "source_url": record.get("source_url", ""),
        "actor_id": record.get("actor_id", ""),
        "method": record.get("method", ""),
        "scope": record.get("scope", ""),
        "metric": record.get("metric", ""),
        "value": record.get("value"),
        "label": record.get("label", "Not verified"),
        "artifact_path": record.get("artifact_path", ""),
        "notes": record.get("notes", ""),
    }
    if output["label"] not in ALLOWED_LABELS:
        raise ValueError(f"Unsupported evidence label: {output['label']}")
    metric = str(output["metric"]).strip().lower().replace(" ", "_")
    if metric in RESTRICTED_METRICS and output["value"] not in (None, "", "Not verified"):
        if output["label"] not in VERIFIED_LABELS:
            raise ValueError(
                f"Metric '{metric}' requires verified evidence; received {output['label']}."
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
