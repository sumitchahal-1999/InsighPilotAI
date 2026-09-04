"""
InsightPilot AI — Decision Graph Validator
Validates structural integrity, edge connectivity, evidence lineage, and abstention compliance.
"""

from typing import List, Dict, Any, Set, Tuple, Optional
from ai.decision_graph.models import DynamicDecisionGraph, DecisionGraphNodeModel, DecisionGraphEdgeModel

class DecisionGraphValidationError(Exception):
    """Raised when a generated decision graph violates structural or factual constraints."""
    pass

class DecisionGraphValidator:
    """Validates that a generated decision graph is strictly grounded and topologically sound."""

    @staticmethod
    def validate_graph(
        graph: DynamicDecisionGraph,
        validated_evidence_ids: Optional[Set[str]] = None,
        authoritative_driver_ids: Optional[Set[str]] = None
    ) -> Tuple[bool, List[str]]:
        """
        Validates full decision graph topology and returns (is_valid, list_of_errors).
        """
        errors: List[str] = []
        node_ids: Set[str] = set()

        # 1. Check Node Uniqueness
        for node in graph.nodes:
            if node.id in node_ids:
                errors.append(f"Duplicate node ID detected: '{node.id}'")
            node_ids.add(node.id)

        # 2. Check Edge Connectivity (No dangling edges)
        for edge in graph.edges:
            if edge.source not in node_ids:
                errors.append(f"Dangling edge source: '{edge.source}' not found in node set.")
            if edge.target not in node_ids:
                errors.append(f"Dangling edge target: '{edge.target}' not found in node set.")

        # 3. Check Parent/Child Link Consistency
        for node in graph.nodes:
            for p in node.linked_parents:
                if p not in node_ids:
                    errors.append(f"Node '{node.id}' references non-existent parent '{p}'")
            for c in node.linked_children:
                if c not in node_ids:
                    errors.append(f"Node '{node.id}' references non-existent child '{c}'")

        # 4. Check Evidence Integrity (No fabricated evidence IDs)
        if validated_evidence_ids is not None:
            for node in graph.nodes:
                if node.node_type == "EVIDENCE" or node.evidence_id:
                    eid = node.evidence_id
                    if eid and eid not in validated_evidence_ids:
                        errors.append(f"Unverified evidence ID '{eid}' on node '{node.id}' is not in validated evidence set.")

        # 5. Check Driver Integrity (No fabricated drivers)
        if authoritative_driver_ids is not None:
            for node in graph.nodes:
                if node.node_type == "DRIVER":
                    # Check if driver ID or node metadata driver matches
                    drv_key = node.metadata.get("driver_id")
                    if drv_key and drv_key not in authoritative_driver_ids:
                        errors.append(f"Unauthorized driver node '{node.id}' with driver_id '{drv_key}'")

        # 6. Check Abstention Safety
        if graph.abstained:
            forbidden_types = {"ACTION", "OUTCOME", "MECHANISM"}
            for node in graph.nodes:
                if node.node_type in forbidden_types:
                    errors.append(f"Abstained graph contains forbidden speculative node type '{node.node_type}' (ID: '{node.id}')")

        is_valid = len(errors) == 0
        return is_valid, errors

    @classmethod
    def assert_valid(
        cls,
        graph: DynamicDecisionGraph,
        validated_evidence_ids: Optional[Set[str]] = None,
        authoritative_driver_ids: Optional[Set[str]] = None
    ) -> None:
        """Raises DecisionGraphValidationError if validation fails."""
        is_valid, errors = cls.validate_graph(graph, validated_evidence_ids, authoritative_driver_ids)
        if not is_valid:
            raise DecisionGraphValidationError(f"Decision Graph validation failed with {len(errors)} error(s): {'; '.join(errors)}")
