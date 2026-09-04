"""
InsightPilot AI — Simulation Service Layer
Orchestrates deterministic what-if scenario simulations for API endpoints.
"""

from typing import Optional, Dict, Any
from analytics.data_loader import DataLoader
from simulation.simulation_engine import SimulationEngine
from backend.app.schemas.simulation import (
    SimulationResponse,
    SimulationBaselineResponse,
    SimulationRecoveryModel,
    SimulationConfidenceModel
)
from backend.app.errors import APIError

class InvalidSimulationInputError(APIError):
    """Raised when simulation parameters are invalid."""
    def __init__(self, message: str):
        super().__init__(
            code="INVALID_SIMULATION_INPUT",
            message=message,
            status_code=400
        )

class SimulationService:
    """Service wrapping simulation.simulation_engine.SimulationEngine."""

    def __init__(self, data_loader: Optional[DataLoader] = None):
        self.loader = data_loader or DataLoader()
        self.engine = SimulationEngine(self.loader)

    def get_baseline(self, region: str = "NA-East") -> SimulationBaselineResponse:
        """Returns baseline empirical availability and revenue."""
        baseline = self.engine.get_baseline_state(region)
        return SimulationBaselineResponse(**baseline)

    def simulate_availability(
        self,
        inventory_availability: float,
        region: str = "NA-East"
    ) -> SimulationResponse:
        """Runs deterministic simulation on inventory availability parameter."""
        try:
            raw_sim = self.engine.simulate_inventory_availability(
                inventory_availability=inventory_availability,
                region=region
            )
        except ValueError as ve:
            raise InvalidSimulationInputError(str(ve))

        return SimulationResponse(
            simulation_id=raw_sim["simulation_id"],
            simulation_name=raw_sim["simulation_name"],
            input_variable=raw_sim["input_variable"],
            target_facility_or_scope=raw_sim["target_facility_or_scope"],
            baseline_value=raw_sim["baseline_value"],
            scenario_value=raw_sim["scenario_value"],
            availability_delta=raw_sim["availability_delta"],
            baseline_revenue_usd=raw_sim["baseline_revenue_usd"],
            projected_metric=raw_sim["projected_metric"],
            projected_value=raw_sim["projected_value"],
            estimated_recovery=SimulationRecoveryModel(**raw_sim["estimated_recovery"]),
            assumptions=raw_sim["assumptions"],
            confidence=SimulationConfidenceModel(**raw_sim["confidence"])
        )
