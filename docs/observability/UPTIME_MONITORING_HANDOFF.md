# InsightPilot AI — Uptime & External Monitoring Handoff

**Project:** InsightPilot AI  
**Competition:** Accenture Innovation Challenge 2026 (Track 3: BusinessIntelligence.ai)  
**Document:** External Uptime Probes, Synthetic Canary Tests & Monitoring Configuration  
**Status:** `CONFIGURATION READY — EXTERNAL ACTION REQUIRED FOR LIVE MONITORS`

---

## 1. External Monitoring Integration Architecture

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│ EXTERNAL UPTIME MONITOR (e.g., BetterUptime / UptimeRobot / Pingdom)        │
│                                                                             │
│ 1. Liveness Monitor: Pings GET https://[BACKEND_URL]/health every 60s      │
│    -> Expected: HTTP 200 OK {"status": "ok", "service": "insightpilot-api"} │
│                                                                             │
│ 2. Deep Subsystem Monitor: Pings GET https://[BACKEND_URL]/api/v1/demo/readiness│
│    -> Expected: HTTP 200 OK {"submission_ready": true}                     │
│                                                                             │
│ 3. Frontend CDN Monitor: Pings GET https://[FRONTEND_URL]/                 │
│    -> Expected: HTTP 200 OK (Pre-rendered HTML payload)                    │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Monitoring Status & Configuration Matrix

| Monitoring Target | Verification Status | Target Endpoint | Alert Threshold | Recommended Platform |
| :--- | :---: | :--- | :--- | :--- |
| **Backend API Liveness** | `CONFIGURATION READY` | `GET https://[BACKEND_URL]/health` | 2 consecutive failures (&gt;30s) | Render Built-in Healthcheck / UptimeRobot |
| **12-Subsystem Readiness** | `CONFIGURATION READY` | `GET https://[BACKEND_URL]/api/v1/demo/readiness` | 1 failure | BetterUptime / Datadog Synthetic |
| **Frontend Edge CDN** | `CONFIGURATION READY` | `GET https://[FRONTEND_URL]/` | 2 consecutive failures | Vercel Deployment Analytics |
| **AI Provider Telemetry** | `REPOSITORY VERIFIED` | Internal in-memory failover logger | 3 cascaded provider events | Structured log stream |

---

## 3. External Setup Instructions (Project Owner Step-by-Step)

1. Create a free monitor at [BetterUptime](https://betteruptime.com/) or [UptimeRobot](https://uptimerobot.com/).
2. Add Monitor 1:
   - **Type:** HTTP(s)
   - **URL:** `https://[YOUR_RENDER_BACKEND_URL]/health`
   - **Interval:** 1 minute
   - **Keyword Assertion:** `"status":"ok"`
3. Add Monitor 2:
   - **Type:** HTTP(s)
   - **URL:** `https://[YOUR_RENDER_BACKEND_URL]/api/v1/demo/readiness`
   - **Interval:** 5 minutes
   - **Keyword Assertion:** `"submission_ready":true`
4. Add Monitor 3:
   - **Type:** HTTP(s)
   - **URL:** `https://[YOUR_VERCEL_FRONTEND_URL]/`
   - **Interval:** 2 minutes
