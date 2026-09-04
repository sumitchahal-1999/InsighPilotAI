"""
InsightPilot AI — Backend API Test Suite
Comprehensive unit and integration tests for all FastAPI endpoints using TestClient.
"""

import unittest
from fastapi.testclient import TestClient
from backend.app.main import app

class TestAPIEndpoints(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    # 1. Health Probe
    def test_health_endpoint(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "ok")
        self.assertEqual(data["service"], "insightpilot-api")
        self.assertIn("version", data)

    # 2. List All KPIs
    def test_list_kpis_endpoint(self):
        response = self.client.get("/api/v1/kpis")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["total_count"], 5)
        self.assertEqual(len(data["kpis"]), 5)
        kpi_ids = [k["id"] for k in data["kpis"]]
        self.assertIn("north_america_east_revenue", kpi_ids)
        self.assertIn("gross_margin", kpi_ids)
        self.assertIn("units_sold", kpi_ids)
        self.assertIn("distributor_orders", kpi_ids)
        self.assertIn("inventory_availability", kpi_ids)

    # 3. Single KPI State
    def test_get_revenue_kpi_state(self):
        response = self.client.get("/api/v1/kpis/north_america_east_revenue")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["id"], "north_america_east_revenue")
        self.assertAlmostEqual(data["previous_value"], 15430000.06, delta=100.0)
        self.assertAlmostEqual(data["current_value"], 14200000.05, delta=100.0)
        self.assertAlmostEqual(data["percent_change"], -7.97, places=1)
        self.assertEqual(data["materiality_status"], "CRITICAL_NEGATIVE_VARIANCE")

    # 4. Unknown KPI 404
    def test_unknown_kpi_404(self):
        response = self.client.get("/api/v1/kpis/non_existent_kpi")
        self.assertEqual(response.status_code, 404)
        data = response.json()
        self.assertIn("error", data)
        self.assertEqual(data["error"]["code"], "KPI_NOT_FOUND")

    # 5. Full Root Cause Investigation
    def test_investigation_endpoint(self):
        response = self.client.get("/api/v1/investigations/north_america_east_revenue")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("investigation_id", data)
        self.assertIn("timestamp", data)
        self.assertIn("kpi", data)
        self.assertIn("drivers", data)
        self.assertIn("overall", data)
        self.assertIn("lineage_graph", data)

        # Check KPI values
        self.assertEqual(data["kpi"]["id"], "north_america_east_revenue")
        self.assertAlmostEqual(data["kpi"]["percent_change"], -7.97, places=1)

        # Check drivers
        self.assertEqual(len(data["drivers"]), 4)
        total_contrib = sum(d["contribution_pct"] for d in data["drivers"])
        self.assertAlmostEqual(total_contrib, 100.0, places=1)

    # 6. Investigation Drivers List
    def test_investigation_drivers_endpoint(self):
        response = self.client.get("/api/v1/investigations/north_america_east_revenue/drivers")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["kpi_id"], "north_america_east_revenue")
        self.assertEqual(data["total_drivers"], 4)
        self.assertEqual(data["drivers"][0]["driver_id"], "atlanta_dc_stockout")
        self.assertEqual(data["drivers"][0]["rank"], 1)

    # 7. Decision Graph Endpoint
    def test_decision_graph_endpoint(self):
        response = self.client.get("/api/v1/investigations/north_america_east_revenue/decision-graph")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["kpi_id"], "north_america_east_revenue")
        self.assertEqual(data["total_columns"], 6)
        self.assertGreaterEqual(data["total_nodes_count"], 10)
        self.assertGreaterEqual(data["total_edges_count"], 10)

    # 8. Investigation Evidence List
    def test_investigation_evidence_endpoint(self):
        response = self.client.get("/api/v1/investigations/north_america_east_revenue/evidence")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["kpi_id"], "north_america_east_revenue")
        self.assertGreater(data["total_evidence_count"], 0)
        ev_ids = [e["evidence_id"] for e in data["evidence"]]
        self.assertIn("EVID_ERP_ATL_STOCKOUT_001", ev_ids)

    # 9. Global Evidence List & Filters
    def test_get_all_evidence_list(self):
        response = self.client.get("/api/v1/evidence")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["total_evidence_count"], 9)
        self.assertEqual(len(data["evidence"]), 9)

        # Domain filter
        erp_res = self.client.get("/api/v1/evidence?domain=ERP")
        self.assertEqual(erp_res.status_code, 200)
        self.assertGreater(erp_res.json()["total_evidence_count"], 0)

        # Search filter
        search_res = self.client.get("/api/v1/evidence?q=Atlanta")
        self.assertEqual(search_res.status_code, 200)
        self.assertGreater(search_res.json()["total_evidence_count"], 0)

    # 10. Single Evidence Node Lookup
    def test_single_evidence_endpoint(self):
        response = self.client.get("/api/v1/evidence/EVID_ERP_ATL_STOCKOUT_001")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["evidence_id"], "EVID_ERP_ATL_STOCKOUT_001")
        self.assertEqual(data["source_domain"], "ERP")
        self.assertIn("source_record_id", data)
        self.assertIn("lineage", data)
        self.assertTrue(data["lineage"]["verification_hash"].startswith("sha256:"))

    # 11. Unknown Evidence 404
    def test_unknown_evidence_404(self):
        response = self.client.get("/api/v1/evidence/EVID_NON_EXISTENT")
        self.assertEqual(response.status_code, 404)
        data = response.json()
        self.assertIn("error", data)
        self.assertEqual(data["error"]["code"], "EVIDENCE_NOT_FOUND")

    # 12. Evidence Lineage Trace
    def test_evidence_lineage_endpoint(self):
        response = self.client.get("/api/v1/evidence/EVID_ERP_ATL_STOCKOUT_001/lineage")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["evidence_id"], "EVID_ERP_ATL_STOCKOUT_001")
        self.assertEqual(data["kpi"], "north_america_east_revenue")
        self.assertEqual(data["driver"], "atlanta_dc_stockout")
        self.assertTrue(data["verification_hash"].startswith("sha256:"))

    # 13. Unknown Evidence Lineage 404
    def test_unknown_evidence_lineage_404(self):
        response = self.client.get("/api/v1/evidence/EVID_INVALID/lineage")
        self.assertEqual(response.status_code, 404)
        data = response.json()
        self.assertEqual(data["error"]["code"], "EVIDENCE_NOT_FOUND")

    # 14. Recommendations List
    def test_get_recommendations_endpoint(self):
        response = self.client.get("/api/v1/recommendations/north_america_east_revenue")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["kpi_id"], "north_america_east_revenue")
        self.assertEqual(data["total_recommendations"], 4)
        self.assertEqual(data["recommendations"][0]["recommendation_id"], "REC-2026-NAE-001")
        self.assertEqual(data["recommendations"][0]["priority"], "CRITICAL")

        # Default route test
        def_res = self.client.get("/api/v1/recommendations")
        self.assertEqual(def_res.status_code, 200)
        self.assertEqual(def_res.json()["kpi_id"], "north_america_east_revenue")

    # 15. Single Recommendation Detail
    def test_get_single_recommendation_endpoint(self):
        response = self.client.get("/api/v1/recommendations/north_america_east_revenue/REC-2026-NAE-001")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["recommendation_id"], "REC-2026-NAE-001")
        self.assertEqual(data["driver_id"], "atlanta_dc_stockout")
        self.assertIn("Emergency Inventory Transfer", data["action"])

    # 16. Simulation Baseline State
    def test_simulation_baseline_endpoint(self):
        response = self.client.get("/api/v1/simulations/baseline")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["baseline_availability_pct"], 79.4)
        self.assertEqual(data["baseline_revenue_usd"], 14200000.05)

    # 17. Simulation Inventory Availability Execution
    def test_simulation_execution_endpoint(self):
        response = self.client.post(
            "/api/v1/simulations/inventory-availability",
            json={"inventory_availability": 0.90}
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["baseline_value"], 79.4)
        self.assertEqual(data["scenario_value"], 90.0)
        self.assertEqual(data["availability_delta"], 10.6)
        self.assertGreater(data["estimated_recovery"]["revenue_recovery_usd"], 300000.0)
        self.assertEqual(data["confidence"]["label"], "HIGH")

        # Test unified alias /api/v1/simulations/run
        alias_res = self.client.post(
            "/api/v1/simulations/run",
            json={"target_availability_pct": 90.0}
        )
        self.assertEqual(alias_res.status_code, 200)
        self.assertEqual(alias_res.json()["scenario_value"], 90.0)

    # 18. Simulation Invalid Input 400
    def test_simulation_invalid_input_400(self):
        response = self.client.post(
            "/api/v1/simulations/inventory-availability",
            json={"inventory_availability": 150.0} # > 100%
        )
        self.assertEqual(response.status_code, 400)
        data = response.json()
        self.assertEqual(data["error"]["code"], "INVALID_SIMULATION_INPUT")

    # 19. Deterministic Repeated Requests
    def test_investigation_determinism(self):
        res1 = self.client.get("/api/v1/investigations/north_america_east_revenue").json()
        res2 = self.client.get("/api/v1/investigations/north_america_east_revenue").json()

        self.assertEqual(res1["kpi"]["current_value"], res2["kpi"]["current_value"])
        self.assertEqual(res1["kpi"]["previous_value"], res2["kpi"]["previous_value"])
        self.assertEqual(res1["overall"]["overall_confidence"], res2["overall"]["overall_confidence"])
        self.assertEqual(len(res1["drivers"]), len(res2["drivers"]))

    # 20. OpenAPI Docs Availability
    def test_openapi_docs_endpoint(self):
        response = self.client.get("/openapi.json")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("paths", data)
        self.assertIn("/health", data["paths"])
        self.assertIn("/api/v1/kpis", data["paths"])
        self.assertIn("/api/v1/investigations/{kpi_id}", data["paths"])
        self.assertIn("/api/v1/investigations/{kpi_id}/decision-graph", data["paths"])
        self.assertIn("/api/v1/evidence", data["paths"])
        self.assertIn("/api/v1/recommendations/{kpi_id}", data["paths"])
        self.assertIn("/api/v1/simulations/inventory-availability", data["paths"])
        self.assertIn("/api/v1/simulations/run", data["paths"])

    # 21. CORS Options Preflight
    def test_cors_preflight(self):
        response = self.client.options(
            "/api/v1/kpis",
            headers={
                "Origin": "http://localhost:3000",
                "Access-Control-Request-Method": "GET"
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers.get("access-control-allow-origin"), "http://localhost:3000")

if __name__ == "__main__":
    unittest.main()
