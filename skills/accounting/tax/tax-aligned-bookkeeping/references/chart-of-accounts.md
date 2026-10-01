# Tax-Aligned Chart of Accounts Template

Standard chart of accounts for small LLCs/S-Corps mapped to IRS form lines.
Customize account numbers and sub-accounts for your business.

## Assets (1000-1999)

| Code | Account | Notes |
|------|---------|-------|
| 1000 | Business Checking | Primary operating account |
| 1010 | Business Savings | Reserve/savings account |
| 1020 | Petty Cash | Small cash transactions |
| 1100 | Accounts Receivable | Amounts owed by clients |
| 1200 | Inventory | If selling products (COGS tracking) |
| 1300 | Prepaid Expenses | Prepaid insurance, rent, subscriptions |
| 1400 | Security Deposits | Refundable deposits paid |
| 1500 | Equipment | Computers, furniture, tools (>$2,500) |
| 1510 | Vehicles | Business vehicles |
| 1520 | Leasehold Improvements | Improvements to rented space |
| 1550 | Accumulated Depreciation | Contra-asset (negative balance) |
| 1600 | Other Assets | Intangibles, goodwill, etc. |

## Liabilities (2000-2999)

| Code | Account | Notes |
|------|---------|-------|
| 2000 | Accounts Payable | Amounts owed to vendors |
| 2100 | Credit Card Payable | Business credit card balances |
| 2200 | Payroll Liabilities | Withheld taxes, employer taxes owed |
| 2210 | Federal Payroll Tax Payable | Federal income tax, FICA withheld |
| 2220 | State Payroll Tax Payable | IL income tax withheld, SUTA |
| 2300 | Sales Tax Payable | If collecting sales tax |
| 2400 | Short-Term Loans Payable | Line of credit, short-term debt |
| 2500 | Long-Term Loans Payable | Business loans, vehicle loans |
| 2600 | Other Liabilities | Deferred revenue, deposits received |

## Equity (3000-3999)

| Code | Account | Notes |
|------|---------|-------|
| 3000 | Owner's Equity / Member Capital | Opening/accumulated equity |
| 3100 | Owner's Contributions | Cash/assets contributed to business |
| 3200 | Owner's Draws / Distributions | Withdrawals (NOT an expense) |
| 3300 | Retained Earnings | Prior year accumulated profit/loss |

**For S-Corps**: Use Shareholder Distributions (3200) and track basis separately.
**For Partnerships**: Use separate capital accounts per member (3000-A, 3000-B, etc.).

## Revenue / Income (4000-4999)

| Code | Account | Notes |
|------|---------|-------|
| 4000 | Service Revenue | Primary service income |
| 4100 | Product Sales | Revenue from product sales |
| 4200 | Returns & Allowances | Refunds, credits issued (contra-revenue) |
| 4300 | Other Income | Interest income, miscellaneous income |
| 4400 | Reimbursed Expenses | Client reimbursements (if tracked separately) |

## Cost of Goods Sold (5000-5099)

| Code | Account | Schedule C Line | Notes |
|------|---------|----------------|-------|
| 5000 | Cost of Goods Sold | Part III | Direct materials and labor for products |
| 5010 | Materials / Supplies (COGS) | Part III | Raw materials |
| 5020 | Direct Labor (COGS) | Part III | Labor directly tied to production |
| 5030 | Subcontractor (COGS) | Part III | Outsourced production work |

## Expenses (5100-8999) — Mapped to Schedule C Lines

### Schedule C Part II — Standard Expense Lines

| Code | Account | Sched C Line | Form 1065/1120-S | What Maps Here |
|------|---------|-------------|-----------------|----------------|
| 5100 | Advertising | Line 8 | Deductions | Google/Meta ads, business cards, website, SEO, promotional materials |
| 5200 | Car & Truck Expenses | Line 9 | Deductions | Mileage OR actual vehicle expenses (not both) |
| 5300 | Commissions & Fees | Line 10 | Deductions | Payment processor fees (Stripe, PayPal), referral fees, platform fees |
| 5400 | Contract Labor | Line 11 | Deductions | 1099-NEC payments to freelancers/contractors ($600+ requires 1099) |
| 5500 | Depletion | Line 12 | Deductions | Natural resources only (rare) |
| 5600 | Depreciation | Line 13 | Form 4562 | Assets >$2,500 capitalized; Section 179 or bonus depreciation |
| 5700 | Employee Benefits | Line 14 | Deductions | Health insurance for employees (NOT owner), retirement for employees |
| 5800 | Insurance (non-health) | Line 15 | Deductions | General liability, E&O, professional liability, property, cyber |
| 5900 | Mortgage Interest | Line 16a | Deductions | Interest on business property mortgage |
| 5910 | Other Interest | Line 16b | Deductions | Business loan interest, credit card interest, LOC interest |
| 6000 | Legal & Professional | Line 17 | Deductions | Attorney, CPA, bookkeeper, tax prep (business portion) |
| 6100 | Office Expenses | Line 18 | Deductions | Office supplies, postage, printing, small software (<$2,500) |
| 6200 | Pension/Profit-Sharing | Line 19 | Deductions | SEP-IRA, SIMPLE, Solo 401(k) employer contributions |
| 6300 | Rent (Equipment) | Line 20a | Deductions | Equipment leases, vehicle leases |
| 6400 | Rent (Other Property) | Line 20b | Deductions | Office/warehouse rent, coworking space |
| 6500 | Repairs & Maintenance | Line 22 | Deductions | Equipment repairs, building maintenance |
| 6600 | Supplies | Line 22 | Deductions | Materials consumed in business (distinct from inventory) |
| 6700 | Taxes & Licenses | Line 23 | Deductions | Business licenses, registration, employer payroll taxes, IL replacement tax |
| 6800 | Travel | Line 24a | Deductions | Airfare, hotel, ground transport for business travel |
| 6900 | Meals (50%) | Line 24b | Deductions | Business meals — 50% deductible. Document: who, purpose, where, when |
| 7000 | Utilities | Line 25 (Other) | Deductions | Electric, gas, water, trash (for business location) |
| 7100 | Wages | Line 26 | Deductions | Employee wages (W-2 wages paid) |

### Other Expenses (Schedule C Line 27 / Other Deductions)

| Code | Account | What Maps Here |
|------|---------|----------------|
| 7200 | Bank & Merchant Fees | Bank service charges, wire fees, merchant account fees |
| 7300 | Software & Subscriptions | SaaS tools, cloud services, domain names, hosting |
| 7400 | Education & Training | Courses, conferences, books, certifications (business-related) |
| 7500 | Dues & Memberships | Professional associations, trade organizations |
| 7600 | Telephone & Internet | Business phone, internet (business % if shared with home) |
| 7700 | Shipping & Delivery | Postage, courier, freight costs |
| 7800 | Cleaning & Janitorial | Office cleaning services |
| 7900 | Security | Alarm systems, security services |

### Home Office (Schedule C Line 30 / Form 8829)

| Code | Account | Notes |
|------|---------|-------|
| 8000 | Home Office Expense | Simplified method ($5/sq ft, max $1,500) OR actual via Form 8829 |
| 8010 | Home Mortgage Interest (Office %) | Actual method — business % of mortgage interest |
| 8020 | Home Property Tax (Office %) | Actual method — business % of property taxes |
| 8030 | Home Utilities (Office %) | Actual method — business % of utilities |
| 8040 | Home Insurance (Office %) | Actual method — business % of homeowner's insurance |
| 8050 | Home Repairs (Office %) | Actual method — business % of general home repairs |
| 8060 | Home Depreciation (Office %) | Actual method — depreciation of home (39 years, business %) |

### Special / Suspense

| Code | Account | Notes |
|------|---------|-------|
| 6999 | Ask My Accountant | Suspense account for uncertain categorizations — clear quarterly |
| 9000 | Owner's Health Insurance | Self-employed health insurance (deducted on 1040, not Sched C) |
| 9100 | Owner's Retirement | Owner's retirement contributions (deducted on 1040 for sole props) |

## Best Practices

1. **40-60 accounts total** is sufficient for most LLCs — avoid over-creating
2. **Use sub-accounts** for detail (e.g., 5100.1 Google Ads, 5100.2 Meta Ads) that roll up to main category
3. **Every expense account must map** to a specific IRS form line
4. **Separate personal and business** — never mix in the same accounts
5. **Clear the suspense account (6999)** every quarter
6. **Consistent naming** — use the IRS terminology for main categories
7. **Track owner transactions through equity** — draws and contributions are NOT revenue/expenses
