"""
InsightPilot AI — Insufficient Evidence Unit Tests
Tests evidence validator behavior when supporting evidence is absent or missing.
"""

import unittest
from evidence.evidence_loader import EvidenceLoader
from evidence.evidence_validator import EvidenceValidator

class TestInsufficientEvidence(unittest.TestCase):
    
    def setUp(self):
        self.loader = EvidenceLoader()
        self.validator = EvidenceValidator(self.loader)

    def test_insufficient_evidence_status(self):
        report = self.validator.check_driver_evidence_sufficiency("unsupported_driver", [])
        self.assertEqual(report["evidence_status"], "INSUFFICIENT")
        self.assertEqual(report["evidence_count"], 0)
        self.assertIn("No corroborating source records found", report["reason"])

    def test_sufficient_evidence_status(self):
        report = self.validator.check_driver_evidence_sufficiency("atlanta_dc_stockout", [{"id": "ev1"}, {"id": "ev2"}])
        self.assertEqual(report["evidence_status"], "SUFFICIENT")
        self.assertEqual(report["evidence_count"], 2)

if __name__ == "__main__":
    unittest.main()
