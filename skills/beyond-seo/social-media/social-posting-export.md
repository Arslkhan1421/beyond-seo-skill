# Social Posting Export

Use this module when the user asks to export LinkedIn or Instagram content to CSV, spreadsheet, scheduler-ready format, or posting handoff files.

## Export Purpose

Create files that can be reviewed manually or imported into scheduling tools such as Buffer, Hootsuite, Later, Metricool, Sprout Social, SocialBee, HubSpot, or similar tools.

Do not claim direct posting is complete. This module prepares content for human approval and scheduler import.

## Default CSV Columns

Use `templates/social-posting-30-day-template.csv` when available.

Required columns:

```text
day
date
platform
post_type
content_pillar
seo_source_url
target_keyword_or_topic
hook
post_copy
caption
carousel_slides_or_visual_brief
cta
target_url
utm_url
hashtags
evidence_label
status
approval_notes
```

## UTM Pattern

Use a readable campaign slug:

```text
utm_source={platform}
utm_medium=social
utm_campaign={campaign_slug}
utm_content=day-{day}-{post_type}
```

If the target URL already has query parameters, append UTM parameters with `&`. Otherwise use `?`.

## Scheduler Compatibility

If the user names a scheduler, adapt column names to that scheduler's import format when known. If unsure, keep the default Beyond SEO format and mention that the file may need column mapping inside the scheduler.

## Export Quality Gate

Before delivering an export:

- check that every row has platform, post type, hook, copy/caption, CTA, status, and evidence label;
- check target URLs for link posts;
- check UTM URLs are present when target URLs are present;
- avoid duplicate post copy;
- keep LinkedIn copy and Instagram captions separate when a post appears on both platforms;
- keep hashtags platform-relevant;
- keep all unverified performance claims out of the copy.

## API Publishing Boundary

This module does not publish posts through LinkedIn, Instagram, Meta, or third-party scheduler APIs.

If the user asks for auto-posting later, require:

```text
platform or scheduler choice
developer app or scheduler API access
permissions/scopes
account/page IDs
media assets
human approval step
dry-run mode
posting log
rollback/edit plan
```
