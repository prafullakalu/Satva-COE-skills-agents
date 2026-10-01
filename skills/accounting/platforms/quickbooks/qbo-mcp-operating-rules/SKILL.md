---
name: qbo-mcp-operating-rules
description: >-
  Rules for using the Satva QuickBooks Online MCP server safely: how to pick the company, which tool to call (generic *_entity tools vs legacy per-entity tools vs workflow tools), read-before-write, dry runs, SyncToken and sparse-update behaviour, void vs delete, batch limits, and how to read QBO fault codes. Use before ANY QuickBooks write, and when the user says "update this invoice in QBO", "delete that bill", "why did QuickBooks reject this", "stale object", "which QuickBooks tool should I use", or "is it safe to run this on the live company".
metadata:
  department: "accounting"
  domain: "mcp-operations"
  platform: "quickbooks"
  owner: "satva-coe"
  status: "stable"
  license: "Satva-original"
  source: "original"
---

# QuickBooks MCP operating rules

Applies to every `qbo-*` skill. These rules come from the server source (Satva `quickbooks-online-mcp-server`), not from general API folklore. Tool names are exact. If a tool you need is missing from the tool list, the deployment is on the `core` profile or `QBO_READ_ONLY=true`: say so, do not improvise another route.

## 1. Pick the company first
1. Call `list_companies` (or `list_companies_summary` to also check token health). Each row has realm id, name, `sandbox` or `production`, and which one is the default.
2. Every tool accepts an optional `company` (name or realm id). Pass it on EVERY call when more than one company is connected. `set_active_company` only changes the default for later calls; prefer explicit `company`.
3. State the company and environment in your reply before any write. Writes to `production` need explicit user approval for that specific change.
4. Call `get_company_overview` once per session: it reports multicurrency, class tracking, location (department) tracking, inventory, sales tax, report basis and which entities will be rejected. Many "validation" errors are just a feature switched off.

## 2. Choose the tool (cheapest and safest first)
| Need | Use | Notes |
|---|---|---|
| Any lookup or filter | `query_quickbooks` | Single `SELECT`, read-only, max 1000 rows per page. |
| Known report | `get_profit_and_loss`, `get_balance_sheet`, ... or `run_report` | Never rebuild a report from invoices and bills. |
| Worklists and analysis | `ar_collections_worklist`, `ap_due_bills_worklist`, `cash_position`, `customer_360`, `vendor_360`, `find_duplicates`, `uncategorized_transactions`, `period_comparison` | All read-only. |
| Learn an entity's rules | `describe_entity` | Required fields, example body, update mode (sparse or full), delete mode (hard or deactivate). |
| Read, create, update, delete any entity | `get_entity`, `create_entity`, `update_entity`, `delete_entity` | Preferred write path. |
| Purpose-built writes | `apply_payment_to_invoices`, `convert_estimate_to_invoice` (both have `dryRun`), `void_invoice`, `void_payment`, `void_sales_receipt`, `send_invoice`, `upload_attachment` | |
| Many small writes | `batch_operations` | Max 10 items, independent, no ordering. |
| Changes since a time | `get_changes` | Change Data Capture, last 30 days, max 1000 objects. |

Legacy per-entity tools (`create_invoice`, `update_purchase`, `search_bills`, ...) still exist unless the deployment uses the `core` profile, where only `search_*` legacy tools remain. Note the odd spellings: bills and vendors use hyphens (`create-bill`, `get-bill`, `update-bill`, `delete-bill`, `create-vendor`, `get-vendor`, `update-vendor`, `delete-vendor`); everything else uses underscores. The legacy `search_*` tools each take a slightly different criteria shape (objects, arrays or an advanced `filters` form), so prefer `query_quickbooks` for lookups. Prefer the generic `*_entity` tools; they fetch the SyncToken for you and share one validated path.

## 3. Read before write (always)
1. Read the current object (`get_entity`, or `query_quickbooks` for sets) and show the user the before state.
2. Draft the exact change as a field-level diff: `Invoice 1042: DueDate 2026-07-01 -> 2026-07-15`.
3. Get a clear yes. "Looks good" about a plan is a yes; silence is not.
4. Write once. Never loop a write tool "to be sure".
5. Read it back and report ids plus the `qboLink` the tool returns. Report any difference from what was approved.

Where a `dryRun` flag exists (`apply_payment_to_invoices`, `convert_estimate_to_invoice`), run it first and show the returned body.

## 4. How updates really work
- `update_entity` reads the current object, then POSTs. For entities where Intuit documents sparse updates (Customer, Invoice, Estimate, Payment, BillPayment, Deposit, JournalEntry, SalesReceipt, RefundReceipt, Transfer, CompanyInfo, CreditCardPayment) it sends only your `patch` plus `Id`, `SyncToken`, `sparse: true`. For the rest (Account, Bill, Vendor, Purchase, VendorCredit, CreditMemo, Item, Class, Department, Term, ...) it deep-merges your patch over the full object and sends all of it: a full update clears any field omitted from the body, which the merge prevents.
- Arrays are replaced wholesale. Patching `Line` replaces EVERY line, so send the complete intended `Line` array (read the current lines first). This is the most common way to silently delete invoice lines.
- Lines from a read carry computed rows (`SubTotalLineDetail`); drop them before sending lines back.
- `create_entity` refuses bodies containing `Id`, `SyncToken` or `sparse` (QBO would treat them as an update). Use `update_entity`.
- Legacy `update_purchase` and `update_journal_entry` (and likely other legacy updates that take a whole object) pass your object straight to QBO and do NOT fetch a SyncToken: you must supply the current `Id` and `SyncToken` yourself. `update_invoice` is the exception (it reads the invoice and sends a sparse update).

## 5. SyncToken and stale objects
Every QBO object has a `SyncToken` that increments on each save. A write with an old token fails with fault code 5010 (Stale Object Error). Fix: re-read, re-apply the same intended change on the fresh object, re-confirm if the fresh object differs materially (someone else edited it), write again. Do not retry blindly with a guessed token.

## 6. Delete, deactivate, void
- `delete_entity` hard-deletes transactions (Invoice, Bill, Payment, JournalEntry, Deposit, ...). It deactivates list entities (Customer, Vendor, Item, Class, Department, Term, PaymentMethod, Employee) by setting `Active=false`. `Account` can only be deactivated.
- Prefer `void_invoice`, `void_payment` or `void_sales_receipt` over delete for anything that was sent, paid or reported: the document stays in the books with zeroed amounts and a `Voided` note. Voiding is not reversible.
- Hard delete leaves only an audit-log entry. Never delete to "undo" something that has been reconciled, filed in a tax return or emailed to a customer. Reverse it with a credit memo, vendor credit, or reversing journal entry instead.
- There is no undo tool. The only undo is a compensating transaction, so say that before the write.

## 7. Idempotency
The server sends no request id and does not de-duplicate. A timed-out write may still have succeeded. Before retrying any create: query for it by `DocNumber`, customer/vendor plus amount plus date, or `get_changes` with a `changedSince` just before the attempt. Only create again if it is absent. QBO rejects a duplicate Bill `DocNumber` unless `include=allowduplicatedocnum`, but invoices and journal entries are not protected.

## 8. Rate and size limits
- `query_quickbooks`: one entity, filters combine with AND only (no OR, no JOIN, no GROUP BY), `LIKE` supports only `%`. Page with `STARTPOSITION n MAXRESULTS m`; quote strings with single quotes and escape a literal quote as `\'`.
- Workflow tools read at most 1000 rows and set a `truncated` flag. If `truncated` is true, say totals are partial and narrow the window.
- The server does not retry. An HTTP 429 (throttled) means wait and reduce the number of calls; prefer one workflow tool over many `get_entity` calls.
- Reports return amounts as strings; the tools flatten the tree and also return raw JSON. Do not add up floats: work in cents.

## 9. Reading errors
Errors arrive as `Error: QuickBooks <type> (HTTP n): [code] Message - Detail (field: X)`. Common cases:
| Signal | Meaning | Action |
|---|---|---|
| 5010 | Stale object (SyncToken) | Re-read, re-apply, retry once. |
| 6240 | Reference is inactive or not found | Reactivate it (`update_entity` `Active:true`) with approval, or choose another. |
| Duplicate document number | DocNumber already used | Use the next number; do not force the duplicate flag unless the user wants it. |
| Validation errors naming Class, Department, Currency, Tax, Inventory | Feature switched off or plan lacks it | Check `get_company_overview`. |
| Period closed / closing date | Transaction date is before the books' closing date | Do not backdate around it. Ask the controller. |
| 401 / token errors | Connection expired | Run `list_companies_summary`; the user reconnects in the dashboard. |
| HTTP 403 | The connected QBO user's role cannot do this | Report it; do not retry. |
Quote the code and message to the user. Never retry a validation error with the same body.

## 10. Never
- Never write on a guess: if an id, account or tax code is ambiguous, ask.
- Never run a write against `production` that you have not shown as a diff and had approved.
- Never use `send_invoice` without confirming the address already on the invoice (`BillEmail`); the tool cannot change it and always emails that address.
- Never paste tokens, realm secrets or API keys into replies.
- Never describe a number you did not read from a tool result.
