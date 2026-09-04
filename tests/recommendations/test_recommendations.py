"""
InsightPilot AI — Recommendation Engine Unit Tests
Tests deterministic action generation, driver-lever mapping, prioritization, ownership, and schema compliance.
"""

import os
import json
import unittest
from analytics.recommendations import RecommendationEngine
from analytics.config import BASE_DIR

class TestRecommendations(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.engine = RecommendationEngine()
        schema_path = os.path.join(BASE_DIR, "data", "schemas", "recommendation_contract.json")
        with open(schema_path, "r", encoding="utf-8") as sf:
            cls.schema = json.load(sf)

    # 1. Recommendation generation succeeds
    def test_recommendation_generation_succeeds(self):
        recs = self.engine.generate_recommendations("north_america_east_revenue", "NA-East")
        self.assertGreater(len(recs), 0)
        self.assertEqual(len(recs), 4)

    # 2. Driver -> lever mapping is deterministic
    def test_driver_to_lever_mapping(self):
        recs = self.engine.generate_recommendations("north_america_east_revenue", "NA-East")
        d_map = {r["driver_id"]: r["controllable_lever"] for r in recs}
        self.assertIn("Inventory Availability", d_map["atlanta_dc_stockout"])
        self.assertIn("Channel Partner", d_map["distributor_orders"])
        self.assertIn("Production Schedule", d_map["sku_8821_sales_volume"])
        self.assertIn("Trade Allowance", d_map["competitor_horizon_pricing"])

    # 3. Controllability classification is deterministic
    def test_controllability_classification(self):
        recs = self.engine.generate_recommendations("north_america_east_revenue", "NA-East")
        c_map = {r["driver_id"]: r["controllability"] for r in recs}
        self.assertEqual(c_map["atlanta_dc_stockout"], "HIGH")
        self.assertEqual(c_map["distributor_orders"], "HIGH")
        self.assertEqual(c_map["sku_8821_sales_volume"], "MEDIUM")
        self.assertEqual(c_map["competitor_horizon_pricing"], "LOW")

    # 4. Recommendation ranking is deterministic
    def test_recommendation_ranking_order(self):
        recs = self.engine.generate_recommendations("north_america_east_revenue", "NA-East")
        ranks = [r["priority_rank"] for r in recs]
        self.assertEqual(ranks, [1, 2, 3, 4])
        self.assertEqual(recs[0]["priority"], "CRITICAL")
        self.assertEqual(recs[0]["driver_id"], "atlanta_dc_stockout")

    # 5. Owner assignment is deterministic
    def test_owner_assignment(self):
        recs = self.engine.generate_recommendations("north_america_east_revenue", "NA-East")
        o_map = {r["driver_id"]: r["owner"] for r in recs}
        self.assertEqual(o_map["atlanta_dc_stockout"], "Supply Chain / Operations")
        self.assertEqual(o_map["distributor_orders"], "Regional Sales / Commercial Operations")
        self.assertEqual(o_map["sku_8821_sales_volume"], "Manufacturing & Product Operations")
        self.assertEqual(o_map["competitor_horizon_pricing"], "Commercial Strategy & Pricing")

    # 6. Recommendation confidence is deterministic
    def test_recommendation_confidence(self):
        recs = self.engine.generate_recommendations("north_america_east_revenue", "NA-East")
        for r in recs:
            self.assertIn("score", r["confidence"])
            self.assertIn("label", r["confidence"])
            self.assertGreaterEqual(r["confidence"]["score"], 80)

    # 7. Supporting evidence IDs exist
    def test_supporting_evidence_ids_exist(self):
        recs = self.engine.generate_recommendations("north_america_east_revenue", "NA-East")
        for r in recs:
            self.assertGreater(len(r["supporting_evidence_ids"]), 0)
            for eid in r["supporting_evidence_ids"]:
                self.assertTrue(eid.startswith("EVID_"))

    # 8. Primary recommendation exists (Emergency Inventory Transfer)
    def test_primary_recommendation(self):
        recs = self.engine.generate_recommendations("north_america_east_revenue", "NA-East")
        primary = recs[0]
        self.assertEqual(primary["recommendation_id"], "REC-2026-NAE-001")
        self.assertIn("Emergency Inventory Transfer", primary["action"])
        self.assertGreater(primary["expected_impact"]["revenue_recovery_usd"], 400000.0)

    # 9. Secondary recommendation exists (Targeted Distributor Outreach)
    def test_secondary_recommendation(self):
        recs = self.engine.generate_recommendations("north_america_east_revenue", "NA-East")
        secondary = recs[1]
        self.assertEqual(secondary["recommendation_id"], "REC-2026-NAE-002")
        self.assertIn("Distributor Recovery", secondary["action"])

    # 10. Single recommendation detail retrieval
    def test_single_recommendation_lookup(self):
        rec = self.engine.get_recommendation_by_id("REC-2026-NAE-001", "north_america_east_revenue", "NA-East")
        self.assertIsNotNone(rec)
        self.assertEqual(rec["driver_id"], "atlanta_dc_stockout")

        non_rec = self.engine.get_recommendation_by_id("REC-NON-EXISTENT", "north_america_east_revenue", "NA-East")
        self.assertIsNone(non_rec)

    # 11. Schema conformance validation
    def test_recommendations_conform_to_schema(self):
        recs = self.engine.generate_recommendations("north_america_east_revenue", "NA-East")
        required_keys = set(self.schema.get("required", []))
        for r in recs:
            missing = required_keys - set(r.keys())
            self.assertFalse(missing, f"Recommendation missing required fields: {missing}")

    # 12. Overlapping recovery is not double counted
    def test_overlap_group_identification(self):
        recs = self.engine.generate_recommendations("north_america_east_revenue", "NA-East")
        groups = [r["overlap_group"] for r in recs]
        self.assertEqual(groups.count("FULFILLMENT_RECOVERY"), 2)
        self.assertEqual(groups.count("CHANNEL_SALES"), 1)
        self.assertEqual(groups.count("COMMERCIAL_PRICING"), 1)

    # 13. Repeated calls are 100% deterministic
    def test_recommendation_determinism(self):
        recs1 = self.engine.generate_recommendations("north_america_east_revenue", "NA-East")
        recs2 = self.engine.generate_recommendations("north_america_east_revenue", "NA-East")
        self.assertEqual(recs1, recs2)

if __name__ == "__main__":
    unittest.main()
