# InsightPilot AI — Vercel Frontend Cloud Deployment Runbook

**Project:** InsightPilot AI  
**Competition:** Accenture Innovation Challenge 2026 (Track 3: BusinessIntelligence.ai)  
**Target Platform:** Vercel Global Edge Network (Next.js 14 Static & Dynamic App)  
**Status:** `READY FOR OWNER PLATFORM AUTHORIZATION`

---

## 1. Frontend Architecture & Build Settings

- **Framework:** Next.js 14 (App Router)
- **Root Directory:** `frontend/next-app`
- **Build Output:** Static pre-rendered routes (`○ Static`) & Edge API rewrites.
- **Node.js Runtime:** 18.x or 20.x

---

## 2. Step-by-Step Vercel Deployment Instructions

### Step 1: Import Project into Vercel
1. Log in to your [Vercel Dashboard](https://vercel.com/).
2. Click **Add New...** $\to$ **Project**.
3. Import the GitHub repository: `https://github.com/ayus1234/InsighPilotAI.git`.

### Step 2: Configure Project Root & Build Settings
- **Project Name:** `insightpilot-ai`
- **Framework Preset:** **Next.js**
- **Root Directory:** Click **Edit** $\to$ Select `frontend/next-app` $\to$ Click **Continue**.
- **Build Command:** `npm run build` (Default)
- **Output Directory:** `.next` (Default)
- **Install Command:** `npm install` (Default)

### Step 3: Configure Environment Variables
In the **Environment Variables** section, add the following single variable:

| Key | Value | Description |
| :--- | :--- | :--- |
| `NEXT_PUBLIC_API_URL` | `https://[YOUR_RENDER_BACKEND_URL]` | The live production backend URL provisioned in Step 1. |

> [!IMPORTANT]
> Do NOT include a trailing slash in `NEXT_PUBLIC_API_URL` (e.g. use `https://insightpilot-api.onrender.com`, not `https://insightpilot-api.onrender.com/`).

### Step 4: Trigger Deployment
1. Click **Deploy**.
2. Vercel will build the 10 static routes and deploy them globally across edge CDN regions (&lt;60s build time).

---

## 3. Post-Deployment Verification Procedure

Once Vercel assigns the live `.vercel.app` domain:
1. **Homepage Loading:** Navigate to `https://[YOUR_VERCEL_APP].vercel.app/` and confirm the Executive Command Center renders.
2. **7 Core Screens Smoke Test:**
   - [ ] `/` (Executive Command Center)
   - [ ] `/root-cause` (Waterfall Decomposition)
   - [ ] `/investigation` (LangGraph Trace)
   - [ ] `/decision-graph` (Dynamic 6-Column Topology)
   - [ ] `/evidence` (SHA-256 Evidence Lineage)
   - [ ] `/recommendations` (Action Plan & What-If Simulation)
   - [ ] `/briefing` (Executive Briefing Narrative)
3. **CORS Synchronization:** Copy the live Vercel URL and update `CORS_ORIGINS` in your Render backend dashboard.
