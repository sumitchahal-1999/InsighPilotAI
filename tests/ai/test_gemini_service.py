"""
InsightPilot AI — Gemini Service Comprehensive Tests
Validates the backend GeminiService abstraction, context builder, prompt contracts,
abstention enforcement, persona handling, and error resiliency using mocked Gemini client.
"""

import unittest
from unittest.mock import MagicMock
from backend.app.services.gemini_service import GeminiService
from backend.app.services.investigation_service import InvestigationService
from backend.app.services.evidence_service import EvidenceService
from backend.app.services.recommendation_service import RecommendationService
from backend.app.services.simulation_service import SimulationService
from backend.app.errors import KPINotFoundError, InvalidPersonaAPIError, AIServiceUnavailableAPIError, AIGroundingAPIError
from ai.service import AIService
from ai.client import GeminiClient, GeminiAPIError
from ai.context import GroundedContextBuilder
from ai.prompts.investigation_explanation_v1 import build_structured_investigation_prompt

class TestGeminiService(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.inv_service = InvestigationService()
        cls.ev_service = EvidenceService()
        cls.rec_service = RecommendationService()
        cls.sim_service = SimulationService()

    def _get_mocked_gemini_service(self, mock_return_value):
        mock_client = MagicMock(spec=GeminiClient)
        mock_client.generate_json.return_value = mock_return_value
        ai_service = AIService(client=mock_client)
        return GeminiService(
            ai_service=ai_service,
            investigation_service=self.inv_service,
            evidence_service=self.ev_service,
            recommendation_service=self.rec_service,
            simulation_service=self.sim_service
        )

    # 1. Test Context Construction
    def test_context_construction_completeness(self):
        inv_res = self.inv_service.run_investigation("north_america_east_revenue").model_dump()
        ev_res = [e.model_dump() for e in self.ev_service.get_investigation_evidence("north_america_east_revenue").evidence]
        recs = [r.model_dump() for r in self.rec_service.get_recommendations("north_america_east_revenue").recommendations]
        sim = self.sim_service.get_baseline().model_dump()


        context = GroundedContextBuilder.build_investigation_context(
            investigation_result=inv_res,
            evidence_items=ev_res,
            persona="CFO",
            recommendations=recs,
            simulation=sim
        )

        self.assertEqual(context["kpi"]["id"], "north_america_east_revenue")
        self.assertAlmostEqual(context["kpi"]["variance_amount"], -1230000.01, delta=100.0)
        self.assertEqual(len(context["drivers"]), 4)
        self.assertGreaterEqual(len(context["evidence"]), 4)
        self.assertIn("recommendations", context)
        self.assertIn("simulation", context)
        self.assertEqual(context["overall_confidence"]["score"], 89)
        self.assertEqual(context["persona"]["persona_name"], "CFO")

    # 2. Test Prompt Contract
    def test_prompt_contract_contains_directives(self):
        inv_res = self.inv_service.run_investigation("north_america_east_revenue").model_dump()
        ev_res = [e.model_dump() for e in self.ev_service.get_investigation_evidence("north_america_east_revenue").evidence]
        context = GroundedContextBuilder.build_investigation_context(inv_res, ev_res, persona="CFO")
        
        prompt = build_structured_investigation_prompt(context)
        
        self.assertIn("AUTHORITATIVE AND ABSOLUTE", prompt)
        self.assertIn("DO NOT recalculate numbers", prompt)
        self.assertIn("DO NOT invent, assume, or hallucinate", prompt)
        self.assertIn("Chief Financial Officer", prompt)
        self.assertIn("north_america_east_revenue", prompt)

    # 3. Test Structured Explanation Success
    def test_structured_explanation_success(self):
        mock_payload = (
            {
                "summary": "Revenue contracted 7.97% driven by Atlanta DC stockouts.",
                "reasoning": [
                    {
                        "statement": "Atlanta DC availability fell to 68.2%, leading to unmet customer demand.",
                        "supporting_evidence_ids": ["EVID_ERP_ATL_STOCKOUT_001"],
                        "confidence": 94
                    }
                ],
                "primary_driver_explanation": "Atlanta DC stockout accounts for 43.2% of the deficit.",
                "secondary_driver_explanation": "SKU-8821 sales contraction compounded the decline.",
                "uncertainty": "Competitor pricing impact is an analytical estimate.",
                "recommended_next_step": "Transfer inventory from Charlotte.",
                "abstained": False,
                "abstention_reason": None,
                "grounded_evidence_ids": ["EVID_ERP_ATL_STOCKOUT_001"]
            },
            {"model": "gemini-2.5-flash", "latency_ms": 450.0, "total_tokens": 580}
        )
        service = self._get_mocked_gemini_service(mock_payload)
        resp = service.explain_investigation_structured("north_america_east_revenue", persona="CFO")

        self.assertEqual(resp.investigation_id, "INV-EXEC-2026-NAE-001")
        self.assertEqual(resp.persona, "CFO")
        self.assertIn("7.97%", resp.explanation.summary)
        self.assertEqual(len(resp.explanation.reasoning), 1)
        self.assertEqual(resp.explanation.reasoning[0].confidence, 94)
        self.assertFalse(resp.explanation.abstained)
        self.assertEqual(resp.metadata.validation_status, "VERIFIED_GROUNDED")

    # 4. Test Persona Handling (Regional Sales Manager)
    def test_regional_sales_manager_persona(self):
        mock_payload = (
            {
                "summary": "Fulfillment constraints in Atlanta DC impacted regional distributor orders.",
                "reasoning": [
                    {
                        "statement": "Atlanta DC backorders delayed wholesale shipments.",
                        "supporting_evidence_ids": ["EVID_ERP_ATL_STOCKOUT_001"],
                        "confidence": 94
                    }
                ],
                "primary_driver_explanation": "Atlanta DC stockout is the main operational bottleneck.",
                "secondary_driver_explanation": "Distributor order deferrals followed inventory shortages.",
                "uncertainty": "Regional demand spikes require continued monitoring.",
                "recommended_next_step": "Engage Tier-1 distributor accounts with delivery timelines.",
                "abstained": False,
                "abstention_reason": None,
                "grounded_evidence_ids": ["EVID_ERP_ATL_STOCKOUT_001"]
            },
            {"model": "gemini-2.5-flash", "latency_ms": 420.0, "total_tokens": 520}
        )
        service = self._get_mocked_gemini_service(mock_payload)
        resp = service.explain_investigation_structured(
            "north_america_east_revenue",
            persona="REGIONAL_SALES_MANAGER"
        )
        self.assertEqual(resp.persona, "REGIONAL_SALES_MANAGER")
        self.assertIn("Fulfillment constraints", resp.explanation.summary)

    # 5. Test Invalid Persona Rejection
    def test_invalid_persona_raises_error(self):
        mock_payload = ({}, {})
        service = self._get_mocked_gemini_service(mock_payload)
        with self.assertRaises(InvalidPersonaAPIError):
            service.explain_investigation_structured("north_america_east_revenue", persona="NON_EXISTENT_ROLE")

    # 6. Test Hallucinated Evidence ID Rejection
    def test_hallucinated_evidence_id_raises_grounding_error(self):
        mock_payload = (
            {
                "summary": "Revenue down",
                "reasoning": [
                    {
                        "statement": "Fake finding",
                        "supporting_evidence_ids": ["EVID_FAKE_RECORD_999"],
                        "confidence": 90
                    }
                ],
                "primary_driver_explanation": "Text",
                "secondary_driver_explanation": "Text",
                "uncertainty": "Text",
                "recommended_next_step": "Text",
                "abstained": False,
                "abstention_reason": None,
                "grounded_evidence_ids": ["EVID_FAKE_RECORD_999"]
            },
            {"model": "gemini-2.5-flash", "latency_ms": 300.0}
        )
        service = self._get_mocked_gemini_service(mock_payload)
        with self.assertRaises(AIGroundingAPIError):
            service.explain_investigation_structured("north_america_east_revenue", persona="CFO")

    # 7. Test Gemini Unavailable / Timeout Error Handling
    def test_gemini_unavailable_raises_api_error(self):
        mock_client = MagicMock(spec=GeminiClient)
        mock_client.generate_json.side_effect = GeminiAPIError("Connection timed out after 30s.")
        ai_service = AIService(client=mock_client)
        service = GeminiService(
            ai_service=ai_service,
            investigation_service=self.inv_service,
            evidence_service=self.ev_service
        )
        with self.assertRaises(AIServiceUnavailableAPIError) as ctx:
            service.explain_investigation_structured("north_america_east_revenue", persona="CFO")
        self.assertIn("Connection timed out", str(ctx.exception))

if __name__ == "__main__":
    unittest.main()
