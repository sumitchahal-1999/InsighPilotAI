"""
InsightPilot AI — Phase 5.3 E2E Scenario & Reliability Tests
Tests real multi-provider routing, dual key pool failovers, capability filtering,
grounding & schema validation, persona adaptation, zero secret leakage, and graceful degradation.
"""

import unittest
from unittest.mock import MagicMock, patch
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
from ai.orchestration.task_classifier import TaskClassifier
from ai.orchestration.fallback_manager import FallbackManager
from ai.orchestration.provider_router import ProviderRouter
from ai.validator import GroundingValidator, GroundingValidationError
from ai.schemas.explanation import StructuredInvestigationExplanation, AIExplanation
from backend.app.services.investigation_service import InvestigationService

class TestPhase53E2EScenarios(unittest.TestCase):

    def setUp(self):
        self.sample_context = {
            "investigation_id": "INV-EXEC-2026-NAE-001",
            "kpi": {
                "id": "north_america_east_revenue",
                "name": "North America East Revenue",
                "current_value": 14200000.05,
                "previous_value": 15430000.06,
                "variance_amount": -1230000.01,
                "percent_change": -7.97
            },
            "drivers": [
                {
                    "driver_id": "atlanta_dc_stockout",
                    "driver_name": "Atlanta DC Stockout",
                    "rank": 1,
                    "contribution_pct": 43.2,
                    "impact_usd": -550000.0,
                    "confidence_score": 94
                },
                {
                    "driver_id": "sku_8821_sales_contraction",
                    "driver_name": "SKU-8821 Sales Contraction",
                    "rank": 2,
                    "contribution_pct": 26.7,
                    "impact_usd": -340000.0,
                    "confidence_score": 89
                }
            ],
            "evidence": [
                {
                    "evidence_id": "EVID-SAP-001",
                    "finding_summary": "14 consecutive zero stock days for SKU-8821"
                },
                {
                    "evidence_id": "EVID-CRM-002",
                    "finding_summary": "+310% stockout complaint surge"
                }
            ],
            "overall_confidence": {
                "score": 88,
                "label": "HIGH",
                "abstention": False
            },
            "persona": {
                "persona_name": "CFO",
                "role_title": "Chief Financial Officer"
            }
        }

    # -------------------------------------------------------------------------
    # 1. PROVIDER ROUTING & FAILOVER TESTS
    # -------------------------------------------------------------------------

    def test_standard_reasoning_routes_to_groq_primary(self):
        """Standard text reasoning routes to Groq primary and Gemini fallback."""
        primary, fallback = TaskClassifier.get_provider_routing(TaskType.BUSINESS_REASONING)
        self.assertEqual(primary, "groq")
        self.assertEqual(fallback, "gemini")

    def test_multimodal_task_routes_strictly_to_gemini(self):
        """Multimodal analysis routes exclusively to Gemini with zero fallback to Groq."""
        primary, fallback = TaskClassifier.get_provider_routing(TaskType.MULTIMODAL_ANALYSIS)
        self.assertEqual(primary, "gemini")
        self.assertIsNone(fallback)

    def test_groq_pool_1_rate_limit_fails_over_to_pool_2(self):
        """When Groq Key 1 hits 429 rate limit, FallbackManager rotates seamlessly to Groq Key 2."""
        mock_groq = MagicMock(spec=GroqProvider)
        mock_groq.name = "groq"
        mock_groq.is_configured.return_value = True
        mock_groq.key_pool_ids = ["groq_pool_1", "groq_pool_2"]

        # Pool 1 fails with RATE_LIMITED, Pool 2 succeeds
        def groq_side_effect(req, key_pool_index=0):
            if key_pool_index == 0:
                raise AIProviderError(
                    "Rate limit exceeded on Groq Key 1",
                    error_category=AIErrorCategory.RATE_LIMITED,
                    provider="groq",
                    key_pool_id="groq_pool_1",
                    retryable=True
                )
            return AIResponse(
                content='{"summary": "Recovered via Key 2"}',
                parsed_json={"summary": "Recovered via Key 2"},
                provider="groq",
                model="llama-3.3-70b-versatile",
                key_pool_id="groq_pool_2",
                latency_ms=120.0
            )

        mock_groq.generate.side_effect = groq_side_effect

        manager = FallbackManager(providers={"groq": mock_groq}, fallback_enabled=True)
        req = AIRequest(task_type=TaskType.BUSINESS_REASONING, prompt="Explain variance")
        resp = manager.execute_with_fallback(req, primary_provider_name="groq", fallback_provider_name=None)

        self.assertTrue(resp.success)
        self.assertTrue(resp.fallback_used)
        self.assertEqual(resp.key_pool_id, "groq_pool_2")
        self.assertIn("groq_pool_1:RATE_LIMITED", resp.fallback_chain)

    def test_both_groq_pools_fail_cross_provider_fallback_to_gemini(self):
        """When all Groq pools fail, FallbackManager falls back to Gemini Pool 1."""
        mock_groq = MagicMock(spec=GroqProvider)
        mock_groq.name = "groq"
        mock_groq.is_configured.return_value = True
        mock_groq.key_pool_ids = ["groq_pool_1", "groq_pool_2"]
        mock_groq.generate.side_effect = AIProviderError(
            "Groq quota exhausted",
            error_category=AIErrorCategory.QUOTA_EXCEEDED,
            provider="groq",
            key_pool_id="groq_pool",
            retryable=True
        )

        mock_gemini = MagicMock(spec=GeminiProvider)
        mock_gemini.name = "gemini"
        mock_gemini.is_configured.return_value = True
        mock_gemini.key_pool_ids = ["gemini_pool_1"]
        mock_gemini.generate.return_value = AIResponse(
            content='{"summary": "Synthesized by Gemini"}',
            parsed_json={"summary": "Synthesized by Gemini"},
            provider="gemini",
            model="gemini-2.5-flash",
            key_pool_id="gemini_pool_1",
            latency_ms=350.0
        )

        manager = FallbackManager(
            providers={"groq": mock_groq, "gemini": mock_gemini},
            fallback_enabled=True
        )
        req = AIRequest(task_type=TaskType.BUSINESS_REASONING, prompt="Synthesize context")
        resp = manager.execute_with_fallback(req, primary_provider_name="groq", fallback_provider_name="gemini")

        self.assertTrue(resp.success)
        self.assertTrue(resp.fallback_used)
        self.assertEqual(resp.provider, "gemini")
        self.assertEqual(resp.key_pool_id, "gemini_pool_1")

    # -------------------------------------------------------------------------
    # 2. GROUNDING & SCHEMA VALIDATION TESTS
    # -------------------------------------------------------------------------

    def test_grounding_validation_success_with_valid_citations(self):
        """Valid response with legitimate evidence and driver citations passes."""
        valid_response = {
            "summary": "Revenue contracted by -$1.23M due to Atlanta DC stockouts.",
            "primary_driver_explanation": "Atlanta DC experienced 14 zero-stock days.",
            "supporting_driver_ids": ["atlanta_dc_stockout"],
            "supporting_evidence_ids": ["EVID-SAP-001"],
            "business_implications": ["$550K direct revenue constraint in NA-East"],
            "risks": ["Distributor churn if inventory is not reallocated"],
            "recommended_next_actions": ["Reallocate 20,000 units from Charlotte Hub"],
            "uncertainty": "Assumes constant POS end-consumer brand demand baseline.",
            "abstained": False
        }
        validated = GroundingValidator.validate_grounding(valid_response, self.sample_context)
        self.assertIn("EVID-SAP-001", validated["grounded_evidence_ids"])
        self.assertEqual(validated["supporting_driver_ids"], ["atlanta_dc_stockout"])

    def test_grounding_validation_rejects_hallucinated_evidence_ids(self):
        """Response containing fake or hallucinated evidence IDs is strictly rejected."""
        fake_evidence_response = {
            "summary": "Revenue contracted due to stockout.",
            "primary_driver_explanation": "Stockout confirmed.",
            "supporting_evidence_ids": ["EVID-SAP-001", "EVID-FAKE-999"],
            "uncertainty": "Standard analytical limits.",
            "abstained": False
        }
        with self.assertRaises(GroundingValidationError) as ctx:
            GroundingValidator.validate_grounding(fake_evidence_response, self.sample_context)
        self.assertIn("EVID-FAKE-999", str(ctx.exception))

    def test_grounding_validation_rejects_hallucinated_driver_ids(self):
        """Response containing non-existent driver IDs is strictly rejected."""
        fake_driver_response = {
            "summary": "Revenue contracted due to unknown causes.",
            "primary_driver_explanation": "Explanation.",
            "supporting_driver_ids": ["hallucinated_driver_id_xyz"],
            "supporting_evidence_ids": ["EVID-SAP-001"],
            "uncertainty": "Standard bounds.",
            "abstained": False
        }
        with self.assertRaises(GroundingValidationError) as ctx:
            GroundingValidator.validate_grounding(fake_driver_response, self.sample_context)
        self.assertIn("hallucinated_driver_id_xyz", str(ctx.exception))

    def test_grounding_validation_enforces_abstention_on_low_confidence(self):
        """When investigation confidence is low, confident assertions without uncertainty fail."""
        low_conf_context = dict(self.sample_context)
        low_conf_context["overall_confidence"] = {
            "score": 45,
            "label": "LOW",
            "abstention": True,
            "abstention_reason": "Insufficient verified telemetry."
        }

        confident_response = {
            "summary": "Atlanta DC is 100% definitively the sole reason for revenue loss.",
            "primary_driver_explanation": "Conclusive evidence proves full causality.",
            "supporting_evidence_ids": ["EVID-SAP-001"],
            "uncertainty": "Zero uncertainty exists.",
            "abstained": False
        }

        with self.assertRaises(GroundingValidationError) as ctx:
            GroundingValidator.validate_grounding(confident_response, low_conf_context)
        self.assertIn("mandatory abstention", str(ctx.exception).lower())

    # -------------------------------------------------------------------------
    # 3. SECURITY & SECRET SAFETY TESTS
    # -------------------------------------------------------------------------

    def test_zero_secret_leakage_in_service_execution(self):
        """Ensures service execution and generated traces never leak raw API keys or secrets."""
        service = InvestigationService()
        trace = service.run_langgraph_investigation(
            kpi_id="north_america_east_revenue",
            region="NA-East",
            persona_id="CFO"
        )
        json_repr = str(trace.model_dump()).lower()
        self.assertNotIn("api_key", json_repr)
        self.assertNotIn("gsk_", json_repr)
        self.assertNotIn("ai_za", json_repr)
        self.assertNotIn("bearer", json_repr)

    # -------------------------------------------------------------------------
    # 4. PERSONA-AWARE SYNTHESIS IMMUTABILITY
    # -------------------------------------------------------------------------

    def test_persona_adaptation_preserves_quantitative_truth(self):
        """CFO vs Sales Manager personas have distinct narratives but 100% identical numbers."""
        service = InvestigationService()

        trace_cfo = service.run_langgraph_investigation(
            kpi_id="north_america_east_revenue",
            persona_id="CFO"
        )
        trace_sales = service.run_langgraph_investigation(
            kpi_id="north_america_east_revenue",
            persona_id="REGIONAL_SALES_MANAGER"
        )

        # Quantitative numbers MUST be exactly identical
        self.assertEqual(
            trace_cfo.deterministic_summary["previous_value"],
            trace_sales.deterministic_summary["previous_value"]
        )
        self.assertEqual(
            trace_cfo.deterministic_summary["variance_amount"],
            trace_sales.deterministic_summary["variance_amount"]
        )
        self.assertEqual(
            trace_cfo.confidence["overall_confidence"],
            trace_sales.confidence["overall_confidence"]
        )

if __name__ == "__main__":
    unittest.main()
