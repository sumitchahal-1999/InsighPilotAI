/**
 * InsightPilot AI — Lightweight State Store
 * Manages active executive context, persona selections, and in-memory response caches.
 */

import { CONFIG } from "../config/config.js";

class AppStore {
    constructor() {
        this.state = {
            selectedKPI: CONFIG.DEFAULT_KPI_ID,
            selectedPersona: CONFIG.DEFAULT_PERSONA,
            selectedRegion: CONFIG.DEFAULT_REGION,
            prevPeriod: CONFIG.DEFAULT_PREV_PERIOD,
            currPeriod: CONFIG.DEFAULT_CURR_PERIOD,
        };
        this.cache = new Map();
        this.listeners = [];
    }

    getState() {
        return { ...this.state };
    }

    setState(partial) {
        this.state = { ...this.state, ...partial };
        this.listeners.forEach((fn) => fn(this.state));
    }

    getPersona() {
        return this.state.selectedPersona;
    }

    setPersona(persona) {
        const normalized = (persona || "").toUpperCase();
        const validPersona = (normalized === "REGIONAL_SALES_MANAGER" || normalized === "RSM") 
            ? "REGIONAL_SALES_MANAGER" 
            : "CFO";
        this.setState({ selectedPersona: validPersona });
    }

    subscribe(listener) {
        this.listeners.push(listener);
        return () => {
            this.listeners = this.listeners.filter((fn) => fn !== listener);
        };
    }

    setCache(key, value) {
        this.cache.set(key, { value, timestamp: Date.now() });
    }

    getCache(key, maxAgeMs = 120000) {
        const entry = this.cache.get(key);
        if (!entry) return null;
        if (Date.now() - entry.timestamp > maxAgeMs) {
            this.cache.delete(key);
            return null;
        }
        return entry.value;
    }

    // Persona-aware AI explanation caching
    getAIExplanationCache(kpiId = this.state.selectedKPI, persona = this.state.selectedPersona, region = this.state.selectedRegion) {
        const key = `ai_explanation_${kpiId}_${persona}_${region}_${this.state.prevPeriod}_${this.state.currPeriod}`;
        return this.getCache(key);
    }

    setAIExplanationCache(data, kpiId = this.state.selectedKPI, persona = this.state.selectedPersona, region = this.state.selectedRegion) {
        const key = `ai_explanation_${kpiId}_${persona}_${region}_${this.state.prevPeriod}_${this.state.currPeriod}`;
        this.setCache(key, data);
    }
}

export const store = new AppStore();
