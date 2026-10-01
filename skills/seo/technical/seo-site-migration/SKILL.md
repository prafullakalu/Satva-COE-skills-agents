---
name: seo-site-migration
description: >-
  Plan and execute an SEO-safe site migration: redirect mapping, URL inventory, launch checklist and post-launch
  monitoring. Use for "site migration", "redesign without losing rankings", "change domain", "move to HTTPS",
  "switch CMS/platform", "URL restructure", "redirect map", "301 redirects", "staging launch SEO checklist" or
  "traffic dropped after relaunch".
metadata:
  department: "seo"
  domain: "technical"
  owner: "satva-coe"
  status: "beta"
  license: "Satva-original"
  source: "original"
---

# Site migration

A migration changes URLs, domain, platform, structure or rendering. Rankings transfer only if every old URL that
earned traffic or links maps to its closest equivalent and the new site is indexable. Expect a short volatility
window even when done perfectly; plan for it.

## Migration types and risk
| Type | Risk | Notes |
|---|---|---|
| HTTP -> HTTPS | Low | Per-URL 301, update canonicals/sitemaps/internal links, HSTS after stable |
| Redesign, same URLs | Medium | Risk is content/template/JS changes, not redirects |
| URL restructure / CMS change | High | Redirect map is the project |
| Domain change / merge | High | Add new domain property, Change of Address tool |
| Subdomain <-> folder | High | Treat as domain-level move |
| JS framework / rendering change | High | See `seo-javascript-rendering` |

## Workflow
1. **Benchmark (before anything changes).** Full crawl of old site; export GSC top pages and queries (16 months);
   GA4 landing pages with conversions; backlink URLs with links (Ahrefs/Majestic/GSC Links); current rankings for
   priority keywords; CWV baseline; XML sitemap and robots.txt snapshots. Store dated copies.
2. **Inventory and scope.** One master list of every old URL = crawl + sitemap + GSC + analytics + backlinks (deduped,
   normalised for scheme/host/case/slash). Tag each: keep, merge, retire.
3. **Redirect map.** For each old URL assign one target:
   - Same content -> exact new URL (301 or 308).
   - Merged/consolidated -> the best matching page (not the homepage).
   - Truly gone with no equivalent -> 410 or 404. Mass redirect to the homepage is treated as soft 404.
   Prioritise by traffic + referring domains. Pattern rules (regex) cover bulk templates; one-off rows cover
   high-value pages. Resolve chains: old -> final in a single hop. Include parameters and case variants.
4. **Pre-launch on staging** (blocked from indexing by authentication or `noindex`, never robots.txt-only).
   Crawl staging with the redirect map applied and test: every old URL returns 301 to a 200 target; targets are
   indexable; canonicals self-reference the new URL; hreflang, structured data, titles, meta, H1, internal
   links, images, PDFs, sitemap all use new URLs; no staging hostnames leak; robots.txt is the production one
   but ready to ship allowing crawl.
5. **Launch** during low traffic, with dev and SEO on call. Order: deploy site, remove staging noindex/auth
   (check that the production robots.txt and meta robots do NOT carry the staging blocks, the classic launch
   failure), enable redirects, submit new sitemap, add/verify new GSC property, test the top 50 old URLs live.
6. **Domain change only:** keep the old domain verified in GSC, 301 old -> new per URL, then use *Change of
   Address* (Settings, from the old Domain/Domain-prefix property). Not available for HTTP->HTTPS or
   subdomain moves. Also update Google Business Profile, Analytics, ad accounts, email/SPF, social profiles,
   and ask top linking sites to update links.
7. **Post-launch monitoring (daily for 2 weeks, then weekly for 3 months).** GSC: Indexing > Pages errors, new
   404s, crawl stats (Settings > Crawl stats), clicks by section; analytics: organic landing sessions vs
   benchmark; log files: Googlebot hitting old URLs (should see 301s), 5xx, redirect chains; rankings.
   Fix newly surfaced 404s with new map rows.
8. **Retention.** Keep redirects live at least 12 months (indefinitely for URLs with backlinks). Keep the old
   domain registered for years.

## Redirect rules
- Permanent: 301 or 308 server-side (nginx `return 301`, Apache `RewriteRule ... [R=301,L]`, edge rules).
  Avoid meta-refresh and JS redirects. 302/307 only for genuinely temporary moves.
- Preserve protocol/host normalisation in the same hop (do not chain http -> https -> www -> new).
- Redirect map columns: old URL | new URL | status | rule type | traffic | linking domains | owner | tested.
- Test with a list tester or crawler in list mode: assert status, final URL, hop count, final 200/indexable.
- Internal links, canonicals, sitemaps and hreflang must be updated to new URLs; redirects are for external/old
  links, not for site navigation.
- Large sites: rules must not slow TTFB; benchmark regex rule count.

## Expectation setting
Temporary fluctuation of weeks is normal; a sustained drop beyond ~4-6 weeks signals a mapping, indexability,
content-parity or performance issue. Pre-agree a rollback threshold and who decides.

## Output
Benchmark pack, master URL inventory, redirect map, staging test report, launch runbook (owner and time per
step), post-launch dashboard definition, and a go/no-go checklist signed off before launch.

## Do not
- Launch with staging `noindex` or `Disallow: /` still in place, or with a staging domain in canonicals.
- Redirect everything to the homepage or to a generic category.
- Combine a migration with a major content rewrite and a redesign without a plan to isolate the cause.
- Delete the old redirect layer after a few weeks.
- Change URLs "while we are at it" if they were not part of the brief.
