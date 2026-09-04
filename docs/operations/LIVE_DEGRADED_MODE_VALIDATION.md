# InsightPilot AI — Live Degraded Mode & Fallback Validation

**Project:** InsightPilot AI  
**Competition:** Accenture Innovation Challenge 2026 (Track 3: BusinessIntelligence.ai)  
**Document:** Fault-Tolerant Degraded Mode, AI Provider Outage & Fallback Validation Report  
**Status:** `VERIFIED LOCALLY (PASS) — LIVE CLOUD PENDING OWNER DEPLOYMENT`

---

## 1. Fault-Tolerant Architecture & Degradation Hierarchy

InsightPilot AI's deterministic analytics engine operates independently of external LLMs, ensuring zero downtime even during total AI provider outages:

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│ 1. PRIMARY PATH: EXTERNAL LLM PROVIDERS AVAILABLE                          │
│    • LangGraph multi-agent flow dispatches to Groq / Gemini pools           │
│    • LLM synthesizes natural language executive narratives                  │
│    • Hallucination Guard verifies grounded facts against deterministic truth│
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │
                                       ▼ (If AI Provider Down / Keys Missing)
┌─────────────────────────────────────────────────────────────────────────────┐
│ 2. FALLBACK PATH: GROUNDED DETERMINISTIC SYNTHESIS                          │
│    • Deterministic engine calculates 100% of figures, variances, & drivers  │
│    • Template-based grounded narrative generator produces CFO brief         │
│    • Zero hallucination, zero crashes, zero data drift                      │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Degraded Mode Verification Matrix

| Failure Scenario | Injected Condition | Expected Behavior | Local Status | Cloud Status |
| :--- | :--- | :--- | :---: | :---: |
| **Missing AI Keys** | Unset `GROQ_API_KEY_*` & `GEMINI_API_KEY_*` | Engages deterministic template synthesis. | `VERIFIED LOCALLY (PASS)` | `NOT EXECUTED (Live Pending)` |
| **Provider 429 Quota** | Mock HTTP 429 Rate Limit from Groq | Triggers failover to secondary pool / fallback. | `VERIFIED LOCALLY (PASS)` | `NOT EXECUTED (Live Pending)` |
| **Invalid Payload** | Out-of-bounds simulation request | Returns HTTP 422/400 sanitized error JSON. | `VERIFIED LOCALLY (PASS)` | `NOT EXECUTED (Live Pending)` |
| **Unknown KPI** | `GET /api/v1/investigations/unknown_kpi` | Returns clean HTTP 404 with error message. | `VERIFIED LOCALLY (PASS)` | `NOT EXECUTED (Live Pending)` |
