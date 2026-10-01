<!-- Adapted from GAJETOso/financeskills skills/intercompany-accounting (MIT, Copyright (c) 2026 KOMVIA). Modified by Satva: merged SKILL framework with the worked-eliminations reference; jurisdiction-specific rules removed. Illustrative figures only. -->
# Intercompany framework and worked eliminations

Supplements `SKILL.md`. Read when a mismatch needs a resolution order, or when preparing consolidation eliminations.

## Transaction lifecycle discipline
1. **Agreement**: every recurring intercompany flow has a signed agreement (service description, pricing basis, payment terms); transfer pricing documentation depends on it.
2. **Pricing**: arm's length per the group's transfer pricing policy (cost-plus for services, comparable-price or resale-minus for goods, market-rate interest on loans). Local rules apply; confirm them with the tax adviser.
3. **Both-sides booking standard**: seller and buyer book in the same period. Set an intercompany cut-off deadline before entity close; the seller's invoice is authoritative.
4. **Settlement**: periodic cash settlement or netting. Aged unsettled balances attract thin-capitalisation, deemed-dividend and withholding scrutiny and create FX exposure.

## Mismatch resolution hierarchy
Work in this order: timing (in transit) then FX (different rates; fix by mandating a single rate source) then missing booking (one side never recorded) then pricing dispute (escalate to the transfer pricing owner). Differences under the tolerance auto-clear to the P&L of the buying entity and are logged.

## Elimination mechanics (consolidation)
- Balances: due-from against due-to by counterparty pair must net to zero before elimination.
- P&L: intercompany revenue against intercompany cost is eliminated gross.
- Unrealised profit: in inventory (intercompany margin times inventory still held) and in fixed assets (eliminate the gain, recompute depreciation), with deferred tax at the buyer's rate.
- Intercompany dividends, interest and management fees are eliminated; withholding tax actually paid stays real.
- A balance in a third currency revalues differently in each entity; the consolidation FX difference goes to the translation reserve, not to suspense.

## Worked eliminations (figures illustrative)

### 1. Balance elimination
Parent due-from Sub 40M; Sub due-to Parent 40M: `Dr IC Payable (Sub) 40M / Cr IC Receivable (Parent) 40M`, at consolidation level only; never touch entity books. If they do not match, fix the entity books first. Eliminating a mismatch hides an error.

### 2. Intercompany sales and unrealised profit in inventory
Sub sold goods to Parent for 30M (cost 22M); Parent resold 75 percent and holds 25 percent.
- Eliminate trading gross: `Dr IC Revenue 30M / Cr IC COGS 30M`
- Unrealised profit = 25 percent x 8M = 2M: `Dr COGS 2M / Cr Inventory 2M`
- Deferred tax at the buyer's rate (30 percent): `Dr Deferred tax asset 0.6M / Cr Tax expense 0.6M`
- If the seller is a partly owned subsidiary (upstream sale), allocate the elimination against the non-controlling interest's profit share proportionately.

### 3. Fixed asset transfer with gain
Sub sells a machine to Parent: proceeds 15M, carrying amount 10M, remaining life 5 years, transfer at the start of the year.
- Eliminate the gain: `Dr Gain on disposal 5M / Cr PP&E 5M`
- Depreciation correction (parent depreciates 3M a year, group basis 2M): `Dr Accumulated depreciation 1M / Cr Depreciation expense 1M`, repeated annually until the life ends.
- Deferred tax on the net 4M difference at the buyer's rate.

### 4. Intercompany loan and interest
Parent lends Sub 1M at 8 percent; half a year elapsed.
- Eliminate the balance: `Dr Loan payable 1M / Cr Loan receivable 1M`
- Eliminate interest: `Dr Interest income 40k / Cr Interest expense 40k`
- Withholding tax withheld on interest stays in the consolidated tax accounts (real cash to the tax authority).
- Check both sides accrued: a common mismatch is the lender accruing monthly while the borrower books on payment.

### 5. Management fees and royalties
`Dr Management fee income (Parent) / Cr Management fee expense (Sub)`, a gross elimination. Verify the transfer pricing markup documentation before eliminating; elimination does not sanitise a non-arm's-length price for tax.

### 6. Intercompany dividend
Sub declares a 20M dividend to Parent: eliminate dividend income against the subsidiary's retained earnings movement at consolidation. The non-controlling interest's share is real cash leaving the group and is not eliminated.

## Settlement netting cycle (monthly)
Build the obligation matrix, net bilaterally (or multilaterally through a netting centre), make a single payment per pair, book settlements the same day on both sides, then revalue residual FX stubs. Netting cuts wire costs and FX spread and ages nothing.

## Checks to run
- Matching matrix: counterparty-pair grid of due-from and due-to and of revenue and cost, with a difference report sorted by size.
- Unrealised profit: inventory holding report times intercompany margin by product flow.
- Loan compliance: interest accrued on both sides, market-rate evidence, thin-capitalisation headroom, withholding on interest.
