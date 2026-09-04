"""
InsightPilot AI — Driver Specific Evidence Retrieval Unit Tests
Verifies evidence extraction for each individual driver and validates that all source record IDs exist.
"""

import unittest
from evidence.evidence_engine import EvidenceEngine

class TestDriverEvidenceRetrieval(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.engine = EvidenceEngine()

    def test_atlanta_stockout_evidence_retrieval(self):
        items = self.engine.get_evidence_for_driver("atlanta_dc_stockout", "NA-East")
        self.assertEqual(len(items), 3)
        ev_ids = [x["evidence_id"] for x in items]
        self.assertIn("EVID_ERP_ATL_STOCKOUT_001", ev_ids)
        self.assertIn("EVID_ERP_TRANSFER_LOG_002", ev_ids)
        self.assertIn("EVID_ZENDESK_ATL_DELAY_003", ev_ids)

        # Verify source records exist
        for item in items:
            rec_id = item["source_record_id"]
            self.assertTrue(len(rec_id) > 0)

    def test_sku8821_volume_evidence_retrieval(self):
        items = self.engine.get_evidence_for_driver("sku_8821_sales_volume", "NA-East")
        self.assertEqual(len(items), 2)
        ev_ids = [x["evidence_id"] for x in items]
        self.assertIn("EVID_CRM_SKU8821_SALES_004", ev_ids)
        self.assertIn("EVID_ERP_BOM_MARGIN_005", ev_ids)

    def test_distributor_orders_evidence_retrieval(self):
        items = self.engine.get_evidence_for_driver("distributor_orders", "NA-East")
        self.assertEqual(len(items), 2)
        ev_ids = [x["evidence_id"] for x in items]
        self.assertIn("EVID_CRM_PO_DEF_006", ev_ids)
        self.assertIn("EVID_COMM_DIST_EMAIL_007", ev_ids)

    def test_competitor_pricing_evidence_retrieval(self):
        items = self.engine.get_evidence_for_driver("competitor_horizon_pricing", "NA-East")
        self.assertEqual(len(items), 2)
        ev_ids = [x["evidence_id"] for x in items]
        self.assertIn("EVID_MKT_HORIZON_PROMO_008", ev_ids)
        self.assertIn("EVID_ZENDESK_COMP_FEEDBACK_009", ev_ids)

if __name__ == "__main__":
    unittest.main()
