"""
Reconciliation: Linnworks-derived totals vs QBO totals for the same period (spec #9).

Never invents explanations for a variance it can't account for — reports UNEXPLAINED_VARIANCE
verbatim rather than guessing (spec #9, and sat:reconciliation's "no silent success" rule).
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional

TOLERANCE_PCT = 0.5  # variance within this % of the larger side is treated as immaterial/rounding


@dataclass
class ReconciliationRow:
    category: str
    linnworks_total: float
    qbo_total: float
    currency: str
    linnworks_currency: Optional[str] = None
    qbo_currency: Optional[str] = None
    variance: Optional[float] = field(init=False)
    variance_pct: Optional[float] = field(init=False)
    status: str = field(init=False)

    def __post_init__(self):
        # Cross-currency comparison without an FX rate is invalid arithmetic, not a real variance —
        # refuse to compute one rather than silently mixing currencies (spec #9 / sat:reconciliation).
        if self.linnworks_currency and self.qbo_currency and self.linnworks_currency != self.qbo_currency:
            self.variance = None
            self.variance_pct = None
            self.status = "CURRENCY_MISMATCH"
            return
        self.variance = round(self.linnworks_total - self.qbo_total, 2)
        base = max(abs(self.linnworks_total), abs(self.qbo_total))
        self.variance_pct = round(abs(self.variance) / base * 100, 2) if base else None
        if base == 0:
            self.status = "MATCHED"
        elif self.variance_pct is not None and self.variance_pct <= TOLERANCE_PCT:
            self.status = "MATCHED"
        else:
            self.status = "UNEXPLAINED_VARIANCE"

    def to_row(self) -> dict:
        return {
            "category": self.category,
            "linnworks": self.linnworks_total,
            "qbo": self.qbo_total,
            "currency": self.currency,
            "variance": self.variance,
            "variance_pct": self.variance_pct,
            "status": self.status,
        }


def reconcile(category: str, linnworks_total: float, qbo_total: float, currency: str,
              linnworks_currency: Optional[str] = None, qbo_currency: Optional[str] = None) -> ReconciliationRow:
    return ReconciliationRow(category=category, linnworks_total=linnworks_total, qbo_total=qbo_total,
                              currency=currency, linnworks_currency=linnworks_currency, qbo_currency=qbo_currency)


def reconcile_many(rows: list[dict]) -> list[ReconciliationRow]:
    """rows: [{"category", "linnworks_total", "qbo_total", "currency",
                "linnworks_currency"?, "qbo_currency"?}, ...]
    Pass linnworks_currency/qbo_currency explicitly when they might differ (spec #12) — omitting
    them assumes same-currency and computes a normal variance.
    """
    return [reconcile(r["category"], r["linnworks_total"], r["qbo_total"], r["currency"],
                       r.get("linnworks_currency"), r.get("qbo_currency")) for r in rows]
