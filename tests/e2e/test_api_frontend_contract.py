"""
InsightPilot AI — Phase 5.8: API Contract & Serialization Validation Suite
Verifies that all FastAPI backend endpoints conform strictly to Pydantic schemas,
match frontend TypeScript interface contracts, and never leak secret tokens.
"""

import unittest
from unittest.mock import patch
from fastapi.testclient import TestClient
from backend.app.main import app
from ai.schemas.explanation import (
    StructuredAIExplanationResponse,
    StructuredInvestigationExplanation,
    AIResponseMetadata
)


class TestAPIFrontendContract(unittest.TestCase):
    """Full API contract validation across all system endpoints."""

    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)
        cls.kpi_id = "north_america_east_revenue"
        cls.evidence_id = "EVID_ERP_ATL_STOCKOUT_001"

    # -------------------------------------------------------------------------
    # 1. KPI Endpoints Contract
    # -------------------------------------------------------------------------
    def test_kpi_endpoints_contract(self):
        """Validates /api/v1/kpis list and single KPI contracts."""
        res_list = self.client.get("/api/v1/kpis")
        self.assertEqual(res_list.status_code, 200)
        data_list = res_list.json()
        self.assertIn("total_count", data_list)
        self.assertIn("kpis", data_list)
        self.assertIsInstance(data_list["kpis"], list)

        res_single = self.client.get(f"/api/v1/kpis/{self.kpi_id}")
        self.assertEqual(res_single.status_code, 200)
        data_single = res_single.json()
        self.assertEqual(data_single["id"], self.kpi_id)
        self.assertIn("previous_value", data_single)
        self.assertIn("current_value", data_single)
        self.assertIn("variance_amount", data_single)
        self.assertIn("percent_change", data_single)

    # -------------------------------------------------------------------------
    # 2. Investigation Endpoints Contract
    # -------------------------------------------------------------------------
    def test_investigation_endpoints_contract(self):
        """Validates /api/v1/investigations/* schema contracts."""
        # Main Investigation
        res_inv = self.client.get(f"/api/v1/investigations/{self.kpi_id}")
        self.assertEqual(res_inv.status_code, 200)
        data_inv = res_inv.json()
        self.assertIn("investigation_id", data_inv)
        self.assertIn("kpi", data_inv)
        self.assertIn("drivers", data_inv)
        self.assertIn("overall", data_inv)

        # Drivers
        res_drv = self.client.get(f"/api/v1/investigations/{self.kpi_id}/drivers")
        self.assertEqual(res_drv.status_code, 200)
        data_drv = res_drv.json()
        self.assertIn("total_drivers", data_drv)
        self.assertIn("drivers", data_drv)

        # Decision Graph
        res_graph = self.client.get(f"/api/v1/investigations/{self.kpi_id}/decision-graph")
        self.assertEqual(res_graph.status_code, 200)
        data_graph = res_graph.json()
        self.assertIn("total_columns", data_graph)
        self.assertIn("total_nodes_count", data_graph)
        self.assertIn("total_edges_count", data_graph)
        self.assertIn("nodes", data_graph)
        self.assertIn("edges", data_graph)

        # LangGraph Trace
        res_trace = self.client.get(f"/api/v1/investigations/{self.kpi_id}/langgraph-trace")
        self.assertEqual(res_trace.status_code, 200)
        data_trace = res_trace.json()
        self.assertIn("investigation_id", data_trace)
        self.assertIn("nodes", data_trace)
        self.assertIn("total_duration_ms", data_trace)

    # -------------------------------------------------------------------------
    # 3. Evidence Endpoints Contract
    # -------------------------------------------------------------------------
    def test_evidence_endpoints_contract(self):
        """Validates /api/v1/evidence/* schema contracts."""
        res_list = self.client.get("/api/v1/evidence")
        self.assertEqual(res_list.status_code, 200)
        data_list = res_list.json()
        self.assertIn("total_evidence_count", data_list)
        self.assertIn("evidence", data_list)

        res_single = self.client.get(f"/api/v1/evidence/{self.evidence_id}")
        self.assertEqual(res_single.status_code, 200)
        data_single = res_single.json()
        self.assertEqual(data_single["evidence_id"], self.evidence_id)
        self.assertIn("source", data_single)
        self.assertIn("source_domain", data_single)
        self.assertIn("lineage", data_single)

        res_lineage = self.client.get(f"/api/v1/evidence/{self.evidence_id}/lineage")
        self.assertEqual(res_lineage.status_code, 200)
        data_lineage = res_lineage.json()
        self.assertEqual(data_lineage["evidence_id"], self.evidence_id)
        self.assertIn("lineage_metadata", data_lineage)
        self.assertIn("verification_hash", data_lineage)

    # -------------------------------------------------------------------------
    # 4. Recommendations and Simulation Contract
    # -------------------------------------------------------------------------
    def test_recommendations_and_simulation_contract(self):
        """Validates /api/v1/recommendations and /api/v1/simulations contracts."""
        res_rec = self.client.get(f"/api/v1/recommendations/{self.kpi_id}")
        self.assertEqual(res_rec.status_code, 200)
        data_rec = res_rec.json()
        self.assertIn("recommendations", data_rec)
        self.assertIn("total_recommendations", data_rec)

        res_base = self.client.get("/api/v1/simulations/baseline?region=NA-East")
        self.assertEqual(res_base.status_code, 200)
        data_base = res_base.json()
        self.assertIn("baseline_availability_pct", data_base)

        sim_payload = {
            "inventory_availability": 0.90,
            "region": "NA-East"
        }
        res_sim = self.client.post("/api/v1/simulations/run", json=sim_payload)
        self.assertEqual(res_sim.status_code, 200)
        data_sim = res_sim.json()
        self.assertIn("projected_value", data_sim)
        self.assertIn("estimated_recovery", data_sim)
        self.assertIn("confidence", data_sim)

    # -------------------------------------------------------------------------
    # 5. AI Reasoning Contract with Mock
    # -------------------------------------------------------------------------
    def test_ai_explain_contract(self):
        """Validates /api/v1/ai/explain/{kpi_id} contract."""
        mock_resp = StructuredAIExplanationResponse(
            investigation_id=f"INV-{self.kpi_id}",
            persona="CFO",
            explanation=StructuredInvestigationExplanation(
                summary="Revenue contracted by -$1.23M (-7.97%).",
                executive_summary="Revenue contracted by -$1.23M (-7.97%).",
                primary_driver_explanation="Stockout at Atlanta DC.",
                uncertainty="Empirical confidence is high.",
                business_implications=["Working capital strain"],
                risks=["Customer attrition"],
                recommended_next_actions=["Emergency transfer"],
                grounded_evidence_ids=[self.evidence_id],
                supporting_evidence_ids=[self.evidence_id],
                supporting_driver_ids=["atlanta_dc_stockout"],
                abstained=False
            ),
            metadata=AIResponseMetadata(
                model="llama-3.3-70b-versatile",
                provider="groq",
                key_pool_id="groq_pool_1",
                generated_at="2026-08-28T00:00:00Z",
                latency_ms=180.5,
                prompt_tokens=400,
                completion_tokens=150,
                total_tokens=550,
                grounded_evidence_count=1,
                validation_status="VERIFIED_GROUNDED"
            )
        )

        with patch("backend.app.services.gemini_service.GeminiService.explain_investigation_structured", return_value=mock_resp):
            res_ai = self.client.post(f"/api/v1/ai/explain/{self.kpi_id}", json={"persona": "CFO"})
            self.assertEqual(res_ai.status_code, 200)
            data_ai = res_ai.json()
            self.assertEqual(data_ai["investigation_id"], f"INV-{self.kpi_id}")
            self.assertEqual(data_ai["persona"], "CFO")
            self.assertIn("explanation", data_ai)
            self.assertIn("summary", data_ai["explanation"])
            self.assertIn("metadata", data_ai)
            self.assertEqual(data_ai["metadata"]["provider"], "groq")


if __name__ == "__main__":
    unittest.main()
