from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch
from urllib.parse import urlparse

import requests

from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))

from audit_compare import compare  # noqa: E402
from audit_runner import fetch, run, run_apify_serp  # noqa: E402
from clarity_export import load_saved_export, normalize_export  # noqa: E402
from competitor_classifier import classify, qualify  # noqa: E402
from evidence_ledger import EvidenceLedger, normalize_record  # noqa: E402
from lighthouse_runner import collect as collect_lighthouse  # noqa: E402
from pdf_qa import inspect_pdf  # noqa: E402
from report_builder import build_and_validate_pdf, build_pdf, main as report_main, sample_payload  # noqa: E402
from source_classifier import detect_source, evidence_level, metric_confidence  # noqa: E402


class EvidenceTests(unittest.TestCase):
    def test_rejects_unverified_proprietary_metric(self):
        with self.assertRaises(ValueError):
            normalize_record({"source_name": "Guess", "metric": "keyword_volume", "value": 500, "label": "Directional"})

    def test_writes_json_and_csv(self):
        ledger = EvidenceLedger()
        ledger.add(source_type="crawl", source_name="Native crawl", provenance="direct_observation", scope="1 URL", label="Confirmed")
        with tempfile.TemporaryDirectory() as directory:
            json_path = Path(directory) / "ledger.json"
            csv_path = Path(directory) / "ledger.csv"
            ledger.write(json_path, csv_path)
            self.assertEqual(len(json.loads(json_path.read_text(encoding="utf-8"))), 1)
            self.assertTrue(csv_path.exists())

    def test_verified_labels_require_provenance(self):
        with self.assertRaises(ValueError):
            normalize_record({"source_name": "gsc.csv", "metric": "conversions", "value": 1, "label": "First-party verified"})
        record = normalize_record({
            "source_name": "GSC export",
            "source_type": "first_party",
            "provenance": "owner_export",
            "metric": "conversions",
            "value": 1,
            "label": "First-party verified",
        })
        self.assertEqual(record["provenance"], "owner_export")

    def test_confirmed_label_cannot_authorize_keyword_volume(self):
        with self.assertRaises(ValueError):
            normalize_record({
                "source_name": "Manual guess",
                "provenance": "direct_observation",
                "metric": "keyword_volume",
                "value": 999,
                "label": "Confirmed",
            })

    def test_metric_alias_cannot_bypass_ledger_policy(self):
        with self.assertRaises(ValueError):
            normalize_record({
                "source_name": "Guess",
                "metric": "keyword-volume",
                "value": 999,
                "label": "Directional",
            })
        for alias in ("domain authority score", "AI visibility score"):
            with self.subTest(alias=alias), self.assertRaises(ValueError):
                normalize_record({
                    "source_name": "Guess",
                    "metric": alias,
                    "value": 88,
                    "label": "Directional",
                })
        with self.assertRaises(ValueError):
            normalize_record({
                "source_name": "Guess",
                "metric": "monthly keyword-volume estimate",
                "value": 999,
                "label": "Directional",
            })

    def test_metric_source_family_is_required(self):
        with self.assertRaises(ValueError):
            normalize_record({
                "source_name": "Uploaded file",
                "source_type": "first_party",
                "provenance": "owner_export",
                "metric": "keyword_volume",
                "value": 100,
                "label": "Paid-tool verified",
            })
        record = normalize_record({
            "source_name": "Paid SEO export",
            "source_type": "paid_tool",
            "provenance": "owner_export",
            "metric": "keyword_volume",
            "value": 100,
            "label": "Paid-tool verified",
        })
        self.assertEqual(record["value"], 100)


class CompetitorTests(unittest.TestCase):
    def test_excludes_platforms_and_keeps_agency(self):
        result = classify([
            {"domain": "reddit.com", "ranking_keyword": "crm development", "observed_position": 1},
            {"domain": "smallagency.com", "ranking_keyword": "crm development", "service_focus": "crm development", "observed_position": 3},
        ], {"services": ["crm development"]})
        self.assertEqual(result["excluded"][0]["domain"], "reddit.com")
        self.assertEqual(result["comparable"][0]["domain"], "smallagency.com")

    def test_unknown_business_model_gets_no_bonus(self):
        row = qualify({"domain": "random.example", "observed_position": 1}, {"services": []})
        self.assertEqual(row["qualification_score"], 30)
        self.assertEqual(row["classification"], "Content competitor")
        self.assertIn("not verified", row["qualification_reason"])

    def test_string_false_business_model_gets_no_bonus(self):
        row = qualify({"domain": "random.example", "observed_position": 1, "business_model_match": "false"}, {"services": []})
        self.assertEqual(row["qualification_score"], 30)


class ComparisonTests(unittest.TestCase):
    def test_change_states(self):
        fixtures = ROOT / "tests" / "fixtures"
        previous = json.loads((fixtures / "previous-audit.json").read_text(encoding="utf-8"))
        current = json.loads((fixtures / "current-audit.json").read_text(encoding="utf-8"))
        result = compare(previous, current)
        self.assertEqual(result["summary"]["New"], 1)
        self.assertEqual(result["summary"]["Improved"], 1)
        self.assertEqual(result["summary"]["Resolved"], 1)

    def test_worsening_severity_is_not_improvement(self):
        result = compare(
            {"findings": [{"id": "x", "severity": "Medium", "evidence": ["a"]}]},
            {"findings": [{"id": "x", "severity": "High", "evidence": ["a"]}]},
        )
        self.assertEqual(result["summary"]["Worsened"], 1)
        self.assertEqual(result["changes"][0]["status"], "Worsened")

    def test_unknown_severity_change_is_changed(self):
        result = compare(
            {"findings": [{"id": "x", "severity": "Needs review", "evidence": []}]},
            {"findings": [{"id": "x", "severity": "Urgent", "evidence": []}]},
        )
        self.assertEqual(result["changes"][0]["status"], "Changed")


class ClarityTests(unittest.TestCase):
    def test_normalizes_verified_behavior_and_flags_friction(self):
        raw = [
            {
                "metricName": "Rage Click Count",
                "information": [{
                    "URL": "/contact?email=private@example.com",
                    "rageClickCount": "2",
                    "customEmail": "private@example.com",
                }],
            }
        ]
        export = normalize_export(raw, 3, ["URL"])
        self.assertEqual(export["evidence_label"], "First-party verified")
        self.assertEqual(export["report_section"]["metrics"][0]["segment"], "URL: /contact")
        self.assertNotIn("customEmail", json.dumps(export))
        self.assertEqual(export["report_section"]["signals"][0]["signal"], "Rage Click Count")

    def test_saved_json_is_revalidated_and_report_section_rebuilt(self):
        saved = {
            "retrieved_at": "2026-10-04T09:00:00+00:00",
            "num_days": 3,
            "dimensions": ["URL"],
            "data": [{
                "metricName": "Traffic",
                "information": [{
                    "URL": "/private?email=x@example.com",
                    "userId": 12345,
                    "unrecognizedReference": 67890,
                    "totalSessionCount": "4",
                }],
            }],
            "report_section": {"metrics": [{"observed": "do-not-trust"}]},
        }
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "clarity.json"
            path.write_text(json.dumps(saved), encoding="utf-8")
            export = load_saved_export(path, 3, ["URL"])
        rendered = json.dumps(export["report_section"])
        stored = json.dumps(export["data"])
        self.assertNotIn("do-not-trust", rendered)
        self.assertNotIn("userId", stored)
        self.assertNotIn("12345", stored)
        self.assertNotIn("unrecognizedReference", stored)
        self.assertNotIn("67890", stored)
        self.assertNotIn("email=x", rendered)

    def test_url_dimensions_strip_credentials_and_path_identifiers(self):
        raw = [{
            "metricName": "Traffic",
            "information": [{
                "URL": "https://name:secret@example.com/users/alice@example.com/12345?token=private",
                "totalSessionCount": "4",
                "unknownScore": 99,
            }],
        }]
        export = normalize_export(raw, 3, ["URL"])
        persisted = json.dumps(export)
        self.assertNotIn("name:secret", persisted)
        self.assertNotIn("alice@example.com", persisted)
        self.assertNotIn("12345", persisted)
        self.assertNotIn("token=private", persisted)
        self.assertNotIn("unknownScore", persisted)
        self.assertIn("totalSessionCount", persisted)

    def test_saved_json_requires_retrieval_time(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "clarity.json"
            path.write_text(json.dumps({"num_days": 3, "dimensions": ["URL"], "data": []}), encoding="utf-8")
            with self.assertRaises(ValueError):
                load_saved_export(path, 3, ["URL"])

    def test_saved_csv_is_supported(self):
        content = (
            "retrieved_at_utc,window_days,dimension,url,metric_name,observed_value,evidence_label,interpretation,action\n"
            "2026-10-04T09:00:00+00:00,3,URL,/contact?email=x@example.com,Rage Click Count,2,First-party verified,,Investigate\n"
        )
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "clarity.csv"
            path.write_text(content, encoding="utf-8")
            export = load_saved_export(path, 3, ["URL"])
        self.assertEqual(export["provenance"], "owner_export")
        self.assertEqual(export["report_section"]["metrics"][0]["segment"], "URL: /contact")

    def test_saved_csv_uses_declared_dimension(self):
        content = (
            "retrieved_at_utc,window_days,dimension,device,metric_name,observed_value\n"
            "2026-10-04T10:00:00Z,3,Device,Mobile,Dead Click Count,2\n"
        )
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "clarity.csv"
            path.write_text(content, encoding="utf-8")
            export = load_saved_export(path, 3, ["URL"])
        self.assertEqual(export["dimensions"], ["Device"])
        self.assertEqual(export["data"][0]["information"][0]["Device"], "Mobile")

    def test_saved_json_rejects_non_list_data(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "clarity.json"
            path.write_text(json.dumps({
                "retrieved_at": "2026-10-04T10:00:00Z",
                "num_days": 3,
                "dimensions": ["URL"],
                "data": {"metricName": "Traffic"},
            }), encoding="utf-8")
            with self.assertRaises(ValueError):
                load_saved_export(path, 3, ["URL"])

    def test_source_classifier_recognizes_clarity(self):
        source = detect_source(
            Path("microsoft-clarity-live-insights.csv"),
            ["metric_name", "observed_value", "url"],
            None,
        )
        self.assertEqual(source, "microsoft clarity")
        self.assertEqual(evidence_level(source), "Not verified")
        self.assertEqual(evidence_level(source, "owner_export"), "First-party verified")

    def test_competitor_inference_uses_canonical_label(self):
        self.assertEqual(evidence_level("competitor page review", "live_observation"), "Inferred")

    def test_metric_confidence_enforces_source_family(self):
        row = {"volume": "100", "conversions": "3", "position": "4", "backlinks": "20"}
        first_party, _ = metric_confidence(row, "First-party verified")
        paid_tool, _ = metric_confidence(row, "Paid-tool verified")
        self.assertNotIn("volume", first_party)
        self.assertNotIn("backlinks", first_party)
        self.assertIn("conversions", first_party)
        self.assertIn("volume", paid_tool)
        self.assertIn("backlinks", paid_tool)
        self.assertNotIn("conversions", paid_tool)


class NetworkBoundaryTests(unittest.TestCase):
    def test_credentialed_url_is_rejected_before_request(self):
        with patch("audit_runner.open_pinned_response") as request:
            result = fetch("https://public.example@127.0.0.1/", allowed_hosts={"127.0.0.1"})
        self.assertIsNone(result["status"])
        self.assertIn("credentials", result["error"])
        request.assert_not_called()

    def test_redirect_to_private_address_is_rejected(self):
        connection = Mock()
        response = Mock()
        response.status = 302
        response.getheaders.return_value = [("location", "http://127.0.0.1/private")]
        response.close = Mock()
        with patch("audit_runner.socket.getaddrinfo", return_value=[(2, 1, 6, "", ("93.184.216.34", 443))]), patch(
            "audit_runner.open_pinned_response", return_value=(connection, response)
        ) as request:
            result = fetch("https://example.com/", allowed_hosts={"example.com", "127.0.0.1"})
        self.assertIsNone(result["status"])
        self.assertIn("Private or non-public", result["error"])
        self.assertEqual(request.call_count, 1)

    def test_oversized_response_is_rejected_before_body_read(self):
        connection = Mock()
        response = Mock(status=200)
        response.getheaders.return_value = [("content-length", "101")]
        with patch(
            "audit_runner.resolve_network_target",
            return_value=(urlparse("https://example.com/"), "93.184.216.34"),
        ), patch(
            "audit_runner.open_pinned_response", return_value=(connection, response)
        ):
            result = fetch("https://example.com/", allowed_hosts={"example.com"}, max_bytes=100)
        self.assertIn("exceeded", result["error"])
        response.read.assert_not_called()
        response.close.assert_called_once()
        connection.close.assert_called_once()

    def test_connection_uses_the_validated_ip(self):
        connection = Mock()
        response = Mock(status=200)
        response.getheaders.return_value = [("Content-Length", "0")]
        response.read.return_value = b""
        with patch(
            "audit_runner.socket.getaddrinfo",
            return_value=[(2, 1, 6, "", ("93.184.216.34", 443))],
        ), patch(
            "audit_runner.open_pinned_response",
            return_value=(connection, response),
        ) as opened:
            result = fetch("https://example.com/", allowed_hosts={"example.com"})
        self.assertEqual(result["status"], 200)
        self.assertEqual(opened.call_args.args[2], "93.184.216.34")


class ApifyTests(unittest.TestCase):
    def test_token_uses_authorization_header_not_query_string(self):
        response = Mock()
        response.status_code = 200
        response.raise_for_status.return_value = None
        response.json.return_value = []
        config = {"queries": ["test"], "apify": {"enabled": True}}
        with tempfile.TemporaryDirectory() as directory, patch.dict("os.environ", {"APIFY_API_TOKEN": "SECRET123"}), patch(
            "audit_runner.requests.post", return_value=response
        ) as post:
            run_apify_serp(config, Path(directory))
        kwargs = post.call_args.kwargs
        self.assertNotIn("token", kwargs["params"])
        self.assertEqual(kwargs["headers"]["Authorization"], "Bearer SECRET123")

    def test_apify_error_message_does_not_repeat_token(self):
        response = Mock()
        response.status_code = 401
        response.raise_for_status.side_effect = requests.HTTPError("401 unauthorized")
        config = {"queries": ["test"], "apify": {"enabled": True}}
        with tempfile.TemporaryDirectory() as directory, patch.dict("os.environ", {"APIFY_API_TOKEN": "SECRET123"}), patch(
            "audit_runner.requests.post", return_value=response
        ):
            with self.assertRaises(RuntimeError) as caught:
                run_apify_serp(config, Path(directory))
        self.assertNotIn("SECRET123", str(caught.exception))


class LighthouseBoundaryTests(unittest.TestCase):
    def test_local_browser_fallback_requires_explicit_opt_in(self):
        with patch("lighthouse_runner.run_pagespeed", return_value=(None, "Unavailable.")), patch(
            "lighthouse_runner.run_local"
        ) as local:
            result = collect_lighthouse("https://example.com", "mobile", Path("."))
        local.assert_not_called()
        self.assertEqual(result["status"], "not_verified")
        self.assertIn("disabled", result["note"])


class ReportTests(unittest.TestCase):
    def test_report_cli_always_invokes_pdf_validation(self):
        with tempfile.TemporaryDirectory() as directory, patch.object(
            sys, "argv", ["report_builder.py", "--output", str(Path(directory) / "report.pdf")]
        ), patch(
            "report_builder.load_payload", return_value={}
        ), patch(
            "report_builder.build_and_validate_pdf", return_value={"passed": True}
        ) as validate, patch(
            "report_builder.build_pdf"
        ) as unchecked:
            report_main()
        validate.assert_called_once()
        unchecked.assert_not_called()

    def test_sample_pdf_passes_structural_qa(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "sample.pdf"
            build_pdf(sample_payload(), output)
            result = inspect_pdf(output)
            self.assertTrue(result["passed"], result)
            text = "\n".join(page.extract_text() or "" for page in PdfReader(str(output)).pages)
            self.assertIn("Microsoft Clarity Behavior Insights", text)

    def test_validated_builder_writes_qa_artifact(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "sample.pdf"
            qa = Path(directory) / "sample.qa.json"
            result = build_and_validate_pdf(sample_payload(), output, qa)
            self.assertTrue(result["passed"])
            self.assertTrue(qa.exists())

    def test_audit_runner_invokes_pdf_validation(self):
        config = {
            "website_url": "https://example.com/",
            "performance": {"enabled": False},
            "clarity": {"enabled": False},
            "apify": {"enabled": False},
        }
        with tempfile.TemporaryDirectory() as directory, patch(
            "audit_runner.crawl", return_value=([], {"status": 200}, {"status": 200, "urls": []})
        ), patch("audit_runner.build_and_validate_pdf", return_value={"passed": True}) as validate:
            result = run(config, Path(directory), build_report=True)
        validate.assert_called_once()
        self.assertTrue(result["pdf_qa"].endswith("beyond-seo-audit.qa.json"))


if __name__ == "__main__":
    unittest.main()
