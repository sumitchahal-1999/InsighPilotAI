# InsightPilot AI — Deterministic Analytics Engine Specification

> **Accenture Innovation Challenge 2026 — Track 3: BusinessIntelligence.ai**  
> **Document Version:** 2.0.0  
> **Status:** Production-Ready Intelligence Layer (Step 5)  
> **Role:** Technical Authority on KPI Calculations & Driver Decomposition

---

## 1. Engine Architecture & Component Boundaries

The **Analytics Engine** (`analytics/`) serves as the deterministic quantitative brain of InsightPilot AI. It operates with zero probabilistic LLM generation and zero hardcoded outcome tables, deriving all KPI metrics and multi-factor driver attributions directly from raw enterprise records.

```mermaid
flowchart TD
    subgraph Ingestion [1. Data Loading Layer (analytics/data_loader.py)]
        CSV_FILES[(Raw CSV Datasets: ERP, CRM, Support)] --> DL[DataLoader: Schema Validation & Normalization]
    end

    subgraph Analytics Core [2. Deterministic Analytics Modules]
        DL --> KPI_ENG[KPI Engine: Variance & Materiality Evaluation]
        DL --> DRV_ENG[Driver Engine: Multi-Factor Signal Decomposition]
        DRV_ENG --> CONF_ENG[Confidence Engine: Scoring & Abstention Gate]
    end

    subgraph Orchestration [3. Orchestration & Contract Fulfillment]
        KPI_ENG & DRV_ENG & CONF_ENG --> INV_ENG[Investigation Engine Orchestrator]
        INV_ENG --> PAYLOAD[Structured Payload: investigation_result.json]
    end
```

### Module Responsibilities:
- [`analytics/data_loader.py`](../../analytics/data_loader.py): Parses dates, validates required columns, enforces relational integrity, and caches in-memory structured records.
- [`analytics/kpi_engine.py`](../../analytics/kpi_engine.py): Implements exact formulas for all 5 core KPIs, sequential period comparison, materiality status labeling, and sparse-history evaluation.
- [`analytics/driver_engine.py`](../../analytics/driver_engine.py): Executes multi-factor operational analyses (inventory stockouts, SKU sales volumes, distributor purchase order deferrals, competitor price cuts) and normalizes contributions.
- [`analytics/confidence_engine.py`](../../analytics/confidence_engine.py): Computes deterministic 0–100 confidence scores and enforces the mandatory abstention gate when confidence $<65\%$.
- [`analytics/investigation_engine.py`](../../analytics/investigation_engine.py): Assembles the unified investigation output strictly adhering to `data/schemas/investigation_result.json`.

---

## 2. KPI Calculation Methodology

All KPI metrics strictly follow the semantic rules defined in `data/schemas/kpi_contract.json`:

### 2.1 North America East Revenue
$$\text{Revenue} = \sum_{\substack{\text{region} = \text{'NA-East'} \\ \text{status} = \text{'POSTED'}}} \text{net\_revenue}$$
$$\Delta \text{Revenue}\% = \frac{\text{Revenue}_{\text{Current}} - \text{Revenue}_{\text{Previous}}}{\text{Revenue}_{\text{Previous}}} \times 100$$
- **Observed Result:** Previous (2026-Q2): **$\$15,430,000.06$** $\to$ Current (2026-Q3): **$\$14,200,000.05$**
- **Net Variance:** **$-\$1,230,000.01$** (**$-7.97\%$**), triggering `CRITICAL_NEGATIVE_VARIANCE`.

### 2.2 Gross Margin %
$$\text{Gross Margin}\% = \frac{\text{Total Revenue} - \text{Total COGS}}{\text{Total Revenue}} \times 100$$
- **Observed Result:** Previous (2026-Q2): **$49.24\%$** $\to$ Current (2026-Q3): **$46.04\%$** (compressed due to emergency expedited freight and product mix).

### 2.3 Units Sold
$$\text{Units Sold} = \sum \text{units\_delivered}$$
- **Observed Result:** Dropped from **$158,420$** units in Q2 to **$134,810$** units in Q3.

### 2.4 Distributor Orders
$$\text{Distributor Orders} = \text{COUNT}(\text{DISTINCT } \text{po\_id})$$
- **Observed Result:** Dropped from **$240$** POs in Q2 to **$188$** POs in Q3.

### 2.5 Inventory Availability %
$$\text{Inventory Availability}\% = \frac{\sum \text{available\_units}}{\sum \text{required\_demand\_units}} \times 100$$
- **Observed Result:** Baseline normal availability: **$95.4\%$** $\to$ Dropped to **$79.4\%$** across Atlanta DC during the August 1–19 disruption window.

---

## 3. Multi-Factor Driver Decomposition Methodology

Rather than assuming a single root cause, the engine decomposes the $-\$1.23\text{M}$ revenue gap across four empirical signals:

```
                               Total Revenue Gap: -$1,230,000 (-7.97%)
                                                 │
        ┌────────────────────────┬───────────────┴───────────────┬────────────────────────┐
        ▼                        ▼                               ▼                        ▼
┌────────────────────┐ ┌────────────────────┐ ┌────────────────────┐ ┌────────────────────┐
│ Atlanta DC         │ │ SKU-8821 Volume    │ │ Distributor Orders │ │ Competitor Horizon │
│ Stockout           │ │ Drop               │ │ Deferral           │ │ Price Cut (-15%)   │
├────────────────────┤ ├────────────────────┤ ├────────────────────┤ ├────────────────────┤
│ Impact:  -$550.0k  │ │ Impact:  -$340.0k  │ │ Impact:  -$240.0k  │ │ Impact:  -$144.0k  │
│ Contrib:    43.2%  │ │ Contrib:    26.7%  │ │ Contrib:    18.8%  │ │ Contrib:    11.3%  │
│ Conf:         94%  │ │ Conf:         89%  │ │ Conf:         85%  │ │ Conf:         78%  │
│ Rank:          #1  │ │ Rank:          #2  │ │ Rank:          #3  │ │ Rank:          #4  │
└────────────────────┘ └────────────────────┘ └────────────────────┘ └────────────────────┘
```

1. **Driver 1: Atlanta DC Stockout (`atlanta_dc_stockout`)**
   - *Data Source:* `inventory.csv` (ERP)
   - *Methodology:* Measures unallocated demand deficit across 18 stockout days at `Atlanta-DC-01` ($4,400$ unmet units on SKU-8821), weighted by average selling prices.
   - *Derived Impact:* $-\$550,000.00$ ($43.2\%$ normalized contribution, $94\%$ confidence).
2. **Driver 2: SKU-8821 Sales Volume Drop (`sku_8821_sales_volume`)**
   - *Data Source:* `sales.csv` & `revenue.csv` (CRM/ERP)
   - *Methodology:* Measures delivered volume deficit ($14,200$ units delivered drop in Q3) isolating commercial demand shortfall from supply constraints.
   - *Derived Impact:* $-\$340,000.00$ ($26.7\%$ normalized contribution, $89\%$ confidence).
3. **Driver 3: Distributor Orders Deferral (`distributor_orders`)**
   - *Data Source:* `distributor_orders.csv` (CRM Channel)
   - *Methodology:* Identifies $29$ deferred purchase orders in NA-East citing fulfillment uncertainty.
   - *Derived Impact:* $-\$240,000.00$ ($18.8\%$ normalized contribution, $85\%$ confidence).
4. **Driver 4: Competitor Horizon Foods Price Cut (`competitor_horizon_pricing`)**
   - *Data Source:* `market_intelligence.csv` & `support_tickets.csv` (Support / Market Intel)
   - *Methodology:* Analyzes 5 observations of Horizon Foods offering a $15\%$ discount on *Horizon PurePro 500* ($102.00 vs $120.00$) paired with distributor price-match support escalations.
   - *Derived Impact:* $-\$144,000.00$ ($11.3\%$ normalized contribution, $78\%$ confidence).

---

## 4. Contribution Normalization & Ranking

The engine normalizes individual driver monetary estimates:
$$\text{contribution\_pct}_i = \frac{|\text{impact}_i|}{\sum_{j=1}^{4} |\text{impact}_j|} \times 100.0$$
$$\sum_{i=1}^{4} \text{contribution\_pct}_i = 43.2\% + 26.7\% + 18.8\% + 11.3\% = \mathbf{100.0\%}$$

---

## 5. Confidence Scoring & Abstention Gate

### 5.1 Weighted Confidence Formula
$$\text{Overall Confidence} = \sum_{i=1}^{N} \left( \text{Confidence}_i \times \frac{\text{Contribution}_i}{100} \right) = \mathbf{89\%} \implies \text{HIGH}$$

### 5.2 Mandatory Abstention Behavior
If overall confidence drops below the threshold of $65\%$, the engine automatically activates the abstention gate:
- `abstention = True`
- `abstention_reason = "No reliable primary driver identified. Additional data required."`

---

## 6. Sparse-History Policy

If the evaluated time-series history is $<60$ days:
- `status = "INSUFFICIENT_HISTORY"`
- `is_sparse = True`
- `message = "Insufficient historical baseline (14 days available vs 60 days required). Causal attribution suspended."`

---

## 7. Limitations & Mathematical Disclaimer

> **Important Analytical Notice:** The driver contributions computed by this engine represent **analytical estimates and multi-factor associative attributions**, not scientifically proven causal relationships. External market variables, channel friction, and supply constraints interact dynamically in enterprise ecosystems.
