---
name: healthcare-practice-accounting
description: >-
  Accounting for medical, dental and allied-health practices: charges to collections flow, contractual adjustments, net patient revenue, AR by payer, deposits and clearinghouse reconciliation, patient credits and refunds, provider compensation, supplies and equipment, and practice KPIs. Use when keeping books for a clinic or private practice, or when someone says "net collection rate", "contractual adjustment", "payer AR", "ERA/EOB posting", "days in AR", "provider compensation" or "practice management system to GL". No protected patient data should be pasted into the conversation.
metadata:
  department: "accounting"
  domain: "industries"
  owner: "satva-coe"
  status: "beta"
  license: "Satva-original"
  source: "original"
---

# Healthcare practice accounting

A practice has two ledgers that disagree by design: the practice management system (PMS) holds *gross charges* by patient and payer; the general ledger should hold *net revenue* and cash. The accountant's job is to bridge them every month and to keep patient identifiers out of the GL entirely.

Privacy rule: work from summary reports (daily deposit, charge and adjustment totals, AR aging by payer class). Never request or store patient names, record numbers or diagnoses in accounting files. If a vendor requires patient-level data, it falls under a HIPAA business-associate agreement with the practice, not an ad hoc upload.

## Step 1: Revenue model

1. Gross charges are the fee schedule price. They are *not* revenue.
2. Net patient service revenue = gross charges less contractual adjustments (payer-allowed difference), implicit price concessions (expected bad debt, charity, discounts) and refunds. Under ASC 606 the transaction price is the amount expected to be collected.
3. Post to the GL at net: record contractual adjustments as a contra-revenue, not an expense. Keep gross charge detail only in the PMS and a memo schedule.
4. Capitated or value-based arrangements: recognise the per-member payment in the month covered; reconcile settlements and withholds separately.
5. Cash-pay and membership models: unearned membership fees are deferred and recognised over the service period.

## Step 2: The daily-to-monthly bridge

For each period:
1. PMS charges, adjustments, payments and refunds report -> summarised journal (revenue by service line or provider, contra-revenue by payer class, AR change).
2. Bank deposits vs PMS payments: reconcile card processor, EFT/ERA remits and patient copays separately. Differences are timing (deposit lag, batch holds) or unposted remits.
3. Patient AR (PMS aging) must equal GL accounts receivable (split insurance AR and patient AR). Reconcile to the cent; unreconciled items older than 60 days are escalated.
4. Credit balances (overpayments) are liabilities (refunds due), not negative AR; report them gross and track state unclaimed-property deadlines.
5. Reserve for uncollectible: an allowance by payer class and aging bucket (for example 0-30 low, 120+ heavy) tested against actual write-offs.

## Step 3: Cost side

- Provider compensation: base, productivity (wRVU or collections-based), bonuses and benefits. Accrue earned-but-unpaid productivity monthly; the formula must be written in the employment agreement and the calculation reproducible.
- Clinical supplies and drugs: inventory counted at least year-end; expense on consumption; medical supply spend by procedure for margin analysis.
- Malpractice, credentialing, licences, EHR and clearinghouse fees, equipment leases.
- Capital equipment (imaging, chairs, lasers): capitalise above threshold; depreciate; review lease vs buy under ASC 842.
- Owner-physician practices: separate owner draws, personal expenses and distributions; reasonable compensation matters for S-corp tax.

## Step 4: KPIs (calculate monthly, trend 13 months)

| KPI | Formula | Watch for |
|---|---|---|
| Gross collection rate | Payments / gross charges | Falls with fee-schedule creep |
| Net collection rate | Payments / (charges - contractual adjustments) | Target typically above 95 percent |
| Days in AR | Ending AR / (net revenue / days in period) | Rising means posting or denial problems |
| AR over 90 days % | AR >90 / total AR | Payer concentration |
| Denial rate | Denied claims / claims submitted | From PMS, not GL |
| Revenue per provider / per visit | Net revenue / provider FTE or visits | Productivity drift |
| Overhead ratio | Non-provider operating costs / net revenue | Benchmarks vary by specialty |

## Failure modes

- Booking gross charges as revenue, then "writing off" half as expense.
- Deposits posted as revenue without matching the remit, so patient balances never clear.
- Patient credit balances netted against AR.
- Mixing owner personal expenses into practice expenses.
- Uploading patient-level exports into spreadsheets or chat tools.

## Output

Monthly bridge workpaper (PMS to GL), payer-class AR aging with allowance, KPI dashboard, provider-compensation accrual schedule, and exceptions list.
