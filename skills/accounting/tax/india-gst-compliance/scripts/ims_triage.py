#!/usr/bin/env python3
"""Three-way IMS triage: local invoices x IMS records x payment evidence.

`reconcile.py` answers "do these two lists match". This answers the question that
actually has to be decided on the portal: **for each IMS record, do I Accept,
Reject or keep Pending — and why.**

Two sources are not enough for that. An IMS record with no local invoice is not
automatically bogus (the invoice may simply not have reached the folder yet), and
an invoice paid from a partner's personal account is not automatically
disqualified. Payment evidence is what separates "I have not found the document"
from "this is not mine".

The other job here is the **missing-document list**: the exact identifiers to go
and look for, produced *early* — while GSTR-1 is still being prepared — so the
search happens in parallel rather than blocking GSTR-3B at the end.

    Local invoice   IMS record   Payment evidence   Recommended action
    -------------   ----------   ----------------   ------------------
    exact match     present      available          ACCEPT
    exact match     present      none found         ACCEPT, flag 180-day tracking
    missing         present      available          PENDING - obtain the invoice
    missing         present      none found         PENDING - verify it is yours
    tax-head/POS
      mismatch      present      any                PENDING - supplier must amend
    value mismatch  present      any                PENDING - reconcile first
    present         absent       any                cannot claim; chase supplier

Nothing here decides anything on the portal. It produces a recommendation table
for a human to confirm, one record at a time, per the Tier 2 rule in SKILL.md.

Input CSVs (extra columns are carried through):

    invoices.csv   gstin, doc_no, doc_date, taxable, igst, cgst, sgst, cess [, pos, name]
    ims.csv        gstin, doc_no, doc_date, taxable, igst, cgst, sgst, cess
                   [, pos, name, ims_status, eligible]
    payments.csv   gstin, doc_no, amount [, paid_on, paid_from, reference]
                   -- doc_no may be blank; matching then falls back to gstin+amount

Usage:
    python3 ims_triage.py --invoices inv.csv --ims ims.csv --payments bank.csv \\
        --out work/ims-triage.csv --missing work/missing-documents.md
    python3 ims_triage.py --selftest
"""

from __future__ import annotations

import argparse
import csv
import io
import sys
from collections import defaultdict
from decimal import Decimal

from reconcile import TAX_COLS, _load_rows, dec, load, norm_doc, norm_gstin

# Action, why, and whether the record is safe to claim this period.
ACTIONS = {
    "ACCEPT": "Matches a local invoice; values agree",
    "ACCEPT_NO_PAYMENT_EVIDENCE": "Matches a local invoice, but no payment traced — "
                                  "claim, and track the 180-day Rule 37 deadline",
    "PENDING_NO_INVOICE": "In IMS with no local invoice — obtain the invoice before "
                          "claiming; s16(2)(a) requires possession of it",
    "PENDING_UNVERIFIED": "In IMS, no local invoice and no payment trace — verify "
                          "this supply is yours before accepting anything",
    "PENDING_HEAD_MISMATCH": "Tax head or place of supply differs from the local "
                             "invoice — the supplier must amend; a wrong head "
                             "cannot be corrected by set-off",
    "PENDING_VALUE_MISMATCH": "Value differs from the local invoice — reconcile "
                              "before claiming",
    "NOT_IN_IMS": "Local invoice with no IMS record — supplier has not filed. "
                  "Cannot claim this period; track within the s16(4) limit",
}

SAFE_TO_CLAIM = {"ACCEPT", "ACCEPT_NO_PAYMENT_EVIDENCE"}

FIELDS = ["action", "reason", "safe_to_claim", "gstin", "name", "doc_no",
          "doc_date", "invoice_taxable", "ims_taxable", "invoice_tax", "ims_tax",
          "tax_diff", "invoice_pos", "ims_pos", "head_mismatch", "payment_found",
          "paid_from", "payment_reference", "ims_status", "owner", "status"]


def load_payments(path_or_fh, source: str = "payments") -> list[dict]:
    """Payment evidence is looser than an invoice register: doc_no may be blank."""
    fh = open(path_or_fh, newline="", encoding="utf-8-sig") \
        if isinstance(path_or_fh, str) else path_or_fh
    try:
        reader = csv.DictReader(fh)
        if reader.fieldnames is None:
            raise ValueError(f"{source}: file is empty")
        cols = {(c or "").strip().lower() for c in reader.fieldnames}
        for req in ("gstin", "amount"):
            if req not in cols:
                raise ValueError(f"{source}: missing required column '{req}'")
        rows = []
        for i, raw in enumerate(reader, start=2):
            row = {k.strip().lower(): (v.strip() if isinstance(v, str) else v)
                   for k, v in raw.items() if k}
            try:
                row["amount"] = dec(row.get("amount"))
            except ValueError as exc:
                raise ValueError(f"{source} line {i}: {exc}") from exc
            row["_gstin"] = norm_gstin(row.get("gstin"))
            row["_doc"] = norm_doc(row.get("doc_no")) if row.get("doc_no") else ""
            if not row["_gstin"]:
                raise ValueError(f"{source} line {i}: gstin cannot be blank")
            rows.append(row)
        return rows
    finally:
        if isinstance(path_or_fh, str):
            fh.close()


def _find_payment(rec: dict, payments: list[dict], used: set[int],
                  tolerance: Decimal) -> dict | None:
    """Match on GSTIN + document number, else GSTIN + gross amount within tolerance.

    The amount fallback exists because bank narrations rarely carry an invoice
    number. It is deliberately conservative: it only fires when exactly one
    unused payment for that supplier is close enough in value.
    """
    gross = rec["taxable"] + rec["_tax"]
    exact = [p for p in payments
             if id(p) not in used and p["_gstin"] == rec["_gstin"]
             and p["_doc"] and p["_doc"] == rec["_doc"]]
    if exact:
        used.add(id(exact[0]))
        return exact[0]
    near = [p for p in payments
            if id(p) not in used and p["_gstin"] == rec["_gstin"]
            and abs(p["amount"] - gross) <= tolerance]
    if len(near) == 1:
        used.add(id(near[0]))
        return near[0]
    return None


def triage(invoices: list[dict], ims: list[dict], payments: list[dict] | None = None,
           tolerance: Decimal = Decimal("1"),
           payment_tolerance: Decimal = Decimal("2")) -> dict:
    payments = payments or []
    inv_index: dict[tuple[str, str], list[dict]] = defaultdict(list)
    for r in invoices:
        inv_index[(r["_gstin"], r["_doc"])].append(r)

    used_inv: set[int] = set()
    used_pay: set[int] = set()
    rows: list[dict] = []

    for rec in ims:
        cands = [i for i in inv_index.get((rec["_gstin"], rec["_doc"]), [])
                 if id(i) not in used_inv]
        if not cands:
            # Same conservative fallback reconcile.py uses: GSTIN + date, only
            # where it is unambiguous on both sides.
            same_key = [i for i in invoices
                        if id(i) not in used_inv and i["_gstin"] == rec["_gstin"]
                        and str(i.get("doc_date", "")).strip()
                        == str(rec.get("doc_date", "")).strip()
                        and str(rec.get("doc_date", "")).strip()]
            peers = [o for o in ims
                     if o["_gstin"] == rec["_gstin"]
                     and str(o.get("doc_date", "")).strip()
                     == str(rec.get("doc_date", "")).strip()]
            if len(same_key) == 1 and len(peers) == 1:
                cands = same_key

        inv = cands[0] if cands else None
        if inv is not None:
            used_inv.add(id(inv))

        pay = _find_payment(rec, payments, used_pay, payment_tolerance)

        inv_pos = str(inv.get("pos", "")).strip() if inv else ""
        ims_pos = str(rec.get("pos", "")).strip()
        head_mismatch = bool(
            inv and (any(abs(inv[c] - rec[c]) > tolerance for c in TAX_COLS)
                     and abs(inv["_tax"] - rec["_tax"]) <= tolerance))
        pos_mismatch = bool(inv and inv_pos and ims_pos and inv_pos != ims_pos)
        value_mismatch = bool(inv and abs(inv["_tax"] - rec["_tax"]) > tolerance)

        if inv is None:
            action = "PENDING_NO_INVOICE" if pay else "PENDING_UNVERIFIED"
        elif value_mismatch:
            action = "PENDING_VALUE_MISMATCH"
        elif head_mismatch or pos_mismatch:
            action = "PENDING_HEAD_MISMATCH"
        elif pay:
            action = "ACCEPT"
        else:
            action = "ACCEPT_NO_PAYMENT_EVIDENCE"

        rows.append({
            "action": action, "reason": ACTIONS[action],
            "safe_to_claim": "yes" if action in SAFE_TO_CLAIM else "no",
            "gstin": rec.get("gstin", ""),
            "name": (inv or rec).get("name", ""),
            "doc_no": rec.get("doc_no", ""), "doc_date": rec.get("doc_date", ""),
            "invoice_taxable": inv["taxable"] if inv else Decimal(0),
            "ims_taxable": rec["taxable"],
            "invoice_tax": inv["_tax"] if inv else Decimal(0),
            "ims_tax": rec["_tax"],
            "tax_diff": (inv["_tax"] - rec["_tax"]) if inv else Decimal(0),
            "invoice_pos": inv_pos, "ims_pos": ims_pos,
            "head_mismatch": "yes" if (head_mismatch or pos_mismatch) else "",
            "payment_found": "yes" if pay else "no",
            "paid_from": (pay or {}).get("paid_from", ""),
            "payment_reference": (pay or {}).get("reference", ""),
            "ims_status": rec.get("ims_status", ""),
            "owner": "", "status": "open",
        })

    for inv in invoices:
        if id(inv) in used_inv:
            continue
        pay = _find_payment(inv, payments, used_pay, payment_tolerance)
        rows.append({
            "action": "NOT_IN_IMS", "reason": ACTIONS["NOT_IN_IMS"],
            "safe_to_claim": "no", "gstin": inv.get("gstin", ""),
            "name": inv.get("name", ""), "doc_no": inv.get("doc_no", ""),
            "doc_date": inv.get("doc_date", ""),
            "invoice_taxable": inv["taxable"], "ims_taxable": Decimal(0),
            "invoice_tax": inv["_tax"], "ims_tax": Decimal(0),
            "tax_diff": inv["_tax"], "invoice_pos": str(inv.get("pos", "")).strip(),
            "ims_pos": "", "head_mismatch": "",
            "payment_found": "yes" if pay else "no",
            "paid_from": (pay or {}).get("paid_from", ""),
            "payment_reference": (pay or {}).get("reference", ""),
            "ims_status": "", "owner": "", "status": "open",
        })

    summary: dict[str, dict] = defaultdict(lambda: {"count": 0, "tax": Decimal(0)})
    for r in rows:
        s = summary[r["action"]]
        s["count"] += 1
        s["tax"] += r["ims_tax"] if r["action"] != "NOT_IN_IMS" else r["invoice_tax"]

    claimable = sum(r["ims_tax"] for r in rows if r["safe_to_claim"] == "yes")
    deferred = sum(r["ims_tax"] for r in rows
                   if r["action"].startswith("PENDING"))
    unavailable = sum(r["invoice_tax"] for r in rows if r["action"] == "NOT_IN_IMS")

    return {
        "rows": rows, "summary": {k: dict(v) for k, v in sorted(summary.items())},
        "totals": {
            "ims_records": len(ims), "local_invoices": len(invoices),
            "payments": len(payments),
            "claimable_tax": claimable, "deferred_tax": deferred,
            "unavailable_tax": unavailable,
        },
    }


def missing_documents(result: dict) -> list[dict]:
    """Exact identifiers to go and find, so the search runs in parallel."""
    out = []
    for r in result["rows"]:
        if r["action"] in ("PENDING_NO_INVOICE", "PENDING_UNVERIFIED"):
            out.append({"what": "supplier invoice (not in the local folder)",
                        "identifier": r["doc_no"], "supplier": r["name"] or r["gstin"],
                        "date": r["doc_date"], "tax": r["ims_tax"],
                        "why": "cannot claim without possession of the invoice "
                               "(s16(2)(a)); IMS record stays Pending until found"})
        elif r["action"] == "PENDING_HEAD_MISMATCH":
            out.append({"what": "corrected invoice / supplier amendment",
                        "identifier": r["doc_no"], "supplier": r["name"] or r["gstin"],
                        "date": r["doc_date"], "tax": r["ims_tax"],
                        "why": f"local shows POS {r['invoice_pos'] or '?'} and IMS "
                               f"shows {r['ims_pos'] or '?'} — the tax head cannot "
                               f"be corrected by set-off"})
        elif r["action"] == "PENDING_VALUE_MISMATCH":
            out.append({"what": "clarification of the correct value",
                        "identifier": r["doc_no"], "supplier": r["name"] or r["gstin"],
                        "date": r["doc_date"], "tax": r["ims_tax"],
                        "why": f"local invoice and IMS differ by {r['tax_diff']} "
                               f"in tax"})
    return out


def render_missing(items: list[dict]) -> str:
    if not items:
        return ("# Missing documents\n\nNone. Every IMS record is supported by a "
                "local invoice.\n")
    out = ["# Missing documents", "",
           f"{len(items)} item(s) to find. Start looking now — this list is produced "
           "while GSTR-1 is still being prepared so the search runs in parallel "
           "rather than blocking GSTR-3B at the end.", "",
           "| # | Identifier | Supplier | Date | Tax | What is needed | Why it matters |",
           "|---|---|---|---|---|---|---|"]
    for i, m in enumerate(items, start=1):
        out.append(f"| {i} | `{m['identifier']}` | {m['supplier']} | {m['date']} | "
                   f"{m['tax']} | {m['what']} | {m['why']} |")
    out += ["", "Each of these keeps its IMS record in **Pending** until resolved. "
                "Pending is time-limited and always bounded by the s16(4) deadline — "
                "a record left pending past its window is credit lost."]
    return "\n".join(out) + "\n"


def write_csv(rows: list[dict], out) -> None:
    w = csv.DictWriter(out, fieldnames=FIELDS, extrasaction="ignore")
    w.writeheader()
    order = {a: i for i, a in enumerate(
        ["PENDING_UNVERIFIED", "PENDING_HEAD_MISMATCH", "PENDING_VALUE_MISMATCH",
         "PENDING_NO_INVOICE", "NOT_IN_IMS", "ACCEPT_NO_PAYMENT_EVIDENCE", "ACCEPT"])}
    for r in sorted(rows, key=lambda x: (order.get(x["action"], 9), -abs(x["ims_tax"]))):
        w.writerow({k: (str(v) if isinstance(v, Decimal) else v)
                    for k, v in r.items()})


def print_summary(res: dict) -> None:
    t = res["totals"]
    print(f"IMS triage: {t['ims_records']} IMS record(s), {t['local_invoices']} local "
          f"invoice(s), {t['payments']} payment(s)")
    print()
    print(f"  {'Recommended action':<28}{'Count':>7}{'Tax':>14}  Why")
    for action, s in res["summary"].items():
        print(f"  {action:<28}{s['count']:>7}{str(s['tax']):>14}  {ACTIONS[action]}")
    print()
    print(f"  Safe to claim this period : {t['claimable_tax']}")
    print(f"  Deferred (pending)        : {t['deferred_tax']}")
    print(f"  Not in IMS, cannot claim  : {t['unavailable_tax']}")
    pend = sum(s["count"] for a, s in res["summary"].items() if a.startswith("PENDING"))
    if pend:
        print()
        print(f"  {pend} record(s) recommended as Pending. Confirm each one "
              f"individually before acting in IMS — and remember that taking no "
              f"action is deemed acceptance, so every record needs a decision.")


def selftest() -> int:
    failures = []

    invoices = io.StringIO(
        "gstin,name,doc_no,doc_date,taxable,igst,cgst,sgst,cess,pos\n"
        "27AAPFU0939F1ZV,Matched Co,INV/001,2026-06-01,100000,0,9000,9000,0,27\n"
        "27AAPFU0939F1ZV,Unpaid Co,INV/002,2026-06-02,50000,0,4500,4500,0,27\n"
        "29AAACR5055K1ZD,HeadDiff Co,INV/003,2026-06-03,10000,1800,0,0,0,27\n"
        "29AAACR5055K1ZD,ValueDiff Co,INV/004,2026-06-04,20000,3600,0,0,0,29\n"
        "33AAACT2727Q1ZW,NotInIms Co,INV/005,2026-06-05,30000,5400,0,0,0,33\n"
    )
    ims = io.StringIO(
        "gstin,name,doc_no,doc_date,taxable,igst,cgst,sgst,cess,pos\n"
        "27AAPFU0939F1ZV,Matched Co,INV-001,2026-06-01,100000,0,9000,9000,0,27\n"
        "27AAPFU0939F1ZV,Unpaid Co,INV/002,2026-06-02,50000,0,4500,4500,0,27\n"
        "29AAACR5055K1ZD,HeadDiff Co,INV/003,2026-06-03,10000,0,900,900,0,29\n"
        "29AAACR5055K1ZD,ValueDiff Co,INV/004,2026-06-04,25000,4500,0,0,0,29\n"
        "27AAPFU0939F1ZV,Stranger Co,RCT2026-06-01043,2026-06-08,80000,0,7200,7200,0,27\n"
        "27AAPFU0939F1ZV,Paid Unknown,RCT2026-06-01388,2026-06-09,10000,0,900,900,0,27\n"
    )
    payments = io.StringIO(
        "gstin,doc_no,amount,paid_on,paid_from,reference\n"
        "27AAPFU0939F1ZV,INV/001,118000,2026-06-05,business current,NEFT001\n"
        "27AAPFU0939F1ZV,,11800,2026-06-11,partner personal,UPI778\n"
    )
    res = triage(_load_rows(invoices, "inv"), _load_rows(ims, "ims"),
                 load_payments(payments, "pay"))
    got = {a: s["count"] for a, s in res["summary"].items()}
    want = {"ACCEPT": 1, "ACCEPT_NO_PAYMENT_EVIDENCE": 1,
            "PENDING_HEAD_MISMATCH": 1, "PENDING_VALUE_MISMATCH": 1,
            "PENDING_UNVERIFIED": 1, "PENDING_NO_INVOICE": 1, "NOT_IN_IMS": 1}
    if got != want:
        failures.append(f"triage classification: got {got}, expected {want}")

    by_doc = {r["doc_no"]: r for r in res["rows"]}

    # The partner-paid record must be traced by amount and its source preserved:
    # a personal bank account does not by itself disqualify the invoice.
    paid = by_doc.get("RCT2026-06-01388")
    if not paid or paid["payment_found"] != "yes":
        failures.append("amount-fallback payment matching failed")
    elif paid["paid_from"] != "partner personal":
        failures.append(f"payment source lost: {paid['paid_from']!r}")
    elif paid["action"] != "PENDING_NO_INVOICE":
        failures.append(f"paid-but-no-invoice should be PENDING_NO_INVOICE, "
                        f"got {paid['action']}")

    # No invoice and no payment is the weakest case and must say so.
    if by_doc["RCT2026-06-01043"]["action"] != "PENDING_UNVERIFIED":
        failures.append("unverified stranger record misclassified")

    # A head/POS mismatch must not be reported as safe to claim.
    hd = by_doc["INV/003"]
    if hd["safe_to_claim"] != "no" or hd["head_mismatch"] != "yes":
        failures.append(f"head mismatch not flagged: {hd}")

    # Nothing pending may be counted as claimable.
    if any(r["safe_to_claim"] == "yes" for r in res["rows"]
           if r["action"].startswith("PENDING")):
        failures.append("a pending record was marked safe to claim")

    # Claimable total must be exactly the two accepted records.
    if res["totals"]["claimable_tax"] != Decimal("27000"):
        failures.append(f"claimable total wrong: {res['totals']['claimable_tax']}")

    # Missing-document list must name the exact identifiers.
    md = missing_documents(res)
    ids = {m["identifier"] for m in md}
    for want_id in ("RCT2026-06-01043", "RCT2026-06-01388", "INV/003", "INV/004"):
        if want_id not in ids:
            failures.append(f"missing-document list omitted {want_id}")
    if "INV/001" in ids:
        failures.append("missing-document list included a fully matched invoice")
    text = render_missing(md)
    if "RCT2026-06-01043" not in text or "s16(4)" not in text:
        failures.append("rendered missing-document list is incomplete")
    if "None." not in render_missing([]):
        failures.append("empty missing-document list did not say so")

    # CSV output round-trips, unresolved first.
    buf = io.StringIO()
    write_csv(res["rows"], buf)
    written = list(csv.DictReader(io.StringIO(buf.getvalue())))
    if len(written) != len(res["rows"]):
        failures.append("CSV write dropped rows")
    if written[0]["action"].startswith("ACCEPT"):
        failures.append("CSV not sorted with unresolved actions first")

    # Works with no payment evidence at all — everything falls back safely.
    res2 = triage(_load_rows(io.StringIO(invoices.getvalue()), "inv"),
                  _load_rows(io.StringIO(ims.getvalue()), "ims"), [])
    if any(r["action"] == "ACCEPT" for r in res2["rows"]):
        failures.append("ACCEPT issued with no payment evidence supplied")
    if not any(r["action"] == "ACCEPT_NO_PAYMENT_EVIDENCE" for r in res2["rows"]):
        failures.append("matched invoice without payment evidence misclassified")

    # An ambiguous amount must not be matched to a payment.
    amb_i = io.StringIO("gstin,doc_no,doc_date,taxable,igst,cgst,sgst,cess\n"
                        "27AAPFU0939F1ZV,A1,2026-06-01,1000,180,0,0,0\n")
    amb_m = io.StringIO("gstin,doc_no,doc_date,taxable,igst,cgst,sgst,cess\n"
                        "27AAPFU0939F1ZV,A1,2026-06-01,1000,180,0,0,0\n")
    amb_p = io.StringIO("gstin,doc_no,amount\n"
                        "27AAPFU0939F1ZV,,1180\n27AAPFU0939F1ZV,,1180\n")
    amb = triage(_load_rows(amb_i, "i"), _load_rows(amb_m, "m"),
                 load_payments(amb_p, "p"))
    if amb["rows"][0]["payment_found"] != "no":
        failures.append("ambiguous payment was matched; it should not be")

    # Malformed payment input must fail loudly.
    for label, text_in in [("no amount", "gstin,doc_no\n27AAPFU0939F1ZV,X\n"),
                           ("no gstin", "doc_no,amount\nX,100\n"),
                           ("bad amount", "gstin,amount\n27AAPFU0939F1ZV,abc\n"),
                           ("empty", "")]:
        try:
            load_payments(io.StringIO(text_in), label)
            failures.append(f"no error raised for {label}")
        except ValueError:
            pass

    if failures:
        print("SELFTEST FAILED")
        for f in failures:
            print("  -", f)
        return 1
    print("SELFTEST PASSED (three-way classification, payment fallback matching, "
          "partner-paid handling, missing-document list, CSV output, no-payments "
          "mode, ambiguity guard, input validation)")
    return 0


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--invoices", help="local purchase invoice register CSV")
    p.add_argument("--ims", help="IMS / GSTR-2B export CSV")
    p.add_argument("--payments", default=None, help="bank or payment evidence CSV")
    p.add_argument("--out", default=None, help="write the triage table here (CSV)")
    p.add_argument("--missing", default=None,
                   help="write the missing-document list here (markdown)")
    p.add_argument("--tolerance", default="1", help="rupee tolerance on tax")
    p.add_argument("--payment-tolerance", default="2",
                   help="rupee tolerance when matching a payment by amount")
    p.add_argument("--selftest", action="store_true")
    args = p.parse_args()

    if args.selftest:
        return selftest()
    if not (args.invoices and args.ims):
        p.print_help()
        return 2

    res = triage(load(args.invoices), load(args.ims),
                 load_payments(args.payments) if args.payments else [],
                 dec(args.tolerance), dec(args.payment_tolerance))
    print_summary(res)

    if args.out:
        with open(args.out, "w", newline="", encoding="utf-8") as fh:
            write_csv(res["rows"], fh)
        print(f"\n  Triage table written to {args.out}")

    md = missing_documents(res)
    if args.missing:
        with open(args.missing, "w", encoding="utf-8") as fh:
            fh.write(render_missing(md))
        print(f"  Missing-document list written to {args.missing} ({len(md)} item(s))")
    elif md:
        print()
        print(render_missing(md))

    if not args.payments:
        print("\n  No payment evidence supplied. Every match is therefore "
              "ACCEPT_NO_PAYMENT_EVIDENCE at best — pass --payments to separate "
              "'document not found yet' from 'not ours'.")

    return 1 if any(r["safe_to_claim"] == "no" for r in res["rows"]) else 0


if __name__ == "__main__":
    sys.exit(main())
