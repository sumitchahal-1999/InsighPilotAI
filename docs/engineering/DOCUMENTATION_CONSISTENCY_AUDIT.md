# InsightPilot AI — Documentation & Code Consistency Audit

**Project:** InsightPilot AI  
**Competition:** Accenture Innovation Challenge 2026 (Track 3: BusinessIntelligence.ai)  
**Document:** Cross-Document Consistency Matrix, Metric Verification & Path Synchronization  

---

## 📑 1. Cross-Document Consistency Matrix

| Dimension / Metric | Authoritative Repository Truth | Documentation Audit Result | Status |
| :--- | :--- | :--- | :---: |
| **Backend Test Suite** | **265 Tests Passing** (Phase 9.1) / **271 Tests** (Phase 9.2) | Synchronized across `README.md`, `CASE_STUDY.md`, and `RECRUITER_OVERVIEW.md`. | `VERIFIED & SYNCED` |
| **Frontend Static Routes** | **10 Static Routes** (`○ Static`) | Consistently documented across all operations and architecture hubs. | `VERIFIED PARITY` |
| **Enterprise Datasets** | **8 CSV Datasets (43,000+ rows)** | Verified by `tests/validate_dataset.py` (6/6 checks passing). | `VERIFIED PARITY` |
| **Decision Graph Topology** | **14 Nodes, 17 Edges, 6 Columns** | Verified by `analytics/decision_graph_engine.py` and frontend DAG renderer. | `VERIFIED PARITY` |
| **LangGraph Lifecycle** | **11-Node StateGraph** | Verified by `ai/orchestration/state_graph.py` and `/investigation` trace. | `VERIFIED PARITY` |
| **Evidence Records** | **9 Empirical Records (SHA-256)** | Verified by `evidence/evidence_engine.py` with 64-character digests. | `VERIFIED PARITY` |
| **Revenue Anomaly** | **$15,430,000.06 $\to$ $14,200,000.05 (-7.97%)** | 100% numerical match across data, engines, APIs, and UI cards. | `VERIFIED PARITY` |
| **Primary Root Cause** | **Atlanta DC Stockout (43.2% / -$550K)** | 100% numerical match with 94% confidence rating. | `VERIFIED PARITY` |
| **Simulation Elasticity** | **79.4% $\to$ 90% $\to$ +$341,422.91** | $32,209.71 per percentage point elasticity verified in `simulation_engine.py`. | `VERIFIED PARITY` |
| **Priority 1 Recovery** | **+$484,000.00 (14-day SLA)** | Emergency stock transfer action lever confirmed across all screens. | `VERIFIED PARITY` |

---

## 🔍 2. Resolved Documentation Inconsistencies

1. **Test Count Synchronization:** Updated root `README.md` badge from an older `259/259` count to the current verified `265/265 Passing` (and updated to `271/271 Passing` with Phase 9.2).
2. **Package Path References:** Corrected occasional `ai_service/` references in portfolio walkthroughs to match the exact root package directory `ai/`.
3. **Operations Hub Indexing:** Ensured all 25 operations runbooks, audits, and handoff sign-offs are indexed in `docs/operations/README.md`.
