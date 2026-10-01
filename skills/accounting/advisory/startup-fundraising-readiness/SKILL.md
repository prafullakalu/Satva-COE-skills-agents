---
name: startup-fundraising-readiness
description: >-
  Getting a startup finance function ready for fundraising or a lender: clean books, investor metrics, financial model, data room, cap table hygiene, use of funds and runway, and what investors test in financial diligence. Use when a founder says "we are raising", "investor due diligence", "build a data room", "financial model for investors", "Series A readiness", "how much should we raise" or "runway planning", or when preparing sell-side financials for a venture, angel or venture-debt process.
metadata:
  department: "accounting"
  domain: "advisory"
  owner: "satva-coe"
  status: "beta"
  license: "Satva-original"
  source: "original"
---

# Startup fundraising readiness

Investors price risk; sloppy finance is read as operating risk. Diligence kills deals less by finding bad numbers than by finding numbers nobody can explain. Start six months before the raise.

## Step 1: Readiness assessment (score each, red/amber/green)

| Area | Green looks like |
|---|---|
| Books | Accrual basis, closed within 15 days, bank-reconciled, revenue recognised correctly |
| Revenue | Contract-backed, recognised per policy, deferred revenue tied out |
| Metrics | ARR/MRR, churn, NRR, CAC, payback derived from the ledger and billing data and reproducible |
| Cap table | Fully diluted, every grant, SAFE, convertible and warrant recorded with executed documents |
| Tax and payroll | Filed, no arrears; contractors vs employees classified; 83(b) elections where relevant |
| Legal and IP | IP assignments, founder vesting, no unresolved claims |
| Model | Integrated three-statement model with driver assumptions that tie to history |
| Data room | Organised, indexed, current |

Anything red goes on a remediation plan with owner and date before the first investor meeting.

## Step 2: Financial model

1. Structure: assumptions sheet, monthly (first 24 months) then quarterly or annual (to 5 years), revenue build, headcount plan, opex, working capital, capex, financing, three statements that balance, scenarios.
2. Revenue build: bottoms-up from drivers (leads, conversion, price, churn, expansion) not "1 percent of a big market". Back-test the drivers against the last 12 months.
3. Unit economics: CAC by channel, gross margin, LTV, payback, contribution margin; see `saas-metrics-coach` and `unit-economics-analysis`.
4. Cash: monthly burn, runway under base and downside, and the month the company hits zero without new capital.
5. Check integrity: balance sheet balances, cash ties, no hardcodes inside formulas, version control, an error check row.

## Step 3: How much to raise and use of funds

1. Required raise = cumulative burn to the next value-inflection milestone + 6 to 9 months of buffer (fundraising takes 3 to 6 months) + contingency.
2. Milestones: the metrics the next round will require (for example growth rate, revenue scale, retention, margin, regulatory approval); show how the money reaches them.
3. Use of funds as percentages by function: product, go-to-market, hiring, infrastructure, G&A; reconcile to the model.
4. Dilution: raise amount / post-money valuation; show ownership after the round and option pool top-up; consider structure alternatives (SAFE, convertible, priced round, venture debt, revenue-based financing) and their cost and covenants.

## Step 4: Data room (indexed folders)

1. Corporate: formation, bylaws, board minutes, shareholder agreements, cap table with all instruments.
2. Financial: annual and monthly statements (24 to 36 months), management accounts, budget, model, tax returns, bank statements summary, debt agreements, KPI definitions and support.
3. Commercial: top customer contracts, pipeline, pricing, churn analysis, cohort data.
4. People: org chart, key employee agreements, option plan and grant ledger, contractor agreements, policies.
5. Legal and IP: IP assignments, licences, trademarks, litigation, regulatory approvals.
6. Tech and security: architecture overview, security policies, incident log, third-party dependencies.
Use a view-tracking data-room tool, control access by stage, watermark sensitive files, log every upload. Never share unredacted personal data.

## Step 5: Diligence response

1. Prepare an FAQ on known weak points (customer concentration, a down month, a change in metric definition) with the explanation and evidence.
2. Reconcile every number in the pitch deck to the model and to the ledger; one version of truth.
3. Quality-of-earnings style review for later rounds and debt: see `quality-of-earnings-review`.
4. Track requests in a log (request, owner, date, status); aim to answer within 48 hours.

## Failure modes

- Metrics computed in a spreadsheet from memory that don't tie to billing.
- ARR including one-off or non-recurring revenue.
- Unrecorded SAFEs or side letters surfacing in diligence.
- Model with a hockey stick untied to drivers.
- Overstating runway (ignoring payables, tax liabilities, deferred payroll).
- Mixing personal and company expenses.

## Output

Readiness scorecard with remediation plan, three-statement model and scenario summary, raise-size and use-of-funds table, indexed data-room checklist, diligence request log, and a one-page metrics definitions sheet.
