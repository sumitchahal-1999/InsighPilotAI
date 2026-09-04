"use client";

import React, { useState } from "react";
import { Sidebar } from "@/components/navigation/Sidebar";
import { TopBar } from "@/components/navigation/TopBar";
import { useApp } from "@/context/AppContext";
import { apiClient } from "@/lib/api";
import { SimulationResult } from "@/lib/types";
import Link from "next/link";

export default function RecommendationsPage() {
  const { region, regionData } = useApp();
  const [availabilityVal, setAvailabilityVal] = useState<number>(90.0);
  const [freightDaysVal, setFreightDaysVal] = useState<number>(7);
  const [discountConcessionVal, setDiscountConcessionVal] = useState<number>(2.5);

  const [dispatchedActions, setDispatchedActions] = useState<Record<string, boolean>>({});
  const [activeMatrixSpotlight, setActiveMatrixSpotlight] = useState<number>(1);
  const [showDispatchModal, setShowDispatchModal] = useState<boolean>(false);
  const [activeDispatchItem, setActiveDispatchItem] = useState<{ id: string; title: string; units: number; poNumber: string } | null>(null);

  // Compute live multi-lever elasticity
  const baselineAvail = 79.4;
  const deltaAvail = Math.max(0, availabilityVal - baselineAvail);
  const availRecovery = deltaAvail * 32209.71;
  const freightSpeedBonus = Math.max(0, (14 - freightDaysVal) * 8500);
  const concessionCost = (discountConcessionVal / 100) * 180000 * 0.4;

  const totalDynamicRecovery = availRecovery + freightSpeedBonus - concessionCost;
  const projectedTotalRevenue = regionData.revenueRaw + totalDynamicRecovery;
  const projectedMarginLift = parseFloat(((deltaAvail * 0.132) + ((14 - freightDaysVal) * 0.04) - (discountConcessionVal * 0.05)).toFixed(1));

  const handleAuthorizeAction = (actionId: string, title: string, units: number) => {
    const randomPo = `SAP-PO-2026-${Math.floor(1000 + Math.random() * 9000)}-ATL`;
    setActiveDispatchItem({ id: actionId, title, units, poNumber: randomPo });
    setShowDispatchModal(true);
  };

  const confirmDispatch = () => {
    if (activeDispatchItem) {
      setDispatchedActions((prev) => ({ ...prev, [activeDispatchItem.id]: true }));
    }
    setShowDispatchModal(false);
  };

  return (
    <div className="flex min-h-screen bg-[#051424] text-on-surface">
      <Sidebar />

      <div className="flex-1 flex flex-col min-w-0">
        <TopBar breadcrumb="Recommendations & What-If" />

        <main className="flex-1 p-6 md:p-8 space-y-6 max-w-[1600px] mx-auto w-full">
          {/* Header Bar */}
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-2">
            <div>
              <div className="flex items-center gap-2 mb-1.5">
                <span className="text-[10px] font-mono text-primary font-bold uppercase tracking-widest bg-primary/10 border border-primary/20 px-2 py-0.5 rounded flex items-center gap-1">
                  <span className="material-symbols-outlined text-[14px]">auto_awesome</span>
                  Prescriptive Interventions
                </span>
                <span className="text-xs font-mono text-on-surface-variant">
                  Region: <strong className="text-on-surface">{region}</strong> • Dynamic Multi-Lever Simulator
                </span>
              </div>
              <h1 className="font-display font-extrabold text-2xl text-on-surface tracking-tight">
                Recommendations & What-If Simulation
              </h1>
            </div>

            <div className="flex items-center gap-3">
              <Link
                href="/briefing"
                className="bg-primary-container text-on-primary-container font-mono text-xs font-bold px-4 py-2 rounded-lg hover:bg-primary transition-colors flex items-center gap-2 shadow-glow"
              >
                <span className="material-symbols-outlined text-[16px]">description</span>
                <span>Generate Boardroom Briefing</span>
              </Link>
            </div>
          </div>

          {/* Main 2-Column Grid */}
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
            {/* Left Column (5 cols): Action Strategy Cards */}
            <div className="lg:col-span-5 space-y-4">
              {/* Priority 1 Card */}
              <div
                className={`glass-panel rounded-xl p-5 border transition-all duration-200 flex flex-col justify-between shadow-glow relative ${
                  activeMatrixSpotlight === 1
                    ? "border-primary bg-gradient-to-br from-primary-container/20 via-surface-container to-surface ring-2 ring-primary/60"
                    : "border-primary/40 bg-surface-container/70"
                }`}
              >
                <div>
                  <div className="flex justify-between items-start mb-3">
                    <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded bg-primary/20 text-primary border border-primary/40 font-mono text-[10px] font-bold uppercase">
                      Priority 1 • Critical Action
                    </span>
                    <span className="font-mono text-xs text-primary font-bold">91% Conf</span>
                  </div>

                  <h3 className="font-display font-bold text-base text-on-surface leading-tight mb-3">
                    Emergency Stock Transfer (Chicago → Atlanta)
                  </h3>

                  <div className="grid grid-cols-3 gap-2.5 mb-3 font-mono text-xs">
                    <div className="bg-surface-container p-2.5 rounded-lg border border-outline-variant/30 text-center">
                      <div className="text-[9px] text-on-surface-variant uppercase font-bold mb-0.5">Recovery</div>
                      <div className="font-display font-bold text-sm text-primary">+$484K</div>
                    </div>
                    <div className="bg-surface-container p-2.5 rounded-lg border border-outline-variant/30 text-center">
                      <div className="text-[9px] text-on-surface-variant uppercase font-bold mb-0.5">Margin Lift</div>
                      <div className="font-display font-bold text-sm text-on-surface">+1.2 pts</div>
                    </div>
                    <div className="bg-surface-container p-2.5 rounded-lg border border-outline-variant/30 text-center">
                      <div className="text-[9px] text-on-surface-variant uppercase font-bold mb-0.5">Lead Time</div>
                      <div className="font-display font-bold text-sm text-on-surface">{freightDaysVal} Days</div>
                    </div>
                  </div>

                  <p className="text-xs text-on-surface-variant font-sans leading-relaxed mb-4">
                    Transfer 3,200 surplus units of SKU-8821 from Chicago Central DC to Atlanta DC via expedited freight to restore regional inventory availability from 79.4% to {availabilityVal.toFixed(1)}%.
                  </p>
                </div>

                <div className="pt-3 border-t border-outline-variant/30 flex items-center justify-between font-mono text-xs">
                  <div className="flex items-center gap-2">
                    <div className="w-6 h-6 rounded-full bg-primary/20 text-primary flex items-center justify-center font-bold text-[10px]">
                      SC
                    </div>
                    <div>
                      <span className="text-[9px] text-on-surface-variant block">Owner</span>
                      <span className="text-[11px] font-sans font-semibold text-on-surface">Supply Chain Ops</span>
                    </div>
                  </div>

                  <button
                    onClick={() => handleAuthorizeAction("stock_transfer", "Emergency Stock Transfer", 3200)}
                    disabled={dispatchedActions.stock_transfer}
                    className={`px-3.5 py-1.5 rounded-lg font-mono text-xs font-bold transition-all flex items-center gap-1.5 ${
                      dispatchedActions.stock_transfer
                        ? "bg-success/20 text-success border border-success/40"
                        : "bg-primary text-black hover:bg-primary-light shadow-glow"
                    }`}
                  >
                    <span className="material-symbols-outlined text-[14px]">
                      {dispatchedActions.stock_transfer ? "check_circle" : "bolt"}
                    </span>
                    <span>{dispatchedActions.stock_transfer ? "In-Transit (Dispatched)" : "Authorize Transfer"}</span>
                  </button>
                </div>
              </div>

              {/* Priority 2 Card */}
              <div
                className={`glass-panel rounded-xl p-5 border transition-all duration-200 flex flex-col justify-between ${
                  activeMatrixSpotlight === 2
                    ? "border-secondary bg-surface-container ring-2 ring-secondary/60"
                    : "border-outline-variant/30 bg-surface-container/70"
                }`}
              >
                <div>
                  <div className="flex justify-between items-start mb-3">
                    <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded bg-surface-container text-on-surface-variant border border-outline-variant/30 font-mono text-[10px] font-bold uppercase">
                      Priority 2 • High Action
                    </span>
                    <span className="font-mono text-xs text-on-surface-variant font-bold">85% Conf</span>
                  </div>

                  <h3 className="font-display font-bold text-base text-on-surface leading-tight mb-3">
                    Distributor Recovery Outreach
                  </h3>

                  <div className="grid grid-cols-3 gap-2.5 mb-3 font-mono text-xs">
                    <div className="bg-surface-dim p-2.5 rounded-lg border border-outline-variant/30 text-center">
                      <div className="text-[9px] text-on-surface-variant uppercase font-bold mb-0.5">Recovery</div>
                      <div className="font-display font-bold text-sm text-primary">+$180K</div>
                    </div>
                    <div className="bg-surface-dim p-2.5 rounded-lg border border-outline-variant/30 text-center">
                      <div className="text-[9px] text-on-surface-variant uppercase font-bold mb-0.5">Margin Lift</div>
                      <div className="font-display font-bold text-sm text-on-surface">+0.6 pts</div>
                    </div>
                    <div className="bg-surface-dim p-2.5 rounded-lg border border-outline-variant/30 text-center">
                      <div className="text-[9px] text-on-surface-variant uppercase font-bold mb-0.5">Lead Time</div>
                      <div className="font-display font-bold text-sm text-on-surface">21 Days</div>
                    </div>
                  </div>

                  <p className="text-xs text-on-surface-variant font-sans leading-relaxed mb-4">
                    Deploy dedicated commercial sales account managers with priority delivery guarantees to capture 29 deferred distributor purchase orders before the quarter close.
                  </p>
                </div>

                <div className="pt-3 border-t border-outline-variant/30 flex items-center justify-between font-mono text-xs">
                  <div className="flex items-center gap-2">
                    <div className="w-6 h-6 rounded-full bg-secondary/20 text-secondary flex items-center justify-center font-bold text-[10px]">
                      CS
                    </div>
                    <div>
                      <span className="text-[9px] text-on-surface-variant block">Owner</span>
                      <span className="text-[11px] font-sans font-semibold text-on-surface">Commercial Sales</span>
                    </div>
                  </div>

                  <button
                    onClick={() => handleAuthorizeAction("distributor_outreach", "Distributor Recovery Outreach", 29)}
                    disabled={dispatchedActions.distributor_outreach}
                    className={`px-3 py-1.5 rounded-lg font-mono text-xs font-bold transition-all flex items-center gap-1.5 ${
                      dispatchedActions.distributor_outreach
                        ? "bg-success/20 text-success border border-success/40"
                        : "bg-surface-dim hover:bg-secondary/20 text-secondary border border-secondary/40"
                    }`}
                  >
                    <span className="material-symbols-outlined text-[14px]">
                      {dispatchedActions.distributor_outreach ? "check_circle" : "send"}
                    </span>
                    <span>{dispatchedActions.distributor_outreach ? "Outreach Active" : "Launch Outreach"}</span>
                  </button>
                </div>
              </div>
            </div>

            {/* Right Column (7 cols): Prioritization Matrix + Multi-Lever Simulator */}
            <div className="lg:col-span-7 space-y-5">
              {/* Impact vs Effort Matrix */}
              <div className="glass-panel rounded-xl p-5 border border-outline-variant/30 bg-surface-container/60">
                <div className="flex items-center justify-between mb-3">
                  <h3 className="font-mono text-xs text-on-surface-variant uppercase tracking-wider font-bold flex items-center gap-2">
                    <span className="material-symbols-outlined text-[16px]">grid_view</span>
                    Action Prioritization Matrix (Click dot to focus)
                  </h3>
                  <span className="text-[10px] font-mono text-primary">Interactive 2x2 Plot</span>
                </div>

                {/* Interactive 2x2 Prioritization Matrix */}
                <div className="relative w-full h-[210px] bg-surface-dim/90 border border-outline-variant/30 rounded-xl p-4 font-mono overflow-hidden select-none">
                  {/* 4 Quadrant Background Tints */}
                  <div className="absolute inset-0 grid grid-cols-2 grid-rows-2 pointer-events-none opacity-40">
                    <div className="border-r border-b border-outline-variant/30 bg-primary/5 flex items-start justify-start p-2.5">
                      <span className="text-[8px] text-primary font-bold uppercase tracking-widest">
                        Quick Wins (High ROI)
                      </span>
                    </div>
                    <div className="border-b border-outline-variant/30 bg-surface-container/20 flex items-start justify-end p-2.5">
                      <span className="text-[8px] text-on-surface-variant uppercase tracking-widest">
                        Strategic Bets
                      </span>
                    </div>
                    <div className="border-r border-outline-variant/30 bg-surface-container/20 flex items-end justify-start p-2.5">
                      <span className="text-[8px] text-on-surface-variant uppercase tracking-widest">
                        Low Effort / Low Impact
                      </span>
                    </div>
                    <div className="bg-surface-dim flex items-end justify-end p-2.5">
                      <span className="text-[8px] text-on-surface-variant/60 uppercase tracking-widest">
                        De-Prioritized
                      </span>
                    </div>
                  </div>

                  {/* Axis Labels */}
                  <div className="absolute top-2 left-1/2 -translate-x-1/2 text-[9px] text-primary font-bold uppercase z-10">
                    ▲ High Impact
                  </div>
                  <div className="absolute bottom-2 left-1/2 -translate-x-1/2 text-[9px] text-on-surface-variant uppercase z-10">
                    ▼ Low Impact
                  </div>
                  <div className="absolute top-1/2 right-2 -translate-y-1/2 text-[9px] text-on-surface-variant uppercase rotate-90 origin-right z-10">
                    High Effort ▶
                  </div>
                  <div className="absolute top-1/2 left-2 -translate-y-1/2 text-[9px] text-on-surface-variant uppercase -rotate-90 origin-left z-10">
                    ◀ Low Effort
                  </div>

                  {/* Axis Lines */}
                  <div className="absolute inset-x-6 top-1/2 h-px bg-outline-variant/40 border-dashed z-0"></div>
                  <div className="absolute inset-y-6 left-1/2 w-px bg-outline-variant/40 border-dashed z-0"></div>

                  {/* Point 1: Emergency Stock Transfer (High Impact, Low Effort) */}
                  <div
                    onClick={() => setActiveMatrixSpotlight(1)}
                    className="absolute top-[24%] left-[26%] -translate-x-1/2 -translate-y-1/2 z-20 cursor-pointer group"
                  >
                    <div className="flex items-center gap-2">
                      <div className="w-6 h-6 rounded-full bg-primary flex items-center justify-center text-[11px] font-bold text-black shadow-glow animate-pulse group-hover:scale-125 transition-transform shrink-0">
                        1
                      </div>
                      <div className="bg-[#051424]/95 border border-primary/50 px-2.5 py-1 rounded-md text-[10px] whitespace-nowrap shadow-xl text-primary font-bold group-hover:border-primary">
                        Emerg Transfer (+$484K)
                      </div>
                    </div>
                  </div>

                  {/* Point 2: Distributor Outreach (Moderate Impact, Low-Mid Effort) */}
                  <div
                    onClick={() => setActiveMatrixSpotlight(2)}
                    className="absolute top-[60%] left-[20%] -translate-x-1/2 -translate-y-1/2 z-20 cursor-pointer group"
                  >
                    <div className="flex items-center gap-2">
                      <div className="w-6 h-6 rounded-full bg-[#A4C9FE] flex items-center justify-center text-[11px] font-bold text-black shadow-sm group-hover:scale-125 transition-transform shrink-0">
                        2
                      </div>
                      <div className="bg-[#051424]/95 border border-[#A4C9FE]/50 px-2.5 py-1 rounded-md text-[10px] whitespace-nowrap shadow-xl text-[#A4C9FE] font-bold group-hover:border-[#A4C9FE]">
                        Distr Outreach (+$180K)
                      </div>
                    </div>
                  </div>

                  {/* Point 3: Pricing Defense (Lower Impact, Higher Effort) */}
                  <div
                    onClick={() => setActiveMatrixSpotlight(3)}
                    className="absolute top-[68%] left-[72%] -translate-x-1/2 -translate-y-1/2 z-20 cursor-pointer group"
                  >
                    <div className="flex items-center gap-2">
                      <div className="w-5 h-5 rounded-full bg-surface-container-high border border-outline-variant flex items-center justify-center text-[10px] font-bold text-on-surface group-hover:scale-125 transition-transform shrink-0">
                        3
                      </div>
                      <div className="bg-[#051424]/95 border border-outline-variant/60 px-2 py-0.5 rounded-md text-[10px] whitespace-nowrap shadow-lg text-on-surface-variant group-hover:text-on-surface">
                        Pricing Defense (+$93.6K)
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              {/* Multi-Lever What-If Simulation Engine */}
              <div className="glass-panel rounded-xl p-5 border border-primary/30 bg-gradient-to-br from-surface-container via-surface to-surface-dim space-y-4 shadow-sm">
                <div className="flex justify-between items-center pb-2 border-b border-outline-variant/30">
                  <h3 className="font-display font-bold text-base text-on-surface flex items-center gap-2">
                    <span className="material-symbols-outlined text-primary text-[20px]">science</span>
                    Multi-Lever What-If Scenario Simulator
                  </h3>
                  <span className="font-mono text-[10px] text-primary bg-primary/10 border border-primary/30 px-2 py-0.5 rounded font-bold">
                    91.0% Conf (HIGH)
                  </span>
                </div>

                {/* 3 Interactive Sliders */}
                <div className="space-y-3 font-mono text-xs">
                  {/* Slider 1: Target Availability */}
                  <div className="bg-surface-dim p-3 rounded-lg border border-outline-variant/30 space-y-1">
                    <div className="flex justify-between items-center">
                      <span className="text-on-surface font-semibold">1. Atlanta DC Availability Target:</span>
                      <span className="text-primary font-bold">{availabilityVal.toFixed(1)}%</span>
                    </div>
                    <input
                      type="range"
                      min="79.4"
                      max="100.0"
                      step="0.5"
                      value={availabilityVal}
                      onChange={(e) => setAvailabilityVal(parseFloat(e.target.value))}
                      className="w-full h-1.5 bg-surface-container rounded-lg appearance-none cursor-pointer accent-primary"
                    />
                    <div className="flex justify-between text-[9px] text-on-surface-variant">
                      <span>Baseline: 79.4%</span>
                      <span>Target: 90.0%</span>
                      <span>Max: 100.0%</span>
                    </div>
                  </div>

                  {/* Slider 2: Freight Transit SLA */}
                  <div className="bg-surface-dim p-3 rounded-lg border border-outline-variant/30 space-y-1">
                    <div className="flex justify-between items-center">
                      <span className="text-on-surface font-semibold">2. Freight Transit SLA:</span>
                      <span className="text-primary font-bold">{freightDaysVal} Days</span>
                    </div>
                    <input
                      type="range"
                      min="3"
                      max="14"
                      step="1"
                      value={freightDaysVal}
                      onChange={(e) => setFreightDaysVal(parseInt(e.target.value))}
                      className="w-full h-1.5 bg-surface-container rounded-lg appearance-none cursor-pointer accent-primary"
                    />
                    <div className="flex justify-between text-[9px] text-on-surface-variant">
                      <span>Expedited: 3 Days</span>
                      <span>Standard: 7 Days</span>
                      <span>Relaxed: 14 Days</span>
                    </div>
                  </div>

                  {/* Slider 3: Distributor Concession */}
                  <div className="bg-surface-dim p-3 rounded-lg border border-outline-variant/30 space-y-1">
                    <div className="flex justify-between items-center">
                      <span className="text-on-surface font-semibold">3. Priority PO Concession Discount:</span>
                      <span className="text-primary font-bold">{discountConcessionVal.toFixed(1)}%</span>
                    </div>
                    <input
                      type="range"
                      min="0"
                      max="10"
                      step="0.5"
                      value={discountConcessionVal}
                      onChange={(e) => setDiscountConcessionVal(parseFloat(e.target.value))}
                      className="w-full h-1.5 bg-surface-container rounded-lg appearance-none cursor-pointer accent-primary"
                    />
                    <div className="flex justify-between text-[9px] text-on-surface-variant">
                      <span>None: 0%</span>
                      <span>Moderate: 2.5%</span>
                      <span>Aggressive: 10%</span>
                    </div>
                  </div>
                </div>

                {/* Live Mathematical Elasticity Output Cards */}
                <div className="grid grid-cols-3 gap-3 font-mono text-xs">
                  <div className="bg-surface-container p-3 rounded-lg border border-primary/40 text-center shadow-glow">
                    <div className="text-[9px] text-on-surface-variant uppercase font-bold mb-1">Projected Recovery</div>
                    <div className="font-display font-bold text-lg md:text-xl text-primary">
                      +${(totalDynamicRecovery / 1000).toFixed(1)}K
                    </div>
                  </div>

                  <div className="bg-surface-container p-3 rounded-lg border border-outline-variant/30 text-center">
                    <div className="text-[9px] text-on-surface-variant uppercase font-bold mb-1">Projected Revenue</div>
                    <div className="font-display font-bold text-lg md:text-xl text-on-surface">
                      ${(projectedTotalRevenue / 1000000).toFixed(2)}M
                    </div>
                  </div>

                  <div className="bg-surface-container p-3 rounded-lg border border-outline-variant/30 text-center">
                    <div className="text-[9px] text-on-surface-variant uppercase font-bold mb-1">Margin Delta</div>
                    <div className="font-display font-bold text-lg md:text-xl text-on-surface">
                      +{projectedMarginLift.toFixed(1)} pts
                    </div>
                  </div>
                </div>

                <div className="flex items-center justify-between pt-2 border-t border-outline-variant/30 font-mono text-[10px] text-on-surface-variant">
                  <span className="flex items-center gap-1">
                    <span className="material-symbols-outlined text-[14px]">calculate</span>
                    Multi-Factor Elasticity Ratio: 0.73
                  </span>
                  <span className="text-primary font-bold">Deterministic Financial Model</span>
                </div>
              </div>
            </div>
          </div>

          {/* Interactive Dispatch Confirmation Modal */}
          {showDispatchModal && activeDispatchItem && (
            <div className="fixed inset-0 z-50 bg-black/75 backdrop-blur-sm flex items-center justify-center p-4">
              <div className="bg-surface-container border border-primary/50 rounded-2xl max-w-md w-full p-6 shadow-glow space-y-4 font-mono">
                <div className="flex items-center gap-3 border-b border-outline-variant/30 pb-3">
                  <div className="w-10 h-10 rounded-xl bg-primary/20 text-primary border border-primary/40 flex items-center justify-center">
                    <span className="material-symbols-outlined text-2xl">local_shipping</span>
                  </div>
                  <div>
                    <h3 className="font-display font-bold text-base text-on-surface">Confirm Action Dispatch</h3>
                    <span className="text-[11px] text-primary">{activeDispatchItem.title}</span>
                  </div>
                </div>

                <div className="p-3 bg-surface-dim rounded-xl border border-outline-variant/30 space-y-2 text-xs">
                  <div className="flex justify-between">
                    <span className="text-on-surface-variant">Generated SAP Order:</span>
                    <strong className="text-on-surface">{activeDispatchItem.poNumber}</strong>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-on-surface-variant">Target Freight SLA:</span>
                    <strong className="text-primary">{freightDaysVal} Business Days</strong>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-on-surface-variant">Expected Recovery Lift:</span>
                    <strong className="text-primary">+${(totalDynamicRecovery / 1000).toFixed(1)}K</strong>
                  </div>
                </div>

                <div className="flex gap-3 pt-2">
                  <button
                    onClick={() => setShowDispatchModal(false)}
                    className="flex-1 py-2 rounded-lg border border-outline-variant/40 text-on-surface-variant hover:text-on-surface transition-colors text-xs font-bold"
                  >
                    Cancel
                  </button>
                  <button
                    onClick={confirmDispatch}
                    className="flex-1 py-2 rounded-lg bg-primary text-black font-bold hover:bg-primary-light transition-all shadow-glow text-xs"
                  >
                    Confirm & Dispatch
                  </button>
                </div>
              </div>
            </div>
          )}
        </main>
      </div>
    </div>
  );
}
