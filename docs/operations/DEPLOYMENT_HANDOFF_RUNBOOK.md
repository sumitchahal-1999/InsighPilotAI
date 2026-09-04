# InsightPilot AI — Production Deployment Handoff Runbook

**Project:** InsightPilot AI  
**Competition:** Accenture Innovation Challenge 2026 (Track 3: BusinessIntelligence.ai)  
**Document:** Cloud Deployment Instructions, Operational Boundaries & Rollback Procedures  
**Status:** `DEPLOYMENT HANDOFF READY — EXTERNAL ACTIVATION REQUIRED`

---

## 1. Application vs. Cloud Platform Responsibility Matrix

| Area / Operational Domain | Application Responsibility (Repository Verified) | Cloud Platform Responsibility (DevOps / Owner) |
| :--- | :--- | :--- |
| **Runtime Process** | `uvicorn backend.app.main:app` ASGI factory. | Provisioning Web Service CPU/RAM (Render / AWS). |
| **Static Web Hosting** | Next.js 14 static HTML/JS export compilation. | Global Edge CDN distribution (Vercel / Cloudflare). |
| **Secrets & Keys** | Safe runtime reading via Pydantic `BaseSettings`. | Injecting real API keys in cloud secrets vault. |
| **TLS / SSL** | Supporting HTTPS reverse proxy headers (`X-Forwarded-*`).| Provisioning Let's Encrypt TLS 1.3 certificates. |
| **CORS Policy** | Whitelisting allowed origins in `backend/app/config.py`. | Configuring `CORS_ORIGINS` with exact frontend URL. |
| **Telemetry & Logs** | Emitting structured JSON logs with `X-Request-ID`. | Centralizing logs in Datadog, CloudWatch, or Papertrail. |
| **Edge DDoS Defense** | Request validation & bounded payloads. | Configuring Cloudflare / AWS WAF edge rate limits. |

---

## 2. Step-by-Step Production Deployment Procedure

### Step 1: Deploy Backend to Render (or AWS / Railway)
1. Connect GitHub repository `ayus1234/InsighPilotAI`.
2. Select **Python 3.11** environment.
3. Build Command: `pip install -r requirements.txt`
4. Start Command: `uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT`
5. Set Environment Variables:
   - `APP_ENV=production`
   - `CORS_ORIGINS=https://[YOUR_VERCEL_APP].vercel.app`
   - `GROQ_API_KEY_1=[YOUR_ACTUAL_KEY]` (Optional)
   - `GEMINI_API_KEY_1=[YOUR_ACTUAL_KEY]` (Optional)
6. Verify: `GET https://[YOUR_BACKEND_URL]/health` returns `200 OK`.

### Step 2: Deploy Frontend to Vercel
1. Import repository on Vercel.
2. Root Directory: `frontend/next-app`.
3. Framework Preset: **Next.js**.
4. Set Environment Variable:
   - `NEXT_PUBLIC_API_URL=https://[YOUR_RENDER_BACKEND_URL]`
5. Deploy and verify 7 core screens load smoothly.

---

## 3. Rollback Playbook

If a critical issue occurs post-deployment:
1. **Render Instant Rollback:** In Render Dashboard $\to$ Deployments $\to$ Select previous successful build $\to$ Click **"Rollback to this deploy"** (&lt;30s).
2. **Vercel Instant Rollback:** In Vercel Dashboard $\to$ Deployments $\to$ Promote previous production deployment to Live (&lt;5s).
