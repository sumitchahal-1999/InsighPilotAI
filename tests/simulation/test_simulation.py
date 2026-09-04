"""
InsightPilot AI — What-If Simulation Engine Unit Tests
Tests deterministic scenario simulation, baseline calculation, parameter bounds, and schema compliance.
"""

import os
import json
import unittest
from simulation.simulation_engine import SimulationEngine
from analytics.config import BASE_DIR

class TestSimulation(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.engine = SimulationEngine()
        schema_path = os.path.join(BASE_DIR, "data", "schemas", "simulation_contract.json")
        with open(schema_path, "r", encoding="utf-8") as sf:
            cls.schema = json.load(sf)

    # 1. Baseline simulation succeeds
    def test_baseline_state_calculation(self):
        base = self.engine.get_baseline_state("NA-East")
        self.assertEqual(base["baseline_availability_pct"], 79.4)
        self.assertEqual(base["baseline_availability_ratio"], 0.794)
        self.assertEqual(base["baseline_revenue_usd"], 14200000.05)

    # 2. 90% scenario succeeds
    def test_90_percent_scenario_success(self):
        res = self.engine.simulate_inventory_availability(0.90, "NA-East")
        self.assertEqual(res["input_variable"], "inventory_availability")
        self.assertEqual(res["baseline_value"], 79.4)
        self.assertEqual(res["scenario_value"], 90.0)
        self.assertEqual(res["availability_delta"], 10.6)
        self.assertGreater(res["estimated_recovery"]["revenue_recovery_usd"], 0)
        self.assertEqual(res["estimated_recovery"]["margin_recovery_pct"], 0.72)
        self.assertEqual(res["estimated_recovery"]["recovery_timeframe_days"], 14)

    # 3. Ratio (0.90) and percentage (90.0) produce identical results
    def test_ratio_and_percentage_equivalence(self):
        res_ratio = self.engine.simulate_inventory_availability(0.90, "NA-East")
        res_pct = self.engine.simulate_inventory_availability(90.0, "NA-East")
        self.assertEqual(res_ratio, res_pct)

    # 4. Projected revenue equals baseline + recovery
    def test_projected_revenue_sum(self):
        res = self.engine.simulate_inventory_availability(0.90, "NA-East")
        expected_total = round(res["baseline_revenue_usd"] + res["estimated_recovery"]["revenue_recovery_usd"], 2)
        self.assertEqual(res["projected_value"], expected_total)

    # 5. Determinism test
    def test_simulation_determinism(self):
        run1 = self.engine.simulate_inventory_availability(0.85, "NA-East")
        run2 = self.engine.simulate_inventory_availability(0.85, "NA-East")
        self.assertEqual(run1, run2)

    # 6. Scenario below baseline yields 0 recovery
    def test_scenario_below_baseline(self):
        res = self.engine.simulate_inventory_availability(0.70, "NA-East")
        self.assertEqual(res["estimated_recovery"]["revenue_recovery_usd"], 0.0)
        self.assertEqual(res["estimated_recovery"]["margin_recovery_pct"], 0.0)
        self.assertEqual(res["projected_value"], res["baseline_revenue_usd"])

    # 7. 100% scenario reaches maximum recoverable recovery
    def test_100_percent_scenario(self):
        res = self.engine.simulate_inventory_availability(1.0, "NA-East")
        self.assertEqual(res["scenario_value"], 100.0)
        self.assertGreater(res["estimated_recovery"]["revenue_recovery_usd"], 600000.0)

    # 8. Negative availability input rejected
    def test_negative_input_rejected(self):
        with self.assertRaises(ValueError) as ctx:
            self.engine.simulate_inventory_availability(-0.10, "NA-East")
        self.assertIn("between 0.0 and 1.0", str(ctx.exception))

    # 9. Greater than 100% (or >100.0) input rejected
    def test_out_of_bounds_input_rejected(self):
        with self.assertRaises(ValueError) as ctx:
            self.engine.simulate_inventory_availability(150.0, "NA-East")
        self.assertIn("between 0.0 and 1.0", str(ctx.exception))

    # 10. Non-numeric input rejected
    def test_non_numeric_input_rejected(self):
        with self.assertRaises(ValueError) as ctx:
            self.engine.simulate_inventory_availability("invalid_string", "NA-East")
        self.assertIn("must be numeric", str(ctx.exception))

    # 11. Assumptions returned
    def test_assumptions_present(self):
        res = self.engine.simulate_inventory_availability(0.90, "NA-East")
        self.assertIsInstance(res["assumptions"], list)
        self.assertGreater(len(res["assumptions"]), 2)

    # 12. Schema conformance validation
    def test_simulation_conforms_to_schema(self):
        res = self.engine.simulate_inventory_availability(0.90, "NA-East")
        required_keys = set(self.schema.get("required", []))
        missing = required_keys - set(res.keys())
        self.assertFalse(missing, f"Simulation missing required fields: {missing}")

    # 13. Source data immutability
    def test_source_data_immutability(self):
        base_before = self.engine.get_baseline_state("NA-East")
        self.engine.simulate_inventory_availability(0.95, "NA-East")
        self.engine.simulate_inventory_availability(0.50, "NA-East")
        base_after = self.engine.get_baseline_state("NA-East")
        self.assertEqual(base_before, base_after)

if __name__ == "__main__":
    unittest.main()
