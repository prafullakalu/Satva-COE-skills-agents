---
name: stripe-refunds-disputes-accounting
description: >-
  Accounting treatment for Stripe refunds, partial refunds, chargebacks and dispute fees: what balance transactions appear, how to book each stage, how disputes affect the clearing account and revenue, tax and credit-note consequences, and the reserve for open disputes. Use when asked to "book a Stripe refund", "how do we account for a chargeback", "dispute fee accounting", "refund after payout", "Stripe dispute lost or won entries", or "why did the Stripe balance go negative".
metadata:
  department: "accounting"
  domain: "revenue-adjustments"
  platform: "stripe"
  owner: "satva-coe"
  status: "beta"
  license: "Satva-original"
  source: "original"
---

# Stripe: refunds and disputes accounting

Grounded in Stripe's public dispute and balance-transaction documentation. No Stripe MCP connector exists at Satva yet; work from the user's reports or read-only exports. Prerequisite concepts are in `stripe-payout-fee-reconciliation`.

## Refunds

What Stripe does: a refund creates a balance transaction (reporting_category `refund`) with a negative gross, deducted from the balance and therefore netted in the next payout. For a **partial** refund the BT is for that amount only. Stripe usually does not return its processing fee on the original charge; the refund BT typically has no fee credit. Check your plan: the fee is a real cost of the refunded sale.

Booking (accrual):
1. The original sale stands. Do not delete or edit the original invoice.
2. Issue a **credit note** (or sales return) for the refunded amount in the accounting system, linked to the invoice, with tax reversed in proportion. Refunds without a credit note leave output tax overstated.
3. Dr Sales returns (or revenue) and Dr Output tax payable (refunded tax), Cr Stripe clearing (refund gross).
4. Show the credit note as applied to the invoice so AR stays correct: invoice balance = original - credit note = amount actually kept.
5. Fees paid on the original charge remain an expense (no reversal) unless the BT shows a fee refund.

Edge cases:
- Refund after payout: Stripe takes it from the future balance; if the balance is insufficient the balance goes negative and Stripe debits the bank. The clearing account shows a credit balance until recovered; this is a payable to Stripe, not an error.
- Failed refunds (`refund_failure`, `payment_failure_refund`): the money returns to the balance; reverse the refund entry and flag the customer.
- Refund of a multi-currency charge: the refund is in the charge currency, but the BT is in the settlement currency at a new rate; the difference is realised FX.
- Proactive refund versus dispute: refunding during an open dispute is not allowed outside the dispute process; do not book a refund the dashboard shows as blocked.

## Disputes (chargebacks)

Lifecycle (Stripe): enquiry/inquiry (optional, no funds move on most networks), then dispute opened (`needs_response`), evidence submitted (`under_review`), then `won` or `lost`. Cardholders usually have about 120 days; you typically have 7 to 21 days to respond; the issuer takes up to roughly 60 to 75 days to decide.

Money movements (balance transactions, reporting category `dispute`, and `dispute_reversal` on a win):
1. **Dispute opened**: the disputed amount is debited immediately from the balance, plus a **dispute fee** (a separate charge, normally non-refundable). Funds are held for the whole case.
2. **Won**: the disputed amount is credited back (`dispute_reversal`). Stripe returns the dispute countered fee if you submitted evidence and won; the dispute received fee is normally not returned (jurisdiction exceptions exist, check contract).
3. **Lost**: nothing further moves; the original debit stands.

Booking:
- At opening: Dr Disputed receivables / chargeback holding (asset, disputed amount), Dr Dispute fees expense, Cr Stripe clearing. Revenue is untouched while the outcome is open. If your policy is prudence-first, reserve instead: Dr Chargeback losses, Cr Allowance for chargebacks. Pick one and apply consistently.
- Won: Dr Stripe clearing, Cr Disputed receivables (or release the allowance). Revenue stays.
- Lost: Dr Chargeback losses or Sales returns (policy: loss on fraud, revenue reversal if goods/services were not delivered), Cr Disputed receivables. Reverse output tax only where a credit note would be valid; a fraud chargeback usually still leaves the tax charged unless the jurisdiction allows bad-debt relief.
- The fee is expense in every outcome, except a returned countered fee, which is credited on the win.

Disputed amount can differ from the charge: FX movement, partial dispute, one dispute for several recurring charges, or a dispute on a partially refunded payment. Book what the BT shows, and tie it to the charge with `charge_id`; do not assume equality.

Evidence deadlines: put the due date on the dispute record and alert the owner early. A missed deadline is an automatic loss.

## Month-end reserve and checks

1. List all disputes still `needs_response` or `under_review` at period end: amount, charge date, due date, probability of loss (history of win rates by reason; use a flat rate if no data). Exposure = open disputed amounts + fees already paid is a sunk cost.
2. Allowance for chargebacks (if used) is trued up to the expected loss on open disputes; record the change in the P&L.
3. Dispute rate (disputes / charges over the period) should be tracked monthly; networks penalise high rates, and a rising rate is an operational finding to report beyond accounting.
4. Clearing account must reflect all open dispute debits; if the Stripe balance went negative, say why (dispute plus refunds exceeding pending balance).
5. Reconcile to the payout reconciliation report: categories `dispute` and `dispute_reversal` must tie to the entries above.

## Do not

- Delete the original sale or invoice when a refund or dispute happens.
- Book a dispute loss on opening when your policy is to wait for the outcome, or the reverse; document the policy.
- Treat the dispute fee as a reduction of sales.
- Re-submit evidence or accept disputes on the user's behalf without explicit instruction; those are irreversible actions with business consequences.

## Output

For each refund or dispute: charge id, dates, amounts (gross, fee), status, proposed journal (accounts, debit, credit), tax effect, and the one open action (credit note to issue, evidence due date). A summary table for the period by reporting category with the reserve calculation.
