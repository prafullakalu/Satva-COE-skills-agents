---
name: xero-multi-currency
description: >-
  Handles foreign-currency work in Xero via the Satva Xero MCP: reading which currencies and rates apply, reviewing
  foreign-currency invoices, bills and bank accounts, separating realised from unrealised FX, reporting in base
  currency, and spotting multi-currency pitfalls. Use for "multi-currency in Xero", "invoice in USD", "FX gain loss",
  "exchange rate on invoice", "foreign bank account", "revaluation", "report in base currency", "AUD vs USD totals
  don't add up".
metadata:
  department: "accounting"
  domain: "multi-currency"
  platform: "xero"
  owner: "satva-coe"
  status: "beta"
  license: "Satva-original"
  source: "original"
---

# Xero multi-currency

Follow `xero-mcp-operating-rules`. Status is beta: tool behaviour below is verified in the server source, but the
FX accounting statements describe Xero's standard behaviour and should be confirmed in a live org before use in a
client deliverable.

## Tools used

Read: `list-organisation-details` (base currency), `list-currencies` (enabled currencies), `list-invoices`
(`Currency`, `Currency Rate`, `Amount Due`, `Total`), `list-bank-transactions` (`Currency Code`),
`list-payments`, `list-accounts`, `list-contacts` (`Default Currency`), `list-trial-balance`,
`list-report-balance-sheet`, `list-profit-and-loss`.
Write: `create-invoice`, `create-credit-note`, `create-payment`, `create-bank-transaction`,
`create-manual-journal`.

## What the tools can and cannot do

- `create-invoice`, `create-credit-note`, `create-purchase-order`, `create-bank-transaction`: **no currency or
  rate parameter.** The currency follows the contact's default/the bank account's currency, and the rate comes from
  Xero's rate table. If the user needs a document in a specific currency or at a specific rate, set the contact's
  default currency or create the document in Xero. Do not pretend this MCP chose the currency.
- Currencies can only be enabled in Xero settings; `list-currencies` is read-only.
- Foreign-currency bank accounts, and the realised/unrealised FX gain/loss accounts, are Xero system settings.
- `list-invoices` returns each invoice's `Currency` and `Currency Rate`; amounts are in the invoice currency.

## Workflow: review a multi-currency organisation

1. Base currency and enabled currencies: `list-organisation-details`, `list-currencies`.
2. Inventory of exposure: page `list-invoices`; group open items (AUTHORISED, Amount Due > 0) by `Type` and
   `Currency`. Show per-currency totals; do **not** add across currencies.
3. Convert for reporting only when asked: choose the rate source (invoice rate, period-end rate, average rate),
   state it, and label the result "indicative conversion". Xero's own reports give base-currency values at its
   own rates; do not overwrite them with yours.
4. Bank: `list-accounts` Type=BANK with a non-base currency; `list-report-bank-summary` shows balances in the
   account currency. Reconcile in account currency (`xero-bank-reconciliation-review`).
5. FX gain/loss lines: `list-trial-balance` for Realised Currency Gains/Unrealised Currency Gains. Realised FX
   arises when a foreign invoice is paid at a different rate than booked; unrealised arises on revaluing open
   balances at period end (Xero revalues AR/AP/bank at the report date for reporting; it reverses the next day).
   Large realised FX on small payments suggests wrong rate or wrong payment date.
6. Spot checks: invoices where the contact default currency differs from the invoice currency; the same customer
   with two contact records by currency; payments recorded in the wrong bank account currency.

## Workflow: before paying or receiving a foreign invoice

1. Confirm invoice currency and `Amount Due` (`get-invoice`).
2. The payment account must be in the same currency (or you accept an FX difference): `create-payment invoiceId
   accountId amount date`. Amount is in the invoice currency; confirm that the bank amount in base currency matches the
   statement after the bank's conversion. Rate differences post to realised FX in Xero.
3. If the bank account is base currency but the invoice is foreign, the amount actually debited is the converted one;
   record this carefully in Xero and flag it; the MCP cannot enter a custom rate, so a person must set the rate in
   Xero.

## Pitfalls

- Summing `Total` across currencies without conversion.
- Using the transaction date rate for an end-of-period balance sheet figure.
- Journals to foreign-currency accounts must be in the account's currency; the manual journal tool has no currency
  field, so avoid journalling to foreign-currency bank accounts and use a bank transaction or transfer in Xero.
- Changing a contact's default currency after transactions exist is blocked or confusing; create a separate contact
  if needed.
- Bank transfers between base and foreign accounts (`create-bank-transfer`) need both amounts/rates; the tool takes a
  single `amount`, so transfers across currencies must be entered in Xero.
- Archiving a currency or changing base currency is not possible once transactions exist.

## Output format

```
Org | base currency | enabled currencies | as-at
Exposure table: Type | currency | # open | amount (currency) | indicative base amount (rate source)
FX accounts: realised, unrealised balances
Findings: item | evidence | action; Needs Xero UI: rate entry, currency enable, cross-currency transfers
Assumptions: rate source and date for every conversion
```
