# 🚀 InsightPilot AI

### AI-Powered Enterprise Decision Intelligence Platform

**InsightPilot AI** is an AI-powered decision-intelligence platform designed to help businesses understand:

> **What happened → Why did it happen → What should we do → What result can we expect?**

🔗 **Live Demo:** [InsightPilot AI — Live Demo](https://insigh-pilot-ai.vercel.app/?utm_source=chatgpt.com)

---

## 🎯 Why InsightPilot AI?

Traditional business dashboards are good at answering **"What happened?"**, but they often require users to manually investigate **why it happened** and **what action should be taken**.

For example:

> Revenue decreased by 15%.

A traditional dashboard may show the decrease, but the business user still needs to investigate:

* Was the decrease caused by lower sales?
* Was inventory unavailable?
* Did a particular product or region perform poorly?
* Which factors contributed most?
* What action could recover the lost revenue?

Generic AI systems also have another problem: an LLM may generate incorrect numbers or unsupported conclusions.

InsightPilot AI addresses these problems by combining:

**Deterministic Analytics + AI Reasoning + Evidence + Confidence Checks**

### Core Principle

> **The analytics engine calculates the truth. AI explains and investigates the truth.**

---

# 🏗️ Architecture

```text
                         ┌──────────────────────┐
                         │      User / User      │
                         │     Business Query   │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │      Next.js         │
                         │   React + Tailwind   │
                         │      Frontend        │
                         └──────────┬───────────┘
                                    │
                               REST API
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │       FastAPI        │
                         │       Backend        │
                         └──────────┬───────────┘
                                    │
                ┌───────────────────┼───────────────────┐
                ▼                   ▼                   ▼
        ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
        │ CSV /       │     │ Analytics   │     │ LangGraph   │
        │ Enterprise  │     │ Engine      │     │ AI Agent    │
        │ Data        │     │             │     │             │
        └─────────────┘     └─────────────┘     └──────┬──────┘
                                                        │
                                          ┌─────────────┴─────────────┐
                                          ▼                           ▼
                                    ┌───────────┐               ┌───────────┐
                                    │   Groq    │               │  Gemini   │
                                    │  Llama    │               │   Flash   │
                                    └───────────┘               └───────────┘
                                          │                           │
                                          └─────────────┬─────────────┘
                                                        ▼
                                              AI Investigation
                                                        │
                                                        ▼
                                           Confidence / Safety
                                                        │
                                                        ▼
                                         Recommendations & Simulation
                                                        │
                                                        ▼
                                             Executive Dashboard
```

---

# ✨ Key Features

### 📊 Business KPI Analysis

Analyzes important business metrics and detects unusual changes.

### 🔎 Root-Cause Analysis

Identifies the major factors contributing to a business anomaly.

### 🤖 AI Investigation

Uses a multi-step LangGraph workflow to investigate and explain validated business results.

### 📚 Evidence Explorer

Provides supporting records behind conclusions so users can trace the result back to source data.

### 🔐 Evidence Integrity

Uses SHA-256 hashing to help verify that evidence records have not been modified.

### 🛡️ Confidence & Abstention

If the available evidence is insufficient, the system can avoid presenting an unsupported conclusion.

### 💡 Recommendations

Generates actionable recommendations based on the validated analysis.

### 🔮 What-If Simulation

Allows users to explore potential actions and estimate their possible financial impact.

### 📈 Decision Graph

Visualizes the relationship between business factors, evidence, analysis, and recommendations.

### 📄 Executive Briefing

Provides an executive-friendly summary of the investigation and recommendations.

---

# 🔄 How the System Works

The complete workflow is:

```text
1. Data Collection
       ↓
2. Data Validation
       ↓
3. KPI / Anomaly Detection
       ↓
4. Root-Cause Analysis
       ↓
5. Evidence Collection
       ↓
6. Evidence Verification
       ↓
7. LangGraph AI Investigation
       ↓
8. Confidence / Safety Check
       ↓
9. Recommendations
       ↓
10. What-If Simulation
       ↓
11. Executive Briefing
```

### Important Design Decision

The LLM is **not responsible for calculating important financial values**.

Instead:

```text
Python Analytics
      ↓
Calculates validated business facts
      ↓
LangGraph
      ↓
Coordinates investigation
      ↓
LLM
      ↓
Interprets and explains results
```

This separation helps reduce AI hallucination and improves explainability.

---

# 🧠 AI Agent Workflow

InsightPilot AI uses **LangGraph** to orchestrate the multi-step investigation process.

```text
Business Problem
       ↓
Understand Problem
       ↓
Retrieve Validated Data
       ↓
Analyze KPI
       ↓
Find Root Causes
       ↓
Collect Evidence
       ↓
AI Investigation
       ↓
Confidence Check
       ↓
 ┌─────┴─────┐
 ↓           ↓
Strong      Weak
Evidence    Evidence
 ↓           ↓
Continue    Abstain
 ↓
Recommendation
 ↓
What-If Simulation
 ↓
Final Decision
```

LangGraph is used as the **workflow/orchestration framework**. It is not itself the AI model.

The actual reasoning is provided by the LLM, while LangGraph controls the sequence of operations and movement of information between workflow steps.

---

# 🛠️ Technology Stack

## Frontend

| Technology       | Purpose                        |
| ---------------- | ------------------------------ |
| **Next.js 14**   | Web application and dashboard  |
| **React 18**     | UI components and interactions |
| **Tailwind CSS** | Styling and responsive design  |

## Backend

| Technology      | Purpose                     |
| --------------- | --------------------------- |
| **Python 3.11** | Analytics and backend logic |
| **FastAPI**     | REST API layer              |
| **Pydantic**    | Request/response validation |
| **Uvicorn**     | FastAPI application server  |

## AI / Agent

| Technology                  | Purpose                           |
| --------------------------- | --------------------------------- |
| **LangGraph**               | Multi-step AI-agent orchestration |
| **Llama 3.3 70B via Groq**  | Main AI reasoning model           |
| **Google Gemini 2.5 Flash** | Alternative model / failover      |

## Data

| Technology           | Purpose                                           |
| -------------------- | ------------------------------------------------- |
| **CSV datasets**     | Enterprise-style ERP, CRM, inventory and EDI data |
| **Python analytics** | Data processing and deterministic calculations    |

> The current prototype uses normalized CSV datasets rather than a traditional database such as MongoDB or PostgreSQL.

## Reliability & Security

| Technology                | Purpose                         |
| ------------------------- | ------------------------------- |
| **SHA-256**               | Evidence integrity verification |
| **Environment variables** | Secure API credentials          |
| **Rate limiting**         | API protection                  |
| **Request IDs**           | Request tracing                 |
| **Security headers**      | Additional API security         |
| **Structured logging**    | Monitoring and debugging        |

## Testing & Reporting

| Technology          | Purpose                       |
| ------------------- | ----------------------------- |
| **Python unittest** | Backend and analytics testing |
| **jsPDF**           | PDF report generation         |

---

# 🧩 Problems Faced & Solutions

## 1. Different Data Sources

Enterprise systems can have different formats, identifiers, and missing values.

### Solution

Used normalized schemas, validation, and referential-integrity checks before running analytics.

---

## 2. AI Hallucination

An LLM can potentially generate incorrect numbers or unsupported evidence.

### Solution

Financial calculations and rankings are handled by deterministic Python analytics.

The AI receives validated results and focuses on investigation and explanation.

---

## 3. AI API Failures

External AI services can experience rate limits, downtime, or failures.

### Solution

Implemented model failover between Groq and Gemini along with fallback behavior.

---

## 4. Frontend / Backend Consistency

Changes in API responses can break frontend screens.

### Solution

Used Pydantic models, structured JSON contracts, API testing, and health checks.

---

## 5. Multi-Step Workflow Latency

Multiple AI and analytics operations can increase response time.

### Solution

Used fast models, structured outputs, workflow telemetry, and clearly separated workflow nodes.

---

## 6. Reliability & Security

API keys and user inputs need to be handled securely.

### Solution

Used environment variables for secrets, input validation, rate limiting, security headers, request IDs, and structured logging.

---

# 📱 Main Application Screens

The platform contains several major screens:

1. **Command Center**
2. **Root Cause Analysis**
3. **Investigation Trace**
4. **Decision Graph**
5. **Evidence Explorer**
6. **Recommendations**
7. **Executive Briefing**

---

# 🎯 Example Business Flow

Imagine the system detects:

```text
Revenue ↓ 15%
```

Instead of simply displaying this number, InsightPilot AI investigates:

```text
Revenue Decline
      ↓
Which factors changed?
      ↓
Inventory shortage
      ↓
Affected products / orders
      ↓
Supporting evidence
      ↓
AI investigation
      ↓
Confidence check
      ↓
Recommended action
      ↓
Potential recovery simulation
```

The result is therefore not just:

> **"Revenue decreased."**

It becomes:

> **"Revenue decreased because of identified contributing factors, supported by specific evidence, with recommended actions and estimated potential impact."**

---

# 🚀 Running the Project Locally

## Backend

```bash
cd backend

python -m venv venv

# Windows
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start FastAPI
uvicorn main:app --reload
```

Backend will normally be available at:

```text
http://localhost:8000
```

## Frontend

```bash
cd frontend

npm install

npm run dev
```

Frontend will normally be available at:

```text
http://localhost:3000
```

---

# 🔑 Environment Variables

Create a `.env` file for required API credentials.

Example:

```env
GROQ_API_KEY=your_groq_api_key
GEMINI_API_KEY=your_gemini_api_key
```

**Never commit API keys or `.env` files to GitHub.**

---

# 🧪 Testing

Backend tests can be executed using:

```bash
python -m unittest
```

The project also uses API health checks and validation to improve reliability.

---

# 🌐 Live Demo

### 🚀 Try InsightPilot AI

**https://insigh-pilot-ai.vercel.app/**

---

# 📌 Project Highlights

* AI-powered decision intelligence
* Multi-step AI-agent workflow
* LangGraph orchestration
* Deterministic financial analytics
* Root-cause analysis
* Evidence-backed AI reasoning
* Confidence and abstention checks
* Groq + Gemini model failover
* Evidence integrity using SHA-256
* What-if business simulation
* Executive dashboard
* PDF executive reporting

---

# 🧠 Key Engineering Principle

> **Don't ask the LLM to calculate the truth.**
>
> **Calculate the truth with reliable software, then let AI investigate, explain, and communicate it.**

---

# 👨‍💻 Project

**InsightPilot AI**

AI-powered enterprise decision intelligence platform.

🔗 **Live Application:** https://insigh-pilot-ai.vercel.app/

---

## ⭐ If you found this project interesting

Feel free to explore the live application and the source code, and use the project as a reference for building reliable AI-agent systems.
