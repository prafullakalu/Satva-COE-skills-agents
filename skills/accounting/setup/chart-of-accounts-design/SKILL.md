---
name: chart-of-accounts-design
description: >-
  Design, review or clean up a chart of accounts: numbering, account types, control and clearing accounts, tracking dimensions, mapping to financial statement lines, and merge or retire rules. Use for "design a chart of accounts", "clean up the COA", "too many accounts", "map accounts to the P&L", "add an account", or "restructure categories".
metadata:
  department: "accounting"
  domain: "setup"
  owner: "satva-coe"
  status: "beta"
  license: "Satva-original"
  source: "original"
---

# Chart of accounts design

A chart answers financial-statement questions with the fewest accounts that still separate things with different tax, control or decision treatment. Account count is a cost: every account is something to reconcile, map and explain.

## 1. Inputs

Business model, entity type, jurisdiction and tax regime, basis (cash or accrual), reporting needs (lender covenants, investors, grants, segment reporting), existing chart if any, systems that post into the ledger (payroll, payment processors, inventory).

## 2. Structure and numbering

Use a gapped numeric scheme so accounts can be inserted without renumbering:

| Range | Class | Normal balance |
|---|---|---|
| 1000-1999 | Assets (cash, receivables, inventory, prepaids, fixed assets, accumulated depreciation) | Debit (contra: credit) |
| 2000-2999 | Liabilities (payables, accruals, tax, deferred revenue, loans) | Credit |
| 3000-3999 | Equity (capital, drawings or dividends, retained earnings) | Credit |
| 4000-4999 | Revenue and contra-revenue (returns, discounts) | Credit |
| 5000-5999 | Cost of sales | Debit |
| 6000-7999 | Operating expenses | Debit |
| 8000-8999 | Other income and expense (interest, FX, gains and losses) | by nature |
| 9000-9999 | Tax expense, suspense and system-use | Debit |

Keep the tree two levels deep: header and posting accounts. Posting only to leaf accounts.

## 3. Accounts every chart needs

- **Control accounts**, one per subledger: accounts receivable, accounts payable, inventory, fixed assets, payroll liabilities. Block manual journals to them where the system allows (see `subledger-to-gl-reconciliation`).
- **Clearing accounts**: payment processor clearing, undeposited funds, payroll clearing, intercompany due-to and due-from per counterparty. Each must have a reconciliation and should clear to zero.
- **Tax accounts**: sales tax or VAT/GST payable and receivable (separate input and output), income tax payable, payroll tax payable.
- **Suspense**: one named suspense account for unidentified bank items, with a rule that it is cleared before period close and reviewed for age.
- **Equity roll-forward**: opening balance equity (zero after setup), retained earnings (system), current-year earnings (system).
- **FX**: realised and unrealised gain or loss, separate.
- **Rounding**: only if the system needs one; investigate anything beyond cents.

## 4. Expenses: separate by decision, not by vendor

Create a separate account only when at least one is true: different tax treatment (for example meals, entertainment, fines, owner personal), different reporting line (cost of sales versus operating), a budget owner reviews it, a regulator or lender asks for it, or the annual amount is material. Everything else belongs in a broader account, with detail via tracking categories or the transaction description.

Never create accounts per vendor or per customer. Use contacts for that.

## 5. Dimensions instead of duplicates

Use tracking categories, classes, departments or locations for "same account, different slice" (department, project, channel). Rule of thumb: if you would be tempted to create "Marketing - Region A" and "Marketing - Region B", add a dimension.

## 6. Map to statements

Give every posting account a statement line (for example P&L: revenue, cost of sales, operating expense by function; balance sheet: current versus non-current). Keep a mapping table in the client file. Unmapped accounts are a defect found at first reporting.

## 7. Reviewing or cleaning an existing chart

1. Pull the trial balance for the last 24 months with transaction counts per account.
2. Classify each account: keep, merge, rename, retire, wrong-type.
3. Candidates to merge: duplicates by meaning, accounts under about 5 transactions a year with no distinct treatment.
4. Wrong-type examples: loan principal in expenses, owner draws in expenses, prepaid in expense, deposits in revenue.
5. Retire by marking inactive after the balance is zero; do not delete accounts that have history. Merging changes history: do it only at a closed-period boundary, with a documented before and after trial balance, and prefer a reclassification journal in the current period when the prior period was filed.
6. Propose the change list and wait for approval before touching a live chart.

## 8. Naming rules

Plain names ("Software subscriptions", not "Misc 2"), no vendor names, no dates, consistent singular or plural, record the purpose in the account description for any non-obvious account.

## Output

Chart table (number, name, type, statement line, control or clearing flag, tax code default, description), mapping notes, and for a cleanup the change list with before and after balances.

## Do not

- Reuse a number for a different meaning.
- Put payroll, tax or loan liabilities in one catch-all "other liabilities".
- Leave tax defaults unset on accounts that carry taxable transactions.
- Retire an account with a non-zero balance or open items.
