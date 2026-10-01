---
name: qbo-financial-reports
description: >-
  Pull and read QuickBooks Online financial reports through the Satva MCP: Profit and Loss, Balance Sheet, Cash Flow, Trial Balance, A/R and A/P aging, General Ledger, sales and expense reports, with correct period, basis, grouping and filters, and a method for explaining the numbers. Use when asked for "P&L", "balance sheet", "cash flow statement", "aged receivables", "sales by customer/item/class", "compare this month to last", "report by class or location", "how is the business doing", or "what changed vs last year".
metadata:
  department: "accounting"
  domain: "financial-reporting"
  platform: "quickbooks"
  owner: "satva-coe"
  status: "stable"
  license: "Satva-original"
  source: "original"
---

# QuickBooks financial reports

All read-only. Follow `qbo-mcp-operating-rules` for company choice. Do not rebuild a report from invoices and bills: the server's own guidance, and the numbers will not match QuickBooks.

## Tools
Dedicated tools (each takes the same period and filter parameters): `get_profit_and_loss`, `get_profit_and_loss_detail`, `get_balance_sheet`, `get_cash_flow`, `get_trial_balance`, `get_aged_receivables`, `get_aged_receivable_detail`, `get_aged_payables`, `get_aged_payable_detail`, `get_customer_sales`, `get_item_sales`, `get_class_sales`, `get_department_sales`, `get_customer_income`, `get_customer_balance`, `get_customer_balance_detail`, `get_vendor_balance`, `get_vendor_balance_detail`, `get_vendor_expenses`, `get_inventory_valuation_summary`, `get_transaction_list`, `get_transaction_list_by_customer`, `get_transaction_list_by_vendor`, `get_transaction_list_with_splits`, `get_general_ledger`, `get_journal_report`, `get_tax_summary`, `get_account_list`. `run_report` takes `report_type` (canonical name or alias such as `pnl`, `balance_sheet`, `ar_aging`) and does the same. The Intuit reports API supports a fixed set of reports; contact lists and some regional reports (for example BAS, budget vs actuals) are not available through this server. `period_comparison` and `cash_position` are derived tools described below.

## Parameters that matter
- Period: `start_date` / `end_date` (`YYYY-MM-DD`) or `date_macro` (for example `This Month`, `Last Month`, `This Fiscal Year-to-date`). A macro overrides dates.
- `accounting_method`: `Accrual` or `Cash`. Always set it and always say which you used; the company default can differ from what the user expects. Balance sheet totals differ by basis only through A/R, A/P and related accounts.
- `summarize_column_by`: `Total`, `Month`, `Week`, `Days`, `Quarter`, `Year`, `Customers`, `Vendors`, `Classes`, `Departments`. Month columns give trend; Classes/Departments give dimension P&L.
- Filters (only where documented for the report; others are passed through with a warning in the output): `customer`, `vendor`, `item`, `class`, `department`, `account`, `source_account`, `account_type`, `report_date` (as-of date for balance-type and aging reports), `aging_method`, `aging_period`, `num_periods`, `past_due`, `cleared`, `columns`, `sort_by`, `group_by`. Entity filters take comma-separated Ids, not names; look Ids up with `query_quickbooks`.
- Balance-type reports (balance sheet, aging, inventory valuation) are as-of a date: use `end_date` for the balance sheet, `report_date` for aging and inventory.

## Which report answers which question
| Question | Report | Read it for |
|---|---|---|
| Are we profitable? | P&L, `summarize_column_by: "Month"` | Revenue, gross margin, operating expenses, net income trend |
| Where did one number come from? | P&L Detail or General Ledger with `account` | Transactions behind a line |
| What do we own and owe? | Balance Sheet | Cash, A/R, inventory, A/P, loans, equity |
| Why did cash move? | Cash Flow | Operating vs investing vs financing |
| Do the books balance? | Trial Balance | Debits = credits; suspense balances |
| Who owes us, who do we owe? | Aged Receivables, Aged Payables | Buckets; must equal control account |
| Best customers/products | Customer Sales, Item Sales, Customer Income | Concentration, margin by customer |
| Dimension view | P&L by Classes or Departments | Business lines, locations |
| What did vendors cost? | Vendor Expenses | Spend concentration |
| Stock position | Inventory Valuation Summary | Quantity, value |
| Tax liability | Tax Summary | Collected vs payable by agency |

## Method for any report
1. State the scope: company, period, basis, currency.
2. Run it. The tool returns a flattened table plus the raw JSON; header lines show `Period`, `Basis`, `Currency`, and any `Warning` about filters.
3. Sanity-test before explaining:
   - Balance sheet: Total Assets = Total Liabilities + Equity.
   - Trial balance: debit total = credit total.
   - A/R aging total = Accounts Receivable on the balance sheet at the same date; A/P likewise.
   - P&L net income = the current year's net income inside Equity on the balance sheet (plus retained earnings from prior years).
   - Cash Flow ending cash = balance sheet cash.
   If a test fails, report that before any commentary.
4. Explain with comparison: `period_comparison` (`start_date`, `end_date`, `compare: "prior_period"` or `"prior_year"`, `accounting_method`) returns per-account change and percent change, totals and top increases and decreases. For a single-month range it compares to the previous calendar month. Section tells you whether an increase is good (Income) or cost (Expenses).
5. Quote amounts with currency, and percentages to one decimal. Never round away the sign: parentheses and minus signs mean different things in a few report layouts, so check the raw JSON when unsure.
6. Separate fact from inference. "Marketing is up 42% (+$6,300)" is fact; "due to the June campaign" is inference unless a transaction shows it.

## Reading specific reports
- **P&L**: Gross margin = (Income - Cost of Goods Sold) / Income. Watch Uncategorized Income/Expense lines and "Other Expense" growth; they hide miscoding.
- **Balance Sheet**: look for Undeposited Funds, Opening Balance Equity, negative cash or A/R, and Retained Earnings that moved mid-year without a close.
- **Cash Flow**: derived from account types, so a mis-typed account (loan under expenses) distorts it.
- **Aging**: current means not yet due, not "new". The bucket basis follows `aging_method` (`Report_Date` or `Current`). Open credits can offset overdue amounts in the totals, so check the detail report before reading a customer as current.
- **Class P&L**: compare the sum of class columns to the company total; the difference is unclassified.
- **Inventory valuation**: QuickBooks Online costs inventory on a FIFO basis; the value is as of the `report_date`, and back-dated bills or sales change history.

## Limits and traps
- Reports return strings; use integer cents when adding. The tools flatten at most 200 report lines in the text summary; the raw JSON has everything.
- Cash basis reports can lag (a bill appears when paid); accrual shows it at bill date.
- A report is live. If a transaction was added after you ran it, re-run before quoting. Note the run time.
- Reads count against Intuit API quota: avoid running the same report repeatedly; prefer one `summarize_column_by: "Month"` call over twelve monthly calls.
- Multi-company: pass `company` explicitly; do not mix numbers from two companies in one table without labelling.
- `get_trial_balance_fr` exists in the tool list but is a regional variant; use it only if the user asks and tell them it may be unsupported.

## Output
A short summary (3-6 bullets with numbers) first, then the table, then sanity-test results and the "Basis/period/currency" line. Offer drill-downs; do not dump raw JSON.
