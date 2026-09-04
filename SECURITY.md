# Security & Responsible AI Policy

> **InsightPilot AI — Enterprise Decision-Intelligence Platform**  
> *Accenture Innovation Challenge 2026 — Track 3: BusinessIntelligence.ai*

---

## 🛡️ Security Architecture & Philosophy

InsightPilot AI is engineered with defense-in-depth security, credential isolation, and strict responsible AI governance.

---

## 🔒 Credential Safety & Isolation

1. **Zero Secret Leakage:**
   - Raw API keys (Groq, Google Gemini) are isolated within server-side environment variables and are **never** returned in client payloads, WebSocket messages, or telemetry event traces.
   - Client responses and trace endpoints only expose sanitized logical pool identifiers (`groq_pool_1`, `groq_pool_2`, `gemini_pool_1`, `gemini_pool_2`, `deterministic_fallback`).
2. **Environment Protection:**
   - Git ignore rules strictly prevent committing `.env`, `.env.local`, and other credential files.
   - All secret fields are excluded from Pydantic serialization models.

---

## 🧠 Responsible AI & Anti-Hallucination Governance

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                    RESPONSIBLE AI GOVERNANCE GUARANTEES                     │
├────────────────────────┬──────────────────────────┬─────────────────────────┤
│ 1. FACTUAL GROUNDING   │ 2. MANDATORY ABSTENTION  │ 3. CRYPTOGRAPHIC AUDIT  │
│ Strict schema contexts │ Suspends LLM generation  │ SHA-256 hash digests on │
│ forbid hallucination   │ if confidence < 65%      │ every empirical finding │
├────────────────────────┼──────────────────────────┼─────────────────────────┤
│ 4. DETERMINISTIC TRUTH │ 5. POST-GEN VALIDATION   │ 6. DATA PRIVACY         │
│ Financial metrics are  │ Regex validator rejects  │ Zero training on user   │
│ 100% Python-computed   │ ungrounded citations     │ or enterprise data      │
└────────────────────────┴──────────────────────────┴─────────────────────────┘
```

1. **Deterministic Truth Boundary:** Generative AI models are strictly constrained to explaining validated facts; they are technically incapable of modifying financial totals, variances, or driver contributions.
2. **Mandatory Abstention Gate:** If empirical evidence is insufficient or analytical confidence falls below `65%`, the system suppresses generative LLM calls and returns a transparent abstention state.
3. **Post-Generation Grounding Validator:** Every LLM response is parsed and validated against the input context container; any hallucinated evidence citations trigger immediate response rejection.
4. **Data Privacy:** Customer data is processed statelessly and is never used to train or fine-tune public foundation models.

---

## 🚨 Reporting a Vulnerability

If you discover a security vulnerability or credential exposure in InsightPilot AI, please report it responsibly:

* **Email:** [sumit.chahal@example.com](mailto:sumit.chahal@example.com)
* **Response SLA:** Vulnerability reports will be acknowledged within 24 hours with a mitigation roadmap.
* **Responsible Disclosure:** Please do not open public GitHub issues for security vulnerabilities.
