"""
Phase 9.2: Engineering Quality & Maintainability Audit Test Suite
Project: InsightPilot AI
Competition: Accenture Innovation Challenge 2026 (Track 3: BusinessIntelligence.ai)

Validates:
1. Existence of all required Phase 9.2 engineering quality deliverables in docs/engineering/
2. Indexing completeness in docs/engineering/README.md
3. Navigation linkage from root README.md to docs/engineering/
4. Stale test count remediation across root README.md
5. Preservation of locked canonical metrics across engineering documentation
6. Operational health and readiness probes
"""

import unittest
import os
from fastapi.testclient import TestClient
from backend.app.main import app

class TestPhase92EngineeringQuality(unittest.TestCase):

    def setUp(self):
        self.project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
        self.engineering_dir = os.path.join(self.project_root, "docs", "engineering")
        self.client = TestClient(app)

    # --------------------------------------------------------------------------
    # Test 1: Required Engineering Quality Deliverables Existence
    # --------------------------------------------------------------------------
    def test_engineering_deliverables_exist(self):
        """Verify that all 8 required Phase 9.2 engineering documents exist on disk."""
        required_files = [
            "ENGINEERING_QUALITY_AUDIT.md",
            "MAINTAINABILITY_ASSESSMENT.md",
            "CODE_QUALITY_FINDINGS.md",
            "TECHNICAL_DEBT_REGISTER.md",
            "DEPENDENCY_REVIEW.md",
            "DOCUMENTATION_CONSISTENCY_AUDIT.md",
            "REMEDIATION_LOG.md",
            "README.md",
        ]

        for fname in required_files:
            fpath = os.path.join(self.engineering_dir, fname)
            self.assertTrue(os.path.isfile(fpath), f"Missing engineering deliverable: {fname}")

    # --------------------------------------------------------------------------
    # Test 2: Engineering Hub Indexing Completeness
    # --------------------------------------------------------------------------
    def test_engineering_hub_links(self):
        """Verify that docs/engineering/README.md links to all engineering documents."""
        fpath = os.path.join(self.engineering_dir, "README.md")
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()

        expected_links = [
            "ENGINEERING_QUALITY_AUDIT.md",
            "MAINTAINABILITY_ASSESSMENT.md",
            "CODE_QUALITY_FINDINGS.md",
            "TECHNICAL_DEBT_REGISTER.md",
            "DEPENDENCY_REVIEW.md",
            "DOCUMENTATION_CONSISTENCY_AUDIT.md",
            "REMEDIATION_LOG.md",
        ]

        for link in expected_links:
            self.assertIn(link, content, f"Engineering README missing link to: {link}")

    # --------------------------------------------------------------------------
    # Test 3: Root README Links to Engineering Hub
    # --------------------------------------------------------------------------
    def test_root_readme_engineering_links(self):
        """Verify that the root README.md links to docs/engineering/."""
        fpath = os.path.join(self.project_root, "README.md")
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn("docs/engineering/README.md", content)

    # --------------------------------------------------------------------------
    # Test 4: Stale Test Count Badge Remediation
    # --------------------------------------------------------------------------
    def test_stale_count_remediation(self):
        """Verify that the root README reflects an updated test count beyond stale 259."""
        fpath = os.path.join(self.project_root, "README.md")
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertNotIn("259%2F259_Passing", content)
        self.assertIn("Passing_(100%25)", content)


    # --------------------------------------------------------------------------
    # Test 5: Canonical Invariants Preservation
    # --------------------------------------------------------------------------
    def test_canonical_invariants_in_consistency_audit(self):
        """Verify that DOCUMENTATION_CONSISTENCY_AUDIT.md preserves locked metrics."""
        fpath = os.path.join(self.engineering_dir, "DOCUMENTATION_CONSISTENCY_AUDIT.md")
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn("Atlanta DC Stockout", content)
        self.assertIn("43.2%", content)
        self.assertIn("+$484,000.00", content)
        self.assertIn("+$341,422.91", content)

    # --------------------------------------------------------------------------
    # Test 6: Health and Readiness Probes
    # --------------------------------------------------------------------------
    def test_health_and_readiness_probes(self):
        """Verify that local /health and /api/v1/demo/readiness respond successfully."""
        res_health = self.client.get("/health")
        self.assertEqual(res_health.status_code, 200)
        self.assertEqual(res_health.json().get("status"), "ok")

        res_readiness = self.client.get("/api/v1/demo/readiness")
        self.assertEqual(res_readiness.status_code, 200)
        self.assertTrue(res_readiness.json().get("submission_ready"))

if __name__ == "__main__":
    unittest.main()
