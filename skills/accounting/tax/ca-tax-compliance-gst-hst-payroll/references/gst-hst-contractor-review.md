<!-- Adapted from AlexTeplovCPA/it-contractors-skills skills/checking-gst-hst/SKILL.md (MIT, Copyright (c) 2026 Alex Teplov). Modified by Satva: frontmatter removed. -->

# Checking GST/HST

Review GST/HST registration, collection, and input tax credit facts for a Canadian IT contractor.

## Core Rules

- Organize and flag GST/HST facts, do not advise on compliance positions.
- Do not determine final registration obligation.
- Do not calculate net tax owing.
- Do not determine final ITC eligibility.
- Do not determine the correct GST/HST rate for any supply.
- Preserve uncertainty where facts are incomplete.
- Do not state that the user is or is not required to register.
- Do not state that the user's GST/HST return is correct.
- Do not state that the user is ready to file.
- Use this phrase where relevant: "That is outside what this workflow covers. It is a question for a CPA before you file."

## Inputs

Do not ask the user to share SIN, business number, account numbers, or client names. Use general descriptions and rounded amounts.

Accept any of:

- output from `identifying-income-sources`
- output from `organizing-t2125-gross-business-income`
- prior year GST/HST return summary
- invoice summaries or client contract descriptions
- expense records for ITC purposes
- user explanation in chat

Minimum useful input:

- some indication of annual business revenue
- description of the type of services provided
- any known GST/HST registration details

Read from the shared input schema where available: `case_id`, `tax_year`, `engagement_mode`, `user_profile`, `facts.business_activity`, `facts.gst_hst`, `documents.gst_hst_records`, `form_context`, `review_state`.

Read from prior skill outputs where available: `identifying-income-sources`, `organizing-t2125-gross-business-income`.

## Workflow

### 1. Confirm GST/HST review is relevant

Check whether the user earns income from a business activity in Canada. If income appears entirely employment income or exempt, note this and return an appropriate status.

### 2. Organize registration facts

Identify:

- whether the user is currently registered for GST/HST
- whether the user has a GST/HST number
- approximate annual revenue across all business income sources
- whether any income may be from zero-rated or exempt supplies

Do not conclude registration obligation. Flag if total revenue appears to approach or exceed the $30,000 small supplier threshold.

### 3. Organize collection facts

Identify:

- whether the user has been collecting GST/HST on invoices
- whether clients are Canadian businesses or consumers
- whether services may be supplied internationally

Note any apparent inconsistency between registration status and collection behavior.

### 4. Organize ITC candidates

Identify expense categories from prior skills that may give rise to input tax credits:

- software and cloud tools
- office supplies
- phone and internet
- professional fees
- meals and entertainment (at applicable rate)
- home office expenses (where applicable)

Do not determine final ITC amounts. Note that ITC eligibility and rate depend on facts not fully reviewed here.

### 5. Assess support strength

Note whether the user has:

- GST/HST returns filed for the period
- records of GST/HST collected
- records of GST/HST paid on purchases

Mark overall support as `sufficient`, `partial`, `weak`, or `none`.

### 6. Flag issues that affect readiness

Flag issues such as:

- revenue level suggests registration may be required but status is unclear
- GST/HST collected without registration
- no GST/HST collected despite apparent obligation
- foreign income or zero-rated supply uncertainty
- ITC documentation incomplete
- filing period or due dates not confirmed

Only flag issues that materially affect readiness.

### 7. Prepare downstream routing

Indicate likely downstream uses:

- `generating-cpa-handoff-summary`
- `generating-missing-items-summary`

Do not run those workflows inside this skill.

## Resource Map

- `../../references/shared-input-schema.md`: read to populate input fields
- `../../references/shared-output-schema.md`: read to format output fields

## Output

Return using the shared output schema. Include:

- `facts_accepted`: usable GST/HST facts the skill relied on
- `mappings_proposed`: GST/HST fact groupings including registration status, collection summary, ITC candidates; use entries such as confirmed, provisional, unclear, needs_manual_review
- `flags`: use `missing_support`, `gst_hst_issue`, `cross_border_issue`, `mapping_uncertain` where applicable
- `open_questions`: only questions needed to resolve meaningful uncertainty; typical useful questions include: Are you registered for GST/HST? Have you been collecting GST/HST on invoices? What was your total business revenue this year?
- `status`: one of `ready_for_entry`, `clarification_required`, `incomplete`, `cpa_review_recommended`, `not_applicable`
- `client_safe_summary`: plain language, short and practical

Also include a GST/HST fact summary grouped into:

- registration and filing facts (status, number if known, filing period)
- collection summary (whether GST/HST was charged, approximate amounts if known)
- ITC candidates (expense categories with potential ITC, support strength)
- open issues

## Status Guidance

- `ready_for_entry`: GST/HST facts are sufficiently organized for CPA handoff or downstream summary
- `clarification_required`: some GST/HST facts are available but registration, collection, or ITC support is incomplete
- `cpa_review_recommended`: file includes material uncertainty about obligation, foreign supplies, or inconsistent treatment
- `incomplete`: key GST/HST facts are missing and review cannot proceed meaningfully
- `not_applicable`: GST/HST review does not appear relevant from the facts provided

Do not use `ready_for_entry` if registration status or collection behavior is unresolved.

## Validation

- Registration status is noted or flagged as unresolved.
- Revenue level is noted in relation to the small supplier threshold.
- ITC candidates are listed by expense category.
- At least one downstream skill is identified in routing.
- `status` is one of the five standard values.
- `client_safe_summary` is present and contains no tax advice.
