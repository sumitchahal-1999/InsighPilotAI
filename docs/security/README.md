# InsightPilot AI — Security & Operational Hardening Hub

**Project:** InsightPilot AI  
**Competition:** Accenture Innovation Challenge 2026 (Track 3: BusinessIntelligence.ai)  
**Directory:** `docs/security/`  
**Status:** `🟢 SECURITY & PERFORMANCE FOUNDATION VERIFIED`

---

## Overview

This directory contains the enterprise security blueprints, HTTP security header specifications, Content Security Policy (CSP) architectures, CORS boundary audits, request validation models, rate-limiting frameworks, performance baselines, threat models, pre-deployment security checklists, and status records for **InsightPilot AI**.

---

## Security Documentation Directory

| # | Document | Purpose & Description |
| :---: | :--- | :--- |
| **1** | **[Production Security Architecture](./PRODUCTION_SECURITY_ARCHITECTURE.md)** | Defense-in-depth model, application vs. infrastructure security, and trust boundaries. |
| **2** | **[HTTP Security Headers](./HTTP_SECURITY_HEADERS.md)** | Specifications for `nosniff`, `DENY`, `Referrer-Policy`, `Permissions-Policy`, and HSTS. |
| **3** | **[Content Security Policy](./CONTENT_SECURITY_POLICY.md)** | CSP directives, edge injection strategy, and Next.js / Tailwind compatibility. |
| **4** | **[CORS & API Security](./CORS_AND_API_SECURITY.md)** | Cross-Origin Resource Sharing rules, origin whitelisting, and transport hardening. |
| **5** | **[Request Validation Hardening](./REQUEST_VALIDATION_HARDENING.md)** | Pydantic v2 schema bounds, input sanitization, and payload size defenses. |
| **6** | **[Rate Limiting & Abuse Resilience](./RATE_LIMITING_AND_ABUSE_RESILIENCE.md)** | Multi-tier rate limiting architecture, AI key rotation, and circuit breaking. |
| **7** | **[Performance Hardening Baseline](./PERFORMANCE_HARDENING_BASELINE.md)** | Measured local test benchmarks, memory optimizations, and sub-50ms latency profiles. |
| **8** | **[Security Threat Model](./SECURITY_THREAT_MODEL.md)** | STRIDE threat modeling, LLM prompt-injection defense, and attack mitigations. |
| **9** | **[Production Deployment Security Checklist](./PRODUCTION_DEPLOYMENT_SECURITY_CHECKLIST.md)** | Pre-deployment operational security verification checklist. |
| **10**| **[Phase 8.4 Security Status](./PHASE_84_SECURITY_STATUS.md)** | Authoritative status record and `SECURITY & PERFORMANCE FOUNDATION VERIFIED` verdict. |

---

## Core Security Invariants

```text
1. Mathematical Truth: Deterministic Python engines calculate 100% of figures.
2. Canonical Metrics: $15.43M -> $14.20M (-$1.23M / -7.97%), 43.2% Atlanta DC, 89% Confidence, <65% Abstention.
3. Secret Isolation: Zero API keys in client bundles, logs, or public error responses.
4. Security Headers: nosniff, DENY, Referrer-Policy, and Cache-Control enforced on all responses.
5. Error Sanitization: Python stack traces and file paths masked from client responses.
```
