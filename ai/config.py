"""
InsightPilot AI — AI Layer Configuration
Manages multi-model credentials (Gemini + Groq), key pools, model parameters, and operational constraints.
"""

import os
from typing import List
from dotenv import load_dotenv

load_dotenv()

class AIConfig:
    """Configuration settings for the Multi-Model AI reasoning and orchestration layer."""

    # Gemini Key Pools
    GEMINI_API_KEY_1: str = (os.getenv("GEMINI_API_KEY_1") or os.getenv("GEMINI_API_KEY") or "").strip()
    GEMINI_API_KEY_2: str = os.getenv("GEMINI_API_KEY_2", "").strip()
    GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-2.5-flash").strip()

    # Groq Key Pools
    GROQ_API_KEY_1: str = (os.getenv("GROQ_API_KEY_1") or os.getenv("GROQ_API_KEY") or "").strip()
    GROQ_API_KEY_2: str = os.getenv("GROQ_API_KEY_2", "").strip()
    GROQ_MODEL: str = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant").strip()

    # Provider Routing Priorities
    AI_PRIMARY_PROVIDER: str = os.getenv("AI_PRIMARY_PROVIDER", "groq").lower().strip()
    AI_FALLBACK_PROVIDER: str = os.getenv("AI_FALLBACK_PROVIDER", "gemini").lower().strip()

    # Shared Parameters
    TEMPERATURE: float = float(os.getenv("AI_TEMPERATURE", "0.1"))
    TIMEOUT_SECONDS: int = int(os.getenv("AI_REQUEST_TIMEOUT_SECONDS", "30"))
    MAX_OUTPUT_TOKENS: int = int(os.getenv("AI_MAX_TOKENS", "2048"))
    MAX_RETRIES: int = int(os.getenv("AI_MAX_RETRIES", "1"))
    FALLBACK_ENABLED: bool = os.getenv("AI_PROVIDER_FALLBACK_ENABLED", "true").lower() in ("true", "1", "yes")

    # Legacy compatibility property
    @property
    def API_KEY(self) -> str:
        return self.GEMINI_API_KEY_1

    @property
    def MODEL_NAME(self) -> str:
        return self.GEMINI_MODEL

    @classmethod
    def get_gemini_keys(cls) -> List[str]:
        """Returns ordered list of configured non-empty Gemini API keys."""
        keys = []
        if cls.GEMINI_API_KEY_1:
            keys.append(cls.GEMINI_API_KEY_1)
        if cls.GEMINI_API_KEY_2 and cls.GEMINI_API_KEY_2 != cls.GEMINI_API_KEY_1:
            keys.append(cls.GEMINI_API_KEY_2)
        return keys

    @classmethod
    def get_groq_keys(cls) -> List[str]:
        """Returns ordered list of configured non-empty Groq API keys."""
        keys = []
        if cls.GROQ_API_KEY_1:
            keys.append(cls.GROQ_API_KEY_1)
        if cls.GROQ_API_KEY_2 and cls.GROQ_API_KEY_2 != cls.GROQ_API_KEY_1:
            keys.append(cls.GROQ_API_KEY_2)
        return keys

    @classmethod
    def is_configured(cls) -> bool:
        """Returns True if at least one AI provider has a configured API key."""
        return bool(cls.get_gemini_keys() or cls.get_groq_keys())

ai_config = AIConfig()
