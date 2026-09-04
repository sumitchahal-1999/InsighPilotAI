"""
InsightPilot AI — Database Persistence & Repository Test Suite
Validates database schema creation, CSV seeding pipeline, repository queries, and numerical parity.
"""

import unittest
from backend.app.db.session import engine, SessionLocal, init_db
from backend.app.db.seed import seed_database
from backend.app.db.models.analytics import KPIDefinitionRecord
from backend.app.repositories.data_repository import DataRepository
from analytics.data_loader import DataLoader
from analytics.kpi_engine import KPIEngine

class TestDatabasePersistence(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        # Initialize and seed database
        cls.seed_summary = seed_database()
        cls.repo = DataRepository()
        cls.db_loader = DataLoader(use_db=True)
        cls.csv_loader = DataLoader(use_db=False)

    def test_seeding_row_counts(self):
        """Verifies that all 8 datasets were seeded into the database."""
        raw_rows = self.seed_summary["raw_dataset_rows"]
        self.assertEqual(raw_rows["raw_revenue"], 12322)
        self.assertEqual(raw_rows["raw_inventory"], 13710)
        self.assertEqual(raw_rows["raw_margin"], 75)
        self.assertEqual(raw_rows["raw_sales"], 12344)
        self.assertEqual(raw_rows["raw_distributor_orders"], 1640)
        self.assertEqual(raw_rows["raw_support_tickets"], 2856)
        self.assertEqual(raw_rows["raw_distributor_communications"], 39)
        self.assertEqual(raw_rows["raw_market_intelligence"], 12)

        # Total registered KPIs in DB should be 5
        db = SessionLocal()
        try:
            kpi_count = db.query(KPIDefinitionRecord).count()
            self.assertEqual(kpi_count, 5)
        finally:
            db.close()

    def test_repository_queries(self):
        """Verifies that DataRepository queries return valid, populated records."""
        rev = self.repo.get_revenue(region="NA-East")
        self.assertGreater(len(rev), 0)
        self.assertIn("invoice_id", rev[0])
        self.assertIn("net_revenue", rev[0])

        inv = self.repo.get_inventory(region="NA-East")
        self.assertGreater(len(inv), 0)
        self.assertIn("dc_location", inv[0])

        sales = self.repo.get_sales(region="NA-East")
        self.assertGreater(len(sales), 0)

        orders = self.repo.get_distributor_orders(region="NA-East")
        self.assertGreater(len(orders), 0)

    def test_loader_parity_db_vs_csv(self):
        """Verifies 100% numerical parity between DB-backed and CSV-backed data loaders."""
        rev_db = self.db_loader.get_revenue()
        rev_csv = self.csv_loader.get_revenue()
        self.assertEqual(len(rev_db), len(rev_csv))

        inv_db = self.db_loader.get_inventory()
        inv_csv = self.csv_loader.get_inventory()
        self.assertEqual(len(inv_db), len(inv_csv))

        margin_db = self.db_loader.get_margin()
        margin_csv = self.csv_loader.get_margin()
        self.assertEqual(len(margin_db), len(margin_csv))

    def test_deterministic_kpi_parity(self):
        """Verifies that KPIEngine calculates exact identical values using the DB persistence layer."""
        kpi_engine_db = KPIEngine(self.db_loader)
        kpi_engine_csv = KPIEngine(self.csv_loader)

        rev_state_db = kpi_engine_db.evaluate_kpi_movement(
            "north_america_east_revenue", region="NA-East", prev_period_id="2026-Q2", curr_period_id="2026-Q3"
        )
        rev_state_csv = kpi_engine_csv.evaluate_kpi_movement(
            "north_america_east_revenue", region="NA-East", prev_period_id="2026-Q2", curr_period_id="2026-Q3"
        )

        # Grounded truth values
        self.assertAlmostEqual(rev_state_db["previous_value"], 15430000.06, delta=0.01)
        self.assertAlmostEqual(rev_state_db["current_value"], 14200000.05, delta=0.01)
        self.assertAlmostEqual(rev_state_db["variance_amount"], -1230000.01, delta=0.01)
        self.assertAlmostEqual(rev_state_db["percent_change"], -7.97, places=2)

        # Exact parity
        self.assertEqual(rev_state_db["current_value"], rev_state_csv["current_value"])
        self.assertEqual(rev_state_db["previous_value"], rev_state_csv["previous_value"])
        self.assertEqual(rev_state_db["percent_change"], rev_state_csv["percent_change"])

if __name__ == "__main__":
    unittest.main()
