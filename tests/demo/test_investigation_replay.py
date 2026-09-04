"""
InsightPilot AI — Phase 5.9: Investigation Replay Test Suite
Validates the execution lifecycle replay endpoint, node classification, latency tracking, and credential safety.
"""

import unittest
from fastapi.testclient import TestClient
from backend.app.main import app


class TestInvestigationReplay(unittest.TestCase):
    """Execution replay and lifecycle observability tests."""

    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)
        cls.kpi_id = "north_america_east_revenue"

    # -------------------------------------------------------------------------
    # 1. Investigation Replay Contract & Structure
    # -------------------------------------------------------------------------
    def test_investigation_replay_endpoint(self):
        """Verifies that GET /api/v1/demo/replay/{kpi_id} returns an ordered, classified execution replay."""
        res = self.client.get(f"/api/v1/demo/replay/{self.kpi_id}?persona=CFO")
        self.assertEqual(res.status_code, 200)
        data = res.json()

        self.assertEqual(data["kpi_id"], self.kpi_id)
        self.assertGreaterEqual(data["total_steps"], 10)
        self.assertGreater(data["total_duration_ms"], 0.0)

        # Check step ordering and properties
        steps = data["replay_nodes"]
        self.assertEqual(len(steps), data["total_steps"])
        for idx, step in enumerate(steps, start=1):
            self.assertEqual(step["step_number"], idx)
            self.assertIn(step["classification"], ["DETERMINISTIC", "AI_ORCHESTRATION", "SAFETY_GUARD"])
            self.assertEqual(step["status"], "COMPLETED")
            self.assertGreaterEqual(step["duration_ms"], 0.0)

        # Check specific node classifications
        node_names = [s["node_name"] for s in steps]
        self.assertIn("load_kpi_node", node_names)
        self.assertIn("calculate_movement_node", node_names)
        self.assertIn("identify_drivers_node", node_names)
        self.assertIn("validate_evidence_node", node_names)
        self.assertIn("calculate_confidence_node", node_names)
        self.assertIn("ai_invocation_node", node_names)

        # Verify load_kpi_node is DETERMINISTIC
        load_kpi_step = next(s for s in steps if s["node_name"] == "load_kpi_node")
        self.assertEqual(load_kpi_step["classification"], "DETERMINISTIC")

        # Verify validate_evidence_node is SAFETY_GUARD
        val_step = next(s for s in steps if s["node_name"] == "validate_evidence_node")
        self.assertEqual(val_step["classification"], "SAFETY_GUARD")

        # Verify ai_invocation_node is AI_ORCHESTRATION
        ai_step = next(s for s in steps if s["node_name"] == "ai_invocation_node")
        self.assertEqual(ai_step["classification"], "AI_ORCHESTRATION")

    # -------------------------------------------------------------------------
    # 2. Secret Isolation in Replay Traces
    # -------------------------------------------------------------------------
    def test_zero_secret_leakage_in_replay(self):
        """Ensures that execution traces never reveal API keys, tokens, or credentials."""
        res = self.client.get(f"/api/v1/demo/replay/{self.kpi_id}?persona=CFO")
        data_text = res.text

        self.assertNotIn("gsk_", data_text)
        self.assertNotIn("AIzaSy", data_text)
        self.assertNotIn("Bearer ", data_text)
        self.assertNotIn("Authorization", data_text)


if __name__ == "__main__":
    unittest.main()
