# InsightPilot AI — Production Security Architecture

**Project:** InsightPilot AI  
**Competition:** Accenture Innovation Challenge 2026 (Track 3: BusinessIntelligence.ai)  
**Document:** Enterprise Defense-in-Depth, Trust Perimeter & Application Security Architecture  
**Status:** `SECURITY & PERFORMANCE FOUNDATION VERIFIED`

---

## 1. Security Architecture & Foundational Invariant

InsightPilot AI enforces a zero-trust perimeter between deterministic computational truth, browser clients, and third-party foundation models:

> **"Deterministic systems own quantitative truth.  
> LangGraph orchestrates investigation.  
> AI explains grounded facts."**

---

## 2. Multi-Layered Defense-in-Depth Architecture

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│ 1. EDGE & NETWORK SECURITY TIER (Vercel Edge / Cloudflare WAF / Render)     │
│ • HTTPS / TLS 1.3 Transport Encryption                                      │
│ • Edge HTTP Security Headers: nosniff, frame-ancestors, Permissions-Policy │
│ • Next.js Dynamic API Rewrites & Static Bundle Secret Stripping             │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │ HTTPS / JSON with X-Request-ID
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ 2. API GATEWAY SECURITY TIER (FastAPI ASGI Middleware)                      │
│ • SecurityHeadersMiddleware: nosniff, DENY, Referrer-Policy, Cache-Control  │
│ • CORS Whitelist Enforcement (No Wildcard + Credentials Combos)             │
│ • RequestCorrelationMiddleware: Monotonic Latency & Unique X-Request-ID     │
│ • Pydantic v2 Schema Bounds & Payload Type Validation                       │
└──────────────────┬───────────────────────────────────────┬──────────────────┘
                   │                                       │
                   ▼                                       ▼
┌──────────────────────────────────────┐ ┌────────────────────────────────────┐
│ 3. DETERMINISTIC CORE & DATA LAYER   │ │ 4. AI ISOLATION & SAFETY LAYER     │
│ • Zero LLM Arithmetic Privilege      │ │ • Dual-Key In-Memory Rotation      │
│ • Read-Only Relational Schema Access │ │ • 65% Mandatory Abstention Gate    │
│ • SHA-256 Cryptographic Hash Engine  │ │ • Post-Generation Grounding Guard  │
│ • Standardized Error Sanitization    │ │ • Zero Key Exposure in Telemetry   │
└──────────────────────────────────────┘ └────────────────────────────────────┘
```

---

## 3. Trust Boundary Matrix

| Boundary | Interacting Layers | Security Controls Enforced |
| :--- | :--- | :--- |
| **Boundary 1** | Browser $\to$ Next.js Frontend | Static pre-rendering, CSP compatibility, client bundle secret isolation. |
| **Boundary 2** | Next.js Frontend $\to$ FastAPI Backend | Explicit CORS origin whitelist, JSON schema validation, HTTP security headers. |
| **Boundary 3** | FastAPI Backend $\to$ Analytics Core | Direct in-memory Python function execution; SQL injection immune. |
| **Boundary 4** | FastAPI Backend $\to$ External AI APIs | Abstracted prompt context (no raw PII), key rotation, fallback circuit breaker. |

---

## 4. Responsibility Separation

- **Application-Level Responsibilities (Implemented in Repo):**
  - Security headers injection (`SecurityHeadersMiddleware`).
  - Input bounds and type validation via Pydantic v2.
  - Sanitized JSON error responses without stack traces.
  - Zero-secret leakage in client bundles and logs.
- **Infrastructure-Level Responsibilities (Cloud Platform):**
  - TLS certificate provisioning (Let's Encrypt / Vercel SSL).
  - Distributed DDoS mitigation (Cloudflare / AWS Shield).
  - Platform environment secret encryption at rest.
