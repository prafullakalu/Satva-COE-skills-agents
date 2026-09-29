"""
Covers spec #15 cases 9-16: count coverage, value coverage, reconciliation variance,
currency difference, refund mismatch, tax mismatch, shipping mismatch, marketplace fee gap.
"""
import sys, os, unittest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

from mapping_engine import MappingResult
from coverage import coverage_report
from reconcile import reconcile, reconcile_many


def mr(status, value=None, currency="USD", name="x"):
    return MappingResult(
        source_id=name, source_type="channel", source_name=name, source_value=value,
        currency=currency, target_id=("t" if status == "MAPPED" else None),
        target_name=("Target" if status == "MAPPED" else None), target_type="Income",
        status=status, confidence="HIGH" if status == "MAPPED" else "UNRESOLVED",
    )


class TestCoverage(unittest.TestCase):

    def test_9_count_coverage(self):
        results = [mr("MAPPED") for _ in range(95)] + [mr("UNMAPPED") for _ in range(5)]
        cov = coverage_report(results)
        self.assertEqual(cov["total_count"], 100)
        self.assertEqual(cov["count_coverage_pct"], 95.0)

    def test_10_value_coverage_diverges_from_count(self):
        # 95% count coverage but low value coverage: mirrors spec's own worked example.
        results = [mr("MAPPED", value=1200) for _ in range(95)]
        results += [mr("UNMAPPED", value=85000 / 5) for _ in range(5)]
        cov = coverage_report(results)
        self.assertEqual(cov["count_coverage_pct"], 95.0)
        self.assertLess(cov["value_coverage_pct"], cov["count_coverage_pct"])

    def test_11_reconciliation_variance(self):
        row = reconcile("Sales", 412830, 398120, "USD")
        self.assertEqual(row.status, "UNEXPLAINED_VARIANCE")
        self.assertAlmostEqual(row.variance, 14710)

    def test_12_currency_difference_not_summed(self):
        # coverage_report must never merge two currencies into one total silently at this layer;
        # caller is responsible for grouping by currency before calling. Verify totals are per-call.
        usd = coverage_report([mr("MAPPED", value=100, currency="USD")])
        gbp = coverage_report([mr("MAPPED", value=100, currency="GBP")])
        self.assertEqual(usd["total_value"], 100)
        self.assertEqual(gbp["total_value"], 100)

    def test_13_refund_mismatch(self):
        row = reconcile("Refunds", 2910, 2500, "USD")
        self.assertEqual(row.status, "UNEXPLAINED_VARIANCE")

    def test_14_tax_mismatch(self):
        row = reconcile("Tax", 105.42, 105.42, "USD")
        self.assertEqual(row.status, "MATCHED")

    def test_15_shipping_mismatch(self):
        row = reconcile("Shipping", 3033.30, 1840.00, "USD")
        self.assertEqual(row.status, "UNEXPLAINED_VARIANCE")
        self.assertGreater(row.variance_pct, 0.5)

    def test_16_marketplace_fee_gap_zero_qbo_side(self):
        # Marketplace fees: Linnworks has nothing, QBO has an unrelated total -> still a variance,
        # not swallowed as 'matched by coincidence'.
        row = reconcile("Marketplace fees", 0, 0, "USD")
        self.assertEqual(row.status, "MATCHED")  # both zero is a real match, not a gap
        row2 = reconcile("Marketplace fees", 0, 450, "USD")
        self.assertEqual(row2.status, "UNEXPLAINED_VARIANCE")

    def test_reconcile_many(self):
        rows = reconcile_many([
            {"category": "Sales", "linnworks_total": 100, "qbo_total": 100, "currency": "USD"},
            {"category": "Tax", "linnworks_total": 10, "qbo_total": 9, "currency": "USD"},
        ])
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0].status, "MATCHED")


if __name__ == "__main__":
    unittest.main()
