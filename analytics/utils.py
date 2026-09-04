"""
InsightPilot AI — Analytics Utility Functions
Helper utilities for date handling, quarter parsing, and numeric calculations.
"""

from datetime import date, datetime
from typing import Tuple

def parse_date(date_str: str) -> date:
    """Parses ISO date string or ISO datetime string into date object."""
    if not date_str:
        raise ValueError("Cannot parse empty date string")
    clean_str = date_str.strip()
    if "T" in clean_str:
        return datetime.fromisoformat(clean_str.replace("Z", "+00:00")).date()
    return date.fromisoformat(clean_str)

def get_fiscal_quarter(d: date) -> str:
    """Returns fiscal quarter identifier string (e.g. 2026-Q3)."""
    month = d.month
    year = d.year
    if month in (1, 2, 3):
        return f"{year}-Q1"
    elif month in (4, 5, 6):
        return f"{year}-Q2"
    elif month in (7, 8, 9):
        return f"{year}-Q3"
    else:
        return f"{year}-Q4"

def calculate_percentage_change(current_val: float, previous_val: float) -> float:
    """Calculates percentage change between previous and current values."""
    if previous_val == 0:
        return 0.0
    return round(((current_val - previous_val) / previous_val) * 100.0, 2)
