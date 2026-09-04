"use client";

import React from "react";
import { Globe, ArrowRight } from "lucide-react";
import Link from "next/link";

export function RegionalHealthTable() {
  const regions = [
    {
      region: "North America East",
      code: "NA-East",
      revenue: "$14.20M",
      variance: "-7.97%",
      margin: "57.4%",
      avail: "79.4%",
      status: "CRITICAL",
      statusColor: "text-error bg-error-container/20 border-error/30",
    },
    {
      region: "North America West",
      code: "NA-West",
      revenue: "$16.85M",
      variance: "+2.10%",
      margin: "61.2%",
      avail: "93.8%",
      status: "HEALTHY",
      statusColor: "text-success bg-success-container/20 border-success/30",
    },
    {
      region: "North America Central",
      code: "NA-Central",
      revenue: "$11.40M",
      variance: "+0.45%",
      margin: "59.0%",
      avail: "91.1%",
      status: "HEALTHY",
      statusColor: "text-success bg-success-container/20 border-success/30",
    },
    {
      region: "Europe & UK",
      code: "EU-West",
      revenue: "$18.20M",
      variance: "-1.20%",
      margin: "58.1%",
      avail: "88.6%",
      status: "WATCH",
      statusColor: "text-warning bg-warning-container/20 border-warning/30",
    },
  ];

  return (
    <div className="glass-panel rounded-xl p-5">
      <div className="flex items-center justify-between pb-3 border-b border-outline-variant mb-4">
        <div className="flex items-center gap-2">
          <Globe className="w-4 h-4 text-primary" />
          <h3 className="font-display font-semibold text-sm text-on-surface">
            Regional Portfolio Breakdown
          </h3>
        </div>
        <span className="text-[10px] font-mono text-on-surface-variant">
          Fiscal 2026-Q3
        </span>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full text-left text-xs font-mono">
          <thead>
            <tr className="border-b border-outline-variant text-on-surface-variant/70 text-[10px] uppercase">
              <th className="pb-2 font-medium">Territory</th>
              <th className="pb-2 font-medium">Revenue</th>
              <th className="pb-2 font-medium">Variance</th>
              <th className="pb-2 font-medium">Margin</th>
              <th className="pb-2 font-medium">Availability</th>
              <th className="pb-2 font-medium text-right">Status</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-outline-variant/30">
            {regions.map((r) => (
              <tr
                key={r.code}
                className={
                  r.status === "CRITICAL"
                    ? "bg-primary-container/10 hover:bg-primary-container/20 transition-colors"
                    : "hover:bg-surface-bright/20 transition-colors"
                }
              >
                <td className="py-2.5 font-bold text-on-surface flex items-center gap-2">
                  {r.region}
                  {r.status === "CRITICAL" && (
                    <span className="w-1.5 h-1.5 rounded-full bg-error animate-ping"></span>
                  )}
                </td>
                <td className="py-2.5 text-on-surface">{r.revenue}</td>
                <td
                  className={`py-2.5 font-bold ${
                    r.variance.startsWith("-") ? "text-error" : "text-success"
                  }`}
                >
                  {r.variance}
                </td>
                <td className="py-2.5 text-on-surface">{r.margin}</td>
                <td className="py-2.5 text-on-surface">{r.avail}</td>
                <td className="py-2.5 text-right">
                  <span
                    className={`inline-block px-2 py-0.5 rounded text-[10px] uppercase font-bold border ${r.statusColor}`}
                  >
                    {r.status}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
