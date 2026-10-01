---
name: customer-credit-control
description: >-
  Set and operate customer credit control: credit assessment at onboarding, credit limits and terms, order and shipment holds, limit-breach and overdue triggers, credit insurance and security, review cycles, and the escalation path between sales, credit control and finance. Use for "set a credit limit", "new customer credit check", "should we ship to this customer", "customer over limit", "put account on hold", "credit policy", "payment terms review", "credit insurance", "stop supply". Preventive companion to ar-collections-dunning, which handles accounts that are already late.
metadata:
  department: "accounting"
  domain: "payables-receivables"
  owner: "satva-coe"
  status: "beta"
  license: "Satva-original"
  source: "original"
---

# Customer credit control

Collections chases debt that exists; credit control decides how much debt to create. A sale is only revenue when it turns into cash, so the credit decision belongs before the order, with the same rigour as the invoice.

## 1. Credit policy (write it once, approve it, apply it consistently)
Define: standard terms by customer segment (for example net 30, net 14, prepay for new or high-risk), who may grant exceptions and up to what amount, limit-setting method, review frequency, hold and release rules, late-fee terms stated on every quote and invoice, and the escalation path. Terms are agreed in the contract or order acceptance, not after the invoice is late. A policy applied selectively is lost the first time a customer argues.

## 2. Assess a new customer
1. Identify: legal entity name, registration number, trading address, ownership, who signs, who pays (the payables contact), billing currency, tax identifiers. Confirm the entity exists and is active through a public registry.
2. Evidence of capacity, proportionate to the exposure: trade references (at least two suppliers, asked about terms, limit and payment behaviour), recent financial statements for larger limits, a credit bureau or agency report, bank reference where available, news and litigation search, and for existing relationships the payment history.
3. Red flags: very new entity asking for large credit, mismatch of names across order, bank account and registry, a request to ship to a different address or pay through a third party, pressure to skip checks, accounts filed late or with going-concern language, a history of insolvency of connected directors.
4. Decide: prepay or deposit, a limited trial limit, credit with security (parent guarantee, bank guarantee, letter of credit, credit insurance) or decline. Record the basis and approver.

## 3. Set the limit
A limit is a maximum exposure including invoiced balance, unbilled work and open orders, not only the aged balance. Start from the lowest of: what the evidence supports (for example a small percentage of net worth or one to two months of expected sales), what the insurer covers, and what the business can bear to lose without damaging cash. Split limits by entity or currency where exposure differs. Large limits and any exception above delegated authority are approved by a second person.

## 4. Triggers and holds

| Trigger | Action |
|---|---|
| Order would take exposure over the limit | Hold the order; sales and credit control decide: part-ship, prepay the excess, raise the limit with evidence, or decline |
| Any invoice over the overdue threshold (for example 30 days past due) | Credit-hold warning to sales; no new terms increase |
| Overdue past the hold threshold (for example 45 to 60 days), or a broken payment promise | Stop supply or move to cash on delivery per policy, with notice to the customer and sales |
| Bounced payment, insolvency signal, or a dispute not progressing | Immediate review; consider security and legal advice |
| Customer paid and cash applied | Release the hold the same day; holds that outlive the cause damage trade |

A hold is released by credit control, not by the salesperson who wants the order shipped. Document every override with approver and reason. Contract and law may restrict stopping supply (continuing services, regulated sectors, notice periods); check before holding.

## 5. Review cycle
Review limits at least annually, and sooner on a trigger: payment behaviour worsens (days beyond terms rising across three months), a large order, adverse news, change of ownership, or a covenant breach by the customer. Use `ar-aging-analysis` for payment behaviour and concentration. Keep a watch list of customers to review monthly and a list of accounts on hold.

## 6. Security and insurance
Credit insurance transfers loss above an excess, but cover is conditional on insurer limits, notification of overdues within the policy period and clean documentation: manage the policy's overdue-notification deadlines like a legal calendar. Guarantees and letters of credit must be checked for validity, amount, expiry and presentation conditions before shipping. Retention-of-title clauses must be in the signed terms to help in an insolvency.

## 7. Governance
Sales may not set limits or lift holds alone. Credit control reports monthly: exposure versus limits, over-limit accounts, accounts on hold with reason, overrides, and bad-debt and provision movements (`bad-debt-and-credit-loss-allowance`). Customer data used in credit files is personal or confidential business data: collect only what is needed, store it securely, and respect privacy and consumer-credit rules in the jurisdiction.

## Output
Credit assessment memo (customer, evidence, red flags, decision, limit, terms, security, approver), limit register, hold and release log, over-limit and watch-list report, and a review calendar.

## Do not
- Extend credit because the salesperson vouches for the customer.
- Set a limit from the aged balance alone.
- Let holds linger after payment, or release them on a promise alone.
- Threaten stop-supply or legal steps the business will not take.
- Skip identity verification for a large first order.
