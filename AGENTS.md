# AGENTS.md — Master AI Development Instructions

> **Platform:** Tekken 8 Movepedia & Tournament Lab (Academic FYP)  
> **Repository:** `i:\tekken 8` | **Branch:** `main` | **Target Patch:** `v3.00.02` (Season 2 Standard)  
> **Core Architecture:** Python 3.12 (FastAPI) + SQLite 3 (SQLAlchemy 2.0) + Vanilla ES6 SPA (zero UI frameworks)

---

## 1. Documentation Index & Mandatory Reading Triggers

Before modifying any file, consult the specific documentation below:

| When You Are... | You MUST Read | Purpose |
|---|---|---|
| **Starting any new task or planning changes** | [docs/PROJECT_CONTEXT.md](docs/PROJECT_CONTEXT.md)<br>[docs/CHANGE_POLICY.md](docs/CHANGE_POLICY.md) | Understand project purpose, tech stack constraints, and strict preservation rules. |
| **Touching UI, CSS, buttons, cards, or layouts** | [docs/DESIGN_SYSTEM.md](docs/DESIGN_SYSTEM.md) | Standard design tokens, button sizes, grid stops, color palette, and accessibility. |
| **Adding/modifying endpoints, models, or services** | [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)<br>[docs/DATA_AND_INTEGRATIONS.md](docs/DATA_AND_INTEGRATIONS.md) | Code ownership, directory layout, routing, database schemas, and data pipelines. |
| **Investigating features, bugs, or scope** | [docs/FEATURE_INVENTORY.md](docs/FEATURE_INVENTORY.md) | Verified status of all 43 fighters, 18 stages, 1,203 moves, and tools. |
| **Running tests or validating changes** | [docs/TESTING.md](docs/TESTING.md) | Exact test commands, smoke tests, test suite layout (148 tests passing). |
| **Ending turn, handing off, or logging changes** | [docs/WORKLOG.md](docs/WORKLOG.md) | Record concise work summaries, verified status, and pending tasks. |

---

## 2. Core Operational Commandments

1. **Strict Feature & Code Preservation:**
   - Preserve all existing routes, features, business logic, and UI components by default.
   - Modify only what the user explicitly requested and the minimum supporting code necessary.
   - Treat unrequested features as strictly protected.
2. **Zero Framework Bloat:**
   - The frontend is strictly **Vanilla HTML5, CSS3, and ES6 JavaScript**. Do NOT introduce React, Vue, Tailwind, Bootstrap, or build tools (Vite, Webpack) unless explicitly authorized by the user.
3. **Architecture & Database Integrity:**
   - Database is SQLite (`tekken8_fyp.db`). Do NOT drop tables or replace the database engine.
   - Serverless / Vercel compatibility is maintained via `/tmp` database copying in `backend/app/database/session.py`. Never revert this mechanism.
4. **No Speculative or Destructive Changes:**
   - Do NOT delete, rename, or relocate files unless authorized.
   - Never overwrite documentation blindly; merge useful facts.
   - Never claim tests passed without executing them.
5. **Secrets & Security:**
   - Never commit or expose passwords, JWT secrets, TOTP seeds, or API tokens in code or documentation. Use `.env` and environment variables.

---

## 3. Environment & Execution Cheat Sheet

- **OS / Shell:** Windows 11 / PowerShell
- **Virtual Environment:** `.\.venv\Scripts\python.exe`
- **Run Pytest:** `.\.venv\Scripts\pytest backend/tests` (uses `pytest.ini`)
- **Run Dev Server:** `.\.venv\Scripts\uvicorn main:app --reload --port 8000`
- **Root Entrypoint:** `main.py` (`app = FastAPI(...)`)
- **Vercel Entrypoint:** `api/index.py` (`vercel.json`)
