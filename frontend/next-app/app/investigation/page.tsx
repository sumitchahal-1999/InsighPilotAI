"use client";

import React, { useEffect, useState } from "react";
import { Sidebar } from "@/components/navigation/Sidebar";
import { TopBar } from "@/components/navigation/TopBar";
import { useApp } from "@/context/AppContext";
import { apiClient } from "@/lib/api";
import { AIExplanationResponse } from "@/lib/types";
import Link from "next/link";

interface AgentStep {
  id: string;
  stepNumber: string;
  name: string;
  role: string;
  stageNum: number;
  nodeType: "DETERMINISTIC" | "SAFETY_GUARD" | "AI_ORCHESTRATION" | string;
  status: "COMPLETED" | "RUNNING" | "PENDING" | "ABSTAINED" | string;
  timestamp: string;
  duration: string;
  summary: string;
  details: string[];
}

const DEFAULT_LANGGRAPH_STEPS: AgentStep[] = [
  {
    id: "load_kpi_node",
    stepNumber: "01",
    name: "Load KPI Time-Series Context",
    role: "Time-Series Ingestion & Baseline Loading",
    stageNum: 1,
    nodeType: "DETERMINISTIC",
    status: "COMPLETED",
    timestamp: "10:42:01 AM",
    duration: "12.4ms",
    summary: "Loaded baseline ($15.43M) and target period ($14.20M) revenue context for NA-East.",
    details: [
      "Ingested 18,400 daily transaction records across 4 operational tiers.",
      "Identified statistically significant anomaly trigger (z-score: -3.42, threshold: -2.0).",
    ],
  },
  {
    id: "calculate_movement_node",
    stepNumber: "02",
    name: "Calculate Variance Materiality",
    role: "Variance Computation & Severity Classification",
    stageNum: 1,
    nodeType: "DETERMINISTIC",
    status: "COMPLETED",
    timestamp: "10:42:02 AM",
    duration: "8.6ms",
    summary: "Computed exact -$1,230,000.01 (-7.97%) shortfall, triggering CRITICAL_NEGATIVE_VARIANCE.",
    details: [
      "Evaluated threshold condition: -7.97% exceeds materiality boundary of -3.0%.",
      "Classified status: CRITICAL_NEGATIVE_VARIANCE.",
    ],
  },
  {
    id: "identify_drivers_node",
    stepNumber: "03",
    name: "Decompose Causal Drivers",
    role: "Multi-Factor Waterfall Decomposition Engine",
    stageNum: 2,
    nodeType: "DETERMINISTIC",
    status: "COMPLETED",
    timestamp: "10:42:02 AM",
    duration: "18.2ms",
    summary: "Identified 4 mutually exclusive causal drivers accounting for 100.0% of variance.",
    details: [
      "Driver 1: Atlanta DC Stockout (43.2% / -$550K / 94% conf).",
      "Driver 2: SKU-8821 Sales Volume Contraction (26.7% / -$340K / 89% conf).",
      "Driver 3: Distributor PO Deferrals (18.8% / -$240K / 85% conf).",
      "Driver 4: Horizon Promotional Pricing (11.3% / -$144K / 78% conf).",
    ],
  },
  {
    id: "gather_evidence_node",
    stepNumber: "04",
    name: "Verify Cryptographic Evidence",
    role: "Cross-System Provenance & SHA-256 Checksum",
    stageNum: 3,
    nodeType: "DETERMINISTIC",
    status: "COMPLETED",
    timestamp: "10:42:03 AM",
    duration: "24.1ms",
    summary: "Collected 4 verified empirical evidence records with 100% SHA-256 data contracts.",
    details: [
      "EVID_ERP_ATL_STOCKOUT_001 (SAP S/4HANA Daily Inventory Snapshot).",
      "EVID_ZENDESK_ATL_DELAY_003 (Zendesk Support CRM +310% Out of Stock tickets).",
      "EVID_CRM_PO_DEF_006 (EDI Gateway 29 deferred distributor POs).",
    ],
  },
  {
    id: "generate_recommendations_node",
    stepNumber: "05",
    name: "Prescriptive Levers & Simulation",
    role: "Elasticity Modeling & Strategic Action Levers",
    stageNum: 4,
    nodeType: "DETERMINISTIC",
    status: "COMPLETED",
    timestamp: "10:42:04 AM",
    duration: "14.5ms",
    summary: "Formulated 2 deterministic action levers modeling +$757.6K addressable recovery.",
    details: [
      "Priority 1: Emergency Stock Transfer (+$484K recovery, 14d SLA, 91% conf).",
      "Priority 2: Distributor Recovery Outreach (+$180K recovery, 21d SLA, 85% conf).",
    ],
  },
];

const STAGES = [
  {
    stage: 1,
    label: "Detecting",
    title: "Anomaly Detection",
    icon: "troubleshoot",
    badge: "NA-East ↓7.97%",
    nodeId: "load_kpi_node",
    synthesis: "Ingested 18,400 daily ERP transaction records and flagged statistically significant -7.97% (-$1.23M) shortfall against baseline.",
    linkId: "KPI_REV_DEFICIT",
  },
  {
    stage: 2,
    label: "Investigating",
    title: "Root Cause",
    icon: "account_tree",
    badge: "4 Drivers (100%)",
    nodeId: "identify_drivers_node",
    synthesis: "Decomposed the $1.23M variance into 4 causal drivers. Primary driver is Atlanta DC Stockout (43.2% attribution share / -$550K).",
    linkId: "DRV_ATL_STOCKOUT",
  },
  {
    stage: 3,
    label: "Validating",
    title: "Evidence",
    icon: "folder_special",
    badge: "4 Verified Nodes",
    nodeId: "gather_evidence_node",
    synthesis: "Corroborated root cause across SAP S/4HANA (14 days zero stock) and Zendesk CRM (+310% out-of-stock tickets) with 100% SHA-256 provenance.",
    linkId: "EVID_ERP_ATL_STOCKOUT_001",
  },
  {
    stage: 4,
    label: "Simulating",
    title: "Recommendation",
    icon: "science",
    badge: "2 Action Levers",
    nodeId: "generate_recommendations_node",
    synthesis: "Formulated emergency stock transfer (Chicago → Atlanta / 3,200 units) modeling +$484K recovery at 91% confidence.",
    linkId: "ACT_EMERGENCY_TRANSFER",
  },
  {
    stage: 5,
    label: "Briefing Ready",
    title: "Briefing",
    icon: "description",
    badge: "Boardroom Ready",
    nodeId: "generate_recommendations_node",
    synthesis: "Generated executive intelligence briefing certified for CFO and Boardroom sign-off with $757.6K projected recovery pool.",
    linkId: "BRIEF_2026_Q3_CFO",
  },
];

export default function InvestigationActivityPage() {
  const {
    persona,
    region,
    isInvestigationRunning,
    activeInvestigationStep,
    triggerLiveInvestigation,
  } = useApp();

  const [selectedStageNum, setSelectedStageNum] = useState<number>(1);
  const [selectedStepId, setSelectedStepId] = useState<string>("load_kpi_node");
  const [aiExplanation, setAiExplanation] = useState<AIExplanationResponse | null>(null);
  const [showJsonRaw, setShowJsonRaw] = useState<boolean>(false);

  useEffect(() => {
    async function loadData() {
      try {
        const aiData = await apiClient.getAIExplanation("north_america_east_revenue", {
          persona,
          region,
          prevPeriod: "2026-Q2",
          currPeriod: "2026-Q3",
        });
        setAiExplanation(aiData);
      } catch (e) {
        console.warn("AI trace explanation fallback:", e);
      }
    }
    loadData();
  }, [persona, region]);

  // When stage is clicked, select that stage and jump to its LangGraph node
  const handleStageClick = (st: typeof STAGES[0]) => {
    setSelectedStageNum(st.stage);
    setSelectedStepId(st.nodeId);
  };

  const currentStage = STAGES.find((s) => s.stage === selectedStageNum) || STAGES[0];
  const selectedStep =
    DEFAULT_LANGGRAPH_STEPS.find((s) => s.id === selectedStepId) || DEFAULT_LANGGRAPH_STEPS[0];

  return (
    <div className="flex min-h-screen bg-[#051424] text-on-surface">
      <Sidebar />

      <div className="flex-1 flex flex-col min-w-0">
        <TopBar breadcrumb="AI Investigation Activity" />

        <main className="flex-1 p-6 md:p-8 space-y-6 max-w-[1600px] mx-auto w-full">
          {/* Header Bar */}
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-2">
            <div>
              <div className="flex items-center gap-2 mb-1.5">
                <span className="text-[10px] font-mono text-primary font-bold uppercase tracking-widest bg-primary/10 border border-primary/20 px-2 py-0.5 rounded flex items-center gap-1">
                  <span className="material-symbols-outlined text-[14px]">psychology</span>
                  Autonomous Multi-Agent Pipeline
                </span>
                <span className="text-xs font-mono text-on-surface-variant">
                  Deterministic LangGraph State Machine
                </span>
              </div>
              <h1 className="font-display font-extrabold text-2xl text-on-surface tracking-tight">
                Multi-Agent Investigation Timeline
              </h1>
            </div>

            <div className="flex items-center gap-4">
              <div className="text-right font-mono">
                <div className="text-[10px] text-on-surface-variant uppercase font-bold">Time Elapsed</div>
                <div className="font-display font-bold text-base text-primary">02:14 ms</div>
              </div>
              <div className="h-8 w-px bg-outline-variant/30 hidden sm:block"></div>
              <div className="text-right font-mono">
                <div className="text-[10px] text-on-surface-variant uppercase font-bold">Confidence</div>
                <div className="font-display font-bold text-base text-primary">89.0%</div>
              </div>

              {/* Re-run Pipeline Button */}
              <button
                onClick={triggerLiveInvestigation}
                disabled={isInvestigationRunning}
                className={`px-4 py-2 rounded-lg font-mono text-xs font-bold transition-all flex items-center gap-2 ${
                  isInvestigationRunning
                    ? "bg-primary text-black shadow-glow animate-pulse"
                    : "bg-primary/20 text-primary border border-primary/40 hover:bg-primary hover:text-black shadow-sm"
                }`}
              >
                <span className="material-symbols-outlined text-[16px]">
                  {isInvestigationRunning ? "sync" : "bolt"}
                </span>
                <span>{isInvestigationRunning ? "Pipeline Running..." : "Re-Execute Agents"}</span>
              </button>
            </div>
          </div>

          {/* 5-Stage Interactive Pipeline Stepper (Fully Clickable & Animated) */}
          <div className="glass-panel rounded-2xl p-6 border border-outline-variant/30 bg-surface-container/70 shadow-sm relative overflow-hidden">
            <div className="flex items-center justify-between mb-2">
              <span className="text-[10px] font-mono text-on-surface-variant uppercase tracking-wider font-bold">
                Pipeline Stages (Click any stage to inspect node)
              </span>
              <span className="text-xs font-mono text-primary font-bold">
                Stage {selectedStageNum} of 5 Active
              </span>
            </div>

            <div className="relative flex items-center justify-between min-w-[700px] px-6 py-4 overflow-x-auto">
              {/* Background Line */}
              <div className="absolute left-16 right-16 h-1 bg-outline-variant/30 top-1/2 -translate-y-1/2 z-0 rounded-full"></div>

              {/* Active Glowing Progress Track */}
              <div
                className="absolute left-16 h-1 bg-primary top-1/2 -translate-y-1/2 z-0 rounded-full shadow-glow transition-all duration-300"
                style={{ width: `${((selectedStageNum - 1) / 4) * 82}%` }}
              ></div>

              {STAGES.map((st) => {
                const isSelected = selectedStageNum === st.stage;
                const isStepActive = selectedStageNum >= st.stage;

                return (
                  <div
                    key={st.stage}
                    onClick={() => handleStageClick(st)}
                    className="relative z-10 flex flex-col items-center w-36 text-center cursor-pointer group"
                  >
                    <span
                      className={`font-mono text-[10px] mb-2 uppercase tracking-widest font-bold transition-colors ${
                        isSelected
                          ? "text-primary font-bold"
                          : "text-on-surface-variant group-hover:text-on-surface"
                      }`}
                    >
                      {st.label}
                    </span>
                    <div
                      className={`w-14 h-14 rounded-2xl border-2 flex items-center justify-center mb-3 transition-all group-hover:scale-110 ${
                        isSelected
                          ? "bg-primary text-black border-primary shadow-glow scale-110 ring-4 ring-primary/30"
                          : isStepActive
                          ? "bg-surface-container border-primary text-primary shadow-glow"
                          : "bg-surface-dim border-outline-variant text-on-surface-variant opacity-60"
                      }`}
                    >
                      <span className="material-symbols-outlined text-2xl">{st.icon}</span>
                    </div>
                    <h4 className="font-display font-bold text-xs text-on-surface mb-1 leading-tight">{st.title}</h4>
                    <span
                      className={`font-mono text-[10px] px-2 py-0.5 rounded-full border transition-colors ${
                        isSelected
                          ? "bg-primary text-black font-bold border-primary"
                          : "bg-primary/10 text-primary border-primary/20"
                      }`}
                    >
                      {st.badge}
                    </span>
                  </div>
                );
              })}
            </div>

            {/* Grounded AI Synthesis Banner for Selected Stage */}
            <div className="mt-5 pt-4 border-t border-outline-variant/30 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
              <div className="flex items-center gap-3">
                <div className="bg-primary/15 p-2 rounded-lg border border-primary/30 text-primary shrink-0">
                  <span className="material-symbols-outlined text-[20px]">auto_awesome</span>
                </div>
                <div>
                  <div className="flex items-center gap-2 mb-0.5">
                    <span className="font-mono text-[10px] text-primary font-bold tracking-wider">
                      GROUNDED AI SYNTHESIS • {currentStage.label.toUpperCase()}
                    </span>
                    <span className="font-mono text-[9px] text-on-surface-variant bg-surface-dim px-1.5 py-0.5 rounded border border-outline-variant/30">
                      {persona} VIEW
                    </span>
                  </div>
                  <p className="text-xs text-on-surface font-sans leading-snug">
                    {currentStage.synthesis}
                  </p>
                </div>
              </div>

              <div className="flex items-center gap-2 shrink-0 font-mono text-[10px]">
                <Link
                  href={`/evidence?q=${currentStage.linkId}`}
                  className="px-2.5 py-1.5 rounded bg-primary/10 text-primary border border-primary/20 hover:bg-primary hover:text-black transition-colors flex items-center gap-1 font-bold"
                >
                  <span className="material-symbols-outlined text-[12px]">link</span>
                  <span>{currentStage.linkId}</span>
                </Link>
              </div>
            </div>
          </div>

          {/* LangGraph 5-Step Deep Inspection Drawer */}
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
            {/* Step Selector List (5 cols) */}
            <div className="lg:col-span-5 space-y-2.5">
              <div className="flex items-center justify-between mb-1">
                <span className="font-mono text-xs text-on-surface-variant uppercase tracking-wider font-bold">
                  LangGraph Nodes ({DEFAULT_LANGGRAPH_STEPS.length})
                </span>
                <span className="font-mono text-[10px] text-primary">Click to inspect payload</span>
              </div>

              {DEFAULT_LANGGRAPH_STEPS.map((step) => {
                const isSelected = selectedStepId === step.id;

                return (
                  <div
                    key={step.id}
                    onClick={() => {
                      setSelectedStepId(step.id);
                      setSelectedStageNum(step.stageNum);
                    }}
                    className={`p-3.5 rounded-xl border transition-all duration-200 cursor-pointer flex items-center justify-between ${
                      isSelected
                        ? "border-primary bg-primary/15 ring-1 ring-primary shadow-glow"
                        : "border-outline-variant/30 bg-surface-container/60 hover:bg-surface-container hover:border-primary/40"
                    }`}
                  >
                    <div className="flex items-center gap-3">
                      <span className="font-mono text-xs font-bold text-primary">{step.stepNumber}</span>
                      <div>
                        <h4 className="font-display font-bold text-xs text-on-surface leading-tight">
                          {step.name}
                        </h4>
                        <span className="font-mono text-[10px] text-on-surface-variant">{step.role}</span>
                      </div>
                    </div>
                    <span className="font-mono text-[10px] text-primary font-bold bg-primary/10 px-2 py-0.5 rounded border border-primary/20">
                      {step.duration}
                    </span>
                  </div>
                );
              })}
            </div>

            {/* Deep Step Payload & Execution Trace (7 cols) */}
            <div className="lg:col-span-7 space-y-4">
              <div className="glass-panel rounded-2xl p-6 border border-outline-variant/30 bg-surface-container/70 shadow-sm space-y-4">
                <div className="flex items-center justify-between pb-3 border-b border-outline-variant/30">
                  <div>
                    <span className="text-[10px] font-mono text-primary font-bold uppercase tracking-wider block">
                      Node {selectedStep.stepNumber} Execution Trace
                    </span>
                    <h3 className="font-display font-bold text-base text-on-surface">{selectedStep.name}</h3>
                  </div>

                  <div className="flex items-center gap-2 font-mono text-xs">
                    <button
                      onClick={() => setShowJsonRaw(!showJsonRaw)}
                      className={`px-2.5 py-1 rounded text-[10px] font-bold border transition-colors ${
                        showJsonRaw
                          ? "bg-primary text-black border-primary"
                          : "bg-surface-dim text-on-surface-variant border-outline-variant/40 hover:text-on-surface"
                      }`}
                    >
                      Raw JSON
                    </button>
                    <span className="px-2 py-0.5 rounded bg-success/15 text-success border border-success/30 text-[10px] font-bold">
                      {selectedStep.status}
                    </span>
                  </div>
                </div>

                {showJsonRaw ? (
                  <pre className="bg-[#051424] p-4 rounded-xl border border-outline-variant/30 text-[11px] font-mono text-primary overflow-x-auto max-h-[340px]">
                    {JSON.stringify(selectedStep, null, 2)}
                  </pre>
                ) : (
                  <div className="space-y-4 font-mono text-xs">
                    <div className="bg-surface-dim p-4 rounded-xl border border-outline-variant/30">
                      <span className="text-[9px] text-on-surface-variant uppercase font-bold block mb-1">
                        Objective & Runtime Output
                      </span>
                      <p className="text-on-surface font-sans text-xs leading-relaxed">
                        {selectedStep.summary}
                      </p>
                    </div>

                    <div className="bg-surface-dim p-4 rounded-xl border border-outline-variant/30 space-y-2">
                      <span className="text-[9px] text-on-surface-variant uppercase font-bold block">
                        Deterministic Execution Log
                      </span>
                      <div className="space-y-1.5">
                        {selectedStep.details.map((line, idx) => (
                          <div key={idx} className="flex items-start gap-2 text-[11px] text-on-surface-variant">
                            <span className="text-primary font-bold">›</span>
                            <span>{line}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  </div>
                )}
              </div>
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}
