# InsightPilot AI — Rate Limit & Resilience Audit

**Project:** InsightPilot AI  
**Competition:** Accenture Innovation Challenge 2026 (Track 3: BusinessIntelligence.ai)  
**Document:** Rate Limiting, Timeout Policies, Backoff Mechanics & Circuit Breaking  
**Status:** `RESILIENCE AUDIT COMPLETE`

---

## 1. Resilience Mechanism Classification Matrix

| Mechanism | Current Status | Implemented Behavior / Responsibility |
| :--- | :---: | :--- |
| **API Request Timeout** | `IMPLEMENTED` | `httpx.Timeout(30.0)` enforced on all outbound AI provider network requests. |
| **AI Provider Key Rotation** | `IMPLEMENTED` | Dual-pool key rotation across Groq (`GROQ_API_KEY_1`, `_2`) and Gemini (`GEMINI_API_KEY_1`, `_2`). |
| **Provider Failover Cascading**| `IMPLEMENTED` | Cascades on HTTP 429, 500, 503, Quota Exceeded, and Connection Timeout. |
| **Grounded Fallback Engine** | `IMPLEMENTED` | Deterministic template synthesis ensures 100% operational uptime without LLMs. |
| **Public API Rate Limiting** | `EXTERNAL PLATFORM` | Delegated to Cloudflare / Vercel Edge / Render WAF (prevents DDoS at edge). |
| **Client Exponential Backoff**| `CONFIGURATION READY` | Frontend `lib/api.ts` retry wrapper available for unstable mobile networks. |
| **Database Connection Pooling**| `IMPLEMENTED` | SQLAlchemy connection pool handles concurrent async requests. |
| **Circuit Breaking** | `PARTIALLY IMPLEMENTED`| Provider router skips repeatedly failing pools during active investigation runs. |

---

## 2. Timeout & Retry Policy Specifications

```text
Outbound AI Provider SLA:
  • Connect Timeout:    5.0 seconds
  • Read/Write Timeout: 30.0 seconds
  • Max Retries:        1 retry per pool before cascading to next pool
  • Total Chain Budget: 35.0 seconds maximum before falling back to local synthesis
```
