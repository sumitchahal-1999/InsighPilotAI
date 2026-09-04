"""
InsightPilot AI — AI Reasoning & Narrative Package
Accenture Innovation Challenge 2026 — Track 3: BusinessIntelligence.ai

Grounded Gemini LLM reasoning layer operating strictly downstream of deterministic analytics.
"""

from ai.client import GeminiClient
from ai.context import GroundedContextBuilder
from ai.validator import GroundingValidator
from ai.service import AIService

__all__ = [
    "GeminiClient",
    "GroundedContextBuilder",
    "GroundingValidator",
    "AIService",
]
