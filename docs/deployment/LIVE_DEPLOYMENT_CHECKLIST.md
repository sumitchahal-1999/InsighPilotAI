# InsightPilot AI — Live Production Deployment Checklist

**Project:** InsightPilot AI  
**Competition:** Accenture Innovation Challenge 2026 (Track 3: BusinessIntelligence.ai)  
**Document:** Operational Go-Live & Verification Checklist  
**Status:** `READY FOR DEPLOYMENT EXECUTION`

---

## 1. Pre-Deployment Stage (Local Verification)

- [x] Full regression test suite passing: **211 / 211 tests passing**.
- [x] Dataset validation passing: 6 / 6 automated data checks healthy.
- [x] Frontend Next.js production build passing: 10 / 10 static pages compiled.
- [x] Environment variable templates documented (`.env.example` and `frontend/next-app/.env.example`).
- [x] Zero credentials or API keys tracked in Git repository history.
- [x] Dual healthcheck endpoints operational (`/health` and `/api/v1/health`).
- [x] Dynamic readiness probe (`/api/v1/demo/readiness`) passing across all 12 subsystems.
- [x] Canonical invariants locked ($15.43M $\to$ $14.20M, -$1.23M, 43.2% Atlanta, 89% confidence, &lt;65% abstention).

---

## 2. Deployment Execution Stage (Cloud Actions)

- [ ] **[EXTERNAL ACTION REQUIRED]** Create and configure backend web service on Render / Railway / Fly.io / AWS ECS.
- [ ] **[EXTERNAL ACTION REQUIRED]** Configure backend environment variables (`APP_ENV`, `CORS_ORIGINS`, `GROQ_API_KEY_1`, `GEMINI_API_KEY_1`).
- [ ] **[EXTERNAL ACTION REQUIRED]** Deploy backend and verify health endpoint: `GET https://[YOUR_BACKEND_URL]/health`.
- [ ] **[EXTERNAL ACTION REQUIRED]** Create frontend project on Vercel / Netlify / Cloudflare Pages pointing to `frontend/next-app`.
- [ ] **[EXTERNAL ACTION REQUIRED]** Configure frontend environment variable: `NEXT_PUBLIC_API_URL` = `https://[YOUR_BACKEND_URL]`.
- [ ] **[EXTERNAL ACTION REQUIRED]** Deploy frontend and verify public HTTPS URL.
- [ ] **[EXTERNAL ACTION REQUIRED]** Update backend `CORS_ORIGINS` to whitelist the live frontend HTTPS domain.

---

## 3. Post-Deployment Stage (Live Smoke Test)

- [ ] **[EXTERNAL ACTION REQUIRED]** Open live frontend URL in an incognito browser window.
- [ ] **[EXTERNAL ACTION REQUIRED]** Verify Command Center (`/`) displays -$1.23M anomaly card.
- [ ] **[EXTERNAL ACTION REQUIRED]** Verify Root Cause (`/root-cause`) displays 4-factor decomposition and 43.2% Atlanta stockout.
- [ ] **[EXTERNAL ACTION REQUIRED]** Verify Investigation (`/investigation`) displays live 11-node LangGraph trace.
- [ ] **[EXTERNAL ACTION REQUIRED]** Verify Decision Graph (`/decision-graph`) renders dynamic 6-column topology.
- [ ] **[EXTERNAL ACTION REQUIRED]** Verify Evidence Explorer (`/evidence`) shows 9 records with SHA-256 hashes.
- [ ] **[EXTERNAL ACTION REQUIRED]** Verify Recommendations (`/recommendations`) slider simulates 90.0% availability (+$341.4K recovery).
- [ ] **[EXTERNAL ACTION REQUIRED]** Verify Executive Briefing (`/briefing`) renders persona synthesis without console errors.
