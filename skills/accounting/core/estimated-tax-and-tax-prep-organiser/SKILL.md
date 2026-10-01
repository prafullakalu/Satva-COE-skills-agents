---
name: estimated-tax-and-tax-prep-organiser
description: >-
  Estimated (quarterly) income tax calculations with safe-harbour logic, and organising books and documents for the tax preparer: deduction categories, personal-vs-business separation, document checklist. Use for "quarterly estimated taxes", "how much should I set aside for tax", "get ready for tax season", "tax prep checklist", "what does my accountant need". Not tax advice.
metadata:
  department: "accounting"
  domain: "tax"
  owner: "satva-coe"
  status: "beta"
  license: "Satva-original"
  source: "original"
---

# Estimated taxes and tax-prep organiser

**Boundary: not tax advice.** This produces estimates and organised workpapers for a qualified preparer. Rates, brackets, deadlines and safe-harbour rules vary by country, state and year and are updated regularly: confirm current figures before relying on any number. State all assumptions in the output.

## Part A: Estimated tax (US-style pattern)
1. **Basis:** collect year-to-date net profit from the P&L (after reconciliation), expected full-year profit (annualise with seasonality, not x4 blindly), other income, expected deductions and credits, estimated payments already made.
2. **Annual tax estimate:** apply to the entity type: sole proprietor/partner (income tax + self-employment tax on net earnings, with the deduction for half of SE tax), S corporation (owner reasonable salary through payroll; pass-through income), C corporation (flat corporate rate), plus state/local. Use the preparer's or authority's current computation; do not hard-code brackets in this skill.
3. **Safe harbours (US individuals, verify yearly):** pay the lesser of ~90% of current-year tax or 100% of prior-year tax (110% if prior-year AGI exceeded 150,000). Corporations use 100% of current or prior-year tax rules with a large-corporation exception. Meeting a safe harbour avoids the underpayment penalty even if the final bill is larger.
4. **Quarterly schedule:** typically four instalments (US: 15 Apr, 15 Jun, 15 Sep, 15 Jan for individuals; shifted if a due date falls on a weekend or holiday). Annualised-income method helps seasonal earners.
5. **Set-aside rule of thumb** for cash planning only: set aside a percentage of each deposit (pick from the estimate: tax / profit, e.g. 25-35% for a sole proprietor) into a separate tax account, topped up quarterly.
6. **Post entries:** payments to the tax authority are not an expense for pass-through owners (equity draw/tax payable); for corporations they reduce income tax payable. Do not expense owner income-tax payments in the business P&L.

## Part B: Tax-prep organiser
Prepare a package the preparer can work from without email ping-pong.

### Books
- Reconciled TB and year-end P&L/BS with prior-year comparatives (quarter-and-year-end-close).
- All accounts reconciled; no uncategorised or suspense balances; owner draws/contributions and personal items cleaned (separate personal spending from business; reclass to owner equity).
- Fixed asset register with additions/disposals and depreciation method (fixed-assets-depreciation); loan statements and interest; vehicle mileage logs.
- Contractor payments and forms (contractor-1099-reporting); payroll year-end forms (payroll-accounting); sales tax returns (sales-tax-vat-gst-compliance).
- Home-office, vehicle and travel/meals support: apply the documented allocation method (business-use %, per-diem or actuals).

### Document checklist
Income: sales reports, 1099-K/1099-NEC received, bank and processor statements. Expenses: categorised ledger and receipts above the substantiation threshold. Assets: purchase invoices, closing statements. Financing: loan statements, interest forms. Prior year: filed return and carryforwards (losses, credits, depreciation, charitable). Elections and letters: tax authority notices, entity filings. Personal items for owner-level returns: W-2s, interest/dividends, retirement contributions, health coverage forms, estimated payments made (dates and amounts).

### Deduction categorisation guardrails
Ordinary and necessary business expenses with documentation; capitalise items above the capitalisation policy/threshold; partially personal items split with a documented basis; fines and penalties, personal expenses, and entertainment (jurisdiction-specific) typically not deductible; meals often limited. Flag, do not decide, grey areas.

## Output
(1) Estimate worksheet with assumptions, safe-harbour test result and instalment schedule; (2) organiser index of documents with status (have / missing / not applicable); (3) list of judgement items for the preparer.

## Do not
Do not file, pay or elect anything. Do not present an estimate as a tax liability. Do not include full tax IDs or account numbers in shared documents.
