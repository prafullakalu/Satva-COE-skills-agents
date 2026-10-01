---
name: shopify-sales-tax-and-refunds
description: >-
  Analyse Shopify sales, discounts, shipping, sales tax/VAT and refunds/returns for a period with the read-only
  Shopify MCP, and tie them to the ledger: gross-to-net bridge per order, tax-inclusive versus exclusive stores,
  refund and return reconciliation, cancelled and partially refunded orders, restock and write-off effects. Use for
  "Shopify sales tax report for March", "refunds by month", "does Shopify revenue match the ledger", "VAT collected
  on Shopify", "partial refund tax", "returns not refunded". Tools: get-orders, get-order-by-id,
  get-order-refund-details, get-returns, get-shop-info.
metadata:
  department: "accounting"
  domain: "ecommerce-tax"
  platform: "shopify"
  owner: "satva-coe"
  status: "beta"
  license: "Satva-original"
  source: "original"
---

# Shopify sales, tax and refunds

Prerequisite: `shopify-mcp-operating-rules` (nested caps, paging, 60-day window, rate limits). Tax rates and filing
treatment depend on jurisdiction; this skill finds and explains the numbers, and does not give tax advice.

## What each tool gives you

| Need | Tool | Fields that matter |
|---|---|---|
| Orders in a window | `get-orders(status, query, limit, after, sortKey)` | `name`, `createdAt`, `displayFinancialStatus`, `totalPriceSet`, `subtotalPriceSet`, `totalShippingPriceSet`, `totalTaxSet` (all `shopMoney`), line items (first 10 only) |
| One order in depth | `get-order-by-id` | adds `currentTotalPriceSet`, `discountCodes`, `cancelReason`, `cancelledAt`, `returnStatus`, `processedAt`, billing address, metafields; lines capped at 20 |
| Refunds | `get-order-refund-details(orderId)` | per refund: `totalRefundedSet`, refund lines (`quantity`, `restockType`, `restocked`, `subtotalSet`, `totalTaxSet`, `location`), refund transactions (gateway, status), `duties` |
| Returns | `get-returns(orderId)` (returns hang off an order), `get-return-by-id` | `status`, `totalQuantity` |
| Store tax settings | `get-shop-info` | `taxesIncluded`, `taxShipping`, `currencyCode`, `ianaTimezone` |
| Discount definitions | `get-discounts` | titles, status, codes (not usage amounts) |

There is no tax-line breakdown by jurisdiction in these tools; `totalTaxSet` is a single figure per order.
Jurisdiction-level tax (state, county, EU country) needs the Shopify Taxes report export.

## Workflow 1: gross-to-net sales bridge

1. `get-shop-info`: note `taxesIncluded` and `taxShipping`. If `taxesIncluded` is true, product prices already
   contain tax and `subtotalPriceSet` follows that; the bridge below changes accordingly.
2. Page `get-orders` for the period with a `query` such as
   `created_at:>=2026-03-01 created_at:<2026-04-01` (state it on the report), `status: any`. Choose `created_at`
   (order date) or `processed_at` once, matching the ledger basis. Page to `hasNextPage` false.
3. Per order bridge (shop currency):
   `total = subtotal(after discounts) + shipping + tax` (when taxes are exclusive). Test this on five orders with
   `get-order-by-id`; if the identity fails, discounts, duties, tips or rounding are in play: investigate before
   aggregating.
4. Exclude or isolate: `cancelledAt` set, `displayFinancialStatus` voided/pending/authorized (not paid), test
   orders (tag or `test` transaction), draft orders not completed.
5. Aggregate per day and month: gross sales (subtotal + discounts added back if the ledger records gross with a
   discount contra), discounts, shipping, tax, total. Tie each line to a ledger account.
6. Compare to the ledger: sales, shipping income, output tax, discounts. Residual differences are listed by cause
   (date basis, refund timing, cancelled, double-synced).

Verification gate: any order whose `lineItems` count is exactly 10 (via `get-orders`) is possibly truncated; if you
need line-level analysis, re-read with `get-order-by-id` (cap 20) and mark orders with more lines as incomplete.

## Workflow 2: tax collected

- Sum `totalTaxSet` for paid, non-cancelled orders = tax charged at order time, before refunds.
- Net tax = tax charged - tax on refunds (`refundLineItems.totalTaxSet`). Tax on a shipping-only refund is not in
  those lines; derive it from the refund amount and the order's shipping tax rate, and mark it as derived. Keep refunds in their *refund* period for the return unless filing rules say otherwise.
- Tax-inclusive store: tax is extracted from the price, so revenue ex-tax = gross - tax. Booking gross as revenue is the
  classic overstatement.
- Orders imported into Shopify from another channel: these tools do not expose the sales channel, so use `tags` and
  `note` from `get-orders`, and confirm per channel whether the tax is yours to remit.
- Cross-border (EU OSS, UK, Canada, US states with economic nexus): destination from shipping address
  (`get-orders` returns `shippingAddress.country`, `provinceCode`, `zip`). Build the country/state summary and hand it to
  the tax preparer; do not assign rates yourself.

## Workflow 3: refunds and returns

1. For each paid order in the window with `displayFinancialStatus` refunded or partially refunded (use
   `query: "financial_status:refunded OR financial_status:partially_refunded"`), call
   `get-order-refund-details`. Respect the throttle: fetch only those orders.
2. Per refund: amount (`totalRefundedSet`), items and `restockType` (return, cancel, no_restock), `restocked`,
   tax on lines, and the refund transaction gateway.
3. Classify: item return (stock back), cancellation before shipment, no-restock refund (goodwill, damaged,
   not-returned), shipping-only refund, discount adjustment.
4. Ledger effect: Dr sales returns and Dr output tax, Cr clearing/bank. Restocked items also Dr Inventory, Cr COGS at
   original cost (cost from `get-inventory-items.unitCost` is merchant-entered; prefer ledger cost). `no_restock`
   refunds do not restore stock.
5. Returns without refunds: `get-returns(orderId)` status open/closed with no refund transaction = refund owed or
   exchange. `get-orders` `returnStatus` via `get-order-by-id`.
6. Flag any order whose cumulative refunds exceed its order total.
7. Timing: refunds processed after period end are a next-period event; refunds requested but not issued are
   not in Shopify at all (check support backlog with the client).

## Edge cases

- **Order edits** after payment change totals; `currentTotalPriceSet` vs `totalPriceSet` difference = net edits and
  refunds.
- **Partial shipment/partial refund** on mixed-tax baskets: allocate refund tax by line, not by order proportion.
- **Presentment vs shop currency:** use shop currency for ledger, note FX.
- **Duties and import taxes** (`duties` in refunds) are not VAT; separate account.
- **Tips** and **gift-card sales** are not revenue; see `shopify-gift-cards-and-store-credit`.
- **Free orders** (100 percent discount) have zero cash; they still carry COGS and need an expense treatment of the
  promotion (marketing or contra revenue by policy).
- **Cancelled-after-capture** orders: money returns via refund; check a refund exists.

## Output

Monthly table: orders, gross, discounts, shipping, net sales, tax charged, refunds (value, tax, count, restocked vs not),
net tax; reconciliation to ledger lines with each difference named; list of incomplete orders (capped lists),
list of unrefunded returns, plus notes on tax-inclusive/exclusive handling and the exact `query` strings used.
