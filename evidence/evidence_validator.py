"""
InsightPilot AI — Evidence Contract Validator
Validates evidence nodes against schema definitions and verifies source record existence.
"""

from typing import List, Dict, Any
from evidence.evidence_loader import EvidenceLoader

class EvidenceValidator:
    """Validates structural contract conformance and cross-references source records."""
    
    REQUIRED_FIELDS = [
        "evidence_id",
        "source",
        "source_record_id",
        "source_domain",
        "timestamp",
        "freshness",
        "evidence_type",
        "analytical_method",
        "contribution",
        "confidence",
        "supports_driver",
        "supports_kpi",
        "lineage"
    ]

    def __init__(self, loader: EvidenceLoader):
        self.loader = loader

    def validate_evidence_item(self, item: Dict[str, Any], table_name: str) -> Dict[str, Any]:
        """Validates a single evidence item for completeness and source record traceability."""
        missing = [f for f in self.REQUIRED_FIELDS if f not in item]
        if missing:
            raise ValueError(f"Evidence item {item.get('evidence_id')} missing required fields: {missing}")
            
        # Check freshness structure
        freshness = item.get("freshness", {})
        if "age_hours" not in freshness or "status" not in freshness:
            raise ValueError(f"Evidence {item.get('evidence_id')} invalid freshness object: {freshness}")
            
        # Check contribution structure
        contrib = item.get("contribution", {})
        if "percentage" not in contrib or "monetary_impact_usd" not in contrib:
            raise ValueError(f"Evidence {item.get('evidence_id')} invalid contribution object: {contrib}")
            
        # Check lineage structure
        lineage = item.get("lineage", {})
        if "source_table" not in lineage or "pipeline_job_id" not in lineage or "verification_hash" not in lineage:
            raise ValueError(f"Evidence {item.get('evidence_id')} invalid lineage object: {lineage}")
            
        # Verify source record existence
        record_id = item["source_record_id"]
        source_rec = self.loader.find_record(table_name, record_id)
        if not source_rec:
            raise ValueError(f"Traceability Error: Record {record_id} not found in table {table_name}")
            
        return item

    def check_driver_evidence_sufficiency(self, driver_id: str, evidence_list: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Evaluates whether retrieved evidence is sufficient for decision explainability."""
        if not evidence_list:
            return {
                "driver_id": driver_id,
                "evidence_status": "INSUFFICIENT",
                "evidence_count": 0,
                "reason": f"No corroborating source records found for driver '{driver_id}'."
            }
        return {
            "driver_id": driver_id,
            "evidence_status": "SUFFICIENT",
            "evidence_count": len(evidence_list),
            "reason": f"Found {len(evidence_list)} corroborating source records."
        }
