"""
InsightPilot AI — Grounding Validator Unit Tests
Tests strict post-generation verification, hallucination rejection, and abstention compliance.
"""

import unittest
from ai.validator import GroundingValidator, GroundingValidationError

class TestGroundingValidator(unittest.TestCase):

    def setUp(self):
        self.validator = GroundingValidator()
        self.sample_context = {
            "evidence": [
                {"evidence_id": "EVID_ERP_ATL_STOCKOUT_001"},
                {"evidence_id": "EVID_ERP_TRANSFER_LOG_002"},
                {"evidence_id": "EVID_CRM_PO_DEF_006"}
            ],
            "overall_confidence": {
                "score": 89,
                "abstention": False
            }
        }

    def test_valid_grounding_passes(self):
        response_dict = {
            "headline": "Revenue down 7.97%",
            "grounded_evidence_ids": ["EVID_ERP_ATL_STOCKOUT_001", "EVID_CRM_PO_DEF_006"]
        }
        res = self.validator.validate_grounding(response_dict, self.sample_context)
        self.assertEqual(res, response_dict)

    def test_hallucinated_evidence_id_fails(self):
        response_dict = {
            "headline": "Revenue down 7.97%",
            "grounded_evidence_ids": [
                "EVID_ERP_ATL_STOCKOUT_001",
                "EVID_FAKE_INVENTED_EVIDENCE_999" # Hallucinated ID
            ]
        }
        with self.assertRaises(GroundingValidationError) as ctx:
            self.validator.validate_grounding(response_dict, self.sample_context)
        self.assertIn("unknown or unverified evidence IDs", str(ctx.exception))

    def test_abstention_requires_uncertainty_statement(self):
        abstained_context = {
            "evidence": [{"evidence_id": "EVID_01"}],
            "overall_confidence": {
                "score": 45,
                "abstention": True,
                "abstention_reason": "Low confidence"
            }
        }
        
        # A confident response without uncertainty indicators should fail validation
        confident_response = {
            "headline": "Revenue declined solely due to warehouse mismanagement.",
            "situation": "Clear operational failure.",
            "uncertainty": "No doubts present.",
            "grounded_evidence_ids": ["EVID_01"]
        }
        with self.assertRaises(GroundingValidationError) as ctx:
            self.validator.validate_grounding(confident_response, abstained_context)
        self.assertIn("abstention state", str(ctx.exception))


        # A response acknowledging uncertainty passes
        uncertain_response = {
            "headline": "Analytical conclusion uncertain due to insufficient evidence.",
            "situation": "Available signals are low confidence.",
            "uncertainty": "Insufficient historical baseline to establish primary driver.",
            "grounded_evidence_ids": ["EVID_01"]
        }
        res = self.validator.validate_grounding(uncertain_response, abstained_context)
        self.assertEqual(res, uncertain_response)

    def test_empty_evidence_context_forbids_citations(self):
        empty_context = {
            "evidence": [],
            "overall_confidence": {"abstention": False}
        }
        bad_response = {
            "headline": "Revenue dropped",
            "grounded_evidence_ids": ["EVID_ERP_ATL_STOCKOUT_001"]
        }
        with self.assertRaises(GroundingValidationError):
            self.validator.validate_grounding(bad_response, empty_context)

if __name__ == "__main__":
    unittest.main()
