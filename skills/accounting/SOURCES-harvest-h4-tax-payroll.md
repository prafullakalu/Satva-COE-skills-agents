# Harvest h4: tax and payroll stages

Stage folders: `skills/accounting/tax/`, `skills/accounting/payroll/`. Licences below were read from each LICENSE file in a local clone (verbatim copies are in `skills/accounting/LICENSES/`). GitHub's licence metadata was never relied on alone. Tax content ages fast: every adapted skill keeps its "verify against current guidance" caveat and names the tax year the upstream targets.

## Repos evaluated

| Repo | Licence (read from file) | Verdict | Why | Fed |
|---|---|---|---|---|
| https://github.com/Receiptor-AI/bookkeeping-skills | MIT, (c) 2026 Receiptor AI | imported | Clear, structured US small-business tax skills (1099, estimated tax, Schedule C, meals, home office, vehicle, tax package). Vendor promotion removed. Upstream figures mostly 2024, 2026 law changes noted. | contractor-1099-reporting, estimated-tax-and-tax-prep-organiser, schedule-c-expense-categories, business-meals-deduction, home-office-deduction, vehicle-expense-deduction, tax-prep-package |
| https://github.com/anthropics/knowledge-work-plugins (small-business) | Apache-2.0 (no NOTICE file) | imported (reworked) | payroll-prep (anomaly rules, run sheet, books sync, intake) and tax-season-organizer (annualised estimate, missed quarter, assumptions, worked example) are strong. Every Gusto / QuickBooks Payroll / connector step removed. plan-payroll and tax-prep (chain skills that call sibling plugin skills) skipped as plugin-bound. | payroll-run-prep-and-anomaly-checks, payroll-accounting (references), estimated-tax-and-tax-prep-organiser (references), contractor-1099-reporting (ideas) |
| https://github.com/openaccountant/skills | MIT, (c) 2026 Open Accountant | imported (parts) | Skills are short and tied to the vendor's "Wilson" tools. Kept the substance of tax-penalty-calc, state-tax-estimator, sales-tax-nexus and contractor-tracking as references or sections of stronger skills. Not imported as standalone skills. | estimated-tax-and-tax-prep-organiser (references), sales-tax-vat-gst-compliance (reference), contractor-1099-reporting |
| https://github.com/davidjelinekk/tax-skills-claude-code | MIT, "Copyright (c) 2025-2026" (the file names no holder) | imported | 5 skills, 25 reference files, post-OBBBA US law (TY2025/2026), Illinois default state. Orchestrator reduced to a reference skill. | tax-audit-risk-assessment, tax-optimization-strategies, tax-aligned-bookkeeping, us-return-forms-and-filing-checklist, us-tax-rates-and-calendar-reference |
| https://github.com/karbonhq/Public-Claude-Skills | MIT, (c) 2026 Karbon | imported | payroll-journal-entry-skill-builder with its five reconciliation identities and provider notes. | payroll-journal-entry-skill-builder, payroll-accounting |
| https://github.com/ajaysurie/tax-prep | MIT, (c) 2026 Ajay Surie | imported (reworked) | Document collection and CPA handoff workflow with good references. SKILL.md rewritten: upstream had a network update check, MCP detection, fixed home-directory state and TurboTax export. | tax-document-collection-and-cpa-handoff |
| https://github.com/adoptai/cpa-skills | MIT, (c) 2026 AdoptAI | imported | Reviewer-grade reconciliation and review skills with local scripts (stdlib plus openpyxl, no network). The K-1 PDF extraction script (subprocess/OCR) left out. | payroll-tax-reconciliation, sales-tax-reconciliation, tax-return-review, filing-diff, return-yoy-variance, k1-extract-summarize |
| https://github.com/amit-voais/fortax-skills | Apache-2.0 (+ NOTICE) | imported | India GST/TDS/advance-tax and payroll. All use of the Fortax hosted engine removed. | see India slice below |
| https://github.com/AmolDerickSoans/gst-filing-india, SahilRakhaiya05/GST-expert-skills, NidheeshJain/itr-prep-skill | MIT | imported | India GST (most detailed found), ITR | see India slice below |
| https://github.com/ryanduguid/australian-accounting-skills, caseonix/canadian-regulatory-compliance, AlexTeplovCPA/it-contractors-skills, joetobrien/irish-accounting-skill, thriveventurelabs/accountsos-agent-plugin, erp-mafia/accounted-skills, imadbadreddine7-bot/uae-vat-registration-skill | MIT | imported | AU, CA, IE, UK, SE, UAE | see international slice below |
| https://github.com/openaccountants/openaccountants | AGPL-3.0 for software; tax Guides under the "OA Guide License" (source-available), per its LICENSING.md | **link-only** | Large country-by-country tax guide library (hundreds of skills) but not under a permitted licence. Do not copy. | none |
| https://github.com/calef/us-federal-tax-assistant-skill | GPL-3.0 (LICENSE.md read) | **link-only** | Individual US federal return prep; GPL not permitted. | none |
| https://github.com/quantavil/gstr-wala | GPL-3.0 per GitHub metadata (not cloned, LICENSE not read) | **link-only** | Indian GST engine; GPL. | none |
| https://github.com/karanb192/itr-wala, nijanthan-dev/taxmate-australia, charlootz/claude-cpa, robbalian/claude-tax-filing | GitHub shows "other" or none; no LICENSE read (charlootz clone has no LICENSE file) | **link-only** | No usable permissive licence. | none |
| https://github.com/FedTax/taxcloud-agent-skills | Apache-2.0 | skipped | Tied to one vendor's API (TaxCloud). | none |
| https://github.com/ramil/cc-payroll-plugin | MIT | skipped | SAP payroll (PCC) proof-of-concept, SAP-specific and alpha. | none |
| https://github.com/cyanxxy/nl-tax-agent-skills, arifulislamat/bd-income-tax-skills | Apache-2.0 / MIT | skipped | Dutch and Bangladeshi individual income-tax filing; out of the stage's scope (businesses, VAT/GST, payroll). | none |
| https://github.com/elderengineer/tax-organizer | MIT | skipped | 885-line individual-taxpayer monolith with no references; overlaps tax-document-collection-and-cpa-handoff. | none |
| https://github.com/anthropics/financial-services, anthropics/financial-services-plugins, panaversity/agentfactory-business-plugins, claude-office-skills/skills, alirezarezvani/claude-skills, VexloCa/toolbox, JoelLewis/finance_skills, harshith-vaddiparthy/finance-skills, w95/awesome-claude-corporate-skills, 0xelitesystem/sales-tax-nexus-awareness-reference | Apache-2.0 / MIT | skipped | Searched: no tax or payroll skill of depth (investment banking, wealth management, invoicing, or too thin). | none |
| darrentmorgan/au-accounting, ar-ti-fi/plugins, angellaudde/european-vat, hmrc/paye-estimator-skill, JohnY0920/canadian-t2-tax-skill, cynco-labs/ai-accounting-skills | MIT / Apache-2.0 | skipped | Proprietary tool set, vendor plugin runtime, French-only, an Alexa app, or not examined (T2, Malaysia). | none |

## Imported skills (per skill: upstream path, our path, status)

All are "new" in the tax and payroll stages except where noted ("replaced ours" = kept our folder name and replaced content; "kept ours + added" = our original text retained and extended).

### US tax
| Our path | Upstream | Status |
|---|---|---|
| tax/contractor-1099-reporting | Receiptor-AI/bookkeeping-skills skills/contractor-1099 (+ openaccountant business/contractor-tracking, anthropics tax-season-organizer ideas, Satva checks) | replaced ours |
| tax/estimated-tax-and-tax-prep-organiser | Receiptor skills/estimated-taxes + anthropics small-business/tax-season-organizer/reference + openaccountant tax-penalty-calc, state-tax-estimator; Satva Part B kept | replaced ours |
| tax/sales-tax-vat-gst-compliance | Satva original + openaccountant shared/sales-tax-nexus; added jurisdiction routing and a regime overview (Satva original) | kept ours + added |
| tax/tax-prep-package | Receiptor skills/tax-prep (+ jurisdictions/us.md) | new |
| tax/schedule-c-expense-categories | Receiptor skills/schedule-c-categories | new |
| tax/business-meals-deduction | Receiptor skills/meals-deduction | new |
| tax/home-office-deduction | Receiptor skills/home-office | new |
| tax/vehicle-expense-deduction | Receiptor skills/vehicle-expenses | new |
| tax/tax-audit-risk-assessment | davidjelinekk skills/tax-audit-risk | new |
| tax/tax-optimization-strategies | davidjelinekk skills/tax-optimize | new |
| tax/tax-aligned-bookkeeping | davidjelinekk skills/tax-bookkeeping | new |
| tax/us-return-forms-and-filing-checklist | davidjelinekk skills/tax-prep | new |
| tax/us-tax-rates-and-calendar-reference | davidjelinekk skills/tax (orchestrator + 4 references) | new |
| tax/tax-document-collection-and-cpa-handoff | ajaysurie/tax-prep | new |
| tax/sales-tax-reconciliation | adoptai/cpa-skills skills/sales-tax-reconciliation | new |
| tax/tax-return-review | adoptai/cpa-skills skills/tax-return-review | new |
| tax/filing-diff | adoptai/cpa-skills skills/filing-diff | new |
| tax/return-yoy-variance | adoptai/cpa-skills skills/return-yoy-variance | new |
| tax/k1-extract-summarize | adoptai/cpa-skills skills/k1-extract-summarize | new |

### Payroll
| Our path | Upstream | Status |
|---|---|---|
| payroll/payroll-accounting | Satva original + karbonhq reconciliation-identities and provider notes + anthropics payroll-prep books_sync | kept ours + added |
| payroll/payroll-run-prep-and-anomaly-checks | anthropics/knowledge-work-plugins small-business/skills/payroll-prep | new |
| payroll/payroll-journal-entry-skill-builder | karbonhq/Public-Claude-Skills plugins/karbon-claude-plugins/skills/payroll-journal-entry-skill-builder | new |
| payroll/payroll-tax-reconciliation | adoptai/cpa-skills skills/payroll-tax-reconciliation | new |

### India, international and Israel slices
See the three evaluation tables at the end of this file (written by the helper forks).

## Licence files saved in skills/accounting/LICENSES/

Receiptor-AI__bookkeeping-skills, anthropics__knowledge-work-plugins, openaccountant__skills, davidjelinekk__tax-skills-claude-code, karbonhq__Public-Claude-Skills, ajaysurie__tax-prep, adoptai__cpa-skills, plus the India and international repos listed below.

## Not verified

- No upstream rate, threshold, bracket or due date was checked against official sources. Each skill states the tax year it targets (US figures: 2024 in Receiptor files, 2025 in the Anthropic and Illinois files; India FY 2026-27; AU/UK checked dates in the upstream's own notes).
- `sales-tax-vat-gst-compliance/references/vat-gst-regimes-overview.md` and `eu-vat-cross-border-oss` are Satva originals written from general knowledge; thresholds are marked last-known and must be verified.
- Bundled scripts (India GST, interest computation, adoptai reconciliations) were read for network, subprocess and destructive calls; their self-tests were run only for the India GST scripts.


---

## India slice (fork)

| Repo | Licence (read from LICENSE) | Verdict | Reason | Fed |
|---|---|---|---|---|
| https://github.com/AmolDerickSoans/gst-filing-india | MIT, (c) 2026 Amol Derick Soans | imported | Most detailed GST skill found: 16 references, 7 checklists/templates, 7 scripts. Dropped browser-automation reference (Claude-in-Chrome specific), automation checklist, and the action_log/period_state scripts (rmtree in selftests; replaced by two hand-kept markdown files). Kept 5 pure-local scripts (selftests pass). | india-gst-compliance |
| https://github.com/SahilRakhaiya05/GST-expert-skills | MIT, (c) 2026 Indian GST Expert Skill Contributors | imported (2 refs) | HSN/SAC guide and FY2026-27 compliance calendar added as references 17, 18; rest overlaps Amol. Its .skill zip and calculator not copied. | india-gst-compliance |
| https://github.com/amit-voais/fortax-skills | Apache-2.0 (+NOTICE) | imported (7 skills + merged 2) | Methodology is strong; all dependence on the Fortax hosted engine (scripts/fortax.py, kb lookups, ai.fortax.in), browser-tool instructions and cross-skill names removed. Copied only compute_interest_234.py (read: stdlib only, no network). Skipped: fortax-gstr1-and-3b, gstr2b-reconciliation, gst-annual-return, gst-eway-einvoice, gst-lut-refunds (superseded by the more detailed MIT gst-india), itr / itr-portal-operations / notice-reply (engine- and portal-automation-bound; ITR covered by NidheeshJain), and non-tax skills (legal, MCA, trademark, DPDP, xlsx, pdf, etc.). | see below |
| https://github.com/Loki200399/india-itr-copilot | MIT, (c) 2026 Lokendar Ram P S (licence text taken from the copy inside fortax-skills; repo itself not cloned) | imported (1 script) | compute_interest_234.py | india-advance-tax-and-interest |
| https://github.com/NidheeshJain/itr-prep-skill | MIT, (c) 2026 Nidheesh Jain | imported | Detailed personal ITR skill, 10 references. Dropped decrypt_ais.py (handles PAN/DOB passwords) and self-install instructions. | india-itr-preparation |
| https://github.com/mnbresearch/mnb-claude-skills (gst-invoice-compliance) | MIT, (c) 2025 Mridul Nanda / MNB Research | skipped | Introductory, thin vs gst-india. | none |

| Upstream path | Our path | Status |
|---|---|---|
| AmolDerickSoans/gst-filing-india skills/gst-india (+ SahilRakhaiya05 refs) | skills/accounting/tax/india-gst-compliance | new |
| fortax-skills skills/fortax-gst-registration + fortax-gst-amendment-cancellation | skills/accounting/tax/india-gst-registration-and-amendment | new (merged) |
| fortax-skills skills/fortax-tds | skills/accounting/tax/india-tds-tcs-returns | new |
| fortax-skills skills/fortax-advance-tax-and-interest | skills/accounting/tax/india-advance-tax-and-interest | new |
| NidheeshJain/itr-prep-skill | skills/accounting/tax/india-itr-preparation | new |
| fortax-skills skills/fortax-payroll-monthly-run | skills/accounting/payroll/india-payroll-monthly-run | new |
| fortax-skills skills/fortax-payroll-registrations | skills/accounting/payroll/india-payroll-registrations-pf-esi-pt | new |
| fortax-skills skills/fortax-salary-structuring | skills/accounting/payroll/india-salary-structuring | new |
| fortax-skills skills/fortax-gratuity-bonus-leave | skills/accounting/payroll/india-gratuity-bonus-leave | new |
| fortax-skills skills/fortax-hr-compliance-calendar | skills/accounting/payroll/india-hr-compliance-calendar | new |

Licence files saved: LICENSES/AmolDerickSoans__gst-filing-india.LICENSE, SahilRakhaiya05__GST-expert-skills.LICENSE, amit-voais__fortax-skills.LICENSE + .NOTICE, Loki200399__india-itr-copilot.LICENSE, NidheeshJain__itr-prep-skill.LICENSE


---

# FRAGMENT-intl (non-US, non-India slice)

## Repos evaluated
| Repo | Licence (read from file) | Verdict | Reason | Fed |
|---|---|---|---|---|
| https://github.com/ryanduguid/australian-accounting-skills | MIT (c) 2026 Ryan Duguid; NOTICE copied | imported | detailed AU workpaper skills, ATO-primary-source disciplined | au-gst-bas-workpaper, au-payroll-super-and-payroll-tax |
| https://github.com/darrentmorgan/au-accounting | MIT | skipped | skills call a proprietary tool set (bas_gst_worksheet etc.), tool-tied | none |
| https://github.com/caseonix/canadian-regulatory-compliance | MIT (c) 2026 Srivatsa Kasagar | imported (canadian-tax-compliance only) | CA GST/HST, payroll, corp tax overview; 2025 figures | ca-tax-compliance-gst-hst-payroll |
| https://github.com/AlexTeplovCPA/it-contractors-skills | MIT (c) 2026 Alex Teplov | imported (checking-gst-hst as reference only) | other 18 skills are T2125 personal self-entry workflows, out of scope | ca-tax-compliance-gst-hst-payroll |
| https://github.com/JohnY0920/canadian-t2-tax-skill | Apache-2.0 | skipped | corporate T2 return prep, not examined in depth (out of time) | none |
| https://github.com/joetobrien/irish-accounting-skill | MIT (c) 2026 Joe O'Brien / Web Digital Innovation | imported (Xero/API/MCP parts removed) | full Irish Revenue framework | ie-revenue-vat-and-compliance |
| https://github.com/angellaudde/european-vat | MIT | skipped | body and references are in French; not translated. Original English skill written instead | eu-vat-cross-border-oss (original) |
| https://github.com/thriveventurelabs/accountsos-agent-plugin | MIT (c) 2026 Thrive Venture Labs | imported (vat-rules, tax-deadlines) | UK VAT/MTD and calendar, verified 2026/27 upstream; other skills (uk-accounting, expense-categories) not taken | uk-vat-mtd-and-tax-deadlines |
| https://github.com/hmrc/paye-estimator-skill | Apache-2.0 | skipped | Amazon Alexa JS skill, not an agent SKILL.md | none |
| https://github.com/erp-mafia/accounted-skills | MIT (c) 2026 ERP MAFIA | imported (swedish-vat, swedish-payroll) | detailed Swedish references; other 18 Swedish skills (bookkeeping, SIE, K2/K3, industries) belong to other stages | se-vat-moms, se-payroll-agi |
| https://github.com/ar-ti-fi/plugins | MIT | skipped | Estonian VAT/payroll plugins tied to a vendor plugin runtime | none |
| https://github.com/imadbadreddine7-bot/uae-vat-registration-skill | MIT (c) 2026 Squarezone Corporate Services LLC-FZ | imported | UAE VAT registration threshold and EmaraTax walkthrough | uae-vat-registration-turnover-check |
| https://github.com/skills-il/tax-and-finance, skills-il/accounting | MIT | skipped | Israel lowest priority; not reviewed | none |
| https://github.com/cynco-labs/ai-accounting-skills | MIT | skipped | Malaysian, low priority | none |

## Per skill
| Our path | Upstream path | Status |
|---|---|---|
| skills/accounting/tax/au-gst-bas-workpaper | ryanduguid .claude/skills/bas-preparation (+ au-gst-registration-review, tax-invoice-review, au-payg-instalment-variation, au-ato-penalties-interest as references) | new |
| skills/accounting/payroll/au-payroll-super-and-payroll-tax | .claude/skills/au-payroll-review (+ stp-finalisation, au-payroll-tax-states, payroll-tax-contractors, contractor-super-tpar as references) | new |
| skills/accounting/tax/ca-tax-compliance-gst-hst-payroll | caseonix skills/canadian-tax-compliance (+ AlexTeplov checking-gst-hst reference) | new |
| skills/accounting/tax/uk-vat-mtd-and-tax-deadlines | thriveventurelabs skills/vat-rules (+ tax-deadlines reference) | new |
| skills/accounting/tax/ie-revenue-vat-and-compliance | joetobrien SKILL.md | new |
| skills/accounting/tax/se-vat-moms | erp-mafia swedish-vat | new |
| skills/accounting/payroll/se-payroll-agi | erp-mafia swedish-payroll | new |
| skills/accounting/tax/uae-vat-registration-turnover-check | imadbadreddine7-bot SKILL.md | new |
| skills/accounting/tax/eu-vat-cross-border-oss | none (Satva-original) | new |

Licences saved in skills/accounting/LICENSES/: ryanduguid__australian-accounting-skills (.LICENSE + .NOTICE), caseonix__canadian-regulatory-compliance, AlexTeplovCPA__it-contractors-skills, thriveventurelabs__accountsos-agent-plugin, joetobrien__irish-accounting-skill, erp-mafia__accounted-skills, imadbadreddine7-bot__uae-vat-registration-skill.


---

| Repo | Licence (read from file) | Verdict | Skills fed |
|---|---|---|---|
| https://github.com/skills-il/tax-and-finance | MIT, Copyright (c) 2026 Skills IL (Yootech) | imported (israeli-vat-reporting); israeli-tax-withholding skipped (overlap/size) | il-vat-reporting |
| https://github.com/skills-il/accounting | MIT, Copyright (c) 2026 Skills IL (Yootech) | imported (israeli-payroll-calculator) | il-payroll-calculator |

| Upstream path | Our path | Status |
|---|---|---|
| tax-and-finance/israeli-vat-reporting | skills/accounting/tax/il-vat-reporting | new |
| accounting/israeli-payroll-calculator | skills/accounting/payroll/il-payroll-calculator | new |
