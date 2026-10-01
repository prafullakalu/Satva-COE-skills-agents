---
name: stripe-payout-fee-reconciliation
description: >-
  Reconcile Stripe to the bank and the ledger: tie each payout to its itemised balance transactions, split gross sales, Stripe fees, refunds, disputes and adjustments, and book one clean journal per payout so the bank deposit matches. Use when asked to "reconcile Stripe payouts", "why doesn't the Stripe deposit match the bank", "book Stripe fees", "Stripe clearing account", "payout reconciliation report", or "gross vs net revenue from Stripe".
metadata:
  department: "accounting"
  domain: "reconciliation"
  platform: "stripe"
  owner: "satva-coe"
  status: "beta"
  license: "Satva-original"
  source: "original"
---

# Stripe: payout and fee reconciliation

Grounded in Stripe's public documentation (balance transactions, payout reconciliation report). Satva has no Stripe MCP connector yet; work from exports (Dashboard CSV or Reporting API) or the user's read-only restricted key. Never ask for a secret key in chat; a restricted key with read access to balance transactions, payouts and reports is enough.

## The model (get this right and everything else follows)

- Stripe holds a **balance**. Every money movement creates a **balance transaction** (BT) with `amount` (gross), `fee`, `net = amount - fee`, `currency`, `type` and `reporting_category`, `created`, `available_on`, `source`.
- A **payout** moves the available balance to the bank. With automatic payouts, each payout settles a batch of BTs, identified by `automatic_payout_id`. The bank sees ONE credit equal to the payout amount: the sum of net amounts of its BTs.
- Reconciliation is therefore: bank line = payout = sum(net of itemised BTs). Book gross revenue and fees separately, never the net deposit as revenue.
- Use `reporting_category` for accounting (charge, refund, dispute, dispute_reversal, fee, adjustment, transfer, payout, and so on). The raw `type` enum is wider and noisier.

## Source data

Preferred: the **Payout reconciliation** report (Dashboard > Reports, or Reporting API `payout_reconciliation.itemized.*` and `payout_reconciliation.summary.*`). Columns that matter: `automatic_payout_id`, `automatic_payout_effective_at`, `balance_transaction_id`, `reporting_category`, `gross`, `fee`, `net`, `currency`, `charge_id`, `payment_intent_id`, `invoice_id`, `customer_id`, plus custom metadata via `payment_metadata[key]`, which lets you carry your order or invoice number through. Amounts in reports are in major units; API objects use minor units (cents, or yen as whole units). Convert once and say which you used.

Caveats from the docs:
- The report is for **automatic payouts**. On manual payouts or instant payouts, Stripe cannot say which BTs a payout covered; reconcile the Balance report ("balance.summary") against the bank instead, and treat the Stripe balance like a bank account.
- Reports group a payout by its **estimated arrival date**, not the day the bank posted it. Match on amount and payout id first, date second (allow 1 to 3 business days).
- Report data lags the payout; a payout can land before its itemised data exists. Re-run later rather than guessing.
- Each currency settles separately; a payout is in one currency. Multi-currency accounts have one payout per currency.

## Workflow

1. **Scope.** Account, period, currencies, payout schedule (automatic, manual, instant).
2. **List payouts** in the period (`payout_reconciliation.summary` or `GET /v1/payouts`): id, amount, currency, arrival date, status. Failed payouts get their own section (failed payouts report): the money returns to the balance and is paid again in a later payout; do not book a deposit that never reached the bank.
3. **For each payout, pull the itemised BTs** and group by `reporting_category`: count, sum gross, sum fee, sum net.
4. **Foot it.** Sum of `net` across all BTs of the payout must equal the payout amount to the minor unit. If not: BTs missing (report lag), a different currency, or an instant payout. Stop and say which; do not force it.
5. **Match to the bank.** Find the bank credit with that amount around the arrival date. Statement descriptors differ by bank; `payout_reference_token` or the trace id (where supported) is printed on some statements and is a strong key.
6. **Match sales to the ledger.** Each charge BT should link to an invoice/order via `invoice_id`, `payment_intent_id`, or your metadata key. List charges with no counterpart (missing invoice) and invoices marked paid with no charge (paid outside Stripe, or timing).
7. **Build the journal per payout** (see below) and compare to what is already booked.
8. **Ending balance.** The Stripe balance at period end (ending balance reconciliation) is an asset: money earned but not yet paid out. It should equal the Stripe clearing account balance in the ledger. A difference is unbooked BTs or unmatched payouts.

## Journal pattern (accrual, one per payout)

Use a **Stripe clearing** (receivable) account so the bank is only touched by the payout.

Per charge or per daily batch (when the sale is recorded):
- Dr Stripe clearing (gross), Cr Accounts receivable or Sales (gross), plus tax per the invoice.

Per payout (when it settles):
- Dr Bank (payout amount = net total)
- Dr Payment processing fees (sum of `fee` on charges, plus any fee-category BTs)
- Dr Refunds / Sales returns (refund gross)
- Dr Chargebacks and dispute losses (dispute gross, dispute fees)
- Cr Stripe clearing (sum of gross of the charges in the batch, with adjustments)

Check: debits equal credits and Cr clearing equals the batch's gross movement. After the payout, clearing should hold only unsettled BTs.

Fees:
- Stripe fees are an expense, not a sales reduction, unless the entity's policy nets them. Be consistent and write the policy down.
- Where Stripe withholds VAT/GST on its fees (`withheld_tax`, included in `fee`), split it: `fee_net_of_withheld_tax` is the processing expense, `withheld_tax` is recoverable or reportable per local rules. Ask before treating it as input tax.
- FX: when a charge is converted, the BT carries `exchange_rate` and the converted `amount`. Book at the settled amounts; Stripe's FX fee is `stripe_fx_fee` (a fee). Differences between invoice currency and settlement currency are realised FX, not revenue.

## Failure modes

| Symptom | Cause | Fix |
|---|---|---|
| Payout total differs from bank | Instant payout, bank fee, FX at bank, or wrong day | Check payout currency vs bank account; look for a separate bank fee line |
| Net of BTs differs from payout | Report not yet complete, or rolling reserve adjustments | Re-pull; look at `adjustment` and `reserve` categories |
| Same charge booked twice | Both webhook and report import ran | Dedupe on `balance_transaction_id` |
| Revenue overstated | Booked net deposits as sales | Rebuild from gross + fee split |
| Clearing account never zero | Unbooked refunds/disputes or BTs from the following period | List open BTs by category |

## Do not

- Book the bank deposit as revenue.
- Hand-edit totals to force a match; carry an explicit reconciling item with a reason instead.
- Mix test-mode and live-mode data.
- Store keys, customer emails or card details in outputs; use ids.

## Output

Per payout: id, arrival date, bank amount, matched bank line, table by reporting category (count, gross, fee, net), the footing check (pass or residual), and the journal. Then a period summary: total gross, fees (and effective rate = fees / gross), refunds, disputes, net, ending Stripe balance versus clearing account, and the open exceptions list.
