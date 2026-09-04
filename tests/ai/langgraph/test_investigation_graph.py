"""
InsightPilot AI — LangGraph Investigation Pipeline Tests
Validates graph compilation, deterministic node execution, abstention branching, and numerical integrity.
"""

import unittest
from ai.langgraph.graph import (
    build_investigation_graph,
    compile_investigation_graph,
    run_investigation_workflow
)
from ai.langgraph.state import InvestigationState

class TestLangGraphInvestigation(unittest.TestCase):

    def test_graph_compilation(self):
        """Verifies that the LangGraph StateGraph compiles into an executable app."""
        app = compile_investigation_graph()
        self.assertIsNotNone(app)

    def test_full_investigation_workflow_execution(self):
        """Executes full multi-agent investigation workflow and verifies quantitative truth."""
        final_state = run_investigation_workflow(
            kpi_id="north_america_east_revenue",
            region="NA-East",
            prev_period_id="2026-Q2",
            curr_period_id="2026-Q3",
            persona="CFO"
        )

        # 1. Verify Nodes Executed
        nodes = final_state.get("nodes_executed", [])
        self.assertIn("load_kpi_node", nodes)
        self.assertIn("calculate_movement_node", nodes)
        self.assertIn("identify_drivers_node", nodes)
        self.assertIn("retrieve_evidence_node", nodes)
        self.assertIn("validate_evidence_node", nodes)
        self.assertIn("calculate_confidence_node", nodes)
        self.assertIn("prepare_grounding_node", nodes)
        self.assertIn("route_ai_capability_node", nodes)
        self.assertIn("ai_invocation_node", nodes)
        self.assertIn("executive_synthesis_node", nodes)
        self.assertIn("recommendations_context_node", nodes)

        # 2. Verify Grounded Deterministic Truth
        movement = final_state.get("kpi_movement", {})
        self.assertAlmostEqual(movement.get("previous_value", 0), 15430000.06, delta=0.01)
        self.assertAlmostEqual(movement.get("current_value", 0), 14200000.05, delta=0.01)
        self.assertAlmostEqual(movement.get("variance_amount", 0), -1230000.01, delta=0.01)
        self.assertAlmostEqual(movement.get("percent_change", 0), -7.97, places=2)

        # 3. Verify Drivers & Evidence
        drivers = final_state.get("drivers", [])
        self.assertEqual(len(drivers), 4)
        self.assertEqual(drivers[0]["driver_id"], "atlanta_dc_stockout")
        self.assertAlmostEqual(drivers[0]["contribution_pct"], 43.2, places=1)
        self.assertAlmostEqual(drivers[0]["impact_usd"], -550000.0, delta=0.01)

        evidence = final_state.get("evidence", [])
        self.assertGreater(len(evidence), 0)

        # 4. Verify Confidence & Non-Abstention
        confidence = final_state.get("confidence", {})
        conf_score = confidence.get("overall_confidence", confidence.get("overall_score", 0))
        self.assertGreaterEqual(conf_score, 65.0)
        self.assertFalse(final_state.get("abstention", True))

        # 5. Verify Structured AI Explanation Output
        explanation = final_state.get("ai_explanation", {})
        self.assertIsNotNone(explanation)
        self.assertIn("headline", explanation)
        self.assertIn("summary", explanation)

        # 6. Verify Recommendations Attached
        recs = final_state.get("recommendations", [])
        self.assertGreater(len(recs), 0)

    def test_abstention_branch_routing(self):
        """Verifies that an artificial low-confidence state routes strictly to abstention_node."""
        from ai.langgraph.nodes.investigation_nodes import confidence_router

        low_conf_state: InvestigationState = {
            "abstention": True,
            "confidence": {"overall_confidence": 45, "abstention": True}
        }
        self.assertEqual(confidence_router(low_conf_state), "abstention_node")

        high_conf_state: InvestigationState = {
            "abstention": False,
            "confidence": {"overall_confidence": 92, "abstention": False}
        }
        self.assertEqual(confidence_router(high_conf_state), "prepare_grounding_node")

if __name__ == "__main__":
    unittest.main()
