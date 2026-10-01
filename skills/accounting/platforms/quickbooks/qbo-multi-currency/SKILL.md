---
name: qbo-multi-currency
description: >-
  Work with multicurrency in QuickBooks Online: check whether it is enabled, foreign-currency customers, vendors, invoices, bills and bank accounts, exchange rates, realised and unrealised gains and losses, and home-currency reporting. Use when asked to "invoice in euros in QuickBooks", "multicurrency setup", "exchange rate wrong on this bill", "realised gain/loss", "revalue foreign balances", "why does the A/R total differ by currency", or "set exchange rates for month end".
metadata:
  department: "accounting"
  domain: "multi-currency"
  platform: "quickbooks"
  owner: "satva-coe"
  status: "beta"
  license: "Satva-original"
  source: "original"
---

# QuickBooks multi-currency

Status beta: tool names are verified in the server source; QuickBooks' currency behaviour is described from the public API and product model and has not been run against a live multicurrency company here. Follow `qbo-mcp-operating-rules`.

## Facts that decide everything
- Multicurrency, once turned on in a company, cannot be turned off. Do not recommend enabling it for one or two foreign invoices; prefer a home-currency invoice with a note unless the customer must be billed in their currency and you need the receivable in that currency.
- Home currency is fixed at set-up. Each customer, vendor and foreign bank or card account has its own currency, and a customer or vendor with transactions cannot change currency.
- A/R and A/P control accounts exist per currency (for example "Accounts Receivable (A/R) - EUR").
- Check `get_company_overview`: `multiCurrency` and `homeCurrency`. When off, `CompanyCurrency`, `ExchangeRate` and `CurrencyRef` are rejected.
- Tools in this server: `get_entity` and `update_entity` on `ExchangeRate` (the `id` is the source currency code, such as `EUR`; there is no create; the home currency has no rate), and `create_entity`, `get_entity`, `update_entity`, `delete_entity` on `CompanyCurrency` (`delete_entity` deactivates it). `query_quickbooks` can list `SELECT * FROM CompanyCurrency` and `SELECT * FROM ExchangeRate`.
- The worklists (`ar_collections_worklist`, `ap_due_bills_worklist`, `cash_position`) total home-currency balances (`HomeBalance`) so mixed-currency totals add up. `cash_position` assumes home currency for account balances; for foreign bank accounts read `get_balance_sheet` instead.

## Workflow: review
1. `get_company_overview`; list enabled currencies with `query_quickbooks` `SELECT Code, Name, Active FROM CompanyCurrency`.
2. Current rates: `get_entity` `ExchangeRate` for each active code (`id` = code). Note `AsOfDate`; rates that are weeks old explain odd gains/losses and revaluation differences. QuickBooks can fetch daily rates automatically; manual rates stay as set.
3. Balances by currency: `get_aged_receivables` and `get_aged_payables` show amounts in each currency and home equivalents; `get_balance_sheet` shows home-currency values. Foreign-currency control accounts are revalued only when you run an exchange-gain/loss adjustment.
4. Realised vs unrealised:
   - Realised gain/loss arises when a foreign invoice or bill is settled at a different rate from the one used at posting. QuickBooks books it automatically to "Realized Currency Gain or Loss". Check that account in the P&L.
   - Unrealised gain/loss arises on open foreign balances (A/R, A/P, foreign bank) at period end. QuickBooks books it to "Unrealized Currency Gain or Loss" through an exchange-gain/loss adjustment that is posted in the QuickBooks user interface. This server has no tool for it: for month end, report the expected amount, and the user posts the adjustment (or the accountant books a journal entry), then reverses it next month.
5. Estimate unrealised gain/loss to propose: for each foreign balance, home value at period-end rate minus current home carrying value. Show the arithmetic per balance and per currency in cents; use the period-end rate from `ExchangeRate` or the user's rate source, stating which.

## Workflow: write
1. Create a foreign invoice or bill: set `CurrencyRef` (`{"value":"EUR"}`) and, if the user wants a specific rate, `ExchangeRate`; otherwise QuickBooks uses its stored rate for the date. The customer or vendor must already be in that currency; the bank deposit account must be in that currency or home currency.
2. After create, read back and show `TotalAmt`, `ExchangeRate`, `HomeTotalAmt`.
3. Payments: a foreign invoice paid into a home-currency bank account produces a realised gain/loss when the payment's rate differs. Check the payment's `ExchangeRate` equals the rate used at the bank (the bank statement shows the home-currency amount received).
4. Update a rate: `update_entity` `ExchangeRate` (`id` = code, patch `{"Rate": 1.0830, "AsOfDate": "2026-06-30"}`). This changes the stored rate for later transactions; it does not restate posted ones. Confirm with the user which rate source and date.
5. Foreign journal entry: all lines in one currency; A/R and A/P lines need a customer or vendor in the same currency. See `qbo-journal-entries`.

## Pitfalls
- A bill or invoice has a single currency; all its lines are in that currency.
- Credit memos and vendor credits must match the currency of the invoice or bill they offset.
- A report in home currency differs from the sum of foreign amounts because of rate movements; do not "fix" the difference.
- Hard-coding a rate on a transaction to match a bank statement creates a realised difference somewhere else only if the booked rate was wrong; verify against the statement, not memory.
- Bank feed lines in a foreign-currency account arrive in that currency. Matching them to home-currency transactions breaks reconciliation.
- Do not delete a currency that has open balances; deactivation fails or hides it.

## Output
Currency set-up summary, rates table with dates, balances per currency and home equivalent, proposed unrealised gain/loss entry with calculation, and the manual steps the user must take in QuickBooks.
