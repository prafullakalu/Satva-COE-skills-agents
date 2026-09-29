"""
Renders the structured markdown report (spec #10). Pure formatting — no calculation happens here;
everything it prints must have come from coverage.py / reconcile.py / mapping_engine.py already.
"""
from __future__ import annotations
from mapping_engine import MappingResult
from reconcile import ReconciliationRow


def render_report(
    period: str,
    coverage: dict,
    mapping_results: list[MappingResult],
    data_gaps: list[dict],
    reconciliation_rows: list[ReconciliationRow],
    unresolved_notes: list[str],
    data_source_note: str = "",
    product_results: list[MappingResult] | None = None,
    product_coverage: dict | None = None,
    conclusions: list[str] | None = None,
) -> str:
    lines = []
    lines.append("# Linnworks -> QuickBooks Data Mapping Health\n")
    lines.append(f"Period: {period}\n")
    if data_source_note:
        lines.append(f"> {data_source_note}\n")

    lines.append("## Overall\n")
    lines.append(f"- Mapping coverage (count): {_fmt_pct(coverage['count_coverage_pct'])}")
    lines.append(f"- Value coverage: {_fmt_pct(coverage['value_coverage_pct'])}")
    lines.append(f"- Mapped: {coverage['mapped_count']}")
    lines.append(f"- Unmapped: {coverage['unmapped_count']}")
    lines.append(f"- Ambiguous: {coverage['ambiguous_count']}")
    lines.append(f"- Invalid: {coverage['invalid_count']}")
    lines.append(f"- Inactive: {coverage.get('inactive_count', 0)}")
    lines.append(f"- Unverified: {coverage.get('unverified_count', 0)}")
    lines.append(f"- Structural gaps: {coverage['structural_gap_count']}")
    lines.append(f"- Orphaned QBO targets: {coverage['orphaned_count']}")
    lines.append(f"- Total value in scope: {coverage['total_value']}")
    lines.append(f"- Mapped value: {coverage['mapped_value']}")
    lines.append(f"- Unmapped value: {coverage['unmapped_value']}\n")

    if coverage["largest_financial_gaps"]:
        lines.append("### Largest financial gaps\n")
        for i, r in enumerate(coverage["largest_financial_gaps"], 1):
            lines.append(f"{i}. {r.source_name} ({r.status}) — {r.source_value} {r.currency or ''}")
        lines.append("")

    if conclusions:
        lines.append("## Key Findings / Conclusions\n")
        for c in conclusions:
            lines.append(f"- {c}")
        lines.append("")

    lines.append("## Category Summary\n")
    lines.append("Every source and target record lands in exactly one row below — this is the complete")
    lines.append("breakdown behind the coverage percentages, not just the headline numbers.\n")
    lines.append("| Category | Meaning | Count | Value |")
    lines.append("|---|---|---:|---:|")
    cat_meaning = {
        "mapped_count": ("MAPPED", "Confirmed correspondence, active + type-compatible target"),
        "unmapped_count": ("UNMAPPED", "No candidate target found at all"),
        "ambiguous_count": ("AMBIGUOUS", "2+ equally-plausible targets, no tiebreaker"),
        "unverified_count": ("UNVERIFIED", "One candidate found, evidence insufficient to confirm"),
        "invalid_count": ("INVALID", "Mapping exists but target is structurally wrong"),
        "inactive_count": ("INACTIVE", "Mapping points at a non-usable (inactive) target"),
        "structural_gap_count": ("STRUCTURAL_DATA_GAP", "Source system doesn't carry this data at all"),
        "orphaned_count": ("ORPHANED", "QBO target with no corresponding Linnworks source"),
    }
    cat_values = _category_values(mapping_results + (product_results or []))
    for key, (label, meaning) in cat_meaning.items():
        lines.append(f"| {label} | {meaning} | {coverage.get(key, 0)} | {cat_values.get(label, 0)} |")
    lines.append("")

    lines.append("## Mapping Matrix (Channel / Refund / Tax -> QBO Account)\n")
    lines.append("| Linnworks Source | Source Type | QBO Target | Target Type | Status | Confidence | Evidence |")
    lines.append("|---|---|---|---|---|---|---|")
    for r in mapping_results:
        row = r.to_row()
        lines.append(
            f"| {row['linnworks_source']} | {row['source_type']} | {row['qbo_target'] or '-'} | "
            f"{row['target_type'] or '-'} | {row['status']} | {row['confidence']} | {row['evidence']} |"
        )
    lines.append("")

    if product_results:
        lines.append("## Product / SKU Matching (Linnworks StockItem -> QBO Item)\n")
        lines.append("Matched in priority order: SKU exact match, then product name, then price/qty as")
        lines.append("corroboration only (price/qty alone never confirms a match on its own).\n")
        if product_coverage:
            lines.append(f"- Product count coverage: {_fmt_pct(product_coverage.get('count_coverage_pct'))}")
            lines.append(f"- Product value coverage: {_fmt_pct(product_coverage.get('value_coverage_pct'))}\n")
        lines.append("| Linnworks SKU | Product Name | QBO Item | Status | Confidence | Evidence |")
        lines.append("|---|---|---|---|---|---|")
        for r in product_results:
            row = r.to_row()
            lines.append(
                f"| {r.source_id or '-'} | {row['linnworks_source']} | {row['qbo_target'] or '-'} | "
                f"{row['status']} | {row['confidence']} | {row['evidence']} |"
            )
        lines.append("")

    lines.append("## Data Gaps\n")
    lines.append("| Gap | Source | Required Accounting Concept | Severity | Financial Impact | Explanation |")
    lines.append("|---|---|---|---|---|---|")
    for g in data_gaps:
        lines.append(
            f"| {g['gap']} | {g['source']} | {g['required_concept']} | {g['severity']} | "
            f"{g.get('financial_impact', 'n/a')} | {g['explanation']} |"
        )
    lines.append("")

    lines.append("## Reconciliation\n")
    lines.append("| Category | Linnworks | QBO | Variance | Variance % | Status |")
    lines.append("|---|---:|---:|---:|---:|---|")
    for row in reconciliation_rows:
        d = row.to_row()
        lines.append(
            f"| {d['category']} | {d['linnworks']} {d['currency']} | {d['qbo']} {d['currency']} | "
            f"{d['variance']} | {d['variance_pct']} | {d['status']} |"
        )
    lines.append("")

    lines.append("## Unresolved Items\n")
    if unresolved_notes:
        for n in unresolved_notes:
            lines.append(f"- {n}")
    else:
        lines.append("- None.")

    return "\n".join(lines) + "\n"


def _fmt_pct(v):
    return f"{v}%" if v is not None else "n/a (no valued records in scope)"


def _category_values(results: list[MappingResult]) -> dict:
    out: dict[str, float] = {}
    for r in results:
        if r.status == "ORPHANED" or r.source_value is None:
            continue
        out[r.status] = round(out.get(r.status, 0) + abs(r.source_value), 2)
    return out
