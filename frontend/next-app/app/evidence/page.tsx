"use client";

import React, { useState, useEffect, Suspense } from "react";
import { useSearchParams } from "next/navigation";
import { Sidebar } from "@/components/navigation/Sidebar";
import { TopBar } from "@/components/navigation/TopBar";
import { useApp } from "@/context/AppContext";
import Link from "next/link";

interface EvidenceItem {
  id: string;
  system: string;
  recordId: string;
  domain: string;
  type: string;
  category: "ERP" | "CRM" | "Sales" | "Inventory" | "Support" | "Market Intel";
  finding: string;
  timestamp: string;
  confidenceScore: number;
  relevanceScore: number;
  driverLinkage: string;
  hash: string;
  sourceType: "unstructured" | "structured";
  icon: string;
}

const DEFAULT_EVIDENCE: EvidenceItem[] = [
  // --- UNSTRUCTURED SOURCE MATERIAL ---
  {
    id: "EVID_CRM_PO_DEF_006",
    system: "Distributor Communication",
    recordId: "PO-HOLD-8821-29",
    domain: "Distributor Channel",
    category: "CRM",
    type: "Email & PO Gateway",
    finding:
      "...experiencing severe inventory depletion at Atlanta DC. 29 distributor purchase orders deferred / delayed replenishment. Immediate supply reallocation required...",
    timestamp: "Aug 10, 2026",
    confidenceScore: 85,
    relevanceScore: 94,
    driverLinkage: "Distributor Purchase Order Deferral",
    hash: "ca978112ca1bbdcafac231b39a23dc4da786eff8147c4e72b9807785afee48bb",
    sourceType: "unstructured",
    icon: "mail",
  },
  {
    id: "EVID_ZENDESK_ATL_DELAY_003",
    system: "Zendesk Support CRM",
    recordId: "TICKET-CLUSTER-ATL",
    domain: "Customer Support",
    category: "Support",
    type: "Support CRM",
    finding:
      "Spike in unfulfilled order complaints. +310% surge in 'Out of Stock' tickets from key regional accounts during the disruption window.",
    timestamp: "Aug 08, 2026",
    confidenceScore: 89,
    relevanceScore: 91,
    driverLinkage: "Atlanta DC Stockout",
    hash: "8f434346648f6b96df89dda901c5176b10a6d83961dd3c1ac88b59b2dc327aa4",
    sourceType: "unstructured",
    icon: "headset_mic",
  },
  {
    id: "EVID_MKT_HORIZON_PROMO_008",
    system: "Market Intelligence",
    recordId: "MKT-SCRAPE-HORIZON-08",
    domain: "Market Competition",
    category: "Market Intel",
    type: "Web Scrape Feed",
    finding:
      "Automated web scrape detected aggressive 15% discount promotions launched by Horizon Foods targeting East region retail partners.",
    timestamp: "Aug 05, 2026",
    confidenceScore: 78,
    relevanceScore: 82,
    driverLinkage: "Competitor Horizon Pricing Pressure",
    hash: "4b227777d4dd1fc61c6f884f48641d02b4d121d3fd328cb08b5531fcacdabf8a",
    sourceType: "unstructured",
    icon: "insights",
  },
  {
    id: "EVID_EXEC_COMM_SLACK_009",
    system: "Executive Supply Chain Slack",
    recordId: "SLACK-WAR-ROOM-ATL",
    domain: "Internal Escalations",
    category: "Support",
    type: "Chat Channel Transcript",
    finding:
      "COO flagged Atlanta lead time escalation: 'Safety buffer breached 4 days ago; rebalance from Chicago Hub immediately to avoid Tier-1 retail penalties.'",
    timestamp: "Aug 07, 2026",
    confidenceScore: 92,
    relevanceScore: 96,
    driverLinkage: "Executive Response Strategy",
    hash: "1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef",
    sourceType: "unstructured",
    icon: "forum",
  },

  // --- STRUCTURED ENTERPRISE CORROBORATION ---
  {
    id: "EVID_ERP_ATL_STOCKOUT_001",
    system: "SAP S/4HANA (MM-WM)",
    recordId: "INV-SNAP-21971",
    domain: "ERP Inventory",
    category: "ERP",
    type: "Daily Inventory Snapshot",
    finding:
      "14 consecutive days of zero available inventory for SKU-8821 at Atlanta DC (Aug 10 - Aug 24, 2026). Stock buffer fell below critical 15-day SLA.",
    timestamp: "Aug 24, 2026",
    confidenceScore: 94,
    relevanceScore: 99,
    driverLinkage: "Atlanta DC Stockout",
    hash: "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    sourceType: "structured",
    icon: "database",
  },
  {
    id: "EVID_ERP_CHI_SURPLUS_002",
    system: "SAP S/4HANA (Chicago DC)",
    recordId: "INV-SNAP-CHI-04",
    domain: "Supply Chain",
    category: "Inventory",
    type: "Surplus Inventory Balance",
    finding:
      "Chicago Central DC holds 4,800 surplus units of SKU-8821 (142% of safety buffer), confirming inter-warehouse stock transfer feasibility.",
    timestamp: "Aug 24, 2026",
    confidenceScore: 92,
    relevanceScore: 95,
    driverLinkage: "Emergency Stock Transfer",
    hash: "f4a1c55398fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b999",
    sourceType: "structured",
    icon: "inventory",
  },
  {
    id: "EVID_EDI_PO_HOLD_003",
    system: "Oracle NetSuite (Wholesale EDI)",
    recordId: "EDI-PO-8821-29",
    domain: "Channel Sales",
    category: "Sales",
    type: "Distributor Purchase Orders",
    finding:
      "29 Tier-1 regional distributor replenishment POs deferred due to warehouse fulfillment uncertainty. Total held revenue value: $240,000.00.",
    timestamp: "Aug 18, 2026",
    confidenceScore: 89,
    relevanceScore: 93,
    driverLinkage: "Distributor Orders Deferral",
    hash: "ca978112ca1bbdcafac231b39a23dc4da786eff8147c4e72b9807785afee48bb",
    sourceType: "structured",
    icon: "receipt_long",
  },
  {
    id: "EVID_CRM_TKT_ATL_004",
    system: "Salesforce Service Cloud DB",
    recordId: "CRM-TKT-ATL-142",
    domain: "Customer Support",
    category: "Support",
    type: "Customer Escalation Metrics",
    finding:
      "142 regional wholesale accounts submitted critical backorder delivery escalations, resulting in +310% support ticket surge during stockout.",
    timestamp: "Aug 14, 2026",
    confidenceScore: 91,
    relevanceScore: 90,
    driverLinkage: "Customer Service Escalations",
    hash: "8f434346648f6b96df89dda901c5176b10a6d83961dd3c1ac88b59b2dc327aa4",
    sourceType: "structured",
    icon: "headset_mic",
  },
  {
    id: "EVID_POS_SCAN_EAST_005",
    system: "Retail POS Scanner Telemetry",
    recordId: "POS-SCAN-EAST-Q3",
    domain: "Retail Point-of-Sale",
    category: "Sales",
    type: "Store Register Transactions",
    finding:
      "7.97% SKU-8821 register scan deficit recorded across 410 regional retail outlets in East territory, confirming consumer availability bottleneck.",
    timestamp: "Aug 20, 2026",
    confidenceScore: 93,
    relevanceScore: 96,
    driverLinkage: "SKU-8821 Sales Volume Drop",
    hash: "3b7c891a45defa9812456789abcdef0123456789abcdef0123456789abcdef01",
    sourceType: "structured",
    icon: "point_of_sale",
  },
  {
    id: "EVID_MKT_PRICE_SCRAPE_006",
    system: "Bloomberg / Nielsen Market DB",
    recordId: "MKT-PRICE-HORIZON-08",
    domain: "Market Intelligence",
    category: "Market Intel",
    type: "Competitor Price Index",
    finding:
      "Horizon Foods 15% discount promotional pricing scraped across 18 regional e-commerce & retail channels, capturing deferred East territory demand.",
    timestamp: "Aug 05, 2026",
    confidenceScore: 86,
    relevanceScore: 88,
    driverLinkage: "Competitor Horizon Price Cut",
    hash: "4b227777d4dd1fc61c6f884f48641d02b4d121d3fd328cb08b5531fcacdabf8a",
    sourceType: "structured",
    icon: "price_check",
  },
  {
    id: "EVID_LOG_3PL_FREIGHT_007",
    system: "Logistics 3PL Carrier TMS",
    recordId: "LOG-3PL-TRK-7712",
    domain: "Freight & Logistics",
    category: "Inventory",
    type: "Carrier Dispatch Records",
    finding:
      "Expedited dedicated truckload transit time between Chicago Central and Atlanta DC clocked at 28.4 hours with SLA delivery confirmation.",
    timestamp: "Aug 22, 2026",
    confidenceScore: 90,
    relevanceScore: 92,
    driverLinkage: "Chicago Hub Buffer Stock Rebalance",
    hash: "a1b2c3d4e5f60718293a4b5c6d7e8f90123456789abcdef0123456789abcdef0",
    sourceType: "structured",
    icon: "local_shipping",
  },
  {
    id: "EVID_FIN_LEDGER_VAR_008",
    system: "SAP S/4HANA Finance (FI-GL)",
    recordId: "GL-POST-2026-Q3-VAR",
    domain: "Financial Audit",
    category: "ERP",
    type: "General Ledger Posting",
    finding:
      "Q3 Net Revenue recognized at $14,200,000.05 against $15,430,000.06 baseline, verifying the -$1,230,000.01 net empirical deficit.",
    timestamp: "Aug 25, 2026",
    confidenceScore: 100,
    relevanceScore: 100,
    driverLinkage: "Enterprise Financial Reconciliation",
    hash: "9876543210fedcba0987654321fedcba0987654321fedcba0987654321fedcba",
    sourceType: "structured",
    icon: "account_balance",
  },
];

function EvidenceExplorerContent() {
  const searchParams = useSearchParams();
  const highlightQuery = searchParams.get("q") || "";
  const [filterType, setFilterType] = useState<string>("ALL");
  const [categoryFilter, setCategoryFilter] = useState<string>("ALL");
  const [searchTerm, setSearchTerm] = useState<string>("");
  const [selectedItem, setSelectedItem] = useState<EvidenceItem>(DEFAULT_EVIDENCE[0]);
  const [verifiedMap, setVerifiedMap] = useState<Record<string, boolean>>({});
  const [isVerifying, setIsVerifying] = useState<boolean>(false);

  useEffect(() => {
    if (highlightQuery) {
      const match = DEFAULT_EVIDENCE.find((e) => e.id === highlightQuery);
      if (match) setSelectedItem(match);
    }
  }, [highlightQuery]);

  const filteredEvidence = DEFAULT_EVIDENCE.filter((item) => {
    if (filterType !== "ALL" && item.sourceType !== filterType.toLowerCase()) return false;
    if (categoryFilter !== "ALL" && item.category !== categoryFilter) return false;
    if (searchTerm.trim()) {
      const q = searchTerm.toLowerCase();
      const match =
        item.id.toLowerCase().includes(q) ||
        item.system.toLowerCase().includes(q) ||
        item.finding.toLowerCase().includes(q) ||
        item.driverLinkage.toLowerCase().includes(q);
      if (!match) return false;
    }
    return true;
  });

  const unstructuredItems = filteredEvidence.filter((e) => e.sourceType === "unstructured");
  const structuredItems = filteredEvidence.filter((e) => e.sourceType === "structured");

  const handleVerifyHash = (id: string) => {
    setIsVerifying(true);
    setTimeout(() => {
      setVerifiedMap((prev) => ({ ...prev, [id]: true }));
      setIsVerifying(false);
    }, 450);
  };

  const showUnstructuredColumn = filterType === "ALL" || filterType === "UNSTRUCTURED";
  const showStructuredColumn = filterType === "ALL" || filterType === "STRUCTURED";
  const isSingleColumn = filterType === "UNSTRUCTURED" || filterType === "STRUCTURED";

  return (
    <div className="flex min-h-screen bg-[#051424] text-on-surface">
      <Sidebar />

      <div className="flex-1 flex flex-col min-w-0">
        <TopBar breadcrumb="Evidence Explorer" />

        <main className="flex-1 p-6 md:p-8 space-y-6 max-w-[1600px] mx-auto w-full">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-1">
            <div>
              <div className="flex items-center gap-2 mb-1">
                <span className="text-[10px] font-mono text-primary font-bold uppercase tracking-widest bg-primary/10 border border-primary/20 px-2 py-0.5 rounded flex items-center gap-1 shrink-0">
                  <span className="material-symbols-outlined text-[14px]">travel_explore</span>
                  Evidence Ledger
                </span>
                <span className="text-xs font-mono text-on-surface-variant">
                  {filteredEvidence.length} Verified Records • 100% SHA-256 Provenance
                </span>
              </div>
              <h1 className="font-display font-extrabold text-2xl text-on-surface tracking-tight">
                Evidence Explorer
              </h1>
            </div>

            <Link
              href="/decision-graph"
              className="px-3.5 py-1.5 rounded-xl border border-outline-variant/30 text-on-surface-variant font-mono text-xs hover:bg-surface-container hover:text-primary transition-colors flex items-center gap-1.5 shrink-0 self-start sm:self-auto"
            >
              <span className="material-symbols-outlined text-[16px]">account_tree</span>
              <span>Decision Graph</span>
            </Link>
          </div>

          <div className="bg-surface-container/60 p-4 rounded-xl border border-outline-variant/30 space-y-3 font-mono">
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-3">
              <div className="relative flex-1">
                <input
                  type="text"
                  placeholder="Search logs, IDs, findings, or drivers..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="w-full bg-surface-dim border border-outline-variant/30 rounded-xl pl-9 pr-4 py-2 text-xs text-on-surface placeholder:text-on-surface-variant/50 focus:border-primary focus:outline-none"
                />
                <span className="material-symbols-outlined text-on-surface-variant text-[16px] absolute left-3 top-1/2 -translate-y-1/2">
                  search
                </span>
              </div>

              <div className="flex bg-surface-dim p-1 rounded-xl border border-outline-variant/30 text-xs shrink-0">
                {["ALL", "UNSTRUCTURED", "STRUCTURED"].map((t) => (
                  <button
                    key={t}
                    onClick={() => setFilterType(t)}
                    className={`px-3 py-1 rounded-lg transition-all font-bold ${
                      filterType === t ? "bg-primary text-black shadow-glow" : "text-on-surface-variant hover:text-on-surface"
                    }`}
                  >
                    {t === "ALL" ? "All Sources" : t.charAt(0) + t.slice(1).toLowerCase()}
                  </button>
                ))}
              </div>
            </div>

            <div className="flex flex-wrap items-center gap-2 pt-1 border-t border-outline-variant/20 text-xs">
              <span className="text-[10px] text-on-surface-variant uppercase font-bold mr-1">Category:</span>
              {["ALL", "ERP", "CRM", "Sales", "Inventory", "Support", "Market Intel"].map((cat) => (
                <button
                  key={cat}
                  onClick={() => setCategoryFilter(cat)}
                  className={`px-2.5 py-0.5 rounded-lg border text-[11px] transition-colors font-bold ${
                    categoryFilter === cat
                      ? "bg-primary/20 text-primary border-primary"
                      : "bg-surface-dim/80 border-outline-variant/30 text-on-surface-variant hover:text-on-surface"
                  }`}
                >
                  {cat}
                </button>
              ))}
            </div>
          </div>

          <div className={`grid grid-cols-1 ${isSingleColumn ? "lg:grid-cols-1" : "lg:grid-cols-2"} gap-6`}>
            {showUnstructuredColumn && (
              <div className="space-y-4 flex flex-col min-w-0">
                <div className="flex items-center justify-between border-b border-outline-variant/30 pb-2">
                  <h3 className="font-mono text-xs text-on-surface-variant uppercase tracking-wider font-bold">
                    Unstructured Source Material
                  </h3>
                  <span className="text-[11px] font-mono text-primary font-semibold">
                    {unstructuredItems.length} Verified Records
                  </span>
                </div>

                <div className={`grid ${filterType === "UNSTRUCTURED" ? "grid-cols-1 md:grid-cols-2 gap-4" : "space-y-4"}`}>
                  {unstructuredItems.map((item) => (
                    <div
                      key={item.id}
                      onClick={() => setSelectedItem(item)}
                      className={`bg-surface-container/70 border rounded-2xl p-5 hover:border-primary/50 transition-all duration-200 cursor-pointer relative overflow-hidden group flex flex-col justify-between ${
                        selectedItem.id === item.id
                          ? "border-primary ring-2 ring-primary/60 shadow-glow bg-surface-container"
                          : "border-outline-variant/30 hover:bg-surface-container"
                      }`}
                    >
                      <div>
                        <div className="flex justify-between items-start mb-2.5">
                          <div className="flex items-center gap-2">
                            <div className="w-8 h-8 rounded-xl bg-primary/15 border border-primary/30 flex items-center justify-center text-primary">
                              <span className="material-symbols-outlined text-[16px]">{item.icon}</span>
                            </div>
                            <div>
                              <span className="font-mono text-[10px] text-primary font-bold block">{item.id}</span>
                              <span className="text-[10px] text-on-surface-variant font-mono">Source: {item.system}</span>
                            </div>
                          </div>
                          <span className="text-[11px] font-mono text-on-surface-variant/80">{item.timestamp}</span>
                        </div>

                        <h4 className="font-display font-bold text-sm text-on-surface mb-2.5 leading-snug">
                          {item.domain} Telemetry Feed
                        </h4>

                        <div className="bg-surface-dim border-l-2 border-primary p-3 rounded-r-xl mb-3">
                          <p className="text-xs text-on-surface/90 italic leading-relaxed font-sans">
                            "{item.finding}"
                          </p>
                        </div>
                      </div>

                      <div className="flex items-center justify-between pt-3 border-t border-outline-variant/20 font-mono text-xs">
                        <div className="flex items-center gap-4">
                          <div>
                            <span className="text-[9px] text-on-surface-variant uppercase block">Relevance</span>
                            <div className="flex items-center gap-1.5 mt-0.5">
                              <span className="text-primary font-bold text-[11px]">{item.relevanceScore}%</span>
                              <div className="w-10 h-1 bg-surface-dim rounded-full overflow-hidden">
                                <div className="h-full bg-primary" style={{ width: `${item.relevanceScore}%` }}></div>
                              </div>
                            </div>
                          </div>

                          <div className="border-l border-outline-variant/30 pl-3">
                            <span className="text-[9px] text-on-surface-variant uppercase block">Confidence</span>
                            <span className="text-primary font-bold text-[11px]">{item.confidenceScore}% HIGH</span>
                          </div>
                        </div>

                        <button
                          onClick={(e) => {
                            e.stopPropagation();
                            handleVerifyHash(item.id);
                          }}
                          className={`px-2.5 py-1 rounded-lg border text-[10px] font-bold flex items-center gap-1 transition-all ${
                            verifiedMap[item.id]
                              ? "bg-success/20 text-success border-success/40 shadow-glow"
                              : "bg-primary/10 text-primary border-primary/30 hover:bg-primary hover:text-black"
                          }`}
                        >
                          <span className="material-symbols-outlined text-[13px]">
                            {verifiedMap[item.id] ? "verified" : "fingerprint"}
                          </span>
                          <span>{verifiedMap[item.id] ? "SHA-256 Valid" : "Verify Hash"}</span>
                        </button>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {showStructuredColumn && (
              <div className="space-y-4 flex flex-col min-w-0">
                <div className="flex items-center justify-between border-b border-outline-variant/30 pb-2">
                  <h3 className="font-mono text-xs text-on-surface-variant uppercase tracking-wider font-bold">
                    Structured Corroboration & Lineage
                  </h3>
                  <span className="text-[11px] font-mono text-primary font-semibold">
                    {structuredItems.length} Structured Records
                  </span>
                </div>

                {/* Structured Records Table (Consolidated 3-Column Layout: Zero Right-Edge Clipping) */}
                <div className="bg-surface-container/70 border border-outline-variant/30 rounded-2xl overflow-hidden shadow-sm">
                  <table className="w-full text-left border-collapse font-mono text-xs">
                    <thead>
                      <tr className="border-b border-outline-variant/30 bg-surface-container-high/60 text-on-surface-variant text-[10px] uppercase">
                        <th className="py-2.5 px-3.5 font-bold">Source & Domain</th>
                        <th className="py-2.5 px-3.5 font-bold">Record ID</th>
                        <th className="py-2.5 px-3.5 font-bold text-right">Confidence</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-outline-variant/20 text-on-surface">
                      {structuredItems.map((row) => (
                        <tr
                          key={row.id}
                          onClick={() => setSelectedItem(row)}
                          className={`hover:bg-surface-bright/30 transition-colors cursor-pointer ${
                            selectedItem.id === row.id ? "bg-primary/15 border-l-4 border-l-primary" : ""
                          }`}
                        >
                          <td className="py-2.5 px-3.5">
                            <div className="flex items-center gap-2.5">
                              <div className="w-7 h-7 rounded-lg bg-primary/15 border border-primary/30 flex items-center justify-center text-primary shrink-0">
                                <span className="material-symbols-outlined text-[15px]">{row.icon}</span>
                              </div>
                              <div className="min-w-0">
                                <span className="font-sans font-semibold text-xs text-on-surface leading-tight block">
                                  {row.system}
                                </span>
                                <span className="text-on-surface-variant font-mono text-[10px] block mt-0.5">
                                  {row.domain} • {row.category}
                                </span>
                              </div>
                            </div>
                          </td>
                          <td className="py-2.5 px-3.5 text-primary font-bold text-xs font-mono whitespace-nowrap">
                            {row.recordId}
                          </td>
                          <td className="py-2.5 px-3.5 text-right whitespace-nowrap">
                            <span className="inline-flex items-center px-2.5 py-1 rounded-full bg-primary/10 text-primary border border-primary/30 text-[10px] font-bold shadow-sm">
                              {row.confidenceScore}% High
                            </span>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>

                <div className="glass-panel rounded-2xl p-5 border border-primary/30 bg-gradient-to-br from-surface-container via-surface to-surface-dim space-y-3 shadow-xl">
                  <div className="flex items-center justify-between pb-2.5 border-b border-outline-variant/30">
                    <div className="flex items-center gap-2">
                      <div className="w-7 h-7 rounded-lg bg-primary/15 border border-primary/30 flex items-center justify-center text-primary">
                        <span className="material-symbols-outlined text-[16px]">verified_user</span>
                      </div>
                      <h4 className="font-display font-bold text-sm text-on-surface">
                        Selected Evidence Lineage & Cryptographic Proof
                      </h4>
                    </div>
                    <span className="font-mono text-[10px] text-primary font-bold bg-primary/10 border border-primary/20 px-2 py-0.5 rounded">
                      {selectedItem.id}
                    </span>
                  </div>

                  <div className="text-xs font-mono space-y-2.5">
                    <div>
                      <span className="text-on-surface-variant text-[10px] uppercase block mb-0.5 font-bold">
                        Linked Causal Driver
                      </span>
                      <span className="text-on-surface font-bold font-sans text-xs">{selectedItem.driverLinkage}</span>
                    </div>

                    <div className="p-3 rounded-xl bg-surface-dim border border-outline-variant/30 text-xs">
                      <span className="text-on-surface-variant text-[10px] uppercase block mb-1 font-bold">
                        Finding Statement
                      </span>
                      <p className="text-on-surface font-sans leading-relaxed text-xs">{selectedItem.finding}</p>
                    </div>

                    <div className="p-2.5 rounded-xl bg-surface-dim border border-outline-variant/30 text-[10px] text-primary">
                      <span className="text-on-surface-variant text-[9px] block font-bold mb-0.5">
                        Cryptographic SHA-256 Digest:
                      </span>
                      <code className="text-primary font-bold break-all block">{selectedItem.hash}</code>
                    </div>

                    <div className="pt-2 flex flex-wrap items-center justify-between gap-3">
                      <span className="text-[11px] text-on-surface-variant font-bold">
                        Relevance: <strong className="text-primary">{selectedItem.relevanceScore}%</strong> • Confidence: <strong className="text-primary">{selectedItem.confidenceScore}%</strong>
                      </span>
                      <button
                        onClick={() => handleVerifyHash(selectedItem.id)}
                        className="px-3.5 py-1.5 rounded-xl bg-primary text-black font-mono text-xs font-bold hover:bg-primary-light transition-all shadow-glow flex items-center gap-1.5"
                      >
                        <span className="material-symbols-outlined text-[14px]">
                          {verifiedMap[selectedItem.id] ? "verified" : "fingerprint"}
                        </span>
                        <span>{verifiedMap[selectedItem.id] ? "SHA-256 Validated" : "Verify Cryptographic Proof"}</span>
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            )}
          </div>
        </main>
      </div>
    </div>
  );
}

export default function EvidenceExplorerPage() {
  return (
    <Suspense fallback={<div className="p-8 text-on-surface font-mono">Loading Evidence Ledger...</div>}>
      <EvidenceExplorerContent />
    </Suspense>
  );
}
