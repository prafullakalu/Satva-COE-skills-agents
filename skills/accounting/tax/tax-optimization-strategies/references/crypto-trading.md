# Crypto & Trading Tax Rules — Digital Assets, Section 475, Section 1256

## Crypto as Property — Foundational Rule

### IRS Notice 2014-21
- Cryptocurrency is **property** for federal tax purposes (not currency)
- **Every disposition is a taxable event**: sale, trade, exchange, spending
- Gain/loss = FMV at disposition minus cost basis
- Holding period determines short-term (ordinary rates) vs long-term (LTCG rates)

### What Triggers a Taxable Event
- Selling crypto for fiat (USD, EUR, etc.)
- Trading one crypto for another (e.g., BTC to ETH)
- Spending crypto on goods or services
- Receiving crypto as payment for services (ordinary income at FMV)
- Mining or staking rewards received (ordinary income at FMV)
- Airdrops (ordinary income at FMV when received, if dominion and control)
- Hard forks resulting in new tokens (ordinary income when received, per Rev. Rul. 2019-24)

### What Is NOT Taxable
- Buying crypto with fiat
- Transferring between your own wallets
- Gifting crypto (but recipient takes carryover basis; donor may file Form 709)
- Donating crypto to qualified charity (deduct FMV, no gain recognized)

## Form 8949 Reporting

### Required for Every Disposition
- Part I: Short-term (held 1 year or less) — taxed at ordinary income rates
- Part II: Long-term (held more than 1 year) — taxed at 0%, 15%, or 20%
- Each transaction requires: description, date acquired, date sold, proceeds, cost basis, gain/loss
- Summary flows to Schedule D

### Adjustment Codes (Column f)
- **B**: Basis not reported to IRS (most crypto before 2025)
- **W**: Wash sale loss disallowed (crypto ETFs only)
- **N**: Gain/loss is not reported on 1099

### Volume Traders
- Aggregate reporting allowed on Form 8949 using summary totals
- Attach a detailed statement with all transactions
- Software recommended: CoinTracker, Koinly, TaxBit, CoinLedger

## 1099-DA (New Digital Asset Reporting)

### Phased Implementation
- **2025 tax year**: Centralized exchanges (Coinbase, Kraken, etc.) begin reporting sales proceeds
- **2026 tax year**: Cost basis reporting required from exchanges
- **Brokers required to report**: Sale date, proceeds, cost basis (when available), gain/loss
- **DeFi/self-custodial**: Reporting requirements for "DeFi brokers" delayed — litigation and rulemaking ongoing

### Practical Impact
- IRS will match 1099-DA to your return (like stock 1099-B matching)
- Failure to report = CP2000 underreporter notice
- **Action**: Reconcile exchange 1099-DA with your own records before filing

## Cost Basis Methods

### Specific Identification (Preferred)
- Select exactly which lots you're selling
- Requires adequate records linking each acquisition to each disposition
- Allows strategic lot selection to minimize tax (sell highest-cost lots first)
- Must identify lots **at the time of sale** (not retroactively)

### FIFO (First-In, First-Out)
- Default method if no specific identification
- First coins purchased are first coins sold
- In a rising market, tends to produce **higher gains** (older/cheaper coins sold first)

### Average Cost (New, 2025+)
- IRS finalized rules allowing average cost basis for crypto (Reg. 1.1012-1(e))
- Once elected, applies to all units in that account/wallet
- Similar to mutual fund average cost method
- **Caution**: Once elected, changing back requires IRS consent

### LIFO (Last-In, First-Out)
- Available under specific identification
- In a rising market, tends to produce **lower gains** (newer/more expensive coins sold first)
- Useful strategy when recent purchases are at higher prices

### Best Practice
- Use **specific identification** for maximum flexibility
- Track every acquisition with: date, amount, FMV, source, wallet/exchange
- Use crypto tax software to maintain lot-level records

## Staking & Mining Rewards

### Mining
- **Ordinary income** at FMV when coins are received (mined)
- Self-employment income if mining as a business (subject to SE tax)
- Hobby mining: still ordinary income, but no SE tax
- Mining expenses: deductible as business expenses (electricity, equipment, depreciation)
- Equipment eligible for Section 179 / bonus depreciation

### Staking
- **Ordinary income** at FMV when rewards are received
- IRS position: taxable upon receipt (not when sold) — see Rev. Rul. 2023-14
- Whether staking is SE income depends on facts (active business vs passive)
- Basis in received tokens = FMV at time of receipt (for future gain/loss calculation)

### Reporting
- Mining/staking income reported on Schedule C (if business) or Schedule 1 (other income)
- Also creates a new cost basis lot for future sale

## DeFi Taxable Events

### Liquidity Pools
- Adding tokens to a liquidity pool = potential taxable exchange (depends on token structure)
- LP tokens received may be new assets with basis = FMV of tokens contributed
- Removing liquidity: taxable event, gain/loss measured against LP token basis
- Impermanent loss: NOT deductible as a separate loss (reflected in withdrawal proceeds)

### Yield Farming
- Tokens received as yield = ordinary income at FMV when received
- Compounding/reinvesting rewards = additional ordinary income events
- Each reward receipt is a separate taxable event with its own basis lot

### Token Swaps (DEX)
- Swapping Token A for Token B on a DEX = taxable disposition of Token A
- Gain/loss calculated on Token A
- Basis in Token B = FMV at time of swap

### Wrapping/Unwrapping
- Wrapping ETH to WETH: IRS has not issued definitive guidance
- Conservative position: treat as taxable exchange
- Aggressive position: treat as non-taxable (same economic substance)
- **Document your position and be consistent**

## NFT Transactions

### Collectibles Rate
- NFTs may be classified as **collectibles** under IRC Section 408(m)
- Collectibles LTCG rate: **28%** (vs standard 15%/20%)
- IRS Notice 2023-27: NFTs representing collectible art, gems, antiques, etc. are collectibles
- NFTs representing other assets (e.g., tickets, memberships, in-game items) may qualify for regular LTCG rates

### Reporting
- Sale of NFT: Form 8949 like any other property disposition
- Creating and selling NFT: ordinary income (self-employment if a business)
- Buying an NFT: not taxable (acquisition of property)
- Trading one NFT for another: taxable exchange

## Wash Sale Rule & Crypto

### Current Law
- Wash sale rule (Section 1091) applies to **stocks and securities**
- Crypto held directly is **NOT a security** under current IRS interpretation
- **Crypto ETFs/trusts ARE securities** — wash sale rule applies (GBTC, ETHE, IBIT, etc.)

### Strategy (While Loophole Exists)
- Sell crypto at a loss → immediately repurchase the same crypto
- Harvest the tax loss without losing your position
- **Cannot do this with crypto ETFs** — must wait 31 days or buy a different fund
- Multiple legislative proposals to extend wash sale rules to crypto — expect change

## Digital Assets Question — Form 1040 Page 1

### The Question
"At any time during [year], did you receive, sell, send, exchange, or otherwise acquire any digital assets?"

### Must Answer "Yes" If You
- Received crypto as payment, reward, airdrop, or hard fork
- Sold, traded, or exchanged any cryptocurrency
- Received crypto in exchange for property or services
- Disposed of any digital asset

### Can Answer "No" If You Only
- Held crypto without any transactions
- Transferred between your own wallets
- Purchased crypto with fiat (but did not sell/trade)

### Penalty
- False answer = **false statement under penalties of perjury**
- It's on page 1 — IRS specifically flagged for enforcement
- Even small transactions require "Yes" answer

## Section 475 Mark-to-Market Election (Traders)

### Trader vs Investor Status — IRS Factors
The IRS uses multiple factors to distinguish traders from investors:

1. **Frequency and regularity**: Substantial number of trades, nearly daily
2. **Holding period**: Short-term, days to weeks (not buy-and-hold)
3. **Time devoted**: Trading is a substantial part of daily activity
4. **Income source**: Seeks profit from short-term market swings (not dividends/long-term appreciation)
5. **Continuity**: Regular and continuous activity throughout the year (not seasonal)

Key cases:
- **Endicott v. Commissioner** (2013): Day trader denied — insufficient volume
- **Chen v. Commissioner** (2004): 323 trades in a year was insufficient
- **Poppe v. Commissioner** (2015): 720+ trades qualified as trader

### Election Mechanics
- **Deadline**: Must be filed by the **due date of the prior year's return** (without extension)
- **First year of trading**: Election statement must be filed within **75 days** of starting trading activity
- File a statement with your tax return: attach to Form 3115 or standalone election statement
- Must specify: the first tax year the election is effective, the trade or business to which it applies
- **Irrevocable** without IRS consent once made

### Benefits of Section 475
- All gains and losses treated as **ordinary income/loss** (not capital)
- **No $3,000 capital loss limitation** — deduct unlimited ordinary losses against other income
- **No wash sale issues** — wash sale rule applies only to capital assets (Section 475 assets are not capital assets)
- Mark all positions to market at year-end (recognize unrealized gain/loss)
- Losses offset any income type (W-2, business, interest, etc.)

### Risks of Section 475
- All gains are **ordinary income** — lose access to preferential LTCG rates (0%, 15%, 20%)
- Must mark ALL positions to market at December 31 (recognize unrealized gains)
- Cannot cherry-pick — applies to all securities/commodities in the trading business
- If trading income is high, all taxed at ordinary rates up to 37%
- **Cannot revoke** without IRS permission

### Who Should Consider
- Active day traders with significant losses
- Traders who frequently trigger wash sale issues
- Traders with net losses exceeding $3,000 in most years
- **NOT appropriate** for buy-and-hold investors or those with large unrealized LTCG

## Section 1256 Contracts — 60/40 Treatment

### Qualifying Instruments
- Regulated futures contracts (CME, CBOT, NYMEX)
- Foreign currency contracts (Section 988 may override — see election)
- Non-equity options (broad-based index options: SPX, NDX, RUT, VIX)
- Dealer equity options and dealer securities futures contracts

### Does NOT Qualify
- Equity options (options on individual stocks)
- ETF options (even if index-based, e.g., SPY options are NOT Section 1256)
- Crypto futures on unregulated exchanges

### Tax Treatment
- **60% long-term** capital gain/loss (regardless of holding period)
- **40% short-term** capital gain/loss
- Blended max rate: ~26.8% (vs 37% for all short-term)
- Mark-to-market at year-end: recognize unrealized gains/losses on December 31
- Reported on **Form 6781** (Gains and Losses from Section 1256 Contracts and Straddles)

### Carryback Rule
- Net Section 1256 losses can be **carried back 3 years** (unique to Section 1256)
- Applied only against prior Section 1256 gains
- Filed on Form 1045 or amended returns

## Straddle Rules (Section 1092)

### What Triggers Straddle Rules
- Offsetting positions in actively traded personal property
- Common: long stock + long put, long call + short call at different strikes
- If positions substantially diminish risk of loss on each other

### Tax Impact
- **Loss deferral**: Cannot deduct loss on one leg if there's an unrealized gain on the offsetting position
- Holding period: may be suspended or restarted for the appreciated position
- **Identified straddles**: Taxpayer can elect to identify straddle positions to manage tax treatment
- Qualified covered calls: exempt from straddle rules (specific IRS requirements)

### Reporting
- Form 6781 Part II for straddle transactions
- Must track offsetting positions carefully

## Day Trading Considerations

### Pattern Day Trader (FINRA Rule 4210)
- 4+ day trades within 5 business days in a margin account
- Requires $25,000 minimum equity
- **Regulatory rule only** — does not directly affect tax treatment
- Affects account type and margin requirements, not IRS classification

### Tax Implications for Day Traders
- All gains are short-term (ordinary rates) unless holding overnight extends past 1 year
- Commissions and fees are deductible (Schedule C if trader status, or investment expenses)
- Trading-related expenses: software, data feeds, education, home office
- Consider Section 475 election if sustaining regular losses

### Home Office for Traders
- Must be primary place of business for trading
- Regular and exclusive use requirement
- Deduct: proportionate rent/mortgage interest, utilities, internet, equipment

## IRS Enforcement — Blockchain Analytics

### Tools Used by IRS
- **Chainalysis**: Primary IRS contractor for blockchain tracing
- **CipherTrace** (now Mastercard): Transaction monitoring and compliance
- IRS Criminal Investigation has dedicated crypto units

### What They Can Track
- On-chain transactions linked to known exchange accounts (KYC data from subpoenas)
- Movement of funds between wallets
- Large transactions and patterns consistent with unreported income
- John Doe summons to exchanges for user transaction data (Coinbase 2017, Kraken 2021)

### Compliance Implications
- Assume the IRS can and will link exchange activity to your SSN
- Report all transactions — amended returns are better than audit adjustments
- Keep records for at least **6 years** (fraud statute is unlimited)

## FBAR and Foreign Account Reporting

### FBAR (FinCEN Form 114)
- Required if aggregate value of foreign financial accounts exceeds **$10,000** at any point during the year
- **Evolving guidance**: Whether crypto on foreign exchanges qualifies is unsettled
- FinCEN proposed rulemaking would explicitly include foreign crypto accounts
- **Conservative approach**: File FBAR if you hold crypto on foreign exchanges with >$10,000 value
- Penalties for non-filing: $10,000 per account per year (non-willful), up to $100,000 or 50% of balance (willful)

### FATCA (Form 8938)
- Separate from FBAR — filed with tax return
- Higher thresholds: $50,000+ (single, domestic) / $200,000+ (single, foreign)
- May apply to foreign exchange accounts holding crypto

### Practical Guidance
- Use U.S.-based exchanges when possible for simplicity
- If using foreign exchanges (Binance non-US, KuCoin, etc.), track balances and report conservatively
- Do NOT assume foreign exchanges are invisible to the IRS
