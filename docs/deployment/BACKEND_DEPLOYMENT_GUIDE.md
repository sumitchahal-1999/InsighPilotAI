# InsightPilot AI — Backend Production Deployment Guide

**Project:** InsightPilot AI  
**Competition:** Accenture Innovation Challenge 2026 (Track 3: BusinessIntelligence.ai)  
**Document:** Python FastAPI Production Deployment, ASGI Configuration & Process Management  
**Status:** `PRODUCTION READINESS SPECIFICATION`

---

## 1. Backend Architecture & Runtime Overview

The InsightPilot AI backend is powered by **Python 3.11** and **FastAPI**, serving deterministic analytics, 11-node LangGraph orchestration, and grounded multi-model reasoning.

### Key Production Characteristics:
- **Stateless Microservice:** The API operates statelessly; worker nodes can be horizontally scaled behind a load balancer.
- **Lightweight Health Checks:** `/health` and `/api/v1/health` return sub-millisecond status responses without invoking expensive AI or database locks.
- **Relational Persistence:** SQLAlchemy 2.0 with support for SQLite (dev/prototype) and managed PostgreSQL (production).

---

## 2. Deploying to Render / Railway / Fly.io (Recommended PaaS)

### Step-by-Step Render Deployment:
1. **Create Web Service:**
   - Log into [Render Dashboard](https://render.com/) $\to$ **New Web Service**.
   - Connect repository: `https://github.com/ayus1234/InsighPilotAI.git`.
2. **Configure Build & Start Commands:**
   - **Environment:** Python
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python -m uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT --workers 2`
3. **Configure Environment Variables:**
   - `APP_ENV`: `production`
   - `CORS_ORIGINS`: `https://your-frontend.vercel.app`
   - `GROQ_API_KEY_1`: `[YOUR_GROQ_API_KEY]`
   - `GEMINI_API_KEY_1`: `[YOUR_GEMINI_API_KEY]`
   - `DATABASE_URL`: `[YOUR_POSTGRESQL_URL]` (Optional, defaults to SQLite)
4. **Health Check Path:**
   - Set Health Check Path to `/health`.
5. **Deploy:**
   - Render automatically deploys and assigns an HTTPS URL (e.g. `https://insightpilot-api.onrender.com`).

---

## 3. Containerized Deployment (Dockerfile & Docker Compose)

### Dockerfile Specification (Root Directory):
```dockerfile
FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code
COPY . .

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

# Start Uvicorn ASGI server
CMD ["python", "-m", "uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]
```

---

## 4. Backend Production Verification Checklist

- [x] Liveness probe `/health` and `/api/v1/health` return HTTP 200 `{"status": "ok"}`.
- [x] Readiness probe `/api/v1/demo/readiness` passes 12 subsystem checks.
- [x] CORS middleware restricts origins to verified frontend domains.
- [x] Full test suite passes: 211 / 211 tests passing.
- [x] Zero credential exposure in API response models or error logs.
