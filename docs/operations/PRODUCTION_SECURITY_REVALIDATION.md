# InsightPilot AI — Production Security Revalidation

**Project:** InsightPilot AI  
**Competition:** Accenture Innovation Challenge 2026 (Track 3: BusinessIntelligence.ai)  
**Document:** Security Control Revalidation, Header Auditing & Boundary Verification  
**Status:** `SECURITY REVALIDATION PASSED`

---

## 1. Security Controls Verification Audit

| Security Control | Implementation Mechanism | Revalidation Check | Status |
| :--- | :--- | :--- | :---: |
| **`nosniff` Header** | `SecurityHeadersMiddleware` | Header `X-Content-Type-Options: nosniff` on all responses. | `VERIFIED ACTIVE` |
| **`DENY` Frame Header** | `SecurityHeadersMiddleware` | Header `X-Frame-Options: DENY` on all responses. | `VERIFIED ACTIVE` |
| **`Referrer-Policy`** | `SecurityHeadersMiddleware` | Header `Referrer-Policy: strict-origin-when-cross-origin`. | `VERIFIED ACTIVE` |
| **`Permissions-Policy`**| `SecurityHeadersMiddleware` | Header `Permissions-Policy: geolocation=(), camera=(), microphone=()`.| `VERIFIED ACTIVE` |
| **`Cache-Control`** | `SecurityHeadersMiddleware` | Header `Cache-Control: no-store, no-cache` on `/api/v1/*`. | `VERIFIED ACTIVE` |
| **Input Validation** | Pydantic v2 Schemas | Out-of-bounds parameters rejected with HTTP 400/422. | `VERIFIED ACTIVE` |
| **Error Sanitization** | `register_error_handlers` | Zero Python tracebacks or `c:\Users` paths leaked. | `VERIFIED ACTIVE` |
| **Secret Isolation** | Next.js Build Stripping | Zero API keys present in client bundle or logs. | `VERIFIED ACTIVE` |
| **CORS Guard** | `CORSMiddleware` | Explicit whitelist; wildcard origins disable credentials. | `VERIFIED ACTIVE` |

---

## 2. Environment Configuration Boundaries

- **Dynamic Backend Target:** Frontend `frontend/next-app/lib/api.ts` uses `process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000"`.
- **Zero Localhost Assumption in Production:** When deployed to Vercel, `NEXT_PUBLIC_API_URL` is set to the live Render backend URL, ensuring seamless cloud communication.
