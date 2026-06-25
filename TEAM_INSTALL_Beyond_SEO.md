# Beyond SEO Skill - Team Install Guide

This repository contains the Beyond SEO Codex skill at:

```text
skills/beyond-seo
```

## Install For Codex

Copy the `skills/beyond-seo` folder into your local Codex skills directory.

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
Beyond SEO 1.0.4 - 2026 SEO Intelligence and AI-search reporting update
```
