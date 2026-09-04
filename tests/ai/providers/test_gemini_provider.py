"""
InsightPilot AI — Gemini Provider Unit Tests
Tests Gemini provider initialization, dual key pool failover, capability reporting, and error mapping.
"""

import unittest
from unittest.mock import MagicMock, patch
from ai.providers.gemini_provider import GeminiProvider
from ai.providers.types import (
    AIRequest,
    TaskType,
    Capability,
    AIProviderError,
    AIErrorCategory
)

class TestGeminiProvider(unittest.TestCase):

    def test_provider_metadata(self):
        provider = GeminiProvider(api_keys=["test-key-1", "test-key-2"])
        self.assertEqual(provider.name, "gemini")
        self.assertTrue(provider.is_configured())
        self.assertEqual(len(provider.key_pool_ids), 2)
        self.assertEqual(provider.key_pool_ids, ["gemini_pool_1", "gemini_pool_2"])
        self.assertIn(Capability.MULTIMODAL_VISION, provider.supported_capabilities)
        self.assertIn(Capability.TEXT_REASONING, provider.supported_capabilities)
        self.assertIn(Capability.STRUCTURED_JSON, provider.supported_capabilities)

    def test_unconfigured_provider_raises_error(self):
        provider = GeminiProvider(api_keys=[])
        self.assertFalse(provider.is_configured())
        req = AIRequest(prompt="Test prompt")
        with self.assertRaises(AIProviderError) as ctx:
            provider.generate(req)
        self.assertEqual(ctx.exception.error_category, AIErrorCategory.AUTHENTICATION_ERROR)

    @patch("ai.providers.gemini_provider.genai.Client")
    def test_successful_structured_generation(self, mock_client_cls):
        mock_client = MagicMock()
        mock_client_cls.return_value = mock_client

        mock_response = MagicMock()
        mock_response.text = '{"summary": "Revenue declined by 7.97%", "grounded_evidence_ids": ["EVID-REV-01"]}'
        mock_response.usage_metadata = MagicMock(prompt_token_count=100, candidates_token_count=50, total_token_count=150)
        mock_client.models.generate_content.return_value = mock_response

        provider = GeminiProvider(api_keys=["test-key-1"])
        req = AIRequest(
            task_type=TaskType.MULTIMODAL_ANALYSIS,
            required_capabilities=[Capability.TEXT_REASONING, Capability.STRUCTURED_JSON],
            prompt="Analyze the chart."
        )

        resp = provider.generate(req, key_pool_index=0)
        self.assertTrue(resp.success)
        self.assertEqual(resp.provider, "gemini")
        self.assertEqual(resp.key_pool_id, "gemini_pool_1")
        self.assertIsNotNone(resp.parsed_json)
        self.assertEqual(resp.parsed_json["summary"], "Revenue declined by 7.97%")

    @patch("ai.providers.gemini_provider.genai.Client")
    def test_rate_limit_error_categorization(self, mock_client_cls):
        mock_client = MagicMock()
        mock_client_cls.return_value = mock_client
        mock_client.models.generate_content.side_effect = Exception("RESOURCE_EXHAUSTED: Quota exceeded for quota metric")

        provider = GeminiProvider(api_keys=["test-key-1"])
        req = AIRequest(prompt="Test prompt")

        with self.assertRaises(AIProviderError) as ctx:
            provider.generate(req, key_pool_index=0)
        self.assertEqual(ctx.exception.error_category, AIErrorCategory.QUOTA_EXCEEDED)
        self.assertTrue(ctx.exception.retryable)

if __name__ == "__main__":
    unittest.main()
