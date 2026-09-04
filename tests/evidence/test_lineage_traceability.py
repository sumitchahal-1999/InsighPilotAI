"""
InsightPilot AI — Lineage Traceability & Hashing Unit Tests
Tests 5-layer lineage path resolution and deterministic cryptographic verification hashing.
"""

import unittest
from evidence.evidence_engine import EvidenceEngine
from evidence.lineage import LineageTracker

class TestLineageTraceability(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.engine = EvidenceEngine()
        cls.lineage = LineageTracker()

    def test_deterministic_verification_hash(self):
        rec1 = {"id": "REC_01", "val": 100.5, "flag": True}
        rec2 = {"flag": True, "id": "REC_01", "val": 100.5}

        h1 = self.lineage.compute_verification_hash(rec1)
        h2 = self.lineage.compute_verification_hash(rec2)

        self.assertEqual(h1, h2)
        self.assertTrue(h1.startswith("sha256:"))

    def test_lineage_trace_resolution(self):
        trace = self.engine.trace_lineage("EVID_ERP_ATL_STOCKOUT_001", "NA-East")
        self.assertIsNotNone(trace)
        self.assertEqual(trace["evidence_id"], "EVID_ERP_ATL_STOCKOUT_001")
        self.assertEqual(trace["kpi"], "north_america_east_revenue")
        self.assertEqual(trace["driver"], "atlanta_dc_stockout")
        self.assertEqual(trace["source_domain"], "ERP")
        self.assertTrue(len(trace["source_record_id"]) > 0)
        self.assertTrue(trace["verification_hash"].startswith("sha256:"))

    def test_invalid_evidence_id_trace(self):
        trace = self.engine.trace_lineage("EVID_NON_EXISTENT", "NA-East")
        self.assertIsNone(trace)

if __name__ == "__main__":
    unittest.main()
