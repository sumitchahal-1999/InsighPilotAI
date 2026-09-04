"""
InsightPilot AI — Decision Graph Domain Models
Defines strongly typed models for dynamic, deterministic decision graph generation.
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class DecisionGraphNodeModel(BaseModel):
    """Represents a single typed node in the 6-column decision graph."""
    id: str = Field(..., description="Unique deterministic node identifier (e.g. 'kpi-1', 'drv-1')")
    column: int = Field(..., ge=1, le=6, description="Column index from 1 (KPI Anomaly) to 6 (Predicted Outcome)")
    column_title: str = Field(..., description="Human readable column title")
    title: str = Field(..., description="Node display title")
    node_type: str = Field(..., description="Node category: KPI, DRIVER, EVIDENCE, MECHANISM, ACTION, OUTCOME, ABSTENTION")
    category: str = Field("General", description="Business domain category (Finance, Supply Chain, Commercial Sales, etc.)")
    primary_metric: str = Field(..., description="Top-line metric value formatted for presentation")
    secondary_metric: Optional[str] = Field(None, description="Contextual secondary metric or impact")
    confidence: int = Field(100, ge=0, le=100, description="Empirical confidence score (0-100)")
    description: str = Field(..., description="Factually grounded node narrative")
    status: str = Field("ACTIVE", description="Node status: CRITICAL, HIGH, VERIFIED, ACTIVE, SUCCESS, ABSTAINED")
    evidence_id: Optional[str] = Field(None, description="Authoritative empirical evidence ID if applicable")
    hash: Optional[str] = Field(None, description="SHA-256 cryptographic verification hash for evidence")
    linked_parents: List[str] = Field(default_factory=list, description="IDs of direct parent nodes")
    linked_children: List[str] = Field(default_factory=list, description="IDs of direct child nodes")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Deterministic analytical metadata")

class DecisionGraphEdgeModel(BaseModel):
    """Represents a directional causal or logical relationship between two graph nodes."""
    source: str = Field(..., description="Origin node ID")
    target: str = Field(..., description="Destination node ID")
    relationship_type: str = Field(..., description="Relationship label: DECOMPOSED_TO, SUBSTANTIATED_BY, TRIGGERS, CORROBORATES, AMPLIFIES, MITIGATED_BY, YIELDS, ATTRIBUTION_SUSPENDED")
    confidence: Optional[int] = Field(None, ge=0, le=100, description="Confidence of the relationship")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Edge metadata")

class DynamicDecisionGraph(BaseModel):
    """Canonical dynamic decision graph payload for API contracts and UI rendering."""
    graph_id: str = Field(..., description="Deterministic graph execution ID")
    kpi_id: str = Field(..., description="Root KPI identifier")
    region: str = Field("NA-East", description="Geographic region")
    total_columns: int = Field(6, description="Total column count")
    total_nodes_count: int = Field(..., description="Total node count")
    total_edges_count: int = Field(..., description="Total edge count")
    nodes: List[DecisionGraphNodeModel]
    edges: List[DecisionGraphEdgeModel]
    confidence: int = Field(89, description="Investigation overall confidence score")
    abstained: bool = Field(False, description="Whether causal graph attribution was suspended")
    abstention_reason: Optional[str] = Field(None, description="Abstention explanation if active")
    abstention_reason_codes: List[str] = Field(default_factory=list, description="Machine-readable abstention codes")
    generated_at: str = Field(..., description="ISO 8601 generation timestamp")
