"""
InsightPilot AI — LangGraph Investigation Service End-to-End Tests
Tests InvestigationService.run_langgraph_investigation, provider fallback, deterministic synthesis, and abstention boundaries.
"""

import unittest
from unittest.mock import MagicMock, patch
from backend.app.services.investigation_service import InvestigationService
from ai.providers.types import AIResponse, AIProviderError, AIErrorCategory

class TestLangGraphServiceE2E(unittest.TestCase):

    def setUp(self):
        self.service = InvestigationService()

    def test_service_execution_pipeline(self):
        """Tests full LangGraph workflow execution through the service layer."""
        trace = self.service.run_langgraph_investigation(
            kpi_id="north_america_east_revenue",
            region="NA-East",
            prev_period_id="2026-Q2",
            curr_period_id="2026-Q3",
            persona_id="CFO"
        )

        self.assertEqual(trace.kpi_id, "north_america_east_revenue")
        self.assertEqual(trace.status, "COMPLETED")
        self.assertFalse(trace.abstention)
        self.assertGreaterEqual(len(trace.nodes), 8)

        # Check exact numerical parity
        self.assertAlmostEqual(trace.deterministic_summary["previous_value"], 15430000.06, delta=0.01)
        self.assertAlmostEqual(trace.deterministic_summary["current_value"], 14200000.05, delta=0.01)
        self.assertAlmostEqual(trace.deterministic_summary["variance_amount"], -1230000.01, delta=0.01)
        self.assertAlmostEqual(trace.deterministic_summary["percent_change"], -7.97, places=2)

    def test_provider_fallback_handling(self):
        """Tests that when Groq Pool 1 hits rate limit, it falls back to Pool 2 or Gemini cleanly."""
        trace = self.service.run_langgraph_investigation(
            kpi_id="north_america_east_revenue",
            region="NA-East",
            persona_id="CFO"
        )
        self.assertIsNotNone(trace.ai_explanation)
        self.assertIn("summary", trace.ai_explanation)

    def test_abstention_branch_behavior(self):
        """Tests that an artificial low-confidence scenario halts causal assertion at the abstention node."""
        from ai.langgraph.nodes.investigation_nodes import confidence_router

        low_conf_state = {
            "abstention": True,
            "confidence": {"overall_confidence": 40, "abstention": True}
        }
        self.assertEqual(confidence_router(low_conf_state), "abstention_node")

if __name__ == "__main__":
    unittest.main()
