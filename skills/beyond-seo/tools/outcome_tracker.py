#!/usr/bin/env python3
"""Summarize implementation outcomes without converting correlation to causation."""
from __future__ import annotations

import argparse
import csv
import json
import math
from datetime import date
from pathlib import Path

from first_party_quality import comparison_compatibility


def assess_outcome(row: dict) -> dict:
    result = dict(row)
    result.update({"implementation_status": "Not verified", "measurement_status": "Not comparable",
                   "absolute_change": None, "percent_change": None, "causal_claim": "Not established"})
    if row.get("validation_result") == "passed" and row.get("validation_evidence"):
        result["implementation_status"] = "Fix verified"
    try:
        implemented = date.fromisoformat(row["implementation_date"])
        before = {"source": row["source"], "property": row["property"], "timezone": row["timezone"],
                  "dimensions": row["segment"], "filters": row["filters"],
                  "start_date": row["baseline_start"], "end_date": row["baseline_end"]}
        after = {**before, "start_date": row["followup_start"], "end_date": row["followup_end"]}
        reasons = comparison_compatibility(before, after)
        if date.fromisoformat(row["baseline_end"]) >= implemented or date.fromisoformat(row["followup_start"]) <= implemented:
            reasons.append("Baseline must precede implementation; follow-up must follow it")
        values = [float(row[key]) for key in ("baseline_value", "followup_value")]
        if any(not math.isfinite(v) or v < 0 for v in values):
            raise ValueError
        if not row.get("unit") or not row.get("measurement_evidence") or not row.get("confounders"):
            reasons.append("Missing units, measurement evidence or confounder review")
        if row.get("source_label") not in {"First-party verified", "Paid-tool verified", "Confirmed"}:
            reasons.append("Measurement provenance is not verified")
        result["comparability_notes"] = reasons
        if not reasons:
            result.update({"measurement_status": "Observed change", "absolute_change": values[1] - values[0],
                           "percent_change": 100 * (values[1] - values[0]) / values[0] if values[0] else None})
    except (KeyError, TypeError, ValueError):
        result["comparability_notes"] = ["Missing or invalid measurement dates/values"]
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    with Path(args.input).open(encoding="utf-8-sig", newline="") as handle:
        results = [assess_outcome(row) for row in csv.DictReader(handle)]
    Path(args.output).write_text(json.dumps(results, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"rows": len(results)}))


if __name__ == "__main__":
    main()
