# InsightPilot AI — Production Observability Architecture

**Project:** InsightPilot AI  
**Competition:** Accenture Innovation Challenge 2026 (Track 3: BusinessIntelligence.ai)  
**Document:** System Observability Blueprint, Telemetry Pipelines & Monitoring Strategy  
**Status:** `OBSERVABILITY FOUNDATION VERIFIED`

---

## 1. Executive Summary & Foundational Invariant

InsightPilot AI enforces a strict architectural boundary between deterministic truth and AI reasoning:
> **"Deterministic systems own quantitative truth.  
> LangGraph orchestrates investigation.  
> AI explains grounded facts."**

The production observability architecture ensures that system health, request lifecycles, execution latencies, failover events, and analytical outputs are transparently diagnosable across all deployment tiers without leaking confidential business records, customer PII, or upstream foundation model API keys.

---

## 2. Telemetry & Observability Architecture Overview

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│ 1. EDGE / CLIENT TELEMETRY (Vercel / Browser)                              │
│ • Client Request Headers: X-Request-ID propagation                          │
│ • Client-Side Latency: Time-to-Interactive, First Contentful Paint          │
│ • UI Error Boundaries: React component error isolation                      │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │ HTTPS / JSON with X-Request-ID
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ 2. API GATEWAY OBSERVABILITY (FastAPI / Uvicorn)                            │
│ • Request Correlation Middleware: Auto-generates / forwards X-Request-ID    │
│ • Response Headers: X-Request-ID, X-Response-Time-Ms                        │
│ • Structured JSON Logging: Method, path, status, latency_ms, client_ip      │
│ • Dual Health Probes: /health (Liveness) & /api/v1/demo/readiness (12 Subs) │
└──────────────────┬───────────────────────────────────────┬──────────────────┘
                   │                                       │
                   ▼                                       ▼
┌──────────────────────────────────────┐ ┌────────────────────────────────────┐
│ 3. ANALYTICS & LINEAGE OBSERVABILITY │ │ 4. AI ROUTER & FAILOVER TELEMETRY  │
│ • Sub-millisecond Execution Profiler │ │ • In-Memory Failover Event Log     │
│ • 4-Factor Variance Contribution Sum │ │ • Key Pool Rotation Telemetry      │
│ • 6-Factor Confidence Scoring (89%)  │ │ • Rate Limit (429) & Quota Monitor │
│ • SHA-256 Hash Integrity Validator   │ │ • Post-Generation Grounding Guard  │
└──────────────────────────────────────┘ └────────────────────────────────────┘
```

---

## 3. Observability Classification Matrix

| Layer | Implemented / Verified in Repo | Platform Dependent / Recommended |
| :--- | :--- | :--- |
| **Request Tracing** | `IMPLEMENTED` — `RequestCorrelationMiddleware` attaches `X-Request-ID` and `X-Response-Time-Ms`. | Distributed tracing (OpenTelemetry / Jaeger). |
| **Structured Logging** | `IMPLEMENTED` — JSON telemetry emitter in `backend/app/logging.py`. | CloudWatch / Datadog / Papertrail ingestion. |
| **Health Probes** | `IMPLEMENTED` — `/health`, `/api/v1/health`, `/api/v1/demo/readiness`. | UptimeRobot / Pingdom external probes. |
| **AI Provider Telemetry**| `IMPLEMENTED` — Dual-pool failover logger & rate limit event tracker in `ai/orchestration/`. | Foundation model cost analytics dashboard. |
| **Error Handling** | `IMPLEMENTED` — Typed `APIError` hierarchy in `backend/app/errors.py` with sanitized responses. | Sentry / Bugsnag exception reporting. |
| **Metric Invariance** | `IMPLEMENTED` — Automated regression suite (225 tests) locking canonical values. | Prometheus / Grafana timeseries alerting. |

---

## 4. Privacy & Secret Isolation Boundaries

1. **Zero Key Logging:** Upstream API keys (`GROQ_API_KEY_*`, `GEMINI_API_KEY_*`) are strictly excluded from logging formatters.
2. **Payload Sanitization:** Raw CSV rows and unmasked customer identifiers are excluded from HTTP request log payloads.
3. **Internal Traceback Masking:** Public error responses return standardized JSON error codes without revealing internal file paths or database credentials.
