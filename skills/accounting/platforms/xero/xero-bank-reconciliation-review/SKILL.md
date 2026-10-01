---
name: xero-bank-reconciliation-review
description: >-
  Reviews bank reconciliation health in Xero using the Satva Xero MCP: bank summary movement, unreconciled
  transactions, stale items, suspense postings, bank transfers between own accounts, bank-rule side effects, and
  recording missing spend/receive money items. Use for "is the bank reconciled", "unreconciled items in Xero",
  "bank rec review", "bank feed has duplicates", "transfer between accounts", "month-end bank check". It reviews and
  records transactions; it cannot match statement lines (the MCP has no statement-line tool).
metadata:
  department: "accounting"
  domain: "reconciliation"
  platform: "xero"
  owner: "satva-coe"
  status: "stable"
  license: "Satva-original"
  source: "original"
---

# Xero bank reconciliation review

Follow `xero-mcp-operating-rules`. For platform-neutral reconciliation theory, the core accounting skills apply; this
skill is what is possible and risky inside Xero with this MCP.

## What the MCP can and cannot do

Can: read bank transactions with their `Reconciled/Unreconciled` flag (`list-bank-transactions`), read the bank
summary report (`list-report-bank-summary`), list accounts, payments, bank transfers, overpayments/prepayments; create
RECEIVE/SPEND bank transactions, bank transfers, payments and batch payments.

Cannot: read bank statement lines waiting in the "Reconcile" tab, accept/match/create from a statement line, create or
edit bank rules, or connect/repair a bank feed. Statement-line matching must be done by a person in Xero. Say this at
the start; do not imply the review proves the statement-line queue is empty.

## Workflow

1. **Select org and bank account.** `list-accounts`, filter Type=BANK; note each `ID` (needed as `bankAccountId`).
2. **Movement and balance view.** `list-report-bank-summary fromDate toDate` (needs the bank-summary scope; if 401,
   see operating rules). Record opening, cash in/out, closing per account for the period.
3. **Unreconciled population.** `list-bank-transactions bankAccountId=<id> page=1..n`. Collect rows flagged
   Unreconciled. Also scan rows with status other than AUTHORISED.
4. **Triage unreconciled rows** into: (a) recent, normal timing; (b) older than 30 days (stale); (c) duplicates
   (same date, amount, contact, reference); (d) posted to a suspense/clearing account; (e) one half of an inter-bank
   transfer; (f) round-sum or unusual contacts.
5. **Payments side.** Payments against invoices that were made but not reconciled appear via `list-payments`;
   cross-check the amounts with the bank list for the same dates.
6. **Report** the reconciliation position (formula below) and the item list. Recommend actions; make no changes until
   confirmed.
7. **Make approved entries only** (section "Recording items").

## Reconciliation position

```
Statement balance (from the bank, supplied by the user)
 - outstanding payments (in Xero, not yet on statement)
 + outstanding receipts
 = adjusted bank balance
Xero book balance (bank summary closing, or balance sheet bank line)
Difference must be 0 after unreconciled statement lines are accounted for.
```

The statement balance must come from the user or an uploaded statement. Never infer it from Xero.

## Pitfalls specific to Xero

- **Bank rules fire at accept time.** A rule can auto-code lines to the wrong account or tax type, or two rules can
  overlap (the first by priority wins). A cluster of transactions coded to the same unexpected account is a rule
  conflict symptom; report the pattern and have a user fix the rule in Xero.
- **Duplicate entry.** If a payment is both recorded against an invoice and later also entered as a SPEND/RECEIVE
  bank transaction, income/expense is double counted. Before creating any bank transaction, search `list-payments` and
  `list-bank-transactions` for the same amount and date.
- **Transfers.** Money between own accounts is a bank transfer (`create-bank-transfer`, `list-bank-transfers`), never
  a spend on one side and a receive on the other. Both legs on a bank transfer reconcile separately in Xero.
- **Suspense accounts.** Items coded to "Suspense", "Uncategorised" or "Ask my accountant" must end at zero; list them
  with their original statement description and propose a real account. See `xero-org-and-chart-review`.
- **Locked periods.** A bank transaction dated on or before the period lock date is rejected. Do not date it after the
  lock to get it through; tell the user.
- **Reconciled items are protected.** `update-bank-transaction` re-sends all line items (omitted lines are removed)
  and Xero restricts edits to reconciled transactions. Do not try to "unreconcile" through this MCP.
- **Foreign-currency accounts.** Reconcile in the account's currency; compare to the bank statement, not base-currency
  totals. See `xero-multi-currency`.
- **Feed gaps.** A closing balance difference with no unreconciled Xero rows usually means statement lines are
  missing from the feed, or lines were deleted. Ask a user to compare statement line counts.

## Recording items (after confirmation)

- Missing bank fee/interest: `create-bank-transaction type=SPEND|RECEIVE bankAccountId contactId lineItems[]
  date reference`. Each line needs `description, quantity, unitAmount, accountCode, taxType`; get the codes from
  `list-accounts` and `list-tax-rates`. It posts immediately as AUTHORISED.
- Transfer: `create-bank-transfer fromBankAccountId toBankAccountId amount date`.
- Pay a bill or invoice: `create-payment invoiceId accountId amount date reference` (invoice must be AUTHORISED).
- Pay several bills in one bank line: `create-batch-payment` (the statement shows one debit).
- A wrong entry made through this MCP: `delete-payment` for payments, or reverse with a corrective transaction;
  there is no tool that deletes a bank transaction.

## Output format

```
Org / bank account / period / as-at
Position: statement <x> | adjusted <y> | Xero <z> | difference <d>   (or "statement balance not provided")
Unreconciled: <n> items, <sum>; stale >30d: <n>; duplicates suspected: <n>; in suspense: <n>
Table: date | contact | reference | amount | bucket | recommended action
Needs a person in Xero: statement lines to accept/match, bank-rule fixes
```
