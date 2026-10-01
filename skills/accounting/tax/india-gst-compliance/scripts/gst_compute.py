#!/usr/bin/env python3
"""Deterministic GST arithmetic: tax split, interest under s50, late fee under s47.

GST arithmetic is mechanical, and mechanical work done in prose produces
different answers on different days. Everything here uses Decimal so that
rupee-and-paise figures behave the way an accountant expects rather than the way
binary floats do.

VERIFY BEFORE USE. Rates, late-fee caps and thresholds are set by notification
and change. The defaults below reflect the position as at 2026-07-29; confirm
them for the tax period you are working on and override with the flags if they
have moved. A script that is confidently out of date is worse than one you had
to check.

Commands:
    split      split a taxable value into IGST / CGST / SGST / cess
    interest   interest under s50 for delayed payment or utilised wrong credit
    latefee    late fee under s47 with the applicable cap
    liability  net payable from output tax and ITC, with ledger utilisation
    selftest   run built-in tests

Examples:
    python3 gst_compute.py split --value 100000 --rate 18 --intra
    python3 gst_compute.py interest --amount 250000 --from 2026-06-20 --to 2026-07-29
    python3 gst_compute.py latefee --form GSTR-3B --days 12 --aato 30000000
    python3 gst_compute.py liability --json liability.json
    python3 gst_compute.py selftest
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date, datetime
from decimal import Decimal, ROUND_HALF_UP

# --- defaults, all verifiable and all overridable -------------------------

INTEREST_DELAYED_PAYMENT = Decimal("18")   # s50(1)
INTEREST_WRONG_ITC = Decimal("18")         # s50(3) r/w Rule 88B(3). Substituted
                                           # retrospectively from 01.07.2017;
                                           # older material saying 24% is stale.
INTEREST_DELAYED_REFUND = Decimal("6")     # s56
INTEREST_REFUND_APPEAL = Decimal("9")      # s56 proviso

# s47 late fee: (per-day with tax, per-day nil). Split equally CGST/SGST.
LATE_FEE_PER_DAY = {
    "GSTR-1":  (Decimal("50"), Decimal("20")),
    "GSTR-3B": (Decimal("50"), Decimal("20")),
    "GSTR-4":  (Decimal("50"), Decimal("20")),
    "GSTR-7":  (Decimal("50"), Decimal("20")),
}

# Caps for GSTR-1 / GSTR-3B by AATO of the preceding FY, in rupees.
LATE_FEE_CAPS = [
    (Decimal("15000000"), Decimal("2000")),    # AATO <= 1.5 cr
    (Decimal("50000000"), Decimal("5000")),    # 1.5 cr < AATO <= 5 cr
    (None,                Decimal("10000")),   # AATO > 5 cr
]
LATE_FEE_CAP_NIL = Decimal("500")
LATE_FEE_CAP_GSTR4 = (Decimal("2000"), Decimal("500"))   # (with tax, nil)
LATE_FEE_CAP_GSTR7 = Decimal("2000")

# GSTR-9 / 9C: (per-day, cap as a fraction of turnover in the state/UT).
GSTR9_LATE_FEE = [
    (Decimal("50000000"),  Decimal("50"),  Decimal("0.0004")),   # AATO <= 5 cr
    (Decimal("200000000"), Decimal("100"), Decimal("0.0004")),   # 5-20 cr
    (None,                 Decimal("200"), Decimal("0.005")),    # > 20 cr
]

TWOPLACES = Decimal("0.01")


def D(x) -> Decimal:
    return x if isinstance(x, Decimal) else Decimal(str(x))


def money(x) -> Decimal:
    """Round to paise, half-up — the convention Indian tax computations use."""
    return D(x).quantize(TWOPLACES, rounding=ROUND_HALF_UP)


def rupees(x) -> Decimal:
    """Round to the nearest rupee, half-up. Returns are reported in rupees."""
    return D(x).quantize(Decimal("1"), rounding=ROUND_HALF_UP)


# --- tax split -------------------------------------------------------------

def split_tax(taxable_value, rate, intra_state: bool, cess_rate=0,
              cess_fixed=0) -> dict:
    """Split a taxable value into its tax heads.

    Intra-state supplies carry CGST and SGST at half the rate each; inter-state
    supplies carry IGST at the full rate. Cess, where it applies, may be
    ad valorem, a fixed amount, or both.
    """
    tv = D(taxable_value)
    r = D(rate)
    if tv < 0:
        raise ValueError("taxable value cannot be negative; use a credit note")
    if r < 0:
        raise ValueError("rate cannot be negative")

    total_tax = money(tv * r / 100)
    if intra_state:
        cgst = money(tv * r / 200)
        # Derive SGST from the total so the two heads always sum exactly to the
        # tax on the line; halving twice can leave a paisa adrift.
        sgst = money(total_tax - cgst)
        igst = Decimal("0.00")
    else:
        igst, cgst, sgst = total_tax, Decimal("0.00"), Decimal("0.00")

    cess = money(tv * D(cess_rate) / 100) + money(cess_fixed)

    return {
        "taxable_value": money(tv), "rate": r, "intra_state": intra_state,
        "igst": igst, "cgst": cgst, "sgst": sgst, "cess": money(cess),
        "total_tax": money(igst + cgst + sgst + cess),
        "invoice_value": money(tv + igst + cgst + sgst + cess),
    }


# --- interest --------------------------------------------------------------

def interest(amount, from_date: date, to_date: date, rate=None,
             basis: str = "delayed_payment") -> dict:
    """Simple interest on a daily basis, inclusive of the end date.

    s50 interest runs from the day after the due date to the date of payment.
    Interest is computed on a 365-day year (366 is used by some software; the
    difference is immaterial at these rates but note which you used).

    basis:
      delayed_payment  s50(1)  — on the net cash liability paid late
      wrong_itc        s50(3)  — on ITC wrongly availed AND UTILISED. Credit
                                 availed but not utilised attracts no interest.
      delayed_refund   s56     — payable by the department
      refund_appeal    s56 proviso
    """
    rates = {
        "delayed_payment": INTEREST_DELAYED_PAYMENT,
        "wrong_itc": INTEREST_WRONG_ITC,
        "delayed_refund": INTEREST_DELAYED_REFUND,
        "refund_appeal": INTEREST_REFUND_APPEAL,
    }
    if basis not in rates:
        raise ValueError(f"unknown basis '{basis}'; expected one of {sorted(rates)}")
    r = D(rate) if rate is not None else rates[basis]

    days = (to_date - from_date).days
    if days < 0:
        raise ValueError("to_date is before from_date")

    amt = D(amount)
    value = money(amt * r / 100 * days / 365)
    return {
        "amount": money(amt), "rate": r, "basis": basis,
        "from": from_date.isoformat(), "to": to_date.isoformat(),
        "days": days, "interest": value,
        "note": ("s50(3) applies only to credit that was availed AND utilised"
                 if basis == "wrong_itc" else
                 "s50(1) is charged on the net cash liability where the return is "
                 "filed late but before proceedings under s73/s74 commence"),
    }


# --- late fee --------------------------------------------------------------

def _cap_for_aato(aato) -> Decimal:
    a = D(aato)
    for threshold, cap in LATE_FEE_CAPS:
        if threshold is None or a <= threshold:
            return cap
    return LATE_FEE_CAPS[-1][1]


def late_fee(form: str, days: int, nil_return: bool = False, aato=0,
             state_turnover=None) -> dict:
    """Late fee under s47, applying the cap for the form and turnover band."""
    form = form.upper().replace(" ", "")
    if days < 0:
        raise ValueError("days of delay cannot be negative")
    if days == 0:
        return {"form": form, "days": 0, "gross": Decimal("0.00"),
                "cap": None, "late_fee": Decimal("0.00"),
                "cgst": Decimal("0.00"), "sgst": Decimal("0.00"),
                "note": "filed on or before the due date"}

    if form in ("GSTR-9", "GSTR9", "GSTR-9C", "GSTR9C"):
        a = D(aato)
        for threshold, per_day, cap_pct in GSTR9_LATE_FEE:
            if threshold is None or a <= threshold:
                break
        gross = money(per_day * days)
        if state_turnover is None:
            cap = None
            note = ("cap is a percentage of turnover in the state/UT — supply "
                    "--state-turnover to apply it")
        else:
            cap = money(D(state_turnover) * cap_pct)
            note = f"cap = {cap_pct * 100}% of turnover in the state/UT"
        fee = gross if cap is None else min(gross, cap)
    else:
        if form not in LATE_FEE_PER_DAY:
            raise ValueError(f"unknown form '{form}'; expected one of "
                             f"{sorted(LATE_FEE_PER_DAY)} or GSTR-9/9C")
        with_tax, nil = LATE_FEE_PER_DAY[form]
        per_day = nil if nil_return else with_tax
        gross = money(per_day * days)
        if form == "GSTR-4":
            cap = LATE_FEE_CAP_GSTR4[1] if nil_return else LATE_FEE_CAP_GSTR4[0]
        elif form == "GSTR-7":
            cap = LATE_FEE_CAP_GSTR7
        else:
            cap = LATE_FEE_CAP_NIL if nil_return else _cap_for_aato(aato)
        fee = min(gross, cap)
        note = "cap applied" if fee < gross else "under the cap"

    cgst = money(fee / 2)
    return {
        "form": form, "days": days, "nil_return": nil_return,
        "gross": gross, "cap": cap, "late_fee": fee,
        "cgst": cgst, "sgst": money(fee - cgst), "note": note,
    }


# --- net liability ---------------------------------------------------------

def net_liability(output: dict, itc: dict, reversals: dict | None = None,
                  cash_balance: dict | None = None,
                  monthly_taxable_turnover=None,
                  rounding: str = "exact") -> dict:
    """Net payable by head, with credit utilisation and a Rule 86B test.

    Utilisation follows the statutory order: IGST credit is used against IGST
    first, then against CGST and SGST; CGST and SGST credit can only be used
    against their own head and then IGST, and CGST credit can never be set off
    against SGST or vice versa. Cess credit is usable only against cess.

    rounding:
      exact   keep paise throughout — the arithmetically correct figure
      portal  round output tax and available credit to the nearest rupee before
              offsetting, which is what the GST portal does at the utilisation
              step. Rs 4,675.50 of CGST credit is utilised as Rs 4,676.

    Use `portal` whenever you are about to compare against the portal's own
    summary. The two modes differ by a rupee or two, and the distinction matters:
    a difference you predicted is rounding, and a difference you did not predict
    is a transposed invoice. Only the second is worth stopping for.
    """
    if rounding not in ("exact", "portal"):
        raise ValueError(f"rounding must be 'exact' or 'portal', got {rounding!r}")
    heads = ("igst", "cgst", "sgst", "cess")
    rev = reversals or {}
    out = {h: D(output.get(h, 0)) for h in heads}
    cred = {h: D(itc.get(h, 0)) - D(rev.get(h, 0)) for h in heads}
    for h in heads:
        if cred[h] < 0:
            raise ValueError(f"reversal of {h} exceeds credit availed — check inputs")

    if rounding == "portal":
        out = {h: rupees(out[h]) for h in heads}
        cred = {h: rupees(cred[h]) for h in heads}

    avail = dict(cred)
    used = {h: {"igst": Decimal(0), "cgst": Decimal(0),
                "sgst": Decimal(0), "cess": Decimal(0)} for h in heads}
    remaining = dict(out)

    def apply(credit_head: str, liability_head: str) -> None:
        take = min(avail[credit_head], remaining[liability_head])
        if take > 0:
            avail[credit_head] -= take
            remaining[liability_head] -= take
            used[liability_head][credit_head] += take

    apply("igst", "igst")
    apply("igst", "cgst")
    apply("igst", "sgst")
    apply("cgst", "cgst")
    apply("cgst", "igst")
    apply("sgst", "sgst")
    apply("sgst", "igst")
    apply("cess", "cess")

    cash_needed = {h: money(remaining[h]) for h in heads}
    total_output = money(sum(out.values()))
    total_cash = money(sum(cash_needed.values()))

    result = {
        "rounding": rounding,
        "output_tax": {h: money(out[h]) for h in heads},
        "itc_available": {h: money(cred[h]) for h in heads},
        "utilised": {h: {k: money(v) for k, v in used[h].items()} for h in heads},
        "credit_balance_carried": {h: money(avail[h]) for h in heads},
        "payable_in_cash": cash_needed,
        "total_output_tax": total_output,
        "total_cash_payable": total_cash,
        "warnings": [],
    }

    # Rule 86B: taxable turnover above Rs 50 lakh in the month means at least 1%
    # of output tax liability must go through the cash ledger. Exceptions exist
    # (income tax paid above Rs 1 lakh in each of the last two years, large
    # zero-rated/inverted refunds received, government bodies and PSUs) so this
    # is a flag to check, not an automatic adjustment.
    if monthly_taxable_turnover is not None and D(monthly_taxable_turnover) > Decimal("5000000"):
        minimum_cash = money(total_output * Decimal("0.01"))
        result["rule_86b"] = {
            "applies": True, "minimum_cash_required": minimum_cash,
            "cash_currently_payable": total_cash,
            "satisfied": total_cash >= minimum_cash,
        }
        if total_cash < minimum_cash:
            result["warnings"].append(
                f"Rule 86B: taxable turnover exceeds Rs 50 lakh, so at least "
                f"Rs {minimum_cash} (1% of output tax) must be paid in cash, but "
                f"only Rs {total_cash} is currently payable in cash. Check whether "
                f"an exception applies before filing."
            )
    elif monthly_taxable_turnover is not None:
        result["rule_86b"] = {"applies": False}

    if cash_balance:
        short = {}
        for h in heads:
            bal = D(cash_balance.get(h, 0))
            if cash_needed[h] > bal:
                short[h] = money(cash_needed[h] - bal)
        if short:
            result["cash_ledger_shortfall"] = short
            result["warnings"].append(
                "Cash ledger is short — generate and pay the challan before filing: "
                + ", ".join(f"{k.upper()} Rs {v}" for k, v in short.items())
            )

    result["reminders"] = [
        "RCM liability must be paid in cash and can never be discharged from the "
        "credit ledger — confirm it is included in the output figures above.",
        "Cess credit is usable only against cess liability.",
    ]
    if rounding == "exact":
        result["reminders"].append(
            "These are exact figures. Before comparing against the portal's own "
            "summary, recompute with rounding='portal' — the portal rounds to the "
            "nearest rupee at the utilisation step."
        )
    return result


# --- CLI -------------------------------------------------------------------

def _date(s: str) -> date:
    return datetime.strptime(s, "%Y-%m-%d").date()


def _dump(obj) -> None:
    print(json.dumps(obj, indent=2, default=str))


def selftest() -> int:
    failures = []

    def check(label, got, want):
        if got != want:
            failures.append(f"{label}: got {got}, expected {want}")

    # Intra-state split: heads halve and sum back exactly.
    s = split_tax(100000, 18, intra_state=True)
    check("intra cgst", s["cgst"], Decimal("9000.00"))
    check("intra sgst", s["sgst"], Decimal("9000.00"))
    check("intra igst", s["igst"], Decimal("0.00"))
    check("intra total", s["total_tax"], Decimal("18000.00"))
    check("intra invoice value", s["invoice_value"], Decimal("118000.00"))

    # Inter-state split.
    s = split_tax(100000, 18, intra_state=False)
    check("inter igst", s["igst"], Decimal("18000.00"))
    check("inter cgst", s["cgst"], Decimal("0.00"))

    # An odd value must not lose a paisa between CGST and SGST.
    s = split_tax("1234.57", 5, intra_state=True)
    if s["cgst"] + s["sgst"] != s["total_tax"]:
        failures.append(f"odd-value split does not reconcile: {s}")

    # 40% demerit rate with cess should still balance.
    s = split_tax(50000, 40, intra_state=False, cess_rate=12)
    check("demerit igst", s["igst"], Decimal("20000.00"))
    check("demerit cess", s["cess"], Decimal("6000.00"))

    # Interest: 18% on 100000 for 365 days is exactly 18000.
    i = interest(100000, date(2025, 1, 1), date(2026, 1, 1))
    check("interest 365d", i["interest"], Decimal("18000.00"))
    check("interest days", i["days"], 365)
    # s50(3) must be 18%, not the stale 24% figure still circulating.
    check("s50(3) rate", interest(1000, date(2026, 1, 1), date(2026, 1, 2),
                                  basis="wrong_itc")["rate"], Decimal("18"))

    # Late fee: under the cap, then capped.
    f = late_fee("GSTR-3B", days=10, aato=1000000)
    check("late fee 10 days", f["late_fee"], Decimal("500.00"))
    f = late_fee("GSTR-3B", days=400, aato=1000000)
    check("late fee capped small", f["late_fee"], Decimal("2000"))
    f = late_fee("GSTR-3B", days=400, aato=600000000)
    check("late fee capped large", f["late_fee"], Decimal("10000"))
    f = late_fee("GSTR-1", days=100, nil_return=True, aato=1000000)
    check("nil late fee capped", f["late_fee"], Decimal("500"))
    check("late fee zero days", late_fee("GSTR-1", 0)["late_fee"], Decimal("0.00"))
    f = late_fee("GSTR-9", days=30, aato=600000000, state_turnover=600000000)
    check("gstr9 per day", f["gross"], Decimal("6000.00"))

    # Utilisation: IGST credit spills over into CGST then SGST.
    r = net_liability(output={"igst": 0, "cgst": 9000, "sgst": 9000},
                      itc={"igst": 20000})
    check("igst spillover cgst", r["payable_in_cash"]["cgst"], Decimal("0.00"))
    check("igst spillover sgst", r["payable_in_cash"]["sgst"], Decimal("0.00"))
    check("igst carried", r["credit_balance_carried"]["igst"], Decimal("2000.00"))

    # CGST credit must never discharge SGST.
    r = net_liability(output={"cgst": 0, "sgst": 5000}, itc={"cgst": 5000})
    check("cgst cannot pay sgst", r["payable_in_cash"]["sgst"], Decimal("5000.00"))

    # Cess is ring-fenced.
    r = net_liability(output={"cess": 1000}, itc={"igst": 100000})
    check("cess ring-fenced", r["payable_in_cash"]["cess"], Decimal("1000.00"))

    # Rule 86B fires when everything would otherwise be paid from credit.
    r = net_liability(output={"igst": 100000}, itc={"igst": 100000},
                      monthly_taxable_turnover=6000000)
    if r["rule_86b"]["satisfied"] or not r["warnings"]:
        failures.append("Rule 86B warning did not fire when it should have")
    r = net_liability(output={"igst": 100000}, itc={"igst": 100000},
                      monthly_taxable_turnover=4000000)
    if r["rule_86b"]["applies"]:
        failures.append("Rule 86B fired below the Rs 50 lakh threshold")

    # Portal rounding: 4675.50 of each head is utilised as 4676, per the field
    # observation this mode exists for.
    r = net_liability(output={"cgst": 10000, "sgst": 10000},
                      itc={"cgst": "4675.50", "sgst": "4675.50"},
                      rounding="portal")
    check("portal round cgst cash", r["payable_in_cash"]["cgst"], Decimal("5324.00"))
    check("portal round sgst cash", r["payable_in_cash"]["sgst"], Decimal("5324.00"))
    check("portal mode recorded", r["rounding"], "portal")
    r = net_liability(output={"cgst": 10000, "sgst": 10000},
                      itc={"cgst": "4675.50", "sgst": "4675.50"})
    check("exact keeps paise", r["payable_in_cash"]["cgst"], Decimal("5324.50"))
    if not any("rounding='portal'" in n for n in r["reminders"]):
        failures.append("exact mode did not point at the portal comparison")
    try:
        net_liability({"igst": 1}, {}, rounding="nearest")
        failures.append("accepted an unknown rounding mode")
    except ValueError:
        pass

    # Cash ledger shortfall must be surfaced.
    r = net_liability(output={"igst": 5000}, itc={}, cash_balance={"igst": 1000})
    if "cash_ledger_shortfall" not in r:
        failures.append("cash ledger shortfall not detected")

    # Input guards.
    for label, fn in [
        ("negative taxable value", lambda: split_tax(-1, 18, True)),
        ("reversed dates", lambda: interest(100, date(2026, 2, 1), date(2026, 1, 1))),
        ("negative days", lambda: late_fee("GSTR-1", -1)),
        ("unknown form", lambda: late_fee("GSTR-42", 1)),
        ("unknown interest basis", lambda: interest(100, date(2026, 1, 1),
                                                    date(2026, 1, 2), basis="x")),
        ("reversal exceeds credit", lambda: net_liability({"igst": 0},
                                                          {"igst": 100},
                                                          {"igst": 500})),
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
    print("SELFTEST PASSED (split, interest, late fee, utilisation, Rule 86B, guards)")
    return 0


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd")

    sp = sub.add_parser("split", help="split a taxable value into tax heads")
    sp.add_argument("--value", required=True)
    sp.add_argument("--rate", required=True)
    sp.add_argument("--intra", action="store_true", help="intra-state (CGST+SGST)")
    sp.add_argument("--cess-rate", default=0)
    sp.add_argument("--cess-fixed", default=0)

    ip = sub.add_parser("interest", help="interest under s50 / s56")
    ip.add_argument("--amount", required=True)
    ip.add_argument("--from", dest="from_date", required=True, help="YYYY-MM-DD")
    ip.add_argument("--to", dest="to_date", required=True, help="YYYY-MM-DD")
    ip.add_argument("--rate", default=None, help="override the statutory rate")
    ip.add_argument("--basis", default="delayed_payment",
                    choices=["delayed_payment", "wrong_itc",
                             "delayed_refund", "refund_appeal"])

    lp = sub.add_parser("latefee", help="late fee under s47")
    lp.add_argument("--form", required=True)
    lp.add_argument("--days", type=int, required=True)
    lp.add_argument("--nil", action="store_true")
    lp.add_argument("--aato", default=0, help="AATO of the preceding FY, in rupees")
    lp.add_argument("--state-turnover", default=None,
                    help="turnover in the state/UT — needed for the GSTR-9 cap")

    np_ = sub.add_parser("liability", help="net payable and credit utilisation")
    np_.add_argument("--json", required=True,
                     help='file with {"output":{...},"itc":{...},'
                          '"reversals":{...},"cash_balance":{...},'
                          '"monthly_taxable_turnover":N}')
    np_.add_argument("--rounding", default="exact", choices=["exact", "portal"],
                     help="'portal' rounds to the nearest rupee before offsetting, "
                          "matching the portal's utilisation step")

    sub.add_parser("selftest", help="run built-in tests")

    # Accept --selftest as well, so every script in this directory answers to the
    # same flag. Checked before parse_args, because the subparsers would reject it
    # as an unrecognised argument.
    if "--selftest" in sys.argv[1:]:
        return selftest()

    args = p.parse_args()

    if args.cmd == "split":
        _dump(split_tax(args.value, args.rate, args.intra,
                        args.cess_rate, args.cess_fixed))
    elif args.cmd == "interest":
        _dump(interest(args.amount, _date(args.from_date), _date(args.to_date),
                       args.rate, args.basis))
    elif args.cmd == "latefee":
        _dump(late_fee(args.form, args.days, args.nil, args.aato,
                       args.state_turnover))
    elif args.cmd == "liability":
        with open(args.json, encoding="utf-8") as fh:
            cfg = json.load(fh)
        _dump(net_liability(cfg.get("output", {}), cfg.get("itc", {}),
                            cfg.get("reversals"), cfg.get("cash_balance"),
                            cfg.get("monthly_taxable_turnover"),
                            args.rounding))
    elif args.cmd == "selftest":
        return selftest()
    else:
        p.print_help()
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
