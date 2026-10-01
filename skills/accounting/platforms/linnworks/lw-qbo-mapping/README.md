# lw-qbo-mapping

Read-only Claude Code skill: analyzes Linnworks ecommerce/operational data against QuickBooks
Online accounting data for a period, maps Linnworks dimensions to QBO accounting objects,
identifies mapping/data gaps, computes count- and value-based coverage, and reconciles Linnworks
totals against QBO totals. Produces an auditable markdown report.

## Why this exists, and why it isn't a COA mapper

Linnworks is **not** a chart-of-accounts system. It's an operational/ecommerce system: orders,
channels, SKUs, refunds, shipping, warehouses. None of that is directly an accounting object.
This skill's mapping engine has two stages, not one:

```
Linnworks dimension  --[ concept translation ]-->  Accounting concept  --[ matching ]-->  QBO object
```

The `concept translation` step is what generic chart-of-accounts mappers (e.g. `coa-mapper-mcp`,
which maps QuickBooks<->Xero<->Wave COAs to each other) don't do — see the research report from
this project's design phase for why that tool couldn't be reused as-is.

## How it uses the two MCPs

- **Linnworks** (`mcp__satva-linnworks-read-only__*`): read-only SQL-backed tools over an
  allowlisted table set (orders, refunds, returns, stock, suppliers, etc.). No write tools exist.
- **QuickBooks** (`mcp__satva-quickbooks__*`): has both read and write tools, but this skill calls
  **only** read tools (`get_*`, `search_*`, `query_quickbooks`, `list_companies`,
  `describe_entity`). It never calls `create_*`/`update_*`/`delete_*`/`void_*`.

Tool → entity mapping (verified against this project's actual connected servers, not assumed) is
in `SKILL.md`.

## Architecture

```
reference/               design docs the engine and skill both follow
  gap-taxonomy.md         MAPPED/UNMAPPED/AMBIGUOUS/UNVERIFIED/INVALID/ORPHANED/INACTIVE/STRUCTURAL_DATA_GAP
  confidence-model.md     HIGH/MEDIUM/LOW/UNRESOLVED + the account pipeline (8 steps) AND the
                           product/SKU-identity pipeline (SKU -> name -> price/qty corroboration)
  normalization-schema.md SourceRecord / AccountingConcept / TargetRecord / MappingResult shapes

scripts/                  deterministic, dependency-free (Python stdlib only), no MCP calls inside
  normalize.py             raw MCP JSON -> SourceRecord[] / TargetRecord[]
  mapping_engine.py         propose_mapping() (channel/refund/tax -> account, steps 1-6 + orphan
                            pass) AND match_product_identity() (Linnworks StockItem -> QBO Item,
                            SKU -> name -> price/qty corroboration + orphan pass)
  coverage.py               MappingResult[] -> count/value coverage numbers per status bucket
                            (MAPPED/UNMAPPED/AMBIGUOUS/UNVERIFIED/INVALID/INACTIVE/
                            STRUCTURAL_DATA_GAP/ORPHANED)
  reconcile.py               Linnworks total vs QBO total -> variance row (currency-mismatch-safe)
  conclusions.py             deterministic "what do these numbers mean" bullets, traceable to the
                            computed coverage/reconciliation/gap facts -- not freehand narrative
  report.py                  renders the final markdown report: Overall, Key Findings, full
                            Category Summary table, account Mapping Matrix, Product/SKU Matching
                            table, Data Gaps, Reconciliation, Unresolved Items
  export_xlsx.py              INVENTORY-focused .xlsx export, 2 sheets only: "Matched Products"
                            (Linnworks SKU/name <-> QBO SKU/name/COA, plus post-match price/qty
                            verification) and "Unmatched - Needs Review" (everything else, with
                            its reason). Requires openpyxl -- report.py's markdown has no such
                            dependency and always works as a fallback.

tests/                    37 cases (16 spec-mandated + product-matching + conclusions + inventory
                          xlsx export), all SYNTHETIC fixtures, no live MCP calls
```

## Running it

```bash
cd .claude/skills/lw-qbo-mapping
python -m unittest discover -s tests -v      # 19 tests, all synthetic
```

To run a real analysis, invoke the skill in Claude Code (`/lw-qbo-mapping` or by asking "analyze my
Linnworks and QuickBooks data for <period>") — the agent fetches live data per `SKILL.md`'s tool
table, normalizes it with `normalize.py`, and drives the rest of the pipeline (mapping_engine.py,
coverage.py, reconcile.py, conclusions.py, report.py / export_xlsx.py).

## Known limitations (v1)

- **Read-only, always.** Proposing a mapping never applies it. A later phase could add a
  write-back of confirmed HIGH-confidence mappings into a `mapping_rules.json`, but that requires
  explicit user opt-in per spec §11 — not built here.
- **No LLM step wired into the deterministic scripts.** `mapping_engine.apply_llm_proposal()`
  exists as the integration point; the calling skill is responsible for deciding when to invoke the
  LLM (only on `UNRESOLVED` results with real source information, never for STRUCTURAL_DATA_GAP
  cases where no amount of reasoning fixes a missing source field).
- **Marketplace/PSP fees are a confirmed structural gap**, not a bug: no field for them exists
  anywhere in the allowlisted Linnworks schema (verified via `listTables`/`describeTable` against
  the live server, not assumed).
- **Currency mismatches block reconciliation** rather than producing a wrong number — see
  `reconcile.py`'s `CURRENCY_MISMATCH` status.


## Accountant workflow (per client, on the user's own machine)

`scripts/run_analysis.py` turns Linnworks + QuickBooks data into `~/LW-QBO-Mapping/<client>/workbook.xlsx`
(+ `summary.csv`). The workbook is both the accountant's control panel and the skill's memory:

| Sheet | Purpose |
|---|---|
| Start Here | Plain-English status and health score |
| Needs Your Decision | Approve / Reject / Change dropdown; picks are learned next run |
| Approved Mappings | Everything confirmed (this replaces any JSON rules file) |
| Matched Products, Only in QuickBooks, Only in Linnworks | The two-sided diff |
| What's Wrong | Plain-language findings and data gaps |
| History, Change Log, Glossary | Trend, audit trail, terms |

Design rules: both systems are required (no one-sided reports); client data never enters the repo; no
credentials are read or stored (they live in the MCP connections); read-only on both systems; a backup
precedes every write; a workbook open in Excel produces a `_pending` copy instead of an error.

Install: `./install.sh` or `install.ps1` from the repo root copies the skill; it needs `python` and `openpyxl`.
