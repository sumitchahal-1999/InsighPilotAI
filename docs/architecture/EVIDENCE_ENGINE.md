# InsightPilot AI — Evidence Retrieval & Lineage Engine Specification

> **Accenture Innovation Challenge 2026 — Track 3: BusinessIntelligence.ai**  
> **Document Version:** 2.0.0  
> **Status:** Production-Ready Explainability Layer (Step 6)  
> **Role:** Technical Authority on Evidence Extraction, Ranking & Cryptographic Audit Lineage

---

## 1. Executive Summary & Explainability Principle

The **Evidence and Lineage Engine** (`evidence/`) is the deterministic explainability layer of InsightPilot AI. It answers the fundamental enterprise question: **"Why should leadership trust this analytical conclusion?"**

Rather than relying on black-box LLM hallucinations or static mock cards, the engine retrieves concrete, immutable evidence records from the underlying enterprise datasets and establishes an unbroken 5-layer lineage path:

$$\text{Root KPI} \longrightarrow \text{Analytical Driver} \longrightarrow \text{Evidence Node} \longrightarrow \text{Enterprise Source System} \longrightarrow \text{Raw Record ID}$$

```mermaid
flowchart TD
    subgraph Analytics Layer [1. Deterministic Analytical Truth]
        KPI[Root KPI: NA-East Revenue -7.97%]
        DRV1[Driver #1: Atlanta DC Stockout 43.2%]
        DRV2[Driver #2: SKU-8821 Sales Volume 26.7%]
        DRV3[Driver #3: Distributor Orders 18.8%]
        DRV4[Driver #4: Competitor Horizon Pricing 11.3%]
        KPI --> DRV1 & DRV2 & DRV3 & DRV4
    end

    subgraph Evidence Layer [2. Evidence Retrieval & Ranking (evidence/)]
        DRV1 --> EV1[EVID_ERP_ATL_STOCKOUT_001<br>Telemetry Log: 68.2% Avail]
        DRV1 --> EV2[EVID_ERP_TRANSFER_LOG_002<br>Ledger: $291k Expedited Freight]
        DRV1 --> EV3[EVID_ZENDESK_ATL_DELAY_003<br>Ticket: Sunbelt Parts Escalation]
        DRV2 --> EV4[EVID_CRM_SKU8821_SALES_004<br>Sales Order: Partial Delivery]
        DRV2 --> EV5[EVID_ERP_BOM_MARGIN_005<br>COPA Ledger: Margin 42.5%]
        DRV3 --> EV6[EVID_CRM_PO_DEF_006<br>Purchase Order: Deferred Status]
        DRV3 --> EV7[EVID_COMM_DIST_EMAIL_007<br>Email: Apex Reorder Hold]
        DRV4 --> EV8[EVID_MKT_HORIZON_PROMO_008<br>Scrape: 15% Horizon Promo]
        DRV4 --> EV9[EVID_ZENDESK_COMP_FEEDBACK_009<br>Ticket: Price Match Request]
    end

    subgraph Lineage Layer [3. Cryptographic Lineage & Audit]
        EV1 --> REC1[(inventory.csv / INV-SNAP-21971<br>sha256:c7ba...)]
        EV2 --> REC2[(margin.csv / MRG-1062<br>sha256:2d03...)]
        EV3 --> REC3[(support_tickets.csv / ZD-TK-3376<br>sha256:9cbc...)]
        EV4 --> REC4[(sales.csv / SLS-510712<br>sha256:6771...)]
        EV6 --> REC5[(distributor_orders.csv / PO-DIST-2418<br>sha256:65ed...)]
        EV7 --> REC6[(distributor_communications.csv / COMM-EMAIL-101<br>sha256:0ec9...)]
        EV8 --> REC7[(market_intelligence.csv / MKT-INTEL-101<br>sha256:4076...)]
    end
```

---

## 2. Multi-Domain Evidence Retrieval Methodology

The engine queries all 8 raw CSV datasets across three enterprise domains, extracting verified records that substantiate each analytical driver:

### 2.1 Driver 1: Atlanta DC Stockout (`atlanta_dc_stockout`)
1. **`EVID_ERP_ATL_STOCKOUT_001` (ERP Telemetry Log):**
   - *Source System:* SAP S/4HANA Supply Chain Logistics (`inventory.csv` / `INV-SNAP-21971`).
   - *Finding:* Atlanta-DC-01 inventory availability dropped to $68.2\%$ for `SKU-8821` on August 5, 2026 ($1,986$ available vs $2,912$ required demand units).
   - *Method:* DC Stockout Duration & Demand Gap Analysis ($94\%$ confidence).
2. **`EVID_ERP_TRANSFER_LOG_002` (ERP Transaction Record):**
   - *Source System:* SAP COPA Margin & Profitability Ledger (`margin.csv` / `MRG-1062`).
   - *Finding:* Emergency expedited freight allocations spiked to $\$291,183.12$ for `SKU-8821` due to inter-DC stock transfers from Charlotte DC to Atlanta Hub.
   - *Method:* Expedited Logistics Variance Allocation ($92\%$ confidence).
3. **`EVID_ZENDESK_ATL_DELAY_003` (Customer Signal):**
   - *Source System:* Zendesk Customer Service Desk (`support_tickets.csv` / `ZD-TK-3376`).
   - *Finding:* Tier-2 distributor `DIST-SUNBELT-PARTS` logged a `HIGH` severity complaint regarding Atlanta DC stockout impacting SKU-8821 with negative sentiment score $-0.60$.
   - *Method:* NLP Complaint Cluster & Sentiment Extraction ($90\%$ confidence).

---

### 2.2 Driver 2: SKU-8821 Sales Volume Drop (`sku_8821_sales_volume`)
1. **`EVID_CRM_SKU8821_SALES_004` (CRM Transaction Record):**
   - *Source System:* Salesforce Sales Cloud Fulfillment Ledger (`sales.csv` / `SLS-510712`).
   - *Finding:* Sales order line item `SO-710711` experienced `PARTIAL` delivery ($95$ units delivered of $145$ ordered).
   - *Method:* Order Fulfillment Line Item Audit ($89\%$ confidence).
2. **`EVID_ERP_BOM_MARGIN_005` (ERP Transaction Record):**
   - *Source System:* SAP COPA Profitability Analysis (`margin.csv` / `MRG-1062`).
   - *Finding:* SKU-8821 quarterly recognized revenue fell to $\$3,176,208.54$ with gross margin compressing to $42.5\%$.
   - *Method:* Product Gross Margin Contribution Decomposition ($88\%$ confidence).

---

### 2.3 Driver 3: Distributor Orders Deferral (`distributor_orders`)
1. **`EVID_CRM_PO_DEF_006` (CRM Transaction Record):**
   - *Source System:* Salesforce Partner Portal & PO Management (`distributor_orders.csv` / `PO-DIST-2418`).
   - *Finding:* Purchase order `PO-DIST-2418` ($\$181,363.00$) for Tier-1 distributor `DIST-APEX-EAST` was marked `DEFERRED` citing *"Holding purchase order pending fulfillment assurance on SKU-8821"*.
   - *Method:* Wholesale PO Lifecycle Tracking ($85\%$ confidence).
2. **`EVID_COMM_DIST_EMAIL_007` (Communication Extract):**
   - *Source System:* Enterprise Email Ingestion Pipeline (`distributor_communications.csv` / `COMM-EMAIL-101`).
   - *Finding:* Distributor procurement director email from `procurement@apexdistributors.com` regarding holding 24,000 unit order for SKU-8821 and noting Horizon Foods 15% discount offer.
   - *Method:* Structured Communication NLP Extraction ($84\%$ confidence).

---

### 2.4 Driver 4: Competitor Horizon Foods Price Cut (`competitor_horizon_pricing`)
1. **`EVID_MKT_HORIZON_PROMO_008` (Market Observation):**
   - *Source System:* Wholesale Market Pricing Intelligence Feed (`market_intelligence.csv` / `MKT-INTEL-101`).
   - *Finding:* Competitive scrape captured on July 22, 2026 recorded Horizon Foods offering a $15\%$ promotional price cut on `Horizon PurePro 500` ($\$102.00$ vs list $\$120.00$) across the Mid-Atlantic corridor.
   - *Method:* Competitive Price Scraping & Parity Indexing ($78\%$ confidence).
2. **`EVID_ZENDESK_COMP_FEEDBACK_009` (Customer Signal):**
   - *Source System:* Zendesk Customer Service Desk (`support_tickets.csv` / `ZD-TK-1001`).
   - *Finding:* Price matching inquiry logged by wholesale account referencing competitor promotional terms.
   - *Method:* Price Escalation Feedback Mining ($76\%$ confidence).

---

## 3. Deterministic Evidence Ranking Methodology

The engine ranks retrieved evidence items per driver using a composite formula based on objective characteristics:

$$\text{Ranking Score} = (\text{Confidence Score} \times 0.50) + (\text{Directness Weight} \times 100 \times 0.30) + (\text{Freshness Weight} \times 100 \times 0.20)$$

| Directness Dimension | Evidence Type | Directness Weight |
|---|---|---|
| **Direct Hardware/Database Telemetry** | `TELEMETRY_LOG` | $1.00$ |
| **Financial/ERP Ledger Entry** | `TRANSACTION_RECORD` | $0.95$ |
| **Customer Support Ticket** | `CUSTOMER_SIGNAL` | $0.85$ |
| **Partner Email / Communication** | `COMMUNICATION_EXTRACT` | $0.80$ |
| **Market Scraped Observation** | `MARKET_OBSERVATION` | $0.75$ |

- **Tie-Breaking:** Broken deterministically by alphanumeric sorting on `evidence_id`.

---

## 4. Freshness Classification Policy

Freshness status is computed relative to the reporting evaluation timestamp:
- **`LIVE`:** Event occurred within $\le 14$ days ($\le 336$ hours). Freshness weight = $1.00$.
- **`RECENT`:** Event occurred within $15 - 60$ days ($336 - 1,440$ hours). Freshness weight = $0.90$.
- **`STALE`:** Event occurred $> 60$ days ago ($> 1,440$ hours). Freshness weight = $0.70$.

---

## 5. Cryptographic Lineage & Audit Hashes

Every evidence item includes an immutable `lineage` payload containing:
- `source_table`: Underlying database table / dataset name.
- `pipeline_job_id`: Official ETL batch/stream ingestion identifier.
- `verification_hash`: Deterministic SHA-256 hash calculated over the sorted, canonical JSON representation of the raw record:
  $$\text{verification\_hash} = \text{"sha256:"} + \text{SHA256}(\text{CanonicalJSON}(\text{raw\_record}))$$

---

## 6. Insufficient Evidence Handling

If an analytical driver has zero supporting source records in the repository:
- `evidence_status = "INSUFFICIENT"`
- `evidence_count = 0`
- `reason = "No corroborating source records found for driver '{driver_id}'."`
- The system prevents false attribution and reports missing audit references explicitly.

---

## 7. Limitations & Mathematical Disclaimer

> **Explainability Notice:** Evidence nodes provide **verifiable empirical substantiation** for analytical findings. They prove that operational disruptions, customer complaints, order deferrals, and price incursions occurred in enterprise systems; they do not imply that correlation alone establishes sole causal exclusivity.
