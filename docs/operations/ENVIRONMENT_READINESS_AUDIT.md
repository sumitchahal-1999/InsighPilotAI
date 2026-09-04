# InsightPilot AI — Environment Readiness & Configuration Audit

**Project:** InsightPilot AI  
**Competition:** Accenture Innovation Challenge 2026 (Track 3: BusinessIntelligence.ai)  
**Document:** Environment Variable Taxonomy, Secret Boundaries & Configuration Matrix  
**Status:** `AUDIT COMPLETE — LOCAL & PRODUCTION READY`

---

## 1. Environment Variable Master Taxonomy

| Variable Name | Layer / Component | Purpose | Secret? | Startup Required? | Missing Behavior / Fallback | Classification |
| :--- | :--- | :--- | :---: | :---: | :--- | :---: |
| **`APP_ENV`** | Backend (FastAPI) | Sets runtime environment (`development`, `production`). | No | No (Defaults: `development`) | Safe development mode with open CORS. | `CONFIGURATION REQUIRED` |
| **`PORT`** | Backend (FastAPI) | ASGI listener port (defaults: `8000`). | No | No (Defaults: `8000`) | Listens on port 8000. | `PRODUCTION REQUIRED` |
| **`CORS_ORIGINS`** | Backend (FastAPI) | Allowed HTTP origins whitelist for CORS. | No | No (Defaults: `*` in dev) | Wildcards disabled in prod; allows local dev. | `PRODUCTION REQUIRED` |
| **`GROQ_API_KEY_1`** | AI Router (Groq) | Primary API key for Llama 3.3 70B pool 1. | **Yes** | No | Falls back to Pool 2 or Gemini or local template. | `OPTIONAL / SECRET` |
| **`GROQ_API_KEY_2`** | AI Router (Groq) | Secondary API key for Llama 3.3 70B pool 2. | **Yes** | No | Falls back to Gemini or local template. | `OPTIONAL / SECRET` |
| **`GEMINI_API_KEY_1`** | AI Router (Gemini)| Primary API key for Gemini 2.5 Flash pool 1. | **Yes** | No | Falls back to Gemini Pool 2 or local template. | `OPTIONAL / SECRET` |
| **`GEMINI_API_KEY_2`** | AI Router (Gemini)| Secondary API key for Gemini 2.5 Flash pool 2. | **Yes** | No | Falls back to local grounded deterministic engine. | `OPTIONAL / SECRET` |
| **`DATABASE_URL`** | Data / Storage | SQLAlchemy SQLite/PostgreSQL connection string. | No/Yes | No (Defaults: local SQLite) | Uses in-memory / local SQLite repo. | `DEVELOPMENT ONLY` |
| **`NEXT_PUBLIC_API_URL`**| Frontend (Next.js)| Base URL for FastAPI backend proxy and fetch client. | No | No (Defaults: `http://127.0.0.1:8000`) | Next.js rewrites route to localhost:8000. | `PRODUCTION REQUIRED` |

---

## 2. Zero-Secret Guarantee & Security Isolation

1. **Client Bundle Isolation:** The Next.js client bundle only includes variables prefixed with `NEXT_PUBLIC_`. Upstream foundation model API keys (`GROQ_API_KEY_*`, `GEMINI_API_KEY_*`) are strictly backend-only and never leaked to the browser.
2. **Git Repository Hygiene:** Root `.env` and `frontend/next-app/.env.local` are strictly excluded from Git via `.gitignore`.
3. **Template Parity:** Standardized `.env.example` and `frontend/next-app/.env.example` provide placeholder configurations for platform deployment.
