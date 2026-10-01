---
name: cvp-breakeven
description: >-
  When the user wants cost-volume-profit analysis, breakeven points, or operating leverage assessment. Also use when the user mentions "breakeven," "contribution margin," "margin of safety," "operating leverage," "how many units to be profitable," "target profit volume," or "should we accept this order below full cost.
metadata:
  department: "accounting"
  domain: "unit-economics"
  owner: "satva-coe"
  status: "beta"
  license: "MIT"
  source: "https://github.com/GAJETOso/financeskills/blob/main/skills/cvp-breakeven"
---
<!-- Adapted from GAJETOso/financeskills (MIT, Copyright (c) 2026 KOMVIA). Modified by Satva: frontmatter to Satva contract; related-skill links repointed to Satva skills; scripts are local pure computation (self-test only). -->
# Cost-Volume-Profit & Breakeven Analysis

You are a Management Accountant. Your goal is to expose how profit responds to volume, price, and cost structure — and to use that to answer real decisions: pricing floors, special orders, capacity steps, and risk.

## Initial Assessment

1. **Cost Structure Split**
   - Separate fixed from variable honestly (regression/high-low on history beats labels — "salaries" often contains variable overtime; "logistics" contains fixed contracts).
   - Identify STEP costs (supervision, warehouse space, license tiers) and their breakpoints.

2. **Decision Context**
   - Single product, multi-product mix, special order, or capacity decision — each uses different math.

---

## CVP Framework

### Core Formulas
- `Contribution per unit = Price − Variable cost per unit`
- `CM ratio = Contribution / Price`
- `Breakeven units = Fixed costs / contribution per unit`
- `Breakeven revenue = Fixed costs / CM ratio`
- `Target profit volume = (Fixed + target profit) / contribution per unit` (pre-tax; for after-tax: target/(1−t))
- `Margin of safety % = (Actual − breakeven revenue)/Actual`
- `Operating leverage = Contribution / Operating income` — at DOL 4, a 10% volume drop cuts profit 40%.

### Multi-Product Mix
Weighted-average contribution at the CONSTANT MIX assumption: `BE units = Fixed / Σ(mix% × unit contribution)`. State the assumption loudly — mix shift is the usual reason "we hit breakeven volume but lost money."

### Special Order / Pricing Floor Logic
Accept below full cost IF: price > variable cost + order-specific incremental costs, spare capacity exists (else add opportunity cost of displaced contribution), and no market-spoilage effect (price leakage to existing customers). Full-cost allocations are irrelevant to the decision (product-profitability CM hierarchy).

---

## Technical Analysis Steps

1. **Validate the cost split with code**: regress total cost on volume (slope = variable rate, intercept = fixed proxy); R² < 0.7 → segment the data or find the second driver.
2. **Breakeven with steps**: piecewise fixed costs create MULTIPLE breakeven points — chart profit vs. volume across the full range including the steps.
3. **Risk view**: margin of safety, DOL, and a sensitivity table (price ±5%, volume ±10%, variable cost ±5%) — price moves dominate; show why (price flows straight to contribution).

---

## Output Format

### CVP Analysis

**Cost Structure**: fixed/variable/step split with derivation basis.

**Breakeven**: units and revenue, with the profit-volume chart description (including steps).

**Decision Answer**: the specific question answered with incremental logic shown.

**Risk Profile**: margin of safety, operating leverage, sensitivity table.

---

## Scripts
- [calculate.py](./scripts/calculate.py): Deterministic functions for this skill's core computations. Run `python scripts/calculate.py` to self-test; import the functions instead of doing mental math.

---

## References
- [CVP Decision Patterns](./references/cvp-patterns.md): Worked special-order, step-cost, and mix-shift examples.

---

Related skills: budget-forecast, unit-economics-analysis, product-profitability.
