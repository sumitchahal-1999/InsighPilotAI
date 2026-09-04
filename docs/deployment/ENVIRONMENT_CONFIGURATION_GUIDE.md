# InsightPilot AI — Environment Configuration & Security Guide

**Project:** InsightPilot AI  
**Competition:** Accenture Innovation Challenge 2026 (Track 3: BusinessIntelligence.ai)  
**Document:** Multi-Environment Configuration, Variable Specifications & Credential Handling  
**Status:** `PRODUCTION CONFIGURATION MANUAL`

---

## 1. Multi-Environment Overview

InsightPilot AI supports three standard operational environments:
1. **Local Development:** Developers running FastAPI on port 8000 and Next.js on port 3000.
2. **Staging / Preview:** Pull request preview deployments with automated test validation.
3. **Production:** Scaled, HTTPS-secured cloud infrastructure serving executives and judges.

---

## 2. Environment Variable Master Matrix

| Variable Name | Environment | Required? | Recommended Production Value | Description |
| :--- | :---: | :---: | :--- | :--- |
| `APP_ENV` | Backend | Optional | `production` | Sets application runtime environment. |
| `API_HOST` | Backend | Optional | `0.0.0.0` | Host interface for FastAPI binding (use `0.0.0.0` in Docker/cloud). |
| `API_PORT` | Backend | Optional | `8000` | Port for ASGI listener (Render/Railway dynamically inject `PORT`). |
| `API_PREFIX` | Backend | Optional | `/api/v1` | Base route prefix for API endpoints. |
| `CORS_ORIGINS` | Backend | **REQUIRED** | `https://insightpilot.vercel.app` | Comma-separated list of allowed frontend domain origins. |
| `NEXT_PUBLIC_API_URL` | Frontend | **REQUIRED** | `https://api.insightpilot.ai` | Base URL used by browser to query backend API. |
| `DATABASE_URL` | Backend | Optional | `postgresql://user:pass@host:5432/db` | Connection string for PostgreSQL (defaults to SQLite if omitted). |
| `GEMINI_API_KEY_1` | Backend | Optional | `AIzaSy...` | Primary Google Gemini API key. |
| `GEMINI_API_KEY_2` | Backend | Optional | `AIzaSy...` | Secondary failover Google Gemini key. |
| `GEMINI_MODEL` | Backend | Optional | `gemini-2.5-flash` | Gemini model family identifier. |
| `GROQ_API_KEY_1` | Backend | Optional | `gsk_...` | Primary Groq API key. |
| `GROQ_API_KEY_2` | Backend | Optional | `gsk_...` | Secondary failover Groq key. |
| `GROQ_MODEL` | Backend | Optional | `llama-3.3-70b-versatile` | Groq Llama model identifier. |
| `CONFIDENCE_ABSTENTION_THRESHOLD` | Backend | Locked | `0.65` | Mandatory safety threshold (&lt;65% triggers abstention). |
| `MATERIALITY_VARIANCE_THRESHOLD` | Backend | Locked | `-0.03` | Anomaly trigger threshold (-3.00%). |

---

## 3. Environment-Specific Setup Instructions

### A. Local Development Setup
1. Copy `.env.example` to `.env` in the repository root:
   ```bash
   cp .env.example .env
   ```
2. Copy `frontend/next-app/.env.example` to `frontend/next-app/.env.local`:
   ```bash
   cp frontend/next-app/.env.example frontend/next-app/.env.local
   ```
3. Start backend on `http://127.0.0.1:8000` and frontend on `http://localhost:3000`.

### B. Production Deployment Setup (e.g. Vercel + Render)
1. **Frontend (Vercel):**
   - In Vercel Project Settings $\to$ Environment Variables:
     - Add `NEXT_PUBLIC_API_URL` = `https://your-backend-api.onrender.com`
2. **Backend (Render / Railway / Fly.io):**
   - In Backend Service Settings $\to$ Environment Variables:
     - Add `APP_ENV` = `production`
     - Add `CORS_ORIGINS` = `https://your-frontend.vercel.app`
     - Add `GROQ_API_KEY_1` = `[YOUR_GROQ_KEY]`
     - Add `GEMINI_API_KEY_1` = `[YOUR_GEMINI_KEY]`
     - Add `DATABASE_URL` = `[YOUR_POSTGRESQL_CONNECTION_STRING]` (Optional)

---

## 4. Secret & Credential Handling Rules

1. **Zero Hardcoded Secrets:** Never insert live API keys, tokens, or database passwords into `.env.example`, code files, or Git commits.
2. **Client-Side Secret Isolation:** Never prefix secret API keys with `NEXT_PUBLIC_`. The frontend bundle must only contain `NEXT_PUBLIC_API_URL`.
3. **Repository History Protection:** Hardened `.gitignore` (66 rules) prevents tracking `.env`, `.env.local`, `.pem`, and temporary test caches.
