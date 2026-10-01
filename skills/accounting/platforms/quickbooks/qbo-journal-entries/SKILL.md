---
name: qbo-journal-entries
description: >-
  Prepare, post, correct and reverse journal entries in QuickBooks Online: accruals, prepayments, reclassifications, depreciation, payroll and loan postings, with the A/R and A/P entity rules, class/location on lines, and reversing entries. Use when asked to "post a journal entry in QuickBooks", "reclass these transactions", "book the accrual", "reverse last month's entry", "adjusting entries", "fix this with a journal", or "why is QBO asking for a name on a journal line".
metadata:
  department: "accounting"
  domain: "journal-entries"
  platform: "quickbooks"
  owner: "satva-coe"
  status: "stable"
  license: "Satva-original"
  source: "original"
---

# QuickBooks journal entries

A journal entry (JE) is the most powerful and least visible write in QuickBooks. It bypasses every subledger. Use it only when no native transaction does the job, and always with a supporting document. Follow `qbo-mcp-operating-rules`.

## When NOT to use a JE
| Need | Use instead |
|---|---|
| Move money between own bank accounts | `Transfer` |
| Pay a card balance from bank | `CreditCardPayment` |
| Fix a customer balance | `CreditMemo`, `Payment`, or void the invoice |
| Fix a vendor balance | `VendorCredit`, `BillPayment` |
| Bank fee, interest | `Purchase` or `Deposit` |
| Change the account on one expense | Edit that `Purchase`/`Bill` line (`update_entity`) |
A JE touching Accounts Receivable or Accounts Payable does NOT update an invoice or bill balance and often leaves the aging report and the balance sheet disagreeing. Avoid it unless the user's accountant specifically wants it.

## Workflow
1. **Purpose and source.** Capture: period, reason, supporting document (invoice, schedule, calculation), who approves. No document, no entry.
2. **Check period status.** If the date is before the company's closing date, QBO rejects or warns; do not backdate around it. Ask the controller.
3. **Check features.** `get_company_overview`: class/location tracking, multicurrency, home currency.
4. **Resolve accounts.** `query_quickbooks` `SELECT Id, Name, AccountType, Active FROM Account WHERE Name LIKE '%Prepaid%'`. Use Ids. Active accounts only (an inactive account errors with 6240).
5. **Build and prove it balances in cents.** Sum debits and credits as integers; they must be equal. Round per line, put the cent difference on a named rounding line, never on a random line.
6. **Show the entry** as a table (account, debit, credit, name, class, location, description) with date, `DocNumber` and `PrivateNote`; ask for approval.
7. **Post**: `create_entity` `JournalEntry` (or `create_journal_entry` with `journalEntry` = the body).
8. **Verify**: `get_entity` `JournalEntry`, then `get_trial_balance` (still balanced) and the affected accounts via `get_general_ledger` with `account` = Id.

## Body shape
```
{
  "TxnDate": "2026-06-30",
  "DocNumber": "AJE-2026-06-01",
  "PrivateNote": "June accrual: contractor invoice not yet received. Support: timesheet 2026-06.",
  "Line": [
    {"DetailType":"JournalEntryLineDetail","Amount":1200.00,
     "Description":"Contractor fees accrued",
     "JournalEntryLineDetail":{"PostingType":"Debit","AccountRef":{"value":"<expense id>"},
        "ClassRef":{"value":"<class id>"}}},
    {"DetailType":"JournalEntryLineDetail","Amount":1200.00,
     "JournalEntryLineDetail":{"PostingType":"Credit","AccountRef":{"value":"<accrued liabilities id>"}}}
  ]
}
```
`Amount` is always positive; the side is `PostingType`. `describe_entity` `JournalEntry` returns the current required fields.

## QuickBooks-specific rules
- **Names on control accounts.** A line to Accounts Receivable needs a customer, a line to Accounts Payable needs a vendor, in `JournalEntryLineDetail.Entity` (`{"Type":"Customer","EntityRef":{"value":"<id>"}}`). Without it QBO rejects the entry.
- **Class and location** are per line (`ClassRef`, `DepartmentRef` in the line detail). If the company requires class on every line and you omit it, the P&L by class shows "Not specified". Balance sheet lines do not need a class.
- **Multicurrency JE.** Currency is set on the entry (`CurrencyRef`, `ExchangeRate`); all lines use that currency, and A/R and A/P lines must use accounts in that currency. See `qbo-multi-currency`.
- **Tax.** JE lines do not calculate sales tax. A tax adjustment via JE will not appear on the sales tax liability or filing reports unless the tax centre is adjusted separately; say so before booking one.
- **`Adjustment` flag** (`"Adjustment": true`) marks the entry as an accountant adjustment; useful for year-end entries, but only if the accountant's workflow uses it.
- **Account types cannot be fixed by JE.** If an account's type is wrong, create the right account and reclass.

## Common entries
| Entry | Debit | Credit | Reverse? |
|---|---|---|---|
| Accrued expense | Expense | Accrued liabilities | Yes, first day of next period |
| Accrued revenue | Accrued income (asset) | Revenue | Yes |
| Prepaid expense amortisation (month n of N) | Expense | Prepaid asset | No (schedule) |
| Depreciation | Depreciation expense | Accumulated depreciation | No (schedule) |
| Deferred revenue release | Deferred revenue | Revenue | No |
| Reclass between expense accounts | New account | Old account | No |
| Correct a mispost to the wrong class | Same account, right class | Same account, wrong class | No |
| Loan: interest and principal split | Interest expense and Loan liability | Bank | No |
Payroll provider summaries: debit wages, employer taxes, benefits; credit liabilities and bank; map each provider line to a QBO account once and reuse; never rebuild from the bank feed alone.

## Reversals and corrections
- **Reversing accrual**: create a second JE dated the first day of the next period, the same lines with `PostingType` swapped, `DocNumber` suffix `-R`, `PrivateNote` referencing the original. Prepare both together and get both approved.
- **Wrong entry, open period**: `update_entity` `JournalEntry` (sparse; send the complete `Line` array, as arrays are replaced) or `delete_entity` if nothing depends on it.
- **Wrong entry, closed period or already reported**: do not edit or delete. Post a correcting JE in the current period and explain it.
- Bulk reclass of many transactions: use one JE per source account and period, not one per transaction; keep a list of the transaction ids in `PrivateNote` or an attached file (`upload_attachment`, `attachTo: [{type:"JournalEntry", id}]`).

## Review a company's existing JEs
`query_quickbooks` `SELECT * FROM JournalEntry WHERE TxnDate >= '2026-01-01' ORDERBY TxnDate DESC MAXRESULTS 200`. Flag: round numbers without a note, JEs to A/R or A/P, JEs to Retained Earnings or Opening Balance Equity, entries by a non-accountant user (`MetaData`), unbalanced class assignments, and entries without `DocNumber` or `PrivateNote`.

## Output
The entry table (balanced, with totals), supporting reference, tool call body, verification result (trial balance still balances; ledger lines show), and the reversal plan.
