"""
InsightPilot AI — Evidence Determinism Unit Tests
Tests that evidence retrieval, hashing, and ranking produce 100% deterministic output.
"""

import unittest
from evidence.evidence_engine import EvidenceEngine

class TestEvidenceDeterminism(unittest.TestCase):
    
    def test_evidence_id_and_content_determinism(self):
        engine1 = EvidenceEngine()
        engine2 = EvidenceEngine()

        res1 = engine1.get_all_evidence_for_investigation("NA-East")
        res2 = engine2.get_all_evidence_for_investigation("NA-East")

        self.assertEqual(res1["total_evidence_count"], res2["total_evidence_count"])

        nodes1 = res1["all_evidence_nodes"]
        nodes2 = res2["all_evidence_nodes"]

        for n1, n2 in zip(nodes1, nodes2):
            self.assertEqual(n1["evidence_id"], n2["evidence_id"])
            self.assertEqual(n1["source_record_id"], n2["source_record_id"])
            self.assertEqual(n1["timestamp"], n2["timestamp"])
            self.assertEqual(n1["analytical_method"], n2["analytical_method"])
            self.assertEqual(n1["confidence"]["score"], n2["confidence"]["score"])
            self.assertEqual(n1["lineage"]["verification_hash"], n2["lineage"]["verification_hash"])
            self.assertEqual(n1.get("ranking_score"), n2.get("ranking_score"))

if __name__ == "__main__":
    unittest.main()
