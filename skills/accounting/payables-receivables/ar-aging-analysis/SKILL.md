---
name: ar-aging-analysis
description: >-
  Build and interpret AR and AP aging: buckets, DSO and DPO, concentration, credit and unapplied-cash netting, collection risk and allowance, tie-out to the ledger. Use for "aging report", "who owes us", "what do we owe", "DSO", "overdue analysis", "AR concentration", "allowance for doubtful accounts", or "aging does not match the balance sheet".
metadata:
  department: "accounting"
  domain: "ap-ar"
  owner: "satva-coe"
  status: "beta"
  license: "Satva-original"
  source: "original"
---

# AR and AP aging analysis

An aging report is a read-only analysis. It tells you where cash is trapped (AR) or where obligations are building (AP), and it supports the allowance estimate. It does not send or pay anything; actions follow `ar-collections-dunning` or `ap-invoice-processing`.

## 1. Produce the report correctly

1. State the as-at date and the basis: aging by **due date** (days past due) is the standard for collection and payment urgency; aging by **invoice date** is used for allowance policies and some covenants. Say which.
2. Buckets: current (not yet due), 1 to 30, 31 to 60, 61 to 90, over 90 days past due. Adapt to the client's terms.
3. Include credit notes, unapplied payments and prepayments. Show them separately by party, then net.
4. Currency: age in the transaction currency; present a translated total at the as-at rate and say so.
5. Missing or unreadable due dates are listed as exceptions with the document number, never guessed into a bucket.
6. Exclude disputed or on-hold items from the "collectable" view but show them in a separate column.

## 2. Tie out first

The aging total at the as-at date must equal the ledger control account (`subledger-to-gl-reconciliation`). Typical breaks: manual journals to the control account, backdated documents entered after the report was run, unapplied cash not included in the report, foreign-currency revaluation, deleted or voided documents. Resolve before analysing; otherwise the analysis is of the wrong population.

## 3. Metrics

```
DSO  = (AR balance / credit sales in period) x days in period
       (use the period matching the balance; for seasonal business use countback method)
DPO  = (AP balance / purchases or COGS in period) x days in period
Past-due ratio = past-due balance / total balance
Average days to pay (weighted) = sum(days to pay x payment amount) / sum(payment amount)
Collection effectiveness = (opening AR + credit sales - closing total AR) / (opening AR + credit sales - closing current AR)
```

Compare to terms: if terms are 30 days and DSO is 55, the gap is lateness (or mix of terms), not just distribution. Trend over at least six months; one month's DSO is noisy.

## 4. Analyse

- **Concentration**: top 5 and top 10 customers as a share of AR and of revenue. A single customer above about 20 percent of AR is a risk to flag.
- **Risk movers**: customers who moved to an older bucket since last month; customers with several consecutive late payments; balances over 90 days.
- **Dispute and credit exposure**: value of disputes, unapplied cash, credits awaiting issue.
- **Credit limit breaches**: balance above limit, or limit with overdue items.
- **AP**: what is due in the next 7, 14, 30 days against forecast cash; early-payment discount opportunities; vendors who may stop supply for non-payment; stretching payables (DPO rising) that suggests a cash squeeze.
- **Net positions**: a party that is both customer and vendor; offset only where there is a legal right and agreement.

## 5. Allowance for doubtful accounts

Aging-matrix method: apply the client's historical loss rate to each bucket, then adjust for specific known cases.

```
Bucket          Balance   Rate    Allowance
Current         80,000    0.5%       400
1-30            20,000    2%         400
31-60           10,000    5%         500
61-90            4,000   15%         600
90+              6,000   40%       2,400
Specific (named account fully doubtful)       3,000
Required allowance                              7,300
Existing allowance                              5,000
Adjustment: Dr Bad debt expense 2,300  Cr Allowance 2,300
```

Rates come from the client's own history, not a generic table; document the basis. Entries are drafted and approved (`journal-entry-controls`). Frameworks (expected credit loss under IFRS 9 or CECL under US GAAP) require more; use this as the practical estimate and flag when the client reports under those standards.

## 6. Presentation

Answer in three parts: the picture (totals per bucket, party, as-at date, currency), what the data means (largest risks and trend), and recommended next actions with owners. Mark any figure that could not be verified, and say plainly when a tool or source failed instead of estimating.

## Output

Aging table by party and bucket, tie-out to the ledger, metrics with trend, top risks, proposed allowance entry (draft), and action list.

## Do not

- Net a customer credit against what they owe without saying so.
- Rank a customer as "most overdue" before checking for credits and unapplied cash.
- Present a DSO without stating the formula and period.
- Use a generic loss-rate table as if it were the client's history.
- Imply that anything was sent, paid or posted.
