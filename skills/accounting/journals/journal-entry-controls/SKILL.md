---
name: journal-entry-controls
description: >-
  Prepare, review and approve manual and adjusting journal entries: standard entry types (AP accrual, prepaid amortisation, depreciation, payroll accrual, revenue and deferred revenue, reclass, correction), required support, approval matrix, reversal logic, a balanced import-ready CSV and a reviewer checklist. Use for "post a journal", "prepare a JE", "adjusting entry", "reclass", "correct a mistake", "reversing entry", "journal entry review", or "manual journal approval".
metadata:
  department: "accounting"
  domain: "journal-entries"
  owner: "satva-coe"
  status: "beta"
  license: "Apache-2.0"
  source: "https://github.com/anthropics/knowledge-work-plugins/tree/main/finance/skills/journal-entry-prep"
---

<!-- Adapted from anthropics/knowledge-work-plugins finance/skills/journal-entry and journal-entry-prep (Apache-2.0) and hazlijohar95/skills skills/financial-close/journal-entry (MIT, Copyright (c) 2026 Hazli Johar). Modified by Satva: merged into one skill, connector placeholders removed, folded in Satva review, reversal and period-lock controls. -->

# Journal entry controls

A manual journal bypasses the controls built into invoices, bills and bank matching, so it needs more evidence, not less. This skill assists with preparation; every entry is reviewed by a qualified person before posting.

## 1. When a journal is the right tool

Use a journal for accruals and deferrals, depreciation and amortisation, reclassifications, corrections of coding errors, revaluations, intercompany and eliminations, opening balances and period-end estimates. Do not use one to fix what a source document should fix (correct a wrong bill on the bill or with a credit note) and do not post directly to AR, AP or inventory control accounts; change them through their subledger so subledger and ledger still agree.

## 2. The entry contract

Every entry, whoever drafts it:

| Element | Standard |
|---|---|
| Date | In the period the economics belong to (accruals: last day); period must be open |
| Reference | Unique and coded by type (ACC-2026-03-01) |
| Memo | Stable and reproducible: `<period>: <what and why>`, plus `(auto-reverse <next period>)` where relevant, so a rerun can recognise an entry already imported |
| Lines | Account exactly as named in the client's chart, debit or credit, amount, tax code, department or project |
| Currency | Functional currency; foreign lines show currency, rate and rate source |
| Source | A document, schedule, named policy or approved categorisation item. No source, no entry |
| Preparer, reviewer, approver | Distinct people above the threshold |
| Reversal flag | Stated at creation |

Debits equal credits to the cent, per entry. One entry, one purpose, so it can be reviewed and reversed alone. An account that does not exist in the chart is a question for the owner, never something to invent. A data gap blocks the entry; it is not estimated unless the client has a written estimation policy for exactly that item.

## 3. Standard entry types

| Type | Debit | Credit | Key checks |
|---|---|---|---|
| AP accrual (received, not invoiced) | Expense (or asset if capitalisable) | Accrued liabilities | Source: PO receipts, contracts, run-rate; auto-reverse; consistent estimate method; track actual vs accrual |
| Prepaid amortisation | Expense by type | Prepaid | Schedule with start, end and monthly amount; accelerate on cancellation; add new prepaids promptly |
| Depreciation and amortisation | Depreciation expense by department | Accumulated depreciation | Run from the asset register; new additions set up with life and method; disposals and impairments flagged |
| Payroll accrual | Salary, bonus, benefits, employer tax expense | Accrued payroll, benefits, payroll taxes | Working days in the period versus pay period; bonus per plan terms; include employer taxes and leave liability where required |
| Revenue earned, not billed | Contract or accrued asset | Revenue | Timesheet or signed milestone; reverse on invoicing |
| Release of deferred revenue | Deferred revenue | Revenue | Tied to the service term or milestone |
| Revenue received in advance | Cash or AR | Deferred revenue | Contract-level detail kept |
| Reclassification | Correct account | Wrong account | Original entry referenced; current period if the prior one is filed |

Depreciation methods: straight-line (cost less salvage, over life), declining balance, units of production. Use the client's stated method. For contract revenue, apply the applicable standard (ASC 606 or IFRS 15) per `revenue-recognition-606` where it exists; this skill covers routine mechanics only.

Worked example, annual insurance 12,000 paid 1 January and expensed in full by mistake, reclassed at end of January:

```
Dr Prepaid insurance     11,000
  Cr Insurance expense         11,000
Memo: 2026-01: reclass 11 months of annual premium paid 1 Jan to prepaid; source policy and payment.
Then monthly:  Dr Insurance expense 1,000   Cr Prepaid insurance 1,000
```

## 4. Construct the entry

1. State the economic event in words ("March rent due but unbilled").
2. Identify accounts affected and their normal balances.
3. Compute the amount in a visible schedule, not in your head.
4. Write lines and prove debit total equals credit total.
5. Sanity check statement impact: which line moves, by how much, in which direction, and whether it crosses materiality.
6. Check the books first: an entry already posted for the same period and memo is done, not drafted twice.

## 5. Reversing versus permanent

- **Auto-reversing**: accruals for expected invoices or unbilled revenue. Dated the last day, reversed on day one of the next period so the real document books normally. After reversal confirm nothing is left behind: a reversed accrual with no bill means the bill is missing; a bill with no reversal means double expense.
- **Permanent**: depreciation, amortisation, true reclassifications, corrections.
- **Corrections**: reverse the wrong entry and post the right one, never overwrite. If only part is wrong, post the difference with a narrative referencing the original.

## 6. Approval matrix (set thresholds per client materiality)

| Entry type | Example threshold | Approver |
|---|---|---|
| Standard recurring | Any amount | Accounting manager |
| Non-recurring or manual | Under 50,000 | Accounting manager |
| Non-recurring or manual | 50,000 to 250,000 | Controller |
| Non-recurring or manual | Over 250,000 | CFO or finance head |
| Top-side or consolidation | Any amount | Controller or above |
| Out-of-period adjustments | Any amount | Controller or above |

Entries to equity, tax, intercompany, revenue or related-party accounts, anything posted after soft close, and any non-routine entry need review regardless of amount. The preparer never approves their own. In a one-person team the owner reviews the journal listing monthly.

Draft then confirm: show the entry with lines, support and impact; mark it approved only on explicit confirmation, and record who and when. An approval mark of unknown provenance is a proposal to re-confirm.

## 7. Reviewer checklist

1. Debits equal credits; date in an open, correct period.
2. Accounts exist and are right; direction is right (check normal balances).
3. Amount recomputed independently from support.
4. Memo is specific; support attached and external or a signed-off schedule.
5. Department, project, tax and currency populated.
6. Treatment consistent with prior periods and policy; reversal flag correct.
7. Within the preparer's authority; not a duplicate.
8. Unusual patterns explained: round numbers, weekend or just-before-close posting, large reversal with no original, suspense entries that never clear.

## 8. Common errors to catch

Unbalanced entry; wrong period or already-closed period; wrong sign; duplicate; wrong account (similar codes); missing reversal; stale recurring accrual; suspiciously round estimate; wrong FX rate or date; missing intercompany elimination; capitalisation error either way; cut-off error against delivery or service date.

## 9. Journal listing review (detective control)

Each close pull all manual journals: sort by amount, preparer and account sensitivity. Look for entries without support or approval, posted after lock, or repeated corrections of one issue (a root cause to fix upstream).

## 10. Import file

One CSV per close, approved entries only, columns `entry_no,date,account,memo,debit,credit`; format and invariants in [references/je-csv-format.md](references/je-csv-format.md). Nothing is posted by this skill; the CSV is the handoff and the user imports it with the accounting system's journal import.

## Output

The formatted entry (date, ref, account, debit, credit, memo), the supporting schedule, a comparison with the prior period's entry of the same type, statement impact in one line, approval status, items flagged for follow-up, and the CSV path or "not emitted: not approved".

## Do not

- Post to a locked or filed period; request a controlled reopen or post in the current period with a prior-period note.
- Post a balancing line to suspense, retained earnings or "other" to make an entry foot.
- Post journals directly to AR, AP or inventory control accounts.
- Leave an accrual without a reversal plan.
- Use a vague memo ("adjustment", "per discussion").
- Present model arithmetic as fact: figures come from the cited source or an authorised policy.
