"""
InsightPilot AI — Evidence Contract Conformance Tests
Validates all retrieved evidence items against data/schemas/evidence_contract.json.
"""

import os
import json
import unittest
from evidence.evidence_engine import EvidenceEngine
from analytics.config import BASE_DIR

class TestEvidenceContract(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.engine = EvidenceEngine()
        schema_path = os.path.join(BASE_DIR, "data", "schemas", "evidence_contract.json")
        with open(schema_path, "r", encoding="utf-8") as sf:
            cls.schema = json.load(sf)

    def test_all_evidence_nodes_conform_to_contract(self):
        bundle = self.engine.get_all_evidence_for_investigation("NA-East")
        all_nodes = bundle["all_evidence_nodes"]
        self.assertGreater(len(all_nodes), 0)

        required_keys = set(self.schema.get("required", []))

        for node in all_nodes:
            node_keys = set(node.keys())
            missing = required_keys - node_keys
            self.assertFalse(missing, f"Node {node.get('evidence_id')} missing required fields: {missing}")

            # Check nested objects
            self.assertIn("age_hours", node["freshness"])
            self.assertIn("status", node["freshness"])
            self.assertIn(node["freshness"]["status"], ["LIVE", "RECENT", "STALE"])

            self.assertIn("percentage", node["contribution"])
            self.assertIn("monetary_impact_usd", node["contribution"])

            self.assertIn("score", node["confidence"])
            self.assertIn("label", node["confidence"])
            self.assertIn(node["confidence"]["label"], ["HIGH", "MEDIUM", "LOW"])

            self.assertIn("source_table", node["lineage"])
            self.assertIn("pipeline_job_id", node["lineage"])
            self.assertIn("verification_hash", node["lineage"])
            self.assertTrue(node["lineage"]["verification_hash"].startswith("sha256:"))

if __name__ == "__main__":
    unittest.main()
