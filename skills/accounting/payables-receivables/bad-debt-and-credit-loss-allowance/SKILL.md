---
name: bad-debt-and-credit-loss-allowance
description: >-
  Estimate, record and review the allowance for doubtful accounts and bad-debt write-offs: aging-matrix and specific-provision methods, expected credit loss (IFRS 9 simplified approach and CECL) basics, write-off approval and evidence, recoveries, tax and VAT or GST bad-debt relief checks, and period-end disclosure support. Use for "bad debt provision", "allowance for doubtful accounts", "write off this customer", "expected credit loss", "provision matrix", "recovered a written-off debt", "should we provide for this receivable". Works from the aging produced by ar-aging-analysis.
metadata:
  department: "accounting"
  domain: "payables-receivables"
  owner: "satva-coe"
  status: "beta"
  license: "Satva-original"
  source: "original"
---

# Bad debt and credit-loss allowance

The allowance recognises that part of receivables will not be collected, before the loss is certain. The estimate is a judgement made from the client's own history, supported by evidence, approved by someone other than the collector, and re-performed every period.

## 1. Inputs
Aging at the period end by due date, tied to the ledger control account (`subledger-to-gl-reconciliation`); cash applied up to cut-off (`ar-cash-application`); the disputes log, promise-to-pay log and credit holds (`ar-collections-dunning`, `customer-credit-control`); at least 24 to 36 months of history of invoices raised and amounts finally lost, by bucket and segment; subsequent receipts after the period end; the existing allowance and last period's workings.

## 2. Aging-matrix method (the practical default)
1. Take bucket totals from the aging (current, 1 to 30, 31 to 60, 61 to 90, over 90 days past due), excluding amounts that will be handled specifically.
2. Derive each bucket's loss rate from history: of balances that were in this bucket at past period ends, the share eventually written off. Use segments (customer type, country, product) if the rates differ materially.
3. Adjust for forward-looking information that moves risk: the customer base's industry conditions, a change in terms, a large concentration, interest-rate and macro signals. Document the size and reason of each adjustment; a change without a reason is plugging.
4. Allowance = sum of bucket balance times rate, plus specific provisions.

```
Bucket          Balance   Rate    Allowance
Current          80,000   0.5%         400
1-30             20,000   2%           400
31-60            10,000   5%           500
61-90             4,000   15%          600
Over 90           6,000   40%        2,400
Specific (named account, fully doubtful)  3,000
Required allowance                        7,300
Existing allowance                        5,000
Adjustment: Dr Bad debt expense 2,300  Cr Allowance 2,300
```

Compute the multiplication in a spreadsheet or script, not by estimate, and keep the workings with the journal. The figures above are illustrative; rates come from the client's data.

## 3. Specific provisions
Provide specifically against named accounts when there is evidence of credit impairment: insolvency or administration, a disputed amount the customer will not pay, a customer who has stopped responding, a failed payment plan, collection agency or legal outcome. Exclude those balances from the matrix to avoid double counting. Provide the unrecoverable portion, not necessarily all, after expected security, insurance and set-off, and record the evidence for the percentage.

## 4. Frameworks
- **IFRS 9 simplified approach** for trade receivables: lifetime expected credit loss from day one, normally through a provision matrix like section 2 with forward-looking adjustments. Credit-impaired balances are assessed individually.
- **CECL (US GAAP)**: lifetime expected loss on pool-level or individual basis with reasonable and supportable forecasts. A matrix by aging is an accepted starting method when supported.
- Private-company and small-entity frameworks may permit incurred-loss or specific methods. Confirm which framework the client reports under and flag when this practical estimate needs the fuller standard.

## 5. Write-off
A write-off removes a specific uncollectable balance. Conditions: collection efforts are exhausted and documented (contacts, letters, agency or legal result), the debtor is insolvent or the cost of pursuit exceeds the recovery, the balance has been reviewed for credits and unapplied cash, and the approver is not the collector (thresholds by amount; higher amounts go to the controller or the board). Entry: Dr Allowance, Cr Accounts receivable (customer). Do not write off directly to expense if an allowance exists, except where policy provides.
VAT or GST on the written-off invoice: relief is often available only after conditions (time since due, evidence, formal notice, debt written off in the books) and the claim must be reversed if the debt is later paid. Income-tax deductibility has its own rules. Confirm both for the jurisdiction before relying on them.

## 6. Recoveries
When cash arrives for a written-off debt: reinstate the receivable and the allowance (Dr Accounts receivable, Cr Allowance), then record the receipt against the receivable (Dr Bank, Cr Accounts receivable). Reverse any tax relief claimed. Record in the customer file; the customer may need to return to credit control.

## 7. Period-end review
Re-perform the matrix on the final aging; compare to last period and explain movements; test subsequent receipts after the cut-off date to support specific and matrix conclusions; reassess the history table annually; check that disputed and promised balances are classed correctly; ensure concentration risk is visible; draft the journal for approval (`journal-entry-controls`) and keep the evidence. Disclosures often need an allowance movement table (opening, charge, utilised, released, closing) and the method and key judgements.

## Output
Allowance workings (buckets, rates and their basis, adjustments, specific provisions), proposed journal, write-off and recovery proposals with evidence and approver, movement table for disclosure, and open judgements for the reviewer.

## Do not
- Use a generic loss-rate table as if it were the client's history.
- Release the allowance to reach a profit target, or build a cushion in good years.
- Write off without approval or evidence of collection effort.
- Count a disputed or already-provided balance twice.
- Claim VAT or tax relief without checking the conditions.
