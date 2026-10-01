---
name: ecommerce-kpi-metrics
description: >-
  Define, compute and sanity-check e-commerce finance KPIs from ledger and store data: net revenue, gross and contribution margin, AOV, refund and discount rates, CAC, MER/ROAS, repeat rate, LTV, inventory turns, sell-through, cash conversion and payout reconciliation. Use for "e-commerce metrics", "Shopify KPI report", "contribution margin by channel", "is our ROAS real", "why does the store dashboard not match the ledger", "monthly KPI pack for an online store".
metadata:
  department: "accounting"
  domain: "ecommerce-reporting"
  owner: "satva-coe"
  status: "beta"
  license: "Satva-original"
  source: "original"
---

# E-commerce KPI metrics

Store dashboards report gross order value; the ledger reports recognised revenue net of refunds, discounts, fees and timing. A KPI pack is only trusted when each store-side figure reconciles to the ledger. Compute from the ledger first, use store data for drivers.

## Definitions (state them in the pack header)
| KPI | Formula | Trap |
|---|---|---|
| Gross sales | List price x units, before discounts | Includes cancelled and unpaid orders in some exports |
| Net revenue | Gross sales - discounts - refunds/returns (excl. tax, incl. shipping charged if policy says so) | Sales tax/VAT collected is a liability, never revenue |
| Gross margin % | (Net revenue - COGS incl. landed cost, packaging, payment fees if policy) / Net revenue | Freight-in and duties omitted from COGS inflate margin |
| Contribution margin | Net revenue - COGS - fulfilment - shipping paid - payment fees - variable marketing | Allocate shared costs by driver, state the key |
| AOV | Net revenue / orders | Use orders, not line items; exclude zero-value replacements |
| Refund rate | Refunds / gross sales (value) and units returned / units sold | Refunds booked in a later month than the sale: use cohort view too |
| Discount rate | Discounts / gross sales | Track by code and channel |
| CAC | Paid acquisition spend / new customers | Blended CAC includes organic; show paid CAC separately |
| MER | Net revenue / total marketing spend | Platform ROAS is attributed and overstated; MER is ledger-based |
| Repeat rate | Customers with 2+ orders in window / customers with 1+ | State window (90 or 365 days) |
| LTV (margin-based) | AOV x gross margin % x orders per customer over horizon | Use margin, not revenue; cap horizon at 12-24 months |
| LTV:CAC and payback | LTV / CAC; months until cumulative contribution margin covers CAC | Payback matters more than ratio for cash-constrained stores |
| Inventory turns | COGS (12m) / average inventory at cost | Use cost, not retail |
| Days of inventory | Inventory / (COGS / 365) by SKU class | Dead stock hides in the average |
| Sell-through | Units sold / (opening units + received) over period | |
| Cash conversion cycle | DSO + DIO - DPO | DSO is near zero for card sales; payout lag is the real receivable |

## Procedure
1. Fix the period, currency and basis; pull the P&L and sales detail from the ledger.
2. **Reconcile revenue.** Store gross sales - discounts - refunds - tax - cancelled/unfulfilled (if recognised on shipment) = ledger net revenue. Explain any residual by timing (orders vs shipments), gift cards (liability until redeemed), and currency.
3. **Reconcile payouts.** Processor payouts = sales - refunds - fees - reserves - chargebacks; clearing account balance should equal funds in transit (see the platform reconciliation skills).
4. Compute the KPIs above; trend 13 months and show same-month prior year (seasonality).
5. Segment by channel, product class and new vs returning customer. Flag any segment with negative contribution margin.
6. Check marketing: platform-reported revenue vs ledger revenue by channel; if the sum of platform attributions exceeds ledger revenue, report MER, not ROAS.
7. Inventory: tie the valuation report to the GL; list SKUs over 180 days and their carrying value; reserve policy applied.
8. Commentary: top three movers in contribution margin with driver and action (see flux-variance-analysis).

## Edge cases
- Pre-orders and deposits: liability until shipped.
- Bundles: allocate price to components by relative list price for margin by product.
- Multi-currency: report constant-currency growth beside reported growth.
- Marketplace sales (fees netted by the marketplace): gross up revenue and fees, do not book net payouts as revenue.
- Returns after period end: estimate a returns reserve from historic rate.

## Do not
- Do not report ROAS from ad platforms as profitability.
- Do not use revenue-based LTV for spend decisions.
- Do not mix tax-inclusive store figures with tax-exclusive ledger figures.
- Do not change KPI definitions between periods without restating comparatives.

## Output
One page: KPI table (current, prior period, prior year, target), contribution-margin bridge, reconciliation block (store to ledger, payouts to bank), inventory ageing, and three commentary bullets with actions. Related: financial-reporting-pack, ecommerce-inventory-cogs, flux-variance-analysis.
