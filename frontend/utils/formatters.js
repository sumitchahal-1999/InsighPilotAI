/**
 * InsightPilot AI — Presentation Formatting Utilities
 * Pure presentation formatting helpers ensuring zero alteration of underlying business data.
 */

export function formatCurrencyMillions(val) {
    if (val === null || val === undefined || isNaN(val)) return "$0.00M";
    const num = Number(val);
    const sign = num < 0 ? "-" : "";
    const absVal = Math.abs(num) / 1000000.0;
    return `${sign}$${absVal.toFixed(2)}M`;
}

export function formatCurrencyThousands(val) {
    if (val === null || val === undefined || isNaN(val)) return "$0K";
    const num = Number(val);
    const sign = num < 0 ? "-" : "";
    const absVal = Math.abs(num) / 1000.0;
    return `${sign}$${absVal.toFixed(0)}K`;
}

export function formatCurrencyExact(val) {
    if (val === null || val === undefined || isNaN(val)) return "$0.00";
    const num = Number(val);
    const sign = num < 0 ? "-" : "";
    return `${sign}$${Math.abs(num).toLocaleString("en-US", { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
}

export function formatPercent(val, includeSign = true) {
    if (val === null || val === undefined || isNaN(val)) return "0.0%";
    const num = Number(val);
    const sign = includeSign && num > 0 ? "+" : "";
    return `${sign}${num.toFixed(1)}%`;
}

export function formatPoints(val) {
    if (val === null || val === undefined || isNaN(val)) return "0.0 pts";
    const num = Number(val);
    const sign = num > 0 ? "+" : "";
    return `${sign}${num.toFixed(1)} pts`;
}

export function formatNumber(val) {
    if (val === null || val === undefined || isNaN(val)) return "0";
    return Number(val).toLocaleString("en-US");
}

export function formatConfidence(val) {
    if (val === null || val === undefined || isNaN(val)) return "0%";
    const num = Number(val);
    const pct = num <= 1.0 && num > 0 ? num * 100 : num;
    return `${pct.toFixed(0)}%`;
}

export function formatConfidencePrecise(val, decimals = 1) {
    if (val === null || val === undefined || isNaN(val)) return "0.0%";
    const num = Number(val);
    const pct = num <= 1.0 && num > 0 ? num * 100 : num;
    return `${pct.toFixed(decimals)}%`;
}

export function truncateHash(hashStr) {
    if (!hashStr || typeof hashStr !== "string") return "";
    const clean = hashStr.startsWith("sha256:") ? hashStr.slice(7) : hashStr;
    if (clean.length <= 12) return clean;
    return `${clean.slice(0, 8)}...${clean.slice(-4)}`;
}

