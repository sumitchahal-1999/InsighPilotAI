"""
InsightPilot AI — Recommendation Routes
Exposes prioritized action recommendations mapped from deterministic drivers.
"""

from fastapi import APIRouter, Depends, Path, Query
from backend.app.schemas.recommendation import RecommendationListResponse, RecommendationItemResponse
from backend.app.schemas.common import ErrorResponse
from backend.app.services.recommendation_service import RecommendationService
from backend.app.dependencies import get_recommendation_service

router = APIRouter(prefix="/recommendations", tags=["Recommendations"])

@router.get(
    "",
    response_model=RecommendationListResponse,
    summary="Get all prioritized recommendations",
    description="Returns prioritized recommendations for the primary KPI (north_america_east_revenue)."
)
async def list_default_recommendations(
    region: str = Query("NA-East", description="Target geographical region"),
    prev_period_id: str = Query("2026-Q2", description="Baseline comparison fiscal period"),
    curr_period_id: str = Query("2026-Q3", description="Current target fiscal period"),
    recommendation_service: RecommendationService = Depends(get_recommendation_service)
) -> RecommendationListResponse:
    """Returns prioritized recommendations for the default KPI."""
    return recommendation_service.get_recommendations(
        kpi_id="north_america_east_revenue",
        region=region,
        prev_period_id=prev_period_id,
        curr_period_id=curr_period_id
    )

@router.get(
    "/{kpi_id}",
    response_model=RecommendationListResponse,
    responses={404: {"model": ErrorResponse, "description": "KPI not found"}},
    summary="Get prioritized recommendations for KPI",
    description="Returns deterministic action recommendations mapped to ranked drivers with expected impact, ownership, and confidence."
)
async def get_recommendations(
    kpi_id: str = Path(..., description="Target KPI identifier (e.g. north_america_east_revenue)"),
    region: str = Query("NA-East", description="Target geographical region"),
    prev_period_id: str = Query("2026-Q2", description="Baseline comparison fiscal period"),
    curr_period_id: str = Query("2026-Q3", description="Current target fiscal period"),
    recommendation_service: RecommendationService = Depends(get_recommendation_service)
) -> RecommendationListResponse:
    """Returns prioritized recommendations for the specified KPI."""
    return recommendation_service.get_recommendations(
        kpi_id=kpi_id,
        region=region,
        prev_period_id=prev_period_id,
        curr_period_id=curr_period_id
    )

@router.get(
    "/{kpi_id}/{recommendation_id}",
    response_model=RecommendationItemResponse,
    responses={404: {"model": ErrorResponse, "description": "Recommendation or KPI not found"}},
    summary="Get single recommendation detail",
    description="Returns detailed rationale, constraints, assumptions, and evidence links for a specific recommendation."
)
async def get_recommendation_detail(
    kpi_id: str = Path(..., description="Target KPI identifier (e.g. north_america_east_revenue)"),
    recommendation_id: str = Path(..., description="Target recommendation ID (e.g. REC-2026-NAE-001)"),
    region: str = Query("NA-East", description="Target geographical region"),
    recommendation_service: RecommendationService = Depends(get_recommendation_service)
) -> RecommendationItemResponse:
    """Returns single recommendation detail by ID."""
    return recommendation_service.get_recommendation_by_id(
        recommendation_id=recommendation_id,
        kpi_id=kpi_id,
        region=region
    )
