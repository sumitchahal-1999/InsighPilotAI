# InsightPilot AI — Deployment Architecture Audit

**Project:** InsightPilot AI  
**Competition:** Accenture Innovation Challenge 2026 (Track 3: BusinessIntelligence.ai)  
**Document:** System Deployment Architecture, Runtime Dependencies & Production Gap Audit  
**Status:** `VERIFIED CURRENT STATE & PRODUCTION READINESS AUDIT`

---

## 1. Executive Summary

This audit establishes the baseline deployment readiness of **InsightPilot AI** as it transitions from a **Competition-Ready Prototype** to a **Production-Deployable Enterprise Application**.

### Foundational Architectural Invariant:
> **"Deterministic systems own quantitative truth.  
> LangGraph orchestrates investigation.  
> AI explains grounded facts."**

---

## 2. Current Architecture Inventory (Verified Current State)

### A. Frontend Architecture (Next.js 14 App Router)
- **Framework:** Next.js 14.2.35 (React 18, TypeScript, Tailwind CSS, Lucide Icons, Recharts).
- **Directory Location:** `frontend/next-app/`.
- **Static Page Generation:** 10 / 10 static pages compiled (`/`, `/root-cause`, `/investigation`, `/decision-graph`, `/evidence`, `/recommendations`, `/briefing`, `/_not-found`).
- **API Base URL Strategy:** Configurable via `NEXT_PUBLIC_API_URL` environment variable with safe local fallback (`http://127.0.0.1:8000`).
- **Build Output:** Production bundle verified with 0 lint warnings and 0 TypeScript errors.

### B. Backend Architecture (Python 3.11 FastAPI)
- **Framework:** FastAPI 0.115+ running on Uvicorn ASGI server.
- **Directory Location:** `backend/` and `analytics/`, `ai/`.
- **Endpoints Exposed:** 18 typed RESTful endpoints under `/api/v1` prefix.
- **Health Probes:** Dual lightweight liveness probes at `/health` and `/api/v1/health`.
- **Data Persistence:** Relational schemas with SQLite / PostgreSQL-compatible SQLAlchemy models.
- **AI Orchestration:** 11-node LangGraph state machine with dual-provider failover (Groq Llama 3.3 70B & Google Gemini 2.5 Flash).

---

## 3. Runtime Dependencies & Environment Matrix

| Layer | Runtime Requirement | Verified Version | Package Manager / Tool |
| :--- | :--- | :--- | :--- |
| **Backend Runtime** | Python 3.11+ | Python 3.11.x | `pip` (`requirements.txt`) |
| **Frontend Runtime** | Node.js 18.17+ / 20+ | Node.js 20.x | `npm` (`package.json`) |
| **Relational Storage** | Relational SQL / SQLite | SQLite 3 (Dev) / Postgres (Prod) | SQLAlchemy 2.0.36 + Alembic |
| **Process Manager** | Uvicorn / Gunicorn | Uvicorn 0.34+ | ASGI worker pool |
| **Reverse Proxy / CDN** | Nginx / Cloudflare / Vercel Edge | HTTPS / TLS 1.3 | Edge routing |

---

## 4. Environment Variables Audit

| Variable Name | Layer | Required / Optional | Default Value | Purpose |
| :--- | :---: | :---: | :--- | :--- |
| `APP_ENV` | Backend | Optional | `development` | Sets environment mode (`development`, `staging`, `production`, `test`). |
| `API_HOST` | Backend | Optional | `127.0.0.1` | Network interface for FastAPI binding (`0.0.0.0` in containers). |
| `API_PORT` | Backend | Optional | `8000` | Port for ASGI server listener. |
| `API_PREFIX` | Backend | Optional | `/api/v1` | Base route prefix for API endpoints. |
| `CORS_ORIGINS` | Backend | Required in Prod | `http://localhost:3000,...` | Comma-separated list of allowed frontend domain origins. |
| `NEXT_PUBLIC_API_URL` | Frontend | Required in Prod | `http://127.0.0.1:8000` | Base URL used by browser to query backend API. |
| `DATABASE_URL` | Backend | Optional | `sqlite:///data/insightpilot.db` | Connection string for relational database. |
| `GEMINI_API_KEY_1` | Backend | Optional | `""` | Primary key for Google Gemini 2.5 Flash. |
| `GEMINI_API_KEY_2` | Backend | Optional | `""` | Failover pool key for Google Gemini. |
| `GROQ_API_KEY_1` | Backend | Optional | `""` | Primary key for Groq Llama 3.3 70B. |
| `GROQ_API_KEY_2` | Backend | Optional | `""` | Failover pool key for Groq. |
| `CONFIDENCE_ABSTENTION_THRESHOLD` | Backend | Locked Invariant | `0.65` | Mandatory safety threshold (&lt;65% triggers abstention). |

---

## 5. Production Readiness Gap Analysis

| Subsystem | Verified Current State | Production Deployment Gap | Recommended Remediation |
| :--- | :--- | :--- | :--- |
| **Frontend Deployment** | Local development & Next.js production build (`npm run build`) passing. | Needs external CDN/edge hosting (e.g. Vercel, Cloudflare Pages). | Deploy static/hybrid Next.js bundle to Vercel/Netlify with `NEXT_PUBLIC_API_URL`. |
| **Backend Deployment** | Local Uvicorn server running cleanly on port 8000. | Needs containerized / PaaS hosting (e.g. Render, Railway, Fly.io, AWS ECS). | Containerize FastAPI with Docker/Uvicorn workers behind HTTPS load balancer. |
| **CORS Origins** | Configured for localhost development ports. | Needs production frontend domain added to `CORS_ORIGINS`. | Set `CORS_ORIGINS=https://your-domain.vercel.app` in production environment. |
| **Database Tier** | SQLite local database with relational schemas. | SQLite file lock constraints during concurrent webhooks. | Switch `DATABASE_URL` to managed PostgreSQL (Supabase/Neon/AWS RDS) for multi-tenant scale. |
| **Monitoring & Telemetry**| Console logging and in-memory test telemetry. | Centralized cloud log aggregation. | Connect structured JSON logs to Datadog/CloudWatch. |
