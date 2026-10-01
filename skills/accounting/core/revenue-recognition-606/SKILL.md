---
name: revenue-recognition-606
description: >-
  Revenue recognition under ASC 606 / IFRS 15: the five-step model, performance obligations, variable consideration, contract modifications, principal vs agent, deferred revenue schedules and journal entries. Use for "how should we recognise this revenue", "deferred revenue schedule", "SaaS subscription accounting", "multi-element contract", "gross vs net revenue", "606 memo". Judgement areas need a qualified accountant.
metadata:
  department: "accounting"
  domain: "revenue"
  owner: "satva-coe"
  status: "beta"
  license: "Satva-original"
  source: "original"
---

# Revenue recognition (ASC 606 / IFRS 15 basics)

The core principle is the same under both: recognise revenue to depict transfer of promised goods or services in an amount reflecting the consideration expected. Differences exist (collectibility threshold wording, licensing detail, disclosures); note them in the memo. Complex or material contracts need a technical-accounting review.

## Five-step model
1. **Identify the contract:** approved, rights and payment terms identifiable, commercial substance, collection probable (ASC: probable; IFRS: probable). Combine contracts entered at or near the same time with the same customer if negotiated as a package.
2. **Identify performance obligations (POs):** a good/service is distinct if the customer can benefit from it on its own AND it is separately identifiable in the contract. Typical bundles: software licence + implementation + support; device + service plan; product + free shipping (shipping after control transfers can be a fulfilment cost election).
3. **Determine the transaction price:** fixed + variable consideration (discounts, rebates, returns, penalties, usage fees, bonuses) using expected value or most likely amount; constrain so a significant reversal is not probable. Remove sales tax collected for authorities. Adjust for significant financing component if payment timing differs from transfer by more than 1 year (practical expedient to ignore). Non-cash consideration at fair value.
4. **Allocate to POs** on relative standalone selling price (SSP): allocation = SSP of PO / sum of SSPs x transaction price. SSP: observable price first, then adjusted market assessment, expected cost plus margin, or residual (only if highly variable/uncertain). Allocate discounts proportionally unless evidence says it relates to specific POs.
5. **Recognise when/as each PO is satisfied:**
   - **Over time** if (a) customer simultaneously receives and consumes benefit (subscriptions, SaaS, support), (b) the entity's performance creates/enhances an asset the customer controls, or (c) the asset has no alternative use and there is an enforceable right to payment for work to date. Measure progress: input (cost-to-cost, hours) or output (milestones, units). Ratable for stand-ready obligations.
   - **Point in time** otherwise: indicators of control transfer: present right to payment, legal title, physical possession, risks and rewards, customer acceptance.

## Principal vs agent
Principal if the entity controls the good/service before transfer (primary responsibility, inventory risk, pricing discretion): report gross. Agent: report net fee/commission. Marketplaces, travel and reseller models are common judgement calls: document the indicators for each.

## Special topics
- **Contract modifications:** separate contract if distinct additional goods at SSP; otherwise terminate-and-create-new (prospective) or cumulative catch-up if remaining goods are not distinct.
- **Right of return / refunds:** recognise revenue net of expected returns; refund liability and return-asset (ecommerce-inventory-cogs).
- **Licences:** right to use (point in time) vs right to access (over time); sales/usage-based royalties recognised when the later of usage and satisfaction occurs.
- **Costs to obtain a contract:** capitalise incremental costs (commissions) if recovery expected; amortise over the contract term including expected renewals; practical expedient to expense if amortisation period is one year or less.
- **Gift cards/breakage:** liability until redeemed; recognise breakage in proportion to redemption pattern when expected breakage is reliably estimable.
- **Contract assets and liabilities:** contract liability (deferred revenue) when payment is received/due before performance; contract asset when revenue recognised before the right to payment is unconditional; receivable when only time passes.

## Journal patterns
- Annual SaaS invoiced upfront 12,000 on 1 Jan: Dr AR 12,000, Cr Deferred revenue 12,000. Monthly: Dr Deferred revenue 1,000, Cr Revenue 1,000. If cash not yet due and non-cancellable, check whether presenting AR is appropriate (unconditional right).
- Multi-element: allocate price across POs by SSP; recognise implementation over time (input method) and support ratably.
- Percentage of completion: revenue to date = (cost incurred / estimated total cost) x transaction price; prior cumulative revenue deducted for the period amount. Revisit estimates each period; recognise full expected loss immediately on onerous contracts.

## Deferred revenue schedule (build once, roll monthly)
Contract | start | end | billing | total | recognised to date | deferred balance | monthly amount. Roll-forward: opening deferred + billings - revenue recognised = closing; closing ties to the GL. Check: unbilled revenue and deferred revenue should not both be positive for the same contract without explanation.

## Memo template (for each material arrangement)
Contract summary; POs identified and why; transaction price incl. variable consideration; SSP evidence and allocation; timing and method; principal/agent conclusion; entries; open judgements; approver.

## Do not
Do not recognise revenue on invoicing or cash receipt by default; do not skip step 2 for bundled contracts; do not change estimates without a documented catch-up entry; do not conclude on complex judgements without review.

## Output
Per-contract recognition schedule, journals, deferred revenue roll-forward tied to GL, and completed memo for non-routine contracts.
