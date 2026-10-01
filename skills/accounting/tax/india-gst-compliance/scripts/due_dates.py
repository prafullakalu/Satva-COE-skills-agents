#!/usr/bin/env python3
"""GST due dates, days overdue, and the three-year filing bar.

Off-by-one due dates and the QRMP 22nd-vs-24th split are among the easiest
mistakes to make and the easiest to avoid mechanically.

VERIFY BEFORE USE. Any due date can be extended by notification for a specific
period, state or category, and extensions are frequently issued mid-month. This
script gives the statutory date; always check gst.gov.in "News and Updates" for
an extension covering the period in hand before telling anyone a deadline.

Usage:
    python3 due_dates.py --period 2026-06 --gstin 27AAPFU0939F1ZV
    python3 due_dates.py --period 2026-06 --state 27 --scheme qrmp
    python3 due_dates.py --period 2026-Q1 --state 19 --scheme composition
    python3 due_dates.py --period 2026-06 --state 27 --as-of 2026-07-29
    python3 due_dates.py --timebar --period 2022-06 --state 27
    python3 due_dates.py --selftest
"""

from __future__ import annotations

import argparse
import re
import sys
from calendar import monthrange
from datetime import date, datetime, timedelta

# QRMP GSTR-3B due date groups, by state/UT code. Set by notification; the split
# is geographical. Confirm against the current notification if the date is tight.
QRMP_22ND = {"22", "23", "24", "25", "26", "27", "28", "29", "30",
             "31", "32", "33", "34", "35", "36", "37"}
QRMP_24TH = {"01", "02", "03", "04", "05", "06", "07", "08", "09", "10",
             "11", "12", "13", "14", "15", "16", "17", "18", "19", "20",
             "21", "38", "97"}

MONTHLY_DUE = {
    "GSTR-1": 11, "GSTR-3B": 20, "GSTR-5": 13, "GSTR-5A": 20,
    "GSTR-6": 13, "GSTR-7": 10, "GSTR-8": 10, "GSTR-11": 28,
}


def _last_day(y: int, m: int) -> int:
    return monthrange(y, m)[1]


def _next_month(y: int, m: int) -> tuple[int, int]:
    return (y + 1, 1) if m == 12 else (y, m + 1)


def _safe(y: int, m: int, d: int) -> date:
    return date(y, m, min(d, _last_day(y, m)))


def parse_period(period: str) -> dict:
    """Accept 2026-06 (month) or 2026-Q1 (quarter) or 2025-26 (financial year).

    Quarters are GST quarters: Q1 = Apr-Jun, Q2 = Jul-Sep, Q3 = Oct-Dec,
    Q4 = Jan-Mar. Q4 of FY 2025-26 therefore falls in calendar 2026.
    """
    period = period.strip().upper()

    m = re.fullmatch(r"(\d{4})-(\d{2})", period)
    if m and 1 <= int(m.group(2)) <= 12:
        y, mo = int(m.group(1)), int(m.group(2))
        return {"kind": "month", "year": y, "month": mo,
                "start": date(y, mo, 1), "end": date(y, mo, _last_day(y, mo)),
                "label": f"{date(y, mo, 1):%B %Y}", "fy": financial_year(date(y, mo, 1))}

    m = re.fullmatch(r"(\d{4})-Q([1-4])", period)
    if m:
        fy_start = int(m.group(1))
        q = int(m.group(2))
        first_month = 4 + (q - 1) * 3
        y = fy_start if first_month <= 12 else fy_start + 1
        if first_month > 12:
            first_month -= 12
        if q == 4:
            y, first_month = fy_start + 1, 1
        end_y, end_m = y, first_month + 2
        if end_m > 12:
            end_y, end_m = end_y + 1, end_m - 12
        return {"kind": "quarter", "year": y, "month": end_m, "quarter": q,
                "start": date(y, first_month, 1),
                "end": date(end_y, end_m, _last_day(end_y, end_m)),
                "label": f"Q{q} FY {fy_start}-{str(fy_start + 1)[-2:]}",
                "fy": f"{fy_start}-{str(fy_start + 1)[-2:]}"}

    # Financial year, e.g. 2025-26. The second pair must be the next year's last
    # two digits, otherwise "2026-13" would silently parse as an FY. Note that a
    # string like "2011-12" is treated as December 2011, not FY 2011-12 — the
    # month reading is checked first. Pass an unambiguous form if you mean the FY.
    m = re.fullmatch(r"(\d{4})-(\d{2})", period)
    if m and int(m.group(2)) == (int(m.group(1)) + 1) % 100:
        fy_start = int(m.group(1))
        return {"kind": "fy", "year": fy_start,
                "start": date(fy_start, 4, 1), "end": date(fy_start + 1, 3, 31),
                "label": f"FY {fy_start}-{m.group(2)}",
                "fy": f"{fy_start}-{m.group(2)}"}

    raise ValueError(f"cannot parse period '{period}' — use 2026-06, 2026-Q1 or 2025-26")


def financial_year(d: date) -> str:
    start = d.year if d.month >= 4 else d.year - 1
    return f"{start}-{str(start + 1)[-2:]}"


def qrmp_group(state_code: str) -> int:
    if state_code in QRMP_22ND:
        return 22
    if state_code in QRMP_24TH:
        return 24
    raise ValueError(f"state code '{state_code}' is not in the QRMP grouping — verify it")


def due_dates(period: str, state_code: str | None = None,
              scheme: str = "monthly") -> dict:
    """Statutory due dates for the given period and scheme."""
    scheme = scheme.lower()
    p = parse_period(period)
    out: dict[str, date] = {}

    if scheme == "monthly":
        if p["kind"] != "month":
            raise ValueError("monthly scheme needs a month period, e.g. 2026-06")
        ny, nm = _next_month(p["year"], p["month"])
        for form, day in MONTHLY_DUE.items():
            out[form] = _safe(ny, nm, day)
        out["GSTR-2B generated"] = _safe(ny, nm, 14)
        out["GSTR-1A window closes"] = out["GSTR-3B"]

    elif scheme == "qrmp":
        if state_code is None:
            raise ValueError("QRMP due dates need a state code")
        day = qrmp_group(state_code)
        if p["kind"] == "month":
            ny, nm = _next_month(p["year"], p["month"])
            out["IFF (optional)"] = _safe(ny, nm, 13)
            out["PMT-06"] = _safe(ny, nm, 25)
            out["_note"] = ("month within a quarter — GSTR-1 and GSTR-3B are "
                            "quarterly; pass the quarter for those dates")
        else:
            ny, nm = _next_month(p["end"].year, p["end"].month)
            out["GSTR-1 (quarterly)"] = _safe(ny, nm, 13)
            out["GSTR-2B generated"] = _safe(ny, nm, 14)
            out[f"GSTR-3B (quarterly, {day}th group)"] = _safe(ny, nm, day)

    elif scheme == "composition":
        if p["kind"] == "quarter":
            ny, nm = _next_month(p["end"].year, p["end"].month)
            out["CMP-08"] = _safe(ny, nm, 18)
        elif p["kind"] == "fy":
            out["GSTR-4 (annual)"] = date(p["year"] + 1, 6, 30)
        else:
            raise ValueError("composition needs a quarter (CMP-08) or an FY (GSTR-4)")

    else:
        raise ValueError(f"unknown scheme '{scheme}'; use monthly, qrmp or composition")

    if p["kind"] == "fy":
        out["GSTR-9 / GSTR-9C"] = date(p["year"] + 1, 12, 31)
        out["s16(4) ITC cut-off"] = date(p["year"] + 1, 11, 30)
        out["Rule 37A reversal deadline"] = date(p["year"] + 1, 11, 30)
        out["Rule 42/43 annual finalisation"] = date(p["year"] + 1, 9, 30)
        out["LUT (RFD-11) for the year"] = date(p["year"], 4, 1)

    return {"period": p["label"], "period_kind": p["kind"], "fy": p.get("fy"),
            "scheme": scheme, "state_code": state_code, "due_dates": out}


def overdue(due: date, as_of: date) -> dict:
    days = (as_of - due).days
    return {"due": due.isoformat(), "as_of": as_of.isoformat(),
            "days_overdue": max(0, days),
            "status": "overdue" if days > 0 else ("due today" if days == 0 else "not yet due")}


def time_bar(due: date, as_of: date) -> dict:
    """Three-year bar under s37(5)/s39(11)/s44(2)/s52(15).

    A return cannot be furnished after three years from its due date, and the
    portal enforces this. The liability does not disappear — it moves into
    assessment and demand proceedings, and any ITC for the period is lost.
    """
    barred_on = date(due.year + 3, due.month, min(due.day, _last_day(due.year + 3, due.month)))
    days_left = (barred_on - as_of).days
    if days_left < 0:
        status, urgency = "TIME-BARRED", "critical"
    elif days_left <= 90:
        status, urgency = "closing", "critical"
    elif days_left <= 365:
        status, urgency = "closing", "high"
    else:
        status, urgency = "open", "normal"
    return {"due": due.isoformat(), "barred_on": barred_on.isoformat(),
            "as_of": as_of.isoformat(), "days_remaining": days_left,
            "status": status, "urgency": urgency,
            "note": ("Filing is blocked on the portal. An 'Application for Unbarring "
                     "Returns' exists but is discretionary and does not cure the "
                     "s16(4) ITC time limit." if days_left < 0 else
                     "File before the bar. After it, the liability is assessed on a "
                     "best-judgement basis and the ITC for the period is lost.")}


def selftest() -> int:
    failures = []

    def check(label, got, want):
        if got != want:
            failures.append(f"{label}: got {got}, expected {want}")

    p = parse_period("2026-06")
    check("month start", p["start"], date(2026, 6, 1))
    check("month end", p["end"], date(2026, 6, 30))
    check("month fy", p["fy"], "2026-27")
    check("march is prior fy", parse_period("2026-03")["fy"], "2025-26")

    # GST quarters, including Q4 spilling into the next calendar year.
    check("Q1 start", parse_period("2025-Q1")["start"], date(2025, 4, 1))
    check("Q1 end", parse_period("2025-Q1")["end"], date(2025, 6, 30))
    check("Q4 start", parse_period("2025-Q4")["start"], date(2026, 1, 1))
    check("Q4 end", parse_period("2025-Q4")["end"], date(2026, 3, 31))

    d = due_dates("2026-06", "27", "monthly")["due_dates"]
    check("GSTR-1 monthly", d["GSTR-1"], date(2026, 7, 11))
    check("GSTR-3B monthly", d["GSTR-3B"], date(2026, 7, 20))
    check("2B generation", d["GSTR-2B generated"], date(2026, 7, 14))
    check("1A closes with 3B", d["GSTR-1A window closes"], date(2026, 7, 20))

    # QRMP: Maharashtra is a 22nd state, West Bengal a 24th state.
    d = due_dates("2025-Q4", "27", "qrmp")["due_dates"]
    check("QRMP MH 3B", d["GSTR-3B (quarterly, 22th group)"], date(2026, 4, 22))
    check("QRMP MH 1", d["GSTR-1 (quarterly)"], date(2026, 4, 13))
    d = due_dates("2025-Q4", "19", "qrmp")["due_dates"]
    check("QRMP WB 3B", d["GSTR-3B (quarterly, 24th group)"], date(2026, 4, 24))
    check("group 22", qrmp_group("29"), 22)
    check("group 24", qrmp_group("07"), 24)

    d = due_dates("2026-06", "27", "qrmp")["due_dates"]
    check("PMT-06", d["PMT-06"], date(2026, 7, 25))

    d = due_dates("2025-Q4", "27", "composition")["due_dates"]
    check("CMP-08", d["CMP-08"], date(2026, 4, 18))

    d = due_dates("2025-26", "27", "composition")["due_dates"]
    check("GSTR-4", d["GSTR-4 (annual)"], date(2026, 6, 30))
    check("GSTR-9 FY25-26", d["GSTR-9 / GSTR-9C"], date(2026, 12, 31))
    check("s16(4) FY25-26", d["s16(4) ITC cut-off"], date(2026, 11, 30))

    # December period rolls into the next January.
    check("dec rolls over", due_dates("2026-12", "27", "monthly")["due_dates"]["GSTR-3B"],
          date(2027, 1, 20))

    o = overdue(date(2026, 7, 20), date(2026, 7, 29))
    check("overdue days", o["days_overdue"], 9)
    check("not yet due", overdue(date(2026, 8, 20), date(2026, 7, 29))["status"],
          "not yet due")
    check("due today", overdue(date(2026, 7, 29), date(2026, 7, 29))["status"],
          "due today")

    t = time_bar(date(2022, 7, 20), date(2026, 7, 29))
    check("time barred", t["status"], "TIME-BARRED")
    t = time_bar(date(2023, 8, 20), date(2026, 7, 29))
    check("closing soon", t["urgency"], "critical")
    t = time_bar(date(2026, 7, 20), date(2026, 7, 29))
    check("open", t["status"], "open")

    for label, fn in [
        ("bad period", lambda: parse_period("June 2026")),
        ("bad month", lambda: parse_period("2026-13")),
        ("bad fy pairing", lambda: parse_period("2025-29")),
        ("bad quarter", lambda: parse_period("2025-Q5")),
        ("qrmp without state", lambda: due_dates("2025-Q4", None, "qrmp")),
        ("unknown scheme", lambda: due_dates("2026-06", "27", "annual")),
        ("monthly with quarter", lambda: due_dates("2025-Q4", "27", "monthly")),
        ("unknown state", lambda: qrmp_group("55")),
    ]:
        try:
            fn()
            failures.append(f"no error raised for {label}")
        except ValueError:
            pass

    if failures:
        print("SELFTEST FAILED")
        for f in failures:
            print("  -", f)
        return 1
    print("SELFTEST PASSED (periods, monthly, QRMP groups, composition, annual, "
          "overdue, time bar, guards)")
    return 0


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--period", help="2026-06 (month), 2026-Q1 (quarter) or 2025-26 (FY)")
    p.add_argument("--state", help="two-digit state/UT code")
    p.add_argument("--gstin", help="derive the state code from a GSTIN")
    p.add_argument("--scheme", default="monthly",
                   choices=["monthly", "qrmp", "composition"])
    p.add_argument("--as-of", default=None, help="YYYY-MM-DD, defaults to today")
    p.add_argument("--timebar", action="store_true",
                   help="report the three-year bar for this period's GSTR-3B")
    p.add_argument("--selftest", action="store_true")
    args = p.parse_args()

    if args.selftest:
        return selftest()
    if not args.period:
        p.print_help()
        return 2

    state = args.state or (args.gstin[:2] if args.gstin else None)
    as_of = datetime.strptime(args.as_of, "%Y-%m-%d").date() if args.as_of else date.today()

    info = due_dates(args.period, state, args.scheme)
    print(f"Period : {info['period']}  ({info['scheme']}"
          + (f", state {state}" if state else "") + ")")
    print(f"As of  : {as_of.isoformat()}")
    print()
    for form, d in info["due_dates"].items():
        if form.startswith("_"):
            print(f"  note: {d}")
            continue
        o = overdue(d, as_of)
        flag = "" if o["status"] == "not yet due" else f"   <-- {o['status'].upper()}"
        if o["days_overdue"]:
            flag += f" by {o['days_overdue']} day(s)"
        print(f"  {form:<38} {d.isoformat()}{flag}")

    if args.timebar:
        base = info["due_dates"].get("GSTR-3B") or next(iter(info["due_dates"].values()))
        print()
        print("Three-year filing bar:")
        for k, v in time_bar(base, as_of).items():
            print(f"  {k}: {v}")

    print()
    print("VERIFY: check gst.gov.in News and Updates for an extension notified for "
          "this period, state or category before relying on any date above.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
