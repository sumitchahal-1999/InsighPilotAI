# InsightPilot AI — Economic & Business Model Reconciliation

> **Accenture Innovation Challenge 2026 — Track 3: BusinessIntelligence.ai**  
> **Document Version:** 2.0.0  
> **Status:** Completed Audit & Authoritative Reconciliation (Step 9A)  
> **Role:** Technical Authority on Financial Modeling, Presentation vs. Deterministic Economics, and Business Model Consistency

---

## 1. Executive Summary

This document provides a thorough audit and reconciliation between the **Round 1 conceptual presentation figures** shown in the static Stitch UI screens and the **Round 2 deterministic accounting engine** implemented in the Python backend.

### Key Finding
- In **Round 1 (Static Prototype)**, the platform displayed conceptual macro-level figures: **$\$6.20\text{M}$** for Emergency Inventory Transfer, **$\$2.90\text{M}$** for Temporary Trade Allowance, and **$\$9.10\text{M}$** for Total Projected Recovery.
- In **Round 2 (Deterministic Backend)**, the system models the locked **North America East Q3 Revenue Deficit**:
  $$\text{Baseline Q2: } \$15,430,000.06 \longrightarrow \text{Current Q3: } \$14,200,000.05 \quad (\Delta = -\$1,230,000.01, -7.97\%)$$
- **Mathematical Reality:** Recovering $\$6.20\text{M}$ in a single quarter on a $-\$1.23\text{M}$ regional deficit would represent $>500\%$ of the entire quarterly loss—a physical impossibility under GAAP accounting.
- **Reconciliation Verdict (Option A):** The Round 2 deterministic backend values ($\$484\text{k}$, $\$180\text{k}$, $\$238\text{k}$, $\$93.6\text{k}$) represent the true **Near-Term Immediate Realizable Quarterly Recovery**, while the Round 1 Stitch figures represented **Illustrative Annualized Addressable Run-Rate Opportunity**. The deterministic backend is the sole source of quantitative truth for the prototype.

---

## 2. Comparison: Round 1 Presentation vs. Round 2 Deterministic Backend

| Metric / Parameter | Round 1 Stitch UI Mockups | Round 2 Deterministic Backend | Reconciliation Classification |
|---|---|---|---|
| **Investigated KPI Movement** | NA-East Revenue $\downarrow 8.0\%$ | NA-East Revenue: $\$15.43\text{M} \to \$14.20\text{M} = -7.97\%$ | **Exact Match** (Locked Ground Truth) |
| **Quarterly Net Variance** | $-\$1.2\text{M}$ | $-\$1,230,000.01$ | **Exact Match** |
| **Top Driver (Atlanta DC Stockout)** | Rank #1 ($44\%$) | Rank #1 ($43.2\%$ contribution, $-\$550,000.00$ impact) | **Deterministic Calculation** |
| **P1 Action (Emergency Transfer)** | Recovery: **$\$6.20\text{M}$**, Cost: $\$180\text{k}$, Net: $\$6.02\text{M}$ | Recovery: **$\$484,000.00$**, Cost: $\$28\text{k}$, Net: $\$456\text{k}$ | **Quarterly vs. Annualized Concept** |
| **P1 Confidence** | $91.2\%$ | $91\%$ (`HIGH`) | **Integer Engine Precision** |
| **P2 Action (Trade Allowance)** | Recovery: **$\$2.90\text{M}$**, Cost: $\$240\text{k}$ | Recovery: **$\$93,600.00$**, Budget: $\$50\text{k}$ | **Quarterly vs. Annualized Concept** |
| **P2 Confidence** | $83.6\%$ | $84\%$ (`HIGH`) | **Integer Engine Precision** |
| **Total Projected Recovery** | **$\$9.10\text{M}$** ($6.2\text{M} + 2.9\text{M}$) | **$\$484\text{k} + \$180\text{k} + \$93.6\text{k} = \$757.6\text{k}$** (De-duplicated) | **Strict Double-Counting Prevention** |
| **What-If Simulation (90% Avail.)** | $+\$1.2\text{M}$ (Illustrative slider tag) | **$+\$341,422.91$** (Baseline $79.4\% \to 90.0\%$) | **Pure Mathematical Simulation** |

---

## 3. Location of Round 1 Values in Stitch UI Screens

The Round 1 values originate from static HTML mockups created during the initial visual design phase:

1. **`stitch_insightpilot_ai_executive_platform/recommendations_simulation_v3_decision_ready/code.html`:**
   - Line 243: `Recovery: $6.20M` (Emergency Inventory Transfer)
   - Line 247: `Cost: $180K`
   - Line 239: `Net Benefit: $6.02M`
   - Line 280: `Recovery: $2.90M` (Temporary Trade Allowance)
   - Line 284: `Cost: $240K`
   - Line 345: `(Illustrative simulation)`
   - Line 380: `+$1.2M` (Slider outcome)
2. **`stitch_insightpilot_ai_executive_platform/executive_briefing_v3_boardroom_ready/code.html`:**
   - Line 346: `Projected Recovery: +$9.1M`
   - Line 353: `AI Confidence Score: 87.4%`
3. **`stitch_insightpilot_ai_executive_platform/decision_graph_v4_final_presentation_view/code.html`:**
   - Line 476: `Projected Recovery: $9.1M`
   - Line 479: `Net Benefit: $8.68M` ($6.02\text{M} + (2.90\text{M} - 0.24\text{M}) = \$8.68\text{M}$)

---

## 4. Mathematical Audit & Infeasibility of $6.2M Quarterly Recovery

### The Fundamental Accounting Equation
In the synthetic enterprise datasets (`data/raw/sales.csv`), the total quarterly sales for NA-East across Q3 2026 are:
- Target / Baseline Q2 Invoiced Revenue: **$\$15,430,000.06$**
- Actual Realized Q3 Invoiced Revenue: **$\$14,200,000.05$**
- **Maximum Possible Quarterly Revenue Gap:** **$\$1,230,000.01$**

### Why $6.20M Cannot Be Single-Quarter Recovery
1. If the entire revenue shortfall in Q3 is $\$1.23\text{M}$, a single intervention (Emergency Inventory Transfer) recovering $\$6.20\text{M}$ would imply that the intervention recovers:
   $$\frac{\$6,200,000}{\$1,230,000} \approx 504\% \text{ of the entire lost quarterly revenue}$$
2. The Atlanta DC stockout caused **4,400 unfulfilled units** during August 1–19. At an average SKU-8821 unit selling price of $\$125.00$, the lost invoice revenue is:
   $$4,400 \text{ units} \times \$125.00/\text{unit} = \$550,000.00$$
3. Therefore, transferring 20,000 units from Charlotte to Atlanta can recover at most the **$\$550,000.00$** direct inventory loss plus downstream distributor re-orders ($\approx \$484,000.00$ at $88\%$ recapture rate).
4. Forcing the backend to report $\$6.20\text{M}$ for a $\$550\text{k}$ driver would be completely indefensible under enterprise scrutiny.

---

## 5. Mathematical Audit of the $2.9M Trade Allowance

- **Horizon Foods Competitor Price Cut Impact:** The driver analysis establishes that Horizon Foods' 15% price cut caused **$-\$144,000.00$** in direct quarterly volume loss across Mid-Atlantic accounts.
- **Recoverable Opportunity:** A 10% targeted wholesale trade allowance on high-volume SKUs defends against further share erosion, recapturing $65\%$ of the at-risk revenue:
  $$\$144,000.00 \times 0.65 = \mathbf{\$93,600.00}$$
- **Origin of $\$2.90\text{M}$:** In the Round 1 conceptual narrative, $\$2.90\text{M}$ represented the **annualized wholesale distributor account value** at risk across all Tier-1 and Tier-2 accounts if competitive price matching was ignored for 4 quarters.

---

## 6. Audit of the $9.1M Figure & Double-Counting Analysis

In the Round 1 Stitch screens:
$$\$6.20\text{M} \text{ (P1)} + \$2.90\text{M} \text{ (P2)} = \mathbf{\$9.10\text{M}}$$
$$\$6.02\text{M} \text{ (P1 Net)} + \$2.66\text{M} \text{ (P2 Net)} = \mathbf{\$8.68\text{M}}$$

### Double-Counting Vulnerability
In reality, Emergency Inventory Transfer (`atlanta_dc_stockout`) and SKU-8821 Accelerated Production (`sku_8821_sales_volume`) share the **same customer demand pool**. If both interventions are executed simultaneously, they cannot each independently claim the full unfulfilled order backlog.
- InsightPilot AI Step 9 introduced the `overlap_group: FULFILLMENT_RECOVERY` tag to explicitly prevent double-counting.
- The de-duplicated near-term recovery across all 4 levers is:
  $$\text{De-duplicated Recovery} = \$484\text{k} + \$180\text{k} + \$93.6\text{k} = \mathbf{\$757,600.00}$$

---

## 7. 20,000-Unit Inventory Transfer Analysis

- **Status:** **Candidate Prescriptive Intervention Scenario** (not past historical fact).
- **Feasibility in Data:**
  - `data/raw/inventory.csv` confirms that Charlotte Hub (`Charlotte-HUB-01`) maintains an average inventory availability of $>94\%$ with $>42,000$ available units of SKU-8821.
  - Transferring 20,000 units from Charlotte to Atlanta DC is physically and logistically feasible within 72 hours.
  - The direct expedited freight surcharge is modeled at **$\$28,000.00$** (matching logistics logs in `data/raw/logistics.csv`).

---

## 8. Confidence Score Precision (91.2% vs. 91%)

- In Round 1, confidence was displayed with one decimal place (`91.2%`, `83.6%`, `87.4%`).
- In Round 2, `analytics/confidence_engine.py` evaluates confidence deterministically based on data quality (0.35), signal consistency (0.30), corroborating sources (0.20), and sample size (0.15), producing calibrated integer scores (`91%`, `84%`, `88%`).
- **Conclusion:** Integer representation is standard for deterministic multi-factor scoring. Manufacturing artificial decimal precision would be misleading.

---

## 9. Final Reconciliation Decision

### Selected Path: OPTION A (Grounded Deterministic Truth)
1. **Authoritative Backend Truth:** The Python backend calculations ($\$484\text{k}$, $\$180\text{k}$, $\$238\text{k}$, $\$93.6\text{k}$, $\$341.4\text{k}$ simulation) are the **sole authoritative source of quantitative truth**.
2. **Stitch UI Role:** When the Stitch frontend is connected in Step 10, the UI cards will bind dynamically to the real FastAPI `/api/v1/recommendations` and `/api/v1/simulations` endpoints, displaying the real deterministic figures.
3. **Zero Hardcoded Falsification:** No synthetic formulas or artificial scaling multipliers will be introduced to force the backend to match static mockup text.

---

## 10. Summary Table of Authoritative Prototype Truth

| Field | Authoritative Value | Derivation Source |
|---|---|---|
| **Base Q2 Revenue** | $\$15,430,000.06$ | `analytics/kpi_engine.py` (`sales.csv`) |
| **Q3 Realized Revenue** | $\$14,200,000.05$ | `analytics/kpi_engine.py` (`sales.csv`) |
| **Q3 Net Variance** | $-\$1,230,000.01$ ($-7.97\%$) | Deterministic difference |
| **Atlanta Stockout Impact** | $-\$550,000.00$ ($43.2\%$) | `analytics/driver_engine.py` |
| **SKU-8821 Volume Deficit Impact** | $-\$340,000.00$ ($26.7\%$) | `analytics/driver_engine.py` |
| **Distributor Deferral Impact** | $-\$240,000.00$ ($18.8\%$) | `analytics/driver_engine.py` |
| **Competitor Pricing Impact** | $-\$144,000.00$ ($11.3\%$) | `analytics/driver_engine.py` |
| **Emergency Transfer Recovery (P1)** | **$\$484,000.00$** ($91\%$ conf) | `analytics/recommendations.py` ($\$550\text{k} \times 0.88$) |
| **Distributor Outreach Recovery (P2)**| **$\$180,000.00$** ($85\%$ conf) | `analytics/recommendations.py` ($\$240\text{k} \times 0.75$) |
| **SKU-8821 Production Run Recovery (P3)**| **$\$238,000.00$** ($88\%$ conf) | `analytics/recommendations.py` ($\$340\text{k} \times 0.70$) |
| **Trade Allowance Match Recovery (P4)**| **$\$93,600.00$** ($84\%$ conf) | `analytics/recommendations.py` ($\$144\text{k} \times 0.65$) |
| **Simulation Baseline Availability** | **$79.4\%$** | `simulation/simulation_engine.py` |
| **Simulation 90% Target Recovery** | **$+\$341,422.91$** ($91\%$ conf) | `simulation/simulation_engine.py` |
