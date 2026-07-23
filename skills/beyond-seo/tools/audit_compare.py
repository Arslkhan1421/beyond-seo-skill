#!/usr/bin/env python3
"""Compare two normalized Beyond SEO audits."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


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
    for key in sorted(set(old) | set(new)):
        if key not in old:
            state = "Reopened" if new[key].get("previous_status") == "Resolved" else "New"
            changes.append({"id": key, "status": state, "current": new[key]})
        elif key not in new:
            changes.append({"id": key, "status": "Resolved", "previous": old[key]})
        else:
            old_severity = old[key].get("severity") or old[key].get("priority")
            new_severity = new[key].get("severity") or new[key].get("priority")
            old_evidence = json.dumps(old[key].get("evidence", ""), sort_keys=True)
            new_evidence = json.dumps(new[key].get("evidence", ""), sort_keys=True)
            state = "Improved" if new_severity != old_severity else "Changed" if new_evidence != old_evidence else "Unchanged"
            changes.append({"id": key, "status": state, "previous": old[key], "current": new[key]})
    counts = {status: sum(1 for row in changes if row["status"] == status) for status in ("New", "Improved", "Changed", "Unchanged", "Resolved", "Reopened")}
    return {"previous_date": previous.get("audit_date"), "current_date": current.get("audit_date"), "summary": counts, "changes": changes}


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
