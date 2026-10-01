---
name: shopify-gift-cards-and-store-credit
description: >-
  Account for Shopify gift cards and store credit: sale of a card as a liability (not revenue), redemption as
  tender, breakage and unclaimed-property rules, store credit issued on refunds, and how to find these in order data
  with the read-only Shopify MCP. Use for "gift card liability", "gift card sales are in revenue", "store credit
  refunds", "gift card redemption reconciliation", "breakage income", "Shopify tender types". Be clear that the MCP
  has no gift-card balance or store-credit tool; liability balance comes from the Shopify admin report.
metadata:
  department: "accounting"
  domain: "ecommerce-liabilities"
  platform: "shopify"
  owner: "satva-coe"
  status: "beta"
  license: "Satva-original"
  source: "original"
---

# Shopify gift cards and store credit

Prerequisite: `shopify-mcp-operating-rules`. Two limits to state up front:
1. The read-only MCP cannot list gift cards, their balances, or store-credit account balances (no such tool, and no
   `read_gift_cards` or store-credit scope in the granted list). `get-shop-info` only shows `features.giftCards`
   (feature on/off).
2. What it can see is the *order side*: line items that are gift cards, and payment transactions whose gateway
   shows a gift card or store credit tender. Inspect `gateway` / `formattedGateway` on a known order first; do not
   assume the exact gateway strings [Likely: gift_card for gift-card tender; store-credit tender naming varies, verify].

## Accounting principles

- **Selling a gift card is not a sale.** Cash received creates a liability (deferred revenue). Dr Bank/clearing, Cr Gift
  card liability. No output VAT/sales tax at sale in most regimes (single-purpose vouchers can differ: confirm
  with the tax adviser). Revenue is recognised when the card is redeemed against goods.
- **Redemption.** The order is a normal sale of goods with tax, tendered partly or wholly by gift card:
  Dr Gift card liability (and Dr clearing for any cash portion), Cr Sales, Cr Output tax. Order totals still equal the
  goods value; cash received is lower.
- **Store credit** issued instead of a cash refund: Dr Sales returns (and output tax), Cr Store credit liability.
  Used later like a gift card. Store credit is a liability of the same nature; keep a separate sub-account because
  expiry and legal treatment differ.
- **Breakage** (cards never redeemed): recognise income only as permitted by policy and law. Many jurisdictions
  treat unredeemed balances as unclaimed property (escheat) after a dormancy period, in which case the liability
  moves to the authority, not to income. Never book breakage without a documented policy and jurisdiction check.
- **Promotional cards** issued free (compensation, marketing): no liability until the promotion is a binding
  obligation; expense (marketing) when issued if redeemable, per policy. Distinguish them from paid cards.
- **Gift card purchased with a gift card** is rare but exists; avoid circular liabilities.
- **Refund of an order paid by gift card** returns value to the card or to store credit, not the bank.

## Workflow

1. **Policy.** Collect: expiry rules, breakage policy, jurisdiction, whether cards are sold in other channels
   (POS, marketplace) and which system holds the master balance.
2. **Cards sold in the period.** `get-orders` for the period (query by date), line items whose `title` indicates a gift
   card (line items are capped at 10 per order; use `get-order-by-id` where needed). Sum their `originalTotalSet`.
   Confirm each such order carries no sales tax and that the revenue account did not receive them.
3. **Redemptions in the period.** For the paid orders, `get-order-transactions` and count transactions with a gift
   card or store-credit gateway; sum `amountSet.shopMoney`. This is a per-order call: select orders with a
   gift-card tender hint (Shopify's order search has a payment-gateway-name filter, for example
   `query="payment_gateway_names:gift_card"`; this has not been tested through the MCP, so confirm it returns results on a
   known order before relying on it, otherwise scan transactions for the period).
4. **Liability roll-forward** (the control):
   `opening balance + cards sold + store credit issued - redemptions - expiries/breakage recognised - transfers to
   escheat = closing balance`. Closing balance must equal the Shopify admin gift-card report (Gift cards page,
   outstanding balance export) at the same date. That report is a file from the user, not an MCP output.
5. **Refund flows.** `get-order-refund-details`: refund transactions with gift-card/store-credit gateway or a refund
   with no bank leg indicate store credit or card reload. Post to the store-credit liability, not to bank.
6. **Reconcile.** Compare ledger liability to the admin report; differences are usually (a) cards sold but booked as
   revenue, (b) redemptions booked as bank receipts, (c) promotional cards counted as paid, (d) cards sold at POS
   or other channels, (e) expired cards released too early.
7. **Tax.** Verify no tax was charged at card sale and that tax was charged on the redeeming order; the order's
   `totalTaxSet` includes tax on the full goods value, not just the cash portion.

## Traps

- Reporting "revenue" from cash received per payout includes gift card sales and excludes redemption value:
  revenue is simultaneously overstated (card sales) and understated (gift-tendered orders). Build revenue from
  order totals, tender from transactions.
- Payouts exclude gift-card and store-credit tender (no cash moves). A reconciliation that expects order total =
  payout will always be short by the gift-card portion.
- Foreign currency cards: balance held in shop currency; presentment differences produce FX noise.
- Shopify store credit may be per-customer account; there is no MCP view of balances, so customer-level
  reconciliation cannot be done from the MCP.
- Do not move liability to income at year-end to "tidy up".

## Output

Liability roll-forward with sources per line; list of gift-card line items booked to revenue; redemption count and
value; refunds to store credit; reconciliation to the admin report (or an explicit "report not provided"); policy
questions still open (breakage, escheat, expiry).
