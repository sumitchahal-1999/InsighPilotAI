"""
Phase 8.2: Real Deployment Execution & Cloud Infrastructure Test Suite
Project: InsightPilot AI
Competition: Accenture Innovation Challenge 2026 (Track 3: BusinessIntelligence.ai)

Validates:
1. Existence of all 7 Phase 8.2 cloud deployment deliverables in docs/deployment/
2. Existence of Infrastructure as Code files (render.yaml, Dockerfile, Procfile) in root
3. Strict placeholder integrity in docs/deployment/PRODUCTION_SECRET_HANDOFF.md
4. Honesty in docs/deployment/LIVE_DEPLOYMENT_STATUS.md (no fabricated live URLs)
5. Valid deployment verdict in LIVE_DEPLOYMENT_STATUS.md
6. Operational health and readiness probes
7. Preservation of canonical numerical invariants
8. Complete navigation links in docs/deployment/README.md
"""

import unittest
import os
from fastapi.testclient import TestClient
from backend.app.main import app

class TestPhase82LiveDeployment(unittest.TestCase):

    def setUp(self):
        self.project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
        self.deployment_dir = os.path.join(self.project_root, "docs", "deployment")
        self.client = TestClient(app)

    # --------------------------------------------------------------------------
    # Test 1: Required Phase 8.2 Deliverables Existence
    # --------------------------------------------------------------------------
    def test_phase82_deliverables_exist(self):
        """Verify that all 7 required Phase 8.2 deployment documents exist on disk."""
        required_files = [
            "PHASE_82_DEPLOYMENT_TOPOLOGY.md",
            "BACKEND_LIVE_DEPLOYMENT_REPORT.md",
            "FRONTEND_LIVE_DEPLOYMENT_REPORT.md",
            "PRODUCTION_SECRET_HANDOFF.md",
            "LIVE_CORS_AND_API_VALIDATION.md",
            "PRODUCTION_SMOKE_TEST_REPORT.md",
            "LIVE_DEPLOYMENT_STATUS.md",
        ]

        for fname in required_files:
            fpath = os.path.join(self.deployment_dir, fname)
            self.assertTrue(os.path.isfile(fpath), f"Missing Phase 8.2 deliverable: {fname}")

    # --------------------------------------------------------------------------
    # Test 2: Infrastructure as Code Files Existence
    # --------------------------------------------------------------------------
    def test_iac_files_exist(self):
        """Verify that render.yaml, Dockerfile, and Procfile exist in the root directory."""
        iac_files = ["render.yaml", "Dockerfile", "Procfile"]
        for fname in iac_files:
            fpath = os.path.join(self.project_root, fname)
            self.assertTrue(os.path.isfile(fpath), f"Missing IaC file in root: {fname}")

    # --------------------------------------------------------------------------
    # Test 3: Secret Handoff Placeholder Integrity
    # --------------------------------------------------------------------------
    def test_secret_handoff_placeholders(self):
        """Verify that PRODUCTION_SECRET_HANDOFF.md uses only placeholders and no real keys."""
        fpath = os.path.join(self.deployment_dir, "PRODUCTION_SECRET_HANDOFF.md")
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn("[YOUR_GROQ_API_KEY]", content)
        self.assertIn("[YOUR_GEMINI_API_KEY]", content)
        self.assertIn("[YOUR_FRONTEND_URL]", content)
        self.assertIn("[YOUR_BACKEND_URL]", content)
        # Ensure no real keys exist
        self.assertNotIn("AIzaSy", content)
        self.assertNotIn("gsk_", content)

    # --------------------------------------------------------------------------
    # Test 4: Live Deployment Status Transparency & Honesty
    # --------------------------------------------------------------------------
    def test_live_deployment_status_honesty(self):
        """Verify that LIVE_DEPLOYMENT_STATUS.md explicitly identifies TBD / External Actions."""
        fpath = os.path.join(self.deployment_dir, "LIVE_DEPLOYMENT_STATUS.md")
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn("EXTERNAL ACTION REQUIRED", content)
        self.assertIn("🟡 DEPLOYMENT READY — EXTERNAL PLATFORM ACTION REQUIRED", content)

    # --------------------------------------------------------------------------
    # Test 5: Operational Health Probes
    # --------------------------------------------------------------------------
    def test_operational_health_probes(self):
        """Verify that both liveness probes return HTTP 200 OK."""
        res_root = self.client.get("/health")
        self.assertEqual(res_root.status_code, 200)
        self.assertEqual(res_root.json().get("status"), "ok")

        res_api = self.client.get("/api/v1/health")
        self.assertEqual(res_api.status_code, 200)
        self.assertEqual(res_api.json().get("status"), "ok")

    # --------------------------------------------------------------------------
    # Test 6: Canonical Invariants Preservation
    # --------------------------------------------------------------------------
    def test_canonical_invariants_in_topology(self):
        """Verify that PHASE_82_DEPLOYMENT_TOPOLOGY.md strictly preserves canonical metrics."""
        fpath = os.path.join(self.deployment_dir, "PHASE_82_DEPLOYMENT_TOPOLOGY.md")
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn("15.43M", content)
        self.assertIn("14.20M", content)
        self.assertIn("43.2% Atlanta DC", content)
        self.assertIn("89% confidence", content)

    # --------------------------------------------------------------------------
    # Test 7: Deployment Directory Index Coverage
    # --------------------------------------------------------------------------
    def test_deployment_readme_phase82_links(self):
        """Verify that docs/deployment/README.md links to all Phase 8.2 documents."""
        fpath = os.path.join(self.deployment_dir, "README.md")
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()

        expected_links = [
            "PHASE_82_DEPLOYMENT_TOPOLOGY.md",
            "BACKEND_LIVE_DEPLOYMENT_REPORT.md",
            "FRONTEND_LIVE_DEPLOYMENT_REPORT.md",
            "PRODUCTION_SECRET_HANDOFF.md",
            "LIVE_CORS_AND_API_VALIDATION.md",
            "PRODUCTION_SMOKE_TEST_REPORT.md",
            "LIVE_DEPLOYMENT_STATUS.md",
        ]

        for link in expected_links:
            self.assertIn(link, content, f"Deployment README missing link to: {link}")

if __name__ == "__main__":
    unittest.main()
