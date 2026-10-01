---
name: manufacturing-cost-accounting
description: >-
  Manufacturing cost accounting: bills of materials and routings, raw material/WIP/finished goods flow, standard costing and variances, overhead absorption, job and process costing, inventory valuation (LCNRV), scrap and yield, and month-end manufacturing close. Use when a manufacturer needs product costs, inventory valuation or variance analysis, or someone says "standard cost", "overhead absorption", "purchase price variance", "WIP inventory", "yield loss", "BOM cost rollup" or "manufacturing variance".
metadata:
  department: "accounting"
  domain: "industries"
  owner: "satva-coe"
  status: "beta"
  license: "Satva-original"
  source: "original"
---

# Manufacturing cost accounting

Product cost is only as true as the BOM, routing and overhead rate behind it. Inventory is typically the largest balance-sheet asset and the largest audit risk, so the goal is a cost method that is reproducible, reconciled to the stock ledger and explainable by variance.

## Step 1: Costing method

| Environment | Method |
|---|---|
| Repetitive, many units, few products | Process costing (cost per equivalent unit per department) |
| Custom or batch work | Job costing (actual cost per job order) |
| Stable products, planning-driven | Standard costing with variance accounts |
| Small/simple | Actual (FIFO or weighted average) with a periodic overhead true-up |

LIFO is not permitted under IFRS and is rare under GAAP outside tax conformity. Choose one cost-flow assumption per inventory class and apply it consistently.

## Step 2: Cost build-up

1. **Materials:** BOM quantity x unit cost, plus normal scrap/yield allowance. Include freight-in and duties in landed cost.
2. **Direct labour:** routing hours per operation x labour rate (loaded).
3. **Overhead:** variable (energy, consumables) and fixed (rent, depreciation, supervision) pools, absorbed by a driver: machine hours, labour hours or units. Rate = budgeted pool / budgeted driver at *normal* capacity. Fixed overhead is not absorbed on idle capacity beyond normal; the excess is expensed in the period.
4. **Cost roll-up:** bottom-up from components to subassemblies to finished goods; re-run when prices, BOMs, routings or rates change, and keep a dated cost snapshot.

Worked example: component cost 6.00 plus 0.5 labour hour at 24.00 = 12.00, overhead at 18.00 per machine hour x 0.25 = 4.50, standard cost = 22.50.

## Step 3: Inventory accounts and flow

Raw materials -> WIP -> finished goods -> COGS. Journals per period:
- Receipt: Dr Raw materials / Cr GRNI (goods received not invoiced), cleared by the AP invoice; the difference vs standard goes to purchase price variance.
- Issue to production: Dr WIP / Cr Raw materials at standard.
- Labour and overhead applied: Dr WIP / Cr Labour applied, Overhead applied.
- Completion: Dr Finished goods / Cr WIP at standard.
- Shipment: Dr COGS / Cr Finished goods.

Actual payroll and overhead go to control accounts; the difference to *applied* amounts is under/over-absorbed.

## Step 4: Variance analysis

| Variance | Formula | Likely cause |
|---|---|---|
| Purchase price | (Actual price - standard) x quantity bought | Supplier price, freight, currency |
| Material usage | (Actual qty - standard qty) x standard price | Scrap, yield, BOM wrong |
| Labour rate | (Actual rate - standard) x actual hours | Overtime, mix of grades |
| Labour efficiency | (Actual hours - standard hours) x standard rate | Rework, setup, learning curve |
| Variable overhead spending/efficiency | As labour/machine hours | Utilities, consumables |
| Fixed overhead volume | (Normal capacity - actual) x fixed rate | Under-utilisation |

At period end, immaterial variances go to COGS; material variances are prorated across WIP, finished goods and COGS in proportion to the standard cost in each. Review standards at least annually or when cumulative variances stay above a set percent of cost.

## Step 5: Valuation and close

1. Physical count or cycle counts reconcile to the perpetual record; post adjustments with reason codes and approval.
2. Lower of cost and net realisable value (IFRS, and GAAP for FIFO/average): write down obsolete, slow-moving and damaged stock using aging and sell-through; keep a reserve schedule.
3. Capitalise only production-related cost in inventory; abnormal waste, storage not needed for production, admin and selling costs are period expenses.
4. Consigned stock stays off the balance sheet unless you own it; goods in transit follow incoterm title transfer.
5. Reconcile inventory subledger to GL, GRNI to open receipts, and WIP to open work orders. Any unreconciled item over a threshold is investigated before close.

## Failure modes

- Standards left unchanged for years, variances drowning real signals.
- Fixed overhead absorbed on idle capacity, inflating inventory.
- GRNI never cleared; liabilities and stock both overstated.
- BOM changes without cost re-roll.
- Scrap booked only at count time.

## Output

Cost roll-up with component detail, monthly variance report with proration, inventory reconciliation, obsolescence reserve schedule.
