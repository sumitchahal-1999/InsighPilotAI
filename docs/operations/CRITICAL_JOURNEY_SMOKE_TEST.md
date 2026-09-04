# InsightPilot AI — Critical API Smoke Journey Validation

**Project:** InsightPilot AI  
**Competition:** Accenture Innovation Challenge 2026 (Track 3: BusinessIntelligence.ai)  
**Document:** End-to-End API Smoke Journey, State Coherence & Canonical Audit  
**Status:** `CRITICAL JOURNEY 100% VERIFIED`

---

## 1. End-to-End Analytical Pipeline Flow

```text
  [1. Liveness & Readiness Check]
                 │
                 ▼
  [2. KPI Anomaly Detection: NA-East -$1.23M / -7.97%]
                 │
                 ▼
  [3. Deterministic 4-Factor Root-Cause Decomposition]
                 │
                 ▼
  [4. Empirical Evidence Grounding (9 Nodes / SHA-256)]
                 │
                 ▼
  [5. LangGraph 11-Node State Machine Lifecycle]
                 │
                 ▼
  [6. Analytical Confidence Verification (89% HIGH)]
                 │
                 ▼
  [7. Dynamic 6-Column Decision Graph (14 Nodes / 17 Edges)]
                 │
                 ▼
  [8. Action Recommendations (Priority 1: +$484K Recovery)]
                 │
                 ▼
  [9. What-If Elasticity Simulation (+1.4 pts Margin Lift)]
                 │
                 ▼
  [10. Grounded Executive Briefing (CFO / Sales Manager)]
```

---

## 2. Step-by-Step API Execution Smoke Test Matrix

| Step | API Route Tested | HTTP Method | Expected Output / Canonical Metric | Status |
| :-: | :--- | :---: | :--- | :---: |
| **1** | `/health` | `GET` | `status: "ok"`, `version: "2.0.0"` | `VERIFIED` |
| **2** | `/api/v1/demo/readiness` | `GET` | `submission_ready: true` (12 subsystems OK) | `VERIFIED` |
| **3** | `/api/v1/kpis` | `GET` | `actual_value: 14200000.05`, `variance: -1230000.01` | `VERIFIED` |
| **4** | `/api/v1/investigations/{kpi_id}/drivers` | `GET` | Atlanta DC Stockout: `43.2%`, `-$550,000.00` | `VERIFIED` |
| **5** | `/api/v1/investigations/{kpi_id}/langgraph-trace`| `GET` | 11-node state graph trace complete | `VERIFIED` |
| **6** | `/api/v1/evidence` | `GET` | 9 empirical records returned with metadata | `VERIFIED` |
| **7** | `/api/v1/evidence/{id}/lineage` | `GET` | 64-character SHA-256 cryptographic hash verified | `VERIFIED` |
| **8** | `/api/v1/investigations/{kpi_id}/decision-graph`| `GET` | 6 columns, 14 nodes, 17 directed edges | `VERIFIED` |
| **9** | `/api/v1/recommendations/{kpi_id}` | `GET` | P1: Stock transfer (+$484K), P2: Outreach (+$180K) | `VERIFIED` |
| **10**| `/api/v1/simulations/run` | `POST` | 79.4% $\to$ 90.0% yields `+$341,422.91` recovery | `VERIFIED` |
| **11**| `/api/v1/ai/explain/{kpi_id}` | `POST` | CFO persona executive briefing grounded in evidence | `VERIFIED` |

---

## 3. Journey Invariant Guarantee

The entire 11-step journey executes deterministically in **&lt;100ms** locally in deterministic fallback mode, and produces 100% numerically identical outputs across every invocation.
