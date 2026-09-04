"""
InsightPilot AI — Data Repository Layer
Type-safe database repository for querying normalized enterprise datasets and analytical entities.
"""

from typing import List, Dict, Any, Optional
from datetime import date
from sqlalchemy.orm import Session
from sqlalchemy import select, func, and_
from backend.app.db.session import SessionLocal
from backend.app.db.models.raw_data import (
    RawRevenueRecord,
    RawInventoryRecord,
    RawMarginRecord,
    RawSalesRecord,
    RawDistributorOrderRecord,
    RawSupportTicketRecord,
    RawDistributorCommunicationRecord,
    RawMarketIntelligenceRecord
)
from backend.app.db.models.analytics import (
    KPIDefinitionRecord,
    InvestigationRecord,
    InvestigationDriverRecord,
    EvidenceRecordModel,
    RecommendationRecordModel,
    SimulationRunRecord
)

class DataRepository:
    """Repository layer accessing PostgreSQL / SQLite tables via SQLAlchemy ORM."""

    def __init__(self, db_session: Optional[Session] = None):
        self._external_session = db_session

    def _get_session(self) -> Session:
        return self._external_session or SessionLocal()

    # 1. Revenue
    def get_revenue(self, region: Optional[str] = None) -> List[Dict[str, Any]]:
        """Queries invoiced revenue records."""
        session = self._get_session()
        try:
            stmt = select(RawRevenueRecord)
            if region:
                stmt = stmt.where(RawRevenueRecord.region == region)
            records = session.scalars(stmt).all()
            return [
                {
                    "invoice_id": r.invoice_id,
                    "invoice_date": r.invoice_date,
                    "region": r.region,
                    "territory": r.territory,
                    "customer_id": r.customer_id,
                    "sku_id": r.sku_id,
                    "gross_amount": r.gross_amount,
                    "discount_amount": r.discount_amount,
                    "net_revenue": r.net_revenue,
                    "currency": r.currency,
                    "posting_status": r.posting_status
                }
                for r in records
            ]
        finally:
            if not self._external_session:
                session.close()

    # 2. Inventory
    def get_inventory(self, region: Optional[str] = None) -> List[Dict[str, Any]]:
        """Queries daily inventory snapshot records."""
        session = self._get_session()
        try:
            stmt = select(RawInventoryRecord)
            if region:
                stmt = stmt.where(RawInventoryRecord.region == region)
            records = session.scalars(stmt).all()
            return [
                {
                    "snapshot_id": r.snapshot_id,
                    "snapshot_date": r.snapshot_date,
                    "dc_location": r.dc_location,
                    "region": r.region,
                    "sku_id": r.sku_id,
                    "on_hand_units": r.on_hand_units,
                    "available_units": r.available_units,
                    "required_demand_units": r.required_demand_units,
                    "availability_percentage": r.availability_percentage,
                    "stockout_status": r.stockout_status,
                    "reorder_in_transit_units": r.reorder_in_transit_units
                }
                for r in records
            ]
        finally:
            if not self._external_session:
                session.close()

    # 3. Margin
    def get_margin(self, region: Optional[str] = None) -> List[Dict[str, Any]]:
        """Queries gross margin analysis records."""
        session = self._get_session()
        try:
            stmt = select(RawMarginRecord)
            if region:
                stmt = stmt.where(RawMarginRecord.region == region)
            records = session.scalars(stmt).all()
            return [
                {
                    "margin_record_id": r.margin_record_id,
                    "fiscal_period": r.fiscal_period,
                    "region": r.region,
                    "sku_id": r.sku_id,
                    "sales_revenue": r.sales_revenue,
                    "cogs_material": r.cogs_material,
                    "cogs_freight_expedited": r.cogs_freight_expedited,
                    "total_cogs": r.total_cogs,
                    "gross_profit": r.gross_profit,
                    "gross_margin_percentage": r.gross_margin_percentage
                }
                for r in records
            ]
        finally:
            if not self._external_session:
                session.close()

    # 4. Sales
    def get_sales(self, region: Optional[str] = None) -> List[Dict[str, Any]]:
        """Queries sales line items."""
        session = self._get_session()
        try:
            stmt = select(RawSalesRecord)
            if region:
                stmt = stmt.where(RawSalesRecord.region == region)
            records = session.scalars(stmt).all()
            return [
                {
                    "sales_item_id": r.sales_item_id,
                    "order_id": r.order_id,
                    "transaction_date": r.transaction_date,
                    "region": r.region,
                    "distributor_id": r.distributor_id,
                    "sku_id": r.sku_id,
                    "units_ordered": r.units_ordered,
                    "units_sold": r.units_sold,
                    "unit_price": r.unit_price,
                    "total_item_revenue": r.total_item_revenue,
                    "delivery_status": r.delivery_status
                }
                for r in records
            ]
        finally:
            if not self._external_session:
                session.close()

    # 5. Distributor Orders
    def get_distributor_orders(self, region: Optional[str] = None) -> List[Dict[str, Any]]:
        """Queries distributor purchase orders."""
        session = self._get_session()
        try:
            stmt = select(RawDistributorOrderRecord)
            if region:
                stmt = stmt.where(RawDistributorOrderRecord.region == region)
            records = session.scalars(stmt).all()
            return [
                {
                    "po_id": r.po_id,
                    "order_date": r.order_date,
                    "region": r.region,
                    "distributor_id": r.distributor_id,
                    "distributor_tier": r.distributor_tier,
                    "total_order_value": r.total_order_value,
                    "order_status": r.order_status,
                    "deferral_reason": r.deferral_reason,
                    "expected_delivery_date": r.expected_delivery_date
                }
                for r in records
            ]
        finally:
            if not self._external_session:
                session.close()

    # 6. Support Tickets
    def get_support_tickets(self, region: Optional[str] = None) -> List[Dict[str, Any]]:
        """Queries support tickets."""
        session = self._get_session()
        try:
            stmt = select(RawSupportTicketRecord)
            if region:
                stmt = stmt.where(RawSupportTicketRecord.region == region)
            records = session.scalars(stmt).all()
            return [
                {
                    "ticket_id": r.ticket_id,
                    "created_at": r.created_at,
                    "created_date": r.created_date,
                    "region": r.region,
                    "source_entity": r.source_entity,
                    "category": r.category,
                    "severity": r.severity,
                    "subject": r.subject,
                    "content_summary": r.content_summary,
                    "sentiment_score": r.sentiment_score
                }
                for r in records
            ]
        finally:
            if not self._external_session:
                session.close()

    # 7. Distributor Communications
    def get_distributor_communications(self) -> List[Dict[str, Any]]:
        """Queries distributor communications."""
        session = self._get_session()
        try:
            records = session.scalars(select(RawDistributorCommunicationRecord)).all()
            return [
                {
                    "comm_id": r.comm_id,
                    "sent_at": r.sent_at,
                    "sent_date": r.sent_date,
                    "sender": r.sender,
                    "recipient": r.recipient,
                    "subject": r.subject,
                    "key_extracted_claims": r.key_extracted_claims,
                    "urgency": r.urgency
                }
                for r in records
            ]
        finally:
            if not self._external_session:
                session.close()

    # 8. Market Intelligence
    def get_market_intelligence(self) -> List[Dict[str, Any]]:
        """Queries market intelligence records."""
        session = self._get_session()
        try:
            records = session.scalars(select(RawMarketIntelligenceRecord)).all()
            return [
                {
                    "report_id": r.report_id,
                    "captured_date": r.captured_date,
                    "competitor_name": r.competitor_name,
                    "competing_product": r.competing_product,
                    "target_geography": r.target_geography,
                    "promotional_action": r.promotional_action,
                    "observed_price_usd": r.observed_price_usd,
                    "baseline_price_usd": r.baseline_price_usd,
                    "source_channel": r.source_channel
                }
                for r in records
            ]
        finally:
            if not self._external_session:
                session.close()

    # 9. KPI Registry
    def get_kpis(self) -> List[Dict[str, Any]]:
        """Queries registered KPI definitions."""
        session = self._get_session()
        try:
            records = session.scalars(select(KPIDefinitionRecord)).all()
            return [r.to_dict() for r in records]
        finally:
            if not self._external_session:
                session.close()
