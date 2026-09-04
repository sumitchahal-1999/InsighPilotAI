# InsightPilot AI — Backend API Service

> **Accenture Innovation Challenge 2026 — Track 3: BusinessIntelligence.ai**  
> **Framework:** FastAPI  
> **Role:** REST API layer exposing deterministic KPI analytics, driver ranking, and evidence lineage.

---

## 1. Purpose & Architecture

The InsightPilot AI backend exposes the deterministic business logic and cryptographic evidence graph through clean, versioned REST endpoints (`/api/v1`). It serves as the bridge between the underlying analytical engines and the future executive UI.

```
                  ┌──────────────────────┐
                  │     Stitch UI        │
                  └──────────┬───────────┘
                             │
                             ↓
                     REST API / FastAPI (/api/v1)
                             │
              ┌──────────────┼──────────────┐
              ↓              ↓              ↓
          KPIService   InvestigationService EvidenceService
              │              │              │
              ↓              ↓              ↓
          KPIEngine     DriverEngine    EvidenceEngine
              │              │              │
              └──────────────┼──────────────┘
                             ↓
                    Raw Enterprise Data (data/raw/)
```

---

## 2. Installation & Setup

Ensure the Python environment dependencies are installed:
```bash
pip install -r requirements.txt
```

---

## 3. Running Locally

Start the development server with hot-reload enabled:
```bash
uvicorn backend.app.main:app --reload --host 127.0.0.1 --port 8000
```

Once running, interactive API documentation is available at:
- **Swagger UI:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc:** [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)
- **OpenAPI Schema:** [http://127.0.0.1:8000/openapi.json](http://127.0.0.1:8000/openapi.json)

---

## 4. Key Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/health` | Liveness and health check probe |
| `GET` | `/api/v1/kpis` | List all calculated KPI states across 5 core metrics |
| `GET` | `/api/v1/kpis/{kpi_id}` | Get calculated state, variance, and materiality for a KPI |
| `GET` | `/api/v1/investigations/{kpi_id}` | Run full deterministic root cause investigation |
| `GET` | `/api/v1/investigations/{kpi_id}/drivers` | Get ranked explanatory drivers with normalized contributions |
| `GET` | `/api/v1/investigations/{kpi_id}/evidence` | Get all verified evidence nodes supporting the investigation |
| `GET` | `/api/v1/evidence/{evidence_id}` | Get single verified evidence item |
| `GET` | `/api/v1/evidence/{evidence_id}/lineage` | Get 5-layer cryptographic lineage trace |

---

## 5. Running Tests

Execute the backend API test suite:
```bash
python -m unittest discover -s tests/api -p "test_*.py" -v
```

Full project test suite:
```bash
python -m unittest discover -s tests/analytics -p "test_*.py"
python -m unittest discover -s tests/evidence -p "test_*.py"
python -m unittest discover -s tests/api -p "test_*.py"
```

---

## 6. Detailed API Documentation

Comprehensive endpoint schemas, error response formats, and CORS configurations are documented in:
[docs/api/API.md](file:///c:/Users/hp/Downloads/New%20folder%20(11)/docs/api/API.md)
