---
name: shopify-payout-reconciliation
description: >-
  Reconcile Shopify sales to Shopify Payments (and other gateway) payouts and bank deposits: build the order-level
  gross-to-net bridge, match payouts to bank lines, explain fees, refunds, chargebacks, reserves and timing, and keep
  the Shopify clearing account at zero. Use for "reconcile Shopify payouts", "payout does not match the bank",
  "Shopify clearing account", "why is the deposit lower than sales", "Shopify fees", "chargeback on a Shopify order".
  Needs the user's payout/transactions export because the read-only MCP has no payout or fee tools.
metadata:
  department: "accounting"
  domain: "ecommerce-reconciliation"
  platform: "shopify"
  owner: "satva-coe"
  status: "beta"
  license: "Satva-original"
  source: "original"
---

# Shopify payout reconciliation

Prerequisite: `shopify-mcp-operating-rules`. Be explicit with the user at the start: the read-only MCP **cannot see
payouts, balance transactions or processing fees**. It can supply the order side (orders, transactions, refunds); the
payout side must be a file the user exports from Shopify Payments (Payouts report, or "Transactions" export per
payout) and the bank statement. Never reconstruct fees from order totals.

## The model

```
Orders (gross, incl. tax and shipping)
  - refunds
  - processing fees (rate + fixed, per transaction)
  - chargebacks and dispute fees
  +/- adjustments and reserves
  = payout amount (what lands in the bank)
```
Every payout is a bundle of balance transactions: charge, refund, adjustment, dispute, fee, reserve, payout itself.
The reconciliation proves each payout equals the sum of its bundle, and each bundle line ties to an order or to a
named non-order event.

## Workflow

1. **Inputs.** Payout export (payout id, date, amount, currency, status), per-payout transaction detail (type, order
   name, amount, fee, net), bank statement lines for the period, and ledger Shopify clearing account movement.
   Record store, shop currency, and period.
2. **Pull the order side.** For the payout window (payout covers transactions up to a few days earlier), page
   `get-orders` with `query: "processed_at:>=... processed_at:<..."` (or `created_at`) and `status: any`. Keep
   `name`, `displayFinancialStatus`, `totalPriceSet`, `totalTaxSet`, `totalShippingPriceSet` (shopMoney).
   Mind the 60-day order window and nested caps (see operating rules).
3. **Payment detail per order only where needed.** `get-order-transactions(orderId)` returns `kind`
   (authorization, sale, capture, refund, void), `status`, `gateway`/`formattedGateway`, `amountSet`, `processedAt`,
   `errorCode`, `test`, `parentTransaction`, card company, and `receiptJson`. Use it to:
   - split gateways (Shopify Payments, PayPal, manual, gift card, store credit, COD): each gateway pays out
     differently and needs its own clearing account;
   - confirm capture happened (an authorised but uncaptured transaction is not revenue cash);
   - find `test: true` transactions to exclude.
   `receiptJson` is gateway-specific raw data; inspect one example before relying on any field in it.
4. **Match bundle to orders.** In the payout transaction detail, each charge/refund line has an order name. Join on
   order name. Output three lists: (a) payout lines with no order, (b) captured orders with no payout line yet,
   (c) amount mismatches (partial capture, currency conversion).
5. **Prove each payout:** sum of net lines = payout amount to the cent. If not, the missing delta is a reserve,
   adjustment or timing, never a plug.
6. **Match payouts to the bank.** One bank line per payout. Payout date vs bank date differ by processing days;
   a payout "paid" but not in the bank is a bank-side exception; a bank line with no payout may be a different
   gateway (PayPal) or a manual deposit.
7. **Clearing account.** Ledger Dr clearing for sales as recorded (by the integration or journal), Cr clearing for
   fees, refunds, chargebacks, Cr clearing / Dr bank for payouts. Closing balance should equal sales captured but not
   yet in a payout, less fees and refunds on them. Anything else is unexplained.
8. **Report.**

## Proposed journals (to be posted by a human or other system)

| Event | Dr | Cr |
|---|---|---|
| Gross sales (if not already booked by sync) | Shopify clearing | Sales, Output tax, Shipping income |
| Processing fees | Payment processing fees | Shopify clearing |
| Refund | Sales returns, Output tax | Shopify clearing |
| Chargeback (lost) | Chargebacks expense | Shopify clearing |
| Dispute fee | Bank and dispute fees | Shopify clearing |
| Payout | Bank | Shopify clearing |
| Reserve held | Reserve receivable | Shopify clearing |
Fees on refunded orders: Shopify typically does not return the fixed fee; confirm in the export, not by assumption.

## Timing and edge cases

- Orders in period but payout after period end: remain in clearing; this is normal, quantify it.
- Chargebacks arrive weeks later against an old order: book when the dispute is lost (and fee when charged).
- Refund in month N+1 of a month N sale: reduces N+1 cash; revenue reversal period follows policy.
- Multi-currency: Shopify Payments pays out in the payout currency; presentment currency differences show as
  conversion in the transaction detail. Post FX difference separately.
- Gift card and store-credit tenders reduce cash received but not sales; see `shopify-gift-cards-and-store-credit`.
- Manual payment methods (bank transfer, COD) have no payout; they reconcile to the bank directly, outside this flow.
- Draft orders marked paid are in `get-draft-orders`; they can create sales without an online gateway.
- Shopify "paid" status on the order is not the same as funds received: payout status `in_transit` or `scheduled`
  is not in the bank yet.

## Output

Per payout: id, date, amount, bundle sum, difference (should be zero), unmatched lines. Period summary: gross sales,
refunds, fees, chargebacks, reserve movement, payouts, closing clearing, items awaiting payout. Exceptions with order
names (never customer details), and the proposed journals.
