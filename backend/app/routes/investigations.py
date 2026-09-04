"""
InsightPilot AI — Investigation Routes
Exposes full root cause investigations, ranked driver breakdowns, decision graph topology, and supporting evidence summaries.
"""

from typing import Optional
from fastapi import APIRouter, Depends, Query, Path
from backend.app.schemas.investigation import (
    InvestigationResponse,
    DriverListResponse,
    DecisionGraphResponse,
    LangGraphTraceResponse
)
from backend.app.schemas.evidence import EvidenceListResponse
from backend.app.schemas.common import ErrorResponse
from backend.app.services.investigation_service import InvestigationService
from backend.app.services.evidence_service import EvidenceService
from backend.app.dependencies import get_investigation_service, get_evidence_service

router = APIRouter(prefix="/investigations", tags=["Investigations"])

@router.get(
    "/{kpi_id}",
    response_model=InvestigationResponse,
    responses={404: {"model": ErrorResponse, "description": "KPI not found"}},
    summary="Execute root cause investigation",
    description="Orchestrates the deterministic investigation engine, returning variance evaluation, ranked drivers, confidence score, and lineage graph."
)
async def run_investigation(
    kpi_id: str = Path(..., description="Target KPI identifier (e.g. north_america_east_revenue)"),
    region: str = Query("NA-East", description="Target geographical region"),
    prev_period_id: str = Query("2026-Q2", description="Baseline comparison fiscal period"),
    curr_period_id: str = Query("2026-Q3", description="Current target fiscal period"),
    persona_id: str = Query("CFO", description="Executive user persona requesting investigation"),
    investigation_service: InvestigationService = Depends(get_investigation_service)
) -> InvestigationResponse:
    """Runs deterministic investigation on target KPI."""
    return investigation_service.run_investigation(
        kpi_id=kpi_id,
        region=region,
        prev_period_id=prev_period_id,
        curr_period_id=curr_period_id,
        persona_id=persona_id
    )

@router.get(
    "/{kpi_id}/drivers",
    response_model=DriverListResponse,
    responses={404: {"model": ErrorResponse, "description": "KPI not found"}},
    summary="Get ranked explanatory drivers",
    description="Returns the quantified, ranked drivers explaining the KPI movement with normalized contribution percentages and confidence scores."
)
async def get_investigation_drivers(
    kpi_id: str = Path(..., description="Target KPI identifier (e.g. north_america_east_revenue)"),
    region: str = Query("NA-East", description="Target geographical region"),
    prev_period_id: str = Query("2026-Q2", description="Baseline comparison fiscal period"),
    curr_period_id: str = Query("2026-Q3", description="Current target fiscal period"),
    investigation_service: InvestigationService = Depends(get_investigation_service)
) -> DriverListResponse:
    """Returns the list of ranked drivers for the specified KPI investigation."""
    return investigation_service.get_drivers(
        kpi_id=kpi_id,
        region=region,
        prev_period_id=prev_period_id,
        curr_period_id=curr_period_id
    )

@router.get(
    "/{kpi_id}/decision-graph",
    response_model=DecisionGraphResponse,
    responses={404: {"model": ErrorResponse, "description": "KPI not found"}},
    summary="Get 6-column decision graph topology",
    description="Returns the complete causal topology connecting KPI Anomaly -> Causal Drivers -> Empirical Evidence -> Causal Mechanics -> Action Levers -> Predicted Outcome."
)
async def get_decision_graph(
    kpi_id: str = Path(..., description="Target KPI identifier (e.g. north_america_east_revenue)"),
    region: str = Query("NA-East", description="Target geographical region"),
    prev_period_id: str = Query("2026-Q2", description="Baseline comparison fiscal period"),
    curr_period_id: str = Query("2026-Q3", description="Current target fiscal period"),
    persona: str = Query("CFO", description="Executive persona context"),
    investigation_service: InvestigationService = Depends(get_investigation_service)
) -> DecisionGraphResponse:
    """Returns the typed decision graph topology for the specified KPI investigation."""
    return investigation_service.get_decision_graph(
        kpi_id=kpi_id,
        region=region,
        prev_period_id=prev_period_id,
        curr_period_id=curr_period_id,
        persona=persona
    )

@router.get(
    "/{kpi_id}/evidence",
    response_model=EvidenceListResponse,
    responses={404: {"model": ErrorResponse, "description": "KPI not found"}},
    summary="Get all evidence nodes for investigation",
    description="Returns all verified evidence items substantiating the drivers in the specified KPI investigation."
)
async def get_investigation_evidence(
    kpi_id: str = Path(..., description="Target KPI identifier (e.g. north_america_east_revenue)"),
    region: str = Query("NA-East", description="Target geographical region"),
    evidence_service: EvidenceService = Depends(get_evidence_service)
) -> EvidenceListResponse:
    """Returns all evidence items for the specified KPI investigation."""
    return evidence_service.get_investigation_evidence(
        kpi_id=kpi_id,
        region=region
    )

@router.get(
    "/{kpi_id}/langgraph-trace",
    response_model=LangGraphTraceResponse,
    responses={404: {"model": ErrorResponse, "description": "KPI not found"}},
    summary="Get live LangGraph multi-agent execution trace",
    description="Executes or retrieves the LangGraph investigation workflow, returning fine-grained node transition timings, provider events, confidence progression, and grounded synthesis."
)
async def get_langgraph_trace(
    kpi_id: str = Path(..., description="Target KPI identifier (e.g. north_america_east_revenue)"),
    region: str = Query("NA-East", description="Target geographical region"),
    prev_period_id: str = Query("2026-Q2", description="Baseline comparison fiscal period"),
    curr_period_id: str = Query("2026-Q3", description="Current target fiscal period"),
    persona_id: str = Query("CFO", description="Executive user persona (e.g. CFO or REGIONAL_SALES_MANAGER)"),
    investigation_service: InvestigationService = Depends(get_investigation_service)
) -> LangGraphTraceResponse:
    """Executes the live LangGraph multi-agent investigation workflow and returns the full typed execution trace."""
    return investigation_service.run_langgraph_investigation(
        kpi_id=kpi_id,
        region=region,
        prev_period_id=prev_period_id,
        curr_period_id=curr_period_id,
        persona_id=persona_id
    )

