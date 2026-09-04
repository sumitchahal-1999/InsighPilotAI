"""
Phase 8.5: Production Environment Validation, Smoke Testing & Go-Live Readiness Test Suite
Project: InsightPilot AI
Competition: Accenture Innovation Challenge 2026 (Track 3: BusinessIntelligence.ai)

Validates:
1. Existence of all 10 Phase 8.5 operational deliverables in docs/operations/
2. Liveness and 12-subsystem deep readiness health probes
3. End-to-end critical API journey (KPIs -> Drivers -> Evidence -> Graph -> Recommendations -> Simulation)
4. Degraded mode fallback synthesis when external AI APIs are unconfigured
5. Coexistence of security headers, request correlation, and sanitized error responses
6. Preservation of canonical invariants in operations documentation
7. Complete navigation coverage in docs/operations/README.md
"""

import unittest
import os
from fastapi.testclient import TestClient
from backend.app.main import app

class TestPhase85ProductionReadiness(unittest.TestCase):

    def setUp(self):
        self.project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
        self.operations_dir = os.path.join(self.project_root, "docs", "operations")
        self.client = TestClient(app)

    # --------------------------------------------------------------------------
    # Test 1: Required Phase 8.5 Deliverables Existence
    # --------------------------------------------------------------------------
    def test_phase85_deliverables_exist(self):
        """Verify that all 10 required Phase 8.5 operations documents exist on disk."""
        required_files = [
            "ENVIRONMENT_READINESS_AUDIT.md",
            "CLEAN_START_SMOKE_TEST.md",
            "HEALTH_AND_READINESS_VALIDATION.md",
            "CRITICAL_JOURNEY_SMOKE_TEST.md",
            "DEGRADED_MODE_AND_FAILURE_HANDLING.md",
            "PRODUCTION_SECURITY_REVALIDATION.md",
            "FRONTEND_PRODUCTION_SMOKE_TEST.md",
            "DEPLOYMENT_HANDOFF_RUNBOOK.md",
            "GO_LIVE_RISK_REGISTER.md",
            "PHASE_85_GO_LIVE_READINESS_SIGN_OFF.md",
            "README.md",
        ]

        for fname in required_files:
            fpath = os.path.join(self.operations_dir, fname)
            self.assertTrue(os.path.isfile(fpath), f"Missing Phase 8.5 deliverable: {fname}")

    # --------------------------------------------------------------------------
    # Test 2: Clean-Start Health & Readiness Probes
    # --------------------------------------------------------------------------
    def test_clean_start_health_and_readiness(self):
        """Verify that process liveness and 12-subsystem readiness respond successfully."""
        res_health = self.client.get("/health")
        self.assertEqual(res_health.status_code, 200)
        self.assertEqual(res_health.json().get("status"), "ok")
        self.assertEqual(res_health.json().get("version"), "2.0.0")

        res_readiness = self.client.get("/api/v1/demo/readiness")
        self.assertEqual(res_readiness.status_code, 200)
        data = res_readiness.json()
        self.assertTrue(data.get("submission_ready"))
        self.assertIn("subsystems", data)
        self.assertTrue(data["subsystems"].get("analytics_parity"))
        self.assertTrue(data["subsystems"].get("evidence_lineage_ready"))

    # --------------------------------------------------------------------------
    # Test 3: Critical API Smoke Journey
    # --------------------------------------------------------------------------
    def test_critical_api_journey(self):
        """Verify the complete end-to-end analytical pipeline across all core API endpoints."""
        # 1. KPIs Anomaly
        res_kpis = self.client.get("/api/v1/kpis")
        self.assertEqual(res_kpis.status_code, 200)
        kpi_data = res_kpis.json()
        self.assertGreater(len(kpi_data), 0)

        # 2. Causal Drivers Decomposition
        res_drivers = self.client.get("/api/v1/investigations/north_america_east_revenue/drivers")
        self.assertEqual(res_drivers.status_code, 200)
        drivers_data = res_drivers.json()
        self.assertIn("drivers", drivers_data)
        top_driver = drivers_data["drivers"][0]
        self.assertEqual(top_driver.get("driver_name"), "Atlanta DC Stockout")
        self.assertEqual(top_driver.get("contribution_pct"), 43.2)
        self.assertEqual(top_driver.get("impact_usd"), -550000.00)

        # 3. Evidence Explorer
        res_evidence = self.client.get("/api/v1/evidence")
        self.assertEqual(res_evidence.status_code, 200)
        evidence_list = res_evidence.json().get("evidence", [])
        self.assertEqual(len(evidence_list), 9)

        # 4. Decision Graph Topology
        res_graph = self.client.get("/api/v1/investigations/north_america_east_revenue/decision-graph")
        self.assertEqual(res_graph.status_code, 200)
        graph_data = res_graph.json()
        self.assertEqual(len(graph_data.get("nodes", [])), 14)
        self.assertEqual(len(graph_data.get("edges", [])), 17)

        # 5. Recommendations
        res_recs = self.client.get("/api/v1/recommendations/north_america_east_revenue")
        self.assertEqual(res_recs.status_code, 200)
        recs = res_recs.json().get("recommendations", [])
        self.assertGreaterEqual(len(recs), 2)
        self.assertEqual(recs[0]["expected_impact"].get("revenue_recovery_usd"), 484000.00)


        # 6. What-If Simulation
        res_sim = self.client.post("/api/v1/simulations/run", json={
            "scenario_name": "Inventory Elasticity",
            "region": "NA-East",
            "target_availability_pct": 90.0
        })
        self.assertEqual(res_sim.status_code, 200)
        sim_data = res_sim.json()
        self.assertAlmostEqual(sim_data["estimated_recovery"].get("revenue_recovery_usd"), 341422.91, places=1)


    # --------------------------------------------------------------------------
    # Test 4: Degraded Mode Fallback Synthesis in Demo Investigation
    # --------------------------------------------------------------------------
    def test_degraded_mode_synthesis(self):
        """Verify that demo investigation runs deterministically when external keys are unconfigured."""
        res_demo = self.client.get("/api/v1/demo/investigation/north_america_east_revenue")
        self.assertEqual(res_demo.status_code, 200)
        data = res_demo.json()
        self.assertIn("demo_narrative", data)
        self.assertIn("ai_explanation", data)
        self.assertIn("ai_source_indicator", data)
        self.assertEqual(data.get("kpi_id"), "north_america_east_revenue")
        self.assertIn("movement", data)
        self.assertEqual(data["movement"].get("variance"), -1230000.01)
        self.assertIn("Atlanta DC Stockout", str(data["ai_explanation"]))

    # --------------------------------------------------------------------------
    # Test 5: Coexistence of Security Headers and Observability
    # --------------------------------------------------------------------------
    def test_security_and_observability_coexistence(self):
        """Verify that security headers and correlation telemetry operate harmoniously."""
        res = self.client.get("/api/v1/kpis")
        self.assertEqual(res.status_code, 200)
        self.assertIn("X-Request-ID", res.headers)
        self.assertIn("X-Response-Time-Ms", res.headers)
        self.assertEqual(res.headers.get("X-Content-Type-Options"), "nosniff")
        self.assertEqual(res.headers.get("X-Frame-Options"), "DENY")
        self.assertIn("no-store", res.headers.get("Cache-Control", ""))

    # --------------------------------------------------------------------------
    # Test 6: Canonical Invariants Preservation in Sign-Off
    # --------------------------------------------------------------------------
    def test_canonical_invariants_in_operations_sign_off(self):
        """Verify that PHASE_85_GO_LIVE_READINESS_SIGN_OFF.md preserves locked metrics."""
        fpath = os.path.join(self.operations_dir, "PHASE_85_GO_LIVE_READINESS_SIGN_OFF.md")
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn("Deterministic systems own quantitative truth", content)
        self.assertIn("Atlanta DC Stockout", content)
        self.assertIn("+$484,000.00", content)
        self.assertIn("+$757,600.00", content)

    # --------------------------------------------------------------------------
    # Test 7: Operations README Navigation Links Integrity
    # --------------------------------------------------------------------------
    def test_operations_readme_links(self):
        """Verify that docs/operations/README.md links to all 10 documents."""
        fpath = os.path.join(self.operations_dir, "README.md")
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()

        expected_links = [
            "ENVIRONMENT_READINESS_AUDIT.md",
            "CLEAN_START_SMOKE_TEST.md",
            "HEALTH_AND_READINESS_VALIDATION.md",
            "CRITICAL_JOURNEY_SMOKE_TEST.md",
            "DEGRADED_MODE_AND_FAILURE_HANDLING.md",
            "PRODUCTION_SECURITY_REVALIDATION.md",
            "FRONTEND_PRODUCTION_SMOKE_TEST.md",
            "DEPLOYMENT_HANDOFF_RUNBOOK.md",
            "GO_LIVE_RISK_REGISTER.md",
            "PHASE_85_GO_LIVE_READINESS_SIGN_OFF.md",
        ]

        for link in expected_links:
            self.assertIn(link, content, f"Operations README missing link to: {link}")

if __name__ == "__main__":
    unittest.main()
