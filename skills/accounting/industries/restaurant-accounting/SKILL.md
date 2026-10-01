---
name: restaurant-accounting
description: >-
  Restaurant, cafe and bar accounting: POS-to-GL daily sales journal, tips and tip pooling, sales tax, prime cost (food, beverage, labour), inventory and theoretical vs actual food cost, delivery-app commissions, gift cards, comps/discounts, cash handling and multi-location reporting. Use when books for a restaurant group need to tie to the POS, or someone says "prime cost", "food cost percentage", "tip reporting", "delivery app payouts", "daily sales report", "comps and voids" or "restaurant P&L".
metadata:
  department: "accounting"
  domain: "industries"
  owner: "satva-coe"
  status: "beta"
  license: "Satva-original"
  source: "original"
---

# Restaurant accounting

Restaurants run on thin margins and high cash velocity. The ledger must reproduce the POS daily sales report exactly, then show prime cost (cost of goods plus labour) weekly, because by the time the monthly P&L arrives the problem is a month old.

## Step 1: Daily sales journal (one per location per day)

| Line | Side | Account |
|---|---|---|
| Food, beverage (beer/wine/liquor separately), retail, catering | Cr | Sales by category |
| Comps, discounts, promotions, voids (net) | Dr | Contra-revenue (comps/discounts) |
| Sales tax collected | Cr | Sales tax payable |
| Tips: card tips | Cr | Tips payable (liability) |
| Service charges / auto-gratuity | Cr | Revenue or tips payable per local law and who keeps it |
| Gift card sold / redeemed | Cr / Dr | Gift card liability |
| Cash, card, delivery-app, house account, paid-outs | Dr | Tender clearing accounts |
| Cash over/short | Dr or Cr | Cash over/short |

Post the journal from the POS end-of-day report; if the tender total does not equal sales plus tax plus tips, there is a missed line. Deposits then clear the tender accounts: bank cash deposits (with deposit slips) to cash clearing, card processor settlements to card clearing, delivery-platform payouts to platform clearing.

## Step 2: Tips and payroll

1. Card tips are owed to staff, net of card processing fee only if permitted by law; never retained by the business.
2. Tip pooling is allowed only among eligible employees (typically excluding owners and managers); document the formula and the approving law for the jurisdiction.
3. Tipped-wage credit and minimum-wage make-up: payroll must top up when tips plus cash wage fall below the minimum.
4. Report tips for payroll tax; reconcile Tips payable monthly to zero after payouts.
5. Service charges are not tips unless legally characterised that way; treat as revenue with wage and tax consequences.

## Step 3: Delivery apps and third-party platforms

Gross order value is revenue only where the restaurant is principal; commissions, marketing fees, and adjustments are expenses, not netted. Reconcile each payout to the platform's statement: orders, refunds, commissions, tax remitted by the platform, tip pass-through. Marketplace facilitator tax collected by the platform stays out of your tax payable.

## Step 4: Prime cost and inventory

- **Food cost %** = (opening inventory + purchases - closing inventory - transfers/staff meals adjustment) / food sales. Do the same for beverage, by sub-category.
- **Prime cost %** = (COGS + total labour including payroll taxes and benefits) / net sales. A well-run full-service operation aims at roughly 60 to 65 percent, quick-service lower; treat as a guide, not a rule.
- **Theoretical vs actual food cost:** theoretical = recipe cost x units sold from POS; the gap is waste, over-portioning, theft or unrecorded comps. Investigate any gap over 1 to 2 points.
- Weekly counts of high-value items (proteins, liquor) and monthly full counts; value at latest invoice cost; accrue unpaid deliveries.

## Step 5: Monthly close by location

1. Reconcile each tender clearing account, tips payable, gift card liability and sales tax payable to supporting reports.
2. Accrue rent, utilities, payroll, credit-card fees, delivery fees, linen and licence renewals.
3. P&L per location with prime cost, occupancy cost % (rent / sales), controllable expenses and four-wall EBITDA; consolidate for the group with intercompany management fees eliminated.
4. Review cash over/short by shift and by cashier; patterns matter more than totals.
5. Capitalise build-out and equipment above threshold; depreciate over the shorter of lease term and life; track pre-opening costs as expense.

## Failure modes

- Revenue booked from deposits, so tips, tax and timing contaminate sales.
- Tips mixed into revenue or held in operating cash.
- Delivery sales netted of commission, hiding the real cost of the channel.
- Food cost computed monthly only, with an approximate count.
- Gift cards recognised as revenue when sold.

## Output

Daily sales journal template, tender and liability reconciliations, weekly prime-cost report, theoretical-vs-actual food-cost analysis, location P&L and group consolidation.
