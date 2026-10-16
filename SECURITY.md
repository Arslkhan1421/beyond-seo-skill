# Security reporting

Do not disclose credentials, private client exports or exploitable security details in a public issue.

Use this repository's **Security → Report a vulnerability** option for a private report. If that option is unavailable, use GitHub's private reporting/support channels rather than opening a public issue containing exploit details or secrets.

Include the affected release/commit, component, expected security boundary, reproduction steps, impact and a minimal synthetic example. Redact access tokens, cookies, private URLs and customer information. Do not test systems you do not have authorization to assess.

The current release is v1.5.1. Reproduce against the latest release where possible; provide the exact older version if the problem is version-specific. No response-time or remediation-service commitment is implied.

The project processes untrusted HTML, URLs, XML/gzip, CSV and JSON. Relevant reports include scope or network-boundary bypasses, credential exposure, unsafe artifact handling and unbounded input processing. SEO inaccuracies and feature requests belong in normal issues when no sensitive information is involved.
