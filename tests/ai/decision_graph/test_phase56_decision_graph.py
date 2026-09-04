"""
InsightPilot AI — Phase 5.6 Decision Graph Comprehensive Test Suite
Validates dynamic deterministic decision graph generation, structural topology,
evidence lineage integrity, abstention guards, API contracts, and persona invariance.
"""

import unittest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient

from ai.decision_graph.generator import DecisionGraphGenerator, decision_graph_generator
from ai.decision_graph.validator import DecisionGraphValidator, DecisionGraphValidationError
from ai.decision_graph.models import DynamicDecisionGraph, DecisionGraphNodeModel, DecisionGraphEdgeModel
from ai.langgraph.graph import run_investigation_workflow
from backend.app.main import app

class TestPhase56DecisionGraph(unittest.TestCase):
    """Phase 5.6 dynamic decision graph validation test cases."""

    def setUp(self):
        self.client = TestClient(app)
        self.generator = DecisionGraphGenerator()
        self.canonical_kpi_movement = {
            "name": "North America East Revenue",
            "current_value": 14200000.05,
            "previous_value": 15430000.06,
            "variance_amount": -1230000.01,
            "percent_change": -7.97,
            "materiality_status": "CRITICAL"
        }
        self.canonical_drivers = [
            {"driver_id": "atlanta_dc_stockout", "driver_name": "Atlanta DC Stockout", "contribution_pct": 43.2, "impact_usd": -550000.0, "confidence_score": 94},
            {"driver_id": "sku8821_volume", "driver_name": "SKU-8821 Volume Contraction", "contribution_pct": 26.7, "impact_usd": -340000.0, "confidence_score": 89},
            {"driver_id": "distributor_deferral", "driver_name": "Distributor PO Deferral", "contribution_pct": 18.8, "impact_usd": -240000.0, "confidence_score": 85},
            {"driver_id": "horizon_promo", "driver_name": "Competitor Horizon Promo", "contribution_pct": 11.3, "impact_usd": -144000.0, "confidence_score": 78}
        ]
        self.canonical_evidence = [
            {"evidence_id": "EVID_ERP_ATL_STOCKOUT_001", "source_system": "SAP_ERP", "confidence": 94},
            {"evidence_id": "EVID_ZENDESK_ATL_DELAY_003", "source_system": "ZENDESK_CRM", "confidence": 89},
            {"evidence_id": "EVID_CRM_PO_DEF_006", "source_system": "CRM_EDI", "confidence": 85},
            {"evidence_id": "EVID_MKT_HORIZON_PROMO_008", "source_system": "MKT_SCRAPE", "confidence": 78}
        ]
        self.canonical_confidence = {
            "overall_confidence": 89,
            "tier": "HIGH",
            "abstention": False
        }

    # -------------------------------------------------------------------------
    # Test 1: Canonical 6-Column Graph Generation
    # -------------------------------------------------------------------------
    def test_canonical_graph_generation(self):
        """Canonical investigation generates complete 6-column topology."""
        graph = self.generator.generate(
            kpi_id="north_america_east_revenue",
            region="NA-East",
            kpi_movement=self.canonical_kpi_movement,
            drivers=self.canonical_drivers,
            validated_evidence=self.canonical_evidence,
            confidence=self.canonical_confidence
        )

        self.assertEqual(graph.total_columns, 6)
        self.assertEqual(graph.total_nodes_count, 14)
        self.assertEqual(graph.total_edges_count, 17)
        self.assertFalse(graph.abstained)
        self.assertEqual(graph.confidence, 89)

        # Verify column counts
        col_map = {}
        for n in graph.nodes:
            col_map[n.column] = col_map.get(n.column, 0) + 1
        
        self.assertEqual(col_map[1], 1)  # KPI Anomaly
        self.assertEqual(col_map[2], 4)  # 4 Causal Drivers
        self.assertEqual(col_map[3], 4)  # 4 Verified Evidence
        self.assertEqual(col_map[4], 2)  # 2 Causal Mechanics
        self.assertEqual(col_map[5], 2)  # 2 Action Levers
        self.assertEqual(col_map[6], 1)  # 1 Predicted Outcome

    # -------------------------------------------------------------------------
    # Test 2: Stable and Deterministic Node/Edge IDs
    # -------------------------------------------------------------------------
    def test_stable_graph_ids(self):
        """Generating the graph twice produces identical node IDs and edge structures."""
        graph1 = self.generator.generate(
            kpi_id="north_america_east_revenue",
            region="NA-East",
            kpi_movement=self.canonical_kpi_movement,
            drivers=self.canonical_drivers,
            validated_evidence=self.canonical_evidence,
            confidence=self.canonical_confidence
        )
        graph2 = self.generator.generate(
            kpi_id="north_america_east_revenue",
            region="NA-East",
            kpi_movement=self.canonical_kpi_movement,
            drivers=self.canonical_drivers,
            validated_evidence=self.canonical_evidence,
            confidence=self.canonical_confidence
        )

        ids1 = [n.id for n in graph1.nodes]
        ids2 = [n.id for n in graph2.nodes]
        self.assertEqual(ids1, ids2)

        edges1 = [(e.source, e.target, e.relationship_type) for e in graph1.edges]
        edges2 = [(e.source, e.target, e.relationship_type) for e in graph2.edges]
        self.assertEqual(edges1, edges2)

    # -------------------------------------------------------------------------
    # Test 3: Driver Node Integrity
    # -------------------------------------------------------------------------
    def test_driver_integrity(self):
        """All driver nodes map exactly to authoritative drivers without fabrication."""
        graph = self.generator.generate(
            kpi_id="north_america_east_revenue",
            region="NA-East",
            kpi_movement=self.canonical_kpi_movement,
            drivers=self.canonical_drivers,
            validated_evidence=self.canonical_evidence,
            confidence=self.canonical_confidence
        )

        driver_nodes = [n for n in graph.nodes if n.node_type == "DRIVER"]
        self.assertEqual(len(driver_nodes), 4)
        
        top_driver = driver_nodes[0]
        self.assertEqual(top_driver.id, "drv-1")
        self.assertEqual(top_driver.title, "Atlanta DC Stockout")
        self.assertEqual(top_driver.primary_metric, "43.2% Share")
        self.assertEqual(top_driver.secondary_metric, "-$550K Impact")
        self.assertEqual(top_driver.confidence, 94)

    # -------------------------------------------------------------------------
    # Test 4: Evidence Node Integrity
    # -------------------------------------------------------------------------
    def test_evidence_integrity(self):
        """All evidence nodes correspond to real validated empirical evidence IDs."""
        graph = self.generator.generate(
            kpi_id="north_america_east_revenue",
            region="NA-East",
            kpi_movement=self.canonical_kpi_movement,
            drivers=self.canonical_drivers,
            validated_evidence=self.canonical_evidence,
            confidence=self.canonical_confidence
        )

        evidence_nodes = [n for n in graph.nodes if n.node_type == "EVIDENCE"]
        self.assertEqual(len(evidence_nodes), 4)

        eids = {n.evidence_id for n in evidence_nodes}
        expected_eids = {
            "EVID_ERP_ATL_STOCKOUT_001",
            "EVID_ZENDESK_ATL_DELAY_003",
            "EVID_CRM_PO_DEF_006",
            "EVID_MKT_HORIZON_PROMO_008"
        }
        self.assertEqual(eids, expected_eids)

    # -------------------------------------------------------------------------
    # Test 5: Validator Catches Fabricated Evidence
    # -------------------------------------------------------------------------
    def test_validator_rejects_fabricated_evidence(self):
        """DecisionGraphValidator raises error if an unverified evidence ID is injected."""
        graph = self.generator.generate(
            kpi_id="north_america_east_revenue",
            region="NA-East",
            kpi_movement=self.canonical_kpi_movement,
            drivers=self.canonical_drivers,
            validated_evidence=self.canonical_evidence,
            confidence=self.canonical_confidence
        )

        # Inject an unauthorized evidence ID into node
        graph.nodes[4].evidence_id = "EVID_HALLUCINATED_INVENTORY_999"
        
        valid_eids = {e["evidence_id"] for e in self.canonical_evidence}
        is_valid, errors = DecisionGraphValidator.validate_graph(graph, validated_evidence_ids=valid_eids)
        self.assertFalse(is_valid)
        self.assertTrue(any("EVID_HALLUCINATED_INVENTORY_999" in err for err in errors))

    # -------------------------------------------------------------------------
    # Test 6: Edge Connectivity Integrity
    # -------------------------------------------------------------------------
    def test_edge_integrity(self):
        """Every edge connects existing source and target nodes with zero dangling references."""
        graph = self.generator.generate(
            kpi_id="north_america_east_revenue",
            region="NA-East",
            kpi_movement=self.canonical_kpi_movement,
            drivers=self.canonical_drivers,
            validated_evidence=self.canonical_evidence,
            confidence=self.canonical_confidence
        )

        node_id_set = {n.id for n in graph.nodes}
        for edge in graph.edges:
            self.assertIn(edge.source, node_id_set)
            self.assertIn(edge.target, node_id_set)

    # -------------------------------------------------------------------------
    # Test 7: Recommendation and Action Node Integrity
    # -------------------------------------------------------------------------
    def test_action_levers_integrity(self):
        """Action lever nodes match authoritative recommendation actions."""
        graph = self.generator.generate(
            kpi_id="north_america_east_revenue",
            region="NA-East",
            kpi_movement=self.canonical_kpi_movement,
            drivers=self.canonical_drivers,
            validated_evidence=self.canonical_evidence,
            confidence=self.canonical_confidence
        )

        action_nodes = [n for n in graph.nodes if n.node_type == "ACTION"]
        self.assertEqual(len(action_nodes), 2)
        self.assertEqual(action_nodes[0].id, "act-1")
        self.assertEqual(action_nodes[0].title, "Emergency Stock Transfer")
        self.assertEqual(action_nodes[0].primary_metric, "+$484K Recovery")
        self.assertEqual(action_nodes[1].id, "act-2")
        self.assertEqual(action_nodes[1].title, "Targeted Distributor Outreach")
        self.assertEqual(action_nodes[1].primary_metric, "+$180K Recovery")

    # -------------------------------------------------------------------------
    # Test 8: Predicted Outcome Node Integrity
    # -------------------------------------------------------------------------
    def test_predicted_outcome_integrity(self):
        """Outcome node matches authoritative modeled recovery projections."""
        graph = self.generator.generate(
            kpi_id="north_america_east_revenue",
            region="NA-East",
            kpi_movement=self.canonical_kpi_movement,
            drivers=self.canonical_drivers,
            validated_evidence=self.canonical_evidence,
            confidence=self.canonical_confidence
        )

        outcome_nodes = [n for n in graph.nodes if n.node_type == "OUTCOME"]
        self.assertEqual(len(outcome_nodes), 1)
        out = outcome_nodes[0]
        self.assertEqual(out.id, "out-1")
        self.assertEqual(out.title, "Projected Fiscal Recovery")
        self.assertEqual(out.primary_metric, "+$757.6K")
        self.assertEqual(out.secondary_metric, "$14.54M Projected Rev")
        self.assertEqual(out.confidence, 91)

    # -------------------------------------------------------------------------
    # Test 9: Abstention Safe Limited Graph
    # -------------------------------------------------------------------------
    def test_abstention_limited_graph(self):
        """When abstention triggers, a restricted 2-column safe graph is produced."""
        abstained_confidence = {
            "overall_confidence": 42,
            "tier": "LOW",
            "abstention": True,
            "abstention_reason": "Confidence below threshold (65%).",
            "reason_codes": ["LOW_CONFIDENCE"]
        }
        graph = self.generator.generate(
            kpi_id="north_america_east_revenue",
            region="NA-East",
            kpi_movement=self.canonical_kpi_movement,
            drivers=self.canonical_drivers,
            validated_evidence=self.canonical_evidence,
            confidence=abstained_confidence
        )

        self.assertTrue(graph.abstained)
        self.assertEqual(graph.total_columns, 2)
        self.assertEqual(graph.total_nodes_count, 2)
        self.assertEqual(graph.total_edges_count, 1)

        node_types = {n.node_type for n in graph.nodes}
        self.assertEqual(node_types, {"KPI", "ABSTENTION"})
        # No speculative actions or outcomes
        self.assertNotIn("ACTION", node_types)
        self.assertNotIn("OUTCOME", node_types)
        self.assertNotIn("MECHANISM", node_types)

    # -------------------------------------------------------------------------
    # Test 10: Provider Independence
    # -------------------------------------------------------------------------
    def test_provider_independence(self):
        """Decision graph generates successfully even if AI providers are completely down."""
        with patch("ai.orchestration.provider_router.AIProviderRouter.route_and_execute") as mock_gen:
            mock_gen.side_effect = Exception("LLM Provider Unavailable")

            state = run_investigation_workflow(kpi_id="north_america_east_revenue", persona="CFO")
            self.assertIn("decision_graph", state)
            self.assertIsNotNone(state["decision_graph"])
            self.assertEqual(state["decision_graph"]["total_nodes_count"], 14)
            self.assertEqual(state["decision_graph"]["total_edges_count"], 17)

    # -------------------------------------------------------------------------
    # Test 11: FastAPI Decision Graph Endpoint Contract
    # -------------------------------------------------------------------------
    def test_api_decision_graph_endpoint(self):
        """GET /api/v1/investigations/{kpi_id}/decision-graph returns 200 and valid schema."""
        resp = self.client.get("/api/v1/investigations/north_america_east_revenue/decision-graph")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["kpi_id"], "north_america_east_revenue")
        self.assertEqual(data["total_columns"], 6)
        self.assertEqual(data["total_nodes_count"], 14)
        self.assertEqual(data["total_edges_count"], 17)
        self.assertEqual(len(data["nodes"]), 14)
        self.assertEqual(len(data["edges"]), 17)

    # -------------------------------------------------------------------------
    # Test 12: Persona Invariance
    # -------------------------------------------------------------------------
    def test_persona_invariance(self):
        """Decision graph structure and metrics are 100% identical between CFO and Sales Manager."""
        graph_cfo = self.generator.generate(
            kpi_id="north_america_east_revenue",
            persona="CFO",
            kpi_movement=self.canonical_kpi_movement,
            drivers=self.canonical_drivers,
            validated_evidence=self.canonical_evidence,
            confidence=self.canonical_confidence
        )
        graph_sales = self.generator.generate(
            kpi_id="north_america_east_revenue",
            persona="Regional Sales Manager",
            kpi_movement=self.canonical_kpi_movement,
            drivers=self.canonical_drivers,
            validated_evidence=self.canonical_evidence,
            confidence=self.canonical_confidence
        )

        self.assertEqual(graph_cfo.total_nodes_count, graph_sales.total_nodes_count)
        self.assertEqual(graph_cfo.total_edges_count, graph_sales.total_edges_count)
        self.assertEqual([n.id for n in graph_cfo.nodes], [n.id for n in graph_sales.nodes])
        self.assertEqual([e.source for e in graph_cfo.edges], [e.source for e in graph_sales.edges])

if __name__ == "__main__":
    unittest.main()
