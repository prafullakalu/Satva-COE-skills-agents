---
name: financial-statement-preparation
description: >-
  Prepare and check the three core statements: P&L, balance sheet and cash flow statement (indirect method), with classification rules, tie-out checks and a presentation format. Use when asked to "produce financial statements", "build a cash flow statement", "why doesn't the balance sheet balance", "prepare the P&L and balance sheet", or "indirect cash flow from a trial balance".
metadata:
  department: "accounting"
  domain: "financial-reporting"
  owner: "satva-coe"
  status: "beta"
  license: "Satva-original"
  source: "original"
---

# Financial statement preparation

Start from an adjusted, locked trial balance (see month-end-close). Statements are a re-presentation of the TB; never hand-type numbers.

## Pre-flight checks
1. TB debits = credits. Assets = Liabilities + Equity at the report date.
2. Account map: every GL account maps to exactly one statement line; no unmapped accounts.
3. Comparatives: same mapping for the prior period; restate comparatives and disclose if mapping changed.
4. Basis and currency stated in the header; reporting period and "unaudited/draft" label.

## Income statement (P&L) layout
Revenue (net of returns, discounts) -> Cost of goods sold -> **Gross profit** -> Operating expenses (by nature or function; be consistent) -> **Operating income (EBIT)** -> Other income/expense (interest, FX, disposal gains) -> **Pre-tax income** -> Income tax -> **Net income**. Show EBITDA only as a labelled non-GAAP supplement: EBITDA = Operating income + depreciation + amortisation.

Checks: gross margin % vs history; payroll and rent both appear; depreciation present; no balance sheet accounts in P&L; one-offs shown separately.

## Balance sheet layout
Current assets (cash, receivables net of allowance, inventory, prepaids) -> Non-current assets (PPE net, intangibles, deposits) -> Total assets. Current liabilities (payables, accruals, deferred revenue, tax, current portion of debt) -> Non-current liabilities -> Equity (share capital, retained earnings, current-year earnings, other reserves).

Classification: current = settled or realised within 12 months or operating cycle. Debt with covenant breach at the date is current unless a waiver exists. Customer credit balances in AR present as liabilities; vendor debit balances in AP present as assets (do not net across parties unless right of offset).

Checks: retained earnings roll (opening + net income - dividends = closing); allowance and accumulated depreciation as contra accounts; no negative cash across accounts netted (overdraft is a liability unless offset rights exist); intercompany eliminated.

## Cash flow statement (indirect)
Operating = Net income
  + depreciation, amortisation, impairment
  + loss (- gain) on disposals
  + unrealised FX loss (- gain) and other non-cash items
  - increase (+ decrease) in receivables, inventory, prepaids
  + increase (- decrease) in payables, accruals, deferred revenue, tax payable
Investing = - purchases of PPE/intangibles + proceeds from disposals - loans made + loans repaid to the entity.
Financing = + new borrowings - repayments + share issues - dividends. (Interest paid and received, dividends received: choose a classification policy and apply consistently; US GAAP puts interest in operating, IFRS allows a choice.)
Net change in cash = Operating + Investing + Financing. **Must equal closing minus opening cash and cash equivalents; if not, the difference is an error, not a plug.**

Common causes of a failed tie-out: change in a working-capital account that was not mapped; capex bought on credit (non-cash: exclude from investing, disclose); depreciation double-counted; FX on cash balances omitted (show as a separate effect-of-exchange-rates line); current-portion-of-debt movement missed; dividends declared but unpaid.

Cash equivalents: short-term, highly liquid, original maturity of 3 months or less. State the policy.

## Notes and disclosures (minimum for management accounts)
Basis of preparation, significant accounting policies, receivable ageing, debt maturity, related-party balances, commitments, contingencies, subsequent events. Statutory accounts need a full framework (IFRS, IFRS for SMEs, US GAAP or local) and a qualified accountant.

## Review sign-off
Preparer, reviewer, date; analytics: gross margin %, operating margin %, DSO, DPO, current ratio vs prior period all explained (flux-variance-analysis).

## Do not
Do not net items to make a statement tidy; do not move accounts between lines without disclosure; do not publish from an unlocked period without a "draft" label.

## Output
Three statements with comparatives, a tie-out sheet (BS balances, RE roll, cash proof), and a short note of judgements made.
