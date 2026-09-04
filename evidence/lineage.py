"""
InsightPilot AI — Lineage Tracker & Cryptographic Audit Verification
Builds deterministic lineage graphs and source record verification hashes.
"""

import hashlib
import json
from typing import Dict, Any

class LineageTracker:
    """Computes deterministic verification hashes and builds 5-layer lineage pathways."""
    
    TABLE_PIPELINE_MAP = {
        "inventory": ("sap_mm_inventory_snapshots", "JOB_ERP_STOCK_FEED_20260815_01"),
        "sales": ("salesforce_order_items", "JOB_CRM_SALES_FULFILLMENT_02"),
        "margin": ("sap_copa_margin_ledger", "JOB_ERP_COPA_MARGIN_03"),
        "distributor_orders": ("salesforce_purchase_orders", "JOB_CRM_CHANNEL_ORDERS_04"),
        "support_tickets": ("zendesk_service_tickets", "JOB_SUPPORT_ESCALATIONS_05"),
        "distributor_communications": ("exchange_distributor_comms", "JOB_COMM_INTELLIGENCE_06"),
        "market_intelligence": ("market_price_scraper_feed", "JOB_MKT_INTEL_SCRAPER_07"),
        "revenue": ("sap_fico_invoiced_sales", "JOB_ERP_REVENUE_INVOICES_08")
    }

    @staticmethod
    def compute_verification_hash(source_record: Dict[str, Any]) -> str:
        """Computes deterministic SHA-256 hash of canonical sorted JSON record."""
        # Convert date objects to string for JSON serialization
        clean_dict = {}
        for k, v in sorted(source_record.items()):
            if hasattr(v, "isoformat"):
                clean_dict[k] = v.isoformat()
            else:
                clean_dict[k] = v
        canonical_bytes = json.dumps(clean_dict, sort_keys=True).encode("utf-8")
        digest = hashlib.sha256(canonical_bytes).hexdigest()
        return f"sha256:{digest}"

    def build_lineage(
        self,
        table_name: str,
        source_record_id: str,
        source_record: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Constructs the lineage node metadata conforming to evidence_contract.json."""
        table_entry = self.TABLE_PIPELINE_MAP.get(
            table_name,
            (f"raw_{table_name}", "JOB_GENERIC_INGESTION_01")
        )
        source_table, pipeline_job = table_entry
        verification_hash = self.compute_verification_hash(source_record)
        
        return {
            "source_table": source_table,
            "pipeline_job_id": pipeline_job,
            "verification_hash": verification_hash
        }
