---
name: financial-statement-preparation
description: >-
  Prepare income statement, balance sheet and cash flow statement from a locked trial balance with period-over-period and budget comparison, variance flags, GAAP presentation requirements (ASC 220/210/230) and period-end adjustments. Use for "prepare the P&L", "balance sheet and cash flow", "monthly/quarterly/annual financial statements", "financial summary for leadership", "does the cash flow tie out".
metadata:
  department: "accounting"
  domain: "financial-reporting"
  owner: "satva-coe"
  status: "beta"
  license: "Apache-2.0"
  source: "https://github.com/anthropics/knowledge-work-plugins/blob/main/finance/skills/financial-statements"
---
<!-- Adapted from anthropics/knowledge-work-plugins (Apache-2.0, no copyright line in LICENSE; Anthropic). Modified by Satva: frontmatter to Satva contract; connector placeholders replaced with tool-agnostic wording; folded in Satva pre-flight checks, indirect cash-flow tie-out and sign-off. -->
# Financial statement preparation

**Important**: This command assists with financial statement workflows but does not provide financial advice. All statements should be reviewed by qualified financial professionals before use in reporting or filings.

Generate financial statements with period-over-period comparison and variance analysis. The workflow below walks through income statement generation; balance sheet and cash flow statement reference formats, GAAP presentation requirements (ASC 220/210/230), and common period-end adjustments are included as supporting reference material.

## Usage

```
financial-statement-preparation <period-type> <period>
```

### Arguments

- `period-type` — The reporting period type:
  - `monthly` — Single month P&L with prior month and prior year month comparison
  - `quarterly` — Quarter P&L with prior quarter and prior year quarter comparison
  - `annual` — Full year P&L with prior year comparison
  - `ytd` — Year-to-date P&L with prior year YTD comparison
- `period` — The period to report (e.g., `2024-12`, `2024-Q4`, `2024`)

## Workflow

### 1. Gather Financial Data

Obtain from the ledger or accounting system (report export, trial balance, or pasted data):
- Trial balance or income statement data for the specified period
- Comparison period data (prior period, prior year, budget/forecast)
- Account hierarchy and groupings for presentation

If no data can be pulled directly, ask the user to paste trial balance data, upload a spreadsheet, or provide income statement data. Prompt the user to provide:
- Current period revenue and expense data (by account or category)
- Comparison period data (prior period, prior year, and/or budget)
- Any known adjustments or reclassifications

### 2. Generate Income Statement

Present in standard multi-column format:

```
INCOME STATEMENT
Period: [Period description]
(in thousands, unless otherwise noted)

                              Current    Prior      Variance   Variance   Budget    Budget
                              Period     Period     ($)        (%)        Amount    Var ($)
                              --------   --------   --------   --------   --------  --------
REVENUE
  Product revenue             $XX,XXX    $XX,XXX    $X,XXX     X.X%       $XX,XXX   $X,XXX
  Service revenue             $XX,XXX    $XX,XXX    $X,XXX     X.X%       $XX,XXX   $X,XXX
  Other revenue               $XX,XXX    $XX,XXX    $X,XXX     X.X%       $XX,XXX   $X,XXX
                              --------   --------   --------              --------  --------
TOTAL REVENUE                 $XX,XXX    $XX,XXX    $X,XXX     X.X%       $XX,XXX   $X,XXX

COST OF REVENUE
  [Cost items]                $XX,XXX    $XX,XXX    $X,XXX     X.X%       $XX,XXX   $X,XXX
                              --------   --------   --------              --------  --------
GROSS PROFIT                  $XX,XXX    $XX,XXX    $X,XXX     X.X%       $XX,XXX   $X,XXX
  Gross Margin                XX.X%      XX.X%

OPERATING EXPENSES
  Research & development      $XX,XXX    $XX,XXX    $X,XXX     X.X%       $XX,XXX   $X,XXX
  Sales & marketing           $XX,XXX    $XX,XXX    $X,XXX     X.X%       $XX,XXX   $X,XXX
  General & administrative    $XX,XXX    $XX,XXX    $X,XXX     X.X%       $XX,XXX   $X,XXX
                              --------   --------   --------              --------  --------
TOTAL OPERATING EXPENSES      $XX,XXX    $XX,XXX    $X,XXX     X.X%       $XX,XXX   $X,XXX

OPERATING INCOME (LOSS)       $XX,XXX    $XX,XXX    $X,XXX     X.X%       $XX,XXX   $X,XXX
  Operating Margin            XX.X%      XX.X%

OTHER INCOME (EXPENSE)
  Interest income             $XX,XXX    $XX,XXX    $X,XXX     X.X%
  Interest expense           ($XX,XXX)  ($XX,XXX)   $X,XXX     X.X%
  Other, net                  $XX,XXX    $XX,XXX    $X,XXX     X.X%
                              --------   --------   --------
TOTAL OTHER INCOME (EXPENSE)  $XX,XXX    $XX,XXX    $X,XXX     X.X%

INCOME BEFORE TAXES           $XX,XXX    $XX,XXX    $X,XXX     X.X%
  Income tax expense          $XX,XXX    $XX,XXX    $X,XXX     X.X%
                              --------   --------   --------

NET INCOME (LOSS)             $XX,XXX    $XX,XXX    $X,XXX     X.X%       $XX,XXX   $X,XXX
  Net Margin                  XX.X%      XX.X%
```

### 3. Variance Analysis

For each line item, calculate and flag material variances.

#### Variance Calculation

For each line item, calculate:
- **Dollar variance:** Current period - Prior period (or current period - budget)
- **Percentage variance:** (Current - Prior) / |Prior| x 100
- **Basis point change:** For margins and ratios, express change in basis points (1 bp = 0.01%)

#### Materiality Thresholds

Define what constitutes a "material" variance requiring investigation. Common approaches:

- **Fixed dollar threshold:** Variances exceeding a set dollar amount (e.g., $50K, $100K)
- **Percentage threshold:** Variances exceeding a set percentage (e.g., 10%, 15%)
- **Combined:** Either the dollar OR percentage threshold is exceeded
- **Scaled:** Different thresholds for different line items based on their size and volatility

*Example thresholds (adjust for your organization):*

| Line Item Size | Dollar Threshold | Percentage Threshold |
|---------------|-----------------|---------------------|
| > $10M        | $500K           | 5%                  |
| $1M - $10M    | $100K           | 10%                 |
| < $1M         | $50K            | 15%                 |

#### Variance Decomposition

Break down total variance into component drivers:

- **Volume/quantity effect:** Change in volume at prior period rates
- **Rate/price effect:** Change in rate/price at current period volume
- **Mix effect:** Shift in composition between items with different rates/margins
- **New/discontinued items:** Items present in one period but not the other
- **One-time/non-recurring items:** Items that are not expected to repeat
- **Timing effect:** Items shifting between periods (not a true change in run rate)
- **Currency effect:** Impact of FX rate changes on translated results

#### Investigation and Narrative

For each material variance:
1. Quantify the variance ($ and %)
2. Identify whether favorable or unfavorable
3. Decompose into drivers using the categories above
4. Provide a narrative explanation of the business reason
5. Assess whether the variance is temporary or represents a trend change
6. Note any actions required (further investigation, forecast update, process change)

### 4. Key Metrics Summary

```
KEY METRICS
                              Current    Prior      Change
Revenue growth (%)                                  X.X%
Gross margin (%)              XX.X%      XX.X%      X.X pp
Operating margin (%)          XX.X%      XX.X%      X.X pp
Net margin (%)                XX.X%      XX.X%      X.X pp
OpEx as % of revenue          XX.X%      XX.X%      X.X pp
Effective tax rate (%)        XX.X%      XX.X%      X.X pp
```

### 5. Material Variance Summary

List all material variances requiring investigation:

| Line Item | Variance ($) | Variance (%) | Direction | Preliminary Driver | Action |
|-----------|-------------|-------------|-----------|-------------------|--------|
| [Item]    | $X,XXX      | X.X%        | Unfav.    | [If known]        | Investigate |

### 6. Output

Provide:
1. Formatted income statement with comparisons
2. Key metrics summary
3. Material variance listing with investigation flags
4. Suggested follow-up questions for unexplained variances
5. Offer to drill into any specific variance with `/flux`

## GAAP Presentation Requirements

### Income Statement (ASC 220 / IAS 1)

- Present all items of income and expense recognized in a period
- Classify expenses either by nature (materials, labor, depreciation) or by function (COGS, R&D, S&M, G&A) — function is more common for US companies
- If classified by function, disclose depreciation, amortization, and employee benefit costs by nature in the notes
- Present operating and non-operating items separately
- Show income tax expense as a separate line
- Extraordinary items are prohibited under both US GAAP and IFRS
- Discontinued operations presented separately, net of tax

**Common presentation considerations:**

- **Revenue disaggregation:** ASC 606 requires disaggregation of revenue into categories that depict how the nature, amount, timing, and uncertainty of revenue are affected by economic factors
- **Stock-based compensation:** Classify within the functional expense categories (R&D, S&M, G&A) with total SBC disclosed in notes
- **Restructuring charges:** Present separately if material, or include in operating expenses with note disclosure
- **Non-GAAP adjustments:** If presenting non-GAAP measures (common in earnings releases), clearly label and reconcile to GAAP

### Balance Sheet (ASC 210 / IAS 1)

- Distinguish between current and non-current assets and liabilities
- Current: expected to be realized, consumed, or settled within 12 months (or the operating cycle if longer)
- Present assets in order of liquidity (most liquid first) — standard US practice
- Accounts receivable shown net of allowance for credit losses (ASC 326)
- Property and equipment shown net of accumulated depreciation
- Goodwill is not amortized — tested for impairment annually (ASC 350)
- Leases: recognize right-of-use assets and lease liabilities for operating and finance leases (ASC 842)

### Cash Flow Statement (ASC 230 / IAS 7)

- Indirect method is most common (start with net income, adjust for non-cash items)
- Direct method is permitted but rarely used (requires supplemental indirect reconciliation)
- Interest paid and income taxes paid must be disclosed (either on the face or in notes)
- Non-cash investing and financing activities disclosed separately (e.g., assets acquired under leases, stock issued for acquisitions)
- Cash equivalents: short-term, highly liquid investments with original maturities of 3 months or less

## Balance Sheet Reference Format

```
ASSETS
Current Assets
  Cash and cash equivalents
  Short-term investments
  Accounts receivable, net
  Inventory
  Prepaid expenses and other current assets
Total Current Assets

Non-Current Assets
  Property and equipment, net
  Operating lease right-of-use assets
  Goodwill
  Intangible assets, net
  Long-term investments
  Other non-current assets
Total Non-Current Assets

TOTAL ASSETS

LIABILITIES AND STOCKHOLDERS' EQUITY
Current Liabilities
  Accounts payable
  Accrued liabilities
  Deferred revenue, current portion
  Current portion of long-term debt
  Operating lease liabilities, current portion
  Other current liabilities
Total Current Liabilities

Non-Current Liabilities
  Long-term debt
  Deferred revenue, non-current
  Operating lease liabilities, non-current
  Other non-current liabilities
Total Non-Current Liabilities

Total Liabilities

Stockholders' Equity
  Common stock
  Additional paid-in capital
  Retained earnings (accumulated deficit)
  Accumulated other comprehensive income (loss)
  Treasury stock
Total Stockholders' Equity

TOTAL LIABILITIES AND STOCKHOLDERS' EQUITY
```

## Cash Flow Statement Reference Format (Indirect Method)

```
CASH FLOWS FROM OPERATING ACTIVITIES
Net income (loss)
Adjustments to reconcile net income to net cash from operations:
  Depreciation and amortization
  Stock-based compensation
  Amortization of debt issuance costs
  Deferred income taxes
  Loss (gain) on disposal of assets
  Impairment charges
  Other non-cash items
Changes in operating assets and liabilities:
  Accounts receivable
  Inventory
  Prepaid expenses and other assets
  Accounts payable
  Accrued liabilities
  Deferred revenue
  Other liabilities
Net Cash Provided by (Used in) Operating Activities

CASH FLOWS FROM INVESTING ACTIVITIES
  Purchases of property and equipment
  Purchases of investments
  Proceeds from sale/maturity of investments
  Acquisitions, net of cash acquired
  Other investing activities
Net Cash Provided by (Used in) Investing Activities

CASH FLOWS FROM FINANCING ACTIVITIES
  Proceeds from issuance of debt
  Repayment of debt
  Proceeds from issuance of common stock
  Repurchases of common stock
  Dividends paid
  Payment of debt issuance costs
  Other financing activities
Net Cash Provided by (Used in) Financing Activities

Effect of exchange rate changes on cash

Net Increase (Decrease) in Cash and Cash Equivalents
Cash and cash equivalents, beginning of period
Cash and cash equivalents, end of period
```

## Common Adjustments and Reclassifications

### Period-End Adjustments

1. **Accruals:** Record expenses incurred but not yet paid (AP accruals, payroll accruals, interest accruals)
2. **Deferrals:** Adjust prepaid expenses, deferred revenue, and deferred costs for the period
3. **Depreciation and amortization:** Book periodic depreciation/amortization from fixed asset and intangible schedules
4. **Bad debt provision:** Adjust allowance for credit losses based on aging analysis and historical loss rates
5. **Inventory adjustments:** Record write-downs for obsolete, slow-moving, or impaired inventory
6. **FX revaluation:** Revalue foreign-currency-denominated monetary assets and liabilities at period-end rates
7. **Tax provision:** Record current and deferred income tax expense
8. **Fair value adjustments:** Mark-to-market investments, derivatives, and other fair-value items

### Reclassifications

1. **Current/non-current reclassification:** Reclassify long-term debt maturing within 12 months to current
2. **Contra account netting:** Net allowances against gross receivables, accumulated depreciation against gross assets
3. **Intercompany elimination:** Eliminate intercompany balances and transactions in consolidation
4. **Discontinued operations:** Reclassify results of discontinued operations to a separate line item
5. **Equity method adjustments:** Record share of investee income/loss for equity method investments
6. **Segment reclassifications:** Ensure transactions are properly classified by operating segment


---

# Satva additions (pre-flight and tie-outs)

## Pre-flight checks
1. TB debits = credits. Assets = Liabilities + Equity at the report date.
2. Account map: every GL account maps to exactly one statement line; no unmapped accounts.
3. Comparatives: same mapping for the prior period; restate comparatives and disclose if mapping changed.
4. Basis and currency stated in the header; reporting period and "unaudited/draft" label.

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

## Review sign-off
Preparer, reviewer, date; analytics: gross margin %, operating margin %, DSO, DPO, current ratio vs prior period all explained (flux-variance-analysis).

## Do not
Do not net items to make a statement tidy; do not move accounts between lines without disclosure; do not publish from an unlocked period without a "draft" label.

## Deliverable
Three statements with comparatives, a tie-out sheet (BS balances, RE roll, cash proof), and a short note of judgements made.

Related skills: month-end-close, flux-variance-analysis, financial-reporting-pack.
