"""
Deterministic "what does this mean" synthesis over already-computed facts.

Every bullet here must trace to a number produced by coverage.py/reconcile.py/mapping_engine.py --
this module does no matching or arithmetic of its own, only interpretation rules over results
already computed. Keeps "conclusions" auditable instead of free-text LLM narrative that can't be
checked against the underlying data (spec #18: LLM for semantic reasoning, not arithmetic --
and conclusions here are neither; they're templated interpretation of numbers already proven).
"""
from __future__ import annotations

COUNT_VALUE_DIVERGENCE_PCT = 15.0  # count vs value coverage gap this large gets its own callout


def derive_conclusions(coverage: dict, product_coverage: dict | None = None,
                        reconciliation_rows: list | None = None, data_gaps: list | None = None) -> list[str]:
    out: list[str] = []
    reconciliation_rows = reconciliation_rows or []
    data_gaps = data_gaps or []

    # --- count vs value coverage divergence (spec #8's core warning) ---
    cc, vc = coverage.get("count_coverage_pct"), coverage.get("value_coverage_pct")
    if cc is not None and vc is not None:
        gap = cc - vc
        if gap >= COUNT_VALUE_DIVERGENCE_PCT:
            out.append(
                f"Count coverage ({cc}%) is materially higher than value coverage ({vc}%) — "
                f"a {round(gap, 1)} point gap. The unmapped records are disproportionately large "
                f"in dollar terms; a per-record count alone would understate the real financial exposure."
            )
        elif vc > cc + COUNT_VALUE_DIVERGENCE_PCT:
            out.append(
                f"Value coverage ({vc}%) exceeds count coverage ({cc}%) — the unmapped records "
                f"skew small individually, but there are many of them ({coverage.get('unmapped_count', 0)})."
            )
        elif cc == 0 and vc == 0 and coverage.get("total_count", 0) > 0:
            out.append(
                "Zero mapping coverage on both count and value. Before treating this as an engine "
                "failure, check the Data Scoping note above — a near-100% mismatch between the two "
                "connected systems (wrong company, unrelated business) produces exactly this signature."
            )

    if coverage.get("ambiguous_count", 0) > coverage.get("mapped_count", 0) and coverage.get("total_count", 0) > 0:
        out.append(
            f"More sources are AMBIGUOUS ({coverage['ambiguous_count']}) than confidently MAPPED "
            f"({coverage['mapped_count']}). The QBO chart of accounts likely lacks channel/source-specific "
            f"income accounts (e.g. no 'Amazon Sales' vs generic 'Sales') — accountant review of the "
            f"income account structure would resolve more of these than further automated matching."
        )

    if coverage.get("orphaned_count", 0) > 0:
        out.append(
            f"{coverage['orphaned_count']} QBO account(s) have no corresponding Linnworks source at all "
            f"this period — either they're used for non-ecommerce activity (legitimate) or they're "
            f"dead/legacy accounts worth a chart-of-accounts cleanup pass."
        )

    # --- product/SKU-level findings ---
    if product_coverage:
        pcc, pvc = product_coverage.get("count_coverage_pct"), product_coverage.get("value_coverage_pct")
        unverified = product_coverage.get("unverified_count", 0)
        if unverified > 0:
            out.append(
                f"{unverified} product(s) matched by name only, with no SKU or price corroboration — "
                f"these are UNVERIFIED, not confirmed. Treat COGS/inventory postings for these products "
                f"as unproven until an accountant confirms the SKU on both sides."
            )
        if pcc is not None and pcc < 50:
            out.append(
                f"Only {pcc}% of Linnworks products resolve to a QBO item by SKU/name/price. If COGS "
                f"is meant to post per-item, most of it currently has no reliable QBO item to attach to."
            )

    # --- reconciliation ---
    mismatches = [r for r in reconciliation_rows if getattr(r, "status", None) == "UNEXPLAINED_VARIANCE"]
    currency_mismatches = [r for r in reconciliation_rows if getattr(r, "status", None) == "CURRENCY_MISMATCH"]
    if mismatches:
        worst = max(mismatches, key=lambda r: abs(r.variance) if r.variance is not None else 0)
        out.append(
            f"{len(mismatches)} reconciliation categor{'y has' if len(mismatches)==1 else 'ies have'} an "
            f"unexplained variance; largest is '{worst.category}' at {worst.variance} "
            f"({worst.variance_pct}%). No explanation is inferred here — this needs a source-by-source "
            f"trace (see sat:reconciliation), not a guess."
        )
    if currency_mismatches:
        out.append(
            f"{len(currency_mismatches)} reconciliation categor{'y' if len(currency_mismatches)==1 else 'ies'} "
            f"could not be compared at all due to a currency mismatch between the two systems — "
            f"reconciliation for these is blocked until an FX rate/base-currency alignment is available."
        )

    structural = [g for g in data_gaps if g.get("severity", "").upper() == "HIGH"]
    if structural:
        names = ", ".join(g["gap"] for g in structural)
        out.append(
            f"{len(structural)} HIGH-severity structural data gap(s) exist ({names}) — these are not "
            f"fixable by better matching logic; the source data doesn't carry the information at all."
        )

    if not out:
        out.append("No material findings beyond the numbers above — coverage and reconciliation look clean for this period.")

    return out
