# InsightPilot AI — Live 7-Screen User Journey Report

**Project:** InsightPilot AI  
**Competition:** Accenture Innovation Challenge 2026 (Track 3: BusinessIntelligence.ai)  
**Document:** 7-Screen End-to-End User Journey Audit, State Coherence & Invariant Verification  
**Status:** `LOCAL VERIFICATION PASSED — LIVE CLOUD PENDING OWNER DEPLOYMENT`

---

## 1. 7-Screen Verification Audit Table

```text
================================================================================
                    7-SCREEN LIVE USER JOURNEY AUDIT
================================================================================
```

### Screen 1: Executive Command Center
- **Route:** `/`
- **Expected Result:** Renders KPI overview with North America East Revenue highlighted as critical anomaly.
- **Actual Result (Local):** Anomaly banner displayed: `$15,430,000.06` $\to$ `$14,200,000.05` (`-$1,230,000.01` / `-7.97%`).
- **Canonical Metric Verified:** `$15.43M -> $14.20M (-7.97%)`
- **Deployment Environment:** Local Runtime (`PASS`) | Live Cloud (`NOT EXECUTED — DEPLOYMENT UNAVAILABLE`)

### Screen 2: Root-Cause Waterfall Decomposition
- **Route:** `/root-cause`
- **Expected Result:** 4 ranked causal drivers explaining exactly 100.0% of the variance.
- **Actual Result (Local):** 1. Atlanta DC Stockout (43.2% / -$550K), 2. SKU-8821 (26.7% / -$340K), 3. PO Deferrals (18.8% / -$240K), 4. Competitor Pricing (11.3% / -$144K).
- **Canonical Metric Verified:** `100.0% Total Explained Variance, 89% HIGH Confidence`
- **Deployment Environment:** Local Runtime (`PASS`) | Live Cloud (`NOT EXECUTED — DEPLOYMENT UNAVAILABLE`)

### Screen 3: LangGraph Investigation Trace
- **Route:** `/investigation`
- **Expected Result:** 11-node state graph lifecycle trace displaying multi-agent reasoning steps.
- **Actual Result (Local):** All 11 nodes render with execution latency and state payloads.
- **Canonical Metric Verified:** `11-Node Lifecycle Graph`
- **Deployment Environment:** Local Runtime (`PASS`) | Live Cloud (`NOT EXECUTED — DEPLOYMENT UNAVAILABLE`)

### Screen 4: Dynamic 6-Column Decision Graph
- **Route:** `/decision-graph`
- **Expected Result:** Interactive topology graph with 14 nodes and 17 edges across 6 structural columns.
- **Actual Result (Local):** 14 nodes and 17 edges render cleanly with interactive node inspectors.
- **Canonical Metric Verified:** `14 Nodes, 17 Edges, 6 Columns`
- **Deployment Environment:** Local Runtime (`PASS`) | Live Cloud (`NOT EXECUTED — DEPLOYMENT UNAVAILABLE`)

### Screen 5: SHA-256 Evidence Explorer
- **Route:** `/evidence`
- **Expected Result:** 9 empirical evidence records with 64-character SHA-256 hashes and cross-system corroboration.
- **Actual Result (Local):** 9 records rendered with full cryptographic lineage and data source tags.
- **Canonical Metric Verified:** `9 Empirical Evidence Records with SHA-256 Lineage`
- **Deployment Environment:** Local Runtime (`PASS`) | Live Cloud (`NOT EXECUTED — DEPLOYMENT UNAVAILABLE`)

### Screen 6: Recommendations & What-If Simulation
- **Route:** `/recommendations`
- **Expected Result:** Priority 1 action (+$484K recovery) and interactive What-If slider (79.4% $\to$ 90% $\to$ +$341.4K).
- **Actual Result (Local):** Priority 1 stock transfer active; simulation recalculates instantly ($32,209.71/pt).
- **Canonical Metric Verified:** `+$484,000.00 Recovery (14-day SLA), +$341,422.91 Simulation`
- **Deployment Environment:** Local Runtime (`PASS`) | Live Cloud (`NOT EXECUTED — DEPLOYMENT UNAVAILABLE`)

### Screen 7: Executive Decision Briefing
- **Route:** `/briefing`
- **Expected Result:** Role-tailored CFO briefing narrative with 10-beat storyboard and 13-point integrity audit.
- **Actual Result (Local):** Complete executive brief formatted with grounded figures and abstention status.
- **Canonical Metric Verified:** `10-Beat Storyboard Narrative & System Integrity Report`
- **Deployment Environment:** Local Runtime (`PASS`) | Live Cloud (`NOT EXECUTED — DEPLOYMENT UNAVAILABLE`)
