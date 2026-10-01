---
name: zoho-books-bank-reconciliation
description: >-
  Prepare and prove a bank or credit-card reconciliation for Zoho Books: gather what Zoho holds for the account and period, compare it with the statement, find unmatched, duplicate, mis-dated and uncategorised items, and hand the user an exact worklist. Use when asked to "reconcile the bank in Zoho", "why doesn't the bank balance match", "find missing payments", "what is uncategorised", or "prep the statement reconciliation". Read-mostly: the MCP cannot read feed lines or press Reconcile, so this skill produces evidence and a worklist.
metadata:
  department: "accounting"
  domain: "reconciliation"
  platform: "zoho-books"
  owner: "satva-coe"
  status: "beta"
  license: "Satva-original"
  source: "original"
---

# Zoho Books: bank reconciliation

Prerequisite: `zoho-books-operating-rules`. Tools available: `list_bank_accounts`, `list_chart_of_accounts` (with `showbalance`), `list_customer_payments`, `list_expenses`, `list_invoices`, `list_contacts`, `create_customer_payment`, `create_expense`.
Not available in the MCP: bank statement/feed lines, matching, categorising, the Reconcile action, bank transfers, vendor payments, journals. Say so up front, then do the preparation that makes the UI step quick.

## Inputs you need from the user

1. The account (name) and the period (statement start and end dates).
2. The statement closing balance and opening balance, and the statement lines (CSV or paste). Without the statement there is nothing to reconcile against; do not fabricate lines.

## Workflow

1. **Find the account.** `list_bank_accounts` (`filter_by=Status.Active`); take its `account_id`. Note currency; a foreign-currency account reconciles in its own currency.
2. **Ledger balance.** `list_chart_of_accounts` with `showbalance=true` for the same account: this is Zoho's book balance as of today, not as of the statement date. Money posted after the statement date explains the difference; list it in step 5.
3. **Pull what Zoho recorded for the period** (page to the end every time):
   - Money in: `list_customer_payments` filtered by date range; keep those whose deposit `account_id` or `account_name` is this account.
   - Money out: `list_expenses` with `paid_through_account_id` set to this account and the date range.
   - Other flows (vendor payments, transfers, journals, owner draws) are invisible here. Mark them "not visible to connector" so they are not misreported as missing.
4. **Match statement lines to Zoho records**, in this order (strongest first):
   1. Amount equal AND `reference_number` equal to the statement reference.
   2. Amount equal AND date within 5 days (banks post later than the payment date) AND counterparty name similar.
   3. One statement line equal to the sum of several Zoho records (batch deposit: Stripe, PayPal, cash banking). Test subsets of same-day records; never force a match that needs more than five records without telling the user.
   4. Same amount, opposite sign within a few days: probably a reversal or refund; flag, do not match.
5. **Classify every leftover item:**

| Bucket | Meaning | Action |
|---|---|---|
| Statement line, no Zoho record | Unrecorded receipt or payment, bank fee, interest | Propose the record (customer payment against which invoice, or expense with which account) |
| Zoho record, no statement line | Outstanding (cheque not cleared, deposit in transit) or wrongly dated | Keep if date is near period end; else query |
| Amount differs | Bank fee netted, FX difference, typo | Quantify the delta; fees go to a bank-charges expense |
| Duplicate in Zoho | Same amount/reference/date twice | Recommend deleting one in the UI, show both ids |
| Wrong date | Recorded in the wrong period | Re-date in the UI |

6. **Prove it.** Standard formula:
   `statement closing balance + deposits in transit - outstanding payments = adjusted bank balance`
   must equal the Zoho book balance at the statement date after the proposed entries. If the difference is not zero, state the exact residual and which bucket is incomplete. Never "plug" a difference into suspense or write off an unexplained residual without the user's sign-off.
7. **Writes (only on request, with confirmation).** `create_customer_payment` for an unrecorded receipt (see `zoho-books-invoices-ar` C), `create_expense` for fees and unrecorded payments. Always set `reference_number` to the bank reference. The final matching and "Reconcile" click are done in the UI (Banking > account > Reconcile).

## Common traps

- Statement signs: credits and debits are reversed between bank and ledger. Say which convention you used.
- Timezone and posting lag: month-end items land in the next statement.
- Gateway payouts (Stripe, PayPal) arrive net of fees on one line: reconcile via the gateway report first (`stripe-payout-fee-reconciliation`), then the deposit matches one lump.
- Credit-card accounts: payments to the card are transfers, not expenses.
- Opening balance mismatch means a prior period was reconciled wrongly or a reconciled item was edited. Stop and report; do not continue on a broken base.
- Reconciled items must not be edited. If the proof needs changing one, the user must un-reconcile in the UI.

## Output

1. Header: account, period, statement balances, Zoho balance, currency.
2. Matched count and total.
3. Worklist table per bucket: date, amount, reference, suggested action, confidence (high/medium/low).
4. The proof calculation with the residual.
5. What the user must do in the UI, in order.
