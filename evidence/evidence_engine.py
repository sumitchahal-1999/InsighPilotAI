"""
InsightPilot AI — Evidence & Lineage Engine Orchestrator
Coordinates deterministic evidence retrieval, lineage tagging, ranking, and validation.
"""

from typing import List, Dict, Any, Optional
from evidence.evidence_loader import EvidenceLoader
from evidence.evidence_retriever import EvidenceRetriever
from evidence.evidence_ranker import EvidenceRanker
from evidence.evidence_validator import EvidenceValidator
from evidence.lineage import LineageTracker

class EvidenceEngine:
    """Central engine orchestrating evidence extraction, validation, ranking, and lineage tracing."""
    
    def __init__(self, data_loader: Optional[Any] = None):
        self.loader = EvidenceLoader(data_loader)
        self.retriever = EvidenceRetriever(self.loader)
        self.ranker = EvidenceRanker()
        self.validator = EvidenceValidator(self.loader)
        self.lineage_tracker = LineageTracker()

    def get_evidence_for_driver(self, driver_id: str, region: str = "NA-East", kpi_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Retrieves, validates, and ranks evidence items for a specific driver."""
        if driver_id == "atlanta_dc_stockout":
            raw_items = self.retriever.retrieve_atlanta_stockout_evidence(region)
            table_map = {
                "EVID_ERP_ATL_STOCKOUT_001": "inventory",
                "EVID_ERP_TRANSFER_LOG_002": "margin",
                "EVID_ZENDESK_ATL_DELAY_003": "support_tickets"
            }
        elif driver_id == "sku_8821_sales_volume":
            raw_items = self.retriever.retrieve_sku8821_volume_evidence(region)
            table_map = {
                "EVID_CRM_SKU8821_SALES_004": "sales",
                "EVID_ERP_BOM_MARGIN_005": "margin"
            }
        elif driver_id == "distributor_orders":
            raw_items = self.retriever.retrieve_distributor_orders_evidence(region)
            table_map = {
                "EVID_CRM_PO_DEF_006": "distributor_orders",
                "EVID_COMM_DIST_EMAIL_007": "distributor_communications"
            }
        elif driver_id == "competitor_horizon_pricing":
            raw_items = self.retriever.retrieve_competitor_pricing_evidence(region)
            table_map = {
                "EVID_MKT_HORIZON_PROMO_008": "market_intelligence",
                "EVID_ZENDESK_COMP_FEEDBACK_009": "support_tickets"
            }
        else:
            return []

        # Validate against schema and source record existence
        validated_items = []
        for item in raw_items:
            tbl = table_map.get(item["evidence_id"], "revenue")
            validated = self.validator.validate_evidence_item(item, tbl)
            validated_items.append(validated)

        # Rank evidence items deterministically
        ranked_items = self.ranker.rank_evidence(validated_items)
        return ranked_items

    def get_all_evidence_for_investigation(self, region: str = "NA-East") -> Dict[str, Any]:
        """Retrieves and groups all evidence items across all 4 drivers."""
        driver_ids = [
            "atlanta_dc_stockout",
            "sku_8821_sales_volume",
            "distributor_orders",
            "competitor_horizon_pricing"
        ]
        
        evidence_by_driver = {}
        all_evidence_nodes = []
        sufficiency_reports = {}
        
        for d_id in driver_ids:
            items = self.get_evidence_for_driver(d_id, region)
            evidence_by_driver[d_id] = items
            all_evidence_nodes.extend(items)
            sufficiency_reports[d_id] = self.validator.check_driver_evidence_sufficiency(d_id, items)
            
        return {
            "evidence_by_driver": evidence_by_driver,
            "all_evidence_nodes": all_evidence_nodes,
            "total_evidence_count": len(all_evidence_nodes),
            "sufficiency_status": sufficiency_reports
        }

    def trace_lineage(self, evidence_id: str, region: str = "NA-East") -> Optional[Dict[str, Any]]:
        """Returns the full 5-layer lineage trace for a specific evidence item."""
        all_res = self.get_all_evidence_for_investigation(region)
        for item in all_res["all_evidence_nodes"]:
            if item["evidence_id"] == evidence_id:
                return {
                    "evidence_id": evidence_id,
                    "kpi": item["supports_kpi"],
                    "driver": item["supports_driver"],
                    "source_system": item["source"],
                    "source_domain": item["source_domain"],
                    "source_record_id": item["source_record_id"],
                    "lineage_metadata": item["lineage"],
                    "verification_hash": item["lineage"]["verification_hash"]
                }
        return None
