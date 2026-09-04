"""
Phase 9.4: Final Project Closure, README Finalization & Long-Term Handoff Test Suite
Project: InsightPilot AI
Competition: Accenture Innovation Challenge 2026 (Track 3: BusinessIntelligence.ai)

Validates:
1. Existence of all required Phase 9.4 closure documents in docs/closure/
2. Indexing completeness in docs/closure/README.md
3. Navigation linkage from root README.md to docs/closure/
4. Preservation of locked canonical metrics across closure documentation
5. Foundational architectural invariant preservation
6. Final project state claim categories definition
7. Manual action register human-boundary preservation
8. Operational health and readiness probes
"""

import unittest
import os
from fastapi.testclient import TestClient
from backend.app.main import app

class TestPhase94ProjectClosure(unittest.TestCase):

    def setUp(self):
        self.project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
        self.closure_dir = os.path.join(self.project_root, "docs", "closure")
        self.client = TestClient(app)

    # --------------------------------------------------------------------------
    # Test 1: Required Closure Deliverables Existence
    # --------------------------------------------------------------------------
    def test_closure_deliverables_exist(self):
        """Verify that all 9 required Phase 9.4 closure documents exist on disk."""
        required_files = [
            "DOCUMENTATION_NAVIGATION_AUDIT.md",
            "LONG_TERM_HANDOFF.md",
            "PROJECT_MAINTENANCE_AND_EVOLUTION.md",
            "PROJECT_ARCHIVE.md",
            "FINAL_PROJECT_STATE.md",
            "MANUAL_ACTION_REGISTER.md",
            "FINAL_REPOSITORY_CLOSURE_AUDIT.md",
            "FINAL_PROJECT_COMPLETION_REPORT.md",
            "README.md",
        ]

        for fname in required_files:
            fpath = os.path.join(self.closure_dir, fname)
            self.assertTrue(os.path.isfile(fpath), f"Missing closure deliverable: {fname}")

    # --------------------------------------------------------------------------
    # Test 2: Closure Hub Indexing Completeness
    # --------------------------------------------------------------------------
    def test_closure_hub_links(self):
        """Verify that docs/closure/README.md links to all major closure documents."""
        fpath = os.path.join(self.closure_dir, "README.md")
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()

        expected_links = [
            "DOCUMENTATION_NAVIGATION_AUDIT.md",
            "LONG_TERM_HANDOFF.md",
            "PROJECT_MAINTENANCE_AND_EVOLUTION.md",
            "PROJECT_ARCHIVE.md",
            "FINAL_PROJECT_STATE.md",
            "MANUAL_ACTION_REGISTER.md",
            "FINAL_REPOSITORY_CLOSURE_AUDIT.md",
            "FINAL_PROJECT_COMPLETION_REPORT.md",
        ]

        for link in expected_links:
            self.assertIn(link, content, f"Closure README missing link to: {link}")

    # --------------------------------------------------------------------------
    # Test 3: Root README Links to Closure Hub
    # --------------------------------------------------------------------------
    def test_root_readme_closure_links(self):
        """Verify that the root README.md links to docs/closure/."""
        fpath = os.path.join(self.project_root, "README.md")
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn("docs/closure/README.md", content)

    # --------------------------------------------------------------------------
    # Test 4: Foundational Architectural Invariant Preservation
    # --------------------------------------------------------------------------
    def test_foundational_invariant_preserved(self):
        """Verify that the foundational invariant is preserved in closure documents."""
        fpath = os.path.join(self.closure_dir, "LONG_TERM_HANDOFF.md")
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn("Deterministic systems own quantitative truth", content)
        self.assertIn("AI explains grounded facts", content)


    # --------------------------------------------------------------------------
    # Test 5: Canonical Metrics Invariants Preservation
    # --------------------------------------------------------------------------
    def test_canonical_metrics_in_closure_report(self):
        """Verify that FINAL_PROJECT_COMPLETION_REPORT.md preserves locked metrics."""
        fpath = os.path.join(self.closure_dir, "FINAL_PROJECT_COMPLETION_REPORT.md")
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn("Atlanta DC Stockout", content)
        self.assertIn("43.2%", content)
        self.assertIn("+$484,000.00", content)
        self.assertIn("+$341,422.91", content)
        self.assertIn("+$757,600.00", content)

    # --------------------------------------------------------------------------
    # Test 6: Final Project State Claim Categories
    # --------------------------------------------------------------------------
    def test_claim_categories_in_final_project_state(self):
        """Verify that FINAL_PROJECT_STATE.md defines all 4 capability categories."""
        fpath = os.path.join(self.closure_dir, "FINAL_PROJECT_STATE.md")
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn("VERIFIED IMPLEMENTATION", content)
        self.assertIn("MODELED / SIMULATED", content)
        self.assertIn("DOCUMENTED FUTURE ROADMAP", content)
        self.assertIn("NOT CLAIMED", content)

    # --------------------------------------------------------------------------
    # Test 7: Manual Action Register Boundaries
    # --------------------------------------------------------------------------
    def test_manual_action_register_boundaries(self):
        """Verify that MANUAL_ACTION_REGISTER.md accurately identifies pending human actions."""
        fpath = os.path.join(self.closure_dir, "MANUAL_ACTION_REGISTER.md")
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn("Export Pitch Deck PDF", content)
        self.assertIn("Record 3-Minute Demo Video", content)
        self.assertIn("Submit on Competition Portal", content)

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
