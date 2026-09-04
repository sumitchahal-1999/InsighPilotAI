"""
InsightPilot AI — What-If Simulation Routes
Exposes deterministic what-if scenario simulations for operational parameter adjustments.
"""

from fastapi import APIRouter, Depends, Query, status
from backend.app.schemas.simulation import (
    SimulationRequest,
    SimulationResponse,
    SimulationBaselineResponse
)
from backend.app.schemas.common import ErrorResponse
from backend.app.services.simulation_service import SimulationService
from backend.app.dependencies import get_simulation_service

router = APIRouter(prefix="/simulations", tags=["What-If Simulations"])

@router.get(
    "/baseline",
    response_model=SimulationBaselineResponse,
    summary="Get simulation baseline state",
    description="Returns the empirical baseline inventory availability and current revenue before intervention."
)
async def get_simulation_baseline(
    region: str = Query("NA-East", description="Target geographical region"),
    simulation_service: SimulationService = Depends(get_simulation_service)
) -> SimulationBaselineResponse:
    """Returns empirical baseline state for simulation comparison."""
    return simulation_service.get_baseline(region=region)

@router.post(
    "/inventory-availability",
    response_model=SimulationResponse,
    responses={400: {"model": ErrorResponse, "description": "Invalid simulation parameter"}},
    summary="Simulate inventory availability recovery",
    description="Calculates deterministic revenue and margin recovery projections under a target inventory availability slider setting."
)
async def simulate_inventory_availability(
    request: SimulationRequest,
    region: str = Query("NA-East", description="Target geographical region"),
    simulation_service: SimulationService = Depends(get_simulation_service)
) -> SimulationResponse:
    """Runs deterministic simulation on inventory availability slider parameter."""
    avail_val = request.inventory_availability if request.inventory_availability is not None else (request.target_availability_pct or 90.0)
    target_region = request.region or region
    return simulation_service.simulate_availability(
        inventory_availability=avail_val,
        region=target_region
    )

@router.post(
    "/run",
    response_model=SimulationResponse,
    responses={400: {"model": ErrorResponse, "description": "Invalid simulation parameter"}},
    summary="Run what-if simulation (Unified alias)",
    description="Unified simulation runner accepting target availability percentage or ratio."
)
async def run_simulation(
    request: SimulationRequest,
    region: str = Query("NA-East", description="Target geographical region"),
    simulation_service: SimulationService = Depends(get_simulation_service)
) -> SimulationResponse:
    """Unified simulation runner endpoint."""
    avail_val = request.inventory_availability if request.inventory_availability is not None else (request.target_availability_pct or 90.0)
    target_region = request.region or region
    return simulation_service.simulate_availability(
        inventory_availability=avail_val,
        region=target_region
    )
