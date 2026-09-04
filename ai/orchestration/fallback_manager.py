"""
InsightPilot AI — AI Fallback & Failover Manager
Orchestrates request-level key pool failover and cross-provider resilience with bounded retry policies.
"""

import logging
from typing import Dict, Any, List, Optional
from ai.config import ai_config
from ai.providers.base import BaseAIProvider
from ai.providers.types import (
    AIRequest,
    AIResponse,
    AIProviderError,
    AIErrorCategory
)
from ai.orchestration.telemetry import telemetry_manager

logger = logging.getLogger("insightpilot.ai.fallback_manager")

class FallbackManager:
    """Manages sequential key pool failovers and capability-aware cross-provider fallbacks."""

    def __init__(
        self,
        providers: Dict[str, BaseAIProvider],
        fallback_enabled: Optional[bool] = None
    ):
        self.providers = providers
        self.fallback_enabled = (
            fallback_enabled if fallback_enabled is not None else ai_config.FALLBACK_ENABLED
        )

    def execute_with_fallback(
        self,
        request: AIRequest,
        primary_provider_name: str,
        fallback_provider_name: Optional[str] = None
    ) -> AIResponse:
        """
        Executes request trying primary provider key pools first, then fallback provider if allowed.
        """
        fallback_chain: List[str] = []
        errors: List[str] = []

        # 1. Determine execution sequence of (provider_name, key_pool_index)
        execution_plan: List[tuple[str, int]] = []

        primary_provider = self.providers.get(primary_provider_name)
        if primary_provider and primary_provider.is_configured():
            for idx in range(len(primary_provider.key_pool_ids)):
                execution_plan.append((primary_provider_name, idx))

        if self.fallback_enabled and fallback_provider_name:
            fallback_provider = self.providers.get(fallback_provider_name)
            if fallback_provider and fallback_provider.is_configured():
                for idx in range(len(fallback_provider.key_pool_ids)):
                    execution_plan.append((fallback_provider_name, idx))

        if not execution_plan:
            # No configured providers
            err = AIProviderError(
                f"No configured AI providers available for task '{request.task_type.value}' "
                f"(Attempted primary: {primary_provider_name}, fallback: {fallback_provider_name}).",
                error_category=AIErrorCategory.AUTHENTICATION_ERROR,
                provider=primary_provider_name,
                key_pool_id="none",
                retryable=False
            )
            telemetry_manager.record_failure(request.task_type, err)
            raise err

        # 2. Iterate through execution plan
        for step_num, (prov_name, key_idx) in enumerate(execution_plan):
            prov = self.providers[prov_name]
            pool_id = f"{prov_name}_pool_{key_idx+1}"

            try:
                logger.info(f"[AI Router] Attempting {pool_id} for task {request.task_type.value} (Step {step_num+1}/{len(execution_plan)})")
                response = prov.generate(request, key_pool_index=key_idx)

                # Annotate fallback metadata
                is_fallback = step_num > 0
                response.fallback_used = is_fallback
                response.fallback_chain = fallback_chain

                telemetry_manager.record_success(request.task_type, response, failover_occurred=is_fallback)
                return response

            except AIProviderError as pe:
                fallback_chain.append(f"{pool_id}:{pe.error_category.value}")
                errors.append(f"{pool_id} error ({pe.error_category.value}): {pe.message}")

                # Non-retryable errors (e.g. Capability Unavailable, Invalid Request) should fail immediately
                if not pe.retryable or not self.fallback_enabled:
                    telemetry_manager.record_failure(request.task_type, pe)
                    raise pe

                logger.warning(
                    f"[AI Router] Failover triggered from {pool_id} due to {pe.error_category.value}: {pe.message}"
                )

        # 3. If all attempts failed
        final_err_msg = " | ".join(errors)
        overall_error = AIProviderError(
            f"All AI provider key pools exhausted for task '{request.task_type.value}': {final_err_msg}",
            error_category=AIErrorCategory.PROVIDER_UNAVAILABLE,
            provider=primary_provider_name,
            key_pool_id=f"exhausted({len(execution_plan)}_pools)",
            retryable=False
        )
        telemetry_manager.record_failure(request.task_type, overall_error)
        raise overall_error
