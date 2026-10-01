---
name: qbo-data-cleanup
description: >-
  Clean up a messy QuickBooks Online file: duplicate customers, vendors and transactions, Uncategorized Expense/Income/Asset and Ask My Accountant balances, stuck Undeposited Funds, Opening Balance Equity, unapplied payments and credits, inactive-but-used records, and wrong-period postings. Use when asked to "clean up this QuickBooks file", "fix uncategorized transactions", "remove duplicate customers", "Opening Balance Equity has a balance", "Undeposited Funds is huge", "take over a messy QBO", or "catch-up bookkeeping review".
metadata:
  department: "accounting"
  domain: "data-cleanup"
  platform: "quickbooks"
  owner: "satva-coe"
  status: "stable"
  license: "Satva-original"
  source: "original"
---

# QuickBooks data clean-up

Order matters: diagnose everything read-only, agree a plan, then fix in the safest order, then re-run the diagnostics. Every write follows `qbo-mcp-operating-rules` (diff, approval, read-back). Keep a clean-up log: id, before, after, reason, who approved.

## Phase 1: diagnose (read-only)
Run each and keep the numbers.
1. `get_company_overview` and `get_trial_balance` at today's date. Note the starting balance of every catch-all account.
2. **Catch-all postings**: `uncategorized_transactions` (default last 365 days; set `start_date`/`end_date` to cover the whole file in chunks). It covers any account named `Uncategorized ...` (Expense, Income, Asset) and `Ask My Accountant`, up to 6 accounts; if it lists `accountsNotSearched`, run the rest with `get_general_ledger` and `account`.
3. **Duplicates**: `find_duplicates` for each of `customers`, `vendors`, `invoices`, `bills`, `purchases`. Customers and vendors match on normalised name (case, punctuation and Inc/LLC/Ltd ignored), email and phone; transactions match on same party, same amount, dates within `windowDays` (default 3), or a repeated document number. Results are POTENTIAL duplicates: nothing is changed.
4. **Control-account noise**: `get_general_ledger` on Accounts Receivable, Accounts Payable, Undeposited Funds, Opening Balance Equity, Retained Earnings. Look for journal entries, odd sources and old items.
5. **Unapplied items**: `query_quickbooks` `SELECT Id, CustomerRef, TotalAmt, UnappliedAmt, TxnDate FROM Payment WHERE UnappliedAmt > '0'` and open credit memos (`SELECT Id, CustomerRef, Balance FROM CreditMemo WHERE Balance > '0'`). Vendor side: `SELECT Id, VendorRef, TotalAmt FROM VendorCredit` (QBO does not expose an unapplied balance on vendor credits; read `LinkedTxn` to see if applied).
6. **Aged items**: `get_aged_receivables` and `get_aged_payables`; invoices and bills older than 12 months, uncleared bank items older than 90 days (`get_transaction_list` with `cleared: "Uncleared"`).
7. **Inactive but used**: `query_quickbooks` `SELECT Id, Name, CurrentBalance FROM Account WHERE Active = false` and look for non-zero balances; same idea for inactive customers with open balances.
8. Write the findings table: issue, count, amount, risk, proposed fix, order.

## Phase 2: fix in this order (safest first)
1. **Catch-all postings to proper accounts.** For each transaction: decide the right account from the payee's history (`query_quickbooks` last 5 transactions for that vendor), the memo and the amount. Fix on the source transaction with `update_entity` (`Purchase`, `Bill`, `Deposit` are full-update entities: send the complete `Line` array and keep other fields). If many items have the same cause, ask the user for a rule rather than guessing one by one. Items you cannot classify stay in the catch-all and go on a question list: ask, do not guess. After posting, re-run `uncategorized_transactions` and confirm the account balance fell by exactly the amount moved. A transaction in a reconciled period: tell the user that changing the account (not the amount or date) does not alter the bank balance, but do it only with approval.
2. **Opening Balance Equity.** It should be zero after the first period. A balance means opening balances were entered as transactions or journal entries instead of properly. Find the lines with `get_general_ledger` on that account. Typical resolution (accountant's decision): reclass to the correct prior-period retained earnings, or to the correct balance sheet account if the opening entry was mis-coded, via a dated journal entry (`qbo-journal-entries`). Never zero it with a plug to income or expense.
3. **Undeposited Funds.** Customer payments recorded without a bank deposit. Match them to the bank deposit lines and record a `Deposit` that includes those payments (`create_entity` `Deposit`, lines linking `Payment`s). Where the bank received the money directly and a deposit already exists as an income line, the revenue is double counted: remove the duplicate income line by editing that deposit.
4. **Duplicate customers/vendors.** QuickBooks merges two records when one is renamed to exactly the other's name and the types match; the merge is permanent. For each pair: confirm same entity (tax id, address, email), pick the survivor (the one with history and the fuller profile), compare balances, rename the loser to the survivor's exact `DisplayName` with `update_entity` (sparse for Customer; full-merge for Vendor), then verify with `customer_360` or `vendor_360` and the aging report. If a rename does not merge (a difference in type or sub-customer structure), deactivate the loser instead: `delete_entity` (sets `Active=false`) after moving any open items.
5. **Duplicate transactions.** For each flagged group, find which one is linked to a payment or reconciled. Keep that one. If the duplicate is unreconciled and unlinked, remove it: bills, expenses and journals with `delete_entity`; sent invoices with `void_invoice`. A reconciled duplicate is reversed with a credit memo, vendor credit or journal, not deleted.
6. **Unapplied payments and credits.** Apply them (`apply_payment_to_invoices` for the invoice side with `dryRun` first, and credit memo links as in `qbo-invoicing-and-collections`) or refund them. Leave nothing floating without a decision.
7. **Stale uncleared and ancient open items.** Old uncleared cheques: ask whether they were voided or lost; if void, record a reversing deposit or void the cheque entry per policy. Ancient unpaid invoices: bad-debt write-off by credit memo to a bad-debt expense account, with approval.
8. **Inactive accounts with balances**: reactivate (`update_entity` `Active:true`), move the balance by journal, deactivate again.

## Phase 3: verify and report
Re-run Phase 1 queries. Targets: catch-all balances at 0 or listed with questions, Opening Balance Equity 0, Undeposited Funds only recent, no unflagged duplicates, A/R and A/P aging equals control accounts, trial balance balanced. Provide before/after counts and amounts.

## Rules
- Do not mass-edit. `batch_operations` (max 10 items, independent, results include per-item Fault) is for the safe, uniform subset only, after a sample of three has been approved and verified.
- Never delete a customer or vendor with transactions: QuickBooks deactivates them; hard delete is not available once used.
- Do not change dates or amounts on transactions in closed or filed periods; post a current-period entry.
- Re-run `find_duplicates` after fixes. A bank-feed re-import is the usual cause of the same duplicates returning.
- Identify and stop the cause (rules for the bank feed, duplicate entry by two users, import without de-duplication). Fixing symptoms only means doing it again next month.

## Output
Findings table, the plan with order and expected balance effects, the clean-up log, verification results, and the list of questions needing the owner or accountant.
