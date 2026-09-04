# InsightPilot AI — Live Production Smoke Test Protocol

**Project:** InsightPilot AI  
**Competition:** Accenture Innovation Challenge 2026 (Track 3: BusinessIntelligence.ai)  
**Document:** Live Cloud Smoke Testing Protocol, Verification Checklist & Execution Log  
**Status:** `LOCAL VERIFICATION PASSED — LIVE CLOUD PENDING OWNER DEPLOYMENT`

---

## 1. Live Cloud Smoke Testing Protocol

This protocol defines the exact test battery to execute against public cloud URLs (`Render` + `Vercel`) once provisioned:

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│ 1. BACKEND CLOUD REACHABILITY (Render)                                      │
│ • GET https://[BACKEND_URL]/health -> HTTP 200 OK                          │
│ • GET https://[BACKEND_URL]/api/v1/demo/readiness -> HTTP 200 (12 OK)      │
│ • Check X-Response-Time-Ms and X-Request-ID response headers                │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ 2. FRONTEND CLOUD REACHABILITY (Vercel)                                     │
│ • GET https://[FRONTEND_URL]/ -> HTTP 200 (Static HTML / JS Hydration)     │
│ • Verify zero client-side uncaught exceptions in browser developer console  │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ 3. END-TO-END CROSS-ORIGIN DATA FLOW (Vercel -> Render)                     │
│ • Browser fetches /api/v1/kpis over HTTPS with zero CORS errors             │
│ • Dynamic 6-Column Decision Graph renders 14 nodes and 17 edges             │
│ • What-If Simulation evaluates 90% availability -> +$341.4K recovery        │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Live Smoke Test Execution Checklist

| Test Item | Verification Target | Expected Response / Indicator | Local Status | Cloud Status |
| :--- | :--- | :--- | :---: | :---: |
| **B1: Liveness** | `GET /health` | `HTTP 200 {"status":"ok","version":"2.0.0"}` | `PASS` | `PENDING CLOUD DEPLOY` |
| **B2: Readiness**| `GET /api/v1/demo/readiness` | `HTTP 200 {"submission_ready": true}` | `PASS` | `PENDING CLOUD DEPLOY` |
| **B3: Security** | Inspect Response Headers | `X-Content-Type-Options: nosniff`, `DENY` | `PASS` | `PENDING CLOUD DEPLOY` |
| **F1: Homepage** | `GET /` | Executive Command Center renders | `PASS` | `PENDING CLOUD DEPLOY` |
| **F2: Waterfall**| `GET /root-cause` | 4-Factor Waterfall renders ($15.43M $\to$ $14.20M) | `PASS` | `PENDING CLOUD DEPLOY` |
| **F3: Trace** | `GET /investigation` | 11-Node LangGraph state diagram | `PASS` | `PENDING CLOUD DEPLOY` |
| **F4: Graph** | `GET /decision-graph` | 6 columns, 14 nodes, 17 edges | `PASS` | `PENDING CLOUD DEPLOY` |
| **F5: Evidence** | `GET /evidence` | 9 empirical nodes with SHA-256 hashes | `PASS` | `PENDING CLOUD DEPLOY` |
| **F6: Action** | `GET /recommendations` | Prioritized levers + What-If slider | `PASS` | `PENDING CLOUD DEPLOY` |
| **F7: Briefing** | `GET /briefing` | CFO executive briefing narrative | `PASS` | `PENDING CLOUD DEPLOY` |
