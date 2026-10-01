---
name: shopify-inventory-vs-ledger
description: >-
  Value Shopify inventory (on-hand quantity by location times cost) and reconcile it to the general-ledger inventory
  account with the read-only Shopify MCP: on-hand versus available versus committed, incoming and damaged stock,
  untracked and zero-cost variants, multi-location, bundles, and what Shopify cannot say about cost. Use for "Shopify
  stock value for the balance sheet", "inventory does not match the ledger", "on hand vs available", "which variants
  have no cost", "stock by location". Tools: get-products, get-inventory-items, get-inventory-levels, get-locations,
  get-product-variants-detailed.
metadata:
  department: "accounting"
  domain: "ecommerce-reconciliation"
  platform: "shopify"
  owner: "satva-coe"
  status: "beta"
  license: "Satva-original"
  source: "original"
---

# Shopify inventory versus ledger

Prerequisite: `shopify-mcp-operating-rules`. Counterpart for Linnworks clients: `linnworks-inventory-vs-ledger`. If
Shopify is a sales channel in front of Linnworks, Linnworks is the stock master and this skill checks the channel's
copy, not the books (see "Whose number is the number" below).

## Whose number is the number

1. Shopify is the stock master (no inventory system): Shopify on-hand valued at cost is the subledger.
2. Linnworks or another IMS is the master: Shopify quantities are a synced copy. Reconcile the ledger to the master;
   use Shopify only to check sync health (differences per SKU).
Decide with the client first, and state it in the output.

## The data and its limits

- Quantities: `get-inventory-levels(inventoryItemId)` returns per location: `available`, `on_hand`, `committed`,
  `reserved`, `incoming`, `damaged`, `quality_control`, `safety_stock`, plus `updatedAt`. Only the first 50 locations.
- Cost: `get-inventory-items(productId)` and `get-product-variants-detailed` give `inventoryItem.unitCost`
  (amount, currency), `tracked`, `sku`, `requiresShipping`, country of origin. **`unitCost` is a merchant-typed
  field.** It is not FIFO or average cost and may be blank or stale.
- Quick view: `get-products` returns `totalInventory` and `inventoryQuantity` for only the first 5 variants of each
  product, not per location. Good for triage, not for valuation.
- Locations: `get-locations` (active flag, names); a location may be a 3PL or a retail store, not your warehouse.
- Discovery: `get-products(query="status:active", limit, after)` pages products; variants (cap 100 per product in
  `get-inventory-items` and `get-product-variants-detailed(productId, first<=100)`) lead to inventory item ids. This is a per-product, per-item call pattern, so a catalogue of
  2,000 variants costs thousands of calls at 30 per minute. Plan the pull, or ask the client for a Shopify inventory
  export for large catalogues and use the MCP to spot-check.

## Workflow

1. `list-stores`, then `get-locations`: classify locations as owned stock, consigned/3PL (owned by you, held by
   others), or not yours. Record the classification.
2. Enumerate variants: `get-products` pages (note `status`, ignore archived/draft if the client agrees), then
   `get-inventory-items(productId)` for cost and tracked flag.
3. For tracked variants, `get-inventory-levels(inventoryItemId)`. Value = `on_hand` x cost per location.
   Use **on_hand** for the balance sheet (the stock you own), not `available` (on_hand minus committed and reserved).
   Add `damaged` and `quality_control` separately: owned but possibly impaired.
4. Exclusions: untracked variants (`tracked=false`: services, digital, made-to-order), gift cards (no stock),
   `incoming` (not yet owned until received; ledger may carry it as in-transit).
5. Cost exceptions list: variants with quantity > 0 and cost missing or zero; cost above selling price; negative
   `on_hand`.
6. Tie to the ledger: Shopify valuation vs inventory control account at the same instant. Remember Shopify gives
   *current* quantities, so run it at close date or accept the difference and document it; for a historic date, roll
   back using sales and receipts, which needs `get-orders` and purchase data and is approximate.
7. Reconciling items: stock in transit and incoming, GRNI, returns restocked but not credited back, no-restock refunds
   (goods not back), shrinkage adjustments done in Shopify without a journal, cost differences, bundle/composite
   products that hold stock on components, and 3PL stock not in Shopify.

## Checks that catch real errors

- Sum of `committed` is stock sold but unshipped; it is still owned inventory until dispatch, so it stays in on_hand.
- `available` negative means overselling; list and root-cause.
- `on_hand` large and `available` zero: reserved or committed stock stuck on old open orders; list stale unfulfilled orders with
  `get-orders(query="fulfillment_status:unfulfilled")` (`get-fulfillment-orders` needs a single orderId).
- Product sold at a loss vs unit cost, or cost 10x price: unit-of-measure error.
- Variants shared across locations with different cost: Shopify holds one cost per variant, so location-specific cost
  differences must come from the ledger.
- Cycle-count adjustments made in the admin leave no journal; ask for the adjustment history from the client if the
  variance is quantity-driven (this MCP has no inventory-adjustment history tool).

## COGS link

COGS posting follows the revenue basis chosen in `ecommerce-multichannel-month-end`. Shopify gives units sold per
variant (`get-orders` line items, capped at 10 per order, so use `get-order-by-id` for large baskets); cost per unit
must come from the ledger or a costing system. Do not derive COGS from `unitCost` unless the client has confirmed it is
maintained as average cost.

## Output

Valuation table by location (units, cost, value), exceptions (missing cost, negative stock, untracked with stock),
reconciliation to the ledger with each reconciling item, completeness statement (variants covered, calls made, any
throttling), and proposed journals for adjustments (proposals only).
