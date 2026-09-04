"""
InsightPilot AI — AI Reasoning Routes
Exposes grounded Gemini executive narrative, structured reasoning, and driver explanation endpoints.
"""

from typing import Optional, Literal
from pydantic import BaseModel, Field
from fastapi import APIRouter, Depends, Path, Query, status
from backend.app.schemas.common import ErrorResponse
from backend.app.services.gemini_service import GeminiService
from backend.app.dependencies import get_gemini_service
from backend.app.errors import (
    KPINotFoundError,
    InvalidPersonaAPIError,
    AIServiceUnavailableAPIError,
    AIGroundingAPIError
)
from ai.schemas.explanation import (
    StructuredAIExplanationResponse,
    AIExplanationResponse,
    AIDriverExplanationResponse
)

router = APIRouter(prefix="/ai", tags=["AI Reasoning"])

class AIExplanationRequest(BaseModel):
    persona: str = Field("CFO", example="CFO", description="Target executive persona ('CFO' or 'REGIONAL_SALES_MANAGER')")

class AIExplainRequest(BaseModel):
    persona: str = Field("CFO", example="CFO", description="Target executive persona ('CFO' or 'REGIONAL_SALES_MANAGER')")
    explanation_mode: Literal["structured", "executive", "driver"] = Field("structured", description="Explanation output mode")
    driver_id: Optional[str] = Field(None, example="atlanta_dc_stockout", description="Target driver ID if mode is 'driver'")
    include_recommendations: bool = Field(True, description="Whether to ground the explanation with recommended actions")
    include_simulation: bool = Field(False, description="Whether to include simulation state in the context")

@router.post(
    "/explain/{kpi_id}",
    response_model=StructuredAIExplanationResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Invalid persona or request parameters"},
        404: {"model": ErrorResponse, "description": "KPI not found"},
        422: {"model": ErrorResponse, "description": "AI grounding validation failed"},
        503: {"model": ErrorResponse, "description": "AI service unavailable / unconfigured"}
    },
    summary="Generate canonical structured AI explanation",
    description="Orchestrates grounded Gemini reasoning over deterministic investigation, evidence, and recommendation data."
)
async def explain_investigation(
    kpi_id: str = Path(..., description="Target KPI identifier (e.g. north_america_east_revenue)"),
    request: AIExplainRequest = AIExplainRequest(),
    region: str = Query("NA-East", description="Target geographical region"),
    prev_period_id: str = Query("2026-Q2", description="Baseline comparison fiscal period"),
    curr_period_id: str = Query("2026-Q3", description="Current target fiscal period"),
    gemini_service: GeminiService = Depends(get_gemini_service)
) -> StructuredAIExplanationResponse:
    """Generates a structured, evidence-grounded reasoning response for the target KPI."""
    return gemini_service.explain_investigation_structured(
        kpi_id=kpi_id,
        persona=request.persona,
        region=region,
        prev_period_id=prev_period_id,
        curr_period_id=curr_period_id,
        include_recommendations=request.include_recommendations,
        include_simulation=request.include_simulation
    )

@router.post(
    "/investigations/{kpi_id}/explanation",
    response_model=AIExplanationResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Invalid persona or request parameters"},
        404: {"model": ErrorResponse, "description": "KPI not found"},
        422: {"model": ErrorResponse, "description": "AI grounding validation failed"},
        503: {"model": ErrorResponse, "description": "AI service unavailable / unconfigured"}
    },
    summary="Generate grounded executive explanation",
    description="Uses Gemini to synthesize deterministic investigation results into an executive-level narrative tailored to the requested persona."
)
async def generate_executive_explanation(
    kpi_id: str = Path(..., description="Target KPI identifier (e.g. north_america_east_revenue)"),
    request: AIExplanationRequest = AIExplanationRequest(),
    region: str = Query("NA-East", description="Target geographical region"),
    prev_period_id: str = Query("2026-Q2", description="Baseline comparison fiscal period"),
    curr_period_id: str = Query("2026-Q3", description="Current target fiscal period"),
    gemini_service: GeminiService = Depends(get_gemini_service)
) -> AIExplanationResponse:
    """Generates an executive briefing narrative tailored to leadership."""
    return gemini_service.explain_investigation_executive(
        kpi_id=kpi_id,
        persona=request.persona,
        region=region,
        prev_period_id=prev_period_id,
        curr_period_id=curr_period_id
    )

@router.post(
    "/investigations/{kpi_id}/drivers/{driver_id}/explanation",
    response_model=AIDriverExplanationResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Invalid persona or request parameters"},
        404: {"model": ErrorResponse, "description": "KPI or driver not found"},
        422: {"model": ErrorResponse, "description": "AI grounding validation failed"},
        503: {"model": ErrorResponse, "description": "AI service unavailable / unconfigured"}
    },
    summary="Generate grounded driver explanation",
    description="Uses Gemini to generate an in-depth explanation of a specific ranked driver and its supporting evidence."
)
async def generate_driver_explanation(
    kpi_id: str = Path(..., description="Target KPI identifier (e.g. north_america_east_revenue)"),
    driver_id: str = Path(..., description="Target driver identifier (e.g. atlanta_dc_stockout)"),
    request: AIExplanationRequest = AIExplanationRequest(),
    region: str = Query("NA-East", description="Target geographical region"),
    prev_period_id: str = Query("2026-Q2", description="Baseline comparison fiscal period"),
    curr_period_id: str = Query("2026-Q3", description="Current target fiscal period"),
    gemini_service: GeminiService = Depends(get_gemini_service)
) -> AIDriverExplanationResponse:
    """Generates a grounded driver-specific explanation."""
    return gemini_service.explain_driver(
        kpi_id=kpi_id,
        driver_id=driver_id,
        persona=request.persona,
        region=region,
        prev_period_id=prev_period_id,
        curr_period_id=curr_period_id
    )
