"""
InsightPilot AI — Investigation Result Integration Tests
Tests full orchestration of the analytics engine and validates output compliance
against data/schemas/investigation_result.json.
"""

import os
import json
import unittest
from analytics.investigation_engine import InvestigationEngine
from analytics.config import BASE_DIR

class TestInvestigationResult(unittest.TestCase):
    
    def setUp(self):
        self.engine = InvestigationEngine()

    def test_investigation_result_structure(self):
        result = self.engine.run_investigation(
            kpi_id="north_america_east_revenue",
            region="NA-East",
            prev_period_id="2026-Q2",
            curr_period_id="2026-Q3",
            persona_id="CFO"
        )
        
        # Check Top-Level Keys
        self.assertIn("investigation_id", result)
        self.assertIn("timestamp", result)
        self.assertIn("persona_id", result)
        self.assertIn("kpi", result)
        self.assertIn("drivers", result)
        self.assertIn("evidence_summary", result)
        self.assertIn("overall", result)
        self.assertIn("lineage_graph", result)
        
        # Check KPI block
        kpi = result["kpi"]
        self.assertEqual(kpi["id"], "north_america_east_revenue")
        self.assertAlmostEqual(kpi["percent_change"], -7.97, places=1)
        self.assertEqual(kpi["materiality_status"], "CRITICAL_NEGATIVE_VARIANCE")
        
        # Check Drivers block
        drivers = result["drivers"]
        self.assertEqual(len(drivers), 4)
        for d in drivers:
            self.assertIn("driver_id", d)
            self.assertIn("driver_name", d)
            self.assertIn("contribution_pct", d)
            self.assertIn("impact_usd", d)
            self.assertIn("confidence_score", d)
            self.assertIn("rank", d)
            self.assertIn("evidence_ids", d)
            self.assertGreater(len(d["evidence_ids"]), 0)
            
        # Check Schema Conformance against data/schemas/investigation_result.json
        schema_path = os.path.join(BASE_DIR, "data", "schemas", "investigation_result.json")
        self.assertTrue(os.path.exists(schema_path))
        with open(schema_path, "r", encoding="utf-8") as sf:
            schema_json = json.load(sf)
            
        required_keys = set(schema_json.get("required", []))
        self.assertTrue(required_keys.issubset(set(result.keys())))

if __name__ == "__main__":
    unittest.main()
