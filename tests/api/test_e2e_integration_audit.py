"""
InsightPilot AI — End-to-End Integration & Contract Audit Test Suite
Verifies the complete analytical and decision chain across all 7 presentation screens:
Raw Data -> KPI -> Investigation -> Drivers -> Evidence -> Recommendations -> Simulation -> Executive Briefing.
"""

import unittest
from fastapi.testclient import TestClient
from backend.app.main import app

class TestEndToEndIntegrationAudit(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    # 1. Screen 1 Contract Audit: Executive Command Center
    def test_screen_1_command_center_contract(self):
        res = self.client.get("/api/v1/kpis")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        
        self.assertEqual(data["total_count"], 5)
        kpi_map = {k["id"]: k for k in data["kpis"]}
        
        # Verify Revenue KPI
        rev = kpi_map["north_america_east_revenue"]
        self.assertAlmostEqual(rev["previous_value"], 15430000.06, delta=100.0)
        self.assertAlmostEqual(rev["current_value"], 14200000.05, delta=100.0)
        self.assertAlmostEqual(rev["variance_amount"], -1230000.01, delta=100.0)
        self.assertAlmostEqual(rev["percent_change"], -7.97, places=1)
        self.assertEqual(rev["materiality_status"], "CRITICAL_NEGATIVE_VARIANCE")
        
        # Verify Other 4 Core KPIs
        self.assertIn("gross_margin", kpi_map)
        self.assertIn("units_sold", kpi_map)
        self.assertIn("inventory_availability", kpi_map)
        self.assertIn("distributor_orders", kpi_map)

    # 2. Screen 2 & 3 Contract Audit: Investigation Activity & Root Cause
    def test_screen_2_and_3_investigation_and_drivers(self):
        res = self.client.get("/api/v1/investigations/north_america_east_revenue?region=NA-East&prev_period_id=2026-Q2&curr_period_id=2026-Q3")
        self.assertEqual(res.status_code, 200)
        inv = res.json()
        
        # Investigation Header & Confidence
        self.assertEqual(inv["kpi"]["id"], "north_america_east_revenue")
        self.assertAlmostEqual(inv["kpi"]["variance_amount"], -1230000.01, delta=100.0)
        self.assertAlmostEqual(inv["kpi"]["percent_change"], -7.97, places=1)
        self.assertEqual(inv["overall"]["overall_confidence"], 89)
        self.assertEqual(inv["overall"]["confidence_label"], "HIGH")
        self.assertFalse(inv["overall"]["abstention"])
        
        # 4 Authoritative Drivers
        self.assertEqual(len(inv["drivers"]), 4)
        d1, d2, d3, d4 = inv["drivers"]
        
        # Driver 1: Atlanta DC Stockout
        self.assertEqual(d1["driver_id"], "atlanta_dc_stockout")
        self.assertAlmostEqual(d1["contribution_pct"], 43.2, places=1)
        self.assertAlmostEqual(d1["impact_usd"], -550000.0, delta=1000.0)
        self.assertEqual(d1["confidence_score"], 94)
        self.assertEqual(d1["rank"], 1)
        
        # Driver 2: SKU-8821 Sales Volume
        self.assertEqual(d2["driver_id"], "sku_8821_sales_volume")
        self.assertAlmostEqual(d2["contribution_pct"], 26.7, places=1)
        self.assertAlmostEqual(d2["impact_usd"], -340000.0, delta=1000.0)
        self.assertEqual(d2["confidence_score"], 89)
        self.assertEqual(d2["rank"], 2)
        
        # Driver 3: Distributor Orders Deferral
        self.assertEqual(d3["driver_id"], "distributor_orders")
        self.assertAlmostEqual(d3["contribution_pct"], 18.8, places=1)
        self.assertAlmostEqual(d3["impact_usd"], -240000.0, delta=1000.0)
        self.assertEqual(d3["confidence_score"], 85)
        self.assertEqual(d3["rank"], 3)
        
        # Driver 4: Competitor Horizon Foods Pricing
        self.assertEqual(d4["driver_id"], "competitor_horizon_pricing")
        self.assertAlmostEqual(d4["contribution_pct"], 11.3, places=1)
        self.assertAlmostEqual(d4["impact_usd"], -144000.0, delta=1000.0)
        self.assertEqual(d4["confidence_score"], 78)
        self.assertEqual(d4["rank"], 4)
        
        # Total contribution must sum to 100%
        total_pct = sum(d["contribution_pct"] for d in inv["drivers"])
        self.assertAlmostEqual(total_pct, 100.0, places=1)

    # 3. Screen 4 & 5 Contract Audit: Decision Graph & Evidence Explorer
    def test_screen_4_and_5_decision_graph_and_evidence(self):
        res = self.client.get("/api/v1/investigations/north_america_east_revenue/evidence")
        self.assertEqual(res.status_code, 200)
        ev_data = res.json()
        
        self.assertEqual(ev_data["total_evidence_count"], 9)
        ev_map = {e["evidence_id"]: e for e in ev_data["evidence"]}
        
        # Verify primary evidence items
        self.assertIn("EVID_ERP_ATL_STOCKOUT_001", ev_map)
        e1 = ev_map["EVID_ERP_ATL_STOCKOUT_001"]
        self.assertEqual(e1["source_domain"], "ERP")
        self.assertEqual(e1["source_record_id"], "INV-SNAP-21971")
        self.assertEqual(e1["confidence"]["score"], 94)
        self.assertTrue(e1["lineage"]["verification_hash"].startswith("sha256:"))
        
        # Verify Zendesk ticket delay evidence
        self.assertIn("EVID_ZENDESK_ATL_DELAY_003", ev_map)
        e2 = ev_map["EVID_ZENDESK_ATL_DELAY_003"]
        self.assertEqual(e2["source_domain"], "SUPPORT_MARKET_INTEL")
        self.assertEqual(e2["confidence"]["score"], 90)
        
        # Verify Market promo evidence
        self.assertIn("EVID_MKT_HORIZON_PROMO_008", ev_map)
        e3 = ev_map["EVID_MKT_HORIZON_PROMO_008"]
        self.assertEqual(e3["confidence"]["score"], 78)

        
        # Lineage detail verification
        res_lineage = self.client.get("/api/v1/evidence/EVID_ERP_ATL_STOCKOUT_001/lineage")
        self.assertEqual(res_lineage.status_code, 200)
        lineage = res_lineage.json()
        self.assertEqual(lineage["kpi"], "north_america_east_revenue")
        self.assertEqual(lineage["driver"], "atlanta_dc_stockout")

    # 4. Screen 6 Contract Audit: Recommendations & What-If Simulation
    def test_screen_6_recommendations_and_simulation(self):
        # Recommendations
        res_rec = self.client.get("/api/v1/recommendations/north_america_east_revenue")
        self.assertEqual(res_rec.status_code, 200)
        rec_data = res_rec.json()
        
        self.assertEqual(rec_data["total_recommendations"], 4)
        r1 = rec_data["recommendations"][0]
        self.assertEqual(r1["recommendation_id"], "REC-2026-NAE-001")
        self.assertIn("Emergency Inventory Transfer", r1["action"])
        self.assertEqual(r1["expected_impact"]["revenue_recovery_usd"], 484000.0)
        self.assertEqual(r1["confidence"]["score"], 91)
        self.assertEqual(r1["expected_impact"]["recovery_timeframe_days"], 14)
        
        r2 = rec_data["recommendations"][1]
        self.assertEqual(r2["recommendation_id"], "REC-2026-NAE-002")
        self.assertEqual(r2["expected_impact"]["revenue_recovery_usd"], 180000.0)
        self.assertEqual(r2["confidence"]["score"], 85)
        
        # Simulation Baseline
        res_base = self.client.get("/api/v1/simulations/baseline")
        self.assertEqual(res_base.status_code, 200)
        base = res_base.json()
        self.assertEqual(base["baseline_availability_pct"], 79.4)
        self.assertEqual(base["baseline_revenue_usd"], 14200000.05)
        
        # Simulation 90% Availability
        res_sim = self.client.post(
            "/api/v1/simulations/inventory-availability",
            json={"inventory_availability": 0.90}
        )
        self.assertEqual(res_sim.status_code, 200)
        sim = res_sim.json()
        self.assertEqual(sim["baseline_value"], 79.4)
        self.assertEqual(sim["scenario_value"], 90.0)
        self.assertAlmostEqual(sim["estimated_recovery"]["revenue_recovery_usd"], 341422.91, places=1)
        self.assertAlmostEqual(sim["projected_value"], 14541422.96, places=1)
        self.assertEqual(sim["confidence"]["score"], 91)

    # 5. Screen 7 Contract Audit: Executive Briefing Aggregation Consistency
    def test_screen_7_executive_briefing_consistency(self):
        # Briefing consumes /investigations and /recommendations
        inv_res = self.client.get("/api/v1/investigations/north_america_east_revenue")
        rec_res = self.client.get("/api/v1/recommendations/north_america_east_revenue")
        
        self.assertEqual(inv_res.status_code, 200)
        self.assertEqual(rec_res.status_code, 200)
        
        inv = inv_res.json()
        recs = rec_res.json()
        
        # Verify Situation consistency
        self.assertAlmostEqual(inv["kpi"]["current_value"], 14200000.05, delta=100.0)
        self.assertAlmostEqual(inv["kpi"]["variance_amount"], -1230000.01, delta=100.0)
        
        # Verify Primary Diagnosis matches Driver 1
        self.assertEqual(inv["drivers"][0]["driver_name"], "Atlanta DC Stockout")
        self.assertEqual(inv["drivers"][0]["rank"], 1)
        
        # Verify Primary Recommendation matches Recommendation 1
        self.assertEqual(recs["recommendations"][0]["driver_id"], inv["drivers"][0]["driver_id"])
        self.assertGreater(recs["recommendations"][0]["expected_impact"]["revenue_recovery_usd"], 0)

if __name__ == "__main__":
    unittest.main()
