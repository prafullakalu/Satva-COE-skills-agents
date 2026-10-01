---
name: se-vat-moms
description: >-
  Swedish VAT (moms) compliance: reporting periods and deadlines, EU reverse charge and OSS, import/export VAT, representation VAT, mixed-use proportional deduction, input-VAT adjustment (jamkning), voluntary VAT liability for rental, momsdeklaration box-to-BAS-account mapping and common error patterns. Use for "momsdeklaration", "omvand skattskyldighet", "which BAS account for reverse charge VAT", "Swedish VAT rate", "skattetillagg". Rates as stated upstream; verify at skatteverket.se.
metadata:
  department: "accounting"
  domain: "tax"
  owner: "satva-coe"
  status: "beta"
  license: "MIT"
  source: "https://github.com/erp-mafia/accounted-skills/tree/main/.claude/skills/swedish-vat"
---

<!-- Adapted from erp-mafia/accounted-skills .claude/skills/swedish-vat/SKILL.md (MIT, Copyright (c) 2026 ERP MAFIA). Modified by Satva: dropped local-path instructions; rates are as stated upstream. -->

# Swedish VAT (Moms) Compliance Skill

This skill provides authoritative compliance reference for Swedish VAT. It is the **single highest-error-rate area** in Swedish bookkeeping.

## When to use

Always read the full reference before answering ANY question about:

- Momsredovisning periods, thresholds, deadlines
- EU VAT: reverse charge, intra-EU goods/services, triangulation, OSS
- Import/export VAT
- Representation moms (deduction limits, BAS accounts)
- Mixed activities (proportional deduction, HFD 2023 ref. 45)
- Jämkning (adjustment of input VAT on capital goods)
- Frivillig skattskyldighet for property rental
- Momsdeklaration field-to-BAS account mapping
- BAS 26xx account usage
- VAT error patterns, penalties, skattetillägg

## How to use

2. Find the relevant section for the user's question
3. Provide precise answers with account numbers, ruta numbers, legal references, and thresholds
4. Flag common error patterns relevant to the user's scenario

## Quick reference: VAT rates

| Rate | Applies to |
|------|-----------|
| 25% | Default rate, most goods and services |
| 12% | Hotel, restaurant and catering, camping, repairs (bicycles/shoes/leather goods/clothing/household linen, ML 9:7); food before 2026-04-01 and again from 2028-01-01 (SFS 2026:119) |
| 6% | Books, newspapers, transport, cultural events, sports; food (livsmedel, incl. takeaway) 2026-04-01 to 2027-12-31 (SFS 2026:118); entry to dance events from 2026-07-01 (SFS 2026:841) |
| 0% | Exports outside EU, intra-EU supplies (with conditions) |

## Quick reference: Key BAS accounts

| Account | Purpose | Momsdeklaration |
|---------|---------|-----------------|
| 2611 | Utgående moms domestic 25% | Ruta 10 |
| 2614 | Utgående moms reverse charge 25% | Ruta 30 |
| 2615 | Utgående moms import 25% | Ruta 60 |
| 2641 | Debiterad ingående moms | Ruta 48 |
| 2645 | Beräknad ingående moms förvärv utlandet | Ruta 48 |
| 2650 | Momsredovisningskonto (clearing) | Ruta 49 |

## Quick reference: Reporting thresholds

| Annual beskattningsunderlag | Default period |
|----------------------------|----------------|
| ≤ 1M SEK | Annual |
| > 1M - ≤ 40M SEK | Quarterly |
| > 40M SEK | Monthly |

## Critical error patterns to flag

1. **2611 vs 2614**: Reverse charge output VAT must go to 2614 (Ruta 30), never 2611 (Ruta 10)
2. **One-sided reverse charge**: Both output AND input VAT must be booked; silent netting is prohibited
3. **Import double-counting**: Since 2015, VAT-registered businesses report import VAT to Skatteverket only, not Tullverket
4. **Representation**: VAT deductible on 300 SEK base; income tax deduction abolished for meals since 2017
5. **Period-end clearing**: All 261x-264x must clear to 2650; residual balances cause reconciliation failures

For the complete reference with all account mappings, legal citations, formulas, and detailed rules, read:
`references/vat-compliance-reference.md`
