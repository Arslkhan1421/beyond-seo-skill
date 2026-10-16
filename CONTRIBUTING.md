# Contributing to Beyond SEO

Use [issues](https://github.com/Arslkhan1421/beyond-seo-skill/issues) for reproducible bugs and focused feature requests. Search existing issues first. Keep proposals tied to a concrete audit workflow and explain the evidence available.

## Development

Use Python 3.11 or newer and an isolated environment:

```text
python -m venv .venv
```

Activate it with `.venv\Scripts\Activate.ps1` on Windows PowerShell or `source .venv/bin/activate` on macOS/Linux, then run:

```text
python -m pip install -r skills/beyond-seo/requirements.txt
python skills/beyond-seo/tools/validate_skill.py
python -m unittest discover -s skills/beyond-seo/tests -v
```

CI checks Python 3.11 and 3.14.

## Pull requests

- Explain the concrete problem, final behavior and validation performed.
- Keep changes focused. Include regression coverage for meaningful behavior changes and false-positive cases.
- Retain the evidence contract: source, provenance, collection time, scope, artifact references and honest missing-data labels.
- Do not turn heuristic review candidates into verified causes, guaranteed rankings or automatic redirects/disavow actions.
- Preserve bounded network access, offline execution and credential redaction.
- If package files change, update the complete index in SKILL.md and run `tools/build_manifest.py`; the portable skill must remain within its 90-file budget.
- For report changes, render a sample PDF and inspect page breaks, tables and evidence labels.
- Document breaking input/schema/path changes and update release metadata consistently when a release version changes.

Never include client exports, private audit outputs, credentials, `.env` files or local environments. Use synthetic or properly anonymized fixtures. Follow [security reporting](SECURITY.md) for sensitive findings and the [code of conduct](CODE_OF_CONDUCT.md) when participating.

Contributions must be compatible with the MIT License. Do not submit third-party or client material you do not have permission to contribute.
