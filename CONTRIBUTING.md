# Contributing to InsightPilot AI

Thank you for your interest in contributing to **InsightPilot AI** (*Accenture Innovation Challenge 2026 — Track 3: BusinessIntelligence.ai*)!

---

## 🏛️ Core Architectural Principle

All contributors must uphold the platform's foundational invariant:

> **"Deterministic systems own quantitative truth. LangGraph orchestrates investigation. AI explains grounded facts."**
> 
> *Large Language Models (LLMs) are strictly forbidden from computing metrics, inventing driver contributions, fabricating evidence citations, or generating ungrounded financial recovery estimates.*

---

## 🛠️ Local Development Setup

### 1. Prerequisites
* Python 3.11+ (Python 3.13 recommended)
* Node.js 18+ (Node.js 20+ recommended) & npm
* Git

### 2. Backend Setup
```bash
# Clone the repository
git clone https://github.com/ayus1234/InsighPilotAI.git
cd InsighPilotAI

# Create and activate Python virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env

# Run FastAPI backend
uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload
```

### 3. Frontend Setup
```bash
cd frontend/next-app

# Install dependencies
npm install

# Start Next.js development server
npm run dev
```

---

## 🧪 Verification & Testing Standards

Every contribution must pass the full verification suite with **zero regressions**:

```bash
# 1. Validate dataset schema and referential integrity
python tests/validate_dataset.py

# 2. Run comprehensive unit, integration, and E2E regression tests
python -m unittest discover -s tests -t . -p "test_*.py" -v

# 3. Verify Next.js production build compiles cleanly
cd frontend/next-app && npm run build
```

---

## 📋 Pull Request Workflow

1. **Branch Naming:** Use descriptive branch names:
   - `feat/feature-name`
   - `fix/bug-description`
   - `docs/documentation-update`
   - `test/test-enhancement`
2. **Commit Messages:** Follow Conventional Commits format:
   - `feat(scope): add new capability`
   - `fix(scope): resolve issue`
   - `docs(scope): update documentation`
3. **Zero Credential Policy:** Ensure no `.env` files, API keys, or private tokens are committed.
4. **Code Quality:** Ensure all Python code is typed with Pydantic / standard type hints and Next.js code is strict TypeScript.
