---
name: flux-variance-analysis
description: >-
  Flux (period-over-period) and budget-vs-actual variance analysis with thresholds, price/volume/mix decomposition, driver commentary and unexplained-variance escalation. Use when asked for "flux analysis", "variance commentary", "why did expenses go up", "budget vs actual", "explain the P&L movement", or when reviewing a trial balance before lock.
metadata:
  department: "accounting"
  domain: "period-close"
  owner: "satva-coe"
  status: "beta"
  license: "Satva-original"
  source: "original"
---

# Flux and variance analysis

Purpose: find errors and explain real movement before numbers go to management. A variance with no explanation is an open question, not a finished review.

## Set up
1. Pick comparisons: current vs prior month, vs same month last year (seasonality), vs budget/forecast, and YTD vs prior YTD. Always use the same entity, currency and account mapping; re-map if the chart of accounts changed.
2. Thresholds: investigate a line if BOTH `|variance| > absolute floor` AND `|variance %| > percent threshold`. Defaults: P&L lines 10% and 1,000 (base currency units; scale to entity size); balance sheet lines 10% and 5,000; always investigate any line crossing sign, any new account, any account that went to zero, and any account over 1% of revenue with movement above 5%. Set these in writing and keep them stable.
3. Formulas:
   - Variance = Actual - Comparison. Variance % = Variance / |Comparison|.
   - Favourable/unfavourable: revenue and income up = F; expense up = U. State the convention in the header.
   - Common-size: line / revenue to spot margin movement even when absolutes look fine.

## Decompose, then explain
- **Revenue:** Volume effect = (Actual qty - Base qty) x Base price. Price effect = (Actual price - Base price) x Actual qty. Mix = change in average price caused by product shift; compute residual after price and volume. Check with FX effect for multi-currency sales (constant-currency view).
- **COGS/gross margin:** margin % movement split into price, input cost, mix, shrinkage, freight, discounts.
- **Payroll:** headcount x average cost, plus one-offs (bonus, severance, backpay), plus timing (pay-period count: months with 3 pay dates in bi-weekly payroll).
- **Opex:** one-off vs recurring; timing (annual invoice expensed vs prepaid); reclass between accounts; vendor price change; new contract.
- **Balance sheet:** AR (DSO change, large unbilled, bad debt), inventory (days on hand, reserve), AP (DPO, payment run timing), deferred revenue (billings vs recognition), accruals (reversal missing = doubled expense).

## Driver commentary standard
Each explained line: what changed (number and %), why (specific driver with evidence: invoice, contract, headcount list, event), is it recurring or one-off, action or forecast impact. Reject commentary like "timing", "higher activity", "per management" without a document or a number.

Example good: "Software subscriptions +4,200 (+38%): annual renewal of design licence invoiced Mar, expensed in full instead of prepaid over 12 months. Reclass 3,850 to prepaid; recurring impact +350/month."

## Error tests while you review
- Duplicate postings (same amount, vendor, date); missing reversal of last month's accrual; expense posted to revenue accounts or sign flipped.
- Recurring entry missing (rent, depreciation, subscription revenue) or doubled.
- Unusual round amounts, weekend postings, entries by users who do not usually post.
- Month with zero activity in an account that is normally active.

## Escalation
Unexplained after one working day, or explanation reveals an error: owner reposts correction, reviewer re-runs the flux, and the original variance and its resolution stay in the file. Variances over 2x the threshold with no support go to the controller before the period locks.

## Do not
- Do not explain a variance by the account name ("travel was up because travel expense increased").
- Do not net offsetting variances inside a subtotal; test at account level, then at subtotal.
- Do not change thresholds mid-year to avoid investigations.

## Output
Table: account | current | comparison | variance | variance % | F/U | explanation | evidence ref | reviewer. Followed by: top 5 drivers of net-income change, list of errors corrected, open items.
