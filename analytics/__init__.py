"""
InsightPilot AI — Analytics Engine Package
Accenture Innovation Challenge 2026 — Track 3: BusinessIntelligence.ai

Deterministic KPI calculations, multi-factor driver decomposition,
confidence scoring, and investigation orchestration.
"""

from analytics.data_loader import DataLoader
from analytics.kpi_engine import KPIEngine
from analytics.driver_engine import DriverEngine
from analytics.confidence_engine import ConfidenceEngine
from analytics.investigation_engine import InvestigationEngine

__all__ = [
    "DataLoader",
    "KPIEngine",
    "DriverEngine",
    "ConfidenceEngine",
    "InvestigationEngine",
]
