---
name: construction-job-costing
description: >-
  Construction and contractor accounting: job cost structure, percentage-of-completion revenue, WIP schedule (over/under billing), retainage, change orders, progress billing (AIA G702/G703 style), subcontractor compliance and job profitability review. Use when a contractor, builder or trades business needs job costing set up or its books fixed, or when someone says "WIP schedule", "over/under billing", "retainage", "change order", "cost-to-complete", "percent complete" or "job profitability".
metadata:
  department: "accounting"
  domain: "industries"
  owner: "satva-coe"
  status: "beta"
  license: "Satva-original"
  source: "original"
---

# Construction job costing and WIP

The contractor's financials are only as good as the cost-to-complete estimate. Revenue is recognised over time (ASC 606 input method, cost-to-cost, or IFRS 15 equivalent), so a stale estimate misstates profit in every period until the job closes.

## Step 1: Job cost structure

1. One job (project) record per contract, with contract amount, start/end, billing terms, retainage %, and a budget by cost code.
2. Cost codes: use a stable scheme (CSI MasterFormat divisions or an internal list) with cost *types*: labor, material, subcontract, equipment, other. Every cost line carries job + code + type.
3. Direct costs go to the job; shared overhead stays in G&A or a separate indirect-cost pool allocated by an approved rate. Do not bury overhead in jobs to flatter margin.
4. Payroll burden (taxes, insurance, benefits, workers' comp) is loaded into labor cost by a rate you can defend.
5. Subcontractor bills are coded to job and cost code, with retainage payable tracked separately.

## Step 2: Revenue recognition (cost-to-cost)

Per job, each period:
1. Percent complete = cost incurred to date / total estimated cost at completion (exclude uninstalled stored materials from the numerator unless the policy treats them as satisfied).
2. Revenue earned to date = percent complete x current contract value (original plus approved change orders).
3. Period revenue = earned to date less revenue previously recognised.
4. Gross profit to date = earned revenue less cost incurred. Gross margin = GP / earned revenue.
5. Estimated loss on a job: recognise the full expected loss immediately (provision for loss contract) regardless of percent complete.

Worked example: contract 1,000,000; estimated cost 800,000; cost to date 400,000 -> 50% complete; earned revenue 500,000; billed to date 560,000 -> overbilled 60,000 (contract liability). If estimated cost rises to 900,000, percent complete = 44.4%, earned = 444,444, and GP drops from 100,000 to 44,444 at completion; the catch-up hits this period.

## Step 3: WIP schedule (the central control)

Columns per job: contract value, approved change orders, revised contract, estimated total cost, cost to date, estimated cost to complete, percent complete, earned revenue, billed to date, over/(under) billing, gross profit to date, projected GP, projected margin %, backlog.

- Overbilling (billed > earned) is a contract liability; underbilling is a contract asset (costs and estimated earnings in excess of billings). Present them gross by job where the balance sheet requires, not netted across jobs.
- Backlog = revised contract less earned revenue.
- Bonding and bank covenants read this schedule; accuracy is a lending matter, not only an accounting one.
- Reconcile: WIP total cost to the job-cost subledger; billings to AR + retainage receivable; earned revenue to the GL revenue account.

## Step 4: Billing, retainage and change orders

1. Progress billing from the schedule of values: percent complete per line x line value less prior billings; retain the contract retainage %.
2. Retainage receivable (customer) and retainage payable (subcontractor) are separate accounts, released on the contract milestone or lien-waiver conditions.
3. Change orders: unapproved changes are *claims*; include them in contract value only when enforceable rights exist and approval is probable. Track a change-order log (number, scope, amount, approval date, effect on cost estimate).
4. Collect conditional/unconditional lien waivers with each payment where the jurisdiction uses them.

## Step 5: Monthly review

1. Project managers re-estimate cost to complete for every open job; accountants challenge any job where cost incurred rose and ETC did not.
2. Flag jobs with: margin fade vs prior month greater than a set threshold, ETC below remaining committed subcontracts, cost incurred above revised budget, billing materially behind or ahead of earned revenue.
3. Compare original bid margin, current projected margin, and actual to date; feed the lessons back to estimating.
4. Close the job: final costs, retainage release, warranty reserve, final lien waivers, then zero the job and move it from open WIP.

## Failure modes

- Cost-to-complete never updated, so profit "appears" at the end of the job.
- Unapproved change-order revenue booked while the cost is real.
- Overbillings netted against underbillings on another job.
- Costs coded to the wrong job to dodge a loss job.
- Subcontractor insurance, license and 1099 data missing at payment time.
- Using billings as revenue (cash-basis habit) in a company that needs accrual statements for bonding.

## Output

A WIP schedule with the reconciliations above, a change-order log, a job-margin fade report, and a short exceptions memo for jobs outside tolerance.
