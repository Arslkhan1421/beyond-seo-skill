# One-Line Install Prompt

After this project is pushed to GitHub, give your team one line like this:

```text
Install the Codex skill from https://github.com/YOUR_ORG/YOUR_REPO/tree/main/skills/beyond-seo
```

That is it.

Codex should use the `skill-installer` skill, download the folder from GitHub, and install it into:

```text
~/.codex/skills/beyond-seo
```

For Windows, that means:

```text
C:\Users\THEIR_USERNAME\.codex\skills\beyond-seo
```

After install, they should restart Codex so the new skill is picked up.

## Example

If your repo is:

```text
https://github.com/puredesigners/beyond-seo-skill
```

The install line is:

```text
Install the Codex skill from https://github.com/puredesigners/beyond-seo-skill/tree/main/skills/beyond-seo
```
