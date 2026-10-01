---
name: linnworks-to-ledger-posting-rules
description: >-
  Design and review how multichannel e-commerce activity from Linnworks (marketplace sales, shipping, VAT/sales tax,
  refunds, marketplace and payment fees, settlements, chargebacks, FBA and stock movements) should post to a general
  ledger: accounts, clearing accounts, timing, COGS, VAT/OSS and multi-currency. Use for "how should Amazon sales
  post", "set up a channel clearing account", "where do marketplace fees go", "VAT OSS on marketplace sales",
  "when to recognise COGS", "design the journal for a settlement". Platform-neutral posting logic fed by Linnworks data;
  client mapping execution is in lw-qbo-mapping.
metadata:
  department: "accounting"
  domain: "ecommerce-posting"
  platform: "linnworks"
  owner: "satva-coe"
  status: "beta"
  license: "Satva-original"
  source: "original"
---

# Linnworks to ledger: posting rules

Linnworks is an order and stock system, not a ledger and not a settlement system. Correct books come from joining
three streams: **orders** (what was sold, from Linnworks), **settlements** (what the channel paid and charged, from the
channel or PSP), and **stock** (cost, from Linnworks plus purchases). This skill defines how each posts. To execute
mapping against QuickBooks Online, use the existing `lw-qbo-mapping` skill; do not re-do its job here.

## Core design: one clearing account per channel

For every channel (and PSP) keep a **clearing account** (asset, "Amazon clearing", "Shopify clearing"). Sales debit
it; fees, refunds and chargebacks credit it; the settlement payout credits it and debits bank. The balance is, by
definition, money the channel owes you. A clearing account that does not trend to near zero after each payout cycle
is the single best error detector in e-commerce accounting.

Never post sales straight to bank. Never net fees against sales in one line: the gross/fee split is needed for margin,
VAT and tax filings.

## Posting matrix

| Event | Source | Dr | Cr | Timing and notes |
|---|---|---|---|---|
| Sale (goods) | Linnworks order lines | Channel clearing (gross incl. tax) | Sales revenue by channel (net), Output tax | On order basis chosen once (order date or dispatch date). Record the basis in the client file |
| Shipping charged | Order postage (`PostageCostExTax`) | Channel clearing | Shipping income, Output tax | Separate account; shipping tax rate can differ from goods |
| Discount/promo funded by seller | `LineDiscount`, `TotalDiscount` | Sales discounts (contra revenue) | Channel clearing | Net to revenue, not a marketing expense, unless the channel invoices it as a fee |
| Marketplace referral/final-value fee | Settlement report | Marketplace fees expense | Channel clearing | Gross of fee VAT where the fee carries input VAT |
| Fulfilment (FBA) fees, storage, removal | Settlement report | Fulfilment cost (COGS-adjacent or opex by policy) | Channel clearing | Keep apart from referral fees; FBA is a cost of selling |
| Advertising | Settlement report/invoice | Advertising expense | Channel clearing or AP | Often billed, not netted; follow the document |
| Refund (customer) | `Order_Refund`, settlement | Sales returns (contra revenue), Output tax | Channel clearing | Recognise when the refund is processed; restock cost per section on COGS |
| Refund fee returned by channel | Settlement | Channel clearing | Marketplace fees expense | Many marketplaces keep part of the fee on refunds; do not assume full return |
| Payout | Bank statement | Bank | Channel clearing | One journal per payout, match to settlement id |
| Reserve held/released | Settlement | Channel reserve (asset) | Channel clearing | Reserve is not a loss; track separately |
| Chargeback/claim | Settlement | Chargebacks expense (or Sales returns) | Channel clearing | Plus reverse COGS only if goods were recovered |
| Bank charge on payment | `Accounting_Payment.BankCharges` | Merchant/bank fees | PSP clearing | Only if the tenant captures it |

## COGS and stock

- **Perpetual**: on dispatch, Dr COGS, Cr Inventory at moving-average or FIFO cost. Linnworks gives
  `OrderItem.DispatchStockUnitCost` (cost used at dispatch) and `StockChange.ChangeValue`; treat them as a
  subledger to reconcile to, not as the posting if the ledger holds its own costing.
- **Periodic**: Dr COGS for opening plus purchases minus closing stock value. Use `getStockValuation` for closing.
- **Revenue and COGS must share a basis.** Revenue on order date with COGS on dispatch date leaves an in-transit
  mismatch at month end; either align both to dispatch, or accrue COGS for orders placed but not dispatched.
- **Returns**: restocked returns reverse COGS at the original cost; `scrapped` returns do not restore Inventory, they
  expense the cost (write-off). Both come from `getReturns`.
- **FBA / fulfilment-centre stock**: owned inventory sitting in a channel warehouse stays on the balance sheet at cost;
  its Linnworks quantity mirrors channel availability and must not be added to your own warehouse quantity.
- **Landed cost** (freight, duty) is not in Linnworks. Capitalise through the purchase bill or a landed-cost
  allocation, not at the sales order.

## VAT, sales tax and OSS

- Linnworks gives `fTax` per order and `SalesTax`/`TaxRate` per line. It does **not** know the filing treatment.
  Establish per channel: **who collects and remits** (marketplace facilitator vs you). Where the marketplace
  collects and remits, its tax collected is NOT your output tax and must not be posted to your VAT control account;
  record it as a pass-through memo or exclude from revenue (confirm sales are net).
- EU/UK distance-selling: place of supply is the customer's country, so rates differ per destination. Under the EU
  One-Stop Shop scheme, post tax by destination country sub-account and file the OSS return from that, not from the
  home-country VAT account. Order destination is in `searchOrdersFull` (`fkCountryId`, `CountryTaxRate`) and customer
  data; a country-by-country sales extract is the OSS work paper.
- Reverse VAT on refunds at the original rate; partial refunds require line proportion.
- Prices tax-inclusive on the channel but tax-exclusive in the ledger (or vice versa) is the usual reason revenue is
  off by exactly the tax amount.
- This section is accounting practice, not tax advice for a given jurisdiction: confirm thresholds, schemes and rates
  with the client's tax adviser.

## Multi-currency

- Post in transaction currency with the rate at the date of the event; settle the clearing account in the payout
  currency. The difference is realised FX gain/loss. Do not hide it inside sales.
- Revalue open clearing balances at period end (unrealised FX), reversing next period.
- Linnworks reports per-currency rows; `Order.ConversionRate` exists but is the order's rate, not necessarily yours.

## Period-end cut-off checks

1. Orders dispatched after the cut-off but received before: revenue and COGS cut-off per the chosen basis.
2. Refunds created but not actioned: accrue if policy owes them.
3. Settlements spanning the period end: the clearing account balance should equal unsettled sales less unsettled fees.
4. Gift cards and store credit: see the Shopify skill `shopify-gift-cards-and-store-credit` for the liability pattern.

## Common mistakes

- Posting net payouts as revenue: sales understated, fees invisible, VAT wrong.
- One shared clearing account for all channels: unreconcilable.
- Booking marketplace-collected tax as output tax: double VAT.
- Posting FBA fees to marketing.
- Reversing a refund's COGS when the goods were scrapped.
- Forgetting that a channel can charge fees months after the sale (disputes, long-term storage).
