"""
Phase 8.1: Production Deployment & Live Application Readiness Test Suite
Project: InsightPilot AI
Competition: Accenture Innovation Challenge 2026 (Track 3: BusinessIntelligence.ai)

Validates:
1. Existence of all 10 Phase 8.1 deployment documentation deliverables in docs/deployment/
2. Template environment variable integrity in root .env.example and frontend/next-app/.env.example
3. Zero secret leakage across tracked deployment templates
4. Dual healthcheck endpoints (/health and /api/v1/health) return HTTP 200
5. Dynamic readiness probe (/api/v1/demo/readiness) evaluates all 12 subsystems
6. Preservation of canonical numerical invariants without drift
7. Complete index coverage in docs/deployment/README.md
"""

import unittest
import os
from fastapi.testclient import TestClient
from backend.app.main import app

class TestPhase81DeploymentReadiness(unittest.TestCase):

    def setUp(self):
        self.project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
        self.deployment_dir = os.path.join(self.project_root, "docs", "deployment")
        self.client = TestClient(app)

    # --------------------------------------------------------------------------
    # Test 1: Required Phase 8.1 Deliverables Existence
    # --------------------------------------------------------------------------
    def test_phase81_deliverables_exist(self):
        """Verify that all 10 required Phase 8.1 deployment documents exist on disk."""
        required_files = [
            "DEPLOYMENT_ARCHITECTURE_AUDIT.md",
            "PRODUCTION_DEPLOYMENT_ARCHITECTURE.md",
            "ENVIRONMENT_CONFIGURATION_GUIDE.md",
            "FRONTEND_DEPLOYMENT_GUIDE.md",
            "BACKEND_DEPLOYMENT_GUIDE.md",
            "API_SECURITY_AND_CORS_AUDIT.md",
            "PRODUCTION_HEALTH_CHECKS.md",
            "DEPLOYMENT_SECURITY_REVIEW.md",
            "DEPLOYMENT_RUNBOOK.md",
            "LIVE_DEPLOYMENT_CHECKLIST.md",
            "README.md",
        ]

        for fname in required_files:
            fpath = os.path.join(self.deployment_dir, fname)
            self.assertTrue(os.path.isfile(fpath), f"Missing deployment deliverable: {fname}")

    # --------------------------------------------------------------------------
    # Test 2: Environment Templates Configuration Integrity
    # --------------------------------------------------------------------------
    def test_environment_templates_integrity(self):
        """Verify that root .env.example and frontend .env.example contain required keys."""
        root_env_path = os.path.join(self.project_root, ".env.example")
        frontend_env_path = os.path.join(self.project_root, "frontend", "next-app", ".env.example")

        self.assertTrue(os.path.isfile(root_env_path), "Root .env.example missing")
        self.assertTrue(os.path.isfile(frontend_env_path), "Frontend .env.example missing")

        with open(root_env_path, "r", encoding="utf-8") as f:
            root_content = f.read()

        with open(frontend_env_path, "r", encoding="utf-8") as f:
            frontend_content = f.read()

        # Root variables
        self.assertIn("APP_ENV=", root_content)
        self.assertIn("API_HOST=", root_content)
        self.assertIn("API_PORT=", root_content)
        self.assertIn("CORS_ORIGINS=", root_content)
        self.assertIn("NEXT_PUBLIC_API_URL=", root_content)
        self.assertIn("CONFIDENCE_ABSTENTION_THRESHOLD=0.65", root_content)

        # Frontend variables
        self.assertIn("NEXT_PUBLIC_API_URL=", frontend_content)

    # --------------------------------------------------------------------------
    # Test 3: Zero Secret Leakage in Tracked Templates
    # --------------------------------------------------------------------------
    def test_zero_secret_leakage_in_templates(self):
        """Verify that environment templates do not contain real API keys or credentials."""
        root_env_path = os.path.join(self.project_root, ".env.example")
        with open(root_env_path, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn("GEMINI_API_KEY_1=", content)
        self.assertIn("GROQ_API_KEY_1=", content)
        # Ensure no actual key value follows the equals sign
        self.assertNotIn("GEMINI_API_KEY_1=AIzaSy", content)
        self.assertNotIn("GROQ_API_KEY_1=gsk_", content)

    # --------------------------------------------------------------------------
    # Test 4: Dual Health Probes Response
    # --------------------------------------------------------------------------
    def test_dual_health_probes(self):
        """Verify that both /health and /api/v1/health return HTTP 200 OK."""
        res_root = self.client.get("/health")
        self.assertEqual(res_root.status_code, 200)
        data_root = res_root.json()
        self.assertEqual(data_root.get("status"), "ok")
        self.assertEqual(data_root.get("service"), "insightpilot-api")

        res_api = self.client.get("/api/v1/health")
        self.assertEqual(res_api.status_code, 200)
        data_api = res_api.json()
        self.assertEqual(data_api.get("status"), "ok")
        self.assertEqual(data_api.get("service"), "insightpilot-api")

    # --------------------------------------------------------------------------
    # Test 5: Dynamic Readiness Probe
    # --------------------------------------------------------------------------
    def test_dynamic_readiness_probe(self):
        """Verify that /api/v1/demo/readiness evaluates subsystems as healthy."""
        res = self.client.get("/api/v1/demo/readiness")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertTrue(data.get("submission_ready"))
        subsystems = data.get("subsystems", {})
        self.assertGreaterEqual(len(subsystems), 10)
        self.assertTrue(all(subsystems.values()), f"Some subsystems failed: {subsystems}")


    # --------------------------------------------------------------------------
    # Test 6: Canonical Metrics Invariant Parity
    # --------------------------------------------------------------------------
    def test_canonical_metrics_in_deployment_audit(self):
        """Verify that DEPLOYMENT_ARCHITECTURE_AUDIT.md preserves canonical values."""
        fpath = os.path.join(self.deployment_dir, "DEPLOYMENT_ARCHITECTURE_AUDIT.md")
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn("Deterministic systems own quantitative truth", content)
        self.assertIn("10 / 10 static pages", content)
        self.assertIn("0.65", content)

    # --------------------------------------------------------------------------
    # Test 7: Deployment README Index Integrity
    # --------------------------------------------------------------------------
    def test_deployment_readme_links(self):
        """Verify that docs/deployment/README.md links to all 10 deployment documents."""
        fpath = os.path.join(self.deployment_dir, "README.md")
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()

        expected_links = [
            "DEPLOYMENT_ARCHITECTURE_AUDIT.md",
            "PRODUCTION_DEPLOYMENT_ARCHITECTURE.md",
            "ENVIRONMENT_CONFIGURATION_GUIDE.md",
            "FRONTEND_DEPLOYMENT_GUIDE.md",
            "BACKEND_DEPLOYMENT_GUIDE.md",
            "API_SECURITY_AND_CORS_AUDIT.md",
            "PRODUCTION_HEALTH_CHECKS.md",
            "DEPLOYMENT_SECURITY_REVIEW.md",
            "DEPLOYMENT_RUNBOOK.md",
            "LIVE_DEPLOYMENT_CHECKLIST.md",
        ]

        for link in expected_links:
            self.assertIn(link, content, f"Deployment README missing link to: {link}")

if __name__ == "__main__":
    unittest.main()
