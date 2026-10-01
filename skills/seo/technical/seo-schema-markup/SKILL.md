---
name: seo-schema-markup
description: >-
  Plan, write and validate schema.org structured data (JSON-LD) for search. Use for "add schema", "structured
  data", "JSON-LD", "rich results", "product schema", "article schema", "FAQ schema", "LocalBusiness
  markup", "Organization schema", "breadcrumb markup", "why is my rich result not showing" or "schema errors in
  Search Console".
metadata:
  department: "seo"
  domain: "technical"
  owner: "satva-coe"
  status: "beta"
  license: "Satva-original"
  source: "original"
---

# Schema markup (structured data)

Structured data describes what is already visible on the page in a machine-readable vocabulary
(schema.org). It makes pages eligible for rich results and helps entity understanding. It does not
guarantee a rich result and it is not a ranking factor by itself.

## Principles
1. Mark up only content that is visible to users on that page. Hidden or contradictory markup is a spam
   violation (manual action risk).
2. Use **JSON-LD** in `<script type="application/ld+json">`, preferably server-rendered in the initial HTML.
   JS-injected markup is processed later and can be missed on time-sensitive pages (price, stock).
3. Use the most specific type, include all *required* properties and as many *recommended* ones as the page
   truly supports. Google's per-feature documentation is the authority on required/recommended fields.
4. Link entities with `@id` and reference them rather than duplicating (`"publisher": {"@id": "https://example.com/#org"}`).
5. Keep markup in sync with the CMS: generate from the same data fields as the page, not hand-pasted.

## Workflow
1. **Map page templates to types**:
   | Template | Types |
   |---|---|
   | Home / about | `Organization` (or `LocalBusiness` subtype), `WebSite` |
   | Article / blog | `Article` / `BlogPosting` / `NewsArticle`, `BreadcrumbList`, `Person` author |
   | Product | `Product` + `Offer` (price, priceCurrency, availability, url) + `AggregateRating`/`Review` only if real |
   | Category | `CollectionPage`/`ItemList`, `BreadcrumbList` |
   | Local / location | `LocalBusiness` subtype (`Dentist`, `Restaurant`, `ProfessionalService`...), `PostalAddress`, `GeoCoordinates`, `OpeningHoursSpecification` |
   | Event | `Event` with `startDate`, `location`, `eventAttendanceMode` |
   | Job posting | `JobPosting` (title, description, datePosted, hiringOrganization, jobLocation, validThrough) |
   | Video | `VideoObject` (name, thumbnailUrl, uploadDate) |
   | Software | `SoftwareApplication` |
   | Any hierarchy | `BreadcrumbList` |
2. **Check current eligibility** in Google's Search gallery before investing: Google has retired or restricted
   several features (FAQ rich results are limited to well-known authoritative government/health sites; HowTo
   rich results were removed; the sitelinks search box was removed). Valid schema.org markup without a Google
   feature is still harmless and can still help other consumers, but do not promise a SERP change. Re-verify the
   gallery each audit because the list changes.
3. **Write** the JSON-LD from page data (see example). Use ISO 8601 dates, absolute URLs, numeric prices without
   currency symbols, `availability` as the schema.org URL (`https://schema.org/InStock`).
4. **Validate**: Rich Results Test (eligibility, Google-specific) and Schema Markup Validator
   (schema.org syntax, vendor-neutral). Fix errors first (block eligibility), then warnings.
5. **Deploy** on a sample of templates, then monitor GSC > Enhancements reports (Products, Breadcrumbs,
   Videos, etc.) and the "Search appearance" filter in Performance.
6. **Maintain**: re-validate after every template release; add schema checks to monitoring.

## Example: Product (server-rendered)
```json
{
  "@context": "https://schema.org",
  "@type": "Product",
  "@id": "https://www.example.com/p/widget#product",
  "name": "Widget Pro",
  "image": ["https://www.example.com/img/widget-1x1.jpg"],
  "description": "Short factual description matching the page.",
  "sku": "WID-001",
  "brand": {"@type": "Brand", "name": "Example"},
  "offers": {
    "@type": "Offer",
    "url": "https://www.example.com/p/widget",
    "price": "49.00",
    "priceCurrency": "USD",
    "availability": "https://schema.org/InStock",
    "itemCondition": "https://schema.org/NewCondition"
  }
}
```
Organization snippet: `@type Organization`, `name`, `url`, `logo`, `sameAs` (official profile URLs),
`contactPoint`. `sameAs` should list only profiles you control.

## Common failure modes
- Price/availability in markup differs from the page or feed (also triggers Merchant Center mismatch).
- `AggregateRating` self-written about the business itself, or copied reviews: policy violation.
- Missing required property (e.g. `Offer.price`), invalid enum value, relative URLs, wrong date format.
- Duplicate conflicting blocks from theme plus SEO plugin: emit one authoritative graph, disable the others.
- Markup on a noindexed page or one blocked by robots.txt (never processed).
- Marking up content not on the page (FAQ answers hidden, reviews from another site).
- Using Microdata/RDFa and JSON-LD for the same entity with different values.

## Output
Template-to-type map, the JSON-LD per template with the CMS field each property comes from, validation results
(tool, errors, warnings), and a rollout/monitoring plan.

## Do not
- Add `Review`/`AggregateRating` without genuine, visible, first-party reviews.
- Mark up everything possible "for SEO"; each type needs a purpose.
- Rely on schema to fix thin content or indexation problems.
- Hand-write markup per page when a template can generate it.
