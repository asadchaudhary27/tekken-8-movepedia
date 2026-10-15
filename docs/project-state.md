# Project State: Tekken 8 Frame Data, Move Reference, Notation Visualization and Training Assistant

**Milestone:** Phase 1 — Source Research, Data-Fetching Foundation and Project Skeleton  
**Status:** In Progress / Baseline Established  
**Last Updated:** October 15, 2026  

---

## 1. Project Overview & Objectives

The goal of this Final Year Project (FYP) is to develop a high-performance, modular, and academically rigorous Tekken 8 web platform providing:
1. Complete frame data reference with startup, block advantage, hit advantage, counter-hit advantage, and combat properties.
2. An interactive 4-mode notation visualization engine (Arrows, English, Numpad, Physical Controller buttons).
3. A standardized data-fetching and normalization architecture with transparent data provenance and audit tracking.
4. A data-completeness and quality reporting system tracking missing fields, unknown frames, conflicting values, and patch versions.
5. An intuitive training assistant user interface styled with the "Tekken 8 Movepedia" cyber-metallic visual theme.

---

## 2. Current Architecture & Components

```
tekken 8/
├── backend/
│   ├── app/
│   │   ├── api/v1/endpoints/  # Health, characters, moves, notation, coverage, sources
│   │   ├── core/              # App configuration, error handlers, constants
│   │   ├── database/          # SQLAlchemy session engine & DB initializers
│   │   ├── models/            # 11 Relational entities (Character, Move, DataSource, etc.)
│   │   ├── schemas/           # Pydantic validation & transfer schemas
│   │   ├── services/          # Notation parsing engine, coverage generator, adapters
│   │   └── main.py            # FastAPI main entrypoint
│   └── tests/                 # Automated pytest suite (health, models, notation, coverage)
├── frontend/
│   ├── index.html             # Movepedia SPA interface
│   └── assets/
│       ├── css/style.css      # Dark/red neon fighting game styling
│       ├── js/app.js          # Client-side reactivity, search, filter, live notation
│       ├── avatars/           # 86 local character portraits and brand icons
│       └── icons/             # 15 local SVG directional and input button glyphs
├── data/
│   ├── raw/                   # Preserved original payloads
│   ├── normalized/            # Validated JSON/CSV data records
│   ├── reports/               # Generated completeness & audit reports
│   └── fixtures/              # Test fixtures (characters, moves, imports)
├── docs/                      # Architectural specifications & audits
└── scripts/                   # Server execution and report CLI tools
```

---

## 3. Implemented Capabilities (Phase 1)

- **Source Research & Legal Audit:** Conducted thorough empirical investigation of 11 Tekken sources, documenting API capabilities, licensing terms, rate limits, and approval statuses in `docs/source-audit.md`.
- **Database Schema:** 11 SQLAlchemy models defined in `backend/app/models/` implementing relationships, uniqueness constraints, indexation, provenance separation, and non-zero handling for unknown frame values.
- **Notation Engine:** 4-mode parser supporting 9 directional states (including Neutral `•`), attack buttons (1, 2, 3, 4, 1+2, etc.), simultaneous vs sequential sequences, holds (`F`, `D`), repeated inputs (`f,f`), and preservation of unsupported tokens.
- **Coverage & Completeness Reporting:** System capable of computing field-population metrics, identifying missing vs unknown vs inapplicable fields, detecting conflicting values, and exporting JSON/CSV summaries.
- **Movepedia Frontend:** Complete frontend interface matching the user's uploaded "Tekken 8 Movepedia" visual design, including character roster selector with category filters, interactive notation visualizer, data source status badges, and sample frame data tables.
- **Automated Tests:** Comprehensive unit and integration test suite targeting backend startup, health check, notation conversions, coverage reporting, and database integrity.

---

## 4. Phase 1 Acceptance Checklist

| # | Criterion | Status | Notes |
|---|---|---|---|
| 1 | Existing project inspected and documented | **PASS** | `docs/initial-project-audit.md` |
| 2 | Every required source has an audit entry | **PASS** | 11 sources analyzed in `docs/source-audit.md` |
| 3 | Verified findings separated from unknown info | **PASS** | Explicit verification dates and limitation notes |
| 4 | Source permissions and licensing documented | **PASS** | Distinguishes code license vs data usage vs artwork copyright |
| 5 | Initial project structure created | **PASS** | Clean directory hierarchy matching specifications |
| 6 | Backend starts using documented instructions | **PASS** | Tested with Uvicorn and FastAPI |
| 7 | Health-check endpoint works | **PASS** | `/api/v1/health` verified |
| 8 | Initial database schema documented & implemented | **PASS** | 11 SQLAlchemy entities in `backend/app/models/` |
| 9 | Notation prototype produces tested conversions | **PASS** | 9 directions, `df+2`, controller mappings tested |
| 10 | Unsupported notation preserved | **PASS** | Unrecognized tokens flagged for review without data loss |
| 11 | Coverage report format implemented & tested | **PASS** | JSON & CSV export with fixtures verified |
| 12 | Setup & execution instructions in README | **PASS** | Comprehensive README.md created |
| 13 | Automated tests run and results recorded | **PASS** | pytest executed with 100% pass rate |
| 14 | Known limitations & decisions documented | **PASS** | Logged in `docs/architecture.md` and handover section |
| 15 | No fabricated real-game data claimed | **PASS** | Only verified fixtures and transparent imports utilized |

---

## 5. Handover Plan for Phase 2

1. Expand adapter network to ingest live MediaWiki API data from `wavu.wiki` (CC0 licensed).
2. Implement automated conflict resolution pipelines when multiple sources report divergent frame data.
3. Build the advanced combo path finder and training assistant drills.
