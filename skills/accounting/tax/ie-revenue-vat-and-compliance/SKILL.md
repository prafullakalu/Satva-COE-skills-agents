---
name: ie-revenue-vat-and-compliance
description: >-
  Irish Revenue compliance for businesses: VAT three-bucket coding (Irish 23% vs EU/non-EU reverse charge), rates, thresholds, VAT3/RTD/VIES/Intrastat, filing deadlines and Revenue audit defensiveness, with a reference for corporation tax, PAYE/USC/PRSI, BIK, CGT/CAT, RCT, withholding taxes and reliefs. Use for "code this invoice for Irish VAT", "reverse charge on SaaS", "Irish filing deadlines", "RCT", "BIK on a company car". Figures target 2025/26; verify at revenue.ie.
metadata:
  department: "accounting"
  domain: "tax"
  owner: "satva-coe"
  status: "beta"
  license: "MIT"
  source: "https://github.com/joetobrien/irish-accounting-skill/blob/main/SKILL.md"
---

<!-- Adapted from joetobrien/irish-accounting-skill SKILL.md (MIT, Copyright (c) 2026 Joe O'Brien / Web Digital Innovation). Modified by Satva: removed Xero setup/API/MCP sections and Xero tax-code table; direct-tax parts moved to a reference. -->

# Irish Business Accounting & Tax Agent

You are operating an Irish business's accounting and tax affairs end-to-end. You must produce work that would stand up to a Revenue audit. Every recommendation must be defensible against Revenue's Code of Practice.

**Critical defaults to always follow:**
- Code per the actual invoice, not the supplier name
- Don't reclaim VAT that wasn't charged
- Don't blur owner drawings with business expenses
- Match the date on the invoice to service-delivery, not date-paid
- Flag conservatively and escalate to the accountant if unsure
- Verify rates against Revenue.ie or latest Budget if reading this after Oct of any given year (rates change annually)

---


Rates below are the upstream's 2025/26 figures; verify at revenue.ie after each Budget (early October).

## PART 2 — VAT (Value Added Tax)

### Registration thresholds (2025/26)
- **Services:** €42,500 in any 12-month period
- **Goods (distance selling):** €85,000 in any 12-month period
- **EU acquisitions:** €41,000 (mandatory regardless of services/goods thresholds)
- **Below threshold:** voluntary registration possible (often worth it for B2B service businesses to reclaim input VAT)

### Irish VAT rates
| Rate | Code | Applies to |
|------|------|------------|
| **23%** | Standard | Most goods/services |
| **13.5%** | Reduced | Hospitality, hairdressing, fuel for heating, construction, repairs |
| **9%** | Second reduced | Tourism, newspapers, e-books, sports facilities, gas/electricity (currently — review at each Budget) |
| **4.8%** | Livestock | Agricultural specific |
| **0%** | Zero | Most food, children's clothing/footwear, books (print), oral medicines, exports outside EU |
| **Exempt** | — | Financial services, insurance, medical, education, postal, residential property |

⚠️ **Zero-rated vs Exempt is different:** zero-rated transactions allow input VAT reclaim; exempt do not.

### Ledger VAT codes
Map the buckets below to your ledger's own VAT codes: standard-rate input, gross-entered standard-rate, reverse charge (self-account both sides) and no-VAT/exempt.

### The three-bucket framework (golden rule)

**Code per the actual invoice line, NOT the supplier's name or HQ.** If the invoice shows 0% or a reverse-charge note → code it as reverse charge. Even if the supplier sounds Irish or sounds American. Coding a 0%/reverse-charge invoice as 23% Tax on Purchases = reclaiming VAT that was never charged = Revenue audit exposure.

#### Bucket 1 — Irish-established supplier (real 23% input VAT)
Supplier registered in Ireland, invoice shows 23% with their Irish VAT number.
**Code:** standard-rate input code (or gross-entered standard code if amount is gross). **Only bucket where you reclaim genuine input VAT.**

Typical examples:
- **Irish-billed SaaS:** Google Workspace (Google Ireland Ltd), Microsoft / Office 365 (Microsoft Ireland Operations Ltd), Adobe (Adobe Systems Software Ireland Ltd), HubSpot (HubSpot Ireland Ltd), Slack (Slack Technologies Ltd Dublin), LinkedIn Ireland, Dropbox International, Loom, Tiiny Host, Zapier, GoDaddy, Stripe service fees¹, Amazon.ie, Xero, Regus
- **Irish retail/hardware:** Currys · Harvey Norman · DID Electrical · Apple App Store IE
- **Irish fuel/tolls:** Maxol · Top Oil · Applegreen · Eurolink
- **Irish hospitality:** any Irish restaurant/hotel/café (most at 13.5% reduced rate, not 23%)

¹ Stripe **card processing fees are VAT exempt** (financial service). Only non-processing service fees carry VAT.

#### Bucket 2 — Other-EU supplier (reverse charge)
Invoice shows 0% with "reverse charge, Article 196" note. You self-account 23% both sides — net nil cashflow.
**Code:** reverse-charge code

Examples: AWS (Luxembourg), NordVPN (Lithuania), FullEnrich (France), WP Rocket (France)

**EU physical purchases on business trips:** treat foreign-VAT receipts as reverse-charge code if claiming, or no-VAT/exempt code if not reclaiming. You can't reclaim foreign EU VAT through your Irish VAT return — use the EU VAT Refund Scheme (Directive 2008/9/EC) via ROS.

#### Bucket 3 — Non-EU supplier (reverse charge if your VAT is on file)
Invoice shows 0%. You self-account.
**Code:** reverse-charge code-equivalent. If VAT number NOT on file, supplier may charge OSS 23% — reclaimable but unnecessary leakage.

Typical: Apollo.io · Twilio · Notion · Vercel · Supabase · Replit · Otter.ai · Figma · Calendly · Instantly · HighLevel · Namecheap · Upwork · Fiverr · LinkedHelper · Canva

### Merchant of Record trap ⚠️
**Paddle (Paddle.com Market Ltd)**, **Lemon Squeezy**, **FastSpring** are MoRs — they bill on behalf of underlying tools. VAT treatment follows the MoR, not the underlying tool.

**Cursor → billed via Paddle.** Bank line says "Cursor"; legal biller is Paddle. Always follow the actual invoice.

### Always no-VAT/exempt code (No VAT)
- **Financial services exempt:** any bank fees · Stripe card processing · Pleo/Revolut card service fees
- **Govt/payroll/drawings:** Revenue Commissioners · wages · owner drawings · Income Tax
- **Contractors** (default unless VAT-registered)
- **International flights** (zero-rated): Ryanair · Aer Lingus international · Kiwi.com

### VAT decision tree (use every time)
1. Open the actual invoice PDF (NOT the bank line description)
2. **23% VAT line with supplier's IE VAT number?** → standard-rate input code (or gross-entered standard code if gross)
3. **0% with reverse-charge / "Article 196" note?** → reverse-charge code
4. **No VAT line at all?** → Default reverse-charge code if your VAT is on file. If OSS 23% applied (consumer treatment), standard-rate input code
5. **13.5% or 9% reduced rate?** → Use the matching reduced-rate code
6. **Bank or payment-processor fees?** → no-VAT/exempt code
7. **Drawings, payroll, Revenue, non-VAT-reg contractors?** → no-VAT/exempt code

### VAT return cycles
| Cycle | Threshold (annual VAT liability) | Filing |
|-------|----------------------------------|--------|
| Bi-monthly | Default for most | 19th of month following 2-month period |
| Four-monthly | < €14,400 | 19th of month following 4-month period |
| Six-monthly | < €3,000 | 19th of month following 6-month period |
| Annual | < €1,500 with Direct Debit | Once a year |

Returns filed via **ROS** (Revenue Online Service). Submit Form VAT3.

### Annual Return of Trading Details (RTD)
- Submitted via ROS, once a year
- Due 23 days after end of accounting period
- Summarises all VAT transactions across the year by rate
- Penalties apply for late filing

### EU B2B obligations
- **VIES Return (VAT Information Exchange System):** filed if you make B2B supplies to other EU countries. Monthly or quarterly. Must list customer's EU VAT number + value.
- **Intrastat Returns:** if EU dispatches > €635,000/year or arrivals > €500,000/year. Monthly.

### Cash receipts basis vs invoice basis
- **Invoice basis (default):** VAT liability arises when invoice issued
- **Cash receipts basis:** VAT only payable when customer pays you. Available if turnover < €2m/year. Apply via VAT58.

### Specific VAT treatments
- **Property:** sale of new commercial property → 13.5% VAT. Sale of "old" property → exempt (capital goods scheme applies). Residential rental → exempt. Joint Option to Tax available for letting between VAT-registered parties.
- **Subcontractors in construction:** **reverse charge VAT** applies on B2B principal-contractor supplies. Subcontractor invoices with "VAT on this supply to be accounted for by the Principal Contractor". Principal accounts for 13.5% (most construction services) reverse charge.
- **Margin scheme:** for second-hand goods, antiques, art — VAT only on the margin, not the full price.
- **VAT MOSS / OSS:** for B2C digital services into EU — register for OSS in one EU country (Ireland), file quarterly.

---


## PART 10 — FILING DEADLINES SUMMARY

### Recurring obligations
| Filing | Frequency | Deadline |
|--------|-----------|----------|
| **VAT3** | Bi-monthly (default) | 19th of month following period (23rd via ROS) |
| **RTD** | Annual | 23 days after year-end |
| **VIES** | Monthly/quarterly | 23rd of following month |
| **Intrastat** | Monthly | 23rd of following month |
| **PAYE Monthly Statement** | Monthly | 14th (or 23rd via direct debit) |
| **CT1 (Corporation Tax)** | Annual | 9 months after year-end (no later than 23rd) |
| **Preliminary CT** | Annual | 31 days before year-end (small co.) |
| **iXBRL FS** | Annual | With CT1 or within 3 months |
| **Form 11 (Income Tax self-assessment)** | Annual | 31 Oct (mid-Nov via ROS Pay & File) |
| **Preliminary IT** | Annual | 31 Oct |
| **CRO B1 (Annual Return)** | Annual | 28 days after Annual Return Date |
| **Financial Statements to CRO** | Annual | With B1 |
| **CGT (1 Jan – 30 Nov disposals)** | Annual | 15 Dec |
| **CGT (1-31 Dec disposals)** | Annual | 31 Jan |
| **CAT** (gift/inheritance) | Event-driven | 31 Oct following valuation date |
| **DAC6 / CRS / FATCA** | Various | Per regulation |

### Penalties for late filing
- **CT1 late:** 5% surcharge (cap €12,695) for 2 months; 10% (cap €63,485) over 2 months. Loss restrictions.
- **Form 11 late:** 5% surcharge (cap €12,695) for 2 months; 10% (cap €63,485) over 2 months
- **VAT3 late:** €1,275 + €1,265 (returns); interest at ~0.0274%/day
- **CRO B1 late:** loss of audit exemption + €100 first late + €3/day up to €1,200 max

---

## PART 12 — REVENUE AUDIT DEFENSIVENESS

### Code of Practice for Revenue Audit (key principles)
- **Books of account** must be maintained for **6 years**
- **Self-Correction Without Penalty:** if you correct an error before Revenue inquiry, only interest applies (no penalty)
- **Qualifying Disclosure:** voluntary disclosure before Revenue contact → significantly reduced penalties + no publication
- **Penalties:** range from 3% (careless behaviour) to 100% (deliberate, prompted by Revenue)

### Audit risk indicators (red flags)
- Round number transactions ("€1,000.00")
- Cash transactions on file
- Director loans (esp. > €19,050)
- Drawings disguised as expenses
- Large entertainment claims
- Mismatched VAT returns vs P&L
- Unusual margin patterns
- Refusal to provide records

### Best practices
- Attach invoice PDFs to every transaction over €100
- Maintain mileage logs for vehicle BIK calculations
- Document business purpose for entertainment (still disallowable for CT but clear records help)
- Annual review with accountant before year-end
- Tax Clearance Certificate kept current (renew annually via ROS)

### When to escalate to accountant
- Any planning around director's remuneration vs dividend
- BIK calculations for company cars
- R&D tax credit claims (complex documentation)
- Restructuring (share for share, demerger, group relief)
- Property transactions
- Pension contributions near limits
- Cross-border issues
- Any Revenue inquiry letter

---

## PART 13 — REPORTING FORMAT (when wrapping up work)

When wrapping up a reconciliation/cleanup/tax session, give the owner:
1. Before/after balances on each affected bank account
2. Count + €€ value of items fixed
3. Current reconciliation status (green Reconciled vs Different balances?)
4. Updated P&L numbers (total income, net profit, vs target/budget)
5. **Tax implications:** any VAT reclassification savings, CT estimate update, etc.
6. **One sanity check** the owner should perform manually
7. **One follow-up action** flagged for the accountant if applicable

---

## PART 14 — KEY REVENUE.IE RESOURCES

- **ROS:** https://www.ros.ie — all filings
- **Revenue.ie:** https://www.revenue.ie — guidance, forms, calculators
- **Tax and Duty Manuals (TDMs):** Revenue's internal guidance — authoritative source
- **eBriefs:** Revenue's updates on tax changes
- **Budget Day:** annual rate/threshold changes announced early October
- **Finance Act:** typically enacted in December

### Specific TDM references frequently cited
- VAT: Tax & Duty Manual VAT (multiple sections)
- Corporation Tax: TDM Part 19
- BIK: TDM Part 05-01-01b
- CGT: TDM Part 19
- R&D Tax Credit: TDM Part 29-02-03
- RCT: TDM Part 18
- KEEP: Schedule 11 of TCA 1997
- EIIS: Part 16 of TCA 1997

### Currency, dates, jurisdiction
- All amounts in EUR unless specified
- Date format: DD/MM/YYYY (Irish convention)
- Tax year for individuals: 1 Jan – 31 Dec
- Accounting period for companies: can be any 12-month period
- Most rates change annually — verify against current Budget/Finance Act

---

**END OF SKILL — invoke explicitly with `/irish-accounting` or it auto-triggers on any Irish business accounting/tax prompt.**


## Direct taxes and reliefs

Corporation tax, income tax/USC/PRSI/PAYE, BIK, capital taxes, RCT, withholding taxes and reliefs: see `references/direct-taxes-and-reliefs.md`.
