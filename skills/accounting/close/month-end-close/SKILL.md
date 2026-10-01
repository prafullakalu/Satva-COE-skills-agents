---
name: month-end-close
description: >-
  Run the month-end close end to end: pre-close checklist, day-by-day close calendar (5-day and accelerated 3-day), task dependency levels and critical path, status tracking, close metrics, bottleneck fixes and retrospective, plus balance sheet reconciliation standard, materiality, evidence and red flags. Use for "run the month-end close", "close checklist", "close calendar", "what blocks the period lock", "why does close take so long", "close status".
metadata:
  department: "accounting"
  domain: "period-close"
  owner: "satva-coe"
  status: "beta"
  license: "Apache-2.0"
  source: "https://github.com/anthropics/knowledge-work-plugins/blob/main/finance/skills/close-management"
---
<!-- Adapted from anthropics/knowledge-work-plugins (Apache-2.0, no copyright line in LICENSE; Anthropic). Modified by Satva: frontmatter to Satva contract; folded in Satva original inputs, reconciliation standard, evidence, red flags and do-not list. -->
# Month-end close

**Important**: This skill assists with close management workflows but does not provide financial advice. All close activities should be reviewed by qualified financial professionals.

Month-end close checklist, task sequencing and dependencies, status tracking, and common close activities organized by day.

## Month-End Close Checklist

### Pre-Close (Last 2-3 Business Days of the Month)

- [ ] Send close calendar and deadline reminders to all contributors
- [ ] Confirm cut-off procedures with AP, AR, payroll, and treasury
- [ ] Verify all sub-systems are processing normally (ERP, payroll, banking)
- [ ] Complete preliminary bank reconciliation (all but last-day activity)
- [ ] Review open purchase orders for potential accrual needs
- [ ] Confirm payroll processing schedule aligns with close timeline
- [ ] Collect information for any known unusual transactions

### Close Day 1 (T+1: First Business Day After Month-End)

- [ ] Confirm all sub-ledger modules have completed period-end processing
- [ ] Run AP accruals for goods/services received but not invoiced
- [ ] Post payroll entries and payroll accrual (if pay period straddles month-end)
- [ ] Record cash receipts and disbursements through month-end
- [ ] Post intercompany transactions and confirm with counterparties
- [ ] Complete bank reconciliation with final bank statement
- [ ] Run fixed asset depreciation
- [ ] Post prepaid expense amortization

### Close Day 2 (T+2)

- [ ] Complete revenue recognition entries and deferred revenue adjustments
- [ ] Post all remaining accrual journal entries
- [ ] Complete AR subledger reconciliation
- [ ] Complete AP subledger reconciliation
- [ ] Record inventory adjustments (if applicable)
- [ ] Post FX revaluation entries for foreign currency balances
- [ ] Begin balance sheet account reconciliations

### Close Day 3 (T+3)

- [ ] Complete all balance sheet reconciliations
- [ ] Post any adjusting journal entries identified during reconciliation
- [ ] Complete intercompany reconciliation and elimination entries
- [ ] Run preliminary trial balance and income statement
- [ ] Perform preliminary flux analysis on income statement
- [ ] Investigate and resolve material variances

### Close Day 4 (T+4)

- [ ] Post tax provision entries (income tax, sales tax, property tax)
- [ ] Complete equity roll-forward (stock compensation, treasury stock)
- [ ] Finalize all journal entries — soft close
- [ ] Generate draft financial statements (P&L, BS, CF)
- [ ] Perform detailed flux analysis and prepare variance explanations
- [ ] Management review of financial statements and key metrics

### Close Day 5 (T+5)

- [ ] Post any final adjustments from management review
- [ ] Finalize financial statements — hard close
- [ ] Lock the period in the ERP/GL system
- [ ] Distribute financial reporting package to stakeholders
- [ ] Update forecasts/projections based on actual results
- [ ] Conduct close retrospective — identify process improvements

## Task Sequencing and Dependencies

### Dependency Map

Tasks are organized by what must complete before the next task can begin:

```
LEVEL 1 (No dependencies — can start immediately at T+1):
├── Cash receipts/disbursements recording
├── Bank statement retrieval
├── Payroll processing/accrual
├── Fixed asset depreciation run
├── Prepaid amortization
├── AP accrual preparation
└── Intercompany transaction posting

LEVEL 2 (Depends on Level 1 completion):
├── Bank reconciliation (needs: cash entries + bank statement)
├── Revenue recognition (needs: billing/delivery data finalized)
├── AR subledger reconciliation (needs: all revenue/cash entries)
├── AP subledger reconciliation (needs: all AP entries/accruals)
├── FX revaluation (needs: all foreign currency entries posted)
└── Remaining accrual JEs (needs: review of all source data)

LEVEL 3 (Depends on Level 2 completion):
├── All balance sheet reconciliations (needs: all JEs posted)
├── Intercompany reconciliation (needs: both sides posted)
├── Adjusting entries from reconciliations
└── Preliminary trial balance

LEVEL 4 (Depends on Level 3 completion):
├── Tax provision (needs: pre-tax income finalized)
├── Equity roll-forward
├── Consolidation and eliminations
├── Draft financial statements
└── Preliminary flux analysis

LEVEL 5 (Depends on Level 4 completion):
├── Management review
├── Final adjustments
├── Hard close / period lock
├── Financial reporting package
└── Forecast updates
```

### Critical Path

The critical path determines the minimum close duration. Typical critical path:

```
Cash/AP/AR entries → Subledger reconciliations → Balance sheet recs →
  Tax provision → Draft financials → Management review → Hard close
```

To shorten the close:
- Automate Level 1 entries (depreciation, prepaid amortization, standard accruals)
- Pre-reconcile accounts during the month (continuous reconciliation)
- Parallel-process independent reconciliations
- Set clear deadlines with consequences for late submissions
- Use standardized templates to reduce reconciliation prep time

## Status Tracking and Reporting

### Close Status Dashboard

Track each close task with the following attributes:

| Task | Owner | Deadline | Status | Blocker | Notes |
|------|-------|----------|--------|---------|-------|
| [Task name] | [Person/role] | [Day T+N] | Not Started / In Progress / Complete / Blocked | [If blocked, what's blocking] | [Any notes] |

### Status Definitions

- **Not Started:** Task has not yet begun (may be waiting on dependencies)
- **In Progress:** Task is actively being worked on
- **Complete:** Task is finished and has been reviewed/approved
- **Blocked:** Task cannot proceed due to a dependency, missing data, or issue
- **At Risk:** Task is in progress but may not meet its deadline

### Daily Close Status Meeting (Recommended)

During the close period, hold a brief (15-minute) daily standup:

1. **Review status board:** Walk through open tasks, flag any that are behind
2. **Identify blockers:** Surface any issues preventing task completion
3. **Reassign or escalate:** Adjust ownership or escalate blockers to resolve quickly
4. **Update timeline:** If any tasks are at risk, assess impact on overall close timeline

### Close Metrics to Track Over Time

| Metric | Definition | Target |
|--------|-----------|--------|
| Close duration | Business days from period end to hard close | Reduce over time |
| # of adjusting entries after soft close | Entries posted during management review | Minimize |
| # of late tasks | Tasks completed after their deadline | Zero |
| # of reconciliation exceptions | Reconciling items requiring investigation | Reduce over time |
| # of restatements / corrections | Errors found after close | Zero |

## Common Close Activities by Day

### Typical 5-Day Close Calendar

| Day | Key Activities | Responsible |
|-----|---------------|-------------|
| **T+1** | Cash entries, payroll, AP accruals, depreciation, prepaid amortization, intercompany posting | Staff accountants, payroll |
| **T+2** | Revenue recognition, remaining accruals, subledger reconciliations (AR, AP, FA), FX revaluation | Revenue accountant, AP/AR, treasury |
| **T+3** | Balance sheet reconciliations, intercompany reconciliation, eliminations, preliminary trial balance, preliminary flux | Accounting team, consolidation |
| **T+4** | Tax provision, equity roll-forward, draft financial statements, detailed flux analysis, management review | Tax, controller, FP&A |
| **T+5** | Final adjustments, hard close, period lock, reporting package distribution, forecast update, retrospective | Controller, FP&A, finance leadership |

### Accelerated Close (3-Day Target)

For organizations targeting a faster close:

| Day | Key Activities |
|-----|---------------|
| **T+1** | All JEs posted (automated + manual), all subledger reconciliations, bank reconciliation, intercompany reconciliation, preliminary trial balance |
| **T+2** | All balance sheet reconciliations, tax provision, consolidation, draft financial statements, flux analysis, management review |
| **T+3** | Final adjustments, hard close, reporting package, forecast update |

**Prerequisites for a 3-day close:**
- Automated recurring journal entries (depreciation, amortization, standard accruals)
- Continuous reconciliation during the month (not all at month-end)
- Automated intercompany elimination
- Pre-close activities completed before month-end (cut-off, accrual estimates)
- Empowered team with clear ownership and minimal handoffs
- Real-time or near-real-time sub-system integration

## Close Process Improvement

### Common Bottlenecks and Solutions

| Bottleneck | Root Cause | Solution |
|-----------|-----------|---------|
| Late AP accruals | Waiting for department spend confirmation | Implement continuous accrual estimation; set cut-off deadlines |
| Manual journal entries | Recurring entries prepared manually each month | Automate standard recurring entries in the ERP |
| Slow reconciliations | Starting from scratch each month | Implement continuous/rolling reconciliation |
| Intercompany delays | Waiting for counterparty confirmation | Automate intercompany matching; set stricter deadlines |
| Management review changes | Large adjustments found during review | Improve preliminary review process; empower team to catch issues earlier |
| Missing supporting documents | Scrambling for documentation at close | Maintain documentation throughout the month |

### Close Retrospective Questions

After each close, ask:
1. What went well this close that we should continue?
2. What took longer than expected and why?
3. What blockers did we encounter and how can we prevent them?
4. Were there any surprises in the financial results we should have caught earlier?
5. What can we automate or streamline for next month?


---

# Satva additions (controls and standards)

## Inputs to confirm before starting
- Period end date, entity, base currency, reporting basis (cash, accrual, IFRS, US GAAP).
- Prior period close package and open-items list (carry-forwards).
- Materiality: default for review = the lower of 0.5% of revenue or 5% of pre-tax income for the month; for SMEs also set an absolute floor (e.g. 250 in base currency) below which items are not investigated.
- Who prepares, who reviews. Preparer and reviewer must be different people; record both.

## Balance sheet reconciliation standard
For every balance sheet account: GL balance, supporting balance (statement, sub-ledger, schedule), difference, explanation of each reconciling item with age, preparer, reviewer, date. Tolerance: zero for cash and control accounts; judgement elsewhere but any unexplained difference over materiality escalates.

## Evidence to keep
Bank statements, reconciliation reports, accrual and prepaid schedules, depreciation run, payroll register, tax return working, flux commentary, signed checklist, lock-date screenshot or audit-log entry.

## Red flags
- Same person prepares and approves their own manual journals.
- Large round-number journals at period end without support.
- Reversals that do not reverse; recurring entries that stopped.
- Suspense balances carried more than one close.
- Close takes longer each month: usually unreconciled bank feeds or late AP.

## Do not
- Do not lock the period before the flux review is done.
- Do not plug differences to suspense or to retained earnings.
- Do not post into a locked period; reopen with approval and log it.

## Close package output
A close package: (1) completed checklist with names and dates, (2) trial balance, P&L and balance sheet, (3) flux commentary, (4) open-items list with owner and due date, (5) summary of adjustments posted after the first TB.

Related skills: flux-variance-analysis, quarter-and-year-end-close, financial-statement-preparation, accruals-deferrals-prepaids, bank-reconciliation, subledger-to-gl-reconciliation.
