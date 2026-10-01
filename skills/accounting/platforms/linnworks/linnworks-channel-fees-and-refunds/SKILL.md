---
name: linnworks-channel-fees-and-refunds
description: >-
  Analyse refunds, returns, shipping charges and (where they exist) payment bank charges for Linnworks channels, and
  frame the marketplace fee analysis correctly: Linnworks does not hold marketplace fees, so fees must come from the
  channel settlement report. Use for "refund rate by channel", "returns vs refunds mismatch", "refunds not exported to
  accounting", "shipping charged vs shipping cost", "what did Amazon/eBay take in fees", "chargebacks", "marketplace
  fee percentage". Tools: getOrderRefunds, getReturns, getPayments, getOrderAdditionalInfo, getConsignments.
metadata:
  department: "accounting"
  domain: "ecommerce-analysis"
  platform: "linnworks"
  owner: "satva-coe"
  status: "beta"
  license: "Satva-original"
  source: "original"
---

# Linnworks channel fees, refunds and shipping

Prerequisite: `linnworks-mcp-operating-rules`. Fees are the headline gap: **Linnworks carries no marketplace fee,
commission, advertising or settlement data** (checked against all ~134 allowlisted tables). Do not estimate fees from
order totals and call it analysis. The skill's job is to quantify what Linnworks does hold (refunds, returns,
shipping, payment bank charges) and to set up the fee comparison against the settlement source.

## A. Refunds

`getOrderRefunds` reads `Order_Refund`: filters `order_id`, `created_from/to` (CreateDate), `actioned_from/to`
(ActionDate), `actioned` (true/false), keyset paged, newest CreateDate first. Useful columns: `Amount`, `Reason`,
`ReasonCategory`, `ChannelReason`, `RefundStatus`, `Actioned`, `AccountingExported`, `IsShippingRefund`,
`IsAdditionalRefund`, `IsChannelInitiated`, `CancellationQuantity`, `fkOrderItemId`, `RefundReference`.

Workflow:
1. Pull refunds for the period by `created_from/to`. Separately pull by `actioned_from/to`: a refund created in
   March and actioned in April is a March event by cause and an April event by cash. State which you report.
2. Split into **item refunds**, **shipping refunds** (`IsShippingRefund`), **goodwill/additional**
   (`IsAdditionalRefund`) and **channel-initiated** (`IsChannelInitiated`: the marketplace already took the money
   back, so Linnworks is recording, not causing it).
3. Join to channel: `getOrderBundle(order_id)` or `searchOrders(reference=..)` gives `source`/`sub_source`, currency
   and tax. Refund rate = refund value / sales value per channel and currency, both on the same date basis.
4. **Unactioned refunds** (`actioned=false`): requested but not paid. Liability at period end, not revenue reduction
   yet, unless the policy is to accrue.
5. **`AccountingExported` = false** older than the close date: refunds Linnworks never passed to its accounting
   integration. These are the classic cause of "ledger revenue higher than Linnworks net".
6. Tax on a refund: `Amount` is a gross figure. Refund tax comes from the original order lines
   (`getOrderItems`: `sales_tax`, `tax_rate`) pro-rated; flag partial refunds where the line split is unknown.

## B. Returns versus refunds

`getReturns(returned_from, returned_to, reason_prefix, scrapped, location)` reads `OrderItemReturn`: `return_qty`,
`reason`, `category`, `scrapped`, `refund_given`, `is_exchange`, `status`, `location_id`.

- A return is a stock event; a refund is a money event. Reconcile the two: returns with `refund_given=false` and no
  `Order_Refund` row are unrefunded returns (customer service issue and, for accounting, an unrecorded liability if
  the policy owes the refund). `Order_Refund` rows with no return are refunds without stock coming back.
- `scrapped=true` returns are inventory write-offs, not restocks: the stock side must expense them
  (see `linnworks-inventory-vs-ledger`).
- `is_exchange` is a swap, not a revenue reversal.
- Use `getOrderWithReturns(order_id)` to see a single order's chain.

## C. Shipping

- Revenue side: order `postage` and `PostageCostExTax` (`searchOrdersFull`), refunds with `IsShippingRefund`.
- Cost side: `getConsignments(order_id, generated_from/to, canceled)` and `getConsignmentPackages` show carrier
  consignments, `getManifests` the manifests; `listPostalServices` names the services. These show *what was shipped
  and by whom*; they carry no carrier invoice amount, so shipping margin needs the carrier invoice.
- Checks: shipping charged on orders with no consignment (not shipped or digital); consignments `canceled`;
  `Manifested=false` consignments still open at period end.

## D. Payment bank charges (the only fee-like field)

`getPayments(received_from/to, cleared_from/to, payment_type_id, currency_code, transaction_reference)` reads
`Accounting_Payment`: `Amount`, `BankCharges`, `Refunded`, `RefundBankCharges`, `DateReceieved`, `DateCleared`.
`getPaymentTypes` shows which bank each type lands in; `getBankMappings` maps channel (source/subsource) to bank.

- First test whether `BankCharges` is populated for this tenant at all (sum on a month). If it is zero everywhere,
  report "not captured", not "no fees".
- `DateCleared` null means funds not confirmed cleared: an unreconciled receivable, not cash.

## E. Marketplace fee analysis (framework, data from outside)

Obtain the channel settlement report for the same period (Amazon settlement flat file, eBay/PayPal/Managed Payments
transaction report, Shopify payout transactions). Then:

1. Match settlement lines to Linnworks orders on channel reference (`ReferenceNum` / `ExternalReference`;
   `searchOrders(reference=..)` matches prefix, leading `#` stripped).
2. Classify settlement lines: sale principal, shipping credit, tax collected by marketplace, referral/final-value
   fee, fulfilment (FBA) fee, storage fee, advertising, refund principal, refund commission returned, reserve
   hold/release, chargeback/claim, adjustment.
3. Compute per channel: fee % of principal = (referral + fulfilment) / principal. Compare with the channel's
   published rate card; a drift above rate-card tolerance means category/size mis-tier or promotion fees.
4. Orders in Linnworks but not in settlement (not yet paid out) and settlement lines with no Linnworks order are
   both reconciling items; list both sides.
5. Where marketplace remits VAT (facilitator regimes), sales tax in the settlement differs from Linnworks `fTax`;
   see `linnworks-to-ledger-posting-rules`.

## Output

Per channel and currency: gross sales, refunds (item, shipping, goodwill, channel-initiated), refund rate,
unactioned refunds, un-exported refunds, return/refund mismatches, shipping revenue vs consignment count, bank charges
(or "not captured"), and the fee table with source named as the settlement report. List what you could not obtain.
