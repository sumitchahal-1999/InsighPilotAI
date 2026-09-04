"""
InsightPilot AI — Investigation Summary Prompt
Generates a complete structured executive investigation briefing.
"""

import json
from typing import Dict, Any
from ai.prompts.base import BASE_GROUNDING_DIRECTIVE

def build_investigation_summary_prompt(context: Dict[str, Any]) -> str:
    """Builds prompt for structured investigation summary."""
    context_json = json.dumps(context, indent=2)

    schema_spec = """
{
  "headline": "High-level investigation briefing headline",
  "situation": "Overview of investigated KPI variance and timeframe",
  "primary_driver": "Identification of rank #1 driver, impact, and root cause context",
  "driver_breakdown": [
    "Driver #1 summary bullet with contribution % and impact",
    "Driver #2 summary bullet with contribution % and impact",
    "Driver #3 summary bullet with contribution % and impact",
    "Driver #4 summary bullet with contribution % and impact"
  ],
  "evidence_synthesis": "Synthesis of cross-functional evidence from ERP, CRM, and Support",
  "abstention_status": "Summary of confidence level and abstention evaluation",
  "executive_takeaway": "Key operational and strategic takeaway for executive leadership",
  "grounded_evidence_ids": ["List of all verified evidence_ids cited"]
}
"""

    return f"""{BASE_GROUNDING_DIRECTIVE}

TASK:
Generate a comprehensive structured investigation summary based on the authoritative context below.

TARGET PERSONA:
{context.get('persona', {}).get('role_title', 'Executive')}

STRUCTURED CONTEXT:
{context_json}

OUTPUT FORMAT:
Return ONLY a valid JSON object conforming to this schema:
{schema_spec}
"""
