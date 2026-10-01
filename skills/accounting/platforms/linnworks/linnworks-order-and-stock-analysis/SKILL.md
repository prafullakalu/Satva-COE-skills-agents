---
name: linnworks-order-and-stock-analysis
description: >-
  Analyse Linnworks orders, channel sales, open-order backlog, stock levels, stock movements and top SKUs with the
  read-only Linnworks MCP, and produce figures an accountant can trust (per currency, per location, with counts and
  completeness). Use for "sales by channel for March", "which orders are overdue", "what is stock at the main
  warehouse", "when did this SKU go out of stock", "top sellers", "revenue by supplier", "check the order totals
  against the invoice". Names the real tools: getChannelBreakdown, getRevenueSummary, searchOrders, getOrderBundle,
  getStockLevels, getStockHistory, getTopSkus.
metadata:
  department: "accounting"
  domain: "ecommerce-analysis"
  platform: "linnworks"
  owner: "satva-coe"
  status: "beta"
  license: "Satva-original"
  source: "original"
---

# Linnworks order and stock analysis

Read `linnworks-mcp-operating-rules` first (paging, throttles, per-currency and per-location rules). This skill is the
analysis playbook on top of it. Tool behaviour is verified against the server code; the workflow has not been run
against a live ledger, hence `beta`.

## Choose the right tool for the question

| Question | Tool | Why |
|---|---|---|
| Sales and tax by channel and store | `getChannelBreakdown(from_date,to_date,date_field)` | SQL-aggregated by Source, SubSource, currency: orders, revenue, subtotal, tax, postage, discount |
| Period total, any channel | `getRevenueSummary` | Same aggregation without channel split; one row per currency |
| Best sellers | `getTopSkus(rank_by="revenue" or "units")` | Revenue is tax-inclusive, `revenue_ex_tax` also returned |
| Sales by supplier | `getSalesBySupplier` | Null supplier = lines with no default supplier, shown not dropped |
| One order, everything | `getOrderBundle(order_id, include_returns=true)` | Header, lines, tax, composites, returns |
| Find orders | `searchOrders` (filters: received_from/to, processed, status, source, sub_source, reference, sku, location) | Keyset paged, newest first |
| Dispatched in a window | `getProcessedOrders(from_date,to_date,date_field)` | `received` or `processed` |
| Backlog | `getOpenOrders`, `getAgingOpenOrders` | Per location, never summed across locations |
| Stock now | `getStockLevels(skus or location)` | Per item per location, deliberately no total |
| One item's owned total | `getStockItem(sku)` | `owned_total` excludes FBA, fulfilment, untracked, deleted |
| Why stock moved or hit zero | `getStockHistory(skus<=10)` | Movements with `change_source`, `out_of_stock_since` |
| Stock value | `getStockValuation` | See `linnworks-inventory-vs-ledger` |

## Workflow: period sales analysis

1. **Fix the basis.** Pick `date_field`: `received` (order date; right for sales recognised on order) or `processed`
   (dispatch date; right when revenue follows shipment). Write the choice on the output. Mixing bases is the most
   common reason Linnworks and the ledger disagree by "a few orders".
2. **Aggregate first.** `getChannelBreakdown` for the period. Keep rows separate per currency. Note each row's
   `orders`, `revenue`, `subtotal`, `tax`, `postage`, `discount`.
3. **Prove the aggregate.** Establish how this tenant composes the total (try `revenue = subtotal + postage + tax -
   discount` on five orders via `getOrderBundle`; whether `Subtotal` is pre- or post-discount varies by channel
   import, so confirm before relying on it). Then test the identity per row within rounding. A row that breaks it has
   tax-inclusive/exclusive inconsistency or manual adjustments; list a sample with `searchOrders`.
4. **Exclude what should not count.** Status `2` (return) and cancelled/`HoldOrCancel` orders, unpaid status `0` if
   sales are recognised on payment, and test or zero-value orders. Use `searchOrdersFull` when you need columns such
   as `postage_ex_tax`, `postage_discount`, `HoldOrCancel`, `ConversionRate`, `fkBankId`.
5. **Sample drill-down.** For the three largest and three smallest orders per channel, `getOrderBundle`, and confirm
   line sum equals header and tax equals line `sales_tax` sum.
6. **Report** with channel, currency, orders, revenue, tax, postage, discount, refunds (from
   `linnworks-channel-fees-and-refunds`), and a completeness line (pages pulled, any `rate_limited`).

## Workflow: stock analysis

1. `getLocations`; classify each as owned or mirrored (fba/fulfilment_centre). Only owned locations are real stock.
2. `getStockLevels(location_id=..)` paged; compute `available = quantity - in_orders` (the tool returns it) and
   flag `below_minimum`.
3. For anomalies (negative quantity, sudden zero), `getStockHistory(skus=[..])`. Read `out_of_stock_since` as the
   *transition* to zero, not the newest zero row; if `out_of_stock_since_is_lower_bound` is true the real date is
   older, page back with `before=oldest_movement`.
4. Composite products: `getStockComposition(sku)` shows parent/child. `getOrderItems` marks child lines with
   `composite_parent_row_id`; counting both parent and child lines double counts units.
5. Inbound: `getIncomingStock(due_before=..)` for purchase orders not yet received; `include_pending` default false.

## Traps (each has cost real money)

- **Cross-location totals.** Never add `quantity` across locations. Use `getStockItem.owned_total`.
- **Cross-currency totals.** Never add GBP and USD rows; convert with a stated rate.
- **Page-local figures.** `overdue_count` and `owned_page_value` cover one page only.
- **Archived items are invisible** to `searchStockItems`; "not found" may mean archived (`listArchivedItems`).
- **Services and postage lines.** `is_service` lines are not stock; exclude from unit counts, include in revenue.
- **Order status 4 (resend)** can duplicate a shipment without new revenue.
- **Partial shipment.** `part_shipped_qty` on lines: a processed order may not be fully shipped.
- **Throttled run.** Never publish a table where a page returned `complete:false`.

## Output format

Provide: (1) headline numbers per currency and channel with order counts, (2) the basis statement (date field, period,
time zone, locations), (3) exceptions list with order numbers and reason, (4) completeness line, (5) what was not
checkable from Linnworks (fees, VAT return, ledger postings) and which skill picks it up next.
