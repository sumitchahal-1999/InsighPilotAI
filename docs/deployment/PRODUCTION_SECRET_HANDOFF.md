# InsightPilot AI — Production Secret & Environment Handoff

**Project:** InsightPilot AI  
**Competition:** Accenture Innovation Challenge 2026 (Track 3: BusinessIntelligence.ai)  
**Document:** Workstream D — Production Environment Variables & Secure Credential Handoff  
**Status:** `SECURITY SANITIZED — ZERO REAL SECRETS COMMITTED`

---

## 1. Security Compliance & Zero Leakage Guarantee

> [!IMPORTANT]
> This document contains **PLACEHOLDERS ONLY**. Real API keys, database credentials, and production secrets must **NEVER** be committed to version control, documentation, or public pull requests.

All real values must be injected directly into the cloud hosting platform's secure environment variable dashboard (e.g., Vercel Environment Variables, Render Environment Variables).

---

## 2. Backend Cloud Environment Configuration (e.g. Render Dashboard)

Configure the following key-value pairs in your backend service dashboard:

```bash
# ------------------------------------------------------------------------------
# 1. Application Mode
# ------------------------------------------------------------------------------
APP_ENV=production

# ------------------------------------------------------------------------------
# 2. CORS Whitelist (Set to your actual deployed frontend HTTPS domain)
# ------------------------------------------------------------------------------
CORS_ORIGINS=https://[YOUR_FRONTEND_URL]

# ------------------------------------------------------------------------------
# 3. AI Provider Credentials (Optional — API operates cleanly with fallback)
# ------------------------------------------------------------------------------
# Obtain at https://console.groq.com/
GROQ_API_KEY_1=[YOUR_GROQ_API_KEY]
GROQ_API_KEY_2=[YOUR_GROQ_BACKUP_KEY]
GROQ_MODEL=llama-3.3-70b-versatile

# Obtain at https://aistudio.google.com/
GEMINI_API_KEY_1=[YOUR_GEMINI_API_KEY]
GEMINI_API_KEY_2=[YOUR_GEMINI_BACKUP_KEY]
GEMINI_MODEL=gemini-2.5-flash

# ------------------------------------------------------------------------------
# 4. Responsible AI Safety Controls (Locked Canonical Values)
# ------------------------------------------------------------------------------
CONFIDENCE_ABSTENTION_THRESHOLD=0.65
MATERIALITY_VARIANCE_THRESHOLD=-0.03

# ------------------------------------------------------------------------------
# 5. Database Connection (Optional — defaults to SQLite if omitted)
# ------------------------------------------------------------------------------
DATABASE_URL=postgresql://[DB_USER]:[DB_PASSWORD]@[DB_HOST]:5432/[DB_NAME]
```

---

## 3. Frontend Cloud Environment Configuration (e.g. Vercel Dashboard)

Configure the following key-value pair in your frontend project settings:

```bash
# ------------------------------------------------------------------------------
# Frontend API Gateway URL (Points to your live backend service)
# ------------------------------------------------------------------------------
NEXT_PUBLIC_API_URL=https://[YOUR_BACKEND_URL]
```

---

## 4. Verification of Client-Side Secret Isolation

| Variable Name | Present in Client Bundle? | Classification |
| :--- | :---: | :--- |
| `NEXT_PUBLIC_API_URL` | **YES** | Safe (Public API endpoint address). |
| `GROQ_API_KEY_*` | **NO** (Filtered) | Secure (Never exposed to browser). |
| `GEMINI_API_KEY_*` | **NO** (Filtered) | Secure (Never exposed to browser). |
| `DATABASE_URL` | **NO** (Filtered) | Secure (Never exposed to browser). |
