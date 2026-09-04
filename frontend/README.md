# InsightPilot AI — Frontend Architecture & Integration Guide

> **Accenture Innovation Challenge 2026 — Track 3: BusinessIntelligence.ai**  
> **Status:** Grounded Gemini Intelligence Integrated Across All 7 Stitch Screens

---

## 1. Architecture Overview

InsightPilot AI utilizes a zero-framework, lightweight frontend architecture designed to preserve the Round 1 Stitch visual design system:

- **Markup:** Semantic HTML5 (`code.html` across 7 screen directories).
- **Styling:** Tailwind CSS CDN with Material 3 Dark Theme design tokens (Primary Teal `#4fdbc8`, Deep Navy `#051424`, Glass Panels with backdrop blur).
- **Scripts:** Native JavaScript (ES Modules).
- **Icons & Fonts:** Material Symbols Outlined, Manrope (Display KPIs), Inter (Body), JetBrains Mono (Labels).
- **API Client:** Native browser `fetch()` client (`frontend/api/client.js`) with configurable base URL, `AbortController` timeouts, typed errors, and grounded Gemini endpoint helpers.
- **State Store:** Lightweight in-memory cache store (`frontend/state/store.js`) supporting persona switching (CFO vs Regional Sales Manager) and query parameter deep-links.

---

## 2. Directory Structure

```text
stitch_insightpilot_ai_executive_platform/
├── executive_command_center_v3_optimized_hierarchy/   # Screen 1 (Live KPI & Grounded AI Summary)
├── ai_investigation_activity_v2/                       # Screen 2 (Timeline & Grounded AI Synthesis)
├── root_cause_investigation_v2/                        # Screen 3 (Diagnostic Drivers & AI Reasoning)
├── decision_graph_v4_final_presentation_view/         # Screen 4 (Decision Graph & AI Inspector)
├── evidence_explorer_v2/                               # Screen 5 (Evidence Repository & URL Filter)
├── recommendations_simulation_v3_decision_ready/       # Screen 6 (Action Cards & What-If Slider)
└── executive_briefing_v3_boardroom_ready/              # Screen 7 (Executive Boardroom Briefing)

frontend/
├── api/
│   └── client.js             # API client with timeout, JSON parsing, and domain helpers
├── config/
│   └── config.js             # Base URL config (defaults to http://127.0.0.1:8000)
├── utils/
│   └── formatters.js         # Formatting helpers (Currency, %, Points, Numbers, Confidence)
├── state/
│   └── store.js              # Lightweight state store for active KPI, persona, and caches
└── README.md                 # This documentation
```

---

## 3. How to Run Locally

### Step 1: Start the Backend (Port 8000)
```bash
python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000
```

### Step 2: Start the Frontend Static Server (Port 8080)
```bash
python -m http.server 8080
```

### Step 3: Open in Browser
Navigate to:
```text
http://localhost:8080/stitch_insightpilot_ai_executive_platform/executive_command_center_v3_optimized_hierarchy/code.html
```

---

## 4. API Client & Base URL Configuration

The API client (`frontend/api/client.js`) automatically connects to `http://127.0.0.1:8000` (or `window.__API_BASE_URL__`).

### Available Methods:
- `apiClient.getKPIs()`: Returns all 5 tracked enterprise KPIs.
- `apiClient.getKPI(kpiId)`: Returns single KPI detail and variance.
- `apiClient.getInvestigation(kpiId, region, prevPeriod, currPeriod, persona)`: Full root cause diagnostic tree.
- `apiClient.getDrivers(kpiId, region)`: Ranked drivers list.
- `apiClient.getEvidenceList(kpiId, region)`: Corroborating evidence records.
- `apiClient.getEvidence(evidenceId)`: Single evidence node.
- `apiClient.getEvidenceLineage(evidenceId)`: 5-layer cryptographic audit trace.
- `apiClient.getRecommendations(kpiId, region)`: Prioritized prescriptive actions.
- `apiClient.getSimulationBaseline(region)`: Empirical baseline availability & revenue.
- `apiClient.simulateInventoryAvailability(availabilityRatio, region)`: Live recovery projection.
- `apiClient.getAIExplanation(kpiId, options)`: Grounded Gemini executive narrative (`POST /api/v1/ai/explain/{kpi_id}`).

---

## 5. Screen Integration Summary

| Screen | Primary API Endpoint | Grounded Gemini Role | Quantitative Truth |
| :--- | :--- | :--- | :--- |
| **1. Command Center** | `GET /api/v1/kpis` | Executive summary narrative | Revenue `$14.20M (-7.97%)` |
| **2. Investigation** | `GET /api/v1/investigations/{id}` | Multi-agent synthesis & status | Confidence `89.0% HIGH` |
| **3. Root Cause** | `GET /api/v1/investigations/{id}` | Causal & secondary reasoning | Atlanta Stockout `43.2% (-$550K)` |
| **4. Decision Graph** | `GET /api/v1/investigations/{id}` | Node inspector synthesis | Full causal graph topology |
| **5. Evidence Explorer** | `GET /api/v1/evidence/{id}` | Verified citation deep-linking | 9 cryptographically verified nodes |
| **6. Recommendations** | `GET /api/v1/recommendations/{id}` | Action rationale synthesis | P1 Emergency Transfer `+$484K` |
| **7. Executive Briefing** | `GET /api/v1/ai/explain/{id}` | Comprehensive boardroom briefing | Total recovery projected: `+$757.6K` |
