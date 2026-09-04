# InsightPilot AI — Observability Security & Privacy Policy

**Project:** InsightPilot AI  
**Competition:** Accenture Innovation Challenge 2026 (Track 3: BusinessIntelligence.ai)  
**Document:** Telemetry Privacy Rules, Secret Masking Standards & Log Security  
**Status:** `SECURITY POLICY VERIFIED`

---

## 1. Core Telemetry Security Standards

1. **Zero Secret Persistence:** API keys (`AIzaSy...`, `gsk_...`), database passwords, and private session tokens must never appear in log records, error messages, or telemetry event objects.
2. **Key Slot Masking:** Internal AI key slots are identified as `slot_1`, `slot_2`, or `pool_a` in telemetry objects; raw cryptographic key strings are strictly redacted.
3. **Environment Variable Dump Prohibition:** Endpoints and debug routines are prohibited from printing or returning `os.environ` dictionaries.
4. **Stack Trace Masking:** Internal Python stack traces and file paths (`c:\Users\...`) are caught by global exception handlers and masked from API responses.
5. **PII Minimization:** Aggregated financial metrics and abstracted evidence codes (`EVID_INV_ATL_001`) are processed; raw customer PII is never logged in plaintext.
6. **Safe Correlation Header Injection:** Response headers `X-Request-ID` and `X-Response-Time-Ms` contain only random UUIDs and numeric millisecond timestamps.

---

## 2. Telemetry Audit Verification

| Vulnerability Vector | Enforcement Mechanism | Automated Verification |
| :--- | :--- | :--- |
| **API Response Secret Leakage** | Pydantic response filtering & `register_error_handlers`. | `tests/api/test_phase83_observability_reliability.py` |
| **Log Format Injection** | Structured JSON key-value formatting in `backend/app/logging.py`. | Middleware unit tests. |
| **Client Bundle Key Extraction** | Next.js build excludes non-`NEXT_PUBLIC_` variables. | `tests/api/test_phase81_deployment_readiness.py` |
