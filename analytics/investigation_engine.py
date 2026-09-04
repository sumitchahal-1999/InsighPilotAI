"""
InsightPilot AI — Investigation Engine Orchestrator
Assembles end-to-end investigation results adhering strictly to data/schemas/investigation_result.json.
"""

from typing import Dict, Any, Optional
from datetime import datetime, timezone
from analytics.data_loader import DataLoader
from analytics.kpi_engine import KPIEngine
from analytics.driver_engine import DriverEngine
from analytics.confidence_engine import ConfidenceEngine
from analytics.config import PREVIOUS_PERIOD_ID, CURRENT_PERIOD_ID

class InvestigationEngine:
    """Orchestrates KPI calculation, driver decomposition, confidence scoring, and lineage graph assembly."""
    
    def __init__(self, data_loader: Optional[DataLoader] = None):
        self.loader = data_loader or DataLoader()
        self.kpi_engine = KPIEngine(self.loader)
        self.driver_engine = DriverEngine(self.loader)
        self.confidence_engine = ConfidenceEngine()

    def run_investigation(
        self,
        kpi_id: str = "north_america_east_revenue",
        region: str = "NA-East",
        prev_period_id: str = PREVIOUS_PERIOD_ID,
        curr_period_id: str = CURRENT_PERIOD_ID,
        persona_id: str = "CFO",
        investigation_id: str = "INV-EXEC-2026-NAE-001"
    ) -> Dict[str, Any]:
        """Executes full deterministic investigation pipeline and returns schema-compliant dictionary."""
        
        # 1. Evaluate KPI Movement
        kpi_eval = self.kpi_engine.evaluate_kpi_movement(
            kpi_id=kpi_id,
            region=region,
            prev_period_id=prev_period_id,
            curr_period_id=curr_period_id
        )
        
        # 2. Decompose Multi-Factor Drivers
        drivers = self.driver_engine.investigate_revenue_drivers(
            region=region,
            prev_period_id=prev_period_id,
            curr_period_id=curr_period_id
        )
        
        # 3. Compute Overall Confidence & Abstention Status
        overall_conf = self.confidence_engine.calculate_overall_confidence(drivers)
        
        # 4. Aggregate Evidence Summary
        all_evidence_ids = []
        for d in drivers:
            all_evidence_ids.extend(d.get("evidence_ids", []))
            
        unique_evidence_ids = list(dict.fromkeys(all_evidence_ids))
        
        evidence_summary = {
            "evidence_ids": unique_evidence_ids,
            "source_count": 3,
            "source_domains": ["ERP", "CRM_SALES", "SUPPORT_MARKET_INTEL"]
        }
        
        # 5. Build Lineage Graph
        lineage_graph = {
            "kpi_node": kpi_eval["id"],
            "driver_nodes": [d["driver_id"] for d in drivers],
            "evidence_nodes": unique_evidence_ids
        }
        
        # Format driver records to match schema exactly
        formatted_drivers = []
        for d in drivers:
            formatted_drivers.append({
                "driver_id": d["driver_id"],
                "driver_name": d["driver_name"],
                "contribution_pct": d["contribution_pct"],
                "impact_usd": d["impact_usd"],
                "confidence_score": d["confidence_score"],
                "rank": d["rank"],
                "evidence_ids": d["evidence_ids"]
            })
            
        # Format KPI block
        formatted_kpi = {
            "id": kpi_eval["id"],
            "name": kpi_eval["name"],
            "current_value": kpi_eval["current_value"],
            "previous_value": kpi_eval["previous_value"],
            "variance_amount": kpi_eval["variance_amount"],
            "percent_change": kpi_eval["percent_change"],
            "materiality_status": kpi_eval["materiality_status"]
        }
        
        timestamp_str = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        
        return {
            "investigation_id": investigation_id,
            "timestamp": timestamp_str,
            "persona_id": persona_id,
            "kpi": formatted_kpi,
            "drivers": formatted_drivers,
            "evidence_summary": evidence_summary,
            "overall": overall_conf,
            "lineage_graph": lineage_graph
        }
