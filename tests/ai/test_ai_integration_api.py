"""
InsightPilot AI — AI API Endpoint Integration Tests
Tests POST /api/v1/ai/... routes using TestClient and mocked Gemini client.
"""

import unittest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.dependencies import get_ai_service
from ai.service import AIService
from ai.client import GeminiClient, GeminiAPIError

class TestAIIntegrationAPI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    def _get_mock_ai_service(self, generate_mock_data):
        mock_gemini = MagicMock(spec=GeminiClient)
        mock_gemini.generate_json.return_value = generate_mock_data
        return AIService(client=mock_gemini)

    def test_structured_explain_api_success(self):
        mock_response = (
            {
                "summary": "North America East revenue contracted 7.97% (-$1.23M) primarily due to Atlanta DC stockouts.",
                "reasoning": [
                    {
                        "statement": "Atlanta DC inventory dropped to 68.2%, causing $550k in unfulfilled demand.",
                        "supporting_evidence_ids": ["EVID_ERP_ATL_STOCKOUT_001"],
                        "confidence": 94
                    }
                ],
                "primary_driver_explanation": "Atlanta DC stockout was the primary operational bottleneck.",
                "secondary_driver_explanation": "SKU-8821 sales volume and distributor order deferrals compounded the deficit.",
                "uncertainty": "Competitor pricing impact is an analytical estimate.",
                "recommended_next_step": "Transfer inventory from Charlotte to Atlanta.",
                "abstained": False,
                "abstention_reason": None,
                "grounded_evidence_ids": ["EVID_ERP_ATL_STOCKOUT_001"]
            },
            {
                "model": "gemini-2.5-flash",
                "latency_ms": 480.0,
                "prompt_tokens": 450,
                "completion_tokens": 180,
                "total_tokens": 630
            }
        )
        mock_service = self._get_mock_ai_service(mock_response)
        app.dependency_overrides[get_ai_service] = lambda: mock_service

        try:
            response = self.client.post(
                "/api/v1/ai/explain/north_america_east_revenue",
                json={
                    "persona": "CFO",
                    "explanation_mode": "structured",
                    "include_recommendations": True
                }
            )
            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertEqual(data["persona"], "CFO")
            self.assertIn("7.97%", data["explanation"]["summary"])
            self.assertEqual(len(data["explanation"]["reasoning"]), 1)
            self.assertEqual(data["explanation"]["reasoning"][0]["confidence"], 94)
            self.assertEqual(data["metadata"]["validation_status"], "VERIFIED_GROUNDED")
        finally:
            app.dependency_overrides.pop(get_ai_service, None)

    def test_executive_explanation_api_success(self):
        mock_response = (
            {
                "headline": "NA-East Q3 revenue fell 7.97% driven by Atlanta DC stockouts.",
                "situation": "Revenue dropped from $15.43M to $14.20M (-$1.23M).",
                "diagnosis": "Atlanta DC stockout (43.2%) and SKU-8821 sales volume (26.7%) drove the bulk of the decline.",
                "evidence_summary": "ERP and CRM records corroborate warehouse stockouts and distributor backorders.",
                "uncertainty": "External competitor price impact remains an analytical estimate.",
                "executive_takeaway": "Focus inventory replenishment on Atlanta DC.",
                "grounded_evidence_ids": ["EVID_ERP_ATL_STOCKOUT_001", "EVID_CRM_PO_DEF_006"]
            },
            {
                "model": "gemini-2.5-flash",
                "latency_ms": 500.0,
                "prompt_tokens": 400,
                "completion_tokens": 150,
                "total_tokens": 550
            }
        )
        mock_service = self._get_mock_ai_service(mock_response)
        app.dependency_overrides[get_ai_service] = lambda: mock_service

        try:
            response = self.client.post(
                "/api/v1/ai/investigations/north_america_east_revenue/explanation",
                json={"persona": "CFO"}
            )
            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertEqual(data["persona"], "CFO")
            self.assertIn("7.97%", data["explanation"]["headline"])
            self.assertEqual(len(data["explanation"]["grounded_evidence_ids"]), 2)
            self.assertEqual(data["metadata"]["validation_status"], "VERIFIED_GROUNDED")
        finally:
            app.dependency_overrides.pop(get_ai_service, None)

    def test_driver_explanation_api_success(self):
        mock_response = (
            {
                "driver_id": "atlanta_dc_stockout",
                "driver_name": "Atlanta DC Stockout",
                "contribution_summary": "43.2% contribution (-$550,000.00).",
                "evidence_rationale": "Inventory telemetry showed 68.2% availability on Aug 5.",
                "operational_context": "Fulfillment constraints caused backorders.",
                "uncertainty": "Direct operational telemetry yields high confidence.",
                "grounded_evidence_ids": ["EVID_ERP_ATL_STOCKOUT_001"]
            },
            {
                "model": "gemini-2.5-flash",
                "latency_ms": 400.0,
                "prompt_tokens": 300,
                "completion_tokens": 100,
                "total_tokens": 400
            }
        )
        mock_service = self._get_mock_ai_service(mock_response)
        app.dependency_overrides[get_ai_service] = lambda: mock_service

        try:
            response = self.client.post(
                "/api/v1/ai/investigations/north_america_east_revenue/drivers/atlanta_dc_stockout/explanation",
                json={"persona": "REGIONAL_SALES_MANAGER"}
            )
            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertEqual(data["driver_id"], "atlanta_dc_stockout")
            self.assertEqual(data["persona"], "REGIONAL_SALES_MANAGER")
        finally:
            app.dependency_overrides.pop(get_ai_service, None)

    def test_invalid_persona_returns_400(self):
        response = self.client.post(
            "/api/v1/ai/explain/north_america_east_revenue",
            json={"persona": "UNSUPPORTED_ROLE"}
        )
        self.assertEqual(response.status_code, 400)
        data = response.json()
        self.assertEqual(data["error"]["code"], "INVALID_PERSONA")

    def test_unknown_kpi_returns_404(self):
        response = self.client.post(
            "/api/v1/ai/explain/unknown_kpi",
            json={"persona": "CFO"}
        )
        self.assertEqual(response.status_code, 404)
        data = response.json()
        self.assertEqual(data["error"]["code"], "KPI_NOT_FOUND")

    def test_ai_service_unavailable_returns_503(self):
        mock_gemini = MagicMock(spec=GeminiClient)
        mock_gemini.generate_json.side_effect = GeminiAPIError("GEMINI_API_KEY is not configured in the environment.")
        mock_service = AIService(client=mock_gemini)
        app.dependency_overrides[get_ai_service] = lambda: mock_service

        try:
            response = self.client.post(
                "/api/v1/ai/explain/north_america_east_revenue",
                json={"persona": "CFO"}
            )
            self.assertEqual(response.status_code, 503)
            data = response.json()
            self.assertEqual(data["error"]["code"], "AI_SERVICE_UNAVAILABLE")
        finally:
            app.dependency_overrides.pop(get_ai_service, None)

    def test_ai_grounding_failure_returns_422(self):
        # Return response with hallucinated evidence ID
        mock_response = (
            {
                "summary": "Revenue down",
                "reasoning": [],
                "primary_driver_explanation": "Diagnosis text",
                "secondary_driver_explanation": "Secondary text",
                "uncertainty": "Caveats",
                "recommended_next_step": "Takeaway",
                "abstained": False,
                "abstention_reason": None,
                "grounded_evidence_ids": ["EVID_HALLUCINATED_999"]
            },
            {"model": "gemini-2.5-flash", "latency_ms": 300.0}
        )
        mock_service = self._get_mock_ai_service(mock_response)
        app.dependency_overrides[get_ai_service] = lambda: mock_service

        try:
            response = self.client.post(
                "/api/v1/ai/explain/north_america_east_revenue",
                json={"persona": "CFO"}
            )
            self.assertEqual(response.status_code, 422)
            data = response.json()
            self.assertEqual(data["error"]["code"], "AI_GROUNDING_FAILED")
        finally:
            app.dependency_overrides.pop(get_ai_service, None)

if __name__ == "__main__":
    unittest.main()
