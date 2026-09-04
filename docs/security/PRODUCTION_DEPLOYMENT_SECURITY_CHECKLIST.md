# InsightPilot AI — Production Deployment Security Checklist

**Project:** InsightPilot AI  
**Competition:** Accenture Innovation Challenge 2026 (Track 3: BusinessIntelligence.ai)  
**Document:** Operational Security Go-Live & Verification Checklist  
**Status:** `READY FOR DEPLOYMENT AUDIT`

---

## 1. Pre-Deployment Security Checklist

- [x] Zero API keys or secrets committed to Git repository history (`.env.example` uses placeholders).
- [x] Hardened `.gitignore` (66 rules) blocks sensitive extensions (`.env`, `.pem`, `.key`, `.log`).
- [x] Security headers middleware active in FastAPI (`X-Content-Type-Options`, `X-Frame-Options`, `Referrer-Policy`).
- [x] Security headers active in Next.js edge configuration (`frontend/next-app/next.config.mjs`).
- [x] CORS middleware restricts origin access and prevents credential leakage on wildcard origins.
- [x] Standardized error handlers mask Python stack traces and server filepaths from public JSON responses.
- [x] Dynamic `/api/v1/*` routes emit `Cache-Control: no-store` to prevent caching confidential variance data.
- [x] Pydantic v2 schemas enforce strict input bounds on all request parameters.
- [x] Full regression test suite passing: **232 / 232 tests passing**.
- [x] Dataset validation passing: 6 / 6 checks 100% healthy.
- [x] Canonical metrics locked: $15.43M $\to$ $14.20M (-$1.23M), 43.2% Atlanta, 89% confidence, &lt;65% abstention.

---

## 2. Cloud Platform Deployment Tasks (External Action Required)

- [ ] Ensure HTTPS / TLS 1.3 is enabled on both frontend (Vercel) and backend (Render) domains.
- [ ] Configure `CORS_ORIGINS` in Render dashboard with exact Vercel frontend HTTPS domain.
- [ ] Inject live API keys (`GROQ_API_KEY_1`, `GEMINI_API_KEY_1`) in Render secure environment settings.
- [ ] Verify that live `/health` and `/api/v1/demo/readiness` endpoints respond over HTTPS.
