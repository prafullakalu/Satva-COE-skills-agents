---
name: subledger-to-gl-reconciliation
description: >-
  Reconcile general ledger control and balance-sheet accounts to their supporting detail: AR and AP to agings, prepaids and accruals to schedules, loans to lender statements, payroll and tax liabilities to returns, clearing accounts to zero. Use for "tie AR to the GL", "AP subledger does not match", "balance sheet reconciliation", "account analysis", "clearing account not zero", or "reconciliation certificate".
metadata:
  department: "accounting"
  domain: "reconciliation"
  owner: "satva-coe"
  status: "beta"
  license: "Satva-original"
  source: "original"
---

# Subledger and balance-sheet reconciliation

Principle: every balance sheet account has an independent source of truth, an owner, a frequency, and a tolerance. A balance with no support is an unreconciled balance.

## 1. Reconciliation register

Keep one row per balance sheet account: account, supporting source, owner, reviewer, frequency (monthly for risky accounts, quarterly for stable ones), risk rating, tolerance, last reconciled date. Cash and clearing accounts monthly, always.

| Account | Support to tie to |
|---|---|
| Accounts receivable control | AR aging as of the same date and time |
| Accounts payable control | AP aging as of the same date |
| Prepaids | Amortisation schedule (`accruals-deferrals-prepaids`) |
| Accrued liabilities | Accrual listing with calculations |
| Deferred revenue | Contract or release schedule |
| Inventory | Valuation report from stock records |
| Fixed assets and accumulated depreciation | Asset register |
| Loans | Lender statement (principal and accrued interest) |
| Payroll liabilities | Payroll register and remittance confirmations |
| Sales tax, VAT/GST | Tax return workings; the filed return amount |
| Payment processor or undeposited funds clearing | Processor reports and bank |
| Intercompany | Counterparty ledger (`intercompany-tie-out`) |
| Equity | Roll-forward from prior closing balances |

## 2. Procedure for any account

1. Pull the ledger balance at the cut-off date, and the support at the same date and time. Aging reports run on a different day than the ledger will differ for reasons unrelated to error.
2. Compute the difference. Zero within tolerance: document and sign.
3. Otherwise decompose the difference into specific items, each with amount, date, cause and owner.
4. Determine cause class: timing (batch posted next day), manual journal posted to a control account, subledger transaction not interfaced, backdated entry after the report was run, reclass without subledger adjustment, system or integration failure, error.
5. Resolve: correct the source (reverse the manual journal to control, repost the failed transaction), or document a genuine timing item with expected clearing date.
6. Re-run the comparison; difference should now be only documented timing items.

Diagnostic shortcuts: compare activity not balance (this period's ledger movement versus subledger movement) to isolate the month the break began; check for a single entry equal to the difference or half of it; sort manual journals to the control account in the period; check entries dated after the report-run time.

## 3. Account-specific points

- **AR and AP**: credits and unapplied payments must be inside both ledger and aging; a debit-balance AP vendor or credit-balance AR customer is reclassified for presentation if material. Foreign-currency items revalued consistently in both.
- **Clearing accounts**: expected balance is zero or a small in-transit amount that clears next period. Items older than 30 days are investigated.
- **Prepaids and accruals**: aged items released or justified; check amortisation ran for every month.
- **Loans**: split current and non-current at reporting; accrued interest tied to the statement.
- **Payroll and tax**: balance equals what is due and not yet remitted. After remittance the account should return to the expected liability for the unpaid period only.
- **Suspense**: should be zero at close; any balance is listed with age and owner.

Break buckets (matched, amount, quantity, timing, GL-only, subledger-only), likely-cause tags, the one-sentence root-cause format, reconciling-item categories, ageing bands and example escalation thresholds are in `references/break-analysis-and-escalation.md`.

## 4. Tolerances and escalation

Define tolerance per account type (for example zero for cash and tax, a small absolute amount for high-volume subledgers). Differences above tolerance, any difference older than two periods, and any unsupported manual journal to a control account are escalated to the reviewer and recorded.

## 5. Reconciliation certificate

For each reconciled account record: account, date, ledger balance, supporting balance, difference and its composition, preparer and date, reviewer and date, evidence location, open items and expected resolution. Review confirms the support is independent (not generated from the ledger itself) and that the reviewer re-performed at least one line.

## Output

Register status (reconciled, overdue, exceptions), certificate for each account done, break analysis for any failures, and proposed correcting entries as drafts.

## Do not

- Reconcile a ledger to a report that is derived from the same ledger.
- Plug differences to retained earnings or "miscellaneous".
- Mark an account reconciled with items older than policy and no action.
- Post manual journals to control accounts to force agreement.
