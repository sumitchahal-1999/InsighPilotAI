"""
InsightPilot AI — AI Error Handling Unit Tests
Tests service behavior under unconfigured API keys, Gemini network errors, and malformed outputs.
"""

import unittest
from unittest.mock import MagicMock
from ai.service import AIService, AIServiceUnavailableError
from ai.client import GeminiClient, GeminiAPIError

class TestAIErrorHandling(unittest.TestCase):

    def setUp(self):
        self.sample_inv = {"investigation_id": "INV-001", "kpi": {}, "drivers": []}
        self.sample_ev = []

    def test_missing_api_key_client_error(self):
        client = GeminiClient(api_key="")
        with self.assertRaises(GeminiAPIError) as ctx:
            client.generate_json("test prompt")
        self.assertIn("GEMINI_API_KEY is not configured", str(ctx.exception))

    def test_service_maps_gemini_error_to_unavailable(self):
        mock_client = MagicMock(spec=GeminiClient)
        mock_client.generate_json.side_effect = GeminiAPIError("Network connection timed out.")

        service = AIService(client=mock_client)
        with self.assertRaises(AIServiceUnavailableError) as ctx:
            service.generate_executive_explanation(self.sample_inv, self.sample_ev, persona="CFO")
        self.assertIn("unavailable", str(ctx.exception))

    def test_malformed_json_from_model(self):
        mock_client = MagicMock(spec=GeminiClient)
        mock_client.generate_json.side_effect = GeminiAPIError("Failed to parse JSON response from Gemini model: Unterminated string")

        service = AIService(client=mock_client)
        with self.assertRaises(AIServiceUnavailableError):
            service.generate_executive_explanation(self.sample_inv, self.sample_ev, persona="CFO")

if __name__ == "__main__":
    unittest.main()
