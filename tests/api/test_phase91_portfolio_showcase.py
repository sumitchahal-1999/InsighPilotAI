"""
Phase 9.1: Portfolio & Open-Source Showcase Test Suite
Project: InsightPilot AI
Competition: Accenture Innovation Challenge 2026 (Track 3: BusinessIntelligence.ai)

Validates:
1. Existence of all required Phase 9.1 portfolio deliverables in docs/portfolio/
2. Indexing completeness in docs/portfolio/README.md
3. Navigation linkage from root README.md to docs/portfolio/
4. Preservation of locked canonical metrics across portfolio documents
5. Truthful deployment status representation (pending cloud actions marked accurately)
6. Operational health and readiness probes
"""

import unittest
import os
from fastapi.testclient import TestClient
from backend.app.main import app

class TestPhase91PortfolioShowcase(unittest.TestCase):

    def setUp(self):
        self.project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
        self.portfolio_dir = os.path.join(self.project_root, "docs", "portfolio")
        self.client = TestClient(app)

    # --------------------------------------------------------------------------
    # Test 1: Required Portfolio Deliverables Existence
    # --------------------------------------------------------------------------
    def test_portfolio_deliverables_exist(self):
        """Verify that all 7 required Phase 9.1 portfolio documents exist on disk."""
        required_files = [
            "CASE_STUDY.md",
            "RECRUITER_OVERVIEW.md",
            "TECHNICAL_WALKTHROUGH.md",
            "FEATURE_SHOWCASE.md",
            "REPOSITORY_TOUR.md",
            "README.md",
            "OPEN_SOURCE_SHOWCASE_AUDIT.md",
        ]

        for fname in required_files:
            fpath = os.path.join(self.portfolio_dir, fname)
            self.assertTrue(os.path.isfile(fpath), f"Missing portfolio deliverable: {fname}")

    # --------------------------------------------------------------------------
    # Test 2: Portfolio Hub Indexing Completeness
    # --------------------------------------------------------------------------
    def test_portfolio_hub_links(self):
        """Verify that docs/portfolio/README.md links to all portfolio documents."""
        fpath = os.path.join(self.portfolio_dir, "README.md")
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()

        expected_links = [
            "RECRUITER_OVERVIEW.md",
            "CASE_STUDY.md",
            "TECHNICAL_WALKTHROUGH.md",
            "FEATURE_SHOWCASE.md",
            "REPOSITORY_TOUR.md",
            "OPEN_SOURCE_SHOWCASE_AUDIT.md",
        ]

        for link in expected_links:
            self.assertIn(link, content, f"Portfolio README missing link to: {link}")

    # --------------------------------------------------------------------------
    # Test 3: Root README Links to Portfolio Hub
    # --------------------------------------------------------------------------
    def test_root_readme_portfolio_links(self):
        """Verify that the root README.md prominently links to docs/portfolio/."""
        fpath = os.path.join(self.project_root, "README.md")
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn("docs/portfolio/RECRUITER_OVERVIEW.md", content)
        self.assertIn("docs/portfolio/CASE_STUDY.md", content)
        self.assertIn("docs/portfolio/TECHNICAL_WALKTHROUGH.md", content)
        self.assertIn("docs/portfolio/FEATURE_SHOWCASE.md", content)
        self.assertIn("docs/portfolio/README.md", content)

    # --------------------------------------------------------------------------
    # Test 4: Canonical Metrics Preservation in Portfolio Materials
    # --------------------------------------------------------------------------
    def test_canonical_metrics_in_case_study(self):
        """Verify that CASE_STUDY.md and TECHNICAL_WALKTHROUGH.md preserve canonical truth."""
        case_study_path = os.path.join(self.portfolio_dir, "CASE_STUDY.md")
        with open(case_study_path, "r", encoding="utf-8") as f:
            cs_content = f.read()

        self.assertIn("Deterministic systems own quantitative truth", cs_content)
        self.assertIn("Atlanta DC Stockout", cs_content)
        self.assertIn("43.2%", cs_content)
        self.assertIn("+$484,000.00", cs_content)
        self.assertIn("+$341,422.91", cs_content)

        walkthrough_path = os.path.join(self.portfolio_dir, "TECHNICAL_WALKTHROUGH.md")
        with open(walkthrough_path, "r", encoding="utf-8") as f:
            wt_content = f.read()

        self.assertIn("Atlanta DC Stockout: 43.2%", wt_content)
        self.assertIn("+$484K recovery", wt_content)
        self.assertIn("11-node StateGraph", wt_content)

    # --------------------------------------------------------------------------
    # Test 5: Truthful Status Representation
    # --------------------------------------------------------------------------
    def test_truthful_status_representation(self):
        """Verify that root README accurately represents cloud deployment as pending."""
        fpath = os.path.join(self.project_root, "README.md")
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn("PENDING OWNER ACTION", content)
        self.assertIn("Requires Render/Vercel Dashboard Linking", content)

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
