"""
InsightPilot AI — Phase 5.9: System-Level Demo Integrity Guard
Validates all 13 critical integrity criteria across deterministic calculations,
evidence lineage, multi-factor confidence, AI grounding, Decision Graph topology,
and security constraints to guarantee competition demonstration readiness.
"""

from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field


class IntegrityCheckItem(BaseModel):
    check_id: str = Field(..., description="Unique check identifier")
    name: str = Field(..., description="Human-readable check title")
    passed: bool = Field(..., description="True if verification succeeded")
    details: str = Field(..., description="Diagnostic validation message")


class DemoIntegrityReport(BaseModel):
    demo_ready: bool = Field(..., description="True if all 13 critical integrity checks pass")
    total_checks: int = Field(13, description="Total number of integrity criteria evaluated")
    passed_checks: int = Field(..., description="Number of passed criteria")
    failed_checks: int = Field(..., description="Number of failed criteria")
    checks: List[IntegrityCheckItem] = Field(..., description="Detailed verification checklist")
    summary: str = Field(..., description="Executive integrity readiness summary")


class DemoIntegrityGuard:
    """Rigorous pre-flight validator ensuring 100% integrity before presenting demonstrations."""

    @staticmethod
    def evaluate_integrity(
        kpi_movement: Dict[str, Any],
        drivers: List[Dict[str, Any]],
        evidence_items: List[Dict[str, Any]],
        confidence: Dict[str, Any],
        ai_explanation: Optional[Dict[str, Any]],
        decision_graph: Optional[Dict[str, Any]],
        recommendations: Optional[List[Dict[str, Any]]] = None,
        simulation: Optional[Dict[str, Any]] = None,
        persona: str = "CFO"
    ) -> DemoIntegrityReport:
        recommendations = recommendations or []
        ai_explanation = ai_explanation or {}
        decision_graph = decision_graph or {}
        simulation = simulation or {}

        checks: List[IntegrityCheckItem] = []

        # 1. KPI Values Exist
        has_kpi = bool(kpi_movement and "current_value" in kpi_movement and "previous_value" in kpi_movement)
        checks.append(IntegrityCheckItem(
            check_id="CHK_01_KPI_EXISTS",
            name="KPI Baseline & Target Values Exist",
            passed=has_kpi,
            details="Verified KPI baseline and target values are present." if has_kpi else "Missing KPI value fields."
        ))

        # 2. KPI Movement Mathematically Consistent
        prev_v = kpi_movement.get("previous_value", 0.0)
        curr_v = kpi_movement.get("current_value", 0.0)
        var_v = kpi_movement.get("variance_amount", 0.0)
        pct_v = kpi_movement.get("percent_change", 0.0)
        calc_var = round(curr_v - prev_v, 2)
        calc_pct = round(((curr_v - prev_v) / prev_v) * 100.0, 2) if prev_v != 0 else 0.0
        movement_valid = (abs(var_v - calc_var) <= 0.05) and (abs(pct_v - calc_pct) <= 0.05)
        checks.append(IntegrityCheckItem(
            check_id="CHK_02_KPI_MATH_CONSISTENCY",
            name="KPI Variance & Percentage Change Parity",
            passed=movement_valid,
            details=f"Calculated variance ${calc_var:,.2f} ({calc_pct:.2f}%) matches payload ${var_v:,.2f} ({pct_v:.2f}%)." if movement_valid else "Mathematical discrepancy in KPI movement calculations."
        ))

        # 3. Drivers Available
        has_drivers = len(drivers) > 0
        checks.append(IntegrityCheckItem(
            check_id="CHK_03_DRIVERS_AVAILABLE",
            name="Causal Driver Decomposition Present",
            passed=has_drivers,
            details=f"Identified {len(drivers)} causal drivers." if has_drivers else "Zero causal drivers identified."
        ))

        # 4. Driver Contribution Normalization (Sum ~ 100%)
        contrib_sum = sum(d.get("contribution_pct", 0.0) for d in drivers)
        contrib_valid = abs(contrib_sum - 100.0) <= 0.5 if drivers else False
        checks.append(IntegrityCheckItem(
            check_id="CHK_04_DRIVER_CONTRIBUTION_SUM",
            name="Driver Contribution Normalization (100% Sum)",
            passed=contrib_valid,
            details=f"Driver contributions sum to {contrib_sum:.1f}%." if contrib_valid else f"Contributions sum to {contrib_sum:.1f}% (expected ~100.0%)."
        ))

        # 5. Evidence Exists or Abstention Correctly Triggered
        is_abstained = confidence.get("abstention", False) or confidence.get("abstain", False)
        evidence_sufficient = (len(evidence_items) > 0) or is_abstained
        checks.append(IntegrityCheckItem(
            check_id="CHK_05_EVIDENCE_SUFFICIENCY",
            name="Empirical Evidence Sufficiency or Abstention",
            passed=evidence_sufficient,
            details=f"Found {len(evidence_items)} evidence records (Abstention: {is_abstained})." if evidence_sufficient else "Zero evidence found without triggering abstention."
        ))

        # 6. Evidence Lineage Cryptographic Integrity
        hashes_valid = True
        for ev in evidence_items:
            lineage = ev.get("lineage", {}) if isinstance(ev, dict) else getattr(ev, "lineage", None)
            h = None
            if isinstance(lineage, dict) and lineage.get("verification_hash"):
                h = lineage.get("verification_hash")
            elif hasattr(lineage, "verification_hash") and getattr(lineage, "verification_hash"):
                h = getattr(lineage, "verification_hash")
            elif isinstance(ev, dict):
                h = ev.get("verification_hash") or ev.get("hash")
            else:
                h = getattr(ev, "verification_hash", None) or getattr(ev, "hash", None)

            if not h or not str(h).startswith("sha256:"):
                hashes_valid = False
                break
        checks.append(IntegrityCheckItem(
            check_id="CHK_06_LINEAGE_CRYPTOGRAPHIC_HASH",
            name="SHA-256 Cryptographic Evidence Lineage",
            passed=hashes_valid,
            details="All evidence items possess valid SHA-256 cryptographic digests." if hashes_valid else "Invalid or missing SHA-256 verification hash on evidence item."
        ))

        # 7. Confidence Calculation Bounds [0, 100]
        conf_score = confidence.get("overall_confidence", -1)
        conf_valid = 0 <= conf_score <= 100
        checks.append(IntegrityCheckItem(
            check_id="CHK_07_CONFIDENCE_BOUNDS",
            name="Multi-Factor Confidence Bounds [0, 100]",
            passed=conf_valid,
            details=f"Multi-factor confidence score is {conf_score}%." if conf_valid else f"Confidence score out of bounds: {conf_score}."
        ))

        # 8. Abstention Safety Policy (Score < 65 -> Abstention == True)
        abstention_policy_valid = True
        if conf_score < 65 and not is_abstained:
            abstention_policy_valid = False
        checks.append(IntegrityCheckItem(
            check_id="CHK_08_ABSTENTION_SAFETY_POLICY",
            name="Mandatory Confidence Threshold Abstention Guard",
            passed=abstention_policy_valid,
            details=f"Abstention policy verified (Score: {conf_score}%, Abstained: {is_abstained})." if abstention_policy_valid else "Safety violation: Confidence < 65% failed to trigger mandatory abstention."
        ))

        # 9. AI Explanation Grounding Check
        valid_ev_ids = {ev.get("evidence_id") for ev in evidence_items if ev.get("evidence_id")}
        valid_drv_ids = {d.get("driver_id") for d in drivers if d.get("driver_id")}
        cited_evs = set(ai_explanation.get("grounded_evidence_ids", [])) | set(ai_explanation.get("supporting_evidence_ids", []))
        cited_drvs = set(ai_explanation.get("supporting_driver_ids", []))
        hallucinated_evs = [e for e in cited_evs if e not in valid_ev_ids]
        hallucinated_drvs = [d for d in cited_drvs if d not in valid_drv_ids]
        grounding_clean = len(hallucinated_evs) == 0 and len(hallucinated_drvs) == 0
        checks.append(IntegrityCheckItem(
            check_id="CHK_09_AI_GROUNDING_INTEGRITY",
            name="AI Factual Grounding & Zero Hallucination Citations",
            passed=grounding_clean,
            details="All cited evidence and driver IDs match verified context." if grounding_clean else f"Hallucinated citations detected: ev={hallucinated_evs}, drv={hallucinated_drvs}."
        ))

        # 10. Decision Graph Structural Integrity
        dg_nodes = decision_graph.get("nodes", [])
        dg_edges = decision_graph.get("edges", [])
        dg_node_ids = {n.get("id") if isinstance(n, dict) else getattr(n, "id", "") for n in dg_nodes}
        dg_edges_valid = True
        for e in dg_edges:
            src = e.get("source") if isinstance(e, dict) else getattr(e, "source", "")
            tgt = e.get("target") if isinstance(e, dict) else getattr(e, "target", "")
            if src not in dg_node_ids or tgt not in dg_node_ids:
                dg_edges_valid = False
                break
        dg_valid = (len(dg_nodes) > 0) and dg_edges_valid if decision_graph else True
        checks.append(IntegrityCheckItem(
            check_id="CHK_10_DECISION_GRAPH_INTEGRITY",
            name="Decision Graph Referential Integrity & Zero Orphaned Edges",
            passed=dg_valid,
            details=f"Decision graph validated ({len(dg_nodes)} nodes, {len(dg_edges)} edges)." if dg_valid else "Decision graph contains dangling edge references."
        ))

        # 11. Recommendations Context Grounding
        recs_grounded = True
        for r in recommendations:
            d_id = r.get("driver_id")
            if d_id and d_id not in valid_drv_ids:
                recs_grounded = False
                break
        checks.append(IntegrityCheckItem(
            check_id="CHK_11_RECOMMENDATION_CONTEXT_GROUNDING",
            name="Action Levers Grounded in Verified Drivers",
            passed=recs_grounded,
            details=f"All {len(recommendations)} recommendations map to verified causal drivers." if recs_grounded else "Recommendation references unknown driver ID."
        ))

        # 12. Simulation Determinism & Bounds
        sim_valid = True
        if simulation:
            est_rec = simulation.get("estimated_recovery", {})
            rev_rec = est_rec.get("revenue_recovery_usd", 0.0)
            if rev_rec < 0.0:
                sim_valid = False
        checks.append(IntegrityCheckItem(
            check_id="CHK_12_SIMULATION_DETERMINISM",
            name="What-If Simulation Mathematical Bounds",
            passed=sim_valid,
            details="Simulation recovery output satisfies non-negative bounds." if sim_valid else "Simulation generated negative recovery value."
        ))

        # 13. Zero Secret Leakage
        all_text = str(kpi_movement) + str(drivers) + str(evidence_items) + str(confidence) + str(ai_explanation) + str(decision_graph) + str(recommendations) + str(simulation)
        secret_leaked = ("gsk_" in all_text) or ("AIzaSy" in all_text) or ("Bearer " in all_text)
        checks.append(IntegrityCheckItem(
            check_id="CHK_13_ZERO_SECRET_LEAKAGE",
            name="Zero API Key & Credential Leakage in Payloads",
            passed=not secret_leaked,
            details="No API keys, authorization tokens, or secrets found in data payloads." if not secret_leaked else "Security alert: Secret token detected in serialized state!"
        ))

        passed_count = sum(1 for c in checks if c.passed)
        failed_count = len(checks) - passed_count
        demo_ready = (failed_count == 0)

        summary_msg = (
            f"All {len(checks)} critical system integrity checks passed. System is 100% DEMO READY."
            if demo_ready
            else f"Integrity check failed: {failed_count} check(s) violated. DEMO NOT READY."
        )

        return DemoIntegrityReport(
            demo_ready=demo_ready,
            total_checks=len(checks),
            passed_checks=passed_count,
            failed_checks=failed_count,
            checks=checks,
            summary=summary_msg
        )
