---
name: fixed-assets-depreciation
description: >-
  Fixed assets and depreciation: capitalisation policy, asset register, straight-line, declining balance and units-of-production formulas, disposals, impairment, and the book-versus-tax difference. Use for "depreciation schedule", "capitalise or expense", "asset register reconciliation", "dispose of an asset", "section 179 / tax depreciation question", "fixed assets year-end".
metadata:
  department: "accounting"
  domain: "fixed-assets"
  owner: "satva-coe"
  status: "beta"
  license: "Satva-original"
  source: "original"
---

# Fixed assets and depreciation

Tax depreciation rules (accelerated allowances, bonus depreciation, expensing elections) are jurisdiction- and year-specific: verify with the tax adviser; this skill covers the book side and organises tax data. Not tax advice.

## Capitalisation policy
Set a written threshold (e.g. 1,000-5,000 per item depending on entity size; US de minimis safe harbour for tax commonly 2,500 per invoice/item, or 5,000 with an applicable financial statement; verify). Capitalise: purchase price + taxes not recoverable + delivery + installation + testing + professional fees to bring the asset into use + borrowing costs for qualifying assets. Expense: repairs and maintenance that restore rather than improve or extend life, training, relocation. Betterments extending useful life or capacity are capitalised. Group low-value items (laptops, furniture) by class if policy says so.

## Asset register (one row per asset)
ID, description, class, location/custodian, serial number, vendor and invoice, in-service date, cost, residual value, useful life, method, accumulated depreciation, net book value, disposal date/proceeds, tax basis/method. Register must reconcile to GL: total cost = fixed asset cost accounts; total accumulated depreciation = AD accounts; depreciation expense for the period = register run.

## Methods and formulas
- **Straight-line:** annual depreciation = (Cost - Residual) / Useful life. Monthly = annual / 12. Start in the month placed in service (policy: full month, mid-month or half-year convention: document).
- **Declining balance:** annual depreciation = Opening NBV x rate; rate = factor / life (double-declining = 2 / life). Switch to straight-line when it gives a larger charge; never depreciate below residual.
- **Units of production:** (Cost - Residual) / Total expected units x units produced in the period.
- **Sum of the years' digits:** (Cost - Residual) x remaining life / sum of digits.
Typical lives (confirm to policy, local rules and actual use): computers 3-5 years, vehicles 4-5, furniture 7-10, machinery 5-15, leasehold improvements the shorter of lease term and life, buildings 25-50 (land is not depreciated), software 3-5.

Components approach (IFRS): depreciate significant parts with different lives separately (building structure vs roof vs HVAC).

## Monthly procedure
1. Add: capitalise invoices meeting the policy; record in service date.
2. Run depreciation by asset; post: Dr Depreciation expense, Cr Accumulated depreciation, by cost centre.
3. Reconcile register to GL (cost, AD, expense); investigate differences.
4. Review CIP (construction in progress): move to the class when ready for use and start depreciation; CIP not moving for over 6 months needs an explanation.

## Disposal
Gain/loss = Proceeds - NBV at disposal date. Entry: Dr Cash/receivable (proceeds), Dr Accumulated depreciation, Dr Loss (or Cr Gain), Cr Asset cost. Depreciate up to the disposal date first. Scrapped assets: proceeds zero, loss = NBV. Trade-ins and sale-leasebacks need judgement. Sales tax or VAT on disposal applies in many jurisdictions.

## Impairment
At each reporting date check indicators (physical damage, idle assets, market decline, plans to abandon). If indicators exist: US GAAP test: undiscounted cash flows < carrying amount, then write down to fair value; IFRS: recoverable amount (higher of fair value less costs of disposal and value in use) vs carrying amount. Reversals allowed under IFRS (except goodwill), not under US GAAP.

## Changes in estimate
Change in useful life/residual is prospective: new annual depreciation = (NBV - new residual) / remaining life. Do not restate prior periods; disclose.

## Book vs tax
Maintain separate tax depreciation columns (method, life, basis, bonus/expensing election). Difference creates deferred tax: deferred tax liability = (tax basis lower than book NBV) x tax rate. Report to the tax preparer with additions, disposals and listed property usage logs (estimated-tax-and-tax-prep-organiser).

## Controls
Capitalisation approved above a limit; annual physical verification of a sample (or all high-value); tag assets; disposals approved; fully depreciated assets still in use reviewed; no capitalisation of operating costs to improve profit (watch large capitalised payroll or software without time records).

## Do not
Do not depreciate land; do not backdate in-service dates to catch up; do not leave disposed assets in the register; do not change methods without approval and disclosure.

## Output
Depreciation schedule for the period, register-to-GL reconciliation, additions/disposals listing with support, impairment assessment note, tax depreciation workings for the preparer.
