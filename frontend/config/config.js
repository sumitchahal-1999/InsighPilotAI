/**
 * InsightPilot AI — Frontend Configuration
 * Manages API base URLs and environment parameters for local development and deployment.
 */

export const CONFIG = {
    // Backend API Base URL (Configurable via window.__API_BASE_URL__ or default localhost:8000)
    API_BASE_URL: (typeof window !== "undefined" && window.__API_BASE_URL__) || "http://127.0.0.1:8000",
    DEFAULT_KPI_ID: "north_america_east_revenue",
    DEFAULT_REGION: "NA-East",
    DEFAULT_PREV_PERIOD: "2026-Q2",
    DEFAULT_CURR_PERIOD: "2026-Q3",
    DEFAULT_PERSONA: "CFO",
    REQUEST_TIMEOUT_MS: 15000,
};
