"""
Covers spec #15 cases 1-8 (mapping-engine-level) with synthetic fixtures.
Run: python -m pytest tests/ -v   (or: python tests/test_mapping_engine.py)
"""
import sys, os, unittest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

from normalize import SourceRecord, TargetRecord
from mapping_engine import propose_mapping, find_orphaned_targets, apply_llm_proposal


def src(entity_type, name, source_id=None, amount=None, currency="USD", channel=None):
    return SourceRecord(
        source_system="linnworks", entity_type=entity_type, source_id=source_id or name,
        name=name, amount=amount, currency=currency, channel=channel,
    )


def tgt(name, account_type, target_id=None, active=True):
    return TargetRecord(
        target_system="qbo", entity_type="account", target_id=target_id or name,
        name=name, account_type=account_type, active=active,
    )


class TestMappingEngine(unittest.TestCase):

    def test_1_exact_mapping(self):
        s = src("channel", "Amazon Sales", source_id="Amazon Sales")
        t = tgt("Amazon Sales", "Income")
        r = propose_mapping(s, [t])
        self.assertEqual(r.status, "MAPPED")
        self.assertEqual(r.confidence, "HIGH")
        self.assertFalse(r.review_required)

    def test_2_semantic_mapping(self):
        s = src("channel", "Acme Co - Amazon", channel="AMAZON")
        t = tgt("Amazon Income", "Income")
        r = propose_mapping(s, [t])
        self.assertEqual(r.status, "MAPPED")
        self.assertIn(r.confidence, ("HIGH", "MEDIUM"))

    def test_3_account_type_mismatch(self):
        s = src("channel", "eBay", channel="EBAY")
        t = tgt("eBay Fees", "Expenses")  # wrong type for a sales_income concept
        r = propose_mapping(s, [t])
        self.assertEqual(r.status, "UNMAPPED")

    def test_4_missing_target(self):
        s = src("channel", "TikTok", channel="TIKTOK")
        r = propose_mapping(s, [tgt("Amazon Sales", "Income")])
        self.assertEqual(r.status, "UNMAPPED")
        self.assertEqual(r.confidence, "UNRESOLVED")

    def test_5_ambiguous_target(self):
        s = src("channel", "Direct", channel="DIRECT")
        targets = [tgt("Sales", "Income"), tgt("Sales of Product Income", "Income")]
        r = propose_mapping(s, targets)
        self.assertEqual(r.status, "AMBIGUOUS")
        self.assertTrue(r.review_required)

    def test_6_inactive_target(self):
        s = src("channel", "Amazon Sales", source_id="Amazon Sales")
        t = tgt("Amazon Sales", "Income", active=False)
        r = propose_mapping(s, [t])
        self.assertEqual(r.status, "INACTIVE")
        self.assertTrue(r.review_required)

    def test_7_orphan_qbo_account(self):
        s = src("channel", "Amazon Sales", source_id="Amazon Sales")
        matched = tgt("Amazon Sales", "Income")
        orphan = tgt("Commission Income", "Income")
        result = propose_mapping(s, [matched, orphan])
        orphans = find_orphaned_targets([matched, orphan], [result])
        self.assertEqual(len(orphans), 1)
        self.assertEqual(orphans[0].target_name, "Commission Income")
        self.assertEqual(orphans[0].status, "ORPHANED")

    def test_8_structural_data_gap_undetermined_concept(self):
        # entity_type not in CONCEPT_RULES -> concept 'undetermined' -> UNRESOLVED, not a false MAPPED
        s = SourceRecord(source_system="linnworks", entity_type="marketplace_settlement_adjustment",
                          source_id="x", name="Settlement adjustment", amount=42.0, currency="USD")
        r = propose_mapping(s, [tgt("Merchant Account Fees", "Cost of Goods Sold")])
        self.assertEqual(r.status, "UNMAPPED")
        self.assertEqual(r.confidence, "UNRESOLVED")

    def test_invalid_explicit_rule_wrong_type(self):
        s = src("refund", "Refund", source_id="refund-1")
        t = tgt("Bank charges", "Expenses", target_id="acct-bank-charges")
        r = propose_mapping(s, [t], explicit_rules={"refund-1": "acct-bank-charges"})
        self.assertEqual(r.status, "INVALID")
        self.assertTrue(r.review_required)

    def test_llm_proposal_always_review_required_medium_cap(self):
        s = src("channel", "Weird Channel Name", channel="WEIRD")
        t = tgt("Some Income Account", "Income")
        r = apply_llm_proposal(s, t, "LLM inferred this is likely the general sales account")
        self.assertEqual(r.confidence, "MEDIUM")
        self.assertTrue(r.review_required)


if __name__ == "__main__":
    unittest.main()


class TestDiagnostics(unittest.TestCase):
    """SYNTHETIC fixtures."""

    def test_multi_location_warning(self):
        from mapping_engine import inventory_totals_check
        s = [SourceRecord("linnworks", "sku", "a", "a", sku="a", qty=300)]
        t = [TargetRecord("qbo", "item", "1", "a", qty=100)]
        c = inventory_totals_check(s, t)
        self.assertEqual((c["lw_total_qty"], c["qbo_total_qty"], c["ratio"]), (300, 100, 3.0))
        self.assertTrue(c["possible_multi_location_sum"])
        t[0].qty = 250
        self.assertFalse(inventory_totals_check(s, t)["possible_multi_location_sum"])

    def test_data_gap_findings(self):
        from mapping_engine import data_gap_findings
        srcs = [SourceRecord("linnworks", "sku", "a", "a", sku="a", qty=300),
                SourceRecord("linnworks", "channel", "TIKTOK||USD", "TIKTOK", channel="TIKTOK")]
        tgts = [TargetRecord("qbo", "item", "1", "a", qty=100)]
        res = [propose_mapping(srcs[1], tgts)]
        gaps = {g["gap"]: g for g in data_gap_findings(srcs, tgts, res)}
        for k in ("no_price_data", "no_chart_of_accounts", "marketplace_fees_not_in_linnworks",
                  "channel_no_clearing_account", "possible_multi_location_qty"):
            self.assertIn(k, gaps)
            self.assertEqual(set(gaps[k]), {"gap", "severity", "detail"})
        self.assertIn("TIKTOK", gaps["channel_no_clearing_account"]["detail"])
        tgts.append(TargetRecord("qbo", "account", "9", "Sales", account_type="Income"))
        self.assertNotIn("no_chart_of_accounts", {g["gap"] for g in data_gap_findings(srcs, tgts)})
