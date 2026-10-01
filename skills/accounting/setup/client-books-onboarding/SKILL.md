---
name: client-books-onboarding
description: >-
  Set up or take over a client's books: collect entity facts, choose basis and fiscal year, set the opening position, lock the cutoff and produce a clean-start checklist. Use for "onboard a new client", "take over the books", "set up bookkeeping", "opening balances", "conversion from another system", "catch-up bookkeeping", or "new entity setup".
metadata:
  department: "accounting"
  domain: "setup"
  owner: "satva-coe"
  status: "beta"
  license: "MIT"
  source: "https://github.com/Receiptor-AI/bookkeeping-skills/tree/main/skills/bookkeeping-setup"
---

<!-- Satva original, extended with a reference adapted from Receiptor-AI/bookkeeping-skills skills/bookkeeping-setup (MIT, Copyright (c) 2026 Receiptor AI). Modified by Satva: condensed, tool-agnostic. -->

# Client books onboarding

Goal: reach a state where every later month can be closed from evidence, with a known opening position and a named owner for every control. Nothing in a live ledger is posted until the owner has approved the plan in step 8.

## 1. Collect entity facts (do not guess any of these)

| Item | Why it matters |
|---|---|
| Legal name, registration number, jurisdiction, entity type | Drives tax forms, statutory deadlines, equity structure |
| Tax identifiers and registrations (VAT/GST/sales tax, payroll) | Tax codes, filing calendar |
| Fiscal year end and first period to be kept | Period structure, cutoff |
| Accounting basis: cash, accrual, or cash for tax and accrual for management | Chart design, accrual journals |
| Functional currency and any foreign-currency bank accounts or customers | Revaluation, bank feed setup |
| Revenue streams, sales channels, payment processors | Clearing accounts, revenue accounts |
| Bank, card, loan, payroll and merchant accounts (last four digits only in notes) | Reconciliation scope |
| Existing software, prior accountant, prior-year returns | Opening balances, continuity |
| Related entities and intercompany flows | Intercompany accounts, see `intercompany-tie-out` |
| Who approves bills, who releases payments, who can post journals | Segregation of duties |

If any row is unknown, record it as an open question with an owner and date. Do not default the basis or fiscal year.

## 2. Decide scope and cutoff

- Pick the **conversion date**: ideally a period end (month or year end) with a bank statement and filed returns behind it.
- Starting mid-year: either load a full trial balance at the conversion date plus year-to-date activity by month, or load opening balances only and accept that prior-period comparatives are unavailable. State which in writing.
- Catch-up work: process oldest period first and reconcile each period before moving on. Never reconcile only the latest month.

## 3. Obtain the opening position

Required: closing trial balance (or balance sheet) at the conversion date from the prior accountant or system, final bank and card statements, loan statements, AR and AP agings, fixed-asset register, payroll liabilities, tax account balances, equity roll-forward.

Validate before loading:
1. Trial balance debits equal credits.
2. Every control account agrees to its subledger (AR to aging, AP to aging, loans to lender statement, bank to statement). Differences become dated, named reconciling items, not plugs.
3. Retained earnings equals prior-year closing retained earnings plus current-year result to date.
4. Accounts that look wrong (negative AR, negative inventory, credit balance in an asset, stale undeposited funds) are listed for the owner, not silently cleaned.

## 4. Build the chart and setup

Design the chart with `chart-of-accounts-design`. Then configure: fiscal year and period lock, tax rates and codes (read from the jurisdiction, never invented), currencies, numbering for invoices and journals, tracking categories or classes, users and roles.

## 5. Load opening balances

- One opening journal dated the day after the conversion date (or the system's opening-balance facility), source document = the prior trial balance.
- Open AR and AP are loaded as individual open invoices and bills dated their true dates so aging is correct. Do not load them as a single lump journal.
- The offset for any unavoidable difference goes to a clearly named opening-balance suspense account that must be zero by the first close. A non-zero balance after first close is a defect.

## 6. Connect and reconcile

Connect bank feeds per `bank-feed-import-and-capture`. Reconcile each account at the conversion date first (it must tie to the final statement) and then forward per `bank-reconciliation`.

## 7. Controls and calendar

Record in the client file: who prepares, who reviews, who approves payments, month-end deadlines, document request cadence, tax filing dates, retention period. Preparer and approver must be different people for payments and for manual journals above the agreed threshold. Where a single owner does everything, record the compensating control (for example the owner reviews the bank statement directly).

## 8. Approval gate (draft then confirm)

Present to the owner: entity facts, basis, chart summary, opening trial balance with reconciling items, open questions, and the proposed first-month calendar. Wait for explicit approval before posting opening entries or locking a period.

## Output

A client file containing: entity fact sheet, conversion memo (cutoff, basis, load method), opening trial balance with tie-out evidence, open-questions list, control matrix, and close calendar.

## Do not

- Plug an out-of-balance opening to retained earnings or "miscellaneous".
- Load a year of history before the opening position is reconciled.
- Store full account numbers, passwords or tax IDs in notes; reference the secure system instead.
- Change fiscal year, basis or functional currency after posting without a documented restatement decision.

## References

- [references/bookkeeping-context-profile.md](references/bookkeeping-context-profile.md): a reusable context profile (entity, tax, accounting method, sources, approval thresholds), basis selection table, starter chart baseline, approval boundaries and a finishing checklist.
- `client-close-profile`: the standing profile of close-governing facts (materiality, risk areas, schedules, estimation policies) to create once the books are live.
