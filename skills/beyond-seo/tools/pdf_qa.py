#!/usr/bin/env python3
"""Detect blank pages and broken score-bar text in Beyond SEO PDFs."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from pypdf import PdfReader


BROKEN_MARKERS = ("HTTP 429", "########", "????????", "\ufffd")


def inspect_pdf(path: Path, output: Path | None = None) -> dict:
    reader = PdfReader(str(path))
    page_text = [(page.extract_text() or "").strip() for page in reader.pages]
    blank_pages = [index for index, text in enumerate(page_text, 1) if len(text) < 20]
    full_text = "\n".join(page_text)
    marker_counts = {marker.encode("unicode_escape").decode("ascii"): full_text.count(marker) for marker in BROKEN_MARKERS}
    result = {
        "file": str(path.resolve()), "pages": len(reader.pages),
        "blank_pages": blank_pages, "broken_markers": marker_counts,
        "passed": bool(reader.pages) and not blank_pages and not any(marker_counts.values()),
    }
    if output:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(result, indent=2), encoding="utf-8")
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="Inspect a Beyond SEO PDF.")
    parser.add_argument("--input", required=True)
    parser.add_argument("--output")
    args = parser.parse_args()
    result = inspect_pdf(Path(args.input), Path(args.output) if args.output else None)
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if result["passed"] else 1)


if __name__ == "__main__":
    main()
