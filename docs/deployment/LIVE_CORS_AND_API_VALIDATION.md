# InsightPilot AI — Live CORS & API Validation Plan

**Project:** InsightPilot AI  
**Competition:** Accenture Innovation Challenge 2026 (Track 3: BusinessIntelligence.ai)  
**Document:** Workstream E — End-to-End CORS Negotiation, Transport Security & API Gateway Validation  
**Status:** `CONFIGURATION VERIFIED — PENDING LIVE CLOUD URLS`

---

## 1. CORS Protocol & Handshake Flow

```text
1. Browser Client (https://[FRONTEND_URL])
   │
   │ Sends Preflight HTTP OPTIONS request
   │ Headers: Origin, Access-Control-Request-Method, Access-Control-Request-Headers
   ▼
2. FastAPI Backend API (https://[BACKEND_URL])
   │
   │ Validates Origin against CORS_ORIGINS whitelist
   │ Returns HTTP 200 with Access-Control-Allow-Origin: https://[FRONTEND_URL]
   ▼
3. Browser Client
   │
   │ Executes actual GET/POST API request
   │ Parses JSON response and updates React state
   ▼
4. User Interface
   │
   │ Renders pre-computed deterministic charts and evidence graphs
```

---

## 2. Live Validation Command Sequence

Once the cloud deployment URLs have been provisioned by the project owner, execute the following validation commands:

### Step 1: Verify Preflight CORS Negotiation
```bash
# Test CORS preflight response
curl -i -X OPTIONS https://[YOUR_BACKEND_URL]/api/v1/kpis \
  -H "Origin: https://[YOUR_FRONTEND_URL]" \
  -H "Access-Control-Request-Method: GET"
# Expected: HTTP 200 OK with Access-Control-Allow-Origin: https://[YOUR_FRONTEND_URL]
```

### Step 2: Verify Backend Liveness & Readiness Probes
```bash
# Probe 1: Root Liveness
curl -i https://[YOUR_BACKEND_URL]/health
# Expected: HTTP 200 OK {"status": "ok", "service": "insightpilot-api", "version": "2.0.0"}

# Probe 2: Subsystem Readiness
curl -i https://[YOUR_BACKEND_URL]/api/v1/demo/readiness
# Expected: HTTP 200 OK {"submission_ready": true, ...}
```

### Step 3: Verify Core Analytical Endpoints
```bash
# Probe 3: Canonical KPI Anomaly
curl -s "https://[YOUR_BACKEND_URL]/api/v1/kpis?region=NA-East" | grep "14200000.05"
# Expected: Returns North America East Revenue record

# Probe 4: 4-Factor Root Cause Decomposition
curl -s "https://[YOUR_BACKEND_URL]/api/v1/investigations/north_america_east_revenue" | grep "Atlanta DC Stockout"
# Expected: Returns 43.2% primary contribution driver

# Probe 5: SHA-256 Evidence Records
curl -s "https://[YOUR_BACKEND_URL]/api/v1/evidence" | grep "EVID_INV_ATL_001"
# Expected: Returns 9 empirical evidence records
```

---

## 3. Validation Status Summary

```text
Localhost Development CORS:
STATUS: LOCAL VERIFIED (Ports 3000, 8080, 5173 whitelisted)

Production Domain Whitelist:
STATUS: CONFIGURATION VERIFIED (Controlled via CORS_ORIGINS environment variable)

Live Cloud Protocol Negotiation:
STATUS: PENDING LIVE URL PROBE (External action required)
```
