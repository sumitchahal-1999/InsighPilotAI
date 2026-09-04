# InsightPilot AI — Production URL & Deployment Registry

**Project:** InsightPilot AI  
**Competition:** Accenture Innovation Challenge 2026 (Track 3: BusinessIntelligence.ai)  
**Document:** Authoritative Endpoint Registry, Hosting Targets & Verification Status  
**Status:** `REGISTRY ACTIVE — REPOSITORY VERIFIED, LIVE CLOUD PENDING`

---

## 1. Production Endpoint & Resource Registry

```text
================================================================================
                    PRODUCTION URL & ENDPOINT REGISTRY
================================================================================

1. Git Source Repository
   STATUS: VERIFIED
   URL:    https://github.com/ayus1234/InsighPilotAI.git

2. Backend API Service (Render Web Service)
   STATUS: PENDING EXTERNAL PLATFORM DEPLOYMENT
   URL:    TBD — RENDER DEPLOYMENT REQUIRED

3. Backend Liveness Health Probe
   STATUS: PENDING EXTERNAL PLATFORM DEPLOYMENT
   URL:    TBD — RENDER DEPLOYMENT REQUIRED (Target: https://[RENDER_URL]/health)

4. Backend 12-Subsystem Readiness Probe
   STATUS: PENDING EXTERNAL PLATFORM DEPLOYMENT
   URL:    TBD — RENDER DEPLOYMENT REQUIRED (Target: https://[RENDER_URL]/api/v1/demo/readiness)

5. Frontend Web Application (Vercel Edge Network)
   STATUS: PENDING EXTERNAL PLATFORM DEPLOYMENT
   URL:    TBD — VERCEL DEPLOYMENT REQUIRED

================================================================================
```

---

## 2. Strict Endpoint Status Table

| Environment | Service | URL | Status | Verification |
| :--- | :--- | :--- | :---: | :---: |
| **Git SCM** | Source Code Repository | `https://github.com/ayus1234/InsighPilotAI.git` | `LOCAL VERIFIED` | `PASS (main @ e7981a3)` |
| **Local Backend** | FastAPI ASGI Server | `http://127.0.0.1:8000` | `LOCAL VERIFIED` | `PASS (Liveness <1ms)` |
| **Local Swagger** | OpenAPI 3.0 Interactive | `http://127.0.0.1:8000/docs` | `LOCAL VERIFIED` | `PASS (Interactive UI)` |
| **Local Frontend** | Next.js 14 Web App | `http://localhost:3000` | `LOCAL VERIFIED` | `PASS (10 Static Routes)` |
| **Local Demo Route**| Grounded Investigation | `http://127.0.0.1:8000/api/v1/demo/investigation/*` | `LOCAL VERIFIED` | `PASS (~35ms Response)` |
| **Cloud Backend** | Render Web Service | `TBD — RENDER DEPLOYMENT REQUIRED` | `PENDING EXTERNAL DEPLOYMENT` | `PENDING OWNER ACTION` |
| **Cloud Health** | Liveness Probe | `TBD — Target: https://[RENDER_URL]/health` | `PENDING EXTERNAL DEPLOYMENT` | `PENDING OWNER ACTION` |
| **Cloud Readiness**| 12-Subsystem Readiness | `TBD — Target: https://[RENDER_URL]/api/v1/demo/readiness`| `PENDING EXTERNAL DEPLOYMENT` | `PENDING OWNER ACTION` |
| **Cloud Frontend** | Vercel Edge Network | `TBD — VERCEL DEPLOYMENT REQUIRED` | `PENDING EXTERNAL DEPLOYMENT` | `PENDING OWNER ACTION` |

---

## 3. Production URL Configuration Guidelines

When live provisioning is executed by the repository owner:
1. **Render Backend Hostname:** Paste the assigned URL (e.g. `https://insightpilot-api.onrender.com`) into Vercel's `NEXT_PUBLIC_API_URL`.
2. **Vercel Frontend Hostname:** Paste the assigned URL (e.g. `https://insightpilot-ai.vercel.app`) into Render's `CORS_ORIGINS`.
3. **No Trailing Slashes:** Never append trailing `/` to environment variable hostnames.
