---
name: xero-mcp-operating-rules
description: >-
  Safe read/write rules for the Satva Xero MCP server: choosing the organisation, reading before writing,
  pagination, rate limits (60/min, 5000/day per org), scope-gated tools, status limits (drafts only), irreversible
  actions and how to interpret Xero errors. Use before any Xero MCP work, when the user says "use Xero", "post this
  to Xero", "which org", "why did the Xero tool fail", "rate limit", "401", "403", or when another xero-* skill
  needs the ground rules.
metadata:
  department: "accounting"
  domain: "platform-operations"
  platform: "xero"
  owner: "satva-coe"
  status: "stable"
  license: "Satva-original"
  source: "original"
---

# Xero MCP operating rules

These rules apply to every `xero-*` skill. Tool names below are the names registered by the Satva Xero MCP server
(`xero-mcp-server`). If a tool is not in your tool list, say so; do not improvise another route.

## 1. Pick the organisation first (tenant selection)

Every tool accepts an optional `organisation` argument (name or tenant id). If omitted, the server uses the dashboard
default ("Active") org.

1. Call `list-companies` (names, tenant ids, which is Default).
2. If more than one org is linked, never rely on the default for a write. Pass `organisation=<Name>` on every call and
   state the org name in your first line of output.
3. Confirm the target with `list-organisation-details organisation=<Name>` (legal name, base currency, country,
   period lock date). Mismatched base currency or country is the usual sign of the wrong org.
4. `set-active-company(realmId)` only changes the dashboard default. It is a convenience, not a guard; explicit
   `organisation=` is safer.
5. `list-orgs-summary` shows token health and invoice/bill counts for all orgs; `diagnose-connection` tests the
   connection. Use them when a tool errors, before telling the user to reconnect.

## 2. Read first, then draft, then confirm, then write

1. Read the current state (list/get tools) for exactly the records you will touch. Quote the IDs.
2. Show the user the proposed payload in plain terms: org, contact, date, accounts, tax types, amounts, status.
3. Wait for an explicit yes. A request like "fix the bills" is not approval of a specific payload.
4. Execute the smallest write. Re-read the record and report the result with the deep link the tool returns.
5. Batches: write one record, verify it, then continue. Never fire 40 creates blind.

## 3. What the write tools really do (verified in the server source)

| Tool | Resulting state / limit |
|---|---|
| `create-invoice` | Always DRAFT. No status parameter, no currency parameter. `type` ACCREC (sales) or ACCPAY (bill). |
| `update-invoice` | Only DRAFT invoices. All `lineItems` must be re-sent; omitted lines are removed. No status parameter. |
| `create-credit-note` | Always DRAFT. `void-credit-note` handles VOIDED/DELETED. |
| `create-bank-transaction` | RECEIVE/SPEND, created AUTHORISED (posted), not a draft. |
| `create-manual-journal` | DRAFT by default; `status: POSTED` posts it. `update-manual-journal` only on drafts. |
| `create-purchase-order` / `update-purchase-order` | DRAFT default; status can move DRAFT, SUBMITTED, AUTHORISED, DELETED. |
| `create-payment` | Only against AUTHORISED, not fully paid invoices; amount must not exceed amount due. |
| `void-invoice`, `void-credit-note` | Irreversible. VOIDED only from AUTHORISED; DELETED only from DRAFT/SUBMITTED. |
| `delete-payment`, `delete-batch-payment` | Irreversible; reopens the invoice balance. |
| `add-history-note` | Permanent audit note; cannot be edited or deleted. |
| `email-invoice` | Sends Xero's standard email to the contact. Only AUTHORISED invoices. Cannot be recalled. |

Consequence: this MCP cannot approve (authorise) a draft invoice or credit note. Tell the user to approve in Xero, or
ask for explicit direction before using another path. Do not claim an invoice is "posted" after `create-invoice`.

Irreversible or externally visible actions (`void-*`, `delete-*`, `email-invoice`, `add-history-note`,
`create-batch-payment`, `create-payment`) need a named confirmation naming the record, not a general approval.

## 4. Pagination

- `list-invoices`: `page` is required, `pageSize` 1-100 (default 100). The response states `hasMore`; keep the same
  filters and increment `page`. It has no status or date filter: filter the results yourself.
- `list-contacts`: 100 per page; use `searchTerm` instead of paging when you know the name.
- `list-bank-transactions`, `list-credit-notes`, `list-quotes`, `list-items`, `list-payments`, `list-overpayments`,
  `list-prepayments`, `list-manual-journals`, `list-purchase-orders`: page-based; page until a short page returns.
  Do not trust the page size quoted in a tool description; count the rows you get.
- `list-journals` pages by `offset` = highest JournalNumber seen, 100 per call.
- `list-accounts`, `list-tax-rates`, `list-currencies`, `list-tracking-categories` return everything in one call.
- State the total you retrieved vs what the tool said exists. Never report a total from page 1 alone.

## 5. Rate limits

Xero allows 60 calls/minute and 5000 calls/day per organisation. The server paces itself to 55/min per org
(`XERO_MAX_CALLS_PER_MINUTE`) and retries a 429 up to twice, honouring `retry-after` up to 65 s. If it still fails
you get "Xero rate limit reached (minute|daily limit), retry in Ns".

- minute limit: wait the stated seconds, then resume; do not loop.
- daily limit: stop; tell the user the remaining work resumes after the 24 h window.
- Prefer one wide read over many narrow ones (`list-invoices` once, not per invoice). Use `invoiceNumbers` only when
  you need line items.
- A loop of "list rows, then act on each" over hundreds of rows is a plan that must be sized first: rows x calls each.

## 6. Reading errors

| Message | Meaning | Action |
|---|---|---|
| "Authentication failed" (401) | Expired credentials OR a scope the connection was never granted | Run `diagnose-connection`. If the tool is scope-gated (below), the tool output says so; reconnecting is the only fix, refreshing cannot widen scopes |
| "You don't have permission" (403) | User role in Xero cannot do this | Report; do not retry |
| "not found" (404) | Wrong ID, wrong org, or record deleted | Re-check `organisation=` first |
| "rate limit reached" | Section 5 | Wait/stop |
| Validation text (e.g. account code, tax type, locked period) | Xero rejected the payload; message is passed through | Fix the payload; do not retry unchanged |

Scope-gated tools: `list-journals` (needs the Journals scope, which Xero only grants to certified Advanced-tier apps),
`list-attachments`/`get-attachment`/`upload-attachment`, `list-report-bank-summary`,
`list-report-executive-summary`. `list-published-reports`, `get-report-by-id`, `list-report-budget-summary` and
`list-report-1099` cannot work on connections created on or after 2 March 2026: use the specific report tools.
Payroll tools (`list-payroll-*`, timesheets) need an NZ or UK org. Projects and Assets tools need those optional scopes.

## 7. Never

- Never write to an org you have not named in the conversation.
- Never retry a validation error unchanged, or a 401/403 in a loop.
- Never put tokens, secrets or client data in notes, history notes or attachments.
- Never state a number that no tool returned. If a tool failed, say it failed.
- Never use `add-history-note` for working notes; it is permanent.

## Output format

Open with `Org: <name> (<base currency>) | as at <date> | read-only|write`. Then findings, then (for writes) the exact
payload shown before execution and the returned ID/link after.
