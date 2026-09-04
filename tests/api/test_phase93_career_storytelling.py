"""
Phase 9.3: Career, Resume & Technical Interview Storytelling Test Suite
Project: InsightPilot AI
Competition: Accenture Innovation Challenge 2026 (Track 3: BusinessIntelligence.ai)

Validates:
1. Existence of all 13 Phase 9.3 career deliverables in docs/career/
2. Indexing completeness in docs/career/README.md
3. Navigation linkage from root README.md to docs/career/
4. Preservation of locked canonical metrics across career documentation
5. Claim boundary policy definitions (Safe vs Conditional vs Unsafe)
6. Role-specific resume bullet sets existence
7. 30-question count in Interview QA stress test bank
8. Operational health and readiness probes
"""

import unittest
import os
from fastapi.testclient import TestClient
from backend.app.main import app

class TestPhase93CareerStorytelling(unittest.TestCase):

    def setUp(self):
        self.project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
        self.career_dir = os.path.join(self.project_root, "docs", "career")
        self.client = TestClient(app)

    # --------------------------------------------------------------------------
    # Test 1: Required Career Deliverables Existence
    # --------------------------------------------------------------------------
    def test_career_deliverables_exist(self):
        """Verify that all 13 required Phase 9.3 career documents exist on disk."""
        required_files = [
            "CAREER_PORTFOLIO_CASE_STUDY.md",
            "RESUME_PROJECT_BULLETS.md",
            "TECHNICAL_INTERVIEW_STORYBOOK.md",
            "BEHAVIORAL_INTERVIEW_STORIES.md",
            "SYSTEM_DESIGN_INTERVIEW_GUIDE.md",
            "TECHNICAL_SKILLS_EVIDENCE_MATRIX.md",
            "PROJECT_ELEVATOR_PITCHES.md",
            "INTERVIEW_QA_STRESS_TEST.md",
            "LINKEDIN_PROJECT_SHOWCASE.md",
            "GITHUB_PORTFOLIO_PRESENTATION_GUIDE.md",
            "CAREER_READINESS_SCORECARD.md",
            "CLAIM_BOUNDARY_POLICY.md",
            "README.md",
        ]

        for fname in required_files:
            fpath = os.path.join(self.career_dir, fname)
            self.assertTrue(os.path.isfile(fpath), f"Missing career deliverable: {fname}")

    # --------------------------------------------------------------------------
    # Test 2: Career Hub Indexing Completeness
    # --------------------------------------------------------------------------
    def test_career_hub_links(self):
        """Verify that docs/career/README.md links to all major career documents."""
        fpath = os.path.join(self.career_dir, "README.md")
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()

        expected_links = [
            "CAREER_PORTFOLIO_CASE_STUDY.md",
            "RESUME_PROJECT_BULLETS.md",
            "TECHNICAL_INTERVIEW_STORYBOOK.md",
            "BEHAVIORAL_INTERVIEW_STORIES.md",
            "SYSTEM_DESIGN_INTERVIEW_GUIDE.md",
            "TECHNICAL_SKILLS_EVIDENCE_MATRIX.md",
            "PROJECT_ELEVATOR_PITCHES.md",
            "INTERVIEW_QA_STRESS_TEST.md",
            "LINKEDIN_PROJECT_SHOWCASE.md",
            "GITHUB_PORTFOLIO_PRESENTATION_GUIDE.md",
            "CAREER_READINESS_SCORECARD.md",
            "CLAIM_BOUNDARY_POLICY.md",
        ]

        for link in expected_links:
            self.assertIn(link, content, f"Career README missing link to: {link}")

    # --------------------------------------------------------------------------
    # Test 3: Root README Links to Career Hub
    # --------------------------------------------------------------------------
    def test_root_readme_career_links(self):
        """Verify that the root README.md links to docs/career/."""
        fpath = os.path.join(self.project_root, "README.md")
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn("docs/career/README.md", content)

    # --------------------------------------------------------------------------
    # Test 4: Canonical Metrics Preservation in Career Case Study
    # --------------------------------------------------------------------------
    def test_canonical_metrics_in_career_materials(self):
        """Verify that CAREER_PORTFOLIO_CASE_STUDY.md preserves locked metrics."""
        fpath = os.path.join(self.career_dir, "CAREER_PORTFOLIO_CASE_STUDY.md")
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn("Atlanta DC Stockout", content)
        self.assertIn("43.2%", content)
        self.assertIn("+$484,000.00", content)
        self.assertIn("+$341,422.91", content)
        self.assertIn("+$757,600.00", content)

    # --------------------------------------------------------------------------
    # Test 5: Claim Boundary Policy Definitions
    # --------------------------------------------------------------------------
    def test_claim_boundary_policy(self):
        """Verify that CLAIM_BOUNDARY_POLICY.md defines safe, conditional, and unsafe rules."""
        fpath = os.path.join(self.career_dir, "CLAIM_BOUNDARY_POLICY.md")
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn("SAFE CLAIMS", content)
        self.assertIn("CONDITIONAL CLAIMS", content)
        self.assertIn("UNSAFE CLAIMS", content)

    # --------------------------------------------------------------------------
    # Test 6: Role-Specific Resume Bullet Sets
    # --------------------------------------------------------------------------
    def test_resume_bullet_roles(self):
        """Verify that RESUME_PROJECT_BULLETS.md contains targeted role sections."""
        fpath = os.path.join(self.career_dir, "RESUME_PROJECT_BULLETS.md")
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn("AI Engineer", content)
        self.assertIn("Backend Engineer", content)
        self.assertIn("Full-Stack Engineer", content)
        self.assertIn("Machine Learning", content)

    # --------------------------------------------------------------------------
    # Test 7: Interview QA Stress Test Count
    # --------------------------------------------------------------------------
    def test_interview_qa_count(self):
        """Verify that INTERVIEW_QA_STRESS_TEST.md contains 30 numbered defense scenarios."""
        fpath = os.path.join(self.career_dir, "INTERVIEW_QA_STRESS_TEST.md")
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn("### 1.", content)
        self.assertIn("### 10.", content)
        self.assertIn("30.", content)

    # --------------------------------------------------------------------------
    # Test 8: Health and Readiness Probes
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
