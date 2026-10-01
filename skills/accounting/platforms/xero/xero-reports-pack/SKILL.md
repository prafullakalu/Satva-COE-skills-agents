---
name: xero-reports-pack
description: >-
  Pulls and interprets Xero financial reports through the Satva Xero MCP: profit and loss, balance sheet, trial
  balance, bank summary, executive summary, aged receivables/payables per contact, budget comparison, with correct
  dates, periods, tracking filters and a tie-out between reports. Use for "P&L from Xero", "balance sheet at 30
  June", "trial balance", "management pack", "aged receivables", "compare this month to last", "report for each
  department/tracking option", "why don't the reports agree".
metadata:
  department: "accounting"
  domain: "reporting"
  platform: "xero"
  owner: "satva-coe"
  status: "stable"
  license: "Satva-original"
  source: "original"
---

# Xero reports pack

Follow `xero-mcp-operating-rules`. Report tools are read-only and safe, but each call counts toward the rate limit.

## Tool map (verified parameters)

| Need | Tool | Parameters |
|---|---|---|
| Profit and loss | `list-profit-and-loss` | `fromDate`, `toDate`, `periods`, `timeframe` MONTH/QUARTER/YEAR, `standardLayout`, `paymentsOnly` |
| Balance sheet | `list-report-balance-sheet` | `date`, `periods`, `timeframe`, `trackingOptionID1`, `trackingOptionID2`, `standardLayout`, `paymentsOnly` |
| Trial balance | `list-trial-balance` | `date`, `paymentsOnly` |
| Bank summary | `list-report-bank-summary` | `fromDate`, `toDate` (scope-gated) |
| Executive summary | `list-report-executive-summary` | `date` (scope-gated) |
| Aged receivables / payables | `list-aged-receivables-by-contact`, `list-aged-payables-by-contact` | `contactId` (required), `reportDate`, `invoicesFromDate`, `invoicesToDate` |
| Budgets | `list-budgets` (`budgetId` for line detail) | `ids`, `dateFrom`, `dateTo` |

Not usable on connections created on/after 2 March 2026: `list-report-budget-summary`, `list-report-1099`,
`list-published-reports`, `get-report-by-id`. Do not call them; use the tools above.

The P&L and balance sheet tools do not take a tracking filter for P&L; only the balance sheet accepts
`trackingOptionID1/2` here. For P&L by tracking option see `xero-tracking-categories` (build from transactions, and
flag it as derived, not a native report).

## Workflow

1. **Set the frame before pulling.** Org, base currency, accounting basis you are reporting (`paymentsOnly` =
   cash-style, otherwise accrual), period start/end, as-at date. Write them down.
2. **P&L.** For a month: `fromDate` = first day, `toDate` = last day. For a trend: `fromDate/toDate` of the latest
   period with `periods=N timeframe=MONTH` to get N comparative columns (Xero adds earlier periods). Never request
   a range that spans an uneven pair of dates and compare it with a calendar month.
3. **Balance sheet** at the period end `date`; `periods` and `timeframe` for comparatives.
4. **Trial balance** at the same `date`: this is the proof that debits equal credits and the source for any
   account-level drill.
5. **Aged reports.** Per contact only. For an organisation-wide view, build from `list-invoices` (see
   `xero-invoices-and-collections`, `xero-bills-and-supplier-payments`) and tie to the control accounts.
6. **Tie-out checks** before presenting (all must hold):
   - Net profit on P&L (period) = movement in current-year earnings/retained earnings on the balance sheet.
   - Balance sheet: assets = liabilities + equity.
   - TB totals debit = credit; AR/AP/bank lines equal the balance sheet at the same date.
   - Bank summary closing balance per account = balance sheet bank line per account.
   - Same basis (`paymentsOnly`) on every report in the pack.
7. **Interpret**, do not transcribe: margins, growth, cash conversion, liquidity ratios (current assets / current
   liabilities, quick ratio), DSO = AR / revenue x days, DPO = AP / cost of sales x days. State the formula and
   inputs. Flag zero or negative balances in unlikely lines.
8. Present in the format below; keep currency code and as-at date on every table.

## Pitfalls

- **Dates are inclusive and the P&L is a flow, balance sheet a point-in-time**; a P&L `toDate` is not an as-at date.
- `standardLayout=true` collapses custom report layouts; use it when you need consistent line items for comparison.
- Cash-basis reports (`paymentsOnly=true`) exclude unpaid invoices/bills and will not tie to AR/AP: never mix.
- Journals marked "not on cash basis" appear only on accrual reports.
- Back-dated entries change prior-period reports; always state "as run on <date>".
- Foreign-currency balances revalue at the report date; differences between report dates can be pure FX
  (`xero-multi-currency`).
- `list-trial-balance` and the balance sheet include system accounts such as unrealised currency gains; do not call
  them errors.
- Large outputs: summarise lines above materiality, offer the full table on request. Do not truncate silently.
- Budgets: `list-budgets` lines are by account and period; compare only the same periods and accounts, and note a
  budget is a plan, not a forecast.
- Never present a number that did not come from a tool in this session.

## Management pack template

1. Headline: revenue, gross profit and %, operating expenses, net profit, cash, AR, AP (current vs prior period vs
   prior year).
2. P&L summary with variance to prior and budget (if exists), variance commentary on lines beyond threshold.
3. Balance sheet summary and working capital.
4. Cash: bank summary movement by account.
5. Receivables/payables: top 5 overdue each, DSO/DPO.
6. Risks, one-offs, questions for management.

## Output format

```
Org | basis (accrual/cash) | period/as-at | currency | run date
Tie-out: [ok/fail] per check above
Tables per report; variance columns: amount, %
Commentary (max 8 bullets, each with figure and cause or question)
Data not available: <reports blocked by scope/connection>
```
