---
name: ecommerce-inventory-cogs
description: >-
  Inventory valuation and COGS accounting for e-commerce and product businesses: costing methods, landed cost, marketplace and payment fees, returns, shrinkage, reserves, count reconciliation to the GL, and period-end COGS tie-out. Use for "COGS is wrong", "inventory doesn't match the GL", "landed cost", "FIFO vs average cost", "returns accounting", "inventory write-down".
metadata:
  department: "accounting"
  domain: "inventory"
  owner: "satva-coe"
  status: "beta"
  license: "Satva-original"
  source: "original"
---

# Inventory and COGS for e-commerce

## Core equation
COGS = Opening inventory + Purchases (landed cost) - Closing inventory. Inventory in the GL must equal the valuation report from the inventory system (quantity x cost per SKU/location) at every period end.

## Costing method
- **FIFO:** oldest cost leaves first; matches physical flow for perishables/expiry.
- **Weighted average:** (cost of opening + cost of receipts) / (units) recalculated on each receipt; common default for e-commerce.
- **Specific identification:** serialised/high-value items.
- **LIFO:** permitted under US GAAP, not IFRS; avoid unless tax-driven and approved.
Pick one per product class, document it, apply it consistently, and make the system and the books use the same one.

## Landed cost
Inventory cost = purchase price - trade discounts + freight in + import duty + non-recoverable taxes + insurance + customs brokerage + inbound handling. Excluded (expense): storage after receipt, outbound shipping, marketing, admin overhead. Allocate shared costs (freight, duty) to units by value, weight or volume consistently. Until final landed cost is known, receive at estimate and true-up through a landed-cost clearing account.

## What belongs in COGS vs opex (policy to state)
| Item | Common treatment |
|---|---|
| Product cost, landed cost | COGS |
| Packaging materials | COGS |
| Outbound shipping paid by the merchant | COGS (or "fulfilment" in opex; be consistent and disclosed) |
| Payment processing fees | Opex (selling) or contra-revenue; do not put in COGS unless policy says so |
| Marketplace referral fees | Selling expense or contra-revenue (gross vs net per principal/agent: revenue-recognition-606) |
| 3PL storage and pick/pack | Fulfilment cost: COGS or opex by policy |
| Shrinkage, damages, count variances | COGS |
| Inventory write-downs | COGS |

## Sales flow entries
- Sale: Dr AR/clearing, Cr Revenue (net of discounts), Cr Sales tax payable. Cost: Dr COGS, Cr Inventory at the system cost at time of shipment.
- Return with restock: Dr Revenue (or sales returns), Cr AR/refund liability; Dr Inventory, Cr COGS at original cost. Return damaged: Dr write-off (COGS), no inventory.
- Refund liability and returns reserve: estimate returns after period end for sales already recognised, using historic return rate x sales; Dr Revenue, Cr Refund liability and Dr Inventory-returns asset (right to recover products), Cr COGS.
- Drop-shipped: no inventory; COGS recognised when the customer order is fulfilled.
- Gift cards: liability until redeemed (see revenue-recognition-606 for breakage).

## Period-end reconciliation
1. Inventory valuation report total = GL inventory. Difference sources: manual journals to inventory, costs posted to wrong period, inventory-in-transit, negative on-hand quantities, items without cost.
2. Quantity reconciliation: system on-hand vs physical count (full or cycle count); variance = (counted - system) x cost; post shrink only after recount and investigation.
3. Negative inventory: investigate before closing; negative on-hand means shipments before receipts, inflating COGS at a stale cost.
4. In-transit: ownership transfers per incoterms (FOB shipping point vs destination); record goods in transit on the right side of cut-off.
5. Gross margin by SKU/channel: flag margin below threshold or above 80%+ outliers (usually missing cost).
6. Multi-channel: ensure each channel's sales feed (marketplace, storefront) posts COGS from the same costing source.

## Valuation: lower of cost and net realisable value
Write down when NRV (expected selling price - selling costs) is below cost. Reserve for slow-moving items using ageing buckets (e.g. 0-90 days 0%, 91-180 5%, 181-365 25%, >365 50-100%; tune to the business and document). Reverse only when NRV recovers (IFRS allows reversal up to original cost; US GAAP generally does not for inventory).

## KPIs
Inventory turns = COGS / average inventory; days on hand = 365 / turns; gross margin %; sell-through = units sold / units available; return rate. (See financial-reporting-pack.)

## Do not
Do not adjust COGS to hit a margin; do not write off stock without a count and approval; do not mix cost methods across systems; do not leave inventory-clearing balances open.

## Output
Inventory roll-forward (opening + receipts - COGS +/- adjustments = closing), valuation tie-out, reserve calculation, margin by SKU/channel with exceptions.

See also: `inventory-costing` (IAS 2 / ASC 330 overhead absorption and NRV with a verified script) and `inventory-reorder-planner` (velocity-based reordering).
