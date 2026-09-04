"use client";

import React from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { cn } from "@/lib/utils";

const NAV_ITEMS = [
  {
    name: "Executive Command Center",
    href: "/",
    icon: "dashboard",
    badge: "Live",
  },
  {
    name: "Insights (Root Cause)",
    href: "/root-cause",
    icon: "analytics",
    badge: "4 Drivers",
  },
  {
    name: "Decision Graph",
    href: "/decision-graph",
    icon: "account_tree",
    badge: "6 Stages",
  },
  {
    name: "AI Investigation Trace",
    href: "/investigation",
    icon: "psychology",
    badge: "11 Nodes",
  },
  {
    name: "Evidence Explorer",
    href: "/evidence",
    icon: "folder_special",
    badge: "SHA-256",
  },
  {
    name: "Recommendations & What-If",
    href: "/recommendations",
    icon: "science",
    badge: "+$484K",
  },
  {
    name: "Executive Briefings",
    href: "/briefing",
    icon: "description",
    badge: "Boardroom",
  },
];

export function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="w-[285px] lg:w-[290px] bg-[#051424] border-r border-outline-variant/30 flex flex-col shrink-0 min-h-screen select-none z-40 shadow-2xl">
      {/* Brand Header */}
      <div className="px-5 py-6 border-b border-outline-variant/20 bg-surface-container/40">
        <div className="flex items-center gap-3">
          <div className="w-9 h-9 rounded-xl bg-primary/15 border border-primary/40 flex items-center justify-center text-primary shadow-glow">
            <span className="material-symbols-outlined text-[22px]">shield_with_heart</span>
          </div>
          <div>
            <h1 className="font-display font-extrabold text-lg text-primary tracking-tight leading-none">
              InsightPilot AI
            </h1>
            <p className="font-mono text-[10px] text-on-surface-variant uppercase tracking-widest mt-1">
              Global Enterprise
            </p>
          </div>
        </div>
      </div>

      {/* Navigation List */}
      <div className="flex-1 py-6 px-3 space-y-1.5 overflow-y-auto">
        <div className="px-3 pb-2 text-[10px] font-mono uppercase tracking-widest text-on-surface-variant/70 font-bold">
          Decision Lifecycle
        </div>

        {NAV_ITEMS.map((item) => {
          const isActive = pathname === item.href;

          return (
            <Link
              key={item.href}
              href={item.href}
              className={cn(
                "flex items-center justify-between px-3 py-2.5 rounded-xl text-xs transition-all duration-200 group relative",
                isActive
                  ? "bg-primary/15 text-primary border border-primary/40 font-bold shadow-sm"
                  : "text-on-surface-variant hover:text-on-surface hover:bg-surface-container/60"
              )}
            >
              <div className="flex items-center gap-2.5 min-w-0">
                <span
                  className={cn(
                    "material-symbols-outlined text-[19px] transition-colors shrink-0",
                    isActive ? "text-primary" : "text-on-surface-variant group-hover:text-primary"
                  )}
                >
                  {item.icon}
                </span>
                <span className="font-sans text-xs font-semibold tracking-tight whitespace-nowrap">
                  {item.name}
                </span>
              </div>

              {item.badge && (
                <span
                  className={cn(
                    "text-[9px] font-mono font-bold px-1.5 py-0.5 rounded border shrink-0 transition-colors ml-2",
                    isActive
                  ? "bg-primary/25 text-primary border-primary/40 shadow-sm"
                  : "bg-surface-dim/80 text-on-surface-variant/70 border-outline-variant/40 group-hover:text-on-surface"
                  )}
                >
                  {item.badge}
                </span>
              )}
            </Link>
          );
        })}
      </div>

      {/* Generate Briefing CTA Button & Live Health Footer */}
      <div className="p-4 border-t border-outline-variant/20 bg-surface-container/30 space-y-3">
        <Link
          href="/briefing"
          className="w-full bg-primary text-black font-mono text-xs font-bold py-2.5 px-4 rounded-xl hover:bg-primary-light transition-all duration-200 flex items-center justify-center gap-2 shadow-glow text-center"
        >
          <span className="material-symbols-outlined text-[16px]">description</span>
          <span>Generate Briefing</span>
        </Link>

        {/* System Status Footer */}
        <div className="flex items-center justify-between text-[10px] font-mono px-1">
          <div className="flex items-center gap-1.5 text-primary">
            <span className="w-2 h-2 rounded-full bg-primary animate-pulse"></span>
            <span className="font-bold tracking-tight">PIPELINE ONLINE</span>
          </div>
          <span className="text-on-surface-variant/70 font-semibold">94.0% Grounded</span>
        </div>
      </div>
    </aside>
  );
}
