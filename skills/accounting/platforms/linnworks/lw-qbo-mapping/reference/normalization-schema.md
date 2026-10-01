# Normalization schema

The mapping engine never talks to Linnworks/QBO field names directly — everything goes through
these three shapes first. This is what makes the engine reusable for other source/target pairs later
(Shopify→QBO, Linnworks→Xero) without a rewrite: only `normalize.py`'s adapters change.

## SourceRecord (from Linnworks)

```json
{
  "source_system": "linnworks",
  "entity_type": "channel | sku_category | payment_method | refund | shipping | tax | cogs | inventory_adjustment | purchase_order",
  "source_id": "string — stable id within Linnworks (e.g. Source+SubSource, SKU category name, StockItemID)",
  "name": "human label, e.g. 'AMAZON / Acme Co - Amazon'",
  "category": "optional sub-grouping, e.g. SKU category name",
  "subtype": "optional, e.g. payment method type",
  "amount": "decimal, in source currency, for the sampled period — null if this SourceRecord represents a dimension rather than a transaction total",
  "currency": "ISO 4217 code, e.g. USD",
  "date_range": {"from": "ISO date", "to": "ISO date"},
  "channel": "Source/SubSource when entity_type isn't itself the channel",
  "metadata": {"...": "raw fields kept for evidence/audit, e.g. raw Linnworks column values"}
}
```

## AccountingConcept (the translation step coa-mapper-mcp does not have)

This is the layer that turns an ecommerce dimension into an accounting-meaningful concept
*before* any QBO matching happens. Every `SourceRecord` must be classified into exactly one:

```json
{
  "concept": "sales_income | shipping_income | shipping_expense | sales_tax_liability | discount_contra_income | refund_contra_income | cogs | inventory_asset | marketplace_fee_expense | payment_processing_fee_expense | fx_gain_loss | supplier_payable | undetermined",
  "expected_account_type": "Income | Expense | Cost of Goods Sold | Other Current Liability | Current assets | Other Expense | ...",
  "derivation": "which rule in mapping_engine.py assigned this concept, for audit"
}
```

`concept: "undetermined"` is valid and expected — it's what a `SourceRecord` gets when the
ecommerce dimension (e.g. a raw channel name) doesn't map to a single accounting concept without
more context (e.g. "DIRECT" channel could be sales_income of several sub-flavors). Matching against
QBO still proceeds using `entity_type` + name signals, just without the `expected_account_type` guard,
which caps confidence at `MEDIUM`.

## TargetRecord (from QuickBooks)

```json
{
  "target_system": "qbo",
  "entity_type": "account | item | class | tax_code | customer | vendor",
  "target_id": "QBO Id",
  "name": "QBO Name / FullyQualifiedName",
  "account_type": "QBO AccountType, e.g. Income, Expense, Cost of Goods Sold, Other Current Liability",
  "subtype": "QBO AccountSubType or Item Type",
  "active": true,
  "metadata": {"...": "raw QBO fields kept for evidence/audit"}
}
```

## MappingResult (engine output — one per SourceRecord)

```json
{
  "source": "SourceRecord (or its source_id/name for a compact report row)",
  "source_type": "SourceRecord.entity_type",
  "source_value": "SourceRecord.amount + currency, or null for dimension-only records",
  "target": "TargetRecord.name, or null",
  "target_type": "TargetRecord.entity_type + account_type, or null",
  "status": "MAPPED | UNMAPPED | AMBIGUOUS | INVALID | ORPHANED | INACTIVE | STRUCTURAL_DATA_GAP",
  "confidence": "HIGH | MEDIUM | LOW | UNRESOLVED",
  "evidence": ["ordered list of which pipeline step(s) fired and why"],
  "reason": "one-line human-readable explanation",
  "review_required": true
}
```

`ORPHANED` results are produced the other direction — iterating QBO `TargetRecord`s that no
`MappingResult.target` ever points at — and use the same shape with `source=null`.
