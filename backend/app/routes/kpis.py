"""
InsightPilot AI — KPI Routes
Exposes deterministic KPI definitions and calculated states across regions and periods.
"""

from typing import Optional
from fastapi import APIRouter, Depends, Query, Path
from backend.app.schemas.kpi import KPIListResponse, KPIStateResponse
from backend.app.schemas.common import ErrorResponse
from backend.app.services.kpi_service import KPIService
from backend.app.dependencies import get_kpi_service

router = APIRouter(prefix="/kpis", tags=["KPIs"])

@router.get(
    "",
    response_model=KPIListResponse,
    summary="List all calculated KPI states",
    description="Calculates and returns the full set of five core KPIs from underlying enterprise datasets."
)
async def list_kpis(
    region: str = Query("NA-East", description="Geographic region filter"),
    prev_period_id: str = Query("2026-Q2", description="Baseline comparison fiscal period"),
    curr_period_id: str = Query("2026-Q3", description="Current target fiscal period"),
    kpi_service: KPIService = Depends(get_kpi_service)
) -> KPIListResponse:
    """Returns calculated states for all supported KPIs."""
    states = kpi_service.get_all_kpi_states(
        region=region,
        prev_period_id=prev_period_id,
        curr_period_id=curr_period_id
    )
    return KPIListResponse(total_count=len(states), kpis=states)

@router.get(
    "/{kpi_id}",
    response_model=KPIStateResponse,
    responses={404: {"model": ErrorResponse, "description": "KPI not found"}},
    summary="Get single calculated KPI state",
    description="Calculates and returns current value, baseline value, variance, and materiality status for a specific KPI."
)
async def get_kpi(
    kpi_id: str = Path(..., description="Unique KPI identifier (e.g. north_america_east_revenue)"),
    region: str = Query("NA-East", description="Geographic region filter"),
    prev_period_id: str = Query("2026-Q2", description="Baseline comparison fiscal period"),
    curr_period_id: str = Query("2026-Q3", description="Current target fiscal period"),
    kpi_service: KPIService = Depends(get_kpi_service)
) -> KPIStateResponse:
    """Returns the calculated state of the specified KPI."""
    return kpi_service.get_kpi_state(
        kpi_id=kpi_id,
        region=region,
        prev_period_id=prev_period_id,
        curr_period_id=curr_period_id
    )
