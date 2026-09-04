# InsightPilot AI — Production Deployment Runbook

**Project:** InsightPilot AI  
**Competition:** Accenture Innovation Challenge 2026 (Track 3: BusinessIntelligence.ai)  
**Document:** End-to-End Operational Deployment Runbook & Verification Manual  
**Status:** `PRODUCTION DEPLOYMENT MANUAL`

---

## Section 1: Prerequisites

Before initiating deployment, ensure you have:
1. Access to GitHub repository: `https://github.com/ayus1234/InsighPilotAI.git`.
2. A free or enterprise account on a Frontend Host (e.g., [Vercel](https://vercel.com/)).
3. A free or enterprise account on a Backend PaaS (e.g., [Render](https://render.com/) or [Railway](https://railway.app/)).
4. Optional API keys for live AI synthesis: Google Gemini API Key and/or Groq API Key.

---

## Section 2: Pre-Deployment Local Verification

Execute the local verification pipeline from the repository root:
```bash
# 1. Validate dataset integrity (6/6 checks)
python tests/validate_dataset.py

# 2. Run full backend regression suite (211/211 tests)
python -m unittest discover -s tests -t . -p "test_*.py" -v

# 3. Test frontend production build (10/10 static pages)
cd frontend/next-app
npm run build
cd ../..
```

---

## Section 3: Backend Deployment Procedure (e.g. Render)

1. Navigate to [Render Dashboard](https://dashboard.render.com/) $\to$ **New Web Service**.
2. Connect repository: `https://github.com/ayus1234/InsighPilotAI.git`.
3. Configure settings:
   - **Name:** `insightpilot-api`
   - **Environment:** `Python`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python -m uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT --workers 2`
4. Add Environment Variables:
   - `APP_ENV` = `production`
   - `CORS_ORIGINS` = `https://insightpilot-ai.vercel.app` (or temporary `*` during initial bootstrap)
   - `GROQ_API_KEY_1` = `[YOUR_GROQ_KEY]` (Optional)
   - `GEMINI_API_KEY_1` = `[YOUR_GEMINI_KEY]` (Optional)
5. Set Health Check Path: `/health`.
6. Click **Create Web Service**. Record your deployed backend URL: `https://insightpilot-api.onrender.com`.

---

## Section 4: Frontend Deployment Procedure (e.g. Vercel)

1. Navigate to [Vercel Dashboard](https://vercel.com/) $\to$ **Add New Project**.
2. Import repository `https://github.com/ayus1234/InsighPilotAI.git`.
3. Configure settings:
   - **Framework Preset:** `Next.js`
   - **Root Directory:** `frontend/next-app`
   - **Build Command:** `npm run build`
4. Configure Environment Variables:
   - `NEXT_PUBLIC_API_URL` = `https://insightpilot-api.onrender.com` (Your backend URL from Section 3)
5. Click **Deploy**. Record your deployed frontend URL: `https://insightpilot-ai.vercel.app`.

---

## Section 5: CORS Synchronization

1. Return to the Render Backend Settings $\to$ Environment Variables.
2. Update `CORS_ORIGINS` to match your exact Vercel frontend URL:
   ```bash
   CORS_ORIGINS=https://insightpilot-ai.vercel.app
   ```
3. Save changes; Render will automatically restart the web service with updated CORS policies.

---

## Section 6: Production Smoke Testing

Run the following smoke tests against the live deployment:

```bash
# 1. Test Backend Liveness
curl -i https://insightpilot-api.onrender.com/health
# Expected: HTTP 200 {"status": "ok", "service": "insightpilot-api", "version": "2.0.0"}

# 2. Test Backend 12-Subsystem Readiness
curl -i https://insightpilot-api.onrender.com/api/v1/demo/readiness
# Expected: HTTP 200 {"submission_ready": true, "total_subsystems": 12, ...}

# 3. Test KPI Endpoint
curl -i "https://insightpilot-api.onrender.com/api/v1/kpis?region=NA-East"
# Expected: HTTP 200 with NA-East -$1,230,000.01 (-7.97%)

# 4. Test Frontend Accessibility
curl -i https://insightpilot-ai.vercel.app/
# Expected: HTTP 200
```

---

## Section 7: Rollback Strategy

- **Frontend Rollback (Vercel):** Go to Vercel $\to$ Deployments $\to$ select the previous working deployment $\to$ click **Promote to Production** (Instant &lt;1s rollback).
- **Backend Rollback (Render):** Go to Render $\to$ Deploys $\to$ select previous deployment commit $\to$ click **Rollback to this deploy**.

---

## Section 8: Post-Deployment Verification

1. Open `https://insightpilot-ai.vercel.app/` in an incognito browser window.
2. Verify all 7 screens load with live data:
   - `/` (Command Center)
   - `/root-cause` (4-factor decomposition)
   - `/investigation` (11-node LangGraph trace)
   - `/decision-graph` (6-column causal topology)
   - `/evidence` (SHA-256 evidence drawer)
   - `/recommendations` (Action cards and What-If slider)
   - `/briefing` (Executive summary)
