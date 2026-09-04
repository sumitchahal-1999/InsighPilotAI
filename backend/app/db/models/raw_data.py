"""
InsightPilot AI — Raw Enterprise Dataset Models
SQLAlchemy ORM models representing the 8 normalized synthetic enterprise datasets with exact column mapping.
"""

from datetime import date
from typing import Optional
from sqlalchemy import String, Float, Integer, Date, Boolean, Text, Index
from sqlalchemy.orm import Mapped, mapped_column
from backend.app.db.base import Base

class RawRevenueRecord(Base):
    """Normalized invoiced revenue transactions table."""
    __tablename__ = "raw_revenue"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    invoice_id: Mapped[str] = mapped_column(String(64), unique=True, index=True, nullable=False)
    invoice_date: Mapped[date] = mapped_column(Date, index=True, nullable=False)
    region: Mapped[str] = mapped_column(String(32), index=True, nullable=False)
    territory: Mapped[str] = mapped_column(String(32), nullable=False)
    customer_id: Mapped[str] = mapped_column(String(64), index=True, nullable=False)
    sku_id: Mapped[str] = mapped_column(String(64), index=True, nullable=False)
    gross_amount: Mapped[float] = mapped_column(Float, nullable=False)
    discount_amount: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    net_revenue: Mapped[float] = mapped_column(Float, nullable=False)
    currency: Mapped[str] = mapped_column(String(8), default="USD", nullable=False)
    posting_status: Mapped[str] = mapped_column(String(32), default="POSTED", nullable=False)

    __table_args__ = (
        Index("ix_revenue_region_date", "region", "invoice_date"),
    )

class RawInventoryRecord(Base):
    """Daily warehouse inventory snapshots table."""
    __tablename__ = "raw_inventory"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    snapshot_id: Mapped[str] = mapped_column(String(64), unique=True, index=True, nullable=False)
    snapshot_date: Mapped[date] = mapped_column(Date, index=True, nullable=False)
    dc_location: Mapped[str] = mapped_column(String(64), index=True, nullable=False)
    region: Mapped[str] = mapped_column(String(32), index=True, nullable=False)
    sku_id: Mapped[str] = mapped_column(String(64), index=True, nullable=False)
    on_hand_units: Mapped[int] = mapped_column(Integer, nullable=False)
    available_units: Mapped[int] = mapped_column(Integer, nullable=False)
    required_demand_units: Mapped[int] = mapped_column(Integer, nullable=False)
    availability_percentage: Mapped[float] = mapped_column(Float, nullable=False)
    stockout_status: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    reorder_in_transit_units: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    __table_args__ = (
        Index("ix_inventory_location_sku_date", "dc_location", "sku_id", "snapshot_date"),
    )

class RawMarginRecord(Base):
    """Gross margin profitability analysis records table."""
    __tablename__ = "raw_margin"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    margin_record_id: Mapped[str] = mapped_column(String(64), unique=True, index=True, nullable=False)
    fiscal_period: Mapped[str] = mapped_column(String(16), index=True, nullable=False)
    region: Mapped[str] = mapped_column(String(32), index=True, nullable=False)
    sku_id: Mapped[str] = mapped_column(String(64), index=True, nullable=False)
    sales_revenue: Mapped[float] = mapped_column(Float, nullable=False)
    cogs_material: Mapped[float] = mapped_column(Float, nullable=False)
    cogs_freight_expedited: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    total_cogs: Mapped[float] = mapped_column(Float, nullable=False)
    gross_profit: Mapped[float] = mapped_column(Float, nullable=False)
    gross_margin_percentage: Mapped[float] = mapped_column(Float, nullable=False)

class RawSalesRecord(Base):
    """Commercial sales unit delivery line items table."""
    __tablename__ = "raw_sales"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    sales_item_id: Mapped[str] = mapped_column(String(64), unique=True, index=True, nullable=False)
    order_id: Mapped[str] = mapped_column(String(64), index=True, nullable=False)
    transaction_date: Mapped[date] = mapped_column(Date, index=True, nullable=False)
    region: Mapped[str] = mapped_column(String(32), index=True, nullable=False)
    distributor_id: Mapped[str] = mapped_column(String(64), index=True, nullable=False)
    sku_id: Mapped[str] = mapped_column(String(64), index=True, nullable=False)
    units_ordered: Mapped[int] = mapped_column(Integer, nullable=False)
    units_sold: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_price: Mapped[float] = mapped_column(Float, nullable=False)
    total_item_revenue: Mapped[float] = mapped_column(Float, nullable=False)
    delivery_status: Mapped[str] = mapped_column(String(32), default="DELIVERED", nullable=False)

class RawDistributorOrderRecord(Base):
    """B2B distributor purchase orders table."""
    __tablename__ = "raw_distributor_orders"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    po_id: Mapped[str] = mapped_column(String(64), unique=True, index=True, nullable=False)
    order_date: Mapped[date] = mapped_column(Date, index=True, nullable=False)
    region: Mapped[str] = mapped_column(String(32), index=True, nullable=False)
    distributor_id: Mapped[str] = mapped_column(String(64), index=True, nullable=False)
    distributor_tier: Mapped[str] = mapped_column(String(16), default="Tier-1", nullable=False)
    total_order_value: Mapped[float] = mapped_column(Float, nullable=False)
    order_status: Mapped[str] = mapped_column(String(32), index=True, nullable=False)
    deferral_reason: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    expected_delivery_date: Mapped[date] = mapped_column(Date, nullable=False)

class RawSupportTicketRecord(Base):
    """Customer service and partner escalation tickets table."""
    __tablename__ = "raw_support_tickets"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    ticket_id: Mapped[str] = mapped_column(String(64), unique=True, index=True, nullable=False)
    created_at: Mapped[str] = mapped_column(String(64), nullable=False)
    created_date: Mapped[date] = mapped_column(Date, index=True, nullable=False)
    region: Mapped[str] = mapped_column(String(32), index=True, nullable=False)
    source_entity: Mapped[str] = mapped_column(String(64), nullable=False)
    category: Mapped[str] = mapped_column(String(64), index=True, nullable=False)
    severity: Mapped[str] = mapped_column(String(32), default="MEDIUM", nullable=False)
    subject: Mapped[str] = mapped_column(String(255), nullable=False)
    content_summary: Mapped[str] = mapped_column(Text, nullable=False)
    sentiment_score: Mapped[float] = mapped_column(Float, nullable=False)

class RawDistributorCommunicationRecord(Base):
    """Distributor correspondence and contract communication table."""
    __tablename__ = "raw_distributor_communications"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    comm_id: Mapped[str] = mapped_column(String(64), unique=True, index=True, nullable=False)
    sent_at: Mapped[str] = mapped_column(String(64), nullable=False)
    sent_date: Mapped[date] = mapped_column(Date, index=True, nullable=False)
    sender: Mapped[str] = mapped_column(String(128), nullable=False)
    recipient: Mapped[str] = mapped_column(String(128), nullable=False)
    subject: Mapped[str] = mapped_column(String(255), nullable=False)
    key_extracted_claims: Mapped[str] = mapped_column(Text, nullable=False)
    urgency: Mapped[str] = mapped_column(String(32), default="MEDIUM", nullable=False)

class RawMarketIntelligenceRecord(Base):
    """Competitor pricing and syndicated market intelligence table."""
    __tablename__ = "raw_market_intelligence"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    report_id: Mapped[str] = mapped_column(String(64), unique=True, index=True, nullable=False)
    captured_date: Mapped[date] = mapped_column(Date, index=True, nullable=False)
    competitor_name: Mapped[str] = mapped_column(String(64), index=True, nullable=False)
    competing_product: Mapped[str] = mapped_column(String(64), nullable=False)
    target_geography: Mapped[str] = mapped_column(String(32), index=True, nullable=False)
    promotional_action: Mapped[str] = mapped_column(String(255), nullable=False)
    observed_price_usd: Mapped[float] = mapped_column(Float, nullable=False)
    baseline_price_usd: Mapped[float] = mapped_column(Float, nullable=False)
    source_channel: Mapped[str] = mapped_column(String(64), nullable=False)
