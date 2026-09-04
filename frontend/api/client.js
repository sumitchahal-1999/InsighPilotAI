/**
 * InsightPilot AI — Reusable Browser API Client
 * Wraps native fetch() with timeouts, typed errors, and domain endpoint helpers.
 */

import { CONFIG } from "../config/config.js";

export class APIClientError extends Error {
    constructor(message, status = 0, code = "UNKNOWN_ERROR", details = null) {
        super(message);
        this.name = "APIClientError";
        this.status = status;
        this.code = code;
        this.details = details;
    }
}

class APIClient {
    constructor(baseUrl = CONFIG.API_BASE_URL) {
        this.baseUrl = baseUrl.replace(/\/+$/, "");
        this.timeoutMs = CONFIG.REQUEST_TIMEOUT_MS;
    }

    async _request(path, options = {}) {
        const url = `${this.baseUrl}${path.startsWith("/") ? path : `/${path}`}`;
        const controller = new AbortController();
        const timerId = setTimeout(() => controller.abort(), this.timeoutMs);

        const defaultHeaders = {
            "Accept": "application/json",
        };

        if (options.body && typeof options.body === "object" && !(options.body instanceof FormData)) {
            defaultHeaders["Content-Type"] = "application/json";
            options.body = JSON.stringify(options.body);
        }

        try {
            const response = await fetch(url, {
                ...options,
                headers: {
                    ...defaultHeaders,
                    ...(options.headers || {}),
                },
                signal: controller.signal,
            });

            clearTimeout(timerId);

            let data;
            const contentType = response.headers.get("content-type");
            if (contentType && contentType.includes("application/json")) {
                data = await response.json();
            } else {
                data = await response.text();
            }

            if (!response.ok) {
                const errorCode = (data && data.error && data.error.code) || `HTTP_${response.status}`;
                const errorMessage = (data && data.error && data.error.message) || response.statusText || "Request failed";
                throw new APIClientError(errorMessage, response.status, errorCode, data);
            }

            return data;
        } catch (err) {
            clearTimeout(timerId);
            if (err instanceof APIClientError) {
                throw err;
            }
            if (err.name === "AbortError") {
                throw new APIClientError(`Request timed out after ${this.timeoutMs}ms`, 408, "TIMEOUT_ERROR");
            }
            throw new APIClientError(err.message || "Network connection failed", 0, "NETWORK_ERROR");
        }
    }

    get(path, params = {}) {
        const query = new URLSearchParams(params).toString();
        const fullPath = query ? `${path}?${query}` : path;
        return this._request(fullPath, { method: "GET" });
    }

    post(path, body = {}) {
        return this._request(path, { method: "POST", body });
    }

    // Domain Specific Methods
    getKPIs() {
        return this.get("/api/v1/kpis");
    }

    getKPI(kpiId = CONFIG.DEFAULT_KPI_ID) {
        return this.get(`/api/v1/kpis/${kpiId}`);
    }

    getInvestigation(kpiId = CONFIG.DEFAULT_KPI_ID, region = CONFIG.DEFAULT_REGION, prevPeriod = CONFIG.DEFAULT_PREV_PERIOD, currPeriod = CONFIG.DEFAULT_CURR_PERIOD, persona = CONFIG.DEFAULT_PERSONA) {
        return this.get(`/api/v1/investigations/${kpiId}`, {
            region,
            prev_period_id: prevPeriod,
            curr_period_id: currPeriod,
            persona
        });
    }

    getDrivers(kpiId = CONFIG.DEFAULT_KPI_ID, region = CONFIG.DEFAULT_REGION) {
        return this.get(`/api/v1/investigations/${kpiId}/drivers`, { region });
    }

    getEvidenceList(kpiId = CONFIG.DEFAULT_KPI_ID, region = CONFIG.DEFAULT_REGION) {
        return this.get(`/api/v1/investigations/${kpiId}/evidence`, { region });
    }

    getEvidence(evidenceId) {
        return this.get(`/api/v1/evidence/${evidenceId}`);
    }

    getEvidenceLineage(evidenceId) {
        return this.get(`/api/v1/evidence/${evidenceId}/lineage`);
    }

    getRecommendations(kpiId = CONFIG.DEFAULT_KPI_ID, region = CONFIG.DEFAULT_REGION) {
        return this.get(`/api/v1/recommendations/${kpiId}`, { region });
    }

    getRecommendation(kpiId = CONFIG.DEFAULT_KPI_ID, recId = "") {
        return this.get(`/api/v1/recommendations/${kpiId}/${recId}`);
    }

    getSimulationBaseline(region = CONFIG.DEFAULT_REGION) {
        return this.get(`/api/v1/simulations/baseline`, { region });
    }

    simulateInventoryAvailability(availabilityRatio, region = CONFIG.DEFAULT_REGION) {
        return this.post(`/api/v1/simulations/inventory-availability?region=${encodeURIComponent(region)}`, {
            inventory_availability: availabilityRatio
        });
    }

    getAIExplanation(kpiId = CONFIG.DEFAULT_KPI_ID, options = {}) {
        const persona = typeof options === "string" ? options : (options.persona || CONFIG.DEFAULT_PERSONA);
        const region = options.region || CONFIG.DEFAULT_REGION;
        const prevPeriod = options.prevPeriod || CONFIG.DEFAULT_PREV_PERIOD;
        const currPeriod = options.currPeriod || CONFIG.DEFAULT_CURR_PERIOD;
        const explanationMode = options.explanationMode || "structured";
        const driverId = options.driverId || null;
        const includeRecommendations = options.includeRecommendations !== undefined ? options.includeRecommendations : true;
        const includeSimulation = options.includeSimulation !== undefined ? options.includeSimulation : false;

        const queryParams = new URLSearchParams({
            region,
            prev_period_id: prevPeriod,
            curr_period_id: currPeriod
        }).toString();

        return this.post(`/api/v1/ai/explain/${kpiId}?${queryParams}`, {
            persona,
            explanation_mode: explanationMode,
            driver_id: driverId,
            include_recommendations: includeRecommendations,
            include_simulation: includeSimulation
        });
    }

    getAIDriverExplanation(kpiId = CONFIG.DEFAULT_KPI_ID, driverId = "", persona = CONFIG.DEFAULT_PERSONA, region = CONFIG.DEFAULT_REGION) {
        const queryParams = new URLSearchParams({ region }).toString();
        return this.post(`/api/v1/ai/investigations/${kpiId}/drivers/${driverId}/explanation?${queryParams}`, {
            persona
        });
    }
}

export const apiClient = new APIClient();

