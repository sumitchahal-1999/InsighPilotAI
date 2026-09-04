"""
InsightPilot AI — Safe AI Provider Telemetry
Tracks request metrics, key pool utilization, latencies, and failover counts without storing secrets.
"""

import time
import logging
from typing import Dict, Any, List, Optional
from collections import defaultdict
from ai.providers.types import AIResponse, AIProviderError, TaskType

logger = logging.getLogger("insightpilot.ai.telemetry")

class TelemetryManager:
    """Safe, non-leaking telemetry manager for AI provider orchestration."""

    def __init__(self):
        self._total_requests: int = 0
        self._successful_requests: int = 0
        self._failed_requests: int = 0
        self._failover_events: int = 0
        self._key_pool_counts: Dict[str, int] = defaultdict(int)
        self._provider_counts: Dict[str, int] = defaultdict(int)
        self._task_counts: Dict[str, int] = defaultdict(int)
        self._error_counts: Dict[str, int] = defaultdict(int)
        self._recent_latencies: List[float] = []

    def record_success(
        self,
        request_task: TaskType,
        response: AIResponse,
        failover_occurred: bool = False
    ) -> None:
        """Records a successful AI generation event."""
        self._total_requests += 1
        self._successful_requests += 1
        self._provider_counts[response.provider] += 1
        self._key_pool_counts[response.key_pool_id] += 1
        self._task_counts[request_task.value] += 1

        if failover_occurred or response.fallback_used:
            self._failover_events += 1

        self._recent_latencies.append(response.latency_ms)
        if len(self._recent_latencies) > 200:
            self._recent_latencies.pop(0)

        logger.info(
            f"[AI Telemetry] SUCCESS | Task={request_task.value} | Provider={response.provider} | "
            f"Pool={response.key_pool_id} | Latency={response.latency_ms}ms | Fallback={response.fallback_used}"
        )

    def record_failure(
        self,
        request_task: TaskType,
        error: AIProviderError
    ) -> None:
        """Records an unrecovered AI generation failure."""
        self._total_requests += 1
        self._failed_requests += 1
        self._provider_counts[error.provider] += 1
        self._key_pool_counts[error.key_pool_id] += 1
        self._task_counts[request_task.value] += 1
        self._error_counts[error.error_category.value] += 1

        logger.warning(
            f"[AI Telemetry] FAILURE | Task={request_task.value} | Provider={error.provider} | "
            f"Pool={error.key_pool_id} | Category={error.error_category.value} | Retryable={error.retryable}"
        )

    def get_summary(self) -> Dict[str, Any]:
        """Returns safe summary metrics without any API keys or credentials."""
        avg_latency = (
            round(sum(self._recent_latencies) / len(self._recent_latencies), 2)
            if self._recent_latencies
            else 0.0
        )
        return {
            "total_requests": self._total_requests,
            "successful_requests": self._successful_requests,
            "failed_requests": self._failed_requests,
            "failover_events": self._failover_events,
            "success_rate_pct": (
                round((self._successful_requests / self._total_requests) * 100.0, 2)
                if self._total_requests > 0
                else 100.0
            ),
            "average_latency_ms": avg_latency,
            "key_pool_utilization": dict(self._key_pool_counts),
            "provider_distribution": dict(self._provider_counts),
            "task_distribution": dict(self._task_counts),
            "error_distribution": dict(self._error_counts)
        }

telemetry_manager = TelemetryManager()
