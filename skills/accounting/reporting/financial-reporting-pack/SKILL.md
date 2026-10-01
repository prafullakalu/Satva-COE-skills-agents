---
name: financial-reporting-pack
description: >-
  Build the management/board reporting pack: KPI definitions and formulas, budget vs actual, headline commentary, trend and rolling views, and the recurring pack structure. Use when asked for a "board pack", "monthly management report", "KPI dashboard definitions", "budget vs actual report", "investor update financials", or "what metrics should we track".
metadata:
  department: "accounting"
  domain: "financial-reporting"
  owner: "satva-coe"
  status: "beta"
  license: "Satva-original"
  source: "original"
---

# Financial reporting pack

Audience decides content. Board: 1-2 pages of conclusions plus appendix. Management: line-level detail. Lenders/investors: covenant and growth metrics. Numbers come from the locked period (month-end-close) and the statements (financial-statement-preparation).

## Pack structure (monthly)
1. **One-page summary:** 5-8 KPIs vs budget and prior year, traffic-light status, three sentences on what moved and what management is doing.
2. P&L: actual, budget, variance, prior year; YTD and full-year forecast.
3. Balance sheet and net debt/cash.
4. Cash: opening, movement by category, closing, 13-week outlook (cash-flow-forecasting).
5. Working capital: AR ageing, AP ageing, inventory.
6. Budget vs actual with commentary (flux-variance-analysis thresholds).
7. Forecast vs budget bridge: budget net income -> forecast net income by driver.
8. Risks, decisions needed, open items.

## KPI library (define each once; do not change definitions mid-year)
| KPI | Formula | Note |
|---|---|---|
| Gross margin % | (Revenue - COGS) / Revenue | Define whether freight/fees are COGS |
| Operating margin % | Operating income / Revenue | |
| EBITDA | Operating income + D&A | Label as non-GAAP |
| Current ratio | Current assets / Current liabilities | |
| Quick ratio | (Cash + receivables) / Current liabilities | |
| DSO | Average AR / Credit revenue x days in period | Use countback method if sales are seasonal |
| DPO | Average AP / COGS (or purchases) x days | |
| DIO | Average inventory / COGS x days | |
| Cash conversion cycle | DSO + DIO - DPO | |
| Burn / runway | Net monthly cash outflow; runway = cash / avg monthly burn | |
| Revenue growth | (Current - Prior) / Prior; also MoM and YoY | |
| Working capital | Current assets - current liabilities | |
| Debt service cover | Net operating income / debt service | Covenant metric |
| SaaS only: MRR/ARR, net revenue retention, churn %, CAC payback | state formulas in appendix | Align to revenue-recognition-606 for deferred revenue |
| E-commerce only: AOV, gross margin per order, return rate, inventory turns | COGS / average inventory | See ecommerce-inventory-cogs |

## Budget vs actual
- Budget version locked and labelled (original budget vs latest forecast). Report against both when forecast exists.
- Variance and F/U convention as in flux-variance-analysis. Show YTD variance beside month; a small monthly miss that repeats is a trend.
- Reforecast quarterly: actual YTD + forecast remainder = full-year outlook; explain delta to budget.
- Flexed budget for variable lines: budget unit cost x actual volume, to separate volume from efficiency.

## Quality gates
- Every number reconciles to the TB; totals foot and cross-foot.
- Same account mapping as prior packs; disclose any reclass.
- Charts only where they add value: trend lines for revenue, cash, margin; avoid pie charts for more than 4 slices.
- Commentary names drivers and actions, not restating the table.
- Reviewer sign-off before distribution; version and date on the cover.

## Do not
Do not show a KPI without its definition and period. Do not mix cash and accrual views on one page. Do not distribute preliminary numbers without a "draft" mark.

## Output
Pack in the format the audience uses (slide or document); data tables behind it; list of definitions and any changes since last pack.
