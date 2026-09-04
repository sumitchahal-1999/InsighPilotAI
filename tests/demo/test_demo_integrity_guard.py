"""
InsightPilot AI — Phase 5.9: System-Level Demo Integrity Guard Test Suite
Validates all 13 integrity criteria, safety boundaries, hallucination traps, and credential leakage checks.
"""

import unittest
from ai.demo.integrity_guard import DemoIntegrityGuard


class TestDemoIntegrityGuard(unittest.TestCase):
    """Test suite for the 13-point pre-flight system integrity guard."""

    def setUp(self):
        self.kpi_movement = {
            "id": "north_america_east_revenue",
            "name": "North America East Revenue",
            "previous_value": 15430000.06,
            "current_value": 14200000.05,
            "variance_amount": -1230000.01,
            "percent_change": -7.97,
            "materiality_status": "CRITICAL_NEGATIVE_VARIANCE"
        }
        self.drivers = [
            {"driver_id": "atlanta_dc_stockout", "driver_name": "Atlanta DC Stockout", "contribution_pct": 43.2, "impact_usd": -550000.0},
            {"driver_id": "horizon_pricing_pressure", "driver_name": "Horizon Foods Price Cut", "contribution_pct": 26.1, "impact_usd": -332000.0},
            {"driver_id": "distributor_order_deferral", "driver_name": "Distributor Order Deferrals", "contribution_pct": 18.4, "impact_usd": -234000.0},
            {"driver_id": "sku_mix_shift", "driver_name": "SKU Mix Shift", "contribution_pct": 12.3, "impact_usd": -156000.0}
        ]
        self.evidence_items = [
            {"evidence_id": "EVID_ERP_ATL_STOCKOUT_001", "verification_hash": "sha256:abc12345"},
            {"evidence_id": "EVID_CRM_PO_DEF_006", "verification_hash": "sha256:def67890"}
        ]
        self.confidence = {
            "overall_confidence": 89,
            "confidence_label": "HIGH",
            "tier": "HIGH",
            "abstention": False
        }
        self.ai_explanation = {
            "summary": "Revenue dropped due to Atlanta DC stockout.",
            "grounded_evidence_ids": ["EVID_ERP_ATL_STOCKOUT_001"],
            "supporting_driver_ids": ["atlanta_dc_stockout"]
        }
        self.decision_graph = {
            "nodes": [{"id": "n1"}, {"id": "n2"}],
            "edges": [{"source": "n1", "target": "n2"}]
        }
        self.recommendations = [
            {"recommendation_id": "rec-1", "driver_id": "atlanta_dc_stockout", "action": "Rebalance stock"}
        ]
        self.simulation = {
            "estimated_recovery": {"revenue_recovery_usd": 341422.91}
        }

    # -------------------------------------------------------------------------
    # 1. Canonical State Passes 100%
    # -------------------------------------------------------------------------
    def test_canonical_state_passes_all_13_checks(self):
        """Verifies that the canonical NA-East investigation passes all 13 checks."""
        report = DemoIntegrityGuard.evaluate_integrity(
            kpi_movement=self.kpi_movement,
            drivers=self.drivers,
            evidence_items=self.evidence_items,
            confidence=self.confidence,
            ai_explanation=self.ai_explanation,
            decision_graph=self.decision_graph,
            recommendations=self.recommendations,
            simulation=self.simulation
        )
        self.assertTrue(report.demo_ready)
        self.assertEqual(report.total_checks, 13)
        self.assertEqual(report.passed_checks, 13)
        self.assertEqual(report.failed_checks, 0)

    # -------------------------------------------------------------------------
    # 2. Math Inconsistency Detection
    # -------------------------------------------------------------------------
    def test_kpi_math_inconsistency_fails(self):
        """Detects if variance amount does not match current - previous."""
        bad_kpi = dict(self.kpi_movement)
        bad_kpi["variance_amount"] = 999999.99  # Discrepancy
        report = DemoIntegrityGuard.evaluate_integrity(
            kpi_movement=bad_kpi,
            drivers=self.drivers,
            evidence_items=self.evidence_items,
            confidence=self.confidence,
            ai_explanation=self.ai_explanation,
            decision_graph=self.decision_graph
        )
        self.assertFalse(report.demo_ready)
        failed_ids = [c.check_id for c in report.checks if not c.passed]
        self.assertIn("CHK_02_KPI_MATH_CONSISTENCY", failed_ids)

    # -------------------------------------------------------------------------
    # 3. Abstention Safety Policy Enforcement
    # -------------------------------------------------------------------------
    def test_low_confidence_without_abstention_fails(self):
        """Detects if confidence is <65% but abstention flag is False."""
        bad_conf = {
            "overall_confidence": 52,
            "abstention": False  # Violates policy
        }
        report = DemoIntegrityGuard.evaluate_integrity(
            kpi_movement=self.kpi_movement,
            drivers=self.drivers,
            evidence_items=self.evidence_items,
            confidence=bad_conf,
            ai_explanation=self.ai_explanation,
            decision_graph=self.decision_graph
        )
        self.assertFalse(report.demo_ready)
        failed_ids = [c.check_id for c in report.checks if not c.passed]
        self.assertIn("CHK_08_ABSTENTION_SAFETY_POLICY", failed_ids)

    # -------------------------------------------------------------------------
    # 4. AI Hallucinated Citation Detection
    # -------------------------------------------------------------------------
    def test_hallucinated_evidence_citation_fails(self):
        """Rejects AI explanation citing non-existent evidence IDs."""
        bad_ai = {
            "summary": "Fabricated explanation",
            "grounded_evidence_ids": ["EVID_FAKE_INVENTED_999"]
        }
        report = DemoIntegrityGuard.evaluate_integrity(
            kpi_movement=self.kpi_movement,
            drivers=self.drivers,
            evidence_items=self.evidence_items,
            confidence=self.confidence,
            ai_explanation=bad_ai,
            decision_graph=self.decision_graph
        )
        self.assertFalse(report.demo_ready)
        failed_ids = [c.check_id for c in report.checks if not c.passed]
        self.assertIn("CHK_09_AI_GROUNDING_INTEGRITY", failed_ids)

    # -------------------------------------------------------------------------
    # 5. Zero Secret Leakage Enforcement
    # -------------------------------------------------------------------------
    def test_secret_token_in_payload_fails(self):
        """Rejects payload if an API key or auth token appears anywhere in data."""
        bad_kpi = dict(self.kpi_movement)
        bad_kpi["name"] = "Leaked Token: gsk_fake_secret_key_12345"
        report = DemoIntegrityGuard.evaluate_integrity(
            kpi_movement=bad_kpi,
            drivers=self.drivers,
            evidence_items=self.evidence_items,
            confidence=self.confidence,
            ai_explanation=self.ai_explanation,
            decision_graph=self.decision_graph
        )
        self.assertFalse(report.demo_ready)
        failed_ids = [c.check_id for c in report.checks if not c.passed]
        self.assertIn("CHK_13_ZERO_SECRET_LEAKAGE", failed_ids)


if __name__ == "__main__":
    unittest.main()
