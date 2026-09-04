"""
InsightPilot AI — AI Explanation Output Schemas
Typed Pydantic models for structured Gemini & Groq responses, reasoning traces, and telemetry metadata.
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field, model_validator

class AIResponseMetadata(BaseModel):
    model: str = Field(..., example="gemini-2.5-flash", description="AI model identifier")
    generated_at: str = Field(..., description="UTC ISO generation timestamp")
    latency_ms: float = Field(..., example=842.5, description="End-to-end execution time in milliseconds")
    prompt_tokens: Optional[int] = Field(None, example=450, description="Input tokens consumed")
    completion_tokens: Optional[int] = Field(None, example=210, description="Output tokens generated")
    total_tokens: Optional[int] = Field(None, example=660, description="Total tokens consumed")
    grounded_evidence_count: int = Field(..., example=9, description="Number of verified evidence nodes grounded in narrative")
    validation_status: str = Field(..., example="VERIFIED_GROUNDED", description="Post-generation grounding check status")
    provider: Optional[str] = Field(None, example="groq", description="Provider identifier")
    key_pool_id: Optional[str] = Field(None, example="groq_pool_1", description="Logical key pool identifier")
    fallback_used: Optional[bool] = Field(False, description="True if failover occurred")

class ReasoningStatement(BaseModel):
    statement: str = Field(..., description="Factual analytical deduction grounded in deterministic evidence")
    supporting_evidence_ids: List[str] = Field(default_factory=list, description="Exact evidence IDs substantiating this statement")
    confidence: int = Field(..., example=94, description="Deterministic confidence score associated with this finding")

class StructuredInvestigationExplanation(BaseModel):
    """Canonical structured response contract for Gemini and Groq reasoning layers."""
    summary: str = Field(..., description="Concise 1-2 sentence executive summary of the KPI movement and main driver")
    executive_summary: Optional[str] = Field(None, description="Alias for summary")
    primary_driver_explanation: str = Field(..., description="Detailed diagnosis of the rank #1 primary driver")
    primary_explanation: Optional[str] = Field(None, description="Alias for primary_driver_explanation")
    secondary_driver_explanation: Optional[str] = Field(None, description="Diagnosis of the secondary contributing driver(s)")
    supporting_driver_ids: List[str] = Field(default_factory=list, description="IDs of drivers substantiated in this explanation")
    supporting_evidence_ids: List[str] = Field(default_factory=list, description="Direct list of all cited evidence IDs")
    business_implications: List[str] = Field(default_factory=list, description="Strategic and business impacts derived from findings")
    risks: List[str] = Field(default_factory=list, description="Downside risks if no corrective intervention is executed")
    recommended_next_actions: List[str] = Field(default_factory=list, description="Prioritized operational next actions")
    uncertainty: str = Field(..., description="Explicit acknowledgement of analytical limits, assumptions, or residual risk")
    uncertainty_statement: Optional[str] = Field(None, description="Alias for uncertainty")
    recommended_next_step: Optional[str] = Field(None, description="Executive takeaway or recommended operational next step")
    abstained: bool = Field(False, description="True if low confidence triggered mandatory analytical abstention")
    abstention_reason: Optional[str] = Field(None, description="Explanation of why the engine abstained from definitive attribution")
    grounded_evidence_ids: List[str] = Field(default_factory=list, description="Complete list of all verified evidence IDs referenced")
    reasoning: List[ReasoningStatement] = Field(default_factory=list, description="Step-by-step evidence-grounded reasoning statements")
    headline: Optional[str] = Field(None, description="High-impact title summarizing the investigation outcome")

    @model_validator(mode="before")
    @classmethod
    def populate_aliases_and_defaults(cls, data: Any) -> Any:
        if isinstance(data, dict):
            # Sync summary and executive_summary
            if "executive_summary" in data and "summary" not in data:
                data["summary"] = data["executive_summary"]
            elif "summary" in data and "executive_summary" not in data:
                data["executive_summary"] = data["summary"]

            # Sync primary_driver_explanation and primary_explanation
            if "primary_explanation" in data and "primary_driver_explanation" not in data:
                data["primary_driver_explanation"] = data["primary_explanation"]
            elif "primary_driver_explanation" in data and "primary_explanation" not in data:
                data["primary_explanation"] = data["primary_driver_explanation"]

            # Sync uncertainty and uncertainty_statement
            if "uncertainty_statement" in data and "uncertainty" not in data:
                data["uncertainty"] = data["uncertainty_statement"]
            elif "uncertainty" in data and "uncertainty_statement" not in data:
                data["uncertainty_statement"] = data["uncertainty"]

            # Combine supporting_evidence_ids and grounded_evidence_ids
            all_evidence = set(data.get("grounded_evidence_ids", []))
            all_evidence.update(data.get("supporting_evidence_ids", []))
            for item in data.get("reasoning", []):
                if isinstance(item, dict):
                    all_evidence.update(item.get("supporting_evidence_ids", []))
            data["grounded_evidence_ids"] = list(all_evidence)
            data["supporting_evidence_ids"] = list(all_evidence)
        return data

# AIExplanation alias for the unified structured output model
AIExplanation = StructuredInvestigationExplanation

class ExecutiveExplanation(BaseModel):
    """Legacy/executive view model for boardroom briefings."""
    headline: str = Field(..., description="High-impact 1-sentence executive summary of the KPI movement")
    situation: str = Field(..., description="Contextual statement of what KPI moved, by how much, and its materiality")
    diagnosis: str = Field(..., description="Multi-factor explanation synthesizing the ranked drivers")
    evidence_summary: str = Field(..., description="Synthesis of verified empirical evidence supporting the diagnosis")
    uncertainty: str = Field(..., description="Explicit acknowledgement of analytical limits or residual uncertainty")
    executive_takeaway: str = Field(..., description="Core takeaway tailored to the requesting executive persona")
    grounded_evidence_ids: List[str] = Field(..., description="List of evidence IDs cited in the narrative")

class DriverExplanation(BaseModel):
    """In-depth driver-specific explanation."""
    driver_id: str = Field(..., description="Target driver identifier")
    driver_name: str = Field(..., description="Target driver display name")
    contribution_summary: str = Field(..., description="Quantified summary of contribution and estimated monetary impact")
    evidence_rationale: str = Field(..., description="How empirical source records substantiate this specific driver")
    operational_context: str = Field(..., description="Operational breakdown tailored to the persona")
    uncertainty: str = Field(..., description="Confidence explanation and unobserved causal caveats")
    grounded_evidence_ids: List[str] = Field(..., description="List of evidence IDs cited for this driver")

class InvestigationSummary(BaseModel):
    """Complete summary briefing model."""
    headline: str = Field(..., description="Overall investigation briefing headline")
    situation: str = Field(..., description="Overview of the investigated KPI movement")
    primary_driver: str = Field(..., description="Identification and summary of the top-ranked explanatory driver")
    driver_breakdown: List[str] = Field(..., description="Bulleted narrative summaries of all ranked drivers")
    evidence_synthesis: str = Field(..., description="Cross-system synthesis of ERP, CRM, and Support signals")
    abstention_status: str = Field(..., description="Status of the confidence and abstention evaluation")
    executive_takeaway: str = Field(..., description="Summary takeaway for leadership")
    grounded_evidence_ids: List[str] = Field(..., description="All verified evidence IDs cited")

class AIExplanationResponse(BaseModel):
    investigation_id: str = Field(..., example="INV-EXEC-2026-NAE-001")
    persona: str = Field(..., example="CFO")
    explanation: ExecutiveExplanation
    metadata: AIResponseMetadata

class AIDriverExplanationResponse(BaseModel):
    investigation_id: str = Field(..., example="INV-EXEC-2026-NAE-001")
    driver_id: str = Field(..., example="atlanta_dc_stockout")
    persona: str = Field(..., example="CFO")
    explanation: DriverExplanation
    metadata: AIResponseMetadata

class StructuredAIExplanationResponse(BaseModel):
    investigation_id: str = Field(..., example="INV-EXEC-2026-NAE-001")
    persona: str = Field(..., example="CFO")
    explanation: StructuredInvestigationExplanation
    metadata: AIResponseMetadata
