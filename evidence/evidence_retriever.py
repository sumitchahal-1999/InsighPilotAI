"""
InsightPilot AI — Deterministic Evidence Retriever
Extracts verifiable evidence records from raw enterprise datasets for each analytical driver.
"""

from typing import List, Dict, Any, Optional
from datetime import date
from evidence.evidence_loader import EvidenceLoader
from evidence.lineage import LineageTracker

class EvidenceRetriever:
    """Retrieves and structures evidence records for all four analytical drivers."""
    
    def __init__(self, loader: Optional[EvidenceLoader] = None):
        self.loader = loader or EvidenceLoader()
        self.lineage = LineageTracker()

    def _calculate_freshness(self, record_date: date) -> Dict[str, Any]:
        """Calculates freshness metadata relative to Q3 2026 reporting baseline (2026-09-30)."""
        baseline_date = date(2026, 9, 30)
        days_diff = max(0, (baseline_date - record_date).days)
        hours_diff = float(days_diff * 24)
        
        # Categorize freshness status according to contract
        if days_diff <= 14:
            status = "LIVE"
        elif days_diff <= 60:
            status = "RECENT"
        else:
            status = "STALE"
            
        return {
            "age_hours": round(hours_diff, 1),
            "status": status
        }

    # -------------------------------------------------------------------------
    # 1. Atlanta DC Stockout Evidence
    # -------------------------------------------------------------------------
    def retrieve_atlanta_stockout_evidence(self, region: str = "NA-East") -> List[Dict[str, Any]]:
        """Retrieves ERP inventory snapshots, COGS freight allocations, and support escalations."""
        evidence_items = []
        raw_inventory = self.loader.raw_loader.get_inventory()
        raw_margin = self.loader.raw_loader.get_margin()
        raw_tickets = self.loader.raw_loader.get_support_tickets()

        # Evidence Node 1: Direct DC Inventory Snapshot showing stockout
        atl_snaps = [
            r for r in raw_inventory
            if r["dc_location"] == "Atlanta-DC-01" and r["sku_id"] == "SKU-8821"
            and date(2026, 8, 1) <= r["snapshot_date"] <= date(2026, 8, 19)
        ]
        if atl_snaps:
            best_snap = min(atl_snaps, key=lambda x: x["availability_percentage"])
            snap_date = best_snap["snapshot_date"]
            source_rec_id = best_snap["snapshot_id"]
            lineage_info = self.lineage.build_lineage("inventory", source_rec_id, best_snap)
            
            evidence_items.append({
                "evidence_id": "EVID_ERP_ATL_STOCKOUT_001",
                "source": "SAP S/4HANA Supply Chain Logistics (MM-WM)",
                "source_record_id": source_rec_id,
                "source_domain": "ERP",
                "timestamp": f"{snap_date.isoformat()}T06:00:00Z",
                "freshness": self._calculate_freshness(snap_date),
                "evidence_type": "TELEMETRY_LOG",
                "analytical_method": "DC Stockout Duration & Demand Gap Analysis",
                "finding_summary": f"Atlanta-DC-01 inventory availability dropped to {best_snap['availability_percentage']:.1f}% for SKU-8821 with {best_snap['available_units']:,} available vs {best_snap['required_demand_units']:,} required demand.",
                "contribution": {"percentage": 43.2, "monetary_impact_usd": -550000.0},
                "confidence": {"score": 94, "label": "HIGH"},
                "supports_driver": "atlanta_dc_stockout",
                "supports_kpi": "north_america_east_revenue",
                "lineage": lineage_info
            })

        # Evidence Node 2: Emergency Inter-DC Freight Surcharge
        margin_recs = [
            m for m in raw_margin
            if m["region"] == region and m["sku_id"] == "SKU-8821" and m["fiscal_period"] == "2026-Q3"
        ]
        if margin_recs:
            mrg = margin_recs[0]
            source_rec_id = mrg["margin_record_id"]
            lineage_info = self.lineage.build_lineage("margin", source_rec_id, mrg)
            
            evidence_items.append({
                "evidence_id": "EVID_ERP_TRANSFER_LOG_002",
                "source": "SAP COPA Margin & Profitability Ledger",
                "source_record_id": source_rec_id,
                "source_domain": "ERP",
                "timestamp": "2026-08-18T18:00:00Z",
                "freshness": self._calculate_freshness(date(2026, 8, 18)),
                "evidence_type": "TRANSACTION_RECORD",
                "analytical_method": "Expedited Logistics Variance Allocation",
                "finding_summary": f"Emergency freight surcharges increased to ${mrg['cogs_freight_expedited']:,.2f} for SKU-8821 due to expedited inter-DC transfers from Charlotte to Atlanta.",
                "contribution": {"percentage": 43.2, "monetary_impact_usd": -550000.0},
                "confidence": {"score": 92, "label": "HIGH"},
                "supports_driver": "atlanta_dc_stockout",
                "supports_kpi": "north_america_east_revenue",
                "lineage": lineage_info
            })

        # Evidence Node 3: Zendesk Escalation Ticket regarding Stockout Delay
        stockout_tickets = [
            t for t in raw_tickets
            if t["region"] == region and t["category"] == "STOCKOUT_COMPLAINT"
            and date(2026, 8, 1) <= t["created_date"] <= date(2026, 8, 19)
        ]
        if stockout_tickets:
            best_ticket = stockout_tickets[0]
            source_rec_id = best_ticket["ticket_id"]
            lineage_info = self.lineage.build_lineage("support_tickets", source_rec_id, best_ticket)
            
            evidence_items.append({
                "evidence_id": "EVID_ZENDESK_ATL_DELAY_003",
                "source": "Zendesk Customer Service Desk",
                "source_record_id": source_rec_id,
                "source_domain": "SUPPORT_MARKET_INTEL",
                "timestamp": best_ticket["created_at"],
                "freshness": self._calculate_freshness(best_ticket["created_date"]),
                "evidence_type": "CUSTOMER_SIGNAL",
                "analytical_method": "NLP Complaint Cluster & Sentiment Extraction",
                "finding_summary": f"Distributor {best_ticket['source_entity']} logged severity {best_ticket['severity']} ticket: '{best_ticket['subject']}' with negative sentiment {best_ticket['sentiment_score']}.",
                "contribution": {"percentage": 43.2, "monetary_impact_usd": -550000.0},
                "confidence": {"score": 90, "label": "HIGH"},
                "supports_driver": "atlanta_dc_stockout",
                "supports_kpi": "north_america_east_revenue",
                "lineage": lineage_info
            })

        return evidence_items

    # -------------------------------------------------------------------------
    # 2. SKU-8821 Sales Volume Evidence
    # -------------------------------------------------------------------------
    def retrieve_sku8821_volume_evidence(self, region: str = "NA-East") -> List[Dict[str, Any]]:
        """Retrieves CRM sales delivery deficit line items and product margin records."""
        evidence_items = []
        raw_sales = self.loader.raw_loader.get_sales()
        raw_margin = self.loader.raw_loader.get_margin()

        # Evidence Node 1: CRM Sales Backorder / Partial Delivery Item
        backordered_sales = [
            s for s in raw_sales
            if s["region"] == region and s["sku_id"] == "SKU-8821" and s["delivery_status"] in ("PARTIAL", "BACKORDERED")
            and date(2026, 8, 1) <= s["transaction_date"] <= date(2026, 8, 20)
        ]
        if backordered_sales:
            sample_sale = backordered_sales[0]
            source_rec_id = sample_sale["sales_item_id"]
            lineage_info = self.lineage.build_lineage("sales", source_rec_id, sample_sale)
            
            evidence_items.append({
                "evidence_id": "EVID_CRM_SKU8821_SALES_004",
                "source": "Salesforce Sales Cloud Fulfillment Ledger",
                "source_record_id": source_rec_id,
                "source_domain": "CRM_SALES",
                "timestamp": f"{sample_sale['transaction_date'].isoformat()}T14:30:00Z",
                "freshness": self._calculate_freshness(sample_sale["transaction_date"]),
                "evidence_type": "TRANSACTION_RECORD",
                "analytical_method": "Order Fulfillment Line Item Audit",
                "finding_summary": f"Order item {sample_sale['order_id']} for {sample_sale['distributor_id']} experienced {sample_sale['delivery_status']} delivery ({sample_sale['units_sold']} delivered of {sample_sale['units_ordered']} ordered).",
                "contribution": {"percentage": 26.7, "monetary_impact_usd": -340000.0},
                "confidence": {"score": 89, "label": "HIGH"},
                "supports_driver": "sku_8821_sales_volume",
                "supports_kpi": "north_america_east_revenue",
                "lineage": lineage_info
            })

        # Evidence Node 2: Product Margin Compression Record
        sku_margins = [
            m for m in raw_margin
            if m["region"] == region and m["sku_id"] == "SKU-8821" and m["fiscal_period"] == "2026-Q3"
        ]
        if sku_margins:
            mrg = sku_margins[0]
            source_rec_id = mrg["margin_record_id"]
            lineage_info = self.lineage.build_lineage("margin", source_rec_id, mrg)
            
            evidence_items.append({
                "evidence_id": "EVID_ERP_BOM_MARGIN_005",
                "source": "SAP COPA Profitability Analysis",
                "source_record_id": source_rec_id,
                "source_domain": "ERP",
                "timestamp": "2026-09-30T23:59:59Z",
                "freshness": self._calculate_freshness(date(2026, 9, 30)),
                "evidence_type": "TRANSACTION_RECORD",
                "analytical_method": "Product Gross Margin Contribution Decomposition",
                "finding_summary": f"SKU-8821 recognized revenue dropped to ${mrg['sales_revenue']:,.2f} with margin compressing to {mrg['gross_margin_percentage']:.1f}%.",
                "contribution": {"percentage": 26.7, "monetary_impact_usd": -340000.0},
                "confidence": {"score": 88, "label": "HIGH"},
                "supports_driver": "sku_8821_sales_volume",
                "supports_kpi": "north_america_east_revenue",
                "lineage": lineage_info
            })

        return evidence_items

    # -------------------------------------------------------------------------
    # 3. Distributor Orders Evidence
    # -------------------------------------------------------------------------
    def retrieve_distributor_orders_evidence(self, region: str = "NA-East") -> List[Dict[str, Any]]:
        """Retrieves deferred purchase orders and distributor communication thread extracts."""
        evidence_items = []
        raw_orders = self.loader.raw_loader.get_distributor_orders()
        raw_comms = self.loader.raw_loader.get_distributor_communications()

        # Evidence Node 1: CRM Purchase Order Deferral
        deferred_pos = [
            o for o in raw_orders
            if o["region"] == region and o["order_status"] == "DEFERRED"
        ]
        if deferred_pos:
            sample_po = deferred_pos[0]
            source_rec_id = sample_po["po_id"]
            lineage_info = self.lineage.build_lineage("distributor_orders", source_rec_id, sample_po)
            
            evidence_items.append({
                "evidence_id": "EVID_CRM_PO_DEF_006",
                "source": "Salesforce Partner Portal & PO Management",
                "source_record_id": source_rec_id,
                "source_domain": "CRM_SALES",
                "timestamp": f"{sample_po['order_date'].isoformat()}T11:15:00Z",
                "freshness": self._calculate_freshness(sample_po["order_date"]),
                "evidence_type": "TRANSACTION_RECORD",
                "analytical_method": "Wholesale PO Lifecycle Tracking",
                "finding_summary": f"Purchase order {sample_po['po_id']} (${sample_po['total_order_value']:,.2f}) for Tier-1 distributor {sample_po['distributor_id']} marked DEFERRED: '{sample_po['deferral_reason']}'.",
                "contribution": {"percentage": 18.8, "monetary_impact_usd": -240000.0},
                "confidence": {"score": 85, "label": "HIGH"},
                "supports_driver": "distributor_orders",
                "supports_kpi": "north_america_east_revenue",
                "lineage": lineage_info
            })

        # Evidence Node 2: Executive Distributor Email Notice
        apex_comms = [
            c for c in raw_comms
            if "procurement@apexdistributors.com" in c["sender"] or "orders@midatlanticsupply.com" in c["sender"]
        ]
        if apex_comms:
            sample_comm = apex_comms[0]
            source_rec_id = sample_comm["comm_id"]
            lineage_info = self.lineage.build_lineage("distributor_communications", source_rec_id, sample_comm)
            
            evidence_items.append({
                "evidence_id": "EVID_COMM_DIST_EMAIL_007",
                "source": "Enterprise Email Ingestion Pipeline",
                "source_record_id": source_rec_id,
                "source_domain": "SUPPORT_MARKET_INTEL",
                "timestamp": sample_comm["sent_at"],
                "freshness": self._calculate_freshness(sample_comm["sent_date"]),
                "evidence_type": "COMMUNICATION_EXTRACT",
                "analytical_method": "Structured Communication NLP Extraction",
                "finding_summary": f"Distributor email from {sample_comm['sender']}: '{sample_comm['subject']}' with key claims: '{sample_comm['key_extracted_claims']}'.",
                "contribution": {"percentage": 18.8, "monetary_impact_usd": -240000.0},
                "confidence": {"score": 84, "label": "HIGH"},
                "supports_driver": "distributor_orders",
                "supports_kpi": "north_america_east_revenue",
                "lineage": lineage_info
            })

        return evidence_items

    # -------------------------------------------------------------------------
    # 4. Horizon Foods Competitor Pricing Evidence
    # -------------------------------------------------------------------------
    def retrieve_competitor_pricing_evidence(self, region: str = "NA-East") -> List[Dict[str, Any]]:
        """Retrieves market intelligence pricing observations and customer feedback."""
        evidence_items = []
        raw_mkt = self.loader.raw_loader.get_market_intelligence()
        raw_tickets = self.loader.raw_loader.get_support_tickets()

        # Evidence Node 1: Market Intelligence Scraped Price Observation
        horizon_mkts = [
            m for m in raw_mkt
            if "Horizon Foods" in m["competitor_name"] and m["observed_price_usd"] <= 105.0
        ]
        if horizon_mkts:
            sample_mkt = horizon_mkts[0]
            source_rec_id = sample_mkt["report_id"]
            lineage_info = self.lineage.build_lineage("market_intelligence", source_rec_id, sample_mkt)
            
            evidence_items.append({
                "evidence_id": "EVID_MKT_HORIZON_PROMO_008",
                "source": "Wholesale Market Pricing Intelligence Feed",
                "source_record_id": source_rec_id,
                "source_domain": "SUPPORT_MARKET_INTEL",
                "timestamp": f"{sample_mkt['captured_date'].isoformat()}T09:00:00Z",
                "freshness": self._calculate_freshness(sample_mkt["captured_date"]),
                "evidence_type": "MARKET_OBSERVATION",
                "analytical_method": "Competitive Price Scraping & Parity Indexing",
                "finding_summary": f"Observed 15% price promotion on {sample_mkt['competing_product']} (${sample_mkt['observed_price_usd']:.2f} vs list ${sample_mkt['baseline_price_usd']:.2f}) across {sample_mkt['target_geography']}.",
                "contribution": {"percentage": 11.3, "monetary_impact_usd": -144000.0},
                "confidence": {"score": 78, "label": "MEDIUM"},
                "supports_driver": "competitor_horizon_pricing",
                "supports_kpi": "north_america_east_revenue",
                "lineage": lineage_info
            })

        # Evidence Node 2: Zendesk Price Dispute Support Ticket
        price_tickets = [
            t for t in raw_tickets
            if t["region"] == region and t["category"] == "PRICE_DISPUTE"
        ]
        if price_tickets:
            sample_ticket = price_tickets[0]
            source_rec_id = sample_ticket["ticket_id"]
            lineage_info = self.lineage.build_lineage("support_tickets", source_rec_id, sample_ticket)
            
            evidence_items.append({
                "evidence_id": "EVID_ZENDESK_COMP_FEEDBACK_009",
                "source": "Zendesk Customer Service Desk",
                "source_record_id": source_rec_id,
                "source_domain": "SUPPORT_MARKET_INTEL",
                "timestamp": sample_ticket["created_at"],
                "freshness": self._calculate_freshness(sample_ticket["created_date"]),
                "evidence_type": "CUSTOMER_SIGNAL",
                "analytical_method": "Price Escalation Feedback Mining",
                "finding_summary": f"Price matching request logged by {sample_ticket['source_entity']}: '{sample_ticket['subject']}'.",
                "contribution": {"percentage": 11.3, "monetary_impact_usd": -144000.0},
                "confidence": {"score": 76, "label": "MEDIUM"},
                "supports_driver": "competitor_horizon_pricing",
                "supports_kpi": "north_america_east_revenue",
                "lineage": lineage_info
            })

        return evidence_items
