# Beyond SEO 1.3.0 Reusable Audit Runtime

This release adds:

- reusable configuration-driven crawl and SERP audit runner;
- machine-readable JSON/CSV evidence ledger with proprietary-metric safeguards;
- realistic competitor classifier that separates comparable, content, and excluded domains;
- dated audit comparison with New, Improved, Worsened, Changed, Unchanged, Resolved, and Reopened states;
- PageSpeed collection with an explicit opt-in local Lighthouse fallback for trusted targets and plain-language failures;
- automatic, fail-closed PDF builder QA for blank pages, broken bars, and replacement characters;
- optional Microsoft Clarity Data Export API integration with dated JSON/CSV validation, evidence-safe behavior metrics, privacy gates, source classification, import template, and PDF reporting;
- concise skill router, agent metadata, configuration template, fixtures, and automated tests.

Older release history follows.

# Beyond SEO 1.0.5 Visual Scorecards and Keyword Evidence Update

Added client-reporting improvements:

- Visual SEO scorecards using Markdown-safe progress bars, category scores, status labels, and priority heatmaps.
- Authentic keyword evidence rules for Google Search Console, Google Ads Keyword Planner, Google Trends, Semrush, Ahrefs, Moz, DataForSEO, SE Ranking, Sistrix, Bing Webmaster Tools, Apify SERP scrapes, and manual SERP samples.
- Competitor keyword verification rules separating confirmed competitor ranking keywords from inferred competitor targeted keywords.
- SEO data tool workflow covering Semrush, Ahrefs, DataForSEO, Moz, Majestic, SE Ranking, Sistrix, Screaming Frog, Sitebulb, BrightLocal, Whitespark, Local Falcon, and AI visibility sources.
- Website improvement text blocks for the top recommendations, including current problem, why it matters, recommended change, example improvement text, priority, and evidence.

---

# Beyond SEO 1.0.4 2026 SEO Intelligence Update

Updated the skill for current SEO and AI-search behavior:

- Added a current SEO intelligence layer that prioritizes official Google sources for ranking updates, spam policies, Search Console changes, and AI-search guidance.
- Added handling for Search Console Search Generative AI performance reports, including AI Overviews, AI Mode, and Discover generative AI visibility.
- Added branded vs non-branded query segmentation guidance for Search Console analysis.
- Clarified that AEO/GEO for Google Search is still SEO: crawlable, indexed, useful, unique, expert-led, source-worthy content.
- Added mythbusting rules so the skill does not recommend `llms.txt`, special AI-only schema, artificial chunking, mass query-variant pages, or inauthentic mentions as Google AI visibility requirements.
- Added spam-risk awareness for back button hijacking, site reputation abuse, scaled content abuse, expired domain abuse, and link spam.
- Expanded data-quality rules to prevent invented AI Overview, AI Mode, Discover AI, and branded/non-branded query data.

---

# Beyond SEO 1.0.3 AI-Friendly SEO Expansion

Added dedicated AI-friendly SEO modules:

- AEO content writing persona
- GEO AI citation optimization
- Entity SEO knowledge graph system
- Reputation SEO proof stack
- Third-party authority article system
- Conversation SEO framework
- AI-friendly SEO master workflow
- Apify AI-friendly SEO workflows
- AI-friendly SEO report template

The skill now knows what to do when a user asks for AI-friendly SEO and can produce a combined SEO + AEO + GEO + Entity + Reputation + Conversation SEO report.

---

# Beyond SEO 1.0.2 Apify-First Universal Release

This release incorporates the Codex-installed Apify updates and changes the skill behavior from "ask for many APIs" to "Apify-first".

## Changes

- Added Codex-updated `integrations/apify.md`.
- Added `integrations/apify-actor-shortlist.md`.
- Added `integrations/apify-first-operating-policy.md`.
- Rewrote onboarding so the skill asks only for `APIFY_API_TOKEN` by default.
- Updated setup, install, capability detection, audit modes, README, and SKILL.md to prefer Apify first.
- Added `apify-client` to requirements.
- Added `tools/apify_start_check.py`.
- Confirmed no API token is stored in the package.

---

# Beyond SEO 1.0.1 Universal Release

This release polishes the complete Beyond SEO 1.0 structure for broader AI-agent compatibility.

## Fixes Applied

- Added Codex-compatible YAML frontmatter to `SKILL.md`.
- Synced version metadata to `1.0.1`.
- Cleaned README language so completed files are not called upcoming.
- Added `requirements.txt` for optional Python tools.
- Added `INSTALL_FOR_AGENTS.md` for Codex, Claude, OpenClaw, Cursor, and local agents.
- Added `PLAYBOOK_DEPTH.md` to clarify deep modules vs lightweight specialist playbooks.
- Regenerated `MANIFEST.json` with clean file counts.
- Kept the full Beyond SEO structure intact.

## Compatibility

- Codex
- Claude Projects
- OpenClaw
- Cursor
- MCP-enabled agents
- Custom file-based AI agents


---

# Beyond SEO 1.0 Complete Structure Release

This package includes the full expanded Beyond SEO structure requested by the user.

It contains:
- Core brain and operating rules
- Apify and native scraping integrations
- Technical, on-page, content, schema, internal linking, speed, and conversion audit workflows
- Keyword discovery, clustering, intent, money keyword, local keyword, and page mapping workflows
- Competitor crawl, SERP gap, content gap, authority gap, and service-page gap workflows
- AEO/GEO and AI overview opportunity workflows
- Local SEO workflows
- Full backlink system with free/paid backlink source library and backlink database
- Strategy files for 30/60/90-day plans and query/visitor growth models
- Industry playbooks
- Reporting files
- Templates
- Examples
- Tools

Use SKILL.md as the master instruction file.
