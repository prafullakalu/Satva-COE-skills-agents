---
name: seo-monitoring-alerts
description: >-
  Design ongoing SEO monitoring and alerting so regressions (accidental noindex, robots.txt change, 5xx,
  canonical shifts, CWV decay, traffic drops, expiring certificates) are caught within hours. Use for "SEO
  monitoring", "set up SEO alerts", "detect noindex deploy", "SEO regression testing", "weekly SEO health
  dashboard", "uptime for robots.txt", "SEO change detection" or "what should we monitor after launch".
metadata:
  department: "seo"
  domain: "analytics"
  owner: "satva-coe"
  status: "beta"
  license: "Satva-original"
  source: "original"
---

# SEO monitoring and alerts

Most catastrophic SEO losses are self-inflicted deploys that nobody noticed for weeks. Monitoring is cheap
insurance. Design it in layers: synthetic checks (minutes), data checks (daily), trend checks (weekly).

## Layer 1: synthetic checks on every release and every hour/day
Run against a fixed list of ~20-50 URLs (one or two per template, the money pages, the homepage).
| Check | Assert | Severity |
|---|---|---|
| robots.txt | status 200; byte hash unchanged or diff reviewed; no `Disallow: /` for `User-agent: *`; sitemap line present | Page immediately |
| Status codes | 200 for key URLs, 301 for known redirects, 404 for known dead; response time < threshold | Page on 5xx |
| Meta robots / X-Robots-Tag | no `noindex` (unless expected); compare raw and rendered | Page |
| Canonical | equals expected self URL; absolute; same host | High |
| Title / H1 / meta description | present, not empty, not changed to a staging string | Medium |
| Hreflang | reciprocal set intact (sample) | Medium |
| Structured data | JSON-LD parses; required fields present | Medium |
| Sitemap | 200, valid XML, URL count within +/-20% of baseline, only 200 URLs in a sample | High |
| TLS certificate | days to expiry > 21 | High at 21 / Page at 7 |
| Hostname | staging hostname or `localhost` in canonicals/links | Page |
| Redirects | http->https and www normalisation in one hop | Medium |
Implementation: a scheduled script (cron/GitHub Actions/serverless) using curl or a headless browser, writing
results to a table with last-known-good snapshot and diff; notify on change. Run the same suite in the CI pipeline
against the staging build before release (fail the pipeline on critical asserts). Existing tools can supply this
(change detection, uptime monitors, crawler scheduled audits); do not build bespoke if a tool covers it.

## Layer 2: daily data checks
- Search Console (API or BigQuery export): clicks and impressions vs the same weekday average of the previous 4 weeks;
  alert when a section's clicks fall more than ~25-30% (tune to variance) for 2 consecutive days. Account for
  2-day data lag.
- Indexing: count of "not indexed" by reason; alert on a jump in `Server error (5xx)`, `Blocked by robots.txt`,
  `Excluded by noindex`, `Soft 404`.
- Sitemap submitted vs indexed ratio.
- Manual actions / security issues: email notifications on for all owners; route to a shared mailbox.
- Crawl stats: host availability issues, average response time rising.
- GA4: organic sessions anomaly via Analytics Intelligence custom insights, or BigQuery z-score vs trailing mean.
- Logs (if available): share of Googlebot 5xx and 3xx; sudden Googlebot volume change.

## Layer 3: weekly/monthly
- Core Web Vitals field data (CrUX API/GSC): alert when a template moves from Good to Needs improvement/Poor
  (LCP > 2.5 s, INP > 200 ms, CLS > 0.1 at p75).
- Rank tracking for ~50-200 priority queries by market/device; alert on top-3 losers.
- Backlink loss/gain for key pages; brand SERP changes; competitor changes (new pages, schema).
- Index bloat/crawl diff: scheduled full crawl compared with the previous crawl (new/removed URLs, changed
  titles/canonicals/status).

## Alert hygiene
1. Define an owner and an on-call route per severity (page vs ticket vs weekly digest). 2. Every alert has a
runbook line (what to check, who to call, how to roll back). 3. Tune thresholds from history; suppress known
events (planned migrations, holidays). 4. Track mean time to detect. 5. Review false positives monthly.

## Release gate (minimum viable)
Before each production deploy: crawl or fetch the representative URL list on staging; assert indexable, canonical,
title, robots.txt production-correct, no staging hostnames. After deploy: re-run the same list on production
within 15 minutes.

## Output
Monitoring spec: check | tool | frequency | threshold | severity | owner | runbook link; a sample alert message
(what failed, URL, expected vs actual, first action); and baseline values recorded with date.

## Do not
- Alert on every small ranking wiggle or day-of-week variance.
- Rely on a single human to open the Search Console emails.
- Monitor only the homepage; templates are what break.
- Store API tokens in the monitoring script; use a secret manager.
