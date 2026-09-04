# InsightPilot AI — Production Error Taxonomy

**Project:** InsightPilot AI  
**Competition:** Accenture Innovation Challenge 2026 (Track 3: BusinessIntelligence.ai)  
**Document:** Error Classification, Failure Codes, Client Responses & Escalation Matrix  
**Status:** `STANDARDIZED ERROR SPECIFICATION`

---

## 1. Error Classification Taxonomy

| Error Code | HTTP Status | Detection Signal | User-Facing Message | Retry Policy | Severity |
| :--- | :---: | :--- | :--- | :---: | :---: |
| **`CLIENT_ERROR`** | `400` | Malformed URL parameters or unsupported query strings. | "Invalid request parameters provided." | Do not retry without modifying request. | Low |
| **`VALIDATION_ERROR`** | `422` | Request body fails Pydantic schema validation. | "The incoming request failed validation constraints." | Do not retry without schema fix. | Low |
| **`NOT_FOUND`** | `404` | Unknown KPI identifier or missing evidence node ID. | "Requested entity was not found in the verified repository." | Do not retry. | Low |
| **`ANALYTICS_ERROR`** | `422` | Out-of-bounds simulation input or division by zero. | "Mathematical bounds exception during scenario evaluation." | Retry with valid range. | Medium |
| **`DATA_ERROR`** | `500` | Missing CSV file or referential integrity mismatch. | "Internal dataset access error." | Immediate engineer alert. | High |
| **`DEPENDENCY_ERROR`** | `503` | Database connection pool timeout. | "Database service temporarily unavailable." | Retry with exponential backoff. | High |
| **`AI_PROVIDER_ERROR`** | Handled | Rate limit (429) or authentication failure on LLM pool. | Transparently masked; fallback served. | Automatic internal pool failover. | Low |
| **`TIMEOUT`** | `504` | External HTTP call exceeds 30s SLA. | "Upstream request timed out." | Single retry before fallback. | Medium |
| **`INTERNAL_ERROR`** | `500` | Unhandled Python runtime exception. | "An unexpected internal server error occurred." | Engineer review required. | Critical |

---

## 2. Standardized Error Response Schema

All error responses adhere to the typed `ErrorResponse` schema:

```json
{
  "error": {
    "code": "KPI_NOT_FOUND",
    "message": "KPI with identifier 'invalid_kpi_id' is not recognized or supported by the analytics engine."
  }
}
```

### Security Rule:
- Internal Python stack traces, absolute filesystem paths (`c:\Users\...`), and database connection credentials are **NEVER** returned in the JSON error payload.
