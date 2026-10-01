"""
The accountant's persistent Excel workbook: his control panel AND the skill's memory.
Run -> update_workbook -> he picks Approve/Reject/Change in Excel -> next run reads it (load_decisions / rules.py).
Stdlib + openpyxl only. Never overwrites a cell the accountant typed in; never crashes on a locked file.
"""
from __future__ import annotations
import hashlib, os, shutil
from datetime import datetime
from openpyxl import Workbook, load_workbook
from openpyxl.styles import Font, PatternFill
from openpyxl.worksheet.datavalidation import DataValidation

START, DEC, APP, MATCHED, ONLY_Q, ONLY_L, WRONG, HIST, LOG, GLOSS = (
    "Start Here", "Needs Your Decision", "Approved Mappings", "Matched Products", "Only in QBO",
    "Only in Linnworks", "What's Wrong", "History", "Change Log", "Glossary")
DECISIONS = ["Approve", "Reject", "Change to..."]
DEC_HEADERS = ["Row ID", "Key", "Status", "Kind", "What we found", "Our suggestion", "Evidence", "Value",
               "Your Decision", "Change to", "Your Notes", "Source ID", "Source Name", "Target ID", "Applied"]
APP_HEADERS = ["Row ID", "Source ID", "Source Name", "QBO Target ID", "QBO Target Name", "Decision",
               "Approved On", "Last Used", "Status"]
WRONG_HEADERS = ["Row ID", "Severity", "What is wrong", "Money at stake"]
HIST_HEADERS = ["Date", "Period", "Health %", "Need decision", "Urgent", "Matched", "Only in QBO", "Only in Linnworks"]
LOG_HEADERS = ["When", "Who", "What happened", "Row Key"]
GLOSS_HEADERS = ["Term", "Meaning"]
URGENT = {"urgent", "high", "critical"}
KEEP_BACKUPS = 10
CHECK = "Check 'Change to'"  # he picked Change but the typed item was not found (or matched several)
DEFAULT_GLOSSARY = [
    ("Approve", "The suggestion is right. The skill will remember it and reuse it next time."),
    ("Reject", "The suggestion is wrong. The skill will not suggest it again."),
    ("Change to...", "Right idea, wrong target. Pick this and type the correct QuickBooks item name or number in 'Change to'."),
    ("Resolved", "The problem no longer shows up in the latest run. Nothing to do."),
    ("Health %", "Share of Linnworks items that are cleanly matched to QuickBooks."),
]
_HEAD_FILL = PatternFill("solid", fgColor="1194D2")


class WorkbookDamaged(Exception):
    """Raised (plain English) when the accountant's workbook headers were renamed/deleted."""


def row_id(key) -> str:
    return hashlib.sha1(str(key).encode("utf-8")).hexdigest()[:10]


def _now():
    return datetime.now().strftime("%Y-%m-%d %H:%M")


def _text(v):
    return "; ".join(map(str, v)) if isinstance(v, (list, tuple)) else v


def _style(ws, headers, widths=None, hide=("A",)):
    for i, h in enumerate(headers, 1):
        c = ws.cell(1, i, h)
        c.font, c.fill = Font(bold=True, color="FFFFFF"), _HEAD_FILL
        ws.column_dimensions[c.column_letter].width = (widths or {}).get(h, max(14, len(h) + 4))
    ws.freeze_panes = "A2"
    for col in hide:
        ws.column_dimensions[col].hidden = True


def _layout():
    """sheet name -> (headers, widths, hidden columns)."""
    return {
        START: ([], {}, ()),
        DEC: (DEC_HEADERS, {"What we found": 50, "Our suggestion": 34, "Evidence": 50, "Your Decision": 16,
                            "Change to": 30, "Your Notes": 40}, ("A", "B", "L", "M", "N")),
        APP: (APP_HEADERS, {"Source Name": 30, "QBO Target Name": 30}, ("A",)),
        MATCHED: ([], {}, ("A",)), ONLY_Q: ([], {}, ("A",)), ONLY_L: ([], {}, ("A",)),
        WRONG: (WRONG_HEADERS, {"What is wrong": 70}, ("A",)),
        HIST: (HIST_HEADERS, {}, ()), LOG: (LOG_HEADERS, {"What happened": 80}, ("D",)),
        GLOSS: (GLOSS_HEADERS, {"Term": 20, "Meaning": 90}, ()),
    }


def create_workbook(path, client_name):
    wb = Workbook()
    wb.remove(wb.active)
    for name, (headers, widths, hide) in _layout().items():
        ws = wb.create_sheet(name)
        if headers:
            _style(ws, headers, widths, hide)
    wb[START]["A1"] = f"{client_name} - Linnworks to QuickBooks mapping"
    wb[START]["A1"].font = Font(bold=True, size=16)
    _add_dropdown(wb[DEC])
    wb.save(path)
    return path


def _add_dropdown(ws):
    dv = DataValidation(type="list", formula1='"' + ",".join(DECISIONS) + '"', allow_blank=True,
                        showErrorMessage=True, errorTitle="Pick from the list",
                        error="Please choose Approve, Reject or Change to...")
    ws.add_data_validation(dv)
    dv.add("I2:I50000")


def _sheet(wb, name, headers):
    """Return the sheet after checking its header row; raise WorkbookDamaged (plain English) if changed."""
    if name not in wb.sheetnames:
        raise WorkbookDamaged(f"The sheet '{name}' is missing. Restore the latest copy from the 'backups' "
                              "folder next to this file, then run again.")
    ws = wb[name]
    if [c.value for c in ws[1]][:len(headers)] != headers:
        raise WorkbookDamaged(
            f"The sheet '{name}' has changed: its column titles in row 1 were renamed, moved or deleted "
            f"(expected: {', '.join(headers)}). Nothing was changed. To fix: press Ctrl+Z in Excel, or restore "
            "the latest copy from the 'backups' folder next to this file, then run again. "
            "Please don't rename or delete the header row or the hidden columns.")
    return ws


def _rows(ws, headers):
    """[(excel_row_number, {header: value})] for non-empty data rows."""
    out = []
    for r in range(2, ws.max_row + 1):
        vals = [ws.cell(r, i + 1).value for i in range(len(headers))]
        if any(v not in (None, "") for v in vals):
            out.append((r, dict(zip(headers, vals))))
    return out


def _set(ws, r, headers, **cols):
    for h, v in cols.items():
        ws.cell(r, headers.index(h.replace("_", " ")) + 1, _text(v))


def backup(path):
    """Timestamped copy into backups/ next to the file; keep the last KEEP_BACKUPS."""
    if not os.path.exists(path):
        return None
    d = os.path.join(os.path.dirname(os.path.abspath(path)), "backups")
    os.makedirs(d, exist_ok=True)
    stem = os.path.splitext(os.path.basename(path))[0]
    dest = os.path.join(d, f"{stem}_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}.xlsx")
    shutil.copy2(path, dest)
    for f in sorted(f for f in os.listdir(d) if f.startswith(stem + "_"))[:-KEEP_BACKUPS]:
        os.remove(os.path.join(d, f))
    return dest


def _save(wb, path):
    """Save; if Excel has the file open, write <name>_pending.xlsx instead. Returns path written."""
    try:
        wb.save(path)
        return path
    except PermissionError:
        base, ext = os.path.splitext(path)
        pending = f"{base}_pending{ext}"
        wb.save(pending)
        return pending


def _log(wb, who, what, key=""):
    _sheet(wb, LOG, LOG_HEADERS).append([_now(), who, what, key])


def norm_decision(v):
    s = str(v or "").strip().lower()
    return ("Approve" if s.startswith("approve") else "Reject" if s.startswith("reject")
            else "Change" if s.startswith("change") else None)


def _apply_decisions(wb, resolve=None):
    """Turn the accountant's picks into Approved Mappings rows + Change Log. A pick that changed since it was
    applied is re-applied (he can change his mind); one source keeps only one active rule.
    resolve(text) -> (target_id, target_name) or None finds what he typed under 'Change to'."""
    dec, app = _sheet(wb, DEC, DEC_HEADERS), _sheet(wb, APP, APP_HEADERS)
    for r, v in _rows(dec, DEC_HEADERS):
        d = norm_decision(v["Your Decision"])
        change = str(v["Change to"] or "").strip()
        sig = f"{d}|{change}"
        if not d or not (v["Status"] in ("Open", CHECK) or (v["Status"] == "Decided" and v["Applied"] != sig)):
            continue
        if d == "Change":
            if not change:
                continue  # picked Change but hasn't said to what yet: leave open
            hit = resolve(change) if resolve else (change, change)
            if not hit:
                if v["Status"] != CHECK:
                    _log(wb, "System", f"Couldn't find '{change}' in QuickBooks (type the exact item name or number)", v["Key"])
                _set(dec, r, DEC_HEADERS, Status=CHECK)
                continue
            tid, tname = hit
        else:
            tid, tname = v["Target ID"], v["Our suggestion"]
        sid = v["Source ID"]
        if sid and tid:
            existing = {a["Row ID"]: i for i, a in _rows(app, APP_HEADERS)}
            for i, a in _rows(app, APP_HEADERS):  # one active rule per source
                if str(a["Source ID"]) == str(sid) and a["Status"] == "Active" and str(a["QBO Target ID"]) != str(tid):
                    app.cell(i, APP_HEADERS.index("Status") + 1, "Revoked")
            rid = row_id(f"{sid}|{tid}")
            row = [rid, sid, v["Source Name"], tid, tname, "Rejected" if d == "Reject" else "Approved",
                   _now(), None, "Active"]
            if rid in existing:
                for i, val in enumerate(row):
                    if i != 7:  # keep Last Used
                        app.cell(existing[rid], i + 1, val)
            else:
                app.append(row)
        _set(dec, r, DEC_HEADERS, Status="Decided", Applied=sig)
        _log(wb, "Accountant", f"{d}: {v['What we found']} -> {tname or ''}", v["Key"])


def _upsert_decisions(wb, decisions):
    ws = _sheet(wb, DEC, DEC_HEADERS)
    active = {str(a["Source ID"]) for _, a in _rows(wb[APP], APP_HEADERS) if a["Status"] == "Active"}
    have = {v["Key"]: r for r, v in _rows(ws, DEC_HEADERS)}
    seen = set()
    for d in decisions:
        k = str(d["key"])
        seen.add(k)
        sysvals = dict(Kind=d.get("kind"), What_we_found=d.get("what_we_found"), Our_suggestion=d.get("suggestion"),
                       Evidence=d.get("evidence"), Value=d.get("value"), Source_ID=d.get("source_id"),
                       Source_Name=d.get("source_name"), Target_ID=d.get("target_id"))
        if k in have:
            r = have[k]
            status = ws.cell(r, 3).value
            if status == "Decided":
                same = str(ws.cell(r, DEC_HEADERS.index("Target ID") + 1).value or "") == str(d.get("target_id") or "")
                if same and str(d.get("source_id")) in active:
                    continue  # he decided; leave his row exactly as it is
                _set(ws, r, DEC_HEADERS, Your_Decision="", Change_to="", Applied="", Status="Open")
            _set(ws, r, DEC_HEADERS, **sysvals)
            if status == "Resolved":
                _set(ws, r, DEC_HEADERS, Status="Open")
        else:
            ws.append([row_id(k), k, "Open"] + [None] * (len(DEC_HEADERS) - 3))
            _set(ws, ws.max_row, DEC_HEADERS, **sysvals)
    for k, r in have.items():  # vanished -> Resolved (never deleted); decided rows keep their state
        if k not in seen and ws.cell(r, 3).value in ("Open", CHECK):
            _set(ws, r, DEC_HEADERS, Status="Resolved")
    return ws


def _rewrite(wb, name, rows):
    """Read-only info sheets (accountant never types here): rebuilt from the run each time."""
    ws = wb[name]
    ws.delete_rows(1, ws.max_row)
    cols = list(dict.fromkeys(k for r in rows for k in r if k != "key"))
    _style(ws, ["Row ID"] + cols, {c: 24 for c in cols})
    for r in rows:
        ws.append([row_id(r.get("key", sorted(map(str, r.items()))))] + [_text(r.get(c)) for c in cols])


def _start_here(wb, run, n_open, n_urgent):
    ws = wb[START]
    ws.delete_rows(1, ws.max_row)
    ws["A1"] = f"{run.get('client', '')} - Linnworks to QuickBooks mapping"
    ws["A1"].font = Font(bold=True, size=16)
    ws["A3"] = (f"{n_open} things need your decision, {n_urgent} problems are urgent."
                if n_open or n_urgent else "Nothing needs your decision right now.")
    ws["A3"].font = Font(bold=True, size=13)
    ws["A4"] = (f"Health score: {run.get('health_pct', 0):.0f}%   |   Period: {run.get('period', '')}"
                f"   |   Last run: {run.get('run_at', _now())}")
    ws["A6"] = "How to use this file"
    ws["A6"].font = Font(bold=True)
    ws["A7"] = "1. Open 'Needs Your Decision'.  2. In 'Your Decision' pick Approve, Reject or Change to...  3. Save and close Excel. The next run learns from your choices."
    ws["A8"] = "Only type in 'Your Decision', 'Change to' and 'Your Notes'. Everything else is refreshed by the skill."
    ws["A10"] = "Latest numbers"
    ws["A10"].font = Font(bold=True)
    for i, (m, v) in enumerate(run.get("summary", []), 11):
        ws.cell(i, 1, m)
        ws.cell(i, 2, v)
    ws.column_dimensions["A"].width = 45
    ws.column_dimensions["B"].width = 25


def update_workbook(path, run, do_backup=True):
    """Merge a run into the workbook. Returns the path actually written (main file, or <name>_pending.xlsx if locked)."""
    path = str(path)
    if not os.path.exists(path):
        create_workbook(path, run.get("client", ""))
    if do_backup:
        backup(path)
    wb = load_workbook(path)
    for name, headers in ((DEC, DEC_HEADERS), (APP, APP_HEADERS), (WRONG, WRONG_HEADERS), (HIST, HIST_HEADERS),
                          (LOG, LOG_HEADERS), (GLOSS, GLOSS_HEADERS)):
        _sheet(wb, name, headers)  # validate everything before touching anything
    _apply_decisions(wb, run.get("resolve"))
    dec = _upsert_decisions(wb, run.get("decisions", []))
    if not dec.data_validations.dataValidation:
        _add_dropdown(dec)
    app, used = wb[APP], set(map(str, run.get("used_sources", [])))
    for r, v in _rows(app, APP_HEADERS):
        if str(v["Source ID"]) in used and v["Status"] == "Active":
            app.cell(r, 8, _now())
    for name, key in ((MATCHED, "matched"), (ONLY_Q, "only_in_qbo"), (ONLY_L, "only_in_lw")):
        _rewrite(wb, name, run.get(key, []))
    wrongs = run.get("wrongs", [])
    ws = wb[WRONG]
    ws.delete_rows(2, ws.max_row)
    for w in wrongs:
        ws.append([row_id(w["key"]), w.get("severity"), w.get("plain_text"), w.get("money_at_stake")])
    n_open = sum(1 for _, v in _rows(dec, DEC_HEADERS) if v["Status"] in ("Open", CHECK))
    n_urgent = sum(1 for w in wrongs if str(w.get("severity", "")).lower() in URGENT)
    wb[HIST].append([run.get("run_at", _now()), run.get("period"), run.get("health_pct"), n_open, n_urgent,
                     len(run.get("matched", [])), len(run.get("only_in_qbo", [])), len(run.get("only_in_lw", []))])
    _log(wb, "System", f"Run for {run.get('period', '')}: {n_open} open decisions, health {run.get('health_pct', 0):.0f}%")
    g = wb[GLOSS]
    g.delete_rows(2, g.max_row)
    for row in DEFAULT_GLOSSARY + list(run.get("glossary", [])):
        g.append(list(row))
    _start_here(wb, run, n_open, n_urgent)
    return _save(wb, path)


def apply_decisions(path, resolve=None):
    """Fold the accountant's picks into Approved Mappings now (so a run can use them). Returns path written."""
    path = str(path)
    backup(path)
    wb = load_workbook(path)
    _apply_decisions(wb, resolve)
    return _save(wb, path)


def open_count(path):
    """How many decisions are still waiting for the accountant."""
    ws = _sheet(load_workbook(path, data_only=True), DEC, DEC_HEADERS)
    return sum(1 for _, v in _rows(ws, DEC_HEADERS) if v["Status"] in ("Open", CHECK))


def load_decisions(path):
    """Accountant's picks: [{'key','decision' (Approve|Reject|Change),'change_to','notes'}]. Raises WorkbookDamaged."""
    ws = _sheet(load_workbook(path, data_only=True), DEC, DEC_HEADERS)
    return [{"key": v["Key"], "decision": norm_decision(v["Your Decision"]),
             "change_to": str(v["Change to"] or "").strip(), "notes": v["Your Notes"] or ""}
            for _, v in _rows(ws, DEC_HEADERS) if norm_decision(v["Your Decision"])]
