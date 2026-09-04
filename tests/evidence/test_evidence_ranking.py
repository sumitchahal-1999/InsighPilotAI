"""
InsightPilot AI — Evidence Ranking Unit Tests
Tests ranking score calculations and sorting determinism across evidence types.
"""

import unittest
from evidence.evidence_ranker import EvidenceRanker

class TestEvidenceRanking(unittest.TestCase):
    
    def setUp(self):
        self.ranker = EvidenceRanker()

    def test_ranking_score_calculation(self):
        item_telemetry = {
            "evidence_id": "EV_01",
            "evidence_type": "TELEMETRY_LOG",
            "freshness": {"status": "LIVE"},
            "confidence": {"score": 95}
        }
        score = self.ranker.score_evidence(item_telemetry)
        self.assertGreaterEqual(score, 90.0)

    def test_ranking_order_priority(self):
        items = [
            {
                "evidence_id": "EV_OBS",
                "evidence_type": "MARKET_OBSERVATION",
                "freshness": {"status": "STALE"},
                "confidence": {"score": 75}
            },
            {
                "evidence_id": "EV_TEL",
                "evidence_type": "TELEMETRY_LOG",
                "freshness": {"status": "LIVE"},
                "confidence": {"score": 95}
            },
            {
                "evidence_id": "EV_TX",
                "evidence_type": "TRANSACTION_RECORD",
                "freshness": {"status": "RECENT"},
                "confidence": {"score": 90}
            }
        ]
        ranked = self.ranker.rank_evidence(items)
        self.assertEqual(ranked[0]["evidence_id"], "EV_TEL")
        self.assertEqual(ranked[0]["evidence_rank"], 1)
        self.assertEqual(ranked[1]["evidence_id"], "EV_TX")
        self.assertEqual(ranked[1]["evidence_rank"], 2)
        self.assertEqual(ranked[2]["evidence_id"], "EV_OBS")
        self.assertEqual(ranked[2]["evidence_rank"], 3)

if __name__ == "__main__":
    unittest.main()
