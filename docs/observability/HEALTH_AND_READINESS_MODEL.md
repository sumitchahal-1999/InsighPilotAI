# InsightPilot AI — Health & Readiness Reliability Model

**Project:** InsightPilot AI  
**Competition:** Accenture Innovation Challenge 2026 (Track 3: BusinessIntelligence.ai)  
**Document:** Health Probe Taxonomy, Liveness/Readiness Semantics & Degradation Hierarchy  
**Status:** `OPERATIONAL RELIABILITY SPECIFICATION`

---

## 1. Health Probe Hierarchy & Operational Semantics

InsightPilot AI decouples fast process liveness from deep system readiness to prevent cascading restarts during upstream provider hiccups:

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│ 1. LIVENESS PROBE (GET /health & GET /api/v1/health)                        │
│ • SLA: <1 ms execution time                                                 │
│ • Purpose: Process liveness probe for Kubernetes / Docker / AWS ALB / Render│
│ • Failure Condition: ASGI event loop deadlock or unhandled process crash     │
│ • Orchestrator Action on Failure: Restart container worker                  │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│ 2. READINESS PROBE (GET /api/v1/demo/readiness)                             │
│ • SLA: ~15 ms execution time                                                │
│ • Purpose: Deep 12-subsystem health verification before routing traffic     │
│ • Evaluates: Database rows, KPI parity, Driver engine, Evidence SHA-256     │
│ • Failure Condition: Missing data files, corrupted schemas, broken parity  │
│ • Orchestrator Action on Failure: Hold traffic / alert on-call engineer     │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Subsystem Degradation Matrix

| Subsystem | Impact of Failure | Overall API Status | Fallback / Mitigation Strategy |
| :--- | :--- | :---: | :--- |
| **Relational Database / DataLoader** | Cannot load invoices or inventory. | `DEGRADED / 503` | Fall back to cached local CSV repository files. |
| **Deterministic Analytics Engine** | Cannot compute variance or drivers. | `UNHEALTHY / 500` | Block traffic; trigger immediate release rollback. |
| **LangGraph Orchestrator** | Cannot run multi-node state graph. | `UNHEALTHY / 500` | Fall back to direct deterministic API responses. |
| **Google Gemini API Provider** | Cannot perform multimodal vision. | **`HEALTHY (200 OK)`** | Automatic failover to Groq Llama 3.3 70B pool. |
| **Groq Llama 3.3 70B Provider** | Cannot perform rapid text synthesis. | **`HEALTHY (200 OK)`** | Automatic failover to Google Gemini 2.5 Flash pool. |
| **All AI Providers Unavailable** | Zero upstream LLM response. | **`HEALTHY (200 OK)`** | Grounded deterministic synthesis engine serves 100% compliant narrative. |

---

## 3. Resilience Principle: AI Provider Independence

> [!IMPORTANT]
> The health and availability of InsightPilot AI **NEVER** depends on third-party foundation model uptime. Because deterministic analytics and evidence lineage operate locally, the platform serves 100% accurate financial variance explanations even when upstream AI APIs suffer global outages.
