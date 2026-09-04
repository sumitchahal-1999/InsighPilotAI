# InsightPilot AI — Production Operations & Observability Runbook

**Project:** InsightPilot AI  
**Competition:** Accenture Innovation Challenge 2026 (Track 3: BusinessIntelligence.ai)  
**Document:** Operational Procedures, Incident Triage, Log Inspection & Escalation Runbook  
**Status:** `OPERATIONAL RUNBOOK ACTIVE`

---

## 1. Fast Diagnostics & Health Verification

### Procedure 1: Check High-Speed Liveness
```bash
curl -i https://[YOUR_BACKEND_URL]/health
# Expected: HTTP 200 OK {"status": "ok", "service": "insightpilot-api", "version": "2.0.0"}
```

### Procedure 2: Check 12-Subsystem Readiness
```bash
curl -i https://[YOUR_BACKEND_URL]/api/v1/demo/readiness
# Expected: HTTP 200 OK {"submission_ready": true, ...}
```

---

## 2. Common Incident Triage Playbooks

### Playbook A: Investigating Slow API Responses (&gt;2,000 ms)
1. Check `X-Response-Time-Ms` response header on affected endpoint.
2. If slow endpoint is `/api/v1/ai/explain/*`, inspect whether external Groq or Gemini API is experiencing latency spikes.
3. Switch primary provider by setting `AI_PRIMARY_PROVIDER=groq` or temporarily rely on grounded deterministic mode.

### Playbook B: Diagnosing CORS Browser Errors
1. Check browser console for: `Cross-Origin Request Blocked`.
2. Inspect backend environment variable:
   ```bash
   CORS_ORIGINS=https://[YOUR_VERCEL_DOMAIN]
   ```
3. Ensure no trailing slashes are present in `CORS_ORIGINS` (e.g. use `https://app.vercel.app`, not `https://app.vercel.app/`).

### Playbook C: Inspecting Structured Telemetry Logs
Look for structured JSON entries in Render / Docker log stream:
```json
{"timestamp": "2026-08-29 01:40:00", "severity": "INFO", "service": "insightpilot-api", "request_id": "req_8f1a29bc03d1", "method": "GET", "path": "/api/v1/kpis", "status_code": 200, "latency_ms": 12.4}
```

---

## 3. Escalation Severity Matrix

- **Severity 1 (P1) — Critical:** Deterministic calculations fail or API returns 500 on core KPI routes. $\to$ Immediate rollback.
- **Severity 2 (P2) — High:** Upstream AI providers rate-limited; system successfully serving deterministic fallback. $\to$ Monitor pool quotas.
- **Severity 3 (P3) — Low:** Minor UI formatting discrepancy. $\to$ Next sprint patch.
