# InsightPilot AI — Gemini Grounded Reasoning Architecture

> **Accenture Innovation Challenge 2026 — Track 3: BusinessIntelligence.ai**  
> **Document Version:** 2.0.0  
> **Status:** Production-Ready Reasoning Layer (Step 8)  
> **Role:** Technical Authority on Grounded LLM Inference, Persona Adaptation & Hallucination Prevention

---

## 1. Architectural Principle: Separation of Quantitative Truth and AI Narrative

InsightPilot AI strictly separates quantitative numerical calculation from generative language reasoning. **Gemini is never used as an arithmetic engine, database, or speculative forecasting tool.**

```mermaid
flowchart TD
    subgraph UI_Layer [1. User / Future Stitch Frontend]
        REQ[Executive User Request: POST /api/v1/ai/investigations/{kpi_id}/explanation]
    end

    subgraph Deterministic_Core [2. Authoritative Deterministic Engine (Steps 4-6)]
        CSV[(Raw Datasets in data/raw/)] --> KPI_ENG[KPI Engine: Variance & Materiality]
        CSV --> DRV_ENG[Driver Engine: Multi-Factor Breakdown]
        CSV --> EV_ENG[Evidence Engine: 5-Layer Cryptographic Lineage]
        KPI_ENG & DRV_ENG & EV_ENG --> DET_RES[Authoritative Investigation Result & Evidence List]
    end

    subgraph AI_Reasoning_Layer [3. Grounded Gemini Layer (Step 8)]
        DET_RES --> CTX[GroundedContextBuilder: Structured Compact Facts]
        CTX --> PRM[Prompt Templating: Directives & Persona Profile]
        PRM --> GEMINI[GeminiClient: Official Google GenAI SDK (gemini-2.5-flash)]
        GEMINI --> RAW_JSON[Raw JSON Response + Telemetry]
        RAW_JSON --> VAL[GroundingValidator: Strict Evidence & Fact Check]
        VAL --> TYPED_RESP[Structured Pydantic AIExplanationResponse]
    end

    REQ --> DET_RES
    TYPED_RESP --> REQ
```

### Absolute Governance Boundaries:
| Responsibility | Owned By | Mechanism |
|---|---|---|
| **KPI Values & Historical Baselines** | Deterministic Engine | Raw ERP Invoiced Sales aggregation (`analytics/kpi_engine.py`) |
| **Variance & Movement %** | Deterministic Engine | Exact percentage change formula ($\Delta\% = \frac{Curr - Prev}{Prev} \times 100$) |
| **Driver Ranking & Monetary Impacts** | Deterministic Engine | Multi-factor operational signal decomposition (`analytics/driver_engine.py`) |
| **Confidence Scoring & Abstention** | Deterministic Engine | Multi-factor weighted confidence gate (`analytics/confidence_engine.py`) |
| **Evidence Extraction & Audit Hashes** | Evidence Engine | SHA-256 canonical source hashing (`evidence/evidence_engine.py`) |
| **Executive Synthesis & Narrative** | **Gemini LLM Layer** | Structured JSON generation grounded strictly on deterministic context |
| **Persona Stylistic Adaptation** | **Gemini LLM Layer** | Strategic CFO vs Operational Sales Manager narrative emphasis |

---

## 2. Gemini SDK & Model Configuration

- **SDK:** Official Google GenAI SDK (`from google import genai`)
- **Default Model:** `gemini-2.5-flash` (Configurable via `GEMINI_MODEL` environment variable)
- **Temperature:** `0.1` (Minimizes randomness, maximizes factual consistency)
- **Response Format:** `response_mime_type="application/json"` with schema enforcement
- **Credential Handling:** Ingested strictly via `GEMINI_API_KEY` from environment; never logged, exposed in APIs, or committed to Git.

---

## 3. Structured Grounded Context

Before calling Gemini, `GroundedContextBuilder` creates an authoritative, compact representation containing only verified facts:

```json
{
  "investigation_id": "INV-EXEC-2026-NAE-001",
  "kpi": {
    "id": "north_america_east_revenue",
    "name": "North America East Revenue",
    "current_value": 14200000.05,
    "previous_value": 15430000.06,
    "variance_amount": -1230000.01,
    "percent_change": -7.97,
    "materiality_status": "CRITICAL_NEGATIVE_VARIANCE"
  },
  "drivers": [
    {
      "driver_id": "atlanta_dc_stockout",
      "driver_name": "Atlanta DC Stockout",
      "rank": 1,
      "contribution_pct": 43.2,
      "impact_usd": -550000.0,
      "confidence_score": 94,
      "evidence_ids": ["EVID_ERP_ATL_STOCKOUT_001", "EVID_ERP_TRANSFER_LOG_002", "EVID_ZENDESK_ATL_DELAY_003"]
    }
  ],
  "evidence": [
    {
      "evidence_id": "EVID_ERP_ATL_STOCKOUT_001",
      "supports_driver": "atlanta_dc_stockout",
      "source_system": "SAP S/4HANA Supply Chain Logistics (MM-WM)",
      "source_record_id": "INV-SNAP-21971",
      "finding_summary": "Atlanta-DC-01 availability fell to 68.2% for SKU-8821 with 1,986 available vs 2,912 required.",
      "confidence_score": 94
    }
  ],
  "overall_confidence": {
    "score": 89,
    "label": "HIGH",
    "abstention": false
  },
  "persona": {
    "persona_name": "CFO",
    "role_title": "Chief Financial Officer",
    "focus_areas": ["Revenue and gross margin variance", "Financial exposure", "EBITDA risk"],
    "tone": "Strategic, financially rigorous, high-level, and decision-oriented"
  }
}
```

---

## 4. Persona Adaptation

The engine adapts narrative framing based on the requesting persona while keeping the underlying quantitative ground truth identical:

1. **Chief Financial Officer (`CFO`):**
   - *Focal Area:* Topline revenue shortfall ($-\$1.23\text{M}$), margin compression ($-3.20\text{ pts}$), emergency freight exposure ($\$291\text{k}$), and EBITDA impact.
   - *Tone:* Strategic, executive, governance-oriented.
2. **Regional Sales Manager (`REGIONAL_SALES_MANAGER`):**
   - *Focal Area:* Warehouse fulfillment rates ($68.2\%$), distributor purchase order deferrals ($29$ deferred POs), backordered SKU delivery items, and local competitive discounting.
   - *Tone:* Operational, account-centric, tactical execution.

---

## 5. Post-Generation Grounding Validator

The `GroundingValidator` executes strict verification rules before returning responses:
1. **Evidence ID Whitelist Check:** Asserts that every ID in `grounded_evidence_ids` exists in the input context. Rejects hallucinated IDs with `422 AI_GROUNDING_FAILED`.
2. **Abstention Integrity Check:** If the deterministic investigation triggered `abstention: true` or confidence $<65\%$, asserts that the generated narrative explicitly communicates uncertainty and refuses false confidence.
3. **Empty Evidence Constraint:** If zero evidence records were retrieved, asserts that the model cites zero evidence IDs.

---

## 6. Telemetry & Cost Monitoring

Every AI response includes transparent execution metadata:
```json
{
  "model": "gemini-2.5-flash",
  "generated_at": "2026-08-22T13:30:00Z",
  "latency_ms": 742.5,
  "prompt_tokens": 420,
  "completion_tokens": 185,
  "total_tokens": 605,
  "grounded_evidence_count": 3,
  "validation_status": "VERIFIED_GROUNDED"
}
```

---

## 7. Graceful Fallback & Availability

If `GEMINI_API_KEY` is not present or the Gemini service is unreachable:
- The endpoint returns `503 Service Unavailable` with `code: AI_SERVICE_UNAVAILABLE`.
- **All deterministic endpoints (`/kpis`, `/investigations`, `/evidence`, `/lineage`) remain 100% functional and available.**
- Zero mock/fabricated AI results are emitted without active verification.
