"""
InsightPilot AI — Evidence Service Layer
Orchestrates evidence retrieval and lineage tracing for API endpoints.
"""

from typing import Optional, List
from analytics.data_loader import DataLoader
from evidence.evidence_engine import EvidenceEngine
from backend.app.schemas.evidence import (
    EvidenceListResponse,
    AllEvidenceListResponse,
    EvidenceItemResponse,
    LineageTraceResponse,
    FreshnessModel,
    ContributionModel,
    ConfidenceModel,
    LineageMetadataModel
)
from backend.app.errors import KPINotFoundError, EvidenceNotFoundError

class EvidenceService:
    """Service layer delegating evidence extraction and lineage tracing to evidence.evidence_engine."""
    
    SUPPORTED_KPIS = {"north_america_east_revenue"}

    def __init__(self, data_loader: Optional[DataLoader] = None):
        self.loader = data_loader or DataLoader()
        self.evidence_engine = EvidenceEngine(self.loader)

    def _format_evidence_item(self, item: dict) -> EvidenceItemResponse:
        return EvidenceItemResponse(
            evidence_id=item["evidence_id"],
            source=item["source"],
            source_record_id=item["source_record_id"],
            source_domain=item["source_domain"],
            timestamp=item["timestamp"],
            freshness=FreshnessModel(**item["freshness"]),
            evidence_type=item["evidence_type"],
            analytical_method=item["analytical_method"],
            finding_summary=item.get("finding_summary"),
            contribution=ContributionModel(**item["contribution"]),
            confidence=ConfidenceModel(**item["confidence"]),
            supports_driver=item["supports_driver"],
            supports_kpi=item["supports_kpi"],
            lineage=LineageMetadataModel(**item["lineage"]),
            evidence_rank=item.get("evidence_rank"),
            ranking_score=item.get("ranking_score")
        )

    def get_all_evidence(
        self,
        domain: Optional[str] = None,
        search: Optional[str] = None,
        region: str = "NA-East"
    ) -> AllEvidenceListResponse:
        """Returns all verified evidence nodes across all domains with optional filtering."""
        evidence_bundle = self.evidence_engine.get_all_evidence_for_investigation(region)
        formatted_list = [
            self._format_evidence_item(node)
            for node in evidence_bundle["all_evidence_nodes"]
        ]

        if domain and domain.upper() != "ALL":
            domain_upper = domain.upper()
            formatted_list = [
                e for e in formatted_list
                if domain_upper in e.source_domain.upper() or domain_upper in e.source.upper()
            ]

        if search:
            q = search.lower()
            formatted_list = [
                e for e in formatted_list
                if q in e.evidence_id.lower()
                or (e.finding_summary and q in e.finding_summary.lower())
                or q in e.source.lower()
                or q in e.supports_driver.lower()
            ]

        return AllEvidenceListResponse(
            region=region,
            total_evidence_count=len(formatted_list),
            evidence=formatted_list
        )

    def get_investigation_evidence(self, kpi_id: str, region: str = "NA-East") -> EvidenceListResponse:
        """Returns all ranked evidence nodes substantiating the given KPI investigation."""
        if kpi_id not in self.SUPPORTED_KPIS:
            raise KPINotFoundError(kpi_id)

        evidence_bundle = self.evidence_engine.get_all_evidence_for_investigation(region)
        formatted_list = [
            self._format_evidence_item(node)
            for node in evidence_bundle["all_evidence_nodes"]
        ]

        return EvidenceListResponse(
            kpi_id=kpi_id,
            total_evidence_count=len(formatted_list),
            evidence=formatted_list
        )

    def get_single_evidence(self, evidence_id: str, region: str = "NA-East") -> EvidenceItemResponse:
        """Returns a single evidence item by ID."""
        evidence_bundle = self.evidence_engine.get_all_evidence_for_investigation(region)
        for node in evidence_bundle["all_evidence_nodes"]:
            if node["evidence_id"] == evidence_id:
                return self._format_evidence_item(node)
        raise EvidenceNotFoundError(evidence_id)

    def get_evidence_lineage(self, evidence_id: str, region: str = "NA-East") -> LineageTraceResponse:
        """Returns the full 5-layer lineage trace for a specific evidence item."""
        trace = self.evidence_engine.trace_lineage(evidence_id, region)
        if not trace:
            raise EvidenceNotFoundError(evidence_id)

        return LineageTraceResponse(
            evidence_id=trace["evidence_id"],
            kpi=trace["kpi"],
            driver=trace["driver"],
            source_system=trace["source_system"],
            source_domain=trace["source_domain"],
            source_record_id=trace["source_record_id"],
            lineage_metadata=LineageMetadataModel(**trace["lineage_metadata"]),
            verification_hash=trace["verification_hash"]
        )
