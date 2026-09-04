"""
InsightPilot AI — Recommendation API Schemas
Pydantic models matching data/schemas/recommendation_contract.json.
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class ExpectedImpactModel(BaseModel):
    revenue_recovery_usd: float = Field(..., example=550000.0)
    margin_impact_pct: float = Field(..., example=1.2)
    recovery_timeframe_days: int = Field(..., example=14)

class RecommendationConfidenceModel(BaseModel):
    score: int = Field(..., example=91)
    label: str = Field(..., example="HIGH")

class RecommendationItemResponse(BaseModel):
    recommendation_id: str = Field(..., example="REC-2026-NAE-001")
    kpi_id: str = Field(..., example="north_america_east_revenue")
    driver_id: str = Field(..., example="atlanta_dc_stockout")
    driver_name: str = Field(..., example="Atlanta DC Stockout")
    controllability: str = Field(..., example="HIGH")
    controllable_lever: str = Field(..., example="Inventory Availability / Inter-DC Stock Rebalancing")
    action: str = Field(..., example="Execute Emergency Inventory Transfer (20,000 Units from Charlotte Hub to Atlanta DC)")
    rationale: str = Field(...)
    expected_impact: ExpectedImpactModel
    owner: str = Field(..., example="Supply Chain / Operations")
    priority: str = Field(..., example="CRITICAL")
    priority_rank: int = Field(..., example=1)
    confidence: RecommendationConfidenceModel
    supporting_evidence_ids: List[str] = Field(...)
    assumptions: List[str] = Field(...)
    constraints: List[str] = Field(default_factory=list)
    overlap_group: Optional[str] = Field(None, example="FULFILLMENT_RECOVERY")

class RecommendationListResponse(BaseModel):
    kpi_id: str = Field(..., example="north_america_east_revenue")
    total_recommendations: int = Field(..., example=4)
    recommendations: List[RecommendationItemResponse]
