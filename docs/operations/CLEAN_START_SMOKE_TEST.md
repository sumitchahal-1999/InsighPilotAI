# InsightPilot AI — Clean-Start Production Smoke Test Report

**Project:** InsightPilot AI  
**Competition:** Accenture Innovation Challenge 2026 (Track 3: BusinessIntelligence.ai)  
**Document:** Clean-Start Verification, Asset Availability & Runtime Smoke Test Log  
**Status:** `LOCALLY VERIFIED & PASSED`

---

## 1. Clean-Start Verification Checklist & Results

| # | Verification Check | Execution Command | Result Classification | Observed Output / Behavior |
| :-: | :--- | :--- | :---: | :--- |
| **1** | **Dataset Schema Validation** | `python tests/validate_dataset.py` | `EXECUTED AND PASSED` | 6/6 checks passed across 8 CSV datasets (12.3K invoices, 13.7K inventory). |
| **2** | **Backend Dependency Tree** | `python -c "import fastapi, pydantic, starlette, pandas, httpx"` | `EXECUTED AND PASSED` | Zero missing Python dependencies; clean import tree. |
| **3** | **Backend App Factory Clean-Start** | `python -c "from backend.app.main import app; print(app.title)"` | `EXECUTED AND PASSED` | App initialized: `"InsightPilot AI API"`. |
| **4** | **Backend ASGI Startup & Health** | `GET /health` via TestClient | `EXECUTED AND PASSED` | HTTP 200 OK `{"status": "ok", "service": "insightpilot-api"}` (&lt;1ms). |
| **5** | **12-Subsystem Readiness Probe** | `GET /api/v1/demo/readiness` via TestClient | `EXECUTED AND PASSED` | HTTP 200 OK `{"submission_ready": true}` (12/12 subsystems healthy). |
| **6** | **Frontend Production Build** | `cd frontend/next-app && npm run build` | `EXECUTED AND PASSED` | 10/10 static pages compiled with 0 errors (`○ Static` pre-rendered). |
| **7** | **Static Asset Generation** | Check `frontend/next-app/.next/static/` | `EXECUTED AND PASSED` | All JavaScript chunks, CSS stylesheets, and HTML routes generated. |
| **8** | **No Undeclared Local Files** | Clean git checkout test | `EXECUTED AND PASSED` | All runtime datasets reside in `data/raw/` with matching JSON schemas. |
| **9** | **Missing Secrets Safe Handling** | API tests run with empty API keys | `EXECUTED AND PASSED` | Grounded deterministic engine activates transparently with zero crashes. |
| **10**| **Live Cloud Infrastructure** | Ping Render / Vercel cloud URLs | `REQUIRES EXTERNAL ENVIRONMENT` | Platform deployment pending owner configuration. |

---

## 2. Execution Summary

- **Local Clean-Start Posture:** 100% functional and verified without external dependencies.
- **Zero Local Secrets Dependency:** System operates out-of-the-box in deterministic mode.
