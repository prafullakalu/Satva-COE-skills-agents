---
name: payroll-accounting
description: >-
  Account for payroll: build and prove the payroll journal (gross pay, employee deductions, employer taxes, benefits, net pay), accrue unpaid wages, bonus and leave, allocate labour to jobs or departments, and reconcile payroll registers to the GL and tax-liability accounts using five reconciliation identities. Use for 'post payroll journal', 'payroll doesn't reconcile to GL', 'accrue payroll', 'payroll liabilities', 'year-end payroll tie-out', 'payroll clearing account'. Not payroll processing or tax advice.
metadata:
  department: "accounting"
  domain: "payroll"
  owner: "satva-coe"
  status: "beta"
  license: "MIT"
  source: "https://github.com/karbonhq/Public-Claude-Skills/tree/main/plugins/karbon-claude-plugins/skills/payroll-journal-entry-skill-builder"
---
<!-- Extends the Satva original payroll-accounting skill; reconciliation identities and provider notes adapted from karbonhq/Public-Claude-Skills (MIT, Copyright (c) 2026 Karbon); books-sync and job-costing guidance adapted from anthropics/knowledge-work-plugins small-business/skills/payroll-prep (Apache-2.0). Modified by Satva: merged into the existing skill, vendor connector steps removed. -->
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
Check: total debits = total credits; gross = net + employee withholdings + employee deductions. Prove it with the five reconciliation identities in `references/reconciliation-identities.md` before posting.

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

## Post after the run, never before
Post the journal after the run is submitted: the proposed run and the run that actually happened differ whenever the owner edited a line at the last step. Take final figures from the payroll provider's register; confirm gross and tax amounts manually if payroll was run outside a provider. Post cash to the pay date. A period ending on the 31st with a pay date on the 4th straddles month end: ask once whether the business accrues wages, and do not add accruals to books that have never had them. If the entry does not balance, find the cause; never plug a suspense account.

## Job-cost and department allocation
Allocate wages by the job or department hours already on the timesheets. Allocate at fully burdened cost only when the owner has given a burden rate; otherwise allocate raw wages and label them raw. Never invent a burden rate: a guessed loading makes every job margin wrong in the same invisible direction. Hours with no job go to a visible unallocated-labour bucket; a large one is itself a finding. After posting verify: debits = credits, net pay = the actual bank debit, allocated hours + unallocated = total paid hours, and the entry lands in the pay-date period. Detail: `references/books-sync-job-costing.md`.

## Controls
Segregate: who edits employee/rate/bank data, who runs payroll, who approves, who reconciles. Payroll changes require HR-approved documents. Review exception report (new payees, rate changes, bank changes, zero or negative pay) before each approval.

## Do not
- Do not net payroll liabilities against each other or against cash to make a rec work.
- Do not expense employee-withheld taxes; they are liabilities, not cost.
- Do not store employee personal data in the books beyond what is necessary; keep salary information restricted.

## Reconciliation failures and what they mean
| Symptom | Likely cause |
|---|---|
| Total-cost identity off by a few dollars | Rounding in per-employee lines: trust the register's totals row |
| Off by exactly one line item | A line misread (e.g. employee-only deduction treated as having an employer side) |
| Net pay differs from the bank debit | Direct-deposit reversal, manual or final cheque, void |
| Tax liability identity fails | A state or local tax missed, or employer share not separated from employee share |
| One benefit's liability fails | Pre-/post-tax misclassified, benefit waived this period, employer share invoiced separately |
| Debits and credits differ but identities 1-4 pass | Transposed line or sign error on a deduction |

## References
- `references/reconciliation-identities.md`: the five identities and derivations.
- `references/books-sync-job-costing.md`: timing, entry structure, accruals, job costing.
- `references/payroll-provider-report-notes.md`: which register report to request per provider, and bank-debit timing.
- To codify one client's allocation rules as a reusable procedure, use `payroll-journal-entry-skill-builder`. To get hours and rates right before the run, use `payroll-run-prep-and-anomaly-checks`.

## Output
Payroll journal (balanced) with source register reference; liability reconciliation schedule; accrual schedule; list of reconciling items with owner.
