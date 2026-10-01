# Satva COE Skills & Agents: architecture

> **One repo is the single source of truth for every skill and agent Satva gives its people.**
> Obot points at it once. Developers browse it by department. CI keeps it valid.

## 1. Problem this solves

- Skills were scattered across product repos, personal folders and a flat `skills/` list of five.
- Obot indexes **every** `SKILL.md` it finds and lists invalid ones org-wide. It has no ignore file, so the tree itself must be clean.
- A developer could not answer "which skill do I use for X, and which agent runs it?".
- Copying third-party skills into a **public** repo is redistribution. Licences were never recorded.

## 2. Principles

1. **Single source of truth.** Every skill lives here, once. Product repos consume it; they do not fork it.
2. **One Obot link.** The only `SKILL.md` files in the repo are under `skills/`, so the source URL works whether Obot reads the repo root or `/tree/main/skills`.
3. **Organised by who needs it.** `department / domain / skill`. A developer finds the skill by the job, not by where it was harvested from.
4. **Grounded in our systems.** Platform skills name the real tools of the Satva MCP servers (Xero, QuickBooks, Linnworks, Shopify, Zoho Books). A skill that names another product's tools is not published.
5. **Licence-clean.** Only permissively licensed third-party content is copied, with attribution. Everything else is a link in `docs/SOURCES.md`, never a copy.
6. **Machine-enforced.** `scripts/validate.py` runs in CI and fails the PR on anything Obot would show as invalid, plus our own rules.
7. **Nothing is lost.** Existing skills keep their `name`. Client work (the Linnworks-QuickBooks mapping for Coins of America) moves byte-for-byte; only frontmatter gains metadata.

## 3. Repository layout

```
skills/                                 <- the ONLY place a SKILL.md may exist
  accounting/
    <stage>/<skill>/                    platform-neutral practice by lifecycle stage: setup, capture, journals, reconciliation,
                                        payables-receivables, close, reporting, planning, tax, payroll, audit-controls,
                                        consolidation, revenue-inventory-assets
    platforms/<platform>/<skill>/       quickbooks, xero, linnworks, shopify, zoho-books, ... one folder per system we run in SaaS
  marketing/<domain>/<skill>/           content, social, email, ads, cro, brand, video, strategy
  seo/<domain>/<skill>/                 technical, content, local, ai-search, analytics
  satva/<domain>/<skill>/               house skills: Satva-branded documents, guides, product videos
  general/<domain>/<skill>/             cross-department (reserved until needed)
agents/<department>/<agent>.md          Claude Code subagents; each lists the skills it uses
CATALOG.md                              GENERATED: department -> skill -> agent. Do not hand-edit.
docs/ARCHITECTURE.md                    this file
docs/SOURCES.md                         every third-party source: URL, licence, copied or link-only
scripts/validate.py                     validator + catalog generator (CI)
install.sh / install.ps1                installers (nested-aware, `--dept` filter)
examples/ docs/img/                     samples; never contain a SKILL.md
```

Depth is fixed: `skills/<department>/<group>/<skill>/SKILL.md` (for accounting the group is a lifecycle stage), or for platforms
`skills/accounting/platforms/<platform>/<skill>/SKILL.md`.

## 4. The skill contract

```yaml
---
name: xero-bank-reconciliation        # == folder name; a-z 0-9 single hyphens; <= 64; UNIQUE across the repo
description: >-                       # <= 1024 chars. Say what it does AND when to trigger it.
  ...
metadata:                             # Obot reads this map; every value MUST be a string
  department: "accounting"            # == the folder under skills/
  domain: "reconciliation"            # free tag inside the department
  platform: "xero"                    # only for platform skills (comma-separate for integrations)
  owner: "satva-coe"
  status: "stable"                    # stable | beta
  license: "Satva-original"           # or MIT | Apache-2.0 | BSD-2-Clause | BSD-3-Clause | ISC | CC0-1.0
  source: "original"                  # or the upstream URL (required when licence is not Satva-original)
  agents: "accounting-bookkeeper"     # optional: agents that use it
---
```

Rules the validator enforces: Obot's own rules (name, description, size <= 1 MB, string-only metadata, not at repo root),
unique names, folder path matches `metadata.department`, allowed licence list, `source` for third-party content,
no secrets in any skill file, no `SKILL.md` outside `skills/`, and every agent's `skills:` entry must exist.

Trust tiers: `Satva-original` (we wrote and own it), permissive third-party (adapted, attributed), link-only (not in the repo).

## 5. Departments

| Department | Covers | Typical consumer |
|---|---|---|
| `accounting/<stage>` | How an accountant works, independent of software, one folder per lifecycle stage | Accountants, the Satva Ledger agent |
| `accounting/platforms/*` | Doing the job inside one system, using its real tool names | Accountants, integration developers |
| `marketing` | Content, social, email, ads, conversion, brand, launch video | Marketing, sales |
| `seo` | Technical SEO, content, local, AI-search visibility | Marketing, web developers |
| `satva` | Satva house formats and product assets | Everyone at Satva |
| `general` | Cross-department helpers | Everyone |

## 6. Agents layer

`agents/<department>/<agent>.md` are Claude Code subagent definitions (`name`, `description`, `tools`) with an extra
`skills:` line naming the skills the agent leans on. The catalog inverts that mapping, so a developer can answer both
"what skill for this job?" and "which agent already uses it?".

## 7. Third-party provenance and licences

- A source is **copied** only if its licence is MIT, Apache-2.0, BSD-2/3-Clause, ISC or CC0-1.0, and the skill is adapted, attributed in `NOTICE.md`, and tagged in its own `metadata`.
- No licence file, a non-commercial licence, or a copyleft licence: **link only**, recorded in `docs/SOURCES.md`.
- This repo is public. Licence review is part of every PR that adds third-party content.

## 8. Obot integration

- Add **one** source URL for this repo. Skills appear as `skills/<department>/...`.
- Obot derives a skill's identity from its repo path. **Moving a skill changes its Obot ID.** After the first merge, re-check *Skill Access Policies* for the five pre-existing skills (`satva-doc`, `satva-guide-gif`, `feature-launch-video`, `satva-ledger-marketing-video`, `lw-qbo-mapping`).
- Obot rejects a skill whose folder name differs from `name`. CI makes that impossible to merge.
- Held-back or draft skills must **not** be named `SKILL.md`. Park them as `SKILL.draft.md` (Obot ignores it).

## 9. Delivery pipeline

`branch -> PR -> CI (validate.py + skill tests) -> review -> merge to main -> Obot syncs -> people install`

`CATALOG.md` is regenerated by CI and must be committed; a stale catalog fails the check.

## 10. Roadmap

- **v1 (this change):** layout, validator, catalog, installers, accounting/marketing/seo/satva skills, agent set.
- **v2:** product repos (`accounting-agent-skills`) consume this repo instead of keeping a copy; per-skill evals; semver tags and a deprecation policy.
- **v3:** skill usage telemetry from Obot to retire dead skills and invest in busy ones.

## 11. Risks

| Risk | Mitigation |
|---|---|
| Obot IDs change when skills move | Access-policy re-check checklist (section 8); five names unchanged |
| Licence breach in a public repo | Allowed-licence gate in CI; link-only fallback |
| Client data leaking into a public repo | Secret/PII review on every PR; `lw-qbo-mapping` ships rules and code only |
| Catalog drift | Generated and CI-checked |
| Deployed Obot subpath behaviour unverified | Nothing outside `skills/` holds a `SKILL.md`, so either reading is safe |
