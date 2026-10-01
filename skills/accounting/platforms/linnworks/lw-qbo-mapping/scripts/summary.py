"""
Summary metrics: the ordered (Metric, Value) list an analyst hands over, plus CSV writer.
Client-agnostic; every number is counted from already-computed results (no matching here).
"""
from __future__ import annotations
import csv
import plain
from mapping_engine import MappingResult, inventory_totals_check


def summary_metrics(scope: str, sku_key_info: dict, sources: list, targets: list,
                    results: list[MappingResult], data_gaps: list | None = None, *,
                    plain: bool = False) -> list[tuple]:
    """results: match_product_identity results plus find_orphaned_products rows (ORPHANED).
    sku_key_info: detect_sku_key() output. data_gaps: data_gap_findings() output.
    plain=True: same numbers in accountant wording (no jargon); lines sum to the Linnworks total."""
    key = sku_key_info.get("sku_key_source", "sku")
    dq = sku_key_info.get("data_quality", [])
    rel = [r for r in results if r.status != "ORPHANED"]
    n = lambda st: sum(1 for r in rel if r.status == st)
    items = [t for t in targets if t.entity_type == "item"]
    src_by = {s.source_id: s for s in sources}
    tgt_by = {t.target_id: t for t in items}
    exact = [r for r in rel if r.status == "MAPPED" and "SKU exact match" in r.evidence]
    qty_ok = qty_bad = 0
    for r in exact:
        a, b = getattr(src_by.get(r.source_id), "qty", None), getattr(tgt_by.get(r.target_id), "qty", None)
        if a is not None and b is not None:
            qty_ok, qty_bad = (qty_ok + 1, qty_bad) if a == b else (qty_ok, qty_bad + 1)
    tot = inventory_totals_check(sources, targets)
    label = {"name": "SKU exact match: LW SKU = QBO Item Name (Matched)"}.get(key, "SKU exact match (Matched)")
    approved = sum(1 for r in rel if r.status == "MAPPED" and any("approved by accountant" in e for e in r.evidence))
    pct = f"{round(len(exact) / len(rel) * 100, 1)}%" if rel else "n/a"
    if plain:
        return _plain_metrics(scope, key, dq, sources, items, tot, rel, exact, qty_ok, qty_bad, approved, pct,
                              sum(1 for r in results if r.status == "ORPHANED"), data_gaps)
    m: list[tuple] = [("Scope", scope)]
    if key != "sku" or dq:
        msg = [d["detail"] for d in dq] + ([f"Matching uses QBO {key} as the SKU key."] if key != "sku" else [])
        m.append(("Key finding", " ".join(msg)))
    m += [
        ("", ""),
        ("Linnworks active products", len(sources)),
        ("QBO inventory items", len(items)),
        ("Difference (LW - QBO)", len(sources) - len(items)),
        ("Linnworks total on-hand qty (as exported)", tot["lw_total_qty"]),
        ("QBO total qty on hand", tot["qbo_total_qty"]),
        ("", ""),
        (label, len(exact)),
        ("   of which qty MATCH", qty_ok),
        ("   of which qty MISMATCH", qty_bad),
        *([("Approved by accountant (Matched)", approved)] if approved else []),
        ("Name overlap only - needs review (UNVERIFIED)", n("UNVERIFIED")),
        ("Multiple candidates (AMBIGUOUS)", n("AMBIGUOUS")),
        ("Missing in QBO (UNMAPPED)", n("UNMAPPED")),
        ("Missing in Linnworks (QBO orphan)", sum(1 for r in results if r.status == "ORPHANED")),
        ("SKU match coverage (count)", pct),
        ("", ""),
        ("Exact name match, SKU differs", sum(1 for r in rel if "exact_name_sku_differs" in r.evidence)),
        ("Near SKU match (case/spacing/punctuation/leading zeros)",
         sum(1 for r in rel if "near SKU match (normalized)" in r.evidence)),
    ]
    gaps = [g["detail"] for g in (data_gaps or [])]
    if gaps:
        m.append(("", ""))
        m += [("Data gaps" if i == 0 else "", d) for i, d in enumerate(gaps)]
    return m


def _plain_metrics(scope, key, dq, sources, items, tot, rel, exact, qty_ok, qty_bad, approved, pct, orphans, data_gaps):
    n = lambda st: sum(1 for r in rel if r.status == st)
    has = lambda tag: sum(1 for r in rel if r.status == "MAPPED" and tag in r.evidence)
    near, inactive = has("near SKU match (normalized)"), n("INACTIVE")
    name_only, several, missing = n("UNVERIFIED"), n("AMBIGUOUS"), n("UNMAPPED")
    parts = [len(exact), near, approved, name_only, several, missing, inactive]
    msg = [plain.gap_text(d) for d in dq] + (["Products were matched using the QuickBooks item name as the product code."]
                                             if key != "sku" and not dq else [])
    m: list[tuple] = [("Scope", scope)]
    if msg:
        m.append(("Key finding", " ".join(msg)))
    m += [
        ("", ""),
        ("Linnworks active products", len(sources)),
        ("QuickBooks inventory items", len(items)),
        ("Difference (Linnworks minus QuickBooks)", len(sources) - len(items)),
        ("Linnworks total quantity on hand (as exported)", tot["lw_total_qty"]),
        ("QuickBooks total quantity on hand", tot["qbo_total_qty"]),
        ("", ""),
        ("Products matched by product code", len(exact)),
        ("   of which quantity agrees", qty_ok),
        ("   of which quantity differs", qty_bad),
        ("Products matched by a nearly identical product code (spacing, capitals or zeros differ)", near),
        *([("Matched because you approved them", approved)] if approved else []),
        ("Products matched by name only - please confirm", name_only),
        ("   of which the name is identical but the product code differs",
         sum(1 for r in rel if "exact_name_sku_differs" in r.evidence)),
        ("Products with several possible matches", several),
        ("Products missing in QuickBooks", missing),
        *([("Products found in QuickBooks but switched off", inactive)] if inactive else []),
        ("All Linnworks products counted above (equals Linnworks active products)", sum(parts)),
        ("", ""),
        ("Items only in QuickBooks (not part of the total above)", orphans),
        ("Product code check: share of products matched by product code", pct),
    ]
    gaps = [plain.gap_text(g) for g in (data_gaps or [])]
    if gaps:
        m.append(("", ""))
        m += [("Data gaps" if i == 0 else "", d) for i, d in enumerate(gaps)]
    return m


def save_summary_csv(path: str, metrics: list[tuple]) -> str:
    with open(path, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["Metric", "Value"])
        w.writerows(metrics)
    return path
