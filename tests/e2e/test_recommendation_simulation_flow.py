"""
InsightPilot AI — Phase 5.8: Recommendations & Simulation E2E Test Suite
Verifies that prescriptive action levers and deterministic what-if simulations
preserve exact quantitative integrity, mathematical determinism, and source immutability.
"""

import unittest
from fastapi.testclient import TestClient
from backend.app.main import app
from analytics.data_loader import DataLoader
from analytics.recommendations import RecommendationEngine
from simulation.simulation_engine import SimulationEngine


class TestRecommendationSimulationFlow(unittest.TestCase):
    """End-to-End Recommendations & Simulation Engine tests."""

    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)
        cls.kpi_id = "north_america_east_revenue"
        cls.loader = DataLoader(use_db=True)
        cls.rec_engine = RecommendationEngine(cls.loader)
        cls.sim_engine = SimulationEngine(cls.loader)

    # -------------------------------------------------------------------------
    # 1. Canonical Recommendations Suite
    # -------------------------------------------------------------------------
    def test_canonical_recommendations_integrity(self):
        """Verifies that the recommendation engine returns prioritized, grounded action levers."""
        recs = self.rec_engine.generate_recommendations(self.kpi_id)
        self.assertEqual(len(recs), 4)

        # Rec #1: Atlanta DC Transfer
        rec1 = recs[0]
        self.assertEqual(rec1["driver_id"], "atlanta_dc_stockout")
        self.assertIn("20,000", rec1["action"])
        self.assertEqual(rec1["controllability"], "HIGH")
        self.assertAlmostEqual(rec1["expected_impact"]["revenue_recovery_usd"], 484000.0, places=0)
        self.assertEqual(rec1["priority"], "CRITICAL")
        self.assertEqual(rec1["priority_rank"], 1)
        self.assertIn("EVID_ERP_ATL_STOCKOUT_001", rec1["supporting_evidence_ids"])

        # Rec #2: Distributor Outreach
        rec2 = recs[1]
        self.assertEqual(rec2["driver_id"], "distributor_orders")
        self.assertAlmostEqual(rec2["expected_impact"]["revenue_recovery_usd"], 180000.0, places=0)
        self.assertEqual(rec2["controllability"], "HIGH")

        # Rec #3: SKU Allocation
        rec3 = recs[2]
        self.assertEqual(rec3["driver_id"], "sku_8821_sales_volume")
        self.assertAlmostEqual(rec3["expected_impact"]["revenue_recovery_usd"], 238000.0, places=0)
        self.assertEqual(rec3["controllability"], "MEDIUM")

        # Rec #4: Competitor Horizon Pricing
        rec4 = recs[3]
        self.assertEqual(rec4["driver_id"], "competitor_horizon_pricing")
        self.assertAlmostEqual(rec4["expected_impact"]["revenue_recovery_usd"], 93600.0, places=0)
        self.assertEqual(rec4["controllability"], "LOW")

    # -------------------------------------------------------------------------
    # 2. Deterministic What-If Simulation
    # -------------------------------------------------------------------------
    def test_deterministic_simulation_execution(self):
        """Verifies simulation engine calculation for inventory availability improvement from 79.4% to 90.0%."""
        result = self.sim_engine.simulate_inventory_availability(
            inventory_availability=90.0,
            region="NA-East"
        )

        self.assertAlmostEqual(result["baseline_value"], 79.4, places=1)
        self.assertAlmostEqual(result["scenario_value"], 90.0, places=1)
        self.assertAlmostEqual(result["estimated_recovery"]["revenue_recovery_usd"], 341422.91, places=2)
        self.assertAlmostEqual(result["estimated_recovery"]["margin_recovery_pct"], 0.72, places=2)
        self.assertAlmostEqual(result["projected_value"], 14541422.96, places=2)
        self.assertEqual(result["confidence"]["score"], 91)
        self.assertEqual(result["confidence"]["label"], "HIGH")

    # -------------------------------------------------------------------------
    # 3. Mathematical Parity & Immutability
    # -------------------------------------------------------------------------
    def test_simulation_mathematical_determinism_and_immutability(self):
        """Repeated simulation executions yield exact identical floating point values without mutating data."""
        res1 = self.sim_engine.simulate_inventory_availability(85.0, "NA-East")
        res2 = self.sim_engine.simulate_inventory_availability(85.0, "NA-East")

        self.assertEqual(res1["projected_value"], res2["projected_value"])
        self.assertEqual(res1["estimated_recovery"]["revenue_recovery_usd"], res2["estimated_recovery"]["revenue_recovery_usd"])

        # Check baseline has not changed
        baseline = self.sim_engine.get_baseline_state("NA-East")
        self.assertAlmostEqual(baseline["baseline_availability_pct"], 79.4, places=1)

    # -------------------------------------------------------------------------
    # 4. Simulation API Endpoints & Input Boundaries
    # -------------------------------------------------------------------------
    def test_simulation_api_validation(self):
        """Verifies that FastAPI simulation endpoints enforce input boundary constraints."""
        # 1. Valid Simulation
        valid_payload = {
            "inventory_availability": 0.90,
            "region": "NA-East"
        }
        res = self.client.post("/api/v1/simulations/run", json=valid_payload)
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertAlmostEqual(data["estimated_recovery"]["revenue_recovery_usd"], 341422.91, places=2)

        # 2. Out of bounds (>100%)
        invalid_payload = {
            "target_availability_pct": 150.0,
            "region": "NA-East"
        }
        res_invalid = self.client.post("/api/v1/simulations/run", json=invalid_payload)
        self.assertEqual(res_invalid.status_code, 400)

        # 3. Negative value (<0%)
        negative_payload = {
            "target_availability_pct": -10.0,
            "region": "NA-East"
        }
        res_neg = self.client.post("/api/v1/simulations/run", json=negative_payload)
        self.assertEqual(res_neg.status_code, 400)


if __name__ == "__main__":
    unittest.main()
