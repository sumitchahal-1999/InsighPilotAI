# InsightPilot AI — API Security & CORS Configuration Audit

**Project:** InsightPilot AI  
**Competition:** Accenture Innovation Challenge 2026 (Track 3: BusinessIntelligence.ai)  
**Document:** API Trust Boundaries, Cross-Origin Resource Sharing (CORS) & Transport Security  
**Status:** `AUDITED & PRODUCTION READY`

---

## 1. CORS Configuration Architecture

Cross-Origin Resource Sharing (CORS) in InsightPilot AI is configured in `backend/app/main.py` and governed by the `CORS_ORIGINS` environment variable in `backend/app/config.py`.

### A. Development Configuration (Default)
```python
# Allowed Origins in Local Development:
CORS_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:8080",
    "http://localhost:5173",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:8080",
    "http://127.0.0.1:5173"
]
```

### B. Production Configuration (Restricted Whitelist)
```bash
# In Production Environment (e.g. Render / Railway / AWS):
CORS_ORIGINS=https://insightpilot.vercel.app,https://insightpilot-ai.com
```

### C. Wildcard vs. Credentials Safety Rule:
FastAPI CORS middleware in `backend/app/main.py` automatically checks whether `*` is present:
```python
cors_origins = settings.CORS_ORIGINS
allow_credentials = "*" not in cors_origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=allow_credentials,
    allow_methods=["*"],
    allow_headers=["*"],
)
```
- When explicit domain origins are specified: `allow_credentials=True`.
- If a wildcard `*` is configured: `allow_credentials=False` to prevent browser security exceptions.

---

## 2. API Endpoint Security & Data Protection

| Security Dimension | Implementation Mechanism | Verification Method |
| :--- | :--- | :--- |
| **Transport Encryption** | Strict HTTPS / TLS 1.3 enforced by cloud edge/load balancer. | Automated SSL certificate checks. |
| **Input Validation** | Pydantic v2 schemas reject malformed request bodies and invalid query parameters. | `tests/api/test_api_endpoints.py`. |
| **Zero Secret Leakage** | Authorization headers and AI provider keys are filtered from API responses. | `test_invariant_10_zero_secret_leakage`. |
| **Error Sanitization** | Global exception handlers mask internal database tracebacks from client responses. | `backend/app/errors.py`. |
| **Rate Limiting Resilience** | Multi-pool AI router cascades on HTTP 429 without dropping user requests. | `tests/e2e/test_provider_failover_flow.py`. |

---

## 3. Production Deployment Security Guidelines

1. **Explicit Allowed Origins:** In production, never set `CORS_ORIGINS=*`. Always specify the exact HTTPS URL of the deployed frontend.
2. **Environment Variable Injection:** Inject `NEXT_PUBLIC_API_URL` into the frontend build environment so API requests target the verified backend domain.
3. **Internal Network Isolation:** For enterprise VPC deployments, place the PostgreSQL database and backend API inside private subnets, exposing only the HTTPS gateway to the public edge.
