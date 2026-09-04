"""
InsightPilot AI — Driver Engine Unit Tests
Tests multi-factor driver decomposition, Atlanta stockout signals, SKU-8821 volume,
distributor deferrals, competitor pricing, and contribution normalization.
"""

import unittest
from datetime import date
from analytics.data_loader import DataLoader
from analytics.driver_engine import DriverEngine

class TestDriverEngine(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.loader = DataLoader()
        cls.driver_engine = DriverEngine(cls.loader)

    def test_atlanta_stockout_analysis(self):
        res = self.driver_engine.analyze_atlanta_stockout("NA-East", date(2026, 7, 1), date(2026, 9, 30))
        self.assertEqual(res["driver_id"], "atlanta_dc_stockout")
        self.assertLess(res["raw_impact_usd"], 0)
        self.assertGreater(res["disruption_days_count"], 10)
        self.assertGreater(len(res["evidence_ids"]), 0)

    def test_sku8821_volume_analysis(self):
        res = self.driver_engine.analyze_sku8821_volume(
            "NA-East",
            date(2026, 4, 1), date(2026, 6, 30),
            date(2026, 7, 1), date(2026, 9, 30)
        )
        self.assertEqual(res["driver_id"], "sku_8821_sales_volume")
        self.assertLess(res["raw_impact_usd"], 0)
        self.assertGreater(res["unit_deficit"], 5000)

    def test_distributor_orders_analysis(self):
        res = self.driver_engine.analyze_distributor_orders("NA-East", date(2026, 7, 1), date(2026, 9, 30))
        self.assertEqual(res["driver_id"], "distributor_orders")
        self.assertLess(res["raw_impact_usd"], 0)
        self.assertGreater(res["deferred_orders_count"], 5)

    def test_competitor_pricing_analysis(self):
        res = self.driver_engine.analyze_competitor_pricing("NA-East", date(2026, 7, 1), date(2026, 9, 30))
        self.assertEqual(res["driver_id"], "competitor_horizon_pricing")
        self.assertLess(res["raw_impact_usd"], 0)
        self.assertGreater(res["competitor_observations_count"], 0)

    def test_contribution_normalization_sum(self):
        drivers = self.driver_engine.investigate_revenue_drivers("NA-East", "2026-Q2", "2026-Q3")
        self.assertEqual(len(drivers), 4)
        
        # Verify ranked ordering (Rank 1, 2, 3, 4)
        ranks = [d["rank"] for d in drivers]
        self.assertEqual(ranks, [1, 2, 3, 4])
        
        # Verify sum of contributions equals exactly 100.0%
        total_pct = sum(d["contribution_pct"] for d in drivers)
        self.assertAlmostEqual(total_pct, 100.0, places=1)
        
        # Verify Atlanta Stockout is top contributor
        self.assertEqual(drivers[0]["driver_id"], "atlanta_dc_stockout")
        self.assertGreater(drivers[0]["contribution_pct"], 35.0)

if __name__ == "__main__":
    unittest.main()
