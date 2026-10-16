# Beyond SEO Skill - Team Install Guide

Current release: [v1.5.1](https://github.com/Arslkhan1421/beyond-seo-skill/releases/tag/v1.5.1). Download its ZIP for a fixed version, or use the [one-line install prompt](ONE_LINE_INSTALL_Beyond_SEO.md) for main.

This repository contains the Beyond SEO Codex skill at:

```text
skills/beyond-seo
```

## Install For Codex

For a fresh installation, copy the `skills/beyond-seo` folder into your local Codex skills directory. The commands below assume no existing `beyond-seo` directory. For an upgrade, follow the upgrade procedure below instead of overlaying old files.

Windows:

```powershell
New-Item -ItemType Directory -Force "$env:USERPROFILE\.codex\skills" | Out-Null
Copy-Item -Recurse -Force ".\skills\beyond-seo" "$env:USERPROFILE\.codex\skills\beyond-seo"
```

Mac/Linux:

```bash
mkdir -p ~/.codex/skills
cp -R ./skills/beyond-seo ~/.codex/skills/beyond-seo
```

## Verify installation

Install dependencies and validate from the installed skill directory:

```text
python -m pip install -r requirements.txt
python tools/validate_skill.py
python -m unittest discover -s tests -v
```

Use Python 3.11 or newer. The current skill has 76 packaged files and 108 tests. Review the release checksum before installation.

## Upgrade an existing installation

1. Back up the entire existing skill outside its installation directory.
2. Preserve local-only configuration and credentials privately; never upload them with the release.
3. Replace the managed skill files with the new release. Remove obsolete managed paths listed in the previous manifest only after backup; a simple overlay leaves the consolidated v1.4 modules behind. Use `core/module-migration.json` to locate replacement guides.
4. Restore needed local configuration without placing private client exports inside the distributable. Never overwrite credentials with package examples.
5. Install the updated requirements and run the package validator and tests. Keep the backup until validation succeeds.

## Use The Skill

In Codex, ask:

```text
Use the beyond-seo skill to audit this website: https://example.com
```

Or:

```text
Use beyond-seo to create an AI-friendly SEO, AEO, GEO, local SEO, and backlink growth plan.
```

## Optional Apify Token

For stronger crawls, SERP samples, Maps/local checks, and competitor research, each teammate should use their own Apify token.

Set it as an environment variable:

```text
APIFY_API_TOKEN=your_token_here
```

Do not commit tokens, `.env` files, private exports, or client data to this repo.

## Version

Current packaged skill version:

```text
Beyond SEO 1.5.1 - Portable evidence workflows and action-focused reporting
```
