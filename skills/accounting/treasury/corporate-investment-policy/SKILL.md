---
name: corporate-investment-policy
description: >-
  Investing a company's surplus cash: writing a board-approved corporate investment policy, safety-liquidity-yield hierarchy, permitted instruments, credit and concentration limits, laddering, counterparty monitoring, accounting classification of investments and interest accrual. Use when a company has excess cash to place, or someone says "where do we park surplus cash", "treasury investment policy", "money market vs T-bills", "CD ladder", "investment concentration limits" or "held-to-maturity vs fair value". Not for personal or client portfolio advice.
metadata:
  department: "accounting"
  domain: "treasury"
  owner: "satva-coe"
  status: "beta"
  license: "Satva-original"
  source: "original"
---

# Corporate investment policy

A company invests surplus cash for **preservation of capital first, liquidity second, yield third**. Anything that reverses that order (chasing a rate, a concentrated bank, an unrated product) is a treasury control failure even if it works. This skill writes the policy and runs the process; it does not recommend securities to individuals.

## Step 1: Define the cash that may be invested

1. Take the liquidity tiers from `corporate-cash-management`: operating cash stays liquid; reserve and strategic cash may be invested.
2. Subtract restricted, trapped, covenant-minimum and customer-held cash.
3. Check the forecast: no investment may mature after the date cash will be needed (use the 13-week forecast and the longer plan). Match tenor to need.

## Step 2: Write the policy (one to three pages, board or CFO approved)

| Section | Content |
|---|---|
| Objectives | Safety, liquidity, yield, in that order |
| Authority | Who may invest, who approves, dual authorisation, limits per person |
| Permitted instruments | Bank deposits within insured and credit limits, government treasury bills, government money-market funds, high-quality prime money-market funds, short-term deposits, high-grade commercial paper only if explicitly approved |
| Prohibited | Equities, crypto, leveraged products, structured notes, unrated paper, related-party deals, derivatives not for hedging |
| Credit limits | Minimum rating per instrument or counterparty (for example investment-grade, higher for longer tenors); maximum per issuer or bank as percent of portfolio and in absolute amount |
| Concentration | No single bank or fund above a set share; sovereign/agency exempt only if stated |
| Tenor | Maximum final maturity and weighted average maturity; ladder structure |
| Liquidity | Minimum share available within 1 day and within 30 days |
| Currency | Invest in the currency of the liability; any FX held follows `fx-exposure-and-revaluation` |
| Reporting | Monthly portfolio report, quarterly policy compliance review, annual policy refresh |
| Breaches | Cure within a set period; report to CFO and audit committee |

## Step 3: Place and operate

1. Compare quotes from at least two providers for any placement above a threshold; record the rate, tenor, counterparty and approver.
2. Confirm the instrument before funding: legal name, protection or insurance limits (deposit insurance caps are per depositor per bank and change), withdrawal and break terms, early-redemption penalties, gate or fee provisions for funds.
3. Maintain a laddered maturity schedule so a tranche matures regularly.
4. Reconcile holdings to custodian statements monthly; review credit ratings, news and CDS or spread signals for counterparties; move cash if a counterparty weakens.

## Step 4: Accounting

- **Cash equivalents:** short-term (original maturity three months or less), readily convertible, insignificant value risk. Money-market funds and treasury bills qualify when they meet the test; others are short-term investments.
- **Debt securities:** classify as held-to-maturity (amortised cost), available-for-sale (fair value through OCI) or trading (fair value through P&L) under US GAAP; under IFRS 9 by business model and cash-flow characteristics.
- **Accruals:** accrue interest daily/monthly; amortise premium or discount; record realised gains and losses on sale.
- **Impairment/credit losses:** allowance for credit losses for amortised-cost holdings (CECL / IFRS 9 ECL).
- **Presentation and disclosure:** classify current vs non-current by maturity; disclose fair-value hierarchy, concentrations and restrictions.
- **Control:** a signed investment confirmation and portfolio listing support each month-end balance.

## Step 5: Monitor and review

Monthly: yield vs benchmark (government bill or money-market index), credit exposure vs limits, weighted average maturity, liquidity ladder, upcoming maturities and reinvestment plan. Quarterly: compliance report to CFO or audit committee. Annually: policy refresh, counterparty list review, comparison of net return against the opportunity cost of debt paydown (surplus cash earning less than the cost of debt is often better used to repay it, if prepayment terms allow).

## Failure modes

- Parking balances above the deposit-insurance cap in one bank with no limit.
- Chasing yield into unrated or illiquid funds.
- Locking cash in a term deposit that matures after the payroll gap.
- No documented authority; one person places and reconciles.
- Misclassifying non-qualifying holdings as cash equivalents.

## Output

Board-ready investment policy, portfolio register with maturities and limits test, monthly compliance and yield report, accounting classification memo.
