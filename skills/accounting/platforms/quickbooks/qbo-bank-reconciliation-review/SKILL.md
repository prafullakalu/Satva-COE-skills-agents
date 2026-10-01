---
name: qbo-bank-reconciliation-review
description: >-
  Review bank, credit card and Undeposited Funds accounts in QuickBooks Online and prepare a reconciliation: find uncleared and stale items, duplicates, transfers booked twice, payments stuck in Undeposited Funds, and uncategorised postings, then explain a reconciliation difference. Use when asked to "reconcile the bank in QuickBooks", "why doesn't the QBO bank balance match the statement", "what is sitting in Undeposited Funds", "bank feed review", "find the reconciliation difference", or "check cleared vs uncleared".
metadata:
  department: "accounting"
  domain: "reconciliation"
  platform: "quickbooks"
  owner: "satva-coe"
  status: "stable"
  license: "Satva-original"
  source: "original"
---

# QuickBooks bank and card reconciliation review

## What the tools can and cannot do (verified in the server)
- CAN read accounts and balances (`search_accounts`, `get_account`, `cash_position`), ledger detail (`get_general_ledger`, `get_transaction_list`, `get_transaction_list_with_splits`) with a `cleared` filter, and create deposits, transfers, purchases and journal entries.
- CANNOT see bank-feed items still waiting in the Banking tab (the `uncategorized_transactions` tool says so explicitly), and no tool exposes the Reconcile screen: you cannot mark items cleared or finish a reconciliation. The final tick-and-finish is done by a person in QuickBooks. Your job is to prepare it and explain differences.
- Never "fix" a reconciliation difference by posting a plug to an expense or to Reconciliation Discrepancies without finding the cause.

## Inputs to get from the user
Statement ending date, ending balance, and the account (name or Id). If the user has no statement, say the review can only test internal consistency, not agreement to the bank.

## Workflow
1. **Identify the account.** `query_quickbooks` `SELECT Id, Name, AccountType, CurrentBalance FROM Account WHERE AccountType IN ('Bank','Credit Card') AND Active = true`, or `cash_position` for every active bank and card account with `CurrentBalance`. Note Id and `CurrentBalance`.
2. **Book balance at statement date.** `get_balance_sheet` with `end_date` = statement date (set `accounting_method` to match; bank balances do not depend on basis). Read the bank account line. This is the "QuickBooks balance" to compare to the statement. `CurrentBalance` on the account is as of today, not statement date.
3. **Cleared vs uncleared.** `get_transaction_list` with `account` = the Id, `start_date`/`end_date` bounding the statement period, and `cleared: "Uncleared"`; repeat with `cleared: "Cleared"` or `"Reconciled"` as needed. Use `columns: "tx_date,txn_type,doc_num,name,memo,subt_nat_amount"` to keep output small.
4. **Proof formula.** Statement ending balance
   = QuickBooks book balance at statement date
   + uncleared withdrawals/cheques (still outstanding at the bank)
   - uncleared deposits (in transit)
   +/- items the bank has that QuickBooks lacks (fees, interest, unrecorded transfers).
   Work in cents; state each term. If the proof does not close, the remaining difference is the number to explain.
5. **Hunt the difference**, cheapest explanation first:
   - A transaction dated after the statement date but cleared early, or before it but not cleared (check dates, not just amounts).
   - A single amount equal to the difference, or half of it (a sign error shows as 2x the amount; transposition shows as a multiple of 9).
   - Duplicates: `find_duplicates` with `kind: "purchases"` (and `"bills"`) for the same payee, amount, within a few days. A bank-feed item added AND a manually entered expense is the usual cause.
   - Transfers booked twice (once from each side, or as expense and as transfer): look for equal and opposite amounts across two bank accounts on the same date in `get_transaction_list` for each.
   - Deposits: a bank deposit that is one lump sum made up of several customer payments must be recorded as one `Deposit` that includes those payments (see below).
   - Voided or deleted cleared transactions after a prior reconciliation: `get_general_ledger` plus the account's last reconciled balance shows the opening balance moved.
   - A changed amount on a previously reconciled item: `get_changes` with `entities: ["Purchase","Deposit","Payment","BillPayment","Transfer","JournalEntry"]` and `changedSince` = the last reconciliation date shows edits made since.
6. **Undeposited Funds.** `get_general_ledger` with `account` = the Undeposited Funds account Id lists what is parked there. Customer payments recorded without a deposit account (the default for `apply_payment_to_invoices` and QBO's Receive Payment) park in Undeposited Funds until a `Deposit` moves them. Expected balance at any date is only payments received but not yet banked. Anything older than about 5 business days is stale and needs a deposit or a correction.
   - Create the missing deposit with `create_entity` `Deposit`: `DepositToAccountRef` = the bank account, one line per payment with `LinkedTxn` `[{TxnId, TxnType:"Payment"}]` and `Amount`, so the payments leave Undeposited Funds. A `DepositLineDetail` line posts straight to an income or other account instead and will double count revenue if the invoice was already paid. Confirm with the user which they mean, read the deposit back, and check Undeposited Funds fell by the same amount.
7. **Uncategorised.** `uncategorized_transactions` for the period; each posting in `Uncategorized ...` or `Ask My Accountant` is a classification task, not a reconciliation item. Hand over to `qbo-data-cleanup`.
8. **Report** using the output format below. Offer the fixes as proposed entries; do not post without approval.

## Common posting fixes (all need a diff and approval, see `qbo-mcp-operating-rules`)
| Cause | Fix |
|---|---|
| Bank fee not recorded | `create_entity` `Purchase` (`PaymentType: "Cash"` or `"Check"`, `AccountRef` = bank, expense line to Bank Charges). |
| Transfer between own accounts coded as expense | Replace with a `Transfer` (`FromAccountRef`, `ToAccountRef`, `Amount`) after deleting or reclassing the expense. |
| Duplicate expense | Delete the unreconciled duplicate (`delete_entity`). If the duplicate is already reconciled, reverse with a journal entry instead. |
| Credit card payment booked as expense | Use `CreditCardPayment` (`create_entity`), home-currency accounts only. |
| Wrong period cut-off | Re-date the transaction (`update_entity` `TxnDate`) if the period is open; otherwise a journal entry in the right period. |

## Never
- Never delete or edit a transaction that already shows as reconciled without telling the user it will change the prior reconciliation's opening balance.
- Never accept a "difference" journal entry as the answer.
- Never declare the account reconciled: say "prepared; ready for the user to finish in QuickBooks".

## Output
- Header: account, Id, statement date, statement balance, QuickBooks balance at that date.
- Proof table with each reconciling item (date, type, payee, amount, status).
- Unexplained difference (cents) and the ranked hypotheses tested.
- Stale items list (older than 30 days uncleared) and Undeposited Funds list.
- Proposed entries, each with the exact tool and body, marked NOT POSTED.
