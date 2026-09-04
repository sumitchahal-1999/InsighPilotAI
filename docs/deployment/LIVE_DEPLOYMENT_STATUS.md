# InsightPilot AI — Live Production Deployment Status Registry

**Project:** InsightPilot AI  
**Competition:** Accenture Innovation Challenge 2026 (Track 3: BusinessIntelligence.ai)  
**Document:** Workstream G — Authoritative Master Deployment Status Record  
**Status:** `🟡 DEPLOYMENT READY — EXTERNAL PLATFORM ACTION REQUIRED`

---

## Master Deployment Registry

```text
================================================================================
                 INSIGHTPILOT AI — PHASE 8.2 DEPLOYMENT STATUS
================================================================================

Repository:
  STATUS: VERIFIED (GitHub: ayus1234/InsighPilotAI | Branch: main)

Backend Configuration:
  STATUS: VERIFIED (FastAPI 0.115+ / Uvicorn / render.yaml / Dockerfile / Procfile)

Backend Live URL:
  STATUS: TBD — EXTERNAL ACTION REQUIRED (e.g., https://insightpilot-api.onrender.com)

Frontend Configuration:
  STATUS: VERIFIED (Next.js 14 App Router / 10 Static Pages / NEXT_PUBLIC_API_URL)

Frontend Live URL:
  STATUS: TBD — EXTERNAL ACTION REQUIRED (e.g., https://insightpilot-ai.vercel.app)

CORS Policy Configuration:
  STATUS: VERIFIED (Environment-driven whitelist via CORS_ORIGINS)

Health Liveness Probe (/health & /api/v1/health):
  STATUS: VERIFIED (Local HTTP 200 OK) / PENDING LIVE URL PROBE

Readiness Probe (/api/v1/demo/readiness):
  STATUS: VERIFIED (12/12 Subsystems Healthy) / PENDING LIVE URL PROBE

Full Production Smoke Test:
  STATUS: LOCAL VERIFIED (218/218 Tests Passing) / LIVE PENDING HOSTING

================================================================================
OVERALL DEPLOYMENT VERDICT:
  🟡 DEPLOYMENT READY — EXTERNAL PLATFORM ACTION REQUIRED
================================================================================
```

---

## 1. What is Verified & Ready Inside the Repository

1. **Deterministic Core:** 100% of mathematical variance, driver attribution, and confidence scoring verified.
2. **Backend Gateway:** FastAPI application configured with dual health probes, Pydantic v2 schemas, and safe CORS handling.
3. **Frontend Edge:** Next.js 14 application compiles 10/10 static pages with zero errors.
4. **Zero Secret Leakage:** Tracked templates use placeholders only; zero credentials committed.
5. **Infrastructure as Code:** `render.yaml`, `Dockerfile`, and `Procfile` committed and ready for one-click deployment.

---

## 2. External Human Actions Required for Live Public URL

1. **Step 1:** Log into [Render](https://render.com/) or [Railway](https://railway.app/) and create a Web Service pointing to `ayus1234/InsighPilotAI`.
2. **Step 2:** Log into [Vercel](https://vercel.com/) and create a Project pointing to `frontend/next-app` in `ayus1234/InsighPilotAI`.
3. **Step 3:** Set `NEXT_PUBLIC_API_URL` in Vercel to your deployed Render URL.
4. **Step 4:** Set `CORS_ORIGINS` in Render to your deployed Vercel domain.
5. **Step 5:** Run live smoke test commands from `docs/deployment/LIVE_CORS_AND_API_VALIDATION.md`.
