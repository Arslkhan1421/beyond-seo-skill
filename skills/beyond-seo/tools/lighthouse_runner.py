#!/usr/bin/env python3
"""Collect PageSpeed data with a local Lighthouse fallback."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
from pathlib import Path

import requests


PSI_URL = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"


def summarize_lighthouse(payload: dict, source: str, strategy: str) -> dict:
    categories = payload.get("lighthouseResult", payload).get("categories", {})
    audits = payload.get("lighthouseResult", payload).get("audits", {})
    score = lambda name: round((categories.get(name, {}).get("score") or 0) * 100) if categories.get(name, {}).get("score") is not None else None
    numeric = lambda name: audits.get(name, {}).get("numericValue")
    return {
        "status": "verified",
        "source": source,
        "strategy": strategy,
        "scores": {name: score(name) for name in ("performance", "seo", "accessibility", "best-practices")},
        "metrics": {
            "lcp_ms": numeric("largest-contentful-paint"),
            "cls": numeric("cumulative-layout-shift"),
            "tbt_ms": numeric("total-blocking-time"),
            "fcp_ms": numeric("first-contentful-paint"),
        },
        "evidence_label": "Confirmed",
    }


def run_pagespeed(url: str, strategy: str, api_key: str | None = None, timeout: int = 75) -> tuple[dict | None, str]:
    params: list[tuple[str, str]] = [("url", url), ("strategy", strategy)]
    params.extend(("category", item) for item in ("performance", "seo", "accessibility", "best-practices"))
    if api_key:
        params.append(("key", api_key))
    try:
        response = requests.get(PSI_URL, params=params, timeout=timeout)
        if response.status_code == 200:
            return summarize_lighthouse(response.json(), "PageSpeed Insights", strategy), ""
        if response.status_code == 429:
            return None, "PageSpeed request limit reached; a local Lighthouse fallback was attempted."
        return None, f"PageSpeed did not return a usable result ({response.status_code}); a local fallback was attempted."
    except requests.RequestException:
        return None, "PageSpeed was unavailable; a local Lighthouse fallback was attempted."


def find_lighthouse() -> list[str] | None:
    direct = shutil.which("lighthouse")
    if direct:
        return [direct]
    npx = shutil.which("npx")
    if npx:
        return [npx, "--no-install", "lighthouse"]
    return None


def run_local(url: str, strategy: str, output_dir: Path, timeout: int = 150) -> dict | None:
    command = find_lighthouse()
    if not command:
        return None
    output_dir.mkdir(parents=True, exist_ok=True)
    output = output_dir / f"lighthouse-{strategy}.json"
    form_factor = "mobile" if strategy == "mobile" else "desktop"
    args = command + [url, "--quiet", "--output=json", f"--output-path={output}", "--chrome-flags=--headless --no-sandbox", f"--form-factor={form_factor}"]
    try:
        subprocess.run(args, check=True, capture_output=True, text=True, timeout=timeout)
        return summarize_lighthouse(json.loads(output.read_text(encoding="utf-8")), "Local Lighthouse", strategy)
    except (subprocess.SubprocessError, OSError, json.JSONDecodeError):
        return None


def collect(url: str, strategy: str, output_dir: Path, api_key: str | None = None) -> dict:
    result, note = run_pagespeed(url, strategy, api_key)
    if result:
        return result
    local = run_local(url, strategy, output_dir)
    if local:
        local["note"] = note
        return local
    return {
        "status": "not_verified",
        "source": "PageSpeed / Lighthouse",
        "strategy": strategy,
        "scores": {},
        "metrics": {},
        "evidence_label": "Not verified",
        "note": note + " Local Lighthouse was not installed or did not complete.",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Run PageSpeed with local Lighthouse fallback.")
    parser.add_argument("--url", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--strategy", choices=("mobile", "desktop", "both"), default="both")
    args = parser.parse_args()
    strategies = ("mobile", "desktop") if args.strategy == "both" else (args.strategy,)
    output = Path(args.output)
    results = [collect(args.url, strategy, output.parent, os.getenv("PAGESPEED_API_KEY")) for strategy in strategies]
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(json.dumps({"output": str(output.resolve()), "results": len(results)}))


if __name__ == "__main__":
    main()
