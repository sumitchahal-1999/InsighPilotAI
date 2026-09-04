"""
InsightPilot AI — Deterministic KPI Engine
Implements mathematically rigorous, contract-compliant calculations for all 5 core KPIs.
"""

from typing import Dict, Any, Optional, Tuple
from datetime import date
from analytics.data_loader import DataLoader
from analytics.config import (
    PERIOD_DATES,
    DEFAULT_WARNING_THRESHOLD_PCT,
    DEFAULT_CRITICAL_THRESHOLD_PCT,
    MINIMUM_HISTORICAL_DAYS_REQUIRED
)
from analytics.utils import get_fiscal_quarter

class KPIEngine:
    """Calculates deterministic KPI values, variances, materiality, and history sufficiency."""
    
    def __init__(self, data_loader: Optional[DataLoader] = None):
        self.loader = data_loader or DataLoader()

    def get_period_dates(self, period_id: str) -> Tuple[date, date]:
        """Resolves period identifier (e.g. 2026-Q3) to start and end date objects."""
        if period_id in PERIOD_DATES:
            return PERIOD_DATES[period_id]
        raise ValueError(f"Unknown period identifier: {period_id}. Supported: {list(PERIOD_DATES.keys())}")

    def check_sparse_history(self, start_date: date, end_date: date, min_days: int = MINIMUM_HISTORICAL_DAYS_REQUIRED) -> Dict[str, Any]:
        """Evaluates whether time span meets minimum historical baseline requirements."""
        total_days = (end_date - start_date).days + 1
        if total_days < min_days:
            return {
                "status": "INSUFFICIENT_HISTORY",
                "days_available": total_days,
                "days_required": min_days,
                "is_sparse": True,
                "message": f"Insufficient historical baseline ({total_days} days available vs {min_days} days required). Causal attribution suspended."
            }
        return {
            "status": "SUFFICIENT_HISTORY",
            "days_available": total_days,
            "days_required": min_days,
            "is_sparse": False,
            "message": "Historical baseline is sufficient for time-series analysis."
        }

    # -------------------------------------------------------------------------
    # Core KPI Calculation Methods
    # -------------------------------------------------------------------------
    def calculate_revenue(self, region: str, start_date: date, end_date: date, sku_id: Optional[str] = None) -> float:
        """Calculates SUM(net_revenue) for posted invoices in the specified region and date window."""
        revenue_records = self.loader.get_revenue()
        total_net_rev = 0.0
        for r in revenue_records:
            if r["region"] == region and r["posting_status"] == "POSTED":
                if start_date <= r["invoice_date"] <= end_date:
                    if sku_id is None or r["sku_id"] == sku_id:
                        total_net_rev += r["net_revenue"]
        return round(total_net_rev, 2)

    def calculate_gross_margin(self, region: str, period_id: str, sku_id: Optional[str] = None) -> float:
        """Calculates Gross Margin %: ((Revenue - COGS) / Revenue) * 100 from margin records."""
        margin_records = self.loader.get_margin()
        total_rev = 0.0
        total_profit = 0.0
        for m in margin_records:
            if m["region"] == region and m["fiscal_period"] == period_id:
                if sku_id is None or m["sku_id"] == sku_id:
                    total_rev += m["sales_revenue"]
                    total_profit += m["gross_profit"]
        if total_rev == 0:
            return 0.0
        return round((total_profit / total_rev) * 100.0, 2)

    def calculate_units_sold(self, region: str, start_date: date, end_date: date, sku_id: Optional[str] = None) -> int:
        """Calculates SUM(units_sold) delivered across accounts."""
        sales_records = self.loader.get_sales()
        total_units = 0
        for s in sales_records:
            if s["region"] == region and s["delivery_status"] in ("DELIVERED", "PARTIAL"):
                if start_date <= s["transaction_date"] <= end_date:
                    if sku_id is None or s["sku_id"] == sku_id:
                        total_units += s["units_sold"]
        return total_units

    def calculate_distributor_orders(self, region: str, start_date: date, end_date: date) -> int:
        """Calculates COUNT(DISTINCT po_id) purchase orders submitted by distributors."""
        dist_orders = self.loader.get_distributor_orders()
        po_ids = set()
        for o in dist_orders:
            if o["region"] == region:
                if start_date <= o["order_date"] <= end_date:
                    po_ids.add(o["po_id"])
        return len(po_ids)

    def calculate_inventory_availability(self, region: str, start_date: date, end_date: date, dc_location: Optional[str] = None, sku_id: Optional[str] = None) -> float:
        """Calculates (SUM(available_units) / SUM(required_demand_units)) * 100."""
        inventory_records = self.loader.get_inventory()
        total_avail = 0
        total_demand = 0
        for inv in inventory_records:
            if inv["region"] == region:
                if start_date <= inv["snapshot_date"] <= end_date:
                    if dc_location is None or inv["dc_location"] == dc_location:
                        if sku_id is None or inv["sku_id"] == sku_id:
                            total_avail += inv["available_units"]
                            total_demand += inv["required_demand_units"]
        if total_demand == 0:
            return 0.0
        return round((total_avail / total_demand) * 100.0, 2)

    # -------------------------------------------------------------------------
    # KPI Movement & Materiality Analysis
    # -------------------------------------------------------------------------
    def evaluate_kpi_movement(
        self,
        kpi_id: str,
        region: str,
        prev_period_id: str,
        curr_period_id: str
    ) -> Dict[str, Any]:
        """Calculates previous value, current value, percentage change, and materiality status."""
        prev_start, prev_end = self.get_period_dates(prev_period_id)
        curr_start, curr_end = self.get_period_dates(curr_period_id)
        
        if kpi_id == "north_america_east_revenue" or kpi_id == "revenue":
            prev_val = self.calculate_revenue(region, prev_start, prev_end)
            curr_val = self.calculate_revenue(region, curr_start, curr_end)
            kpi_name = "North America East Revenue"
            unit = "USD"
        elif kpi_id == "gross_margin":
            prev_val = self.calculate_gross_margin(region, prev_period_id)
            curr_val = self.calculate_gross_margin(region, curr_period_id)
            kpi_name = "Gross Margin"
            unit = "PERCENTAGE"
        elif kpi_id == "units_sold":
            prev_val = float(self.calculate_units_sold(region, prev_start, prev_end))
            curr_val = float(self.calculate_units_sold(region, curr_start, curr_end))
            kpi_name = "Units Sold"
            unit = "UNITS"
        elif kpi_id == "distributor_orders":
            prev_val = float(self.calculate_distributor_orders(region, prev_start, prev_end))
            curr_val = float(self.calculate_distributor_orders(region, curr_start, curr_end))
            kpi_name = "Distributor Orders"
            unit = "ORDER_COUNT"
        elif kpi_id == "inventory_availability":
            prev_val = self.calculate_inventory_availability(region, prev_start, prev_end)
            curr_val = self.calculate_inventory_availability(region, curr_start, curr_end)
            kpi_name = "Inventory Availability"
            unit = "PERCENTAGE"
        else:
            raise ValueError(f"Unsupported KPI identifier: {kpi_id}")

        variance_amount = round(curr_val - prev_val, 2)
        if prev_val != 0:
            if unit == "PERCENTAGE":
                percent_change = round(curr_val - prev_val, 2)
            else:
                percent_change = round(((curr_val - prev_val) / prev_val) * 100.0, 2)
        else:
            percent_change = 0.0

        # Materiality status evaluation
        if percent_change <= DEFAULT_CRITICAL_THRESHOLD_PCT:
            materiality = "CRITICAL_NEGATIVE_VARIANCE"
        elif percent_change <= DEFAULT_WARNING_THRESHOLD_PCT:
            materiality = "WARNING"
        else:
            materiality = "NOMINAL"

        return {
            "id": kpi_id,
            "name": kpi_name,
            "unit": unit,
            "region": region,
            "previous_period": prev_period_id,
            "current_period": curr_period_id,
            "previous_value": prev_val,
            "current_value": curr_val,
            "variance_amount": variance_amount,
            "percent_change": percent_change,
            "materiality_status": materiality
        }
