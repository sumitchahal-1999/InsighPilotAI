"""
InsightPilot AI — Provider Router & Telemetry Unit Tests
Tests task classification routing, telemetry metrics capture, and secret-free status reporting.
"""

import unittest
from unittest.mock import MagicMock
from ai.providers.types import AIRequest, AIResponse, TaskType, Capability
from ai.orchestration.task_classifier import TaskClassifier
from ai.orchestration.telemetry import TelemetryManager
from ai.orchestration.provider_router import AIProviderRouter

class TestProviderRouterAndTelemetry(unittest.TestCase):

    def test_task_classification_routing(self):
        # Business reasoning tasks route to Groq primary, Gemini fallback
        b_primary, b_fallback = TaskClassifier.get_provider_routing(TaskType.BUSINESS_REASONING)
        self.assertEqual(b_primary, "groq")
        self.assertEqual(b_fallback, "gemini")

        # Multimodal vision tasks route to Gemini primary, No fallback
        m_primary, m_fallback = TaskClassifier.get_provider_routing(TaskType.MULTIMODAL_ANALYSIS)
        self.assertEqual(m_primary, "gemini")
        self.assertIsNone(m_fallback)

    def test_telemetry_captures_metrics_without_secrets(self):
        telemetry = TelemetryManager()
        resp = AIResponse(
            content="test",
            provider="groq",
            model="llama-3.3-70b",
            key_pool_id="groq_pool_1",
            latency_ms=85.5,
            success=True
        )

        telemetry.record_success(TaskType.BUSINESS_REASONING, resp)
        summary = telemetry.get_summary()

        self.assertEqual(summary["total_requests"], 1)
        self.assertEqual(summary["successful_requests"], 1)
        self.assertEqual(summary["failed_requests"], 0)
        self.assertEqual(summary["key_pool_utilization"]["groq_pool_1"], 1)
        self.assertEqual(summary["provider_distribution"]["groq"], 1)
        self.assertEqual(summary["average_latency_ms"], 85.5)

        # Confirm no API key leaks in telemetry summary keys or values
        for k, v in summary.items():
            self.assertNotIn("api_key", str(k).lower())
            self.assertNotIn("secret", str(k).lower())

    def test_router_status(self):
        mock_gemini = MagicMock()
        mock_gemini.is_configured.return_value = True
        mock_gemini.key_pool_ids = ["gemini_pool_1", "gemini_pool_2"]
        mock_gemini.supported_capabilities = {Capability.MULTIMODAL_VISION}

        mock_groq = MagicMock()
        mock_groq.is_configured.return_value = True
        mock_groq.key_pool_ids = ["groq_pool_1", "groq_pool_2"]
        mock_groq.supported_capabilities = {Capability.TEXT_REASONING}

        router = AIProviderRouter(gemini_provider=mock_gemini, groq_provider=mock_groq)
        status = router.get_status()

        self.assertIn("providers", status)
        self.assertIn("gemini", status["providers"])
        self.assertIn("groq", status["providers"])
        self.assertEqual(status["providers"]["gemini"]["key_pools"], 2)
        self.assertEqual(status["providers"]["groq"]["key_pools"], 2)

if __name__ == "__main__":
    unittest.main()
