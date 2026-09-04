# InsightPilot AI — Synthetic Enterprise Data Foundation

> **Accenture Innovation Challenge 2026 — Track 3: BusinessIntelligence.ai**  
> **Documentation:** Synthetic Dataset Specification & Integrity Guide  
> **Status:** Production-Ready Baseline Dataset (Step 4)

---

## 1. Overview & Purpose

This directory contains realistic, synthetic enterprise datasets simulating three heterogeneous data domains:
1. **ERP (Financials & Supply Chain):** `revenue.csv`, `inventory.csv`, `margin.csv`
2. **CRM / Sales:** `sales.csv`, `distributor_orders.csv`
3. **Support & Market Intelligence:** `support_tickets.csv`, `distributor_communications.csv`, `market_intelligence.csv`

> **Design Principle:** The data is generated as raw operational transaction records, DC snapshots, support escalations, communications, and price observations. It contains **no hidden driver labels, no hardcoded final scores, and no artificial "root_cause" columns**. All conclusions, variance calculations, and driver rankings will be computed independently by the deterministic analytics layer in subsequent steps.

---

## 2. Temporal Boundaries & Periods

The dataset spans 15 months of daily/weekly records across 5 fiscal quarters (July 1, 2025 – September 30, 2026):

| Period Identifier | Calendar Date Range | Role in Decision Intelligence |
|---|---|---|
| **Baseline Quarters** | `2025-07-01` to `2026-03-31` (2025-Q3, Q4, 2026-Q1) | Multi-quarter baseline for trend calculation & seasonal comparison |
| **Previous Comparison Period** | `2026-04-01` to `2026-06-30` (2026-Q2) | Direct predecessor quarter for sequential KPI variance detection ($\$15.43\text{M}$ NA-East Revenue) |
| **Current Investigation Period** | `2026-07-01` to `2026-09-30` (2026-Q3) | Target period exhibiting the primary anomaly ($\$14.20\text{M}$ NA-East Revenue / $-7.97\% \approx -8.0\%$) |

---

## 3. Master Dimensions & Relational Keys

The synthetic datasets are cross-linked through explicit relational keys conforming to schemas in `data/schemas/entities/`:

### 3.1 Geographic Regions & Territories
- **`NA-East` (Primary Focus Region):** Territories include `Southeast-ATL`, `Mid-Atlantic-VA`, `Northeast-NY`.
- **`NA-Central` (Comparison Region):** Territories include `Midwest-IL`, `GreatLakes-MI`, `Texas-DFW`.
- **`NA-West` (Comparison Region):** Territories include `PacificNW-WA`, `California-LA`, `Mountain-CO`.

### 3.2 Product Lines & SKUs
- **`SKU-8821` (High-Performance Industrial Fluid):** Unit list price $\$120.00$, material standard cost $\$58.00$. Primary revenue driver subject to regional stockout and competitor pressure.
- **`SKU-4410` (Standard Commercial Fluid):** Unit list price $\$85.00$, material cost $\$46.00$.
- **`SKU-5520` (Eco-Line Synthetic Blend):** Unit list price $\$110.00$, material cost $\$55.00$.
- **`SKU-9930` (Heavy-Duty Transmission Oil):** Unit list price $\$150.00$, material cost $\$72.00$.
- **`SKU-2205` (Precision Hydraulic Sealant):** Unit list price $\$65.00$, material cost $\$30.00$.

### 3.3 Distribution Centers (DCs)
- **`Atlanta-DC-01` (Atlanta, GA — NA-East):** Regional hub servicing Southeast and Mid-Atlantic.
- **`Charlotte-DC-02` (Charlotte, NC — NA-East):** Secondary hub used for emergency stock re-routing.
- **`Chicago-DC-01` (Chicago, IL — NA-Central)**
- **`Dallas-DC-02` (Dallas, TX — NA-Central)**
- **`Reno-DC-01` (Reno, NV — NA-West)**
- **`Seattle-DC-02` (Seattle, WA — NA-West)**

### 3.4 Authorized Distributors
- **Tier 1 Strategic:** `DIST-APEX-EAST`, `DIST-MIDATL-SUPPLY`, `DIST-EMPIRE-IND`, `DIST-MIDWEST-DIRECT`, `DIST-TEXAS-COMMERCIAL`, `DIST-PACIFIC-LOGISTICS`, `DIST-CAL-ENTERPRISE`.
- **Tier 2 Regional:** `DIST-COASTAL-WHOLESALE`, `DIST-SUNBELT-PARTS`, `DIST-GREATLAKES-SUPPLY`, `DIST-MOUNTAIN-PARTS`.
- **Tier 3 Local:** `DIST-TRI-STATE-OPS`.

---

## 4. Dataset Catalog & Schema Conformance

| Dataset File | Domain | Row Count | Primary Key | Key Schema Properties |
|---|---|---|---|---|
| [`revenue.csv`](file:///c:/Users/hp/Downloads/New%20folder%20(11)/data/raw/revenue.csv) | ERP | 12,322 | `invoice_id` | `invoice_date`, `region`, `customer_id`, `sku_id`, `gross_amount`, `discount_amount`, `net_revenue`, `posting_status` |
| [`inventory.csv`](file:///c:/Users/hp/Downloads/New%20folder%20(11)/data/raw/inventory.csv) | ERP | 13,710 | `snapshot_id` | `snapshot_date`, `dc_location`, `region`, `sku_id`, `on_hand_units`, `available_units`, `required_demand_units`, `availability_percentage`, `stockout_status` |
| [`margin.csv`](file:///c:/Users/hp/Downloads/New%20folder%20(11)/data/raw/margin.csv) | ERP | 75 | `margin_record_id` | `fiscal_period`, `region`, `sku_id`, `sales_revenue`, `cogs_material`, `cogs_freight_expedited`, `total_cogs`, `gross_profit`, `gross_margin_percentage` |
| [`sales.csv`](file:///c:/Users/hp/Downloads/New%20folder%20(11)/data/raw/sales.csv) | CRM/Sales | 12,344 | `sales_item_id` | `order_id`, `transaction_date`, `region`, `distributor_id`, `sku_id`, `units_ordered`, `units_sold`, `unit_price`, `total_item_revenue`, `delivery_status` |
| [`distributor_orders.csv`](file:///c:/Users/hp/Downloads/New%20folder%20(11)/data/raw/distributor_orders.csv) | CRM/Sales | 1,640 | `po_id` | `order_date`, `region`, `distributor_id`, `distributor_tier`, `total_order_value`, `order_status`, `deferral_reason`, `expected_delivery_date` |
| [`support_tickets.csv`](file:///c:/Users/hp/Downloads/New%20folder%20(11)/data/raw/support_tickets.csv) | Support | 2,856 | `ticket_id` | `created_at`, `region`, `source_entity`, `category`, `severity`, `subject`, `content_summary`, `sentiment_score` |
| [`distributor_communications.csv`](file:///c:/Users/hp/Downloads/New%20folder%20(11)/data/raw/distributor_communications.csv) | Support | 39 | `comm_id` | `sent_at`, `sender`, `recipient`, `subject`, `key_extracted_claims`, `urgency` |
| [`market_intelligence.csv`](file:///c:/Users/hp/Downloads/New%20folder%20(11)/data/raw/market_intelligence.csv) | Market Intel | 12 | `report_id` | `captured_date`, `competitor_name`, `competing_product`, `target_geography`, `promotional_action`, `observed_price_usd`, `baseline_price_usd`, `source_channel` |

---

## 5. Observable Operational Scenario Signals

The raw data organically exhibits signals corresponding to the primary investigation scenario without artificial labeling:

1. **Supply Chain Disruption at Atlanta DC:**
   - Between `2026-08-01` and `2026-08-19`, daily snapshots for `Atlanta-DC-01` show available inventory dropping to an average of $79.4\%$ (and $\sim 72\%$ specifically for `SKU-8821`) with `stockout_status = true` and replenishment delays.
2. **Sales Unit Suppression on SKU-8821:**
   - In Q3 2026, delivery fulfillment status shows partial shipments and backorders, reducing recognized sales units of SKU-8821 by over $31\%$.
3. **Wholesale Channel Purchase Order Deferrals:**
   - Tier-1 distributors (`DIST-APEX-EAST`, `DIST-MIDATL-SUPPLY`) log $29$ deferred purchase orders in August 2026 citing delivery uncertainty and competitor promotions.
4. **Competitor Pricing Incursion:**
   - Scraped reports between July 22 and August 19, 2026 record `Horizon Foods Ltd.` offering a $15\%$ promotional price cut on `Horizon PurePro 500` ($\$102.00$ vs $\$120.00$) across the Mid-Atlantic corridor.
5. **Customer Support & Email Sentiment Signals:**
   - An escalation spike of $67$ stockout and fulfillment complaint tickets (sentiment scores between $-0.60$ and $-0.95$) and high-urgency distributor communications demanding emergency freight transfers.

---

## 6. Dataset Validation

Automated validation suite is available at `tests/validate_dataset.py`:
```bash
python tests/validate_dataset.py
```
Validates JSON schema alignment, primary key uniqueness, foreign key consistency, numerical boundaries, scenario signal presence, and mathematical target revenue variance ($-7.97\%$).
