# InsightPilot AI — Production Health Checks & Readiness Probes

**Project:** InsightPilot AI  
**Competition:** Accenture Innovation Challenge 2026 (Track 3: BusinessIntelligence.ai)  
**Document:** Healthcheck Specifications, Liveness/Readiness Probes & Monitoring Guide  
**Status:** `OPERATIONAL SPECIFICATION`

---

## 1. Healthcheck Endpoints Overview

InsightPilot AI provides two specialized health and readiness endpoints for production load balancers, container orchestrators, and monitoring systems:

| Endpoint Path | Purpose | Overhead / Latency | Target Consumer |
| :--- | :--- | :---: | :--- |
| **`GET /health`** | High-speed liveness check probe. | &lt;1 ms | Kubernetes, AWS ALB, Render, Docker healthcheck. |
| **`GET /api/v1/health`** | Prefixed API gateway liveness check. | &lt;1 ms | API Gateways, reverse proxies, frontend health probes. |
| **`GET /api/v1/demo/readiness`** | Comprehensive 12-subsystem readiness audit. | ~15 ms | Deployment smoke tests, CI/CD pipelines, judge audits. |

---

## 2. Endpoint Specifications

### A. Liveness Probe (`GET /health` & `GET /api/v1/health`)
- **HTTP Method:** `GET`
- **Authentication:** Public (No credentials required)
- **Expected Status Code:** `200 OK`
- **Response Schema (`HealthResponse`):**
  ```json
  {
    "status": "ok",
    "service": "insightpilot-api",
    "version": "2.0.0"
  }
  ```
- **Behavior:** Returns immediately without database queries or external API calls. Used by container orchestrators to detect deadlocks.

---

### B. Dynamic Readiness Probe (`GET /api/v1/demo/readiness`)
- **HTTP Method:** `GET`
- **Authentication:** Public
- **Expected Status Code:** `200 OK`
- **Response Schema (`SubmissionReadinessReport`):**
  ```json
  {
    "submission_ready": true,
    "timestamp": "2026-08-29T01:20:00Z",
    "subsystems": {
      "database_ready": true,
      "analytics_parity": true,
      "driver_engine_ready": true,
      "evidence_engine_ready": true,
      "confidence_engine_ready": true,
      "recommendations_ready": true,
      "simulation_engine_ready": true,
      "ai_router_ready": true,
      "decision_graph_ready": true,
      "integrity_guard_ready": true
    },
    "diagnostics": {
      "database_ready": "Loaded 12322 revenue records from data tier.",
      "analytics_parity": "Canonical revenue variance verified: $-1,230,000.01 (-7.97%)."
    }
  }
  ```


---

## 3. Safe Monitoring & Smoke Testing Usage

1. **Uptime Monitoring:** Configure Pingdom, UptimeRobot, or BetterUptime to ping `GET https://your-api.com/health` every 60 seconds.
2. **Post-Deployment Smoke Test:** Run `curl -f https://your-api.com/api/v1/demo/readiness` immediately after deployment to verify all 12 subsystems before routing traffic.
