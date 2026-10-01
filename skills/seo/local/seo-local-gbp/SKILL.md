---
name: seo-local-gbp
description: >-
  Plan, audit and optimise local SEO and Google Business Profile for single-location, multi-location and
  service-area businesses. Use for "local SEO", "Google Business Profile", "GBP optimisation", "Google Maps
  ranking", "local pack", "NAP consistency", "citations", "reviews strategy", "multi-location SEO", "service
  area business", "suspended Google listing" or "LocalBusiness schema".
metadata:
  department: "seo"
  domain: "local"
  owner: "satva-coe"
  status: "beta"
  license: "Satva-original"
  source: "original"
---

# Local SEO and Google Business Profile

Google ranks local results on **relevance** (profile + site match the query), **distance** (searcher to business, or
to the specified location) and **prominence** (reviews, links, citations, brand fame). You control relevance and
influence prominence; you cannot control distance, so set expectations by geography.

## Eligibility and policy first
- A GBP listing is for a business with in-person contact with customers at a staffed address, or a service-area
  business (SAB) that travels to customers. P.O. boxes, virtual offices and unstaffed spaces are ineligible.
- SABs hide the address and list service areas (max 20); storefronts show the address.
- Business name = real-world name (as signage/branding). Adding keywords or a location to the name is a
  guideline violation and the commonest reason for suspension. Lead-gen or "directory" listings are not allowed.
- Review gating (soliciting only happy customers), incentivised reviews and fake reviews violate policy.

## Audit workflow
1. **Discovery**: list each location with legal name, exact address, phone, hours, categories, URL, ownership
   (who has Owner access), verification status. Search the brand and `category + city`; screenshot the local
   pack and Maps results.
2. **GBP completeness**:
   - Primary category = the most specific category that describes the main service (biggest relevance lever);
     add secondary categories that truly apply (usually <=3-5).
   - Services and products with descriptions; attributes; opening hours incl. special hours; service areas.
   - Business description (750 chars max), no promotional URLs/phone numbers/keyword stuffing.
   - Photos: exterior, interior, team, work; add regularly; real, not stock. Cover and logo set.
   - Website link to the location landing page (not the homepage, for multi-location), tagged
     with UTM (`utm_source=google&utm_medium=organic&utm_campaign=gbp`) so GA4 separates it. Appointment/menu links.
   - Posts/updates periodically; Q&A seeded and monitored (where available); messaging per policy.
3. **Reviews**: volume, velocity, average, recency, response rate. Reply to every review professionally within
   days; address negatives factually; ask every customer via a neutral link (the GBP review link/QR), never
   gate. Keyword mentions occur naturally; do not script them.
4. **NAP consistency and citations**: Name, Address, Phone identical across site, GBP and core data aggregators
   and directories (Apple Business Connect, Bing Places, Facebook, Yelp, industry/local directories). Fix
   duplicates (search the phone and address), closed or moved listings and tracking-number conflicts (use the
   main number as primary, tracking as additional).
5. **Website local signals**:
   - One unique, substantive landing page per location (and per major service+location combination only when the
     content is genuinely different): name, address, phone, hours, embedded map, directions, staff, local
     testimonials, services, FAQs, photos. No doorway pages with swapped city names.
   - Page title: `Primary Service in City | Brand`; H1 matching; consistent NAP in the HTML (text, not image).
   - Internal links from a locations hub and relevant service pages; breadcrumbs.
   - `LocalBusiness` (or specific subtype) JSON-LD per location page with `name`, `address` (`PostalAddress`),
     `telephone`, `geo` (`GeoCoordinates`), `openingHoursSpecification`, `url`, `sameAs`, `image`, `priceRange`. Match visible content
     (see `seo-schema-markup`).
   - Mobile speed and click-to-call/click-to-map links; Core Web Vitals pass.
6. **Prominence/links**: local press, sponsorships, chambers, supplier/partner pages, unique local content;
   not paid link networks.
7. **Measure**: GBP Performance (calls, direction requests, website clicks, search/Maps views, search terms), GA4
   (UTM traffic and conversions), call tracking, local rank grid tracking (e.g. a geo-grid tool) with several
   points around each location, not one pin. Report by location. Set baseline before work begins.

## Multi-location notes
Use the bulk upload/GBP API/Business Profile management tools for scale; keep one source of truth for location
data; enforce naming and category conventions; central review-response workflow; location pages generated from
structured data but with unique local content blocks; store locator crawlable (no JS-only search with no URLs).
Handle closures and moves: mark closed or update address; redirect and update the page.

## Suspensions and problems
Common causes: keyword-stuffed name, ineligible address, edits to category/name/address on a verified listing
triggering re-verification, duplicate listings, shared address with a similar business. Process: read the exact
violation, correct the listing to reality, gather evidence (signage, licence, utility bill, storefront and
interior photos, branded vehicles), submit reinstatement via the Business Profile appeal form. Do not create a new
listing to get around a suspension.

## Output
Location audit table (location | completeness % | NAP issues | review stats | landing page status | schema | key gap),
a prioritised 30/60/90-day plan, citation clean-up list, and monthly reporting spec.

## Do not
- Buy reviews, gate reviews, or offer discounts for positive reviews.
- Put keywords or locations into the business name.
- Create multiple listings for one location, or virtual-office listings.
- Clone location pages with only the city name swapped.
- Promise a map-pack position; distance and competition cap outcomes.
