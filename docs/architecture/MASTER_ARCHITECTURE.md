# InsightPilot AI — Master Architecture Specification

**Accenture Innovation Challenge 2026 — Track 3: BusinessIntelligence.ai**  
*Enterprise Root-Cause Intelligence, Cryptographic Evidence Lineage, and Agentic Decision Orchestration*

---

## 1. Executive Summary & Core Philosophy

Modern enterprise business intelligence suffers from a fundamental paradox:
* **Traditional Dashboards (PowerBI, Tableau):** Highly accurate at describing **what** happened (historical aggregation), but completely silent on **why** it happened and **what to do next**.
* **Generic GenAI Chatbots (ChatGPT, Copilot):** Capable of generating plausible narrative summaries, but prone to **hallucinating quantitative figures**, inventing non-existent causes, and lacking verifiable audit trails.

**InsightPilot AI** resolves this dilemma through a strict, defensible architectural principle:

> ### 🛡️ Foundational Architectural Invariant
> **"Deterministic systems own quantitative truth. LangGraph orchestrates investigation. AI explains grounded facts."**

Under this invariant, Large Language Models (LLMs) are **strictly forbidden** from calculating revenue, variance, driver contributions, ranking causal factors, inventing evidence IDs, modifying recovery projections, or generating speculative actions when analytical confidence is low.

```
                    INSIGHTPILOT AI
                          │
                          ▼
                  KPI ANOMALY DETECTED
                          │
                          ▼
               DETERMINISTIC INVESTIGATION
                          │
          ┌───────────────┼────────────────┐
          ▼               ▼                ▼
      KPI Movement      Drivers          Evidence
          │               │                │
          └───────────────┼────────────────┘
                          ▼
                 CONFIDENCE ENGINE
                          │
                 ┌────────┴────────┐
                 │                 │
             CONFIDENT          ABSTAIN
                 │                 │
                 ▼                 ▼
        LANGGRAPH ORCHESTRATION   SAFE RESPONSE
                 │
                 ▼
       GEMINI + GROQ AI ROUTING
                 │
                 ▼
          GROUNDED EXPLANATION
                 │
                 ▼
            DECISION GRAPH
                 │
                 ▼
        RECOMMENDATION ENGINE
                 │
                 ▼
          WHAT-IF SIMULATION
                 │
                 ▼
         EXECUTIVE DECISION BRIEF
```

---

## 2. Canonical Invariant Truth Table

The system operates across a locked, mathematically reconciled canonical enterprise scenario:

| Dimension / Metric | Canonical Invariant Value | System Authority | Verification Hash / Status |
| :--- | :--- | :--- | :--- |
| **Target KPI** | North America East Revenue (`north_america_east_revenue`) | Master Dimension | ✅ Verified |
| **Baseline Period (2026-Q2)** | `$15,430,000.06` | ERP Data Tier (`revenue.csv`) | ✅ Deterministic |
| **Target Period (2026-Q3)** | `$14,200,000.05` | ERP Data Tier (`revenue.csv`) | ✅ Deterministic |
| **Net Variance Amount** | `-$1,230,000.01` | KPI Engine (`kpi_engine.py`) | ✅ Deterministic |
| **Percentage Change** | `-7.97%` (`CRITICAL_NEGATIVE_VARIANCE`) | KPI Engine (`kpi_engine.py`) | ✅ Deterministic |
| **Top Causal Driver** | Atlanta DC Stockout (`atlanta_dc_stockout`) | Driver Engine (`driver_engine.py`) | ✅ Deterministic |
| **Driver 1 Contribution** | `43.2%` (`-$550,000.00` impact / `94%` confidence) | Driver Engine (`driver_engine.py`) | ✅ Deterministic |
| **Driver 2 Contribution** | Horizon Foods Price War (`26.1%` / `-$332,000.00`) | Driver Engine (`driver_engine.py`) | ✅ Deterministic |
| **Driver 3 Contribution** | Distributor Order Deferrals (`18.4%` / `-$234,000.00`)| Driver Engine (`driver_engine.py`) | ✅ Deterministic |
| **Driver 4 Contribution** | SKU Mix Shift (`12.3%` / `-$156,000.00`) | Driver Engine (`driver_engine.py`) | ✅ Deterministic |
| **Total Attributed Sum** | `100.0%` (`-$1,272,000.00` unconstrained impact) | Economic Reconciliation Layer | ✅ Mathematically Normalized |
| **Investigation Confidence**| `89%` (`HIGH` tier, `abstention: false`) | Confidence Engine (`confidence_engine.py`) | ✅ 6-Factor Model |
| **Decision Graph Topology** | 6 Columns, 14 Nodes, 17 Edges | Decision Graph Engine | ✅ Dynamic Deterministic |
| **Priority 1 Action Lever** | Charlotte $\to$ Atlanta 20,000-unit transfer (`+$484K`) | Recommendation Engine | ✅ Grounded Lever |
| **What-If Simulation** | 79.4% $\to$ 90.0% Availability yields `+$341,422.91` | Simulation Engine (`simulation_engine.py`) | ✅ Float Invariant |

---

## 3. Five-Layer System Architecture

InsightPilot AI is organized into 5 modular, decoupled, and testable tiers:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    5. DYNAMIC PRESENTATION & CONSUMPTION LAYER              │
│   Next.js 14 (App Router) • 7 Executive Screens • FastAPI REST Gateway      │
└──────────────────────────────────────▲──────────────────────────────────────┘
                                       │
┌──────────────────────────────────────┴──────────────────────────────────────┐
│                  4. CAPABILITY-AWARE AI & SAFETY GUARD LAYER                │
│   Multi-Pool Router (Groq/Gemini) • Grounding Validator • Abstention Gate   │
└──────────────────────────────────────▲──────────────────────────────────────┘
                                       │
┌──────────────────────────────────────┴──────────────────────────────────────┐
│                    3. AGENTIC ORCHESTRATION PIPELINE LAYER                  │
│   LangGraph 11-Node StateGraph • Replay Lifecycle • Telemetry Observer     │
└──────────────────────────────────────▲──────────────────────────────────────┘
                                       │
┌──────────────────────────────────────┴──────────────────────────────────────┐
│                  2. DETERMINISTIC ANALYTICS & INFERENCE LAYER               │
│   KPI Engine • Driver Engine • Evidence Engine • Confidence • Simulation     │
└──────────────────────────────────────▲──────────────────────────────────────┘
                                       │
┌──────────────────────────────────────┴──────────────────────────────────────┐
│                     1. ENTERPRISE DATA & TELEMETRY LAYER                    │
│   PostgreSQL / CSV Tier • 8 Validated Schemas • SHA-256 Lineage Generator   │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

### Layer 1: Enterprise Data & Telemetry Ingestion Layer
* **Data Sources (8 Enterprise CSV / PostgreSQL Entities):**
  1. `revenue.csv` (12,322 invoices across 5 regions and 4 quarters).
  2. `inventory.csv` (13,710 warehouse snapshot logs tracking stock availability).
  3. `sales.csv` (12,344 granular transaction items).
  4. `margin.csv` (75 quarterly margin reconciliation records).
  5. `distributor_orders.csv` (1,640 purchase order fulfillment records).
  6. `support_tickets.csv` (2,856 customer service escalations).
  7. `distributor_communications.csv` (39 executive emails / EDI notes).
  8. `market_intelligence.csv` (12 competitive pricing observation reports).
* **Integrity Enforcement:**
  - Strict JSON schema validation per entity (`data/schemas/entities/*.json`).
  - Cross-dataset referential integrity across SKUs (`SKU-8821`), Facilities (`FAC-ATL-01`), and Distributors (`DIST-SE-001`).
  - Cryptographic Lineage: Every ingested fact is hashed using SHA-256 (`sha256:...`) to guarantee zero data tampering.

---

### Layer 2: Deterministic Analytics & Inference Layer
* **KPI Engine ([`analytics/kpi_engine.py`](../../analytics/kpi_engine.py)):**
  - Computes period-over-period variance: $\Delta V = V_{curr} - V_{prev}$.
  - Materiality classification: Flags $\le -3.0\%$ as `CRITICAL_NEGATIVE_VARIANCE`.
* **Driver Engine ([`analytics/driver_engine.py`](../../analytics/driver_engine.py)):**
  - Performs multi-factor variance decomposition across 4 independent causal dimensions.
  - Normalizes raw unconstrained impact ($1.272M) to exact 100.0% variance allocation.
* **Evidence Engine ([`evidence/evidence_engine.py`](../../evidence/evidence_engine.py)):**
  - Retrieves empirical corroboration across ERP, CRM, Support, and Market Intel.
  - Calculates evidence ranking score $R = 0.40 \cdot \text{Relevance} + 0.35 \cdot \text{Reliability} + 0.25 \cdot \text{LineageQuality}$.
* **Confidence Engine ([`analytics/confidence_engine.py`](../../analytics/confidence_engine.py)):**
  - Deterministic 6-Factor Multi-Factor Confidence Scoring Model:
    $$\text{Score} = 0.25 \cdot \text{Sufficiency} + 0.20 \cdot \text{Quality} + 0.20 \cdot \text{DriverCoverage} + 0.15 \cdot \text{Corroboration} + 0.10 \cdot \text{Lineage} + 0.10 \cdot \text{Consistency}$$
  - Canonical calculation yields **89% (HIGH)**.
  - Mandatory Abstention Rule: If $\text{Score} < 65\%$, system activates `abstention_node` and suppresses generative LLM invocation.
* **Recommendation Engine ([`analytics/recommendations.py`](../../analytics/recommendations.py)):**
  - Generates 4 prioritized, actionable intervention levers with estimated recovery amounts ($484K, $180K, $238K, $93.6K).
* **Simulation Engine ([`simulation/simulation_engine.py`](../../simulation/simulation_engine.py)):**
  - Sandbox what-if model calculating revenue and gross margin recovery from parameter modifications (e.g. 79.4% $\to$ 90.0% inventory availability yields +$341,422.91).

---

### Layer 3: Agentic Orchestration Layer (LangGraph)
* **11-Node LangGraph State Pipeline ([`ai/langgraph/graph.py`](../../ai/langgraph/graph.py)):**
  1. `load_kpi_node` (DETERMINISTIC): Ingests baseline and comparison period records.
  2. `calculate_movement_node` (DETERMINISTIC): Calculates exact numerical movement and threshold materiality.
  3. `identify_drivers_node` (DETERMINISTIC): Decomposes variance into 4 normalized causal drivers.
  4. `retrieve_evidence_node` (DETERMINISTIC): Gathers empirical records from ERP, CRM, and Zendesk.
  5. `validate_evidence_node` (SAFETY_GUARD): Validates SHA-256 digests and cross-source corroboration.
  6. `calculate_confidence_node` (SAFETY_GUARD): Computes 6-factor analytical confidence score.
  7. `confidence_router` (CONDITIONAL_EDGE): Directs to `abstention_node` if score $< 65\%$, else proceeds to `prepare_grounding_node`.
  8. `prepare_grounding_node` (DETERMINISTIC): Constructs immutable context container forbidding hallucinated IDs.
  9. `route_ai_capability_node` (ORCHESTRATION): Selects optimal model based on task requirements.
  10. `ai_invocation_node` (AI_ORCHESTRATION): Calls provider pool with automatic failover and grounding checks.
  11. `executive_synthesis_node` (AI/DETERMINISTIC): Synthesizes persona-specific briefing narrative.
  12. `recommendations_context_node` (DETERMINISTIC): Connects validated root cause to prioritized action levers.
  13. `abstention_node` (SAFETY_GUARD): Generates safe, non-speculative diagnostic response when confidence is low.

---

### Layer 4: Capability-Aware AI & Safety Guard Layer
* **Multi-Tier Provider Routing Matrix ([`ai/orchestration/provider_router.py`](../../ai/orchestration/provider_router.py)):**
  ```text
  STANDARD REASONING TASKS:
  [Groq Pool 1: llama-3.3-70b-versatile]
        │ (429 Rate Limit / Quota)
        ▼
  [Groq Pool 2: llama-3.3-70b-versatile]
        │ (Provider Unavailable)
        ▼
  [Gemini Pool 1: gemini-2.5-flash]
        │ (429 / Quota)
        ▼
  [Gemini Pool 2: gemini-2.5-flash]
        │ (Total AI Outage)
        ▼
  [Deterministic Grounded Fallback Engine]
  ```
  ```text
  MULTIMODAL TASKS (Image / Chart / Vision):
  [Gemini Pool 1] ──(failover)──► [Gemini Pool 2] ──(fallback)──► [Deterministic Fallback]
  ```
* **Grounding Validator ([`ai/langgraph/nodes/investigation_nodes.py`](../../ai/langgraph/nodes/investigation_nodes.py)):**
  - Inspects LLM JSON responses against the immutable context container.
  - Rejects any response citing unverified evidence IDs or hallucinated driver names.
  - Automatically activates deterministic synthesis if an LLM fails grounding validation.
* **Security & Credential Isolation:**
  - Zero API key exposure: Telemetry, logs, and API payloads use safe logical pool identifiers (`groq_pool_1`, `gemini_pool_1`, `deterministic_fallback`).

---

### Layer 5: Dynamic Decision Graph & Presentation Layer
* **Dynamic Decision Graph Generator ([`ai/decision_graph/generator.py`](../../ai/decision_graph/generator.py)):**
  - Dynamically synthesizes the authoritative 6-column causal topology:
    - **Col 1 (KPI Anomaly):** `kpi-1` (-$1.23M / -7.97%).
    - **Col 2 (Causal Drivers):** `drv-1` (Atlanta Stockout), `drv-2` (Horizon Pricing), `drv-3` (PO Deferrals), `drv-4` (SKU Mix Shift).
    - **Col 3 (Empirical Evidence):** `evid-1` (ERP WMS Log), `evid-2` (Distributor Orders), `evid-3` (Pricing Intel), `evid-4` (SKU Volume).
    - **Col 4 (Business Mechanisms):** `mech-1` (Phantom Inventory Backlog), `mech-2` (Price Elasticity Churn).
    - **Col 5 (Action Levers):** `act-1` (Charlotte Emergency Transfer), `act-2` (Distributor Promotional Allowance).
    - **Col 6 (Predicted Outcome):** `out-1` (+$484K Revenue Recovery & Inventory Stabilization).
* **Restricted 2-Column Graph on Abstention:**
  - If analytical confidence is below 65%, Columns 3–6 are suppressed to prevent speculative actions.
* **FastAPI REST Service ([`backend/app/main.py`](../../backend/app/main.py)):**
  - Typed Pydantic v2 endpoints for `/kpis`, `/investigations`, `/evidence`, `/decision-graph`, `/recommendations`, `/simulations`, `/ai`, and `/demo`.
* **Next.js 14 Interactive Web Application ([`frontend/next-app/`](../../frontend/next-app)):**
  - **Screen 1:** Command Center (KPI anomaly triage & persona selector).
  - **Screen 2:** Root Cause Diagnosis (Driver decomposition & Grounded AI synthesis).
  - **Screen 3:** AI Investigation Activity (Live LangGraph node execution & latency telemetry).
  - **Screen 4:** Decision Graph (Interactive 6-column SVG causal canvas).
  - **Screen 5:** Evidence Explorer (5-layer audit drawer & SHA-256 hash verifier).
  - **Screen 6:** Recommendations & Simulation (Action levers & interactive slider sandbox).
  - **Screen 7:** Executive Briefing (Boardroom-ready pitch & decision report).

---

## 4. Persona Dual-View Synthesis

InsightPilot AI provides role-tailored narratives while strictly maintaining **100% quantitative parity**:

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                   DETERMINISTIC INVESTIGATION STATE                         │
│       (100% Locked Metrics, Drivers, Evidence Hashes & Confidence)          │
└──────────────────────┬───────────────────────────────┬──────────────────────┘
                       │                               │
                       ▼                               ▼
       ┌───────────────────────────────┐ ┌───────────────────────────────┐
       │     CFO PERSONA SYNTHESIS     │ │   SALES MANAGER SYNTHESIS     │
       ├───────────────────────────────┤ ├───────────────────────────────┤
       │ • EBITDA & Financial Exposure │ │ • Atlanta DC Availability 79% │
       │ • $1.23M Revenue Shortfall    │ │ • 29 Deferred Purchase Orders │
       │ • Gross Margin Impact (+0.72%)│ │ • SKU-8821 Stockout Timeline  │
       │ • Recovery ROI ($484K Target) │ │ • Charlotte Emergency Transfer│
       └───────────────────────────────┘ └───────────────────────────────┘
```

* **CFO Narrative Focus:** Focuses on EBITDA impact, $1.23M revenue exposure, margin recovery (+0.72%), and capital allocation.
* **Sales Manager Narrative Focus:** Focuses on Atlanta DC availability (79.4%), SKU-8821 order deferrals (29 POs), and the 20,000-unit Charlotte transfer.
* **Invariance Guarantee:** Revenue, variance, driver percentages, confidence, evidence hashes, and simulation outputs are 100% identical between personas.

---

## 5. Verification & Testing Matrix

The system is fortified by **174 automated tests** covering all operational domains:

```text
======================================================================
INSIGHTPILOT AI -- COMPREHENSIVE TEST SUITE SUMMARY
======================================================================
[1] Dataset Validation:       6/6 Checks Pass (100% Schema & Referential Integrity)
[2] Unit & Integration Tests: 174/174 Tests Pass (100% Passing in ~31s)
    ├── tests/demo/:           12 Tests Pass (Demo Mode, Narrative, Replay, Readiness)
    ├── tests/e2e/:            37 Tests Pass (Failover Scenarios A-E, Abstention, DG)
    ├── tests/ai/:             51 Tests Pass (LangGraph Nodes, Routing, Grounding)
    ├── tests/api/:            34 Tests Pass (FastAPI REST Contracts, Personas)
    ├── tests/evidence/:       11 Tests Pass (Lineage, Cryptographic Hashes, Ranking)
    ├── tests/analytics/:      13 Tests Pass (KPI Math, Driver Normalization, Confidence)
    ├── tests/recommendations/: 10 Tests Pass (Action Levers, Impact Prioritization)
    └── tests/simulation/:      6 Tests Pass (Mathematical Bounds, Source Immutability)
[3] Next.js Production Build:  10/10 Routes Compile to Static Production HTML/JS
======================================================================
```

---

## 6. Architectural Conclusion

InsightPilot AI represents a new standard in Enterprise Business Intelligence: combining the **bulletproof precision of deterministic analytical systems** with the **fluid synthesis of modern generative models** under a **verifiable, zero-hallucination, and resilient multi-agent architecture**.
