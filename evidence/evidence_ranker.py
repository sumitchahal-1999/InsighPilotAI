"""
InsightPilot AI — Deterministic Evidence Ranker
Ranks retrieved evidence nodes using transparent multi-criteria scoring without ML or LLMs.
"""

from typing import List, Dict, Any

class EvidenceRanker:
    """Ranks evidence nodes deterministically based on relevance, directness, entity match, and freshness."""
    
    TYPE_DIRECTNESS_WEIGHTS = {
        "TELEMETRY_LOG": 1.00,
        "TRANSACTION_RECORD": 0.95,
        "CUSTOMER_SIGNAL": 0.85,
        "COMMUNICATION_EXTRACT": 0.80,
        "MARKET_OBSERVATION": 0.75
    }
    
    FRESHNESS_WEIGHTS = {
        "LIVE": 1.00,
        "RECENT": 0.90,
        "STALE": 0.70
    }

    def score_evidence(self, item: Dict[str, Any]) -> float:
        """Calculates a deterministic composite relevance score (0 - 100)."""
        ev_type = item.get("evidence_type", "TELEMETRY_LOG")
        type_weight = self.TYPE_DIRECTNESS_WEIGHTS.get(ev_type, 0.80)
        
        freshness_obj = item.get("freshness", {})
        fresh_status = freshness_obj.get("status", "RECENT")
        fresh_weight = self.FRESHNESS_WEIGHTS.get(fresh_status, 0.85)
        
        confidence_obj = item.get("confidence", {})
        conf_score = float(confidence_obj.get("score", 80))
        
        # Composite score
        raw_score = conf_score * 0.50 + (type_weight * 100.0) * 0.30 + (fresh_weight * 100.0) * 0.20
        return round(raw_score, 2)

    def rank_evidence(self, evidence_list: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Sorts evidence list deterministically by score descending, breaking ties by evidence_id."""
        for item in evidence_list:
            item["ranking_score"] = self.score_evidence(item)
            
        sorted_list = sorted(
            evidence_list,
            key=lambda x: (x["ranking_score"], x["evidence_id"]),
            reverse=True
        )
        
        for idx, item in enumerate(sorted_list, start=1):
            item["evidence_rank"] = idx
            
        return sorted_list
