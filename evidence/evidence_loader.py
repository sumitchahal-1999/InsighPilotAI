"""
InsightPilot AI — Evidence Data Loader & Record Indexer
Provides indexed access to raw enterprise records and canonical representations for hashing.
"""

from typing import Dict, Any, Optional
from analytics.data_loader import DataLoader

class EvidenceLoader:
    """Provides indexed lookups across all raw enterprise datasets."""
    
    def __init__(self, data_loader: Optional[DataLoader] = None):
        self.data_loader = data_loader or DataLoader()
        self._indexed = False
        self._revenue_by_id: Dict[str, Dict[str, Any]] = {}
        self._inventory_by_id: Dict[str, Dict[str, Any]] = {}
        self._margin_by_id: Dict[str, Dict[str, Any]] = {}
        self._sales_by_id: Dict[str, Dict[str, Any]] = {}
        self._orders_by_id: Dict[str, Dict[str, Any]] = {}
        self._tickets_by_id: Dict[str, Dict[str, Any]] = {}
        self._comms_by_id: Dict[str, Dict[str, Any]] = {}
        self._mkt_by_id: Dict[str, Dict[str, Any]] = {}

    def _ensure_indexed(self):
        if not self._indexed:
            for r in self.data_loader.get_revenue():
                self._revenue_by_id[r["invoice_id"]] = r
            for r in self.data_loader.get_inventory():
                self._inventory_by_id[r["snapshot_id"]] = r
            for r in self.data_loader.get_margin():
                self._margin_by_id[r["margin_record_id"]] = r
            for r in self.data_loader.get_sales():
                self._sales_by_id[r["sales_item_id"]] = r
            for r in self.data_loader.get_distributor_orders():
                self._orders_by_id[r["po_id"]] = r
            for r in self.data_loader.get_support_tickets():
                self._tickets_by_id[r["ticket_id"]] = r
            for r in self.data_loader.get_distributor_communications():
                self._comms_by_id[r["comm_id"]] = r
            for r in self.data_loader.get_market_intelligence():
                self._mkt_by_id[r["report_id"]] = r
            self._indexed = True

    def find_record(self, table_name: str, record_id: str) -> Optional[Dict[str, Any]]:
        """Finds raw record by table name and primary identifier."""
        self._ensure_indexed()
        table_map = {
            "revenue": self._revenue_by_id,
            "inventory": self._inventory_by_id,
            "margin": self._margin_by_id,
            "sales": self._sales_by_id,
            "distributor_orders": self._orders_by_id,
            "support_tickets": self._tickets_by_id,
            "distributor_communications": self._comms_by_id,
            "market_intelligence": self._mkt_by_id
        }
        store = table_map.get(table_name)
        if store:
            return store.get(record_id)
        return None

    @property
    def raw_loader(self) -> DataLoader:
        return self.data_loader
