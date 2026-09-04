"use client";

import React from "react";
import { AlertOctagon, AlertTriangle, Info, ArrowRight, ShieldCheck } from "lucide-react";
import Link from "next/link";

interface AlertFeedProps {
  onInvestigate?: () => void;
}

export function AlertFeed({ onInvestigate }: AlertFeedProps) {
  const alerts = [
    {
      id: "ALT-001",
      severity: "CRITICAL",
      title: "North America East Revenue Shortfall",
      desc: "Revenue fell -$1.23M (-7.97%) below Q2 baseline driven by multi-tier supply chain constraint.",
      metric: "-$1.23M",
      action: "Investigate Drivers",
      href: "/root-cause",
      icon: AlertOctagon,
      color: "text-error border-error/30 bg-error-container/20",
    },
    {
      id: "ALT-002",
      severity: "HIGH",
      title: "Atlanta DC Inventory Availability Depleted",
      desc: "Stockouts in high-velocity SKUs dropped regional availability from 94.2% to 79.4% (-14.8 pts).",
      metric: "79.4% Avail.",
      action: "View ERP Evidence",
      href: "/evidence?q=EVID_ERP_ATL_STOCKOUT_001",
      icon: AlertTriangle,
      color: "text-warning border-warning/30 bg-warning-container/20",
    },
    {
      id: "ALT-003",
      severity: "MEDIUM",
      title: "Distributor Purchase Order Deferrals",
      desc: "29 delayed PO memos recorded across Key East Tier-1 distributors due to backorder wait times.",
      metric: "29 POs",
      action: "Review Levers",
      href: "/recommendations",
      icon: Info,
      color: "text-secondary border-secondary/30 bg-secondary-container/20",
    },
  ];

  return (
    <div className="glass-panel rounded-xl p-5 flex flex-col justify-between">
      <div>
        <div className="flex items-center justify-between pb-3 border-b border-outline-variant mb-4">
          <div className="flex items-center gap-2">
            <ShieldCheck className="w-4 h-4 text-primary" />
            <h3 className="font-display font-semibold text-sm text-on-surface">
              Autonomous Detection Feed
            </h3>
          </div>
          <span className="text-[10px] font-mono bg-primary/10 border border-primary/30 text-primary px-2 py-0.5 rounded-full">
            3 Active Signals
          </span>
        </div>

        <div className="space-y-3">
          {alerts.map((alt) => {
            const Icon = alt.icon;
            return (
              <div
                key={alt.id}
                className="p-3 rounded-lg bg-surface-dim border border-outline-variant hover:border-primary/40 transition-colors"
              >
                <div className="flex items-start justify-between gap-2 mb-1.5">
                  <div className="flex items-center gap-2">
                    <span
                      className={`text-[10px] font-mono font-bold uppercase px-2 py-0.5 rounded border ${alt.color}`}
                    >
                      {alt.severity}
                    </span>
                    <span className="text-xs font-semibold text-on-surface tracking-tight">
                      {alt.title}
                    </span>
                  </div>
                  <span className="text-xs font-mono font-bold text-error">
                    {alt.metric}
                  </span>
                </div>
                <p className="text-xs text-on-surface-variant leading-relaxed mb-3">
                  {alt.desc}
                </p>
                <div className="flex justify-end">
                  <Link
                    href={alt.href}
                    className="text-[11px] font-mono font-semibold text-primary hover:text-primary-dark flex items-center gap-1 transition-colors"
                  >
                    <span>{alt.action}</span>
                    <ArrowRight className="w-3 h-3" />
                  </Link>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}
