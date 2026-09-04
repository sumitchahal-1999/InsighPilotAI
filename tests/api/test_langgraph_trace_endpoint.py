"""
InsightPilot AI — LangGraph Trace API Endpoint Integration Tests
Tests GET /api/v1/investigations/{kpi_id}/langgraph-trace contract, schema validation, persona switching, and secret safety.
"""

import unittest
from fastapi.testclient import TestClient
from backend.app.main import app

class TestLangGraphTraceEndpoint(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    def test_get_langgraph_trace_success_cfo(self):
        """Tests successful retrieval of live LangGraph trace for CFO persona."""
        response = self.client.get(
            "/api/v1/investigations/north_america_east_revenue/langgraph-trace",
            params={"region": "NA-East", "persona_id": "CFO"}
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()

        # 1. Root structure verification
        self.assertEqual(data["kpi_id"], "north_america_east_revenue")
        self.assertEqual(data["region"], "NA-East")
        self.assertEqual(data["persona_id"], "CFO")
        self.assertEqual(data["status"], "COMPLETED")
        self.assertIn("started_at", data)
        self.assertIn("completed_at", data)
        self.assertGreater(data["total_duration_ms"], 0.0)

        # 2. Node trace array verification
        nodes = data.get("nodes", [])
        self.assertGreaterEqual(len(nodes), 8)
        node_names = [n["node_name"] for n in nodes]
        self.assertIn("load_kpi_node", node_names)
        self.assertIn("calculate_movement_node", node_names)
        self.assertIn("identify_drivers_node", node_names)
        self.assertIn("retrieve_evidence_node", node_names)
        self.assertIn("validate_evidence_node", node_names)
        self.assertIn("calculate_confidence_node", node_names)

        # Check structure of a node trace
        first_node = nodes[0]
        self.assertIn("display_name", first_node)
        self.assertIn("role", first_node)
        self.assertIn("status", first_node)
        self.assertIn("duration_ms", first_node)
        self.assertIn("summary", first_node)
        self.assertIn("metrics", first_node)

        # 3. Deterministic summary numerical verification
        det = data["deterministic_summary"]
        self.assertAlmostEqual(det["previous_value"], 15430000.06, delta=0.01)
        self.assertAlmostEqual(det["current_value"], 14200000.05, delta=0.01)
        self.assertAlmostEqual(det["variance_amount"], -1230000.01, delta=0.01)
        self.assertAlmostEqual(det["percent_change"], -7.97, places=2)
        self.assertEqual(det["drivers_count"], 4)

        # 4. Confidence & Abstention verification
        conf = data["confidence"]
        self.assertGreaterEqual(conf.get("overall_confidence", 0), 65)
        self.assertFalse(data["abstention"])

        # 5. AI Explanation verification
        explanation = data.get("ai_explanation")
        self.assertIsNotNone(explanation)
        self.assertIn("summary", explanation)

    def test_get_langgraph_trace_regional_sales_manager(self):
        """Tests persona adaptation for Regional Sales Manager without altering quantitative metrics."""
        response = self.client.get(
            "/api/v1/investigations/north_america_east_revenue/langgraph-trace",
            params={"region": "NA-East", "persona_id": "REGIONAL_SALES_MANAGER"}
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["persona_id"], "REGIONAL_SALES_MANAGER")

        # Confirm numerical truth remains unchanged across personas
        det = data["deterministic_summary"]
        self.assertAlmostEqual(det["previous_value"], 15430000.06, delta=0.01)
        self.assertAlmostEqual(det["current_value"], 14200000.05, delta=0.01)
        self.assertAlmostEqual(det["variance_amount"], -1230000.01, delta=0.01)

    def test_unknown_kpi_returns_404(self):
        """Tests that an unsupported KPI returns a clean 404 response."""
        response = self.client.get("/api/v1/investigations/unknown_kpi_metric/langgraph-trace")
        self.assertEqual(response.status_code, 404)

    def test_zero_secret_leakage(self):
        """Tests that response body never leaks API keys or secret tokens."""
        response = self.client.get(
            "/api/v1/investigations/north_america_east_revenue/langgraph-trace",
            params={"region": "NA-East", "persona_id": "CFO"}
        )
        raw_text = response.text.lower()
        self.assertNotIn("api_key", raw_text)
        self.assertNotIn("gsk_", raw_text)
        self.assertNotIn("ai_za", raw_text)
        self.assertNotIn("secret", raw_text)
        self.assertNotIn("bearer", raw_text)

if __name__ == "__main__":
    unittest.main()
