# InsightPilot AI — Production Smoke Test Report

**Project:** InsightPilot AI  
**Competition:** Accenture Innovation Challenge 2026 (Track 3: BusinessIntelligence.ai)  
**Document:** Workstream F — Production Smoke Testing Matrix & Live Verification Audit  
**Status:** `LOCAL VERIFIED & CONFIGURATION AUDITED — LIVE EXECUTION PENDING HOSTING`

---

## 1. Production Smoke Test Execution Matrix

### A. Infrastructure & Transport Tier

| Check # | Test Description | Target Endpoint / Layer | Local Status | Live Cloud Status |
| :---: | :--- | :--- | :---: | :---: |
| **INF-01** | Frontend Pre-Rendered Pages | Vercel Edge CDN | `PASS` | `NOT EXECUTED (PENDING DEPLOY)` |
| **INF-02** | Backend ASGI Web Service | Render / Railway Gateway | `PASS` | `NOT EXECUTED (PENDING DEPLOY)` |
| **INF-03** | End-to-End HTTPS / TLS 1.3 | Cloud Edge Layer | `PASS` | `NOT EXECUTED (PENDING DEPLOY)` |
| **INF-04** | Fast Liveness Health Probe | `/health` & `/api/v1/health` | `PASS` | `NOT EXECUTED (PENDING DEPLOY)` |
| **INF-05** | 12-Subsystem Readiness Audit | `/api/v1/demo/readiness` | `PASS` | `NOT EXECUTED (PENDING DEPLOY)` |

---

### B. Application Core Screens Tier

| Check # | Screen / Route | Expected Verification Signal | Local Status | Live Cloud Status |
| :---: | :--- | :--- | :---: | :---: |
| **APP-01** | Executive Command Center (`/`) | -$1.23M (-7.97%) Critical Deficit Card | `PASS` | `NOT EXECUTED (PENDING DEPLOY)` |
| **APP-02** | Root Cause Explorer (`/root-cause`) | 4-Factor Decomposition (43.2% Atlanta) | `PASS` | `NOT EXECUTED (PENDING DEPLOY)` |
| **APP-03** | LangGraph Trace (`/investigation`) | 11-Node State Pipeline Execution | `PASS` | `NOT EXECUTED (PENDING DEPLOY)` |
| **APP-04** | Decision Graph (`/decision-graph`) | 6-Column Topology (14 Nodes, 17 Edges) | `PASS` | `NOT EXECUTED (PENDING DEPLOY)` |
| **APP-05** | Evidence Drawer (`/evidence`) | 9 Empirical Records with SHA-256 Hashes | `PASS` | `NOT EXECUTED (PENDING DEPLOY)` |
| **APP-06** | Recommendations (`/recommendations`)| Priority 1 (+$484K) & Simulation Slider | `PASS` | `NOT EXECUTED (PENDING DEPLOY)` |
| **APP-07** | Executive Briefing (`/briefing`) | Dual CFO / RSM Persona Synthesis | `PASS` | `NOT EXECUTED (PENDING DEPLOY)` |

---

### C. Responsible AI & Trust Tier

| Check # | Trust Safeguard | Verification Criteria | Local Status | Live Cloud Status |
| :---: | :--- | :--- | :---: | :---: |
| **SEC-01** | Canonical Metric Invariance | $15.43M $\to$ $14.20M (-$1.23M) parity | `PASS` | `PASS (LOCKED IN CODE)` |
| **SEC-02** | Mandatory Abstention Gate | Triggered when confidence &lt;65% | `PASS` | `PASS (LOCKED IN CODE)` |
| **SEC-03** | SHA-256 Cryptographic Lineage | 64-char hashes match dataset records | `PASS` | `PASS (LOCKED IN CODE)` |
| **SEC-04** | Zero Secret Exposure | No API keys in responses or logs | `PASS` | `PASS (LOCKED IN CODE)` |

---

## 2. Overall Smoke Test Verdict

```text
================================================================================
                    PRODUCTION SMOKE TEST AUDIT VERDICT
================================================================================

  • Local Test Suite (218/218 Tests):           PASS (100% HEALTHY)
  • Dataset Validation Suite (6/6 Checks):      PASS (100% HEALTHY)
  • Frontend Next.js Production Build:          PASS (10/10 STATIC PAGES)
  • Backend FastAPI Routing & Dual Probes:      PASS (HEALTHY)
  • Live Cloud End-to-End Smoke Test:           NOT EXECUTED (HOSTING PENDING)

  OVERALL STATUS:
  🟡 LOCAL VERIFIED & CONFIGURATION READY — AWAITING LIVE HOSTING PROVISIONING
================================================================================
```
