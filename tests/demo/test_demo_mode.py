"""
InsightPilot AI — Phase 5.9: Competition Demo Mode & Narrative Test Suite
Verifies the complete end-to-end demo execution bundle, 10-beat narrative structure,
deterministic numerical truth preservation, and provider source attribution.
"""

import unittest
from fastapi.testclient import TestClient
from backend.app.main import app
from ai.demo.narrative import DemoNarrativeBuilder


class TestDemoMode(unittest.TestCase):
    """Execution and validation tests for the competition demo bundle and storyboard narrative."""

    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)
        cls.kpi_id = "north_america_east_revenue"

    # -------------------------------------------------------------------------
    # 1. Unified Competition Demo Bundle API Contract
    # -------------------------------------------------------------------------
    def test_canonical_demo_investigation_endpoint(self):
        """Verifies that GET /api/v1/demo/investigation/{kpi_id} returns a complete, valid bundle."""
        res = self.client.get(f"/api/v1/demo/investigation/{self.kpi_id}?persona=CFO")
        self.assertEqual(res.status_code, 200)
        data = res.json()

        # Invariants
        self.assertEqual(data["kpi_id"], self.kpi_id)
        self.assertEqual(data["persona"], "CFO")
        self.assertAlmostEqual(data["movement"]["baseline_value"], 15430000.06, places=2)
        self.assertAlmostEqual(data["movement"]["target_value"], 14200000.05, places=2)
        self.assertAlmostEqual(data["movement"]["variance"], -1230000.01, places=2)
        self.assertAlmostEqual(data["movement"]["percent_change"], -7.97, places=2)

        # Causal Drivers
        self.assertEqual(len(data["drivers"]), 4)
        self.assertEqual(data["drivers"][0]["driver_id"], "atlanta_dc_stockout")
        self.assertAlmostEqual(data["drivers"][0]["contribution_pct"], 43.2, places=1)
        self.assertAlmostEqual(data["drivers"][0]["impact_usd"], -550000.0, places=2)

        # Confidence & Abstention
        self.assertEqual(data["confidence"]["overall_confidence"], 89)
        self.assertFalse(data["abstention"]["abstained"])

        # Decision Graph Summary
        self.assertEqual(data["decision_graph_summary"]["total_columns"], 6)
        self.assertEqual(data["decision_graph_summary"]["total_nodes_count"], 14)
        self.assertEqual(data["decision_graph_summary"]["total_edges_count"], 17)

        # Recommendations & Simulation
        self.assertEqual(len(data["recommendations"]), 4)
        self.assertIn("20,000", data["recommendations"][0]["action"])
        self.assertAlmostEqual(data["recommendations"][0]["expected_impact"]["revenue_recovery_usd"], 484000.0, places=0)
        self.assertAlmostEqual(data["simulation_summary"]["estimated_recovery"]["revenue_recovery_usd"], 341422.91, places=2)

        # AI Source Attribution
        self.assertIn("AI Source:", data["ai_source_indicator"])

        # Integrity Report
        self.assertTrue(data["integrity_report"]["demo_ready"])
        self.assertEqual(data["integrity_report"]["passed_checks"], 13)
        self.assertEqual(data["integrity_report"]["failed_checks"], 0)

    # -------------------------------------------------------------------------
    # 2. 10-Beat Demo Storyboard Narrative Structure
    # -------------------------------------------------------------------------
    def test_10_beat_demo_narrative_completeness(self):
        """Verifies that the demo narrative produces all 10 canonical story beats with exact numbers."""
        res = self.client.get(f"/api/v1/demo/investigation/{self.kpi_id}?persona=CFO")
        data = res.json()
        narrative = data["demo_narrative"]

        self.assertEqual(narrative["total_beats"], 10)
        self.assertEqual(len(narrative["beats"]), 10)

        beat_names = [b["beat_name"] for b in narrative["beats"]]
        expected_beats = [
            "business_problem",
            "kpi_detection",
            "investigation_orchestration",
            "driver_decomposition",
            "evidence_corroboration",
            "grounded_explanation",
            "decision_graph",
            "recommendation_actions",
            "what_if_simulation",
            "executive_briefing"
        ]
        self.assertEqual(beat_names, expected_beats)

        # Verify Beat 1 (Business Problem)
        beat1 = narrative["beats"][0]
        self.assertEqual(beat1["screen_id"], "screen_1_command_center")
        self.assertIn("$15,430,000.06", beat1["summary"])
        self.assertIn("$14,200,000.05", beat1["summary"])
        self.assertIn("-7.97%", beat1["summary"])

        # Verify Beat 4 (Root Cause)
        beat4 = narrative["beats"][3]
        self.assertEqual(beat4["screen_id"], "screen_3_root_cause")
        self.assertIn("Atlanta DC Stockout", beat4["summary"])
        self.assertIn("43.2%", beat4["summary"])

        # Verify Beat 9 (Simulation)
        beat9 = narrative["beats"][8]
        self.assertEqual(beat9["screen_id"], "screen_6_recommendations")
        self.assertIn("79.4% to 90.0%", beat9["summary"])
        self.assertIn("$341,422.91", beat9["summary"])

    # -------------------------------------------------------------------------
    # 3. Persona Invariance in Demo Flow
    # -------------------------------------------------------------------------
    def test_demo_persona_numerical_invariance(self):
        """Ensures that CFO and Regional Sales Manager demo responses maintain 100% quantitative parity."""
        res_cfo = self.client.get(f"/api/v1/demo/investigation/{self.kpi_id}?persona=CFO")
        res_rsm = self.client.get(f"/api/v1/demo/investigation/{self.kpi_id}?persona=REGIONAL_SALES_MANAGER")

        self.assertEqual(res_cfo.status_code, 200)
        self.assertEqual(res_rsm.status_code, 200)

        data_cfo = res_cfo.json()
        data_rsm = res_rsm.json()

        self.assertEqual(data_cfo["movement"]["variance"], data_rsm["movement"]["variance"])
        self.assertEqual(data_cfo["movement"]["percent_change"], data_rsm["movement"]["percent_change"])
        self.assertEqual(data_cfo["confidence"]["overall_confidence"], data_rsm["confidence"]["overall_confidence"])
        self.assertEqual(data_cfo["drivers"][0]["contribution_pct"], data_rsm["drivers"][0]["contribution_pct"])
        self.assertEqual(data_cfo["decision_graph_summary"], data_rsm["decision_graph_summary"])
        self.assertEqual(data_cfo["simulation_summary"], data_rsm["simulation_summary"])


if __name__ == "__main__":
    unittest.main()
