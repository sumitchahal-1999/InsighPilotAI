# InsightPilot AI — Live Production Security & Privacy Audit

**Project:** InsightPilot AI  
**Competition:** Accenture Innovation Challenge 2026 (Track 3: BusinessIntelligence.ai)  
**Document:** Live Security Audit Checklist, Header Inspection & Zero-Secret Verification  
**Status:** `SECURITY POLICIES VERIFIED — READY FOR LIVE PLATFORM AUDIT`

---

## 1. Live Production Security Audit Matrix

| Security Vector | Audit Protocol | Local Verification Status | Live Cloud Target Status |
| :--- | :--- | :---: | :---: |
| **Zero Secret Leakage** | Scan client bundle JS files for `AIzaSy`, `gsk_`, `.env` tokens. | `VERIFIED SAFE` | `PENDING CLOUD DEPLOY` |
| **HTTP Security Headers**| Inspect headers: `nosniff`, `DENY`, `strict-origin`, `Cache-Control`. | `VERIFIED ACTIVE` | `PENDING CLOUD DEPLOY` |
| **Error Sanitization** | Send malformed requests (`GET /api/v1/kpis/invalid_id`). | `VERIFIED SANITIZED` | `PENDING CLOUD DEPLOY` |
| **CORS Origin Whitelist**| Attempt cross-origin requests from unauthorized origins. | `VERIFIED RESTRICTED`| `PENDING CLOUD DEPLOY` |
| **Pydantic Bounds** | Submit out-of-bounds simulation payloads (`pct: 150.0`). | `VERIFIED REJECTED` | `PENDING CLOUD DEPLOY` |
| **HSTS Enforcement** | Verify `Strict-Transport-Security` header over HTTPS. | `VERIFIED IN PROD` | `PENDING CLOUD DEPLOY` |

---

## 2. Privacy & Secret Defense Verification

1. **Client-Side Build:** Next.js bundler tree-shakes all server-side environment variables, ensuring third-party API keys are never compiled into browser chunks.
2. **Server-Side Logs:** FastAPI structured JSON logger strips all Authorization headers and query tokens before emitting logs.
3. **Public API Errors:** Python stack traces and server filepaths (`c:\Users\...`) are completely masked by `register_error_handlers`.
