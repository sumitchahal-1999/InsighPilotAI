"""
Phase 7.4: Final Competition Submission Assets & Delivery Package Test Suite
Project: InsightPilot AI
Competition: Accenture Innovation Challenge 2026 (Track 3: BusinessIntelligence.ai)

Validates:
1. Existence of all Phase 7.4 submission documentation deliverables
2. Internal documentation paths resolve to actual files
3. External asset placeholders use explicit '[TBD ...]' markers without fabricated URLs
4. Canonical numerical invariants are preserved without drift
5. Submission Manifest indexes all 6 asset categories
6. Submission README links to all required audit and packaging files
"""

import unittest
import os
import re

class TestPhase74SubmissionAssets(unittest.TestCase):

    def setUp(self):
        self.project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
        self.submission_dir = os.path.join(self.project_root, "docs", "submission")

    # --------------------------------------------------------------------------
    # Test 1: Required Phase 7.4 Deliverables Existence
    # --------------------------------------------------------------------------
    def test_phase74_deliverables_exist(self):
        """Verify that all 7 required Phase 7.4 submission documents exist on disk."""
        required_files = [
            "FINAL_SUBMISSION_PACKAGE.md",
            "FINAL_SUBMISSION_MANIFEST.md",
            "SUBMISSION_PORTAL_METADATA_TEMPLATE.md",
            "FINAL_ASSET_CHECKLIST.md",
            "EXTERNAL_ASSET_PLACEHOLDERS.md",
            "JUDGE_SUBMISSION_MAP.md",
            "FINAL_DELIVERY_MATRIX.md",
            "README.md",
        ]

        for fname in required_files:
            fpath = os.path.join(self.submission_dir, fname)
            self.assertTrue(os.path.isfile(fpath), f"Missing submission deliverable: {fname}")

    # --------------------------------------------------------------------------
    # Test 2: External Asset Placeholders Integrity
    # --------------------------------------------------------------------------
    def test_external_asset_placeholders_format(self):
        """Verify that external asset placeholders use explicit [TBD ...] format."""
        fpath = os.path.join(self.submission_dir, "EXTERNAL_ASSET_PLACEHOLDERS.md")
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn("[TBD — INSERT FINAL 3-MINUTE VIDEO URL]", content)
        self.assertIn("[TBD — INSERT FINAL 5-MINUTE TECHNICAL VIDEO URL]", content)
        self.assertIn("[TBD — INSERT FINAL PRESENTATION PDF / SLIDES URL]", content)

        # Ensure no fake YouTube or cloud drive URLs are present
        fake_patterns = [
            r"https?://(?:www\.)?youtube\.com/watch\?v=[a-zA-Z0-9_-]{8,}",
            r"https?://drive\.google\.com/file/d/[a-zA-Z0-9_-]{10,}",
        ]
        for pattern in fake_patterns:
            self.assertIsNone(re.search(pattern, content), "Fabricated external URL found in placeholders")

    # --------------------------------------------------------------------------
    # Test 3: Canonical Metrics Parity in Final Submission Package
    # --------------------------------------------------------------------------
    def test_canonical_metrics_in_submission_package(self):
        """Verify that FINAL_SUBMISSION_PACKAGE.md strictly reflects canonical metrics."""
        fpath = os.path.join(self.submission_dir, "FINAL_SUBMISSION_PACKAGE.md")
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
        self.assertIn("90.0%", content)

    # --------------------------------------------------------------------------
    # Test 4: Submission Manifest 6 Categories Coverage
    # --------------------------------------------------------------------------
    def test_submission_manifest_categories(self):
        """Verify that FINAL_SUBMISSION_MANIFEST.md covers all 6 required categories."""
        fpath = os.path.join(self.submission_dir, "FINAL_SUBMISSION_MANIFEST.md")
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()

        categories = [
            "Category A: Core Project & Technical Architecture",
            "Category B: Product Demonstration & Video Assets",
            "Category C: Presentation & Pitch Materials",
            "Category D: Business Case & Commercial Strategy",
            "Category E: Technical Validation & Test Automation",
            "Category F: Trust, AI Safety & Governance",
        ]

        for cat in categories:
            self.assertIn(cat, content, f"Missing manifest category: {cat}")

    # --------------------------------------------------------------------------
    # Test 5: Submission README Index Integrity
    # --------------------------------------------------------------------------
    def test_submission_readme_links(self):
        """Verify that docs/submission/README.md references all key packaging documents."""
        fpath = os.path.join(self.submission_dir, "README.md")
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()

        expected_links = [
            "JUDGE_QUICKSTART.md",
            "FINAL_SUBMISSION_PACKAGE.md",
            "JUDGE_SUBMISSION_MAP.md",
            "FINAL_SUBMISSION_MANIFEST.md",
            "FINAL_ASSET_CHECKLIST.md",
            "SUBMISSION_PORTAL_METADATA_TEMPLATE.md",
            "EXTERNAL_ASSET_PLACEHOLDERS.md",
            "FINAL_DELIVERY_MATRIX.md",
            "FINAL_SUBMISSION_AUDIT.md",
            "METRIC_CONSISTENCY_AUDIT.md",
            "REPRODUCIBILITY_GUIDE.md",
        ]

        for link in expected_links:
            self.assertIn(link, content, f"Submission README missing link to: {link}")

if __name__ == "__main__":
    unittest.main()
