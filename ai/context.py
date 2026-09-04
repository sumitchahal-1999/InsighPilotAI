"""
InsightPilot AI — Grounded Context Builder
Converts deterministic investigation results, evidence records, recommendations, and simulations
into a clean, compact, structured context for Gemini reasoning prompts.
"""

from typing import Dict, Any, List, Optional
from ai.schemas.persona import PersonaProfile, resolve_persona

class GroundedContextBuilder:
    """Builds authoritative, compact context representations from deterministic outputs."""

    @staticmethod
    def build_investigation_context(
        investigation_result: Dict[str, Any],
        evidence_items: List[Dict[str, Any]],
        persona: str = "CFO",
        recommendations: Optional[List[Dict[str, Any]]] = None,
        simulation: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Constructs the canonical grounded context payload for LLM reasoning."""
        persona_profile = resolve_persona(persona)

        kpi_raw = investigation_result.get("kpi", {})
        kpi_block = {
            "id": kpi_raw.get("id"),
            "name": kpi_raw.get("name"),
            "current_value": kpi_raw.get("current_value"),
            "previous_value": kpi_raw.get("previous_value"),
            "variance_amount": kpi_raw.get("variance_amount"),
            "percent_change": kpi_raw.get("percent_change"),
            "materiality_status": kpi_raw.get("materiality_status"),
            "region": investigation_result.get("region", "NA-East"),
            "period": f"{investigation_result.get('prev_period_id', '2026-Q2')} -> {investigation_result.get('curr_period_id', '2026-Q3')}"
        }

        drivers_list = []
        for d in investigation_result.get("drivers", []):
            drivers_list.append({
                "driver_id": d.get("driver_id"),
                "driver_name": d.get("driver_name"),
                "rank": d.get("rank"),
                "contribution_pct": d.get("contribution_pct"),
                "impact_usd": d.get("impact_usd"),
                "confidence_score": d.get("confidence_score"),
                "evidence_ids": d.get("evidence_ids", [])
            })

        evidence_list = []
        for ev in evidence_items:
            evidence_list.append({
                "evidence_id": ev.get("evidence_id"),
                "supports_driver": ev.get("supports_driver"),
                "source_system": ev.get("source"),
                "source_domain": ev.get("source_domain"),
                "source_record_id": ev.get("source_record_id"),
                "timestamp": ev.get("timestamp"),
                "freshness_status": ev.get("freshness", {}).get("status") if isinstance(ev.get("freshness"), dict) else ev.get("freshness"),
                "analytical_method": ev.get("analytical_method"),
                "finding_summary": ev.get("finding_summary"),
                "confidence_score": ev.get("confidence", {}).get("score") if isinstance(ev.get("confidence"), dict) else ev.get("confidence")
            })

        overall_raw = investigation_result.get("overall", {})
        overall_block = {
            "score": overall_raw.get("overall_confidence", 89),
            "label": overall_raw.get("confidence_label", "HIGH"),
            "abstention": overall_raw.get("abstention", False),
            "abstention_reason": overall_raw.get("abstention_reason")
        }

        context: Dict[str, Any] = {
            "investigation_id": investigation_result.get("investigation_id", "INV-EXEC-2026-NAE-001"),
            "kpi": kpi_block,
            "drivers": drivers_list,
            "evidence": evidence_list,
            "overall_confidence": overall_block,
            "persona": {
                "persona_name": persona_profile.persona.value,
                "role_title": persona_profile.role_title,
                "focus_areas": persona_profile.focus_areas,
                "tone": persona_profile.tone
            }
        }

        # Optional recommendations context
        if recommendations:
            recs_list = []
            for r in recommendations:
                exp_impact = r.get("expected_impact", {})
                recs_list.append({
                    "recommendation_id": r.get("recommendation_id"),
                    "action": r.get("action"),
                    "owner": r.get("owner"),
                    "controllability": r.get("controllability"),
                    "priority": r.get("priority"),
                    "expected_recovery_usd": exp_impact.get("revenue_recovery_usd", r.get("expected_recovery_usd")),
                    "margin_impact_pts": exp_impact.get("gross_margin_impact_points", r.get("margin_impact_pts")),
                    "recovery_timeframe_days": exp_impact.get("recovery_timeframe_days", r.get("recovery_timeframe_days")),
                    "confidence_score": r.get("confidence", {}).get("score") if isinstance(r.get("confidence"), dict) else r.get("confidence_score")
                })
            context["recommendations"] = recs_list

        # Optional simulation context
        if simulation:
            context["simulation"] = {
                "baseline_availability_pct": simulation.get("baseline_value", simulation.get("baseline_availability_pct")),
                "scenario_availability_pct": simulation.get("scenario_value", simulation.get("scenario_availability_pct")),
                "projected_revenue_usd": simulation.get("projected_value", simulation.get("projected_revenue_usd")),
                "estimated_recovery_usd": simulation.get("estimated_recovery", {}).get("revenue_recovery_usd", simulation.get("estimated_recovery_usd")),
                "confidence_score": simulation.get("confidence", {}).get("score") if isinstance(simulation.get("confidence"), dict) else simulation.get("confidence_score")
            }

        return context
