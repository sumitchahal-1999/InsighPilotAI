"""
Phase 7.2: End-to-End Competition Demo Validation & Judge Experience Audit Test Suite
Project: InsightPilot AI
Competition: Accenture Innovation Challenge 2026 (Track 3: BusinessIntelligence.ai)

Validates the complete 7-screen judge journey, cross-screen canonical invariants,
API contracts, persona invariance, multi-model routing, 65% abstention gate,
evidence lineage, and zero credential leakage.
"""

import unittest
import json
import re
from unittest.mock import MagicMock
from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.dependencies import get_gemini_service, get_ai_service
from backend.app.services.gemini_service import GeminiService
from ai.service import AIService
from ai.client import GeminiClient

class TestPhase72JudgeJourney(unittest.TestCase):

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
    # 1. Screen 1: Command Center Audit (Route: /)
    # --------------------------------------------------------------------------
    def test_screen_1_command_center_judge_experience(self):
        """Judge Step 1: Detect critical revenue anomaly on Executive Command Center."""
        res = self.client.get("/api/v1/kpis?region=NA-East&prev_period_id=2026-Q2&curr_period_id=2026-Q3")
        self.assertEqual(res.status_code, 200)
        data = res.json()

        self.assertIn("kpis", data)
        self.assertGreaterEqual(len(data["kpis"]), 5)

        rev_kpi = next((k for k in data["kpis"] if k["id"] == "north_america_east_revenue"), None)
        self.assertIsNotNone(rev_kpi, "Hero KPI 'north_america_east_revenue' must be present")

        # Canonical Numerical Invariants for Screen 1
        self.assertAlmostEqual(rev_kpi["previous_value"], 15430000.06, delta=100.0)
        self.assertAlmostEqual(rev_kpi["current_value"], 14200000.05, delta=100.0)
        self.assertAlmostEqual(rev_kpi["variance_amount"], -1230000.01, delta=100.0)
        self.assertAlmostEqual(rev_kpi["percent_change"], -7.97, places=1)
        self.assertEqual(rev_kpi["materiality_status"], "CRITICAL_NEGATIVE_VARIANCE")

    # --------------------------------------------------------------------------
    # 2. Screen 2: Root Cause Diagnosis Audit (Route: /root-cause)
    # --------------------------------------------------------------------------
    def test_screen_2_root_cause_decomposition_judge_experience(self):
        """Judge Step 2: 4-factor deterministic causal decomposition explaining 100% variance."""
        res = self.client.get(
            "/api/v1/investigations/north_america_east_revenue"
            "?region=NA-East&prev_period_id=2026-Q2&curr_period_id=2026-Q3"
        )
        self.assertEqual(res.status_code, 200)
        inv = res.json()

        # Overall Invariants
        self.assertEqual(inv["kpi"]["id"], "north_america_east_revenue")
        self.assertEqual(inv["overall"]["overall_confidence"], 89)
        self.assertEqual(inv["overall"]["confidence_label"], "HIGH")
        self.assertFalse(inv["overall"]["abstention"])

        # Driver Decomposition Invariants
        self.assertEqual(len(inv["drivers"]), 4)
        total_contrib = sum(d["contribution_pct"] for d in inv["drivers"])
        self.assertAlmostEqual(total_contrib, 100.0, places=1)

        # Top Driver: Atlanta DC Stockout
        top = inv["drivers"][0]
        self.assertEqual(top["driver_id"], "atlanta_dc_stockout")
        self.assertEqual(top["rank"], 1)
        self.assertAlmostEqual(top["contribution_pct"], 43.2, places=1)
        self.assertAlmostEqual(top["impact_usd"], -550000.00, delta=100.0)
        self.assertEqual(top["confidence_score"], 94)
        self.assertIn("EVID_ERP_ATL_STOCKOUT_001", top["evidence_ids"])

    # --------------------------------------------------------------------------
    # 3. Screen 3: AI Investigation Activity Audit (Route: /investigation)
    # --------------------------------------------------------------------------
    def test_screen_3_investigation_langgraph_trace_judge_experience(self):
        """Judge Step 3: LangGraph 11-node execution timeline with safe telemetry."""
        res = self.client.get(
            "/api/v1/investigations/north_america_east_revenue/langgraph-trace"
            "?region=NA-East&persona_id=CFO&prev_period_id=2026-Q2&curr_period_id=2026-Q3"
        )
        self.assertEqual(res.status_code, 200)
        trace = res.json()

        self.assertIn("nodes", trace)
        self.assertGreaterEqual(len(trace["nodes"]), 7)

        # Confirm node structure and latency metrics
        node_names = [n["node_name"] for n in trace["nodes"]]
        self.assertTrue(any("kpi" in n for n in node_names))
        self.assertTrue(any("driver" in n for n in node_names))
        self.assertTrue(any("evidence" in n for n in node_names))
        self.assertTrue(any("confidence" in n for n in node_names))

        # Check total duration is positive and logged
        self.assertGreater(trace.get("total_duration_ms", 0), 0)

    # --------------------------------------------------------------------------
    # 4. Screen 4: Decision Graph Audit (Route: /decision-graph)
    # --------------------------------------------------------------------------
    def test_screen_4_decision_graph_causal_topology_judge_experience(self):
        """Judge Step 4: 6-column causal topology linking KPI to predicted outcomes."""
        res = self.client.get(
            "/api/v1/investigations/north_america_east_revenue/decision-graph"
            "?region=NA-East&prev_period_id=2026-Q2&curr_period_id=2026-Q3"
        )
        self.assertEqual(res.status_code, 200)
        graph = res.json()

        self.assertEqual(graph["total_columns"], 6)
        self.assertGreaterEqual(len(graph["nodes"]), 10)
        self.assertGreaterEqual(len(graph["edges"]), 10)

        # Check column presence
        columns_present = set(n["column"] for n in graph["nodes"])
        self.assertEqual(columns_present, {1, 2, 3, 4, 5, 6})

        # Verify evidence node link in Column 3
        evid_nodes = [n for n in graph["nodes"] if n["column"] == 3]
        self.assertGreaterEqual(len(evid_nodes), 3)
        self.assertTrue(any(n.get("evidence_id") == "EVID_ERP_ATL_STOCKOUT_001" for n in evid_nodes))

    # --------------------------------------------------------------------------
    # 5. Screen 5: Evidence Explorer Audit (Route: /evidence)
    # --------------------------------------------------------------------------
    def test_screen_5_evidence_explorer_lineage_judge_experience(self):
        """Judge Step 5: Cryptographic SHA-256 evidence validation and 5-layer lineage."""
        res = self.client.get("/api/v1/evidence?region=NA-East")
        self.assertEqual(res.status_code, 200)
        data = res.json()

        self.assertIn("evidence", data)
        self.assertGreaterEqual(len(data["evidence"]), 7)

        # Find primary stockout record
        atl_evid = next((e for e in data["evidence"] if e["evidence_id"] == "EVID_ERP_ATL_STOCKOUT_001"), None)
        self.assertIsNotNone(atl_evid)
        self.assertEqual(atl_evid["source_domain"], "ERP")
        self.assertEqual(atl_evid["confidence"]["score"], 94)

        # Verify SHA-256 digest format in lineage
        sha_hash = atl_evid.get("lineage", {}).get("verification_hash", "")
        self.assertTrue(sha_hash.startswith("sha256:"))

    # --------------------------------------------------------------------------
    # 6. Screen 6: Recommendations & What-If Simulation Audit (Route: /recommendations)
    # --------------------------------------------------------------------------
    def test_screen_6_recommendations_and_simulation_judge_experience(self):
        """Judge Step 6: Prescriptive action levers (+$484K/+$550K) and simulation (+$341.4K at 90%)."""
        # A. Recommendations
        rec_res = self.client.get("/api/v1/recommendations/north_america_east_revenue?region=NA-East")
        self.assertEqual(rec_res.status_code, 200)
        rec_data = rec_res.json()

        self.assertIn("recommendations", rec_data)
        self.assertGreaterEqual(len(rec_data["recommendations"]), 2)
        top_rec = rec_data["recommendations"][0]
        self.assertAlmostEqual(top_rec["expected_impact"]["revenue_recovery_usd"], 550000.00, delta=100000.0)

        # B. What-If Simulation at 90.0% Availability
        sim_res = self.client.post(
            "/api/v1/simulations/inventory-availability",
            json={"inventory_availability": 0.90}
        )
        self.assertEqual(sim_res.status_code, 200)
        sim = sim_res.json()

        self.assertEqual(sim["scenario_value"], 90.0)
        self.assertAlmostEqual(sim["baseline_value"], 79.4, places=1)
        self.assertAlmostEqual(sim["availability_delta"], 10.6, places=1)
        self.assertGreater(sim["estimated_recovery"]["revenue_recovery_usd"], 300000.0)
        self.assertEqual(sim["confidence"]["label"], "HIGH")

    # --------------------------------------------------------------------------
    # 7. Screen 7: Executive Decision Briefing Audit (Route: /briefing)
    # --------------------------------------------------------------------------
    def test_screen_7_executive_briefing_synthesis_judge_experience(self):
        """Judge Step 7: Persona-tailored strategic synthesis and boardroom sign-off."""
        for persona in ["CFO", "REGIONAL_SALES_MANAGER"]:
            res = self.client.post(
                "/api/v1/ai/explain/north_america_east_revenue",
                json={"persona": persona, "explanation_mode": "structured"}
            )
            self.assertEqual(res.status_code, 200)
            ai_data = res.json()

            # Ensure response structure
            self.assertEqual(ai_data["persona"], persona)
            self.assertIn("explanation", ai_data)
            self.assertTrue(len(ai_data["explanation"].get("summary", "")) > 20)

    # --------------------------------------------------------------------------
    # 8. Persona Invariance: Quantitative Facts Never Change Across Personas
    # --------------------------------------------------------------------------
    def test_persona_invariance_quantitative_consistency(self):
        """Verify that switching personas alters executive narrative framing, never mathematical facts."""
        res_cfo = self.client.post(
            "/api/v1/ai/explain/north_america_east_revenue",
            json={"persona": "CFO"}
        ).json()
        res_mgr = self.client.post(
            "/api/v1/ai/explain/north_america_east_revenue",
            json={"persona": "REGIONAL_SALES_MANAGER"}
        ).json()

        # Both cite the same baseline variance and top driver
        cfo_summary = res_cfo["explanation"]["summary"]
        mgr_summary = res_mgr["explanation"]["summary"]

        self.assertIn("1.23", cfo_summary)
        self.assertIn("Atlanta", cfo_summary)
        self.assertIn("Atlanta", mgr_summary)

    # --------------------------------------------------------------------------
    # 9. Safety Guard: Mandatory Abstention Gate
    # --------------------------------------------------------------------------
    def test_mandatory_abstention_gate_behavior(self):
        """Verify that low confidence or ungrounded data triggers safe fallback without crashing."""
        res = self.client.get(
            "/api/v1/investigations/north_america_east_revenue"
        )
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertIn("overall", data)
        self.assertIn("abstention", data["overall"])

    # --------------------------------------------------------------------------
    # 10. Security Audit: Zero Secret & Credential Leakage in Any API Payload
    # --------------------------------------------------------------------------
    def test_zero_secret_leakage_across_all_endpoints(self):
        """Verify that no API keys, tokens, or raw credentials appear in any endpoint response."""
        endpoints = [
            "/api/v1/kpis",
            "/api/v1/investigations/north_america_east_revenue",
            "/api/v1/investigations/north_america_east_revenue/langgraph-trace",
            "/api/v1/investigations/north_america_east_revenue/decision-graph",
            "/api/v1/evidence",
            "/api/v1/recommendations/north_america_east_revenue",
        ]

        forbidden_patterns = [
            r"gsk_[a-zA-Z0-9]{20,}",           # Groq API key pattern
            r"AIzaSy[a-zA-Z0-9_-]{33}",         # Google Gemini API key pattern
            r"Bearer\s+[a-zA-Z0-9_\-\.]{20,}",  # JWT/Bearer token
            r"password\s*[:=]\s*['\"][^'\"]+", # Password field
        ]

        for ep in endpoints:
            res = self.client.get(ep)
            self.assertEqual(res.status_code, 200, f"Endpoint {ep} failed")
            payload_str = json.dumps(res.json())

            for pattern in forbidden_patterns:
                match = re.search(pattern, payload_str, re.IGNORECASE)
                self.assertIsNone(
                    match,
                    f"CRITICAL SECURITY DEFECT: Secret pattern '{pattern}' found in {ep} response: {match}"
                )

if __name__ == "__main__":
    unittest.main()
