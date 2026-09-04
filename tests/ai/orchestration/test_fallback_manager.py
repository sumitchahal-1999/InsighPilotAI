"""
InsightPilot AI — Fallback Manager Unit Tests
Tests primary key pool failover (Pool 1 -> Pool 2) and cross-provider failover (Groq -> Gemini).
"""

import unittest
from unittest.mock import MagicMock
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
        return {TaskType.BUSINESS_REASONING}

    @property
    def key_pool_ids(self):
        return self._key_pools

    def is_configured(self) -> bool:
        return len(self._key_pools) > 0

    def generate(self, request: AIRequest, key_pool_index: int = 0) -> AIResponse:
        return self.generate_mock(request, key_pool_index)

class TestFallbackManager(unittest.TestCase):

    def test_primary_pool_1_success_no_fallback(self):
        groq_prov = DummyProvider("groq", 2)
        gemini_prov = DummyProvider("gemini", 2)

        groq_prov.generate_mock.return_value = AIResponse(
            content="Groq response",
            provider="groq",
            model="llama-3.3-70b",
            key_pool_id="groq_pool_1",
            latency_ms=120.0,
            success=True
        )

        manager = FallbackManager(providers={"groq": groq_prov, "gemini": gemini_prov})
        req = AIRequest(task_type=TaskType.BUSINESS_REASONING, prompt="test")

        resp = manager.execute_with_fallback(req, "groq", "gemini")
        self.assertEqual(resp.provider, "groq")
        self.assertEqual(resp.key_pool_id, "groq_pool_1")
        self.assertFalse(resp.fallback_used)
        self.assertEqual(groq_prov.generate_mock.call_count, 1)

    def test_key_pool_failover_groq_pool_1_to_pool_2(self):
        groq_prov = DummyProvider("groq", 2)
        gemini_prov = DummyProvider("gemini", 2)

        # First call fails with rate limit, second call succeeds
        def groq_side_effect(request, key_pool_index):
            if key_pool_index == 0:
                raise AIProviderError("Rate limit hit", AIErrorCategory.RATE_LIMITED, "groq", "groq_pool_1", True)
            return AIResponse(
                content="Groq Pool 2 response",
                provider="groq",
                model="llama-3.3-70b",
                key_pool_id="groq_pool_2",
                latency_ms=150.0,
                success=True
            )

        groq_prov.generate_mock.side_effect = groq_side_effect

        manager = FallbackManager(providers={"groq": groq_prov, "gemini": gemini_prov})
        req = AIRequest(task_type=TaskType.BUSINESS_REASONING, prompt="test")

        resp = manager.execute_with_fallback(req, "groq", "gemini")
        self.assertEqual(resp.provider, "groq")
        self.assertEqual(resp.key_pool_id, "groq_pool_2")
        self.assertTrue(resp.fallback_used)
        self.assertEqual(len(resp.fallback_chain), 1)
        self.assertIn("groq_pool_1:RATE_LIMITED", resp.fallback_chain[0])
        self.assertEqual(groq_prov.generate_mock.call_count, 2)
        self.assertEqual(gemini_prov.generate_mock.call_count, 0)

    def test_cross_provider_failover_groq_to_gemini(self):
        groq_prov = DummyProvider("groq", 2)
        gemini_prov = DummyProvider("gemini", 2)

        # Both groq pools fail
        groq_prov.generate_mock.side_effect = AIProviderError(
            "Quota exceeded", AIErrorCategory.QUOTA_EXCEEDED, "groq", "groq_pool", True
        )

        gemini_prov.generate_mock.return_value = AIResponse(
            content="Gemini fallback response",
            provider="gemini",
            model="gemini-2.5-flash",
            key_pool_id="gemini_pool_1",
            latency_ms=200.0,
            success=True
        )

        manager = FallbackManager(providers={"groq": groq_prov, "gemini": gemini_prov})
        req = AIRequest(task_type=TaskType.BUSINESS_REASONING, prompt="test")

        resp = manager.execute_with_fallback(req, "groq", "gemini")
        self.assertEqual(resp.provider, "gemini")
        self.assertEqual(resp.key_pool_id, "gemini_pool_1")
        self.assertTrue(resp.fallback_used)
        self.assertEqual(len(resp.fallback_chain), 2)
        self.assertEqual(gemini_prov.generate_mock.call_count, 1)

    def test_non_retryable_error_does_not_failover(self):
        groq_prov = DummyProvider("groq", 2)
        gemini_prov = DummyProvider("gemini", 2)

        groq_prov.generate_mock.side_effect = AIProviderError(
            "Invalid prompt schema", AIErrorCategory.INVALID_REQUEST, "groq", "groq_pool_1", False
        )

        manager = FallbackManager(providers={"groq": groq_prov, "gemini": gemini_prov})
        req = AIRequest(task_type=TaskType.BUSINESS_REASONING, prompt="test")

        with self.assertRaises(AIProviderError) as ctx:
            manager.execute_with_fallback(req, "groq", "gemini")
        self.assertEqual(ctx.exception.error_category, AIErrorCategory.INVALID_REQUEST)
        self.assertEqual(groq_prov.generate_mock.call_count, 1)
        self.assertEqual(gemini_prov.generate_mock.call_count, 0)

if __name__ == "__main__":
    unittest.main()
