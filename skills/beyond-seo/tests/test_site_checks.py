import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from site_checks import analyze


class SiteChecksTests(unittest.TestCase):
    def test_relative_links_fragments_and_unique_referrers(self):
        result = analyze([{'url': 'https://example.com/', 'links': ['/product#details', '/product']}, {'url': 'https://example.com/product', 'priority': True}])
        self.assertEqual(result['incoming_pages']['https://example.com/product'], 1)
        self.assertEqual(result['review_candidates'], [])

    def test_priority_gap_is_review_not_orphan_claim(self):
        result = analyze([{'url': 'https://example.com/product?a=1', 'priority': True}])
        self.assertIn('Orphan status is Not verified', result['review_candidates'][0]['action'])

    def test_render_provenance_required(self):
        page = {'url': 'https://example.com/', 'fetched_text': '', 'rendered_text': 'Product details'}
        self.assertEqual(analyze([page])['review_candidates'], [])
        page.update(rendered_artifact='dom.html', rendered_at='2026-10-06T12:00:00+05:00')
        self.assertEqual(analyze([page])['review_candidates'][0]['check'], 'rendered-content-difference')

    def test_jsonld_parse_does_not_grant_eligibility(self):
        result = analyze([{'url': 'https://example.com/', 'structured_data': ['{"@type":"Product"}', '{broken']}])
        self.assertEqual(len(result['review_candidates']), 1)
        self.assertIn('eligibility remains Not verified', result['review_candidates'][0]['action'])
