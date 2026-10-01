#!/usr/bin/env python3
"""Validate an Indian GSTIN: format, checksum, state code and embedded PAN.

A GSTIN is 15 characters:

    27  AAPFU0939F  1  Z  V
    |   |           |  |  |
    |   |           |  |  +-- check character (mod-36 checksum)
    |   |           |  +----- 'Z' by default
    |   |           +-------- entity code (registrations under the same PAN in
    |   |                     the same state)
    |   +-------------------- PAN of the taxpayer
    +------------------------ state / UT code

Catching a bad GSTIN at intake is far cheaper than discovering it after a return
is filed against the wrong registration, or after a customer's credit fails
because the GSTIN on the invoice was mistyped.

This validates structure only. It cannot tell you whether the registration is
active, suspended or cancelled — check that on the GST portal's "Search
Taxpayer" page.

Usage:
    python3 gstin_check.py 27AAPFU0939F1ZV
    python3 gstin_check.py --file gstins.txt
    python3 gstin_check.py --selftest
"""

from __future__ import annotations

import argparse
import re
import sys

ALPHABET = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"

GSTIN_RE = re.compile(r"^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}[Z1-9A-J]{1}[0-9A-Z]{1}$")

STATE_CODES = {
    "01": "Jammu and Kashmir", "02": "Himachal Pradesh", "03": "Punjab",
    "04": "Chandigarh", "05": "Uttarakhand", "06": "Haryana", "07": "Delhi",
    "08": "Rajasthan", "09": "Uttar Pradesh", "10": "Bihar", "11": "Sikkim",
    "12": "Arunachal Pradesh", "13": "Nagaland", "14": "Manipur",
    "15": "Mizoram", "16": "Tripura", "17": "Meghalaya", "18": "Assam",
    "19": "West Bengal", "20": "Jharkhand", "21": "Odisha",
    "22": "Chhattisgarh", "23": "Madhya Pradesh", "24": "Gujarat",
    "25": "Daman and Diu (pre-merger)",
    "26": "Dadra and Nagar Haveli and Daman and Diu",
    "27": "Maharashtra", "28": "Andhra Pradesh (pre-bifurcation)",
    "29": "Karnataka", "30": "Goa", "31": "Lakshadweep", "32": "Kerala",
    "33": "Tamil Nadu", "34": "Puducherry",
    "35": "Andaman and Nicobar Islands", "36": "Telangana",
    "37": "Andhra Pradesh", "38": "Ladakh",
    "97": "Other Territory", "99": "Centre Jurisdiction",
}

# Fourth character of a PAN encodes the holder's status.
PAN_ENTITY = {
    "P": "Individual / proprietor", "C": "Company", "H": "Hindu Undivided Family",
    "F": "Firm / LLP", "A": "Association of Persons", "T": "Trust",
    "B": "Body of Individuals", "L": "Local Authority",
    "J": "Artificial Juridical Person", "G": "Government",
}


def check_character(first14: str) -> str:
    """Return the expected 15th character for the first 14 of a GSTIN.

    Positions are weighted 1, 2, 1, 2, ... Each product is split into its
    quotient and remainder on 36 and both are added to the running total; the
    check character makes the total a multiple of 36.
    """
    total = 0
    for i, ch in enumerate(first14):
        value = ALPHABET.index(ch)
        product = value * (1 if i % 2 == 0 else 2)
        total += product // 36 + product % 36
    return ALPHABET[(36 - (total % 36)) % 36]


def validate(gstin: str) -> dict:
    """Validate a GSTIN and describe what it decodes to."""
    raw = gstin
    gstin = (gstin or "").strip().upper().replace(" ", "")
    result = {
        "input": raw, "gstin": gstin, "valid": False, "errors": [],
        "state_code": None, "state": None, "pan": None,
        "entity_type": None, "entity_number": None,
        "expected_check_char": None,
    }

    if len(gstin) != 15:
        result["errors"].append(f"length is {len(gstin)}, expected 15")
        return result

    if any(c not in ALPHABET for c in gstin):
        result["errors"].append("contains characters outside 0-9 and A-Z")
        return result

    if not GSTIN_RE.match(gstin):
        result["errors"].append("does not match the GSTIN structural pattern")

    state = gstin[:2]
    result["state_code"] = state
    result["state"] = STATE_CODES.get(state)
    if result["state"] is None:
        result["errors"].append(f"state code '{state}' is not a recognised state/UT code")

    pan = gstin[2:12]
    result["pan"] = pan
    if not re.match(r"^[A-Z]{5}[0-9]{4}[A-Z]$", pan):
        result["errors"].append(f"embedded PAN '{pan}' is not a valid PAN pattern")
    else:
        result["entity_type"] = PAN_ENTITY.get(pan[3], f"unknown status code '{pan[3]}'")

    result["entity_number"] = gstin[12]

    if gstin[13] != "Z":
        # Non-'Z' occurs for some categories (UIN holders, OIDAR, TDS/TCS).
        result["errors"].append(
            f"14th character is '{gstin[13]}', not 'Z' — valid only for special "
            "registration categories; confirm this is intended"
        )

    expected = check_character(gstin[:14])
    result["expected_check_char"] = expected
    if gstin[14] != expected:
        result["errors"].append(
            f"checksum mismatch: 15th character is '{gstin[14]}', expected '{expected}'"
        )

    result["valid"] = not result["errors"]
    return result


def report(res: dict) -> str:
    lines = [f"GSTIN: {res['gstin']}"]
    if res["state"]:
        lines.append(f"  State        : {res['state_code']} — {res['state']}")
    if res["pan"]:
        lines.append(f"  PAN          : {res['pan']}")
    if res["entity_type"]:
        lines.append(f"  Entity type  : {res['entity_type']}")
    if res["entity_number"]:
        lines.append(f"  Entity code  : {res['entity_number']}")
    if res["valid"]:
        lines.append("  Result       : VALID (structure and checksum)")
        lines.append("  Note         : confirm the registration is ACTIVE on the GST portal — "
                     "this check cannot see registration status.")
    else:
        lines.append("  Result       : INVALID")
        for e in res["errors"]:
            lines.append(f"    - {e}")
    return "\n".join(lines)


def selftest() -> int:
    """Check the checksum implementation against known-good and mutated inputs."""
    failures = []

    # Generate a set of structurally valid GSTINs by computing their own check
    # character, then confirm the validator accepts them.
    bases = [
        "27AAPFU0939F1Z", "29AAACR5055K1Z", "07AABCU9603R1Z",
        "33AAACT2727Q1Z", "19AAACW1234F1Z", "24AAACC1206D1Z",
    ]
    for base in bases:
        gstin = base + check_character(base)
        res = validate(gstin)
        if not res["valid"]:
            failures.append(f"expected {gstin} to be valid, got: {res['errors']}")

    # Every single-character mutation of the check digit must be rejected.
    good = "27AAPFU0939F1Z" + check_character("27AAPFU0939F1Z")
    for ch in ALPHABET:
        if ch == good[14]:
            continue
        if validate(good[:14] + ch)["valid"]:
            failures.append(f"checksum accepted a wrong check character '{ch}'")

    # Structural rejections.
    bad_cases = {
        "27AAPFU0939F1Z": "14 characters",
        "": "empty",
        "27AAPFU0939F1ZVX": "16 characters",
        "00AAPFU0939F1ZV": "invalid state code 00",
        "27AAPF00939F1ZV": "malformed PAN",
        "27AAPFU0939F1ZV ".strip()[:14] + "!": "illegal character",
    }
    for gstin, why in bad_cases.items():
        if validate(gstin)["valid"]:
            failures.append(f"accepted an invalid GSTIN ({why}): {gstin!r}")

    # Whitespace and lower case should be tolerated, not rejected.
    if not validate(f"  {good.lower()}  ")["valid"]:
        failures.append("failed to normalise whitespace and case")

    if failures:
        print("SELFTEST FAILED")
        for f in failures:
            print("  -", f)
        return 1
    print(f"SELFTEST PASSED ({len(bases)} valid GSTINs, "
          f"{len(ALPHABET) - 1} checksum mutations, {len(bad_cases)} malformed inputs)")
    return 0


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("gstin", nargs="*", help="one or more GSTINs to validate")
    p.add_argument("--file", help="file containing one GSTIN per line")
    p.add_argument("--selftest", action="store_true", help="run built-in tests and exit")
    args = p.parse_args()

    if args.selftest:
        return selftest()

    targets = list(args.gstin)
    if args.file:
        with open(args.file, encoding="utf-8") as fh:
            targets += [ln.strip() for ln in fh if ln.strip()]

    if not targets:
        p.print_help()
        return 2

    invalid = 0
    for g in targets:
        res = validate(g)
        print(report(res))
        print()
        invalid += 0 if res["valid"] else 1

    if invalid:
        print(f"{invalid} of {len(targets)} GSTIN(s) failed validation.")
    return 1 if invalid else 0


if __name__ == "__main__":
    sys.exit(main())
