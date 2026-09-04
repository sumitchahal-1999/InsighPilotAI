"use client";

import React, { useState, useEffect, useRef, useLayoutEffect } from "react";
import { Sidebar } from "@/components/navigation/Sidebar";
import { TopBar } from "@/components/navigation/TopBar";
import { useApp } from "@/context/AppContext";
import Link from "next/link";

interface GraphNode {
  id: string;
  badge: string;
  badgeType: "primary" | "error" | "int" | "ext" | "action" | "outcome";
  title: string;
  metric: string;
  subMetric?: string;
  confidence?: number;
  icon: string;
  description: string;
  column: number;
  impactUsd?: number;
  hash?: string;
  evidenceId?: string;
  stream: "stockout" | "volume" | "distributor" | "competitor" | "core";
  linkedParents?: string[];
  linkedChildren?: string[];
}

interface GraphEdge {
  id: string;
  from: string;
  to: string;
  stream: "stockout" | "volume" | "distributor" | "competitor" | "core";
  label: string;
  weight?: string;
  type: "causal" | "evidence" | "action" | "outcome";
}

const GRAPH_EDGES: GraphEdge[] = [
  // Column 1 -> Column 2 (KPI to Drivers)
  { id: "e-kpi-d1", from: "kpi", to: "driver-1", stream: "stockout", label: "Primary Causal (43.2%)", weight: "43.2%", type: "causal" },
  { id: "e-kpi-d2", from: "kpi", to: "driver-2", stream: "volume", label: "Volume Contraction (26.7%)", weight: "26.7%", type: "causal" },
  { id: "e-kpi-d3", from: "kpi", to: "driver-3", stream: "distributor", label: "Distributor Holds (18.8%)", weight: "18.8%", type: "causal" },
  { id: "e-kpi-d4", from: "kpi", to: "driver-4", stream: "competitor", label: "Horizon Pricing (11.3%)", weight: "11.3%", type: "causal" },

  // Column 2/3 -> Column 4 (Drivers to Evidence)
  { id: "e-d1-ev1", from: "driver-1", to: "evidence-1", stream: "stockout", label: "SAP 0-Stock Snapshot", weight: "94% Conf", type: "evidence" },
  { id: "e-d1-ev2", from: "driver-1", to: "evidence-2", stream: "stockout", label: "Zendesk +310% Tickets", weight: "89% Conf", type: "evidence" },
  { id: "e-d2-ev1", from: "driver-2", to: "evidence-1", stream: "volume", label: "Sales Contraction Proof", weight: "89% Conf", type: "evidence" },
  { id: "e-d3-ev3", from: "driver-3", to: "evidence-3", stream: "distributor", label: "EDI 29 PO Holds", weight: "85% Conf", type: "evidence" },
  { id: "e-d4-ev4", from: "driver-4", to: "evidence-4", stream: "competitor", label: "Web Scrape -15% Promo", weight: "78% Conf", type: "evidence" },

  // Column 4 -> Column 5 (Evidence to Actions)
  { id: "e-ev1-act1", from: "evidence-1", to: "action-1", stream: "stockout", label: "Rebalance Surplus", weight: "+$484K Rec", type: "action" },
  { id: "e-ev2-act1", from: "evidence-2", to: "action-1", stream: "stockout", label: "Fulfillment Restoration", weight: "14d SLA", type: "action" },
  { id: "e-ev3-act2", from: "evidence-3", to: "action-2", stream: "distributor", label: "Commercial SLA Outreach", weight: "+$180K Rec", type: "action" },

  // Column 5 -> Column 6 (Actions to Outcome)
  { id: "e-act1-out", from: "action-1", to: "outcome", stream: "stockout", label: "+$484K Modeled Lift", weight: "+$484K", type: "outcome" },
  { id: "e-act2-out", from: "action-2", to: "outcome", stream: "distributor", label: "+$180K Modeled Lift", weight: "+$180K", type: "outcome" },
  { id: "e-ev4-out", from: "evidence-4", to: "outcome", stream: "competitor", label: "+$93.6K Pricing Defense", weight: "+$93.6K", type: "outcome" },
];

export default function DecisionGraphPage() {
  const { region, regionData } = useApp();
  const [selectedNodeId, setSelectedNodeId] = useState<string>("driver-1");
  const [hoveredNodeId, setHoveredNodeId] = useState<string | null>(null);
  const [hoveredEdgeId, setHoveredEdgeId] = useState<string | null>(null);
  const [activeStreamFilter, setActiveStreamFilter] = useState<string>("ALL");
  const [searchQuery, setSearchQuery] = useState<string>("");
  const [isDrawerOpen, setIsDrawerOpen] = useState<boolean>(true);

  const containerRef = useRef<HTMLDivElement>(null);
  const [edgePaths, setEdgePaths] = useState<Array<{ id: string; d: string; edge: GraphEdge }>>([]);

  const scrollToColumn = (index: number) => {
    if (!containerRef.current) return;
    const positions = [0, 260, 520, 800, 1100, 1400];
    containerRef.current.scrollTo({
      left: positions[index] || 0,
      behavior: "smooth",
    });
  };

  const handleSelectNode = (id: string) => {
    setSelectedNodeId(id);
    setIsDrawerOpen(true);
  };

  const nodes: Record<string, GraphNode> = {
    kpi: {
      id: "kpi",
      column: 1,
      badge: "Critical Anomaly",
      badgeType: "error",
      title: `${region} Revenue Deficit`,
      metric: regionData.variance,
      subMetric: `${regionData.variancePct} vs Baseline`,
      confidence: 100,
      icon: "warning",
      stream: "core",
      description: `Q3 actual revenue fell to ${regionData.revenue} against baseline, triggering a critical enterprise anomaly investigation.`,
      linkedParents: [],
      linkedChildren: ["driver-1", "driver-2", "driver-3", "driver-4"],
    },
    "driver-1": {
      id: "driver-1",
      column: 2,
      badge: "Primary Driver",
      badgeType: "primary",
      title: "Atlanta DC Stockout",
      metric: "43.2% Share",
      subMetric: "-$550K Financial Impact",
      confidence: 94.0,
      icon: "warehouse",
      stream: "stockout",
      description: "Depleted inventory for SKU-8821 across 14 consecutive days created acute regional order fulfillment delays.",
      evidenceId: "EVID_ERP_ATL_STOCKOUT_001",
      hash: "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      linkedParents: ["kpi"],
      linkedChildren: ["evidence-1", "evidence-2", "action-1"],
    },
    "driver-2": {
      id: "driver-2",
      column: 2,
      badge: "Internal Factor",
      badgeType: "int",
      title: "SKU-8821 Sales Volume",
      metric: "-$340K",
      subMetric: "26.7% Share • 8.5% Contraction",
      confidence: 89.0,
      icon: "trending_down",
      stream: "volume",
      description: "High-margin flagship product volume dropped across Tier-1 East territory retail accounts.",
      evidenceId: "EVID_CRM_SKU8821_SALES_004",
      hash: "7c33b41298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b111",
      linkedParents: ["kpi"],
      linkedChildren: ["evidence-1"],
    },
    "driver-3": {
      id: "driver-3",
      column: 2,
      badge: "Internal Factor",
      badgeType: "int",
      title: "Distributor PO Deferrals",
      metric: "-$240K",
      subMetric: "18.8% Share • 29 Delayed POs",
      confidence: 85.0,
      icon: "assignment_return",
      stream: "distributor",
      description: "29 purchase orders deferred by Tier-1 distributors due to warehouse fulfillment uncertainty.",
      evidenceId: "EVID_CRM_PO_DEF_006",
      hash: "ca978112ca1bbdcafac231b39a23dc4da786eff8147c4e72b9807785afee48bb",
      linkedParents: ["kpi"],
      linkedChildren: ["evidence-3", "action-2"],
    },
    "driver-4": {
      id: "driver-4",
      column: 3,
      badge: "External Factor",
      badgeType: "ext",
      title: "Horizon Foods Pricing",
      metric: "-15% Promo",
      subMetric: "-$144K Elasticity Impact",
      confidence: 78.0,
      icon: "storefront",
      stream: "competitor",
      description: "Competitor launched 15% promotional discount in East territory, exerting price elasticity pressure.",
      evidenceId: "EVID_MKT_HORIZON_PROMO_008",
      hash: "4b227777d4dd1fc61c6f884f48641d02b4d121d3fd328cb08b5531fcacdabf8a",
      linkedParents: ["kpi"],
      linkedChildren: ["evidence-4"],
    },
    "evidence-1": {
      id: "evidence-1",
      column: 4,
      badge: "ERP Telemetry",
      badgeType: "int",
      title: "SAP Inventory Snapshot",
      metric: "14 Days 0 Stock",
      subMetric: "Aug 10 - Aug 24 Duration",
      confidence: 94.0,
      icon: "inventory_2",
      stream: "stockout",
      description: "Cryptographic ERP extract confirming zero inventory at Atlanta DC between Aug 10 and Aug 24.",
      evidenceId: "EVID_ERP_ATL_STOCKOUT_001",
      hash: "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      linkedParents: ["driver-1", "driver-2"],
      linkedChildren: ["action-1"],
    },
    "evidence-2": {
      id: "evidence-2",
      column: 4,
      badge: "CRM Telemetry",
      badgeType: "int",
      title: "Zendesk Support Tickets",
      metric: "+310% Tickets",
      subMetric: "142 Backlog Reports",
      confidence: 89.0,
      icon: "confirmation_number",
      stream: "stockout",
      description: "Customer service CRM telemetry logging unfulfilled order complaints from key regional accounts.",
      evidenceId: "EVID_ZENDESK_ATL_DELAY_003",
      hash: "8f434346648f6b96df89dda901c5176b10a6d83961dd3c1ac88b59b2dc327aa4",
      linkedParents: ["driver-1"],
      linkedChildren: ["action-1"],
    },
    "evidence-3": {
      id: "evidence-3",
      column: 4,
      badge: "EDI Telemetry",
      badgeType: "int",
      title: "Distributor PO Holds",
      metric: "29 Held Orders",
      subMetric: "$240K Held Value",
      confidence: 85.0,
      icon: "mail",
      stream: "distributor",
      description: "EDI gateway logs confirming distributor PO holds due to unconfirmed fulfillment dispatch dates.",
      evidenceId: "EVID_CRM_PO_DEF_006",
      hash: "ca978112ca1bbdcafac231b39a23dc4da786eff8147c4e72b9807785afee48bb",
      linkedParents: ["driver-3"],
      linkedChildren: ["action-2"],
    },
    "evidence-4": {
      id: "evidence-4",
      column: 4,
      badge: "Web Scrape",
      badgeType: "ext",
      title: "Competitor Web Scrape",
      metric: "-15.0% Discount",
      subMetric: "East Retail Channel",
      confidence: 78.0,
      icon: "insights",
      stream: "competitor",
      description: "Automated web scrape detected promotional discounts by Horizon Foods.",
      evidenceId: "EVID_MKT_HORIZON_PROMO_008",
      hash: "4b227777d4dd1fc61c6f884f48641d02b4d121d3fd328cb08b5531fcacdabf8a",
      linkedParents: ["driver-4"],
      linkedChildren: ["outcome"],
    },
    "action-1": {
      id: "action-1",
      column: 5,
      badge: "Operations Priority 1",
      badgeType: "action",
      title: "Emergency Stock Transfer",
      metric: "+$484K",
      subMetric: "3,200 units • 14 Days SLA",
      confidence: 91.0,
      icon: "local_shipping",
      stream: "stockout",
      description: "Reallocate 3,200 units of SKU-8821 from Chicago Central DC to Atlanta DC via expedited freight.",
      linkedParents: ["driver-1", "evidence-1", "evidence-2"],
      linkedChildren: ["outcome"],
    },
    "action-2": {
      id: "action-2",
      column: 5,
      badge: "Commercial Priority 2",
      badgeType: "action",
      title: "Targeted Distributor Outreach",
      metric: "+$180K",
      subMetric: "29 POs • 21 Days SLA",
      confidence: 85.0,
      icon: "payments",
      stream: "distributor",
      description: "Deploy commercial account managers with priority delivery guarantees to capture 29 deferred purchase orders.",
      linkedParents: ["driver-3", "evidence-3"],
      linkedChildren: ["outcome"],
    },
    outcome: {
      id: "outcome",
      column: 6,
      badge: "Projected Outcome",
      badgeType: "outcome",
      title: "Projected Fiscal Recovery",
      metric: regionData.recoveryPool,
      subMetric: "Recovers 61.6% of addressable deficit",
      confidence: 91.0,
      icon: "monitoring",
      stream: "core",
      description: "Deterministic elasticity model projects recovery and gross margin improvement.",
      linkedParents: ["action-1", "action-2"],
      linkedChildren: [],
    },
  };

  const selectedNode = nodes[selectedNodeId] || nodes["driver-1"];

  const isNodeVisible = (node: GraphNode) => {
    if (searchQuery.trim()) {
      const q = searchQuery.toLowerCase();
      const matchText =
        node.title.toLowerCase().includes(q) ||
        node.metric.toLowerCase().includes(q) ||
        node.badge.toLowerCase().includes(q);
      if (!matchText) return false;
    }
    if (activeStreamFilter === "ALL") return true;
    if (node.stream === "core") return true;
    return node.stream === activeStreamFilter;
  };

  // Re-calculate dynamic connector paths based on exact DOM port coordinates
  const updateConnectorPositions = () => {
    if (!containerRef.current) return;
    const containerRect = containerRef.current.getBoundingClientRect();
    const scrollLeft = containerRef.current.scrollLeft || 0;
    const scrollTop = containerRef.current.scrollTop || 0;

    const newPaths: Array<{ id: string; d: string; edge: GraphEdge }> = [];

    GRAPH_EDGES.forEach((edge) => {
      const fromNode = nodes[edge.from];
      const toNode = nodes[edge.to];
      if (!fromNode || !toNode) return;
      if (!isNodeVisible(fromNode) || !isNodeVisible(toNode)) return;

      const outPortEl = document.getElementById(`port-out-${edge.from}`);
      const inPortEl = document.getElementById(`port-in-${edge.to}`);

      if (outPortEl && inPortEl) {
        const r1 = outPortEl.getBoundingClientRect();
        const r2 = inPortEl.getBoundingClientRect();

        const x1 = r1.left - containerRect.left + scrollLeft + r1.width / 2;
        const y1 = r1.top - containerRect.top + scrollTop + r1.height / 2;
        const x2 = r2.left - containerRect.left + scrollLeft + r2.width / 2;
        const y2 = r2.top - containerRect.top + scrollTop + r2.height / 2;

        const dx = Math.max(30, (x2 - x1) * 0.45);
        const d = `M ${x1} ${y1} C ${x1 + dx} ${y1}, ${x2 - dx} ${y2}, ${x2} ${y2}`;
        newPaths.push({ id: edge.id, d, edge });
      }
    });

    setEdgePaths(newPaths);
  };

  useLayoutEffect(() => {
    updateConnectorPositions();
    const timer = setTimeout(updateConnectorPositions, 150);
    return () => clearTimeout(timer);
  }, [selectedNodeId, activeStreamFilter, searchQuery, region]);

  useEffect(() => {
    const handleResize = () => updateConnectorPositions();
    window.addEventListener("resize", handleResize);
    return () => window.removeEventListener("resize", handleResize);
  }, []);

  // Compute active highway lineage for highlighting
  const activeFocusNodeId = hoveredNodeId || selectedNodeId;
  const isEdgeActive = (edge: GraphEdge) => {
    if (hoveredEdgeId === edge.id) return true;
    if (activeStreamFilter !== "ALL" && edge.stream === activeStreamFilter) return true;
    if (edge.from === activeFocusNodeId || edge.to === activeFocusNodeId) return true;

    // Check upstream & downstream connections of focus node
    const focusNode = nodes[activeFocusNodeId];
    if (focusNode) {
      if (focusNode.linkedParents?.includes(edge.from) && edge.to === activeFocusNodeId) return true;
      if (focusNode.linkedChildren?.includes(edge.to) && edge.from === activeFocusNodeId) return true;
    }
    return false;
  };

  return (
    <div className="flex min-h-screen bg-[#0B0F19] text-on-surface">
      <Sidebar />

      <div className="flex-1 flex flex-col min-w-0">
        <TopBar breadcrumb="Decision Graph" />

        <main className="flex-1 flex flex-col relative overflow-hidden">
          {/* Top Interactive Toolbar (Evenly Distributed Left, Center, and Right Layout) */}
          <div className="px-4 sm:px-6 md:px-8 py-3.5 border-b border-outline-variant/20 flex items-center justify-between z-20 relative bg-[#051424]/90 backdrop-blur-md gap-4 select-none w-full min-w-0">
            {/* Left Section: Title & Live Telemetry */}
            <div className="flex items-center gap-3 shrink-0 min-w-0">
              <div className="w-10 h-10 rounded-xl bg-primary/10 border border-primary/30 flex items-center justify-center text-primary shrink-0 shadow-sm">
                <span className="material-symbols-outlined text-[22px]">account_tree</span>
              </div>
              <div className="min-w-0">
                <h2 className="font-display font-extrabold text-base text-on-surface whitespace-nowrap tracking-tight">
                  Decision Graph Canvas
                </h2>
                <div className="flex items-center gap-1.5 mt-0.5 font-mono text-[10px] sm:text-[11px] text-on-surface-variant whitespace-nowrap">
                  <span className="inline-block w-1.5 h-1.5 rounded-full bg-primary animate-pulse"></span>
                  <span>11 Nodes</span>
                  <span className="text-outline-variant">•</span>
                  <span>14 Edges</span>
                  <span className="text-outline-variant hidden md:inline">•</span>
                  <span className="text-primary font-semibold hidden md:inline">Active Focus</span>
                </div>
              </div>
            </div>

            {/* Center Section: Centered Flow Pathway Selector (Utilizes Middle Space Evenly) */}
            <div className="flex items-center justify-center shrink-0">
              <div className="flex items-center gap-2 bg-surface-container px-3.5 py-2 rounded-xl border border-outline-variant/30 font-mono text-xs shadow-sm">
                <span className="material-symbols-outlined text-primary text-[17px]">filter_alt</span>
                <span className="text-[10px] text-on-surface-variant uppercase font-bold hidden sm:inline">
                  Flow:
                </span>
                <select
                  value={activeStreamFilter}
                  onChange={(e) => setActiveStreamFilter(e.target.value)}
                  className="bg-transparent text-xs font-mono font-bold text-primary focus:outline-none cursor-pointer pr-1"
                >
                  <option value="ALL" className="bg-[#0B0F19] text-on-surface">All Flows (100% Causal)</option>
                  <option value="stockout" className="bg-[#0B0F19] text-primary font-bold">Atlanta Stockout (43.2%)</option>
                  <option value="volume" className="bg-[#0B0F19] text-on-surface">Volume Contraction (26.7%)</option>
                  <option value="distributor" className="bg-[#0B0F19] text-on-surface">Distributor Holds (18.8%)</option>
                  <option value="competitor" className="bg-[#0B0F19] text-on-surface">Competitor Promo (11.3%)</option>
                </select>
              </div>
            </div>

            {/* Right Section: Expanded Search, Diagnosis Link & Inspector Toggle */}
            <div className="flex items-center gap-2.5 sm:gap-3 shrink-0 justify-end">
              <div className="relative">
                <input
                  type="text"
                  placeholder="Search & filter nodes..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="bg-surface-dim border border-outline-variant/30 rounded-xl pl-8 pr-3 py-2 text-xs text-on-surface placeholder:text-on-surface-variant/50 focus:border-primary focus:outline-none w-40 sm:w-52 lg:w-60 font-mono transition-all"
                />
                <span className="material-symbols-outlined text-on-surface-variant text-[15px] absolute left-2.5 top-1/2 -translate-y-1/2">
                  search
                </span>
              </div>

              <Link
                href="/root-cause"
                className="px-3.5 py-2 rounded-xl border border-outline-variant/30 text-on-surface-variant font-mono text-xs hover:bg-surface-container hover:text-primary transition-colors flex items-center gap-1.5 whitespace-nowrap shrink-0"
              >
                <span className="material-symbols-outlined text-[15px]">analytics</span>
                <span>Diagnosis</span>
              </Link>

              {/* Toggle Drawer Button */}
              <button
                onClick={() => setIsDrawerOpen(!isDrawerOpen)}
                className={`px-3 py-2 rounded-xl border text-xs font-mono font-bold transition-all flex items-center gap-1.5 shrink-0 ${
                  isDrawerOpen
                    ? "bg-primary/20 text-primary border-primary/40 shadow-glow"
                    : "bg-surface-dim hover:bg-surface-container border-outline-variant/30 text-on-surface-variant hover:text-on-surface"
                }`}
                title={isDrawerOpen ? "Collapse Node Details Panel" : "Open Node Details Panel"}
              >
                <span className="material-symbols-outlined text-[16px]">
                  {isDrawerOpen ? "side_navigation" : "dock_to_left"}
                </span>
                <span className="hidden xl:inline">{isDrawerOpen ? "Hide Panel" : "Node Details"}</span>
              </button>
            </div>
          </div>

          {/* Graph Canvas & Right Side Panel */}
          <div className="flex-1 flex relative overflow-hidden">
            {/* Scrollable Graph Layout Area */}
            <div
              ref={containerRef}
              onScroll={updateConnectorPositions}
              className="flex-1 overflow-x-auto overflow-y-auto p-8 pr-32 relative flex items-center justify-start gap-8 z-10 w-full min-h-[660px]"
            >
              {/* Dynamic SVG Connection Paths (Calculated from Port Centers) */}
              <svg className="absolute inset-0 w-full h-full pointer-events-none z-0 min-w-[1440px]">
                <defs>
                  <linearGradient id="activeGradient" x1="0%" y1="0%" x2="100%" y2="0%">
                    <stop offset="0%" stopColor="#4FDEC8" stopOpacity="1" />
                    <stop offset="100%" stopColor="#6FF2DC" stopOpacity="1" />
                  </linearGradient>
                  <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
                    <feGaussianBlur stdDeviation="3" result="blur" />
                    <feComposite in="SourceGraphic" in2="blur" operator="over" />
                  </filter>
                </defs>

                {edgePaths.map(({ id, d, edge }) => {
                  const active = isEdgeActive(edge);
                  return (
                    <g key={id} className="cursor-pointer pointer-events-auto">
                      {/* Wider invisible hit-area for hover */}
                      <path
                        d={d}
                        fill="none"
                        stroke="transparent"
                        strokeWidth="18"
                        onMouseEnter={() => setHoveredEdgeId(edge.id)}
                        onMouseLeave={() => setHoveredEdgeId(null)}
                      />

                      {/* Visible Edge Path */}
                      <path
                        d={d}
                        fill="none"
                        stroke={active ? "url(#activeGradient)" : "rgba(255, 255, 255, 0.12)"}
                        strokeWidth={active ? "3.5" : "1.5"}
                        strokeDasharray={active ? "6 4" : undefined}
                        filter={active ? "url(#glow)" : undefined}
                        className={active ? "transition-all duration-300 animate-pulse" : "transition-all duration-300"}
                      />
                    </g>
                  );
                })}
              </svg>

              {/* Column 1: KPI Anchor */}
              <div className="flex flex-col gap-4 w-52 shrink-0 justify-center z-10">
                {isNodeVisible(nodes.kpi) && (
                  <div
                    onClick={() => handleSelectNode("kpi")}
                    onMouseEnter={() => setHoveredNodeId("kpi")}
                    onMouseLeave={() => setHoveredNodeId(null)}
                    className={`rounded-2xl p-4 cursor-pointer relative transition-all duration-200 border ${
                      selectedNodeId === "kpi"
                        ? "border-error bg-error/15 ring-2 ring-error/60 shadow-[0_0_20px_rgba(255,180,171,0.2)]"
                        : "border-error/40 bg-error/10 hover:border-error"
                    }`}
                  >
                    {/* Dynamic Output Port */}
                    <div
                      id="port-out-kpi"
                      className="absolute -right-2 top-1/2 -translate-y-1/2 w-4 h-4 bg-error rounded-full border-2 border-[#0B0F19] shadow-sm z-20"
                    />

                    <div className="flex items-center gap-1.5 mb-2.5">
                      <span className="material-symbols-outlined text-error text-[18px]">warning</span>
                      <span className="text-[9px] bg-error text-black px-1.5 py-0.5 rounded font-mono uppercase font-bold">
                        {nodes.kpi.badge}
                      </span>
                    </div>
                    <h3 className="font-display font-bold text-xs leading-tight text-on-surface mb-2">
                      {nodes.kpi.title}
                    </h3>
                    <div className="font-display font-extrabold text-2xl text-error leading-none mb-1">
                      {nodes.kpi.metric}
                    </div>
                    <span className="text-[10px] font-mono text-error font-bold">
                      {nodes.kpi.subMetric}
                    </span>
                  </div>
                )}
              </div>

              {/* Column 2: Operational Drivers */}
              <div className="flex flex-col gap-3.5 w-52 shrink-0 justify-center z-10">
                <div className="font-mono text-[9px] text-on-surface-variant/70 uppercase tracking-widest px-1">
                  Operational Drivers
                </div>

                {["driver-1", "driver-2", "driver-3"].map((dId) => {
                  const node = nodes[dId];
                  if (!isNodeVisible(node)) return null;
                  const isSelected = selectedNodeId === dId;
                  return (
                    <div
                      key={dId}
                      onClick={() => handleSelectNode(dId)}
                      onMouseEnter={() => setHoveredNodeId(dId)}
                      onMouseLeave={() => setHoveredNodeId(null)}
                      className={`rounded-xl p-3.5 cursor-pointer relative transition-all duration-200 border ${
                        isSelected
                          ? "border-primary bg-primary/15 ring-2 ring-primary shadow-glow z-20"
                          : "border-outline-variant/60 bg-surface-container/80 hover:border-primary/40"
                      }`}
                    >
                      {/* Dynamic Input Port */}
                      <div
                        id={`port-in-${dId}`}
                        className="absolute -left-2 top-1/2 -translate-y-1/2 w-3.5 h-3.5 bg-surface-container rounded-full border-2 border-[#0B0F19] z-20"
                      />
                      {/* Dynamic Output Port */}
                      <div
                        id={`port-out-${dId}`}
                        className={`absolute -right-2 top-1/2 -translate-y-1/2 w-3.5 h-3.5 rounded-full border-2 border-[#0B0F19] z-20 ${
                          isSelected ? "bg-primary shadow-glow" : "bg-surface-container"
                        }`}
                      />

                      <div className="flex items-center justify-between mb-1.5">
                        <span className="material-symbols-outlined text-primary text-[16px]">{node.icon}</span>
                        <span className="text-[9px] bg-primary/20 text-primary px-1.5 py-0.5 rounded font-mono font-bold">
                          {node.badge}
                        </span>
                      </div>
                      <h4 className="font-display font-bold text-xs text-on-surface leading-tight mb-1">
                        {node.title}
                      </h4>
                      <div className="text-primary font-mono text-xs font-bold">{node.metric}</div>
                    </div>
                  );
                })}
              </div>

              {/* Column 3: External Factors */}
              <div className="flex flex-col gap-3.5 w-48 shrink-0 justify-center z-10">
                <div className="font-mono text-[9px] text-on-surface-variant/70 uppercase tracking-widest px-1">
                  External Factor
                </div>
                {isNodeVisible(nodes["driver-4"]) && (
                  <div
                    onClick={() => handleSelectNode("driver-4")}
                    onMouseEnter={() => setHoveredNodeId("driver-4")}
                    onMouseLeave={() => setHoveredNodeId(null)}
                    className={`rounded-xl p-3.5 cursor-pointer relative transition-all duration-200 border ${
                      selectedNodeId === "driver-4"
                        ? "border-primary bg-primary/15 ring-2 ring-primary z-20"
                        : "border-outline-variant/60 bg-surface-container/80 hover:border-primary/40"
                    }`}
                  >
                    <div
                      id="port-in-driver-4"
                      className="absolute -left-2 top-1/2 -translate-y-1/2 w-3.5 h-3.5 bg-surface-container rounded-full border-2 border-[#0B0F19] z-20"
                    />
                    <div
                      id="port-out-driver-4"
                      className="absolute -right-2 top-1/2 -translate-y-1/2 w-3.5 h-3.5 bg-surface-container rounded-full border-2 border-[#0B0F19] z-20"
                    />

                    <div className="flex items-center justify-between mb-1.5">
                      <span className="material-symbols-outlined text-on-surface-variant text-[16px]">storefront</span>
                      <span className="text-[9px] bg-surface-container px-1.5 py-0.5 rounded text-on-surface-variant font-mono">
                        Market
                      </span>
                    </div>
                    <h4 className="font-display font-bold text-xs text-on-surface leading-tight mb-1">
                      {nodes["driver-4"].title}
                    </h4>
                    <div className="text-on-surface-variant text-[11px] font-mono">
                      Price <span className="text-error font-bold">-15%</span>
                    </div>
                  </div>
                )}
              </div>

              {/* Column 4: Evidence Layer */}
              <div className="flex flex-col gap-3.5 w-52 shrink-0 justify-center z-10">
                <div className="font-mono text-[9px] text-on-surface-variant/70 uppercase tracking-widest px-1">
                  Evidence Layer
                </div>
                {["evidence-1", "evidence-2", "evidence-3", "evidence-4"].map((eId) => {
                  const node = nodes[eId];
                  if (!isNodeVisible(node)) return null;
                  const isSelected = selectedNodeId === eId;
                  return (
                    <div
                      key={eId}
                      onClick={() => handleSelectNode(eId)}
                      onMouseEnter={() => setHoveredNodeId(eId)}
                      onMouseLeave={() => setHoveredNodeId(null)}
                      className={`rounded-xl p-3.5 cursor-pointer relative transition-all duration-200 border ${
                        isSelected
                          ? "border-primary bg-primary/15 ring-2 ring-primary z-20"
                          : "border-outline-variant/60 bg-surface-container/80 hover:border-primary/40"
                      }`}
                    >
                      <div
                        id={`port-in-${eId}`}
                        className="absolute -left-2 top-1/2 -translate-y-1/2 w-3.5 h-3.5 bg-surface-container rounded-full border-2 border-[#0B0F19] z-20"
                      />
                      <div
                        id={`port-out-${eId}`}
                        className="absolute -right-2 top-1/2 -translate-y-1/2 w-3.5 h-3.5 bg-surface-container rounded-full border-2 border-[#0B0F19] z-20"
                      />

                      <div className="flex items-center justify-between mb-1.5">
                        <span className="material-symbols-outlined text-primary text-[16px]">{node.icon}</span>
                        <span className="text-[9px] bg-primary/10 text-primary px-1.5 py-0.5 rounded font-mono font-bold">
                          {node.badge}
                        </span>
                      </div>
                      <h4 className="font-display font-bold text-xs text-on-surface leading-tight mb-1">
                        {node.title}
                      </h4>
                      <div className="text-primary font-mono text-xs font-extrabold">{node.metric}</div>
                    </div>
                  );
                })}
              </div>

              {/* Column 5: Proposed Actions */}
              <div className="flex flex-col gap-3.5 w-52 shrink-0 justify-center z-10">
                <div className="font-mono text-[9px] text-on-surface-variant/70 uppercase tracking-widest px-1">
                  Proposed Actions
                </div>
                {["action-1", "action-2"].map((aId) => {
                  const node = nodes[aId];
                  if (!isNodeVisible(node)) return null;
                  const isSelected = selectedNodeId === aId;
                  return (
                    <div
                      key={aId}
                      onClick={() => handleSelectNode(aId)}
                      onMouseEnter={() => setHoveredNodeId(aId)}
                      onMouseLeave={() => setHoveredNodeId(null)}
                      className={`rounded-xl p-3.5 cursor-pointer relative transition-all duration-200 border ${
                        isSelected
                          ? "border-primary bg-primary/15 ring-2 ring-primary shadow-glow z-20"
                          : "border-primary/30 bg-primary/10 hover:border-primary"
                      }`}
                    >
                      <div
                        id={`port-in-${aId}`}
                        className="absolute -left-2 top-1/2 -translate-y-1/2 w-3.5 h-3.5 bg-surface-container rounded-full border-2 border-[#0B0F19] z-20"
                      />
                      <div
                        id={`port-out-${aId}`}
                        className="absolute -right-2 top-1/2 -translate-y-1/2 w-3.5 h-3.5 bg-primary rounded-full border-2 border-[#0B0F19] shadow-glow z-20"
                      />

                      <div className="flex items-center gap-2 mb-1.5">
                        <span className="material-symbols-outlined text-primary text-[16px]">{node.icon}</span>
                        <span className="text-[9px] font-mono text-primary font-bold uppercase">{node.badge}</span>
                      </div>
                      <h4 className="font-display font-bold text-xs text-on-surface leading-tight mb-1">
                        {node.title}
                      </h4>
                      <div className="text-primary font-mono text-xs font-extrabold">{node.metric} Recovery</div>
                    </div>
                  );
                })}
              </div>

              {/* Column 6: Predicted Outcome */}
              <div className="flex flex-col w-56 shrink-0 justify-center z-10">
                <div className="font-mono text-[9px] text-on-surface-variant/70 uppercase tracking-widest px-1 mb-1">
                  Predicted Outcome
                </div>
                {isNodeVisible(nodes.outcome) && (
                  <div
                    onClick={() => handleSelectNode("outcome")}
                    onMouseEnter={() => setHoveredNodeId("outcome")}
                    onMouseLeave={() => setHoveredNodeId(null)}
                    className={`rounded-2xl p-4 border-l-4 border-l-primary bg-gradient-to-r from-primary/15 to-surface-container/80 relative transition-all duration-200 border ${
                      selectedNodeId === "outcome"
                        ? "border-primary ring-2 ring-primary shadow-glow z-20"
                        : "border-outline-variant/60 hover:border-primary/40"
                    }`}
                  >
                    <div
                      id="port-in-outcome"
                      className="absolute -left-2.5 top-1/2 -translate-y-1/2 w-4 h-4 bg-primary rounded-full border-2 border-[#0B0F19] shadow-glow z-20"
                    />

                    <div className="flex items-center gap-1.5 mb-2">
                      <span className="material-symbols-outlined text-primary text-[18px]">monitoring</span>
                      <span className="font-mono text-[9px] text-on-surface-variant uppercase font-bold">
                        Projected Recovery
                      </span>
                    </div>
                    <div className="font-display font-extrabold text-2xl text-primary mb-2">
                      {nodes.outcome.metric}
                    </div>
                    <div className="text-[10px] font-mono text-on-surface-variant mb-3 bg-surface-container/60 p-2 rounded border border-outline-variant/30 leading-snug">
                      Recovers <span className="text-primary font-bold">61.6%</span> of addressable deficit.
                    </div>
                    <Link
                      href="/recommendations"
                      className="w-full py-1.5 bg-primary text-black rounded-lg text-xs font-mono font-bold hover:bg-primary-light transition-colors shadow-glow flex items-center justify-center gap-1 text-center"
                    >
                      <span>Execute Strategy</span>
                    </Link>
                  </div>
                )}
              </div>
            </div>

            {/* Floating Canvas Stage Navigator (Scaled for Optimal Readability & Text-Only) */}
            <div className="absolute bottom-4 left-6 z-20 hidden md:flex items-center gap-2.5 bg-[#051424]/95 backdrop-blur-xl px-4 py-2 rounded-xl border border-outline-variant/40 font-mono text-xs shadow-2xl select-none">
              <span className="text-xs text-on-surface-variant uppercase font-extrabold pr-2.5 border-r border-outline-variant/30 tracking-wider">
                Jump To:
              </span>

              <div className="flex items-center gap-1.5">
                {[
                  { name: "1. Anomaly", idx: 0 },
                  { name: "2. Drivers", idx: 1 },
                  { name: "3. Market", idx: 2 },
                  { name: "4. Evidence", idx: 3 },
                  { name: "5. Actions", idx: 4 },
                  { name: "6. Outcome", idx: 5 },
                ].map((col, i) => (
                  <React.Fragment key={col.idx}>
                    {i > 0 && <span className="text-outline-variant/50 text-xs font-bold">›</span>}
                    <button
                      onClick={() => scrollToColumn(col.idx)}
                      className="px-3 py-1.5 rounded-lg border border-outline-variant/30 bg-surface-container/80 hover:bg-primary/15 hover:border-primary/50 text-on-surface-variant hover:text-primary transition-all font-bold text-xs shadow-sm"
                    >
                      {col.name}
                    </button>
                  </React.Fragment>
                ))}
              </div>
            </div>

            {/* Right Side Drawer (Selected Node Details) */}
            {isDrawerOpen && (
              <aside className="w-72 sm:w-80 shrink-0 h-full border-l border-outline-variant/30 flex flex-col z-20 bg-[#051424]/95 backdrop-blur-xl animate-in slide-in-from-right duration-200">
                <div className="p-4 border-b border-outline-variant/30 flex items-center justify-between">
                  <h3 className="font-display font-bold text-sm text-on-surface flex items-center gap-2">
                    <span className="material-symbols-outlined text-primary text-[18px]">hub</span>
                    Node Details
                  </h3>
                  <div className="flex items-center gap-2">
                    <span className="font-mono text-[10px] text-primary uppercase font-bold px-1.5 py-0.5 rounded bg-primary/10 border border-primary/20">
                      {selectedNode.badge}
                    </span>
                    <button
                      onClick={() => setIsDrawerOpen(false)}
                      className="w-6 h-6 rounded-md hover:bg-surface-container flex items-center justify-center text-on-surface-variant hover:text-on-surface transition-colors"
                      title="Close Inspector"
                    >
                      <span className="material-symbols-outlined text-[16px]">close</span>
                    </button>
                  </div>
                </div>

                <div className="flex-1 overflow-y-auto p-4 space-y-4 text-xs font-mono">
                  <div>
                    <h2 className="font-display font-bold text-base text-on-surface mb-1">
                      {selectedNode.title}
                    </h2>
                    <p className="text-xs font-sans text-on-surface-variant leading-relaxed">
                      {selectedNode.description}
                    </p>
                  </div>

                  <div className="grid grid-cols-2 gap-2">
                    <div className="bg-surface-container p-2.5 rounded-lg border border-outline-variant/30">
                      <div className="text-[9px] text-on-surface-variant uppercase font-bold mb-0.5">Confidence</div>
                      <div className="text-sm font-extrabold text-primary">{selectedNode.confidence || 91}%</div>
                    </div>
                    <div className="bg-surface-container p-2.5 rounded-lg border border-outline-variant/30">
                      <div className="text-[9px] text-on-surface-variant uppercase font-bold mb-0.5">Metric</div>
                      <div className="text-sm font-extrabold text-on-surface">{selectedNode.metric}</div>
                    </div>
                  </div>

                  {selectedNode.evidenceId && (
                    <div className="p-3 rounded-lg bg-surface-dim border border-outline-variant/40 space-y-1">
                      <div className="text-[9px] text-on-surface-variant uppercase font-bold">Linked Evidence</div>
                      <div className="text-primary text-[10px] font-bold truncate">{selectedNode.evidenceId}</div>
                      {selectedNode.hash && (
                        <div className="text-[8px] text-on-surface-variant/60 truncate">
                          SHA-256: <code>{selectedNode.hash}</code>
                        </div>
                      )}
                    </div>
                  )}

                  <div className="space-y-2 pt-2 border-t border-outline-variant/30">
                    <div className="text-[9px] text-on-surface-variant uppercase font-bold">Connected Lineage</div>
                    <div className="space-y-1">
                      {selectedNode.linkedParents?.map((pid) => (
                        <button
                          key={pid}
                          onClick={() => handleSelectNode(pid)}
                          className="w-full text-left p-1.5 rounded bg-surface-container hover:bg-primary/10 border border-outline-variant/30 text-primary text-[10px] truncate flex items-center justify-between"
                        >
                          <span>← {pid.toUpperCase()}</span>
                        </button>
                      ))}
                      {selectedNode.linkedChildren?.map((cid) => (
                        <button
                          key={cid}
                          onClick={() => handleSelectNode(cid)}
                          className="w-full text-left p-1.5 rounded bg-surface-container hover:bg-primary/10 border border-outline-variant/30 text-primary text-[10px] truncate flex items-center justify-between"
                        >
                          <span>→ {cid.toUpperCase()}</span>
                        </button>
                      ))}
                    </div>
                  </div>
                </div>
              </aside>
            )}
          </div>
        </main>
      </div>
    </div>
  );
}
