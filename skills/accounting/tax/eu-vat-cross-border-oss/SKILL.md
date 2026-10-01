---
name: eu-vat-cross-border-oss
description: >-
  Decide VAT treatment for cross-border EU transactions: B2B vs B2C, goods vs services vs digital services, place of supply, reverse charge, intra-EU supplies and acquisitions, the EUR 10,000 distance-sales threshold, OSS (Union, non-Union) and IOSS, VAT-number validation and invoice wording. Use for "do we charge VAT to a German customer", "reverse charge on a EU service", "do we need OSS", "SaaS sold to EU consumers", "VIES check", "EC Sales List". Prepares a position for review; not tax advice.
metadata:
  department: "accounting"
  domain: "tax"
  owner: "satva-coe"
  status: "beta"
  license: "Satva-original"
  source: "original"
---

# EU cross-border VAT and OSS

Scope: the common cross-border cases for an EU-established business or a non-EU seller to EU customers. It produces a documented VAT position per transaction type for an accountant or tax adviser to confirm. Member-State rules differ in detail (rates, invoice wording, filing portals, domestic registration thresholds), so every rate, threshold and deadline below is a prompt to verify at the Member State tax authority or the European Commission's Taxes in Europe Database (TEDB). Never quote a rate from memory.

## Inputs

Supplier and customer countries and VAT status; customer VAT number and VIES result (with date); what is supplied (goods, services, digital service, mixed); where goods start and end their transport; who arranges transport and the incoterm; contract value, invoice and payment dates; any platform or marketplace involved; evidence of customer location.

## Workflow

1. **Classify the customer.** Business (taxable person with a VAT number that validates in VIES on the supply date) or consumer. Record the VIES result and date; a number that fails validation means treat as B2C until fixed. A business customer without a VAT number needs documentary proof of business status.
2. **Classify the supply.** Goods (physical movement), services, or electronically supplied services (software, streaming, downloads, online platforms). Mixed supplies: identify the principal element or whether it is a composite supply; escalate if unclear.
3. **Place of supply (default rules).**
   - B2B services: the customer's country. Supplier invoices without local VAT and the customer self-accounts (reverse charge). Exceptions: services connected with land, admission to events, passenger transport, short-term vehicle hire and restaurant services are taxed where the property, event or service is physically supplied.
   - B2C services: generally the supplier's country, except electronically supplied services (and telecom/broadcasting), where it is the consumer's country.
   - Goods: where transport starts, except distance sales to consumers (destination), installation/assembly (where installed) and imports.
4. **Intra-EU B2B goods.** Supplier invoices 0% only if the customer has a valid VAT number in another Member State quoted on the invoice, the goods physically leave the supplier's Member State, and transport evidence is held. Missing any element means local VAT applies. The customer self-accounts for the acquisition. Report on the EC Sales List and the periodic return per local rules.
5. **B2C goods sold across borders (distance sales).** The EU-wide EUR 10,000 annual threshold covers cross-border B2C goods plus B2C telecom, broadcasting and electronic services combined. Below it the supplier may charge origin VAT; above it, or if the supplier opts out, destination VAT applies. Verify the threshold and any later change before relying on it.
6. **OSS.** Union OSS lets an EU-established business declare destination VAT on B2C distance sales of goods and B2C services in one quarterly return filed in its home Member State, paid in EUR, records kept for 10 years. Non-Union OSS covers non-EU businesses supplying services to EU consumers. IOSS covers B2C imports of low-value consignments (verify the EUR 150 limit) so VAT is collected at sale. Once a scheme is used it applies to all eligible supplies in it. Check the platform deemed-supplier rule: an electronic interface facilitating qualifying sales may be treated as the supplier.
7. **Evidence of customer location (B2C digital).** Collect two non-contradictory pieces (billing address, IP geolocation, bank or card country, SIM country) and keep them. A relaxed evidence rule exists only below the threshold in step 5.
8. **Invoice wording.** B2B reverse charge: no VAT charged, the customer's VAT number and the legal reference (Article 196 of Directive 2006/112/EC or the local equivalent). Intra-EU goods: exemption reference and both VAT numbers. OSS invoices carry the destination rate. Check local mandatory invoice content and any e-invoicing mandate already in force in the Member State.
9. **Triangulation and chains.** Three parties in three Member States with goods moving directly: a simplification may avoid registration in the middle Member State if every condition is met. Call-off or consignment stock, chain transactions and drop-shipments: escalate to a specialist.
10. **Record the position.** For each transaction type: facts, rule applied, evidence held, filing destination. List open questions.

## Failure modes to catch

- Zero-rating intra-EU goods on an unvalidated VAT number or without transport proof.
- Charging origin VAT to consumers after crossing the distance-sales threshold.
- Treating a non-EU B2C digital supply as outside scope: it is taxed where the consumer is.
- Reverse charge applied to supplies whose place of supply is local (events, land, hire).
- A stale customer VAT number: re-validate per transaction or periodically per policy.
- Forgetting the platform deemed-supplier rule, or treating the UK as inside the EU: it is a third country for EU VAT.
- Using a ledger's default tax code without checking the supply.

## Do not

- Do not give a final VAT ruling or file returns; prepare the position for the registered adviser.
- Do not state a threshold, rate or deadline without its source and check date.
- Do not assume one Member State's invoice or reporting rules apply in another.
- Do not ignore pending EU changes (digital reporting and e-invoicing under the VAT in the Digital Age package are phasing in): verify the status for the period.

## Output

A table per transaction type (customer type, supply, place of supply, VAT treatment, evidence, filing), an open-questions list, and the sources checked with dates.
