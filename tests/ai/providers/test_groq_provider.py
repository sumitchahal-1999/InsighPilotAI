"""
InsightPilot AI — Groq Provider Unit Tests
Tests Groq provider initialization, dual key pool failover, capability rejection, and error mapping.
"""

import unittest
from unittest.mock import MagicMock, patch
from ai.providers.groq_provider import GroqProvider
from ai.providers.types import (
    AIRequest,
    TaskType,
    Capability,
    AIProviderError,
    AIErrorCategory
)

class TestGroqProvider(unittest.TestCase):

    def test_provider_metadata(self):
        provider = GroqProvider(api_keys=["gsk-test-1", "gsk-test-2"])
        self.assertEqual(provider.name, "groq")
        self.assertTrue(provider.is_configured())
        self.assertEqual(len(provider.key_pool_ids), 2)
        self.assertEqual(provider.key_pool_ids, ["groq_pool_1", "groq_pool_2"])
        self.assertIn(Capability.TEXT_REASONING, provider.supported_capabilities)
        self.assertIn(Capability.STRUCTURED_JSON, provider.supported_capabilities)
        self.assertNotIn(Capability.MULTIMODAL_VISION, provider.supported_capabilities)

    def test_multimodal_capability_rejection(self):
        provider = GroqProvider(api_keys=["gsk-test-1"])
        req = AIRequest(
            task_type=TaskType.IMAGE_ANALYSIS,
            required_capabilities=[Capability.MULTIMODAL_VISION],
            prompt="Describe this image"
        )
        with self.assertRaises(AIProviderError) as ctx:
            provider.generate(req)
        self.assertEqual(ctx.exception.error_category, AIErrorCategory.CAPABILITY_UNAVAILABLE)
        self.assertFalse(ctx.exception.retryable)

    @patch("ai.providers.groq_provider.Groq")
    def test_successful_structured_generation(self, mock_groq_cls):
        mock_groq = MagicMock()
        mock_groq_cls.return_value = mock_groq

        mock_choice = MagicMock()
        mock_choice.message.content = '{"headline": "Atlanta DC Stockout Impact", "contribution": 43.2}'
        mock_completion = MagicMock()
        mock_completion.choices = [mock_choice]
        mock_completion.usage = MagicMock(prompt_tokens=80, completion_tokens=40, total_tokens=120)
        mock_groq.chat.completions.create.return_value = mock_completion

        provider = GroqProvider(api_keys=["gsk-test-1"])
        req = AIRequest(
            task_type=TaskType.BUSINESS_REASONING,
            required_capabilities=[Capability.TEXT_REASONING, Capability.STRUCTURED_JSON],
            prompt="Explain the revenue variance."
        )

        resp = provider.generate(req, key_pool_index=0)
        self.assertTrue(resp.success)
        self.assertEqual(resp.provider, "groq")
        self.assertEqual(resp.key_pool_id, "groq_pool_1")
        self.assertIsNotNone(resp.parsed_json)
        self.assertEqual(resp.parsed_json["headline"], "Atlanta DC Stockout Impact")

    @patch("ai.providers.groq_provider.Groq")
    def test_rate_limit_error_mapping(self, mock_groq_cls):
        mock_groq = MagicMock()
        mock_groq_cls.return_value = mock_groq
        mock_groq.chat.completions.create.side_effect = Exception("rate_limit_exceeded: Rate limit reached for model")

        provider = GroqProvider(api_keys=["gsk-test-1"])
        req = AIRequest(prompt="Test prompt")

        with self.assertRaises(AIProviderError) as ctx:
            provider.generate(req, key_pool_index=0)
        self.assertEqual(ctx.exception.error_category, AIErrorCategory.RATE_LIMITED)
        self.assertTrue(ctx.exception.retryable)

if __name__ == "__main__":
    unittest.main()
