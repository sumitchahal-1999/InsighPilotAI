# InsightPilot AI — Frontend Live Deployment Report

**Project:** InsightPilot AI  
**Competition:** Accenture Innovation Challenge 2026 (Track 3: BusinessIntelligence.ai)  
**Document:** Workstream C — Next.js 14 Frontend Edge Deployment & Route Verification  
**Status:** `CONFIGURATION VERIFIED — EXTERNAL ACTION REQUIRED FOR LIVE HOSTING`

---

## 1. Frontend Verification & Configuration Status

| Area | Status | Verified Details |
| :--- | :---: | :--- |
| **Source Directory** | `LOCAL VERIFIED` | `frontend/next-app/` |
| **Framework & Engine** | `LOCAL VERIFIED` | Next.js 14.2.35 App Router (React 18 / TypeScript 5 / Tailwind CSS). |
| **Node.js Runtime** | `LOCAL VERIFIED` | Node.js 18.17+ / 20.x verified. |
| **Production Build** | `LOCAL VERIFIED` | `npm run build` generates 10 / 10 static pre-rendered pages with 0 errors and 0 lint warnings. |
| **API Base URL Binding**| `LOCAL VERIFIED` | `lib/api.ts` binds to `process.env.NEXT_PUBLIC_API_URL` with local fallback. |
| **Zero Hardcoded URLs** | `LOCAL VERIFIED` | No hardcoded localhost strings in production client bundles. |
| **Live Edge Deployment**| `EXTERNAL ACTION REQUIRED` | Requires connecting GitHub repository to Vercel/Netlify dashboard and setting `NEXT_PUBLIC_API_URL`. |

---

## 2. Seven-Screen Route Verification Matrix

All 7 core application screens compile cleanly into pre-rendered static routes:

| Route Path | Screen Name | Build Classification | Bundle Size | First Load JS |
| :--- | :--- | :---: | :---: | :---: |
| **`/`** | Executive Command Center | `○ (Static)` | 105 kB | 214 kB |
| **`/root-cause`** | 4-Factor Causal Decomposition | `○ (Static)` | 5.4 kB | 114 kB |
| **`/investigation`** | 11-Node LangGraph Lifecycle | `○ (Static)` | 6.15 kB | 115 kB |
| **`/decision-graph`** | 6-Column Dynamic Causal Graph | `○ (Static)` | 5.24 kB | 114 kB |
| **`/evidence`** | SHA-256 Cryptographic Lineage | `○ (Static)` | 6.88 kB | 115 kB |
| **`/recommendations`** | Action Plan & Simulation Slider | `○ (Static)` | 4.5 kB | 113 kB |
| **`/briefing`** | Executive Narrative Briefing | `○ (Static)` | 5.37 kB | 114 kB |

---

## 3. Vercel Deployment Settings

- **Root Directory:** `frontend/next-app`
- **Framework Preset:** `Next.js`
- **Build Command:** `npm run build`
- **Output Directory:** `.next`
- **Environment Variable:** `NEXT_PUBLIC_API_URL` = `https://[LIVE_BACKEND_URL]`

---

## 4. Live Deployment Status

```text
Frontend Live URL:
STATUS: TBD — EXTERNAL ACTION REQUIRED (e.g., https://insightpilot-ai.vercel.app)

Client-to-API Connectivity:
STATUS: LOCAL VERIFIED (against 127.0.0.1:8000) / PENDING LIVE VERCEL PROBE
```
