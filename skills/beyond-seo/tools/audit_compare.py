#!/usr/bin/env python3
"""Compare two normalized Beyond SEO audits."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


SEVERITY_RANK = {
    "info": 0,
    "low": 1,
    "medium": 2,
    "high": 3,
    "critical": 4,
}


def severity_change(previous: object, current: object) -> str | None:
    old_rank = SEVERITY_RANK.get(str(previous or "").strip().lower())
    new_rank = SEVERITY_RANK.get(str(current or "").strip().lower())
    if old_rank is None or new_rank is None or old_rank == new_rank:
        return None
    return "Improved" if new_rank < old_rank else "Worsened"


def finding_key(row: dict) -> str:
    if row.get("id"):
        return str(row["id"])
    material = "|".join([
        str(row.get("finding") or row.get("issue") or row.get("title") or "").lower().strip(),
        ",".join(sorted(str(x) for x in row.get("urls", row.get("evidence", [])) if isinstance(row.get("urls", row.get("evidence", [])), list))),
    ])
    return hashlib.sha256(material.encode("utf-8")).hexdigest()[:16]


def compare(previous: dict, current: dict) -> dict:
    old = {finding_key(row): row for row in previous.get("findings", previous.get("issues", []))}
    new = {finding_key(row): row for row in current.get("findings", current.get("issues", []))}
    changes = []
    warnings = []
    old_context, new_context = previous.get("business_context", {}), current.get("business_context", {})
    incompatible = False
    for field in ("website_url", "country_code", "language_code", "device"):
        if field in old_context and field in new_context and old_context[field] != new_context[field]:
            incompatible = True
            warnings.append(f"Different comparison scope: {field}")
    if previous.get("schema_version") != current.get("schema_version"):
        warnings.append("Different audit schema versions; score and check definitions may differ.")
    pages = {page["url"]: page for page in current.get("pages", [])}

    def rechecked(row):
        urls = row.get("affected_urls", row.get("urls", row.get("evidence", [])))
        check = row.get("check_id")
        return bool(check and isinstance(urls, list) and urls and all(
            url in pages and check in pages[url].get("checks_performed", []) for url in urls if isinstance(url, str)
        ) and all(isinstance(url, str) for url in urls))

    for key in sorted(set(old) | set(new)):
        if incompatible:
            changes.append({"id": key, "status": "Not comparable", "previous": old.get(key), "current": new.get(key)})
            continue
        if key not in old:
            state = "Reopened" if new[key].get("previous_status") == "Resolved" else "New"
            changes.append({"id": key, "status": state, "current": new[key]})
        elif key not in new:
            state = "Resolved" if rechecked(old[key]) else "Not rechecked"
            changes.append({"id": key, "status": state, "previous": old[key], "note": "Resolution requires the same check on every previously affected URL."})
        else:
            old_severity = old[key].get("severity") or old[key].get("priority")
            new_severity = new[key].get("severity") or new[key].get("priority")
            old_evidence = json.dumps(old[key].get("evidence", ""), sort_keys=True)
            new_evidence = json.dumps(new[key].get("evidence", ""), sort_keys=True)
            state = severity_change(old_severity, new_severity)
            if state is None:
                state = "Changed" if new_severity != old_severity or new_evidence != old_evidence else "Unchanged"
            if state == "Improved" and old[key].get("check_id") and not rechecked(old[key]):
                state = "Not rechecked"
            changes.append({"id": key, "status": state, "previous": old[key], "current": new[key]})
    counts = {status: sum(1 for row in changes if row["status"] == status) for status in ("New", "Improved", "Worsened", "Changed", "Unchanged", "Resolved", "Reopened", "Not rechecked", "Not comparable")}
    return {"previous_date": previous.get("audit_date"), "current_date": current.get("audit_date"), "summary": counts, "changes": changes, "comparability_warnings": warnings}


def main() -> None:
    parser = argparse.ArgumentParser(description="Compare two Beyond SEO audit JSON files.")
    parser.add_argument("--previous", required=True)
    parser.add_argument("--current", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    result = compare(
        json.loads(Path(args.previous).read_text(encoding="utf-8")),
        json.loads(Path(args.current).read_text(encoding="utf-8")),
    )
    Path(args.output).write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(result["summary"]))


if __name__ == "__main__":
    main()
