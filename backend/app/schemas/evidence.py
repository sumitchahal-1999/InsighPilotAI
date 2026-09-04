"""
InsightPilot AI — Evidence API Schemas
Models matching data/schemas/evidence_contract.json for evidence nodes and lineage traces.
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class FreshnessModel(BaseModel):
    age_hours: float = Field(..., example=1344.0)
    status: str = Field(..., example="RECENT")

class ContributionModel(BaseModel):
    percentage: float = Field(..., example=43.2)
    monetary_impact_usd: float = Field(..., example=-550000.0)

class ConfidenceModel(BaseModel):
    score: int = Field(..., example=94)
    label: str = Field(..., example="HIGH")

class LineageMetadataModel(BaseModel):
    source_table: str = Field(..., example="sap_mm_inventory_snapshots")
    pipeline_job_id: str = Field(..., example="JOB_ERP_STOCK_FEED_20260815_01")
    verification_hash: str = Field(..., example="sha256:c7ba9851c56f6d474290bf459b5cd09b9027eed31589ca47d582b71ca80e91d9")

class EvidenceItemResponse(BaseModel):
    evidence_id: str = Field(..., example="EVID_ERP_ATL_STOCKOUT_001")
    source: str = Field(..., example="SAP S/4HANA Supply Chain Logistics (MM-WM)")
    source_record_id: str = Field(..., example="INV-SNAP-21971")
    source_domain: str = Field(..., example="ERP")
    timestamp: str = Field(..., example="2026-08-05T06:00:00Z")
    freshness: FreshnessModel
    evidence_type: str = Field(..., example="TELEMETRY_LOG")
    analytical_method: str = Field(..., example="DC Stockout Duration & Demand Gap Analysis")
    finding_summary: Optional[str] = Field(None, example="Atlanta-DC-01 inventory availability dropped to 68.2% for SKU-8821...")
    contribution: ContributionModel
    confidence: ConfidenceModel
    supports_driver: str = Field(..., example="atlanta_dc_stockout")
    supports_kpi: str = Field(..., example="north_america_east_revenue")
    lineage: LineageMetadataModel
    evidence_rank: Optional[int] = Field(None, example=1)
    ranking_score: Optional[float] = Field(None, example=95.0)

class EvidenceListResponse(BaseModel):
    kpi_id: str = Field(..., example="north_america_east_revenue")
    total_evidence_count: int = Field(..., example=9)
    evidence: List[EvidenceItemResponse]

class AllEvidenceListResponse(BaseModel):
    region: str = Field("NA-East", example="NA-East")
    total_evidence_count: int = Field(..., example=9)
    evidence: List[EvidenceItemResponse]

class LineageTraceResponse(BaseModel):
    evidence_id: str = Field(..., example="EVID_ERP_ATL_STOCKOUT_001")
    kpi: str = Field(..., example="north_america_east_revenue")
    driver: str = Field(..., example="atlanta_dc_stockout")
    source_system: str = Field(..., example="SAP S/4HANA Supply Chain Logistics (MM-WM)")
    source_domain: str = Field(..., example="ERP")
    source_record_id: str = Field(..., example="INV-SNAP-21971")
    lineage_metadata: LineageMetadataModel
    verification_hash: str = Field(..., example="sha256:c7ba9851c56f6d474290bf459b5cd09b9027eed31589ca47d582b71ca80e91d9")
