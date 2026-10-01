---
name: fx-exposure-and-revaluation
description: >-
  Foreign exchange for finance teams: transaction, translation and economic exposure, measuring net exposure by currency, hedging policy and instruments (forwards, options, natural hedges), period-end revaluation of monetary items, realised vs unrealised FX, functional currency and translation (ASC 830 / IAS 21), and intercompany FX. Use when a business has multi-currency books, payables or receivables, or someone says "unrealised FX gain/loss", "revalue foreign currency balances", "functional currency", "hedge our EUR exposure", "translation adjustment" or "CTA".
metadata:
  department: "accounting"
  domain: "treasury"
  owner: "satva-coe"
  status: "beta"
  license: "Satva-original"
  source: "original"
---

# FX exposure and revaluation

Two jobs share one name: **treasury** decides how much currency risk to carry; **accounting** measures and reports whatever risk exists. Do the accounting correctly first; hedging a mismeasured exposure only adds noise.

## Step 1: Set currencies

1. **Functional currency** of each entity: the currency of the primary economic environment (sales prices, costs, financing, cash retention). Decide it once, document the indicators, and change it only for a real change in facts.
2. **Presentation currency** of the consolidation.
3. **Transaction currency** of each invoice, bill, loan and bank account.
Bank accounts in a foreign currency are monetary items.

## Step 2: Transaction-level accounting

1. Record foreign-currency transactions at the spot rate (or an average rate for a period where that approximates) at the transaction date. Use one rate source and time (for example the central bank or a defined data provider daily close) and record the source in the policy.
2. Settlement: the difference between booked rate and settlement rate is a **realised** FX gain or loss.
3. Period-end: **revalue monetary items** (cash, receivables, payables, loans, accruals settled in cash) at the closing rate; the difference is an **unrealised** FX gain or loss in profit or loss. Reverse it on day one of the next period, or keep revaluing from the original carrying amount as the system supports.
4. **Non-monetary items** (inventory, fixed assets, prepaid, deferred revenue) stay at historical rate.
5. Foreign-currency intercompany loans: gains/losses go to P&L unless the loan is of a long-term investment nature and settlement is neither planned nor likely (then to OCI in consolidation).

Worked example: EUR 10,000 invoice booked at 1.0800 = USD 10,800. Month-end rate 1.1000 revalues the receivable to USD 11,000 (unrealised gain 200). Paid at 1.0900 = USD 10,900; realised loss on settlement vs the revalued carrying amount reverses the unrealised and leaves a net realised gain of 100 against the original booking.

## Step 3: Translation of foreign subsidiaries

Translate assets and liabilities at the closing rate; income and expenses at the transaction-date or average rate; equity at historical rates. The balancing difference is the **cumulative translation adjustment** in OCI. On disposal or liquidation of the foreign entity, recycle CTA to profit or loss. Entities in hyperinflationary economies need a separate remeasurement approach.

## Step 4: Measure exposure

Build a currency net exposure table: monetary assets less monetary liabilities by currency and entity, plus forecast committed cash flows by month (receipts, payments, interest, dividends, capex) for 12 months. Net across natural hedges (USD costs against USD revenues). Report: gross, net, hedged, residual, sensitivity (a 10 percent move in each currency x net exposure). Forecast exposure is less certain than booked exposure; tag each by confidence tier.

## Step 5: Hedging policy

1. Objectives: protect budget rates and margin, not speculate. Set the hedge ratio by confidence (for example highly probable 12-month forecast flows partly hedged, booked exposures largely hedged), the maximum tenor, authorised instruments, authorised counterparties, and approval limits.
2. Natural hedges first: invoice in cost currency, match borrowing currency to revenue, net intercompany balances, leads and lags within terms.
3. Instruments: forwards (lock rate, no upside), options (premium, keeps upside), swaps (hedging loans). Reject exotic or leveraged products for non-financial companies.
4. Counterparty and documentation: ISDA or bank terms, credit lines, margin requirements, signatory authority.
5. Hedge accounting (ASC 815 / IFRS 9): designate and document at inception (relationship, risk, effectiveness assessment). Without designation, derivative fair-value changes go straight to P&L and may create volatility not offset by the hedged item.
6. Review monthly: mark-to-market, hedge ratio vs policy, effectiveness, maturities, counterparty exposure.

## Failure modes

- Revaluing non-monetary items or forgetting loans and accruals.
- Mixing realised and unrealised FX on one account so nobody can explain it.
- Different rate sources per module, creating phantom differences.
- Hedge placed with no documented exposure.
- Treating the forward rate as a forecast of the spot rate.
- Intercompany balances not eliminated at consistent rates.

## Output

Currency and rate policy, exposure table, revaluation journal and reversal, realised/unrealised FX report, CTA roll-forward, hedge register with mark-to-market.
