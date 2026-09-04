"""
InsightPilot AI — Phase 5.9: Submission Readiness Test Suite
Validates the dynamic competition readiness audit, health checks, and subsystem diagnostics.
"""

import unittest
from fastapi.testclient import TestClient
from backend.app.main import app
from ai.demo.readiness import SubmissionReadinessService


class TestSubmissionReadiness(unittest.TestCase):
    """Subsystem health and submission readiness test suite."""

    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    # -------------------------------------------------------------------------
    # 1. Direct Service Evaluation
    # -------------------------------------------------------------------------
    def test_submission_readiness_service_direct(self):
        """Verifies that the SubmissionReadinessService passes all dynamic subsystem checks."""
        report = SubmissionReadinessService.evaluate_readiness()

        self.assertTrue(report.submission_ready)
        self.assertTrue(report.subsystems["database_ready"])
        self.assertTrue(report.subsystems["analytics_parity"])
        self.assertTrue(report.subsystems["evidence_lineage_ready"])
        self.assertTrue(report.subsystems["confidence_engine_ready"])
        self.assertTrue(report.subsystems["abstention_ready"])
        self.assertTrue(report.subsystems["ai_orchestration_ready"])
        self.assertTrue(report.subsystems["fallback_ready"])
        self.assertTrue(report.subsystems["decision_graph_ready"])
        self.assertTrue(report.subsystems["recommendation_ready"])
        self.assertTrue(report.subsystems["simulation_ready"])
        self.assertTrue(report.subsystems["backend_ready"])
        self.assertTrue(report.subsystems["frontend_build_ready"])

    # -------------------------------------------------------------------------
    # 2. RESTful Endpoint Contract
    # -------------------------------------------------------------------------
    def test_readiness_endpoint(self):
        """Verifies that GET /api/v1/demo/readiness returns a 200 with complete audit report."""
        res = self.client.get("/api/v1/demo/readiness")
        self.assertEqual(res.status_code, 200)
        data = res.json()

        self.assertTrue(data["submission_ready"])
        self.assertIn("timestamp", data)
        self.assertGreaterEqual(len(data["subsystems"]), 10)
        self.assertGreaterEqual(len(data["diagnostics"]), 10)


if __name__ == "__main__":
    unittest.main()
