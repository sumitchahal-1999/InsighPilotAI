"""
InsightPilot AI — Health Route
Provides a lightweight liveness/healthcheck probe without exposing internal credentials.
"""

from fastapi import APIRouter
from backend.app.schemas.common import HealthResponse
from backend.app.config import settings

router = APIRouter(tags=["Health"])

@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Health check probe",
    description="Returns the operational health status and version identifier of the InsightPilot API service."
)
@router.get(
    "/api/v1/health",
    response_model=HealthResponse,
    summary="Health check probe (prefixed)",
    description="Returns the operational health status and version identifier of the InsightPilot API service."
)
async def get_health() -> HealthResponse:
    """Liveness probe returning operational status."""
    return HealthResponse(
        status="ok",
        service="insightpilot-api",
        version=settings.APP_VERSION
    )

