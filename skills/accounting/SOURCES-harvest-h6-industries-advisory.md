# Harvest sources: h6-industries-advisory (industries, advisory, treasury)

Clones made 2026-10-01 into a scratch dir; LICENSE files read from the clones. GitHub search API was rate-limited mid-session, so wildcard discovery relied on known repos plus direct clones.

## Repos evaluated

| Repo | Licence (read from LICENSE) | Verdict | Notes |
|---|---|---|---|
| https://github.com/alirezarezvani/claude-skills | MIT, (c) 2025 Alireza Rezvani | imported | cfo-advisor, ma-playbook, financial-analyst, business-investment-advisor, scenario-war-room, saas-metrics-coach. Pure-stdlib scripts copied after reading. Other c-level skills not imported (CxO role playbooks outside accounting). |
| https://github.com/anthropics/financial-services (identical content to anthropics/financial-services-plugins) | Apache-2.0 (no NOTICE file) | imported | Valuation, M&A and PE diligence skills. MCP/data-vendor wording made tool-agnostic. Scripts (validate_dcf.py, contains pip-install message) and requirements.txt not copied. Equity research, IB pitch/CIM/teaser, partner-built (LSEG, S&P) and KYC skills skipped: not accounting, or vendor-tied. |
| https://github.com/karbonhq/Public-Claude-Skills | MIT, (c) 2026 Karbon | imported (1 of 3) | sop-library-auditor imported (parse_sops.py not copied, pip-install messages). firm-ai-strategy skipped: Karbon-product-tied, mandatory "Powered by Karbon" footer. payroll-journal-entry-skill-builder belongs to the payroll stage. |
| https://github.com/anthropics/knowledge-work-plugins | Apache-2.0 | skipped for these folders | small-business/cash-flow-snapshot needs ledger/payment connectors and overlaps planning/cash-flow-forecasting. |
| https://github.com/JoelLewis/finance_skills | MIT, (c) 2026 Joel Lewis | link-only for these folders | Wealth-management and personal-finance oriented (currencies-and-fx, liquidity-management, debt-management, digital-assets target individuals/portfolios, not corporate treasury or company books). |
| https://github.com/claude-office-skills/skills | MIT | skipped | saas-metrics, dcf-valuation, investment-memo, financial-modeling, crypto-report duplicate better imported skills or are market commentary. |
| https://github.com/openaccountant/skills | MIT | skipped | runway-calculator, break-even-calc, pricing-optimizer, client-profitability, rental-property are 55-85 line stubs; covered by our originals. |
| https://github.com/panaversity/agentfactory-business-plugins | Apache-2.0 | skipped | Banking regulatory skills (LCR, NSFR, Basel, IFRS 9 for banks) are not corporate treasury. |
| https://github.com/Receiptor-AI/bookkeeping-skills | MIT | skipped | Sole-proprietor US tax bookkeeping; outside these folders. |
| https://github.com/yuping322/financial-services-plugins-new and other forks of Anthropic financial-services (Apache-2.0 per GitHub metadata) | not cloned | skipped | Forks/translations of the same upstream; no need to duplicate. |

## Imported skills

| Our skill | Upstream path | Status |
|---|---|---|
| advisory/cfo-advisor | alirezarezvani/claude-skills c-level-advisor/skills/cfo-advisor | new (refs + scripts kept) |
| advisory/ma-playbook | c-level-advisor/skills/ma-playbook | new |
| advisory/financial-analyst | finance/skills/financial-analyst | new (refs, assets, scripts) |
| advisory/business-investment-advisor | finance/business-investment-advisor/skills/business-investment-advisor | new |
| advisory/scenario-war-room | c-level-advisor/skills/scenario-war-room | new |
| industries/saas-metrics-coach | finance/skills/saas-metrics-coach | new (refs, assets, scripts) |
| advisory/dcf-model | anthropics/financial-services plugins/vertical-plugins/financial-analysis/skills/dcf-model | new |
| advisory/comparable-company-analysis | .../financial-analysis/skills/comps-analysis | new |
| advisory/lbo-model | .../financial-analysis/skills/lbo-model | new |
| advisory/merger-model | .../investment-banking/skills/merger-model | new |
| advisory/due-diligence-checklist | .../private-equity/skills/dd-checklist | new |
| advisory/unit-economics-analysis | .../private-equity/skills/unit-economics | new |
| advisory/value-creation-plan | .../private-equity/skills/value-creation-plan | new |
| advisory/pe-returns-analysis | .../private-equity/skills/returns-analysis | new |
| advisory/investment-committee-memo | .../private-equity/skills/ic-memo | new |
| advisory/sop-library-auditor | karbonhq/Public-Claude-Skills plugins/karbon-claude-plugins/skills/sop-library-auditor | new (stripped trailing NUL bytes from upstream SKILL.md) |

Satva-original (written from practitioner expertise, no upstream): advisory (fractional-cfo-playbook, startup-fundraising-readiness, quality-of-earnings-review, small-business-valuation, pricing-and-profitability-analysis, accounting-firm-engagement-letters-and-pricing, accounting-firm-client-onboarding-sop, accounting-practice-workflow-management); industries (nonprofit-fund-accounting, construction-job-costing, real-estate-property-accounting, healthcare-practice-accounting, professional-services-and-agency-accounting, retail-ecommerce-accounting, manufacturing-cost-accounting, restaurant-accounting, crypto-asset-accounting, saas-accounting); treasury (corporate-cash-management, banking-relationships-and-facilities, fx-exposure-and-revaluation, debt-and-covenant-management, corporate-investment-policy).
