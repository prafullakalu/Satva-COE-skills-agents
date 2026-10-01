---
name: seo-server-log-analysis
description: >-
  Analyse web server or CDN access logs to see how Googlebot and other crawlers actually behave: crawl waste,
  status codes, orphan discovery, crawl frequency per section. Use for "log file analysis", "Googlebot crawl
  stats", "crawl budget waste", "what is Google crawling", "verify Googlebot", "access log SEO", "crawl spike" or
  "pages Google never crawls".
metadata:
  department: "seo"
  domain: "technical"
  owner: "satva-coe"
  status: "beta"
  license: "Satva-original"
  source: "original"
---

# Server log analysis for SEO

Logs are the only ground truth of what crawlers fetch. GSC Crawl Stats is a sampled summary; logs are complete and
per-URL. Use them to confirm or refute hypotheses from crawls and GSC, mainly on sites above ~10k URLs, after
migrations, or when indexing lags.

## Data to obtain
- 30 days minimum (90 for seasonal sites) of raw access logs from origin and CDN (CloudFront, Cloudflare Logpush,
  Fastly, nginx/Apache). CDN logs miss nothing the edge cached; origin logs miss cache hits: prefer edge logs.
- Fields: timestamp, client IP, method, URL (with query), status, bytes, response time, user agent, referrer,
  host, cache status.
- Privacy: logs hold IP addresses. Strip or hash non-bot IPs before analysis and storage; keep only crawler
  rows. Do not paste raw logs into tickets or chat.

## Verify the bot (user agents are spoofed)
1. Filter by UA string containing `Googlebot` (Smartphone UA contains "Mobile Safari" and "Googlebot/2.1";
   also `Googlebot-Image`, `Googlebot-Video`, `AdsBot-Google`, `Google-InspectionTool`, `GoogleOther`; Bing is `bingbot`).
2. Verify by IP: reverse DNS resolves to `*.googlebot.com` or `*.google.com`, and forward DNS of that host returns the
   same IP; or match against Google's published IP range JSON (googlebot.json / common-crawlers.json under
   developers.google.com/search/apis/ipranges). Drop unverified rows into a "fake bot" bucket and report it.
3. AI crawlers (`GPTBot`, `OAI-SearchBot`, `ClaudeBot`, `PerplexityBot`...) can be broken out the same way to see
   how much they fetch; verify with the vendor's published ranges.

## Parsing (combined log format)
```
IP - - [10/Oct/2026:13:55:36 +0000] "GET /path?x=1 HTTP/1.1" 200 5316 "ref" "UA"
```
Load into a database/BigQuery/DuckDB/pandas. Normalise the URL (lowercase host, strip fragments, keep query
for parameter analysis), derive `directory`, `template`, `has_params`, `status_class`, `is_verified_bot`.

## Analyses (each yields an action)
1. **Crawl volume trend**: Googlebot hits/day by type (smartphone vs desktop vs image). Sudden drop: robots/5xx/
   server speed incident. Spike: new parameter trap, migration, or bad deploy.
2. **Status mix** for verified Googlebot: target ~90%+ 200; track share of 3xx (chains and un-updated links),
   4xx (dead links, missing redirects), 5xx (stability; any 5xx cluster correlates with crawl slowdown), 304.
3. **Crawl allocation by section/template vs business value**: % of hits to money pages versus faceted/
   parameter/search/pagination/legacy URLs. Waste share = hits to non-indexable, non-canonical, parameterised or
   redirecting URLs. Compare with revenue share.
4. **Frequency per URL class**: median days between crawls for key templates; slow recrawl of important or
   frequently changing pages suggests weak internal links or thin quality.
5. **Never-crawled set**: sitemap URLs and crawler-discovered URLs with zero Googlebot hits in the window
   (discovery problem) versus URLs crawled but not indexed (quality problem).
6. **Orphans**: URLs Googlebot hits that are absent from the crawl graph (old links, external links, stale sitemaps).
7. **Response time**: Googlebot average/p95 time-to-first-byte by template; slow responses reduce crawl rate.
8. **Redirect and 404 hot spots**: top 50 URLs by Googlebot hits that return 3xx/4xx; fix at source.
9. **Rendering resources**: Googlebot hits to JS/CSS/API paths returning errors or blocked by robots.txt.
10. **Before/after tests**: compare crawl allocation across a robots.txt/internal-link change (use same weekday mix).

## Output
Dashboard or table: metric | value | benchmark | finding | action | expected effect; plus a top-50 waste URL list
with the fix per pattern (robots rule, canonical, redirect, link removal, 410).

## Do not
- Count every UA containing "Googlebot" as Google.
- Optimise "crawl budget" on a small site; crawl demand, quality and links are the issue there.
- Block waste URLs in robots.txt before confirming the valuable pages remain reachable and linked.
- Keep raw logs with personal data longer than the analysis requires.
