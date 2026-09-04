"""
InsightPilot AI — Google Gemini AI Provider Implementation
Wraps Google GenAI SDK with multi-key pool support, structured generation, and error mapping.
"""

import json
import time
import logging
from typing import Set, List, Optional, Dict, Any
from google import genai
from google.genai import types

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

logger = logging.getLogger("insightpilot.ai.gemini_provider")

class GeminiProvider(BaseAIProvider):
    """Gemini provider supporting multimodal vision, structured reasoning, and dual key pools."""

    def __init__(
        self,
        api_keys: Optional[List[str]] = None,
        model_name: Optional[str] = None
    ):
        self._keys = api_keys if api_keys is not None else ai_config.get_gemini_keys()
        self.model_name = model_name or ai_config.GEMINI_MODEL
        self._clients: Dict[int, genai.Client] = {}

    @property
    def name(self) -> str:
        return "gemini"

    @property
    def supported_capabilities(self) -> Set[Capability]:
        return {
            Capability.TEXT_REASONING,
            Capability.STRUCTURED_JSON,
            Capability.MULTIMODAL_VISION,
            Capability.IMAGE_GENERATION
        }

    @property
    def supported_tasks(self) -> Set[TaskType]:
        return {
            TaskType.MULTIMODAL_ANALYSIS,
            TaskType.IMAGE_ANALYSIS,
            TaskType.VISUAL_DOCUMENT_ANALYSIS,
            TaskType.CHART_ANALYSIS,
            TaskType.IMAGE_GENERATION,
            TaskType.BUSINESS_REASONING,
            TaskType.EXECUTIVE_SYNTHESIS,
            TaskType.PERSONA_ADAPTATION,
            TaskType.INVESTIGATION_EXPLANATION,
            TaskType.RECOMMENDATION_NARRATIVE,
            TaskType.DECISION_NARRATIVE
        }

    @property
    def key_pool_ids(self) -> List[str]:
        return [f"gemini_pool_{i+1}" for i in range(len(self._keys))]

    def is_configured(self) -> bool:
        return len(self._keys) > 0

    def _get_client(self, pool_idx: int) -> genai.Client:
        if pool_idx >= len(self._keys):
            raise AIProviderError(
                f"Invalid Gemini key pool index: {pool_idx}. Configured pools: {len(self._keys)}",
                error_category=AIErrorCategory.AUTHENTICATION_ERROR,
                provider=self.name,
                key_pool_id=f"gemini_pool_{pool_idx+1}",
                retryable=False
            )
        if pool_idx not in self._clients:
            key = self._keys[pool_idx]
            if not key:
                raise AIProviderError(
                    f"Gemini API key at pool {pool_idx+1} is empty.",
                    error_category=AIErrorCategory.AUTHENTICATION_ERROR,
                    provider=self.name,
                    key_pool_id=f"gemini_pool_{pool_idx+1}",
                    retryable=False
                )
            self._clients[pool_idx] = genai.Client(api_key=key)
        return self._clients[pool_idx]

    def _clean_json_text(self, raw_text: str) -> str:
        """Strips markdown code blocks from JSON output."""
        cleaned = raw_text.strip()
        if cleaned.startswith("```json"):
            cleaned = cleaned[7:]
        elif cleaned.startswith("```"):
            cleaned = cleaned[3:]
        if cleaned.endswith("```"):
            cleaned = cleaned[:-3]
        return cleaned.strip()

    def generate(self, request: AIRequest, key_pool_index: int = 0) -> AIResponse:
        """Executes generation against Gemini with structured response handling."""
        if not self.is_configured():
            raise AIProviderError(
                "Gemini provider has no configured API keys in environment.",
                error_category=AIErrorCategory.AUTHENTICATION_ERROR,
                provider=self.name,
                key_pool_id=f"gemini_pool_{key_pool_index+1}",
                retryable=False
            )

        pool_id = f"gemini_pool_{key_pool_index+1}"
        client = self._get_client(key_pool_index)
        start_time = time.perf_counter()

        try:
            temperature = request.temperature if request.temperature is not None else ai_config.TEMPERATURE
            max_tokens = request.max_tokens or ai_config.MAX_OUTPUT_TOKENS

            config = types.GenerateContentConfig(
                temperature=temperature,
                max_output_tokens=max_tokens,
                response_mime_type="application/json" if Capability.STRUCTURED_JSON in request.required_capabilities else "text/plain"
            )

            if request.system_instruction:
                config.system_instruction = request.system_instruction

            response = client.models.generate_content(
                model=self.model_name,
                contents=request.prompt,
                config=config
            )

            elapsed_ms = round((time.perf_counter() - start_time) * 1000.0, 2)
            raw_text = response.text or "{}"
            cleaned_text = self._clean_json_text(raw_text)

            parsed_json = None
            if Capability.STRUCTURED_JSON in request.required_capabilities:
                try:
                    parsed_json = json.loads(cleaned_text)
                except json.JSONDecodeError as jde:
                    raise AIProviderError(
                        f"Failed to parse structured JSON from Gemini: {jde}",
                        error_category=AIErrorCategory.INVALID_REQUEST,
                        provider=self.name,
                        key_pool_id=pool_id,
                        retryable=False
                    )

            usage = getattr(response, "usage_metadata", None)
            raw_usage = {
                "prompt_tokens": getattr(usage, "prompt_token_count", None) if usage else None,
                "completion_tokens": getattr(usage, "candidates_token_count", None) if usage else None,
                "total_tokens": getattr(usage, "total_token_count", None) if usage else None
            }

            return AIResponse(
                content=cleaned_text,
                parsed_json=parsed_json,
                provider=self.name,
                model=self.model_name,
                key_pool_id=pool_id,
                latency_ms=elapsed_ms,
                success=True,
                raw_usage=raw_usage
            )

        except AIProviderError:
            raise
        except Exception as e:
            err_msg = str(e).lower()
            if "resource_exhausted" in err_msg or "quota" in err_msg:
                cat = AIErrorCategory.QUOTA_EXCEEDED
            elif "rate" in err_msg or "429" in err_msg:
                cat = AIErrorCategory.RATE_LIMITED
            elif "deadline" in err_msg or "timeout" in err_msg:
                cat = AIErrorCategory.TIMEOUT
            elif "api_key" in err_msg or "auth" in err_msg or "unauthenticated" in err_msg:
                cat = AIErrorCategory.AUTHENTICATION_ERROR
            else:
                cat = AIErrorCategory.PROVIDER_UNAVAILABLE

            raise AIProviderError(
                f"Gemini API invocation failed ({pool_id}): {str(e)}",
                error_category=cat,
                provider=self.name,
                key_pool_id=pool_id,
                retryable=(cat in (AIErrorCategory.RATE_LIMITED, AIErrorCategory.QUOTA_EXCEEDED, AIErrorCategory.TIMEOUT, AIErrorCategory.PROVIDER_UNAVAILABLE))
            )
