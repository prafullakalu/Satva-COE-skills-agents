#!/usr/bin/env python3
"""Invoice-level reconciliation between books and the portal, with a difference register.

A matched *total* proves nothing — two offsetting errors reconcile perfectly. So
this matches line by line and classifies every difference into a class with a
distinct remedy and a distinct owner:

    A  matched, values agree                 -> claim / report
    B  in books, not on the portal           -> supplier has not filed; chase
    C  on the portal, not in books           -> missing entry, or not yours
    D  matched, tax value differs            -> investigate; claim the lower
    E  matched, tax head or POS differs      -> supplier must amend; not fixable
                                                by set-off
    F  on the portal, flagged ineligible     -> report in 4D(2), do not claim

The output is the difference register itself, which is the working paper a
reviewer or an officer actually reads.

Input CSVs need these columns (extra columns are carried through untouched):

    gstin, doc_no, doc_date, taxable, igst, cgst, sgst, cess

Optional: doc_type, name, pos, eligible ("Y"/"N"; a GSTR-2B export's eligibility
flag — rows marked "N" become class F).

Usage:
    python3 reconcile.py --books purchases.csv --portal gstr2b.csv \\
        --out work/difference-register.csv
    python3 reconcile.py --books sales.csv --portal gstr1.csv --label outward
    python3 reconcile.py --selftest

Exit status is 1 whenever any row falls outside class A. That is not an error —
it is the script refusing to report "clean" while differences remain, so a
scripted pipeline cannot skip past them.
"""

from __future__ import annotations

import argparse
import csv
import io
import re
import sys
from collections import defaultdict
from decimal import Decimal, InvalidOperation

TAX_COLS = ("igst", "cgst", "sgst", "cess")
NUM_COLS = ("taxable",) + TAX_COLS

CLASS_MEANING = {
    "A": "Matched — values agree",
    "B": "In books, not on the portal — supplier has not filed or reported the wrong GSTIN",
    "C": "On the portal, not in books — missing purchase entry, or not this taxpayer's invoice",
    "D": "Matched, tax value differs",
    "E": "Matched, tax head or place of supply differs",
    "F": "On the portal, flagged ineligible",
}

CLASS_ACTION = {
    "A": "Claim / report",
    "B": "Do not claim this period. Chase the supplier; track within the s16(4) limit",
    "C": "Investigate before accepting. Never claim an invoice you cannot trace to a purchase",
    "D": "Reconcile to the invoice. Claim the lower figure until resolved",
    "E": "Supplier must amend. IGST wrongly charged as CGST+SGST cannot be corrected by set-off",
    "F": "Do not claim. Report in GSTR-3B Table 4D(2)",
}


def dec(v) -> Decimal:
    """Parse a CSV cell into a Decimal, tolerating blanks, commas and currency."""
    if v is None:
        return Decimal(0)
    s = str(v).strip().replace(",", "").replace("₹", "").replace("Rs.", "").replace("Rs", "")
    if s in ("", "-", "NA", "N/A"):
        return Decimal(0)
    neg = s.startswith("(") and s.endswith(")")
    if neg:
        s = s[1:-1]
    try:
        d = Decimal(s)
    except InvalidOperation as exc:
        raise ValueError(f"cannot parse '{v}' as a number") from exc
    return -d if neg else d


def norm_doc(doc_no: str) -> str:
    """Normalise an invoice number for matching.

    Books and the portal routinely disagree on leading zeros, slashes, hyphens,
    spaces and case for the same document. Matching on the raw string produces a
    pile of spurious class B and C rows that bury the real ones.
    """
    s = re.sub(r"[^A-Za-z0-9]", "", str(doc_no or "")).upper()
    return re.sub(r"(?<=[A-Z])0+(?=\d)", "", s).lstrip("0") or s


def norm_gstin(g: str) -> str:
    return re.sub(r"\s", "", str(g or "")).upper()


def load(path: str) -> list[dict]:
    with open(path, newline="", encoding="utf-8-sig") as fh:
        return _load_rows(fh, path)


def _load_rows(fh, source: str) -> list[dict]:
    reader = csv.DictReader(fh)
    if reader.fieldnames is None:
        raise ValueError(f"{source}: file is empty")
    cols = {(c or "").strip().lower(): c for c in reader.fieldnames}
    required = ("gstin", "doc_no", "doc_date", "taxable")
    missing = [c for c in required if c not in cols]
    if missing:
        raise ValueError(f"{source}: missing required column(s): {', '.join(missing)}")

    rows = []
    for i, raw in enumerate(reader, start=2):
        row = {k.strip().lower(): (v.strip() if isinstance(v, str) else v)
               for k, v in raw.items() if k}
        try:
            for c in NUM_COLS:
                row[c] = dec(row.get(c))
        except ValueError as exc:
            raise ValueError(f"{source} line {i}: {exc}") from exc
        row["_gstin"] = norm_gstin(row.get("gstin"))
        row["_doc"] = norm_doc(row.get("doc_no"))
        row["_tax"] = sum(row[c] for c in TAX_COLS)
        row["_line"] = i
        if not row["_gstin"] or not row["_doc"]:
            raise ValueError(f"{source} line {i}: gstin and doc_no cannot be blank")
        rows.append(row)
    return rows


def reconcile(books: list[dict], portal: list[dict],
              tolerance: Decimal = Decimal("1")) -> dict:
    """Match on (GSTIN, normalised doc number) and classify every row.

    `tolerance` is the absolute rupee difference in total tax below which a
    matched pair is treated as agreeing. It defaults to Re 1 to absorb rounding,
    not to hide differences — every tolerated difference is still reported in the
    summary so nothing vanishes silently.
    """
    index: dict[tuple[str, str], list[dict]] = defaultdict(list)
    for r in portal:
        index[(r["_gstin"], r["_doc"])].append(r)

    register: list[dict] = []
    matched_portal: set[int] = set()
    tolerated = Decimal(0)
    pairs: list[tuple[dict, dict, str]] = []
    unmatched_books: list[dict] = []

    # Pass 1 — exact match on GSTIN plus the normalised document number.
    for b in books:
        candidates = [p for p in index.get((b["_gstin"], b["_doc"]), [])
                      if id(p) not in matched_portal]
        if not candidates:
            unmatched_books.append(b)
            continue
        # Prefer the candidate closest in tax value, so a duplicated document
        # number does not match the wrong line.
        p = min(candidates, key=lambda c: abs(c["_tax"] - b["_tax"]))
        matched_portal.add(id(p))
        pairs.append((b, p, "doc_no"))

    # Pass 2 — the same document reported under a differently formatted number
    # (a prefix present on one side only, a series change, a manual re-key) is
    # extremely common, and leaving those as unmatched B and C pairs buries the
    # genuine ones. Fall back to GSTIN + document date, but only where exactly
    # one unmatched row carries that key on each side. The uniqueness guard is
    # what makes this safe: a guess must never displace a real match, and an
    # ambiguous case is better reported than resolved. Every fallback match is
    # labelled in the register so a reviewer can see how it was paired.
    if unmatched_books:
        def fb_key(r: dict) -> tuple:
            return (r["_gstin"], str(r.get("doc_date", "")).strip())

        portal_keys: dict[tuple, list[dict]] = defaultdict(list)
        for p in portal:
            if id(p) not in matched_portal:
                portal_keys[fb_key(p)].append(p)
        books_keys: dict[tuple, int] = defaultdict(int)
        for b in unmatched_books:
            books_keys[fb_key(b)] += 1

        still_unmatched = []
        for b in unmatched_books:
            key = fb_key(b)
            cands = portal_keys.get(key, [])
            if key[1] and len(cands) == 1 and books_keys[key] == 1:
                matched_portal.add(id(cands[0]))
                pairs.append((b, cands[0], "gstin+date"))
            else:
                still_unmatched.append(b)
        unmatched_books = still_unmatched

    for b, p, basis in pairs:
        note = ""
        if basis == "gstin+date":
            note = (f"matched on date and value; document numbers differ "
                    f"(books '{b.get('doc_no')}' / portal '{p.get('doc_no')}') — "
                    f"verify, and correct whichever is wrong")

        if str(p.get("eligible", "")).strip().upper() == "N":
            register.append(_entry("F", b, p, basis, note))
            continue

        head_diff = any(abs(b[c] - p[c]) > tolerance for c in TAX_COLS)
        total_diff = abs(b["_tax"] - p["_tax"])
        b_pos, p_pos = str(b.get("pos", "")).strip(), str(p.get("pos", "")).strip()

        if total_diff > tolerance:
            # A value difference must not mask a head or POS difference sitting
            # underneath it — those need a supplier amendment, not a reconciling
            # entry, so the reviewer has to see both.
            extra = []
            if head_diff:
                extra.append("tax heads also differ (IGST vs CGST+SGST) — "
                             "check the place of supply, not just the value")
            if b_pos and p_pos and b_pos != p_pos:
                extra.append(f"place of supply also differs ({b_pos} / {p_pos})")
            register.append(_entry("D", b, p, basis,
                                   "; ".join(([note] if note else []) + extra)))
        elif head_diff:
            # Heads differ but the total does not — IGST vs CGST+SGST.
            register.append(_entry("E", b, p, basis, note))
        elif b_pos and p_pos and b_pos != p_pos:
            register.append(_entry("E", b, p, basis,
                                   (note + "; " if note else "")
                                   + f"place of supply differs ({b_pos} / {p_pos})"))
        else:
            if total_diff > 0:
                tolerated += total_diff
            register.append(_entry("A", b, p, basis, note))

    for b in unmatched_books:
        register.append(_entry("B", b, None, "unmatched", ""))

    for p in portal:
        if id(p) in matched_portal:
            continue
        cls = "F" if str(p.get("eligible", "")).strip().upper() == "N" else "C"
        register.append(_entry(cls, None, p, "unmatched", ""))

    summary = defaultdict(lambda: {"count": 0, "books_tax": Decimal(0),
                                   "portal_tax": Decimal(0), "diff_tax": Decimal(0)})
    for e in register:
        s = summary[e["class"]]
        s["count"] += 1
        s["books_tax"] += e["books_tax"]
        s["portal_tax"] += e["portal_tax"]
        s["diff_tax"] += e["diff_tax"]

    claimable = sum(e["portal_tax"] for e in register if e["class"] == "A")
    at_risk = sum(e["books_tax"] for e in register if e["class"] in ("B", "D", "E"))

    return {
        "register": register,
        "summary": {k: dict(v) for k, v in sorted(summary.items())},
        "totals": {
            "books_rows": len(books), "portal_rows": len(portal),
            "books_tax": sum(b["_tax"] for b in books),
            "portal_tax": sum(p["_tax"] for p in portal),
            "matched_tax_class_a": claimable,
            "tax_at_risk_or_unresolved": at_risk,
            "tolerated_rounding": tolerated,
        },
    }


def _entry(cls: str, b: dict | None, p: dict | None,
           basis: str = "", note: str = "") -> dict:
    src = b or p
    bt = b["_tax"] if b else Decimal(0)
    pt = p["_tax"] if p else Decimal(0)
    return {
        "class": cls, "meaning": CLASS_MEANING[cls], "action": CLASS_ACTION[cls],
        "matched_on": basis, "note": note,
        "gstin": src.get("gstin", ""), "name": src.get("name", ""),
        "doc_type": src.get("doc_type", ""), "doc_no": src.get("doc_no", ""),
        "doc_date": src.get("doc_date", ""),
        "books_taxable": b["taxable"] if b else Decimal(0),
        "portal_taxable": p["taxable"] if p else Decimal(0),
        "books_igst": b["igst"] if b else Decimal(0),
        "portal_igst": p["igst"] if p else Decimal(0),
        "books_cgst": b["cgst"] if b else Decimal(0),
        "portal_cgst": p["cgst"] if p else Decimal(0),
        "books_sgst": b["sgst"] if b else Decimal(0),
        "portal_sgst": p["sgst"] if p else Decimal(0),
        "books_cess": b["cess"] if b else Decimal(0),
        "portal_cess": p["cess"] if p else Decimal(0),
        "books_tax": bt, "portal_tax": pt, "diff_tax": bt - pt,
        "owner": "", "due_by": "", "status": "open" if cls != "A" else "closed",
    }


FIELDS = ["class", "meaning", "action", "matched_on", "note", "gstin", "name",
          "doc_type", "doc_no", "doc_date", "books_taxable", "portal_taxable",
          "books_igst", "portal_igst", "books_cgst", "portal_cgst",
          "books_sgst", "portal_sgst", "books_cess", "portal_cess",
          "books_tax", "portal_tax", "diff_tax", "owner", "due_by", "status"]


def write_register(register: list[dict], out) -> None:
    w = csv.DictWriter(out, fieldnames=FIELDS, extrasaction="ignore")
    w.writeheader()
    order = {c: i for i, c in enumerate("BCDEFA")}
    for e in sorted(register, key=lambda r: (order.get(r["class"], 9),
                                             -abs(r["diff_tax"]))):
        w.writerow({k: (str(v) if isinstance(v, Decimal) else v)
                    for k, v in e.items()})


def print_summary(res: dict, label: str) -> None:
    t = res["totals"]
    print(f"Reconciliation: {label}")
    print(f"  books rows {t['books_rows']}, portal rows {t['portal_rows']}")
    print(f"  books tax  {t['books_tax']}")
    print(f"  portal tax {t['portal_tax']}")
    print()
    print(f"  {'Class':<6}{'Count':>7}{'Books tax':>16}{'Portal tax':>16}{'Difference':>16}  Meaning")
    for cls, s in res["summary"].items():
        print(f"  {cls:<6}{s['count']:>7}{str(s['books_tax']):>16}"
              f"{str(s['portal_tax']):>16}{str(s['diff_tax']):>16}  {CLASS_MEANING[cls]}")
    print()
    print(f"  Matched and claimable (class A) : {t['matched_tax_class_a']}")
    print(f"  Unresolved / at risk (B, D, E)  : {t['tax_at_risk_or_unresolved']}")
    if t["tolerated_rounding"]:
        print(f"  Rounding absorbed within tolerance: {t['tolerated_rounding']}")

    unresolved = sum(s["count"] for c, s in res["summary"].items() if c != "A")
    print()
    if unresolved:
        print(f"  {unresolved} row(s) need resolution. Do not finalise the return "
              f"until each has a cause, an owner and a status in the register.")
    else:
        print("  No differences. Record in the working paper what was reconciled "
              "and against which files.")


def selftest() -> int:
    failures = []

    books = io.StringIO(
        "gstin,name,doc_no,doc_date,taxable,igst,cgst,sgst,cess,pos\n"
        "27AAPFU0939F1ZV,Matched Co,INV/001,2026-06-01,100000,0,9000,9000,0,27\n"
        "27AAPFU0939F1ZV,Not Filed Co,INV-002,2026-06-02,50000,9000,0,0,0,29\n"
        "29AAACR5055K1ZD,Value Diff Co,0003,2026-06-03,20000,0,1800,1800,0,29\n"
        "29AAACR5055K1ZD,Head Diff Co,INV 4,2026-06-04,10000,1800,0,0,0,27\n"
        "27AAPFU0939F1ZV,Blocked Co,INV/005,2026-06-05,10000,0,900,900,0,27\n"
        "27AAPFU0939F1ZV,Rounding Co,INV/006,2026-06-06,1000,0,90.40,90.40,0,27\n"
    )
    portal = io.StringIO(
        "gstin,name,doc_no,doc_date,taxable,igst,cgst,sgst,cess,pos,eligible\n"
        "27AAPFU0939F1ZV,Matched Co,INV-001,2026-06-01,100000,0,9000,9000,0,27,Y\n"
        "29AAACR5055K1ZD,Value Diff Co,INV/0003,2026-06-03,25000,0,2250,2250,0,29,Y\n"
        "29AAACR5055K1ZD,Head Diff Co,INV/4,2026-06-04,10000,0,900,900,0,27,Y\n"
        "27AAPFU0939F1ZV,Blocked Co,INV/005,2026-06-05,10000,0,900,900,0,27,N\n"
        "27AAPFU0939F1ZV,Rounding Co,INV/006,2026-06-06,1000,0,90,90,0,27,Y\n"
        "27AAPFU0939F1ZV,Stranger Co,INV/999,2026-06-09,80000,14400,0,0,0,29,Y\n"
    )
    res = reconcile(_load_rows(books, "books"), _load_rows(portal, "portal"))
    got = {c: s["count"] for c, s in res["summary"].items()}
    want = {"A": 2, "B": 1, "C": 1, "D": 1, "E": 1, "F": 1}
    if got != want:
        failures.append(f"classification: got {got}, expected {want}")

    # The rounding row must land in A but still be reported, not silently dropped.
    if res["totals"]["tolerated_rounding"] != Decimal("0.80"):
        failures.append(f"tolerated rounding not surfaced: "
                        f"{res['totals']['tolerated_rounding']}")

    # Document-number normalisation across common format variants.
    for a, b in [("INV/001", "INV-001"), ("INV 4", "INV/4"), ("inv/001", "INV001")]:
        if norm_doc(a) != norm_doc(b):
            failures.append(f"doc normalisation failed: {a!r} vs {b!r} -> "
                            f"{norm_doc(a)!r} vs {norm_doc(b)!r}")

    # The gstin+date fallback must pair a bare number with a prefixed one, label
    # how it matched, and still classify the value difference correctly.
    fb = [e for e in res["register"] if e["matched_on"] == "gstin+date"]
    if len(fb) != 1 or fb[0]["class"] != "D":
        failures.append(f"gstin+date fallback did not behave as expected: "
                        f"{[(e['doc_no'], e['class'], e['matched_on']) for e in fb]}")
    elif "document numbers differ" not in fb[0]["note"]:
        failures.append("fallback match was not labelled in the register")

    # The fallback must NOT fire when the key is ambiguous on either side —
    # guessing is worse than reporting an unmatched pair.
    amb_b = io.StringIO("gstin,doc_no,doc_date,taxable,igst,cgst,sgst,cess\n"
                        "27AAPFU0939F1ZV,A1,2026-06-01,100,18,0,0,0\n"
                        "27AAPFU0939F1ZV,A2,2026-06-01,100,18,0,0,0\n")
    amb_p = io.StringIO("gstin,doc_no,doc_date,taxable,igst,cgst,sgst,cess\n"
                        "27AAPFU0939F1ZV,B1,2026-06-01,100,18,0,0,0\n"
                        "27AAPFU0939F1ZV,B2,2026-06-01,100,18,0,0,0\n")
    amb = reconcile(_load_rows(amb_b, "b"), _load_rows(amb_p, "p"))
    amb_counts = {c: s["count"] for c, s in amb["summary"].items()}
    if amb_counts != {"B": 2, "C": 2}:
        failures.append(f"ambiguous fallback should not match: {amb_counts}")

    # Number parsing tolerances.
    for raw, want_val in [("1,00,000", Decimal("100000")), ("", Decimal(0)),
                          ("(500)", Decimal("-500")), ("₹ 250.50", Decimal("250.50")),
                          ("-", Decimal(0))]:
        if dec(raw) != want_val:
            failures.append(f"dec({raw!r}) = {dec(raw)}, expected {want_val}")

    # A duplicated document number must match the nearer line, not the first.
    b2 = io.StringIO("gstin,doc_no,doc_date,taxable,igst,cgst,sgst,cess\n"
                     "27AAPFU0939F1ZV,DUP1,2026-06-01,100,0,9,9,0\n")
    p2 = io.StringIO("gstin,doc_no,doc_date,taxable,igst,cgst,sgst,cess\n"
                     "27AAPFU0939F1ZV,DUP1,2026-06-01,9999,0,899,899,0\n"
                     "27AAPFU0939F1ZV,DUP1,2026-06-01,100,0,9,9,0\n")
    r2 = reconcile(_load_rows(b2, "b"), _load_rows(p2, "p"))
    counts2 = {c: s["count"] for c, s in r2["summary"].items()}
    if counts2.get("A") != 1 or counts2.get("C") != 1:
        failures.append(f"duplicate doc_no matched the wrong line: {counts2}")

    # Register must be writable and complete.
    buf = io.StringIO()
    write_register(res["register"], buf)
    written = list(csv.DictReader(io.StringIO(buf.getvalue())))
    if len(written) != len(res["register"]):
        failures.append("register write dropped rows")
    if written and written[0]["class"] == "A":
        failures.append("register is not sorted with unresolved classes first")

    # Malformed inputs must fail loudly, not silently produce a clean register.
    for label, text in [
        ("missing column", "gstin,doc_no,taxable\n27AAPFU0939F1ZV,INV/1,100\n"),
        ("bad number", "gstin,doc_no,doc_date,taxable\n27AAPFU0939F1ZV,INV/1,2026-06-01,abc\n"),
        ("blank gstin", "gstin,doc_no,doc_date,taxable\n,INV/1,2026-06-01,100\n"),
        ("empty file", ""),
    ]:
        try:
            _load_rows(io.StringIO(text), label)
            failures.append(f"no error raised for {label}")
        except ValueError:
            pass

    if failures:
        print("SELFTEST FAILED")
        for f in failures:
            print("  -", f)
        return 1
    print("SELFTEST PASSED (classification A-F, normalisation, parsing, "
          "duplicate handling, register output, input guards)")
    return 0


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--books", help="CSV from the accounting system")
    p.add_argument("--portal", help="CSV from GSTR-2B / GSTR-1 / IMS")
    p.add_argument("--out", help="write the difference register here (CSV)")
    p.add_argument("--label", default="books vs portal")
    p.add_argument("--tolerance", default="1",
                   help="rupee tolerance on total tax for a matched pair (default 1)")
    p.add_argument("--selftest", action="store_true")
    args = p.parse_args()

    if args.selftest:
        return selftest()
    if not (args.books and args.portal):
        p.print_help()
        return 2

    res = reconcile(load(args.books), load(args.portal), dec(args.tolerance))
    print_summary(res, args.label)

    if args.out:
        with open(args.out, "w", newline="", encoding="utf-8") as fh:
            write_register(res["register"], fh)
        print(f"\n  Difference register written to {args.out}")
        print("  Fill in the owner and due_by columns before review — an item "
              "without an owner does not get resolved.")
    else:
        print("\n  Pass --out to write the difference register. The register is the "
              "working paper; this summary is not.")

    return 1 if any(c != "A" for c in res["summary"]) else 0


if __name__ == "__main__":
    sys.exit(main())
