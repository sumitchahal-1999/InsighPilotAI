"""
InsightPilot AI — AI Reasoning Service
Orchestrates context assembly, prompt execution, Gemini inference, and post-generation grounding.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
from ai.config import ai_config
from ai.client import GeminiClient, GeminiAPIError
from ai.context import GroundedContextBuilder
from ai.validator import GroundingValidator, GroundingValidationError
from ai.prompts.investigation_explanation_v1 import build_structured_investigation_prompt
from ai.prompts.executive_explanation import build_executive_explanation_prompt
from ai.prompts.driver_explanation import build_driver_explanation_prompt
from ai.prompts.investigation_summary import build_investigation_summary_prompt
from ai.schemas.explanation import (
    StructuredInvestigationExplanation,
    StructuredAIExplanationResponse,
    ExecutiveExplanation,
    DriverExplanation,
    InvestigationSummary,
    AIResponseMetadata,
    AIExplanationResponse,
    AIDriverExplanationResponse
)

class AIServiceError(Exception):
    """Base exception for AI reasoning service failures."""
    pass

class AIServiceUnavailableError(AIServiceError):
    """Raised when the Gemini API is unconfigured or unreachable."""
    pass

class AIGroundingError(AIServiceError):
    """Raised when the generated narrative fails grounding validation."""
    pass

class AIService:
    """High-level service for executing grounded executive reasoning over deterministic outputs."""

    def __init__(self, client: Optional[GeminiClient] = None):
        self.client = client or GeminiClient()
        self.context_builder = GroundedContextBuilder()
        self.validator = GroundingValidator()

    def generate_structured_explanation(
        self,
        investigation_result: Dict[str, Any],
        evidence_items: List[Dict[str, Any]],
        persona: str = "CFO",
        recommendations: Optional[List[Dict[str, Any]]] = None,
        simulation: Optional[Dict[str, Any]] = None
    ) -> StructuredAIExplanationResponse:
        """Generates canonical structured evidence-grounded explanation."""
        context = self.context_builder.build_investigation_context(
            investigation_result=investigation_result,
            evidence_items=evidence_items,
            persona=persona,
            recommendations=recommendations,
            simulation=simulation
        )

        prompt = build_structured_investigation_prompt(context)

        try:
            raw_json, telemetry = self.client.generate_json(prompt)
        except GeminiAPIError as ge:
            raise AIServiceUnavailableError(f"AI Reasoning Service unavailable: {ge}")

        try:
            validated_json = self.validator.validate_grounding(raw_json, context)
        except GroundingValidationError as gve:
            raise AIGroundingError(f"Post-generation grounding check failed: {gve}")

        explanation = StructuredInvestigationExplanation(**validated_json)

        utc_now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        metadata = AIResponseMetadata(
            model=telemetry.get("model", ai_config.MODEL_NAME),
            generated_at=utc_now,
            latency_ms=telemetry.get("latency_ms", 0.0),
            prompt_tokens=telemetry.get("prompt_tokens"),
            completion_tokens=telemetry.get("completion_tokens"),
            total_tokens=telemetry.get("total_tokens"),
            grounded_evidence_count=len(explanation.grounded_evidence_ids),
            validation_status="VERIFIED_GROUNDED"
        )

        return StructuredAIExplanationResponse(
            investigation_id=context["investigation_id"],
            persona=persona,
            explanation=explanation,
            metadata=metadata
        )

    def generate_executive_explanation(
        self,
        investigation_result: Dict[str, Any],
        evidence_items: List[Dict[str, Any]],
        persona: str = "CFO"
    ) -> AIExplanationResponse:
        """Generates a grounded executive explanation for the given investigation."""
        # 1. Build authoritative context
        context = self.context_builder.build_investigation_context(
            investigation_result=investigation_result,
            evidence_items=evidence_items,
            persona=persona
        )

        # 2. Build Prompt
        prompt = build_executive_explanation_prompt(context)

        # 3. Call Gemini Client
        try:
            raw_json, telemetry = self.client.generate_json(prompt)
        except GeminiAPIError as ge:
            raise AIServiceUnavailableError(f"AI Reasoning Service unavailable: {ge}")

        # 4. Grounding Validation
        try:
            validated_json = self.validator.validate_grounding(raw_json, context)
        except GroundingValidationError as gve:
            raise AIGroundingError(f"Post-generation grounding check failed: {gve}")

        # 5. Schema Serialization
        explanation = ExecutiveExplanation(**validated_json)

        utc_now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        metadata = AIResponseMetadata(
            model=telemetry.get("model", ai_config.MODEL_NAME),
            generated_at=utc_now,
            latency_ms=telemetry.get("latency_ms", 0.0),
            prompt_tokens=telemetry.get("prompt_tokens"),
            completion_tokens=telemetry.get("completion_tokens"),
            total_tokens=telemetry.get("total_tokens"),
            grounded_evidence_count=len(explanation.grounded_evidence_ids),
            validation_status="VERIFIED_GROUNDED"
        )

        return AIExplanationResponse(
            investigation_id=context["investigation_id"],
            persona=persona,
            explanation=explanation,
            metadata=metadata
        )

    def generate_driver_explanation(
        self,
        investigation_result: Dict[str, Any],
        evidence_items: List[Dict[str, Any]],
        driver_id: str,
        persona: str = "CFO"
    ) -> AIDriverExplanationResponse:
        """Generates a detailed grounded explanation for a specific driver."""
        context = self.context_builder.build_investigation_context(
            investigation_result=investigation_result,
            evidence_items=evidence_items,
            persona=persona
        )

        prompt = build_driver_explanation_prompt(context, driver_id)

        try:
            raw_json, telemetry = self.client.generate_json(prompt)
        except GeminiAPIError as ge:
            raise AIServiceUnavailableError(f"AI Reasoning Service unavailable: {ge}")

        try:
            validated_json = self.validator.validate_grounding(raw_json, context)
        except GroundingValidationError as gve:
            raise AIGroundingError(f"Post-generation grounding check failed: {gve}")

        explanation = DriverExplanation(**validated_json)

        utc_now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        metadata = AIResponseMetadata(
            model=telemetry.get("model", ai_config.MODEL_NAME),
            generated_at=utc_now,
            latency_ms=telemetry.get("latency_ms", 0.0),
            prompt_tokens=telemetry.get("prompt_tokens"),
            completion_tokens=telemetry.get("completion_tokens"),
            total_tokens=telemetry.get("total_tokens"),
            grounded_evidence_count=len(explanation.grounded_evidence_ids),
            validation_status="VERIFIED_GROUNDED"
        )

        return AIDriverExplanationResponse(
            investigation_id=context["investigation_id"],
            driver_id=driver_id,
            persona=persona,
            explanation=explanation,
            metadata=metadata
        )
