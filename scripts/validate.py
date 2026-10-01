#!/usr/bin/env python3
"""Validate skills/ and agents/, and generate CATALOG.md.

  python scripts/validate.py                 validate everything (CI)
  python scripts/validate.py skills/seo      validate one subtree (fast self-check while authoring)
  python scripts/validate.py --catalog       also (re)write CATALOG.md
  python scripts/validate.py --check-catalog fail if CATALOG.md is stale

Rules mirror Obot's skill indexer (pkg/skillformat, skillrepository/scan.go) plus ours (docs/ARCHITECTURE.md).
Needs PyYAML (pip install pyyaml).
"""
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
DEPARTMENTS = {"accounting", "marketing", "seo", "satva", "general"}
LICENSES = {"Satva-original", "MIT", "Apache-2.0", "BSD-2-Clause", "BSD-3-Clause", "ISC", "CC0-1.0"}
REQUIRED = ("department", "domain", "owner", "status", "license", "source")
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
SECRETS = re.compile(r"sk-[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16}|-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY|xox[bp]-[0-9A-Za-z-]{10,}|ghp_[A-Za-z0-9]{30,}|AIza[0-9A-Za-z_-]{35}")
SKIP_DIRS = {".git", "node_modules", "__pycache__", ".pytest_cache"}
MAX_SKILL_MD = 1024 * 1024  # Obot limit


def frontmatter(path: Path):
    text = path.read_text(encoding="utf-8", errors="replace")
    m = re.match(r"^---\r?\n(.*?)\r?\n---", text, re.S)
    if not m:
        return None, "no frontmatter"
    try:
        fm = yaml.safe_load(m.group(1)) or {}
    except yaml.YAMLError as e:
        return None, f"yaml: {str(e).splitlines()[0]}"
    return (fm, None) if isinstance(fm, dict) else (None, "frontmatter is not a map")


def walk(base: Path):
    for p in sorted(base.rglob("*")):
        if p.is_file() and not (set(p.relative_to(ROOT).parts) & SKIP_DIRS):
            yield p


def check_skill(md: Path, errors: list, skills: dict):
    rel = md.relative_to(ROOT).as_posix()
    if md.stat().st_size > MAX_SKILL_MD:
        errors.append(f"{rel}: SKILL.md over 1 MB")
    fm, err = frontmatter(md)
    if err:
        return errors.append(f"{rel}: {err}")
    folder = md.parent.name
    name, desc = fm.get("name"), fm.get("description")
    if not isinstance(name, str) or not NAME_RE.match(name) or len(name) > 64:
        errors.append(f"{rel}: bad name {name!r}")
    elif name != folder:
        errors.append(f"{rel}: name {name!r} != folder {folder!r}")
    if not isinstance(desc, str) or not desc.strip() or len(desc) > 1024:
        errors.append(f"{rel}: description missing or > 1024 chars")
    for key in ("license", "compatibility", "allowed-tools"):  # Obot decodes these into Go strings; a list/map makes the skill invalid there
        if key in fm and not isinstance(fm[key], str):
            errors.append(f"{rel}: frontmatter {key!r} must be a string for Obot, got {type(fm[key]).__name__}")
    if fm.get("compatibility") and len(str(fm["compatibility"])) > 500:
        errors.append(f"{rel}: compatibility > 500 chars")
    meta = fm.get("metadata")
    if not isinstance(meta, dict):
        return errors.append(f"{rel}: metadata map required")
    if any(not isinstance(v, str) for v in meta.values()):
        errors.append(f"{rel}: every metadata value must be a string (quote it)")
    for k in REQUIRED:
        if not meta.get(k):
            errors.append(f"{rel}: metadata.{k} required")
    parts = md.relative_to(ROOT).parts  # skills, dept, ..., skill, SKILL.md
    dept = parts[1] if len(parts) > 2 else ""
    depth_ok = (len(parts) == 5) or (len(parts) == 6 and parts[1] == "accounting" and parts[2] == "platforms")
    if dept not in DEPARTMENTS or not depth_ok:
        errors.append(f"{rel}: path must be skills/<dept>/<group>/<skill>/SKILL.md (or accounting/platforms/<platform>/<skill>), dept in {sorted(DEPARTMENTS)}")
    if meta.get("department") != dept:
        errors.append(f"{rel}: metadata.department {meta.get('department')!r} != folder {dept!r}")
    if meta.get("status") not in ("stable", "beta"):
        errors.append(f"{rel}: metadata.status must be stable|beta")
    lic = meta.get("license")
    if lic not in LICENSES:
        errors.append(f"{rel}: license {lic!r} not allowed (allowed: {sorted(LICENSES)}); link-only sources go in docs/SOURCES.md")
    if lic != "Satva-original" and not str(meta.get("source", "")).startswith("http"):
        errors.append(f"{rel}: third-party skill needs metadata.source = upstream URL")
    if isinstance(name, str):
        if name in skills:
            errors.append(f"{rel}: duplicate skill name, also at {skills[name]['path']}")
        skills[name] = {"path": rel, "desc": (desc or "").strip(), "meta": meta}


def check_agent(md: Path, errors: list, agents: dict):
    rel = md.relative_to(ROOT).as_posix()
    fm, err = frontmatter(md)
    if err:
        return errors.append(f"{rel}: {err}")
    if not fm.get("name") or not fm.get("description"):
        errors.append(f"{rel}: name and description required")
    elif fm["name"] != md.stem:
        errors.append(f"{rel}: name {fm['name']!r} != file name {md.stem!r}")
    agents[md.stem] = {"path": rel, "desc": str(fm.get("description", "")).strip(), "skills": [s.strip() for s in str(fm.get("skills", "")).split(",") if s.strip()], "dept": md.parent.name}


def first_sentence(s: str, n=150) -> str:
    s = " ".join(s.split())
    cut = re.split(r"(?<=[.!?])\s", s, 1)[0]
    return (cut if len(cut) <= n else cut[: n - 1].rstrip() + "…").replace("|", "\\|")


def catalog(skills: dict, agents: dict) -> str:
    users = {}
    for a, d in agents.items():
        for s in d["skills"]:
            users.setdefault(s, set()).add(a)
    out = ["# Catalog", "", "> Generated by `scripts/validate.py --catalog`. Do not edit by hand.", "",
           f"**{len(skills)} skills · {len(agents)} agents.** Find the job below, then use the skill or hand it to the agent listed.", ""]
    for dept in sorted(DEPARTMENTS):
        rows = sorted((n, d) for n, d in skills.items() if d["meta"].get("department") == dept)
        if not rows:
            continue
        out += [f"## {dept} ({len(rows)})", "", "| Skill | What it does | Platform / domain | Status | Agents |", "|---|---|---|---|---|"]
        for n, d in rows:
            m = d["meta"]
            ag = sorted(users.get(n, set()) | {a.strip() for a in m.get("agents", "").split(",") if a.strip()})
            out.append(f"| [`{n}`]({d['path'].rsplit('/', 1)[0]}/) | {first_sentence(d['desc'])} | {m.get('platform') or m.get('domain')} | {m.get('status')} | {', '.join(f'`{a}`' for a in ag) or '-'} |")
        out.append("")
    if agents:
        out += [f"## Agents ({len(agents)})", "", "| Agent | Use it when | Department | Skills it uses |", "|---|---|---|---|"]
        for a, d in sorted(agents.items()):
            out.append(f"| [`{a}`]({d['path']}) | {first_sentence(d['desc'])} | {d['dept']} | {', '.join(f'`{s}`' for s in d['skills']) or '-'} |")
        out.append("")
    return "\n".join(out)


def main(argv):
    flags = {a for a in argv if a.startswith("--")}
    target = next((ROOT / a for a in argv if not a.startswith("--")), None)
    errors, skills, agents = [], {}, {}
    for md in walk(ROOT / "skills"):
        if md.name == "SKILL.md" and (target is None or target in md.parents):
            check_skill(md, errors, skills)
    for md in walk(ROOT / "agents") if (ROOT / "agents").exists() else []:
        if md.suffix == ".md" and md.name != "README.md" and (target is None or target in md.parents):
            check_agent(md, errors, agents)
    for md in walk(ROOT):  # Obot indexes the whole repo: no SKILL.md outside skills/
        if md.name == "SKILL.md" and "skills" not in md.relative_to(ROOT).parts[:1]:
            errors.append(f"{md.relative_to(ROOT).as_posix()}: SKILL.md outside skills/ (Obot would index it)")
    for md in walk(ROOT / "skills"):
        if target is not None and target not in md.parents:
            continue
        try:
            if md.stat().st_size < 2_000_000 and SECRETS.search(md.read_text(encoding="utf-8", errors="ignore")):
                errors.append(f"{md.relative_to(ROOT).as_posix()}: looks like a secret")
        except OSError:
            pass
    if target is None:  # cross-refs need the full set
        for a, d in agents.items():
            errors += [f"{d['path']}: references unknown skill {s!r}" for s in d["skills"] if s not in skills]
    text = catalog(skills, agents)
    cat = ROOT / "CATALOG.md"
    if "--catalog" in flags and target is None:
        cat.write_text(text + "\n", encoding="utf-8", newline="\n")
    if "--check-catalog" in flags and (not cat.exists() or cat.read_text(encoding="utf-8").strip() != text.strip()):
        errors.append("CATALOG.md is stale: run python scripts/validate.py --catalog")
    for e in errors:
        print("FAIL", e)
    print(f"{'FAILED' if errors else 'OK'}: {len(skills)} skills, {len(agents)} agents, {len(errors)} problems")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
