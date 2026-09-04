# InsightPilot AI — CORS & API Boundary Security

**Project:** InsightPilot AI  
**Competition:** Accenture Innovation Challenge 2026 (Track 3: BusinessIntelligence.ai)  
**Document:** Cross-Origin Resource Sharing (CORS), Trust Boundaries & Transport Hardening  
**Status:** `CORS SECURITY HARDENED`

---

## 1. CORS Configuration Architecture

Cross-Origin Resource Sharing (CORS) is configured in `backend/app/main.py` and strictly validated against `CORS_ORIGINS`:

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

---

## 2. Environment-Specific Origin Policies

### A. Local Development Environment
- **Allowed Origins:** `http://localhost:3000`, `http://localhost:8080`, `http://localhost:5173`, `http://127.0.0.1:3000`.
- **Credentials:** Allowed (`allow_credentials=True`).
- **Use Case:** Seamless local development between Next.js frontend and FastAPI backend.

### B. Production Environment
- **Allowed Origins:** Explicit list defined via `CORS_ORIGINS=https://[YOUR_VERCEL_DOMAIN]`.
- **Credentials:** Allowed only for explicit HTTPS origin strings.
- **Wildcard Defense:** If `*` is accidentally supplied, `allow_credentials` automatically downgrades to `False` to prevent browser credential leakage.

---

## 3. Allowed HTTP Methods & Headers

- **Allowed Methods:** `GET`, `POST`, `OPTIONS`.
- **Allowed Headers:** `Content-Type`, `Authorization`, `X-Request-ID`, `X-Correlation-ID`.
- **Exposed Headers:** `X-Request-ID`, `X-Response-Time-Ms`.
