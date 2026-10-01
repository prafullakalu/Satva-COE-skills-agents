---
name: sales-tax-vat-gst-compliance
description: >-
  Indirect tax support: sales tax, VAT and GST. Registration and nexus thresholds, taxability and rate checks, return preparation, input credits, reverse charge, marketplace facilitators, reconciliation to the GL. Includes a not-tax-advice boundary. Use for "sales tax return", "do we need to register", "VAT reconciliation", "GST BAS/return prep", "nexus review", "tax control account doesn't match".
metadata:
  department: "accounting"
  domain: "tax"
  owner: "satva-coe"
  status: "beta"
  license: "Satva-original"
  source: "original"
---

# Sales tax / VAT / GST compliance support

**Boundary: this skill supports preparation and review. It is not tax advice.** Rates, thresholds, exemptions and filing rules change by jurisdiction and date; confirm against the tax authority's current guidance or a licensed adviser before filing or taking a position. Mark any assumption you could not verify.

## Concepts
- **US sales tax:** destination-based, imposed on the buyer, collected by the seller with nexus. No input credit: purchases for resale are exempt via resale certificates; consumable purchases pay tax (use tax if the vendor did not charge).
- **VAT/GST:** tax at every stage; output tax on sales minus input tax on purchases = net payable (or refundable). Zero-rated (taxable at 0%, input recoverable), exempt (no output, input usually not recoverable) and out-of-scope are different.
- **Reverse charge:** buyer self-assesses on certain cross-border services/goods; records output and input simultaneously.

## Registration and nexus review
1. US: for each state compute last-12-month (or calendar-year, per state) gross sales and transaction count into the state. Economic nexus thresholds are commonly 100,000 in sales or 200 transactions, but they vary (some drop the transaction test, some differ). Physical presence (employees, inventory incl. third-party warehouses, events) creates nexus regardless of volume. Record the date the threshold was crossed; registration is due per state rules, and uncollected back tax is exposure.
2. VAT/GST: compare taxable turnover with the local registration threshold (varies widely by country); distance-selling and digital-services rules may require registration in the customer's country; non-resident rules differ.
3. Marketplace facilitators (e.g. major marketplaces) often collect and remit for their sales in US states: exclude those sales from your own collection duty but keep them for threshold tracking where the state counts them.
4. Output: nexus matrix: jurisdiction | threshold | 12-month sales | status | action | evidence.

## Taxability and rate checks
- Map every product/service to a tax code per jurisdiction (taxable, exempt, reduced rate). SaaS, digital goods, shipping, delivery charges, gift cards and services differ by state/country.
- Rate source: use the tax system or authority tables; never type rates from memory. Rates must be rooftop/destination-accurate for US, and valid on the invoice date.
- Exemptions: hold a valid certificate (resale, government, non-profit) with expiry date; no certificate means tax is due.

## Return preparation
1. Pull taxable sales, exempt sales, tax collected by jurisdiction and rate for the filing period (accrual vs cash basis per jurisdiction).
2. Adjust for credit notes, bad-debt relief where allowed, prior-period corrections.
3. VAT: output tax by box; input tax on purchases and imports (check valid tax invoice, business purpose, partial-exemption apportionment); reverse charge entries.
4. Reconcile: tax per return = tax control account movement. Formula: Opening balance + tax collected/accrued - tax paid/credited = Closing balance. Differences usually come from rounding at line vs invoice level, timing of payments, manual adjustments, or tax posted to wrong account.
5. Reviewer checks: filing deadline, payment date, penalty/interest exposure, e-filing receipt.

## Evidence to keep
Return and filing confirmation, sales/purchase tax reports, exemption certificates, valid input tax invoices, customs documents for imports, nexus matrix, reconciliation of control account. Retain for the jurisdiction's statutory period (commonly 4-10 years).

## Red flags
- Tax collected and not remitted (liability balance growing); tax code "none" on taxable items; rate changes mid-period not updated; invoices to EU businesses without a validated VAT number; negative tax payable not investigated.

## Do not
Do not decide taxability, nexus conclusions or voluntary disclosures on your own; surface to a tax professional. Do not file or pay without approval. Do not net tax into revenue.

## Output
Return worksheet (box-by-box or jurisdiction-by-jurisdiction), control account rec, nexus matrix, and a list of assumptions and questions for the tax adviser.
