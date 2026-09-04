"""
InsightPilot AI — Base AI Provider Abstract Interface
Defines the contract for LLM provider implementations (Gemini, Groq, etc.).
"""

from abc import ABC, abstractmethod
from typing import Set, List, Optional
from ai.providers.types import AIRequest, AIResponse, Capability, TaskType

class BaseAIProvider(ABC):
    """Abstract interface for multi-model AI providers with key pool support."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Unique identifier for the provider (e.g. 'gemini', 'groq')."""
        pass

    @property
    @abstractmethod
    def supported_capabilities(self) -> Set[Capability]:
        """Set of capabilities supported by this provider."""
        pass

    @property
    @abstractmethod
    def supported_tasks(self) -> Set[TaskType]:
        """Set of tasks natively handled by this provider."""
        pass

    @property
    @abstractmethod
    def key_pool_ids(self) -> List[str]:
        """List of logical key pool identifiers configured for this provider."""
        pass

    @abstractmethod
    def is_configured(self) -> bool:
        """Returns True if at least one valid key is available for this provider."""
        pass

    @abstractmethod
    def generate(self, request: AIRequest, key_pool_index: int = 0) -> AIResponse:
        """Executes generation using the specified key pool index."""
        pass
