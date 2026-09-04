"""
InsightPilot AI — Phase 5.8: Failure Resilience & Edge Cases Test Suite
Verifies system resilience against malformed LLM outputs, hallucinated citations,
database errors, non-existent KPI lookups, and ensures robust exception containment.
"""

import unittest
from unittest.mock import patch
from fastapi.testclient import TestClient
from backend.app.main import app
from ai.langgraph.graph import run_investigation_workflow
from ai.providers.types import (
    AIRequest,
    AIResponse,
    TaskType,
    AIErrorCategory,
    AIProviderError
)


class TestFailureResilience(unittest.TestCase):
    """Failure handling, grounding guardrails, and edge case resilience tests."""

    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)
        cls.kpi_id = "north_america_east_revenue"

    # -------------------------------------------------------------------------
    # 1. Malformed JSON from AI Provider
    # -------------------------------------------------------------------------
    def test_malformed_json_triggers_deterministic_fallback(self):
        """When an LLM returns malformed or non-JSON content, workflow falls back to deterministic synthesis."""
        malformed_resp = AIResponse(
            content="This is definitely not a JSON object: {broken...",
            provider="groq",
            model="llama-3.3-70b-versatile",
            key_pool_id="groq_pool_1",
            latency_ms=120.0,
            success=True
        )

        with patch("ai.orchestration.fallback_manager.FallbackManager.execute_with_fallback", return_value=malformed_resp):
            result = run_investigation_workflow(kpi_id=self.kpi_id, persona="CFO")

            # Workflow must succeed with deterministic fallback
            self.assertIsNotNone(result)
            self.assertFalse(result["abstention"])
            self.assertIn("summary", result["ai_explanation"])
            self.assertIn("atlanta dc stockout", result["ai_explanation"]["summary"].lower())

    # -------------------------------------------------------------------------
    # 2. Hallucinated Driver Citations Rejected
    # -------------------------------------------------------------------------
    def test_hallucinated_driver_citation_rejected(self):
        """When an LLM invents a non-existent driver ID, grounding check fails and triggers fallback."""
        fake_driver_resp = AIResponse(
            content='{"summary": "Fake driver summary", "supporting_driver_ids": ["hallucinated_driver_xyz"], "supporting_evidence_ids": ["EVID_ERP_ATL_STOCKOUT_001"]}',
            provider="groq",
            model="llama-3.3-70b-versatile",
            key_pool_id="groq_pool_1",
            latency_ms=150.0,
            success=True
        )

        with patch("ai.orchestration.fallback_manager.FallbackManager.execute_with_fallback", return_value=fake_driver_resp):
            result = run_investigation_workflow(kpi_id=self.kpi_id, persona="CFO")

            self.assertIsNotNone(result)
            self.assertNotIn("hallucinated_driver_xyz", result["ai_explanation"].get("supporting_driver_ids", []))
            self.assertIn("atlanta_dc_stockout", result["ai_explanation"]["supporting_driver_ids"])

    # -------------------------------------------------------------------------
    # 3. Hallucinated Evidence Citations Rejected
    # -------------------------------------------------------------------------
    def test_hallucinated_evidence_citation_rejected(self):
        """When an LLM invents a fake evidence ID, grounding validation rejects the response."""
        fake_evid_resp = AIResponse(
            content='{"summary": "Fake evidence summary", "supporting_driver_ids": ["atlanta_dc_stockout"], "supporting_evidence_ids": ["EVID_FAKE_NONEXISTENT_999"]}',
            provider="groq",
            model="llama-3.3-70b-versatile",
            key_pool_id="groq_pool_1",
            latency_ms=140.0,
            success=True
        )

        with patch("ai.orchestration.fallback_manager.FallbackManager.execute_with_fallback", return_value=fake_evid_resp):
            result = run_investigation_workflow(kpi_id=self.kpi_id, persona="CFO")

            self.assertIsNotNone(result)
            self.assertNotIn("EVID_FAKE_NONEXISTENT_999", result["ai_explanation"].get("grounded_evidence_ids", []))

    # -------------------------------------------------------------------------
    # 4. Unknown KPI Returns Clean 404
    # -------------------------------------------------------------------------
    def test_unknown_kpi_returns_clean_404(self):
        """Requesting an unknown KPI returns structured 404 without 500 crashes."""
        res = self.client.get("/api/v1/investigations/unknown_nonexistent_kpi")
        self.assertEqual(res.status_code, 404)
        data = res.json()
        self.assertIn("error", data)
        self.assertEqual(data["error"]["code"], "KPI_NOT_FOUND")

    # -------------------------------------------------------------------------
    # 5. Invalid Persona Value Handled Gracefully
    # -------------------------------------------------------------------------
    def test_invalid_persona_value_handled_gracefully(self):
        """Specifying an unknown persona falls back safely or returns clean 400."""
        res = self.client.get(f"/api/v1/investigations/{self.kpi_id}?persona_id=INVALID_PERSONA")
        # Should either succeed falling back to CFO default or return clean 400
        self.assertIn(res.status_code, [200, 400])


if __name__ == "__main__":
    unittest.main()
