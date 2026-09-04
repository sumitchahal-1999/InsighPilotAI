"""
InsightPilot AI — Investigation Explanation Prompt (v1)
Canonical prompt contract for structured executive reasoning and evidence-grounded attribution.
"""

import json
from typing import Dict, Any
from ai.prompts.base import BASE_GROUNDING_DIRECTIVE

SCHEMA_SPEC_V1 = """
{
  "summary": "Concise 1-2 sentence executive summary of the investigated KPI variance and primary operational cause.",
  "primary_driver_explanation": "Detailed explanation of why the rank #1 primary driver matters, its operational mechanism, and empirical backing.",
  "secondary_driver_explanation": "Contextual explanation of secondary contributing driver(s) and their compounding effect.",
  "supporting_driver_ids": ["Exact driver_id(s) from the context supporting this diagnosis"],
  "supporting_evidence_ids": ["Exact evidence_id(s) from the context supporting this statement"],
  "business_implications": ["Key strategic and business impacts derived directly from the facts"],
  "risks": ["Operational or financial risks if no corrective intervention is executed"],
  "recommended_next_actions": ["Prioritized operational next actions grounded in findings"],
  "uncertainty": "Transparent statement of analytical bounds, assumptions, unobserved variables, and confidence level.",
  "recommended_next_step": "Key strategic takeaway or recommended operational next step based on the findings.",
  "abstained": false,
  "abstention_reason": null,
  "grounded_evidence_ids": ["Complete list of all unique evidence_ids cited across reasoning and narratives"],
  "reasoning": [
    {
      "statement": "Evidence-grounded factual deduction regarding a specific driver or operational event.",
      "supporting_evidence_ids": ["Exact evidence_id(s) from the context supporting this statement"],
      "confidence": 94
    }
  ]
}
"""

def build_structured_investigation_prompt(context: Dict[str, Any]) -> str:
    """Builds the canonical v1 structured investigation reasoning prompt."""
    context_json = json.dumps(context, indent=2)
    persona_name = context.get('persona', {}).get('persona_name', 'CFO')
    role_title = context.get('persona', {}).get('role_title', 'Chief Financial Officer')
    tone = context.get('persona', {}).get('tone', 'Strategic, precise, risk-oriented')
    focus_areas = ', '.join(context.get('persona', {}).get('focus_areas', ['Revenue variance', 'Margin impact']))
    is_abstained = context.get('overall_confidence', {}).get('abstention', False)

    abstention_instruction = ""
    if is_abstained:
        abstention_instruction = """
IMPORTANT - ABSTENTION MANDATE ACTIVE:
The investigation confidence score is BELOW the threshold (abstention: true).
You MUST set 'abstained': true in your response.
Do NOT produce a confident or definitive primary driver attribution.
Explicitly state in 'summary' and 'uncertainty' that evidence is insufficient to isolate a conclusive single root cause.
In 'abstention_reason', explain what additional empirical evidence (e.g. detailed freight logs, direct distributor confirmations) would be required.
"""

    return f"""{BASE_GROUNDING_DIRECTIVE}

{abstention_instruction}

TASK:
You are the business reasoning layer of InsightPilot AI.
Analyze the provided structured deterministic context and produce a structured, evidence-grounded explanation.

STRICT REASONING RULES:
1. Use ONLY the supplied deterministic context.
2. You must NOT:
   - invent revenue figures
   - change KPI values
   - invent variance percentages
   - invent driver contributions
   - invent driver rankings
   - invent confidence scores
   - invent recovery amounts
   - invent simulation results
   - invent evidence IDs
   - cite records not included in the context
   - introduce unsupported causal relationships
3. Do not perform independent quantitative calculations.
4. Do not contradict deterministic values.
5. If the supplied evidence is insufficient or confidence is low, explicitly state that the evidence is insufficient.
6. Distinguish observed evidence from inferred explanation. Do not present correlation as proven causation.
7. Use confidence scores supplied by the deterministic system (e.g. 94, 89, 85, 78).
8. Every evidence ID in 'supporting_evidence_ids' and 'grounded_evidence_ids' MUST be an exact 'evidence_id' from the supplied context.
9. Every driver ID in 'supporting_driver_ids' MUST be an exact 'driver_id' from the supplied context.

TARGET PERSONA:
- Role: {role_title} ({persona_name})
- Tone: {tone}
- Focus Areas: {focus_areas}

STRUCTURED DETERMINISTIC CONTEXT:
{context_json}

OUTPUT FORMAT:
Return ONLY a valid JSON object strictly conforming to this schema without code fences or markdown wrapper:
{SCHEMA_SPEC_V1}
"""
