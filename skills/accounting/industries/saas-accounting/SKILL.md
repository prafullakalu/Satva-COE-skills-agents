---
name: saas-accounting
description: >-
  Accounting for SaaS and subscription businesses: ASC 606 / IFRS 15 recognition for subscriptions, usage and implementation fees, deferred revenue and unbilled roll-forwards, capitalised commissions (ASC 340-40), capitalised software costs, multi-element contracts, credits and refunds, and reconciling billing system, payments and GL. Use when books for a subscription business need correct revenue and deferred revenue, or someone says "deferred revenue roll-forward", "capitalised commissions", "usage billing revenue", "annual prepay", "billing system to GL" or "SaaS month-end". Metrics (ARR, churn, NRR) are in saas-metrics-coach.
metadata:
  department: "accounting"
  domain: "industries"
  owner: "satva-coe"
  status: "beta"
  license: "Satva-original"
  source: "original"
---

# SaaS accounting

Billing is not revenue and cash is not billing. Three clocks run at once: when the customer is invoiced, when cash arrives, and when the service is delivered. The ledger needs a revenue schedule that follows delivery and balances for the other two.

## Step 1: Identify performance obligations per contract

1. Subscription access (hosted software, stand-ready): one obligation, recognised ratably over the term from the service start date.
2. Implementation or onboarding: separate obligation only if distinct (the customer can benefit from it on its own or with readily available resources); otherwise combine with the subscription and recognise ratably over the expected customer relationship/term.
3. Usage-based fees: recognise as usage occurs (variable consideration allocated to the period it relates to), subject to minimum commitments recognised ratably.
4. Professional services and training: as delivered (hours or milestones).
5. On-premise licence with hosting, support or upgrade rights: apply licence guidance; allocate the transaction price by relative standalone selling price.
6. Free trials and discounts: recognise nothing for free periods; spread multi-year discounts and ramps over the term when the obligation is delivered evenly.

Record the conclusion per product family in a policy memo and reference it in the revenue schedule.

## Step 2: The revenue schedule (the control)

Per contract line: start date, end date, term, total contract value, billing schedule, recognition method, monthly revenue. Daily or monthly proration for partial periods must follow one policy (calendar-day proration is typical). Use a spreadsheet or revenue sub-ledger, not manual entries. Monthly output:

**Deferred revenue roll-forward** = opening + billings in the period - revenue recognised +/- credits and refunds +/- FX = closing. The closing balance must equal the GL deferred revenue balance and the sum of contract-level remaining unrecognised billed amounts.

**Unbilled receivable (contract asset)** = revenue recognised in excess of billing (for example, annual-in-arrears or ramp contracts). Track separately and age it.

**Remaining performance obligations (RPO)** = contracted but unrecognised revenue; disclose current vs non-current.

## Step 3: Costs to obtain and fulfil

- **Sales commissions (ASC 340-40):** incremental costs of obtaining a contract are capitalised and amortised over the period the benefit is expected (often customer life, longer than the initial term when renewal commissions are not commensurate). Practical expedient: expense if amortisation would be one year or less. Capitalise the commission, accrued bonus and employer taxes tied to the contract; amortise monthly; test for impairment.
- **Capitalised software (ASC 350-40 internal-use / 985-20):** capitalise application-development-stage costs after technological feasibility or preliminary stage ends; expense planning and maintenance. Document stage gates and time tracking by project.
- **Hosting and cloud implementation costs:** capitalise implementation costs of a cloud computing arrangement as a prepaid over the term.
- **Cost of revenue:** hosting, support, customer success, payment processing, amortised commissions per policy.

## Step 4: Billing-to-GL reconciliation

1. Billing system invoices (including credit notes) = GL AR + deferred revenue + revenue + tax payable movements for the period.
2. Payments processor settlements = bank deposits + fees + chargebacks + reserves.
3. Sales tax or VAT: calculated by the tax engine, reconciled to the liability account.
4. Reconcile subscriptions: active count and MRR in billing vs contract register; investigate mismatches (cancelled but still billed, billed but not provisioned).

## Step 5: Month-end checklist

New and amended contracts reviewed and entered; revenue schedule run; deferred and unbilled rolled forward and tied out; commissions capitalised and amortised; refunds and credits cut off; bad-debt allowance reviewed; hosting and vendor accruals; stock-based compensation posted; MRR/ARR bridge produced from the same data (see `saas-metrics-coach`).

## Failure modes

- Booking annual invoices to revenue when billed.
- Implementation fee recognised up front without a distinct-obligation analysis.
- Commission capitalised but never amortised, or amortised over the wrong life.
- Credits and refunds applied to the wrong period.
- Deferred revenue not tied to contracts (so audit sampling fails).
- Billing system and CRM disagree on ARR.

## Output

Revenue schedule, deferred/unbilled roll-forwards, commission capitalisation schedule, billing-to-GL reconciliation, and a short accounting-policy memo per revenue stream.
