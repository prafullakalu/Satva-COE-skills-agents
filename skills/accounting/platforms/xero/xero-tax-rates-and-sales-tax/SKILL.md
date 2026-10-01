---
name: xero-tax-rates-and-sales-tax
description: >-
  Reviews and maintains GST/VAT/sales-tax setup in Xero via the Satva Xero MCP: tax rates and components, default
  tax on accounts and contacts, tax type on invoice lines, cash vs accrual basis, tax-inclusive vs exclusive lines,
  and pre-return checks on the sales tax control account. Use for "which tax rate in Xero", "GST/VAT is wrong on
  this invoice", "add a tax rate", "review tax codes", "pre-VAT-return check", "tax control account doesn't match",
  "non-recoverable tax".
metadata:
  department: "accounting"
  domain: "tax"
  platform: "xero"
  owner: "satva-coe"
  status: "stable"
  license: "Satva-original"
  source: "original"
---

# Xero tax rates and sales tax (GST/VAT)

Follow `xero-mcp-operating-rules`. Tax rules are jurisdictional; this skill checks the mechanics inside Xero and
never gives a filing position. State the org country (`list-organisation-details`) and send legal/tax-rate
questions to the responsible accountant.

## Tools used

Read: `list-organisation-details` (country, `Pays Tax`, `Sales Tax Basis`, `Sales Tax Period`, tax number),
`list-tax-rates`, `list-accounts` (Tax Type per account), `list-contacts` (AR/AP Tax Type), `list-invoices`,
`list-bank-transactions`, `list-trial-balance`, `list-report-balance-sheet`.
Write: `create-tax-rate`, `update-tax-rate`, `update-account` (default tax), `create-invoice` (line `taxType`).

## Facts to rely on (from the tool output)

- `list-tax-rates` returns per rate: name, **Tax Type** (the code used on lines), status, display and effective rate,
  components (name, rate, compound, non-recoverable), and what it can apply to (assets/equity/expenses/liabilities/
  revenue). Always take `taxType` from here; never guess a code like "OUTPUT2".
- Line `taxType` is required on `create-invoice`, `create-bank-transaction`, `create-credit-note`; optional on
  manual journal lines (`create-manual-journal`).
- The MCP's invoice tool is tax-exclusive in practice (no `lineAmountTypes` parameter on `create-invoice`; manual
  journals default to `NO_TAX`).

## Workflow A: setup review

1. Pull org details and all tax rates. Mark: ACTIVE rates not used by anything, duplicates (same effective rate,
   different names), rates with no component breakdown, rates created for one-offs.
2. Cross-check each account's default tax type in `list-accounts` with the nature of the account:
   revenue accounts -> output tax rate; expenses -> input; wages, bank fees, interest, insurance, depreciation,
   owner funds -> usually no tax / exempt per local rules (verify); payroll, loan, tax payments -> out of scope.
3. Check contacts: customers/suppliers with an `AR Tax Type` or `AP Tax Type` that contradicts their status
   (overseas customer with domestic rate). Those override defaults on new transactions.
4. Review the control account: balance on the sales tax account(s) in `list-trial-balance` at the period end.

## Workflow B: pre-return check

1. Period and basis: confirm `Sales Tax Basis` (accrual/cash/payments) and `Sales Tax Period`; the return period dates.
2. Control account tie-out: opening balance + output tax - input tax - payments to authority = closing balance.
   Large unexplained difference means manual journals to the control account, or tax types changed after filing.
3. Spot checks on the invoices/bills for the period (page `list-invoices`; filter dates yourself):
   - lines with tax 0 where the supplier/customer normally has tax
   - tax-rate that doesn't match the account default
   - large items with unusual rate
   - credit notes without matching tax reversal
4. Manual journals touching tax accounts (`list-manual-journals`): each needs support; these break the audit trail
   between the transactions and the return.
5. Report: list exceptions with IDs. No returns are filed through this MCP.

## Workflow C: create or change a tax rate

1. Confirm with the accountant that a new rate is needed; Xero system rates for the country normally cover it.
2. `create-tax-rate name taxComponents[{name, rate, isCompound?, isNonRecoverable?}] reportTaxType?`
   `name` must be unique. `reportTaxType` is region-specific (e.g. INPUT, OUTPUT, GSTONIMPORTS); copy from an
   existing similar rate in `list-tax-rates` of this same org.
3. `update-tax-rate` finds the rate by **name** (no ID) and **replaces** all components. Send the full component set.
   Editing a rate that is in use changes how future transactions are taxed; does not restate past ones.
4. Re-run `list-tax-rates` to verify. Tell the user that reporting treatment (return box mapping) depends on
   `reportTaxType`.

## Pitfalls

- Tax-inclusive documents (supplier invoice shows gross): convert to net before `create-invoice`; or enter in Xero UI
  with "Tax Inclusive". A wrong basis creates cent-level differences and wrong tax.
- Compound and non-recoverable components exist (Canada-style); do not treat them as ordinary single-rate tax.
- Changing a rate's percentage mid-period (rate change) needs a new rate with effective dating handled outside the
  tool; do not retro-edit the old rate.
- Cash/payments basis: tax is due when paid, so invoice-date review misses timing; use payments (`list-payments`).
- Tax on bank transactions (spend/receive money) is easily missed because there is no document; review them.
- Do not archive or edit a tax rate to hide an error; fix the transactions.
- Manual journals default to NO_TAX; a journal that should carry tax needs explicit `taxType` and amount handling.

## Output format

```
Org | country | basis/period | as-at
Setup findings: rate/account/contact | issue | impact | fix
Return prep: control account opening, output, input, payments, expected closing vs Xero closing; exceptions list
Questions for the tax accountant (not decided by this review)
```
