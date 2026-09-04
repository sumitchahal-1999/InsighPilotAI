"""
Phase 9.6: Final Manual Execution Handoff & Owner Completion Package Test Suite
Project: InsightPilot AI
Competition: Accenture Innovation Challenge 2026 (Track 3: BusinessIntelligence.ai)

Validates:
1. Existence of all required Phase 9.6 handoff documents in docs/handoff/
2. Indexing completeness in docs/handoff/README.md
3. Navigation linkage from root README.md to docs/handoff/
4. Zero machine-specific paths in docs/handoff/ documents
5. Truthful boundaries: no premature claims of completed video or portal submission
6. Preservation of locked canonical metrics across handoff documentation
7. Foundational architectural invariant preservation
8. Required external-action placeholders in SUBMISSION_EVIDENCE_REGISTER.md
9. Formal owner sign-off boundary preservation in OWNER_FINAL_SIGN_OFF.md
10. Operational health and readiness probes
"""

import unittest
import os
from fastapi.testclient import TestClient
from backend.app.main import app

class TestPhase96ManualHandoff(unittest.TestCase):

    def setUp(self):
        self.project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
        self.handoff_dir = os.path.join(self.project_root, "docs", "handoff")
        self.client = TestClient(app)

    # --------------------------------------------------------------------------
    # Test 1: Required Handoff Deliverables Existence
    # --------------------------------------------------------------------------
    def test_handoff_deliverables_exist(self):
        """Verify that all 12 required Phase 9.6 handoff documents exist on disk."""
        required_files = [
            "FINAL_OWNER_EXECUTION_ROADMAP.md",
            "FINAL_DEMO_EXECUTION_GUIDE.md",
            "RECORDING_DAY_CHECKLIST.md",
            "FINAL_PITCH_DECK_EXECUTION_GUIDE.md",
            "EXTERNAL_ASSET_VERIFICATION_WORKFLOW.md",
            "FINAL_COMPETITION_PORTAL_EXECUTION_RUNBOOK.md",
            "FINAL_OWNER_PRE_SUBMISSION_GATE.md",
            "SUBMISSION_EVIDENCE_REGISTER.md",
            "OWNER_FINAL_SIGN_OFF.md",
            "MANUAL_EXECUTION_SEQUENCE.md",
            "PHASE_96_FINAL_HANDOFF_REPORT.md",
            "README.md",
        ]

        for fname in required_files:
            fpath = os.path.join(self.handoff_dir, fname)
            self.assertTrue(os.path.isfile(fpath), f"Missing handoff deliverable: {fname}")

    # --------------------------------------------------------------------------
    # Test 2: Handoff Hub Indexing Completeness
    # --------------------------------------------------------------------------
    def test_handoff_hub_links(self):
        """Verify that docs/handoff/README.md links to all major handoff documents."""
        fpath = os.path.join(self.handoff_dir, "README.md")
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()

        expected_links = [
            "FINAL_OWNER_EXECUTION_ROADMAP.md",
            "MANUAL_EXECUTION_SEQUENCE.md",
            "FINAL_DEMO_EXECUTION_GUIDE.md",
            "RECORDING_DAY_CHECKLIST.md",
            "FINAL_PITCH_DECK_EXECUTION_GUIDE.md",
            "EXTERNAL_ASSET_VERIFICATION_WORKFLOW.md",
            "FINAL_COMPETITION_PORTAL_EXECUTION_RUNBOOK.md",
            "FINAL_OWNER_PRE_SUBMISSION_GATE.md",
            "SUBMISSION_EVIDENCE_REGISTER.md",
            "OWNER_FINAL_SIGN_OFF.md",
            "PHASE_96_FINAL_HANDOFF_REPORT.md",
        ]

        for link in expected_links:
            self.assertIn(link, content, f"Handoff README missing link to: {link}")

    # --------------------------------------------------------------------------
    # Test 3: Root README Links to Handoff Hub
    # --------------------------------------------------------------------------
    def test_root_readme_handoff_links(self):
        """Verify that the root README.md links to docs/handoff/."""
        fpath = os.path.join(self.project_root, "README.md")
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn("docs/handoff/README.md", content)

    # --------------------------------------------------------------------------
    # Test 4: Zero Machine-Specific Paths in Handoff Docs
    # --------------------------------------------------------------------------
    def test_no_machine_specific_paths_in_handoff_docs(self):
        """Verify that no local machine paths (e.g. file:///C:/ or C:\\Users) exist in docs/handoff/."""
        for fname in os.listdir(self.handoff_dir):
            if fname.endswith(".md"):
                fpath = os.path.join(self.handoff_dir, fname)
                with open(fpath, "r", encoding="utf-8") as f:
                    content = f.read()
                self.assertNotIn("file:///C:", content, f"Machine-specific path found in {fname}")
                self.assertNotIn("C:\\Users", content, f"Machine-specific path found in {fname}")

    # --------------------------------------------------------------------------
    # Test 5: Truthful Boundaries — No False Video or Portal Claims
    # --------------------------------------------------------------------------
    def test_truthful_boundaries_preserved(self):
        """Verify that pending human items are explicitly designated as pending."""
        fpath = os.path.join(self.handoff_dir, "OWNER_FINAL_SIGN_OFF.md")
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn("ANTIGRAVITY WORK COMPLETE", content)
        self.assertIn("OWNER SUBMISSION PENDING", content)
        self.assertIn("Record 3-Minute Demonstration Video", content)
        self.assertIn("Complete Official Portal Submission", content)

    # --------------------------------------------------------------------------
    # Test 6: Foundational Invariant Preservation
    # --------------------------------------------------------------------------
    def test_foundational_invariant_preserved(self):
        """Verify that the foundational invariant is preserved in handoff documents."""
        fpath = os.path.join(self.handoff_dir, "FINAL_COMPETITION_PORTAL_EXECUTION_RUNBOOK.md")
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn("Deterministic systems own quantitative truth", content)
        self.assertIn("AI explains grounded facts", content)

    # --------------------------------------------------------------------------
    # Test 7: Canonical Metrics Invariants Preservation
    # --------------------------------------------------------------------------
    def test_canonical_metrics_in_handoff_docs(self):
        """Verify that locked metrics are preserved in handoff documentation."""
        fpath = os.path.join(self.handoff_dir, "PHASE_96_FINAL_HANDOFF_REPORT.md")
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn("Atlanta DC Stockout", content)
        self.assertIn("43.2%", content)
        self.assertIn("+$484,000.00", content)
        self.assertIn("+$341,422.91", content)
        self.assertIn("+$757,600.00", content)

    # --------------------------------------------------------------------------
    # Test 8: Submission Evidence Register Placeholders
    # --------------------------------------------------------------------------
    def test_evidence_register_placeholders(self):
        """Verify that SUBMISSION_EVIDENCE_REGISTER.md contains required pending fields."""
        fpath = os.path.join(self.handoff_dir, "SUBMISSION_EVIDENCE_REGISTER.md")
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn("Final Demo Video URL", content)
        self.assertIn("Pitch Deck PDF Name", content)
        self.assertIn("Portal Confirmation ID", content)
        self.assertIn("Confirmation Screenshot", content)

    # --------------------------------------------------------------------------
    # Test 9: Health and Readiness Probes
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
