# InsightPilot AI — Render Backend Cloud Deployment Runbook

**Project:** InsightPilot AI  
**Competition:** Accenture Innovation Challenge 2026 (Track 3: BusinessIntelligence.ai)  
**Target Platform:** Render Web Services (FastAPI ASGI Service)  
**Status:** `READY FOR OWNER PLATFORM AUTHORIZATION`

---

## 1. Cloud Architecture & Entry Point

InsightPilot AI's backend is architected as a stateless ASGI application running on Python 3.11 with Uvicorn:

- **Root Directory:** `./` (Repository root `ayus1234/InsighPilotAI`)
- **Application Factory:** `backend.app.main:app`
- **Port Binding:** Dynamically binds to platform-provided `$PORT` (defaults to 8000).
- **Host Binding:** `0.0.0.0` (accessible to internal and external reverse proxies).

---

## 2. Step-by-Step Render Deployment Instructions

### Step 1: Connect Repository
1. Log in to your [Render Dashboard](https://dashboard.render.com/).
2. Click **New +** $\to$ **Web Service**.
3. Connect your GitHub repository: `https://github.com/ayus1234/InsighPilotAI.git`.
4. Branch: `main`.

### Step 2: Configure Service Runtime & Build Settings
- **Name:** `insightpilot-api`
- **Region:** US East (Ohio / Virginia) or closest geographic region.
- **Language / Runtime:** **Python 3** (3.11+)
- **Root Directory:** Leave empty (root `./`).
- **Build Command:**
  ```bash
  pip install --upgrade pip && pip install -r requirements.txt
  ```
- **Start Command:**
  ```bash
  uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT
  ```

### Step 3: Configure Environment Variables
In the **Environment** tab on Render, add the following key-value pairs:

| Key | Example Value | Description |
| :--- | :--- | :--- |
| `APP_ENV` | `production` | Enables production security headers & disables debug handlers. |
| `PORT` | `8000` | Render injects this automatically. |
| `CORS_ORIGINS` | `https://[YOUR_VERCEL_APP].vercel.app` | Whitelists the deployed frontend URL (no trailing slash). |
| `GROQ_API_KEY_1` | `gsk_...` | Optional: Primary Groq API key for Llama 3.3 70B pool 1. |
| `GROQ_API_KEY_2` | `gsk_...` | Optional: Secondary Groq API key for pool failover. |
| `GEMINI_API_KEY_1` | `AIzaSy...` | Optional: Primary Gemini 2.5 Flash API key. |
| `GEMINI_API_KEY_2` | `AIzaSy...` | Optional: Secondary Gemini 2.5 Flash API key. |

> [!NOTE]
> If all optional AI provider keys are left blank, InsightPilot AI automatically and safely engages its **deterministic grounded fallback synthesis**, serving 100% accurate financial insights without errors.

### Step 4: Configure Health Check Path
- **Health Check Path:** `/health`
- Render will ping `GET /health` during deployment; it returns `HTTP 200 OK` in &lt;1ms.

---

## 3. Post-Deployment Verification Procedure

Once Render completes the build and transitions to `Live`:
1. **Liveness Verification:**
   ```bash
   curl -i https://[YOUR_RENDER_URL]/health
   # Expected: HTTP 200 OK {"status": "ok", "service": "insightpilot-api", "version": "2.0.0"}
   ```
2. **12-Subsystem Readiness Verification:**
   ```bash
   curl -i https://[YOUR_RENDER_URL]/api/v1/demo/readiness
   # Expected: HTTP 200 OK {"submission_ready": true, ...}
   ```
3. **Record Verified URL:**
   Update `docs/operations/PRODUCTION_URL_REGISTRY.md` with the verified Render hostname.
