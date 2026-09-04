# InsightPilot AI — Request Validation & Payload Hardening

**Project:** InsightPilot AI  
**Competition:** Accenture Innovation Challenge 2026 (Track 3: BusinessIntelligence.ai)  
**Document:** Input Sanitization, Pydantic Schema Bounds & Payload Defense  
**Status:** `INPUT VALIDATION HARDENED`

---

## 1. Request Validation Model

InsightPilot AI employs strict **Pydantic v2** schema models across all API input vectors (URL path parameters, query parameters, request headers, and JSON request bodies).

---

## 2. Endpoint Validation Master Matrix

| Endpoint | Input Vector | Validation Rule | Invalid Input Behavior |
| :--- | :--- | :--- | :--- |
| **`GET /api/v1/kpis/{kpi_id}`** | Path Parameter | Validated against recognized KPI catalog. | Returns `404 KPI_NOT_FOUND`. |
| **`GET /api/v1/kpis`** | Query (`region`) | Non-empty string constraint (e.g. `NA-East`). | Returns `422 VALIDATION_ERROR`. |
| **`GET /api/v1/evidence/{id}`** | Path Parameter | Regex/lookup validation for `EVID_*` format. | Returns `404 EVIDENCE_NOT_FOUND`. |
| **`POST /api/v1/simulations/run`** | JSON Body | `target_availability_pct` bounded `[0.0, 100.0]`. | Returns `400 BAD_REQUEST`. |
| **`POST /api/v1/ai/explain/{id}`** | JSON Body | `persona` strictly restricted to `['CFO', 'REGIONAL_SALES_MANAGER']`. | Returns `400 INVALID_PERSONA`. |

---

## 3. Malformed JSON & Payload Size Defense

- **Malformed JSON Payloads:** Caught by Starlette JSON parser; returns `422 UNPROCESSABLE_ENTITY` with standardized JSON error message.
- **Large Payload Bounds:** FastAPI request stream limits prevent memory exhaustion from oversized request bodies.
- **SQL Injection Defense:** All analytical queries utilize SQLAlchemy parameter binding or deterministic pandas/in-memory dataframes; zero dynamic string concatenation in SQL.
