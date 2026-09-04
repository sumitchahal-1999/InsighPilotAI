"""
InsightPilot AI — AI Provider Router
Central routing hub coordinating task classification, provider selection, failover, and telemetry.
"""

from typing import Dict, Any, Optional
from ai.providers.base import BaseAIProvider
from ai.providers.gemini_provider import GeminiProvider
from ai.providers.groq_provider import GroqProvider
from ai.providers.types import AIRequest, AIResponse, TaskType, Capability
from ai.orchestration.task_classifier import TaskClassifier
from ai.orchestration.fallback_manager import FallbackManager
from ai.orchestration.telemetry import telemetry_manager

class AIProviderRouter:
    """Capability-aware multi-model AI provider router."""

    def __init__(
        self,
        gemini_provider: Optional[BaseAIProvider] = None,
        groq_provider: Optional[BaseAIProvider] = None,
        fallback_enabled: Optional[bool] = None
    ):
        self.providers: Dict[str, BaseAIProvider] = {
            "gemini": gemini_provider or GeminiProvider(),
            "groq": groq_provider or GroqProvider()
        }
        self.classifier = TaskClassifier()
        self.fallback_manager = FallbackManager(
            providers=self.providers,
            fallback_enabled=fallback_enabled
        )

    def route_and_execute(self, request: AIRequest) -> AIResponse:
        """Classifies task, resolves required capabilities, and executes via fallback manager."""
        # 1. Enrich request with default required capabilities if not explicitly provided
        if not request.required_capabilities:
            request.required_capabilities = self.classifier.get_required_capabilities(request.task_type)

        # 2. Determine provider routing
        primary_name, fallback_name = self.classifier.get_provider_routing(request.task_type)

        # 3. Execute with request-level failover
        return self.fallback_manager.execute_with_fallback(
            request=request,
            primary_provider_name=primary_name,
            fallback_provider_name=fallback_name
        )

    def get_status(self) -> Dict[str, Any]:
        """Returns safe provider health and key pool status."""
        return {
            "providers": {
                name: {
                    "configured": p.is_configured(),
                    "key_pools": len(p.key_pool_ids),
                    "supported_capabilities": [c.value for c in p.supported_capabilities]
                }
                for name, p in self.providers.items()
            },
            "telemetry": telemetry_manager.get_summary()
        }

provider_router = AIProviderRouter()
ProviderRouter = AIProviderRouter
