"""
Tests for the SKU-first product-identity matching pipeline (mapping_engine.match_product_identity)
and the deterministic conclusions generator.
"""
import sys, os, unittest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

from normalize import SourceRecord, TargetRecord
from mapping_engine import match_product_identity, find_orphaned_products
from coverage import coverage_report
from conclusions import derive_conclusions


def prod_src(sku, name, price=None):
    return SourceRecord(source_system="linnworks", entity_type="sku", source_id=sku, name=name, amount=price, sku=sku)


def item_tgt(target_id, sku, name, price=None, active=True):
    return TargetRecord(target_system="qbo", entity_type="item", target_id=target_id, name=name, sku=sku,
                         unit_price=price, active=active)


class TestProductMatching(unittest.TestCase):

    def test_sku_exact_match_is_high_confidence(self):
        s = prod_src("0051", "Two Cent Coin", price=33)
        t = item_tgt("i1", "0051", "Two Cent Coin Item", price=999)  # price irrelevant once SKU hits
        r = match_product_identity(s, [t])
        self.assertEqual(r.status, "MAPPED")
        self.assertEqual(r.confidence, "HIGH")
        self.assertFalse(r.review_required)

    def test_duplicate_sku_in_qbo_is_ambiguous(self):
        s = prod_src("0051", "Two Cent Coin")
        t1 = item_tgt("i1", "0051", "Two Cent Coin A")
        t2 = item_tgt("i2", "0051", "Two Cent Coin B")
        r = match_product_identity(s, [t1, t2])
        self.assertEqual(r.status, "AMBIGUOUS")

    def test_name_only_match_no_price_is_unverified(self):
        s = prod_src("9999-NOTINQBO", "Two Cent Coin", price=33)
        t = item_tgt("i1", "OTHER-SKU", "Two Cent Coin", price=500)  # name matches, price way off
        r = match_product_identity(s, [t])
        self.assertEqual(r.status, "UNVERIFIED")
        self.assertEqual(r.confidence, "LOW")
        self.assertTrue(r.review_required)

    def test_name_match_with_price_corroboration_is_mapped_medium(self):
        s = prod_src("9999-NOTINQBO", "Two Cent Coin", price=33)
        t = item_tgt("i1", "OTHER-SKU", "Two Cent Coin", price=33.50)  # within 5% tolerance
        r = match_product_identity(s, [t])
        self.assertEqual(r.status, "MAPPED")
        self.assertEqual(r.confidence, "MEDIUM")

    def test_name_tie_broken_by_price(self):
        s = prod_src("x", "Water Bottles Generic", price=10)
        t1 = item_tgt("i1", "WB-1", "Water Bottles Generic", price=10.10)
        t2 = item_tgt("i2", "WB-2", "Water Bottles Generic", price=999)
        r = match_product_identity(s, [t1, t2])
        self.assertEqual(r.status, "MAPPED")
        self.assertEqual(r.target_id, "i1")

    def test_name_tie_unbroken_is_ambiguous(self):
        s = prod_src("x", "Water Bottles Generic", price=10)
        t1 = item_tgt("i1", "WB-1", "Water Bottles Generic", price=None)
        t2 = item_tgt("i2", "WB-2", "Water Bottles Generic", price=None)
        r = match_product_identity(s, [t1, t2])
        self.assertEqual(r.status, "AMBIGUOUS")

    def test_no_sku_no_name_overlap_is_unmapped(self):
        s = prod_src("x", "Two Cent Coin", price=33)
        t = item_tgt("i1", "y", "Guest Book", price=25)
        r = match_product_identity(s, [t])
        self.assertEqual(r.status, "UNMAPPED")

    def test_orphaned_product(self):
        s = prod_src("0051", "Two Cent Coin")
        matched = item_tgt("i1", "0051", "Two Cent Coin")
        orphan = item_tgt("i2", "9999", "Unrelated Badge")
        result = match_product_identity(s, [matched, orphan])
        orphans = find_orphaned_products([matched, orphan], [result])
        self.assertEqual(len(orphans), 1)
        self.assertEqual(orphans[0].target_name, "Unrelated Badge")

    def test_coverage_report_counts_unverified_separately_from_unmapped(self):
        r1 = match_product_identity(prod_src("a", "Coin X", price=10),
                                     [item_tgt("i1", "b", "Coin X", price=500)])  # UNVERIFIED
        cov = coverage_report([r1])
        self.assertEqual(cov["unverified_count"], 1)
        self.assertEqual(cov["unmapped_count"], 0)


class TestConclusions(unittest.TestCase):

    def test_flags_count_value_divergence(self):
        cov = {"count_coverage_pct": 95.0, "value_coverage_pct": 58.5, "total_count": 100,
               "mapped_count": 95, "ambiguous_count": 0, "orphaned_count": 0}
        notes = derive_conclusions(cov)
        self.assertTrue(any("materially higher" in n for n in notes))

    def test_flags_zero_zero_as_scoping_signal(self):
        cov = {"count_coverage_pct": 0.0, "value_coverage_pct": 0.0, "total_count": 6,
               "mapped_count": 0, "ambiguous_count": 6, "orphaned_count": 14}
        notes = derive_conclusions(cov)
        self.assertTrue(any("Data Scoping" in n for n in notes))

    def test_no_findings_message_when_clean(self):
        cov = {"count_coverage_pct": 100.0, "value_coverage_pct": 100.0, "total_count": 5,
               "mapped_count": 5, "ambiguous_count": 0, "orphaned_count": 0}
        notes = derive_conclusions(cov)
        self.assertTrue(any("clean" in n for n in notes))


if __name__ == "__main__":
    unittest.main()
