# Tekken 8 Frame Data, Move Reference, Notation Visualization and Training Assistant Website

**Academic Project:** Computer Science Final Year Project (FYP)  
**Milestone:** Phase 1 — Source Research, Data-Fetching Foundation and Project Skeleton  
**Status:** Completed & Validated  
**Author:** Senior Software Architect & Lead Developer  
**Date:** October 15, 2026  

---

## 1. Project Overview

This project is an academic Final Year Project developing a web-based **Tekken 8 Movepedia & Training Assistant**. It is designed to provide:
1. **Accurate Frame Data & Move References:** Startup frames, block advantage, hit advantage, counter-hit advantage, hit levels, damage, and combat properties.
2. **Interactive 4-Mode Notation Visualization:** Real-time translation of Tekken input notation into Directional Arrows, English names, Numpad notation, and Physical Controller layouts (PlayStation, Xbox, Arcade).
3. **Transparent Data-Fetching & Provenance:** Modular source-adapter architecture with rate limiting, legal compliance tracking, and raw payload archiving.
4. **Data Completeness & Quality Auditing:** Mathematical coverage reporting separating missing, unknown, not provided, and inapplicable attributes.
5. **Movepedia User Interface:** A responsive, dark cyber-metallic fighting game interface matching modern fighting game aesthetics with zero external JavaScript frameworks.

---

## 2. Technology Stack

- **Backend:** Python 3.12 with FastAPI (ASGI REST API)
- **Database:** SQLite 3 (Standard SQL syntax engineered for seamless PostgreSQL migration)
- **ORM:** SQLAlchemy 2.0+ (Declarative Mapping)
- **Data Validation & Schemas:** Pydantic v2 & Pydantic-Settings
- **Frontend:** HTML5, CSS3, and Vanilla ES6 JavaScript (No bloated external UI frameworks)
- **Testing:** pytest & HTTPX
- **API Documentation:** Interactive OpenAPI / Swagger (`/docs`) and ReDoc (`/redoc`)
- **Version Control:** Git

---

## 3. Project Directory Hierarchy

```
tekken 8/
├── backend/
│   ├── app/
│   │   ├── api/v1/endpoints/  # Health, characters, moves, notation, coverage, sources
│   │   ├── core/              # Config settings, domain exceptions, error handlers
│   │   ├── database/          # SQLAlchemy session engine & DB init/seed scripts
│   │   ├── models/            # 11 Relational entities (Character, Move, Source, etc.)
│   │   ├── schemas/           # Pydantic v2 schemas for requests & responses
│   │   ├── services/          # Notation engine, coverage generator, source adapters
│   │   └── main.py            # FastAPI main application
│   └── tests/                 # Comprehensive automated pytest test suite
├── frontend/
│   ├── index.html             # Movepedia single-page application interface
│   └── assets/
│       ├── css/style.css      # Dark/red cyber-metallic fighting game styles
│       ├── js/app.js          # Reactive vanilla JS controller
│       ├── avatars/           # 86 local character brand renders & portraits
│       └── icons/             # 15 local SVG directional and attack button glyphs
├── data/
│   ├── raw/                   # Preserved original API payloads
│   ├── normalized/            # Standardized JSON/CSV datasets
│   ├── reports/               # Generated completeness & coverage reports (JSON/CSV)
│   └── fixtures/              # Validated offline test fixtures
├── docs/
│   ├── initial-project-audit.md  # Inspection of pre-existing website mirrors
│   ├── source-audit.md           # Audit of 11 external sources & legal permissions
│   ├── architecture.md           # System architecture, adapter pattern & notation specs
│   ├── data-dictionary.md        # Entity definitions, types, indexes & nullability rules
│   ├── coverage-report-design.md # Coverage formulas and JSON/CSV specifications
│   ├── project-state.md          # Current project state & Phase 1 checklist
│   └── changelog.md              # Semantic release changelog
├── scripts/
│   ├── init_db.py             # CLI database creation and seeding tool
│   ├── run_server.py          # CLI backend development server runner
│   └── generate_report.py     # CLI coverage & data completeness report generator
├── .env.example               # Environment configuration template
├── .gitignore                 # Version control exclusions
├── requirements.txt           # Python package dependencies
└── README.md                  # Project documentation
```

---

## 4. Setup & Installation Instructions

### Prerequisites
- Python 3.12 (or installed via `uv` / standard python.exe)
- Git

### Step-by-Step Setup

1. **Clone or navigate to the repository root:**
   ```bash
   cd "I:\tekken 8"
   ```

2. **Create and activate a virtual environment:**
   Using standard Python or `uv`:
   ```bash
   uv venv
   # Or: python -m venv .venv
   ```

3. **Install dependencies:**
   ```bash
   uv pip install -r requirements.txt
   # Or: .venv\Scripts\pip install -r requirements.txt
   ```

4. **Configure environment variables:**
   ```bash
   cp .env.example .env
   ```

5. **Initialize and seed the database:**
   ```bash
   $env:PYTHONPATH = "I:\tekken 8"
   .venv\Scripts\python.exe scripts/init_db.py
   ```

---

## 5. Execution Instructions

### Launch the Application Server
Run the backend web server with live reloading:
```bash
$env:PYTHONPATH = "I:\tekken 8"
.venv\Scripts\python.exe scripts/run_server.py
```
- **Web Application:** `http://127.0.0.1:8000/`
- **Swagger UI:** `http://127.0.0.1:8000/docs`
- **ReDoc:** `http://127.0.0.1:8000/redoc`

### Generate Coverage Reports via CLI
```bash
$env:PYTHONPATH = "I:\tekken 8"
.venv\Scripts\python.exe scripts/generate_report.py
```
Exports JSON and CSV reports into `data/reports/`.

---

## 6. Running Automated Tests

Run the full automated test suite using `pytest`:
```bash
$env:PYTHONPATH = "I:\tekken 8"
.venv\Scripts\pytest -v backend/tests
```

### Verified Test Results (2026-10-15):
```
backend/tests/test_coverage.py::test_empty_coverage_report_generation PASSED
backend/tests/test_coverage.py::test_populated_coverage_report_and_export PASSED
backend/tests/test_database.py::test_character_and_move_relationships PASSED
backend/tests/test_database.py::test_uniqueness_constraint_prevents_duplicates PASSED
backend/tests/test_database.py::test_nullable_frame_handling_preserves_none PASSED
backend/tests/test_health.py::test_health_check_endpoint PASSED
backend/tests/test_health.py::test_openapi_docs_endpoint PASSED
backend/tests/test_notation.py::test_all_nine_directions PASSED
backend/tests/test_notation.py::test_df_plus_2_test_case PASSED
backend/tests/test_notation.py::test_simultaneous_vs_sequential_inputs PASSED
backend/tests/test_notation.py::test_holds_and_repeated_inputs PASSED
backend/tests/test_notation.py::test_unsupported_notation_preservation PASSED
backend/tests/test_source_audit.py::test_data_sources_approval_status PASSED
backend/tests/test_source_audit.py::test_fixture_adapter_import_and_error_handling PASSED

======================== 14 passed in 2.34s ========================
```

---

## 7. Data Sources & Legal Compliance Summary

11 external sources were empirically investigated and audited in `docs/source-audit.md`:

| Source | Status | Licensing & Usage Rationale |
|---|---|---|
| **WavuWiki (`wavu.wiki`)** | **APPROVED** | Authoritative community database under **Creative Commons Zero (CC0 1.0)** / Public Domain. Designated as primary automated ingestion target via `/w/api.php`. |
| **TekkenDocs (`tekkendocs.com`)** | **APPROVED WITH RESTRICTIONS** | Proprietary code; community data use permitted with mandatory attribution to `tekkendocs.com` and `rbnorway.org`. |
| **T8 Notation Maker** | **APPROVED WITH RESTRICTIONS** | MIT code license for notation syntax models. |
| **Tekken8.org Frame Data** | **RESEARCH ONLY** | Cross-referencing and test fixture verification. |
| **Official Tekken / Bandai Namco** | **BLOCKED PENDING PERMISSION** | Proprietary intellectual property. |

---

## 8. Academic Integrity & Ethics

- Factual game frame data represents mathematical rules and measurements of game systems.
- Proprietary game artwork and trademarks remain the sole property of Bandai Namco Entertainment Inc.
- All community-curated data sources are explicitly credited in compliance with academic research standards.
