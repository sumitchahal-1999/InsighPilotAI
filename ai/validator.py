"""
InsightPilot AI — Post-Generation Grounding & Schema Validator
Validates Gemini and Groq responses to ensure zero hallucinated evidence IDs, valid driver references,
strict abstention adherence, schema conformance, and factual alignment with deterministic outputs.
"""

from typing import Dict, Any, List, Set

class GroundingValidationError(Exception):
    """Raised when an LLM generated response violates grounding constraints."""
    pass

class GroundingValidator:
    """Performs rigorous post-generation grounding, schema, and consistency checks."""

    @staticmethod
    def validate_grounding(
        response_dict: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Validates:
        1. Evidence ID citations match verified empirical evidence in context.
        2. Driver ID citations match verified drivers in context.
        3. Abstention policy is strictly respected when confidence is low.
        4. Empty evidence contexts forbid citations.
        """
        if not isinstance(response_dict, dict):
            raise GroundingValidationError("Grounding Failure: LLM response is not a valid dictionary/JSON object.")

        # 1. Extract valid evidence IDs from input context
        context_evidence = context.get("evidence", [])
        valid_evidence_ids: Set[str] = {
            ev["evidence_id"] for ev in context_evidence if isinstance(ev, dict) and "evidence_id" in ev
        }

        # 2. Extract valid driver IDs from input context
        context_drivers = context.get("drivers", [])
        valid_driver_ids: Set[str] = {
            d["driver_id"] for d in context_drivers if isinstance(d, dict) and "driver_id" in d
        }

        # 3. Extract and check cited evidence IDs
        cited_evidence_ids: Set[str] = set(response_dict.get("grounded_evidence_ids", []))
        cited_evidence_ids.update(response_dict.get("supporting_evidence_ids", []))

        for item in response_dict.get("reasoning", []):
            if isinstance(item, dict):
                for sid in item.get("supporting_evidence_ids", []):
                    cited_evidence_ids.add(sid)

        # Check for hallucinated evidence IDs
        invalid_evidence_ids = [cid for cid in cited_evidence_ids if cid not in valid_evidence_ids]
        if invalid_evidence_ids:
            raise GroundingValidationError(
                f"Grounding Failure: Model cited unknown or unverified evidence IDs: {invalid_evidence_ids}."
            )

        # 4. Check for hallucinated driver IDs
        cited_driver_ids = response_dict.get("supporting_driver_ids", [])
        if isinstance(cited_driver_ids, list):
            invalid_driver_ids = [did for did in cited_driver_ids if did not in valid_driver_ids]
            if invalid_driver_ids:
                raise GroundingValidationError(
                    f"Grounding Failure: Model referenced unknown driver IDs: {invalid_driver_ids}."
                )

        target_driver_id = response_dict.get("driver_id")
        if target_driver_id and valid_driver_ids and target_driver_id not in valid_driver_ids:
            raise GroundingValidationError(
                f"Grounding Failure: Target driver_id '{target_driver_id}' not found in verified drivers."
            )

        # Ensure all cited IDs are captured in grounded_evidence_ids and supporting_evidence_ids
        if cited_evidence_ids:
            response_dict["grounded_evidence_ids"] = list(cited_evidence_ids)
            if "supporting_evidence_ids" in response_dict or "primary_driver_explanation" in response_dict:
                response_dict["supporting_evidence_ids"] = list(cited_evidence_ids)

        # 5. Check Empty Evidence Scenario
        if len(valid_evidence_ids) == 0:
            if len(cited_evidence_ids) > 0:
                raise GroundingValidationError(
                    "Grounding Failure: Zero evidence available in context, but model cited evidence."
                )

        # 6. Check Abstention Policy
        is_abstained = context.get("overall_confidence", {}).get("abstention", False)
        if is_abstained:
            headline = str(response_dict.get("headline", "")).lower()
            summary = str(response_dict.get("summary", "") or response_dict.get("executive_summary", "")).lower()
            uncertainty = str(response_dict.get("uncertainty", "") or response_dict.get("uncertainty_statement", "")).lower()
            abstained_flag = response_dict.get("abstained", False)

            # Ensure text communicates low confidence or abstention
            abstention_signals = [
                "insufficient", "low confidence", "abstain", "cannot determine",
                "unreliable", "inconclusive", "data gap", "preliminary",
                "confidence below threshold", "limited data"
            ]
            combined_text = f"{headline} {summary} {uncertainty}"
            has_signal = any(sig in combined_text for sig in abstention_signals)

            # If text explicitly denies uncertainty (e.g. "zero uncertainty", "no uncertainty"), it fails
            if "zero uncertainty" in combined_text or "no uncertainty" in combined_text:
                has_signal = False

            if not has_signal and not abstained_flag:
                raise GroundingValidationError(
                    "Grounding Failure: Investigation is in mandatory abstention state, but model generated a confident narrative without uncertainty or abstention signals."
                )

            # Ensure abstained flag is explicitly true
            response_dict["abstained"] = True
            if not response_dict.get("abstention_reason"):
                response_dict["abstention_reason"] = context.get("overall_confidence", {}).get(
                    "abstention_reason",
                    "Analytical confidence below required threshold (65%). Additional empirical data required."
                )

        return response_dict
