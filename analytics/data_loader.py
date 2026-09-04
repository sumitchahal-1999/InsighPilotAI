"""
InsightPilot AI — Data Loader Layer
Robust, deterministic data loading from PostgreSQL/SQLite database or enterprise CSV datasets.
"""

import os
import csv
from typing import List, Dict, Any, Optional
from datetime import date
from analytics.config import DATA_RAW_DIR
from analytics.utils import parse_date

class DataLoader:
    """Loads, validates, and indexes enterprise datasets with dual DB/CSV backing."""
    
    def __init__(self, data_dir: str = DATA_RAW_DIR, use_db: bool = True):
        self.data_dir = data_dir
        self.use_db = use_db
        self._revenue: Optional[List[Dict[str, Any]]] = None
        self._inventory: Optional[List[Dict[str, Any]]] = None
        self._margin: Optional[List[Dict[str, Any]]] = None
        self._sales: Optional[List[Dict[str, Any]]] = None
        self._distributor_orders: Optional[List[Dict[str, Any]]] = None
        self._support_tickets: Optional[List[Dict[str, Any]]] = None
        self._distributor_communications: Optional[List[Dict[str, Any]]] = None
        self._market_intelligence: Optional[List[Dict[str, Any]]] = None

        self._repo = None
        if self.use_db:
            try:
                from backend.app.repositories.data_repository import DataRepository
                self._repo = DataRepository()
            except Exception:
                self._repo = None

    def _read_csv(self, filename: str, required_cols: List[str]) -> List[Dict[str, Any]]:
        file_path = os.path.join(self.data_dir, filename)
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Dataset file missing: {file_path}")
        
        records = []
        with open(file_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            if not reader.fieldnames:
                raise ValueError(f"CSV file is empty: {file_path}")
            
            missing = set(required_cols) - set(reader.fieldnames)
            if missing:
                raise ValueError(f"CSV {filename} missing required columns: {missing}")
            
            for row in reader:
                records.append(row)
        return records

    def get_revenue(self) -> List[Dict[str, Any]]:
        """Loads and returns parsed invoiced revenue records."""
        if self._revenue is None:
            if self._repo:
                try:
                    db_records = self._repo.get_revenue()
                    if db_records and len(db_records) > 0:
                        self._revenue = db_records
                        return self._revenue
                except Exception:
                    pass

            raw = self._read_csv("revenue.csv", [
                "invoice_id", "invoice_date", "region", "territory", "customer_id",
                "sku_id", "gross_amount", "discount_amount", "net_revenue", "currency", "posting_status"
            ])
            self._revenue = []
            for r in raw:
                self._revenue.append({
                    "invoice_id": r["invoice_id"],
                    "invoice_date": parse_date(r["invoice_date"]),
                    "region": r["region"],
                    "territory": r["territory"],
                    "customer_id": r["customer_id"],
                    "sku_id": r["sku_id"],
                    "gross_amount": float(r["gross_amount"]),
                    "discount_amount": float(r["discount_amount"]),
                    "net_revenue": float(r["net_revenue"]),
                    "currency": r["currency"],
                    "posting_status": r["posting_status"]
                })
        return self._revenue

    def get_inventory(self) -> List[Dict[str, Any]]:
        """Loads and returns parsed inventory snapshot records."""
        if self._inventory is None:
            if self._repo:
                try:
                    db_records = self._repo.get_inventory()
                    if db_records and len(db_records) > 0:
                        self._inventory = db_records
                        return self._inventory
                except Exception:
                    pass

            raw = self._read_csv("inventory.csv", [
                "snapshot_id", "snapshot_date", "dc_location", "region", "sku_id",
                "on_hand_units", "available_units", "required_demand_units",
                "availability_percentage", "stockout_status", "reorder_in_transit_units"
            ])
            self._inventory = []
            for r in raw:
                self._inventory.append({
                    "snapshot_id": r["snapshot_id"],
                    "snapshot_date": parse_date(r["snapshot_date"]),
                    "dc_location": r["dc_location"],
                    "region": r["region"],
                    "sku_id": r["sku_id"],
                    "on_hand_units": int(r["on_hand_units"]),
                    "available_units": int(r["available_units"]),
                    "required_demand_units": int(r["required_demand_units"]),
                    "availability_percentage": float(r["availability_percentage"]),
                    "stockout_status": r["stockout_status"].lower() == "true",
                    "reorder_in_transit_units": int(r["reorder_in_transit_units"])
                })
        return self._inventory

    def get_margin(self) -> List[Dict[str, Any]]:
        """Loads and returns parsed gross margin analysis records."""
        if self._margin is None:
            if self._repo:
                try:
                    db_records = self._repo.get_margin()
                    if db_records and len(db_records) > 0:
                        self._margin = db_records
                        return self._margin
                except Exception:
                    pass

            raw = self._read_csv("margin.csv", [
                "margin_record_id", "fiscal_period", "region", "sku_id", "sales_revenue",
                "cogs_material", "cogs_freight_expedited", "total_cogs", "gross_profit", "gross_margin_percentage"
            ])
            self._margin = []
            for r in raw:
                self._margin.append({
                    "margin_record_id": r["margin_record_id"],
                    "fiscal_period": r["fiscal_period"],
                    "region": r["region"],
                    "sku_id": r["sku_id"],
                    "sales_revenue": float(r["sales_revenue"]),
                    "cogs_material": float(r["cogs_material"]),
                    "cogs_freight_expedited": float(r["cogs_freight_expedited"]),
                    "total_cogs": float(r["total_cogs"]),
                    "gross_profit": float(r["gross_profit"]),
                    "gross_margin_percentage": float(r["gross_margin_percentage"])
                })
        return self._margin

    def get_sales(self) -> List[Dict[str, Any]]:
        """Loads and returns parsed sales unit delivery line items."""
        if self._sales is None:
            if self._repo:
                try:
                    db_records = self._repo.get_sales()
                    if db_records and len(db_records) > 0:
                        self._sales = db_records
                        return self._sales
                except Exception:
                    pass

            raw = self._read_csv("sales.csv", [
                "sales_item_id", "order_id", "transaction_date", "region", "distributor_id",
                "sku_id", "units_ordered", "units_sold", "unit_price", "total_item_revenue", "delivery_status"
            ])
            self._sales = []
            for r in raw:
                self._sales.append({
                    "sales_item_id": r["sales_item_id"],
                    "order_id": r["order_id"],
                    "transaction_date": parse_date(r["transaction_date"]),
                    "region": r["region"],
                    "distributor_id": r["distributor_id"],
                    "sku_id": r["sku_id"],
                    "units_ordered": int(r["units_ordered"]),
                    "units_sold": int(r["units_sold"]),
                    "unit_price": float(r["unit_price"]),
                    "total_item_revenue": float(r["total_item_revenue"]),
                    "delivery_status": r["delivery_status"]
                })
        return self._sales

    def get_distributor_orders(self) -> List[Dict[str, Any]]:
        """Loads and returns parsed distributor purchase orders."""
        if self._distributor_orders is None:
            if self._repo:
                try:
                    db_records = self._repo.get_distributor_orders()
                    if db_records and len(db_records) > 0:
                        self._distributor_orders = db_records
                        return self._distributor_orders
                except Exception:
                    pass

            raw = self._read_csv("distributor_orders.csv", [
                "po_id", "order_date", "region", "distributor_id", "distributor_tier",
                "total_order_value", "order_status", "deferral_reason", "expected_delivery_date"
            ])
            self._distributor_orders = []
            for r in raw:
                self._distributor_orders.append({
                    "po_id": r["po_id"],
                    "order_date": parse_date(r["order_date"]),
                    "region": r["region"],
                    "distributor_id": r["distributor_id"],
                    "distributor_tier": r["distributor_tier"],
                    "total_order_value": float(r["total_order_value"]),
                    "order_status": r["order_status"],
                    "deferral_reason": r["deferral_reason"],
                    "expected_delivery_date": parse_date(r["expected_delivery_date"])
                })
        return self._distributor_orders

    def get_support_tickets(self) -> List[Dict[str, Any]]:
        """Loads and returns parsed support tickets."""
        if self._support_tickets is None:
            if self._repo:
                try:
                    db_records = self._repo.get_support_tickets()
                    if db_records and len(db_records) > 0:
                        self._support_tickets = db_records
                        return self._support_tickets
                except Exception:
                    pass

            raw = self._read_csv("support_tickets.csv", [
                "ticket_id", "created_at", "region", "source_entity", "category",
                "severity", "subject", "content_summary", "sentiment_score"
            ])
            self._support_tickets = []
            for r in raw:
                self._support_tickets.append({
                    "ticket_id": r["ticket_id"],
                    "created_at": r["created_at"],
                    "created_date": parse_date(r["created_at"]),
                    "region": r["region"],
                    "source_entity": r["source_entity"],
                    "category": r["category"],
                    "severity": r["severity"],
                    "subject": r["subject"],
                    "content_summary": r["content_summary"],
                    "sentiment_score": float(r["sentiment_score"])
                })
        return self._support_tickets

    def get_distributor_communications(self) -> List[Dict[str, Any]]:
        """Loads and returns parsed distributor communication records."""
        if self._distributor_communications is None:
            if self._repo:
                try:
                    db_records = self._repo.get_distributor_communications()
                    if db_records and len(db_records) > 0:
                        self._distributor_communications = db_records
                        return self._distributor_communications
                except Exception:
                    pass

            raw = self._read_csv("distributor_communications.csv", [
                "comm_id", "sent_at", "sender", "recipient", "subject", "key_extracted_claims", "urgency"
            ])
            self._distributor_communications = []
            for r in raw:
                self._distributor_communications.append({
                    "comm_id": r["comm_id"],
                    "sent_at": r["sent_at"],
                    "sent_date": parse_date(r["sent_at"]),
                    "sender": r["sender"],
                    "recipient": r["recipient"],
                    "subject": r["subject"],
                    "key_extracted_claims": r["key_extracted_claims"],
                    "urgency": r["urgency"]
                })
        return self._distributor_communications

    def get_market_intelligence(self) -> List[Dict[str, Any]]:
        """Loads and returns parsed market intelligence records."""
        if self._market_intelligence is None:
            if self._repo:
                try:
                    db_records = self._repo.get_market_intelligence()
                    if db_records and len(db_records) > 0:
                        self._market_intelligence = db_records
                        return self._market_intelligence
                except Exception:
                    pass

            raw = self._read_csv("market_intelligence.csv", [
                "report_id", "captured_date", "competitor_name", "competing_product",
                "target_geography", "promotional_action", "observed_price_usd",
                "baseline_price_usd", "source_channel"
            ])
            self._market_intelligence = []
            for r in raw:
                self._market_intelligence.append({
                    "report_id": r["report_id"],
                    "captured_date": parse_date(r["captured_date"]),
                    "competitor_name": r["competitor_name"],
                    "competing_product": r["competing_product"],
                    "target_geography": r["target_geography"],
                    "promotional_action": r["promotional_action"],
                    "observed_price_usd": float(r["observed_price_usd"]),
                    "baseline_price_usd": float(r["baseline_price_usd"]),
                    "source_channel": r["source_channel"]
                })
        return self._market_intelligence
