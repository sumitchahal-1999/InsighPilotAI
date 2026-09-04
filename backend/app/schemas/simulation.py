"""
InsightPilot AI — What-If Simulation API Schemas
Pydantic models matching data/schemas/simulation_contract.json.
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field, root_validator

class SimulationRequest(BaseModel):
    inventory_availability: Optional[float] = Field(
        None,
        example=0.90,
        description="Target inventory availability parameter (0.0 to 1.0 or 0% to 100%)"
    )
    target_availability_pct: Optional[float] = Field(
        None,
        example=90.0,
        description="Target inventory availability percentage (0% to 100%)"
    )
    scenario_name: Optional[str] = Field(
        "Atlanta DC Inventory Optimization",
        example="Atlanta DC Inventory Optimization"
    )
    region: Optional[str] = Field("NA-East", example="NA-East")

    @root_validator(pre=True)
    def validate_inputs(cls, values: dict) -> dict:
        avail = values.get("inventory_availability")
        target_pct = values.get("target_availability_pct")
        if avail is None and target_pct is None:
            raise ValueError("Either 'inventory_availability' or 'target_availability_pct' must be provided.")
        if avail is None and target_pct is not None:
            values["inventory_availability"] = target_pct
        return values

class SimulationRecoveryModel(BaseModel):
    revenue_recovery_usd: float = Field(..., example=421500.0)
    margin_recovery_pct: float = Field(..., example=1.4)
    recovery_timeframe_days: int = Field(..., example=14)

class SimulationConfidenceModel(BaseModel):
    score: int = Field(..., example=91)
    label: str = Field(..., example="HIGH")

class SimulationResponse(BaseModel):
    simulation_id: str = Field(..., example="SIM-RUN-2026-ATL-90")
    simulation_name: str = Field(...)
    input_variable: str = Field(..., example="inventory_availability")
    target_facility_or_scope: str = Field(..., example="Atlanta DC (Atlanta-DC-01) / NA-East")
    baseline_value: float = Field(..., example=79.4)
    scenario_value: float = Field(..., example=90.0)
    availability_delta: float = Field(..., example=10.6)
    baseline_revenue_usd: float = Field(..., example=14200000.05)
    projected_metric: str = Field(..., example="north_america_east_revenue")
    projected_value: float = Field(..., example=14541422.96)
    estimated_recovery: SimulationRecoveryModel
    assumptions: List[str] = Field(...)
    confidence: SimulationConfidenceModel

class SimulationBaselineResponse(BaseModel):
    baseline_availability_pct: float = Field(..., example=79.4)
    baseline_availability_ratio: float = Field(..., example=0.794)
    baseline_revenue_usd: float = Field(..., example=14200000.05)
