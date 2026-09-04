"""
InsightPilot AI — Executive Explanation Prompt
Generates high-level executive narrative explaining KPI movement, ranked drivers, and evidence synthesis.
"""

import json
from typing import Dict, Any
from ai.prompts.base import BASE_GROUNDING_DIRECTIVE

def build_executive_explanation_prompt(context: Dict[str, Any]) -> str:
    """Builds the complete prompt asking Gemini to generate an ExecutiveExplanation."""
    context_json = json.dumps(context, indent=2)
    
    schema_spec = """
{
  "headline": "Concise 1-sentence executive headline of the KPI movement and main driver",
  "situation": "Clear description of the KPI baseline, current value, variance ($ and %), and materiality",
  "diagnosis": "Comprehensive narrative explaining the ranked drivers (Driver #1 Atlanta stockout, Driver #2 SKU-8821 volume, Driver #3 distributor deferrals, Driver #4 Horizon pricing) with exact contributions",
  "evidence_summary": "Cross-system evidence synthesis citing the verified ERP, CRM, and Support records",
  "uncertainty": "Transparent statement of analytical bounds, confidence level, and unobserved variables",
  "executive_takeaway": "Key strategic or operational insight tailored to the requested persona",
  "grounded_evidence_ids": ["Exact list of evidence_ids referenced from the context"]
}
"""

    return f"""{BASE_GROUNDING_DIRECTIVE}

TASK:
Generate a structured executive explanation for the investigated KPI movement based on the authoritative context below.

TARGET PERSONA:
{context.get('persona', {}).get('role_title', 'Executive')} ({context.get('persona', {}).get('persona_name', 'CFO')})
Tone: {context.get('persona', {}).get('tone')}
Focus Areas: {', '.join(context.get('persona', {}).get('focus_areas', []))}

STRUCTURED INVESTIGATION CONTEXT:
{context_json}

OUTPUT FORMAT:
Return ONLY a valid JSON object conforming to this schema:
{schema_spec}
"""
