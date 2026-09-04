"""
InsightPilot AI — Phase 5.4 LangGraph AI Nodes Integration Tests
Tests LangGraph AI explanation node integration, provider failover, grounding validation,
deterministic fallback, low-confidence abstention, persona synthesis, and secret safety.
"""

import unittest
from unittest.mock import MagicMock, patch
from ai.langgraph.graph import run_investigation_workflow, investigation_graph_app
from ai.langgraph.nodes.investigation_nodes import (
    prepare_grounding_node,
    build_grounded_context_node,
    ai_invocation_node,
    ai_explanation_node,
    abstention_node
)
from ai.providers.types import (
    AIRequest,
    AIResponse,
    TaskType,
    Capability,
    AIProviderError,
    AIErrorCategory
)
from ai.providers.groq_provider import GroqProvider
from ai.providers.gemini_provider import GeminiProvider
from ai.orchestration.provider_router import AIProviderRouter

class TestPhase54LangGraphAINodes(unittest.TestCase):

    def setUp(self):
        self.kpi_id = "north_america_east_revenue"
        self.region = "NA-East"

    # -------------------------------------------------------------------------
    # TEST A: Successful Groq Explanation & Grounding
    # -------------------------------------------------------------------------
    def test_successful_groq_explanation(self):
        """Tests that a valid Groq response passes post-LLM validation and updates state."""
        mock_groq_json = {
            "summary": "Revenue contracted 7.97% primarily due to the Atlanta DC stockout bottleneck.",
            "primary_driver_explanation": "Atlanta DC stockout restricted $550K in customer orders.",
            "secondary_driver_explanation": "SKU-8821 sales volume and distributor deferrals added secondary pressure.",
            "supporting_driver_ids": ["atlanta_dc_stockout"],
            "supporting_evidence_ids": ["EVID_ERP_ATL_STOCKOUT_001"],
            "business_implications": ["-$550K direct revenue constraint in NA-East"],
            "risks": ["Potential market share loss to Horizon Foods promotion"],
            "recommended_next_actions": ["Transfer 20,000 units from Charlotte Hub"],
            "uncertainty": "Competitor promotional pricing impact carries residual variance bounds.",
            "abstained": False
        }

        mock_groq = MagicMock(spec=GroqProvider)
        mock_groq.name = "groq"
        mock_groq.is_configured.return_value = True
        mock_groq.key_pool_ids = ["groq_pool_1"]
        mock_groq.generate.return_value = AIResponse(
            content=str(mock_groq_json),
            parsed_json=mock_groq_json,
            provider="groq",
            model="llama-3.3-70b-versatile",
            key_pool_id="groq_pool_1",
            latency_ms=160.0
        )

        with patch("ai.langgraph.nodes.investigation_nodes.provider_router", AIProviderRouter(groq_provider=mock_groq)):
            state = run_investigation_workflow(
                kpi_id=self.kpi_id,
                region=self.region,
                persona="CFO"
            )

            self.assertEqual(state["kpi_id"], self.kpi_id)
            self.assertFalse(state["abstention"])
            self.assertIsNotNone(state.get("ai_explanation"))
            self.assertEqual(state["provider_metadata"]["provider"], "groq")
            self.assertEqual(state["provider_metadata"]["key_pool_id"], "groq_pool_1")
            self.assertIn("ai_invocation_node", state["nodes_executed"])
            self.assertIn("EVID_ERP_ATL_STOCKOUT_001", state["ai_explanation"]["grounded_evidence_ids"])

    # -------------------------------------------------------------------------
    # TEST B: Groq Failover (Key 1 -> Key 2)
    # -------------------------------------------------------------------------
    def test_groq_key1_failover_to_key2(self):
        """Tests that Groq Key 1 rate limit fails over seamlessly to Groq Key 2 in LangGraph."""
        mock_groq = MagicMock(spec=GroqProvider)
        mock_groq.name = "groq"
        mock_groq.is_configured.return_value = True
        mock_groq.key_pool_ids = ["groq_pool_1", "groq_pool_2"]

        def generate_mock(req, key_pool_index=0):
            if key_pool_index == 0:
                raise AIProviderError(
                    "Rate limit exceeded on Groq Key 1",
                    error_category=AIErrorCategory.RATE_LIMITED,
                    provider="groq",
                    key_pool_id="groq_pool_1",
                    retryable=True
                )
            return AIResponse(
                content='{"summary": "Successfully recovered via Groq Key 2", "primary_driver_explanation": "Atlanta stockout", "uncertainty": "Standard bounds", "abstained": false}',
                parsed_json={
                    "summary": "Successfully recovered via Groq Key 2",
                    "primary_driver_explanation": "Atlanta stockout",
                    "supporting_evidence_ids": ["EVID_ERP_ATL_STOCKOUT_001"],
                    "uncertainty": "Standard bounds",
                    "abstained": False
                },
                provider="groq",
                model="llama-3.3-70b-versatile",
                key_pool_id="groq_pool_2",
                latency_ms=145.0
            )

        mock_groq.generate.side_effect = generate_mock

        with patch("ai.langgraph.nodes.investigation_nodes.provider_router", AIProviderRouter(groq_provider=mock_groq)):
            state = run_investigation_workflow(
                kpi_id=self.kpi_id,
                persona="CFO"
            )

            self.assertTrue(state["provider_metadata"]["fallback_used"])
            self.assertEqual(state["provider_metadata"]["key_pool_id"], "groq_pool_2")

    # -------------------------------------------------------------------------
    # TEST C: Cross-Provider Fallback (Groq -> Gemini)
    # -------------------------------------------------------------------------
    def test_groq_exhausted_falls_back_to_gemini(self):
        """Tests that when all Groq pools fail, workflow falls back to Gemini."""
        mock_groq = MagicMock(spec=GroqProvider)
        mock_groq.name = "groq"
        mock_groq.is_configured.return_value = True
        mock_groq.key_pool_ids = ["groq_pool_1"]
        mock_groq.generate.side_effect = AIProviderError(
            "Groq quota exceeded",
            error_category=AIErrorCategory.QUOTA_EXCEEDED,
            provider="groq",
            key_pool_id="groq_pool_1",
            retryable=True
        )

        mock_gemini = MagicMock(spec=GeminiProvider)
        mock_gemini.name = "gemini"
        mock_gemini.is_configured.return_value = True
        mock_gemini.key_pool_ids = ["gemini_pool_1"]
        mock_gemini.generate.return_value = AIResponse(
            content='{"summary": "Gemini fallback explanation", "primary_driver_explanation": "Atlanta stockout", "uncertainty": "Standard bounds", "abstained": false}',
            parsed_json={
                "summary": "Gemini fallback explanation",
                "primary_driver_explanation": "Atlanta stockout",
                "supporting_evidence_ids": ["EVID_ERP_ATL_STOCKOUT_001"],
                "uncertainty": "Standard bounds",
                "abstained": False
            },
            provider="gemini",
            model="gemini-2.5-flash",
            key_pool_id="gemini_pool_1",
            latency_ms=310.0
        )

        with patch("ai.langgraph.nodes.investigation_nodes.provider_router", AIProviderRouter(groq_provider=mock_groq, gemini_provider=mock_gemini)):
            state = run_investigation_workflow(
                kpi_id=self.kpi_id,
                persona="CFO"
            )

            self.assertEqual(state["provider_metadata"]["provider"], "gemini")
            self.assertEqual(state["provider_metadata"]["key_pool_id"], "gemini_pool_1")
            self.assertTrue(state["provider_metadata"]["fallback_used"])

    # -------------------------------------------------------------------------
    # TEST D: All Providers Unavailable -> Deterministic Fallback Synthesis
    # -------------------------------------------------------------------------
    def test_all_providers_unavailable_deterministic_fallback(self):
        """When all external AI providers fail, workflow gracefully degrades to deterministic synthesis."""
        mock_groq = MagicMock(spec=GroqProvider)
        mock_groq.is_configured.return_value = False
        mock_gemini = MagicMock(spec=GeminiProvider)
        mock_gemini.is_configured.return_value = False

        with patch("ai.langgraph.nodes.investigation_nodes.provider_router", AIProviderRouter(groq_provider=mock_groq, gemini_provider=mock_gemini)):
            state = run_investigation_workflow(
                kpi_id=self.kpi_id,
                persona="CFO"
            )

            self.assertIsNotNone(state.get("ai_explanation"))
            self.assertEqual(state["provider_metadata"]["provider"], "deterministic_fallback")
            self.assertEqual(state["provider_metadata"]["model"], "rule_based_engine")
            # Mathematical truth remains completely intact
            self.assertAlmostEqual(state["kpi_movement"]["variance_amount"], -1230000.01, delta=0.01)

    # -------------------------------------------------------------------------
    # TEST E: Low-Confidence Investigation (< 65%) -> Abstention Path
    # -------------------------------------------------------------------------
    def test_low_confidence_routes_to_abstention(self):
        """When analytical confidence is below 65%, workflow routes strictly to abstention node."""
        with patch("analytics.confidence_engine.ConfidenceEngine.evaluate_investigation_confidence") as mock_conf:
            mock_conf.return_value = {
                "overall_confidence": 42,
                "confidence_label": "LOW",
                "tier": "LOW",
                "abstention": True,
                "abstain": True,
                "abstention_reason": "Insufficient verified inventory logs."
            }

            state = run_investigation_workflow(
                kpi_id=self.kpi_id,
                persona="CFO"
            )

            self.assertTrue(state["abstention"])
            self.assertIn("abstention_node", state["nodes_executed"])
            self.assertNotIn("ai_invocation_node", state["nodes_executed"])
            self.assertTrue(state["ai_explanation"]["abstained"])
            self.assertEqual(state["ai_explanation"]["abstention_reason"], "Insufficient verified inventory logs.")

    # -------------------------------------------------------------------------
    # TEST F: Hallucinated Evidence ID -> Deterministic Fallback
    # -------------------------------------------------------------------------
    def test_hallucinated_evidence_triggers_safe_fallback(self):
        """When LLM returns a hallucinated evidence ID, grounding failure triggers safe deterministic fallback."""
        mock_groq = MagicMock(spec=GroqProvider)
        mock_groq.name = "groq"
        mock_groq.is_configured.return_value = True
        mock_groq.key_pool_ids = ["groq_pool_1"]
        mock_groq.generate.return_value = AIResponse(
            content='{"summary": "Fake evidence hallucination", "supporting_evidence_ids": ["FAKE-EVIDENCE-999"]}',
            parsed_json={
                "summary": "Fake evidence hallucination",
                "primary_driver_explanation": "Explanation",
                "supporting_evidence_ids": ["FAKE-EVIDENCE-999"],
                "uncertainty": "Standard",
                "abstained": False
            },
            provider="groq",
            model="llama-3.3-70b-versatile",
            key_pool_id="groq_pool_1",
            latency_ms=150.0
        )

        with patch("ai.langgraph.nodes.investigation_nodes.provider_router", AIProviderRouter(groq_provider=mock_groq)):
            state = run_investigation_workflow(
                kpi_id=self.kpi_id,
                persona="CFO"
            )

            # Grounding rejection caused fallback to deterministic synthesis
            self.assertEqual(state["provider_metadata"]["provider"], "deterministic_fallback")
            self.assertNotIn("FAKE-EVIDENCE-999", state["ai_explanation"]["grounded_evidence_ids"])

    # -------------------------------------------------------------------------
    # TEST G: Hallucinated Driver ID -> Deterministic Fallback
    # -------------------------------------------------------------------------
    def test_hallucinated_driver_triggers_safe_fallback(self):
        """When LLM returns a non-existent driver ID, grounding failure triggers safe deterministic fallback."""
        mock_groq = MagicMock(spec=GroqProvider)
        mock_groq.name = "groq"
        mock_groq.is_configured.return_value = True
        mock_groq.key_pool_ids = ["groq_pool_1"]
        mock_groq.generate.return_value = AIResponse(
            content='{"summary": "Fake driver hallucination", "supporting_driver_ids": ["UNKNOWN-DRIVER-XYZ"]}',
            parsed_json={
                "summary": "Fake driver hallucination",
                "primary_driver_explanation": "Explanation",
                "supporting_driver_ids": ["UNKNOWN-DRIVER-XYZ"],
                "uncertainty": "Standard",
                "abstained": False
            },
            provider="groq",
            model="llama-3.3-70b-versatile",
            key_pool_id="groq_pool_1",
            latency_ms=150.0
        )

        with patch("ai.langgraph.nodes.investigation_nodes.provider_router", AIProviderRouter(groq_provider=mock_groq)):
            state = run_investigation_workflow(
                kpi_id=self.kpi_id,
                persona="CFO"
            )

            self.assertEqual(state["provider_metadata"]["provider"], "deterministic_fallback")

    # -------------------------------------------------------------------------
    # TEST H: Persona Consistency & Framing
    # -------------------------------------------------------------------------
    def test_persona_adaptation_and_numerical_immutability(self):
        """CFO vs Sales Manager personas have distinct tailored framing with 100% identical numbers."""
        state_cfo = run_investigation_workflow(
            kpi_id=self.kpi_id,
            persona="CFO"
        )
        state_sales = run_investigation_workflow(
            kpi_id=self.kpi_id,
            persona="REGIONAL_SALES_MANAGER"
        )

        # 1. Exact numerical parity
        self.assertAlmostEqual(
            state_cfo["kpi_movement"]["variance_amount"],
            state_sales["kpi_movement"]["variance_amount"]
        )
        self.assertEqual(
            len(state_cfo["drivers"]),
            len(state_sales["drivers"])
        )
        self.assertEqual(
            state_cfo["confidence"]["overall_confidence"],
            state_sales["confidence"]["overall_confidence"]
        )

        # 2. Framing adaptation
        self.assertIn("financial", state_cfo["ai_explanation"]["summary"].lower())
        self.assertIn("territory", state_sales["ai_explanation"]["summary"].lower())

    # -------------------------------------------------------------------------
    # TEST I: Zero Secret Leakage in LangGraph State
    # -------------------------------------------------------------------------
    def test_zero_secret_leakage_in_state(self):
        """Ensures state, node traces, telemetry, and error lists contain no secrets or API keys."""
        state = run_investigation_workflow(
            kpi_id=self.kpi_id,
            persona="CFO"
        )
        raw_state_str = str(state).lower()
        self.assertNotIn("api_key", raw_state_str)
        self.assertNotIn("gsk_", raw_state_str)
        self.assertNotIn("ai_za", raw_state_str)
        self.assertNotIn("bearer", raw_state_str)

    # -------------------------------------------------------------------------
    # TEST J: Node Aliases Compatibility
    # -------------------------------------------------------------------------
    def test_node_aliases_callable(self):
        """Ensures build_grounded_context_node and ai_explanation_node aliases work."""
        self.assertEqual(build_grounded_context_node, prepare_grounding_node)
        self.assertEqual(ai_explanation_node, ai_invocation_node)

if __name__ == "__main__":
    unittest.main()
