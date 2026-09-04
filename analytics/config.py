"""
InsightPilot AI — Analytics Configuration
Central configuration paths, contract references, and analytical parameters.
"""

import os
from datetime import date

# Root directories
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_RAW_DIR = os.path.join(BASE_DIR, "data", "raw")
SCHEMAS_DIR = os.path.join(BASE_DIR, "data", "schemas")

# Default Period Configurations
PREVIOUS_PERIOD_ID = "2026-Q2"
CURRENT_PERIOD_ID = "2026-Q3"

PERIOD_DATES = {
    "2025-Q3": (date(2025, 7, 1), date(2025, 9, 30)),
    "2025-Q4": (date(2025, 10, 1), date(2025, 12, 31)),
    "2026-Q1": (date(2026, 1, 1), date(2026, 3, 31)),
    "2026-Q2": (date(2026, 4, 1), date(2026, 6, 30)),
    "2026-Q3": (date(2026, 7, 1), date(2026, 9, 30)),
}

# Materiality & Confidence Thresholds
DEFAULT_WARNING_THRESHOLD_PCT = -3.0
DEFAULT_CRITICAL_THRESHOLD_PCT = -5.0
ABSTENTION_CONFIDENCE_THRESHOLD = 65
MINIMUM_HISTORICAL_DAYS_REQUIRED = 60
