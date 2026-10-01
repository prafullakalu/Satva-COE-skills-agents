---
name: linnworks-mcp-operating-rules
description: >-
  Operating rules for the Satva read-only Linnworks MCP server (96 tools): what it can and cannot do, paging with
  page_token/nextPageToken, the per-tenant rate limit, how to tell a throttle from an empty result, per-currency and
  per-location totals, and which accounting facts Linnworks does NOT hold. Load this first whenever a task will call
  Linnworks tools such as searchOrders, getProcessedOrders, getRevenueSummary, getStockValuation, getPayments or
  getOrderRefunds. Trigger on "pull Linnworks data", "why did the Linnworks call return nothing", "Linnworks rate
  limit", "can the MCP write to Linnworks", "page through Linnworks orders".
metadata:
  department: "accounting"
  domain: "ecommerce-operations"
  platform: "linnworks"
  owner: "satva-coe"
  status: "stable"
  license: "Satva-original"
  source: "original"
---

# Linnworks MCP: operating rules

Behaviour below was checked against the server source (`linnworks_ro`), not the vendor docs. Other Linnworks skills in
this library assume you have read this one.

## 1. What the server is

- **Read-only, 96 tools.** No tool writes, cancels, refunds, re-prices or re-locates anything. Under the tools there is
  no free-text SQL for the model: tools take typed parameters, the server builds one `SELECT`, and a fail-closed
  validator rejects anything that is not a single SELECT/WITH over an allowlisted table (about 134 business tables;
  `users`, `user`, `user_group` are permanently blocked). Every top-level SELECT is capped at 1000 rows.
- Consequence: you can never "fix" Linnworks from here. Anything that needs a change is a recommendation to a human.
- Free-text columns (order notes, audit text, extended-property values) can hold customer data typed by staff or
  copied from a marketplace. Do not quote them into deliverables.
- Email search is deliberately unavailable (`searchOrders` searches name prefix, postcode prefix, SKU, references).

## 2. What Linnworks does NOT hold (verified against the table registry)

No column in the allowlisted schema is named fee, commission, settlement, payout or VAT-return. Specifically:

- **Marketplace fees, FBA fees, PSP fees, reserves, chargebacks, advertising: absent.** The only fee-like field is
  `Accounting_Payment.BankCharges` (and `RefundBankCharges`), read via `getPayments`; treat it as present only after you
  confirm it is populated for that tenant.
- **Settlement or bank-deposit totals: absent.** They live in the channel settlement report or PSP payout.
- **VAT/tax-return boxes: absent.** Per-order `fTax` and per-line `SalesTax`/`TaxRate` exist; jurisdiction and OSS
  treatment do not.
- **Landed cost and COGS journals: absent.** `OrderItem.DispatchStockUnitCost`, `StockLevel.CurrentStockValue` and
  `StockChange.ChangeValue` are operational valuations, not ledger entries.

Say so in the report. A gap you did not name becomes a silent mismatch later.

## 3. Pagination

- Typed list tools use **keyset paging**: pass the returned `nextPageToken` back as `page_token`, with the *same*
  filters. A token is bound to the exact query; changing any filter or `limit` starts a new search.
- `limit` defaults to 100, max 1000. Exceptions: `searchStockItems` max 200 and is page-number based;
  `getStockHistory` takes 1 to 10 SKUs per call and `max_movements` per SKU.
- Loop until `hasMore` is false and `complete` is true. Record page count and row count in your working notes.
- Per-page figures (`overdue_count`, `buckets_on_page`, `owned_page_value`) are page-local. Never present them as a
  total. If a total is required, page to the end and sum the rows yourself, or use an SQL-aggregated tool.

## 4. Throttle is not "no data"

Every failure comes back structured. Handle each:

| `error` | Meaning | Action |
|---|---|---|
| `rate_limited` (`complete:false`, `rate_limited.retry_after_seconds`) | Per-tenant token bucket (default 120 calls/min, shared fairly between callers) or upstream quota | Wait `retry_after_seconds`, repeat the SAME call. Never record the missing page as zero rows |
| `sql_unavailable` | This tenant has no Custom SQL | Stop; most typed tools depend on it. Escalate |
| `invalid_request` | Bad parameter, ambiguous location name (candidates are listed) | Fix the parameter; re-call with the GUID |
| `upstream_error` | Linnworks API failed | Retry once, then report |
| `not_configured` | Server has no client for this caller | Reconnect the MCP in Obot |

`getStockHistory` returns throttled SKUs in `rate_limited`, never in `unresolved`. Any response with
`complete:false` is a partial answer: say so on the deliverable.

## 4a. Batching to stay inside the bucket

120 calls a minute sounds generous until you fan out per order. Prefer one aggregated call to a thousand detail calls:

- Period totals by channel: `getChannelBreakdown` (SQL GROUP BY), not paging every order.
- Lines for many orders: `dumpJoined` (Order + OrderItem) over a date window, rather than `getOrderItems` per order.
- Use `getOrderBundle` only when one order needs header, lines, tax and returns together.
- Do a cheap `countTable` first when you need to know whether a window is 300 rows or 300,000.

## 5. Money and quantity rules the server enforces (and you must keep)

- **One row per currency.** `getRevenueSummary`, `getChannelBreakdown`, `getTopSkus` return per-currency rows. Never
  add across currencies. Convert only with a rate you state (`Order.ConversionRate` exists per order).
- **Never sum stock across locations.** FBA and fulfilment-centre locations mirror availability, so summing
  double counts. Call `getLocations` first (location `kind`: default, physical, fulfilment_centre, fba; `owned`
  flag; FBA is inferred from name/tag because the schema has no FBA flag).
- **Location names are not unique.** Pass the GUID (`location_id`) once known.
- **Dates:** `dReceievedDate` (note the vendor spelling) is order received; `dProcessedOn` is dispatch;
  payment date is `dPaidOn` in `getOrderAdditionalInfo`, not on the order. `getProcessedOrders` accepts
  `date_field` of `received` or `processed` only.
- Order `status_code`: 0 unpaid, 1 paid, 2 return, 3 pending, 4 resend.

## 6. Pre-flight for any analysis

1. Confirm both the Linnworks MCP and the comparison source (ledger or export) are reachable; stop if not.
2. `getLocations`, `getPaymentTypes`, `getBankMappings`: learn how this tenant models locations and channel-to-bank.
3. State the period, the date field and the time zone before pulling anything.
4. Pull, page to completion, tally rows, then analyse. Quote counts with every figure.

## Do not

- Do not infer fees, VAT or COGS from order totals.
- Do not treat an empty page after a throttle as "none".
- Do not widen a query to dodge a validator rejection; the rejection is the design.
- Do not paste credentials, tenant IDs or customer details into outputs.
