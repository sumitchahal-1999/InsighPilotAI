"""
InsightPilot AI — Database Seeding Pipeline
Imports raw CSV synthetic datasets and registers initial analytical entities into the database.
"""

import os
import csv
from datetime import datetime
from typing import Dict, Any, List
from sqlalchemy.orm import Session
from backend.app.db.session import engine, SessionLocal, init_db
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
    EvidenceRecordModel,
    RecommendationRecordModel
)
from analytics.config import DATA_RAW_DIR
from analytics.utils import parse_date

def _load_csv(filename: str) -> List[Dict[str, Any]]:
    path = os.path.join(DATA_RAW_DIR, filename)
    if not os.path.exists(path):
        raise FileNotFoundError(f"CSV missing: {path}")
    with open(path, "r", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def seed_raw_data(db: Session) -> Dict[str, int]:
    """Idempotently seeds all 8 raw synthetic enterprise datasets into the database."""
    counts = {}

    # 1. Revenue
    if db.query(RawRevenueRecord).count() == 0:
        rows = _load_csv("revenue.csv")
        records = [
            RawRevenueRecord(
                invoice_id=r["invoice_id"],
                invoice_date=parse_date(r["invoice_date"]),
                region=r["region"],
                territory=r["territory"],
                customer_id=r["customer_id"],
                sku_id=r["sku_id"],
                gross_amount=float(r["gross_amount"]),
                discount_amount=float(r["discount_amount"]),
                net_revenue=float(r["net_revenue"]),
                currency=r["currency"],
                posting_status=r["posting_status"]
            )
            for r in rows
        ]
        db.bulk_save_objects(records)
        db.commit()
        counts["raw_revenue"] = len(records)
    else:
        counts["raw_revenue"] = db.query(RawRevenueRecord).count()

    # 2. Inventory
    if db.query(RawInventoryRecord).count() == 0:
        rows = _load_csv("inventory.csv")
        records = [
            RawInventoryRecord(
                snapshot_id=r["snapshot_id"],
                snapshot_date=parse_date(r["snapshot_date"]),
                dc_location=r["dc_location"],
                region=r["region"],
                sku_id=r["sku_id"],
                on_hand_units=int(r["on_hand_units"]),
                available_units=int(r["available_units"]),
                required_demand_units=int(r["required_demand_units"]),
                availability_percentage=float(r["availability_percentage"]),
                stockout_status=r["stockout_status"].lower() == "true",
                reorder_in_transit_units=int(r["reorder_in_transit_units"])
            )
            for r in rows
        ]
        db.bulk_save_objects(records)
        db.commit()
        counts["raw_inventory"] = len(records)
    else:
        counts["raw_inventory"] = db.query(RawInventoryRecord).count()

    # 3. Margin
    if db.query(RawMarginRecord).count() == 0:
        rows = _load_csv("margin.csv")
        records = [
            RawMarginRecord(
                margin_record_id=r["margin_record_id"],
                fiscal_period=r["fiscal_period"],
                region=r["region"],
                sku_id=r["sku_id"],
                sales_revenue=float(r["sales_revenue"]),
                cogs_material=float(r["cogs_material"]),
                cogs_freight_expedited=float(r["cogs_freight_expedited"]),
                total_cogs=float(r["total_cogs"]),
                gross_profit=float(r["gross_profit"]),
                gross_margin_percentage=float(r["gross_margin_percentage"])
            )
            for r in rows
        ]
        db.bulk_save_objects(records)
        db.commit()
        counts["raw_margin"] = len(records)
    else:
        counts["raw_margin"] = db.query(RawMarginRecord).count()

    # 4. Sales
    if db.query(RawSalesRecord).count() == 0:
        rows = _load_csv("sales.csv")
        records = [
            RawSalesRecord(
                sales_item_id=r["sales_item_id"],
                order_id=r["order_id"],
                transaction_date=parse_date(r["transaction_date"]),
                region=r["region"],
                distributor_id=r["distributor_id"],
                sku_id=r["sku_id"],
                units_ordered=int(r["units_ordered"]),
                units_sold=int(r["units_sold"]),
                unit_price=float(r["unit_price"]),
                total_item_revenue=float(r["total_item_revenue"]),
                delivery_status=r["delivery_status"]
            )
            for r in rows
        ]
        db.bulk_save_objects(records)
        db.commit()
        counts["raw_sales"] = len(records)
    else:
        counts["raw_sales"] = db.query(RawSalesRecord).count()

    # 5. Distributor Orders
    if db.query(RawDistributorOrderRecord).count() == 0:
        rows = _load_csv("distributor_orders.csv")
        records = [
            RawDistributorOrderRecord(
                po_id=r["po_id"],
                order_date=parse_date(r["order_date"]),
                region=r["region"],
                distributor_id=r["distributor_id"],
                distributor_tier=r["distributor_tier"],
                total_order_value=float(r["total_order_value"]),
                order_status=r["order_status"],
                deferral_reason=r.get("deferral_reason"),
                expected_delivery_date=parse_date(r["expected_delivery_date"])
            )
            for r in rows
        ]
        db.bulk_save_objects(records)
        db.commit()
        counts["raw_distributor_orders"] = len(records)
    else:
        counts["raw_distributor_orders"] = db.query(RawDistributorOrderRecord).count()

    # 6. Support Tickets
    if db.query(RawSupportTicketRecord).count() == 0:
        rows = _load_csv("support_tickets.csv")
        records = [
            RawSupportTicketRecord(
                ticket_id=r["ticket_id"],
                created_at=r["created_at"],
                created_date=parse_date(r["created_at"]),
                region=r["region"],
                source_entity=r["source_entity"],
                category=r["category"],
                severity=r["severity"],
                subject=r["subject"],
                content_summary=r["content_summary"],
                sentiment_score=float(r["sentiment_score"])
            )
            for r in rows
        ]
        db.bulk_save_objects(records)
        db.commit()
        counts["raw_support_tickets"] = len(records)
    else:
        counts["raw_support_tickets"] = db.query(RawSupportTicketRecord).count()

    # 7. Distributor Communications
    if db.query(RawDistributorCommunicationRecord).count() == 0:
        rows = _load_csv("distributor_communications.csv")
        records = [
            RawDistributorCommunicationRecord(
                comm_id=r["comm_id"],
                sent_at=r["sent_at"],
                sent_date=parse_date(r["sent_at"]),
                sender=r["sender"],
                recipient=r["recipient"],
                subject=r["subject"],
                key_extracted_claims=r["key_extracted_claims"],
                urgency=r["urgency"]
            )
            for r in rows
        ]
        db.bulk_save_objects(records)
        db.commit()
        counts["raw_distributor_communications"] = len(records)
    else:
        counts["raw_distributor_communications"] = db.query(RawDistributorCommunicationRecord).count()

    # 8. Market Intelligence
    if db.query(RawMarketIntelligenceRecord).count() == 0:
        rows = _load_csv("market_intelligence.csv")
        records = [
            RawMarketIntelligenceRecord(
                report_id=r["report_id"],
                captured_date=parse_date(r["captured_date"]),
                competitor_name=r["competitor_name"],
                competing_product=r["competing_product"],
                target_geography=r["target_geography"],
                promotional_action=r["promotional_action"],
                observed_price_usd=float(r["observed_price_usd"]),
                baseline_price_usd=float(r["baseline_price_usd"]),
                source_channel=r["source_channel"]
            )
            for r in rows
        ]
        db.bulk_save_objects(records)
        db.commit()
        counts["raw_market_intelligence"] = len(records)
    else:
        counts["raw_market_intelligence"] = db.query(RawMarketIntelligenceRecord).count()

    return counts

def seed_kpi_registry(db: Session) -> int:
    """Seeds authoritative KPI metadata registry."""
    kpi_defs = [
        {
            "id": "north_america_east_revenue",
            "name": "North America East Revenue",
            "category": "Finance",
            "formula": "SUM(net_revenue)",
            "unit": "USD",
            "direction": "HIGHER_IS_BETTER",
            "default_period": "2026-Q3",
            "materiality_threshold_pct": 5.0,
            "source_datasets": ["revenue.csv", "sales.csv"]
        },
        {
            "id": "gross_margin",
            "name": "Gross Margin Percentage",
            "category": "Finance",
            "formula": "(SUM(sales_revenue) - SUM(total_cogs)) / SUM(sales_revenue)",
            "unit": "PERCENTAGE",
            "direction": "HIGHER_IS_BETTER",
            "default_period": "2026-Q3",
            "materiality_threshold_pct": 2.0,
            "source_datasets": ["margin.csv"]
        },
        {
            "id": "units_sold",
            "name": "Total Volume Sold",
            "category": "Operations",
            "formula": "SUM(shipped_units)",
            "unit": "COUNT",
            "direction": "HIGHER_IS_BETTER",
            "default_period": "2026-Q3",
            "materiality_threshold_pct": 5.0,
            "source_datasets": ["sales.csv"]
        },
        {
            "id": "distributor_orders",
            "name": "Distributor Orders Placed",
            "category": "Commercial",
            "formula": "COUNT(po_number)",
            "unit": "COUNT",
            "direction": "HIGHER_IS_BETTER",
            "default_period": "2026-Q3",
            "materiality_threshold_pct": 5.0,
            "source_datasets": ["distributor_orders.csv"]
        },
        {
            "id": "inventory_availability",
            "name": "Warehouse Inventory Availability",
            "category": "Supply Chain",
            "formula": "AVG(availability_percentage)",
            "unit": "PERCENTAGE",
            "direction": "HIGHER_IS_BETTER",
            "default_period": "2026-Q3",
            "materiality_threshold_pct": 5.0,
            "source_datasets": ["inventory.csv"]
        }
    ]

    count = 0
    for k in kpi_defs:
        existing = db.query(KPIDefinitionRecord).filter_by(id=k["id"]).first()
        if not existing:
            db.add(KPIDefinitionRecord(**k))
            count += 1
    db.commit()
    return count

def seed_database() -> Dict[str, Any]:
    """Top-level database seeding execution."""
    init_db()
    db = SessionLocal()
    try:
        raw_counts = seed_raw_data(db)
        kpi_count = seed_kpi_registry(db)
        return {
            "status": "success",
            "raw_dataset_rows": raw_counts,
            "kpis_registered": kpi_count
        }
    finally:
        db.close()
