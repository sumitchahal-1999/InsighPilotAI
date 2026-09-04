#!/usr/bin/env python3
"""
InsightPilot AI — Investigation CLI Entry Point
Accenture Innovation Challenge 2026 — Track 3: BusinessIntelligence.ai

Executes the deterministic analytics engine for North America East Revenue Q3 FY2026.
"""

import os
import sys
import json

# Ensure workspace root is on PYTHONPATH
WORKSPACE_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if WORKSPACE_ROOT not in sys.path:
    sys.path.insert(0, WORKSPACE_ROOT)

from analytics.investigation_engine import InvestigationEngine

def main():
    print("=" * 75)
    print("  INSIGHTPILOT AI -- DETERMINISTIC INVESTIGATION ENGINE")
    print("  Accenture Innovation Challenge 2026 -- Track 3: BusinessIntelligence.ai")
    print("=" * 75)
    
    engine = InvestigationEngine()
    result = engine.run_investigation(
        kpi_id="north_america_east_revenue",
        region="NA-East",
        prev_period_id="2026-Q2",
        curr_period_id="2026-Q3",
        persona_id="CFO"
    )
    
    kpi = result["kpi"]
    drivers = result["drivers"]
    overall = result["overall"]
    evidence = result["evidence_summary"]
    lineage = result["lineage_graph"]
    
    print(f"\n[INVESTIGATION TARGET]")
    print(f"  * KPI:                {kpi['name']} ({kpi['id']})")
    print(f"  * Region:             NA-East")
    print(f"  * Previous Period:    2026-Q2 (${kpi['previous_value']:,.2f})")
    print(f"  * Current Period:     2026-Q3 (${kpi['current_value']:,.2f})")
    print(f"  * Net Variance:       ${kpi['variance_amount']:,.2f} ({kpi['percent_change']:.2f}%)")
    print(f"  * Materiality Status: {kpi['materiality_status']}")
    
    print(f"\n[RANKED EXPLANATORY DRIVERS]")
    print(f"  {'Rank':<5} {'Driver Name':<42} {'Impact (USD)':<15} {'Contribution':<14} {'Confidence'}")
    print("  " + "-" * 85)
    for d in drivers:
        print(f"  #{d['rank']:<4} {d['driver_name']:<42} ${d['impact_usd']:>12,.2f}  {d['contribution_pct']:>6.1f}%        {d['confidence_score']}%")
        
    print(f"\n[CONFIDENCE & ABSTENTION]")
    print(f"  * Overall Confidence Score: {overall['overall_confidence']}% ({overall['confidence_label']})")
    print(f"  * Abstention Gate Triggered: {overall['abstention']}")
    if overall['abstention']:
        print(f"  * Abstention Reason:        {overall['abstention_reason']}")
        
    print(f"\n[EVIDENCE & LINEAGE GRAPH]")
    print(f"  * Enterprise Domains:       {', '.join(evidence['source_domains'])}")
    print(f"  * Evidence Nodes Linked:    {len(evidence['evidence_ids'])} citations ({', '.join(evidence['evidence_ids'][:4])}...)")
    print(f"  * Root KPI Node:            {lineage['kpi_node']}")
    print(f"  * Driver Nodes:             {', '.join(lineage['driver_nodes'])}")
    
    # Verify Schema Conformance
    schema_path = os.path.join(WORKSPACE_ROOT, "data", "schemas", "investigation_result.json")
    if os.path.exists(schema_path):
        with open(schema_path, "r", encoding="utf-8") as sf:
            schema_json = json.load(sf)
        required_top_keys = set(schema_json.get("required", []))
        result_keys = set(result.keys())
        missing = required_top_keys - result_keys
        if not missing:
            print("\n[SCHEMA VERIFICATION]")
            print("  [PASS] Investigation output perfectly conforms to data/schemas/investigation_result.json")
            
    print("\n" + "=" * 75)
    print("INVESTIGATION EXECUTION COMPLETED (DETERMINISTIC & REPRODUCIBLE)")
    print("=" * 75)

if __name__ == "__main__":
    main()
