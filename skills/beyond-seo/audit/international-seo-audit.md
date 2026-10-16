# International and multi-regional SEO
Run `tools/international_checks.py` on observed crawl JSON. The runtime also saves international-review.json and includes review candidates in the PDF.
- Validate ISO 639-1 languages, optional ISO 15924 scripts and ISO 3166-1 alpha-2 regions through pycountry. Country-only codes, en-UK and es-419 are not valid Google language/region combinations.
- Check self references, conflicting destinations for one code, observed return links, noindex alternates and canonical destinations. Unsampled alternate pages are Not verified, not missing-return errors.
- x-default is optional fallback guidance, not a required property. Cross-domain alternates are allowed but must be separately sampled; never silently expand a network crawl to new hosts.
- Review HTML, HTTP Link and sitemap implementations separately. The automated checker currently covers HTML tags only. Regional targeting does not establish local presence, Google rankings or indexation.
- Confirm translations, currency, delivery areas, contact details and regional legal copy with the owner. Avoid doorway country pages and automatic redirects by IP.
Source checked 2026-10-15: https://developers.google.com/search/docs/specialty/international/localized-versions . Recheck at use.
