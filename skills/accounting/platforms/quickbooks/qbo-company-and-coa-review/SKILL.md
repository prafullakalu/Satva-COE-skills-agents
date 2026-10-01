---
name: qbo-company-and-coa-review
description: >-
  Review a QuickBooks Online company's setup and chart of accounts: features switched on (class/location tracking, multicurrency, inventory, sales tax), report basis, account types and detail types, junk and duplicate accounts, catch-all accounts, inactive accounts with balances, class/location strategy. Use when asked to "review the QuickBooks setup", "audit the chart of accounts", "clean up the COA", "take over this QBO file", "onboard a new client in QuickBooks", or "why is this account type wrong".
metadata:
  department: "accounting"
  domain: "setup"
  platform: "quickbooks"
  owner: "satva-coe"
  status: "stable"
  license: "Satva-original"
  source: "original"
---

# QuickBooks company and chart of accounts review

Read-only by default. Follow `qbo-mcp-operating-rules` for company selection and for any change.

## Workflow
1. **Company and features.** `list_companies`, then `get_company_overview` (pass `company`). Record: legal name, country, fiscal year start month, home currency, multicurrency on/off, class tracking, location tracking (`departmentTerminology` tells you whether the UI says Location or Department), inventory (quantity on hand), sales tax, report basis, payroll, plan name and users when readable.
2. **Preferences that bite later** via `get_entity` with `entity: "Preferences"`: the default report basis (`ReportPrefs.ReportBasis`), whether class tracking is per transaction or per line (`AccountingInfoPrefs`), whether `TrackDepartments` is on, and tax prefs. Multicurrency and inventory cannot be switched off once used, so flag any "on" that the business does not need.
3. **Pull the full chart.** `get_account_list` (report) for the readable list, or `query_quickbooks` with `SELECT * FROM Account MAXRESULTS 1000` for fields (`AccountType`, `AccountSubType`, `Classification`, `CurrentBalance`, `Active`, `SubAccount`, `ParentRef`). For inactive accounts add `account_status: "All"` on the report or `WHERE Active IN (true,false)` in the query.
4. **Run the checks below** and list findings with the account name, Id and balance.
5. **Balance sanity.** `get_trial_balance` at the last month end and `get_balance_sheet`. Check the trial balance foots (debits equal credits) and compare to the prior accountant's numbers if given.
6. **Report** findings in the format at the end. Propose fixes; change nothing without approval.

## Checks
**Structure**
- Every account has the right `AccountType` and a sensible `AccountSubType` (detail type). Type drives which report section and which cash-flow bucket the account lands in, and cannot be freely changed between some families once transactions exist.
- Accounts are not mis-typed: loans as Other Current Liability instead of Long Term Liability, owner draws booked to Expense, prepaid expense in Expense instead of Other Current Asset, fixed-asset cost netted with depreciation in one account.
- Sub-accounts nest under the correct parent; no sub-account whose parent has a different type family.
- Numbering: if account numbers are used, they are on for all accounts and follow a consistent scheme; mixed numbered and un-numbered accounts are a smell.

**Junk and duplicates**
- Near-duplicate names ("Office Supplies" and "Office supplies and software"), one-off accounts with a single transaction, accounts named after a vendor or person.
- Catch-all accounts: `Uncategorized Expense`, `Uncategorized Income`, `Uncategorized Asset`, `Ask My Accountant`, `Opening Balance Equity`, `Retained Earnings` activity, and `Undeposited Funds` or `Payroll Clearing` with non-zero balances. Run `uncategorized_transactions` for the first group (it covers accounts named "Uncategorized ..." and "Ask My Accountant", up to 6 accounts). A non-zero `Opening Balance Equity` after the first period is an error to be explained and cleared; see `qbo-data-cleanup`.
- Inactive accounts with a non-zero `CurrentBalance`: balance is hidden from pick-lists but still on the balance sheet.

**Control accounts**
- Exactly the expected system accounts exist: Accounts Receivable, Accounts Payable, Undeposited Funds, Opening Balance Equity, Retained Earnings, Inventory Asset (if inventory is on), Sales Tax Payable (if tax is on). Multi-currency companies also have one A/R and A/P per currency; that is normal.
- A/R and A/P balances on the balance sheet equal the totals on `get_aged_receivables` and `get_aged_payables` at the same date. If not, a journal entry has been posted straight to a control account; find it with `get_general_ledger` filtered by `account`.

**Class and location strategy** (only if enabled)
- Decide what each dimension means before using it: Class = business line or program; Location (Department) = physical or legal unit. Mixing the two meanings in one list is the usual failure.
- Per-transaction vs per-line class tracking: per-line is more flexible but needs a class on every line; check how many recent transactions lack one by running `get_profit_and_loss` with `summarize_column_by: "Classes"` and reading the "Not specified" column.
- Class is not a ledger split: a balance sheet is not class-balanced, so class P&L totals can differ from the whole-company P&L only through unclassified amounts.

**Tax and basis**
- Report basis (accrual or cash) matches what the accountant and the tax return use. Basis is a report setting, not a data difference; confirm the number you quote says which one.

## Fix proposals (examples, each needs approval)
- Rename or merge: QBO merges two accounts when one is renamed to the exact name of the other of the same type; this re-points history irreversibly. Prefer deactivating the junk account after moving its transactions with a reclass journal (`qbo-journal-entries`).
- Create a missing account: `create_entity` `Account` with `Name`, `AccountType`, `AccountSubType` (see `describe_entity` for the required fields).
- Deactivate: `delete_entity` on an Account deactivates it (accounts cannot be deleted). Zero the balance first.
- Fixing a type: change `AccountType` or `AccountSubType` with `update_entity` only after reading the account's transaction count; if the change is refused, create the right account and reclass.

## Output
1. Company profile (one table).
2. Findings, ranked High/Medium/Low, each: what, where (account Id), evidence (balance or count), proposed fix.
3. Questions for the owner or accountant.
4. "Not checked": anything the tools could not see (bank feed items are not visible to the API; locked closing-date settings are not read).
