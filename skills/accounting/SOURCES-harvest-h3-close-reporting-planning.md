# Harvest sources: close, reporting, planning (tag h3-close-reporting-planning)

## Repos evaluated
| Repo | Licence (read from LICENSE) | Verdict | Notes |
|---|---|---|---|
| https://github.com/anthropics/knowledge-work-plugins | Apache-2.0 (no NOTICE file; no copyright line in LICENSE) | imported | finance/close-management, variance-analysis, financial-statements; data/build-dashboard. small-business/* skills (month-end-prep, cash-flow-snapshot, close-month, report-pack) skipped: bound to named ledger/processor connectors |
| https://github.com/anthropics/financial-services-plugins | Apache-2.0 (no NOTICE) | imported | 3-statement-model. month-end-closer agent skills (accrual-schedule, roll-forward, variance-commentary) skipped: ~35 lines each, thin |
| https://github.com/alirezarezvani/claude-skills | MIT, Copyright (c) 2025 Alireza Rezvani | imported | board-deck-builder. cfo-advisor, financial-analyst, scenario-war-room, saas-metrics-coach already imported by another agent under advisory/industries |
| https://github.com/Receiptor-AI/bookkeeping-skills | MIT, Copyright (c) 2026 Receiptor AI | imported | monthly-close |
| https://github.com/GAJETOso/financeskills | MIT, Copyright (c) 2026 KOMVIA | imported | budget-forecast, working-capital-analysis, cvp-breakeven, predictive-burn-rate, product-profitability (its close-management, variance-analysis, statement-preparation, three-statement-modeling skipped: ~80 lines, weaker than the Anthropic versions) |
| https://github.com/EveryInc/charlie-cfo-skill | MIT, Copyright (c) 2026 Every | imported | SKILL.md + references |
| https://github.com/claude-office-skills/skills | MIT, Copyright (c) 2026 Claude Office Skills Contributors | skipped | saas-metrics and financial-modeling are template-style and tied to named analytics MCP tools; covered better by saas-metrics-coach and three-statement-model |
| https://github.com/openaccountant/skills | MIT, Copyright (c) 2026 Open Accountant | skipped | month-end-close, cash-flow-forecast, runway-calculator are 65-80 lines and tied to the vendor's own tools |
| https://github.com/panaversity/agentfactory-business-plugins | Apache-2.0 | skipped | nothing for these stages (banking/ifrs9 only) |
| https://github.com/karbonhq/Public-Claude-Skills | MIT, Copyright (c) 2026 Karbon | skipped | no skills for these stages (SOP audit, firm AI strategy, payroll JE builder) |
| https://github.com/anthropics/skills | no top-level LICENSE (THIRD_PARTY_NOTICES only) | link-only | no finance skills; per-skill licences differ |
| https://github.com/mohitagw15856/pm-claude-skills | MIT, Copyright (c) 2026 Mohit Aggarwal | skipped | pm-accounting / pm-finance skills are 60-90 line stubs |
| https://github.com/w95/awesome-claude-corporate-skills | MIT, Copyright (c) 2026 Enrike | skipped | largely copies of the Anthropic financial-services skills; imported from the original instead |
| https://github.com/vivy-yi/finance-skills | MIT, Copyright (c) 2026 vivy-yi | link-only | deep CFO-domain set (month-end-close, budget-management, kpi-management, board-reporting) but in Chinese and built on PRC accounting standards; not suitable for the Satva library without full translation and re-basing |
| https://github.com/JoelLewis/finance_skills | MIT, Copyright (c) 2026 Joel Lewis | skipped | wealth management / advisory practice, off-topic |
| https://github.com/himself65/finance-skills | MIT, Copyright (c) 2025 Alex Yang | skipped | market data and equity analysis, off-topic |
| https://github.com/get-zeked/finance-super-skill | no LICENSE file | link-only | no licence |
| https://github.com/willpowerju-lgtm/3-statement-ultra-for-finance | not checked (no licence seen in GitHub metadata) | link-only | not cloned |
| https://github.com/jeremylongshore/excel-analyst-pro-skill-md | GitHub reports "other" | link-only | unclear licence, not cloned |
| https://github.com/Apennilessbear/Claude-Finance-Skills | MIT, Copyright (c) 2026 ryanlane17-web | skipped | only an Excel formula-auditing skill, outside my stages |
| https://github.com/RKiding/Awesome-finance-skills | Apache-2.0 | skipped | markets/trading focus |

## Imported skills
| Our path | Upstream path | Status |
|---|---|---|
| close/month-end-close | anthropics/knowledge-work-plugins finance/skills/close-management | replaced ours (original controls folded in) |
| close/flux-variance-analysis | anthropics/knowledge-work-plugins finance/skills/variance-analysis | replaced ours (original review discipline folded in) |
| reporting/financial-statement-preparation | anthropics/knowledge-work-plugins finance/skills/financial-statements | replaced ours (original pre-flight and cash-flow tie-out folded in) |
| close/small-business-monthly-close | Receiptor-AI/bookkeeping-skills skills/monthly-close | new |
| reporting/board-deck-builder | alirezarezvani/claude-skills c-level-advisor/skills/board-deck-builder | new |
| reporting/kpi-dashboard-builder | anthropics/knowledge-work-plugins data/skills/build-dashboard | new |
| planning/three-statement-model | anthropics/financial-services-plugins plugins/vertical-plugins/financial-analysis/skills/3-statement-model | new |
| planning/budget-forecast | GAJETOso/financeskills skills/budget-forecast | new |
| planning/working-capital-analysis | GAJETOso/financeskills skills/working-capital-analysis | new |
| planning/cvp-breakeven | GAJETOso/financeskills skills/cvp-breakeven | new |
| planning/runway-burn-forecast | GAJETOso/financeskills skills/predictive-burn-rate | new |
| planning/product-profitability | GAJETOso/financeskills skills/product-profitability | new |
| planning/bootstrapped-cfo-playbook | EveryInc/charlie-cfo-skill | new |

## Kept ours / originals
- close/quarter-and-year-end-close: kept ours (no upstream matched its depth on subsequent events, going concern, audit file).
- planning/cash-flow-forecasting: kept ours (13-week direct plus 12-month indirect; the Anthropic cash-flow-snapshot is bound to named connectors).
- reporting/financial-reporting-pack: kept ours.
- reporting/ecommerce-kpi-metrics: new Satva original (no permissively licensed upstream found).

## Scripts bundled (read; pure local computation, no network or file writes)
small-business-monthly-close/scripts/monthly_close_summary.py; calculate.py in budget-forecast, working-capital-analysis, cvp-breakeven, runway-burn-forecast, product-profitability.
