"use client";

import React from "react";
import { Sparkles, ArrowRight, ShieldAlert, Cpu } from "lucide-react";
import Link from "next/link";
import { Badge } from "@/components/ui/Badge";
import { AIExplanationResponse } from "@/lib/types";



interface AISummaryBannerProps {
  aiData: AIExplanationResponse | null;
  loading: boolean;
}

export function AISummaryBanner({ aiData, loading }: AISummaryBannerProps) {
  if (loading) {
    return (
      <div className="glass-panel rounded-xl p-5 border-primary/30 relative overflow-hidden animate-pulse">
        <div className="flex items-center gap-3 mb-2">
          <div className="w-6 h-6 rounded-full bg-primary/20"></div>
          <div className="h-4 w-48 bg-primary/20 rounded"></div>
        </div>
        <div className="h-4 w-full bg-surface-container rounded mb-2"></div>
        <div className="h-4 w-3/4 bg-surface-container rounded"></div>
      </div>
    );
  }

  const isAbstained = aiData?.explanation?.abstained;
  const summaryText =
    aiData?.explanation?.summary ||
    "Revenue contraction of -$1.23M (-7.97%) in North America East is driven by a multi-factor operational bottleneck. Atlanta DC stockouts (43.2% contribution) and SKU-8821 volume decline represent the primary causal factors.";
  const persona = aiData?.persona || "CFO";
  const confidence = aiData?.explanation?.reasoning?.[0]?.confidence || 89;

  return (
    <div className="glass-panel rounded-xl p-5 border-primary/30 relative overflow-hidden bg-gradient-to-r from-primary-container/20 via-surface-container to-surface">
      <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-4">
        <div className="flex items-start gap-3.5 flex-1">
          <div className="w-9 h-9 rounded-lg bg-primary/20 border border-primary/40 flex items-center justify-center text-primary shrink-0 shadow-glow mt-0.5">
            <Sparkles className="w-5 h-5" />
          </div>
          <div>
            <div className="flex items-center gap-3 mb-1.5">
              <span className="font-mono text-xs font-bold text-primary uppercase tracking-wider flex items-center gap-1.5">
                Grounded AI Executive Synthesis
              </span>
              <span className="text-[10px] font-mono bg-primary/10 border border-primary/30 text-primary px-2 py-0.5 rounded-full uppercase">
                {persona} Mode
              </span>
              <span className="text-[10px] font-mono bg-surface-dim border border-outline-variant text-on-surface-variant px-2 py-0.5 rounded-full">
                Confidence: <strong className="text-on-surface">{confidence}%</strong>
              </span>
              {isAbstained && (
                <span className="text-[10px] font-mono bg-warning/20 text-warning border border-warning/40 px-2 py-0.5 rounded-full uppercase font-bold">
                  ABSTAINED (Low Confidence)
                </span>
              )}
            </div>
            <p className="text-xs text-on-surface/90 leading-relaxed font-body">
              {summaryText}
            </p>
          </div>
        </div>

        {/* CTA to Investigation */}
        <div className="flex items-center gap-3 shrink-0">
          <Link
            href="/investigation"
            className="px-4 py-2 bg-primary text-background font-mono text-xs font-bold rounded-lg hover:bg-primary-dark transition-all flex items-center gap-2 shadow-glow active:scale-[0.98]"
          >
            <span>Investigate Root Cause</span>
            <ArrowRight className="w-4 h-4" />
          </Link>
        </div>
      </div>
    </div>
  );
}
