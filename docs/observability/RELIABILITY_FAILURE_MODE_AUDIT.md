# InsightPilot AI — Reliability & Failure Mode Audit

**Project:** InsightPilot AI  
**Competition:** Accenture Innovation Challenge 2026 (Track 3: BusinessIntelligence.ai)  
**Document:** Failure Mode and Effects Analysis (FMEA), Resilience Matrix & Recovery Paths  
**Status:** `RELIABILITY & FAULT-TOLERANCE AUDIT COMPLETE`

---

## 1. Failure Modes & Resilience Matrix

| # | Failure Scenario | Detection Mechanism | User-Facing Impact | Application Behavior | Recovery Path | Manual Action? |
| :-: | :--- | :--- | :--- | :--- | :--- | :---: |
| **1** | **Backend Unavailable** | Browser `fetch()` network error. | Frontend displays clean retry banner. | Graceful error boundary; UI does not crash. | Restart backend web service. | Yes (Ops) |
| **2** | **Frontend Up / Backend Down** | Next.js API client catch block. | Clear offline indicator shown on dashboard. | Fallback UI states rendered; no white screen. | Backend auto-restart / healthcheck recovery. | No |
| **3** | **Invalid Environment Config** | Missing required environment variables. | API starts with safe defaults (development mode). | Emits structured warning log on startup. | Correct environment variables in cloud dashboard. | Yes (Ops) |
| **4** | **Dataset Validation Failure** | `tests/validate_dataset.py` fails. | Build / deployment pipeline blocked. | Git CI/CD prevents broken code promotion. | Fix CSV column alignment or primary keys. | Yes (Dev) |
| **5** | **AI Provider HTTP 429/500** | AI Router telemetry exception. | Zero disruption to user. | Automatic failover to secondary pool / fallback model. | Internal key rotation; automatic retry. | No |
| **6** | **AI Provider Timeout (&gt;30s)**| `httpx.TimeoutException`. | Slight delay (~1-2s). | Drops slow provider; engages deterministic fallback. | Automatic circuit break. | No |
| **7** | **Multi-Pool AI Exhaustion** | Both Groq & Gemini pools exhausted. | Zero disruption to user. | Grounded deterministic synthesis serves verified narrative. | System operates 100% locally. | No |
| **8** | **CORS Misconfiguration** | Browser console CORS origin error. | API calls blocked by browser. | FastAPI returns HTTP 403 / rejects preflight. | Add frontend URL to `CORS_ORIGINS`. | Yes (Ops) |
| **9** | **Invalid Request Payload** | Pydantic validation exception. | HTTP 422 with descriptive error code. | Returns structured JSON error without crashing. | Client corrects JSON payload. | No |
| **10**| **Analytics Exception** | Python arithmetic / logic exception.| HTTP 500 error code. | Global exception handler masks stack trace. | Rollback release; fix analytics bug. | Yes (Dev) |
| **11**| **Deployment Restart** | SIGTERM signal sent to Uvicorn. | &lt;2s transition period. | Zero-downtime rolling restart (Render/Vercel). | New container worker takes over traffic. | No |
| **12**| **Cloud Platform Outage** | External DNS / Gateway failure. | Global outage message. | Static edge pages cached by Cloudflare/Vercel CDN. | Cloud vendor service restoration. | No |

---

## 2. Multi-Tiered Failover Chain

```text
[Incoming Investigation Request]
               │
               ▼
   [Deterministic Analytics Core]  ────────────> (100% Calculated Locally)
               │
               ▼
      [LangGraph Orchestrator]
               │
               ├──> 1. Try Groq Llama 3.3 70B (Pool 1)
               │          │ (If Rate-Limited / 429)
               │          ▼
               ├──> 2. Failover to Groq (Pool 2)
               │          │ (If Quota Exceeded)
               │          ▼
               ├──> 3. Failover to Google Gemini 2.5 Flash (Pool 1)
               │          │ (If Timeout / 503)
               │          ▼
               ├──> 4. Failover to Google Gemini (Pool 2)
               │          │ (If All Remote Pools Down)
               │          ▼
               └──> 5. Grounded Deterministic Template Engine (100% Reliable)
```
