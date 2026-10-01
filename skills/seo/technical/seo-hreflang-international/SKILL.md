---
name: seo-hreflang-international
description: >-
  Design and debug international and multilingual SEO: hreflang annotations, URL structure (ccTLD, subdomain,
  subfolder), x-default and geotargeting. Use for "hreflang", "multilingual SEO", "international SEO", "wrong
  country version ranking", "language targeting", "x-default", "hreflang errors", "no return tags" or "expand
  site to new markets".
metadata:
  department: "seo"
  domain: "technical"
  owner: "satva-coe"
  status: "beta"
  license: "Satva-original"
  source: "original"
---

# International SEO and hreflang

Hreflang tells Google which alternate of a page to show a searcher in a given language/region. It swaps the URL in
results; it does not boost rankings and is not a canonical signal. Each language version must still be
indexable, self-canonical and independently good.

## Structure decision
| Option | Pros | Cons |
|---|---|---|
| ccTLD (`example.fr`) | Strong geo signal, trust | Costly, each domain builds authority separately |
| Subfolder (`/fr/`) | Shares domain authority, easy to ops | Weaker explicit geo signal (set via hreflang) |
| Subdomain (`fr.example.com`) | Separate hosting possible | Treated more like separate sites |
Default recommendation for most B2B/ecommerce: subfolders on one gTLD. Avoid URL parameters (`?lang=fr`) and
IP/cookie-based auto-redirect or content swap (Googlebot crawls mostly from the US and never sees alternate
versions). Offer a language switcher and a suggestion banner instead of forced redirects.

## Hreflang syntax
- Value = ISO 639-1 language, optionally `-` ISO 3166-1 Alpha-2 region: `en`, `en-GB`, `fr-CA`, `pt-BR`.
  Region alone is invalid (`GB` is wrong). Script variants allowed (`zh-Hans`, `zh-Hant`). Use `x-default` for the
  fallback/selector page.
- Rules: annotations must be **reciprocal** (A lists B, B lists A) or they are ignored; each page includes a
  **self-reference**; URLs absolute, canonical, 200, indexable; every page in the set lists the full set.
- Three equivalent methods; pick one and stay consistent:
  1. `<head>`:
  ```html
  <link rel="alternate" hreflang="en-us" href="https://www.example.com/us/pricing/" />
  <link rel="alternate" hreflang="en-gb" href="https://www.example.com/uk/pricing/" />
  <link rel="alternate" hreflang="fr"    href="https://www.example.com/fr/tarifs/" />
  <link rel="alternate" hreflang="x-default" href="https://www.example.com/pricing/" />
  ```
  2. HTTP `Link` header (for PDFs/non-HTML): `Link: <https://example.com/fr/doc.pdf>; rel="alternate"; hreflang="fr"`
  3. XML sitemap (best for large sites: no HTML bloat):
  ```xml
  <url><loc>https://www.example.com/us/pricing/</loc>
    <xhtml:link rel="alternate" hreflang="en-us" href="https://www.example.com/us/pricing/"/>
    <xhtml:link rel="alternate" hreflang="fr" href="https://www.example.com/fr/tarifs/"/>
  </url>
  ```
  with `xmlns:xhtml="http://www.w3.org/1999/xhtml"` declared.
- Google does not use `<html lang>` or `content-language` for targeting (Bing does read `content-language`); keep both accurate anyway.

## Workflow
1. Define markets and languages; confirm each has real, localised content (translated + currency, units,
   shipping, legal, local examples). Machine-translated thin duplicates risk quality problems.
2. Choose structure; set up GSC properties for each country folder/domain.
3. Map page equivalents (a table of `page_id | locale | URL`). Only pages with a real equivalent get hreflang;
   do not point missing translations to the homepage.
4. Generate annotations from that table (sitemap method for >~50 locales x pages). One source of truth.
5. Validate: crawl with hreflang extraction; report non-reciprocal, non-canonical targets, targets that are
   noindex/redirect/404, invalid codes, duplicate language-region conflicts, missing self-reference.
6. Monitor GSC performance filtered by country and the correct-version-ranking check with local SERP queries (VPN
   or `gl=`/`hl=` parameters).

## Debugging "wrong version ranks"
- Missing/non-reciprocal tags (most common) -> fix return links.
- Hreflang targets are canonicalised elsewhere (canonical points to another locale) -> each locale canonicals itself.
- Near-identical same-language variants (en-US vs en-GB) may be folded by Google as duplicates; differentiate
  or accept clustering.
- Geo auto-redirects hiding versions from Googlebot.
- Slow indexing of alternates: alternates need to be crawled to be recognised; link them internally and in sitemaps.

## Output
Locale map, chosen URL structure with rationale, hreflang generation spec, validation report (error counts by
type), and a rollout plan.

## Do not
- Use `en-UK` (invalid; correct is `en-GB`) or region-only codes.
- Canonical all locales to one URL (this removes the alternates from the index).
- Add hreflang to non-indexable pages or mix HTML and sitemap methods with conflicting values.
- Redirect users by IP and block crawlers from locale folders.
