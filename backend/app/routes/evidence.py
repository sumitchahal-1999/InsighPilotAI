"""
InsightPilot AI — Evidence Routes
Exposes verified evidence items, global domain filtering, and complete 5-layer cryptographic lineage traces.
"""

from typing import Optional
from fastapi import APIRouter, Depends, Path, Query
from backend.app.schemas.evidence import (
    EvidenceItemResponse,
    EvidenceListResponse,
    AllEvidenceListResponse,
    LineageTraceResponse
)
from backend.app.schemas.common import ErrorResponse
from backend.app.services.evidence_service import EvidenceService
from backend.app.dependencies import get_evidence_service

router = APIRouter(prefix="/evidence", tags=["Evidence"])

@router.get(
    "",
    response_model=AllEvidenceListResponse,
    summary="Get all verified empirical evidence nodes",
    description="Returns all 9 verified evidence items across ERP, CRM, Support, and Market Intel with optional domain and search query filtering."
)
async def list_all_evidence(
    domain: Optional[str] = Query(None, description="Optional domain filter (e.g. ERP, CRM, Support, Market)"),
    q: Optional[str] = Query(None, description="Optional search term matching ID, text, or driver"),
    region: str = Query("NA-East", description="Target geographical region"),
    evidence_service: EvidenceService = Depends(get_evidence_service)
) -> AllEvidenceListResponse:
    """Returns global verified evidence list across all domains."""
    return evidence_service.get_all_evidence(
        domain=domain,
        search=q,
        region=region
    )

@router.get(
    "/{evidence_id}",
    response_model=EvidenceItemResponse,
    responses={404: {"model": ErrorResponse, "description": "Evidence not found"}},
    summary="Get single evidence item",
    description="Returns the verified evidence item by ID including source record references, analytical method, confidence, and freshness."
)
async def get_evidence(
    evidence_id: str = Path(..., description="Unique evidence identifier (e.g. EVID_ERP_ATL_STOCKOUT_001)"),
    region: str = Query("NA-East", description="Target geographical region"),
    evidence_service: EvidenceService = Depends(get_evidence_service)
) -> EvidenceItemResponse:
    """Returns a single verified evidence node."""
    return evidence_service.get_single_evidence(
        evidence_id=evidence_id,
        region=region
    )

@router.get(
    "/{evidence_id}/lineage",
    response_model=LineageTraceResponse,
    responses={404: {"model": ErrorResponse, "description": "Evidence not found"}},
    summary="Get 5-layer lineage trace",
    description="Returns the machine-readable lineage path connecting Root KPI -> Driver -> Evidence -> Source Table/Job -> Raw Record ID with SHA-256 audit hash."
)
async def get_evidence_lineage(
    evidence_id: str = Path(..., description="Unique evidence identifier (e.g. EVID_ERP_ATL_STOCKOUT_001)"),
    region: str = Query("NA-East", description="Target geographical region"),
    evidence_service: EvidenceService = Depends(get_evidence_service)
) -> LineageTraceResponse:
    """Returns the cryptographic lineage trace for a specific evidence item."""
    return evidence_service.get_evidence_lineage(
        evidence_id=evidence_id,
        region=region
    )
