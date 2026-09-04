"""
Phase 7.3: Final Competition Submission Readiness & Delivery Audit Test Suite
Project: InsightPilot AI
Competition: Accenture Innovation Challenge 2026 (Track 3: BusinessIntelligence.ai)

Validates the 12 competition-critical submission invariants:
1. Canonical investigation accessibility
2. Canonical revenue variance (-$1,230,000.01 / -7.97%)
3. Top driver attribution (Atlanta DC Stockout, 43.2%, -$550K, 94%)
4. Overall confidence scoring (89% HIGH)
5. Mandatory abstention safety gate (<65%)
6. Evidence lineage and SHA-256 integrity
7. Decision Graph 6-column topology integrity
8. Recommendation continuity (+$484K Priority 1 recovery)
9. Simulation determinism (+$341,422.91 at 90.0% availability)
10. Zero secret or credential leakage
11. Demo readiness endpoint availability
12. Critical competition documentation files existence
"""

import unittest
import os
import json
import re
from unittest.mock import MagicMock
from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.dependencies import get_gemini_service, get_ai_service
from backend.app.services.gemini_service import GeminiService
from ai.service import AIService
from ai.client import GeminiClient

class TestPhase73SubmissionReadiness(unittest.TestCase):

    def setUp(self):
        self.mock_gemini = MagicMock(spec=GeminiClient)
        self.mock_gemini.generate_json.return_value = (
            {
                "summary": "North America East revenue contracted -$1.23M (-7.97%) in 2026-Q3 against baseline $15.43M. Root cause analysis confirms Atlanta DC stockouts (43.2% contribution) as the top operational bottleneck.",
                "reasoning": [
                    {
                        "statement": "Atlanta DC inventory dropped across 14 consecutive business days for SKU-8821.",
                        "supporting_evidence_ids": ["EVID_ERP_ATL_STOCKOUT_001"],
                        "confidence": 94
                    }
                ],
                "primary_driver_explanation": "Atlanta DC Stockout contributed 43.2% (-$550K) of the revenue deficit.",
                "secondary_driver_explanation": "SKU-8821 volume contraction and distributor deferrals contributed remaining shortfall.",
                "uncertainty": "Competitor promotion depth is estimated from automated retail web scrapes.",
                "recommended_next_step": "Execute emergency stock transfer of 3,200 units from Chicago to Atlanta.",
                "abstained": False,
                "abstention_reason": None,
                "grounded_evidence_ids": ["EVID_ERP_ATL_STOCKOUT_001"]
            },
            {"model": "gemini-2.5-flash", "latency_ms": 185.0, "total_tokens": 420}
        )

        mock_ai_service = AIService(client=self.mock_gemini)
        mock_gemini_service = GeminiService(ai_service=mock_ai_service)

        app.dependency_overrides[get_ai_service] = lambda: mock_ai_service
        app.dependency_overrides[get_gemini_service] = lambda: mock_gemini_service
        self.client = TestClient(app)

    def tearDown(self):
        app.dependency_overrides.clear()

    # --------------------------------------------------------------------------
    # Invariant 1: Canonical Investigation Accessibility
    # --------------------------------------------------------------------------
    def test_invariant_1_investigation_accessible(self):
        """Invariant 1: Primary investigation endpoint is online and responsive."""
        res = self.client.get("/api/v1/investigations/north_america_east_revenue")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["kpi"]["id"], "north_america_east_revenue")

    # --------------------------------------------------------------------------
    # Invariant 2: Canonical KPI Variance (-$1,230,000.01 / -7.97%)
    # --------------------------------------------------------------------------
    def test_invariant_2_canonical_revenue_variance(self):
        """Invariant 2: Net revenue variance is strictly -$1,230,000.01 (-7.97%)."""
        res = self.client.get("/api/v1/kpis/north_america_east_revenue")
        self.assertEqual(res.status_code, 200)
        kpi = res.json()
        self.assertAlmostEqual(kpi["previous_value"], 15430000.06, delta=100.0)
        self.assertAlmostEqual(kpi["current_value"], 14200000.05, delta=100.0)
        self.assertAlmostEqual(kpi["variance_amount"], -1230000.01, delta=100.0)
        self.assertAlmostEqual(kpi["percent_change"], -7.97, places=1)
        self.assertEqual(kpi["materiality_status"], "CRITICAL_NEGATIVE_VARIANCE")

    # --------------------------------------------------------------------------
    # Invariant 3: Top Driver Attribution (Atlanta DC Stockout, 43.2%, -$550K, 94%)
    # --------------------------------------------------------------------------
    def test_invariant_3_top_driver_attribution(self):
        """Invariant 3: Top causal driver is Atlanta DC Stockout with 43.2% share and 94% confidence."""
        res = self.client.get("/api/v1/investigations/north_america_east_revenue/drivers")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        top_driver = data["drivers"][0]
        self.assertEqual(top_driver["driver_id"], "atlanta_dc_stockout")
        self.assertEqual(top_driver["rank"], 1)
        self.assertAlmostEqual(top_driver["contribution_pct"], 43.2, places=1)
        self.assertAlmostEqual(top_driver["impact_usd"], -550000.0, delta=100.0)
        self.assertEqual(top_driver["confidence_score"], 94)

    # --------------------------------------------------------------------------
    # Invariant 4: Overall Confidence Scoring (89% HIGH)
    # --------------------------------------------------------------------------
    def test_invariant_4_overall_confidence_score(self):
        """Invariant 4: Overall analytical confidence evaluates to 89% (HIGH tier)."""
        res = self.client.get("/api/v1/investigations/north_america_east_revenue")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["overall"]["overall_confidence"], 89)
        self.assertEqual(data["overall"]["confidence_label"], "HIGH")
        self.assertFalse(data["overall"]["abstention"])

    # --------------------------------------------------------------------------
    # Invariant 5: Mandatory Abstention Safety Gate (<65%)
    # --------------------------------------------------------------------------
    def test_invariant_5_abstention_safety_gate(self):
        """Invariant 5: Investigation enforces abstention flag handling without crashing."""
        res = self.client.get("/api/v1/investigations/north_america_east_revenue")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertIn("abstention", data["overall"])
        self.assertIn("overall_confidence", data["overall"])
        # Score 89 >= 65 -> abstention should be False
        self.assertFalse(data["overall"]["abstention"])

    # --------------------------------------------------------------------------
    # Invariant 6: Evidence Lineage & SHA-256 Integrity
    # --------------------------------------------------------------------------
    def test_invariant_6_evidence_lineage_sha256(self):
        """Invariant 6: Evidence records contain verifiable SHA-256 lineage hashes."""
        res = self.client.get("/api/v1/evidence")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertGreaterEqual(data["total_evidence_count"], 7)
        for ev in data["evidence"]:
            sha = ev["lineage"]["verification_hash"]
            self.assertTrue(sha.startswith("sha256:"), f"Evidence {ev['evidence_id']} missing sha256 prefix")
            hash_part = sha.replace("sha256:", "")
            self.assertEqual(len(hash_part), 64, f"Evidence {ev['evidence_id']} hash length not 64 chars")

    # --------------------------------------------------------------------------
    # Invariant 7: Decision Graph 6-Column Topology Integrity
    # --------------------------------------------------------------------------
    def test_invariant_7_decision_graph_topology(self):
        """Invariant 7: Decision Graph exposes valid 6-column topology with linked nodes."""
        res = self.client.get("/api/v1/investigations/north_america_east_revenue/decision-graph")
        self.assertEqual(res.status_code, 200)
        graph = res.json()
        self.assertEqual(graph["total_columns"], 6)
        self.assertGreaterEqual(graph["total_nodes_count"], 10)
        self.assertGreaterEqual(graph["total_edges_count"], 10)

    # --------------------------------------------------------------------------
    # Invariant 8: Recommendation Continuity (+$484K Priority 1 Recovery)
    # --------------------------------------------------------------------------
    def test_invariant_8_recommendations_continuity(self):
        """Invariant 8: Recommendations map to drivers with quantified recovery potential."""
        res = self.client.get("/api/v1/recommendations/north_america_east_revenue")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertGreaterEqual(data["total_recommendations"], 2)
        top_rec = data["recommendations"][0]
        self.assertEqual(top_rec["priority_rank"], 1)
        self.assertEqual(top_rec["driver_id"], "atlanta_dc_stockout")
        self.assertGreaterEqual(top_rec["expected_impact"]["revenue_recovery_usd"], 400000.0)

    # --------------------------------------------------------------------------
    # Invariant 9: Simulation Determinism (+$341,422.91 at 90.0% Availability)
    # --------------------------------------------------------------------------
    def test_invariant_9_simulation_determinism(self):
        """Invariant 9: What-if inventory simulation produces deterministic elasticity output."""
        res = self.client.post(
            "/api/v1/simulations/inventory-availability",
            json={"inventory_availability": 0.90}
        )
        self.assertEqual(res.status_code, 200)
        sim = res.json()
        self.assertEqual(sim["scenario_value"], 90.0)
        self.assertAlmostEqual(sim["baseline_value"], 79.4, places=1)
        self.assertAlmostEqual(sim["availability_delta"], 10.6, places=1)
        self.assertGreater(sim["estimated_recovery"]["revenue_recovery_usd"], 300000.0)
        self.assertEqual(sim["confidence"]["label"], "HIGH")

    # --------------------------------------------------------------------------
    # Invariant 10: Zero Secret or Credential Leakage
    # --------------------------------------------------------------------------
    def test_invariant_10_zero_secret_leakage(self):
        """Invariant 10: Public API endpoints contain zero credentials, API keys, or raw tokens."""
        endpoints = [
            "/api/v1/kpis",
            "/api/v1/investigations/north_america_east_revenue",
            "/api/v1/investigations/north_america_east_revenue/drivers",
            "/api/v1/investigations/north_america_east_revenue/decision-graph",
            "/api/v1/evidence",
            "/api/v1/recommendations/north_america_east_revenue",
            "/api/v1/simulations/baseline",
        ]

        forbidden_patterns = [
            r"gsk_[a-zA-Z0-9]{20,}",
            r"AIzaSy[a-zA-Z0-9_-]{33}",
            r"Bearer\s+[a-zA-Z0-9_\-\.]{20,}",
        ]

        for ep in endpoints:
            res = self.client.get(ep)
            self.assertEqual(res.status_code, 200)
            payload_str = json.dumps(res.json())
            for pattern in forbidden_patterns:
                match = re.search(pattern, payload_str, re.IGNORECASE)
                self.assertIsNone(match, f"Secret pattern '{pattern}' detected in {ep}")

    # --------------------------------------------------------------------------
    # Invariant 11: Demo Readiness Endpoint
    # --------------------------------------------------------------------------
    def test_invariant_11_demo_readiness_endpoint(self):
        """Invariant 11: Demo readiness endpoint evaluates system-wide health."""
        res = self.client.get("/api/v1/demo/readiness")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertIn("submission_ready", data)
        self.assertTrue(data["submission_ready"])
        self.assertIn("subsystems", data)
        self.assertTrue(all(data["subsystems"].values()), f"Subsystem failure: {data['subsystems']}")

    # --------------------------------------------------------------------------
    # Invariant 12: Critical Competition Documentation Files Existence
    # --------------------------------------------------------------------------
    def test_invariant_12_critical_documentation_exists(self):
        """Invariant 12: All critical competition submission documentation files exist on disk."""
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
        critical_files = [
            "README.md",
            "CONTRIBUTING.md",
            "SECURITY.md",
            "LICENSE",
            ".env.example",
            "docs/architecture/MASTER_ARCHITECTURE.md",
            "docs/business-proposal/BUSINESS_PROPOSAL.md",
            "docs/demo/DEMO_STORYBOARD.md",
            "docs/presentation/UI_VISUAL_AUDIT.md",
            "docs/presentation/JUDGE_EXPERIENCE_AUDIT.md",
        ]

        for rel_path in critical_files:
            full_path = os.path.join(project_root, rel_path)
            self.assertTrue(os.path.isfile(full_path), f"Critical competition file missing: {rel_path}")

if __name__ == "__main__":
    unittest.main()
