"""
InsightPilot AI — Analytics Determinism Tests
Asserts that running the investigation engine repeatedly on identical data produces
100% identical, deterministic results across all numerical calculations and rankings.
"""

import unittest
from analytics.investigation_engine import InvestigationEngine

class TestDeterminism(unittest.TestCase):
    
    def test_investigation_determinism(self):
        engine1 = InvestigationEngine()
        engine2 = InvestigationEngine()
        
        res1 = engine1.run_investigation("north_america_east_revenue", "NA-East", "2026-Q2", "2026-Q3", "CFO")
        res2 = engine2.run_investigation("north_america_east_revenue", "NA-East", "2026-Q2", "2026-Q3", "CFO")
        
        # Check exact KPI equivalence
        self.assertEqual(res1["kpi"]["current_value"], res2["kpi"]["current_value"])
        self.assertEqual(res1["kpi"]["previous_value"], res2["kpi"]["previous_value"])
        self.assertEqual(res1["kpi"]["variance_amount"], res2["kpi"]["variance_amount"])
        self.assertEqual(res1["kpi"]["percent_change"], res2["kpi"]["percent_change"])
        self.assertEqual(res1["kpi"]["materiality_status"], res2["kpi"]["materiality_status"])
        
        # Check exact Driver rankings and numerical contributions
        self.assertEqual(len(res1["drivers"]), len(res2["drivers"]))
        for d1, d2 in zip(res1["drivers"], res2["drivers"]):
            self.assertEqual(d1["driver_id"], d2["driver_id"])
            self.assertEqual(d1["rank"], d2["rank"])
            self.assertEqual(d1["contribution_pct"], d2["contribution_pct"])
            self.assertEqual(d1["impact_usd"], d2["impact_usd"])
            self.assertEqual(d1["confidence_score"], d2["confidence_score"])
            self.assertEqual(d1["evidence_ids"], d2["evidence_ids"])
            
        # Check exact Confidence equivalence
        self.assertEqual(res1["overall"]["overall_confidence"], res2["overall"]["overall_confidence"])
        self.assertEqual(res1["overall"]["confidence_label"], res2["overall"]["confidence_label"])
        self.assertEqual(res1["overall"]["abstention"], res2["overall"]["abstention"])

if __name__ == "__main__":
    unittest.main()
