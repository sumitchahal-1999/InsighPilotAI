# InsightPilot AI — Rate Limiting & Abuse Resilience Architecture

**Project:** InsightPilot AI  
**Competition:** Accenture Innovation Challenge 2026 (Track 3: BusinessIntelligence.ai)  
**Document:** Rate Limiting Architecture, Anti-Abuse Strategies & Edge Defense  
**Status:** `ABUSE RESILIENCE SPECIFIED`

---

## 1. Rate Limiting Multi-Tier Classification

| Tier | Protection Scope | Implementation Mechanism | Status |
| :--- | :--- | :--- | :---: |
| **Tier 1: Upstream AI Provider Protection** | Outbound API call throttling and key pool rotation. | `ProviderRouter` in `ai/orchestration/`. | `REPOSITORY IMPLEMENTED` |
| **Tier 2: Application Circuit Breaking** | Cascades on 429 / 503 to local grounded template synthesis. | `ai/orchestration/provider_router.py`. | `REPOSITORY IMPLEMENTED` |
| **Tier 3: Inbound HTTP Rate Limiting** | Per-IP request quotas (e.g. 100 req/min). | Render WAF / Cloudflare Rate Limiting / Vercel Edge. | `DEPLOYMENT REQUIREMENT` |
| **Tier 4: Distributed Token Bucket** | Redis-backed distributed rate limiter. | Recommended for multi-region enterprise clusters. | `FUTURE RECOMMENDATION` |

---

## 2. Endpoint Abuse Risk Profile & Recommended Limits

| Endpoint Category | Cost / CPU Overhead | Target Endpoint | Recommended Cloud Rate Limit |
| :--- | :---: | :--- | :---: |
| **High Overhead (AI Calls)** | High (Tokens / LLM) | `POST /api/v1/ai/explain/*` | 20 requests / min / IP |
| **Medium Overhead (Simulations)** | Low (Deterministic) | `POST /api/v1/simulations/run` | 60 requests / min / IP |
| **Standard Analytical Routes** | Low (In-Memory) | `GET /api/v1/kpis`, `GET /api/v1/investigations/*` | 120 requests / min / IP |
| **Health Probes** | Sub-millisecond | `GET /health` | 300 requests / min / IP |

---

## 3. Preservation of Judge & Testing Workflows

- In-memory automated test execution (232 tests) and judge demonstration flows are never throttled during local evaluation.
- Cloud edge rate limits only apply to untrusted public IP ranges.
