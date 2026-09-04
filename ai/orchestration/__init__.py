"""
InsightPilot AI — AI Orchestration & Routing Layer
"""

from ai.orchestration.task_classifier import TaskClassifier
from ai.orchestration.fallback_manager import FallbackManager
from ai.orchestration.telemetry import TelemetryManager, telemetry_manager
from ai.orchestration.provider_router import AIProviderRouter, provider_router

__all__ = [
    "TaskClassifier",
    "FallbackManager",
    "TelemetryManager",
    "telemetry_manager",
    "AIProviderRouter",
    "provider_router"
]
