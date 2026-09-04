# InsightPilot AI — Deployment Security & Vulnerability Review

**Project:** InsightPilot AI  
**Competition:** Accenture Innovation Challenge 2026 (Track 3: BusinessIntelligence.ai)  
**Document:** Security Perimeter Audit, Threat Model & Secret Protection Review  
**Status:** `SECURITY REVIEW COMPLETE`

---

## 1. Security Review Classification Matrix

| Security Area | Current Status | Finding / Implementation | Action Required |
| :--- | :---: | :--- | :--- |
| **Git Repository Secrets** | `VERIFIED SAFE` | Zero `.env`, `.pem`, `.key`, or `.log` files committed in history. | None. |
| **Hardened Gitignore** | `VERIFIED SAFE` | 66 rules blocking sensitive files, caches, and build artifacts. | None. |
| **Frontend Public Variables** | `VERIFIED SAFE` | Only `NEXT_PUBLIC_API_URL` exposed; zero AI keys in client bundle. | None. |
| **Backend Secret Sanitization** | `VERIFIED SAFE` | API keys stripped from all public response schemas and telemetry logs. | None. |
| **Automated Secret Leakage Tests**| `VERIFIED SAFE` | `test_invariant_10_zero_secret_leakage` passes on every test run. | None. |
| **CORS Middleware Boundary** | `VERIFIED SAFE` | Explicit domain whitelist supported; wildcards disable credentials safely. | Set production domain in cloud settings. |
| **Error Message Sanitization** | `VERIFIED SAFE` | Global exception handlers mask raw database connection strings. | None. |
| **Production HTTPS Enforcement** | `REQUIRES EXTERNAL CONFIG` | HTTPS/TLS 1.3 termination provided by cloud edge (Vercel/Render). | Enable HTTPS on deployment platform. |
| **Cloud Secret Storage** | `REQUIRES EXTERNAL CONFIG` | Cloud platform environment variables (Render/Vercel Secret Store). | Inject live API keys in platform dashboard. |
| **Database Encryption at Rest** | `RECOMMENDED IMPROVEMENT`| SQLite is local unencrypted; PostgreSQL RDS supports AES-256 at rest. | Enable AWS KMS / RDS encryption in production. |

---

## 2. Threat Modeling & Safeguards

### Threat 1: Reverse Engineering Client Bundles for AI API Keys
- **Mitigation:** The frontend makes zero direct calls to Google Gemini or Groq. All generative AI requests are mediated by the backend FastAPI gateway. The client bundle contains zero foundation model credentials.

### Threat 2: Untrusted Cross-Origin Browser Injections (CORS Exploits)
- **Mitigation:** In production, `CORS_ORIGINS` is configured with exact domain strings (e.g. `https://insightpilot.vercel.app`). Unauthorized domains attempting AJAX requests receive HTTP 403 Forbidden.

### Threat 3: Data Exfiltration via Prompt Injection
- **Mitigation:** Prompt context only receives pre-aggregated mathematical summaries and abstracted evidence IDs. Raw customer PII or raw SQL database tables are never passed to the LLM.
