---
name: payroll-accounting
description: >-
  Account for payroll: the payroll journal (gross pay, employee deductions, employer taxes, benefits), accruals for unpaid wages, bonus and holiday pay, and reconciliation of payroll registers to the GL and tax liability accounts. Use when asked to "post payroll journal", "payroll doesn't reconcile to GL", "accrue payroll", "payroll liabilities", "year-end payroll tie-out". Not payroll processing or tax advice.
metadata:
  department: "accounting"
  domain: "payroll"
  owner: "satva-coe"
  status: "beta"
  license: "Satva-original"
  source: "original"
---

# Payroll accounting

Scope: recording and reconciling payroll in the books. Calculating pay, withholding tax and filing payroll returns belongs to the payroll provider or a payroll specialist; this skill checks the result. Rates and rules vary by jurisdiction.

## The payroll journal (per pay run)
Debit expense; credit liabilities and cash. Typical structure:
| Line | Debit | Credit |
|---|---|---|
| Gross wages/salaries (by department or cost centre) | Wages expense | |
| Employer payroll taxes (e.g. FICA/NI/social security, unemployment) | Payroll tax expense | Payroll tax payable |
| Employer benefit contributions (pension, health) | Benefits expense | Benefits payable |
| Employee taxes withheld (income tax) | | Withholding payable |
| Employee social-security share withheld | | Payable (same liability as employer share, tracked separately) |
| Employee deductions (pension, health, garnishments, loans) | | Respective payables |
| Net pay | | Cash (or payroll clearing if funded separately) |
Check: total debits = total credits; gross = net + employee withholdings + employee deductions.

Use a **payroll clearing** account when the provider debits the bank in a different amount or date from the journal; clearing must be zero after each cycle.

## Reconciliation to GL (every run and every month)
1. Payroll register gross pay by department = wages expense posted.
2. Net pay per register = bank disbursement (direct deposits + cheques); outstanding cheques listed.
3. Each liability: Opening + accrued (employee + employer) - remitted = Closing; closing agrees to the latest provider liability report or tax return. Differences: late remittance, rounding, adjustments, wrong account mapping.
4. Employer cost reasonableness: total employer cost / gross wages (burden rate). Month-over-month change beyond about 2 percentage points needs an explanation (benefit enrolment, wage-base caps, rate change).
5. Headcount rollforward: opening + hires - leavers = closing; compare to HR list. Ghost-employee test: every payee has an HR record, bank detail change log is reviewed, no duplicate bank accounts.

## Accruals
- **Unpaid wages at period end:** days worked but unpaid / days in pay period x gross for the period, plus related employer taxes. Reverse next period.
- **Holiday/vacation:** accrue earned unused leave where it vests or is payable (accrual = hours x rate x burden); true up at year end.
- **Bonuses and commissions:** accrue in the period earned, estimated from plan terms and results; document the calculation.
- **Pay-period timing:** bi-weekly payrolls have 26 (sometimes 27) pay dates a year; monthly P&L should be smoothed by accrual rather than showing 3-pay-date spikes.
- **Capitalised labour** (e.g. internal software development, construction): reclass from expense to asset per policy with time records.

## Year-end
Tie yearly totals in the register to payroll tax returns and year-end employee statements (W-2/P60/T4-style). Gross wages per GL = gross per quarterly returns +/- identified differences (taxable benefits, non-cash). Remit remaining liabilities; accrue final-quarter filings. Contractors are separate (contractor-1099-reporting).

## Controls
Segregate: who edits employee/rate/bank data, who runs payroll, who approves, who reconciles. Payroll changes require HR-approved documents. Review exception report (new payees, rate changes, bank changes, zero or negative pay) before each approval.

## Do not
- Do not net payroll liabilities against each other or against cash to make a rec work.
- Do not expense employee-withheld taxes; they are liabilities, not cost.
- Do not store employee personal data in the books beyond what is necessary; keep salary information restricted.

## Output
Payroll journal (balanced) with source register reference; liability reconciliation schedule; accrual schedule; list of reconciling items with owner.
