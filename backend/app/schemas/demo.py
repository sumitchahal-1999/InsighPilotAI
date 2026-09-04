"""
InsightPilot AI — Competition Demo API Schemas
Typed Pydantic models for unified demo bundles, narrative storyboards, execution replays, and readiness audits.
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from ai.demo.narrative import DemoNarrative
from ai.demo.integrity_guard import DemoIntegrityReport


class InvestigationReplayNode(BaseModel):
    step_number: int = Field(..., example=1)
    node_name: str = Field(..., example="load_kpi_node")
    display_name: str = Field(..., example="Load KPI Context")
    classification: str = Field(..., example="DETERMINISTIC", description="DETERMINISTIC | AI_ORCHESTRATION | SAFETY_GUARD")
    status: str = Field(..., example="COMPLETED")
    duration_ms: float = Field(..., example=12.4)
    provider_pool_id: str = Field("none", example="deterministic_fallback", description="Safe logical key pool identifier")
    summary: str = Field(..., example="Loaded baseline and target revenue records.")
    details: List[str] = Field(default_factory=list)


class InvestigationReplayResponse(BaseModel):
    investigation_id: str = Field(...)
    kpi_id: str = Field(...)
    persona: str = Field("CFO")
    total_steps: int = Field(...)
    total_duration_ms: float = Field(...)
    replay_nodes: List[InvestigationReplayNode] = Field(default_factory=list)
    failover_events: List[Dict[str, Any]] = Field(default_factory=list)
    abstention_occurred: bool = Field(False)
    fallback_occurred: bool = Field(False)


class CompetitionDemoResponse(BaseModel):
    investigation_id: str = Field(...)
    kpi_id: str = Field(...)
    persona: str = Field("CFO")
    kpi: Dict[str, Any] = Field(...)
    movement: Dict[str, Any] = Field(...)
    drivers: List[Dict[str, Any]] = Field(default_factory=list)
    confidence: Dict[str, Any] = Field(...)
    abstention: Dict[str, Any] = Field(...)
    ai_explanation: Dict[str, Any] = Field(...)
    ai_source_indicator: str = Field(..., example="AI Source: Groq (llama-3.3-70b-versatile)")
    evidence_summary: Dict[str, Any] = Field(...)
    decision_graph_summary: Dict[str, Any] = Field(...)
    recommendations: List[Dict[str, Any]] = Field(default_factory=list)
    simulation_summary: Dict[str, Any] = Field(...)
    demo_narrative: DemoNarrative = Field(...)
    integrity_report: DemoIntegrityReport = Field(...)
    demo_status: Dict[str, Any] = Field(...)
