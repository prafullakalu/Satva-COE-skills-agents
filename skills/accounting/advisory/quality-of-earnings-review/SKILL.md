---
name: quality-of-earnings-review
description: >-
  Quality of earnings (QoE) and financial due diligence analysis for a transaction: adjusted EBITDA bridge, revenue and cost normalisation, net working capital peg, net debt and debt-like items, proof of cash, customer and revenue quality, and red flags. Use for buy-side or sell-side diligence on an SMB or mid-market company, or when someone says "quality of earnings", "adjusted EBITDA", "EBITDA add-backs", "working capital peg", "net debt and debt-like items", "proof of cash" or "financial due diligence report". Complements due-diligence-checklist.
metadata:
  department: "accounting"
  domain: "advisory"
  owner: "satva-coe"
  status: "beta"
  license: "Satva-original"
  source: "original"
---

# Quality of earnings review

Valuation is a multiple of earnings, so every dollar of EBITDA is worth the multiple. A QoE tests whether reported earnings are real, recurring and convertible to cash. Output is a defensible adjusted EBITDA, a working-capital target and a list of debt-like items. Use `due-diligence-checklist` for the full request list and `dcf-model` / `comparable-company-analysis` for valuation.

## Step 1: Scope and data request

Agree the period (typically three fiscal years plus trailing twelve months), the entity perimeter, the accounting basis, the materiality threshold, and the deliverable. Request: monthly trial balances and financials, general ledger detail for the TTM, revenue by customer/product/month, AR and AP agings, bank statements, payroll registers, tax returns, debt and lease agreements, top contracts, inventory records, management adjustments schedule, and budget vs actual. Log requests and responses.

## Step 2: Proof of cash

Reconcile book receipts and disbursements to bank statements for the period (at least the last 12 months by month). Unexplained gaps indicate unrecorded revenue, owner transactions, or timing games. This is the highest-value test in small companies with weak controls.

## Step 3: Revenue quality

1. Recognise per policy; test cut-off for the month before and after year end and each quarter-end.
2. Customer concentration: top 1, 5, 10 share; contract terms and renewal dates; churn by cohort.
3. Recurring vs non-recurring; price vs volume vs mix; one-time projects; large year-end billings; credit notes after period end; bill-and-hold; related-party revenue.
4. Reconcile revenue per ledger to billing system, to AR movements and to cash receipts.
5. Gross margin by product and customer; unusual jumps are probes for capitalised costs or misclassification.

## Step 4: Adjusted EBITDA bridge

Start from reported net income and build to adjusted EBITDA:

| Step | Item |
|---|---|
| Reported net income | |
| + Interest, taxes, depreciation and amortisation | EBITDA |
| +/- Accounting corrections | Revenue cut-off, accrual completeness, capitalisation of expenses, inventory valuation |
| +/- Normalisation | Owner compensation to market, related-party rent or services to market, personal expenses, one-off legal or restructuring, non-recurring revenue or costs, out-of-period items |
| +/- Pro forma | Run-rate effect of price changes, new hires, closed locations, acquisitions made mid-period |
| = Adjusted EBITDA | |

Classify each adjustment as management-proposed or diligence-identified; show support (document, calculation, rationale), the period, the sign, and a confidence level. Reject add-backs that are really recurring (regular marketing spend labelled "one-off", recurring "consulting"). Buyers should haircut aggressive pro forma and synergy items; sellers should document them rigorously.

## Step 5: Net working capital

1. Compute monthly NWC = (AR + inventory + prepaid + other operating current assets) - (AP + accrued liabilities + deferred revenue + other operating current liabilities); exclude cash, debt, income taxes and debt-like items.
2. Normalise for unusual balances and seasonality; peg = average of the last 12 months (or season-adjusted level).
3. Closing NWC vs peg drives the purchase-price adjustment: define the accounting policies for the closing statement in the agreement to avoid disputes.

## Step 6: Net debt and debt-like items

Bank debt, notes, finance leases, accrued interest, deferred purchase price, customer deposits and deferred revenue in excess of cost to serve, unpaid taxes, accrued bonuses and unfunded pensions, unpaid owner payables, capex catch-up, litigation accruals, aged payables stretched beyond terms, transaction bonuses. Each reduces equity value on a cash-free debt-free basis.

## Step 7: Other tests

Capex: maintenance vs growth and underinvestment. Payroll: headcount by month vs P&L, owner and family on payroll, contractor misclassification exposure. Tax: nexus, sales-tax exposure, payroll tax arrears. Controls and systems: reliance on the owner, spreadsheet processes, audit status. Forecast: compare budget accuracy history; test the current-year trading against the plan.

## Red flags

Growth in AR faster than revenue; margins improving while reserves shrink; revenue spikes at period ends; cash conversion falling; large "other" accounts; frequent restatements; related-party flows; owner compensation far from market; EBITDA-to-cash conversion below 70 percent for a non-growing company; inconsistent definitions between monthly and annual accounts.

## Output

QoE report: executive summary, adjusted EBITDA bridge with support, proof of cash, revenue and customer analysis, NWC analysis and peg, net debt and debt-like items, tax and other findings, and a list of issues with their valuation effect.
