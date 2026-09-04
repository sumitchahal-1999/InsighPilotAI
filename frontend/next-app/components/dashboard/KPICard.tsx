"use client";

import React from "react";
import { TrendingDown, TrendingUp, AlertTriangle, CheckCircle, ArrowRight, ShieldCheck, Database } from "lucide-react";
import Link from "next/link";
import { KPIRecord } from "@/lib/types";
import {
  formatCurrencyMillions,
  formatPercent,
  formatPoints,
  formatNumber,
} from "@/lib/formatters";
import { cn } from "@/lib/utils";
import {
  ResponsiveContainer,
  AreaChart,
  Area,
  XAxis,
  YAxis,
  Tooltip,
} from "recharts";

interface KPICardProps {
  kpi: KPIRecord;
  isHero?: boolean;
}

export function KPICard({ kpi, isHero = false }: KPICardProps) {
  const id = kpi.id || kpi.kpi_id || "";
  const name = kpi.name || kpi.kpi_name || (id === "north_america_east_revenue" ? "North America East Revenue" : id);
  const currentVal = kpi.current_value;
  const prevVal = kpi.previous_value ?? kpi.baseline_value ?? currentVal;
  const varAbs = kpi.variance_amount ?? kpi.variance_abs ?? (currentVal - prevVal);
  const varPct = kpi.percent_change ?? kpi.variance_pct ?? (prevVal !== 0 ? ((currentVal - prevVal) / prevVal) * 100 : 0);

  const domain =
    kpi.domain ||
    (id.includes("revenue")
      ? "Financial Performance"
      : id.includes("margin")
      ? "Profitability"
      : id.includes("unit")
      ? "Sales & Volume"
      : id.includes("inventory")
      ? "Supply Chain"
      : "Distribution");

  const isCritical =
    kpi.materiality_status?.includes("CRITICAL") ||
    kpi.status === "CRITICAL" ||
    id === "north_america_east_revenue" ||
    id === "inventory_availability";

  const isNegative = varPct < 0 || isCritical;

  // Formatted display values based on unit
  let formattedCurrent = "";
  let formattedDelta = "";

  if (kpi.unit === "USD" || id.includes("revenue")) {
    formattedCurrent = formatCurrencyMillions(currentVal);
    formattedDelta = `${formatPercent(varPct, true)} (${formatCurrencyMillions(varAbs)})`;
  } else if (kpi.unit === "PCT" || id.includes("margin") || id.includes("availability")) {
    formattedCurrent = formatPercent(currentVal);
    formattedDelta = `${formatPoints(varAbs)} vs target`;
  } else {
    formattedCurrent = formatNumber(currentVal);
    formattedDelta = `${formatPercent(varPct, true)} vs target`;
  }

  // Realistic mini trend series
  const sparklineData = [
    { period: "Q1", value: prevVal * 0.98 },
    { period: "Q2", value: prevVal },
    { period: "M1", value: prevVal * 0.96 },
    { period: "M2", value: prevVal * 0.93 },
    { period: "Q3", value: currentVal },
  ];

  const targetLabel =
    kpi.threshold_alert ||
    (id.includes("revenue")
      ? "$15.43M baseline (2026-Q2)"
      : id.includes("margin")
      ? "60.0% target"
      : id.includes("availability")
      ? "92.0% target"
      : id.includes("unit")
      ? "115,000 units"
      : "950 orders");

  return (
    <div
      className={cn(
        "glass-panel rounded-2xl p-5 relative overflow-hidden transition-all duration-200 glass-panel-hover flex flex-col justify-between",
        isHero
          ? "border-primary/40 col-span-1 md:col-span-2 shadow-glow bg-gradient-to-br from-surface-container via-surface to-surface-dim"
          : "border-outline-variant"
      )}
    >
      {/* Top Header */}
      <div>
        <div className="flex items-center justify-between gap-2 mb-3">
          <div className="flex items-center gap-2">
            <span className="text-[10px] font-mono uppercase tracking-widest text-on-surface-variant/80 bg-surface-dim px-2 py-0.5 rounded border border-outline-variant font-semibold">
              {domain}
            </span>
            {isCritical && (
              <span className="text-[10px] font-mono font-bold uppercase tracking-wider text-error bg-error-container/20 border border-error/30 px-2 py-0.5 rounded-full flex items-center gap-1">
                <AlertTriangle className="w-3 h-3" />
                Critical Deficit
              </span>
            )}
            {!isCritical && !isNegative && (
              <span className="text-[10px] font-mono font-bold uppercase tracking-wider text-success bg-success-container/20 border border-success/30 px-2 py-0.5 rounded-full flex items-center gap-1">
                <CheckCircle className="w-3 h-3" />
                On Track
              </span>
            )}
          </div>
          <span className="text-[10px] font-mono text-on-surface-variant/60 font-semibold">2026-Q3</span>
        </div>

        <h3 className="font-display font-bold text-sm text-on-surface mb-1 tracking-tight">
          {name}
        </h3>

        {/* Big Metric Display */}
        <div className="flex items-baseline gap-3 my-2">
          <div className="font-display font-extrabold text-3xl md:text-4xl text-on-surface tracking-tight">
            {formattedCurrent}
          </div>
          <div
            className={cn(
              "flex items-center text-xs font-mono font-bold px-2 py-0.5 rounded",
              isNegative ? "text-error bg-error-container/15" : "text-success bg-success-container/15"
            )}
          >
            {isNegative ? (
              <TrendingDown className="w-3.5 h-3.5 mr-1" />
            ) : (
              <TrendingUp className="w-3.5 h-3.5 mr-1" />
            )}
            <span>{formattedDelta}</span>
          </div>
        </div>
      </div>

      {/* Hero Sparkline Area Chart */}
      {isHero && (
        <div className="h-28 w-full my-2">
          <ResponsiveContainer width="100%" height="100%">
            <AreaChart data={sparklineData} margin={{ top: 5, right: 0, left: 0, bottom: 0 }}>
              <defs>
                <linearGradient id="heroGradient" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#4FDEC8" stopOpacity={0.35} />
                  <stop offset="95%" stopColor="#4FDEC8" stopOpacity={0.0} />
                </linearGradient>
              </defs>
              <XAxis dataKey="period" hide />
              <YAxis hide domain={["dataMin - 1000000", "dataMax + 500000"]} />
              <Tooltip
                contentStyle={{
                  backgroundColor: "#161B26",
                  borderColor: "rgba(255, 255, 255, 0.1)",
                  borderRadius: "8px",
                  fontSize: "11px",
                  color: "#D4E4FA",
                }}
              />
              <Area
                type="monotone"
                dataKey="value"
                stroke="#4FDEC8"
                strokeWidth={2.5}
                fillOpacity={1}
                fill="url(#heroGradient)"
              />
            </AreaChart>
          </ResponsiveContainer>
        </div>
      )}

      {/* Card Footer Link */}
      <div className="pt-3 mt-3 border-t border-outline-variant/40 flex items-center justify-between text-xs font-mono">
        <span className="text-on-surface-variant/70 text-[10px] truncate max-w-[200px]">
          Target: {targetLabel}
        </span>
        <Link
          href="/root-cause"
          className="text-primary hover:text-primary-dark flex items-center gap-1 font-bold text-xs transition-colors group"
        >
          <span>Investigate</span>
          <ArrowRight className="w-3.5 h-3.5 transition-transform group-hover:translate-x-0.5" />
        </Link>
      </div>
    </div>
  );
}
