"""Plain-accounting-English layer. Pure functions; no jargon reaches the accountant.
Steps are for the HUMAN to do in QuickBooks Online -- this skill never writes to QBO/Linnworks."""

STATUS_PLAIN = {
    "MAPPED": {"label": "Matched", "urgency": "low",
               "sentence": "This is set up correctly in QuickBooks."},
    "UNMAPPED": {"label": "Missing in QuickBooks", "urgency": "high",
                 "sentence": "We could not find anything in QuickBooks to match this."},
    "AMBIGUOUS": {"label": "Needs your choice", "urgency": "medium",
                  "sentence": "More than one QuickBooks entry could fit, so you need to pick the right one."},
    "INVALID": {"label": "Wrong kind of account", "urgency": "high",
                "sentence": "This points to a QuickBooks account of the wrong type, so it will post to the wrong place."},
    "ORPHANED": {"label": "Not used by Linnworks", "urgency": "low",
                 "sentence": "This exists in QuickBooks but nothing in Linnworks feeds it."},
    "INACTIVE": {"label": "Account switched off", "urgency": "high",
                 "sentence": "This points to a QuickBooks entry that is switched off, so nothing can post to it."},
    "UNVERIFIED": {"label": "Please confirm", "urgency": "medium",
                   "sentence": "We found a product with a similar name but couldn't confirm it's the same one."},
    "STRUCTURAL_DATA_GAP": {"label": "Not in Linnworks", "urgency": "high",
                            "sentence": "Linnworks does not hold this information, so it has to come from another source such as the marketplace payout statement."},
    "exact_name_sku_differs": {"label": "Same name, different code", "urgency": "medium",
                               "sentence": "The product name matches but the product code is different in the two systems."},
    "near_sku_match": {"label": "Almost the same code", "urgency": "medium",
                       "sentence": "A product code is very close to one in QuickBooks, possibly a typo."},
}
_URG = {"high": 0, "medium": 1, "low": 2}
_SHOW_TARGET = ("UNVERIFIED", "AMBIGUOUS", "INVALID", "INACTIVE", "MAPPED")


def plain_reason(row):
    """One plain sentence for a MappingResult.to_row()-style dict."""
    info = STATUS_PLAIN.get(row.get("status"), {"sentence": "This needs a quick look."})
    src, tgt = row.get("linnworks_source"), row.get("qbo_target")
    s = f"{src}: " if src else ""
    s += info["sentence"]
    if tgt and row.get("status") in _SHOW_TARGET:
        s += f" (QuickBooks entry: {tgt})"
    return s


def fix_steps(kind, **ctx):
    """Numbered click-path steps in QuickBooks Online wording. Unknown kind -> ValueError.
    ctx keys used: name, sku (product code), qty, current_qty, channel, account_type, detail_type."""
    g = lambda k, d="": ctx.get(k) or d
    channel = g("channel", "this channel")
    steps = {
        "missing_item": [
            "Go to Sales > Products and services.",
            "Click New, then choose Inventory.",
            f"Type the Name: {g('name', '(product name)')} and the Product code: {g('sku', '(product code)')}.",
            f"Set Initial quantity on hand to {g('qty', '(quantity)')} and As of date to the date you are starting from.",
            "Choose the Income, Inventory asset and Cost of goods sold accounts, then click Save and close.",
        ],
        "missing_account": [
            "Go to Settings (gear icon) > Chart of accounts.",
            "Click New.",
            f"Account type: {g('account_type', 'Income')}. Detail type: {g('detail_type', 'Sales of Product Income')}.",
            f"Name: {g('name', channel + ' Sales')}.",
            "Click Save and close.",
            f"Tell whoever runs the sync that {channel} should post to the new account.",
        ],
        "inactive_account": [
            "Go to Settings (gear icon) > Chart of accounts.",
            "Tick 'Include inactive' (gear icon above the table) so switched-off accounts show.",
            f"Find {g('name', 'the account')}, open the Action menu on its row and click Make active.",
        ],
        "item_mismatch": [
            "Go to Sales > Products and services.",
            f"Find {g('name', 'the product')} and click Edit.",
            f"Change the Name or Product code so both systems show the same value: {g('sku', '(product code from Linnworks)')}.",
            "Click Save and close.",
        ],
        "quantity_mismatch": [
            "First check in Linnworks that the quantity is not added up across several warehouses. Compare with the one warehouse QuickBooks should track.",
            "In QuickBooks click + New > Inventory qty adjustment.",
            f"Pick the Adjustment date and an Inventory adjustment account, then add {g('name', 'the product')}.",
            f"Enter the New quantity: {g('qty', '(correct quantity)')} (QuickBooks currently shows {g('current_qty', 'a different number')}).",
            "Click Save and close.",
        ],
        "tax_account": [
            "Go to Taxes > Sales tax.",
            "Check the sales tax payable account is a Liability account and is active (Settings > Chart of accounts).",
            f"If it is missing, create it: Chart of accounts > New > Other Current Liabilities > Sales Tax Payable. Name it {g('name', 'Sales Tax Payable')}.",
        ],
        "refund_account": [
            "Go to Settings (gear icon) > Chart of accounts.",
            "Find or create an account for refunds: New > Income > Discounts/Refunds Given. This reduces sales; it is not an expense.",
            f"Name it {g('name', 'Sales Returns and Refunds')} and click Save and close.",
        ],
        "shipping_account": [
            "Go to Settings (gear icon) > Chart of accounts.",
            "Click New. For shipping you charge customers use Income > Shipping Income; for shipping you pay use Expenses > Shipping and delivery expense.",
            f"Name it {g('name', 'Shipping')} and click Save and close.",
        ],
        "marketplace_fees": [
            "Linnworks does not hold these fees. Download the payout statement from the marketplace.",
            "In QuickBooks click + New > Expense (or Bank deposit for the net payout).",
            f"Record the fees for {channel} against a Marketplace fees expense account, using the amounts on the statement.",
            "Click Save and close.",
        ],
    }
    if kind not in steps:
        raise ValueError(f"unknown fix kind: {kind}")
    return [f"{i}. {t}" for i, t in enumerate(steps[kind], 1)]


def rank_findings(findings):
    """Biggest money first, then urgency of the status."""
    def key(f):
        urg = STATUS_PLAIN.get(f.get("status"), {}).get("urgency", "medium")
        return (-abs(f.get("money") or 0), _URG[urg])
    return sorted(findings, key=key)


def headline(counts):
    """counts: {"decisions": int, "urgent": int}"""
    n, u = counts.get("decisions", 0), counts.get("urgent", 0)
    if n == 0:
        return "Nothing needs your decision."
    s = f"{n} thing{'s' if n != 1 else ''} need{'' if n != 1 else 's'} your decision"
    return s + (f", {u} {'are' if u != 1 else 'is'} urgent." if u else ".")


GLOSSARY = [
    ("Clearing account", "A temporary holding account where money sits until it is matched to a bank deposit or payout."),
    ("Contra-income", "An income account that reduces sales, such as refunds or discounts given."),
    ("Inventory asset", "The account showing the value of stock you own but have not yet sold."),
    ("COGS (cost of goods sold)", "What the stock you sold cost you. It moves out of inventory when a sale is made."),
    ("Reconciliation", "Checking that two sets of numbers (for example Linnworks and QuickBooks) agree, and explaining any difference."),
    ("Variance", "The difference between two numbers that should have matched."),
    ("Marketplace fee", "The commission and charges a sales channel such as Amazon or eBay keeps from each sale."),
    ("Payout / settlement", "The lump sum a marketplace pays into your bank, after taking its fees and refunds."),
    ("Product code", "The unique code that identifies one product, used to match it between Linnworks and QuickBooks."),
    ("Channel", "Where the sale happened, such as Amazon, eBay, Walmart or TikTok."),
    ("Chart of accounts", "The full list of accounts in QuickBooks that every transaction posts to."),
    ("Inventory adjustment", "An entry that corrects the stock quantity or value in QuickBooks."),
    ("Sales tax payable", "Tax collected from customers that you owe to the tax authority."),
    ("Inactive account", "An account switched off in QuickBooks; nothing new can post to it until it is made active again."),
    ("Warehouse / location", "A physical place stock is held. Linnworks can total stock across several, so check which one you are comparing."),
]


GAP_PLAIN = {
    "no_price_data": "Neither system's list has prices, so price can't help confirm a product match.",
    "no_chart_of_accounts": "The QuickBooks chart of accounts wasn't provided, so product categories can't be matched to accounts (an unmatched category can make a Sales Order fail to sync).",
    "marketplace_fees_not_in_linnworks": "Marketplace and payment fees aren't in Linnworks; they come from the payout statements (Amazon, eBay, Stripe) and need recording separately.",
    "channel_no_clearing_account": "Some sales channels have no clearing account in QuickBooks, so their sales have nowhere correct to post.",
    "possible_multi_location_qty": "Linnworks stock looks far higher than QuickBooks; it may be added up across warehouses. Confirm before adjusting any quantity.",
    "qbo_sku_column_is_item_id": "The QuickBooks list's product-code column actually holds QuickBooks item numbers; product names were used to match instead.",
}


def gap_text(gap):
    """Plain sentence for a data_gap_findings() dict; falls back to its detail text."""
    return GAP_PLAIN.get(gap.get("gap"), gap.get("detail", ""))
