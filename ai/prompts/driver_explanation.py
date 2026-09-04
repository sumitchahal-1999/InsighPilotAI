"""
InsightPilot AI — Driver Explanation Prompt
Generates detailed narrative focusing on a specific deterministic driver and its supporting evidence.
"""

import json
from typing import Dict, Any
from ai.prompts.base import BASE_GROUNDING_DIRECTIVE

def build_driver_explanation_prompt(context: Dict[str, Any], driver_id: str) -> str:
    """Builds the prompt asking Gemini to explain a single driver in depth."""
    driver_item = next((d for d in context.get("drivers", []) if d["driver_id"] == driver_id), None)
    if not driver_item:
        raise ValueError(f"Driver '{driver_id}' not found in investigation context.")

    linked_evidence = [
        ev for ev in context.get("evidence", [])
        if ev.get("supports_driver") == driver_id
    ]

    target_context = {
        "investigation_id": context.get("investigation_id"),
        "kpi": context.get("kpi"),
        "target_driver": driver_item,
        "linked_evidence": linked_evidence,
        "persona": context.get("persona")
    }

    schema_spec = """
{
  "driver_id": "Target driver identifier (e.g. atlanta_dc_stockout)",
  "driver_name": "Target driver display name",
  "contribution_summary": "Summary of driver's contribution percentage and dollar impact",
  "evidence_rationale": "Detailed explanation of how the empirical source records substantiate this driver",
  "operational_context": "Operational breakdown tailored to the target persona",
  "uncertainty": "Confidence score context and residual analytical caveats",
  "grounded_evidence_ids": ["Exact list of evidence_ids referenced"]
}
"""

    return f"""{BASE_GROUNDING_DIRECTIVE}

TASK:
Generate a detailed grounded explanation for the specific driver '{driver_item.get('driver_name')}' ({driver_id}) based strictly on the context below.

TARGET PERSONA:
{context.get('persona', {}).get('role_title', 'Executive')}

DRIVER CONTEXT:
{json.dumps(target_context, indent=2)}

OUTPUT FORMAT:
Return ONLY a valid JSON object conforming to this schema:
{schema_spec}
"""
