"""
InsightPilot AI — LangGraph Investigation Workflow Graph
Compiles and executes the multi-agent deterministic + AI investigation pipeline.
"""

import time
from datetime import datetime, timezone
from typing import Dict, Any, Optional
from langgraph.graph import StateGraph, START, END
from ai.langgraph.state import InvestigationState
from ai.langgraph.nodes import (
    load_kpi_node,
    calculate_movement_node,
    identify_drivers_node,
    retrieve_evidence_node,
    validate_evidence_node,
    calculate_confidence_node,
    confidence_router,
    abstention_node,
    prepare_grounding_node,
    route_ai_capability_node,
    ai_invocation_node,
    executive_synthesis_node,
    recommendations_context_node
)

def build_investigation_graph() -> StateGraph:
    """Constructs the full multi-agent investigation StateGraph."""
    graph = StateGraph(InvestigationState)

    # 1. Register Nodes
    graph.add_node("load_kpi", load_kpi_node)
    graph.add_node("calculate_movement", calculate_movement_node)
    graph.add_node("identify_drivers", identify_drivers_node)
    graph.add_node("retrieve_evidence", retrieve_evidence_node)
    graph.add_node("validate_evidence", validate_evidence_node)
    graph.add_node("calculate_confidence", calculate_confidence_node)
    graph.add_node("abstention", abstention_node)
    graph.add_node("prepare_grounding", prepare_grounding_node)
    graph.add_node("route_ai_capability", route_ai_capability_node)
    graph.add_node("ai_invocation", ai_invocation_node)
    graph.add_node("executive_synthesis", executive_synthesis_node)
    graph.add_node("recommendations_context", recommendations_context_node)

    # 2. Sequential Deterministic Edges
    graph.add_edge(START, "load_kpi")
    graph.add_edge("load_kpi", "calculate_movement")
    graph.add_edge("calculate_movement", "identify_drivers")
    graph.add_edge("identify_drivers", "retrieve_evidence")
    graph.add_edge("retrieve_evidence", "validate_evidence")
    graph.add_edge("validate_evidence", "calculate_confidence")

    # 3. Conditional Edge: Confidence Check (< 65% Abstains, >= 65% Continues)
    graph.add_conditional_edges(
        "calculate_confidence",
        confidence_router,
        {
            "abstention_node": "abstention",
            "prepare_grounding_node": "prepare_grounding"
        }
    )

    # 4. Abstention Branch Edge
    graph.add_edge("abstention", "recommendations_context")

    # 5. Grounded AI Reasoning Branch Edges
    graph.add_edge("prepare_grounding", "route_ai_capability")
    graph.add_edge("route_ai_capability", "ai_invocation")
    graph.add_edge("ai_invocation", "executive_synthesis")
    graph.add_edge("executive_synthesis", "recommendations_context")

    # 6. Terminal Edge
    graph.add_edge("recommendations_context", END)

    return graph

def compile_investigation_graph():
    """Compiles the investigation StateGraph into an executable runnable."""
    graph = build_investigation_graph()
    return graph.compile()

# Global compiled instance
investigation_graph_app = compile_investigation_graph()

def run_investigation_workflow(
    kpi_id: str = "north_america_east_revenue",
    region: str = "NA-East",
    prev_period_id: str = "2026-Q2",
    curr_period_id: str = "2026-Q3",
    persona: str = "CFO",
    include_recommendations: bool = True,
    include_simulation: bool = False
) -> Dict[str, Any]:
    """Executes the full compiled LangGraph investigation workflow."""
    start_time = time.perf_counter()
    started_iso = datetime.now(timezone.utc).isoformat()

    initial_state: InvestigationState = {
        "kpi_id": kpi_id,
        "region": region,
        "prev_period_id": prev_period_id,
        "curr_period_id": curr_period_id,
        "persona": persona,
        "include_recommendations": include_recommendations,
        "include_simulation": include_simulation,
        "nodes_executed": [],
        "node_traces": [],
        "provider_events": [],
        "errors": []
    }

    final_state = investigation_graph_app.invoke(initial_state)

    total_duration_ms = round((time.perf_counter() - start_time) * 1000.0, 2)
    completed_iso = datetime.now(timezone.utc).isoformat()

    final_state["started_at"] = started_iso
    final_state["completed_at"] = completed_iso
    final_state["total_duration_ms"] = total_duration_ms

    return final_state
