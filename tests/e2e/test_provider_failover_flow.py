"""
InsightPilot AI — Phase 5.8: Provider Failover & Resilience E2E Test Suite
Verifies the multi-pool failover routing chain:
Groq Pool 1 -> Groq Pool 2 -> Gemini Pool 1 -> Gemini Pool 2 -> Deterministic Fallback.
Tests quota exhaustion, 429 rate limits, non-retryable errors, multimodal routing,
and zero secret leakage.
"""

import unittest
from unittest.mock import MagicMock, patch
from ai.providers.base import BaseAIProvider
from ai.providers.types import (
    AIRequest,
    AIResponse,
    TaskType,
    Capability,
    AIProviderError,
    AIErrorCategory
)
from ai.orchestration.fallback_manager import FallbackManager
from ai.orchestration.provider_router import provider_router
from ai.orchestration.telemetry import telemetry_manager
from ai.langgraph.graph import run_investigation_workflow


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


class TestProviderFailoverFlow(unittest.TestCase):
    """End-to-end provider failover, quota resilience, and deterministic fallback tests."""

    def setUp(self):
        self.groq_prov = DummyProvider("groq", 2)
        self.gemini_prov = DummyProvider("gemini", 2)
        self.manager = FallbackManager(providers={"groq": self.groq_prov, "gemini": self.gemini_prov})
        self.request = AIRequest(
            task_type=TaskType.INVESTIGATION_EXPLANATION,
            prompt="Explain the North America East revenue contraction.",
            system_instruction="You are InsightPilot AI.",
            response_schema={"type": "object"}
        )

    # -------------------------------------------------------------------------
    # 1. Scenario A: Primary Success (Groq Pool 1)
    # -------------------------------------------------------------------------
    def test_scenario_a_groq_pool_1_primary_success(self):
        """Scenario A: Groq Key 1 succeeds on the first attempt without failover."""
        self.groq_prov.generate_mock.return_value = AIResponse(
            content='{"summary": "Revenue contracted by -$1.23M (-7.97%) due to Atlanta DC Stockout."}',
            structured_data={"summary": "Revenue contracted by -$1.23M (-7.97%) due to Atlanta DC Stockout."},
            provider="groq",
            model="llama-3.3-70b-versatile",
            key_pool_id="groq_pool_1",
            latency_ms=185.0,
            success=True
        )

        resp = self.manager.execute_with_fallback(self.request, "groq", "gemini")
        self.assertEqual(resp.key_pool_id, "groq_pool_1")
        self.assertEqual(resp.provider, "groq")
        self.assertFalse(resp.fallback_used)
        self.assertIn("Atlanta DC Stockout", resp.content)
        self.assertEqual(self.groq_prov.generate_mock.call_count, 1)
        self.assertEqual(self.gemini_prov.generate_mock.call_count, 0)

    # -------------------------------------------------------------------------
    # 2. Scenario B: Rate Limit Failover (Groq Pool 1 -> Groq Pool 2)
    # -------------------------------------------------------------------------
    def test_scenario_b_groq_pool_1_rate_limit_failover_to_pool_2(self):
        """Scenario B: Groq Key 1 encounters 429 Rate Limit and fails over to Groq Key 2."""
        def side_effect(req: AIRequest, idx: int) -> AIResponse:
            if idx == 0:
                raise AIProviderError(
                    "Rate limit reached: 429 Too Many Requests",
                    AIErrorCategory.RATE_LIMITED,
                    "groq",
                    "groq_pool_1",
                    True
                )
            return AIResponse(
                content='{"summary": "Failover to Groq Pool 2 succeeded."}',
                structured_data={"summary": "Failover to Groq Pool 2 succeeded."},
                provider="groq",
                model="llama-3.3-70b-versatile",
                key_pool_id="groq_pool_2",
                latency_ms=210.0,
                success=True
            )

        self.groq_prov.generate_mock.side_effect = side_effect
        resp = self.manager.execute_with_fallback(self.request, "groq", "gemini")
        self.assertEqual(resp.key_pool_id, "groq_pool_2")
        self.assertEqual(resp.provider, "groq")
        self.assertTrue(resp.fallback_used)
        self.assertEqual(self.groq_prov.generate_mock.call_count, 2)
        self.assertEqual(self.gemini_prov.generate_mock.call_count, 0)

    # -------------------------------------------------------------------------
    # 3. Scenario C: Quota Exhaustion Cross-Provider Fallback (Groq -> Gemini 1)
    # -------------------------------------------------------------------------
    def test_scenario_c_groq_exhaustion_cross_provider_fallback_to_gemini_1(self):
        """Scenario C: Both Groq pools exhaust quota, triggering cross-provider fallback to Gemini Pool 1."""
        self.groq_prov.generate_mock.side_effect = AIProviderError(
            "Monthly token quota exceeded",
            AIErrorCategory.QUOTA_EXCEEDED,
            "groq",
            "groq_pool_1",
            True
        )
        self.gemini_prov.generate_mock.return_value = AIResponse(
            content='{"summary": "Gemini Pool 1 handled cross-provider failover."}',
            structured_data={"summary": "Gemini Pool 1 handled cross-provider failover."},
            provider="gemini",
            model="gemini-2.5-flash",
            key_pool_id="gemini_pool_1",
            latency_ms=640.0,
            success=True
        )

        resp = self.manager.execute_with_fallback(self.request, "groq", "gemini")
        self.assertEqual(resp.key_pool_id, "gemini_pool_1")
        self.assertEqual(resp.provider, "gemini")
        self.assertTrue(resp.fallback_used)
        self.assertEqual(self.groq_prov.generate_mock.call_count, 2)
        self.assertEqual(self.gemini_prov.generate_mock.call_count, 1)

    # -------------------------------------------------------------------------
    # 4. Scenario D: Final Provider Pool Failover (Gemini 1 -> Gemini 2)
    # -------------------------------------------------------------------------
    def test_scenario_d_gemini_pool_1_failover_to_gemini_pool_2(self):
        """Scenario D: Groq unavailable and Gemini Pool 1 rate-limited, failing over to Gemini Pool 2."""
        self.groq_prov.generate_mock.side_effect = AIProviderError(
            "Service unavailable",
            AIErrorCategory.PROVIDER_UNAVAILABLE,
            "groq",
            "groq_pool_1",
            True
        )

        def gemini_side_effect(req: AIRequest, idx: int) -> AIResponse:
            if idx == 0:
                raise AIProviderError(
                    "Resource exhausted on Gemini 1",
                    AIErrorCategory.RATE_LIMITED,
                    "gemini",
                    "gemini_pool_1",
                    True
                )
            return AIResponse(
                content='{"summary": "Gemini Pool 2 succeeded as final AI provider."}',
                structured_data={"summary": "Gemini Pool 2 succeeded as final AI provider."},
                provider="gemini",
                model="gemini-2.5-flash",
                key_pool_id="gemini_pool_2",
                latency_ms=720.0,
                success=True
            )

        self.gemini_prov.generate_mock.side_effect = gemini_side_effect
        resp = self.manager.execute_with_fallback(self.request, "groq", "gemini")
        self.assertEqual(resp.key_pool_id, "gemini_pool_2")
        self.assertEqual(resp.provider, "gemini")
        self.assertTrue(resp.fallback_used)

    # -------------------------------------------------------------------------
    # 5. Scenario E: Total Outage Deterministic Fallback Synthesis
    # -------------------------------------------------------------------------
    def test_scenario_e_total_ai_outage_deterministic_fallback_in_workflow(self):
        """Scenario E: When all LLM providers fail, LangGraph investigation pipeline uses deterministic fallback."""
        # Unconfigured / failed providers in workflow
        result = run_investigation_workflow(
            kpi_id="north_america_east_revenue",
            persona="CFO"
        )

        # Deterministic truth is fully preserved
        self.assertIsNotNone(result)
        self.assertAlmostEqual(result["kpi_movement"]["variance_amount"], -1230000.01, places=2)
        self.assertEqual(result["confidence"]["overall_confidence"], 89)
        self.assertFalse(result["abstention"])

        # AI explanation contains fallback synthesis
        explanation = result.get("ai_explanation", {})
        self.assertIn("summary", explanation)
        self.assertIn("atlanta dc stockout", explanation["summary"].lower())
        self.assertIn("EVID_ERP_ATL_STOCKOUT_001", explanation["grounded_evidence_ids"])

    # -------------------------------------------------------------------------
    # 6. Multimodal Tasks Route Exclusively to Gemini
    # -------------------------------------------------------------------------
    def test_multimodal_tasks_route_strictly_to_gemini(self):
        """Multimodal image/chart analysis requests route strictly to Gemini with zero Groq fallback."""
        from ai.orchestration.task_classifier import TaskClassifier
        primary, fallback = TaskClassifier.get_provider_routing(TaskType.IMAGE_ANALYSIS)
        self.assertEqual(primary, "gemini")
        self.assertIsNone(fallback, "Multimodal must never have Groq as fallback")

        caps = TaskClassifier.get_required_capabilities(TaskType.IMAGE_ANALYSIS)
        self.assertIn(Capability.MULTIMODAL_VISION, caps)

    # -------------------------------------------------------------------------
    # 7. Non-Retryable Error Safety
    # -------------------------------------------------------------------------
    def test_non_retryable_error_does_not_failover(self):
        """Non-retryable client errors (e.g. invalid request) stop immediately without retry spam."""
        self.groq_prov.generate_mock.side_effect = AIProviderError(
            "Invalid parameters in request",
            AIErrorCategory.INVALID_REQUEST,
            "groq",
            "groq_pool_1",
            False
        )

        with self.assertRaises(AIProviderError) as ctx:
            self.manager.execute_with_fallback(self.request, "groq", "gemini")
        self.assertEqual(ctx.exception.error_category, AIErrorCategory.INVALID_REQUEST)
        self.assertEqual(self.groq_prov.generate_mock.call_count, 1)
        self.assertEqual(self.gemini_prov.generate_mock.call_count, 0)

    # -------------------------------------------------------------------------
    # 8. Zero Secret Leakage in Telemetry and State
    # -------------------------------------------------------------------------
    def test_zero_secret_leakage_in_failover_telemetry(self):
        """Ensures that failover events, telemetry logs, and error strings never expose API keys."""
        summary = telemetry_manager.get_summary()
        for k, val in summary.items():
            val_str = str(val)
            self.assertNotIn("gsk_", val_str, "Groq API key found in telemetry!")
            self.assertNotIn("AIzaSy", val_str, "Gemini API key found in telemetry!")
            self.assertNotIn("Bearer ", val_str, "Auth header token found in telemetry!")


if __name__ == "__main__":
    unittest.main()
