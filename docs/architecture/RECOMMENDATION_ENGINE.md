# InsightPilot AI — Recommendation Engine Architecture

> **Accenture Innovation Challenge 2026 — Track 3: BusinessIntelligence.ai**  
> **Document Version:** 2.0.0  
> **Status:** Production-Ready (Step 9)  
> **Role:** Technical Authority on Prescriptive Decision Intelligence, Controllability, and Impact Attribution

---

## 1. Recommendation Architecture

The InsightPilot AI Recommendation Engine transforms diagnostic investigation findings into prioritized, actionable executive interventions. In accordance with core architectural guidelines, **all recommendations, expected impacts, prioritization ranks, ownership mappings, and confidence scores are calculated deterministically**.

```mermaid
flowchart TD
    subgraph Diagnostic_Layer [1. Diagnostic Analytics (Step 5)]
        DRV[Ranked Drivers: Atlanta Stockout, Volume Deficit, PO Deferral, Horizon Pricing]
    end

    subgraph Decision_Logic [2. Recommendation Engine (Step 9)]
        DRV --> LEVER[Driver-to-Lever Mapping]
        LEVER --> CTRL[Controllability Classification: HIGH / MEDIUM / LOW]
        CTRL --> ACT[Concrete Prescriptive Actions & Assumptions]
        ACT --> IMP[Deterministic Impact & Recovery Model]
        IMP --> PRIO[Multi-Factor Prioritization Matrix]
        PRIO --> OWNR[Deterministic Ownership Assignment]
        OWNR --> EVLNK[Evidence Linkage & Lineage Reference]
        EVLNK --> DBL[Overlap & Double-Counting Identification]
    end

    subgraph API_Delivery [3. FastAPI Endpoints]
        DBL --> RESP[GET /api/v1/recommendations/{kpi_id}]
    end
```

---

## 2. Driver-to-Lever Mapping & Controllability

Not all drivers of business variance can be controlled with equal organizational agency. The engine evaluates operational controllability to prioritize high-leverage internal interventions over passive market forces.

| Driver ID | Controllability | Controllable Lever | Prescriptive Business Action |
|---|---|---|---|
| `atlanta_dc_stockout` | **HIGH** | Inventory Availability / Inter-DC Stock Rebalancing | **Execute Emergency Inventory Transfer (20,000 Units from Charlotte Hub to Atlanta DC)** |
| `distributor_orders` | **HIGH** | Channel Partner Relationship & Order Re-commitment | **Targeted Distributor Recovery Outreach (Tier-1 Apex & Mid-Atlantic accounts)** |
| `sku_8821_sales_volume` | **MEDIUM** | Production Schedule & SKU Line Reallocation | **Accelerate SKU-8821 Production Run & Safety Stock Rebalancing** |
| `competitor_horizon_pricing` | **LOW** | Targeted Trade Allowance / Promotional Match | **Authorize Temporary 10% Wholesale Trade Allowance on Select High-Volume Accounts** |

---

## 3. Deterministic Impact Model

Expected revenue recovery is modeled as a function of the driver's quantified baseline impact, intervention feasibility, and customer elasticity:

$$\text{Projected Revenue Recovery} = |\text{Driver Impact USD}| \times \text{Intervention Recovery Efficiency}$$

| Recommendation | Driver Impact | Recovery Efficiency | Expected Revenue Recovery | Gross Margin Impact | Timeframe |
|---|---|---|---|---|---|
| **REC-2026-NAE-001 (Emergency Transfer)** | $-\$550,000.00$ | $88\%$ | **$\$484,000.00$** | $+1.2\text{ pts}$ | $14\text{ days}$ |
| **REC-2026-NAE-002 (Distributor Outreach)** | $-\$240,000.00$ | $75\%$ | **$\$180,000.00$** | $+0.6\text{ pts}$ | $21\text{ days}$ |
| **REC-2026-NAE-003 (SKU-8821 Run)** | $-\$340,000.00$ | $70\%$ | **$\$238,000.00$** | $+0.8\text{ pts}$ | $30\text{ days}$ |
| **REC-2026-NAE-004 (Trade Allowance)** | $-\$144,000.00$ | $65\%$ | **$\$93,600.00$** | $-0.4\text{ pts}$ | $45\text{ days}$ |

---

## 4. Prioritization Matrix

Recommendations are deterministically ranked based on a composite evaluation of:
1. **Controllability Level** ($\text{HIGH} > \text{MEDIUM} > \text{LOW}$)
2. **Absolute Recoverable Revenue Pool**
3. **Execution Speed** ($14\text{d} < 21\text{d} < 30\text{d} < 45\text{d}$)
4. **Empirical Evidence Confidence**

Resulting in the prioritized queue:
- **Rank 1 (`CRITICAL`):** `REC-2026-NAE-001` (Emergency Inventory Transfer)
- **Rank 2 (`HIGH`):** `REC-2026-NAE-002` (Targeted Distributor Outreach)
- **Rank 3 (`HIGH`):** `REC-2026-NAE-003` (Accelerate SKU-8821 Production Run)
- **Rank 4 (`MEDIUM`):** `REC-2026-NAE-004` (Authorize 10% Trade Allowance)

---

## 5. Ownership Mapping

Organizational ownership is assigned directly by business function:
- **Supply Chain / Operations:** `REC-2026-NAE-001`
- **Regional Sales / Commercial Operations:** `REC-2026-NAE-002`
- **Manufacturing & Product Operations:** `REC-2026-NAE-003`
- **Commercial Strategy & Pricing:** `REC-2026-NAE-004`

---

## 6. Overlap & Double-Counting Policy

To prevent misleading executive summaries where overlapping actions are summed without boundary, the engine attaches `overlap_group` tags:
- `REC-2026-NAE-001` and `REC-2026-NAE-003` share `overlap_group: FULFILLMENT_RECOVERY` (both address the same unfulfilled demand pool at Atlanta DC and regional depots).
- `REC-2026-NAE-002` belongs to `CHANNEL_SALES`.
- `REC-2026-NAE-004` belongs to `COMMERCIAL_PRICING`.
