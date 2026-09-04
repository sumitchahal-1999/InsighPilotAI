"""
InsightPilot AI — Groq AI Provider Implementation
Wraps official Groq Python SDK with dual key pools, high-speed structured generation, and error mapping.
"""

import json
import time
import logging
from typing import Set, List, Optional, Dict, Any
from groq import Groq

from ai.config import ai_config
from ai.providers.base import BaseAIProvider
from ai.providers.types import (
    AIRequest,
    AIResponse,
    Capability,
    TaskType,
    AIProviderError,
    AIErrorCategory
)

logger = logging.getLogger("insightpilot.ai.groq_provider")

class GroqProvider(BaseAIProvider):
    """High-speed Groq provider specialized for business reasoning, executive synthesis, and structured JSON."""

    def __init__(
        self,
        api_keys: Optional[List[str]] = None,
        model_name: Optional[str] = None
    ):
        self._keys = api_keys if api_keys is not None else ai_config.get_groq_keys()
        self.model_name = model_name or ai_config.GROQ_MODEL
        self._clients: Dict[int, Groq] = {}

    @property
    def name(self) -> str:
        return "groq"

    @property
    def supported_capabilities(self) -> Set[Capability]:
        return {
            Capability.TEXT_REASONING,
            Capability.STRUCTURED_JSON,
            Capability.FAST_INFERENCE
        }

    @property
    def supported_tasks(self) -> Set[TaskType]:
        return {
            TaskType.BUSINESS_REASONING,
            TaskType.EXECUTIVE_SYNTHESIS,
            TaskType.PERSONA_ADAPTATION,
            TaskType.INVESTIGATION_EXPLANATION,
            TaskType.RECOMMENDATION_NARRATIVE,
            TaskType.DECISION_NARRATIVE
        }

    @property
    def key_pool_ids(self) -> List[str]:
        return [f"groq_pool_{i+1}" for i in range(len(self._keys))]

    def is_configured(self) -> bool:
        return len(self._keys) > 0

    def _get_client(self, pool_idx: int) -> Groq:
        if pool_idx >= len(self._keys):
            raise AIProviderError(
                f"Invalid Groq key pool index: {pool_idx}. Configured pools: {len(self._keys)}",
                error_category=AIErrorCategory.AUTHENTICATION_ERROR,
                provider=self.name,
                key_pool_id=f"groq_pool_{pool_idx+1}",
                retryable=False
            )
        if pool_idx not in self._clients:
            key = self._keys[pool_idx]
            if not key:
                raise AIProviderError(
                    f"Groq API key at pool {pool_idx+1} is empty.",
                    error_category=AIErrorCategory.AUTHENTICATION_ERROR,
                    provider=self.name,
                    key_pool_id=f"groq_pool_{pool_idx+1}",
                    retryable=False
                )
            self._clients[pool_idx] = Groq(api_key=key)
        return self._clients[pool_idx]

    def _clean_json_text(self, raw_text: str) -> str:
        cleaned = raw_text.strip()
        if cleaned.startswith("```json"):
            cleaned = cleaned[7:]
        elif cleaned.startswith("```"):
            cleaned = cleaned[3:]
        if cleaned.endswith("```"):
            cleaned = cleaned[:-3]
        return cleaned.strip()

    def generate(self, request: AIRequest, key_pool_index: int = 0) -> AIResponse:
        """Executes generation against Groq with structured JSON handling."""
        # 1. Capability Validation: Groq does not support multimodal vision or image generation
        if Capability.MULTIMODAL_VISION in request.required_capabilities or Capability.IMAGE_GENERATION in request.required_capabilities:
            raise AIProviderError(
                "Groq provider does not support multimodal vision or image generation capabilities.",
                error_category=AIErrorCategory.CAPABILITY_UNAVAILABLE,
                provider=self.name,
                key_pool_id=f"groq_pool_{key_pool_index+1}",
                retryable=False
            )

        if not self.is_configured():
            raise AIProviderError(
                "Groq provider has no configured API keys in environment.",
                error_category=AIErrorCategory.AUTHENTICATION_ERROR,
                provider=self.name,
                key_pool_id=f"groq_pool_{key_pool_index+1}",
                retryable=False
            )

        pool_id = f"groq_pool_{key_pool_index+1}"
        client = self._get_client(key_pool_index)
        start_time = time.perf_counter()

        try:
            temperature = request.temperature if request.temperature is not None else ai_config.TEMPERATURE
            max_tokens = request.max_tokens or ai_config.MAX_OUTPUT_TOKENS

            messages = []
            sys_inst = request.system_instruction or "You are InsightPilot AI, an enterprise decision intelligence system."
            if Capability.STRUCTURED_JSON in request.required_capabilities and "json" not in sys_inst.lower() and "json" not in request.prompt.lower():
                sys_inst += " You must respond with a valid JSON object."

            messages.append({"role": "system", "content": sys_inst})
            messages.append({"role": "user", "content": request.prompt})

            candidate_models = [
                self.model_name,
                "openai/gpt-oss-120b",
                "openai/gpt-oss-20b",
                "qwen/qwen3.8-27b",
                "llama-3.3-70b-versatile",
                "llama-3.1-8b-instant"
            ]

            completion = None
            used_model = self.model_name
            last_err = None

            for m in candidate_models:
                try:
                    kwargs: Dict[str, Any] = {
                        "model": m,
                        "messages": messages,
                        "temperature": temperature,
                        "max_tokens": max_tokens
                    }
                    if Capability.STRUCTURED_JSON in request.required_capabilities:
                        kwargs["response_format"] = {"type": "json_object"}

                    completion = client.chat.completions.create(**kwargs)
                    used_model = m
                    break
                except Exception as call_err:
                    last_err = call_err
                    err_str = str(call_err).lower()
                    if "model_not_found" in err_str or "model_decommissioned" in err_str or "decommissioned" in err_str or "404" in err_str:
                        continue
                    raise

            if completion is None and last_err is not None:
                raise last_err

            elapsed_ms = round((time.perf_counter() - start_time) * 1000.0, 2)
            raw_text = completion.choices[0].message.content or "{}"
            cleaned_text = self._clean_json_text(raw_text)

            parsed_json = None
            if Capability.STRUCTURED_JSON in request.required_capabilities:
                try:
                    parsed_json = json.loads(cleaned_text)
                except json.JSONDecodeError as jde:
                    raise AIProviderError(
                        f"Failed to parse structured JSON from Groq: {jde}",
                        error_category=AIErrorCategory.INVALID_REQUEST,
                        provider=self.name,
                        key_pool_id=pool_id,
                        retryable=False
                    )

            usage = getattr(completion, "usage", None)
            raw_usage = {
                "prompt_tokens": getattr(usage, "prompt_tokens", None) if usage else None,
                "completion_tokens": getattr(usage, "completion_tokens", None) if usage else None,
                "total_tokens": getattr(usage, "total_tokens", None) if usage else None
            }

            return AIResponse(
                content=cleaned_text,
                parsed_json=parsed_json,
                provider=self.name,
                model=used_model,
                key_pool_id=pool_id,
                latency_ms=elapsed_ms,
                success=True,
                raw_usage=raw_usage
            )

        except AIProviderError:
            raise
        except Exception as e:
            err_msg = str(e).lower()
            if "rate_limit_exceeded" in err_msg or "429" in err_msg:
                cat = AIErrorCategory.RATE_LIMITED
            elif "quota" in err_msg or "insufficient_quota" in err_msg:
                cat = AIErrorCategory.QUOTA_EXCEEDED
            elif "timeout" in err_msg or "timed out" in err_msg:
                cat = AIErrorCategory.TIMEOUT
            elif "authentication" in err_msg or "invalid_api_key" in err_msg or "401" in err_msg:
                cat = AIErrorCategory.AUTHENTICATION_ERROR
            else:
                cat = AIErrorCategory.PROVIDER_UNAVAILABLE

            raise AIProviderError(
                f"Groq API invocation failed ({pool_id}): {str(e)}",
                error_category=cat,
                provider=self.name,
                key_pool_id=pool_id,
                retryable=(cat in (AIErrorCategory.RATE_LIMITED, AIErrorCategory.QUOTA_EXCEEDED, AIErrorCategory.TIMEOUT, AIErrorCategory.PROVIDER_UNAVAILABLE))
            )
