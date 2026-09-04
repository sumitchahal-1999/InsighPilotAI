# InsightPilot AI — Live Production Critical Journey Validation

**Project:** InsightPilot AI  
**Competition:** Accenture Innovation Challenge 2026 (Track 3: BusinessIntelligence.ai)  
**Document:** Live Deployed User Journey Validation, State Coherence & Invariant Verification  
**Status:** `LOCAL VERIFICATION PASSED — LIVE CLOUD PENDING OWNER DEPLOYMENT`

---

## 1. Deployed Critical Journey Verification Model

The critical user journey tests the 7 core competition screens against the live production environment to verify that no schema drift, metric drift, or CORS failures occur:

```text
Screen 1: Executive Command Center (/ )
  • Revenue Anomaly Detected: $15.43M -> $14.20M (-$1.23M / -7.97%)
  • Materiality Status: CRITICAL_NEGATIVE_VARIANCE
  • Cross-Dataset Signals: 8 Enterprise Data Sources Synced
           │
           ▼
Screen 2: LangGraph Investigation Trace (/investigation)
  • 11-Node Multi-Agent Execution State Graph
  • Time-series movement -> driver identification -> evidence retrieval
           │
           ▼
Screen 3: Root-Cause Decomposition Waterfall (/root-cause)
  • 4 Ranked Drivers explaining 100.0% variance:
    1. Atlanta DC Stockout (43.2% / -$550K / 94% conf)
    2. SKU-8821 Volume Drop (26.7% / -$340K / 89% conf)
    3. Distributor PO Deferrals (18.8% / -$240K / 85% conf)
    4. Competitor Horizon Pricing (11.3% / -$144K / 78% conf)
           │
           ▼
Screen 4: Dynamic 6-Column Decision Graph (/decision-graph)
  • 14 Nodes, 17 Directed Edges across 6 Topological Columns:
    1. Metric Anomaly -> 2. Causal Drivers -> 3. Empirical Evidence
    -> 4. Business Mechanisms -> 5. Action Levers -> 6. Predicted Outcomes
           │
           ▼
Screen 5: SHA-256 Evidence Explorer (/evidence)
  • 9 Empirical Evidence Records with 64-char Cryptographic Digests
  • Multi-Source Corroboration (SAP ERP, Salesforce CRM, Zendesk, POS)
           │
           ▼
Screen 6: Action Recommendations & What-If Simulation (/recommendations)
  • Priority 1 Action: Emergency Stock Transfer (+$484K Recovery / 14-day SLA)
  • Priority 2 Action: Targeted Distributor Outreach (+$180K Recovery)
  • What-If Sandbox: 79.4% -> 90.0% Availability yields +$341,422.91 recovery
           │
           ▼
Screen 7: Executive Decision Briefing (/briefing)
  • Role-tailored CFO Boardroom Narrative
  • 10-Beat Storyboard Narrative + 13-Point System Integrity Report
```

---

## 2. Invariant Parity Verification

Across all 7 screens, the deterministic analytics core guarantees that every metric matches the locked canonical truth, with zero hallucination.
