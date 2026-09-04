"use client";

import React, { createContext, useContext, useState, useEffect } from "react";
import { PersonaType } from "@/lib/types";

export type RegionType = "NA-East" | "Global" | "EMEA" | "APAC";
export type QuarterType = "2026-Q3" | "2026-Q2" | "2026-Q1";

export interface RegionData {
  revenue: string;
  revenueRaw: number;
  variance: string;
  varianceRaw: number;
  variancePct: string;
  grossMargin: string;
  grossMarginDelta: string;
  unitsSold: string;
  unitsSoldDelta: string;
  availability: string;
  availabilityDelta: string;
  orders: string;
  ordersDelta: string;
  primaryDriver: string;
  primaryDriverShare: string;
  recoveryPool: string;
  recoveryRaw: number;
}

const REGION_DATA_MAP: Record<RegionType, RegionData> = {
  "NA-East": {
    revenue: "$14.20M",
    revenueRaw: 14200000.05,
    variance: "-$1.23M",
    varianceRaw: -1230000.01,
    variancePct: "-7.97%",
    grossMargin: "57.4%",
    grossMarginDelta: "-3.2 pts",
    unitsSold: "105,400",
    unitsSoldDelta: "-8.5%",
    availability: "79.4%",
    availabilityDelta: "-14.8 pts",
    orders: "842",
    ordersDelta: "-12.1%",
    primaryDriver: "Atlanta DC Stockout",
    primaryDriverShare: "43.2%",
    recoveryPool: "+$757.6K",
    recoveryRaw: 757600,
  },
  Global: {
    revenue: "$68.45M",
    revenueRaw: 68450000,
    variance: "-$2.15M",
    varianceRaw: -2150000,
    variancePct: "-3.04%",
    grossMargin: "59.1%",
    grossMarginDelta: "-1.4 pts",
    unitsSold: "482,000",
    unitsSoldDelta: "-4.2%",
    availability: "86.2%",
    availabilityDelta: "-6.5 pts",
    orders: "3,890",
    ordersDelta: "-5.1%",
    primaryDriver: "North America Regional Disruption",
    primaryDriverShare: "58.0%",
    recoveryPool: "+$1.42M",
    recoveryRaw: 1420000,
  },
  EMEA: {
    revenue: "$24.10M",
    revenueRaw: 24100000,
    variance: "-$0.42M",
    varianceRaw: -420000,
    variancePct: "-1.71%",
    grossMargin: "61.3%",
    grossMarginDelta: "-0.8 pts",
    unitsSold: "168,000",
    unitsSoldDelta: "-2.1%",
    availability: "92.4%",
    availabilityDelta: "-2.2 pts",
    orders: "1,420",
    ordersDelta: "-1.8%",
    primaryDriver: "Rotterdam Port Lead-Time Delay",
    primaryDriverShare: "38.5%",
    recoveryPool: "+$310.0K",
    recoveryRaw: 310000,
  },
  APAC: {
    revenue: "$18.60M",
    revenueRaw: 18600000,
    variance: "+$0.18M",
    varianceRaw: 180000,
    variancePct: "+0.98%",
    grossMargin: "56.8%",
    grossMarginDelta: "+0.4 pts",
    unitsSold: "142,000",
    unitsSoldDelta: "+1.5%",
    availability: "94.8%",
    availabilityDelta: "+0.5 pts",
    orders: "1,180",
    ordersDelta: "+2.4%",
    primaryDriver: "Singapore Cross-Dock Optimization",
    primaryDriverShare: "41.0%",
    recoveryPool: "+$85.0K",
    recoveryRaw: 85000,
  },
};

interface AppContextType {
  persona: PersonaType;
  setPersona: (p: PersonaType) => void;
  region: RegionType;
  setRegion: (r: RegionType) => void;
  quarter: QuarterType;
  setQuarter: (q: QuarterType) => void;
  regionData: RegionData;
  selectedDriverId: string;
  setSelectedDriverId: (id: string) => void;
  activeCausalFilter: string;
  setActiveCausalFilter: (f: string) => void;
  isInvestigationRunning: boolean;
  activeInvestigationStep: number;
  triggerLiveInvestigation: () => void;
  dispatchedActions: Record<string, boolean>;
  dispatchAction: (actionId: string) => void;
  isVerifiedHashModalOpen: boolean;
  activeVerifyingEvidenceId: string | null;
  openHashVerifier: (evidenceId: string) => void;
  closeHashVerifier: () => void;
}

const AppContext = createContext<AppContextType | undefined>(undefined);

export function AppProvider({ children }: { children: React.ReactNode }) {
  const [persona, setPersona] = useState<PersonaType>("CFO");
  const [region, setRegion] = useState<RegionType>("NA-East");
  const [quarter, setQuarter] = useState<QuarterType>("2026-Q3");
  const [selectedDriverId, setSelectedDriverId] = useState<string>("atlanta_dc_stockout");
  const [activeCausalFilter, setActiveCausalFilter] = useState<string>("ALL");
  const [isInvestigationRunning, setIsInvestigationRunning] = useState<boolean>(false);
  const [activeInvestigationStep, setActiveInvestigationStep] = useState<number>(5);
  const [dispatchedActions, setDispatchedActions] = useState<Record<string, boolean>>({});
  const [isVerifiedHashModalOpen, setIsVerifiedHashModalOpen] = useState<boolean>(false);
  const [activeVerifyingEvidenceId, setActiveVerifyingEvidenceId] = useState<string | null>(null);

  const regionData = REGION_DATA_MAP[region] || REGION_DATA_MAP["NA-East"];

  const triggerLiveInvestigation = () => {
    if (isInvestigationRunning) return;
    setIsInvestigationRunning(true);
    setActiveInvestigationStep(1);

    const stepInterval = setInterval(() => {
      setActiveInvestigationStep((prev) => {
        if (prev >= 5) {
          clearInterval(stepInterval);
          setIsInvestigationRunning(false);
          return 5;
        }
        return prev + 1;
      });
    }, 900);
  };

  const dispatchAction = (actionId: string) => {
    setDispatchedActions((prev) => ({ ...prev, [actionId]: true }));
  };

  const openHashVerifier = (evidenceId: string) => {
    setActiveVerifyingEvidenceId(evidenceId);
    setIsVerifiedHashModalOpen(true);
  };

  const closeHashVerifier = () => {
    setIsVerifiedHashModalOpen(false);
    setActiveVerifyingEvidenceId(null);
  };

  return (
    <AppContext.Provider
      value={{
        persona,
        setPersona,
        region,
        setRegion,
        quarter,
        setQuarter,
        regionData,
        selectedDriverId,
        setSelectedDriverId,
        activeCausalFilter,
        setActiveCausalFilter,
        isInvestigationRunning,
        activeInvestigationStep,
        triggerLiveInvestigation,
        dispatchedActions,
        dispatchAction,
        isVerifiedHashModalOpen,
        activeVerifyingEvidenceId,
        openHashVerifier,
        closeHashVerifier,
      }}
    >
      {children}
    </AppContext.Provider>
  );
}

export function useApp() {
  const context = useContext(AppContext);
  if (!context) {
    throw new Error("useApp must be used within an AppProvider");
  }
  return context;
}
