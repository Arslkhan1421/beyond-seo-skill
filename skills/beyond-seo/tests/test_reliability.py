from __future__ import annotations

import hashlib
import json
import sys
import tempfile
import unittest
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from audit_compare import compare
from audit_quality import safe_config, sample_score, sanitize_artifact, validate_findings, write_reproducibility
from audit_runner import build_findings, crawl, normalize_serps, normalize_url, parse_page, parse_sitemap, run
from evidence_ledger import EvidenceLedger, normalize_record
from first_party_quality import comparison_compatibility, validate_export
from outcome_tracker import assess_outcome
from report_builder import build_and_validate_pdf
from lighthouse_runner import run_pagespeed, summarize_lighthouse


def response(url="https://example.com/", status=200, text="<html><head><title>Example</title></head><body><h1>Example</h1><p>Useful information.</p></body></html>", headers=None):
    return {"url": url, "final_url": url, "status": status, "text": text,
            "headers": headers or {"Content-Type": "text/html"}, "collected_at": "2026-10-05T09:00:00Z"}


def observed(text):
    page = parse_page(response(text=text), "example.com")
    page["evidence_id"] = "page-1"
    return page


class FindingReliabilityTests(unittest.TestCase):
    def test_js_shell_is_review_signal_not_content_failure(self):
        page = observed('<html><head><title>App</title></head><body><div id="root"></div><script>const secret = "not visible";</script></body></html>')
        self.assertEqual(page["word_count"], 0)
        findings = build_findings([page], {"status": None}, "example.com")
        short = next(f for f in findings if f["check_id"] == "content-review")
        self.assertEqual(short["severity"], "Review")
        self.assertEqual(short["interpretation_label"], "Inferred")
        self.assertEqual(page["google_indexation"], "Not verified")

    def test_canonical_and_meta_are_preserved_before_text_extraction(self):
        page = observed('<html><head><title>App</title><link rel="canonical" href="/preferred"><meta name="description" content="Description"></head><body><h1>Hello</h1></body></html>')
        self.assertEqual(page["canonical"], "/preferred")
        self.assertEqual(page["meta_description"], "Description")
        self.assertEqual(page["word_count"], 1)

    def test_header_and_googlebot_meta_noindex_are_detected(self):
        for headers, text in [({"x-robots-tag": "noindex"}, "<html><h1>Hello</h1></html>"),
                              ({}, '<html><meta name="googlebot" content="noindex"><h1>Hello</h1></html>')]:
            with self.subTest(headers=headers):
                page = parse_page(response(headers=headers, text=text), "example.com")
                self.assertTrue(page["noindex"])

    def test_unrelated_bot_directive_is_not_google_noindex(self):
        page = parse_page(response(headers={"X-Robots-Tag": "bingbot: noindex"}), "example.com")
        self.assertFalse(page["noindex"])
        page = parse_page(response(headers={"X-Robots-Tag": "bingbot: nofollow, noindex"}), "example.com")
        self.assertFalse(page["noindex"])

    def test_unavailable_sitemap_does_not_produce_omission_finding(self):
        page = observed("<html><title>Useful</title><h1>Useful</h1></html>")
        findings = build_findings([page], {"status": 503, "urls": []}, "example.com")
        self.assertNotIn("sitemap-review", {f["check_id"] for f in findings})

    def test_failed_pages_do_not_produce_heading_or_content_claims(self):
        page = parse_page(response(status=500, text=""), "example.com")
        page["evidence_id"] = "error-1"
        findings = build_findings([page], {}, "example.com")
        self.assertEqual([f["check_id"] for f in findings], ["http-availability"])

    def test_evidence_references_must_exist(self):
        page = observed("<html></html>")
        findings = build_findings([page], {}, "example.com")
        with self.assertRaises(ValueError):
            validate_findings(findings, [])

    def test_confirmed_finding_cannot_reference_unverified_evidence(self):
        page = observed("<html></html>")
        findings = build_findings([page], {}, "example.com")
        with self.assertRaises(ValueError):
            validate_findings(findings, [{"id": "page-1", "label": "Not verified"}])

    def test_strict_report_rejects_unsupported_evidence(self):
        page = observed("<html></html>")
        findings = build_findings([page], {}, "example.com")
        with tempfile.TemporaryDirectory() as directory, self.assertRaises(ValueError):
            build_and_validate_pdf({"strict_evidence": True, "findings": findings, "evidence_records": []}, Path(directory)/"report.pdf")

    def test_report_cannot_accept_unsourced_keyword_volume(self):
        with tempfile.TemporaryDirectory() as directory, self.assertRaises(ValueError):
            build_and_validate_pdf({'keywords': [{'keyword': 'service', 'volume': 100}]}, Path(directory)/'report.pdf')


class ScoringTests(unittest.TestCase):
    def test_empty_and_failed_transport_have_no_score(self):
        self.assertIsNone(sample_score([], {})["score"])
        page = parse_page(response(status=None, text=""), "example.com")
        self.assertIsNone(sample_score([page], {})["score"])
        self.assertEqual(sample_score([page], {})["check_coverage_percent"], 0)

    def test_review_signals_do_not_deduct_score(self):
        page = observed("<html><title>Title</title><h1>Heading</h1></html>")
        self.assertEqual(sample_score([page], {})["score"], 100)
        self.assertGreater(len(build_findings([page], {}, "example.com")), 0)

    def test_failed_priority_page_has_greater_business_weight(self):
        good = observed("<html><title>Good</title><h1>Good</h1></html>")
        bad = parse_page(response(url="https://example.com/service", status=500), "example.com")
        ordinary = sample_score([good, bad], {})
        priority = sample_score([good, bad], {"priority_urls": [bad["url"]]})
        self.assertLess(priority["score"], ordinary["score"])


class CrawlCoverageTests(unittest.TestCase):
    def test_slash_and_scheme_variants_remain_distinct(self):
        self.assertEqual(normalize_url("http://example.com/path/", "example.com"), "http://example.com/path/")
        self.assertNotEqual(normalize_url("https://example.com/path", "example.com"), normalize_url("https://example.com/path/", "example.com"))

    def test_sitemap_xml_decodes_entities_and_rejects_html(self):
        self.assertEqual(parse_sitemap('<urlset><url><loc>https://example.com/?a=1&amp;b=2</loc></url></urlset>'), ["https://example.com/?a=1&b=2"])
        self.assertEqual(parse_sitemap("<html><loc>https://example.com/</loc></html>"), [])

    def test_page_limit_discloses_partial_coverage(self):
        def fake_fetch(url, **kwargs):
            if url.endswith("robots.txt"):
                return response(url, text="User-agent: *\nAllow: /\n")
            return response(url, text='<html><title>Example</title><a href="/two">Two</a></html>')
        with patch("audit_runner.fetch", side_effect=fake_fetch), patch("audit_runner.collect_sitemap_urls", return_value=(404, [])):
            pages, robots, _ = crawl({"website_url": "https://example.com/", "max_crawl_pages": 1, "crawl_delay_seconds": 0})
        self.assertEqual(len(pages), 1)
        self.assertTrue(robots["coverage"]["partial"])
        self.assertEqual(robots["coverage"]["stopping_reason"], "page_limit")
        self.assertEqual(robots["coverage"]["unattempted_urls"], ["https://example.com/two"])

    def test_robots_failure_does_not_silently_crawl(self):
        with patch("audit_runner.fetch", return_value=response(status=503)), patch("audit_runner.collect_sitemap_urls", return_value=(404, [])):
            pages, robots, _ = crawl({"website_url": "https://example.com/"})
        self.assertEqual(pages, [])
        self.assertEqual(robots["coverage"]["stopping_reason"], "robots_unavailable")

    def test_no_overwrite_of_prior_audit(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root/"audit-data.json").write_text("original", encoding="utf-8")
            with self.assertRaises(ValueError):
                run({"website_url": "https://example.com"}, root, build_report=False)
            self.assertEqual((root/"audit-data.json").read_text(), "original")

    def test_empty_serp_does_not_establish_absent_rank(self):
        baseline, _ = normalize_serps([{"query": "example", "organicResults": []}], "example.com", {"country_code": "us", "language_code": "en", "device": "mobile"})
        self.assertEqual(baseline[0]["evidence_label"], "Not verified")
        self.assertEqual(baseline[0]["sample_depth"], 0)

    def test_serp_uses_actual_sample_depth_and_localization(self):
        baseline, _ = normalize_serps([{"query": "example", "organicResults": [{"url": "https://competitor.com"}]}], "example.com", {"country_code": "gb", "language_code": "en", "device": "mobile"})
        self.assertEqual(baseline[0]["visibility"], "Not visible within sampled top 1")
        self.assertEqual(baseline[0]["country"], "gb")


class HistoryReliabilityTests(unittest.TestCase):
    def test_noindex_page_does_not_prove_heading_issue_resolved(self):
        page = parse_page(response(text='<html><meta name="robots" content="noindex"></html>'), "example.com")
        finding={"id": "h1", "check_id": "missing-h1", "affected_urls": [page["url"]]}
        result=compare({'findings': [finding]}, {'findings': [], 'pages': [page]})
        self.assertEqual(result['changes'][0]['status'], 'Not rechecked')

    def test_absence_in_partial_crawl_is_not_resolution(self):
        finding = {"id": "h1", "check_id": "missing-h1", "affected_urls": ["https://example.com/a"]}
        result = compare({"findings": [finding]}, {"findings": [], "pages": []})
        self.assertEqual(result["changes"][0]["status"], "Not rechecked")

    def test_same_check_on_all_urls_proves_resolution(self):
        finding = {"id": "h1", "check_id": "missing-h1", "affected_urls": ["https://example.com/a"]}
        result = compare({"findings": [finding]}, {"findings": [], "pages": [{"url": "https://example.com/a", "checks_performed": ["missing-h1"]}]})
        self.assertEqual(result["changes"][0]["status"], "Resolved")

    def test_scope_mismatch_is_not_comparable(self):
        result = compare({"business_context": {"country_code": "us"}, "findings": [{"id": "x"}]}, {"business_context": {"country_code": "gb"}, "findings": []})
        self.assertEqual(result["changes"][0]["status"], "Not comparable")


class FirstPartyTests(unittest.TestCase):
    def test_unrelated_property_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            source=Path(directory)/'export.csv'
            source.write_text('query,clicks,impressions,ctr,position\na,1,10,0.1,2\n', encoding='utf-8')
            result=validate_export(source, {**self.metadata(), 'website_url': 'https://another.com'}, 'https://another.com')
            self.assertFalse(result['passed'])

    def test_malformed_metadata_is_unverified_not_guessed(self):
        result=self.quality('query,clicks,impressions,ctr,position\na,1,10,0.1,2\n', {**self.metadata(), 'dimensions': [{}], 'retrieved_at': 123})
        self.assertFalse(result['passed'])

    def metadata(self):
        return {"source": "gsc", "provenance": "owner_export", "property": "sc-domain:example.com",
                "retrieved_at": "2026-10-05T09:00:00Z", "start_date": "2026-09-01", "end_date": "2026-09-30",
                "timezone": "America/Los_Angeles", "dimensions": ["query"], "filters": {}}

    def quality(self, content, metadata=None):
        with tempfile.TemporaryDirectory() as directory:
            path=Path(directory)/"gsc.csv"
            path.write_text(content, encoding="utf-8")
            return validate_export(path, metadata or self.metadata())

    def test_valid_export_uses_weighted_ctr(self):
        result = self.quality("query,clicks,impressions,ctr,position\na,10,100,0.1,2\nb,1,100,0.01,3\n")
        self.assertTrue(result["passed"], result)
        self.assertEqual(result["summary"]["ctr"], 0.055)
        self.assertNotIn("position", result["summary"])

    def test_missing_metadata_does_not_verify_file(self):
        result = self.quality("query,clicks,impressions,ctr,position\na,1,10,0.1,2\n", {"source": "gsc"})
        self.assertFalse(result["passed"])
        self.assertEqual(result["summary"], {})

    def test_duplicate_rows_and_invalid_metrics_are_rejected(self):
        for content in ["a,1,10,0.1,2\na,1,10,0.1,2", "a,nan,10,0.1,2", "a,1,10,10,2"]:
            with self.subTest(content=content):
                result = self.quality("query,clicks,impressions,ctr,position\n"+content+"\n")
                self.assertFalse(result["passed"])

    def test_unequal_windows_or_properties_are_not_comparable(self):
        old = self.metadata()
        new = {**old, "property": "other", "start_date": "2026-10-01", "end_date": "2026-10-31"}
        reasons = comparison_compatibility(old, new)
        self.assertIn("Different property", reasons)
        self.assertIn("Unequal measurement window lengths", reasons)

    def test_ga4_events_need_definition(self):
        metadata={**self.metadata(), "source": "ga4", "dimensions": ["page"]}
        result=self.quality("page,sessions,key_events\n/,3,5\n", metadata)
        self.assertFalse(result["passed"])
        result=self.quality("page,sessions,key_events\n/,3,5\n", {**metadata, "key_event_definition": "Submitted form"})
        self.assertTrue(result["passed"], result)

    def test_gsc_cannot_authorize_conversions(self):
        with self.assertRaises(ValueError):
            normalize_record({"source_name": "GSC", "source_type": "search_console", "provenance": "owner_export", "label": "First-party verified", "metric": "conversions", "value": 1})


class ReproducibilityTests(unittest.TestCase):
    def test_artifact_redacts_credentials_but_preserves_filter_queries(self):
        result = sanitize_artifact({"url": "https://name:SECRET@example.com/?category=tools&token=SECRET", "token": "SECRET"})
        self.assertNotIn("SECRET", json.dumps(result))
        self.assertIn("category=tools", result["url"])

    def test_secrets_and_url_credentials_are_not_persisted(self):
        config={"api_key": "SECRET", "nested": {"token": "SECRET"}, "website_url": "https://name:SECRET@example.com/?token=SECRET"}
        self.assertNotIn("SECRET", json.dumps(safe_config(config)))

    def test_checksum_manifest_does_not_collect_private_files(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            (root/"audit-data.json").write_text("{}", encoding="utf-8")
            (root/"private.csv").write_text("private", encoding="utf-8")
            result=write_reproducibility(root, {}, "2026-10-05T09:00:00Z")
            names={a["path"] for a in result["artifacts"]}
            self.assertNotIn("private.csv", names)
            record=next(a for a in result["artifacts"] if a["path"] == "audit-data.json")
            self.assertEqual(record["sha256"], hashlib.sha256(b"{}").hexdigest())


class OutcomeTests(unittest.TestCase):
    def row(self):
        return {"implementation_date": "2026-09-08", "validation_result": "passed", "validation_evidence": "qa.json",
                "source": "gsc", "source_label": "First-party verified", "property": "example.com", "timezone": "UTC", "segment": "desktop", "filters": "{}",
                "baseline_start": "2026-09-01", "baseline_end": "2026-09-07", "baseline_value": "0",
                "followup_start": "2026-09-09", "followup_end": "2026-09-15", "followup_value": "10",
                "unit": "clicks", "measurement_evidence": "exports.json", "confounders": "Reviewed; no known changes"}

    def test_zero_baseline_has_no_percentage_or_causal_claim(self):
        result=assess_outcome(self.row())
        self.assertEqual(result["absolute_change"], 10)
        self.assertIsNone(result["percent_change"])
        self.assertEqual(result["causal_claim"], "Not established")
        self.assertEqual(result["implementation_status"], "Fix verified")

    def test_failed_validation_is_separate_from_observed_change(self):
        result=assess_outcome({**self.row(), "validation_result": "failed"})
        self.assertEqual(result["implementation_status"], "Not verified")
        self.assertEqual(result["measurement_status"], "Observed change")

    def test_invalid_window_rejects_growth_claim(self):
        result=assess_outcome({**self.row(), "followup_start": "2026-09-07"})
        self.assertEqual(result["measurement_status"], "Not comparable")
        self.assertIsNone(result["absolute_change"])


class PerformanceReliabilityTests(unittest.TestCase):
    def test_empty_lighthouse_is_not_verified(self):
        with self.assertRaises(ValueError):
            summarize_lighthouse({}, 'PageSpeed Insights', 'mobile')

    def test_runtime_error_is_not_verified(self):
        with self.assertRaises(ValueError):
            summarize_lighthouse({'runtimeError': {'code': 'NO_FCP'}, 'categories': {'performance': {'score': 0.9}}}, 'Lighthouse', 'mobile')

    def test_http_success_with_empty_measurements_remains_unverified(self):
        from unittest.mock import Mock
        response=Mock(status_code=200)
        response.json.return_value={}
        with patch('lighthouse_runner.requests.get', return_value=response):
            result, note=run_pagespeed('https://example.com', 'mobile')
        self.assertIsNone(result)
        self.assertTrue(note)


class PipelineIntegrationTests(unittest.TestCase):
    def test_real_http_crawl_import_and_pdf_pipeline(self):
        class Handler(BaseHTTPRequestHandler):
            def do_GET(self):
                base = f"http://127.0.0.1:{self.server.server_port}"
                pages = {
                    "/robots.txt": (200, "text/plain", "User-agent: *\nDisallow: /blocked\n"),
                    "/sitemap.xml": (200, "application/xml", f'<sitemapindex><sitemap><loc>{base}/page-map</loc></sitemap></sitemapindex>'),
                    "/page-map": (200, "application/xml", '<urlset>' + ''.join(f'<url><loc>{base}{path}</loc></url>' for path in ['/', '/service', '/shell', '/broken', '/blocked']) + '</urlset>'),
                    "/": (200, "text/html", '<html><head><title>Local fixture</title></head><body><h1>Local fixture</h1><a href="/privacy">Privacy</a></body></html>'),
                    "/service": (200, "text/html", '<html><head><title>Service</title><meta name="robots" content="noindex"></head><body><h1>Service</h1></body></html>'),
                    "/shell": (200, "text/html", '<html><title>App</title><body><div id="root"></div></body></html>'),
                    "/broken": (503, "text/html", '<html><h1>Temporarily unavailable</h1></html>'),
                }
                status, content_type, text = pages.get(self.path, (404, 'text/plain', 'Not found'))
                self.send_response(status)
                self.send_header('Content-Type', content_type)
                self.end_headers()
                self.wfile.write(text.encode('utf-8'))

            def log_message(self, *args):
                pass

        server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            with tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                source = root/'gsc.csv'
                metadata_path=root/'metadata.json'
                source.write_text('query,clicks,impressions,ctr,position\nservice,10,100,0.1,2\n', encoding='utf-8')
                base=f'http://127.0.0.1:{server.server_port}'
                metadata_path.write_text(json.dumps({**FirstPartyTests().metadata(), 'property': base+'/', 'website_url': base+'/'}), encoding='utf-8')
                output=root/'audit'
                result=run({'website_url': base+'/', 'allow_private_network': True, 'crawl_delay_seconds': 0,
                            'priority_urls': [base+'/service'], 'exclude_paths': ['/privacy'],
                            'page_templates': {base+'/service': 'Service'},
                            'apify': {'enabled': False}, 'performance': {'enabled': False}, 'clarity': {'enabled': False},
                            'first_party_imports': [{'input_path': str(source), 'metadata_path': str(metadata_path)}]}, output)
                audit=json.loads((output/'audit-data.json').read_text(encoding='utf-8'))
                self.assertEqual(result['pages'], 4)
                self.assertTrue(audit['coverage']['partial'])
                self.assertEqual(audit['coverage']['blocked_urls'], [base+'/blocked'])
                self.assertEqual(audit['coverage']['excluded_urls'], [base+'/privacy'])
                self.assertEqual(audit['coverage']['template_counts']['Service'], 1)
                self.assertTrue(audit['sitemap']['complete'])
                self.assertIn('noindex-review', {f['check_id'] for f in audit['findings']})
                self.assertEqual(audit['first_party_quality'][0]['summary']['clicks'], 10)
                self.assertTrue(json.loads((output/'beyond-seo-audit.qa.json').read_text())['passed'])
                self.assertIsNone(json.loads((output/'report-input.json').read_text())['overall_score'])
                validate_findings(audit['findings'], audit['evidence_records'])
                manifest=json.loads((output/'reproducibility-manifest.json').read_text())
                for artifact in manifest['artifacts']:
                    self.assertEqual(hashlib.sha256((output/artifact['path']).read_bytes()).hexdigest(), artifact['sha256'])
        finally:
            server.shutdown()
            server.server_close()
            thread.join(timeout=5)


if __name__ == "__main__":
    unittest.main()
