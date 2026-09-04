"use client";

import React, { useEffect, useState } from "react";
import { Sidebar } from "@/components/navigation/Sidebar";
import { TopBar } from "@/components/navigation/TopBar";
import { useApp } from "@/context/AppContext";
import { apiClient } from "@/lib/api";
import { InvestigationResponse, DriverRecord, AIExplanationResponse } from "@/lib/types";
import {
  formatCurrencyThousands,
  formatCurrencyMillions,
  formatPercent,
  formatConfidence,
} from "@/lib/formatters";
import Link from "next/link";

const DEFAULT_DRIVERS: DriverRecord[] = [
  {
    driver_id: "atlanta_dc_stockout",
    driver_name: "Atlanta DC Stockout",
    rank: 1,
    contribution_pct: 43.2,
    impact_usd: -550000,
    confidence_score: 94.0,
    confidence_level: "HIGH",
    supporting_evidence_ids: ["EVID_ERP_ATL_STOCKOUT_001", "EVID_ZENDESK_ATL_DELAY_003"],
    controllability: "HIGH",
    category: "Supply Chain",
  },
  {
    driver_id: "sku_8821_sales_volume",
    driver_name: "SKU-8821 Sales Volume",
    rank: 2,
    contribution_pct: 26.7,
    impact_usd: -340000,
    confidence_score: 89.0,
    confidence_level: "HIGH",
    supporting_evidence_ids: ["EVID_CRM_SKU8821_SALES_004"],
    controllability: "MEDIUM",
    category: "Commercial Sales",
  },
  {
    driver_id: "distributor_orders",
    driver_name: "Distributor Orders Deferral",
    rank: 3,
    contribution_pct: 18.8,
    impact_usd: -240000,
    confidence_score: 85.0,
    confidence_level: "HIGH",
    supporting_evidence_ids: ["EVID_CRM_PO_DEF_006"],
    controllability: "MEDIUM",
    category: "Distribution Channel",
  },
  {
    driver_id: "competitor_horizon_pricing",
    driver_name: "Competitor Horizon Foods Pricing",
    rank: 4,
    contribution_pct: 11.3,
    impact_usd: -144000,
    confidence_score: 78.0,
    confidence_level: "MEDIUM",
    supporting_evidence_ids: ["EVID_MKT_HORIZON_PROMO_008"],
    controllability: "LOW",
    category: "Market Competition",
  },
];

interface TimelineMilestone {
  title: string;
  stageName: string;
  date: string;
  icon: string;
  type: "causal" | "signal" | "outcome";
  typeLabel: string;
  source: string;
  evidenceId: string;
  impact: string;
  description: string;
  metricLabel: string;
  metricValue: string;
}

const TIMELINE_MILESTONES: TimelineMilestone[] = [
  {
    title: "Inventory Decline",
    stageName: "Stage 1: Buffer Depletion",
    date: "Aug 02, 2026",
    icon: "inventory_2",
    type: "signal",
    typeLabel: "Correlated Early Warning Signal",
    source: "SAP MM-WM Inventory Telemetry",
    evidenceId: "EVID_ERP_ATL_BUFFER_001",
    impact: "Safety Stock Contraction",
    description: "Atlanta DC inventory buffer for SKU-8821 dropped below the 15-day safety threshold due to replenishment transit lead-time delays from upstream manufacturing.",
    metricLabel: "Remaining Buffer",
    metricValue: "4.2 Days (Critical)",
  },
  {
    title: "Atlanta Stockout",
    stageName: "Stage 2: Complete Depletion Trigger",
    date: "Aug 10, 2026",
    icon: "warning",
    type: "causal",
    typeLabel: "Primary Root Cause Driver",
    source: "SAP S/4HANA Daily Snapshot (INV-SNAP-21971)",
    evidenceId: "EVID_ERP_ATL_STOCKOUT_001",
    impact: "-$550K Revenue Contraction (43.2% Attribution)",
    description: "14 consecutive days of zero available inventory for SKU-8821 at Atlanta DC (Aug 10 - Aug 24). Regional retail orders experienced unfulfilled backorders.",
    metricLabel: "Stockout Duration",
    metricValue: "14 Days (0 Units)",
  },
  {
    title: "Support Tickets",
    stageName: "Stage 3: Customer Escalation Surge",
    date: "Aug 14, 2026",
    icon: "confirmation_number",
    type: "signal",
    typeLabel: "Customer Friction Telemetry",
    source: "Zendesk Support CRM (TICKET-CLUSTER-ATL)",
    evidenceId: "EVID_ZENDESK_ATL_DELAY_003",
    impact: "142 Regional Backlog Tickets",
    description: "Zendesk support cluster detected a +310% surge in 'Out of Stock' tickets from key East territory wholesale and retail partner accounts.",
    metricLabel: "Ticket Growth",
    metricValue: "+310% (142 Tickets)",
  },
  {
    title: "PO Deferrals",
    stageName: "Stage 4: Channel Order Postponement",
    date: "Aug 18, 2026",
    icon: "assignment_return",
    type: "causal",
    typeLabel: "Secondary Causal Driver",
    source: "EDI Gateway Orders (PO-HOLD-8821-29)",
    evidenceId: "EVID_CRM_PO_DEF_006",
    impact: "-$240K Held Purchase Orders (18.8% Attribution)",
    description: "29 purchase orders deferred by Tier-1 regional distributors due to warehouse fulfillment uncertainty and unconfirmed dispatch dates.",
    metricLabel: "Deferred Orders",
    metricValue: "29 Purchase Orders",
  },
  {
    title: "Horizon Promo",
    stageName: "Stage 5: Competitor Market Pressure",
    date: "Aug 20, 2026",
    icon: "storefront",
    type: "signal",
    typeLabel: "External Market Factor",
    source: "Market Intelligence Web Scrape (MKT-SCRAPE-HORIZON-08)",
    evidenceId: "EVID_MKT_HORIZON_PROMO_008",
    impact: "-$144K Elasticity Loss (11.3% Attribution)",
    description: "Automated web scraping detected Horizon Foods launching aggressive 15% discount promotions in the East territory, capturing deferred demand.",
    metricLabel: "Discount Depth",
    metricValue: "-15.0% Promotion",
  },
  {
    title: "Revenue Decline",
    stageName: "Stage 6: Fiscal Quarter Close Anomaly",
    date: "Aug 24, 2026",
    icon: "trending_down",
    type: "outcome",
    typeLabel: "Fiscal Variance Outcome",
    source: "General Ledger Financial Accounting",
    evidenceId: "EVID_FIN_GL_REV_Q3_001",
    impact: "-$1.23M Net Variance (-7.97% Deficit)",
    description: "Actual Q3 East territory revenue finalized at $14.20M against $15.43M baseline, cementing the critical negative variance anomaly.",
    metricLabel: "Total Shortfall",
    metricValue: "-$1,230,000.01",
  },
];

export default function RootCausePage() {
  const { persona, region, regionData, selectedDriverId, setSelectedDriverId } = useApp();
  const [data, setData] = useState<InvestigationResponse | null>(null);
  const [aiExplanation, setAiExplanation] = useState<AIExplanationResponse | null>(null);
  const [sortBy, setSortBy] = useState<"contrib" | "impact" | "conf">("contrib");
  const [controlFilter, setControlFilter] = useState<string>("ALL");
  const [eliminatedDrivers, setEliminatedDrivers] = useState<Record<string, boolean>>({});
  const [activeTimelineIdx, setActiveTimelineIdx] = useState<number>(1);

  useEffect(() => {
    async function loadInvestigation() {
      try {
        const res = await apiClient.getInvestigation("north_america_east_revenue", region, "2026-Q2", "2026-Q3");
        setData(res);
      } catch (e) {
        console.warn("Backend investigation fallback:", e);
      }
    }
    loadInvestigation();
  }, [region]);

  useEffect(() => {
    async function loadDriverExplanation() {
      try {
        const aiRes = await apiClient.getAIExplanation("north_america_east_revenue", {
          persona,
          driverId: selectedDriverId,
          region,
          prevPeriod: "2026-Q2",
          currPeriod: "2026-Q3",
        });
        setAiExplanation(aiRes);
      } catch (aiErr) {
        console.warn("AI reasoning fallback:", aiErr);
      }
    }
    loadDriverExplanation();
  }, [persona, selectedDriverId, region]);

  const rawDrivers = data?.drivers?.length ? data.drivers : DEFAULT_DRIVERS;

  // Filter & Sort
  const filteredDrivers = rawDrivers
    .filter((d) => {
      if (controlFilter === "ALL") return true;
      return d.controllability === controlFilter;
    })
    .sort((a, b) => {
      if (sortBy === "contrib") return b.contribution_pct - a.contribution_pct;
      if (sortBy === "impact") return a.impact_usd - b.impact_usd;
      if (sortBy === "conf") return b.confidence_score - a.confidence_score;
      return 0;
    });

  // Calculate dynamic residual deficit after simulated eliminations
  const totalEliminatedImpact = Object.keys(eliminatedDrivers).reduce((acc, dId) => {
    if (eliminatedDrivers[dId]) {
      const match = rawDrivers.find((d) => d.driver_id === dId);
      return acc + (match ? Math.abs(match.impact_usd) : 0);
    }
    return acc;
  }, 0);

  const baselineDeficitRaw = Math.abs(regionData.varianceRaw);
  const dynamicResidualDeficit = Math.max(0, baselineDeficitRaw - totalEliminatedImpact);

  const toggleEliminate = (e: React.MouseEvent, driverId: string) => {
    e.stopPropagation();
    setEliminatedDrivers((prev) => ({ ...prev, [driverId]: !prev[driverId] }));
  };

  const selectedMilestone = TIMELINE_MILESTONES[activeTimelineIdx] || TIMELINE_MILESTONES[1];

  return (
    <div className="flex min-h-screen bg-[#051424] text-on-surface">
      <Sidebar />

      <div className="flex-1 flex flex-col min-w-0">
        <TopBar breadcrumb="Insights (Root Cause)" />

        <main className="flex-1 p-6 md:p-8 space-y-6 max-w-[1600px] mx-auto w-full">
          {/* Header Summary Card with Live Residual Deficit Simulation */}
          <div className="bg-surface-container rounded-xl border border-outline-variant/30 p-5 flex flex-col md:flex-row md:items-center justify-between gap-4 shadow-sm">
            <div>
              <div className="flex items-center gap-2 mb-1.5">
                <span className="text-[10px] font-mono text-primary font-bold uppercase tracking-widest bg-primary/10 border border-primary/20 px-2 py-0.5 rounded flex items-center gap-1">
                  <span className="material-symbols-outlined text-[14px]">analytics</span>
                  Grounded Decomposition Engine
                </span>
                <span className="text-xs font-mono text-on-surface-variant">
                  Region: <strong className="text-on-surface">{region}</strong> • 2026-Q3 vs Baseline
                </span>
              </div>
              <h1 className="font-display font-extrabold text-2xl text-on-surface tracking-tight">
                Root Cause Investigation & Attribution
              </h1>
            </div>

            <div className="flex items-center gap-5 border-t md:border-t-0 md:border-l border-outline-variant/30 pt-3 md:pt-0 md:pl-6">
              <div>
                <div className="text-[10px] font-mono uppercase text-on-surface-variant mb-0.5 font-bold">
                  {Object.values(eliminatedDrivers).some(Boolean)
                    ? "Simulated Residual Deficit"
                    : "Target Anomaly Deficit"}
                </div>
                <div className="flex items-baseline gap-2">
                  <span className="font-display font-extrabold text-2xl text-error">
                    -${(dynamicResidualDeficit / 1000000).toFixed(2)}M
                  </span>
                  {Object.values(eliminatedDrivers).some(Boolean) ? (
                    <span className="text-xs font-mono text-primary font-bold">
                      +${(totalEliminatedImpact / 1000).toFixed(0)}K Addressed
                    </span>
                  ) : (
                    <span className="text-xs font-mono text-error font-bold flex items-center">
                      <span className="material-symbols-outlined text-[14px]">arrow_downward</span>
                      {regionData.variancePct}
                    </span>
                  )}
                </div>
              </div>

              <Link
                href="/decision-graph"
                className="px-3.5 py-2 bg-primary/15 text-primary border border-primary/30 hover:bg-primary hover:text-black rounded-lg font-mono text-xs font-bold transition-all flex items-center gap-1.5 shrink-0 shadow-sm"
              >
                <span>View Decision Graph</span>
                <span className="material-symbols-outlined text-[14px]">open_in_new</span>
              </Link>
            </div>
          </div>

          {/* Controls Bar: Sort, Filter, Telemetry (Evenly Distributed 3-Section Layout) */}
          <div className="flex flex-wrap items-center justify-between gap-4 bg-[#051424]/90 backdrop-blur-md p-3.5 rounded-xl border border-outline-variant/30 font-mono text-xs shadow-md">
            {/* Left Section: Sort Selection */}
            <div className="flex items-center gap-2.5">
              <span className="text-on-surface-variant text-[11px] uppercase font-bold tracking-wider">Sort By:</span>
              <div className="flex gap-1 bg-surface-dim p-1 rounded-lg border border-outline-variant/30">
                <button
                  onClick={() => setSortBy("contrib")}
                  className={`px-3 py-1 rounded-md text-xs transition-colors font-bold ${
                    sortBy === "contrib" ? "bg-primary text-black shadow-glow" : "text-on-surface-variant hover:text-on-surface"
                  }`}
                >
                  Contribution %
                </button>
                <button
                  onClick={() => setSortBy("impact")}
                  className={`px-3 py-1 rounded-md text-xs transition-colors font-bold ${
                    sortBy === "impact" ? "bg-primary text-black shadow-glow" : "text-on-surface-variant hover:text-on-surface"
                  }`}
                >
                  Impact $
                </button>
                <button
                  onClick={() => setSortBy("conf")}
                  className={`px-3 py-1 rounded-md text-xs transition-colors font-bold ${
                    sortBy === "conf" ? "bg-primary text-black shadow-glow" : "text-on-surface-variant hover:text-on-surface"
                  }`}
                >
                  Confidence
                </button>
              </div>
            </div>

            {/* Center Section: Controllability Filter (Utilizes Center Space Evenly) */}
            <div className="flex items-center gap-2.5">
              <span className="text-on-surface-variant text-[11px] uppercase font-bold tracking-wider">Controllability:</span>
              <div className="flex gap-1 bg-surface-dim p-1 rounded-lg border border-outline-variant/30">
                {["ALL", "HIGH", "MEDIUM", "LOW"].map((ctrl) => (
                  <button
                    key={ctrl}
                    onClick={() => setControlFilter(ctrl)}
                    className={`px-3 py-1 rounded-md text-xs transition-colors font-bold ${
                      controlFilter === ctrl ? "bg-primary text-black shadow-glow" : "text-on-surface-variant hover:text-on-surface"
                    }`}
                  >
                    {ctrl}
                  </button>
                ))}
              </div>
            </div>

            {/* Right Section: Active Telemetry & What-If Reset */}
            <div className="flex items-center gap-2.5">
              <div className="flex items-center gap-1.5 px-3 py-1 rounded-lg bg-surface-dim border border-outline-variant/30 text-on-surface-variant text-[11px]">
                <span className="inline-block w-1.5 h-1.5 rounded-full bg-primary animate-pulse"></span>
                <span className="text-on-surface font-bold">{filteredDrivers.length} Drivers</span>
                <span className="text-outline-variant/50">•</span>
                <span className="text-primary font-bold">94% Max Conf</span>
              </div>

              {Object.values(eliminatedDrivers).some(Boolean) && (
                <button
                  onClick={() => setEliminatedDrivers({})}
                  className="px-3 py-1 rounded-lg bg-error/15 text-error border border-error/30 text-xs font-bold hover:bg-error hover:text-black transition-colors"
                >
                  Reset What-If
                </button>
              )}
            </div>
          </div>

          {/* Main Grid Layout (Expanded Left Column: Rankings + Timeline, Streamlined Right Column: AI Reasoning + Evidence) */}
          <div className="grid grid-cols-1 xl:grid-cols-[1fr_350px] 2xl:grid-cols-[1fr_380px] gap-6">
            {/* Left Column (Expansive Width): Rankings + Interactive Timeline */}
            <div className="space-y-6 min-w-0">
              {/* Root Cause Ranking Section (Expanded Enterprise Height & Spacing) */}
              <section className="bg-surface-container rounded-2xl border border-outline-variant/20 p-6 flex flex-col shadow-xl">
                <div className="flex items-center justify-between mb-5 pb-3 border-b border-outline-variant/20">
                  <div className="flex items-center gap-2.5">
                    <div className="w-8 h-8 rounded-xl bg-primary/10 border border-primary/30 flex items-center justify-center text-primary">
                      <span className="material-symbols-outlined text-[20px]">format_list_numbered</span>
                    </div>
                    <h3 className="font-display font-bold text-base text-on-surface">
                      Root Cause Attribution Ranking ({filteredDrivers.length} Drivers)
                    </h3>
                  </div>
                  <span className="text-xs font-mono text-on-surface-variant hidden sm:inline">
                    Click card to spotlight & toggle What-If
                  </span>
                </div>

                <div className="space-y-3.5">
                  {filteredDrivers.map((d, idx) => {
                    const isSelected = selectedDriverId === d.driver_id;
                    const isEliminated = !!eliminatedDrivers[d.driver_id];
                    const isPrimary = idx === 0;

                    return (
                      <div
                        key={d.driver_id}
                        onClick={() => setSelectedDriverId(d.driver_id)}
                        className={`p-4 sm:p-5 rounded-2xl relative overflow-hidden cursor-pointer transition-all duration-200 border ${
                          isEliminated
                            ? "border-dashed border-outline-variant/40 bg-surface-dim/40 opacity-60"
                            : isSelected
                            ? "border-primary bg-surface-dim ring-2 ring-primary/60 shadow-glow"
                            : "border-outline-variant/30 bg-surface-dim/80 hover:border-primary/40"
                        }`}
                      >
                        {/* Background Progress Fill */}
                        {!isEliminated && (
                          <div
                            className={`absolute left-0 top-0 bottom-0 ${
                              isPrimary ? "bg-primary/15" : "bg-surface-container-high/40"
                            } transition-all duration-500 z-0`}
                            style={{ width: `${Math.min(100, Math.max(8, d.contribution_pct))}%` }}
                          />
                        )}

                        <div className="relative z-10 flex flex-col md:flex-row md:items-center justify-between gap-4">
                          <div className="flex-1">
                            <div className="flex items-center gap-2 mb-1.5 flex-wrap">
                              <span className="font-display font-bold text-sm sm:text-base text-on-surface">
                                #{d.rank || idx + 1} {d.driver_name}
                              </span>
                              {isPrimary && (
                                <span className="px-2.5 py-0.5 rounded-full bg-error/20 text-error font-mono text-[9px] font-bold uppercase border border-error/30">
                                  Primary Driver
                                </span>
                              )}
                              <span className="px-2 py-0.5 rounded-md bg-surface-container text-on-surface-variant font-mono text-[9px] border border-outline-variant/30">
                                {d.controllability} Controllability
                              </span>
                              {isEliminated && (
                                <span className="px-2 py-0.5 rounded-md bg-primary/20 text-primary font-mono text-[9px] font-bold">
                                  Mitigated in What-If
                                </span>
                              )}
                            </div>
                            <p className="text-xs text-on-surface-variant font-sans leading-relaxed">
                              {d.driver_id === "atlanta_dc_stockout"
                                ? "Prolonged inventory depletion for SKU-8821 leading to regional retail out-of-stocks."
                                : d.driver_id === "sku_8821_sales_volume"
                                ? "Core product velocity contraction across Tier-1 East territory accounts."
                                : d.driver_id === "distributor_orders"
                                ? "Key distribution partners postponed replenishment POs due to fulfillment lead-time uncertainty."
                                : "Horizon Foods initiated aggressive 15% promotional discount pressure in East territory."}
                            </p>
                          </div>

                          <div className="flex items-center gap-5 shrink-0 font-mono text-xs pt-1 md:pt-0 border-t md:border-t-0 border-outline-variant/20">
                            <div className="text-right">
                              <div className="text-[9px] text-on-surface-variant uppercase font-bold mb-0.5">Contribution</div>
                              <div className="font-display font-extrabold text-base text-primary">
                                {d.contribution_pct.toFixed(1)}%
                              </div>
                            </div>
                            <div className="text-right">
                              <div className="text-[9px] text-on-surface-variant uppercase font-bold mb-0.5">Confidence</div>
                              <div className="text-xs text-on-surface font-bold">
                                {d.confidence_score.toFixed(1)}%
                              </div>
                            </div>
                            <div className="text-right">
                              <div className="text-[9px] text-on-surface-variant uppercase font-bold mb-0.5">Impact</div>
                              <div className="text-xs font-bold text-error">
                                {formatCurrencyThousands(d.impact_usd)}
                              </div>
                            </div>

                            {/* What-If Mitigation Toggle */}
                            <button
                              onClick={(e) => toggleEliminate(e, d.driver_id)}
                              className={`p-2 rounded-xl border text-xs font-mono font-bold transition-all ${
                                isEliminated
                                  ? "bg-primary text-black border-primary shadow-glow"
                                  : "bg-surface-container text-on-surface-variant hover:text-primary border-outline-variant/30 hover:border-primary/40"
                              }`}
                              title={isEliminated ? "Restore driver" : "Simulate mitigating this driver"}
                            >
                              <span className="material-symbols-outlined text-[16px]">
                                {isEliminated ? "check" : "do_not_disturb_on"}
                              </span>
                            </button>
                          </div>
                        </div>
                      </div>
                    );
                  })}
                </div>
              </section>

              {/* Rich Interactive Sequence of Events Timeline (Expanded Enterprise Height) */}
              <section className="bg-surface-container rounded-2xl border border-outline-variant/20 p-6 flex flex-col space-y-5 shadow-xl">
                <div className="flex flex-wrap items-center justify-between gap-3 pb-3 border-b border-outline-variant/20">
                  <div className="flex items-center gap-2.5">
                    <div className="w-8 h-8 rounded-xl bg-primary/10 border border-primary/30 flex items-center justify-center text-primary">
                      <span className="material-symbols-outlined text-[20px]">timeline</span>
                    </div>
                    <h3 className="font-display font-bold text-base text-on-surface">
                      Sequence of Events (Click node to inspect milestone)
                    </h3>
                  </div>

                  <div className="flex items-center gap-3 font-mono text-[10px]">
                    <div className="flex items-center gap-1.5 bg-surface-dim px-2.5 py-1 rounded-md border border-outline-variant/30">
                      <span className="w-2.5 h-2.5 rounded-full bg-primary inline-block"></span>
                      <span className="text-on-surface-variant font-bold">Causal Driver</span>
                    </div>
                    <div className="flex items-center gap-1.5 bg-surface-dim px-2.5 py-1 rounded-md border border-outline-variant/30">
                      <span className="w-2.5 h-2.5 rounded-full bg-[#A4C9FE] inline-block"></span>
                      <span className="text-on-surface-variant font-bold">Correlated Signal</span>
                    </div>
                  </div>
                </div>

                {/* Horizontal Timeline Track (6-column responsive grid with expanded height) */}
                <div className="relative py-6 px-1">
                  <div className="relative w-full">
                    {/* Background Connecting Line */}
                    <div className="absolute top-[24px] left-[8%] right-[8%] h-1 bg-outline-variant/30 z-0 rounded-full"></div>

                    {/* Active Animated Glowing Progress Line */}
                    <div
                      className="absolute top-[24px] left-[8%] h-1 bg-primary z-0 rounded-full shadow-glow transition-all duration-300"
                      style={{ width: `${(activeTimelineIdx / (TIMELINE_MILESTONES.length - 1)) * 84}%` }}
                    ></div>

                    {/* Milestone Nodes in 6 Grid Columns (Full Text Visible, Zero Truncation) */}
                    <div className="grid grid-cols-6 gap-2 relative z-10">
                      {TIMELINE_MILESTONES.map((step, sIdx) => {
                        const isSelected = activeTimelineIdx === sIdx;
                        const isCausal = step.type === "causal";
                        const isOutcome = step.type === "outcome";

                        return (
                          <div
                            key={sIdx}
                            onClick={() => setActiveTimelineIdx(sIdx)}
                            className="flex flex-col items-center text-center cursor-pointer group px-1"
                          >
                            <div
                              className={`w-11 h-11 sm:w-12 sm:h-12 rounded-full flex items-center justify-center mb-2 border-2 transition-all group-hover:scale-110 ${
                                isSelected
                                  ? "bg-primary text-black border-primary shadow-glow ring-4 ring-primary/30 scale-110"
                                  : isCausal
                                  ? "bg-primary/20 border-primary text-primary shadow-[0_0_12px_rgba(79,222,200,0.4)]"
                                  : isOutcome
                                  ? "bg-error/20 border-error text-error shadow-[0_0_12px_rgba(255,180,171,0.4)]"
                                  : "bg-surface-dim border-[#A4C9FE]/50 text-[#A4C9FE]"
                              }`}
                            >
                              <span className="material-symbols-outlined text-[20px] sm:text-[22px]">{step.icon}</span>
                            </div>
                            <span
                              className={`text-[10px] sm:text-xs font-mono leading-tight whitespace-normal text-center ${
                                isSelected ? "font-bold text-primary" : "font-semibold text-on-surface"
                              }`}
                            >
                              {step.title}
                            </span>
                            <span className="text-[9px] font-mono text-on-surface-variant mt-1 whitespace-nowrap font-medium">
                              {step.date.replace(", 2026", "")}
                            </span>
                          </div>
                        );
                      })}
                    </div>
                  </div>
                </div>

                {/* Milestone Details Inspection Drawer (Expanded & 100% Full Text Visible) */}
                <div className="p-5 sm:p-6 rounded-2xl bg-surface-dim border border-primary/40 shadow-md space-y-4 font-mono text-xs">
                  <div className="flex flex-wrap items-center justify-between gap-2 pb-3 border-b border-outline-variant/30">
                    <div className="flex items-center gap-2.5">
                      <span className="text-primary font-bold text-sm sm:text-base font-display">
                        {selectedMilestone.stageName}
                      </span>
                      <span className="text-[11px] text-on-surface-variant font-mono">({selectedMilestone.date})</span>
                    </div>

                    <div className="flex items-center gap-2.5">
                      <span
                        className={`text-[10px] px-2.5 py-0.5 rounded-full font-bold uppercase ${
                          selectedMilestone.type === "causal"
                            ? "bg-primary/20 text-primary border border-primary/40"
                            : selectedMilestone.type === "outcome"
                            ? "bg-error/20 text-error border border-error/40"
                            : "bg-[#A4C9FE]/20 text-[#A4C9FE] border border-[#A4C9FE]/40"
                        }`}
                      >
                        {selectedMilestone.typeLabel}
                      </span>

                      {/* Stepper Navigation Buttons */}
                      <div className="flex items-center gap-1">
                        <button
                          disabled={activeTimelineIdx === 0}
                          onClick={() => setActiveTimelineIdx((prev) => Math.max(0, prev - 1))}
                          className="p-1.5 rounded-lg bg-surface-container border border-outline-variant/30 text-on-surface-variant hover:text-on-surface disabled:opacity-30 disabled:pointer-events-none transition-colors"
                          title="Previous milestone"
                        >
                          <span className="material-symbols-outlined text-[16px]">chevron_left</span>
                        </button>
                        <button
                          disabled={activeTimelineIdx === TIMELINE_MILESTONES.length - 1}
                          onClick={() =>
                            setActiveTimelineIdx((prev) => Math.min(TIMELINE_MILESTONES.length - 1, prev + 1))
                          }
                          className="p-1.5 rounded-lg bg-surface-container border border-outline-variant/30 text-on-surface-variant hover:text-on-surface disabled:opacity-30 disabled:pointer-events-none transition-colors"
                          title="Next milestone"
                        >
                          <span className="material-symbols-outlined text-[16px]">chevron_right</span>
                        </button>
                      </div>
                    </div>
                  </div>

                  <p className="font-sans text-xs sm:text-sm text-on-surface leading-relaxed">
                    {selectedMilestone.description}
                  </p>

                  <div className="grid grid-cols-1 md:grid-cols-3 gap-3.5 pt-1 text-xs">
                    {/* Source Telemetry Card (Full Text, No Truncation) */}
                    <div className="p-3.5 rounded-xl bg-surface-container border border-outline-variant/30 flex flex-col justify-between min-w-0">
                      <span className="text-[9px] text-on-surface-variant uppercase font-bold tracking-wider mb-1">
                        Source Telemetry
                      </span>
                      <span className="text-on-surface text-xs font-semibold leading-relaxed break-words">
                        {selectedMilestone.source}
                      </span>
                    </div>

                    {/* Metric Card (Full Text, No Truncation) */}
                    <div className="p-3.5 rounded-xl bg-surface-container border border-outline-variant/30 flex flex-col justify-between min-w-0">
                      <span className="text-[9px] text-on-surface-variant uppercase font-bold tracking-wider mb-1">
                        {selectedMilestone.metricLabel}
                      </span>
                      <span className="text-primary text-xs font-bold leading-relaxed break-words">
                        {selectedMilestone.metricValue}
                      </span>
                    </div>

                    {/* Evidence ID & Action Card (Full Text, No Truncation) */}
                    <div className="p-3.5 rounded-xl bg-surface-container border border-outline-variant/30 flex flex-col justify-between gap-2.5 min-w-0">
                      <div>
                        <span className="text-[9px] text-on-surface-variant uppercase font-bold tracking-wider mb-1 block">
                          Evidence ID
                        </span>
                        <span className="text-primary text-xs font-mono font-bold leading-tight break-all block">
                          {selectedMilestone.evidenceId}
                        </span>
                      </div>

                      <Link
                        href={`/evidence?q=${selectedMilestone.evidenceId}`}
                        className="w-full py-1.5 rounded-lg bg-primary/15 text-primary hover:bg-primary hover:text-black border border-primary/30 text-xs font-bold transition-all flex items-center justify-center gap-1.5 shadow-sm text-center"
                      >
                        <span>Inspect Evidence</span>
                        <span className="material-symbols-outlined text-[14px]">open_in_new</span>
                      </Link>
                    </div>
                  </div>
                </div>
              </section>
            </div>

            {/* Right Column (Streamlined Width): AI Reasoning + Evidence Points */}
            <div className="space-y-6 min-w-0">
              {/* AI Reasoning Panel (Expanded & Richly Detailed) */}
              <section className="glass-panel rounded-2xl border border-primary/30 p-6 bg-gradient-to-br from-primary-container/15 via-surface-container/90 to-surface shadow-xl flex flex-col justify-between">
                <div className="flex items-center justify-between mb-4 pb-3 border-b border-outline-variant/30">
                  <div className="flex items-center gap-2.5">
                    <div className="w-8 h-8 rounded-xl bg-primary/10 border border-primary/30 flex items-center justify-center text-primary">
                      <span className="material-symbols-outlined text-[20px]">psychology</span>
                    </div>
                    <h3 className="font-display font-bold text-base text-on-surface">Grounded AI Reasoning</h3>
                  </div>
                  <span className="font-mono text-[10px] text-primary uppercase font-bold bg-primary/10 border border-primary/30 px-2.5 py-1 rounded-full">
                    {persona} VIEW
                  </span>
                </div>

                <div className="space-y-4 text-xs font-mono">
                  <div className="flex gap-3.5 p-3.5 rounded-xl bg-surface-dim/80 border border-outline-variant/20">
                    <div className="w-1.5 bg-primary rounded-full shrink-0"></div>
                    <div>
                      <div className="flex items-center justify-between gap-2 mb-1">
                        <span className="text-on-surface font-bold text-xs">
                          Driver Lens: {selectedDriverId.replace(/_/g, " ").toUpperCase()}
                        </span>
                        <span className="text-error font-bold text-[11px]">-$550K Impact</span>
                      </div>
                      <p className="text-on-surface-variant font-sans leading-relaxed text-xs">
                        {aiExplanation?.explanation?.summary ||
                          "Atlanta DC inventory depletion (43.2% causal share) preceded regional order cancellations. Causal engine confirms 14-day stockout as primary bottleneck."}
                      </p>
                    </div>
                  </div>

                  <div className="flex gap-3.5 p-3.5 rounded-xl bg-surface-dim/80 border border-outline-variant/20">
                    <div className="w-1.5 bg-[#A4C9FE] rounded-full shrink-0"></div>
                    <div>
                      <div className="flex items-center justify-between gap-2 mb-1">
                        <span className="text-on-surface font-bold text-xs">Cross-Silo Correlation</span>
                        <span className="text-primary font-bold text-[11px]">94% Confidence</span>
                      </div>
                      <p className="text-on-surface-variant font-sans leading-relaxed text-xs">
                        SAP inventory zero-stock triggers synchronized with +310% Zendesk customer support escalations and 29 distributor purchase order deferrals.
                      </p>
                    </div>
                  </div>

                  <div className="flex gap-3.5 p-3.5 rounded-xl bg-surface-dim/80 border border-outline-variant/20">
                    <div className="w-1.5 bg-secondary rounded-full shrink-0"></div>
                    <div>
                      <div className="flex items-center justify-between gap-2 mb-1">
                        <span className="text-on-surface font-bold text-xs">Prescriptive Feasibility</span>
                        <span className="text-primary font-bold text-[11px]">+$484K Modeled Lift</span>
                      </div>
                      <p className="text-on-surface-variant font-sans leading-relaxed text-xs">
                        Rebalancing buffer stock from Chicago Hub recovers 61.6% of addressable deficit within a 14-day delivery window with zero factory retooling.
                      </p>
                    </div>
                  </div>
                </div>
              </section>

              {/* Evidence Sidebar (Expanded Height & Rich Cards) */}
              <section className="bg-surface-container rounded-2xl border border-outline-variant/20 p-6 flex flex-col space-y-4 shadow-xl">
                <div className="flex items-center justify-between pb-3 border-b border-outline-variant/30">
                  <div className="flex items-center gap-2.5">
                    <div className="w-8 h-8 rounded-xl bg-primary/10 border border-primary/30 flex items-center justify-center text-primary">
                      <span className="material-symbols-outlined text-[18px]">verified</span>
                    </div>
                    <h3 className="font-display font-bold text-base text-on-surface">
                      Verified Evidence Ledger
                    </h3>
                  </div>
                  <span className="bg-primary/10 text-primary border border-primary/20 px-2.5 py-0.5 rounded-md text-[10px] font-mono font-bold">
                    4 Cryptographically Verified
                  </span>
                </div>

                <div className="space-y-2.5">
                  {[
                    {
                      id: "EVID_ERP_ATL_STOCKOUT_001",
                      type: "ERP Snapshot",
                      title: "Atlanta DC Inventory Daily Snapshot (INV-SNAP-21971)",
                      meta: "14 Consecutive Days Zero-Stock",
                      hash: "e3b0c442...7852b855",
                    },
                    {
                      id: "EVID_ZENDESK_ATL_DELAY_003",
                      type: "Support CRM",
                      title: "Zendesk 'Out of Stock' ticket cluster surge (+310%)",
                      meta: "142 Regional Customer Inquiries",
                      hash: "7f83b165...7e24088b",
                    },
                    {
                      id: "EVID_CRM_PO_DEF_006",
                      type: "Sales EDI",
                      title: "Regional Distributor PO Deferral Memos (29 delayed POs)",
                      meta: "29 Purchase Orders Held ($240K)",
                      hash: "4b227777...d820ca21",
                    },
                    {
                      id: "EVID_MKT_HORIZON_PROMO_008",
                      type: "Market Intel",
                      title: "Competitor Horizon Foods Promotional Scrape (-15%)",
                      meta: "Regional Price Promo Defense",
                      hash: "ef2d127d...8e192c73",
                    },
                  ].map((ev) => (
                    <Link
                      key={ev.id}
                      href={`/evidence?q=${ev.id}`}
                      className="block p-3.5 rounded-xl bg-surface-dim hover:bg-surface-bright/30 border border-outline-variant/30 hover:border-primary/50 transition-all group shadow-sm"
                    >
                      <div className="flex justify-between items-center mb-1.5">
                        <span className="font-mono text-[11px] font-bold text-primary group-hover:text-primary-light flex items-center gap-1">
                          <span className="material-symbols-outlined text-[13px]">lock</span>
                          {ev.id}
                        </span>
                        <span className="text-[9px] uppercase tracking-wider text-on-surface-variant font-mono bg-surface-container px-2 py-0.5 rounded border border-outline-variant/20 font-bold">
                          {ev.type}
                        </span>
                      </div>
                      <p className="text-xs text-on-surface font-sans leading-snug mb-2 font-medium">{ev.title}</p>
                      <div className="flex items-center justify-between text-[10px] font-mono text-on-surface-variant/70 pt-1.5 border-t border-outline-variant/20">
                        <span className="text-primary font-bold">{ev.meta}</span>
                        <span className="font-mono text-[9px]">SHA: {ev.hash}</span>
                      </div>
                    </Link>
                  ))}
                </div>

                <Link
                  href="/evidence"
                  className="w-full text-center py-2.5 rounded-xl bg-surface-dim border border-outline-variant/40 hover:border-primary/50 text-primary font-mono text-xs font-bold transition-all block mt-2 shadow-sm hover:bg-primary/10"
                >
                  View All Evidence in Explorer →
                </Link>
              </section>
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}
