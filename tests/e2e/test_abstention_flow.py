"""
InsightPilot AI — Phase 5.8: Responsible AI Abstention E2E Test Suite
Verifies that low confidence, missing evidence, lineage failures, or unverified
drivers trigger mandatory analytical abstention, bypassing generative LLMs,
rendering restricted safe Decision Graphs, and maintaining factual integrity.
"""

import unittest
from unittest.mock import patch
from fastapi.testclient import TestClient
from backend.app.main import app
from ai.langgraph.graph import run_investigation_workflow
from ai.decision_graph import decision_graph_generator
from ai.langgraph.nodes.investigation_nodes import abstention_node
from ai.langgraph.state import InvestigationState


class TestAbstentionFlow(unittest.TestCase):
    """End-to-End Responsible AI Abstention Guard tests."""

    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)
        cls.kpi_id = "north_america_east_revenue"

    # -------------------------------------------------------------------------
    # 1. Low Confidence (<65%) Triggers Safe Abstention
    # -------------------------------------------------------------------------
    def test_low_confidence_triggers_abstention_workflow(self):
        """When multi-factor confidence drops below 65%, workflow routes strictly to abstention."""
        with patch("analytics.confidence_engine.ConfidenceEngine.evaluate_investigation_confidence") as mock_conf:
            mock_conf.return_value = {
                "overall_confidence": 52,
                "confidence_label": "LOW",
                "abstention": True,
                "abstention_reason": "Low aggregate confidence score (52% < 65% threshold).",
                "factor_breakdown": {}
            }

            result = run_investigation_workflow(
                kpi_id=self.kpi_id,
                persona="CFO"
            )

            # Workflow marked as abstained
            self.assertTrue(result.get("abstention"))
            self.assertEqual(result.get("abstention_reason"), "Low aggregate confidence score (52% < 65% threshold).")

            # Executed nodes included abstention_node and skipped ai_invocation_node
            nodes_executed = result.get("nodes_executed", [])
            self.assertIn("abstention_node", nodes_executed)
            self.assertNotIn("ai_invocation_node", nodes_executed)

            # AI Explanation explicitly reflects abstention
            ai_explanation = result.get("ai_explanation", {})
            self.assertTrue(ai_explanation.get("abstained"))
            self.assertIn("Suspended", ai_explanation.get("headline", ""))

            # Restricted 2-column Decision Graph generated
            decision_graph = result.get("decision_graph", {})
            self.assertEqual(decision_graph.get("total_columns"), 2)

    # -------------------------------------------------------------------------
    # 2. Missing Evidence Triggers Abstention
    # -------------------------------------------------------------------------
    def test_no_valid_evidence_triggers_abstention(self):
        """When evidence retrieval yields 0 verified records, workflow triggers mandatory abstention."""
        with patch("evidence.evidence_engine.EvidenceEngine.get_evidence_for_driver", return_value=[]):
            result = run_investigation_workflow(
                kpi_id=self.kpi_id,
                persona="CFO"
            )

            self.assertTrue(result.get("abstention"))
            self.assertIn("abstention_node", result.get("nodes_executed", []))
            self.assertNotIn("ai_invocation_node", result.get("nodes_executed", []))

    # -------------------------------------------------------------------------
    # 3. Direct Abstention Node Output Verification
    # -------------------------------------------------------------------------
    def test_abstention_node_structured_output_contract(self):
        """Verifies the exact structured dictionary contract returned by the abstention node."""
        state: InvestigationState = {
            "investigation_id": "INV-EXEC-2026-NAE-001",
            "kpi_id": self.kpi_id,
            "region": "NA-East",
            "prev_period_id": "2026-Q2",
            "curr_period_id": "2026-Q3",
            "persona": "CFO",
            "kpi_movement": {
                "previous_value": 15430000.06,
                "current_value": 14200000.05,
                "variance_amount": -1230000.01,
                "percent_change": -7.97,
                "materiality_status": "CRITICAL_NEGATIVE_VARIANCE"
            },
            "drivers": [
                {
                    "driver_id": "atlanta_dc_stockout",
                    "driver_name": "Atlanta DC Stockout",
                    "rank": 1,
                    "contribution_pct": 43.2,
                    "impact_usd": -550000.0,
                    "confidence_score": 94,
                    "supporting_evidence_ids": []
                }
            ],
            "confidence": {
                "overall_confidence": 54,
                "confidence_label": "LOW",
                "abstention": True,
                "abstention_reason": "Insufficient empirical evidence."
            },
            "abstention": True,
            "abstention_reason": "Insufficient empirical evidence.",
            "nodes_executed": ["calculate_confidence_node"],
            "node_traces": [],
            "provider_events": [],
            "errors": []
        }

        output = abstention_node(state)

        self.assertIn("ai_explanation", output)
        self.assertTrue(output["ai_explanation"]["abstained"])
        self.assertEqual(output["ai_explanation"]["abstention_reason"], "Insufficient empirical evidence.")
        self.assertEqual(output["telemetry"]["generation_status"], "abstained")

    # -------------------------------------------------------------------------
    # 4. Decision Graph Generator Restricted Abstention Graph
    # -------------------------------------------------------------------------
    def test_decision_graph_generator_on_abstention(self):
        """Verifies that decision_graph_generator produces a safe 2-column restricted graph when abstained."""
        kpi_movement = {
            "previous_value": 15430000.06,
            "current_value": 14200000.05,
            "variance_amount": -1230000.01,
            "percent_change": -7.97,
            "materiality_status": "CRITICAL_NEGATIVE_VARIANCE"
        }
        drivers = [
            {
                "driver_id": "atlanta_dc_stockout",
                "driver_name": "Atlanta DC Stockout",
                "rank": 1,
                "contribution_pct": 43.2,
                "impact_usd": -550000.0,
                "confidence_score": 94,
                "supporting_evidence_ids": []
            }
        ]

        graph = decision_graph_generator.generate(
            kpi_id=self.kpi_id,
            region="NA-East",
            kpi_movement=kpi_movement,
            drivers=drivers,
            validated_evidence=[],
            confidence={
                "overall_confidence": 48,
                "abstention": True,
                "abstention_reason": "Low confidence score."
            }
        )

        self.assertEqual(graph.total_columns, 2)
        # Verify columns are strictly KPI Anomaly (1) and Drivers (2)
        column_indices = {n.column for n in graph.nodes}
        self.assertEqual(column_indices, {1, 2})
        # Verify no speculative actions or outcomes exist
        node_types = {n.node_type for n in graph.nodes}
        self.assertNotIn("ACTION", node_types)
        self.assertNotIn("OUTCOME", node_types)


if __name__ == "__main__":
    unittest.main()
