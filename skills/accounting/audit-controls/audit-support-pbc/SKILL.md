---
name: audit-support-pbc
description: >-
  Prepare for and support an external or internal audit: build the provided-by-client (PBC) request list, assemble support by account, manage sampling requests, track open requests and respond to auditor queries. Use for "audit PBC list", "prepare for the audit", "auditor asked for support", "sample selection support", "audit readiness".
metadata:
  department: "accounting"
  domain: "audit-controls"
  owner: "satva-coe"
  status: "beta"
  license: "Satva-original"
  source: "original"
---

# Audit support and PBC management

Goal: shorten the audit by delivering complete, consistent, indexed support the first time. Audit scope and procedures are the auditor's call; you supply evidence.

## Timeline
| When | Action |
|---|---|
| 8-10 weeks before | Agree timetable, scope, materiality conversation, PBC list, portal/access |
| 4-6 weeks before | Interim work: controls walkthroughs, early cut-off testing, confirmations sent |
| Year-end close | Close and lock (quarter-and-year-end-close) |
| Fieldwork | Daily request tracker stand-up; response SLA 2 working days |
| Post fieldwork | Draft FS review, management representation letter, adjustments, management letter responses |

## PBC list: standard contents, by area
- **General:** trial balance and GL detail; prior-year FS and adjustments; chart of accounts; org chart; board/shareholder minutes; policies; related-party list; legal letters; insurance schedule.
- **Cash:** bank recs for every account at year end; bank statements for the last month and the first month after; confirmations authorised.
- **Receivables/revenue:** AR ageing tied to GL; subsequent receipts; credit notes after year end; contracts for top customers and unusual terms; revenue recognition memos (revenue-recognition-606); confirmation list; allowance calculation.
- **Inventory:** count sheets, count instructions, roll-forward between count and year-end, costing support, reserves (ecommerce-inventory-cogs).
- **Fixed assets:** register, additions over threshold with invoices, disposals, depreciation recalc (fixed-assets-depreciation).
- **Payables/accruals:** AP ageing, unrecorded-liabilities search (payments and bills after year end), accrual schedules with support.
- **Debt/equity/leases:** agreements, statements, covenant calculations, lease schedules, cap table.
- **Payroll:** payroll register to GL tie-out, year-end returns (payroll-accounting), bonus and leave calculations.
- **Tax:** provision and deferred tax workings, returns filed, notices.
- **Journals:** listing of manual and post-close journals with preparer/approver and support.
- **Intercompany:** matched balances, eliminations (multi-entity-intercompany-consolidation).
- **Controls:** RCM, evidence of key controls (internal-controls-matrix).

## Request tracker
Columns: ID | area | request (verbatim) | owner | date requested | due | date delivered | file path/link | status (open, delivered, follow-up, closed) | auditor comment. Single tracker, single source; never answer requests by email without logging them.

## Assembling support
1. Index folder by TB account number; each file named `<acct>-<description>-<period>`.
2. Every schedule ties to the GL: show the tie-out line (schedule total, GL balance, difference = 0).
3. Documents are complete (all pages), legible, and sourced (system report with run date, user, filters).
4. For sample requests: provide the population report first, let the auditor select, then pull documents for exactly those items. Do not cherry-pick.
5. Review before release: second person checks that amounts agree to the GL and that no confidential content outside scope (other clients, personal data) is exposed.

## Responding to queries
Answer the question asked, with evidence, and state facts not opinions. If something is wrong, say so promptly and propose the correction with an entry and support. Unknowns: say "to be confirmed by <name> by <date>". Do not backdate or alter documents; provide corrected documents with a new version note.

## Management letter follow-up
Log each finding with root cause, owner, fix and target date; verify closure before next year's audit.

## Do not
Do not provide documents you have not reviewed; do not edit source records after request (create an adjusting entry instead); do not delay bad news to the end of fieldwork.

## Output
PBC list with owners and due dates, tracker, indexed support folder, tie-out sheet, post-audit action log.

See also: `sox-404-audit-support-methodology` (evidence standards, sampling) and `sox-testing` (testing workpapers).
