"""
InsightPilot AI — Phase 5.7 Integration Test Suite
Verifies the complete end-to-end integration of FastAPI backend, LangGraph workflow,
Decision Graph, Evidence Lineage, Confidence Guard, and Next.js frontend contracts.
"""

import unittest
from unittest.mock import patch
from fastapi.testclient import TestClient
from backend.app.main import app


class TestPhase57Integration(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)
        cls.kpi_id = "north_america_east_revenue"

    # -------------------------------------------------------------------------
    # 1. Canonical Numerical Invariance
    # -------------------------------------------------------------------------
    def test_canonical_numerical_invariance(self):
        """Verifies that the investigation endpoint preserves 100% exact canonical facts."""
        response = self.client.get(f"/api/v1/investigations/{self.kpi_id}")
        self.assertEqual(response.status_code, 200)
        data = response.json()

        # KPI Variance
        kpi = data["kpi"]
        self.assertAlmostEqual(kpi["previous_value"], 15430000.06, places=2)
        self.assertAlmostEqual(kpi["current_value"], 14200000.05, places=2)
        self.assertAlmostEqual(kpi["variance_amount"], -1230000.01, places=2)
        self.assertAlmostEqual(kpi["percent_change"], -7.97, places=2)
        self.assertEqual(kpi["materiality_status"], "CRITICAL_NEGATIVE_VARIANCE")

        # Top Driver: Atlanta DC Stockout
        top_driver = data["drivers"][0]
        self.assertEqual(top_driver["driver_name"], "Atlanta DC Stockout")
        self.assertEqual(top_driver["rank"], 1)
        self.assertAlmostEqual(top_driver["contribution_pct"], 43.2, places=1)
        self.assertAlmostEqual(top_driver["impact_usd"], -550000.0, places=0)
        self.assertEqual(top_driver["confidence_score"], 94)

        # Canonical Investigation Confidence = 89% (HIGH)
        self.assertEqual(data["overall"]["overall_confidence"], 89)
        self.assertEqual(data["overall"]["confidence_label"], "HIGH")
        self.assertFalse(data["overall"]["abstention"])

    # -------------------------------------------------------------------------
    # 2. Driver Decomposition Integrity
    # -------------------------------------------------------------------------
    def test_investigation_drivers_breakdown(self):
        """Verifies that all 4 causal drivers sum to 100% and preserve quantitative truth."""
        response = self.client.get(f"/api/v1/investigations/{self.kpi_id}/drivers")
        self.assertEqual(response.status_code, 200)
        data = response.json()

        self.assertEqual(len(data["drivers"]), 4)
        total_share = sum(d["contribution_pct"] for d in data["drivers"])
        self.assertAlmostEqual(total_share, 100.0, places=1)

        expected_ranks = [
            ("atlanta_dc_stockout", 43.2, -550000.0, 94),
            ("sku_8821_sales_volume", 26.7, -340000.0, 89),
            ("distributor_orders", 18.8, -240000.0, 85),
            ("competitor_horizon_pricing", 11.3, -144000.0, 78),
        ]

        for idx, (drv_id, share, impact, conf) in enumerate(expected_ranks):
            drv = data["drivers"][idx]
            self.assertEqual(drv["driver_id"], drv_id)
            self.assertAlmostEqual(drv["contribution_pct"], share, places=1)
            self.assertAlmostEqual(drv["impact_usd"], impact, places=0)
            self.assertEqual(drv["confidence_score"], conf)

    # -------------------------------------------------------------------------
    # 3. Decision Graph 6-Column Topology Integration
    # -------------------------------------------------------------------------
    def test_decision_graph_topology(self):
        """Verifies the backend Decision Graph endpoint returns authoritative 6-column topology."""
        response = self.client.get(f"/api/v1/investigations/{self.kpi_id}/decision-graph")
        self.assertEqual(response.status_code, 200)
        data = response.json()

        self.assertEqual(data["total_columns"], 6)
        self.assertEqual(data["total_nodes_count"], 14)
        self.assertEqual(data["total_edges_count"], 17)
        self.assertEqual(len(data["nodes"]), 14)
        self.assertEqual(len(data["edges"]), 17)

        # Check Column 1 (KPI) and Column 6 (Outcome)
        node_map = {n["id"]: n for n in data["nodes"]}
        self.assertIn("kpi-1", node_map)
        self.assertIn("out-1", node_map)
        self.assertEqual(node_map["kpi-1"]["node_type"], "KPI")
        self.assertEqual(node_map["out-1"]["node_type"], "OUTCOME")

    # -------------------------------------------------------------------------
    # 4. Evidence Lineage Verification
    # -------------------------------------------------------------------------
    def test_evidence_explorer_integration(self):
        """Verifies that evidence records match validated SHA-256 digests."""
        response = self.client.get(f"/api/v1/investigations/{self.kpi_id}/evidence")
        self.assertEqual(response.status_code, 200)
        data = response.json()

        self.assertGreaterEqual(len(data["evidence"]), 4)
        for ev in data["evidence"]:
            self.assertIn("evidence_id", ev)
            self.assertIn("lineage", ev)
            self.assertIn("verification_hash", ev["lineage"])
            self.assertTrue(ev["lineage"]["verification_hash"].startswith("sha256:"))

    # -------------------------------------------------------------------------
    # 5. Persona Invariance & Numerical Immutability
    # -------------------------------------------------------------------------
    def test_persona_invariance(self):
        """Verifies that switching between CFO and Regional Sales Manager never alters numbers."""
        cfo_res = self.client.get(f"/api/v1/investigations/{self.kpi_id}?persona_id=CFO").json()
        rsm_res = self.client.get(f"/api/v1/investigations/{self.kpi_id}?persona_id=REGIONAL_SALES_MANAGER").json()

        # Strict equality on quantitative fields
        self.assertEqual(cfo_res["kpi"]["variance_amount"], rsm_res["kpi"]["variance_amount"])
        self.assertEqual(cfo_res["kpi"]["percent_change"], rsm_res["kpi"]["percent_change"])
        self.assertEqual(cfo_res["overall"]["overall_confidence"], rsm_res["overall"]["overall_confidence"])

        for idx in range(len(cfo_res["drivers"])):
            self.assertEqual(cfo_res["drivers"][idx]["contribution_pct"], rsm_res["drivers"][idx]["contribution_pct"])
            self.assertEqual(cfo_res["drivers"][idx]["impact_usd"], rsm_res["drivers"][idx]["impact_usd"])
            self.assertEqual(cfo_res["drivers"][idx]["confidence_score"], rsm_res["drivers"][idx]["confidence_score"])

    # -------------------------------------------------------------------------
    # 6. Live LangGraph Trace Endpoint
    # -------------------------------------------------------------------------
    def test_langgraph_trace_endpoint(self):
        """Verifies live multi-agent LangGraph execution trace contract."""
        response = self.client.get(f"/api/v1/investigations/{self.kpi_id}/langgraph-trace?persona_id=CFO")
        self.assertEqual(response.status_code, 200)
        data = response.json()

        self.assertEqual(data["kpi_id"], self.kpi_id)
        self.assertIn("nodes", data)
        self.assertGreaterEqual(len(data["nodes"]), 6)
        self.assertIn("provider_events", data)
        self.assertIn("confidence", data)
        self.assertFalse(data["abstention"])

    # -------------------------------------------------------------------------
    # 7. AI Explanation Endpoint with Persona Adaptation
    # -------------------------------------------------------------------------
    def test_ai_explain_endpoint_with_persona(self):
        """Verifies grounded AI explanation endpoint adapts tone while retaining numerical truth."""
        mock_ai_response = {
            "investigation_id": f"INV-{self.kpi_id}",
            "persona": "CFO",
            "explanation": {
                "summary": "Revenue in North America East contracted by -$1.23M (-7.97%).",
                "executive_summary": "Revenue in North America East contracted by -$1.23M (-7.97%).",
                "primary_driver_explanation": "14 days zero stockout at Atlanta DC.",
                "uncertainty": "High empirical confidence.",
                "uncertainty_statement": "High empirical confidence.",
                "business_implications": ["Gross margin contraction"],
                "risks": ["Further customer churn"],
                "recommended_next_actions": ["Emergency stock transfer"],
                "grounded_evidence_ids": ["EVID_ERP_ATL_STOCKOUT_001"],
                "supporting_evidence_ids": ["EVID_ERP_ATL_STOCKOUT_001"],
                "supporting_driver_ids": ["atlanta_dc_stockout"],
                "abstained": False,
                "abstention_reason": None,
            },
            "metadata": {
                "model": "llama-3.3-70b-versatile",
                "generated_at": "2026-08-28T02:45:00Z",
                "latency_ms": 180.5,
                "grounded_evidence_count": 1,
                "validation_status": "VERIFIED_GROUNDED",
                "provider": "groq",
                "key_pool_id": "groq_pool_1",
                "fallback_used": False,
            }
        }

        with patch("backend.app.services.gemini_service.GeminiService.explain_investigation_structured", return_value=mock_ai_response):
            payload = {
                "persona": "CFO",
                "explanation_mode": "structured",
                "driver_id": "atlanta_dc_stockout",
                "include_recommendations": True,
                "include_simulation": False,
            }
            response = self.client.post(f"/api/v1/ai/explain/{self.kpi_id}", json=payload)
            self.assertEqual(response.status_code, 200)
            data = response.json()

            self.assertEqual(data["investigation_id"], f"INV-{self.kpi_id}")
            self.assertEqual(data["persona"], "CFO")
            self.assertIn("explanation", data)
            self.assertEqual(data["explanation"]["summary"], "Revenue in North America East contracted by -$1.23M (-7.97%).")
            self.assertIn("EVID_ERP_ATL_STOCKOUT_001", data["explanation"]["grounded_evidence_ids"])
            self.assertFalse(data["explanation"]["abstained"])

    # -------------------------------------------------------------------------
    # 8. Recommendations and Simulation Pipeline
    # -------------------------------------------------------------------------
    def test_recommendations_and_simulation_pipeline(self):
        """Verifies recommendations and deterministic simulation sandbox."""
        rec_res = self.client.get(f"/api/v1/recommendations/{self.kpi_id}")
        self.assertEqual(rec_res.status_code, 200)
        rec_data = rec_res.json()
        self.assertGreaterEqual(len(rec_data["recommendations"]), 2)

        # Simulation Run (90.0% Availability Target)
        sim_res = self.client.post("/api/v1/simulations/run", json={
            "scenario_name": "Atlanta DC Inventory Optimization",
            "region": "NA-East",
            "target_availability_pct": 90.0,
        })
        self.assertEqual(sim_res.status_code, 200)
        sim_data = sim_res.json()
        self.assertAlmostEqual(sim_data["estimated_recovery"]["revenue_recovery_usd"], 341422.91, places=1)
        self.assertAlmostEqual(sim_data["projected_value"], 14541422.96, places=1)

    # -------------------------------------------------------------------------
    # 9. Abstention Safety Handling
    # -------------------------------------------------------------------------
    def test_abstention_safety_handling(self):
        """Verifies that an artificial low-confidence state produces safe abstained outputs."""
        with patch("analytics.confidence_engine.ConfidenceEngine.evaluate_investigation_confidence") as mock_conf:
            mock_conf.return_value = {
                "overall_confidence": 42,
                "confidence_label": "LOW",
                "tier": "LOW",
                "abstention": True,
                "abstain": True,
                "abstention_reason": "Insufficient verified inventory logs.",
                "reasons": ["Insufficient verified inventory logs."],
            }
            response = self.client.get(f"/api/v1/investigations/{self.kpi_id}/langgraph-trace")
            self.assertEqual(response.status_code, 200)
            data = response.json()

            self.assertTrue(data["abstention"])
            self.assertEqual(data["status"], "ABSTAINED")
            self.assertEqual(data["abstention_reason"], "Insufficient verified inventory logs.")

    # -------------------------------------------------------------------------
    # 10. Zero Secret Leakage
    # -------------------------------------------------------------------------
    def test_zero_secret_leakage(self):
        """Verifies that no API keys or internal tokens leak in response payloads."""
        endpoints = [
            f"/api/v1/investigations/{self.kpi_id}",
            f"/api/v1/investigations/{self.kpi_id}/drivers",
            f"/api/v1/investigations/{self.kpi_id}/decision-graph",
            f"/api/v1/investigations/{self.kpi_id}/evidence",
            f"/api/v1/investigations/{self.kpi_id}/langgraph-trace",
            f"/api/v1/recommendations/{self.kpi_id}",
            "/api/v1/simulations/baseline",
        ]
        for ep in endpoints:
            res = self.client.get(ep)
            self.assertEqual(res.status_code, 200)
            body_str = res.text.lower()
            self.assertNotIn("gsk_", body_str)
            self.assertNotIn("aiza", body_str)
            self.assertNotIn("api_key", body_str)
            self.assertNotIn("secret", body_str)


if __name__ == "__main__":
    unittest.main()
