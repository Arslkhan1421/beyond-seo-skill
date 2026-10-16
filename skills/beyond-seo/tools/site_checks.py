"""Offline review candidates from saved crawl and browser observations."""
import argparse
import json
from datetime import datetime
from urllib.parse import urlsplit, urlunsplit, urljoin


def identity(url):
    parsed = urlsplit(url)
    return urlunsplit((parsed.scheme.lower(), parsed.netloc.lower(), parsed.path or '/', parsed.query, ''))


def analyze(pages):
    known = {identity(p['url']): p for p in pages}
    incoming = {url: set() for url in known}
    results = []
    for url, page in known.items():
        for link in page.get('links', []):
            target = identity(urljoin(url, link))
            if target in incoming and target != url:
                incoming[target].add(url)
        if page.get('rendered_artifact') and page.get('rendered_at'):
            try:
                timestamp = datetime.fromisoformat(page['rendered_at'].replace('Z', '+00:00'))
                if timestamp.tzinfo is None:
                    raise ValueError('timezone required')
                if 'fetched_text' in page and 'rendered_text' in page:
                    source = ' '.join(page['fetched_text'].split())
                    rendered = ' '.join(page['rendered_text'].split())
                    if source != rendered:
                        results.append({'url': url, 'check': 'rendered-content-difference', 'label': 'Inferred', 'action': 'Review saved source and rendered content; difference does not establish indexation.', 'artifact': page['rendered_artifact']})
            except (ValueError, TypeError):
                results.append({'url': url, 'check': 'rendered-provenance', 'label': 'Not verified', 'action': 'Supply a timezone-aware collection timestamp.'})
        for block in page.get('structured_data', []):
            try:
                parsed = json.loads(block) if isinstance(block, str) else block
                if not isinstance(parsed, (dict, list)):
                    raise ValueError('object or array required')
            except (ValueError, TypeError):
                results.append({'url': url, 'check': 'json-ld-parse', 'label': 'Confirmed', 'action': 'Saved JSON-LD cannot be parsed as an object or array. Review source; eligibility remains Not verified.'})
    for url, page in known.items():
        if page.get('priority') and not incoming[url]:
            results.append({'url': url, 'check': 'sample-inlinks', 'label': 'Inferred', 'action': 'No referring pages observed in this sample; review relevant internal links. Orphan status is Not verified.'})
    return {'sample_pages': len(known), 'incoming_pages': {u: len(v) for u, v in incoming.items()}, 'review_candidates': results, 'limitations': 'Saved observations only. No live fetch, Google indexation, structured-data eligibility or ranking impact verified.'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', required=True)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    from pathlib import Path
    output = analyze(json.loads(Path(args.input).read_text(encoding='utf-8')))
    Path(args.output).write_text(json.dumps(output, indent=2), encoding='utf-8')
