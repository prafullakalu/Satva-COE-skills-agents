---
name: lw-qbo-mapping
description: >
  Analyze Linnworks ecommerce/operational data and QuickBooks Online accounting data for a given
  period, map Linnworks dimensions (channel, SKU, refunds, shipping, tax, payment method) to QBO
  accounting objects (accounts, items), identify mapping/data gaps, compute count+value coverage,
  and reconcile Linnworks totals against QBO totals. READ-ONLY. Trigger on "analyze my Linnworks
  and QuickBooks data", "mapping health report", "gap analysis Linnworks QBO", "update my mapping
  workbook", "what needs my decision", or /lw-qbo-mapping.
metadata:
  department: "accounting"
  domain: "integration-mapping"
  platform: "linnworks,quickbooks"
  owner: "satva-coe"
  status: "stable"
  license: "Satva-original"
  source: "original"
---

# Linnworks -> QuickBooks Data Mapping & Gap Analysis

## Quick run (default for accountants — start here)

The user may be a non-technical accountant. Talk plain accounting English (see `reference/glossary.md`;
never say UNVERIFIED/AMBIGUOUS/SKU — say "couldn't confirm", "product code"). Never ask for
credentials: both systems come through the connected MCP servers (or the user's export files).

1. **Both systems, always.** Fetch from BOTH Linnworks and QuickBooks (tool map in Step 3). If either
   is unavailable, say which one and stop — never report from one side.
2. **Save the data** as JSON (raw MCP output) or use the user's `.xlsx`/`.csv` exports.
3. **One command** (needs `openpyxl`; `pip install openpyxl` if missing):
   `python scripts/run_analysis.py --client "<Client Name>" --lw <lw file> --qbo <qbo file> [--mcp] [--period "<label>"]`
   `--mcp` = the JSON files are raw MCP tool output; omit for export rows.
4. **It writes to `~/LW-QBO-Mapping/<client>/`** (never the repo): `workbook.xlsx` (his control panel and
   the skill's memory) and `summary.csv`. Re-running updates the same workbook: his Approve/Reject/Change
   picks are kept and learned, nothing he typed is overwritten, a backup is taken first.
5. **Tell him** the printed headline, where the workbook is, and to open **Start Here** then **Needs Your
   Decision**. If the run says Excel has the file open, relay the `_pending` instruction verbatim.

New client = new `--client` name; nothing carries over between clients. Everything below is the detailed
method the script implements plus the account/channel mapping and reconciliation it does not yet automate.

## Hard rules (read first)

- **READ-ONLY.** This skill never calls a write tool on either MCP server (no `create_*`,
  `update_*`, `delete_*`, `void_*` QBO tools; Linnworks MCP is read-only by construction). If asked
  to "fix" or "apply" a mapping, propose it in the report and stop — do not call a write tool.
- **Never fabricate MCP capability.** If a tool doesn't exist or a call errors, report it under
  Data Gaps / Data Availability Gap. Never invent a plausible-sounding number.
- **Never silently merge currencies.** Every Linnworks money figure comes tagged with a currency
  (see MCP server notes: rows in `getChannelBreakdown`/`getRevenueSummary` are per-currency).
  Keep coverage and reconciliation grouped by currency; never sum two currencies into one total.
- **Never sum Linnworks stock across locations** (FBA/fulfilment locations mirror availability).
- **An LLM proposal is never a confirmed mapping.** Confidence caps at `MEDIUM`,
  `review_required=true`, always. See `reference/confidence-model.md`.
- **If the connected QBO company looks unrelated to the Linnworks business** (different industry,
  no channel-matching account names at all), say so explicitly in the report's Overall section
  before quoting a coverage percentage — a low/zero coverage number against a mismatched company is
  a data-scoping finding, not proof the mapping engine failed.

## Flow

```
1. IDENTIFY SCOPE     -> period, which QBO company (list_companies), Linnworks account (fixed by credential)
2. DISCOVER           -> confirm which MCP tools actually answer each data need (do not assume)
3. FETCH              -> call the MCP tools for the period
4. NORMALIZE          -> scripts/normalize.py adapters: raw JSON -> SourceRecord[] / TargetRecord[]
5. MAP (accounts)     -> scripts/mapping_engine.py propose_mapping() per SourceRecord (steps 1-6);
                          for UNRESOLVED results where entity_type is NOT already a known structural
                          gap, optionally reason step 8 (LLM) yourself and call apply_llm_proposal()
5b. MAP (products)     -> scripts/mapping_engine.py match_product_identity() per Linnworks StockItem,
                          SKU-first: SKU exact match -> product name overlap -> price/qty as
                          corroboration ONLY (never the primary signal). See "Product/SKU matching"
                          below and reference/confidence-model.md's dedicated pipeline section.
6. VALIDATE            -> scripts/mapping_engine.py find_orphaned_targets() / find_orphaned_products()
7. COVERAGE            -> scripts/coverage.py coverage_report() for BOTH the account mapping and the
                          product mapping separately (count AND value, per currency)
8. DATA GAPS           -> reference/gap-taxonomy.md source-availability grading, from what step 3
                          actually returned (or didn't)
9. RECONCILE           -> scripts/reconcile.py reconcile_many() comparing Linnworks totals
                          (getRevenueSummary etc.) to QBO totals (get_profit_and_loss /
                          get_trial_balance / run_report), same period, same currency
10. CONCLUDE            -> scripts/conclusions.py derive_conclusions() — deterministic, templated
                          interpretation of the numbers above (never free-text LLM narrative
                          disconnected from the computed facts)
11. REPORT             -> scripts/report.py render_report(), passing product_results/
                          product_coverage/conclusions so the report includes the full Category
                          Summary table (every status bucket, count AND value) and Key Findings
```

Run scripts via `python -c` or a short driver script inside `scripts/`; they are pure functions
with no I/O, so you assemble the JSON payloads from MCP tool results yourself, in-conversation.

## Step 1-2: Scope and discovery

- Call `mcp__satva-quickbooks__list_companies` to see which QBO companies are connected. If more
  than one, ask the user which one corresponds to the Linnworks account (do not guess a client
  match).
- The Linnworks side is fixed by the connected credential — there's no tenant selection.
- Call `mcp__satva-linnworks-read-only__listTables` once per session to confirm which tables are
  actually allowlisted before assuming an entity is queryable (e.g. `Accounting_PaymentType` may
  legitimately have 0 rows — verify via `getPaymentTypes`/`row_count` in `listTables`, don't assume
  payment-method data exists just because the table is listed).

## Step 3: Fetch — tool -> entity map (verified against this project's actual MCP schemas)

| Need | Linnworks tool | QBO tool |
|---|---|---|
| Channel/sales revenue split | `getChannelBreakdown`, `getRevenueSummary` | `get_profit_and_loss`, `get_class_sales` (if classes used for channel) |
| Orders + lines | `searchOrders` -> `getOrderItems` / `dumpJoined(Order, OrderItem)` | `search_sales_receipts`, `search_invoices`, `query_quickbooks` |
| Refunds | `getOrderRefunds` (needs date or order filter) | `search_refund_receipts`, `search_credit_memos` |
| Returns | `getReturns` | (no direct QBO equivalent — returns are a Linnworks-only concept; note as a translation gap) |
| Payment methods | `getPaymentTypes`, `getPaymentHistory`, `getPayments` | `search_payments`, `get_transaction_list` |
| SKU / inventory / COGS | `searchStockItems`, `getStockItem`, `getStockValuation` | `search_items`, `get_inventory_valuation_summary` |
| Chart of accounts (targets) | n/a | `get_account_list` (flatten via `normalize.flatten_account_list_report` if raw report JSON) or `search_accounts` |
| Tax | Order table `fTax`/`CountryTaxRate` via `searchOrders`/`dumpTable` | `get_tax_summary` |
| Shipping | Order table `fPostageCost`/`PostageCostExTax` | no dedicated shipping report — derive from `get_profit_and_loss` account rows if a Shipping Income/Expense account exists |
| Suppliers / purchase orders | `getSuppliers`, `getPurchaseOrders`, `getPurchaseOrderItems` | `search_vendors`, `search_bills`, `search_purchase_orders` |
| Marketplace fees / settlements | **not present** — see Data Gaps | n/a (would show as a manually-entered Expense if the client books it) |

## Step 8: Data Gaps — apply the grading in `reference/gap-taxonomy.md`

Known structural gap (confirmed by schema inspection, not assumed): Linnworks' `Order` /
`OrderItem` / `Order_Refund` tables carry subtotal/tax/postage/discount breakdowns per order, but
**no marketplace-fee or payment-processor-fee field anywhere in the allowlisted schema** —
those settle outside Linnworks (Seller Central, PSP dashboards). Grade this
`SOURCE_NOT_AVAILABLE` for `marketplace_fee_expense` / `payment_processing_fee_expense` concepts
every time, don't re-derive it live unless the schema has changed.

## Step 5b: Product / SKU matching (Linnworks StockItem -> QBO Item)

Separate from the channel/account mapping above — this answers "does this specific product exist,
correctly, in QBO?" not "which account does the revenue post to?". Priority order, per requirement:

1. **SKU exact match** (case-insensitive) — the strongest possible signal, `HIGH` confidence.
2. **Product name** overlap — a real but unconfirmed candidate on its own (`UNVERIFIED`).
3. **Price/qty** — corroboration only. Within `PRICE_TOLERANCE_PCT` (default 5%) of a name-matched
   candidate elevates it to `MAPPED`/`MEDIUM`, or breaks a tie between 2+ name-matched candidates.
   Price/qty **never** promotes a match on its own — two unrelated products can share a price.

Get Linnworks products via `searchStockItems`/`getProductBySku`/`getStockLevels` (never sum
quantity across locations — pass `owned_total` or a single location only). Get QBO items via
`search_items` (carries `Sku`, `UnitPrice`, `QtyOnHand` when present). Call
`normalize.from_stock_items()` / `normalize.from_qbo_items()` then `mapping_engine.
match_product_identity()` per product, then `find_orphaned_products()` for QBO items nothing
selected.

## Step 10: Report

Use `scripts/report.py render_report()`. Always populate `data_source_note` when the QBO company
is a generic/demo/unrelated company relative to the Linnworks business — state that plainly instead
of letting a 0% coverage number stand unexplained.

Always pass `product_results`/`product_coverage` (from step 5b/7) and `conclusions` (from step
10/`conclusions.py`) so the report includes:
- The **Category Summary** table — every status (MAPPED/UNMAPPED/AMBIGUOUS/UNVERIFIED/INVALID/
  INACTIVE/STRUCTURAL_DATA_GAP/ORPHANED), with both count and value, in one place — not just the
  headline mapped/unmapped numbers.
- The **Product / SKU Matching** table, separate from the account Mapping Matrix.
- **Key Findings / Conclusions** — what the numbers mean, always generated by `conclusions.py`
  (deterministic, traces to the computed facts), never freehand text disconnected from the report's
  own numbers.

## Step 12: xlsx export — inventory matching (on request)

When the user wants a spreadsheet specifically for **inventory management** ("xlsx", "excel",
"diff file", "spreadsheet" in the context of products/SKUs/inventory), call
`scripts/export_xlsx.py save_inventory_workbook()` with the product-matching inputs from step 5b
(`sources`=Linnworks StockItem `SourceRecord[]`, `targets`=QBO Item `TargetRecord[]`,
`results`=`match_product_identity()` outputs, `orphan_results`=`find_orphaned_products()` output).
This is narrower than the full markdown report on purpose — two sheets only:

1. **Matched Products** — Linnworks SKU/product name next to QBO SKU/product name and the QBO
   chart-of-accounts object it posts to (Asset/Income/COGS, pulled from the Item's
   `AssetAccountRef`/`IncomeAccountRef`/`ExpenseAccountRef`), for rows where identity is confirmed
   (`status == MAPPED`). For those rows only, price and on-hand quantity are compared as a
   **post-match verification** (never part of the match decision itself) and flagged
   MATCH/MISMATCH/N/A — N/A when either side's value wasn't available, never fabricated.
2. **Unmatched - Needs Review** — everything else, using a single coarse `Status` column with
   exactly four values (no free-text reason column, no confidence column): `Missing in QBO`
   (Linnworks product, no QBO item at all — was `UNMAPPED`), `Missing in Linnworks` (QBO item, no
   Linnworks product — was `ORPHANED`), or `Unmatched` (some candidate exists but couldn't be
   confirmed — was `AMBIGUOUS`/`UNVERIFIED`/`INACTIVE`/`INVALID`). Mapping is
   `export_xlsx.COARSE_STATUS`.

Requires `openpyxl` (already available in this environment; `report.py`'s markdown output has no
such dependency and always works as a fallback).

## Testing

`python -m unittest discover -s tests -v` from the skill root. Covers the 16 spec-mandated cases
(exact/semantic mapping, type mismatch, missing/ambiguous/inactive target, orphan, structural gap,
count/value coverage, reconciliation variance, currency, refund/tax/shipping mismatch, marketplace
fee gap) plus the product/SKU-matching pipeline (SKU exact, duplicate SKU, name-only unverified,
name+price corroboration, price-broken tie, orphaned product) and the conclusions generator — all
synthetic fixtures, marked as such; no live MCP calls happen in tests.
