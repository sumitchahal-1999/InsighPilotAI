"""
InsightPilot AI — Deterministic Recommendation Engine
Generates prioritized, evidence-linked action recommendations based on driver controllability.
"""

from typing import List, Dict, Any, Optional
from analytics.data_loader import DataLoader
from analytics.investigation_engine import InvestigationEngine
from evidence.evidence_engine import EvidenceEngine

class RecommendationEngine:
    """Generates structured, deterministic recommendations mapped from analytical drivers."""

    DRIVER_LEVER_MAP = {
        "atlanta_dc_stockout": {
            "lever": "Inventory Availability / Inter-DC Stock Rebalancing",
            "action": "Execute Emergency Inventory Transfer (20,000 Units from Charlotte Hub to Atlanta DC)",
            "rationale": "Restores Atlanta-DC-01 availability from 72.4% to 90%+, unblocking unallocated wholesale distributor backlog.",
            "owner": "Supply Chain / Operations",
            "controllability": "HIGH",
            "priority": "CRITICAL",
            "priority_rank": 1,
            "confidence_score": 91,
            "margin_impact_pct": 1.2,
            "timeframe_days": 14,
            "recovery_efficiency": 0.88,
            "overlap_group": "FULFILLMENT_RECOVERY",
            "assumptions": [
                "Inter-DC freight from Charlotte to Atlanta can be executed within 72 hours",
                "Unmet distributor demand remains recapturable with zero permanent brand churn",
                "Direct expedited logistics surcharge is capped at $28,000"
            ],
            "constraints": [
                "Atlanta DC receiving dock capacity constraints during morning shift",
                "Minimum safety stock threshold at Charlotte DC must remain above 85%"
            ]
        },
        "distributor_orders": {
            "lever": "Channel Partner Relationship & Order Re-commitment",
            "action": "Targeted Distributor Recovery Outreach (Tier-1 Apex & Mid-Atlantic accounts)",
            "rationale": "Direct executive outreach with delivery guarantees to accelerate the release of 29 deferred POs.",
            "owner": "Regional Sales / Commercial Operations",
            "controllability": "HIGH",
            "priority": "HIGH",
            "priority_rank": 2,
            "confidence_score": 85,
            "margin_impact_pct": 0.6,
            "timeframe_days": 21,
            "recovery_efficiency": 0.75,
            "overlap_group": "CHANNEL_SALES",
            "assumptions": [
                "29 deferred purchase orders can be recaptured upon delivery assurance",
                "Tier-1 distributors accept phased fulfillment commitments"
            ],
            "constraints": [
                "Standard distributor credit lines and payment terms apply"
            ]
        },
        "sku_8821_sales_volume": {
            "lever": "Production Schedule & SKU Line Reallocation",
            "action": "Accelerate SKU-8821 Production Run & Safety Stock Rebalancing",
            "rationale": "Reallocates production lines to SKU-8821 to rebuild safety stock buffer and eliminate backorders.",
            "owner": "Manufacturing & Product Operations",
            "controllability": "MEDIUM",
            "priority": "HIGH",
            "priority_rank": 3,
            "confidence_score": 88,
            "margin_impact_pct": 0.8,
            "timeframe_days": 30,
            "recovery_efficiency": 0.70,
            "overlap_group": "FULFILLMENT_RECOVERY",
            "assumptions": [
                "Plant line 3 conversion to SKU-8821 completed within 5 business days",
                "Raw material component inventory is available at standard BOM cost"
            ],
            "constraints": [
                "Manufacturing line changeover time requires 24-hour maintenance window"
            ]
        },
        "competitor_horizon_pricing": {
            "lever": "Targeted Trade Allowance / Promotional Match",
            "action": "Authorize Temporary 10% Wholesale Trade Allowance on Select High-Volume Accounts",
            "rationale": "Defends market share against Horizon Foods' 15% discount in Mid-Atlantic accounts while preserving gross margin.",
            "owner": "Commercial Strategy & Pricing",
            "controllability": "LOW",
            "priority": "MEDIUM",
            "priority_rank": 4,
            "confidence_score": 84,
            "margin_impact_pct": -0.4,
            "timeframe_days": 45,
            "recovery_efficiency": 0.65,
            "overlap_group": "COMMERCIAL_PRICING",
            "assumptions": [
                "10% allowance matches effective price gap and stabilizes distributor loyalty",
                "Allowance restricted strictly to Mid-Atlantic wholesale accounts to prevent margin leakage"
            ],
            "constraints": [
                "Maximum trade allowance budget capped at $50,000"
            ]
        }
    }

    def __init__(self, data_loader: Optional[DataLoader] = None):
        self.loader = data_loader or DataLoader()
        self.inv_engine = InvestigationEngine(self.loader)
        self.ev_engine = EvidenceEngine(self.loader)

    def generate_recommendations(
        self,
        kpi_id: str = "north_america_east_revenue",
        region: str = "NA-East",
        prev_period_id: str = "2026-Q2",
        curr_period_id: str = "2026-Q3"
    ) -> List[Dict[str, Any]]:
        """Generates deterministic, prioritized recommendations for the specified KPI."""
        inv_result = self.inv_engine.run_investigation(
            kpi_id=kpi_id,
            region=region,
            prev_period_id=prev_period_id,
            curr_period_id=curr_period_id
        )
        drivers = inv_result.get("drivers", [])

        recommendations = []
        for d in drivers:
            driver_id = d["driver_id"]
            if driver_id not in self.DRIVER_LEVER_MAP:
                continue

            config = self.DRIVER_LEVER_MAP[driver_id]
            raw_impact = abs(d.get("impact_usd", 0.0))
            recovery_eff = config["recovery_efficiency"]
            projected_recovery = round(raw_impact * recovery_eff, 2)

            conf_score = config["confidence_score"]
            conf_label = "HIGH" if conf_score >= 80 else ("MEDIUM" if conf_score >= 65 else "LOW")

            # Extract linked evidence IDs
            ev_ids = d.get("evidence_ids", [])

            rec_id = f"REC-2026-NAE-00{config['priority_rank']}"

            recommendations.append({
                "recommendation_id": rec_id,
                "kpi_id": kpi_id,
                "driver_id": driver_id,
                "driver_name": d["driver_name"],
                "controllability": config["controllability"],
                "controllable_lever": config["lever"],
                "action": config["action"],
                "rationale": config["rationale"],
                "expected_impact": {
                    "revenue_recovery_usd": projected_recovery,
                    "margin_impact_pct": config["margin_impact_pct"],
                    "recovery_timeframe_days": config["timeframe_days"]
                },
                "owner": config["owner"],
                "priority": config["priority"],
                "priority_rank": config["priority_rank"],
                "confidence": {
                    "score": conf_score,
                    "label": conf_label
                },
                "supporting_evidence_ids": ev_ids,
                "assumptions": config["assumptions"],
                "constraints": config["constraints"],
                "overlap_group": config["overlap_group"]
            })

        # Sort deterministically by priority rank
        sorted_recs = sorted(recommendations, key=lambda x: x["priority_rank"])
        return sorted_recs

    def get_recommendation_by_id(
        self,
        recommendation_id: str,
        kpi_id: str = "north_america_east_revenue",
        region: str = "NA-East"
    ) -> Optional[Dict[str, Any]]:
        """Returns single recommendation by ID."""
        all_recs = self.generate_recommendations(kpi_id=kpi_id, region=region)
        for r in all_recs:
            if r["recommendation_id"] == recommendation_id:
                return r
        return None
