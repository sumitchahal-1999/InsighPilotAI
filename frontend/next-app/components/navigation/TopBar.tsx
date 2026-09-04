"use client";

import React from "react";
import { useApp } from "@/context/AppContext";
import { PersonaType } from "@/lib/types";
import Link from "next/link";

interface TopBarProps {
  breadcrumb?: string;
  persona?: PersonaType;
  onPersonaChange?: (p: PersonaType) => void;
}

export function TopBar({ breadcrumb = "Command Center" }: TopBarProps) {
  const {
    persona,
    setPersona,
    region,
    setRegion,
    quarter,
    isInvestigationRunning,
    triggerLiveInvestigation,
  } = useApp();

  return (
    <header className="h-16 border-b border-outline-variant/30 bg-[#051424]/90 backdrop-blur-md px-4 sm:px-6 lg:px-8 flex items-center justify-between sticky top-0 z-30 shadow-sm gap-3 select-none">
      {/* Breadcrumb Context */}
      <div className="flex items-center gap-2 text-xs font-mono text-on-surface-variant min-w-0 shrink">
        <span className="text-on-surface-variant/70 hidden sm:inline">Enterprise</span>
        <span className="text-outline-variant hidden sm:inline">/</span>
        <span className="text-primary font-bold truncate">{breadcrumb}</span>

        {/* Live Pulse Chip (visible on larger screens) */}
        <span className="hidden xl:inline-flex items-center gap-1.5 bg-surface-container px-2 py-0.5 rounded text-[10px] text-primary border border-outline-variant/30 font-bold ml-1.5 shrink-0 whitespace-nowrap">
          <span className="w-1.5 h-1.5 rounded-full bg-primary animate-pulse"></span>
          <span>{quarter}</span>
        </span>
      </div>

      {/* Right Controls */}
      <div className="flex items-center gap-2 sm:gap-2.5 shrink-0">
        {/* Interactive Region Switcher */}
        <div className="flex items-center gap-1 bg-surface-container/70 border border-outline-variant/30 rounded-lg px-2 py-1 text-xs font-mono shrink-0">
          <span className="text-[10px] text-on-surface-variant uppercase font-bold hidden md:inline">
            Region:
          </span>
          <select
            value={region}
            onChange={(e) => setRegion(e.target.value as any)}
            className="bg-transparent text-xs font-mono font-bold text-on-surface focus:outline-none cursor-pointer pr-1"
          >
            <option value="NA-East" className="bg-[#0B0F19] text-on-surface">NA-East</option>
            <option value="Global" className="bg-[#0B0F19] text-on-surface">Global Org</option>
            <option value="EMEA" className="bg-[#0B0F19] text-on-surface">EMEA</option>
            <option value="APAC" className="bg-[#0B0F19] text-on-surface">APAC</option>
          </select>
        </div>

        {/* Persona Selector */}
        <div className="flex items-center gap-1 bg-surface-container border border-primary/40 px-2 sm:px-2.5 py-1 rounded-lg shadow-sm shrink-0">
          <span className="material-symbols-outlined text-primary text-[15px]">psychology</span>
          <select
            value={persona}
            onChange={(e) => setPersona(e.target.value as PersonaType)}
            className="bg-transparent text-xs font-mono font-bold text-primary focus:outline-none cursor-pointer pr-1"
          >
            <option value="CFO" className="bg-[#0B0F19] text-on-surface">
              CFO
            </option>
            <option value="REGIONAL_SALES_MANAGER" className="bg-[#0B0F19] text-on-surface">
              Sales Lead
            </option>
            <option value="COO" className="bg-[#0B0F19] text-on-surface">
              COO
            </option>
            <option value="SUPPLY_CHAIN_LEAD" className="bg-[#0B0F19] text-on-surface">
              Supply Chain
            </option>
          </select>
        </div>

        {/* Live Re-Run Pipeline CTA */}
        <button
          onClick={triggerLiveInvestigation}
          disabled={isInvestigationRunning}
          className={`px-2.5 sm:px-3 py-1 rounded-lg font-mono text-xs font-bold transition-all flex items-center gap-1.5 shrink-0 ${
            isInvestigationRunning
              ? "bg-primary/20 text-primary border border-primary/50 animate-pulse"
              : "bg-surface-container hover:bg-primary/10 text-primary border border-primary/30"
          }`}
          title="Trigger autonomous multi-agent LangGraph execution"
        >
          <span className="material-symbols-outlined text-[15px]">
            {isInvestigationRunning ? "sync" : "bolt"}
          </span>
          <span className="hidden md:inline">
            {isInvestigationRunning ? "Analyzing..." : "Re-run AI"}
          </span>
        </button>

        {/* Live Integrity Chip (visible on wide screens) */}
        <div className="hidden 2xl:flex items-center gap-1 text-[10px] font-mono text-success bg-success/10 border border-success/30 px-2 py-1 rounded-md shrink-0 whitespace-nowrap">
          <span className="material-symbols-outlined text-[13px]">verified</span>
          <span>100% HEALTHY</span>
        </div>

        {/* User Profile Avatar */}
        <div className="flex items-center gap-1.5 pl-1.5 sm:pl-2 border-l border-outline-variant/30 shrink-0">
          <div className="w-7 h-7 rounded-full bg-primary/20 border border-primary/40 flex items-center justify-center text-primary font-mono font-bold text-xs">
            JD
          </div>
        </div>
      </div>
    </header>
  );
}
