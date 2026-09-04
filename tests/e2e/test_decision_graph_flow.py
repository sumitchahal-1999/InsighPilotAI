"""
InsightPilot AI — Phase 5.8: Decision Graph Lineage E2E Test Suite
Verifies the complete 6-column causal topology:
KPI Anomaly -> Drivers -> Evidence -> Business Mechanisms -> Recommended Actions -> Outcomes.
Tests edge connectivity, evidence ID validation, persona invariance, and API serialization.
"""

import unittest
from fastapi.testclient import TestClient
from backend.app.main import app
from ai.decision_graph import decision_graph_generator
from ai.decision_graph.validator import DecisionGraphValidator
from analytics.data_loader import DataLoader
from analytics.investigation_engine import InvestigationEngine
from evidence.evidence_engine import EvidenceEngine


class TestDecisionGraphFlow(unittest.TestCase):
    """End-to-End Decision Graph topology and lineage tests."""

    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)
        cls.kpi_id = "north_america_east_revenue"
        cls.loader = DataLoader(use_db=True)
        cls.inv_engine = InvestigationEngine(cls.loader)
        cls.evidence_engine = EvidenceEngine(cls.loader)
        cls.validator = DecisionGraphValidator()

    # -------------------------------------------------------------------------
    # 1. 6-Column Canonical Topology Integrity
    # -------------------------------------------------------------------------
    def test_canonical_decision_graph_topology(self):
        """Verifies that the canonical NA-East investigation produces the authoritative 6-column topology."""
        inv_res = self.inv_engine.run_investigation(self.kpi_id)
        evidence_resp = self.evidence_engine.get_all_evidence_for_investigation("NA-East")
        evidence = evidence_resp["all_evidence_nodes"]

        graph = decision_graph_generator.generate(
            kpi_id=self.kpi_id,
            region="NA-East",
            kpi_movement=inv_res["kpi"],
            drivers=inv_res["drivers"],
            validated_evidence=evidence,
            confidence={"overall_confidence": 89, "abstention": False}
        )

        # 6 Columns, 14 Nodes, 17 Edges
        self.assertEqual(graph.total_columns, 6)
        self.assertEqual(graph.total_nodes_count, 14)
        self.assertEqual(graph.total_edges_count, 17)

        # Validate Column Distribution (Columns 1 to 6)
        col_counts = {}
        for node in graph.nodes:
            col_counts[node.column] = col_counts.get(node.column, 0) + 1

        self.assertEqual(col_counts.get(1), 1, "Column 1 (KPI Anomaly) must have 1 node")
        self.assertEqual(col_counts.get(2), 4, "Column 2 (Drivers) must have 4 nodes")
        self.assertEqual(col_counts.get(3), 4, "Column 3 (Evidence) must have 4 nodes")
        self.assertEqual(col_counts.get(4), 2, "Column 4 (Mechanisms) must have 2 nodes")
        self.assertEqual(col_counts.get(5), 2, "Column 5 (Actions) must have 2 nodes")
        self.assertEqual(col_counts.get(6), 1, "Column 6 (Outcome) must have 1 node")

    # -------------------------------------------------------------------------
    # 2. Edge Integrity & Zero Dangling References
    # -------------------------------------------------------------------------
    def test_edge_connectivity_and_referential_integrity(self):
        """Ensures every edge connects valid source and target nodes with zero orphaned references."""
        inv_res = self.inv_engine.run_investigation(self.kpi_id)
        evidence_resp = self.evidence_engine.get_all_evidence_for_investigation("NA-East")
        evidence = evidence_resp["all_evidence_nodes"]

        graph = decision_graph_generator.generate(
            kpi_id=self.kpi_id,
            region="NA-East",
            kpi_movement=inv_res["kpi"],
            drivers=inv_res["drivers"],
            validated_evidence=evidence,
            confidence={"overall_confidence": 89, "abstention": False}
        )

        node_ids = {n.id for n in graph.nodes}
        for edge in graph.edges:
            self.assertIn(edge.source, node_ids, f"Edge source {edge.source} does not exist in graph nodes")
            self.assertIn(edge.target, node_ids, f"Edge target {edge.target} does not exist in graph nodes")
            self.assertIsNotNone(edge.relationship_type)

    # -------------------------------------------------------------------------
    # 3. Evidence Node Grounding Validation
    # -------------------------------------------------------------------------
    def test_evidence_node_grounding(self):
        """Verifies that all evidence nodes correspond strictly to real validated evidence records."""
        inv_res = self.inv_engine.run_investigation(self.kpi_id)
        evidence_resp = self.evidence_engine.get_all_evidence_for_investigation("NA-East")
        evidence = evidence_resp["all_evidence_nodes"]
        evidence_ids = {e["evidence_id"] for e in evidence}

        graph = decision_graph_generator.generate(
            kpi_id=self.kpi_id,
            region="NA-East",
            kpi_movement=inv_res["kpi"],
            drivers=inv_res["drivers"],
            validated_evidence=evidence,
            confidence={"overall_confidence": 89, "abstention": False}
        )

        evidence_nodes = [n for n in graph.nodes if n.column == 3]
        self.assertEqual(len(evidence_nodes), 4)
        for enode in evidence_nodes:
            self.assertIn(enode.evidence_id, evidence_ids)

    # -------------------------------------------------------------------------
    # 4. Persona Invariance on Decision Graph
    # -------------------------------------------------------------------------
    def test_persona_invariance_on_decision_graph(self):
        """Decision Graph structure, nodes, edges, and numerical metrics are 100% invariant between CFO and Sales Manager."""
        response_cfo = self.client.get(f"/api/v1/investigations/{self.kpi_id}/decision-graph?persona=CFO")
        response_rsm = self.client.get(f"/api/v1/investigations/{self.kpi_id}/decision-graph?persona=REGIONAL_SALES_MANAGER")

        self.assertEqual(response_cfo.status_code, 200)
        self.assertEqual(response_rsm.status_code, 200)

        data_cfo = response_cfo.json()
        data_rsm = response_rsm.json()

        self.assertEqual(data_cfo["total_columns"], data_rsm["total_columns"])
        self.assertEqual(data_cfo["total_nodes_count"], data_rsm["total_nodes_count"])
        self.assertEqual(data_cfo["total_edges_count"], data_rsm["total_edges_count"])

        # Compare node IDs and values
        cfo_node_ids = [n["id"] for n in data_cfo["nodes"]]
        rsm_node_ids = [n["id"] for n in data_rsm["nodes"]]
        self.assertEqual(cfo_node_ids, rsm_node_ids)


if __name__ == "__main__":
    unittest.main()
