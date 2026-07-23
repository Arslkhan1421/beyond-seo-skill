#!/usr/bin/env python3
"""Run a reusable, evidence-led Beyond SEO crawl and SERP baseline."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import time
from collections import Counter, deque
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urldefrag, urljoin, urlparse

import requests
from bs4 import BeautifulSoup

from audit_compare import compare
from clarity_export import collect as collect_clarity
from clarity_export import normalize_export as normalize_clarity_export
from competitor_classifier import classify
from evidence_ledger import EvidenceLedger
from lighthouse_runner import collect as collect_performance
from report_builder import build_pdf


HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}


def clean(value: str) -> str:
    return re.sub(r"\s+", " ", value or "").strip()


def normalize_url(url: str, host: str) -> str | None:
    url = urldefrag(url)[0]
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"} or parsed.netloc.lower().removeprefix("www.") != host:
        return None
    path = parsed.path or "/"
    if path != "/":
        path = path.rstrip("/")
    return f"https://{host}{path}" + (f"?{parsed.query}" if parsed.query else "")


def fetch(url: str, timeout: int = 25) -> dict:
    try:
        response = requests.get(url, headers=HEADERS, timeout=timeout, allow_redirects=True)
        return {"url": url, "status": response.status_code, "final_url": response.url, "headers": dict(response.headers), "text": response.text}
    except requests.RequestException as exc:
        return {"url": url, "status": None, "final_url": "", "headers": {}, "text": "", "error": str(exc)}


def parse_page(result: dict, host: str) -> dict:
    soup = BeautifulSoup(result.get("text", ""), "html.parser")
    title = clean(soup.title.get_text(" ")) if soup.title else ""
    meta_tag = soup.find("meta", attrs={"name": re.compile("^description$", re.I)})
    canonical_tag = soup.find("link", attrs={"rel": lambda value: value and "canonical" in value})
    robots_tag = soup.find("meta", attrs={"name": re.compile("^robots$", re.I)})
    body = clean(soup.get_text(" "))
    links = []
    for anchor in soup.find_all("a", href=True):
        normalized = normalize_url(urljoin(result.get("final_url") or result["url"], anchor["href"]), host)
        if normalized:
            links.append(normalized)
    schema = []
    for script in soup.find_all("script", attrs={"type": re.compile("ld\\+json", re.I)}):
        schema.extend(re.findall(r'"@type"\s*:\s*"([^"]+)"', script.string or script.get_text() or ""))
    visible_hash = hashlib.sha256(body.lower().encode("utf-8")).hexdigest() if body else ""
    return {
        "url": result["url"], "status": result.get("status"), "final_url": result.get("final_url"),
        "title": title, "meta_description": clean(meta_tag.get("content", "")) if meta_tag else "",
        "canonical": canonical_tag.get("href", "") if canonical_tag else "",
        "robots": clean(robots_tag.get("content", "")) if robots_tag else "",
        "h1": [clean(tag.get_text(" ")) for tag in soup.find_all("h1") if clean(tag.get_text(" "))],
        "h2": [clean(tag.get_text(" ")) for tag in soup.find_all("h2") if clean(tag.get_text(" "))][:15],
        "word_count": len(re.findall(r"\b[\w'-]{2,}\b", body)),
        "schema_types": sorted(set(schema)), "internal_links": sorted(set(links)),
        "visible_text_hash": visible_hash, "noindex": "noindex" in clean(robots_tag.get("content", "")).lower() if robots_tag else False,
    }


def parse_sitemap(text: str) -> list[str]:
    return [clean(item) for item in re.findall(r"<loc>\s*([^<]+)\s*</loc>", text or "", flags=re.I)]


def collect_sitemap_urls(sitemap_url: str, host: str, max_sitemaps: int = 25) -> tuple[int | None, list[str]]:
    queue = deque([sitemap_url])
    seen_sitemaps: set[str] = set()
    page_urls: set[str] = set()
    root_status = None
    while queue and len(seen_sitemaps) < max_sitemaps:
        current = queue.popleft()
        if current in seen_sitemaps:
            continue
        seen_sitemaps.add(current)
        result = fetch(current)
        if root_status is None:
            root_status = result.get("status")
        for location in parse_sitemap(result.get("text", "")):
            if urlparse(location).path.lower().endswith(".xml"):
                queue.append(location)
                continue
            normalized = normalize_url(location, host)
            if normalized:
                page_urls.add(normalized)
    return root_status, sorted(page_urls)


def crawl(config: dict) -> tuple[list[dict], dict, dict]:
    start = config["website_url"].rstrip("/") + "/"
    host = urlparse(start).netloc.lower().removeprefix("www.")
    robots = fetch(urljoin(start, "/robots.txt"))
    sitemap_url = config.get("sitemap_url") or urljoin(start, "/sitemap.xml")
    sitemap_status, sitemap_urls = collect_sitemap_urls(sitemap_url, host)
    seeds = [start, *sitemap_urls, *config.get("seed_urls", [])]
    queue = deque(filter(None, (normalize_url(urljoin(start, url), host) for url in seeds)))
    seen, pages = set(), []
    max_pages = min(int(config.get("max_crawl_pages", 100)), 500)
    while queue and len(pages) < max_pages:
        url = queue.popleft()
        if url in seen:
            continue
        seen.add(url)
        page = parse_page(fetch(url), host)
        page["in_sitemap"] = url in set(filter(None, sitemap_urls))
        pages.append(page)
        if page.get("status") == 200:
            queue.extend(link for link in page["internal_links"] if link not in seen)
        time.sleep(float(config.get("crawl_delay_seconds", 0.1)))
    return pages, {"status": robots.get("status"), "url": robots.get("final_url")}, {"status": sitemap_status, "url": sitemap_url, "urls": sitemap_urls}


def run_apify_serp(config: dict, output_dir: Path) -> list[dict]:
    token = os.getenv("APIFY_API_TOKEN")
    queries = config.get("queries", [])[: int(config.get("max_serp_queries", 20))]
    if not token or not queries or not config.get("apify", {}).get("enabled", True):
        return []
    payload = {
        "queries": "\n".join(queries), "resultsPerPage": min(int(config.get("serp_results_per_query", 10)), 10),
        "maxPagesPerQuery": 1, "countryCode": config.get("country_code", "us"),
        "languageCode": config.get("language_code", "en"), "mobileResults": config.get("device", "desktop") == "mobile",
        "saveHtml": False, "includeUnfilteredResults": False,
    }
    endpoint = "https://api.apify.com/v2/acts/apify~google-search-scraper/run-sync-get-dataset-items"
    response = requests.post(endpoint, params={"token": token, "timeout": 300}, json=payload, timeout=330)
    response.raise_for_status()
    rows = response.json()
    (output_dir / "apify-serp-raw.json").write_text(json.dumps(rows, indent=2, ensure_ascii=False), encoding="utf-8")
    return rows


def normalize_serps(items: list[dict], target_host: str) -> tuple[list[dict], list[dict]]:
    baseline, candidates = [], []
    for item in items:
        query = (item.get("searchQuery") or {}).get("term") or item.get("query") or ""
        organic = item.get("organicResults") or []
        own = []
        for position, result in enumerate(organic[:10], 1):
            domain = urlparse(result.get("url", "")).netloc.lower().removeprefix("www.")
            if domain == target_host:
                own.append((position, result.get("url")))
            elif domain:
                candidates.append({"domain": domain, "ranking_url": result.get("url", ""), "title": result.get("title", ""), "description": result.get("description", ""), "ranking_keyword": query, "observed_position": position})
        baseline.append({"keyword": query, "observed_position": min((row[0] for row in own), default=None), "observed_url": own[0][1] if own else None, "source": "Apify Google Search Scraper", "evidence_label": "Live SERP sample"})
    counts = Counter(row["domain"] for row in candidates)
    for row in candidates:
        row["serp_appearances"] = counts[row["domain"]]
    unique = {row["domain"]: row for row in candidates}
    return baseline, list(unique.values())


def build_findings(pages: list[dict], sitemap: dict, target_host: str) -> list[dict]:
    findings = []
    live = [page for page in pages if page.get("status") == 200 and not page.get("noindex")]
    missing_h1 = [page["url"] for page in live if not page.get("h1")]
    thin = [page["url"] for page in live if page.get("word_count", 0) < 400]
    missing_canonical = [page["url"] for page in live if not page.get("canonical")]
    duplicate_groups: dict[str, list[str]] = {}
    for page in live:
        duplicate_groups.setdefault(page.get("visible_text_hash", ""), []).append(page["url"])
    duplicates = [urls for digest, urls in duplicate_groups.items() if digest and len(urls) > 1]
    specs = [
        ("missing-h1", "Pages missing an H1", missing_h1, "High", "Add a unique, intent-aligned H1."),
        ("thin-pages", "Pages under 400 words", thin, "Medium", "Review by page type; expand commercial/proof pages with useful evidence."),
        ("missing-canonical", "Indexable pages missing a canonical", missing_canonical, "High", "Add a self-referencing canonical to preferred URLs."),
        ("duplicate-content", "Exact visible-content duplicates", duplicates, "High", "Choose one preferred route and consolidate duplicates with one-hop redirects."),
    ]
    for identifier, title, evidence, severity, fix in specs:
        if evidence:
            findings.append({"id": identifier, "finding": title, "evidence": evidence, "severity": severity, "fix": fix, "evidence_label": "Confirmed"})
    sitemap_set = set(sitemap.get("urls", []))
    missing = [page["url"] for page in live if page["url"] not in sitemap_set]
    if missing:
        findings.append({"id": "sitemap-coverage", "finding": "Indexable crawled pages missing from sitemap", "evidence": missing, "severity": "Medium", "fix": "Include preferred indexable URLs or document intentional exclusions.", "evidence_label": "Confirmed"})
    return findings


def collect_clarity_evidence(config: dict, output_dir: Path) -> dict | None:
    settings = config.get("clarity") or {}
    if not settings.get("enabled", False):
        return None
    num_days = int(settings.get("num_days", 3))
    dimensions = settings.get("dimensions") or ["URL"]
    export_path = settings.get("export_path") or os.getenv("CLARITY_EXPORT_PATH")
    try:
        if export_path:
            raw = json.loads(Path(export_path).read_text(encoding="utf-8"))
            if isinstance(raw, dict) and raw.get("source") == "Microsoft Clarity Data Export API" and raw.get("report_section"):
                export = raw
            else:
                export = normalize_clarity_export(raw, num_days, dimensions)
        else:
            token = os.getenv(settings.get("token_env", "CLARITY_API_TOKEN"))
            if not token:
                return None
            export = collect_clarity(token, num_days, dimensions)
        (output_dir / "clarity-live-insights.json").write_text(
            json.dumps(export, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        return export
    except (OSError, ValueError, RuntimeError, requests.RequestException, json.JSONDecodeError) as exc:
        return {
            "source": "Microsoft Clarity",
            "evidence_label": "Not verified",
            "reason": str(exc),
        }


def report_payload(config: dict, audit: dict) -> dict:
    pages, findings = audit["pages"], audit["findings"]
    live = [page for page in pages if page.get("status") == 200]
    technical_score = max(0, 100 - 8 * len(findings))
    clarity = audit.get("clarity") or {}
    clarity_verified = clarity.get("evidence_label") == "First-party verified"
    data_gaps = [
        row for row in config.get("data_gaps", [])
        if not (clarity_verified and "clarity" in str(row.get("source", "")).lower())
    ]
    if not clarity_verified and not any("clarity" in str(row.get("source", "")).lower() for row in data_gaps):
        data_gaps.append({
            "source": "Microsoft Clarity",
            "needed": "CLARITY_API_TOKEN or a dated 1–3 day Data Export API JSON/CSV export",
        })
    sources = [{"label": "Website", "url": config["website_url"]}]
    if clarity_verified:
        sources.append({
            "label": "Microsoft Clarity Data Export API",
            "url": clarity.get("source_url", "https://learn.microsoft.com/en-us/clarity/setup-and-installation/clarity-data-export-api"),
        })
    payload = {
        "title": "Beyond SEO Full-Depth Audit", "client": config.get("client_name") or urlparse(config["website_url"]).netloc,
        "site_url": config["website_url"], "audit_date": audit["audit_date"][:10], "audit_mode": audit["audit_mode"],
        "overall_score": technical_score, "status": "Observed readiness; unverified categories excluded",
        "summary": f"Reviewed {len(pages)} URLs, {len(live)} successful pages, {len(audit['rank_baseline'])} live SERP samples, and {len(findings)} prioritized findings.",
        "data_confidence": audit["data_confidence"],
        "scores": [{"area": "Observed technical/on-page readiness", "score": technical_score, "display": f"{technical_score} / 100", "note": "Based only on collected crawl and SERP evidence."}],
        "findings": [{"issue": row["finding"], "evidence": json.dumps(row["evidence"], ensure_ascii=False), "priority": row["severity"], "fix": row["fix"]} for row in findings],
        "keywords": [{"keyword": row["keyword"], "intent": "Requires mapping", "source": row["source"], "volume": "Not verified", "difficulty": "Not verified", "action": "Review target page", "confidence": row["evidence_label"]} for row in audit["rank_baseline"]],
        "competitors": [{"competitor": row["domain"], "evidence": f"Position {row.get('observed_position')} for {row.get('ranking_keyword')}", "gap": row.get("classification"), "action": "Crawl and compare the ranking page."} for row in audit["competitors"].get("comparable", [])[:10]],
        "roadmap": config.get("roadmap", []), "data_gaps": data_gaps,
        "sources": sources,
    }
    if clarity_verified:
        payload["clarity"] = clarity.get("report_section", {})
    return payload


def run(config: dict, output_dir: Path, previous: Path | None = None, build_report: bool = True) -> dict:
    output_dir.mkdir(parents=True, exist_ok=True)
    pages, robots, sitemap = crawl(config)
    target_host = urlparse(config["website_url"]).netloc.lower().removeprefix("www.")
    serp_items = run_apify_serp(config, output_dir)
    baseline, candidates = normalize_serps(serp_items, target_host)
    competitors = classify(candidates, config)
    findings = build_findings(pages, sitemap, target_host)
    performance = [collect_performance(config["website_url"], strategy, output_dir, os.getenv("PAGESPEED_API_KEY")) for strategy in ("mobile", "desktop")] if config.get("performance", {}).get("enabled", True) else []
    clarity = collect_clarity_evidence(config, output_dir)
    ledger = EvidenceLedger()
    ledger.add(source_type="crawl", source_name="Native crawl", source_url=config["website_url"], method="requests + HTML parser", scope=f"{len(pages)} URLs", label="Confirmed", artifact_path=str(output_dir / "audit-data.json"))
    if baseline:
        ledger.add(source_type="serp", source_name="Apify Google Search Scraper", actor_id="apify/google-search-scraper", method="top-10 one-time sample", scope=f"{len(baseline)} queries", label="Live SERP sample", artifact_path=str(output_dir / "apify-serp-raw.json"))
    if clarity and clarity.get("evidence_label") == "First-party verified":
        ledger.add(
            source_type="behavior analytics",
            source_name="Microsoft Clarity Data Export API",
            source_url=clarity.get("source_url", ""),
            method="authenticated project export",
            scope=f"Previous {clarity.get('num_days')} day(s); dimensions: {', '.join(clarity.get('dimensions') or []) or 'none'}",
            label="First-party verified",
            artifact_path=str(output_dir / "clarity-live-insights.json"),
        )
    clarity_verified = clarity and clarity.get("evidence_label") == "First-party verified"
    audit_mode = "Apify + native crawl" if baseline else "Native crawl"
    if clarity_verified:
        audit_mode += " + Microsoft Clarity"
    data_confidence = [
        {"label": "Confirmed", "value": f"Native crawl: {len(pages)} URLs"},
        {"label": "Live SERP sample", "value": f"{len(baseline)} one-time queries"},
        {
            "label": "First-party verified" if clarity_verified else "Not verified",
            "value": (
                f"Microsoft Clarity: previous {clarity.get('num_days')} day(s)"
                if clarity_verified
                else "Microsoft Clarity: connect CLARITY_API_TOKEN or provide a dated export"
            ),
        },
        {"label": "Not verified", "value": "GSC, GA4, backlinks, proprietary volume/KD unless separately imported"},
    ]
    audit = {
        "schema_version": "1.3.0", "audit_date": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "audit_mode": audit_mode,
        "business_context": config, "robots": robots, "sitemap": sitemap, "pages": pages,
        "findings": findings, "rank_baseline": baseline, "competitors": competitors,
        "performance": performance, "clarity": clarity,
        "data_confidence": data_confidence,
    }
    audit_path = output_dir / "audit-data.json"
    audit_path.write_text(json.dumps(audit, indent=2, ensure_ascii=False), encoding="utf-8")
    ledger.write(output_dir / "evidence-ledger.json", output_dir / "evidence-ledger.csv")
    (output_dir / "competitor-classification.json").write_text(json.dumps(competitors, indent=2, ensure_ascii=False), encoding="utf-8")
    if previous:
        comparison = compare(json.loads(previous.read_text(encoding="utf-8")), audit)
        (output_dir / "audit-comparison.json").write_text(json.dumps(comparison, indent=2, ensure_ascii=False), encoding="utf-8")
    payload = report_payload(config, audit)
    (output_dir / "report-input.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    if build_report:
        build_pdf(payload, output_dir / "beyond-seo-audit.pdf")
    return {"audit": str(audit_path.resolve()), "pages": len(pages), "queries": len(baseline), "findings": len(findings), "pdf": str((output_dir / "beyond-seo-audit.pdf").resolve()) if build_report else None}


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the Beyond SEO v1.3 audit pipeline.")
    parser.add_argument("--config", required=True, help="Audit configuration JSON.")
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--previous", help="Optional previous audit-data.json.")
    parser.add_argument("--no-pdf", action="store_true")
    args = parser.parse_args()
    result = run(json.loads(Path(args.config).read_text(encoding="utf-8")), Path(args.output_dir), Path(args.previous) if args.previous else None, not args.no_pdf)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
