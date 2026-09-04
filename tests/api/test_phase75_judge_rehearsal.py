"""
Phase 7.5: Judge Simulation & Pitch Rehearsal Test Suite
Project: InsightPilot AI
Competition: Accenture Innovation Challenge 2026 (Track 3: BusinessIntelligence.ai)

Validates:
1. Existence of all 9 Phase 7.5 rehearsal documentation deliverables
2. Preservation of canonical numerical invariants across rehearsal documents
3. Presence of mandatory AI Safety guarantee boundaries in AI_SAFETY_QA.md
4. Proper classification categories in CLAIM_VALIDATION_MATRIX.md
5. Complete index coverage in docs/rehearsal/README.md
"""

import unittest
import os

class TestPhase75JudgeRehearsal(unittest.TestCase):

    def setUp(self):
        self.project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
        self.rehearsal_dir = os.path.join(self.project_root, "docs", "rehearsal")

    # --------------------------------------------------------------------------
    # Test 1: Required Phase 7.5 Deliverables Existence
    # --------------------------------------------------------------------------
    def test_phase75_deliverables_exist(self):
        """Verify that all 9 required Phase 7.5 rehearsal documents exist on disk."""
        required_files = [
            "JUDGE_SIMULATION_PLAYBOOK.md",
            "JUDGE_QA_CHEAT_SHEET.md",
            "DIFFICULT_QUESTIONS_STRESS_TEST.md",
            "TECHNICAL_DEFENSE_PLAYBOOK.md",
            "BUSINESS_DEFENSE_PLAYBOOK.md",
            "AI_SAFETY_QA.md",
            "LIVE_PITCH_REHEARSAL.md",
            "CLAIM_VALIDATION_MATRIX.md",
            "JUDGE_REHEARSAL_SCORECARD.md",
            "README.md",
        ]

        for fname in required_files:
            fpath = os.path.join(self.rehearsal_dir, fname)
            self.assertTrue(os.path.isfile(fpath), f"Missing rehearsal deliverable: {fname}")

    # --------------------------------------------------------------------------
    # Test 2: Canonical Metric Parity in Rehearsal Playbook
    # --------------------------------------------------------------------------
    def test_canonical_metrics_in_playbook(self):
        """Verify that JUDGE_SIMULATION_PLAYBOOK.md preserves canonical metrics."""
        fpath = os.path.join(self.rehearsal_dir, "JUDGE_SIMULATION_PLAYBOOK.md")
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn("$15,430,000.06", content)
        self.assertIn("$14,200,000.05", content)
        self.assertIn("-$1,230,000.01", content)
        self.assertIn("-7.97%", content)
        self.assertIn("Atlanta DC Stockout", content)
        self.assertIn("43.2%", content)
        self.assertIn("-$550,000.00", content)
        self.assertIn("89%", content)
        self.assertIn("65%", content)
        self.assertIn("+$484,000.00", content)
        self.assertIn("+$341,422.91", content)
        self.assertIn("+$757,600.00", content)

    # --------------------------------------------------------------------------
    # Test 3: Mandatory AI Safety Boundaries Section
    # --------------------------------------------------------------------------
    def test_mandatory_ai_safety_boundaries(self):
        """Verify that AI_SAFETY_QA.md contains the mandatory boundaries section."""
        fpath = os.path.join(self.rehearsal_dir, "AI_SAFETY_QA.md")
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn("What InsightPilot AI Does NOT Guarantee", content)
        self.assertIn("philosophical causality", content)
        self.assertIn("upstream data correctness", content)
        self.assertIn("65% MANDATORY ABSTENTION", content)
        self.assertIn("SHA-256", content)

    # --------------------------------------------------------------------------
    # Test 4: Claim Validation Matrix Classifications
    # --------------------------------------------------------------------------
    def test_claim_validation_matrix_classifications(self):
        """Verify that CLAIM_VALIDATION_MATRIX.md contains required claim categories."""
        fpath = os.path.join(self.rehearsal_dir, "CLAIM_VALIDATION_MATRIX.md")
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()

        required_classifications = [
            "VERIFIED IN CODE",
            "VERIFIED IN TESTS",
            "VERIFIED IN DATA",
            "DOCUMENTED BUSINESS ASSUMPTION",
            "MODELED SCENARIO",
            "FUTURE ROADMAP",
        ]

        for classification in required_classifications:
            self.assertIn(classification, content, f"Missing claim classification: {classification}")

    # --------------------------------------------------------------------------
    # Test 5: Rehearsal README Index Integrity
    # --------------------------------------------------------------------------
    def test_rehearsal_readme_links(self):
        """Verify that docs/rehearsal/README.md links to all 9 rehearsal documents."""
        fpath = os.path.join(self.rehearsal_dir, "README.md")
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()

        expected_links = [
            "JUDGE_SIMULATION_PLAYBOOK.md",
            "JUDGE_QA_CHEAT_SHEET.md",
            "DIFFICULT_QUESTIONS_STRESS_TEST.md",
            "TECHNICAL_DEFENSE_PLAYBOOK.md",
            "BUSINESS_DEFENSE_PLAYBOOK.md",
            "AI_SAFETY_QA.md",
            "LIVE_PITCH_REHEARSAL.md",
            "CLAIM_VALIDATION_MATRIX.md",
            "JUDGE_REHEARSAL_SCORECARD.md",
        ]

        for link in expected_links:
            self.assertIn(link, content, f"Rehearsal README missing link to: {link}")

if __name__ == "__main__":
    unittest.main()
