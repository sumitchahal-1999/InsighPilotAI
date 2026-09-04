"""
InsightPilot AI — Database Models Package
Exports all raw dataset and analytical SQLAlchemy ORM models.
"""

from backend.app.db.base import Base
from backend.app.db.models.raw_data import (
    RawRevenueRecord,
    RawInventoryRecord,
    RawMarginRecord,
    RawSalesRecord,
    RawDistributorOrderRecord,
    RawSupportTicketRecord,
    RawDistributorCommunicationRecord,
    RawMarketIntelligenceRecord
)
from backend.app.db.models.analytics import (
    KPIDefinitionRecord,
    InvestigationRecord,
    InvestigationDriverRecord,
    EvidenceRecordModel,
    RecommendationRecordModel,
    SimulationRunRecord
)

__all__ = [
    "Base",
    "RawRevenueRecord",
    "RawInventoryRecord",
    "RawMarginRecord",
    "RawSalesRecord",
    "RawDistributorOrderRecord",
    "RawSupportTicketRecord",
    "RawDistributorCommunicationRecord",
    "RawMarketIntelligenceRecord",
    "KPIDefinitionRecord",
    "InvestigationRecord",
    "InvestigationDriverRecord",
    "EvidenceRecordModel",
    "RecommendationRecordModel",
    "SimulationRunRecord"
]
