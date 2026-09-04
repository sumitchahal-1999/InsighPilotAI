"""
Phase 8.3: Production Observability, Reliability & Operational Resilience Test Suite
Project: InsightPilot AI
Competition: Accenture Innovation Challenge 2026 (Track 3: BusinessIntelligence.ai)

Validates:
1. Existence of all 10 Phase 8.3 observability deliverables in docs/observability/
2. Request correlation middleware generates X-Request-ID and measures latency (X-Response-Time-Ms)
3. Request correlation header forwarding (incoming X-Request-ID preserved in response)
4. Sanitized error responses without internal tracebacks or secrets
5. Operational health probes (/health and /api/v1/demo/readiness)
6. Preservation of canonical invariants in observability documentation
7. Complete navigation coverage in docs/observability/README.md
"""

import unittest
import os
from fastapi.testclient import TestClient
from backend.app.main import app

class TestPhase83ObservabilityReliability(unittest.TestCase):

    def setUp(self):
        self.project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
        self.observability_dir = os.path.join(self.project_root, "docs", "observability")
        self.client = TestClient(app)

    # --------------------------------------------------------------------------
    # Test 1: Required Phase 8.3 Deliverables Existence
    # --------------------------------------------------------------------------
    def test_phase83_deliverables_exist(self):
        """Verify that all 10 required Phase 8.3 observability documents exist on disk."""
        required_files = [
            "PRODUCTION_OBSERVABILITY_ARCHITECTURE.md",
            "HEALTH_AND_READINESS_MODEL.md",
            "PRODUCTION_ERROR_TAXONOMY.md",
            "LATENCY_AND_PERFORMANCE_BASELINE.md",
            "RELIABILITY_FAILURE_MODE_AUDIT.md",
            "RATE_LIMIT_AND_RESILIENCE_AUDIT.md",
            "UPTIME_MONITORING_HANDOFF.md",
            "OBSERVABILITY_SECURITY_POLICY.md",
            "PRODUCTION_OPERATIONS_RUNBOOK.md",
            "PHASE_83_OBSERVABILITY_STATUS.md",
            "README.md",
        ]

        for fname in required_files:
            fpath = os.path.join(self.observability_dir, fname)
            self.assertTrue(os.path.isfile(fpath), f"Missing Phase 8.3 deliverable: {fname}")

    # --------------------------------------------------------------------------
    # Test 2: Request Correlation Headers Generation
    # --------------------------------------------------------------------------
    def test_request_correlation_headers_generation(self):
        """Verify that API requests automatically receive X-Request-ID and X-Response-Time-Ms headers."""
        res = self.client.get("/health")
        self.assertEqual(res.status_code, 200)
        self.assertIn("X-Request-ID", res.headers)
        self.assertTrue(res.headers["X-Request-ID"].startswith("req_"))
        self.assertIn("X-Response-Time-Ms", res.headers)
        # Latency should be a valid floating-point string
        latency = float(res.headers["X-Response-Time-Ms"])
        self.assertGreaterEqual(latency, 0.0)

    # --------------------------------------------------------------------------
    # Test 3: Request Correlation Forwarding
    # --------------------------------------------------------------------------
    def test_request_correlation_forwarding(self):
        """Verify that an incoming X-Request-ID is preserved and echoed in response headers."""
        custom_id = "test_custom_correlation_id_999"
        res = self.client.get("/health", headers={"X-Request-ID": custom_id})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.headers.get("X-Request-ID"), custom_id)

    # --------------------------------------------------------------------------
    # Test 4: Error Sanitization & No Secret Leakage
    # --------------------------------------------------------------------------
    def test_error_sanitization(self):
        """Verify that error responses return clean JSON codes without tracebacks or file paths."""
        res = self.client.get("/api/v1/kpis/non_existent_kpi_id_123")
        self.assertEqual(res.status_code, 404)
        data = res.json()
        self.assertIn("error", data)
        self.assertEqual(data["error"].get("code"), "KPI_NOT_FOUND")
        # Ensure no system path leaks
        self.assertNotIn("c:\\Users\\", str(data).lower())
        self.assertNotIn("traceback", str(data).lower())
        # Ensure correlation header still attached
        self.assertIn("X-Request-ID", res.headers)

    # --------------------------------------------------------------------------
    # Test 5: Health and Readiness Probes
    # --------------------------------------------------------------------------
    def test_health_and_readiness_probes(self):
        """Verify that liveness probe and readiness probe return healthy statuses."""
        res_health = self.client.get("/health")
        self.assertEqual(res_health.status_code, 200)
        self.assertEqual(res_health.json().get("status"), "ok")

        res_readiness = self.client.get("/api/v1/demo/readiness")
        self.assertEqual(res_readiness.status_code, 200)
        self.assertTrue(res_readiness.json().get("submission_ready"))

    # --------------------------------------------------------------------------
    # Test 6: Canonical Invariants in Observability Architecture
    # --------------------------------------------------------------------------
    def test_canonical_invariants_in_observability(self):
        """Verify that PRODUCTION_OBSERVABILITY_ARCHITECTURE.md preserves canonical values."""
        fpath = os.path.join(self.observability_dir, "PRODUCTION_OBSERVABILITY_ARCHITECTURE.md")
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn("Deterministic systems own quantitative truth", content)
        self.assertIn("6-Factor Confidence Scoring (89%)", content)
        self.assertIn("4-Factor Variance Contribution", content)

    # --------------------------------------------------------------------------
    # Test 7: Observability README Links Integrity
    # --------------------------------------------------------------------------
    def test_observability_readme_links(self):
        """Verify that docs/observability/README.md links to all 10 documents."""
        fpath = os.path.join(self.observability_dir, "README.md")
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()

        expected_links = [
            "PRODUCTION_OBSERVABILITY_ARCHITECTURE.md",
            "HEALTH_AND_READINESS_MODEL.md",
            "PRODUCTION_ERROR_TAXONOMY.md",
            "LATENCY_AND_PERFORMANCE_BASELINE.md",
            "RELIABILITY_FAILURE_MODE_AUDIT.md",
            "RATE_LIMIT_AND_RESILIENCE_AUDIT.md",
            "UPTIME_MONITORING_HANDOFF.md",
            "OBSERVABILITY_SECURITY_POLICY.md",
            "PRODUCTION_OPERATIONS_RUNBOOK.md",
            "PHASE_83_OBSERVABILITY_STATUS.md",
        ]

        for link in expected_links:
            self.assertIn(link, content, f"Observability README missing link to: {link}")

if __name__ == "__main__":
    unittest.main()
