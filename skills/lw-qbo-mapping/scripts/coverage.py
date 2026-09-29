"""
Coverage calculator: count-based AND value-based (spec #8).

A small number of unmapped records can represent a large financial exposure — the two numbers
are reported side by side and NEVER collapsed into one "X% mapped" headline.
"""
from __future__ import annotations
from mapping_engine import MappingResult


def coverage_report(results: list[MappingResult]) -> dict:
    """results should exclude ORPHANED rows (those have no source side to count)."""
    relevant = [r for r in results if r.status != "ORPHANED"]
    total_count = len(relevant)
    mapped = [r for r in relevant if r.status == "MAPPED"]
    unmapped = [r for r in relevant if r.status == "UNMAPPED"]
    ambiguous = [r for r in relevant if r.status == "AMBIGUOUS"]
    invalid = [r for r in relevant if r.status == "INVALID"]
    structural = [r for r in relevant if r.status == "STRUCTURAL_DATA_GAP"]
    inactive = [r for r in relevant if r.status == "INACTIVE"]
    unverified = [r for r in relevant if r.status == "UNVERIFIED"]
    orphaned = [r for r in results if r.status == "ORPHANED"]

    def abs_value(rows):
        return sum(abs(r.source_value) for r in rows if r.source_value is not None)

    valued = [r for r in relevant if r.source_value is not None]
    total_value = abs_value(valued)
    mapped_value = abs_value(mapped)

    count_coverage = (len(mapped) / total_count) if total_count else None
    value_coverage = (mapped_value / total_value) if total_value else None

    return {
        "total_count": total_count,
        "mapped_count": len(mapped),
        "unmapped_count": len(unmapped),
        "ambiguous_count": len(ambiguous),
        "invalid_count": len(invalid),
        "structural_gap_count": len(structural),
        "inactive_count": len(inactive),
        "unverified_count": len(unverified),
        "orphaned_count": len(orphaned),
        "count_coverage_pct": round(count_coverage * 100, 1) if count_coverage is not None else None,
        "total_value": round(total_value, 2),
        "mapped_value": round(mapped_value, 2),
        "unmapped_value": round(total_value - mapped_value, 2),
        "value_coverage_pct": round(value_coverage * 100, 1) if value_coverage is not None else None,
        "largest_financial_gaps": sorted(
            [r for r in relevant if r.status != "MAPPED" and r.source_value],
            key=lambda r: abs(r.source_value), reverse=True,
        )[:10],
    }
