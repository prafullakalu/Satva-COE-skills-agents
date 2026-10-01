---
name: impairment-provisions-contingencies
description: >-
  Impairment of non-financial assets (IAS 36, ASC 360 and ASC 350), provisions and contingent liabilities (IAS 37, ASC 450), onerous contracts, restructuring and asset retirement obligations, and the simplified expected-credit-loss provision matrix for receivables (IFRS 9 / CECL). Use for 'do we need an impairment test', 'goodwill impairment', 'should we book a provision', 'contingent liability disclosure', 'warranty provision', 'decommissioning liability', 'bad debt allowance calculation'.
metadata:
  department: "accounting"
  domain: "provisions"
  owner: "satva-coe"
  status: "beta"
  license: "Satva-original"
  source: "original"
---

# Impairment, provisions and contingencies

Judgement-heavy area. Prepare the analysis, the numbers and the memo; the conclusion on material items is reviewed by the controller and, where relevant, the auditor. Standards cited are the framework; always confirm the applicable GAAP and the entity's policy.

## Part 1: Impairment of non-financial assets

### Step 1: Is a test required?
- **Goodwill and indefinite-life intangibles:** test at least annually (same date each year) and whenever an indicator exists. Intangibles not yet in use: annual under IFRS.
- **PP&E, finite-life intangibles, ROU assets:** test only when an indicator exists at the reporting date.
- Indicators: market capitalisation below book equity, adverse change in market, legal or regulatory environment, physical damage or obsolescence, asset idle or plan to dispose early, worse-than-budget performance, rising interest rates that raise the discount rate, loss of a key customer or licence.
- Record the indicator review every period even when the answer is "none", with the evidence examined. An undocumented review is a finding.

### Step 2: Group the assets
IFRS: **cash-generating unit (CGU)** = smallest group generating largely independent cash inflows. US GAAP: **asset group** (ASC 360, lowest level with identifiable cash flows) and **reporting unit** (goodwill, ASC 350: operating segment or one level below). Document why the grouping is stable year to year; changing it to avoid an impairment is a red flag.

### Step 3: Run the test
| | IFRS (IAS 36) | US GAAP |
|---|---|---|
| Long-lived assets | Carrying amount vs **recoverable amount** = higher of fair value less costs of disposal (FVLCD) and value in use (VIU) | Step 1 recoverability: carrying amount vs **undiscounted** cash flows. If not recoverable, Step 2: write down to **fair value** |
| Goodwill | CGU carrying amount (incl. allocated goodwill) vs recoverable amount | Reporting unit fair value vs carrying amount (ASC 350-20); loss = excess, capped at goodwill |
| Reversal | Allowed for assets other than goodwill, up to the carrying amount that would have existed without impairment | Not allowed for assets held and used |

Impairment loss = carrying amount - recoverable amount (or fair value). Allocate a CGU loss first to goodwill, then pro rata to other assets, but not below the highest of FVLCD, VIU and zero for any single asset.

### Step 4: Value in use inputs
- Cash flows from the latest board-approved budget, normally 5 years maximum; beyond that a steady or declining growth rate not above long-term average growth of the market. Exclude uncommitted restructurings and enhancements, financing flows and tax cash flows (pre-tax model).
- Pre-tax discount rate reflecting time value and asset-specific risk; derive from WACC and check against market evidence. Do not use a rate that "works".
- Sensitivity: headroom (recoverable amount - carrying amount) and the change in discount rate, growth rate and margin that eliminates it. Disclose when a reasonably possible change causes impairment.

### Worked example (IFRS)
CGU carrying amount 12.0m including goodwill 3.0m. VIU 10.4m; FVLCD 9.8m. Recoverable amount = 10.4m. Loss = 1.6m, all to goodwill (leaving 1.4m). Entry: Dr Impairment loss 1.6m, Cr Goodwill 1.6m. Depreciation of other assets continues on unchanged carrying amounts.

### Impairment checks
Carrying amounts in the test tie to the trial balance (same perimeter, including working capital treatment, corporate assets allocated, ROU assets and lease liabilities treated consistently with the cash flows). Forecast accuracy: back-test last year's forecast against actuals. Impairment losses flagged separately in the income statement or notes.

## Part 2: Provisions and contingencies

### Recognition test (IAS 37 / ASC 450)
Recognise a **provision** when all hold: (1) present obligation (legal or constructive) from a past event; (2) outflow probable (IFRS: more likely than not; US GAAP: "probable" is a higher bar, roughly 70-75%+ in practice); (3) amount can be reliably estimated (US GAAP: reasonably estimable).
- **IFRS measurement:** best estimate; expected value for a large population (warranties), most likely outcome for a single obligation; discount if the time value is material.
- **US GAAP:** best estimate in a range; if no amount is better, accrue the **low end** of the range and disclose the range; no discounting unless the amount and timing are fixed.
- Reimbursements (insurance) are a separate asset, recognised only when virtually certain (IFRS) or probable (US GAAP), never netted in the provision.

### Contingent liability
Possible obligation or probable-but-not-estimable: do not recognise; disclose nature and estimate of range unless remote. Contingent **assets**: never recognise until realisation is virtually certain; disclose if inflow is probable (IFRS).

### Common provisions
| Item | Test and measurement |
|---|---|
| Warranty | Expected value: units sold x failure rate x average cost; reassess rate from claim history each period |
| Onerous contract (IAS 37; ASC 450/605-35 for losses) | Unavoidable cost of meeting the contract exceeds the benefits; IFRS cost = lower of cost to fulfil and cost to exit; includes direct and allocated costs |
| Restructuring | Only when a detailed formal plan exists and has been announced or started; include only direct costs of the restructuring, not future operating costs. IFRS: constructive obligation; US GAAP: one-time benefits recognised when communicated, plus ASC 420 criteria |
| Legal claim | Counsel assessment of probability and range; update every quarter; do not book without evidence just to be prudent (cookie-jar reserves) |
| Asset retirement obligation (IFRIC 1 / ASC 410-20) | PV = future cost (inflation adjusted) / (1 + rate)^n; capitalise PV to the asset, accrete the liability each period (opening balance x rate), depreciate the capitalised piece; revise for changes in estimate prospectively |
| Dilapidations, onerous leases | Recognise when the obligation arises; for leases under IFRS 16/ASC 842 impair the ROU asset instead of a separate onerous provision |

### Provision roll-forward (required disclosure)
Opening + additions - utilised - reversed (unused) + unwinding of discount (+/- FX) = closing. Utilise only against the cost the provision was created for; releasing to profit needs approval and a reason.

## Part 3: Receivables allowance (simplified ECL / CECL)
1. Segment receivables by shared risk characteristics (customer type, geography, product).
2. Age each segment; take the historical loss rate per bucket over 2-3 years (write-offs plus subsequent recoveries / balances in the bucket at the start of the period).
3. Adjust for current conditions and reasonable forecasts (sector stress, customer concentration, macro indicators); document the adjustment, even when it is zero.
4. Allowance = sum(bucket balance x adjusted loss rate). Specific allowance for individually credit-impaired balances first; remove them from the matrix.
5. Entry: Dr Credit loss expense, Cr Allowance. Write-off: Dr Allowance, Cr Receivable (needs approval). Recovery: Dr Receivable and Cr Allowance, then cash receipt.
6. Check: allowance movement (opening + expense - write-offs + recoveries = closing) and coverage ratio trend. Coverage dropping while overdue balances rise needs an explanation.
For loans and bond portfolios (staging, 12-month vs lifetime ECL, PD x LGD x EAD x discount factor) use a dedicated credit-risk methodology.

## Do not
Do not use provisions to smooth earnings; do not release a provision without the triggering evidence; do not discount at a convenient rate; do not net insurance recoveries against the provision; do not skip documenting a "no impairment indicators" conclusion; do not change the test date, grouping or method to avoid a loss.

## Output
Indicator review log, impairment model with sensitivity and headroom, provision schedule with roll-forward and support per item, contingent liabilities register with counsel status, ECL matrix and allowance reconciliation, draft journals and the memo for the controller.
