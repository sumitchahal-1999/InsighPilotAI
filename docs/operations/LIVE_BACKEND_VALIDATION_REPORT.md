# InsightPilot AI — Live Backend Validation Report

**Project:** InsightPilot AI  
**Competition:** Accenture Innovation Challenge 2026 (Track 3: BusinessIntelligence.ai)  
**Document:** Backend Cloud Health, Readiness, and Endpoint Validation Report  
**Status:** `LOCAL VERIFICATION PASSED — LIVE CLOUD PENDING OWNER DEPLOYMENT`

---

## 1. Backend Validation Scope & Verification Matrix

| Endpoint | Target Method | Local Verification (Executed) | Live Cloud Verification (Target) |
| :--- | :---: | :---: | :---: |
| `/health` | `GET` | `HTTP 200 {"status":"ok","version":"2.0.0"}` (&lt;1ms) | `PENDING CLOUD DEPLOYMENT` |
| `/api/v1/demo/readiness` | `GET` | `HTTP 200 {"submission_ready":true}` (12/12 OK) | `PENDING CLOUD DEPLOYMENT` |
| `/api/v1/kpis` | `GET` | `HTTP 200` (Returns 3 KPI objects) | `PENDING CLOUD DEPLOYMENT` |
| `/api/v1/investigations/{kpi_id}/drivers` | `GET` | `HTTP 200` (4 ranked drivers, 100% variance) | `PENDING CLOUD DEPLOYMENT` |
| `/api/v1/evidence` | `GET` | `HTTP 200` (9 empirical nodes with SHA-256) | `PENDING CLOUD DEPLOYMENT` |
| `/api/v1/recommendations/{kpi_id}` | `GET` | `HTTP 200` (2 prioritized recovery actions) | `PENDING CLOUD DEPLOYMENT` |
| `/api/v1/simulations/run` | `POST` | `HTTP 200` (90% availability $\to$ +$341.4K) | `PENDING CLOUD DEPLOYMENT` |
| `/api/v1/demo/investigation/{kpi_id}` | `GET` | `HTTP 200` (Full deterministic investigation) | `PENDING CLOUD DEPLOYMENT` |

---

## 2. Information Leakage & Security Boundary Audit

- **No Public Credentials:** Zero API keys, database connection strings, or internal tokens exposed in response bodies.
- **No Path Disclosure:** Server filesystem paths (`c:\Users\...` or `/home/...`) masked in all responses and error payloads.
- **No Public Tracebacks:** Uncaught exceptions intercepted by global error handlers, returning structured JSON error objects with unique `X-Request-ID`.
