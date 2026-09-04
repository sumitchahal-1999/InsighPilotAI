# InsightPilot AI — Production Deployment Architecture

**Project:** InsightPilot AI  
**Competition:** Accenture Innovation Challenge 2026 (Track 3: BusinessIntelligence.ai)  
**Document:** Recommended Cloud Topology, Service Boundaries & Security Perimeter  
**Status:** `RECOMMENDED PRODUCTION TOPOLOGY SPECIFICATION`

---

## 1. High-Level Production Deployment Topology

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│ DEVELOPER / CI/CD AUTOMATION                                                │
│ • GitHub Repository (main branch)                                           │
│ • Automated Dataset Validation & Full Regression Test Suite (211 Tests)     │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │ Git Push / Release Tag
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ 1. FRONTEND EDGE TIER (e.g. Vercel / Cloudflare Pages / AWS CloudFront)     │
│ • Next.js 14 App Router (React 18 / TypeScript / Tailwind CSS)              │
│ • 10 Static Pre-Rendered Routes (Zero Server-Side Execution Bottlenecks)    │
│ • Environment Variable: NEXT_PUBLIC_API_URL -> https://api.insightpilot.ai │
│ • TLS 1.3 / HTTPS Termination with Automated Global CDN Caching             │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │ HTTPS REST / JSON API Calls
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ 2. BACKEND API GATEWAY TIER (e.g. Render / Railway / Fly.io / AWS ECS)     │
│ • Python 3.11 FastAPI running on Uvicorn ASGI Worker Pool                   │
│ • CORS Middleware: Restricted to Verified Frontend Domains (No Wildcards)  │
│ • Lightweight Liveness / Readiness Probes (/health & /api/v1/health)        │
│ • Pydantic v2 Request/Response Schema Validation                            │
└──────────────────┬───────────────────────────────────────┬──────────────────┘
                   │                                       │
                   ▼                                       ▼
┌──────────────────────────────────────┐ ┌────────────────────────────────────┐
│ 3. DETERMINISTIC ANALYTICS CORE      │ │ 4. AGENTIC ORCHESTRATION LAYER     │
│ • Period-over-Period Variance Math   │ │ • 11-Node LangGraph State Graph    │
│ • 4-Factor Causal Attribution Engine │ │ • 65% Mandatory Abstention Gate    │
│ • 6-Factor Confidence Engine (89%)   │ │ • Multi-Pool Provider Router       │
│ • SHA-256 Cryptographic Hash Engine  │ │ • Post-Generation Validator        │
│ • What-If Elasticity Simulation      │ │ • Dynamic 6-Column Decision Graph  │
└──────────────────┬───────────────────┘ └─────────────────┬──────────────────┘
                   │                                       │
                   ▼                                       ▼
┌──────────────────────────────────────┐ ┌────────────────────────────────────┐
│ 5. MANAGED RELATIONAL DATA STORAGE   │ │ 6. SECURE AI PROVIDER GATEWAY      │
│ • Managed PostgreSQL (RDS/Supabase)  │ │ • Groq Llama 3.3 70B (Primary)     │
│ • Relational Invoices & Inventory    │ │ • Google Gemini 2.5 Flash (Vision) │
│ • SQLAlchemy 2.0 + Alembic Migrations│ │ • Grounded Deterministic Fallback  │
└──────────────────────────────────────┘ └────────────────────────────────────┘
```

---

## 2. Service Boundary Specifications

### Boundary 1: Frontend Edge to Backend API (CORS & HTTPS)
- **Protocol:** Strict HTTPS (TLS 1.3).
- **CORS Configuration:** `CORS_ORIGINS` explicitly set to production frontend domain (e.g., `https://insightpilot.vercel.app`).
- **Data Exchange:** JSON payloads adhering to typed Pydantic/TypeScript contracts.

### Boundary 2: Backend API to Analytics Engine (Zero LLM Contamination)
- **Protocol:** Internal in-process synchronous / asynchronous Python function calls.
- **Data Integrity:** Analytics engine executes directly against relational database models; LLMs have zero write access and zero database connection strings.

### Boundary 3: Backend API to External AI Providers (Credential Isolation)
- **Protocol:** Secure outbound HTTPS via official SDKs (`google-genai`, `groq`).
- **Data Minimization:** Only aggregated quantitative summaries and abstracted evidence IDs are passed in prompt context. Raw customer records remain inside the enterprise boundary.
- **Failover Chain:** `Groq Pool 1` $\to$ `Groq Pool 2` $\to$ `Gemini Pool 1` $\to$ `Gemini Pool 2` $\to$ `Deterministic Fallback`.

---

## 3. Observability & Health Check Architecture

- **Liveness Probe (`/health` & `/api/v1/health`):** Sub-millisecond probe returning `{"status": "ok", "service": "insightpilot-api", "version": "2.0.0"}`.
- **Readiness Probe (`/api/v1/demo/readiness`):** Comprehensive system probe evaluating 12 analytical, database, and AI subsystems.
- **Structured Logging:** JSON-formatted application logs with timestamp, route, status code, latency, and sanitized telemetry.
