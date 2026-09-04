"""
InsightPilot AI — Investigation Service Layer
Orchestrates deterministic root cause investigations, driver decomposition, and decision graph topology for API endpoints.
"""

from typing import Dict, Any, Optional, List
from analytics.data_loader import DataLoader
from analytics.investigation_engine import InvestigationEngine
from evidence.evidence_engine import EvidenceEngine
from analytics.recommendations import RecommendationEngine
from simulation.simulation_engine import SimulationEngine
from ai.decision_graph import decision_graph_generator
from ai.langgraph.graph import run_investigation_workflow
from backend.app.schemas.investigation import (
    InvestigationResponse,
    DriverListResponse,
    DriverResponse,
    KPIBlock,
    EvidenceSummaryBlock,
    OverallConfidenceBlock,
    LineageGraphBlock,
    DecisionGraphNode,
    DecisionGraphEdge,
    DecisionGraphResponse,
    LangGraphTraceResponse,
    LangGraphNodeTrace,
    LangGraphNodeMetric,
    ProviderEventTrace,
)
from backend.app.errors import KPINotFoundError

class InvestigationService:
    """Service layer delegating investigation logic to analytics.investigation_engine."""
    
    SUPPORTED_KPIS = {"north_america_east_revenue"}

    def __init__(self, data_loader: Optional[DataLoader] = None):
        self.loader = data_loader or DataLoader()
        self.investigation_engine = InvestigationEngine(self.loader)
        self.evidence_engine = EvidenceEngine(self.loader)
        self.rec_engine = RecommendationEngine(self.loader)
        self.sim_engine = SimulationEngine(self.loader)

    def run_investigation(
        self,
        kpi_id: str,
        region: str = "NA-East",
        prev_period_id: str = "2026-Q2",
        curr_period_id: str = "2026-Q3",
        persona_id: str = "CFO"
    ) -> InvestigationResponse:
        """Executes full deterministic investigation pipeline and formats Pydantic response."""
        if kpi_id not in self.SUPPORTED_KPIS:
            raise KPINotFoundError(kpi_id)

        raw_result = self.investigation_engine.run_investigation(
            kpi_id=kpi_id,
            region=region,
            prev_period_id=prev_period_id,
            curr_period_id=curr_period_id,
            persona_id=persona_id
        )

        return InvestigationResponse(
            investigation_id=raw_result["investigation_id"],
            timestamp=raw_result["timestamp"],
            persona_id=raw_result["persona_id"],
            kpi=KPIBlock(**raw_result["kpi"]),
            drivers=[DriverResponse(**d) for d in raw_result["drivers"]],
            evidence_summary=EvidenceSummaryBlock(**raw_result["evidence_summary"]),
            overall=OverallConfidenceBlock(**raw_result["overall"]),
            lineage_graph=LineageGraphBlock(**raw_result["lineage_graph"])
        )

    def run_langgraph_investigation(
        self,
        kpi_id: str,
        region: str = "NA-East",
        prev_period_id: str = "2026-Q2",
        curr_period_id: str = "2026-Q3",
        persona_id: str = "CFO",
        include_recommendations: bool = True,
        include_simulation: bool = False
    ) -> LangGraphTraceResponse:
        """Executes the compiled LangGraph multi-agent workflow and returns typed trace data."""
        if kpi_id not in self.SUPPORTED_KPIS:
            raise KPINotFoundError(kpi_id)

        final_state = run_investigation_workflow(
            kpi_id=kpi_id,
            region=region,
            prev_period_id=prev_period_id,
            curr_period_id=curr_period_id,
            persona=persona_id,
            include_recommendations=include_recommendations,
            include_simulation=include_simulation
        )

        nodes: List[LangGraphNodeTrace] = []
        for n in final_state.get("node_traces", []):
            metrics_list = [LangGraphNodeMetric(**m) for m in n.get("metrics", [])]
            nodes.append(LangGraphNodeTrace(
                node_name=n["node_name"],
                display_name=n.get("display_name", n["node_name"]),
                role=n.get("role", "Investigation Node"),
                status=n.get("status", "COMPLETED"),
                started_at=n.get("started_at"),
                completed_at=n.get("completed_at"),
                duration_ms=float(n.get("duration_ms", 0.0)),
                summary=n.get("summary", ""),
                details=n.get("details", []),
                metrics=metrics_list,
                metadata=n.get("metadata", {})
            ))

        provider_events: List[ProviderEventTrace] = []
        for pe in final_state.get("provider_events", []):
            provider_events.append(ProviderEventTrace(
                provider=pe.get("provider", "groq"),
                key_pool=pe.get("key_pool", "none"),
                task_type=pe.get("task_type", "INVESTIGATION_EXPLANATION"),
                model=pe.get("model", "llama-3.3-70b-versatile"),
                status=pe.get("status", "SUCCESS"),
                fallback_from=pe.get("fallback_from"),
                duration_ms=float(pe.get("duration_ms", 0.0))
            ))

        is_abstained = final_state.get("abstention", False)
        status_str = "ABSTAINED" if is_abstained else "COMPLETED"

        kpi_movement = final_state.get("kpi_movement", {})
        drivers = final_state.get("drivers", [])

        deterministic_summary = {
            "kpi_id": kpi_id,
            "region": region,
            "previous_value": kpi_movement.get("previous_value", 15430000.06),
            "current_value": kpi_movement.get("current_value", 14200000.05),
            "variance_amount": kpi_movement.get("variance_amount", -1230000.01),
            "percent_change": kpi_movement.get("percent_change", -7.97),
            "materiality_status": kpi_movement.get("materiality_status", "CRITICAL_NEGATIVE_VARIANCE"),
            "drivers_count": len(drivers),
            "top_driver": drivers[0]["driver_name"] if drivers else None
        }

        return LangGraphTraceResponse(
            investigation_id=final_state.get("investigation_id", f"INV-{kpi_id}"),
            kpi_id=kpi_id,
            region=region,
            prev_period_id=prev_period_id,
            curr_period_id=curr_period_id,
            persona_id=persona_id,
            status=status_str,
            started_at=final_state.get("started_at", ""),
            completed_at=final_state.get("completed_at", ""),
            total_duration_ms=float(final_state.get("total_duration_ms", 0.0)),
            nodes=nodes,
            provider_events=provider_events,
            confidence=final_state.get("confidence", {}),
            abstention=is_abstained,
            abstention_reason=final_state.get("abstention_reason"),
            ai_explanation=final_state.get("ai_explanation"),
            deterministic_summary=deterministic_summary,
            recommendations=final_state.get("recommendations", []),
            telemetry=final_state.get("telemetry", {})
        )

    def get_drivers(
        self,
        kpi_id: str,
        region: str = "NA-East",
        prev_period_id: str = "2026-Q2",
        curr_period_id: str = "2026-Q3"
    ) -> DriverListResponse:
        """Retrieves and returns the ranked explanatory drivers list."""
        inv_res = self.run_investigation(kpi_id, region, prev_period_id, curr_period_id)
        return DriverListResponse(
            kpi_id=kpi_id,
            total_drivers=len(inv_res.drivers),
            drivers=inv_res.drivers
        )

    def get_decision_graph(
        self,
        kpi_id: str,
        region: str = "NA-East",
        prev_period_id: str = "2026-Q2",
        curr_period_id: str = "2026-Q3",
        persona: str = "CFO"
    ) -> DecisionGraphResponse:
        """Constructs the deterministic 6-column causal topology for the decision graph dynamically."""
        if kpi_id not in self.SUPPORTED_KPIS:
            raise KPINotFoundError(kpi_id)

        # 1. Fetch live deterministic state
        kpi_movement = self.investigation_engine.kpi_engine.evaluate_kpi_movement(
            kpi_id=kpi_id,
            region=region,
            prev_period_id=prev_period_id,
            curr_period_id=curr_period_id
        )
        drivers = self.investigation_engine.driver_engine.investigate_revenue_drivers(
            region=region,
            prev_period_id=prev_period_id,
            curr_period_id=curr_period_id
        )
        evidence = self.evidence_engine.get_all_evidence_for_investigation(region=region)["all_evidence_nodes"]
        conf = self.investigation_engine.confidence_engine.evaluate_investigation_confidence(
            drivers=drivers,
            evidence_items=evidence,
            validated_evidence=evidence,
            lineage_valid=True,
            kpi_movement=kpi_movement
        )
        recs = self.rec_engine.generate_recommendations(kpi_id=kpi_id, region=region)
        sim = self.sim_engine.simulate_inventory_availability(inventory_availability=0.90, region=region)

        # 2. Dynamically generate Decision Graph
        dyn_graph = decision_graph_generator.generate(
            kpi_id=kpi_id,
            region=region,
            kpi_movement=kpi_movement,
            drivers=drivers,
            validated_evidence=evidence,
            confidence=conf,
            recommendations=recs,
            simulation=sim,
            persona=persona
        )

        # 3. Transform to DecisionGraphResponse
        nodes = [
            DecisionGraphNode(
                id=n.id,
                column=n.column,
                column_title=n.column_title,
                title=n.title,
                node_type=n.node_type,
                category=n.category,
                primary_metric=n.primary_metric,
                secondary_metric=n.secondary_metric,
                confidence=n.confidence,
                description=n.description,
                status=n.status,
                evidence_id=n.evidence_id,
                hash=n.hash,
                linked_parents=n.linked_parents,
                linked_children=n.linked_children
            )
            for n in dyn_graph.nodes
        ]
        edges = [
            DecisionGraphEdge(
                source=e.source,
                target=e.target,
                relationship_type=e.relationship_type
            )
            for e in dyn_graph.edges
        ]

        return DecisionGraphResponse(
            kpi_id=kpi_id,
            region=region,
            total_columns=dyn_graph.total_columns,
            total_nodes_count=dyn_graph.total_nodes_count,
            total_edges_count=dyn_graph.total_edges_count,
            nodes=nodes,
            edges=edges
        )

