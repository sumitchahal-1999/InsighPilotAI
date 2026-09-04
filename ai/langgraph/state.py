"""
InsightPilot AI — LangGraph Investigation State
Defines the strongly-typed investigation state shared across all LangGraph nodes.
"""

from typing import Dict, Any, List, Optional
from typing_extensions import TypedDict

class InvestigationState(TypedDict, total=False):
    """Canonical LangGraph state for end-to-end deterministic + AI investigation."""

    # 1. Investigation Identity & Request
    investigation_id: str
    kpi_id: str
    region: str
    prev_period_id: str
    curr_period_id: str
    persona: str
    include_recommendations: bool
    include_simulation: bool

    # 2. Deterministic Quantitative Truth State
    kpi_context: Optional[Dict[str, Any]]
    kpi_movement: Optional[Dict[str, Any]]
    drivers: Optional[List[Dict[str, Any]]]
    evidence: Optional[List[Dict[str, Any]]]
    validated_evidence: Optional[List[Dict[str, Any]]]
    confidence: Optional[Dict[str, Any]]
    recommendations: Optional[List[Dict[str, Any]]]
    simulation: Optional[Dict[str, Any]]
    decision_graph: Optional[Dict[str, Any]]

    # 3. Grounding & Abstention Guard
    grounding_context: Optional[Dict[str, Any]]
    abstention: bool
    abstention_reason: Optional[str]

    # 4. AI Orchestration & Reasoning State
    task_type: str
    primary_provider: str
    fallback_provider: Optional[str]
    ai_request: Optional[Dict[str, Any]]
    ai_response: Optional[Dict[str, Any]]
    ai_explanation: Optional[Dict[str, Any]]
    provider_metadata: Optional[Dict[str, Any]]
    provider_events: List[Dict[str, Any]]

    # 5. Telemetry & Execution Trace
    started_at: str
    completed_at: str
    total_duration_ms: float
    telemetry: Dict[str, Any]
    nodes_executed: List[str]
    node_traces: List[Dict[str, Any]]
    errors: List[str]
