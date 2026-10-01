---
name: seo-crawl-indexation-diagnosis
description: >-
  Diagnose why pages are not crawled or not indexed by Google, and fix robots.txt, XML sitemaps, canonical tags,
  noindex directives, soft 404s and duplicate clusters. Use for "page not indexed", "Crawled - currently not
  indexed", "Discovered - currently not indexed", "Duplicate, Google chose different canonical", "submitted URL
  blocked by robots.txt", "is my robots.txt right", "sitemap errors" or "crawl budget".
metadata:
  department: "seo"
  domain: "technical"
  owner: "satva-coe"
  status: "beta"
  license: "Satva-original"
  source: "original"
---

# Crawlability and indexation diagnosis

Crawling (fetching) and indexing (storing and eligible to rank) are separate. Diagnose in that order, one URL
class at a time. Always start from the exact status string in Search Console (Indexing > Pages) or the URL
Inspection tool; the wording tells you the stage that failed.

## Status string -> meaning -> first action
| GSC status | Meaning | First action |
|---|---|---|
| Blocked by robots.txt | Googlebot may not fetch it | Test in robots.txt report; remove the `Disallow` or accept it |
| Excluded by `noindex` tag | Meta/header noindex seen | Confirm intended; check X-Robots-Tag and rendered DOM |
| Page with redirect | URL redirects; target is what counts | Normal; remove from sitemap and fix internal links |
| Not found (404) / Soft 404 | Gone, or thin page returning 200 | 404/410 if gone; give soft-404 real content or a proper status |
| Duplicate without user-selected canonical | Google clustered it, you gave no signal | Add self-canonical on the preferred URL |
| Duplicate, Google chose different canonical than user | Your canonical was overridden | Compare content, internal links, redirects, sitemap signals; align all of them |
| Discovered - currently not indexed | Known URL, not yet crawled | Crawl-demand/quality/capacity problem; improve internal links, prune junk, check server speed |
| Crawled - currently not indexed | Fetched, judged not worth indexing | Quality/duplication problem: differentiate content, consolidate, strengthen internal links |
| Alternate page with proper canonical | Intentional duplicate | Normal |
| Server error (5xx) / Redirect error | Fetch failed or loop | Fix server/redirect; see log skill |

## Workflow
1. **Pick a sample** of 5-10 affected URLs per status and per template. Never debug from one URL.
2. **URL Inspection** on each: Google-selected vs user-declared canonical, last crawl date, crawl-allowed,
   indexing-allowed, referring sitemap, "Test live URL" to see current vs indexed render.
3. **Fetch raw** (`curl -sI -A "Googlebot" URL` and `curl -s URL`): status code, `Location`, `X-Robots-Tag`,
   `Link: <...>; rel="canonical"`, `<meta name="robots">`, `<link rel="canonical">`. Compare to rendered DOM.
4. **Check the robots.txt** (see rules below) and test the exact URL against it.
5. **Check sitemap hygiene**, canonical agreement, internal links pointing at non-canonical or redirected URLs.
6. **Check duplication**: parameters, trailing slash, case, `index.html`, http/https, www, pagination, faceted
   navigation, print/session URLs, near-duplicate location/service pages.
7. **Fix, then validate** with "Validate fix" in GSC; expect days to weeks. Canonical changes can take up to a
   couple of weeks to reconsolidate; do not call a fix failed after 48 hours.

## robots.txt rules that bite
- Location is `https://host/robots.txt` per host and protocol; subdomains need their own file.
- Max processed size 500 KiB (content beyond is ignored). UTF-8 plain text.
- HTTP behaviour: 2xx = parse; 4xx = treated as "no robots.txt" (everything allowed); 5xx or timeout = Google
  assumes everything disallowed for a while and may eventually fall back to a cached copy. A broken deploy that
  makes robots.txt return 503 can silently deindex a site: alert on it.
- Longest-match wins; `Allow` beats `Disallow` at equal length. `*` wildcard and `$` end anchor are supported.
- `Crawl-delay` is ignored by Google. `noindex` in robots.txt has been unsupported since 2019.
- Disallow does not remove a URL from the index: a blocked URL with external links can be indexed without a
  snippet. To deindex, allow crawling and serve `noindex` (a blocked page's `noindex` is never seen).
- Never block CSS/JS/image paths Google needs to render the page.
```
User-agent: *
Disallow: /cart/
Disallow: /*?sessionid=
Allow: /cart/help$

Sitemap: https://www.example.com/sitemap_index.xml
```

## Directive reference
- Page: `<meta name="robots" content="noindex, follow">`; any non-HTML file: `X-Robots-Tag: noindex`.
  Targeted: `<meta name="googlebot" content="noindex">`. Others: `nofollow`, `nosnippet`, `max-snippet:N`,
  `max-image-preview:large`, `unavailable_after: <date>`.
- Canonical: `<link rel="canonical" href="https://www.example.com/page/">` in the head, or HTTP `Link` header
  for PDFs. One canonical, absolute, pointing to a 200 indexable URL. Canonical is a hint, not a command.
- Conflicts to eliminate: canonical + noindex on the same page; canonical to a URL that redirects, 404s or is
  noindexed; canonicals differing between raw HTML and rendered DOM (Google may pick either); `noindex` in the
  raw HTML that JavaScript later removes (Google may honour the raw one).

## Sitemap rules
- Limits per file: 50,000 URLs and 50 MB uncompressed; use a sitemap index for more. Reference in robots.txt
  and submit in GSC.
- Include only canonical, 200, indexable URLs. A sitemap full of redirects/404/noindex teaches Google to ignore it.
- `<lastmod>` is used only if consistently accurate (real content change, W3C datetime); `changefreq` and
  `priority` are ignored. Separate sitemaps per type (pages, images, video, news) help diagnosis: GSC reports
  indexation per sitemap, so split by template to localise the problem.

## Crawl budget (only for >10k URLs or heavy daily change)
Waste sources: faceted navigation, infinite parameter combinations, internal search, calendar traps, redirect
chains, soft 404s, duplicate hosts. Levers: consolidate or robots-block genuinely useless parameter spaces,
fix internal links to point at canonical URLs, return 404/410 for dead sections, keep server response fast
(Google backs off on slow or 5xx hosts; there is no manual crawl-rate control). Verify with logs
(`seo-server-log-analysis`) before and after.

## Output
A table of URL classes: status string | count | root cause | fix | owner | validation date, plus the corrected
robots.txt / sitemap / template snippet.

## Do not
- Use robots.txt to hide pages you want deindexed, or to "save crawl budget" on a small site.
- Mass-submit URLs via Request Indexing as a fix; it is quota-limited and does not cure a quality or canonical issue.
- Treat "Crawled - not indexed" as a technical bug by default; it is usually a value/duplication judgement.
- Add noindex to paginated/filtered pages without checking that the products they list are linked elsewhere.
