"""
InsightPilot AI — Competition Demo & Observability Routes
Exposes unified competition demo packages, execution lifecycle replays, and submission readiness audits.
"""

from typing import Optional
from fastapi import APIRouter, Depends, Path, Query, status
from backend.app.schemas.demo import (
    CompetitionDemoResponse,
    InvestigationReplayResponse,
    InvestigationReplayNode
)
from backend.app.schemas.common import ErrorResponse
from ai.demo.narrative import DemoNarrativeBuilder
from ai.demo.integrity_guard import DemoIntegrityGuard
from ai.demo.readiness import SubmissionReadinessService, SubmissionReadinessReport
from backend.app.services.investigation_service import InvestigationService
from backend.app.dependencies import get_investigation_service

router = APIRouter(prefix="/demo", tags=["Competition Demo"])


@router.get(
    "/investigation/{kpi_id}",
    response_model=CompetitionDemoResponse,
    responses={404: {"model": ErrorResponse, "description": "KPI not found"}},
    summary="Get complete unified competition demo package",
    description="Executes canonical investigation, evaluates 13 integrity criteria, builds the 10-beat storyboard narrative, and attaches safe provider source attribution."
)
async def get_demo_investigation(
    kpi_id: str = Path(..., description="Target KPI identifier (e.g. north_america_east_revenue)"),
    region: str = Query("NA-East", description="Target geographical region"),
    prev_period_id: str = Query("2026-Q2", description="Baseline comparison period"),
    curr_period_id: str = Query("2026-Q3", description="Current target period"),
    persona: str = Query("CFO", description="Audience persona ('CFO' or 'REGIONAL_SALES_MANAGER')"),
    investigation_service: InvestigationService = Depends(get_investigation_service)
) -> CompetitionDemoResponse:
    # 1. Run live investigation workflow
    trace = investigation_service.run_langgraph_investigation(
        kpi_id=kpi_id,
        region=region,
        prev_period_id=prev_period_id,
        curr_period_id=curr_period_id,
        persona_id=persona
    )

    inv_id = trace.investigation_id
    inv_std = investigation_service.run_investigation(kpi_id, region, prev_period_id, curr_period_id, persona)
    kpi_data = inv_std.kpi.model_dump()
    drivers = [d.model_dump() for d in inv_std.drivers]

    evidence_items = investigation_service.evidence_engine.get_all_evidence_for_investigation(region=region)["all_evidence_nodes"]

    recs = trace.recommendations or []
    if not recs:
        recs = investigation_service.rec_engine.generate_recommendations(kpi_id=kpi_id, region=region)

    # What-if simulation
    sim_res = investigation_service.sim_engine.simulate_inventory_availability(90.0, region=region)

    # Decision graph
    dg = investigation_service.get_decision_graph(kpi_id, region, prev_period_id, curr_period_id, persona)
    dg_dict = dg.model_dump()

    # AI Explanation & Source Attribution
    ai_expl = trace.ai_explanation or {}
    prov_meta = trace.telemetry or {}
    selected_prov = prov_meta.get("selected_provider", "deterministic_fallback")
    if selected_prov == "groq":
        ai_source_indicator = "AI Source: Groq (llama-3.3-70b-versatile)"
    elif selected_prov == "gemini":
        ai_source_indicator = "AI Source: Google Gemini (gemini-2.5-flash)"
    else:
        ai_source_indicator = "AI Source: Deterministic Grounded Fallback"

    # Build 10-Beat Storyboard Narrative
    narrative = DemoNarrativeBuilder.build_narrative(
        kpi_movement=kpi_data,
        drivers=drivers,
        evidence_items=evidence_items,
        confidence=trace.confidence,
        ai_explanation=ai_expl,
        recommendations=recs,
        simulation=sim_res,
        persona=persona
    )

    # Evaluate 13-Point System-Level Integrity Guard
    integrity_report = DemoIntegrityGuard.evaluate_integrity(
        kpi_movement=kpi_data,
        drivers=drivers,
        evidence_items=evidence_items,
        confidence=trace.confidence,
        ai_explanation=ai_expl,
        decision_graph=dg_dict,
        recommendations=recs,
        simulation=sim_res,
        persona=persona
    )

    return CompetitionDemoResponse(
        investigation_id=inv_id,
        kpi_id=kpi_id,
        persona=persona,
        kpi=kpi_data,
        movement={
            "baseline_value": kpi_data.get("previous_value", 15430000.06),
            "target_value": kpi_data.get("current_value", 14200000.05),
            "variance": kpi_data.get("variance_amount", -1230000.01),
            "percent_change": kpi_data.get("percent_change", -7.97),
            "status": kpi_data.get("materiality_status", "CRITICAL_NEGATIVE_VARIANCE")
        },
        drivers=drivers,
        confidence=trace.confidence,
        abstention={
            "abstained": trace.abstention,
            "reason": trace.abstention_reason
        },
        ai_explanation=ai_expl,
        ai_source_indicator=ai_source_indicator,
        evidence_summary={
            "total_evidence_count": len(evidence_items),
            "verified_lineage_count": len(evidence_items),
            "source_domains": ["ERP", "CRM_SALES", "SUPPORT_MARKET_INTEL"]
        },
        decision_graph_summary={
            "total_columns": dg.total_columns,
            "total_nodes_count": dg.total_nodes_count,
            "total_edges_count": dg.total_edges_count
        },
        recommendations=recs,
        simulation_summary=sim_res,
        demo_narrative=narrative,
        integrity_report=integrity_report,
        demo_status={
            "demo_ready": integrity_report.demo_ready,
            "environment": "COMPETITION_DEMO",
            "pipeline": "LangGraph Multi-Agent Orchestrator"
        }
    )


@router.get(
    "/replay/{kpi_id}",
    response_model=InvestigationReplayResponse,
    responses={404: {"model": ErrorResponse, "description": "KPI not found"}},
    summary="Get safe step-by-step investigation execution replay",
    description="Returns full node transition sequence with node classification (DETERMINISTIC vs AI), latencies, and safe pool IDs."
)
async def get_investigation_replay(
    kpi_id: str = Path(..., description="Target KPI identifier"),
    region: str = Query("NA-East", description="Target geographical region"),
    prev_period_id: str = Query("2026-Q2", description="Baseline comparison period"),
    curr_period_id: str = Query("2026-Q3", description="Current target period"),
    persona: str = Query("CFO", description="Audience persona"),
    investigation_service: InvestigationService = Depends(get_investigation_service)
) -> InvestigationReplayResponse:
    trace = investigation_service.run_langgraph_investigation(
        kpi_id=kpi_id,
        region=region,
        prev_period_id=prev_period_id,
        curr_period_id=curr_period_id,
        persona_id=persona
    )

    replay_nodes: list[InvestigationReplayNode] = []
    for idx, node in enumerate(trace.nodes, start=1):
        classification = "DETERMINISTIC"
        if "ai" in node.node_name or "synthesis" in node.node_name:
            classification = "AI_ORCHESTRATION"
        elif "abstention" in node.node_name or "confidence" in node.node_name or "validate" in node.node_name:
            classification = "SAFETY_GUARD"

        pool_id = "none"
        if node.node_name == "ai_invocation_node":
            pool_id = trace.telemetry.get("selected_key_slot", "none") or "deterministic_fallback"

        replay_nodes.append(InvestigationReplayNode(
            step_number=idx,
            node_name=node.node_name,
            display_name=node.display_name,
            classification=classification,
            status=node.status,
            duration_ms=node.duration_ms,
            provider_pool_id=pool_id,
            summary=node.summary,
            details=node.details
        ))

    fallback_occurred = any(e.status == "FALLBACK" for e in trace.provider_events) or (trace.telemetry.get("fallback_count", 0) > 0)

    return InvestigationReplayResponse(
        investigation_id=trace.investigation_id,
        kpi_id=kpi_id,
        persona=persona,
        total_steps=len(replay_nodes),
        total_duration_ms=trace.total_duration_ms,
        replay_nodes=replay_nodes,
        failover_events=[e.model_dump() for e in trace.provider_events],
        abstention_occurred=trace.abstention,
        fallback_occurred=fallback_occurred
    )


@router.get(
    "/readiness",
    response_model=SubmissionReadinessReport,
    summary="Get dynamic machine-readable competition readiness audit",
    description="Runs live health and integrity checks across all 10 analytical, database, and AI subsystems."
)
async def get_submission_readiness() -> SubmissionReadinessReport:
    return SubmissionReadinessService.evaluate_readiness()
