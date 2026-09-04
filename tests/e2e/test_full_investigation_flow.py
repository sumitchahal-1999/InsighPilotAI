"""
InsightPilot AI — Phase 5.8: End-to-End Investigation Flow Test Suite
Verifies the complete analytical pipeline from KPI anomaly selection to
deterministic calculations, evidence validation, multi-factor confidence,
LangGraph AI orchestration, Decision Graph generation, recommendations,
simulation, and executive synthesis.
"""

import unittest
from fastapi.testclient import TestClient
from backend.app.main import app
from ai.langgraph.graph import run_investigation_workflow
from ai.decision_graph import decision_graph_generator
from simulation.simulation_engine import SimulationEngine
from analytics.recommendations import RecommendationEngine
from analytics.data_loader import DataLoader


class TestFullInvestigationFlow(unittest.TestCase):
    """End-to-End full investigation pipeline tests."""

    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)
        cls.kpi_id = "north_america_east_revenue"
        cls.loader = DataLoader(use_db=True)
        cls.rec_engine = RecommendationEngine(cls.loader)
        cls.sim_engine = SimulationEngine(cls.loader)

    # -------------------------------------------------------------------------
    # 1. Complete LangGraph Workflow Execution
    # -------------------------------------------------------------------------
    def test_langgraph_full_pipeline_execution(self):
        """Executes the entire LangGraph workflow and validates state transitions."""
        result = run_investigation_workflow(
            kpi_id=self.kpi_id,
            region="NA-East",
            prev_period_id="2026-Q2",
            curr_period_id="2026-Q3",
            persona="CFO",
            include_recommendations=True,
            include_simulation=True
        )

        # 1. Pipeline Execution Metadata
        self.assertIn("started_at", result)
        self.assertIn("completed_at", result)
        self.assertGreater(result["total_duration_ms"], 0)

        # 2. Node Execution Sequence (all 11 canonical nodes)
        nodes_executed = result.get("nodes_executed", [])
        expected_nodes = [
            "load_kpi_node",
            "calculate_movement_node",
            "identify_drivers_node",
            "retrieve_evidence_node",
            "validate_evidence_node",
            "calculate_confidence_node",
            "prepare_grounding_node",
            "route_ai_capability_node",
            "ai_invocation_node",
            "executive_synthesis_node",
            "recommendations_context_node"
        ]
        for node in expected_nodes:
            self.assertIn(node, nodes_executed, f"Node {node} missing from executed sequence")

        # 3. Deterministic KPI Calculations
        kpi_movement = result.get("kpi_movement", {})
        self.assertAlmostEqual(kpi_movement["previous_value"], 15430000.06, places=2)
        self.assertAlmostEqual(kpi_movement["current_value"], 14200000.05, places=2)
        self.assertAlmostEqual(kpi_movement["variance_amount"], -1230000.01, places=2)
        self.assertAlmostEqual(kpi_movement["percent_change"], -7.97, places=2)
        self.assertEqual(kpi_movement["materiality_status"], "CRITICAL_NEGATIVE_VARIANCE")

        # 4. Multi-Factor Driver Engine
        drivers = result.get("drivers", [])
        self.assertEqual(len(drivers), 4)
        top_driver = drivers[0]
        self.assertEqual(top_driver["driver_id"], "atlanta_dc_stockout")
        self.assertAlmostEqual(top_driver["contribution_pct"], 43.2, places=1)
        self.assertAlmostEqual(top_driver["impact_usd"], -550000.0, places=0)
        self.assertEqual(top_driver["confidence_score"], 94)

        # 5. Evidence Sufficiency & Validation
        evidence_summary = result.get("evidence", [])
        self.assertGreater(len(evidence_summary), 0)

        # 6. Multi-Factor Confidence & Abstention Guard
        confidence_data = result.get("confidence", {})
        self.assertEqual(confidence_data.get("overall_confidence"), 89)
        self.assertEqual(confidence_data.get("confidence_label"), "HIGH")
        self.assertFalse(confidence_data.get("abstention", True))
        self.assertFalse(result.get("abstention", True))

        # 7. AI Grounded Reasoning State
        ai_explanation = result.get("ai_explanation", {})
        self.assertIsNotNone(ai_explanation)
        self.assertIn("summary", ai_explanation)
        self.assertIn("grounded_evidence_ids", ai_explanation)
        self.assertIn("EVID_ERP_ATL_STOCKOUT_001", ai_explanation["grounded_evidence_ids"])

        # 8. Decision Graph Integrity
        decision_graph = result.get("decision_graph", {})
        self.assertIsNotNone(decision_graph)
        self.assertEqual(decision_graph.get("total_columns"), 6)
        self.assertEqual(len(decision_graph.get("nodes", [])), 14)
        self.assertEqual(len(decision_graph.get("edges", [])), 17)

    # -------------------------------------------------------------------------
    # 2. FastAPI End-to-End Investigation Contract
    # -------------------------------------------------------------------------
    def test_fastapi_investigation_endpoint_e2e(self):
        """Verifies the complete FastAPI investigation endpoint response."""
        response = self.client.get(f"/api/v1/investigations/{self.kpi_id}")
        self.assertEqual(response.status_code, 200)
        data = response.json()

        # Invariance of canonical values
        self.assertEqual(data["kpi"]["id"], self.kpi_id)
        self.assertEqual(data["kpi"]["name"], "North America East Revenue")

        # KPI Block
        kpi = data["kpi"]
        self.assertAlmostEqual(kpi["previous_value"], 15430000.06, places=2)
        self.assertAlmostEqual(kpi["current_value"], 14200000.05, places=2)
        self.assertAlmostEqual(kpi["variance_amount"], -1230000.01, places=2)
        self.assertAlmostEqual(kpi["percent_change"], -7.97, places=2)

        # 4 Drivers sum to 100%
        drivers = data["drivers"]
        self.assertEqual(len(drivers), 4)
        total_contrib = sum(d["contribution_pct"] for d in drivers)
        self.assertAlmostEqual(total_contrib, 100.0, places=1)

        # Overall Confidence
        self.assertEqual(data["overall"]["overall_confidence"], 89)
        self.assertEqual(data["overall"]["confidence_label"], "HIGH")
        self.assertFalse(data["overall"]["abstention"])

    # -------------------------------------------------------------------------
    # 3. Recommendations and Simulation Integration
    # -------------------------------------------------------------------------
    def test_recommendation_and_simulation_full_flow(self):
        """Verifies that recommendation actions connect directly to simulation models."""
        # 1. Fetch recommendations
        recs = self.rec_engine.generate_recommendations(self.kpi_id)
        self.assertGreater(len(recs), 0)
        top_rec = recs[0]
        self.assertIn("20,000", top_rec["action"])
        self.assertAlmostEqual(top_rec["expected_impact"]["revenue_recovery_usd"], 484000.0, places=0)

        # 2. Run simulation
        sim_result = self.sim_engine.simulate_inventory_availability(
            inventory_availability=90.0,
            region="NA-East"
        )
        self.assertAlmostEqual(sim_result["baseline_value"], 79.4, places=1)
        self.assertAlmostEqual(sim_result["scenario_value"], 90.0, places=1)
        self.assertAlmostEqual(sim_result["estimated_recovery"]["revenue_recovery_usd"], 341422.91, places=2)
        self.assertAlmostEqual(sim_result["projected_value"], 14541422.96, places=2)


if __name__ == "__main__":
    unittest.main()
