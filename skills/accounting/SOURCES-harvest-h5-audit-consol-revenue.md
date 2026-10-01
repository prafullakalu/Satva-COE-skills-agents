# Harvest sources: audit-controls, consolidation, revenue-inventory-assets (tag h5-audit-consol-revenue)

Licences read from each repo's LICENSE file in a local clone. Verbatim texts are in `skills/accounting/LICENSES/`.
Neither Apache-2.0 repo ships a NOTICE file.

## Repositories evaluated

| Repo | Licence (read from file) | Verdict | Notes |
|---|---|---|---|
| https://github.com/VincentChuWaiChow/vanguard-frontier-agentic | Apache-2.0 | imported | Strongest source: 12-27 KB standalone ASC/IFRS reference skills. 7 imported |
| https://github.com/anthropics/knowledge-work-plugins | Apache-2.0 | imported | finance/sox-testing, finance/audit-support, small-business/inventory-planner |
| https://github.com/GAJETOso/financeskills | MIT (KOMVIA) | imported | forensic-accounting, inventory-costing (with reference files and pure-computation scripts, read before copying). Other skills thinner than Vanguard equivalents or ~80-line stubs: ecl-computation, aro-computation, sox-compliance, audit-checklist, ai-anomaly-detection, revenue-recognition, lease-accounting, fixed-asset-accounting, intercompany-accounting, corporate-consolidation not imported |
| https://github.com/Receiptor-AI/bookkeeping-skills | MIT (Receiptor AI) | imported | depreciation-assets (US tax) |
| https://github.com/hazlijohar95/skills | MIT | link-only (skipped) | revenue-recognition is deep (principles, playbooks) but coupled to its closekit scripts, plugin root and agents; not tool-agnostic |
| https://github.com/countz-ai/agentic-tools | Apache-2.0 | skipped | lease, revenue-recognition and check-* skills are workers of the Countz run harness (run_dir, plugin scripts); inseparable from that tooling |
| https://github.com/simonplmak-cloud/intangible-valuation | MIT | skipped | impairment-testing is a 94-line MCP-tool wrapper; replaced by our original impairment skill |
| https://github.com/openaccountant/skills | MIT | skipped | depreciation-schedule and multi-entity are shallow and tied to the Wilson tools; Receiptor's depreciation skill is better |
| https://github.com/panaversity/agentfactory-business-plugins | Apache-2.0 | skipped | ifrs9-* skills are bank-credit-risk specific, outside these stages |
| https://github.com/anthropics/financial-services-plugins | Apache-2.0 | skipped | equity research / PE / audit-xls skills; no revenue, lease, consolidation or control skills in scope |
| https://github.com/alirezarezvani/claude-skills | MIT | skipped | compliance-os (SOC 2, ISO, GDPR) is IT compliance, not accounting controls |
| https://github.com/claude-office-skills/skills, https://github.com/karbonhq/Public-Claude-Skills | MIT | skipped | nothing on these topics |
| https://github.com/w95/awesome-claude-corporate-skills | MIT | skipped | finance skills are copies of Anthropic equity-research skills |
| https://github.com/davidnumeric/generalaccountingskills | none (clone empty) | link-only | no files, no licence |
| https://github.com/mukul975/Privacy-Data-Protection-Skills, Sushegaad/Claude-Skills-Governance-Risk-and-Compliance | not cloned | link-only | privacy / IT GRC audit, not financial audit; licences not read |

## Per-skill mapping

| Our path (under skills/accounting/) | Upstream path | Status |
|---|---|---|
| consolidation/multi-entity-intercompany-consolidation | VincentChuWaiChow/vanguard-frontier-agentic skills/accounting/consolidation-intercompany-advisor | replaced ours (our operating procedure appended) |
| consolidation/fx-translation-advisor | .../fx-translation-advisor | new |
| consolidation/business-combinations-advisor | .../business-combinations-advisor | new |
| revenue-inventory-assets/revenue-recognition-606 | .../revenue-recognition-advisor | replaced ours (our schedules, journals, memo appended) |
| revenue-inventory-assets/lease-accounting-advisor | .../lease-accounting-advisor | new |
| revenue-inventory-assets/fixed-assets-depreciation | .../fixed-assets-advisor | replaced ours (our monthly procedure and controls appended) |
| revenue-inventory-assets/equity-compensation-advisor | .../equity-compensation-advisor | new |
| revenue-inventory-assets/us-tax-depreciation-179-macrs | Receiptor-AI/bookkeeping-skills skills/depreciation-assets | new (figures flagged as year-specific) |
| revenue-inventory-assets/inventory-costing | GAJETOso/financeskills skills/inventory-costing | new |
| revenue-inventory-assets/inventory-reorder-planner | anthropics/knowledge-work-plugins small-business/skills/inventory-planner | new (connector, artifact and voice-profile dependencies removed) |
| audit-controls/sox-testing | anthropics/knowledge-work-plugins finance/skills/sox-testing | new |
| audit-controls/sox-404-audit-support-methodology | anthropics/knowledge-work-plugins finance/skills/audit-support | new (renamed to avoid clash with audit-support-pbc) |
| audit-controls/forensic-accounting | GAJETOso/financeskills skills/forensic-accounting | new |
| audit-controls/internal-controls-matrix, audit-support-pbc, fraud-red-flags | none | kept ours + see-also links added |
| revenue-inventory-assets/ecommerce-inventory-cogs | none | kept ours + see-also link added |
| revenue-inventory-assets/impairment-provisions-contingencies | none | original (no suitable permissive upstream found) |
