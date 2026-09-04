"""
InsightPilot AI — Recommendation Service Layer
Orchestrates deterministic recommendation generation for API endpoints.
"""

from typing import List, Optional
from analytics.data_loader import DataLoader
from analytics.recommendations import RecommendationEngine
from backend.app.schemas.recommendation import (
    RecommendationListResponse,
    RecommendationItemResponse,
    ExpectedImpactModel,
    RecommendationConfidenceModel
)
from backend.app.errors import KPINotFoundError, APIError

class RecommendationNotFoundError(APIError):
    """Raised when a requested recommendation ID is not found."""
    def __init__(self, rec_id: str):
        super().__init__(
            code="RECOMMENDATION_NOT_FOUND",
            message=f"Recommendation with identifier '{rec_id}' was not found.",
            status_code=404
        )

class RecommendationService:
    """Service wrapping analytics.recommendations.RecommendationEngine."""
    
    SUPPORTED_KPIS = {"north_america_east_revenue"}

    def __init__(self, data_loader: Optional[DataLoader] = None):
        self.loader = data_loader or DataLoader()
        self.engine = RecommendationEngine(self.loader)

    def _format_item(self, r: dict) -> RecommendationItemResponse:
        return RecommendationItemResponse(
            recommendation_id=r["recommendation_id"],
            kpi_id=r["kpi_id"],
            driver_id=r["driver_id"],
            driver_name=r["driver_name"],
            controllability=r["controllability"],
            controllable_lever=r["controllable_lever"],
            action=r["action"],
            rationale=r["rationale"],
            expected_impact=ExpectedImpactModel(**r["expected_impact"]),
            owner=r["owner"],
            priority=r["priority"],
            priority_rank=r["priority_rank"],
            confidence=RecommendationConfidenceModel(**r["confidence"]),
            supporting_evidence_ids=r["supporting_evidence_ids"],
            assumptions=r["assumptions"],
            constraints=r.get("constraints", []),
            overlap_group=r.get("overlap_group")
        )

    def get_recommendations(
        self,
        kpi_id: str,
        region: str = "NA-East",
        prev_period_id: str = "2026-Q2",
        curr_period_id: str = "2026-Q3"
    ) -> RecommendationListResponse:
        """Returns prioritized list of recommendations for the KPI."""
        if kpi_id not in self.SUPPORTED_KPIS:
            raise KPINotFoundError(kpi_id)

        raw_recs = self.engine.generate_recommendations(
            kpi_id=kpi_id,
            region=region,
            prev_period_id=prev_period_id,
            curr_period_id=curr_period_id
        )

        formatted = [self._format_item(r) for r in raw_recs]
        return RecommendationListResponse(
            kpi_id=kpi_id,
            total_recommendations=len(formatted),
            recommendations=formatted
        )

    def get_recommendation_by_id(
        self,
        kpi_id: str,
        recommendation_id: str,
        region: str = "NA-East"
    ) -> RecommendationItemResponse:
        """Returns a single recommendation by ID."""
        if kpi_id not in self.SUPPORTED_KPIS:
            raise KPINotFoundError(kpi_id)

        rec = self.engine.get_recommendation_by_id(recommendation_id, kpi_id=kpi_id, region=region)
        if not rec:
            raise RecommendationNotFoundError(recommendation_id)
        return self._format_item(rec)
