"""
InsightPilot AI — Gemini Client Abstraction
Wraps official Google GenAI SDK with error handling, telemetry capture, and timeouts.
"""

import json
import time
from typing import Dict, Any, Optional, Tuple
from google import genai
from google.genai import types
from ai.config import ai_config

class GeminiAPIError(Exception):
    """Raised when an error occurs while communicating with Google Gemini API."""
    pass

class GeminiClient:
    """Client abstraction for sending structured prompts to Google Gemini."""

    def __init__(self, api_key: Optional[str] = None, model_name: Optional[str] = None):
        self.api_key = api_key or ai_config.API_KEY
        self.model_name = model_name or ai_config.MODEL_NAME
        self._client: Optional[genai.Client] = None

    def _get_client(self) -> genai.Client:
        """Initializes and returns the official genai Client."""
        if not self.api_key:
            raise GeminiAPIError("GEMINI_API_KEY is not configured in the environment.")
        if self._client is None:
            self._client = genai.Client(api_key=self.api_key)
        return self._client

    def generate_json(self, prompt: str) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """
        Sends a prompt to Gemini and parses the resulting JSON response.
        Returns: (parsed_json_dict, telemetry_dict)
        """
        client = self._get_client()
        start_time = time.perf_counter()

        try:
            # Configure structured generation
            config = types.GenerateContentConfig(
                temperature=ai_config.TEMPERATURE,
                max_output_tokens=ai_config.MAX_OUTPUT_TOKENS,
                response_mime_type="application/json"
            )

            response = client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=config
            )

            elapsed_ms = round((time.perf_counter() - start_time) * 1000.0, 2)

            raw_text = response.text or "{}"
            # Strip markdown json codeblocks if any remain
            cleaned_text = raw_text.strip()
            if cleaned_text.startswith("```json"):
                cleaned_text = cleaned_text[7:]
            if cleaned_text.startswith("```"):
                cleaned_text = cleaned_text[3:]
            if cleaned_text.endswith("```"):
                cleaned_text = cleaned_text[:-3]
            cleaned_text = cleaned_text.strip()

            parsed_data = json.loads(cleaned_text)

            # Telemetry extraction
            usage = getattr(response, "usage_metadata", None)
            prompt_tokens = getattr(usage, "prompt_token_count", None) if usage else None
            completion_tokens = getattr(usage, "candidates_token_count", None) if usage else None
            total_tokens = getattr(usage, "total_token_count", None) if usage else None

            telemetry = {
                "model": self.model_name,
                "latency_ms": elapsed_ms,
                "prompt_tokens": prompt_tokens,
                "completion_tokens": completion_tokens,
                "total_tokens": total_tokens
            }

            return parsed_data, telemetry

        except json.JSONDecodeError as jde:
            raise GeminiAPIError(f"Failed to parse JSON response from Gemini model: {jde}")
        except Exception as e:
            raise GeminiAPIError(f"Gemini API request failed: {str(e)}")
