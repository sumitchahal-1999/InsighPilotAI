# InsightPilot AI — Observability & Reliability Operations Hub

**Project:** InsightPilot AI  
**Competition:** Accenture Innovation Challenge 2026 (Track 3: BusinessIntelligence.ai)  
**Directory:** `docs/observability/`  
**Status:** `🟢 OBSERVABILITY FOUNDATION VERIFIED`

---

## Overview

This directory contains the production observability architecture, health probe semantics, standardized error taxonomy, latency baselines, failure mode and effects analysis (FMEA), rate-limiting audits, external uptime monitoring handoff guides, security policies, operations runbooks, and status records for **InsightPilot AI**.

---

## Observability Documentation Directory

| # | Document | Purpose & Description |
| :---: | :--- | :--- |
| **1** | **[Production Observability Architecture](./PRODUCTION_OBSERVABILITY_ARCHITECTURE.md)** | Telemetry architecture, request tracing, structured logging, and observability boundaries. |
| **2** | **[Health & Readiness Model](./HEALTH_AND_READINESS_MODEL.md)** | Liveness vs. readiness semantics, health probe SLA (&lt;1ms), and degradation hierarchy. |
| **3** | **[Production Error Taxonomy](./PRODUCTION_ERROR_TAXONOMY.md)** | Standardized error codes (`CLIENT_ERROR`, `ANALYTICS_ERROR`, etc.) and response formats. |
| **4** | **[Latency & Performance Baseline](./LATENCY_AND_PERFORMANCE_BASELINE.md)** | Measured local test benchmarks, endpoint latency profiles, and timing breakdowns. |
| **5** | **[Reliability & Failure Mode Audit](./RELIABILITY_FAILURE_MODE_AUDIT.md)** | 12-scenario Failure Mode and Effects Analysis (FMEA) and multi-tier recovery chains. |
| **6** | **[Rate Limit & Resilience Audit](./RATE_LIMIT_AND_RESILIENCE_AUDIT.md)** | Request timeout policies (30s), AI key pool rotation, and circuit breaking analysis. |
| **7** | **[Uptime Monitoring Handoff](./UPTIME_MONITORING_HANDOFF.md)** | External synthetic uptime probe setup (BetterUptime / UptimeRobot / Pingdom). |
| **8** | **[Observability Security Policy](./OBSERVABILITY_SECURITY_POLICY.md)** | Telemetry privacy rules, secret redaction standards, and traceback masking. |
| **9** | **[Production Operations Runbook](./PRODUCTION_OPERATIONS_RUNBOOK.md)** | Incident triage playbooks, slow response diagnostics, and escalation procedures. |
| **10**| **[Phase 8.3 Observability Status](./PHASE_83_OBSERVABILITY_STATUS.md)** | Authoritative status record and `OBSERVABILITY FOUNDATION VERIFIED` verdict. |

---

## Core Operational Invariants

```text
1. Mathematical Truth: Deterministic Python engines calculate 100% of figures.
2. Canonical Metrics: $15.43M -> $14.20M (-$1.23M / -7.97%), 43.2% Atlanta DC, 89% Confidence, <65% Abstention.
3. Secret Isolation: Zero API keys in logs, telemetry payloads, or public error responses.
4. Request Tracing: Every request emits X-Request-ID and X-Response-Time-Ms.
5. High Availability: System serves 100% accurate grounded analysis even during total third-party AI outages.
```
