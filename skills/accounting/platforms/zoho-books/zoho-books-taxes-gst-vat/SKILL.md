---
name: zoho-books-taxes-gst-vat
description: >-
  Getting indirect tax right in Zoho Books: choosing and creating tax rates, GST (India) treatment and place of supply, UK/EU/GCC VAT treatment, reverse charge, tax-inclusive pricing, TDS, and sanity-checking tax on invoices and expenses before filing. Use when asked "which tax should this invoice carry", "set up GST in Zoho", "VAT treatment for this customer", "why is tax wrong on this invoice", "create a tax rate", or "check our tax before the return".
metadata:
  department: "accounting"
  domain: "tax"
  platform: "zoho-books"
  owner: "satva-coe"
  status: "beta"
  license: "Satva-original"
  source: "original"
---

# Zoho Books: taxes, GST and VAT

Prerequisite: `zoho-books-operating-rules`. Tools: `get_organization`, `list_taxes`, `get_tax`, `create_tax`, `get_contact`, `list_contacts`, `list_invoices`, `list_expenses`, `create_invoice`.
This skill gives mechanics, not tax advice. For filing positions, rates that changed this year, or edge cases, the user's tax adviser decides; say so when it matters.

## 1. Establish the regime

`get_organization`: country, tax registration (GSTIN / VAT number), edition. The fields the API accepts depend on the edition. India GST fields sent to a UK org (or the reverse) are ignored or rejected. If the org is not tax-registered, tax lines must be zero; do not add rates.

## 2. Choosing a tax on a line

1. `list_taxes`: use existing taxes. Match on name, percentage and type. Never create a near-duplicate "VAT 20" next to "VAT 20%".
2. A tax on a line is set by `tax_id`. Order of decision: customer treatment, then item/product type, then place of supply, then rate.
3. Create a tax only when none fits and the user confirms: `create_tax` needs `tax_name`, `tax_percentage`, `tax_type` (`tax` or `compound_tax`). Set country-specific fields (below). Warning: the update flags (`update_draft_invoice`, `update_recurring_invoice`, `update_subscription`, ...) change existing documents; leave them false unless asked.
4. A rate change going forward: create a new tax and retire the old one. Never edit a rate that posted history uses.

## 3. India (GST)

- Contact fields: `gst_treatment` (`business_gst` registered, `business_none` unregistered, `consumer`, `overseas`) and `gst_no` (15 characters).
- `place_of_supply` (state code) decides the split: supplier state equals place of supply gives CGST + SGST; different state gives IGST. `tax_specific_type` on a tax is `cgst`, `sgst`, `igst`, `nil` or `cess`. Use Zoho tax groups for intra-state so both halves post.
- Goods and services carry `hsn_or_sac` on lines. Missing HSN/SAC is a filing risk above the turnover threshold.
- Exports and SEZ: `overseas` treatment, zero rated; with or without LUT is a business decision, ask.
- Shipping-party fields (`shipping_gst_no`, `shipping_legal_name`) matter only for e-invoice and e-way bill.
- TDS: `tds_tax_id` on lines for withholding; tax withheld by the customer at receipt is applied through `tax_amount_withheld` in `create_customer_payment`.

## 4. UK, EU, GCC (VAT)

- Invoice/contact `tax_treatment` or `vat_treatment` carries registration status and location (UK: `uk`, `eu_vat_registered`, `overseas`; GCC: `vat_registered`, `gcc_vat_registered`, `non_gcc`, and others). The edition decides the allowed set.
- Reverse charge: `is_reverse_charge_applied` on sales; expense lines use `reverse_charge_vat_id` / `acquisition_vat_id`. A reverse-charge purchase posts both input and output VAT: net zero cash, but both return boxes must show it.
- GCC: `place_of_supply` is an emirate or country code; `tax_treatment_code` explains out-of-scope lines.
- Zero-rated, exempt and out-of-scope are three different return lines. Do not use "0%" for all three.

## 4b. US sales tax

Zoho can use Avalara fields (`avatax_tax_code`, `avatax_use_code`, `avatax_exempt_no`) or tax authorities (`tax_authority_id`). Nexus is a legal question: do not switch collection on or off on your own authority.

## 5. Inclusive vs exclusive

`is_inclusive_tax=true` means the rate already contains tax and the engine backs it out. Mixing both across lines on one invoice is where totals drift by a few cents. Quote the final total from `get_invoice`, not from your own arithmetic. If totals differ by one minor unit, check whether the org rounds tax per line or per document before assuming a bug.

## 6. Pre-return sanity pass

For the period (`date_start`/`date_end`), page through `list_invoices` and `list_expenses`:

1. Tax lines present on every taxable sale; zero-tax lines have a reason (exempt, export, unregistered customer).
2. Customers with a GST/VAT number on file but a not-registered treatment (or the reverse).
3. Outliers: effective tax rate (tax / net) per invoice far from the nominal rate.
4. Total output tax versus the tax liability account in `list_chart_of_accounts` (`showbalance=true`); explain differences (manual journals, credit notes, cash-basis timing).
5. Drafts do not post; list them separately.

No return or report tool exists in the connector: hand the figures over for filing in the UI.

## Do not

- Guess a customer's registration status; ask for the number and treatment.
- Edit tax on invoices in a filed period; propose an adjustment in the current period instead.
- Create taxes with the update flags on unless asked.

## Output

Per question: the tax to use (name, `tax_id`, rate), the reason (treatment + place of supply), and any field the user must supply. For checks: a table of exceptions with invoice number, issue and suggested fix.
