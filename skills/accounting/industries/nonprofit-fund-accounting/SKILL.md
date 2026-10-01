---
name: nonprofit-fund-accounting
description: >-
  Nonprofit and fund accounting: net-asset classes (with and without donor restrictions), restricted gifts and grants, release from restriction, pledges and conditional contributions, functional expense allocation, program/admin/fundraising reporting, Form 990 alignment and grant compliance. Use when books for a charity, association, foundation or school are being set up, closed or cleaned, or when someone says "restricted funds", "grant reporting", "net assets", "functional expenses", "pledges receivable", "ASU 2018-08" or "fund accounting in QuickBooks/Xero".
metadata:
  department: "accounting"
  domain: "industries"
  owner: "satva-coe"
  status: "beta"
  license: "Satva-original"
  source: "original"
---

# Nonprofit and fund accounting

Nonprofit books answer two questions a commercial ledger does not: did we spend restricted money only as the donor allowed, and what did each program cost. Everything below serves those two questions. US GAAP (ASC 958) is assumed; IFRS or local charity SORP differences are noted where they bite.

## Step 1: Set the structure before posting anything

1. **Net-asset classes.** Two classes only under ASU 2016-14: *without donor restrictions* and *with donor restrictions* (purpose-restricted, time-restricted, or perpetual). Board designations stay inside "without restrictions" and are shown as a sub-line, never as a restriction.
2. **Chart of accounts.** Give revenue accounts a restriction attribute, not a separate account per grant. Use the platform's class/tracking category/fund dimension for *Fund* (restricted purpose) and *Program* (service line). Expense accounts are natural (salaries, rent); program/admin/fundraising comes from a second dimension, not from account names.
3. **Fund register.** One row per restricted source: donor/funder, purpose, amount, period, release condition, reporting due date, reimbursable or advance, indirect-cost rate. This register is the control; the ledger must tie to it.

## Step 2: Classify each inflow

| Inflow | Test | Treatment |
|---|---|---|
| Unconditional contribution | No barrier and no right of return | Revenue now; with-restriction if donor-stipulated |
| Conditional contribution (ASU 2018-08) | Barrier (match, milestone, qualifying expense) AND right of release/return | Not revenue; hold as refundable advance or off-book until the barrier is met |
| Exchange transaction (fees, tuition, contracts for deliverables) | Commensurate value received | ASC 606 revenue, no restriction |
| Pledge | Written promise, unconditional | Receivable at present value if due beyond one year; allowance for uncollectible |
| Gift in kind | Fair value at gift date | Revenue and matching asset or expense; document the valuation basis |
| Government grant | Cost-reimbursement vs fixed fee | Cost-reimbursement is conditional: revenue as qualifying costs are incurred |

A restriction is released to "without restrictions" when the purpose is met or the time passes. Post it as a transfer between classes (reclassification line on the statement of activities), not as new income. A restricted gift spent in the same period it was received may be shown as unrestricted only if the policy is applied consistently and disclosed.

## Step 3: Allocate functional expenses

Every expense is program, management and general, or fundraising. Direct costs are coded at entry. Shared costs (rent, utilities, shared salaries, IT) are allocated on a documented basis: square footage, time sheets, headcount, or direct-cost ratio. Rules:
- Write the allocation policy down and apply it the same way every period.
- Staff time allocations need a time record or an annual time study, not a guess.
- Fundraising includes the cost of donor solicitations and events net of direct donor benefit; report gross special-event revenue and the direct benefit cost separately.
- The statement of functional expenses (natural classification by function) must foot to the statement of activities.

## Step 4: Month-end

1. Reconcile cash by fund: bank total equals the sum of fund cash balances.
2. Release restrictions for the month's qualifying spend; tie to the fund register.
3. Review grants: spend vs award, burn rate vs time elapsed, unspent balances, reimbursement requests due.
4. Accrue pledges received and write down doubtful ones.
5. Allocate shared costs and review the program/admin/fundraising ratio for reasonableness (funders and rating bodies read it).
6. Check that no restricted fund is overdrawn (negative net assets with restrictions means unrestricted money is subsidising it; flag to the finance lead).

## Step 5: Year-end and external reporting

- Statements: financial position, activities, cash flows, functional expenses, and notes (liquidity and availability, restrictions, concentrations, related parties).
- Liquidity disclosure: financial assets available within one year less donor restrictions and board designations.
- Form 990 / local return: reconcile the 990 revenue and expense totals to the audited statements; differences (unrealized gains, in-kind, donor-benefit) go on the reconciliation schedule.
- Single audit threshold for US federal awards (check the current expenditure threshold in the Uniform Guidance) triggers a compliance audit.
- Perpetual endowments: track UPMIFA/local-law spending policy, appropriation, and underwater funds.

## Failure modes

- Booking a conditional grant as revenue on award letter signature.
- Releasing restrictions on cash receipt rather than on spend.
- One bank account and one big "restricted" liability account with no fund detail.
- Indirect costs charged above the negotiated or de minimis rate.
- Allocating on a basis nobody can reproduce when the auditor asks.
- Treating board-designated funds as restricted.

## Output

Fund register tied to the ledger, month-end checklist with sign-off, restriction-release schedule, functional-expense allocation workpaper, and a grant-compliance tracker (award, spend, remaining, next report due).
