---
name: linnworks-inventory-vs-ledger
description: >-
  Reconcile Linnworks stock valuation to the general-ledger inventory account and explain the difference: owned versus
  mirrored (FBA/fulfilment) locations, negative stock, stock takes and counts, purchase deliveries not billed, scrapped
  returns, transfers in transit, composites. Use for "does Linnworks stock value match the balance sheet", "inventory
  variance at month end", "stock take adjustments to book", "negative stock", "goods received not invoiced". Tools:
  getStockValuation, getStockLevels, getStockTakes, getStockCounts, getStockCountLines, getTransfers,
  getPurchaseDeliveries, getStockAudit.
metadata:
  department: "accounting"
  domain: "ecommerce-reconciliation"
  platform: "linnworks"
  owner: "satva-coe"
  status: "beta"
  license: "Satva-original"
  source: "original"
---

# Linnworks inventory versus ledger

Prerequisite: `linnworks-mcp-operating-rules` (never sum across locations; per-page figures are not totals).
Counterparts: `linnworks-to-ledger-posting-rules` (how COGS and inventory should post) and
`ecommerce-multichannel-month-end` (where this sits in the close).

## Step 1: establish the Linnworks number properly

1. `getLocations`: list every location with `kind`, `owned`, deleted flag. Decide with the client which are inventory
   the entity owns and carries on its books. Typical: default/physical warehouses = yes; FBA/fulfilment-centre =
   owned-but-mirrored (see below); not_trackable and deleted = no.
2. `getStockValuation(location_id=.., owned_only=true)`, page via `nextPageToken` until `hasMore` is false. Each row:
   `sku`, `quantity`, `current_stock_value` (from `StockLevel.CurrentStockValue`), `purchase_price`.
   **Compute the total yourself by summing rows across all pages**; `owned_page_value` is page-local. Record row count.
3. Run it twice if the date matters: the tool is *current* valuation, not as-at a past date. For a historic close,
   reconstruct from `StockChange` movements (`getStockHistory` per SKU, `StockValue` after each change) or take the
   valuation on the close date; never run it a week later and call it month-end.
4. Items with `current_stock_value` null or zero and `quantity > 0`: missing cost. List them; they understate stock.
5. Negative `quantity` rows: stock sold below zero. List them; valuation is meaningless until corrected.

## Step 2: get the ledger number

From the accounting system, take the inventory control account balance at the same date, plus any related
asset accounts (goods in transit, FBA inventory, prepaid/in-bound). Take its subledger/cost layer detail if the
ledger tracks it.

## Step 3: reconcile

Start: Linnworks owned valuation. Adjust to ledger:

| Reconciling item | Where to find it | Direction |
|---|---|---|
| Mirrored FBA/fulfilment stock carried in ledger but excluded by `owned_only` | `getStockValuation(owned_only=false, location_id=<fba>)` | Add (if owned and booked) |
| Purchase deliveries received in Linnworks, supplier bill not yet booked (GRNI) | `getPurchaseDeliveries`, `getPurchaseOrders`, `getPurchaseOrderItems(outstanding_only=false)`, `getIncomingStock` | Linnworks higher than ledger |
| Bills booked, goods not yet received (in transit) | `getIncomingStock(due_before=..)` | Ledger higher |
| Transfers between locations in transit | `getTransfers(status=..)`, `getTransferItems` | Check both legs |
| Stock take or count variances posted in Linnworks, not in ledger | `getStockTakes(location_id, stock_take_from/to)`, `getStockTakeLines`, `getStockCounts`, `getStockCountLines` (`WasQty`, `WasValue`, `ValueNow`) | Linnworks lower/higher by net variance |
| Scrapped returns written off in Linnworks, not expensed | `getReturns(scrapped=true)` | Linnworks lower |
| Returns restocked but ledger not credited back | `getReturns(scrapped=false)` | Linnworks higher |
| Manual stock adjustments | `getStockAudit(audit_from/to, audit_type)` | Either |
| Costing method difference (Linnworks average vs ledger FIFO/standard) | Compare unit cost on a sample | Residual |
| Purchase price differences, landed cost not in Linnworks | Purchase bills vs `purchase_price` | Ledger higher |
| Composite/bundle parents holding value as well as children | `getStockComposition` | Double count in Linnworks |

Compute unexplained = ledger - (Linnworks + explained items). Tolerance is a client decision; anything above it gets
an owner and a date. Do not plug the difference into COGS.

## Step 4: stock-take accounting

- A stock take (`getStockTakes`, one per location and date) with lines in `getStockTakeLines` changes quantities
  and values in Linnworks. The ledger must record the variance: Dr/Cr Inventory, Cr/Dr Stock adjustment (COGS or
  inventory shrinkage by policy). Confirm it is posted once and in the period of the count.
- `getStockCounts` shows `Locked` registers and total variance; a count not yet locked is still provisional.
- Large positive variances usually mean receipts not booked or a unit-of-measure error, not found stock.

## Step 5: ageing and provision (optional but valuable)

- Dead stock: `getStockHistory(skus)` gives `out_of_stock_since`; the opposite signal (no sales for N days with
  positive quantity) comes from `getTopSkus` over a long window versus `getStockLevels`.
- Propose a provision only with an approved rule (age bands, net realisable value). Never book it from this skill.

## Traps

- **Valuation is current, not historic.** The most common false variance is a late pull.
- **FBA double count.** Adding FBA and warehouse quantities for the same SKU counts channel mirror and physical.
- **`StockLevel.CurrentStockValue` is only as good as purchase cost data.** Missing `PurchasePrice` yields zero value.
- **Archived items** still hold value if quantity > 0; the tool excludes them unless `include_archived=true`.
- **Multi-currency purchasing:** `Purchase.Currency` and `ConversionRate` exist; cost in Linnworks may be in the
  base currency at a stale rate.

## Output

A one-page reconciliation: Linnworks owned valuation (with row count and location list), each reconciling item with
source and amount, unexplained remainder, lists of negative-stock and zero-cost SKUs, stock-take variances to post,
and recommended journals as proposals only (the server cannot post anything).
