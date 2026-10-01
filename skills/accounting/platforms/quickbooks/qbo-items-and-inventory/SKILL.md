---
name: qbo-items-and-inventory
description: >-
  Set up and audit products and services in QuickBooks Online: item types (service, non-inventory, inventory, bundle), income/expense/asset account mapping, pricing, inventory quantity on hand and valuation, negative stock, adjustments, and cost of goods sold. Use when asked to "set up items in QuickBooks", "inventory valuation doesn't match the balance sheet", "negative quantity on hand", "fix COGS", "inventory adjustment", "item sales report", or "which items have wrong income account".
metadata:
  department: "accounting"
  domain: "inventory"
  platform: "quickbooks"
  owner: "satva-coe"
  status: "beta"
  license: "Satva-original"
  source: "original"
---

# QuickBooks items and inventory

Status beta: tool names verified in the server source; inventory costing behaviour is described from QuickBooks Online's documented model and not exercised live here. Follow `qbo-mcp-operating-rules`.

## Facts
- Item types (`Item.Type`): `Service`, `NonInventory`, `Inventory`, `Category`, `Group` (bundle). The API cannot create bundles (`describe_entity` `Item` says so); create bundles in the UI. Category items cannot be inactivated.
- `Inventory` items need `IncomeAccountRef`, `ExpenseAccountRef` (Cost of Goods Sold), `AssetAccountRef` (Inventory Asset), `InvStartDate` and `QtyOnHand`. Service and non-inventory items need only `IncomeAccountRef` (non-inventory may also carry an expense account).
- Inventory tracking exists only if `get_company_overview` shows `inventoryTracking: true` (quantity on hand switched on in Preferences). `InventoryAdjustment` is available on QuickBooks Plus and Advanced, US only.
- QuickBooks Online costs inventory on a FIFO basis. Inventory value moves when a bill or expense with the item is entered (cost in) and when an invoice or sales receipt is saved (cost out at the FIFO cost). Back-dating transactions changes historical COGS and can cause negative stock.
- `update_entity` `Item` is a full-update entity (merge of your patch into the whole object). Items are deactivated, not deleted (`delete_entity` sets `Active=false`; `delete_item` does the same).
- Reads: `query_quickbooks` `SELECT Id, Name, Type, Active, QtyOnHand, UnitPrice, PurchaseCost, IncomeAccountRef, ExpenseAccountRef, AssetAccountRef FROM Item MAXRESULTS 1000`; `read_item`; reports `get_item_sales`, `get_inventory_valuation_summary`.

## Workflow: item set-up
1. Decide the type: services and fees = Service; things you buy and resell but do not count = NonInventory; counted stock = Inventory. Do not use Inventory for items you do not track by quantity.
2. Map accounts. Income: product sales or service revenue accounts, one per revenue stream for reporting. COGS: Cost of Goods Sold for inventory. Asset: Inventory Asset. Check the account types: an Inventory item cannot point at a non-asset account.
3. Search for an existing item (`query_quickbooks ... WHERE Name LIKE '%x%'`) to avoid duplicates; item names must be unique.
4. Show the draft; `create_entity` `Item` (see `describe_entity` for a minimal body, e.g. `{"Name":"Consulting","Type":"Service","IncomeAccountRef":{"value":"79"}}`). Include `UnitPrice`, `PurchaseCost`, `Taxable`, `SalesTaxCodeRef` as needed (`qbo-sales-tax`).
5. For stock, set `QtyOnHand` and `InvStartDate` only at creation; later changes to quantity go through bills, invoices or an `InventoryAdjustment`, never by editing `QtyOnHand`.

## Workflow: audit
1. **Mapping check.** Pull all items; flag items whose `IncomeAccountRef` is Uncategorized Income or a generic account, inventory items with no asset or COGS account, and service items mapped to inventory accounts. Compare to the expected mapping the user provides.
2. **Valuation tie-out.** `get_inventory_valuation_summary` with `report_date` = period end versus the Inventory Asset line on `get_balance_sheet` at the same date. They should agree. If not, suspects: a journal entry posted directly to Inventory Asset, items on bills coded to expense accounts instead of item lines, inventory adjustment posted to the wrong account, or a different date.
3. **Negative and zero stock.** In the valuation report and the item query, list items with `QtyOnHand < 0` (sold before purchase was entered, or back-dated purchases), and items with quantity but zero cost. Fix at the cause: enter the missing bill with a correct date, or create an adjustment.
4. **COGS reasonableness.** `get_profit_and_loss` with `summarize_column_by: "Month"`: gross margin by month; spikes in COGS with flat sales indicate a mis-costed or adjusted item.
5. **Sales mix.** `get_item_sales` (`start_date`, `end_date`; filter `item` by Id): quantity, amount and average price; items with sales but zero margin.
6. **Report** findings with item Ids, quantities, values and fixes.

## Workflow: adjustments
- Stock count differences: `create_entity` `InventoryAdjustment` with `AdjustAccountRef` (an inventory shrinkage or COGS adjustment account) and `Line[]` of `ItemAdjustmentLineDetail` (`ItemRef`, `QtyDiff`, positive or negative). Show the quantity and value effect first; adjustments change COGS or the chosen adjustment account.
- Opening stock for a new item: enter via a bill or an initial `QtyOnHand` with `InvStartDate` before the first sale, not an adjustment.
- Write-offs: negative adjustment to a write-off expense account; document the reason.
- Wrong item on a transaction: edit that transaction line (`update_entity` with the full `Line` array); do not compensate with an adjustment.

## Pitfalls
- Inventory is not tracked by lot or serial in standard QuickBooks Online; a business needing that should use an inventory system and post summary entries (see the Linnworks mapping skill for that pattern).
- `UnitPrice` and `PurchaseCost` on the item are defaults only; they do not revalue existing stock.
- Changing an item's type after use is limited by QuickBooks; create a new item and map going forward.
- Renaming an item re-labels history; it does not merge.
- Items on estimates and purchase orders do not move stock until converted to invoices or bills.

## Output
Item mapping exceptions, valuation tie-out table, negative stock list with causes, proposed adjustments with calculation, and questions for the owner.
