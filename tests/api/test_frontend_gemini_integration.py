"""
InsightPilot AI — Frontend Gemini Integration & Contract Audit
Validates end-to-end frontend-backend contracts for grounded Gemini reasoning,
persona variations, evidence link integrity, abstention boundaries, and deterministic immutability.
"""

import unittest
from unittest.mock import MagicMock
from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.dependencies import get_ai_service
from ai.service import AIService
from ai.client import GeminiClient

class TestFrontendGeminiIntegration(unittest.TestCase):

    def setUp(self):
        self.mock_gemini = MagicMock(spec=GeminiClient)
        mock_ai_service = AIService(client=self.mock_gemini)
        app.dependency_overrides[get_ai_service] = lambda: mock_ai_service
        self.client = TestClient(app)

    def tearDown(self):
        app.dependency_overrides.clear()

    # 1. Test Structured Explanation Contract for Screen 1 & 2
    def test_screen_1_and_2_gemini_synthesis_contract(self):
        self.mock_gemini.generate_json.return_value = (
            {
                "summary": "North America East revenue declined 7.97% (-$1.23M) driven primarily by Atlanta DC stockouts.",
                "reasoning": [
                    {
                        "statement": "Atlanta DC inventory availability fell to 68.2%, leading to unmet regional fulfillment.",
                        "supporting_evidence_ids": ["EVID_ERP_ATL_STOCKOUT_001"],
                        "confidence": 94
                    }
                ],
                "primary_driver_explanation": "The primary contributing factor is the Atlanta DC stockout (43.2% contribution).",
                "secondary_driver_explanation": "SKU-8821 sales contraction compounded the decline.",
                "uncertainty": "External competitor price elasticity is estimated from web scrapes.",
                "recommended_next_step": "Execute emergency inventory transfer from Charlotte DC.",
                "abstained": False,
                "abstention_reason": None,
                "grounded_evidence_ids": ["EVID_ERP_ATL_STOCKOUT_001"]
            },
            {"model": "gemini-2.5-flash", "latency_ms": 320.0, "total_tokens": 480}
        )

        response = self.client.post("/api/v1/ai/explain/north_america_east_revenue", json={"persona": "CFO"})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        self.assertEqual(data["persona"], "CFO")
        self.assertIn("7.97%", data["explanation"]["summary"])
        self.assertIn("EVID_ERP_ATL_STOCKOUT_001", data["explanation"]["grounded_evidence_ids"])
        self.assertEqual(data["metadata"]["validation_status"], "VERIFIED_GROUNDED")

    # 2. Test Persona Switching (CFO vs REGIONAL_SALES_MANAGER)
    def test_persona_switching_narratives(self):
        self.mock_gemini.generate_json.return_value = (
            {
                "summary": "Fulfillment constraints in Atlanta DC delayed distributor replenishment orders across the East territory.",
                "reasoning": [
                    {
                        "statement": "Atlanta DC backorders resulted in 29 deferred distributor POs.",
                        "supporting_evidence_ids": ["EVID_ERP_ATL_STOCKOUT_001", "EVID_CRM_PO_DEF_006"],
                        "confidence": 94
                    }
                ],
                "primary_driver_explanation": "Atlanta stockouts disrupted Tier-1 distributor delivery schedules.",
                "secondary_driver_explanation": "Distributor accounts deferred purchase orders until inventory stabilizes.",
                "uncertainty": "Competitor promotional actions may affect regional customer loyalty.",
                "recommended_next_step": "Conduct distributor recovery outreach with freight priority guarantees.",
                "abstained": False,
                "abstention_reason": None,
                "grounded_evidence_ids": ["EVID_ERP_ATL_STOCKOUT_001", "EVID_CRM_PO_DEF_006"]
            },
            {"model": "gemini-2.5-flash", "latency_ms": 310.0, "total_tokens": 490}
        )

        response = self.client.post(
            "/api/v1/ai/explain/north_america_east_revenue",
            json={"persona": "REGIONAL_SALES_MANAGER"}
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["persona"], "REGIONAL_SALES_MANAGER")
        self.assertIn("distributor", data["explanation"]["summary"].lower())

    # 3. Test Abstention Contract
    def test_abstention_contract_for_low_confidence(self):
        self.mock_gemini.generate_json.return_value = (
            {
                "summary": "Analytical conclusion uncertain due to insufficient telemetry data.",
                "reasoning": [],
                "primary_driver_explanation": "Confidence score is below the 65% certainty boundary.",
                "secondary_driver_explanation": "Insufficient empirical records.",
                "uncertainty": "Data signal threshold not met; abstaining from causal claims.",
                "recommended_next_step": "Collect additional warehouse telemetry before taking action.",
                "abstained": True,
                "abstention_reason": "Confidence score below 65% threshold.",
                "grounded_evidence_ids": []
            },
            {"model": "gemini-2.5-flash", "latency_ms": 280.0}
        )

        response = self.client.post("/api/v1/ai/explain/north_america_east_revenue", json={"persona": "CFO"})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["explanation"]["abstained"])

    # 4. Test Deterministic Analytics Remain Authoritative
    def test_deterministic_analytics_immutability(self):
        kpi_resp = self.client.get("/api/v1/kpis/north_america_east_revenue")
        self.assertEqual(kpi_resp.status_code, 200)
        kpi = kpi_resp.json()
        self.assertAlmostEqual(kpi["current_value"], 14200000.05, places=2)
        self.assertAlmostEqual(kpi["percent_change"], -7.97, places=2)

        inv_resp = self.client.get("/api/v1/investigations/north_america_east_revenue")
        self.assertEqual(inv_resp.status_code, 200)
        inv = inv_resp.json()
        self.assertEqual(inv["drivers"][0]["driver_name"], "Atlanta DC Stockout")
        self.assertAlmostEqual(inv["drivers"][0]["contribution_pct"], 43.2, places=1)
        self.assertAlmostEqual(inv["drivers"][0]["impact_usd"], -550000.0, delta=100.0)

        rec_resp = self.client.get("/api/v1/recommendations/north_america_east_revenue")
        self.assertEqual(rec_resp.status_code, 200)
        rec = rec_resp.json()
        self.assertEqual(rec["recommendations"][0]["recommendation_id"], "REC-2026-NAE-001")
        self.assertEqual(rec["recommendations"][0]["expected_impact"]["revenue_recovery_usd"], 484000.0)



if __name__ == "__main__":
    unittest.main()
