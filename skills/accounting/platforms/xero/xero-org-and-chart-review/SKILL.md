---
name: xero-org-and-chart-review
description: >-
  Reviews a Xero organisation's setup and chart of accounts through the Satva Xero MCP: org settings, base currency,
  period lock date, sales tax basis, system and bank accounts, duplicate or unused accounts, suspense/clearing
  accounts, tax type on accounts, and safe account creation or archiving. Use for "review our Xero setup", "audit the
  chart of accounts", "new Xero org onboarding", "clean up accounts", "add an account", "archive accounts", or
  "do we have a suspense account".
metadata:
  department: "accounting"
  domain: "setup"
  platform: "xero"
  owner: "satva-coe"
  status: "stable"
  license: "Satva-original"
  source: "original"
---

# Xero organisation and chart-of-accounts review

Follow `xero-mcp-operating-rules` first (org selection, confirm before write).

## Tools used

Read: `list-companies`, `list-organisation-details`, `list-accounts`, `list-tax-rates`, `list-currencies`,
`list-tracking-categories`, `list-users`, `list-trial-balance`, `list-report-bank-summary`.
Write: `create-account`, `update-account`, `archive-account`.

## Workflow

1. **Identify the org.** `list-organisation-details`. Record legal name, country, base currency, financial year end
   (day/month), sales tax basis (cash vs accrual) and period, `Period Lock Date`, organisation type. If no period
   lock date is shown, flag it: nothing stops back-dated entries into closed periods.
2. **Pull the chart.** `list-accounts` (one call, no paging). Group by Type. Count ACTIVE vs ARCHIVED.
3. **Run the checks** below; log each as finding / evidence / risk / proposed fix.
4. **Cross-check with balances.** `list-trial-balance` at today's date: accounts with balances that are archived,
   wrongly signed, or sit in an account named like a clearing/suspense account.
5. **Propose, confirm, then change** (section "Making changes").
6. Deliver the review in the output format at the end.

## Checks

| # | Check | How | Why it matters |
|---|---|---|---|
| 1 | Base currency and country match the entity | org details | base currency cannot be changed after transactions exist |
| 2 | Period lock date set and recent | org details | back-dating into filed periods corrupts tax returns |
| 3 | Sales tax basis and period correct for the registration | org details | wrong basis changes when tax is reported |
| 4 | Duplicate names or near-duplicates (e.g. "Bank Fees" vs "Bank Charges") | list-accounts | split reporting, mispostings |
| 5 | Code scheme consistent (ranges per type; no gaps used as meaning) | list-accounts | maintainability, 10-char code limit |
| 6 | Every account has a sensible default `Tax Type` | list-accounts Tax Type vs list-tax-rates | wrong default tax is the most common systematic error |
| 7 | Suspense / clearing / "Ask my accountant" / "Uncategorised" accounts | name match + TB balance | should be zero at period end; a balance means unresolved items |
| 8 | Bank accounts: one per real account, correct type BANK, no stale ones | Type=BANK, bank summary | stale bank accounts hide unreconciled cash |
| 9 | System accounts present (Accounts Receivable, Accounts Payable, Retained Earnings, etc.) and untouched | list-accounts | Xero blocks archiving these; renames confuse reports |
| 10 | Archived accounts that still carry a balance | TB | balance is orphaned from normal views |
| 11 | Expense accounts used as catch-all ("General Expenses" large vs the rest) | P&L (see `xero-reports-pack`) | weak management information |
| 12 | Tracking categories exist and are used consistently | `list-tracking-categories` | see `xero-tracking-categories` |

## Pitfalls

- A suspense balance is not a presentation issue; it is unposted work. Do not "net it off" with a journal until the
  underlying items are identified.
- `update-account` can change only name, description, tax type and enablePaymentsToAccount. Code and type are fixed
  after creation: a wrong type means create a new account and move balances with a journal
  (`xero-manual-journals`), then archive the old one.
- Changing an account's default tax type does not change existing transactions; it only affects new ones.
- `archive-account` is refused for system accounts, and Xero rejects it when the account is still in use. Archiving
  is reversible only in the Xero UI.
- Bank accounts (`type BANK`) require `bankAccountNumber` on create; creating one here does not connect a bank feed.
  Feeds are set up in Xero by a user with bank access.
- Do not rename accounts that the organisation's reports or integrations reference by code without checking who
  depends on them; ask the user.

## Making changes

1. Before `create-account`: confirm the code is unused (`list-accounts`), the type is right (it cannot change), and
   the `taxType` exists in `list-tax-rates` and is allowed on that account type.
2. Show the user `code | name | type | tax type | payments enabled` and wait for yes.
3. After a write, re-run `list-accounts` and confirm the single new/changed row.
4. Archive in small, named batches. Before each: confirm zero balance on the TB and no open drafts using it.

## Output format

```
Org: <name> | base <CCY> | FYE <dd mmm> | lock date <date or NONE> | tax basis <cash/accrual>
Summary: <n> active accounts, <n> archived. <n> findings (H/M/L).
Findings (table): # | finding | evidence (account code/name, balance) | risk | proposed fix
Safe quick wins / Needs accountant decision / Do not touch
```
