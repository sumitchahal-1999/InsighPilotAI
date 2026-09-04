# InsightPilot AI — Frontend Production Smoke Test Report

**Project:** InsightPilot AI  
**Competition:** Accenture Innovation Challenge 2026 (Track 3: BusinessIntelligence.ai)  
**Document:** Next.js Static Build Audit, 7 Core Routes Verification & Bundle Inspection  
**Status:** `FRONTEND PRODUCTION SMOKE TEST PASSED (10/10 STATIC PAGES)`

---

## 1. Production Build & Static Page Generation Matrix

| Route Path | Page Title / Component | Render Mode | First Load JS | Smoke Test Status |
| :--- | :--- | :---: | :---: | :---: |
| **`/`** | Executive Command Center (ECC) | `○ Static` | 214 kB | `VERIFIED HEALTHY` |
| **`/root-cause`** | Root-Cause Decomposition Waterfall | `○ Static` | 114 kB | `VERIFIED HEALTHY` |
| **`/investigation`** | LangGraph 11-Node Investigation Trace | `○ Static` | 115 kB | `VERIFIED HEALTHY` |
| **`/decision-graph`** | Dynamic 6-Column Decision Topology | `○ Static` | 114 kB | `VERIFIED HEALTHY` |
| **`/evidence`** | SHA-256 Empirical Evidence Explorer | `○ Static` | 115 kB | `VERIFIED HEALTHY` |
| **`/recommendations`**| Action Plan & What-If Simulator | `○ Static` | 113 kB | `VERIFIED HEALTHY` |
| **`/briefing`** | Executive Briefing & Persona Generator| `○ Static` | 114 kB | `VERIFIED HEALTHY` |
| **`/_not-found`** | Custom 404 Error Boundary | `○ Static` | 88.4 kB | `VERIFIED HEALTHY` |

---

## 2. Client-Side Bundle Inspection

1. **Shared JavaScript Bundle:** 87.5 kB shared base bundle across all routes.
2. **Zero Secret Leakage:** Static asset scans confirm zero occurrences of `GROQ_API_KEY`, `GEMINI_API_KEY`, `AIzaSy...`, or internal filesystem paths.
3. **Graceful Offline Behavior:** React error boundaries capture backend unreachable states and display retry controls without breaking page layouts.
