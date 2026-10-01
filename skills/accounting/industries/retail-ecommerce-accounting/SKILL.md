---
name: retail-ecommerce-accounting
description: >-
  Retail and e-commerce accounting beyond inventory: sales-channel and payout reconciliation, marketplace and payment fees, returns and refunds, gift cards and store credit, loyalty programmes, discounts, shipping income and cost, sales tax by channel, and channel-level margin. Use when books for a shop, DTC brand or marketplace seller need to tie to Shopify/Amazon/POS/Stripe payouts, or someone says "payout doesn't match", "gift card liability", "returns reserve", "marketplace fees", "channel margin" or "POS to GL". Inventory costing is in ecommerce-inventory-cogs.
metadata:
  department: "accounting"
  domain: "industries"
  owner: "satva-coe"
  status: "beta"
  license: "Satva-original"
  source: "original"
---

# Retail and e-commerce accounting

The bank deposit is never the sales figure. Between an order and a payout sit refunds, fees, chargebacks, reserves, taxes collected for governments, and timing. This skill is the bridge. For stock valuation and COGS see `ecommerce-inventory-cogs`; for the platform mechanics see the platform skills under `platforms/`.

## Step 1: One clearing account per channel

1. Post each channel's gross sales, discounts, refunds, shipping, tax collected and fees to a **channel clearing account** (for example "Shopify clearing", "Amazon clearing", "POS card clearing").
2. Payouts and settlements then *clear* that account to the bank. A clearing balance that does not trend to near zero is the error alert.
3. Never post the payout straight to revenue; that double counts when sales are also posted from the order feed.

## Step 2: The standard daily/period entry (summary journal)

| Line | Side | Account |
|---|---|---|
| Gross product sales | Cr | Sales by channel/product line |
| Shipping charged | Cr | Shipping income |
| Discounts and promotions | Dr | Discounts (contra-revenue) |
| Sales tax collected | Cr | Sales tax payable (by jurisdiction) |
| Gift card redeemed | Dr | Gift card liability |
| Net received/receivable | Dr | Channel clearing |
| Refunds | Dr | Sales returns (contra-revenue); Cr clearing |
| Platform/payment fees | Dr | Merchant fees; Cr clearing |
| COGS for items shipped | Dr | COGS; Cr Inventory |

Summarise by day or settlement batch; keep order-level detail in the platform, referenced by batch ID. Post revenue at shipment or delivery per the control-transfer terms; cash received before shipment is a contract liability.

## Step 3: Reconcile payouts

For each payout: expected = sales - refunds - fees - chargebacks - reserve held + reserve released +/- adjustments. Compare to the bank line. Typical differences:
- Reserve or rolling holdback (Amazon, PayPal, Stripe): recorded as a receivable from the platform, released on schedule.
- Fee deducted from payout: booked to fees, not netted into revenue.
- Chargebacks and disputes: reverse revenue; record dispute fees; track win/loss.
- Currency conversion: gain or loss to FX, not to sales.
- Sales tax withheld and remitted by the marketplace (marketplace facilitator rules): remove from your payable, but keep the sale in gross revenue and in nexus analysis.

## Step 4: Returns, gift cards, loyalty

- **Returns reserve:** where return rates are material, estimate returns at sale (revenue reduced, refund liability recognised, asset for the right to recover goods at cost less expected impairment). Refresh the rate from the last 6-12 months of return history.
- **Gift cards and store credit:** a liability at issue; recognise revenue on redemption. Breakage is recognised only when the legal escheat and policy position supports it (proportionally with redemption pattern, subject to unclaimed-property law).
- **Loyalty points:** a separate performance obligation; defer the standalone value of points earned and recognise on redemption or expiry.
- **Discounts and coupons:** reduce the transaction price at sale; influencer and affiliate commissions are a selling expense, not a discount, unless paid to the customer.

## Step 5: Channel margin

Per channel: gross sales, less discounts and returns = net sales; less COGS = product margin; less fees, fulfilment, shipping net of income, and allocated advertising = contribution margin. Present both by channel and by top SKUs. Allocate ad spend by attributed channel, not evenly.

## Step 6: Sales tax

Register by nexus; map each product to a tax code; collect and report by jurisdiction. Reconcile the tax payable account to filed returns each period. Marketplace-collected tax stays out of your liability. Exempt and wholesale sales need certificates on file.

## Failure modes

- Posting payouts as revenue and also the order feed.
- Fees netted against sales so margin looks higher.
- Gift card sales recorded as revenue.
- Clearing accounts left to grow with unexplained residue.
- Refund liability ignored at year-end (large Q4, returns in Q1).

## Output

Channel clearing reconciliation with open items, summary journal template, returns/gift card/loyalty schedules, and a channel contribution-margin report.
