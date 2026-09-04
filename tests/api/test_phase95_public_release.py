"""
Phase 9.5: Public Repository Release & External Readiness Verification Test Suite
Project: InsightPilot AI
Competition: Accenture Innovation Challenge 2026 (Track 3: BusinessIntelligence.ai)

Validates:
1. Existence of all required Phase 9.5 public release documents in docs/release/
2. Indexing completeness in docs/release/README.md
3. Navigation linkage from root README.md to docs/release/
4. Zero machine-specific paths in docs/release/ documents
5. Preservation of locked canonical metrics across release documentation
6. Foundational architectural invariant preservation
7. 5-Tier claim classification in PUBLIC_CLAIM_AND_TRUST_AUDIT.md
8. Presence of required human actions in FINAL_EXTERNAL_ACTION_REGISTER.md
9. Operational health and readiness probes
"""

import unittest
import os
from fastapi.testclient import TestClient
from backend.app.main import app

class TestPhase95PublicRelease(unittest.TestCase):

    def setUp(self):
        self.project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
        self.release_dir = os.path.join(self.project_root, "docs", "release")
        self.client = TestClient(app)

    # --------------------------------------------------------------------------
    # Test 1: Required Public Release Deliverables Existence
    # --------------------------------------------------------------------------
    def test_release_deliverables_exist(self):
        """Verify that all 9 required Phase 9.5 release documents exist on disk."""
        required_files = [
            "PUBLIC_REPOSITORY_READINESS_AUDIT.md",
            "EXTERNAL_LINK_VERIFICATION.md",
            "PUBLIC_CLAIM_AND_TRUST_AUDIT.md",
            "EVALUATOR_5_MINUTE_GUIDE.md",
            "RECRUITER_PORTFOLIO_AUDIT.md",
            "FINAL_EXTERNAL_ACTION_REGISTER.md",
            "PUBLIC_RELEASE_CHECKLIST.md",
            "PHASE_95_RELEASE_SUMMARY.md",
            "README.md",
        ]

        for fname in required_files:
            fpath = os.path.join(self.release_dir, fname)
            self.assertTrue(os.path.isfile(fpath), f"Missing release deliverable: {fname}")

    # --------------------------------------------------------------------------
    # Test 2: Public Release Hub Indexing Completeness
    # --------------------------------------------------------------------------
    def test_release_hub_links(self):
        """Verify that docs/release/README.md links to all major release documents."""
        fpath = os.path.join(self.release_dir, "README.md")
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()

        expected_links = [
            "EVALUATOR_5_MINUTE_GUIDE.md",
            "PUBLIC_REPOSITORY_READINESS_AUDIT.md",
            "EXTERNAL_LINK_VERIFICATION.md",
            "PUBLIC_CLAIM_AND_TRUST_AUDIT.md",
            "RECRUITER_PORTFOLIO_AUDIT.md",
            "FINAL_EXTERNAL_ACTION_REGISTER.md",
            "PUBLIC_RELEASE_CHECKLIST.md",
            "PHASE_95_RELEASE_SUMMARY.md",
        ]

        for link in expected_links:
            self.assertIn(link, content, f"Release README missing link to: {link}")

    # --------------------------------------------------------------------------
    # Test 3: Root README Links to Public Release Hub
    # --------------------------------------------------------------------------
    def test_root_readme_release_links(self):
        """Verify that the root README.md links to docs/release/."""
        fpath = os.path.join(self.project_root, "README.md")
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn("docs/release/README.md", content)

    # --------------------------------------------------------------------------
    # Test 4: Zero Machine-Specific Paths in Public Docs
    # --------------------------------------------------------------------------
    def test_no_machine_specific_paths_in_release_docs(self):
        """Verify that no local machine paths (e.g. file:///C:/ or C:\\Users) exist in docs/release/."""
        for fname in os.listdir(self.release_dir):
            if fname.endswith(".md"):
                fpath = os.path.join(self.release_dir, fname)
                with open(fpath, "r", encoding="utf-8") as f:
                    content = f.read()
                self.assertNotIn("file:///C:", content, f"Machine-specific path found in {fname}")
                self.assertNotIn("C:\\Users", content, f"Machine-specific path found in {fname}")

    # --------------------------------------------------------------------------
    # Test 5: Foundational Invariant Preservation
    # --------------------------------------------------------------------------
    def test_foundational_invariant_preserved(self):
        """Verify that the foundational invariant is preserved in release documents."""
        fpath = os.path.join(self.release_dir, "PHASE_95_RELEASE_SUMMARY.md")
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn("Deterministic systems own quantitative truth", content)
        self.assertIn("AI explains grounded facts", content)

    # --------------------------------------------------------------------------
    # Test 6: Canonical Metrics Invariants Preservation
    # --------------------------------------------------------------------------
    def test_canonical_metrics_in_release_docs(self):
        """Verify that locked metrics are preserved in release documentation."""
        fpath = os.path.join(self.release_dir, "PHASE_95_RELEASE_SUMMARY.md")
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn("Atlanta DC Stockout", content)
        self.assertIn("43.2%", content)
        self.assertIn("+$484,000.00", content)
        self.assertIn("+$341,422.91", content)
        self.assertIn("+$757,600.00", content)

    # --------------------------------------------------------------------------
    # Test 7: 5-Tier Claim Classification
    # --------------------------------------------------------------------------
    def test_claim_classification_in_trust_audit(self):
        """Verify that PUBLIC_CLAIM_AND_TRUST_AUDIT.md defines all claim tiers."""
        fpath = os.path.join(self.release_dir, "PUBLIC_CLAIM_AND_TRUST_AUDIT.md")
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn("VERIFIED IMPLEMENTATION", content)
        self.assertIn("MODELED / SIMULATED", content)
        self.assertIn("DOCUMENTED FUTURE ROADMAP", content)
        self.assertIn("PENDING MANUAL EXTERNAL ACTION", content)
        self.assertIn("NOT CLAIMED", content)

    # --------------------------------------------------------------------------
    # Test 8: External Action Register Contents
    # --------------------------------------------------------------------------
    def test_external_action_register_items(self):
        """Verify that FINAL_EXTERNAL_ACTION_REGISTER.md lists required human actions."""
        fpath = os.path.join(self.release_dir, "FINAL_EXTERNAL_ACTION_REGISTER.md")
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn("Record Demo Video", content)
        self.assertIn("Export Pitch Deck PDF", content)
        self.assertIn("Official Portal Submission", content)

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
