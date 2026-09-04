"""
InsightPilot AI — KPI API Schemas
Models for KPI definitions and calculated state responses.
"""

from typing import List, Optional
from pydantic import BaseModel, Field

class KPIDefinition(BaseModel):
    id: str = Field(..., example="north_america_east_revenue", description="Unique KPI identifier")
    name: str = Field(..., example="North America East Revenue", description="Human-readable KPI name")
    domain: str = Field(..., example="FINANCE_REVENUE", description="Business domain category")
    aggregation_level: str = Field(..., example="REGIONAL_QUARTERLY", description="Aggregation granularity")
    unit: str = Field(..., example="USD", description="Measurement unit")
    materiality_threshold_pct: float = Field(..., example=-3.0, description="Materiality threshold percentage")

class KPIStateResponse(BaseModel):
    id: str = Field(..., example="north_america_east_revenue", description="KPI identifier")
    name: str = Field(..., example="North America East Revenue", description="KPI name")
    region: str = Field(..., example="NA-East", description="Target region")
    current_period: str = Field(..., example="2026-Q3", description="Current evaluation period")
    previous_period: str = Field(..., example="2026-Q2", description="Previous baseline period")
    current_value: float = Field(..., example=14200000.05, description="Current period value")
    previous_value: float = Field(..., example=15430000.06, description="Previous baseline value")
    variance_amount: float = Field(..., example=-1230000.01, description="Absolute variance")
    percent_change: float = Field(..., example=-7.97, description="Percentage change")
    materiality_status: str = Field(..., example="CRITICAL_NEGATIVE_VARIANCE", description="Materiality flag")
    unit: str = Field(..., example="USD", description="Measurement unit")
    source_datasets: List[str] = Field(..., description="Underlying enterprise datasets used in calculation")

class KPIListResponse(BaseModel):
    total_count: int = Field(..., example=5, description="Total number of supported KPIs")
    kpis: List[KPIStateResponse] = Field(..., description="List of calculated KPI states")
