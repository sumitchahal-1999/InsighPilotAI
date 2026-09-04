"""
Phase 8.6: Final Go-Live Cloud Provisioning & Production Handoff Test Suite
Project: InsightPilot AI
Competition: Accenture Innovation Challenge 2026 (Track 3: BusinessIntelligence.ai)

Validates:
1. Existence of all required Phase 8.6 deployment runbooks and handoff deliverables in docs/operations/
2. Truthful URL representation in PRODUCTION_URL_REGISTRY.md (pending cloud URLs labeled accurately)
3. Final handoff verdict consistency in FINAL_PRODUCTION_HANDOFF.md (CONDITIONAL GO)
4. Preservation of canonical invariants across Phase 8.6 deployment documentation
5. Operational health probes (/health and /api/v1/demo/readiness)
6. Complete navigation coverage in docs/operations/README.md
"""

import unittest
import os
from fastapi.testclient import TestClient
from backend.app.main import app

class TestPhase86ProductionHandoff(unittest.TestCase):

    def setUp(self):
        self.project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
        self.operations_dir = os.path.join(self.project_root, "docs", "operations")
        self.client = TestClient(app)

    # --------------------------------------------------------------------------
    # Test 1: Required Phase 8.6 Deliverables Existence
    # --------------------------------------------------------------------------
    def test_phase86_deliverables_exist(self):
        """Verify that all required Phase 8.6 deployment runbooks and handoff documents exist."""
        required_files = [
            "RENDER_DEPLOYMENT_RUNBOOK.md",
            "VERCEL_DEPLOYMENT_RUNBOOK.md",
            "LIVE_PRODUCTION_SMOKE_TEST.md",
            "LIVE_PRODUCTION_JOURNEY_VALIDATION.md",
            "LIVE_PRODUCTION_SECURITY_AUDIT.md",
            "PRODUCTION_URL_REGISTRY.md",
            "FINAL_PRODUCTION_HANDOFF.md",
            "README.md",
        ]

        for fname in required_files:
            fpath = os.path.join(self.operations_dir, fname)
            self.assertTrue(os.path.isfile(fpath), f"Missing Phase 8.6 deliverable: {fname}")

    # --------------------------------------------------------------------------
    # Test 2: Truthful URL Representation in Registry
    # --------------------------------------------------------------------------
    def test_truthful_url_representation(self):
        """Verify that PRODUCTION_URL_REGISTRY.md does not falsely claim cloud deployment."""
        fpath = os.path.join(self.operations_dir, "PRODUCTION_URL_REGISTRY.md")
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()

        # Git repository must be verified
        self.assertIn("https://github.com/ayus1234/InsighPilotAI.git", content)
        self.assertIn("STATUS: VERIFIED", content)

        # Unprovisioned cloud URLs must be marked pending
        self.assertIn("PENDING EXTERNAL PLATFORM DEPLOYMENT", content)
        self.assertIn("TBD — RENDER DEPLOYMENT REQUIRED", content)
        self.assertIn("TBD — VERCEL DEPLOYMENT REQUIRED", content)

    # --------------------------------------------------------------------------
    # Test 3: Final Production Handoff Verdict Consistency
    # --------------------------------------------------------------------------
    def test_final_production_handoff_verdict(self):
        """Verify that FINAL_PRODUCTION_HANDOFF.md records CONDITIONAL GO."""
        fpath = os.path.join(self.operations_dir, "FINAL_PRODUCTION_HANDOFF.md")
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn("CONDITIONAL GO", content)
        self.assertIn("REPOSITORY READINESS 100% VERIFIED", content)
        self.assertIn("EXTERNAL CLOUD PLATFORM PROVISIONING ACTION REQUIRED", content)

    # --------------------------------------------------------------------------
    # Test 4: Canonical Invariants Preservation
    # --------------------------------------------------------------------------
    def test_canonical_invariants_in_phase86_docs(self):
        """Verify that Phase 8.6 documents preserve the locked canonical metrics."""
        fpath = os.path.join(self.operations_dir, "FINAL_PRODUCTION_HANDOFF.md")
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn("Deterministic systems own quantitative truth", content)
        self.assertIn("Atlanta DC Stockout", content)
        self.assertIn("43.2%", content)
        self.assertIn("+$484,000.00", content)
        self.assertIn("+$757,600.00", content)


    # --------------------------------------------------------------------------
    # Test 5: Local Health and Readiness Probes
    # --------------------------------------------------------------------------
    def test_health_and_readiness_probes(self):
        """Verify that /health and /api/v1/demo/readiness respond in healthy states."""
        res_health = self.client.get("/health")
        self.assertEqual(res_health.status_code, 200)
        self.assertEqual(res_health.json().get("status"), "ok")

        res_readiness = self.client.get("/api/v1/demo/readiness")
        self.assertEqual(res_readiness.status_code, 200)
        self.assertTrue(res_readiness.json().get("submission_ready"))

    # --------------------------------------------------------------------------
    # Test 6: Operations README Navigation Links Integrity
    # --------------------------------------------------------------------------
    def test_operations_readme_links(self):
        """Verify that docs/operations/README.md links to all Phase 8.6 documents."""
        fpath = os.path.join(self.operations_dir, "README.md")
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()

        expected_links = [
            "RENDER_DEPLOYMENT_RUNBOOK.md",
            "VERCEL_DEPLOYMENT_RUNBOOK.md",
            "LIVE_PRODUCTION_SMOKE_TEST.md",
            "LIVE_PRODUCTION_JOURNEY_VALIDATION.md",
            "LIVE_PRODUCTION_SECURITY_AUDIT.md",
            "PRODUCTION_URL_REGISTRY.md",
            "FINAL_PRODUCTION_HANDOFF.md",
        ]

        for link in expected_links:
            self.assertIn(link, content, f"Operations README missing link to: {link}")

if __name__ == "__main__":
    unittest.main()
