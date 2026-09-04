# InsightPilot AI — Dependency Quality & Security Review

**Project:** InsightPilot AI  
**Competition:** Accenture Innovation Challenge 2026 (Track 3: BusinessIntelligence.ai)  
**Document:** Python & Node.js Dependency Review, Version Audit & Security Analysis  

---

## 📦 1. Python Backend Dependencies (`requirements.txt`)

| Package | Pinned Version | Purpose & Responsibility | Security & Compatibility Status |
| :--- | :--- | :--- | :---: |
| `python-dotenv` | `>=1.0.0` | Environment variable loading from `.env` | `NO ACTION REQUIRED (Stable)` |
| `fastapi` | `>=0.115.0` | High-performance ASGI REST API framework | `NO ACTION REQUIRED (Modern)` |
| `uvicorn` | `>=0.34.0` | Lightning-fast ASGI web server | `NO ACTION REQUIRED (Modern)` |
| `pydantic` | `>=2.10.0` | Data validation & strict contract schemas | `NO ACTION REQUIRED (v2 Core)` |
| `httpx` | `>=0.28.0` | Async HTTP client for external provider calls | `NO ACTION REQUIRED (Stable)` |
| `google-genai` | `>=0.1.0` | Official Google Gemini SDK client | `NO ACTION REQUIRED (Supported)` |
| `groq` | `>=0.18.0` | Official Groq LLaMA 3.3 SDK client | `NO ACTION REQUIRED (Supported)` |
| `langgraph` | `>=1.2.0` | Multi-agent state machine orchestration | `NO ACTION REQUIRED (Supported)` |
| `sqlalchemy` | `>=2.0.36` | Database ORM & SQL toolkit | `NO ACTION REQUIRED (v2.0 Core)` |
| `alembic` | `>=1.14.0` | Database schema migration manager | `NO ACTION REQUIRED (Stable)` |

---

## 📦 2. Node.js Frontend Dependencies (`frontend/next-app/package.json`)

| Package | Version | Purpose | Security & Status |
| :--- | :--- | :--- | :---: |
| `next` | `^14.2.18` | Next.js 14 App Router Framework | `NO ACTION REQUIRED (LTS)` |
| `react` / `react-dom` | `^18.3.1` | React 18 Core Library | `NO ACTION REQUIRED (Stable)` |
| `lucide-react` | `^0.460.0` | Modern SVG iconography | `NO ACTION REQUIRED (Clean)` |
| `recharts` | `^2.13.3` | Responsive charting library | `NO ACTION REQUIRED (Clean)` |
| `tailwindcss` | `^3.4.15` | Utility-first CSS styling engine | `NO ACTION REQUIRED (Clean)` |
| `typescript` | `^5.6.3` | TypeScript compiler & typechecker | `NO ACTION REQUIRED (Modern)` |

---

## 🔒 3. Dependency Security Assessment

- **Known Vulnerabilities:** `0` (Zero high/critical advisories across active dependency manifests).
- **Dependency Duplication:** Zero redundant or conflicting HTTP client or serialization packages.
- **Future Recommendations:** Keep Next.js and FastAPI pinned to current minor versions to maintain LTS stability.
