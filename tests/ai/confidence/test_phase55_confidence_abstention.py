"""
InsightPilot AI — Phase 5.5 Multi-Factor Confidence & Abstention Guard Tests
Tests evidence sufficiency, quality, corroboration, lineage integrity,
threshold banding, critical abstention safety gates, persona invariance, and mandatory LLM bypass.
"""

import unittest
from unittest.mock import MagicMock, patch
from analytics.confidence_engine import ConfidenceEngine
from ai.langgraph.graph import run_investigation_workflow
from ai.providers.groq_provider import GroqProvider
from ai.orchestration.provider_router import AIProviderRouter

class TestPhase55ConfidenceAbstention(unittest.TestCase):

    def setUp(self):
        self.engine = ConfidenceEngine(abstention_threshold=65)
        self.canonical_drivers = [
            {
                "driver_id": "atlanta_dc_stockout",
                "driver_name": "Atlanta DC Stockout",
                "contribution_pct": 43.2,
                "confidence_score": 94,
                "evidence_ids": [
                    "EVID_ERP_ATL_STOCKOUT_001",
                    "EVID_ERP_TRANSFER_LOG_002",
                    "EVID_ZENDESK_ATL_DELAY_003"
                ]
            },
            {
                "driver_id": "sku_8821_sales_volume",
                "driver_name": "SKU-8821 Sales Contraction",
                "contribution_pct": 26.7,
                "confidence_score": 89,
                "evidence_ids": [
                    "EVID_CRM_SKU8821_SALES_004",
                    "EVID_ERP_BOM_MARGIN_005"
                ]
            },
            {
                "driver_id": "distributor_orders",
                "driver_name": "Distributor PO Deferrals",
                "contribution_pct": 18.8,
                "confidence_score": 85,
                "evidence_ids": [
                    "EVID_CRM_PO_DEF_006",
                    "EVID_COMM_DIST_EMAIL_007"
                ]
            },
            {
                "driver_id": "competitor_horizon_pricing",
                "driver_name": "Competitor Horizon Promo",
                "contribution_pct": 11.3,
                "confidence_score": 78,
                "evidence_ids": [
                    "EVID_MKT_HORIZON_PROMO_008",
                    "EVID_ZENDESK_COMP_FEEDBACK_009"
                ]
            }
        ]
        self.canonical_evidence = [
            {"evidence_id": "EVID_ERP_ATL_STOCKOUT_001", "source_system": "SAP_ERP_INVENTORY", "confidence": 95},
            {"evidence_id": "EVID_ERP_TRANSFER_LOG_002", "source_system": "SAP_ERP_TRANSFER", "confidence": 92},
            {"evidence_id": "EVID_ZENDESK_ATL_DELAY_003", "source_system": "ZENDESK_SUPPORT", "confidence": 88},
            {"evidence_id": "EVID_CRM_SKU8821_SALES_004", "source_system": "SALESFORCE_CRM", "confidence": 90},
            {"evidence_id": "EVID_ERP_BOM_MARGIN_005", "source_system": "SAP_ERP_COPA", "confidence": 85},
            {"evidence_id": "EVID_CRM_PO_DEF_006", "source_system": "SALESFORCE_CRM", "confidence": 86},
            {"evidence_id": "EVID_COMM_DIST_EMAIL_007", "source_system": "OUTLOOK_COMM", "confidence": 80},
            {"evidence_id": "EVID_MKT_HORIZON_PROMO_008", "source_system": "PRICE_SPIDER_MKT", "confidence": 82},
            {"evidence_id": "EVID_ZENDESK_COMP_FEEDBACK_009", "source_system": "ZENDESK_SUPPORT", "confidence": 84}
        ]

    # -------------------------------------------------------------------------
    # TEST 1: High Confidence Investigation
    # -------------------------------------------------------------------------
    def test_high_confidence_investigation(self):
        """Full evidence, validated lineage, and multi-domain corroboration yield HIGH confidence."""
        res = self.engine.evaluate_investigation_confidence(
            drivers=self.canonical_drivers,
            evidence_items=self.canonical_evidence,
            validated_evidence=self.canonical_evidence,
            lineage_valid=True
        )
        self.assertEqual(res["overall_confidence"], 89)
        self.assertEqual(res["tier"], "HIGH")
        self.assertEqual(res["confidence_label"], "HIGH")
        self.assertFalse(res["abstention"])
        self.assertFalse(res["abstain"])
        self.assertIsNone(res["abstention_reason"])
        self.assertTrue(res["evidence_sufficiency"]["sufficient"])
        self.assertEqual(res["evidence_sufficiency"]["evidence_count"], 9)
        self.assertGreaterEqual(res["evidence_sufficiency"]["corroborating_domains"], 3)

    # -------------------------------------------------------------------------
    # TEST 2: Low Confidence Investigation (< 65)
    # -------------------------------------------------------------------------
    def test_low_confidence_mandatory_abstention(self):
        """Low individual driver scores yield confidence < 65 and trigger mandatory abstention."""
        low_drivers = [
            {"driver_id": "d1", "contribution_pct": 50.0, "confidence_score": 40, "evidence_ids": ["E1"]},
            {"driver_id": "d2", "contribution_pct": 50.0, "confidence_score": 42, "evidence_ids": ["E2"]}
        ]
        low_evidence = [
            {"evidence_id": "E1", "source_system": "GENERAL", "confidence": 40},
            {"evidence_id": "E2", "source_system": "GENERAL", "confidence": 42}
        ]
        res = self.engine.evaluate_investigation_confidence(
            drivers=low_drivers,
            evidence_items=low_evidence,
            validated_evidence=low_evidence,
            lineage_valid=True
        )
        self.assertLess(res["overall_confidence"], 65)
        self.assertEqual(res["tier"], "LOW")
        self.assertEqual(res["confidence_label"], "LOW")
        self.assertTrue(res["abstention"])
        self.assertTrue(res["abstain"])
        self.assertIn("LOW_CONFIDENCE", res["reason_codes"])

    # -------------------------------------------------------------------------
    # TEST 3: Missing Primary Driver Evidence
    # -------------------------------------------------------------------------
    def test_missing_primary_driver_evidence_abstains(self):
        """If primary driver has zero validated evidence records, mandatory abstention triggers."""
        # Top driver has no evidence in validated list
        evidence_without_primary = [
            {"evidence_id": "EVID_CRM_PO_DEF_006", "source_system": "CRM", "confidence": 90}
        ]
        res = self.engine.evaluate_investigation_confidence(
            drivers=self.canonical_drivers,
            evidence_items=evidence_without_primary,
            validated_evidence=evidence_without_primary,
            lineage_valid=True
        )
        self.assertTrue(res["abstention"])
        self.assertIn("PRIMARY_DRIVER_UNSUPPORTED", res["reason_codes"])
        self.assertFalse(res["evidence_sufficiency"]["sufficient"])

    # -------------------------------------------------------------------------
    # TEST 4: Invalid Lineage Failure
    # -------------------------------------------------------------------------
    def test_invalid_lineage_triggers_abstention(self):
        """Cryptographic lineage failure causes immediate safety gate abstention."""
        res = self.engine.evaluate_investigation_confidence(
            drivers=self.canonical_drivers,
            evidence_items=self.canonical_evidence,
            validated_evidence=self.canonical_evidence,
            lineage_valid=False
        )
        self.assertTrue(res["abstention"])
        self.assertIn("LINEAGE_FAILURE", res["reason_codes"])
        self.assertEqual(res["factors"]["lineage_integrity"], 0.0)

    # -------------------------------------------------------------------------
    # TEST 5: No Valid Evidence
    # -------------------------------------------------------------------------
    def test_no_valid_evidence_triggers_abstention(self):
        """Zero validated evidence records causes immediate abstention."""
        res = self.engine.evaluate_investigation_confidence(
            drivers=self.canonical_drivers,
            evidence_items=[],
            validated_evidence=[],
            lineage_valid=True
        )
        self.assertTrue(res["abstention"])
        self.assertIn("NO_VALID_EVIDENCE", res["reason_codes"])
        self.assertEqual(res["evidence_sufficiency"]["evidence_count"], 0)

    # -------------------------------------------------------------------------
    # TEST 6: Confidence Below 65 Banding
    # -------------------------------------------------------------------------
    def test_confidence_below_65_banding(self):
        """Scores < 65 are banded to LOW tier and mandate abstention."""
        res = self.engine.evaluate_synthetic_low_confidence_scenario()
        self.assertLess(res["overall_confidence"], 65)
        self.assertEqual(res["tier"], "LOW")
        self.assertTrue(res["abstention"])

    # -------------------------------------------------------------------------
    # TEST 7: Threshold Boundary (Score >= 65)
    # -------------------------------------------------------------------------
    def test_confidence_at_threshold_boundary(self):
        """Moderate drivers reaching >= 65 score pass abstention threshold."""
        moderate_drivers = [
            {"driver_id": "d1", "contribution_pct": 50.0, "confidence_score": 75, "evidence_ids": ["E1", "E2"]},
            {"driver_id": "d2", "contribution_pct": 50.0, "confidence_score": 70, "evidence_ids": ["E3"]}
        ]
        moderate_evidence = [
            {"evidence_id": "E1", "source_system": "SAP_ERP", "confidence": 75},
            {"evidence_id": "E2", "source_system": "CRM", "confidence": 72},
            {"evidence_id": "E3", "source_system": "ZENDESK", "confidence": 70}
        ]
        res = self.engine.evaluate_investigation_confidence(
            drivers=moderate_drivers,
            evidence_items=moderate_evidence,
            validated_evidence=moderate_evidence,
            lineage_valid=True
        )
        self.assertGreaterEqual(res["overall_confidence"], 65)
        self.assertFalse(res["abstention"])
        self.assertIn(res["tier"], ["MODERATE", "HIGH"])

    # -------------------------------------------------------------------------
    # TEST 8: Persona Invariance
    # -------------------------------------------------------------------------
    def test_persona_invariance(self):
        """CFO vs Sales Manager personas have 100% identical confidence scores and factors."""
        state_cfo = run_investigation_workflow(kpi_id="north_america_east_revenue", persona="CFO")
        state_sales = run_investigation_workflow(kpi_id="north_america_east_revenue", persona="REGIONAL_SALES_MANAGER")

        self.assertEqual(state_cfo["confidence"]["overall_confidence"], state_sales["confidence"]["overall_confidence"])
        self.assertEqual(state_cfo["confidence"]["tier"], state_sales["confidence"]["tier"])
        self.assertEqual(state_cfo["confidence"]["abstention"], state_sales["confidence"]["abstention"])
        self.assertEqual(state_cfo["confidence"]["factors"], state_sales["confidence"]["factors"])

    # -------------------------------------------------------------------------
    # TEST 9: Mandatory LLM Bypass on Abstention
    # -------------------------------------------------------------------------
    def test_mandatory_llm_bypass_on_abstention(self):
        """When abstention is active, provider router is never called."""
        mock_groq = MagicMock(spec=GroqProvider)
        mock_groq.name = "groq"
        mock_groq.is_configured.return_value = True

        with patch("analytics.confidence_engine.ConfidenceEngine.evaluate_investigation_confidence") as mock_conf:
            mock_conf.return_value = {
                "overall_confidence": 35,
                "confidence_score": 35.0,
                "confidence_label": "LOW",
                "tier": "LOW",
                "abstention": True,
                "abstain": True,
                "abstention_reason": "Low confidence telemetry deficit.",
                "reason_codes": ["LOW_CONFIDENCE"],
                "factors": {},
                "evidence_sufficiency": {"sufficient": False}
            }

            with patch("ai.langgraph.nodes.investigation_nodes.provider_router", AIProviderRouter(groq_provider=mock_groq)):
                state = run_investigation_workflow(kpi_id="north_america_east_revenue", persona="CFO")

                # Verify LLM generation was bypassed
                mock_groq.generate.assert_not_called()
                self.assertTrue(state["abstention"])
                self.assertIn("abstention_node", state["nodes_executed"])
                self.assertNotIn("ai_invocation_node", state["nodes_executed"])
                self.assertFalse(state["provider_metadata"]["provider_called"])
                self.assertIsNone(state["provider_metadata"]["provider"])

    # -------------------------------------------------------------------------
    # TEST 10: Baseline Regression Parity
    # -------------------------------------------------------------------------
    def test_canonical_baseline_regression_parity(self):
        """Canonical investigation retains 88 score, HIGH tier, and non-abstained status."""
        state = run_investigation_workflow(kpi_id="north_america_east_revenue", persona="CFO")
        self.assertEqual(state["confidence"]["overall_confidence"], 89)
        self.assertEqual(state["confidence"]["tier"], "HIGH")
        self.assertFalse(state["confidence"]["abstention"])
        self.assertAlmostEqual(state["kpi_movement"]["variance_amount"], -1230000.01, delta=0.01)

if __name__ == "__main__":
    unittest.main()
