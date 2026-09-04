"""
InsightPilot AI — AI Task Classifier
Maps task types to primary and fallback providers and required model capabilities.
"""

from typing import Dict, Any, Optional, Tuple, List
from ai.config import ai_config
from ai.providers.types import TaskType, Capability

class TaskClassifier:
    """Classifies AI requests and selects appropriate providers and capabilities."""

    # Default capability mappings
    _TASK_CAPABILITIES: Dict[TaskType, List[Capability]] = {
        TaskType.BUSINESS_REASONING: [Capability.TEXT_REASONING, Capability.STRUCTURED_JSON],
        TaskType.EXECUTIVE_SYNTHESIS: [Capability.TEXT_REASONING, Capability.STRUCTURED_JSON],
        TaskType.PERSONA_ADAPTATION: [Capability.TEXT_REASONING, Capability.STRUCTURED_JSON],
        TaskType.INVESTIGATION_EXPLANATION: [Capability.TEXT_REASONING, Capability.STRUCTURED_JSON],
        TaskType.RECOMMENDATION_NARRATIVE: [Capability.TEXT_REASONING, Capability.STRUCTURED_JSON],
        TaskType.DECISION_NARRATIVE: [Capability.TEXT_REASONING, Capability.STRUCTURED_JSON],
        TaskType.MULTIMODAL_ANALYSIS: [Capability.MULTIMODAL_VISION],
        TaskType.IMAGE_ANALYSIS: [Capability.MULTIMODAL_VISION],
        TaskType.VISUAL_DOCUMENT_ANALYSIS: [Capability.MULTIMODAL_VISION],
        TaskType.CHART_ANALYSIS: [Capability.MULTIMODAL_VISION],
        TaskType.IMAGE_GENERATION: [Capability.IMAGE_GENERATION]
    }

    _MULTIMODAL_TASKS = {
        TaskType.MULTIMODAL_ANALYSIS,
        TaskType.IMAGE_ANALYSIS,
        TaskType.VISUAL_DOCUMENT_ANALYSIS,
        TaskType.CHART_ANALYSIS,
        TaskType.IMAGE_GENERATION
    }

    @classmethod
    def get_required_capabilities(cls, task_type: TaskType) -> List[Capability]:
        """Returns the capabilities required for a given task type."""
        return cls._TASK_CAPABILITIES.get(
            task_type,
            [Capability.TEXT_REASONING, Capability.STRUCTURED_JSON]
        )

    @classmethod
    def get_provider_routing(cls, task_type: TaskType) -> Tuple[str, Optional[str]]:
        """
        Returns (primary_provider_name, fallback_provider_name) for a task type.
        If task requires Gemini-specific multimodal capabilities, fallback to Groq is forbidden (None).
        """
        if task_type in cls._MULTIMODAL_TASKS:
            return ("gemini", None)

        primary = ai_config.AI_PRIMARY_PROVIDER or "groq"
        fallback = ai_config.AI_FALLBACK_PROVIDER or "gemini"
        if fallback == primary:
            fallback = "gemini" if primary == "groq" else "groq"
        return (primary, fallback)
