"use client";

import React, { useEffect, useState } from "react";
import { Sidebar } from "@/components/navigation/Sidebar";
import { TopBar } from "@/components/navigation/TopBar";
import { useApp } from "@/context/AppContext";
import { apiClient } from "@/lib/api";
import { AIExplanationResponse } from "@/lib/types";
import Link from "next/link";

export default function CommandCenterPage() {
  const { persona, region, setRegion, regionData, quarter, setQuarter, triggerLiveInvestigation, isInvestigationRunning } = useApp();
  const [selectedKpi, setSelectedKpi] = useState<string>("revenue");
  const [aiExplanation, setAiExplanation] = useState<AIExplanationResponse | null>(null);
  const [lastRefreshed, setLastRefreshed] = useState<string>("Just now");

  useEffect(() => {
    async function loadAIData() {
      try {
        const aiData = await apiClient.getAIExplanation("north_america_east_revenue", {
          persona,
          region,
          prevPeriod: "2026-Q2",
          currPeriod: "2026-Q3",
        });
        setAiExplanation(aiData);
      } catch (aiErr) {
        console.warn("AI summary fallback:", aiErr);
      }
    }
    loadAIData();
    const interval = setInterval(() => {
      setLastRefreshed(new Date().toLocaleTimeString());
    }, 15000);
    return () => clearInterval(interval);
  }, [persona, region]);

  // Dynamic persona tailored summaries
  const getPersonaExecutiveSummary = () => {
    if (aiExplanation?.explanation?.summary) {
      return aiExplanation.explanation.summary;
    }
    switch (persona) {
      case "CFO":
        return `North America East revenue contracted by ${regionData.variancePct} (${regionData.variance}) against the Q2 baseline. Gross margin diluted by ${regionData.grossMarginDelta}. The primary root cause is the ${regionData.primaryDriver} (${regionData.primaryDriverShare} contribution), with deterministic prescriptive recovery modeled at ${regionData.recoveryPool}.`;
      case "REGIONAL_SALES_MANAGER":
        return `Commercial order conversion dropped in NA-East due to acute stockouts of SKU-8821. 29 distributor purchase orders are deferred ($240K held volume), and competitor Horizon Foods introduced 15% discount promotions in retail channels.`;
      case "COO":
        return `Supply chain operational availability plunged to ${regionData.availability} in Atlanta DC across a 14-day zero-stock period. Authorizing the Chicago-to-Atlanta emergency stock transfer will restore regional fulfillment within 14 days.`;
      case "SUPPLY_CHAIN_LEAD":
        return `Atlanta DC safety buffer was depleted due to transit delays. Chicago Central DC holds 4,800 surplus units (142% safety buffer). Immediate reallocation of 3,200 units resolves the regional bottleneck.`;
      default:
        return `Target revenue anomaly of ${regionData.variance} detected. Multi-factor causal attribution identifies ${regionData.primaryDriver} as the dominant contributor (${regionData.primaryDriverShare}).`;
    }
  };

  return (
    <div className="flex min-h-screen bg-[#051424] text-on-surface">
      <Sidebar />

      <div className="flex-1 flex flex-col min-w-0">
        <TopBar breadcrumb="Executive Command Center" />

        <main className="flex-1 p-6 md:p-8 space-y-6 max-w-[1600px] mx-auto w-full">
          {/* Top Filter & Interactive Action Bar (Guaranteed Single-Row Alignment) */}
          <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-4 pb-3 border-b border-outline-variant/15">
            {/* Left: Telemetry Status & Title */}
            <div className="shrink-0 min-w-0">
              <div className="flex items-center gap-2 mb-1">
                <span className="text-[10px] font-mono text-primary font-bold uppercase tracking-widest bg-primary/10 border border-primary/20 px-2 py-0.5 rounded-md flex items-center gap-1.5 shrink-0">
                  <span className="w-2 h-2 rounded-full bg-primary animate-ping inline-block"></span>
                  Live Telemetry Feed
                </span>
                <span className="text-xs font-mono text-on-surface-variant whitespace-nowrap">
                  Updated: <strong className="text-on-surface">{lastRefreshed}</strong>
                </span>
              </div>
              <h1 className="font-display font-extrabold text-2xl text-on-surface tracking-tight whitespace-nowrap">
                Executive Command Center
              </h1>
            </div>

            {/* Right: Quarter Filter, Refresh, and Briefing Action */}
            <div className="flex flex-wrap items-center gap-2.5 shrink-0">
              {/* Interactive Quarter Filter */}
              <div className="flex p-1 bg-surface-container rounded-xl border border-outline-variant/30 font-mono text-xs shadow-sm">
                {(["2026-Q3", "2026-Q2", "2026-Q1"] as const).map((q) => (
                  <button
                    key={q}
                    onClick={() => setQuarter(q)}
                    className={`px-3 py-1.5 rounded-lg transition-all font-bold ${
                      quarter === q
                        ? "bg-primary text-black shadow-glow"
                        : "text-on-surface-variant hover:text-on-surface"
                    }`}
                  >
                    {q}
                  </button>
                ))}
              </div>

              {/* Re-run Pipeline Button */}
              <button
                onClick={triggerLiveInvestigation}
                disabled={isInvestigationRunning}
                className={`px-3.5 py-2 rounded-xl font-mono text-xs font-bold transition-all flex items-center gap-1.5 ${
                  isInvestigationRunning
                    ? "bg-primary/20 text-primary border border-primary/50 animate-pulse"
                    : "bg-surface-container hover:bg-primary/10 text-primary border border-primary/30 shadow-sm"
                }`}
              >
                <span className="material-symbols-outlined text-[16px]">
                  {isInvestigationRunning ? "sync" : "refresh"}
                </span>
                <span>{isInvestigationRunning ? "Re-Evaluating..." : "Refresh Live"}</span>
              </button>

              {/* Generate Briefing CTA */}
              <Link
                href="/briefing"
                className="bg-primary text-black font-mono text-xs font-bold px-4 py-2 rounded-xl hover:bg-primary-light transition-all flex items-center gap-1.5 shadow-glow whitespace-nowrap"
              >
                <span className="material-symbols-outlined text-[16px]">description</span>
                <span>Generate Briefing</span>
              </Link>
            </div>
          </div>

          {/* 5-Column KPI Bento Grid (Interactive Selection & Live Values) */}
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-3.5">
            {/* KPI 1: Revenue */}
            <div
              onClick={() => setSelectedKpi("revenue")}
              className={`glass-panel rounded-xl p-4 flex flex-col justify-between relative overflow-hidden transition-all duration-200 cursor-pointer border ${
                selectedKpi === "revenue"
                  ? "border-error ring-2 ring-error/50 bg-error/15 shadow-glow"
                  : "border-error/40 bg-error/5 hover:border-error"
              }`}
            >
              <div className="absolute top-0 left-0 w-full h-1 bg-error"></div>
              <div className="flex justify-between items-start mb-1">
                <h3 className="font-mono text-[10px] text-on-surface-variant uppercase tracking-wider font-bold">
                  Revenue ({region})
                </h3>
                <div className="bg-error/20 text-error px-1.5 py-0.5 rounded text-[9px] font-mono flex items-center gap-1 border border-error/30 font-bold">
                  <span className="material-symbols-outlined text-[11px]">warning</span> CRITICAL
                </div>
              </div>
              <div>
                <span className="font-display font-extrabold text-2xl md:text-3xl text-on-surface block mb-1">
                  {regionData.revenue}
                </span>
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-1 text-error font-mono font-bold text-xs">
                    <span className="material-symbols-outlined text-[14px]">trending_down</span>
                    <span>{regionData.variancePct}</span>
                  </div>
                  <svg className="w-14 h-5" viewBox="0 0 100 20">
                    <path
                      d="M0,5 L20,10 L40,8 L60,16 L80,18 L100,20"
                      fill="none"
                      stroke="#ffb4ab"
                      strokeWidth="2"
                      strokeLinecap="round"
                    />
                  </svg>
                </div>
              </div>
            </div>

            {/* KPI 2: Gross Margin */}
            <div
              onClick={() => setSelectedKpi("margin")}
              className={`glass-panel rounded-xl p-4 flex flex-col justify-between transition-all duration-200 cursor-pointer border ${
                selectedKpi === "margin"
                  ? "border-primary ring-2 ring-primary/50 bg-primary/15 shadow-glow"
                  : "border-outline-variant/30 bg-surface-container/60 hover:border-primary/40"
              }`}
            >
              <div className="flex justify-between items-start mb-1">
                <h3 className="font-mono text-[10px] text-on-surface-variant uppercase tracking-wider font-bold">
                  Gross Margin
                </h3>
                <span className="material-symbols-outlined text-on-surface-variant text-[16px]">monetization_on</span>
              </div>
              <div>
                <span className="font-display font-extrabold text-2xl md:text-3xl text-on-surface block mb-1">
                  {regionData.grossMargin}
                </span>
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-1 text-error font-mono font-bold text-xs">
                    <span className="material-symbols-outlined text-[14px]">trending_down</span>
                    <span>{regionData.grossMarginDelta}</span>
                  </div>
                  <svg className="w-14 h-5" viewBox="0 0 100 20">
                    <path
                      d="M0,15 L20,12 L40,14 L60,8 L80,5 L100,2"
                      fill="none"
                      stroke="#ffb4ab"
                      strokeWidth="2"
                      strokeLinecap="round"
                    />
                  </svg>
                </div>
              </div>
            </div>

            {/* KPI 3: Units Sold */}
            <div
              onClick={() => setSelectedKpi("units")}
              className={`glass-panel rounded-xl p-4 flex flex-col justify-between transition-all duration-200 cursor-pointer border ${
                selectedKpi === "units"
                  ? "border-primary ring-2 ring-primary/50 bg-primary/15 shadow-glow"
                  : "border-outline-variant/30 bg-surface-container/60 hover:border-primary/40"
              }`}
            >
              <div className="flex justify-between items-start mb-1">
                <h3 className="font-mono text-[10px] text-on-surface-variant uppercase tracking-wider font-bold">
                  Units Sold
                </h3>
                <span className="material-symbols-outlined text-on-surface-variant text-[16px]">inventory</span>
              </div>
              <div>
                <span className="font-display font-extrabold text-2xl md:text-3xl text-on-surface block mb-1">
                  {regionData.unitsSold}
                </span>
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-1 text-error font-mono font-bold text-xs">
                    <span className="material-symbols-outlined text-[14px]">trending_down</span>
                    <span>{regionData.unitsSoldDelta}</span>
                  </div>
                  <svg className="w-14 h-5" viewBox="0 0 100 20">
                    <path
                      d="M0,15 L20,12 L40,16 L60,8 L80,6 L100,2"
                      fill="none"
                      stroke="#ffb4ab"
                      strokeWidth="2"
                      strokeLinecap="round"
                    />
                  </svg>
                </div>
              </div>
            </div>

            {/* KPI 4: Availability */}
            <div
              onClick={() => setSelectedKpi("availability")}
              className={`glass-panel rounded-xl p-4 flex flex-col justify-between relative transition-all duration-200 cursor-pointer border ${
                selectedKpi === "availability"
                  ? "border-error ring-2 ring-error/50 bg-error/15 shadow-glow"
                  : "border-error/30 bg-error/5 hover:border-error"
              }`}
            >
              <div className="absolute top-2 right-2 w-1.5 h-1.5 bg-error rounded-full animate-pulse"></div>
              <div className="flex justify-between items-start mb-1">
                <h3 className="font-mono text-[10px] text-on-surface-variant uppercase tracking-wider font-bold">
                  Availability
                </h3>
                <span className="material-symbols-outlined text-error text-[16px]">warehouse</span>
              </div>
              <div>
                <span className="font-display font-extrabold text-2xl md:text-3xl text-on-surface block mb-1">
                  {regionData.availability}
                </span>
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-1 text-error font-mono font-bold text-xs">
                    <span className="material-symbols-outlined text-[14px]">trending_down</span>
                    <span>{regionData.availabilityDelta}</span>
                  </div>
                  <svg className="w-14 h-5" viewBox="0 0 100 20">
                    <path
                      d="M0,2 L20,5 L40,10 L60,8 L80,18 L100,20"
                      fill="none"
                      stroke="#ffb4ab"
                      strokeWidth="2"
                      strokeLinecap="round"
                    />
                  </svg>
                </div>
              </div>
            </div>

            {/* KPI 5: Orders */}
            <div
              onClick={() => setSelectedKpi("orders")}
              className={`glass-panel rounded-xl p-4 flex flex-col justify-between transition-all duration-200 cursor-pointer border ${
                selectedKpi === "orders"
                  ? "border-primary ring-2 ring-primary/50 bg-primary/15 shadow-glow"
                  : "border-outline-variant/30 bg-surface-container/60 hover:border-primary/40"
              }`}
            >
              <div className="flex justify-between items-start mb-1">
                <h3 className="font-mono text-[10px] text-on-surface-variant uppercase tracking-wider font-bold">
                  Orders
                </h3>
                <span className="material-symbols-outlined text-on-surface-variant text-[16px]">shopping_cart</span>
              </div>
              <div>
                <span className="font-display font-extrabold text-2xl md:text-3xl text-on-surface block mb-1">
                  {regionData.orders}
                </span>
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-1 text-error font-mono font-bold text-xs">
                    <span className="material-symbols-outlined text-[14px]">trending_down</span>
                    <span>{regionData.ordersDelta}</span>
                  </div>
                  <svg className="w-14 h-5" viewBox="0 0 100 20">
                    <path
                      d="M0,10 L20,11 L40,9 L60,10 L80,10 L100,10"
                      fill="none"
                      stroke="#ffb4ab"
                      strokeWidth="2"
                      strokeLinecap="round"
                    />
                  </svg>
                </div>
              </div>
            </div>
          </div>

          {/* Middle Section: AI Executive Summary & Priority Alerts */}
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
            {/* AI Executive Summary (8 cols) */}
            <div className="lg:col-span-8 glass-panel rounded-xl p-6 border border-primary/30 flex flex-col justify-between shadow-[0_4px_24px_rgba(20,184,166,0.06)] bg-gradient-to-br from-primary-container/15 via-surface-container to-surface">
              <div>
                <div className="flex items-center justify-between mb-4">
                  <div className="flex items-center gap-3">
                    <div className="bg-primary/20 p-2 rounded-lg border border-primary/30 text-primary">
                      <span className="material-symbols-outlined text-[22px]">auto_awesome</span>
                    </div>
                    <div>
                      <h2 className="font-display font-bold text-lg text-on-surface">
                        Grounded AI Executive Summary
                      </h2>
                      <span className="text-[10px] font-mono text-primary font-bold">
                        Persona Lens: {persona.replace("_", " ")}
                      </span>
                    </div>
                  </div>
                  <div className="bg-surface-container border border-outline-variant/30 px-3 py-1 rounded-full font-mono text-[11px] text-on-surface-variant flex items-center gap-2">
                    Confidence: <span className="text-primary font-bold">89.0%</span>
                  </div>
                </div>

                <p className="font-sans text-sm md:text-base leading-relaxed text-on-surface font-normal">
                  "{getPersonaExecutiveSummary()}"
                </p>
              </div>

              <div className="flex flex-wrap items-center justify-between pt-5 mt-5 border-t border-outline-variant/20 gap-3">
                <div className="flex items-center gap-2 font-mono text-xs text-on-surface-variant">
                  <span className="material-symbols-outlined text-primary text-[16px]">verified</span>
                  <span>100% Deterministic Evidence Lineage</span>
                </div>

                <Link
                  href="/decision-graph"
                  className="bg-primary text-black font-mono text-xs px-5 py-2.5 rounded-lg hover:bg-primary-light transition-all flex items-center gap-2 font-bold shadow-glow"
                >
                  <span>Open Decision Graph</span>
                  <span className="material-symbols-outlined text-[16px]">arrow_forward</span>
                </Link>
              </div>
            </div>

            {/* Priority Alerts (4 cols) */}
            <div className="lg:col-span-4 glass-panel rounded-xl p-5 border border-outline-variant/30 flex flex-col space-y-3 bg-surface-container/80">
              <div className="flex items-center justify-between pb-2 border-b border-outline-variant/30">
                <div className="flex items-center gap-2">
                  <span className="material-symbols-outlined text-error text-[20px]">notification_important</span>
                  <h2 className="font-display font-bold text-base text-on-surface">Priority Alerts</h2>
                </div>
                <span className="text-[10px] font-mono text-on-surface-variant">3 Active</span>
              </div>

              <div className="space-y-2.5">
                {/* Critical Alert */}
                <div className="bg-error/10 border border-error/30 rounded-lg p-3 flex gap-3 relative overflow-hidden">
                  <div className="absolute left-0 top-0 bottom-0 w-1 bg-error"></div>
                  <span className="material-symbols-outlined text-error text-[18px] shrink-0 mt-0.5">warning</span>
                  <div className="flex-1 text-xs">
                    <div className="flex justify-between items-center mb-1 font-mono">
                      <span className="text-error font-bold tracking-wider">CRITICAL</span>
                      <span className="text-[10px] text-on-surface-variant">2h ago</span>
                    </div>
                    <p className="text-on-surface font-sans mb-1 leading-snug">
                      {region} Revenue missed baseline by {regionData.variance} ({regionData.variancePct})
                    </p>
                    <Link href="/root-cause" className="text-primary font-mono text-[10px] hover:underline font-bold">
                      Investigate Root Cause →
                    </Link>
                  </div>
                </div>

                {/* High Alert */}
                <div className="bg-surface-dim border border-outline-variant/30 rounded-lg p-3 flex gap-3 relative overflow-hidden">
                  <div className="absolute left-0 top-0 bottom-0 w-1 bg-primary"></div>
                  <span className="material-symbols-outlined text-primary text-[18px] shrink-0 mt-0.5">priority_high</span>
                  <div className="flex-1 text-xs">
                    <div className="flex justify-between items-center mb-1 font-mono">
                      <span className="text-primary font-bold tracking-wider">HIGH</span>
                      <span className="text-[10px] text-on-surface-variant">4h ago</span>
                    </div>
                    <p className="text-on-surface font-sans mb-1 leading-snug">
                      Availability fell to {regionData.availability} in regional fulfillment DC
                    </p>
                    <Link href="/evidence" className="text-primary font-mono text-[10px] hover:underline font-bold">
                      View Evidence Ledger →
                    </Link>
                  </div>
                </div>

                {/* Medium Alert */}
                <div className="bg-surface-dim border border-outline-variant/30 rounded-lg p-3 flex gap-3 relative overflow-hidden">
                  <div className="absolute left-0 top-0 bottom-0 w-1 bg-secondary"></div>
                  <span className="material-symbols-outlined text-secondary text-[18px] shrink-0 mt-0.5">info</span>
                  <div className="flex-1 text-xs">
                    <div className="flex justify-between items-center mb-1 font-mono">
                      <span className="text-secondary font-bold tracking-wider">MEDIUM</span>
                      <span className="text-[10px] text-on-surface-variant">Yesterday</span>
                    </div>
                    <p className="text-on-surface font-sans mb-1 leading-snug">
                      29 distributor replenishment POs deferred pending availability
                    </p>
                    <Link href="/recommendations" className="text-primary font-mono text-[10px] hover:underline font-bold">
                      Review Levers →
                    </Link>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Bottom Decision Graph Interactive Preview Strip (Dynamic & Clickable) */}
          <div className="glass-panel rounded-2xl p-6 border border-outline-variant/30 bg-surface-container/60 shadow-xl">
            <div className="flex flex-wrap items-center justify-between gap-3 mb-4 pb-3 border-b border-outline-variant/20">
              <div className="flex items-center gap-3">
                <div className="w-8 h-8 rounded-xl bg-primary/10 border border-primary/30 flex items-center justify-center text-primary">
                  <span className="material-symbols-outlined text-[18px]">account_tree</span>
                </div>
                <div>
                  <h3 className="font-display font-bold text-sm text-on-surface">
                    Decision Graph: Root Cause Attribution Flow
                  </h3>
                  <p className="text-xs font-mono text-on-surface-variant">
                    Interactive pipeline: Click any stage to inspect nodes & live causal evidence
                  </p>
                </div>
              </div>
              <Link
                href="/decision-graph"
                className="text-primary hover:bg-primary/10 px-3.5 py-1.5 rounded-xl border border-primary/30 text-xs font-mono font-bold transition-all flex items-center gap-1.5 shadow-sm hover:shadow-glow"
              >
                <span>Open Full Graph Canvas</span>
                <span className="material-symbols-outlined text-[16px]">arrow_forward</span>
              </Link>
            </div>

            <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3 text-xs font-mono">
              {[
                {
                  stage: "1. Anomaly",
                  title: "Revenue Deficit",
                  val: regionData.variance,
                  valColor: "text-error",
                  badge: "Empirical Gap",
                  href: "/decision-graph",
                  icon: "warning",
                },
                {
                  stage: "2. Driver",
                  title: regionData.primaryDriver,
                  val: `${regionData.primaryDriverShare} Share`,
                  valColor: "text-primary",
                  badge: "Primary Bottleneck",
                  href: "/root-cause",
                  icon: "warehouse",
                },
                {
                  stage: "3. Evidence",
                  title: "SAP Zero-Stock",
                  val: "14 Days",
                  valColor: "text-primary",
                  badge: "ERP Snapshot",
                  href: "/evidence?q=EVID_ERP_ATL_STOCKOUT_001",
                  icon: "verified",
                },
                {
                  stage: "4. Mechanic",
                  title: "Depletion Cascade",
                  val: `${regionData.availability} Avail`,
                  valColor: "text-on-surface",
                  badge: "Supply Shock",
                  href: "/decision-graph",
                  icon: "account_tree",
                },
                {
                  stage: "5. Action",
                  title: "Stock Transfer",
                  val: "+$484K Rec",
                  valColor: "text-primary",
                  badge: "Buffer Rebalance",
                  href: "/recommendations",
                  icon: "bolt",
                },
                {
                  stage: "6. Outcome",
                  title: "Fiscal Recovery",
                  val: regionData.recoveryPool,
                  valColor: "text-primary font-black",
                  badge: "Projected Lift",
                  href: "/recommendations",
                  icon: "monitoring",
                },
              ].map((s, sIdx) => (
                <Link
                  key={sIdx}
                  href={s.href}
                  className="p-3.5 rounded-xl bg-surface-dim hover:bg-surface-bright/30 border border-outline-variant/30 hover:border-primary/60 hover:shadow-glow hover:-translate-y-0.5 transition-all flex flex-col justify-between group cursor-pointer relative overflow-hidden"
                >
                  {/* Subtle top indicator bar */}
                  <div className="flex items-center justify-between mb-1.5">
                    <span className="text-[9px] uppercase tracking-wider text-on-surface-variant font-bold">
                      {s.stage}
                    </span>
                    <span className="material-symbols-outlined text-[13px] text-primary opacity-0 group-hover:opacity-100 transition-all -translate-x-1 group-hover:translate-x-0">
                      arrow_forward
                    </span>
                  </div>

                  <div className="font-sans font-bold text-xs text-on-surface group-hover:text-primary transition-colors leading-tight mb-1 truncate">
                    {s.title}
                  </div>

                  <div className={`font-mono text-xs font-extrabold ${s.valColor} mb-1.5`}>
                    {s.val}
                  </div>

                  <div className="pt-1 border-t border-outline-variant/20 flex items-center justify-between text-[9px] font-mono text-on-surface-variant">
                    <span>{s.badge}</span>
                    <span className="material-symbols-outlined text-[11px] text-primary/70">{s.icon}</span>
                  </div>
                </Link>
              ))}
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}
