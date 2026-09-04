"""
InsightPilot AI — AI Provider Types & Data Models
Defines capability types, task classifications, requests, responses, and error categories.
"""

from enum import Enum
from typing import Dict, Any, List, Optional, Set
from pydantic import BaseModel, Field

class TaskType(str, Enum):
    """Categorization of AI tasks handled by the system."""
    BUSINESS_REASONING = "BUSINESS_REASONING"
    EXECUTIVE_SYNTHESIS = "EXECUTIVE_SYNTHESIS"
    PERSONA_ADAPTATION = "PERSONA_ADAPTATION"
    INVESTIGATION_EXPLANATION = "INVESTIGATION_EXPLANATION"
    RECOMMENDATION_NARRATIVE = "RECOMMENDATION_NARRATIVE"
    DECISION_NARRATIVE = "DECISION_NARRATIVE"
    MULTIMODAL_ANALYSIS = "MULTIMODAL_ANALYSIS"
    IMAGE_ANALYSIS = "IMAGE_ANALYSIS"
    VISUAL_DOCUMENT_ANALYSIS = "VISUAL_DOCUMENT_ANALYSIS"
    CHART_ANALYSIS = "CHART_ANALYSIS"
    IMAGE_GENERATION = "IMAGE_GENERATION"

class Capability(str, Enum):
    """Model and provider capability flags."""
    TEXT_REASONING = "TEXT_REASONING"
    STRUCTURED_JSON = "STRUCTURED_JSON"
    FAST_INFERENCE = "FAST_INFERENCE"
    MULTIMODAL_VISION = "MULTIMODAL_VISION"
    IMAGE_GENERATION = "IMAGE_GENERATION"

class AIErrorCategory(str, Enum):
    """Normalized provider error classifications."""
    RATE_LIMITED = "RATE_LIMITED"
    QUOTA_EXCEEDED = "QUOTA_EXCEEDED"
    TIMEOUT = "TIMEOUT"
    PROVIDER_UNAVAILABLE = "PROVIDER_UNAVAILABLE"
    AUTHENTICATION_ERROR = "AUTHENTICATION_ERROR"
    INVALID_REQUEST = "INVALID_REQUEST"
    CAPABILITY_UNAVAILABLE = "CAPABILITY_UNAVAILABLE"
    GROUNDING_FAILED = "GROUNDING_FAILED"

class AIProviderError(Exception):
    """Structured exception raised by AI providers during generation."""
    def __init__(
        self,
        message: str,
        error_category: AIErrorCategory = AIErrorCategory.PROVIDER_UNAVAILABLE,
        provider: str = "unknown",
        key_pool_id: str = "unknown",
        retryable: bool = True
    ):
        super().__init__(message)
        self.message = message
        self.error_category = error_category
        self.provider = provider
        self.key_pool_id = key_pool_id
        self.retryable = retryable

    def to_dict(self) -> Dict[str, Any]:
        return {
            "error_category": self.error_category.value,
            "provider": self.provider,
            "key_pool_id": self.key_pool_id,
            "message": self.message,
            "retryable": self.retryable
        }

class AIRequest(BaseModel):
    """Structured request payload for multi-model AI generation."""
    task_type: TaskType = Field(default=TaskType.BUSINESS_REASONING)
    required_capabilities: List[Capability] = Field(default_factory=lambda: [Capability.TEXT_REASONING, Capability.STRUCTURED_JSON])
    prompt: str
    grounding_context: Optional[Dict[str, Any]] = None
    persona: str = "CFO"
    system_instruction: Optional[str] = None
    temperature: Optional[float] = None
    max_tokens: Optional[int] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)

class AIResponse(BaseModel):
    """Structured response payload returned by AI providers."""
    content: str
    parsed_json: Optional[Dict[str, Any]] = None
    provider: str
    model: str
    key_pool_id: str
    latency_ms: float
    success: bool = True
    fallback_used: bool = False
    fallback_chain: List[str] = Field(default_factory=list)
    error_type: Optional[str] = None
    raw_usage: Optional[Dict[str, Any]] = None
