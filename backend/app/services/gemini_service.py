"""
InsightPilot AI — Gemini Service Layer
Backend service abstraction managing Gemini reasoning requests, deterministic context assembly,
grounding validation, persona enforcement, and telemetry logging without secrets.
"""

import logging
import time
from typing import Dict, Any, List, Optional
from ai.config import ai_config
from ai.service import AIService, AIServiceUnavailableError, AIGroundingError
from ai.schemas.persona import resolve_persona
from ai.schemas.explanation import (
    StructuredAIExplanationResponse,
    AIExplanationResponse,
    AIDriverExplanationResponse
)
from backend.app.services.investigation_service import InvestigationService
from backend.app.services.evidence_service import EvidenceService
from backend.app.services.recommendation_service import RecommendationService
from backend.app.services.simulation_service import SimulationService
from backend.app.errors import (
    KPINotFoundError,
    InvalidPersonaAPIError,
    AIServiceUnavailableAPIError,
    AIGroundingAPIError
)

logger = logging.getLogger("insightpilot.gemini_service")

class GeminiService:
    """Backend service orchestrating grounded Gemini reasoning over deterministic outputs."""

    def __init__(
        self,
        ai_service: Optional[AIService] = None,
        investigation_service: Optional[InvestigationService] = None,
        evidence_service: Optional[EvidenceService] = None,
        recommendation_service: Optional[RecommendationService] = None,
        simulation_service: Optional[SimulationService] = None
    ):
        self.ai_service = ai_service or AIService()
        self.investigation_service = investigation_service or InvestigationService()
        self.evidence_service = evidence_service or EvidenceService()
        self.recommendation_service = recommendation_service or RecommendationService()
        self.simulation_service = simulation_service or SimulationService()

    def explain_investigation_structured(
        self,
        kpi_id: str,
        persona: str = "CFO",
        region: str = "NA-East",
        prev_period_id: str = "2026-Q2",
        curr_period_id: str = "2026-Q3",
        include_recommendations: bool = True,
        include_simulation: bool = False
    ) -> StructuredAIExplanationResponse:
        """Executes full deterministic pipeline, builds context, and invokes Gemini for structured explanation."""
        # 1. Validate Persona
        try:
            persona_profile = resolve_persona(persona)
        except ValueError:
            raise InvalidPersonaAPIError(persona)

        # 2. Retrieve Authoritative Investigation State
        inv_response = self.investigation_service.run_investigation(
            kpi_id=kpi_id,
            region=region,
            prev_period_id=prev_period_id,
            curr_period_id=curr_period_id,
            persona_id=persona_profile.persona.value
        )
        inv_dict = inv_response.model_dump()

        # 3. Retrieve Authoritative Evidence State
        ev_response = self.evidence_service.get_investigation_evidence(kpi_id=kpi_id, region=region)
        ev_list = [e.model_dump() for e in ev_response.evidence]

        # 4. Optional Recommendations State
        recs_list = None
        if include_recommendations:
            try:
                rec_resp = self.recommendation_service.get_recommendations(kpi_id=kpi_id)
                recs_list = [r.model_dump() for r in rec_resp.recommendations]
            except Exception as re:
                logger.warning(f"Could not attach recommendations to AI context: {re}")

        # 5. Optional Simulation Baseline State
        sim_dict = None
        if include_simulation:
            try:
                sim_resp = self.simulation_service.get_baseline()
                sim_dict = sim_resp.model_dump()
            except Exception as se:
                logger.warning(f"Could not attach simulation to AI context: {se}")


        # 6. Execute Grounded AI Reasoning
        start_time = time.perf_counter()
        try:
            ai_resp = self.ai_service.generate_structured_explanation(
                investigation_result=inv_dict,
                evidence_items=ev_list,
                persona=persona_profile.persona.value,
                recommendations=recs_list,
                simulation=sim_dict
            )
            elapsed_ms = round((time.perf_counter() - start_time) * 1000.0, 2)
            logger.info(
                f"[GeminiService] Structured explanation generated for KPI '{kpi_id}' (persona: {persona}) "
                f"in {elapsed_ms}ms (model: {ai_resp.metadata.model}, grounded nodes: {ai_resp.metadata.grounded_evidence_count})"
            )
            return ai_resp
        except AIServiceUnavailableError as sue:
            logger.error(f"[GeminiService] AI service unavailable for KPI '{kpi_id}': {sue}")
            raise AIServiceUnavailableAPIError(str(sue))
        except AIGroundingError as ge:
            logger.error(f"[GeminiService] Grounding validation failed for KPI '{kpi_id}': {ge}")
            raise AIGroundingAPIError(str(ge))

    def explain_investigation_executive(
        self,
        kpi_id: str,
        persona: str = "CFO",
        region: str = "NA-East",
        prev_period_id: str = "2026-Q2",
        curr_period_id: str = "2026-Q3"
    ) -> AIExplanationResponse:
        """Generates executive briefing narrative for leadership personas."""
        try:
            persona_profile = resolve_persona(persona)
        except ValueError:
            raise InvalidPersonaAPIError(persona)

        inv_response = self.investigation_service.run_investigation(
            kpi_id=kpi_id,
            region=region,
            prev_period_id=prev_period_id,
            curr_period_id=curr_period_id,
            persona_id=persona_profile.persona.value
        )
        inv_dict = inv_response.model_dump()

        ev_response = self.evidence_service.get_investigation_evidence(kpi_id=kpi_id, region=region)
        ev_list = [e.model_dump() for e in ev_response.evidence]

        try:
            return self.ai_service.generate_executive_explanation(
                investigation_result=inv_dict,
                evidence_items=ev_list,
                persona=persona_profile.persona.value
            )
        except AIServiceUnavailableError as sue:
            raise AIServiceUnavailableAPIError(str(sue))
        except AIGroundingError as ge:
            raise AIGroundingAPIError(str(ge))

    def explain_driver(
        self,
        kpi_id: str,
        driver_id: str,
        persona: str = "CFO",
        region: str = "NA-East",
        prev_period_id: str = "2026-Q2",
        curr_period_id: str = "2026-Q3"
    ) -> AIDriverExplanationResponse:
        """Generates grounded explanation for a specific ranked driver."""
        try:
            persona_profile = resolve_persona(persona)
        except ValueError:
            raise InvalidPersonaAPIError(persona)

        inv_response = self.investigation_service.run_investigation(
            kpi_id=kpi_id,
            region=region,
            prev_period_id=prev_period_id,
            curr_period_id=curr_period_id,
            persona_id=persona_profile.persona.value
        )
        inv_dict = inv_response.model_dump()

        # Check driver exists in investigation
        valid_driver_ids = {d["driver_id"] for d in inv_dict.get("drivers", [])}
        if driver_id not in valid_driver_ids:
            from backend.app.errors import DriverNotFoundError
            raise DriverNotFoundError(driver_id)

        ev_response = self.evidence_service.get_investigation_evidence(kpi_id=kpi_id, region=region)
        ev_list = [e.model_dump() for e in ev_response.evidence]

        try:
            return self.ai_service.generate_driver_explanation(
                investigation_result=inv_dict,
                evidence_items=ev_list,
                driver_id=driver_id,
                persona=persona_profile.persona.value
            )
        except AIServiceUnavailableError as sue:
            raise AIServiceUnavailableAPIError(str(sue))
        except AIGroundingError as ge:
            raise AIGroundingAPIError(str(ge))
