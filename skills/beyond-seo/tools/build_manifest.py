#!/usr/bin/env python3
"""Refresh Beyond SEO manifest file inventory and release metadata."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "MANIFEST.json"


def package_file(path: Path) -> bool:
    return (path.is_file() and "__pycache__" not in path.parts and path.suffix != ".pyc"
            and path.name != ".env" and not path.name.startswith(".env.") and path.suffix != ".env")


def main() -> None:
    payload = json.loads(MANIFEST.read_text(encoding="utf-8")) if MANIFEST.exists() else {}
    files = sorted(
        path.relative_to(ROOT).as_posix()
        for path in ROOT.rglob("*")
        if package_file(path) and path.name != "MANIFEST.json"
    )
    payload.update({
        "package": "Beyond SEO",
        "version": json.loads((ROOT / "core/evidence-schema.json").read_text(encoding="utf-8"))["schema_version"],
        "release": "traceable findings, sample scoring and coverage, first-party quality, reproducibility and outcome tracking",
        "root_folder": "beyond-seo",
        "actual_files_count": len(files) + 1,
        "ai_friendly_seo": True,
        "apify_first": True,
        "microsoft_clarity": True,
        "files": ["MANIFEST.json", *files],
    })
    MANIFEST.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"manifest": str(MANIFEST), "files": len(files) + 1}))


if __name__ == "__main__":
    main()
