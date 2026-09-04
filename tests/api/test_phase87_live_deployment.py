"""
Phase 8.7: Live Cloud Deployment, Production Validation & URL Activation Test Suite
Project: InsightPilot AI
Competition: Accenture Innovation Challenge 2026 (Track 3: BusinessIntelligence.ai)

Validates:
1. Existence of all required Phase 8.7 live deployment audit deliverables in docs/operations/
2. Strict deployment status categorization (LOCAL VERIFIED, PENDING EXTERNAL DEPLOYMENT)
3. No fictional production URLs represented as verified in PRODUCTION_URL_REGISTRY.md
4. Authoritative Phase 8.7 decision consistency in PHASE_87_LIVE_GO_LIVE_DECISION.md (CONDITIONAL GO)
5. Preservation of canonical invariants across Phase 8.7 documentation
6. Operational health and readiness probes
7. Complete navigation coverage in docs/operations/README.md
"""

import unittest
import os
from fastapi.testclient import TestClient
from backend.app.main import app

class TestPhase87LiveDeployment(unittest.TestCase):

    def setUp(self):
        self.project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
        self.operations_dir = os.path.join(self.project_root, "docs", "operations")
        self.client = TestClient(app)

    # --------------------------------------------------------------------------
    # Test 1: Required Phase 8.7 Deliverables Existence
    # --------------------------------------------------------------------------
    def test_phase87_deliverables_exist(self):
        """Verify that all required Phase 8.7 documents exist on disk."""
        required_files = [
            "LIVE_CLOUD_DEPLOYMENT_EXECUTION.md",
            "PRODUCTION_URL_REGISTRY.md",
            "LIVE_BACKEND_VALIDATION_REPORT.md",
            "LIVE_FRONTEND_VALIDATION_REPORT.md",
            "LIVE_7_SCREEN_JOURNEY_REPORT.md",
            "PRODUCTION_CORS_VALIDATION.md",
            "LIVE_SECURITY_VERIFICATION_REPORT.md",
            "LIVE_DEGRADED_MODE_VALIDATION.md",
            "PHASE_87_LIVE_GO_LIVE_DECISION.md",
            "README.md",
        ]

        for fname in required_files:
            fpath = os.path.join(self.operations_dir, fname)
            self.assertTrue(os.path.isfile(fpath), f"Missing Phase 8.7 deliverable: {fname}")

    # --------------------------------------------------------------------------
    # Test 2: Strict Deployment Status Categorization in Registry
    # --------------------------------------------------------------------------
    def test_strict_status_categorization(self):
        """Verify that PRODUCTION_URL_REGISTRY.md strictly categorizes endpoint statuses."""
        fpath = os.path.join(self.operations_dir, "PRODUCTION_URL_REGISTRY.md")
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()

        # Git repository and local services must be marked LOCAL VERIFIED
        self.assertIn("LOCAL VERIFIED", content)
        self.assertIn("https://github.com/ayus1234/InsighPilotAI.git", content)

        # Unprovisioned cloud services must be marked PENDING EXTERNAL DEPLOYMENT
        self.assertIn("PENDING EXTERNAL DEPLOYMENT", content)
        self.assertIn("TBD — RENDER DEPLOYMENT REQUIRED", content)
        self.assertIn("TBD — VERCEL DEPLOYMENT REQUIRED", content)

    # --------------------------------------------------------------------------
    # Test 3: Phase 8.7 Go-Live Verdict Consistency
    # --------------------------------------------------------------------------
    def test_phase87_go_live_verdict(self):
        """Verify that PHASE_87_LIVE_GO_LIVE_DECISION.md records CONDITIONAL GO."""
        fpath = os.path.join(self.operations_dir, "PHASE_87_LIVE_GO_LIVE_DECISION.md")
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn("CONDITIONAL GO", content)
        self.assertIn("EXTERNAL DEPLOYMENT ACTION REQUIRED", content)
        self.assertIn("REPOSITORY & LOCAL READINESS 100% VERIFIED", content)

    # --------------------------------------------------------------------------
    # Test 4: Canonical Invariants Preservation
    # --------------------------------------------------------------------------
    def test_canonical_invariants_in_phase87_decision(self):
        """Verify that PHASE_87_LIVE_GO_LIVE_DECISION.md preserves locked metrics."""
        fpath = os.path.join(self.operations_dir, "PHASE_87_LIVE_GO_LIVE_DECISION.md")
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
        """Verify that local /health and /api/v1/demo/readiness respond successfully."""
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
        """Verify that docs/operations/README.md links to all Phase 8.7 documents."""
        fpath = os.path.join(self.operations_dir, "README.md")
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()

        expected_links = [
            "LIVE_CLOUD_DEPLOYMENT_EXECUTION.md",
            "LIVE_BACKEND_VALIDATION_REPORT.md",
            "LIVE_FRONTEND_VALIDATION_REPORT.md",
            "LIVE_7_SCREEN_JOURNEY_REPORT.md",
            "PRODUCTION_CORS_VALIDATION.md",
            "LIVE_SECURITY_VERIFICATION_REPORT.md",
            "LIVE_DEGRADED_MODE_VALIDATION.md",
            "PHASE_87_LIVE_GO_LIVE_DECISION.md",
        ]

        for link in expected_links:
            self.assertIn(link, content, f"Operations README missing link to: {link}")

if __name__ == "__main__":
    unittest.main()
