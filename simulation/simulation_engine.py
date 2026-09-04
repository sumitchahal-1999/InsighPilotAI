"""
InsightPilot AI — Deterministic What-If Simulation Engine
Simulates revenue and margin recovery projections under operational parameter adjustments.
"""

from typing import Dict, Any, Optional
from datetime import date
from analytics.data_loader import DataLoader
from analytics.kpi_engine import KPIEngine
from analytics.driver_engine import DriverEngine

class SimulationEngine:
    """Deterministic simulation engine projecting KPI recovery from operational intervention sliders."""

    def __init__(self, data_loader: Optional[DataLoader] = None):
        self.loader = data_loader or DataLoader()
        self.kpi_engine = KPIEngine(self.loader)
        self.driver_engine = DriverEngine(self.loader)

    def get_baseline_state(self, region: str = "NA-East") -> Dict[str, Any]:
        """Calculates current empirical baseline availability and revenue."""
        # 1. Baseline Atlanta DC Availability during disruption
        disrupt_start, disrupt_end = date(2026, 8, 1), date(2026, 8, 19)
        baseline_avail = self.kpi_engine.calculate_inventory_availability(
            region=region,
            start_date=disrupt_start,
            end_date=disrupt_end,
            dc_location="Atlanta-DC-01"
        )
        
        # 2. Baseline Q3 Revenue
        q3_start, q3_end = date(2026, 7, 1), date(2026, 9, 30)
        baseline_rev = self.kpi_engine.calculate_revenue(region, q3_start, q3_end)

        return {
            "baseline_availability_pct": round(baseline_avail, 1),
            "baseline_availability_ratio": round(baseline_avail / 100.0, 3),
            "baseline_revenue_usd": round(baseline_rev, 2)
        }

    def simulate_inventory_availability(
        self,
        inventory_availability: float,
        region: str = "NA-East"
    ) -> Dict[str, Any]:
        """
        Simulates revenue recovery under a target inventory availability parameter.
        Accepts inventory_availability as ratio (e.g. 0.90) or percentage (e.g. 90.0).
        """
        # 1. Input Validation & Normalization
        if not isinstance(inventory_availability, (int, float)):
            raise ValueError(f"Invalid input: inventory_availability must be numeric, got {type(inventory_availability).__name__}.")

        norm_avail = float(inventory_availability)
        if norm_avail > 1.0:
            norm_avail = norm_avail / 100.0

        if norm_avail < 0.0 or norm_avail > 1.0:
            raise ValueError(f"Inventory availability must be between 0.0 and 1.0 (0% to 100%), got {inventory_availability}.")

        scenario_pct = round(norm_avail * 100.0, 1)

        # 2. Retrieve Baseline State
        baseline_data = self.get_baseline_state(region)
        baseline_pct = baseline_data["baseline_availability_pct"] # 72.4%
        baseline_ratio = baseline_data["baseline_availability_ratio"] # 0.724
        baseline_revenue = baseline_data["baseline_revenue_usd"] # $14,200,000.05

        # 3. Calculate Availability Delta
        delta_pct = round(scenario_pct - baseline_pct, 1)
        delta_ratio = round(norm_avail - baseline_ratio, 3)

        # 4. Deterministic Recovery Mathematical Model
        # Recoverable pool: Atlanta stockout impact ($550k) + SKU-8821 commercial volume recovery ($204k) = $754k
        recoverable_revenue_pool = 754000.00
        max_availability_gap = max(0.01, 1.0 - baseline_ratio) # 0.276
        
        if delta_ratio > 0:
            improvement_factor = min(1.0, delta_ratio / max_availability_gap)
            # Recovery elasticity: 0.88
            revenue_recovery = round(recoverable_revenue_pool * improvement_factor * 0.88, 2)
            margin_recovery = round(improvement_factor * 1.4, 2)
        else:
            revenue_recovery = 0.0
            margin_recovery = 0.0

        projected_revenue = round(baseline_revenue + revenue_recovery, 2)

        assumptions = [
            f"Inter-DC inventory transfer from Charlotte Hub to Atlanta DC completes within 72 hours",
            f"Baseline Atlanta DC availability during August disruption was {baseline_pct:.1f}%",
            f"Recoverable revenue pool bounded at ${recoverable_revenue_pool:,.2f} across fulfillment drivers",
            f"Tier-1 distributor re-order elasticity modeled at 0.88 relative to stock restoration",
            f"Direct expedited freight costs modeled at $28,000"
        ]

        conf_score = 91 if scenario_pct >= 85.0 else 85
        conf_label = "HIGH" if conf_score >= 80 else "MEDIUM"

        return {
            "simulation_id": f"SIM-RUN-2026-ATL-{int(scenario_pct)}",
            "simulation_name": f"Atlanta DC Inventory Restoration to {scenario_pct:.1f}%",
            "input_variable": "inventory_availability",
            "target_facility_or_scope": "Atlanta DC (Atlanta-DC-01) / NA-East",
            "baseline_value": baseline_pct,
            "scenario_value": scenario_pct,
            "availability_delta": delta_pct,
            "baseline_revenue_usd": baseline_revenue,
            "projected_metric": "north_america_east_revenue",
            "projected_value": projected_revenue,
            "estimated_recovery": {
                "revenue_recovery_usd": revenue_recovery,
                "margin_recovery_pct": margin_recovery,
                "recovery_timeframe_days": 14
            },
            "assumptions": assumptions,
            "confidence": {
                "score": conf_score,
                "label": conf_label
            }
        }
