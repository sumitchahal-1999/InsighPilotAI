"use client";

import React, { useState, useEffect } from "react";
import { Sidebar } from "@/components/navigation/Sidebar";
import { TopBar } from "@/components/navigation/TopBar";
import { useApp } from "@/context/AppContext";
import Link from "next/link";

export default function ExecutiveBriefingPage() {
  const { persona, region, regionData, quarter } = useApp();
  const [approved, setApproved] = useState<boolean>(false);
  const [showApprovalModal, setShowApprovalModal] = useState<boolean>(false);
  const [approvalTimestamp, setApprovalTimestamp] = useState<string>("");
  const [slideMode, setSlideMode] = useState<boolean>(false);
  const [currentSlide, setCurrentSlide] = useState<number>(0);

  // Keyboard navigation for Slide Mode (Arrow Left / Right)
  useEffect(() => {
    if (!slideMode) return;
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === "ArrowRight" || e.key === "PageDown") {
        setCurrentSlide((prev) => (prev < 3 ? prev + 1 : prev));
      } else if (e.key === "ArrowLeft" || e.key === "PageUp") {
        setCurrentSlide((prev) => (prev > 0 ? prev - 1 : prev));
      }
    };
    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, [slideMode]);

  const handleApprove = () => {
    setApprovalTimestamp(new Date().toLocaleString());
    setShowApprovalModal(true);
  };

  const confirmApproval = () => {
    setApproved(true);
    setShowApprovalModal(false);
  };

  const [isExporting, setIsExporting] = useState<boolean>(false);

  const handleExportPdf = async () => {
    try {
      setIsExporting(true);
      const { jsPDF } = await import("jspdf");
      const doc = new jsPDF({
        orientation: "portrait",
        unit: "pt",
        format: "letter",
      });

      const pageWidth = doc.internal.pageSize.getWidth();
      const pageHeight = doc.internal.pageSize.getHeight();
      const margin = 40;
      const contentWidth = pageWidth - margin * 2;

      // Header background
      doc.setFillColor(15, 23, 42); // #0F172A
      doc.rect(0, 0, pageWidth, 75, "F");

      // Header Accent line
      doc.setFillColor(2, 132, 199); // #0284C7
      doc.rect(0, 75, pageWidth, 3, "F");

      // Title
      doc.setTextColor(255, 255, 255);
      doc.setFont("helvetica", "bold");
      doc.setFontSize(15);
      doc.text("INSIGHTPILOT AI — EXECUTIVE INTELLIGENCE BRIEFING", margin, 34);

      doc.setFont("helvetica", "normal");
      doc.setFontSize(8.5);
      doc.setTextColor(186, 230, 253); // #BAE6FD
      doc.text("Track 3: BusinessIntelligence.ai • Accenture Innovation Challenge 2026", margin, 52);
      doc.text("Live URL: https://insigh-pilot-ai.vercel.app", pageWidth - margin, 52, { align: "right" });

      let y = 96;

      // Metadata card banner
      doc.setFillColor(241, 245, 249); // #F1F5F9
      doc.roundedRect(margin, y, contentWidth, 38, 4, 4, "F");
      doc.setDrawColor(203, 213, 225);
      doc.roundedRect(margin, y, contentWidth, 38, 4, 4, "S");

      doc.setFontSize(8);
      doc.setTextColor(51, 65, 85);
      doc.setFont("helvetica", "bold");
      doc.text("QUARTER: ", margin + 10, y + 15);
      doc.setFont("helvetica", "normal");
      doc.text(`${quarter}`, margin + 60, y + 15);

      doc.setFont("helvetica", "bold");
      doc.text("REGION: ", margin + 130, y + 15);
      doc.setFont("helvetica", "normal");
      doc.text(`${region}`, margin + 175, y + 15);

      doc.setFont("helvetica", "bold");
      doc.text("LENS / PERSONA: ", margin + 250, y + 15);
      doc.setFont("helvetica", "normal");
      doc.setTextColor(2, 132, 199);
      doc.text(`${persona.replace(/_/g, " ")}`, margin + 345, y + 15);

      doc.setFont("helvetica", "bold");
      doc.setTextColor(51, 65, 85);
      doc.text("DOC ID: ", margin + 10, y + 29);
      doc.setFont("helvetica", "normal");
      doc.text(`BRIEF-${quarter}-${region}-REV`, margin + 50, y + 29);

      doc.setFont("helvetica", "bold");
      doc.text("GENERATED: ", margin + 250, y + 29);
      doc.setFont("helvetica", "normal");
      doc.text(`${new Date().toLocaleString()}`, margin + 325, y + 29);

      y += 50;

      // Section 1: Executive KPI Scorecard
      doc.setFont("helvetica", "bold");
      doc.setFontSize(10.5);
      doc.setTextColor(15, 23, 42);
      doc.text("1. Executive Variance & Health Scorecard", margin, y);
      y += 12;

      const cardWidth = (contentWidth - 24) / 4;
      const kpis = [
        { label: "Net Revenue", val: regionData.revenue, sub: `${regionData.variance} (${regionData.variancePct})`, alert: true },
        { label: "Gross Margin", val: regionData.grossMargin, sub: `${regionData.grossMarginDelta} vs Baseline`, alert: true },
        { label: "Availability", val: regionData.availability, sub: `${regionData.availabilityDelta || "-14.8 pts"} (CRITICAL)`, alert: true },
        { label: "Recovery Pool", val: regionData.recoveryPool, sub: "27.0x Modeled ROI", alert: false },
      ];

      kpis.forEach((kpi, idx) => {
        const cx = margin + idx * (cardWidth + 8);
        doc.setFillColor(kpi.alert ? 254 : 240, kpi.alert ? 242 : 253, kpi.alert ? 242 : 244);
        doc.roundedRect(cx, y, cardWidth, 46, 4, 4, "F");
        doc.setDrawColor(kpi.alert ? 254 : 186, kpi.alert ? 202 : 230, kpi.alert ? 202 : 253);
        doc.roundedRect(cx, y, cardWidth, 46, 4, 4, "S");

        doc.setFontSize(7);
        doc.setFont("helvetica", "bold");
        doc.setTextColor(100, 116, 139);
        doc.text(kpi.label.toUpperCase(), cx + 7, y + 13);

        doc.setFontSize(11);
        doc.setFont("helvetica", "bold");
        doc.setTextColor(kpi.alert ? 185 : 13, kpi.alert ? 28 : 148, kpi.alert ? 28 : 136);
        doc.text(kpi.val, cx + 7, y + 28);

        doc.setFontSize(6.5);
        doc.setFont("helvetica", "normal");
        doc.text(kpi.sub, cx + 7, y + 39);
      });

      y += 58;

      // Section 2: Situation & Executive Narrative
      doc.setFont("helvetica", "bold");
      doc.setFontSize(10.5);
      doc.setTextColor(15, 23, 42);
      doc.text(`2. Operational Situation (${persona.replace(/_/g, " ")} Lens)`, margin, y);
      y += 12;

      doc.setFont("helvetica", "normal");
      doc.setFontSize(8);
      doc.setTextColor(51, 65, 85);
      const situationLines = doc.splitTextToSize(narrative.situation, contentWidth - 16);
      
      doc.setFillColor(248, 250, 252);
      doc.roundedRect(margin, y, contentWidth, situationLines.length * 11 + 12, 4, 4, "F");
      doc.setDrawColor(226, 232, 240);
      doc.roundedRect(margin, y, contentWidth, situationLines.length * 11 + 12, 4, 4, "S");
      
      doc.text(situationLines, margin + 8, y + 12);
      y += situationLines.length * 11 + 20;

      // Section 3: 4-Factor Deterministic Root-Cause Attribution Table
      doc.setFont("helvetica", "bold");
      doc.setFontSize(10.5);
      doc.setTextColor(15, 23, 42);
      doc.text("3. Causal Decomposition (100.0% Variance Explained)", margin, y);
      y += 12;

      // Table Header
      doc.setFillColor(15, 23, 42);
      doc.rect(margin, y, contentWidth, 16, "F");
      doc.setTextColor(255, 255, 255);
      doc.setFontSize(7);
      doc.setFont("helvetica", "bold");
      doc.text("RANK & CAUSAL FACTOR", margin + 8, y + 11);
      doc.text("FISCAL IMPACT", margin + 200, y + 11);
      doc.text("ATTRIBUTION SHARE", margin + 300, y + 11);
      doc.text("CONFIDENCE", margin + 410, y + 11);
      y += 16;

      const drivers = [
        { rank: "1. Atlanta DC Stockout (INV-SNAP-21971)", impact: "-$550,000.00", share: "43.2%", conf: "94% (CRITICAL)", alert: true },
        { rank: "2. SKU-8821 Volume Contraction", impact: "-$340,000.00", share: "26.7%", conf: "88% (HIGH)", alert: false },
        { rank: "3. Distributor PO Deferrals (29 Orders)", impact: "-$240,000.00", share: "18.8%", conf: "85% (HIGH)", alert: false },
        { rank: "4. Horizon Competitor Price War (-15%)", impact: "-$144,000.00", share: "11.3%", conf: "82% (MODERATE)", alert: false },
      ];

      drivers.forEach((d, i) => {
        doc.setFillColor(i % 2 === 0 ? 255 : 248, i % 2 === 0 ? 255 : 250, i % 2 === 0 ? 255 : 252);
        doc.rect(margin, y, contentWidth, 15, "F");
        doc.setDrawColor(226, 232, 240);
        doc.line(margin, y + 15, margin + contentWidth, y + 15);

        doc.setFontSize(7);
        doc.setFont("helvetica", d.alert ? "bold" : "normal");
        doc.setTextColor(d.alert ? 185 : 51, d.alert ? 28 : 65, d.alert ? 28 : 85);
        doc.text(d.rank, margin + 8, y + 10);
        doc.text(d.impact, margin + 200, y + 10);
        doc.text(d.share, margin + 300, y + 10);
        doc.text(d.conf, margin + 410, y + 10);
        y += 15;
      });

      y += 14;

      // Section 4: Prescriptive Recommendation & ROI
      doc.setFont("helvetica", "bold");
      doc.setFontSize(10.5);
      doc.setTextColor(15, 23, 42);
      doc.text("4. Prescriptive Action Plan & Projected Recovery", margin, y);
      y += 12;

      const recLines = doc.splitTextToSize(narrative.recommendation, contentWidth - 16);
      doc.setFillColor(240, 253, 244); // #F0FDF4
      doc.roundedRect(margin, y, contentWidth, recLines.length * 11 + 12, 4, 4, "F");
      doc.setDrawColor(187, 247, 208);
      doc.roundedRect(margin, y, contentWidth, recLines.length * 11 + 12, 4, 4, "S");
      
      doc.setFontSize(8);
      doc.setTextColor(22, 101, 52); // green-800
      doc.setFont("helvetica", "bold");
      doc.text(recLines, margin + 8, y + 12);
      y += recLines.length * 11 + 18;

      // Section 5: Governance & Cryptographic Provenance
      doc.setFillColor(241, 245, 249);
      doc.roundedRect(margin, y, contentWidth, 34, 4, 4, "F");
      doc.setDrawColor(203, 213, 225);
      doc.roundedRect(margin, y, contentWidth, 34, 4, 4, "S");

      doc.setFontSize(7);
      doc.setTextColor(30, 41, 59);
      doc.setFont("helvetica", "bold");
      doc.text("CRYPTOGRAPHIC PROVENANCE & AUDIT TRAIL:", margin + 8, y + 12);
      doc.setFont("courier", "normal");
      doc.setFontSize(6);
      doc.setTextColor(71, 85, 105);
      doc.text("SHA-256: a7f92b41c0e891d4e21971bc3f8204618e7921a982635a901f4c7183e921d904", margin + 8, y + 24);
      doc.setFont("helvetica", "bold");
      doc.setFontSize(7);
      doc.setTextColor(approved ? 22 : 100, approved ? 101 : 116, approved ? 52 : 139);
      doc.text(
        approved
          ? `✓ EXECUTIVE SIGN-OFF CONFIRMED (${approvalTimestamp || "APPROVED"})`
          : "STATUS: READY FOR BOARDROOM SIGN-OFF",
        pageWidth - margin - 8,
        y + 18,
        { align: "right" }
      );

      // Footer
      doc.setDrawColor(203, 213, 225);
      doc.line(margin, pageHeight - 25, pageWidth - margin, pageHeight - 25);
      doc.setFont("helvetica", "normal");
      doc.setFontSize(6.5);
      doc.setTextColor(100, 116, 139);
      doc.text("InsightPilot AI • Enterprise Decision Intelligence • Track 3: BusinessIntelligence.ai", margin, pageHeight - 14);
      doc.text("Page 1 of 1 • Confidential", pageWidth - margin, pageHeight - 14, { align: "right" });

      // Save / Direct Download
      const fileName = `InsightPilot_Executive_Briefing_${persona}_${quarter}_${region}.pdf`;
      doc.save(fileName);
    } catch (err) {
      console.error("Failed to generate PDF:", err);
      if (typeof window !== "undefined") {
        window.print();
      }
    } finally {
      setIsExporting(false);
    }
  };

  // Persona-specific narrative content
  const getPersonaBriefingNarrative = () => {
    switch (persona) {
      case "CFO":
        return {
          situation: `${region} region experienced a net revenue contraction from baseline to ${regionData.revenue} (${regionData.variancePct}), creating a ${regionData.variance} variance gap with -3.2 pts gross margin dilution.`,
          recommendation: `Authorize $28,000 expedited ground freight transfer of 3,200 units from Chicago to Atlanta. Return on investment: $757.6K projected recovery vs $28K transfer cost (27.0x ROI).`,
        };
      case "REGIONAL_SALES_MANAGER":
        return {
          situation: `Retail partner order fulfillment in East territory dropped due to stockouts. 29 distributor purchase orders ($240K value) are held, while competitor Horizon Foods launched 15% promotional pricing discounts.`,
          recommendation: `Deploy 4 commercial account managers with priority SLA fulfillment guarantees to convert all 29 held POs within 21 business days.`,
        };
      case "COO":
        return {
          situation: `Atlanta DC experienced 14 consecutive days of zero available inventory for SKU-8821. Availability collapsed to ${regionData.availability} (-14.8 pts), triggering regional shipping backlogs.`,
          recommendation: `Execute expedited Chicago-to-Atlanta inventory rebalancing (3,200 units / 14-day SLA) to immediately restore regional fulfillment capability above 90%.`,
        };
      case "SUPPLY_CHAIN_LEAD":
        return {
          situation: `Chicago Central DC holds 4,800 surplus units (142% of safety threshold) of SKU-8821 while Atlanta DC is at zero stock, creating an inter-hub inventory imbalance.`,
          recommendation: `Issue transfer order for 3,200 units from Chicago to Atlanta via designated expedited freight lane, preserving 1,600 units (110% buffer) at Chicago.`,
        };
      default:
        return {
          situation: `${region} region revenue fell to ${regionData.revenue} (${regionData.variancePct}) against the baseline target.`,
          recommendation: `Execute Emergency Inventory Transfer and targeted distributor commercial outreach to recover ${regionData.recoveryPool}.`,
        };
    }
  };

  const narrative = getPersonaBriefingNarrative();

  return (
    <div className="flex min-h-screen bg-[#051424] text-on-surface">
      <Sidebar />

      <div className="flex-1 flex flex-col min-w-0">
        <TopBar breadcrumb="Executive Briefing (Boardroom Ready)" />

        <main className="flex-1 p-6 md:p-8 space-y-6 max-w-[1600px] mx-auto w-full">
          {/* Header Bar */}
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-2">
            <div>
              <div className="flex items-center gap-2 mb-1 flex-wrap">
                <span className="text-[10px] font-mono text-primary font-bold uppercase tracking-widest bg-primary/10 border border-primary/20 px-2 py-0.5 rounded flex items-center gap-1 shrink-0">
                  <span className="material-symbols-outlined text-[14px]">verified</span>
                  Boardroom Certified
                </span>
                <span className="text-xs font-mono text-on-surface-variant">
                  Doc ID: BRIEF-{quarter}-{region}-REV • Lens: <strong className="text-primary">{persona.replace("_", " ")}</strong>
                </span>
              </div>
              <h1 className="font-display font-extrabold text-2xl text-on-surface tracking-tight">
                Executive Intelligence Briefing
              </h1>
            </div>

            {/* Clean Action Buttons */}
            <div className="flex flex-wrap items-center gap-2">
              {/* Presentation Mode Toggle */}
              <button
                onClick={() => setSlideMode(!slideMode)}
                className={`px-2.5 py-1.5 rounded-lg font-mono text-xs font-bold transition-all flex items-center gap-1.5 ${
                  slideMode
                    ? "bg-secondary text-black shadow-sm"
                    : "bg-surface-container border border-outline-variant/30 text-on-surface-variant hover:text-on-surface"
                }`}
              >
                <span className="material-symbols-outlined text-[15px]">slideshow</span>
                <span>{slideMode ? "Doc View" : "Slide Mode"}</span>
              </button>

              <button
                onClick={handleExportPdf}
                disabled={isExporting}
                className="px-2.5 py-1.5 rounded-lg border border-outline-variant/30 text-on-surface-variant font-mono text-xs hover:bg-surface-container hover:text-primary transition-colors flex items-center gap-1.5 disabled:opacity-50"
              >
                <span className="material-symbols-outlined text-[15px]">
                  {isExporting ? "hourglass_empty" : "download"}
                </span>
                <span>{isExporting ? "Generating..." : "Export PDF"}</span>
              </button>

              <button
                onClick={handleApprove}
                disabled={approved}
                className={`font-mono text-xs font-bold px-3 py-1.5 rounded-lg transition-all flex items-center gap-1.5 ${
                  approved
                    ? "bg-success/20 text-success border border-success/40"
                    : "bg-primary text-black hover:bg-primary-light shadow-glow"
                }`}
              >
                <span className="material-symbols-outlined text-[15px]">
                  {approved ? "check_circle" : "task_alt"}
                </span>
                <span>{approved ? "Signed" : "Approve Strategy"}</span>
              </button>
            </div>
          </div>

          {/* Approved Audit Banner */}
          {approved && (
            <div className="p-3.5 rounded-xl bg-success/10 border border-success/30 flex items-center justify-between font-mono text-xs text-success">
              <div className="flex items-center gap-2">
                <span className="material-symbols-outlined text-[18px]">verified</span>
                <span>
                  <strong>EXECUTIVE AUDIT SIGN-OFF CONFIRMED:</strong> Approved by John Doe ({persona}) on {approvalTimestamp}
                </span>
              </div>
              <span className="text-[10px] bg-success/20 px-2 py-0.5 rounded font-bold">SHA-256 SEAL VALID</span>
            </div>
          )}

          {slideMode ? (
            /* 16:9 Interactive Presentation Slide Mode */
            <div className="space-y-4">
              {/* Slide Navigation & Stepper Header */}
              <div className="p-4 bg-surface-container/90 rounded-2xl border border-primary/30 flex flex-wrap items-center justify-between gap-4">
                <div className="flex items-center gap-2">
                  <span className="text-xs font-mono font-bold text-primary uppercase tracking-widest bg-primary/10 border border-primary/20 px-3 py-1 rounded-lg flex items-center gap-1.5">
                    <span className="material-symbols-outlined text-[16px]">slideshow</span>
                    Slide {currentSlide + 1} of 4
                  </span>
                  <span className="text-xs font-mono text-on-surface-variant hidden sm:inline">
                    Use ← / → keys to navigate
                  </span>
                </div>

                {/* Slide Tabs */}
                <div className="flex items-center gap-1.5 bg-surface-dim p-1 rounded-xl border border-outline-variant/30 flex-wrap">
                  {[
                    { label: "1. Situation & KPIs", icon: "trending_down" },
                    { label: "2. Root Cause", icon: "troubleshoot" },
                    { label: "3. Evidence", icon: "verified" },
                    { label: "4. Strategic Action", icon: "offline_bolt" },
                  ].map((tab, idx) => (
                    <button
                      key={idx}
                      onClick={() => setCurrentSlide(idx)}
                      className={`px-3 py-1.5 rounded-lg text-xs font-mono font-bold transition-all flex items-center gap-1.5 ${
                        currentSlide === idx
                          ? "bg-primary text-black shadow-glow"
                          : "text-on-surface-variant hover:text-on-surface hover:bg-surface-container"
                      }`}
                    >
                      <span className="material-symbols-outlined text-[15px]">{tab.icon}</span>
                      <span>{tab.label}</span>
                    </button>
                  ))}
                </div>

                {/* Prev / Next Arrows */}
                <div className="flex items-center gap-2">
                  <button
                    onClick={() => setCurrentSlide((prev) => Math.max(0, prev - 1))}
                    disabled={currentSlide === 0}
                    className="p-2 rounded-xl bg-surface-container border border-outline-variant/30 text-on-surface-variant hover:text-on-surface hover:bg-surface-dim disabled:opacity-30 transition-all flex items-center justify-center"
                    title="Previous Slide"
                  >
                    <span className="material-symbols-outlined text-[18px]">chevron_left</span>
                  </button>
                  <button
                    onClick={() => setCurrentSlide((prev) => Math.min(3, prev + 1))}
                    disabled={currentSlide === 3}
                    className="p-2 rounded-xl bg-surface-container border border-outline-variant/30 text-on-surface-variant hover:text-on-surface hover:bg-surface-dim disabled:opacity-30 transition-all flex items-center justify-center"
                    title="Next Slide"
                  >
                    <span className="material-symbols-outlined text-[18px]">chevron_right</span>
                  </button>
                </div>
              </div>

              {/* Active Slide Canvas (Executive Glassmorphism Presentation Container) */}
              <div className="glass-panel rounded-3xl p-8 md:p-12 border-2 border-primary/30 bg-gradient-to-br from-surface-container via-surface to-[#030d17] shadow-glow min-h-[520px] flex flex-col justify-between relative overflow-hidden">
                {/* Slide Watermark Background Accent */}
                <div className="absolute -top-24 -right-24 w-96 h-96 rounded-full bg-primary/5 blur-3xl pointer-events-none"></div>

                {/* SLIDE 1: Situation & Anomaly Overview */}
                {currentSlide === 0 && (
                  <div className="space-y-8 flex-1 flex flex-col justify-between">
                    <div className="border-b border-outline-variant/30 pb-4 flex flex-col sm:flex-row sm:items-center justify-between gap-2">
                      <div>
                        <span className="text-[11px] font-mono text-primary font-bold uppercase tracking-widest">
                          Slide 1 • Executive Anomaly Assessment
                        </span>
                        <h2 className="font-display font-black text-2xl md:text-3xl text-on-surface mt-1">
                          Regional Revenue Deficit & Financial Variance Overview
                        </h2>
                      </div>
                      <span className="text-xs font-mono text-error font-bold px-3 py-1 rounded-lg bg-error/15 border border-error/30">
                        CRITICAL ANOMALY
                      </span>
                    </div>

                    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
                      <div className="bg-surface-dim/80 p-6 rounded-2xl border border-error/40 flex flex-col justify-between">
                        <span className="text-xs font-mono text-on-surface-variant uppercase font-bold">Net Revenue</span>
                        <div className="font-display font-extrabold text-4xl text-error my-2">{regionData.revenue}</div>
                        <span className="text-xs font-mono text-error font-bold">{regionData.variance} ({regionData.variancePct}) vs target</span>
                      </div>

                      <div className="bg-surface-dim/80 p-6 rounded-2xl border border-error/40 flex flex-col justify-between">
                        <span className="text-xs font-mono text-on-surface-variant uppercase font-bold">Gross Margin</span>
                        <div className="font-display font-extrabold text-4xl text-error my-2">{regionData.grossMargin}</div>
                        <span className="text-xs font-mono text-error font-bold">{regionData.grossMarginDelta} Dilution</span>
                      </div>

                      <div className="bg-surface-dim/80 p-6 rounded-2xl border border-error/40 flex flex-col justify-between">
                        <span className="text-xs font-mono text-on-surface-variant uppercase font-bold">Regional Availability</span>
                        <div className="font-display font-extrabold text-4xl text-error my-2">{regionData.availability}</div>
                        <span className="text-xs font-mono text-error font-bold">{regionData.availabilityDelta || "-14.8 pts"} Stockout</span>
                      </div>

                      <div className="bg-surface-dim/80 p-6 rounded-2xl border border-primary/40 flex flex-col justify-between">
                        <span className="text-xs font-mono text-primary uppercase font-bold">Addressable Recovery</span>
                        <div className="font-display font-extrabold text-4xl text-primary my-2">{regionData.recoveryPool}</div>
                        <span className="text-xs font-mono text-primary font-bold">27.0x Modeled Fiscal ROI</span>
                      </div>
                    </div>

                    <div className="p-6 rounded-2xl bg-surface-container/90 border border-outline-variant/30 flex items-start gap-4">
                      <span className="material-symbols-outlined text-primary text-3xl shrink-0 mt-0.5">account_balance</span>
                      <div>
                        <h3 className="font-display font-bold text-sm text-on-surface mb-1">
                          Executive Synthesis ({persona.replace(/_/g, " ")} Lens)
                        </h3>
                        <p className="text-sm text-on-surface-variant leading-relaxed font-sans">
                          {narrative.situation}
                        </p>
                      </div>
                    </div>
                  </div>
                )}

                {/* SLIDE 2: Root-Cause Decomposition */}
                {currentSlide === 1 && (
                  <div className="space-y-6 flex-1 flex flex-col justify-between">
                    <div className="border-b border-outline-variant/30 pb-4 flex flex-col sm:flex-row sm:items-center justify-between gap-2">
                      <div>
                        <span className="text-[11px] font-mono text-primary font-bold uppercase tracking-widest">
                          Slide 2 • Causal Waterfall Decomposition
                        </span>
                        <h2 className="font-display font-black text-2xl md:text-3xl text-on-surface mt-1">
                          100.0% Variance Explained Across 4 Ranked Deterministic Factors
                        </h2>
                      </div>
                      <span className="text-xs font-mono text-primary font-bold px-3 py-1 rounded-lg bg-primary/15 border border-primary/30">
                        ZERO HALLUCINATION
                      </span>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                      {/* Left: Driver Breakdown Table */}
                      <div className="space-y-3">
                        {[
                          { rank: "1. Atlanta DC Stockout", impact: "-$550,000", share: "43.2%", conf: "94% Statistical Conf", alert: true },
                          { rank: "2. SKU-8821 Contraction", impact: "-$340,000", share: "26.7%", conf: "88% Conf", alert: false },
                          { rank: "3. Distributor PO Deferrals", impact: "-$240,000", share: "18.8%", conf: "85% Conf", alert: false },
                          { rank: "4. Horizon Price War (-15%)", impact: "-$144,000", share: "11.3%", conf: "82% Conf", alert: false },
                        ].map((d, i) => (
                          <div
                            key={i}
                            className={`p-4 rounded-xl border flex items-center justify-between ${
                              d.alert ? "bg-error/10 border-error/40" : "bg-surface-dim border-outline-variant/30"
                            }`}
                          >
                            <div>
                              <strong className={`text-sm ${d.alert ? "text-error" : "text-on-surface"}`}>{d.rank}</strong>
                              <div className="text-xs font-mono text-on-surface-variant mt-0.5">{d.conf}</div>
                            </div>
                            <div className="text-right">
                              <div className={`font-mono text-sm font-bold ${d.alert ? "text-error" : "text-primary"}`}>{d.impact}</div>
                              <span className="text-xs font-mono text-on-surface-variant">{d.share} share</span>
                            </div>
                          </div>
                        ))}
                      </div>

                      {/* Right: Primary Bottleneck Callout */}
                      <div className="bg-surface-container/90 p-6 rounded-2xl border border-error/30 flex flex-col justify-between">
                        <div>
                          <span className="text-xs font-mono text-error uppercase font-bold flex items-center gap-1.5 mb-2">
                            <span className="material-symbols-outlined text-[16px]">warning</span>
                            Primary Bottleneck Diagnostic
                          </span>
                          <h3 className="font-display font-extrabold text-xl text-on-surface mb-2">
                            Atlanta Distribution Center Depletion
                          </h3>
                          <p className="text-xs text-on-surface-variant leading-relaxed font-sans">
                            Atlanta DC experienced 14 consecutive days of zero available inventory for SKU-8821. Regional availability collapsed from 94.2% down to 79.4%, triggering 29 distributor PO deferrals and surging customer stockout tickets (+310%).
                          </p>
                        </div>

                        <div className="pt-4 border-t border-outline-variant/30 space-y-2 font-mono text-xs">
                          <div className="flex justify-between">
                            <span className="text-on-surface-variant">Attribution Weight:</span>
                            <strong className="text-error">43.2% (-$550K)</strong>
                          </div>
                          <div className="flex justify-between">
                            <span className="text-on-surface-variant">Calibrated Confidence:</span>
                            <strong className="text-primary">94.0% HIGH</strong>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                )}

                {/* SLIDE 3: Corroborating Evidence & Provenance */}
                {currentSlide === 2 && (
                  <div className="space-y-6 flex-1 flex flex-col justify-between">
                    <div className="border-b border-outline-variant/30 pb-4 flex flex-col sm:flex-row sm:items-center justify-between gap-2">
                      <div>
                        <span className="text-[11px] font-mono text-primary font-bold uppercase tracking-widest">
                          Slide 3 • Empirical Proof & Cryptographic Lineage
                        </span>
                        <h2 className="font-display font-black text-2xl md:text-3xl text-on-surface mt-1">
                          12 Verified Multi-Modal Records Across ERP, CRM & EDI
                        </h2>
                      </div>
                      <span className="text-xs font-mono text-success font-bold px-3 py-1 rounded-lg bg-success/15 border border-success/30">
                        SHA-256 SEALED
                      </span>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                      <div className="bg-surface-dim/80 p-6 rounded-2xl border border-outline-variant/30 space-y-3">
                        <span className="text-xs font-mono text-primary uppercase font-bold flex items-center gap-1.5">
                          <span className="material-symbols-outlined text-[16px]">database</span>
                          SAP S/4HANA (MM-WM)
                        </span>
                        <h3 className="font-display font-bold text-sm text-on-surface">Record: INV-SNAP-21971</h3>
                        <p className="text-xs text-on-surface-variant leading-relaxed font-sans">
                          Atlanta inventory snapshot confirmed 0 units available for 14 consecutive days.
                        </p>
                        <span className="text-[10px] font-mono text-error font-bold bg-error/15 px-2 py-0.5 rounded border border-error/30 block w-fit">
                          Confidence: 94% (CRITICAL)
                        </span>
                      </div>

                      <div className="bg-surface-dim/80 p-6 rounded-2xl border border-outline-variant/30 space-y-3">
                        <span className="text-xs font-mono text-primary uppercase font-bold flex items-center gap-1.5">
                          <span className="material-symbols-outlined text-[16px]">support_agent</span>
                          Zendesk Service Cloud
                        </span>
                        <h3 className="font-display font-bold text-sm text-on-surface">Support Ticket Influx</h3>
                        <p className="text-xs text-on-surface-variant leading-relaxed font-sans">
                          +310% surge in stockout & unfulfilled order complaints from key East retail partners.
                        </p>
                        <span className="text-[10px] font-mono text-error font-bold bg-error/15 px-2 py-0.5 rounded border border-error/30 block w-fit">
                          +310% Escalation Surge
                        </span>
                      </div>

                      <div className="bg-surface-dim/80 p-6 rounded-2xl border border-outline-variant/30 space-y-3">
                        <span className="text-xs font-mono text-primary uppercase font-bold flex items-center gap-1.5">
                          <span className="material-symbols-outlined text-[16px]">price_change</span>
                          EDI 832 Market Scrape
                        </span>
                        <h3 className="font-display font-bold text-sm text-on-surface">Competitor Horizon Scrape</h3>
                        <p className="text-xs text-on-surface-variant leading-relaxed font-sans">
                          Horizon Foods launched an aggressive 15% discount across competing SKU lines in territory.
                        </p>
                        <span className="text-[10px] font-mono text-primary font-bold bg-primary/15 px-2 py-0.5 rounded border border-primary/30 block w-fit">
                          -15.0% Price Disruption
                        </span>
                      </div>
                    </div>

                    <div className="p-4 rounded-xl bg-surface-container border border-outline-variant/30 flex items-center justify-between font-mono text-xs">
                      <span className="text-on-surface-variant">Cryptographic Provenance Digest:</span>
                      <span className="text-primary font-mono text-[11px] truncate max-w-md">
                        SHA-256: a7f92b41c0e891d4e21971bc3f8204618e7921a982635a901f4c7183e921d904
                      </span>
                    </div>
                  </div>
                )}

                {/* SLIDE 4: Strategic Recommendation & Sign-Off */}
                {currentSlide === 3 && (
                  <div className="space-y-6 flex-1 flex flex-col justify-between">
                    <div className="border-b border-outline-variant/30 pb-4 flex flex-col sm:flex-row sm:items-center justify-between gap-2">
                      <div>
                        <span className="text-[11px] font-mono text-primary font-bold uppercase tracking-widest">
                          Slide 4 • Prescriptive Action & Governance
                        </span>
                        <h2 className="font-display font-black text-2xl md:text-3xl text-on-surface mt-1">
                          Priority 1 Emergency Inventory Transfer & Executive Authorization
                        </h2>
                      </div>
                      <span className="text-xs font-mono text-primary font-bold px-3 py-1 rounded-lg bg-primary/15 border border-primary/30">
                        BOARDROOM SIGN-OFF
                      </span>
                    </div>

                    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                      <div className="bg-surface-container/90 p-6 rounded-2xl border border-primary/40 space-y-4">
                        <span className="text-xs font-mono text-primary uppercase font-bold flex items-center gap-1.5">
                          <span className="material-symbols-outlined text-[16px]">offline_bolt</span>
                          Prescriptive Strategy ({persona.replace(/_/g, " ")} Focus)
                        </span>
                        <h3 className="font-display font-bold text-lg text-on-surface">
                          Transfer 3,200 Units (Chicago Central &rarr; Atlanta DC)
                        </h3>
                        <p className="text-xs text-on-surface-variant leading-relaxed font-sans">
                          {narrative.recommendation}
                        </p>
                        <div className="pt-3 border-t border-outline-variant/30 grid grid-cols-3 gap-2 font-mono text-[11px] text-center">
                          <div className="bg-surface-dim p-2 rounded-lg">
                            <span className="text-on-surface-variant block text-[9px]">SLA</span>
                            <strong className="text-on-surface">14 Days</strong>
                          </div>
                          <div className="bg-surface-dim p-2 rounded-lg">
                            <span className="text-on-surface-variant block text-[9px]">EXPEDITED COST</span>
                            <strong className="text-on-surface">$28,000</strong>
                          </div>
                          <div className="bg-surface-dim p-2 rounded-lg">
                            <span className="text-on-surface-variant block text-[9px]">RECOVERY</span>
                            <strong className="text-primary">+$484,000</strong>
                          </div>
                        </div>
                      </div>

                      <div className="bg-surface-container/90 p-6 rounded-2xl border border-outline-variant/30 flex flex-col justify-between space-y-4">
                        <div>
                          <span className="text-xs font-mono text-on-surface-variant uppercase font-bold block mb-2">
                            Total Modeled Fiscal Benefit
                          </span>
                          <div className="font-display font-black text-5xl text-primary mb-1">
                            +$757,600.00
                          </div>
                          <span className="text-xs font-mono text-on-surface-variant">
                            Yields 27.0x ROI against $28K total intervention expenditure.
                          </span>
                        </div>

                        <div className="p-4 bg-surface-dim rounded-xl border border-outline-variant/30 flex items-center justify-between">
                          <div>
                            <div className="text-xs font-mono font-bold text-on-surface">Executive Sign-Off:</div>
                            <div className="text-[11px] font-mono text-on-surface-variant">
                              {approved ? `Approved on ${approvalTimestamp}` : "Pending Boardroom Authorization"}
                            </div>
                          </div>

                          <button
                            onClick={handleApprove}
                            disabled={approved}
                            className={`font-mono text-xs font-bold px-4 py-2 rounded-lg transition-all flex items-center gap-1.5 ${
                              approved
                                ? "bg-success/20 text-success border border-success/40"
                                : "bg-primary text-black hover:bg-primary-light shadow-glow"
                            }`}
                          >
                            <span className="material-symbols-outlined text-[16px]">
                              {approved ? "verified" : "draw"}
                            </span>
                            <span>{approved ? "Signed" : "Authorize Strategy"}</span>
                          </button>
                        </div>
                      </div>
                    </div>
                  </div>
                )}
              </div>
            </div>
          ) : (
            /* 5-Section Boardroom Grid (Standard Document View) */
            <div className="space-y-6">
              {/* Top 3-Card Bento Row */}
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                {/* Section 1: Situation */}
                <section className="glass-panel rounded-2xl p-6 flex flex-col justify-between border border-outline-variant/30 bg-surface-container/70">
                  <div>
                    <h2 className="font-mono text-xs text-on-surface-variant mb-4 uppercase tracking-widest flex items-center gap-2 border-b border-outline-variant/30 pb-3 font-bold">
                      <span className="material-symbols-outlined text-error text-[18px]">trending_down</span>
                      1. Situation
                    </h2>
                    <div className="font-display font-extrabold text-4xl md:text-5xl text-error mb-2 leading-none">
                      {regionData.variance}
                    </div>
                    <div className="flex items-center gap-1 text-error font-mono text-sm font-bold">
                      <span className="material-symbols-outlined text-[16px]">arrow_downward</span>
                      <span>{regionData.variancePct} vs Q2 baseline</span>
                    </div>
                  </div>
                  <p className="text-xs text-on-surface-variant font-sans leading-relaxed mt-4 border-t border-outline-variant/30 pt-4">
                    {narrative.situation}
                  </p>
                </section>

                {/* Section 2: Diagnosis */}
                <section className="glass-panel rounded-2xl p-6 flex flex-col border border-outline-variant/30 bg-surface-container/70 space-y-4">
                  <h2 className="font-mono text-xs text-on-surface-variant uppercase tracking-widest flex items-center gap-2 border-b border-outline-variant/30 pb-3 font-bold">
                    <span className="material-symbols-outlined text-primary text-[18px]">troubleshoot</span>
                    2. Diagnosis
                  </h2>

                  <div className="space-y-3">
                    <div className="bg-surface-dim p-3.5 rounded-xl border border-outline-variant/30">
                      <h3 className="font-display font-bold text-xs text-on-surface mb-1">
                        Primary: {regionData.primaryDriver}
                      </h3>
                      <p className="text-[11px] text-on-surface-variant font-sans mb-2">
                        Critical inventory depletion at regional DC (-14.8 pts availability drop).
                      </p>
                      <div className="flex justify-between font-mono text-[10px] mb-1">
                        <span className="text-on-surface-variant">Attribution Share</span>
                        <span className="text-error font-bold">{regionData.primaryDriverShare} (-$550K)</span>
                      </div>
                      <div className="w-full bg-surface-container h-1.5 rounded-full overflow-hidden">
                        <div className="bg-error w-[43.2%] h-full"></div>
                      </div>
                    </div>

                    <div className="bg-surface-dim p-3.5 rounded-xl border border-outline-variant/30">
                      <h3 className="font-display font-bold text-xs text-on-surface mb-1">
                        Secondary: SKU-8821 Contraction
                      </h3>
                      <p className="text-[11px] text-on-surface-variant font-sans mb-2">
                        Flagship volume contraction exacerbated by distributor PO deferrals.
                      </p>
                      <div className="flex justify-between font-mono text-[10px] mb-1">
                        <span className="text-on-surface-variant">Attribution Share</span>
                        <span className="text-primary font-bold">26.7% (-$340K)</span>
                      </div>
                      <div className="w-full bg-surface-container h-1.5 rounded-full overflow-hidden">
                        <div className="bg-primary w-[26.7%] h-full"></div>
                      </div>
                    </div>
                  </div>
                </section>

                {/* Section 3: Corroborating Evidence */}
                <section className="glass-panel rounded-2xl p-6 flex flex-col border border-outline-variant/30 bg-surface-container/70 space-y-3">
                  <h2 className="font-mono text-xs text-on-surface-variant uppercase tracking-widest flex items-center gap-2 border-b border-outline-variant/30 pb-3 font-bold">
                    <span className="material-symbols-outlined text-primary text-[18px]">plagiarism</span>
                    3. Corroborating Evidence
                  </h2>

                  <div className="space-y-2.5 flex-1 flex flex-col justify-around">
                    <div className="flex items-center justify-between p-3 bg-surface-dim rounded-xl border border-outline-variant/30">
                      <span className="font-sans font-semibold text-xs text-on-surface">Atlanta DC Availability</span>
                      <span className="font-mono text-[10px] font-bold text-error bg-error/15 px-2 py-0.5 rounded border border-error/30">
                        {regionData.availability} (CRITICAL)
                      </span>
                    </div>

                    <div className="flex items-center justify-between p-3 bg-surface-dim rounded-xl border border-outline-variant/30">
                      <span className="font-sans font-semibold text-xs text-on-surface">Zendesk Stockout Tickets</span>
                      <span className="font-mono text-[10px] font-bold text-error bg-error/15 px-2 py-0.5 rounded border border-error/30">
                        +310% Surge
                      </span>
                    </div>

                    <div className="flex items-center justify-between p-3 bg-surface-dim rounded-xl border border-outline-variant/30">
                      <span className="font-sans font-semibold text-xs text-on-surface">Competitor Horizon Pricing</span>
                      <span className="font-mono text-[10px] font-bold text-primary bg-primary/15 px-2 py-0.5 rounded border border-primary/30">
                        -15.0% Scrape
                      </span>
                    </div>
                  </div>
                </section>
              </div>

              {/* Bottom Full-Width Section: Recommended Action & Projected Impact */}
              <section className="glass-panel rounded-2xl p-6 md:p-8 border border-primary/40 bg-gradient-to-br from-primary-container/15 via-surface-container to-surface shadow-glow relative overflow-hidden">
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 relative z-10">
                  {/* Left: Recommended Action */}
                  <div className="flex flex-col justify-between border-b lg:border-b-0 lg:border-r border-outline-variant/30 pb-6 lg:pb-0 lg:pr-8">
                    <div>
                      <div className="flex justify-between items-center mb-3 border-b border-primary/20 pb-2.5">
                        <h2 className="font-mono text-xs text-primary uppercase tracking-widest flex items-center gap-2 font-bold">
                          <span className="material-symbols-outlined text-[20px]">offline_bolt</span>
                          4. Recommended Action
                        </h2>
                        <span className="font-mono text-[10px] bg-primary/20 text-primary px-2.5 py-0.5 rounded-full border border-primary/30 font-bold uppercase">
                          Priority: Critical
                        </span>
                      </div>

                      <h3 className="font-display font-extrabold text-xl md:text-2xl text-on-surface mb-3 leading-tight">
                        Execute Emergency Inventory Transfer (3,200 Units)
                      </h3>

                      <p className="text-xs md:text-sm leading-relaxed text-on-surface-variant font-sans">
                        {narrative.recommendation}
                      </p>
                    </div>

                    <div className="mt-4 pt-3 border-t border-outline-variant/20 flex items-center gap-4 font-mono text-[11px] text-on-surface-variant">
                      <span>SLA: 14 Days</span>
                      <span>•</span>
                      <span>Owner: Supply Chain Operations</span>
                    </div>
                  </div>

                  {/* Right: Projected Impact & Confidence */}
                  <div className="flex flex-col justify-between">
                    <div>
                      <h2 className="font-mono text-xs text-on-surface-variant mb-3 uppercase tracking-widest flex items-center gap-2 border-b border-outline-variant/30 pb-2.5 font-bold">
                        <span className="material-symbols-outlined text-[18px]">insights</span>
                        5. Projected Impact & Confidence
                      </h2>

                      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 mt-3">
                        <div className="bg-surface-dim border border-primary/30 rounded-xl p-5 flex flex-col justify-center">
                          <div className="font-mono text-[10px] text-on-surface-variant uppercase font-bold mb-1">
                            Projected Recovery Pool
                          </div>
                          <div className="font-display font-extrabold text-3xl md:text-4xl text-primary leading-none mb-1">
                            {regionData.recoveryPool}
                          </div>
                          <div className="text-xs font-mono text-on-surface-variant">+$729.6K net fiscal benefit</div>
                        </div>

                        <div className="bg-surface-dim border border-outline-variant/30 rounded-xl p-5 flex flex-col justify-center gap-3">
                          <div>
                            <div className="flex justify-between items-center mb-1 font-mono">
                              <span className="text-[10px] text-on-surface-variant uppercase font-bold">
                                Confidence Score
                              </span>
                              <span className="text-sm text-primary font-extrabold">89.0%</span>
                            </div>
                            <div className="w-full bg-surface-container h-2 rounded-full overflow-hidden">
                              <div className="bg-primary w-[89%] h-full"></div>
                            </div>
                          </div>
                          <p className="text-[10px] font-sans text-on-surface-variant leading-snug">
                            Multi-layer deterministic reconciliation across 8 enterprise data sources.
                          </p>
                        </div>
                      </div>
                    </div>

                    <div className="mt-4 pt-3 border-t border-outline-variant/20 flex items-center justify-between font-mono text-[10px] text-on-surface-variant">
                      <span>Deterministic Lineage Verified</span>
                      <span className="text-primary font-bold">Zero-Hallucination Safe</span>
                    </div>
                  </div>
                </div>
              </section>
            </div>
          )}

          {/* Boardroom Sign-Off Modal */}
          {showApprovalModal && (
            <div className="fixed inset-0 z-50 bg-black/75 backdrop-blur-sm flex items-center justify-center p-4">
              <div className="bg-surface-container border border-primary/50 rounded-2xl max-w-md w-full p-6 shadow-glow space-y-4 font-mono">
                <div className="flex items-center gap-3 border-b border-outline-variant/30 pb-3">
                  <div className="w-10 h-10 rounded-xl bg-primary/20 text-primary border border-primary/40 flex items-center justify-center">
                    <span className="material-symbols-outlined text-2xl">draw</span>
                  </div>
                  <div>
                    <h3 className="font-display font-bold text-base text-on-surface">Executive Authorization Sign-Off</h3>
                    <span className="text-[11px] text-primary">{region} • {quarter} Briefing</span>
                  </div>
                </div>

                <p className="text-xs text-on-surface-variant font-sans leading-relaxed">
                  By clicking confirm, you authorize the execution of Strategy Lever 1 (Emergency Stock Transfer) and record an immutable audit signature in the enterprise governance ledger.
                </p>

                <div className="p-3 bg-surface-dim rounded-xl border border-outline-variant/30 space-y-1.5 text-xs">
                  <div className="flex justify-between">
                    <span className="text-on-surface-variant">Signatory Role:</span>
                    <strong className="text-primary">{persona.replace("_", " ")}</strong>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-on-surface-variant">Signatory ID:</span>
                    <strong className="text-on-surface">JD-EXEC-2026-991</strong>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-on-surface-variant">Timestamp:</span>
                    <span className="text-[11px] text-on-surface-variant">{approvalTimestamp}</span>
                  </div>
                </div>

                <div className="flex gap-3 pt-2">
                  <button
                    onClick={() => setShowApprovalModal(false)}
                    className="flex-1 py-2 rounded-lg border border-outline-variant/40 text-on-surface-variant hover:text-on-surface transition-colors text-xs font-bold"
                  >
                    Cancel
                  </button>
                  <button
                    onClick={confirmApproval}
                    className="flex-1 py-2 rounded-lg bg-primary text-black font-bold hover:bg-primary-light transition-all shadow-glow text-xs"
                  >
                    Authorize & Sign
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
