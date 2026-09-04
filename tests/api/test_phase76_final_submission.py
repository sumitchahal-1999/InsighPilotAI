"""
Phase 7.6: Final Competition Submission Sign-Off & Delivery Readiness Test Suite
Project: InsightPilot AI
Competition: Accenture Innovation Challenge 2026 (Track 3: BusinessIntelligence.ai)

Validates:
1. Existence of all 8 Phase 7.6 final sign-off deliverables in docs/submission/final/
2. Canonical metric lock integrity and trace references
3. Valid evidence-based decision category (CONDITIONAL GO) in sign-off records
4. Strict external asset placeholder integrity (TBD / NOT YET VERIFIED)
5. Comprehensive index coverage in docs/submission/README.md
"""

import unittest
import os
import re

class TestPhase76FinalSubmission(unittest.TestCase):

    def setUp(self):
        self.project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
        self.final_dir = os.path.join(self.project_root, "docs", "submission", "final")
        self.submission_dir = os.path.join(self.project_root, "docs", "submission")

    # --------------------------------------------------------------------------
    # Test 1: Required Phase 7.6 Deliverables Existence
    # --------------------------------------------------------------------------
    def test_phase76_deliverables_exist(self):
        """Verify that all 8 required Phase 7.6 final submission documents exist on disk."""
        required_files = [
            "FINAL_COMPETITION_SIGN_OFF.md",
            "FINAL_SUBMISSION_AUDIT.md",
            "EXTERNAL_SUBMISSION_VERIFICATION.md",
            "FINAL_SUBMISSION_COMMANDS.md",
            "FINAL_COMPETITION_CHECKLIST.md",
            "FINAL_METRIC_LOCK.md",
            "FINAL_DELIVERY_LOG.md",
            "SUBMISSION_READINESS_SUMMARY.md",
        ]

        for fname in required_files:
            fpath = os.path.join(self.final_dir, fname)
            self.assertTrue(os.path.isfile(fpath), f"Missing final submission deliverable: {fname}")

    # --------------------------------------------------------------------------
    # Test 2: Canonical Metric Lock Invariant Parity
    # --------------------------------------------------------------------------
    def test_canonical_metric_lock_invariants(self):
        """Verify that FINAL_METRIC_LOCK.md strictly locks all canonical metrics."""
        fpath = os.path.join(self.final_dir, "FINAL_METRIC_LOCK.md")
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn("$15,430,000.06", content)
        self.assertIn("$14,200,000.05", content)
        self.assertIn("-$1,230,000.01", content)
        self.assertIn("-7.97%", content)
        self.assertIn("Atlanta DC Stockout", content)
        self.assertIn("43.2%", content)
        self.assertIn("-$550,000.00", content)
        self.assertIn("89% HIGH", content)
        self.assertIn("<65%", content)
        self.assertIn("+$484,000.00", content)
        self.assertIn("+$341,422.91", content)
        self.assertIn("+$757,600.00", content)

    # --------------------------------------------------------------------------
    # Test 3: Valid Decision Category in Final Sign-Off
    # --------------------------------------------------------------------------
    def test_final_sign_off_decision_verdict(self):
        """Verify that FINAL_COMPETITION_SIGN_OFF.md records a valid CONDITIONAL GO verdict."""
        fpath = os.path.join(self.final_dir, "FINAL_COMPETITION_SIGN_OFF.md")
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn("CONDITIONAL GO — EXTERNAL ACTION REQUIRED", content)
        self.assertIn("206 / 206 tests passing", content)
        self.assertIn("10/10 static pages", content)

    # --------------------------------------------------------------------------
    # Test 4: External Asset Placeholders Integrity
    # --------------------------------------------------------------------------
    def test_external_submission_verification_integrity(self):
        """Verify that EXTERNAL_SUBMISSION_VERIFICATION.md uses strict TBD markers."""
        fpath = os.path.join(self.final_dir, "EXTERNAL_SUBMISSION_VERIFICATION.md")
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn("TBD — VERIFIED URL REQUIRED", content)
        self.assertIn("NOT YET VERIFIED", content)

        # Ensure no fake YouTube or cloud drive URLs are present
        fake_patterns = [
            r"https?://(?:www\.)?youtube\.com/watch\?v=[a-zA-Z0-9_-]{8,}",
            r"https?://drive\.google\.com/file/d/[a-zA-Z0-9_-]{10,}",
        ]
        for pattern in fake_patterns:
            self.assertIsNone(re.search(pattern, content), "Fabricated external URL found in verification file")

    # --------------------------------------------------------------------------
    # Test 5: Submission Hub Index Links
    # --------------------------------------------------------------------------
    def test_submission_hub_final_links(self):
        """Verify that docs/submission/README.md links to all final submission documents."""
        fpath = os.path.join(self.submission_dir, "README.md")
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()

        expected_links = [
            "./final/FINAL_COMPETITION_SIGN_OFF.md",
            "./final/FINAL_SUBMISSION_AUDIT.md",
            "./final/EXTERNAL_SUBMISSION_VERIFICATION.md",
            "./final/FINAL_SUBMISSION_COMMANDS.md",
            "./final/FINAL_COMPETITION_CHECKLIST.md",
            "./final/FINAL_METRIC_LOCK.md",
            "./final/FINAL_DELIVERY_LOG.md",
            "./final/SUBMISSION_READINESS_SUMMARY.md",
        ]

        for link in expected_links:
            self.assertIn(link, content, f"Submission README missing link to: {link}")

if __name__ == "__main__":
    unittest.main()
