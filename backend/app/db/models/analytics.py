"""
InsightPilot AI — Analytical & Investigation Database Models
SQLAlchemy ORM models for KPI metadata, investigations, drivers, evidence, recommendations, and simulations.
"""

from datetime import datetime
from typing import Optional, List
from sqlalchemy import String, Float, Integer, DateTime, Boolean, Text, JSON, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.app.db.base import Base

class KPIDefinitionRecord(Base):
    """Authoritative KPI metadata registry."""
    __tablename__ = "kpi_definitions"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    category: Mapped[str] = mapped_column(String(64), default="Finance", nullable=False)
    formula: Mapped[str] = mapped_column(String(255), nullable=False)
    unit: Mapped[str] = mapped_column(String(16), default="USD", nullable=False)
    direction: Mapped[str] = mapped_column(String(16), default="HIGHER_IS_BETTER", nullable=False)
    default_period: Mapped[str] = mapped_column(String(16), default="2026-Q3", nullable=False)
    materiality_threshold_pct: Mapped[float] = mapped_column(Float, default=5.0, nullable=False)
    source_datasets: Mapped[dict] = mapped_column(JSON, default=list, nullable=False)

class InvestigationRecord(Base):
    """Deterministic investigation runs and executive diagnostic states."""
    __tablename__ = "investigations"

    investigation_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    kpi_id: Mapped[str] = mapped_column(String(64), ForeignKey("kpi_definitions.id"), index=True, nullable=False)
    region: Mapped[str] = mapped_column(String(32), default="NA-East", nullable=False)
    prev_period_id: Mapped[str] = mapped_column(String(16), default="2026-Q2", nullable=False)
    curr_period_id: Mapped[str] = mapped_column(String(16), default="2026-Q3", nullable=False)
    persona_id: Mapped[str] = mapped_column(String(32), default="CFO", nullable=False)
    baseline_value: Mapped[float] = mapped_column(Float, nullable=False)
    current_value: Mapped[float] = mapped_column(Float, nullable=False)
    variance_amount: Mapped[float] = mapped_column(Float, nullable=False)
    percent_change: Mapped[float] = mapped_column(Float, nullable=False)
    materiality_status: Mapped[str] = mapped_column(String(64), nullable=False)
    overall_confidence: Mapped[int] = mapped_column(Integer, default=89, nullable=False)
    confidence_label: Mapped[str] = mapped_column(String(16), default="HIGH", nullable=False)
    abstention: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    abstention_reason: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    drivers: Mapped[List["InvestigationDriverRecord"]] = relationship(
        "InvestigationDriverRecord", back_populates="investigation", cascade="all, delete-orphan"
    )

class InvestigationDriverRecord(Base):
    """Ranked explanatory drivers attached to an investigation."""
    __tablename__ = "investigation_drivers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    investigation_id: Mapped[str] = mapped_column(String(64), ForeignKey("investigations.investigation_id"), index=True, nullable=False)
    driver_id: Mapped[str] = mapped_column(String(64), index=True, nullable=False)
    driver_name: Mapped[str] = mapped_column(String(128), nullable=False)
    rank: Mapped[int] = mapped_column(Integer, nullable=False)
    contribution_pct: Mapped[float] = mapped_column(Float, nullable=False)
    impact_usd: Mapped[float] = mapped_column(Float, nullable=False)
    confidence_score: Mapped[int] = mapped_column(Integer, nullable=False)
    category: Mapped[str] = mapped_column(String(64), nullable=False)
    controllability: Mapped[str] = mapped_column(String(32), default="DIRECTLY_CONTROLLABLE", nullable=False)
    evidence_ids: Mapped[dict] = mapped_column(JSON, default=list, nullable=False)

    investigation: Mapped["InvestigationRecord"] = relationship("InvestigationRecord", back_populates="drivers")

class EvidenceRecordModel(Base):
    """Empirical verified evidence nodes and cryptographic lineage metadata."""
    __tablename__ = "evidence_records"

    evidence_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    source: Mapped[str] = mapped_column(String(128), nullable=False)
    source_record_id: Mapped[str] = mapped_column(String(64), nullable=False)
    source_domain: Mapped[str] = mapped_column(String(32), index=True, nullable=False)
    timestamp: Mapped[str] = mapped_column(String(64), nullable=False)
    age_hours: Mapped[float] = mapped_column(Float, nullable=False)
    freshness_status: Mapped[str] = mapped_column(String(32), default="RECENT", nullable=False)
    evidence_type: Mapped[str] = mapped_column(String(64), nullable=False)
    analytical_method: Mapped[str] = mapped_column(String(128), nullable=False)
    finding_summary: Mapped[str] = mapped_column(Text, nullable=False)
    contribution_pct: Mapped[float] = mapped_column(Float, nullable=False)
    monetary_impact_usd: Mapped[float] = mapped_column(Float, nullable=False)
    confidence_score: Mapped[int] = mapped_column(Integer, nullable=False)
    confidence_label: Mapped[str] = mapped_column(String(16), default="HIGH", nullable=False)
    supports_driver: Mapped[str] = mapped_column(String(64), index=True, nullable=False)
    supports_kpi: Mapped[str] = mapped_column(String(64), default="north_america_east_revenue", nullable=False)
    source_table: Mapped[str] = mapped_column(String(128), nullable=False)
    pipeline_job_id: Mapped[str] = mapped_column(String(128), nullable=False)
    verification_hash: Mapped[str] = mapped_column(String(128), nullable=False)

class RecommendationRecordModel(Base):
    """Prescriptive action levers and strategic intervention records."""
    __tablename__ = "recommendations"

    recommendation_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    kpi_id: Mapped[str] = mapped_column(String(64), ForeignKey("kpi_definitions.id"), index=True, nullable=False)
    driver_id: Mapped[str] = mapped_column(String(64), nullable=False)
    driver_name: Mapped[str] = mapped_column(String(128), nullable=False)
    priority: Mapped[str] = mapped_column(String(32), default="CRITICAL", nullable=False)
    priority_rank: Mapped[int] = mapped_column(Integer, nullable=False)
    controllability: Mapped[str] = mapped_column(String(32), default="DIRECTLY_CONTROLLABLE", nullable=False)
    controllable_lever: Mapped[str] = mapped_column(String(128), nullable=False)
    action: Mapped[str] = mapped_column(String(255), nullable=False)
    rationale: Mapped[str] = mapped_column(Text, nullable=False)
    expected_recovery_usd: Mapped[float] = mapped_column(Float, nullable=False)
    expected_margin_lift_pts: Mapped[float] = mapped_column(Float, nullable=False)
    timeframe_days: Mapped[int] = mapped_column(Integer, default=14, nullable=False)
    owner: Mapped[str] = mapped_column(String(128), nullable=False)
    confidence_score: Mapped[int] = mapped_column(Integer, default=91, nullable=False)
    supporting_evidence_ids: Mapped[dict] = mapped_column(JSON, default=list, nullable=False)
    assumptions: Mapped[dict] = mapped_column(JSON, default=list, nullable=False)
    constraints: Mapped[dict] = mapped_column(JSON, default=list, nullable=False)

class SimulationRunRecord(Base):
    """Persisted What-If simulation execution records."""
    __tablename__ = "simulation_runs"

    simulation_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    scenario_name: Mapped[str] = mapped_column(String(128), nullable=False)
    region: Mapped[str] = mapped_column(String(32), default="NA-East", nullable=False)
    input_variable: Mapped[str] = mapped_column(String(64), default="inventory_availability", nullable=False)
    baseline_value: Mapped[float] = mapped_column(Float, nullable=False)
    scenario_value: Mapped[float] = mapped_column(Float, nullable=False)
    availability_delta: Mapped[float] = mapped_column(Float, nullable=False)
    projected_recovery_usd: Mapped[float] = mapped_column(Float, nullable=False)
    projected_total_revenue_usd: Mapped[float] = mapped_column(Float, nullable=False)
    projected_margin_impact_pts: Mapped[float] = mapped_column(Float, nullable=False)
    confidence_score: Mapped[int] = mapped_column(Integer, default=91, nullable=False)
    assumptions: Mapped[dict] = mapped_column(JSON, default=list, nullable=False)
