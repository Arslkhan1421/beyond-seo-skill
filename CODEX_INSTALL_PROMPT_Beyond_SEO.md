# Codex Install Prompt - Beyond SEO Skill

Send this prompt to any teammate using Codex.

Replace:

```text
PASTE_GITHUB_REPO_URL_HERE
```

with the GitHub repository URL that contains this project.

---

```text
Please install the Beyond SEO Codex skill from this GitHub repo:

PASTE_GITHUB_REPO_URL_HERE

Steps:
1. Clone or download the repo into a temporary/local folder.
2. Copy the folder `skills/beyond-seo` into my Codex skills folder:
   - Windows: `%USERPROFILE%\.codex\skills\beyond-seo`
   - Mac/Linux: `~/.codex/skills/beyond-seo`
3. Do not copy any `.env` files, tokens, client exports, private data, or zip packages.
4. After installing, verify that `SKILL.md` exists at the destination.
5. Tell me the installed skill version from `SKILL.md`.

After that, I should be able to say:

Use the beyond-seo skill to audit this website.
```
```

## Optional Apify Setup Prompt

Each teammate should use their own Apify token. They can paste this separately:

```text
Help me set up my own `APIFY_API_TOKEN` environment variable for the Beyond SEO skill. Do not store the token in the skill files, reports, templates, manifests, or git repo.
```
