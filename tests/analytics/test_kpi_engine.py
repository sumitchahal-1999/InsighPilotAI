"""
InsightPilot AI — KPI Engine Unit Tests
Tests deterministic calculations for all 5 core KPIs, variances, and sparse-history evaluation.
"""

import unittest
from datetime import date
from analytics.data_loader import DataLoader
from analytics.kpi_engine import KPIEngine

class TestKPIEngine(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.loader = DataLoader()
        cls.kpi_engine = KPIEngine(cls.loader)

    def test_revenue_calculation(self):
        # Q2 2026 NA-East
        q2_start, q2_end = date(2026, 4, 1), date(2026, 6, 30)
        q2_rev = self.kpi_engine.calculate_revenue("NA-East", q2_start, q2_end)
        self.assertGreater(q2_rev, 15000000.0)
        self.assertAlmostEqual(q2_rev, 15430000.0, delta=50000.0)

        # Q3 2026 NA-East
        q3_start, q3_end = date(2026, 7, 1), date(2026, 9, 30)
        q3_rev = self.kpi_engine.calculate_revenue("NA-East", q3_start, q3_end)
        self.assertGreater(q3_rev, 13800000.0)
        self.assertAlmostEqual(q3_rev, 14200000.0, delta=50000.0)

    def test_revenue_movement_evaluation(self):
        eval_res = self.kpi_engine.evaluate_kpi_movement(
            kpi_id="north_america_east_revenue",
            region="NA-East",
            prev_period_id="2026-Q2",
            curr_period_id="2026-Q3"
        )
        self.assertEqual(eval_res["id"], "north_america_east_revenue")
        self.assertAlmostEqual(eval_res["percent_change"], -7.97, places=1)
        self.assertEqual(eval_res["materiality_status"], "CRITICAL_NEGATIVE_VARIANCE")

    def test_gross_margin_calculation(self):
        q2_margin = self.kpi_engine.calculate_gross_margin("NA-East", "2026-Q2")
        q3_margin = self.kpi_engine.calculate_gross_margin("NA-East", "2026-Q3")
        self.assertGreater(q2_margin, 45.0)
        self.assertLess(q3_margin, q2_margin) # Margin compressed due to emergency freight and SKU mix
        self.assertAlmostEqual(q3_margin, 46.04, places=1)

    def test_units_sold_calculation(self):
        q2_start, q2_end = date(2026, 4, 1), date(2026, 6, 30)
        q3_start, q3_end = date(2026, 7, 1), date(2026, 9, 30)
        q2_units = self.kpi_engine.calculate_units_sold("NA-East", q2_start, q2_end)
        q3_units = self.kpi_engine.calculate_units_sold("NA-East", q3_start, q3_end)
        self.assertGreater(q2_units, q3_units)
        self.assertGreater(q2_units, 100000)

    def test_distributor_orders_calculation(self):
        q2_start, q2_end = date(2026, 4, 1), date(2026, 6, 30)
        orders_count = self.kpi_engine.calculate_distributor_orders("NA-East", q2_start, q2_end)
        self.assertGreater(orders_count, 50)

    def test_inventory_availability_calculation(self):
        # Healthy period
        q2_start, q2_end = date(2026, 4, 1), date(2026, 6, 30)
        q2_avail = self.kpi_engine.calculate_inventory_availability("NA-East", q2_start, q2_end)
        self.assertGreater(q2_avail, 90.0)

        # Disruption period at Atlanta DC
        disrupt_start, disrupt_end = date(2026, 8, 1), date(2026, 8, 19)
        atl_avail = self.kpi_engine.calculate_inventory_availability("NA-East", disrupt_start, disrupt_end, dc_location="Atlanta-DC-01")
        self.assertLess(atl_avail, 85.0)

    def test_sparse_history_check(self):
        # 14-day sparse window
        sparse_res = self.kpi_engine.check_sparse_history(date(2026, 8, 1), date(2026, 8, 14), min_days=60)
        self.assertTrue(sparse_res["is_sparse"])
        self.assertEqual(sparse_res["status"], "INSUFFICIENT_HISTORY")

        # 90-day sufficient window
        suff_res = self.kpi_engine.check_sparse_history(date(2026, 7, 1), date(2026, 9, 30), min_days=60)
        self.assertFalse(suff_res["is_sparse"])
        self.assertEqual(suff_res["status"], "SUFFICIENT_HISTORY")

if __name__ == "__main__":
    unittest.main()
