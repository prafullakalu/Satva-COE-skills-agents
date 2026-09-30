"""
Normalize raw Linnworks / QBO MCP tool output into SourceRecord / TargetRecord shapes.

This module has NO network/MCP calls in it on purpose — it is a pure transform so it can be
unit-tested with fixtures and so the calling agent stays in control of which MCP tools to call.
The agent (SKILL.md) is responsible for fetching raw JSON via the MCP tools and passing it here.

See reference/normalization-schema.md for the target shapes.
"""
from __future__ import annotations
import re
from dataclasses import dataclass, field, asdict
from typing import Any, Optional


@dataclass
class SourceRecord:
    source_system: str
    entity_type: str
    source_id: str
    name: str
    amount: Optional[float] = None
    currency: Optional[str] = None
    category: Optional[str] = None
    subtype: Optional[str] = None
    channel: Optional[str] = None
    date_range: Optional[dict] = None
    sku: Optional[str] = None       # product-identity matching (spec: SKU is priority-1 evidence)
    qty: Optional[float] = None     # per-location or owned_total only -- never a cross-location sum
    metadata: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class TargetRecord:
    target_system: str
    entity_type: str
    target_id: str
    name: str
    account_type: Optional[str] = None
    subtype: Optional[str] = None
    active: bool = True
    sku: Optional[str] = None       # QBO Item.Sku, when entity_type == "item"
    unit_price: Optional[float] = None  # QBO Item.UnitPrice
    qty: Optional[float] = None     # QBO Item.QtyOnHand
    metadata: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return asdict(self)


# ---------------------------------------------------------------------------
# Linnworks adapters
# ---------------------------------------------------------------------------

def from_channel_breakdown(items: list[dict], date_range: Optional[dict] = None) -> list[SourceRecord]:
    """getChannelBreakdown result items -> one SourceRecord per (channel, sub_source, currency) row.

    NEVER sums across currency rows (per the Linnworks MCP's own instruction) — each row stays a
    separate SourceRecord so downstream coverage/reconciliation never silently mixes currencies.
    """
    out = []
    for it in items:
        source_id = f"{it['channel']}|{it.get('sub_source', '')}|{it['currency']}"
        out.append(SourceRecord(
            source_system="linnworks",
            entity_type="channel",
            source_id=source_id,
            name=(it.get("sub_source") or it["channel"]),
            amount=it.get("revenue"),
            currency=it.get("currency"),
            channel=it["channel"],
            date_range=date_range,
            metadata=it,
        ))
    return out


def from_order_refunds(items: list[dict], date_range: Optional[dict] = None) -> list[SourceRecord]:
    out = []
    for it in items:
        out.append(SourceRecord(
            source_system="linnworks",
            entity_type="refund",
            source_id=it.get("pkRefundRowId") or it.get("return_id") or it.get("order_id", ""),
            name="Refund" + (f" ({it['Reason']})" if it.get("Reason") else ""),
            amount=it.get("Amount") or it.get("amount"),
            currency=it.get("currency"),
            date_range=date_range,
            metadata=it,
        ))
    return out


def from_stock_items(items: list[dict], qty_by_sku: Optional[dict] = None) -> list[SourceRecord]:
    """Accepts either raw StockItem table rows (ItemNumber/ItemTitle/RetailPrice) or
    getProductBySku/searchStockItems-shaped dicts (sku/title/retail_price). entity_type="sku"
    marks these as product-identity records for mapping_engine.match_product_identity(), distinct
    from the generic accounting-concept "sku" rows used by propose_mapping() for COGS-account
    matching -- both share entity_type="sku" but are consumed by different engine functions.
    qty_by_sku: optional {sku: owned_total_qty} from getStockItem/getStockLevels (never a
    cross-location sum -- pass owned_total or a single location's quantity only).
    """
    qty_by_sku = qty_by_sku or {}
    out = []
    for it in items:
        sku = it.get("sku") or it.get("ItemNumber") or it.get("SKU", "")
        out.append(SourceRecord(
            source_system="linnworks",
            entity_type="sku",
            source_id=sku or it.get("pkStockItemID", ""),
            name=it.get("title") or it.get("ItemTitle") or it.get("ItemNumber", ""),
            category=it.get("category") or it.get("category_name") or it.get("CategoryId"),
            amount=it.get("retail_price") if "retail_price" in it else it.get("RetailPrice"),
            sku=sku or None,
            qty=qty_by_sku.get(sku),
            metadata=it,
        ))
    return out


# ---------------------------------------------------------------------------
# QBO adapters
# ---------------------------------------------------------------------------

def from_qbo_account_list(rows: list[dict]) -> list[TargetRecord]:
    """rows: [{"account_name": ..., "account_type": ..., "account_sub_type": ...}, ...]
    (already flattened from the AccountList report's ColData pairs by the caller)
    """
    out = []
    for i, r in enumerate(rows):
        out.append(TargetRecord(
            target_system="qbo",
            entity_type="account",
            target_id=r.get("id", str(i)),
            name=r["account_name"],
            account_type=r.get("account_type"),
            subtype=r.get("account_sub_type"),
            active=r.get("active", True),
            metadata=r,
        ))
    return out


def from_qbo_items(items: list[dict]) -> list[TargetRecord]:
    out = []
    for it in items:
        out.append(TargetRecord(
            target_system="qbo",
            entity_type="item",
            target_id=it.get("Id", ""),
            name=it.get("FullyQualifiedName") or it.get("Name", ""),
            account_type=it.get("Type"),
            subtype=(it.get("IncomeAccountRef") or {}).get("name"),
            active=it.get("Active", True),
            sku=it.get("Sku") or None,
            unit_price=it.get("UnitPrice"),
            qty=it.get("QtyOnHand"),
            metadata=it,
        ))
    return out


def flatten_account_list_report(report_json: dict) -> list[dict]:
    """Flatten the raw QBO AccountList Report JSON (Header/Columns/Rows) into
    [{"account_name": ..., "account_type": ...}, ...]. Handles the shape returned by
    get_account_list when it returns the raw report object rather than pre-rendered text.
    """
    rows = report_json.get("Rows", {}).get("Row", [])
    out = []
    for row in rows:
        cols = row.get("ColData", [])
        if len(cols) >= 2:
            out.append({"account_name": cols[0].get("value", ""), "account_type": cols[1].get("value", "")})
    return out


# ---------------------------------------------------------------------------
# File-input mode: dict rows from an XLSX/CSV export (tolerant header aliases)
# ---------------------------------------------------------------------------

def _pick(row: dict, *aliases: str):
    """First non-blank value whose header matches an alias (case/space/punctuation-insensitive)."""
    norm = {re.sub(r"[^a-z0-9]", "", str(k).lower()): v for k, v in row.items()}
    for a in aliases:
        v = norm.get(a)
        if v is not None and str(v).strip() != "":
            return v
    return None


def _txt(v) -> Optional[str]:
    if v is None:
        return None
    if isinstance(v, float) and v.is_integer():
        v = int(v)
    return str(v).strip() or None


def _num(v) -> Optional[float]:
    try:
        return float(str(v).replace(",", "").replace("$", "").strip())
    except (TypeError, ValueError):
        return None


def from_lw_export_rows(rows: list[dict]) -> list[SourceRecord]:
    """Linnworks stock export rows (SKU/ItemSKU, Name/Product Name/Title, Qty/Quantity/Stock, Price...)."""
    out = []
    for r in rows:
        sku = _txt(_pick(r, "sku", "itemsku", "itemnumber"))
        name = _txt(_pick(r, "name", "productname", "title", "itemtitle", "itemname")) or ""
        if not sku and not name:
            continue
        out.append(SourceRecord(
            source_system="linnworks", entity_type="sku", source_id=sku or name, name=name,
            category=_txt(_pick(r, "category", "categoryname")),
            amount=_num(_pick(r, "price", "retailprice", "salesprice")),
            sku=sku, qty=_num(_pick(r, "qty", "quantity", "stock", "stocklevel", "instock", "qtyonhand")),
            metadata=dict(r)))
    return out


def from_qbo_export_rows(rows: list[dict]) -> list[TargetRecord]:
    """QBO product/service export rows. NB the 'SKU' column may really be the Item ID: keep it in
    `sku` as exported and let mapping_engine.detect_sku_key() decide."""
    out = []
    for i, r in enumerate(rows):
        name = _txt(_pick(r, "name", "fullyqualifiedname", "itemname", "productname", "productservicename", "title"))
        if not name:
            continue
        act = str(_pick(r, "active", "status") or "true").strip().lower()
        out.append(TargetRecord(
            target_system="qbo", entity_type="item", target_id=_txt(_pick(r, "id", "itemid")) or str(i),
            name=name, account_type=_txt(_pick(r, "type", "itemtype")),
            active=act not in ("false", "no", "0", "inactive"),
            sku=_txt(_pick(r, "sku", "itemsku")),
            unit_price=_num(_pick(r, "unitprice", "price", "salesprice", "rate")),
            qty=_num(_pick(r, "qtyonhand", "qty", "quantity", "quantityonhand", "stock")),
            metadata=dict(r)))
    return out
