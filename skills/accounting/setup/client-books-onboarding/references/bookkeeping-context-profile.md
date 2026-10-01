<!-- Adapted from Receiptor-AI/bookkeeping-skills skills/bookkeeping-setup (MIT, Copyright (c) 2026 Receiptor AI). Modified by Satva: condensed, tool-agnostic. -->

# Bookkeeping context profile

Create this before downstream bookkeeping work so agents do not guess entity type, accounting method, tax treatment, approval boundaries or chart structure. Look for an existing profile first (project notes, onboarding doc, accounting export, prior agent output); if one exists, summarise it and ask only for missing or stale fields.

```yaml
bookkeeping_context_profile:
  business: {legal_name, trade_name, entity_type, jurisdiction, home_currency, fiscal_year_end}
  tax: {country, filing_context, sales_tax_or_vat_registered, payroll_in_use, contractor_payments_expected}
  accounting: {method: cash|accrual|unknown, books_tool, bank_accounts, credit_cards, connected_sources, chart_of_accounts_baseline}
  operations: {receipt_sources, bank_statement_sources, recurring_vendors, approval_thresholds, posting_policy, record_retention_policy}
  review: {can_auto_draft, requires_user_approval, requires_accountant_review, open_questions}
```

## Choosing the accounting basis

| Situation | Likely method |
|---|---|
| Solo operator, simple services | Cash (common default; confirm for tax) |
| Tracks unpaid invoices or vendor bills | Accrual or hybrid |
| Inventory-heavy | Accrual; inventory and cost of sales need tighter controls |
| Unsure | Unknown: do not infer final tax treatment; flag method-sensitive decisions |

Cash basis records income and expense when money moves. Accrual adds receivables, payables, accruals, prepaids, deferred revenue and adjusting entries.

## Starter chart baseline

A practical baseline, not an overbuilt system: cash and bank accounts, credit cards and loans, revenue, cost of goods sold if applicable, operating expenses mapped to the relevant tax lines, owner equity with draws and contributions, and sales tax, VAT, payroll or contractor liabilities where they apply. Keep jurisdiction-specific mappings explicit and marked for review. Full design rules: `chart-of-accounts-design`.

## Approval boundaries

Safe to draft without asking: collecting setup facts from available context, drafting the profile, proposing a chart baseline, listing missing data, preparing import maps, review queues and draft rules.

Require explicit approval before: changing accounting-system settings; creating, renaming, merging or deleting accounts; posting journals; locking periods; filing tax, VAT, payroll or contractor returns; applying tax treatment to ambiguous items.

Require accountant review when: entity type or tax election is unclear; cash versus accrual affects material amounts; inventory, payroll, sales tax, multi-entity or international tax is involved; owner transactions are mixed with business activity.

## Setup checklist to finish with

```
Business identity captured: yes/no        Entity type confirmed: yes/no
Tax jurisdiction confirmed: yes/no        Accounting method: cash/accrual/unknown
Chart baseline drafted: yes/no            Source systems listed: yes/no
Approval thresholds set: yes/no           Record retention policy set: yes/no
Open questions: ...                       Recommended next skill: ...
```

Hand-offs: capture documents -> `receipt-ocr-intake`; categorise -> `transaction-categorisation-rules`; match to statements -> `bank-reconciliation`; close a month -> the close skills; accountant or tax package -> the tax skills.
