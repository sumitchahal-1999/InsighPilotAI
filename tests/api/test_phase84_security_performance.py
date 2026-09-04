"""
Phase 8.4: Production Security, Performance & Operational Hardening Test Suite
Project: InsightPilot AI
Competition: Accenture Innovation Challenge 2026 (Track 3: BusinessIntelligence.ai)

Validates:
1. Existence of all 10 Phase 8.4 security deliverables in docs/security/
2. HTTP Security Headers (X-Content-Type-Options, X-Frame-Options, Referrer-Policy, Cache-Control)
3. Request correlation and latency headers remain active alongside security headers
4. Input validation hardening (rejection of out-of-bounds simulation parameters)
5. Persona validation hardening (rejection of unauthorized personas)
6. Standardized error sanitization (no internal stack traces or server file paths)
7. Canonical invariants preservation in security architecture documentation
8. Complete navigation links in docs/security/README.md
"""

import unittest
import os
from fastapi.testclient import TestClient
from backend.app.main import app

class TestPhase84SecurityPerformance(unittest.TestCase):

    def setUp(self):
        self.project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
        self.security_dir = os.path.join(self.project_root, "docs", "security")
        self.client = TestClient(app)

    # --------------------------------------------------------------------------
    # Test 1: Required Phase 8.4 Deliverables Existence
    # --------------------------------------------------------------------------
    def test_phase84_deliverables_exist(self):
        """Verify that all 10 required Phase 8.4 security documents exist on disk."""
        required_files = [
            "PRODUCTION_SECURITY_ARCHITECTURE.md",
            "HTTP_SECURITY_HEADERS.md",
            "CONTENT_SECURITY_POLICY.md",
            "CORS_AND_API_SECURITY.md",
            "REQUEST_VALIDATION_HARDENING.md",
            "RATE_LIMITING_AND_ABUSE_RESILIENCE.md",
            "PERFORMANCE_HARDENING_BASELINE.md",
            "SECURITY_THREAT_MODEL.md",
            "PRODUCTION_DEPLOYMENT_SECURITY_CHECKLIST.md",
            "PHASE_84_SECURITY_STATUS.md",
            "README.md",
        ]

        for fname in required_files:
            fpath = os.path.join(self.security_dir, fname)
            self.assertTrue(os.path.isfile(fpath), f"Missing Phase 8.4 deliverable: {fname}")

    # --------------------------------------------------------------------------
    # Test 2: HTTP Security Headers Enforcement
    # --------------------------------------------------------------------------
    def test_http_security_headers(self):
        """Verify that API responses contain OWASP-recommended HTTP security headers."""
        res = self.client.get("/api/v1/kpis")
        self.assertEqual(res.status_code, 200)

        # Verify MIME-sniffing defense
        self.assertEqual(res.headers.get("X-Content-Type-Options"), "nosniff")

        # Verify Clickjacking defense
        self.assertEqual(res.headers.get("X-Frame-Options"), "DENY")

        # Verify Referrer policy
        self.assertEqual(res.headers.get("Referrer-Policy"), "strict-origin-when-cross-origin")

        # Verify Permissions policy
        self.assertEqual(res.headers.get("Permissions-Policy"), "geolocation=(), camera=(), microphone=()")

        # Verify dynamic API cache prevention
        self.assertIn("no-store", res.headers.get("Cache-Control", ""))

    # --------------------------------------------------------------------------
    # Test 3: Correlation & Latency Headers Compatibility
    # --------------------------------------------------------------------------
    def test_correlation_and_security_headers_coexistence(self):
        """Verify that X-Request-ID and X-Response-Time-Ms coexist with security headers."""
        res = self.client.get("/health")
        self.assertEqual(res.status_code, 200)
        self.assertIn("X-Request-ID", res.headers)
        self.assertIn("X-Response-Time-Ms", res.headers)
        self.assertEqual(res.headers.get("X-Content-Type-Options"), "nosniff")
        self.assertEqual(res.headers.get("X-Frame-Options"), "DENY")

    # --------------------------------------------------------------------------
    # Test 4: Simulation Input Bounds Validation Hardening
    # --------------------------------------------------------------------------
    def test_simulation_input_bounds_validation(self):
        """Verify that simulation endpoints reject invalid availability percentages."""
        # Test out-of-bounds percentage (> 100%)
        res_high = self.client.post("/api/v1/simulations/run", json={
            "scenario_name": "Invalid Test",
            "region": "NA-East",
            "target_availability_pct": 150.0
        })
        self.assertEqual(res_high.status_code, 400)

        # Test out-of-bounds percentage (< 0%)
        res_low = self.client.post("/api/v1/simulations/run", json={
            "scenario_name": "Invalid Test",
            "region": "NA-East",
            "target_availability_pct": -10.0
        })
        self.assertEqual(res_low.status_code, 400)

    # --------------------------------------------------------------------------
    # Test 5: Persona Input Validation Hardening
    # --------------------------------------------------------------------------
    def test_persona_input_validation(self):
        """Verify that AI explanation endpoints reject unauthorized persona values."""
        res = self.client.post("/api/v1/ai/explain/north_america_east_revenue", json={
            "persona": "UNAUTHORIZED_HACKER_ROLE"
        })
        self.assertEqual(res.status_code, 400)
        data = res.json()
        self.assertIn("error", data)
        self.assertEqual(data["error"].get("code"), "INVALID_PERSONA")

    # --------------------------------------------------------------------------
    # Test 6: Error Sanitization & Zero Secret Exposure
    # --------------------------------------------------------------------------
    def test_error_sanitization_under_attack(self):
        """Verify that malformed requests return sanitized error schemas without path leaks."""
        res = self.client.get("/api/v1/evidence/EVID_MALICIOUS_INJECTION_%27%20OR%201=1")
        self.assertEqual(res.status_code, 404)
        data = res.json()
        self.assertIn("error", data)
        self.assertNotIn("c:\\Users\\", str(data).lower())
        self.assertNotIn("traceback", str(data).lower())
        self.assertIn("X-Request-ID", res.headers)
        self.assertEqual(res.headers.get("X-Content-Type-Options"), "nosniff")

    # --------------------------------------------------------------------------
    # Test 7: Canonical Invariants Preservation
    # --------------------------------------------------------------------------
    def test_canonical_invariants_in_security_docs(self):
        """Verify that PRODUCTION_SECURITY_ARCHITECTURE.md preserves canonical values."""
        fpath = os.path.join(self.security_dir, "PRODUCTION_SECURITY_ARCHITECTURE.md")
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn("Deterministic systems own quantitative truth", content)
        self.assertIn("65% Mandatory Abstention Gate", content)
        self.assertIn("SHA-256 Cryptographic Hash Engine", content)

    # --------------------------------------------------------------------------
    # Test 8: Security README Navigation Integrity
    # --------------------------------------------------------------------------
    def test_security_readme_links(self):
        """Verify that docs/security/README.md links to all 10 documents."""
        fpath = os.path.join(self.security_dir, "README.md")
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()

        expected_links = [
            "PRODUCTION_SECURITY_ARCHITECTURE.md",
            "HTTP_SECURITY_HEADERS.md",
            "CONTENT_SECURITY_POLICY.md",
            "CORS_AND_API_SECURITY.md",
            "REQUEST_VALIDATION_HARDENING.md",
            "RATE_LIMITING_AND_ABUSE_RESILIENCE.md",
            "PERFORMANCE_HARDENING_BASELINE.md",
            "SECURITY_THREAT_MODEL.md",
            "PRODUCTION_DEPLOYMENT_SECURITY_CHECKLIST.md",
            "PHASE_84_SECURITY_STATUS.md",
        ]

        for link in expected_links:
            self.assertIn(link, content, f"Security README missing link to: {link}")

if __name__ == "__main__":
    unittest.main()
