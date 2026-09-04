"""
InsightPilot AI — AI Reasoning Service Tests
Tests structured explanation, executive explanation, and driver explanation using mocked Gemini client (zero external API calls).
"""

import unittest
from unittest.mock import MagicMock
from ai.service import AIService, AIServiceUnavailableError, AIGroundingError
from ai.client import GeminiClient, GeminiAPIError
from ai.schemas.persona import resolve_persona
from analytics.investigation_engine import InvestigationEngine
from evidence.evidence_engine import EvidenceEngine

class TestAIService(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.inv_engine = InvestigationEngine()
        cls.ev_engine = EvidenceEngine(cls.inv_engine.loader)
        
        # Real deterministic outputs
        cls.inv_res = cls.inv_engine.run_investigation("north_america_east_revenue", "NA-East", "2026-Q2", "2026-Q3", "CFO")
        ev_bundle = cls.ev_engine.get_all_evidence_for_investigation("NA-East")
        cls.evidence_items = ev_bundle["all_evidence_nodes"]

    def test_structured_explanation_generation(self):
        mock_client = MagicMock(spec=GeminiClient)
        mock_client.generate_json.return_value = (
            {
                "summary": "North America East revenue contracted 7.97% (-$1.23M) primarily due to Atlanta DC inventory availability dropping to 68.2%.",
                "reasoning": [
                    {
                        "statement": "Atlanta DC experienced inventory stockout on SKU-8821 causing $550k in unfulfilled demand.",
                        "supporting_evidence_ids": ["EVID_ERP_ATL_STOCKOUT_001"],
                        "confidence": 94
                    },
                    {
                        "statement": "Wholesale distributor Apex East deferred purchase orders pending inventory replenishment.",
                        "supporting_evidence_ids": ["EVID_CRM_PO_DEF_006"],
                        "confidence": 85
                    }
                ],
                "primary_driver_explanation": "Atlanta DC stockout (43.2% contribution) is the primary driver substantiated by SAP inventory snapshots and expedited freight surcharges.",
                "secondary_driver_explanation": "Secondary drivers include SKU-8821 volume contraction and distributor order deferrals.",
                "uncertainty": "Competitor pricing impact is an analytical inference from regional scrapers.",
                "recommended_next_step": "Execute emergency inter-DC transfer from Charlotte to Atlanta.",
                "abstained": False,
                "abstention_reason": None,
                "grounded_evidence_ids": [
                    "EVID_ERP_ATL_STOCKOUT_001",
                    "EVID_CRM_PO_DEF_006"
                ]
            },
            {
                "model": "gemini-2.5-flash",
                "latency_ms": 710.0,
                "prompt_tokens": 480,
                "completion_tokens": 220,
                "total_tokens": 700
            }
        )

        service = AIService(client=mock_client)
        resp = service.generate_structured_explanation(
            investigation_result=self.inv_res,
            evidence_items=self.evidence_items,
            persona="CFO"
        )

        self.assertEqual(resp.investigation_id, self.inv_res["investigation_id"])
        self.assertEqual(resp.persona, "CFO")
        self.assertIn("7.97%", resp.explanation.summary)
        self.assertEqual(len(resp.explanation.reasoning), 2)
        self.assertEqual(resp.explanation.reasoning[0].confidence, 94)
        self.assertEqual(len(resp.explanation.grounded_evidence_ids), 2)
        self.assertFalse(resp.explanation.abstained)
        self.assertEqual(resp.metadata.validation_status, "VERIFIED_GROUNDED")
        self.assertEqual(resp.metadata.total_tokens, 700)

    def test_executive_explanation_generation(self):
        mock_client = MagicMock(spec=GeminiClient)
        mock_client.generate_json.return_value = (
            {
                "headline": "North America East revenue declined 7.97% driven by Atlanta DC stockouts and commercial order deferrals.",
                "situation": "Q3 2026 revenue of $14.20M fell $1.23M (-7.97%) below the Q2 baseline of $15.43M.",
                "diagnosis": "The primary operational driver was the Atlanta DC stockout (43.2% contribution), compounded by SKU-8821 sales volume contraction (26.7%), distributor PO deferrals (18.8%), and competitor Horizon Foods price discounting (11.3%).",
                "evidence_summary": "ERP inventory logs confirm availability dropped to 68.2%, supported by $291k in expedited freight and customer escalation tickets.",
                "uncertainty": "External competitor price impact remains an analytical estimate based on regional scrapers and customer feedback.",
                "executive_takeaway": "Immediate priority is stabilizing Atlanta DC inventory replenishment to recover deferred wholesale orders.",
                "grounded_evidence_ids": [
                    "EVID_ERP_ATL_STOCKOUT_001",
                    "EVID_ERP_TRANSFER_LOG_002",
                    "EVID_CRM_PO_DEF_006"
                ]
            },
            {
                "model": "gemini-2.5-flash",
                "latency_ms": 750.0,
                "prompt_tokens": 420,
                "completion_tokens": 190,
                "total_tokens": 610
            }
        )

        service = AIService(client=mock_client)
        resp = service.generate_executive_explanation(self.inv_res, self.evidence_items, persona="CFO")

        self.assertEqual(resp.investigation_id, self.inv_res["investigation_id"])
        self.assertEqual(resp.persona, "CFO")
        self.assertIn("7.97%", resp.explanation.headline)
        self.assertEqual(len(resp.explanation.grounded_evidence_ids), 3)
        self.assertEqual(resp.metadata.validation_status, "VERIFIED_GROUNDED")
        self.assertEqual(resp.metadata.prompt_tokens, 420)
        self.assertEqual(resp.metadata.total_tokens, 610)

    def test_driver_explanation_generation(self):
        mock_client = MagicMock(spec=GeminiClient)
        mock_client.generate_json.return_value = (
            {
                "driver_id": "atlanta_dc_stockout",
                "driver_name": "Atlanta DC Stockout",
                "contribution_summary": "Rank #1 explanatory driver contributing 43.2% (-$550,000.00) to the revenue deficit.",
                "evidence_rationale": "Inventory telemetry snapshots show availability fell to 68.2% during Aug 1-19, resulting in 4,400 unmet demand units.",
                "operational_context": "Fulfillment constraints caused backorders for Tier-1 distributors across NA-East.",
                "uncertainty": "Confidence is rated HIGH (94%) based on direct ERP telemetry.",
                "grounded_evidence_ids": ["EVID_ERP_ATL_STOCKOUT_001", "EVID_ERP_TRANSFER_LOG_002"]
            },
            {
                "model": "gemini-2.5-flash",
                "latency_ms": 620.0,
                "prompt_tokens": 310,
                "completion_tokens": 140,
                "total_tokens": 450
            }
        )

        service = AIService(client=mock_client)
        resp = service.generate_driver_explanation(self.inv_res, self.evidence_items, "atlanta_dc_stockout", persona="CFO")

        self.assertEqual(resp.driver_id, "atlanta_dc_stockout")
        self.assertEqual(resp.explanation.driver_name, "Atlanta DC Stockout")
        self.assertEqual(len(resp.explanation.grounded_evidence_ids), 2)
        self.assertEqual(resp.metadata.validation_status, "VERIFIED_GROUNDED")

    def test_persona_resolution(self):
        cfo = resolve_persona("CFO")
        self.assertEqual(cfo.role_title, "Chief Financial Officer")
        self.assertIn("Revenue and gross margin variance", cfo.focus_areas)

        rsm = resolve_persona("REGIONAL_SALES_MANAGER")
        self.assertEqual(rsm.role_title, "Regional Sales & Operations Manager")
        self.assertIn("Distribution center fulfillment and stockouts", rsm.focus_areas)

        with self.assertRaises(ValueError):
            resolve_persona("INVALID_ROLE")

if __name__ == "__main__":
    unittest.main()
