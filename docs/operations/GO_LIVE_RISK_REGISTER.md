# InsightPilot AI — Go-Live Production Risk Register

**Project:** InsightPilot AI  
**Competition:** Accenture Innovation Challenge 2026 (Track 3: BusinessIntelligence.ai)  
**Document:** Operational Risk Assessment, Mitigation Strategies & Action Items  
**Status:** `RISK REGISTER ACTIVE & MANAGED`

---

## 1. Production Go-Live Risk Register

| # | Risk Description | Category | Likelihood | Impact | Current Mitigation | Remaining Action | Owner Type | Status |
| :-: | :--- | :--- | :---: | :---: | :--- | :--- | :---: | :---: |
| **R1** | Third-party AI API rate limits (429) during demo. | AI Provider | Medium | Low | Multi-key pool rotation + instant local deterministic fallback. | Inject live backup keys in Render. | Project Owner | `MITIGATED` |
| **R2** | CORS mismatch between Vercel and Render. | Configuration | Low | High | Standardized `CORS_ORIGINS` parsing supports explicit HTTPS origins. | Verify exact Vercel URL in Render config. | DevOps / Ops | `MITIGATED` |
| **R3** | Render free-tier cold starts (&gt;30s spin-up). | Availability | Medium | Medium | Sub-millisecond `/health` probe available for synthetic keep-alive pingers. | Configure 5-minute UptimeRobot ping. | DevOps / Ops | `PLANNED` |
| **R4** | Secret leakage in client bundle or Git history. | Security | Low | Critical | Hardened `.gitignore`, placeholder `.env.example`, client bundle variable stripping. | Maintain zero secrets in repo. | Dev Team | `VERIFIED SAFE` |
| **R5** | CSV dataset tampering or corruption. | Data Integrity | Low | Critical | Dataset validation suite (`validate_dataset.py`) locks schemas and rows. | Automated CI pipeline validation. | Dev Team | `VERIFIED SAFE` |
| **R6** | Mathematical variance calculation drift. | Deterministic Truth | Low | Critical | Automated regression suite (240 tests) locks all canonical metrics. | Run full test suite prior to release. | Dev Team | `VERIFIED SAFE` |

---

## 2. Risk Mitigation Summary

All **High and Critical Severity** risks have verified architectural mitigations embedded in the codebase. Remaining items are purely operational configuration steps on external cloud dashboards.
