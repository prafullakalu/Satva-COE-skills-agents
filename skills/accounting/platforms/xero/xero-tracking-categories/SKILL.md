---
name: xero-tracking-categories
description: >-
  Designs, audits and maintains Xero tracking categories and options via the Satva Xero MCP, and applies them
  correctly on invoice and bill lines. Use for "set up tracking categories", "departments / locations / projects in
  Xero", "tracking option missing on invoice", "report by tracking option", "archive a tracking option", "balance
  sheet by department", "why did the tracking disappear after an edit".
metadata:
  department: "accounting"
  domain: "tracking"
  platform: "xero"
  owner: "satva-coe"
  status: "stable"
  license: "Satva-original"
  source: "original"
---

# Xero tracking categories

Follow `xero-mcp-operating-rules`.

## Tools used

Read: `list-tracking-categories includeArchived?` (categories with options and IDs), `list-invoices`,
`list-bank-transactions`, `list-report-balance-sheet` (`trackingOptionID1`, `trackingOptionID2`).
Write: `create-tracking-category name`, `create-tracking-options trackingCategoryId optionNames[] (max 10)`,
`update-tracking-category trackingCategoryId name? status ACTIVE|ARCHIVED`, `update-tracking-options
trackingCategoryId options[{trackingOptionId, name?, status ACTIVE|ARCHIVED}] (max 10)`.
Use on documents: `create-invoice` / `update-invoice` / `create-purchase-order` line `tracking[]`.

## Xero facts that shape every design

- **Maximum two active tracking categories per organisation.** Plan them before creating one. A third is not
  possible without archiving one.
- Options are per category; each category holds a limited, manageable list. Keep options mutually exclusive and
  collectively exhaustive (every transaction can be assigned to exactly one).
- Tracking is applied **per line**, on invoices, bills, bank transactions, credit notes, quotes, POs, repeating
  documents. It is not attached to manual journal lines through this MCP.
- Tracking does not retroactively apply: past transactions are untagged unless edited.
- Archiving an option hides it from new transactions; existing history keeps it. Archive rather than delete.

## Workflow: design

1. Start from the reporting question (profit by department? location? project?). One category per question.
2. Check what exists: `list-tracking-categories includeArchived=true`. Reuse before creating.
3. Choose names a non-accountant understands ("Department", "Location"). Keep option names short and stable;
   renames change history labels.
4. Plan the account scope: Xero lets tracking be required on revenue/expense lines only through user discipline;
   P&L accounts are tracked, balance sheet tracking only via the balance sheet filters. Say what will not be tracked
   (payroll journals, bank fees, FX).
5. Create: `create-tracking-category name` then `create-tracking-options` (<= 10 per call). Verify with
   `list-tracking-categories`.

## Workflow: use on a document

1. Get the category `name`, `option` name and `trackingCategoryID` from `list-tracking-categories`. All three
   fields are required on each line's `tracking` entry.
2. Max 2 entries per line, one per category. Do not add tracking unless the user asked for it or the org's policy
   requires it.
3. On `update-invoice` re-send all lines **with** their tracking; any line or tracking omitted is lost.

## Workflow: audit

1. List categories, options, status. Find: option names that are typos or near-duplicates, archived options still in
   use, "Other"/"Unassigned" options with large volume, categories nobody uses.
2. Sample documents: page `list-invoices` (line items appear when queried by `invoiceNumbers`) and
   `list-bank-transactions`; compute % of lines with tracking and a breakdown by option. Anything that should be
   tracked but is not is the actionable list.
3. Balance sheet slice: `list-report-balance-sheet date trackingOptionID1=<id>` shows the balance sheet for that
   option; use to test that tracked balance-sheet items behave.
4. For P&L by option, the MCP P&L report has no tracking filter. Build it by summing tracked lines from
   transactions, and label it as derived, with coverage % (share of P&L activity actually tracked). Native
   "Profit and Loss by tracking category" is a Xero UI report.

## Maintenance

- Rename an option: `update-tracking-options options[{trackingOptionId, name}]`; ask first (it changes every past
  report label).
- Retire: `update-tracking-options options[{trackingOptionId, status: ARCHIVED}]` or
  `update-tracking-category status=ARCHIVED` for the entire category. Confirm nothing recurring (repeating invoices,
  bank rules) still uses it; Xero rejects or silently fails a document that references an archived option.
- Restructure (e.g. split "Location" into two): create new options, re-tag by editing the draft documents; for
  posted history use a documented reporting mapping, not mass edits.

## Pitfalls

- 2-category limit reached: cannot create more; the fix is a combined option naming scheme or archiving.
- Bank rules and repeating invoices may carry tracking; archiving breaks them.
- Tracking on draft vs approved: editing approved documents is limited; plan changes for drafts.
- Do not encode non-reporting facts in tracking (e.g. approval state); use references or history notes.
- More than 10 options per call is rejected; batch.

## Output format

```
Org | categories (active x/2) | options per category
Design/audit table: category | option | status | usage lines | issue | action
Proposed changes (none executed) -> after confirmation: IDs created/updated
```
