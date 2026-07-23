from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))

from audit_compare import compare  # noqa: E402
from competitor_classifier import classify  # noqa: E402
from evidence_ledger import EvidenceLedger, normalize_record  # noqa: E402
from pdf_qa import inspect_pdf  # noqa: E402
from report_builder import build_pdf, sample_payload  # noqa: E402


class EvidenceTests(unittest.TestCase):
    def test_rejects_unverified_proprietary_metric(self):
        with self.assertRaises(ValueError):
            normalize_record({"source_name": "Guess", "metric": "keyword_volume", "value": 500, "label": "Directional"})

    def test_writes_json_and_csv(self):
        ledger = EvidenceLedger()
        ledger.add(source_type="crawl", source_name="Native crawl", scope="1 URL", label="Confirmed")
        with tempfile.TemporaryDirectory() as directory:
            json_path = Path(directory) / "ledger.json"
            csv_path = Path(directory) / "ledger.csv"
            ledger.write(json_path, csv_path)
            self.assertEqual(len(json.loads(json_path.read_text(encoding="utf-8"))), 1)
            self.assertTrue(csv_path.exists())


class CompetitorTests(unittest.TestCase):
    def test_excludes_platforms_and_keeps_agency(self):
        result = classify([
            {"domain": "reddit.com", "ranking_keyword": "crm development", "observed_position": 1},
            {"domain": "smallagency.com", "ranking_keyword": "crm development", "service_focus": "crm development", "observed_position": 3},
        ], {"services": ["crm development"]})
        self.assertEqual(result["excluded"][0]["domain"], "reddit.com")
        self.assertEqual(result["comparable"][0]["domain"], "smallagency.com")


class ComparisonTests(unittest.TestCase):
    def test_change_states(self):
        fixtures = ROOT / "tests" / "fixtures"
        previous = json.loads((fixtures / "previous-audit.json").read_text(encoding="utf-8"))
        current = json.loads((fixtures / "current-audit.json").read_text(encoding="utf-8"))
        result = compare(previous, current)
        self.assertEqual(result["summary"]["New"], 1)
        self.assertEqual(result["summary"]["Improved"], 1)
        self.assertEqual(result["summary"]["Resolved"], 1)


class ReportTests(unittest.TestCase):
    def test_sample_pdf_passes_structural_qa(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "sample.pdf"
            build_pdf(sample_payload(), output)
            result = inspect_pdf(output)
            self.assertTrue(result["passed"], result)


if __name__ == "__main__":
    unittest.main()
