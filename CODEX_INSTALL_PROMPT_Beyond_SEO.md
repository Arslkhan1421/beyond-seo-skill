# Codex Install Prompt - Beyond SEO Skill

Send this prompt to any teammate using Codex.

Use this repository: https://github.com/Arslkhan1421/beyond-seo-skill . For a fixed version, use the v1.5.0 release ZIP.

---

```text
Please install the Beyond SEO Codex skill from this GitHub repo:

https://github.com/Arslkhan1421/beyond-seo-skill

Steps:
1. Clone or download the repo into a temporary/local folder.
2. Back up any existing installation, preserve local-only configuration, and install the folder `skills/beyond-seo` into my Codex skills folder:
   - Windows: `%USERPROFILE%\.codex\skills\beyond-seo`
   - Mac/Linux: `~/.codex/skills/beyond-seo`
3. Do not copy any `.env` files, tokens, client exports, private data, or zip packages.
4. Install requirements.txt in the Python environment used to execute the skill. Verify that `SKILL.md` exists, then run tools/validate_skill.py and unittest discovery against the installed folder.
5. Tell me the installed version from `SKILL.md` (v1.5.0 for the version-pinned ZIP) and report any dependency or validation failures.

After that, I should be able to say:

Use the beyond-seo skill to audit this website.
```

## Optional Apify Setup Prompt

Each teammate should use their own Apify token. They can paste this separately:

```text
Help me set up my own `APIFY_API_TOKEN` environment variable for the Beyond SEO skill. Do not store the token in the skill files, reports, templates, manifests, or git repo.
```
