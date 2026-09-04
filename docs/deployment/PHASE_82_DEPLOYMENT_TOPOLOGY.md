# InsightPilot AI — Phase 8.2 Production Deployment Topology

**Project:** InsightPilot AI  
**Competition:** Accenture Innovation Challenge 2026 (Track 3: BusinessIntelligence.ai)  
**Document:** Workstream A — Selected Production Cloud Topology & Hosting Infrastructure  
**Status:** `PLATFORM DECISION & TOPOLOGY APPROVED`

---

## 1. Selected Production Hosting Architecture

To transition InsightPilot AI from a local verified repository into a live, public, enterprise-grade cloud service, the following platform topology has been selected based on runtime efficiency, zero-config edge caching, and cost-free demonstration availability:

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│ 1. PUBLIC EVALUATOR / COMPETITION JUDGE                                     │
│ • Accesses global HTTPS edge domain via desktop, tablet, or mobile          │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │ HTTPS (TLS 1.3)
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ 2. FRONTEND EDGE HOSTING: VERCEL (OR CLOUDFLARE PAGES)                      │
│ • Directory: frontend/next-app/                                             │
│ • Framework Preset: Next.js 14 App Router                                   │
│ • Build Command: npm run build                                              │
│ • Static Optimization: 10/10 static pages pre-rendered (sub-50ms TTFB)      │
│ • Environment Variable: NEXT_PUBLIC_API_URL -> https://[BACKEND_URL]        │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │ REST / JSON API Calls over HTTPS
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ 3. BACKEND API GATEWAY: RENDER (OR RAILWAY / FLY.IO / AWS ECS)              │
│ • Runtime: Python 3.11 with Uvicorn ASGI Multi-Worker Server                │
│ • Blueprint: render.yaml / Dockerfile / Procfile                            │
│ • Start Command: python -m uvicorn backend.app.main:app --host 0.0.0.0      │
│ • Health Probes: /health (Liveness) & /api/v1/demo/readiness (12 Checks)    │
│ • CORS Whitelist: Explicitly tied to live Vercel domain                     │
└──────────────────┬───────────────────────────────────────┬──────────────────┘
                   │                                       │
                   ▼                                       ▼
┌──────────────────────────────────────┐ ┌────────────────────────────────────┐
│ 4. DETERMINISTIC ANALYTICS CORE      │ │ 5. AGENTIC ORCHESTRATION LAYER     │
│ • Period-over-Period Variance Engine │ │ • 11-Node LangGraph Lifecycle      │
│ • 4-Factor Causal Attribution Engine │ │ • 65% Mandatory Abstention Gate    │
│ • 6-Factor Confidence Engine (89%)   │ │ • Dual-Key AI Multi-Pool Router    │
│ • SHA-256 Cryptographic Hash Engine  │ │ • Post-Generation Grounding Guard  │
│ • Predictive Simulation Elasticity   │ │ • Dynamic 6-Column Decision Graph  │
└──────────────────────────────────────┘ └────────────────────────────────────┘
```

---

## 2. Platform Selection Rationale & Boundary Matrix

| Tier | Selected Platform | Purpose | Selection Rationale | External Authorization Required |
| :--- | :--- | :--- | :--- | :--- |
| **Frontend Edge** | **Vercel** | Host Next.js 14 App Router | Native Next.js 14 support, automatic SSL, edge CDN caching, instant rollback. | Vercel account login & GitHub repository import. |
| **Backend API** | **Render** | Host Python FastAPI API | Native Python 3.11 support, `render.yaml` infrastructure-as-code, free tier. | Render account login & GitHub repository import. |
| **Alternative Backend** | **Railway / Fly.io / Docker** | Containerized alternative | `Dockerfile` and `Procfile` ready for zero-friction container deployment. | Platform account authorization. |
| **Source Control & CI/CD** | **GitHub** (`main` branch) | Continuous deployment | Direct automated trigger upon pushing to `origin main`. | Public repo access (`ayus1234/InsighPilotAI`). |

---

## 3. Deployment Invariant Preservation

1. **Deterministic Analytics Execution:** All mathematical computations ($15.43M $\to$ $14.20M, -$1.23M / -7.97%, 43.2% Atlanta DC, 89% confidence) run exclusively in deterministic Python engines; no LLM performs quantitative arithmetic.
2. **AI Provider Decoupling:** The API operates fully with or without live Groq/Gemini API keys. When keys are omitted, the grounded deterministic fallback produces 100% compliant responses.
3. **Secret Isolation:** No API keys or credentials are baked into client bundles or deployment templates.
