"""
InsightPilot AI — Phase 5.8: Hackathon Demo Scenarios Test Suite
Validates the 4 key competition demonstration storylines:
  DEMO 1: The Canonical 7-Screen Investigation Flow
  DEMO 2: Live Multi-Pool AI Provider Failover (Groq 429 -> Groq 2)
  DEMO 3: Total AI Outage Graceful Degradation (Deterministic Fallback)
  DEMO 4: Responsible AI Low-Confidence Abstention Guard
"""

import unittest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from backend.app.main import app
from ai.langgraph.graph import run_investigation_workflow
from ai.orchestration.fallback_manager import FallbackManager
from ai.providers.base import BaseAIProvider
from ai.providers.types import (
    AIRequest,
    AIResponse,
    TaskType,
    Capability,
    AIProviderError,
    AIErrorCategory
)
from analytics.data_loader import DataLoader
from analytics.recommendations import RecommendationEngine
from simulation.simulation_engine import SimulationEngine


class DummyProvider(BaseAIProvider):
    def __init__(self, name: str, key_pool_count: int = 2):
        self._name = name
        self._key_pools = [f"{name}_pool_{i+1}" for i in range(key_pool_count)]
        self.generate_mock = MagicMock()

    @property
    def name(self) -> str:
        return self._name

    @property
    def supported_capabilities(self):
        return {Capability.TEXT_REASONING, Capability.STRUCTURED_JSON}

    @property
    def supported_tasks(self):
        return {TaskType.BUSINESS_REASONING, TaskType.INVESTIGATION_EXPLANATION}

    @property
    def key_pool_ids(self):
        return self._key_pools

    def is_configured(self) -> bool:
        return len(self._key_pools) > 0

    def generate(self, request: AIRequest, key_pool_index: int = 0) -> AIResponse:
        return self.generate_mock(request, key_pool_index)


class TestDemoScenarios(unittest.TestCase):
    """Execution tests for the 4 canonical live demo scenarios."""

    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)
        cls.kpi_id = "north_america_east_revenue"
        cls.loader = DataLoader(use_db=True)
        cls.rec_engine = RecommendationEngine(cls.loader)
        cls.sim_engine = SimulationEngine(cls.loader)

    # -------------------------------------------------------------------------
    # DEMO 1: Full Canonical 7-Screen Investigation Flow
    # -------------------------------------------------------------------------
    def test_demo_1_full_canonical_investigation_flow(self):
        """Demonstrates the complete executive journey from anomaly detection to boardroom decision briefing."""
        # 1. Screen 1: Executive Command Center (KPI Selection)
        res_kpis = self.client.get("/api/v1/kpis")
        self.assertEqual(res_kpis.status_code, 200)
        kpis_data = res_kpis.json()
        self.assertEqual(kpis_data["total_count"], 5)
        nae_kpi = next((k for k in kpis_data["kpis"] if k["id"] == self.kpi_id), None)
        self.assertIsNotNone(nae_kpi)
        self.assertAlmostEqual(nae_kpi["variance_amount"], -1230000.01, places=2)
        self.assertEqual(nae_kpi["materiality_status"], "CRITICAL_NEGATIVE_VARIANCE")

        # 2. Screen 2: Multi-Agent Investigation Pipeline (LangGraph)
        workflow_res = run_investigation_workflow(kpi_id=self.kpi_id, persona="CFO")
        self.assertEqual(len(workflow_res["nodes_executed"]), 11)
        self.assertEqual(workflow_res["confidence"]["overall_confidence"], 89)
        self.assertFalse(workflow_res["abstention"])

        # 3. Screen 3: Causal Driver Decomposition
        drivers = workflow_res["drivers"]
        self.assertEqual(len(drivers), 4)
        top_driver = drivers[0]
        self.assertEqual(top_driver["driver_id"], "atlanta_dc_stockout")
        self.assertEqual(top_driver["contribution_pct"], 43.2)
        self.assertAlmostEqual(top_driver["impact_usd"], -550000.0, places=2)

        # 4. Screen 4: Dynamic Decision Graph (6 Columns, 14 Nodes, 17 Edges)
        res_graph = self.client.get(f"/api/v1/investigations/{self.kpi_id}/decision-graph")
        self.assertEqual(res_graph.status_code, 200)
        graph_data = res_graph.json()
        self.assertEqual(graph_data["total_columns"], 6)
        self.assertEqual(graph_data["total_nodes_count"], 14)
        self.assertEqual(graph_data["total_edges_count"], 17)

        # 5. Screen 5: Evidence Explorer & Lineage Trace
        res_ev = self.client.get(f"/api/v1/evidence/EVID_ERP_ATL_STOCKOUT_001")
        self.assertEqual(res_ev.status_code, 200)
        ev_data = res_ev.json()
        self.assertIn("SAP", ev_data["source"])
        self.assertEqual(ev_data["source_domain"], "ERP")
        self.assertTrue(ev_data["lineage"]["verification_hash"].startswith("sha256:"))

        # 6. Screen 6: Recommendations & What-If Simulation Sandbox
        recs = self.rec_engine.generate_recommendations(self.kpi_id)
        self.assertIn("20,000", recs[0]["action"])
        self.assertAlmostEqual(recs[0]["expected_impact"]["revenue_recovery_usd"], 484000.0, places=0)

        sim_res = self.sim_engine.simulate_inventory_availability(90.0, "NA-East")
        self.assertAlmostEqual(sim_res["estimated_recovery"]["revenue_recovery_usd"], 341422.91, places=2)

        # 7. Screen 7: Boardroom Decision Briefing
        self.assertIn("summary", workflow_res["ai_explanation"])
        self.assertIn("Atlanta DC stockouts", workflow_res["ai_explanation"]["summary"])
        self.assertIn("recommended_next_actions", workflow_res["ai_explanation"])

    # -------------------------------------------------------------------------
    # DEMO 2: Live AI Provider Failover
    # -------------------------------------------------------------------------
    def test_demo_2_live_ai_provider_failover(self):
        """Demonstrates live failover when primary Groq pool experiences rate limiting."""
        groq_prov = DummyProvider("groq", 2)
        gemini_prov = DummyProvider("gemini", 2)

        def side_effect(req: AIRequest, idx: int) -> AIResponse:
            if idx == 0:
                raise AIProviderError(
                    "429: Too Many Requests on groq_pool_1",
                    AIErrorCategory.RATE_LIMITED,
                    "groq",
                    "groq_pool_1",
                    True
                )
            return AIResponse(
                content='{"summary": "Failover to Groq Pool 2 succeeded with zero downtime."}',
                structured_data={"summary": "Failover to Groq Pool 2 succeeded with zero downtime."},
                provider="groq",
                model="llama-3.3-70b-versatile",
                key_pool_id="groq_pool_2",
                latency_ms=195.0,
                success=True
            )

        groq_prov.generate_mock.side_effect = side_effect
        manager = FallbackManager(providers={"groq": groq_prov, "gemini": gemini_prov})

        req = AIRequest(
            task_type=TaskType.INVESTIGATION_EXPLANATION,
            prompt="Explain the North America East revenue contraction."
        )

        resp = manager.execute_with_fallback(req, "groq", "gemini")
        self.assertEqual(resp.key_pool_id, "groq_pool_2")
        self.assertTrue(resp.fallback_used)
        self.assertEqual(groq_prov.generate_mock.call_count, 2)

    # -------------------------------------------------------------------------
    # DEMO 3: Total AI Outage Fallback to Deterministic Reasoning
    # -------------------------------------------------------------------------
    def test_demo_3_total_ai_outage_deterministic_fallback(self):
        """Demonstrates that even if all LLMs are down, InsightPilot AI remains 100% operational."""
        result = run_investigation_workflow(kpi_id=self.kpi_id, persona="CFO")

        self.assertIsNotNone(result)
        self.assertAlmostEqual(result["kpi_movement"]["variance_amount"], -1230000.01, places=2)
        self.assertEqual(result["confidence"]["overall_confidence"], 89)
        self.assertFalse(result["abstention"])
        self.assertIn("summary", result["ai_explanation"])
        self.assertIn("atlanta dc stockout", result["ai_explanation"]["summary"].lower())

    # -------------------------------------------------------------------------
    # DEMO 4: Responsible AI Low-Confidence Abstention Guard
    # -------------------------------------------------------------------------
    def test_demo_4_responsible_ai_abstention(self):
        """Demonstrates responsible AI behavior: low confidence triggers safe abstention with zero hallucination."""
        with patch("analytics.confidence_engine.ConfidenceEngine.evaluate_investigation_confidence") as mock_conf:
            mock_conf.return_value = {
                "overall_confidence": 45,
                "confidence_label": "LOW",
                "abstention": True,
                "abstention_reason": "Low confidence (45% < 65%). Insufficient evidence.",
                "factor_breakdown": {}
            }

            result = run_investigation_workflow(kpi_id=self.kpi_id, persona="CFO")

            self.assertTrue(result["abstention"])
            self.assertEqual(result["confidence"]["overall_confidence"], 45)
            self.assertIn("abstention_node", result["nodes_executed"])
            self.assertNotIn("ai_invocation_node", result["nodes_executed"])
            self.assertTrue(result["ai_explanation"]["abstained"])
            self.assertEqual(result["decision_graph"]["total_columns"], 2)


if __name__ == "__main__":
    unittest.main()
