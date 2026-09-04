# InsightPilot AI — Operations, Deployment & Production Handoff Hub

**Project:** InsightPilot AI  
**Competition:** Accenture Innovation Challenge 2026 (Track 3: BusinessIntelligence.ai)  
**Directory:** `docs/operations/`  
**Status:** `🟡 CONDITIONAL GO — REPOSITORY & LOCAL READINESS VERIFIED`

---

## Overview

This directory contains the complete operational runbooks, cloud provisioning guides, health validations, smoke testing protocols, security audits, risk registers, and authoritative handoff sign-offs for **InsightPilot AI**.

---

## Operations & Cloud Deployment Directory

| # | Document | Purpose & Description |
| :---: | :--- | :--- |
| **1** | **[Live Cloud Deployment Execution](./LIVE_CLOUD_DEPLOYMENT_EXECUTION.md)** | Real-time audit of cloud provisioning attempts across Render and Vercel. |
| **2** | **[Live Backend Validation Report](./LIVE_BACKEND_VALIDATION_REPORT.md)** | Backend cloud health, readiness, and API validation report. |
| **3** | **[Live Frontend Validation Report](./LIVE_FRONTEND_VALIDATION_REPORT.md)** | Frontend cloud route inspection, static asset verification, and hydration report. |
| **4** | **[Live 7-Screen Journey Report](./LIVE_7_SCREEN_JOURNEY_REPORT.md)** | End-to-end 7-screen competition user journey audit and verification. |
| **5** | **[Production CORS Validation](./PRODUCTION_CORS_VALIDATION.md)** | Cross-origin resource sharing policy, whitelist verification, and credential rules. |
| **6** | **[Live Security Verification Report](./LIVE_SECURITY_VERIFICATION_REPORT.md)** | Security header inspection, secret defense, and error sanitization audit. |
| **7** | **[Live Degraded Mode Validation](./LIVE_DEGRADED_MODE_VALIDATION.md)** | Fault-tolerant fallback verification and AI outage survivability. |
| **8** | **[Phase 8.7 Live Go-Live Decision](./PHASE_87_LIVE_GO_LIVE_DECISION.md)** | Authoritative Phase 8.7 go-live verdict and operational status. |
| **9** | **[Render Deployment Runbook](./RENDER_DEPLOYMENT_RUNBOOK.md)** | Step-by-step instructions for deploying the FastAPI backend to Render Web Services. |
| **10**| **[Vercel Deployment Runbook](./VERCEL_DEPLOYMENT_RUNBOOK.md)** | Step-by-step instructions for deploying the Next.js frontend to the Vercel Edge Network. |
| **11**| **[Live Production Smoke Test](./LIVE_PRODUCTION_SMOKE_TEST.md)** | Verification protocol for live cloud URLs across backend, frontend, and API endpoints. |
| **12**| **[Live Production Journey Validation](./LIVE_PRODUCTION_JOURNEY_VALIDATION.md)** | End-to-end 7-screen competition user journey validation protocol. |
| **13**| **[Live Production Security Audit](./LIVE_PRODUCTION_SECURITY_AUDIT.md)** | Security checklist for live cloud environments (headers, secrets, error sanitization). |
| **14**| **[Production URL Registry](./PRODUCTION_URL_REGISTRY.md)** | Authoritative registry tracking local and cloud URLs (`VERIFIED` vs `PENDING`). |
| **15**| **[Final Production Handoff](./FINAL_PRODUCTION_HANDOFF.md)** | Authoritative handoff sign-off with categorized verification statuses and remaining actions. |
| **16**| **[Environment Readiness Audit](./ENVIRONMENT_READINESS_AUDIT.md)** | Master taxonomy of environment variables, secret boundaries, and configuration rules. |
| **17**| **[Clean-Start Smoke Test](./CLEAN_START_SMOKE_TEST.md)** | Local clean checkout validation, dependency verification, and startup smoke test log. |
| **18**| **[Health & Readiness Validation](./HEALTH_AND_READINESS_VALIDATION.md)** | Liveness vs. 12-subsystem deep readiness probe verification and SLA benchmarks. |
| **19**| **[Critical Journey Smoke Test](./CRITICAL_JOURNEY_SMOKE_TEST.md)** | Step-by-step 11-stage API smoke journey covering end-to-end analytical pipeline. |
| **20**| **[Degraded Mode & Failure Handling](./DEGRADED_MODE_AND_FAILURE_HANDLING.md)** | Fault injection testing across AI outages, bad payloads, and graceful fallbacks. |
| **21**| **[Production Security Revalidation](./PRODUCTION_SECURITY_REVALIDATION.md)** | Revalidation of HTTP security headers, CORS restrictions, and zero secret leakage. |
| **22**| **[Frontend Production Smoke Test](./FRONTEND_PRODUCTION_SMOKE_TEST.md)** | Next.js 14 static build audit, 7 core screens verification, and client bundle inspection. |
| **23**| **[Deployment Handoff Runbook](./DEPLOYMENT_HANDOFF_RUNBOOK.md)** | Cloud deployment procedures for Render/Vercel, operational boundaries, and rollbacks. |
| **24**| **[Go-Live Risk Register](./GO_LIVE_RISK_REGISTER.md)** | Comprehensive risk assessment matrix with owners, mitigations, and current statuses. |
| **25**| **[Phase 8.5 Go-Live Readiness Sign-Off](./PHASE_85_GO_LIVE_READINESS_SIGN_OFF.md)** | Operational sign-off record and readiness evaluation. |

---

## Core Operations Invariants

```text
1. Mathematical Truth: Deterministic Python engines calculate 100% of figures.
2. Canonical Metrics: $15.43M -> $14.20M (-$1.23M / -7.97%), 43.2% Atlanta DC, 89% Confidence, <65% Abstention.
3. Secret Isolation: Zero API keys in client bundles, logs, or error responses.
4. Clean Startup: Application operates out-of-the-box in deterministic mode without external APIs.
5. Absolute Truthfulness: Local readiness is never confused with completed public cloud deployment.
```
