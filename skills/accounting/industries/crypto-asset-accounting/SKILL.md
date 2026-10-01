---
name: crypto-asset-accounting
description: >-
  Accounting for digital assets held or used by a business: classification, fair-value measurement (ASU 2023-08 for US GAAP), cost basis lots, wallet and exchange reconciliation, staking, DeFi and NFT activity, payments received or made in crypto, tax-lot tracking and audit evidence. Use when a company holds, accepts or trades crypto, or someone says "crypto books", "wallet reconciliation", "staking rewards accounting", "cost basis lots", "fair value crypto", "token revenue" or "exchange export to GL".
metadata:
  department: "accounting"
  domain: "industries"
  owner: "satva-coe"
  status: "beta"
  license: "Satva-original"
  source: "original"
---

# Crypto asset accounting

Frameworks differ by jurisdiction and change quickly. State the standard applied in the workpaper, confirm current guidance for the client's jurisdiction, and keep tax and financial-reporting treatments in separate columns because they usually differ.

## Step 1: Classify what is held

| Asset | US GAAP (post ASU 2023-08) | IFRS (general view) |
|---|---|---|
| Bitcoin, ether and similar fungible crypto assets meeting the scope criteria | Fair value, changes in net income each period | Intangible (IAS 38 cost or revaluation) or inventory (IAS 2) for a trader/broker |
| Stablecoins backed by fiat | Often a financial asset or cash-equivalent question; analyse redemption rights | Financial asset analysis |
| NFTs, utility tokens | Scope analysis; may fall outside the fair-value standard | Intangible/inventory |
| Tokens received as customer payment | Non-cash consideration at fair value at contract inception | Same principle |
| Custodial holdings for customers | Possible safeguarding liability and asset (SAB 121 successor guidance) | Case-specific |

Document the scope conclusion per asset class; do not default.

## Step 2: Build the ledger

1. **Wallet and account register:** every address, exchange account, custodian and multisig, with owner, purpose, signers and date opened. An unregistered wallet is an unrecorded asset or a control gap.
2. **Transaction ledger:** import on-chain transactions and exchange exports (trades, deposits, withdrawals, fees, staking). Include network fees. Keep tx hash, timestamp (UTC), asset, amount, counterparty address, and fiat value at transaction time.
3. **Internal transfers** between own wallets are not disposals; match and net them so they do not appear as sales.
4. **Cost basis lots:** keep lots by acquisition date and cost; choose and document the method (specific identification where records support it, else FIFO or per tax rules). Fees adjust basis or proceeds.
5. **Pricing:** one policy for the price source and time (principal market, end-of-day UTC close from a named source) applied consistently to measurement and reconciliations.

## Step 3: Journals

- Purchase with fiat: Dr Digital assets (cost) / Cr Cash.
- Fair-value remeasurement at period end: Dr or Cr Digital assets / Cr or Dr Unrealised gain or loss (net income).
- Sale: Dr Cash, Dr or Cr Realised gain/loss, Cr Digital assets (carrying amount).
- Receipt as payment for goods: Dr Digital assets at fair value at receipt / Cr Revenue; later move with fair value.
- Payment in crypto for expenses or assets: Dr Expense or asset at fair value / Cr Digital assets, with the gain or loss on disposal recognised.
- Staking and mining rewards: income when control is obtained (the entity can freely use or sell), at fair value on that date, with a reasoned judgement if rewards are locked or subject to slashing.
- DeFi: lending and liquidity positions need an analysis of what is held (receipt token, claim on pool); capture impermanent loss, yield and gas on separate lines.

## Step 4: Reconciliation and evidence (the audit risk)

1. Reconcile each wallet and exchange balance to the ledger at period end: on-chain balance via a block explorer snapshot (screenshot or export with block height and time), exchange statement, custodian statement. Differences are traced to a transaction.
2. Existence and ownership: proof of control through a signed message or a test transfer, not a screenshot of a wallet app alone; for custodians, obtain SOC reports and the account agreement.
3. Completeness: scan for unknown inbound transfers, airdrops, dust and spam tokens (assess, do not interact with suspicious tokens).
4. Cut-off: remeasure at the balance-sheet date and time zone convention.
5. Private key and signer controls: who can move funds, thresholds, offboarding, hardware storage, recovery process. Without these, auditors cannot rely on balances.
6. Related-party and token-holder transactions: disclose.

## Step 5: Tax and compliance (kept separate)

Disposals, swaps and spending are generally taxable events in many jurisdictions; staking and mining income has its own timing rules; reporting forms and thresholds vary and change. Maintain per-lot proceeds and basis for tax, and flag travel-rule, AML/KYC and sanctions-screening obligations if the business is a money-services business.

## Failure modes

- Treating wallet-to-wallet moves as sales.
- Valuing at a different price source each month.
- Ignoring network fees.
- Relying on exchange CSVs without on-chain verification.
- No register of wallets, so inherited or legacy addresses go unrecorded.

## Output

Wallet register, lot-level ledger, remeasurement journal, period-end reconciliation pack with evidence references, and an accounting-policy memo with the standard applied.
