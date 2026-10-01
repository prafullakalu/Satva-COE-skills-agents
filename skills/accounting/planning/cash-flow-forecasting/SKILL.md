---
name: cash-flow-forecasting
description: >-
  Build and maintain a cash-flow forecast: 13-week direct method forecast, 12-month indirect projection, collection and payment timing assumptions, scenarios, minimum cash and runway, and forecast-vs-actual tracking. Use for "13-week cash flow", "cash forecast", "will we run out of cash", "runway", "when will we have cash to pay X", "cash flow projection for a loan".
metadata:
  department: "accounting"
  domain: "financial-reporting"
  owner: "satva-coe"
  status: "beta"
  license: "Satva-original"
  source: "original"
---

# Cash-flow forecasting

Two views: **13-week direct** (receipts and payments, weekly, for liquidity management) and **12-month indirect** (from forecast P&L and balance sheet, for planning, covenants, going-concern). Start from reconciled opening cash (bank recs complete) and AR/AP agings.

## 13-week direct forecast
Weekly columns, rolling: drop week 1 as it closes, add week 14.

**Opening cash** (per bank, not per ledger; list outstanding items)
**Receipts**
- Collections of existing AR: by invoice, expected pay date = due date + customer's historical days late (use the customer's average, or bucket: current 95% collected within terms + 5 days; 1-30 days late 85%; 31-60 days 60%; over 60 days only if confirmed). Sum of probability-weighted amounts.
- New sales: forecast billings x collection curve (e.g. 30% in week of terms, 50% next, 20% the rest), or cash sales by day.
- Other: tax refunds, grants, loan drawdowns, asset sales, payment-processor payouts (T+2 to T+7 and reserve holds).
**Disbursements**
- AP by bill: pay date per payment-run policy, early-pay discounts, critical vendors first.
- Payroll and payroll taxes on actual dates (payroll-accounting); benefits; contractor payments.
- Rent, loan repayments, interest, insurance, subscriptions, sales tax/VAT payments (sales-tax-vat-gst-compliance), income-tax instalments (estimated-tax-and-tax-prep-organiser), capex, owner draws/dividends.
- Inventory purchases: PO schedule with deposits and balance dates (ecommerce-inventory-cogs).
**Net cash flow, closing cash, minimum cash buffer, headroom** (closing cash - minimum cash; plus undrawn facilities available).
Minimum cash: at least 2-4 weeks of operating disbursements, or the covenant/bank requirement if higher.

## 12-month indirect forecast
Forecast P&L (revenue drivers, margin, opex by line) -> adjust: + depreciation/amortisation, +/- change in AR (using DSO), inventory (days on hand), AP (DPO), accruals, deferred revenue, - capex, +/- debt drawn and repaid, tax, dividends -> closing cash. Balance sheet must balance each month (build a three-statement link; a forecast that does not balance has hidden errors). Seasonality: use same-month history for sales and working capital.

## Scenarios
Base, downside, upside. Downside typical levers: revenue -10 to -20%, collections delayed 10-15 days, a top-3 customer lost, supplier terms tightened, cost inflation. Show the week/month cash first breaches the minimum and the actions available (pay-run deferral, financing, cost cuts), with lead time for each. Reverse stress test: what revenue decline exhausts cash within 12 months?

## Metrics
Runway (months) = cash / average monthly net burn (use trailing 3 months and forecast burn); Burn multiple = net burn / net new ARR (SaaS); Cash conversion cycle = DSO + DIO - DPO; Interest cover and covenant tests projected.

## Forecast discipline
- Single owner, updated weekly (13-week) and monthly (12-month); versions saved.
- Variance tracking: forecast vs actual receipts and payments by line each week; accuracy = 1 - |actual - forecast| / forecast. Persistent bias (always optimistic collections) is corrected in assumptions.
- Every assumption documented with source (contract, history, management decision). Distinguish committed items (signed orders, due bills) from estimated.
- Reconcile week-1 actual closing cash to bank before rolling.
- Foreign currency flows converted at a stated rate with sensitivity.

## Do not
Do not forecast from the P&L alone for liquidity (timing differences dominate); do not assume invoices are paid on due date; do not hide a shortfall by netting receipts and payments; do not include uncommitted financing as available cash.

## Output
13-week table and chart, 12-month projection, scenario comparison, assumptions list with owners, covenant/runway summary, and forecast-accuracy log.
