<!-- Adapted from Receiptor-AI/bookkeeping-skills skills/expense-categorization (MIT, Copyright (c) 2026 Receiptor AI). Modified by Satva: tax-form mapping removed, generalised to any jurisdiction. -->

# Vendor, line-item and amount signals; split worked example

## Signal order
1. **Vendor name** carries most categorisation for known vendors (ad platforms, fuel, ride-hailing, freelancer marketplaces, telecoms, cloud hosting, SaaS tools, payment processors, accounting software).
2. **Line items** when the vendor is ambiguous (general retailers, marketplaces, electronics vendors). Code each line item separately; a mixed order is split.
3. **Amount pattern**: identical recurring monthly charge suggests a subscription; round-number transfers to individuals suggest contractors; small charges at restaurants suggest meals.
4. **Learned corrections**: a user-confirmed mapping overrides default logic from then on, and is stored as a rule with an owner and a date.

## Ambiguous vendors need line items or a question
- Big retailers and marketplaces: office supplies, equipment, software, books, inventory or personal. Without line items, flag for review.
- Device makers: price separates hardware (capital) from apps and subscriptions.
- Wallet and processor names (PayPal, Stripe, Square): the descriptor often names the underlying seller; look it up. Processor fees are separate from the purchase. A bare processor name goes to review.

## Split worked example
One 347.82 marketplace order: monitor stand 89.99 (equipment), printer paper 42.99 (office supplies), textbook 54.95 (training), HDMI cables 19.89 (equipment), break-room coffee 34.00 (staff amenities), personal items 106.00 (owner drawings or receivable, never expense). Each line gets its own account, the categorised amounts sum to the total, and personal items are excluded from the business expense lines.

## Common mistakes
- Software in office supplies: office supplies are physical consumables; software is its own account. Benchmarks flag an inflated "office supplies".
- Mixing travel and meals: the hotel and the dinner on the trip have different tax treatment.
- Owner health insurance and other owner benefits in business expenses: they are owner items.
- Expensing capital items above the capitalisation threshold.
- Deducting fines and penalties.
- Treating client-reimbursed expenses as pure deductions: the reimbursement is income and the two net out; record both.

## Jurisdiction
Category-to-tax-line mapping is jurisdiction-specific (US federal forms, UK self assessment, Canadian T2125, EU VAT, Australian BAS and so on). Ask the jurisdiction before applying tax lines, track input tax rate per transaction where VAT or GST applies, and keep unknown-jurisdiction work to neutral normalisation and review queues.
