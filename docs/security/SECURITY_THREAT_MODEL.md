# InsightPilot AI — Security Threat Model & Risk Analysis

**Project:** InsightPilot AI  
**Competition:** Accenture Innovation Challenge 2026 (Track 3: BusinessIntelligence.ai)  
**Document:** STRIDE Threat Modeling, Attack Vectors & Defensive Controls  
**Status:** `THREAT MODEL AUDIT COMPLETE`

---

## 1. STRIDE Threat Analysis Matrix

| Threat Category | Specific Attack Vector | Target Surface | Severity | Defensive Mitigation Implemented |
| :--- | :--- | :--- | :---: | :--- |
| **Spoofing** | Forged Client Request IDs | HTTP Request Headers | Low | `RequestCorrelationMiddleware` sanitizes/replaces malformed IDs. |
| **Tampering** | Parameter Tampering in Scenarios | `POST /simulations/run` | Medium | Pydantic v2 numeric bounds enforcement (`0.0 <= pct <= 100.0`). |
| **Repudiation** | Denying Provenance of Evidence | Evidence Lineage | High | SHA-256 cryptographic hashes link every record to source rows. |
| **Information Disclosure** | Secret / Key Leakage in Logs | Telemetry Stream | Critical | `OBSERVABILITY_SECURITY_POLICY.md` strictly strips API keys. |
| **Information Disclosure** | Internal Filepath Exposure | Error Responses | High | `register_error_handlers` masks stack traces from public payloads. |
| **Denial of Service** | Upstream AI Provider Rate Limits | AI Generation | Medium | Dual-pool key rotation + instant fallback to local grounded synthesis. |
| **Elevation of Privilege**| Unauthorized Cross-Origin Queries | Browser Fetch API | High | Strict origin whitelist in `CORS_ORIGINS` (`allow_credentials=False` for `*`). |
| **Browser Attacks** | Clickjacking / Frame Hijacking | Frontend UI | Medium | `X-Frame-Options: DENY` and `frame-ancestors: 'none'`. |
| **Supply Chain** | Vulnerable Python/Node Dependencies| Build Pipeline | Medium | Pinned dependency versions in `requirements.txt` and `package-lock.json`. |

---

## 2. LLM-Specific Threat Model: Anti-Hallucination & Prompt Injection

1. **Deterministic Containment:** Quantitative metrics are calculated by deterministic Python engines before prompt construction; the LLM has zero arithmetic authority.
2. **Context Sandboxing:** Prompts contain only sanitized numerical summaries and evidence IDs (`EVID_INV_ATL_001`); raw customer PII is excluded.
3. **Post-Generation Grounding Validator:** Rejects any AI narrative that cites unverified or hallucinated evidence IDs.
