---
name: account-reconciliation-certification
description: >-
  Run the balance-sheet reconciliation certification programme for a close: build and risk-tier the reconciliation register, set frequency and tolerance, assign preparer and reviewer, test the evidence, sign the certificate, escalate overdue or unreconciled accounts, and report certification status to the close owner or auditor. Use for "reconciliation sign-off", "certify the balance sheet", "which accounts are not reconciled", "reconciliation review checklist", "reconciliation policy", "SOX reconciliation evidence", "reviewer re-performance". Companion to subledger-to-gl-reconciliation (how to reconcile one account); this skill governs the whole population.
metadata:
  department: "accounting"
  domain: "reconciliation"
  owner: "satva-coe"
  status: "beta"
  license: "Satva-original"
  source: "original"
---

# Account reconciliation certification

Reconciling one account is `subledger-to-gl-reconciliation`, `bank-reconciliation` and `credit-card-reconciliation`. Certification is the control over all of them: every balance-sheet account is reconciled, by the right person, on time, to independent evidence, reviewed, and signed. The close is not finished while any material account is uncertified.

## 1. The register
One row per balance-sheet account (or per account group where balances are small): account and entity, balance at last close, supporting source, preparer, reviewer, frequency, risk tier, tolerance, due working day, status, last certified date, open-item count and value. Generate the register from the chart of accounts so new accounts cannot escape it; an account with no row is a finding. Review the register each quarter and on every chart change.

## 2. Risk tier drives frequency and rigour

| Tier | Typical accounts | Frequency | Review |
|---|---|---|---|
| High | Cash, clearing and suspense, intercompany, payroll and tax liabilities, revenue-related deferrals, any account with manual journals or estimates | Monthly, by working day 3 to 5 | Reviewer re-performs a sample and ties evidence to source |
| Medium | AR, AP, inventory, fixed assets, accruals, loans | Monthly | Reviewer reviews differences, ageing and subsequent clearing |
| Low | Stable prepaids, equity, long-term balances with few movements | Quarterly or on movement | Reviewer reviews the roll-forward |

Rate on balance size, volume, manual-journal exposure, estimation, error history and fraud risk. Re-rate after any error or restatement.

## 3. Certification standard (all must be true)
1. **Independent support**: the balance is agreed to a source not generated from the ledger itself (bank or lender statement, aging run from the subledger, schedule, counterparty confirmation).
2. **Same date**: ledger balance and support are both at the cut-off, run after the ledger is final for the period.
3. **Difference explained**: every item has amount, cause class, owner and expected clear date. "Unknown difference" is not an explanation. A residual under tolerance is listed, never silently plugged.
4. **Ageing**: items over 30, 60 and 90 days are shown with action; items past policy are escalated (ageing and escalation table in the `subledger-to-gl-reconciliation` references).
5. **Segregation**: preparer and reviewer are different people and the reviewer is senior; neither sole-controls transactions in the account. Where the team is one person, the owner reviews and the limitation is recorded.
6. **Evidence retained**: reconciliation, support, open-item list, correspondence and review notes are stored where the auditor can find them, and the file is locked after sign-off. A later change needs reversal and a note.
7. **Timeliness**: certified within the close calendar. Late certification is itself reported.

## 4. Reviewer procedure
Confirm the support balance agrees to the source system or document, not to a number the preparer typed. Confirm the ledger balance agrees to the trial balance at the same date. Re-perform at least one line or a sample (high tier: a sample of items plus a subsequent-clearing test against the next period's activity). Check manual journals to the account in the period are supported and approved. Look for round-number items, items re-explained differently month to month, rolling items, suspense used as permanent parking, and reconciliations signed in a batch at the end of the close. Record review notes and clear them before signing.

## 5. Status report to the close owner
Counts and values by tier: certified on time, certified late, overdue, certified with open items over policy, not started. List each exception with owner and age. Provide a certificate pack for the auditor: register, signed certificates, exceptions log and the policy.

## 6. Escalation
A high-tier account uncertified at the deadline goes to the controller the same day. A difference above tolerance that is not explained by the deadline is escalated with a proposed treatment (adjust, accrue, write off) and approver, never plugged to reach zero. Repeat late certifiers, repeated unexplained differences and accounts that need a manual journal every month trigger a process fix, not another reminder.

## Output
Register with status; certificates for completed accounts (account, date, ledger balance, support balance, difference composition, preparer and reviewer with dates, evidence location, open items); exceptions log; escalation list; a one-page status for the close owner.

## Do not
- Certify against a report derived from the same ledger.
- Let the preparer clear their own review notes or sign as reviewer.
- Mark an account certified with aged items and no action, or with an unexplained difference.
- Post a manual journal to force a reconciliation to zero.
- Treat a tool-generated match rate as certification; certification is a human sign-off on evidence.
