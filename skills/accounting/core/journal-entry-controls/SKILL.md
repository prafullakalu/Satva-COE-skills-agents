---
name: journal-entry-controls
description: >-
  Prepare manual and adjusting journal entries with proper debit/credit structure, support, approval and reversal, then post only after review. Use for "post a journal", "adjusting entry", "reclass", "correct a mistake", "reversing entry", "journal entry review", or "manual journal approval".
metadata:
  department: "accounting"
  domain: "journal-entries"
  owner: "satva-coe"
  status: "beta"
  license: "Satva-original"
  source: "original"
---

# Journal entry controls

A manual journal bypasses the controls built into invoices, bills and bank matching. It therefore needs more evidence, not less.

## 1. When a journal is the right tool

Use a journal for: accruals and deferrals, depreciation and amortisation, reclassifications, corrections of coding errors, revaluations, intercompany and eliminations, opening balances, period-end estimates. Do not use a journal to fix something a source document should fix (a wrong bill amount is corrected on the bill or with a credit note) or to touch control accounts such as AR, AP or inventory directly; those are changed through their subledger so the subledger and ledger still agree.

## 2. Required content of every entry

| Element | Standard |
|---|---|
| Entry date | In the period the economics belong to; period must be open |
| Reference | Unique, sequential or coded by type (ACC-2026-03-01) |
| Narrative | What, why, period covered, in one sentence a stranger can follow |
| Lines | Account, debit or credit, amount, tax code if relevant, dimension (department, project) |
| Currency | Entity functional currency; foreign lines show currency and rate |
| Support | Calculation, contract, invoice, schedule or statement, attached or linked |
| Preparer, reviewer, approver | Distinct people above the approval threshold |
| Recurring or reversing flag | Stated at creation |

Total debits must equal total credits to the cent. One entry should address one purpose so it can be reviewed and reversed independently.

## 3. Construct the entry

1. State the economic event in words ("rent for March was due but unbilled").
2. Identify the accounts affected and their normal balances.
3. Compute the amount in a visible schedule (not in your head).
4. Write lines and check that debit total equals credit total.
5. Sanity check the effect on the statements: which line moves, by how much, in the right direction, and does it cross a materiality threshold.

Worked example, one month of insurance paid annually up front (12,000 paid in January, expensed in full by mistake):

```
Dr Prepaid insurance       11,000
  Cr Insurance expense           11,000
Narrative: reclass 11 months of the annual premium paid on 1 Jan to prepaid; support: policy and payment.
Then monthly:  Dr Insurance expense 1,000  Cr Prepaid insurance 1,000
```

## 4. Reversing versus permanent

- **Auto-reversing**: accruals for expected invoices or unbilled revenue. Post at period end dated the last day; reverse on day one of the next period. The real document then books normally without double counting.
- **Permanent**: depreciation, amortisation, true reclassifications, corrections.
- **Corrections**: reverse the incorrect entry and post the correct one, rather than overwriting. The audit trail should show both. If only part is wrong, post the difference with a narrative referencing the original entry.

## 5. Approval and threshold

Set per client: entries above the threshold, any entry to equity, tax, intercompany, revenue or related-party accounts, any entry posted after the soft close, and any non-routine entry, need reviewer approval. Preparer cannot approve their own. Where the team is one person, the owner reviews the journal listing monthly.

Draft then confirm: present the entry (lines, support, impact) and post only after approval. Record who approved and when.

## 6. Review checklist for the reviewer

1. Debits equal credits; date in the right period.
2. Accounts are right and the direction is right (check normal balances).
3. Amount recomputed independently from support.
4. Narrative and support attached; support is external or a signed-off schedule.
5. No unusual pattern: round numbers, posting on weekends or just before close, large reversal with no original, entries to suspense that never clear.
6. Tax and currency handled; dimensions populated.

## 7. Journal listing review (detective control)

Each close, pull all manual journals for the period: sort by amount, by preparer, by account sensitivity. Look for entries without support, without approval, posted after lock, or repeated corrections of the same issue (a root cause to fix upstream).

## Output

The journal as a table (date, ref, account, debit, credit, narrative), the supporting schedule, the statement impact in one line, and the approval status.

## Do not

- Post to a locked or filed period; request a controlled reopen, or post in the current period with a prior-period-adjustment note.
- Post a balancing line to suspense, retained earnings or "other" to make an entry foot.
- Post journals directly to AR, AP or inventory control accounts.
- Leave an accrual without a reversal plan.
- Use a vague narrative ("adjustment", "per discussion").
