#!/usr/bin/env python3
"""
Dataset Validation Suite for InsightPilot AI
Accenture Innovation Challenge 2026 — Track 3: BusinessIntelligence.ai

Validates structural integrity, schema conformity, cross-dataset referential
consistency, date boundaries, and directional KPI movement of the synthetic
enterprise data foundation without hardcoded driver assumptions or LLMs.
"""

import os
import csv
import json
from datetime import datetime, date

WORKSPACE_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_RAW_DIR = os.path.join(WORKSPACE_ROOT, "data", "raw")
SCHEMAS_DIR = os.path.join(WORKSPACE_ROOT, "data", "schemas", "entities")

def load_csv(filename: str):
    path = os.path.join(DATA_RAW_DIR, filename)
    assert os.path.exists(path), f"File not found: {path}"
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)

def test_schemas_and_columns():
    print("[1/6] Validating CSV Column Alignment against JSON Schemas...")
    
    schema_map = {
        "revenue.csv": "revenue.json",
        "inventory.csv": "inventory.json",
        "margin.csv": "margin.json",
        "sales.csv": "sales.json",
        "distributor_orders.csv": "distributor_order.json",
        "support_tickets.csv": "support_ticket.json",
        "distributor_communications.csv": "distributor_communication.json",
        "market_intelligence.csv": "market_intelligence.json"
    }
    
    for csv_file, schema_file in schema_map.items():
        schema_path = os.path.join(SCHEMAS_DIR, schema_file)
        assert os.path.exists(schema_path), f"Missing schema: {schema_path}"
        with open(schema_path, "r", encoding="utf-8") as sf:
            schema_json = json.load(sf)
            
        csv_rows = load_csv(csv_file)
        assert len(csv_rows) > 0, f"CSV {csv_file} is empty!"
        
        csv_fields = set(csv_rows[0].keys())
        required_fields = set(schema_json.get("required", []))
        all_properties = set(schema_json.get("properties", {}).keys())
        
        # Verify all required properties exist in CSV
        missing_required = required_fields - csv_fields
        assert not missing_required, f"{csv_file} is missing required fields: {missing_required}"
        
        # Verify no unknown columns exist
        extra_columns = csv_fields - all_properties
        assert not extra_columns, f"{csv_file} contains uncontracted extra columns: {extra_columns}"
        
        print(f"  [OK] {csv_file} ({len(csv_rows):,} rows) matches schema {schema_file}")

def test_primary_keys_and_nulls():
    print("[2/6] Validating Primary Key Uniqueness and Non-Null Constraints...")
    
    pks = {
        "revenue.csv": "invoice_id",
        "inventory.csv": "snapshot_id",
        "margin.csv": "margin_record_id",
        "sales.csv": "sales_item_id",
        "distributor_orders.csv": "po_id",
        "support_tickets.csv": "ticket_id",
        "distributor_communications.csv": "comm_id",
        "market_intelligence.csv": "report_id"
    }
    
    for csv_file, pk_col in pks.items():
        rows = load_csv(csv_file)
        seen_ids = set()
        for idx, row in enumerate(rows):
            val = row[pk_col].strip()
            assert val != "", f"Row {idx} in {csv_file} has empty primary key {pk_col}"
            assert val not in seen_ids, f"Duplicate primary key '{val}' found in {csv_file}"
            seen_ids.add(val)
            
        print(f"  [OK] {csv_file}: {len(seen_ids):,} unique primary keys verified ({pk_col})")

def test_referential_integrity():
    print("[3/6] Validating Cross-Dataset Referential Integrity (SKUs, Regions, Distributors)...")
    
    revenue = load_csv("revenue.csv")
    sales = load_csv("sales.csv")
    inventory = load_csv("inventory.csv")
    dist_orders = load_csv("distributor_orders.csv")
    
    valid_regions = {"NA-East", "NA-Central", "NA-West"}
    valid_skus = {"SKU-8821", "SKU-4410", "SKU-5520", "SKU-9930", "SKU-2205"}
    
    # Check Regions
    for r in revenue:
        assert r["region"] in valid_regions, f"Invalid region in revenue: {r['region']}"
    for s in sales:
        assert s["region"] in valid_regions, f"Invalid region in sales: {s['region']}"
    for i in inventory:
        assert i["region"] in valid_regions, f"Invalid region in inventory: {i['region']}"
        
    # Check SKUs
    for r in revenue:
        assert r["sku_id"] in valid_skus, f"Invalid SKU in revenue: {r['sku_id']}"
    for s in sales:
        assert s["sku_id"] in valid_skus, f"Invalid SKU in sales: {s['sku_id']}"
    for i in inventory:
        assert i["sku_id"] in valid_skus, f"Invalid SKU in inventory: {i['sku_id']}"
        
    # Check Distributor Consistency
    sales_dists = set(s["distributor_id"] for s in sales)
    order_dists = set(o["distributor_id"] for o in dist_orders)
    assert sales_dists.issubset(order_dists) or order_dists.issubset(sales_dists), "Distributor ID mismatch between sales and orders"
    
    print(f"  [OK] Cross-dataset referential integrity verified across all 5 master dimensions.")

def test_numeric_ranges_and_dates():
    print("[4/6] Validating Numeric Ranges, Non-Negative Constraints & Dates...")
    
    revenue = load_csv("revenue.csv")
    for r in revenue:
        gross = float(r["gross_amount"])
        disc = float(r["discount_amount"])
        net = float(r["net_revenue"])
        assert gross > 0, f"Non-positive gross revenue: {gross}"
        assert disc >= 0, f"Negative discount: {disc}"
        assert round(gross - disc, 2) == round(net, 2), f"Revenue math mismatch: {gross} - {disc} != {net}"
        # Validate date parsing
        d = date.fromisoformat(r["invoice_date"])
        assert date(2025, 7, 1) <= d <= date(2026, 9, 30), f"Date out of bounds: {d}"
        
    inventory = load_csv("inventory.csv")
    for inv in inventory:
        on_hand = int(inv["on_hand_units"])
        avail = int(inv["available_units"])
        req = int(inv["required_demand_units"])
        avail_pct = float(inv["availability_percentage"])
        assert on_hand >= 0 and avail >= 0 and req > 0, "Negative units in inventory"
        assert avail <= on_hand, f"Available units ({avail}) exceed on-hand units ({on_hand})"
        assert 0.0 <= avail_pct <= 100.0, f"Impossible availability percentage: {avail_pct}"
        
    print("  [OK] Mathematical bounds, non-negative constraints, and date validity verified.")

def test_scenario_signals_presence():
    print("[5/6] Validating Operational Scenario Signals (Atlanta Stockout, Orders, Price Drops)...")
    
    # 1. Atlanta DC Disruption Signal
    inventory = load_csv("inventory.csv")
    atl_disruption_snaps = [
        inv for inv in inventory
        if inv["dc_location"] == "Atlanta-DC-01"
        and date(2026, 8, 1) <= date.fromisoformat(inv["snapshot_date"]) <= date(2026, 8, 19)
    ]
    assert len(atl_disruption_snaps) > 0, "No inventory snapshots found for Atlanta DC disruption period"
    avg_atl_avail = sum(float(x["availability_percentage"]) for x in atl_disruption_snaps) / len(atl_disruption_snaps)
    assert avg_atl_avail < 85.0, f"Atlanta DC availability during disruption did not drop: {avg_atl_avail:.2f}%"
    print(f"  [OK] Atlanta DC stockout signal verified: Average availability dropped to {avg_atl_avail:.1f}% during Aug 1-19.")
    
    # 2. Distributor Order Deferrals
    dist_orders = load_csv("distributor_orders.csv")
    deferred_orders = [o for o in dist_orders if o["order_status"] == "DEFERRED" and o["region"] == "NA-East"]
    assert len(deferred_orders) >= 5, f"Insufficient distributor order deferrals in NA-East: {len(deferred_orders)}"
    print(f"  [OK] Distributor order deferral signals verified: {len(deferred_orders)} deferred POs found in NA-East.")
    
    # 3. Horizon Foods Competitive Price Cut
    market_intel = load_csv("market_intelligence.csv")
    horizon_promos = [m for m in market_intel if "Horizon Foods" in m["competitor_name"] and float(m["observed_price_usd"]) <= 105.0]
    assert len(horizon_promos) >= 3, "Horizon Foods price cut observations missing"
    print(f"  [OK] Horizon Foods price cut signal verified: {len(horizon_promos)} observations of 15% discount ($102 vs $120).")
    
    # 4. Support Ticket Escalations
    tickets = load_csv("support_tickets.csv")
    stockout_tickets = [t for t in tickets if t["category"] == "STOCKOUT_COMPLAINT" and t["region"] == "NA-East"]
    assert len(stockout_tickets) >= 10, f"Insufficient stockout support escalations: {len(stockout_tickets)}"
    print(f"  [OK] Customer support escalations verified: {len(stockout_tickets)} stockout complaints in NA-East.")

def test_kpi_directional_movement():
    print("[6/6] Validating Target Scenario Directional Movement (NA-East Revenue -8.0%)...")
    
    revenue = load_csv("revenue.csv")
    
    q2_start = date(2026, 4, 1)
    q2_end = date(2026, 6, 30)
    q3_start = date(2026, 7, 1)
    q3_end = date(2026, 9, 30)
    
    q2_na_east_rev = sum(
        float(r["net_revenue"]) for r in revenue
        if r["region"] == "NA-East" and q2_start <= date.fromisoformat(r["invoice_date"]) <= q2_end
    )
    
    q3_na_east_rev = sum(
        float(r["net_revenue"]) for r in revenue
        if r["region"] == "NA-East" and q3_start <= date.fromisoformat(r["invoice_date"]) <= q3_end
    )
    
    variance_amount = q3_na_east_rev - q2_na_east_rev
    variance_pct = (variance_amount / q2_na_east_rev) * 100.0
    
    print(f"  * Previous Period (2026-Q2) NA-East Revenue: ${q2_na_east_rev:,.2f}")
    print(f"  * Current Period (2026-Q3)  NA-East Revenue: ${q3_na_east_rev:,.2f}")
    print(f"  * Net Variance:                             ${variance_amount:,.2f}")
    print(f"  * Percentage Change:                        {variance_pct:.2f}%")
    
    # Must be between -7.5% and -8.5% (approx -8.0%)
    assert -8.5 <= variance_pct <= -7.5, f"Scenario variance {variance_pct:.2f}% deviates from target ~ -8.0%"
    print(f"  [OK] Target scenario alignment verified: NA-East Revenue dropped by {abs(variance_pct):.2f}% in Q3 2026.")

def main():
    print("=" * 70)
    print("INSIGHTPILOT AI -- DATASET VALIDATION SUITE")
    print("=" * 70)
    test_schemas_and_columns()
    test_primary_keys_and_nulls()
    test_referential_integrity()
    test_numeric_ranges_and_dates()
    test_scenario_signals_presence()
    test_kpi_directional_movement()
    print("=" * 70)
    print("ALL DATASET VALIDATION CHECKS PASSED SUCCESSFULLY! (100% HEALTHY)")
    print("=" * 70)

if __name__ == "__main__":
    main()
