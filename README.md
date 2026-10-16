# Beyond SEO

Evidence-led SEO, AEO/GEO and website audit workflows for AI agents, with deterministic Python analysis and client-ready PDFs.

**Current release: [v1.5.0](https://github.com/Arslkhan1421/beyond-seo-skill/releases/tag/v1.5.0)**

## Install

Ask your agent:

```text
Install the Codex skill from https://github.com/Arslkhan1421/beyond-seo-skill/tree/main/skills/beyond-seo
```

For a version-pinned copy, download the ZIP from the [v1.5.0 release](https://github.com/Arslkhan1421/beyond-seo-skill/releases/tag/v1.5.0). The skill is in `skills/beyond-seo`. See the [team installation guide](TEAM_INSTALL_Beyond_SEO.md) for installation and upgrades.

## What v1.5.0 adds

- A 75-file skill with consolidated topic guides and a complete module index.
- Offline host-agent crawl and SERP snapshots feeding scoring, evidence ledgers and PDF reports.
- Backlink, URL and bounded XML/gzip sitemap import utilities.
- Compatible URL-level GSC, GA4 and Clarity synthesis.
- JSON-LD/visible-content parity, hreflang, query-overlap and internal-link reviews.
- Action-focused PDF reports with finding cards, bookmarks, links and outcome tracking.

## Run and validate

Python 3.11 or newer is recommended; CI runs on 3.11 and 3.14.

```text
python -m pip install -r skills/beyond-seo/requirements.txt
python skills/beyond-seo/tools/validate_skill.py
python -m unittest discover -s skills/beyond-seo/tests -v
```

Copy the [audit configuration](skills/beyond-seo/templates/audit-config-template.json) outside the installed skill and set the website, scope and limits.

```text
python skills/beyond-seo/tools/audit_runner.py --config audit-config.json --output-dir output/site-date
python skills/beyond-seo/tools/audit_runner.py --config audit-config.json --crawl-snapshot pages.json --serp-snapshot serp.json --output-dir output/site-offline
```

The offline crawl-snapshot mode disables network collectors. Read the [input contracts and CLI guide](skills/beyond-seo/core/v1.5-workflows.md) and [skill entrypoint](skills/beyond-seo/SKILL.md) before assembling snapshots or exports.

## Evidence and limitations

Every report separates observed facts, inferred impact and unavailable data. Crawling does not establish Google indexation, schema checks do not guarantee rich results, and funnel/query-overlap signals require contextual review. No automatic redirects, disavow actions or promised ranking/ROI gains.

API access is optional for offline analysis. Keep credentials in your own environment and client exports outside the distributable. Back up the existing skill and preserve local configuration before upgrading; old paths are mapped in the [migration registry](skills/beyond-seo/core/module-migration.json).

See [release notes](skills/beyond-seo/RELEASE_NOTES.md) for changes and compatibility. Existing package metadata describes usage as “Internal / client-use friendly”; this release does not introduce a new open-source license.
