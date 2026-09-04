"""
InsightPilot AI — KPI Service Layer
Thin service orchestrating KPI calculations from the deterministic analytics engine.
"""

from typing import List, Dict, Any, Optional
from datetime import date
from analytics.data_loader import DataLoader
from analytics.kpi_engine import KPIEngine
from backend.app.schemas.kpi import KPIStateResponse
from backend.app.errors import KPINotFoundError

class KPIService:
    """Orchestrates deterministic KPI evaluations for API consumption."""
    
    SUPPORTED_KPIS = {
        "north_america_east_revenue": {
            "name": "North America East Revenue",
            "unit": "USD",
            "source_datasets": ["revenue.csv"]
        },
        "gross_margin": {
            "name": "Gross Margin %",
            "unit": "PERCENT",
            "source_datasets": ["margin.csv", "revenue.csv"]
        },
        "units_sold": {
            "name": "Units Sold",
            "unit": "UNITS",
            "source_datasets": ["sales.csv"]
        },
        "distributor_orders": {
            "name": "Distributor Orders Count",
            "unit": "COUNT",
            "source_datasets": ["distributor_orders.csv"]
        },
        "inventory_availability": {
            "name": "Inventory Availability %",
            "unit": "PERCENT",
            "source_datasets": ["inventory.csv"]
        }
    }

    def __init__(self, data_loader: Optional[DataLoader] = None):
        self.loader = data_loader or DataLoader()
        self.kpi_engine = KPIEngine(self.loader)

    def get_kpi_state(
        self,
        kpi_id: str,
        region: str = "NA-East",
        prev_period_id: str = "2026-Q2",
        curr_period_id: str = "2026-Q3"
    ) -> KPIStateResponse:
        """Evaluates and returns structured state for a specific KPI."""
        if kpi_id not in self.SUPPORTED_KPIS:
            raise KPINotFoundError(kpi_id)

        meta = self.SUPPORTED_KPIS[kpi_id]

        if kpi_id == "north_america_east_revenue":
            eval_res = self.kpi_engine.evaluate_kpi_movement(kpi_id, region, prev_period_id, curr_period_id)
        elif kpi_id == "gross_margin":
            prev_val = self.kpi_engine.calculate_gross_margin(region, prev_period_id)
            curr_val = self.kpi_engine.calculate_gross_margin(region, curr_period_id)
            var_val = round(curr_val - prev_val, 2)
            pct_change = var_val
            eval_res = {
                "id": kpi_id,
                "name": meta["name"],
                "current_value": curr_val,
                "previous_value": prev_val,
                "variance_amount": var_val,
                "percent_change": pct_change,
                "materiality_status": "WARNING" if var_val < 0 else "NORMAL"
            }
        elif kpi_id == "units_sold":
            q2_start, q2_end = date(2026, 4, 1), date(2026, 6, 30)
            q3_start, q3_end = date(2026, 7, 1), date(2026, 9, 30)
            prev_val = float(self.kpi_engine.calculate_units_sold(region, q2_start, q2_end))
            curr_val = float(self.kpi_engine.calculate_units_sold(region, q3_start, q3_end))
            var_val = round(curr_val - prev_val, 2)
            pct_change = round(((curr_val - prev_val) / prev_val) * 100.0, 2) if prev_val else 0.0
            eval_res = {
                "id": kpi_id,
                "name": meta["name"],
                "current_value": curr_val,
                "previous_value": prev_val,
                "variance_amount": var_val,
                "percent_change": pct_change,
                "materiality_status": "CRITICAL_NEGATIVE_VARIANCE" if pct_change <= -5.0 else "NORMAL"
            }
        elif kpi_id == "distributor_orders":
            q2_start, q2_end = date(2026, 4, 1), date(2026, 6, 30)
            q3_start, q3_end = date(2026, 7, 1), date(2026, 9, 30)
            prev_val = float(self.kpi_engine.calculate_distributor_orders(region, q2_start, q2_end))
            curr_val = float(self.kpi_engine.calculate_distributor_orders(region, q3_start, q3_end))
            var_val = round(curr_val - prev_val, 2)
            pct_change = round(((curr_val - prev_val) / prev_val) * 100.0, 2) if prev_val else 0.0
            eval_res = {
                "id": kpi_id,
                "name": meta["name"],
                "current_value": curr_val,
                "previous_value": prev_val,
                "variance_amount": var_val,
                "percent_change": pct_change,
                "materiality_status": "CRITICAL_NEGATIVE_VARIANCE" if pct_change <= -5.0 else "NORMAL"
            }
        elif kpi_id == "inventory_availability":
            q2_start, q2_end = date(2026, 4, 1), date(2026, 6, 30)
            disrupt_start, disrupt_end = date(2026, 8, 1), date(2026, 8, 19)
            prev_val = self.kpi_engine.calculate_inventory_availability(region, q2_start, q2_end)
            curr_val = self.kpi_engine.calculate_inventory_availability(region, disrupt_start, disrupt_end, dc_location="Atlanta-DC-01")
            var_val = round(curr_val - prev_val, 2)
            eval_res = {
                "id": kpi_id,
                "name": meta["name"],
                "current_value": curr_val,
                "previous_value": prev_val,
                "variance_amount": var_val,
                "percent_change": var_val,
                "materiality_status": "CRITICAL_NEGATIVE_VARIANCE" if var_val <= -10.0 else "NORMAL"
            }
        else:
            raise KPINotFoundError(kpi_id)

        return KPIStateResponse(
            id=eval_res["id"],
            name=eval_res["name"],
            region=region,
            current_period=curr_period_id,
            previous_period=prev_period_id,
            current_value=eval_res["current_value"],
            previous_value=eval_res["previous_value"],
            variance_amount=eval_res["variance_amount"],
            percent_change=eval_res["percent_change"],
            materiality_status=eval_res["materiality_status"],
            unit=meta["unit"],
            source_datasets=meta["source_datasets"]
        )

    def get_all_kpi_states(
        self,
        region: str = "NA-East",
        prev_period_id: str = "2026-Q2",
        curr_period_id: str = "2026-Q3"
    ) -> List[KPIStateResponse]:
        """Calculates and returns state for all supported KPIs."""
        return [
            self.get_kpi_state(kpi_id, region, prev_period_id, curr_period_id)
            for kpi_id in self.SUPPORTED_KPIS
        ]
