---
name: stripe-subscription-revenue-mapping
description: >-
  Map Stripe Billing data (customers, products, prices, subscriptions, invoices, credit notes, proration, trials, discounts, tax) to accounting entries: billings versus revenue, deferred revenue schedules, MRR for management reporting, and the invoice-to-ledger linkage. Use when asked to "sync Stripe invoices to the books", "deferred revenue for annual subscriptions", "recognise SaaS revenue from Stripe", "MRR vs revenue", "proration accounting", or "map Stripe products to GL accounts".
metadata:
  department: "accounting"
  domain: "revenue-recognition"
  platform: "stripe"
  owner: "satva-coe"
  status: "beta"
  license: "Satva-original"
  source: "original"
---

# Stripe: subscription revenue mapping

Grounded in Stripe Billing public documentation and ASC 606 / IFRS 15 principles. No Stripe MCP connector at Satva yet; work from invoice and subscription exports or read-only API access. Settlement and fees are in `stripe-payout-fee-reconciliation`; refunds and disputes in `stripe-refunds-disputes-accounting`. Revenue recognition policy is a judgement for the entity's accountant and auditor; this skill gives the mechanics.

## Core distinction

- **Billing** = a finalised Stripe **invoice** (what the customer owes). It creates a receivable and, for periods not yet served, a contract liability (deferred revenue).
- **Cash** = a charge/payment, which settles the invoice (clearing account).
- **Revenue** = the service delivered over time. For a monthly plan, billing and revenue coincide in the month; for an annual plan paid upfront, 1/12 is revenue each month.
- **MRR/ARR** = a management metric from active subscription prices, not an accounting figure; never post it.

Book from **invoices**, not from charges: invoice lines carry the period (`period.start`, `period.end`), product, price, tax and proration; charges do not.

## Data mapping

| Stripe object | Use | Accounting target |
|---|---|---|
| Customer | counterparty | Customer in the ledger (match on email plus stable id stored in metadata) |
| Product / Price | what was sold | Item with revenue account; map each product id to a revenue GL account and a recognition rule (point-in-time, ratable, usage) |
| Invoice (finalised, `status=paid` or `open`) | the billing | Sales invoice, same number (`invoice.number`), same date, currency and tax |
| Invoice line `period` | service period | Drives the deferral schedule |
| Credit note | reduction of an invoice | Credit note on the same ledger invoice; tax reversed |
| Discount/coupon | price reduction | Net the line (revenue is net of discount); do not post as an expense |
| Tax (Stripe Tax or manual) | collected tax | Tax liability, never revenue |
| Charge BT | cash | Clearing account via the payout process |

Keep a mapping table `product_id -> revenue account, deferral rule, tax code`, owned by the accountant. A product with no mapping blocks posting; do not default to "Sales".

## Workflow

1. **Extract** finalised invoices for the period (create date and finalised date; use the finalised date unless policy says otherwise). Exclude drafts and void invoices. Include credit notes issued in the period.
2. **Validate** each invoice: `amount_due + amount_paid` reconcile with line totals, tax and discounts; currency; customer mapped; every line product mapped.
3. **Post** one ledger invoice per Stripe invoice. Idempotency key: Stripe invoice id stored in the reference field; skip if already present.
4. **Defer** where line periods extend past the month: for each line, revenue per day = line net amount / days in the line period; recognise per month by days in service within the month. Post Dr Deferred revenue, Cr Revenue monthly (or compute once and book via a schedule). For monthly plans billed in advance of the same month, no deferral.
5. **Proration.** Mid-cycle changes create proration lines (credit for unused time, charge for the new plan) with their own periods. Treat them as ordinary lines with those periods: do not net them away. The credit line's negative amount reverses prior deferred revenue for the unused days.
6. **Trials.** No invoice, no revenue. A trial converted creates the first invoice; do not accrue during trial.
7. **Usage-based / metered.** Revenue accrues as usage occurs, billed in arrears: at month-end accrue unbilled usage (Dr Unbilled receivable/contract asset, Cr Revenue) and reverse when invoiced. Estimate from the usage records of the period; document the cut-off.
8. **Unpaid and failed invoices.** `open` or `uncollectible` invoices are receivables, not revenue reversals. Provision for bad debt per policy; write-off only with the owner's approval. Subscription `past_due` is an operational state; do not stop recognising revenue unless the policy (collectibility under ASC 606) says so.
9. **Cancellation and refunds.** A cancellation with a prorated credit note reduces deferred revenue for the unrecognised part. A refund without a credit note is a gap: raise one.
10. **Tie-outs** (monthly, all must hold):
    - Sum of ledger invoices = sum of finalised Stripe invoices (count and amount) per currency.
    - Deferred revenue ledger balance = schedule total of unrecognised amounts at period end.
    - Billings - recognised revenue - change in deferred revenue = 0 (excluding tax).
    - AR control = open Stripe invoices (`amount_remaining` summed).
    - Clearing account = unsettled balance (payout skill).

## Common failure modes

- Recognising revenue on charge date, which pulls annual plans into one month.
- Posting net payouts as revenue (fees and refunds vanish).
- Posting tax as income because the invoice total was mapped to one revenue line.
- Duplicate ledger invoices from running both webhook sync and a manual import.
- Using subscription start date instead of the invoice line period for proration lines.
- FX: invoice in EUR, payout in USD; keep the invoice at the invoice-date rate and book the settlement difference as realised FX.
- Multi-element products (setup fee plus plan): one `price` per distinct performance obligation, mapped separately.

## Do not

- Post MRR, ARR or "annualised" figures.
- Rewrite history in closed periods when plans change; post the adjustment in the current period.
- Choose a recognition policy on the entity's behalf; propose, cite the rule, and request approval.

## Output

A mapping table (product, GL, rule), a monthly schedule per subscription (period, billed, recognised, deferred balance), the tie-out checklist with pass/fail and residuals, and an exceptions list (unmapped products, invoices without customers, negative lines).
