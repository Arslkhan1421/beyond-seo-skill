#!/usr/bin/env python3
"""Validate package metadata, shared labels and routed local references."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


def validate(root: Path) -> list[str]:
    errors = []
    schema = json.loads((root / "core/evidence-schema.json").read_text(encoding="utf-8"))
    entrypoint = (root / "SKILL.md").read_text(encoding="utf-8")
    evidence_section = entrypoint.split("## Evidence labels", 1)[1].split("## Start sequence", 1)[0]
    labels = set(re.findall(r"^- `([^`]+)`:.*$", evidence_section, re.M))
    if labels != set(schema["labels"]):
        errors.append("SKILL.md evidence labels differ from the shared schema.")
    versions = {schema["schema_version"]}
    for name in ("skill.json", "_meta.json", "MANIFEST.json"):
        try:
            versions.add(json.loads((root / name).read_text(encoding="utf-8"))["version"])
        except (OSError, ValueError, KeyError):
            errors.append(f"Invalid metadata: {name}")
    found = re.search(r"^  version: (.+)$", entrypoint, re.M)
    versions.add(found.group(1) if found else "missing")
    if len(versions) != 1:
        errors.append(f"Package versions disagree: {sorted(versions)}")
    for path in root.rglob("*.md"):
        content = path.read_text(encoding="utf-8")
        if re.search(r"^(?:#{1,6} )?(?:Likely|Estimated|Not Verified)\s*$|^(?:Likely|Estimated|Observed|Verified|Sampled):", content, re.M):
            errors.append(f"Noncanonical evidence label in {path.relative_to(root)}")
        for reference in re.findall(r"`((?:core|audit|tools|reporting|integrations|templates|keyword-research|aeo-geo|local-seo|backlink-system|strategy|social-media)/[^`\s]+\.(?:md|py|json|csv))`", content):
            if not (root / reference).is_file():
                errors.append(f"Missing reference in {path.relative_to(root)}: {reference}")
    manifest = json.loads((root / "MANIFEST.json").read_text(encoding="utf-8"))
    actual = {p.relative_to(root).as_posix() for p in root.rglob("*") if p.is_file() and "__pycache__" not in p.parts and p.suffix != ".pyc"}
    if set(manifest["files"]) != actual or manifest.get("actual_files_count") != len(actual):
        errors.append("Manifest inventory is stale.")
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", nargs="?", default=str(Path(__file__).resolve().parents[1]))
    args = parser.parse_args()
    errors = validate(Path(args.path))
    print(json.dumps({"passed": not errors, "errors": errors}, indent=2))
    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
