#!/usr/bin/env python3
"""Run a reusable, evidence-led Beyond SEO crawl and SERP baseline."""

from __future__ import annotations

import argparse
import codecs
import hashlib
import http.client
import ipaddress
import json
import os
import re
import socket
import ssl
import time
from collections import Counter, deque
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urldefrag, urljoin, urlparse, urlunparse
from urllib.robotparser import RobotFileParser
from xml.etree import ElementTree

import requests
from bs4 import BeautifulSoup

from audit_compare import compare
from clarity_export import collect as collect_clarity
from clarity_export import load_saved_export as load_saved_clarity_export
from competitor_classifier import classify
from evidence_ledger import EvidenceLedger
from lighthouse_runner import collect as collect_performance
from report_builder import build_and_validate_pdf
from audit_quality import safe_config, sample_score, sanitize_artifact, validate_findings, write_reproducibility
from evidence_ledger import utc_now
from first_party_quality import validate_export


HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Encoding": "identity",
}
MAX_RESPONSE_BYTES = 10_000_000
MAX_REDIRECTS = 5
REDIRECT_STATUSES = {301, 302, 303, 307, 308}


def clean(value: str) -> str:
    return re.sub(r"\s+", " ", value or "").strip()


def canonical_host(value: str) -> str:
    return (value or "").lower().rstrip(".").removeprefix("www.")


def normalize_url(url: str, host: str) -> str | None:
    url = urldefrag(url)[0]
    parsed = urlparse(url)
    if (
        parsed.scheme not in {"http", "https"}
        or not parsed.hostname
        or parsed.username is not None
        or parsed.password is not None
        or canonical_host(parsed.hostname) != canonical_host(host)
    ):
        return None
    path = parsed.path or "/"
    # Slash, scheme and query variants are distinct URLs until the server proves otherwise.
    return parsed._replace(path=path, fragment="").geturl()


class PinnedHTTPConnection(http.client.HTTPConnection):
    def __init__(self, host: str, port: int, connect_ip: str, timeout: int):
        super().__init__(host, port=port, timeout=timeout)
        self._connect_ip = connect_ip

    def connect(self) -> None:
        self.sock = self._create_connection(
            (self._connect_ip, self.port),
            self.timeout,
            self.source_address,
        )


class PinnedHTTPSConnection(http.client.HTTPSConnection):
    def __init__(self, host: str, port: int, connect_ip: str, timeout: int):
        super().__init__(host, port=port, timeout=timeout, context=ssl.create_default_context())
        self._connect_ip = connect_ip

    def connect(self) -> None:
        self.sock = self._create_connection(
            (self._connect_ip, self.port),
            self.timeout,
            self.source_address,
        )
        self.sock = self._context.wrap_socket(self.sock, server_hostname=self.host)


def resolve_network_target(
    url: str,
    allowed_hosts: set[str] | None = None,
    allow_private_network: bool = False,
) -> tuple[object, str]:
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"}:
        raise ValueError("Only HTTP and HTTPS URLs are allowed.")
    if not parsed.hostname or parsed.username is not None or parsed.password is not None:
        raise ValueError("URLs must include a hostname and must not contain credentials.")
    host = canonical_host(parsed.hostname)
    allowed = {canonical_host(item) for item in (allowed_hosts or set())}
    if allowed and host not in allowed:
        raise ValueError(f"Network target host is outside the approved audit scope: {host}")
    try:
        port = parsed.port or (443 if parsed.scheme == "https" else 80)
    except ValueError as exc:
        raise ValueError("URL contains an invalid port.") from exc
    try:
        literal = ipaddress.ip_address(parsed.hostname.split("%", 1)[0])
        addresses = {literal}
    except ValueError:
        try:
            addresses = {
                ipaddress.ip_address(item[4][0].split("%", 1)[0])
                for item in socket.getaddrinfo(parsed.hostname, port, type=socket.SOCK_STREAM)
            }
        except (OSError, ValueError) as exc:
            raise ValueError(f"Could not safely resolve network target: {host}") from exc
    if not addresses:
        raise ValueError(f"Could not safely resolve network target: {host}")
    if not allow_private_network and any(not address.is_global for address in addresses):
        raise ValueError(f"Private or non-public network target is not allowed: {host}")
    selected = sorted(addresses, key=lambda address: (address.version, address.packed))[0]
    return parsed, str(selected)


def validate_network_url(
    url: str,
    allowed_hosts: set[str] | None = None,
    allow_private_network: bool = False,
) -> str:
    resolve_network_target(url, allowed_hosts, allow_private_network)
    return url


def open_pinned_response(url: str, parsed: object, connect_ip: str, timeout: int):
    port = parsed.port or (443 if parsed.scheme == "https" else 80)
    connection_class = PinnedHTTPSConnection if parsed.scheme == "https" else PinnedHTTPConnection
    connection = connection_class(parsed.hostname, port, connect_ip, timeout)
    target = urlunparse(("", "", parsed.path or "/", parsed.params, parsed.query, ""))
    connection.request("GET", target, headers=HEADERS)
    return connection, connection.getresponse()


def fetch(
    url: str,
    timeout: int = 25,
    allowed_hosts: set[str] | None = None,
    allow_private_network: bool = False,
    max_bytes: int = MAX_RESPONSE_BYTES,
) -> dict:
    current = url
    chain = []
    collected_at = utc_now()
    try:
        for _ in range(MAX_REDIRECTS + 1):
            parsed, connect_ip = resolve_network_target(current, allowed_hosts, allow_private_network)
            connection, response = open_pinned_response(current, parsed, connect_ip, timeout)
            try:
                headers = requests.structures.CaseInsensitiveDict(response.getheaders())
                if response.status in REDIRECT_STATUSES and headers.get("Location"):
                    chain.append({"url": current, "status": response.status, "location": urljoin(current, headers["Location"])})
                    current = urljoin(current, headers["Location"])
                    continue
                content_length = headers.get("Content-Length")
                if content_length and int(content_length) > max_bytes:
                    raise ValueError(f"Response exceeded the {max_bytes}-byte audit limit.")
                chunks: list[bytes] = []
                received = 0
                while True:
                    chunk = response.read(65536)
                    if not chunk:
                        break
                    received += len(chunk)
                    if received > max_bytes:
                        raise ValueError(f"Response exceeded the {max_bytes}-byte audit limit.")
                    chunks.append(chunk)
                charset = re.search(r"charset\s*=\s*[\"']?([^;\s\"']+)", headers.get("Content-Type", ""), re.I)
                encoding = charset.group(1) if charset else "utf-8-sig"
                try:
                    codecs.lookup(encoding)
                except LookupError:
                    encoding = "utf-8-sig"
                text = b"".join(chunks).decode(encoding, errors="replace")
                return {
                    "url": url,
                    "status": response.status,
                    "final_url": current,
                    "headers": dict(headers),
                    "text": text,
                    "collected_at": collected_at,
                    "redirect_chain": chain,
                    "response_sha256": hashlib.sha256(b"".join(chunks)).hexdigest(),
                }
            finally:
                response.close()
                connection.close()
        raise ValueError(f"Response exceeded the {MAX_REDIRECTS}-redirect audit limit.")
    except (OSError, http.client.HTTPException, ssl.SSLError, ValueError) as exc:
        return {"url": url, "status": None, "final_url": current, "headers": {}, "text": "", "error": str(exc), "collected_at": collected_at, "redirect_chain": chain}


def parse_page(result: dict, host: str) -> dict:
    soup = BeautifulSoup(result.get("text", ""), "html.parser")
    title = clean(soup.title.get_text(" ")) if soup.title else ""
    meta_tag = soup.find("meta", attrs={"name": re.compile("^description$", re.I)})
    canonical_tag = soup.find("link", attrs={"rel": lambda value: value and "canonical" in value})
    meta_description = clean(meta_tag.get("content", "")) if meta_tag else ""
    canonical = canonical_tag.get("href", "") if canonical_tag else ""
    robots_tags = soup.find_all("meta", attrs={"name": re.compile("^(robots|googlebot)$", re.I)})
    robots_text = ", ".join(clean(tag.get("content", "")) for tag in robots_tags)
    headers = requests.structures.CaseInsensitiveDict(result.get("headers", {}))
    xrobots = headers.get("X-Robots-Tag", "")
    # Directives for an unrelated bot do not establish Google's noindex state.
    active_bot = ""
    relevant_directives = []
    for segment in xrobots.split(","):
        segment = segment.strip()
        if ":" in segment:
            prefix, directive = segment.split(":", 1)
            if prefix.lower() not in {"max-snippet", "max-video-preview", "max-image-preview", "unavailable_after"}:
                active_bot = prefix.lower()
                segment = directive.strip()
        if active_bot in {"", "googlebot"}:
            relevant_directives.append(segment)
    general_xrobots = ",".join(relevant_directives)
    noindex = bool(re.search(r"\b(noindex|none)\b", robots_text + "," + general_xrobots, re.I))
    links = []
    for anchor in soup.find_all("a", href=True):
        normalized = normalize_url(urljoin(result.get("final_url") or result["url"], anchor["href"]), host)
        if normalized:
            links.append(normalized)
    schema = []
    for script in soup.find_all("script", attrs={"type": re.compile("ld\\+json", re.I)}):
        schema.extend(re.findall(r'"@type"\s*:\s*"([^"]+)"', script.string or script.get_text() or ""))
    for tag in soup.find_all(["script", "style", "template", "head"]):
        tag.decompose()
    for tag in soup.select("[hidden], [aria-hidden='true']"):
        tag.decompose()
    body = clean(soup.get_text(" "))
    visible_hash = hashlib.sha256(body.encode("utf-8")).hexdigest() if body else ""
    content_type = headers.get("Content-Type", "").lower()
    is_html = ("text/html" in content_type or "application/xhtml+xml" in content_type) if content_type else bool(re.search(r"<(html|head|body|title|h1)\b", result.get("text", ""), re.I))
    checks = ["http-availability"] if result.get("status") is not None else []
    if result.get("status") == 200 and is_html:
        checks += ["noindex-review"]
        if not noindex:
            checks += ["missing-title", "missing-h1", "content-review", "canonical-review", "duplicate-review"]
    return {
        "url": result["url"], "status": result.get("status"), "final_url": result.get("final_url"),
        "title": title, "meta_description": meta_description,
        "canonical": canonical,
        "robots": robots_text, "x_robots_tag": xrobots, "http_link_header": headers.get("Link", ""),
        "h1": [clean(tag.get_text(" ")) for tag in soup.find_all("h1") if clean(tag.get_text(" "))],
        "h2": [clean(tag.get_text(" ")) for tag in soup.find_all("h2") if clean(tag.get_text(" "))][:15],
        "word_count": len(re.findall(r"\b[\w'-]{2,}\b", body)),
        "schema_types": sorted(set(schema)), "internal_links": sorted(set(links)),
        "visible_text_hash": visible_hash, "noindex": noindex,
        "is_html": is_html, "content_type": content_type,
        "collection_method": "HTTP HTML extraction; JavaScript not rendered",
        "collected_at": result.get("collected_at") or utc_now(),
        "response_sha256": result.get("response_sha256", ""),
        "redirect_chain": result.get("redirect_chain", []),
        "error": result.get("error", ""), "checks_performed": checks,
        "google_indexation": "Not verified",
        "technical_observation": "Not verified" if result.get("status") is None else "No noindex detected in fetched response" if not noindex else "Noindex detected in fetched response",
    }


def parse_sitemap(text: str) -> list[str]:
    try:
        root = ElementTree.fromstring(text)
    except ElementTree.ParseError:
        return []
    if root.tag.rsplit("}", 1)[-1] not in {"sitemapindex", "urlset"}:
        return []
    return [clean(child.text or "") for entry in root for child in entry if child.tag.rsplit("}", 1)[-1] == "loc"]


def collect_sitemap_urls(
    sitemap_url: str,
    host: str,
    max_sitemaps: int = 25,
    allowed_sitemap_hosts: set[str] | None = None,
    allow_private_network: bool = False,
    metadata: dict | None = None,
    max_urls: int = 10000,
) -> tuple[int | None, list[str]]:
    allowed_hosts = {canonical_host(host), *(canonical_host(item) for item in (allowed_sitemap_hosts or set()))}
    queue = deque([sitemap_url])
    seen_sitemaps: set[str] = set()
    page_urls: set[str] = set()
    root_status = None
    issues = []
    while queue and len(seen_sitemaps) < max_sitemaps:
        current = queue.popleft()
        if current in seen_sitemaps:
            continue
        seen_sitemaps.add(current)
        result = fetch(current, allowed_hosts=allowed_hosts, allow_private_network=allow_private_network)
        if root_status is None:
            root_status = result.get("status")
        try:
            root = ElementTree.fromstring(result.get("text", ""))
            kind = root.tag.rsplit("}", 1)[-1]
        except ElementTree.ParseError:
            kind = "invalid"
        if result.get("status") != 200 or kind not in {"sitemapindex", "urlset"}:
            issues.append({"url": current, "status": result.get("status"), "reason": "Sitemap unavailable or invalid XML"})
            continue
        for location in parse_sitemap(result.get("text", "")):
            if kind == "sitemapindex":
                try:
                    validate_network_url(location, allowed_hosts, allow_private_network)
                except ValueError:
                    issues.append({"url": location, "reason": "Sitemap host outside scope or unsafe"})
                    continue
                queue.append(location)
                continue
            normalized = normalize_url(location, host)
            if normalized:
                page_urls.add(normalized)
                if len(page_urls) >= max_urls:
                    issues.append({"reason": "Sitemap URL limit reached"})
                    break
        if len(page_urls) >= max_urls:
            break
    if queue:
        issues.append({"reason": "Sitemap traversal limit reached"})
    if metadata is not None:
        metadata.update({"complete": not issues, "issues": issues, "sitemaps_attempted": len(seen_sitemaps), "max_sitemaps": max_sitemaps, "max_urls": max_urls})
    return root_status, sorted(page_urls)


def crawl(config: dict) -> tuple[list[dict], dict, dict]:
    start = config["website_url"]
    host = canonical_host(urlparse(start).hostname or "")
    allow_private_network = config.get("allow_private_network", False) is True
    site_hosts = {host}
    sitemap_hosts = {canonical_host(item) for item in config.get("allowed_sitemap_hosts", [])}
    robots = fetch(
        urljoin(start, "/robots.txt"),
        allowed_hosts=site_hosts,
        allow_private_network=allow_private_network,
    )
    robots_parser = RobotFileParser()
    robots_parser.set_url(robots.get("final_url") or urljoin(start, "/robots.txt"))
    if robots.get("status") == 200:
        robots_parser.parse(robots.get("text", "").splitlines())
    sitemap_url = config.get("sitemap_url") or urljoin(start, "/sitemap.xml")
    sitemap_metadata = {}
    sitemap_status, sitemap_urls = collect_sitemap_urls(
        sitemap_url,
        host,
        allowed_sitemap_hosts=sitemap_hosts,
        allow_private_network=allow_private_network,
        metadata=sitemap_metadata,
        max_urls=min(int(config.get("max_discovered_urls", 10000)), 50000),
    )
    seeds = [start, *sitemap_urls, *config.get("seed_urls", [])]
    discovery_limit = min(int(config.get("max_discovered_urls", 10000)), 50000)
    normalized_seeds = list(dict.fromkeys(filter(None, (normalize_url(urljoin(start, url), host) for url in seeds))))
    queue = deque(normalized_seeds[:discovery_limit])
    seen, pages, robots_blocked, excluded = set(), [], [], []
    discovered = set(queue)
    frontier_limited = len(normalized_seeds) > discovery_limit
    sitemap_set = set(filter(None, sitemap_urls))
    max_pages = min(int(config.get("max_crawl_pages", 100)), 500)
    robots_unknown = config.get("respect_robots_txt", True) and (robots.get("status") is None or robots.get("status", 0) >= 500 or robots.get("status") == 429)
    robots_denied = config.get("respect_robots_txt", True) and robots.get("status") in {401, 403}
    while queue and len(pages) < max_pages:
        url = queue.popleft()
        if url in seen:
            continue
        seen.add(url)
        if any(urlparse(url).path.startswith(prefix) for prefix in config.get("exclude_paths", [])):
            excluded.append(url)
            continue
        if robots_unknown:
            break
        if robots_denied or (config.get("respect_robots_txt", True) and robots.get("status") == 200 and not robots_parser.can_fetch(HEADERS["User-Agent"], url)):
            robots_blocked.append(url)
            continue
        page = parse_page(fetch(url, allowed_hosts=site_hosts, allow_private_network=allow_private_network), host)
        page["in_sitemap"] = url in sitemap_set
        page["googlebot_robots_allowed"] = robots_parser.can_fetch("Googlebot", url) if robots.get("status") == 200 else None
        if url not in set(config.get("priority_urls", [])):
            page["checks_performed"] = [check for check in page["checks_performed"] if check != "noindex-review"]
        if sitemap_metadata.get("complete") and page.get("status") == 200 and page.get("is_html") and not page.get("noindex"):
            page["checks_performed"].append("sitemap-review")
        pages.append(page)
        if page.get("status") == 200:
            for link in page["internal_links"]:
                if link not in discovered:
                    if len(discovered) >= discovery_limit:
                        frontier_limited = True
                        continue
                    discovered.add(link)
                    queue.append(link)
        time.sleep(float(config.get("crawl_delay_seconds", 0.1)))
    attempted = {page["url"] for page in pages}
    unattempted = sorted(discovered - attempted - set(robots_blocked) - set(excluded))
    coverage = {
        "discovered_urls": len(discovered), "attempted_urls": len(pages),
        "successful_urls": sum(p.get("status") == 200 for p in pages),
        "failed_urls": [p["url"] for p in pages if p.get("status") != 200],
        "blocked_urls": robots_blocked, "excluded_urls": excluded, "unattempted_urls": unattempted,
        "rendered_urls": 0, "rendering": "Not verified; HTTP extraction only",
        "max_crawl_pages": max_pages, "max_discovered_urls": discovery_limit,
        "stopping_reason": "robots_unavailable" if robots_unknown else "page_limit" if unattempted else "discovery_limit" if frontier_limited else "frontier_exhausted",
        "partial": bool(unattempted or frontier_limited or robots_blocked or excluded or not sitemap_metadata.get("complete") or any(p.get("status") != 200 for p in pages)),
        "templates_sampled": config.get("page_templates", {}),
        "template_note": "Owner-supplied template mapping; unlisted templates are not verified",
        "limitations": "Discovered URLs are not the total site inventory. HTTP parsing does not prove Google rendering or indexation. Robots matching uses Python RobotFileParser, not a complete Googlebot emulator.",
    }
    template_mapping = config.get("page_templates", {})
    coverage["template_counts"] = dict(Counter(template_mapping.get(p["url"], "Unclassified") for p in pages))
    return pages, {"status": robots.get("status"), "url": robots.get("final_url"), "blocked_urls": robots_blocked, "coverage": coverage}, {"status": sitemap_status, "url": sitemap_url, "urls": sitemap_urls, **sitemap_metadata}


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
    response = requests.post(
        endpoint,
        params={"timeout": 300},
        headers={"Authorization": f"Bearer {token}"},
        json=payload,
        timeout=330,
    )
    try:
        response.raise_for_status()
    except requests.HTTPError as exc:
        raise RuntimeError(f"Apify SERP request failed with HTTP {response.status_code}.") from exc
    rows = response.json()
    if not isinstance(rows, list) or any(not isinstance(row, dict) for row in rows):
        raise ValueError("SERP export must be an array of result objects.")
    (output_dir / "apify-serp-raw.json").write_text(json.dumps(sanitize_artifact(rows), indent=2, ensure_ascii=False), encoding="utf-8")
    return rows


def normalize_serps(items: list[dict], target_host: str, config: dict | None = None, collected_at: str | None = None) -> tuple[list[dict], list[dict]]:
    baseline, candidates = [], []
    config = config or {}
    collected_at = collected_at or utc_now()
    for raw_index, item in enumerate(items):
        query = (item.get("searchQuery") or {}).get("term") or item.get("query") or ""
        organic = item.get("organicResults") or []
        if not query or not isinstance(organic, list):
            continue
        depth = min(len(organic), int(config.get("serp_results_per_query", 10)), 10)
        context = {"collected_at": collected_at, "country": config.get("country_code", "Not verified"),
                   "language": config.get("language_code", "Not verified"), "device": config.get("device", "Not verified"),
                   "location": "Country scope only; city targeting not configured by this runner", "sample_depth": depth,
                   "serp_features": [key for key in ("paidResults", "peopleAlsoAsk", "relatedQueries", "aiOverview", "localResults") if item.get(key)],
                   "position_definition": "Ordinal among sampled organic results; not absolute SERP position", "artifact_index": raw_index}
        own = []
        for position, result in enumerate(organic[:depth], 1):
            domain = urlparse(result.get("url", "")).netloc.lower().removeprefix("www.")
            if domain == target_host:
                own.append((position, result.get("url")))
            elif domain:
                candidates.append({"domain": domain, "ranking_url": result.get("url", ""), "title": result.get("title", ""), "description": result.get("description", ""), "ranking_keyword": query, "observed_position": position, **context})
        baseline.append({"keyword": query, "observed_position": min((row[0] for row in own), default=None), "observed_url": own[0][1] if own else None, "source": "Apify Google Search Scraper", "evidence_label": "Live SERP sample" if depth else "Not verified",
                         "visibility": f"Observed organic position {own[0][0]}" if own else f"Not visible within sampled top {depth}" if depth else "No usable organic results returned", **context})
    counts = Counter(row["domain"] for row in candidates)
    for row in candidates:
        row["serp_appearances"] = counts[row["domain"]]
    unique = {row["domain"]: row for row in candidates}
    return baseline, list(unique.values())


def build_findings(pages: list[dict], sitemap: dict, target_host: str, config: dict | None = None) -> list[dict]:
    config = config or {}
    findings = []
    live = [page for page in pages if page.get("status") == 200 and page.get("is_html") and not page.get("noindex")]
    priorities = set(config.get("priority_urls", []))

    def add(check_id, title, affected, severity, interpretation, action, criteria):
        if not affected:
            return
        urls = sorted(p["url"] for p in affected)
        identifier = check_id
        findings.append({
            "id": identifier, "finding_id": identifier, "check_id": check_id, "finding": title,
            "affected_urls": urls, "evidence": urls,
            "observation": title + f" ({len(urls)} fetched URL(s)); see evidence records for parsed values.",
            "evidence_ids": [p["evidence_id"] for p in affected], "source_artifact": "crawl-observations.json",
            "collected_at": max(p["collected_at"] for p in affected),
            "observation_label": "Confirmed", "evidence_label": "Confirmed",
            "interpretation": interpretation, "interpretation_label": "Inferred", "confidence": "Context review required",
            "business_impact": "Owner-designated priority pages affected" if priorities.intersection(urls) else "Business impact not verified; review page intent and first-party demand",
            "severity": severity, "owner": "Site owner / SEO reviewer", "recommended_action": action, "fix": action,
            "acceptance_criteria": criteria, "validation_method": "Re-fetch affected URLs; inspect rendered page and intended behavior where required",
        })

    add("http-availability", "URLs returned HTTP errors", [p for p in pages if p.get("status", 0) and p["status"] >= 400], "High",
        "An error was returned to this audit request; intended removals and temporary bot restrictions need review.",
        "Confirm whether each URL should work. Restore intended pages or document intentional removals; do not redirect all errors to the homepage.",
        "Intended pages return the expected status and useful content; intentional removals are documented.")
    add("missing-title", "HTML title absent in fetched pages", [p for p in live if not p.get("title")], "Medium",
        "Missing title may reduce clarity; Google ranking or snippet impact is not established.",
        "Check rendered output and add an intent-aligned title if absent in the final page.", "Expected title is present in source/rendered HTML and matches page purpose.")
    add("missing-h1", "H1 absent in fetched HTML", [p for p in live if not p.get("h1")], "Low",
        "Heading structure needs review; extraction does not establish rendered absence or ranking loss.",
        "Review rendered heading hierarchy and add a descriptive primary heading where useful.", "Rendered primary heading accurately describes the page; HTML findings are rechecked.")
    add("content-review", "Short extracted text requires page-purpose review", [p for p in live if p.get("word_count", 0) < 400], "Review",
        "Word count is a screening signal, not a content-quality failure; JavaScript content is not rendered.",
        "Check page type, intent satisfaction, original proof and rendered content. Expand only if information is missing.", "Reviewer records whether intent is satisfied and verifies any factual additions; no arbitrary word target.")
    add("canonical-review", "Canonical link absent in fetched HTML", [p for p in live if not p.get("canonical")], "Review",
        "Canonical absence alone is not an indexing failure; HTTP Link headers, duplicates and selected canonicals need review.",
        "Check URL variants, HTTP Link headers and Google-selected canonical before proposing a canonical change.", "Preferred URL strategy is documented and source/header signals agree where applicable.")
    groups = {}
    for page in live:
        if page.get("visible_text_hash"):
            groups.setdefault(page["visible_text_hash"], []).append(page)
    duplicates = [p for group in groups.values() if len(group) > 1 for p in group]
    add("duplicate-review", "Identical extracted text across fetched URLs", duplicates, "Review",
        "Shared text may reflect variants, templates or JS shells; it does not prove duplicate rendered pages.",
        "Inspect rendered pages and intent. Consolidate only equivalent pages after reviewing links, traffic and redirect targets.", "Each duplicate group has a documented decision; redirects are tested only where consolidation is justified.")
    add("noindex-review", "Noindex detected on intended search pages", [p for p in pages if p["url"] in priorities and p.get("noindex")], "High",
        "Owner designated these pages for search; detected noindex conflicts with that intent unless deliberate.",
        "Confirm intent, inspect robots directives and remove unintended noindex after review.", "Intended search pages have no unintended source/header noindex; Google indexation is checked separately in GSC.")
    if sitemap.get("complete"):
        add("sitemap-review", "Fetched pages absent from successfully traversed sitemap", [p for p in live if p["url"] not in set(sitemap.get("urls", []))], "Review",
            "Sitemap omission is not proof of indexing failure; canonical variants and intentional omissions need review.",
            "Confirm preferred URLs and sitemap scope. Include intended canonical pages where appropriate.", "Expected canonical URLs are included or intentional exclusions are documented.")
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
            export = load_saved_clarity_export(Path(export_path), num_days, dimensions)
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
    rubric = audit.get("sample_score") or sample_score(pages, config)
    technical_score = rubric["score"]
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
    data_gaps.extend(audit.get("data_gaps", []))
    sources = [{"label": "Website", "url": config["website_url"]}]
    if clarity_verified:
        sources.append({
            "label": "Microsoft Clarity Data Export API",
            "url": clarity.get("source_url", "https://learn.microsoft.com/en-us/clarity/setup-and-installation/clarity-data-export-api"),
        })
    payload = {
        "title": "Beyond SEO Evidence-Led Audit", "client": config.get("client_name") or urlparse(config["website_url"]).netloc,
        "site_url": config["website_url"], "audit_date": audit["audit_date"][:10], "audit_mode": audit["audit_mode"],
        "overall_score": None, "status": "Partial audit" if audit.get("coverage", {}).get("partial", True) else "Observed crawl sample",
        "summary": f"Reviewed {len(pages)} URLs, {len(live)} successful pages, {len(audit['rank_baseline'])} live SERP samples, and {len(findings)} prioritized findings.",
        "data_confidence": audit["data_confidence"],
        "scores": [{"area": "Observed sample checks", "score": technical_score, "display": f"{technical_score} / 100" if technical_score is not None else "Not verified", "note": rubric["limitations"]}],
        "score_methodology": rubric, "coverage": audit.get("coverage", {}),
        "findings": [{**row, "issue": row["finding"], "evidence": "; ".join(row["affected_urls"][:3]) + (f"; +{len(row['affected_urls']) - 3} more in crawl-observations.json" if len(row["affected_urls"]) > 3 else ""), "priority": row["severity"], "fix": row["fix"]} for row in findings],
        "keywords": [{"keyword": row["keyword"], "intent": "Requires mapping", "source": row["source"], "volume": "Not verified", "difficulty": "Not verified", "action": "Review target page", "confidence": row["evidence_label"]} for row in audit["rank_baseline"]],
        "competitors": [{"competitor": row["domain"], "evidence": f"Position {row.get('observed_position')} for {row.get('ranking_keyword')}", "gap": row.get("classification"), "action": "Crawl and compare the ranking page."} for row in audit["competitors"].get("comparable", [])[:10]],
        "roadmap": config.get("roadmap", []), "data_gaps": data_gaps,
        "sources": sources,
        "first_party_quality": audit.get("first_party_quality", []),
        "strict_evidence": True, "evidence_records": audit.get("evidence_records", []),
    }
    if clarity_verified:
        payload["clarity"] = clarity.get("report_section", {})
    imported = {row.get("source") for row in audit.get("first_party_quality", []) if row.get("passed")}
    if "gsc" in imported:
        payload["data_gaps"] = [row for row in payload["data_gaps"] if row.get("source", "").lower() not in {"gsc", "google search console"}]
    return payload


def run(config: dict, output_dir: Path, previous: Path | None = None, build_report: bool = True) -> dict:
    if (output_dir / "audit-data.json").exists() or (output_dir / "reproducibility-manifest.json").exists():
        raise ValueError("Audit output already exists; use a new dated directory to preserve evidence.")
    for key, default, maximum in (("max_crawl_pages", 100, 500), ("max_discovered_urls", 10000, 50000), ("max_serp_queries", 20, 100), ("serp_results_per_query", 10, 10)):
        value = config.get(key, default)
        if not isinstance(value, int) or isinstance(value, bool) or not 1 <= value <= maximum:
            raise ValueError(f"{key} must be an integer from 1 to {maximum}.")
    if not isinstance(config.get("crawl_delay_seconds", 0.1), (int, float)) or not 0 <= config.get("crawl_delay_seconds", 0.1) <= 60:
        raise ValueError("crawl_delay_seconds must be between 0 and 60.")
    output_dir.mkdir(parents=True, exist_ok=True)
    collected_at = utc_now()
    pages, robots, sitemap = crawl(config)
    target_host = urlparse(config["website_url"]).netloc.lower().removeprefix("www.")
    gaps = []
    try:
        serp_items = run_apify_serp(config, output_dir)
    except (RuntimeError, requests.RequestException, ValueError):
        serp_items = []
        gaps.append({"source": "Live SERP", "needed": "SERP collection did not complete; retry in a new dated run. No ranking claims are available."})
    baseline, candidates = normalize_serps(serp_items, target_host, config, collected_at)
    competitors = classify(candidates, config)
    performance_settings = config.get("performance", {})
    performance = [
        collect_performance(
            config["website_url"],
            strategy,
            output_dir,
            os.getenv("PAGESPEED_API_KEY"),
            performance_settings.get("allow_local_lighthouse", False) is True,
        )
        for strategy in ("mobile", "desktop")
    ] if performance_settings.get("enabled", True) else []
    clarity = collect_clarity_evidence(config, output_dir)
    ledger = EvidenceLedger()
    for index, page in enumerate(pages):
        record = ledger.add(source_type="crawl", source_name="Native HTTP observation", source_url=page["url"],
                            collected_at=page["collected_at"], method=page.get("collection_method", "HTTP HTML extraction"),
                            provenance="direct_observation", scope=page["url"], label="Confirmed" if page.get("status") is not None else "Not verified",
                            artifact_path="crawl-observations.json", artifact_locator=f"/{index}", metric="page_observation",
                            value={key: page.get(key) for key in ("status", "title", "h1", "canonical", "noindex", "word_count", "visible_text_hash", "response_sha256")})
        page["evidence_id"] = record["id"]
    findings = build_findings(pages, sitemap, target_host, config)
    validate_findings(findings, ledger.records)
    if baseline:
        for index, row in enumerate(baseline):
            ledger.add(source_type="serp", source_name=row["source"], actor_id="apify/google-search-scraper", method=row["position_definition"], provenance="authenticated_api", scope=row["keyword"], label=row["evidence_label"], artifact_path="apify-serp-raw.json", artifact_locator=f"/{row['artifact_index']}", collected_at=collected_at, country=row["country"], language=row["language"], device=row["device"], sample_depth=row["sample_depth"])
    if clarity and clarity.get("evidence_label") == "First-party verified":
        ledger.add(
            source_type="behavior analytics",
            source_name="Microsoft Clarity Data Export API",
            source_url=clarity.get("source_url", ""),
            method=(
                "owner-supplied dated export"
                if clarity.get("provenance") == "owner_export"
                else "authenticated project export"
            ),
            provenance=clarity.get("provenance", "unknown"),
            scope=f"Previous {clarity.get('num_days')} day(s); dimensions: {', '.join(clarity.get('dimensions') or []) or 'none'}",
            label="First-party verified",
            artifact_path=str(output_dir / "clarity-live-insights.json"),
        )
    first_party = []
    for item in config.get("first_party_imports", []):
        try:
            metadata = json.loads(Path(item["metadata_path"]).read_text(encoding="utf-8"))
            quality = validate_export(Path(item["input_path"]), metadata, config["website_url"])
        except (OSError, ValueError, KeyError):
            quality = {"passed": False, "evidence_label": "Not verified", "errors": ["Import file or metadata could not be read."], "source": "Unknown"}
        first_party.append(quality)
        if quality["passed"]:
            for metric, value in quality["summary"].items():
                ledger.add(source_type="search_console" if quality["source"] == "gsc" else "analytics", source_name=quality["source"],
                           collected_at=metadata["retrieved_at"], provenance=metadata["provenance"], label="First-party verified",
                           scope=str(metadata["property"]), metric=metric, value=value, artifact_path="first-party-quality.json",
                           artifact_locator=f"/{len(first_party)-1}/summary/{metric}", measurement_start=metadata["start_date"], measurement_end=metadata["end_date"])
        else:
            gaps.append({"source": quality["source"], "needed": "; ".join(quality["errors"][:5])})
    clarity_verified = clarity and clarity.get("evidence_label") == "First-party verified"
    audit_mode = "Apify + native crawl" if baseline else "Native crawl"
    if clarity_verified:
        audit_mode += " + Microsoft Clarity"
    data_confidence = [
        {"label": "Confirmed" if any(p.get("status") is not None for p in pages) else "Not verified", "value": f"Native crawl: {len(pages)} attempted URLs; HTTP extraction only"},
        {"label": "Live SERP sample" if any(row["sample_depth"] for row in baseline) else "Not verified", "value": f"{len(baseline)} one-time query records; empty samples do not establish visibility"},
        {
            "label": "First-party verified" if clarity_verified else "Not verified",
            "value": (
                f"Microsoft Clarity: previous {clarity.get('num_days')} day(s)"
                if clarity_verified
                else "Microsoft Clarity: connect CLARITY_API_TOKEN or provide a dated export"
            ),
        },
        {"label": "Not verified", "value": "Backlinks, proprietary volume/KD and any first-party sources not successfully imported"},
    ]
    data_confidence.extend({"label": item["evidence_label"], "value": f"{item.get('source')}: {item.get('row_count', 0)} normalized rows; {'validation passed' if item['passed'] else 'validation failed'}"} for item in first_party)
    audit = {
        "schema_version": "1.4.0", "audit_date": collected_at,
        "audit_mode": audit_mode,
        "business_context": safe_config(config), "robots": robots, "sitemap": sitemap, "pages": pages,
        "findings": findings, "rank_baseline": baseline, "competitors": competitors,
        "performance": performance, "clarity": clarity,
        "data_confidence": data_confidence,
        "coverage": robots.get("coverage", {"partial": True, "stopping_reason": "Coverage not recorded"}),
        "sample_score": sample_score(pages, config), "first_party_quality": first_party,
        "evidence_records": ledger.records, "data_gaps": gaps,
    }
    audit = sanitize_artifact(audit)
    pages = audit["pages"]
    ledger.records = audit["evidence_records"]
    competitors = audit["competitors"]
    first_party = audit["first_party_quality"]
    audit_path = output_dir / "audit-data.json"
    audit_path.write_text(json.dumps(audit, indent=2, ensure_ascii=False), encoding="utf-8")
    (output_dir / "crawl-observations.json").write_text(json.dumps(pages, indent=2, ensure_ascii=False), encoding="utf-8")
    (output_dir / "crawl-coverage.json").write_text(json.dumps(audit["coverage"], indent=2, ensure_ascii=False), encoding="utf-8")
    (output_dir / "first-party-quality.json").write_text(json.dumps(first_party, indent=2, ensure_ascii=False), encoding="utf-8")
    ledger.write(output_dir / "evidence-ledger.json", output_dir / "evidence-ledger.csv")
    (output_dir / "competitor-classification.json").write_text(json.dumps(competitors, indent=2, ensure_ascii=False), encoding="utf-8")
    if previous:
        comparison = compare(json.loads(previous.read_text(encoding="utf-8")), audit)
        (output_dir / "audit-comparison.json").write_text(json.dumps(comparison, indent=2, ensure_ascii=False), encoding="utf-8")
    payload = sanitize_artifact(report_payload(config, audit))
    (output_dir / "report-input.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    pdf_path = output_dir / "beyond-seo-audit.pdf"
    qa_path = output_dir / "beyond-seo-audit.qa.json"
    if build_report:
        build_and_validate_pdf(payload, pdf_path, qa_path)
    write_reproducibility(output_dir, config, collected_at)
    return {
        "audit": str(audit_path.resolve()),
        "pages": len(pages),
        "queries": len(baseline),
        "findings": len(findings),
        "pdf": str(pdf_path.resolve()) if build_report else None,
        "pdf_qa": str(qa_path.resolve()) if build_report else None,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the Beyond SEO v1.4 evidence-led audit pipeline.")
    parser.add_argument("--config", required=True, help="Audit configuration JSON.")
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--previous", help="Optional previous audit-data.json.")
    parser.add_argument("--no-pdf", action="store_true")
    args = parser.parse_args()
    result = run(json.loads(Path(args.config).read_text(encoding="utf-8")), Path(args.output_dir), Path(args.previous) if args.previous else None, not args.no_pdf)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
