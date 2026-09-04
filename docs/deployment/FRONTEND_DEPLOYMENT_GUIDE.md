# InsightPilot AI — Frontend Production Deployment Guide

**Project:** InsightPilot AI  
**Competition:** Accenture Innovation Challenge 2026 (Track 3: BusinessIntelligence.ai)  
**Document:** Next.js 14 Frontend Production Build, Edge Hosting & CDN Configuration  
**Status:** `PRODUCTION READINESS SPECIFICATION`

---

## 1. Frontend Overview & Build Characteristics

The InsightPilot AI user interface is built on **Next.js 14 App Router** (React 18, TypeScript, Tailwind CSS).

### Key Production Characteristics:
- **Zero Server-Side Rendering Bottlenecks:** All 10 application pages are pre-rendered as static content (`○ Static`), maximizing edge CDN cache hit rates and sub-second page loads.
- **Client-Side Data Fetching:** Dynamic API requests query the backend via `lib/api.ts` using the environment-driven `NEXT_PUBLIC_API_URL`.
- **First Load JS Shared:** Lightweight bundle (87.5 kB shared baseline).

---

## 2. Deploying to Vercel (Recommended Edge Platform)

Vercel provides native zero-configuration hosting for Next.js App Router projects.

### Step-by-Step Vercel Deployment:
1. **Connect GitHub Repository:**
   - Go to [Vercel Dashboard](https://vercel.com/) $\to$ **Add New Project**.
   - Import `https://github.com/ayus1234/InsighPilotAI.git`.
2. **Configure Project Settings:**
   - **Framework Preset:** Next.js
   - **Root Directory:** `frontend/next-app` (Set root to subfolder).
   - **Build Command:** `npm run build`
   - **Output Directory:** `.next` (default)
3. **Set Environment Variables:**
   - Add `NEXT_PUBLIC_API_URL`: URL of your deployed backend (e.g. `https://insightpilot-api.onrender.com`).
4. **Deploy:**
   - Click **Deploy**. Vercel will build and assign an HTTPS URL (e.g. `https://insightpilot-ai.vercel.app`).
5. **Update Backend CORS:**
   - Add the assigned Vercel URL to the backend's `CORS_ORIGINS` environment variable.

---

## 3. Alternative Hosting: Docker Container / Node.js Server

For self-hosted Kubernetes, AWS ECS, or virtual private servers:

### Standalone Production Build:
```bash
cd frontend/next-app
npm ci
npm run build
npm run start -p 3000
```

---

## 4. Frontend Production Verification Checklist

- [x] Static build succeeds (`npm run build`) with 10/10 pages generated.
- [x] Zero TypeScript errors and zero ESLint compilation warnings.
- [x] `NEXT_PUBLIC_API_URL` environment variable properly consumed in `lib/api.ts`.
- [x] Responsive layout renders cleanly across mobile, tablet, and 1080p/4K desktop viewports.
- [x] Dark-mode glassmorphism and Lucide icons load with zero layout shifts.
