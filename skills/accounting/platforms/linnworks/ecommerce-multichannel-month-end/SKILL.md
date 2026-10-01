---
name: ecommerce-multichannel-month-end
description: >-
  Month-end close checklist and runbook for a multichannel e-commerce client (Linnworks plus marketplaces, Shopify
  and PSPs): freeze the basis, pull and prove sales per channel, reconcile each channel clearing account to its
  settlement and payout, book fees, refunds, chargebacks and reserves, reconcile inventory, check VAT/OSS and FX, and
  sign off. Use for "e-commerce month-end", "close the books for the Amazon/eBay/Shopify client", "channel clearing
  does not clear", "what do I check before the VAT return". Orchestrates the other Linnworks and Shopify skills.
metadata:
  department: "accounting"
  domain: "ecommerce-close"
  platform: "linnworks,shopify"
  owner: "satva-coe"
  status: "beta"
  license: "Satva-original"
  source: "original"
---

# E-commerce multichannel month-end

Generic close discipline lives in the core `month-end-close` skill. This runbook adds what is specific to channel
businesses. It assumes the read-only Linnworks MCP and, where Shopify is a channel, the read-only Shopify MCP; neither
can post, so every output is a proposed journal or a finding for a human to action.

## Phase 0: freeze the basis (day 1)

Write down, per channel, and keep in the client file:
- Revenue basis: order date or dispatch date (one choice for all channels).
- Time zone and period boundaries (Shopify `ianaTimezone` from `get-shop-info`; Linnworks times as stored).
- Tax regime per channel: who collects and remits; OSS scope.
- Clearing account, fee accounts, reserve account and FX policy per channel.
- Systems of record: Linnworks for orders and stock, channel/PSP for money.
If any is unknown, that is the first question to the client, not an assumption.

## Phase 1: sales proof

1. Per channel and currency: Linnworks totals (`getChannelBreakdown`), Shopify totals where the store is a channel
   (`get-orders` with a `query` date filter, paged). Skills: `linnworks-order-and-stock-analysis`,
   `shopify-sales-tax-and-refunds`.
2. Tie to the ledger sales accounts. Differences usually are: wrong date basis, tax-inclusive vs exclusive, cancelled
   or test orders, orders imported twice (same reference on two channels), Shopify-origin orders flowing through
   Linnworks AND the Shopify-to-ledger sync (double sales).
3. Duplicate check: the same `ExternalReference` appearing twice in `searchOrders` for the period.

## Phase 2: channel clearing accounts

For each channel and each PSP:

| Line | Opening clearing | + Sales (gross) | - Fees | - Refunds | - Chargebacks | +/- Reserve | - Payouts | = Closing |
|---|---|---|---|---|---|---|---|---|

Closing must equal sales not yet paid out less their fees and expected refunds. Tools by source:
- Marketplace money: settlement reports (outside the MCPs).
- Shopify Payments: payout CSV/export plus `get-order-transactions` for orders; see `shopify-payout-reconciliation`.
- Linnworks refunds: `getOrderRefunds`, `linnworks-channel-fees-and-refunds`.
Unmatched items go to a reconciling list with age. Anything older than the channel's payout cycle plus a tolerance
(commonly 14 to 30 days) is an exception for the client, not an accrual to hide.

## Phase 3: fees, refunds, chargebacks

1. Fees booked per settlement period; check fee % against the channel's rate card per category.
2. Refund rate by channel versus prior months; spike = product or fulfilment issue, or a late-booked batch.
3. Unactioned refunds and returns not refunded: accrue per policy.
4. Chargebacks and disputes: open disputes are contingent; lost ones are expense.
5. Gift cards and store credit liability (Shopify): `shopify-gift-cards-and-store-credit`.

## Phase 4: inventory and COGS

`linnworks-inventory-vs-ledger` (Linnworks) and `shopify-inventory-vs-ledger` (Shopify). Confirm stock-take
adjustments, scrapped returns, goods received not invoiced and in-transit transfers. COGS follows the same basis as
revenue (see `linnworks-to-ledger-posting-rules`).

## Phase 5: tax and FX

1. Output tax: ledger tax account versus order tax by channel; remove marketplace-remitted tax.
2. OSS: tax by destination country ties to the OSS work paper; domestic VAT account excludes OSS supplies.
3. Input VAT on fees: marketplace fee invoices carry VAT depending on the seller's and marketplace's country; check
   the invoice, not the settlement line.
4. FX: realised differences on payouts posted; open clearing balances in foreign currency revalued.

## Phase 6: sign-off checklist

- [ ] Every channel and PSP clearing balance reconciled, exceptions listed with age and owner
- [ ] Sales per channel tie to ledger within tolerance; reasons for each difference
- [ ] Fees, refunds, chargebacks recorded in the correct period
- [ ] Inventory reconciliation done, negative stock and zero-cost SKUs reported
- [ ] Tax liabilities (VAT, OSS, sales tax) reconciled and flagged items resolved
- [ ] Gift card/store credit liability agreed to the platform report
- [ ] Reserve and payout timing differences explained
- [ ] Completeness lines present: no throttled or truncated pull behind any figure
- [ ] Proposed journals listed with source references; nothing posted by the tooling

## Cadence

Weekly for high-volume clients: clearing balance and unmatched payouts only (15 minutes). Month-end: everything above.
Quarter-end: add VAT/OSS filing reconciliation and an inventory provision review.

## Do not

- Close with a clearing account that carries unexplained balances "to be cleared next month".
- Use payout amounts as the revenue source.
- Reconcile in net-of-fees terms; reconcile gross, fee, refund and payout separately.
