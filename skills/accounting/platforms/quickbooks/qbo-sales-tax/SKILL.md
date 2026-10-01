---
name: qbo-sales-tax
description: >-
  Check and work with sales tax in QuickBooks Online: whether tax is on, tax codes and rates, taxable vs non-taxable customers and items, how tax lands on invoices, bills and the liability account, tax summary versus payable balance, and common mistakes (tax in journals, wrong code, rounding, VAT/GST differences by country). Use when asked to "check sales tax in QuickBooks", "why is tax wrong on this invoice", "sales tax liability doesn't match", "set up tax codes", "VAT/GST in QBO", or "prepare the sales tax return numbers".
metadata:
  department: "accounting"
  domain: "tax"
  platform: "quickbooks"
  owner: "satva-coe"
  status: "beta"
  license: "Satva-original"
  source: "original"
---

# QuickBooks sales tax

Status beta: the tool names below are verified against the server source, but tax behaviour differs by country (US sales tax, Canada GST/HST/PST, UK/EU VAT, Australia GST, India GST) and this skill has not been exercised against a live company in each. State the company's country first and do not assume US rules elsewhere. This skill prepares and checks; it does not file returns or give tax advice.

## Tool facts (verified)
- `get_company_overview` reports `salesTaxEnabled` and `country`. If tax is off, tax reports and TaxCode lines have no effect.
- `get_entity` reads `TaxCode`, `TaxRate`, `TaxAgency` (read-only for TaxCode and TaxRate through this server). `describe_entity` confirms that `TaxCode` and `TaxRate` cannot be created here (Intuit's TaxService endpoint is not wired) and `TaxAgency` supports create and read only. So tax codes and rates are set up in the QuickBooks UI.
- `get_tax_summary` (or `run_report` `report_type: "tax_summary"`) is the Reports API tax report. It accepts a period, `accounting_method` and `summarize_column_by`, and documents no other filters.
- `get_changes` does not support `TaxCode`, `TaxRate`, `TaxAgency` (Intuit CDC limit); use `query_quickbooks` instead.
- `query_quickbooks` can read `SELECT * FROM TaxCode`, `TaxRate`, `TaxAgency` (single entity, no joins).

## Workflow: tax health check
1. `get_company_overview`: country, `salesTaxEnabled`, report basis. Stop here if tax is disabled and ask whether it should be.
2. Read tax set-up: `query_quickbooks` `SELECT Id, Name, Active, Taxable, TaxGroup FROM TaxCode MAXRESULTS 200`, then `SELECT Id, Name, RateValue, AgencyRef FROM TaxRate`. List codes with their component rates and agencies. Note inactive codes still used on recent transactions.
3. Customers: `query_quickbooks` `SELECT Id, DisplayName, Taxable, DefaultTaxCodeRef FROM Customer WHERE Active = true`. Flag customers marked non-taxable with no exemption reason recorded and customers with no tax code in a taxing country.
4. Items: `SELECT Id, Name, Taxable, SalesTaxCodeRef FROM Item`. Flag taxable services and non-taxable goods that look wrong for the jurisdiction (rules vary; ask the user's accountant when unsure).
5. Tax liability tie-out for the period:
   - `get_tax_summary` for the filing period on the user's basis.
   - Compare tax collected less tax paid on purchases (VAT/GST) to the movement and closing balance of the Sales Tax Payable (or GST/VAT liability) account: `get_general_ledger` with `account` = that account's Id.
   - Differences usually come from: manual journal entries to the tax account, tax payments recorded as expense, changed tax rates mid-period, back-dated invoices, voided invoices, or cash vs accrual basis mismatch.
6. Sample 10 invoices across customers: `get_entity` `Invoice` and check `TxnTaxDetail` (total tax, tax lines per rate), line `TaxCodeRef`, and `GlobalTaxCalculation` (`TaxExcluded`, `TaxInclusive`, `NotApplicable`). Recompute: tax = taxable base x rate, rounded per QuickBooks' rule; list any variance greater than one cent per line.
7. Report exceptions with ids and a proposed fix; no write without approval.

## Writing transactions with tax
- Let QuickBooks calculate. On invoices set line `TaxCodeRef` (or rely on the customer's default) and `GlobalTaxCalculation`; a `TxnTaxDetail` you supply can be overridden. Always read the created invoice back and compare `TotalAmt` to the expected total.
- US companies with automated sales tax: tax rates come from the customer's ship-to address; a missing or wrong address is the main source of wrong tax. Check `ShipAddr` before sending.
- Tax on bills and expenses (input VAT/GST) requires `TaxCodeRef` on lines and `TxnTaxDetail`; mismatches show up as differences on the tax summary.
- To correct tax on an already issued invoice: credit memo and reissue, not a journal. A journal entry to Sales Tax Payable changes the account but not the tax centre or the returns, so the next return will disagree with the ledger.
- Tax payments to the agency are recorded in the QuickBooks tax centre (Pay Sales Tax). Recording them as a plain expense leaves the liability open. Say this to the user; this server has no tool for it.

## Country notes (check, do not assume)
- US: nexus and registration obligations are outside QuickBooks; do not state a rate or taxability rule as fact.
- Canada: GST/HST/PST codes are separate components; Quebec QST and BC PST have different rules; input tax credits flow through purchase tax codes.
- UK/EU VAT and Australia GST: transactions use tax-inclusive or exclusive pricing; reverse-charge and zero-rated vs exempt codes must be distinguished.
- India GST: CGST/SGST/IGST codes follow place of supply.

## Never
- Never change a tax code or rate on historical transactions in a filed period.
- Never present `get_tax_summary` as a filed return.
- Never delete a tax-bearing invoice to "fix" tax; void or credit.
- Do not guess tax treatment: list the question for the accountant.

## Output
Country and set-up summary, tie-out table (summary vs ledger vs return), exception list with ids, proposed corrections, questions for the accountant.
