# InsightPilot AI — Production CORS & Cross-Origin Validation

**Project:** InsightPilot AI  
**Competition:** Accenture Innovation Challenge 2026 (Track 3: BusinessIntelligence.ai)  
**Document:** Cross-Origin Resource Sharing (CORS) Policy, Whitelist Enforcement & Verification  
**Status:** `STATUS: NOT EXECUTED — LIVE DEPLOYMENT REQUIRED (LOCAL CONFIGURATION VERIFIED)`

---

## 1. Production CORS Policy Architecture

InsightPilot AI enforces a strict origin whitelist via FastAPI's `CORSMiddleware`:

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│ 1. VERCEL FRONTEND (Origin: https://insightpilot-ai.vercel.app)             │
│    • Initiates HTTPS fetch('/api/v1/kpis') with credentials: 'include'       │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ 2. FASTAPI CORS VALIDATION (backend/app/main.py)                            │
│    • Checks Origin against CORS_ORIGINS environment variable array          │
│    • If Matched: Injects 'Access-Control-Allow-Origin: [Origin]'            │
│    • If Unmatched: Omits CORS headers, triggering browser security block    │
│    • Wildcard ('*') is strictly forbidden with allow_credentials=True       │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Cross-Origin Verification Checklist

| Origin Scenario | Header Sent | Expected Server Behavior | Local Test Status | Live Cloud Status |
| :--- | :--- | :--- | :---: | :---: |
| **Whitelisted Vercel** | `Origin: https://[VERCEL_APP]` | Echoes back whitelisted origin in `ACAO` header. | `PASS` | `PENDING CLOUD DEPLOY` |
| **Localhost Dev** | `Origin: http://localhost:3000` | Allows preflight `OPTIONS` and API payloads. | `PASS` | `PASS (Local)` |
| **Unauthorized Origin**| `Origin: https://malicious.com` | Rejects cross-origin access; omits `ACAO`. | `PASS` | `PENDING CLOUD DEPLOY` |
| **Credential Safety** | `Allow-Credentials: true` | Preserves security tokens without wildcard risk. | `PASS` | `PENDING CLOUD DEPLOY` |
