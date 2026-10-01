---
name: pricing-and-profitability-analysis
description: >-
  Product, service and customer profitability analysis and pricing review: contribution margin, cost allocation, break-even, price-volume-mix effects, discount leakage, customer and segment profitability, price increases and their break-even volume. Use when a client asks "which customers or products make money", "should we raise prices", "what is our break-even", "why did margin fall", or says "contribution margin", "profitability by customer", "price increase impact" or "discount analysis".
metadata:
  department: "accounting"
  domain: "advisory"
  owner: "satva-coe"
  status: "beta"
  license: "Satva-original"
  source: "original"
---

# Pricing and profitability analysis

Margins fail quietly: a few customers, a few SKUs and a creeping discount policy usually explain most of the leak. The method below finds them and prices the fix before it is proposed.

## Step 1: Build the profit unit

1. Choose the unit: product/SKU, service line, customer, channel, project or location. One analysis, one unit.
2. Pull revenue (net of discounts, returns, credits) and direct costs at that unit from the ledger and operational systems; reconcile the total to the P&L so nothing disappears.
3. Separate **variable** costs (materials, direct labour, freight, payment fees, commissions) from **fixed** costs (rent, salaried staff, software). Mixed costs are split by regression or judgement and disclosed.
4. Contribution margin = revenue - variable costs. Contribution margin % = CM / revenue.

## Step 2: Allocate overhead only where decisions need it

- For *keep or drop* and *price* decisions, use contribution margin; fixed costs are not avoided by dropping a unit unless they truly are.
- For *full-cost pricing* and long-term profitability, allocate shared costs with drivers (time, machine hours, orders, support tickets, floor area). Activity-based costing is worth the effort only when overhead is large and consumption differs materially across units.
- Show both views side by side: contribution margin and fully loaded margin.

## Step 3: Rank and segment

1. Pareto: sort units by contribution; the top 20 percent usually carry most profit and the tail includes loss-makers.
2. Quadrant: volume or revenue vs margin %: stars (high/high), cash cows (high volume/low margin), niche (low volume/high margin), dogs.
3. Customer profitability adds cost to serve: support time, discounts, payment terms (cost of financing = AR x rate), returns, customisation, shipping subsidies.
4. Check concentration: share of profit by top 5 customers; dependence on one channel.

## Step 4: Explain a margin change (price-volume-mix)

For each unit between periods:
- Price effect = (new price - old price) x new volume
- Volume effect = (new volume - old volume) x old margin per unit (at constant mix)
- Mix effect = change in the weighted-average margin from shifting between units
- Cost effect = change in unit cost x new volume
The four effects sum to the change in gross profit; if they do not, a unit is missing. Use `flux-variance-analysis` to explain the remaining movements.

## Step 5: Evaluate a price change

Break-even volume change for a price change x% with contribution margin m% (as a fraction of price): volume can fall by x / (m + x) before profit is lost (for a price increase). Example: 5 percent increase on a 40 percent margin product: 0.05 / (0.40 + 0.05) = 11.1 percent. For a price cut, required volume increase = x / (m - x).
Then test realism: elasticity from history or tests, competitor price points, contract terms and notice periods, customer segments that can bear the increase, bundling or tiering as alternatives, and the risk of churn among high-margin accounts.

## Step 6: Discount leakage

Compare list price to invoiced price by customer and sales rep; quantify the spread, approvals and exceptions; identify discounts that did not produce volume; set a discount-approval matrix and watch realised price monthly.

## Step 7: Recommendations

Format each as: finding, evidence, action (raise price, change terms, minimum order, reduce service, retire, bundle, renegotiate cost), expected annual profit effect (low/base), owner, timeline and risk. Prioritise by profit impact and ease.

## Failure modes

- Allocating all overhead and dropping a unit that actually covers fixed costs.
- Using gross margin when freight, returns and fees decide profitability.
- Analysing the wrong period (promotions, one-off orders).
- Ignoring cost to serve for customers.
- Recommending a price increase without checking elasticity and contracts.

## Output

Profitability table by unit with contribution and fully loaded margins, Pareto and quadrant view, price-volume-mix bridge, price-change scenario sheet with break-even volume, discount-leakage report, ranked action list.
