# InsightPilot AI — Stitch Frontend Architecture Audit & Integration Plan

> **Accenture Innovation Challenge 2026 — Track 3: BusinessIntelligence.ai**  
> **Document Version:** 2.0.0  
> **Status:** Completed Audit & Authoritative Plan (Step 10A)  
> **Role:** Technical Authority on Stitch UI Architecture, Screen-to-API Contracts, and Dynamic Integration

---

## 1. Frontend Technology Inventory

An audit of `stitch_insightpilot_ai_executive_platform/` reveals the following foundational frontend technology stack:

- **Markup & Structure:** Semantic HTML5 (`code.html` across 7 screen directories).
- **Styling & Design System:** Tailwind CSS CDN (`https://cdn.tailwindcss.com?plugins=forms,container-queries`) extended with custom Material 3 / Modern Dark Theme design tokens:
  - *Color Palette:* Primary Teal (`#4fdbc8`, `#14b8a6`), Dark Background (`#051424`, `#0B0F19`), Glass Panels (`rgba(22, 27, 38, 0.6)` with `backdrop-filter: blur(20px)`), Surface Containers (`#122131`, `#1c2b3c`, `#273647`), Error Red (`#ffb4ab`, `#93000a`), Accent Blues (`#adc6ff`, `#0566d9`).
  - *Typography:* Google Fonts — **Manrope** (Headlines & Display KPIs), **Inter** (Body & Table Data), **JetBrains Mono** (Labels & Monospace Metadata).
  - *Iconography:* **Google Material Symbols Outlined** (`wght,FILL@100..700,0..1`).
- **Graph & Connector Visualization:** Pure SVG coordinate connectors and CSS grid columns with responsive bezier curves (`stroke="#14b8a6"` with glow filters).
- **Interactive Elements:** Pure JavaScript event bindings, slider range controls, tab selectors, and glass modal overlays.

---

## 2. Directory Structure Map

```text
stitch_insightpilot_ai_executive_platform/
├── executive_command_center_v3_optimized_hierarchy/
│   ├── code.html          # Screen 1: Executive Command Center v3 (501 lines)
│   └── screen.png         # Visual source of truth reference (423 KB)
├── ai_investigation_activity_v2/
│   ├── code.html          # Screen 2: AI Investigation Activity v2 (306 lines)
│   └── screen.png         # Visual source of truth reference (208 KB)
├── root_cause_investigation_v2/
│   ├── code.html          # Screen 3: Root Cause Investigation v2 (502 lines)
│   └── screen.png         # Visual source of truth reference (388 KB)
├── decision_graph_v4_final_presentation_view/
│   ├── code.html          # Screen 4: Decision Graph v4 (563 lines)
│   └── screen.png         # Visual source of truth reference (314 KB)
├── evidence_explorer_v2/
│   ├── code.html          # Screen 5: Evidence Explorer v2 (429 lines)
│   └── screen.png         # Visual source of truth reference (162 KB)
├── recommendations_simulation_v3_decision_ready/
│   ├── code.html          # Screen 6: Recommendations & Simulation v3 (414 lines)
│   └── screen.png         # Visual source of truth reference (262 KB)
└── executive_briefing_v3_boardroom_ready/
    ├── code.html          # Screen 7: Executive Briefing v3 (367 lines)
    └── screen.png         # Visual source of truth reference (220 KB)
```

---

## 3. Seven-Screen Detailed Inventory

### Screen 1: Executive Command Center v3
- **File:** `executive_command_center_v3_optimized_hierarchy/code.html`
- **Purpose:** Primary executive overview showing the 5 enterprise KPIs, sparkline trends, active anomaly alert (`NA-East Revenue ↓7.97%`), and quick investigation launch.
- **Dynamic Elements to Bind:**
  - 5 KPI Metric Cards: Revenue (`$14.20M`, `-7.97%`), Gross Margin (`57.4%`, `-3.2 pts`), Units Sold (`105,400`, `-8.5%`), Distributor Orders (`842`, `-12.1%`), Inventory Availability (`79.4%`, `-14.8 pts`).
  - Active Alert Banner: `Critical Negative Variance: North America East Revenue`.
  - Sparklines: Dynamic SVG polyline / SVG paths generated from historical quarterly records.
  - Persona Profile Badge: Toggle between `CFO` and `Regional Sales Manager`.

### Screen 2: AI Investigation Activity v2
- **File:** `ai_investigation_activity_v2/code.html`
- **Purpose:** Real-time multi-agent activity canvas showing investigation progression across ERP, CRM, and Logistics telemetry.
- **Dynamic Elements to Bind:**
  - Status Indicator: `SYSTEM STATUS: MISSION ACCOMPLISHED` / `INVESTIGATION COMPLETE`.
  - Execution Telemetry: Latency timer, confidence score (`89% HIGH`), evidence count (`9 verified nodes`).
  - Agent Activity Nodes: Telemetry ingestion, signal correlation, driver decomposition, lineage verification.

### Screen 3: Root Cause Investigation v2
- **File:** `root_cause_investigation_v2/code.html`
- **Purpose:** Detailed diagnostic breakdown of the investigated KPI movement.
- **Dynamic Elements to Bind:**
  - Investigation Header: `Why did North America East revenue decline?` (`ID: INV-EXEC-2026-NAE-001`).
  - KPI Variance Block: `-$1.23M Variance (-7.97%)`.
  - Ranked Drivers List (4 drivers):
    1. Atlanta DC Stockout: $43.2\%$ contribution, $-\$550\text{k}$ impact, $94\%$ confidence.
    2. SKU-8821 Sales Volume: $26.7\%$ contribution, $-\$340\text{k}$ impact, $89\%$ confidence.
    3. Distributor PO Deferrals: $18.8\%$ contribution, $-\$240\text{k}$ impact, $85\%$ confidence.
    4. Competitor Horizon Pricing: $11.3\%$ contribution, $-\$144\text{k}$ impact, $78\%$ confidence.
  - Linked Evidence Preview Drawer: Real source record IDs (`INV-SNAP-21971`, `TR-LOG-8910`, `PO-DEF-4412`).

### Screen 4: Decision Graph v4
- **File:** `decision_graph_v4_final_presentation_view/code.html`
- **Purpose:** Full multi-layered visual reasoning topology showing the complete causal graph from KPI anomaly $\to$ drivers $\to$ evidence $\to$ recommendations $\to$ predicted outcome.
- **Dynamic Elements to Bind:**
  - Column 1: KPI Node (Revenue $-\$1.23\text{M}$).
  - Column 2: Primary Operational Drivers (Atlanta Stockout, Volume Deficit).
  - Column 3: Secondary & External Factors (Distributor Deferral, Competitor Price Cut).
  - Column 4: Corroborating Evidence Nodes (ERP, CRM, Zendesk, Market Intel).
  - Column 5: Prescriptive Interventions (`REC-001`, `REC-002`, `REC-003`, `REC-004`).
  - Column 6: Predicted Outcome ($\$757.6\text{k}$ de-duplicated recovery).
  - SVG Connecting Paths: Dynamic bezier curves connecting active nodes.

### Screen 5: Evidence Explorer v2
- **File:** `evidence_explorer_v2/code.html`
- **Purpose:** Transparent audit workspace exposing verified evidence items, cryptographic SHA-256 hashes, source systems, and 5-layer lineage traces.
- **Dynamic Elements to Bind:**
  - Source System Filter Chips: `All Sources`, `ERP`, `CRM`, `Support`, `Market Intel`.
  - Evidence Node Cards: 9 verified evidence records with exact timestamps, source domains, and finding summaries.
  - Lineage Drawer: 5-layer audit trace (KPI $\to$ Driver $\to$ Evidence Node $\to$ Source Record $\to$ SHA-256 Hash).

### Screen 6: Recommendations & Simulation v3
- **File:** `recommendations_simulation_v3_decision_ready/code.html`
- **Purpose:** Decision workspace presenting prioritized action cards, Impact vs. Effort matrix, and interactive What-If simulation slider.
- **Dynamic Elements to Bind:**
  - Priority 1 Card: Emergency Inventory Transfer ($\$484\text{k}$ recovery, $\$28\text{k}$ cost, $91\%$ confidence, $14\text{d}$, Supply Chain).
  - Priority 2 Card: Targeted Distributor Outreach ($\$180\text{k}$ recovery, $85\%$ confidence, $21\text{d}$, Sales).
  - Priority 3 & 4 Cards: SKU-8821 Production Run ($\$238\text{k}$) & Trade Allowance Match ($\$93.6\text{k}$).
  - Action Matrix: 2D scatter visualization plotting impact vs. effort.
  - Interactive What-If Slider: Adjusts Inventory Availability ($0.0\%$ to $100.0\%$, default $90.0\%$).
  - Live Simulation Results: Live HTTP call to `POST /api/v1/simulations/inventory-availability` updating projected revenue recovery ($+\$341.4\text{k}$) and new projected revenue ($14.54\text{M}$).

### Screen 7: Executive Briefing v3
- **File:** `executive_briefing_v3_boardroom_ready/code.html`
- **Purpose:** Boardroom-ready executive briefing synthesizing Situation, Diagnosis, Evidence, Recommended Actions, Projected Impact, and Grounded Gemini Narrative.
- **Dynamic Elements to Bind:**
  - Section 1 (Situation): Deterministic revenue deficit statement ($-\$1.23\text{M}$, $-7.97\%$).
  - Section 2 (Diagnosis): Ranked driver decomposition.
  - Section 3 (Evidence): Verified multi-source synthesis.
  - Section 4 (Recommendation): Priority #1 & #2 execution strategy.
  - Section 5 (Expected Impact): Reconciled de-duplicated recovery ($\$757.6\text{k}$) and simulation projection.
  - Grounded Gemini Executive Narrative: Tailored narrative requested via `POST /api/v1/ai/investigations/north_america_east_revenue/explanation`.

---

## 4. Route & Navigation Map

```text
/                                   --> Screen 1: Executive Command Center v3
/investigation/activity             --> Screen 2: AI Investigation Activity v2
/investigation/root-cause           --> Screen 3: Root Cause Investigation v2
/investigation/decision-graph       --> Screen 4: Decision Graph v4
/evidence                           --> Screen 5: Evidence Explorer v2
/recommendations                    --> Screen 6: Recommendations & Simulation v3
/briefing                           --> Screen 7: Executive Briefing v3
```

---

## 5. Component Hierarchy & Reusable Elements

1. **`AppShell`:** Persistent layout wrapper containing:
   - `SidebarNav`: 7 navigation items with active glow indicators and live briefing CTA.
   - `TopAppBar`: Breadcrumbs, search input, notification badge, enterprise scope label, and `PersonaSelector` (CFO / Regional Sales Manager).
2. **`KPICard`:** Standardized KPI tile rendering display value, variance badge, sparkline, and materiality alert.
3. **`DriverCard`:** Diagnostic driver item showing rank, display name, contribution bar, monetary impact, and confidence tag.
4. **`EvidenceCard`:** Source-verified evidence item with domain badge, finding summary, timestamp, and lineage button.
5. **`LineageModal`:** Interactive drawer rendering the 5-layer cryptographic audit trail.
6. **`RecommendationCard`:** Prescriptive action card with priority badge, owner tag, expected recovery, and timeframe.
7. **`SimulationSlider`:** Interactive range slider connected to live backend simulation API with real-time recovery calculation.
8. **`AINarrativePanel`:** Executive text briefing rendered from grounded Gemini responses with telemetry tags.

---

## 6. Backend API Inventory

| # | HTTP Method | Endpoint Path | Source Module | Purpose |
|---|---|---|---|---|
| 1 | `GET` | `/health` | `routes/health.py` | Service health probe & version |
| 2 | `GET` | `/api/v1/kpis` | `routes/kpis.py` | Returns all 5 tracked enterprise KPIs |
| 3 | `GET` | `/api/v1/kpis/{kpi_id}` | `routes/kpis.py` | Returns single KPI current, previous, variance, materiality |
| 4 | `GET` | `/api/v1/investigations/{kpi_id}` | `routes/investigations.py` | Full investigation (KPI, drivers, confidence, lineage graph) |
| 5 | `GET` | `/api/v1/investigations/{kpi_id}/drivers` | `routes/investigations.py` | List of ranked analytical drivers |
| 6 | `GET` | `/api/v1/investigations/{kpi_id}/evidence` | `routes/investigations.py` | Corroborating evidence list for investigation |
| 7 | `GET` | `/api/v1/evidence/{evidence_id}` | `routes/evidence.py` | Single evidence node detail with source record ID |
| 8 | `GET` | `/api/v1/evidence/{evidence_id}/lineage` | `routes/evidence.py` | 5-layer lineage trace & SHA-256 verification hash |
| 9 | `POST` | `/api/v1/ai/investigations/{kpi_id}/explanation` | `routes/ai.py` | Grounded Gemini executive explanation |
| 10| `POST` | `/api/v1/ai/investigations/{kpi_id}/drivers/{driver_id}/explanation` | `routes/ai.py` | Grounded Gemini driver-specific explanation |
| 11| `GET` | `/api/v1/recommendations/{kpi_id}` | `routes/recommendations.py` | Prioritized recommendations list |
| 12| `GET` | `/api/v1/recommendations/{kpi_id}/{rec_id}` | `routes/recommendations.py` | Single recommendation detail with constraints & assumptions |
| 13| `GET` | `/api/v1/simulations/baseline` | `routes/simulations.py` | Empirical baseline availability (79.4%) & revenue ($14.20M) |
| 14| `POST` | `/api/v1/simulations/inventory-availability` | `routes/simulations.py` | Deterministic what-if recovery simulation for slider setting |

---

## 7. Screen-to-API Contract Mapping Matrix

| Stitch Screen | Primary Endpoint(s) | Key Response Fields | Applied Data Contract |
|---|---|---|---|
| **Screen 1 (Command Center)** | `GET /api/v1/kpis` | `kpis[].current_value`, `kpis[].percent_change`, `kpis[].materiality_status` | `data/schemas/kpi_contract.json` |
| **Screen 2 (Activity Timeline)** | `GET /api/v1/investigations/{kpi_id}` | `overall.overall_confidence`, `lineage_graph.nodes_count`, `timestamp` | `data/schemas/investigation_result.json` |
| **Screen 3 (Root Cause)** | `GET /api/v1/investigations/{kpi_id}/drivers` | `drivers[].driver_name`, `drivers[].contribution_pct`, `drivers[].impact_usd` | `data/schemas/driver_contract.json` |
| **Screen 4 (Decision Graph)** | `GET /api/v1/investigations/{kpi_id}`, `GET /api/v1/recommendations/{kpi_id}` | `drivers[]`, `evidence[]`, `recommendations[]`, `lineage_graph` | `data/schemas/investigation_result.json` |
| **Screen 5 (Evidence Explorer)**| `GET /api/v1/investigations/{kpi_id}/evidence`, `GET /api/v1/evidence/{id}/lineage` | `evidence[].finding_summary`, `evidence[].source_record_id`, `lineage.verification_hash` | `data/schemas/evidence_contract.json` |
| **Screen 6 (Recommendations)** | `GET /api/v1/recommendations/{kpi_id}`, `POST /api/v1/simulations/inventory-availability` | `recommendations[].expected_impact`, `estimated_recovery.revenue_recovery_usd` | `data/schemas/recommendation_contract.json`, `simulation_contract.json` |
| **Screen 7 (Executive Briefing)**| `POST /api/v1/ai/investigations/{kpi_id}/explanation`, `GET /api/v1/recommendations/{kpi_id}` | `explanation.headline`, `explanation.diagnosis`, `explanation.executive_takeaway` | `ai/schemas/explanation.py` |

---

## 8. UI-to-Response-Field Mapping & Transformation Rules

| UI Field / Component | Backend JSON Field | Raw Backend Value | UI Formatted Display | Transformation Function |
|---|---|---|---|---|
| Revenue Value | `kpis[revenue].current_value` | `14200000.05` | **`$14.20M`** | `formatCurrencyMillions(val)` |
| Revenue Variance | `kpis[revenue].percent_change` | `-7.97` | **`-8.0% (-$1.23M)`** | `formatPct(val)` + `formatVarianceUSD(amt)` |
| Gross Margin | `kpis[gross_margin].current_value`| `57.4` | **`57.4%`** | `val.toFixed(1) + '%'` |
| Inventory Availability Baseline | `baseline.baseline_availability_pct` | `79.4` | **`79.4%`** | `val.toFixed(1) + '%'` |
| Top Driver Contribution | `drivers[0].contribution_pct` | `43.2` | **`43.2%`** | `val.toFixed(1) + '%'` |
| Top Driver Impact | `drivers[0].impact_usd` | `-550000.00` | **`-$550K`** | `formatCurrencyThousands(val)` |
| P1 Recommendation Recovery | `recommendations[0].expected_impact.revenue_recovery_usd` | `484000.00` | **`$484K`** | `formatCurrencyThousands(val)` |
| Simulated Recovery | `simulation.estimated_recovery.revenue_recovery_usd` | `341422.91` | **`+$341.4K`** | `formatCurrencyThousands(val)` |
| SHA-256 Hash | `evidence.lineage.verification_hash` | `sha256:4f8e...` | **`4f8e...c901` (truncated)** | `hash.slice(7, 15) + '...' + hash.slice(-4)` |

---

## 9. State Management Assessment & Architecture

The frontend state architecture should be lightweight and modular:
1. **Global App State:**
   - `selectedKPI`: Default `"north_america_east_revenue"`.
   - `selectedPersona`: `"CFO"` (default) or `"REGIONAL_SALES_MANAGER"`.
   - `activeFiscalPeriod`: `"2026-Q3"` (comparison against `"2026-Q2"`).
2. **Screen-Level Cache:**
   - SWR / React Query or simple singleton in-memory API cache (`apiClient.ts` / `state.js`) to prevent redundant round-trips when switching between tabs.
3. **Simulation Interactive State:**
   - Debounced slider state ($250\text{ms}$) for `inventory_availability` ensuring smooth real-time visual feedback without flooding the server.

---

## 10. Loading, Skeleton, and Error States Plan

- **Loading State:** Maintain existing glassmorphism panels with subtle CSS shimmer skeleton animations (`animate-pulse bg-surface-variant/30`).
- **Error State:** If the backend is unreachable or returns HTTP `500/503`, display a clean glass banner:
  `"API Service Unavailable — Reconnecting..."` with a retry trigger.
- **AI Graceful Fallback:** If `GEMINI_API_KEY` is not configured, the Executive Briefing and AI explanation sections display the deterministic executive summary with a badge: `Deterministic Mode Active (Gemini Optional)`.

---

## 11. Persona Integration Plan

- **Selector Location:** Added to the TopAppBar next to the profile badge.
- **Supported Personas:**
  - `CFO`: Sets request body `{"persona": "CFO"}` for AI explanation; highlights financial exposure ($-\$1.23\text{M}$ revenue, $-3.2\text{ pts}$ margin).
  - `REGIONAL_SALES_MANAGER`: Sets request body `{"persona": "REGIONAL_SALES_MANAGER"}`; highlights operational fulfillment ($79.4\%$ availability, $29$ deferred POs).
- **Zero Quantitative Deviation:** The underlying numbers remain 100% identical.

---

## 12. Grounded Gemini Narrative Integration Plan

1. Frontend initiates `POST /api/v1/ai/investigations/{kpi_id}/explanation` with `{"persona": selectedPersona}`.
2. The browser never communicates with Google Gemini directly.
3. Upon receiving `200 OK`, renders `explanation.headline`, `explanation.diagnosis`, `explanation.executive_takeaway`, and evidence links.
4. If response is `503`, renders deterministic fallback summary without disrupting the page.

---

## 13. Environment Configuration Plan

- **API Base URL Configuration:** Configurable via environment variable:
  `VITE_API_BASE_URL=http://127.0.0.1:8000` (or `window.API_BASE_URL || "http://127.0.0.1:8000"`).
- **Port Standards:** Backend on port `8000`, Frontend dev server on port `3000` or `5173`.

---

## 14. CORS & Network Topology Assessment

- FastAPI backend is already configured in `backend/app/main.py` with:
  ```python
  allow_origins=["http://localhost:3000", "http://localhost:5173", "http://127.0.0.1:3000", "http://127.0.0.1:5173"]
  allow_methods=["GET", "POST", "OPTIONS"]
  allow_headers=["*"]
  ```
- Full preflight OPTIONS requests are supported and tested in `tests/api/test_api_endpoints.py`.

---

## 15. Static-to-Dynamic Migration Summary

| Screen | Static Placeholder | Dynamic Target Field |
|---|---|---|
| **Screen 1** | Hardcoded `-8.0%` & `$14.2M` | Ingest from `GET /api/v1/kpis/north_america_east_revenue` |
| **Screen 3** | Hardcoded driver percentages | Ingest from `GET /api/v1/investigations/north_america_east_revenue/drivers` |
| **Screen 4** | Static SVG decision tree | Ingest nodes & links from `GET /api/v1/investigations/north_america_east_revenue` |
| **Screen 5** | Static evidence cards | Ingest from `GET /api/v1/investigations/north_america_east_revenue/evidence` |
| **Screen 6** | Hardcoded `$6.20M` / `$2.90M` | Ingest reconciled `$484K` / `$180K` from `GET /api/v1/recommendations/...` |
| **Screen 6** | Static `+15%` slider | Bind slider to `POST /api/v1/simulations/inventory-availability` |
| **Screen 7** | Static `+$9.1M` briefing | Ingest de-duplicated `$757.6K` + live simulation outcome |

---

## 16. Formatting & Transformation Rules

```javascript
// Canonical frontend formatting utilities
export const formatCurrencyMillions = (val) => `$${(Math.abs(val) / 1e6).toFixed(2)}M`;
export const formatCurrencyThousands = (val) => `$${(Math.abs(val) / 1e3).toFixed(0)}K`;
export const formatPercent = (val) => `${val > 0 ? '+' : ''}${val.toFixed(1)}%`;
export const formatBasisPoints = (val) => `${val > 0 ? '+' : ''}${val.toFixed(1)} pts`;
```

---

## 17. Animation & Transition Preservation Plan

- **Screen Transitions:** Retain subtle opacity fade transitions (`transition-opacity duration-200`).
- **Graph Bezier Glow:** Retain SVG stroke dasharray and glow filters (`filter="url(#glow)"`).
- **Slider Smooth Feedback:** Retain CSS transition on track width and thumb position.
- **Card Hover Elevation:** Retain `transform transition-transform duration-150 hover:scale-[1.01]`.

---

## 18. Performance Optimization Strategy

1. **Request Deduplication:** Fetch investigation data once and share across screens 2, 3, 4, 5.
2. **Debounced Simulation:** 250ms debounce on slider drag to avoid spamming the simulation endpoint.
3. **SVG DOM Optimization:** Keep graph SVG paths lightweight with coordinate caching.

---

## 19. Browser Security & Secret Protection

- Zero API keys (`GEMINI_API_KEY`), database passwords, or filesystem paths will be exposed in client code.
- All requests flow through structured REST APIs with input validation.

---

## 20. Recommended Step 10 Implementation Order

To execute the frontend integration safely without breaking working screens:

1. **Step 10B — Frontend Foundation & API Client Layer:** Set up routing shell, API service layer, formatting utilities, and shared layout while keeping original Stitch screens 100% visually intact.
2. **Step 10C — Executive Command Center (Screen 1) Integration:** Bind 5 KPI cards and active alert banner to `GET /api/v1/kpis`.
3. **Step 10D — AI Investigation Activity (Screen 2) & Root Cause (Screen 3) Integration:** Bind ranked drivers and execution timeline to `GET /api/v1/investigations/{kpi_id}`.
4. **Step 10E — Decision Graph (Screen 4) Dynamic Rendering:** Bind node topology and SVG connectors to investigation & recommendation outputs.
5. **Step 10F — Evidence Explorer (Screen 5) & Lineage Drawer:** Bind 9 evidence nodes and 5-layer cryptographic lineage trace to `GET /api/v1/evidence`.
6. **Step 10G — Recommendations & What-If Simulation (Screen 6) Integration:** Bind reconciled action cards and interactive availability slider to `GET /api/v1/recommendations` and `POST /api/v1/simulations/inventory-availability`.
7. **Step 10H — Executive Briefing (Screen 7) & Grounded Gemini Integration:** Bind executive briefing and persona toggle to `POST /api/v1/ai/...`.
8. **Step 10I — End-to-End Navigation, Polish & Verification:** Verify seamless tab switching across all 7 screens with live backend data.
