---
name: corporate-cash-management
description: >-
  Corporate cash management for finance teams: cash positioning, liquidity tiers and minimum balances, payment run and collection timing, working-capital levers (DSO, DPO, DIO), sweep and pooling structures, bank account rationalisation and cash controls. Use when a company needs a daily or weekly cash position, a liquidity policy, a cash-conversion improvement plan, or someone says "cash position", "minimum cash buffer", "cash pooling", "working capital release", "payment run timing" or "bank account clean-up". Forecasting method itself is in cash-flow-forecasting.
metadata:
  department: "accounting"
  domain: "treasury"
  owner: "satva-coe"
  status: "beta"
  license: "Satva-original"
  source: "original"
---

# Corporate cash management

Cash management is the discipline of knowing what cash exists today, where it sits, what must be paid before the next inflow, and what to do with the surplus. Forecasting (see `cash-flow-forecasting`) looks forward; this skill runs the daily mechanics and the policy around them.

## Step 1: Daily or weekly cash position

1. List every bank account, currency and entity with ledger balance and *available* balance (after holds, float and uncleared items).
2. Adjust for known items: cheques issued but not cleared, deposits in transit, scheduled payment batches, card settlements due, payroll debits.
3. Output a position table: opening, expected receipts, committed payments, closing available, minimum required, excess/(shortfall) by account and currency.
4. Trapped or restricted cash (escrow, customer funds, collateral, local-law restrictions, overseas subsidiaries) is shown separately and excluded from available liquidity.
5. Compare to the prior day and to the forecast; investigate variances above a set threshold the same day.

## Step 2: Liquidity policy

| Tier | Purpose | Instrument | Typical limit |
|---|---|---|---|
| Operating | Payroll, vendors, taxes in the next 2 to 4 weeks | Current accounts | Minimum balance = outflows to next reliable inflow plus buffer |
| Reserve | Shocks, 1 to 3 months of fixed costs | Sweep, money-market, short deposits | Set by risk appetite and covenant needs |
| Strategic | Surplus beyond reserve | Per investment policy | Credit, tenor, concentration limits |

Define the minimum cash buffer in days of cash outflows (a common starting point is 45 to 90 days of fixed costs for a small company; bigger buffers for volatile or seasonal businesses). Write who may move cash between tiers and what needs a second approval.

## Step 3: Working-capital levers

Cash conversion cycle = DSO + DIO - DPO.
- **Receivables (DSO):** invoice on delivery, clear terms, e-invoicing, direct debit or card on file, automated dunning, early-payment discount only when its annualised cost (discount % / (1 - discount %) x 365 / days accelerated) is below the cost of capital.
- **Payables (DPO):** pay on terms, not early; schedule payment runs weekly rather than daily; use supplier discounts where the implied return beats alternatives; supply-chain finance only after reading the covenant and accounting impact.
- **Inventory (DIO):** reduce slow stock, align reorder points, avoid bulk buys with small discounts.
Quantify each lever in cash terms: change in days x daily revenue (or COGS) = cash released. Do not count one-off timing gains as recurring.

## Step 4: Structures

- **Zero-balance and target-balance sweeps:** move excess from subsidiary accounts to a header account daily; document the intercompany loan treatment and transfer-pricing consequence.
- **Notional pooling:** offsets balances for interest without moving cash; availability depends on the bank, jurisdiction and netting rules.
- **Account rationalisation:** every account has an owner, a purpose and signers; close dormant accounts; separate accounts for restricted cash, payroll and merchant settlements.
- **Payment factory/in-house bank** only when volume and entity count justify the control overhead.

## Step 5: Controls

Dual authorisation for bank changes and payments above limits; segregation between payment creation, approval and release; bank-detail changes verified by a call-back to a known number; positive pay or payee match where offered; daily reconciliation of bank statements to the ledger; signer lists reviewed at least twice a year and on every leaver; token or hardware second factor for bank portals; no shared logins.

## Failure modes

- Reporting ledger balance as available liquidity.
- Pooling cash across entities with no intercompany record, tax or legal basis.
- Chasing early-payment discounts at a negative return.
- Stale signers and unreconciled dormant accounts.
- Counting trapped cash in covenant liquidity.

## Output

Daily cash position, liquidity policy with tiers and approvals, working-capital opportunity table (days, cash released, owner, timing), account register with signers.
